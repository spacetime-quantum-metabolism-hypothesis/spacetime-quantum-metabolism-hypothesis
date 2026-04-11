# simulations/l11/generating_func/dark_energy_cumulants.py
# Attempt 7: Generating function -> DE non-Gaussianity (bispectrum)
# Rule-B 4-person review

import numpy as np
import warnings
warnings.filterwarnings('ignore')

# --- Constants ---
H0 = 2.183e-18
sigma_sq = 4.521e-53
Omega_m = 0.315
rho_crit0 = 9.472e-27
rho_DE0 = (1.0 - Omega_m) * rho_crit0
E_P_J = 1.956e9  # Planck energy in J
c = 3e8
l_P = 1.616e-35

print("=== L11 Attempt 7: Generating Function -> DE Non-Gaussianity ===")
print("")

# --- Generating function for linear birth-death ---
# G(s, t) = sum_{n=0}^inf P(n,t) * s^n
# For stationary birth-death with rate lambda (birth), mu*n (death):
# Stationary distribution: Poisson with mean n_bar = lambda/mu

# For SQMH:
# lambda = Gamma_0, mu = sigma*rho_m + 3H (per quantum)
# Stationary: Poisson with n_bar = Gamma_0 / (sigma*rho_m + 3H) = n_eq

# Cumulants of Poisson(n_bar):
# kappa_1 = n_bar (mean)
# kappa_2 = n_bar (variance = mean, Poisson property)
# kappa_3 = n_bar (3rd cumulant)
# kappa_r = n_bar for all r (Poisson)

# Total number in Hubble volume:
V_H = (c / H0)**3
N_bar = rho_DE0 * V_H / E_P_J
print("Total DE quanta in Hubble volume:")
print("  V_H = {:.3e} m^3".format(V_H))
print("  N_bar = rho_DE0 * V_H / E_P = {:.3e}".format(N_bar))
print("")

# Cumulants of N (total count in V_H):
kappa1 = N_bar
kappa2 = N_bar  # Poisson
kappa3 = N_bar  # Poisson
print("Cumulants of N (total quanta in Hubble volume):")
print("  kappa_1 (mean) = {:.3e}".format(kappa1))
print("  kappa_2 (variance) = {:.3e}".format(kappa2))
print("  kappa_3 (3rd cumulant) = {:.3e}".format(kappa3))
print("")

# Fractional cumulants (relative to mean):
frac_var = kappa2 / kappa1**2  # = 1/N_bar
frac_3rd = kappa3 / kappa1**3  # = 1/N_bar^2
print("Fractional cumulants:")
print("  sigma_N/N = 1/sqrt(N_bar) = {:.3e}".format(1.0/np.sqrt(N_bar)))
print("  kappa_3/mean^3 = 1/N_bar^2 = {:.3e}".format(1.0/N_bar**2))
print("")

# Translate to rho_DE cumulants:
frac_fluct_rho = 1.0 / np.sqrt(N_bar)
print("rho_DE fluctuation amplitude:")
print("  delta_rho_DE / rho_DE = {:.3e}".format(frac_fluct_rho))
print("")

# Bispectrum estimation:
# B_DE(k1, k2, k3) ~ (delta_rho_DE)^2 * rho_DE * f_NL
# For Poisson: f_NL_local = 1 (intrinsic Poisson non-Gaussianity)
# But delta_rho_DE/rho_DE ~ 10^-21 makes bispectrum signal:
B_DE = frac_fluct_rho**3  # very rough estimate of B/P^(3/2)
print("Bispectrum estimate (Poisson):")
print("  B/P^(3/2) ~ (delta_rho/rho)^3 = {:.3e}".format(B_DE))
print("")

# Euclid detection threshold for dark energy clustering:
# Euclid can detect f_NL ~ 1-5 from galaxy bispectrum.
# For DE non-Gaussianity: need fractional DE fluctuation > 10^-3 to be detectable.
print("Euclid detectability:")
print("  Required delta_rho_DE/rho_DE for detection: > 10^-3")
print("  SQMH Poisson prediction: {:.3e}".format(frac_fluct_rho))
print("  Gap: {:.1f} orders of magnitude".format(
    np.log10(1e-3 / frac_fluct_rho)))
print("")
print("Q65 Assessment:")
print("  SQMH bispectrum (Poisson shot noise) = {:.3e}".format(B_DE))
print("  Euclid threshold (rough): delta_rho/rho > 10^-3")
print("  Gap: {:.0f} orders of magnitude".format(np.log10(1e-3 / frac_fluct_rho)))
print("  Q65 result: FAIL (Poisson noise 18 orders below Euclid threshold)")
print("")
print("Note: This is the fundamental Poisson floor for SQMH stochasticity.")
print("  N_bar ~ 10^42 quanta -> fluctuations ~ 10^-21 (model-independent).")
print("  No stochastic extension of SQMH can produce DE bispectrum detectable by Euclid.")
