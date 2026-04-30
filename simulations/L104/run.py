#!/usr/bin/env python3
"""L104 — EP in low-density regime (dwarf interior, voids)."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L104"); OUT.mkdir(parents=True,exist_ok=True)

print("L104 — EP in low-density regime")
hbar=1.055e-34; c=2.998e8; G=6.674e-11; H0=73.8e3/3.086e22
sigma_clu = 10**7.75   # cluster regime σ
sigma_gal = 10**9.56
n_inf = 0.685*(3*H0**2/(8*np.pi*G))*c**2/(hbar*3*H0)
# Dwarf galaxy interior: ρ ~ 1e-23 (transitional, L95 dSph)
# Two test bodies of different composition fall in dwarf gravitational field
# In SQT: gravitational force depends on σ·n·ρ_local (galactic) or modified
# In transitional regime: σ_eff intermediate

# But: EP says inertial mass = gravitational mass independent of composition
# SQT does NOT introduce composition dependence (a1-a6 silent on mass type)
# All matter couples via same σ_0
# → EP preserved across regimes

print("  EP in SQT: matter coupling σ_0·n·ρ_m universal (independent of composition)")
print("  → EP holds in ALL regimes (cosmic, cluster, galactic)")
print()
print("  However: COMPOSITION-dependent absorption σ_0(species)?")
print("  Axiom A1 silent on this. Default: σ_0 same for all matter")
print("  → EP exact in SQT (by construction)")

# But there could be a regime-transition effect:
# Same body, different gravitational regime → different σ_0
# This is NOT EP violation (same body in different gravity strength)
# But it's an environment-dependent EFFECTIVE inertia

# MICROSCOPE: tests on Earth at galactic regime; same regime, different composition
# → η < 1e-15 measured; SQT predicts η = 0 in same regime
# → SQT consistent with MICROSCOPE-1

# Cross-regime test (impossible on Earth):
# Free-fall test in dSph: rho ~ 1e-23 (cluster regime border)
# vs Earth: galactic regime
# Predicted ratio of inertial to gravitational mass: same
# But effective σ is different → free-fall ACCELERATION differs slightly?
# No — gravitational acceleration g = GM/r² is independent of σ
# σ enters only in cosmic Λ contribution

print("  Cross-regime test: dSph interior")
print("  ρ ~ 1e-23 (between cluster and galactic)")
print("  EP holds (matter coupling universal)")
print("  But σ_0_local interpolates between regimes (L95)")
print("  → No EP violation; only σ-dependent Λ contribution")

# NEW prediction: in cosmic voids (low density), local Λ_eff is different
# This can be tested: void galaxies should have slightly different a_0?
print("\n  Void galaxies: ρ ~ 1e-28 (cosmic regime border)")
print("  σ_0_local ≈ σ_cosmic = 10^8.37 (much smaller than galactic 10^9.56)")
print("  Local a_0_eff ∝ σ_0 → a_0(void galaxy) = a_0(field) × (10^8.37/10^9.56) ≈ 0.07")
print("  → SQT predicts void galaxies have ~7% of normal a_0!")
print("  → Testable with future void galaxy surveys")

verdict = ("EP exact in SQT (universal σ_0 coupling). "
           "MICROSCOPE-1 PASS by construction. "
           "NEW prediction: void galaxies have a_0 ~ 7% of normal (regime-dependent).")

fig, ax = plt.subplots(figsize=(10,6))
envs = ['Cosmic void', 'Cluster', 'Galaxy', 'Solar system', 'Earth lab']
log_rho = [-28, -24, -21, -21, -21]
sigma_eff = [10**8.37, 10**7.75, 10**9.56, 10**9.56, 10**9.56]
ax.bar(envs, [np.log10(s) for s in sigma_eff], color='tab:blue', alpha=0.7)
ax.set_ylabel('log10(σ_0_effective)')
ax.set_title('L104 — Effective σ_0 across environments (EP preserved everywhere)')
plt.setp(ax.xaxis.get_majorticklabels(), rotation=15)
plt.tight_layout(); plt.savefig(OUT/'L104.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(EP_violation=0,
                   void_galaxy_a0_ratio=10**(8.37-9.56),
                   verdict=verdict), f, indent=2)
print("L104 DONE")
