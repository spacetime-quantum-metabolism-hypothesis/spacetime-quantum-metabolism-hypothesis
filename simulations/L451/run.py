"""
L451 — Bayes factor anti-cherry-pick mock injection-recovery.

목적: L424 의 ΔlnZ ±34 변동이 *cherry-pick 자유도* 인지 *구조적 신호* 인지
분리. N=200 mock injection 으로 ΔlnZ(three_regime − lcdm) 분포를 측정,
baseline 8-pool vs 13-pool (+5 dSph) 의 *분포 차이* 로 판정.

CLAUDE.md 준수:
- 8인팀 ATTACK + 4인팀 NEXT_STEP 의 *실행* 단계만 — 새 이론 도출 없음.
- multiprocessing.spawn Pool(8), OMP/MKL/OPENBLAS=1 강제.
- mock 단위 work 분할.
- Laplace 실패 = NaN, 성공률 별도 보고.

산출:
  results/L451/report.json
  results/L451/run_log.txt (caller redirect)

사전등록 판정 기준 (B7):
  (a) ΔΔlnZ 분포 평균 < 0  →  model penalty 작동 신호.
  (b) ΔΔlnZ 분포 std < 5    →  cherry-pick 폭 ±34 보다 좁음.
  (c) mapping 두 종 분포 차이 < 1σ_pooled  →  매핑 자유도 흡수.
"""
from __future__ import annotations

import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import json
import math
import multiprocessing as mp
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

RNG_SEED = 4242
N_MOCK = 200
N_WORKERS = 8
R_PRIMARY = 5.0
R_SWEEP = [2.0, 5.0, 10.0]

# ---------------------------------------------------------------------------
# Anchor pools (L424 와 동일 toy)
# ---------------------------------------------------------------------------
BASE_ANCHORS = np.array([
    (+4.5, 1.00, 0.05),
    (+3.7, 0.96, 0.05),
    (+2.8, 0.40, 0.06),
    (+2.0, 0.35, 0.06),
    (+0.5, 0.42, 0.08),
    (-1.0, 0.95, 0.10),
    (-2.0, 1.10, 0.07),
    (-2.5, 1.15, 0.07),
])

DSPH = {
    "Draco":      (9.1,  221.0,  82.0, 2.2),
    "UrsaMinor":  (9.5,  181.0,  78.0, 1.8),
    "Sculptor":   (9.2,  283.0,  86.0, 3.4),
    "Sextans":    (7.9,  695.0,  89.0, 4.1),
    "Carina":     (6.6,  250.0, 106.0, 0.8),
}

def dsph_anchor(name, mode):
    s_los, r_half_pc, D_LG, M_dyn = DSPH[name]
    s_ref = 10.0
    sig0 = 0.95 * (s_los / s_ref)
    sig_err = 0.10 * sig0
    if mode == "local_group":
        log_rho = -0.5 - 0.01 * (D_LG - 80.0)
    elif mode == "galactic_internal":
        Msun_kg = 1.989e30
        pc_m = 3.086e16
        V = (4.0 / 3.0) * math.pi * (r_half_pc * pc_m) ** 3
        M = M_dyn * 1e7 * Msun_kg
        rho = M / V
        rho_crit = 9.47e-27
        log_rho = math.log10(rho / rho_crit)
    else:
        raise ValueError(mode)
    return (log_rho, sig0, sig_err)

def dsph_pool(mode):
    return np.array([dsph_anchor(n, mode) for n in DSPH])

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
def m_three(theta, x):
    s_h, s_m, s_l, t1, t2 = theta
    if t1 <= t2:
        return None
    return np.where(x > t1, s_h, np.where(x > t2, s_m, s_l))

def m_lcdm(theta, x):
    (s0,) = theta
    return np.full_like(x, s0)

