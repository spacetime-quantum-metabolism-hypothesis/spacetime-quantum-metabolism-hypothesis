# -*- coding: utf-8 -*-
"""
l33_test.py -- L33: 8-person team, no pre-assigned roles
=========================================================
Each run: 8 team members each independently propose theories
from the full SQT-consistent function space (random exploration).
After all proposals, duplicates are removed via team discussion.
No roles are pre-assigned — division of labor emerges naturally.

SQT-consistent function space:
  Base quantities: psi_ratio = psi0/psi_z, Gamma = ratio-1, log(ratio), sqrt(ratio)-1
  Transforms: power, tanh, arctan, rational, log1p, 1-exp(-x)
  Amplitudes: fixed SQT-motivated values (no fitting)

Normalization constraint: rho_DE(z=0) = OL0 (automatic via g(0)=0 structure)
  rho_DE(z) = OL0 * (1 + amp * h(g(z)))
  where g(z=0) = 0 for all base quantities

LCDM baseline: chi2=10.192, AICc=15.392
"""

import os, sys, math, json, time, warnings, multiprocessing, itertools
import numpy as np
from scipy.optimize import minimize, differential_evolution

warnings.filterwarnings('ignore')
np.seterr(all='ignore')
os.environ['OMP_NUM_THREADS'] = os.environ['MKL_NUM_THREADS'] = os.environ['OPENBLAS_NUM_THREADS'] = '1'

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SIM_DIR    = os.path.dirname(_SCRIPT_DIR)
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

from desi_data import DESI_DR2, DESI_DR2_COV, DESI_DR2_COV_INV

C_KMS     = 299792.458
R_S       = 147.09
OR        = 5.38e-5
N_DATA    = 13
LCDM_CHI2 = 10.192
LCDM_AICC = 15.392

def aicc(chi2, k=2, n=N_DATA):
    return chi2 + 2*k + 2*k*(k+1)/(n-k-1)

# ─── SQT core ─────────────────────────────────────────────────────────────────

def sqt_bases(z_arr, Om):
    """Return all SQT base g(z) quantities, all satisfy g(0)=0."""
    OL0   = max(1.0 - Om - OR, 1e-6)
    alpha = Om / OL0
    psi_z = 1.0 / (1.0 + alpha * (1.0 + z_arr)**3)
    psi0  = 1.0 / (1.0 + alpha)
    ratio = np.clip(psi0 / psi_z, 1.0, 100.0)  # >= 1, =1 at z=0

    bases = {
        'ratio_m1':   ratio - 1.0,                      # psi0/psi - 1
        'log_ratio':  np.log(ratio),                     # log(psi0/psi)
        'sqrt_m1':    np.sqrt(ratio) - 1.0,              # sqrt(psi0/psi) - 1
        'cbrt_m1':    ratio**(1.0/3.0) - 1.0,            # cbrt(psi0/psi) - 1
        'ratio2_m1':  ratio**2 - 1.0,                   # (psi0/psi)^2 - 1
        'log2_ratio': np.log(ratio)**2 * np.sign(np.log(ratio)),  # sign-preserving log^2
    }
    return bases, OL0

# ─── SQT-consistent transform vocabulary ──────────────────────────────────────
# All h(x) satisfy h(0)=0 and h(x)>0 for x>0

TRANSFORMS = ['identity', 'tanh', 'arctan', 'rational', 'log1p', 'one_minus_exp', 'power']

def apply_transform(x, tr, param):
    """Apply transform h to base quantity x. param is transform-specific."""
    x = np.asarray(x, dtype=float)
    if tr == 'identity':
        return x
    elif tr == 'tanh':
        return np.tanh(x / max(param, 0.01))
    elif tr == 'arctan':
        return (2.0/math.pi) * np.arctan(x / max(param, 0.01))
    elif tr == 'rational':
        return x / (1.0 + np.abs(x) / max(param, 0.01))
    elif tr == 'log1p':
        return np.log1p(np.clip(x, 0, None))
    elif tr == 'one_minus_exp':
        return 1.0 - np.exp(-np.clip(x, 0, None) / max(param, 0.01))
    elif tr == 'power':
        return np.sign(x) * np.abs(x)**param
    return x

