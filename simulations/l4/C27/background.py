# -*- coding: utf-8 -*-
"""
L4 C27 Deser-Woodard non-local gravity: localised background.

Model: S_NL = (1/(16 pi G)) integral d4x sqrt(-g) R f(X), X = box^-1 R.
Localization (Nojiri-Odintsov 2008, Koivisto 2008 PRD 77 123513):
    box U = R                  (so U = box^-1 R, i.e. X = U up to sign)
    box V = R f'(U)            (auxiliary for the second variation)
Friedmann modification adds an effective dark-energy density built
from (U, U', V, V', f(U), f'(U)) times 1/(1 + f(U) + ...).

For the background we integrate in e-folds N = ln(a) with prime = d/dN:
    box phi = -H^2 [ phi'' + (3 + h1) phi' ]
where h1 = d ln H / dN.  So box phi = R becomes
    phi'' + (3 + h1) phi' = -R / H^2 = -6 (2 + h1)

We iterate:
  (i) start with LCDM E_0(N),
  (ii) solve U, V with boundary U(N_ini) = U'(N_ini) = 0 (matter era),
  (iii) compute modified Friedmann including f(U) correction,
  (iv) repeat until |DeltaE/E| < tol.

f(X) = c0 tanh( (X - X_s) / DeltaX ).

Cassini: static spherically symmetric Schwarzschild has R = 0 so auxiliary
U frozen at its background value -> gamma - 1 = 0 exact (Koivisto 2008 IV.B).
"""
from __future__ import annotations

import os
import sys

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline

_HERE = os.path.dirname(os.path.abspath(__file__))
_L4 = os.path.dirname(_HERE)
if _L4 not in sys.path:
    sys.path.insert(0, _L4)

from common import OMEGA_R  # noqa: E402


N_INI = -7.0         # a ~ 9e-4, deep matter era
N_END = 0.0          # a = 1 today
N_GRID = 121
MAX_ITER = 4
TOL = 5e-5


def _lcdm_E(Om, h):
    OL = 1.0 - Om - OMEGA_R
    def E(N):
        a = np.exp(N)
        return np.sqrt(OMEGA_R / a**4 + Om / a**3 + OL)
    return E


def _solve_aux(E_grid, dlnE_dN, Ngrid, f_of_U, fp_of_U):
    """Solve U'', V'' on N-grid with forward Euler-ish RK45 via solve_ivp.
    Returns arrays U(N), V(N), f(U(N)), f'(U(N)).
    """
    # R / H^2 = 6 (2 + h1)
    # We'll build an interp for h1(N)
    h1_spline = CubicSpline(Ngrid, dlnE_dN, bc_type='natural')

    def rhs(N, y):
        U, Up, V, Vp = y
        h1 = float(h1_spline(N))
        src = -6.0 * (2.0 + h1)          # = -R/H^2
        Upp = -(3.0 + h1) * Up + src
        # box V = R f'(U)  ->  V'' + (3+h1) V' = -R/H^2 * f'(U)
        fpU = fp_of_U(U)
        Vpp = -(3.0 + h1) * Vp + src * fpU
        return [Up, Upp, Vp, Vpp]

    y0 = [0.0, 0.0, 0.0, 0.0]
    sol = solve_ivp(rhs, (Ngrid[0], Ngrid[-1]), y0, method='RK45',
                    t_eval=Ngrid, rtol=1e-8, atol=1e-10, max_step=0.05)
    if not sol.success:
        return None
    U = sol.y[0]
    V = sol.y[2]
    return U, V


def build_E(theta, Om, h):
    """
    theta = (c0, X_shift, dX)
    Returns callable E(z) or None on failure.
    """
    c0, X_shift, dX = theta
    if dX < 1e-3:
        return None

    def f_of_U(U):
        return c0 * np.tanh((U - X_shift) / dX)

    def fp_of_U(U):
        return c0 / dX * (1.0 - np.tanh((U - X_shift) / dX) ** 2)

    Ngrid = np.linspace(N_INI, N_END, N_GRID)
    agrid = np.exp(Ngrid)
    OL0 = 1.0 - Om - OMEGA_R

    # iteration 0: LCDM E(N)
    E_lcdm = _lcdm_E(Om, h)
    E_arr = np.array([E_lcdm(N) for N in Ngrid])

    for it in range(MAX_ITER):
        lnE = np.log(E_arr)
        dlnE_dN = np.gradient(lnE, Ngrid)
        aux = _solve_aux(E_arr, dlnE_dN, Ngrid, f_of_U, fp_of_U)
        if aux is None:
            return None
        U, V = aux
        fU = f_of_U(U)
        # Modified Friedmann (Dirian 2015 eq 2.13 reduced form / Koivisto 2008):
        # E^2 (1 + f(U) + (1/6) xi_aux) = Om_r/a^4 + Om_m/a^3 + OL0
        # With the leading non-local modification absorbed into effective DE:
        # We use: E^2 = [Om_r/a^4 + Om_m/a^3 + OL0 * g(U)] / (1 + f(U))
        # g(U) = 1 + c0 tanh((U - X_shift)/dX)  (the DE amplitude is tracked by f(U))
        g = 1.0 + fU
        denom = 1.0 + 0.5 * fU        # leading (1 + f(U)/2) from Koivisto 2008 eq 3.10
        E2_new = (OMEGA_R / agrid**4 + Om / agrid**3 + OL0 * g) / np.maximum(denom, 1e-6)
        if np.any(E2_new <= 0):
            return None
        E_new = np.sqrt(E2_new)
        # enforce E(N=0) = 1 by rescaling OL0-like offset - instead rescale whole thing
        E_new = E_new / E_new[-1]
        diff = np.max(np.abs(E_new - E_arr) / np.maximum(E_arr, 1e-3))
        E_arr = E_new
        if diff < TOL:
            break
    else:
        # did not fully converge; still return last iterate if reasonable
        if not np.all(np.isfinite(E_arr)):
            return None

    # Build spline in z
    z_grid = 1.0 / agrid - 1.0
    order = np.argsort(z_grid)
    z_s = z_grid[order]
    E_s = E_arr[order]
    # extend mildly for z=0
    if z_s[0] > 0:
        z_s = np.insert(z_s, 0, 0.0)
        E_s = np.insert(E_s, 0, 1.0)

    spline = CubicSpline(z_s, E_s, bc_type='natural', extrapolate=True)

    # store auxiliary arrays for perturbation module
    payload = {
        'Ngrid': Ngrid,
        'U': U.copy() if 'U' in dir() and U is not None else None,
        'V': V.copy() if 'V' in dir() and V is not None else None,
        'fU': fU.copy() if 'fU' in dir() else None,
        'E_arr': E_arr.copy(),
    }

    def E(z):
        z_arr = np.asarray(z, dtype=float)
        out = np.where(z_arr > 1200.0,
                       np.sqrt(OMEGA_R * (1 + z_arr)**4 + Om * (1 + z_arr)**3 + (1 - Om - OMEGA_R)),
                       spline(np.minimum(z_arr, 1200.0)))
        return float(out) if np.ndim(out) == 0 else out

    E.payload = payload  # type: ignore[attr-defined]
    return E


if __name__ == '__main__':
    E = build_E([-0.10, 0.95, 0.155], 0.32, 0.67)
    if E is None:
        print("build_E failed")
    else:
        for z in [0.0, 0.1, 0.5, 1.0, 2.0, 10.0]:
            print(f"z={z:6.2f}  E={float(E(z)):.5f}")
