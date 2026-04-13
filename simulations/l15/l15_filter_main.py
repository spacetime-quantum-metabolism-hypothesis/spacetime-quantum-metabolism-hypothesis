# -*- coding: utf-8 -*-
"""
L15 Stage-0T + Stage-1: 5 survivors from A1 theory filter.
Uses DESI DR2 full 13-point covariance chi2.

Models (Stage-0T survivors):
  TF3 (F-G)  : OL0*(1+A*(E-1)*exp(-B*(E-1)^3))
  AX3 (F-C)  : OL0*(1+A*(1-cos(B*(Om*(1+z)^3-Om)/OL0)))
  HB3 (F-L)  : OL0*(1+A*(x_m^2/(B^2+x_m^2)^2 - norm))
  ST1 (F-W)  : OL0*exp(-A*((1+z)^3-1))*(1+B*(1+z)^3)/(1+B)
  EE2 (F-CL) : OL0*(1+A*(1-cos(B*ln(E))))

Stage-0T KILL (4 models excluded before data):
  F-S2 (AX2): sin^2 -> non-monotone, A1 violation
  F-P  (RM3): x^2*exp(-Bx^2) -> peak, A1 violation at high-z
  F-H  (H2) : Page curve, unrelated to A1+A2
  F-CS (AN3): cos(B*sqrt(x)) -> oscillatory, A1 violation
"""
import os, json, sys
import numpy as np
from scipy.optimize import minimize, curve_fit
from scipy.interpolate import interp1d

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
np.seterr(all='ignore')

_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_THIS))
sys.path.insert(0, os.path.join(_ROOT, 'simulations'))

# --- Import DESI DR2 13pt covariance from project ---
from desi_data import DESI_DR2, DESI_DR2_COV, DESI_DR2_COV_INV

c_SI    = 2.998e8
Mpc_m   = 3.086e22
OMEGA_R = 9.1e-5
rs_drag = 147.09
H0_KMS  = 67.7
H0_SI   = H0_KMS * 1e3 / Mpc_m

N_Z   = 3000
Z_MAX = 6.0
Z_ARR = np.linspace(0.0, Z_MAX, N_Z)

# 13-point observation vector (ordered as in desi_data.py)
OBS_13 = DESI_DR2['value']   # shape (13,)
INV_COV = DESI_DR2_COV_INV  # shape (13,13)

# z-values for each of the 13 measurements
Z_13 = DESI_DR2['z_eff']  # [0.295, 0.510, 0.510, 0.706, 0.706, 0.934, 0.934, 1.321, 1.321, 1.484, 1.484, 2.330, 2.330]
QTYPES = DESI_DR2['quantity']  # ['DV_over_rs', 'DM_over_rs', 'DH_over_rs', ...]


def _E_LCDM(Om, z_arr):
    OL0 = 1.0 - Om - OMEGA_R
    return np.sqrt(OMEGA_R*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0)


def _build_E_interp(z_arr, ode_arr, Om):
    E2 = OMEGA_R*(1+z_arr)**4 + Om*(1+z_arr)**3 + np.maximum(ode_arr, 0)
    E_arr = np.sqrt(np.maximum(E2, 1e-15))
    return interp1d(z_arr, E_arr, kind='cubic',
                    fill_value='extrapolate', bounds_error=False)


def _chi_interp(E_interp):
    """Cumulative comoving distance integral via trapezoid."""
    z_int = np.linspace(0, Z_MAX*0.99, 6000)
    inv_E = 1.0 / np.maximum(E_interp(z_int), 1e-10)
    dz = np.diff(z_int)
    cum = np.zeros(len(z_int))
    for i in range(1, len(z_int)):
        cum[i] = cum[i-1] + 0.5*(inv_E[i-1]+inv_E[i])*dz[i-1]
    return interp1d(z_int, cum, kind='cubic',
                    fill_value='extrapolate', bounds_error=False)


def chi2_13pt(z_arr, ode_arr, Om):
    """Full 13-point covariance chi2 using DESI DR2 official matrix."""
    E_interp = _build_E_interp(z_arr, ode_arr, Om)
    chi_func = _chi_interp(E_interp)
    fac = c_SI / (H0_SI * Mpc_m)

    pred = np.zeros(13)
    for i, (z, qt) in enumerate(zip(Z_13, QTYPES)):
        DM = fac * chi_func(z)
        DH = fac / E_interp(z)
        if qt == 'DV_over_rs':
            DV = (z * DM**2 * DH)**(1.0/3.0)
            pred[i] = DV / rs_drag
        elif qt == 'DM_over_rs':
            pred[i] = DM / rs_drag
        elif qt == 'DH_over_rs':
            pred[i] = DH / rs_drag

    if not np.all(np.isfinite(pred)):
        return 1e8
    resid = pred - OBS_13
    c2 = float(resid @ INV_COV @ resid)
    return c2 if np.isfinite(c2) and c2 < 1e8 else 1e8


