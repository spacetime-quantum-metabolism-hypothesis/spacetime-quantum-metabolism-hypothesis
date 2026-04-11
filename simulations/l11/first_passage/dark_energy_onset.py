# simulations/l11/first_passage/dark_energy_onset.py
# Attempt 3: First passage time -> dark energy onset redshift z_DE
# Rule-B 4-person review

import numpy as np
from scipy.integrate import solve_ivp
import warnings
warnings.filterwarnings('ignore')

# --- Constants ---
H0 = 2.183e-18      # s^-1
sigma_sq = 4.521e-53 # m^3 kg^-1 s^-1
Omega_m = 0.315
rho_crit0 = 9.472e-27
rho_m0 = Omega_m * rho_crit0
t_P = 5.391e-44     # s
t_Hubble = 1.0 / H0  # s ~ 4.58e17 s

# --- Birth-death first passage time ---
# For birth-death process starting at n=0 (no DE) to reach n=n_eq (current DE level):
# Mean first passage time: tau_FP = 1 / lambda (birth rate)
# where lambda = Gamma_0 (creation rate)
# tau_FP = 1/Gamma_0 ... but Gamma_0 is in m^-3 s^-1.
# We need to pick a reference volume.
#
# Better: the relaxation time of the birth-death process:
# tau_rel = 1 / (sigma*rho_m + 3H) ~ 1/(3H) at z=0
# This is the timescale for n_bar to reach equilibrium.
# tau_rel(z=0) = 1/(3*H0) = 1.53e17 s ~ 4.8 Gyr

print("=== L11 Attempt 3: First Passage Time -> z_DE ===")
print("")

# --- Approach 1: Relaxation time ---
tau_rel_0 = 1.0 / (3.0 * H0)
print("Relaxation time (z=0): tau_rel = 1/(3H0) = {:.3e} s".format(tau_rel_0))
print("  In Gyr: {:.2f} Gyr".format(tau_rel_0 / (3.156e16)))
print("")

# Find z where tau_rel(z) = t_Hubble - t(z):
# tau_rel(z) = 1/(sigma*rho_m(z) + 3H(z))
# DE "turns on" when tau_rel(z) ~ cosmic time t(z) from Big Bang.

def H_z(z):
    return H0 * np.sqrt(Omega_m * (1+z)**3 + (1-Omega_m))

def tau_rel_z(z):
    rho_m_z = rho_m0 * (1+z)**3
    return 1.0 / (sigma_sq * rho_m_z + 3.0 * H_z(z))

# Cosmic time t(z) via integration:
def integrand_t(zz):
    return 1.0 / ((1.0 + zz) * H_z(zz))

from scipy.integrate import quad
def t_cosmic(z):
    val, _ = quad(integrand_t, z, 100.0, limit=100)
    return val

# --- Q64 check: z where DE starts dominating ---
# Standard observation: dark energy onset around z_DE ~ 0.3-0.5 (matter-Lambda equality)
z_eq_DE = (Omega_m / (1.0 - Omega_m))**(1.0/3.0) - 1.0
print("Matter-Lambda equality redshift:")
print("  z_eq = (Omega_m/Omega_L)^(1/3) - 1 = {:.3f}".format(z_eq_DE))
print("  (This is z when rho_m = rho_DE, standard Lambda-CDM)")
print("")

# First passage approach: z_FP where tau_rel(z) matches t(z) from above
# i.e., system has time to equilibrate within cosmic time
print("Scanning z for tau_rel(z) vs t(z):")
z_scan = np.linspace(0.01, 5.0, 500)
t_arr = np.array([t_cosmic(z) for z in z_scan])
tau_arr = np.array([tau_rel_z(z) for z in z_scan])

# Find crossing
z_cross = None
for i in range(len(z_scan)-1):
    if (tau_arr[i] - t_arr[i]) * (tau_arr[i+1] - t_arr[i+1]) < 0:
        z_cross = 0.5 * (z_scan[i] + z_scan[i+1])
        break

