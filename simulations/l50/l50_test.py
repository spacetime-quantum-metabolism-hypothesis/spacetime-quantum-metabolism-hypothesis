#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L50 (T17_v4): sigma_0(k) Model IV — sigma_IR Grid H0 Tension Re-validation
============================================================================
sigma_0(k) = (sigma_IR + sigma_UV*(k/k_t)^2) / (1 + (k/k_t)^2)
Background (k->0): sigma_eff = sigma_IR
Galaxy scale (T22, k>>k_t): sigma_eff -> sigma_UV = 3.31e9 (L49)

Grid  : 30x30 sigma_IR x Gamma0 = 900 pts, 8 workers
Output: l50_main.png, l50_results.json
"""

import os, sys, time, json, warnings
import numpy as np
from scipy.integrate import solve_ivp
from scipy.integrate import trapezoid
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
# Physical Constants & Observational Anchors
# ──────────────────────────────────────────────────────────────────────────────
G_N    = 6.674e-11      # m^3 kg^-1 s^-2
C_SI   = 2.998e8        # m/s
Mpc_m  = 3.0857e22      # m per Mpc
kmsM   = 1e3 / Mpc_m    # 1 km/s/Mpc in s^-1

H0_LOCAL   = 73.80      # km/s/Mpc (SH0ES)
H0_LOCAL_ERR = 0.88
H0_CMB_PL  = 67.40      # km/s/Mpc (Planck)
H0_CMB_ERR = 0.50
H0_TARGET  = 73.80      # true H0 input for ODE

OM_FID  = 0.3150
OL_FID  = 0.6850
OB_FID  = 0.0493
OR_FID  = 9.20e-5
Z_STAR  = 1090.0
KPC_CONV = 3.241e-14    # 1 (km/s)^2/kpc in m/s^2

# BOSS z=0.57 constraint
H_BOSS_Z  = 0.57
H_BOSS_OBS = 96.8       # km/s/Mpc
H_BOSS_ERR = 3.4

# sigma_0(k) Model IV parameters (fixed in L50, only sigma_IR free)
SIGMA_UV  = 3.31e9      # m^3/(kg*s), from L49 T22 result
K_T       = 1e-2        # Mpc^-1, transition scale (~30 Mpc)
K_HORIZON = H0_TARGET * kmsM / (2 * np.pi * C_SI / Mpc_m)  # ~1e-4 Mpc^-1

# L48/T20 reference values for diagnostic
SIGMA_T17_TENSION = 2.34e8
SIGMA_T17_SC      = 1.17e8
SIGMA_T20_S8      = 5.6e7
SIGMA_T22_A0      = 3.31e9   # L49

# Grid
N_SIG    = 30
N_GAM    = 30
SIGMA_GRID = np.logspace(6, 10, N_SIG)   # sigma_IR [m^3/(kg*s)]
GAMMA_GRID = np.logspace(0, 12, N_GAM)   # Gamma0 [m^-3 s^-1]
N_WORKERS  = 8

# ODE integration
A_INI = 1.0 / 101.0    # z=100 start
A_FIN = 1.0             # z=0
N_A   = 500


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


# ──────────────────────────────────────────────────────────────────────────────
# sigma_0(k) Model IV (Lorentzian, Candidate B)
# ──────────────────────────────────────────────────────────────────────────────

def sigma_k(k_Mpc, sigma_IR, sigma_UV=SIGMA_UV, k_t=K_T):
    """Lorentzian sigma_0(k) profile."""
    x2 = (k_Mpc / k_t)**2
    return (sigma_IR + sigma_UV * x2) / (1.0 + x2)


def sigma_eff_bg(sigma_IR):
    """Background effective sigma: k->0 limit = sigma_IR."""
    return sigma_IR


# ──────────────────────────────────────────────────────────────────────────────
# Derived Parameters (same as L48)
# ──────────────────────────────────────────────────────────────────────────────

def _tau_q(sigma_IR):
    return sigma_IR / (4.0 * np.pi * G_N)

def _n_inf(sigma_IR, Gamma0):
    return Gamma0 * _tau_q(sigma_IR)

def _rho_m0(H0_kmsMpc=H0_TARGET):
    H0_si = H0_kmsMpc * kmsM
    return 3.0 * H0_si**2 * OM_FID / (8.0 * np.pi * G_N)

def _eps(sigma_IR, Gamma0, H0_kmsMpc=H0_TARGET):
    H0_si = H0_kmsMpc * kmsM
    ni = _n_inf(sigma_IR, Gamma0)
    if ni <= 0.0:
        return None
    val = 3.0 * H0_si**2 * OL_FID * C_SI**2 / (8.0 * np.pi * G_N * ni)
    return val if np.isfinite(val) and val > 0 else None


# ──────────────────────────────────────────────────────────────────────────────
# LCDM helpers
# ──────────────────────────────────────────────────────────────────────────────

def _E_lcdm(z, Om=OM_FID, OL=OL_FID, Or=OR_FID):
    return np.sqrt(np.maximum(Om*(1+z)**3 + Or*(1+z)**4 + OL, 1e-30))

def _H_lcdm_si(z, H0_kmsMpc=H0_TARGET):
    return H0_kmsMpc * kmsM * _E_lcdm(z)


# ──────────────────────────────────────────────────────────────────────────────
# SQT ODE (scale factor a, H computed algebraically — P4 fix)
# ──────────────────────────────────────────────────────────────────────────────

def _sqt_ode(a, y, sigma_IR, Gamma0, eps_val):
    """
    y = [n, rho_m].  H computed algebraically each step.
    dy/da = (dy/dt) / (a*H).
    """
    n, rho_m = float(y[0]), float(y[1])
    n     = max(n,     0.0)
    rho_m = max(rho_m, 0.0)

    rho_n   = n * eps_val / C_SI**2
    rho_tot = rho_m + rho_n
    if rho_tot <= 0.0:
        return [0.0, 0.0]

    H = np.sqrt(8.0 * np.pi * G_N * rho_tot / 3.0)
    if not np.isfinite(H) or H <= 0.0:
        return [0.0, 0.0]

    dadt = a * H
    if dadt <= 0.0:
        return [0.0, 0.0]

    dn_dt  = Gamma0 - 3.0*H*n - sigma_IR*n*rho_m
    drm_dt = -3.0*H*rho_m + sigma_IR*n*rho_m*eps_val/C_SI**2

    return [dn_dt / dadt, drm_dt / dadt]


def _solve_sqt(sigma_IR, Gamma0, H0_kmsMpc=H0_TARGET):
    """Solve SQT ODE; return solution dict or None."""
    eps_val = _eps(sigma_IR, Gamma0, H0_kmsMpc)
    if eps_val is None:
        return None

    H0_si = H0_kmsMpc * kmsM
    z_ini = 1.0/A_INI - 1.0
    rm_ini = _rho_m0(H0_kmsMpc) * (1.0 + z_ini)**3
    H_ini  = _H_lcdm_si(z_ini, H0_kmsMpc)
    denom  = 3.0*H_ini + sigma_IR*rm_ini
    n_ini  = Gamma0 / max(denom, 1e-100)

    try:
        sol = solve_ivp(
            _sqt_ode, [A_INI, A_FIN], [n_ini, rm_ini],
            args=(sigma_IR, Gamma0, eps_val),
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
    rn_arr = n_arr * eps_val / C_SI**2
    H2_arr = np.maximum(8.0*np.pi*G_N*(rm_arr+rn_arr)/3.0, 1e-80)
    H_arr  = np.sqrt(H2_arr)
    E_arr  = H_arr / H0_si
    E0     = float(E_arr[-1])
    if not np.isfinite(E0) or E0 <= 0:
        return None

    return {
        'a': a_arr, 'z': 1.0/a_arr - 1.0,
        'H': H_arr, 'E': E_arr, 'E0': E0,
        'H0_eff': float(H_arr[-1]) / kmsM,
        'eps': eps_val,
    }


# ──────────────────────────────────────────────────────────────────────────────
# H0 Tension & BOSS chi2
# ──────────────────────────────────────────────────────────────────────────────

def _E_fn_from_sol(sol):
    z_ode = sol['z'][::-1]
    E_ode = sol['E'][::-1]
    z_max = float(z_ode[-1])
    def E_fn(z):
        z = float(z)
        return float(np.interp(z, z_ode, E_ode)) if z <= z_max else float(_E_lcdm(z))
    return E_fn


def _sound_horizon_si(H0_kmsMpc, E_fn):
    """r_s = integral_{z*}^{10000} c_s/H dz [m]  (pre-recombination)."""
    H0_si = H0_kmsMpc * kmsM
    Rb0   = 3.0*OB_FID / (4.0*OR_FID)
    z_int = np.linspace(Z_STAR, 10000.0, 800)
    Rb_z  = Rb0 / (1.0 + z_int)
    cs_z  = C_SI / np.sqrt(3.0*(1.0 + Rb_z))
    H_z   = H0_si * np.array([E_fn(z) for z in z_int])
    return trapezoid(cs_z / np.maximum(H_z, 1e-50), z_int)


def _comoving_dist_si(H0_kmsMpc, z_max, E_fn):
    """chi = integral_0^{z_max} c/H dz [m]."""
    H0_si = H0_kmsMpc * kmsM
    z_int = np.linspace(0.0, z_max, 800)
    H_z   = H0_si * np.array([E_fn(z) for z in z_int])
    return trapezoid(C_SI / np.maximum(H_z, 1e-50), z_int)


def _tension_metric(sigma_IR, Gamma0):
    """Compute H0_CMB_apparent and BOSS chi2."""
    sol = _solve_sqt(sigma_IR, Gamma0)
    if sol is None:
        return None

    E_sqt  = _E_fn_from_sol(sol)
    E_lcdm = lambda z: float(_E_lcdm(z))

    rs_sqt   = _sound_horizon_si(H0_TARGET, E_sqt)
    rs_lcdm  = _sound_horizon_si(H0_TARGET, E_lcdm)
    chi_sqt  = _comoving_dist_si(H0_TARGET, Z_STAR, E_sqt)
    chi_lcdm = _comoving_dist_si(H0_TARGET, Z_STAR, E_lcdm)

    h0_ratio    = (rs_sqt / max(rs_lcdm, 1e-10)) * (chi_lcdm / max(chi_sqt, 1e-10))
    H0_CMB_app  = H0_TARGET * h0_ratio

    # BOSS z=0.57 chi2
    H_boss_sqt = H0_TARGET * float(E_sqt(H_BOSS_Z))
    chi2_boss  = ((H_boss_sqt - H_BOSS_OBS) / H_BOSS_ERR)**2

    # H0_CMB chi2
    chi2_h0cmb = ((H0_CMB_app - H0_CMB_PL) / H0_CMB_ERR)**2

    return {
        'H0_local':   H0_TARGET,
        'H0_CMB':     float(H0_CMB_app),
        'h0_ratio':   float(h0_ratio),
        'tension_km': float(H0_TARGET - H0_CMB_app),
        'H_boss_sqt': float(H_boss_sqt),
        'chi2_boss':  float(chi2_boss),
        'chi2_h0cmb': float(chi2_h0cmb),
        'chi2_total': float(chi2_boss + chi2_h0cmb),
        'rs_sqt_Mpc':  float(rs_sqt / Mpc_m),
        'rs_lcdm_Mpc': float(rs_lcdm / Mpc_m),
        'sol_E0':     float(sol['E0']),
    }


# ──────────────────────────────────────────────────────────────────────────────
# Worker
# ──────────────────────────────────────────────────────────────────────────────

def _worker(args):
    warnings.filterwarnings('ignore')
    np.seterr(all='ignore')
    sigma_IR, Gamma0 = args

    sc  = {
        'tau_q':     float(_tau_q(sigma_IR)),
        'tau_ratio': float(_tau_q(sigma_IR) * 3.0 * H0_TARGET * kmsM),
        'sigma_sc':  float(G_N * 4.0 * np.pi / (3.0 * H0_TARGET * kmsM)),
    }
    tens = _tension_metric(sigma_IR, Gamma0)
    ni   = _n_inf(sigma_IR, Gamma0)
    eps  = _eps(sigma_IR, Gamma0)

    return {
        'sigma_IR': float(sigma_IR),
        'Gamma0':   float(Gamma0),
        'n_inf':    float(ni) if np.isfinite(ni) else None,
        'tau_q':    float(sc['tau_q']),
        'tau_ratio': float(sc['tau_ratio']),
        'sigma_sc': float(sc['sigma_sc']),
        'eps':      float(eps) if eps is not None and np.isfinite(eps) else None,
        'tension':  tens,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Pre-task
# ──────────────────────────────────────────────────────────────────────────────

def pretask():
    print('\n' + '='*60)
    print('Pre-task: L50 sigma_0(k) Model IV Validation')
    print('='*60)

    H0_si = H0_TARGET * kmsM
    sigma_sc = G_N * 4.0*np.pi / (3.0*H0_si)
    tau_sc   = sigma_sc / (4.0*np.pi*G_N)
    print(f'\n[P1] sigma_sc = {sigma_sc:.4e}  (should equal {SIGMA_T17_SC:.2e})')
    print(f'[P2] tau_q_sc = {tau_sc:.4e} s  = 1/(3H0) = {1/(3*H0_si):.4e} s')

    # sigma_0(k) at k_horizon
    sig_hor = sigma_k(K_HORIZON, sigma_sc)
    sig_gal = sigma_k(1.0, sigma_sc)  # galaxy scale k~1 Mpc^-1
    print(f'\n[P3] K_HORIZON = {K_HORIZON:.4e} Mpc^-1')
    print(f'[P3] sigma_0(k_hor, sigma_sc) = {sig_hor:.4e}  (should ~ sigma_sc={sigma_sc:.2e})')
    print(f'[P3] sigma_0(k=1, sigma_sc)   = {sig_gal:.4e}  (should ~ sigma_UV={SIGMA_UV:.2e})')

    # ODE test at sigma_sc
    sol_test = _solve_sqt(sigma_sc, 1e8)
    if sol_test:
        print(f'[P4] ODE test: E(z=0) = {sol_test["E0"]:.5f}  '
              f'[{"OK" if abs(sol_test["E0"]-1)<0.05 else "WARN"}]')
    else:
        print('[P4] ODE test FAILED')

    print(f'\n[P5] sigma_0(k) diagnostics at sigma_sc:')
    print(f'     k=0 (IR):   sigma = {sigma_k(1e-6, sigma_sc):.4e}  (= sigma_IR)')
    print(f'     k=k_t:      sigma = {sigma_k(K_T, sigma_sc):.4e}  (= midpoint)')
    print(f'     k>>k_t:     sigma = {sigma_k(1e2, sigma_sc):.4e}  (-> sigma_UV={SIGMA_UV:.2e})')
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 1: Grid Scan
# ──────────────────────────────────────────────────────────────────────────────

def task1_scan(pool):
    print('\n' + '='*60)
    print(f'Task 1: sigma_IR x Gamma0 Grid Scan ({N_SIG}x{N_GAM}={N_SIG*N_GAM} pts)')
    print('='*60)
    t0 = time.time()
    param_list = [(s, g) for s in SIGMA_GRID for g in GAMMA_GRID]
    print(f'  Dispatching {len(param_list)} tasks to {N_WORKERS} workers...')
    sys.stdout.flush()

    results = pool.map(_worker, param_list)
    elapsed = time.time() - t0
    print(f'  Done in {elapsed:.1f}s')

    n_pts = len(results)
    H0_CMB_arr  = np.full(n_pts, np.nan)
    tension_arr = np.full(n_pts, np.nan)
    tau_r_arr   = np.full(n_pts, np.nan)
    chi2_boss   = np.full(n_pts, np.nan)
    chi2_total  = np.full(n_pts, np.nan)
    valid       = np.zeros(n_pts, dtype=bool)

    for i, r in enumerate(results):
        tau_r_arr[i] = r.get('tau_ratio', np.nan)
        if r.get('tension') is not None:
            t = r['tension']
            H0_CMB_arr[i]  = t['H0_CMB']
            tension_arr[i] = t['tension_km']
            chi2_boss[i]   = t['chi2_boss']
            chi2_total[i]  = t['chi2_total']
            valid[i]       = True

    n_valid = int(valid.sum())
    print(f'  Valid: {n_valid}/{n_pts}')
    if n_valid > 0:
        print(f'  H0_CMB range: [{np.nanmin(H0_CMB_arr[valid]):.2f}, {np.nanmax(H0_CMB_arr[valid]):.2f}]')
        print(f'  Tension range: [{np.nanmin(tension_arr[valid]):.2f}, {np.nanmax(tension_arr[valid]):.2f}]')
    sys.stdout.flush()

    return {
        'results':    results,
        'H0_CMB':     H0_CMB_arr,
        'tension':    tension_arr,
        'tau_ratio':  tau_r_arr,
        'chi2_boss':  chi2_boss,
        'chi2_total': chi2_total,
        'valid':      valid,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Task 2: Analysis
# ──────────────────────────────────────────────────────────────────────────────

def task2_analyze(scan):
    print('\n' + '='*60)
    print('Task 2: Analysis')
    print('='*60)

    valid   = scan['valid']
    H0_CMB  = scan['H0_CMB']
    tension = scan['tension']
    chi2_tot= scan['chi2_total']
    results = scan['results']

    # H0_CMB matching
    tol = 2.0
    match = valid & (np.abs(H0_CMB - H0_CMB_PL) < tol)
    n_match = int(match.sum())
    print(f'\n  H0_CMB ≈ {H0_CMB_PL} ± {tol}: {n_match}/{N_SIG*N_GAM} pairs')

    # Best chi2
    chi2_valid = np.where(valid, chi2_tot, np.inf)
    best_idx   = int(np.nanargmin(chi2_valid))
    best_r     = results[best_idx]
    best_t     = best_r.get('tension', {}) or {}

    print(f'\n  Best chi2 point:')
    print(f'  sigma_IR = {best_r["sigma_IR"]:.3e}  Gamma0 = {best_r["Gamma0"]:.3e}')
    print(f'  H0_CMB   = {best_t.get("H0_CMB", np.nan):.2f}  '
          f'H_BOSS(z={H_BOSS_Z}) = {best_t.get("H_boss_sqt", np.nan):.2f}')
    print(f'  chi2_boss = {best_t.get("chi2_boss", np.nan):.3f}  '
          f'chi2_total = {chi2_tot[best_idx]:.3f}')
    print(f'  tau_ratio = {best_r["tau_ratio"]:.4f}  (self-consistent = 1.0)')

    # sigma_sc comparison
    sigma_sc = float(G_N * 4.0*np.pi / (3.0 * H0_TARGET * kmsM))
    best_sIR = best_r['sigma_IR']
    print(f'\n  sigma_sc (T17 self-consist) = {sigma_sc:.3e}  log={np.log10(sigma_sc):.3f}')
    print(f'  Best sigma_IR              = {best_sIR:.3e}  log={np.log10(best_sIR):.3f}')
    print(f'  Ratio best/sigma_sc        = {best_sIR/sigma_sc:.3f}  '
          f'delta_log = {np.log10(best_sIR/sigma_sc):.3f} dex')

    sys.stdout.flush()
    return {
        'n_match':    n_match,
        'match':      match,
        'best_idx':   best_idx,
        'best_r':     best_r,
        'sigma_sc':   sigma_sc,
        'best_sIR':   best_sIR,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Task 3: Visualization (6-panel)
# ──────────────────────────────────────────────────────────────────────────────

BLUE = '#1f4e79'
GRAY = '#7f7f7f'
RED  = '#c00000'


def task3_visualize(scan, ana):
    print('\n' + '='*60)
    print('Task 3: 6-Panel Visualization')
    print('='*60)

    ns, ng = N_SIG, N_GAM
    ls = np.log10(SIGMA_GRID)
    lg = np.log10(GAMMA_GRID)
    ls_m, lg_m = np.meshgrid(ls, lg, indexing='ij')

    H0_CMB_2d  = scan['H0_CMB'].reshape(ns, ng)
    tension_2d = scan['tension'].reshape(ns, ng)
    tau_r_2d   = scan['tau_ratio'].reshape(ns, ng)
    chi2_2d    = scan['chi2_total'].reshape(ns, ng)
    valid_2d   = scan['valid'].reshape(ns, ng)

    def _nan(arr):
        return np.where(np.isfinite(arr), arr, np.nan)

    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    fig.suptitle(
        f'L50 (T17_v4): sigma_0(k) Model IV  sigma_UV={SIGMA_UV:.1e}  k_t={K_T:.0e} Mpc^-1\n'
        f'H0_local={H0_TARGET:.1f}  H0_CMB_target={H0_CMB_PL:.1f} km/s/Mpc',
        fontsize=12, fontweight='bold')

    # ── (a) H0_CMB contour ──
    ax = axes[0, 0]
    cf = ax.contourf(ls_m, lg_m, _nan(H0_CMB_2d), levels=50, cmap='coolwarm_r',
                     vmin=60, vmax=80)
    plt.colorbar(cf, ax=ax, label='H0_CMB (km/s/Mpc)')
    cs = ax.contour(ls_m, lg_m, _nan(H0_CMB_2d), levels=[H0_CMB_PL], colors=RED, linewidths=2)
    ax.clabel(cs, fmt=f'{H0_CMB_PL:.1f}', fontsize=9)
    sigma_sc_log = np.log10(ana['sigma_sc'])
    ax.axvline(sigma_sc_log, color=BLUE, ls='--', lw=1.5, label='sigma_sc')
    ax.axvline(np.log10(SIGMA_T17_TENSION), color='orange', ls=':', lw=1, label='sigma_tension')
    ax.set_xlabel('log10(sigma_IR)')
    ax.set_ylabel('log10(Gamma0)')
    ax.set_title('(a) H0_CMB apparent [km/s/Mpc]')
    ax.legend(fontsize=7)

    # ── (b) H0 tension ──
    ax = axes[0, 1]
    target_t = H0_TARGET - H0_CMB_PL
    cf = ax.contourf(ls_m, lg_m, _nan(tension_2d), levels=50, cmap='RdYlGn',
                     vmin=-5, vmax=12)
    plt.colorbar(cf, ax=ax, label='H0_local - H0_CMB (km/s/Mpc)')
    cs = ax.contour(ls_m, lg_m, _nan(tension_2d), levels=[target_t], colors=RED, linewidths=2)
    ax.clabel(cs, fmt=f'tension={target_t:.1f}', fontsize=9)
    ax.axvline(sigma_sc_log, color=BLUE, ls='--', lw=1.5, label='sigma_sc')
    ax.set_xlabel('log10(sigma_IR)')
    ax.set_ylabel('log10(Gamma0)')
    ax.set_title(f'(b) H0 tension (target={target_t:.1f} km/s/Mpc)')
    ax.legend(fontsize=7)

    # ── (c) tau_q self-consistency ──
    ax = axes[0, 2]
    log_tau = np.log10(np.maximum(_nan(tau_r_2d), 1e-10))
    cf = ax.contourf(ls_m, lg_m, log_tau, levels=50, cmap='PuOr')
    plt.colorbar(cf, ax=ax, label='log10(tau_q*3H0)')
    cs = ax.contour(ls_m, lg_m, _nan(tau_r_2d), levels=[1.0], colors=BLUE, linewidths=2.5)
    ax.clabel(cs, fmt='tau*3H0=1', fontsize=9)
    ax.axvline(sigma_sc_log, color=RED, ls='--', lw=1.5, label='tau*3H0=1 exact')
    ax.set_xlabel('log10(sigma_IR)')
    ax.set_ylabel('log10(Gamma0)')
    ax.set_title('(c) Self-consistency: tau_q*3H0')
    ax.legend(fontsize=7)

    # ── (d) chi2 total (BOSS + H0_CMB) ──
    ax = axes[1, 0]
    log_chi2 = np.log10(np.maximum(_nan(chi2_2d), 1e-4))
    cf = ax.contourf(ls_m, lg_m, log_chi2, levels=50, cmap='viridis_r')
    plt.colorbar(cf, ax=ax, label='log10(chi2_BOSS + chi2_H0CMB)')
    # Mark best point
    best_idx = ana['best_idx']
    bi = best_idx // ng
    bj = best_idx %  ng
    ax.scatter([ls[bi]], [lg[bj]], color=RED, s=80, zorder=5, label='best fit')
    ax.axvline(sigma_sc_log, color=BLUE, ls='--', lw=1.5, label='sigma_sc')
    ax.set_xlabel('log10(sigma_IR)')
    ax.set_ylabel('log10(Gamma0)')
    ax.set_title('(d) chi2 (BOSS + H0_CMB)')
    ax.legend(fontsize=7)

    # ── (e) sigma_0(k) curves ──
    ax = axes[1, 1]
    k_range = np.logspace(-6, 2, 300)
    for sIR, col, lbl in [
        (SIGMA_T17_SC,       BLUE,    f'sigma_sc  = {SIGMA_T17_SC:.1e}'),
        (SIGMA_T17_TENSION,  'orange', f'sigma_tension={SIGMA_T17_TENSION:.1e}'),
        (ana['best_sIR'],    RED,     f'L50 best  = {ana["best_sIR"]:.1e}'),
    ]:
        sk_vals = sigma_k(k_range, sIR)
        ax.loglog(k_range, sk_vals, color=col, lw=2, label=lbl)
    ax.axvline(K_T,       color='purple', ls='--', lw=1.5, label=f'k_t={K_T:.0e} Mpc^-1')
    ax.axvline(K_HORIZON, color='green',  ls=':',  lw=1.5, label=f'k_hor={K_HORIZON:.1e}')
    ax.axhline(SIGMA_UV,  color=GRAY,    ls=':',  lw=1,   label=f'sigma_UV={SIGMA_UV:.1e}')
    ax.set_xlabel('k [Mpc^-1]')
    ax.set_ylabel('sigma_0(k) [m^3/(kg*s)]')
    ax.set_title('(e) sigma_0(k) Model IV — Lorentzian Candidate B')
    ax.legend(fontsize=7)
    ax.grid(alpha=0.3)

    # ── (f) Diagnostic comparison bar chart ──
    ax = axes[1, 2]
    refs = {
        'T17 H0\ntension':  np.log10(SIGMA_T17_TENSION),
        'T17 self-\nconsist': np.log10(SIGMA_T17_SC),
        'T20\nsigma8':       np.log10(SIGMA_T20_S8),
        'T22 a_0\n(L49)':    np.log10(SIGMA_T22_A0),
        'L50 best\n(T17_v4)': np.log10(ana['best_sIR']),
    }
    colors_bar = ['#c00000', BLUE, '#2e7d32', '#8B4513', '#e65100']
    bars = ax.bar(list(refs.keys()), list(refs.values()),
                  color=colors_bar, alpha=0.8, edgecolor='k', linewidth=0.5)
    ax.axhline(np.log10(SIGMA_T17_SC), color=BLUE, ls='--', lw=1.5, alpha=0.5)
    for bar, (k, v) in zip(bars, refs.items()):
        ax.text(bar.get_x() + bar.get_width()/2, v + 0.05,
                f'{10**v:.2e}', ha='center', va='bottom', fontsize=7, rotation=60)
    ax.set_ylabel('log10(sigma_0) [m^3/(kg*s)]')
    ax.set_title('(f) sigma_0 Diagnostic Comparison')
    ax.set_ylim(7, 10.5)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    out = os.path.join(_SCRIPT_DIR, 'l50_main.png')
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved: {out}')
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 4: Verdict
# ──────────────────────────────────────────────────────────────────────────────

def task4_verdict(scan, ana):
    print('\n' + '='*60)
    print('L50 FINAL VERDICT')
    print('='*60)

    best_sIR  = ana['best_sIR']
    sigma_sc  = ana['sigma_sc']
    n_match   = ana['n_match']
    best_r    = ana['best_r']
    best_t    = best_r.get('tension', {}) or {}

    log_diff  = abs(np.log10(best_sIR) - np.log10(sigma_sc))
    in_range  = SIGMA_GRID.min() <= sigma_sc <= SIGMA_GRID.max()

    if log_diff < 0.15:
        sc_verdict = f'MATCH: L50 sigma_IR ≈ sigma_sc ({log_diff:.3f} dex)'
    elif log_diff < 0.5:
        sc_verdict = f'NEAR: L50 sigma_IR near sigma_sc ({log_diff:.3f} dex)'
    else:
        sc_verdict = f'4th-VALUE: L50 sigma_IR differs from sigma_sc ({log_diff:.3f} dex)'

    print(f'\n  sigma_sc (T17)  = {sigma_sc:.3e}  log={np.log10(sigma_sc):.3f}')
    print(f'  L50 best sigma_IR = {best_sIR:.3e}  log={np.log10(best_sIR):.3f}')
    print(f'  Self-consist verdict: {sc_verdict}')
    print(f'\n  H0 tension match pairs: {n_match}/{N_SIG*N_GAM}')
    print(f'  Best H0_CMB = {best_t.get("H0_CMB", np.nan):.2f} km/s/Mpc')
    print(f'  Best H(z={H_BOSS_Z}) = {best_t.get("H_boss_sqt", np.nan):.2f} (obs={H_BOSS_OBS})')
    print(f'  Best tau_ratio = {best_r.get("tau_ratio", np.nan):.4f}')

    # Overall
    if n_match > 0 and log_diff < 0.3:
        verdict = 'Q1 CANDIDATE — sigma_IR consistent with sigma_sc AND tension resolved'
    elif n_match > 0:
        verdict = 'Q2 PARTIAL — tension resolved but sigma_IR inconsistent with sigma_sc'
    elif log_diff < 0.3:
        verdict = 'Q3 SC-ONLY — sigma_IR consistent but no tension resolution'
    else:
        verdict = 'K0 FAIL — no tension resolution AND sigma_IR inconsistent'

    print(f'\n  [VERDICT] {verdict}')

    # Diagnostic table
    print(f'\n  === sigma_0 Diagnostic Table (Updated) ===')
    print(f'  {"Constraint":<25} {"sigma_0":>12}  {"log10":>7}')
    print(f'  {"-"*46}')
    for label, val in [
        ('T17 H0 tension',       SIGMA_T17_TENSION),
        ('T17 self-consist',     SIGMA_T17_SC),
        ('T20 sigma8',           SIGMA_T20_S8),
        ('T22 a_0 (L49)',        SIGMA_T22_A0),
        ('L50 best sigma_IR',    best_sIR),
    ]:
        tag = '  <-- THIS RUN' if 'L50' in label else ''
        print(f'  {label:<25} {val:>12.3e}  {np.log10(val):>7.3f}{tag}')

    sys.stdout.flush()
    return {'verdict': verdict, 'sc_verdict': sc_verdict,
            'n_match': n_match, 'best_sIR': best_sIR,
            'log_diff': log_diff}


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('='*60)
    print('L50 (T17_v4): sigma_0(k) Model IV — sigma_IR Grid Scan')
    print(f'Grid: {N_SIG}x{N_GAM}={N_SIG*N_GAM} pts | {N_WORKERS} workers')
    print(f'sigma_IR: [{SIGMA_GRID[0]:.0e}, {SIGMA_GRID[-1]:.0e}]  (10^6 to 10^10)')
    print(f'sigma_UV={SIGMA_UV:.2e}  k_t={K_T:.0e} Mpc^-1 (fixed)')
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
        task3_visualize(scan, ana)
        verdict = task4_verdict(scan, ana)

    finally:
        pool.close()
        pool.join()

    # Summary
    print('\n' + '='*60)
    print('L50 RESULTS SUMMARY')
    print('='*60)
    print(f"Grid: {N_SIG}x{N_GAM}  Valid: {int(scan.get('valid', np.array([])).sum())}/{N_SIG*N_GAM}")
    print(f"H0_CMB match: {ana.get('n_match', 0)}")
    print(f"Best sigma_IR: {ana.get('best_sIR', 0):.3e}")
    print(f"Verdict: {verdict.get('verdict', 'N/A')}")

    save = {
        'n_match':    ana.get('n_match', 0),
        'best_sIR':   ana.get('best_sIR', 0),
        'sigma_sc':   ana.get('sigma_sc', 0),
        'log_diff':   verdict.get('log_diff', 0),
        'verdict':    verdict.get('verdict', ''),
        'sc_verdict': verdict.get('sc_verdict', ''),
        'params': {
            'H0_local':  H0_TARGET,
            'H0_CMB_PL': H0_CMB_PL,
            'sigma_UV':  SIGMA_UV,
            'k_t_Mpc':   K_T,
            'N_SIG':     N_SIG,
            'N_GAM':     N_GAM,
        },
        'refs': {
            'T17_tension': SIGMA_T17_TENSION,
            'T17_sc':      SIGMA_T17_SC,
            'T20_s8':      SIGMA_T20_S8,
            'T22_a0_L49':  SIGMA_T22_A0,
        },
    }
    out_json = os.path.join(_SCRIPT_DIR, 'l50_results.json')
    with open(out_json, 'w') as f:
        json.dump(_jsonify(save), f, indent=2)
    print(f'Saved: {out_json}')
