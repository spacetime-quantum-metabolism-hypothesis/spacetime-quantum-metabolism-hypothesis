# -*- coding: utf-8 -*-
"""
l39_test.py -- L39: SQT V(psi) Prior Model Verification
=========================================================
Task 0: LCDM + Model D baseline reconfirmation
Task 1: Model G_free (k=4, A_K + A_V free)
Task 2: Model G_ratio (k=3, r free)
Task 3: Model G_theory (k=2, A_K/A_V theory-fixed)
Task 4: Bootstrap (G_theory or winner, N=300)
Task 5: CPL extraction for all G models
Task 6: Residual analysis (winner vs LCDM)
Task 7: w(z) visualization

Self-consistent E^2 solution (closed form):
  K_term = (dpsi/dz)^2 * (1+z)^2 * E^2(z)
  rho_DE = A_K * K_term + A_V * P(z)
  => E^2 * [1 - A_K * (dpsi/dz)^2 * (1+z)^2] = OR*(1+z)^4 + Om*(1+z)^3 + A_V*P(z)
  => E^2 = numerator / denominator  (closed form, no iteration)
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

LCDM_AICC  = 1670.1227
D_BEST     = {'Om': 0.3220, 'H0': 66.98, 'amp': 0.8178, 'beta': 3.533}
LCDM_BEST  = {'Om': 0.3094, 'H0': 68.41}
D_K2_DAICC = -12.46  # L38 Task 3 best: D_k2_bothfixed
N_WORKERS  = 8
N_BOOT     = 300


# ─── P1: Boundary detection ───────────────────────────────────────────────────
def _at_boundary(params, bounds, tol=1e-3):
    for p, (lo, hi) in zip(params, bounds):
        span = hi - lo
        if span == 0: continue
        if abs(p - lo) < tol*span or abs(p - hi) < tol*span:
            return True
    return False


# ─── AICc and verdict ─────────────────────────────────────────────────────────
def _aicc(chi2_val, k):
    return chi2_val + 2*k + 2*k*(k+1)/(N_TOTAL - k - 1)

def _verdict_g(daicc, boundary=False, k_theory=False):
    """Verdict for G-series models."""
    if boundary:        return 'K92 INVALID'
    if daicc >= 0:      return 'K90 KILL'
    if daicc >= -2:     return 'Q90 PASS'
    if daicc < -4 and k_theory: return 'Q92 GAME'
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


# ─── chi2_all helper ──────────────────────────────────────────────────────────
def _chi2_all(E_fn, Om, H0):
    cb = chi2_bao(E_fn, Om, H0)
    cc = chi2_cmb(E_fn, Om, H0)
    cs = chi2_sn(E_fn,  Om, H0)
    cr = chi2_rsd(E_fn, Om, H0)
    return cb, cc, cs, cr, cb+cc+cs+cr


# ─── BAO theory vector (for bootstrap) ───────────────────────────────────────
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


# ─── Model D ─────────────────────────────────────────────────────────────────
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


# ─── Model G: ψ(z) kinetic + potential energy density ────────────────────────
def _psi_and_deriv(z_arr, Om):
    """Returns OL0, alpha, psi(z), psi0, dpsi/dz."""
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0: return None, None, None, None, None
    alpha  = Om / OL0
    psi_z  = 1.0 / (1.0 + alpha * (1.0 + z_arr)**3)
    psi0   = 1.0 / (1.0 + alpha)
    dpsi   = -3.0 * alpha * (1.0 + z_arr)**2 * psi_z**2
    return OL0, alpha, psi_z, psi0, dpsi


def _E_G(z_arr, Om, A_K, A_V):
    """
    Model G: rho_DE = A_K*(dpsi/dz)^2*(1+z)^2*E^2 + A_V*(1-psi)^2

    Self-consistent closed-form solution:
      E^2 = [OR*(1+z)^4 + Om*(1+z)^3 + A_V*(1-psi)^2] / [1 - A_K*(dpsi/dz)^2*(1+z)^2]

    Denominator must be > 0 for physical solution.
    """
    OL0, alpha, psi_z, psi0, dpsi = _psi_and_deriv(z_arr, Om)
    if OL0 is None: return None

    P_term   = (1.0 - psi_z)**2
    K_coeff  = dpsi**2 * (1.0 + z_arr)**2   # multiplied by E^2

    numerator   = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + A_V * P_term
    denominator = 1.0 - A_K * K_coeff

    if np.any(denominator <= 0) or np.any(numerator <= 0):
        return None
    E2 = numerator / denominator
    if np.any(E2 <= 0) or not np.all(np.isfinite(E2)):
        return None
    return np.sqrt(E2)


def _G_normalization_check(Om, A_K, A_V, tol=1e-3):
    """Check E(z=0) = 1 to tolerance."""
    E0 = _E_G(np.array([0.0]), Om, A_K, A_V)
    if E0 is None: return False
    return abs(float(E0[0]) - 1.0) < tol


def _G_coeffs_from_ratio(Om, r):
    """
    G_ratio: A_K*K0 + A_V*P0 = OL0, with r = fraction allocated to kinetic.
    K0 = (dpsi/dz|_{z=0})^2 * 1^2 = (3*alpha/(1+alpha)^2)^2
    P0 = (1 - psi0)^2 = (alpha/(1+alpha))^2
    A_K = r * OL0 / K0
    A_V = (1-r) * OL0 / P0
    """
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0: return None, None
    alpha = Om / OL0
    psi0  = 1.0 / (1.0 + alpha)
    K0    = (3.0 * alpha / (1.0 + alpha)**2)**2
    P0    = (1.0 - psi0)**2          # = (alpha/(1+alpha))^2
    if K0 <= 0 or P0 <= 0: return None, None
    A_K = r * OL0 / K0
    A_V = (1.0 - r) * OL0 / P0
    return A_K, A_V


def _G_coeffs_theory(Om):
    """
    G_theory: A_K = 1.5 * alpha^2 * psi0^4 (SQT prior),
              A_V = (OL0 - A_K*K0) / P0
    """
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0: return None, None
    alpha = Om / OL0
    psi0  = 1.0 / (1.0 + alpha)
    K0    = (3.0 * alpha / (1.0 + alpha)**2)**2
    P0    = (1.0 - psi0)**2
    A_K   = 1.5 * alpha**2 * psi0**4
    if P0 <= 0: return None, None
    A_V   = (OL0 - A_K * K0) / P0
    return A_K, A_V


def _make_E_G_free(Om, A_K, A_V):
    def fn(z, _Om): return _E_G(z, Om, A_K, A_V)
    return fn

def _make_E_G_ratio(Om, r):
    A_K, A_V = _G_coeffs_from_ratio(Om, r)
    if A_K is None: return None
    def fn(z, _Om): return _E_G(z, Om, A_K, A_V)
    return fn

def _make_E_G_theory(Om):
    A_K, A_V = _G_coeffs_theory(Om)
    if A_K is None: return None
    def fn(z, _Om): return _E_G(z, Om, A_K, A_V)
    return fn


# ─── G model boundary check (normalization = z=0 E=1) ────────────────────────
def _G_boundary_or_invalid(Om, A_K, A_V, bounds, params):
    """Return True if boundary pinned or E(0)!=1 or A_V<=0."""
    if _at_boundary(params, bounds): return True
    if A_V <= 0: return True
    if not _G_normalization_check(Om, A_K, A_V): return True
    return False


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Workers (module-level for spawn)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _g_free_worker(start):
    """Task 1: single start for G_free (Om, H0, A_K, A_V)."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    bounds = [(0.15,0.50),(55.,82.),(0.0,10.0),(0.0,20.0)]

    def obj(p):
        Om, H0, A_K, A_V = p
        if any(x < b[0] or x > b[1] for x, b in zip(p, bounds)): return 1e9
        E_fn = _make_E_G_free(Om, A_K, A_V)
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


