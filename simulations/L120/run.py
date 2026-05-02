#!/usr/bin/env python3
"""L120 — Most decisive single test for SQT."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L120"); OUT.mkdir(parents=True,exist_ok=True)

print("L120 — Most decisive single SQT test")
# Rank 14 unique predictions by:
# - Distinctness from alternatives (MOND, LCDM, Verlinde, AQUAL)
# - Detection feasibility (5-10 years)
# - Magnitude of effect

predictions_rank = [
    # name, distinctness, feasibility, magnitude_effect, total_score
    ("P3 quantum depletion (MICROSCOPE-2)", 5, 4, 1, 10),  # tiny effect
    ("P7 a_0(z) = c·H_0(z)/(2π) [SKA]", 5, 4, 5, 14),  # large at z=2
    ("G2 a_0(disc)/a_0(spheroid) = 2 (revised L115)", 5, 4, 4, 13),
    ("P13 Void galaxy a_0 ~ 7%", 5, 3, 5, 13),
    ("P14 Halo shape = baryon shape", 4, 4, 3, 11),
    ("P9 dSph intermediate σ_0", 4, 4, 3, 11),
    ("P1 σ_0 regime structure (cluster lensing)", 3, 5, 4, 12),
    ("P2 DESI w_a (Γ_0(t))", 2, 5, 3, 10),  # currently conflicts
    ("P6 galactic intrinsic scatter", 3, 5, 2, 10),
    ("P4 GW absorption (ET/CE)", 3, 3, 2, 8),
    ("P5 BBN constraint", 2, 5, 2, 9),
    ("P8 Σ_0 modified BTFR slope variation", 4, 4, 3, 11),
]
predictions_rank.sort(key=lambda x: -x[4])
print("\n  RANKING (max score = 15):")
for name, dist, feas, mag, total in predictions_rank:
    print(f"  {total:2d} | {name}")

# TOP picks:
# #1: P7 a_0(z) — large effect (factor 3 at z=2), SKA testable, distinct from MOND
# #2: G2 (revised) — factor 2 disc/spheroidal, ATLAS-3D testable
# #3: P13 void galaxy — factor 14 reduction, void surveys

print("\n  TOP 3 most decisive tests:")
print("  1. P7 a_0(z=2)/a_0(0) = 3.03 vs MOND constant — SKA z>1 RC (~2028-2030)")
print("     If SQT correct: factor 3 effect, easily distinguishable")
print("     If MOND correct: SQT REJECTED")
print()
print("  2. G2 (revised L115): a_0(disc)/a_0(spheroid) = 2 — ATLAS-3D (~2025-2030)")
print("     If SQT correct: factor 2 difference, detectable")
print("     If universal: SQT G2 REJECTED, but Branch B can survive")
print()
print("  3. P13 void galaxy a_0 ~ 7% — void galaxy surveys (~2027-2030)")
print("     If confirmed: SQT regime structure VINDICATED")
print("     If not: SQT regime structure WEAKENED")

# Most decisive single: P7 a_0(z) — yields strongest distinction in shortest time
verdict = ("MOST DECISIVE SINGLE TEST: P7 a_0(z=2)/a_0(0) = 3.03 (SKA, ~2028-2030). "
           "Factor 3 effect, completely distinct from MOND universal. "
           "PASS or FAIL determines SQT fate. "
           "Backup: G2 revised (factor 2), void galaxy (factor 14).")

fig, ax = plt.subplots(figsize=(12,7))
names = [p[0][:35] for p in predictions_rank]
scores = [p[4] for p in predictions_rank]
colors_p = ['green' if s >= 12 else ('orange' if s >= 10 else 'red') for s in scores]
ax.barh(names, scores, color=colors_p, alpha=0.7)
ax.axvline(12, color='black', ls='--', label='Top tier threshold')
ax.set_xlabel('Distinctness score (max 15)')
ax.set_title('L120 — Decisive test ranking')
ax.legend(); plt.tight_layout()
plt.savefig(OUT/'L120.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(top_tests=[p[0] for p in predictions_rank[:3]],
                   decisive_test="P7 a_0(z=2)/a_0(0) = 3.03 via SKA",
                   verdict=verdict), f, indent=2)
print("L120 DONE")
