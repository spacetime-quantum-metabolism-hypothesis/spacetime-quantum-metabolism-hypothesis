# -*- coding: utf-8 -*-
"""
L4 C6s Stringy RVM + Chern-Simons anomaly.

Background is identical to C5r Running Vacuum Model.

The Chern-Simons coupling b R R-tilde contributes via the Pontryagin density
R R-tilde, which vanishes identically on any Type-D (FLRW, Schwarzschild)
geometry. So CS drops out of the background Friedmann - C6s reduces to C5r
at background, with parameter relabelled nu -> nu_s.

Closed-form Running Vacuum (Gomez-Valent-Sola 2024):
    E^2(a) = ( Om_m0 a^-3(1-nu_s) + Om_r0 a^-4(1-nu_s)
               + (1 - Om_m0 - Om_r0 - nu_s) ) / (1 - nu_s)
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
    nu_s = float(theta[0])
    if abs(1.0 - nu_s) < 1e-6:
        return None
    if abs(nu_s) > 0.1:
        return None
    OL_shifted = 1.0 - Om - OMEGA_R - nu_s
    exp_m = 3.0 * (1.0 - nu_s)
    exp_r = 4.0 * (1.0 - nu_s)
    one_minus_nu = 1.0 - nu_s

    def E(z):
        z = np.asarray(z, dtype=float)
        onepz = 1.0 + z
        val = (Om * onepz**exp_m + OMEGA_R * onepz**exp_r + OL_shifted) / one_minus_nu
        val = np.where(val < 1e-12, 1e-12, val)
        out = np.sqrt(val)
        return float(out) if out.ndim == 0 else out

    return E


if __name__ == '__main__':
    E = build_E([-0.005], 0.3204, 0.6691)
    for z in (0.0, 0.5, 1.0, 2.0, 1100.0):
        print(f"z={z:7.2f}  E={float(E(z)):.5f}")
