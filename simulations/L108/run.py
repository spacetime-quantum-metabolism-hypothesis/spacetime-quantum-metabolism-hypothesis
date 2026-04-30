#!/usr/bin/env python3
"""L108 — H_0 tension: Branch B contribution."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L108"); OUT.mkdir(parents=True,exist_ok=True)

print("L108 — H_0 tension: Branch B vs SHoES/Planck")
# SHoES: H_0 = 73.0 ± 1.0 km/s/Mpc (Cepheid + SN Ia)
# Planck CMB: H_0 = 67.4 ± 0.5 km/s/Mpc (early universe extrapolation)
# Tension: ~5σ

# Branch B with constant Γ_0:
# - At recombination: same as LCDM (L106 PASS)
# - Today: σ_galactic for local gravity, σ_cosmic for cosmic Λ
# - H_0_local = 73.8 (Cepheid) vs H_0_cosmic = 67.4 (CMB+BAO)
# Branch B doesn't naturally split these — both should match LCDM
# → H_0 tension UNRESOLVED in standard Branch B

# Possible resolution via L78 Γ_0(t):
# If Γ_0 varied since recombination, late-time H_0 different from early
# DESI data already prefers w_a < 0 → Branch B with Γ_0(t) could fit BOTH

# Actually: SHoES vs Planck tension *might* be reduced by w_a < 0 evolution
# Some papers (e.g., Niedermann-Sloth EDE) show DE evolution can shift H_0
# Branch B + Γ_0(t) might have similar effect

print("  H_0 tension: ~5σ between Cepheid (73.0) and Planck (67.4)")
print("  Branch B (const Γ_0): doesn't resolve")
print("  Branch B + L78 Γ_0(t): potentially resolves (similar to EDE)")
print()
# Quantitative: Γ_0(z) decrease past = lower ρ_Λ past = early DE =
# higher H_pre-recombination → smaller r_s → higher H_0_inferred from BAO
# This could reconcile SHoES vs Planck

# Numerical estimate:
# Γ_0(z=2)/Γ_0(0) = 0.76 (L78 best fit)
# At z=1100: extrapolated Γ_0 ratio depends on model
# Naive (1 + 0.077z - 0.085z²): negative for z > ~1, model breaks
# Need physical model
print(f"  Γ_0(z=2)/Γ_0(0) = 0.76 (L78)")
print(f"  Extrapolation to z=1100 unphysical with current ansatz")
print(f"  → Need EDE-like Γ_0(t) model for full H_0 tension solution")

verdict = ("Branch B (const Γ_0) does NOT resolve H_0 tension. "
           "L78 Γ_0(t) extension may help (similar to early DE), "
           "but extrapolation to z=1100 requires new ansatz. "
           "Promising path but unresolved.")

fig, ax = plt.subplots(figsize=(10,6))
methods = ['Cepheid (SHoES)', 'TRGB', 'Strong lensing', 'Planck CMB', 'BAO+SN', 'BB+Γ_0(t)?']
H_vals = [73.0, 69.8, 73.3, 67.4, 67.4, 70.0]
H_err  = [1.0, 1.7, 1.7, 0.5, 0.5, 2.0]
colors_h = ['red', 'orange', 'red', 'blue', 'blue', 'green']
ax.errorbar(H_vals, methods, xerr=H_err, fmt='o', markersize=10, capsize=5,
            ecolor='black')
for i, c in enumerate(colors_h):
    ax.scatter([H_vals[i]], [methods[i]], color=c, s=100, zorder=5)
ax.set_xlabel('H_0 [km/s/Mpc]')
ax.set_title('L108 — H_0 tension: Branch B + Γ_0(t) potential resolution')
plt.tight_layout(); plt.savefig(OUT/'L108.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(SHoES_H0=73.0, Planck_H0=67.4,
                   tension_sigma=5.0,
                   BranchB_const_resolves=False,
                   BranchB_Gamma_t_potential=True,
                   verdict=verdict), f, indent=2)
print("L108 DONE")
