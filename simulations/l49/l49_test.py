#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L49 (T22_full): SPARC 175-Galaxy Rotation Curve Fit
=====================================================
Purpose : Extract a_0, beta, sigma_0 from SPARC rotation curves.
          Compare SQT (simple MOND interp) vs MOND vs NFW.
          Diagnose sigma_0 consistency with T17/T20 results.
Input   : SPARC Rotmod_LTG.zip (auto-download)
Output  : l49_results.json, l49_main.png, l49_sigma8_diag.png
Parallel: 8 workers (joblib, spawn)
Est.time: 5-15 min depending on network + fit convergence
"""

import os, sys, time, json, warnings, zipfile, io
import numpy as np
from pathlib import Path
from scipy.optimize import minimize, curve_fit
from scipy.stats import norm as sp_norm
import multiprocessing as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')
np.seterr(all='ignore')
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

_SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = _SCRIPT_DIR / 'data' / 'sparc'

# ──────────────────────────────────────────────────────────────────────────────
# Physical Constants
# ──────────────────────────────────────────────────────────────────────────────
G_KPC   = 4.302e-6      # kpc (km/s)^2 / M_sun
G_SI    = 6.674e-11     # m^3 kg^-1 s^-2
C_KMS   = 2.998e5       # km/s
C_SI    = 2.998e8       # m/s
H0_KMS  = 73.8          # km/s/Mpc (T17 value, for tau_q)
Mpc_m   = 3.0857e22     # m per Mpc
kmsM    = 1e3 / Mpc_m   # 1 km/s/Mpc in s^-1

# MOND standard a_0 = 1.2e-10 m/s^2 converted to (km/s)^2/kpc
# 1 (km/s)^2/kpc = 1e6 m^2/s^2 / 3.086e19 m = 3.241e-14 m/s^2
KPC_CONV = 3.241e-14    # 1 (km/s)^2/kpc in m/s^2
A0_SI    = 1.2e-10      # m/s^2 (MOND standard)
A0_KPC   = A0_SI / KPC_CONV  # (km/s)^2/kpc ~= 3703

# Critical density at H0=70 in M_sun/kpc^3
H0_70_SI = 70e3 / Mpc_m
RHO_CRIT_KPC = 3 * H0_70_SI**2 / (8 * np.pi * G_SI) * (3.086e19)**3 / 1.989e30

# T17/T20 reference sigma_0 values [m^3/(kg*s)]
SIGMA_T17_TENSION = 2.34e8
SIGMA_T17_SC      = 1.17e8
SIGMA_T20_S8      = 5.6e7

N_WORKERS = 8

# ──────────────────────────────────────────────────────────────────────────────
# SPARC Data Download & Parse
# ──────────────────────────────────────────────────────────────────────────────

SPARC_URL = "https://astroweb.cwru.edu/SPARC/Rotmod_LTG.zip"


def download_sparc():
    """Download and extract SPARC rotmod data. Returns path to .dat directory."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # SPARC zip extracts .dat files directly into DATA_DIR (no subdirectory)
    if any(DATA_DIR.glob('*_rotmod.dat')):
        n = len(list(DATA_DIR.glob('*_rotmod.dat')))
        print(f'  SPARC already downloaded ({n} .dat files)')
        return DATA_DIR

    print(f'  Downloading SPARC from {SPARC_URL} ...')
    try:
        import urllib.request
        with urllib.request.urlopen(SPARC_URL, timeout=120) as resp:
            data = resp.read()
        print(f'  Downloaded {len(data)/1e6:.1f} MB')
        z = zipfile.ZipFile(io.BytesIO(data))
        z.extractall(DATA_DIR)
        n = len(list(DATA_DIR.glob('*_rotmod.dat')))
        print(f'  Extracted {n} .dat files to {DATA_DIR}')
        return DATA_DIR if n > 0 else None
    except Exception as e:
        print(f'  Download failed: {e}')
        return None


def parse_sparc_file(filepath):
    """
    Parse a single SPARC .dat file.
    Returns dict with arrays or None on failure.
    Columns: Rad Vobs errV Vgas Vdisk Vbul SBdisk SBbul
    """
    try:
        rows = []
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split()
                if len(parts) >= 6:
                    row = [float(x) for x in parts[:8]]
                    while len(row) < 8:
                        row.append(0.0)
                    rows.append(row)
        if len(rows) < 3:
            return None
        arr = np.array(rows, dtype=float)   # always (N,8), no ragged arrays
        # Floor errV to prevent division by zero
        errV = np.maximum(arr[:, 2], 1.0)
        return {
            'name':   filepath.stem,
            'Rad':    arr[:, 0],
            'Vobs':   arr[:, 1],
            'errV':   errV,
            'Vgas':   arr[:, 3],
            'Vdisk':  arr[:, 4],
            'Vbul':   arr[:, 5],
            'SBdisk': arr[:, 6] if arr.shape[1] > 6 else np.zeros(len(arr)),
            'SBbul':  arr[:, 7] if arr.shape[1] > 7 else np.zeros(len(arr)),
        }
    except Exception:
        return None


# ──────────────────────────────────────────────────────────────────────────────
# Rotation Curve Models
# ──────────────────────────────────────────────────────────────────────────────

def _v_bary2(g, Upsilon_d, Upsilon_b=None):
    """Baryonic v^2 (km/s)^2 at each radius."""
    if Upsilon_b is None:
        Upsilon_b = Upsilon_d
    return g['Vgas']**2 + Upsilon_d * g['Vdisk']**2 + Upsilon_b * g['Vbul']**2


