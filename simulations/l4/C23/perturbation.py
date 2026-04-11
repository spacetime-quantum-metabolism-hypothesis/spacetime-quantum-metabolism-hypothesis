# -*- coding: utf-8 -*-
"""
L4 C23 perturbation spec.

Asymptotic Safety effective RVM: at the effective FLRW level there is no
new propagating degree of freedom; the RG-running of Lambda is encoded as
a non-derivative source in the Friedmann equation. Sub-horizon linear
growth is therefore identical to Running Vacuum / LCDM to leading order:

  mu(a) = G_eff / G = 1
  c_s^2 = 1  (effective, vacuum-like)
  gamma - 1 = 0  (no scalar, solar system PPN unchanged)

Reference: Bonanno-Platania 2018 (arXiv:1803.03281); Platania 2020 review.
"""
from __future__ import annotations


def mu_of_a(_theta=None):
    def mu(_a):
        return 1.0
    return mu


def sound_speed_sq(_a=None):
    return 1.0


def gamma_minus_one_static(_theta=None):
    return 0.0


def ghost_free(_theta=None):
    return True
