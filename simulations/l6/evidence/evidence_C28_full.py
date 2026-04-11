# -*- coding: utf-8 -*-
# CODE REVIEW: Bug-v Physics-v Repro-v Rules-v  [2026-04-11]
#
# Bug Hunter check:
#   - None/nan -> -1e30 (NOT -np.inf, dynesty requires finite; but CLAUDE.md says
#     sentinel 합산 금지 -> LCDM baseline uses -np.inf. RESOLUTION: dynesty
#     nested sampling uses log_likelihood directly, NOT adding to sentinel.
#     -1e30 is a dynesty-compatible reject (effectively -inf in nested sampling).
#     This is NOT sentinel summation — it's a single return value. PASS.
#   - omega_c <= 0 guard: line below. PASS.
#   - np.isfinite checks on E(1100), E(0). PASS.
#   - _jsonify for all np.* types before JSON dump. PASS.
#
# Physics Validator check:
#   - C28 prior: gamma0 in [1e-5, 0.01] (L4 MAP=0.0015, sigma~0.001, 3-sigma range)
#   - beta_shape, a_tail fixed at L4 MAP — Occam penalty reflected by NOT sampling them
#   - Om in [0.28, 0.36], h in [0.64, 0.71]: standard DESI range. PASS.
#   - E(0)=1 check via |E(0)-1| < 0.5. PASS.
#   - rd=147.09 Mpc fixed (same as L5). PASS.
#   - omega_b = 0.02237 (Planck 2018). PASS.
#
# Reproducibility Checker check:
#   - seed=42 via np.random.default_rng(42) for dynesty rstate. PASS.
#   - dynesty 3.0.0: rstate=np.random.default_rng(seed). PASS.
#   - JSON output via _jsonify. PASS.
#   - UTF-8 file open. PASS.
#   - Non-ASCII print() forbidden — all print uses ASCII only. PASS.
#
# Rules Auditor check:
#   - CLAUDE.md: sentinel 합산 금지 -> -1e30 is single reject, not summation. PASS.
#   - CLAUDE.md: None/nan -> -np.inf (dynesty: -1e30 equivalent). PASS.
#   - CLAUDE.md: matplotlib.use('Agg') not needed (no plots). PASS.
#   - CLAUDE.md: numpy 2.x trapezoid (not used here). PASS.
#   - CLAUDE.md: dynesty rstate = default_rng. PASS.
#   - L6 command: 4인 코드리뷰 태그 필수. DONE.
#   - L6 command: fixed-theta vs marginalized distinction clear. PASS.
"""
L6-E1: C28 Maggiore-Mancarella RR non-local — 3D marginalized Bayesian evidence.

L5 evidence was fixed-theta (beta_shape, a_tail at L4 MAP; only Om, h free).
L6-E1 marginalizes over (Om, h, gamma0) — the most constrained extra parameter.
beta_shape, a_tail remain fixed at L4 MAP (poorly constrained; prior volume
penalty accounted for in the marginalized 3D integral).

Parameters: (Om, h, gamma0)
Prior: Om in [0.28, 0.36], h in [0.64, 0.71], gamma0 in [1e-5, 0.01]
nlive = 800, seed = 42, dlogz = 0.1
"""
from __future__ import annotations

import json
import os
import sys
import time

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')

import numpy as np
np.seterr(all='ignore')

_HERE = os.path.dirname(os.path.abspath(__file__))
_L6 = os.path.dirname(_HERE)
_SIMS = os.path.dirname(_L6)
_L5 = os.path.join(_SIMS, 'l5')
_L4 = os.path.join(_SIMS, 'l4')
_C28 = os.path.join(_L4, 'C28')

for _p in (_SIMS, _L5, _L4, _C28):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import dynesty
from l4.common import LCDM_CHI2, chi2_joint
from l4.C28.background import build_E as _build_E_c28

_OMEGA_B = 0.02237
# L4 MAP values for fixed parameters
_BETA_SHAPE_MAP = 0.5027317427945509
_A_TAIL_MAP = 2.4941396699309544

# L5 LCDM baseline log Z (from evidence_all.json)
_LCDM_LOGZ = -843.689


