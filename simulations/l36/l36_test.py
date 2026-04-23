# -*- coding: utf-8 -*-
"""
l36_test.py -- L36: wa<0 탐색 (L35 한계 해결)
================================================
Models: A'_fixed(k=2), A'_free(k=3), B'(k=4), C'(k=4), D(k=4)
Priority: B', D, C', A'_fixed, A'_free
"""

import os, sys, json, time, warnings
import numpy as np
from scipy.optimize import minimize, differential_evolution

warnings.filterwarnings('ignore')
np.seterr(all='ignore')
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SIM_DIR    = os.path.dirname(_SCRIPT_DIR)
_L35_DIR    = os.path.join(_SCRIPT_DIR, '../l35')

for p in [_SIM_DIR, _L35_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Import validated chi2 functions from l35_test
from l35_test import (
    chi2_bao, chi2_cmb, chi2_sn, chi2_rsd,
    get_sn,            # warm up SN cache
    E_lcdm,
    OR, C_KMS, N_TOTAL, SIGMA_8_0,
    cpl_wa,
)

LCDM_AICC = 1670.1227   # L35 baseline

def aicc(chi2_val, k):
    return chi2_val + 2*k + 2*k*(k+1)/(N_TOTAL - k - 1)

def chi2_all(E_fn, Om, H0):
    c_bao = chi2_bao(E_fn, Om, H0)
    c_cmb = chi2_cmb(E_fn, Om, H0)
    c_sn  = chi2_sn(E_fn, Om, H0)
    c_rsd = chi2_rsd(E_fn, Om, H0)
    return c_bao, c_cmb, c_sn, c_rsd, c_bao + c_cmb + c_sn + c_rsd


# ─── Base ratio helper ────────────────────────────────────────────────────────
def _base(z_arr, Om):
    OL0   = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None, None
    alpha = Om / OL0
    psi_z = 1.0 / (1.0 + alpha * (1.0 + z_arr)**3)
    psi0  = 1.0 / (1.0 + alpha)
    ratio = np.clip(psi0 / psi_z, 1.0, 200.0)
    return OL0, ratio


# ─── Model E(z) functions ────────────────────────────────────────────────────

def E_model_Ap_fixed(z_arr, Om, n=1./3.):
    """A': rho_DE = OL0 * ratio^n  (n=1/3 fixed → (1+z)^1 at high z, no blow-up)"""
    OL0, ratio = _base(z_arr, Om)
    if OL0 is None: return None
    rde = OL0 * ratio**n
    E2  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
    return None if np.any(E2 <= 0) else np.sqrt(E2)

def E_model_Ap_free(z_arr, Om, n=1./3.):
    """A'_free: n fitted."""
    return E_model_Ap_fixed(z_arr, Om, n=n)

def E_model_Bp(z_arr, Om, amp=0.5, gamma=0.0, c_fixed=1.47):
    """B': g = tanh(sqrt(pi/2)*c*(ratio-1)) + gamma*(ratio-1)^2, rho_DE=OL0*(1+amp*g)
    gamma<0 allows phantom. rho_DE<0 region returns None."""
    OL0, ratio = _base(z_arr, Om)
    if OL0 is None: return None
    rm1  = ratio - 1.0
    tanh_term = np.tanh(np.sqrt(np.pi/2) * c_fixed * np.clip(rm1, -10, 10))
    g    = tanh_term + gamma * np.clip(rm1, 0, 8.0)**2  # clip rm1^2 to avoid blow-up
    rde  = OL0 * (1.0 + amp * g)
    E2   = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
    return None if np.any(E2 <= 0) else np.sqrt(E2)

def E_model_Cp(z_arr, Om, amp=1.5, c=1.5):
    """C' (same formula as L35 C, different bounds/starts)"""
    OL0, ratio = _base(z_arr, Om)
    if OL0 is None: return None
    rm1 = ratio - 1.0
    wt  = np.tanh(z_arr)
    g   = ((1.0 - wt) * np.tanh(np.sqrt(np.pi/2) * c * np.clip(rm1, -10, 10))
           + wt * rm1)
    rde = OL0 * (1.0 + amp * g)
    E2  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
    return None if np.any(E2 <= 0) else np.sqrt(E2)

def E_model_D(z_arr, Om, amp=0.5, beta=1.0):
    """D: rho_DE = OL0*(1 + amp*(ratio-1)*exp(-beta*z))
    amp<0 -> rho_DE < OL0 at intermediate z -> phantom possible."""
    OL0, ratio = _base(z_arr, Om)
    if OL0 is None: return None
    rm1 = ratio - 1.0
    rde = OL0 * (1.0 + amp * rm1 * np.exp(-np.abs(beta) * z_arr))
    E2  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
    return None if np.any(E2 <= 0) else np.sqrt(E2)


# ─── Boundary check ──────────────────────────────────────────────────────────
def _at_boundary(params, bounds, tol=1e-3):
    """Return list of params that are within tol*(hi-lo) of a bound."""
    flagged = []
    for i, (p, (lo, hi)) in enumerate(zip(params, bounds)):
        span = hi - lo
        if span == 0: continue
        if abs(p - lo) < tol * span or abs(p - hi) < tol * span:
            flagged.append(i)
    return flagged


# ─── Optimizer ───────────────────────────────────────────────────────────────
def fit_model(name, E_fn_maker, param_names, bounds, n_starts=30, extra_starts=None):
    k = len(param_names)
    print(f"\n[{name}] Fitting joint (BAO+CMB+SN+RSD) k={k}...")

    def obj(params):
        if any(p < b[0] or p > b[1] for p, b in zip(params, bounds)):
            return 1e9
        E_fn = E_fn_maker(params)
        Om, H0 = params[0], params[1]
        if E_fn is None: return 1e9
        c_bao, c_cmb, c_sn, c_rsd, tot = chi2_all(E_fn, Om, H0)
        return tot if np.isfinite(tot) else 1e9

    # Coarse start grid
    starts = []
    for Om0 in np.linspace(0.27, 0.33, 5):
        for H0_0 in [66., 68., 70., 72.]:
            mid_extra = [(b[0]+b[1])/2 for b in bounds[2:]]
            starts.append([Om0, H0_0] + mid_extra)
    # Add extra starts from caller
    if extra_starts:
        starts += extra_starts
    # Pad to n_starts if needed
    while len(starts) < n_starts:
        Om0  = np.random.uniform(0.26, 0.35)
        H0_0 = np.random.uniform(65., 73.)
        extra = [np.random.uniform(b[0], b[1]) for b in bounds[2:]]
        starts.append([Om0, H0_0] + extra)

    np.random.seed(42)
    best_val, best_par = 1e9, None

    for s in starts[:n_starts]:
        try:
            r = minimize(obj, s, method='Nelder-Mead',
                         options={'xatol':1e-4, 'fatol':1e-4, 'maxiter':500})
            if r.fun < best_val:
                best_val, best_par = r.fun, r.x
        except Exception:
            pass

    # Refine
    if best_par is not None:
        try:
            r = minimize(obj, best_par, method='Nelder-Mead',
                         options={'xatol':1e-6, 'fatol':1e-6, 'maxiter':3000})
            if r.fun < best_val:
                best_val, best_par = r.fun, r.x
        except Exception:
            pass
        # Powell cross-check
        try:
            r = minimize(obj, best_par, method='Powell',
                         options={'xtol':1e-5, 'ftol':1e-5, 'maxiter':2000})
            if r.fun < best_val:
                best_val, best_par = r.fun, r.x
        except Exception:
            pass

    try:
        pop = max(6, 5 * k)
        r = differential_evolution(obj, bounds, seed=42, maxiter=100,
                                   tol=1e-5, popsize=pop, workers=1)
        if r.fun < best_val:
            best_val, best_par = r.fun, r.x
    except Exception:
        pass

    if best_par is None:
        print(f"  FAILED")
        return None

    E_fn   = E_fn_maker(best_par)
    Om, H0 = best_par[0], best_par[1]
    c_bao, c_cmb, c_sn, c_rsd, c_tot = chi2_all(E_fn, Om, H0)
    ac     = aicc(c_tot, k)
    d_ac   = ac - LCDM_AICC
    w0, wa = cpl_wa(E_fn, Om)
    h0_t   = (73.04 - H0) / np.sqrt(1.04**2 + 0.5**2)

    # Boundary check
    boundary = _at_boundary(best_par, bounds)
    boundary_names = [param_names[i] for i in boundary]

    param_str = ', '.join(f'{n}={v:.4f}' for n, v in zip(param_names, best_par))
    print(f"  {param_str}")
    if boundary_names:
        print(f"  !! BOUNDARY: {boundary_names}")
    print(f"  chi2_BAO={c_bao:.4f}  chi2_CMB={c_cmb:.4f}  chi2_SN={c_sn:.4f}  chi2_RSD={c_rsd:.4f}")
    print(f"  chi2_joint={c_tot:.4f}  AICc={ac:.4f}  dAICc={d_ac:+.4f}")
    print(f"  w0={w0:.4f}  wa={wa:.4f}  H0_tension={h0_t:.2f}sigma")

    return {
        'name': name, 'k': k,
        'params': {n: float(v) for n, v in zip(param_names, best_par)},
        'boundary_params': boundary_names,
        'chi2_bao': float(c_bao), 'chi2_cmb': float(c_cmb),
        'chi2_sn': float(c_sn),   'chi2_rsd': float(c_rsd),
        'chi2_joint': float(c_tot), 'aicc': float(ac), 'daicc': float(d_ac),
        'w0': float(w0) if w0 else None,
        'wa': float(wa) if wa else None,
        'H0_tension': float(h0_t),
    }


def verdict(res):
    if res is None: return 'FAILED'
    if res['boundary_params']: return 'K92 INVALID'
    d = res['daicc']
    w = res.get('wa')
    if d >= 0: return 'K90 KILL'
    if d >= -2: return 'Q90 PASS'
    if d >= -4: return 'Q91 STRONG'
    # d < -4
    wa_ok  = (w is not None and w < 0)
    h0_ok  = res['H0_tension'] < 4.01   # better than LCDM
    if wa_ok:   return 'Q92 GAME'
    return 'Q91 STRONG'


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    t0 = time.time()
    print("="*60)
    print("L36: wa<0 탐색 (L35 한계 해결)")
    print(f"LCDM baseline AICc = {LCDM_AICC:.4f}")
    print("="*60)

    print("\nWarming up SN cache...")
    get_sn()

    results = {}

    # 1. Model B' (priority 1: phantom허용 구조)
    res_Bp = fit_model(
        'Model_Bp',
        lambda p: (lambda z, Om: E_model_Bp(z, p[0], amp=p[2], gamma=p[3])),
        ['Om', 'H0', 'amp', 'gamma'],
        [(0.15, 0.50), (55., 82.), (0.01, 3.0), (-0.05, 0.5)],
        n_starts=30,
    )
    results['Bp'] = res_Bp

    # 2. Model D (priority 2: phantom자연 구조)
    res_D = fit_model(
        'Model_D',
        lambda p: (lambda z, Om: E_model_D(z, p[0], amp=p[2], beta=p[3])),
        ['Om', 'H0', 'amp', 'beta'],
        [(0.15, 0.50), (55., 82.), (-3.0, 3.0), (0.01, 5.0)],
        n_starts=30,
    )
    results['D'] = res_D

    # 3. Model C' (priority 3: 재최적화)
    res_Cp = fit_model(
        'Model_Cp',
        lambda p: (lambda z, Om: E_model_Cp(z, p[0], amp=p[2], c=p[3])),
        ['Om', 'H0', 'amp', 'c'],
        [(0.15, 0.50), (55., 82.), (0.5, 5.0), (0.5, 2.5)],
        n_starts=50,
    )
    results['Cp'] = res_Cp

    # 4. Model A'_fixed (priority 4: k=2, fast)
    res_Af = fit_model(
        'Model_Ap_fixed',
        lambda p: (lambda z, Om: E_model_Ap_fixed(z, p[0], n=1./3.)),
        ['Om', 'H0'],
        [(0.15, 0.50), (55., 82.)],
        n_starts=20,
    )
    results['Ap_fixed'] = res_Af

    # 5. Model A'_free (priority 5: k=3, n fitted)
    res_Afr = fit_model(
        'Model_Ap_free',
        lambda p: (lambda z, Om: E_model_Ap_free(z, p[0], n=p[2])),
        ['Om', 'H0', 'n'],
        [(0.15, 0.50), (55., 82.), (0.05, 1.5)],
        n_starts=25,
        extra_starts=[[0.30, 68., 0.333], [0.31, 68., 0.5], [0.29, 70., 0.2]],
    )
    results['Ap_free'] = res_Afr

    # ─── Summary ─────────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("SUMMARY (LCDM AICc baseline = {:.4f})".format(LCDM_AICC))
    print("="*60)

    order = [('Bp','Model B\''), ('D','Model D'), ('Cp','Model C\''),
             ('Ap_fixed','Model A\' fixed'), ('Ap_free','Model A\' free')]

    for key, label in order:
        res = results.get(key)
        v   = verdict(res)
        if res is None:
            print(f"\n{label}: FAILED")
            continue
        print(f"\n{label} k={res['k']}:")
        print(f"  chi2: BAO={res['chi2_bao']:.2f} CMB={res['chi2_cmb']:.2f} "
              f"SN={res['chi2_sn']:.2f} RSD={res['chi2_rsd']:.2f} total={res['chi2_joint']:.2f}")
        print(f"  AICc={res['aicc']:.2f}  dAICc={res['daicc']:+.2f}")
        print(f"  params={res['params']}")
        if res['boundary_params']:
            print(f"  !! BOUNDARY-PINNED: {res['boundary_params']} -> K92 INVALID")
        print(f"  w0={res['w0']}  wa={res['wa']}  wa<0: {res['wa'] is not None and res['wa']<0}")
        print(f"  H0 tension={res['H0_tension']:.2f}sigma")
        print(f"  VERDICT: {v}")

    # Save
    out = {**results, 'elapsed_s': time.time()-t0, 'lcdm_aicc': LCDM_AICC}
    out_path = os.path.join(_SCRIPT_DIR, 'l36_results.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2, default=lambda x: None)
    print(f"\nSaved to {out_path}")
    print(f"Total elapsed: {time.time()-t0:.1f}s")


if __name__ == '__main__':
    main()
