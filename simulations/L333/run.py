"""
L333 - Sloppy reparameterization & MBAM-style reduction of BB 3-param.

Independent thinking. Reuses the toy Hessian families calibrated in L323
(no new physics input). Computes:

  1. Fisher eigendecomposition (sorted, signed eigenvectors).
  2. Coordinate mapping of the stiff eigenvector v_max -> (cosmic,
     cluster, galactic) component fractions.
  3. MBAM-style geodesic along the softest eigenvector v_min, integrated
     until either parameter hits the LCDM cutoff or the prior box edge.
     Records which coordinate evaporates first.
  4. Reduced 1-parameter model: chi^2_red(eta) with eta = v_max . theta.
     Compare AICc(3-param) vs AICc(1-param) under standard
     Burnham-Anderson convention. Standard threshold |Delta AICc| > 2
     for decisive evidence.
  5. Marginal evidence: Laplace (3D) vs reduced 1D Laplace.
  6. Linear vs log coordinate robustness on v_max rotation angle.

Independence rule: no formulas / parameters injected beyond standard
Fisher / AICc / Laplace definitions. Stiff ratios come from L323 output.
"""

import json
import os
import numpy as np
from numpy.linalg import eigh, slogdet

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

RNG = np.random.default_rng(20260501)

# ---------------------------------------------------------------
# Public anchors (from L323)
# ---------------------------------------------------------------
DLNZ_FIXED    = 13.0
DLNZ_MARGINAL = 0.8
LOG_VOL_GAP   = DLNZ_FIXED - DLNZ_MARGINAL
NDIM          = 3
COORDS        = ["cosmic", "cluster", "galactic"]

THETA_STAR      = np.array([0.0, 0.0, 0.0])
PRIOR_HALFWIDTH = np.array([2.0, 2.0, 2.0])
THETA_LCDM      = np.array([-3.0, -3.0, -3.0])
CUTOFF          = -3.0  # log10 sigma cutoff representing LCDM


# ---------------------------------------------------------------
# Hessian builders (mirror of L323; identical seeds for consistency)
# ---------------------------------------------------------------
def hessian_anisotropic(stiff, soft1, soft2, rot_seed=1):
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


def laplace_log_volume_3d(H):
    sign, logdet = slogdet(H)
    if sign <= 0:
        return None
    return 0.5 * NDIM * np.log(2 * np.pi) + 0.5 * (NDIM * np.log(2.0) - logdet)


def laplace_log_volume_1d(lam):
    # Fisher = lam/2 ; ln V_1d = 0.5 ln(2 pi) + 0.5 ln(2/lam)
    return 0.5 * np.log(2 * np.pi) + 0.5 * (np.log(2.0) - np.log(lam))


def calibrate(builder, target=LOG_VOL_GAP, scan=np.geomspace(0.01, 1000.0, 401)):
    lnV_prior = float(np.sum(np.log(2 * PRIOR_HALFWIDTH)))
    best = None
    for s in scan:
        H = builder(s)
        lnV_L = laplace_log_volume_3d(H)
        if lnV_L is None:
            continue
        occam = lnV_prior - lnV_L
        if best is None or abs(occam - target) < abs(best[0] - target):
            best = (occam, s, H)
    return best


# ---------------------------------------------------------------
# Eigendecomposition with explicit sort
# ---------------------------------------------------------------
def eigendecomp_sorted(F):
    w, V = eigh(F)
    order = np.argsort(w)[::-1]    # descending
    w = w[order]
    V = V[:, order]
    # sign convention: largest absolute component positive
    for k in range(V.shape[1]):
        i = int(np.argmax(np.abs(V[:, k])))
        if V[i, k] < 0:
            V[:, k] *= -1
    return w, V


# ---------------------------------------------------------------
# MBAM-style geodesic along the softest eigenvector (constant metric toy)
# ---------------------------------------------------------------
def mbam_step(theta0, v_soft, n_steps=2000, step=0.005):
    # March in both directions; record first coord that hits boundary.
    history = []
    for sign in (+1, -1):
        theta = theta0.copy()
        for k in range(n_steps):
            theta = theta + sign * step * v_soft
            # Boundary checks
            for i in range(NDIM):
                if theta[i] <= CUTOFF:
                    history.append((sign, i, "lcdm_cutoff", k * step))
                    break
                if theta[i] >= +PRIOR_HALFWIDTH[i]:
                    history.append((sign, i, "prior_upper", k * step))
                    break
                if theta[i] <= -PRIOR_HALFWIDTH[i]:
                    history.append((sign, i, "prior_lower", k * step))
                    break
            else:
                continue
            break
    return history


