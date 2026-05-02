#!/usr/bin/env python3
"""L209 — SQT n field vs direct DM detection limits."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L209"); OUT.mkdir(parents=True,exist_ok=True)

print("L209 — SQT n field vs DM detection limits (XENON1T, LZ)")
# n field at galactic regime: density ~ rho_DM_local ~ 0.4 GeV/cm^3
# n quanta energy: eps = hbar*H_0 ~ 1.5e-33 J = 1e-14 eV (cosmic)
# At galactic regime: tau_q is shorter → eps higher
# tau_q_galactic = sigma_galactic / (4*pi*G)

c = 2.998e8; G = 6.674e-11; hbar = 1.055e-34
H0 = 73e3/3.086e22
sigma_galactic = 10**9.56
tau_q_gal = sigma_galactic/(4*np.pi*G)
eps_gal = hbar/tau_q_gal  # J
eps_gal_eV = eps_gal/1.602e-19
print(f"  tau_q_galactic = {tau_q_gal:.3e} s")
print(f"  eps_galactic = {eps_gal:.3e} J = {eps_gal_eV:.3e} eV")

# Mass equivalent
m_n_kg = eps_gal/c**2
m_n_eV = m_n_kg*c**2/1.602e-19
print(f"  m_n equivalent = {m_n_eV:.3e} eV/c^2")

# DM detection threshold:
# XENON1T: m_DM > ~1 GeV for nuclear recoil
# DAMIC, SuperCDMS: m_DM > ~1 MeV for electron recoil
# axion-like: m_a ~ 1e-6 eV
# n field at eV level — between SuperCDMS limit and axion regime

# Cross-section: sigma_0 (SQT) is space-quanta absorption rate, NOT particle scattering
# sigma_n-nucleon: not directly given, but from EFT cutoff Lambda_UV ~ 18 MeV
# coupling g ~ 1/Lambda_UV^2 typical
Lambda_UV = 18e6 * 1.602e-19  # J
Lambda_UV_kg = Lambda_UV/c**2
sigma_n_p = (hbar*c)**2 / Lambda_UV**2  # natural unit estimate, m^2
sigma_n_p_cm2 = sigma_n_p*1e4
print(f"\n  EFT cutoff Lambda_UV = 18 MeV")
print(f"  Estimated n-p cross section ~ (hbar c)^2/Lambda_UV^2 = {sigma_n_p_cm2:.3e} cm^2")

# DM direct detection limits at m_n ~ eV scale
# SuperCDMS-CPD m_DM ~ 1 keV: limit ~ 1e-32 cm^2
# At eV scale: weakly constrained
xenon_limit_GeV = 1e-46  # cm^2 at GeV scale
dm_limit_at_eV = 1e-30  # cm^2 (rough scale, SENSEI-type bounds)
print(f"  SENSEI limit at eV mass: ~{dm_limit_at_eV:.0e} cm^2")
print(f"  SQT estimate vs limit: {sigma_n_p_cm2:.3e} vs {dm_limit_at_eV:.0e}")

if sigma_n_p_cm2 < dm_limit_at_eV:
    verdict_dm = f"PASS — SQT cross-section below DM detection limits at eV mass scale"
else:
    verdict_dm = f"FAIL — SQT cross-section ABOVE limits, conflict with detection nulls"
print(f"  → {verdict_dm}")

# Honest critique: this estimate is naive — actual SQT prediction would need
# detailed coupling structure, not yet derived
print(f"\n  HONEST CAVEAT: n-nucleon cross-section structure not derived in SQT.")
print(f"    Cross-section above is order-of-magnitude estimate from EFT cutoff.")
print(f"    Real test requires explicit Lagrangian coupling — open work.")

verdict = (f"SQT n field at eV mass ({m_n_eV:.2e} eV), naive sigma_np ~ {sigma_n_p_cm2:.2e} cm^2. "
           f"vs SENSEI eV-scale limit ~{dm_limit_at_eV:.0e} cm^2. {verdict_dm}. "
           "However, derivation of n-nucleon coupling not yet explicit — caveat applies.")

with open(OUT/'report.json','w') as f:
    json.dump(dict(eps_galactic_eV=float(eps_gal_eV),
                   m_n_eV=float(m_n_eV),
                   Lambda_UV_MeV=18,
                   sigma_np_cm2=float(sigma_n_p_cm2),
                   dm_limit_cm2=dm_limit_at_eV,
                   verdict_dm=verdict_dm,
                   verdict=verdict), f, indent=2)

# Simple bar plot
fig, ax = plt.subplots(figsize=(10,6))
labels = ['SQT estimate', 'SENSEI eV limit', 'XENON1T GeV limit']
vals = [sigma_n_p_cm2, dm_limit_at_eV, xenon_limit_GeV]
ax.bar(labels, vals, color=['tab:blue', 'tab:orange', 'tab:red'])
ax.set_yscale('log'); ax.set_ylabel('cross section (cm^2)')
ax.set_title('L209 — SQT vs DM detection limits')
plt.tight_layout(); plt.savefig(OUT/'L209.png', dpi=120); plt.close()
print("L209 DONE")
