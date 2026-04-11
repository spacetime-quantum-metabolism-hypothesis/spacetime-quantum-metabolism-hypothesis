# -*- coding: utf-8 -*-
"""
L4 C27 linear perturbations.

For Deser-Woodard R f(box^-1 R) models, Dirian-Foffa-Kehagias-Rio-Maggiore 2015
(arXiv:1411.3073) Sec 4 shows:
  * linear scalar mode propagates but is weakly coupled in sub-horizon limit,
  * effective G_eff / G ~ 1 / (1 + f(U) + (1/2) U f'(U)) to leading order,
  * sound speed c_s^2 = 1 for the propagating mode (no gradient instability
    in the branch with c0 < 0; we check sign here numerically).

Cassini: Schwarzschild has R = 0 -> auxiliary U frozen -> gamma - 1 = 0 exact
(Koivisto 2008 PRD 77 123513 Sec IV.B).
"""
from __future__ import annotations

import numpy as np


def mu_of_a_factory(payload, c0, X_shift, dX):
    """G_eff/G = 1/(1 + f(U(a)) + (1/2) U f'(U)).  Clamped near 1."""
    if payload is None or payload.get('U') is None:
        return lambda a: 1.0
    Ngrid = payload['Ngrid']
    U = payload['U']
    a_grid = np.exp(Ngrid)
    fU = c0 * np.tanh((U - X_shift) / dX)
    fpU = (c0 / dX) * (1.0 - np.tanh((U - X_shift) / dX) ** 2)
    denom = 1.0 + fU + 0.5 * U * fpU
    mu = 1.0 / np.where(np.abs(denom) > 1e-3, denom, 1e-3)

    def mu_of_a(a):
        return float(np.interp(a, a_grid, mu, left=mu[0], right=mu[-1]))

    return mu_of_a


def sound_speed_sq(payload, c0, X_shift, dX):
    """c_s^2 of the scalar propagating mode.  Dirian 2015: asymptotically 1;
    return min over trajectory of the leading quadratic kinetic coefficient.
    We approximate by (1 - (1/6) f''(U) * (U')^2); negative -> ghost/gradient.
    """
    if payload is None or payload.get('U') is None:
        return 1.0
    Ngrid = payload['Ngrid']
    U = payload['U']
    dU_dN = np.gradient(U, Ngrid)
    tanh_arg = (U - X_shift) / dX
    fpp = (c0 / dX ** 2) * (-2.0) * np.tanh(tanh_arg) * (1.0 - np.tanh(tanh_arg) ** 2)
    cs2 = 1.0 - (1.0 / 6.0) * fpp * dU_dN ** 2
    return float(np.min(cs2))


def gamma_minus_one_static() -> float:
    """Schwarzschild has R=0 so U is frozen at cosmological background value.
    Koivisto 2008 PRD 77 123513 Sec IV.B: gamma - 1 = 0 exact for R f(box^-1 R)
    in a vacuum Ricci-flat background.
    """
    return 0.0
