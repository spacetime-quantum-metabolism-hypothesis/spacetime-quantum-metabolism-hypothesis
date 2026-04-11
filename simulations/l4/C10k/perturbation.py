# -*- coding: utf-8 -*-
"""
L4 C10k perturbation spec.

Dark-only coupled quintessence (Amendola 2000 Sec IV):
  * Baryons Einstein-frame -> static gamma - 1 = 0 exact.
  * CDM feels G_eff/G = 1 + 2 beta_d^2 (constant, unscreened).
  * Linear growth ODE uses mu(a) = 1 + 2 beta_d^2 as a constant (slow-roll).
  * Quintessence sound speed c_s^2 = 1.
"""
from __future__ import annotations


def mu_of_a(beta_d):
    b = float(beta_d)
    val = 1.0 + 2.0 * b * b
    def mu(a):
        return val
    return mu


def cs2(_a=None):
    return 1.0


def gamma_minus_one_static(_beta_d):
    return 0.0  # dark-only, baryons decoupled


def ghost_free(_beta_d):
    return True
