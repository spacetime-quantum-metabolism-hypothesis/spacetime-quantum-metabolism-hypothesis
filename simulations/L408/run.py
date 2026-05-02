# -*- coding: utf-8 -*-
"""
L408 run.py -- V(n,t)-extension derivation gate test (DESI Tier B)
==================================================================
Purpose:
  Test whether two motivated V(n,t) functional forms (slow-roll analogue
  and thawing-quintessence template match) reach the DESI DR2 (w0, wa)
  1-sigma box AND beat LCDM AICc with HONEST k=4 (Om, H0, plus 2 V(n,t)
  shape parameters). If neither passes, Tier B pre-registration must be
  permanently shelved (G2 + G3 fail).

Conventions (CLAUDE.md L33 재발방지 strict):
  - N_GRID = 4000
  - cumulative_trapezoid for D_M
  - z_grid up to z_eff.max()+0.01
  - DESI DR2 13-point + full COV_INV
  - rho_DE = OL0 * (1 + amp * h(z; params))
  - ratio = clip(psi0/psi_z, 1.0, 200.0) when used
  - Om search [0.05, 0.50], H0 [50, 100]
  - HONEST AICc with k=4 (no template hidden DOF)

Two V(n,t) candidate families (PRE-DECLARED, not picked from L33 scan):
  C1 "slow-roll analogue":   h(z) = (1 - exp(-(z/zc)^p)) * tanh((1+z)^q - 1)
       params: (zc, p) free; q fixed at 0.5 by analogue convention
       motivation: V(n,t)~V0[1 - exp(-N(t)^p)] slow-roll attractor
  C2 "thawing CPL match":    h(z) = (1 - cos(pi*x/(1+x)))/2 with x = z*alpha
       params: (alpha) free; matches V(phi)=m^2 phi^2 thawing in low-z transient
       motivation: thawing quintessence frozen-at-high-z onset

DESI DR2 (DESI+CMB+SN-all) 1-sigma box (target):
  w0 in [-0.815, -0.699],  wa in [-1.04, -0.59]
"""

import os, sys, math, json, time, warnings
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import minimize, differential_evolution

warnings.filterwarnings('ignore')
np.seterr(all='ignore')
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM  = os.path.dirname(_HERE)
if _SIM not in sys.path:
    sys.path.insert(0, _SIM)
from desi_data import DESI_DR2, DESI_DR2_COV_INV

C_KMS  = 299792.458
R_S    = 147.09
OR     = 5.38e-5
N_DATA = 13
N_GRID = 4000

# DESI DR2 (DESI+CMB+SN-all) 1-sigma box, arXiv:2503.14738
W0_BOX = (-0.815, -0.699)
WA_BOX = (-1.04, -0.59)

# LCDM baseline (k=2: Om, H0) — recomputed below for self-consistency.

def aicc(chi2, k, n=N_DATA):
    return chi2 + 2*k + 2*k*(k+1)/(n - k - 1)

# ------------------------------------------------------------------ helpers

def E_lcdm(z, Om):
    return np.sqrt(OR*(1+z)**4 + Om*(1+z)**3 + (1.0-Om-OR))

def compute_tv_from_E(Om, H0, E_arr, z_grid):
    z_eff = DESI_DR2['z_eff']
    Eg = np.maximum(E_arr, 1e-15)
    DM = (C_KMS/H0) * np.concatenate([[0.], cumulative_trapezoid(1./Eg, z_grid)])
    tv = np.empty(13)
    for i, (z, qty) in enumerate(zip(z_eff, DESI_DR2['quantity'])):
        idx = min(np.searchsorted(z_grid, z), N_GRID-1)
        DH  = C_KMS / (H0 * Eg[idx])
        DV  = (z * DM[idx]**2 * DH)**(1./3.) if z > 0 else 0.
        if 'DV' in qty:
            tv[i] = DV / R_S
        elif 'DM' in qty:
            tv[i] = DM[idx] / R_S
        elif 'DH' in qty:
            tv[i] = DH / R_S
        else:
            tv[i] = np.nan
    return tv

def chi2_from_tv(tv):
    if tv is None or not np.all(np.isfinite(tv)):
        return 1e8
    d = DESI_DR2['value'] - tv
    return float(d @ DESI_DR2_COV_INV @ d)

# ------------------------------------------------------------------ LCDM

def fit_lcdm():
    def chi2(p):
        Om, H0 = p
        if not (0.05 < Om < 0.70 and 50. < H0 < 100.):
            return 1e8
        z_eff = DESI_DR2['z_eff']
        z_grid = np.linspace(0., z_eff.max()+0.01, N_GRID)
        E = E_lcdm(z_grid, Om)
        return chi2_from_tv(compute_tv_from_E(Om, H0, E, z_grid))
    rng = np.random.default_rng(0)
    best = (1e9, None)
    starts = [(0.30, 67), (0.32, 68), (0.28, 70), (0.10, 66)]
    starts += list(zip(rng.uniform(0.10, 0.45, 12), rng.uniform(60, 78, 12)))
    for s in starts:
        try:
            r = minimize(chi2, s, method='Nelder-Mead',
                         options={'xatol': 1e-7, 'fatol': 1e-7, 'maxiter': 6000})
            if r.fun < best[0]:
                best = (r.fun, r.x)
        except Exception:
            pass
    if best[1] is None:
        return None
    Om, H0 = best[1]
    return {'chi2': float(best[0]), 'Om': float(Om), 'H0': float(H0),
            'k': 2, 'aicc': aicc(best[0], k=2)}

