"""L219 — DM detection via CMB mu-distortion."""
import os; os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np, json
G_eff_ratio = 1.0229
# mu ~ 10^-8 standard. SQT contribution ~ (G_eff-1) * mu_thermal_baseline
mu_baseline = 1e-8
delta_mu_SQT = (G_eff_ratio - 1) * mu_baseline
mu_pred = mu_baseline + delta_mu_SQT
FIRAS_limit = 9e-5
PIXIE_target = 1e-8
print(f"mu baseline LCDM = {mu_baseline:.3e}")
print(f"Delta mu SQT     = {delta_mu_SQT:.3e}")
print(f"mu_pred SQT      = {mu_pred:.3e}")
print(f"FIRAS limit      = {FIRAS_limit:.1e} (passed: {mu_pred<FIRAS_limit})")
print(f"PIXIE target     = {PIXIE_target:.1e} (detectable: {mu_pred>PIXIE_target/3})")
out = {'mu_baseline':mu_baseline,'delta_mu':delta_mu_SQT,'mu_pred':mu_pred,
       'FIRAS_pass':bool(mu_pred<FIRAS_limit),'PIXIE_detectable':bool(mu_pred>PIXIE_target/3)}
with open(os.path.join(os.path.dirname(__file__),'report.json'),'w') as f:
    json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
