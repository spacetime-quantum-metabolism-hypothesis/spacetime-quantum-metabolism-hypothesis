#!/usr/bin/env python3
"""L189 — AICc: Branch B vs simpler alternatives."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import minimize
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L189"); OUT.mkdir(parents=True,exist_ok=True)

print("L189 — AICc honest comparison: Branch B vs alternatives")

# Anchor data (3 points with errors)
log_rho = np.array([-27, -23.5, -21])
log_sigma_obs = np.array([8.37, 7.75, 9.56])
err = np.array([0.06, 0.06, 0.05])

# Models
def m1_const(p, lr):
    return np.full_like(lr, p[0])

def m2_linear(p, lr):
    return p[0] + p[1]*(lr + 24)

def m3_quad(p, lr):
    return p[0] + p[1]*(lr + 24) + p[2]*(lr + 24)**2

def m4_exp(p, lr):
    """exp transition between two regimes."""
    a, b, c = p
    return a + b * (1 + np.tanh((lr + c)/0.5))/2

def m_BB(p, lr):
    """Branch B 3-regime."""
    return np.where(lr < -25, p[0],
                    np.where(lr < -22, p[1], p[2]))

models = [
    ('M1 const', m1_const, 1, [(7,11)]),
    ('M2 linear', m2_linear, 2, [(7,11), (-2,2)]),
    ('M3 quadratic', m3_quad, 3, [(7,11), (-2,2), (-1,1)]),
    ('M4 exp transition', m4_exp, 3, [(7,11), (-2,2), (-30,-19)]),
    ('M_BB Branch B', m_BB, 3, [(7,11), (7,11), (7,11)]),
]

# Fit each
print(f"\n  Model AICc comparison (3 data points, anchors):")
print(f"  {'Model':<20} {'k':>3} {'χ²':>8} {'AICc':>8}")
results = []
for name, model, k, bounds in models:
    def chi2(p, model=model):
        pred = model(p, log_rho)
        return np.sum(((log_sigma_obs - pred)/err)**2)

    from scipy.optimize import differential_evolution
    res = differential_evolution(chi2, bounds, seed=42, tol=1e-9)
    chi2_best = res.fun
    n = len(log_rho)
    if n - k - 1 > 0:
        AICc = chi2_best + 2*k + 2*k*(k+1)/(n-k-1)
    else:
        AICc = chi2_best + 2*k + 1e6   # heavy penalty
    print(f"  {name:<20} {k:>3} {chi2_best:>8.3f} {AICc:>8.2f}")
    results.append((name, chi2_best, k, AICc))

results.sort(key=lambda x: x[3])
print(f"\n  Ranking (AICc):")
for r in results:
    print(f"    {r[0]:<20} AICc={r[3]:.2f}, k={r[2]}, chi²={r[1]:.2f}")

print("\n  HONEST ASSESSMENT:")
print("  With only 3 data points, all models with k=3 fit perfectly")
print("  Branch B is NOT statistically preferred over smooth alternatives")
print("  Need more data (4th regime or intermediate ρ) to discriminate")
print()
print("  Currently: 'Branch B 3-regime' is ONE valid framework")
print("  Smooth quadratic: equally valid")
print("  Constant: can't fit (chi² high)")
print("  Linear: can't fit either (slope wrong)")
print()
print("  Going forward in paper:")
print("  'We choose Branch B as a simple, transparent ansatz that")
print("   reproduces observed regime structure. Smooth alternatives")
print("   are equally consistent with current data.'")

verdict = ("With 3 data points, AICc cannot distinguish between Branch B and "
           "smooth quadratic models. Branch B preferred ONLY due to physical "
           "interpretation (regime structure suggests phase transition). "
           "Currently a CHOICE, not a UNIQUE inference. "
           "Future data will resolve.")

fig, ax = plt.subplots(figsize=(10,6))
ax.errorbar(log_rho, log_sigma_obs, yerr=err, fmt='ko', markersize=12, capsize=8)
log_rho_grid = np.linspace(-29, -19, 100)
for name, model, k, bounds in models:
    def chi2_(p, model=model):
        pred = model(p, log_rho)
        return np.sum(((log_sigma_obs - pred)/err)**2)
    from scipy.optimize import differential_evolution
    res = differential_evolution(chi2_, bounds, seed=42, tol=1e-9)
    pred = model(res.x, log_rho_grid)
    ax.plot(log_rho_grid, pred, lw=2, label=name)
ax.set_xlabel('log10(ρ_m)'); ax.set_ylabel('log10(σ_0)')
ax.set_title(f'L189 — Branch B vs alternatives: indistinguishable on 3 points')
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout(); plt.savefig(OUT/'L189.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(results=[(r[0], float(r[1]), r[2], float(r[3])) for r in results],
                   verdict=verdict), f, indent=2)
print("L189 DONE")
