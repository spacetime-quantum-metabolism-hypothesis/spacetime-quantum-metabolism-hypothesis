# -*- coding: utf-8 -*-
"""L5 Phase E C11D fast re-judgement.

Strategy: the core scientific question is whether the K3 phantom-crossing
hit in L4 survives once the *exact* pure-disformal background (minimally-
coupled quintessence ODE, A'=0) replaces the leading-order CPL thawing
template. The precise (Om, h, lam) best fit is secondary.

Fast path:
  1. For a coarse grid over lam in [0, 1.6], do a single Nelder-Mead over
     (Om, h) (no multistart), starting from the LCDM baseline.
  2. Track chi2(lam), pick best.
  3. At the best (Om, h, lam) construct E(z) on a dense grid, read w(z)
     directly from the scalar field ODE (no CPL parametrisation), and
     apply the |w+1|>1e-3 phantom guard.
"""
from __future__ import annotations

import json
import os
import sys
import time

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')

import numpy as np
from scipy.optimize import minimize

_HERE = os.path.dirname(os.path.abspath(__file__))
_L5 = os.path.dirname(_HERE)
_SIMS = os.path.dirname(_L5)
_L4 = os.path.join(_SIMS, 'l4')
for _p in (_SIMS, _L4, _HERE, _L5):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from common import (  # noqa: E402
    LCDM_CHI2, LCDM_OM, LCDM_H, cpl_fit, phantom_crossing, jsonify,
    chi2_joint,
)
from background import build_E, w_of_z  # noqa: E402


def _chi2_at(lam, Om, h):
    E = build_E([lam], Om, h)
    if E is None:
        return 1e8
    omega_b = 0.02237
    omega_c = Om * h * h - omega_b
    if omega_c <= 0:
        return 1e8
    try:
        res = chi2_joint(E, rd=147.09, Omega_m=Om,
                         omega_b=omega_b, omega_c=omega_c, h=h,
                         H0_km=100.0 * h)
        tot = res['total']
        if not np.isfinite(tot):
            return 1e8
        return float(tot)
    except Exception:
        return 1e8


def _fit_Om_h(lam, x0):
    """Single NM over (Om, h) at fixed lam, tight box."""
    def cost(x):
        Om, h = float(x[0]), float(x[1])
        if not (0.28 <= Om <= 0.36 and 0.64 <= h <= 0.71):
            return 1e8 + 1e4 * (max(0, 0.28 - Om) ** 2 + max(0, Om - 0.36) ** 2
                                + max(0, 0.64 - h) ** 2 + max(0, h - 0.71) ** 2)
        return _chi2_at(lam, Om, h)

    r = minimize(cost, x0, method='Nelder-Mead',
                 options={'xatol': 1e-4, 'fatol': 1e-3,
                          'maxiter': 200, 'adaptive': True})
    return float(r.x[0]), float(r.x[1]), float(r.fun)


