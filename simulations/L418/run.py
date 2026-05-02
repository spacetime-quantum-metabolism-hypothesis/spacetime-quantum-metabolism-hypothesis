"""L418 simulation — mu-distortion quantitative derivation + foreground separation.

Mandate (from base.l418 command):
  Q1. Sink rate Q from sigma_0, n_inf, epsilon (dimensions only — no smuggled inputs).
  Q2. LCDM baseline mu in mu-window (z ~ 5e4 .. 2e6) for context (Chluba 2016 reference).
  Q3. SNR vs PIXIE noise (sigma_mu ~ 1e-9), 1.02e-8 target.
  Q4. Foreground residual (galactic dust + CIB monopole, ILC residual ~5e-9 assumption).
  Q5. y/mu ratio — is it fixed by SQT axioms or free?

Honesty:
  - The number 1.02e-8 in base.md sec 4.3 is a *target line*. The paper body
    contains no derivation. This script does NOT manufacture a derivation;
    it (a) recomputes the standard adiabatic Silk-damping baseline at order-of-magnitude,
    (b) shows the SNR arithmetic for the announced value, (c) checks foreground-limited
    detectability, and (d) flags y/mu as a *free* axis unless SQT closes it.
  - Per CLAUDE.md sim rules: ASCII-only print, np.trapezoid, parallel-ready (spawn).

Run:
    python3 simulations/L418/run.py
"""

from __future__ import annotations

import os

# Force single-threaded BLAS per CLAUDE.md rule.
for _k in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ.setdefault(_k, "1")

import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np

# ------------------------------------------------------------------
# Constants (SI)
# ------------------------------------------------------------------
C_LIGHT = 2.99792458e8           # m / s
H_BAR = 1.054571817e-34          # J s
K_BOLTZ = 1.380649e-23           # J / K
G_NEWTON = 6.67430e-11           # m^3 kg^-1 s^-2
T_PLANCK = math.sqrt(H_BAR * G_NEWTON / C_LIGHT**5)        # ~5.39e-44 s
M_PLANCK_KG = math.sqrt(H_BAR * C_LIGHT / G_NEWTON)        # kg
RHO_PLANCK = C_LIGHT**5 / (H_BAR * G_NEWTON**2)            # kg/m^3
MPC = 3.0857e22                                            # m
H0_PER_S = 67.4 * 1000.0 / MPC                             # Planck 2018 ~ 2.18e-18 /s
T_CMB = 2.7255                                             # K
# CMB photon energy density today (rho_gamma c^2 in J/m^3) via radiation constant.
A_RAD = 7.5657e-16               # J m^-3 K^-4 (radiation constant 4 sigma_SB / c)
RHO_GAMMA_J_PER_M3 = A_RAD * T_CMB**4
OMEGA_LAMBDA = 0.6847            # Planck 2018
RHO_CRIT_TODAY = 3.0 * H0_PER_S**2 * C_LIGHT**2 / (8 * math.pi * G_NEWTON)  # J/m^3
RHO_LAMBDA_J_PER_M3 = OMEGA_LAMBDA * RHO_CRIT_TODAY        # ~5e-10 J/m^3

# ------------------------------------------------------------------
# SQT canonical inputs (per base.md derived 1..5; CLAUDE.md notes).
# sigma_0 = 4 pi G t_P  (SI), n0*mu = rho_Planck/(4 pi)  (only product is physical)
# epsilon = hbar / tau_q,   tau_q ~ 1/(3 H0)   (paper sec 5.1 default)
# ------------------------------------------------------------------
SIGMA_0 = 4.0 * math.pi * G_NEWTON * T_PLANCK             # m^3 kg^-1 s^-1
N0_TIMES_MU = RHO_PLANCK / (4.0 * math.pi)                # kg / m^3
TAU_Q = 1.0 / (3.0 * H0_PER_S)                            # s, ~ 1/(3 H0)
EPS_Q = H_BAR / TAU_Q                                     # J


def banner(title: str) -> None:
    bar = "=" * len(title)
    print(bar)
    print(title)
    print(bar)


