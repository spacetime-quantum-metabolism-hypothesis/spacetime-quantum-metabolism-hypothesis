# -*- coding: utf-8 -*-
"""
L4 C5r perturbation spec.

Running Vacuum Model has no new propagating degree of freedom:
Lambda(H^2) is a running cosmological constant with only modified
continuity exchange between matter and vacuum (see Gomez-Valent-Sola
ApJ 975 64 2024, sec 2).

Consequences:
  * sub-horizon growth: mu(a) = G_eff/G = 1 (no fifth force)
  * perturbative sound speed: c_s^2 = 1 (formally vacuum - no propagation,
    but the effective fluid sound speed used in the Boltzmann hierarchy
    is set to 1 to match standard RVM pipelines)
  * static PPN: gamma - 1 = 0 exactly (no scalar, no extra polarization)

Citation: Gomez-Valent & Sola 2024, ApJ 975 64 (arXiv:2404.18981).
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
