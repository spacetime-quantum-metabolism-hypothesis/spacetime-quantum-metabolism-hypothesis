# -*- coding: utf-8 -*-
"""
l38_test.py -- L38: Model D 학술 발표 검증
============================================
Task 0: ΛCDM baseline 재확인
Task 1: Bootstrap robustness (500회, parametric, 8-worker)
Task 2: Profile dAICc robustness (Om/H0 재최적화, P2 patch)
Task 3: Model simplification (k=2,3,4)
Task 4: w0waCDM CPL 비교
Task 5: BAO-only k=3 beta 고정 (P4 patch, L37 K92 재분석)
Task 6: 잔차 분석

Patches from L37 code review:
  P1: boundary detection in all workers (K92 auto-flag)
  P2: profile robustness (Om/H0 re-optimized at each grid point)
  P3: H0 profile error (grid-based, not diagonal Hessian)
  P4: BAO-only k=3 with beta fixed
"""

import os, sys, json, time, warnings
import numpy as np
from scipy.optimize import minimize
from scipy.interpolate import interp1d
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
    OR, C_KMS, N_TOTAL, SIGMA_8_0,
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
N_WORKERS = 8
N_BOOT    = 500
BETA_FIXED = 3.533   # Task 5 BAO-only k=3


# ─── P1: Boundary detection utility ──────────────────────────────────────────
def _at_boundary(params, bounds, tol=1e-3):
    for p, (lo, hi) in zip(params, bounds):
        span = hi - lo
        if span == 0: continue
        if abs(p - lo) < tol*span or abs(p - hi) < tol*span:
            return True
    return False


# ─── Model D and CPL ─────────────────────────────────────────────────────────
def _E_D(z_arr, Om, amp, beta):
    OL0, ratio, _ = _base35(z_arr, Om)
    if OL0 is None: return None
    rde = OL0 * (1.0 + amp * (ratio - 1.0) * np.exp(-abs(beta) * z_arr))
    E2  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
    return None if np.any(E2 <= 0) else np.sqrt(E2)

def _make_E_D(Om, amp, beta):
    def fn(z, _Om): return _E_D(z, Om, amp, beta)
    return fn

def _E_CPL(z_arr, Om, w0=-1.0, wa=0.0):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0: return None
    rde = OL0 * (1+z_arr)**(3*(1+w0+wa)) * np.exp(-3*wa*z_arr/(1+z_arr))
    E2  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
    return None if np.any(E2 <= 0) else np.sqrt(E2)

def _make_E_CPL(Om, w0, wa):
    def fn(z, _Om): return _E_CPL(z, Om, w0, wa)
    return fn


# ─── AICc and verdict ─────────────────────────────────────────────────────────
def _aicc(chi2_val, k):
    return chi2_val + 2*k + 2*k*(k+1)/(N_TOTAL - k - 1)

def _verdict(daicc, wa, H0_tension, boundary=False):
    if boundary:    return 'K92 INVALID'
    if daicc >= 0:  return 'K90 KILL'
    if daicc >= -2: return 'Q90 PASS'
    wa_ok = (wa is not None and wa < 0)
    h0_ok = (H0_tension is not None and H0_tension < 4.01)
    if daicc < -4 and wa_ok and h0_ok: return 'Q92 GAME'
    return 'Q91 STRONG'

def _H0_tension(H0_fit):
    return (73.04 - H0_fit) / np.sqrt(1.04**2 + 0.5**2)


# ─── JSON serializer ──────────────────────────────────────────────────────────
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


# ─── BAO theory vector (needed for bootstrap) ─────────────────────────────────
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


# ─── chi2_all helper ──────────────────────────────────────────────────────────
def _chi2_all(E_fn, Om, H0):
    cb = chi2_bao(E_fn, Om, H0)
    cc = chi2_cmb(E_fn, Om, H0)
    cs = chi2_sn(E_fn,  Om, H0)
    cr = chi2_rsd(E_fn, Om, H0)
    return cb, cc, cs, cr, cb+cc+cs+cr


# ─── V-series: ψ(z) helper and E functions ───────────────────────────────────
def _psi_parts(z_arr, Om):
    """OL0, psi(z), psi0 — direct computation (no ratio clipping)."""
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0: return None, None, None
    alpha = Om / OL0
    psi_z = 1.0 / (1.0 + alpha * (1.0 + z_arr)**3)
    psi0  = 1.0 / (1.0 + alpha)
    return OL0, psi_z, psi0


def _E_V1a(z_arr, Om, A, n):
    """V1a: rho_DE = A*(1-psi(z))^n  (no normalization forcing)."""
    OL0, psi_z, _ = _psi_parts(z_arr, Om)
    if OL0 is None: return None
    rde = A * (1.0 - psi_z)**n
    E2  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
    return None if np.any(E2 <= 0) else np.sqrt(E2)

def _make_E_V1a(Om, A, n):
    def fn(z, _Om): return _E_V1a(z, Om, A, n)
    return fn


def _E_V1b(z_arr, Om, n):
    """V1b: rho_DE = OL0*[(1-psi(z))/(1-psi0)]^n  (rho_DE(0)=OL0)."""
    OL0, psi_z, psi0 = _psi_parts(z_arr, Om)
    if OL0 is None: return None
    omp0 = 1.0 - psi0   # = Om/(Om+OL0) > 0
    if omp0 <= 0: return None
    rde = OL0 * ((1.0 - psi_z) / omp0)**n
    E2  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
    return None if np.any(E2 <= 0) else np.sqrt(E2)

def _make_E_V1b(Om, n):
    def fn(z, _Om): return _E_V1b(z, Om, n)
    return fn


def _E_V2prime(z_arr, Om, C):
    """V2': rho_DE = C*(1/2)*(1-psi(z))^2  [V(psi)=mu^2/2*(psi-1)^2, C absorbs mu^2]."""
    OL0, psi_z, _ = _psi_parts(z_arr, Om)
    if OL0 is None: return None
    rde = C * 0.5 * (1.0 - psi_z)**2
    E2  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
    return None if np.any(E2 <= 0) else np.sqrt(E2)

def _make_E_V2prime(Om, C):
    def fn(z, _Om): return _E_V2prime(z, Om, C)
    return fn


V3_BETA_FIXED = 1.0

def _E_V3(z_arr, Om, amp, beta=V3_BETA_FIXED):
    """V3: rho_DE = OL0*(psi(z)/psi0)*(1+amp*exp(-beta*z))."""
    OL0, psi_z, psi0 = _psi_parts(z_arr, Om)
    if OL0 is None or psi0 <= 0: return None
    rde = OL0 * (psi_z / psi0) * (1.0 + amp * np.exp(-abs(beta) * z_arr))
    E2  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
    return None if np.any(E2 <= 0) else np.sqrt(E2)

def _make_E_V3(Om, amp, beta=V3_BETA_FIXED):
    def fn(z, _Om): return _E_V3(z, Om, amp, beta)
    return fn


def _E_V4(z_arr, Om, A):
    """V4: rho_DE = A*(1+z)^3*psi(z)  [annihilation energy accumulation]."""
    OL0, psi_z, _ = _psi_parts(z_arr, Om)
    if OL0 is None: return None
    rde = A * (1.0 + z_arr)**3 * psi_z
    E2  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
    return None if np.any(E2 <= 0) else np.sqrt(E2)

def _make_E_V4(Om, A):
    def fn(z, _Om): return _E_V4(z, Om, A)
    return fn