# ------------------------------------------------------------------
# Q1. Sink rate Q from (sigma_0, n_inf, epsilon).
#    n_inf is fixed by axiom-3 balance using rho_Lambda_obs (sec 5.2 circularity).
#    Q has dimensions of energy / volume / time.
# ------------------------------------------------------------------
def q1_sink_rate() -> dict:
    # n_inf * epsilon = rho_Lambda * c^2  (paper sec 5.2: rho_q = n eps / c^2)
    # so n_inf = rho_Lambda c^2 / eps_q.
    n_inf = RHO_LAMBDA_J_PER_M3 / EPS_Q                   # 1 / m^3 (number density of "spacetime quanta")
    # Sink rate per volume: dimensionally [sigma_0 (m3/kg/s)] x [N0 mu (kg/m3)] x [n_inf (1/m3)] x [eps_q (J)]
    # gives J/m^3/s — energy density absorbed per unit time.  Scaling form only.
    Q_dot = SIGMA_0 * N0_TIMES_MU * n_inf * EPS_Q          # J m^-3 s^-1
    # Compare to H_0 * rho_Lambda_obs  (canonical expectation).
    H0_rhoL = H0_PER_S * RHO_LAMBDA_J_PER_M3
    return {
        "sigma_0_SI": SIGMA_0,
        "n0_mu_SI": N0_TIMES_MU,
        "tau_q_s": TAU_Q,
        "eps_q_J": EPS_Q,
        "n_inf_per_m3": n_inf,
        "Q_dot_J_per_m3_per_s": Q_dot,
        "H0_x_rhoLambda": H0_rhoL,
        "ratio_Q_to_H0rhoL": Q_dot / H0_rhoL,
        "note": (
            "n_inf uses rho_Lambda_obs as input (sec 5.2 circularity). "
            "Q is dimensionally a rate but is *not* a photon-channel rate — "
            "axiom does not specify whether sink couples to em sector."
        ),
    }


# ------------------------------------------------------------------
# Q2. LCDM mu baseline from adiabatic Silk damping (order-of-magnitude).
#    Standard reference: Chluba 2016 — adiabatic dissipation ~ 2e-8 in mu-window.
#    We do NOT re-derive (requires full transfer function); we cite + sanity-check
#    via the dimensionless energy-injection-fraction integral
#       mu ~ 1.4 * Integral_{z_mu_min}^{z_mu_max} dz (1/(1+z)) * d(Q/rho_gamma)/dz
#    using a power-law toy d(Q/rho_gamma)/dz ~ const for visualisation only.
# ------------------------------------------------------------------
def q2_lcdm_baseline() -> dict:
    # mu-window edges (Sunyaev-Zeldovich / Hu-Silk).
    z_mu_min = 5.0e4
    z_mu_max = 2.0e6
    # Reference value (Chluba 2016 Table 1 adiabatic): ~ 2.0e-8.
    mu_silk_reference = 2.0e-8
    # Toy "shape" integral used only to visualise window weighting (no claim).
    z_grid = np.linspace(z_mu_min, z_mu_max, 4000)
    weight = 1.0 / (1.0 + z_grid)
    norm = np.trapezoid(weight, z_grid)
    return {
        "z_mu_min": z_mu_min,
        "z_mu_max": z_mu_max,
        "mu_silk_reference_chluba2016": mu_silk_reference,
        "window_weight_integral": float(norm),
        "note": "Reference value cited from Chluba 2016; not re-derived here.",
    }


# ------------------------------------------------------------------
# Q3. SNR for the announced 1.02e-8 against PIXIE-class noise.
#    Two interpretations:
#      (a) SQT *additional* mu on top of LCDM ~2e-8 baseline,
#      (b) SQT *total* mu = 1.02e-8 (then less than LCDM baseline -> sign-flip).
# ------------------------------------------------------------------
def q3_snr() -> dict:
    mu_target = 1.02e-8
    sigma_pixie = 1.0e-9            # PIXIE-class noise
    sigma_voyage2050 = 1.0e-10      # next-gen
    return {
        "mu_target_announced": mu_target,
        "pixie_noise_sigma_mu": sigma_pixie,
        "snr_pixie_total_interp": mu_target / sigma_pixie,                          # 10.2 sigma
        "snr_pixie_additional_interp": (mu_target) / sigma_pixie,                   # same arithmetic
        "snr_voyage2050": mu_target / sigma_voyage2050,
        "lcdm_baseline_chluba2016": 2.0e-8,
        "interpretation_warning": (
            "If 1.02e-8 is the SQT *total*, it is BELOW the LCDM Silk-damping "
            "baseline (~2e-8) — implying a *negative* deviation. Sign of the "
            "falsifier is then opposite to what base.md sec 4.3 states. If it "
            "is *additional* on top of LCDM, total ~3e-8, still detectable, "
            "but base.md sec 4.3 does not specify which interpretation."
        ),
    }


