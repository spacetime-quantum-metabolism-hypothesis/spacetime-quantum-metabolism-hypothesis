"""
L323 — Information geometry of BB 3-parameter space.

Independent thinking. No imports of L196/L272/L281 internals — we model the
likelihood landscape from publicly stated quantities:

    fixed-theta  ΔlnZ ≈ +13   (L196)
    marginalized ΔlnZ ≈ +0.8  (L281)
    => log volume gap ≈ 12.2  =>  prior_vol / posterior_vol ≈ exp(12.2) ≈ 2e5
    BB params:  σ_cosmic, σ_cluster, σ_galactic  (3 dof)

We construct a toy Gaussian likelihood whose Hessian reproduces the volume
gap, then probe its information geometry. Three Hessian shapes are tried:
  (a) isotropic — sanity check
  (b) anisotropic — one stiff, two soft (the "sloppy" guess)
  (c) ultra-sloppy — log-uniform spectrum (Sethna pattern)

For each: condition number, participation ratio, geodesic distance to LCDM,
Laplace-vs-MC posterior volume, reparameterization invariance check.

Output: report.json + REVIEW data.
"""

import json
import os
import numpy as np
from numpy.linalg import eigvalsh, det, cholesky, inv

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

RNG = np.random.default_rng(20260501)

# ---------------------------------------------------------------
# Public anchors
# ---------------------------------------------------------------
DLNZ_FIXED      = 13.0      # L196
DLNZ_MARGINAL   = 0.8       # L281
LOG_VOL_GAP     = DLNZ_FIXED - DLNZ_MARGINAL   # ≈ 12.2
NDIM            = 3

# Best-fit point (in dex-like log10 σ units) and prior box width.
# Values chosen to reflect the "cosmic / cluster / galactic" hierarchy
# without copying any specific numeric from prior loops.
THETA_STAR = np.array([0.0, 0.0, 0.0])
PRIOR_HALFWIDTH = np.array([2.0, 2.0, 2.0])     # dex (uniform prior)
THETA_LCDM = np.array([-3.0, -3.0, -3.0])       # σ→0 limit (cut-off, log10)


# ---------------------------------------------------------------
# Hessian / Fisher constructions
# ---------------------------------------------------------------
def hessian_isotropic(scale):
    return scale * np.eye(NDIM)


def hessian_anisotropic(stiff, soft1, soft2, rot_seed=1):
    # rotation to mix params (so eigenvectors are not coordinate axes)
    rng = np.random.default_rng(rot_seed)
    A = rng.standard_normal((NDIM, NDIM))
    Q, _ = np.linalg.qr(A)
    D = np.diag([stiff, soft1, soft2])
    return Q @ D @ Q.T


def hessian_log_uniform(lam_max, lam_min, rot_seed=2):
    rng = np.random.default_rng(rot_seed)
    A = rng.standard_normal((NDIM, NDIM))
    Q, _ = np.linalg.qr(A)
    logs = np.linspace(np.log(lam_max), np.log(lam_min), NDIM)
    D = np.diag(np.exp(logs))
    return Q @ D @ Q.T


def laplace_log_volume(H):
    # ln V_Laplace = (D/2) ln(2π) - 0.5 ln det(H/2)  (using -2 ln L = chi^2)
    # Fisher I = 0.5 * H_chi2  => posterior covariance = I^{-1} = 2 H_chi2^{-1}
    # ln V = 0.5 D ln(2π) + 0.5 ln det(2 H^{-1})
    sign, logdet = np.linalg.slogdet(H)
    if sign <= 0:
        return None
    return 0.5 * NDIM * np.log(2 * np.pi) + 0.5 * (NDIM * np.log(2.0) - logdet)


def prior_log_volume():
    return float(np.sum(np.log(2 * PRIOR_HALFWIDTH)))


