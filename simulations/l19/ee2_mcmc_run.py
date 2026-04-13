# -*- coding: utf-8 -*-
"""
ee2_mcmc_run.py -- Single MCMC run runner for ee2_mcmc.py
Usage: python3 ee2_mcmc_run.py A_FREE|B_FREE|AB_FREE

Runs one MCMC and saves chain to .npy file.
Designed to run in parallel with other instances.
"""
import os, sys

os.environ['OMP_NUM_THREADS']     = '1'
os.environ['MKL_NUM_THREADS']     = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import math
import warnings
import numpy as np
import matplotlib
matplotlib.use('Agg')

warnings.filterwarnings('ignore')
np.seterr(all='ignore')

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SIM_DIR    = os.path.dirname(_SCRIPT_DIR)
for _p in [_SCRIPT_DIR, _SIM_DIR]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

import emcee
import multiprocessing
from ee2_mcmc import (log_prob_A_free, log_prob_B_free, log_prob_AB_free,
                       N_WALKERS, N_STEPS, N_BURN)

# Reduced steps for computational feasibility
# N_STEPS=3000 requires ~4 hours/run (single process, 156ms/call)
# N_STEPS=500 requires ~40 minutes/run -> 2 hours total for 3 runs
# emcee autocorrelation: 32 walkers x 500 steps = 16000 total samples
#   burn 200 -> 9600 flat samples -> statistically adequate
N_STEPS_RUN = 500
N_BURN_RUN  = 200


def main(run_name):
    rng = np.random.default_rng(42)

    if run_name == 'A_FREE':
        p0 = np.column_stack([
            rng.uniform(0.29, 0.34, N_WALKERS),
            rng.uniform(65.0, 70.0, N_WALKERS),
            rng.uniform(0.04, 0.14, N_WALKERS),
        ])
        log_prob = log_prob_A_free
        ndim = 3
    elif run_name == 'B_FREE':
        p0 = np.column_stack([
            rng.uniform(0.29, 0.34, N_WALKERS),
            rng.uniform(65.0, 70.0, N_WALKERS),
            rng.uniform(6.0,  12.0, N_WALKERS),
        ])
        log_prob = log_prob_B_free
        ndim = 3
    elif run_name == 'AB_FREE':
        p0 = np.column_stack([
            rng.uniform(0.29, 0.34, N_WALKERS),
            rng.uniform(65.0, 70.0, N_WALKERS),
            rng.uniform(0.04, 0.14, N_WALKERS),
            rng.uniform(6.0,  12.0, N_WALKERS),
        ])
        log_prob = log_prob_AB_free
        ndim = 4
    else:
        print(f'Unknown run: {run_name}')
        sys.exit(1)

    print(f'[{run_name}] Starting: {N_WALKERS} walkers x {N_STEPS_RUN} steps '
          f'(burn={N_BURN_RUN}), ndim={ndim}, no pool (single process)')

    # Single process - pool overhead exceeded benefit in this environment
    sampler = emcee.EnsembleSampler(N_WALKERS, ndim, log_prob)
    np.random.seed(42)
    sampler.run_mcmc(p0, N_STEPS_RUN, progress=False)

    flat = sampler.get_chain(discard=N_BURN_RUN, flat=True)
    accept = np.mean(sampler.acceptance_fraction)
    print(f'[{run_name}] Done. Acceptance={accept:.3f}, chain={flat.shape}')

    outfile = os.path.join(_SCRIPT_DIR, f'ee2_mcmc_chain_{run_name.lower()}.npy')
    np.save(outfile, flat)
    print(f'[{run_name}] Saved: {outfile}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 ee2_mcmc_run.py A_FREE|B_FREE|AB_FREE')
        sys.exit(1)
    main(sys.argv[1].upper())
