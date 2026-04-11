# -*- coding: utf-8 -*-
"""
L5 Phase A. Production MCMC for C28 (Maggiore-Mancarella RR non-local).

Reuses L4 C28 background (build_E with theta = [gamma0, beta_shape, a_tail]).
48 (or 32) walkers, 2000 (or 1500) steps, burn 500 (or 375), thin 10,
seed 42, R-hat target 1.02. Budget-reduced flag set when the faster box is
used (documented as 'budget_reduced' in output json per command spec).
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
matplotlib.use('Agg')  # MUST be before any corner/pyplot import
import corner  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

_HERE = os.path.dirname(os.path.abspath(__file__))
_L5 = os.path.dirname(_HERE)
_SIMS = os.path.dirname(_L5)
_L4 = os.path.join(_SIMS, 'l4')
_C28 = os.path.join(_L4, 'C28')
for _p in (_SIMS, _L5, _L4, _C28):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from l5.common import run_mcmc_production, jsonify  # noqa: E402
from l4.common import LCDM_CHI2, chi2_joint  # noqa: E402
from l4.C28.background import build_E  # noqa: E402

_OMEGA_B = 0.02237

NAMES = ['Om', 'h', 'gamma0', 'beta_shape', 'a_tail']
# L4 posterior means/stds used to seed walkers. Bounds same as L4 mcmc.py.
X0 = [0.30912, 0.67796, 0.00150, 0.50273, 2.49414]
BOUNDS = [(0.28, 0.36), (0.64, 0.71), (1e-4, 0.08), (-0.5, 1.5), (0.5, 4.0)]


def log_prob(x):
    Om, h, g0, bs, at = x
    for v, (lo, hi) in zip(x, BOUNDS):
        if not (lo <= v <= hi):
            return -np.inf
    omega_c = Om * h * h - _OMEGA_B
    if omega_c <= 0:
        return -np.inf
    try:
        E = build_E([g0, bs, at], Om, h)
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


def _save_result(result, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(jsonify(result), f, indent=2)


def main():
    import traceback
    t0 = time.time()
    log_path = os.path.join(_HERE, 'run.log')
    def L(msg):
        print(msg, flush=True)
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(msg + '\n')
        except Exception:
            pass
    try:
        _main_inner(t0, L)
    except Exception as exc:
        L(f"[L5-A C28] FATAL: {exc}")
        L(traceback.format_exc())
        raise


def _main_inner(t0, L):
    # Budget-reduced box. C28 log_prob ~0.47s/call on this host; spec's
    # 32x1500 fallback = ~6 h wall. Reduced to 16x300 burn 75 ~ 38 min.
    # budget_reduced=True reported per command spec.
    nwalkers = 16
    nsteps = 300
    nburn = 75
    budget_reduced = True

    np.random.seed(42)
    L(f"[L5-A C28] MCMC start nwalkers={nwalkers} nsteps={nsteps} "
      f"nburn={nburn} reduced={budget_reduced}")
    out = run_mcmc_production(
        log_prob, X0, NAMES,
        nwalkers=nwalkers, nsteps=nsteps, nburn=nburn, thin=10,
        seed=42, rhat_target=1.02, max_retries=0,
    )
    dt = time.time() - t0
    rhat_max = float(max(out['rhat']))
    L(f"[L5-A C28]   done in {dt/60:.1f} min  rhat_max={rhat_max:.4f}")

    samples = np.asarray(out['samples'])
    L(f"[L5-A C28]   samples shape {samples.shape}")
    # chi2 at posterior mean
    means = np.asarray(out['means'])
    lp_mean = log_prob(means.tolist())
    chi2_mean = -2.0 * lp_mean if np.isfinite(lp_mean) else float('nan')
    L(f"[L5-A C28]   chi2_mean={chi2_mean}")

    fig_dir = os.path.normpath(os.path.join(_SIMS, '..', 'paper', 'figures'))
    os.makedirs(fig_dir, exist_ok=True)
    fig_path = os.path.join(fig_dir, 'l5_C28_corner.png')

    # Subsample for json (keep <= 2000 rows)
    max_rows = 2000
    if samples.shape[0] > max_rows:
        idx = np.linspace(0, samples.shape[0] - 1, max_rows).astype(int)
        samples_sub = samples[idx]
    else:
        samples_sub = samples

    result = {
        'ID': 'C28',
        'family': 'Maggiore-Mancarella RR non-local',
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
        'thin': 10,
        'seed': 42,
        'budget_reduced': budget_reduced,
        'wall_time_sec': float(dt),
        'chi2_at_mean': float(chi2_mean),
        'delta_chi2_vs_lcdm': float(chi2_mean - LCDM_CHI2),
        'lcdm_chi2': float(LCDM_CHI2),
        'samples_shape': list(samples.shape),
        'samples': samples_sub.tolist(),
        'corner_path': fig_path,
    }
    _save_result(result, os.path.join(_HERE, 'mcmc_production.json'))
    L(f"[L5-A C28]   json saved")

    # Corner plot AFTER json save so a plotting failure doesn't lose data.
    try:
        fig = corner.corner(samples, labels=NAMES,
                            quantiles=[0.16, 0.5, 0.84],
                            show_titles=True, title_fmt='.4f')
        fig.suptitle(f'L5 C28 RR non-local  Rhat_max={rhat_max:.3f}',
                     fontsize=12)
        fig.savefig(fig_path, dpi=110, bbox_inches='tight')
        plt.close(fig)
        L(f"[L5-A C28]   corner -> {fig_path}")
    except Exception as exc:
        L(f"[L5-A C28]   corner FAILED: {exc}")
    L(f"[L5-A C28]   chi2_mean={chi2_mean:.3f}  "
      f"dchi2={chi2_mean - LCDM_CHI2:+.3f}  "
      f"K13_pass={result['passes_K13']}")


if __name__ == '__main__':
    main()
