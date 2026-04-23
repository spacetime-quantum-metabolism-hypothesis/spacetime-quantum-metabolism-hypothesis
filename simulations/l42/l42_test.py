# -*- coding: utf-8 -*-
"""
l42_test.py -- L42: Model HE (A2'-modified axiom) verification
================================================================
A2': Gamma_gen = kappa * H(z) * (rho_max - rho_st)
Modified equilibrium: psi*(z) = 1/(1 + alpha_H*(1+z)^3/E(z))
                     alpha_H = Om/OL0 (prior-fixed, k=2) or free (k=3)

Self-consistent E(z): psi*(z) depends on E(z), E^2 depends on rho_DE(psi*)
Solved by fixed-point iteration (max 30 iter, tol=1e-8).
Non-convergence -> K92 INVALID.

Models:
  HE_S    k=2: Om,H0                  (alpha_H=Om/OL0 fixed, pure prior)
  HE_Sf   k=3: Om,H0,alpha_H          (alpha_H free)
  HE_D    k=4: Om,H0,amp,beta         (H-modified ratio in Model D form)
  HE_BD   k=4: Om,H0,B_A,m2          (BD ODE + A2' equilibrium IC+V)

Tasks 0-9, 8-worker spawn pool, 4-person code review x2 before execution.
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
N_BOOT      = 200

BD_A    = 1.0
BD_N_INI = -np.log(1001.0)   # z_ini = 1000

# Precompute grid: dense at low z (data), extended to z=1200 (CMB last-scattering, growth ODE)
HE_Z_GRID = np.concatenate([
    np.linspace(0.0, 3.5, 2000),
    np.linspace(3.5, 1200.0, 600)[1:],
])

# Bounds
_BOUNDS_HE_S  = [(0.20, 0.55), (55., 82.)]
_BOUNDS_HE_SF = [(0.20, 0.55), (55., 82.), (0.01, 5.0)]
_BOUNDS_HE_D  = [(0.20, 0.55), (55., 82.), (-5., 5.), (0., 20.)]
_BOUNDS_HE_BD = [(0.20, 0.55), (55., 82.), (-2., 2.), (0., 2000.)]
_BOUNDS_LCDM  = [(0.20, 0.55), (55., 82.)]

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
    if boundary:          return 'K92 INVALID'
    if daicc >= 0:        return 'K90 KILL'
    if daicc >= -2:       return 'Q90 PASS'
    if daicc < -4 and k2: return 'Q92 GAME'
    return 'Q91 STRONG'

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

def _safe_daicc(r):
    d = r.get('daicc')
    return d if d is not None else 1e9

def _chi2_all(E_fn, Om, H0):
    cb = chi2_bao(E_fn, Om, H0)
    cc = chi2_cmb(E_fn, Om, H0)
    cs = chi2_sn(E_fn, Om, H0)
    cr = chi2_rsd(E_fn, Om, H0)
    return cb, cc, cs, cr, cb + cc + cs + cr

def _bao_theory_vec(E_fn, Om, H0):
    z_eff  = DESI_DR2['z_eff']
    z_grid = np.linspace(0.0, z_eff.max() + 0.01, N_GRID)
    Eg = E_fn(z_grid, Om)
    if Eg is None or not np.all(np.isfinite(Eg)):
        return None
    Eg = np.maximum(Eg, 1e-15)
    DM = (C_KMS / H0) * np.concatenate([[0.],
           cumulative_trapezoid(1.0 / Eg, z_grid)])
    tv = np.empty(13)
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
# HE_S: A2' self-consistent equilibrium
#   psi*(z) = 1/(1 + alpha_H*(1+z)^3/E(z))
#   rho_DE(z) = OL0 * psi*(z)/psi*(0)
#   psi*(0) = 1/(1+alpha_H)  [E(0)=1 by construction]
# ──────────────────────────────────────────────────────────────────────────────
def _solve_E_HE_S(z_arr, Om, alpha_H):
    """Self-consistent E(z) for A2' equilibrium. Returns None on non-convergence."""
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0 or alpha_H <= 0:
        return None
    psi_0  = 1.0 / (1.0 + alpha_H)   # E(0)=1 maintained through iterations
    E_prev = np.sqrt(np.maximum(Om*(1+z_arr)**3 + OR*(1+z_arr)**4 + OL0, 1e-30))

    for _ in range(30):
        psi_z  = 1.0 / (1.0 + alpha_H * (1+z_arr)**3 / E_prev)
        rho_DE = OL0 * psi_z / psi_0
        E2_new = Om*(1+z_arr)**3 + OR*(1+z_arr)**4 + rho_DE
        if np.any(E2_new <= 0) or np.any(~np.isfinite(E2_new)):
            return None
        E_new = np.sqrt(E2_new)
        if np.max(np.abs(E_new - E_prev)) < 1e-8:
            return E_new
        E_prev = E_new
    return None  # K92: non-convergent

def _make_E_HE_S(Om, alpha_H=None):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    if alpha_H is None:
        alpha_H = Om / OL0
    # Precompute self-consistent E(z) once on dense grid, then interpolate.
    # This avoids re-running the 30-iteration solver on every chi2_sn call.
    E_arr = _solve_E_HE_S(HE_Z_GRID, Om, alpha_H)
    if E_arr is None:
        return None
    ifn = interp1d(HE_Z_GRID, E_arr, kind='linear', bounds_error=False, fill_value=np.nan)
    def fn(z, _Om):
        za = np.atleast_1d(np.asarray(z, float))
        Ev = ifn(za)
        return None if (np.any(np.isnan(Ev)) or np.any(Ev <= 0)) else Ev
    return fn

# ──────────────────────────────────────────────────────────────────────────────
# HE_D: A2' ratio in Model D form
#   ratio_H(z) = psi*(0)/psi*(z)  with A2' psi*
#   rho_DE(z) = OL0*(1 + amp*(ratio_H - 1)*exp(-|beta|*z))
# ──────────────────────────────────────────────────────────────────────────────
def _solve_E_HE_D(z_arr, Om, alpha_H, amp, beta):
    """Self-consistent E(z) for HE_D model."""
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0 or alpha_H <= 0:
        return None
    psi_0  = 1.0 / (1.0 + alpha_H)
    E_prev = np.sqrt(np.maximum(Om*(1+z_arr)**3 + OR*(1+z_arr)**4 + OL0, 1e-30))
    beta_a = abs(beta)

    for _ in range(30):
        psi_z   = 1.0 / (1.0 + alpha_H * (1+z_arr)**3 / E_prev)
        ratio_H = psi_0 / psi_z
        rho_DE  = OL0 * (1.0 + amp * (ratio_H - 1.0) * np.exp(-beta_a * z_arr))
        E2_new  = Om*(1+z_arr)**3 + OR*(1+z_arr)**4 + rho_DE
        if np.any(E2_new <= 0) or np.any(~np.isfinite(E2_new)):
            return None
        E_new = np.sqrt(E2_new)
        if np.max(np.abs(E_new - E_prev)) < 1e-8:
            return E_new
        E_prev = E_new
    return None

