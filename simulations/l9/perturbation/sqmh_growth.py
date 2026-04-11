"""
L9 Phase A: SQMH Perturbation-Level Growth Equation
====================================================
Rule-B 4-person code review. Tag: L9-A.

Goal: Compute G_eff/G correction from SQMH sigma*n_bar*rho_m coupling
in the matter perturbation equation. Determine if correction > 1%.

Physics:
  Background: SQMH bg = LCDM (sigma*rho_m/3H ~ 1e-62, negligible)
  Perturbation: delta'' + H*delta' - 4*pi*G*rho_m*delta = SQMH correction?

  SQMH perturbation coupling: when n_bar is perturbed by delta_n,
  the production/destruction coupling produces an effective G correction:
    G_eff/G = 1 + delta_G/G

  The perturbation equation with SQMH coupling:
    dn_bar/dt + 3H*n_bar = Gamma0 - sigma*n_bar*rho_m
  When rho_m -> rho_m*(1 + delta), the steady-state n_bar shifts:
    n_bar_perturbed = Gamma0 / (3H + sigma*rho_m*(1+delta))
                    ~ n_bar* * (1 - delta * sigma*rho_m / (3H + sigma*rho_m))
                    ~ n_bar* * (1 - Pi_SQMH * delta)   [since Pi_SQMH << 1]

  The dark energy density perturbation is then:
    delta_rho_DE = mu * delta_n = -mu * n_bar* * Pi_SQMH * delta
                ~ -Pi_SQMH * rho_DE * delta

  Effective coupling in growth equation:
    delta'' + H*delta' - 4*pi*G*rho_m*(1 + G_correction)*delta = 0
  where G_correction comes from delta_rho_DE feeding back via gravity.

  For a general dark energy perturbation with sound speed c_s:
    G_eff/G = 1 + (rho_DE / rho_m) * (SQMH correction factor)

  The SQMH correction to G_eff:
    delta_G/G = - Pi_SQMH * (rho_DE / rho_m) = -(sigma*rho_m/(3H)) * (rho_DE/rho_m)
              = -sigma*rho_DE / (3H)
              ~ -sigma * (Gamma0/(3H)) / (3H)
              = -sigma * Gamma0 / (9H^2)

  At z=0:
    rho_DE ~ 3H0^2*OmegaL / (8piG)
    sigma = 4piG*t_P = 4piG / m_P*c^2 * hbar
    delta_G/G ~ sigma * rho_DE / (3H0)

NOTES:
- print() no unicode per CLAUDE.md
- numpy 2.x: use trapezoid not trapz
- forward ODE only (N_ini << 0 to 0)
- no double counting of omega_m*(1+z)^3
"""

import numpy as np
from scipy.integrate import odeint, solve_ivp
import json
import os

# ============================================================
# Physical constants (SI)
# ============================================================
G_SI = 6.674e-11        # m^3 kg^-1 s^-2
c_SI = 2.998e8          # m/s
hbar_SI = 1.055e-34     # J*s
t_P = np.sqrt(hbar_SI * G_SI / c_SI**5)  # Planck time [s]
sigma_SQMH = 4 * np.pi * G_SI * t_P      # m^3/(kg*s)

H0_kms = 67.4           # km/s/Mpc
Mpc_m = 3.0857e22       # m/Mpc
H0_SI = H0_kms * 1e3 / Mpc_m             # s^-1

Omega_m0 = 0.315
Omega_L0 = 1.0 - Omega_m0
Omega_r0 = 9.0e-5

# Critical density today
rho_crit0 = 3 * H0_SI**2 / (8 * np.pi * G_SI)  # kg/m^3
rho_m0 = Omega_m0 * rho_crit0
rho_DE0 = Omega_L0 * rho_crit0

# ============================================================
# A12 CPL parameters (best candidate from L8)
# ============================================================
w0_A12 = -0.886
wa_A12 = -0.133

# ============================================================
# LCDM background
# ============================================================
def E_lcdm(a):
    """E(a) = H(a)/H0 for LCDM."""
    return np.sqrt(Omega_r0 * a**-4 + Omega_m0 * a**-3 + Omega_L0)

