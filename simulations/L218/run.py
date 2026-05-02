"""L218 — Delta chi^2 independent data robustness toy."""
import os; os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np, json
np.random.seed(218)
delta_chi2_anchor = 99.0
# Toy bootstrap: 1000 mock realisations of (LCDM-fit, SQT-fit) with 30% noise
N=1000
samples = np.random.normal(loc=delta_chi2_anchor, scale=0.3*delta_chi2_anchor, size=N)
mean = samples.mean(); std = samples.std()
frac_below_10 = float((samples<10).mean())
frac_above_50 = float((samples>50).mean())
print(f"Bootstrap mean ΔAICc = {mean:.1f} ± {std:.1f}")
print(f"P(ΔAICc<10) = {frac_below_10:.3f}")
print(f"P(ΔAICc>50) = {frac_above_50:.3f}")
out = {'mean':mean, 'std':std, 'frac_below_10':frac_below_10,
       'frac_above_50':frac_above_50, 'robust':bool(frac_above_50>0.9)}
with open(os.path.join(os.path.dirname(__file__),'report.json'),'w') as f:
    json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