# ------------------------------------------------------------------ V(n,t) candidates

def h_C1(z, zc, p, q=0.5):
    """slow-roll analogue: (1 - exp(-(z/zc)^p)) * tanh((1+z)^q - 1)
    zc>0, p in (0.3, 4), q fixed.
    """
    zc = max(zc, 1e-3); p = max(p, 0.05)
    arg = np.clip((z/zc)**p, 0, 50)
    onset = 1.0 - np.exp(-arg)
    growth = np.tanh(np.clip((1.0+z)**q - 1.0, 0, 30))
    return onset * growth

def h_C2(z, alpha):
    """thawing CPL match: (1 - cos(pi*x/(1+x)))/2, x = alpha*z
    alpha>0
    """
    a = max(alpha, 1e-3)
    x = a * z
    return 0.5 * (1.0 - np.cos(np.pi * x / (1.0 + x)))

def E_with_h(z, Om, h_arr, amp):
    OL0 = 1.0 - Om - OR
    rde = OL0 * (1.0 + amp * h_arr)
    rde = np.where(rde < 0, 0.0, rde)
    E2 = OR*(1+z)**4 + Om*(1+z)**3 + rde
    if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))

def cpl_extract(Om, H0, h_fn, shape_params, amp):
    """Fit (w0, wa) by least-squares on rho_de(z) (z in [0.01, 1.2])."""
    z_arr = np.linspace(0.01, 1.2, 60)
    h_arr = h_fn(z_arr, *shape_params)
    E = E_with_h(z_arr, Om, h_arr, amp)
    if E is None:
        return None, None
    OL0 = 1.0 - Om - OR
    rde = E**2 - OR*(1+z_arr)**4 - Om*(1+z_arr)**3
    rde0 = OL0 * (1.0 + amp * h_fn(np.array([0.0]), *shape_params))[0]
    if rde0 <= 0 or np.any(rde <= 0):
        return None, None
    lnrde = np.log(rde / rde0)
    ln1z = np.log(1+z_arr)
    A = np.column_stack([-3.*ln1z, -3.*(ln1z - z_arr/(1+z_arr))])
    try:
        coef, *_ = np.linalg.lstsq(A, lnrde, rcond=None)
        return float(coef[0]) - 1., float(coef[1])
    except Exception:
        return None, None

# ------------------------------------------------------------------ generic fitter

def fit_candidate(name, h_fn, n_shape, shape_bounds, k_total):
    """k_total = 2 (Om,H0) + n_shape + 1 (amp)
       For G3 honest accounting we use k=k_total in AICc."""
    z_eff = DESI_DR2['z_eff']
    z_grid = np.linspace(0., z_eff.max()+0.01, N_GRID)

    def chi2(p):
        Om, H0, amp = p[0], p[1], p[2]
        shape = p[3:3+n_shape]
        if not (0.05 < Om < 0.70 and 50. < H0 < 100. and -3. < amp < 3.):
            return 1e8
        for v, (lo, hi) in zip(shape, shape_bounds):
            if not (lo < v < hi):
                return 1e8
        h_arr = h_fn(z_grid, *shape)
        if not np.all(np.isfinite(h_arr)):
            return 1e8
        E = E_with_h(z_grid, Om, h_arr, amp)
        if E is None:
            return 1e8
        return chi2_from_tv(compute_tv_from_E(Om, H0, E, z_grid))

    bounds = [(0.05, 0.50), (58., 80.), (-2.5, 2.5)] + list(shape_bounds)
    rng = np.random.default_rng(7)
    best = (1e9, None)
    # multi-start
    Om_seeds = [0.10, 0.15, 0.22, 0.30, 0.35]
    H_seeds  = [65., 68., 70., 72.]
    amp_seeds = [-0.6, -0.2, 0.2, 0.6, 1.0]
    seeds = []
    for Om0 in Om_seeds:
        for H0 in H_seeds:
            for a0 in amp_seeds:
                shp0 = [0.5*(lo+hi) for (lo, hi) in shape_bounds]
                seeds.append([Om0, H0, a0] + shp0)
    # random
    for _ in range(30):
        s = [rng.uniform(0.10, 0.45), rng.uniform(60, 78), rng.uniform(-1.5, 1.5)]
        for (lo, hi) in shape_bounds:
            s.append(rng.uniform(lo, hi))
        seeds.append(s)
    for s in seeds:
        try:
            r = minimize(chi2, s, method='Nelder-Mead',
                         options={'xatol':1e-7, 'fatol':1e-7, 'maxiter':10000})
            if r.fun < best[0]:
                best = (r.fun, r.x)
        except Exception:
            pass
    # DE polish
    try:
        r = differential_evolution(chi2, bounds, popsize=30, maxiter=600,
                                   tol=1e-8, seed=42, workers=1)
        if r.fun < best[0]:
            best = (r.fun, r.x)
    except Exception:
        pass
    if best[1] is None:
        return {'name': name, 'status': 'FAIL_OPT'}
    p = best[1]
    Om, H0, amp = p[0], p[1], p[2]
    shape = list(p[3:3+n_shape])
    chi2v = float(best[0])
    ac    = aicc(chi2v, k=k_total)
    w0, wa = cpl_extract(Om, H0, h_fn, shape, amp)
    return {
        'name': name,
        'chi2': chi2v,
        'k': k_total,
        'aicc': ac,
        'Om': float(Om), 'H0': float(H0), 'amp': float(amp),
        'shape': [float(v) for v in shape],
        'w0': w0, 'wa': wa,
    }