def E_cpl(a, w0=w0_A12, wa=wa_A12):
    """E(a) for CPL dark energy."""
    w_de = w0 + wa * (1 - a)
    # rho_DE/rho_crit0 = Omega_L0 * exp(3*integral(1+w)dlna)
    # For CPL: rho_DE propto exp(-3*wa*(1-a)) * a^(-3*(1+w0+wa))
    f_de = Omega_L0 * a**(-3*(1+w0+wa)) * np.exp(-3*wa*(1-a))
    return np.sqrt(Omega_r0 * a**-4 + Omega_m0 * a**-3 + f_de)

# ============================================================
# Pi_SQMH: fundamental dimensionless coupling
# ============================================================
Pi_SQMH = sigma_SQMH * rho_m0 / (3 * H0_SI)
print("Pi_SQMH (fundamental scale ratio) =", Pi_SQMH)
print("sigma_SQMH =", sigma_SQMH, "m^3/(kg*s)")

# ============================================================
# G_eff/G correction at z=0
# From SQMH perturbation coupling:
#   delta_G/G = -sigma * rho_DE / (3H)
#             = -Pi_SQMH * (rho_DE/rho_m)
# ============================================================
G_correction_z0 = -Pi_SQMH * (rho_DE0 / rho_m0)
G_eff_over_G_z0 = 1.0 + G_correction_z0
print("\nG_correction at z=0 =", G_correction_z0)
print("G_eff/G at z=0 =", G_eff_over_G_z0)
print("Absolute correction (%) =", abs(G_correction_z0) * 100, "%")

# ============================================================
# Growth equation with SQMH correction
# delta'' + (2 + H'/H) * delta' - (3/2)*Omega_m(a)*delta = SQMH term
# In terms of N = ln(a):
#   delta_NN + (2 + E'/E) * delta_N - (3/2)*(Omega_m0*a^-3/E^2)*delta
#   = SQMH_correction * (3/2)*(Omega_m0*a^-3/E^2)*delta
#
# where SQMH_correction = delta_G/G = -Pi_SQMH * (rho_DE/rho_m)
#
# State: y = [delta, delta_N]
# ============================================================

def growth_rhs_lcdm(N, y):
    """Growth equation for LCDM."""
    a = np.exp(N)
    E = E_lcdm(a)
    dE_da = (-2*Omega_r0*a**-5 - 3*Omega_m0*a**-4) / (2*E) * a  # dE/dN = a*dE/da
    dE_dN = a * (-2*Omega_r0*a**-5 - 3*Omega_m0*a**-4) / (2*E)

    Om_eff = Omega_m0 * a**-3 / E**2
    coeff = 2 + dE_dN / E

    delta, delta_N = y
    delta_NN = -(coeff) * delta_N + 1.5 * Om_eff * delta
    return [delta_N, delta_NN]

def growth_rhs_sqmh(N, y, G_eff_func):
    """Growth equation with SQMH G_eff/G correction."""
    a = np.exp(N)
    E = E_lcdm(a)  # background = LCDM (sigma bg correction is 1e-62)
    dE_dN = a * (-2*Omega_r0*a**-5 - 3*Omega_m0*a**-4) / (2*E)

    Om_eff = Omega_m0 * a**-3 / E**2
    coeff = 2 + dE_dN / E

    # SQMH G_eff correction
    G_eff_ratio = G_eff_func(a)
    delta, delta_N = y
    delta_NN = -(coeff) * delta_N + 1.5 * Om_eff * G_eff_ratio * delta
    return [delta_N, delta_NN]

def G_eff_sqmh(a):
    """
    G_eff/G from SQMH perturbation coupling.
    delta_G/G = -sigma * rho_DE(a) / (3*H(a))
              = -Pi_SQMH * (Omega_L0 / Omega_m0) * a^3  [for LCDM approx]
    More precisely: rho_DE/rho_m = Omega_L0*a^3 / Omega_m0 (LCDM)
    """
    rho_DE_ratio = Omega_L0 / Omega_m0 * a**3  # rho_DE / rho_m at scale factor a
    delta_G_over_G = -Pi_SQMH * rho_DE_ratio
    return 1.0 + delta_G_over_G

def G_eff_A12_like(a):
    """
    A heuristic G_eff correction for CPL-like models.
    For phenomenological context only -- NOT a derivation.
    Assume G_eff/G = 1 + mu_0*(1 - Omega_m(a)) where mu_0 ~ 0.01.
    This tests if a 1% modification at the right redshift can mimic A12.
    """
    E = E_cpl(a)
    Om_a = Omega_m0 * a**-3 / E**2
    # mu_0 chosen to give ~1% effect at z=0
    mu_0 = 0.01
    return 1.0 + mu_0 * (1.0 - Om_a)