def _g_ratio_worker(start):
    """Task 2: single start for G_ratio (Om, H0, r)."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    bounds = [(0.15,0.50),(55.,82.),(0.0,1.0)]

    def obj(p):
        Om, H0, r = p
        if any(x < b[0] or x > b[1] for x, b in zip(p, bounds)): return 1e9
        E_fn = _make_E_G_ratio(Om, r)
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


def _g_theory_worker(start):
    """Task 3: single start for G_theory (Om, H0 only)."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    bounds = [(0.15,0.50),(55.,82.)]

    def obj(p):
        Om, H0 = p
        if Om < 0.15 or Om > 0.50 or H0 < 55 or H0 > 82: return 1e9
        E_fn = _make_E_G_theory(Om)
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


def _boot_g_worker(args):
    """Task 4: bootstrap batch for G_theory (or winner G model)."""
    mode, boot_batch = args   # mode in ('theory','ratio','free')
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    import sys
    _l35 = sys.modules.get('l35_test') or __import__('l35_test')
    orig_bao_dict = dict(_l35.DESI_DR2)
    orig_cmb = _l35.CMB_OBS.copy()
    orig_rsd = _l35.FS8_OBS.copy()

    bounds_LCDM = [(0.15,0.50),(55.,82.)]
    if mode == 'theory':
        k_g = 2
        bounds_g = [(0.15,0.50),(55.,82.)]
    elif mode == 'ratio':
        k_g = 3
        bounds_g = [(0.15,0.50),(55.,82.),(0.0,1.0)]
    else:  # free
        k_g = 4
        bounds_g = [(0.15,0.50),(55.,82.),(0.0,10.0),(0.0,20.0)]

    def obj_G(p):
        for pv, (lo, hi) in zip(p, bounds_g):
            if pv < lo or pv > hi: return 1e9
        Om, H0 = p[0], p[1]
        if mode == 'theory':
            E_fn = _make_E_G_theory(Om)
        elif mode == 'ratio':
            E_fn = _make_E_G_ratio(Om, p[2])
        else:
            E_fn = _make_E_G_free(Om, p[2], p[3])
        if E_fn is None: return 1e9
        tot = (chi2_bao(E_fn,Om,H0)+chi2_cmb(E_fn,Om,H0)+
               chi2_sn(E_fn,Om,H0) +chi2_rsd(E_fn,Om,H0))
        return tot if (np.isfinite(tot) and tot < 1e7) else 1e9

    def obj_LCDM(p):
        Om, H0 = p
        if Om<0.15 or Om>0.50 or H0<55 or H0>82: return 1e9
        E_fn = lambda z, _: E_lcdm(z, Om)
        tot = (chi2_bao(E_fn,Om,H0)+chi2_cmb(E_fn,Om,H0)+
               chi2_sn(E_fn,Om,H0) +chi2_rsd(E_fn,Om,H0))
        return tot if (np.isfinite(tot) and tot < 1e7) else 1e9

    results = []
    np.random.seed(42)
    for (s0_g, new_bao, new_cmb, new_rsd) in boot_batch:
        _l35.DESI_DR2 = {**orig_bao_dict, 'value': new_bao}
        _l35.CMB_OBS  = new_cmb
        _l35.FS8_OBS  = new_rsd

        # Fit LCDM
        best_lcdm, par_lcdm = 1e9, None
        for s in [[0.310,68.4],[0.309,68.0],[0.315,67.5]]:
            try:
                r = minimize(obj_LCDM, s, method='Nelder-Mead',
                             options={'xatol':1e-4,'fatol':1e-4,'maxiter':200})
                if r.fun < best_lcdm: best_lcdm, par_lcdm = r.fun, r.x
            except Exception: pass

        # Fit G model
        best_G, par_G = 1e9, None
        try:
            r = minimize(obj_G, s0_g, method='Nelder-Mead',
                         options={'xatol':1e-4,'fatol':1e-4,'maxiter':300})
            if r.fun < best_G: best_G, par_G = r.fun, r.x
        except Exception: pass

        if par_lcdm is None or par_G is None:
            results.append(float('nan'))
            continue

        bnd_L = _at_boundary(par_lcdm, bounds_LCDM)
        bnd_G = _at_boundary(par_G, bounds_g)
        if bnd_L or bnd_G:
            results.append(float('nan'))
        else:
            aicc_lcdm = _aicc(best_lcdm, k=2)
            aicc_G    = _aicc(best_G, k=k_g)
            results.append(float(aicc_G - aicc_lcdm))

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

    E_lcdm_fn = lambda z, _Om: E_lcdm(z, LCDM_BEST['Om'])
    cb, cc, cs, cr, ctot = _chi2_all(E_lcdm_fn, LCDM_BEST['Om'], LCDM_BEST['H0'])
    ac_lcdm = _aicc(ctot, k=2)
    print(f"  LCDM: Om={LCDM_BEST['Om']}, H0={LCDM_BEST['H0']}")
    print(f"  chi2: BAO={cb:.4f} CMB={cc:.4f} SN={cs:.4f} RSD={cr:.4f}")
    print(f"  AICc={ac_lcdm:.4f} (stored={LCDM_AICC}) [{'CONFIRMED' if abs(ac_lcdm-LCDM_AICC)<0.05 else 'CHANGED'}]")

    E_D = _make_E_D(D_BEST['Om'], D_BEST['amp'], D_BEST['beta'])
    cb2, cc2, cs2, cr2, ctot2 = _chi2_all(E_D, D_BEST['Om'], D_BEST['H0'])
    ac_D = _aicc(ctot2, k=4)
    print(f"  Model D: Om={D_BEST['Om']}, H0={D_BEST['H0']}, amp={D_BEST['amp']}, beta={D_BEST['beta']}")
    print(f"  chi2: BAO={cb2:.4f} CMB={cc2:.4f} SN={cs2:.4f} RSD={cr2:.4f}")
    print(f"  AICc={ac_D:.4f}  dAICc={ac_D-LCDM_AICC:.2f} [{'CONFIRMED' if abs(ac_D-LCDM_AICC+8.44)<0.1 else 'CHANGED'}]")

    return {
        'lcdm': {'aicc': float(ac_lcdm), 'chi2_bao': float(cb), 'chi2_cmb': float(cc),
                 'chi2_sn': float(cs), 'chi2_rsd': float(cr)},
        'modelD': {'aicc': float(ac_D), 'daicc': float(ac_D - LCDM_AICC),
                   'chi2_bao': float(cb2), 'chi2_cmb': float(cc2),
                   'chi2_sn': float(cs2), 'chi2_rsd': float(cr2)},
    }


