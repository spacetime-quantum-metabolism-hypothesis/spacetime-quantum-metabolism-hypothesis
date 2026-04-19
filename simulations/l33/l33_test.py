# -*- coding: utf-8 -*-
"""
l33_test.py -- L33: 8-person team, no pre-assigned roles
=========================================================
8 team members each independently sample the full SQT-consistent
function space. After all proposals, duplicates are removed (discussion).
No roles pre-assigned — division of labor emerges naturally.

SQT-consistent rho_DE structure:
  rho_DE(z) = OL0 * (1 + amp * h(g(z)))
  g(z=0) = 0 for all base quantities
  amp from SQT-motivated fixed set (k=2 maintained)

LCDM baseline: chi2=10.192, AICc=15.392
"""

import os, sys, math, json, time, warnings, multiprocessing
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import minimize, differential_evolution

warnings.filterwarnings('ignore')
np.seterr(all='ignore')
os.environ['OMP_NUM_THREADS'] = os.environ['MKL_NUM_THREADS'] = os.environ['OPENBLAS_NUM_THREADS'] = '1'

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SIM_DIR    = os.path.dirname(_SCRIPT_DIR)
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

from desi_data import DESI_DR2, DESI_DR2_COV_INV

C_KMS     = 299792.458
R_S       = 147.09
OR        = 5.38e-5
N_DATA    = 13
N_GRID    = 4000
LCDM_CHI2 = 10.192
LCDM_AICC = 15.392

def aicc(chi2, k=2, n=N_DATA):
    return chi2 + 2*k + 2*k*(k+1)/(n-k-1)

# ─── SQT-motivated amplitude set ──────────────────────────────────────────────

AMP_SET = [0.5, 1.0/3.0, 1.0/math.pi, 1.0/math.e, 2.0/3.0, 0.25, 0.75, 0.1, 1.0, 0.4]

# ─── SQT building blocks (all g(0)=0, g>0 for z>0) ───────────────────────────

BASE_KEYS = ['ratio_m1', 'log_ratio', 'sqrt_m1', 'cbrt_m1', 'sq_m1', 'log2',
             'psi_dec', 'psi_sq_dec', 'two_comp_dec_cbrt', 'two_comp_dec_log',
             'log1p_psi_dec', 'prod_dec_cbrt', 'sinh_ratio', 'ratio_frac',
             'prod_dec_sqrt', 'tanh_ratio_sat']
TRANSFORMS = ['identity', 'tanh', 'arctan', 'rational', 'log1p', 'one_minus_exp', 'power',
              'sigmoid', 'erf_approx']
TR_PARAMS  = [0.3, 0.5, 0.7, 1.0, 1.5, 2.0]

# ─── E(z) factory (spawn-safe: all logic inline) ──────────────────────────────

def make_E_fn(base_key, transform, tr_param, amp_idx):
    """Build E(z_arr, Om) from SQT building blocks. All fixed, no fit params."""
    amp = AMP_SET[amp_idx % len(AMP_SET)]

    def E_fn(z_arr, Om):
        z_arr = np.asarray(z_arr, dtype=float)
        OL0   = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0:
            return None
        alpha = Om / OL0
        psi_z = 1.0 / (1.0 + alpha * (1.0 + z_arr)**3)
        psi0  = 1.0 / (1.0 + alpha)
        ratio = np.clip(psi0 / psi_z, 1.0, 200.0)

        # base g(z), g(0)=0
        if base_key == 'ratio_m1':
            g = ratio - 1.0
        elif base_key == 'log_ratio':
            g = np.log(ratio)
        elif base_key == 'sqrt_m1':
            g = np.sqrt(ratio) - 1.0
        elif base_key == 'cbrt_m1':
            g = ratio**(1.0/3.0) - 1.0
        elif base_key == 'sq_m1':
            g = ratio**2 - 1.0
        elif base_key == 'log2':
            lr = np.log(ratio)
            g  = lr**2
        else:
            g = ratio - 1.0

        p = max(tr_param, 0.01)
        if transform == 'identity':
            h = g
        elif transform == 'tanh':
            h = np.tanh(g / p)
        elif transform == 'arctan':
            h = (2.0/math.pi) * np.arctan(g / p)
        elif transform == 'rational':
            h = g / (1.0 + g / p)
        elif transform == 'log1p':
            h = np.log1p(np.clip(g, 0, None))
        elif transform == 'one_minus_exp':
            h = 1.0 - np.exp(-np.clip(g, 0, None) / p)
        elif transform == 'power':
            h = np.clip(g, 0, None)**p
        else:
            h = g

        rde = OL0 * (1.0 + amp * h)
        rde = np.where(rde < 0, 0.0, rde)
        E2  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
        if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
            return None
        return np.sqrt(np.maximum(E2, 1e-30))

    return E_fn

