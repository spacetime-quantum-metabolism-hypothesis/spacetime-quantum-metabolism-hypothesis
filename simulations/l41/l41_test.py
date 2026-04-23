# -*- coding: utf-8 -*-
"""
l41_test.py -- L41: Brans-Dicke form SQT verification
=======================================================
Lagrangian: L = sqrt(-g)[(A+B*psi)R + 0.5*(dpsi)^2 - V(psi) + L_m]
V(psi) = 0.5*mu^2*(psi-1)^2   (GL expansion at psi=1)

Modified FRW equations (homogeneous psi(t)):
  3*(A+B*psi)*H^2 = rho_m+rho_r + 0.5*psi_dot^2 + V - 3*B*H*psi_dot      [F1]
  (A+B*psi)*(2*Hdot+3*H^2) = -(p_m+p_r) + 0.5*psi_dot^2 - V
                               - B*(psi_ddot+2*H*psi_dot)                   [F2]
  psi_ddot + 3*H*psi_dot + V'(psi) = B*R,   R=6*(Hdot+2*H^2)              [S]

ODE in N=ln(a): y=[psi, chi=dpsi/dN]
  E^2 algebraic from [F1]
  alpha=E'/E from combined [F2]+[S]   (eliminates chi'' -- closed 2D ODE)
  chi' from [S]

Models:
  BD      k=4: Om,H0,B_A=B/A,m2=mu^2/H0^2  (full)
  BD_min  k=3: Om,H0,B_A                    (m2=0, massless BD)
  BD_mo   k=3: Om,H0,m2                     (B_A=0, GR+quintessence)
  BD_thy  k=2: Om,H0                        (B_A=1 fixed, m2=400 theory)

Tasks 0-8, 8-worker spawn pool, 4-person code review x2 before execution.
"""

import os, sys, time, json, warnings
import numpy as np
from scipy.integrate import solve_ivp, cumulative_trapezoid
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
    OR, C_KMS, N_TOTAL,
    cpl_wa,
    Z_RSD, FS8_OBS, FS8_SIG,
    CMB_OBS, CMB_SIG,
    _base as _base35,
    R_S, N_GRID,
    DESI_DR2, DESI_DR2_COV_INV,
)

# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────
LCDM_AICC   = 1670.1227
D_BEST      = {'Om': 0.3220, 'H0': 66.98, 'amp': 0.8178, 'beta': 3.533}
LCDM_BEST   = {'Om': 0.3094, 'H0': 68.41}
D_AICC      = 1661.68
N_WORKERS   = 8
N_BOOT      = 300

BD_A             = 1.0    # A normalized to 1
BD_THEORY_BA     = 1.0    # SQT natural: B/A = 1
BD_THEORY_M2     = 400.0  # mu = 20*H0 estimate from L39 potential analysis

# BD ODE initial conditions: matter-era attractor (z=1000)
BD_N_INI   = -np.log(1.0 + 1000.0)   # ≈ -6.908
BD_PSI_INI = 1.0                       # tracker at psi=1 in matter era
BD_CHI_INI = 0.0                       # psi' -> 0 in matter era


# ──────────────────────────────────────────────────────────────────────────────
# General helpers
# ──────────────────────────────────────────────────────────────────────────────
def _at_boundary(params, bounds, tol=1e-3):
    for p, (lo, hi) in zip(params, bounds):
        span = hi - lo
        if span == 0:
            continue
        if abs(p - lo) < tol * span or abs(p - hi) < tol * span:
            return True
    return False


def _aicc(chi2_val, k):
    return chi2_val + 2*k + 2*k*(k+1) / (N_TOTAL - k - 1)


def _verdict(daicc, boundary=False, k2=False):
    if boundary:     return 'K92 INVALID'
    if daicc >= 0:   return 'K90 KILL'
    if daicc >= -2:  return 'Q90 PASS'
    if daicc < -4 and k2: return 'Q92 GAME'
    return 'Q91 STRONG'


def _jsonify(obj):
    if isinstance(obj, dict):        return {k: _jsonify(v) for k, v in obj.items()}
    if isinstance(obj, list):        return [_jsonify(v) for v in obj]
    if isinstance(obj, np.ndarray):  return _jsonify(obj.tolist())
    if isinstance(obj, bool):        return bool(obj)
    if isinstance(obj, np.integer):  return int(obj)
    if isinstance(obj, (np.floating, float)):
        f = float(obj)
        return None if not np.isfinite(f) else f
    return obj


def _chi2_all(E_fn, Om, H0):
    cb = chi2_bao(E_fn, Om, H0)
    cc = chi2_cmb(E_fn, Om, H0)
    cs = chi2_sn(E_fn, Om, H0)
    cr = chi2_rsd(E_fn, Om, H0)
    return cb, cc, cs, cr, cb + cc + cs + cr


def _bao_theory_vec(E_fn, Om, H0):
    """Compute BAO theory vector for bootstrap datasets."""
    z_eff  = DESI_DR2['z_eff']
    z_grid = np.linspace(0.0, z_eff.max() + 0.01, N_GRID)
    Eg     = E_fn(z_grid, Om)
    if Eg is None or not np.all(np.isfinite(Eg)):
        return None
    Eg  = np.maximum(Eg, 1e-15)
    DM  = (C_KMS / H0) * np.concatenate([[0.],
           cumulative_trapezoid(1.0 / Eg, z_grid)])
    tv  = np.empty(13)
    for i, (z, qty) in enumerate(zip(z_eff, DESI_DR2['quantity'])):
        idx = min(np.searchsorted(z_grid, z), N_GRID - 1)
        DH  = C_KMS / (H0 * Eg[idx])
        DV  = (z * DM[idx]**2 * DH)**(1./3.) if z > 0 else 0.
        if   'DV' in qty: tv[i] = DV / R_S
        elif 'DM' in qty: tv[i] = DM[idx] / R_S
        elif 'DH' in qty: tv[i] = DH / R_S
        else:              tv[i] = np.nan
    return None if not np.all(np.isfinite(tv)) else tv


