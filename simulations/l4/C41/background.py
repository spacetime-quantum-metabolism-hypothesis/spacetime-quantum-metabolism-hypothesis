# -*- coding: utf-8 -*-
"""
L4 C41 Wetterich / Amendola fluid IDE background.

Coupled continuity (w_DE = -1 effective, Q = H beta rho_DE):
  d rho_m / dN  = -3 rho_m + 3 beta rho_DE
  d rho_DE / dN = -3 beta rho_DE

Closed form (exact for this toy, valid beta != 1):
  rho_DE(a) = OL0 * a^(-3 beta)
  rho_m(a)  = A * a^(-3 beta) + B * a^(-3)
  A = beta / (1 - beta) * OL0
  B = Om - A    (so that rho_m(a=1) = Om)

SQMH sign: beta >= 0 (matter -> DE flow, DESI direction).
Toy validity window: |beta| <= 0.1 (linear regime).
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
    """theta = (beta,). Returns callable E(z) or None on failure."""
    beta = float(theta[0])
    if beta < 0.0 or beta >= 0.5:
        return None
    OL0 = 1.0 - Om - OMEGA_R
    A = beta * OL0 / (1.0 - beta)
    B = Om - A

    def E(z):
        z = np.asarray(z, dtype=float)
        a = 1.0 / (1.0 + z)
        rm = A * a**(-3.0 * beta) + B * a**(-3.0)
        rDE = OL0 * a**(-3.0 * beta)
        Or = OMEGA_R * (1.0 + z)**4
        rm = np.where(rm < 0, 0.0, rm)
        val = rm + rDE + Or
        val = np.where(val < 1e-12, 1e-12, val)
        out = np.sqrt(val)
        return float(out) if out.ndim == 0 else out

    return E


if __name__ == '__main__':
    E = build_E([0.03], 0.32, 0.67)
    for z in [0.0, 0.5, 1.0, 2.0, 1100.0]:
        print(f"z={z:8.2f}  E={float(E(z)):.6f}")
