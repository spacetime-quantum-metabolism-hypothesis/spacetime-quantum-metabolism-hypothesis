#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L53: Integrated Self-Consistency (3D Grid)
==========================================
Single (sigma_IR, sigma_UV, k_t) satisfying 4 constraints simultaneously?
T17 H0 tension + T17 SC + T20 sigma_8 + T22 a_0
Grid: 15x15x15 = 3375 pts, 8 workers
Output: l53_main.png, l53_results.json
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

H0_TARGET = 73.80       # km/s/Mpc (true H0 input)
H0_CMB_PL = 67.40       # km/s/Mpc (Planck)
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

# T22 a_0
A0_OBS     = 1.2e-10    # m/s^2
A0_ERR_FR  = 0.10       # fractional error
SIGMA_UV_L49 = 3.31e9   # L49 T22 normalization

# Self-consistency
SIGMA_SC  = 1.17e8      # m^3/(kg*s)
SC_ERR    = 0.10        # fractional tolerance

# SQT friction (T20)
SIGMA_REF = 1.17e8
ALPHA_FR  = 0.1

# Evaluation k-scales
K_HORIZON = 1e-4        # Mpc^-1 (T17)
K_SIGMA8  = 0.13        # Mpc^-1 (T20)
K_GALAXY  = 100.0       # Mpc^-1 (T22)

# Fixed Gamma_0 (H_0_CMB insensitive to it — L48)
GAMMA0_FIX = 1.0        # m^-3 s^-1

# ODE integration
A_INI = 1.0 / 101.0
A_FIN = 1.0
N_A   = 500

# Growth ODE
A_GROW_INI = 1e-3

# Grid
N_SIG = 15
N_UV  = 15
N_KT  = 15
SIGMA_IR_GRID = np.logspace(7.0, 9.5, N_SIG)
SIGMA_UV_GRID = np.logspace(8.0, 10.0, N_UV)
KT_GRID       = np.logspace(-4.0, 1.0,  N_KT)
N_WORKERS = 8

# Reference diagnostics
SIGMA_T17_TENSION = 2.34e8
SIGMA_T17_SC      = 1.17e8
SIGMA_T20_S8      = 5.6e7
SIGMA_T22_A0      = 3.31e9
SIGMA_L50_BEST    = 3.04e8
SIGMA_L52_BEST    = 5.36e7

# Pass threshold
CHI2_PASS    = 16.0
CHI2_PARTIAL = 50.0


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
# sigma_0(k) Lorentzian (Model IV)
# ──────────────────────────────────────────────────────────────────────────────

def sigma_k(k_Mpc, sigma_IR, sigma_UV, k_t):
    x2 = (k_Mpc / k_t) ** 2
    return (sigma_IR + sigma_UV * x2) / (1.0 + x2)


# ──────────────────────────────────────────────────────────────────────────────
# T17: SQT ODE + H0 CMB tension (same as L50, sigma_eff_T17 replaces sigma_IR)
# ──────────────────────────────────────────────────────────────────────────────

def _eps_val(sigma_eff_T17, H0_kmsMpc=H0_TARGET):
    H0_si = H0_kmsMpc * kmsM
    ni = GAMMA0_FIX * (sigma_eff_T17 / (4.0 * np.pi * G_N))
    if ni <= 0.0:
        return None
    val = 3.0 * H0_si**2 * OL_FID * C_SI**2 / (8.0 * np.pi * G_N * ni)
    return val if (np.isfinite(val) and val > 0.0) else None


