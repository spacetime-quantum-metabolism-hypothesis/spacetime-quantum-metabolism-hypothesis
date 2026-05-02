"""
L410 — Cluster anchor pool expansion: multi-cluster joint fit + dominance analysis.

Goal: paper §6.1 row 8 (single-source dominance 59.7%) RECOVERY 가속도 평가.
- Pool sizes N ∈ {3, 5, 8, 13}
- 3 dominance metrics (variance share / chi2-leverage / LOO regression)
- LOO + L2O sensitivity
- LCDM mock injection FDR (N-scaling)
- AICc penalty (CLAUDE.md 공통원칙)

★ 정직: published σ₀(env) 값이 단일 통합 표로 archive 되어 있지 않음.
   본 스크립트는 plausible mock (Tier-1/2/3 분포 기반) 으로 *forecast* 만 제공.
   실제 archive crawl 은 별도 LXX 위임.

병렬 실행: multiprocessing.spawn pool, OMP/MKL/OPENBLAS=1 강제.
"""
from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import json
import multiprocessing as mp
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent.parent.parent / "results" / "L410"
OUT.mkdir(parents=True, exist_ok=True)

RNG_MASTER = np.random.default_rng(20260501)


# ----------------------------------------------------------------------
# 1. Cluster pool (mock; plausible Tier-1/2/3 분포)
# ----------------------------------------------------------------------
# 각 entry: (name, log10(rho_env / rho_crit), sigma0_obs, sigma0_err, tier)
# rho_env: cluster-scale 환경밀도 dynamic range 약 [2, 4] log10
# sigma0: σ₀(env) 의 가상의 측정값 (paper §3.4 의 비단조 구조에 *부분적으로* 일치하도록 잡음 포함)
POOL = [
    # Tier-1 weak-lensing (anchors + LoCuSS/CLASH)
    ("A1689",       3.5, 0.85, 0.10, 1),  # current anchor
    ("A1703",       3.3, 0.78, 0.13, 1),
    ("A2218",       3.2, 0.72, 0.14, 1),
    ("MACS J1149",  3.7, 0.91, 0.16, 1),
    ("MACS J0717",  3.8, 1.05, 0.20, 1),  # merging — heterogeneity flag
    ("RXJ1347",     3.9, 0.97, 0.15, 1),
    ("A2261",       3.4, 0.80, 0.13, 1),
    ("MS2137",      3.6, 0.88, 0.14, 1),
    # Tier-2 X-ray hydrostatic
    ("Coma",        2.8, 0.55, 0.08, 2),  # current anchor
    ("Perseus",     3.0, 0.62, 0.09, 2),  # current anchor
    ("A1795",       2.9, 0.58, 0.10, 2),
    ("A2029",       3.1, 0.65, 0.11, 2),
    ("A478",        3.0, 0.60, 0.10, 2),
]
# subset definitions
SUBSETS = {
    3: ["A1689", "Coma", "Perseus"],
    5: ["A1689", "Coma", "Perseus", "A1703", "MACS J1149"],
    8: ["A1689", "Coma", "Perseus", "A1703", "MACS J1149", "RXJ1347", "A2261", "A1795"],
    13: [c[0] for c in POOL],
}


def select(names):
    by = {c[0]: c for c in POOL}
    return [by[n] for n in names]


# ----------------------------------------------------------------------
# 2. Models
# ----------------------------------------------------------------------
def model_monotonic(rho, theta):
    a, b = theta
    return a + b * rho


def model_three_regime(rho, theta):
    # piecewise affine with two break points
    a, b1, b2, b3, r1, r2 = theta
    out = np.empty_like(rho)
    m1 = rho < r1
    m3 = rho > r2
    m2 = ~(m1 | m3)
    out[m1] = a + b1 * rho[m1]
    # ensure continuity at r1, r2
    a2 = a + b1 * r1 - b2 * r1
    out[m2] = a2 + b2 * rho[m2]
    a3 = a2 + b2 * r2 - b3 * r2
    out[m3] = a3 + b3 * rho[m3]
    return out


