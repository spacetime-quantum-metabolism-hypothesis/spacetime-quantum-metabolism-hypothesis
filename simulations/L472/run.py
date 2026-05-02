"""L472 — Tsallis non-extensive entropy curve fit for the cluster-scale sigma_0 dip.

Free-speculation companion to results/L472/SPECULATION.md.

This script is intentionally minimal: it fits a single phenomenological "dip" profile
to a synthetic sigma_0(R) dataset (real cluster sigma_0 extraction is a separate L473
task), and compares against a flat Boltzmann-Gibbs baseline via AICc.

It is a curve-fit harness, not a physical derivation. No microphysics is imposed.

Run:
    python3 simulations/L472/run.py
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit

# CLAUDE.md: per-worker thread cap, ASCII-only prints
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

RESULTS_DIR = Path(__file__).resolve().parents[2] / "results" / "L472"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
def sigma_BG(R, sigma_inf):
    """Boltzmann-Gibbs baseline: sigma_0 is scale-independent (no dip)."""
    return np.full_like(R, sigma_inf, dtype=float)


def sigma_Tsallis(R, sigma_inf, A, log10_Rdip, w):
    """Phenomenological Tsallis-running ansatz.

    sigma_0(R) = sigma_inf * (1 - A * exp(-((log10(R) - log10_Rdip)/w)**2))

    Parameters
    ----------
    R         : radius array [Mpc]
    sigma_inf : asymptotic (galactic + supercluster) value
    A         : dip depth, A in [0, 1).  A interpreted as a proxy for q_eff - 1.
    log10_Rdip: log10 of the dip centre [Mpc]
    w         : log10-Gaussian width
    """
    x = np.log10(R)
    return sigma_inf * (1.0 - A * np.exp(-((x - log10_Rdip) / w) ** 2))


# ---------------------------------------------------------------------------
# Synthetic data (placeholder until L473 cluster sigma_0 extraction)
# ---------------------------------------------------------------------------
def make_synthetic(seed: int = 472):
    rng = np.random.default_rng(seed)
    R = np.logspace(-2, 1.5, 24)  # 0.01 .. 31.6 Mpc
    truth = dict(sigma_inf=1.0, A=0.15, log10_Rdip=0.0, w=0.45)  # dip at 1 Mpc
    y_true = sigma_Tsallis(R, **truth)
    err = 0.02 * truth["sigma_inf"] * np.ones_like(R)
    y_obs = y_true + rng.normal(0.0, err)
    return R, y_obs, err, truth


# ---------------------------------------------------------------------------
# Fitting
# ---------------------------------------------------------------------------
def chi2(y_obs, y_mod, err):
    return float(np.sum(((y_obs - y_mod) / err) ** 2))


def aicc(chi2_val, k, n):
    aic = chi2_val + 2.0 * k
    if n - k - 1 <= 0:
        return aic
    return aic + 2.0 * k * (k + 1.0) / (n - k - 1.0)


def fit_BG(R, y, err):
    popt, pcov = curve_fit(sigma_BG, R, y, sigma=err, absolute_sigma=True, p0=[np.mean(y)])
    y_mod = sigma_BG(R, *popt)
    c2 = chi2(y, y_mod, err)
    return popt, np.sqrt(np.diag(pcov)), c2


def fit_Tsallis(R, y, err):
    p0 = [np.max(y), 0.1, 0.0, 0.5]
    bounds = ([0.5, 0.0, -1.0, 0.05], [2.0, 0.99, 1.5, 2.0])
    popt, pcov = curve_fit(
        sigma_Tsallis, R, y, sigma=err, absolute_sigma=True, p0=p0, bounds=bounds, maxfev=20000
    )
    y_mod = sigma_Tsallis(R, *popt)
    c2 = chi2(y, y_mod, err)
    return popt, np.sqrt(np.diag(pcov)), c2


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    R, y, err, truth = make_synthetic()
    n = len(R)

    bg_p, bg_e, bg_c2 = fit_BG(R, y, err)
    ts_p, ts_e, ts_c2 = fit_Tsallis(R, y, err)

    bg_aicc = aicc(bg_c2, k=1, n=n)
    ts_aicc = aicc(ts_c2, k=4, n=n)
    delta_aicc = bg_aicc - ts_aicc  # positive => Tsallis preferred

    sigma_inf, A, log10_Rdip, w = ts_p
    q_eff_minus_1 = A  # proxy: dip depth ~ non-extensivity amplitude

    out = dict(
        n_data=n,
        truth=truth,
        BG=dict(sigma_inf=float(bg_p[0]), sigma_inf_err=float(bg_e[0]), chi2=bg_c2, k=1, AICc=bg_aicc),
        Tsallis=dict(
            sigma_inf=float(sigma_inf),
            A=float(A),
            log10_Rdip=float(log10_Rdip),
            R_dip_Mpc=float(10.0 ** log10_Rdip),
            w=float(w),
            errs=[float(e) for e in ts_e],
            chi2=ts_c2,
            k=4,
            AICc=ts_aicc,
            q_eff_minus_1_proxy=float(q_eff_minus_1),
        ),
        delta_AICc_BG_minus_Tsallis=delta_aicc,
        verdict=(
            "Tsallis preferred (dip detected)"
            if delta_aicc > 0
            else "BG preferred (no dip evidence)"
        ),
        notes=[
            "Synthetic data only. Real cluster sigma_0 extraction = L473 task.",
            "A is a proxy for q_eff - 1, not a derivation.",
            "No physical mapping q(R) imposed; team derives in L473+.",
        ],
    )

    out_path = RESULTS_DIR / "fit_results.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print("L472 Tsallis curve fit -- summary")
    print("  n_data           =", n)
    print("  BG       chi2 =", f"{bg_c2:.3f}", " AICc =", f"{bg_aicc:.3f}")
    print("  Tsallis  chi2 =", f"{ts_c2:.3f}", " AICc =", f"{ts_aicc:.3f}")
    print("  Delta AICc (BG - Tsallis) =", f"{delta_aicc:.3f}")
    print("  Best dip: R_dip =", f"{10.0**log10_Rdip:.3f} Mpc",
          " A =", f"{A:.3f}", " w =", f"{w:.3f}")
    print("  Verdict:", out["verdict"])
    print("  Wrote:", out_path)


if __name__ == "__main__":
    main()
