# -*- coding: utf-8 -*-
"""
L4 C11D perturbation spec.

Pure disformal (A' = 0) Zumalacarregui-Koivisto-Bellini 2013 Sec IV:
  * Static spherically symmetric: disformal transformation leaves Schwarzschild
    structure intact -> gamma - 1 = 0 exact.
  * Scalar sound speed c_s^2 = 1 + small disformal correction. For |B rho/M^2|
    < 1 and pure disformal the scalar kinetic term stays positive; we take
    c_s^2 = 1 / (1 + gamma_D^2 * Omega_m_today) as a safe leading proxy.
  * Linear growth picks up G_eff/G = 1 (pure disformal has no conformal piece
    driving matter; the coupling is kinetic).
"""
from __future__ import annotations


def mu_of_a(_gamma_D):
    def mu(a):
        return 1.0
    return mu


def cs2(gamma_D, Om_today=0.315):
    g2 = float(gamma_D) ** 2
    return 1.0 / (1.0 + g2 * Om_today)


def gamma_minus_one_static(_gamma_D):
    return 0.0


def ghost_free(gamma_D, Om_today=0.315):
    return cs2(gamma_D, Om_today) > 0.0