def task1_G_free(pool):
    print("\n" + "="*60)
    print("Task 1: Model G_free (k=4, A_K + A_V free)")
    print("="*60)
    bounds = [(0.15,0.50),(55.,82.),(0.0,10.0),(0.0,20.0)]

    np.random.seed(42)
    starts = []
    for Om0 in np.linspace(0.29, 0.34, 4):
        for H0_0 in [66., 68., 70.]:
            for AK0 in [0.1, 1.0, 3.0]:
                for AV0 in [0.5, 2.0, 5.0]:
                    starts.append([Om0, H0_0, AK0, AV0])
    # Add LCDM-like starts (A_K~0, A_V~OL0/P0)
    for Om0 in [0.30, 0.32, 0.34]:
        OL0 = 1.0 - Om0 - OR
        alpha = Om0 / OL0
        P0 = (alpha/(1.0+alpha))**2
        starts.append([Om0, 67.0, 0.01, OL0/P0 if P0>0 else 2.0])
    while len(starts) < 30:
        starts.append([np.random.uniform(b[0],b[1]) for b in bounds])

    t0  = time.time()
    raw = pool.map(_g_free_worker, starts[:30])
    print(f"  G_free scan done in {time.time()-t0:.1f}s ({len(starts[:30])} starts)")

    best_val, best_par = 1e9, None
    for (val, par) in raw:
        if par is not None and val < best_val:
            best_val, best_par = val, par

    if best_par is not None:
        def obj_ref(p):
            Om, H0, A_K, A_V = p
            if any(x < b[0] or x > b[1] for x, b in zip(p, bounds)): return 1e9
            E_fn = _make_E_G_free(Om, A_K, A_V)
            if E_fn is None: return 1e9
            cb = chi2_bao(E_fn,Om,H0); cc = chi2_cmb(E_fn,Om,H0)
            cs = chi2_sn(E_fn,Om,H0);  cr = chi2_rsd(E_fn,Om,H0)
            tot = cb+cc+cs+cr
            return tot if (np.isfinite(tot) and tot < 1e7) else 1e9
        try:
            r = minimize(obj_ref, best_par, method='Nelder-Mead',
                         options={'xatol':1e-6,'fatol':1e-6,'maxiter':3000})
            if r.fun < best_val: best_val, best_par = r.fun, r.x
        except Exception: pass

    if best_par is None:
        print("  FAILED"); return None

    Om, H0, A_K, A_V = best_par
    E_fn = _make_E_G_free(Om, A_K, A_V)
    cb, cc, cs, cr, ctot = _chi2_all(E_fn, Om, H0)
    ac    = _aicc(ctot, k=4)
    dac   = ac - LCDM_AICC
    w0, wa = cpl_wa(E_fn, Om)
    bnd   = _at_boundary(best_par, bounds)
    norm_ok = _G_normalization_check(Om, A_K, A_V)
    is_invalid = bnd or not norm_ok
    verd  = _verdict_g(dac, boundary=is_invalid)

    print(f"  Best: Om={Om:.4f}, H0={H0:.2f}, A_K={A_K:.4f}, A_V={A_V:.4f}")
    print(f"  chi2: BAO={cb:.4f} CMB={cc:.4f} SN={cs:.4f} RSD={cr:.4f}")
    print(f"  AICc={ac:.4f}  dAICc={dac:.2f}")
    print(f"  E(0) norm ok: {norm_ok}  boundary: {bnd}")
    w0s = f"{w0:.4f}" if w0 else "None"; was = f"{wa:.4f}" if wa else "None"
    print(f"  CPL: w0={w0s}, wa={was}")
    print(f"  Verdict: {verd}")

    return {
        'Om': float(Om), 'H0': float(H0), 'A_K': float(A_K), 'A_V': float(A_V),
        'chi2_bao': float(cb), 'chi2_cmb': float(cc), 'chi2_sn': float(cs), 'chi2_rsd': float(cr),
        'aicc': float(ac), 'daicc': float(dac),
        'w0': float(w0) if w0 else None, 'wa': float(wa) if wa else None,
        'boundary': bool(bnd), 'norm_ok': bool(norm_ok), 'verdict': verd,
    }


