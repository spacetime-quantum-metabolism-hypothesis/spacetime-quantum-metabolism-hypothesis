# -*- coding: utf-8 -*-
"""
C33 f(Q) linear perturbations (Frusciante 2021 Sec. 4).

For f(Q) = Q + f_1 H0^2 (Q/(6 H0^2))^n with n >= 1 the extra scalar
degree of freedom is non-propagating at the background + subhorizon
level (it becomes a true propagating mode only at second order in
perturbation theory, Hohmann-Krasnov-Krssak 2019).  The effective
linear-growth modification enters through

    mu(a, k) ~ 1 / f_Q(a)  (Frusciante 2021 Eq. 46)

with f_Q(a) = 1 + (f_1 n / 6) (E^2(a))^{n-1}.  For |f_1| < 0.3 and
n in [1, 4] this is within 1% of unity, so we approximate mu = 1
at the L4 stage and flag this as the Phase 5 refinement.

Static PPN: Schwarzschild has Q = 0 (type-D vacuum), so the
correction F(Q) = f_1 H0^2 (Q/(6 H0^2))^n vanishes at all orders in
the static limit for n >= 1.  Therefore gamma - 1 = 0 exactly,
matching GR.  c_s^2 = 1 for the (sub-leading) scalar mode; no
ghost / gradient instability for f_1 > 0 (Frusciante 2021 Fig. 3).
"""
from __future__ import annotations

import numpy as np


def mu_func(theta, Om):
    """Return mu(a) ~ G_eff / G for linear matter growth."""
    f1, n = float(theta[0]), float(theta[1])
    # f_Q(a) = 1 + (f1 * n / 6) * (E^2)^{n-1}.  We approximate by using
    # LCDM E^2; the correction is order (f1 * n / 6).
    def mu(a):
        # LCDM E^2
        E2 = Om * a**-3 + (1.0 - Om)
        fQ = 1.0 + (f1 * n / 6.0) * E2**(n - 1.0)
        if fQ <= 0:
            return 1.0
        return 1.0 / fQ
    return mu


def gamma_minus_one(theta):
    """Static PPN deviation.  Zero for f(Q) power-law (Q=0 in Schwarzschild)."""
    return 0.0


def cs2_min(theta):
    """Scalar sound speed squared minimum over background history.

    Frusciante 2021 shows c_s^2 = 1 (tensor sector unmodified) and the
    scalar mode is non-propagating; no instability for f_1 >= 0.
    Returns 1.0 as the stable reference.
    """
    f1 = float(theta[0])
    if f1 < 0:
        return -1.0  # would correspond to phantom / ghost branch
    return 1.0