def chi2_lcdm_baseline():
    """LCDM best-fit chi2 (Om optimized, H0=67.7 fixed)."""
    def obj(p):
        Om = p[0]
        if Om < 0.28 or Om > 0.36: return 1e8
        OL0 = 1.0 - Om - OMEGA_R
        ode_arr = np.full_like(Z_ARR, OL0)
        return chi2_13pt(Z_ARR, ode_arr, Om)
    res = minimize(obj, [0.315], method='Nelder-Mead',
                   options={'xatol':1e-6, 'fatol':1e-6, 'maxiter':3000})
    return res.fun, float(res.x[0])


def fit_cpl(z_arr, ode_arr):
    z_fit = np.linspace(0.01, 1.5, 300)
    dz = 1e-4
    ode_i = interp1d(z_arr, ode_arr, kind='cubic',
                     fill_value='extrapolate', bounds_error=False)
    u   = np.array([float(ode_i(z)) for z in z_fit])
    u_p = np.array([float(ode_i(z+dz)) for z in z_fit])
    u_m = np.array([float(ode_i(max(z-dz, 1e-5))) for z in z_fit])
    dlnu = (u_p-u_m) / (2*dz*np.maximum(u, 1e-20))
    w_z = (1+z_fit)*dlnu/3.0 - 1.0
    def w_cpl(z, w0, wa): return w0 + wa*(1-1/(1+z))
    try:
        popt, _ = curve_fit(w_cpl, z_fit, w_z, p0=[-0.95, -0.2],
                            bounds=([-3.0, -10.0], [0.5, 5.0]), maxfev=5000)
        return float(popt[0]), float(popt[1])
    except Exception:
        return float('nan'), float('nan')


def aicc(chi2_val, k, n):
    """AICc = AIC + 2k(k+1)/(n-k-1), small-sample corrected."""
    aic = chi2_val + 2*k
    corr = 2*k*(k+1) / max(n-k-1, 1)
    return aic + corr


def fit_model(make_fn, starts, n_data=13):
    best = (1e9, None)
    for p0 in starts:
        def obj(p):
            Om = p[0]
            if Om < 0.28 or Om > 0.36: return 1e8
            try:
                arr = make_fn(p)
                if arr is None: return 1e8
                return chi2_13pt(Z_ARR, arr, Om)
            except Exception:
                return 1e8
        res = minimize(obj, p0, method='Nelder-Mead',
                       options={'xatol':1e-7, 'fatol':1e-7, 'maxiter':8000})
        if res.fun < best[0]:
            best = (res.fun, res.x)
    if best[1] is None:
        return None
    p = best[1]
    Om = float(np.clip(p[0], 0.28, 0.36))
    arr = make_fn(p)
    if arr is None:
        return None
    chi2_val = chi2_13pt(Z_ARR, arr, Om)
    w0, wa = fit_cpl(Z_ARR, arr)
    k = len(p)
    return {
        'chi2': chi2_val,
        'w0': round(w0, 3),
        'wa': round(wa, 3),
        'Om': round(Om, 4),
        'k': k,
        'AICc': round(aicc(chi2_val, k, n_data), 3),
        'p': [float(x) for x in p],
    }


# ============================================================
# Model definitions (from L14 implementations)
# ============================================================

def make_TF3(p):
    """TF3 (F-G): OL0*(1+A*(E-1)*exp(-B*(E-1)^3))"""
    Om=p[0]; A=p[1]; B=max(p[2], 0.01)
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    x = E - 1.0
    return OL0*(1.0 + A*x*np.exp(-B*x**3))


def make_AX3(p):
    """AX3 (F-C): OL0*(1+A*(1-cos(B*(Om*(1+z)^3-Om)/OL0)))"""
    Om=p[0]; A=p[1]; B=max(p[2], 0.01)
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01: return None
    theta_z = B*(Om*(1+Z_ARR)**3 - Om) / max(OL0, 1e-10)
    return OL0*(1.0 + A*(1.0 - np.cos(np.minimum(theta_z, 20))))


def make_HB3(p):
    """HB3 (F-L): OL0*(1+A*(x_m^2/(B^2+x_m^2)^2 - norm))"""
    Om=p[0]; A=p[1]; B=max(p[2], 0.01)
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01: return None
    x_z = Om*(1+Z_ARR)**3
    x_0 = Om
    f_z = x_z**2 / (B**2 + x_z**2)**2
    f_0 = x_0**2 / (B**2 + x_0**2)**2
    return OL0*(1.0 + A*(f_z - f_0))


def make_ST1(p):
    """ST1 (F-W): OL0*exp(-A*((1+z)^3-1))*(1+B*(1+z)^3)/(1+B)"""
    Om=p[0]; A=max(p[1], 0.0); B=max(p[2], 0.0)
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01: return None
    x_z = (1+Z_ARR)**3 - 1.0
    f_z = np.exp(-A*x_z) * (1.0 + B*(1+Z_ARR)**3)
    f_0 = 1.0 * (1.0 + B)
    return OL0*f_z/f_0