def task2_G_ratio(pool):
    print("\n" + "="*60)
    print("Task 2: Model G_ratio (k=3, r free)")
    print("="*60)
    bounds = [(0.15,0.50),(55.,82.),(0.0,1.0)]

    np.random.seed(42)
    starts = []
    for Om0 in np.linspace(0.29, 0.34, 5):
        for H0_0 in [65., 67., 69., 71.]:
            for r0 in [0.05, 0.10, 0.20, 0.50, 0.80]:
                starts.append([Om0, H0_0, r0])
    while len(starts) < 30:
        starts.append([np.random.uniform(b[0],b[1]) for b in bounds])

    t0  = time.time()
    raw = pool.map(_g_ratio_worker, starts[:30])
    print(f"  G_ratio scan done in {time.time()-t0:.1f}s ({len(starts[:30])} starts)")

    best_val, best_par = 1e9, None
    for (val, par) in raw:
        if par is not None and val < best_val:
            best_val, best_par = val, par

    if best_par is not None:
        def obj_ref(p):
            Om, H0, r = p
            if any(x < b[0] or x > b[1] for x, b in zip(p, bounds)): return 1e9
            E_fn = _make_E_G_ratio(Om, r)
            if E_fn is None: return 1e9
            cb = chi2_bao(E_fn,Om,H0); cc = chi2_cmb(E_fn,Om,H0)
            cs = chi2_sn(E_fn,Om,H0);  cr = chi2_rsd(E_fn,Om,H0)
            tot = cb+cc+cs+cr
            return tot if (np.isfinite(tot) and tot < 1e7) else 1e9
        try:
            r = minimize(obj_ref, best_par, method='Nelder-Mead',
                         options={'xatol':1e-6,'fatol':1e-6,'maxiter':3000})
            if r.fun < best_val: best_val, best_par = r.fun, r.x
        except Exception: pass

    if best_par is None:
        print("  FAILED"); return None

    Om, H0, r_fit = best_par
    A_K, A_V = _G_coeffs_from_ratio(Om, r_fit)
    E_fn = _make_E_G_ratio(Om, r_fit)
    cb, cc, cs, cr, ctot = _chi2_all(E_fn, Om, H0)
    ac    = _aicc(ctot, k=3)
    dac   = ac - LCDM_AICC
    w0, wa = cpl_wa(E_fn, Om)
    bnd   = _at_boundary(best_par, bounds)
    norm_ok = _G_normalization_check(Om, A_K, A_V) if A_K is not None else False
    is_invalid = bnd or not norm_ok
    verd  = _verdict_g(dac, boundary=is_invalid)

    r_theory = 0.10
    r_dev = abs(r_fit - r_theory) / r_theory * 100

    print(f"  Best: Om={Om:.4f}, H0={H0:.2f}, r={r_fit:.4f}")
    print(f"  A_K={A_K:.4f}, A_V={A_V:.4f}")
    print(f"  r_theory={r_theory:.2f}, r_fit={r_fit:.4f}, dev={r_dev:.1f}%")
    print(f"  chi2: BAO={cb:.4f} CMB={cc:.4f} SN={cs:.4f} RSD={cr:.4f}")
    print(f"  AICc={ac:.4f}  dAICc={dac:.2f}")
    print(f"  E(0) norm ok: {norm_ok}  boundary: {bnd}")
    w0s = f"{w0:.4f}" if w0 else "None"; was = f"{wa:.4f}" if wa else "None"
    print(f"  CPL: w0={w0s}, wa={was}")
    print(f"  Verdict: {verd}")

    return {
        'Om': float(Om), 'H0': float(H0), 'r_fit': float(r_fit),
        'r_theory': r_theory, 'r_dev_pct': float(r_dev),
        'A_K': float(A_K) if A_K else None, 'A_V': float(A_V) if A_V else None,
        'chi2_bao': float(cb), 'chi2_cmb': float(cc), 'chi2_sn': float(cs), 'chi2_rsd': float(cr),
        'aicc': float(ac), 'daicc': float(dac),
        'w0': float(w0) if w0 else None, 'wa': float(wa) if wa else None,
        'boundary': bool(bnd), 'norm_ok': bool(norm_ok), 'verdict': verd,
    }


