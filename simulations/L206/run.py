#!/usr/bin/env python3
"""L206 — Branch B σ_8(z) prediction via regime-modulated G_eff."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
from scipy.integrate import odeint
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L206"); OUT.mkdir(parents=True,exist_ok=True)

print("L206 — Branch B sigma_8(z) prediction")

# Background LCDM
Om = 0.315; OL = 0.685; h = 0.674; H0 = 100*h
def E(z): return np.sqrt(Om*(1+z)**3 + OL)

# Branch B regime modulation
# Galactic: σ_galactic = 10^9.56, Cosmic: σ_cosmic = 10^8.37
# Δlog σ = 1.19 dex → galactic absorption ~15× stronger
log_sigma_gal = 9.56
log_sigma_cos = 8.37
ratio = 10**(log_sigma_gal - log_sigma_cos)  # ~15.5

# Volume fraction in galactic-mode (depletion zones around baryons)
# At z=0 estimate: galactic halos occupy ~1e-5 of cosmic volume (collapsed structures)
# but absorption cross section weighted: f_eff = f_vol * ratio
# Toy: f_eff(z=0) ~ 1e-4, decays at high z (less structure)
def f_env(z):
    return 1e-4 * (Om*(1+z)**3/E(z)**2)  # follows matter fraction

# G_eff modulation: SQT depletion zone reduces effective G_N for diffuse matter
# Branch B prediction: |ΔG/G| ~ f_env * (something small)
# Toy parameter alpha ~ -0.02 (suppression in cosmic regime)
alpha = -0.02

def G_eff_over_G(z):
    return 1.0 + alpha * f_env(z) * ratio

# Linear growth
# d²D/dN² + (2 + dlnH/dN) dD/dN - 1.5 Om(z) (G_eff/G) D = 0
# N = ln a, z = e^{-N}-1
def deriv(y, N):
    D, Dp = y
    a = np.exp(N); z = 1/a - 1
    Hz = E(z)
    Om_z = Om*(1+z)**3 / Hz**2
    dlnH_dN = -1.5*Om_z  # standard
    GoG = G_eff_over_G(z)
    Dpp = -(2 + dlnH_dN)*Dp + 1.5*Om_z*GoG*D
    return [Dp, Dpp]

N_arr = np.linspace(np.log(1e-3), 0, 500)  # from a=0.001 to today
sol = odeint(deriv, [1e-3, 1e-3], N_arr)
D = sol[:,0]; Dp = sol[:,1]
D /= D[-1]  # normalize to today=1
a_arr = np.exp(N_arr); z_arr = 1/a_arr - 1
f_growth = Dp/D  # = dlnD/dlnN

# Compare LCDM (G_eff=G)
def deriv_lcdm(y, N):
    D, Dp = y
    a = np.exp(N); z = 1/a - 1
    Hz = E(z)
    Om_z = Om*(1+z)**3 / Hz**2
    dlnH_dN = -1.5*Om_z
    Dpp = -(2 + dlnH_dN)*Dp + 1.5*Om_z*D
    return [Dp, Dpp]
sol_lcdm = odeint(deriv_lcdm, [1e-3, 1e-3], N_arr)
D_lcdm = sol_lcdm[:,0]; D_lcdm /= D_lcdm[-1]

# sigma_8 prediction
# Planck normalizes sigma_8(z=0)=0.811 at LCDM growth
# Branch B shifts: sigma_8_BB = 0.811 * (D_BB(z=0)/D_LCDM(z=0)) — both 1 by normalization
# Better: use D at high z normalization (z_drag~1100), compare today
# Approximate: sigma_8_BB/sigma_8_LCDM = D_BB(0)/D_LCDM(0) when both normalized at high z
# Re-normalize: anchor at z=10 (recombination far past)
idx10 = np.argmin(np.abs(z_arr - 10))
D_BB_anchor = sol[:,0]/sol[idx10,0]
D_LCDM_anchor = sol_lcdm[:,0]/sol_lcdm[idx10,0]
ratio_today = D_BB_anchor[-1]/D_LCDM_anchor[-1]

sigma8_planck = 0.811
sigma8_BB = sigma8_planck * ratio_today
sigma8_DES = 0.776  # DES-Y3
S8_planck = sigma8_planck * np.sqrt(Om/0.3)
S8_BB = sigma8_BB * np.sqrt(Om/0.3)
S8_DES = sigma8_DES * np.sqrt(0.3/0.3)

print(f"  alpha={alpha}, ratio={ratio:.2f}, f_env(0)={f_env(0):.2e}")
print(f"  D_BB(0)/D_LCDM(0) = {ratio_today:.6f}")
print(f"  sigma_8 LCDM(Planck) = {sigma8_planck:.3f}")
print(f"  sigma_8 Branch B     = {sigma8_BB:.3f}")
print(f"  sigma_8 DES-Y3       = {sigma8_DES:.3f}")
print(f"  S_8 LCDM = {S8_planck:.3f}")
print(f"  S_8 BB   = {S8_BB:.3f}")
print(f"  S_8 DES  = {S8_DES:.3f}")

# Tension: BB shifts toward DES?
shift = sigma8_planck - sigma8_BB
des_gap = sigma8_planck - sigma8_DES
shift_frac = shift / des_gap if des_gap != 0 else 0
print(f"  BB shift toward DES: {shift:.4f} ({100*shift_frac:.1f}% of total tension)")

verdict = (f"Branch B alpha={alpha}, f_env~1e-4: sigma_8 shift = {shift:.4f} ({100*shift_frac:.1f}% of S_8 tension). "
           f"For full tension resolution alpha would need to be ~{alpha*(1/shift_frac if shift_frac>0 else 100):.2f}, "
           f"requiring f_env*ratio*alpha ~ 0.04. Current toy under-predicts; "
           "explicit volume-weighted integral over depletion zones needed.")

fig, axes = plt.subplots(1, 2, figsize=(14,6))
axes[0].plot(z_arr, D_BB_anchor, 'b-', label='Branch B')
axes[0].plot(z_arr, D_LCDM_anchor, 'r--', label='LCDM')
axes[0].set_xlabel('z'); axes[0].set_ylabel('D(z)/D(z=10)')
axes[0].set_xscale('log'); axes[0].set_yscale('log')
axes[0].legend(); axes[0].grid(alpha=0.3)
axes[0].set_title('Linear growth')

axes[1].plot(z_arr, (D_BB_anchor/D_LCDM_anchor - 1)*100, 'g-')
axes[1].set_xlabel('z'); axes[1].set_ylabel('(D_BB/D_LCDM - 1) %')
axes[1].set_xscale('log'); axes[1].grid(alpha=0.3)
axes[1].set_title('Branch B growth deviation from LCDM')
plt.tight_layout(); plt.savefig(OUT/'L206.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(alpha=alpha, ratio_sigma=float(ratio), f_env_today=float(f_env(0)),
                   D_ratio_today=float(ratio_today),
                   sigma8_BB=float(sigma8_BB), sigma8_LCDM=float(sigma8_planck), sigma8_DES=float(sigma8_DES),
                   S8_BB=float(S8_BB), S8_LCDM=float(S8_planck),
                   shift=float(shift), tension_fraction_resolved=float(shift_frac),
                   verdict=verdict), f, indent=2)
print("L206 DONE")