# ─── Team discussion: independent sampling + deduplication ────────────────────

def team_propose(n_members=8, proposals_each=6, seed=None):
    if seed is None:
        seed = int(time.time() * 1000) % (2**31)
    rng = np.random.default_rng(seed)

    all_specs = []
    for _ in range(n_members):
        for _ in range(proposals_each):
            bk  = str(rng.choice(BASE_KEYS))
            tr  = str(rng.choice(TRANSFORMS))
            trp = float(rng.choice(TR_PARAMS))
            ai  = int(rng.choice(len(AMP_SET)))
            all_specs.append((bk, tr, trp, ai))

    # Discussion: remove duplicates
    seen, unique = set(), []
    for spec in all_specs:
        bk, tr, trp, ai = spec
        key = (bk, tr, round(trp, 2), ai)
        if key not in seen:
            seen.add(key)
            unique.append(spec)

    return unique, seed

# ─── Worker (spawn-safe) ──────────────────────────────────────────────────────

def run_one(args):
    idx, spec, = args
    import os, sys, math, warnings
    import numpy as np
    from scipy.integrate import cumulative_trapezoid
    from scipy.optimize import minimize, differential_evolution

    os.environ['OMP_NUM_THREADS'] = os.environ['MKL_NUM_THREADS'] = os.environ['OPENBLAS_NUM_THREADS'] = '1'
    np.seterr(all='ignore')
    warnings.filterwarnings('ignore')

    _SD = os.path.dirname(os.path.abspath(__file__))
    _SI = os.path.dirname(_SD)
    if _SI not in sys.path:
        sys.path.insert(0, _SI)
    from desi_data import DESI_DR2, DESI_DR2_COV_INV

    C_KMS_W = 299792.458; R_S_W = 147.09; OR_W = 5.38e-5
    N_GRID_W = 4000; LCDM_AICC_W = 15.392
    AMP_SET_W = [0.5, 1.0/3.0, 1.0/math.pi, 1.0/math.e, 2.0/3.0, 0.25, 0.75, 0.1, 1.0, 0.4]

    bk, tr, trp, ai = spec
    amp = AMP_SET_W[ai % len(AMP_SET_W)]

    def E_fn(z_arr, Om):
        z_arr = np.asarray(z_arr, dtype=float)
        OL0 = 1.0 - Om - OR_W
        if OL0 <= 0 or Om <= 0:
            return None
        alpha = Om / OL0
        psi_z = 1.0 / (1.0 + alpha * (1.0 + z_arr)**3)
        psi0  = 1.0 / (1.0 + alpha)
        ratio = np.clip(psi0 / psi_z, 1.0, 200.0)

        psi_z = 1.0 / (1.0 + alpha * (1.0 + z_arr)**3)
        psi0  = 1.0 / (1.0 + alpha)
        psi_frac = psi_z / psi0  # decreases 1→0 with z

        if bk == 'ratio_m1':
            g = ratio - 1.0
        elif bk == 'log_ratio':
            g = np.log(ratio)
        elif bk == 'sqrt_m1':
            g = np.sqrt(ratio) - 1.0
        elif bk == 'cbrt_m1':
            g = ratio**(1.0/3.0) - 1.0
        elif bk == 'sq_m1':
            g = ratio**2 - 1.0
        elif bk == 'log2':
            g = np.log(ratio)**2
        elif bk == 'psi_dec':
            # 1 - psi_z/psi0: grows 0→1, saturates → wa<0 structure
            g = 1.0 - psi_frac
        elif bk == 'psi_sq_dec':
            # 1 - (psi_z/psi0)^2: faster saturation
            g = 1.0 - psi_frac**2
        elif bk == 'two_comp_dec_cbrt':
            # two-component: psi_dec (wa<0) + cbrt_m1 (low chi2)
            w1 = 0.6
            rde = OL0 * (1.0 + amp * (w1*(1.0-psi_frac) + (1.0-w1)*(ratio**(1.0/3.0)-1.0)))
            rde = np.where(rde < 0, 0.0, rde)
            E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
            if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                return None
            return np.sqrt(np.maximum(E2, 1e-30))
        elif bk == 'two_comp_dec_log':
            # two-component: psi_dec (wa<0) + log_ratio (moderate chi2)
            w1 = 0.5
            rde = OL0 * (1.0 + amp * (w1*(1.0-psi_frac) + (1.0-w1)*np.log(ratio)))
            rde = np.where(rde < 0, 0.0, rde)
            E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
            if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                return None
            return np.sqrt(np.maximum(E2, 1e-30))
        elif bk == 'log1p_psi_dec':
            # log(1 + psi_dec): grows 0→log(2)≈0.69, saturates naturally → wa<0
            g = np.log1p(1.0 - psi_frac)
        elif bk == 'prod_dec_cbrt':
            # psi_dec * cbrt_m1: product saturates due to psi_dec capping → wa<0
            g = (1.0 - psi_frac) * (ratio**(1.0/3.0) - 1.0)
        elif bk == 'sinh_ratio':
            # sinh(log_ratio) = (ratio - 1/ratio)/2: between ratio and ratio^2 growth
            lr = np.log(np.clip(ratio, 1e-8, 200))
            g = np.sinh(np.clip(lr, -10, 10))
        elif bk == 'ratio_frac':
            # (ratio-1)/(ratio+1): bounded [0,1), grows then saturates → wa<0
            g = (ratio - 1.0) / (ratio + 1.0)
        elif bk == 'prod_dec_sqrt':
            # psi_dec * sqrt_m1: product — saturates due to psi_dec
            g = (1.0 - psi_frac) * (np.sqrt(ratio) - 1.0)
        elif bk == 'tanh_ratio_sat':
            # tanh(log_ratio): direct saturation of log growth → strong wa<0
            g = np.tanh(np.log(np.clip(ratio, 1e-8, 200)))
        else:
            g = ratio - 1.0

        p = max(trp, 0.01)
        if tr == 'identity':
            h = g
        elif tr == 'tanh':
            h = np.tanh(g / p)
        elif tr == 'arctan':
            h = (2.0/math.pi) * np.arctan(g / p)
        elif tr == 'rational':
            h = g / (1.0 + np.abs(g) / p)
        elif tr == 'log1p':
            h = np.log1p(np.clip(g, 0, None))
        elif tr == 'one_minus_exp':
            h = 1.0 - np.exp(-np.clip(g, 0, None) / p)
        elif tr == 'power':
            h = np.clip(g, 0, None)**p
        elif tr == 'sigmoid':
            h = 1.0 / (1.0 + np.exp(-g/p)) - 0.5
        elif tr == 'erf_approx':
            h = np.tanh(g * 1.2533 / p)  # erf approximation
        else:
            h = g

        rde = OL0 * (1.0 + amp * h)
        rde = np.where(rde < 0, 0.0, rde)
        E2  = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
        if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
            return None
        return np.sqrt(np.maximum(E2, 1e-30))

    def compute_tv(Om, H0):
        z_eff = DESI_DR2['z_eff']
        z_grid = np.linspace(0.0, z_eff.max() + 0.01, N_GRID_W)
        Eg = E_fn(z_grid, Om)
        if Eg is None or not np.all(np.isfinite(Eg)):
            return None
        Eg = np.maximum(Eg, 1e-15)
        DM = (C_KMS_W/H0) * np.concatenate([[0.], cumulative_trapezoid(1./Eg, z_grid)])
        tv = np.empty(13)
        for i, (z, qty) in enumerate(zip(z_eff, DESI_DR2['quantity'])):
            idx_ = min(np.searchsorted(z_grid, z), N_GRID_W-1)
            DH = C_KMS_W / (H0 * Eg[idx_])
            DV = (z * DM[idx_]**2 * DH)**(1./3.) if z > 0 else 0.
            if 'DV' in qty:
                tv[i] = DV / R_S_W
            elif 'DM' in qty:
                tv[i] = DM[idx_] / R_S_W
            elif 'DH' in qty:
                tv[i] = DH / R_S_W
            else:
                tv[i] = np.nan
        return tv

    def chi2_w(params):
        Om, H0 = params
        if not (0.05 < Om < 0.70 and 50. < H0 < 100.):
            return 1e8
        tv = compute_tv(Om, H0)
        if tv is None or not np.all(np.isfinite(tv)):
            return 1e8
        d = DESI_DR2['value'] - tv
        return float(d @ DESI_DR2_COV_INV @ d)

    def cpl_wa_w(Om):
        z_arr = np.linspace(0.01, 2.0, 40)
        Ev = E_fn(z_arr, Om)
        if Ev is None or not np.all(np.isfinite(Ev)):
            return 0., 0.
        rde = Ev**2 - OR_W*(1+z_arr)**4 - Om*(1+z_arr)**3
        E0v = E_fn(np.array([0.0]), Om)
        if E0v is None:
            return 0., 0.
        rde0 = float(E0v[0]**2 - OR_W - Om)
        if rde0 <= 0 or np.any(rde <= 0):
            return 0., 0.
        lnrde = np.log(rde / rde0)
        ln1z  = np.log(1 + z_arr)
        A     = np.column_stack([-3.*ln1z, -3.*(ln1z - z_arr/(1+z_arr))])
        try:
            coef, *_ = np.linalg.lstsq(A, lnrde, rcond=None)
            return float(coef[0]) - 1., float(coef[1])
        except Exception:
            return 0., 0.

    try:
        bounds = [(0.20, 0.40), (62.0, 76.0)]
        rng_l  = np.random.default_rng(42)
        best_c, best_p = 1e9, None

        for Om0, H00 in zip(rng_l.uniform(0.20,0.40,20), rng_l.uniform(62,76,20)):
            try:
                r = minimize(chi2_w, [Om0, H00], method='Nelder-Mead',
                             options={'xatol':1e-6,'fatol':1e-6,'maxiter':5000})
                if r.fun < best_c:
                    best_c, best_p = r.fun, r.x
            except Exception:
                pass

        try:
            r = differential_evolution(chi2_w, bounds, popsize=30, maxiter=1000,
                                       tol=1e-7, seed=42, workers=1)
            if r.fun < best_c:
                best_c, best_p = r.fun, r.x
        except Exception:
            pass

        if best_p is None:
            return None

        Om, H0 = best_p
        chi2   = best_c
        ac     = chi2 + 2*2 + 2*2*3/(13-2-1)
        dac    = ac - LCDM_AICC_W
        w0, wa = cpl_wa_w(Om)

        if ac >= LCDM_AICC_W:
            status = 'K90'
        elif wa >= 0.0:
            status = 'K93'
        elif dac < -4.0 and wa < -0.5:
            status = 'Q92'
        elif dac < -2.0:
            status = 'Q91'
        else:
            status = 'Q90'

        return {
            'id': f'T{idx+1:02d}',
            'base': bk, 'transform': tr,
            'tr_param': round(trp, 3), 'amp_idx': ai,
            'amp': round(amp, 6),
            'name': f'{bk}|{tr}(p={trp:.1f})|amp={amp:.3f}',
            'k': 2,
            'chi2': round(chi2, 4), 'aicc': round(ac, 4),
            'd_aicc': round(dac, 4),
            'Om': round(Om, 4), 'H0': round(H0, 4),
            'w0': round(w0, 4), 'wa': round(wa, 4),
            'status': status
        }
    except Exception:
        return None

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    run_seed = int(time.time() * 1000) % (2**31)
    specs, used_seed = team_propose(n_members=8, proposals_each=6, seed=run_seed)

    print('='*70)
    print(f'L33: 8-person team | seed={used_seed} | {len(specs)} unique theories')
    print('='*70)
    print('No pre-assigned roles. Team independently sampled SQT space.')
    print(f'LCDM: chi2={LCDM_CHI2}, AICc={LCDM_AICC}')

    ctx  = multiprocessing.get_context('spawn')
    args = [(i, spec) for i, spec in enumerate(specs)]
    with ctx.Pool(9) as pool:
        raw = pool.map(run_one, args)

    results = sorted([r for r in raw if r], key=lambda x: x['aicc'])

    print('\n' + '='*115)
    print('RESULTS sorted by AICc:')
    print('='*115)
    print(f"{'ID':>5} {'name':<50} {'chi2':>8} {'AICc':>8} {'dAICc':>8} {'w0':>7} {'wa':>7} {'Status'}")
    print('-'*115)
    for r in results:
        print(f"{r['id']:>5} {r['name']:<50} {r['chi2']:>8.4f} {r['aicc']:>8.4f} {r['d_aicc']:>+8.4f} {r['w0']:>7.4f} {r['wa']:>7.4f}  {r['status']}")

    pass_l = [r for r in results if r['status'] in ('Q90','Q91','Q92')]
    q91_l  = [r for r in results if r['status'] in ('Q91','Q92')]
    q92_l  = [r for r in results if r['status'] == 'Q92']
    k93_l  = [r for r in results if r['status'] == 'K93']
    champ  = results[0] if results else None

    print(f'\nQ90 PASS : {len(pass_l)} / {len(results)}')
    print(f'Q91 STRONG: {len(q91_l)}')
    print(f'Q92 GAME  : {len(q92_l)}')
    print(f'K93 (wa>=0): {len(k93_l)}')
    if champ:
        print(f'Champion: {champ["id"]} dAICc={champ["d_aicc"]} w0={champ["w0"]} wa={champ["wa"]} Om={champ["Om"]} H0={champ["H0"]}')

    out = {
        'run': 'L33-8team-free',
        'seed': used_seed,
        'n_theories': len(results),
        'theories': results,
        'pass_count': len(pass_l),
        'q91': len(q91_l),
        'q92': len(q92_l),
        'k93_count': len(k93_l),
        'kill_count': len(results) - len(pass_l),
        'champion': champ,
        'lcdm': {'chi2': LCDM_CHI2, 'aicc': LCDM_AICC}
    }
    out_path = os.path.join(_SCRIPT_DIR, 'l33_results.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'\nResults saved: {out_path}')

if __name__ == '__main__':
    main()
