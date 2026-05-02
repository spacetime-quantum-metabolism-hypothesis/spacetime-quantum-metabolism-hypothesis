#!/usr/bin/env python3
"""L186 — What would falsify Branch B specifically?"""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L186"); OUT.mkdir(parents=True,exist_ok=True)

print("L186 — Branch B falsifiability: what discriminates from alternatives?")

# Alternative regime structures:
alternatives = {
    'Branch B (3-regime, discrete)': "current SQT, 3 σ_0 values",
    '2-regime (cosmic, structure)': "cosmic + galactic only (cluster=galactic)",
    '4-regime': "additional regime at NS density",
    'Smooth power law σ ~ ρ^α': "monotonic, single power",
    'Smooth log function': "σ = a + b·log(ρ)",
    'Sigmoid (single transition)': "two values smoothly connected",
    'Random per-galaxy': "no regime structure, just scatter",
}

print("\nAlternative σ_0(env) structures:")
for k, v in alternatives.items():
    print(f"  {k}: {v}")

# Falsification tests
print("\n\nFalsification tests for Branch B specifically:")
falsify_tests = [
    ("dSph at intermediate ρ ~ 1e-23",
     "Branch B: σ ~ σ_cluster ≈ 10^7.75",
     "Smooth: σ ~ interpolated value (10^8 to 9)",
     "Discriminates if measurement σ within 0.3 dex"),
    ("Galaxy disk transitions to halo",
     "Branch B: sharp σ change at ρ_c2",
     "Smooth: gradual change",
     "RC outer parts probe transition"),
    ("Cluster + galaxy in same z bin (Tully-Fisher)",
     "Branch B: distinct σ in each environment",
     "Smooth: continuous a_0 evolution",
     "Future surveys with mass-stratification"),
    ("Cosmic acceleration of voids",
     "Branch B: void σ = σ_cosmic",
     "Smooth: void σ slightly < normal",
     "Future void galaxy surveys"),
    ("σ_0 in very low surface brightness galaxies",
     "Branch B: σ = σ_galactic (galactic regime)",
     "Smooth: σ depends on local ρ",
     "Existing SPARC LSB data + dwarfs"),
]
for test, BB, smooth, disc in falsify_tests:
    print(f"\n  TEST: {test}")
    print(f"    Branch B says: {BB}")
    print(f"    Smooth says:   {smooth}")
    print(f"    Discriminator: {disc}")

# Quantitative falsification criterion
print("\n\nQUANTITATIVE FALSIFICATION CRITERIA:")
print("Branch B falsified if:")
print("1. dSph σ_0 ≠ σ_cluster within 0.3 dex (rules out 3-regime, favors smooth)")
print("2. SPARC σ_0 vs ρ shows continuous trend (rules out discrete regimes)")
print("3. Void galaxy σ_0 = σ_galactic (no cosmic regime distinct)")
print("4. Cluster M-σ relation no SQT signature (full DM-particle world)")

# Honest: no current data falsifies Branch B
# But Branch B is also not UNIQUELY supported
# Multiple alternatives consistent with current data
print("\nHONEST CURRENT STATUS:")
print("Existing data CONSISTENT with both:")
print("- Branch B (3-regime discrete)")
print("- Smooth σ_0(ρ) with 3 'inflection points'")
print("- 4-regime with 4th at NS density")
print()
print("Future data will discriminate.")
print("Currently: Branch B is ONE plausible structure among several.")

verdict = ("Branch B falsifiability is moderate. Currently consistent but not "
           "uniquely supported by data. Future tests at intermediate density "
           "(dSph, void galaxies) will discriminate Branch B from smooth "
           "alternatives. Honest paper text: 'Branch B is one of several "
           "consistent regime structures.'")

fig, ax = plt.subplots(figsize=(10,6))
log_rho = np.linspace(-30, -18, 100)
# Branch B (discrete steps)
def BranchB(lr):
    out = np.zeros_like(lr)
    out[lr < -25] = 8.37
    out[(lr >= -25) & (lr < -22)] = 7.75
    out[lr >= -22] = 9.56
    return out
# Smooth alternative
def smooth(lr, a=8.5, b=0.5, c=-0.05):
    return a + b * (lr + 24)**2 / 100 - c * (lr + 24)
# 4-regime (Branch B + 4th at high ρ)
def Branch4(lr):
    out = BranchB(lr)
    out[lr >= -10] = 11   # 4th regime at NS-like
    return out

ax.plot(log_rho, BranchB(log_rho), 'b-', lw=2, label='Branch B (3-regime)')
ax.plot(log_rho, smooth(log_rho), 'g--', lw=2, label='Smooth alternative')
ax.scatter([-23.5], [7.75], color='red', s=200, marker='*', zorder=5,
           label='dSph FALSIFIER (intermediate)')
ax.set_xlabel('log10(ρ_m)'); ax.set_ylabel('log10(σ_0)')
ax.set_title('L186 — Branch B vs alternatives: dSph as falsifier')
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout(); plt.savefig(OUT/'L186.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(attack="What falsifies Branch B?",
                   alternatives=alternatives,
                   tests=falsify_tests,
                   verdict=verdict), f, indent=2)
print("L186 DONE")
