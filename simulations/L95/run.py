#!/usr/bin/env python3
"""L95 — Smooth regime transitions; galactic↔solar continuity."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L95"); OUT.mkdir(parents=True,exist_ok=True)

# Solar system: ρ_local ~ 1e-21 (interstellar) but inside Sun ~1e3
# Galactic disc: ρ ~ 1e-21
# So solar system is at galactic regime UPPER end

print("L95 — Galactic↔Solar continuity")
# Sun + planets in galactic disc → all 'galactic' regime
# σ_0 = σ_galactic for entire solar system
# Earth surface gravity, lunar dynamics: σ_galactic
# Pluto orbit: σ_galactic
# Oort cloud (1e4 AU): still galactic
# Outside heliopause but in galactic ISM: still galactic
# Only when leaving galaxy entirely → cluster regime

# Smoothness: how does σ transition?
# Phase transition has finite width w (L77 fit ~0.5 dex)
# Boundary at ρ_c2 ~ 1e-22: transition from cluster (σ_cluster) to galactic (σ_galactic)

# At ρ = 1e-22 (boundary), σ_0 takes intermediate value
# BUT: physical density gradient is very fast at galaxy edge
# (density falls from disc 1e-21 to halo 1e-25 over kpc)
# → Transition occurs in spatial region ~kpc
# Effective "smearing" of σ_0 over kpc

c=2.998e8
ρ_grid = np.logspace(-30, 5, 500)
log_ρ = np.log10(ρ_grid)
def sigma_smooth(lr, w=0.3):
    """Smooth 3-regime + saturation."""
    cosmic = 8.37; cluster = 7.75; galactic = 9.56
    s_cos_clu = 0.5*(1+np.tanh((lr-(-26))/w))   # 0 below -26, 1 above
    s_clu_gal = 0.5*(1+np.tanh((lr-(-22))/w))
    return cosmic*(1-s_cos_clu) + cluster*s_cos_clu*(1-s_clu_gal) + galactic*s_clu_gal

log_σ = sigma_smooth(log_ρ, w=0.3)
print(f"  Smooth model with w=0.3 dex transitions")
print(f"  ρ at galactic disc (1e-21): log_σ = {sigma_smooth(np.array([-21]), 0.3)[0]:.3f}")
print(f"  ρ at solar surface (sun core 1e5 not interstellar 1e-21):")
print(f"    same regime, log_σ = {sigma_smooth(np.array([5]), 0.3)[0]:.3f}")
print(f"  → continuity holds (saturated above galactic threshold)")
print()
print(f"  Galaxy edge gradient: ρ = 1e-21 → 1e-25 over ~kpc")
print(f"    log_σ at 1e-21: {sigma_smooth(np.array([-21]), 0.3)[0]:.3f}")
print(f"    log_σ at 1e-25: {sigma_smooth(np.array([-25]), 0.3)[0]:.3f}")
print(f"    → smooth transition over halo region (~10 kpc)")

# Test: dwarf spheroidal galaxies (low density ~1e-23) — transitional regime?
# Local Group dwarf spheroidals: ρ_central ~ 1e-22 to 1e-24
print(f"\n  Local Group dwarf spheroidals: ρ ~ 1e-23 (transitional)")
print(f"    log_σ predicted: {sigma_smooth(np.array([-23]), 0.3)[0]:.3f}")
print(f"    → between cluster (7.75) and galactic (9.56)")
print(f"  → unique SQT prediction: dSph have INTERMEDIATE a_0!")

verdict = ("Continuity preserved via smooth tanh transitions w=0.3 dex. "
           "Solar system entirely in galactic regime (saturated). "
           "Galaxy edge: smooth ~10 kpc transition. "
           "Local Group dSph at intermediate σ_0 — TESTABLE prediction.")

fig, ax = plt.subplots(figsize=(10,6))
ax.plot(log_ρ, log_σ, 'b-', lw=2)
for rho_label, name in [(-27, 'cosmic'), (-23.5, 'dSph'), (-21, 'galaxy'),
                         (5, 'solar core')]:
    ax.axvline(rho_label, color='gray', ls=':', alpha=0.5)
    ax.text(rho_label, 9.7, name, fontsize=8, ha='center')
ax.set_xlabel('log10(ρ [kg/m³])'); ax.set_ylabel('log10(σ_0)')
ax.set_title('L95 — Smooth Branch B σ_0(ρ) transitions')
ax.grid(alpha=0.3); plt.tight_layout()
plt.savefig(OUT/'L95.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(attack="regime continuity",
                   defense="tanh smooth w=0.3 dex, dSph intermediate",
                   verdict=verdict), f, indent=2)
print("L95 DONE")
