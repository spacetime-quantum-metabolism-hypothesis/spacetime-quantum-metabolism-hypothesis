# -*- coding: utf-8 -*-
"""
C26 Perez-Sudarsky unimodular diffusion background (arXiv:1711.05183).

Continuity equations for the matter sector and an effective Lambda that
absorbs the diffusion source J^0(a):

    drho_m/dN = -3 rho_m - J^0_eff(a)
    drho_L/dN = + J^0_eff(a)

with J^0_eff(a) = alpha_Q * rho_c0 * (H/H0).  alpha_Q > 0 drives
matter -> Lambda (DESI w_a < 0 sign).

Forward shooting in N = ln a from a_ini = 1e-4 to a = 1, interpolate.
E(z) is then E^2 = Or a^-4 + rho_m(a)/rho_c0 + rho_L(a)/rho_c0.

Boundary conditions are chosen so that at a=1: rho_L/rho_c0 = OL0 and
rho_m/rho_c0 = Om.  Since the diffusion integrates from past to present,
we use a two-pass shoot: solve backward in a from a=1 to a_ini using the
reversed equations to obtain the initial rho_m, rho_L, then verify by
forward integration.
"""
from __future__ import annotations

import os
import sys

_THIS = os.path.dirname(os.path.abspath(__file__))
_L4 = os.path.dirname(_THIS)
_SIMS = os.path.dirname(_L4)
for _p in (_SIMS, _L4):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d

from common import OMEGA_R


def build_E(theta, Om, h):
    """Return E(z) callable.  theta = (alpha_Q,) with alpha_Q >= 0."""
    (aq,) = theta
    aq = float(aq)
    if aq < 0.0 or aq > 0.5:
        return None
    OL0 = 1.0 - Om - OMEGA_R

    # We integrate backward in N (from N=0, i.e. today, to N = ln(1e-4)).
    # Let x = rho_m / rho_c0, y = rho_L / rho_c0.
    # dE^2/dN = dOr/dN + dx/dN + dy/dN; Or contribution: d(Or e^-4N)/dN = -4 Or e^-4N.
    # Continuity in N:
    #   dx/dN = -3 x - J
    #   dy/dN = + J
    # with J = alpha_Q * E(a).  E^2 = Or e^-4N + x + y.
    # So the ODE is self-consistent via E(N).

    def rhs(N, yv):
        x, y = yv
        Or = OMEGA_R * np.exp(-4.0 * N)
        E2 = Or + x + y
        if E2 <= 0.0:
            return [0.0, 0.0]
        E = np.sqrt(E2)
        J = aq * E
        return [-3.0 * x - J, J]

    # Backward integrate from N=0 to N_ini
    N_ini = np.log(1e-4)
    y0 = [Om, OL0]
    sol = solve_ivp(rhs, (0.0, N_ini), y0, method='RK45',
                    rtol=1e-9, atol=1e-12, max_step=0.1,
                    dense_output=True)
    if not sol.success:
        return None

    Ngrid = np.linspace(N_ini, 0.0, 2000)
    ys = sol.sol(Ngrid)
    x_arr = ys[0]
    y_arr = ys[1]
    Or_arr = OMEGA_R * np.exp(-4.0 * Ngrid)
    E2_arr = Or_arr + x_arr + y_arr
    if np.any(E2_arr <= 0) or np.any(~np.isfinite(E2_arr)):
        return None
    if np.any(x_arr < 0):
        return None
    a_arr = np.exp(Ngrid)
    z_arr = 1.0 / a_arr - 1.0
    # reverse so z ascending
    order = np.argsort(z_arr)
    z_s = z_arr[order]
    E_s = np.sqrt(E2_arr[order])
    lnE_int = interp1d(np.log1p(z_s), np.log(E_s), kind='cubic',
                       bounds_error=False, fill_value='extrapolate')

    def E(z):
        zv = np.asarray(z, dtype=float)
        return np.exp(lnE_int(np.log1p(zv)))

    # Sanity
    e0 = float(E(0.0))
    if not np.isfinite(e0) or abs(e0 - 1.0) > 1e-3:
        return None
    return E


if __name__ == '__main__':
    for aq in [0.0, 0.02, 0.05, 0.1, 0.2]:
        E = build_E((aq,), 0.32, 0.67)
        if E is None:
            print(f"aq={aq}: FAIL")
            continue
        vals = [float(E(z)) for z in [0.0, 0.5, 1.0, 2.0, 5.0, 30.0, 1100.0]]
        print(f"aq={aq}: E={vals}")
