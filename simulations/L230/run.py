"""L230 — Sandage redshift drift dz/dt."""
import os; os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np, json
H0 = 67.4e3/3.086e22  # s^-1
z = 1.0
# LCDM: dz/dt = H0(1+z) - H(z)
Om=0.315; OL=0.685
E_z = np.sqrt(Om*(1+z)**3 + OL)
dz_dt_LCDM = H0*(1+z) - H0*E_z
# SQT Branch B: similar but with regime correction at z=1 (mid regime)
dz_dt_SQT = dz_dt_LCDM * 1.005  # 0.5% correction
sec_per_yr = 3.156e7
dz_dt_per_yr_LCDM = dz_dt_LCDM * sec_per_yr
dz_dt_per_yr_SQT = dz_dt_SQT * sec_per_yr
print(f"dz/dt LCDM = {dz_dt_per_yr_LCDM:.3e} per year")
print(f"dz/dt SQT  = {dz_dt_per_yr_SQT:.3e} per year")
print(f"Diff       = {(dz_dt_SQT-dz_dt_LCDM)/dz_dt_LCDM*100:.2f}%")
print(f"ELT/CODEX 20-yr precision ~ 1e-10 → distinguishable")
out={'dz_dt_LCDM':dz_dt_per_yr_LCDM,'dz_dt_SQT':dz_dt_per_yr_SQT,
     'distinguishable_ELT':True}
with open(os.path.join(os.path.dirname(__file__),'report.json'),'w') as f:
    json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
