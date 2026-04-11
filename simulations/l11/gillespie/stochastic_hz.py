# simulations/l11/gillespie/stochastic_hz.py
# Attempt 9: Gillespie algorithm -> stochastic H(z) scatter
# Rule-B 4-person review

import numpy as np
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)

# --- Constants ---
H0 = 2.183e-18
sigma_sq = 4.521e-53
Omega_m = 0.315
rho_crit0 = 9.472e-27
rho_m0 = Omega_m * rho_crit0
rho_DE0 = (1.0 - Omega_m) * rho_crit0
E_P_J = 1.956e9  # J
c = 3e8

print("=== L11 Attempt 9: Gillespie -> Stochastic H(z) Scatter ===")
print("")

# Gillespie approach: simulate SQMH as exact Poisson birth-death process.
# Each event: birth (Gamma_0) or death (sigma*rho_m + 3H per quantum).
# Issue: Gamma_0 has units m^-3 s^-1 -> need to work in a reference volume.

# Work in Hubble volume V_H:
V_H = (c / H0)**3  # m^3

# Total N = n_bar * V_H ~ rho_DE0 * V_H / E_P:
N_bar = rho_DE0 * V_H / E_P_J
mu_0 = sigma_sq * rho_m0 + 3.0 * H0  # per quantum, s^-1
Gamma0_total = N_bar * mu_0  # total birth rate in V_H (s^-1)

print("Gillespie parameters:")
print("  N_bar (mean quanta in V_H) = {:.3e}".format(N_bar))
print("  mu_0 (death rate per quantum) = {:.4e} s^-1".format(mu_0))
print("  Gamma_0 total (birth rate in V_H) = {:.4e} s^-1".format(Gamma0_total))
print("")

# Fractional fluctuation of N in Gillespie:
# delta_N / N_bar = 1/sqrt(N_bar) (Poisson)
frac_fluct = 1.0 / np.sqrt(N_bar)
print("Gillespie N fluctuation: delta_N/N = 1/sqrt(N_bar) = {:.4e}".format(frac_fluct))
print("")

# H(z) scatter from N fluctuation:
# rho_DE(stochastic) = N_stochastic * E_P / V_H
# = rho_DE0 * (1 + delta_N/N_bar)
# = rho_DE0 * (1 + delta)
# E(z)^2 = Omega_m*(1+z)^3 + rho_DE(stoch)/rho_crit0
# delta_E^2 / E^2 = (rho_DE/rho_DE + rho_m) * frac_fluct * rho_DE/E^2
# At z=0: rho_DE/rho_crit = (1-Omega_m) = 0.685
delta_rho_DE = frac_fluct  # fractional
delta_E2 = (1.0 - Omega_m) * delta_rho_DE  # fractional delta in E^2
delta_H = 0.5 * delta_E2  # fractional delta in H
print("H(z) scatter from Gillespie stochasticity:")
print("  delta_rho_DE / rho_DE = {:.4e}".format(delta_rho_DE))
print("  delta_(E^2) / E^2 = (1-Om)*delta_rho = {:.4e}".format(delta_E2))
print("  delta_H / H = {:.4e}".format(delta_H))
print("")

# DESI BAO measurement precision:
sigma_H_DESI = 0.01  # ~ 1% per redshift bin
print("DESI BAO H(z) measurement precision: ~ {:.1%}".format(sigma_H_DESI))
print("SQMH Gillespie H(z) scatter: {:.4e}".format(delta_H))
print("Ratio (SQMH scatter / DESI precision): {:.4e}".format(delta_H / sigma_H_DESI))
print("")

# Realistic Gillespie simulation (simplified, small N proxy):
# We can't simulate N ~ 10^42. Instead, scale to N_proxy = 10^6.
N_proxy = 1e6
n_realizations = 100
N_sim = np.random.poisson(N_proxy, n_realizations)
frac_fluct_sim = np.std(N_sim) / np.mean(N_sim)

print("Simplified Gillespie simulation (N_proxy = 10^6):")
print("  Expected delta_N/N = {:.4f}".format(1.0/np.sqrt(N_proxy)))
print("  Simulated delta_N/N = {:.4f}".format(frac_fluct_sim))
print("  Scales to N_bar = {:.3e}: delta_H = {:.4e}".format(
    N_bar, frac_fluct_sim * (np.sqrt(N_proxy)/np.sqrt(N_bar))))
print("")

print("Conclusion:")
print("  Gillespie algorithm gives H(z) scatter ~ {:.2e}".format(delta_H))
print("  DESI BAO precision ~ 1% per bin")
print("  SQMH stochastic H(z) signature is {:.0f} orders below DESI precision".format(
    np.log10(sigma_H_DESI / delta_H)))
print("  Gillespie approach: correct, but unobservable.")
print("  No new observable predictions from stochastic H(z) scatter.")
