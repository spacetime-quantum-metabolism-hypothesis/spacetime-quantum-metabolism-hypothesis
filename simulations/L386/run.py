"""
L386 — Z_2 SSB finite temperature toy.

Independent derivation by the 8-person team (no map provided).

Goal: estimate T_c, z_PT (domain wall formation epoch), and present-day
domain wall energy density relative to Zel'dovich-Kobzarev-Okun bound.

Strategy (team-derived, recorded here for reproducibility):
  - Take a generic Z_2-symmetric scalar with a vacuum scale eta and a
    quartic self-coupling lam. (eta, lam are scanned, not fixed a priori.)
  - High-T expansion of the 1-loop effective potential gives a thermal
    mass term ~ T^2 phi^2 with coefficient set by lam (and any gauge/
    Yukawa couplings; here pure scalar, coefficient = lam/4 from the
    standard daisy-resummed result for a single real scalar with Z_2).
  - T_c is where the negative mass-squared at the origin is cancelled.
  - Domain wall surface tension sigma_DW ~ eta^3 * sqrt(lam) (kink solution).
  - Wall network in scaling regime: rho_DW(t) ~ sigma_DW / t.
  - Compare rho_DW(t_0) / rho_crit_0 to 1 (Zel'dovich bound).

We scan eta over a wide range (GeV..M_Planck) at a few lam values and
report which (eta, lam) pairs survive Zel'dovich. The point is *structural*:
without an explicit bias term or inflationary dilution, only very low eta
escapes the wall problem.
"""

import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import json
import numpy as np

# ---------------- physical constants (SI + natural where convenient) ----
hbar = 1.054571817e-34          # J s
c    = 2.99792458e8             # m/s
kB   = 1.380649e-23             # J/K
G    = 6.67430e-11              # m^3 kg^-1 s^-2
M_pl_GeV = 1.220890e19          # GeV (Planck mass, not reduced)
GeV_to_J = 1.602176634e-10      # 1 GeV in Joules
GeV_to_K = GeV_to_J / kB        # ~1.16e13 K
GeV_to_invm = GeV_to_J / (hbar * c)  # 1 GeV -> 1/m
H0_SI = 67.4 * 1e3 / 3.0857e22   # 1/s, h=0.674
rho_crit_SI = 3.0 * H0_SI**2 / (8.0 * np.pi * G)   # kg/m^3
rho_crit_GeV4 = rho_crit_SI * c**5 * hbar**3 / GeV_to_J**4  # GeV^4
# Hubble at radiation era: H = 1.66 sqrt(g*) T^2 / M_pl  (natural units, GeV)
G_STAR = 106.75   # SM relativistic dof above EW scale; we keep it constant


# ---------------- Phase A: T_c from daisy-resummed V_eff -----------------
def Tc_GeV(eta_GeV, lam):
    """
    Single real scalar, Z_2 symmetric, V_tree = -mu^2 phi^2/2 + lam phi^4/4
    with mu^2 = lam eta^2.
    High-T 1-loop daisy: V_T contains (lam/4) T^2 phi^2 (coefficient from
    the bosonic thermal mass for a single real d.o.f. with quartic lam).
    Symmetry restoration: lam eta^2 = (lam/4) T_c^2  =>  T_c = 2 eta.
    (Sign-independent, eta is the zero-T VEV.)
    """
    return 2.0 * eta_GeV


def z_PT(Tc_GeV_value):
    """
    Radiation era: T(z) ~ T_CMB (1+z) for z << z_eq if photons alone, but
    above e+e- annihilation entropy g*s changes. We approximate
        T(z) ~ T_CMB_0 * (g*s_0 / g*s)^{1/3} * (1+z)
    With T_CMB_0 = 2.725 K, g*s_0 = 3.91, g*s above EW ~ 106.75.
    Solve for z when T = T_c.
    """
    T0_K = 2.725
    gs0  = 3.91
    gs_high = 106.75
    Tc_K = Tc_GeV_value * GeV_to_K
    one_plus_z = (Tc_K / T0_K) * (gs_high / gs0)**(1.0/3.0)
    return one_plus_z - 1.0


# ---------------- Phase B: domain wall scaling + Zel'dovich --------------
def sigma_DW_GeV3(eta_GeV, lam):
    """
    Kink wall surface tension for V = (lam/4)(phi^2 - eta^2)^2:
        sigma = (2 sqrt(2)/3) sqrt(lam) eta^3.
    Returns in GeV^3.
    """
    return (2.0 * np.sqrt(2.0) / 3.0) * np.sqrt(lam) * eta_GeV**3


def rho_wall_today_GeV4(sigma_GeV3):
    """
    Scaling-regime wall network: average energy density
        rho_DW(t) ~ A sigma / t,  A ~ O(1).
    Take A = 1 (common simulation calibration).
    t_0 ~ 1/H0 (matter-dominated correction ~2/3 absorbed into the O(1)
    fudge of A; this is a structural estimate).
    rho_DW today (GeV^4) = sigma (GeV^3) * H0 (GeV).
    """
    H0_GeV = H0_SI * hbar / GeV_to_J   # H0 in GeV
    return sigma_GeV3 * H0_GeV


def Omega_DW(eta_GeV, lam):
    sig = sigma_DW_GeV3(eta_GeV, lam)
    rho = rho_wall_today_GeV4(sig)
    return rho / rho_crit_GeV4


# ---------------- Phase C: scan ------------------------------------------
def scan():
    eta_grid = np.logspace(-3, 18, 22)   # MeV..M_Planck in GeV
    lam_grid = [1e-2, 1e-1, 1.0]
    rows = []
    for lam in lam_grid:
        for eta in eta_grid:
            Tc  = Tc_GeV(eta, lam)
            zpt = z_PT(Tc)
            sig = sigma_DW_GeV3(eta, lam)
            Om  = Omega_DW(eta, lam)
            rows.append(dict(
                eta_GeV=float(eta),
                lam=float(lam),
                Tc_GeV=float(Tc),
                Tc_K=float(Tc * GeV_to_K),
                z_PT=float(zpt),
                sigma_DW_GeV3=float(sig),
                Omega_DW=float(Om),
                Zeldovich_pass=bool(Om < 1.0),
            ))
    return rows


def survivors(rows):
    return [r for r in rows if r["Zeldovich_pass"]]


def main():
    rows = scan()
    surv = survivors(rows)
    out = dict(
        n_total=len(rows),
        n_survivors=len(surv),
        survivors_eta_max_GeV=max([r["eta_GeV"] for r in surv]) if surv else None,
        sample=rows[::4],   # every 4th row for compactness
        first_killed_eta_at_lam1=next(
            (r["eta_GeV"] for r in rows if r["lam"] == 1.0 and not r["Zeldovich_pass"]),
            None,
        ),
        rho_crit_GeV4=rho_crit_GeV4,
    )
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(
        os.path.dirname(os.path.dirname(here)), "results", "L386"
    )
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "scan.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("L386 Z_2 SSB scan complete.")
    print("  total rows :", len(rows))
    print("  survivors  :", len(surv))
    if surv:
        eta_max = max(r["eta_GeV"] for r in surv)
        print("  max eta passing Zeldovich (GeV): %.3e" % eta_max)
    # show a couple of representative rows
    for r in rows[::6]:
        print("  lam=%.2g eta=%.2e GeV  T_c=%.2e GeV  z_PT=%.2e  Omega_DW=%.2e  pass=%s" %
              (r["lam"], r["eta_GeV"], r["Tc_GeV"], r["z_PT"],
               r["Omega_DW"], r["Zeldovich_pass"]))


if __name__ == "__main__":
    main()
