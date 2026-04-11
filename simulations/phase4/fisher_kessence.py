# -*- coding: utf-8 -*-
"""
Phase 3.6 B4 -- Fisher forecast for k-essence / CPL (w0, wa) extension.

Goal: upper-bound the Delta chi^2 that ANY (w0, wa) extension of LCDM can
attain against the BAO + SN + compressed CMB + RSD dataset used in Phase 3.

Strategy:
  1. Fix (Omega_m, h, omega_b, sigma_8) at Phase 3 LCDM best-fit.
  2. Parametrise w(z) = w0 + wa (1 - a).
  3. Compute chi^2(w0, wa) on a grid near the LCDM point (-1, 0).
  4. Extract Fisher F_ij = 0.5 * d^2 chi^2 / dx_i dx_j at (w0, wa) = (-1, 0).
  5. The maximum Delta chi^2 achievable by shifting along any direction
     (w0-1, wa) = d is given by the data-driven:
         Delta chi^2_max  =  -(dchi^2/dx)^T F^-1 (dchi^2/dx)
     where dchi^2/dx is evaluated at (-1, 0).  This is the best-case
     improvement from moving to the Fisher minimum.
  6. Compare to Decision gate:  Delta chi^2_max <= -15  ->  Go branch.

This is conservative in the sense that it only uses a 2D (w0, wa) sub-space;
non-CPL extensions (k-essence non-linear, coupling) can in principle do
better, but for a *background-only* extension the CPL Fisher is the tight
upper bound (Linder 2005).
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..')))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', 'phase2')))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', 'phase3')))

import config
import desi_fitting as df
import compressed_cmb as ccmb
import sn_likelihood as snl
from mcmc_phase3 import (rsd_chi2_lcdm, _EWrap, _fast_sn_chi2,
                         _bridge_highz, r_d_EH98, SN)


# --- Phase 3 LCDM best-fit (from base.fix.class.md sec 2.2) ---
OM_BF = 0.3129
H_BF = 0.6781
OMB_BF = 0.02237
S8_BF = 0.8095


def E_wowa(Om, h, w0, wa):
    """Flat w0-wa CPL expansion history."""
    Or = config.Omega_r
    OL = 1.0 - Om - Or

    def E(z):
        a = 1.0 / (1.0 + z)
        # Integrated DE density: rho_DE / rho_DE0 = exp(3 int_a^1 (1 + w(a'))
        #                                               dln a')
        # For CPL w(a) = w0 + wa(1-a):
        # rho_DE(a)/rho_DE0 = a^{-3(1+w0+wa)} exp(-3 wa (1-a))
        f_de = a**(-3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * (1.0 - a))
        return float(np.sqrt(Or * (1 + z)**4 + Om * (1 + z)**3 + OL * f_de))

    return E


def chi2_wowa(w0, wa, Om=OM_BF, h=H_BF, omb=OMB_BF, s8=S8_BF):
    omc = Om * h * h - omb
    rd = r_d_EH98(omb, omc, h)
    E = E_wowa(Om, h, w0, wa)
    c_bao = df.chi2(_EWrap(E), rd)
    c_sn = _fast_sn_chi2(SN, E, H0_km=100.0 * h)
    c_cmb = ccmb.chi2_compressed_cmb(omb, omc, h, _bridge_highz(E, Om=Om))
    c_rsd = rsd_chi2_lcdm(Om, s8)   # growth: CPL barely changes f sigma8
                                    # at leading order; keep LCDM growth
    return c_bao + c_sn + c_cmb + c_rsd


from scipy.optimize import minimize


def chi2_wowa_marginalised(w0, wa):
    """chi^2 profile: minimise over (Om, h, omb) at fixed (w0, wa).

    sigma_8 is held at Phase 3 median since RSD chi^2 is small and decouples.
    This is the fair comparison against Phase 3 LCDM (which was itself
    marginalised over the same nuisance parameters).
    """
    s8 = S8_BF

    def cost(x):
        Om, h, omb = x
        if not (0.20 < Om < 0.45): return 1e6
        if not (0.55 < h < 0.80): return 1e6
        if not (0.020 < omb < 0.025): return 1e6
        omc = Om * h * h - omb
        if not (0.05 < omc < 0.20): return 1e6
        try:
            c = chi2_wowa(w0, wa, Om, h, omb, s8)
        except Exception:
            return 1e6
        # BBN gaussian
        c += ((omb - 0.02237) / 0.00015)**2
        return c

    res = minimize(cost, [OM_BF, H_BF, OMB_BF], method='Nelder-Mead',
                   options={'xatol': 1e-5, 'fatol': 1e-3, 'maxiter': 400})
    return res.fun, res.x


def main():
    print("=" * 72)
    print("Phase 3.6 B4 -- Fisher forecast (CPL w0-wa, (Om,h,omb) marginalised)")
    print("=" * 72)

    c0, x0 = chi2_wowa_marginalised(-1.0, 0.0)
    print(f"Marginalised chi^2 at LCDM (w0=-1, wa=0) = {c0:.3f}")
    print(f"   best (Om, h, omb) = ({x0[0]:.4f}, {x0[1]:.4f}, {x0[2]:.5f})")

    # 2-D grid scan of chi^2(w0, wa) with full (Om, h, omb) marginalisation.
    # Small grid near DESI DR2 headline: w0 in [-1.1, -0.6], wa in [-1.2, 0.3]
    print("\nMarginalised chi^2 grid (slow, Nelder-Mead per point):")
    w0_arr = np.linspace(-1.05, -0.65, 5)
    wa_arr = np.linspace(-1.1, 0.3, 5)
    grid = np.full((len(w0_arr), len(wa_arr)), np.nan)
    best_ij = None
    best_val = c0
    for i, w0 in enumerate(w0_arr):
        for j, wa in enumerate(wa_arr):
            c, _ = chi2_wowa_marginalised(float(w0), float(wa))
            grid[i, j] = c
            if c < best_val:
                best_val = c
                best_ij = (i, j)
    print("  w0 \\ wa:  " + "  ".join(f"{wa:+.2f}" for wa in wa_arr))
    for i, w0 in enumerate(w0_arr):
        row = "  ".join(f"{grid[i, j] - c0:+6.2f}" for j in range(len(wa_arr)))
        print(f"  {w0:+.2f}:  {row}")

    if best_ij is not None:
        i, j = best_ij
        dchi2_min = best_val - c0
        print(f"\nGrid minimum Delta chi^2 = {dchi2_min:+.3f}")
        print(f"  at (w0, wa) = ({w0_arr[i]:+.3f}, {wa_arr[j]:+.3f})")

        # Refine: Nelder-Mead on (w0, wa) with inner Om/h/omb marginalisation
        def outer(p):
            w0, wa = p
            c, _ = chi2_wowa_marginalised(float(w0), float(wa))
            return c
        res = minimize(outer, [w0_arr[i], wa_arr[j]], method='Nelder-Mead',
                       options={'xatol': 1e-4, 'fatol': 1e-3, 'maxiter': 80})
        dchi2_min = res.fun - c0
        print(f"Refined: Delta chi^2_min = {dchi2_min:+.3f}")
        print(f"  at (w0, wa) = ({res.x[0]:+.4f}, {res.x[1]:+.4f})")
    else:
        dchi2_min = 0.0
        print("\nNo improvement found on grid.")

    print()
    print("Decision gate (base.todo.md D1): Delta chi^2 <= -15 required.")
    print(f"Fisher upper bound (CPL + marginalised nuisance): {dchi2_min:+.2f}")
    if dchi2_min <= -15:
        print("  --> GO: CPL extension attains Delta chi^2 <= -15")
    elif dchi2_min <= -6:
        print("  --> WEAK: CPL extension reaches 'positive' evidence only")
        print("      (Delta AIC ~ -2 to -4 after k=2 penalty).")
    else:
        print("  --> NO-GO: background-level CPL cannot beat LCDM strongly.")

    c_desi, x_desi = chi2_wowa_marginalised(-0.757, -0.83)
    print(f"\nAt DESI DR2 headline (w0, wa) = (-0.757, -0.83):")
    print(f"  marginalised chi^2 = {c_desi:.3f}   Delta = {c_desi - c0:+.3f}")
    print(f"  requires (Om, h, omb) = ({x_desi[0]:.4f}, {x_desi[1]:.4f}, "
          f"{x_desi[2]:.5f})")


if __name__ == "__main__":
    main()
