# simulations/l11/kingman/sqmh_coalescent.py
# Attempt 14: Kingman coalescent -> SQMH causal origin time
# Rule-B 4-person review

import numpy as np
from scipy.integrate import quad
import warnings
warnings.filterwarnings('ignore')

# --- Constants ---
H0 = 2.183e-18
sigma_sq = 4.521e-53
Omega_m = 0.315
rho_crit0 = 9.472e-27
rho_m0 = Omega_m * rho_crit0
t_P = 5.391e-44
c = 3e8

print("=== L11 Attempt 14: Kingman Coalescent -> SQMH Origin Time ===")
print("")

# Kingman coalescent: N individuals, each pair merges at rate 1/N (C(N,2) pairs).
# In SQMH: reverse time, N = n_eq(z) spacetime quanta.
# All quanta "coalesce" to a single common ancestor in time T_MRCA.

# Time to coalesce N quanta to 1:
# T_MRCA = sum_{k=2}^{N} 1 / (k*(k-1)/2) = 2 * sum_{k=2}^{N} 1/(k*(k-1)) ~ 2

# For large N: T_MRCA ~ 2 * (1 - 1/N) ~ 2 (in units of N/rate)
# But "rate" here is 1/(tau_rel) = mu = 3H(z)

# At z=0: N ~ 10^42, rate = 3H0
# T_MRCA ~ 2 / (3H0) = 2/3 * t_Hubble

T_MRCA = 2.0 / (3.0 * H0)
t_Hubble = 1.0 / H0
print("Kingman coalescent T_MRCA:")
print("  T_MRCA = 2/(3H0) = {:.3e} s".format(T_MRCA))
print("  = {:.2f} * t_Hubble".format(T_MRCA / t_Hubble))
print("  = {:.2f} Gyr".format(T_MRCA / 3.156e16))
print("")

# Find redshift corresponding to T_MRCA:
def H_z(z):
    return H0 * np.sqrt(Omega_m * (1+z)**3 + (1-Omega_m))

def integrand_t(zz):
    return 1.0 / ((1.0 + zz) * H_z(zz))

def t_from_z(z):
    """Age of universe at redshift z (integral from z to infinity)."""
    val, _ = quad(integrand_t, z, 1000.0, limit=500)
    return val

t0 = t_from_z(0.0)
print("Cosmic age at z=0: {:.3e} s = {:.2f} Gyr".format(t0, t0/3.156e16))
print("T_MRCA = {:.3e} s = {:.2f} Gyr".format(T_MRCA, T_MRCA/3.156e16))
print("")

# Find z_MRCA where t_cosmic(z) = T_MRCA (i.e., when universe was T_MRCA old)
# t_cosmic(z) = t0 - t_from_z(z) [time elapsed since BB to z]
# We want t_cosmic(z_MRCA) = T_MRCA:
# -> t_from_z(z_MRCA) = t0 - T_MRCA

t_remaining = t0 - T_MRCA
print("t_remaining = t0 - T_MRCA = {:.3e} s".format(t_remaining))

if t_remaining > 0:
    z_scan = np.linspace(0.01, 20.0, 1000)
    for z in z_scan:
        t_to_today = t_from_z(z)
        if abs(t_to_today - t_remaining) < t_remaining * 0.02:
            z_MRCA = z
            print("z_MRCA (coalescent origin) ~ {:.2f}".format(z_MRCA))
            break
    else:
        print("z_MRCA not found in scan range")
else:
    print("T_MRCA > t0: coalescent time longer than universe age")
    print("  This means: spacetime quanta haven't all 'coalesced' yet")
print("")

# Physical interpretation:
# z_MRCA is when SQMH 'starts' (when DE quanta first appear from common ancestor)
# This is NOT a new prediction -- it's the SQMH relaxation time reinterpreted
# as 'common ancestor time'.

print("Physical interpretation:")
print("  T_MRCA = 2/(3H0) = {:.2f} Gyr is the SQMH relaxation time.".format(
    T_MRCA / 3.156e16))
print("  Corresponding to z_MRCA ~ {:.1f}".format(
    z_MRCA if t_remaining > 0 else -1))
print("  This is the time when DE 'effectively begins' in SQMH (relaxation time scale)")
print("  Not independent of existing SQMH predictions (T_FP = 1/(3H0))")
print("")
print("Conclusion:")
print("  Kingman coalescent gives T_MRCA = 2/(3H0) ~ Hubble time.")
print("  Equivalent to SQMH relaxation time (no new physics).")
print("  'Common ancestor' of DE quanta: the Big Bang initial conditions.")
print("  Attempt 14: Valid framework, tautological result.")
