# -*- coding: utf-8 -*-
"""
L18 Phase 1: EE2 MCMC 정밀 posterior
omega_de = OL0*(1+A*(1-cos(B*ln(E))))
파라미터: (Om, A, log10B)
nwalkers=32, burn=800, prod=1200
CLAUDE.md 규칙: spawn pool, OMP=1, LCDM bridge
"""
import os, sys, json, time, warnings
import numpy as np
from scipy.interpolate import interp1d
import multiprocessing as mp

# matplotlib headless 설정은 import matplotlib 이전에
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
np.seterr(all='ignore')
warnings.filterwarnings('ignore')

_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_THIS))
_SIMS = os.path.join(_ROOT, 'simulations')
_L3   = os.path.join(_SIMS, 'l3')
for _p in (_SIMS, _L3, os.path.join(_SIMS, 'phase2')):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import emcee

# ── 상수 ────────────────────────────────────────────────────────────────────────
c_SI    = 2.998e8
Mpc_m   = 3.086e22
OMEGA_R = 9.1e-5
RS_DRAG = 147.09
H0_KMS  = 67.7
H0_SI   = H0_KMS * 1e3 / Mpc_m
H0_H    = H0_KMS / 100.0
OMEGA_B = 0.02237

N_Z   = 3000
Z_MAX = 6.0
Z_ARR = np.linspace(0.0, Z_MAX, N_Z)

# ── DESI DR2 ─────────────────────────────────────────────────────────────────
from desi_data import DESI_DR2, DESI_DR2_COV_INV
OBS_13  = DESI_DR2['value']
INV_COV = DESI_DR2_COV_INV
Z_13    = DESI_DR2['z_eff']
QTYPES  = DESI_DR2['quantity']


# ── E(z) 및 chi2_13pt ─────────────────────────────────────────────────────────
def _E_LCDM(Om, z_arr):
    OL0 = 1.0 - Om - OMEGA_R
    return np.sqrt(OMEGA_R*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0)


def make_EE2(Om, A, B):
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01: return None
    E   = _E_LCDM(Om, Z_ARR)
    lnE = B * np.log(np.maximum(E, 1e-10))
    return OL0 * (1.0 + A * (1.0 - np.cos(np.minimum(lnE, 20))))


def _build_E_interp(ode_arr, Om):
    E2  = OMEGA_R*(1+Z_ARR)**4 + Om*(1+Z_ARR)**3 + np.maximum(ode_arr, 0)
    Ea  = np.sqrt(np.maximum(E2, 1e-15))
    return interp1d(Z_ARR, Ea, kind='cubic', bounds_error=False,
                    fill_value=(float(Ea[0]), float(Ea[-1])))


def _chi_interp(E_interp):
    z_int = np.linspace(0, Z_MAX*0.99, 6000)
    inv_E = 1.0 / np.maximum(E_interp(z_int), 1e-10)
    dz    = np.diff(z_int)
    cum   = np.zeros(len(z_int))
    for i in range(1, len(z_int)):
        cum[i] = cum[i-1] + 0.5*(inv_E[i-1]+inv_E[i])*dz[i-1]
    return interp1d(z_int, cum, kind='cubic', bounds_error=False,
                    fill_value='extrapolate')


def chi2_13pt(ode_arr, Om):
    ei      = _build_E_interp(ode_arr, Om)
    chi_fn  = _chi_interp(ei)
    fac     = c_SI / (H0_SI * Mpc_m)
    pred    = np.zeros(13)
    for i, (z, qt) in enumerate(zip(Z_13, QTYPES)):
        DM = fac * chi_fn(z)
        DH = fac / ei(z)
        if qt == 'DV_over_rs':
            DV = (z * DM**2 * DH)**(1.0/3.0)
            pred[i] = DV / RS_DRAG
        elif qt == 'DM_over_rs':
            pred[i] = DM / RS_DRAG
        elif qt == 'DH_over_rs':
            pred[i] = DH / RS_DRAG
    if not np.all(np.isfinite(pred)): return 1e8
    resid = pred - OBS_13
    c2    = float(resid @ INV_COV @ resid)
    return c2 if np.isfinite(c2) and c2 < 1e8 else 1e8


# ── log-likelihood ────────────────────────────────────────────────────────────
# 파라미터 벡터: theta = [Om, A, log10B]
BOUNDS = [
    (0.25, 0.40),   # Om
    (0.0,  0.5),    # A
    (-1.0, 1.7),    # log10B: 0.1 ~ 50
]


def log_prior(theta):
    Om, A, lgB = theta
    lo, hi = zip(*BOUNDS)
    if not (lo[0] < Om < hi[0]): return -np.inf
    if not (lo[1] < A  < hi[1]): return -np.inf
    if not (lo[2] < lgB < hi[2]): return -np.inf
    return 0.0


def log_likelihood(theta):
    Om, A, lgB = theta
    B   = 10.0**lgB
    arr = make_EE2(Om, A, B)
    if arr is None: return -np.inf
    if np.any(arr < 0): return -np.inf
    c2 = chi2_13pt(arr, Om)
    if not np.isfinite(c2) or c2 >= 1e7: return -np.inf
    return -0.5 * c2