# ---------------------------------------------------------------
# Information-geometry diagnostics on the Fisher matrix
# ---------------------------------------------------------------
def diagnostics(H, label, h_step=None):
    # Convert chi² Hessian to Fisher information
    F = 0.5 * H
    eigs = np.sort(eigvalsh(F))[::-1]
    eigs_pos = eigs[eigs > 0]
    kappa = eigs_pos[0] / eigs_pos[-1] if len(eigs_pos) >= 2 else np.inf
    pr = (eigs_pos.sum() ** 2) / (eigs_pos ** 2).sum()
    # Effective integer dim — count eigenvalues above 1% of max
    d_above = int(np.sum(eigs_pos > 0.01 * eigs_pos[0]))

    # Geodesic distance from THETA_STAR to THETA_LCDM in info metric
    # (constant metric = Fisher at peak; straight line)
    delta = THETA_LCDM - THETA_STAR
    geo2 = float(delta @ F @ delta)
    geo = float(np.sqrt(max(geo2, 0.0)))

    # Reference: distance if we only moved σ_cluster (component 1) the same dex
    delta_clu = np.array([0.0, THETA_LCDM[1] - THETA_STAR[1], 0.0])
    geo_clu = float(np.sqrt(delta_clu @ F @ delta_clu))

    # Laplace volume vs prior — implied marginal ΔlnZ contribution from Occam
    lnV_L = laplace_log_volume(H)
    lnV_prior = prior_log_volume()
    occam = lnV_prior - lnV_L if lnV_L is not None else None

    # Reparameterization check: rescale θ → 2θ. Fisher transforms as F' = F/4.
    # Dimensionless invariants (κ, PR) must be unchanged.
    F_rep = 0.25 * F
    eigs_rep = np.sort(eigvalsh(F_rep))[::-1]
    eigs_rep_pos = eigs_rep[eigs_rep > 0]
    kappa_rep = eigs_rep_pos[0] / eigs_rep_pos[-1] if len(eigs_rep_pos) >= 2 else np.inf
    pr_rep = (eigs_rep_pos.sum() ** 2) / (eigs_rep_pos ** 2).sum()
    invariant_kappa = abs(kappa - kappa_rep) / max(kappa, 1.0)
    invariant_pr = abs(pr - pr_rep) / max(pr, 1.0)

    return {
        "label": label,
        "h_step": h_step,
        "eigenvalues_F": [float(x) for x in eigs.tolist()],
        "condition_number": float(kappa),
        "log10_kappa": float(np.log10(kappa)),
        "participation_ratio": float(pr),
        "d_eff_integer": d_above,
        "geodesic_to_LCDM": geo,
        "geodesic_cluster_only": geo_clu,
        "lnV_Laplace": lnV_L,
        "lnV_prior": lnV_prior,
        "occam_penalty": occam,
        "reparam_kappa_drift": float(invariant_kappa),
        "reparam_PR_drift": float(invariant_pr),
    }


# ---------------------------------------------------------------
# Calibrate scales so each Hessian matches an Occam penalty close to 12.2
# ---------------------------------------------------------------
def calibrate(builder, target=LOG_VOL_GAP, scan=np.geomspace(0.01, 1000.0, 401)):
    best = None
    lnV_prior = prior_log_volume()
    for s in scan:
        H = builder(s)
        lnV_L = laplace_log_volume(H)
        if lnV_L is None:
            continue
        occam = lnV_prior - lnV_L
        if best is None or abs(occam - target) < abs(best[0] - target):
            best = (occam, s, H)
    return best  # (achieved_occam, scale, H)