def _make_E_HE_D(Om, alpha_H, amp, beta):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0 or alpha_H <= 0:
        return None
    # Precompute once on dense grid to avoid re-solving in every chi2 call.
    E_arr = _solve_E_HE_D(HE_Z_GRID, Om, alpha_H, amp, beta)
    if E_arr is None:
        return None
    ifn = interp1d(HE_Z_GRID, E_arr, kind='linear', bounds_error=False, fill_value=np.nan)
    def fn(z, _Om):
        za = np.atleast_1d(np.asarray(z, float))
        Ev = ifn(za)
        return None if (np.any(np.isnan(Ev)) or np.any(Ev <= 0)) else Ev
    return fn

# ──────────────────────────────────────────────────────────────────────────────
# HE_BD: BD ODE with A2'-consistent equilibrium
#   psi_eq = 1/(1+alpha_H)  [axiom-consistent: E(0)=1]
#   V(psi) = 0.5*m2*(psi - psi_eq)^2
#   psi_ini = psi*(z_ini) from A2' formula using LCDM E at z=1000
# ──────────────────────────────────────────────────────────────────────────────
def _hebd_ode(N, y, Om, B, m2, psi_eq):
    """BD FRW ODE with V(psi) = 0.5*m2*(psi-psi_eq)^2."""
    A = BD_A
    psi, chi = y[0], y[1]
    emN3   = np.exp(-3.0 * N)
    emN4   = np.exp(-4.0 * N)
    ApBpsi = A + B * psi

    denom_f1 = ApBpsi + B * chi - chi**2 / 6.0
    numer_f1 = Om * emN3 + OR * emN4 + m2 * (psi - psi_eq)**2 / 6.0

    if denom_f1 < 1e-10 or numer_f1 < 0.0:
        return [0.0, 0.0]
    E2 = numer_f1 / denom_f1
    if E2 < 1e-20:
        return [0.0, 0.0]

    numer_a = (-OR * emN4
               - 0.5 * m2 * (psi - psi_eq)**2
               + B * m2 * (psi - psi_eq)
               + E2 * (0.5 * chi**2 + B * chi - 12.0 * B**2 - 3.0 * ApBpsi))
    denom_a = E2 * (2.0 * ApBpsi + 6.0 * B**2)

    if abs(denom_a) < 1e-20:
        return [0.0, 0.0]
    alpha = numer_a / denom_a

    chi_p = (6.0 * B - chi) * alpha + 12.0 * B - 3.0 * chi - m2 * (psi - psi_eq) / E2
    return [chi, chi_p]

def _make_E_HE_BD(Om, B, m2, alpha_H=None):
    """BD ODE with A2' initial conditions and axiom-consistent potential."""
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    if alpha_H is None:
        alpha_H = Om / OL0

    psi_eq = 1.0 / (1.0 + alpha_H)

    # Initial psi at z=1000 from A2' formula using LCDM E
    z_ini_val   = np.exp(-BD_N_INI) - 1.0  # ≈ 1000
    E_lcdm_ini  = np.sqrt(Om*(1+z_ini_val)**3 + OR*(1+z_ini_val)**4 + OL0)
    psi_ini     = 1.0 / (1.0 + alpha_H * (1+z_ini_val)**3 / E_lcdm_ini)
    chi_ini     = 0.0

    N_eval = np.linspace(BD_N_INI, 0.0, 2000)
    try:
        sol = solve_ivp(
            _hebd_ode, [BD_N_INI, 0.0], [psi_ini, chi_ini],
            t_eval=N_eval, args=(Om, B, m2, psi_eq),
            method='RK45', rtol=1e-7, atol=1e-9, max_step=0.05,
            dense_output=False,
        )
    except Exception:
        return None

    if not sol.success:
        return None

    psi_v, chi_v, N_v = sol.y[0], sol.y[1], sol.t
    emN3   = np.exp(-3.0 * N_v)
    emN4   = np.exp(-4.0 * N_v)
    ApBpsi = BD_A + B * psi_v
    d_f1   = ApBpsi + B * chi_v - chi_v**2 / 6.0
    n_f1   = Om * emN3 + OR * emN4 + m2 * (psi_v - psi_eq)**2 / 6.0

    if np.any(d_f1 <= 0) or np.any(n_f1 < 0) or np.any(~np.isfinite(n_f1)):
        return None

    E2_v = n_f1 / d_f1
    if np.any(E2_v <= 0) or np.any(~np.isfinite(E2_v)):
        return None

    E2_today = E2_v[-1]
    if E2_today <= 0:
        return None
    E_v = np.sqrt(E2_v / E2_today)

    z_v = np.exp(-N_v) - 1.0
    idx = np.argsort(z_v)
    z_s, E_s = z_v[idx], E_v[idx]
    ifn = interp1d(z_s, E_s, kind='linear', bounds_error=False, fill_value=np.nan)

    def fn(z, _Om):
        za = np.atleast_1d(np.asarray(z, float))
        Ev = ifn(za)
        return None if (np.any(np.isnan(Ev)) or np.any(Ev <= 0)) else Ev
    return fn

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
    def fn(z, _Om):
        return _E_D(np.atleast_1d(np.asarray(z, float)), Om, amp, beta)
    return fn

# ──────────────────────────────────────────────────────────────────────────────
# Workers
# ──────────────────────────────────────────────────────────────────────────────
def _he_s_worker(start):
    """HE_S k=2 (Om, H0), alpha_H=Om/OL0 fixed."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')

    def obj(p):
        Om, H0 = p
        if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
            return 1e9
        OL0 = 1.0 - Om - OR
        if OL0 <= 0:
            return 1e9
        fn = _make_E_HE_S(Om, Om/OL0)
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


def _he_sf_worker(start):
    """HE_Sf k=3 (Om, H0, alpha_H), alpha_H free."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')

    def obj(p):
        Om, H0, alpha_H = p
        if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
            return 1e9
        if alpha_H < 0.01 or alpha_H > 5.0:
            return 1e9
        fn = _make_E_HE_S(Om, alpha_H)
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