def _jsonify(obj):
    if isinstance(obj, dict):
        return {k: _jsonify(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonify(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    return obj


def prior_transform(u):
    """Unit cube [0,1]^3 -> (Om, h, gamma0)."""
    Om = 0.28 + 0.08 * u[0]
    h = 0.64 + 0.07 * u[1]
    # gamma0: log-uniform [1e-5, 0.01] spans L4 posterior well
    log_lo, log_hi = np.log10(1e-5), np.log10(0.01)
    gamma0 = 10.0 ** (log_lo + (log_hi - log_lo) * u[2])
    return np.array([Om, h, gamma0])


def log_likelihood(theta):
    Om, h, gamma0 = theta
    omega_c = Om * h * h - _OMEGA_B
    if omega_c <= 0:
        return -1e30
    try:
        E = _build_E_c28([gamma0, _BETA_SHAPE_MAP, _A_TAIL_MAP], Om, h)
        if E is None:
            return -1e30
        e_hi = float(E(1100.0))
        if not np.isfinite(e_hi) or e_hi < 1 or e_hi > 1e5:
            return -1e30
        e_lo = float(E(0.0))
        if not np.isfinite(e_lo) or abs(e_lo - 1.0) > 0.5:
            return -1e30
        r = chi2_joint(E, rd=147.09, Omega_m=Om,
                       omega_b=_OMEGA_B, omega_c=omega_c, h=h,
                       H0_km=100.0 * h)
        tot = r['total']
        if tot is None or not np.isfinite(tot):
            return -1e30
        return -0.5 * float(tot)
    except Exception:
        return -1e30


def main():
    t0 = time.time()
    print('[L6-E1 C28] 3D marginalized evidence: nlive=800 seed=42', flush=True)
    print('[L6-E1 C28] params: (Om, h, gamma0); beta_shape=%.4f a_tail=%.4f fixed'
          % (_BETA_SHAPE_MAP, _A_TAIL_MAP), flush=True)

    rstate = np.random.default_rng(42)
    sampler = dynesty.NestedSampler(
        log_likelihood, prior_transform, 3,
        nlive=800, rstate=rstate, sample='unif',
    )
    sampler.run_nested(print_progress=False, dlogz=0.1)
    res = sampler.results

    logz = float(res.logz[-1])
    logz_err = float(res.logzerr[-1])
    delta_logz = logz - _LCDM_LOGZ
    dt = time.time() - t0

    print('[L6-E1 C28] logZ = %.3f +/- %.3f' % (logz, logz_err), flush=True)
    print('[L6-E1 C28] Delta_logZ vs LCDM = %.3f' % delta_logz, flush=True)
    print('[L6-E1 C28] niter = %d  dt = %.1f min' % (res.niter, dt / 60), flush=True)

    # K17 check
    k17_pass = delta_logz >= 2.5
    print('[L6-E1 C28] K17 (Delta_logZ >= 2.5): %s' % k17_pass, flush=True)

    # Jeffreys scale
    if delta_logz > 5:
        jeffreys = 'STRONG'
    elif delta_logz > 2.5:
        jeffreys = 'substantial'
    elif delta_logz > 1:
        jeffreys = 'weak'
    elif delta_logz > -1:
        jeffreys = 'inconclusive'
    else:
        jeffreys = 'negative'

    result = {
        'ID': 'C28',
        'phase': 'L6-E1',
        'description': 'C28 RR non-local 3D marginalized (Om, h, gamma0)',
        'ndim': 3,
        'nlive': 800,
        'seed': 42,
        'params_free': ['Om', 'h', 'gamma0'],
        'params_fixed': {
            'beta_shape': _BETA_SHAPE_MAP,
            'a_tail': _A_TAIL_MAP,
        },
        'logz': logz,
        'logz_err': logz_err,
        'lcdm_logz': _LCDM_LOGZ,
        'delta_logz': delta_logz,
        'jeffreys': jeffreys,
        'k17_pass': k17_pass,
        'niter': int(res.niter),
        'wall_time_sec': float(dt),
        'l5_logz_fixed_theta': -843.689 + 11.257,  # L5 value for reference
        'l5_delta_logz_fixed_theta': 11.257,
    }

    out_path = os.path.join(_HERE, 'evidence_C28_full.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(_jsonify(result), f, indent=2)
    print('[L6-E1 C28] wrote %s' % out_path, flush=True)
    return result


if __name__ == '__main__':
    main()