MODELS = {
    "three_regime": dict(fn=m_three, k=5,
                         mu=np.array([1.0, 0.4, 1.1, 3.0, 0.5]),
                         sc=np.array([0.3, 0.3, 0.3, 1.5, 1.5])),
    "lcdm":         dict(fn=m_lcdm,  k=1,
                         mu=np.array([0.8]),
                         sc=np.array([0.3])),
}

# ---------------------------------------------------------------------------
# Likelihood / prior / Laplace lnZ
# ---------------------------------------------------------------------------
def loglike(model, theta, anchors):
    fn = MODELS[model]["fn"]
    pred = fn(theta, anchors[:, 0])
    if pred is None:
        return -np.inf
    chi2 = np.sum(((anchors[:, 1] - pred) / anchors[:, 2]) ** 2)
    return -0.5 * chi2

def logprior(model, theta, R):
    mu = MODELS[model]["mu"]
    s = MODELS[model]["sc"] * R
    if len(theta) != len(mu):
        return -np.inf
    diff = (np.asarray(theta) - mu) / s
    return -0.5 * np.sum(diff ** 2) - np.sum(np.log(s * math.sqrt(2 * math.pi)))

def laplace_lnZ(anchors, model, R, restarts=6, rng=None):
    rng = rng or np.random.default_rng(0)
    mu = MODELS[model]["mu"]
    s = MODELS[model]["sc"] * R
    k = len(mu)

    def neg_logp(theta):
        lp = logprior(model, theta, R)
        ll = loglike(model, theta, anchors)
        if not np.isfinite(lp + ll):
            return 1e8
        return -(lp + ll)

    best = (np.inf, None)
    for _ in range(restarts):
        x0 = mu + 0.3 * s * rng.standard_normal(k)
        try:
            res = minimize(neg_logp, x0, method="Nelder-Mead",
                           options=dict(xatol=1e-5, fatol=1e-5,
                                        maxiter=4000, disp=False))
            if res.fun < best[0]:
                best = (res.fun, res.x)
        except Exception:
            continue
    if best[1] is None:
        return None
    theta_map = best[1]
    logp_map = -best[0]

    eps = 1e-3 * np.maximum(np.abs(theta_map), 1.0)
    H = np.zeros((k, k))
    for i in range(k):
        for j in range(k):
            if i == j:
                ei = np.zeros(k); ei[i] = eps[i]
                fpp = neg_logp(theta_map + ei)
                fmm = neg_logp(theta_map - ei)
                f0 = -logp_map
                H[i, i] = (fpp - 2 * f0 + fmm) / (eps[i] ** 2)
            else:
                ei = np.zeros(k); ei[i] = eps[i]
                ej = np.zeros(k); ej[j] = eps[j]
                fpp = neg_logp(theta_map + ei + ej)
                fpm = neg_logp(theta_map + ei - ej)
                fmp = neg_logp(theta_map - ei + ej)
                fmm = neg_logp(theta_map - ei - ej)
                H[i, j] = (fpp - fpm - fmp + fmm) / (4 * eps[i] * eps[j])
    H = 0.5 * (H + H.T)
    sign, logdet = np.linalg.slogdet(H)
    if sign <= 0 or not np.isfinite(logdet):
        H_reg = H + 1e-3 * np.eye(k)
        sign, logdet = np.linalg.slogdet(H_reg)
        if sign <= 0:
            return None
    return logp_map + 0.5 * k * math.log(2 * math.pi) - 0.5 * logdet

# ---------------------------------------------------------------------------
# SQT pre-fit truth (T1b)
# ---------------------------------------------------------------------------
def sqt_prefit_theta():
    """Fit three_regime to BASE_ANCHORS at R=5 → MAP θ as truth."""
    rng = np.random.default_rng(RNG_SEED)
    mu = MODELS["three_regime"]["mu"]
    s = MODELS["three_regime"]["sc"] * R_PRIMARY

    def neg_logp(theta):
        lp = logprior("three_regime", theta, R_PRIMARY)
        ll = loglike("three_regime", theta, BASE_ANCHORS)
        if not np.isfinite(lp + ll):
            return 1e8
        return -(lp + ll)

    best = (np.inf, None)
    for _ in range(20):
        x0 = mu + 0.3 * s * rng.standard_normal(5)
        res = minimize(neg_logp, x0, method="Nelder-Mead",
                       options=dict(xatol=1e-6, fatol=1e-6, maxiter=6000))
        if res.fun < best[0]:
            best = (res.fun, res.x)
    return best[1]

