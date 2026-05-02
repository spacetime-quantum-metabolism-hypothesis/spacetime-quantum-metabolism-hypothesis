#!/usr/bin/env python3
"""L112 — Γ_0(t) physical origin attempt."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L112"); OUT.mkdir(parents=True,exist_ok=True)

print("L112 — Γ_0(t) physical origin candidates")

# Hypothesis A: Γ_0 ∝ H(t) (creation rate tied to Hubble rate)
#   Physical: 'each Hubble volume creates 1 quantum per τ_q'
#   ρ_Λ(t) = n_∞·ε/c² with n_∞(t) = Γ_0(t)·τ_q
#   If Γ_0 ∝ H, n_∞ ∝ H·τ_q ∝ H/H_0
#   ρ_Λ ∝ H → ρ_Λ varies as H(t)
#   But w_eff ≠ -1 in general

# Hypothesis B: Γ_0 ∝ ρ_critical(t)
#   Self-similar: Γ_0(t) = c · H(t)² / G (some normalization)
#   This gives ρ_Λ ∝ H², matching dark energy = ρ_critical pattern
#   But w_eff = -1 again (constant ρ_Λ/ρ_crit)

# Hypothesis C: Γ_0 has slow-roll component (quintessence-like)
#   Γ_0(t) = Γ_0_0 · exp(-α·H₀·t)  (slow decay)
#   This gives time-evolving DE with w(z)

# Hypothesis D: Γ_0 from horizon thermodynamics
#   Hawking-Gibbons rate: T·dS/dt at de Sitter horizon
#   T_dS = ℏH/(2πk_B), S_dS ∝ 1/H²
#   dS/dt ∝ -2H·Ḣ/H³ ~ -Ḣ/H
#   For decelerating universe (Ḣ<0): dS/dt > 0
#   This naturally gives time-dependent Γ_0

# Numerical comparison to L78 fit Γ_0(z)/Γ_0(0) = 1 + 0.077z - 0.085z²
# at z=0: 1
# at z=2: 1 + 0.154 - 0.34 = 0.814
# at z=1: 1 + 0.077 - 0.085 = 0.992
# Interpretation: Γ_0 was LOWER in past — opposite of expected (DE rho was lower earlier)

H0=73.8e3/3.086e22
def Gamma_h(z):
    return np.sqrt(0.315*(1+z)**3 + 0.685)  # H(z)/H_0
def Gamma_h2(z):
    return Gamma_h(z)**2  # ρ_critical(t)/ρ_crit_0

zs = np.linspace(0, 3, 50)
print("\n  Hypothesis A (Γ_0 ∝ H):")
for z in [0, 0.5, 1, 2]:
    print(f"    z={z}: ratio = {Gamma_h(z):.3f}")
print("  Predicts: Γ_0 LARGER in past (since H bigger)")
print("  But L78 fit shows Γ_0 SMALLER in past!")
print("  → Hypothesis A WRONG sign")
print()
print("  Hypothesis B (Γ_0 ∝ H²):")
for z in [0, 0.5, 1, 2]:
    print(f"    z={z}: ratio = {Gamma_h2(z):.3f}")
print("  Same problem as A — wrong sign")
print()
print("  Hypothesis C (slow decay): Γ_0(z) = exp(α(1-1/(1+z)))")
print(f"    α=2: at z=2 ratio = {np.exp(2*(2/3)):.3f}")
print("  Predicts: Γ_0 LARGER in past — wrong sign")
print()
print("  → All natural hypotheses give Γ_0(past) > Γ_0(now)")
print("  → L78 fit Γ_0(past) < Γ_0(now) is COUNTERINTUITIVE")
print("  → DESI w_a<0 (DE WEAKER in past) requires UNUSUAL Γ_0(t)")
print()
print("  Possible interpretation:")
print("  Γ_0 isn't time-dependent; rather τ_q or ε is.")
print("  Or: SQT REJECTS DESI w_a<0 result.")

# Honest: SQT naturally predicts Γ_0(past) > Γ_0(now) (more cosmic creation when H higher)
# This would give ρ_Λ(past) > ρ_Λ(now) → w_a > 0 (phantom-like)
# Opposite of DESI!
# So SQT may actually CONFLICT with DESI evolution if Γ_0 is physical

verdict = ("All natural Γ_0(t) hypotheses (∝H, ∝H², slow decay) give Γ_0(past) > Γ_0(now), "
           "which predicts ρ_Λ(past) > ρ_Λ(now) → w_a > 0 (phantom-like). "
           "This is OPPOSITE to DESI w_a<0 finding! "
           "SQT may either: (a) REJECT DESI evolution (await DR3 confirmation), "
           "(b) require non-trivial τ_q(t) or ε(t) variation.")

fig, ax = plt.subplots(figsize=(10,6))
zs_plot = np.linspace(0, 3, 100)
ax.plot(zs_plot, np.full_like(zs_plot, 1), 'k-', label='constant Γ_0')
ax.plot(zs_plot, Gamma_h(zs_plot), 'b-', label='Γ_0 ∝ H(z)')
ax.plot(zs_plot, Gamma_h2(zs_plot), 'g-', label='Γ_0 ∝ H²(z)')
ax.plot(zs_plot, 1 + 0.077*zs_plot - 0.085*zs_plot**2, 'r--', label='L78 fit (DESI)')
ax.set_xlabel('z'); ax.set_ylabel('Γ_0(z)/Γ_0(0)')
ax.set_title('L112 — Γ_0(z) candidates vs DESI requirement')
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout(); plt.savefig(OUT/'L112.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(natural_predictions="Γ_0(past) > Γ_0(now)",
                   DESI_requires="Γ_0(past) < Γ_0(now)",
                   conflict=True,
                   verdict=verdict), f, indent=2)
print("L112 DONE")