# ──────────────────────────────────────────────────────────────────────────────
# BD ODE physics
# ──────────────────────────────────────────────────────────────────────────────
def _bd_ode(N, y, Om, B, m2):
    """
    Brans-Dicke FRW ODE in N = ln(a).
    State y = [psi, chi] where chi = dpsi/dN.

    Derivation:
      [F1] / H0^2 (normalized by 3H0^2 so rho->(rho/3H0^2)):
        (A+B*psi)*E^2 = Om*exp(-3N) + OR*exp(-4N) + chi^2*E^2/6
                        + m2*(psi-1)^2/6 - B*E^2*chi
      -> E^2 = [Om*exp(-3N) + OR*exp(-4N) + m2*(psi-1)^2/6]
               / [(A+B*psi) + B*chi - chi^2/6]               [algebraic]

      alpha = E'/E from combined [F2]+[S] after substituting chi' from [S]:
        num_a = -OR*exp(-4N) - m2*(psi-1)^2/2 + B*m2*(psi-1)
                + E^2*(chi^2/2 + B*chi - 12*B^2 - 3*(A+B*psi))
        den_a = E^2*(2*(A+B*psi) + 6*B^2)
        alpha = num_a / den_a

      chi' from [S]:
        chi' = (6B-chi)*alpha + 12B - 3chi - m2*(psi-1)/E^2
    """
    A   = BD_A
    psi = y[0]
    chi = y[1]

    emN3   = np.exp(-3.0 * N)
    emN4   = np.exp(-4.0 * N)
    ApBpsi = A + B * psi

    # --- E^2 from [F1] ---
    denom_f1 = ApBpsi + B * chi - chi**2 / 6.0
    numer_f1 = Om * emN3 + OR * emN4 + m2 * (psi - 1.0)**2 / 6.0

    if denom_f1 < 1e-10 or numer_f1 < 0.0:
        return [0.0, 0.0]

    E2 = numer_f1 / denom_f1
    if E2 < 1e-20:
        return [0.0, 0.0]

    # --- alpha = E'/E from [F2]+[S] ---
    numer_a = (-OR * emN4
               - 0.5 * m2 * (psi - 1.0)**2
               + B * m2 * (psi - 1.0)
               + E2 * (0.5 * chi**2 + B * chi - 12.0 * B**2 - 3.0 * ApBpsi))
    denom_a = E2 * (2.0 * ApBpsi + 6.0 * B**2)

    if abs(denom_a) < 1e-20:
        return [0.0, 0.0]

    alpha = numer_a / denom_a

    # --- chi' from [S] ---
    chi_p = (6.0 * B - chi) * alpha + 12.0 * B - 3.0 * chi - m2 * (psi - 1.0) / E2

    return [chi, chi_p]


def _make_E_BD(Om, B, m2):
    """
    Integrate BD ODE once; return E_fn(z, Om) closure or None.
    ODE: N_ini=-6.908 -> N_end=0, psi_ini=1, chi_ini=0.
    E^2 computed algebraically at each grid point.
    Normalized: E(z=0) = 1 (absorbs A-renormalization).
    """
    A = BD_A
    N_eval = np.linspace(BD_N_INI, 0.0, 2000)

    try:
        sol = solve_ivp(
            _bd_ode,
            [BD_N_INI, 0.0],
            [BD_PSI_INI, BD_CHI_INI],
            t_eval=N_eval,
            args=(Om, B, m2),
            method='RK45',
            rtol=1e-7, atol=1e-9,
            max_step=0.05,
            dense_output=False,
        )
    except Exception:
        return None

    if not sol.success:
        return None

    psi_v = sol.y[0]
    chi_v = sol.y[1]
    N_v   = sol.t

    # Algebraic E^2 at each grid point
    emN3   = np.exp(-3.0 * N_v)
    emN4   = np.exp(-4.0 * N_v)
    ApBpsi = A + B * psi_v
    d_f1   = ApBpsi + B * chi_v - chi_v**2 / 6.0
    n_f1   = Om * emN3 + OR * emN4 + m2 * (psi_v - 1.0)**2 / 6.0

    if np.any(d_f1 <= 0) or np.any(n_f1 <= 0) or np.any(~np.isfinite(n_f1)):
        return None

    E2_v = n_f1 / d_f1
    if np.any(E2_v <= 0) or np.any(~np.isfinite(E2_v)):
        return None

    # Normalize E(z=0)=1; N_v[-1] = 0 (today)
    E2_today = E2_v[-1]
    if E2_today <= 0:
        return None
    E_v = np.sqrt(E2_v / E2_today)

    # Map N -> z, sort ascending in z
    z_v   = np.exp(-N_v) - 1.0   # from ~1000 down to 0
    idx   = np.argsort(z_v)
    z_s   = z_v[idx]
    E_s   = E_v[idx]

    ifn = interp1d(z_s, E_s, kind='linear', bounds_error=False, fill_value=np.nan)

    def fn(z, _Om):
        za = np.atleast_1d(np.asarray(z, dtype=float))
        Ev = ifn(za)
        return None if (np.any(np.isnan(Ev)) or np.any(Ev <= 0)) else Ev

    return fn


def _get_psi_chi_profile(Om, B, m2, z_out):
    """Return (psi(z), chi(z)) at z_out for Task 7 analysis. None on failure."""
    N_eval = np.linspace(BD_N_INI, 0.0, 2000)
    try:
        sol = solve_ivp(
            _bd_ode, [BD_N_INI, 0.0], [BD_PSI_INI, BD_CHI_INI],
            t_eval=N_eval, args=(Om, B, m2),
            method='RK45', rtol=1e-7, atol=1e-9, max_step=0.05,
        )
    except Exception:
        return None, None
    if not sol.success:
        return None, None

    z_v   = np.exp(-sol.t) - 1.0
    psi_v = sol.y[0]
    chi_v = sol.y[1]
    idx   = np.argsort(z_v)
    z_s   = z_v[idx]; psi_s = psi_v[idx]; chi_s = chi_v[idx]

    i_psi = interp1d(z_s, psi_s, kind='linear', bounds_error=False, fill_value=np.nan)
    i_chi = interp1d(z_s, chi_s, kind='linear', bounds_error=False, fill_value=np.nan)
    return i_psi(z_out), i_chi(z_out)