def log_prob(theta):
    lp = log_prior(theta)
    if not np.isfinite(lp): return -np.inf
    ll = log_likelihood(theta)
    if not np.isfinite(ll): return -np.inf
    return lp + ll


# ── MCMC ───────────────────────────────────────────────────────────────────────
def run_mcmc():
    ndim     = 3
    nwalkers = 32
    n_burn   = 800
    n_prod   = 1200

    # 시작점: L17 best-fit 근방
    p0_center = np.array([0.3055, 0.088, np.log10(8.76)])
    np.random.seed(42)
    p0 = p0_center + 1e-3 * np.random.randn(nwalkers, ndim)
    # 경계 클리핑
    for i in range(nwalkers):
        for j, (lo, hi) in enumerate(BOUNDS):
            p0[i, j] = np.clip(p0[i, j], lo + 1e-4, hi - 1e-4)

    print(f"MCMC EE2: nwalkers={nwalkers}, burn={n_burn}, prod={n_prod}")
    print(f"시작점: Om={p0_center[0]:.4f}, A={p0_center[1]:.4f}, B={10**p0_center[2]:.3f}")
    print()

    # burn-in
    t0 = time.time()
    np.random.seed(42)
    sampler = emcee.EnsembleSampler(nwalkers, ndim, log_prob)
    sampler.run_mcmc(p0, n_burn, progress=True)
    print(f"\nburnin 완료: {(time.time()-t0)/60:.1f}분")

    # 수용률 확인
    acc = sampler.acceptance_fraction
    print(f"수용률: mean={acc.mean():.3f}, min={acc.min():.3f}, max={acc.max():.3f}")

    # production
    p0_prod = sampler.get_last_sample().coords
    sampler.reset()
    np.random.seed(43)
    sampler.run_mcmc(p0_prod, n_prod, progress=True)
    print(f"\nproduction 완료: {(time.time()-t0)/60:.1f}분")

    # 결과 추출
    flat = sampler.get_chain(flat=True)  # (n_prod*nwalkers, 3)
    Om_s  = flat[:, 0]
    A_s   = flat[:, 1]
    B_s   = 10.0**flat[:, 2]
    lB_s  = flat[:, 2]

    def stats(arr):
        med = np.median(arr)
        lo  = med - np.percentile(arr, 16)
        hi  = np.percentile(arr, 84) - med
        return med, lo, hi

    Om_m, Om_l, Om_h = stats(Om_s)
    A_m,  A_l,  A_h  = stats(A_s)
    B_m,  B_l,  B_h  = stats(B_s)
    lB_m, lB_l, lB_h = stats(lB_s)

    print(f"\n[MCMC 결과]")
    print(f"Om  = {Om_m:.4f} +{Om_h:.4f} -{Om_l:.4f}")
    print(f"A   = {A_m:.4f}  +{A_h:.4f} -{A_l:.4f}")
    print(f"B   = {B_m:.3f}  +{B_h:.3f} -{B_l:.3f}")
    print(f"B/A = {B_m/A_m:.2f}")

    result = {
        'Om':  {'median': Om_m, 'lo': Om_l, 'hi': Om_h},
        'A':   {'median': A_m,  'lo': A_l,  'hi': A_h},
        'B':   {'median': B_m,  'lo': B_l,  'hi': B_h},
        'logB':{'median': lB_m, 'lo': lB_l, 'hi': lB_h},
        'B_over_A': B_m / A_m,
        'nwalkers': nwalkers, 'n_burn': n_burn, 'n_prod': n_prod,
        'acceptance_mean': float(acc.mean()),
    }

    # 저장
    out_json = os.path.join(_THIS, 'l18_mcmc_results.json')
    with open(out_json, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\nMCMC 결과 저장: {out_json}")

    # corner plot
    try:
        import corner
        labels = ['Om', 'A', 'log10(B)']
        fig = corner.corner(flat, labels=labels, quantiles=[0.16, 0.5, 0.84],
                            show_titles=True, title_kwargs={'fontsize': 10})
        fig.suptitle('EE2 MCMC Posterior (L18)', fontsize=12)
        out_fig = os.path.join(_THIS, 'l18_mcmc_corner.png')
        fig.savefig(out_fig, dpi=100, bbox_inches='tight')
        plt.close(fig)
        print(f"Corner plot 저장: {out_fig}")
    except ImportError:
        print("corner 패키지 없음. plot 생략.")

    # chain plot
    fig, axes = plt.subplots(3, 1, figsize=(10, 8))
    chain = sampler.get_chain()  # (n_prod, nwalkers, 3)
    for i, (ax, lab) in enumerate(zip(axes, ['Om', 'A', 'log10(B)'])):
        ax.plot(chain[:, :, i], alpha=0.3, lw=0.5)
        ax.set_ylabel(lab)
    axes[-1].set_xlabel('step')
    fig.suptitle('EE2 MCMC Chain (L18)')
    out_chain = os.path.join(_THIS, 'l18_mcmc_chain.png')
    fig.savefig(out_chain, dpi=80, bbox_inches='tight')
    plt.close(fig)
    print(f"Chain plot 저장: {out_chain}")

    return result


if __name__ == '__main__':
    run_mcmc()