def _make_E_from_type(model_type, params):
    """Construct E_fn from model_type string and param array [Om, H0, ...]."""
    Om = params[0]
    if model_type == 'ModelD':   return _make_E_D(Om, params[2], params[3])
    if model_type == 'V1a_k3':  return _make_E_V1a(Om, params[2], 2.0)
    if model_type == 'V1a_k4':  return _make_E_V1a(Om, params[2], params[3])
    if model_type == 'V1b':     return _make_E_V1b(Om, params[2])
    if model_type == 'V2prime': return _make_E_V2prime(Om, params[2])
    if model_type == 'V3':      return _make_E_V3(Om, params[2])
    if model_type == 'V4':      return _make_E_V4(Om, params[2])
    return None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Worker functions (module-level for spawn)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _boot_worker(args):
    """Task 1 bootstrap: handle a batch of bootstrap samples."""
    boot_batch = args  # list of (new_bao, new_cmb, new_rsd)
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    import sys
    _l35 = sys.modules.get('l35_test') or __import__('l35_test')
    orig_bao_dict = dict(_l35.DESI_DR2)
    orig_cmb = _l35.CMB_OBS.copy()
    orig_rsd = _l35.FS8_OBS.copy()

    bounds_D    = [(0.15,0.50),(55.,82.),(-3.0,3.0),(0.01,5.)]
    bounds_LCDM = [(0.15,0.50),(55.,82.)]

    def obj_D(p):
        Om, H0, amp, beta = p
        if any(x < b[0] or x > b[1] for x, b in zip(p, bounds_D)): return 1e9
        E_fn = _make_E_D(Om, amp, beta)
        if E_fn is None: return 1e9
        cb  = chi2_bao(E_fn, Om, H0); cc = chi2_cmb(E_fn, Om, H0)
        cs  = chi2_sn(E_fn,  Om, H0); cr = chi2_rsd(E_fn, Om, H0)
        tot = cb+cc+cs+cr
        return tot if np.isfinite(tot) and tot < 1e7 else 1e9

    def obj_LCDM(p):
        Om, H0 = p
        if Om < 0.15 or Om > 0.50 or H0 < 55 or H0 > 82: return 1e9
        E_fn = lambda z, _: E_lcdm(z, Om)
        cb = chi2_bao(E_fn, Om, H0); cc = chi2_cmb(E_fn, Om, H0)
        cs = chi2_sn(E_fn,  Om, H0); cr = chi2_rsd(E_fn, Om, H0)
        tot = cb+cc+cs+cr
        return tot if np.isfinite(tot) and tot < 1e7 else 1e9

    results = []
    np.random.seed(42)
    for (new_bao, new_cmb, new_rsd) in boot_batch:
        # Inject perturbed data into l35_test module
        _l35.DESI_DR2 = {**orig_bao_dict, 'value': new_bao}
        _l35.CMB_OBS  = new_cmb
        _l35.FS8_OBS  = new_rsd

        # Fit ΛCDM (fast: k=2, 3 starts)
        best_lcdm, par_lcdm = 1e9, None
        for s in [[0.310, 68.4], [0.309, 68.0], [0.315, 67.5]]:
            try:
                r = minimize(obj_LCDM, s, method='Nelder-Mead',
                             options={'xatol':1e-4,'fatol':1e-4,'maxiter':200})
                if r.fun < best_lcdm: best_lcdm, par_lcdm = r.fun, r.x
            except Exception: pass

        # Fit Model D (k=4, 1 start from L36 best)
        s0 = [D_BEST['Om'], D_BEST['H0'], D_BEST['amp'], D_BEST['beta']]
        best_D, par_D = 1e9, None
        try:
            r = minimize(obj_D, s0, method='Nelder-Mead',
                         options={'xatol':1e-4,'fatol':1e-4,'maxiter':300})
            if r.fun < best_D: best_D, par_D = r.fun, r.x
        except Exception: pass

        if par_lcdm is None or par_D is None:
            results.append((float('nan'), float('nan'), float('nan')))
            continue

        aicc_lcdm = _aicc(best_lcdm, k=2)
        aicc_D    = _aicc(best_D,    k=4)
        daicc     = aicc_D - aicc_lcdm
        amp_boot  = float(par_D[2]) if par_D is not None else float('nan')
        beta_boot = float(par_D[3]) if par_D is not None else float('nan')
        bnd_D    = _at_boundary(par_D,    bounds_D)    if par_D    is not None else False
        bnd_LCDM = _at_boundary(par_lcdm, bounds_LCDM) if par_lcdm is not None else False
        if bnd_D or bnd_LCDM:
            results.append((float('nan'), float('nan'), float('nan')))
        else:
            results.append((float(daicc), amp_boot, beta_boot))

    # Restore original data
    _l35.DESI_DR2 = orig_bao_dict
    _l35.CMB_OBS  = orig_cmb
    _l35.FS8_OBS  = orig_rsd
    return results


def _profile_worker(args):
    """Task 2: profile dAICc by re-optimizing Om, H0 at fixed (amp, beta)."""
    grid_chunk = args  # list of (amp, beta)
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    bounds_2d = [(0.15, 0.50), (55., 82.)]

    def profile_daicc(amp, beta):
        def obj(p):
            Om, H0 = p
            if Om < 0.15 or Om > 0.50 or H0 < 55 or H0 > 82: return 1e9
            E_fn = _make_E_D(Om, amp, beta)
            if E_fn is None: return 1e9
            cb = chi2_bao(E_fn, Om, H0); cc = chi2_cmb(E_fn, Om, H0)
            cs = chi2_sn(E_fn,  Om, H0); cr = chi2_rsd(E_fn, Om, H0)
            tot = cb+cc+cs+cr
            return tot if np.isfinite(tot) and tot < 1e7 else 1e9

        np.random.seed(42)
        best_val, best_p = 1e9, None
        for s in [[0.322, 66.98], [0.310, 68.0], [0.330, 66.0]]:
            try:
                r = minimize(obj, s, method='Nelder-Mead',
                             options={'xatol':1e-4,'fatol':1e-4,'maxiter':300})
                if r.fun < best_val: best_val, best_p = r.fun, r.x
            except Exception: pass
        if best_val >= 1e8 or best_p is None: return float('nan')
        if _at_boundary(best_p, bounds_2d): return float('nan')
        return float(_aicc(best_val, k=4) - LCDM_AICC)

    results = []
    for (amp, beta) in grid_chunk:
        daicc = profile_daicc(amp, beta)
        results.append((float(amp), float(beta), daicc))
    return results


def _simp_worker(args):
    """Task 3: Model simplification - fit one model variant."""
    variant_name, fixed_params, free_bounds, n_starts = args
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')

    def make_E(p_free):
        # fixed_params: dict {name: value} for amp and/or beta
        Om  = p_free[0]; H0  = p_free[1]
        amp  = fixed_params.get('amp',  p_free[2] if len(p_free) > 2 else D_BEST['amp'])
        beta = fixed_params.get('beta', p_free[3] if len(p_free) > 3 else D_BEST['beta'])
        if len(p_free) == 3:
            # one extra free param
            if 'amp' not in fixed_params:  amp  = p_free[2]
            if 'beta' not in fixed_params: beta = p_free[2]
        return _make_E_D(Om, amp, beta)

    def obj(p):
        for pv, (lo, hi) in zip(p, free_bounds):
            if pv < lo or pv > hi: return 1e9
        E_fn = make_E(p)
        Om, H0 = p[0], p[1]
        if E_fn is None: return 1e9
        cb = chi2_bao(E_fn, Om, H0); cc = chi2_cmb(E_fn, Om, H0)
        cs = chi2_sn(E_fn,  Om, H0); cr = chi2_rsd(E_fn, Om, H0)
        tot = cb+cc+cs+cr
        return tot if np.isfinite(tot) and tot < 1e7 else 1e9

    np.random.seed(42)
    starts = []
    for Om0 in np.linspace(0.29, 0.34, 3):
        for H0_0 in [66., 68., 70.]:
            mid = [(b[0]+b[1])/2 for b in free_bounds[2:]]
            starts.append([Om0, H0_0] + mid)
    while len(starts) < n_starts:
        row = [np.random.uniform(b[0], b[1]) for b in free_bounds]
        starts.append(row)

    best_val, best_par = 1e9, None
    for s in starts[:n_starts]:
        try:
            r = minimize(obj, s, method='Nelder-Mead',
                         options={'xatol':1e-4,'fatol':1e-4,'maxiter':500})
            if r.fun < best_val: best_val, best_par = r.fun, r.x
        except Exception: pass

    if best_par is not None:
        try:
            r = minimize(obj, best_par, method='Nelder-Mead',
                         options={'xatol':1e-6,'fatol':1e-6,'maxiter':2000})
            if r.fun < best_val: best_val, best_par = r.fun, r.x
        except Exception: pass

    if best_par is None:
        return {'name': variant_name, 'failed': True}

    k = len(free_bounds)
    E_fn = make_E(best_par)
    Om, H0 = best_par[0], best_par[1]
    cb, cc, cs, cr, ctot = _chi2_all(E_fn, Om, H0)
    ac   = _aicc(ctot, k)
    dac  = ac - LCDM_AICC
    w0, wa = cpl_wa(E_fn, Om)
    bnd = _at_boundary(best_par, free_bounds)

    return {
        'name': variant_name, 'k': k, 'failed': False,
        'params': {f'p{i}': float(v) for i, v in enumerate(best_par)},
        'fixed':  fixed_params,
        'chi2_bao': float(cb), 'chi2_cmb': float(cc),
        'chi2_sn':  float(cs), 'chi2_rsd': float(cr),
        'chi2_joint': float(ctot), 'aicc': float(ac), 'daicc': float(dac),
        'w0': float(w0) if w0 else None, 'wa': float(wa) if wa else None,
        'boundary': bool(bnd),
        'verdict': _verdict(dac, wa, _H0_tension(H0), bnd),
    }