def _sqt_ode(a, y, sigma_eff_T17, eps_val):
    n, rho_m = max(float(y[0]), 0.0), max(float(y[1]), 0.0)
    rho_n   = n * eps_val / C_SI**2
    rho_tot = rho_m + rho_n
    if rho_tot <= 0.0:
        return [0.0, 0.0]
    H = np.sqrt(8.0 * np.pi * G_N * rho_tot / 3.0)
    if not np.isfinite(H) or H <= 0.0:
        return [0.0, 0.0]
    dadt = a * H
    dn_dt  = GAMMA0_FIX - 3.0*H*n  - sigma_eff_T17*n*rho_m
    drm_dt = -3.0*H*rho_m + sigma_eff_T17*n*rho_m*eps_val/C_SI**2
    return [dn_dt / dadt, drm_dt / dadt]


def _solve_sqt_T17(sigma_eff_T17):
    eps = _eps_val(sigma_eff_T17)
    if eps is None:
        return None
    H0_si  = H0_TARGET * kmsM
    z_ini  = 1.0/A_INI - 1.0
    rm_ini = (3.0*H0_si**2*OM_FID/(8.0*np.pi*G_N)) * (1.0+z_ini)**3
    H_ini  = H0_si * np.sqrt(OM_FID*(1+z_ini)**3 + OR_FID*(1+z_ini)**4 + OL_FID)
    denom  = 3.0*H_ini + sigma_eff_T17*rm_ini
    n_ini  = GAMMA0_FIX / max(denom, 1e-100)
    try:
        sol = solve_ivp(
            _sqt_ode, [A_INI, A_FIN], [n_ini, rm_ini],
            args=(sigma_eff_T17, eps),
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
    H2_arr = np.maximum(8.0*np.pi*G_N*(rm_arr+rn_arr)/3.0, 1e-80)
    H_arr  = np.sqrt(H2_arr)
    E_arr  = H_arr / H0_si
    E0     = float(E_arr[-1])
    if not (np.isfinite(E0) and E0 > 0.0):
        return None
    return {'a': a_arr, 'z': 1.0/a_arr - 1.0, 'H': H_arr, 'E': E_arr, 'E0': E0, 'eps': eps}


def _E_fn_from_sol(sol):
    z_ode = sol['z'][::-1]   # 0 -> 100
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


def _E_lcdm(z):
    return float(np.sqrt(max(OM_FID*(1+z)**3 + OR_FID*(1+z)**4 + OL_FID, 1e-30)))


def _chi2_T17(sigma_eff_T17):
    """Compute chi2 for H0 CMB tension using SQT ODE (same as L50)."""
    sol = _solve_sqt_T17(sigma_eff_T17)
    if sol is None:
        return None, None

    E_sqt  = _E_fn_from_sol(sol)
    E_lcdm = _E_lcdm

    rs_sqt   = _sound_horizon_si(H0_TARGET, E_sqt)
    rs_lcdm  = _sound_horizon_si(H0_TARGET, E_lcdm)
    chi_sqt  = _comoving_dist_si(H0_TARGET, Z_STAR, E_sqt)
    chi_lcdm = _comoving_dist_si(H0_TARGET, Z_STAR, E_lcdm)

    h0_ratio   = (rs_sqt / max(rs_lcdm, 1e-10)) * (chi_lcdm / max(chi_sqt, 1e-10))
    H0_CMB_app = H0_TARGET * h0_ratio
    chi2       = ((H0_CMB_app - H0_CMB_PL) / H0_CMB_ERR) ** 2
    return float(chi2), float(H0_CMB_app)


# ──────────────────────────────────────────────────────────────────────────────
# T20: Structure growth ODE (same as L52)
# ──────────────────────────────────────────────────────────────────────────────

def _growth_ode(a, y, friction_factor, om=OM_FID, ol=OL_FID):
    delta, ddelta_da = y[0], y[1]
    E2 = om / a**3 + ol
    if E2 <= 0.0:
        return [0.0, 0.0]
    H_prime_H  = -1.5 * om / (a**4 * E2)
    coeff_fric = friction_factor * (3.0/a + H_prime_H)
    coeff_coup = 1.5 * om / (a**5 * E2)
    return [ddelta_da,
            -coeff_fric * ddelta_da + coeff_coup * delta]


def _solve_growth(friction_factor):
    y0 = [A_GROW_INI, 1.0]
    try:
        sol = solve_ivp(
            _growth_ode, [A_GROW_INI, 1.0], y0,
            args=(friction_factor,),
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


# Cached at module import — once per worker process
_D_LCDM_REF = _solve_growth(1.0)


def _chi2_T20(sigma_eff_T20):
    """Compute chi2 for sigma_8 using growth ODE."""
    if _D_LCDM_REF is None or _D_LCDM_REF <= 0.0:
        return None, None
    ff = 1.0 + ALPHA_FR * np.log10(max(sigma_eff_T20, 1e-30) / SIGMA_REF)
    ff = max(ff, 0.1)
    D_sqt = _solve_growth(ff)
    if D_sqt is None or D_sqt <= 0.0:
        return None, None
    sigma8 = S8_PLANCK * (D_sqt / _D_LCDM_REF)
    chi2_pl = ((sigma8 - S8_PLANCK) / S8_PLANCK_ERR) ** 2
    chi2_ki = ((sigma8 - S8_KIDS)   / S8_KIDS_ERR)   ** 2
    return float(min(chi2_pl, chi2_ki)), float(sigma8)


# ──────────────────────────────────────────────────────────────────────────────
# T22: a_0 from sigma_eff at galaxy scale
# ──────────────────────────────────────────────────────────────────────────────

def _chi2_T22(sigma_eff_T22):
    """a_0_pred = A0_OBS * sqrt(sigma_eff_T22 / SIGMA_UV_L49)."""
    ratio = sigma_eff_T22 / SIGMA_UV_L49
    a0_pred = A0_OBS * np.sqrt(max(ratio, 0.0))
    chi2    = ((a0_pred / A0_OBS - 1.0) / A0_ERR_FR) ** 2
    return float(chi2), float(a0_pred)


# ──────────────────────────────────────────────────────────────────────────────
# Worker
# ──────────────────────────────────────────────────────────────────────────────

def _worker(args):
    warnings.filterwarnings('ignore')
    np.seterr(all='ignore')
    sigma_IR, sigma_UV, k_t = args

    # Effective sigma at each k-scale
    seff_T17 = float(sigma_k(K_HORIZON, sigma_IR, sigma_UV, k_t))
    seff_T20 = float(sigma_k(K_SIGMA8,  sigma_IR, sigma_UV, k_t))
    seff_T22 = float(sigma_k(K_GALAXY,  sigma_IR, sigma_UV, k_t))

    # T17 self-consistency: tau_q * 3H0 = 1
    tau_q      = seff_T17 / (4.0 * np.pi * G_N)
    tau_ratio  = tau_q * 3.0 * H0_TARGET * kmsM
    chi2_sc    = ((tau_ratio - 1.0) / SC_ERR) ** 2

    # T17 H0 CMB tension
    r_T17, H0_CMB = _chi2_T17(seff_T17)
    if r_T17 is None:
        return {'sigma_IR': float(sigma_IR), 'sigma_UV': float(sigma_UV),
                'k_t': float(k_t), 'success': False}
    chi2_T17 = r_T17

    # T20 sigma_8
    r_T20, sigma8 = _chi2_T20(seff_T20)
    if r_T20 is None:
        return {'sigma_IR': float(sigma_IR), 'sigma_UV': float(sigma_UV),
                'k_t': float(k_t), 'success': False}
    chi2_T20 = r_T20

    # T22 a_0
    chi2_T22, a0_pred = _chi2_T22(seff_T22)

    chi2_total = chi2_T17 + chi2_sc + chi2_T20 + chi2_T22

    return {
        'sigma_IR':    float(sigma_IR),
        'sigma_UV':    float(sigma_UV),
        'k_t':         float(k_t),
        'seff_T17':    seff_T17,
        'seff_T20':    seff_T20,
        'seff_T22':    seff_T22,
        'tau_ratio':   float(tau_ratio),
        'H0_CMB':      H0_CMB,
        'sigma8':      sigma8,
        'a0_pred':     a0_pred,
        'chi2_T17':    chi2_T17,
        'chi2_sc':     float(chi2_sc),
        'chi2_T20':    chi2_T20,
        'chi2_T22':    chi2_T22,
        'chi2_total':  float(chi2_total),
        'success':     True,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Pre-task
# ──────────────────────────────────────────────────────────────────────────────

def pretask():
    print('\n' + '='*60)
    print('Pre-task: L53 Integrated Self-Consistency Validation')
    print('='*60)

    # LCDM growth reference
    print(f'\n[P1] D_LCDM_REF = {_D_LCDM_REF:.6f}  (friction=1, a=1e-3->1)')

    # SC reference
    H0_si = H0_TARGET * kmsM
    sigma_sc = G_N * 4.0*np.pi / (3.0 * H0_si)
    print(f'[P2] sigma_sc = {sigma_sc:.4e}  (should = {SIGMA_SC:.2e})')

    # sigma_k at reference points
    for kt in [1e-3, 1e-2, 0.68, 10.0]:
        s17 = sigma_k(K_HORIZON, sigma_sc, SIGMA_UV_L49, kt)
        s20 = sigma_k(K_SIGMA8,  sigma_sc, SIGMA_UV_L49, kt)
        s22 = sigma_k(K_GALAXY,  sigma_sc, SIGMA_UV_L49, kt)
        print(f'[P3] k_t={kt:.2e}  sigma_eff: T17={s17:.2e}  T20={s20:.2e}  T22={s22:.2e}')

    # T17 chi2 at sigma_sc and sigma_tension
    for name, sIR in [('sigma_sc=1.17e8', SIGMA_SC), ('sigma_T17=2.34e8', SIGMA_T17_TENSION)]:
        r, h0c = _chi2_T17(sIR)
        tau_r = sIR / (4.0*np.pi*G_N) * 3.0 * H0_TARGET * kmsM
        print(f'[P4] {name}: H0_CMB={h0c:.2f}  chi2_T17={r:.2f}  tau_ratio={tau_r:.4f}')

    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 1: Grid Scan
# ──────────────────────────────────────────────────────────────────────────────

def task1_scan(pool):
    print('\n' + '='*60)
    print(f'Task 1: 3D Grid Scan ({N_SIG}x{N_UV}x{N_KT}={N_SIG*N_UV*N_KT} pts)')
    print('='*60)
    t0 = time.time()

    param_list = [(s, su, kt)
                  for s  in SIGMA_IR_GRID
                  for su in SIGMA_UV_GRID
                  for kt in KT_GRID]
    print(f'  Dispatching {len(param_list)} tasks to {N_WORKERS} workers...')
    sys.stdout.flush()

    results = pool.map(_worker, param_list)
    elapsed = time.time() - t0
    print(f'  Done in {elapsed:.1f}s')

    n_pts  = len(results)
    chi2t  = np.full(n_pts, np.nan)
    chi2_17= np.full(n_pts, np.nan)
    chi2_sc= np.full(n_pts, np.nan)
    chi2_20= np.full(n_pts, np.nan)
    chi2_22= np.full(n_pts, np.nan)
    s8_arr = np.full(n_pts, np.nan)
    h0c_arr= np.full(n_pts, np.nan)
    valid  = np.zeros(n_pts, dtype=bool)

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
        'results':   results,
        'chi2_total':chi2t,
        'chi2_T17':  chi2_17,
        'chi2_sc':   chi2_sc,
        'chi2_T20':  chi2_20,
        'chi2_T22':  chi2_22,
        'sigma8':    s8_arr,
        'H0_CMB':    h0c_arr,
        'valid':     valid,
        'n_pass':    n_pass,
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

    # Decode 3D index
    bi  = best_idx // (N_UV * N_KT)
    bj  = (best_idx % (N_UV * N_KT)) // N_KT
    bk  = best_idx % N_KT

    best_sIR = best_r['sigma_IR']
    best_sUV = best_r['sigma_UV']
    best_kt  = best_r['k_t']

    print(f'\n  Best chi2_total = {chi2t[best_idx]:.3f}')
    print(f'  sigma_IR = {best_sIR:.3e}  log={np.log10(best_sIR):.3f}')
    print(f'  sigma_UV = {best_sUV:.3e}  log={np.log10(best_sUV):.3f}')
    print(f'  k_t      = {best_kt:.3e} Mpc^-1  log={np.log10(best_kt):.3f}')
    print(f'  seff_T17 = {best_r.get("seff_T17",0):.3e}  '
          f'seff_T20 = {best_r.get("seff_T20",0):.3e}  '
          f'seff_T22 = {best_r.get("seff_T22",0):.3e}')
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
        'best_sIR': best_sIR,
        'best_sUV': best_sUV,
        'best_kt':  best_kt,
        'best_r':   best_r,
        'best_chi2': float(chi2t[best_idx]),
    }


# ──────────────────────────────────────────────────────────────────────────────
# Task 3: Visualization (6-panel)
# ──────────────────────────────────────────────────────────────────────────────

BLUE = '#1f4e79'
GRAY = '#7f7f7f'
RED  = '#c00000'
GRN  = '#2e7d32'


def task3_visualize(scan, ana):
    print('\n' + '='*60)
    print('Task 3: 6-Panel Visualization')
    print('='*60)

    chi2_3d = scan['chi2_total'].reshape(N_SIG, N_UV, N_KT)
    log_chi2_3d = np.log10(np.maximum(chi2_3d, 1e-2))

    ls  = np.log10(SIGMA_IR_GRID)
    lsu = np.log10(SIGMA_UV_GRID)
    lkt = np.log10(KT_GRID)
    bi, bj, bk = ana['bi'], ana['bj'], ana['bk']

    best_r   = ana['best_r']
    best_chi2= ana['best_chi2']

    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    fig.suptitle(
        f'L53: sigma_0(k) Model IV Integrated Self-Consistency\n'
        f'Best chi2_total={best_chi2:.1f}  '
        f'sigma_IR={ana["best_sIR"]:.2e}  sigma_UV={ana["best_sUV"]:.2e}  k_t={ana["best_kt"]:.2e}',
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

    # (a) sigma_IR x sigma_UV @ best k_t
    _plot_slice(axes[0,0],
                log_chi2_3d[:, :, bk], ls, lsu,
                'log10(sigma_IR)', 'log10(sigma_UV)',
                f'(a) sigma_IR x sigma_UV @ k_t={KT_GRID[bk]:.2e}',
                np.log10(ana['best_sIR']), np.log10(ana['best_sUV']))

    # (b) sigma_IR x k_t @ best sigma_UV
    _plot_slice(axes[0,1],
                log_chi2_3d[:, bj, :], ls, lkt,
                'log10(sigma_IR)', 'log10(k_t) [Mpc^-1]',
                f'(b) sigma_IR x k_t @ sigma_UV={SIGMA_UV_GRID[bj]:.2e}',
                np.log10(ana['best_sIR']), np.log10(ana['best_kt']))
    # L50/L52 reference points on (b)
    axes[0,1].scatter([np.log10(SIGMA_L50_BEST)], [np.log10(1e-2)],
                      marker='*', s=150, color='orange', zorder=6, label='L50')
    axes[0,1].scatter([np.log10(SIGMA_L52_BEST)], [np.log10(0.68)],
                      marker='s', s=80,  color='purple', zorder=6, label='L52')
    axes[0,1].legend(fontsize=7)

    # (c) sigma_UV x k_t @ best sigma_IR
    _plot_slice(axes[0,2],
                log_chi2_3d[bi, :, :], lsu, lkt,
                'log10(sigma_UV)', 'log10(k_t) [Mpc^-1]',
                f'(c) sigma_UV x k_t @ sigma_IR={SIGMA_IR_GRID[bi]:.2e}',
                np.log10(ana['best_sUV']), np.log10(ana['best_kt']))
    axes[0,2].axvline(np.log10(SIGMA_UV_L49), color='lime', ls='--', lw=1.5,
                      label=f'sigma_UV_L49={SIGMA_UV_L49:.1e}')
    axes[0,2].legend(fontsize=7)

    # (d) chi2 breakdown at best
    ax = axes[1, 0]
    chi2_vals = [max(best_r.get('chi2_T17', 0), 1e-3), max(best_r.get('chi2_sc', 0), 1e-3),
                 max(best_r.get('chi2_T20', 0), 1e-3), max(best_r.get('chi2_T22', 0), 1e-3)]
    labels_d  = ['T17 H0\ntension', 'T17\nself-consist', 'T20\nsigma8', 'T22\na_0']
    colors_d  = [RED, BLUE, GRN, '#e65100']
    bars = ax.bar(labels_d, chi2_vals, color=colors_d, alpha=0.8, edgecolor='k')
    ax.axhline(4.0,        color=GRAY, ls=':',  lw=1.5, label='1sigma^2=4')
    ax.axhline(CHI2_PASS,  color='lime', ls='--', lw=2, label=f'PASS={CHI2_PASS:.0f}')
    ax.axhline(CHI2_PARTIAL,color=RED,  ls='--', lw=1.5, label=f'PARTIAL={CHI2_PARTIAL:.0f}')
    for bar, val in zip(bars, chi2_vals):
        ax.text(bar.get_x() + bar.get_width()/2, val + 1.0,
                f'{val:.1f}', ha='center', fontsize=9, fontweight='bold')
    ax.set_ylabel('chi2')
    ax.set_title(f'(d) chi2 breakdown at best fit (total={best_chi2:.1f})')
    ax.legend(fontsize=7)
    ax.set_yscale('log')

    # (e) chi2_total distribution
    ax = axes[1, 1]
    c2_flat = scan['chi2_total']
    valid   = scan['valid']
    c2_v    = c2_flat[valid]
    ax.hist(np.log10(np.maximum(c2_v, 1e-2)), bins=40, color=BLUE, alpha=0.7, edgecolor='k')
    ax.axvline(np.log10(CHI2_PASS),    color='lime', ls='--', lw=2,
               label=f'PASS={CHI2_PASS:.0f}')
    ax.axvline(np.log10(CHI2_PARTIAL), color=RED,   ls='--', lw=1.5,
               label=f'PARTIAL={CHI2_PARTIAL:.0f}')
    ax.axvline(np.log10(best_chi2),    color='orange', ls='-', lw=2.5,
               label=f'best={best_chi2:.1f}')
    ax.set_xlabel('log10(chi2_total)')
    ax.set_ylabel('Count')
    ax.set_title(f'(e) chi2_total dist (PASS: {scan["n_pass"]}/{int(valid.sum())})')
    ax.legend(fontsize=7)

    # (f) best sigma_0(k) curve + reference points
    ax = axes[1, 2]
    k_range  = np.logspace(-6, 3, 400)
    sk_best  = np.array([sigma_k(k, ana['best_sIR'], ana['best_sUV'], ana['best_kt'])
                         for k in k_range])
    sk_l50   = np.array([sigma_k(k, SIGMA_L50_BEST, SIGMA_UV_L49, 1e-2) for k in k_range])
    sk_l52   = np.array([sigma_k(k, SIGMA_L52_BEST, SIGMA_UV_L49, 0.68) for k in k_range])

    ax.loglog(k_range, sk_best, color=RED,    lw=2.5,
              label=f'L53 best sIR={ana["best_sIR"]:.1e} sUV={ana["best_sUV"]:.1e}')
    ax.loglog(k_range, sk_l50,  color='orange', lw=1.5, ls='--',
              label=f'L50 sIR={SIGMA_L50_BEST:.1e} k_t=1e-2')
    ax.loglog(k_range, sk_l52,  color='purple', lw=1.5, ls=':',
              label=f'L52 sIR={SIGMA_L52_BEST:.1e} k_t=0.68')

    # Reference sigma values from L48~L52
    for k_ref, s_ref, col, lbl in [
        (K_HORIZON, SIGMA_T17_SC,      BLUE,   'T17 SC 1.17e8'),
        (K_HORIZON, SIGMA_T17_TENSION, 'cyan', 'T17 tension 2.34e8'),
        (K_SIGMA8,  SIGMA_T20_S8,      GRN,    'T20 sigma8 5.6e7'),
        (K_GALAXY,  SIGMA_T22_A0,      '#8B4513', 'T22 a0 3.31e9'),
    ]:
        ax.scatter([k_ref], [s_ref], s=100, color=col, zorder=5, label=lbl)
    ax.axvline(K_HORIZON, color=BLUE,    ls=':', lw=1, alpha=0.5)
    ax.axvline(K_SIGMA8,  color=GRN,    ls=':', lw=1, alpha=0.5)
    ax.axvline(K_GALAXY,  color='brown', ls=':', lw=1, alpha=0.5)
    ax.axvline(ana['best_kt'], color=RED, ls='--', lw=1.5,
               label=f'k_t={ana["best_kt"]:.2e}')
    ax.set_xlabel('k [Mpc^-1]')
    ax.set_ylabel('sigma_0(k)')
    ax.set_title('(f) sigma_0(k) curves + validation points')
    ax.legend(fontsize=6, loc='lower right')
    ax.grid(alpha=0.3)

    plt.tight_layout()
    out = os.path.join(_SCRIPT_DIR, 'l53_main.png')
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved: {out}')
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 4: Verdict
# ──────────────────────────────────────────────────────────────────────────────

def task4_verdict(scan, ana):
    print('\n' + '='*60)
    print('L53 FINAL VERDICT')
    print('='*60)

    best_chi2 = ana['best_chi2']
    best_r    = ana['best_r']
    n_pass    = scan['n_pass']

    if best_chi2 < CHI2_PASS:
        verdict = 'PASS — integrated region found, Model IV PASSES'
    elif best_chi2 < CHI2_PARTIAL:
        verdict = 'PARTIAL — no full-pass region, some constraints satisfied'
    else:
        verdict = 'FAIL — no integrated region, Model IV inconsistent'

    print(f'\n  [VERDICT] {verdict}')
    print(f'\n  Best chi2_total = {best_chi2:.3f}')
    print(f'  PASS threshold  = {CHI2_PASS:.0f}')
    print(f'  PASS count      = {n_pass}/{N_SIG*N_UV*N_KT}')

    print(f'\n  Chi2 breakdown at best:')
    for key, label in [('chi2_T17','T17 H0 tension'), ('chi2_sc','T17 SC'),
                        ('chi2_T20','T20 sigma8'), ('chi2_T22','T22 a_0')]:
        v = best_r.get(key, float('nan'))
        print(f'    {label:<20}: {v:.3f}  {"PASS" if v < 4 else "FAIL"}')

    print(f'\n  === sigma_0 Diagnostic Table (Updated) ===')
    print(f'  {"Constraint":<28} {"sigma_0":>12}  {"log10":>7}')
    print(f'  {"-"*52}')
    for label, val in [
        ('T17 H0 tension',       SIGMA_T17_TENSION),
        ('T17 self-consist',     SIGMA_T17_SC),
        ('T20 sigma8 (L48)',     SIGMA_T20_S8),
        ('T22 a_0 (L49)',        SIGMA_T22_A0),
        ('L50 best sigma_IR',    SIGMA_L50_BEST),
        ('L52 best sigma_IR',    SIGMA_L52_BEST),
        ('L53 best sigma_IR',    ana['best_sIR']),
    ]:
        tag = '  <-- THIS RUN' if 'L53' in label else ''
        print(f'  {label:<28} {val:>12.3e}  {np.log10(val):>7.3f}{tag}')
    print(f'\n  L53 best sigma_UV = {ana["best_sUV"]:.3e}  log={np.log10(ana["best_sUV"]):.3f}  <-- THIS RUN')
    print(f'  L53 best k_t      = {ana["best_kt"]:.3e} Mpc^-1  log={np.log10(ana["best_kt"]):.3f}  <-- THIS RUN')
    print(f'  L53 best H0_CMB   = {best_r.get("H0_CMB",0):.2f} km/s/Mpc')
    print(f'  L53 best sigma8   = {best_r.get("sigma8",0):.4f}')

    sys.stdout.flush()
    return {
        'verdict':    verdict,
        'best_chi2':  best_chi2,
        'n_pass':     n_pass,
        'best_sIR':   ana['best_sIR'],
        'best_sUV':   ana['best_sUV'],
        'best_kt':    ana['best_kt'],
    }


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('='*60)
    print('L53: Integrated Self-Consistency (3D Grid)')
    print(f'Grid: {N_SIG}x{N_UV}x{N_KT}={N_SIG*N_UV*N_KT} pts | {N_WORKERS} workers')
    print(f'sigma_IR: [10^7, 10^9.5]  sigma_UV: [10^8, 10^10]  k_t: [1e-4, 10]')
    print(f'Gamma0 fixed={GAMMA0_FIX:.1e}  PASS threshold={CHI2_PASS:.0f}')
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
    print('L53 RESULTS SUMMARY')
    print('='*60)
    print(f"Grid: {N_SIG}x{N_UV}x{N_KT}  Valid: {int(scan.get('valid', np.array([])).sum())}/{N_SIG*N_UV*N_KT}")
    print(f"PASS count: {scan.get('n_pass',0)}")
    print(f"Best chi2_total: {ana.get('best_chi2',0):.3f}")
    print(f"Best sigma_IR: {ana.get('best_sIR',0):.3e}  sigma_UV: {ana.get('best_sUV',0):.3e}  k_t: {ana.get('best_kt',0):.3e}")
    print(f"Verdict: {verdict.get('verdict','N/A')}")

    save = {
        'n_pass':       scan.get('n_pass', 0),
        'best_chi2':    ana.get('best_chi2', 0),
        'best_sIR':     ana.get('best_sIR', 0),
        'best_sUV':     ana.get('best_sUV', 0),
        'best_kt':      ana.get('best_kt', 0),
        'verdict':      verdict.get('verdict', ''),
        'chi2_breakdown': {
            'T17':  ana['best_r'].get('chi2_T17', 0),
            'sc':   ana['best_r'].get('chi2_sc', 0),
            'T20':  ana['best_r'].get('chi2_T20', 0),
            'T22':  ana['best_r'].get('chi2_T22', 0),
        },
        'obs': {
            'H0_CMB':  ana['best_r'].get('H0_CMB', 0),
            'sigma8':  ana['best_r'].get('sigma8', 0),
            'a0_pred': ana['best_r'].get('a0_pred', 0),
            'tau_ratio': ana['best_r'].get('tau_ratio', 0),
        },
        'params': {
            'N_SIG': N_SIG, 'N_UV': N_UV, 'N_KT': N_KT,
            'GAMMA0_FIX': GAMMA0_FIX,
            'CHI2_PASS': CHI2_PASS,
        },
    }
    out_json = os.path.join(_SCRIPT_DIR, 'l53_results.json')
    with open(out_json, 'w') as f:
        json.dump(_jsonify(save), f, indent=2)
    print(f'Saved: {out_json}')