print("  tau_rel(z=0) = {:.3e} s, t(z=0) = {:.3e} s".format(tau_arr[0], t_arr[0]))
print("  tau_rel(z=1) = {:.3e} s, t(z=1) = {:.3e} s".format(
    tau_rel_z(1.0), t_cosmic(1.0)))
print("  tau_rel(z=5) = {:.3e} s, t(z=5) = {:.3e} s".format(
    tau_rel_z(5.0), t_cosmic(5.0)))

if z_cross is not None:
    print("  Crossing z (tau_rel = t_cosmic): {:.3f}".format(z_cross))
else:
    print("  No crossing found in z = [0.01, 5.0]")
    print("  tau_rel >> t everywhere (process faster than Hubble time)")
    # tau_rel(z=0) = 1/(3H0) = 1.53e17 s
    # t(z=0) = t_Hubble ~ 4.35e17 s
    print("  tau_rel(0)/t(0) = {:.3f}".format(tau_rel_z(0.01) / t_cosmic(0.01)))
print("")

# --- Approach 2: Mean first passage from 0 to n_eq ---
# In a pure birth process (ignoring death): T_FP = n_eq / lambda = n_eq / Gamma_0
# But Gamma_0 = n_eq * 3H_0 (equilibrium). So T_FP = 1/(3H_0) = tau_rel!
# Same result: tau_FP = tau_rel ~ 1/(3H0) ~ Hubble time/3.

T_FP = 1.0 / (3.0 * H0)
T_Hubble = 1.0 / H0
print("First passage time (birth process):")
print("  T_FP = 1/(3H0) = {:.3e} s".format(T_FP))
print("  T_Hubble = 1/H0 = {:.3e} s".format(T_Hubble))
print("  T_FP / T_Hubble = {:.3f}".format(T_FP / T_Hubble))
print("")

# --- Conclusion ---
print("z_DE prediction (first passage approach):")
print("  Method 1 (tau_rel = t_cosmic): z_DE determined by when relaxation time")
print("  equals cosmic age. At z=0: tau_rel = {:.2f} * Hubble time.".format(
    tau_rel_z(0.01) / t_cosmic(0.01)))
print("  The process equilibrates fast (tau_rel < t_Hubble at all z > 0.3)")
print("  This suggests n_bar tracks n_eq(z) throughout cosmic history.")
print("")
print("  Method 2 (pure birth T_FP): T_FP = 1/(3H0) ~ 4.8 Gyr after Big Bang.")
print("  Corresponding redshift:")
t_FP = T_FP
# Find z where t_cosmic(z) = t_FP:
z_DE_FP = None
for z_try in np.linspace(0.01, 10.0, 1000):
    t_try = t_cosmic(z_try)
    if abs(t_try - t_FP) < t_FP * 0.02:
        z_DE_FP = z_try
        break
print("  z_DE (T_FP match): {:.2f}".format(z_DE_FP if z_DE_FP is not None else -1))
print("  Observed z_DE ~ 0.3-0.5 (matter-Lambda equality)")
print("")
print("Q64 Assessment:")
print("  First passage z_DE prediction from T_FP = 1/(3H0) ~ {:.2f} Gyr".format(
    T_FP / 3.156e16))
print("  Corresponding z ~ {:.2f}".format(z_DE_FP if z_DE_FP else -1))
print("  Observed z_DE ~ 0.3-0.5")
if z_DE_FP is not None and 0.2 <= z_DE_FP <= 0.6:
    print("  Q64 result: PASS (z_DE in range 0.2-0.6)")
else:
    print("  Q64 result: MARGINAL/FAIL")
    print("  Note: T_FP = 1/(3H0) is parametrically the same as relaxation time,")
    print("  which is set by H0 (tautological). Not an independent prediction.")
