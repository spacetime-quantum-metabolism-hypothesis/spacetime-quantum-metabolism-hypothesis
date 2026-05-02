"""L212 — tau_q micro origin: derivable check via (n0 sigma_0)^{-1}.

Hypothesis: tau_q = 1/(n0 * sigma_0 * c) (mean free time of metabolism event).
If yes, tau_q is NOT a free parameter.
"""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')

import numpy as np

# constants (SI)
c = 2.998e8
G = 6.674e-11
hbar = 1.055e-34
t_Pl = np.sqrt(hbar * G / c**5)  # ~5.4e-44 s
H0 = 67.4e3 / 3.086e22  # s^-1
t_H = 1.0 / H0  # ~4.6e17 s

# Branch B fitted (from L77-L99 record)
n0 = 4.1e95  # kg/m^3 (n0*mu = rho_Pl/(4pi))
mu = 1.0  # placeholder, n0*mu meaningful
sigma_0 = 4 * np.pi * G * t_Pl  # SI: m^3 kg^-1 s^-1, ~5.0e-54

# Candidate 1: tau_q = 1/(n0 sigma_0 c) [length-based mfp / c]
# Units: 1/(kg/m^3 * m^3/(kg s) * m/s) = s
tau_candidate_1 = 1.0 / (n0 * sigma_0 * c)
# Candidate 2: tau_q = 1/(n0 sigma_0) [time-based]
# Units: 1/(kg/m^3 * m^3/(kg s)) = s
tau_candidate_2 = 1.0 / (n0 * sigma_0)
# Candidate 3: t_Pl
tau_candidate_3 = t_Pl

print(f"t_Planck         = {t_Pl:.3e} s")
print(f"t_Hubble         = {t_H:.3e} s")
print(f"1/(n0 sigma_0 c) = {tau_candidate_1:.3e} s")
print(f"1/(n0 sigma_0)   = {tau_candidate_2:.3e} s")

# Compare to expected scale
# Branch B requires tau_q such that rho_q/rho_Lambda = 1
# rho_q ~ n0 * mu * (something with tau_q)
# If rho_q ~ (n0 mu) / (tau_q H0^2) and rho_Lambda ~ Omega_L * 3 H0^2 / (8 pi G):
rho_Pl = n0  # n0 ~ rho_Pl/(4pi) ~ 4.1e95
rho_Lambda = 0.685 * 3 * H0**2 / (8 * np.pi * G)
print(f"\nrho_Lambda       = {rho_Lambda:.3e} kg/m^3")
print(f"rho_Pl           = {rho_Pl:.3e} kg/m^3")
print(f"ratio            = {rho_Pl/rho_Lambda:.3e}")

# For rho_q = rho_Lambda, dilution factor needed:
dilution = rho_Pl / rho_Lambda
print(f"required dilution= {dilution:.3e}")
# tau_q^k = dilution * t_Pl^k for some k. If dilution ~ 10^123 ~ (t_H/t_Pl)^2:
ratio_t = t_H / t_Pl
print(f"(t_H/t_Pl)       = {ratio_t:.3e}")
print(f"(t_H/t_Pl)^2     = {ratio_t**2:.3e}")
print(f"log10 dilution   = {np.log10(dilution):.2f}")
print(f"log10 (t_H/t_Pl)^2={2*np.log10(ratio_t):.2f}")

# Conclusion check:
match = np.isclose(np.log10(dilution), 2*np.log10(ratio_t), atol=0.5)
print(f"\nDilution = (t_H/t_Pl)^2 ? {match}")

# tau_q grid scan: rho_q/rho_Lambda sensitivity
tau_grid = np.logspace(-44, 17, 62)  # 1 decade per point
# Toy: rho_q(tau_q) = rho_Pl * (t_Pl/tau_q)^2  (cosmological screening)
rho_q_grid = rho_Pl * (t_Pl / tau_grid)**2
ratio_grid = rho_q_grid / rho_Lambda
unity_idx = np.argmin(np.abs(np.log10(ratio_grid)))
tau_unity = tau_grid[unity_idx]
print(f"\ntau_q at rho_q/rho_L=1: {tau_unity:.3e} s")
print(f"compared to t_H/sqrt(Omega_Pl/Omega_L) ~ {t_Pl*np.sqrt(dilution):.3e} s")

# Save
import json
out = {
    't_Pl': float(t_Pl),
    't_H': float(t_H),
    'tau_candidate_n0sigma0c': float(tau_candidate_1),
    'tau_candidate_n0sigma0': float(tau_candidate_2),
    'rho_Pl_to_rho_Lambda': float(dilution),
    'tau_unity_screening': float(tau_unity),
    'derivable_via_n0sigma0': bool(np.isclose(np.log10(tau_candidate_2), np.log10(tau_unity), atol=2)),
}
with open(os.path.join(os.path.dirname(__file__), 'report.json'), 'w') as f:
    json.dump(out, f, indent=2)
print("\nreport.json saved.")
