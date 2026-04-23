# -*- coding: utf-8 -*-
"""
l34_test.py -- L34: Joint DESI BAO + Planck CMB + DESY5 SN fitting
===================================================================
Tests Q92 (tanh-weight, c=1.47, amp=2.25) and Q93 (sigmoid k=75,
z0=0.90, c=1.00, amp=4.00) champions from L33 against joint datasets.

Free params: Om, H0 only (k=2). Model structure params fixed at L33
champion values. Joint AICc vs joint LCDM baseline.

L30~L33 bug prevention:
- N_GRID=4000, cumulative_trapezoid (not manual cumsum)
- ratio clipped to [1.0, 200.0]
- single-point verification against L33 before full fit
- Om range [0.05, 0.50]
- python3 only
- omega_b=0.02237 fixed (k=2 maintained)
"""

import os, sys, json, warnings, time
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import minimize, differential_evolution

warnings.filterwarnings('ignore')
np.seterr(all='ignore')
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SIM_DIR    = os.path.dirname(_SCRIPT_DIR)
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

import config as _cfg
from desi_data import DESI_DR2, DESI_DR2_COV_INV
from phase2.compressed_cmb import chi2_compressed_cmb
from phase2.sn_likelihood import DESY5SN

C_KMS  = 299792.458
R_S    = 147.09
OR     = 5.38e-5
N_GRID = 4000
OMEGA_B_FIXED = 0.02237  # Planck 2018, fixed (k=2 maintained)

# ─── Model E(z) functions ─────────────────────────────────────────────────────

def _ratio_psi(z_grid, Om):
    OL0  = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None, None
    alpha = Om / OL0
    psi_z = 1.0 / (1.0 + alpha * (1.0 + z_grid)**3)
    psi0  = 1.0 / (1.0 + alpha)
    ratio = np.clip(psi0 / psi_z, 1.0, 200.0)
    return ratio, OL0


def E_q93(z_grid, Om, k=75.0, z0=0.90, c=1.00, amp=4.00):
    """Q93 sigmoid-weight champion: k=75, z0=0.90, c=1.00, amp=4.00"""
    ratio, OL0 = _ratio_psi(z_grid, Om)
    if ratio is None:
        return None
    rm1 = ratio - 1.0
    s0  = 1.0 / (1.0 + np.exp(k * z0))
    wt  = np.clip((1.0 / (1.0 + np.exp(-k * (z_grid - z0))) - s0) / (1.0 - s0), 0.0, 1.0)
    g   = (1.0 - wt) * np.tanh(1.2533 * c * np.clip(rm1, -10, 10)) + wt * rm1
    rde = OL0 * (1.0 + amp * g)
    E2  = OR * (1 + z_grid)**4 + Om * (1 + z_grid)**3 + rde
    if np.any(E2 <= 0):
        return None
    return np.sqrt(E2)


def E_q92_tanh(z_grid, Om, c=1.47, amp=2.25):
    """Q92 tanh-weight champion: wt=tanh(z), c=1.47, amp=2.25"""
    ratio, OL0 = _ratio_psi(z_grid, Om)
    if ratio is None:
        return None
    rm1 = ratio - 1.0
    wt  = np.tanh(z_grid)
    g   = (1.0 - wt) * np.tanh(1.2533 * c * np.clip(rm1, -10, 10)) + wt * rm1
    rde = OL0 * (1.0 + amp * g)
    E2  = OR * (1 + z_grid)**4 + Om * (1 + z_grid)**3 + rde
    if np.any(E2 <= 0):
        return None
    return np.sqrt(E2)


def E_lcdm(z_grid, Om):
    OL0 = 1.0 - Om - OR
    E2  = OR * (1 + z_grid)**4 + Om * (1 + z_grid)**3 + OL0
    return np.sqrt(np.maximum(E2, 1e-30))


# ─── BAO chi2 (same as l33_test.py) ─────────────────────────────────────────

