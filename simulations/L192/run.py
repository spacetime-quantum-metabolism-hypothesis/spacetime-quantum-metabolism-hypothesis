#!/usr/bin/env python3
"""L192 — Smooth σ_0(ρ_m) full test against all data."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L192"); OUT.mkdir(parents=True,exist_ok=True)

print("L192 — Smooth σ_0(ρ_m): full test")
# Anchor data + SPARC inferred
log_rho_anchors = np.array([-27, -23.5, -21])
log_sigma_obs = np.array([8.37, 7.75, 9.56])
err_anchors = np.array([0.06, 0.06, 0.05])

# SPARC: estimate ρ_eff per galaxy
ROOT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis")
with open(ROOT / "results/L69/l69_step1_report.json") as f:
    step1 = json.load(f)
ROWS = step1['rows']
sparc_log_rho = []
sparc_log_sigma = []
for r in ROWS:
    if r.get('log_L36') is None: continue
    M_b = r['L36'] * 1e9 * 0.5 * 1.989e30
    R_disc = 1e22
    rho_eff = M_b / ((4/3)*np.pi*R_disc**3)
    if rho_eff <= 0: continue
    sparc_log_rho.append(np.log10(rho_eff))
    sparc_log_sigma.append(r['log_sigma'])
sparc_log_rho = np.array(sparc_log_rho)
sparc_log_sigma = np.array(sparc_log_sigma)
sparc_err = 0.5  # per-galaxy intrinsic scatter

# Combine anchor + SPARC
all_log_rho = np.concatenate([log_rho_anchors, sparc_log_rho])
all_log_sigma = np.concatenate([log_sigma_obs, sparc_log_sigma])
all_err = np.concatenate([err_anchors, np.full(len(sparc_log_rho), sparc_err)])
print(f"  Total points: {len(all_log_rho)} (3 anchors + {len(sparc_log_rho)} SPARC)")

# Models
def quadratic(p, lr):
    a, b, c = p
    return a + b*(lr+24) + c*(lr+24)**2

def cubic(p, lr):
    a, b, c, d = p
    x = lr+24
    return a + b*x + c*x**2 + d*x**3

def gaussian_dip(p, lr):
    """Gaussian dip at cluster scale + flat above and below"""
    a, dip_amp, dip_pos, dip_width = p
    return a - dip_amp * np.exp(-((lr-dip_pos)/dip_width)**2)

def branchB(p, lr):
    s_c, s_cl, s_g = p
    return np.where(lr < -25, s_c, np.where(lr < -22, s_cl, s_g))

models = [
    ('Branch B (3-step)', branchB, 3, [(7,11), (7,11), (7,11)]),
    ('Quadratic', quadratic, 3, [(5,11), (-3,3), (-1,1)]),
    ('Cubic', cubic, 4, [(5,11), (-3,3), (-1,1), (-0.1,0.1)]),
    ('Gaussian dip', gaussian_dip, 4, [(7,11), (0,5), (-25,-22), (0.5,3)]),
]

def chi2_total(p, model, lr, ls, err):
    pred = model(p, lr)
    return np.sum(((ls - pred)/err)**2)

results = []
print(f"\n  Model fits to all {len(all_log_rho)} points:")
for name, model, k, bounds in models:
    res = differential_evolution(
        lambda p: chi2_total(p, model, all_log_rho, all_log_sigma, all_err),
        bounds, seed=42, tol=1e-9, maxiter=300)
    n = len(all_log_rho)
    chi2 = res.fun
    AICc = chi2 + 2*k + 2*k*(k+1)/(n-k-1)
    BIC = chi2 + k*np.log(n)
    results.append((name, chi2, k, AICc, BIC, res.x))
    print(f"  {name:<22} k={k} chi²={chi2:7.2f} AICc={AICc:.2f} BIC={BIC:.2f}")

results.sort(key=lambda x: x[3])
print(f"\n  Ranking by AICc:")
ai_min = results[0][3]
for r in results:
    delta = r[3] - ai_min
    print(f"    {r[0]:<22} ΔAICc={delta:+.2f}")

# Honest verdict
print("\n  HONEST RESULT:")
best_name = results[0][0]
print(f"  Best: {best_name}")
if 'Branch B' in best_name:
    print("  → Branch B preferred even with all data")
else:
    print(f"  → {best_name} preferred over Branch B")
    delta_BB = next(r[3] for r in results if 'Branch B' in r[0]) - ai_min
    print(f"  → Branch B ΔAICc = {delta_BB:+.2f}")
    print(f"  → Smooth alternative is statistically preferred")

verdict = (f"Best fit: {best_name}. Branch B " +
           ("preferred" if 'Branch B' in best_name else "challenged") +
           " by smooth alternatives. " +
           "Paper should consider reframing: SQT framework with smooth σ(ρ) ansatz.")

fig, ax = plt.subplots(figsize=(12,7))
ax.errorbar(log_rho_anchors, log_sigma_obs, yerr=err_anchors,
            fmt='ks', markersize=15, capsize=8, label='Anchors', zorder=5)
ax.scatter(sparc_log_rho, sparc_log_sigma, alpha=0.3, s=15, color='gray', label='SPARC')
log_rho_grid = np.linspace(-29, -19, 200)
for name, model, k, bounds in models:
    res = differential_evolution(
        lambda p: chi2_total(p, model, all_log_rho, all_log_sigma, all_err),
        bounds, seed=42, tol=1e-9, maxiter=300)
    pred = model(res.x, log_rho_grid)
    ax.plot(log_rho_grid, pred, lw=2, label=f'{name} chi²={res.fun:.0f}')
ax.set_xlabel('log10(ρ_m)'); ax.set_ylabel('log10(σ_0)')
ax.set_title(f'L192 — All data fit: {best_name} preferred')
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout(); plt.savefig(OUT/'L192.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(N_total=len(all_log_rho),
                   results=[(r[0], float(r[1]), r[2], float(r[3]), float(r[4])) for r in results],
                   best=best_name,
                   verdict=verdict), f, indent=2)
print("L192 DONE")
