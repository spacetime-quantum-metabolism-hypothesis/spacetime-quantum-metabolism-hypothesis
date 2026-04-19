# -*- coding: utf-8 -*-
"""
l33_test.py -- L33: 8-person team random theory generation
===========================================================
Each run: 8 independent team members (A-H) each propose 4 theories
from their assigned physical direction. Theories are randomly sampled
within each member's SQT-consistent function space.
Total: 32 theories per run. Different theories each run.

Team directions:
  A: psi-power law family (varying exponent)
  B: log-entropy family (log of psi ratio)
  C: saturation family (bounded functions of psi ratio)
  D: linear hybrid family (weighted combinations of A/B/C)
  E: z-dependent coupling (coupling strength varies with z)
  F: exponential approach family
  G: fractional-power family (non-integer exponents)
  H: dual-channel family (psi + Gamma correction)

SQT core:
  psi*(z) = 1/(1+alpha*(1+z)^3), alpha=Om/OL0
  Gamma_norm(z) = (1+alpha)*(1+z)^3/(1+alpha*(1+z)^3) - 1
  psi0 = psi*(z=0) = 1/(1+alpha)

LCDM baseline: chi2=10.192, AICc=15.392 (k=2, n=13)
"""

import os, sys, math, json, time, warnings, multiprocessing
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

C_KMS  = 299792.458
R_S    = 147.09
OR     = 5.38e-5
N_DATA = 13
N_GRID = 4000
LCDM_CHI2 = 10.192
LCDM_AICC = 15.392

def aicc(chi2, k=2, n=N_DATA):
    return chi2 + 2*k + 2*k*(k+1)/(n-k-1)

# ─── SQT core quantities ──────────────────────────────────────────────────────

def sqt_psi(z_arr, Om):
    OL0   = max(1.0 - Om - OR, 1e-6)
    alpha = Om / OL0
    return 1.0 / (1.0 + alpha * (1.0 + z_arr)**3), alpha, OL0

def sqt_gamma(z_arr, Om):
    psi_z, alpha, OL0 = sqt_psi(z_arr, Om)
    psi0 = 1.0 / (1.0 + alpha)
    gamma = psi0 / psi_z - 1.0
    return gamma, psi_z, psi0, alpha, OL0

# ─── E(z) builder ─────────────────────────────────────────────────────────────

def build_E(rho_de_fn):
    """Return E(z_arr, Om) given a rho_DE(z_arr, Om) function."""
    def E_fn(z_arr, Om):
        rho_de = rho_de_fn(z_arr, Om)
        rho_de = np.where(rho_de < 0, 0.0, rho_de)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_de
        return np.sqrt(np.where(E2 <= 0, 1e-30, E2))
    return E_fn

# ─── CPL w0/wa extraction ─────────────────────────────────────────────────────

def cpl_wa(Om, E_fn):
    z_arr = np.linspace(0.01, 2.0, 60)
    Ev    = E_fn(z_arr, Om)
    rde   = Ev**2 - OR*(1+z_arr)**4 - Om*(1+z_arr)**3
    rde   = np.where(rde <= 0, 1e-30, rde)
    E0    = float(E_fn(np.array([0.0]), Om)[0])
    rde0  = max(E0**2 - OR - Om, 1e-30)
    ln_rde = np.log(rde / rde0)
    ln1z   = np.log(1 + z_arr)
    x_w0   = -3.0 * ln1z
    x_wa   = -3.0 * (ln1z - z_arr / (1 + z_arr))
    A      = np.column_stack([x_w0, x_wa])
    coef, _, _, _ = np.linalg.lstsq(A, ln_rde, rcond=None)
    return float(coef[0]) - 1.0, float(coef[1])

# ─── chi2 computation ─────────────────────────────────────────────────────────