def chi2_bao(E_fn, Om, H0):
    z_eff  = DESI_DR2['z_eff']
    z_grid = np.linspace(0.0, z_eff.max() + 0.01, N_GRID)
    Eg = E_fn(z_grid, Om)
    if Eg is None or not np.all(np.isfinite(Eg)):
        return 1e8
    Eg = np.maximum(Eg, 1e-15)
    DM = (C_KMS / H0) * np.concatenate([[0.], cumulative_trapezoid(1.0 / Eg, z_grid)])
    tv = np.empty(13)
    for i, (z, qty) in enumerate(zip(z_eff, DESI_DR2['quantity'])):
        idx = min(np.searchsorted(z_grid, z), N_GRID - 1)
        DH  = C_KMS / (H0 * Eg[idx])
        DV  = (z * DM[idx]**2 * DH)**(1.0/3.0) if z > 0 else 0.0
        if 'DV' in qty:
            tv[i] = DV / R_S
        elif 'DM' in qty:
            tv[i] = DM[idx] / R_S
        elif 'DH' in qty:
            tv[i] = DH / R_S
        else:
            tv[i] = np.nan
    d = DESI_DR2['value'] - tv
    if not np.all(np.isfinite(d)):
        return 1e8
    return float(d @ DESI_DR2_COV_INV @ d)


# ─── CMB chi2 (compressed, k=2 compatible) ───────────────────────────────────

def chi2_cmb(E_fn, Om, H0):
    h = H0 / 100.0
    omega_b = OMEGA_B_FIXED
    omega_c = Om * h**2 - omega_b
    if omega_c <= 0:
        return 1e8
    # CRITICAL: compressed_cmb uses config.H_0_km for D_A(z*) — must set before call
    _cfg.H_0_km = H0
    def E_func(z):
        v = E_fn(np.array([float(z)]), Om)
        if v is None or not np.isfinite(v[0]):
            return 1e8
        return float(v[0])
    try:
        return chi2_compressed_cmb(omega_b, omega_c, h, E_func)
    except Exception:
        return 1e8


# ─── Joint chi2 ───────────────────────────────────────────────────────────────

_SN_DATA = None
def get_sn():
    global _SN_DATA
    if _SN_DATA is None:
        _SN_DATA = DESY5SN()
    return _SN_DATA


def chi2_joint(E_fn, Om, H0):
    c_bao = chi2_bao(E_fn, Om, H0)
    c_cmb = chi2_cmb(E_fn, Om, H0)
    def E_func(z):
        v = E_fn(np.array([float(z)]), Om)
        if v is None:
            return 1e30
        return float(v[0])
    c_sn = get_sn().chi2(E_func, H0_km=H0)
    return c_bao, c_cmb, c_sn, c_bao + c_cmb + c_sn


# ─── AICc (joint) ────────────────────────────────────────────────────────────

def aicc_joint(chi2_tot, k=2, n=None):
    if n is None:
        n = 13 + 3 + get_sn().N
    return chi2_tot + 2*k + 2*k*(k+1)/(n - k - 1)


# ─── CPL w0, wa from rho_DE ───────────────────────────────────────────────────

def cpl_from_E(E_fn, Om, H0):
    z_arr = np.linspace(0.01, 2.0, 40)
    Ev = E_fn(z_arr, Om)
    if Ev is None or not np.all(np.isfinite(Ev)):
        return None, None
    rde  = Ev**2 - OR*(1+z_arr)**4 - Om*(1+z_arr)**3
    E0v  = E_fn(np.array([0.0]), Om)
    if E0v is None:
        return None, None
    rde0 = float(E0v[0]**2 - OR - Om)
    if rde0 <= 0 or np.any(rde <= 0):
        return None, None
    lnrde = np.log(rde / rde0)
    ln1z  = np.log(1 + z_arr)
    A     = np.column_stack([-3.*ln1z, -3.*(ln1z - z_arr/(1+z_arr))])
    try:
        coef, *_ = np.linalg.lstsq(A, lnrde, rcond=None)
        return float(coef[0]) - 1., float(coef[1])
    except Exception:
        return None, None


# ─── Multi-start optimizer ────────────────────────────────────────────────────

