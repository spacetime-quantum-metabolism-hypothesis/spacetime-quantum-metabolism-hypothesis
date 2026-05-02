"""L214 — inflation epoch: SQT contribution to slow-roll."""
import os; os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np, json

# Planck 2018 + BICEP 2021
n_s_obs = 0.965
n_s_err = 0.004
r_bound = 0.036
H_inf = 1e14 * 1.602e-10 / 1.055e-34 / 2.998e8 * 2.998e8  # roughly H_inf ~ 1e14 GeV in s^-1
# Approximate: H_inf in s^-1 ~ E_inf [J] / hbar
E_inf = 1e14 * 1.602e-10  # J
hbar = 1.055e-34
H_inf_s = E_inf / hbar
print(f"H_inf ~ {H_inf_s:.3e} s^-1")

# SQT: rho_q = (3/(8 pi G)) H^2 (Bianchi-balanced); during inflation rho_q/rho_inf ~ const
# slow-roll modification: epsilon_q = (sigma_0 H) (extra dissipation)
G = 6.674e-11; t_Pl = 5.39e-44
sigma_0 = 4*np.pi*G*t_Pl
eps_q = sigma_0 * H_inf_s
print(f"epsilon_q = sigma_0 * H_inf = {eps_q:.3e}")

# Predicted n_s shift
delta_n_s = -2 * eps_q
n_s_pred = 1 + delta_n_s  # very crude
print(f"delta n_s = {delta_n_s:.3e}")
print(f"n_s pred  = {n_s_pred:.6f}")

# Tensor-to-scalar
r_pred = 16 * eps_q
print(f"r pred    = {r_pred:.3e}")

compat_ns = abs(n_s_pred - n_s_obs) < 5*n_s_err
compat_r = r_pred < r_bound
print(f"n_s compat (5sigma): {compat_ns}")
print(f"r compat: {compat_r}")

out = {
    'H_inf_s': H_inf_s,
    'eps_q': eps_q,
    'n_s_pred': n_s_pred,
    'r_pred': r_pred,
    'n_s_compat_5sigma': bool(compat_ns),
    'r_below_bound': bool(compat_r),
}
with open(os.path.join(os.path.dirname(__file__),'report.json'),'w') as f:
    json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
