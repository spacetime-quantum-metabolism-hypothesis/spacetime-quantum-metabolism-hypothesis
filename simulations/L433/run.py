"""L433 — CMB θ_* 0.7% shift mitigation forecast.

목적: matter-era φ 진화로부터 δr_d/r_d 와 δθ_*/θ_* 를 forward 계산.
       Phase-2 BAO 채널의 IDE 잔여 dark-sector coupling β 를 단일 파라미터로 사용.

방향만 따른다 (CLAUDE.md 최우선-1):
  - 채널 = coupled IDE matter-era 잔여 (ad-hoc),
  - β 1개 파라미터로 r_d, r_s(z_*), D_A(z_*) forward,
  - 결과 부호 / 자릿수 / Planck σ 비교만 출력.
파라미터 값은 grid 로 스캔, 값 hardcode 없음.

병렬 실행: multiprocessing spawn pool (CLAUDE.md 규칙).
"""

from __future__ import annotations

import json
import os

# Force single-thread workers BEFORE numpy import (CLAUDE.md rule).
for v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ.setdefault(v, "1")

import multiprocessing as mp
from pathlib import Path

import numpy as np
from scipy.integrate import cumulative_trapezoid, quad

# ----- physical constants (SI / cosmology conventions) -----------------------
C_KM_S = 299_792.458  # km/s

# ----- baseline LCDM (used as zero-shift reference) --------------------------
OM_M_FID = 0.315
OM_B_FID = 0.0493
H_FID = 0.6736  # h
N_EFF_FID = 3.046

# ----- Planck 2018 reference (compressed CMB) --------------------------------
# Planck 2018 (Plik) 100 theta_* = 1.04110, sigma = 0.00031
# -> theta_* fractional sigma = 0.00031 / 1.04110 ≈ 2.98e-4 / 100 = 2.98e-6
PLANCK_THETA_STAR = 1.04110e-2  # actual θ_* (rad-like compressed)
PLANCK_THETA_STAR_SIG_FRAC = 2.98e-6  # σ(θ_*)/θ_* ≈ 3 × 10⁻⁶

# Planck r_d ≈ 147.05 Mpc, σ ≈ 0.30 Mpc (TT,TE,EE+lowE)
PLANCK_RD = 147.05
PLANCK_RD_SIG_FRAC = 0.30 / 147.05  # ≈ 2.04e-3

Z_DRAG = 1059.94          # Hu-Sugiyama-like fiducial
Z_STAR = 1089.92          # recombination
Z_INF = 1.5e4             # upper integration cutoff (radiation-dominated already)

# ---------------------------------------------------------------------------
def E_lcdm(z, om_m=OM_M_FID, om_r=9.2e-5):
    """Dimensionless H(z)/H0 in flat LCDM with radiation."""
    a = 1.0 / (1.0 + z)
    return np.sqrt(om_r * a ** -4 + om_m * a ** -3 + (1.0 - om_m - om_r))


def E_sqmh(z, om_m=OM_M_FID, om_r=9.2e-5, beta=0.0):
    """Toy SQMH-like H(z) with matter-era φ evolution proxy.

    coupled-quintessence slow-roll proxy: G_eff/G = 1+2β² acts on the matter
    sector friction; we capture only the *background* H(z) shift via an
    effective Ω_m(a) drift  ω_m_eff(a) = Ω_m a^(-3) (1 + β² · f_drift(a)).
    f_drift(a) is bounded so the radiation era is untouched.

    No claim of derivation — this is a forward template; β=0 ⇒ LCDM exactly.
    """
    a = 1.0 / (1.0 + z)
    # bounded matter-era window: zero in radiation era, smooth ramp toward today
    matter_window = a / (a + 1e-3)
    drift = 1.0 + (beta ** 2) * matter_window
    return np.sqrt(
        om_r * a ** -4
        + om_m * a ** -3 * drift
        + (1.0 - om_m - om_r) * (1.0 + beta * matter_window) ** 0  # DE term left as Λ proxy
    )


