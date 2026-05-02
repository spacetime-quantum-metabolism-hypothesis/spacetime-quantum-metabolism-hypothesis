"""L466 free speculation toy: cluster-scale dip via matter-Lambda crossover cancellation.

Hypothesis (speculative, no map):
  axiom 1 (absorption) sources sigma_abs scales with environmental matter density rho_m.
  axiom 3 (generation) sources sigma_gen scales with vacuum / Lambda density rho_L (uniform).
  Cluster-averaged density rho_cl ~ a few hundred * rho_crit; in the deep DM-dominated
  region of the cluster, rho_m >> rho_L. But on cluster *outskirts* and stacked averages
  (R ~ R_200 .. several R_200) the locally averaged matter density crosses through the
  comoving Lambda scale rho_L0 ~ 0.7 * rho_crit_0. There the two source terms can
  partially cancel:

      sigma_eff(r) = sigma_abs(rho_m(r)) - sigma_gen(rho_L)
                   ~ A * rho_m(r) - B * rho_L0

  with rho_m(r) ~ rho_crit_0 * Om * (1 + delta(r)). A "dip" appears wherever
  sigma_eff -> 0, i.e. delta(r) ~ (B/A) * rho_L0 / (Om * rho_crit_0) - 1.

This script:
  1) sweeps a cluster radial profile rho_m(r) (NFW-ish toy).
  2) computes sigma_eff(r) for several (A, B) ratios.
  3) flags the radius where sigma_eff = 0  (candidate "dip").
  4) sketches scale dependence: which cluster mass / radius shows strongest cancellation.

NOT a derivation of L466 amplitude — just a numerical sketch consistent with the
"cluster dip" puzzle.
"""

from __future__ import annotations
import os
import json
import numpy as np

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "results", "L466")
OUT_DIR = os.path.abspath(OUT_DIR)
os.makedirs(OUT_DIR, exist_ok=True)


# ---- background densities (today) ----
Om = 0.315
OL = 0.685
# rho_crit_0 in Msun / Mpc^3 for h=0.674 (handy units; only ratios matter below)
H0 = 67.4  # km/s/Mpc
G = 4.302e-9  # Mpc Msun^-1 (km/s)^2
RHO_CRIT_0 = 3 * H0 ** 2 / (8 * np.pi * G)  # Msun / Mpc^3
RHO_M0 = Om * RHO_CRIT_0
RHO_L0 = OL * RHO_CRIT_0


# ---- NFW-ish toy cluster: rho_m(r) = rho_s / [ (r/rs) (1+r/rs)^2 ] ----
def rho_nfw(r_over_rvir, c=5.0):
    """Returns rho_m / rho_crit_0 for an NFW with concentration c, normalised so that
    mean overdensity inside r_vir is ~ 200."""
    x = r_over_rvir * c  # x = r/rs
    # raw profile shape
    raw = 1.0 / (x * (1 + x) ** 2 + 1e-30)
    # crude normalisation: at r=rvir mean overdensity ~ 200, central rho_s ~ 200/3 * c^3 / [ln(1+c)-c/(1+c)] * rho_crit
    mu = np.log(1 + c) - c / (1 + c)
    rho_s_over_crit = (200.0 / 3.0) * c ** 3 / mu
    return rho_s_over_crit * raw


def main():
    r = np.logspace(-2, 1.0, 400)  # r/r_vir in [0.01, 10]

    # axiom-balance ratios B/A — which "absorption-vs-generation" balance gives a dip in cluster regime?
    BA_list = [0.5, 1.0, 2.0, 5.0]
    results = {}

    rho_ratio = rho_nfw(r)  # rho_m(r) / rho_crit_0   (delta_total + Om at large r)

    for BA in BA_list:
        # sigma_eff in arbitrary common units, normalised so absorption coefficient A=1
        sigma_eff = rho_ratio - BA * OL  # (A=1) * rho_m/rho_crit_0  -  (B/A) * rho_L0/rho_crit_0
        # dip = sign change
        sign = np.sign(sigma_eff)
        crossings = np.where(np.diff(sign) != 0)[0]
        if crossings.size:
            i = crossings[0]
            # linear interp to zero
            r0 = r[i] - sigma_eff[i] * (r[i + 1] - r[i]) / (sigma_eff[i + 1] - sigma_eff[i])
            rho_at_zero = rho_ratio[i] - sigma_eff[i] * (rho_ratio[i + 1] - rho_ratio[i]) / (
                sigma_eff[i + 1] - sigma_eff[i]
            )
        else:
            r0 = None
            rho_at_zero = None
        results[f"BA_{BA}"] = {
            "B_over_A": BA,
            "r_dip_over_rvir": r0,
            "rho_m_at_dip_over_rho_crit": rho_at_zero,
            "rho_L0_over_rho_crit": OL,
            "comment": "sigma_eff=0 means absorption = generation; environment-dependent absorption "
            "matched against environment-uniform generation",
        }

    # scale dependence: fix BA=1 ("natural" SQMH symmetric) and find where the dip lives
    BA = 1.0
    sigma_eff = rho_ratio - BA * OL
    # depth at large r (asymptotic background): rho_m -> 0, sigma_eff -> -BA*OL  (net generation)
    asymptotic = -BA * OL
    # depth in cluster core: rho_m huge, sigma_eff -> +large (net absorption)
    summary = {
        "Om": Om,
        "OL": OL,
        "RHO_CRIT_0_Msun_per_Mpc3": RHO_CRIT_0,
        "asymptotic_sigma_eff_BA1": asymptotic,
        "cluster_core_sigma_eff_BA1_at_001rvir": float(rho_ratio[0] - BA * OL),
        "dip_radius_BA1_over_rvir": results["BA_1.0"]["r_dip_over_rvir"],
        "scan": results,
        "interpretation": (
            "For B/A=1 the cancellation radius sits at rho_m(r)/rho_crit_0 ~ OL ~ 0.685. "
            "That is exactly the cluster *outskirts* / 1-halo to 2-halo transition (a few r_vir). "
            "Inside r_vir the absorption term dominates (positive sigma_eff). Far outside it the "
            "Lambda generation dominates (negative sigma_eff). The crossover band is the "
            "candidate cluster dip in metabolism rate."
        ),
    }

    out_path = os.path.join(OUT_DIR, "toy_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # also dump the raw curve for plotting
    np.savez(
        os.path.join(OUT_DIR, "toy_curve.npz"),
        r_over_rvir=r,
        rho_m_over_rhocrit=rho_ratio,
        sigma_eff_BA1=sigma_eff,
    )

    print("L466 toy done. dip radius (B/A=1) r/r_vir =", summary["dip_radius_BA1_over_rvir"])
    print("written:", out_path)


if __name__ == "__main__":
    main()