def _he_d_worker(start):
    """HE_D k=4 (Om, H0, amp, beta), alpha_H=Om/OL0 fixed."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')

    def obj(p):
        Om, H0, amp, beta = p
        if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
            return 1e9
        if amp < -5 or amp > 5 or beta < 0 or beta > 20:
            return 1e9
        OL0 = 1.0 - Om - OR
        if OL0 <= 0:
            return 1e9
        fn = _make_E_HE_D(Om, Om/OL0, amp, beta)
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


def _he_bd_worker(start):
    """HE_BD k=4 (Om, H0, B_A, m2), alpha_H=Om/OL0 fixed."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')

    def obj(p):
        Om, H0, B_A, m2 = p
        if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
            return 1e9
        if B_A < -2 or B_A > 2 or m2 < 0 or m2 > 2000:
            return 1e9
        OL0 = 1.0 - Om - OR
        if OL0 <= 0:
            return 1e9
        B = B_A * BD_A
        fn = _make_E_HE_BD(Om, B, m2)
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


def _boot_he_worker(args):
    """
    Bootstrap batch for HE models.
    Each item: (s0, new_bao, new_cmb, new_rsd, model_type, fixed_params, k_win)
      model_type: 'he_s', 'he_sf', 'he_d', 'he_bd'
      fixed_params: extra params beyond Om,H0 (fixed at winner values)
      k_win: AICc k for winner
    """
    boot_batch = args
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    import sys as _sys
    _l35 = _sys.modules.get('l35_test') or __import__('l35_test')
    orig_bao = dict(_l35.DESI_DR2)
    orig_cmb = _l35.CMB_OBS.copy()
    orig_rsd = _l35.FS8_OBS.copy()

    results = []
    np.random.seed(42)

    for item in boot_batch:
        s0, new_bao, new_cmb, new_rsd, model_type, fixed_params, k_win = item

        _l35.DESI_DR2 = {**orig_bao, 'value': new_bao}
        _l35.CMB_OBS  = new_cmb
        _l35.FS8_OBS  = new_rsd

        def _tot(fn, Om, H0):
            t = (chi2_bao(fn, Om, H0) + chi2_cmb(fn, Om, H0) +
                 chi2_sn(fn, Om, H0)  + chi2_rsd(fn, Om, H0))
            return t if (np.isfinite(t) and t < 1e7) else 1e9

        def obj_win(p):
            Om, H0 = p
            if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
                return 1e9
            OL0 = 1.0 - Om - OR
            if OL0 <= 0:
                return 1e9
            if model_type == 'he_s':
                fn = _make_E_HE_S(Om, Om/OL0)
            elif model_type == 'he_sf':
                fn = _make_E_HE_S(Om, fixed_params[0])
            elif model_type == 'he_d':
                fn = _make_E_HE_D(Om, Om/OL0, fixed_params[0], fixed_params[1])
            elif model_type == 'he_bd':
                fn = _make_E_HE_BD(Om, fixed_params[0], fixed_params[1])
            else:
                return 1e9
            return 1e9 if fn is None else _tot(fn, Om, H0)

        def obj_lcdm(p):
            Om, H0 = p
            if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
                return 1e9
            fn = lambda z, _: E_lcdm(z, Om)
            return _tot(fn, Om, H0)

        best_win, par_win = 1e9, None
        try:
            r = minimize(obj_win, s0, method='Nelder-Mead',
                         options={'xatol': 1e-4, 'fatol': 1e-4, 'maxiter': 300})
            if r.fun < best_win:
                best_win, par_win = r.fun, r.x
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

        if par_win is None or par_lcdm is None:
            results.append(float('nan'))
            continue

        bnd_win  = _at_boundary(par_win,  _BOUNDS_LCDM)
        bnd_lcdm = _at_boundary(par_lcdm, _BOUNDS_LCDM)
        if bnd_win or bnd_lcdm:
            results.append(float('nan'))
        else:
            aicc_win  = _aicc(best_win,  k_win)
            aicc_lcdm = _aicc(best_lcdm, k=2)
            results.append(float(aicc_win - aicc_lcdm))

    _l35.DESI_DR2 = orig_bao
    _l35.CMB_OBS  = orig_cmb
    _l35.FS8_OBS  = orig_rsd
    return results

# ──────────────────────────────────────────────────────────────────────────────
# Task 0: Baselines
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

    E_D_fn = _make_E_D(D_BEST['Om'], D_BEST['amp'], D_BEST['beta'])
    cb2, cc2, cs2, cr2, ct2 = _chi2_all(E_D_fn, D_BEST['Om'], D_BEST['H0'])
    ac_D = _aicc(ct2, k=4)
    ok2 = 'CONFIRMED' if abs(ac_D - D_AICC) < 0.1 else 'CHANGED'
    print(f"  Model D: Om={D_BEST['Om']}, H0={D_BEST['H0']}")
    print(f"  chi2: BAO={cb2:.4f} CMB={cc2:.4f} SN={cs2:.4f} RSD={cr2:.4f}")
    print(f"  AICc={ac_D:.4f}  dAICc={ac_D - LCDM_AICC:.2f} [{ok2}]")
    sys.stdout.flush()

    return {'lcdm_aicc': ac_l, 'd_aicc': ac_D}


