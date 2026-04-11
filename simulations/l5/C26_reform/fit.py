# -*- coding: utf-8 -*-
"""Fit C26_reform (J^0 = alpha_Q H rho_m) against BAO+SN+CMB+RSD.
Check K10 (toy<->full w_a sign consistency) and L3 drift-toy agreement."""
from __future__ import annotations

import json
import os
import sys

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_L5 = os.path.dirname(_HERE)
_SIMS = os.path.dirname(_L5)
_L4 = os.path.join(_SIMS, 'l4')
for _p in (_SIMS, _L4, _HERE, _L5):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from common import (  # noqa: E402  (l5/common.py)
    LCDM_CHI2, tight_fit, cpl_fit, phantom_crossing, jsonify, OMEGA_R,
)
from background import build_E  # noqa: E402


def main():
    print("=== L5 Phase E : C26 re-formulation (J^0 = alpha_Q H rho_m) ===")

    fit = tight_fit(build_E, theta_bounds=[(0.0, 0.4)], theta0=[0.05])
    if fit is None:
        print("FIT FAILED")
        return None
    Om = fit['Om']; h = fit['h']; aq = fit['theta'][0]
    E = fit['E']
    chi2 = fit['chi2_total']
    dchi2 = chi2 - LCDM_CHI2

    w0_cpl, wa_cpl = cpl_fit(E, Om)
    pc = phantom_crossing(E, Om, z_max=2.0, n=300)

    # L3 drift-toy reference: rho_m_toy = Om a^-3 (1 - aq*(1 - a^3))
    # Leading expansion of exp(-(3+aq) N) in aq:
    #   Om a^-3 * (1 - aq*N) = Om a^-3 * (1 + aq ln(1/a))
    # Different functional form, but same-sign drift (rho_m larger in past
    # for aq>0).  Compute its w_a via the same cpl_fit path for comparison.
    def build_E_L3toy(theta, Om_local, h_local):
        aq2 = float(theta[0])
        if aq2 < 0 or aq2 > 0.4:
            return None
        OL0 = 1.0 - Om_local - OMEGA_R

        def Ef(z):
            zv = np.asarray(z, dtype=float)
            a = 1.0 / (1.0 + zv)
            rho_m = Om_local * a ** (-3) * (1.0 - aq2 * (1.0 - a ** 3))
            rho_m = np.where(rho_m < 1e-12, 1e-12, rho_m)
            rho_L = OL0 + aq2 * Om_local * (1.0 - a ** 3)
            Or = OMEGA_R * (1.0 + zv) ** 4
            E2 = Or + rho_m + rho_L
            E2 = np.where(E2 < 1e-12, 1e-12, E2)
            out = np.sqrt(E2)
            return float(out) if out.ndim == 0 else out
        return Ef

    # Evaluate toy at (Om, h, aq) best-fit
    E_toy = build_E_L3toy([aq], Om, h)
    w0_toy, wa_toy = cpl_fit(E_toy, Om)

    # K10: w_a sign consistency
    sign_full = np.sign(wa_cpl)
    sign_toy = np.sign(wa_toy)
    k10_ok = bool(sign_full == sign_toy and sign_full != 0)

    print(f"  best fit:  Om={Om:.4f}  h={h:.4f}  alpha_Q={aq:.4f}")
    print(f"  chi2_bao={fit['chi2_bao']:.3f}  sn={fit['chi2_sn']:.3f}  "
          f"cmb={fit['chi2_cmb']:.3f}  rsd={fit['chi2_rsd']:.3f}")
    print(f"  chi2_total={chi2:.3f}   delta_vs_LCDM={dchi2:+.3f}")
    print(f"  full model CPL:  w0={w0_cpl:+.4f}  wa={wa_cpl:+.4f}")
    print(f"  L3 drift toy:    w0={w0_toy:+.4f}  wa={wa_toy:+.4f}")
    print(f"  phantom_cross: {pc}")
    print(f"  K10 sign-consistent (full vs L3 toy): {k10_ok}")

    if k10_ok and dchi2 < -2.0:
        verdict = "PROMOTE"
        rationale = (
            f"Reformulated ansatz gives delta_chi2 = {dchi2:+.3f} with "
            f"alpha_Q = {aq:.4f}; w_a = {wa_cpl:+.4f} agrees in sign with "
            f"L3 drift toy w_a = {wa_toy:+.4f}.  K10 CLEARED -- the "
            f"toy<->full disagreement seen in L4 was due to the wrong "
            f"J^0 = alpha_Q rho_c0 (H/H0) ansatz."
        )
    else:
        reasons = []
        if not k10_ok:
            reasons.append("K10 sign mismatch")
        if dchi2 >= -2.0:
            reasons.append(f"weak fit (dchi2={dchi2:+.3f})")
        verdict = "KILL"
        rationale = "; ".join(reasons) if reasons else "unexplained"

    print(f"\nVERDICT: {verdict}")
    print(f"Rationale: {rationale}")

    out = {
        'ID': 'C26_reform',
        'phase': 'L5-E',
        'ansatz': 'J^0 = alpha_Q * H * rho_m  (closed-form)',
        'best_fit': {
            'Om': float(Om), 'h': float(h), 'alpha_Q': float(aq),
            'chi2_bao': float(fit['chi2_bao']),
            'chi2_sn': float(fit['chi2_sn']),
            'chi2_cmb': float(fit['chi2_cmb']),
            'chi2_rsd': float(fit['chi2_rsd']),
            'chi2_total': float(chi2),
        },
        'lcdm_chi2': float(LCDM_CHI2),
        'delta_chi2_vs_lcdm': float(dchi2),
        'cpl_full': {'w0': float(w0_cpl), 'wa': float(wa_cpl)},
        'cpl_L3_toy': {'w0': float(w0_toy), 'wa': float(wa_toy)},
        'phantom_crossing': bool(pc),
        'k10_consistent': bool(k10_ok),
        'verdict': verdict,
        'rationale': rationale,
    }
    out_path = os.path.join(_HERE, 'result.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(jsonify(out), f, indent=2, ensure_ascii=False)
    print(f"wrote {out_path}")
    return out


if __name__ == '__main__':
    main()