# ─── SQT-motivated amplitude set (no free fitting) ────────────────────────────
# Derived from SQT physical scales; team members pick from this set.

def get_amp_set(Om):
    OL0 = max(1.0 - Om - OR, 1e-6)
    return [0.5, 1.0/3.0, 1.0/math.pi, 1.0/math.e,
            Om, OL0, Om/OL0, 1.0-Om, 2.0/3.0, 0.25]

# ─── Theory constructor ────────────────────────────────────────────────────────

def make_theory(base_key, transform, tr_param, amp_idx):
    """
    Build a rho_DE function from SQT building blocks.
    rho_DE(z) = OL0 * (1 + amp * h(g(z)))
    amp is chosen from SQT-motivated set at fit time (using Om).
    """
    def rho_de(z_arr, Om):
        bases, OL0 = sqt_bases(z_arr, Om)
        g = bases[base_key]
        h = apply_transform(g, transform, tr_param)
        amp_set = get_amp_set(Om)
        amp = amp_set[amp_idx % len(amp_set)]
        val = OL0 * (1.0 + amp * h)
        return np.where(val < 0, 0.0, val)
    return rho_de

# ─── Team discussion: propose and deduplicate ─────────────────────────────────

def team_propose(n_members=8, proposals_each=6, seed=None):
    """
    n_members team members each independently propose theories.
    No roles pre-assigned. Each member randomly samples the full space.
    After all propose, duplicates are removed (team discussion).
    Returns list of unique theory specs.
    """
    if seed is None:
        seed = int(time.time() * 1000) % (2**31)
    rng = np.random.default_rng(seed)

    base_keys  = list(sqt_bases(np.array([0.0, 1.0]), 0.30)[0].keys())
    transforms = TRANSFORMS
    tr_params  = [0.3, 0.5, 0.7, 1.0, 1.5, 2.0]
    amp_idxs   = list(range(10))

    all_specs = []
    for member in range(n_members):
        for _ in range(proposals_each):
            bk  = rng.choice(base_keys)
            tr  = rng.choice(transforms)
            trp = float(rng.choice(tr_params))
            ai  = int(rng.choice(amp_idxs))
            all_specs.append((bk, tr, trp, ai))

    # Team discussion: remove duplicates (same base+transform+amp)
    seen = set()
    unique = []
    for spec in all_specs:
        bk, tr, trp, ai = spec
        key = (bk, tr, round(trp, 2), ai)
        if key not in seen:
            seen.add(key)
            unique.append(spec)

    return unique, seed

# ─── E(z) and chi2 ────────────────────────────────────────────────────────────

def compute_DM(z, Om, H0, rho_de_fn, n=2000):
    zv = np.linspace(0.0, z, n)
    E2 = OR*(1+zv)**4 + Om*(1+zv)**3 + rho_de_fn(zv, Om)
    Ev = np.sqrt(np.where(E2 <= 0, 1e-30, E2))
    return C_KMS / H0 * np.trapz(1.0/Ev, zv)

def E_at(z_arr, Om, H0, rho_de_fn):
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_de_fn(z_arr, Om)
    return np.sqrt(np.where(E2 <= 0, 1e-30, E2))

def chi2_fn(params, rho_de_fn, data):
    Om, H0 = params
    if Om <= 0.01 or Om >= 0.99 or H0 <= 40 or H0 >= 100:
        return 1e9
    try:
        res = []
        for row in data:
            z, qty, meas = row['z'], row['qty'], row['meas']
            Ez = float(E_at(np.array([z]), Om, H0, rho_de_fn)[0])
            if Ez <= 0:
                return 1e9
            if qty == 'DV':
                DM = compute_DM(z, Om, H0, rho_de_fn)
                DH = C_KMS / (H0 * Ez)
                pred = (z * DM**2 * DH)**(1.0/3.0) / R_S
            elif qty == 'DM':
                pred = compute_DM(z, Om, H0, rho_de_fn) / R_S
            elif qty == 'DH':
                pred = (C_KMS / (H0 * Ez)) / R_S
            else:
                pred = 0.0
            res.append(pred - meas)
        rv = np.array(res)
        return float(rv @ DESI_DR2_COV_INV @ rv)
    except Exception:
        return 1e9

