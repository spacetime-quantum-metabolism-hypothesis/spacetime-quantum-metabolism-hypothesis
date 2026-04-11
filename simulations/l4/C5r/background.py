# -*- coding: utf-8 -*-
"""
L4 C5r Running Vacuum Model (Gomez-Valent-Sola 2024, ApJ 975 64).

Lambda(H^2) = Lambda_0 + 3 nu H^2.
Modified Friedmann (closed form, valid for |nu| << 1):

    E^2(a) = ( Om_m0 a^-3(1-nu) + Om_r0 a^-4(1-nu)
               + (1 - Om_m0 - Om_r0 - nu) ) / (1 - nu)

SQMH sign: nu < 0 (matter -> Lambda drift, w_a < 0 direction).
No scalar degree of freedom -> gamma - 1 = 0 exactly.

Fast, closed form. No ODE, no blow-up.
"""
from __future__ import annotations

import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_L4 = os.path.dirname(_HERE)
if _L4 not in sys.path:
    sys.path.insert(0, _L4)

from common import OMEGA_R  # noqa: E402


def build_E(theta, Om, h):
    """theta = (nu,). Returns callable E(z) or None on failure."""
    nu = float(theta[0])
    if abs(1.0 - nu) < 1e-6:
        return None
    if abs(nu) > 0.1:
        return None
    OL_shifted = 1.0 - Om - OMEGA_R - nu
    exp_m = 3.0 * (1.0 - nu)
    exp_r = 4.0 * (1.0 - nu)
    one_minus_nu = 1.0 - nu

    def E(z):
        z = np.asarray(z, dtype=float)
        onepz = 1.0 + z
        val = (Om * onepz**exp_m + OMEGA_R * onepz**exp_r + OL_shifted) / one_minus_nu
        val = np.where(val < 1e-12, 1e-12, val)
        out = np.sqrt(val)
        return float(out) if out.ndim == 0 else out

    return E


if __name__ == '__main__':
    for nu in (-0.01, 0.0, 0.01):
        E = build_E([nu], 0.3204, 0.6691)
        vals = [float(E(z)) for z in (0.0, 0.5, 1.0, 2.0, 1100.0)]
        print(f"nu={nu:+.3f}  E(z=0,0.5,1,2,1100) = {vals}")