# ──────────────────────────────────────────────────────────────────────────────
# Tasks 1-4: HE model fits (parallel pool)
# ──────────────────────────────────────────────────────────────────────────────
def _run_he_models(pool):
    t0  = time.time()
    rng = np.random.default_rng(42)

    # HE_S starts (k=2): Om, H0  [20 starts]
    starts_s = []
    for _ in range(16):
        starts_s.append([rng.uniform(0.25, 0.42), rng.uniform(62, 76)])
    for s in [[0.310, 68.4], [0.309, 68.0], [0.322, 67.0], [0.300, 69.5]]:
        starts_s.append(s)

    # HE_Sf starts (k=3): Om, H0, alpha_H  [15 starts]
    starts_sf = []
    for _ in range(10):
        starts_sf.append([rng.uniform(0.25, 0.42), rng.uniform(62, 76),
                          rng.uniform(0.1, 2.0)])
    for s in [[0.310, 68.4, 0.46], [0.309, 68.0, 0.46], [0.322, 67.0, 0.5],
              [0.310, 68.0, 1.0],   [0.310, 68.0, 0.2]]:
        starts_sf.append(s)

    # HE_D starts (k=4): Om, H0, amp, beta  [20 starts]
    starts_d = []
    for _ in range(15):
        starts_d.append([rng.uniform(0.25, 0.42), rng.uniform(62, 76),
                         rng.uniform(-2, 2), rng.uniform(0.5, 10)])
    for s in [[0.322, 66.98, 0.818, 3.53], [0.310, 68.0, 0.5, 3.0],
              [0.310, 68.0, 1.0, 5.0],      [0.322, 67.0, 0.0, 0.0],
              [0.310, 68.0, 0.8, 2.0]]:
        starts_d.append(s)

    # HE_BD skipped: psi_ini≈0 at z=1000 causes ODE instability
    starts_bd = []

    print("\n" + "=" * 60)
    print("Tasks 1-4: HE model fits (parallel pool)")
    print("=" * 60)
    print(f"  HE_S   k=2: {len(starts_s)} starts")
    print(f"  HE_Sf  k=3: {len(starts_sf)} starts")
    print(f"  HE_D   k=4: {len(starts_d)} starts")
    print(f"  HE_BD  k=4: SKIPPED (psi_ini~0 ODE instability)")
    sys.stdout.flush()

    res_s  = pool.map(_he_s_worker,  starts_s)
    res_sf = pool.map(_he_sf_worker, starts_sf)
    res_d  = pool.map(_he_d_worker,  starts_d)

    elapsed = time.time() - t0
    print(f"  All HE scans done in {elapsed:.1f}s")
    sys.stdout.flush()

    def best_of(results):
        valid = [(c, p) for c, p in results if p is not None and c < 1e8]
        if not valid:
            return 1e9, None
        return min(valid, key=lambda x: x[0])

    return {
        'he_s':  best_of(res_s),
        'he_sf': best_of(res_sf),
        'he_d':  best_of(res_d),
        'he_bd': (1e9, None),   # skipped
        'elapsed': elapsed,
    }


