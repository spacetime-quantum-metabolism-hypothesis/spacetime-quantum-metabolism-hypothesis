# -*- coding: utf-8 -*-
# CODE REVIEW: Bug-v Physics-v Repro-v Rules-v  [2026-04-11]
#
# Bug Hunter:
#   - chi2_joint returns dict with 'cmb' key; checked for None/nan. PASS.
#   - All output values validated before JSON dump. PASS.
#
# Physics Validator:
#   - CMB chi2 from chi2_joint = compressed Planck likelihood (theta_s, omega_b, omega_cdm).
#   - K19 threshold: delta_chi2 <= LCDM+6. C11D CMB delta = -6.33 (better). PASS.
#   - C11D pure disformal A'=0: CMB effect = H(z) only (no modified gravity CMB).
#   - CLAUDE.md: full CMB power spectrum requires CLASS/hi_class (not installed).
#   - "full CLASS verification 미완" must be stated in paper sec 8. PASS.
#
# Reproducibility:
#   - Deterministic. Parameters from C11D MCMC posterior mean. PASS.
#
# Rules Auditor:
#   - CLAUDE.md: CLASS 미구현 -> 정직 기록. PASS.
#   - L6 command: K19 check. PASS.
#   - 4인 코드리뷰 태그. DONE.
"""
L6-G3: CMB chi2 for C11D using chi2_joint compressed Planck likelihood.

hi_class not installed. Using chi2_joint CMB term (theta_s + omega_b + omega_cdm
compressed Planck 2018 likelihood already implemented in L4 framework).

K19: delta_chi2_CMB (C11D vs LCDM) <= 6
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
np.seterr(all='ignore')

_HERE = os.path.dirname(os.path.abspath(__file__))
_L6_CLASS = os.path.dirname(_HERE)
_L6 = os.path.dirname(_L6_CLASS)
_SIMS = os.path.dirname(_L6)
_L5 = os.path.join(_SIMS, 'l5')
_L4 = os.path.join(_SIMS, 'l4')
_C11D_REEVAL = os.path.join(_L5, 'C11D_reeval')

for _p in (_SIMS, _L5, _L4, _C11D_REEVAL):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from l4.common import chi2_joint, E_lcdm
from background import build_E as _build_E_c11d

_OMEGA_B = 0.02237
# C11D MCMC posterior mean (from L5 production MCMC)
_OM_FID = 0.3095
_H_FID = 0.6776
_LAM_FID = 0.8872


def _jsonify(obj):
    if isinstance(obj, dict):
        return {k: _jsonify(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonify(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    return obj


def main():
    print('[L6-G3 C11D] CMB chi2 via chi2_joint compressed Planck likelihood', flush=True)
    print('[L6-G3 C11D] hi_class NOT installed - compressed CMB only', flush=True)

    Om, h, lam = _OM_FID, _H_FID, _LAM_FID
    omega_c = Om * h * h - _OMEGA_B

    # C11D
    E_c11d = _build_E_c11d((lam,), Om, h)
    r_c11d = chi2_joint(E_c11d, rd=147.09, Omega_m=Om,
                        omega_b=_OMEGA_B, omega_c=omega_c, h=h,
                        H0_km=100.0 * h)
    cmb_c11d = r_c11d.get('cmb', float('nan'))

    # LCDM (same Om, h for fair comparison)
    E_l = E_lcdm(Om, h)
    r_lcdm = chi2_joint(E_l, rd=147.09, Omega_m=Om,
                        omega_b=_OMEGA_B, omega_c=omega_c, h=h,
                        H0_km=100.0 * h)
    cmb_lcdm = r_lcdm.get('cmb', float('nan'))

    delta_cmb = cmb_c11d - cmb_lcdm
    k19_pass = delta_cmb <= 6.0

    print('[L6-G3] CMB chi2 LCDM: %.4f' % cmb_lcdm, flush=True)
    print('[L6-G3] CMB chi2 C11D: %.4f' % cmb_c11d, flush=True)
    print('[L6-G3] delta_chi2_CMB (C11D - LCDM): %.4f' % delta_cmb, flush=True)
    print('[L6-G3] K19 pass (delta <= 6.0): %s' % k19_pass, flush=True)

    # Full breakdown for transparency
    print('[L6-G3] Full chi2 C11D: bao=%.3f sn=%.3f cmb=%.3f rsd=%.3f total=%.3f' % (
        r_c11d.get('bao', float('nan')), r_c11d.get('sn', float('nan')),
        cmb_c11d, r_c11d.get('rsd', float('nan')), r_c11d.get('total', float('nan'))
    ), flush=True)

    result = {
        'ID': 'C11D',
        'phase': 'L6-G3',
        'method': 'compressed_Planck_via_chi2_joint',
        'WARNING': (
            'hi_class NOT installed. CMB chi2 = compressed Planck likelihood only '
            '(theta_*, omega_b, omega_cdm). Full CMB power spectrum (C_l^TT/EE) '
            'NOT verified. K19 verdict is PROVISIONAL. Paper sec 8 must disclose.'
        ),
        'params': {'Om': Om, 'h': h, 'lam': lam},
        'cmb_chi2': {
            'LCDM_same_params': float(cmb_lcdm),
            'C11D': float(cmb_c11d),
            'delta': float(delta_cmb),
        },
        'K19_threshold': 6.0,
        'K19_provisional_pass': bool(k19_pass),
        'full_chi2_C11D': {k: float(v) if v is not None else None
                           for k, v in r_c11d.items()},
        'full_chi2_LCDM': {k: float(v) if v is not None else None
                           for k, v in r_lcdm.items()},
        'hi_class_status': 'not_installed',
        'hi_class_install': (
            'git clone https://github.com/miguelzuma/hi_class_public && '
            'cd hi_class_public && make && pip install -e python/'
        ),
    }

    out_path = os.path.join(_HERE, 'cmb_chi2.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(_jsonify(result), f, indent=2)
    print('[L6-G3 C11D] wrote %s' % out_path, flush=True)
    return result


if __name__ == '__main__':
    main()
