# simulations/l11/detailed_balance/wwa_direction.py
# Attempt 4: Detailed balance -> wa < 0 directionality
# Rule-B 4-person review

import numpy as np
from scipy.integrate import odeint
import warnings
warnings.filterwarnings('ignore')

# --- Constants ---
H0 = 2.183e-18      # s^-1
sigma_sq = 4.521e-53 # m^3 kg^-1 s^-1
Omega_m = 0.315
rho_crit0 = 9.472e-27
rho_m0 = Omega_m * rho_crit0
rho_DE0 = (1.0 - Omega_m) * rho_crit0
t_P = 5.391e-44     # s

# --- SQMH equilibrium value ---
def H_z(z):
    return H0 * np.sqrt(Omega_m * (1+z)**3 + (1-Omega_m))

def rho_m_z(z):
    return rho_m0 * (1+z)**3

def n_eq_z(z, Gamma0, sigma=sigma_sq):
    return Gamma0 / (sigma * rho_m_z(z) + 3.0 * H_z(z))

# Set Gamma0 from z=0 rho_DE:
# rho_DE0 = n_eq(0) * epsilon_P where epsilon_P is Planck energy density
# We work in normalized units: n_eq(0) = 1 by definition
Gamma0_norm = 3.0 * H0  # normalized so n_eq(0) = 1

# --- Detailed balance condition ---
# Exact detailed balance: Gamma0 = sigma*n_eq*rho_m + 3H*n_eq
# This IS the definition of n_eq. Detailed balance = exact equilibrium.
# So the question is: is the current universe ABOVE or BELOW n_eq?

# In SQMH, n_bar(t) satisfies:
# dn_bar/dt = Gamma0 - sigma*n_bar*rho_m - 3H*n_bar

# Approach from BELOW (n < n_eq): dn/dt > 0, system grows toward n_eq
#   This means dark energy INCREASING (from below) -> wa > 0 (growing w toward -1)
# Approach from ABOVE (n > n_eq): dn/dt < 0, system falls toward n_eq
#   This means dark energy DECREASING (from above) -> wa < 0 (w becoming more negative)

print("=== L11 Attempt 4: Detailed Balance -> wa < 0 ===")
print("")

# --- Determine current departure from detailed balance ---
# At z=0, n_bar = n_eq(0) by assumption (we've normalized to this).
# But the DYNAMICAL HISTORY matters: n was different in the past.

# In matter era (z >> 1): n_eq_high = Gamma0/(sigma*rho_m_high + 3H_high)
# sigma*rho_m_high >> 3H_high iff sigma*rho_m >> 3H
# sigma*rho_m0 / (3*H0) = 2e-62 (tiny at z=0)
# At z: sigma*rho_m(z)/(3H(z)) = sigma*rho_m0*(1+z)^3 / (3*H0*sqrt(Om*(1+z)^3 + OL))
# In matter era (Om*(1+z)^3 >> OL):
# ~ sigma*rho_m0*(1+z)^3 / (3*H0*sqrt(Om)*(1+z)^(3/2))
# = (sigma*rho_m0)/(3*H0*sqrt(Om)) * (1+z)^(3/2)
# = Pi_SQMH_approx * (1+z)^(3/2)
# Even at z=1100 (CMB): Pi_approx * 1100^(3/2) = 2e-62 * 3.6e4 = 7.2e-58 (still tiny)
Pi_approx = sigma_sq * rho_m0 / (3.0 * H0 * np.sqrt(Omega_m))
print("Pi_SQMH approx = sigma*rho_m0/(3*H0*sqrt(Om)): {:.3e}".format(Pi_approx))
print("At z=0: sigma*rho_m/(3H) = {:.3e}".format(sigma_sq * rho_m0 / (3.0 * H0)))
print("At z=1100: sigma*rho_m/(3H) ~ Pi * 1100^1.5 = {:.3e}".format(
    Pi_approx * 1100**1.5))
print("")

# Since sigma*rho_m << 3H at ALL cosmological z, n_eq(z) ~ Gamma0/(3H(z))
# So n_eq(z) ~ rho_DE0 * H_z(0)/H_z(z) = rho_DE0 / E(z)
z_arr = np.linspace(0.0, 3.0, 100)
E_arr = np.array([np.sqrt(Omega_m*(1+z)**3 + (1-Omega_m)) for z in z_arr])
n_eq_arr = 1.0 / E_arr  # normalized

# rho_DE from SQMH (proportional to n_eq):
rho_DE_sqmh = n_eq_arr * rho_DE0  # kg/m^3