def task3_G_theory(pool):
    print("\n" + "="*60)
    print("Task 3: Model G_theory (k=2, A_K/A_V theory-fixed)  <-- CORE")
    print("="*60)
    bounds = [(0.15,0.50),(55.,82.)]

    np.random.seed(42)
    starts = []
    for Om0 in np.linspace(0.27, 0.38, 7):
        for H0_0 in [64., 66., 68., 70., 72.]:
            starts.append([Om0, H0_0])
    while len(starts) < 50:
        starts.append([np.random.uniform(0.15,0.50), np.random.uniform(55.,82.)])

    t0  = time.time()
    raw = pool.map(_g_theory_worker, starts[:50])
    print(f"  G_theory scan done in {time.time()-t0:.1f}s ({len(starts[:50])} starts)")

    best_val, best_par = 1e9, None
    for (val, par) in raw:
        if par is not None and val < best_val:
            best_val, best_par = val, par

    if best_par is not None:
        def obj_ref(p):
            Om, H0 = p
            if Om<0.15 or Om>0.50 or H0<55 or H0>82: return 1e9
            E_fn = _make_E_G_theory(Om)
            if E_fn is None: return 1e9
            cb = chi2_bao(E_fn,Om,H0); cc = chi2_cmb(E_fn,Om,H0)
            cs = chi2_sn(E_fn,Om,H0);  cr = chi2_rsd(E_fn,Om,H0)
            tot = cb+cc+cs+cr
            return tot if (np.isfinite(tot) and tot < 1e7) else 1e9
        try:
            r = minimize(obj_ref, best_par, method='Nelder-Mead',
                         options={'xatol':1e-6,'fatol':1e-6,'maxiter':3000})
            if r.fun < best_val: best_val, best_par = r.fun, r.x
        except Exception: pass

    if best_par is None:
        print("  FAILED"); return None

    Om, H0 = best_par
    A_K, A_V = _G_coeffs_theory(Om)
    E_fn = _make_E_G_theory(Om)
    cb, cc, cs, cr, ctot = _chi2_all(E_fn, Om, H0)
    ac    = _aicc(ctot, k=2)
    dac   = ac - LCDM_AICC
    dac_vs_Dk2 = dac - D_K2_DAICC  # positive = G_theory worse than D_k2
    w0, wa = cpl_wa(E_fn, Om)
    bnd   = _at_boundary(best_par, bounds)
    norm_ok = _G_normalization_check(Om, A_K, A_V) if A_K is not None else False
    is_invalid = bnd or not norm_ok
    verd  = _verdict_g(dac, boundary=is_invalid, k_theory=True)

    print(f"  Best: Om={Om:.4f}, H0={H0:.2f}")
    AK_s = f"{A_K:.6f}" if A_K is not None else "None"
    AV_s = f"{A_V:.6f}" if A_V is not None else "None"
    print(f"  A_K={AK_s} (theory-fixed), A_V={AV_s} (theory-fixed)")
    print(f"  chi2: BAO={cb:.4f} CMB={cc:.4f} SN={cs:.4f} RSD={cr:.4f}")
    print(f"  AICc={ac:.4f}  dAICc={dac:.2f}  vs D_k2: {dac_vs_Dk2:+.2f}")
    print(f"  E(0) norm ok: {norm_ok}  boundary: {bnd}")
    w0s = f"{w0:.4f}" if w0 else "None"; was = f"{wa:.4f}" if wa else "None"
    print(f"  CPL: w0={w0s}, wa={was}")
    print(f"  Verdict: {verd}")

    return {
        'Om': float(Om), 'H0': float(H0),
        'A_K': float(A_K) if A_K is not None else None,
        'A_V': float(A_V) if A_V is not None else None,
        'chi2_bao': float(cb), 'chi2_cmb': float(cc), 'chi2_sn': float(cs), 'chi2_rsd': float(cr),
        'aicc': float(ac), 'daicc': float(dac), 'daicc_vs_Dk2': float(dac_vs_Dk2),
        'w0': float(w0) if w0 else None, 'wa': float(wa) if wa else None,
        'boundary': bool(bnd), 'norm_ok': bool(norm_ok), 'verdict': verd,
    }


