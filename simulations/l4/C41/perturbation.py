# -*- coding: utf-8 -*-
"""
L4 C41 perturbation spec.

For Wetterich/Amendola fluid IDE with Q = H beta rho_DE:
  * Dark sector coupling (both baryons + CDM unless dark-only specified).
    For fluid toy we treat coupling as universal in matter sector.
  * In conformal Newtonian gauge, the coupled-fluid growth equation includes
    a drag term beta * phi_N * delta_m (Amendola 2000, Di Porto-Amendola 2008):
      delta_m'' + (2 + H'/H - beta phi_N') delta_m' =
          (3/2) Omega_m mu(a) delta_m
    where mu(a) = 1 + 2 beta^2 in the slow-roll limit.
  * For small beta ( <= 0.1 ) we approximate mu_of_a = 1 + 2 beta^2 (constant).
  * Sound speed: effective fluid c_s^2 = 1 (quintessence-like), always > 0.
  * Static PPN: beta couples to the whole matter sector so strictly gamma - 1
    != 0, but the Phase 2/3 SQMH embedding treats baryons as decoupled (only
    matter-phi exchange) - we report gamma - 1 = 0 only under that caveat.
    For C41 as a universal fluid toy we take gamma - 1 = 2 beta^2 / (1 + beta^2)
    and flag Cassini manually in result.json.
"""
from __future__ import annotations

import numpy as np


def mu_of_a(beta):
    """G_eff/G (slow-roll). Constant for the toy linear regime."""
    b = float(beta)
    val = 1.0 + 2.0 * b * b
    def mu(a):
        return val
    return mu


def cs2(_a=None):
    """Effective quintessence-like sound speed."""
    return 1.0


def gamma_minus_one_static(beta):
    """Universal fluid coupling -> Cassini sensitive.
    |gamma - 1| = 2 beta^2 / (1 + beta^2).
    """
    b = float(beta)
    return 2.0 * b * b / (1.0 + b * b)


def ghost_free(_beta):
    return True  # fluid toy, no kinetic ghost