def _v_sqt(r, a_N, a_0):
    """
    SQT rotation velocity: simple MOND interpolation.
    a_N  : baryonic acceleration [(km/s)^2/kpc]
    a_0  : critical acceleration [(km/s)^2/kpc]
    Returns v_model [km/s].
    """
    a_N  = np.maximum(a_N,  0.0)
    a_0  = max(a_0, 1e-20)
    # a_total = 0.5*(a_N + sqrt(a_N^2 + 4*a_N*a_0))
    a_tot = 0.5 * (a_N + np.sqrt(a_N**2 + 4.0 * a_N * a_0))
    return np.sqrt(np.maximum(a_tot * r, 0.0))


def _v_mond_std(r, a_N, a_0):
    """
    Standard MOND (mu = x/sqrt(1+x^2), solved implicitly).
    Simple form: a_tot s.t. a_tot * mu(a_tot/a_0) = a_N
    Using same simple interpolation for consistency.
    """
    return _v_sqt(r, a_N, a_0)


def _nfw_v2(r, M200, c):
    """
    NFW halo circular velocity^2 [(km/s)^2].
    r [kpc], M200 [M_sun], c: concentration.
    """
    if M200 <= 0 or c <= 0:
        return np.zeros_like(r)
    r200 = (3 * M200 / (4 * np.pi * 200 * RHO_CRIT_KPC))**(1.0/3.0)
    rs   = r200 / c
    gc   = np.log(1 + c) - c / (1 + c)
    if gc <= 0:
        return np.zeros_like(r)
    rho_s = M200 / (4 * np.pi * rs**3 * gc)
    x = r / rs
    x = np.maximum(x, 1e-8)
    # M_NFW(<r) = 4pi*rho_s*rs^3 * [ln(1+x) - x/(1+x)]
    M_nfw = 4 * np.pi * rho_s * rs**3 * (np.log(1 + x) - x / (1 + x))
    M_nfw = np.maximum(M_nfw, 0.0)
    return G_KPC * M_nfw / r


# ──────────────────────────────────────────────────────────────────────────────
# Galaxy Fitting Functions
# ──────────────────────────────────────────────────────────────────────────────

def _chi2(v_obs, v_mod, err):
    return float(np.sum(((v_obs - v_mod) / err)**2))


def fit_sqt(g):
    """
    Fit SQT model: free log_a0, Upsilon_disk.
    Returns dict.
    """
    r    = g['Rad']
    vobs = g['Vobs']
    err  = g['errV']
    n    = len(r)
    if n < 3:
        return None

    best = {'chi2': np.inf}
    LOG_A0_MOND = np.log10(A0_KPC)   # ~3.57 in (km/s)^2/kpc units

    for log_a0_init in [LOG_A0_MOND - 0.5, LOG_A0_MOND, LOG_A0_MOND + 0.5,
                        LOG_A0_MOND - 1.0, LOG_A0_MOND + 1.0]:
        for Up_init in [0.3, 0.7, 1.2]:
            def objective(params):
                la0, Up = params
                # Soft bounds: penalize outside [log(a0)-2, log(a0)+2] dex
                if la0 < LOG_A0_MOND - 3 or la0 > LOG_A0_MOND + 3:
                    return 1e10
                a0   = 10**la0
                Up_  = max(Up, 0.05)
                aN   = _v_bary2(g, Up_) / r
                vm   = _v_sqt(r, aN, a0)
                if not np.all(np.isfinite(vm)):
                    return 1e10
                return _chi2(vobs, vm, err)

            try:
                res = minimize(objective, [log_a0_init, Up_init],
                               method='Nelder-Mead',
                               options={'xatol': 1e-4, 'fatol': 1e-4,
                                        'maxiter': 2000})
                if res.fun < best['chi2']:
                    la0, Up = res.x
                    a0 = 10**la0
                    aN = _v_bary2(g, max(Up, 0.05)) / r
                    vm = _v_sqt(r, aN, a0)
                    best = {
                        'chi2':    res.fun,
                        'dof':     max(n - 2, 1),
                        'log_a0':  float(la0),
                        'a0_kpc':  float(a0),
                        'a0_SI':   float(a0 * KPC_CONV),
                        'Upsilon': float(max(Up, 0.05)),
                        'v_mod':   vm.tolist(),
                        'success': True,
                    }
            except Exception:
                continue

    return best if best.get('success') else None


def fit_mond_fixed(g, a0_kpc=A0_KPC):
    """
    MOND with fixed a_0=1.2e-10 m/s^2, free Upsilon_disk only.
    """
    r    = g['Rad']
    vobs = g['Vobs']
    err  = g['errV']
    n    = len(r)
    if n < 2:
        return None

    best = {'chi2': np.inf}
    for Up_init in [0.3, 0.5, 0.7, 1.0, 1.5]:
        def objective(Up_arr):
            Up = max(float(Up_arr[0]), 0.05)
            aN = _v_bary2(g, Up) / r
            vm = _v_mond_std(r, aN, a0_kpc)
            if not np.all(np.isfinite(vm)):
                return 1e10
            return _chi2(vobs, vm, err)
        try:
            res = minimize(objective, [Up_init], method='Nelder-Mead',
                           options={'xatol': 1e-4, 'fatol': 1e-4, 'maxiter': 1000})
            if res.fun < best['chi2']:
                Up = max(float(res.x[0]), 0.05)
                aN = _v_bary2(g, Up) / r
                vm = _v_mond_std(r, aN, a0_kpc)
                best = {
                    'chi2':    res.fun,
                    'dof':     max(n - 1, 1),
                    'Upsilon': float(Up),
                    'v_mod':   vm.tolist(),
                    'success': True,
                }
        except Exception:
            continue

    return best if best.get('success') else None


