"""L385 — Holographic n-field upper bound numerical comparison.

Compares SQT asymptotic n_inf against the Cohen-Kaplan-Nelson holographic
upper bound n_max on the number/energy density of effective DOF inside a
causal region of size L. Headline output: saturation ratio r = n_inf / n_max.

Conventions:
- SI units throughout.
- CKN bound: requiring that the IR cutoff L and UV cutoff Lambda satisfy
  L^3 Lambda^4 <= L M_P^2 (no black-hole formation), giving a maximum
  vacuum energy density rho_max(L) = (3/(8 pi)) M_P^2 / L^2 in the
  conventional Friedmann normalisation. The implied number density of
  Planck-energy quanta is n_max(L) = rho_max(L) / (M_P c^2).
- SQT n_inf: asymptotic spacetime quantum number density at the de Sitter
  horizon, n_inf = rho_Lambda_obs / (M_P c^2), where rho_Lambda_obs is the
  measured cosmological constant energy density. Derivation rule: SQT team
  produces this independently; here we use the observational value as a
  stand-in proxy for the team's asymptotic-limit prediction (saturation
  test, not fit).
"""

from __future__ import annotations

import json
import math
import os
from pathlib import Path

# CODATA 2018
C = 2.99792458e8           # m/s
HBAR = 1.054571817e-34     # J s
G = 6.67430e-11            # m^3 kg^-1 s^-2
MPC = 3.0856775814913673e22  # m
KM = 1.0e3

H0_KMS_MPC = 67.4
H0 = H0_KMS_MPC * KM / MPC  # s^-1

# Planck units
L_P = math.sqrt(HBAR * G / C**3)
T_P = math.sqrt(HBAR * G / C**5)
M_P = math.sqrt(HBAR * C / G)
E_P = M_P * C**2
RHO_P = C**5 / (HBAR * G**2)  # Planck energy density [J/m^3]

# Hubble radius
R_H = C / H0  # m

# Observed Lambda energy density (Omega_Lambda ~ 0.685, rho_crit = 3 H0^2 / 8 pi G)
RHO_CRIT = 3.0 * H0**2 / (8.0 * math.pi * G)  # kg/m^3
RHO_LAMBDA_KG = 0.685 * RHO_CRIT             # kg/m^3
RHO_LAMBDA = RHO_LAMBDA_KG * C**2            # J/m^3


def n_max_ckn(L: float) -> float:
    """CKN holographic upper bound on number density of Planck quanta.

    rho_max(L) = (3 / 8 pi) (M_P c^2)^2 / (L^2 hbar c^3) -- equivalent
    expression in SI; returns n_max in m^-3.
    """
    # CKN energy-density bound (SI): rho_max(L) <= 3 c^4 / (8 pi G L^2).
    # This is the Schwarzschild closure condition E <= L c^4/(2G) divided by
    # the volume (4/3) pi L^3, with the conventional 3/(8 pi) factor.
    rho_max_J = 3.0 * C**4 / (8.0 * math.pi * G * L**2)
    return rho_max_J / E_P  # Planck quanta per m^3


def n_inf_sqt() -> float:
    """SQT asymptotic n at de Sitter horizon (proxy: observed Lambda)."""
    return RHO_LAMBDA / E_P


def run() -> dict:
    scales = {
        "lab_1m": 1.0,
        "AU": 1.495978707e11,
        "kpc": 1.0e3 * MPC * 1e-3,  # = 1 kpc
        "Mpc": MPC,
        "Gpc": 1.0e3 * MPC,
        "Hubble": R_H,
    }

    n_inf = n_inf_sqt()

    rows = []
    for name, L in scales.items():
        nmax = n_max_ckn(L)
        ratio = n_inf / nmax
        rows.append({
            "scale": name,
            "L_m": L,
            "n_max_per_m3": nmax,
            "n_inf_per_m3": n_inf,
            "ratio_n_inf_over_n_max": ratio,
            "log10_ratio": math.log10(ratio) if ratio > 0 else float("nan"),
        })

    # CKN scaling check: log d(ln n_max)/d(ln L) ~ -2
    L1, L2 = 1.0, R_H
    slope = math.log(n_max_ckn(L2) / n_max_ckn(L1)) / math.log(L2 / L1)

    summary = {
        "constants": {
            "c": C, "hbar": HBAR, "G": G, "H0_s_inv": H0,
            "l_Planck_m": L_P, "t_Planck_s": T_P, "M_Planck_kg": M_P,
            "rho_Planck_J_per_m3": RHO_P,
        },
        "rho_Lambda_obs_J_per_m3": RHO_LAMBDA,
        "n_inf_per_m3": n_inf,
        "Hubble_radius_m": R_H,
        "ckn_log_slope_dlnnmax_dlnL": slope,
        "rows": rows,
        "headline": {
            "scale": "Hubble",
            "L_m": R_H,
            "n_max_per_m3": n_max_ckn(R_H),
            "n_inf_per_m3": n_inf,
            "ratio": n_inf / n_max_ckn(R_H),
            "log10_ratio": math.log10(n_inf / n_max_ckn(R_H)),
        },
    }

    out_dir = Path(__file__).resolve().parent.parent.parent / "results" / "L385"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("L385 holographic saturation summary")
    print(f"  H0          = {H0:.3e} s^-1")
    print(f"  R_H         = {R_H:.3e} m")
    print(f"  rho_Lambda  = {RHO_LAMBDA:.3e} J/m^3")
    print(f"  n_inf (SQT) = {n_inf:.3e} m^-3")
    print(f"  CKN slope d ln n_max / d ln L = {slope:.3f}  (expected -2)")
    print()
    print(f"  {'scale':10s} {'L [m]':>12s} {'n_max':>14s} {'n_inf/n_max':>14s} {'log10 r':>8s}")
    for r in rows:
        print(f"  {r['scale']:10s} {r['L_m']:>12.3e} {r['n_max_per_m3']:>14.3e}"
              f" {r['ratio_n_inf_over_n_max']:>14.3e} {r['log10_ratio']:>8.3f}")
    print()
    h = summary["headline"]
    print(f"HEADLINE r(R_H) = n_inf / n_max = {h['ratio']:.3e}"
          f"  (log10 = {h['log10_ratio']:.3f})")
    print(f"results -> {out_path}")
    return summary


if __name__ == "__main__":
    run()
