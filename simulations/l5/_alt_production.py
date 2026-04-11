# -*- coding: utf-8 -*-
"""
L5 Phase B. Shared production MCMC helper for alt-20 hard-K2 candidates.

Each candidate (A01, A05, A12, A17) is a 2-D (Om, h) model using the closed
form from simulations/l4_alt/runner.py ALT dict. 48 walkers, 2000 steps,
burn 500, thin 10, seed 42, R-hat target 1.02.
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
_SIMS = os.path.dirname(_HERE)
_L4_ALT = os.path.join(_SIMS, 'l4_alt')
for _p in (_SIMS, _HERE, _L4_ALT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from l5.common import run_mcmc_production, jsonify  # noqa: E402
from l4.common import LCDM_CHI2, chi2_joint  # noqa: E402
from l4_alt.runner import ALT, _make_E  # noqa: E402

_OMEGA_B = 0.02237
NAMES = ['Om', 'h']
BOUNDS = [(0.28, 0.36), (0.64, 0.71)]


def make_log_prob(alt_id):
    name, f_ratio = ALT[alt_id]
    build_E = _make_E(f_ratio)

    def log_prob(x):
        Om, h = x
        if not (BOUNDS[0][0] <= Om <= BOUNDS[0][1]):
            return -np.inf
        if not (BOUNDS[1][0] <= h <= BOUNDS[1][1]):
            return -np.inf
        omega_c = Om * h * h - _OMEGA_B
        if omega_c <= 0:
            return -np.inf
        try:
            E = build_E([], Om, h)
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

    return name, log_prob


def run_alt(alt_id, out_dir):
    t0 = time.time()
    name, log_prob = make_log_prob(alt_id)
    # Seed near LCDM-ish point
    x0 = [0.315, 0.67]
    np.random.seed(42)
    print(f"[L5-B {alt_id}] {name}", flush=True)
    # Full production run: 48x2000 burn 500 thin 10 (K13 target).
    nwalkers = 48
    nsteps = 2000
    nburn = 500
    thin = 10
    out = run_mcmc_production(
        log_prob, x0, NAMES,
        nwalkers=nwalkers, nsteps=nsteps, nburn=nburn, thin=thin,
        seed=42, rhat_target=1.02, max_retries=0,
    )
    dt = time.time() - t0
    rhat_max = float(max(out['rhat']))
    samples = np.asarray(out['samples'])
    means = np.asarray(out['means'])
    lp_mean = log_prob(means.tolist())
    chi2_mean = -2.0 * lp_mean if np.isfinite(lp_mean) else float('nan')

    print(f"[L5-B {alt_id}]   dt={dt:.1f}s  rhat_max={rhat_max:.4f}  "
          f"chi2={chi2_mean:.3f}  dchi2={chi2_mean-LCDM_CHI2:+.3f}",
          flush=True)

    fig_dir = os.path.normpath(os.path.join(_SIMS, '..', 'paper', 'figures'))
    os.makedirs(fig_dir, exist_ok=True)
    fig_path = os.path.join(fig_dir, f'l5_{alt_id}_corner.png')
    try:
        fig = corner.corner(samples, labels=NAMES,
                            quantiles=[0.16, 0.5, 0.84],
                            show_titles=True, title_fmt='.4f')
        fig.suptitle(f'L5 {alt_id} {name}  Rhat_max={rhat_max:.3f}',
                     fontsize=11)
        fig.savefig(fig_path, dpi=110, bbox_inches='tight')
        plt.close(fig)
    except Exception as exc:
        print(f"[L5-B {alt_id}]   corner FAILED: {exc}", flush=True)

    max_rows = 2000
    if samples.shape[0] > max_rows:
        idx = np.linspace(0, samples.shape[0] - 1, max_rows).astype(int)
        samples_sub = samples[idx]
    else:
        samples_sub = samples

    result = {
        'ID': alt_id,
        'family': f'Alt-20 closed-form: {name}',
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
    }
    out_path = os.path.join(out_dir, 'mcmc_production.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(jsonify(result), f, indent=2)
    print(f"[L5-B {alt_id}]   wrote {out_path}", flush=True)
    return result
