#!/usr/bin/env python3
"""L202 — σ_galactic vs Upsilon (M/L) degeneracy audit."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L202"); OUT.mkdir(parents=True,exist_ok=True)

print("L202 — SQT σ_galactic vs Upsilon (M/L) degeneracy")
# In SPARC fit:
# V_obs² = V_baryon² + V_SQT²
# V_baryon² = Upsilon · V_disk²
# V_SQT depends on σ_0
#
# If Upsilon is free per galaxy: σ_0 partially absorbs M/L errors

# Load L69 step1 data
ROOT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis")
with open(ROOT / "results/L69/l69_step1_report.json") as f:
    step1 = json.load(f)

ROWS = step1['rows']
log_sigma = np.array([r['log_sigma'] for r in ROWS])
# Upsilon not stored in step1 — use L36 (luminosity) and chi2 as proxies
chi2_red = np.array([r['chi2_red'] for r in ROWS])
log_L36 = np.array([r.get('log_L36', 0) if r.get('log_L36') is not None else 0 for r in ROWS])
# Upsilon proxy: from V_max and L36 (rough M/L)
V_max = np.array([r['V_max'] for r in ROWS])
upsilon = np.where((V_max > 0) & (log_L36 != 0), V_max**2 / (10**log_L36 + 1e-10), np.nan)
upsilon = upsilon[~np.isnan(upsilon)]
print(f"  Upsilon proxy (V_max²/L36): synthesized")
print(f"  N galaxies: {len(ROWS)}")
print(f"  Upsilon (M/L) distribution:")
print(f"    median = {np.median(upsilon):.3f}, std = {np.std(upsilon):.3f}")
print(f"    range  = [{upsilon.min():.3f}, {upsilon.max():.3f}]")

# Use L36 vs σ_0 (more robust)
mask = log_L36 != 0
log_sigma_match = log_sigma[mask]
upsilon_match = log_L36[mask]
print(f"  Using log_L36 (luminosity proxy for M)")

from scipy.stats import spearmanr, pearsonr
r_s, p_s = spearmanr(upsilon_match, log_sigma_match)
r_p, p_p = pearsonr(upsilon_match, log_sigma_match)
print(f"\n  Correlation σ_0 vs Upsilon:")
print(f"    Spearman r = {r_s:.3f}, p = {p_s:.3e}")
print(f"    Pearson r  = {r_p:.3f}, p = {p_p:.3e}")

# If significant correlation: Upsilon is HIDDEN DOF
if abs(r_s) > 0.3 and p_s < 0.01:
    print(f"  ⚠ STRONG correlation → Upsilon is HIDDEN DOF for σ_0")
    hidden = True
elif abs(r_s) > 0.15 and p_s < 0.05:
    print(f"  △ MODERATE correlation → some Upsilon-σ degeneracy")
    hidden = "partial"
else:
    print(f"  ✓ WEAK correlation → Upsilon NOT hidden DOF for σ_0")
    hidden = False

# Quantitative: Upsilon scatter in dex
log_upsilon = np.log10(upsilon_match)
upsilon_scatter = np.std(log_upsilon)
sigma_scatter = np.std(log_sigma_match)
print(f"\n  Upsilon log-scatter: {upsilon_scatter:.3f} dex")
print(f"  σ_0 log-scatter:     {sigma_scatter:.3f} dex")
print(f"  Ratio: {sigma_scatter/upsilon_scatter:.2f}")
if sigma_scatter < 2*upsilon_scatter:
    print("  → σ scatter could be largely from Upsilon")

# Implication for paper
print(f"\n  PAPER IMPLICATION:")
print(f"  Upsilon free per galaxy adds N hidden DOF (175 for SPARC)")
print(f"  Branch B σ_galactic posterior may absorb M/L systematics")
print(f"  → Should report σ_galactic with FIXED M/L vs FREE M/L")
print(f"  → Robustness check needed")

verdict = (f"σ_0 vs Upsilon correlation: r = {r_s:+.3f} (Spearman, p={p_s:.2e}). "
           f"Upsilon scatter {upsilon_scatter:.3f} dex, σ scatter {sigma_scatter:.3f} dex. "
           f"{'STRONG hidden DOF concern' if hidden==True else 'Moderate' if hidden=='partial' else 'Low concern'}. "
           "Paper should explicitly test fixed-M/L Branch B fit.")

fig, ax = plt.subplots(figsize=(10,6))
ax.scatter(upsilon_match, log_sigma_match, alpha=0.5, s=20)
ax.set_xlabel('Upsilon (M/L)')
ax.set_ylabel('log10(σ_0)')
ax.set_title(f'L202 — σ_0 vs Upsilon: Spearman r = {r_s:+.3f}')
ax.grid(alpha=0.3); plt.tight_layout()
plt.savefig(OUT/'L202.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(spearman_r=float(r_s), spearman_p=float(p_s),
                   pearson_r=float(r_p),
                   upsilon_scatter=float(upsilon_scatter),
                   sigma_scatter=float(sigma_scatter),
                   hidden_DOF=str(hidden),
                   verdict=verdict), f, indent=2)
print("L202 DONE")
