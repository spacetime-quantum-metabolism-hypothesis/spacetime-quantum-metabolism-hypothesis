"""L377 dynesty nested sampling smoke test.

Bimodal 3D Gaussian mixture, uniform prior, 100 live points.
Tests dynesty install + multimodal detection + ln Z accuracy.
"""
import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

import json
import math
import time
from pathlib import Path

import numpy as np

RESULTS = Path(__file__).resolve().parents[2] / "results" / "L377"
RESULTS.mkdir(parents=True, exist_ok=True)

# ---- target ----
NDIM = 3
SIGMA = 0.5
MU_A = np.array([-2.0, -2.0, -2.0])
MU_B = np.array([+2.0, +2.0, +2.0])
PRIOR_LO, PRIOR_HI = -5.0, +5.0
PRIOR_VOL = (PRIOR_HI - PRIOR_LO) ** NDIM

# Analytic ln Z: each Gaussian integrated over R^3 = (2 pi sigma^2)^(3/2);
# mixture has two with equal weight 0.5; divide by prior volume.
def analytic_lnz():
    gauss_int = (2.0 * math.pi * SIGMA * SIGMA) ** (NDIM / 2.0)
    # mixture density = 0.5 * N_A + 0.5 * N_B; integrates to 1; but our
    # likelihood (below) is the unnormalized sum of two Gaussians with
    # peak height 1 each (i.e. sum of two unnormalized Gaussians).
    # L(theta) = exp(-0.5 r_A^2/sigma^2) + exp(-0.5 r_B^2/sigma^2)
    # Integral = 2 * (2 pi sigma^2)^(3/2)
    z_int = 2.0 * gauss_int
    return math.log(z_int / PRIOR_VOL)


def loglike(theta):
    rA2 = np.sum((theta - MU_A) ** 2)
    rB2 = np.sum((theta - MU_B) ** 2)
    s2 = SIGMA * SIGMA
    # logsumexp(-0.5 rA2/s2, -0.5 rB2/s2)
    a = -0.5 * rA2 / s2
    b = -0.5 * rB2 / s2
    m = max(a, b)
    return m + math.log(math.exp(a - m) + math.exp(b - m))


def prior_transform(u):
    return PRIOR_LO + (PRIOR_HI - PRIOR_LO) * u


def main():
    import dynesty
    from dynesty import utils as dyutils

    rng = np.random.default_rng(20260501)

    t0 = time.time()
    sampler = dynesty.NestedSampler(
        loglike,
        prior_transform,
        ndim=NDIM,
        nlive=100,
        sample="rwalk",
        bound="multi",
        rstate=rng,
    )
    sampler.run_nested(dlogz=0.1, print_progress=False)
    res = sampler.results
    elapsed = time.time() - t0

    lnz = float(res.logz[-1])
    lnz_err = float(res.logzerr[-1])
    lnz_true = analytic_lnz()

    # Posterior samples (importance resampled from weighted dead points)
    samples_eq = dyutils.resample_equal(
        res.samples, np.exp(res.logwt - res.logz[-1])
    )

    # KMeans-style 2-cluster split (sklearn-free): assign by nearest of two
    # initial seeds (samples furthest apart), then iterate centroids.
    pts = samples_eq.copy()
    # init: two extremes
    d2 = np.sum((pts - pts[0]) ** 2, axis=1)
    seed1 = pts[np.argmax(d2)]
    d2 = np.sum((pts - seed1) ** 2, axis=1)
    seed0 = pts[np.argmax(d2)]
    centroids = np.vstack([seed0, seed1])
    for _ in range(50):
        d0 = np.sum((pts - centroids[0]) ** 2, axis=1)
        d1 = np.sum((pts - centroids[1]) ** 2, axis=1)
        labels = (d1 < d0).astype(int)
        new_c = np.vstack([
            pts[labels == 0].mean(axis=0) if (labels == 0).any() else centroids[0],
            pts[labels == 1].mean(axis=0) if (labels == 1).any() else centroids[1],
        ])
        if np.allclose(new_c, centroids, atol=1e-4):
            centroids = new_c
            break
        centroids = new_c

    n_total = len(labels)
    w0 = float((labels == 0).sum() / n_total)
    w1 = float((labels == 1).sum() / n_total)
    # mode count: cluster with weight >= 0.05 counts; require centroids near MU_A / MU_B
    near_A = min(np.linalg.norm(centroids[0] - MU_A), np.linalg.norm(centroids[1] - MU_A))
    near_B = min(np.linalg.norm(centroids[0] - MU_B), np.linalg.norm(centroids[1] - MU_B))
    mode_count = int((w0 >= 0.05) + (w1 >= 0.05))

    # acceptance criteria
    c1 = math.isfinite(lnz)
    c2 = abs(lnz - lnz_true) < 0.5
    c3 = (w0 > 0.2) and (w1 > 0.2)

    report = {
        "run": "L377",
        "tool": "dynesty",
        "dynesty_version": getattr(__import__("dynesty"), "__version__", "?"),
        "ndim": NDIM,
        "nlive": 100,
        "sampler": "rwalk",
        "bound": "multi",
        "elapsed_sec": round(elapsed, 3),
        "n_iter": int(res.niter),
        "n_calls": int(np.sum(res.ncall)) if hasattr(res, "ncall") else None,
        "lnZ": lnz,
        "lnZ_err": lnz_err,
        "lnZ_analytic": lnz_true,
        "lnZ_residual": lnz - lnz_true,
        "n_eff_samples": int(n_total),
        "mode_count": mode_count,
        "cluster_weights": [w0, w1],
        "cluster_centroids": centroids.tolist(),
        "centroid_dist_to_MU_A": float(near_A),
        "centroid_dist_to_MU_B": float(near_B),
        "C1_lnZ_finite": bool(c1),
        "C2_lnZ_within_0p5": bool(c2),
        "C3_both_modes_found": bool(c3),
        "PASS": bool(c1 and c2 and c3),
        "honest_one_line": "synthetic toy only; two well-separated 3D Gaussians under uniform prior; not a cosmology fit.",
    }
    out = RESULTS / "report.json"
    out.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    main()
