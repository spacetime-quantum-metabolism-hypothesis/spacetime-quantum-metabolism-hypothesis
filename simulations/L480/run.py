"""L480 — Matter-DE crossover deepen.

Goals (numerical):
  1) B/A scan: for each B/A in a wide grid, find cancellation radius r* where
     sigma_eff(r) = A * rho_m(r) - B * rho_L0 crosses zero, on a NFW toy
     halo of mass M_vir and concentration c.
  2) Test the L466 closure conjecture B/A = Om/OL ~ 0.46
     ("background steady state" condition) and check whether the resulting
     cancellation radius is naturally on the cluster outskirt scale.
  3) Cluster-scale match: vary M_vir over the cluster mass range
     (1e13 - 1e15 Msun) and check r* / r_vir scaling.  The question we are
     trying to answer numerically: does the B/A=Om/OL closure produce a
     *single* cancellation radius in units of r_vir (i.e. is the crossover
     radius cluster-scale-invariant), or does it drift with halo mass?

No theory map: no physical Lagrangian assumed beyond the linear ansatz that
L466 already wrote down (sigma_eff = A rho_m - B rho_Lambda).  Honest scan only.
"""

from __future__ import annotations
import os
import json
import numpy as np

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

OUT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "results", "L480")
)
os.makedirs(OUT_DIR, exist_ok=True)


# ---- background ----
Om = 0.315
OL = 0.685
H0 = 67.4  # km/s/Mpc
G = 4.302e-9  # Mpc Msun^-1 (km/s)^2
RHO_CRIT_0 = 3 * H0 ** 2 / (8 * np.pi * G)  # Msun / Mpc^3
RHO_M0 = Om * RHO_CRIT_0
RHO_L0 = OL * RHO_CRIT_0
DELTA_VIR = 200.0  # virial overdensity convention


def r_vir_from_mass(M_vir_Msun: float) -> float:
    """r_vir from the 200*rho_crit definition: M_vir = (4/3) pi r_vir^3 * 200 rho_crit_0."""
    return (3.0 * M_vir_Msun / (4.0 * np.pi * DELTA_VIR * RHO_CRIT_0)) ** (1.0 / 3.0)


def rho_nfw_over_crit(r_over_rvir: np.ndarray, c: float = 5.0) -> np.ndarray:
    x = r_over_rvir * c
    raw = 1.0 / (x * (1.0 + x) ** 2 + 1e-30)
    mu = np.log(1.0 + c) - c / (1.0 + c)
    rho_s_over_crit = (DELTA_VIR / 3.0) * c ** 3 / mu
    return rho_s_over_crit * raw


def rho_2halo_floor() -> float:
    """At very large r/r_vir, NFW alone -> 0.  Add a 2-halo floor at the cosmic
    mean: rho_m -> Om * rho_crit_0.  Returned in units of rho_crit_0."""
    return Om


def rho_total_over_crit(r_over_rvir: np.ndarray, c: float = 5.0) -> np.ndarray:
    """1-halo NFW + 2-halo floor at cosmic mean."""
    return rho_nfw_over_crit(r_over_rvir, c) + rho_2halo_floor()


def find_first_zero(r: np.ndarray, y: np.ndarray):
    sgn = np.sign(y)
    idx = np.where(np.diff(sgn) != 0)[0]
    if not idx.size:
        return None
    i = idx[0]
    if y[i + 1] == y[i]:
        return float(r[i])
    return float(r[i] - y[i] * (r[i + 1] - r[i]) / (y[i + 1] - y[i]))


def scan_BA(BA_grid: np.ndarray, c: float = 5.0):
    r = np.logspace(-2, 1.5, 1200)  # r/r_vir in [0.01, ~31.6]
    rho_ratio = rho_total_over_crit(r, c=c)  # rho_m(r) / rho_crit_0
    out = []
    for BA in BA_grid:
        sigma_eff = rho_ratio - BA * OL  # A := 1
        r_star = find_first_zero(r, sigma_eff)
        rho_star = None
        if r_star is not None:
            rho_star = float(np.interp(r_star, r, rho_ratio))
        out.append({
            "B_over_A": float(BA),
            "r_star_over_rvir": r_star,
            "rho_m_at_r_star_over_rho_crit": rho_star,
        })
    return out, r, rho_ratio