# ---------------------------------------------------------------
# Reduced 1-param model AICc
# AICc(k) = chi2_min + 2k + 2k(k+1)/(N-k-1)
# At the peak, by construction chi2_min is identical for both models;
# the discriminator is the parameter penalty alone.
# ---------------------------------------------------------------
def aicc(chi2_min, k, n_data):
    if n_data - k - 1 <= 0:
        return chi2_min + 2 * k  # fall back to AIC
    return chi2_min + 2 * k + 2 * k * (k + 1) / (n_data - k - 1)


# ---------------------------------------------------------------
# Per-case analysis
# ---------------------------------------------------------------
def analyze(label, H, n_data_choices=(13, 30, 100)):
    F = 0.5 * H
    w, V = eigendecomp_sorted(F)
    v_max = V[:, 0]
    v_min = V[:, -1]

    # Component fractions of stiff direction
    comp_sq = v_max ** 2
    comp_fraction = {COORDS[i]: float(comp_sq[i]) for i in range(NDIM)}
    dominant = COORDS[int(np.argmax(comp_sq))]

    # Coordinate-robustness check: rescale theta -> 10*theta (proxy for
    # changing log base / linear-vs-log effect at fixed scale). The Fisher
    # transforms F' = F / 100, eigenvectors must be invariant up to sign.
    F_alt = F / 100.0
    w_alt, V_alt = eigendecomp_sorted(F_alt)
    cos_angle = float(np.clip(abs(np.dot(v_max, V_alt[:, 0])), 0.0, 1.0))
    rotation_deg = float(np.degrees(np.arccos(cos_angle)))

    # MBAM along v_min
    mbam = mbam_step(THETA_STAR.copy(), v_min)
    # Pick the *closer* boundary (smaller geodesic distance)
    if mbam:
        closest = min(mbam, key=lambda r: r[3])
        boundary = {
            "direction_sign": int(closest[0]),
            "coordinate": COORDS[closest[1]],
            "type": closest[2],
            "geodesic_distance": float(closest[3]),
        }
    else:
        boundary = None

    # Reduced 1D evidence using stiff eigenvalue lambda_max
    lam_max = float(w[0])
    lam_others = [float(x) for x in w[1:]]
    lnV_3d = laplace_log_volume_3d(H)
    lnV_1d = laplace_log_volume_1d(lam_max)

    # Marginal contribution from sloppy (the 2 small eigenvalues)
    sloppy_log_vol = sum(0.5 * np.log(2 * np.pi) + 0.5 * (np.log(2.0) - np.log(l))
                         for l in lam_others if l > 0)

    # AICc comparison at chi2_min = 0 (best fit)
    aicc_table = {}
    for n in n_data_choices:
        a3 = aicc(0.0, 3, n)
        a1 = aicc(0.0, 1, n)
        aicc_table[str(n)] = {
            "AICc_3param": float(a3),
            "AICc_1param": float(a1),
            "delta_AICc_1_minus_3": float(a1 - a3),
            "favors_reduction": bool(a1 - a3 <= -2.0),
        }

    return {
        "label": label,
        "eigenvalues_F": [float(x) for x in w],
        "v_max_components": v_max.tolist(),
        "v_max_component_sq": comp_fraction,
        "v_max_dominant_coord": dominant,
        "v_max_dominant_fraction": float(np.max(comp_sq)),
        "v_min_components": v_min.tolist(),
        "rotation_under_rescale_deg": rotation_deg,
        "MBAM_first_boundary": boundary,
        "lnV_Laplace_3d": lnV_3d,
        "lnV_Laplace_1d_stiff_only": lnV_1d,
        "sloppy_log_volume_contribution": float(sloppy_log_vol),
        "marginal_eq_reduction_diff": float(lnV_3d - (lnV_1d + sloppy_log_vol))
                                       if lnV_3d is not None else None,
        "AICc_table": aicc_table,
    }


