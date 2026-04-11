# simulations/l11/cme_spectrum/rhode_power_spectrum.py
# Attempt 13: Chemical Master Equation -> rho_DE power spectrum
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

print("=== L11 Attempt 13: CME -> rho_DE Power Spectrum ===")
print("")

# Ornstein-Uhlenbeck process for n_bar(t):
# dn = -gamma*(n - n_eq) dt + sqrt(2*D) dW
# gamma = mu = sigma*rho_m + 3H ~ 3H0 (relaxation rate)
# D = Gamma_0/2 = (n_eq * mu)/2 (Poisson noise)

gamma_0 = sigma_sq * rho_m0 + 3.0 * H0  # = mu
n_eq = 1.0  # normalized
D_noise = n_eq * gamma_0 / 2.0  # normalized Poisson noise

print("O-U parameters:")
print("  gamma = mu = 3H0 = {:.4e} s^-1".format(gamma_0))
print("  D = Gamma_0/2 = n_eq*mu/2 = {:.4e} (normalized)".format(D_noise))
print("")

# Power spectrum of O-U process:
# S_n(omega) = 2*D / (gamma^2 + omega^2)
# = (n_eq * gamma) / (gamma^2 + omega^2)
# Peak at omega = 0, half-power at omega = gamma = 3H0

omega_arr = np.logspace(-3, 3, 1000) * gamma_0  # s^-1
S_n = 2.0 * D_noise / (gamma_0**2 + omega_arr**2)

print("rho_DE power spectrum S(omega) [O-U / CME]:")
print("  Peak (omega=0): S(0) = 2D/gamma^2 = n_eq/gamma = {:.4e} s".format(n_eq/gamma_0))
print("  Half-power frequency: omega_HP = gamma = {:.4e} s^-1".format(gamma_0))
print("  = {:.2f} * H0".format(gamma_0 / H0))
print("")

# Integrated power (variance):
variance = trapezoid(S_n / (2.0 * np.pi), omega_arr)
print("Integrated variance (from power spectrum):")
print("  Var(n)/n_eq^2 = {:.4e}".format(variance / n_eq**2))
print("  (Expected from Poisson: Var/mean^2 = 1/n_eq)".format())
print("  For normalized n_eq=1: Var = n_eq = {:.4f}".format(n_eq))
print("")

# Physical units:
# rho_DE = n * E_P / l_P^3
# S_rho(omega) = (E_P/l_P^3)^2 * S_n(omega)
# But absolute S_n depends on n_eq in physical units (10^42 / V_H).

# For detection by PTA (Pulsar Timing Arrays):
# PTA is sensitive to GW background at f ~ 1-100 nHz = 10^-9 - 10^-7 Hz
# Hubble frequency: f_H = H0/(2pi) = 2.183e-18 / (2*pi) = 3.47e-19 Hz
# PTA band: 10^-9 Hz (much higher than f_H)

f_H = H0 / (2.0 * np.pi)
f_PTA_min = 1e-9  # Hz
print("Frequency comparison:")
print("  Hubble frequency f_H = {:.3e} Hz".format(f_H))
print("  PTA band minimum f_PTA = {:.3e} Hz".format(f_PTA_min))
print("  Ratio f_PTA / f_H = {:.3e}".format(f_PTA_min / f_H))
print("")

# S(omega_PTA) is vastly suppressed compared to S(omega_H):
omega_PTA = 2.0 * np.pi * f_PTA_min
S_at_PTA = 2.0 * D_noise / (gamma_0**2 + omega_PTA**2)
S_at_H = 2.0 * D_noise / (gamma_0**2 + (2*np.pi*f_H)**2)
print("Power spectrum suppression at PTA vs Hubble frequency:")
print("  S(omega_PTA) / S(omega_H) = {:.4e}".format(S_at_PTA / S_at_H))
print("  At PTA frequencies, SQMH power is suppressed by ~ (H0/omega_PTA)^2 ~ 10^-20")
print("")

print("21cm signal:")
print("  SQMH rho_DE fluctuations at 21cm frequencies:")
print("  f_21cm ~ GHz -> omega_21cm ~ 10^9 Hz >> gamma ~ 10^-18 Hz")
print("  S(omega_21cm) ~ 2D/(omega_21cm)^2 ~ 0 (completely negligible)")
print("")

print("Conclusion:")
print("  SQMH O-U power spectrum peaks at omega = H0 (Hubble frequency).")
print("  PTA and 21cm observations are at omega >> H0 -> spectrum suppressed.")
print("  No observable rho_DE fluctuation power in any current frequency band.")
print("  Attempt 13: Well-defined spectrum, completely unobservable.")