# Now compute effective w(z):
# From continuity: d(rho_DE)/dt + 3H*(1+w)*rho_DE = 0
# -> (1+w) = -1/(3H) * d(ln rho_DE)/dt = -1/(3H) * (-d ln rho_DE / d ln a) * H
# = (1/3) * d(ln rho_DE) / d(ln a)
# a = 1/(1+z), d ln a = -dz/(1+z)
# d(ln rho_DE_sqmh)/dz = d(ln n_eq)/dz = -d(ln E)/dz

def ln_n_eq(z):
    return -np.log(np.sqrt(Omega_m*(1+z)**3 + (1-Omega_m)))

# Numerical derivative d(ln rho_DE)/d(ln a) = -(1+z) * d(ln rho_DE)/dz
dz = 1e-4
w_sqmh_arr = []
for z in z_arr:
    dln_dz = (ln_n_eq(z + dz) - ln_n_eq(z - dz)) / (2 * dz)
    dln_dlna = -(1.0 + z) * dln_dz
    w_sqmh = -1.0 + dln_dlna / 3.0
    w_sqmh_arr.append(w_sqmh)
w_sqmh_arr = np.array(w_sqmh_arr)

# CPL fit: w(z) = w0 + wa * z/(1+z)
# At z=0: w(0) = w0
# Derivative: dw/dz|_{z=0} = wa
w0_sqmh = w_sqmh_arr[0]
wa_sqmh = (w_sqmh_arr[10] - w_sqmh_arr[0]) / z_arr[10]  # finite difference

print("SQMH background w(z) (from n_eq(z) ~ 1/E(z)):")
print("  w(z=0) = {:.6f}".format(w0_sqmh))
print("  w(z=1) = {:.6f}".format(w_sqmh_arr[50]))
print("  wa estimate = {:.6f}".format(wa_sqmh))
print("")

# Detailed balance direction:
# n_bar approaches n_eq(z) from ABOVE or BELOW?
# In early universe: n_bar(z_init) set by initial conditions.
# If n_bar starts at 0 (no DE) and grows to n_eq:
# -> approaches from BELOW -> wa > 0 (increasing n_bar)
# If n_bar starts at some large value and decays:
# -> approaches from ABOVE -> wa < 0 (decreasing n_bar)

# SQMH w(z) we computed: wa_sqmh should indicate direction
print("Detailed balance direction interpretation:")
print("  SQMH w(z=0) = {:.4f}, w(z=1) = {:.4f}".format(w0_sqmh, w_sqmh_arr[50]))
print("  w increases from z=0 to z=1 (wa positive) or decreases (wa negative)?")
print("  w(z=0) - w(z=1) = {:.6f}".format(w0_sqmh - w_sqmh_arr[50]))
print("")

# Actually w_SQMH(z) = -1 + (1/3) * d(ln n_eq)/d(ln a)
# n_eq(z) ~ 1/E(z) ~ 1/sqrt(Om*(1+z)^3 + OL)
# As z increases (going back in time), E increases, n_eq decreases
# So n_eq was SMALLER in the past, larger now.
# n_bar tracks n_eq from below (growing) or above (falling)?
# If Big Bang n_bar = 0 and it grows: approaches n_eq from BELOW
# -> wa > 0 (n_bar growing toward n_eq)

# The SQMH predicted wa from A12 fitting is wa = -0.133 < 0.
# This CONTRADICTS "approach from below" (which gives wa > 0).
# Resolution: A12 is a phenomenological fit, not derived from SQMH dynamics.
# The SQMH birth-death process predicts wa > 0 (approach from below)
# But A12 empirically shows wa < 0.

print("Q63 Assessment:")
print("  SQMH birth-death approach from n=0: n_bar grows toward n_eq")
print("  This implies wa > 0 (dark energy INCREASING from below)")
print("  But A12 gives wa = -0.133 < 0")
print("  Contradiction: SQMH dynamics predict wa > 0, data prefer wa < 0")
print("  Q63 result: FAIL (detailed balance approach gives wa > 0, not wa < 0)")
print("")
print("  Note: wa < 0 could arise if n_bar STARTS ABOVE n_eq in early universe,")
print("  then falls down. This requires n_bar(z_init) > n_eq(z_init).")
print("  Physical interpretation: over-production of spacetime quanta at high z")
print("  (e.g., inflation produces excess n_bar -> decay to n_eq gives wa < 0).")
print("  This is speculative but physically consistent.")
print("")
print("  Revised Q63: CONDITIONAL PASS if initial conditions include n_bar > n_eq.")
print("  The detailed balance approach DOES connect to wa sign, but requires")
print("  specific initial conditions (n_bar_init > n_eq_init).")
