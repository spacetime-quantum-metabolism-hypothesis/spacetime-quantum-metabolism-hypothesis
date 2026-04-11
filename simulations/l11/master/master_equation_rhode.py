# simulations/l11/master/master_equation_rhode.py
# Attempt 2: Master equation -> rho_DE probability distribution (Negative Binomial)
# Rule-B 4-person review

import numpy as np
from scipy.stats import nbinom
import warnings
warnings.filterwarnings('ignore')

# --- SQMH constants at z=0 ---
H0 = 2.183e-18      # s^-1
sigma_sq = 4.521e-53 # m^3 kg^-1 s^-1
Omega_m = 0.315
rho_crit0 = 9.472e-27
rho_m0 = Omega_m * rho_crit0
rho_DE0 = (1.0 - Omega_m) * rho_crit0

E_Planck_J = 1.956e9  # J (Planck energy)
l_P = 1.616e-35       # m (Planck length)
V_P = l_P**3          # m^3 (Planck volume)

# Birth rate (production): lambda = Gamma_0
# Death rate (annihilation): mu = sigma*rho_m + 3H
# Negative Binomial parameters: r = Gamma_0/H, p = sigma*rho_m/(sigma*rho_m + 3H)

# At z=0:
lambda_rate = 3.0 * H0  # approximate: Gamma_0 = n_eq * (sigma*rho_m + 3H)
# since sigma*rho_m << 3H (by 62 orders), Gamma_0 ~ n_eq * 3H
mu_rate = sigma_sq * rho_m0 + 3.0 * H0

print("=== L11 Attempt 2: Master Equation -> rho_DE Distribution ===")
print("At z=0:")
print("  H0 [s^-1]: {:.4e}".format(H0))
print("  sigma * rho_m0 [s^-1]: {:.4e}".format(sigma_sq * rho_m0))
print("  3H0 [s^-1]: {:.4e}".format(3.0 * H0))
print("  ratio sigma*rho_m0 / (3H0): {:.4e}".format(sigma_sq * rho_m0 / (3.0 * H0)))
print("")

# Negative Binomial parameters:
# In standard birth-death notation: if birth = lambda, death = mu*n:
# Stationary distribution = Poisson(lambda/mu) (NOT negative binomial)
# Negative binomial arises when there is intrinsic fluctuation in mu.
# Standard linear birth-death: P(n) -> Poisson(n_eq) with n_eq = lambda/mu.

# NegBin parameters: r = Gamma_0/H_total, p = 3H/(3H + sigma*rho_m)
p = 3.0 * H0 / (3.0 * H0 + sigma_sq * rho_m0)
print("Negative Binomial parameters (model):")
print("  p = 3H/(3H + sigma*rho_m): {:.8f}".format(p))
print("  1-p = sigma*rho_m/(3H + sigma*rho_m): {:.4e}".format(1.0 - p))

# For Poisson limit (which is more accurate):
# <n> = n_eq = Gamma_0/(3H) (in high-n limit)
# Var(n) = n_eq (Poisson)
# delta_n/n_eq = 1/sqrt(n_eq)

# Total number of spacetime quanta in Hubble volume:
V_Hubble = (3e8 / H0)**3  # m^3
# rho_DE = N_total * E_Planck / V_Hubble
N_total = rho_DE0 * V_Hubble / E_Planck_J
print("")
print("Total spacetime quanta in Hubble volume:")
print("  V_Hubble [m^3]: {:.3e}".format(V_Hubble))
print("  rho_DE0 [J/m^3]: {:.3e}".format(rho_DE0 * (3e8)**2))
print("  N_total = rho_DE * V / E_Planck: {:.3e}".format(N_total))
print("")

# Fractional fluctuation (Poisson = shot noise)
frac_fluct = 1.0 / np.sqrt(N_total)
print("Fractional rho_DE fluctuation (Poisson shot noise):")
print("  delta_rho_DE / rho_DE = 1/sqrt(N_total): {:.4e}".format(frac_fluct))
print("")

# Skewness of Poisson: 1/sqrt(N_total)
skewness = 1.0 / np.sqrt(N_total)
print("Higher moments (Poisson distribution):")
print("  Skewness = 1/sqrt(N): {:.4e}".format(skewness))
print("  Kurtosis excess = 1/N: {:.4e}".format(1.0/N_total))
print("")

# rho_DE variance
var_rhode = (rho_DE0 * frac_fluct)**2
print("rho_DE variance: {:.3e} (kg/m^3)^2".format(var_rhode))
print("rho_DE std dev: {:.3e} kg/m^3".format(np.sqrt(var_rhode)))
print("rho_DE fractional std: {:.3e}".format(frac_fluct))
print("")

print("Summary:")
print("  Master equation -> Poisson distribution for n (spacetime quanta count)")
print("  delta_rho_DE/rho_DE = 1/sqrt(N_total) = {:.3e}".format(frac_fluct))
print("  This is model-independent (shot noise of N_total quanta)")
print("  Not observable by any current or planned instrument")
print("  Negative Binomial: only if Gamma_0 itself has variance (not in standard SQMH)")
print("  Conclusion: Attempt 2 gives well-defined result but unobservable fluctuations")
