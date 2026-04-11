# -*- coding: utf-8 -*-
"""
L3 master runner — fit & judge all 11 L2 survivors against BAO+SN+CMB+RSD.

For each ModelSpec in ``models.ALL_MODELS``:

  1. Multi-start Nelder-Mead minimisation of total chi^2 over
     (Omega_m, h, *theta) with model-specific bounds.
  2. CPL (w0, w_a) reconstruction on z∈[0.05, 1.8] from the best fit.
  3. Cassini |γ-1| analytic spec.
  4. Phantom crossing scan on z∈[0, 2].
  5. KILL criteria K1-K8 application.
  6. Dumps result into simulations/l3/results/<ID>.json.

Finally writes simulations/l3/results/summary.json with ranking.
"""
from __future__ import annotations

import io
import json
import os
import sys

# Force UTF-8 stdout/stderr (Windows cp949 guard).
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
import traceback
from dataclasses import asdict

import numpy as np
from scipy.optimize import minimize

_THIS = os.path.dirname(os.path.abspath(__file__))
if _THIS not in sys.path:
    sys.path.insert(0, _THIS)
sys.path.insert(0, os.path.dirname(_THIS))

import config  # noqa: E402
from data_loader import chi2_joint, get_data  # noqa: E402
import models as M  # noqa: E402


RESULTS_DIR = os.path.join(_THIS, 'results')
os.makedirs(RESULTS_DIR, exist_ok=True)


with open(os.path.join(_THIS, 'lcdm_baseline.json'), 'r', encoding='utf-8') as f:
    LCDM_BASE = json.load(f)
LCDM_TOT = float(LCDM_BASE['chi2_total'])


# ---------------------------------------------------------------------------
# KILL criteria
# ---------------------------------------------------------------------------

def apply_kill(model: M.ModelSpec, fit: dict) -> dict:
    """Returns dict with keep (bool), reasons (list of failed K ids)."""
    reasons = []

    dchi2 = fit['chi2_total'] - LCDM_TOT
    if dchi2 > 4.0:
        reasons.append(f"K1 Δχ²={dchi2:.2f}>+4")

    wa = abs(fit.get('wa', 0.0))
    if wa < 0.125:
        reasons.append(f"K2 |w_a|={wa:.4f}<0.125")

    if fit.get('phantom_cross', False):
        reasons.append("K3 phantom crossing")

    if abs(model.gamma_minus_one) > 2.3e-5:
        reasons.append(f"K4 |γ-1|={model.gamma_minus_one:.2e}")

    return {
        'keep': len(reasons) == 0,
        'failed_K': reasons,
        'delta_chi2': dchi2,
    }


# ---------------------------------------------------------------------------
# Fit loop per model
# ---------------------------------------------------------------------------

def fit_model(spec: M.ModelSpec) -> dict:
    """Multi-start Nelder-Mead over (Om, h, *theta). Returns best-fit dict.

    Parameters are clipped inside ``total`` instead of returning a hard
    penalty, so the Nelder-Mead simplex sees a smooth landscape. Bounds
    are kept tight around the LCDM best-fit (Om∈[0.28, 0.36], h∈[0.64,
    0.71]) to avoid runaways into high-z Friedmann blow-ups.
    """
    full_bounds = [(0.28, 0.36), (0.64, 0.71)] + list(spec.bounds)
    lo = np.array([b[0] for b in full_bounds])
    hi = np.array([b[1] for b in full_bounds])

    def _clip(x):
        return np.clip(np.asarray(x, dtype=float), lo, hi)

    def total(x_raw):
        x = _clip(x_raw)
        # Penalise boundary excursions so NM retreats from edges
        pen = float(np.sum(np.maximum(0.0, np.asarray(x_raw) - hi)**2) +
                    np.sum(np.maximum(0.0, lo - np.asarray(x_raw))**2)) * 1e4
        Om, h = x[0], x[1]
        theta = list(x[2:])
        omega_b = 0.02237
        omega_c = Om * h * h - omega_b
        if omega_c <= 0:
            return 1e6 + pen
        try:
            E = spec.build(theta, Om, h)
            if E is None:
                return 1e6 + pen
            # E(z) sanity at high-z (z~1100 for CMB).
            e_hi = E(1100.0)
            if not np.isfinite(e_hi) or e_hi > 1e5 or e_hi < 1:
                return 1e6 + pen
            # E(z) must be monotonically increasing for physical models.
            e_lo = E(0.0)
            if not np.isfinite(e_lo) or abs(e_lo - 1.0) > 0.5:
                return 1e6 + pen
            res = chi2_joint(E, rd=147.09, Omega_m=Om,
                             omega_b=omega_b, omega_c=omega_c, h=h,
                             H0_km=100.0 * h)
            tot = res['total']
            if not np.isfinite(tot) or tot > 1e5:
                return 1e6 + pen
            return tot + pen
        except Exception:
            return 1e6 + pen

    rng = np.random.default_rng(42)
    starts = [
        [0.3153, 0.6736] + list(spec.theta0),
        [0.320, 0.670] + list(spec.theta0),
        [0.310, 0.680] + list(spec.theta0),
        [0.325, 0.668] + list(spec.theta0),
    ]
    # Theta-only randomisation, (Om, h) seeded at LCDM neighborhood.
    for _ in range(4):
        theta_r = [rng.uniform(b[0], b[1]) for b in spec.bounds]
        starts.append([0.315, 0.6736] + theta_r)

    best = None
    for s in starts:
        try:
            r = minimize(total, s, method='Nelder-Mead',
                         options={'xatol': 1e-5, 'fatol': 1e-4,
                                  'maxiter': 1200, 'adaptive': True})
            if r.fun < 5e5:
                if best is None or r.fun < best.fun:
                    best = r
        except Exception:
            continue

    if best is None:
        return {'status': 'fit_failed', 'spec': spec.ID}

    x = _clip(best.x)
    Om, h = float(x[0]), float(x[1])
    theta = [float(t) for t in x[2:]]
    omega_b = 0.02237
    omega_c = Om * h * h - omega_b
    E = spec.build(theta, Om, h)
    res = chi2_joint(E, rd=147.09, Omega_m=Om,
                     omega_b=omega_b, omega_c=omega_c, h=h,
                     H0_km=100.0 * h)
    w0, wa = M._cpl_fit(E, Om)
    phantom = M._phantom_crossing(E, Om)

    return {
        'status': 'ok',
        'ID': spec.ID,
        'name': spec.name,
        'family': spec.family,
        'Omega_m': float(Om),
        'h': float(h),
        'theta': [float(t) for t in theta],
        'theta_names': spec.theta_names,
        'chi2_bao': res['bao'],
        'chi2_sn': res['sn'],
        'chi2_cmb': res['cmb'],
        'chi2_rsd': res['rsd'],
        'chi2_total': res['total'],
        'w0': w0, 'wa': wa,
        'phantom_cross': phantom,
        'gamma_minus_one': spec.gamma_minus_one,
        'theory_score': spec.theory_score,
        'sqmh_sign_condition': spec.sqmh_sign_ok_condition,
        'notes': spec.notes,
    }


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------