def main():
    t0 = time.time()
    print("=== L5 Phase E : C11D fast re-judgement ===", flush=True)

    lam_grid = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
    x_cur = (LCDM_OM, LCDM_H)
    rows = []
    best = None
    for lam in lam_grid:
        ts = time.time()
        Om, h, chi2 = _fit_Om_h(lam, x_cur)
        print(f"  lam={lam:.2f}  Om={Om:.4f}  h={h:.4f}  chi2={chi2:.3f}  "
              f"({time.time()-ts:.1f}s)", flush=True)
        rows.append({'lam': lam, 'Om': Om, 'h': h, 'chi2': chi2})
        x_cur = (Om, h)
        if best is None or chi2 < best['chi2']:
            best = {'lam': lam, 'Om': Om, 'h': h, 'chi2': chi2}

    # Refine around best lam with 3 sub-points
    print("  refining...", flush=True)
    lo_lam = max(0.0, best['lam'] - 0.1)
    hi_lam = best['lam'] + 0.1
    for lam in np.linspace(lo_lam, hi_lam, 5):
        if abs(lam - best['lam']) < 1e-6:
            continue
        ts = time.time()
        Om, h, chi2 = _fit_Om_h(float(lam), (best['Om'], best['h']))
        print(f"  lam={lam:.3f}  chi2={chi2:.3f}  ({time.time()-ts:.1f}s)", flush=True)
        if chi2 < best['chi2']:
            best = {'lam': float(lam), 'Om': Om, 'h': h, 'chi2': chi2}

    lam_b = best['lam']; Om_b = best['Om']; h_b = best['h']
    chi2_b = best['chi2']
    dchi2 = chi2_b - LCDM_CHI2
    print(f"\n  BEST: lam={lam_b:.4f}  Om={Om_b:.4f}  h={h_b:.4f}  "
          f"chi2={chi2_b:.3f}  d={dchi2:+.3f}", flush=True)

    # Rebuild for reporting
    E = build_E([lam_b], Om_b, h_b)
    omega_b = 0.02237
    omega_c = Om_b * h_b * h_b - omega_b
    res = chi2_joint(E, rd=147.09, Omega_m=Om_b,
                     omega_b=omega_b, omega_c=omega_c, h=h_b,
                     H0_km=100.0 * h_b)

    # Direct w(z) from scalar field
    z_dense = np.linspace(0.001, 3.0, 500)
    _, w_arr = w_of_z([lam_b], Om_b, z_grid=z_dense)
    w_today = float(w_arr[0])
    w_min = float(np.min(w_arr))
    w_max = float(np.max(w_arr))

    above = np.where(w_arr + 1.0 > 1e-3)[0]
    below = np.where(w_arr + 1.0 < -1e-3)[0]
    pc_direct = bool(len(above) > 0 and len(below) > 0)

    pc_common = phantom_crossing(E, Om_b, z_max=2.5, n=400)

    w0_cpl, wa_cpl = cpl_fit(E, Om_b)

    print(f"  w(z=0)={w_today:+.5f}  w_min={w_min:+.5f}  w_max={w_max:+.5f}",
          flush=True)
    print(f"  phantom_cross direct: {pc_direct}   common: {pc_common}",
          flush=True)
    print(f"  CPL projection: w0={w0_cpl:+.4f}  wa={wa_cpl:+.4f}",
          flush=True)

    if (not pc_direct) and (not pc_common):
        verdict = "PROMOTE"
        rationale = (
            "Pure-disformal (A'=0) branch integrated via CLW 1998 "
            "quintessence ODE has w(z) >= -1 at all z (exactly, by the "
            "positivity of the kinetic term in minimally coupled "
            "quintessence). K3 phantom crossing CLEARED. The L4 K3 hit was "
            "a leading-order CPL thawing-template artifact exactly as "
            "suspected. delta_chi2 vs LCDM = {dc:+.3f}, w_today = "
            "{w0:+.4f}, w_a(CPL) = {wa:+.4f}."
        ).format(dc=dchi2, w0=w_today, wa=wa_cpl)
    else:
        verdict = "KILL"
        rationale = (
            "Even with the exact quintessence ODE the model phantom-"
            "crosses under the |w+1|>1e-3 guard. K3 confirmed."
        )

    print(f"\nVERDICT: {verdict}", flush=True)
    print(f"Rationale: {rationale}", flush=True)

    out = {
        'ID': 'C11D_reeval',
        'phase': 'L5-E',
        'background_method':
            'Copeland-Liddle-Wands 1998 quintessence autonomous system, '
            'exponential V(phi), A_prime=0 pure disformal limit',
        'scan_rows': rows,
        'best_fit': {
            'Om': Om_b, 'h': h_b, 'lam': lam_b,
            'chi2_bao': float(res['bao']),
            'chi2_sn': float(res['sn']),
            'chi2_cmb': float(res['cmb']),
            'chi2_rsd': float(res['rsd']),
            'chi2_total': float(res['total']),
        },
        'lcdm_chi2': float(LCDM_CHI2),
        'delta_chi2_vs_lcdm': float(dchi2),
        'w_direct': {
            'w_today': w_today, 'w_min': w_min, 'w_max': w_max,
        },
        'cpl_projection': {'w0': float(w0_cpl), 'wa': float(wa_cpl)},
        'phantom_crossing': bool(pc_direct or pc_common),
        'phantom_guard': '|w+1|>1e-3 both sides',
        'verdict': verdict,
        'rationale': rationale,
        'runtime_sec': float(time.time() - t0),
    }
    out_path = os.path.join(_HERE, 'result.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(jsonify(out), f, indent=2, ensure_ascii=False)
    print(f"wrote {out_path}  (total {out['runtime_sec']:.1f}s)", flush=True)
    return out


if __name__ == '__main__':
    main()