def chi2(model, theta, data):
    rho = np.array([d[1] for d in data])
    y = np.array([d[2] for d in data])
    e = np.array([d[3] for d in data])
    return float(np.sum(((y - model(rho, theta)) / e) ** 2))


def fit(model, data, kparam, n_starts=64, seed=0):
    from scipy.optimize import minimize

    rho = np.array([d[1] for d in data])
    y = np.array([d[2] for d in data])
    rng = np.random.default_rng(seed)
    best = (np.inf, None)
    for _ in range(n_starts):
        if model is model_monotonic:
            x0 = np.array([y.mean() - 0.3 * rho.mean(), 0.3]) + 0.1 * rng.standard_normal(2)
        else:
            x0 = np.array([
                y.mean() - 0.3 * rho.mean(),
                rng.uniform(0.0, 0.5),
                rng.uniform(-0.2, 0.5),
                rng.uniform(0.0, 0.5),
                rng.uniform(rho.min() + 0.1, rho.mean()),
                rng.uniform(rho.mean(), rho.max() - 0.1),
            ])
        try:
            res = minimize(lambda t: chi2(model, t, data), x0, method="Nelder-Mead",
                           options={"xatol": 1e-5, "fatol": 1e-6, "maxiter": 4000})
            if res.fun < best[0]:
                best = (float(res.fun), res.x.copy())
        except Exception:
            continue
    if best[1] is None:
        return float("nan"), None
    return best


def aicc(chi2_val, k, n):
    aic = chi2_val + 2 * k
    if n - k - 1 <= 0:
        return float("inf")
    return aic + 2 * k * (k + 1) / (n - k - 1)


# ----------------------------------------------------------------------
# 3. Dominance metrics
# ----------------------------------------------------------------------
def dominance_variance_share(data):
    e = np.array([d[3] for d in data])
    w = 1.0 / e ** 2
    s = w / w.sum()
    return float(s.max())


def dominance_chi2_leverage(model, theta, data):
    """Cook's-distance-like: 한 cluster 제거 시 Δχ² / total χ²."""
    base = chi2(model, theta, data)
    deltas = []
    for i in range(len(data)):
        sub = data[:i] + data[i + 1:]
        deltas.append(base - chi2(model, theta, sub))
    deltas = np.array(deltas)
    return float(deltas.max() / max(base, 1e-9))


def dominance_loo_regression(model, data, kparam):
    """한 cluster 제거 시 best-fit theta 변화 비율."""
    base_chi2, base_theta = fit(model, data, kparam, n_starts=24, seed=11)
    if base_theta is None:
        return float("nan")
    norms = []
    for i in range(len(data)):
        sub = data[:i] + data[i + 1:]
        c, t = fit(model, sub, kparam, n_starts=24, seed=22 + i)
        if t is None:
            continue
        norms.append(np.linalg.norm(t - base_theta) / max(np.linalg.norm(base_theta), 1e-9))
    if not norms:
        return float("nan")
    return float(np.max(norms))


# ----------------------------------------------------------------------
# 4. Mock injection (LCDM null = monotonic with small slope)
# ----------------------------------------------------------------------
def mock_injection_fdr(data, n_mocks=200, seed=42):
    """LCDM null: σ₀(env) = a + b·ρ (monotonic). 3-regime 가 잘못 채택되는 비율."""
    rng = np.random.default_rng(seed)
    rho = np.array([d[1] for d in data])
    e = np.array([d[3] for d in data])
    a_null, b_null = 0.10, 0.22  # plausible LCDM-like
    fp = 0
    for k in range(n_mocks):
        y_mock = a_null + b_null * rho + rng.standard_normal(len(rho)) * e
        mock_data = [(POOL_NAMES_BY_SUBSET[k % 1] if False else d[0], d[1], float(y_mock[i]), d[3], d[4])
                     for i, d in enumerate(data)]
        # fit both
        c_m, _ = fit(model_monotonic, mock_data, 2, n_starts=12, seed=100 + k)
        c_3, _ = fit(model_three_regime, mock_data, 6, n_starts=12, seed=200 + k)
        n = len(mock_data)
        a1 = aicc(c_m, 2, n)
        a3 = aicc(c_3, 6, n)
        if a3 < a1 - 2:
            fp += 1
    return fp / n_mocks


