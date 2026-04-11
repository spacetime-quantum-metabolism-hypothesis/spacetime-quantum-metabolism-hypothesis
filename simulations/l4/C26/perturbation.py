# -*- coding: utf-8 -*-
"""
C26 Perez-Sudarsky unimodular diffusion linear perturbations.

The diffusion is a pure background phenomenon at leading order: the
matter -> Lambda current J^0 is a homogeneous source that does not
introduce a new propagating scalar degree of freedom (Perez, Sudarsky,
Bjorken 2019 Sec 4).  Therefore at sub-horizon scales the linear
perturbation equations reduce to LCDM with a slightly renormalised
matter fraction, i.e.

    mu(a) = G_eff / G = 1

No ghost, no extra sound speed: c_s^2 = 1 (tensor sector unmodified,
scalar sector unchanged because J^0 carries no fluctuation).  Static
PPN gamma - 1 = 0 (no fifth force).
"""
from __future__ import annotations


def mu_func(theta, Om):
    def mu(a):
        return 1.0
    return mu


def gamma_minus_one(theta):
    return 0.0


def cs2_min(theta):
    return 1.0
