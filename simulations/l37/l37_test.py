# -*- coding: utf-8 -*-
"""
l37_test.py -- L37: SQT 범위 확정 + 부분 주장 검증
====================================================
Task 1: Model D robustness  (amp,beta grid scan -> heatmap)
Task 2: fsigma8 comparison  (LCDM vs Model D)
Task 3: DESI-only CPL       (BAO-only wa sign reversal)
Task 4: H0 by dataset       (dataset-by-dataset H0 preference)

Parallelism: 8-worker spawn Pool (Task 1 grid, Task 3 starts, Task 4 datasets)
Fixes applied vs L36: verdict h0_ok AND condition, seed before padding, safe JSON.
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
    OR, C_KMS, N_TOTAL, SIGMA_8_0,
    cpl_wa, _growth_fs8,
    Z_RSD, FS8_OBS, FS8_SIG,
    _base as _base35,
)

LCDM_AICC = 1670.1227
D_BEST    = {'Om': 0.3220, 'H0': 66.98, 'amp': 0.8178, 'beta': 3.533}
LCDM_BEST = {'Om': 0.3094, 'H0': 68.41}
N_WORKERS = 8


# ─── Model D E(z) ─────────────────────────────────────────────────────────────
def _E_D(z_arr, Om, amp, beta):
    OL0, ratio, _ = _base35(z_arr, Om)
    if OL0 is None: return None
    rde = OL0 * (1.0 + amp * (ratio - 1.0) * np.exp(-abs(beta) * z_arr))
    E2  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
    return None if np.any(E2 <= 0) else np.sqrt(E2)

def _make_E_D(Om, amp, beta):
    def E_fn(z, _Om): return _E_D(z, Om, amp, beta)
    return E_fn


# ─── AICc ─────────────────────────────────────────────────────────────────────
def _aicc(chi2_val, k):
    return chi2_val + 2*k + 2*k*(k+1)/(N_TOTAL - k - 1)


# ─── Verdict (fixed: h0_ok AND condition) ────────────────────────────────────
def _verdict(daicc, wa, H0_tension, boundary=False):
    if boundary:   return 'K92 INVALID'
    if daicc >= 0: return 'K90 KILL'
    if daicc >= -2: return 'Q90 PASS'
    wa_ok = (wa is not None and wa < 0)
    h0_ok = (H0_tension is not None and H0_tension < 4.01)
    if daicc < -4 and wa_ok and h0_ok: return 'Q92 GAME'
    return 'Q91 STRONG'


# ─── H0 tension ───────────────────────────────────────────────────────────────
def _H0_tension(H0_fit, H0_err=0.5):
    return (73.04 - H0_fit) / np.sqrt(1.04**2 + H0_err**2)


# ─── JSON serializer (safe) ───────────────────────────────────────────────────
def _jsonify(obj):
    if isinstance(obj, dict):      return {k: _jsonify(v) for k, v in obj.items()}
    if isinstance(obj, list):      return [_jsonify(v) for v in obj]
    if isinstance(obj, np.ndarray): return _jsonify(obj.tolist())
    if isinstance(obj, bool):      return bool(obj)
    if isinstance(obj, np.integer): return int(obj)
    if isinstance(obj, (np.floating, float)):
        f = float(obj)
        return None if not np.isfinite(f) else f
    return obj


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Worker functions (module-level for spawn pickling)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _t1_worker(args):
    """Task 1: compute chi2_all for (amp, beta) grid point."""
    amp, beta, Om, H0 = args
    warnings.filterwarnings('ignore')
    np.seterr(all='ignore')
    try:
        E_fn = _make_E_D(Om, amp, beta)
        cb = chi2_bao(E_fn, Om, H0)
        cc = chi2_cmb(E_fn, Om, H0)
        cs = chi2_sn(E_fn,  Om, H0)
        cr = chi2_rsd(E_fn, Om, H0)
        if all(v < 1e7 for v in [cb, cc, cs, cr]):
            ctot = cb + cc + cs + cr
            return float(_aicc(ctot, k=4) - LCDM_AICC)
    except Exception:
        pass
    return float('nan')


def _t3_worker(start):
    """Task 3: BAO-only optimization from a single start."""
    warnings.filterwarnings('ignore')
    np.seterr(all='ignore')
    bounds = [(0.15, 0.50), (55., 82.), (-3.0, 3.0), (0.01, 5.0)]

    def obj(p):
        Om, H0, amp, beta = p
        if any(x < b[0] or x > b[1] for x, b in zip(p, bounds)): return 1e9
        E_fn = _make_E_D(Om, amp, beta)
        if E_fn is None: return 1e9
        v = chi2_bao(E_fn, Om, H0)
        return v if (np.isfinite(v) and v < 1e7) else 1e9

    try:
        r = minimize(obj, start, method='Nelder-Mead',
                     options={'xatol': 1e-5, 'fatol': 1e-5, 'maxiter': 1200})
        return (float(r.fun), [float(x) for x in r.x])
    except Exception:
        return (1e9, None)


def _t4_worker(args):
    """Task 4: fit Model D to a single dataset, return H0 and uncertainty."""
    dataset_name, starts_list = args
    warnings.filterwarnings('ignore')
    np.seterr(all='ignore')

    chi2_fn_map = {
        'BAO': chi2_bao,
        'CMB': chi2_cmb,
        'SN':  chi2_sn,
        'RSD': chi2_rsd,
    }
    chi2_fn = chi2_fn_map[dataset_name]
    bounds  = [(0.15, 0.50), (55., 82.), (-3.0, 3.0), (0.01, 5.0)]

    def obj(p):
        Om, H0, amp, beta = p
        if any(x < b[0] or x > b[1] for x, b in zip(p, bounds)): return 1e9
        E_fn = _make_E_D(Om, amp, beta)
        if E_fn is None: return 1e9
        v = chi2_fn(E_fn, Om, H0)
        return v if (np.isfinite(v) and v < 1e7) else 1e9

    np.random.seed(42)  # seed before optimization loop
    best_val, best_par = 1e9, None
    for s in starts_list:
        try:
            r = minimize(obj, s, method='Nelder-Mead',
                         options={'xatol': 1e-5, 'fatol': 1e-5, 'maxiter': 1000})
            if r.fun < best_val:
                best_val, best_par = r.fun, r.x
        except Exception:
            pass

    if best_par is None:
        return {'dataset': dataset_name, 'failed': True}

    try:
        r2 = minimize(obj, best_par, method='Nelder-Mead',
                      options={'xatol': 1e-6, 'fatol': 1e-6, 'maxiter': 2000})
        if r2.fun < best_val:
            best_val, best_par = r2.fun, r2.x
    except Exception:
        pass

    # H0 uncertainty from 1D Hessian along H0 axis
    H0_err = 0.5  # fallback
    try:
        p0 = best_par.copy()
        dH = 0.2
        pp = p0.copy(); pp[1] += dH
        pm = p0.copy(); pm[1] -= dH
        f0, fp, fm = obj(p0), obj(pp), obj(pm)
        d2f = (fp - 2*f0 + fm) / dH**2
        if d2f > 1e-6:
            H0_err = max(0.1, min(5.0, 1.0 / np.sqrt(d2f)))
    except Exception:
        pass

    Om, H0, amp, beta = best_par
    h0t = _H0_tension(H0, H0_err)
    try:
        w0, wa = cpl_wa(_make_E_D(Om, amp, beta), Om)
    except Exception:
        w0, wa = None, None

    return {
        'dataset': dataset_name,
        'Om': float(Om), 'H0': float(H0),
        'amp': float(amp), 'beta': float(beta),
        'chi2': float(best_val),
        'H0_err': float(H0_err),
        'H0_tension': float(h0t),
        'w0': float(w0) if w0 is not None else None,
        'wa':  float(wa) if wa  is not None else None,
        'failed': False,
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Task functions (called in main process)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def task1_robustness(pool):
    print("\n" + "="*60)
    print("Task 1: Model D Robustness (amp,beta grid scan)")
    print("="*60)

    n_grid    = 20
    amp_best  = D_BEST['amp'];  beta_best = D_BEST['beta']
    Om, H0    = D_BEST['Om'],   D_BEST['H0']
    amp_range  = np.linspace(amp_best  * 0.7, amp_best  * 1.3, n_grid)
    beta_range = np.linspace(beta_best * 0.7, beta_best * 1.3, n_grid)

    args = [(a, b, Om, H0) for a in amp_range for b in beta_range]
    t0   = time.time()
    flat = pool.map(_t1_worker, args)
    print(f"  Grid scan done in {time.time()-t0:.1f}s")

    daicc_grid = np.array(flat).reshape(n_grid, n_grid)
    valid = np.isfinite(daicc_grid)
    n_valid = valid.sum()
    frac6 = float(np.sum(daicc_grid[valid] < -6) / n_valid) if n_valid else 0.0
    frac2 = float(np.sum(daicc_grid[valid] < -2) / n_valid) if n_valid else 0.0
    best_daicc = float(np.nanmin(daicc_grid))
    bi, bj = np.unravel_index(np.nanargmin(daicc_grid), daicc_grid.shape)

    print(f"  Best: amp={amp_range[bi]:.4f}, beta={beta_range[bj]:.4f}, dAICc={best_daicc:.2f}")
    print(f"  dAICc<-6 fraction: {frac6*100:.1f}%")
    print(f"  dAICc<-2 fraction: {frac2*100:.1f}%")
    verdict_t1 = 'PASS' if frac6 > 0.30 else ('CONDITIONAL' if frac6 > 0.05 else 'FAIL')
    print(f"  Robustness verdict: {verdict_t1}")

    # Heatmap
    fig, ax = plt.subplots(figsize=(7, 5))
    im = ax.imshow(daicc_grid, origin='lower', aspect='auto',
                   extent=[beta_range[0], beta_range[-1], amp_range[0], amp_range[-1]],
                   cmap='RdYlGn_r', vmin=-12, vmax=2)
    plt.colorbar(im, ax=ax, label='dAICc')
    try:
        cs = ax.contour(beta_range, amp_range, daicc_grid,
                        levels=[-8, -6, -4, -2, 0], colors='k', linewidths=0.8)
        ax.clabel(cs, fmt='%d')
    except Exception:
        pass
    ax.axhline(amp_best,  color='cyan', ls='--', lw=1.5, label=f'L36 amp={amp_best:.3f}')
    ax.axvline(beta_best, color='cyan', ls='--', lw=1.5, label=f'L36 beta={beta_best:.3f}')
    ax.set_xlabel('beta')
    ax.set_ylabel('amp')
    ax.set_title(f'Model D dAICc scan (Om={Om:.4f}, H0={H0:.2f})')
    ax.legend(fontsize=8)
    fig.tight_layout()
    plot_path = os.path.join(_SCRIPT_DIR, 'l37_task1_heatmap.png')
    fig.savefig(plot_path, dpi=130)
    plt.close(fig)
    print(f"  Plot: {plot_path}")

    return {
        'frac_below_minus6': frac6,
        'frac_below_minus2': frac2,
        'best_amp':   float(amp_range[bi]),
        'best_beta':  float(beta_range[bj]),
        'best_daicc': best_daicc,
        'verdict':    verdict_t1,
        'amp_range':  amp_range.tolist(),
        'beta_range': beta_range.tolist(),
        'daicc_grid': daicc_grid.tolist(),
    }


def task2_fsigma8():
    print("\n" + "="*60)
    print("Task 2: fsigma8 Comparison (LCDM vs Model D)")
    print("="*60)

    E_lcdm_fn = lambda z, _Om: E_lcdm(z, LCDM_BEST['Om'])
    E_D_fn    = _make_E_D(D_BEST['Om'], D_BEST['amp'], D_BEST['beta'])

    fs8_lcdm = _growth_fs8(E_lcdm_fn, LCDM_BEST['Om'], Z_RSD)
    fs8_D    = _growth_fs8(E_D_fn,    D_BEST['Om'],    Z_RSD)

    if fs8_lcdm is None or fs8_D is None:
        print("  FAILED: growth ODE")
        return None

    chi2_l = float(np.sum(((fs8_lcdm - FS8_OBS)/FS8_SIG)**2))
    chi2_d = float(np.sum(((fs8_D    - FS8_OBS)/FS8_SIG)**2))
    delta  = chi2_d - chi2_l
    verdict_t2 = 'WIN' if delta < -2 else ('LOSE' if delta > 2 else 'TIE')

    print(f"  chi2_fsig8 LCDM   : {chi2_l:.4f}")
    print(f"  chi2_fsig8 Model D: {chi2_d:.4f}  (delta={delta:+.4f})")
    print(f"  Verdict: {verdict_t2}")
    print(f"  {'z':>6} {'obs':>8} {'sig':>7} {'LCDM':>8} {'D':>8} {'D-L':>8}")
    for i, z in enumerate(Z_RSD):
        print(f"  {z:>6.3f} {FS8_OBS[i]:>8.3f} {FS8_SIG[i]:>7.3f} "
              f"{fs8_lcdm[i]:>8.3f} {fs8_D[i]:>8.3f} {fs8_D[i]-fs8_lcdm[i]:>+8.3f}")

    # Smooth curves for plot
    z_smooth = np.linspace(0.01, 1.6, 120)
    fs8_lcdm_s = _growth_fs8(E_lcdm_fn, LCDM_BEST['Om'], z_smooth)
    fs8_D_s    = _growth_fs8(E_D_fn,    D_BEST['Om'],    z_smooth)

    fig, ax = plt.subplots(figsize=(7, 5))
    if fs8_lcdm_s is not None:
        ax.plot(z_smooth, fs8_lcdm_s, 'b-', lw=2, label=f'LCDM (chi2={chi2_l:.2f})')
    if fs8_D_s is not None:
        ax.plot(z_smooth, fs8_D_s,    'r-', lw=2, label=f'Model D (chi2={chi2_d:.2f})')
    ax.errorbar(Z_RSD, FS8_OBS, yerr=FS8_SIG, fmt='ko', capsize=4, ms=5, label='RSD data')
    ax.set_xlabel('z');  ax.set_ylabel('f*sigma8(z)')
    ax.set_title('fsigma8: LCDM vs Model D')
    ax.legend(); fig.tight_layout()
    plot_path = os.path.join(_SCRIPT_DIR, 'l37_task2_fsig8.png')
    fig.savefig(plot_path, dpi=130); plt.close(fig)
    print(f"  Plot: {plot_path}")

    return {
        'chi2_fsig8_lcdm': chi2_l,
        'chi2_fsig8_D':    chi2_d,
        'delta_chi2':      delta,
        'verdict':         verdict_t2,
        'z_rsd':   Z_RSD.tolist(),
        'fs8_obs': FS8_OBS.tolist(),
        'fs8_sig': FS8_SIG.tolist(),
        'fs8_lcdm': fs8_lcdm.tolist(),
        'fs8_D':    fs8_D.tolist(),
    }


def task3_desi_only(pool):
    print("\n" + "="*60)
    print("Task 3: DESI BAO-only CPL Reanalysis")
    print("="*60)

    np.random.seed(42)
    starts = []
    for Om0 in np.linspace(0.26, 0.36, 4):
        for H0_0 in [64., 67., 70., 73.]:
            for amp0 in [0.4, 0.8, 1.2]:
                for beta0 in [2.0, 3.5, 5.0]:
                    starts.append([Om0, H0_0, amp0, beta0])
    starts.append([D_BEST['Om'], D_BEST['H0'], D_BEST['amp'], D_BEST['beta']])

    t0      = time.time()
    results = pool.map(_t3_worker, starts)
    print(f"  BAO-only optimization done in {time.time()-t0:.1f}s ({len(starts)} starts)")

    best_val = 1e9; best_par = None
    for val, par in results:
        if par is not None and val < best_val:
            best_val, best_par = val, par

    if best_par is None:
        print("  FAILED")
        return None

    # Refine in main process
    def obj_bao(p):
        Om, H0, amp, beta = p
        bounds = [(0.15,0.50),(55.,82.),(-3.,3.),(0.01,5.)]
        if any(x < b[0] or x > b[1] for x, b in zip(p, bounds)): return 1e9
        E_fn = _make_E_D(Om, amp, beta)
        if E_fn is None: return 1e9
        v = chi2_bao(E_fn, Om, H0)
        return v if (np.isfinite(v) and v < 1e7) else 1e9

    try:
        r = minimize(obj_bao, best_par, method='Nelder-Mead',
                     options={'xatol':1e-6, 'fatol':1e-6, 'maxiter':2000})
        if r.fun < best_val:
            best_val, best_par = r.fun, r.x
    except Exception:
        pass

    Om, H0, amp, beta = best_par
    E_fn_best = _make_E_D(Om, amp, beta)
    w0_bao, wa_bao = cpl_wa(E_fn_best, Om)
    reversal = (wa_bao is not None and wa_bao < 0)

    print(f"  BAO-only: Om={Om:.4f}, H0={H0:.2f}, amp={amp:.4f}, beta={beta:.4f}")
    print(f"  chi2_BAO={best_val:.4f}")
    print(f"  BAO-only CPL: w0={w0_bao:.4f}, wa={wa_bao:.4f}")
    print(f"  Combined CPL (L36): w0=-1.137, wa=+0.367")
    print(f"  wa sign reversal (BAO<0, combined>0): {reversal}")
    verdict_t3 = 'CONFIRMED' if reversal else 'ANOMALY'
    print(f"  Verdict: {verdict_t3}")

    # rho_DE plot: actual vs CPL approximation
    z_arr   = np.linspace(0.001, 2.5, 300)
    E_comb  = _make_E_D(D_BEST['Om'], D_BEST['amp'], D_BEST['beta'])
    E_bao_f = _make_E_D(Om, amp, beta)

    def rho_de_norm(E_fn, Om_v):
        Ev = E_fn(z_arr, Om_v)
        E0 = E_fn(np.array([0.0]), Om_v)
        if Ev is None or E0 is None: return None
        rde  = Ev**2 - OR*(1+z_arr)**4 - Om_v*(1+z_arr)**3
        rde0 = E0[0]**2 - OR - Om_v
        return rde / rde0 if rde0 > 0 else None

    rde_comb = rho_de_norm(E_comb, D_BEST['Om'])
    rde_bao  = rho_de_norm(E_bao_f, Om)

    w0c, wac = cpl_wa(E_comb, D_BEST['Om'])

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    ax = axes[0]
    if rde_comb is not None:
        ax.plot(z_arr, rde_comb, 'r-', lw=2, label=f'Combined (wa={wac:.3f})')
    if rde_bao is not None:
        ax.plot(z_arr, rde_bao, 'b-', lw=2, label=f'BAO-only (wa={wa_bao:.3f})')
    ax.axhline(1, color='k', ls=':', alpha=0.4, label='LCDM')
    ax.set_xlabel('z'); ax.set_ylabel('rho_DE / rho_DE(0)')
    ax.set_title('Model D rho_DE: BAO-only vs Combined')
    ax.legend(); ax.set_xlim(0, 2.5)

    ax = axes[1]
    if rde_comb is not None and w0c is not None:
        rde_cpl = (1+z_arr)**(3*(1+w0c+wac)) * np.exp(-3*wac*z_arr/(1+z_arr))
        ax.plot(z_arr, rde_comb, 'r-',  lw=2, label='Model D actual')
        ax.plot(z_arr, rde_cpl,  'b--', lw=2, label=f'CPL fit (w0={w0c:.3f}, wa={wac:.3f})')
        ax.axhline(1, color='k', ls=':', alpha=0.4)
        ax.set_xlabel('z'); ax.set_ylabel('rho_DE / rho_DE(0)')
        ax.set_title('Model D vs CPL approximation')
        ax.legend(); ax.set_xlim(0, 2.5)

    fig.tight_layout()
    plot_path = os.path.join(_SCRIPT_DIR, 'l37_task3_cpl.png')
    fig.savefig(plot_path, dpi=130); plt.close(fig)
    print(f"  Plot: {plot_path}")

    return {
        'bao_only': {
            'Om': float(Om), 'H0': float(H0), 'amp': float(amp), 'beta': float(beta),
            'chi2_bao': float(best_val),
            'w0': float(w0_bao) if w0_bao is not None else None,
            'wa': float(wa_bao) if wa_bao is not None else None,
        },
        'combined': {'w0': -1.137, 'wa': 0.367},
        'reversal_confirmed': bool(reversal),
        'verdict': verdict_t3,
    }


def task4_h0_by_dataset(pool):
    print("\n" + "="*60)
    print("Task 4: H0 Preference by Dataset")
    print("="*60)

    np.random.seed(42)
    base_start = [D_BEST['Om'], D_BEST['H0'], D_BEST['amp'], D_BEST['beta']]

    def make_starts(n=16):
        st = [base_start[:]]
        for _ in range(n - 1):
            st.append([
                np.random.uniform(0.26, 0.36),
                np.random.uniform(62.,  76.),
                np.random.uniform(0.2,  1.8),
                np.random.uniform(0.5,  5.0),
            ])
        return st

    t4_args = [
        ('BAO', make_starts(16)),
        ('CMB', make_starts(16)),
        ('SN',  make_starts(12)),
        ('RSD', make_starts(16)),
    ]

    t0      = time.time()
    results = pool.map(_t4_worker, t4_args)
    print(f"  Dataset fitting done in {time.time()-t0:.1f}s")

    res_by_name = {r['dataset']: r for r in results}

    print(f"\n  {'Dataset':<10} {'H0':>8} {'H0_err':>8} {'tension':>9} {'Om':>8}")
    print(f"  {'-'*10} {'-'*8} {'-'*8} {'-'*9} {'-'*8}")
    for ds in ['BAO', 'CMB', 'SN', 'RSD']:
        r = res_by_name.get(ds, {})
        if r and not r.get('failed'):
            print(f"  {ds:<10} {r['H0']:>8.2f} {r['H0_err']:>8.3f} "
                  f"{r['H0_tension']:>9.2f}s {r['Om']:>8.4f}")
        else:
            print(f"  {ds:<10} {'FAILED':>8}")
    print(f"  {'Combined':<10} {D_BEST['H0']:>8.2f} {'(L36)':>8} {'5.00':>9}s {D_BEST['Om']:>8.4f}")
    print(f"  {'LCDM':<10} {LCDM_BEST['H0']:>8.2f} {'---':>8} {'4.01':>9}s {LCDM_BEST['Om']:>8.4f}")
    print(f"  {'SH0ES':<10} {'73.04':>8} {'1.04':>8} {'---':>9}")

    cmb_r = res_by_name.get('CMB', {})
    cmb_driven = not cmb_r.get('failed') and cmb_r.get('H0', 70) < 69.0
    print(f"\n  CMB-driven H0 tension: {cmb_driven}")

    # Bar chart
    labels = ['BAO', 'CMB', 'SN', 'RSD', 'Combined', 'LCDM', 'SH0ES']
    h0v    = []
    for ds in ['BAO', 'CMB', 'SN', 'RSD']:
        r = res_by_name.get(ds, {})
        h0v.append(r.get('H0', float('nan')) if not r.get('failed') else float('nan'))
    h0v += [D_BEST['H0'], LCDM_BEST['H0'], 73.04]

    fig, ax = plt.subplots(figsize=(9, 5))
    colors = ['steelblue','steelblue','steelblue','steelblue','crimson','gray','orange']
    xs = np.arange(len(labels))
    bars = ax.bar(xs, h0v, color=colors, alpha=0.85)
    ax.errorbar([0,1,2,3], h0v[:4],
                yerr=[res_by_name.get(d,{}).get('H0_err', 0.5) for d in ['BAO','CMB','SN','RSD']],
                fmt='none', color='k', capsize=5)
    ax.axhline(73.04, color='orange', ls='--', lw=1.5, label='SH0ES 73.04')
    ax.axhline(LCDM_BEST['H0'], color='gray', ls='--', lw=1.5,
               label=f"LCDM {LCDM_BEST['H0']:.2f}")
    ax.set_xticks(xs); ax.set_xticklabels(labels)
    ax.set_ylabel('H0 (km/s/Mpc)'); ax.set_ylim(58, 78)
    ax.set_title('H0 preference by dataset (Model D)')
    ax.legend(fontsize=9)
    for bar, val in zip(bars, h0v):
        if np.isfinite(val):
            ax.text(bar.get_x() + bar.get_width()/2, val + 0.4, f'{val:.1f}',
                    ha='center', va='bottom', fontsize=8)
    fig.tight_layout()
    plot_path = os.path.join(_SCRIPT_DIR, 'l37_task4_h0.png')
    fig.savefig(plot_path, dpi=130); plt.close(fig)
    print(f"  Plot: {plot_path}")

    return {
        'by_dataset': {r['dataset']: r for r in results},
        'combined':   {'H0': D_BEST['H0'], 'Om': D_BEST['Om']},
        'lcdm':       {'H0': LCDM_BEST['H0'], 'Om': LCDM_BEST['Om']},
        'cmb_driven': bool(cmb_driven),
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def main():
    t_total = time.time()
    print("="*60)
    print("L37: SQT Range Verification")
    print(f"8-worker parallel | LCDM baseline AICc={LCDM_AICC}")
    print("="*60)

    print("\nWarming up SN cache...")
    get_sn()
    print("  SN ready.")

    ctx = mp.get_context('spawn')
    with ctx.Pool(N_WORKERS) as pool:
        r1 = task1_robustness(pool)
        r3 = task3_desi_only(pool)
        r4 = task4_h0_by_dataset(pool)

    r2 = task2_fsigma8()

    # ─── Final summary ────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("L37 RESULTS SUMMARY")
    print("="*60)

    print("\n[Task 1] Model D Robustness")
    if r1:
        print(f"  dAICc<-6 region: {r1['frac_below_minus6']*100:.1f}% of (amp,beta) space")
        print(f"  Best in scan: amp={r1['best_amp']:.4f}, beta={r1['best_beta']:.4f}, "
              f"dAICc={r1['best_daicc']:.2f}")
        print(f"  Verdict: {r1['verdict']}")

    print("\n[Task 2] fsigma8 Comparison")
    if r2:
        print(f"  chi2_fsig8 LCDM   : {r2['chi2_fsig8_lcdm']:.4f}")
        print(f"  chi2_fsig8 Model D: {r2['chi2_fsig8_D']:.4f}")
        print(f"  Verdict: {r2['verdict']}")

    print("\n[Task 3] DESI-only CPL")
    if r3 and r3.get('bao_only'):
        b = r3['bao_only']
        wa_bao = b.get('wa')
        print(f"  BAO-only wa: {wa_bao:.4f}" if wa_bao is not None else "  BAO-only wa: N/A")
        print(f"  Combined wa (L36): +0.367")
        print(f"  Reversal confirmed: {r3['reversal_confirmed']}")
        print(f"  Verdict: {r3['verdict']}")

    print("\n[Task 4] H0 by Dataset")
    if r4:
        bd = r4.get('by_dataset', {})
        for ds in ['BAO', 'CMB', 'SN', 'RSD']:
            r = bd.get(ds, {})
            if r and not r.get('failed'):
                print(f"  {ds}: H0={r['H0']:.2f} +- {r['H0_err']:.2f}")
        print(f"  Combined: H0={D_BEST['H0']:.2f}")
        print(f"  CMB-driven tension: {r4.get('cmb_driven')}")

    elapsed = time.time() - t_total
    print(f"\nTotal elapsed: {elapsed:.1f}s")

    # Save JSON
    out = _jsonify({'task1': r1, 'task2': r2, 'task3': r3, 'task4': r4,
                    'elapsed_s': elapsed, 'lcdm_aicc': LCDM_AICC})
    out_path = os.path.join(_SCRIPT_DIR, 'l37_results.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)
    print(f"Saved: {out_path}")


if __name__ == '__main__':
    main()