def _cpl_worker(start):
    """Task 4: single CPL optimization start."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    bounds = [(0.15,0.50),(55.,82.),(-2.5,0.5),(-3.,3.)]

    def obj(p):
        Om, H0, w0, wa = p
        if any(x < b[0] or x > b[1] for x, b in zip(p, bounds)): return 1e9
        E_fn = _make_E_CPL(Om, w0, wa)
        if E_fn is None: return 1e9
        cb = chi2_bao(E_fn, Om, H0); cc = chi2_cmb(E_fn, Om, H0)
        cs = chi2_sn(E_fn,  Om, H0); cr = chi2_rsd(E_fn, Om, H0)
        tot = cb+cc+cs+cr
        return tot if np.isfinite(tot) and tot < 1e7 else 1e9

    try:
        r = minimize(obj, start, method='Nelder-Mead',
                     options={'xatol':1e-5,'fatol':1e-5,'maxiter':1000})
        return (float(r.fun), [float(x) for x in r.x])
    except Exception:
        return (1e9, None)


def _bao_k3_worker(start):
    """Task 5: BAO-only k=3, beta fixed at BETA_FIXED."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    bounds = [(0.15,0.50),(55.,82.),(0.5,10.0)]  # Om, H0, amp; beta fixed

    def obj(p):
        Om, H0, amp = p
        if any(x < b[0] or x > b[1] for x, b in zip(p, bounds)): return 1e9
        E_fn = _make_E_D(Om, amp, BETA_FIXED)
        if E_fn is None: return 1e9
        v = chi2_bao(E_fn, Om, H0)
        return v if (np.isfinite(v) and v < 1e7) else 1e9

    try:
        r = minimize(obj, start, method='Nelder-Mead',
                     options={'xatol':1e-5,'fatol':1e-5,'maxiter':1000})
        return (float(r.fun), [float(x) for x in r.x])
    except Exception:
        return (1e9, None)


def _v_worker(args):
    """Task V: generic V-series (+ Model D re-fit) worker."""
    variant_name, model_type, bounds, n_starts = args
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')

    def obj(p):
        for pv, (lo, hi) in zip(p, bounds):
            if pv < lo or pv > hi: return 1e9
        Om, H0 = p[0], p[1]
        E_fn = _make_E_from_type(model_type, p)
        if E_fn is None: return 1e9
        cb = chi2_bao(E_fn,Om,H0); cc = chi2_cmb(E_fn,Om,H0)
        cs = chi2_sn(E_fn,Om,H0);  cr = chi2_rsd(E_fn,Om,H0)
        tot = cb+cc+cs+cr
        return tot if np.isfinite(tot) and tot < 1e7 else 1e9

    np.random.seed(42)
    starts = []
    for Om0 in np.linspace(0.28, 0.34, 4):
        for H0_0 in [65., 67., 69., 71.]:
            mid = [(b[0]+b[1])/2 for b in bounds[2:]]
            starts.append([Om0, H0_0] + mid)
    while len(starts) < n_starts:
        starts.append([np.random.uniform(b[0], b[1]) for b in bounds])

    best_val, best_par = 1e9, None
    for s in starts[:n_starts]:
        try:
            r = minimize(obj, s, method='Nelder-Mead',
                        options={'xatol':1e-4,'fatol':1e-4,'maxiter':500})
            if r.fun < best_val: best_val, best_par = r.fun, r.x
        except Exception: pass

    if best_par is not None:
        try:
            r = minimize(obj, best_par, method='Nelder-Mead',
                        options={'xatol':1e-6,'fatol':1e-6,'maxiter':2000})
            if r.fun < best_val: best_val, best_par = r.fun, r.x
        except Exception: pass

    if best_par is None:
        return {'name': variant_name, 'model_type': model_type, 'failed': True}

    k = len(bounds)
    Om, H0 = best_par[0], best_par[1]
    E_fn = _make_E_from_type(model_type, best_par)
    cb, cc, cs, cr, ctot = _chi2_all(E_fn, Om, H0)
    ac   = _aicc(ctot, k)
    dac  = ac - LCDM_AICC
    w0, wa = cpl_wa(E_fn, Om)
    bnd  = _at_boundary(best_par, bounds)
    H0_t = _H0_tension(H0)
    v    = _verdict(dac, wa, H0_t, bnd)

    return {
        'name': variant_name, 'model_type': model_type, 'k': k, 'failed': False,
        'params': {f'p{i}': float(x) for i, x in enumerate(best_par)},
        'bounds': [(float(lo), float(hi)) for lo, hi in bounds],
        'chi2_bao': float(cb), 'chi2_cmb': float(cc),
        'chi2_sn':  float(cs), 'chi2_rsd': float(cr),
        'chi2_joint': float(ctot), 'aicc': float(ac), 'daicc': float(dac),
        'w0': float(w0) if w0 is not None else None,
        'wa': float(wa) if wa is not None else None,
        'H0_tension': float(H0_t), 'boundary': bool(bnd), 'verdict': v,
    }