def chi2_fn(params, E_fn, data):
    Om, H0 = params
    if Om <= 0.01 or Om >= 0.99 or H0 <= 40 or H0 >= 100:
        return 1e9
    res = []
    for row in data:
        z, qty, _ = row['z'], row['qty'], row['err']
        Ez = float(E_fn(np.array([z]), Om)[0])
        if qty == 'DV':
            Dv_th = (C_KMS*z / (H0*Ez) * (C_KMS / (H0*Ez) * z / (1+z)**2)**0.0)**(1/3)
            # proper DV = (z * DM^2 * DH)^(1/3) / rs
            # recompute properly
            DM = compute_DM(z, Om, H0, E_fn)
            DH = C_KMS / (H0 * Ez)
            DV = (z * DM**2 * DH)**(1/3)
            pred = DV / R_S
        elif qty == 'DM':
            DM = compute_DM(z, Om, H0, E_fn)
            pred = DM / R_S
        elif qty == 'DH':
            DH = C_KMS / (H0 * Ez)
            pred = DH / R_S
        else:
            pred = 0.0
        res.append(pred - row['meas'])
    res = np.array(res)
    return float(res @ DESI_DR2_COV_INV @ res)

def compute_DM(z, Om, H0, E_fn, n=2000):
    zv = np.linspace(0, z, n)
    Ev = E_fn(zv, Om)
    integrand = 1.0 / Ev
    DM = C_KMS / H0 * np.trapz(integrand, zv)
    return DM

def parse_desi():
    rows = []
    for pt in DESI_DR2:
        z   = pt[0]
        qty = pt[1]
        meas = pt[2]
        err  = pt[3]
        rows.append({'z': z, 'qty': qty, 'meas': meas, 'err': err})
    return rows

# ─── optimizer ────────────────────────────────────────────────────────────────

def fit_theory(E_fn, data, n_starts=20):
    bounds = [(0.20, 0.40), (62.0, 75.0)]
    best_chi2 = 1e9
    best_p    = None

    rng_loc = np.random.default_rng(42)
    Om_starts = rng_loc.uniform(0.20, 0.40, n_starts)
    H0_starts = rng_loc.uniform(62.0, 75.0, n_starts)

    for Om0, H00 in zip(Om_starts, H0_starts):
        try:
            res = minimize(chi2_fn, [Om0, H00], args=(E_fn, data),
                           method='Nelder-Mead',
                           options={'xatol':1e-6,'fatol':1e-6,'maxiter':5000})
            if res.fun < best_chi2:
                best_chi2 = res.fun
                best_p    = res.x
        except Exception:
            pass

    try:
        res_de = differential_evolution(chi2_fn, bounds, args=(E_fn, data),
                                        popsize=30, maxiter=1000, tol=1e-7,
                                        seed=42, workers=1)
        if res_de.fun < best_chi2:
            best_chi2 = res_de.fun
            best_p    = res_de.x
    except Exception:
        pass

    if best_p is None:
        return None
    if best_chi2 >= 0.01:
        for Om0, H00 in zip(rng_loc.uniform(0.20,0.40,50), rng_loc.uniform(62,75,50)):
            try:
                res = minimize(chi2_fn, [Om0,H00], args=(E_fn,data),
                               method='Nelder-Mead',
                               options={'xatol':1e-7,'fatol':1e-7,'maxiter':8000})
                if res.fun < best_chi2:
                    best_chi2 = res.fun
                    best_p    = res.x
            except Exception:
                pass
    return best_p, best_chi2

# ─── 8-person theory generator ───────────────────────────────────────────────

