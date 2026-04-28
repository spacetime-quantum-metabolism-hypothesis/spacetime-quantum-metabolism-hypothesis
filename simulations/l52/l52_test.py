#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L52 (T20_v4): sigma_0(k) Model IV sigma_8 Validation
=====================================================
sigma_eff(k=0.13 Mpc^-1) -> growth ODE -> sigma_8 prediction
Grid: 25x25 sigma_IR x k_t = 625 pts, 8 workers
Output: l52_main.png, l52_results.json
"""

import os, sys, time, json, warnings
import numpy as np
from scipy.integrate import solve_ivp
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

H0_KMS   = 70.0         # km/s/Mpc (fiducial for growth)
H_LITTLE = 0.70
OM_FID   = 0.315
OL_FID   = 0.685

# sigma_8 observational anchors
S8_PLANCK     = 0.811
S8_PLANCK_ERR = 0.006
S8_KIDS       = 0.760
S8_KIDS_ERR   = 0.020

# sigma_0(k) Model IV fixed parameters
SIGMA_UV  = 3.31e9      # m^3/(kg*s), L49 T22 result
K_SIGMA8  = 0.13        # Mpc^-1, k-scale for sigma_8

# SQT friction model
SIGMA_REF = 1.17e8      # m^3/(kg*s), T17 self-consistent sigma_0
ALPHA_FR  = 0.1         # friction coupling (phenomenological)

# L48/L50 reference values for diagnostic
SIGMA_T17_TENSION = 2.34e8
SIGMA_T17_SC      = 1.17e8
SIGMA_T20_S8      = 5.6e7
SIGMA_T22_A0      = 3.31e9
SIGMA_L50_BEST    = 3.04e8

# Grid
N_SIG    = 25
N_KT     = 25
SIGMA_GRID = np.logspace(7, 9.5, N_SIG)    # sigma_IR [m^3/(kg*s)]
KT_GRID    = np.logspace(-4, 0,   N_KT)    # k_t [Mpc^-1]
N_WORKERS  = 8

# Growth ODE integration range
A_INI  = 1e-3    # z = 999
A_FIN  = 1.0     # z = 0


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
# sigma_0(k) Lorentzian (Model IV, Candidate B)
# ──────────────────────────────────────────────────────────────────────────────

def sigma_k(k_Mpc, sigma_IR, sigma_UV=SIGMA_UV, k_t=1e-2):
    """sigma_0(k) Lorentzian: k->0 = sigma_IR, k>>k_t -> sigma_UV."""
    x2 = (k_Mpc / k_t) ** 2
    return (sigma_IR + sigma_UV * x2) / (1.0 + x2)


# ──────────────────────────────────────────────────────────────────────────────
# Structure Growth ODE
# ──────────────────────────────────────────────────────────────────────────────

def _growth_ode(a, y, friction_factor, om, ol):
    """
    delta'' + friction_factor*(3/a + H'/H)*delta' - (3*om)/(2*a^5*E^2)*delta = 0
    y = [delta, ddelta_da]
    H'/H = dH/da / H = -3*om/(2*a^4*E^2)
    """
    delta, ddelta_da = y[0], y[1]

    E2 = om / a**3 + ol
    if E2 <= 0.0:
        return [0.0, 0.0]

    H_prime_H = -1.5 * om / (a**4 * E2)           # dH/da / H
    coeff_fric = friction_factor * (3.0/a + H_prime_H)
    coeff_coup = 1.5 * om / (a**5 * E2)            # 4piG rho_m / (a^2 H^2)

    return [ddelta_da,
            -coeff_fric * ddelta_da + coeff_coup * delta]


def _solve_growth(friction_factor, om=OM_FID, ol=OL_FID):
    """Solve growth ODE; return D+(a=1) or None."""
    # Matter domination IC: delta ~ a, d(delta)/da = 1
    y0 = [A_INI, 1.0]
    try:
        sol = solve_ivp(
            _growth_ode, [A_INI, A_FIN], y0,
            args=(friction_factor, om, ol),
            method='Radau',
            rtol=1e-9, atol=1e-12,
            dense_output=False,
        )
    except Exception:
        return None

    if not sol.success:
        return None

    D_raw = sol.y[0]
    if not (np.all(np.isfinite(D_raw)) and np.all(D_raw > 0.0)):
        return None

    return float(D_raw[-1])


# LCDM reference growth factor — computed once at module import (once per worker process)
_D_LCDM_REF = _solve_growth(1.0)


# ──────────────────────────────────────────────────────────────────────────────
# Worker
# ──────────────────────────────────────────────────────────────────────────────

def _worker(args):
    warnings.filterwarnings('ignore')
    np.seterr(all='ignore')
    sigma_IR, k_t = args

    # sigma_eff at the structure formation scale k=0.13 Mpc^-1
    sigma_eff = float(sigma_k(K_SIGMA8, sigma_IR, SIGMA_UV, k_t))

    # SQT friction factor (LCDM limit at sigma_eff = SIGMA_REF)
    ff = 1.0 + ALPHA_FR * np.log10(max(sigma_eff, 1e-30) / SIGMA_REF)
    ff = max(ff, 0.1)   # clamp: unphysical negative friction not allowed

    # LCDM reference (cached at module import — once per worker process)
    D_lcdm = _D_LCDM_REF
    if D_lcdm is None or D_lcdm <= 0.0:
        return {'sigma_IR': float(sigma_IR), 'k_t': float(k_t), 'success': False}

    # SQT growth
    D_sqt = _solve_growth(ff)
    if D_sqt is None or D_sqt <= 0.0:
        return {'sigma_IR': float(sigma_IR), 'k_t': float(k_t), 'success': False}

    sigma8_sqt = S8_PLANCK * (D_sqt / D_lcdm)

    chi2_planck = ((sigma8_sqt - S8_PLANCK) / S8_PLANCK_ERR) ** 2
    chi2_kids   = ((sigma8_sqt - S8_KIDS)   / S8_KIDS_ERR)   ** 2
    chi2_min    = min(chi2_planck, chi2_kids)

    return {
        'sigma_IR':      float(sigma_IR),
        'k_t':           float(k_t),
        'sigma_eff':     sigma_eff,
        'friction_ff':   float(ff),
        'D_sqt':         float(D_sqt),
        'D_lcdm':        float(D_lcdm),
        'sigma8_sqt':    float(sigma8_sqt),
        'chi2_planck':   float(chi2_planck),
        'chi2_kids':     float(chi2_kids),
        'chi2_min':      float(chi2_min),
        'success':       True,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Pre-task
# ──────────────────────────────────────────────────────────────────────────────

def pretask():
    print('\n' + '='*60)
    print('Pre-task: L52 sigma_0(k) Model IV sigma_8 Validation')
    print('='*60)

    # Verify LCDM growth factor
    D_lcdm = _solve_growth(1.0)
    print(f'\n[P1] D_LCDM(a=1) = {D_lcdm:.6f}  (IC: delta=1e-3, d/da=1 at a=1e-3)')

    # sigma_eff at k=0.13 for a few reference points
    for sIR_name, sIR in [('sigma_sc=1.17e8', SIGMA_REF), ('sigma_T17t=2.34e8', SIGMA_T17_TENSION),
                           ('sigma_L50=3.04e8', SIGMA_L50_BEST), ('sigma_UV=3.31e9', SIGMA_UV)]:
        for kt in [1e-2, 1e-1]:
            se = sigma_k(K_SIGMA8, sIR, SIGMA_UV, kt)
            ff = 1.0 + ALPHA_FR * np.log10(max(se, 1e-30) / SIGMA_REF)
            D_sqt = _solve_growth(max(ff, 0.1))
            s8 = S8_PLANCK * (D_sqt / D_lcdm) if (D_sqt and D_lcdm) else float('nan')
            print(f'[P2] {sIR_name:<22}  k_t={kt:.0e}  '
                  f'sigma_eff={se:.2e}  ff={ff:.4f}  sigma8={s8:.4f}')

    # Lorentzian limits check
    print(f'\n[P3] sigma_k(k=0.13, sigma_IR=sigma_ref, k_t=1e-2) = '
          f'{sigma_k(0.13, SIGMA_REF, k_t=1e-2):.3e}  (k>>k_t: should -> sigma_UV={SIGMA_UV:.2e})')
    print(f'[P3] sigma_k(k=0.13, sigma_IR=sigma_ref, k_t=10.0) = '
          f'{sigma_k(0.13, SIGMA_REF, k_t=10.0):.3e}  (k<<k_t: should -> sigma_IR={SIGMA_REF:.2e})')

    print(f'\n[P4] L48 T20 reference: sigma_eff=5.6e7  log={np.log10(5.6e7):.3f}')
    print(f'[P4] sigma_UV={SIGMA_UV:.2e}  log={np.log10(SIGMA_UV):.3f}  '
          f'gap={np.log10(SIGMA_UV/5.6e7):.2f} dex')
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 1: Grid Scan
# ──────────────────────────────────────────────────────────────────────────────

def task1_scan(pool):
    print('\n' + '='*60)
    print(f'Task 1: sigma_IR x k_t Grid Scan ({N_SIG}x{N_KT}={N_SIG*N_KT} pts)')
    print('='*60)
    t0 = time.time()

    param_list = [(s, k) for s in SIGMA_GRID for k in KT_GRID]
    print(f'  Dispatching {len(param_list)} tasks to {N_WORKERS} workers...')
    sys.stdout.flush()

    results = pool.map(_worker, param_list)
    elapsed = time.time() - t0
    print(f'  Done in {elapsed:.1f}s')

    n_pts = len(results)
    s8_arr    = np.full(n_pts, np.nan)
    seff_arr  = np.full(n_pts, np.nan)
    ff_arr    = np.full(n_pts, np.nan)
    chi2p_arr = np.full(n_pts, np.nan)
    chi2k_arr = np.full(n_pts, np.nan)
    chi2m_arr = np.full(n_pts, np.nan)
    valid     = np.zeros(n_pts, dtype=bool)

    for i, r in enumerate(results):
        if r.get('success'):
            s8_arr[i]    = r['sigma8_sqt']
            seff_arr[i]  = r['sigma_eff']
            ff_arr[i]    = r['friction_ff']
            chi2p_arr[i] = r['chi2_planck']
            chi2k_arr[i] = r['chi2_kids']
            chi2m_arr[i] = r['chi2_min']
            valid[i]     = True

    n_valid = int(valid.sum())
    print(f'  Valid: {n_valid}/{n_pts}')
    if n_valid > 0:
        print(f'  sigma8 range: [{np.nanmin(s8_arr[valid]):.4f}, {np.nanmax(s8_arr[valid]):.4f}]')
        print(f'  sigma_eff range: [{np.nanmin(seff_arr[valid]):.2e}, {np.nanmax(seff_arr[valid]):.2e}]')
    sys.stdout.flush()

    return {
        'results':    results,
        'sigma8':     s8_arr,
        'sigma_eff':  seff_arr,
        'friction_ff':ff_arr,
        'chi2_planck':chi2p_arr,
        'chi2_kids':  chi2k_arr,
        'chi2_min':   chi2m_arr,
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
    s8_arr  = scan['sigma8']
    chi2m   = scan['chi2_min']
    results = scan['results']

    # Planck matching: |sigma8 - 0.811| < 2*err
    tol_pl = 2.0 * S8_PLANCK_ERR
    match_planck = valid & (np.abs(s8_arr - S8_PLANCK) < tol_pl)
    # KiDS matching
    tol_ki = 2.0 * S8_KIDS_ERR
    match_kids   = valid & (np.abs(s8_arr - S8_KIDS)   < tol_ki)

    n_pl = int(match_planck.sum())
    n_ki = int(match_kids.sum())
    print(f'\n  Planck sigma8={S8_PLANCK} +/-{tol_pl:.3f}: {n_pl}/{N_SIG*N_KT} matches')
    print(f'  KiDS   sigma8={S8_KIDS} +/-{tol_ki:.3f}: {n_ki}/{N_SIG*N_KT} matches')

    # Best chi2
    chi2_valid = np.where(valid, chi2m, np.inf)
    if not np.any(valid):
        print('  ERROR: no valid points')
        return None
    best_idx  = int(np.nanargmin(chi2_valid))
    best_r    = results[best_idx]

    best_sIR  = best_r['sigma_IR']
    best_kt   = best_r['k_t']
    best_seff = best_r.get('sigma_eff', np.nan)
    best_s8   = best_r.get('sigma8_sqt', np.nan)
    best_ff   = best_r.get('friction_ff', np.nan)

    print(f'\n  Best chi2 point:')
    print(f'  sigma_IR = {best_sIR:.3e}  k_t = {best_kt:.3e} Mpc^-1')
    print(f'  sigma_eff(k=0.13) = {best_seff:.3e}  (log={np.log10(best_seff):.3f})')
    print(f'  friction_ff = {best_ff:.4f}')
    print(f'  sigma8_sqt = {best_s8:.4f}  (Planck={S8_PLANCK}, KiDS={S8_KIDS})')
    print(f'  chi2_min = {chi2_valid[best_idx]:.3f}')

    # Compare sigma_eff to L48 T20
    gap_dex = np.log10(best_seff / SIGMA_T20_S8) if best_seff > 0 else np.nan
    print(f'\n  L48 T20 sigma_eff = {SIGMA_T20_S8:.2e}  log={np.log10(SIGMA_T20_S8):.3f}')
    print(f'  L52 best sigma_eff = {best_seff:.2e}  log={np.log10(best_seff):.3f}')
    print(f'  Gap from L48 T20: {gap_dex:.3f} dex')

    sys.stdout.flush()
    return {
        'n_planck': n_pl,
        'n_kids':   n_ki,
        'match_planck': match_planck,
        'match_kids':   match_kids,
        'best_idx':  best_idx,
        'best_sIR':  best_sIR,
        'best_kt':   best_kt,
        'best_seff': best_seff,
        'best_s8':   best_s8,
        'best_ff':   best_ff,
        'gap_dex':   float(gap_dex) if np.isfinite(gap_dex) else None,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Task 3: Visualization (6-panel)
# ──────────────────────────────────────────────────────────────────────────────

BLUE = '#1f4e79'
GRAY = '#7f7f7f'
RED  = '#c00000'
ORNG = '#e65100'


def task3_visualize(scan, ana):
    print('\n' + '='*60)
    print('Task 3: 6-Panel Visualization')
    print('='*60)

    ns, nk = N_SIG, N_KT
    ls = np.log10(SIGMA_GRID)
    lk = np.log10(KT_GRID)
    ls_m, lk_m = np.meshgrid(ls, lk, indexing='ij')

    s8_2d   = scan['sigma8'].reshape(ns, nk)
    seff_2d = scan['sigma_eff'].reshape(ns, nk)
    chi2_2d = scan['chi2_min'].reshape(ns, nk)
    valid_2d= scan['valid'].reshape(ns, nk)

    def _nan(arr):
        return np.where(np.isfinite(arr), arr, np.nan)

    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    fig.suptitle(
        f'L52 (T20_v4): sigma_0(k) Model IV sigma_8 Validation\n'
        f'sigma_UV={SIGMA_UV:.1e}  k_sigma8=0.13 Mpc^-1  alpha_fr={ALPHA_FR}',
        fontsize=12, fontweight='bold')

    # ── (a) sigma8 contour ──
    ax = axes[0, 0]
    cf = ax.contourf(ls_m, lk_m, _nan(s8_2d), levels=50, cmap='RdYlGn',
                     vmin=0.6, vmax=1.0)
    plt.colorbar(cf, ax=ax, label='sigma_8 (SQT)')
    cs_pl = ax.contour(ls_m, lk_m, _nan(s8_2d), levels=[S8_PLANCK], colors=RED, linewidths=2)
    ax.clabel(cs_pl, fmt=f'Planck {S8_PLANCK}', fontsize=8)
    cs_ki = ax.contour(ls_m, lk_m, _nan(s8_2d), levels=[S8_KIDS], colors=ORNG, linewidths=2)
    ax.clabel(cs_ki, fmt=f'KiDS {S8_KIDS}', fontsize=8)
    ax.axvline(np.log10(SIGMA_REF), color=BLUE, ls='--', lw=1.5, label='sigma_sc')
    ax.axvline(np.log10(SIGMA_L50_BEST), color='purple', ls=':', lw=1.5, label='L50 best')
    ax.set_xlabel('log10(sigma_IR) [m^3/(kg*s)]')
    ax.set_ylabel('log10(k_t) [Mpc^-1]')
    ax.set_title('(a) sigma_8 prediction')
    ax.legend(fontsize=7)

    # ── (b) chi2 contour ──
    ax = axes[0, 1]
    log_chi2 = np.log10(np.maximum(_nan(chi2_2d), 1e-4))
    cf = ax.contourf(ls_m, lk_m, log_chi2, levels=50, cmap='viridis_r')
    plt.colorbar(cf, ax=ax, label='log10(chi2_min)')
    best_idx = ana['best_idx']
    bi = best_idx // nk
    bj = best_idx %  nk
    ax.scatter([ls[bi]], [lk[bj]], color=RED, s=100, zorder=5, label='best fit')
    ax.axvline(np.log10(SIGMA_REF), color=BLUE, ls='--', lw=1.5, label='sigma_sc')
    ax.set_xlabel('log10(sigma_IR)')
    ax.set_ylabel('log10(k_t) [Mpc^-1]')
    ax.set_title('(b) chi2 (min of Planck+KiDS)')
    ax.legend(fontsize=7)

    # ── (c) sigma_eff(k=0.13) contour ──
    ax = axes[0, 2]
    log_seff = np.log10(np.maximum(_nan(seff_2d), 1e-30))
    cf = ax.contourf(ls_m, lk_m, log_seff, levels=50, cmap='plasma')
    plt.colorbar(cf, ax=ax, label='log10(sigma_eff at k=0.13)')
    ax.axhline(np.log10(K_SIGMA8), color=RED, ls='--', lw=1, alpha=0.5, label='k_t=k_sigma8=0.13')
    # L48 T20 reference line
    cs_t20 = ax.contour(ls_m, lk_m, log_seff,
                         levels=[np.log10(SIGMA_T20_S8)], colors='lime', linewidths=2)
    ax.clabel(cs_t20, fmt='L48 T20=5.6e7', fontsize=8)
    ax.axvline(np.log10(SIGMA_REF), color=BLUE, ls='--', lw=1.5, label='sigma_sc')
    ax.set_xlabel('log10(sigma_IR)')
    ax.set_ylabel('log10(k_t) [Mpc^-1]')
    ax.set_title('(c) sigma_eff at k=0.13 Mpc^-1')
    ax.legend(fontsize=7)

    # ── (d) sigma_0(k) curves ──
    ax = axes[1, 0]
    k_range = np.logspace(-6, 2, 300)
    curves = [
        (SIGMA_T17_SC,     1e-2, BLUE,    f'sigma_sc={SIGMA_T17_SC:.1e}'),
        (SIGMA_L50_BEST,   1e-2, 'purple', f'L50 best={SIGMA_L50_BEST:.1e}'),
        (ana['best_sIR'],  ana['best_kt'], RED, f'L52 best sIR={ana["best_sIR"]:.1e} k_t={ana["best_kt"]:.1e}'),
    ]
    for sIR, kt, col, lbl in curves:
        sk_vals = sigma_k(k_range, sIR, SIGMA_UV, kt)
        ax.loglog(k_range, sk_vals, color=col, lw=2, label=lbl)
    ax.axvline(K_SIGMA8,       color=RED,  ls='--', lw=1.5, label=f'k_sigma8={K_SIGMA8}')
    ax.axhline(SIGMA_T20_S8,   color='lime', ls=':', lw=1.5, label=f'L48 T20=5.6e7')
    ax.axhline(SIGMA_UV,       color=GRAY, ls=':',  lw=1,   label=f'sigma_UV={SIGMA_UV:.1e}')
    ax.set_xlabel('k [Mpc^-1]')
    ax.set_ylabel('sigma_0(k) [m^3/(kg*s)]')
    ax.set_title('(d) sigma_0(k) Model IV — L52 curves')
    ax.legend(fontsize=6)
    ax.grid(alpha=0.3)

    # ── (e) sigma8 vs sigma_IR slices ──
    ax = axes[1, 1]
    for kt_target, col_s, ls_s in [(1e-4, 'navy', '-'), (1e-3, BLUE, '-'),
                                    (1e-2, 'steelblue', '--'), (1e-1, 'teal', ':'),
                                    (1.0,  GRAY, ':')]:
        idx_k = int(np.argmin(np.abs(KT_GRID - kt_target)))
        s8_slice = s8_2d[:, idx_k]
        valid_s  = np.isfinite(s8_slice)
        if valid_s.sum() > 2:
            ax.plot(ls[valid_s], s8_slice[valid_s], color=col_s, ls=ls_s, lw=1.5,
                    label=f'k_t={KT_GRID[idx_k]:.1e}')
    ax.axhline(S8_PLANCK, color=RED,  ls='--', lw=2, label=f'Planck {S8_PLANCK}')
    ax.axhline(S8_KIDS,   color=ORNG, ls='--', lw=2, label=f'KiDS {S8_KIDS}')
    ax.axvline(np.log10(SIGMA_REF), color=BLUE, ls=':', lw=1, alpha=0.7, label='sigma_sc')
    ax.set_xlabel('log10(sigma_IR)')
    ax.set_ylabel('sigma_8 (SQT)')
    ax.set_title('(e) sigma_8 vs sigma_IR (k_t slices)')
    ax.legend(fontsize=7)
    ax.grid(alpha=0.3)

    # ── (f) Diagnostic bar chart ──
    ax = axes[1, 2]
    refs = [
        ('T17 H0\ntension',  SIGMA_T17_TENSION, '#c00000'),
        ('T17 self-\nconsist', SIGMA_T17_SC,     BLUE),
        ('T20 s8\n(L48)',    SIGMA_T20_S8,       '#2e7d32'),
        ('T22 a0\n(L49)',    SIGMA_T22_A0,       '#8B4513'),
        ('L50\nbest',        SIGMA_L50_BEST,     '#e65100'),
        ('L52\nbest',        ana['best_sIR'],    '#9c27b0'),
    ]
    labels_bar = [r[0] for r in refs]
    values_bar = [np.log10(r[1]) for r in refs]
    colors_bar = [r[2] for r in refs]
    bars = ax.bar(labels_bar, values_bar, color=colors_bar,
                  alpha=0.8, edgecolor='k', linewidth=0.5)
    ax.axhline(np.log10(SIGMA_T17_SC), color=BLUE, ls='--', lw=1.5, alpha=0.5, label='sigma_sc')
    ax.axhline(np.log10(SIGMA_T20_S8), color='lime', ls=':', lw=1.5, alpha=0.8, label='L48 T20')
    for bar, val in zip(bars, values_bar):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.04,
                f'{10**val:.2e}', ha='center', va='bottom', fontsize=7, rotation=60)
    ax.set_ylabel('log10(sigma_0) [m^3/(kg*s)]')
    ax.set_title('(f) sigma_0 Diagnostic Table')
    ax.set_ylim(7, 10.5)
    ax.legend(fontsize=7)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    out = os.path.join(_SCRIPT_DIR, 'l52_main.png')
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved: {out}')
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 4: Verdict
# ──────────────────────────────────────────────────────────────────────────────

def task4_verdict(scan, ana):
    print('\n' + '='*60)
    print('L52 FINAL VERDICT')
    print('='*60)

    best_sIR  = ana['best_sIR']
    best_kt   = ana['best_kt']
    best_seff = ana['best_seff']
    best_s8   = ana['best_s8']
    n_pl      = ana['n_planck']
    n_ki      = ana['n_kids']
    gap_dex   = ana.get('gap_dex') or float('nan')

    print(f'\n  Best sigma_IR = {best_sIR:.3e}  log={np.log10(best_sIR):.3f}')
    print(f'  Best k_t      = {best_kt:.3e} Mpc^-1  log={np.log10(best_kt):.3f}')
    print(f'  sigma_eff(k=0.13) = {best_seff:.3e}  log={np.log10(best_seff):.3f}')
    print(f'  sigma8_sqt = {best_s8:.4f}')
    print(f'  gap from L48 T20: {gap_dex:.3f} dex')
    print(f'  Planck match pairs: {n_pl}  KiDS match pairs: {n_ki}')

    # sigma_eff vs L48 T20 consistency
    if abs(gap_dex) < 0.3:
        seff_verdict = f'MATCH: sigma_eff consistent with L48 T20 ({gap_dex:.3f} dex)'
    elif abs(gap_dex) < 1.0:
        seff_verdict = f'NEAR: sigma_eff near L48 T20 ({gap_dex:.3f} dex)'
    else:
        seff_verdict = f'FAIL: sigma_eff inconsistent with L48 T20 ({gap_dex:.3f} dex)'

    print(f'\n  sigma_eff verdict: {seff_verdict}')

    # Overall verdict
    any_match = (n_pl + n_ki) > 0
    if any_match and abs(gap_dex) < 0.5:
        verdict = 'Q1 CANDIDATE — sigma_8 matched AND sigma_eff near L48 T20'
    elif any_match:
        verdict = 'Q2 PARTIAL — sigma_8 matched but sigma_eff inconsistent with L48 T20'
    elif abs(gap_dex) < 0.5:
        verdict = 'Q3 SEFF-ONLY — sigma_eff consistent but no sigma_8 match'
    else:
        verdict = 'K0 FAIL — no sigma_8 match AND sigma_eff inconsistent with L48 T20'

    print(f'\n  [VERDICT] {verdict}')

    # Diagnostic table
    print(f'\n  === sigma_0 Diagnostic Table (Updated) ===')
    print(f'  {"Constraint":<28} {"sigma_0":>12}  {"log10":>7}')
    print(f'  {"-"*50}')
    rows = [
        ('T17 H0 tension',           SIGMA_T17_TENSION),
        ('T17 self-consist',         SIGMA_T17_SC),
        ('T20 sigma8 (L48)',         SIGMA_T20_S8),
        ('T22 a_0 (L49)',            SIGMA_T22_A0),
        ('L50 best sigma_IR',        SIGMA_L50_BEST),
        ('L52 best sigma_IR',        best_sIR),
    ]
    for label, val in rows:
        tag = '  <-- THIS RUN' if 'L52' in label else ''
        print(f'  {label:<28} {val:>12.3e}  {np.log10(val):>7.3f}{tag}')

    print(f'\n  L52 best k_t     = {best_kt:.3e} Mpc^-1  log={np.log10(best_kt):.3f}  <-- THIS RUN')
    print(f'  L52 sigma_eff    = {best_seff:.3e}  log={np.log10(best_seff):.3f}  <-- THIS RUN')
    print(f'  L52 sigma8_sqt   = {best_s8:.4f}')

    sys.stdout.flush()
    return {
        'verdict':       verdict,
        'seff_verdict':  seff_verdict,
        'n_planck':      n_pl,
        'n_kids':        n_ki,
        'best_sIR':      best_sIR,
        'best_kt':       best_kt,
        'best_seff':     best_seff,
        'best_s8':       best_s8,
        'gap_dex':       gap_dex,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('='*60)
    print('L52 (T20_v4): sigma_0(k) Model IV sigma_8 Validation')
    print(f'Grid: {N_SIG}x{N_KT}={N_SIG*N_KT} pts | {N_WORKERS} workers')
    print(f'sigma_IR: [10^7, 10^9.5]  k_t: [1e-4, 1.0] Mpc^-1')
    print(f'sigma_UV={SIGMA_UV:.2e}  k_sigma8=0.13 Mpc^-1  alpha_fr={ALPHA_FR}')
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

    # Summary
    print('\n' + '='*60)
    print('L52 RESULTS SUMMARY')
    print('='*60)
    print(f"Grid: {N_SIG}x{N_KT}  Valid: {int(scan.get('valid', np.array([])).sum())}/{N_SIG*N_KT}")
    print(f"Planck match: {ana.get('n_planck', 0)}  KiDS match: {ana.get('n_kids', 0)}")
    print(f"Best sigma_IR: {ana.get('best_sIR', 0):.3e}")
    print(f"Best k_t: {ana.get('best_kt', 0):.3e}")
    print(f"Best sigma_eff(k=0.13): {ana.get('best_seff', 0):.3e}")
    print(f"Best sigma8: {ana.get('best_s8', 0):.4f}")
    print(f"Verdict: {verdict.get('verdict', 'N/A')}")

    save = {
        'n_planck':   ana.get('n_planck', 0),
        'n_kids':     ana.get('n_kids', 0),
        'best_sIR':   ana.get('best_sIR', 0),
        'best_kt':    ana.get('best_kt', 0),
        'best_seff':  ana.get('best_seff', 0),
        'best_s8':    ana.get('best_s8', 0),
        'gap_dex':    ana.get('gap_dex', 0),
        'verdict':    verdict.get('verdict', ''),
        'seff_verdict': verdict.get('seff_verdict', ''),
        'params': {
            'sigma_UV':   SIGMA_UV,
            'k_sigma8':   K_SIGMA8,
            'sigma_ref':  SIGMA_REF,
            'alpha_fr':   ALPHA_FR,
            'N_SIG':      N_SIG,
            'N_KT':       N_KT,
        },
        'refs': {
            'T17_tension': SIGMA_T17_TENSION,
            'T17_sc':      SIGMA_T17_SC,
            'T20_s8':      SIGMA_T20_S8,
            'T22_a0':      SIGMA_T22_A0,
            'L50_best':    SIGMA_L50_BEST,
        },
    }
    out_json = os.path.join(_SCRIPT_DIR, 'l52_results.json')
    with open(out_json, 'w') as f:
        json.dump(_jsonify(save), f, indent=2)
    print(f'Saved: {out_json}')