def fit_nfw(g):
    """
    NFW+baryonic fit: free log_M200, log_c, Upsilon_disk (3 params).
    """
    r    = g['Rad']
    vobs = g['Vobs']
    err  = g['errV']
    n    = len(r)
    if n < 4:
        return None

    best = {'chi2': np.inf}
    for lM_init in [10.0, 11.0, 12.0]:
        for lc_init in [0.5, 1.0, 1.3]:
            for Up_init in [0.3, 0.7, 1.2]:
                def objective(params):
                    lM, lc, Up = params
                    M200 = 10**lM
                    c_   = max(10**lc, 0.5)
                    Up_  = max(Up, 0.05)
                    v2_b = _v_bary2(g, Up_)
                    v2_n = _nfw_v2(r, M200, c_)
                    v2   = v2_b + v2_n
                    vm   = np.sqrt(np.maximum(v2, 0.0))
                    if not np.all(np.isfinite(vm)):
                        return 1e10
                    return _chi2(vobs, vm, err)
                try:
                    res = minimize(objective, [lM_init, lc_init, Up_init],
                                   method='Nelder-Mead',
                                   options={'xatol': 1e-4, 'fatol': 1e-4,
                                            'maxiter': 3000})
                    if res.fun < best['chi2']:
                        lM, lc, Up = res.x
                        M200 = 10**lM; c_ = max(10**lc, 0.5); Up_ = max(Up, 0.05)
                        v2_b = _v_bary2(g, Up_)
                        v2_n = _nfw_v2(r, M200, c_)
                        vm   = np.sqrt(np.maximum(v2_b + v2_n, 0.0))
                        best = {
                            'chi2':    res.fun,
                            'dof':     max(n - 3, 1),
                            'log_M200': float(lM),
                            'log_c':    float(lc),
                            'Upsilon':  float(Up_),
                            'v_mod':    vm.tolist(),
                            'success':  True,
                        }
                except Exception:
                    continue

    return best if best.get('success') else None


# ──────────────────────────────────────────────────────────────────────────────
# Worker (spawn-safe)
# ──────────────────────────────────────────────────────────────────────────────

def _worker(filepath_str):
    warnings.filterwarnings('ignore')
    np.seterr(all='ignore')
    fp = Path(filepath_str)
    g  = parse_sparc_file(fp)
    if g is None:
        return {'name': fp.stem, 'ok': False, 'reason': 'parse_fail'}
    sqt  = fit_sqt(g)
    mond = fit_mond_fixed(g)
    nfw  = fit_nfw(g)
    # mean SBdisk (environment proxy)
    sb_mean = float(np.nanmean(g['SBdisk'])) if np.any(g['SBdisk'] > 0) else np.nan
    return {
        'name':    g['name'],
        'ok':      True,
        'n_pts':   int(len(g['Rad'])),
        'sqt':     sqt,
        'mond':    mond,
        'nfw':     nfw,
        'sb_mean': sb_mean,
        'r':       g['Rad'].tolist(),
        'vobs':    g['Vobs'].tolist(),
        'errV':    g['errV'].tolist(),
        'Vgas':    g['Vgas'].tolist(),
        'Vdisk':   g['Vdisk'].tolist(),
        'Vbul':    g['Vbul'].tolist(),
    }


# ──────────────────────────────────────────────────────────────────────────────
# Unit Conversion Verification
# ──────────────────────────────────────────────────────────────────────────────

def pretask_units():
    print('\n' + '='*60)
    print('Pre-task: Unit Conversion Verification')
    print('='*60)

    # 1 (km/s)^2/kpc in m/s^2
    conv = 1e6 / 3.086e19
    print(f'\n[U1] 1 (km/s)^2/kpc = {conv:.4e} m/s^2  (expect 3.241e-14)')
    ok1 = abs(conv - 3.241e-14) / 3.241e-14 < 0.01

    a0_kpc_check = A0_SI / conv
    print(f'[U2] a_0 = {A0_SI:.2e} m/s^2 = {a0_kpc_check:.1f} (km/s)^2/kpc  (A0_KPC={A0_KPC:.1f})')
    ok2 = abs(a0_kpc_check - A0_KPC) / A0_KPC < 0.01

    # tau_q at H0=73.8
    H0_si  = H0_KMS * kmsM
    tau_q_sc = G_SI * 4 * np.pi / (3 * H0_si) * 1e0  # wait: tau_q = sigma_sc/(4piG)
    # sigma_sc = G*4pi/(3H0): from tau_q = sigma0/(4pi*G) and tau_q=1/(3H0)
    sigma_sc = G_SI * 4 * np.pi / (3 * H0_si)
    tau_q    = sigma_sc / (4 * np.pi * G_SI)  # = 1/(3H0)
    beta_sc  = A0_SI * tau_q / C_SI
    print(f'\n[U3] sigma_sc (T17) = {sigma_sc:.4e} m^3/(kg*s)')
    print(f'[U4] tau_q at sigma_sc = {tau_q:.4e} s  = 1/(3H0) = {1/(3*H0_si):.4e} s')
    print(f'[U5] beta at MOND a_0  = {beta_sc:.5f}  (expect ~0.056)')

    # sigma_0 from a_0 = beta*c/tau_q
    # sigma_0 = 4pi*G*tau_q = 4pi*G*beta*c/a_0
    sigma_from_a0 = 4 * np.pi * G_SI * beta_sc * C_SI / A0_SI
    print(f'[U6] sigma_0 from a_0  = {sigma_from_a0:.4e} (expect sigma_sc={sigma_sc:.4e})')
    ok3 = abs(sigma_from_a0 - sigma_sc) / sigma_sc < 0.01

    print(f'\n  KPC_CONV = {KPC_CONV:.4e}, ok = {all([ok1,ok2,ok3])}')
    print(f'  rho_crit_kpc = {RHO_CRIT_KPC:.4e} M_sun/kpc^3')
    sys.stdout.flush()
    return {'ok': ok1 and ok2 and ok3, 'sigma_sc': sigma_sc, 'beta_sc': beta_sc}


