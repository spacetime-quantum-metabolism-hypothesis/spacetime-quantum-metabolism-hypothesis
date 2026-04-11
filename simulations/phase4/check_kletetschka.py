# -*- coding: utf-8 -*-
"""
Cross-check of Kletetschka 2025 "3D Time" w(z) prediction against the
Phase 3 joint dataset (BAO + SN + compressed CMB + RSD), N = 1853.

Paper equation (Sec 3.4):
    w(z) = -1 + (0.05 +/- 0.01) (1 + z)^3
    Omega_DE = 0.685 +/- 0.007

This is NOT a CPL form. We feed it into the same expansion-history chi^2
machinery used by fisher_kessence.py (inner Nelder-Mead marginalisation over
Om, h, omb with BBN prior).

Two sanity checks first:
  (a) evaluate w(z) at z = 0, 0.5, 1, 2, 3, 1100 to see high-z divergence
  (b) integrate rho_DE(a)/rho_DE0 = exp( 3 int_a^1 (1+w(a'))/a' da' )
"""
import os, sys
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..')))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', 'phase2')))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', 'phase3')))

import config
import desi_fitting as df
import compressed_cmb as ccmb
from mcmc_phase3 import (rsd_chi2_lcdm, _EWrap, _fast_sn_chi2,
                         _bridge_highz, r_d_EH98, SN)

# --- Kletetschka parameters ---
EPS = 0.05  # dark energy evolution amplitude
OM_DE = 0.685

def w_kletetschka(z):
    return -1.0 + EPS * (1.0 + z) ** 3

def f_de_kletetschka(a):
    """rho_DE(a) / rho_DE(a=1).

    d ln rho_DE / d ln a = -3 (1 + w(a))
    rho_DE(a)/rho_DE0 = exp( 3 int_a^1 (1 + w(a'))/a' da' )
    with w(a') = -1 + eps (1/a')^3
    => 1 + w = eps / a'^3
    => integrand = eps / a'^4
    => int_a^1 eps / a'^4 da' = eps/3 * (1/a^3 - 1)
    => rho_DE(a)/rho_DE0 = exp( eps (1/a^3 - 1) )
    """
    return np.exp(EPS * (a ** (-3) - 1.0))

def E_kletetschka(Om, h):
    Or = config.Omega_r
    OL = 1.0 - Om - Or
    def E(z):
        a = 1.0 / (1.0 + z)
        return float(np.sqrt(Or * (1 + z) ** 4
                             + Om * (1 + z) ** 3
                             + OL * f_de_kletetschka(a)))
    return E

def chi2_total(Om, h, omb):
    if not (0.20 < Om < 0.45): return 1e8
    if not (0.55 < h < 0.80): return 1e8
    if not (0.020 < omb < 0.025): return 1e8
    omc = Om * h * h - omb
    if not (0.05 < omc < 0.20): return 1e8
    rd = r_d_EH98(omb, omc, h)
    try:
        E = E_kletetschka(Om, h)
        c_bao = df.chi2(_EWrap(E), rd)
        c_sn = _fast_sn_chi2(SN, E, H0_km=100.0 * h)
        c_cmb = ccmb.chi2_compressed_cmb(omb, omc, h, _bridge_highz(E, Om=Om))
        c_rsd = rsd_chi2_lcdm(Om, 0.8095)
    except Exception as e:
        return 1e8
    return c_bao + c_sn + c_cmb + c_rsd + ((omb - 0.02237) / 0.00015) ** 2

def main():
    print("=" * 68)
    print("Kletetschka 3D-Time w(z) = -1 + 0.05 (1+z)^3 check")
    print("=" * 68)

    print("\n(a) w(z) sanity:")
    for z in (0, 0.1, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0, 100.0, 1100.0):
        wz = w_kletetschka(z)
        print(f"  z = {z:<8.2f}  w = {wz:+.4e}")

    print("\n(b) rho_DE(a)/rho_DE0 (should diverge at a -> 0):")
    for a in (1.0, 0.9, 0.5, 0.25, 0.1, 0.05, 0.01):
        f = f_de_kletetschka(a)
        print(f"  a = {a:<6.3f}  z = {1/a-1:<8.2f}  rho_DE/rho_DE0 = {f:.4e}")

    print("\n(c) joint chi^2, (Om, h, omb) marginalised")
    res = minimize(lambda x: chi2_total(*x),
                   [0.3152, 0.6715, 0.02237],
                   method='Nelder-Mead',
                   options={'xatol': 1e-5, 'fatol': 1e-3, 'maxiter': 600})
    print(f"  best chi^2 = {res.fun:.3f}")
    print(f"  (Om, h, omb) = ({res.x[0]:.4f}, {res.x[1]:.4f}, {res.x[2]:.5f})")

    # Compare against Phase 3 LCDM r_d-fixed baseline (1683.11)
    # and r_d-free baseline (1666.78).
    print(f"\n  Phase 3 LCDM r_d fixed:  1683.11  ->  dchi^2 = {res.fun - 1683.11:+.2f}")
    print(f"  Phase 3 LCDM r_d free:   1666.78  ->  dchi^2 = {res.fun - 1666.78:+.2f}")

    # Try also eps = 0.04 and 0.06 (1-sigma band)
    global EPS
    for eps_try in (0.04, 0.05, 0.06):
        EPS = eps_try
        r2 = minimize(lambda x: chi2_total(*x),
                      [0.3152, 0.6715, 0.02237],
                      method='Nelder-Mead',
                      options={'xatol': 1e-5, 'fatol': 1e-3, 'maxiter': 600})
        print(f"  eps = {eps_try:.2f}  chi^2 = {r2.fun:.2f}  "
              f"dchi^2 = {r2.fun - 1683.11:+.2f} (vs LCDM rd-fixed)")

if __name__ == "__main__":
    main()
