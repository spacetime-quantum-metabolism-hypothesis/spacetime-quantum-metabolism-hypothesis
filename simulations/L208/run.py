#!/usr/bin/env python3
"""L208 — Joint Branch B vs LCDM chi^2 head-to-head."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L208"); OUT.mkdir(parents=True,exist_ok=True)
ROOT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis")

print("L208 — Joint chi^2 Branch B vs LCDM (SPARC + 3 anchors)")
with open(ROOT/"results/L69/l69_step1_report.json") as f:
    step1 = json.load(f)
ROWS = step1['rows']
log_a0 = np.array([r['log_a0'] for r in ROWS])
log_a0_err = 0.1  # typical SPARC log_a0 uncertainty

# Anchor points (Branch B 3 regimes)
# (log_sigma, log_sigma_err, regime_name)
anchors = [
    (8.37, 0.10, 'cosmic'),
    (7.75, 0.20, 'cluster'),
    (9.56, 0.10, 'galactic'),
]

# Branch B prediction: 3 distinct sigma_0 values
# LCDM: NO sigma_0 prediction (no anchors)
# Comparison: Branch B has theory-predicted sigma_0 at each regime
# LCDM proxy: a single sigma_0 universal? Or no prediction at all?
# Standard MOND: a_0 = 1.2e-10 m/s^2, log_a0 = -10.0 universal

# SPARC chi^2 against universal a_0 = -10.0
log_a0_universal = -10.0
chi2_sparc_universal = np.sum((log_a0 - log_a0_universal)**2 / log_a0_err**2)

# Branch B SPARC: same universal log_a0 = -10.0 (galactic regime)
chi2_sparc_BB = chi2_sparc_universal  # same prediction at galactic regime

# Anchor chi^2: Branch B 3 separate predictions; LCDM has no anchor predictions
# So anchors: Branch B chi^2 = 0 (predictions match observations by construction)
# To be fair: assume sigma_0 measured with quoted errors, BB *predicts* (a3,a6 + D5)
# LCDM has no theory prediction for sigma_0 — count as N anchors all with prediction = mean

# More fair: count chi^2 per dataset
sigma_obs = np.array([a[0] for a in anchors])
sigma_err = np.array([a[1] for a in anchors])

# Branch B prediction matches by construction (3 params, 3 anchors → chi^2 = 0)
chi2_anchor_BB = 0.0
k_BB = 3  # 3 sigma values

# LCDM: 0 prediction → can fit single sigma; with single param, chi^2 = sum((s_i - s_mean)^2/sigma^2)
sigma_mean = np.average(sigma_obs, weights=1/sigma_err**2)
chi2_anchor_LCDM = np.sum((sigma_obs - sigma_mean)**2 / sigma_err**2)
k_LCDM = 1

N_total = len(ROWS) + 3
chi2_total_BB = chi2_sparc_BB + chi2_anchor_BB
chi2_total_LCDM = chi2_sparc_universal + chi2_anchor_LCDM

# AICc
def aicc(chi2, k, N):
    return chi2 + 2*k + 2*k*(k+1)/(N-k-1)

aicc_BB = aicc(chi2_total_BB, k_BB, N_total)
aicc_LCDM = aicc(chi2_total_LCDM, k_LCDM, N_total)

print(f"  N SPARC galaxies: {len(ROWS)}")
print(f"  N anchors: 3")
print(f"  N total: {N_total}")
print(f"\n  SPARC chi^2 (universal a_0=-10):")
print(f"    Branch B = {chi2_sparc_BB:.2f}")
print(f"    LCDM     = {chi2_sparc_universal:.2f}")
print(f"\n  Anchor chi^2:")
print(f"    Branch B = {chi2_anchor_BB:.2f} (3 regimes by construction)")
print(f"    LCDM     = {chi2_anchor_LCDM:.2f} (1 universal sigma)")
print(f"\n  Total chi^2:")
print(f"    Branch B = {chi2_total_BB:.2f} (k={k_BB})")
print(f"    LCDM     = {chi2_total_LCDM:.2f} (k={k_LCDM})")
print(f"\n  AICc:")
print(f"    Branch B = {aicc_BB:.2f}")
print(f"    LCDM     = {aicc_LCDM:.2f}")
print(f"  ΔAICc(LCDM-BB) = {aicc_LCDM - aicc_BB:.2f}")

# Honest critique: this comparison FAVORS BB structurally because anchors are exactly the regime points
# Real test would need INDEPENDENT data with 3 regimes
print(f"\n  HONEST CAVEAT:")
print(f"    Branch B has 3 free params at exactly 3 anchors — overfit risk.")
print(f"    True test: independent data per regime.")

verdict = (f"Branch B vs LCDM: dchi2_total = {chi2_total_LCDM - chi2_total_BB:.2f}, dAICc = {aicc_LCDM - aicc_BB:.2f}. "
           f"Branch B preferred by {(chi2_total_LCDM - chi2_total_BB):.1f} chi^2 units. "
           f"CAVEAT: anchors are by-construction match — independent regime data needed.")

fig, ax = plt.subplots(figsize=(10,6))
labels = ['SPARC 175', 'Anchors (3)', 'Total', 'AICc']
BB_vals = [chi2_sparc_BB, chi2_anchor_BB, chi2_total_BB, aicc_BB]
LCDM_vals = [chi2_sparc_universal, chi2_anchor_LCDM, chi2_total_LCDM, aicc_LCDM]
x = np.arange(len(labels)); w=0.35
ax.bar(x-w/2, BB_vals, w, label='Branch B', color='tab:blue')
ax.bar(x+w/2, LCDM_vals, w, label='LCDM (universal)', color='tab:red')
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylabel('chi^2 / AICc'); ax.legend(); ax.set_yscale('log')
ax.set_title('L208 — Joint chi^2 Branch B vs LCDM')
plt.tight_layout(); plt.savefig(OUT/'L208.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(N_sparc=len(ROWS), N_anchors=3,
                   chi2_sparc_BB=float(chi2_sparc_BB),
                   chi2_sparc_LCDM=float(chi2_sparc_universal),
                   chi2_anchor_BB=float(chi2_anchor_BB),
                   chi2_anchor_LCDM=float(chi2_anchor_LCDM),
                   chi2_total_BB=float(chi2_total_BB),
                   chi2_total_LCDM=float(chi2_total_LCDM),
                   aicc_BB=float(aicc_BB), aicc_LCDM=float(aicc_LCDM),
                   delta_aicc=float(aicc_LCDM-aicc_BB),
                   verdict=verdict), f, indent=2)
print("L208 DONE")
