# -*- coding: utf-8 -*-
"""
L15 Stage-2 (physical filter) + Stage-3 (joint BAO+SN+CMB+RSD).
Parallel execution: one process per model (up to 5 cores).
"""
import os, json, sys, time
import numpy as np
from scipy.optimize import minimize, curve_fit
from scipy.interpolate import interp1d
import multiprocessing as mp

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
np.seterr(all='ignore')

_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_THIS))
_SIMS = os.path.join(_ROOT, 'simulations')
_L3   = os.path.join(_SIMS, 'l3')
for _p in (_SIMS, _L3, os.path.join(_SIMS, 'phase2')):
    if _p not in sys.path:
        sys.path.insert(0, _p)

OMEGA_R = 9.1e-5
H0_KMS  = 67.7
H0_H    = H0_KMS / 100.0
OMEGA_B = 0.02237
RS_DRAG = 147.09
N_Z     = 3000
Z_MAX   = 6.0
Z_ARR   = np.linspace(0.0, Z_MAX, N_Z)


def _E_LCDM(Om, z_arr):
    OL0 = 1.0 - Om - OMEGA_R
    return np.sqrt(OMEGA_R*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0)


# ── model definitions ────────────────────────────────────────────────────────

def make_TF3(p):
    Om=p[0]; A=p[1]; B=max(p[2], 0.01)
    OL0 = 1.0-Om-OMEGA_R
    if OL0<0.01: return None
    E=_E_LCDM(Om,Z_ARR); x=E-1.0
    return OL0*(1.0+A*x*np.exp(-B*x**3))

def make_AX3(p):
    Om=p[0]; A=p[1]; B=max(p[2], 0.01)
    OL0 = 1.0-Om-OMEGA_R
    if OL0<0.01: return None
    theta = B*(Om*(1+Z_ARR)**3-Om)/max(OL0,1e-10)
    return OL0*(1.0+A*(1.0-np.cos(np.minimum(theta,20))))

def make_HB3(p):
    Om=p[0]; A=p[1]; B=max(p[2], 0.01)
    OL0 = 1.0-Om-OMEGA_R
    if OL0<0.01: return None
    x_z=Om*(1+Z_ARR)**3; x_0=Om
    return OL0*(1.0+A*(x_z**2/(B**2+x_z**2)**2 - x_0**2/(B**2+x_0**2)**2))

def make_ST1(p):
    Om=p[0]; A=max(p[1],0.0); B=max(p[2],0.0)
    OL0 = 1.0-Om-OMEGA_R
    if OL0<0.01: return None
    x_z=(1+Z_ARR)**3-1.0
    return OL0*np.exp(-A*x_z)*(1.0+B*(1+Z_ARR)**3)/(1.0+B)

def make_EE2(p):
    Om=p[0]; A=p[1]; B=max(p[2], 0.01)
    OL0 = 1.0-Om-OMEGA_R
    if OL0<0.01: return None
    E=_E_LCDM(Om,Z_ARR)
    theta=B*np.log(np.maximum(E,1e-10))
    return OL0*(1.0+A*(1.0-np.cos(np.minimum(theta,20))))

MAKE_FNS = {
    'TF3-FermiLiquid': make_TF3,
    'AX3-AxionPot':    make_AX3,
    'HB3-Lorentzian':  make_HB3,
    'ST1-StringWind':  make_ST1,
    'EE2-CosLog':      make_EE2,
}


# ── helpers ──────────────────────────────────────────────────────────────────

def fit_cpl(ode_arr):
    z_fit = np.linspace(0.01, 1.5, 300); dz=1e-4
    ode_i = interp1d(Z_ARR, ode_arr, kind='cubic',
                     fill_value='extrapolate', bounds_error=False)
    u   = np.array([float(ode_i(z)) for z in z_fit])
    u_p = np.array([float(ode_i(z+dz)) for z in z_fit])
    u_m = np.array([float(ode_i(max(z-dz,1e-5))) for z in z_fit])
    dlnu = (u_p-u_m)/(2*dz*np.maximum(u,1e-20))
    w_z  = (1+z_fit)*dlnu/3.0 - 1.0
    def w_cpl(z,w0,wa): return w0+wa*(1-1/(1+z))
    try:
        popt,_ = curve_fit(w_cpl, z_fit, w_z, p0=[-0.95,-0.2],
                           bounds=([-3.,-10.],[0.5,5.]), maxfev=5000)
        return float(popt[0]), float(popt[1])
    except Exception:
        return float('nan'), float('nan')