# ------------------------------------------------------------------ gate evaluation

def in_box(w0, wa):
    if w0 is None or wa is None:
        return False, False
    okw0 = (W0_BOX[0] <= w0 <= W0_BOX[1])
    okwa = (WA_BOX[0] <= wa <= WA_BOX[1])
    return okw0, okwa

# ------------------------------------------------------------------ main

def main():
    t0 = time.time()
    print('=== L408 V(n,t) extension gate test ===')
    print(f'DESI DR2 13-pt box: w0 in {W0_BOX}, wa in {WA_BOX}')
    print()

    print('-- LCDM baseline --')
    lcdm = fit_lcdm()
    print(json.dumps(lcdm, indent=2))
    LCDM_AICC = lcdm['aicc']

    print()
    print('-- C1 slow-roll analogue: h = (1-exp(-(z/zc)^p)) * tanh(sqrt(1+z)-1) --')
    res_C1 = fit_candidate(
        'C1_slowroll', h_C1, n_shape=2,
        shape_bounds=[(0.05, 5.0), (0.3, 4.0)],
        k_total=4 + 1,  # Om, H0, amp, zc, p = 5 honest
    )
    print(json.dumps(res_C1, indent=2))

    print()
    print('-- C2 thawing CPL match: h = (1 - cos(pi*x/(1+x)))/2, x=alpha*z --')
    res_C2 = fit_candidate(
        'C2_thawing', h_C2, n_shape=1,
        shape_bounds=[(0.05, 5.0)],
        k_total=3 + 1,  # Om, H0, amp, alpha = 4 honest
    )
    print(json.dumps(res_C2, indent=2))

    print()
    print('=== GATE EVALUATION ===')
    out = {'lcdm': lcdm, 'candidates': {}}
    for r in (res_C1, res_C2):
        name = r['name']
        if 'aicc' not in r:
            out['candidates'][name] = {'status': 'FAIL_OPT'}
            print(f'{name}: FAIL_OPT')
            continue
        d_aicc = r['aicc'] - LCDM_AICC
        ok_w0, ok_wa = in_box(r['w0'], r['wa'])
        g2 = ok_w0 and ok_wa
        g3 = d_aicc < -4.0
        verdict = 'PASS' if (g2 and g3) else 'FAIL'
        out['candidates'][name] = {
            **r, 'd_aicc_vs_lcdm': d_aicc,
            'G2_box_ok': g2, 'G2_w0_ok': ok_w0, 'G2_wa_ok': ok_wa,
            'G3_aicc_ok': g3, 'verdict': verdict,
        }
        print(f"{name}: chi2={r['chi2']:.3f} AICc={r['aicc']:.3f} "
              f"dAICc={d_aicc:+.3f} w0={r['w0']:.3f} wa={r['wa']:.3f} "
              f"G2={'Y' if g2 else 'N'}(w0={ok_w0},wa={ok_wa}) G3={'Y' if g3 else 'N'} -> {verdict}")

    # Overall gate decision (G2 AND G3 from at least one candidate)
    passes = [c for c in out['candidates'].values()
              if isinstance(c, dict) and c.get('verdict') == 'PASS']
    overall = 'OPEN_TIER_B' if passes else 'CLOSE_TIER_B_PERMANENTLY'
    out['overall_gate'] = overall
    print()
    print(f'OVERALL GATE: {overall}')
    print(f'(elapsed: {time.time()-t0:.1f} s)')

    def _jsonify(o):
        if isinstance(o, dict):
            return {k: _jsonify(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [_jsonify(v) for v in o]
        if isinstance(o, (np.bool_,)):
            return bool(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        return o
    out_path = os.path.join(_HERE, 'results.json')
    with open(out_path, 'w') as f:
        json.dump(_jsonify(out), f, indent=2)
    print(f'Wrote {out_path}')
    return out

if __name__ == '__main__':
    main()
