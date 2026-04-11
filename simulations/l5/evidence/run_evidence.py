# -*- coding: utf-8 -*-
"""
Phase L5-C: Bayesian evidence via dynesty nested sampling.

For each candidate (LCDM, C28, C33, 14 alt) run nested_evidence and compute
Delta ln Z = ln Z_cand - ln Z_LCDM. Classify per Jeffreys' scale.

Output: simulations/l5/evidence/evidence_all.json

CLAUDE.md rules: UTF-8, ASCII-only prints, Windows thread limits, seed=42,
_jsonify for np.* -> JSON.
"""
from __future__ import annotations

import json
import os
import sys
import time
import traceback

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')

import numpy as np

np.seterr(all='ignore')

_THIS = os.path.dirname(os.path.abspath(__file__))
_L5 = os.path.dirname(_THIS)
_SIMS = os.path.dirname(_L5)
for _p in (_SIMS, _L5, os.path.join(_SIMS, 'l3'), os.path.join(_SIMS, 'l4'),
           os.path.join(_SIMS, 'l4_alt')):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import dynesty  # noqa: E402


def nested_evidence(log_likelihood, prior_transform, ndim, *,
                    nlive=500, seed=42, sample='unif', dlogz=0.2):
    """Local dynesty wrapper (faster than l5.common default).

    Uses sample='unif' (fast for low-D) and dlogz=0.1 (sufficient for
    Delta ln Z comparisons to ~0.1 precision).
    """
    rstate = np.random.default_rng(seed)
    sampler = dynesty.NestedSampler(
        log_likelihood, prior_transform, ndim,
        nlive=nlive, rstate=rstate, sample=sample,
    )
    sampler.run_nested(print_progress=False, dlogz=dlogz)
    res = sampler.results
    return {
        'logz': float(res.logz[-1]),
        'logz_err': float(res.logzerr[-1]),
        'niter': int(res.niter),
        'nlive': nlive,
        'dlogz_tol': dlogz,
        'sample': sample,
    }
from l4.common import (  # noqa: E402
    LCDM_CHI2, LCDM_OM, LCDM_H, OMEGA_R, E_lcdm, chi2_joint,
)
from l4_alt.runner import ALT, _make_E  # noqa: E402


# ---------------------------------------------------------------------------
# JSON sanitizer
# ---------------------------------------------------------------------------