def make_E_func(make_fn, p):
    arr = make_fn(p)
    if arr is None: return None
    Om = float(np.clip(p[0], 0.28, 0.36))
    E2  = OMEGA_R*(1+Z_ARR)**4 + Om*(1+Z_ARR)**3 + np.maximum(arr,0)
    E_a = np.sqrt(np.maximum(E2,1e-15))
    ei  = interp1d(Z_ARR, E_a, kind='cubic', fill_value='extrapolate', bounds_error=False)
    return lambda z: float(ei(z))


# ── stage-2 check ─────────────────────────────────────────────────────────────

def stage2_check(p, make_fn):
    arr = make_fn(p)
    kills = []
    if arr is None or np.any(arr < -1e-4):
        kills.append('omega_de<0')
        return False, kills
    w0, wa = fit_cpl(arr)
    if not (np.isfinite(w0) and np.isfinite(wa)):
        kills.append('CPL fail')
        return False, kills
    if not (-1.5 < w0 < -0.3): kills.append(f'w0={w0:.3f}')
    if not (-3.0 < wa < 1.5):  kills.append(f'wa={wa:.3f}')
    Om = p[0]
    if not (0.28 < Om < 0.36): kills.append(f'Om={Om:.4f}')
    ode_i = interp1d(Z_ARR, arr, kind='cubic', fill_value='extrapolate', bounds_error=False)
    if float(ode_i(3.0)) > 0.05*Om*(1+3.0)**3:
        kills.append('early DE at z=3')
    return len(kills)==0, kills


# ── per-model worker (runs in separate process) ───────────────────────────────

def run_model(args):
    label, p_init, lcdm_total = args

    # re-import inside worker (spawn-safe)
    import warnings
    warnings.filterwarnings('ignore')
    from l3.data_loader import chi2_joint, get_data
    get_data()   # preload SN data once

    make_fn = MAKE_FNS[label]

    # Stage-2
    s2_ok, kills = stage2_check(p_init, make_fn)
    if not s2_ok:
        return label, {'stage2': 'KILL', 'kills': kills}

    # Stage-3 optimise
    omega_b = OMEGA_B; h = H0_H

    def obj(params):
        p = list(params)
        p[0] = float(np.clip(p[0], 0.28, 0.36))
        omega_c = p[0]*h**2 - omega_b
        if omega_c <= 0.01: return 1e8
        E_func = make_E_func(make_fn, p)
        if E_func is None: return 1e8
        try:
            res = chi2_joint(E_func, rd=RS_DRAG, Omega_m=p[0],
                             omega_b=omega_b, omega_c=omega_c,
                             h=h, H0_km=H0_KMS)
            v = res['total']
            return v if np.isfinite(v) else 1e8
        except Exception:
            return 1e8

    starts = [
        p_init,
        [p_init[0]*0.995, p_init[1],     p_init[2]],
        [p_init[0]*1.005, p_init[1],     p_init[2]],
        [p_init[0],       p_init[1]*0.9, p_init[2]],
        [p_init[0],       p_init[1]*1.1, p_init[2]],
    ]
    best = (1e9, p_init)
    for s in starts:
        try:
            res = minimize(obj, s, method='Nelder-Mead',
                           options={'xatol':1e-5,'fatol':1e-5,'maxiter':2000})
            if res.fun < best[0]:
                best = (res.fun, list(res.x))
        except Exception:
            pass

    p_best = best[1]
    Om_best = float(np.clip(p_best[0], 0.28, 0.36))
    omega_c = Om_best*h**2 - omega_b
    E_func  = make_E_func(make_fn, p_best)
    if E_func is None:
        return label, {'stage2':'PASS','stage3':'FAILED'}

    res = chi2_joint(E_func, rd=RS_DRAG, Omega_m=Om_best,
                     omega_b=omega_b, omega_c=omega_c, h=h, H0_km=H0_KMS)
    arr = make_fn(p_best)
    w0, wa = fit_cpl(arr) if arr is not None else (float('nan'), float('nan'))
    delta = res['total'] - lcdm_total

    return label, {
        'stage2': 'PASS',
        'stage3': 'PASS' if delta < 2.0 else 'KILL',
        'chi2_bao':   round(res['bao'],   3),
        'chi2_sn':    round(res['sn'],    3),
        'chi2_cmb':   round(res['cmb'],   3),
        'chi2_rsd':   round(res['rsd'],   3),
        'chi2_joint': round(res['total'], 3),
        'delta_joint':round(delta,        3),
        'w0':  round(w0, 3),
        'wa':  round(wa, 3),
        'Om':  round(Om_best, 4),
        'p':   [float(x) for x in p_best],
    }


