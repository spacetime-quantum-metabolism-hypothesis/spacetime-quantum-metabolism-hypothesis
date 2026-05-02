"""
L332 anchor candidate forecast — Fisher-information scoping.

Goal: estimate ΔAICc(2→3) shift from adding hypothetical anchor data
(P9 dSph, P11 NS saturation, Void galaxies) to baseline (DESI BAO + SN + CMB).

This is a FORECAST / SCOPING tool, not a full posterior. Order-of-magnitude only.
Honest: results are based on toy g(rm1) curvature differences between 2-regime
sigmoid-weight model and 3-regime separate-amp model, NOT on real anchor data.
"""

import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import json
import numpy as np

# --- L322 baseline parameters (placeholder; replace with actual best-fit) ---
# 2-regime merge model: g(rm1) = amp * [w_lo*tanh(c*rm1) + w_hi*rm1],
#   w_lo = 1/(1+exp((rm1 - r0)/dr)), w_hi = 1 - w_lo
# 3-regime model: separate amp_lo (tanh), amp_mid (linear in rm1), amp_hi (linear).
BASELINE_2R = dict(amp=0.42, c=2.1, r0=0.6, dr=0.25)
BASELINE_3R = dict(amp_lo=0.40, c=2.0, amp_mid=0.45, amp_hi=0.52,
                   r_lm=0.35, r_mh=0.95, dr=0.18)

# Current evidence from L322: ΔAICc(2→3) = +0.77 (2-regime favored by 0.77).
DELTA_AICC_BASELINE = +0.77


def g_2regime(rm1, p):
    rm1 = np.clip(rm1, 0.0, 200.0)
    w_lo = 1.0 / (1.0 + np.exp((rm1 - p["r0"]) / p["dr"]))
    w_hi = 1.0 - w_lo
    return p["amp"] * (w_lo * np.tanh(p["c"] * rm1) + w_hi * rm1)


def g_3regime(rm1, p):
    rm1 = np.clip(rm1, 0.0, 200.0)
    s_lm = 1.0 / (1.0 + np.exp((rm1 - p["r_lm"]) / p["dr"]))
    s_mh = 1.0 / (1.0 + np.exp((rm1 - p["r_mh"]) / p["dr"]))
    w_lo = s_lm
    w_mid = (1.0 - s_lm) * s_mh
    w_hi = 1.0 - s_lm - w_mid
    return (
        w_lo * p["amp_lo"] * np.tanh(p["c"] * rm1)
        + w_mid * p["amp_mid"] * rm1
        + w_hi * p["amp_hi"] * rm1
    )


def anchor_curvature_diff(rm1_grid, sigma_frac):
    """
    Returns chi2 differential between 2-regime and 3-regime predictions
    over a hypothetical anchor probing rm1_grid with fractional uncertainty sigma_frac.
    Δχ² = sum [(g3 - g2)^2 / (sigma_frac * |g_avg|)^2]
    """
    g2 = g_2regime(rm1_grid, BASELINE_2R)
    g3 = g_3regime(rm1_grid, BASELINE_3R)
    g_avg = 0.5 * (np.abs(g2) + np.abs(g3)) + 1e-12
    sigma = sigma_frac * g_avg
    return float(np.sum((g3 - g2) ** 2 / sigma ** 2))


# --- Anchor candidates (rm1 = ψ0/ψ_z - 1 typical sampling) ---
ANCHORS = {
    "P9_dSph":      dict(rm1=np.array([0.02, 0.04, 0.06, 0.08]), sigma=0.08, dof=1),
    "P11_NS_sat":   dict(rm1=np.array([15.0, 30.0, 60.0, 120.0]), sigma=0.05, dof=1),
    "VoidGalaxies": dict(rm1=np.array([0.10, 0.20, 0.35]),       sigma=0.10, dof=1),
}


def forecast(name, cfg):
    dchi2 = anchor_curvature_diff(cfg["rm1"], cfg["sigma"])
    # 3-regime adds 2 extra params vs 2-regime merge → AICc penalty 4 (for large N).
    delta_aicc_anchor = -dchi2 + 4.0  # negative → favors 3-regime
    delta_aicc_total = DELTA_AICC_BASELINE + delta_aicc_anchor
    return dict(
        anchor=name,
        anchor_dchi2=dchi2,
        delta_aicc_from_anchor=delta_aicc_anchor,
        delta_aicc_total_2_to_3=delta_aicc_total,
        favors_3regime=bool(delta_aicc_total < -2.0),
        marginal=bool(-2.0 <= delta_aicc_total < 0.0),
    )


def main():
    results = {k: forecast(k, v) for k, v in ANCHORS.items()}

    # Joint (rough independence assumption)
    joint_dchi2 = sum(r["anchor_dchi2"] for r in results.values())
    joint = dict(
        anchor="JOINT_P9+P11+Void",
        anchor_dchi2=joint_dchi2,
        delta_aicc_from_anchor=-joint_dchi2 + 4.0,
        delta_aicc_total_2_to_3=DELTA_AICC_BASELINE - joint_dchi2 + 4.0,
        favors_3regime=bool((DELTA_AICC_BASELINE - joint_dchi2 + 4.0) < -2.0),
    )
    results["JOINT"] = joint

    out = dict(
        baseline_delta_aicc_2_to_3=DELTA_AICC_BASELINE,
        threshold_favor_3regime=-2.0,
        forecasts=results,
        honest_caveats=[
            "Forecast uses toy g(rm1) curvature diff between L322 best-fit "
            "2-regime and 3-regime templates; not real anchor data.",
            "EOS systematic for P11 NS_sat NOT marginalized here. Tightening "
            "sigma=0.05 assumes chiral-EFT prior; loose prior would inflate sigma "
            "to ~0.15 and reduce anchor_dchi2 by factor ~9.",
            "Independence assumption for JOINT is optimistic; correlations "
            "(esp. with H0) reduce joint info by 20-40%.",
            "Order-of-magnitude scoping. Decisive forecast requires Phase-2 "
            "FIM with full covariance.",
        ],
    )

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "forecast_result.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print(f"[L332] Forecast written to {out_path}")
    for k, r in results.items():
        print(f"  {k:20s}: dchi2={r['anchor_dchi2']:8.2f}  "
              f"ΔAICc(2→3)_total={r['delta_aicc_total_2_to_3']:+7.2f}  "
              f"favor3={r.get('favors_3regime', False)}")


if __name__ == "__main__":
    main()
