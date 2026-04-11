# simulations/l11/turing/sqmh_turing.py
# Attempt 18: Turing instability -> DE spatial pattern conditions
# Rule-B 4-person review

import numpy as np
from scipy.linalg import eigvals
import warnings
warnings.filterwarnings('ignore')

# --- Constants ---
H0 = 2.183e-18
sigma_sq = 4.521e-53
Omega_m = 0.315
rho_crit0 = 9.472e-27
rho_m0 = Omega_m * rho_crit0

print("=== L11 Attempt 18: Turing Instability -> DE Spatial Pattern ===")
print("")

# Two-component system: (n_bar, delta_m) [DE quantum density, matter perturbation]
# SQMH equation for n:
# dn/dt = Gamma_0 - sigma*n*rho_m - 3H*n
# Matter perturbation:
# d delta_m/dt = -3*H*delta_m + 3/2 * H^2/c^2 * (G_eff/G) * delta_m * (a/k)^2
# Linearized around (n_eq, delta_m = 0):
# delta_n_dot = -(sigma*rho_m0 + 3H) * delta_n - sigma*n_eq*rho_m0 * delta_m
# delta_m_dot = f_11 * delta_n + f_22 * delta_m

# f_22 = -3*H + 3/2*H^2/c^2*G_eff/G * a^-2 / k^2 * a^2 (schematic for k=H)
# At sub-Hubble scales (k >> H/c): growth is dominated by gravity
# f_22 ~ -3H/2 (deceleration in matter era)

mu = sigma_sq * rho_m0 + 3.0 * H0  # relaxation rate for n
n_eq = 1.0  # normalized
sigma_n_rho = sigma_sq * rho_m0  # coupling delta_m -> delta_n

print("Jacobian matrix for (delta_n, delta_m) system:")
print("  J_11 = -mu = -{:.4e}".format(mu))
print("  J_12 = -sigma*n_eq*rho_m0 = -{:.4e}".format(sigma_n_rho))
print("  J_21 = 0 (n does not directly drive matter growth)")
print("  J_22 = gravity_term ~ -3H/2 = -{:.4e}".format(1.5*H0))
print("")

# Jacobian:
J = np.array([
    [-mu, -sigma_n_rho],
    [0.0, -1.5*H0]
])

eigenvals = eigvals(J)
print("Eigenvalues of Jacobian:")
for i, ev in enumerate(eigenvals):
    print("  lambda_{} = {:.4e}".format(i, ev.real))
print("")

# For Turing instability: need at least one eigenvalue with positive real part
# when spatial coupling (diffusion) is present.
# Standard Turing: J has stable eigenvalues, but adding D*k^2 to diagonal creates instability
# for some k.

# SQMH has no diffusion term for n. So Turing instability does NOT apply.
# Instead: check if coupled system has growing modes.

print("Turing condition check:")
print("  For standard Turing instability: need Det(J) > 0, Tr(J) < 0 (for homogeneous stability)")
tr_J = J[0,0] + J[1,1]
det_J = J[0,0]*J[1,1] - J[0,1]*J[1,0]
print("  Tr(J) = {:.4e}".format(tr_J))
print("  Det(J) = {:.4e}".format(det_J))
print("  Stability: Tr < 0 and Det > 0? {}, {}".format(tr_J < 0, det_J > 0))
print("")

# Without diffusion: cannot generate Turing patterns.
# With diffusion added to n: D_n*k^2 shifts J_11 to J_11 - D_n*k^2
# For Turing instability with D_n << D_m:
# Need cross-terms J_12 * J_21 > 0, but J_21 = 0 (n doesn't drive matter directly)

print("Turing instability analysis:")
print("  J_21 = 0 (n_bar does not directly couple to matter growth)")
print("  This breaks the Turing mechanism (needs cross-activation)")
print("  With J_21=0: NO Turing instability possible at any diffusion ratio")
print("")

# Indirect coupling: n_bar affects w(z) -> affects rho_DE -> affects H -> affects growth
# But this is a background-level coupling, not a local perturbation coupling.

print("Conclusion:")
print("  SQMH (n_bar, delta_m) system does NOT exhibit Turing instability.")
print("  Reason: J_21 = 0 (n does not drive matter perturbations locally).")
print("  G_eff/G coupling to delta_m is sub-dominant (G_eff/G - 1 ~ 10^-62).")
print("  Attempt 18: No spatial DE pattern from Turing mechanism in SQMH.")
print("  This is EXPECTED from K52 (nonlinear corrections negligible).")
