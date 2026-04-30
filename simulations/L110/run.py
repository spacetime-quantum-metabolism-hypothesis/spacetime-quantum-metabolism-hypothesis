#!/usr/bin/env python3
"""L110 — DM halo triaxiality vs SQT scalar field."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L110"); OUT.mkdir(parents=True,exist_ok=True)

print("L110 — DM halo triaxiality vs SQT scalar n")
# Observation: galaxy halos triaxial (axis ratios b/a ~ 0.7, c/a ~ 0.5)
# Simulation: cold DM produces triaxial halos via gravitational collapse
# SQT: n is scalar, no preferred direction
# Question: can SQT alone produce triaxial 'effective DM' halo?

# In SQT: n depleted in regions of high baryonic ρ
# Depletion follows BARYON distribution shape
# Galaxy disc → baryons in disc → n depleted in disc plane more
# This IS anisotropic (matches baryon shape)
# So effective gravity profile follows baryons → naturally triaxial

# Quantitative:
# n_local(x,y,z) = Γ_0·τ_q / (1 + σ·ρ_baryon(x,y,z)·τ_q/(1+something))
# Steady state: n_local ∝ 1/ρ_baryon (high ρ → low n)
# Effective gravity contribution: σ·n·ρ ~ σ·(Γ_0·τ_q/[1+σ·ρ·τ_q]^n)·ρ
# If σ·ρ·τ_q >> 1 (galactic): saturated, contribution constant
# If σ·ρ·τ_q << 1 (cluster, void): linear in ρ

# SQT in cluster regime gives EFFECTIVE 'DM-like' contribution
# Profile follows baryons → SQT halo triaxiality FROM BARYON shape
# Standard CDM halos: triaxial INDEPENDENTLY of baryons (collisionless DM)

# These differ:
# - CDM halos: triaxial even for spherical baryon distribution
# - SQT 'halo': follows baryon distribution

# Test: spherical galaxy with stripped gas — CDM still triaxial, SQT spherical
# Observation: not currently distinguishing
print("  Halo triaxiality observation: b/a~0.7, c/a~0.5")
print()
print("  CDM prediction: triaxial INDEPENDENT of baryon shape")
print("  SQT prediction: 'halo' FOLLOWS baryon distribution shape")
print("  → Different predictions for stripped/spherical baryon systems")
print()
print("  Falsification test: galaxies with severely stripped baryons")
print("  CDM: halo retains triaxiality")
print("  SQT: halo becomes spherical (matches baryons)")
print("  → Future surveys can distinguish")

verdict = ("SQT 'halo' follows baryon shape (depletion zones). "
           "CDM halos triaxial regardless. "
           "DIFFERENT predictions for stripped systems. "
           "Currently NOT distinguishing data — future test possible.")

fig, ax = plt.subplots(figsize=(10,6))
ax.set_aspect('equal')
# Schematic: CDM halo triaxial; SQT depleted following galaxy disk
theta = np.linspace(0, 2*np.pi, 100)
# CDM ellipse
ax.plot(2*np.cos(theta), 1.4*np.sin(theta), 'b-', lw=2, label='CDM halo (triaxial)')
# SQT 'halo' follows disc baryon
ax.plot(2.0*np.cos(theta), 0.5*np.sin(theta), 'r--', lw=2, label='SQT depletion (disc-shaped)')
# disc baryon
ax.fill(1.5*np.cos(theta), 0.3*np.sin(theta), alpha=0.3, color='green', label='Baryon disc')
ax.set_xlim(-3, 3); ax.set_ylim(-2, 2)
ax.set_title('L110 — Halo shape: CDM (triaxial) vs SQT (baryon-shaped)')
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout(); plt.savefig(OUT/'L110.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(SQT_halo_shape="follows baryon",
                   CDM_halo_shape="triaxial independent",
                   distinguishing_test="stripped baryon galaxies",
                   verdict=verdict), f, indent=2)
print("L110 DONE")