# ============================================================
# Integrate growth equations: forward in N from matter era
# ============================================================
N_ini = -7.0   # z ~ 1096 (recombination era), safe from blow-up
N_end = 0.0    # today
N_arr = np.linspace(N_ini, N_end, 2000)

# Initial conditions: matter-dominated D ~ a, f ~ 1
delta_ini = np.exp(N_ini)
delta_N_ini = np.exp(N_ini)  # d/dN(delta) = delta (matter era)

y0 = [delta_ini, delta_N_ini]

# Integrate LCDM
sol_lcdm = solve_ivp(growth_rhs_lcdm, [N_ini, N_end], y0,
                     t_eval=N_arr, method='RK45', rtol=1e-8, atol=1e-10)

# Integrate SQMH
sol_sqmh = solve_ivp(
    lambda N, y: growth_rhs_sqmh(N, y, G_eff_sqmh),
    [N_ini, N_end], y0,
    t_eval=N_arr, method='RK45', rtol=1e-8, atol=1e-10
)

# Check solutions
D_lcdm = sol_lcdm.y[0].copy()
D_sqmh = sol_sqmh.y[0].copy()
dD_lcdm = sol_lcdm.y[1].copy()
dD_sqmh = sol_sqmh.y[1].copy()

# Normalize to today (use raw values for f calculation)
D_lcdm_today = D_lcdm[-1]
D_sqmh_today = D_sqmh[-1]

# Growth rate f = dlnD/dlnN (use raw unnormalized delta)
f_lcdm = dD_lcdm / D_lcdm
f_sqmh = dD_sqmh / D_sqmh

# Check finiteness
assert np.all(np.isfinite(D_lcdm)), "LCDM D not finite"
assert np.all(np.isfinite(D_sqmh)), "SQMH D not finite"
assert D_lcdm_today > 0, "LCDM D_today must be positive"
assert D_sqmh_today > 0, "SQMH D_today must be positive"

# Normalized growth functions
D_lcdm_norm = D_lcdm / D_lcdm_today
D_sqmh_norm = D_sqmh / D_sqmh_today

print("\n--- Growth Function Comparison ---")
print("f_lcdm at z=0:", f_lcdm[-1])
print("f_sqmh at z=0:", f_sqmh[-1])
print("Delta_f (f_sqmh - f_lcdm) at z=0:", f_sqmh[-1] - f_lcdm[-1])
print("Fractional change in f (%):", (f_sqmh[-1] - f_lcdm[-1]) / f_lcdm[-1] * 100)

# ============================================================
# sigma8 proxy (proportional to D_today in same normalization)
# sigma8_ratio = D_sqmh_today / D_lcdm_today (both use same N_ini)
# ============================================================
sigma8_ratio = D_sqmh_today / D_lcdm_today
S8_lcdm = 0.834  # Planck S8 (LCDM)
S8_sqmh = S8_lcdm * sigma8_ratio  # SQMH prediction (rough proxy)

print("\n--- sigma8 and S8 ---")
print("sigma8_ratio (SQMH/LCDM):", sigma8_ratio)
print("S8_LCDM (input):", S8_lcdm)
print("S8_SQMH (proxy):", S8_sqmh)
print("Delta_S8 (SQMH - LCDM):", S8_sqmh - S8_lcdm)

# ============================================================
# G_eff/G profile across redshift
# ============================================================
a_arr = np.exp(N_arr)
G_eff_arr = np.array([G_eff_sqmh(a) for a in a_arr])
z_arr = 1.0/a_arr - 1.0

print("\n--- G_eff/G profile ---")
idx_z0 = -1
idx_z1 = np.argmin(np.abs(z_arr - 1.0))
idx_z2 = np.argmin(np.abs(z_arr - 2.0))

print("G_eff/G at z=0:", G_eff_arr[idx_z0])
print("G_eff/G at z=1:", G_eff_arr[idx_z1])
print("G_eff/G at z=2:", G_eff_arr[idx_z2])
print("Max deviation from 1:", np.max(np.abs(G_eff_arr - 1.0)))
print("Max deviation from 1 (%):", np.max(np.abs(G_eff_arr - 1.0)) * 100, "%")

