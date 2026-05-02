"""L217 — sigma_8 perturbation under dark-only G_eff."""
import os; os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np, json
G_eff_ratio = 1.0229
# Linear growth: D ~ G_eff^{0.5} for short integration; ∫ over matter era
# Crude: sigma_8 ∝ D today; D_SQT/D_LCDM ≈ sqrt(G_eff_ratio) = 1.0114
delta_sigma_8 = 0.5 * (G_eff_ratio - 1)
sigma_8_LCDM = 0.811
sigma_8_SQT = sigma_8_LCDM * (1 + delta_sigma_8)
S8_LCDM = sigma_8_LCDM * np.sqrt(0.315/0.3)
S8_SQT = sigma_8_SQT * np.sqrt(0.315/0.3)
print(f"sigma_8 LCDM = {sigma_8_LCDM:.4f}")
print(f"sigma_8 SQT  = {sigma_8_SQT:.4f}")
print(f"Delta = {delta_sigma_8*100:.2f}%")
print(f"KiDS = 0.759±0.024; tension worsened (positive Delta).")
out = {'G_eff':G_eff_ratio, 'delta_sigma_8_pct':delta_sigma_8*100,
       'sigma_8_LCDM':sigma_8_LCDM, 'sigma_8_SQT':sigma_8_SQT,
       'tension_helped': bool(delta_sigma_8<0)}
with open(os.path.join(os.path.dirname(__file__),'report.json'),'w') as f:
    json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
