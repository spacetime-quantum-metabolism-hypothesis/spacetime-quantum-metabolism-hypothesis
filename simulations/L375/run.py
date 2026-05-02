"""L375 — SQT mock 100개 injection-recovery (BB σ_0 회수율 toy 검증).

CLAUDE.md 룰 준수:
- numpy 2.x: np.trapezoid 직접 (본 스크립트 미사용).
- 시뮬 결과는 정직 보고. base.md 와 다르면 base.fix.md 에 기록.
- 워커당 OMP/MKL/OPENBLAS_NUM_THREADS=1 (multiprocessing 시).
- print() 비ASCII 유니코드 금지 (cp949 회피).
- 식별자 ASCII 만.

설계는 results/L375/ATTACK_DESIGN.md 참조.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

# 워커 OpenMP 등 단일 스레드 강제 (병렬화 안전)
for _k in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ.setdefault(_k, "1")

import numpy as np
from scipy.optimize import minimize_scalar

# ----- 설정 -----
N_MOCK = 100
Z_GRID = np.array([0.1, 0.3, 0.5, 0.8, 1.2, 1.6, 2.0])
ETA = 0.10  # relative noise
LOG10_SIGMA0_TRUE = 0.0  # truth: sigma_0_true = 1.0
SIGMA0_TRUE = 10.0 ** LOG10_SIGMA0_TRUE

# SQT generative growth template
ALPHA_TRUE, BETA_TRUE = 0.05, 0.01

# BB fit growth template (의도적 미세 mismatch — A1 가드)
ALPHA_FIT, BETA_FIT = 0.07, 0.005

RECOVERY_TOL_DEX = 0.10
PASS_THRESHOLD = 0.68

OUT_REPORT = Path(__file__).resolve().parent.parent.parent / "results" / "L375" / "report.json"


def psi_true(z: np.ndarray) -> np.ndarray:
    return 1.0 + ALPHA_TRUE * z + BETA_TRUE * z * z


def psi_fit(z: np.ndarray) -> np.ndarray:
    return 1.0 + ALPHA_FIT * z + BETA_FIT * z * z


def generate_mock(seed: int) -> tuple[np.ndarray, np.ndarray]:
    """SQT generative: d_i = sigma(z_i) + eps_i, eps ~ N(0, eta * sigma_true(z_i))."""
    rng = np.random.default_rng(seed)
    sigma_true_z = SIGMA0_TRUE * psi_true(Z_GRID)
    noise_sd = ETA * sigma_true_z
    d = sigma_true_z + rng.normal(0.0, noise_sd, size=Z_GRID.shape)
    return d, noise_sd


def chi2_bb(log10_sigma0: float, d: np.ndarray, noise_sd: np.ndarray) -> float:
    """BB MAP objective: chi^2 with fixed psi_fit, free sigma_0."""
    sigma0 = 10.0 ** log10_sigma0
    model = sigma0 * psi_fit(Z_GRID)
    resid = (d - model) / noise_sd
    return float(np.sum(resid * resid))


def fit_one(seed: int) -> dict:
    d, noise_sd = generate_mock(seed)
    res = minimize_scalar(
        chi2_bb,
        args=(d, noise_sd),
        bounds=(-1.0, 1.0),
        method="bounded",
        options={"xatol": 1e-6},
    )
    log10_map = float(res.x)
    chi2_min = float(res.fun)
    err_dex = abs(log10_map - LOG10_SIGMA0_TRUE)
    recovered = bool(err_dex <= RECOVERY_TOL_DEX)
    return {
        "seed": seed,
        "log10_sigma0_map": log10_map,
        "err_dex": err_dex,
        "recovered": recovered,
        "chi2_min": chi2_min,
    }


def main() -> int:
    t0 = time.time()
    results = [fit_one(s) for s in range(N_MOCK)]
    errs = np.array([r["err_dex"] for r in results])
    biases = np.array([r["log10_sigma0_map"] - LOG10_SIGMA0_TRUE for r in results])
    n_recov = int(sum(r["recovered"] for r in results))
    rate = n_recov / N_MOCK
    se = float(np.sqrt(rate * (1 - rate) / N_MOCK))  # binomial SE

    summary = {
        "task": "L375 SQT mock injection-recovery (BB sigma_0 MAP)",
        "n_mock": N_MOCK,
        "z_grid": Z_GRID.tolist(),
        "eta_noise": ETA,
        "log10_sigma0_true": LOG10_SIGMA0_TRUE,
        "alpha_true_beta_true": [ALPHA_TRUE, BETA_TRUE],
        "alpha_fit_beta_fit": [ALPHA_FIT, BETA_FIT],
        "recovery_tol_dex": RECOVERY_TOL_DEX,
        "pass_threshold": PASS_THRESHOLD,
        "n_recovered": n_recov,
        "recovery_rate": rate,
        "recovery_rate_binomial_se": se,
        "bias_dex_mean": float(np.mean(biases)),
        "bias_dex_median": float(np.median(biases)),
        "rmse_dex": float(np.sqrt(np.mean(biases * biases))),
        "err_dex_p50": float(np.percentile(errs, 50)),
        "err_dex_p95": float(np.percentile(errs, 95)),
        "verdict": "PASS" if rate > PASS_THRESHOLD else "FAIL",
        "wall_clock_s": time.time() - t0,
        "per_mock": results,
        "honesty_note": (
            "Toy self-consistency test of BB MAP recovery on SQT-generative mocks. "
            "Not a claim about SQMH performance on real data."
        ),
    }
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_REPORT, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False)

    print(f"L375 done: rate={rate:.3f} ({n_recov}/{N_MOCK}) verdict={summary['verdict']}")
    print(f"bias_mean={summary['bias_dex_mean']:.4f} rmse={summary['rmse_dex']:.4f} dex")
    print(f"report -> {OUT_REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