def _boot_worker_v(args):
    """Task 1 bootstrap for winner V-series model (or Model D)."""
    model_type, bounds_v, boot_batch = args
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    import sys
    _l35 = sys.modules.get('l35_test') or __import__('l35_test')
    orig_bao_dict = dict(_l35.DESI_DR2)
    orig_cmb = _l35.CMB_OBS.copy()
    orig_rsd = _l35.FS8_OBS.copy()

    bounds_LCDM = [(0.15,0.50),(55.,82.)]
    k_v = len(bounds_v)

    def obj_V(p):
        for pv, (lo, hi) in zip(p, bounds_v):
            if pv < lo or pv > hi: return 1e9
        Om, H0 = p[0], p[1]
        E_fn = _make_E_from_type(model_type, p)
        if E_fn is None: return 1e9
        tot = (chi2_bao(E_fn,Om,H0)+chi2_cmb(E_fn,Om,H0)+
               chi2_sn(E_fn,Om,H0) +chi2_rsd(E_fn,Om,H0))
        return tot if np.isfinite(tot) and tot < 1e7 else 1e9

    def obj_LCDM(p):
        Om, H0 = p
        if Om<0.15 or Om>0.50 or H0<55 or H0>82: return 1e9
        E_fn = lambda z, _: E_lcdm(z, Om)
        tot = (chi2_bao(E_fn,Om,H0)+chi2_cmb(E_fn,Om,H0)+
               chi2_sn(E_fn,Om,H0) +chi2_rsd(E_fn,Om,H0))
        return tot if np.isfinite(tot) and tot < 1e7 else 1e9

    results = []
    np.random.seed(42)
    for (s0_v, new_bao, new_cmb, new_rsd) in boot_batch:
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

        best_V, par_V = 1e9, None
        try:
            r = minimize(obj_V, s0_v, method='Nelder-Mead',
                       options={'xatol':1e-4,'fatol':1e-4,'maxiter':300})
            if r.fun < best_V: best_V, par_V = r.fun, r.x
        except Exception: pass

        if par_lcdm is None or par_V is None:
            results.append((float('nan'), float('nan')))
            continue

        aicc_lcdm = _aicc(best_lcdm, k=2)
        aicc_V    = _aicc(best_V, k=k_v)
        daicc = aicc_V - aicc_lcdm
        bnd_V = _at_boundary(par_V,    bounds_v)
        bnd_L = _at_boundary(par_lcdm, bounds_LCDM)
        if bnd_V or bnd_L:
            results.append((float('nan'), float('nan')))
        else:
            results.append((float(daicc), float(par_V[2])))

    _l35.DESI_DR2 = orig_bao_dict
    _l35.CMB_OBS  = orig_cmb
    _l35.FS8_OBS  = orig_rsd
    return results


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Task functions
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def task0_baseline():
    print("\n" + "="*60)
    print("Task 0: ΛCDM Baseline Verification")
    print("="*60)

    E_lcdm_fn = lambda z, _Om: E_lcdm(z, LCDM_BEST['Om'])
    cb, cc, cs, cr, ctot = _chi2_all(E_lcdm_fn, LCDM_BEST['Om'], LCDM_BEST['H0'])
    ac   = _aicc(ctot, k=2)
    delta = abs(ac - LCDM_AICC)
    status = 'CONFIRMED' if delta < 0.05 else 'CHANGED'

    print(f"  Om={LCDM_BEST['Om']}, H0={LCDM_BEST['H0']}")
    print(f"  chi2: BAO={cb:.4f} CMB={cc:.4f} SN={cs:.4f} RSD={cr:.4f}")
    print(f"  AICc={ac:.4f} (stored={LCDM_AICC}) delta={delta:.4f} [{status}]")
    return {'aicc': float(ac), 'delta': float(delta), 'status': status,
            'chi2_bao': float(cb), 'chi2_cmb': float(cc),
            'chi2_sn':  float(cs), 'chi2_rsd': float(cr)}


def task1_bootstrap(pool):
    print("\n" + "="*60)
    print(f"Task 1: Bootstrap Robustness (N={N_BOOT}, 8-worker)")
    print("="*60)

    # Pre-compute theory predictions at Model D best-fit
    E_D = _make_E_D(D_BEST['Om'], D_BEST['amp'], D_BEST['beta'])
    tv_D  = _bao_theory_vec(E_D, D_BEST['Om'], D_BEST['H0'])

    # CMB theory at Model D best-fit
    import l35_test as _l35
    _l35_CMB_SIG = CMB_SIG
    # Approximate CMB theory by computing chi2 components
    # We use CMB_OBS as proxy for theory since chi2_cmb ~ 0.10 at best-fit
    # (near perfect fit → theory ≈ obs). Use observed values + small offset.
    # More precisely: compute from chi2_cmb internals
    # For bootstrap, use observed values as "approximate theory" (conservative)
    theory_cmb = CMB_OBS.copy()  # chi2_cmb=0.10 → theory ≈ obs
    theory_rsd = _growth_fs8(E_D, D_BEST['Om'], Z_RSD)

    if tv_D is None or theory_rsd is None:
        print("  FAILED: theory computation")
        return None

    # Forward BAO covariance
    try:
        COV_BAO = np.linalg.inv(DESI_DR2_COV_INV)
    except Exception:
        print("  FAILED: BAO covariance inversion")
        return None

    # Generate bootstrap samples
    rng = np.random.default_rng(42)
    boot_samples = []
    for _ in range(N_BOOT):
        new_bao = rng.multivariate_normal(tv_D, COV_BAO)
        new_cmb = theory_cmb + rng.normal(0, CMB_SIG)
        new_rsd = theory_rsd + rng.normal(0, FS8_SIG)
        boot_samples.append((new_bao.tolist(), new_cmb.tolist(), new_rsd.tolist()))

    # Split into 8 batches for workers
    batch_size = (N_BOOT + N_WORKERS - 1) // N_WORKERS
    batches    = [boot_samples[i:i+batch_size] for i in range(0, N_BOOT, batch_size)]

    t0 = time.time()
    raw_results = pool.map(_boot_worker, batches)
    elapsed = time.time() - t0
    print(f"  Bootstrap done in {elapsed:.1f}s")

    # Flatten
    all_daicc = []; all_amp = []; all_beta = []
    for batch_res in raw_results:
        for (da, amp, beta) in batch_res:
            if np.isfinite(da) and np.isfinite(amp) and np.isfinite(beta):
                all_daicc.append(da); all_amp.append(amp); all_beta.append(beta)

    n_valid = len(all_daicc)
    if n_valid == 0:
        print("  FAILED: no valid samples")
        return None

    daicc_arr = np.array(all_daicc)
    amp_arr   = np.array(all_amp)
    beta_arr  = np.array(all_beta)

    med   = float(np.median(daicc_arr))
    lo68  = float(np.percentile(daicc_arr, 16))
    hi68  = float(np.percentile(daicc_arr, 84))
    frac4 = float(np.mean(daicc_arr < -4) * 100)
    frac0 = float(np.mean(daicc_arr < 0)  * 100)

    print(f"  Valid samples: {n_valid}/{N_BOOT}")
    print(f"  ΔAICc median={med:.2f}, 68% CI=[{lo68:.2f}, {hi68:.2f}]")
    print(f"  ΔAICc<-4: {frac4:.1f}%  ΔAICc<0: {frac0:.1f}%")
    print(f"  amp:  {amp_arr.mean():.4f} ± {amp_arr.std():.4f}")
    print(f"  beta: {beta_arr.mean():.4f} ± {beta_arr.std():.4f}")

    verdict_t1 = 'PASS' if frac4 > 90 else ('CONDITIONAL' if frac4 > 70 else 'FAIL')
    print(f"  Verdict: {verdict_t1}")

    # Histogram
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    axes[0].hist(daicc_arr, bins=40, color='steelblue', alpha=0.8)
    axes[0].axvline(med, color='r', ls='--', label=f'median={med:.2f}')
    axes[0].axvline(-4,  color='k', ls=':', label='ΔAICc=-4')
    axes[0].set_xlabel('ΔAICc'); axes[0].set_title(f'Bootstrap ΔAICc (N={n_valid})')
    axes[0].legend(fontsize=8)

    axes[1].hist(amp_arr, bins=40, color='coral', alpha=0.8)
    axes[1].axvline(D_BEST['amp'], color='k', ls='--', label=f'L36={D_BEST["amp"]:.3f}')
    axes[1].set_xlabel('amp'); axes[1].set_title('Bootstrap amp')
    axes[1].legend(fontsize=8)

    axes[2].hist(beta_arr, bins=40, color='green', alpha=0.8)
    axes[2].axvline(D_BEST['beta'], color='k', ls='--', label=f'L36={D_BEST["beta"]:.3f}')
    axes[2].set_xlabel('beta'); axes[2].set_title('Bootstrap beta')
    axes[2].legend(fontsize=8)

    fig.suptitle('L38 Task 1: Bootstrap Robustness')
    fig.tight_layout()
    plot_path = os.path.join(_SCRIPT_DIR, 'l38_task1_bootstrap.png')
    fig.savefig(plot_path, dpi=130); plt.close(fig)
    print(f"  Plot: {plot_path}")

    return {
        'n_boot': N_BOOT, 'n_valid': n_valid,
        'daicc_median': med, 'daicc_lo68': lo68, 'daicc_hi68': hi68,
        'frac_below_minus4': frac4, 'frac_below_0': frac0,
        'amp_mean': float(amp_arr.mean()), 'amp_std': float(amp_arr.std()),
        'beta_mean': float(beta_arr.mean()), 'beta_std': float(beta_arr.std()),
        'verdict': verdict_t1,
    }