def cluster_mass_scan(BA: float, c: float = 5.0):
    """Vary halo mass and report r_star / r_vir (which is profile-scale-invariant
    when r_total is parametrised in r/r_vir, modulo the additive 2-halo floor
    Om — the *only* mass-dependent feature here is the 2-halo floor since rho_crit_0
    is universal). So this loop checks whether changing M_vir (and hence r_vir Mpc)
    moves r_star by changing the *physical* radius at which rho_m / rho_crit_0
    crosses BA*OL."""
    masses = np.logspace(13.0, 15.0, 9)  # 1e13 .. 1e15 Msun
    r = np.logspace(-2, 1.5, 1200)
    rho_ratio = rho_total_over_crit(r, c=c)
    sigma_eff = rho_ratio - BA * OL
    r_star = find_first_zero(r, sigma_eff)
    rows = []
    for M in masses:
        rvir = r_vir_from_mass(M)
        rows.append({
            "M_vir_Msun": float(M),
            "r_vir_Mpc": float(rvir),
            "r_star_over_rvir": r_star,
            "r_star_Mpc": float(r_star * rvir) if r_star is not None else None,
        })
    return rows


def main():
    # 1) wide B/A scan including the L466 closure value Om/OL
    BA_closure = Om / OL  # ~ 0.4599
    BA_grid = np.array(sorted(set([
        0.1, 0.2, 0.3, BA_closure, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0
    ])))
    scan, r, rho_ratio = scan_BA(BA_grid, c=5.0)

    # 2) cluster-scale match at the closure ratio
    closure_match = cluster_mass_scan(BA_closure, c=5.0)
    natural_match = cluster_mass_scan(1.0, c=5.0)

    # 3) sensitivity to concentration
    c_scan = []
    for c_val in [3.0, 4.0, 5.0, 7.0, 10.0]:
        rho_ratio_c = rho_total_over_crit(r, c=c_val)
        rstar = find_first_zero(r, rho_ratio_c - BA_closure * OL)
        c_scan.append({
            "c": c_val,
            "r_star_over_rvir_at_BA_closure": rstar,
        })

    # 4) "naturalness" indicator: how many e-folds of B/A produce r* in the
    #    cluster outskirt band [1, 10] r_vir?
    fine = np.logspace(-2, 1.5, 4000)
    rho_fine = rho_total_over_crit(fine, c=5.0)
    BA_dense = np.logspace(-2, 1.5, 600)
    in_band = 0
    rstar_curve = []
    for BA in BA_dense:
        rs = find_first_zero(fine, rho_fine - BA * OL)
        rstar_curve.append(rs if rs is not None else np.nan)
        if rs is not None and 1.0 <= rs <= 10.0:
            in_band += 1
    frac_in_outskirt = in_band / len(BA_dense)

    summary = {
        "background": {"Om": Om, "OL": OL, "rho_crit_0_Msun_Mpc3": float(RHO_CRIT_0)},
        "closure_BA_Om_over_OL": float(BA_closure),
        "scan_BA_to_r_star": scan,
        "cluster_mass_scan_at_BA_closure": closure_match,
        "cluster_mass_scan_at_BA_1": natural_match,
        "concentration_sensitivity_at_BA_closure": c_scan,
        "fraction_of_log_BA_grid_giving_r_star_in_outskirt_band_1_to_10_rvir":
            float(frac_in_outskirt),
        "interpretation_one_liner": (
            "B/A = Om/OL = 0.46 IS the background-null closure; r* lands at "
            "rho_m=Om*rho_crit_0 i.e. cosmic mean -> in NFW+2halo this is at "
            "the 2-halo floor (asymptotic), not a discrete radius. Without the "
            "2-halo floor the crossing sits in the outskirt band; with the "
            "floor included the closure case becomes degenerate. Honest answer: "
            "Om/OL is not derived, it is *imposed* by demanding <sigma_eff>=0 on "
            "the cosmic mean, which trivialises the cluster crossover."
        ),
    }

    out_path = os.path.join(OUT_DIR, "scan_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    np.savez(
        os.path.join(OUT_DIR, "ba_curve.npz"),
        BA_dense=BA_dense,
        r_star_dense=np.array(rstar_curve, dtype=float),
        r=r,
        rho_ratio=rho_ratio,
    )

    print("L480 done.")
    print(f"  closure B/A = Om/OL = {BA_closure:.4f}")
    closure_rstar = scan[list(BA_grid).index(BA_closure)]["r_star_over_rvir"]
    print(f"  r*/r_vir at closure = {closure_rstar}")
    print(f"  fraction of log B/A grid producing r* in [1,10] r_vir = "
          f"{frac_in_outskirt:.3f}")
    print("  written:", out_path)


if __name__ == "__main__":
    main()
