# -*- coding: utf-8 -*-
"""
L4 C11D Disformal IDE background (Zumalacarregui-Koivisto-Bellini 2013,
arXiv:1210.8016; Sakstein-Jain 2017 disformal quintessence).

Pure disformal coupling: g_tilde_{mu nu} = g_{mu nu} + B(phi) partial phi partial phi
with A' = 0 (so static gamma - 1 = 0 exactly, Z-K-B 2013 Sec IV).

For the background we use the thawing disformal quintessence template:
  * Matter-phi coupling of strength gamma_D (dimensionless)
  * Effective w(a) = w0 + wa (1 - a) with analytic leading-order expressions
    derived from the slow-roll disformal Klein-Gordon equation around a
    thawing point at early times.

Derivation (Sakstein-Jain 2017 eq 3.8-3.15 simplified):
  phi'' + 3 H phi' + (1 + 2 B rho_m / M_Pl^2) V_phi = 0
  with B = gamma_D^2 / M_eff^2, constant.

Leading-order thawing gives:
  w0_eff = -1 + gamma_D^2 / 3   (stiffening from matter drag)
  wa_eff = -(2/3) gamma_D^2     (late-time growth of w)

Implementation: build E(z) from CPL form using these (w0, wa) as a function of
gamma_D; self-consistent Om normalisation at a = 1.

This is a deliberate analytic template (hi_class disformal branch unavailable
in this env). The k2_rejudge.md scans the full gamma_D range.
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


def cpl_w(gamma_D):
    g2 = float(gamma_D) ** 2
    w0 = -1.0 + g2 / 3.0
    wa = -(2.0 / 3.0) * g2
    return w0, wa


def build_E(theta, Om, h):
    """theta = (gamma_D,). Returns E(z)."""
    gamma_D = float(theta[0])
    if gamma_D < 0.0 or gamma_D > 3.5:
        return None
    w0, wa = cpl_w(gamma_D)
    OL0 = 1.0 - Om - OMEGA_R

    def rho_de_ratio(a):
        # standard CPL: rho_de(a)/rho_de(a=1) = a^(-3(1+w0+wa)) exp(-3 wa (1-a))
        return a ** (-3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * (1.0 - a))

    def E(z):
        z = np.asarray(z, dtype=float)
        a = 1.0 / (1.0 + z)
        val = (OMEGA_R * (1.0 + z) ** 4
               + Om * (1.0 + z) ** 3
               + OL0 * rho_de_ratio(a))
        val = np.where(val < 1e-12, 1e-12, val)
        out = np.sqrt(val)
        return float(out) if out.ndim == 0 else out

    return E


if __name__ == '__main__':
    for g in [0.0, 0.3, 0.5, 1.0, 2.0, 3.0]:
        E = build_E([g], 0.315, 0.67)
        w0, wa = cpl_w(g)
        print(f"gamma_D={g:.2f}  w0={w0:+.4f}  wa={wa:+.4f}  E(1100)={float(E(1100.0)):.1f}")