def truth_predict(truth_kind, theta_sqt, log_rho_arr):
    if truth_kind == "lcdm":
        return np.full_like(log_rho_arr, 0.85)
    elif truth_kind == "sqt":
        return m_three(theta_sqt, log_rho_arr)
    else:
        raise ValueError(truth_kind)

# ---------------------------------------------------------------------------
# Single mock realisation
# ---------------------------------------------------------------------------
def run_one_mock(args):
    """One mock realisation across (truth × mapping × pool) cells.
    Returns dict keyed by 'cell_id' → ΔlnZ (three_regime − lcdm) or NaN.
    """
    mock_idx, theta_sqt = args
    rng = np.random.default_rng(RNG_SEED + 10007 * (mock_idx + 1))
    out = {"mock_idx": int(mock_idx)}

    for truth in ("lcdm", "sqt"):
        for mapping in ("local_group", "galactic_internal"):
            dsph = dsph_pool(mapping)
            for pool_name, pool in (("base8", BASE_ANCHORS),
                                    ("base13", np.vstack([BASE_ANCHORS, dsph]))):
                # Inject noise around truth at each anchor location.
                log_rho = pool[:, 0]
                err = pool[:, 2]
                truth_vals = truth_predict(truth, theta_sqt, log_rho)
                noisy = truth_vals + rng.normal(0.0, err)
                anchors = np.column_stack([log_rho, noisy, err])

                lnZ_3 = laplace_lnZ(anchors, "three_regime", R_PRIMARY,
                                    restarts=4, rng=rng)
                lnZ_L = laplace_lnZ(anchors, "lcdm", R_PRIMARY,
                                    restarts=2, rng=rng)
                if lnZ_3 is None or lnZ_L is None:
                    delta = float("nan")
                else:
                    delta = float(lnZ_3 - lnZ_L)
                key = f"{truth}__{mapping}__{pool_name}"
                out[key] = delta
    return out

# ---------------------------------------------------------------------------
# Reduce: per-cell stats + ΔΔlnZ (treatment 13 − control 8)
# ---------------------------------------------------------------------------
def cell_stats(values):
    arr = np.asarray(values, dtype=float)
    finite = arr[np.isfinite(arr)]
    n_total = arr.size
    n_ok = finite.size
    if n_ok == 0:
        return dict(n_total=n_total, n_ok=0, success_rate=0.0,
                    mean=None, std=None, p05=None, p50=None, p95=None)
    return dict(
        n_total=int(n_total),
        n_ok=int(n_ok),
        success_rate=float(n_ok / n_total),
        mean=float(np.mean(finite)),
        std=float(np.std(finite, ddof=1)) if n_ok > 1 else 0.0,
        p05=float(np.percentile(finite, 5)),
        p50=float(np.percentile(finite, 50)),
        p95=float(np.percentile(finite, 95)),
    )

