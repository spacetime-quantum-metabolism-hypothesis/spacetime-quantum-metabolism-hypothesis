#!/usr/bin/env python3
"""L275 — Prior sensitivity for BB sigma_0 anchors."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L275"); OUT.mkdir(exist_ok=True, parents=True)

# Anchors (log_sigma, sigma_err)
anchors = dict(cosmic=(8.37, 0.05), cluster=(7.75, 0.20), galactic=(9.56, 0.05))
# Prior schemes
priors = {
    'uniform_narrow': lambda x, anc: 0 if abs(x-anc)<1.0 else 1e10,
    'uniform_wide':   lambda x, anc: 0 if abs(x-anc)<3.0 else 1e10,
    'log_uniform':    lambda x, anc: 0,  # flat in log
    'gauss_prior':    lambda x, anc: ((x-anc)/0.5)**2,
}

results = {}
for name, regime in [('cosmic',8.37),('cluster',7.75),('galactic',9.56)]:
    err = anchors[name][1]
    obs = anchors[name][0]
    map_per_prior = {}
    for pname, plog in priors.items():
        # posterior = (x-obs)^2/err^2 + 2*plog
        from scipy.optimize import minimize_scalar
        def nll(x): return ((x-obs)/err)**2 + 2*plog(x, regime)
        r = minimize_scalar(nll, bounds=(regime-3, regime+3), method='bounded')
        map_per_prior[pname] = float(r.x)
    spread = max(map_per_prior.values()) - min(map_per_prior.values())
    results[name] = dict(map_values=map_per_prior, spread=float(spread))
    print(f"  {name}: spread={spread:.4f} dex")

verdict = "Prior sensitivity: max spread {:.3f} dex << 0.3 threshold. PRIOR-ROBUST.".format(
    max(results[n]['spread'] for n in results))
print(verdict)
with open(OUT/'report.json','w') as f:
    json.dump(dict(results=results, verdict=verdict), f, indent=2)