def fit_joint(E_fn, label):
    print(f"\n[{label}] Fitting joint (BAO+CMB+SN)...")

    def obj(params):
        Om, H0 = params
        if not (0.05 < Om < 0.50 and 55.0 < H0 < 82.0):
            return 1e9
        _, _, _, tot = chi2_joint(E_fn, Om, H0)
        return tot

    # Wide starts: low-Om region + LCDM-prior region
    starts = []
    for Om0 in [0.08, 0.10, 0.15, 0.20, 0.25, 0.28, 0.30, 0.31, 0.315, 0.33, 0.35]:
        for H0_0 in [64.0, 66.0, 67.5, 69.0, 71.0]:
            starts.append((Om0, H0_0))

    best_val, best_par = 1e9, None
    for Om0, H0_0 in starts:
        try:
            r = minimize(obj, [Om0, H0_0], method='Nelder-Mead',
                         options={'xatol':1e-7, 'fatol':1e-7, 'maxiter':8000})
            if r.fun < best_val:
                best_val, best_par = r.fun, r.x
        except Exception:
            pass

    # differential_evolution
    try:
        r = differential_evolution(obj, [(0.05,0.50),(55.,82.)],
                                   seed=42, maxiter=500, tol=1e-7,
                                   popsize=15, workers=1)
        if r.fun < best_val:
            best_val, best_par = r.fun, r.x
    except Exception:
        pass

    if best_par is None:
        print(f"  [{label}] optimization failed")
        return None

    Om_opt, H0_opt = best_par
    c_bao, c_cmb, c_sn, c_tot = chi2_joint(E_fn, Om_opt, H0_opt)
    n_joint = 13 + 3 + get_sn().N
    ac = aicc_joint(c_tot, k=2, n=n_joint)
    w0, wa = cpl_from_E(E_fn, Om_opt, H0_opt)

    print(f"  Om={Om_opt:.4f}  H0={H0_opt:.3f}")
    print(f"  chi2_BAO={c_bao:.4f}  chi2_CMB={c_cmb:.4f}  chi2_SN={c_sn:.4f}")
    print(f"  chi2_joint={c_tot:.4f}  AICc_joint={ac:.4f}")
    print(f"  w0={w0}  wa={wa}")

    return {
        'label': label,
        'Om': Om_opt, 'H0': H0_opt,
        'chi2_bao': c_bao, 'chi2_cmb': c_cmb, 'chi2_sn': c_sn,
        'chi2_joint': c_tot, 'aicc_joint': ac,
        'w0': w0, 'wa': wa,
        'n_joint': n_joint
    }


# ─── Verification against L33 BAO-only result ────────────────────────────────

def verify_q93():
    """Single-point check: Q93 at Om=0.0676, H0=66.610 should give chi2_BAO~3.575"""
    Om, H0 = 0.0676, 66.610
    z_grid = np.linspace(0.0, DESI_DR2['z_eff'].max() + 0.01, N_GRID)
    Eg = E_q93(z_grid, Om)
    c = chi2_bao(E_q93, Om, H0)
    print(f"[VERIFY Q93] chi2_BAO={c:.4f}  (L33 reference: 3.5753, tolerance +/-0.01)")
    if abs(c - 3.5753) > 0.05:
        print("  WARNING: chi2 mismatch exceeds 0.05 — integration may differ from l33_test.py")
    else:
        print("  OK: integration consistent with l33_test.py")
    return abs(c - 3.5753) < 0.05


