# -*- coding: utf-8 -*-
"""
l40_test.py -- L40: Model S Prior Verification (psi direct)
============================================================
SQT reinterpretation: rho_DE directly proportional to psi(z).
Model S (k=2): rho_DE = OL0 * psi(z)/psi(0)
             = OL0 * (1+alpha)/(1+alpha*(1+z)^3)
E(0)=1 guaranteed analytically.

Task 0: LCDM + Model D baseline reconfirmation
Task 1: Model S (k=2) -- CORE
Task 2: Model S_amp (k=3, amplitude A free)
Task 3: Model S_index (k=3, index n free)
Task 4: Bootstrap (Model S, N=300)
Task 5: CPL w0/wa extraction
Task 6: Residual analysis
Task 7: w(z) visualization
Task 8: Model S vs Model D direct comparison
"""

import os, sys, json, time, warnings
import numpy as np
from scipy.optimize import minimize
import multiprocessing as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')
np.seterr(all='ignore')
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_L35_DIR    = os.path.join(_SCRIPT_DIR, '../l35')
for _p in [os.path.dirname(_SCRIPT_DIR), _L35_DIR]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from l35_test import (
    chi2_bao, chi2_cmb, chi2_sn, chi2_rsd,
    get_sn, E_lcdm,
    OR, C_KMS, N_TOTAL,
    cpl_wa, _growth_fs8,
    Z_RSD, FS8_OBS, FS8_SIG,
    CMB_OBS, CMB_SIG,
    _base as _base35,
    R_S, N_GRID,
    DESI_DR2, DESI_DR2_COV_INV,
)
from scipy.integrate import cumulative_trapezoid

LCDM_AICC = 1670.1227
D_BEST    = {'Om': 0.3220, 'H0': 66.98, 'amp': 0.8178, 'beta': 3.533}
LCDM_BEST = {'Om': 0.3094, 'H0': 68.41}
D_AICC    = 1661.68   # L38 confirmed
N_WORKERS = 8
N_BOOT    = 300


# ─── P1: Boundary detection ───────────────────────────────────────────────────
def _at_boundary(params, bounds, tol=1e-3):
    for p, (lo, hi) in zip(params, bounds):
        span = hi - lo
        if span == 0: continue
        if abs(p - lo) < tol*span or abs(p - hi) < tol*span:
            return True
    return False


# ─── AICc, verdict, helpers ───────────────────────────────────────────────────
def _aicc(chi2_val, k):
    return chi2_val + 2*k + 2*k*(k+1)/(N_TOTAL - k - 1)

def _verdict_s(daicc, boundary=False, k2=False):
    if boundary:     return 'K92 INVALID'
    if daicc >= 0:   return 'K90 KILL'
    if daicc >= -2:  return 'Q90 PASS'
    if daicc < -4 and k2: return 'Q92 GAME'
    return 'Q91 STRONG'

def _H0_tension(H0_fit):
    return (73.04 - H0_fit) / np.sqrt(1.04**2 + 0.5**2)

def _chi2_all(E_fn, Om, H0):
    cb = chi2_bao(E_fn, Om, H0)
    cc = chi2_cmb(E_fn, Om, H0)
    cs = chi2_sn(E_fn,  Om, H0)
    cr = chi2_rsd(E_fn, Om, H0)
    return cb, cc, cs, cr, cb+cc+cs+cr

def _jsonify(obj):
    if isinstance(obj, dict):       return {k: _jsonify(v) for k, v in obj.items()}
    if isinstance(obj, list):       return [_jsonify(v) for v in obj]
    if isinstance(obj, np.ndarray): return _jsonify(obj.tolist())
    if isinstance(obj, bool):       return bool(obj)
    if isinstance(obj, np.integer): return int(obj)
    if isinstance(obj, (np.floating, float)):
        f = float(obj)
        return None if not np.isfinite(f) else f
    return obj


# ─── BAO theory vector (bootstrap) ───────────────────────────────────────────
def _bao_theory_vec(E_fn, Om, H0):
    z_eff  = DESI_DR2['z_eff']
    z_grid = np.linspace(0.0, z_eff.max() + 0.01, N_GRID)
    Eg     = E_fn(z_grid, Om)
    if Eg is None or not np.all(np.isfinite(Eg)): return None
    Eg = np.maximum(Eg, 1e-15)
    DM = (C_KMS/H0) * np.concatenate([[0.], cumulative_trapezoid(1.0/Eg, z_grid)])
    tv = np.empty(13)
    for i, (z, qty) in enumerate(zip(z_eff, DESI_DR2['quantity'])):
        idx = min(np.searchsorted(z_grid, z), N_GRID-1)
        DH  = C_KMS / (H0 * Eg[idx])
        DV  = (z * DM[idx]**2 * DH)**(1./3.) if z > 0 else 0.
        if   'DV' in qty: tv[i] = DV / R_S
        elif 'DM' in qty: tv[i] = DM[idx] / R_S
        elif 'DH' in qty: tv[i] = DH / R_S
        else:              tv[i] = np.nan
    return None if not np.all(np.isfinite(tv)) else tv


# ─── Model D (reference) ─────────────────────────────────────────────────────
def _E_D(z_arr, Om, amp, beta):
    OL0, ratio, _ = _base35(z_arr, Om)
    if OL0 is None: return None
    rde = OL0 * (1.0 + amp * (ratio - 1.0) * np.exp(-abs(beta) * z_arr))
    E2  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
    return None if np.any(E2 <= 0) else np.sqrt(E2)