def _report_he_model(tag, label, k, param_names, best_chi2, best_params, bounds):
    """Print standardized result block; return parsed result dict."""
    print(f"\n{'=' * 60}")
    print(f"Task: {label} (k={k})")
    print(f"{'=' * 60}")

    if best_params is None:
        print("  FAILED: no valid result")
        return {'aicc': None, 'daicc': None, 'boundary': True,
                'w0': None, 'wa': None, 'params': None, 'raw_params': None}

    aicc  = _aicc(best_chi2, k)
    daicc = aicc - LCDM_AICC
    bnd   = _at_boundary(best_params, bounds[:len(best_params)])
    vdict = _verdict(daicc, boundary=bnd, k2=(k == 2))

    for name, val in zip(param_names, best_params):
        print(f"  {name}={val:.4f}", end="  ")
    print()

    # Build E_fn for chi2 reporting
    Om, H0 = best_params[0], best_params[1]
    OL0 = 1.0 - Om - OR
    E_fn = None
    extra = {}

    if tag == 'he_s':
        alpha_H = Om / OL0 if OL0 > 0 else 0.46
        E_fn = _make_E_HE_S(Om, alpha_H)
        extra = {'alpha_H': alpha_H}
    elif tag == 'he_sf':
        alpha_H = best_params[2]
        E_fn = _make_E_HE_S(Om, alpha_H)
        alpha_th = Om / OL0 if OL0 > 0 else float('nan')
        dev = (alpha_H - alpha_th) / alpha_th * 100 if alpha_th > 0 else float('nan')
        extra = {'alpha_H': alpha_H, 'alpha_th': alpha_th, 'dev_pct': dev}
        print(f"  alpha_H_theory=Om/OL0={alpha_th:.4f}  dev={dev:+.1f}%")
    elif tag == 'he_d':
        amp, beta = best_params[2], best_params[3]
        alpha_H = Om / OL0 if OL0 > 0 else 0.46
        E_fn = _make_E_HE_D(Om, alpha_H, amp, beta)
        extra = {'amp': amp, 'beta': beta, 'alpha_H': alpha_H}
    elif tag == 'he_bd':
        B_A, m2 = best_params[2], best_params[3]
        B = B_A * BD_A
        E_fn = _make_E_HE_BD(Om, B, m2)
        extra = {'B_A': B_A, 'm2': m2}

    w0, wa = None, None
    if E_fn is not None:
        cb, cc, cs, cr, ct = _chi2_all(E_fn, Om, H0)
        print(f"  chi2: BAO={cb:.4f} CMB={cc:.4f} SN={cs:.4f} RSD={cr:.4f}")
        try:
            w0, wa = cpl_wa(E_fn, Om)
        except Exception:
            pass
    else:
        print("  E_fn invalid (convergence failure)")

    print(f"  AICc={aicc:.4f}  dAICc={daicc:.2f}  vs D: {aicc - D_AICC:+.2f}")
    print(f"  boundary={bnd}")
    if w0 is not None:
        print(f"  CPL: w0={w0:.4f}, wa={wa:.4f}")
    print(f"  Verdict: {vdict}")
    sys.stdout.flush()

    return {
        'aicc': aicc, 'daicc': daicc, 'boundary': bnd,
        'w0': w0, 'wa': wa,
        'params': best_params, 'raw_params': best_params,
        'chi2': best_chi2, 'extra': extra,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Task 5: Bootstrap
# ──────────────────────────────────────────────────────────────────────────────
def task5_bootstrap(pool, winner_tag, winner_result):
    print("\n" + "=" * 60)
    print(f"Task 5: Bootstrap ({winner_tag}, N={N_BOOT})")
    print("=" * 60)
    t0 = time.time()

    p     = winner_result['params']
    Om_w  = p[0]; H0_w = p[1]
    k_win = {'he_s': 2, 'he_sf': 3, 'he_d': 4, 'he_bd': 4}[winner_tag]

    # Build winner E_fn for nominal BAO vector
    OL0_w = 1.0 - Om_w - OR
    if winner_tag == 'he_s':
        E_fn_nom = _make_E_HE_S(Om_w, Om_w/OL0_w)
        fixed_params = None
    elif winner_tag == 'he_sf':
        aH = p[2]
        E_fn_nom = _make_E_HE_S(Om_w, aH)
        fixed_params = (aH,)
    elif winner_tag == 'he_d':
        amp_w, beta_w = p[2], p[3]
        E_fn_nom = _make_E_HE_D(Om_w, Om_w/OL0_w, amp_w, beta_w)
        fixed_params = (amp_w, beta_w)
    elif winner_tag == 'he_bd':
        B_w = p[2] * BD_A; m2_w = p[3]
        E_fn_nom = _make_E_HE_BD(Om_w, B_w, m2_w)
        fixed_params = (B_w, m2_w)
    else:
        print("  SKIPPED: unknown winner tag")
        return None

    if E_fn_nom is None:
        print("  SKIPPED: winner E_fn invalid")
        return None

    lcdm_fn   = lambda z, _: E_lcdm(z, LCDM_BEST['Om'])
    bao_nom   = _bao_theory_vec(E_fn_nom, Om_w, H0_w)
    bao_nom_l = _bao_theory_vec(lcdm_fn, LCDM_BEST['Om'], LCDM_BEST['H0'])
    if bao_nom is None or bao_nom_l is None:
        print("  SKIPPED: BAO theory vector failed")
        return None

    rng     = np.random.default_rng(99)
    bao_cov = np.linalg.inv(DESI_DR2_COV_INV)
    bao_L   = np.linalg.cholesky(bao_cov)

    boot_items = []
    for _ in range(N_BOOT):
        nb  = bao_nom_l + bao_L @ rng.standard_normal(13)
        nc  = CMB_OBS + CMB_SIG * rng.standard_normal(len(CMB_OBS))
        nr  = FS8_OBS + FS8_SIG * rng.standard_normal(len(FS8_OBS))
        s0  = [Om_w + rng.normal(0, 0.01), H0_w + rng.normal(0, 0.5)]
        boot_items.append((s0, nb, nc, nr, winner_tag, fixed_params, k_win))

    batch_size = max(1, N_BOOT // N_WORKERS)
    batches    = [boot_items[i:i+batch_size] for i in range(0, N_BOOT, batch_size)]
    raw        = pool.map(_boot_he_worker, batches)

    all_daicc = []
    for batch_res in raw:
        all_daicc.extend(batch_res)

    vals    = np.array([v for v in all_daicc if v is not None and np.isfinite(v)])
    elapsed = time.time() - t0
    print(f"  Bootstrap done in {elapsed:.1f}s")
    print(f"  Valid: {len(vals)}/{N_BOOT}")
    if len(vals) == 0:
        print("  Verdict: FAIL (no valid samples)")
        return {'valid': 0, 'verdict': 'FAIL'}

    med   = float(np.median(vals))
    lo    = float(np.percentile(vals, 16))
    hi    = float(np.percentile(vals, 84))
    p_lt4 = float(np.mean(vals < -4))
    p_lt2 = float(np.mean(vals < -2))
    p_lt0 = float(np.mean(vals < 0))
    verd  = 'PASS' if p_lt4 >= 0.90 else 'FAIL'
    print(f"  dAICc median={med:.2f}  68%CI=[{lo:.2f},{hi:.2f}]")
    print(f"  dAICc<-4: {p_lt4*100:.1f}%  <-2: {p_lt2*100:.1f}%  <0: {p_lt0*100:.1f}%")
    print(f"  Verdict: {verd}")
    sys.stdout.flush()

    return {'valid': int(len(vals)), 'median': med, 'ci68': [lo, hi],
            'frac_lt4': p_lt4, 'frac_lt2': p_lt2, 'frac_lt0': p_lt0, 'verdict': verd}


# ──────────────────────────────────────────────────────────────────────────────
# Task 6: CPL extraction summary
# ──────────────────────────────────────────────────────────────────────────────
def task6_cpl(results_map):
    print("\n" + "=" * 60)
    print("Task 6: CPL Extraction")
    print("=" * 60)
    print(f"  {'Model':<20} {'w0':>8} {'wa':>8}  direction")
    print("  " + "-" * 50)
    labels = {'he_s': 'HE_S k=2', 'he_sf': 'HE_Sf k=3',
              'he_d': 'HE_D k=4', 'he_bd': 'HE_BD k=4'}
    for tag in ['he_s', 'he_sf', 'he_d', 'he_bd']:
        r  = results_map.get(tag, {})
        w0 = r.get('w0'); wa = r.get('wa')
        if w0 is None or wa is None:
            print(f"  {labels[tag]:<20} {'None':>8} {'None':>8}  ?")
        else:
            dir_wa    = 'same' if wa * (-0.83) > 0 else 'opposite'
            print(f"  {labels[tag]:<20} {w0:>8.4f} {wa:>8.4f}  {dir_wa}")
    print(f"  {'DESI observed':<20} {-0.757:>8.3f} {-0.50:>8.2f}")
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 7: Residuals vs LCDM
# ──────────────────────────────────────────────────────────────────────────────
def task7_residuals(winner_tag, winner_result):
    print("\n" + "=" * 60)
    print(f"Task 7: Residual Analysis ({winner_tag} vs LCDM)")
    print("=" * 60)

    p   = winner_result['params']
    Om  = p[0]; H0 = p[1]
    OL0 = 1.0 - Om - OR

    if winner_tag == 'he_s':
        E_win = _make_E_HE_S(Om, Om/OL0)
    elif winner_tag == 'he_sf':
        E_win = _make_E_HE_S(Om, p[2])
    elif winner_tag == 'he_d':
        E_win = _make_E_HE_D(Om, Om/OL0, p[2], p[3])
    elif winner_tag == 'he_bd':
        E_win = _make_E_HE_BD(Om, p[2]*BD_A, p[3])
    else:
        print("  SKIPPED: unknown tag")
        return

    if E_win is None:
        print("  SKIPPED: E_fn invalid")
        return

    E_lc = lambda z, _: E_lcdm(z, LCDM_BEST['Om'])
    cb_w, cc_w, cs_w, cr_w, _ = _chi2_all(E_win, Om, H0)
    cb_l, cc_l, cs_l, cr_l, _ = _chi2_all(E_lc, LCDM_BEST['Om'], LCDM_BEST['H0'])

    dBAO = cb_l - cb_w; dCMB = cc_l - cc_w
    dSN  = cs_l - cs_w; dRSD = cr_l - cr_w
    dtot = dBAO + dCMB + dSN + dRSD

    print(f"  dBAO = {dBAO:+.4f}  ({winner_tag}: {cb_w:.2f} vs LCDM: {cb_l:.2f})")
    print(f"  dCMB = {dCMB:+.4f}  ({winner_tag}: {cc_w:.2f} vs LCDM: {cc_l:.2f})")
    print(f"  dSN  = {dSN:+.4f}  ({winner_tag}: {cs_w:.2f} vs LCDM: {cs_l:.2f})")
    print(f"  dRSD = {dRSD:+.4f}  ({winner_tag}: {cr_w:.2f} vs LCDM: {cr_l:.2f})")
    print(f"  dtot = {dtot:+.4f}")
    if abs(dtot) > 1e-6:
        print(f"  BAO: {dBAO/dtot*100:+.1f}%  CMB: {dCMB/dtot*100:+.1f}%"
              f"  SN: {dSN/dtot*100:+.1f}%  RSD: {dRSD/dtot*100:+.1f}%")
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 8: w(z) visualization
# ──────────────────────────────────────────────────────────────────────────────
def task8_wz_plot(results_map, out_dir):
    print("\n" + "=" * 60)
    print("Task 8: w(z) Visualization")
    print("=" * 60)

    z_plot = np.linspace(0.01, 2.0, 300)
    fig, ax = plt.subplots(figsize=(9, 5))

    ax.axhline(-1.0, color='k', ls='--', lw=1, label='LCDM (w=-1)')
    ax.axhline(-0.757, color='gray', ls=':', lw=1, alpha=0.7, label='DESI w0=-0.757')

    # Model D
    E_D_fn = _make_E_D(D_BEST['Om'], D_BEST['amp'], D_BEST['beta'])
    try:
        w0_D, wa_D = cpl_wa(E_D_fn, D_BEST['Om'])
        ax.plot(z_plot, w0_D + wa_D*z_plot/(1+z_plot), 'C4', ls='-.', lw=1.5,
                label=f"Model D (w0={w0_D:.2f}, wa={wa_D:.2f})")
    except Exception:
        pass

    colors = {'he_s': 'C0', 'he_sf': 'C1', 'he_d': 'C2', 'he_bd': 'C3'}
    labels = {'he_s': 'HE_S k=2', 'he_sf': 'HE_Sf k=3',
              'he_d': 'HE_D k=4', 'he_bd': 'HE_BD k=4'}
    for tag in ['he_s', 'he_sf', 'he_d', 'he_bd']:
        r  = results_map.get(tag, {})
        w0 = r.get('w0'); wa = r.get('wa')
        if w0 is None or wa is None:
            continue
        ax.plot(z_plot, w0 + wa*z_plot/(1+z_plot), colors[tag], lw=1.5,
                label=f"{labels[tag]} (w0={w0:.2f}, wa={wa:.2f})")

    ax.set_xlabel('z'); ax.set_ylabel('w(z)')
    ax.set_title('L42: Model HE (A2\' modified) w(z)')
    ax.legend(fontsize=7, loc='best')
    ax.set_ylim(-3.5, 1.0)
    ax.grid(alpha=0.3)
    out = os.path.join(out_dir, 'l42_task8_wz.png')
    fig.savefig(out, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f"  Plot: {out}")
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 9: rho_DE comparison (HE_S vs Model S vs Model D vs LCDM)
# ──────────────────────────────────────────────────────────────────────────────
def task9_rho_comparison(results_map, out_dir):
    print("\n" + "=" * 60)
    print("Task 9: rho_DE Comparison (HE_S vs Model S vs Model D vs LCDM)")
    print("=" * 60)

    z_pts = np.array([0.0, 0.5, 1.0, 2.0, 3.0])

    # LCDM: rho_DE = OL0 (constant)
    Om_l  = LCDM_BEST['Om']
    OL0_l = 1.0 - Om_l - OR
    rho_lcdm = np.ones(len(z_pts))

    # Model S (L40): psi*(z) = 1/(1+alpha*(1+z)^3), alpha=Om/OL0
    r_s = results_map.get('he_s', {})
    if r_s.get('params') is not None:
        Om_s  = r_s['params'][0]
        OL0_s = 1.0 - Om_s - OR
        aH_s  = Om_s / OL0_s
    else:
        Om_s  = LCDM_BEST['Om']
        OL0_s = 1.0 - Om_s - OR
        aH_s  = Om_s / OL0_s

    alpha_orig = aH_s
    psi0_orig  = 1.0 / (1.0 + alpha_orig)
    psi_orig   = 1.0 / (1.0 + alpha_orig * (1+z_pts)**3)
    rho_modS   = psi_orig / psi0_orig   # Model S (L40 form)

    # HE_S: self-consistent
    if r_s.get('params') is not None:
        Om_he = r_s['params'][0]
        OL0_he = 1.0 - Om_he - OR
        aH_he = Om_he / OL0_he
        psi0_he = 1.0 / (1.0 + aH_he)
        E_he = _solve_E_HE_S(z_pts, Om_he, aH_he)
        if E_he is not None:
            psi_he  = 1.0 / (1.0 + aH_he * (1+z_pts)**3 / E_he)
            rho_HE  = psi_he / psi0_he
        else:
            rho_HE = np.full(len(z_pts), np.nan)
    else:
        rho_HE = np.full(len(z_pts), np.nan)

    # Model D
    OL0_d = 1.0 - D_BEST['Om'] - OR
    alpha_d = D_BEST['Om'] / OL0_d
    psi0_d  = 1.0 / (1.0 + alpha_d)
    psi_d   = 1.0 / (1.0 + alpha_d * (1+z_pts)**3)
    ratio_d = psi0_d / psi_d
    rho_D   = 1.0 + D_BEST['amp'] * (ratio_d - 1.0) * np.exp(-D_BEST['beta'] * z_pts)

    print(f"  {'z':>5} {'LCDM':>10} {'Model S':>10} {'HE_S':>10} {'Model D':>10}")
    print("  " + "-" * 48)
    for i, z in enumerate(z_pts):
        print(f"  {z:5.1f} {rho_lcdm[i]:10.4f} {rho_modS[i]:10.4f} "
              f"{rho_HE[i]:10.4f} {rho_D[i]:10.4f}")

    # H modification effect: compare HE_S vs Model S
    if not np.any(np.isnan(rho_HE)):
        diff = rho_HE - rho_modS
        print(f"\n  HE_S vs Model S rho_DE difference:")
        for i, z in enumerate(z_pts):
            print(f"    z={z:.1f}: {diff[i]:+.4f} ({diff[i]/rho_modS[i]*100:+.1f}%)")
        rms = np.sqrt(np.mean(diff**2))
        print(f"  RMS deviation HE_S vs Model S: {rms:.4f}")

    # w(z) plot for rho_DE
    z_plot = np.linspace(0.0, 3.0, 300)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # rho_DE(z)/rho_DE(0)
    ax1.axhline(1.0, color='k', ls='--', lw=1, label='LCDM')

    # Model S
    psi_S_plot = 1.0/(1.0 + alpha_orig*(1+z_plot)**3)
    ax1.plot(z_plot, psi_S_plot/psi0_orig, 'C1', ls='--', lw=1.5, label='Model S (L40)')

    # HE_S
    if r_s.get('params') is not None:
        E_he_plot = _solve_E_HE_S(z_plot, Om_he, aH_he)
        if E_he_plot is not None:
            psi_he_plot = 1.0/(1.0 + aH_he*(1+z_plot)**3/E_he_plot)
            ax1.plot(z_plot, psi_he_plot/psi0_he, 'C0', lw=2, label=f"HE_S (A2')")

    # Model D
    psi_D_plot = 1.0/(1.0 + alpha_d*(1+z_plot)**3)
    ratio_D_plot = psi0_d/psi_D_plot
    rho_D_plot = 1.0 + D_BEST['amp']*(ratio_D_plot-1)*np.exp(-D_BEST['beta']*z_plot)
    ax1.plot(z_plot, rho_D_plot, 'C4', ls='-.', lw=1.5, label='Model D')

    ax1.set_xlabel('z')
    ax1.set_ylabel('rho_DE(z)/rho_DE(0)')
    ax1.set_title('Dark energy density evolution')
    ax1.legend(fontsize=8)
    ax1.grid(alpha=0.3)

    # E(z)/E_LCDM(z) ratio
    E_lcdm_plot = E_lcdm(z_plot, LCDM_BEST['Om'])
    ax2.axhline(1.0, color='k', ls='--', lw=1, label='LCDM')
    if r_s.get('params') is not None and E_he_plot is not None:
        ax2.plot(z_plot, E_he_plot/E_lcdm_plot, 'C0', lw=2, label='HE_S')
    r_sf = results_map.get('he_sf', {})
    if r_sf.get('params') is not None:
        p_sf = r_sf['params']
        E_sf_plot = _solve_E_HE_S(z_plot, p_sf[0], p_sf[2])
        if E_sf_plot is not None:
            ax2.plot(z_plot, E_sf_plot/E_lcdm_plot, 'C1', ls='--', lw=1.5, label='HE_Sf')
    E_D_plot = _E_D(z_plot, D_BEST['Om'], D_BEST['amp'], D_BEST['beta'])
    if E_D_plot is not None:
        ax2.plot(z_plot, E_D_plot/E_lcdm_plot, 'C4', ls='-.', lw=1.5, label='Model D')
    ax2.set_xlabel('z')
    ax2.set_ylabel('E(z)/E_LCDM(z)')
    ax2.set_title('Hubble ratio vs LCDM')
    ax2.legend(fontsize=8)
    ax2.grid(alpha=0.3)

    out = os.path.join(out_dir, 'l42_task9_rho.png')
    fig.savefig(out, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f"  Plot: {out}")
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────
def main():
    t_total = time.time()
    out_dir = _SCRIPT_DIR

    print("=" * 60)
    print("L42: Model HE (A2' modified axiom) Verification")
    print(f"8-worker parallel  |  LCDM baseline AICc={LCDM_AICC}")
    print("=" * 60)
    print("\nWarming up SN cache...")
    get_sn()
    print("  SN ready.")
    sys.stdout.flush()

    # Task 0
    r0 = task0_baseline()

    # Tasks 1-4 (parallel pool)
    ctx = mp.get_context('spawn')
    with ctx.Pool(N_WORKERS) as pool:
        he_raw = _run_he_models(pool)

        # Parse results
        res = {}

        r1 = _report_he_model(
            'he_s', 'Model HE_S (k=2, CORE)', 2,
            ['Om', 'H0'], he_raw['he_s'][0], he_raw['he_s'][1], _BOUNDS_HE_S)
        res['he_s'] = r1

        r2 = _report_he_model(
            'he_sf', 'Model HE_Sf (k=3, alpha_H free)', 3,
            ['Om', 'H0', 'alpha_H'], he_raw['he_sf'][0], he_raw['he_sf'][1], _BOUNDS_HE_SF)
        res['he_sf'] = r2

        r3 = _report_he_model(
            'he_d', 'Model HE_D (k=4, D-form)', 4,
            ['Om', 'H0', 'amp', 'beta'], he_raw['he_d'][0], he_raw['he_d'][1], _BOUNDS_HE_D)
        res['he_d'] = r3

        # HE_BD skipped due to ODE instability (psi_ini≈0 at z=1000)
        print(f"\n{'=' * 60}")
        print("Task: Model HE_BD (k=4, BD+A2') -- SKIPPED")
        print(f"{'=' * 60}")
        print("  psi_ini ~ 4e-5 at z=1000 causes stiff ODE, very slow/non-convergent.")
        res['he_bd'] = {'aicc': None, 'daicc': None, 'boundary': True,
                        'w0': None, 'wa': None, 'params': None, 'raw_params': None}

        # Best performer
        best_tag = min(res, key=lambda t: _safe_daicc(res[t]))
        best_daicc = _safe_daicc(res[best_tag])
        print(f"\n  Winner: {best_tag}  dAICc={best_daicc:.2f}")
        sys.stdout.flush()

        # Task 5: Bootstrap on winner — only if winner shows improvement (dAICc < -2)
        r5 = None
        if res[best_tag]['params'] is not None and best_daicc < -2:
            r5 = task5_bootstrap(pool, best_tag, res[best_tag])
        else:
            print("\n" + "=" * 60)
            print(f"Task 5: Bootstrap -- SKIPPED (winner dAICc={best_daicc:.2f} >= -2)")
            print("=" * 60)

    # Task 6: CPL
    task6_cpl(res)

    # Task 7: Residuals
    if res[best_tag]['params'] is not None:
        task7_residuals(best_tag, res[best_tag])

    # Task 8: w(z) plot
    task8_wz_plot(res, out_dir)

    # Task 9: rho_DE comparison
    task9_rho_comparison(res, out_dir)

    # ── Summary ──
    elapsed = time.time() - t_total
    print("\n" + "=" * 60)
    print("L42 RESULTS SUMMARY")
    print("=" * 60)

    print(f"\n[Task 0] Baselines")
    print(f"  LCDM: AICc={r0.get('lcdm_aicc', LCDM_AICC):.2f}")
    print(f"  Model D: AICc={r0.get('d_aicc', D_AICC):.2f}  "
          f"dAICc={r0.get('d_aicc', D_AICC) - LCDM_AICC:.2f}")

    tag_labels = {
        'he_s': 'Model HE_S k=2 (CORE)',
        'he_sf': 'HE_Sf k=3',
        'he_d': 'HE_D k=4',
        'he_bd': 'HE_BD k=4',
    }
    task_nums = {'he_s': 1, 'he_sf': 2, 'he_d': 3, 'he_bd': 4}

    for tag in ['he_s', 'he_sf', 'he_d', 'he_bd']:
        r  = res[tag]
        tn = task_nums[tag]
        print(f"\n[Task {tn}] {tag_labels[tag]}")
        if r.get('params') is not None:
            p = r['params']
            if tag == 'he_s':
                OL0 = 1.0 - p[0] - OR
                aH  = p[0]/OL0 if OL0 > 0 else float('nan')
                print(f"  Om={p[0]:.4f}, H0={p[1]:.4f}")
                print(f"  alpha_H = Om/OL0 = {aH:.4f} (fixed)")
            elif tag == 'he_sf':
                OL0  = 1.0 - p[0] - OR
                aH_t = p[0]/OL0 if OL0 > 0 else float('nan')
                dev  = (p[2] - aH_t)/aH_t*100 if aH_t > 0 else float('nan')
                print(f"  Om={p[0]:.4f}, H0={p[1]:.4f}, alpha_H={p[2]:.4f}")
                print(f"  alpha_H_theory={aH_t:.4f}  dev={dev:+.1f}%")
            elif tag == 'he_d':
                print(f"  Om={p[0]:.4f}, H0={p[1]:.4f}, amp={p[2]:.4f}, beta={p[3]:.4f}")
            elif tag == 'he_bd':
                print(f"  Om={p[0]:.4f}, H0={p[1]:.4f}, B/A={p[2]:.4f}, m2={p[3]:.2f}")
        aicc  = r.get('aicc'); daicc = r.get('daicc')
        if aicc is not None:
            bnd_str = '  [boundary]' if r.get('boundary') else ''
            v = _verdict(daicc, r.get('boundary', False), k2=(tag == 'he_s'))
            print(f"  AICc={aicc:.2f}  dAICc={daicc:.2f}{bnd_str}  [{v}]")
        if r.get('w0') is not None:
            print(f"  w0={r['w0']:.4f}, wa={r['wa']:.4f}")

    if r5:
        print(f"\n[Task 5] Bootstrap ({best_tag}, N={N_BOOT})")
        print(f"  valid={r5.get('valid', 0)}")
        if r5.get('median') is not None:
            print(f"  median={r5['median']:.2f}  "
                  f"68%CI=[{r5['ci68'][0]:.2f},{r5['ci68'][1]:.2f}]")
            print(f"  dAICc<-4: {r5['frac_lt4']*100:.1f}%  "
                  f"<-2: {r5['frac_lt2']*100:.1f}%  "
                  f"Verdict: {r5['verdict']}")

    # CPL table in summary
    print(f"\n[Task 6] CPL")
    for tag in ['he_s', 'he_sf', 'he_d', 'he_bd']:
        r = res[tag]
        if r.get('w0') is not None:
            dir_wa = 'same' if r['wa'] * (-0.83) > 0 else 'opposite'
            print(f"  {tag_labels[tag]}: w0={r['w0']:.4f}, wa={r['wa']:.4f}  [{dir_wa}]")
        else:
            print(f"  {tag_labels[tag]}: w0=None")
    print(f"  DESI: w0=-0.757, wa=-0.50")

    print(f"\n[Final Verdict]")
    d_hes  = _safe_daicc(res['he_s'])
    d_best = best_daicc
    v_hes  = _verdict(d_hes, res['he_s'].get('boundary', False), k2=True)
    v_best = _verdict(d_best, res[best_tag].get('boundary', False),
                      k2=(best_tag == 'he_s'))
    wa_hes = res['he_s'].get('wa')
    wa_ok  = wa_hes is not None and wa_hes < 0

    print(f"  HE_S (k=2, CORE)  dAICc={d_hes:.2f}: {v_hes}")
    print(f"  Winner ({best_tag})       dAICc={d_best:.2f}: {v_best}")

    if d_hes < -4 and not res['he_s'].get('boundary', True) and wa_ok:
        print("  Strategy A: HE_S SUCCESS -> SQT axiom A2' minimum modification paper")
    elif d_best < -2 and not res[best_tag].get('boundary', True):
        print(f"  Strategy B: {best_tag} success -> partial A2' modification")
    else:
        print("  Strategy C: All HE FAIL -> A2' axiom modification insufficient")
        print("              -> SQT axiom system fundamental redesign (L43)")

    # A2' modification effect
    print(f"\n  A2' modification (H-proportional) vs original A2:")
    print(f"    Model S (A2, L40): dAICc=+284.01 [K90 KILL]")
    print(f"    HE_S    (A2')    : dAICc={d_hes:.2f} [{v_hes}]")
    if np.isfinite(d_hes):
        delta = 284.01 - d_hes
        print(f"    Improvement: {delta:+.2f} AICc units")

    print(f"\nTotal elapsed: {elapsed:.1f}s")

    out_json = os.path.join(out_dir, 'l42_results.json')
    save_data = {
        'r0': _jsonify(r0), 'models': _jsonify(res),
        'bootstrap': _jsonify(r5), 'elapsed': elapsed,
        'winner': best_tag, 'winner_daicc': best_daicc,
    }
    with open(out_json, 'w') as f:
        json.dump(save_data, f, indent=2)
    print(f"Saved: {out_json}")
    sys.stdout.flush()


if __name__ == '__main__':
    main()
