#!/usr/bin/env python3
"""L87 — GW dispersion in SQT: refined T26 prediction."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L87"); OUT.mkdir(parents=True,exist_ok=True)

c = 2.998e8; G = 6.674e-11; hbar=1.055e-34; H0=73.8e3/3.086e22
tau_q=1/(3*H0); eps=hbar/tau_q
n_inf = 0.685*(3*H0**2/(8*np.pi*G))*c**2/eps

# GW propagation through SQT medium: medium absorption sigma_GW
# Refractive index n_GW = 1 + δn where δn from GW-quantum coupling
# δn ~ sigma_GW · n_inf · L / c   (for path length L)
# GW170817: distance D ≈ 40 Mpc, |c_g - c|/c < 1e-15
# → sigma_GW · n_inf · D < 1e-15
# → sigma_GW < 1e-15 · c / (n_inf · D)
D_GW170817 = 40 * 3.086e22  # m
sigma_GW_max = 1e-15 * c / (n_inf * D_GW170817)
print("L87 — GW dispersion in SQT")
print(f"  GW170817: D = 40 Mpc = {D_GW170817:.3e} m")
print(f"  Bound: |c_g - c|/c < 1e-15")
print(f"  → sigma_GW < {sigma_GW_max:.3e} m^3/(kg·s)")
print(f"  Comparison to σ_0(galactic) = 3.6e9: σ_GW / σ_0 < {sigma_GW_max/3.6e9:.3e}")
print(f"  → GW-quantum coupling is MUCH WEAKER than matter-quantum (σ_0)")
print()
print(f"  Future: ET/CE at higher frequencies and longer baselines")
print(f"          could tighten by 100x or more")
print(f"  Future: LISA at low frequency could test frequency dependence")

# Frequency dependence: in scenario where σ_GW ∝ ω, dispersion is
# Δc/c ∝ f. SQT default: σ_GW = const → no frequency dependence.

# SQT-specific prediction: GW absorption (amplitude attenuation) ≠ 0
# Attenuation length L_abs = 1/(σ_GW · n_inf · ρ_m)
# For GW170817: ρ_m ~ 1e-27 along path (mostly intergalactic)
rho_m_path = 1e-27
L_abs_max = 1.0 / (sigma_GW_max * n_inf * rho_m_path)
print(f"\nGW absorption length: L_abs > {L_abs_max:.3e} m = {L_abs_max/3.086e22:.3e} Gpc")
print(f"  (very long; not currently constraining)")

verdict = (f"GW dispersion: σ_GW < {sigma_GW_max:.2e} (GW170817), "
           f"σ_GW/σ_0(galactic) < {sigma_GW_max/3.6e9:.2e}. "
           "Future ET/CE/LISA can tighten by 100x.")

fig, ax = plt.subplots(figsize=(10,6))
events = ['GW170817\n(now)', 'GW230529\n(now)', 'ET/CE\n(2030s)', 'LISA\n(2034)']
bounds = [1e-15, 5e-16, 1e-17, 1e-18]
ax.bar(events, [-np.log10(b) for b in bounds], color='tab:purple', alpha=0.7)
ax.set_ylabel('-log10(|c_g-c|/c) bound')
ax.set_title('L87 — GW dispersion bound progression')
plt.tight_layout(); plt.savefig(OUT/'L87.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(sigma_GW_max=float(sigma_GW_max),
                   GW170817_D_m=float(D_GW170817),
                   ratio_to_sigma_galactic=float(sigma_GW_max/3.6e9),
                   verdict=verdict), f, indent=2)
print("L87 DONE")