# ── LCDM joint baseline (main process) ───────────────────────────────────────

def lcdm_joint_baseline(Om_lcdm):
    from l3.data_loader import chi2_joint, get_data
    get_data()
    h = H0_H; omega_c = Om_lcdm*h**2 - OMEGA_B
    OL0 = 1.0-Om_lcdm-OMEGA_R
    def E(z): return float(np.sqrt(OMEGA_R*(1+z)**4+Om_lcdm*(1+z)**3+OL0))
    res = chi2_joint(E, rd=RS_DRAG, Omega_m=Om_lcdm,
                     omega_b=OMEGA_B, omega_c=omega_c, h=h, H0_km=H0_KMS)
    return res


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    stage1_path = os.path.join(_THIS, 'l15_stage1_results.json')
    with open(stage1_path) as f:
        stage1 = json.load(f)

    Om_lcdm = stage1['LCDM'].get('Om', 0.319)
    print(f"LCDM joint baseline (Om={Om_lcdm:.4f})...")
    lcdm_res = lcdm_joint_baseline(Om_lcdm)
    lcdm_total = lcdm_res['total']
    print(f"  LCDM: bao={lcdm_res['bao']:.2f} sn={lcdm_res['sn']:.2f} "
          f"cmb={lcdm_res['cmb']:.2f} rsd={lcdm_res['rsd']:.2f} "
          f"total={lcdm_total:.2f}\n")

    # build task list from Stage-1 survivors
    tasks = []
    for label in MAKE_FNS:
        if label not in stage1: continue
        p_init = stage1[label]['p']
        tasks.append((label, p_init, lcdm_total))

    print(f"Running {len(tasks)} models in parallel (up to {len(tasks)} cores)...")
    t0 = time.time()

    ctx = mp.get_context('spawn')
    with ctx.Pool(processes=len(tasks)) as pool:
        results_list = pool.map(run_model, tasks)

    elapsed = time.time() - t0
    print(f"Done in {elapsed/60:.1f} min.\n")

    results = {'LCDM': {
        'chi2_joint': round(lcdm_total,3),
        'chi2_bao':   round(lcdm_res['bao'],3),
        'chi2_sn':    round(lcdm_res['sn'],3),
        'chi2_cmb':   round(lcdm_res['cmb'],3),
        'chi2_rsd':   round(lcdm_res['rsd'],3),
        'w0':-1.0,'wa':0.0,
    }}

    print(f"{'Model':<22} {'S2':>4} {'S3':>4} {'joint':>7} {'bao':>6} "
          f"{'sn':>6} {'cmb':>6} {'rsd':>6} {'dJnt':>6} {'w0':>6} {'wa':>6}")
    print("-" * 90)

    for label, r in results_list:
        results[label] = r
        s2 = r.get('stage2','?')
        if s2 == 'KILL':
            print(f"{label:<22} KILL  —    kills={r.get('kills')}")
            continue
        s3 = r.get('stage3','?')
        print(f"{label:<22} {s2:>4} {s3:>4} "
              f"{r.get('chi2_joint',0):>7.2f} {r.get('chi2_bao',0):>6.2f} "
              f"{r.get('chi2_sn',0):>6.2f} {r.get('chi2_cmb',0):>6.2f} "
              f"{r.get('chi2_rsd',0):>6.2f} {r.get('delta_joint',0):>+6.2f} "
              f"{r.get('w0',0):>6.3f} {r.get('wa',0):>6.3f}")

    out = os.path.join(_THIS, 'l15_stage23_results.json')
    with open(out,'w') as f: json.dump(results, f, indent=2)
    print(f"\nSaved -> {out}")


if __name__ == '__main__':
    mp.freeze_support()
    main()