def task4_bootstrap(pool, winner_mode='theory', winner_par=None):
    """Bootstrap for winner G model (default: G_theory)."""
    print("\n" + "="*60)
    print(f"Task 4: Bootstrap (G_{winner_mode}, N={N_BOOT})")
    print("="*60)

    if winner_par is None:
        winner_par = [LCDM_BEST['Om'], LCDM_BEST['H0']]
    Om0 = winner_par[0]; H0_0 = winner_par[1]

    # Compute theory predictions at winner best-fit
    if winner_mode == 'theory':
        E_fn_best = _make_E_G_theory(Om0)
    elif winner_mode == 'ratio':
        r0 = winner_par[2] if len(winner_par) > 2 else 0.10
        E_fn_best = _make_E_G_ratio(Om0, r0)
    else:
        A_K0 = winner_par[2] if len(winner_par) > 2 else 0.1
        A_V0 = winner_par[3] if len(winner_par) > 3 else 2.0
        E_fn_best = _make_E_G_free(Om0, A_K0, A_V0)

    if E_fn_best is None:
        print("  FAILED: winner E_fn is None")
        return None

    tv_best = _bao_theory_vec(E_fn_best, Om0, H0_0)
    theory_rsd = _growth_fs8(E_fn_best, Om0, Z_RSD)
    theory_cmb = CMB_OBS.copy()

    if tv_best is None or theory_rsd is None:
        print("  FAILED: theory computation")
        return None

    try:
        COV_BAO = np.linalg.inv(DESI_DR2_COV_INV)
    except Exception:
        print("  FAILED: BAO covariance inversion")
        return None

    rng = np.random.default_rng(42)
    boot_samples = []
    for _ in range(N_BOOT):
        new_bao = rng.multivariate_normal(tv_best, COV_BAO)
        new_cmb = theory_cmb + rng.normal(0, CMB_SIG)
        new_rsd = theory_rsd + rng.normal(0, FS8_SIG)
        s0 = winner_par[:2] + winner_par[2:] if len(winner_par) > 2 else winner_par[:2]
        boot_samples.append((list(s0), new_bao.tolist(), new_cmb.tolist(), new_rsd.tolist()))

    batch_size = (N_BOOT + N_WORKERS - 1) // N_WORKERS
    batches = [(winner_mode, boot_samples[i:i+batch_size])
               for i in range(0, N_BOOT, batch_size)]

    t0 = time.time()
    raw = pool.map(_boot_g_worker, batches)
    print(f"  Bootstrap done in {time.time()-t0:.1f}s")

    all_daicc = [x for batch in raw for x in batch if np.isfinite(x)]
    n_valid = len(all_daicc)
    if n_valid == 0:
        print("  FAILED: no valid samples"); return None

    daicc_arr = np.array(all_daicc)
    med   = float(np.median(daicc_arr))
    lo68  = float(np.percentile(daicc_arr, 16))
    hi68  = float(np.percentile(daicc_arr, 84))
    frac4 = float(np.mean(daicc_arr < -4) * 100)
    frac0 = float(np.mean(daicc_arr < 0)  * 100)

    print(f"  Valid: {n_valid}/{N_BOOT}")
    print(f"  dAICc median={med:.2f}  68%CI=[{lo68:.2f},{hi68:.2f}]")
    print(f"  dAICc<-4: {frac4:.1f}%  <0: {frac0:.1f}%")
    verdict_t4 = 'PASS' if frac4 > 85 else ('CONDITIONAL' if frac4 > 60 else 'FAIL')
    print(f"  Verdict: {verdict_t4}")

    fig, ax = plt.subplots(figsize=(7,4))
    ax.hist(daicc_arr, bins=40, color='steelblue', alpha=0.8)
    ax.axvline(med, color='r', ls='--', label=f'median={med:.2f}')
    ax.axvline(-4,  color='k', ls=':', label='dAICc=-4')
    ax.set_xlabel('dAICc'); ax.set_title(f'L39 Bootstrap G_{winner_mode} (N={n_valid})')
    ax.legend(fontsize=9); fig.tight_layout()
    plot_path = os.path.join(_SCRIPT_DIR, 'l39_task4_bootstrap.png')
    fig.savefig(plot_path, dpi=130); plt.close(fig)
    print(f"  Plot: {plot_path}")

    return {
        'mode': winner_mode, 'n_boot': N_BOOT, 'n_valid': n_valid,
        'daicc_median': med, 'daicc_lo68': lo68, 'daicc_hi68': hi68,
        'frac_below_minus4': frac4, 'frac_below_0': frac0,
        'verdict': verdict_t4,
    }


def task5_cpl_extraction(res1, res2, res3):
    """Task 5: Summarize CPL from all G models."""
    print("\n" + "="*60)
    print("Task 5: CPL Extraction Summary")
    print("="*60)
    desi_w0, desi_wa = -0.76, -0.5

    rows = [
        ('G_free',   res1),
        ('G_ratio',  res2),
        ('G_theory', res3),
    ]
    out = {}
    print(f"  {'Model':<12} {'w0':>8} {'wa':>8} {'dir'}")
    print(f"  {'-'*40}")
    for name, r in rows:
        if r is None:
            print(f"  {name:<12}  FAILED")
            out[name] = None; continue
        w0 = r.get('w0'); wa = r.get('wa')
        w0s = f"{w0:.4f}" if w0 else "  ----"
        was = f"{wa:.4f}" if wa else "  ----"
        wa_dir = 'matched' if (wa is not None and wa < 0) else 'opposite'
        print(f"  {name:<12} {w0s:>8} {was:>8} {wa_dir}")
        out[name] = {'w0': w0, 'wa': wa, 'direction': wa_dir}

    print(f"  DESI observed:  w0={desi_w0:.2f}, wa={desi_wa:.2f}")
    return out