# ──────────────────────────────────────────────────────────────────────────────
# Task 1: Download + Parse
# ──────────────────────────────────────────────────────────────────────────────

def task1_load():
    print('\n' + '='*60)
    print('Task 1: SPARC Data Download + Parse')
    print('='*60)

    rotmod_dir = download_sparc()
    if rotmod_dir is None or not rotmod_dir.exists():
        print('  SPARC download failed. Exiting.')
        sys.exit(1)

    files = sorted(rotmod_dir.glob('*_rotmod.dat'))
    print(f'  Found {len(files)} .dat files')
    sys.stdout.flush()
    return [str(f) for f in files]


# ──────────────────────────────────────────────────────────────────────────────
# Task 2: Parallel Fit
# ──────────────────────────────────────────────────────────────────────────────

def task2_fit(file_list, pool):
    print('\n' + '='*60)
    print(f'Task 2: Parallel Galaxy Fitting ({len(file_list)} galaxies, {N_WORKERS} workers)')
    print('='*60)
    t0 = time.time()
    sys.stdout.flush()

    results = pool.map(_worker, file_list)

    elapsed = time.time() - t0
    n_ok = sum(1 for r in results if r.get('ok'))
    print(f'  Done in {elapsed:.1f}s.  OK: {n_ok}/{len(results)}')
    sys.stdout.flush()
    return results


# ──────────────────────────────────────────────────────────────────────────────
# Task 3: Analysis
# ──────────────────────────────────────────────────────────────────────────────

