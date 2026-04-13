# -*- coding: utf-8 -*-
"""
L15 Stage-5: MCMC posteriors for all 5 Stage-3 survivors.
9 parallel: each model runs in its own process (1 core each).

Settings: nwalkers=24, burn=400, prod=600 → 14400 calls/model.
logp = -0.5 * chi2_joint (BAO+SN+CMB+RSD).
CLAUDE.md: np.random.seed inside run_mcmc for reproducibility.
"""
import os, json, sys, time
import numpy as np
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

NWALKERS = 32
N_BURN   = 500
N_PROD   = 800


def _E_LCDM(Om, z_arr):
    return np.sqrt(OMEGA_R*(1+z_arr)**4 + Om*(1+z_arr)**3 + (1-Om-OMEGA_R))


# ── model definitions ─────────────────────────────────────────────────────────

def make_TF3(p):
    Om=p[0]; A=p[1]; B=max(p[2], 0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0<0.01: return None
    E=_E_LCDM(Om,Z_ARR); x=E-1.0
    return OL0*(1.0+A*x*np.exp(-B*x**3))

def make_AX3(p):
    Om=p[0]; A=p[1]; B=max(p[2], 0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0<0.01: return None
    theta=B*(Om*(1+Z_ARR)**3-Om)/max(OL0,1e-10)
    return OL0*(1.0+A*(1.0-np.cos(np.minimum(theta,20))))

def make_HB3(p):
    Om=p[0]; A=p[1]; B=max(p[2], 0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0<0.01: return None
    x_z=Om*(1+Z_ARR)**3; x_0=Om
    return OL0*(1.0+A*(x_z**2/(B**2+x_z**2)**2 - x_0**2/(B**2+x_0**2)**2))

def make_ST1(p):
    Om=p[0]; A=max(p[1],0.0); B=max(p[2],0.001)
    OL0=1.0-Om-OMEGA_R
    if OL0<0.01: return None
    x_z=(1+Z_ARR)**3-1.0
    return OL0*np.exp(-A*x_z)*(1.0+B*(1+Z_ARR)**3)/(1.0+B)

def make_EE2(p):
    Om=p[0]; A=p[1]; B=max(p[2], 0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0<0.01: return None
    E=_E_LCDM(Om,Z_ARR)
    theta=B*np.log(np.maximum(E,1e-10))
    return OL0*(1.0+A*(1.0-np.cos(np.minimum(theta,20))))


# prior bounds: [Om, A, log(B)]  — B sampled in log space for better mixing
import math
PRIORS = {
    #                    Om              A             log(B)
    'TF3-FermiLiquid': [(0.28,0.36), (-2.0, 5.0),  (math.log(0.01), math.log(50.0))],
    'AX3-AxionPot':    [(0.28,0.36), ( 0.0, 1.0),   (math.log(0.01), math.log(30.0))],
    'HB3-Lorentzian':  [(0.28,0.36), ( 0.0,30.0),   (math.log(0.01), math.log(20.0))],
    'ST1-StringWind':  [(0.28,0.36), ( 0.0, 1.0),   (math.log(0.001),math.log(5.0))],
    'EE2-CosLog':      [(0.28,0.36), ( 0.0, 1.0),   (math.log(0.01), math.log(50.0))],
}
# Note: walker parameter p = [Om, A, logB]; actual B = exp(logB)

MAKE_FNS = {
    'TF3-FermiLiquid': make_TF3,
    'AX3-AxionPot':    make_AX3,
    'HB3-Lorentzian':  make_HB3,
    'ST1-StringWind':  make_ST1,
    'EE2-CosLog':      make_EE2,
}


def make_E_func(make_fn, p):
    from scipy.interpolate import interp1d
    arr = make_fn(p)
    if arr is None: return None
    Om=float(np.clip(p[0],0.28,0.36))
    E2=OMEGA_R*(1+Z_ARR)**4+Om*(1+Z_ARR)**3+np.maximum(arr,0)
    Ea=np.sqrt(np.maximum(E2,1e-15))
    ei=interp1d(Z_ARR,Ea,kind='cubic',fill_value='extrapolate',bounds_error=False)
    return lambda z: float(ei(z))


# ── per-model MCMC worker ─────────────────────────────────────────────────────

def run_mcmc(args):
    label, p_best, seed = args
    import warnings; warnings.filterwarnings('ignore')
    import emcee
    from l3.data_loader import chi2_joint, get_data
    get_data()

    make_fn = MAKE_FNS[label]
    bounds  = PRIORS[label]
    ndim    = 3
    h       = H0_H; omega_b = OMEGA_B

    # p_best from Stage-3 is in [Om, A, B]; convert B→logB for sampling
    import math as _math
    p_init = [p_best[0], p_best[1], _math.log(max(p_best[2], 1e-4))]

    def log_prior(q):
        for i,(lo,hi) in enumerate(bounds):
            if not (lo < q[i] < hi): return -np.inf
        return 0.0

    def log_prob(q):
        lp = log_prior(q)
        if not np.isfinite(lp): return -np.inf
        Om  = float(np.clip(q[0], 0.28, 0.36))
        A   = float(q[1])
        B   = float(np.exp(q[2]))   # back-transform
        omega_c = Om*h**2 - omega_b
        if omega_c <= 0.01: return -np.inf
        E_func = make_E_func(make_fn, [Om, A, B])
        if E_func is None: return -np.inf
        try:
            res = chi2_joint(E_func, rd=RS_DRAG, Omega_m=Om,
                             omega_b=omega_b, omega_c=omega_c,
                             h=h, H0_km=H0_KMS)
            v = res['total']
            return -0.5*v if np.isfinite(v) else -np.inf
        except Exception:
            return -np.inf

    # initialise walkers tightly around best-fit in log(B) space
    np.random.seed(seed)
    scale = np.array([0.003, abs(p_init[1])*0.05+0.005, 0.05])
    p0 = np.array(p_init) + scale * np.random.randn(NWALKERS, ndim)
    for i,(lo,hi) in enumerate(bounds):
        p0[:,i] = np.clip(p0[:,i], lo+1e-4, hi-1e-4)

    # reduced stretch scale for better acceptance in tight posteriors
    sampler = emcee.EnsembleSampler(NWALKERS, ndim, log_prob,
                                    moves=emcee.moves.StretchMove(a=1.5))

    # burn-in
    np.random.seed(seed+1)
    state = sampler.run_mcmc(p0, N_BURN, progress=False)
    sampler.reset()

    # production
    np.random.seed(seed+2)
    sampler.run_mcmc(state, N_PROD, progress=False)

    flat = sampler.get_chain(flat=True)  # (N_PROD*NWALKERS, ndim)
    acc  = float(np.mean(sampler.acceptance_fraction))

    # back-transform logB → B for reporting
    flat_phys = flat.copy()
    flat_phys[:,2] = np.exp(flat[:,2])

    # posterior stats for Om, A, B (in physical space)
    stats = {}
    names = ['Om','A','B']
    for i,name in enumerate(names):
        chain = flat_phys[:,i]
        stats[name] = {
            'mean': round(float(np.mean(chain)),4),
            'std':  round(float(np.std(chain)),4),
            'lo68': round(float(np.percentile(chain,16)),4),
            'hi68': round(float(np.percentile(chain,84)),4),
        }

    # best posterior logp → MAP in physical space
    log_probs = sampler.get_log_prob(flat=True)
    best_idx  = np.argmax(log_probs)
    q_map     = flat[best_idx]
    p_map     = [q_map[0], q_map[1], float(np.exp(q_map[2]))]  # [Om, A, B]
    chi2_map  = -2.0*log_probs[best_idx]

    # CPL at MAP
    from scipy.optimize import curve_fit
    from scipy.interpolate import interp1d as itp
    arr_map = make_fn(p_map)
    w0_map = wa_map = float('nan')
    if arr_map is not None:
        z_fit=np.linspace(0.01,1.5,300); dz=1e-4
        ode_i=itp(Z_ARR,arr_map,kind='cubic',fill_value='extrapolate',bounds_error=False)
        u  =np.array([float(ode_i(z)) for z in z_fit])
        u_p=np.array([float(ode_i(z+dz)) for z in z_fit])
        u_m=np.array([float(ode_i(max(z-dz,1e-5))) for z in z_fit])
        dlnu=(u_p-u_m)/(2*dz*np.maximum(u,1e-20))
        w_z=(1+z_fit)*dlnu/3.0-1.0
        try:
            popt,_=curve_fit(lambda z,w0,wa:w0+wa*(1-1/(1+z)),
                             z_fit,w_z,p0=[-0.9,-0.3],
                             bounds=([-3.,-10.],[0.5,5.]),maxfev=5000)
            w0_map,wa_map=float(popt[0]),float(popt[1])
        except Exception:
            pass

    return label, {
        'acceptance': round(acc, 3),
        'n_samples':  int(len(flat)),
        'chi2_map':   round(chi2_map, 3),
        'w0_map':     round(w0_map, 3),
        'wa_map':     round(wa_map, 3),
        'p_map':      [round(float(x),5) for x in p_map],
        'posterior':  stats,
        'note':       'B sampled in log space; a=1.5 stretch',
    }


def main():
    s3_path = os.path.join(_THIS, 'l15_stage23_results.json')
    with open(s3_path) as f:
        s3 = json.load(f)
    lcdm_joint = s3['LCDM']['chi2_joint']

    tasks = []
    for label, make_fn in MAKE_FNS.items():
        if label not in s3: continue
        if s3[label].get('stage3') != 'PASS': continue
        p_best = s3[label]['p']
        tasks.append((label, p_best, hash(label) % 10000))

    print(f"L15 Stage-5: MCMC for {len(tasks)} models | "
          f"nwalkers={NWALKERS} burn={N_BURN} prod={N_PROD}")
    print(f"LCDM joint = {lcdm_joint:.2f}\n")

    t0 = time.time()
    ctx = mp.get_context('spawn')
    with ctx.Pool(processes=len(tasks)) as pool:
        results_list = pool.map(run_mcmc, tasks)
    elapsed = time.time()-t0
    print(f"Done in {elapsed/60:.1f} min.\n")

    results = {}
    print(f"{'Model':<22} {'acc':>5} {'chi2_MAP':>9} {'dchi2':>7} "
          f"{'w0_MAP':>7} {'wa_MAP':>7} | Om_mean±std  A_mean±std")
    print("-"*95)
    for label, r in results_list:
        results[label] = r
        dc = r['chi2_map'] - lcdm_joint
        om = r['posterior']['Om']
        a  = r['posterior']['A']
        print(f"{label:<22} {r['acceptance']:>5.3f} {r['chi2_map']:>9.2f} "
              f"{dc:>+7.2f} {r['w0_map']:>7.3f} {r['wa_map']:>7.3f} | "
              f"{om['mean']:.4f}±{om['std']:.4f}  {a['mean']:.4f}±{a['std']:.4f}")

    out = os.path.join(_THIS, 'l15_mcmc_results_v2.json')
    with open(out,'w') as f: json.dump(results, f, indent=2)
    print(f"\nSaved -> {out}")


if __name__ == '__main__':
    mp.freeze_support()
    main()
