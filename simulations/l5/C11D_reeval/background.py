# -*- coding: utf-8 -*-
"""
L5 Phase E re-evaluation of C11D Disformal IDE.

Rationale (see CLAUDE.md + base.l5.command.md Phase L5-E):
  The L4 verdict KILLed C11D on K3 (phantom crossing) using a leading-order
  CPL thawing template  w0 = -1 + gamma_D^2/3,  wa = -(2/3) gamma_D^2.
  That template is a low-order expansion that can artificially create a
  phantom-side w(z) when gamma_D becomes large.

  Physically, C11D is the *pure disformal* branch of Zumalacarregui-Koivisto-
  Bellini 2013 (arXiv:1210.8016) with the disformal function B(phi)=B_0 const
  and the conformal piece A(phi)=1 (i.e. A'=0).  Sakstein-Jain 2015
  (arXiv:1409.3708) and ZKB 2013 Sec IV show two crucial facts:

  1. With A'=0 the matter sector is minimally coupled at the background
     level -- the disformal piece g_tilde = g + B d_mu phi d_nu phi modifies
     only the scalar propagation, not the matter stress-energy conservation
     in the Jordan frame.  Therefore the background w(z) is exactly that of
     minimally coupled quintessence.
  2. Minimally coupled quintessence with a real scalar field and a
     standard (positive-definite) kinetic term satisfies w(z) >= -1 at ALL
     times -- phantom crossing is analytically forbidden.

  Consequence: **C11D cannot phantom-cross at the background level.** The
  L4 K3 hit is a template artifact of the leading-order CPL expansion.  In
  this re-evaluation we integrate the quintessence Klein-Gordon equation
  directly (no CPL parametrisation) with an exponential potential
  V(phi) = V0 exp(-lambda phi/M_Pl), using lambda as the dimensionless
  proxy for the disformal-coupling-induced thawing amplitude.  This is the
  Sakstein-Jain 2015 eq (2.8) background in the A'=0 limit.

Parameter mapping (dimensionless, units where M_Pl = 1, H0 = 1):
  theta = (lam,)
  lam   : exponential slope V' / V      (Sakstein-Jain 2015 lambda)
          lam -> 0 recovers LCDM; lam ~ 1 gives thawing with
          w0_today ~ -1 + O(lam^2) / 3.
"""
from __future__ import annotations

import os
import sys

import numpy as np
from scipy.integrate import solve_ivp

_HERE = os.path.dirname(os.path.abspath(__file__))
_L5 = os.path.dirname(_HERE)
_L4 = os.path.join(os.path.dirname(_L5), 'l4')
for _p in (_L5, _L4):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from common import OMEGA_R  # noqa: E402  (l4/common via l5/common sys.path)


def _solve_quint(lam: float, Om: float,
                 N_ini: float = -12.0, n_out: int = 400):
    """Forward-shoot minimally coupled quintessence with exponential V.

    Dimensionless variables (Copeland-Liddle-Wands 1998):
        x = phi' / (sqrt(6) H)            (kinetic fraction sqrt)
        y = sqrt(V) / (sqrt(3) H)         (potential fraction sqrt)
        Omega_phi = x^2 + y^2
        Omega_m   = 1 - Omega_phi - Omega_r
        w_phi     = (x^2 - y^2) / (x^2 + y^2)

    Autonomous system (with radiation):
        x' = -3 x + sqrt(6)/2 lam y^2 + 0.5 x (3 + 3(x^2 - y^2) + Omega_r)
        y' =  -sqrt(6)/2 lam x y + 0.5 y (3 + 3(x^2 - y^2) + Omega_r)
        Omega_r' = -Omega_r (1 - 3(x^2 - y^2) - Omega_r)

    We integrate forward from matter domination (x, y << 1, Omega_r determined
    by N_ini) to N=0 and shoot on the initial y so that at N=0 we get
    Omega_phi = 1 - Om - Omega_r(0).  Since Omega_r(0) = OMEGA_R << 1 and
    Om is fixed externally we solve numerically via bisection on y_ini.

    Returns (N_arr, x_arr, y_arr, Or_arr) or None on failure.
    """
    OL0_target = 1.0 - Om - OMEGA_R
    if OL0_target <= 0:
        return None

    # Radiation at N_ini: Omega_r(N_ini) ~ OMEGA_R exp(-4 N_ini) / E^2(N_ini).
    # In matter era, E^2 ~ Om e^(-3 N) + OMEGA_R e^(-4 N) so
    # Omega_r(N_ini) ~ OMEGA_R e^(-4 N_ini) / (Om e^(-3 N_ini) + OMEGA_R e^(-4 N_ini))
    Or_ini = (OMEGA_R * np.exp(-4.0 * N_ini)
              / (Om * np.exp(-3.0 * N_ini) + OMEGA_R * np.exp(-4.0 * N_ini)))

    def rhs(N, u):
        x, y, Or = u
        w_eff_term = 3.0 * (x * x - y * y) + Or  # 3 w_phi Omega_phi + Omega_r
        xp = (-3.0 * x
              + (np.sqrt(6.0) / 2.0) * lam * y * y
              + 0.5 * x * (3.0 + w_eff_term))
        yp = (-(np.sqrt(6.0) / 2.0) * lam * x * y
              + 0.5 * y * (3.0 + w_eff_term))
        Orp = -Or * (1.0 - w_eff_term)
        return [xp, yp, Orp]

    def shoot(y_ini):
        sol = solve_ivp(
            rhs, (N_ini, 0.0), [0.0, y_ini, Or_ini],
            method='RK45', rtol=1e-6, atol=1e-9, max_step=0.5,
            dense_output=True,
        )
        if not sol.success:
            return None
        x0, y0, Or0 = sol.y[:, -1]
        Om_phi = x0 * x0 + y0 * y0
        return sol, Om_phi

    # Bisection on y_ini in [1e-12, 1.0] for Omega_phi_today = OL0_target
    lo, hi = 1e-12, 1.0
    res_lo = shoot(lo); res_hi = shoot(hi)
    if res_lo is None or res_hi is None:
        return None
    f_lo = res_lo[1] - OL0_target
    f_hi = res_hi[1] - OL0_target
    if f_lo * f_hi > 0:
        # Monotone? If lam is huge we may not bracket -- expand hi
        for _ in range(6):
            hi *= 0.5
            res_hi = shoot(hi)
            if res_hi is None:
                continue
            f_hi = res_hi[1] - OL0_target
            if f_lo * f_hi < 0:
                break
        else:
            return None
    sol = None
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        res_mid = shoot(mid)
        if res_mid is None:
            return None
        f_mid = res_mid[1] - OL0_target
        if abs(f_mid) < 1e-7:
            sol = res_mid[0]
            break
        if f_lo * f_mid < 0:
            hi = mid; f_hi = f_mid
        else:
            lo = mid; f_lo = f_mid
    if sol is None:
        sol = res_mid[0]

    N_arr = np.linspace(N_ini, 0.0, n_out)
    u_arr = sol.sol(N_arr)
    return N_arr, u_arr[0], u_arr[1], u_arr[2]


