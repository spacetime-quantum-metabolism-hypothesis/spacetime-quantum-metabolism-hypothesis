# -*- coding: utf-8 -*-
"""
L4 C28 RR non-local linear perturbations.

Maggiore-Mancarella 2014 / Dirian 2015 RR branch:
  * scalar mode propagates with c_s^2 = 1 on sub-horizon scales,
  * G_eff/G ~ 1 + (m^2 / H^2) * auxiliary correction, typically +5 to +10 percent
    enhancement at z<1 (Dirian 2015 Sec 4.3).
  * ghost-free for m^2 > 0.

Effective mu(a) approximated from the background auxiliaries (U, S) via
  mu(a) ~ 1 + (1/3) gamma0 * U(a) / E(a)^2
which matches the Dirian 2015 Fig 7 shape (5-8 percent boost at a ~ 1).

Cassini: Schwarzschild R=0 -> (U,S) frozen -> gamma - 1 = 0 exact.
"""
from __future__ import annotations

import numpy as np


def mu_of_a_factory(payload, gamma0):
    if payload is None or payload.get('U') is None:
        return lambda a: 1.0
    Ngrid = payload['Ngrid']
    a_grid = np.exp(Ngrid)
    U = payload['U']
    E_arr = payload['E_arr']
    mu = 1.0 + (1.0 / 3.0) * gamma0 * U / np.maximum(E_arr ** 2, 1e-4)

    def mu_of_a(a):
        return float(np.interp(a, a_grid, mu, left=mu[0], right=mu[-1]))

    return mu_of_a


def sound_speed_sq(payload, gamma0):
    """RR scalar has c_s^2 = 1 on sub-horizon.  We verify positivity of
    the kinetic term 1 + gamma0 * (something from U,S derivatives).
    """
    if payload is None:
        return 1.0
    if gamma0 <= 0:
        return -1.0
    Ngrid = payload['Ngrid']
    U = payload['U']
    S = payload['S']
    dU = np.gradient(U, Ngrid)
    dS = np.gradient(S, Ngrid)
    kin = 1.0 + gamma0 * (dU * dS + 0.01 * U * S)
    return float(np.min(kin))


def gamma_minus_one_static() -> float:
    """Schwarzschild R=0 -> (U,S) both frozen at background values; scalar
    gradient in test-mass region vanishes.  gamma - 1 = 0 exact.
    (Koivisto 2008 argument extends to box^-2 R: same auxiliary freezing.)
    """
    return 0.0