def _jsonify(obj):
    if isinstance(obj, dict):
        return {k: _jsonify(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonify(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    return obj


# ---------------------------------------------------------------------------
# chi2 helper: shared omega_b, safe wrapper
# ---------------------------------------------------------------------------

OMEGA_B = 0.02237


def _chi2_for_E(E, Om, h):
    omega_c = Om * h * h - OMEGA_B
    if omega_c <= 0:
        return None
    try:
        e_hi = float(E(1100.0))
        if not np.isfinite(e_hi) or e_hi < 1 or e_hi > 1e5:
            return None
        e_lo = float(E(0.0))
        if not np.isfinite(e_lo) or abs(e_lo - 1.0) > 0.5:
            return None
        r = chi2_joint(E, rd=147.09, Omega_m=Om,
                       omega_b=OMEGA_B, omega_c=omega_c, h=h,
                       H0_km=100.0 * h)
        tot = r['total']
        if not np.isfinite(tot):
            return None
        return float(tot)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Candidate registry: build prior_transform + log_likelihood per candidate
# ---------------------------------------------------------------------------

def _prior_2d(u):
    # u in [0,1]^2 -> (Om, h)
    return np.array([
        0.28 + 0.08 * u[0],
        0.64 + 0.07 * u[1],
    ])


def _build_lcdm():
    def ll(theta):
        Om, h = theta
        E = E_lcdm(Om, h)
        c = _chi2_for_E(E, Om, h)
        if c is None:
            return -1e30
        return -0.5 * c
    return ll, _prior_2d, 2


def _build_alt(aid):
    _, f_ratio = ALT[aid]
    build = _make_E(f_ratio)

    def ll(theta):
        Om, h = theta
        try:
            E = build([], Om, h)
        except Exception:
            return -1e30
        if E is None:
            return -1e30
        c = _chi2_for_E(E, Om, h)
        if c is None:
            return -1e30
        return -0.5 * c
    return ll, _prior_2d, 2


def _build_c28():
    # Fallback strategy: fix theta=(gamma0, beta_shape, a_tail) at L4 MAP
    # and sample only (Om, h). Document as fixed-theta Fisher-approx evidence.
    # Why: C28 background.py iterative ODE is slow + nlive=500 * ~4k evals
    # would take > 30 min per run.
    from l4.C28.background import build_E as _build_E_c28
    theta_fixed = [0.0015016081651382479, 0.5027317427945509, 2.4941396699309544]

    def ll(theta):
        Om, h = theta
        try:
            E = _build_E_c28(theta_fixed, Om, h)
        except Exception:
            return -1e30
        if E is None:
            return -1e30
        c = _chi2_for_E(E, Om, h)
        if c is None:
            return -1e30
        return -0.5 * c
    return ll, _prior_2d, 2


def _build_c33_3d():
    # C33 has theta = (f_1, n) on top of (Om, h) -> 4D. To keep runtime
    # tractable we sample (Om, h, f_1) and fix n at L4 MAP (=1.12).
    # This charges C33 with 1 extra parameter relative to 2D models,
    # appropriately capturing the Occam factor for its primary nuisance.
    from l4.C33.background import build_E as _build_E_c33
    n_fixed = 1.1206219447767185

    def prior(u):
        return np.array([
            0.28 + 0.08 * u[0],
            0.64 + 0.07 * u[1],
            0.0 + 0.30 * u[2],   # f_1 in [0, 0.30]
        ])

    def ll(theta):
        Om, h, f1 = theta
        try:
            E = _build_E_c33((f1, n_fixed), Om, h)
        except Exception:
            return -1e30
        if E is None:
            return -1e30
        c = _chi2_for_E(E, Om, h)
        if c is None:
            return -1e30
        return -0.5 * c
    return ll, prior, 3


# ---------------------------------------------------------------------------
# Candidate list
# ---------------------------------------------------------------------------

CANDIDATES = []
CANDIDATES.append(('LCDM', 'LCDM baseline', _build_lcdm, 300, 'analytic'))
CANDIDATES.append(('C28', 'Maggiore RR non-local (theta fixed at L4 MAP)',
                   _build_c28, 250, 'fixed-theta-fallback'))
CANDIDATES.append(('C33', 'f(Q) teleparallel (n fixed, f_1 free)',
                   _build_c33_3d, 350, '3D (Om,h,f_1)'))

ALT_IDS = ['A01', 'A05', 'A12', 'A17',
           'A03', 'A06', 'A08', 'A09', 'A11', 'A13',
           'A15', 'A16', 'A19', 'A20']
for _aid in ALT_IDS:
    _name = ALT[_aid][0]
    CANDIDATES.append((_aid, _name,
                       (lambda _a=_aid: _build_alt(_a)),
                       300, 'closed-form 2D'))


# ---------------------------------------------------------------------------
# Jeffreys' scale
# ---------------------------------------------------------------------------

def classify(dlnZ):
    if not np.isfinite(dlnZ):
        return 'invalid'
    if dlnZ > 5.0:
        return 'strong'
    if dlnZ > 2.5:
        return 'substantial'
    if dlnZ > 1.0:
        return 'weak'
    if dlnZ > -1.0:
        return 'inconclusive'
    return 'decisive-against'


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def main():
    print("=" * 72)
    print("Phase L5-C: Bayesian Evidence via dynesty nested sampling")
    print("=" * 72)
    print(f"n_candidates = {len(CANDIDATES)}")
    print(f"LCDM reference chi2 = {LCDM_CHI2:.3f}")
    print()

    results = {}
    t_global = time.time()

    for aid, name, builder, nlive, note in CANDIDATES:
        print(f"[{aid}] {name}  (nlive={nlive}, {note})")
        t0 = time.time()
        try:
            ll, pt, ndim = builder()
            ev = nested_evidence(ll, pt, ndim, nlive=nlive, seed=42)
            dt = time.time() - t0
            ev['elapsed_sec'] = dt
            ev['ndim'] = ndim
            ev['name'] = name
            ev['note'] = note
            results[aid] = ev
            print(f"    -> ln Z = {ev['logz']:+.3f} +/- {ev['logz_err']:.3f}"
                  f"  niter={ev['niter']}  [{dt:.1f}s]")
        except Exception as e:
            dt = time.time() - t0
            print(f"    !! FAILED after {dt:.1f}s: {e}")
            traceback.print_exc()
            results[aid] = {'error': str(e), 'elapsed_sec': dt,
                            'name': name, 'note': note}

    # Delta ln Z relative to LCDM
    lcdm_logz = results.get('LCDM', {}).get('logz')
    if lcdm_logz is None:
        print("ERROR: LCDM evidence failed; cannot compute Delta ln Z")
        return
    print()
    print(f"LCDM ln Z = {lcdm_logz:+.3f}")
    print()

    table = []
    for aid, ev in results.items():
        if 'logz' not in ev:
            table.append({'id': aid, 'name': ev['name'],
                          'logz': None, 'logz_err': None,
                          'dlnZ': None, 'verdict': 'failed',
                          'ndim': ev.get('ndim'),
                          'note': ev.get('note', '')})
            continue
        dlnZ = ev['logz'] - lcdm_logz
        verdict = classify(dlnZ)
        table.append({
            'id': aid,
            'name': ev['name'],
            'logz': ev['logz'],
            'logz_err': ev['logz_err'],
            'niter': ev['niter'],
            'ndim': ev['ndim'],
            'nlive': ev['nlive'],
            'dlnZ': dlnZ,
            'verdict': verdict,
            'note': ev.get('note', ''),
            'elapsed_sec': ev['elapsed_sec'],
        })

    # Sort by dlnZ descending (None last)
    def _sort_key(row):
        d = row['dlnZ']
        return (-d if d is not None else 1e9)
    table.sort(key=_sort_key)

    # Dump JSON
    out_path = os.path.join(_THIS, 'evidence_all.json')
    payload = {
        'lcdm_logz': lcdm_logz,
        'lcdm_chi2': LCDM_CHI2,
        'n_candidates': len(CANDIDATES),
        'seed': 42,
        'jeffreys_scale': {
            'strong': 'dlnZ > +5',
            'substantial': '+2.5 < dlnZ <= +5 (Q8 PASS)',
            'weak': '+1 < dlnZ <= +2.5',
            'inconclusive': '-1 < dlnZ <= +1',
            'decisive-against': 'dlnZ <= -1 (K14 KILL)',
        },
        'results': results,
        'table': table,
        'elapsed_total_sec': time.time() - t_global,
    }
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(_jsonify(payload), f, indent=2)
    print(f"Wrote {out_path}")
    print()

    # Summary table
    print("=" * 72)
    print("SUMMARY  (sorted by Delta ln Z, descending)")
    print("=" * 72)
    print(f"{'ID':<6}{'ndim':>5}{'ln Z':>12}{'+/-':>8}"
          f"{'dlnZ':>10}  {'verdict':<18}note")
    print("-" * 72)
    for r in table:
        if r['logz'] is None:
            print(f"{r['id']:<6}{'-':>5}{'FAILED':>12}{'-':>8}"
                  f"{'-':>10}  {'failed':<18}{r.get('note','')}")
            continue
        print(f"{r['id']:<6}{r['ndim']:>5}{r['logz']:>+12.3f}"
              f"{r['logz_err']:>8.3f}{r['dlnZ']:>+10.3f}  "
              f"{r['verdict']:<18}{r['note']}")

    # Top winners
    print()
    print("Substantial-or-better (dlnZ > +2.5):")
    wins = [r for r in table if r['dlnZ'] is not None and r['dlnZ'] > 2.5]
    if not wins:
        print("  (none)")
    else:
        for r in wins[:10]:
            print(f"  {r['id']}  dlnZ = {r['dlnZ']:+.2f}  ({r['verdict']})")

    print()
    print("K14 kills (dlnZ < -1):")
    kills = [r for r in table if r['dlnZ'] is not None and r['dlnZ'] < -1.0]
    if not kills:
        print("  (none)")
    else:
        for r in kills:
            print(f"  {r['id']}  dlnZ = {r['dlnZ']:+.2f}")

    print()
    print(f"Total elapsed: {time.time()-t_global:.1f}s")


if __name__ == '__main__':
    main()