def assess_anti_cherry_pick(dd_stats):
    """B7 (a)/(b)/(c) PASS/FAIL.

    dd_stats: dict 'truth__mapping' → cell_stats of ΔΔlnZ (13−8).
    """
    flags = {}
    for key, st in dd_stats.items():
        if st["mean"] is None:
            flags[key] = dict(a_neg_mean=None, b_std_lt5=None)
            continue
        flags[key] = dict(
            a_neg_mean=bool(st["mean"] < 0.0),
            b_std_lt5=bool(st["std"] < 5.0),
        )
    # (c) mapping difference within pooled sigma
    mapping_check = {}
    for truth in ("lcdm", "sqt"):
        klg = f"{truth}__local_group"
        kin = f"{truth}__galactic_internal"
        a, b = dd_stats.get(klg), dd_stats.get(kin)
        if not a or not b or a["mean"] is None or b["mean"] is None:
            mapping_check[truth] = None
            continue
        diff = abs(a["mean"] - b["mean"])
        pooled = math.sqrt(0.5 * (a["std"] ** 2 + b["std"] ** 2))
        mapping_check[truth] = dict(
            mean_diff=float(diff),
            pooled_std=float(pooled),
            c_within_1sigma=bool(diff < pooled),
        )
    return flags, mapping_check

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    t0 = time.time()
    print("=" * 80)
    print("L451 — Bayes factor anti-cherry-pick mock injection-recovery")
    print(f"  N_MOCK={N_MOCK}  R_PRIMARY={R_PRIMARY}  workers={N_WORKERS}")
    print("=" * 80)

    theta_sqt = sqt_prefit_theta()
    print(f"\nSQT pre-fit MAP θ (three_regime, R={R_PRIMARY}, base8): "
          f"{np.round(theta_sqt, 3).tolist()}")

    # Probe predictions of the SQT truth at base anchor locations
    pred_base = m_three(theta_sqt, BASE_ANCHORS[:, 0])
    print(f"  truth(SQT) at base log_rho = {np.round(pred_base, 3).tolist()}")

    args = [(i, theta_sqt) for i in range(N_MOCK)]
    print(f"\nLaunching {len(args)} mock tasks across {N_WORKERS} workers...")

    ctx = mp.get_context("spawn")
    with ctx.Pool(N_WORKERS) as pool:
        results = pool.map(run_one_mock, args, chunksize=4)

    print(f"  done in {time.time()-t0:.1f}s")

    # Aggregate per cell
    cells = {}
    for key in results[0].keys():
        if key == "mock_idx":
            continue
        vals = [r[key] for r in results]
        cells[key] = cell_stats(vals)

    # ΔΔlnZ (13 − 8) per (truth, mapping)
    dd_dist = {}
    dd_stats = {}
    for truth in ("lcdm", "sqt"):
        for mapping in ("local_group", "galactic_internal"):
            k8 = f"{truth}__{mapping}__base8"
            k13 = f"{truth}__{mapping}__base13"
            v8 = np.array([r[k8] for r in results])
            v13 = np.array([r[k13] for r in results])
            both_ok = np.isfinite(v8) & np.isfinite(v13)
            dd = v13 - v8
            dd_dist[f"{truth}__{mapping}"] = dd[both_ok].tolist()
            dd_stats[f"{truth}__{mapping}"] = cell_stats(dd[both_ok])

    flags, mapping_check = assess_anti_cherry_pick(dd_stats)

    # ----- Print summary tables -----
    print("\n--- Per-cell ΔlnZ (three_regime − lcdm) statistics ---")
    print(f"  {'cell':<42s}  {'n_ok':>5s}  {'mean':>9s}  {'std':>8s}  "
          f"{'[p05,p50,p95]':>30s}")
    for key, st in cells.items():
        if st["mean"] is None:
            print(f"  {key:<42s}  {st['n_ok']:>5d}  {'nan':>9s}  {'nan':>8s}  ALL_FAIL")
            continue
        print(f"  {key:<42s}  {st['n_ok']:>5d}  {st['mean']:>9.3f}  "
              f"{st['std']:>8.3f}  "
              f"[{st['p05']:+7.2f}, {st['p50']:+7.2f}, {st['p95']:+7.2f}]")

    print("\n--- ΔΔlnZ distribution (13-pool − 8-pool, per truth × mapping) ---")
    print(f"  {'cell':<32s}  {'n_ok':>5s}  {'mean':>9s}  {'std':>8s}  "
          f"{'[p05,p50,p95]':>30s}")
    for key, st in dd_stats.items():
        if st["mean"] is None:
            print(f"  {key:<32s}  {st['n_ok']:>5d}  ALL_FAIL")
            continue
        print(f"  {key:<32s}  {st['n_ok']:>5d}  {st['mean']:>9.3f}  "
              f"{st['std']:>8.3f}  "
              f"[{st['p05']:+7.2f}, {st['p50']:+7.2f}, {st['p95']:+7.2f}]")

    print("\n--- B7 anti-cherry-pick flags ---")
    for key, fl in flags.items():
        print(f"  {key:<32s}  (a) mean<0 = {fl['a_neg_mean']}  "
              f"(b) std<5 = {fl['b_std_lt5']}")
    print("\n--- B7 (c) mapping difference within 1σ_pooled ---")
    for truth, mc in mapping_check.items():
        if mc is None:
            print(f"  {truth:<10s}  no data")
            continue
        print(f"  {truth:<10s}  mean_diff={mc['mean_diff']:.3f}  "
              f"pooled_std={mc['pooled_std']:.3f}  "
              f"(c) within_1σ = {mc['c_within_1sigma']}")

    # ----- Verdict -----
    a_pass = sum(1 for f in flags.values() if f.get("a_neg_mean") is True)
    b_pass = sum(1 for f in flags.values() if f.get("b_std_lt5") is True)
    c_pass = sum(1 for mc in mapping_check.values()
                 if mc and mc.get("c_within_1sigma") is True)
    total_a = sum(1 for f in flags.values() if f.get("a_neg_mean") is not None)
    total_b = sum(1 for f in flags.values() if f.get("b_std_lt5") is not None)
    total_c = sum(1 for mc in mapping_check.values() if mc is not None)

    print("\n--- Verdict tally ---")
    print(f"  (a) mean<0           : {a_pass}/{total_a} cells")
    print(f"  (b) std<5            : {b_pass}/{total_b} cells")
    print(f"  (c) mapping within 1σ: {c_pass}/{total_c} truths")

    any_pass = (a_pass > 0) or (b_pass > 0) or (c_pass > 0)
    if a_pass == total_a and total_a > 0:
        verdict = "PASS-A: 모든 셀에서 ΔΔlnZ 평균 음수 (model penalty 작동)"
    elif b_pass == total_b and total_b > 0:
        verdict = "PASS-B: 모든 셀에서 ΔΔlnZ std < 5 (cherry-pick 폭 미만)"
    elif c_pass == total_c and total_c > 0:
        verdict = "PASS-C: 매핑 자유도가 mock 변동 안에 흡수"
    elif any_pass:
        verdict = "PARTIAL: 일부 셀만 통과 — anti-cherry-pick 부분 작동"
    else:
        verdict = "FAIL: 본 toy 에서 Bayes factor 가 anti-cherry-pick 으로 작동하지 않음"
    print(f"\n  ==> {verdict}")

    # ----- Save -----
    out_dir = Path(__file__).resolve().parent.parent.parent / "results" / "L451"
    out_dir.mkdir(parents=True, exist_ok=True)

    def _jsonify(o):
        if isinstance(o, dict):
            return {k: _jsonify(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [_jsonify(v) for v in o]
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        return o

    payload = dict(
        seed=RNG_SEED,
        n_mock=N_MOCK,
        R_primary=R_PRIMARY,
        sqt_prefit_theta=theta_sqt.tolist(),
        cells=cells,
        dd_stats=dd_stats,
        dd_dist=dd_dist,
        flags=flags,
        mapping_check=mapping_check,
        verdict=verdict,
        elapsed_sec=time.time() - t0,
    )
    with (out_dir / "report.json").open("w") as f:
        json.dump(_jsonify(payload), f, indent=2)
    print(f"\n[saved] {out_dir / 'report.json'}")
    print(f"\n=== END L451 (elapsed {time.time()-t0:.1f}s) ===")


if __name__ == "__main__":
    main()
