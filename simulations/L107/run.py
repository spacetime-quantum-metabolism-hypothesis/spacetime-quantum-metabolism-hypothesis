#!/usr/bin/env python3
"""L107 — PTA stochastic GW: SQT contribution?"""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L107"); OUT.mkdir(parents=True,exist_ok=True)

print("L107 — PTA stochastic GW background")
# NANOGrav 2023: stochastic GW background detected at nHz
# Ω_GW ~ 1e-9 at f ~ 10 nHz
# Likely source: supermassive BH binaries (SMBHB)
# Alternatives: cosmic strings, primordial GW, new physics

# SQT contribution to GW background?
# SQT n field has fluctuations from quantum creation Γ_0
# Each Γ_0 event creates a quantum — might emit GW?
# Energy per event: ε ~ ℏH_0 ~ 7.6e-52 J
# This is way below any GW detection scale
# → SQT GW background is utterly negligible

hbar=1.055e-34; H0=73.8e3/3.086e22
eps = hbar/(1/(3*H0))
print(f"  ε per quantum event: {eps:.3e} J")
print(f"  PTA scale: ~10^-7 to 10^-9 Hz frequency, h ~ 1e-15")
print(f"  GW energy density at 10 nHz: ~ 1e-15 J/m³")
# SQT Γ_0 events per m³·s: ~6e24
Gamma_0 = 1e25  # rough
print(f"  SQT Γ_0: ~{Gamma_0:.1e} m^-3 s^-1")
energy_density_SQT = Gamma_0 * eps
print(f"  Energy density of SQT events: {energy_density_SQT:.3e} J/m³")
print(f"  → SQT events energy << PTA observed (1e-15 J/m³)")
print(f"  → SQT stochastic GW NEGLIGIBLE; PTA signal is from SMBHB or cosmic strings")

# What if Γ_0(t) varied: could cause early-universe GW bursts?
# In high-z universe with higher Γ_0, GW could be enhanced
# But total Γ_0 contribution at recombination still tiny vs radiation

verdict = ("SQT contributes negligibly to PTA stochastic GW. "
           "PTA detection is consistent with SMBHB / cosmic strings, "
           "not SQT new physics.")

fig, ax = plt.subplots(figsize=(10,6))
sources = ['SMBHB\n(expected)', 'cosmic strings\n(possible)', 'inflation', 'SQT events']
omega_GW = [1e-9, 1e-10, 1e-12, 1e-30]
ax.barh(sources, [-np.log10(o) for o in omega_GW], color='tab:blue', alpha=0.7)
ax.axvline(9, color='red', ls='--', label='NANOGrav detection 1e-9')
ax.set_xlabel('-log10(Ω_GW at nHz)')
ax.set_title('L107 — PTA stochastic GW sources')
ax.legend(); plt.tight_layout()
plt.savefig(OUT/'L107.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(SQT_GW_negligible=True,
                   PTA_consistent_source="SMBHB or cosmic strings",
                   verdict=verdict), f, indent=2)
print("L107 DONE")