def make_EE2(p):
    """EE2 (F-CL): OL0*(1+A*(1-cos(B*ln(E_LCDM))))"""
    Om=p[0]; A=p[1]; B=max(p[2], 0.01)
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    theta_z = B*np.log(np.maximum(E, 1e-10))
    return OL0*(1.0 + A*(1.0 - np.cos(np.minimum(theta_z, 20))))


# ============================================================
# Multiple starting points
# ============================================================

MODELS = [
    ('TF3-FermiLiquid', make_TF3, [
        [0.305,  1.0, 0.3],
        [0.305,  2.0, 0.1],
        [0.305,  0.5, 0.5],
        [0.310,  1.5, 0.2],
        [0.300,  3.0, 0.05],
    ]),
    ('AX3-AxionPot', make_AX3, [
        [0.305,  0.5, 1.0],
        [0.305,  1.0, 0.5],
        [0.310,  0.3, 2.0],
        [0.300,  0.8, 1.5],
        [0.305,  0.2, 3.0],
    ]),
    ('HB3-Lorentzian', make_HB3, [
        [0.305,  5.0, 0.30],
        [0.305, 10.0, 0.20],
        [0.310,  3.0, 0.50],
        [0.300,  8.0, 0.15],
        [0.305, 15.0, 0.10],
    ]),
    ('ST1-StringWind', make_ST1, [
        [0.305, 0.1, 0.30],
        [0.305, 0.2, 0.10],
        [0.310, 0.05, 0.50],
        [0.300, 0.15, 0.20],
        [0.305, 0.08, 0.40],
    ]),
    ('EE2-CosLog', make_EE2, [
        [0.305,  1.0, 2.0],
        [0.305,  2.0, 1.0],
        [0.310,  0.5, 3.0],
        [0.300,  1.5, 1.5],
        [0.305,  3.0, 0.5],
    ]),
]


def main():
    print("L15 Stage-0T + Stage-1: 13pt covariance chi2")
    print("=" * 65)

    # --- LCDM baseline ---
    print("Computing LCDM baseline (13pt)...")
    lcdm_chi2, lcdm_Om = chi2_lcdm_baseline()
    lcdm_k = 1
    lcdm_aicc = aicc(lcdm_chi2, lcdm_k, 13)
    print(f"  LCDM: chi2={lcdm_chi2:.3f}  Om={lcdm_Om:.4f}  AICc={lcdm_aicc:.3f}")
    print()

    results = {'LCDM': {'chi2': lcdm_chi2, 'Om': lcdm_Om, 'k': 1,
                        'AICc': lcdm_aicc, 'w0': -1.0, 'wa': 0.0}}

    print(f"{'Model':<20} {'chi2':>8} {'Om':>6} {'w0':>7} {'wa':>7} "
          f"{'AICc':>8} {'dAICc':>7} {'Verdict':>8}")
    print("-" * 85)

    for label, make_fn, starts in MODELS:
        r = fit_model(make_fn, starts, n_data=13)
        if r is None:
            print(f"{label:<20} FAILED")
            continue

        dAICc = r['AICc'] - lcdm_aicc
        verdict = 'PASS' if dAICc < 0 else 'KILL'
        # Additional kill: chi2 > LCDM
        if r['chi2'] > lcdm_chi2:
            verdict = 'KILL(chi2)'

        r['dAICc'] = round(dAICc, 3)
        r['verdict'] = verdict
        results[label] = r

        print(f"{label:<20} {r['chi2']:>8.3f} {r['Om']:>6.4f} {r['w0']:>7.3f} "
              f"{r['wa']:>7.3f} {r['AICc']:>8.3f} {dAICc:>+7.3f} {verdict:>8}")

    print()
    print("Stage-1 PASS (dAICc < 0 AND chi2 < LCDM):")
    for k, v in results.items():
        if k == 'LCDM': continue
        if v.get('verdict', '') == 'PASS':
            print(f"  {k}: chi2={v['chi2']:.3f}, w0={v['w0']}, wa={v['wa']}, dAICc={v['dAICc']:+.3f}")

    # --- Save ---
    out = os.path.join(_THIS, 'l15_stage1_results.json')
    def _j(v):
        if isinstance(v, (np.floating, np.float64, np.float32)): return float(v)
        if isinstance(v, (np.integer,)): return int(v)
        if isinstance(v, list): return [_j(x) for x in v]
        return v
    save = {k: {kk: _j(vv) for kk, vv in val.items()} for k, val in results.items()}
    with open(out, 'w') as f:
        json.dump(save, f, indent=2)
    print(f"\nSaved -> {out}")


if __name__ == '__main__':
    main()
