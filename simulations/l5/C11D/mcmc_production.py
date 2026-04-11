# -*- coding: utf-8 -*-
"""
L5 Phase E/A: Production MCMC for C11D (pure-disformal IDE quintessence).

Uses Sakstein-Jain 2015 / Copeland-Liddle-Wands 1998 CLW background ODE.
Parameters: (Om, h, lam) where lam = exponential V(phi) slope.
48 walkers x 2000 steps, burn 500, thin 10, seed 42, R-hat target 1.02.
"""
from __future__ import annotations

import os
import sys
import json
import time

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')

import numpy as np

np.seterr(all='ignore')

import matplotlib
matplotlib.use('Agg')  # MUST precede corner/pyplot
import corner  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

_HERE = os.path.dirname(os.path.abspath(__file__))
_L5 = os.path.dirname(_HERE)
_SIMS = os.path.dirname(_L5)
_C11D_REEVAL = os.path.join(_L5, 'C11D_reeval')

for _p in (_SIMS, _L5, _C11D_REEVAL):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from l5.common import run_mcmc_production, jsonify  # noqa: E402
from l4.common import LCDM_CHI2, chi2_joint  # noqa: E402
from background import build_E as _build_E_c11d  # noqa: E402  (C11D_reeval)

_OMEGA_B = 0.02237

NAMES = ['Om', 'h', 'lam']
BOUNDS = [(0.28, 0.36), (0.64, 0.71), (0.0, 2.0)]

# Start near L5-E best-fit
X0 = [0.3093, 0.6778, 0.90]


def log_prob(x):
    Om, h, lam = x
    if not (BOUNDS[0][0] <= Om <= BOUNDS[0][1]):
        return -np.inf
    if not (BOUNDS[1][0] <= h <= BOUNDS[1][1]):
        return -np.inf
    if not (BOUNDS[2][0] <= lam <= BOUNDS[2][1]):
        return -np.inf
    omega_c = Om * h * h - _OMEGA_B
    if omega_c <= 0:
        return -np.inf
    try:
        E = _build_E_c11d((lam,), Om, h)
        if E is None:
            return -np.inf
        e_hi = float(E(1100.0))
        if not np.isfinite(e_hi) or e_hi < 1 or e_hi > 1e5:
            return -np.inf
        r = chi2_joint(E, rd=147.09, Omega_m=Om,
                       omega_b=_OMEGA_B, omega_c=omega_c, h=h,
                       H0_km=100.0 * h)
        tot = r['total']
        if tot is None or not np.isfinite(tot):
            return -np.inf
        return -0.5 * float(tot)
    except Exception:
        return -np.inf


def main():
    t0 = time.time()
    log = []

    def L(msg):
        print(msg, flush=True)
        log.append(msg)

    L('[L5-E C11D] Production MCMC start: 48x2000 burn=500 thin=10')
    L(f'[L5-E C11D] X0 = {X0}')

    nwalkers = 48
    nsteps = 2000
    nburn = 500
    thin = 10

    np.random.seed(42)
    out = run_mcmc_production(
        log_prob, X0, NAMES,
        nwalkers=nwalkers, nsteps=nsteps, nburn=nburn, thin=thin,
        seed=42, rhat_target=1.02, max_retries=2,
    )
    dt = time.time() - t0
    rhat_max = float(max(out['rhat']))
    samples = np.asarray(out['samples'])
    means = np.asarray(out['means'])

    lp_mean = log_prob(means.tolist())
    chi2_mean = -2.0 * lp_mean if np.isfinite(lp_mean) else float('nan')

    L(f'[L5-E C11D]   done in {dt/60:.1f} min  rhat_max={rhat_max:.4f}')
    L(f'[L5-E C11D]   chi2_mean={chi2_mean:.3f}  dchi2={chi2_mean-LCDM_CHI2:+.3f}')
    L(f'[L5-E C11D]   K13_pass={rhat_max < 1.02}')

    fig_dir = os.path.normpath(os.path.join(_SIMS, '..', 'paper', 'figures'))
    os.makedirs(fig_dir, exist_ok=True)
    fig_path = os.path.join(fig_dir, 'l5_C11D_corner.png')
    try:
        fig = corner.corner(samples, labels=NAMES,
                            quantiles=[0.16, 0.5, 0.84],
                            show_titles=True, title_fmt='.4f')
        fig.suptitle(f'L5 C11D Disformal IDE  Rhat_max={rhat_max:.3f}', fontsize=11)
        fig.savefig(fig_path, dpi=110, bbox_inches='tight')
        plt.close(fig)
        L(f'[L5-E C11D]   corner -> {fig_path}')
    except Exception as exc:
        L(f'[L5-E C11D]   corner FAILED: {exc}')

    max_rows = 2000
    if samples.shape[0] > max_rows:
        idx = np.linspace(0, samples.shape[0] - 1, max_rows).astype(int)
        samples_sub = samples[idx]
    else:
        samples_sub = samples

    result = {
        'ID': 'C11D',
        'family': 'Pure-disformal IDE quintessence (Sakstein-Jain / CLW 1998)',
        'names': NAMES,
        'bounds': BOUNDS,
        'means': out['means'],
        'stds': out['stds'],
        'rhat': out['rhat'],
        'rhat_max': rhat_max,
        'passes_K13': bool(rhat_max < 1.02),
        'nwalkers': nwalkers,
        'nsteps': nsteps,
        'nburn': nburn,
        'steps_final': out['steps_final'],
        'thin': thin,
        'seed': 42,
        'budget_reduced': False,
        'wall_time_sec': float(dt),
        'chi2_at_mean': float(chi2_mean),
        'delta_chi2_vs_lcdm': float(chi2_mean - LCDM_CHI2),
        'lcdm_chi2': float(LCDM_CHI2),
        'samples_shape': list(samples.shape),
        'samples': samples_sub.tolist(),
        'corner_path': fig_path,
        'log': log,
    }
    out_path = os.path.join(_HERE, 'mcmc_production.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(jsonify(result), f, indent=2)
    L(f'[L5-E C11D]   wrote {out_path}')
    return result


if __name__ == '__main__':
    main()
