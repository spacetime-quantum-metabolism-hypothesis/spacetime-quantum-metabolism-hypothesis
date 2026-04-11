# -*- coding: utf-8 -*-
# CODE REVIEW: Bug-v Physics-v Repro-v Rules-v  [2026-04-11]
#
# Bug Hunter:
#   - -1e30 for dynesty reject (not sentinel summation). PASS.
#   - omega_c <= 0 guard. PASS.
#   - E(1100) and E(0) finite/range checks. PASS.
#   - _jsonify all np.* types. PASS.
#   - lam >= 0 enforced by prior [0, 2.0]. PASS.
#
# Physics Validator:
#   - C11D: pure disformal = minimally coupled quintessence background (CLW ODE).
#   - A'=0 -> background identical to CLW tracker. PASS.
#   - lam=0 -> w=-1 (LCDM limit). lam=0.888 best-fit. lam<sqrt(6)~2.449 for tracker.
#   - Prior lam in [0, 2.0] covers tracker regime. PASS.
#   - rd=147.09, omega_b=0.02237. PASS.
#
# Reproducibility:
#   - rstate = np.random.default_rng(42). PASS.
#   - dynesty 3.0.0 compliant. PASS.
#   - nlive=1000 (upgrade from L5 nlive=350). PASS.
#
# Rules Auditor:
#   - CLAUDE.md: pure disformal A'=0 = CLW background. PASS.
#   - CLAUDE.md: CLW ODE forward shooting from matter era. Checked in background.py.
#   - L6 command: nlive=1000 for C11D. PASS.
#   - L6 command: 4인 코드리뷰 태그 필수. DONE.
"""
L6-E2: C11D pure disformal IDE quintessence — 3D marginalized evidence, nlive=1000.

L5 used nlive=350 (budget). L6 uses nlive=1000 for better accuracy.
Parameters: (Om, h, lam) where lam = exponential V(phi) slope.
Prior: Om in [0.28, 0.36], h in [0.64, 0.71], lam in [0.0, 2.0].
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
_C11D_REEVAL = os.path.join(_L5, 'C11D_reeval')

for _p in (_SIMS, _L5, _L4, _C11D_REEVAL):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import dynesty
from l4.common import chi2_joint
from background import build_E as _build_E_c11d  # from C11D_reeval

_OMEGA_B = 0.02237
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
    """Unit cube [0,1]^3 -> (Om, h, lam)."""
    return np.array([
        0.28 + 0.08 * u[0],
        0.64 + 0.07 * u[1],
        0.0  + 2.0  * u[2],
    ])


def log_likelihood(theta):
    Om, h, lam = theta
    omega_c = Om * h * h - _OMEGA_B
    if omega_c <= 0:
        return -1e30
    try:
        E = _build_E_c11d((lam,), Om, h)
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
    print('[L6-E2 C11D] 3D marginalized evidence: nlive=1000 seed=42', flush=True)

    rstate = np.random.default_rng(42)
    sampler = dynesty.NestedSampler(
        log_likelihood, prior_transform, 3,
        nlive=1000, rstate=rstate, sample='unif',
    )
    sampler.run_nested(print_progress=False, dlogz=0.1)
    res = sampler.results

    logz = float(res.logz[-1])
    logz_err = float(res.logzerr[-1])
    delta_logz = logz - _LCDM_LOGZ
    dt = time.time() - t0

    print('[L6-E2 C11D] logZ = %.3f +/- %.3f' % (logz, logz_err), flush=True)
    print('[L6-E2 C11D] Delta_logZ vs LCDM = %.3f' % delta_logz, flush=True)
    print('[L6-E2 C11D] niter = %d  dt = %.1f min' % (res.niter, dt / 60), flush=True)

    k17_pass = delta_logz >= 2.5

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

    print('[L6-E2 C11D] K17 pass: %s  Jeffreys: %s' % (k17_pass, jeffreys), flush=True)

    result = {
        'ID': 'C11D',
        'phase': 'L6-E2',
        'description': 'C11D disformal quintessence 3D marginalized (Om, h, lam)',
        'ndim': 3,
        'nlive': 1000,
        'seed': 42,
        'params_free': ['Om', 'h', 'lam'],
        'logz': logz,
        'logz_err': logz_err,
        'lcdm_logz': _LCDM_LOGZ,
        'delta_logz': delta_logz,
        'jeffreys': jeffreys,
        'k17_pass': k17_pass,
        'niter': int(res.niter),
        'wall_time_sec': float(dt),
        'l5_delta_logz': 8.951,
    }

    out_path = os.path.join(_HERE, 'evidence_C11D_full.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(_jsonify(result), f, indent=2)
    print('[L6-E2 C11D] wrote %s' % out_path, flush=True)
    return result


if __name__ == '__main__':
    main()