# ──────────────────────────────────────────────────────────────────────────────
# Model D reference
# ──────────────────────────────────────────────────────────────────────────────
def _E_D(z_arr, Om, amp, beta):
    OL0, ratio, _ = _base35(z_arr, Om)
    if OL0 is None:
        return None
    rde = OL0 * (1.0 + amp * (ratio - 1.0) * np.exp(-abs(beta) * z_arr))
    E2  = OR * (1+z_arr)**4 + Om * (1+z_arr)**3 + rde
    return None if np.any(E2 <= 0) else np.sqrt(E2)


def _make_E_D(Om, amp, beta):
    def fn(z, _Om): return _E_D(z, Om, amp, beta)
    return fn


# ──────────────────────────────────────────────────────────────────────────────
# Workers  (each imports everything it needs — spawn pool safety)
# ──────────────────────────────────────────────────────────────────────────────

# Bounds for each model
_BOUNDS_BD4  = [(0.20, 0.55), (55., 82.), (-2.0, 2.0), (0.0, 2000.0)]
_BOUNDS_MIN  = [(0.20, 0.55), (55., 82.), (-2.0, 2.0)]
_BOUNDS_MO   = [(0.20, 0.55), (55., 82.), (0.0, 2000.0)]
_BOUNDS_THY  = [(0.20, 0.55), (55., 82.)]
_BOUNDS_LCDM = [(0.20, 0.55), (55., 82.)]


def _bd_k4_worker(start):
    """BD k=4 (Om,H0,B_A,m2) single start."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')

    def obj(p):
        Om, H0, B_A, m2 = p
        if (Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82
                or B_A < -2 or B_A > 2 or m2 < 0 or m2 > 2000):
            return 1e9
        B = B_A * BD_A
        fn = _make_E_BD(Om, B, m2)
        if fn is None:
            return 1e9
        cb = chi2_bao(fn, Om, H0); cc = chi2_cmb(fn, Om, H0)
        cs = chi2_sn(fn, Om, H0);  cr = chi2_rsd(fn, Om, H0)
        tot = cb + cc + cs + cr
        return tot if (np.isfinite(tot) and tot < 1e7) else 1e9

    try:
        r = minimize(obj, start, method='Nelder-Mead',
                     options={'xatol': 1e-4, 'fatol': 1e-4, 'maxiter': 800})
        return (float(r.fun), [float(x) for x in r.x])
    except Exception:
        return (1e9, None)


def _bd_min_worker(start):
    """BD_min k=3 (Om,H0,B_A), m2=0."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')

    def obj(p):
        Om, H0, B_A = p
        if (Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82
                or B_A < -2 or B_A > 2):
            return 1e9
        B = B_A * BD_A
        fn = _make_E_BD(Om, B, 0.0)
        if fn is None:
            return 1e9
        cb = chi2_bao(fn, Om, H0); cc = chi2_cmb(fn, Om, H0)
        cs = chi2_sn(fn, Om, H0);  cr = chi2_rsd(fn, Om, H0)
        tot = cb + cc + cs + cr
        return tot if (np.isfinite(tot) and tot < 1e7) else 1e9

    try:
        r = minimize(obj, start, method='Nelder-Mead',
                     options={'xatol': 1e-4, 'fatol': 1e-4, 'maxiter': 800})
        return (float(r.fun), [float(x) for x in r.x])
    except Exception:
        return (1e9, None)


def _bd_mo_worker(start):
    """BD_massiveonly k=3 (Om,H0,m2), B_A=0."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')

    def obj(p):
        Om, H0, m2 = p
        if (Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82
                or m2 < 0 or m2 > 2000):
            return 1e9
        fn = _make_E_BD(Om, 0.0, m2)
        if fn is None:
            return 1e9
        cb = chi2_bao(fn, Om, H0); cc = chi2_cmb(fn, Om, H0)
        cs = chi2_sn(fn, Om, H0);  cr = chi2_rsd(fn, Om, H0)
        tot = cb + cc + cs + cr
        return tot if (np.isfinite(tot) and tot < 1e7) else 1e9

    try:
        r = minimize(obj, start, method='Nelder-Mead',
                     options={'xatol': 1e-4, 'fatol': 1e-4, 'maxiter': 800})
        return (float(r.fun), [float(x) for x in r.x])
    except Exception:
        return (1e9, None)


def _bd_thy_worker(start):
    """BD_theory k=2 (Om,H0), B_A=1 fixed, m2=400 fixed."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')

    def obj(p):
        Om, H0 = p
        if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
            return 1e9
        B  = BD_THEORY_BA * BD_A
        m2 = BD_THEORY_M2
        fn = _make_E_BD(Om, B, m2)
        if fn is None:
            return 1e9
        cb = chi2_bao(fn, Om, H0); cc = chi2_cmb(fn, Om, H0)
        cs = chi2_sn(fn, Om, H0);  cr = chi2_rsd(fn, Om, H0)
        tot = cb + cc + cs + cr
        return tot if (np.isfinite(tot) and tot < 1e7) else 1e9

    try:
        r = minimize(obj, start, method='Nelder-Mead',
                     options={'xatol': 1e-4, 'fatol': 1e-4, 'maxiter': 600})
        return (float(r.fun), [float(x) for x in r.x])
    except Exception:
        return (1e9, None)