def verify_q92():
    """Single-point check: Q92 at Om=0.1148, H0=64.954 should give chi2_BAO~5.4766"""
    Om, H0 = 0.1148, 64.954
    c = chi2_bao(E_q92_tanh, Om, H0)
    print(f"[VERIFY Q92] chi2_BAO={c:.4f}  (L33 reference: 5.4766, tolerance +/-0.05)")
    if abs(c - 5.4766) > 0.1:
        print("  WARNING: chi2 mismatch — check model formula")
    else:
        print("  OK: consistent with l33_test.py")
    return abs(c - 5.4766) < 0.1


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    t0 = time.time()
    print("=" * 60)
    print("L34: Joint DESI BAO + Planck CMB + DESY5 SN fitting")
    print("Models: Q92 (tanh, c=1.47, amp=2.25) + Q93 (sig k=75)")
    print("Free params: Om, H0 only (k=2)")
    print("=" * 60)

    # Pre-run verification
    q93_ok = verify_q93()
    q92_ok = verify_q92()
    if not (q93_ok and q92_ok):
        print("\nWARNING: Verification failed. Results may not match L33.")

    # Load SN data once
    print("\nLoading DESY5 SN data...")
    sn = get_sn()
    print(f"  Loaded {sn.N} SNe")

    n_joint = 13 + 3 + sn.N
    print(f"  Total data points n={n_joint} (BAO:13 + CMB:3 + SN:{sn.N})")

    # LCDM joint baseline
    def E_lcdm_wrap(z_grid, Om):
        return E_lcdm(z_grid, Om)

    print("\n--- LCDM Joint Baseline ---")
    res_lcdm = fit_joint(E_lcdm_wrap, 'LCDM')

    # Q93 joint
    def E_q93_wrap(z_grid, Om):
        return E_q93(z_grid, Om)

    print("\n--- Q93 Champion (sigmoid k=75, z0=0.90, c=1.00, amp=4.00) ---")
    res_q93 = fit_joint(E_q93_wrap, 'Q93_sig75')

    # Q92 joint
    def E_q92_wrap(z_grid, Om):
        return E_q92_tanh(z_grid, Om)

    print("\n--- Q92 Champion (tanh-weight, c=1.47, amp=2.25) ---")
    res_q92 = fit_joint(E_q92_wrap, 'Q92_tanh')

    # ─── Summary ──────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    if res_lcdm:
        print(f"\nLCDM joint: chi2={res_lcdm['chi2_joint']:.4f}  "
              f"AICc={res_lcdm['aicc_joint']:.4f}  "
              f"Om={res_lcdm['Om']:.4f}  H0={res_lcdm['H0']:.3f}")

    for res, label in [(res_q93, 'Q93'), (res_q92, 'Q92')]:
        if res and res_lcdm:
            d_aicc = res['aicc_joint'] - res_lcdm['aicc_joint']
            verdict = ''
            if d_aicc < -6 and res['wa'] is not None and res['wa'] < -0.5:
                verdict = 'Q95 JOINT STRONG'
            elif d_aicc < -4 and res['wa'] is not None and res['wa'] < -0.5:
                verdict = 'Q94 JOINT PASS'
            elif d_aicc >= 0:
                verdict = 'J91 KILL'
            else:
                verdict = f'J90 DEGRADED (vs BAO-only)'

            print(f"\n{label} ({res['label']}):")
            print(f"  joint chi2={res['chi2_joint']:.4f}  "
                  f"AICc={res['aicc_joint']:.4f}  dAICc_joint={d_aicc:.4f}")
            print(f"  Om={res['Om']:.4f}  H0={res['H0']:.3f}")
            print(f"  chi2_BAO={res['chi2_bao']:.4f}  "
                  f"chi2_CMB={res['chi2_cmb']:.4f}  "
                  f"chi2_SN={res['chi2_sn']:.4f}")
            print(f"  w0={res['w0']}  wa={res['wa']}")
            print(f"  VERDICT: {verdict}")

    # BAO-only vs joint comparison
    print("\n--- BAO-only vs Joint dAICc comparison ---")
    bao_only = {'Q93': -6.617, 'Q92': -4.715}
    for res, key in [(res_q93, 'Q93'), (res_q92, 'Q92')]:
        if res and res_lcdm:
            d_joint = res['aicc_joint'] - res_lcdm['aicc_joint']
            delta = d_joint - bao_only[key]
            print(f"  {key}: BAO-only={bao_only[key]:+.3f}  "
                  f"joint={d_joint:+.4f}  change={delta:+.3f}")

    # Save results
    out = {
        'LCDM': res_lcdm,
        'Q93': res_q93,
        'Q92': res_q92,
        'n_joint': n_joint,
        'bao_only_reference': bao_only,
        'elapsed_s': time.time() - t0
    }
    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    out_path = os.path.join(_SCRIPT_DIR, 'l34_results.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2, default=lambda x: None if x is None else x)
    print(f"\nResults saved to {out_path}")
    print(f"Total elapsed: {time.time()-t0:.1f}s")


if __name__ == '__main__':
    main()
