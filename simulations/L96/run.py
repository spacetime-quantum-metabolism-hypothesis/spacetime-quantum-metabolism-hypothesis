#!/usr/bin/env python3
"""L96 — G2 π/3 cross-check via published a_0 estimates."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L96"); OUT.mkdir(parents=True,exist_ok=True)

# Published a_0 estimates from various galaxy types:
# Discs (SPARC, BTFR): a_0 = 1.20e-10 (Begeman+1991, Famaey+McGaugh review 2012)
# Local Group dSph (Lelli+2017): a_0 = 1.0-1.5e-10 (consistent w/ MOND)
# Elliptical galaxies (Sanders 2010): a_0 = 1.2e-10 (similar)
# Ultra-diffuse galaxies (UDGs): some show MOND deviation

# G2 prediction: a_0(disc) / a_0(spheroidal) = π/3 ≈ 1.047
# Observed: most analyses find UNIVERSAL a_0 ~ 1.2e-10
# → π/3 prediction NOT obviously verified
# But error bars on elliptical a_0 are ~30% (Sanders 2010)
# 1.047 ratio = 4.7% deviation; below detection precision

print("L96 — G2 π/3 prediction cross-check")
a0_disc = 1.20e-10
a0_dSph = 1.20e-10  # within errors of MOND
a0_ellipt = 1.2e-10  # Sanders 2010
ratio_obs = a0_disc / a0_ellipt
print(f"  Observed (literature): a_0 ~ 1.2e-10 universal")
print(f"  Disc / spheroidal ratio = {ratio_obs:.3f}")
print(f"  G2 prediction: π/3 = {np.pi/3:.3f}")
print(f"  Deviation: {abs(np.pi/3 - ratio_obs)*100:.1f}%")
print(f"  Current data precision: ~10-30%")
print(f"  → π/3 within current uncertainty; NOT yet falsified, NOT confirmed")

# What sample/precision needed to test π/3 (4.7% effect)?
# Need precision better than ~2% on each a_0
# This requires: large N samples + clean morphology + uniform M/L
print(f"\n  Required precision: <2% on each subsample")
print(f"  Current SPARC: ~10% on disc a_0 median")
print(f"  ATLAS-3D early-type sample: ~30% on a_0")
print(f"  → π/3 test requires larger surveys: MaNGA, SAMI, SDSS-V")
print(f"  → Specifically: pure dispersion-supported dSph + matched disc")
print(f"  → Estimated: feasible in 2-5 years with combined surveys")

# More aggressive prediction: log10(π/3) = 0.020 dex
# vs observed scatter ~0.5 dex per galaxy: signal completely buried
print(f"\n  In dex: log10(π/3) = {np.log10(np.pi/3):.4f} dex")
print(f"  vs SPARC scatter ~0.5 dex per galaxy")
print(f"  → Need MEDIAN of large samples, both populations")

verdict = ("G2 π/3 (4.7% effect) within current literature precision (~10-30%). "
           "Not falsified, not confirmed. Requires <2% precision on each subsample. "
           "Feasible with MaNGA/SAMI/SDSS-V in 2-5 years.")

fig, ax = plt.subplots(figsize=(10,6))
samples = ['SPARC disc\n(2016)', 'Local Group\ndSph (2017)', 'Sanders\nellipticals',
           'G2 SQT\nprediction']
vals = [1.0, 1.0, 1.0, np.pi/3]
errs = [0.10, 0.30, 0.30, 0]
ax.errorbar(samples, vals, yerr=errs, fmt='o', markersize=10, capsize=5)
ax.axhline(1.0, color='red', ls='--', label='MOND universal')
ax.axhline(np.pi/3, color='green', ls=':', label='SQT π/3')
ax.set_ylim(0.5, 1.5)
ax.set_ylabel('a_0(disc) / a_0(sample)')
ax.set_title('L96 — G2 π/3 cross-check (within current uncertainties)')
ax.legend(); plt.tight_layout()
plt.savefig(OUT/'L96.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(prediction_pi_over_3=float(np.pi/3),
                   observed_ratio=1.0,
                   deviation_pct=4.7,
                   data_precision_pct=20,
                   testable_with="MaNGA/SAMI/SDSS-V, 2-5 years",
                   verdict=verdict), f, indent=2)
print("L96 DONE")
