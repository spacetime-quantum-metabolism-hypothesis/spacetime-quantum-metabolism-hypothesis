#!/usr/bin/env python3
"""L188 — Re-examine: is monotonic really dead?"""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L188"); OUT.mkdir(parents=True,exist_ok=True)

print("L188 — Critical re-examination: monotonic σ_0(ρ) revisited")
# L67 conclusion: monotonic σ(ρ) cannot fit T17/T20/T22
# Because:
# - σ(cosmic) = 2.34e8 (low ρ)
# - σ(cluster) = 5.6e7  (mid ρ, LOWER than cosmic!)
# - σ(galactic) = 3.31e9 (high ρ)
# Non-monotonic in ρ

# But L187 showed within SPARC: smooth quadratic fits well
# So Branch B's 'non-monotonicity' depends on T20 cluster σ_0

# Reality check on T20 σ_0 = 5.6e7:
# This was extracted under specific assumption
# (σ_0(k) Lorentzian model, L48-L52)
# If different model used, σ_0(cluster) might differ

# Let me reconsider T20:
# σ_8 fit gave σ_0 ≈ 5.6e7 for cluster scale
# But this assumed σ_0(k) Lorentzian with k_t = 0.68 Mpc^-1
# Different model assumptions could give different σ_0(cluster)

# Specifically: if cluster σ_0 actually = σ_galactic (universal galactic-cosmic),
# then we need just 2 regimes (cosmic + galactic+cluster)
# AND fit could be MONOTONIC

# Re-examine with σ_cluster ≠ 5.6e7:
import numpy as np

# Three scenarios:
scenarios = {
    "Branch B (3-regime, original)": {
        "cosmic": 8.37, "cluster": 7.75, "galactic": 9.56,
        "monotonic": False, "k": 3,
    },
    "2-regime (cosmic, structure)": {
        "cosmic": 8.37, "cluster": 9.0, "galactic": 9.56,
        "monotonic": True, "k": 2,
    },
    "Smooth log: σ ∝ log(ρ)": {
        "cosmic": 8.5, "cluster": 9.0, "galactic": 9.5,
        "monotonic": True, "k": 2,
    },
}

# Comparing fit quality (chi^2 vs anchors with errors)
log_rho_anchors = np.array([-27, -23.5, -21])
target_log_sig = np.array([8.37, 7.75, 9.56])
errs = np.array([0.06, 0.06, 0.05])

print("\n  Scenario comparison (chi² to anchors with errors):")
for name, sc in scenarios.items():
    pred = np.array([sc['cosmic'], sc['cluster'], sc['galactic']])
    chi2 = np.sum(((target_log_sig - pred)/errs)**2)
    print(f"  {name:<40} chi² = {chi2:.2f}")

# The crux: if T20 σ_0 ≠ 5.6e7 (extracted with Branch B assumptions),
# could monotonic still work?
# This is INFINITE REGRESS: T20 σ assumes a model

# Honest:
print("\n  HONEST RECONSIDERATION:")
print("  - σ_T20 = 5.6e7 was extracted under specific σ_0(k) Lorentzian model")
print("  - σ_T17 = 2.34e8 from BAO fit assuming SQT framework")
print("  - σ_T22 = 3.31e9 from SPARC RC fit")
print("  - If model assumptions differ, σ values would differ")
print("  - Non-monotonicity depends on consistent extraction")
print()
print("  → Branch B's 'non-monotonic' status is MODEL-DEPENDENT")
print("  → Could be 'Bayesian evidence' for non-monotonicity weak if model assumptions")
print("    drive the σ extraction asymmetry")

# What would resolve this?
print("\n  Resolution requires:")
print("  - SAME extraction method for cosmic, cluster, galactic σ_0")
print("  - Direct measurement (not via assumption-laden chain)")
print("  - Future SKA + DESI DR3 will provide more direct probes")

verdict = ("Branch B 'non-monotonicity' depends on T17/T20/T22 σ_0 extractions, "
           "each using different model assumptions. Whether σ truly varies "
           "non-monotonically is MODEL-DEPENDENT. Honest paper text: "
           "'Monotonic alternatives cannot be definitively ruled out without "
           "consistent extraction methodology.'")

fig, ax = plt.subplots(figsize=(10,6))
log_rho_grid = np.linspace(-29, -19, 100)
def BB(lr):
    out = np.zeros_like(lr)
    out[lr < -25] = 8.37
    out[(lr >= -25) & (lr < -22)] = 7.75
    out[lr >= -22] = 9.56
    return out
def monotonic(lr):
    return 8.37 + 0.4 * (lr + 27)
ax.plot(log_rho_grid, BB(log_rho_grid), 'b-', lw=2, label='Branch B (3-regime)')
ax.plot(log_rho_grid, monotonic(log_rho_grid), 'g--', lw=2, label='Monotonic alternative')
ax.errorbar(log_rho_anchors, target_log_sig, yerr=errs, fmt='ko',
            markersize=10, capsize=5, label='Anchors (model-dependent)')
ax.set_xlabel('log10(ρ_m)'); ax.set_ylabel('log10(σ_0)')
ax.set_title('L188 — Branch B vs monotonic: model-dependent')
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout(); plt.savefig(OUT/'L188.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(scenarios=scenarios,
                   honest="non-monotonicity model-dependent",
                   verdict=verdict), f, indent=2)
print("L188 DONE")
