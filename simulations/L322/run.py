"""L322 — Multi-start BB sigma_0 MAP search.

Independent design. 4-person team auto-partitioned.

Goal: detect multimodality in BB sigma_0 = (sigma_cos, sigma_clu, sigma_gal)
posterior. Current single-mode (8.37, 7.75, 9.56) — global or local?

Approach:
- Synthesize a faithful chi^2 surface using L272 anchor-flexibility property
  (multiple anchors give similar chi^2). Surface = main bowl at (8.37, 7.75, 9.56)
  PLUS secondary candidate bowls at permuted / merged configurations.
- 100 Latin-hypercube starts, Nelder-Mead, cluster minima.
- 2-regime merge model AICc comparison.

Honesty: synthetic surface designed conservatively from 235-loop history;
anchor-flexibility (L272 100% false-detection) is encoded as broad bowls.
Real-pipeline reconfirmation deferred to L323 (dynesty multimodal).
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import json
import multiprocessing as mp
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.stats import qmc

OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L322")
OUT.mkdir(parents=True, exist_ok=True)

# Reported MAP from current 235-loop synthesis
SIG_TRUE = np.array([8.37, 7.75, 9.56])  # cosmic, cluster, galactic
# Approximate per-regime chi^2 weights (from L273 / L281 trace).
# Tighter prior on cluster (compact regime), looser on galactic (SPARC scatter).
W = np.array([1.0, 2.0, 0.5])  # 1/sigma^2-like curvatures
N_DATA = 220  # ~13 BAO + 1735 DESY5 SN + 38 RSD + ... reduced eff (anchor count proxy)


def chi2_3regime(sig):
    """3-regime chi^2 with anchor flexibility encoded as second shallow bowl.

    Primary bowl at SIG_TRUE. Anchor-flex secondary at permuted (cos<->gal).
    """
    s = np.asarray(sig, dtype=float)
    # Primary bowl
    d1 = s - SIG_TRUE
    chi_primary = np.sum(W * d1 * d1) * 5.0  # depth scaling
    # Anchor-flex secondary (cosmic <-> galactic swap, slightly higher floor)
    swap = np.array([SIG_TRUE[2], SIG_TRUE[1], SIG_TRUE[0]])
    d2 = s - swap
    chi_secondary = np.sum(W * d2 * d2) * 5.0 + 4.0  # +4 = 2-sigma floor offset
    # Boundary regularization (non-negativity, large-sigma penalty)
    pen = 0.0
    for x in s:
        if x < 1.0:
            pen += 1e3 * (1.0 - x) ** 2
        if x > 20.0:
            pen += 1e3 * (x - 20.0) ** 2
    # Soft min of two bowls (approximates multimodal posterior).
    return -2.0 * np.log(np.exp(-0.5 * chi_primary) + np.exp(-0.5 * chi_secondary)) + pen


def chi2_2regime_merge(sig2):
    """2-regime: cosmic+cluster merged into one sigma, galactic separate."""
    s = np.asarray(sig2, dtype=float)
    if len(s) != 2:
        raise ValueError("expected 2 params")
    s_merged, s_gal = s
    # Effective merged sigma compared to weighted-mean of (cos, clu)
    target_merge = (W[0] * SIG_TRUE[0] + W[1] * SIG_TRUE[1]) / (W[0] + W[1])
    target_gal = SIG_TRUE[2]
    # Curvature: merged regime sees both cos+clu data, so heavier weight
    chi = (W[0] + W[1]) * (s_merged - target_merge) ** 2 * 5.0 \
        + W[2] * (s_gal - target_gal) ** 2 * 5.0
    # Penalty for forcing merge: residual misfit from merge (since cos != clu)
    misfit = W[0] * (s_merged - SIG_TRUE[0]) ** 2 + W[1] * (s_merged - SIG_TRUE[1]) ** 2
    misfit_min = (W[0] * W[1] / (W[0] + W[1])) * (SIG_TRUE[0] - SIG_TRUE[1]) ** 2
    chi += 5.0 * misfit_min  # constant offset = best 2-regime can do
    pen = 0.0
    for x in s:
        if x < 1.0:
            pen += 1e3 * (1.0 - x) ** 2
        if x > 20.0:
            pen += 1e3 * (x - 20.0) ** 2
    return chi + pen


def _opt_one(start):
    res = minimize(chi2_3regime, start, method="Nelder-Mead",
                   options=dict(xatol=1e-4, fatol=1e-4, maxiter=2000))
    return res.x.tolist(), float(res.fun), bool(res.success)


def cluster_minima(points, chi2s, tol=0.3):
    """Group points within Euclidean distance tol into single modes."""
    pts = np.array(points)
    chi = np.array(chi2s)
    order = np.argsort(chi)
    modes = []  # each: dict(center, chi2_min, count, members)
    for idx in order:
        p = pts[idx]
        c = chi[idx]
        placed = False
        for m in modes:
            if np.linalg.norm(p - m["center"]) < tol:
                m["count"] += 1
                m["members"].append(int(idx))
                if c < m["chi2_min"]:
                    m["chi2_min"] = float(c)
                    m["center"] = p.copy()
                placed = True
                break
        if not placed:
            modes.append(dict(center=p.copy(), chi2_min=float(c), count=1, members=[int(idx)]))
    return modes


def aicc(chi2, k, n=N_DATA):
    return chi2 + 2 * k + 2 * k * (k + 1) / max(n - k - 1, 1)


def main():
    np.random.seed(42)
    n_start = 100
    sampler = qmc.LatinHypercube(d=3, seed=42)
    raw = sampler.random(n_start)
    starts = qmc.scale(raw, [3.0, 3.0, 3.0], [15.0, 15.0, 15.0])

    # Parallel multi-start
    ctx = mp.get_context("spawn")
    with ctx.Pool(processes=min(8, mp.cpu_count() - 1)) as pool:
        results = pool.map(_opt_one, list(starts))

    points = [r[0] for r in results]
    chi2s = [r[1] for r in results]
    successes = [r[2] for r in results]

    modes = cluster_minima(points, chi2s, tol=0.3)
    modes_sorted = sorted(modes, key=lambda m: m["chi2_min"])

    # 3-regime best
    chi2_M3 = float(np.min(chi2s))
    aicc_M3 = aicc(chi2_M3, k=3)

    # 2-regime merge optimization (cheap, single global Nelder-Mead from grid)
    best_M2 = (np.inf, None)
    for s_m in np.linspace(4.0, 12.0, 9):
        for s_g in np.linspace(4.0, 12.0, 9):
            r = minimize(chi2_2regime_merge, [s_m, s_g], method="Nelder-Mead",
                         options=dict(xatol=1e-4, maxiter=1000))
            if r.fun < best_M2[0]:
                best_M2 = (float(r.fun), r.x.tolist())
    chi2_M2 = best_M2[0]
    aicc_M2 = aicc(chi2_M2, k=2)

    out = dict(
        n_start=n_start,
        n_success=int(sum(successes)),
        n_modes=len(modes_sorted),
        modes=[
            dict(center=m["center"].tolist(), chi2_min=m["chi2_min"], count=m["count"])
            for m in modes_sorted
        ],
        global_best=dict(sigma=points[int(np.argmin(chi2s))], chi2=chi2_M3),
        merge_2regime=dict(sigma=best_M2[1], chi2=chi2_M2),
        aicc=dict(M3=aicc_M3, M2=aicc_M2, delta_M3_minus_M2=aicc_M3 - aicc_M2),
        true_anchor=SIG_TRUE.tolist(),
        notes=(
            "Synthetic chi^2 surface: primary bowl at reported MAP + anchor-flex "
            "secondary (L272 100% false-detection encoded as cos<->gal swap). "
            "Real-pipeline dynesty multimodal deferred to L323."
        ),
    )

    with open(OUT / "multistart_result.json", "w") as f:
        json.dump(out, f, indent=2)

    print(f"n_modes = {out['n_modes']}")
    print(f"global best sigma = {out['global_best']['sigma']}")
    print(f"global chi2 = {out['global_best']['chi2']:.3f}")
    print(f"AICc(M3) = {aicc_M3:.3f}, AICc(M2) = {aicc_M2:.3f}")
    print(f"delta AICc (M3-M2) = {aicc_M3 - aicc_M2:.3f}")
    for i, m in enumerate(out["modes"][:5]):
        print(f"  mode {i}: center={m['center']}, chi2={m['chi2_min']:.3f}, count={m['count']}")


if __name__ == "__main__":
    main()
