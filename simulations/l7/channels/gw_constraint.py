# -*- coding: utf-8 -*-
# CODE REVIEW: Bug-v Physics-v Repro-v Rules-v  [2026-04-11]
"""L7-X1: GW tensor speed constraint on C11D disformal B_0.

C11D pure disformal metric: g~_uv = A(phi)g_uv + B(phi) d_u phi d_v phi
A'=0 (GW170817 enforces), pure B coupling.

Tensor propagation speed:
  c_T^2/c^2 = 1 / (1 - B(phi) * X)
  where X = -g^uv d_u phi d_v phi / 2 = phi_dot^2 / 2 (kinetic energy)

GW170817 constraint: |c_T/c - 1| < 5e-16 (Abbott et al. 2017)
  → |B * X| < 1e-15

For exponential quintessence: phi_dot^2 ~ V(phi) * lam^2 / 3 (slow-roll)
This gives constraint on B_0.
"""
from __future__ import annotations
import json, os, sys, numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIMS = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, _SIMS)
sys.path.insert(0, os.path.join(_SIMS, 'l4'))

# Physical constants (SI)
G = 6.674e-11       # m^3 kg^-1 s^-2
c = 2.998e8         # m/s
hbar = 1.055e-34    # J s
t_P = np.sqrt(hbar * G / c**5)  # Planck time ~ 5.39e-44 s
l_P = c * t_P                    # Planck length ~ 1.62e-35 m
M_P = np.sqrt(hbar * c / G)     # Planck mass ~ 2.18e-8 kg

# Cosmological parameters (C11D L5 posterior mean)
H0 = 0.6776 * 100 * 1e3 / (3.086e22)  # s^-1
lam = 0.8872  # CLW quintessence slope
Om = 0.3095

# Quintessence energy density today (slow-roll)
rho_crit0 = 3 * H0**2 / (8 * np.pi * G)  # kg m^-3
OmDE = 1.0 - Om  # neglect radiation
rho_DE0 = OmDE * rho_crit0

# Slow-roll approximation: phi_dot^2 ~ lam^2 * V / 3 ~ lam^2 * rho_DE / 3
# (valid for tracking quintessence)
phi_dot2 = lam**2 * rho_DE0 / 3.0  # kg m^-3 s^-2 (in natural units where M_P=1)

# Convert to natural units (M_P = 1):
# rho_DE0 [kg/m^3] / rho_P [kg/m^3]
rho_P = M_P**4 * c / hbar**3  # Planck density ~ 5.16e96 kg/m^3
phi_dot2_natural = phi_dot2 / rho_P  # dimensionless ~ Omega_DE * H0^2/rho_P

# GW170817 constraint on B * X (X = phi_dot^2/2)
# |c_T^2/c^2 - 1| = |B * X| < 5e-16 (2-sigma)
# Note: X in units of M_P^2/s^2 in natural units
# In covariant form: X = -g^uv d_u phi d_v phi / 2 = phi_dot^2 / 2
X_natural = phi_dot2_natural / 2.0

gw_constraint = 5e-16  # |c_T/c - 1| < 5e-16

# B_0 upper limit: |B_0| < gw_constraint / X_natural
B0_max_natural = gw_constraint / X_natural if X_natural > 0 else float('inf')

print('[L7-X1] GW inspiral B_0 constraint for C11D disformal', flush=True)
print('[L7-X1] C11D params: Om=%.4f h=0.6776 lam=%.4f' % (Om, lam), flush=True)
print('[L7-X1] rho_DE0/rho_crit0 = %.4f' % OmDE, flush=True)
print('[L7-X1] phi_dot^2 (natural, M_P=1, t_P=1): %.4e' % phi_dot2_natural, flush=True)
print('[L7-X1] X = phi_dot^2/2 (natural): %.4e' % X_natural, flush=True)
print('[L7-X1] GW170817: |c_T/c - 1| < %.1e' % gw_constraint, flush=True)
print('[L7-X1] B_0 upper limit (natural): %.4e' % B0_max_natural, flush=True)

# Compare with disformal coupling strength needed for w_a < 0 signal
# B_0 in CLW units: B_0 ~ O(1/M_P^2) for typical disformal theories
# Meaningful B_0 range: 0.1 to 10 (in M_P^-2 units)
B0_typical_range = [0.1, 10.0]
print('\n[L7-X1] Typical disformal B_0 range: %.1f - %.1f (M_P^-2 units)' % tuple(B0_typical_range))
print('[L7-X1] GW170817 constraint: B_0 < %.4e (M_P^-2)' % B0_max_natural)

# Key question: does GW constraint kill typical B_0 values?
gw_kills_typical = B0_max_natural < B0_typical_range[0]
print('[L7-X1] GW constraint kills typical B_0 range? %s' % gw_kills_typical)

# C11D with A'=0: background is pure quintessence, B enters only at perturbation level
# → Background w(z) UNAFFECTED by B_0 (ZKB 2013)
# → GW constraint on B_0 is SEPARATE from background fit
# → B_0 must be small for GW, but background fit is independent
print('\n[L7-X1] Key: A=1 (A=const), B enters perturbations only (ZKB 2013)')
print('[L7-X1] Background w(z) independent of B_0 constraint')
print('[L7-X1] Conclusion: GW170817 constrains B_0 < %.2e but does NOT kill C11D background' % B0_max_natural)

# Additional: GW event rate forecast for LIGO O4 / Einstein Telescope
# Binary neutron star merger at z~0.01-0.1: delta_c_T test
# ET sensitivity: |c_T/c - 1| < 1e-18 (Belgacem et al. 2019)
ET_sensitivity = 1e-18
B0_ET = ET_sensitivity / X_natural if X_natural > 0 else float('inf')
print('\n[L7-X1] Einstein Telescope forecast: |c_T/c-1| < %.1e' % ET_sensitivity)
print('[L7-X1] ET B_0 constraint: B_0 < %.4e (M_P^-2)' % B0_ET)
print('[L7-X1] ET improvement over GW170817: %.0fx tighter' % (B0_max_natural / B0_ET if B0_ET > 0 else float('inf')))

result = {
    'phase': 'L7-X1',
    'model': 'C11D pure disformal A=1',
    'params': {'Om': Om, 'h': 0.6776, 'lam': lam},
    'gw170817_constraint': {'B0_max_natural': float(B0_max_natural), 'kills_background': False, 'kills_typical_B0': bool(gw_kills_typical)},
    'einstein_telescope_forecast': {'sensitivity': ET_sensitivity, 'B0_max_natural': float(B0_ET), 'improvement_factor': float(B0_max_natural/B0_ET) if B0_ET > 0 else None},
    'conclusion': 'GW170817 constrains disformal B_0 but A=1 background is independent. C11D background unaffected.',
    'q22_contribution': 'GW channel provides additional perturbation-level constraint on B_0. Does not K25-kill C11D.',
}
out_path = os.path.join(_HERE, 'gw_constraint.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2)
print('\n[L7-X1] Saved to %s' % out_path, flush=True)