def generate_theories(seed=None):
    """
    Generate 32 theories (4 per team member A-H).
    Each call with different seed produces different theories.
    """
    if seed is None:
        seed = int(time.time() * 1000) % (2**31)
    rng = np.random.default_rng(seed)

    theories = []

    # ── Member A: psi-power law family ────────────────────────────────────────
    # ρ_DE = OL0 * ((psi0/psi)^beta * (1-w) + w)
    # beta in (0.1, 1.5), w in (0.3, 0.9)
    betas   = rng.uniform(0.10, 1.50, 4)
    weights = rng.uniform(0.30, 0.90, 4)
    for i, (b, w) in enumerate(zip(betas, weights)):
        _b, _w = float(b), float(w)
        def rho_de_A(z_arr, Om, b=_b, w=_w):
            _, psi_z, psi0, _, OL0 = sqt_gamma(z_arr, Om)
            ratio = np.clip(psi0/psi_z, 1e-6, 50)
            return OL0 * (ratio**b * (1-w) + w)
        theories.append({
            'id': f'A{i+1:02d}',
            'name': f'A: psi^beta b={_b:.3f} w={_w:.3f}',
            'rho_de': rho_de_A
        })

    # ── Member B: log-entropy family ──────────────────────────────────────────
    # ρ_DE = OL0 * (1 + amp * log(psi0/psi)^power)
    # amp in (0.05, 0.60), power in (0.5, 2.0)
    amps   = rng.uniform(0.05, 0.60, 4)
    powers = rng.uniform(0.50, 2.00, 4)
    for i, (a, p) in enumerate(zip(amps, powers)):
        _a, _p = float(a), float(p)
        def rho_de_B(z_arr, Om, a=_a, p=_p):
            _, psi_z, psi0, _, OL0 = sqt_gamma(z_arr, Om)
            ratio = np.clip(psi0/psi_z, 1e-8, 50)
            log_r = np.log(ratio)
            return OL0 * (1.0 + a * np.abs(log_r)**p * np.sign(log_r))
        theories.append({
            'id': f'B{i+1:02d}',
            'name': f'B: log^p a={_a:.3f} p={_p:.3f}',
            'rho_de': rho_de_B
        })

    # ── Member C: saturation family ───────────────────────────────────────────
    # ρ_DE = OL0 * (1 + amp * tanh(k*(psi0/psi - 1)))
    # amp in (0.1, 0.8), k in (0.3, 2.0)
    amps_c = rng.uniform(0.10, 0.80, 4)
    ks_c   = rng.uniform(0.30, 2.00, 4)
    for i, (a, k) in enumerate(zip(amps_c, ks_c)):
        _a, _k = float(a), float(k)
        def rho_de_C(z_arr, Om, a=_a, k=_k):
            _, psi_z, psi0, _, OL0 = sqt_gamma(z_arr, Om)
            x = np.clip(psi0/psi_z - 1.0, -10, 10)
            return OL0 * (1.0 + a * np.tanh(k * x))
        theories.append({
            'id': f'C{i+1:02d}',
            'name': f'C: tanh-sat a={_a:.3f} k={_k:.3f}',
            'rho_de': rho_de_C
        })

    # ── Member D: linear hybrid family ────────────────────────────────────────
    # ρ_DE = OL0 * (w1*(psi0/psi)^b1 + w2*log(psi0/psi)*a2 + (1-w1-w2))
    # ensure w1+w2 < 1
    for i in range(4):
        w1 = float(rng.uniform(0.10, 0.50))
        w2 = float(rng.uniform(0.05, 0.40))
        if w1 + w2 > 0.90:
            w2 = 0.90 - w1
        b1 = float(rng.uniform(0.20, 1.20))
        a2 = float(rng.uniform(0.10, 0.60))
        def rho_de_D(z_arr, Om, w1=w1, w2=w2, b1=b1, a2=a2):
            _, psi_z, psi0, _, OL0 = sqt_gamma(z_arr, Om)
            ratio = np.clip(psi0/psi_z, 1e-8, 50)
            log_r = np.log(ratio)
            part1 = w1 * ratio**b1
            part2 = w2 * a2 * log_r
            base  = 1.0 - w1 - w2
            return OL0 * (base + part1 + part2)
        theories.append({
            'id': f'D{i+1:02d}',
            'name': f'D: hybrid w1={w1:.2f} w2={w2:.2f} b={b1:.2f}',
            'rho_de': rho_de_D
        })

    # ── Member E: z-dependent coupling ────────────────────────────────────────
    # ρ_DE = OL0 * (1 + f(z) * (psi0/psi - 1))
    # f(z) = amp / (1 + (z/z0)^n)  --- decreasing coupling
    for i in range(4):
        amp = float(rng.uniform(0.10, 0.80))
        z0  = float(rng.uniform(0.30, 2.00))
        n   = float(rng.uniform(1.00, 4.00))
        def rho_de_E(z_arr, Om, amp=amp, z0=z0, n=n):
            _, psi_z, psi0, _, OL0 = sqt_gamma(z_arr, Om)
            fz   = amp / (1.0 + (z_arr / z0)**n)
            dev  = np.clip(psi0/psi_z - 1.0, -1, 20)
            return OL0 * (1.0 + fz * dev)
        theories.append({
            'id': f'E{i+1:02d}',
            'name': f'E: z-couple amp={amp:.3f} z0={z0:.3f} n={n:.2f}',
            'rho_de': rho_de_E
        })

    # ── Member F: exponential approach family ─────────────────────────────────
    # ρ_DE = OL0 * (1 - amp*exp(-k*(psi0/psi)) + amp*exp(-k))
    # ensures rho_DE(z=0) = OL0
    for i in range(4):
        amp = float(rng.uniform(0.20, 1.50))
        k   = float(rng.uniform(0.50, 3.00))
        def rho_de_F(z_arr, Om, amp=amp, k=k):
            _, psi_z, psi0, _, OL0 = sqt_gamma(z_arr, Om)
            ratio = np.clip(psi0/psi_z, 1e-6, 50)
            anchor = amp * np.exp(-k * 1.0)  # at z=0 ratio=1
            return OL0 * (1.0 - amp * np.exp(-k * ratio) + anchor)
        theories.append({
            'id': f'F{i+1:02d}',
            'name': f'F: exp-approach amp={amp:.3f} k={k:.3f}',
            'rho_de': rho_de_F
        })

    # ── Member G: fractional-power family ─────────────────────────────────────
    # ρ_DE = OL0 * ((1-w)*(psi0/psi)^(p/q) + w)
    # p/q is non-integer rational
    for i in range(4):
        p = float(rng.choice([1, 2, 3]))
        q = float(rng.choice([3, 4, 5, 7]))
        exp = p / q
        w   = float(rng.uniform(0.40, 0.85))
        def rho_de_G(z_arr, Om, exp=exp, w=w):
            _, psi_z, psi0, _, OL0 = sqt_gamma(z_arr, Om)
            ratio = np.clip(psi0/psi_z, 1e-6, 50)
            return OL0 * ((1-w) * ratio**exp + w)
        theories.append({
            'id': f'G{i+1:02d}',
            'name': f'G: frac-pow exp={exp:.4f} w={w:.3f}',
            'rho_de': rho_de_G
        })

    # ── Member H: dual-channel (psi-decrease + Gamma correction) ──────────────
    # ρ_DE = OL0 * (w_psi*(psi0/psi)^b + w_g*g(Gamma) + (1-w_psi-w_g))
    # g(Gamma) is a bounded correction: tanh(Gamma/sat) or arctan(Gamma)
    g_choices = ['tanh', 'arctan', 'sqrt', 'log1p']
    for i in range(4):
        w_psi = float(rng.uniform(0.20, 0.60))
        w_g   = float(rng.uniform(0.05, 0.30))
        if w_psi + w_g > 0.85:
            w_g = 0.85 - w_psi
        b     = float(rng.uniform(0.20, 1.00))
        sat   = float(rng.uniform(0.50, 3.00))
        gtype = g_choices[i % len(g_choices)]
        def rho_de_H(z_arr, Om, wp=w_psi, wg=w_g, b=b, sat=sat, gt=gtype):
            gm, psi_z, psi0, _, OL0 = sqt_gamma(z_arr, Om)
            ratio = np.clip(psi0/psi_z, 1e-6, 50)
            if gt == 'tanh':
                gc = np.tanh(gm / sat)
            elif gt == 'arctan':
                gc = (2/math.pi) * np.arctan(gm / sat)
            elif gt == 'sqrt':
                gc = np.sqrt(np.clip(gm / sat, 0, 10)) / np.sqrt(10) * 0.9
            else:  # log1p
                gc = np.log1p(gm / sat) / np.log1p(10.0 / sat)
            base = 1.0 - wp - wg
            return OL0 * (base + wp * ratio**b + wg * gc)
        theories.append({
            'id': f'H{i+1:02d}',
            'name': f'H: dual {gtype} wp={w_psi:.2f} b={b:.2f}',
            'rho_de': rho_de_H
        })

    return theories, seed