def task3_analyze(results):
    print('\n' + '='*60)
    print('Task 3: Analysis — a_0 Distribution + sigma_0 Extraction')
    print('='*60)

    ok_results = [r for r in results if r.get('ok') and r.get('sqt') and r['sqt'].get('success')]

    # --- a_0 distribution ---
    log_a0_arr = np.array([r['sqt']['log_a0'] for r in ok_results])
    a0_si_arr  = np.array([r['sqt']['a0_SI']  for r in ok_results])
    upsilon_arr = np.array([r['sqt']['Upsilon'] for r in ok_results])

    log_a0_mean = float(np.nanmedian(log_a0_arr))
    log_a0_std  = float(np.nanstd(log_a0_arr))
    a0_mean_SI  = float(10**log_a0_mean * KPC_CONV)
    print(f'\n  a_0 distribution ({len(ok_results)} galaxies):')
    print(f'  log10(a_0) median = {log_a0_mean:.3f}  std = {log_a0_std:.3f} dex')
    print(f'  a_0 median = {a0_mean_SI:.3e} m/s^2  (MOND std: {A0_SI:.2e})')
    print(f'  sigma A1 test: {log_a0_std:.3f} dex  '
          f'[{"PASS" if log_a0_std < 0.15 else "WARN" if log_a0_std < 0.25 else "FAIL"}]')

    # --- sigma_0 extraction ---
    H0_si   = H0_KMS * kmsM
    tau_q_sc = 1.0 / (3.0 * H0_si)   # self-consistent tau_q from T17
    # beta = a_0 * tau_q_sc / c  (what beta is needed at sigma_sc to give this a_0)
    beta_arr = a0_si_arr * tau_q_sc / C_SI
    # sigma_0 assuming beta=1: a_0 = 1*c/tau_q → tau_q = c/a_0 → sigma_0 = 4piG*c/a_0
    # This gives a_0-dependent sigma_0 (not circular) — the T22 independent measurement
    sigma_arr = G_SI * 4.0 * np.pi * C_SI / a0_si_arr

    sigma_med = float(np.nanmedian(sigma_arr))
    sigma_std = float(np.nanstd(sigma_arr))
    log_sigma_med = np.log10(sigma_med) if sigma_med > 0 else np.nan
    beta_med = float(np.nanmedian(beta_arr))

    print(f'\n  sigma_0 extraction (beta=1 assumption: sigma_0=4piG*c/a_0):')
    print(f'  beta_sc median (at sigma_sc) = {beta_med:.5f}')
    print(f'  sigma_0 median (beta=1) = {sigma_med:.3e} m^3/(kg*s)  '
          f'log_sigma_0 = {log_sigma_med:.3f}')
    print(f'\n  Comparison with T17/T20:')
    print(f'  T17 H_0 tension: sigma = {SIGMA_T17_TENSION:.2e} '
          f'log={np.log10(SIGMA_T17_TENSION):.3f}  '
          f'ratio={sigma_med/SIGMA_T17_TENSION:.3f}')
    print(f'  T17 self-consist: sigma = {SIGMA_T17_SC:.2e} '
          f'log={np.log10(SIGMA_T17_SC):.3f}  '
          f'ratio={sigma_med/SIGMA_T17_SC:.3f}')
    print(f'  T20 sigma_8:     sigma = {SIGMA_T20_S8:.2e} '
          f'log={np.log10(SIGMA_T20_S8):.3f}  '
          f'ratio={sigma_med/SIGMA_T20_S8:.3f}')

    # --- chi2 comparison ---
    sqt_chi2_dof  = [r['sqt']['chi2']/r['sqt']['dof']
                     for r in ok_results if r['sqt'].get('dof', 0) > 0]
    mond_ok = [r for r in results if r.get('ok') and r.get('mond') and r['mond'].get('success')]
    mond_chi2_dof = [r['mond']['chi2']/r['mond']['dof']
                     for r in mond_ok if r['mond'].get('dof', 0) > 0]
    nfw_ok = [r for r in results if r.get('ok') and r.get('nfw') and r['nfw'].get('success')]
    nfw_chi2_dof  = [r['nfw']['chi2']/r['nfw']['dof']
                     for r in nfw_ok if r['nfw'].get('dof', 0) > 0]

    print(f'\n  Chi2/dof comparison:')
    print(f'  SQT  (free a_0)  : median chi2/dof = {np.nanmedian(sqt_chi2_dof):.2f}  '
          f'N={len(sqt_chi2_dof)}')
    print(f'  MOND (fixed a_0) : median chi2/dof = {np.nanmedian(mond_chi2_dof):.2f}  '
          f'N={len(mond_chi2_dof)}')
    print(f'  NFW              : median chi2/dof = {np.nanmedian(nfw_chi2_dof):.2f}  '
          f'N={len(nfw_chi2_dof)}')

    sys.stdout.flush()
    return {
        'ok_results':    ok_results,
        'log_a0_arr':    log_a0_arr,
        'a0_si_arr':     a0_si_arr,
        'beta_arr':      beta_arr,
        'sigma_arr':     sigma_arr,
        'upsilon_arr':   upsilon_arr,
        'log_a0_mean':   log_a0_mean,
        'log_a0_std':    log_a0_std,
        'a0_mean_SI':    a0_mean_SI,
        'beta_med':      beta_med,
        'sigma_med':     sigma_med,
        'log_sigma_med': log_sigma_med,
        'sqt_chi2_dof':  sqt_chi2_dof,
        'mond_chi2_dof': mond_chi2_dof,
        'nfw_chi2_dof':  nfw_chi2_dof,
        'mond_ok':       mond_ok,
        'nfw_ok':        nfw_ok,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Task 4: Visualization
# ──────────────────────────────────────────────────────────────────────────────

BLUE = '#1f4e79'
GREEN = '#2e7d32'
GRAY = '#7f7f7f'
RED  = '#c00000'


def task4_visualize(results, ana):
    print('\n' + '='*60)
    print('Task 4: Visualization (5-panel)')
    print('='*60)

    ok  = ana['ok_results']
    log_a0_arr = ana['log_a0_arr']

    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    fig.suptitle('L49: SQT T22_full — SPARC 175-Galaxy Rotation Curve Analysis\n'
                 f'N_fit={len(ok)}  median log(a_0)={ana["log_a0_mean"]:.3f}  '
                 f'sigma={ana["log_a0_std"]:.3f} dex',
                 fontsize=12, fontweight='bold')

    # ── Panel (a): RAR ──
    ax = axes[0, 0]
    ax.set_title('(a) Radial Acceleration Relation (RAR)', fontsize=10)
    log_aN_all, log_aobs_all = [], []
    for r in ok[:80]:     # plot up to 80 galaxies for clarity
        rad  = np.array(r['r'])
        vobs = np.array(r['vobs'])
        vgas = np.array(r['Vgas'])
        vdsk = np.array(r['Vdisk'])
        vbul = np.array(r['Vbul'])
        Up   = r['sqt']['Upsilon']
        aobs = vobs**2 / np.maximum(rad, 1e-8)
        aN   = (vgas**2 + Up*vdsk**2 + Up*vbul**2) / np.maximum(rad, 1e-8)
        mask = (aN > 0) & (aobs > 0)
        if mask.sum() > 0:
            log_aN_all.extend(np.log10(aN[mask]).tolist())
            log_aobs_all.extend(np.log10(aobs[mask]).tolist())
    if log_aN_all:
        ax.scatter(log_aN_all, log_aobs_all, c='#bbbbbb', s=2, alpha=0.3,
                   label='SPARC data')
    # Theory curves
    aN_grid = np.logspace(-5, 2, 200)
    a0_med  = ana['a0_mean_SI'] / KPC_CONV  # in (km/s)^2/kpc
    atot_sqt  = 0.5*(aN_grid + np.sqrt(aN_grid**2 + 4*aN_grid*a0_med))
    atot_mond = 0.5*(aN_grid + np.sqrt(aN_grid**2 + 4*aN_grid*A0_KPC))
    ax.plot(np.log10(aN_grid), np.log10(atot_sqt),  color=BLUE,  lw=2.5,
            label=f'SQT (a_0 median)')
    ax.plot(np.log10(aN_grid), np.log10(atot_mond), color=GREEN, lw=2, ls='--',
            label=f'MOND std a_0')
    ax.plot([-5, 2], [-5, 2], color=GRAY, lw=1, ls=':', label='Newton (a=a_N)')
    ax.axvline(np.log10(A0_KPC), color='orange', lw=1, ls='--', alpha=0.6,
               label=f'a_0 MOND std')
    ax.set_xlabel('log10(a_N) [(km/s)^2/kpc]')
    ax.set_ylabel('log10(a_obs) [(km/s)^2/kpc]')
    ax.legend(fontsize=7)
    ax.set_xlim(-5, 3); ax.set_ylim(-5, 3)
    ax.grid(alpha=0.3)

    # ── Panel (b): a_0 distribution ──
    ax = axes[0, 1]
    ax.set_title('(b) Galaxy a_0 Distribution (A1 universality test)', fontsize=10)
    valid_la0 = log_a0_arr[np.isfinite(log_a0_arr)]
    if len(valid_la0) > 0:
        bins = np.linspace(valid_la0.min()-0.5, valid_la0.max()+0.5, 30)
        ax.hist(valid_la0, bins=bins, color=BLUE, alpha=0.7, label='SQT free a_0')
        # Gaussian fit
        mu, sg = sp_norm.fit(valid_la0)
        x_fit  = np.linspace(bins[0], bins[-1], 200)
        ax.plot(x_fit, sp_norm.pdf(x_fit, mu, sg) * len(valid_la0) * (bins[1]-bins[0]),
                color=RED, lw=2, label=f'Gaussian mu={mu:.2f} sig={sg:.2f}')
    ax.axvline(np.log10(A0_KPC), color=GREEN, lw=2, ls='--',
               label=f'MOND std ({np.log10(A0_KPC):.2f})')
    ax.axvline(ana['log_a0_mean'], color=BLUE, lw=2, ls='-',
               label=f'median ({ana["log_a0_mean"]:.2f})')
    # A1 condition: sigma < 0.15 dex
    sig_color = 'green' if ana['log_a0_std'] < 0.15 else ('orange' if ana['log_a0_std'] < 0.25 else 'red')
    ax.set_xlabel('log10(a_0) [(km/s)^2/kpc]')
    ax.set_ylabel('Count')
    ax.set_title(f'(b) a_0 distribution  sigma={ana["log_a0_std"]:.3f} dex', fontsize=10)
    ax.legend(fontsize=7)
    ax.grid(alpha=0.3)

    # ── Panel (c): chi2/dof CDF ──
    ax = axes[0, 2]
    ax.set_title('(c) chi2/dof CDF: SQT vs MOND vs NFW', fontsize=10)
    for arr, label, col, ls in [
        (ana['sqt_chi2_dof'],  'SQT (free a_0)', BLUE,  '-'),
        (ana['mond_chi2_dof'], 'MOND (fixed a_0)', GREEN, '--'),
        (ana['nfw_chi2_dof'],  'NFW+baryon',       GRAY,  ':'),
    ]:
        if len(arr) > 0:
            arr_s = np.sort(np.clip(arr, 0, 200))
            cdf   = np.arange(1, len(arr_s)+1) / len(arr_s)
            ax.plot(arr_s, cdf, color=col, lw=2, ls=ls,
                    label=f'{label} med={np.nanmedian(arr):.1f}')
    ax.axvline(1.0, color='orange', lw=1, ls='--', alpha=0.7, label='chi2/dof=1')
    ax.set_xlim(0, 30); ax.set_ylim(0, 1.02)
    ax.set_xlabel('chi2 / dof')
    ax.set_ylabel('CDF')
    ax.legend(fontsize=7)
    ax.grid(alpha=0.3)

    # ── Panel (d): sigma_0 consistency ──
    ax = axes[1, 0]
    ax.set_title('(d) sigma_0 Consistency Diagram (T17/T20/T22)', fontsize=10)
    refs = {
        'T17 H0\ntension':  (np.log10(SIGMA_T17_TENSION), RED),
        'T17 self-\nconsist': (np.log10(SIGMA_T17_SC),      BLUE),
        'T20 sigma8':       (np.log10(SIGMA_T20_S8),       GREEN),
        'T22 a_0\n(L49)':  (ana['log_sigma_med'],          '#8B4513'),
    }
    ys = [0.8, 0.6, 0.4, 0.2]
    for (label, (log_s, col)), y in zip(refs.items(), ys):
        ax.axvline(log_s, color=col, lw=2.5, alpha=0.8, label=f'{label.replace(chr(10)," ")}: {log_s:.3f}')
        ax.text(log_s, y, f'  {10**log_s:.2e}', color=col, fontsize=8, va='center')
    # sigma_0 distribution from T22
    sig_valid = ana['sigma_arr'][np.isfinite(ana['sigma_arr']) & (ana['sigma_arr'] > 0)]
    if len(sig_valid) > 0:
        log_sig = np.log10(sig_valid)
        bins_s  = np.linspace(log_sig.min()-0.3, log_sig.max()+0.3, 25)
        h, b = np.histogram(log_sig, bins=bins_s)
        h    = h / h.max()   # normalize for display
        ax.bar(b[:-1], h*0.3, width=np.diff(b), color='#8B4513', alpha=0.3, align='edge')
    ax.set_xlim(7, 9.5)
    ax.set_ylim(0, 1)
    ax.set_xlabel('log10(sigma_0) [m^3/(kg*s)]')
    ax.set_ylabel('(normalized)')
    ax.legend(fontsize=7, loc='upper left')
    ax.grid(alpha=0.3)

    # ── Panel (e): Surface brightness vs a_0 (environment) ──
    ax = axes[1, 1]
    ax.set_title('(e) Environment: SBdisk vs log(a_0)', fontsize=10)
    sb_vals, la0_vals = [], []
    for r in ok:
        sb = r.get('sb_mean', np.nan)
        la0 = r['sqt'].get('log_a0', np.nan)
        if np.isfinite(sb) and sb > 0 and np.isfinite(la0):
            sb_vals.append(np.log10(sb))
            la0_vals.append(la0)
    if len(sb_vals) > 5:
        ax.scatter(sb_vals, la0_vals, c=BLUE, s=15, alpha=0.6, label='galaxies')
        # Linear fit
        p = np.polyfit(sb_vals, la0_vals, 1)
        x_fit = np.linspace(min(sb_vals), max(sb_vals), 100)
        ax.plot(x_fit, np.polyval(p, x_fit), color=RED, lw=2,
                label=f'h_1 slope={p[0]:.3f}')
        ax.text(0.05, 0.95, f'slope (h_1 proxy) = {p[0]:.4f}', transform=ax.transAxes,
                fontsize=9, va='top',
                color='green' if abs(p[0]) < 0.05 else 'red')
    ax.axhline(np.log10(A0_KPC), color=GREEN, lw=1.5, ls='--',
               label=f'MOND std ({np.log10(A0_KPC):.2f})')
    ax.set_xlabel('log10(SBdisk) [L_sun/pc^2]')
    ax.set_ylabel('log10(a_0) [(km/s)^2/kpc]')
    ax.legend(fontsize=7)
    ax.grid(alpha=0.3)

    # ── Panel (f): Sample rotation curves (best 3) ──
    ax = axes[1, 2]
    ax.set_title('(f) Sample rotation curves (best chi2/dof)', fontsize=10)
    sorted_ok = sorted(ok, key=lambda r: r['sqt']['chi2']/max(r['sqt']['dof'],1))
    colors_s  = [BLUE, '#2471a3', '#5dade2']
    for i, (r, col) in enumerate(zip(sorted_ok[:3], colors_s)):
        rad  = np.array(r['r'])
        vobs = np.array(r['vobs'])
        errV = np.array(r['errV'])
        vm   = np.array(r['sqt']['v_mod'])
        chi2dof = r['sqt']['chi2'] / max(r['sqt']['dof'], 1)
        ax.errorbar(rad, vobs, yerr=errV, fmt='o', color=col, ms=4, alpha=0.7,
                    label=f'{r["name"]} obs')
        ax.plot(rad, vm, color=col, lw=2,
                label=f'{r["name"]} SQT chi2/dof={chi2dof:.1f}')
    ax.set_xlabel('r [kpc]')
    ax.set_ylabel('V [km/s]')
    ax.legend(fontsize=6, loc='lower right')
    ax.grid(alpha=0.3)

    plt.tight_layout()
    out_main = _SCRIPT_DIR / 'l49_main.png'
    fig.savefig(out_main, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Main plot: {out_main}')
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 5: Verdict
# ──────────────────────────────────────────────────────────────────────────────

def task5_verdict(ana):
    print('\n' + '='*60)
    print('L49 FINAL VERDICT')
    print('='*60)

    std  = ana['log_a0_std']
    lsig = ana['log_sigma_med']
    sig  = ana['sigma_med']

    # A1 universality
    if std < 0.15:
        a1_verdict = 'A1-PASS: sigma(log a_0) < 0.15 dex — universal a_0'
    elif std < 0.25:
        a1_verdict = 'A1-WARN: sigma(log a_0) in [0.15, 0.25] dex'
    else:
        a1_verdict = 'A1-FAIL: sigma(log a_0) > 0.25 dex — environment-dependent'

    # sigma_0 consistency with T17/T20
    log_refs = {
        'T17_tension': np.log10(SIGMA_T17_TENSION),
        'T17_sc':      np.log10(SIGMA_T17_SC),
        'T20_s8':      np.log10(SIGMA_T20_S8),
    }
    closest = min(log_refs, key=lambda k: abs(log_refs[k] - lsig))
    closest_diff = abs(log_refs[closest] - lsig)

    if closest_diff < 0.15:
        sig_verdict = f'MATCH — T22 sigma_0 consistent with {closest} (delta={closest_diff:.3f} dex)'
    elif closest_diff < 0.3:
        sig_verdict = f'NEAR — T22 sigma_0 near {closest} (delta={closest_diff:.3f} dex)'
    else:
        all_diffs = {k: abs(log_refs[k]-lsig) for k in log_refs}
        sig_verdict = (f'4th-VALUE — T22 sigma_0={sig:.2e} differs from ALL T17/T20 values '
                       f'(min diff={min(all_diffs.values()):.2f} dex)')

    print(f'\n  a_0 universality: {a1_verdict}')
    print(f'  sigma_0 matching: {sig_verdict}')
    print(f'\n  T22 sigma_0 = {sig:.3e} m^3/(kg*s)  log = {lsig:.3f}')
    print(f'\n  Chi2/dof: SQT={np.nanmedian(ana["sqt_chi2_dof"]):.2f} '
          f'| MOND={np.nanmedian(ana["mond_chi2_dof"]):.2f} '
          f'| NFW={np.nanmedian(ana["nfw_chi2_dof"]):.2f}')

    # Diagnostic table
    print(f'\n  === sigma_0 Diagnostic Table ===')
    print(f'  {"Constraint":<20} {"sigma_0":>12}  {"log sigma_0":>12}')
    print(f'  {"-"*46}')
    print(f'  {"T17 H0 tension":<20} {SIGMA_T17_TENSION:>12.3e}  {np.log10(SIGMA_T17_TENSION):>12.3f}')
    print(f'  {"T17 self-consist":<20} {SIGMA_T17_SC:>12.3e}  {np.log10(SIGMA_T17_SC):>12.3f}')
    print(f'  {"T20 sigma8":<20} {SIGMA_T20_S8:>12.3e}  {np.log10(SIGMA_T20_S8):>12.3f}')
    print(f'  {"T22 a_0 (L49)":<20} {sig:>12.3e}  {lsig:>12.3f}  <-- THIS RUN')

    sys.stdout.flush()
    return {
        'a1_verdict':   a1_verdict,
        'sig_verdict':  sig_verdict,
        'log_a0_std':   std,
        'log_sigma_med': lsig,
        'sigma_med':    sig,
        'closest':      closest,
        'closest_diff': closest_diff,
    }


# ──────────────────────────────────────────────────────────────────────────────
# JSON serialization
# ──────────────────────────────────────────────────────────────────────────────

def _jsonify(obj):
    if isinstance(obj, dict):       return {k: _jsonify(v) for k, v in obj.items()}
    if isinstance(obj, list):       return [_jsonify(v) for v in obj]
    if isinstance(obj, np.ndarray): return _jsonify(obj.tolist())
    if isinstance(obj, bool):       return bool(obj)
    if isinstance(obj, np.integer): return int(obj)
    if isinstance(obj, (np.floating, float)):
        f = float(obj)
        return None if not np.isfinite(f) else f
    if isinstance(obj, Path):       return str(obj)
    return obj


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('='*60)
    print('L49: T22_full — SPARC 175-Galaxy Rotation Curve Analysis')
    print(f'Workers: {N_WORKERS}  |  a_0_MOND = {A0_SI:.2e} m/s^2 = {A0_KPC:.1f} (km/s)^2/kpc')
    print('='*60)
    sys.stdout.flush()

    pt = pretask_units()

    ctx  = mp.get_context('spawn')
    pool = ctx.Pool(N_WORKERS)

    file_list = []
    results   = []
    ana       = {}
    verdict   = {}

    try:
        file_list = task1_load()
        results   = task2_fit(file_list, pool)
        ana       = task3_analyze(results)
        task4_visualize(results, ana)
        verdict   = task5_verdict(ana)

    finally:
        pool.close()
        pool.join()

    # Summary
    print('\n' + '='*60)
    print('L49 RESULTS SUMMARY')
    print('='*60)
    print(f'[T1] Galaxies loaded: {len(file_list)}')
    ok_n = sum(1 for r in results if r.get('ok') and r.get('sqt') and r['sqt'].get('success'))
    print(f'[T2] SQT fits OK: {ok_n}/{len(results)}')
    print(f'[T3] log(a_0) median={ana.get("log_a0_mean","?"):.3f}  '
          f'std={ana.get("log_a0_std","?"):.3f} dex')
    print(f'[T3] sigma_0 median = {ana.get("sigma_med",0):.3e}')
    print(f'[Verdict-A1] {verdict.get("a1_verdict","?")}')
    print(f'[Verdict-SC] {verdict.get("sig_verdict","?")}')

    # Save JSON
    save = {
        'n_galaxies':    len(file_list),
        'n_sqt_ok':      ok_n,
        'log_a0_median': ana.get('log_a0_mean'),
        'log_a0_std':    ana.get('log_a0_std'),
        'a0_median_SI':  ana.get('a0_mean_SI'),
        'beta_median':   ana.get('beta_med'),
        'sigma_median':  ana.get('sigma_med'),
        'log_sigma_med': ana.get('log_sigma_med'),
        'chi2_sqt_med':  float(np.nanmedian(ana['sqt_chi2_dof']))  if ana.get('sqt_chi2_dof')  else None,
        'chi2_mond_med': float(np.nanmedian(ana['mond_chi2_dof'])) if ana.get('mond_chi2_dof') else None,
        'chi2_nfw_med':  float(np.nanmedian(ana['nfw_chi2_dof']))  if ana.get('nfw_chi2_dof')  else None,
        'verdict_a1':    verdict.get('a1_verdict'),
        'verdict_sc':    verdict.get('sig_verdict'),
        'closest_ref':   verdict.get('closest'),
        'closest_diff':  verdict.get('closest_diff'),
        'refs': {
            'T17_tension': SIGMA_T17_TENSION,
            'T17_sc':      SIGMA_T17_SC,
            'T20_s8':      SIGMA_T20_S8,
        },
    }
    out_json = _SCRIPT_DIR / 'l49_results.json'
    with open(out_json, 'w') as f:
        json.dump(_jsonify(save), f, indent=2)
    print(f'Saved: {out_json}')
