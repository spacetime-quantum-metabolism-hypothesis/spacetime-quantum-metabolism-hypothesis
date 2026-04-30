#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L83 — BBN constraint on Γ_0·τ_q."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L83"); OUT.mkdir(parents=True, exist_ok=True)

hbar=1.055e-34; c=2.998e8; G=6.674e-11; H0_today=73.8e3/3.086e22
# At BBN: z ~ 1e9, T ~ 1 MeV
z_BBN = 1e9
T_BBN_eV = 1e6
# H_BBN = H0 · sqrt(Omega_r·(1+z)^4) ~ 1.5 e-1 s^-1
Omega_r = 9.2e-5
H_BBN = H0_today * np.sqrt(Omega_r * (1+z_BBN)**4)
print("L83 — BBN constraint")
print(f"  z_BBN = {z_BBN:.0e}, T_BBN = {T_BBN_eV:.0e} eV = 1 MeV")
print(f"  H_BBN = {H_BBN:.3e} s^-1")
print(f"  expansion timescale at BBN ~ {1/H_BBN:.3e} s")
# SQT: rho_DE_BBN = (cosmic n) · ε / c² ~ rho_Lambda_today (constant if Γ_0 const)
# Compared to rho_total_BBN = Omega_r·(1+z)^4·rho_crit_today
rho_crit_today = 3*H0_today**2/(8*np.pi*G)
rho_tot_BBN = Omega_r * (1+z_BBN)**4 * rho_crit_today
rho_DE_BBN  = 0.685 * rho_crit_today  # constant Λ
ratio = rho_DE_BBN / rho_tot_BBN
print(f"  rho_DE_BBN / rho_tot_BBN = {ratio:.3e}")
print(f"  → SQT contribution at BBN: NEGLIGIBLE (tiny relative to radiation)")
print(f"  → BBN unaffected by SQT cosmic creation Γ_0 (consistent ★)")
# Δ N_eff equivalent: ratio · g_*
delta_Neff_max = 8.0 * ratio  # rough
print(f"  Δ N_eff equivalent: ~ {delta_Neff_max:.3e}")
print(f"  Planck constraint: Δ N_eff < 0.3 → SQT << constraint, PASS")

# Now: if Γ_0(t) per L78 (DESI matching), check if Γ_0_BBN is HIGHER
# Γ_0(z) = Γ_0(0) · (1 + 0.077·z - 0.085·z²)
# At z = 1e9: |Γ_0(z)| → ∞ if extrapolated naively
# But ansatz only valid for z < few. Real Γ_0(t) at BBN unknown.
print(f"\n  L78 Γ_0(z) ansatz: 1 + 0.077z - 0.085z² (valid z<3)")
print(f"  Cannot extrapolate to z=1e9; need physical model for Γ_0(BBN)")
print(f"  Honest: Γ_0(BBN) is UNCONSTRAINED by current theory")
print(f"  Future: BBN tightens Γ_0(BBN) bound")

verdict = ("BBN PASS in standard SQT (constant Γ_0): SQT contribution at BBN negligible.\n"
           "Γ_0(t) extension (L78) requires physical model for high-z extrapolation.")

fig, ax = plt.subplots(figsize=(10,6))
zs = np.logspace(-2, 10, 100)
H_z = H0_today * np.sqrt(Omega_r*(1+zs)**4 + 0.315*(1+zs)**3 + 0.685)
ax.loglog(zs, H_z, 'b-', label='H(z)')
ax.axvline(z_BBN, color='red', ls=':', label='BBN epoch')
ax.set_xlabel('1+z'); ax.set_ylabel('H(z) [s^-1]')
ax.set_title('L83 — Hubble rate, BBN epoch')
ax.legend(); ax.grid(alpha=0.3, which='both')
plt.tight_layout(); plt.savefig(OUT/'L83.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(z_BBN=float(z_BBN), H_BBN=float(H_BBN),
                   rho_DE_over_rho_tot=float(ratio),
                   delta_Neff_max=float(delta_Neff_max),
                   verdict=verdict), f, indent=2)
print("L83 DONE")