def task2_profile(pool):
    print("\n" + "="*60)
    print("Task 2: Profile dAICc Robustness (Om/H0 re-optimized, P2 patch)")
    print("="*60)

    n_grid    = 20
    amp_best  = D_BEST['amp']; beta_best = D_BEST['beta']
    amp_range  = np.linspace(amp_best  * 0.7, amp_best  * 1.3, n_grid)
    beta_range = np.linspace(beta_best * 0.7, beta_best * 1.3, n_grid)

    grid_points = [(a, b) for a in amp_range for b in beta_range]

    # Split into 8 chunks for workers
    chunk_size = (len(grid_points) + N_WORKERS - 1) // N_WORKERS
    chunks     = [grid_points[i:i+chunk_size] for i in range(0, len(grid_points), chunk_size)]

    t0 = time.time()
    raw = pool.map(_profile_worker, chunks)
    elapsed = time.time() - t0
    print(f"  Profile scan done in {elapsed:.1f}s")

    # Reconstruct grid
    flat = [item for batch in raw for item in batch]
    daicc_grid = np.full((n_grid, n_grid), np.nan)
    for (amp, beta, dac) in flat:
        i = int(np.argmin(np.abs(amp_range  - amp)))
        j = int(np.argmin(np.abs(beta_range - beta)))
        if 0 <= i < n_grid and 0 <= j < n_grid:
            daicc_grid[i, j] = dac

    valid = np.isfinite(daicc_grid)
    n_valid = valid.sum()
    frac6 = float(np.sum(daicc_grid[valid] < -6) / n_valid) if n_valid else 0.
    frac2 = float(np.sum(daicc_grid[valid] < -2) / n_valid) if n_valid else 0.
    best  = float(np.nanmin(daicc_grid))
    bi, bj = np.unravel_index(np.nanargmin(daicc_grid), daicc_grid.shape)

    print(f"  Best: amp={amp_range[bi]:.4f}, beta={beta_range[bj]:.4f}, dAICc={best:.2f}")
    print(f"  profile dAICc<-6: {frac6*100:.1f}%  <-2: {frac2*100:.1f}%")
    verdict_t2 = 'PASS' if frac6 > 0.30 else ('CONDITIONAL' if frac6 > 0.10 else 'FAIL')
    print(f"  Verdict: {verdict_t2}")

    # Heatmap
    fig, ax = plt.subplots(figsize=(7, 5))
    im = ax.imshow(daicc_grid, origin='lower', aspect='auto',
                   extent=[beta_range[0], beta_range[-1], amp_range[0], amp_range[-1]],
                   cmap='RdYlGn_r', vmin=-12, vmax=2)
    plt.colorbar(im, ax=ax, label='profile dAICc')
    try:
        cs = ax.contour(beta_range, amp_range, daicc_grid,
                        levels=[-8,-6,-4,-2,0], colors='k', linewidths=0.8)
        ax.clabel(cs, fmt='%d')
    except Exception: pass
    ax.axhline(amp_best,  color='cyan', ls='--', lw=1.5)
    ax.axvline(beta_best, color='cyan', ls='--', lw=1.5)
    ax.set_xlabel('beta'); ax.set_ylabel('amp')
    ax.set_title('Profile dAICc (Om/H0 re-optimized at each point)')
    fig.tight_layout()
    plot_path = os.path.join(_SCRIPT_DIR, 'l38_task2_profile.png')
    fig.savefig(plot_path, dpi=130); plt.close(fig)
    print(f"  Plot: {plot_path}")

    return {
        'frac_below_minus6': frac6, 'frac_below_minus2': frac2,
        'best_daicc': best, 'best_amp': float(amp_range[bi]), 'best_beta': float(beta_range[bj]),
        'verdict': verdict_t2,
        'amp_range': amp_range.tolist(), 'beta_range': beta_range.tolist(),
        'daicc_grid': daicc_grid.tolist(),
    }


def task3_simplification(pool):
    print("\n" + "="*60)
    print("Task 3: Model Simplification (k=2,3,4)")
    print("="*60)

    # Variants: (name, fixed_params, free_bounds, n_starts)
    variants = [
        ('D_k4',
         {},
         [(0.15,0.50),(55.,82.),(-3.0,3.0),(0.01,5.)],
         25),
        ('D_k3_betafixed',
         {'beta': D_BEST['beta']},
         [(0.15,0.50),(55.,82.),(0.01,3.)],
         20),
        ('D_k3_ampfixed',
         {'amp': D_BEST['amp']},
         [(0.15,0.50),(55.,82.),(0.01,5.)],
         20),
        ('D_k2_bothfixed',
         {'amp': D_BEST['amp'], 'beta': D_BEST['beta']},
         [(0.15,0.50),(55.,82.)],
         15),
    ]

    t0  = time.time()
    res = pool.map(_simp_worker, variants)
    print(f"  Simplification done in {time.time()-t0:.1f}s")

    print(f"\n  {'Model':<20} {'k':>3} {'ΔAICc':>8} {'wa':>8} {'verdict':<15} {'boundary'}")
    print(f"  {'-'*20} {'-'*3} {'-'*8} {'-'*8} {'-'*15} {'-'*8}")
    for r in res:
        if r.get('failed'):
            print(f"  {r['name']:<20} FAILED")
        else:
            wa_s = f"{r['wa']:.3f}" if r.get('wa') is not None else 'None'
            print(f"  {r['name']:<20} {r['k']:>3} {r['daicc']:>8.2f} {wa_s:>8} "
                  f"{r['verdict']:<15} {r['boundary']}")

    return {r['name']: r for r in res}


def task4_cpl(pool, winner_aicc=None):
    print("\n" + "="*60)
    print("Task 4: w0waCDM (CPL) Comparison")
    print("="*60)

    np.random.seed(42)
    starts = []
    for Om0 in np.linspace(0.28, 0.34, 4):
        for H0_0 in [66., 68., 70.]:
            for w0_0 in [-1.2, -1.0, -0.8]:
                for wa_0 in [-0.5, 0.0, 0.5]:
                    starts.append([Om0, H0_0, w0_0, wa_0])
    starts.append([LCDM_BEST['Om'], LCDM_BEST['H0'], -1.0, 0.0])

    t0  = time.time()
    res = pool.map(_cpl_worker, starts)
    print(f"  CPL optimization done in {time.time()-t0:.1f}s ({len(starts)} starts)")

    best_val = 1e9; best_par = None
    for (val, par) in res:
        if par is not None and val < best_val:
            best_val, best_par = val, par

    # Refine
    if best_par is not None:
        bounds = [(0.15,0.50),(55.,82.),(-2.5,0.5),(-3.,3.)]
        def obj_cpl(p):
            Om, H0, w0, wa = p
            if any(x < b[0] or x > b[1] for x, b in zip(p, bounds)): return 1e9
            E_fn = _make_E_CPL(Om, w0, wa)
            if E_fn is None: return 1e9
            cb = chi2_bao(E_fn, Om, H0); cc = chi2_cmb(E_fn, Om, H0)
            cs = chi2_sn(E_fn, Om, H0);  cr = chi2_rsd(E_fn, Om, H0)
            tot = cb+cc+cs+cr
            return tot if np.isfinite(tot) and tot < 1e7 else 1e9
        try:
            r = minimize(obj_cpl, best_par, method='Nelder-Mead',
                         options={'xatol':1e-6,'fatol':1e-6,'maxiter':3000})
            if r.fun < best_val: best_val, best_par = r.fun, r.x
        except Exception: pass

    if best_par is None:
        print("  FAILED"); return None

    Om, H0, w0, wa = best_par
    E_fn = _make_E_CPL(Om, w0, wa)
    cb, cc, cs, cr, ctot = _chi2_all(E_fn, Om, H0)
    ac_cpl   = _aicc(ctot, k=4)
    dac_lcdm = ac_cpl - LCDM_AICC
    ref_aicc  = winner_aicc if winner_aicc is not None else 1661.68
    dac_sqt   = ac_cpl - ref_aicc   # vs winner (or Model D L36)
    bnd      = _at_boundary(best_par, [(0.15,0.50),(55.,82.),(-2.5,0.5),(-3.,3.)])

    print(f"  CPL best: Om={Om:.4f}, H0={H0:.2f}, w0={w0:.4f}, wa={wa:.4f}")
    print(f"  chi2: BAO={cb:.2f} CMB={cc:.2f} SN={cs:.2f} RSD={cr:.2f}")
    print(f"  AICc={ac_cpl:.2f}  vs ΛCDM: ΔAICc={dac_lcdm:.2f}")
    winner_label = 'winner' if winner_aicc is not None else 'Model D L36'
    print(f"  vs {winner_label}: ΔAICc(CPL-winner)={dac_sqt:.2f}  ({'winner wins' if dac_sqt > 0 else 'CPL wins'})")
    print(f"  boundary: {bnd}")

    verdict_t4 = 'SQT_WINS' if dac_sqt > 0 else 'CPL_WINS'
    print(f"  Verdict: {verdict_t4}")

    return {
        'Om': float(Om), 'H0': float(H0), 'w0': float(w0), 'wa': float(wa),
        'chi2_bao': float(cb), 'chi2_cmb': float(cc), 'chi2_sn': float(cs), 'chi2_rsd': float(cr),
        'aicc': float(ac_cpl),
        'daicc_vs_lcdm': float(dac_lcdm),
        'daicc_sqt_vs_cpl': float(dac_sqt),
        'boundary': bool(bnd), 'verdict': verdict_t4,
    }


