# -*- coding: utf-8 -*-
"""
C33 f(Q) teleparallel background (Frusciante 2021, arXiv:2103.11823).

Model: f(Q) = Q + f_1 * H0^2 * (Q / (6 H0^2))^n,  n >= 1.

In flat FLRW with Q = 6 H^2 the modified Friedmann equation
(Jimenez, Heisenberg, Koivisto, Pekar 2020 arXiv:1906.10027 Eq. 17;
Frusciante 2021 Eq. 13) reads

    6 H^2 f_Q - (1/2) f = rho_matter  (8 pi G = 1 units)

which, after substituting f = Q + F and simplifying, becomes

    E^2 = Om a^-3 + Or a^-4 + (f_1 / 6) (1 - 2n) * E^(2n)              (*)

At a = 1, E = 1 closure yields OL0 = (f_1/6)(1-2n)(1 - 1) = 0 only if
f_1 is tied to OL0, which removes the free parameter.  To keep the
standard flat closure (1 = Om + Or + OL0) while retaining f_1, n as
perturbations around LCDM we use the "deviation from LCDM" form
(Anagnostopoulos-Basilakos-Saridakis 2021 arXiv:2104.15123, Eq. 2.14
recast),

    E^2 = Om a^-3 + Or a^-4 + OL0 + (f_1 / 6) (1 - 2n) (E^(2n) - 1)    (**)

which is identical to (*) up to the constant shift that absorbs OL0
and reduces exactly to LCDM at f_1 = 0.  Solve for E^2 at each z via
brentq.

Sign note: only f_1 >= 0 gives a well-posed expanding solution for
n >= 1 (the f_1 < 0 branch has no root of (**) for z > 0; numerically
verified over f_1 in [-0.3, 0.3]).  See sign_verification.md.
"""
from __future__ import annotations

import os
import sys

_THIS = os.path.dirname(os.path.abspath(__file__))
_L4 = os.path.dirname(_THIS)
_SIMS = os.path.dirname(_L4)
for _p in (_SIMS, _L4):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np
from scipy.optimize import brentq

from common import OMEGA_R


def build_E(theta, Om, h):
    """Return E(z) callable for f(Q) model with theta = (f_1, n).

    Returns None on blow-up (no bracket root for any requested z).
    """
    f1, n = float(theta[0]), float(theta[1])
    if n < 1.0 or n > 4.5:
        return None
    if f1 < -0.6 or f1 > 0.6:
        return None
    OL0 = 1.0 - Om - OMEGA_R
    c = (f1 / 6.0) * (1.0 - 2.0 * n)  # coefficient of (E^{2n} - 1)

    def _solve(z):
        a = 1.0 / (1.0 + z)
        rhs0 = Om * a**-3 + OMEGA_R * a**-4 + OL0  # LCDM RHS
        # g(E2) = E2 - rhs0 - c*(E2^n - 1)
        def g(E2):
            return E2 - rhs0 - c * (E2**n - 1.0)
        # LCDM guess
        E2_lcdm = rhs0
        # Bracket: search log-space around LCDM for a sign change.
        lo = max(1e-8, 1e-6 * E2_lcdm)
        hi = max(1.0, 1e6 * max(E2_lcdm, 1.0))
        try:
            g_lo = g(lo)
            g_hi = g(hi)
            if not (np.isfinite(g_lo) and np.isfinite(g_hi)):
                return np.nan
            if g_lo * g_hi > 0:
                # scan
                grid = np.logspace(np.log10(lo), np.log10(hi), 64)
                vals = np.array([g(v) for v in grid])
                sig = np.sign(vals)
                found = False
                for i in range(len(sig) - 1):
                    if sig[i] * sig[i + 1] < 0:
                        lo, hi = grid[i], grid[i + 1]
                        found = True
                        break
                if not found:
                    return np.nan
            E2 = brentq(g, lo, hi, xtol=1e-12, maxiter=120)
            return float(np.sqrt(E2))
        except Exception:
            return np.nan

    # Sanity: z = 0 must give E ~= 1.
    e0 = _solve(0.0)
    if not np.isfinite(e0) or abs(e0 - 1.0) > 1e-3:
        return None

    # Pre-compute on a log-spaced z grid for fast interpolation.
    z_grid = np.concatenate([[0.0],
                             np.logspace(-3, np.log10(1500.0), 90)])
    E_grid = np.array([_solve(float(z)) for z in z_grid])
    if np.any(~np.isfinite(E_grid)):
        return None
    lnE_grid = np.log(E_grid)
    ln1pz_grid = np.log1p(z_grid)

    def E(z):
        zv = np.asarray(z, dtype=float)
        return np.exp(np.interp(np.log1p(zv), ln1pz_grid, lnE_grid))

    return E


if __name__ == '__main__':
    for n in [1.5, 2.0, 3.0]:
        for f1 in [0.0, 0.05, 0.1, 0.2]:
            E = build_E((f1, n), 0.32, 0.67)
            if E is None:
                print(f"n={n} f1={f1}: FAIL")
                continue
            vals = [float(E(z)) for z in [0.0, 0.5, 1.0, 2.0, 5.0, 1100.0]]
            print(f"n={n} f1={f1}: E={vals}")
