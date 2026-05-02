"""L213 — n field statistics: Poisson assumption check."""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
import numpy as np, json

n0 = 4.1e95  # kg/m^3 (n0 mu, treat as number density per Planck volume normalised)
# Number of metabolism quanta per cosmological volume
# Take Planck length l_Pl = 1.616e-35 m, so n_quanta per m^3 = n0/m_Pl
m_Pl = 2.176e-8  # kg
n_quanta = n0 / m_Pl  # per m^3 ~ 1.88e103
Mpc = 3.086e22  # m
V_Mpc = Mpc**3
N_in_Mpc = n_quanta * V_Mpc
sigma_over_N = 1.0 / np.sqrt(N_in_Mpc)
print(f"n_quanta per m^3 = {n_quanta:.3e}")
print(f"N in 1 Mpc^3     = {N_in_Mpc:.3e}")
print(f"sigma/N (Poisson)= {sigma_over_N:.3e}")

# CMB scale (Hubble vol)
V_H = (2998 * Mpc)**3  # ~ 4.3e76 m^3 in natural units
N_H = n_quanta * V_H
sigma_H = 1.0 / np.sqrt(N_H)
print(f"sigma/N (Hubble) = {sigma_H:.3e}")

# f_NL prediction: for Gaussian random field, <n^3>/<n^2>^{3/2} = 0
# Poisson skewness = 1/sqrt(N), so f_NL ~ sigma/N negligible
f_NL_pred = sigma_H * 1e10  # assume amplitude ~10^10 enhancement
print(f"f_NL crude bound = {f_NL_pred:.3e}")

out = {
    'n_quanta_per_m3': float(n_quanta),
    'N_per_Mpc3': float(N_in_Mpc),
    'sigma_over_N_Mpc': float(sigma_over_N),
    'sigma_over_N_Hubble': float(sigma_H),
    'f_NL_crude': float(f_NL_pred),
    'CMB_compatible': bool(abs(f_NL_pred) < 5),
}
with open(os.path.join(os.path.dirname(__file__), 'report.json'), 'w') as f:
    json.dump(out, f, indent=2)
print(json.dumps(out, indent=2))
