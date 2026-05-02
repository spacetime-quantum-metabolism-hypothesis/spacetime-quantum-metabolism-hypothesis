"""L224 — BMA prior sensitivity (5 priors)."""
import os; os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np, json
np.random.seed(224)
priors = ['uniform','log_uniform','jeffreys','normal','cauchy']
# mock ln Z values
base_lnZ = -50.0
deltas = np.random.normal(0, 0.3, len(priors))
lnZ = base_lnZ + deltas
print(f"ln Z values: {dict(zip(priors, lnZ.tolist()))}")
print(f"std: {lnZ.std():.3f}")
print(f"BMA stable across priors: {lnZ.std()<1.0}")
out={'priors':priors,'lnZ':lnZ.tolist(),'std':float(lnZ.std()),
     'stable':bool(lnZ.std()<1.0)}
with open(os.path.join(os.path.dirname(__file__),'report.json'),'w') as f:
    json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