def _make_E_D(Om, amp, beta):
    def fn(z, _Om): return _E_D(z, Om, amp, beta)
    return fn


# ─── Model S variants ─────────────────────────────────────────────────────────
def _E_S(z_arr, Om):
    """Model S: rho_DE = OL0*(1+alpha)/(1+alpha*(1+z)^3). E(0)=1 exact."""
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0: return None
    alpha  = Om / OL0
    rde    = OL0 * (1.0 + alpha) / (1.0 + alpha * (1.0 + z_arr)**3)
    E2     = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
    return None if np.any(E2 <= 0) else np.sqrt(E2)

def _make_E_S(Om):
    def fn(z, _Om): return _E_S(z, Om)
    return fn


def _E_S_amp(z_arr, Om, A):
    """Model S_amp: rho_DE = A/(1+alpha*(1+z)^3). A_theory = OL0*(1+alpha)."""
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0: return None
    alpha  = Om / OL0
    rde    = A / (1.0 + alpha * (1.0 + z_arr)**3)
    E2     = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
    return None if np.any(E2 <= 0) else np.sqrt(E2)

def _make_E_S_amp(Om, A):
    def fn(z, _Om): return _E_S_amp(z, Om, A)
    return fn


def _E_S_index(z_arr, Om, n):
    """Model S_index: rho_DE = OL0*(1+alpha)/(1+alpha*(1+z)^n). n_theory=3."""
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0: return None
    alpha  = Om / OL0
    rde    = OL0 * (1.0 + alpha) / (1.0 + alpha * (1.0 + z_arr)**n)
    E2     = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
    return None if np.any(E2 <= 0) else np.sqrt(E2)

def _make_E_S_index(Om, n):
    def fn(z, _Om): return _E_S_index(z, Om, n)
    return fn


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Workers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _s_worker(start):
    """Task 1: single start for Model S (Om, H0)."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    bounds = [(0.15, 0.50), (55., 82.)]

    def obj(p):
        Om, H0 = p
        if Om < 0.15 or Om > 0.50 or H0 < 55 or H0 > 82: return 1e9
        E_fn = _make_E_S(Om)
        if E_fn is None: return 1e9
        cb = chi2_bao(E_fn,Om,H0); cc = chi2_cmb(E_fn,Om,H0)
        cs = chi2_sn(E_fn,Om,H0);  cr = chi2_rsd(E_fn,Om,H0)
        tot = cb+cc+cs+cr
        return tot if (np.isfinite(tot) and tot < 1e7) else 1e9

    try:
        r = minimize(obj, start, method='Nelder-Mead',
                     options={'xatol':1e-5,'fatol':1e-5,'maxiter':1000})
        return (float(r.fun), [float(x) for x in r.x])
    except Exception:
        return (1e9, None)


def _s_amp_worker(start):
    """Task 2: single start for Model S_amp (Om, H0, A)."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    bounds = [(0.15,0.50),(55.,82.),(0.01,5.0)]

    def obj(p):
        Om, H0, A = p
        if any(x < b[0] or x > b[1] for x, b in zip(p, bounds)): return 1e9
        E_fn = _make_E_S_amp(Om, A)
        if E_fn is None: return 1e9
        cb = chi2_bao(E_fn,Om,H0); cc = chi2_cmb(E_fn,Om,H0)
        cs = chi2_sn(E_fn,Om,H0);  cr = chi2_rsd(E_fn,Om,H0)
        tot = cb+cc+cs+cr
        return tot if (np.isfinite(tot) and tot < 1e7) else 1e9

    try:
        r = minimize(obj, start, method='Nelder-Mead',
                     options={'xatol':1e-5,'fatol':1e-5,'maxiter':1000})
        return (float(r.fun), [float(x) for x in r.x])
    except Exception:
        return (1e9, None)


