# -*- coding: utf-8 -*-
"""
L4 C6s perturbation spec.

Stringy Running Vacuum + Chern-Simons anomaly: no new propagating scalar
at background level (CS axion is frozen because Pontryagin vanishes on FLRW).

  mu(a) = G_eff/G = 1   (no fifth force)
  c_s^2 = 1             (effective vacuum-like)
  gamma - 1 = 0         (exact; CS is Kerr-only for solar-system tests)

Reference: Alexander-Yunes Phys Rept 480 (2009) 1; Gomez-Valent-Sola 2024.
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