# ─── worker function ──────────────────────────────────────────────────────────

def run_one(args):
    theory, data = args
    try:
        E_fn = build_E(theory['rho_de'])
        result = fit_theory(E_fn, data)
        if result is None:
            return None
        (Om, H0), chi2 = result
        ac = aicc(chi2)
        d_ac = ac - LCDM_AICC
        w0, wa = cpl_wa(Om, E_fn)

        if ac >= LCDM_AICC:
            status = 'K90'
        elif wa >= 0.0:
            status = 'K93'
        elif d_ac < -4.0 and wa < -0.5:
            status = 'Q92'
        elif d_ac < -2.0:
            status = 'Q91'
        else:
            status = 'Q90'

        return {
            'id': theory['id'],
            'name': theory['name'],
            'k': 2,
            'chi2': round(chi2, 4),
            'aicc': round(ac, 4),
            'd_aicc': round(d_ac, 4),
            'Om': round(Om, 4),
            'H0': round(H0, 4),
            'w0': round(w0, 4),
            'wa': round(wa, 4),
            'status': status
        }
    except Exception as e:
        return None

# ─── main ─────────────────────────────────────────────────────────────────────

def main():
    run_seed = int(time.time() * 1000) % (2**31)
    theories, used_seed = generate_theories(run_seed)
    data = parse_desi()

    print('=' * 70)
    print(f'L33: 8-person team | seed={used_seed} | {len(theories)} theories')
    print('=' * 70)
    print('Teams: A(power) B(log) C(sat) D(hybrid) E(z-couple) F(exp) G(frac) H(dual)')
    print(f'LCDM: chi2={LCDM_CHI2}, AICc={LCDM_AICC}')
    print(f'Theories: {len(theories)}')

    ctx = multiprocessing.get_context('spawn')
    args = [(t, data) for t in theories]
    with ctx.Pool(9) as pool:
        raw_results = pool.map(run_one, args)

    results = [r for r in raw_results if r is not None]
    results.sort(key=lambda x: x['aicc'])

    print('\n' + '=' * 100)
    print('RESULTS sorted by AICc:')
    print('=' * 100)
    print(f"{'ID':>6} {'Theory':<45} {'chi2':>8} {'AICc':>8} {'dAICc':>8} {'w0':>7} {'wa':>7} {'Status'}")
    print('-' * 100)
    for r in results:
        print(f"{r['id']:>6} {r['name']:<45} {r['chi2']:>8.4f} {r['aicc']:>8.4f} {r['d_aicc']:>+8.4f} {r['w0']:>7.4f} {r['wa']:>7.4f} {r['status']:>8}")

    pass_list = [r for r in results if r['status'] in ('Q90','Q91','Q92')]
    q91_list  = [r for r in results if r['status'] in ('Q91','Q92')]
    q92_list  = [r for r in results if r['status'] == 'Q92']
    k93_list  = [r for r in results if r['status'] == 'K93']

    champ = results[0] if results else None

    print(f'\nQ90 PASS : {len(pass_list)} / {len(results)} | KILL: {len(results)-len(pass_list)}')
    print(f'Q91 STRONG: {len(q91_list)}')
    print(f'Q92 GAME  : {len(q92_list)}')
    print(f'K93 (wa>=0): {len(k93_list)}')
    if champ:
        print(f'Champion: {champ["id"]} dAICc={champ["d_aicc"]} chi2={champ["chi2"]} w0={champ["w0"]} wa={champ["wa"]} Om={champ["Om"]} H0={champ["H0"]}')

    out = {
        'run': 'L33-8team',
        'seed': used_seed,
        'theories': results,
        'pass_count': len(pass_list),
        'q91': len(q91_list),
        'q92': len(q92_list),
        'k93_count': len(k93_list),
        'kill_count': len(results) - len(pass_list),
        'champion': champ,
        'lcdm': {'chi2': LCDM_CHI2, 'aicc': LCDM_AICC}
    }

    out_path = os.path.join(_SCRIPT_DIR, 'l33_results.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'\nResults saved: {out_path}')

if __name__ == '__main__':
    main()