def _boot_bd_worker(args):
    """
    Bootstrap batch: fit BD_winner + LCDM on each perturbed dataset.
    args = list of (s0_bd, new_bao_vals, new_cmb, new_rsd, bd_params_fixed)
    bd_params_fixed = (B, m2, k_winner)
    """
    boot_batch = args
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    import sys
    _l35 = sys.modules.get('l35_test') or __import__('l35_test')
    orig_bao = dict(_l35.DESI_DR2)
    orig_cmb = _l35.CMB_OBS.copy()
    orig_rsd = _l35.FS8_OBS.copy()

    results = []
    np.random.seed(42)
    for item in boot_batch:
        s0_bd, new_bao, new_cmb, new_rsd, B_fixed, m2_fixed, k_win = item

        _l35.DESI_DR2 = {**orig_bao, 'value': new_bao}
        _l35.CMB_OBS  = new_cmb
        _l35.FS8_OBS  = new_rsd

        # Fit BD winner (Om, H0 free; B, m2 fixed at winner values)
        def obj_bd(p):
            Om, H0 = p
            if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
                return 1e9
            fn = _make_E_BD(Om, B_fixed, m2_fixed)
            if fn is None:
                return 1e9
            tot = (chi2_bao(fn,Om,H0)+chi2_cmb(fn,Om,H0)+
                   chi2_sn(fn,Om,H0)+chi2_rsd(fn,Om,H0))
            return tot if (np.isfinite(tot) and tot < 1e7) else 1e9

        # Fit LCDM
        def obj_lcdm(p):
            Om, H0 = p
            if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
                return 1e9
            fn = lambda z, _: E_lcdm(z, Om)
            tot = (chi2_bao(fn,Om,H0)+chi2_cmb(fn,Om,H0)+
                   chi2_sn(fn,Om,H0)+chi2_rsd(fn,Om,H0))
            return tot if (np.isfinite(tot) and tot < 1e7) else 1e9

        best_bd, par_bd = 1e9, None
        try:
            r = minimize(obj_bd, s0_bd, method='Nelder-Mead',
                         options={'xatol': 1e-4, 'fatol': 1e-4, 'maxiter': 300})
            if r.fun < best_bd:
                best_bd, par_bd = r.fun, r.x
        except Exception:
            pass

        best_lcdm, par_lcdm = 1e9, None
        for s in [[0.310, 68.4], [0.309, 68.0], [0.315, 67.5]]:
            try:
                r = minimize(obj_lcdm, s, method='Nelder-Mead',
                             options={'xatol': 1e-4, 'fatol': 1e-4, 'maxiter': 200})
                if r.fun < best_lcdm:
                    best_lcdm, par_lcdm = r.fun, r.x
            except Exception:
                pass

        if par_bd is None or par_lcdm is None:
            results.append(float('nan'))
            continue

        bnd_bd   = _at_boundary(par_bd,   _BOUNDS_LCDM)
        bnd_lcdm = _at_boundary(par_lcdm, _BOUNDS_LCDM)
        if bnd_bd or bnd_lcdm:
            results.append(float('nan'))
        else:
            aicc_bd   = _aicc(best_bd,   k=k_win)
            aicc_lcdm = _aicc(best_lcdm, k=2)
            results.append(float(aicc_bd - aicc_lcdm))

    _l35.DESI_DR2 = orig_bao
    _l35.CMB_OBS  = orig_cmb
    _l35.FS8_OBS  = orig_rsd
    return results


# ──────────────────────────────────────────────────────────────────────────────
# Task 0: Baseline
# ──────────────────────────────────────────────────────────────────────────────
def task0_baseline():
    print("\n" + "=" * 60)
    print("Task 0: Baseline Verification (LCDM + Model D)")
    print("=" * 60)

    E_lcdm_fn = lambda z, _: E_lcdm(z, LCDM_BEST['Om'])
    cb, cc, cs, cr, ctot = _chi2_all(E_lcdm_fn, LCDM_BEST['Om'], LCDM_BEST['H0'])
    ac_l = _aicc(ctot, k=2)
    print(f"  LCDM: Om={LCDM_BEST['Om']}, H0={LCDM_BEST['H0']}")
    print(f"  chi2: BAO={cb:.4f} CMB={cc:.4f} SN={cs:.4f} RSD={cr:.4f}")
    ok = 'CONFIRMED' if abs(ac_l - LCDM_AICC) < 0.05 else 'CHANGED'
    print(f"  AICc={ac_l:.4f} (stored={LCDM_AICC}) [{ok}]")

    E_D = _make_E_D(D_BEST['Om'], D_BEST['amp'], D_BEST['beta'])
    cb2, cc2, cs2, cr2, ct2 = _chi2_all(E_D, D_BEST['Om'], D_BEST['H0'])
    ac_D = _aicc(ct2, k=4)
    ok2 = 'CONFIRMED' if abs(ac_D - D_AICC) < 0.1 else 'CHANGED'
    print(f"  Model D: Om={D_BEST['Om']}, H0={D_BEST['H0']}")
    print(f"  chi2: BAO={cb2:.4f} CMB={cc2:.4f} SN={cs2:.4f} RSD={cr2:.4f}")
    print(f"  AICc={ac_D:.4f}  dAICc={ac_D - LCDM_AICC:.2f} [{ok2}]")

    return {'lcdm_aicc': ac_l, 'd_aicc': ac_D}