def task6_residuals(res3, res0):
    """Task 6: Residual analysis for G_theory vs LCDM."""
    print("\n" + "="*60)
    print("Task 6: Residual Analysis (G_theory vs LCDM)")
    print("="*60)

    if res3 is None:
        print("  SKIPPED: G_theory failed"); return None

    lcdm_bao = res0['lcdm']['chi2_bao']
    lcdm_cmb = res0['lcdm']['chi2_cmb']
    lcdm_sn  = res0['lcdm']['chi2_sn']
    lcdm_rsd = res0['lcdm']['chi2_rsd']
    lcdm_tot = lcdm_bao + lcdm_cmb + lcdm_sn + lcdm_rsd

    g_bao = res3['chi2_bao']; g_cmb = res3['chi2_cmb']
    g_sn  = res3['chi2_sn'];  g_rsd = res3['chi2_rsd']
    g_tot = g_bao + g_cmb + g_sn + g_rsd

    d_bao = lcdm_bao - g_bao
    d_cmb = lcdm_cmb - g_cmb
    d_sn  = lcdm_sn  - g_sn
    d_rsd = lcdm_rsd - g_rsd
    d_tot = lcdm_tot - g_tot

    print(f"  ΔBAO = {d_bao:+.4f}  (G: {g_bao:.2f} vs LCDM: {lcdm_bao:.2f})")
    print(f"  ΔCMB = {d_cmb:+.4f}  (G: {g_cmb:.2f} vs LCDM: {lcdm_cmb:.2f})")
    print(f"  ΔSN  = {d_sn:+.4f}  (G: {g_sn:.2f} vs LCDM: {lcdm_sn:.2f})")
    print(f"  ΔRSD = {d_rsd:+.4f}  (G: {g_rsd:.2f} vs LCDM: {lcdm_rsd:.2f})")
    print(f"  Δtot = {d_tot:+.4f}")
    if abs(d_tot) > 0:
        print(f"  Fractional contributions:")
        for name, dv in [('BAO',d_bao),('CMB',d_cmb),('SN',d_sn),('RSD',d_rsd)]:
            print(f"    {name}: {dv/d_tot*100:+.1f}%")
    main = max([('BAO',d_bao),('CMB',d_cmb),('SN',d_sn),('RSD',d_rsd)], key=lambda x: x[1])
    print(f"  Main source of improvement: {main[0]}")

    return {
        'delta_bao': float(d_bao), 'delta_cmb': float(d_cmb),
        'delta_sn': float(d_sn),   'delta_rsd': float(d_rsd),
        'delta_total': float(d_tot), 'main_source': main[0],
    }