def build_E(theta, Om, h):
    """theta = (lam,). Returns E(z) or None."""
    lam = float(theta[0])
    if lam < 0.0 or lam > 2.5:
        return None
    out = _solve_quint(lam, Om)
    if out is None:
        return None
    N_arr, x_arr, y_arr, Or_arr = out
    # H^2 from constraint: Omega_phi + Omega_m + Omega_r = 1 is identically
    # enforced by the autonomous system (CLW 1998).
    # We need E(N) = H(N) / H0.  Use continuity: E^2 = Omega_m(0) a^-3 +
    # Omega_r(0) a^-4 + rho_phi(N)/(3 H0^2).  But x,y are defined with H so
    # we need an independent normalisation.  Trick: use the matter fraction.
    # Omega_m(N) = (1 - x^2 - y^2 - Or).  In terms of physical matter density:
    # rho_m(N) = Omega_m(N) * 3 H(N)^2.  But rho_m a^3 = const = Om * 3 H0^2.
    # So H(N)^2 / H0^2 = Om * exp(-3 N) / Omega_m(N).
    Om_m_arr = 1.0 - x_arr * x_arr - y_arr * y_arr - Or_arr
    Om_m_arr = np.clip(Om_m_arr, 1e-12, None)
    E2 = Om * np.exp(-3.0 * N_arr) / Om_m_arr
    if np.any(E2 <= 0) or np.any(~np.isfinite(E2)):
        return None

    a_arr = np.exp(N_arr)
    z_arr = 1.0 / a_arr - 1.0
    order = np.argsort(z_arr)
    z_s = z_arr[order]
    lnE_s = 0.5 * np.log(E2[order])

    # Normalise E(z=0) = 1 exactly (bisection isn't perfect)
    lnE_s = lnE_s - lnE_s[0] if z_s[0] < 1e-6 else lnE_s

    from scipy.interpolate import interp1d
    lnE_int = interp1d(np.log1p(z_s), lnE_s, kind='cubic',
                       bounds_error=False, fill_value='extrapolate')

    def E(z):
        zv = np.asarray(z, dtype=float)
        # For very high z, use LCDM matter+radiation tail (scalar is negligible)
        hi = zv > 100.0
        out = np.empty_like(zv, dtype=float)
        if np.any(~hi):
            out[~hi] = np.exp(lnE_int(np.log1p(zv[~hi])))
        if np.any(hi):
            OL0 = 1.0 - Om - OMEGA_R
            out[hi] = np.sqrt(OMEGA_R * (1 + zv[hi]) ** 4
                              + Om * (1 + zv[hi]) ** 3
                              + OL0)  # phi is frozen at early times
        return float(out) if out.ndim == 0 else out

    return E


def w_of_z(theta, Om, z_grid=None):
    """Return w_phi(z) sampled on z_grid."""
    lam = float(theta[0])
    out = _solve_quint(lam, Om)
    if out is None:
        return None
    N_arr, x_arr, y_arr, _Or = out
    num = x_arr * x_arr - y_arr * y_arr
    den = x_arr * x_arr + y_arr * y_arr
    den = np.where(den < 1e-30, 1e-30, den)
    w = num / den
    a = np.exp(N_arr)
    z = 1.0 / a - 1.0
    order = np.argsort(z)
    z_s = z[order]
    w_s = w[order]
    if z_grid is None:
        return z_s, w_s
    from scipy.interpolate import interp1d
    w_int = interp1d(z_s, w_s, kind='cubic',
                     bounds_error=False, fill_value=(w_s[0], w_s[-1]))
    return z_grid, w_int(z_grid)


if __name__ == '__main__':
    print("L5 C11D_reeval smoke")
    for lam in [0.0, 0.3, 0.6, 1.0]:
        E = build_E([lam], 0.315, 0.67)
        if E is None:
            print(f"  lam={lam}: FAIL")
            continue
        e0 = float(E(0.0))
        e1 = float(E(1.0))
        e1100 = float(E(1100.0))
        print(f"  lam={lam:.2f}  E(0)={e0:.4f}  E(1)={e1:.3f}  E(1100)={e1100:.1f}")
        z, w = w_of_z([lam], 0.315)
        w_today = float(w[-1])
        w_min = float(np.min(w))
        print(f"    w_today={w_today:+.4f}  w_min={w_min:+.4f}")