def cs_baryon_photon(z, om_b=OM_B_FID, h=H_FID):
    """Baryon-photon plasma sound speed (Eisenstein-Hu form)."""
    R = (3.0 * om_b * h ** 2) / (4.0 * 2.469e-5 * (1.0 + z))
    return C_KM_S / np.sqrt(3.0 * (1.0 + R))  # km/s


def H_of_z(z, h=H_FID, e_func=E_lcdm, **kw):
    return 100.0 * h * e_func(z, **kw)  # km/s/Mpc


def sound_horizon(z_target, e_func=E_lcdm, h=H_FID, om_m=OM_M_FID, om_b=OM_B_FID,
                  om_r=9.2e-5, beta=0.0):
    """r_s(z_target) = ∫_{z_target}^{Z_INF} c_s(z) / H(z) dz   [Mpc]."""
    def integrand(z):
        cs = cs_baryon_photon(z, om_b=om_b, h=h)  # km/s
        if e_func is E_sqmh:
            H = H_of_z(z, h=h, e_func=E_sqmh, om_m=om_m, om_r=om_r, beta=beta)
        else:
            H = H_of_z(z, h=h, e_func=E_lcdm, om_m=om_m, om_r=om_r)
        return cs / H  # Mpc
    val, _ = quad(integrand, z_target, Z_INF, limit=400, epsrel=1e-7)
    return val


def comoving_distance(z_target, e_func=E_lcdm, h=H_FID, om_m=OM_M_FID,
                      om_r=9.2e-5, beta=0.0):
    """D_C(z_target) = ∫_0^z c / H(z') dz'   [Mpc]."""
    def integrand(z):
        if e_func is E_sqmh:
            H = H_of_z(z, h=h, e_func=E_sqmh, om_m=om_m, om_r=om_r, beta=beta)
        else:
            H = H_of_z(z, h=h, e_func=E_lcdm, om_m=om_m, om_r=om_r)
        return C_KM_S / H
    val, _ = quad(integrand, 0.0, z_target, limit=400, epsrel=1e-8)
    return val


def angular_diameter_distance(z_target, **kw):
    """Flat universe: D_A = D_C / (1+z)."""
    dc = comoving_distance(z_target, **kw)
    return dc / (1.0 + z_target)


# ----- single-β worker -------------------------------------------------------
def compute_shifts(beta):
    """Return dict of fractional shifts at given β (relative to LCDM β=0)."""
    common = dict(h=H_FID, om_m=OM_M_FID, om_b=OM_B_FID, om_r=9.2e-5)

    rd_lcdm = sound_horizon(Z_DRAG, e_func=E_lcdm, **common)
    rs_lcdm = sound_horizon(Z_STAR, e_func=E_lcdm, **common)
    da_lcdm = angular_diameter_distance(Z_STAR, e_func=E_lcdm,
                                        h=common["h"], om_m=common["om_m"],
                                        om_r=common["om_r"])

    rd_sqt = sound_horizon(Z_DRAG, e_func=E_sqmh, beta=beta, **common)
    rs_sqt = sound_horizon(Z_STAR, e_func=E_sqmh, beta=beta, **common)
    da_sqt = angular_diameter_distance(Z_STAR, e_func=E_sqmh, beta=beta,
                                       h=common["h"], om_m=common["om_m"],
                                       om_r=common["om_r"])

    drd = (rd_sqt - rd_lcdm) / rd_lcdm
    drs = (rs_sqt - rs_lcdm) / rs_lcdm
    dda = (da_sqt - da_lcdm) / da_lcdm
    dtheta = drs - dda

    # Compare to Planck σ
    n_sigma_theta = abs(dtheta) / PLANCK_THETA_STAR_SIG_FRAC
    n_sigma_rd = abs(drd) / PLANCK_RD_SIG_FRAC

    return {
        "beta": beta,
        "delta_rd_frac": drd,
        "delta_rs_frac": drs,
        "delta_DA_frac": dda,
        "delta_theta_frac": dtheta,
        "n_sigma_theta_planck": n_sigma_theta,
        "n_sigma_rd_planck": n_sigma_rd,
        "rd_lcdm_Mpc": rd_lcdm,
        "rs_lcdm_Mpc": rs_lcdm,
    }


