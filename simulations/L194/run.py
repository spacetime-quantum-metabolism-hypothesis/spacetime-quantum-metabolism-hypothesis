#!/usr/bin/env python3
"""L194 — Independent cross-validation."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L194"); OUT.mkdir(parents=True,exist_ok=True)

print("L194 — Cross-validation: train on subset, predict held-out")
# Use SPARC + anchors
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
print(f"  SPARC: {len(sparc_log_rho)} galaxies")

# 100 random splits
def branchB(p, lr):
    return np.where(lr < -25, p[0], np.where(lr < -22, p[1], p[2]))

def quadratic(p, lr):
    return p[0] + p[1]*(lr+24) + p[2]*(lr+24)**2

def fit_and_test(train_idx, test_idx, model, k, bounds, lr, ls):
    def chi2_train(p):
        pred = model(p, lr[train_idx])
        return np.sum(((ls[train_idx] - pred)/0.5)**2)
    res = differential_evolution(chi2_train, bounds, seed=42, tol=1e-7, maxiter=200)
    pred_test = model(res.x, lr[test_idx])
    chi2_test = np.sum(((ls[test_idx] - pred_test)/0.5)**2)
    return chi2_test

# Anchors always in train
log_rho_anchors = np.array([-27, -23.5, -21])
log_sigma_anchors = np.array([8.37, 7.75, 9.56])

n_splits = 100
chi2_BB_test = []
chi2_quad_test = []
np.random.seed(42)
for s in range(n_splits):
    perm = np.random.permutation(len(sparc_log_rho))
    half = len(sparc_log_rho)//2
    train_sp = perm[:half]
    test_sp = perm[half:]

    # Train: anchors + half SPARC
    lr_train = np.concatenate([log_rho_anchors, sparc_log_rho[train_sp]])
    ls_train = np.concatenate([log_sigma_anchors, sparc_log_sigma[train_sp]])
    # Test: other half SPARC
    lr_test = sparc_log_rho[test_sp]
    ls_test = sparc_log_sigma[test_sp]

    # Fit Branch B on train
    def chi2_BB(p):
        pred = branchB(p, lr_train)
        return np.sum(((ls_train - pred)/0.5)**2)
    res_BB = differential_evolution(chi2_BB, [(7,11)]*3, seed=s, tol=1e-7, maxiter=100)
    pred_BB_test = branchB(res_BB.x, lr_test)
    chi2_BB_test.append(np.sum(((ls_test - pred_BB_test)/0.5)**2))

    # Fit quadratic on train
    def chi2_q(p):
        pred = quadratic(p, lr_train)
        return np.sum(((ls_train - pred)/0.5)**2)
    res_q = differential_evolution(chi2_q, [(5,11), (-3,3), (-1,1)], seed=s, tol=1e-7, maxiter=100)
    pred_q_test = quadratic(res_q.x, lr_test)
    chi2_quad_test.append(np.sum(((ls_test - pred_q_test)/0.5)**2))

chi2_BB_test = np.array(chi2_BB_test)
chi2_quad_test = np.array(chi2_quad_test)

print(f"\n  Cross-validation results (100 random 50/50 splits):")
print(f"  Branch B test χ²: median = {np.median(chi2_BB_test):.2f}, std = {np.std(chi2_BB_test):.2f}")
print(f"  Quadratic test χ²: median = {np.median(chi2_quad_test):.2f}, std = {np.std(chi2_quad_test):.2f}")
print(f"\n  Branch B wins in {sum(chi2_BB_test < chi2_quad_test)}/{n_splits} splits")
median_diff = np.median(chi2_BB_test - chi2_quad_test)
print(f"  Median(BB - quad) = {median_diff:+.2f}")

if median_diff < 0:
    print(f"  → Branch B preferred on test set")
elif median_diff > 0:
    print(f"  → Quadratic preferred on test set")
else:
    print(f"  → No clear preference")

verdict = ("Cross-validation: Branch B test χ² = " +
           f"{np.median(chi2_BB_test):.1f} vs Quadratic = {np.median(chi2_quad_test):.1f}. " +
           ("Branch B preferred" if median_diff < -1 else
            ("Quadratic preferred" if median_diff > 1 else "Indistinguishable")))

fig, ax = plt.subplots(figsize=(10,6))
ax.hist(chi2_BB_test, bins=20, alpha=0.5, label='Branch B', color='blue')
ax.hist(chi2_quad_test, bins=20, alpha=0.5, label='Quadratic', color='green')
ax.set_xlabel('Test χ² (held-out half SPARC)')
ax.set_ylabel('count')
ax.set_title(f'L194 — Cross-validation: BB vs Quadratic (100 splits)')
ax.legend(); plt.tight_layout()
plt.savefig(OUT/'L194.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(N_splits=n_splits,
                   BB_test_chi2_median=float(np.median(chi2_BB_test)),
                   quad_test_chi2_median=float(np.median(chi2_quad_test)),
                   BB_wins=int(sum(chi2_BB_test < chi2_quad_test)),
                   verdict=verdict), f, indent=2)
print("L194 DONE")
