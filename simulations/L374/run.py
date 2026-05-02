"""L374 5-dataset joint MCMC smoke test.

Toy likelihood: 6-D Gaussian-mixture-style chi^2 over 5 mock datasets.
emcee n_walkers=200, n_steps=200. Reports R-hat, autocorr, ESS to report.json.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

# Force single-thread BLAS BEFORE importing numpy (CLAUDE.md 시뮬레이션 원칙).
for _k in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_k] = "1"

import numpy as np
import emcee

NDIM = 6
N_DATASETS = 5
N_WALKERS = 200
N_STEPS = 200
BURN = 50
SEED = 374

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "L374"
OUT.mkdir(parents=True, exist_ok=True)


def build_mock_datasets(seed: int = SEED):
    """Build 5 mock datasets: each is (mu_i, invSigma_i)."""
    rng = np.random.default_rng(seed)
    datasets = []
    for i in range(N_DATASETS):
        mu = rng.normal(0.0, 0.3, size=NDIM)  # small offsets near origin
        A = rng.normal(0.0, 1.0, size=(NDIM, NDIM))
        # invSigma = A^T A + small ridge => positive definite
        inv_sigma = A.T @ A + 0.5 * np.eye(NDIM)
        datasets.append((mu, inv_sigma))
    return datasets


def log_prior(theta: np.ndarray) -> float:
    if np.any(np.abs(theta) > 5.0):
        return -np.inf
    # weak Gaussian prior N(0,1) on top of the uniform box.
    return -0.5 * float(np.dot(theta, theta))


def make_log_prob(datasets):
    def log_prob(theta: np.ndarray) -> float:
        lp = log_prior(theta)
        if not np.isfinite(lp):
            return -np.inf
        chi2_total = 0.0
        for mu, inv_sigma in datasets:
            d = theta - mu
            chi2_total += float(d @ inv_sigma @ d)
        return lp + (-0.5 * chi2_total)
    return log_prob


def gelman_rubin(chain: np.ndarray) -> np.ndarray:
    """chain shape (n_walkers, n_steps, ndim). Split walkers in half -> 2 sub-chains."""
    nw, ns, nd = chain.shape
    half = nw // 2
    a = chain[:half].reshape(-1, nd)  # pooled across walkers a
    b = chain[half:half * 2].reshape(-1, nd)
    # split-R-hat per-parameter using simple between/within variance on walker means
    rhats = np.zeros(nd)
    for j in range(nd):
        means = np.array([chain[:half, :, j].mean(), chain[half:half*2, :, j].mean()])
        vars_ = np.array([chain[:half, :, j].var(ddof=1), chain[half:half*2, :, j].var(ddof=1)])
        n = half * ns  # samples per chain
        W = vars_.mean()
        B = n * means.var(ddof=1)
        if W <= 0:
            rhats[j] = np.nan
            continue
        var_hat = (1.0 - 1.0 / n) * W + B / n
        rhats[j] = float(np.sqrt(var_hat / W))
    return rhats


def jsonify(obj):
    if isinstance(obj, dict):
        return {k: jsonify(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [jsonify(v) for v in obj]
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        v = float(obj)
        return v if np.isfinite(v) else None
    if isinstance(obj, np.ndarray):
        return jsonify(obj.tolist())
    return obj


def main():
    np.random.seed(SEED)
    np.seterr(all="ignore")

    datasets = build_mock_datasets(SEED)
    log_prob = make_log_prob(datasets)

    rng = np.random.default_rng(SEED)
    p0 = rng.uniform(-1.0, 1.0, size=(N_WALKERS, NDIM))

    sampler = emcee.EnsembleSampler(N_WALKERS, NDIM, log_prob)
    t0 = time.time()
    sampler.run_mcmc(p0, N_STEPS, progress=False)
    elapsed = time.time() - t0

    chain = sampler.get_chain()  # shape (n_steps, n_walkers, ndim)
    chain = np.swapaxes(chain, 0, 1)  # -> (n_walkers, n_steps, ndim)
    chain_post = chain[:, BURN:, :]

    # Autocorr
    try:
        tau = sampler.get_autocorr_time(tol=0)
    except Exception as exc:  # pragma: no cover
        tau = np.full(NDIM, np.nan)
        tau_err = str(exc)
    else:
        tau_err = None
    tau = np.asarray(tau, dtype=float)

    # ESS = n_walkers * (n_steps - burn) / tau
    n_eff_steps = N_STEPS - BURN
    with np.errstate(divide="ignore", invalid="ignore"):
        ess = N_WALKERS * n_eff_steps / tau
        ess = np.where(np.isfinite(ess), ess, np.nan)

    rhat = gelman_rubin(chain_post)

    accept = float(np.mean(sampler.acceptance_fraction))
    means = chain_post.reshape(-1, NDIM).mean(axis=0)
    stds = chain_post.reshape(-1, NDIM).std(axis=0, ddof=1)

    pass_rhat = bool(np.all(np.isfinite(rhat)) and np.all(rhat < 1.2))
    pass_tau = bool(np.all(np.isfinite(tau)) and np.all(tau < N_STEPS / 2))
    pass_ess = bool(np.all(np.isfinite(ess)) and np.all(ess > 50.0))
    convergence_pass = pass_rhat and pass_tau and pass_ess

    report = {
        "label": "L374_smoke_test",
        "seed": SEED,
        "ndim": NDIM,
        "n_datasets": N_DATASETS,
        "n_walkers": N_WALKERS,
        "n_steps": N_STEPS,
        "burn": BURN,
        "elapsed_sec": elapsed,
        "acceptance_fraction": accept,
        "posterior_mean": means,
        "posterior_std": stds,
        "rhat": rhat,
        "autocorr_tau": tau,
        "autocorr_warning": tau_err,
        "ess": ess,
        "criteria": {
            "rhat_lt_1p2": pass_rhat,
            "tau_lt_nsteps_half": pass_tau,
            "ess_gt_50": pass_ess,
        },
        "convergence_pass": convergence_pass,
        "honest_one_liner": (
            "smoke test only — emcee pipeline runs and reports R-hat/ESS; "
            "no physics conclusions about SQMH from this run"
        ),
        "emcee_version": emcee.__version__,
    }

    out_path = OUT / "report.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(jsonify(report), f, indent=2)

    print(f"[L374] elapsed={elapsed:.2f}s accept={accept:.3f} "
          f"rhat_max={np.nanmax(rhat):.4f} tau_max={np.nanmax(tau):.2f} "
          f"ess_min={np.nanmin(ess):.1f} pass={convergence_pass}")
    print(f"[L374] report -> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