def task5_bao_k3(pool):
    print("\n" + "="*60)
    print(f"Task 5: BAO-only k=3 (beta={BETA_FIXED} fixed, P4 patch)")
    print("="*60)

    np.random.seed(42)
    starts = []
    for Om0 in np.linspace(0.28, 0.38, 5):
        for H0_0 in [65., 68., 71.]:
            for amp0 in [0.5, 1.0, 2.0, 5.0]:
                starts.append([Om0, H0_0, amp0])
    starts.append([D_BEST['Om'], D_BEST['H0'], D_BEST['amp']])

    t0  = time.time()
    res = pool.map(_bao_k3_worker, starts)
    print(f"  BAO-only k=3 done in {time.time()-t0:.1f}s ({len(starts)} starts)")

    best_val = 1e9; best_par = None
    for (val, par) in res:
        if par is not None and val < best_val:
            best_val, best_par = val, par

    # Refine
    if best_par is not None:
        bounds = [(0.15,0.50),(55.,82.),(0.5,10.0)]
        def obj_bao3(p):
            Om, H0, amp = p
            if any(x < b[0] or x > b[1] for x, b in zip(p, bounds)): return 1e9
            E_fn = _make_E_D(Om, amp, BETA_FIXED)
            if E_fn is None: return 1e9
            v = chi2_bao(E_fn, Om, H0)
            return v if (np.isfinite(v) and v < 1e7) else 1e9
        try:
            r = minimize(obj_bao3, best_par, method='Nelder-Mead',
                         options={'xatol':1e-6,'fatol':1e-6,'maxiter':2000})
            if r.fun < best_val: best_val, best_par = r.fun, r.x
        except Exception: pass

    if best_par is None:
        print("  FAILED"); return None

    Om, H0, amp = best_par
    E_fn = _make_E_D(Om, amp, BETA_FIXED)
    w0, wa = cpl_wa(E_fn, Om)
    bounds_3 = [(0.15,0.50),(55.,82.),(0.5,10.0)]
    bnd = _at_boundary(best_par, bounds_3)

    print(f"  Best: Om={Om:.4f}, H0={H0:.2f}, amp={amp:.4f} (beta={BETA_FIXED} fixed)")
    print(f"  chi2_BAO={best_val:.4f}  boundary={bnd}")
    print(f"  CPL: w0={w0:.4f}, wa={wa:.4f}" if w0 else "  CPL: None")
    reversal = (wa is not None and wa < 0)
    verdict_t5 = 'K92 INVALID' if bnd else ('CONFIRMED' if reversal else 'ANOMALY')
    print(f"  wa reversal: {reversal}  verdict: {verdict_t5}")

    return {
        'Om': float(Om), 'H0': float(H0), 'amp': float(amp), 'beta_fixed': BETA_FIXED,
        'chi2_bao': float(best_val),
        'w0': float(w0) if w0 else None, 'wa': float(wa) if wa else None,
        'boundary': bool(bnd), 'reversal': bool(reversal), 'verdict': verdict_t5,
    }


def task_V(pool):
    print("\n" + "="*60)
    print("Task V: SQT Alternative Model Discovery (Model D + V1a~V4)")
    print("="*60)

    variants = [
        ('ModelD',  'ModelD',  [(0.15,0.50),(55.,82.),(-3.0,3.0),(0.01,5.)], 25),
        ('V1a_k3',  'V1a_k3',  [(0.15,0.50),(55.,82.),(0.01,10.0)],           30),
        ('V1a_k4',  'V1a_k4',  [(0.15,0.50),(55.,82.),(0.01,10.0),(0.1,5.0)], 30),
        ('V1b',     'V1b',     [(0.15,0.50),(55.,82.),(0.1,5.0)],              30),
        ('V2prime', 'V2prime', [(0.15,0.50),(55.,82.),(0.01,200.0)],           30),
        ('V3',      'V3',      [(0.15,0.50),(55.,82.),(-3.0,3.0)],             30),
        ('V4',      'V4',      [(0.15,0.50),(55.,82.),(0.01,5.0)],             30),
    ]

    t0 = time.time()
    res = pool.map(_v_worker, variants)
    print(f"  Task V done in {time.time()-t0:.1f}s")

    print(f"\n  {'Model':<12} {'k':>3} {'ΔAICc':>8} {'w0':>8} {'wa':>8} {'H0_t':>6} {'verdict'}")
    print(f"  {'-'*65}")
    for r in res:
        if r.get('failed'):
            print(f"  {r['name']:<12} FAILED"); continue
        w0_s = f"{r['w0']:.3f}" if r.get('w0') is not None else '  ---'
        wa_s = f"{r['wa']:.3f}" if r.get('wa') is not None else '  ---'
        bnd_s = '*' if r['boundary'] else ' '
        print(f"  {r['name']:<12} {r['k']:>3} {r['daicc']:>8.2f} {w0_s:>8} {wa_s:>8}"
              f" {r['H0_tension']:>6.2f} {r['verdict']}{bnd_s}")

    return {r['name']: r for r in res}


def identify_winner(taskV_results):
    """Phase 2: select best non-boundary model from Task V."""
    print("\n" + "="*60)
    print("Phase 2: Winner Identification")
    print("="*60)

    best_name, best_aicc = None, float('inf')
    for name, res in taskV_results.items():
        if res.get('failed') or res.get('boundary'): continue
        if res['aicc'] < best_aicc:
            best_aicc, best_name = res['aicc'], name

    if best_name is None:
        print("  All models failed/boundary — fallback to Model D L36 hardcoded best")
        best_name = 'ModelD'
        best_aicc = 1661.68
        return {
            'name': 'ModelD', 'model_type': 'ModelD', 'k': 4,
            'aicc': 1661.68, 'daicc': -8.44, 'delta_vs_D': 0.0,
            'best_par': [D_BEST['Om'], D_BEST['H0'], D_BEST['amp'], D_BEST['beta']],
            'bounds': [(0.15,0.50),(55.,82.),(-3.0,3.0),(0.01,5.)],
        }

    res_w = taskV_results.get(best_name, {})
    dac   = res_w.get('daicc', float('nan'))
    dac_vs_D = best_aicc - taskV_results.get('ModelD', {}).get('aicc', 1661.68)
    print(f"  Winner: {best_name}  AICc={best_aicc:.2f}  ΔAICc(vs ΛCDM)={dac:.2f}")
    print(f"  vs Model D this run: {dac_vs_D:+.2f}")

    k = res_w.get('k', 4)
    par_dict = res_w.get('params', {})
    best_par = [par_dict.get(f'p{i}', 0.) for i in range(k)]
    bounds   = res_w.get('bounds', [])
    model_type = res_w.get('model_type', 'ModelD')

    return {
        'name': best_name, 'model_type': model_type, 'k': k,
        'aicc': float(best_aicc), 'daicc': float(dac),
        'delta_vs_D': float(dac_vs_D),
        'best_par': best_par, 'bounds': bounds,
    }