def _s_index_worker(start):
    """Task 3: single start for Model S_index (Om, H0, n)."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    bounds = [(0.15,0.50),(55.,82.),(0.5,6.0)]

    def obj(p):
        Om, H0, n = p
        if any(x < b[0] or x > b[1] for x, b in zip(p, bounds)): return 1e9
        E_fn = _make_E_S_index(Om, n)
        if E_fn is None: return 1e9
        cb = chi2_bao(E_fn,Om,H0); cc = chi2_cmb(E_fn,Om,H0)
        cs = chi2_sn(E_fn,Om,H0);  cr = chi2_rsd(E_fn,Om,H0)
        tot = cb+cc+cs+cr
        return tot if (np.isfinite(tot) and tot < 1e7) else 1e9

    try:
        r = minimize(obj, start, method='Nelder-Mead',
                     options={'xatol':1e-5,'fatol':1e-5,'maxiter':1000})
        return (float(r.fun), [float(x) for x in r.x])
    except Exception:
        return (1e9, None)


def _boot_s_worker(args):
    """Task 4: bootstrap batch for Model S (k=2)."""
    boot_batch = args
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    import sys
    _l35 = sys.modules.get('l35_test') or __import__('l35_test')
    orig_bao_dict = dict(_l35.DESI_DR2)
    orig_cmb = _l35.CMB_OBS.copy()
    orig_rsd = _l35.FS8_OBS.copy()

    bounds_S    = [(0.15,0.50),(55.,82.)]
    bounds_LCDM = [(0.15,0.50),(55.,82.)]

    def obj_S(p):
        Om, H0 = p
        if Om<0.15 or Om>0.50 or H0<55 or H0>82: return 1e9
        E_fn = _make_E_S(Om)
        if E_fn is None: return 1e9
        tot = (chi2_bao(E_fn,Om,H0)+chi2_cmb(E_fn,Om,H0)+
               chi2_sn(E_fn,Om,H0)+chi2_rsd(E_fn,Om,H0))
        return tot if (np.isfinite(tot) and tot < 1e7) else 1e9

    def obj_LCDM(p):
        Om, H0 = p
        if Om<0.15 or Om>0.50 or H0<55 or H0>82: return 1e9
        E_fn = lambda z, _: E_lcdm(z, Om)
        tot = (chi2_bao(E_fn,Om,H0)+chi2_cmb(E_fn,Om,H0)+
               chi2_sn(E_fn,Om,H0)+chi2_rsd(E_fn,Om,H0))
        return tot if (np.isfinite(tot) and tot < 1e7) else 1e9

    results = []
    np.random.seed(42)
    for (s0_S, new_bao, new_cmb, new_rsd) in boot_batch:
        _l35.DESI_DR2 = {**orig_bao_dict, 'value': new_bao}
        _l35.CMB_OBS  = new_cmb
        _l35.FS8_OBS  = new_rsd

        best_lcdm, par_lcdm = 1e9, None
        for s in [[0.310,68.4],[0.309,68.0],[0.315,67.5]]:
            try:
                r = minimize(obj_LCDM, s, method='Nelder-Mead',
                             options={'xatol':1e-4,'fatol':1e-4,'maxiter':200})
                if r.fun < best_lcdm: best_lcdm, par_lcdm = r.fun, r.x
            except Exception: pass

        best_S, par_S = 1e9, None
        try:
            r = minimize(obj_S, s0_S, method='Nelder-Mead',
                         options={'xatol':1e-4,'fatol':1e-4,'maxiter':300})
            if r.fun < best_S: best_S, par_S = r.fun, r.x
        except Exception: pass

        if par_lcdm is None or par_S is None:
            results.append(float('nan'))
            continue

        bnd_L = _at_boundary(par_lcdm, bounds_LCDM)
        bnd_S = _at_boundary(par_S,    bounds_S)
        if bnd_L or bnd_S:
            results.append(float('nan'))
        else:
            aicc_lcdm = _aicc(best_lcdm, k=2)
            aicc_S    = _aicc(best_S,    k=2)
            results.append(float(aicc_S - aicc_lcdm))

    _l35.DESI_DR2 = orig_bao_dict
    _l35.CMB_OBS  = orig_cmb
    _l35.FS8_OBS  = orig_rsd
    return results


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Task functions
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def task0_baseline():
    print("\n" + "="*60)
    print("Task 0: Baseline Verification (LCDM + Model D)")
    print("="*60)

    E_lcdm_fn = lambda z, _: E_lcdm(z, LCDM_BEST['Om'])
    cb, cc, cs, cr, ctot = _chi2_all(E_lcdm_fn, LCDM_BEST['Om'], LCDM_BEST['H0'])
    ac_lcdm = _aicc(ctot, k=2)
    print(f"  LCDM: Om={LCDM_BEST['Om']}, H0={LCDM_BEST['H0']}")
    print(f"  chi2: BAO={cb:.4f} CMB={cc:.4f} SN={cs:.4f} RSD={cr:.4f}")
    ok = 'CONFIRMED' if abs(ac_lcdm - LCDM_AICC) < 0.05 else 'CHANGED'
    print(f"  AICc={ac_lcdm:.4f} (stored={LCDM_AICC}) [{ok}]")

    E_D = _make_E_D(D_BEST['Om'], D_BEST['amp'], D_BEST['beta'])
    cb2, cc2, cs2, cr2, ctot2 = _chi2_all(E_D, D_BEST['Om'], D_BEST['H0'])
    ac_D = _aicc(ctot2, k=4)
    ok2 = 'CONFIRMED' if abs(ac_D - D_AICC) < 0.1 else 'CHANGED'
    print(f"  Model D: Om={D_BEST['Om']}, H0={D_BEST['H0']}")
    print(f"  chi2: BAO={cb2:.4f} CMB={cc2:.4f} SN={cs2:.4f} RSD={cr2:.4f}")
    print(f"  AICc={ac_D:.4f}  dAICc={ac_D-LCDM_AICC:.2f} [{ok2}]")

    return {
        'lcdm': {'aicc': float(ac_lcdm), 'chi2_bao': float(cb), 'chi2_cmb': float(cc),
                 'chi2_sn': float(cs), 'chi2_rsd': float(cr)},
        'modelD': {'aicc': float(ac_D), 'daicc': float(ac_D - LCDM_AICC),
                   'chi2_bao': float(cb2), 'chi2_cmb': float(cc2),
                   'chi2_sn': float(cs2), 'chi2_rsd': float(cr2)},
    }


def _run_model_fit(pool, worker_fn, starts, bounds, refine_obj, label, k, is_k2=False):
    """Generic: parallel multi-start -> refine -> report."""
    t0  = time.time()
    raw = pool.map(worker_fn, starts[:len(starts)])
    print(f"  {label} scan done in {time.time()-t0:.1f}s ({len(starts)} starts)")

    best_val, best_par = 1e9, None
    for (val, par) in raw:
        if par is not None and val < best_val:
            best_val, best_par = val, par

    if best_par is not None:
        try:
            r = minimize(refine_obj, best_par, method='Nelder-Mead',
                         options={'xatol':1e-6,'fatol':1e-6,'maxiter':3000})
            if r.fun < best_val: best_val, best_par = r.fun, r.x
        except Exception: pass

    return best_val, best_par


def task1_model_S(pool):
    print("\n" + "="*60)
    print("Task 1: Model S (k=2)  <-- CORE")
    print("="*60)
    bounds = [(0.15,0.50),(55.,82.)]

    np.random.seed(42)
    starts = []
    for Om0 in np.linspace(0.27, 0.38, 7):
        for H0_0 in [64.,66.,68.,70.,72.]:
            starts.append([Om0, H0_0])
    while len(starts) < 50:
        starts.append([np.random.uniform(0.15,0.50), np.random.uniform(55.,82.)])

    def obj_ref(p):
        Om, H0 = p
        if Om<0.15 or Om>0.50 or H0<55 or H0>82: return 1e9
        E_fn = _make_E_S(Om)
        if E_fn is None: return 1e9
        cb=chi2_bao(E_fn,Om,H0); cc=chi2_cmb(E_fn,Om,H0)
        cs=chi2_sn(E_fn,Om,H0);  cr=chi2_rsd(E_fn,Om,H0)
        tot = cb+cc+cs+cr
        return tot if (np.isfinite(tot) and tot<1e7) else 1e9

    best_val, best_par = _run_model_fit(pool, _s_worker, starts[:50], bounds, obj_ref, 'Model S', k=2)

    if best_par is None:
        print("  FAILED"); return None

    Om, H0 = best_par
    E_fn = _make_E_S(Om)
    cb, cc, cs, cr, ctot = _chi2_all(E_fn, Om, H0)
    ac   = _aicc(ctot, k=2)
    dac  = ac - LCDM_AICC
    dac_D = ac - D_AICC
    w0, wa = cpl_wa(E_fn, Om)
    bnd  = _at_boundary(best_par, bounds)
    verd = _verdict_s(dac, boundary=bnd, k2=True)

    # A_theory check (what OL0*(1+alpha) would be)
    OL0 = 1.0 - Om - OR
    alpha = Om / OL0
    A_theory = OL0 * (1.0 + alpha)

    print(f"  Best: Om={Om:.4f}, H0={H0:.2f}")
    print(f"  A_theory=OL0*(1+alpha)={A_theory:.4f}  (implicit amplitude, theory-fixed)")
    print(f"  chi2: BAO={cb:.4f} CMB={cc:.4f} SN={cs:.4f} RSD={cr:.4f}")
    print(f"  AICc={ac:.4f}  dAICc(vs LCDM)={dac:.2f}  dAICc(vs D_k4)={dac_D:.2f}")
    print(f"  boundary: {bnd}")
    w0s = f"{w0:.4f}" if w0 is not None else "None"
    was = f"{wa:.4f}" if wa is not None else "None"
    print(f"  CPL: w0={w0s}, wa={was}")
    print(f"  Verdict: {verd}")

    return {
        'Om': float(Om), 'H0': float(H0), 'A_theory': float(A_theory),
        'chi2_bao': float(cb), 'chi2_cmb': float(cc), 'chi2_sn': float(cs), 'chi2_rsd': float(cr),
        'aicc': float(ac), 'daicc': float(dac), 'daicc_vs_D': float(dac_D),
        'w0': float(w0) if w0 is not None else None,
        'wa': float(wa) if wa is not None else None,
        'boundary': bool(bnd), 'verdict': verd,
    }


def task2_model_S_amp(pool):
    print("\n" + "="*60)
    print("Task 2: Model S_amp (k=3, amplitude A free)")
    print("="*60)
    bounds = [(0.15,0.50),(55.,82.),(0.01,5.0)]

    np.random.seed(42)
    starts = []
    for Om0 in np.linspace(0.28, 0.36, 5):
        for H0_0 in [65.,67.,69.,71.]:
            OL0 = 1.0 - Om0 - OR
            alpha = Om0 / OL0
            A_th = OL0 * (1.0 + alpha)
            for A0 in [A_th*0.7, A_th, A_th*1.3]:
                starts.append([Om0, H0_0, float(A0)])
    while len(starts) < 30:
        s = [np.random.uniform(b[0],b[1]) for b in bounds]
        starts.append(s)

    def obj_ref(p):
        Om, H0, A = p
        if any(x<b[0] or x>b[1] for x,b in zip(p,bounds)): return 1e9
        E_fn = _make_E_S_amp(Om, A)
        if E_fn is None: return 1e9
        cb=chi2_bao(E_fn,Om,H0); cc=chi2_cmb(E_fn,Om,H0)
        cs=chi2_sn(E_fn,Om,H0);  cr=chi2_rsd(E_fn,Om,H0)
        tot=cb+cc+cs+cr
        return tot if (np.isfinite(tot) and tot<1e7) else 1e9

    best_val, best_par = _run_model_fit(pool, _s_amp_worker, starts[:30], bounds, obj_ref, 'S_amp', k=3)

    if best_par is None:
        print("  FAILED"); return None

    Om, H0, A_fit = best_par
    OL0 = 1.0 - Om - OR
    alpha = Om / OL0
    A_theory = OL0 * (1.0 + alpha)
    A_dev = (A_fit - A_theory) / A_theory * 100

    E_fn = _make_E_S_amp(Om, A_fit)
    cb, cc, cs, cr, ctot = _chi2_all(E_fn, Om, H0)
    ac   = _aicc(ctot, k=3)
    dac  = ac - LCDM_AICC
    w0, wa = cpl_wa(E_fn, Om)
    bnd  = _at_boundary(best_par, bounds)
    verd = _verdict_s(dac, boundary=bnd)

    print(f"  Best: Om={Om:.4f}, H0={H0:.2f}, A_fit={A_fit:.4f}")
    print(f"  A_theory={A_theory:.4f}  dev={A_dev:.1f}%")
    print(f"  chi2: BAO={cb:.4f} CMB={cc:.4f} SN={cs:.4f} RSD={cr:.4f}")
    print(f"  AICc={ac:.4f}  dAICc={dac:.2f}")
    print(f"  boundary: {bnd}")
    w0s = f"{w0:.4f}" if w0 is not None else "None"
    was = f"{wa:.4f}" if wa is not None else "None"
    print(f"  CPL: w0={w0s}, wa={was}")
    print(f"  Verdict: {verd}")

    return {
        'Om': float(Om), 'H0': float(H0), 'A_fit': float(A_fit),
        'A_theory': float(A_theory), 'A_dev_pct': float(A_dev),
        'chi2_bao': float(cb), 'chi2_cmb': float(cc), 'chi2_sn': float(cs), 'chi2_rsd': float(cr),
        'aicc': float(ac), 'daicc': float(dac),
        'w0': float(w0) if w0 is not None else None,
        'wa': float(wa) if wa is not None else None,
        'boundary': bool(bnd), 'verdict': verd,
    }


def task3_model_S_index(pool):
    print("\n" + "="*60)
    print("Task 3: Model S_index (k=3, index n free)")
    print("="*60)
    bounds = [(0.15,0.50),(55.,82.),(0.5,6.0)]

    np.random.seed(42)
    starts = []
    for Om0 in np.linspace(0.28, 0.36, 5):
        for H0_0 in [65.,67.,69.,71.]:
            for n0 in [1.5, 2.0, 3.0, 4.0, 5.0]:
                starts.append([Om0, H0_0, n0])
    while len(starts) < 30:
        s = [np.random.uniform(b[0],b[1]) for b in bounds]
        starts.append(s)

    def obj_ref(p):
        Om, H0, n = p
        if any(x<b[0] or x>b[1] for x,b in zip(p,bounds)): return 1e9
        E_fn = _make_E_S_index(Om, n)
        if E_fn is None: return 1e9
        cb=chi2_bao(E_fn,Om,H0); cc=chi2_cmb(E_fn,Om,H0)
        cs=chi2_sn(E_fn,Om,H0);  cr=chi2_rsd(E_fn,Om,H0)
        tot=cb+cc+cs+cr
        return tot if (np.isfinite(tot) and tot<1e7) else 1e9

    best_val, best_par = _run_model_fit(pool, _s_index_worker, starts[:30], bounds, obj_ref, 'S_index', k=3)

    if best_par is None:
        print("  FAILED"); return None

    Om, H0, n_fit = best_par
    n_theory = 3.0
    n_dev = (n_fit - n_theory) / n_theory * 100

    E_fn = _make_E_S_index(Om, n_fit)
    cb, cc, cs, cr, ctot = _chi2_all(E_fn, Om, H0)
    ac   = _aicc(ctot, k=3)
    dac  = ac - LCDM_AICC
    w0, wa = cpl_wa(E_fn, Om)
    bnd  = _at_boundary(best_par, bounds)
    verd = _verdict_s(dac, boundary=bnd)

    print(f"  Best: Om={Om:.4f}, H0={H0:.2f}, n_fit={n_fit:.4f}")
    print(f"  n_theory={n_theory:.1f}  dev={n_dev:.1f}%")
    print(f"  chi2: BAO={cb:.4f} CMB={cc:.4f} SN={cs:.4f} RSD={cr:.4f}")
    print(f"  AICc={ac:.4f}  dAICc={dac:.2f}")
    print(f"  boundary: {bnd}")
    w0s = f"{w0:.4f}" if w0 is not None else "None"
    was = f"{wa:.4f}" if wa is not None else "None"
    print(f"  CPL: w0={w0s}, wa={was}")
    print(f"  Verdict: {verd}")

    return {
        'Om': float(Om), 'H0': float(H0), 'n_fit': float(n_fit),
        'n_theory': n_theory, 'n_dev_pct': float(n_dev),
        'chi2_bao': float(cb), 'chi2_cmb': float(cc), 'chi2_sn': float(cs), 'chi2_rsd': float(cr),
        'aicc': float(ac), 'daicc': float(dac),
        'w0': float(w0) if w0 is not None else None,
        'wa': float(wa) if wa is not None else None,
        'boundary': bool(bnd), 'verdict': verd,
    }


def task4_bootstrap(pool, Om_best, H0_best):
    print("\n" + "="*60)
    print(f"Task 4: Bootstrap (Model S, N={N_BOOT})")
    print("="*60)

    E_fn_best = _make_E_S(Om_best)
    if E_fn_best is None:
        print("  FAILED: E_fn is None"); return None

    tv_best    = _bao_theory_vec(E_fn_best, Om_best, H0_best)
    theory_rsd = _growth_fs8(E_fn_best, Om_best, Z_RSD)
    theory_cmb = CMB_OBS.copy()

    if tv_best is None or theory_rsd is None:
        print("  FAILED: theory computation"); return None

    try:
        COV_BAO = np.linalg.inv(DESI_DR2_COV_INV)
    except Exception:
        print("  FAILED: BAO cov inversion"); return None

    rng = np.random.default_rng(42)
    boot_samples = []
    for _ in range(N_BOOT):
        new_bao = rng.multivariate_normal(tv_best, COV_BAO)
        new_cmb = theory_cmb + rng.normal(0, CMB_SIG)
        new_rsd = theory_rsd + rng.normal(0, FS8_SIG)
        s0 = [Om_best, H0_best]
        boot_samples.append((list(s0), new_bao.tolist(), new_cmb.tolist(), new_rsd.tolist()))

    batch_size = (N_BOOT + N_WORKERS - 1) // N_WORKERS
    batches    = [boot_samples[i:i+batch_size] for i in range(0, N_BOOT, batch_size)]

    t0  = time.time()
    raw = pool.map(_boot_s_worker, batches)
    print(f"  Bootstrap done in {time.time()-t0:.1f}s")

    all_daicc = [x for batch in raw for x in batch if np.isfinite(x)]
    n_valid   = len(all_daicc)
    if n_valid == 0:
        print("  FAILED: no valid samples"); return None

    daicc_arr = np.array(all_daicc)
    med   = float(np.median(daicc_arr))
    lo68  = float(np.percentile(daicc_arr, 16))
    hi68  = float(np.percentile(daicc_arr, 84))
    frac2 = float(np.mean(daicc_arr < -2) * 100)
    frac4 = float(np.mean(daicc_arr < -4) * 100)
    frac0 = float(np.mean(daicc_arr < 0)  * 100)

    print(f"  Valid: {n_valid}/{N_BOOT}")
    print(f"  dAICc median={med:.2f}  68%CI=[{lo68:.2f},{hi68:.2f}]")
    print(f"  dAICc<-4: {frac4:.1f}%  <-2: {frac2:.1f}%  <0: {frac0:.1f}%")
    verdict_t4 = 'PASS' if frac2 > 85 else ('CONDITIONAL' if frac2 > 60 else 'FAIL')
    print(f"  Verdict: {verdict_t4}")

    fig, ax = plt.subplots(figsize=(7,4))
    ax.hist(daicc_arr, bins=40, color='steelblue', alpha=0.8)
    ax.axvline(med, color='r', ls='--', label=f'median={med:.2f}')
    ax.axvline(-2, color='k', ls=':', label='dAICc=-2')
    ax.axvline(-4, color='gray', ls=':', label='dAICc=-4')
    ax.set_xlabel('dAICc'); ax.set_title(f'L40 Bootstrap Model S (N={n_valid})')
    ax.legend(fontsize=9); fig.tight_layout()
    plot_path = os.path.join(_SCRIPT_DIR, 'l40_task4_bootstrap.png')
    fig.savefig(plot_path, dpi=130); plt.close(fig)
    print(f"  Plot: {plot_path}")

    return {
        'n_boot': N_BOOT, 'n_valid': n_valid,
        'daicc_median': med, 'daicc_lo68': lo68, 'daicc_hi68': hi68,
        'frac_below_minus4': frac4, 'frac_below_minus2': frac2, 'frac_below_0': frac0,
        'verdict': verdict_t4,
    }


def task5_cpl(res1, res2, res3):
    print("\n" + "="*60)
    print("Task 5: CPL Extraction")
    print("="*60)

    desi_w0, desi_wa = -0.76, -0.50
    rows = [('Model S', res1), ('S_amp', res2), ('S_index', res3)]
    out = {}
    print(f"  {'Model':<12} {'w0':>8} {'wa':>8} {'direction'}")
    print(f"  {'-'*44}")
    for name, r in rows:
        if r is None:
            print(f"  {name:<12}  FAILED"); out[name] = None; continue
        w0 = r.get('w0'); wa = r.get('wa')
        w0s = f"{w0:.4f}" if w0 is not None else "  None"
        was = f"{wa:.4f}" if wa is not None else "  None"
        wa_dir = 'matched' if (wa is not None and wa < 0) else 'opposite'
        print(f"  {name:<12} {w0s:>8} {was:>8} {wa_dir}")
        out[name] = {'w0': w0, 'wa': wa, 'direction': wa_dir}
    print(f"  DESI observed:  w0={desi_w0:.2f}, wa={desi_wa:.2f}")
    return out


def task6_residuals(res1, res0):
    print("\n" + "="*60)
    print("Task 6: Residuals (Model S vs LCDM)")
    print("="*60)

    if res1 is None:
        print("  SKIPPED: Model S failed"); return None

    l_bao = res0['lcdm']['chi2_bao']; l_cmb = res0['lcdm']['chi2_cmb']
    l_sn  = res0['lcdm']['chi2_sn'];  l_rsd = res0['lcdm']['chi2_rsd']
    l_tot = l_bao + l_cmb + l_sn + l_rsd

    s_bao = res1['chi2_bao']; s_cmb = res1['chi2_cmb']
    s_sn  = res1['chi2_sn'];  s_rsd = res1['chi2_rsd']
    s_tot = s_bao + s_cmb + s_sn + s_rsd

    d_bao = l_bao - s_bao; d_cmb = l_cmb - s_cmb
    d_sn  = l_sn  - s_sn;  d_rsd = l_rsd - s_rsd
    d_tot = l_tot - s_tot

    print(f"  ΔBAO = {d_bao:+.4f}  (S: {s_bao:.2f} vs LCDM: {l_bao:.2f})")
    print(f"  ΔCMB = {d_cmb:+.4f}  (S: {s_cmb:.2f} vs LCDM: {l_cmb:.2f})")
    print(f"  ΔSN  = {d_sn:+.4f}   (S: {s_sn:.2f} vs LCDM: {l_sn:.2f})")
    print(f"  ΔRSD = {d_rsd:+.4f}  (S: {s_rsd:.2f} vs LCDM: {l_rsd:.2f})")
    print(f"  Δtot = {d_tot:+.4f}")
    if abs(d_tot) > 1e-6:
        for nm, dv in [('BAO',d_bao),('CMB',d_cmb),('SN',d_sn),('RSD',d_rsd)]:
            print(f"    {nm}: {dv/d_tot*100:+.1f}%")
    main = max([('BAO',d_bao),('CMB',d_cmb),('SN',d_sn),('RSD',d_rsd)], key=lambda x: x[1])
    print(f"  Main source: {main[0]}")

    return {
        'delta_bao': float(d_bao), 'delta_cmb': float(d_cmb),
        'delta_sn': float(d_sn),   'delta_rsd': float(d_rsd),
        'delta_total': float(d_tot), 'main_source': main[0],
    }


def task7_wz_plot(res1, res2, res3):
    print("\n" + "="*60)
    print("Task 7: w(z) Visualization")
    print("="*60)

    z_arr = np.linspace(0.01, 2.0, 300)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.axhline(-1.0, color='k', ls='--', lw=1.5, label='LCDM (w=-1)')

    def compute_w(E_fn, Om, label, color, ls):
        if E_fn is None: return
        w_arr = []
        for zi in z_arr:
            dz = 1e-4
            try:
                E1 = E_fn(np.array([zi]),      None)[0]
                E2 = E_fn(np.array([zi+dz]),   None)[0]
                rde1 = E1**2 - OR*(1+zi)**4 - Om*(1+zi)**3
                rde2 = E2**2 - OR*(1+zi+dz)**4 - Om*(1+zi+dz)**3
                if rde1 <= 0 or rde2 <= 0: w_arr.append(np.nan); continue
                w_arr.append(-1 - (np.log(rde2)-np.log(rde1))/dz * (1+zi)/3.0)
            except Exception: w_arr.append(np.nan)
        ax.plot(z_arr, w_arr, color=color, ls=ls, lw=2, label=label)

    # Model D
    E_D_fn = _make_E_D(D_BEST['Om'], D_BEST['amp'], D_BEST['beta'])
    compute_w(E_D_fn, D_BEST['Om'], f"Model D (k=4, dAICc=-8.44)", 'blue', '-')

    if res1:
        E_fn = _make_E_S(res1['Om'])
        dac_s = f"{res1['daicc']:.2f}"
        compute_w(E_fn, res1['Om'], f"Model S (k=2, dAICc={dac_s})", 'red', '-')

    if res2:
        E_fn = _make_E_S_amp(res2['Om'], res2['A_fit'])
        compute_w(E_fn, res2['Om'], f"S_amp (k=3, dAICc={res2['daicc']:.2f})", 'green', '--')

    if res3:
        E_fn = _make_E_S_index(res3['Om'], res3['n_fit'])
        compute_w(E_fn, res3['Om'], f"S_index n={res3['n_fit']:.2f} (dAICc={res3['daicc']:.2f})", 'orange', '--')

    ax.set_xlabel('z'); ax.set_ylabel('w(z)')
    ax.set_xlim(0, 2); ax.set_ylim(-2, 1)
    ax.set_title('L40: w(z) — Model S vs Model D vs LCDM')
    ax.legend(fontsize=9); ax.grid(alpha=0.3)
    fig.tight_layout()
    plot_path = os.path.join(_SCRIPT_DIR, 'l40_task7_wz.png')
    fig.savefig(plot_path, dpi=130); plt.close(fig)
    print(f"  Plot: {plot_path}")
    return {'plot': plot_path}


def task8_comparison(res1, res0):
    print("\n" + "="*60)
    print("Task 8: Model S vs Model D Direct Comparison")
    print("="*60)

    if res1 is None:
        print("  SKIPPED: Model S failed"); return None

    dac_S = res1['daicc']
    dac_D = res0['modelD']['daicc']
    dac_diff = res1['aicc'] - res0['modelD']['aicc']

    w0_S = res1.get('w0'); wa_S = res1.get('wa')
    desi_w0 = -0.76

    w0_S_str = f"{w0_S:.3f}" if w0_S is not None else "N/A"
    wa_S_str = f"{wa_S:.3f}" if wa_S is not None else "N/A"

    print(f"  Model S  (k=2): dAICc={dac_S:.2f}  w0={w0_S_str}  wa={wa_S_str}")
    print(f"  Model D  (k=4): dAICc={dac_D:.2f}  w0={res0['modelD'].get('w0_ref','~-1.14')}")
    print(f"  AICc(S) - AICc(D) = {dac_diff:+.2f}")

    if w0_S is not None:
        w0_err_S = abs(w0_S - desi_w0)
        w0_err_D = abs(-1.138 - desi_w0)
        better_w0 = 'S' if w0_err_S < w0_err_D else 'D'
        print(f"  w0 accuracy vs DESI: S err={w0_err_S:.3f}, D err={w0_err_D:.3f} -> {better_w0} better")
    else:
        better_w0 = 'unknown'

    prior_winner = 'S' if dac_S < dac_D - 4 else ('S(marginal)' if dac_S < dac_D else 'D')
    print(f"  Prior status: Model S k=2 (no free params beyond Om/H0)")
    print(f"  Winner by AICc: {prior_winner}")

    return {
        'daicc_S': float(dac_S), 'daicc_D': float(dac_D),
        'aicc_diff': float(dac_diff),
        'w0_S': float(w0_S) if w0_S is not None else None,
        'better_w0': better_w0,
        'prior_winner': prior_winner,
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    print("="*60)
    print("L40: Model S Prior Verification (psi direct)")
    print(f"8-worker parallel  |  LCDM baseline AICc={LCDM_AICC}")
    print("="*60)

    print("\nWarming up SN cache...")
    get_sn(); print("  SN ready.")

    t_total = time.time()
    results = {}
    ctx = mp.get_context('spawn')

    results['task0'] = task0_baseline()

    with ctx.Pool(N_WORKERS) as pool:
        results['task1'] = task1_model_S(pool)
        results['task2'] = task2_model_S_amp(pool)
        results['task3'] = task3_model_S_index(pool)

    r1 = results['task1']
    Om_boot = r1['Om'] if r1 else LCDM_BEST['Om']
    H0_boot = r1['H0'] if r1 else LCDM_BEST['H0']

    with ctx.Pool(N_WORKERS) as pool:
        results['task4'] = task4_bootstrap(pool, Om_boot, H0_boot)

    results['task5'] = task5_cpl(results['task1'], results['task2'], results['task3'])
    results['task6'] = task6_residuals(results['task1'], results['task0'])
    results['task7'] = task7_wz_plot(results['task1'], results['task2'], results['task3'])
    results['task8'] = task8_comparison(results['task1'], results['task0'])

    # ─── Final Summary ────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("L40 RESULTS SUMMARY")
    print("="*60)

    r0 = results['task0']
    print(f"\n[Task 0] Baselines")
    print(f"  LCDM: AICc={r0['lcdm']['aicc']:.2f}")
    print(f"  Model D: AICc={r0['modelD']['aicc']:.2f}  dAICc={r0['modelD']['daicc']:.2f}")

    r1 = results['task1']
    print(f"\n[Task 1] Model S (k=2) <- CORE")
    if r1:
        print(f"  Om={r1['Om']:.4f}, H0={r1['H0']:.2f}")
        print(f"  AICc={r1['aicc']:.2f}  dAICc(LCDM)={r1['daicc']:.2f}  dAICc(D)={r1['daicc_vs_D']:.2f}")
        print(f"  [{r1['verdict']}]")
    else:
        print("  FAILED")

    r2 = results['task2']
    print(f"\n[Task 2] Model S_amp (k=3)")
    if r2:
        print(f"  A_fit={r2['A_fit']:.4f}  A_theory={r2['A_theory']:.4f}  dev={r2['A_dev_pct']:.1f}%")
        print(f"  dAICc={r2['daicc']:.2f}  [{r2['verdict']}]")
    else:
        print("  FAILED")

    r3 = results['task3']
    print(f"\n[Task 3] Model S_index (k=3)")
    if r3:
        print(f"  n_fit={r3['n_fit']:.4f}  n_theory=3.0  dev={r3['n_dev_pct']:.1f}%")
        print(f"  dAICc={r3['daicc']:.2f}  [{r3['verdict']}]")
    else:
        print("  FAILED")

    r4 = results['task4']
    print(f"\n[Task 4] Bootstrap (Model S, N={N_BOOT})")
    if r4:
        print(f"  median={r4['daicc_median']:.2f}  68%CI=[{r4['daicc_lo68']:.2f},{r4['daicc_hi68']:.2f}]")
        print(f"  dAICc<-4: {r4['frac_below_minus4']:.1f}%  <-2: {r4['frac_below_minus2']:.1f}%")
        print(f"  Verdict: {r4['verdict']}")
    else:
        print("  FAILED/SKIPPED")

    r5 = results['task5']
    print(f"\n[Task 5] CPL Extraction")
    if r5:
        for nm in ['Model S', 'S_amp', 'S_index']:
            if r5.get(nm):
                w0 = r5[nm].get('w0'); wa = r5[nm].get('wa')
                w0s = f"{w0:.4f}" if w0 is not None else "None"
                was = f"{wa:.4f}" if wa is not None else "None"
                print(f"  {nm}: w0={w0s}, wa={was}  [{r5[nm].get('direction','?')}]")

    r6 = results['task6']
    if r6:
        print(f"\n[Task 6] Residuals (Model S vs LCDM)")
        print(f"  ΔBAO={r6['delta_bao']:+.2f}  ΔCMB={r6['delta_cmb']:+.2f}  ΔSN={r6['delta_sn']:+.2f}  ΔRSD={r6['delta_rsd']:+.2f}")
        print(f"  Main source: {r6['main_source']}")

    r8 = results['task8']
    if r8:
        print(f"\n[Task 8] Model S vs Model D")
        print(f"  AICc(S) - AICc(D) = {r8['aicc_diff']:+.2f}")
        print(f"  w0 better: {r8['better_w0']}")
        print(f"  Winner: {r8['prior_winner']}")

    # Final verdict
    print(f"\n[Final Verdict]")
    if r1 and r1['verdict'] == 'Q92 GAME':
        print(f"  Strategy A: Model S k=2 GAME (dAICc={r1['daicc']:.2f}) -> SQT prior WINS")
    elif r1 and r1['daicc'] < -2:
        print(f"  Strategy A/B: Model S STRONG (dAICc={r1['daicc']:.2f})")
    elif r1 and r1['daicc'] < 0:
        print(f"  Strategy B: Model S PASS (dAICc={r1['daicc']:.2f}) -> Model D preferred")
    else:
        dac_s = f"{r1['daicc']:.2f}" if r1 else "N/A"
        print(f"  Strategy C: Model S FAIL (dAICc={dac_s}) -> Model D phenomenological")

    elapsed = time.time() - t_total
    print(f"\nTotal elapsed: {elapsed:.1f}s")

    out_path = os.path.join(_SCRIPT_DIR, 'l40_results.json')
    with open(out_path, 'w') as f:
        json.dump(_jsonify(results), f, indent=2)
    print(f"Saved: {out_path}")


if __name__ == '__main__':
    main()