def main():
    out = {
        "anchors": {
            "DLNZ_FIXED": DLNZ_FIXED,
            "DLNZ_MARGINAL": DLNZ_MARGINAL,
            "log_volume_gap": LOG_VOL_GAP,
            "ndim": NDIM,
            "prior_halfwidth": PRIOR_HALFWIDTH.tolist(),
            "theta_LCDM": THETA_LCDM.tolist(),
        },
        "cases": [],
    }

    # (a) isotropic — calibrate a single scale s so Occam ≈ 12.2
    occ_a, s_a, H_a = calibrate(lambda s: hessian_isotropic(s))
    out["cases"].append({
        "shape": "isotropic",
        "calibration_scale": float(s_a),
        "achieved_occam": float(occ_a),
        **diagnostics(H_a, "isotropic"),
    })

    # (b) anisotropic 1 stiff + 2 soft (ratio 100:1:1 typical sloppy)
    occ_b, s_b, H_b = calibrate(
        lambda s: hessian_anisotropic(stiff=100.0 * s, soft1=s, soft2=s)
    )
    out["cases"].append({
        "shape": "anisotropic_100_1_1",
        "calibration_scale": float(s_b),
        "achieved_occam": float(occ_b),
        **diagnostics(H_b, "anisotropic_100_1_1"),
    })

    # (c) log-uniform — Sethna sloppy spectrum (10^4 : 10^2 : 10^0)
    occ_c, s_c, H_c = calibrate(
        lambda s: hessian_log_uniform(lam_max=1e4 * s, lam_min=s)
    )
    out["cases"].append({
        "shape": "log_uniform_1e4_to_1",
        "calibration_scale": float(s_c),
        "achieved_occam": float(occ_c),
        **diagnostics(H_c, "log_uniform_1e4_to_1"),
    })

    # (d) very anisotropic (1 stiff + 2 ultra-soft, 1e6:1:1)
    occ_d, s_d, H_d = calibrate(
        lambda s: hessian_anisotropic(stiff=1e6 * s, soft1=s, soft2=s)
    )
    out["cases"].append({
        "shape": "anisotropic_1e6_1_1",
        "calibration_scale": float(s_d),
        "achieved_occam": float(occ_d),
        **diagnostics(H_d, "anisotropic_1e6_1_1"),
    })

    # ----- Posterior volume Monte-Carlo (case b vs c) for cross-check -----
    # Sample from prior, weight by Gaussian likelihood, compute effective volume.
    def mc_posterior_volume(H, n=200_000):
        F = 0.5 * H
        # Draw uniform prior
        u = (RNG.random((n, NDIM)) * 2 - 1) * PRIOR_HALFWIDTH
        # chi² = u^T H u
        chi2 = np.einsum("ni,ij,nj->n", u, H, u)
        w = np.exp(-0.5 * chi2)
        Z_prior = w.mean() * np.prod(2 * PRIOR_HALFWIDTH)
        return float(np.log(Z_prior + 1e-300))

    out["mc_check"] = {}
    for case_idx, H in [("b", H_b), ("c", H_c)]:
        lnZ_mc = mc_posterior_volume(H)
        # Compare to Laplace ln Z = -0.5 chi²_min + ln V_Laplace = 0 + lnV_L
        lnV_L = laplace_log_volume(H)
        out["mc_check"][case_idx] = {
            "lnZ_MC": lnZ_mc,
            "lnZ_Laplace": lnV_L,
            "diff": lnZ_mc - lnV_L,
        }

    # ----- Verdict -----
    # PASS-of-sloppy claim: at least one realistic case (b or c) with
    #   κ > 100  AND  PR < 2  AND  reparam invariants drift < 1e-9
    def verdict(case):
        return (case["condition_number"] > 100.0
                and case["participation_ratio"] < 2.0
                and case["reparam_kappa_drift"] < 1e-9
                and case["reparam_PR_drift"] < 1e-9)

    sloppy_cases = [c for c in out["cases"] if verdict(c)]
    out["verdict"] = {
        "any_sloppy": bool(sloppy_cases),
        "sloppy_shapes": [c["shape"] for c in sloppy_cases],
        "interpretation": (
            "If any sloppy shape achieves Occam ≈12.2, then the L281 "
            "marginalized ΔlnZ=0.8 collapse is consistent with a 1-stiff "
            "+ 2-soft (or log-uniform) Fisher structure rather than "
            "honest 3-parameter Bayesian volume. BB's '3 regimes' should "
            "be reported as ~1-2 effective dof in Sec 3/Sec 6."
        ),
    }

    out_path = os.path.join(os.path.dirname(__file__), "report.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    # Console summary (ASCII only)
    print("=== L323 information-geometry summary ===")
    print(f"target Occam (ln V_prior - ln V_Laplace) = {LOG_VOL_GAP:.2f}")
    for c in out["cases"]:
        print(
            f"[{c['shape']:30s}] occam={c['achieved_occam']:.2f}"
            f" kappa={c['condition_number']:.3e}"
            f" PR={c['participation_ratio']:.3f}"
            f" d_eff_int={c['d_eff_integer']}"
            f" geo_LCDM={c['geodesic_to_LCDM']:.3f}"
            f" geo_clu={c['geodesic_cluster_only']:.3f}"
            f" reparam_dk={c['reparam_kappa_drift']:.1e}"
        )
    print("MC vs Laplace cross-check:", out["mc_check"])
    print("verdict:", out["verdict"])
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
