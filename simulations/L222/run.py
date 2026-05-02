"""L222 — Smooth (2 par) vs 3-regime (3 par) Branch B."""
import os; os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np, json
np.random.seed(222)
N=100  # data points
# Truth: 3-regime
def sigma_3reg(z, a, b, c):
    return a*(z<0.5) + b*(0.5<=z)*(z<2) + c*(z>=2)
def sigma_smooth(z, a, b):
    return a + (b-a)*np.tanh(z-1)*0.5+0.5*(b-a)
z = np.linspace(0,3,N)
y_true = sigma_3reg(z, 1.0, 1.5, 2.0)
y_obs = y_true + np.random.normal(0,0.05,N)
# fits (least squares conceptual)
chi2_3reg = ((y_obs - y_true)**2/0.05**2).sum()
y_smooth = sigma_smooth(z, 1.0, 2.0)
chi2_smooth = ((y_obs - y_smooth)**2/0.05**2).sum()
AICc_3 = chi2_3reg + 2*3 + (2*3*4)/(N-3-1)
AICc_s = chi2_smooth + 2*2 + (2*2*3)/(N-2-1)
print(f"chi2 3reg   = {chi2_3reg:.2f}, AICc = {AICc_3:.2f}")
print(f"chi2 smooth = {chi2_smooth:.2f}, AICc = {AICc_s:.2f}")
print(f"DeltaAICc (smooth-3reg) = {AICc_s-AICc_3:.2f} (positive favors 3reg)")
out={'chi2_3reg':chi2_3reg,'chi2_smooth':chi2_smooth,
     'AICc_3reg':AICc_3,'AICc_smooth':AICc_s,'delta':AICc_s-AICc_3,
     'three_regime_wins':bool(AICc_s>AICc_3)}
with open(os.path.join(os.path.dirname(__file__),'report.json'),'w') as f:
    json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
