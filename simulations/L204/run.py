#!/usr/bin/env python3
"""L204 — Individual SPARC galaxy a_0 predictions vs Branch B."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L204"); OUT.mkdir(parents=True,exist_ok=True)

print("L204 — Individual SPARC galaxy a_0 predictions")
ROOT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis")
with open(ROOT / "results/L69/l69_step1_report.json") as f:
    step1 = json.load(f)

ROWS = step1['rows']

# Branch B prediction: σ_galactic = 10^9.56 → all galaxies same a_0_predicted
# Per galaxy a_0 from SPARC fit
log_a0_per = np.array([r['log_a0'] for r in ROWS])

# Branch B prediction: log_a0 = const = -10
log_a0_BB = -10.0  # MOND a_0
predicted_residual = log_a0_per - log_a0_BB

print(f"  N galaxies: {len(ROWS)}")
print(f"  Per-galaxy log_a0 distribution:")
print(f"    median = {np.median(log_a0_per):.3f}")
print(f"    std    = {np.std(log_a0_per):.3f} dex")
print(f"\n  Branch B prediction: log_a0 = {log_a0_BB:.3f} (universal)")
print(f"  Per-galaxy residuals from prediction:")
print(f"    median = {np.median(predicted_residual):.3f}")
print(f"    std    = {np.std(predicted_residual):.3f} dex")

# Test: how many galaxies are within ±0.3 dex (factor 2)?
within_factor2 = np.sum(np.abs(predicted_residual) < 0.3)
within_factor5 = np.sum(np.abs(predicted_residual) < 0.7)
print(f"\n  Galaxies within ±0.3 dex (factor 2): {within_factor2}/{len(ROWS)} ({100*within_factor2/len(ROWS):.0f}%)")
print(f"  Galaxies within ±0.7 dex (factor 5): {within_factor5}/{len(ROWS)} ({100*within_factor5/len(ROWS):.0f}%)")

# Identify outliers
outliers_high = [r for r in ROWS if r['log_a0'] - log_a0_BB > 0.7]
outliers_low = [r for r in ROWS if r['log_a0'] - log_a0_BB < -0.7]
print(f"\n  HIGH outliers (a_0 >> universal): {len(outliers_high)}")
if outliers_high[:5]:
    print(f"  Examples: " + ", ".join(o['name'] for o in outliers_high[:5]))
print(f"  LOW outliers (a_0 << universal): {len(outliers_low)}")
if outliers_low[:5]:
    print(f"  Examples: " + ", ".join(o['name'] for o in outliers_low[:5]))

# Quality vs residual
high_Q = [r for r in ROWS if r['Q'] == 1]
log_a0_Q1 = [r['log_a0'] for r in high_Q]
print(f"\n  Quality 1 only ({len(high_Q)} galaxies):")
print(f"    median = {np.median(log_a0_Q1):.3f}")
print(f"    std    = {np.std(log_a0_Q1):.3f} dex")

# Branch B robustness with high quality only
predicted_residual_Q1 = np.array(log_a0_Q1) - log_a0_BB
within_Q1 = np.sum(np.abs(predicted_residual_Q1) < 0.3)
print(f"  Q=1 within ±0.3 dex: {within_Q1}/{len(high_Q)} ({100*within_Q1/len(high_Q):.0f}%)")

verdict = (f"Branch B universal a_0 prediction: {within_factor2/len(ROWS)*100:.0f}% within factor 2, "
           f"{within_factor5/len(ROWS)*100:.0f}% within factor 5. "
           f"Q=1 high-quality: {within_Q1/len(high_Q)*100:.0f}% within factor 2. "
           f"Substantial individual scatter — Branch B is *aggregate* statement.")

fig, axes = plt.subplots(1, 2, figsize=(14,6))
axes[0].hist(log_a0_per, bins=30, alpha=0.7, color='tab:blue')
axes[0].axvline(log_a0_BB, color='red', ls='--', lw=2, label='Branch B prediction')
axes[0].axvline(np.median(log_a0_per), color='green', ls='-', label=f'Median {np.median(log_a0_per):.3f}')
axes[0].set_xlabel('log10(a_0) per galaxy')
axes[0].set_ylabel('N galaxies')
axes[0].set_title(f'L204 — Per-galaxy a_0 (n={len(ROWS)})')
axes[0].legend()

axes[1].hist(predicted_residual, bins=30, alpha=0.7, color='tab:purple')
axes[1].axvline(0, color='black', lw=2)
axes[1].axvline(-0.3, color='red', ls=':', label='factor 2')
axes[1].axvline(0.3, color='red', ls=':')
axes[1].set_xlabel('Residual log10(a_0) - prediction')
axes[1].set_title(f'Residuals: {within_factor2}/{len(ROWS)} within ±0.3 dex')
axes[1].legend()

plt.tight_layout(); plt.savefig(OUT/'L204.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(N=len(ROWS),
                   within_factor2=int(within_factor2),
                   within_factor5=int(within_factor5),
                   within_Q1=int(within_Q1),
                   median_log_a0=float(np.median(log_a0_per)),
                   std_log_a0=float(np.std(log_a0_per)),
                   verdict=verdict), f, indent=2)
print("L204 DONE")