# ============================================================
# Q41 Judgment
# ============================================================
max_G_correction_pct = np.max(np.abs(G_eff_arr - 1.0)) * 100
Q41_threshold = 1.0  # percent

Q41_pass = max_G_correction_pct > Q41_threshold
print("\n--- Q41 Judgment ---")
print("Q41 threshold: G_eff/G correction > 1%")
print("Max correction:", max_G_correction_pct, "%")
print("Q41 PASS:", Q41_pass)

if not Q41_pass:
    print("Q41 FAIL: G_eff/G correction =", max_G_correction_pct, "% << 1%")
    print("Reason: Pi_SQMH =", Pi_SQMH, "(62-order suppression persists at perturbation level)")
    print("K41 condition met: perturbation-level SQMH also fails to produce wa<0 structure")

# ============================================================
# Analytical understanding: why G_eff correction is suppressed
# ============================================================
print("\n--- Analytical structure ---")
print("Pi_SQMH = sigma*rho_m0/(3H0) =", Pi_SQMH)
print("rho_DE/rho_m at z=0 =", Omega_L0/Omega_m0)
print("Max G_correction = Pi_SQMH * max(rho_DE/rho_m) =",
      Pi_SQMH * (Omega_L0 / Omega_m0) * 1.0, "(z=0, a=1)")
print("This is still ~1e-62 suppressed -- identical suppression at bg AND perturbation levels")

# ============================================================
# A12 CPL growth comparison
# ============================================================
def growth_rhs_cpl(N, y):
    """Growth equation for A12 CPL model."""
    a = np.exp(N)
    E = E_cpl(a)
    # dE/dN for CPL (numerical)
    da = a * 1e-5
    dE_dN = a * (E_cpl(a + da) - E_cpl(a - da)) / (2*da)

    Om_eff = Omega_m0 * a**-3 / E**2
    coeff = 2 + dE_dN / E

    delta, delta_N = y
    delta_NN = -(coeff) * delta_N + 1.5 * Om_eff * delta
    return [delta_N, delta_NN]

sol_cpl = solve_ivp(growth_rhs_cpl, [N_ini, N_end], y0,
                    t_eval=N_arr, method='RK45', rtol=1e-8, atol=1e-10)
D_cpl = sol_cpl.y[0].copy()
D_cpl_today = D_cpl[-1]
sigma8_cpl_ratio = D_cpl_today / D_lcdm_today
S8_cpl = S8_lcdm * sigma8_cpl_ratio

print("\n--- A12 CPL Growth Comparison ---")
print("sigma8_ratio (A12 CPL/LCDM):", sigma8_cpl_ratio)
print("S8_A12_proxy:", S8_cpl)
print("Delta_S8 (A12 CPL vs LCDM):", S8_cpl - S8_lcdm)
print("f_CPL at z=0:", sol_cpl.y[1][-1] / D_cpl[-1])

# ============================================================
# Save results
# ============================================================
results = {
    "Pi_SQMH": float(Pi_SQMH),
    "sigma_SQMH": float(sigma_SQMH),
    "G_correction_z0_pct": float(G_correction_z0 * 100),
    "max_G_correction_pct": float(max_G_correction_pct),
    "Q41_pass": bool(Q41_pass),
    "Q41_threshold_pct": float(Q41_threshold),
    "f_lcdm_z0": float(f_lcdm[-1]),
    "f_sqmh_z0": float(f_sqmh[-1]),
    "sigma8_ratio_sqmh_lcdm": float(sigma8_ratio),
    "sigma8_ratio_cpl_lcdm": float(sigma8_cpl_ratio),
    "S8_lcdm": float(S8_lcdm),
    "S8_sqmh_proxy": float(S8_sqmh),
    "S8_cpl_proxy": float(S8_cpl),
    "Delta_S8_sqmh": float(S8_sqmh - S8_lcdm),
    "Delta_S8_cpl": float(S8_cpl - S8_lcdm),
    "verdict": "K41_met" if not Q41_pass else "Q41_pass",
    "note": "Pi_SQMH suppression persists at perturbation level. G_eff/G - 1 ~ 1e-62. K41 condition met."
}

out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, "sqmh_growth_results.json")
with open(out_path, "w") as f:
    json.dump(results, f, indent=2)

print("\nResults saved to", out_path)
print("\n=== L9-A COMPLETE ===")
