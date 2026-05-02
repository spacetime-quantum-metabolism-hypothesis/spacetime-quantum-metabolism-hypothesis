"""L227 — GW scalar polarization prediction."""
import os; os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np, json
beta_d = 0.107
h_s_over_h_t = beta_d**2  # toy
LIGO_sens = 1e-3  # current bound on extra polarizations
print(f"h_s/h_t predicted = {h_s_over_h_t:.4f}")
print(f"LIGO O4 bound     = {LIGO_sens}")
print(f"Detectable?       = {h_s_over_h_t > LIGO_sens}")
out={'h_s_over_h_t':h_s_over_h_t,'LIGO_bound':LIGO_sens,
     'detectable':bool(h_s_over_h_t>LIGO_sens),
     'P15_prediction':'GW scalar mode amplitude ~1.1% relative to tensor'}
with open(os.path.join(os.path.dirname(__file__),'report.json'),'w') as f:
    json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