# ──────────────────────────────────────────────────────────────────────────────
# Tasks 1-4: BD model fits (parallel pool)
# ──────────────────────────────────────────────────────────────────────────────
def _run_bd_models(pool):
    """Dispatch all BD model starts to pool, collect results."""
    t0 = time.time()

    rng = np.random.default_rng(42)

    # Starts for each model
    starts_bd4 = []
    for _ in range(30):
        Om = rng.uniform(0.22, 0.45)
        H0 = rng.uniform(60, 78)
        BA = rng.uniform(-0.5, 0.5)
        m2 = rng.uniform(0, 500)
        starts_bd4.append([Om, H0, BA, m2])
    # Add LCDM-like start
    starts_bd4.append([0.31, 68.0, 0.0, 0.0])
    starts_bd4.append([0.31, 68.0, 0.1, 10.0])
    starts_bd4.append([0.31, 68.0,-0.1, 10.0])

    starts_min = []
    for _ in range(25):
        Om = rng.uniform(0.22, 0.45)
        H0 = rng.uniform(60, 78)
        BA = rng.uniform(-1.0, 1.0)
        starts_min.append([Om, H0, BA])
    starts_min.append([0.31, 68.0, 0.0])
    starts_min.append([0.31, 68.0, 0.1])

    starts_mo = []
    for _ in range(25):
        Om = rng.uniform(0.22, 0.45)
        H0 = rng.uniform(60, 78)
        m2 = rng.uniform(0, 800)
        starts_mo.append([Om, H0, m2])
    starts_mo.append([0.31, 68.0,   0.0])
    starts_mo.append([0.31, 68.0, 100.0])
    starts_mo.append([0.31, 68.0, 400.0])

    starts_thy = []
    for _ in range(45):
        Om = rng.uniform(0.25, 0.45)
        H0 = rng.uniform(60, 78)
        starts_thy.append([Om, H0])
    starts_thy.append([0.31, 68.0])
    starts_thy.append([0.32, 67.0])
    starts_thy.append([0.30, 69.0])
    starts_thy.append([0.33, 66.0])
    starts_thy.append([0.28, 70.0])

    print("\n" + "=" * 60)
    print("Tasks 1-4: BD model fits (parallel pool)")
    print("=" * 60)
    print(f"  BD k=4: {len(starts_bd4)} starts")
    print(f"  BD_min k=3: {len(starts_min)} starts")
    print(f"  BD_mo k=3: {len(starts_mo)} starts")
    print(f"  BD_thy k=2: {len(starts_thy)} starts")
    sys.stdout.flush()

    res_bd4 = pool.map(_bd_k4_worker, starts_bd4)
    res_min = pool.map(_bd_min_worker, starts_min)
    res_mo  = pool.map(_bd_mo_worker,  starts_mo)
    res_thy = pool.map(_bd_thy_worker, starts_thy)

    elapsed = time.time() - t0
    print(f"  All BD scans done in {elapsed:.1f}s")
    sys.stdout.flush()

    def best_of(res):
        valid = [(chi2, p) for chi2, p in res if p is not None and chi2 < 1e8]
        if not valid:
            return 1e9, None
        return min(valid, key=lambda x: x[0])

    return {
        'bd4': best_of(res_bd4),
        'min': best_of(res_min),
        'mo':  best_of(res_mo),
        'thy': best_of(res_thy),
        'elapsed': elapsed,
    }


def report_bd_model(tag, label, k, params_names, best_chi2, best_params,
                    bounds, lcdm_aicc=LCDM_AICC, d_aicc=D_AICC):
    """Print standardized BD model result block."""
    print(f"\n{'=' * 60}")
    print(f"Task: {label} (k={k})")
    print(f"{'=' * 60}")
    if best_params is None:
        print("  FAILED: no valid result")
        return None, None, None, None, None, None

    aicc = _aicc(best_chi2, k)
    daicc = aicc - lcdm_aicc
    bnd = _at_boundary(best_params, bounds[:len(best_params)])
    vdict = _verdict(daicc, boundary=bnd, k2=(k == 2))

    for name, val in zip(params_names, best_params):
        print(f"  {name}={val:.4f}", end="  ")
    print()

    # Build E_fn
    if tag == 'bd4':
        Om, H0, B_A, m2 = best_params
        B = B_A * BD_A
    elif tag == 'min':
        Om, H0, B_A = best_params
        B = B_A * BD_A; m2 = 0.0
    elif tag == 'mo':
        Om, H0, m2 = best_params
        B = 0.0
    elif tag == 'thy':
        Om, H0 = best_params
        B = BD_THEORY_BA * BD_A; m2 = BD_THEORY_M2
    else:
        return None, None, None, None, None, None

    E_fn = _make_E_BD(Om, B, m2)
    if E_fn is not None:
        cb, cc, cs, cr, ct = _chi2_all(E_fn, Om, H0)
        print(f"  chi2: BAO={cb:.4f} CMB={cc:.4f} SN={cs:.4f} RSD={cr:.4f}")
        w0, wa = (None, None)
        try:
            w0, wa = cpl_wa(E_fn, Om)
        except Exception:
            pass
    else:
        ct = best_chi2; w0, wa = None, None

    print(f"  AICc={aicc:.4f}  dAICc={daicc:.2f}  vs D: {aicc - d_aicc:+.2f}")
    print(f"  boundary={bnd}")
    if w0 is not None:
        print(f"  CPL: w0={w0:.4f}, wa={wa:.4f}")
    print(f"  Verdict: {vdict}")
    sys.stdout.flush()

    return aicc, daicc, bnd, w0, wa, (Om, H0, B, m2)


