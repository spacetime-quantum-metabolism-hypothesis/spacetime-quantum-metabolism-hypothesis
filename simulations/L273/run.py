#!/usr/bin/env python3
"""L273 — Hierarchical Bayesian: 1/2/3-component GMM on SPARC sigma_0."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
from scipy.stats import norm
from scipy.optimize import minimize
ROOT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis")
OUT = ROOT/"results/L273"; OUT.mkdir(exist_ok=True, parents=True)

with open(ROOT/"results/L69/l69_step1_report.json") as f:
    step1 = json.load(f)
log_sigma = np.array([r['log_sigma'] for r in step1['rows']])
N = len(log_sigma)

def gmm_nll(params, k, x):
    if k==1:
        mu, s = params[0], abs(params[1])+0.01
        return -np.sum(norm.logpdf(x, mu, s))
    weights_raw = params[:k]; mus = params[k:2*k]; ss = np.abs(params[2*k:3*k])+0.01
    w = np.exp(weights_raw); w /= w.sum()
    pdf = sum(w[i]*norm.pdf(x, mus[i], ss[i]) for i in range(k))
    return -np.sum(np.log(pdf+1e-300))

results = {}
for k in [1,2,3]:
    if k==1:
        x0 = [np.mean(log_sigma), np.std(log_sigma)]
    else:
        x0 = list(np.zeros(k)) + list(np.linspace(log_sigma.min(), log_sigma.max(), k)) + [np.std(log_sigma)/2]*k
    best_nll = 1e30
    for trial in range(10):
        x0_t = np.array(x0) + np.random.RandomState(trial).normal(0,0.1,len(x0))
        try:
            r = minimize(gmm_nll, x0_t, args=(k, log_sigma), method='Nelder-Mead', options=dict(maxiter=5000))
            if r.fun < best_nll: best_nll, best_x = r.fun, r.x
        except: pass
    n_params = 2*k + (k-1)  # weights k-1, means k, stds k
    aic = 2*best_nll + 2*n_params
    bic = 2*best_nll + n_params*np.log(N)
    results[k] = dict(aic=float(aic), bic=float(bic), nll=float(best_nll), n_params=int(n_params))
    print(f"  k={k}: AIC={aic:.1f} BIC={bic:.1f} NLL={best_nll:.2f}")

best_aic = min(results, key=lambda k: results[k]['aic'])
print(f"\n  Best by AIC: k={best_aic}")
verdict = f"SPARC sigma_0 hierarchical: best k={best_aic} components by AIC. Single Gaussian {'preferred' if best_aic==1 else 'NOT preferred'}."
print(verdict)
with open(OUT/'report.json','w') as f:
    json.dump(dict(results=results, best=best_aic, verdict=verdict), f, indent=2)
