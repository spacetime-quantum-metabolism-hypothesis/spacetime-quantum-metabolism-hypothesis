"""L228 — 21cm absorption prediction."""
import os; os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np, json
T_b_LCDM = -0.220  # K, expected
T_b_EDGES = -0.500  # K, observed (Bowman+2018, controversial)
G_eff = 1.0229
T_b_SQT = T_b_LCDM * G_eff  # crude
print(f"T_b LCDM = {T_b_LCDM}")
print(f"T_b SQT  = {T_b_SQT:.3f}")
print(f"T_b EDGES= {T_b_EDGES}")
match = abs(T_b_SQT - T_b_EDGES) < 0.1
print(f"Match EDGES (within 0.1K)? {match}")
out={'T_b_LCDM':T_b_LCDM,'T_b_SQT':T_b_SQT,'T_b_EDGES':T_b_EDGES,
     'matches_EDGES':bool(match),
     'caveat':'EDGES detection contested (SARAS3 null)'}
with open(os.path.join(os.path.dirname(__file__),'report.json'),'w') as f:
    json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