# ------------------------------------------------------------------
# Q4. Foreground residual analysis.
#    Galactic dust monopole at 200-800 GHz can mimic mu signal. Rough
#    component-separation residuals reported in PIXIE/PRISM literature:
#      ILC (no priors) residual ~ 5e-9 in mu;
#      MILCA / NILC w/ multi-frequency ~ 1e-9 (best case).
# ------------------------------------------------------------------
def q4_foreground() -> dict:
    mu_target = 1.02e-8
    fg_resid_ilc = 5.0e-9
    fg_resid_best = 1.0e-9
    return {
        "mu_target": mu_target,
        "foreground_residual_ILC": fg_resid_ilc,
        "foreground_residual_best_case": fg_resid_best,
        "snr_after_ILC": mu_target / fg_resid_ilc,
        "snr_after_best_separation": mu_target / fg_resid_best,
        "base_md_quoted_2sigma_vs_foreground": True,
        "note": (
            "base.md sec 4.3 quotes 'foreground 2 sigma' which corresponds to "
            "ILC-class separation (mu/5e-9 ~ 2). Best-case multi-component "
            "separation gives ~10 sigma but is observatory-dependent."
        ),
    }


# ------------------------------------------------------------------
# Q5. y vs mu branching — is it fixed by SQT axioms?
#    Standard photon Boltzmann: epoch z > 2e6 -> thermalised (no distortion);
#    5e4 < z < 2e6 -> mu-type; z < 5e4 -> y-type.
#    SQT axiom set (1-6) does NOT specify *when* the sink Q couples to photons.
#    Therefore the y/mu branching ratio is a *free* axis in the current paper.
# ------------------------------------------------------------------
def q5_y_over_mu() -> dict:
    return {
        "y_over_mu_axiom_fixed": False,
        "y_over_mu_value": float("nan"),
        "reason": (
            "Branching depends on epoch of energy injection, which the SQT "
            "axioms (1-6) do not specify. Without a *time profile* of Q(z), "
            "y/mu is not predicted. Adding such a profile = extra input -> "
            "PASS_STRONG forfeit (PASS_IDENTITY at best)."
        ),
    }


# ------------------------------------------------------------------
# Verdict aggregation.
# ------------------------------------------------------------------
def verdict(results: dict) -> dict:
    v = {}
    # A1 derivation closure.
    v["A1_derivation_closed_under_sigma0_ninf_eps"] = False  # n_inf needs rho_Lambda_obs.
    # A2 PASS_IDENTITY risk.
    v["A2_pass_identity_risk"] = True
    # A3 Lambda circularity inheritance.
    v["A3_lambda_circularity_inherited"] = True              # via n_inf.
    # A4/A8 sign and baseline.
    v["A4_sign_ambiguity_total_vs_additional"] = True
    # A5 photon-channel coupling specified by axiom.
    v["A5_photon_channel_specified"] = False
    # A6 foreground separation feasibility.
    v["A6_foreground_separation_marginal_at_ILC"] = True
    # A7 PIXIE confirmed mission?
    v["A7_pixie_flight_confirmed"] = False  # PIXIE never approved; PRISM/BISOU candidates.
    # Final.
    closed = (
        not v["A3_lambda_circularity_inherited"]
        and v["A1_derivation_closed_under_sigma0_ninf_eps"]
        and v["A5_photon_channel_specified"]
        and not v["A4_sign_ambiguity_total_vs_additional"]
    )
    v["overall_pass_strong_eligible"] = closed
    v["recommended_status"] = (
        "PENDING (PASS_IDENTITY risk + Lambda circularity + photon-channel unspecified)"
    )
    return v


def main() -> None:
    out = Path(__file__).parent / "results.json"
    banner("L418 — mu-distortion quantitative derivation")
    print(f"sigma_0 [m3/kg/s]   = {SIGMA_0:.6e}")
    print(f"n0*mu   [kg/m3]     = {N0_TIMES_MU:.6e}")
    print(f"tau_q   [s]         = {TAU_Q:.6e}")
    print(f"eps_q   [J]         = {EPS_Q:.6e}")
    print(f"rho_Lambda [J/m3]   = {RHO_LAMBDA_J_PER_M3:.6e}")
    print()

    q1 = q1_sink_rate();    print("[Q1]", json.dumps(q1, indent=2))
    q2 = q2_lcdm_baseline();print("[Q2]", json.dumps(q2, indent=2))
    q3 = q3_snr();          print("[Q3]", json.dumps(q3, indent=2))
    q4 = q4_foreground();   print("[Q4]", json.dumps(q4, indent=2))
    q5 = q5_y_over_mu();    print("[Q5]", json.dumps(q5, indent=2))

    results = {"Q1": q1, "Q2": q2, "Q3": q3, "Q4": q4, "Q5": q5}
    results["verdict"] = verdict(results)

    banner("VERDICT")
    print(json.dumps(results["verdict"], indent=2))

    out.write_text(json.dumps(results, indent=2))
    print(f"\nresults written to: {out}")


if __name__ == "__main__":
    main()
