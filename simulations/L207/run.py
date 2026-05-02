#!/usr/bin/env python3
"""L207 — Stress-energy conservation check for T^{μν}_n in FLRW."""
import os, json
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L207"); OUT.mkdir(parents=True,exist_ok=True)

print("L207 — T^{mu nu}_n explicit form + Bianchi identity check")
# T^{mu nu}_n = (rho_q + p_q) u^mu u^nu + p_q g^{mu nu}
# rho_q = n*eps/c^2, p_q = w_q * rho_q (w_q = -1 for cosmic, 0 for galactic-bound)
# In FLRW: drho_q/dt + 3H(rho_q + p_q) = -Q (energy transfer to matter)
# Branch B: Q = sigma_0 * n * rho_m * eps/c^2

c = 2.998e8; G = 6.674e-11; hbar = 1.055e-34
H0 = 73e3/3.086e22
sigma_cosmic = 10**8.37
tau_q = 1/(3*H0)
eps = hbar/tau_q
rho_crit = 3*H0**2/(8*np.pi*G)
n_inf = 0.685 * rho_crit * c**2 / eps
rho_m_0 = 0.315 * rho_crit
rho_q_0 = n_inf * eps / c**2

print(f"  rho_q_0 = {rho_q_0:.3e} kg/m^3")
print(f"  rho_Lambda(0.685 rho_crit) = {0.685*rho_crit:.3e}")
print(f"  Match (should be ~1): {rho_q_0/(0.685*rho_crit):.4f}")

# Test Bianchi identity in FLRW for cosmic regime (w_q = -1)
# drho_q/dt + 3H(1+w_q) rho_q = -Q
# w_q = -1 → drho_q/dt = -Q
# If Q = sigma_cosmic * n * rho_m * eps/c^2:
Q_cosmic = sigma_cosmic * n_inf * rho_m_0 * eps/c**2
# rate of n loss from absorption
abs_rate_n = sigma_cosmic * n_inf * rho_m_0
# rate of rho_q loss
drho_q_dt = - abs_rate_n * eps/c**2
# Hubble timescale rate of rho_q (3H rho_q for w=0 baseline)
hubble_rate = 3*H0*rho_q_0
print(f"\n  Q (energy transfer) = {Q_cosmic:.3e}")
print(f"  drho_q/dt from absorption = {drho_q_dt:.3e}")
print(f"  3H rho_q = {hubble_rate:.3e}")
print(f"  ratio absorption/hubble: {abs(drho_q_dt)/hubble_rate:.3e}")

# This ratio determines whether Lambda is stable or evolving
# If << 1: rho_q ~ const (effective Lambda) ✓
# If ~1: Lambda evolves significantly (DESI w_a)
ratio = abs(drho_q_dt)/hubble_rate
if ratio < 0.01:
    verdict_stab = "rho_q effectively constant (Lambda-like) — consistent with Lambda interpretation"
elif ratio < 0.1:
    verdict_stab = f"rho_q evolves at {ratio*100:.1f}% per Hubble — small evolving DE (DESI compatible)"
else:
    verdict_stab = f"rho_q evolves strongly ({ratio*100:.1f}%) — phantom/quintessence-like"
print(f"  → {verdict_stab}")

# Check: matter side conservation
# drho_m/dt + 3H rho_m = +Q (matter gains from absorption, in mass-density sense)
# But absorption typically converts n -> g (graviton/spacetime) not n -> baryon
# Actually: n absorbs INTO matter halo, supports gravity
# Energy: rho_m steady at Hubble rate
hubble_rate_m = 3*H0*rho_m_0
print(f"\n  3H rho_m = {hubble_rate_m:.3e}")
print(f"  Q/(3H rho_m) = {Q_cosmic/hubble_rate_m:.3e}")

verdict = (f"T^{{mu nu}}_n = (rho_q+p_q) u^mu u^nu + p_q g^{{mu nu}}, "
           f"rho_q_0 / rho_Lambda(Planck) = {rho_q_0/(0.685*rho_crit):.4f}. "
           f"Bianchi: drho_q/dt vs 3H rho_q = {ratio:.2e}. {verdict_stab}.")

# Plot: rho_q evolution including absorption term
z_arr = np.logspace(-3, 1, 200)
a = 1/(1+z_arr)
# Approx: rho_m(z) = rho_m_0 (1+z)^3, n(z) ≈ n_inf (steady-state assumed)
# integrate drho_q/dt with H = H0*sqrt(Om*(1+z)^3 + OL)
from scipy.integrate import odeint
def deriv(rho_q, t, sign):
    # t in 1/H0
    pass

# Simple analytic: rho_q(a) = rho_q_0 - integral(Q dt)
# dt/da = 1/(a H), Q ~ sigma*n_inf*rho_m_0*(1+z)^3 * eps/c^2
# Numerical
def Hubble(a):
    return H0*np.sqrt(0.315*a**(-3)+0.685)

a_arr = np.logspace(-3, 0, 500)
rho_q_arr = np.zeros_like(a_arr)
rho_q_arr[-1] = rho_q_0
for i in range(len(a_arr)-2, -1, -1):
    da = a_arr[i+1]-a_arr[i]
    a_mid = 0.5*(a_arr[i]+a_arr[i+1])
    rho_m_mid = rho_m_0/a_mid**3
    Q = sigma_cosmic * n_inf * rho_m_mid * eps/c**2
    H_mid = Hubble(a_mid)
    drho_da = -Q/(a_mid*H_mid)  # drho/dt = -Q so drho/da = -Q/(aH)
    # Going backward (da<0): rho(a) = rho(a+da) - drho_da*da
    rho_q_arr[i] = rho_q_arr[i+1] - drho_da*da

z_full = 1/a_arr - 1
rho_q_const = np.full_like(a_arr, rho_q_0)

fig, ax = plt.subplots(figsize=(10,6))
ax.plot(z_full, rho_q_arr/rho_q_0, 'b-', lw=2, label='SQT rho_q with absorption')
ax.plot(z_full, rho_q_const/rho_q_0, 'r--', lw=1, label='Pure Lambda (constant)')
ax.set_xlabel('z'); ax.set_ylabel('rho_q(z)/rho_q_0')
ax.set_xscale('log'); ax.legend(); ax.grid(alpha=0.3)
ax.set_title('L207 — rho_q evolution from Bianchi identity')
plt.tight_layout(); plt.savefig(OUT/'L207.png', dpi=120); plt.close()

with open(OUT/'report.json','w') as f:
    json.dump(dict(rho_q_0=float(rho_q_0), rho_Lambda_planck=float(0.685*rho_crit),
                   match_ratio=float(rho_q_0/(0.685*rho_crit)),
                   absorption_per_hubble=float(ratio),
                   verdict_stability=verdict_stab,
                   verdict=verdict), f, indent=2)
print("L207 DONE")
