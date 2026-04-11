# -*- coding: utf-8 -*-
"""
L5 Phase E re-evaluation of C26 Perez-Sudarsky unimodular diffusion.

Reformulated diffusion ansatz (replaces L4 J^0 = alpha_Q * rho_c0 * H/H0):

    J^0 = alpha_Q * H * rho_m    (matter-proportional drift)

Unimodular continuity:
    drho_m/dt + 3 H rho_m = -J^0
    drho_L/dt             = +J^0

In e-folds N = ln a, this becomes **linear and closed-form**:
    drho_m/dN = -(3 + alpha_Q) rho_m
    drho_L/dN = +alpha_Q rho_m

=>  rho_m(N) = rho_m,0 * exp(-(3 + alpha_Q) N)
    rho_L(N) = rho_L,0 - alpha_Q * rho_m,0 * [exp(-(3+alpha_Q) N) - 1] / (3 + alpha_Q)

(Integration constant chosen so today's values are Om and OL0.)

Advantages vs L4 ansatz:
  * No ODE stiffness / solver fail.
  * alpha_Q > 0 drives matter -> Lambda (DESI w_a<0 direction).
  * Trivially invertible, no bisection.
  * K10 (L3 toy vs full) is trivially self-consistent: the L3 linearised
    drift `rho_m ~ Om a^-3 (1 - alpha_Q(1 - a^3))` is now the exact leading
    term of the expansion of exp(-(3+alpha_Q) N) in alpha_Q.
"""
from __future__ import annotations

import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_L5 = os.path.dirname(_HERE)
_SIMS = os.path.dirname(_L5)
_L4 = os.path.join(_SIMS, 'l4')
for _p in (_SIMS, _L4, _HERE, _L5):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from common import OMEGA_R  # noqa: E402  (l4/common via path)


def build_E(theta, Om, h):
    """theta = (alpha_Q,). Returns E(z) or None."""
    aq = float(theta[0])
    if aq < 0.0 or aq > 0.5:
        return None
    if Om <= 0 or Om >= 1:
        return None
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 <= 0:
        return None

    three_p = 3.0 + aq

    def rho_m_of_a(a):
        # rho_m / rho_c0 = Om * a^-(3 + alpha_Q)
        return Om * a ** (-three_p)

    def rho_L_of_a(a):
        # closed-form primitive of d rho_L / dN = aq * rho_m
        # rho_L(a) - rho_L(1) = aq * Om * integral_{N=0}^{N=ln a} e^{-three_p N'} dN'
        # = aq * Om * [1 - a^{-three_p}] / (three_p)    <-- careful sign
        # check: at a=1 -> 0; at a<1 -> negative (rho_L was smaller in past)
        return OL0 + (aq * Om / three_p) * (1.0 - a ** (-three_p))

    def E(z):
        zv = np.asarray(z, dtype=float)
        a = 1.0 / (1.0 + zv)
        rho_m = rho_m_of_a(a)
        rho_L = rho_L_of_a(a)
        Or = OMEGA_R * (1.0 + zv) ** 4
        E2 = Or + rho_m + rho_L
        E2 = np.where(E2 < 1e-12, 1e-12, E2)
        out = np.sqrt(E2)
        return float(out) if out.ndim == 0 else out

    # sanity: E(0) = 1 exactly by construction
    e0 = float(E(0.0))
    if not np.isfinite(e0) or abs(e0 - 1.0) > 1e-6:
        return None

    # Note: rho_L formally goes negative at very high z (a < a_crit where
    # aq*Om/three_p * (a_crit^{-three_p} - 1) = OL0).  This is fine for the
    # total E(z): matter dominates by many orders of magnitude there, so
    # E^2 = rho_m + rho_L + Or > 0 stays physical.  We guard against actual
    # E^2 <= 0 in the E callable above.

    return E


if __name__ == '__main__':
    print("L5 C26_reform smoke")
    for aq in [0.0, 0.02, 0.05, 0.1, 0.2]:
        E = build_E((aq,), 0.32, 0.67)
        if E is None:
            print(f"  aq={aq}: FAIL")
            continue
        vals = [float(E(z)) for z in [0.0, 0.5, 1.0, 2.0, 5.0, 30.0, 1100.0]]
        print(f"  aq={aq}: E={[f'{v:.3f}' for v in vals]}")
