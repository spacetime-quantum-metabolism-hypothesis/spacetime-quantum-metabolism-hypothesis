# simulations/l11/void_bias/rhode_void_bias.py
# Attempt 15: Zero-inflated Poisson -> rho_DE void bias
# PRIORITY ATTEMPT -- direct DESI void catalog connection
# Rule-B 4-person review

import numpy as np
from scipy.integrate import trapezoid
import warnings
warnings.filterwarnings('ignore')

# --- Constants ---
H0 = 2.183e-18
sigma_sq = 4.521e-53
Omega_m = 0.315
rho_crit0 = 9.472e-27
rho_m0 = Omega_m * rho_crit0
rho_DE0 = (1.0 - Omega_m) * rho_crit0
t_P = 5.391e-44
c = 3e8

print("=== L11 Attempt 15: Void Bias -> rho_DE Spatial Inhomogeneity ===")
print("  [PRIORITY ATTEMPT - DESI Void Catalog Connection]")
print("")

# --- SQMH n_eq in void vs filament ---
# Void: delta_m = -0.8 -> rho_m_void = rho_m0 * (1 - 0.8) = 0.2 * rho_m0
# Filament: delta_m = +3 -> rho_m_fil = rho_m0 * (1 + 3) = 4 * rho_m0
# Cluster: delta_m = +200 -> rho_m_clust = 201 * rho_m0

def n_eq_env(delta_m, z=0.0, sigma=sigma_sq):
    """n_eq in given environment with matter overdensity delta_m."""
    rho_m_local = rho_m0 * (1+z)**3 * (1.0 + delta_m)
    H_z = H0 * np.sqrt(Omega_m * (1+z)**3 + (1-Omega_m))
    # Gamma_0 is spatially uniform (it's a background creation rate)
    # n_eq = Gamma_0 / (sigma*rho_m_local + 3H)
    # Normalized to background: n_eq = n_eq_background * mu_bg / mu_local
    mu_bg = sigma * rho_m0 * (1+z)**3 + 3.0 * H_z
    mu_local = sigma * rho_m_local + 3.0 * H_z
    return mu_bg / mu_local  # normalized to background n_eq = 1

print("n_eq in different environments (normalized to background):")
print("{:<20} {:<15} {:<15} {:<20}".format(
    "Environment", "delta_m", "rho_m/rho_m0", "n_eq (norm.)"))
print("-" * 75)

environments = [
    ("Deep void", -0.9, -0.9),
    ("Moderate void", -0.6, -0.6),
    ("Void wall", -0.3, -0.3),
    ("Background", 0.0, 0.0),
    ("Sheet/filament", 1.0, 1.0),
    ("Dense filament", 5.0, 5.0),
    ("Group", 20.0, 20.0),
    ("Cluster core", 200.0, 200.0),
]

n_eq_values = {}
for name, delta_m, delta in environments:
    n = n_eq_env(delta_m)
    n_eq_values[name] = n
    print("{:<20} {:<15.2f} {:<15.2f} {:<20.6f}".format(
        name, delta_m, 1.0 + delta_m, n))

print("")

# --- rho_DE bias ---
print("rho_DE spatial distribution (relative to background):")
print("  rho_DE(void) / rho_DE(background) ~ n_eq(void) / n_eq(bg)")
print("")

# Physical mechanism:
# In voids: rho_m -> 0, so n_eq -> Gamma_0/(3H) (maximum)
# In clusters: rho_m large, so n_eq -> Gamma_0/(sigma*rho_m) < Gamma_0/(3H)
# -> rho_DE is HIGHER in voids and LOWER in clusters

delta_m_scan = np.linspace(-0.95, 500.0, 1000)
n_eq_scan = np.array([n_eq_env(dm) for dm in delta_m_scan])