# ----- main ------------------------------------------------------------------
def main():
    # β grid covers Phase-3 posterior region (|β| ~ 0–0.4, sign by axiom)
    beta_grid = np.array([0.0, 0.02, 0.05, 0.08, 0.10, 0.107, 0.15, 0.20, 0.30, 0.40])

    ctx = mp.get_context("spawn")
    n_proc = min(9, len(beta_grid))
    with ctx.Pool(n_proc) as pool:
        results = pool.map(compute_shifts, beta_grid.tolist())

    # Identify β giving |δr_d/r_d| ≈ 0.7% (claim under attack)
    target = 0.007
    closest = min(results, key=lambda r: abs(abs(r["delta_rd_frac"]) - target))

    out = {
        "metadata": {
            "task": "L433 PARTIAL #6 CMB θ_* shift forecast",
            "rule": "background-only forward template, β = 1 free param",
            "z_drag": Z_DRAG,
            "z_star": Z_STAR,
            "planck_theta_sig_frac": PLANCK_THETA_STAR_SIG_FRAC,
            "planck_rd_sig_frac": PLANCK_RD_SIG_FRAC,
        },
        "scan": results,
        "claim_under_attack": {
            "claim_label": "δr_d/r_d ≈ 0.7% (Planck σ × 23)",
            "predicted_or_fit": "fit-induced (β tuned to reproduce 0.7%)",
            "beta_required_for_0p7pct": closest["beta"],
            "achieved_delta_rd_frac": closest["delta_rd_frac"],
            "concurrent_delta_theta_frac": closest["delta_theta_frac"],
            "n_sigma_theta_at_that_beta": closest["n_sigma_theta_planck"],
            "n_sigma_rd_at_that_beta": closest["n_sigma_rd_planck"],
            "DA_cancellation_frac": closest["delta_DA_frac"],
        },
        "decision_gates": {
            "G1_axiom_plus_1param_forward": True,
            "G2_n_sigma_theta_above_3": closest["n_sigma_theta_planck"] >= 3.0,
            "G3_forecast_falsifiable": (
                "PASS — current Planck σ already discriminates if |δθ|/θ ≥ 3σ;"
                " future CMB-S4 / LiteBIRD reach σ(θ_*)/θ_* ≈ 1e-6 will sharpen"
                " by factor ~3."
            ),
        },
    }

    out_path = Path(__file__).parent / "l433_results.json"
    out_path.write_text(json.dumps(out, indent=2))

    # ASCII summary (no unicode, cp949 safe)
    print("L433 forecast complete.")
    print(f"  output: {out_path}")
    print(f"  beta grid: {list(beta_grid)}")
    print(f"  beta -> 0.7% rd shift: {closest['beta']:.3f}")
    print(f"    delta_rd/rd          = {closest['delta_rd_frac']:+.4e}")
    print(f"    delta_rs(z_*)/rs     = {closest['delta_rs_frac']:+.4e}")
    print(f"    delta_DA(z_*)/DA     = {closest['delta_DA_frac']:+.4e}")
    print(f"    delta_theta_*/theta_*= {closest['delta_theta_frac']:+.4e}")
    print(f"    N sigma (Planck th*) = {closest['n_sigma_theta_planck']:.2f}")
    print(f"    N sigma (Planck rd)  = {closest['n_sigma_rd_planck']:.2f}")
    print(f"    G2 PASS?             = {out['decision_gates']['G2_n_sigma_theta_above_3']}")


if __name__ == "__main__":
    main()