def parse_desi():
    return [{'z': pt[0], 'qty': pt[1], 'meas': pt[2], 'err': pt[3]}
            for pt in DESI_DR2]

def cpl_wa(Om, rho_de_fn):
    z_arr = np.linspace(0.01, 2.0, 60)
    Ev    = E_at(z_arr, Om, 70.0, rho_de_fn)
    rde   = Ev**2 - OR*(1+z_arr)**4 - Om*(1+z_arr)**3
    rde   = np.where(rde <= 0, 1e-30, rde)
    E0    = float(E_at(np.array([0.0]), Om, 70.0, rho_de_fn)[0])
    rde0  = max(E0**2 - OR - Om, 1e-30)
    lnr   = np.log(rde / rde0)
    ln1z  = np.log(1 + z_arr)
    A     = np.column_stack([-3.0*ln1z, -3.0*(ln1z - z_arr/(1+z_arr))])
    coef, *_ = np.linalg.lstsq(A, lnr, rcond=None)
    return float(coef[0]) - 1.0, float(coef[1])

def fit_theory(rho_de_fn, data):
    bounds = [(0.20, 0.40), (62.0, 76.0)]
    rng_loc = np.random.default_rng(42)
    best_chi2, best_p = 1e9, None
    for Om0, H00 in zip(rng_loc.uniform(0.20,0.40,20), rng_loc.uniform(62,76,20)):
        try:
            r = minimize(chi2_fn, [Om0, H00], args=(rho_de_fn, data),
                         method='Nelder-Mead',
                         options={'xatol':1e-6,'fatol':1e-6,'maxiter':5000})
            if r.fun < best_chi2:
                best_chi2, best_p = r.fun, r.x
        except Exception:
            pass
    try:
        r = differential_evolution(chi2_fn, bounds, args=(rho_de_fn, data),
                                   popsize=30, maxiter=1000, tol=1e-7,
                                   seed=42, workers=1)
        if r.fun < best_chi2:
            best_chi2, best_p = r.fun, r.x
    except Exception:
        pass
    return (best_p, best_chi2) if best_p is not None else None

# ─── Worker ───────────────────────────────────────────────────────────────────

def run_one(args):
    idx, spec, data = args
    bk, tr, trp, ai = spec
    try:
        rho_de_fn = make_theory(bk, tr, trp, ai)
        result = fit_theory(rho_de_fn, data)
        if result is None:
            return None
        (Om, H0), chi2 = result
        ac   = aicc(chi2)
        dac  = ac - LCDM_AICC
        w0, wa = cpl_wa(Om, rho_de_fn)

        if ac >= LCDM_AICC:
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
            'name': f'{bk}|{tr}(p={trp:.1f})|amp[{ai}]',
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
    data = parse_desi()

    print('='*70)
    print(f'L33: 8-person team | seed={used_seed} | {len(specs)} unique theories')
    print('='*70)
    print('No pre-assigned roles. Team independently sampled SQT space.')
    print(f'LCDM: chi2={LCDM_CHI2}, AICc={LCDM_AICC}')

    ctx  = multiprocessing.get_context('spawn')
    args = [(i, spec, data) for i, spec in enumerate(specs)]
    with ctx.Pool(9) as pool:
        raw = pool.map(run_one, args)

    results = sorted([r for r in raw if r], key=lambda x: x['aicc'])

    print('\n' + '='*110)
    print('RESULTS sorted by AICc:')
    print('='*110)
    print(f"{'ID':>5} {'name':<45} {'chi2':>8} {'AICc':>8} {'dAICc':>8} {'w0':>7} {'wa':>7} {'Status'}")
    print('-'*110)
    for r in results:
        print(f"{r['id']:>5} {r['name']:<45} {r['chi2']:>8.4f} {r['aicc']:>8.4f} {r['d_aicc']:>+8.4f} {r['w0']:>7.4f} {r['wa']:>7.4f}  {r['status']}")

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