# ──────────────────────────────────────────────────────────────────────────────
# Task 5: Bootstrap
# ──────────────────────────────────────────────────────────────────────────────
def task5_bootstrap(pool, winner_tag, winner_params, winner_k):
    print("\n" + "=" * 60)
    print(f"Task 5: Bootstrap ({winner_tag}, N={N_BOOT})")
    print("=" * 60)
    t0 = time.time()

    Om_w, H0_w, B_w, m2_w = winner_params

    # Build perturbed datasets from nominal theory vectors
    E_fn_nom = _make_E_BD(Om_w, B_w, m2_w)
    if E_fn_nom is None:
        print("  SKIPPED: winner E_fn invalid")
        return None

    bao_nom = _bao_theory_vec(E_fn_nom, Om_w, H0_w)
    lcdm_fn = lambda z, _: E_lcdm(z, LCDM_BEST['Om'])
    bao_nom_lcdm = _bao_theory_vec(lcdm_fn, LCDM_BEST['Om'], LCDM_BEST['H0'])
    if bao_nom is None or bao_nom_lcdm is None:
        print("  SKIPPED: BAO theory vector failed")
        return None

    rng = np.random.default_rng(99)
    bao_cov  = np.linalg.inv(DESI_DR2_COV_INV)
    bao_L    = np.linalg.cholesky(bao_cov)
    cmb_sig  = CMB_SIG
    rsd_sig  = FS8_SIG

    boot_items = []
    for _ in range(N_BOOT):
        nb = bao_nom_lcdm + bao_L @ rng.standard_normal(13)
        nc = CMB_OBS + cmb_sig * rng.standard_normal(len(CMB_OBS))
        nr = FS8_OBS + rsd_sig * rng.standard_normal(len(FS8_OBS))
        s0 = [Om_w + rng.normal(0, 0.01), H0_w + rng.normal(0, 0.5)]
        boot_items.append((s0, nb, nc, nr, B_w, m2_w, winner_k))

    batch_size = max(1, N_BOOT // N_WORKERS)
    batches = [boot_items[i:i+batch_size] for i in range(0, N_BOOT, batch_size)]
    raw = pool.map(_boot_bd_worker, batches)
    all_daicc = []
    for batch_res in raw:
        all_daicc.extend(batch_res)

    vals = np.array([v for v in all_daicc if v is not None and np.isfinite(v)])
    elapsed = time.time() - t0
    print(f"  Bootstrap done in {elapsed:.1f}s")
    print(f"  Valid: {len(vals)}/{N_BOOT}")
    if len(vals) == 0:
        print("  Verdict: FAIL (no valid samples)")
        return {'valid': 0, 'verdict': 'FAIL'}

    med  = float(np.median(vals))
    lo   = float(np.percentile(vals, 16))
    hi   = float(np.percentile(vals, 84))
    p_lt4 = float(np.mean(vals < -4))
    p_lt0 = float(np.mean(vals < 0))
    verd  = 'PASS' if p_lt4 >= 0.90 else 'FAIL'
    print(f"  dAICc median={med:.2f}  68%CI=[{lo:.2f},{hi:.2f}]")
    print(f"  dAICc<-4: {p_lt4*100:.1f}%  <0: {p_lt0*100:.1f}%")
    print(f"  Verdict: {verd}")
    sys.stdout.flush()
    return {'valid': int(len(vals)), 'median': med, 'ci68': [lo, hi],
            'frac_lt4': p_lt4, 'frac_lt0': p_lt0, 'verdict': verd}


# ──────────────────────────────────────────────────────────────────────────────
# Task 6: CPL summary
# ──────────────────────────────────────────────────────────────────────────────
def task6_cpl(results_map):
    print("\n" + "=" * 60)
    print("Task 6: CPL Extraction Summary")
    print("=" * 60)
    print(f"  {'Model':<18} {'w0':>8} {'wa':>8}  direction")
    print("  " + "-" * 50)
    for tag, label in [('bd4','BD k=4'),('min','BD_min k=3'),
                        ('mo','BD_mo k=3'),('thy','BD_thy k=2')]:
        r = results_map.get(tag, {})
        w0 = r.get('w0'); wa = r.get('wa')
        if w0 is None or wa is None:
            print(f"  {label:<18} {'None':>8} {'None':>8}  ?")
        else:
            desi_w0, desi_wa = -0.757, -0.83
            dir_w0 = 'same' if (w0 - (-1)) * (desi_w0 - (-1)) > 0 else 'opp'
            dir_wa = 'same' if wa * desi_wa > 0 else 'opp'
            direction = 'same' if dir_wa == 'same' else 'opposite'
            print(f"  {label:<18} {w0:>8.4f} {wa:>8.4f}  {direction}")
    print(f"  {'DESI observed':<18} {-0.757:>8.3f} {-0.83:>8.2f}")
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 7: Residuals
# ──────────────────────────────────────────────────────────────────────────────
def task7_residuals(best_tag, best_params):
    print("\n" + "=" * 60)
    print(f"Task 7: Residual Analysis ({best_tag} vs LCDM)")
    print("=" * 60)

    Om_b, H0_b, B_b, m2_b = best_params
    E_bd = _make_E_BD(Om_b, B_b, m2_b)
    E_lc = lambda z, _: E_lcdm(z, LCDM_BEST['Om'])

    if E_bd is None:
        print("  SKIPPED: E_BD invalid")
        return

    def safe_chi2(fn, Om, H0):
        return (chi2_bao(fn,Om,H0), chi2_cmb(fn,Om,H0),
                chi2_sn(fn,Om,H0), chi2_rsd(fn,Om,H0))

    cb_b,cc_b,cs_b,cr_b = safe_chi2(E_bd, Om_b, H0_b)
    cb_l,cc_l,cs_l,cr_l = safe_chi2(E_lc, LCDM_BEST['Om'], LCDM_BEST['H0'])

    dBAO = cb_l - cb_b; dCMB = cc_l - cc_b
    dSN  = cs_l - cs_b; dRSD = cr_l - cr_b
    dtot = dBAO + dCMB + dSN + dRSD

    print(f"  dBAO = {dBAO:+.4f}  (BD: {cb_b:.2f} vs LCDM: {cb_l:.2f})")
    print(f"  dCMB = {dCMB:+.4f}  (BD: {cc_b:.2f} vs LCDM: {cc_l:.2f})")
    print(f"  dSN  = {dSN:+.4f}  (BD: {cs_b:.2f} vs LCDM: {cs_l:.2f})")
    print(f"  dRSD = {dRSD:+.4f}  (BD: {cr_b:.2f} vs LCDM: {cr_l:.2f})")
    print(f"  dtot = {dtot:+.4f}")
    if abs(dtot) > 1e-6:
        print(f"  BAO: {dBAO/dtot*100:+.1f}%  CMB: {dCMB/dtot*100:+.1f}%"
              f"  SN: {dSN/dtot*100:+.1f}%  RSD: {dRSD/dtot*100:+.1f}%")
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 8: Model D vs BD comparison (psi profile)
# ──────────────────────────────────────────────────────────────────────────────
def task8_comparison(best_tag, best_params, d_aicc_val):
    print("\n" + "=" * 60)
    print("Task 8: Model D vs BD Comparison (psi profile)")
    print("=" * 60)

    Om_b, H0_b, B_b, m2_b = best_params
    z_out = np.array([0.0, 0.1, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0])

    psi_z, chi_z = _get_psi_chi_profile(Om_b, B_b, m2_b, z_out)
    if psi_z is None:
        print("  SKIPPED: psi profile failed")
        return

    # BD effective coupling ratio: (A+B*psi(z))/(A+B*psi(0))
    A = BD_A; B = B_b
    ApBpsi0 = A + B * psi_z[0]
    ratio_bd = (A + B * psi_z) / ApBpsi0

    # Model D g(z) = 1 + amp*(psi0/psi_z - 1)*exp(-beta*z)
    OL0_D = 1.0 - D_BEST['Om'] - OR
    alpha_D = D_BEST['Om'] / OL0_D
    psi0_D  = 1.0 / (1.0 + alpha_D)
    psi_D   = 1.0 / (1.0 + alpha_D * (1.0 + z_out)**3)
    ratio_D = psi0_D / psi_D
    modD_factor = 1.0 + D_BEST['amp'] * (ratio_D - 1.0) * np.exp(-D_BEST['beta'] * z_out)

    print(f"  BD best: Om={Om_b:.4f}, H0={H0_b:.4f}, B={B_b:.4f}, m2={m2_b:.2f}")
    print(f"  {'z':>5}  {'(A+Bpsi)/(A+Bpsi0)':>22}  {'Model D factor':>16}  {'diff':>8}")
    for i, z in enumerate(z_out):
        diff = ratio_bd[i] - modD_factor[i]
        print(f"  {z:5.1f}  {ratio_bd[i]:>22.6f}  {modD_factor[i]:>16.6f}  {diff:>8.4f}")

    rms = np.sqrt(np.mean((ratio_bd - modD_factor)**2))
    print(f"  RMS deviation BD vs D-factor: {rms:.4f}")
    approx = 'YES' if rms < 0.05 else 'NO'
    print(f"  Model D is BD approximation: {approx}")
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 9: w(z) visualization
# ──────────────────────────────────────────────────────────────────────────────
def task9_wz_plot(results_map, out_dir):
    z_plot = np.linspace(0.01, 2.0, 300)
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = {'bd4': 'C0', 'min': 'C1', 'mo': 'C2', 'thy': 'C3', 'lcdm': 'k', 'd': 'C4'}
    labels = {'bd4': 'BD k=4', 'min': 'BD_min k=3', 'mo': 'BD_mo k=3',
              'thy': 'BD_thy k=2', 'lcdm': 'LCDM', 'd': 'Model D'}

    # LCDM: w=-1
    ax.axhline(-1.0, color='k', ls='--', lw=1, label='LCDM (w=-1)')

    # Model D
    E_D = _make_E_D(D_BEST['Om'], D_BEST['amp'], D_BEST['beta'])
    try:
        w0_D, wa_D = cpl_wa(E_D, D_BEST['Om'])
        w_D = w0_D + wa_D * z_plot / (1.0 + z_plot)
        ax.plot(z_plot, w_D, color='C4', ls='-.', lw=1.5, label=f"Model D (w0={w0_D:.2f},wa={wa_D:.2f})")
    except Exception:
        pass

    for tag in ['bd4', 'min', 'mo', 'thy']:
        r = results_map.get(tag, {})
        p = r.get('params'); w0 = r.get('w0'); wa = r.get('wa')
        if p is None or w0 is None:
            continue
        w_z = w0 + wa * z_plot / (1.0 + z_plot)
        ax.plot(z_plot, w_z, color=colors[tag], lw=1.5,
                label=f"{labels[tag]} (w0={w0:.2f},wa={wa:.2f})")

    ax.axhline(-0.757, color='gray', ls=':', lw=1, alpha=0.7, label='DESI w0=-0.757')
    ax.set_xlabel('z'); ax.set_ylabel('w(z)')
    ax.set_title('L41: BD SQT models vs LCDM/Model D')
    ax.legend(fontsize=7, loc='best')
    ax.set_ylim(-3.0, 1.0)
    ax.grid(alpha=0.3)
    out = os.path.join(out_dir, 'l41_task9_wz.png')
    fig.savefig(out, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f"  Plot: {out}")
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────
def main():
    t_total = time.time()
    out_dir  = _SCRIPT_DIR

    print("=" * 60)
    print("L41: Brans-Dicke SQT Verification")
    print(f"8-worker parallel  |  LCDM baseline AICc={LCDM_AICC}")
    print("=" * 60)
    print("\nWarming up SN cache...")
    get_sn()
    print("  SN ready.")
    sys.stdout.flush()

    # Task 0
    r0 = task0_baseline()

    # Tasks 1-4 (parallel)
    ctx = mp.get_context('spawn')
    with ctx.Pool(N_WORKERS) as pool:
        bd_raw = _run_bd_models(pool)

        # Parse results
        res = {}

        def parse(tag, label, k, param_names, bounds_key):
            best_chi2, best_p = bd_raw[tag]
            bounds = {'bd4': _BOUNDS_BD4, 'min': _BOUNDS_MIN,
                      'mo': _BOUNDS_MO, 'thy': _BOUNDS_THY}[bounds_key]
            aicc, daicc, bnd, w0, wa, phys = report_bd_model(
                tag, label, k, param_names, best_chi2, best_p, bounds)
            res[tag] = {
                'aicc': aicc, 'daicc': daicc, 'boundary': bnd,
                'w0': w0, 'wa': wa, 'params': phys,
                'raw_params': best_p, 'chi2': best_chi2
            }

        parse('bd4', 'BD (k=4, full)',        4,
              ['Om','H0','B/A','m2'], 'bd4')
        parse('min', 'BD_min (k=3, massless)', 3,
              ['Om','H0','B/A'],      'min')
        parse('mo',  'BD_mo (k=3, pot-only)',  3,
              ['Om','H0','m2'],       'mo')
        parse('thy', 'BD_theory (k=2, core)',  2,
              ['Om','H0'],            'thy')

        # Find best performer
        def _safe_daicc(r):
            d = r.get('daicc')
            return d if d is not None else 1e9

        best_tag = min(res, key=lambda t: _safe_daicc(res[t]))
        best_daicc = _safe_daicc(res[best_tag])
        best_k = {'bd4': 4, 'min': 3, 'mo': 3, 'thy': 2}[best_tag]

        print(f"\n  Winner: {best_tag}  dAICc={best_daicc:.2f}")
        sys.stdout.flush()

        # Task 5: Bootstrap (only if best has dAICc < 100, else skip)
        r5 = None
        bp = res[best_tag].get('params')
        if bp is not None and best_daicc < 100:
            r5 = task5_bootstrap(pool, best_tag, bp, best_k)
        else:
            print("\n" + "=" * 60)
            print("Task 5: Bootstrap -- SKIPPED (all models K90 KILL)")
            print("=" * 60)

    # Task 6: CPL
    task6_cpl(res)

    # Task 7: Residuals (best model)
    if res[best_tag].get('params') is not None:
        task7_residuals(best_tag, res[best_tag]['params'])

    # Task 8: Comparison
    if res[best_tag].get('params') is not None:
        task8_comparison(best_tag, res[best_tag]['params'], D_AICC)

    # Task 9: w(z) plot
    print("\n" + "=" * 60)
    print("Task 9: w(z) Visualization")
    print("=" * 60)
    task9_wz_plot(res, out_dir)

    # Summary
    elapsed = time.time() - t_total
    print("\n" + "=" * 60)
    print("L41 RESULTS SUMMARY")
    print("=" * 60)
    print(f"\n[Task 0] Baselines")
    print(f"  LCDM: AICc={r0.get('lcdm_aicc',LCDM_AICC):.2f}")
    print(f"  Model D: AICc={r0.get('d_aicc',D_AICC):.2f}  dAICc={r0.get('d_aicc',D_AICC)-LCDM_AICC:.2f}")

    tag_labels = {'bd4': 'BD k=4', 'min': 'BD_min k=3', 'mo': 'BD_mo k=3', 'thy': 'BD_theory k=2'}
    task_nums  = {'bd4': 1, 'min': 2, 'mo': 3, 'thy': 4}
    for tag in ['bd4', 'min', 'mo', 'thy']:
        r = res[tag]
        tn = task_nums[tag]
        print(f"\n[Task {tn}] {tag_labels[tag]}")
        if r.get('raw_params') is not None:
            p = r['raw_params']
            if tag == 'bd4':   print(f"  Om={p[0]:.4f}, H0={p[1]:.4f}, B/A={p[2]:.4f}, m2={p[3]:.2f}")
            elif tag == 'min': print(f"  Om={p[0]:.4f}, H0={p[1]:.4f}, B/A={p[2]:.4f}")
            elif tag == 'mo':  print(f"  Om={p[0]:.4f}, H0={p[1]:.4f}, m2={p[2]:.2f}")
            elif tag == 'thy': print(f"  Om={p[0]:.4f}, H0={p[1]:.4f} (B/A=1 fixed, m2=400 fixed)")
        aicc = r.get('aicc'); daicc = r.get('daicc')
        if aicc is not None:
            bnd_str = '  [boundary]' if r.get('boundary') else ''
            v = _verdict(daicc, r.get('boundary', False), k2=(tag == 'thy'))
            print(f"  AICc={aicc:.2f}  dAICc={daicc:.2f}{bnd_str}  [{v}]")

    if r5:
        print(f"\n[Task 5] Bootstrap ({best_tag}, N={N_BOOT})")
        print(f"  valid={r5.get('valid',0)}")
        if r5.get('median') is not None:
            print(f"  median={r5['median']:.2f}  68%CI=[{r5['ci68'][0]:.2f},{r5['ci68'][1]:.2f}]")
            print(f"  dAICc<-4: {r5['frac_lt4']*100:.1f}%  Verdict: {r5['verdict']}")

    print(f"\n[Final Verdict]")
    d_thy = _safe_daicc(res['thy']); d_bd4 = _safe_daicc(res['bd4'])
    v_thy = _verdict(d_thy, res['thy'].get('boundary', False), k2=True)
    v_bd4 = _verdict(d_bd4, res['bd4'].get('boundary', False))
    print(f"  BD_theory (k=2) dAICc={d_thy:.2f}: {v_thy}")
    print(f"  BD (k=4)        dAICc={d_bd4:.2f}: {v_bd4}")

    if d_thy < -4 and not res['thy'].get('boundary', True):
        print("  Strategy A: BD_theory SUCCESS -> SQT complete a priori victory")
    elif d_bd4 < -2 and not res['bd4'].get('boundary', True):
        print("  Strategy B: BD k=4 success, BD_theory partial -> partial a priori")
    else:
        print("  Strategy C: All BD FAIL -> BD-form SQT axiom refuted")
        print("              -> Model D remains phenomenological; axiom revision needed")

    print(f"\nTotal elapsed: {elapsed:.1f}s")
    out_json = os.path.join(out_dir, 'l41_results.json')
    save_data = {'r0': _jsonify(r0), 'models': _jsonify(res),
                 'bootstrap': _jsonify(r5), 'elapsed': elapsed}
    with open(out_json, 'w') as f:
        json.dump(save_data, f, indent=2)
    print(f"Saved: {out_json}")
    sys.stdout.flush()


if __name__ == '__main__':
    main()
