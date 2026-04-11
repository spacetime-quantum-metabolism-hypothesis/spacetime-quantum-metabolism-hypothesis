# simulations/l11/michaelis/mm_vs_erf.py
# Attempt 1: Michaelis-Menten transition curve vs A12 erf
# Rule-B 4-person code review applied

import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings('ignore')

# --- SQMH constants ---
H0 = 2.183e-18       # s^-1
sigma_sq = 4.521e-53  # m^3 kg^-1 s^-1
Omega_m = 0.315
rho_crit0 = 9.472e-27  # kg/m^3
rho_m0 = Omega_m * rho_crit0

# A12 parameters
w0_A12 = -0.886
wa_A12 = -0.133

# --- E(z) for matter+DE (LCDM baseline for rho_m) ---
def E(z, w0=-1.0, wa=0.0, Om=0.315):
    a = 1.0 / (1.0 + z)
    Ode = (1.0 - Om) * a**(-3.0*(1.0 + w0 + wa)) * np.exp(-3.0*wa*(1.0 - a))
    return np.sqrt(Om * (1+z)**3 + Ode)

# --- rho_m(z) ---
def rho_m(z):
    return rho_m0 * (1.0 + z)**3

# --- Michaelis-Menten: equilibrium n_eq ---
def n_eq_mm(z, Gamma0, sigma=sigma_sq):
    rho = rho_m(z)
    Ez = E(z)
    H_z = H0 * Ez
    return Gamma0 / (sigma * rho + 3.0 * H_z)

# --- MM dark energy EOS: w(z) from n_eq structure ---
# DE density from n_eq: rho_DE ~ n_eq * E_Planck / l_P^3 (normalization)
# w(z) derived from continuity:
# w(z) = -1 + (1/(3H)) * d(ln rho_DE)/d(ln a) ... simplified:
# Effective: w_MM(z) via MM-like ansatz
# rho_m / K_M = (rho_m * sigma) / (3H)
def w_MM(z):
    rho = rho_m(z)
    Ez = E(z)
    H_z = H0 * Ez
    K_M = 3.0 * H_z / sigma_sq  # Michaelis constant (kg/m^3)
    # MM saturation function s(z) = rho_m / (rho_m + K_M)
    s = rho / (rho + K_M)
    # w_MM = -1 + s (ranges from -1 at z->inf to 0 at z->0 where rho>>K_M)
    # Wait: K_M at z=0: K_M = 3*H0/sigma = 3*2.183e-18/4.521e-53 = 1.45e35 kg/m^3
    # rho_m0 = 2.98e-27 kg/m^3 << K_M(0) = 1.45e35 kg/m^3
    # So at z=0: s(0) = rho_m0/K_M0 ~ 2e-62 (tiny!)
    # w_MM(0) = -1 + 2e-62 ~ -1
    # At z=1e10 (matter era): rho_m >> K_M? K_M(z) = 3*H(z)/sigma
    # H(z) ~ H0 * sqrt(Om) * (1+z)^(3/2) in matter era
    # K_M(z) ~ (3*H0*sqrt(Om)/sigma) * (1+z)^(3/2)
    # rho_m(z) = rho_m0 * (1+z)^3
    # rho_m/K_M ~ (rho_m0*sigma)/(3*H0*sqrt(Om)) * (1+z)^(3/2) ~ Pi_SQMH * (1+z)^(3/2)
    # At z=0: Pi_SQMH ~ 1.8e-62 (tiny). At z~10^40: ratio ~ 1.
    # MM transition: s ~ 0.5 at z_half where rho_m = K_M.
    return -1.0 + s

# --- A12 erf-like w(z) (from paper) ---
def w_A12(z):
    return w0_A12 + wa_A12 * z / (1.0 + z)  # CPL

# --- z array ---
z_arr = np.linspace(0.0, 2.0, 200)
w_mm_arr = np.array([w_MM(z) for z in z_arr])
w_a12_arr = np.array([w_A12(z) for z in z_arr])

# --- chi^2/dof comparison ---
# Normalize: chi^2 based on A12 as "data" with 1% error bars
sigma_obs = 0.01 * np.abs(w_a12_arr)
sigma_obs = np.where(sigma_obs < 1e-4, 1e-4, sigma_obs)
chi2_mm = np.sum(((w_mm_arr - w_a12_arr) / sigma_obs)**2)
dof = len(z_arr) - 1
chi2_per_dof = chi2_mm / dof

print("=== L11 Attempt 1: Michaelis-Menten vs A12 ===")
print("w_MM(z=0): {:.6f}".format(w_MM(0.0)))
print("w_MM(z=1): {:.6f}".format(w_MM(1.0)))
print("w_A12(z=0): {:.6f}".format(w_A12(0.0)))
print("w_A12(z=1): {:.6f}".format(w_A12(1.0)))
print("K_M(z=0) [kg/m^3]: {:.3e}".format(3.0 * H0 / sigma_sq))
print("rho_m0 [kg/m^3]: {:.3e}".format(rho_m0))
print("rho_m0/K_M(z=0): {:.3e}".format(rho_m0 * sigma_sq / (3.0 * H0)))
print("")
print("chi^2/dof (MM vs A12): {:.2f}".format(chi2_per_dof))
print("Q62 threshold: chi^2/dof < 2")
print("Q62 result: FAIL (chi^2/dof >> 2)" if chi2_per_dof > 2 else "Q62 result: PASS")
print("")
print("Physical interpretation:")
print("  K_M = 3H/sigma = {:.3e} kg/m^3".format(3.0 * H0 / sigma_sq))
print("  rho_m0 << K_M: MM saturation s ~ {:.2e} (tiny)".format(
    rho_m0 * sigma_sq / (3.0 * H0 + sigma_sq * rho_m0)))
print("  w_MM ~ -1 everywhere (no z-variation at cosmological level)")
print("  MM transition occurs at rho_m ~ K_M: z_transition ~ {:.1e}".format(
    (3.0 * H0 / (sigma_sq * rho_m0))**(1.0/3.0) - 1.0
    if (3.0 * H0 / (sigma_sq * rho_m0)) > 1 else 0.0))
print("")
print("Conclusion: Q62 FAIL. MM w(z) ~ -1 identically (saturation at s~1e-62).")
print("  MM transition is cosmologically inaccessible (requires z~10^40).")
print("  The MM analogy is mathematically valid but w(z) prediction is trivial.")
