# -*- coding: utf-8 -*-
"""
Phase L5-D: cosmic shear S_8 channel + K15 / Q10 / Q11 checks.

For each L5 candidate (LCDM, C28, C33, A01/A05/A12/A17 mainstream, and
alt-soft cluster A03/A04/A06/A08/A09/A11/A13/A15/A16/A19/A20) compute
  - S_8 via simulations.l5.common.s8_from_Efunc
  - chi2_WL = ((S_8 - 0.7656) / 0.0138)^2
  - chi2_joint (BAO+SN+CMB+RSD) with the same best-fit (Om, h)
  - K15 verdict (S_8 < 0.84)
  - Q10 verdict (delta chi2_WL vs LCDM <= +3)
  - Q11 verdict (|h - 0.732| not worsened by > 0.005 vs LCDM)

Mainstream and C28/C33 E(z) are built from the CPL (w0_fid, wa_fid)
template stored in simulations/l5/forecast/dr3_forecast.json together
with the per-candidate best-fit (Om, h) coming from the L4 result.json
files (C28, C33) or simulations/l4_alt/alt20_results.json (A01..A20).

Writes simulations/l5/shear/s8_k15_q10_q11.json.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')

np.seterr(all='ignore')

_HERE = os.path.dirname(os.path.abspath(__file__))
_L5 = os.path.dirname(_HERE)
_SIMS = os.path.dirname(_L5)
for _p in (_SIMS, _L5, os.path.join(_SIMS, 'l4'), os.path.join(_SIMS, 'l3')):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from l5.common import (  # noqa: E402
    s8_from_Efunc, chi2_shear, S8_WL_MEAN, S8_WL_SIGMA,
    LCDM_OM, LCDM_H, LCDM_CHI2, OMEGA_R, E_lcdm, jsonify,
)
from l3.data_loader import chi2_joint  # noqa: E402


H0_SHOES = 0.732  # SH0ES
Q11_TOL = 0.005
K15_MAX = 0.84
Q10_MAX = 3.0
_OMEGA_B = 0.02237


# ---------------------------------------------------------------------------
# Data sources
# ---------------------------------------------------------------------------

_FORECAST = os.path.join(_L5, 'forecast', 'dr3_forecast.json')
_ALT20 = os.path.join(_SIMS, 'l4_alt', 'alt20_results.json')
_L4_C28 = os.path.join(_SIMS, 'l4', 'C28', 'result.json')
_L4_C33 = os.path.join(_SIMS, 'l4', 'C33', 'result.json')

with open(_FORECAST, 'r', encoding='utf-8') as _f:
    _FC = json.load(_f)
with open(_ALT20, 'r', encoding='utf-8') as _f:
    _ALT = json.load(_f)
with open(_L4_C28, 'r', encoding='utf-8') as _f:
    _C28R = json.load(_f)
with open(_L4_C33, 'r', encoding='utf-8') as _f:
    _C33R = json.load(_f)

_CPL_BY_ID = {c['id']: c for c in _FC['candidates']}
_ALT_BY_ID = {r['id']: r for r in _ALT['results']}


def _cpl_E(Om, h, w0, wa):
    """CPL background E(z) at given (Om, h, w0, wa)."""
    OL0 = 1.0 - Om - OMEGA_R

    def E(z):
        z = np.asarray(z, dtype=float)
        f = (1.0 + z) ** (3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * z / (1.0 + z))
        E2 = OMEGA_R * (1 + z) ** 4 + Om * (1 + z) ** 3 + OL0 * f
        E2 = np.where(E2 > 0, E2, np.nan)
        return np.sqrt(E2)
    return E


def _alt_E(aid, Om, h):
    """Build zero-parameter alt-20 E(z) from runner.ALT."""
    from l4_alt.runner import ALT, _make_E  # noqa: E402
    f_ratio = ALT[aid][1]
    build = _make_E(f_ratio)
    return build([], Om, h)


# ---------------------------------------------------------------------------
# Per-candidate eval
# ---------------------------------------------------------------------------

def _chi2_bg(E, Om, h):
    """BAO+SN+CMB+RSD joint chi2 for given E."""
    omega_c = Om * h * h - _OMEGA_B
    res = chi2_joint(E, rd=147.09, Omega_m=Om,
                     omega_b=_OMEGA_B, omega_c=omega_c, h=h,
                     H0_km=100.0 * h)
    return float(res['total'])


def eval_candidate(cand_id, label, Om, h, E):
    S8 = s8_from_Efunc(E, Om, h)
    if S8 is None or not np.isfinite(S8):
        return None
    chi2_wl = float(((S8 - S8_WL_MEAN) / S8_WL_SIGMA) ** 2)
    chi2_bg = _chi2_bg(E, Om, h)
    return {
        'id': cand_id,
        'label': label,
        'Om': float(Om),
        'h': float(h),
        'S8': float(S8),
        'chi2_joint_bg': chi2_bg,
        'chi2_wl': chi2_wl,
        'chi2_joint_plus_wl': chi2_bg + chi2_wl,
        'h_minus_shoes_abs': float(abs(h - H0_SHOES)),
    }


def main():
    out = {
        'S8_WL_MEAN': S8_WL_MEAN,
        'S8_WL_SIGMA': S8_WL_SIGMA,
        'H0_SHOES': H0_SHOES,
        'gates': {
            'K15_S8_max': K15_MAX,
            'Q10_delta_chi2_wl_max': Q10_MAX,
            'Q11_h_tol': Q11_TOL,
        },
        'candidates': [],
    }

    # ---- LCDM reference ----
    E_lc = E_lcdm(LCDM_OM, LCDM_H)
    lcdm = eval_candidate('LCDM', 'LCDM', LCDM_OM, LCDM_H, E_lc)
    assert lcdm is not None
    lcdm_chi2_wl = lcdm['chi2_wl']
    lcdm_h_tension = lcdm['h_minus_shoes_abs']
    out['lcdm'] = lcdm

    print("=== Phase L5-D cosmic shear S_8 check ===")
    print(f"LCDM: S_8={lcdm['S8']:.4f}, chi2_WL={lcdm_chi2_wl:.2f},"
          f" chi2_joint={lcdm['chi2_joint_bg']:.2f}, |h-SH0ES|={lcdm_h_tension:.4f}")
    print()

    # ---- C28 and C33 (CPL template at L4 best-fit Om,h) ----
    mainstream_ids = [
        ('C28', 'Maggiore-Mancarella RR (CPL template)', _C28R),
        ('C33', 'f(Q) teleparallel (CPL template)', _C33R),
    ]
    entries = []
    for cid, label, r in mainstream_ids:
        Om = float(r['Om'])
        h = float(r['h'])
        cpl = _CPL_BY_ID[cid]
        E = _cpl_E(Om, h, cpl['w0_fid'], cpl['wa_fid'])
        entry = eval_candidate(cid, label, Om, h, E)
        entries.append(entry)

    # ---- Mainstream alt (A01, A05, A12, A17) and alt-soft cluster ----
    alt_mainstream = ['A01', 'A05', 'A12', 'A17']
    alt_soft = ['A03', 'A04', 'A06', 'A08', 'A09', 'A11', 'A13', 'A15', 'A16', 'A19', 'A20']
    for aid in alt_mainstream + alt_soft:
        r = _ALT_BY_ID[aid]
        Om = float(r['Om']); h = float(r['h'])
        E = _alt_E(aid, Om, h)
        label = f"{aid} [{r['name']}]"
        entry = eval_candidate(aid, label, Om, h, E)
        if entry is None:
            entry = {'id': aid, 'label': label, 'error': 'S8 computation failed'}
        entries.append(entry)

    # ---- Apply gates, compute deltas vs LCDM ----
    lcdm_bg = lcdm['chi2_joint_bg']
    for e in entries:
        if 'error' in e:
            out['candidates'].append(e)
            continue
        delta_wl = e['chi2_wl'] - lcdm_chi2_wl
        delta_bg = e['chi2_joint_bg'] - lcdm_bg
        net_with_shear = delta_bg + delta_wl
        k15_pass = bool(e['S8'] < K15_MAX)
        # Q10: the shear channel adds at most +3 vs LCDM's shear penalty.
        # Since LCDM already has chi2_WL ~ 27.6, we interpret as:
        # (delta_wl) <= +3 -> the new channel did not catastrophically
        # worsen the growth sector relative to LCDM.
        q10_pass = bool(delta_wl <= Q10_MAX)
        q11_pass = bool(e['h_minus_shoes_abs'] <= lcdm_h_tension + Q11_TOL)
        e.update({
            'delta_chi2_wl_vs_lcdm': float(delta_wl),
            'delta_chi2_joint_vs_lcdm': float(delta_bg),
            'net_delta_chi2_with_shear': float(net_with_shear),
            'K15_pass': k15_pass,
            'Q10_pass': q10_pass,
            'Q11_pass': q11_pass,
        })
        out['candidates'].append(e)

    out_path = os.path.join(_HERE, 's8_k15_q10_q11.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(jsonify(out), f, indent=2)
    print(f"wrote {out_path}")

    # Console summary
    hdr = ("{:<6} {:>7} {:>7} {:>8} {:>8} {:>10} {:>10} {:>5} {:>5} {:>5}"
           .format("ID", "Om", "h", "S_8", "chi2_WL", "d_chi2_WL",
                   "d_chi2_bg", "K15", "Q10", "Q11"))
    print()
    print(hdr)
    print("-" * len(hdr))
    # print LCDM first
    print("{:<6} {:>7.4f} {:>7.4f} {:>8.4f} {:>8.2f} {:>10} {:>10} {:>5} {:>5} {:>5}"
          .format("LCDM", lcdm['Om'], lcdm['h'], lcdm['S8'],
                  lcdm_chi2_wl, "  0.00", "  0.00",
                  "PASS" if lcdm['S8'] < K15_MAX else "FAIL",
                  "PASS", "PASS"))
    for e in out['candidates']:
        if 'error' in e:
            print(f"{e['id']:<6} ERROR: {e['error']}")
            continue
        print("{:<6} {:>7.4f} {:>7.4f} {:>8.4f} {:>8.2f} {:>10.3f} {:>10.3f} {:>5} {:>5} {:>5}"
              .format(e['id'], e['Om'], e['h'], e['S8'], e['chi2_wl'],
                      e['delta_chi2_wl_vs_lcdm'],
                      e['delta_chi2_joint_vs_lcdm'],
                      "PASS" if e['K15_pass'] else "FAIL",
                      "PASS" if e['Q10_pass'] else "FAIL",
                      "PASS" if e['Q11_pass'] else "FAIL"))

    # K15/Q10/Q11 aggregate
    any_fail_k15 = [e['id'] for e in out['candidates']
                    if 'error' not in e and not e['K15_pass']]
    any_fail_q10 = [e['id'] for e in out['candidates']
                    if 'error' not in e and not e['Q10_pass']]
    any_fail_q11 = [e['id'] for e in out['candidates']
                    if 'error' not in e and not e['Q11_pass']]
    print()
    print(f"K15 fails (S_8 >= {K15_MAX}): {any_fail_k15}")
    print(f"Q10 fails (d_chi2_WL > +{Q10_MAX}): {any_fail_q10}")
    print(f"Q11 fails (|h-SH0ES| worse by > {Q11_TOL}): {any_fail_q11}")


if __name__ == '__main__':
    main()
