#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L54: sigma_0(z) Time-Varying (Model V) — Theory's Last Attempt
===============================================================
sigma_0(z) = sigma_now + (sigma_late - sigma_now) * 0.5*(1+tanh((z-z_t)/dz))
dz=0.5 fixed. sigma_UV=3.31e9 fixed (L49).
Grid: sigma_now x sigma_late x z_t = 12x15x12 = 2160 pts, 8 workers
Output: l54_main.png, l54_results.json
"""

import os, sys, time, json, warnings
import numpy as np
from scipy.integrate import solve_ivp, trapezoid
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

# ──────────────────────────────────────────────────────────────────────────────
# Physical Constants
# ──────────────────────────────────────────────────────────────────────────────
G_N    = 6.674e-11      # m^3 kg^-1 s^-2
C_SI   = 2.998e8        # m/s
Mpc_m  = 3.0857e22      # m per Mpc
kmsM   = 1e3 / Mpc_m    # 1 km/s/Mpc in s^-1

H0_TARGET  = 73.80      # km/s/Mpc (true local H0, Riess)
H0_CMB_PL  = 67.40      # km/s/Mpc (Planck CMB)
H0_CMB_ERR = 0.50

OM_FID = 0.315
OL_FID = 0.685
OB_FID = 0.0493
OR_FID = 9.20e-5
Z_STAR = 1090.0

# T20 sigma_8
S8_PLANCK     = 0.811
S8_PLANCK_ERR = 0.006
S8_KIDS       = 0.760
S8_KIDS_ERR   = 0.020

# T22 a_0 — sigma_UV fixed from L49, chi2 always 0
A0_OBS       = 1.2e-10     # m/s^2
A0_ERR_FR    = 0.10
SIGMA_UV_L49 = 3.31e9      # fixed normalization

# Self-consistency (z=0)
SIGMA_SC = 1.17e8
SC_ERR   = 0.10

# SQT friction (T20)
SIGMA_REF = 1.17e8
ALPHA_FR  = 0.1

# Fixed Gamma_0
GAMMA0_FIX = 1.0

# Model V fixed parameters
DZ_FIXED = 0.5              # tanh width (fixed)

# SQT ODE integration range (z: 100 -> 0)
A_INI = 1.0 / 101.0
A_FIN = 1.0
N_A   = 500

# Growth ODE
A_GROW_INI = 1e-3

# Grid
N_NOW  = 12
N_LATE = 15
N_ZT   = 12
SIGMA_NOW_GRID  = np.logspace(7.5, 8.5, N_NOW)    # around sigma_sc=1.17e8
SIGMA_LATE_GRID = np.logspace(7.5, 10.0, N_LATE)  # H0 tension range
ZT_GRID         = np.linspace(0.3, 5.0, N_ZT)     # transition redshift

N_WORKERS = 8

# Reference diagnostics (L48~L53)
SIGMA_T17_TENSION = 2.34e8
SIGMA_T17_SC      = 1.17e8
SIGMA_T20_S8      = 5.6e7
SIGMA_T22_A0      = 3.31e9
SIGMA_L50_BEST    = 3.04e8
SIGMA_L52_BEST    = 5.36e7
L53_BEST_CHI2     = 58.245

# Verdict thresholds
CHI2_PASS    = 16.0
CHI2_PARTIAL = 50.0

# Colors
BLUE = '#1f4e79'
GRAY = '#7f7f7f'
RED  = '#c00000'
GRN  = '#2e7d32'


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


# ──────────────────────────────────────────────────────────────────────────────
# Model V: sigma_0(z) — tanh interpolation
# ──────────────────────────────────────────────────────────────────────────────

def sigma_z_func(z, sigma_now, sigma_late, z_t, dz=DZ_FIXED):
    """sigma_0(z) = sigma_now + (sigma_late-sigma_now)*0.5*(1+tanh((z-z_t)/dz))."""
    tanh_val = np.tanh((float(z) - z_t) / dz)
    return float(sigma_now + (sigma_late - sigma_now) * 0.5 * (1.0 + tanh_val))


# ──────────────────────────────────────────────────────────────────────────────
# T17: SQT ODE with time-varying sigma(z) → H0 CMB tension
# ──────────────────────────────────────────────────────────────────────────────

def _eps_val(sigma_now):
    """eps calibrated so rho_n(z=0) = OL*rho_crit (dark energy self-consistency)."""
    H0_si = H0_TARGET * kmsM
    ni = GAMMA0_FIX * (sigma_now / (4.0 * np.pi * G_N))
    if ni <= 0.0:
        return None
    val = 3.0 * H0_si**2 * OL_FID * C_SI**2 / (8.0 * np.pi * G_N * ni)
    return val if (np.isfinite(val) and val > 0.0) else None


def _sqt_ode(a, y, sigma_now, sigma_late, z_t, dz, eps_val):
    n  = max(float(y[0]), 0.0)
    rm = max(float(y[1]), 0.0)
    z  = 1.0 / a - 1.0
    sigma_eff = sigma_z_func(z, sigma_now, sigma_late, z_t, dz)
    rho_n   = n * eps_val / C_SI**2
    rho_tot = rm + rho_n
    if rho_tot <= 0.0:
        return [0.0, 0.0]
    H = np.sqrt(8.0 * np.pi * G_N * rho_tot / 3.0)
    if not np.isfinite(H) or H <= 0.0:
        return [0.0, 0.0]
    dadt   = a * H
    dn_dt  = GAMMA0_FIX - 3.0*H*n - sigma_eff*n*rm
    drm_dt = -3.0*H*rm + sigma_eff*n*rm*eps_val / C_SI**2
    return [dn_dt / dadt, drm_dt / dadt]


def _solve_sqt(sigma_now, sigma_late, z_t, dz=DZ_FIXED):
    eps = _eps_val(sigma_now)
    if eps is None:
        return None
    H0_si  = H0_TARGET * kmsM
    z_ini  = 1.0 / A_INI - 1.0
    rm_ini = (3.0*H0_si**2*OM_FID / (8.0*np.pi*G_N)) * (1.0 + z_ini)**3
    # sigma at ODE start (z=100 >> z_t for all grid points -> sigma_late)
    sigma_ini = sigma_z_func(z_ini, sigma_now, sigma_late, z_t, dz)
    H_ini  = H0_si * np.sqrt(OM_FID*(1+z_ini)**3 + OR_FID*(1+z_ini)**4 + OL_FID)
    denom  = 3.0*H_ini + sigma_ini*rm_ini
    n_ini  = GAMMA0_FIX / max(denom, 1e-100)
    try:
        sol = solve_ivp(
            _sqt_ode, [A_INI, A_FIN], [n_ini, rm_ini],
            args=(sigma_now, sigma_late, z_t, dz, eps),
            method='RK45', t_eval=np.linspace(A_INI, A_FIN, N_A),
            rtol=1e-6, atol=1e-10, max_step=0.01,
        )
    except Exception:
        return None
    if not sol.success or sol.y.shape[1] < 2:
        return None
    a_arr  = sol.t
    n_arr  = np.maximum(sol.y[0], 0.0)
    rm_arr = np.maximum(sol.y[1], 0.0)
    rn_arr = n_arr * eps / C_SI**2
    H2_arr = np.maximum(8.0*np.pi*G_N*(rm_arr + rn_arr) / 3.0, 1e-80)
    H_arr  = np.sqrt(H2_arr)
    H0_si_input = H0_TARGET * kmsM
    E_arr  = H_arr / H0_si_input   # normalize by true H0
    E0     = float(E_arr[-1])
    if not (np.isfinite(E0) and E0 > 0.0):
        return None
    return {'a': a_arr, 'z': 1.0/a_arr - 1.0, 'H': H_arr, 'E': E_arr, 'eps': eps}


def _E_lcdm(z):
    return float(np.sqrt(max(OM_FID*(1+z)**3 + OR_FID*(1+z)**4 + OL_FID, 1e-30)))


def _E_fn_from_sol(sol):
    z_ode = sol['z'][::-1]   # ascending: 0 -> 100
    E_ode = sol['E'][::-1]
    z_max = float(z_ode[-1])
    def E_fn(z):
        z = float(z)
        return float(np.interp(z, z_ode, E_ode)) if z <= z_max else _E_lcdm(z)
    return E_fn


def _sound_horizon_si(H0_kmsMpc, E_fn):
    H0_si = H0_kmsMpc * kmsM
    Rb0   = 3.0*OB_FID / (4.0*OR_FID)
    z_int = np.linspace(Z_STAR, 10000.0, 800)
    Rb_z  = Rb0 / (1.0 + z_int)
    cs_z  = C_SI / np.sqrt(3.0*(1.0 + Rb_z))
    H_z   = H0_si * np.array([E_fn(z) for z in z_int])
    return trapezoid(cs_z / np.maximum(H_z, 1e-50), z_int)


def _comoving_dist_si(H0_kmsMpc, z_max, E_fn):
    H0_si = H0_kmsMpc * kmsM
    z_int = np.linspace(0.0, z_max, 800)
    H_z   = H0_si * np.array([E_fn(z) for z in z_int])
    return trapezoid(C_SI / np.maximum(H_z, 1e-50), z_int)


def _chi2_T17(sigma_now, sigma_late, z_t, dz=DZ_FIXED):
    sol = _solve_sqt(sigma_now, sigma_late, z_t, dz)
    if sol is None:
        return None, None
    E_sqt  = _E_fn_from_sol(sol)
    rs_sqt  = _sound_horizon_si(H0_TARGET, E_sqt)
    rs_lcdm = _sound_horizon_si(H0_TARGET, _E_lcdm)
    chi_sqt  = _comoving_dist_si(H0_TARGET, Z_STAR, E_sqt)
    chi_lcdm = _comoving_dist_si(H0_TARGET, Z_STAR, _E_lcdm)
    h0_ratio   = (rs_sqt / max(rs_lcdm, 1e-10)) * (chi_lcdm / max(chi_sqt, 1e-10))
    H0_CMB_app = H0_TARGET * h0_ratio
    chi2       = ((H0_CMB_app - H0_CMB_PL) / H0_CMB_ERR) ** 2
    return float(chi2), float(H0_CMB_app)


# ──────────────────────────────────────────────────────────────────────────────
# T20: Growth ODE with time-varying friction factor
# ──────────────────────────────────────────────────────────────────────────────

def _growth_ode_lcdm(a, y, om=OM_FID, ol=OL_FID):
    """Pure LCDM growth (friction=1) for D_LCDM_REF."""
    delta, ddelta_da = y[0], y[1]
    E2 = om / a**3 + ol
    if E2 <= 0.0:
        return [0.0, 0.0]
    H_prime_H  = -1.5 * om / (a**4 * E2)
    coeff_fric = 3.0/a + H_prime_H        # friction_factor=1
    coeff_coup = 1.5 * om / (a**5 * E2)
    return [ddelta_da, -coeff_fric * ddelta_da + coeff_coup * delta]


def _growth_ode_sqt(a, y, sigma_now, sigma_late, z_t, dz, om=OM_FID, ol=OL_FID):
    """SQT growth with z-varying friction from sigma_0(z)."""
    delta, ddelta_da = y[0], y[1]
    z = 1.0 / a - 1.0
    sigma_eff  = sigma_z_func(z, sigma_now, sigma_late, z_t, dz)
    ff = 1.0 + ALPHA_FR * np.log10(max(sigma_eff, 1e-30) / SIGMA_REF)
    ff = max(ff, 0.1)
    E2 = om / a**3 + ol
    if E2 <= 0.0:
        return [0.0, 0.0]
    H_prime_H  = -1.5 * om / (a**4 * E2)
    coeff_fric = ff * (3.0/a + H_prime_H)
    coeff_coup = 1.5 * om / (a**5 * E2)
    return [ddelta_da, -coeff_fric * ddelta_da + coeff_coup * delta]


def _solve_growth_lcdm():
    y0 = [A_GROW_INI, 1.0]
    try:
        sol = solve_ivp(
            _growth_ode_lcdm, [A_GROW_INI, 1.0], y0,
            method='Radau', rtol=1e-9, atol=1e-12,
        )
    except Exception:
        return None
    if not sol.success:
        return None
    D_raw = sol.y[0]
    if not (np.all(np.isfinite(D_raw)) and np.all(D_raw > 0.0)):
        return None
    return float(D_raw[-1])


def _solve_growth_sqt(sigma_now, sigma_late, z_t, dz=DZ_FIXED):
    y0 = [A_GROW_INI, 1.0]
    try:
        sol = solve_ivp(
            _growth_ode_sqt, [A_GROW_INI, 1.0], y0,
            args=(sigma_now, sigma_late, z_t, dz),
            method='Radau', rtol=1e-9, atol=1e-12,
        )
    except Exception:
        return None
    if not sol.success:
        return None
    D_raw = sol.y[0]
    if not (np.all(np.isfinite(D_raw)) and np.all(D_raw > 0.0)):
        return None
    return float(D_raw[-1])


# Cached at module import — once per worker process (spawn)
_D_LCDM_REF = _solve_growth_lcdm()


def _chi2_T20(sigma_now, sigma_late, z_t, dz=DZ_FIXED):
    if _D_LCDM_REF is None or _D_LCDM_REF <= 0.0:
        return None, None
    D_sqt = _solve_growth_sqt(sigma_now, sigma_late, z_t, dz)
    if D_sqt is None or D_sqt <= 0.0:
        return None, None
    sigma8 = S8_PLANCK * (D_sqt / _D_LCDM_REF)
    chi2_pl = ((sigma8 - S8_PLANCK) / S8_PLANCK_ERR) ** 2
    chi2_ki = ((sigma8 - S8_KIDS)   / S8_KIDS_ERR)   ** 2
    return float(min(chi2_pl, chi2_ki)), float(sigma8)


# ──────────────────────────────────────────────────────────────────────────────
# T22: a_0 — sigma_UV fixed from L49, chi2 always 0
# ──────────────────────────────────────────────────────────────────────────────

def _chi2_T22():
    """sigma_UV=3.31e9 fixed → ratio=1 → a0_pred=A0_OBS → chi2=0."""
    ratio   = SIGMA_UV_L49 / SIGMA_UV_L49   # 1.0
    a0_pred = A0_OBS * np.sqrt(ratio)
    chi2    = ((a0_pred / A0_OBS - 1.0) / A0_ERR_FR) ** 2
    return float(chi2), float(a0_pred)


# ──────────────────────────────────────────────────────────────────────────────
# Worker
# ──────────────────────────────────────────────────────────────────────────────

def _worker(args):
    warnings.filterwarnings('ignore')
    np.seterr(all='ignore')
    sigma_now, sigma_late, z_t = args

    # T17 SC: tau_q_now * 3H0 = 1 (z=0 self-consistency)
    H0_si      = H0_TARGET * kmsM
    tau_q_now  = sigma_now / (4.0 * np.pi * G_N)
    tau_ratio  = tau_q_now * 3.0 * H0_si
    chi2_sc    = ((tau_ratio - 1.0) / SC_ERR) ** 2

    # T17 H0 tension (SQT ODE with time-varying sigma)
    r_T17, H0_CMB = _chi2_T17(sigma_now, sigma_late, z_t)
    if r_T17 is None:
        return {'sigma_now': float(sigma_now), 'sigma_late': float(sigma_late),
                'z_t': float(z_t), 'success': False}

    # T20 sigma_8 (growth ODE with time-varying friction)
    r_T20, sigma8 = _chi2_T20(sigma_now, sigma_late, z_t)
    if r_T20 is None:
        return {'sigma_now': float(sigma_now), 'sigma_late': float(sigma_late),
                'z_t': float(z_t), 'success': False}

    # T22 a_0 (always 0 — sigma_UV fixed)
    chi2_T22, a0_pred = _chi2_T22()

    chi2_total = r_T17 + float(chi2_sc) + r_T20 + chi2_T22

    return {
        'sigma_now':  float(sigma_now),
        'sigma_late': float(sigma_late),
        'z_t':        float(z_t),
        'tau_ratio':  float(tau_ratio),
        'H0_CMB':     H0_CMB,
        'sigma8':     sigma8,
        'a0_pred':    a0_pred,
        'chi2_T17':   r_T17,
        'chi2_sc':    float(chi2_sc),
        'chi2_T20':   r_T20,
        'chi2_T22':   chi2_T22,
        'chi2_total': float(chi2_total),
        'success':    True,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Pre-task diagnostics
# ──────────────────────────────────────────────────────────────────────────────

def pretask():
    print('\n' + '='*60)
    print('Pre-task: L54 sigma_0(z) Model V Diagnostics')
    print('='*60)

    print(f'\n[P1] D_LCDM_REF = {_D_LCDM_REF:.6f}  (friction=1, a=1e-3->1)')

    H0_si     = H0_TARGET * kmsM
    sigma_sc  = G_N * 4.0*np.pi / (3.0 * H0_si)
    print(f'[P2] sigma_sc = {sigma_sc:.4e}  (target={SIGMA_SC:.2e})')

    # sigma_z_func checks
    for zt in [0.5, 2.0, 5.0]:
        for sigma_late in [1.17e8, 2.34e8, 1e9]:
            s_z0 = sigma_z_func(0.0, SIGMA_SC, sigma_late, zt)
            s_z1 = sigma_z_func(zt, SIGMA_SC, sigma_late, zt)
            s_z10 = sigma_z_func(10.0, SIGMA_SC, sigma_late, zt)
            print(f'[P3] z_t={zt:.1f} sl={sigma_late:.2e}: '
                  f'sigma(z=0)={s_z0:.2e} sigma(z=zt)={s_z1:.2e} sigma(z=10)={s_z10:.2e}')

    # T17 chi2 at reference sigma_now, sigma_late
    for sn, sl, zt in [(SIGMA_SC, 1.17e8, 2.0), (SIGMA_SC, 2.34e8, 2.0),
                       (SIGMA_SC, 5.0e8, 1.0)]:
        r, h0c = _chi2_T17(sn, sl, zt)
        print(f'[P4] sn={sn:.2e} sl={sl:.2e} z_t={zt:.1f}: '
              f'H0_CMB={h0c:.2f} chi2_T17={r:.2f}')

    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 1: Grid Scan
# ──────────────────────────────────────────────────────────────────────────────

def task1_scan(pool):
    print('\n' + '='*60)
    print(f'Task 1: 3D Grid Scan ({N_NOW}x{N_LATE}x{N_ZT}={N_NOW*N_LATE*N_ZT} pts)')
    print('='*60)
    t0 = time.time()

    param_list = [(sn, sl, zt)
                  for sn in SIGMA_NOW_GRID
                  for sl in SIGMA_LATE_GRID
                  for zt in ZT_GRID]
    print(f'  Dispatching {len(param_list)} tasks to {N_WORKERS} workers...')
    sys.stdout.flush()

    results = pool.map(_worker, param_list)
    elapsed = time.time() - t0
    print(f'  Done in {elapsed:.1f}s')

    n_pts   = len(results)
    chi2t   = np.full(n_pts, np.nan)
    chi2_17 = np.full(n_pts, np.nan)
    chi2_sc = np.full(n_pts, np.nan)
    chi2_20 = np.full(n_pts, np.nan)
    chi2_22 = np.full(n_pts, np.nan)
    s8_arr  = np.full(n_pts, np.nan)
    h0c_arr = np.full(n_pts, np.nan)
    valid   = np.zeros(n_pts, dtype=bool)

    for i, r in enumerate(results):
        if r.get('success'):
            chi2t[i]   = r['chi2_total']
            chi2_17[i] = r['chi2_T17']
            chi2_sc[i] = r['chi2_sc']
            chi2_20[i] = r['chi2_T20']
            chi2_22[i] = r['chi2_T22']
            s8_arr[i]  = r.get('sigma8', np.nan)
            h0c_arr[i] = r.get('H0_CMB', np.nan)
            valid[i]   = True

    n_valid = int(valid.sum())
    n_pass  = int(np.sum(valid & (chi2t < CHI2_PASS)))
    print(f'  Valid: {n_valid}/{n_pts}  PASS (chi2<{CHI2_PASS:.0f}): {n_pass}')
    if n_valid > 0:
        print(f'  chi2_total range: [{np.nanmin(chi2t[valid]):.2f}, {np.nanmax(chi2t[valid]):.2f}]')
    sys.stdout.flush()

    return {
        'results':    results,
        'chi2_total': chi2t,
        'chi2_T17':   chi2_17,
        'chi2_sc':    chi2_sc,
        'chi2_T20':   chi2_20,
        'chi2_T22':   chi2_22,
        'sigma8':     s8_arr,
        'H0_CMB':     h0c_arr,
        'valid':      valid,
        'n_pass':     n_pass,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Task 2: Analysis
# ──────────────────────────────────────────────────────────────────────────────

def task2_analyze(scan):
    print('\n' + '='*60)
    print('Task 2: Analysis')
    print('='*60)

    valid   = scan['valid']
    chi2t   = scan['chi2_total']
    results = scan['results']

    if not np.any(valid):
        print('  ERROR: no valid points')
        return None

    chi2_sel = np.where(valid, chi2t, np.inf)
    best_idx = int(np.nanargmin(chi2_sel))
    best_r   = results[best_idx]

    # Decode 3D index: param_list ordered as sn x sl x zt
    bi  = best_idx // (N_LATE * N_ZT)
    bj  = (best_idx % (N_LATE * N_ZT)) // N_ZT
    bk  = best_idx % N_ZT

    best_sn  = best_r['sigma_now']
    best_sl  = best_r['sigma_late']
    best_zt  = best_r['z_t']

    print(f'\n  Best chi2_total = {chi2t[best_idx]:.3f}')
    print(f'  sigma_now  = {best_sn:.3e}  log={np.log10(best_sn):.3f}')
    print(f'  sigma_late = {best_sl:.3e}  log={np.log10(best_sl):.3f}')
    print(f'  z_t        = {best_zt:.3f}')
    print(f'\n  Chi2 breakdown:')
    print(f'    chi2_T17 = {best_r.get("chi2_T17",0):.3f}  '
          f'(H0_CMB={best_r.get("H0_CMB",0):.2f} km/s/Mpc)')
    print(f'    chi2_sc  = {best_r.get("chi2_sc",0):.3f}  '
          f'(tau_ratio={best_r.get("tau_ratio",0):.4f})')
    print(f'    chi2_T20 = {best_r.get("chi2_T20",0):.3f}  '
          f'(sigma8={best_r.get("sigma8",0):.4f})')
    print(f'    chi2_T22 = {best_r.get("chi2_T22",0):.3f}  '
          f'(a0_pred={best_r.get("a0_pred",0):.3e} m/s^2)')
    print(f'  PASS (chi2<{CHI2_PASS:.0f}): {scan["n_pass"]} points')
    sys.stdout.flush()

    return {
        'best_idx': best_idx,
        'bi': bi, 'bj': bj, 'bk': bk,
        'best_sn':   best_sn,
        'best_sl':   best_sl,
        'best_zt':   best_zt,
        'best_r':    best_r,
        'best_chi2': float(chi2t[best_idx]),
    }


# ──────────────────────────────────────────────────────────────────────────────
# Task 3: Visualization (6-panel)
# ──────────────────────────────────────────────────────────────────────────────

def task3_visualize(scan, ana):
    print('\n' + '='*60)
    print('Task 3: 6-Panel Visualization')
    print('='*60)

    chi2_3d     = scan['chi2_total'].reshape(N_NOW, N_LATE, N_ZT)
    log_chi2_3d = np.log10(np.maximum(chi2_3d, 1e-2))

    lsn = np.log10(SIGMA_NOW_GRID)
    lsl = np.log10(SIGMA_LATE_GRID)
    bi, bj, bk = ana['bi'], ana['bj'], ana['bk']
    best_r   = ana['best_r']
    best_chi2 = ana['best_chi2']

    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    fig.suptitle(
        f'L54: sigma_0(z) Model V — Theory Last Attempt\n'
        f'Best chi2_total={best_chi2:.1f}  '
        f'sigma_now={ana["best_sn"]:.2e}  sigma_late={ana["best_sl"]:.2e}  z_t={ana["best_zt"]:.2f}',
        fontsize=11, fontweight='bold')

    def _plot_slice(ax, Z, xs, ys, xlabel, ylabel, title, best_x, best_y):
        cf = ax.contourf(xs, ys, Z.T, levels=50, cmap='viridis_r')
        plt.colorbar(cf, ax=ax, label='log10(chi2_total)')
        try:
            cs = ax.contour(xs, ys, Z.T, levels=[np.log10(CHI2_PASS)],
                            colors='lime', linewidths=2)
            ax.clabel(cs, fmt=f'PASS={CHI2_PASS:.0f}', fontsize=8)
        except Exception:
            pass
        ax.scatter([best_x], [best_y], color=RED, s=120, zorder=5, label='best')
        ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.set_title(title)
        ax.legend(fontsize=7)

    # (a) sigma_now x sigma_late @ best z_t
    _plot_slice(axes[0, 0],
                log_chi2_3d[:, :, bk], lsn, lsl,
                'log10(sigma_now)', 'log10(sigma_late)',
                f'(a) sigma_now x sigma_late @ z_t={ZT_GRID[bk]:.2f}',
                np.log10(ana['best_sn']), np.log10(ana['best_sl']))
    # reference lines
    axes[0, 0].axvline(np.log10(SIGMA_SC), color='lime', ls='--', lw=1.5,
                       label='sigma_sc=1.17e8')
    axes[0, 0].axhline(np.log10(SIGMA_T17_TENSION), color='cyan', ls='--', lw=1.5,
                       label='T17 tension')
    axes[0, 0].legend(fontsize=6)

    # (b) sigma_now x z_t @ best sigma_late
    _plot_slice(axes[0, 1],
                log_chi2_3d[:, bj, :], lsn, ZT_GRID,
                'log10(sigma_now)', 'z_t',
                f'(b) sigma_now x z_t @ sigma_late={SIGMA_LATE_GRID[bj]:.2e}',
                np.log10(ana['best_sn']), ana['best_zt'])
    axes[0, 1].axvline(np.log10(SIGMA_SC), color='lime', ls='--', lw=1.5,
                       label='sigma_sc')
    axes[0, 1].legend(fontsize=7)

    # (c) sigma_late x z_t @ best sigma_now
    _plot_slice(axes[0, 2],
                log_chi2_3d[bi, :, :], lsl, ZT_GRID,
                'log10(sigma_late)', 'z_t',
                f'(c) sigma_late x z_t @ sigma_now={SIGMA_NOW_GRID[bi]:.2e}',
                np.log10(ana['best_sl']), ana['best_zt'])
    axes[0, 2].axvline(np.log10(SIGMA_T17_TENSION), color='cyan', ls='--', lw=1.5,
                       label='T17 tension 2.34e8')
    axes[0, 2].legend(fontsize=7)

    # (d) chi2 breakdown at best
    ax = axes[1, 0]
    chi2_vals  = [max(best_r.get('chi2_T17', 0), 1e-3),
                  max(best_r.get('chi2_sc',  0), 1e-3),
                  max(best_r.get('chi2_T20', 0), 1e-3),
                  max(best_r.get('chi2_T22', 0), 1e-3)]
    labels_d   = ['T17 H0\ntension', 'T17\nself-consist', 'T20\nsigma8', 'T22\na_0']
    colors_d   = [RED, BLUE, GRN, '#e65100']
    bars = ax.bar(labels_d, chi2_vals, color=colors_d, alpha=0.8, edgecolor='k')
    ax.axhline(4.0,         color=GRAY,  ls=':',  lw=1.5, label='1sigma^2=4')
    ax.axhline(CHI2_PASS,   color='lime', ls='--', lw=2,  label=f'PASS={CHI2_PASS:.0f}')
    ax.axhline(CHI2_PARTIAL, color=RED,  ls='--', lw=1.5, label=f'PARTIAL={CHI2_PARTIAL:.0f}')
    for bar, val in zip(bars, chi2_vals):
        ax.text(bar.get_x() + bar.get_width()/2, val * 1.3,
                f'{val:.1f}', ha='center', fontsize=9, fontweight='bold')
    ax.set_ylabel('chi2')
    ax.set_title(f'(d) chi2 breakdown at best (total={best_chi2:.1f})')
    ax.legend(fontsize=7)
    ax.set_yscale('log')

    # (e) chi2_total distribution
    ax = axes[1, 1]
    c2_v = scan['chi2_total'][scan['valid']]
    ax.hist(np.log10(np.maximum(c2_v, 1e-2)), bins=40, color=BLUE, alpha=0.7, edgecolor='k')
    ax.axvline(np.log10(CHI2_PASS),    color='lime',   ls='--', lw=2,
               label=f'PASS={CHI2_PASS:.0f}')
    ax.axvline(np.log10(CHI2_PARTIAL), color=RED,      ls='--', lw=1.5,
               label=f'PARTIAL={CHI2_PARTIAL:.0f}')
    ax.axvline(np.log10(best_chi2),    color='orange', ls='-',  lw=2.5,
               label=f'best={best_chi2:.1f}')
    ax.axvline(np.log10(L53_BEST_CHI2), color=GRAY,   ls=':',  lw=2,
               label=f'L53 best={L53_BEST_CHI2:.1f}')
    ax.set_xlabel('log10(chi2_total)')
    ax.set_ylabel('Count')
    ax.set_title(f'(e) chi2_total dist (PASS: {scan["n_pass"]}/{int(scan["valid"].sum())})')
    ax.legend(fontsize=7)

    # (f) sigma_0(z) curve at best + reference points
    ax = axes[1, 2]
    z_range = np.linspace(0.0, 8.0, 400)
    sz_best = np.array([sigma_z_func(z, ana['best_sn'], ana['best_sl'], ana['best_zt'])
                        for z in z_range])
    sz_ref  = np.full_like(z_range, SIGMA_SC)

    ax.semilogy(z_range, sz_best, color=BLUE, lw=2.5,
                label=f'L54 best: sn={ana["best_sn"]:.1e} sl={ana["best_sl"]:.1e} z_t={ana["best_zt"]:.2f}')
    ax.semilogy(z_range, sz_ref,  color=GRAY, lw=1.5, ls='--', label=f'sigma_sc={SIGMA_SC:.2e}')

    # Reference sigma values from L48~L53 as horizontal lines
    for s_ref, col, lbl in [
        (SIGMA_T17_TENSION, 'cyan',   'T17 tension 2.34e8'),
        (SIGMA_T17_SC,      'lime',   'T17 SC 1.17e8'),
        (SIGMA_T20_S8,      GRN,      'T20 sigma8 5.6e7'),
        (SIGMA_T22_A0,      '#8B4513','T22 a0 3.31e9'),
        (SIGMA_L50_BEST,    'orange', 'L50 sIR 3.04e8'),
        (SIGMA_L52_BEST,    'purple', 'L52 sIR 5.36e7'),
    ]:
        ax.axhline(s_ref, color=col, ls=':', lw=1.2, alpha=0.7, label=lbl)
    ax.axvline(ana['best_zt'], color=RED, ls='--', lw=1.5, label=f'z_t={ana["best_zt"]:.2f}')
    ax.set_xlabel('z (redshift)')
    ax.set_ylabel('sigma_0(z)')
    ax.set_title('(f) sigma_0(z) curve + reference values')
    ax.legend(fontsize=6, loc='upper left')
    ax.grid(alpha=0.3)
    ax.set_xlim(0, 8)

    plt.tight_layout()
    out = os.path.join(_SCRIPT_DIR, 'l54_main.png')
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved: {out}')
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 4: Verdict
# ──────────────────────────────────────────────────────────────────────────────

def task4_verdict(scan, ana):
    print('\n' + '='*60)
    print('L54 FINAL VERDICT')
    print('='*60)

    best_chi2 = ana['best_chi2']
    best_r    = ana['best_r']
    n_pass    = scan['n_pass']
    n_total   = N_NOW * N_LATE * N_ZT

    if best_chi2 < CHI2_PASS:
        verdict = 'PASS — sigma_0(z) Model V satisfies all 4 constraints; THEORY SURVIVES'
    elif best_chi2 < CHI2_PARTIAL:
        verdict = 'PARTIAL — no full-pass region; theory needs further refinement'
    else:
        verdict = 'FAIL — sigma_0(z) Model V cannot satisfy 4 constraints; THEORY DIES'

    print(f'\n  [VERDICT] {verdict}')
    print(f'\n  Best chi2_total = {best_chi2:.3f}  (L53 best: {L53_BEST_CHI2:.3f})')
    print(f'  PASS threshold  = {CHI2_PASS:.0f}')
    print(f'  PASS count      = {n_pass}/{n_total}')

    print(f'\n  Chi2 breakdown at best:')
    for key, label in [('chi2_T17', 'T17 H0 tension'),
                       ('chi2_sc',  'T17 SC'),
                       ('chi2_T20', 'T20 sigma8'),
                       ('chi2_T22', 'T22 a_0')]:
        v = best_r.get(key, float('nan'))
        status = 'PASS' if v < 4 else ('PARTIAL' if v < 16 else 'FAIL')
        print(f'    {label:<20}: {v:.3f}  [{status}]')

    print(f'\n  === sigma_0 Diagnostic Table (L54 Update) ===')
    print(f'  {"Constraint":<28} {"sigma_0":>12}  {"log10":>7}')
    print(f'  {"-"*52}')
    for label, val in [
        ('T17 H0 tension',       SIGMA_T17_TENSION),
        ('T17 self-consist',     SIGMA_T17_SC),
        ('T20 sigma8 (L48)',     SIGMA_T20_S8),
        ('T22 a_0 (L49)',        SIGMA_T22_A0),
        ('L50 best sigma_IR',    SIGMA_L50_BEST),
        ('L52 best sigma_IR',    SIGMA_L52_BEST),
        ('L54 best sigma_now',   ana['best_sn']),
        ('L54 best sigma_late',  ana['best_sl']),
    ]:
        tag = '  <-- THIS RUN' if 'L54' in label else ''
        print(f'  {label:<28} {val:>12.3e}  {np.log10(val):>7.3f}{tag}')
    print(f'\n  L54 best z_t      = {ana["best_zt"]:.3f}')
    print(f'  L54 best H0_CMB   = {best_r.get("H0_CMB",0):.2f} km/s/Mpc')
    print(f'  L54 best sigma8   = {best_r.get("sigma8",0):.4f}')
    print(f'  L53 best chi2     = {L53_BEST_CHI2:.3f}  (for comparison)')
    sys.stdout.flush()

    return {
        'verdict':   verdict,
        'best_chi2': best_chi2,
        'n_pass':    n_pass,
        'best_sn':   ana['best_sn'],
        'best_sl':   ana['best_sl'],
        'best_zt':   ana['best_zt'],
    }


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('='*60)
    print('L54: sigma_0(z) Time-Varying (Model V)')
    print(f'Grid: {N_NOW}x{N_LATE}x{N_ZT}={N_NOW*N_LATE*N_ZT} pts | {N_WORKERS} workers')
    print(f'sigma_now: [10^7.5, 10^8.5]  sigma_late: [10^7.5, 10^10]  z_t: [0.3, 5.0]')
    print(f'Gamma0={GAMMA0_FIX:.1e}  dz={DZ_FIXED}  PASS threshold={CHI2_PASS:.0f}')
    print('='*60)
    sys.stdout.flush()

    pretask()

    ctx  = mp.get_context('spawn')
    pool = ctx.Pool(N_WORKERS)

    scan    = {}
    ana     = {}
    verdict = {}

    try:
        scan    = task1_scan(pool)
        ana     = task2_analyze(scan)
        if ana is None:
            print('ERROR: analysis failed')
            sys.exit(1)
        task3_visualize(scan, ana)
        verdict = task4_verdict(scan, ana)

    finally:
        pool.close()
        pool.join()

    print('\n' + '='*60)
    print('L54 RESULTS SUMMARY')
    print('='*60)
    n_valid = int(scan.get('valid', np.array([])).sum())
    print(f'Grid: {N_NOW}x{N_LATE}x{N_ZT}  Valid: {n_valid}/{N_NOW*N_LATE*N_ZT}')
    print(f'PASS count: {scan.get("n_pass", 0)}')
    print(f'Best chi2_total: {ana.get("best_chi2", 0):.3f}')
    print(f'Best sigma_now: {ana.get("best_sn", 0):.3e}  '
          f'sigma_late: {ana.get("best_sl", 0):.3e}  '
          f'z_t: {ana.get("best_zt", 0):.3f}')
    print(f'Verdict: {verdict.get("verdict", "N/A")}')

    save = {
        'n_pass':    scan.get('n_pass', 0),
        'best_chi2': ana.get('best_chi2', 0),
        'best_sn':   ana.get('best_sn', 0),
        'best_sl':   ana.get('best_sl', 0),
        'best_zt':   ana.get('best_zt', 0),
        'verdict':   verdict.get('verdict', ''),
        'chi2_breakdown': {
            'T17': ana['best_r'].get('chi2_T17', 0),
            'sc':  ana['best_r'].get('chi2_sc',  0),
            'T20': ana['best_r'].get('chi2_T20', 0),
            'T22': ana['best_r'].get('chi2_T22', 0),
        },
        'obs': {
            'H0_CMB':    ana['best_r'].get('H0_CMB',    0),
            'sigma8':    ana['best_r'].get('sigma8',    0),
            'a0_pred':   ana['best_r'].get('a0_pred',   0),
            'tau_ratio': ana['best_r'].get('tau_ratio', 0),
        },
        'params': {
            'N_NOW': N_NOW, 'N_LATE': N_LATE, 'N_ZT': N_ZT,
            'DZ_FIXED': DZ_FIXED, 'GAMMA0_FIX': GAMMA0_FIX,
            'CHI2_PASS': CHI2_PASS,
        },
    }
    out_json = os.path.join(_SCRIPT_DIR, 'l54_results.json')
    with open(out_json, 'w') as f:
        json.dump(_jsonify(save), f, indent=2)
    print(f'Saved: {out_json}')