POOL_NAMES_BY_SUBSET = {1: 1}  # placeholder unused


# ----------------------------------------------------------------------
# 5. Worker per subset
# ----------------------------------------------------------------------
@dataclass
class SubsetResult:
    N: int
    chi2_mono: float
    chi2_3reg: float
    aicc_mono: float
    aicc_3reg: float
    delta_aicc: float
    dom_var: float
    dom_chi2: float
    dom_loo: float
    fdr_3reg: float


def run_subset(N):
    names = SUBSETS[N]
    data = select(names)
    c_m, t_m = fit(model_monotonic, data, 2, n_starts=64, seed=N * 10 + 1)
    c_3, t_3 = fit(model_three_regime, data, 6, n_starts=128, seed=N * 10 + 2)
    a_m = aicc(c_m, 2, N)
    a_3 = aicc(c_3, 6, N)
    dv = dominance_variance_share(data)
    dc = dominance_chi2_leverage(model_three_regime, t_3, data) if t_3 is not None else float("nan")
    dl = dominance_loo_regression(model_three_regime, data, 6)
    fdr = mock_injection_fdr(data, n_mocks=200, seed=N * 100 + 7)
    return SubsetResult(
        N=N,
        chi2_mono=c_m, chi2_3reg=c_3,
        aicc_mono=a_m, aicc_3reg=a_3,
        delta_aicc=a_3 - a_m,
        dom_var=dv, dom_chi2=dc, dom_loo=dl,
        fdr_3reg=fdr,
    )


# ----------------------------------------------------------------------
# 6. Main (parallel)
# ----------------------------------------------------------------------
def main():
    Ns = [3, 5, 8, 13]
    ctx = mp.get_context("spawn")
    with ctx.Pool(min(len(Ns), 9)) as pool:
        results = pool.map(run_subset, Ns)

    out = {
        "version": "L410-v1",
        "honest_caveat": "published archive crawl deferred; results are mock-based forecasts.",
        "pool_size_total": len(POOL),
        "subsets": {r.N: asdict(r) for r in results},
        "threshold_recovery_closed": 0.30,
    }

    # threshold check
    table = []
    for r in results:
        max_dom = max(r.dom_var, r.dom_chi2, r.dom_loo)
        status = "CLOSED-CANDIDATE" if max_dom < 0.30 else (
            "RECOVERY-PROGRESS" if max_dom < 0.50 else "OPEN")
        table.append((r.N, r.dom_var, r.dom_chi2, r.dom_loo, r.delta_aicc, r.fdr_3reg, status))
    out["status_table"] = table

    (OUT / "joint_fit_results.json").write_text(json.dumps(out, indent=2, default=float))

    # human-readable summary
    lines = ["# L410 simulation summary", "",
             "*mock-based forecast; published archive crawl deferred.*", "",
             "| N | dom_var | dom_chi2 | dom_loo | dAICc(3reg-mono) | FDR(3reg) | status |",
             "|---|---------|----------|---------|------------------|-----------|--------|"]
    for r in results:
        max_dom = max(r.dom_var, r.dom_chi2, r.dom_loo)
        status = "CLOSED-CANDIDATE" if max_dom < 0.30 else (
            "RECOVERY-PROGRESS" if max_dom < 0.50 else "OPEN")
        lines.append(f"| {r.N} | {r.dom_var:.3f} | {r.dom_chi2:.3f} | {r.dom_loo:.3f} | "
                     f"{r.delta_aicc:+.2f} | {r.fdr_3reg:.3f} | {status} |")
    (OUT / "REVIEW.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