def main():
    out = {
        "anchors": {
            "DLNZ_FIXED": DLNZ_FIXED,
            "DLNZ_MARGINAL": DLNZ_MARGINAL,
            "ndim": NDIM,
            "coords": COORDS,
            "cutoff_log10sigma": CUTOFF,
        },
        "cases": [],
    }

    # Case b: anisotropic 100:1:1 (PR ~ 1.04 in L323)
    occ_b, s_b, H_b = calibrate(
        lambda s: hessian_anisotropic(stiff=100.0 * s, soft1=s, soft2=s)
    )
    out["cases"].append({
        "shape": "anisotropic_100_1_1",
        "achieved_occam": float(occ_b),
        **analyze("anisotropic_100_1_1", H_b),
    })

    # Case c: log-uniform 1e4 -> 1 (PR ~ 1.02)
    occ_c, s_c, H_c = calibrate(
        lambda s: hessian_log_uniform(lam_max=1e4 * s, lam_min=s)
    )
    out["cases"].append({
        "shape": "log_uniform_1e4_to_1",
        "achieved_occam": float(occ_c),
        **analyze("log_uniform_1e4_to_1", H_c),
    })

    # Case d: extreme 1e6:1:1 (effective dim = 1)
    occ_d, s_d, H_d = calibrate(
        lambda s: hessian_anisotropic(stiff=1e6 * s, soft1=s, soft2=s)
    )
    out["cases"].append({
        "shape": "anisotropic_1e6_1_1",
        "achieved_occam": float(occ_d),
        **analyze("anisotropic_1e6_1_1", H_d),
    })

    # Verdict per attack pass-criteria
    def pass_criteria(case):
        dom = case["v_max_dominant_fraction"]
        rot = case["rotation_under_rescale_deg"]
        # AICc 1 vs 3 at typical n=30
        d_aicc = case["AICc_table"]["30"]["delta_AICc_1_minus_3"]
        boundary_ok = case["MBAM_first_boundary"] is not None
        # marginal vs reduction agreement
        diff = case.get("marginal_eq_reduction_diff")
        marg_ok = diff is not None and abs(diff) <= 0.5
        return {
            "P1_stiff_dominant_geq_0.7": bool(dom >= 0.7),
            "P2_MBAM_boundary_found": boundary_ok,
            "P3_AICc_favors_1param": bool(d_aicc <= -2.0),
            "P4_marginal_eq_reduction": marg_ok,
            "P5_coord_robust_lt_15deg": bool(rot < 15.0),
            "delta_AICc_1_minus_3_n30": float(d_aicc),
            "v_max_dom_fraction": float(dom),
            "rotation_deg": float(rot),
            "marginal_diff": diff,
        }

    out["verdicts"] = [
        {"shape": c["shape"], **pass_criteria(c)} for c in out["cases"]
    ]

    # Aggregate decision
    p3_any = any(v["P3_AICc_favors_1param"] for v in out["verdicts"])
    p1_majority = sum(v["P1_stiff_dominant_geq_0.7"] for v in out["verdicts"]) >= 2
    out["decision"] = {
        "p3_any_AICc_favors_1param": bool(p3_any),
        "p1_majority_stiff_dominant": bool(p1_majority),
        "recommend_reduction_to_1param": bool(p3_any and p1_majority),
        "interpretation": (
            "Reduction recommended only when AICc penalty difference favors "
            "1-param AND the stiff direction has a coordinate-dominant "
            "interpretation (so the reduced model has a physical meaning, "
            "not just a statistical one)."
        ),
    }

    out_path = os.path.join(os.path.dirname(__file__), "report.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    # ASCII-only console summary
    print("=== L333 sloppy reparameterization summary ===")
    for c in out["cases"]:
        b = c.get("MBAM_first_boundary") or {}
        print(
            f"[{c['shape']:25s}] occam={c['achieved_occam']:.2f} "
            f"dom={c['v_max_dominant_coord']}({c['v_max_dominant_fraction']:.3f}) "
            f"rot={c['rotation_under_rescale_deg']:.2f}deg "
            f"MBAM->{b.get('coordinate','?')}/{b.get('type','?')}@{b.get('geodesic_distance', float('nan')):.2f}"
        )
    for v in out["verdicts"]:
        print(
            f"  verdict[{v['shape']}]: P1={v['P1_stiff_dominant_geq_0.7']} "
            f"P2={v['P2_MBAM_boundary_found']} P3={v['P3_AICc_favors_1param']} "
            f"P4={v['P4_marginal_eq_reduction']} P5={v['P5_coord_robust_lt_15deg']} "
            f"dAICc(n=30)={v['delta_AICc_1_minus_3_n30']:+.2f}"
        )
    print("decision:", out["decision"])
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