def task1_bootstrap_v(pool, winner):
    """Task 1 bootstrap for Phase 3 winner model."""
    model_type = winner['model_type']
    best_par   = winner['best_par']
    bounds_v   = winner['bounds']
    name       = winner['name']

    print("\n" + "="*60)
    print(f"Task 1: Bootstrap ({name}, N={N_BOOT})")
    print("="*60)

    Om_w, H0_w = best_par[0], best_par[1]
    E_w = _make_E_from_type(model_type, best_par)
    tv_w      = _bao_theory_vec(E_w, Om_w, H0_w)
    theory_rsd = _growth_fs8(E_w, Om_w, Z_RSD)
    theory_cmb = CMB_OBS.copy()   # chi2_cmb~0 at best-fit → theory≈obs

    if tv_w is None or theory_rsd is None:
        print("  FAILED: theory computation"); return None
    try:
        COV_BAO = np.linalg.inv(DESI_DR2_COV_INV)
    except Exception:
        print("  FAILED: BAO covariance"); return None

    rng = np.random.default_rng(42)
    boot_samples = []
    for _ in range(N_BOOT):
        new_bao = rng.multivariate_normal(tv_w, COV_BAO)
        new_cmb = theory_cmb + rng.normal(0, CMB_SIG)
        new_rsd = theory_rsd + rng.normal(0, FS8_SIG)
        boot_samples.append((best_par[:], new_bao.tolist(), new_cmb.tolist(), new_rsd.tolist()))

    batch_size = (N_BOOT + N_WORKERS - 1) // N_WORKERS
    batches = [(model_type, bounds_v, boot_samples[i:i+batch_size])
               for i in range(0, N_BOOT, batch_size)]

    t0 = time.time()
    raw = pool.map(_boot_worker_v, batches)
    print(f"  Bootstrap done in {time.time()-t0:.1f}s")

    all_da = []; all_p2 = []
    for batch_res in raw:
        for (da, p2) in batch_res:
            if np.isfinite(da) and np.isfinite(p2):
                all_da.append(da); all_p2.append(p2)

    n_valid = len(all_da)
    if n_valid == 0: print("  FAILED: no valid samples"); return None

    da_arr = np.array(all_da)
    med   = float(np.median(da_arr))
    lo68  = float(np.percentile(da_arr, 16))
    hi68  = float(np.percentile(da_arr, 84))
    frac4 = float(np.mean(da_arr < -4) * 100)
    frac0 = float(np.mean(da_arr < 0)  * 100)
    print(f"  Valid: {n_valid}/{N_BOOT}")
    print(f"  ΔAICc median={med:.2f}  68%CI=[{lo68:.2f},{hi68:.2f}]")
    print(f"  ΔAICc<-4: {frac4:.1f}%  <0: {frac0:.1f}%")
    verdict_t1 = 'PASS' if frac4 > 90 else ('CONDITIONAL' if frac4 > 70 else 'FAIL')
    print(f"  Verdict: {verdict_t1}")

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(da_arr, bins=40, color='steelblue', alpha=0.8)
    ax.axvline(med, color='r', ls='--', label=f'median={med:.2f}')
    ax.axvline(-4,  color='k', ls=':', label='ΔAICc=-4')
    ax.set_xlabel('ΔAICc'); ax.set_title(f'L38 Task 1 Bootstrap ({name}, N={n_valid})')
    ax.legend(fontsize=8); fig.tight_layout()
    plot_path = os.path.join(_SCRIPT_DIR, 'l38_task1_bootstrap.png')
    fig.savefig(plot_path, dpi=130); plt.close(fig)
    print(f"  Plot: {plot_path}")

    return {
        'winner': name, 'n_boot': N_BOOT, 'n_valid': n_valid,
        'daicc_median': med, 'daicc_lo68': lo68, 'daicc_hi68': hi68,
        'frac_below_minus4': frac4, 'frac_below_0': frac0, 'verdict': verdict_t1,
    }


