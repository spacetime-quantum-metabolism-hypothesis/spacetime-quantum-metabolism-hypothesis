# -*- coding: utf-8 -*-
"""
L3 LCDM baseline — one-shot optimiser.

Minimises BAO+SN+CMB+RSD joint chi^2 over (Omega_m, h). r_d fixed to 147.09
Mpc (DESI fiducial, CamB-sound-horizon). omega_b, omega_c derived from
Omega_m and h, with omega_b/Omega_m ratio locked to Planck 2018 fiducial
(omega_b = 0.02237, so omega_c = Omega_m*h^2 - omega_b). No free params.

Output: simulations/l3/lcdm_baseline.json with:
    {Omega_m, h, rd, chi2_bao, chi2_sn, chi2_cmb, chi2_rsd, chi2_total}

This is the Δχ² reference point for K1.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
from scipy.optimize import minimize

_THIS = os.path.dirname(os.path.abspath(__file__))
if _THIS not in sys.path:
    sys.path.insert(0, _THIS)

from data_loader import chi2_joint, get_data  # noqa: E402

sys.path.insert(0, os.path.dirname(_THIS))  # access simulations.config
import config  # noqa: E402


def _E_lcdm(Om, h):
    Or = config.Omega_r
    OL = 1.0 - Om - Or

    def E(z):
        return np.sqrt(Or * (1 + z)**4 + Om * (1 + z)**3 + OL)

    return E


def total_chi2(params):
    Om, h = params
    if not (0.15 < Om < 0.5) or not (0.5 < h < 0.9):
        return 1e8
    omega_b = 0.02237
    omega_c = Om * h * h - omega_b
    if omega_c <= 0:
        return 1e8
    E = _E_lcdm(Om, h)
    res = chi2_joint(E, rd=147.09, Omega_m=Om,
                     omega_b=omega_b, omega_c=omega_c, h=h,
                     H0_km=100.0 * h)
    return res['total']


def main():
    _ = get_data()  # preload
    # Multi-start for safety.
    starts = [(0.30, 0.67), (0.315, 0.6736), (0.33, 0.68), (0.29, 0.66),
              (0.325, 0.685), (0.305, 0.672), (0.34, 0.69), (0.298, 0.665)]
    best = None
    for s in starts:
        try:
            r = minimize(total_chi2, s, method='Nelder-Mead',
                         options={'xatol': 1e-5, 'fatol': 1e-4,
                                  'maxiter': 400})
            if r.success or r.fun < 1e7:
                if best is None or r.fun < best.fun:
                    best = r
        except Exception as e:
            print(f"  start {s} failed: {e}")
    if best is None:
        raise RuntimeError("LCDM multi-start all failed")

    Om, h = best.x
    omega_b = 0.02237
    omega_c = Om * h * h - omega_b
    E = _E_lcdm(Om, h)
    res = chi2_joint(E, rd=147.09, Omega_m=Om,
                     omega_b=omega_b, omega_c=omega_c, h=h,
                     H0_km=100.0 * h)

    out = {
        'model': 'LCDM',
        'Omega_m': float(Om),
        'h': float(h),
        'rd_Mpc': 147.09,
        'omega_b': omega_b,
        'omega_c': float(omega_c),
        'chi2_bao': res['bao'],
        'chi2_sn': res['sn'],
        'chi2_cmb': res['cmb'],
        'chi2_rsd': res['rsd'],
        'chi2_total': res['total'],
        'notes': 'rd=147.09 fixed. omega_b fixed to Planck fid; '
                 'omega_c derived. BAO+SN+CMB+RSD joint minimisation.',
    }
    out_path = os.path.join(_THIS, 'lcdm_baseline.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)

    print("LCDM baseline (L3 reference)")
    print("=" * 60)
    for k, v in out.items():
        print(f"  {k:12s} = {v}")
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