print("rho_DE enhancement in deep voids vs cluster cores:")
print("  Deep void (delta_m = -0.9): n_eq = {:.6f}".format(n_eq_env(-0.9)))
print("  Cluster core (delta_m = 200): n_eq = {:.6e}".format(n_eq_env(200.0)))
print("")

# Fractional rho_DE difference between void and mean:
delta_rho_DE_void = (n_eq_env(-0.8) - 1.0)
print("Fractional rho_DE excess in void (delta_m = -0.8):")
print("  delta_rho_DE / rho_DE = {:.8f}".format(delta_rho_DE_void))
print("  = {:.4e}".format(delta_rho_DE_void))
print("")

# Physical explanation:
# sigma * rho_m0 / (3H0) = Pi_SQMH ~ 1.8e-62 (tiny)
# So n_eq(delta_m) ~ 1 + sigma*rho_m0*delta_m / (3H) (linear approx)
# -> delta_n_eq / n_eq ~ Pi_SQMH * delta_m
# For delta_m = -0.8 (deep void):
Pi_SQMH = sigma_sq * rho_m0 / (3.0 * H0)
delta_n_linear = -Pi_SQMH * (-0.8)  # positive in void
print("Linear approximation: delta_n/n ~ Pi_SQMH * delta_m")
print("  Pi_SQMH = sigma*rho_m0/(3H0) = {:.4e}".format(Pi_SQMH))
print("  delta_rho_DE/rho_DE (void, delta_m=-0.8) ~ Pi_SQMH * 0.8 = {:.4e}".format(
    Pi_SQMH * 0.8))
print("")

# Observational implications:
# DESI void catalog: can measure delta_rho_DE in voids from lensing
# Required precision: delta_rho_DE/rho_DE ~ 10^-62 (SQMH void bias)
print("DESI Void Catalog observational requirements:")
print("  Predicted rho_DE void bias (SQMH): {:.4e}".format(Pi_SQMH * 0.8))
print("  Current observational precision: ~ 10^-2 (1% level)")
print("  Required improvement: {:.0f} orders of magnitude".format(
    np.log10(1e-2 / (Pi_SQMH * 0.8))))
print("")

# But wait: is the bias at void WALLS (void-cluster interface) detectable?
# At void wall (delta_m ~ -0.3 inside, +1.0 outside):
# delta_rho_DE / rho_DE ~ Pi_SQMH * 1.3 (wall to void difference)
# Still ~ 10^-62. Undetectable.

print("Q61 Assessment (Void Bias):")
print("  SQMH predicts rho_DE anti-correlated with matter density:")
print("  rho_DE(void) > rho_DE(filament) > rho_DE(cluster)")
print("  Enhancement factor: 1 + Pi_SQMH * |delta_m| ~ 1 + {:.2e} * |delta_m|".format(
    Pi_SQMH))
print("  Signal: delta_rho_DE/rho_DE ~ 10^-62 * |delta_m|")
print("")
print("  Observable? NO.")
print("    Current precision: ~ 1% (delta_rho/rho ~ 10^-2)")
print("    SQMH signal: ~ 10^-62")
print("    Gap: 60 orders of magnitude")
print("")
print("Q64 Assessment (z_DE from void onset):")
print("  Void bias does not predict z_DE directly.")
print("  The bias exists at all z, but with the same Pi_SQMH ~ 10^-62 suppression.")
print("")
print("CONCLUSION:")
print("  Attempt 15 (void bias) is physically well-defined and mathematically correct.")
print("  SQMH predicts rho_DE is higher in voids and lower in clusters.")
print("  This is an anti-correlation: b_DE = -Pi_SQMH * b_matter ~ -10^-62.")
print("  The void bias IS a new qualitative prediction (direction: anti-correlation).")
print("  QUANTITATIVELY: unobservable (10^-62 suppression).")
print("  Q61 result: QUALITATIVE PASS (direction), QUANTITATIVE FAIL (amplitude).")
print("  This is the most interesting attempt for paper discussion.")
