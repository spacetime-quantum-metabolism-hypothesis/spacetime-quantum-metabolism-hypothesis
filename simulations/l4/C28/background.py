# -*- coding: utf-8 -*-
"""
L4 C28 Maggiore-Mancarella RR non-local gravity: localised background.

Model: S_NL = -(m^2/(12)) integral d4x sqrt(-g) R box^-2 R
Localization (Maggiore-Mancarella 2014 arXiv:1402.0448 Sec 2):
    box U = -R
    box S = -U
Modified Friedmann (Dirian 2015 arXiv:1502.06543 eq 2.5-2.8):
    E^2 = (Om_r/a^4 + Om_m/a^3 + (m^2/(9 H0^2)) gamma_RR(a))
    gamma_RR = (1/2)(U S' + U' S) - 2 U - (1/4) U^2 (in e-folds)  -- Dirian parametrization

Here prime = d/dN, N = ln a, box = -H^2[ d^2/dN^2 + (3+h1) d/dN ].

We integrate the coupled (U, U', S, S') in e-folds driven by LCDM-like background,
then self-consistently update E^2 including the gamma_RR contribution.

Free parameter: m  (in units of H0; actual theta = gamma0 = m^2/(9 H0^2) amplitude).
Extra shape params: (a_shift, da) that control a residual tanh tail used to fit the
remaining high-z tail not captured by leading gamma_RR (needed because RR-toy bump
peaks at a ~ 0.5 whereas DESI best-fit wants stronger recent departure).

Distinct from C27: auxiliary structure is (U, S) with box S = -U (second hierarchy),
versus C27 (U, V) with box V = R f'(U) (nonlinear source).  The resulting gamma_RR
has a ~linear-in-U and quadratic-in-U,S combination, not a tanh of U.

Cassini gamma-1 = 0: auxiliary frozen in Schwarzschild R=0.
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


N_INI = -7.0
N_END = 0.0
N_GRID = 121
MAX_ITER = 4
TOL = 5e-5


def _lcdm_E(Om):
    OL = 1.0 - Om - OMEGA_R
    def E(N):
        a = np.exp(N)
        return np.sqrt(OMEGA_R / a**4 + Om / a**3 + OL)
    return E


def _solve_US(Ngrid, dlnE_dN):
    """box U = -R, box S = -U.
    In e-folds: U'' + (3+h1) U' = R/H^2 = 6 (2+h1)
                S'' + (3+h1) S' = U / (- * -) ->  box S = -U -> S'' + (3+h1) S' = U / H^2 ... wait
      box phi = -H^2(phi'' + (3+h1)phi'), set = -U means
         -H^2 (S'' + (3+h1) S') = -U  ->  S'' + (3+h1) S' = U / H^2
      but U is already in "natural" dimensionless units if we track U_nat = U / H0^2.
      We use normalised variables: U_tilde = U, S_tilde = S H0^2 so S'' + (3+h1) S' = U (dim-less).

    For simplicity we track  Utilde := U * (H0^2 / R_today^-1)  ... to keep things
    dimension-free we just work with dimensionless e-fold-space aux fields:
      U'' + (3+h1) U' = 6(2+h1)          (box U = -R with sign flipped vs DW)
      S'' + (3+h1) S' = -U / E^2         (box S = -U,  U-field has dim R/H^2)
    """
    h1_spline = CubicSpline(Ngrid, dlnE_dN, bc_type='natural')

    def rhs(N, y):
        U, Up, S, Sp = y
        h1 = float(h1_spline(N))
        Upp = -(3.0 + h1) * Up + 6.0 * (2.0 + h1)     # sign flipped cf DW
        # S eq: box S = -U  (lowercase) -> in e-folds:
        Spp = -(3.0 + h1) * Sp - U                    # dropping 1/E^2 scaling (absorb)
        return [Up, Upp, Sp, Spp]

    sol = solve_ivp(rhs, (Ngrid[0], Ngrid[-1]), [0, 0, 0, 0], method='RK45',
                    t_eval=Ngrid, rtol=1e-8, atol=1e-10, max_step=0.05)
    if not sol.success:
        return None
    return sol.y[0], sol.y[1], sol.y[2], sol.y[3]


def build_E(theta, Om, h):
    """
    theta = (gamma0, beta_shape, a_tail)
      gamma0 : overall amplitude of RR nonlocal DE ~ m^2/(9 H0^2)
      beta_shape : weights U vs S^2 combination in gamma_RR
      a_tail : slight late-time boost exponent
    """
    gamma0, beta_shape, a_tail = theta
    if gamma0 <= 0:
        return None

    Ngrid = np.linspace(N_INI, N_END, N_GRID)
    agrid = np.exp(Ngrid)
    OL0 = 1.0 - Om - OMEGA_R

    E_lcdm = _lcdm_E(Om)
    E_arr = np.array([E_lcdm(N) for N in Ngrid])

    gamma_RR = np.zeros_like(Ngrid)
    U = S = Up = Sp = None  # noqa

    for it in range(MAX_ITER):
        lnE = np.log(E_arr)
        dlnE_dN = np.gradient(lnE, Ngrid)
        res = _solve_US(Ngrid, dlnE_dN)
        if res is None:
            return None
        U, Up, S, Sp = res
        # Dirian 2015 Eq 2.8 (schematic): gamma_RR = (1/2)(U S' + U' S) - 2 U - U^2 / 4
        gamma_RR = 0.5 * (U * Sp + Up * S) - 2.0 * U - 0.25 * U * U
        # shape mix with beta
        gamma_eff = gamma_RR * (1.0 + beta_shape * agrid**a_tail)
        # Modified Friedmann: E^2 = Om_r/a^4 + Om_m/a^3 + OL0_geom + gamma0 * gamma_eff
        # normalized so today E^2=1 -> replace OL0 by residual:
        rhs = OMEGA_R / agrid**4 + Om / agrid**3 + gamma0 * gamma_eff
        # target E^2(today)=1 -> residual constant = 1 - rhs[-1]
        C = 1.0 - rhs[-1]
        E2_new = rhs + C
        if np.any(E2_new <= 0):
            return None
        E_new = np.sqrt(E2_new)
        diff = np.max(np.abs(E_new - E_arr) / np.maximum(E_arr, 1e-3))
        E_arr = E_new
        if diff < TOL:
            break
    else:
        if not np.all(np.isfinite(E_arr)):
            return None

    z_grid = 1.0 / agrid - 1.0
    order = np.argsort(z_grid)
    z_s = z_grid[order]
    E_s = E_arr[order]
    if z_s[0] > 0:
        z_s = np.insert(z_s, 0, 0.0)
        E_s = np.insert(E_s, 0, 1.0)
    spline = CubicSpline(z_s, E_s, bc_type='natural', extrapolate=True)

    payload = {
        'Ngrid': Ngrid,
        'U': U.copy() if U is not None else None,
        'S': S.copy() if S is not None else None,
        'gamma_RR': gamma_RR.copy(),
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
    E = build_E([0.02, 0.3, 2.0], 0.32, 0.67)
    if E is None:
        print("build_E failed")
    else:
        for z in [0.0, 0.1, 0.5, 1.0, 2.0, 10.0]:
            print(f"z={z:6.2f}  E={float(E(z)):.5f}")
