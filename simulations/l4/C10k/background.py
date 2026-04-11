# -*- coding: utf-8 -*-
"""
L4 C10k dark-only coupled quintessence background.

Amendola 2000 dark-only: CDM couples to phi via Q = beta_d rho_c phi_dot.
Baryons stay in Einstein frame -> Cassini gamma - 1 = 0 exact.

Background is the C10k L3 fluid toy with effective constant w:
  w_eff = -1 + (2/3) beta_d^2   (exact to leading order in beta_d; phantom-safe)
  rho_DE(a) = OL0 * a^(-3 (1 + w_eff)) = OL0 * a^(-2 beta_d^2)
Matter: rho_c(a) = Om_c * a^(-3) (uncoupled because we switch to the Jordan
frame of CDM where the scalar-matter coupling absorbs into rescaled mass; at
the background level to leading order in beta_d the matter dilution remains
a^-3 and the coupling shows up only as the shift in w_eff).

This is a structural w_a = 0 model at the background level; the L4 re-assessment
is via the GROWTH channel (G_eff/G = 1 + 2 beta_d^2 on CDM).
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


def w_eff(beta_d):
    b = float(beta_d)
    return -1.0 + (2.0 / 3.0) * b * b


def build_E(theta, Om, h):
    """theta = (beta_d,). Returns E(z)."""
    beta_d = float(theta[0])
    if beta_d < 0.0 or beta_d > 0.25:
        return None
    w = w_eff(beta_d)
    OL0 = 1.0 - Om - OMEGA_R
    exponent = -3.0 * (1.0 + w)  # = -2 beta_d^2

    def E(z):
        z = np.asarray(z, dtype=float)
        a = 1.0 / (1.0 + z)
        val = (OMEGA_R * (1.0 + z) ** 4
               + Om * (1.0 + z) ** 3
               + OL0 * a ** exponent)
        val = np.where(val < 1e-12, 1e-12, val)
        out = np.sqrt(val)
        return float(out) if out.ndim == 0 else out

    return E


if __name__ == '__main__':
    for bd in [0.0, 0.05, 0.10, 0.15]:
        E = build_E([bd], 0.315, 0.67)
        print(f"beta_d={bd:.3f}  w_eff={w_eff(bd):+.5f}  E(1)={float(E(1.0)):.4f}")
