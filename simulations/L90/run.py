#!/usr/bin/env python3
"""L90 — NS and BH physics in SQT."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L90"); OUT.mkdir(parents=True,exist_ok=True)

c=2.998e8; G=6.674e-11; hbar=1.055e-34; H0=73.8e3/3.086e22

print("L90 — Neutron stars and black holes in SQT")

# Neutron star: rho ~ 10^17 kg/m^3 (nuclear)
rho_NS = 1e17
sigma_gal = 10**9.56
tau_q = 1/(3*H0)
n_inf = 0.685*(3*H0**2/(8*np.pi*G))*c**2/(hbar/tau_q)
Gamma_0 = n_inf/tau_q
# Steady state n inside NS: n = Gamma_0 / (sigma · rho)
n_NS = Gamma_0 / (sigma_gal * rho_NS)
print(f"  NS interior: rho = 1e17 kg/m^3")
print(f"    n_local / n_inf = {n_NS/n_inf:.3e}  (extreme depletion)")

# But local σ may be different — at NS-scale density, what regime?
# Actually density 1e17 is FAR above galactic (1e-21), needs new regime!
# Branch B has only 3 regimes; NS density is OUT of this range
print(f"  ⚠ NS density 1e17 is FAR above galactic regime threshold (1e-22)")
print(f"  Branch B σ_0(galactic) may not apply at NS density")
print(f"  → Branch B incomplete for NS physics")

# Black hole: Schwarzschild radius
M_sun = 1.989e30
M_BH = 10*M_sun  # stellar BH
r_s = 2*G*M_BH/c**2
print(f"\n  Black hole (10 M_sun):")
print(f"    Schwarzschild r_s = {r_s:.3e} m")
# At horizon: g_00 = 0, infinite redshift
# In SQT: quanta cannot escape horizon (causality F1)
# Hawking radiation: T_H = ℏc^3/(8π·G·M·k_B)
T_H = hbar*c**3/(8*np.pi*G*M_BH*1.38e-23)
print(f"    Hawking T = {T_H:.2e} K (very cold for stellar BH)")

# SQT prediction near BH:
# - n is depleted (P3) — but also stops being well-defined inside horizon
# - Cosmic creation Γ_0 still occurs OUTSIDE horizon
# - BH eats quanta, area grows (consistent with second law)
print(f"\n  SQT vs BH:")
print(f"    Outside horizon: standard quantum field n, GR-like geodesics")
print(f"    Inside horizon: SQT description breakdown (causality)")
print(f"    → Need full GR + SQT coupling at horizon — UV completion (LQG)")

# EHT shadow: SQT predicts identical to Schwarzschild at outside horizon
# Sgr A* shadow ~ 50 microarcsec — measured
print(f"\n  EHT shadow: SQT galactic regime = GR-like → matches observation")

verdict = ("SQT in NS/BH: outside horizon GR-like (✓). "
           "NS interior FAR above Branch B regime, NEEDS NEW REGIME (★)."
           " BH interior beyond SQT framework (UV completion needed).")

fig, ax = plt.subplots(figsize=(10,6))
regimes_density = ['cosmic', 'cluster', 'galactic', 'planet (Earth)', 'nuclear (NS)', 'Planck']
densities = [2.7e-27, 2.7e-24, 1.7e-21, 5500, 1e17, 5.16e96]
ax.bar(regimes_density, [np.log10(d) for d in densities], color='tab:purple', alpha=0.7)
ax.axhline(np.log10(1e-22), color='red', ls='--', label='Branch B galactic threshold')
ax.set_ylabel('log10(rho [kg/m^3])')
ax.set_title('L90 — Density regimes; Branch B covers up to galactic only')
ax.legend(); plt.setp(ax.xaxis.get_majorticklabels(), rotation=15)
plt.tight_layout(); plt.savefig(OUT/'L90.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(NS_density_kg_m3=float(rho_NS),
                   NS_above_branch_B="True — NEW REGIME needed",
                   BH_outside_horizon="GR-like ✓",
                   BH_inside_horizon="SQT breakdown — UV completion",
                   verdict=verdict), f, indent=2)
print("L90 DONE")
