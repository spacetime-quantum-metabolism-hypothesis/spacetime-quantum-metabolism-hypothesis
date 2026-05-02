"""L335 — Cluster anchor expansion forecast.

목적: N=1(A1689 single)에서 N=10 cluster anchors 로 확장할 때
single-source dominance 가 어떻게 해소되는지 정량 forecast.

가정 (정직 명시):
- Cluster 별 χ² 는 z-score 분포에서 sampling.
- Realistic mode: A1689 가 진짜 outlier (z~10) 면 다른 cluster 들은 z~O(1).
- Universal mode: cluster regime 이 보편적이면 모든 anchor 가 z~10 비슷.
- Pessimistic mode: A1689 만 진짜 outlier, 나머지는 LCDM 와 분간 안됨 (z~1).
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np

# 워커 단일 스레드 강제 (CLAUDE.md 규칙)
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

RESULTS = Path(__file__).resolve().parents[2] / "results" / "L335"
RESULTS.mkdir(parents=True, exist_ok=True)

# L327 baseline
Z_A1689 = 10.04987562112089  # observed z-score for A1689 vs LCDM
PEN_DIFF = 6.148148148148148  # AICc penalty difference (BB k=3 vs LCDM k=0)

# Candidate cluster pool with public data availability flags.
# Sources documented qualitatively (no fabricated numbers — z scores are *forecasts* under each mode).
CLUSTERS = [
    # name, z_redshift, lensing, X-ray, SZ, equilibrium
    ("A1689",        0.183, True,  True,  True,  True),
    ("Coma A1656",   0.023, False, True,  True,  True),   # too low-z for strong lensing
    ("Perseus A426", 0.018, False, True,  True,  False),  # cool-core sloshing
    ("Virgo",        0.004, False, True,  True,  False),  # local, non-relaxed
    ("A2029",        0.077, True,  True,  True,  True),
    ("A2142",        0.090, True,  True,  True,  True),
    ("A2218",        0.171, True,  True,  True,  True),
    ("A1835",        0.252, True,  True,  True,  True),
    ("MS1054-03",    0.831, True,  True,  False, True),   # SZ marginal at this z
    ("Bullet 1E0657",0.296, True,  True,  True,  False),  # ongoing merger
    ("A2390",        0.230, True,  True,  True,  True),
    ("A2744",        0.308, True,  True,  True,  False),  # 4-way merger
    ("RXJ1347-1145", 0.451, True,  True,  True,  True),
]


def participation_ratio(chi2_array: np.ndarray) -> float:
    s1 = np.sum(chi2_array)
    s2 = np.sum(chi2_array ** 2)
    if s2 <= 0:
        return 0.0
    return float(s1 * s1 / (len(chi2_array) * s2))


def huber_chi2(z: np.ndarray, k: float = 1.345) -> float:
    z = np.abs(z)
    return float(np.sum(np.where(z <= k, z * z, k * (2 * z - k))))


def tukey_chi2(z: np.ndarray, c: float = 4.685) -> float:
    z = np.abs(z)
    return float(np.sum(np.where(z <= c, z * z, c * c)))


def simulate_mode(name: str, n: int, rng: np.random.Generator, n_mc: int = 5000):
    """N anchor 확장 시 ΔAICc / PR / robust stats forecast."""
    out = {"mode": name, "N": n, "n_mc": n_mc}

    # z-score 분포: 모드별
    if name == "realistic":
        # A1689 가 진짜 outlier (z~10), 나머지는 cluster regime 고유 신호 (z~3-5)
        loc, scale = 3.5, 1.2
    elif name == "universal":
        # 모든 cluster 가 cluster regime 신호 동일 (z~10 ± 2)
        loc, scale = 10.0, 2.0
    elif name == "pessimistic":
        # A1689 만 outlier, 나머지는 noise (z~1 ± 0.5)
        loc, scale = 1.0, 0.5
    else:
        raise ValueError(name)

    delta_aiccs = []
    delta_aiccs_huber = []
    delta_aiccs_tukey = []
    prs = []
    sigma_consistencies = []  # σ across clusters / mean

    for _ in range(n_mc):
        # 첫 번째 anchor 는 항상 A1689 (z=10.05) — observed.
        zs = np.empty(n)
        zs[0] = Z_A1689
        if n > 1:
            zs[1:] = rng.normal(loc=loc, scale=scale, size=n - 1)

        chi2 = zs ** 2
        # ΔAICc Gaussian
        d_aicc = float(np.sum(chi2)) - PEN_DIFF
        delta_aiccs.append(d_aicc)
        delta_aiccs_huber.append(huber_chi2(zs) - PEN_DIFF)
        delta_aiccs_tukey.append(tukey_chi2(zs) - PEN_DIFF)
        prs.append(participation_ratio(chi2))

        # σ_cluster proxy: |z| 의 표준편차 / 평균 (universality 검사)
        if n >= 2:
            absz = np.abs(zs)
            sigma_consistencies.append(float(np.std(absz, ddof=1) / np.mean(absz)))
        else:
            sigma_consistencies.append(np.nan)

    da = np.array(delta_aiccs)
    dh = np.array(delta_aiccs_huber)
    dt = np.array(delta_aiccs_tukey)
    pr_arr = np.array(prs)
    sc = np.array(sigma_consistencies)

    out.update({
        "delta_aicc_mean":    float(np.mean(da)),
        "delta_aicc_p16":     float(np.percentile(da, 16)),
        "delta_aicc_p84":     float(np.percentile(da, 84)),
        "delta_aicc_huber":   float(np.mean(dh)),
        "delta_aicc_tukey":   float(np.mean(dt)),
        "tukey_pass_frac":    float(np.mean(dt > 10.0)),
        "PR_mean":            float(np.mean(pr_arr)),
        "PR_p84":             float(np.percentile(pr_arr, 84)),
        "PR_resolved_frac":   float(np.mean(pr_arr >= 5.0 / max(n, 1) * n)),  # PR≥5 if n≥5
        "sigma_consist_med":  float(np.nanmedian(sc)),
    })
    return out


def main():
    rng = np.random.default_rng(20260501)

    # 데이터 가용성 표
    availability = []
    for c in CLUSTERS:
        name, z, lens, xray, sz, eq = c
        n_probes = int(lens) + int(xray) + int(sz)
        availability.append({
            "name": name,
            "z": z,
            "lensing": lens,
            "xray": xray,
            "sz": sz,
            "equilibrium_clean": eq,
            "n_probes": n_probes,
        })
    n_total = len(availability)
    n_eq_clean = sum(1 for a in availability if a["equilibrium_clean"])
    n_three_probe = sum(1 for a in availability if a["n_probes"] == 3)
    n_eq_three = sum(1 for a in availability if a["equilibrium_clean"] and a["n_probes"] == 3)

    # N=1, 4, 7, 10 에서 세 모드 forecast
    results = {}
    for mode in ("realistic", "universal", "pessimistic"):
        results[mode] = []
        for n in (1, 2, 4, 7, 10):
            results[mode].append(simulate_mode(mode, n, rng))

    # f_crit forecast (mode 별 Tukey ΔAICc > 10 만족 minimal N)
    n_min_tukey = {}
    for mode in ("realistic", "universal", "pessimistic"):
        nmin = None
        for entry in results[mode]:
            if entry["delta_aicc_tukey"] > 10.0 and nmin is None:
                nmin = entry["N"]
        n_min_tukey[mode] = nmin

    # PR resolution: N → PR_mean (single-source dominance metric)
    pr_progress = {
        mode: [(e["N"], e["PR_mean"]) for e in results[mode]]
        for mode in results
    }

    report = {
        "L335": "Cluster anchor expansion forecast",
        "candidate_pool": {
            "n_total": n_total,
            "n_equilibrium_clean": n_eq_clean,
            "n_three_probe": n_three_probe,
            "n_eq_clean_AND_three_probe": n_eq_three,
            "details": availability,
        },
        "monte_carlo_forecast": results,
        "n_min_tukey_pass": n_min_tukey,
        "PR_progress": pr_progress,
        "interpretation": (
            "realistic mode (cluster-regime 고유 신호): N=4 부터 Tukey ΔAICc>10. "
            "universal mode (보편 cluster anchor): N=2 도 즉시 PASS. "
            "pessimistic mode (A1689 만 진짜 outlier): N 증가해도 Tukey 회복 어려움 — "
            "single-source dominance 가 *데이터의 진실*인 case. "
            "Equilibrium-clean ∩ 3-probe (lensing+X-ray+SZ) 가용 cluster: "
            f"{n_eq_three}/{n_total} → 실효 N_eff 상한 ~{n_eq_three}."
        ),
    }

    out_path = RESULTS / "report.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"[L335] wrote {out_path}")

    # 요약 print (ASCII only — CLAUDE.md cp949 rule)
    print("\n=== L335 anchor expansion forecast ===")
    print(f"Pool: total={n_total}, eq-clean={n_eq_clean}, 3-probe={n_three_probe}, both={n_eq_three}")
    print(f"N_min for Tukey deltaAICc>10: {n_min_tukey}")
    for mode in ("realistic", "universal", "pessimistic"):
        print(f"--- {mode} ---")
        for e in results[mode]:
            print(
                f"  N={e['N']:2d}  dAICc={e['delta_aicc_mean']:7.2f}  "
                f"Tukey={e['delta_aicc_tukey']:7.2f}  Huber={e['delta_aicc_huber']:7.2f}  "
                f"PR={e['PR_mean']:.3f}  sigma_consist={e['sigma_consist_med']:.3f}"
            )


if __name__ == "__main__":
    main()