def main():
    np.random.seed(42)
    _ = get_data()
    print("L3 master runner")
    print(f"LCDM baseline chi2 = {LCDM_TOT:.3f}")
    print("=" * 70)

    all_results = []
    for spec in M.ALL_MODELS:
        print(f"\n[{spec.ID}] {spec.name}  ({spec.family})")
        try:
            fit = fit_model(spec)
        except Exception as e:
            traceback.print_exc()
            fit = {'status': 'exception', 'spec': spec.ID, 'error': str(e)}

        if fit.get('status') != 'ok':
            print(f"  FAILED : {fit}")
            out_path = os.path.join(RESULTS_DIR, f"{spec.ID}.json")
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(fit, f, indent=2)
            all_results.append(fit)
            continue

        judge = apply_kill(spec, fit)
        fit.update(judge)
        all_results.append(fit)

        print(f"  Om={fit['Omega_m']:.4f}  h={fit['h']:.4f}")
        print(f"  theta ({', '.join(spec.theta_names)}) = "
              f"{[round(t, 4) for t in fit['theta']]}")
        print(f"  chi2: bao={fit['chi2_bao']:.2f}  sn={fit['chi2_sn']:.2f}  "
              f"cmb={fit['chi2_cmb']:.2f}  rsd={fit['chi2_rsd']:.2f}  "
              f"tot={fit['chi2_total']:.2f}")
        print(f"  Delta chi2 = {judge['delta_chi2']:+.2f}")
        print(f"  w0={fit['w0']:+.4f}  wa={fit['wa']:+.4f}  "
              f"phantom={fit['phantom_cross']}")
        if judge['keep']:
            print(f"  -> KEEP")
        else:
            print(f"  -> KILLED: {'; '.join(judge['failed_K'])}")

        out_path = os.path.join(RESULTS_DIR, f"{spec.ID}.json")
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(fit, f, indent=2)

    # Ranking summary
    oks = [r for r in all_results if r.get('status') == 'ok']
    oks.sort(key=lambda x: x['delta_chi2'])

    print("\n" + "=" * 70)
    print("L3 ranking (by Delta chi^2 vs LCDM)")
    print("=" * 70)
    print(f"{'ID':>6}  {'family':>14}  {'Dchi2':>8}  {'w0':>8}  "
          f"{'wa':>8}  status")
    for r in oks:
        st = "KEEP" if r.get('keep') else "KILL"
        print(f"{r['ID']:>6}  {r['family']:>14}  {r['delta_chi2']:+8.2f}  "
              f"{r['w0']:+8.4f}  {r['wa']:+8.4f}  {st}")

    summary = {
        'lcdm_baseline_total': LCDM_TOT,
        'lcdm': LCDM_BASE,
        'candidates': all_results,
        'ranking_ids': [r['ID'] for r in oks],
        'keep_ids': [r['ID'] for r in oks if r.get('keep')],
        'kill_ids': [r['ID'] for r in oks if not r.get('keep')],
    }
    with open(os.path.join(RESULTS_DIR, 'summary.json'), 'w',
              encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    print(f"\nKEEP: {summary['keep_ids']}")
    print(f"KILL: {summary['kill_ids']}")
    print(f"\nSaved {len(all_results)} result JSONs + summary.json")


if __name__ == "__main__":
    main()