def task6_residuals(winner_E_fn=None, winner_Om=None, winner_H0=None, winner_name='Model D'):
    print("\n" + "="*60)
    print(f"Task 6: Residual Analysis ({winner_name} vs LCDM)")
    print("="*60)

    E_D    = winner_E_fn if winner_E_fn else _make_E_D(D_BEST['Om'], D_BEST['amp'], D_BEST['beta'])
    Om_D   = winner_Om   if winner_Om   else D_BEST['Om']
    H0_D   = winner_H0   if winner_H0   else D_BEST['H0']
    E_LCDM = lambda z, _: E_lcdm(z, LCDM_BEST['Om'])

    # Dataset-level chi2 contributions
    cb_D, cc_D, cs_D, cr_D, _ = _chi2_all(E_D, Om_D, H0_D)
    cb_L, cc_L, cs_L, cr_L, _ = _chi2_all(E_LCDM, LCDM_BEST['Om'], LCDM_BEST['H0'])

    delta_bao = cb_D - cb_L
    delta_cmb = cc_D - cc_L
    delta_sn  = cs_D - cs_L
    delta_rsd = cr_D - cr_L
    delta_tot = delta_bao + delta_cmb + delta_sn + delta_rsd

    print(f"  ΔBAO = {delta_bao:+.4f}  (D: {cb_D:.2f} vs ΛCDM: {cb_L:.2f})")
    print(f"  ΔCMB = {delta_cmb:+.4f}  (D: {cc_D:.2f} vs ΛCDM: {cc_L:.2f})")
    print(f"  ΔSN  = {delta_sn:+.4f}   (D: {cs_D:.2f} vs ΛCDM: {cs_L:.2f})")
    print(f"  ΔRSD = {delta_rsd:+.4f}  (D: {cr_D:.2f} vs ΛCDM: {cr_L:.2f})")
    print(f"  Δtot = {delta_tot:+.4f}")

    fracs = {
        'BAO': delta_bao / delta_tot if delta_tot != 0 else 0,
        'CMB': delta_cmb / delta_tot if delta_tot != 0 else 0,
        'SN':  delta_sn  / delta_tot if delta_tot != 0 else 0,
        'RSD': delta_rsd / delta_tot if delta_tot != 0 else 0,
    }
    deltas_raw = {'BAO': delta_bao, 'CMB': delta_cmb, 'SN': delta_sn, 'RSD': delta_rsd}
    main_src = min(deltas_raw, key=deltas_raw.get)  # most negative delta = biggest improvement
    print(f"  Fractional contribution to Δchi2:")
    for k, v in fracs.items():
        print(f"    {k}: {v*100:+.1f}%")
    print(f"  Main source of improvement: {main_src}")

    # RSD point-by-point
    fs8_D    = _growth_fs8(E_D,    Om_D,            Z_RSD)
    fs8_LCDM = _growth_fs8(E_LCDM, LCDM_BEST['Om'], Z_RSD)

    print(f"\n  RSD residuals:")
    print(f"  {'z':>6} {'obs':>8} {'sig':>7} {'LCDM':>8} {'D':>8} {'ΔLCDM':>8} {'ΔD':>8}")
    if fs8_D is not None and fs8_LCDM is not None:
        for i, z in enumerate(Z_RSD):
            chi2_l = ((fs8_LCDM[i]-FS8_OBS[i])/FS8_SIG[i])**2
            chi2_d = ((fs8_D[i]   -FS8_OBS[i])/FS8_SIG[i])**2
            print(f"  {z:>6.3f} {FS8_OBS[i]:>8.3f} {FS8_SIG[i]:>7.3f} "
                  f"{fs8_LCDM[i]:>8.3f} {fs8_D[i]:>8.3f} {chi2_l:>8.3f} {chi2_d:>8.3f}")

    # BAO point residuals (marginal sigma approximation)
    sigma_bao_marg = np.sqrt(np.diag(np.linalg.inv(DESI_DR2_COV_INV)))
    tv_D    = _bao_theory_vec(E_D,    Om_D,            H0_D)
    tv_LCDM = _bao_theory_vec(E_LCDM, LCDM_BEST['Om'], LCDM_BEST['H0'])
    obs_bao = DESI_DR2['value']

    print(f"\n  BAO residuals (marginal sigma approx):")
    print(f"  {'z':>6} {'qty':>8} {'obs':>8} {'LCDM':>8} {'D':>8} {'ΔLCDM':>8} {'ΔD':>8}")
    if tv_D is not None and tv_LCDM is not None:
        for i, (z, qty) in enumerate(zip(DESI_DR2['z_eff'], DESI_DR2['quantity'])):
            chi2_l = ((obs_bao[i]-tv_LCDM[i])/sigma_bao_marg[i])**2
            chi2_d = ((obs_bao[i]-tv_D[i])    /sigma_bao_marg[i])**2
            print(f"  {z:>6.3f} {qty[:6]:>8} {obs_bao[i]:>8.4f} "
                  f"{tv_LCDM[i]:>8.4f} {tv_D[i]:>8.4f} {chi2_l:>8.3f} {chi2_d:>8.3f}")

    # Bar chart
    datasets = ['BAO', 'CMB', 'SN', 'RSD']
    deltas   = [delta_bao, delta_cmb, delta_sn, delta_rsd]
    colors   = ['steelblue' if d < 0 else 'tomato' for d in deltas]

    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(datasets, deltas, color=colors, alpha=0.8)
    ax.axhline(0, color='k', lw=1)
    for bar, val in zip(bars, deltas):
        ax.text(bar.get_x() + bar.get_width()/2, val + (0.2 if val >= 0 else -0.8),
                f'{val:+.2f}', ha='center', va='bottom', fontsize=10)
    ax.set_ylabel('Δchi2 (Model D - ΛCDM)')
    ax.set_title('L38 Task 6: chi2 improvement by dataset\n(negative = Model D wins)')
    fig.tight_layout()
    plot_path = os.path.join(_SCRIPT_DIR, 'l38_task6_residuals.png')
    fig.savefig(plot_path, dpi=130); plt.close(fig)
    print(f"\n  Plot: {plot_path}")

    return {
        'delta_bao': float(delta_bao), 'delta_cmb': float(delta_cmb),
        'delta_sn':  float(delta_sn),  'delta_rsd': float(delta_rsd),
        'delta_tot': float(delta_tot), 'fracs': {k: float(v) for k, v in fracs.items()},
        'main_source': main_src,
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def main():
    t0_total = time.time()
    print("="*60)
    print("L38: SQT Publication Verification + Alternative Model Discovery")
    print(f"8-worker parallel  |  LCDM baseline AICc={LCDM_AICC}")
    print("="*60)

    print("\nWarming up SN cache...")
    get_sn()
    print("  SN ready.")

    ctx = mp.get_context('spawn')
    results = {}

    # ── Phase 1: Model Discovery ───────────────────────────────────────────────
    results['task0'] = task0_baseline()

    with ctx.Pool(N_WORKERS) as pool:
        results['taskV'] = task_V(pool)

    # ── Phase 2: Winner Selection ──────────────────────────────────────────────
    winner = identify_winner(results['taskV'])
    results['winner'] = winner

    # ── Phase 3: Winner Validation ────────────────────────────────────────────
    winner_E_fn = _make_E_from_type(winner['model_type'], winner['best_par'])
    winner_Om   = winner['best_par'][0] if winner['best_par'] else D_BEST['Om']
    winner_H0   = winner['best_par'][1] if len(winner['best_par']) > 1 else D_BEST['H0']

    with ctx.Pool(N_WORKERS) as pool:
        results['task1'] = task1_bootstrap_v(pool, winner)
        results['task2'] = task2_profile(pool)               # Model D profile (reference)
        results['task3'] = task3_simplification(pool)        # Model D simplification
        results['task4'] = task4_cpl(pool, winner['aicc'])   # CPL vs winner
        results['task5'] = task5_bao_k3(pool)

    results['task6'] = task6_residuals(
        winner_E_fn=winner_E_fn, winner_Om=winner_Om,
        winner_H0=winner_H0, winner_name=winner['name'])

    # ── Final summary ──────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("L38 RESULTS SUMMARY")
    print("="*60)

    t0r = results.get('task0', {})
    tv_r = results.get('taskV', {})
    wr   = results.get('winner', {})
    t1r  = results.get('task1', {})
    t2r  = results.get('task2', {})
    t3r  = results.get('task3', {})
    t4r  = results.get('task4', {})
    t5r  = results.get('task5', {})
    t6r  = results.get('task6', {})

    print(f"\n[Task 0] LCDM AICc={t0r.get('aicc',0):.2f}  [{t0r.get('status','?')}]")

    print(f"\n[Task V] Model Discovery")
    for nm, r in tv_r.items():
        if r.get('failed'): print(f"  {nm}: FAILED"); continue
        bnd = '*' if r.get('boundary') else ''
        print(f"  {nm:<12} k={r['k']}  ΔAICc={r['daicc']:.2f}  [{r['verdict']}]{bnd}")

    print(f"\n[Phase 2] Winner: {wr.get('name','?')}"
          f"  AICc={wr.get('aicc',0):.2f}  ΔAICc(vs LCDM)={wr.get('daicc',0):.2f}"
          f"  vs ModelD: {wr.get('delta_vs_D',0):+.2f}")

    print(f"\n[Task 1] Bootstrap ({wr.get('name','?')})")
    if t1r:
        print(f"  median={t1r['daicc_median']:.2f}  68%CI=[{t1r['daicc_lo68']:.2f},{t1r['daicc_hi68']:.2f}]")
        print(f"  <-4: {t1r['frac_below_minus4']:.1f}%  Verdict: {t1r['verdict']}")

    print(f"\n[Task 2] Profile (Model D reference)")
    if t2r:
        print(f"  dAICc<-6: {t2r['frac_below_minus6']*100:.1f}%  Verdict: {t2r['verdict']}")

    print(f"\n[Task 3] Simplification (Model D)")
    for nm in ['D_k4','D_k3_betafixed','D_k3_ampfixed','D_k2_bothfixed']:
        r = t3r.get(nm, {})
        if r.get('failed'): print(f"  {nm}: FAILED")
        else: print(f"  {nm} (k={r.get('k','?')}): ΔAICc={r.get('daicc',0):.2f}  [{r.get('verdict','?')}]")

    print(f"\n[Task 4] vs CPL")
    if t4r:
        print(f"  CPL AICc={t4r['aicc']:.2f}  winner AICc={wr.get('aicc',0):.2f}")
        print(f"  winner vs CPL: {-t4r['daicc_sqt_vs_cpl']:.2f}  {t4r['verdict']}")

    print(f"\n[Task 5] BAO-only k=3")
    if t5r:
        print(f"  boundary={t5r['boundary']}  verdict={t5r['verdict']}")

    print(f"\n[Task 6] Residuals ({wr.get('name','?')} vs LCDM)")
    if t6r:
        print(f"  ΔBAO={t6r['delta_bao']:+.2f}  ΔCMB={t6r['delta_cmb']:+.2f}"
              f"  ΔSN={t6r['delta_sn']:+.2f}  ΔRSD={t6r['delta_rsd']:+.2f}")
        print(f"  Main source: {t6r['main_source']}")

    elapsed = time.time() - t0_total
    print(f"\nTotal elapsed: {elapsed:.1f}s")

    out_path = os.path.join(_SCRIPT_DIR, 'l38_results.json')
    with open(out_path, 'w') as f:
        json.dump(_jsonify(results), f, indent=2)
    print(f"Saved: {out_path}")


if __name__ == '__main__':
    main()