def task7_wz_plot(res1, res2, res3):
    """Task 7: w(z) visualization for all G models + Model D + LCDM."""
    print("\n" + "="*60)
    print("Task 7: w(z) Visualization")
    print("="*60)

    z_arr = np.linspace(0.01, 2.0, 200)
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.axhline(-1.0, color='k', ls='--', lw=1.5, label='LCDM (w=-1)')

    E_D_fn = _make_E_D(D_BEST['Om'], D_BEST['amp'], D_BEST['beta'])
    try:
        w_D = []
        for zi in z_arr:
            dz = 1e-4
            E1 = E_D_fn(np.array([zi]),      None)[0]
            E2 = E_D_fn(np.array([zi+dz]),   None)[0]
            E0 = E_D_fn(np.array([max(zi-dz,0.001)]), None)[0]
            OL0 = 1.0 - D_BEST['Om'] - OR
            rde1 = E1**2 - OR*(1+zi)**4 - D_BEST['Om']*(1+zi)**3
            rde2 = E2**2 - OR*(1+zi+dz)**4 - D_BEST['Om']*(1+zi+dz)**3
            dlnrde = (np.log(max(rde2,1e-30)) - np.log(max(rde1,1e-30))) / dz
            w_D.append(-1 - dlnrde * (1+zi) / 3.0)
        ax.plot(z_arr, w_D, 'b-', lw=2, label=f'Model D (dAICc=-8.44)')
    except Exception: pass

    def plot_G(E_fn, Om, label, color, ls):
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
                dlnrde = (np.log(rde2) - np.log(rde1)) / dz
                w_arr.append(-1 - dlnrde * (1+zi) / 3.0)
            except Exception: w_arr.append(np.nan)
        ax.plot(z_arr, w_arr, color=color, ls=ls, lw=2, label=label)

    if res1:
        E_fn = _make_E_G_free(res1['Om'], res1['A_K'], res1['A_V'])
        plot_G(E_fn, res1['Om'], f"G_free (dAICc={res1['daicc']:.2f})", 'green', '-')
    if res2:
        E_fn = _make_E_G_ratio(res2['Om'], res2['r_fit'])
        plot_G(E_fn, res2['Om'], f"G_ratio (dAICc={res2['daicc']:.2f})", 'orange', '-')
    if res3:
        E_fn = _make_E_G_theory(res3['Om'])
        plot_G(E_fn, res3['Om'], f"G_theory/k=2 (dAICc={res3['daicc']:.2f})", 'red', '-')

    ax.set_xlabel('z'); ax.set_ylabel('w(z)')
    ax.set_xlim(0, 2); ax.set_ylim(-3, 1)
    ax.set_title('L39: w(z) comparison (G models vs Model D vs LCDM)')
    ax.legend(fontsize=9); ax.grid(alpha=0.3)
    fig.tight_layout()
    plot_path = os.path.join(_SCRIPT_DIR, 'l39_task7_wz.png')
    fig.savefig(plot_path, dpi=130); plt.close(fig)
    print(f"  Plot: {plot_path}")
    return {'plot': plot_path}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    print("="*60)
    print("L39: SQT V(psi) Prior Model Verification")
    print(f"8-worker parallel  |  LCDM baseline AICc={LCDM_AICC}")
    print("="*60)

    print("\nWarming up SN cache...")
    get_sn(); print("  SN ready.")

    t_total = time.time()
    results = {}
    ctx = mp.get_context('spawn')

    results['task0'] = task0_baseline()

    with ctx.Pool(N_WORKERS) as pool:
        results['task1'] = task1_G_free(pool)
        results['task2'] = task2_G_ratio(pool)
        results['task3'] = task3_G_theory(pool)

    # Identify best G model for bootstrap
    # Priority: G_theory (k=2, cleanest), then G_ratio, then G_free
    winner_mode = 'theory'
    winner_par  = [results['task3']['Om'], results['task3']['H0']] if results['task3'] else None

    if winner_par is None and results['task2']:
        winner_mode = 'ratio'
        winner_par = [results['task2']['Om'], results['task2']['H0'], results['task2']['r_fit']]
    if winner_par is None and results['task1']:
        winner_mode = 'free'
        winner_par = [results['task1']['Om'], results['task1']['H0'],
                      results['task1']['A_K'], results['task1']['A_V']]

    with ctx.Pool(N_WORKERS) as pool:
        if winner_par is not None:
            results['task4'] = task4_bootstrap(pool, winner_mode, winner_par)
        else:
            results['task4'] = None
            print("\nTask 4: SKIPPED (no winner)")

    results['task5'] = task5_cpl_extraction(results['task1'], results['task2'], results['task3'])
    results['task6'] = task6_residuals(results['task3'], results['task0'])
    results['task7'] = task7_wz_plot(results['task1'], results['task2'], results['task3'])

    # ─── Final Summary ────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("L39 RESULTS SUMMARY")
    print("="*60)

    r0 = results['task0']
    print(f"\n[Task 0] Baselines")
    print(f"  LCDM: AICc={r0['lcdm']['aicc']:.2f}")
    print(f"  Model D: AICc={r0['modelD']['aicc']:.2f}  dAICc={r0['modelD']['daicc']:.2f}")

    for tag, name, r in [('task1','G_free',results['task1']),
                          ('task2','G_ratio',results['task2']),
                          ('task3','G_theory',results['task3'])]:
        task_num = {'task1':'1','task2':'2','task3':'3'}[tag]
        print(f"\n[Task {task_num}] Model {name}")
        if r is None: print("  FAILED"); continue
        print(f"  Om={r['Om']:.4f}, H0={r['H0']:.2f}")
        if name == 'G_ratio': print(f"  r_fit={r['r_fit']:.4f} (theory=0.10, dev={r['r_dev_pct']:.1f}%)")
        if name in ('G_free','G_ratio'): print(f"  A_K={r.get('A_K',0):.4f}, A_V={r.get('A_V',0):.4f}")
        if name == 'G_theory': print(f"  A_K={r.get('A_K'):.6f} (fixed), A_V={r.get('A_V'):.4f} (fixed)")
        print(f"  AICc={r['aicc']:.2f}  dAICc={r['daicc']:.2f}  [{r['verdict']}]")
        if name == 'G_theory': print(f"  vs D_k2: {r.get('daicc_vs_Dk2',0):+.2f}")

    r4 = results['task4']
    print(f"\n[Task 4] Bootstrap (G_{winner_mode}, N={N_BOOT})")
    if r4:
        print(f"  median={r4['daicc_median']:.2f}  68%CI=[{r4['daicc_lo68']:.2f},{r4['daicc_hi68']:.2f}]")
        print(f"  dAICc<-4: {r4['frac_below_minus4']:.1f}%  Verdict: {r4['verdict']}")
    else:
        print("  FAILED/SKIPPED")

    r5 = results['task5']
    print(f"\n[Task 5] CPL Extraction")
    for nm in ['G_free','G_ratio','G_theory']:
        if r5 and r5.get(nm):
            w0 = r5[nm].get('w0'); wa = r5[nm].get('wa')
            print(f"  {nm}: w0={w0:.4f if w0 else 'None'}, wa={wa:.4f if wa else 'None'}  [{r5[nm].get('direction','?')}]")

    r6 = results['task6']
    if r6:
        print(f"\n[Task 6] Residuals (G_theory vs LCDM)")
        print(f"  ΔBAO={r6['delta_bao']:+.2f}  ΔCMB={r6['delta_cmb']:+.2f}  ΔSN={r6['delta_sn']:+.2f}  ΔRSD={r6['delta_rsd']:+.2f}")
        print(f"  Main source: {r6['main_source']}")

    # ─── Final verdict ────────────────────────────────────────────────────────
    r3 = results['task3']
    print(f"\n[Final Verdict]")
    if r3 and r3['verdict'] == 'Q92 GAME':
        print(f"  G_theory (k=2) dAICc={r3['daicc']:.2f}: Q92 GAME")
        print(f"  Strategy A: SQT prior WINS -> paper with theory derivation")
    elif r3 and r3['daicc'] < -2:
        print(f"  G_theory (k=2) dAICc={r3['daicc']:.2f}: {r3['verdict']}")
        print(f"  Strategy B: G models competitive but not decisive -> report both")
    else:
        dac_s = f"{r3['daicc']:.2f}" if r3 else "N/A"
        print(f"  G_theory (k=2) dAICc={dac_s}: FAIL/WEAK")
        print(f"  Strategy C: Model D phenomenological confirmed -> paper as is")

    elapsed = time.time() - t_total
    print(f"\nTotal elapsed: {elapsed:.1f}s")

    out_path = os.path.join(_SCRIPT_DIR, 'l39_results.json')
    with open(out_path, 'w') as f:
        json.dump(_jsonify(results), f, indent=2)
    print(f"Saved: {out_path}")


if __name__ == '__main__':
    main()
