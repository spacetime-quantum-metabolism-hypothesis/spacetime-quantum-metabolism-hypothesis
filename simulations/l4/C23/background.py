# -*- coding: utf-8 -*-
"""
L4 C23 Asymptotic Safety effective Running Vacuum
(Bonanno-Platania 2018, arXiv:1803.03281; Platania 2020).

RG identification k = xi H (xi = O(1)) produces

    Lambda_eff(H) = Lambda_0 + nu_eff (H^2 - H0^2)

yielding a closed-form Friedmann identical in structure to C5r RVM
with nu -> nu_eff.

Unitarity bound (Sola 2022):
    |nu_eff| < 0.03      # hard prior, enforced here via build_E rejection
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


NU_MAX = 0.03  # Sola unitarity bound (hard |nu_eff| cutoff)


def build_E(theta, Om, h):
    """theta = (nu_eff,). Rejects |nu_eff| >= NU_MAX."""
    nu_eff = float(theta[0])
    if abs(nu_eff) >= NU_MAX:
        return None
    if abs(1.0 - nu_eff) < 1e-6:
        return None
    OL_shifted = 1.0 - Om - OMEGA_R - nu_eff
    exp_m = 3.0 * (1.0 - nu_eff)
    exp_r = 4.0 * (1.0 - nu_eff)
    one_minus_nu = 1.0 - nu_eff

    def E(z):
        z = np.asarray(z, dtype=float)
        onepz = 1.0 + z
        val = (Om * onepz**exp_m + OMEGA_R * onepz**exp_r + OL_shifted) / one_minus_nu
        val = np.where(val < 1e-12, 1e-12, val)
        out = np.sqrt(val)
        return float(out) if out.ndim == 0 else out

    return E


if __name__ == '__main__':
    for ne in (-0.02, -0.005, 0.0, 0.01, 0.025, 0.035):
        E = build_E([ne], 0.3204, 0.6691)
        if E is None:
            print(f"nu_eff={ne:+.3f} rejected")
            continue
        vals = [float(E(z)) for z in (0.0, 0.5, 1.0, 2.0, 1100.0)]
        print(f"nu_eff={ne:+.3f}  {vals}")
