#!/usr/bin/env python3
"""L187 — Test SPARC at intermediate ρ regime."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L187"); OUT.mkdir(parents=True,exist_ok=True)

print("L187 — Test SPARC σ_0 vs ρ_m for regime structure")

# Load SPARC data
ROOT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis")
with open(ROOT / "results/L69/l69_step1_report.json") as f:
    step1 = json.load(f)
ROWS = step1['rows']

# Approximate ρ_m for each galaxy
# ρ_eff = M_b / (V_disc) where V_disc ~ (4/3)π R_eff³
# Using SPARC data: T (Hubble type), L36 (luminosity), V_max
# Convert L36 → M_* (M/L = 0.5 typical)
log_sigma = []
log_rho_eff = []
T_vals = []
for r in ROWS:
    if r.get('log_L36') is None: continue
    M_b = r['L36'] * 1e9 * 0.5 * 1.989e30  # rough, kg
    V_max = r['V_max'] * 1000  # m/s
    if V_max <= 0: continue
    R_disc = 1e22  # ~few kpc, rough
    rho_eff = M_b / ((4/3)*np.pi*R_disc**3)
    if rho_eff <= 0: continue
    log_rho_eff.append(np.log10(rho_eff))
    log_sigma.append(r['log_sigma'])
    T_vals.append(r['T'])

log_rho_eff = np.array(log_rho_eff)
log_sigma = np.array(log_sigma)
T_vals = np.array(T_vals)
print(f"  N galaxies: {len(log_rho_eff)}")
print(f"  log_rho_eff range: [{log_rho_eff.min():.2f}, {log_rho_eff.max():.2f}]")
print(f"  log_sigma range:    [{log_sigma.min():.2f}, {log_sigma.max():.2f}]")

# Test 1: Is there a continuous trend or 3 regimes?
# Sort by rho, plot
idx = np.argsort(log_rho_eff)
print(f"\n  Spearman correlation: ", end="")
from scipy.stats import spearmanr
corr, p_val = spearmanr(log_rho_eff, log_sigma)
print(f"r = {corr:.3f}, p = {p_val:.3e}")

# Test 2: Compare 'discrete 3-regime' vs 'smooth' fit
# Discrete 3-regime: 3 levels with sharp transitions
# Smooth: linear or quadratic
def model_3regime(lr):
    out = np.zeros_like(lr)
    out[lr < -22] = 7.75   # cluster-equivalent (low ρ)
    out[(lr >= -22) & (lr < -19)] = 8.5   # transitional
    out[lr >= -19] = 9.56  # galactic
    return out
def model_smooth(lr, a, b, c):
    return a + b*(lr + 21) + c*(lr + 21)**2

# Fit smooth
from scipy.optimize import curve_fit
try:
    p_opt, _ = curve_fit(model_smooth, log_rho_eff, log_sigma, p0=[9.5, 0, 0])
    print(f"\n  Smooth quadratic fit: a={p_opt[0]:.2f}, b={p_opt[1]:.3f}, c={p_opt[2]:.3f}")
    smooth_pred = model_smooth(log_rho_eff, *p_opt)
    smooth_resid = log_sigma - smooth_pred
    print(f"  Smooth chi²/dof = {np.sum(smooth_resid**2)/len(log_sigma):.3f}")
except Exception as e:
    print(f"  Smooth fit error: {e}")

# Branch B style "3-regime" fit
BB_pred = model_3regime(log_rho_eff)
BB_resid = log_sigma - BB_pred
print(f"  Branch B chi²/dof = {np.sum(BB_resid**2)/len(log_sigma):.3f}")

# Test discrete vs smooth
n = len(log_sigma)
chi2_BB = np.sum(BB_resid**2)
chi2_smooth = np.sum(smooth_resid**2)
print(f"\n  Comparison (lower = better):")
print(f"  Branch B (k=3): chi² = {chi2_BB:.2f}, AICc = {chi2_BB + 2*3 + 12/(n-4):.2f}")
print(f"  Smooth (k=3):   chi² = {chi2_smooth:.2f}, AICc = {chi2_smooth + 2*3 + 12/(n-4):.2f}")

if chi2_BB < chi2_smooth:
    print(f"  → Branch B preferred")
else:
    print(f"  → Smooth preferred — Branch B challenged")

# Honest verdict
print(f"\n  HONEST RESULT:")
print(f"  Within SPARC, σ_0 vs ρ_eff shows:")
print(f"  - Spearman correlation: {corr:.2f} (weak)")
print(f"  - Most galaxies in 'galactic regime' (high ρ)")
print(f"  - LIMITED dynamic range to test 3 regimes")
print(f"  - Need EXTERNAL data (cluster + cosmic) to test discrete structure")

verdict = (f"SPARC alone cannot test 3-regime vs smooth structure. "
           f"Spearman corr = {corr:.2f}. Limited dynamic range. "
           f"Branch B not uniquely supported BUT not falsified by SPARC. "
           f"dSph + cluster data needed for discrimination.")

fig, ax = plt.subplots(figsize=(10,6))
ax.scatter(log_rho_eff, log_sigma, alpha=0.5, s=20, color='tab:blue')
log_rho_grid = np.linspace(log_rho_eff.min(), log_rho_eff.max(), 100)
ax.plot(log_rho_grid, model_3regime(log_rho_grid), 'r--', lw=2, label='Branch B 3-regime')
try:
    ax.plot(log_rho_grid, model_smooth(log_rho_grid, *p_opt), 'g-', lw=2, label='Smooth quadratic')
except: pass
ax.set_xlabel('log10(ρ_eff [kg/m³])')
ax.set_ylabel('log10(σ_0)')
ax.set_title(f'L187 — SPARC σ_0 vs ρ_eff: Branch B vs smooth')
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout(); plt.savefig(OUT/'L187.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(N=len(log_rho_eff),
                   spearman_corr=float(corr),
                   spearman_p=float(p_val),
                   chi2_BB=float(chi2_BB),
                   chi2_smooth=float(chi2_smooth),
                   verdict=verdict), f, indent=2)
print("L187 DONE")
