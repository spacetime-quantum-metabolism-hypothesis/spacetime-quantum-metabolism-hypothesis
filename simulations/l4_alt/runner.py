# -*- coding: utf-8 -*-
"""
Alt-20 Independent SQMH candidates runner.

20 zero-parameter closed-form rho_DE(a)/OL modifications where the
amplitude is locked to Omega_m (matter fraction) itself. Only (Om, h)
are fit against BAO+SN+CMB+RSD via L4 common utilities.

See refs/alt20_catalog.md for the frozen definitions.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

_THIS = os.path.dirname(os.path.abspath(__file__))
_SIMS = os.path.dirname(_THIS)
if _SIMS not in sys.path:
    sys.path.insert(0, _SIMS)

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')

from l4.common import (  # noqa: E402
    LCDM_CHI2, LCDM_OM, LCDM_H, OMEGA_R,
    tight_fit, cpl_fit, phantom_crossing, run_mcmc, chi2_joint,
)

# ---------------------------------------------------------------------------
# 20 zero-parameter closed-form modifications: rho_DE(a) = OL0 * f(a; Om)
# ---------------------------------------------------------------------------

def _make_E(f_ratio):
    """Wrap a f(a, Om) -> rho_DE/OL0 into a build_E(theta, Om, h) callable."""
    def build(theta, Om, h):
        OL0 = 1.0 - Om - OMEGA_R
        def E(z):
            z = np.asarray(z, dtype=float)
            a = 1.0 / (1.0 + z)
            r = f_ratio(a, Om)
            rho_de = OL0 * r
            E2 = OMEGA_R * (1 + z)**4 + Om * (1 + z)**3 + rho_de
            E2 = np.where(E2 > 0, E2, np.nan)
            return np.sqrt(E2)
        return E
    return build


def _safe_exp(x):
    return np.exp(np.clip(x, -50, 50))


ALT = {}

ALT['A01'] = ('SQMH canonical (matter-weighted drift)',
              lambda a, m: 1.0 + m * (1.0 - a))
ALT['A02'] = ('Quadratic metabolism drift',
              lambda a, m: 1.0 + m * (1.0 - a)**2)
ALT['A03'] = ('Log horizon entropy',
              lambda a, m: 1.0 - m * np.log(np.clip(a, 1e-8, None)))
ALT['A04'] = ('Volume-cumulative matter drift',
              lambda a, m: 1.0 + m * (1.0 - a**3))
ALT['A05'] = ('Sqrt relaxation',
              lambda a, m: np.sqrt(np.clip(1.0 + 2.0 * m * (1.0 - a), 1e-8, None)))
ALT['A06'] = ('Exponential metabolism',
              lambda a, m: _safe_exp(m * (1.0 - a)))
ALT['A07'] = ('Hyperbolic cosh',
              lambda a, m: np.cosh(m * (1.0 - a)))
ALT['A08'] = ('Tanh transition',
              lambda a, m: 1.0 + np.tanh(m * (1.0 - a)) / (1.0 + np.tanh(m)))
ALT['A09'] = ('Causal-diamond 2D',
              lambda a, m: 1.0 + m * (1.0 - a) * (2.0 - a))
ALT['A10'] = ('Reciprocal drift',
              lambda a, m: 1.0 / np.clip(1.0 - m * (1.0 - a) * a, 1e-6, None))
ALT['A11'] = ('Sigmoid (logistic)',
              lambda a, m: 2.0 / (1.0 + _safe_exp(-m * (1.0 - a))))
ALT['A12'] = ('Error-function diffusion',
              lambda a, m: 1.0 + _erf(m * (1.0 - a)))
ALT['A13'] = ('Arctan plateau',
              lambda a, m: 1.0 + (2.0 / np.pi) * np.arctan(m * (1.0 - a)))
ALT['A14'] = ('Matter-ratio power',
              lambda a, m: np.power(np.clip(a, 1e-8, None),
                                    -m * (1.0 - m) * (1.0 - a)))
ALT['A15'] = ('Stretched exponential',
              lambda a, m: _safe_exp(m * (1.0 - np.sqrt(np.clip(a, 0, None)))))
ALT['A16'] = ('Second-order Taylor',
              lambda a, m: 1.0 + m * (1.0 - a) + 0.5 * m * m * (1.0 - a)**2)
ALT['A17'] = ('Adiabatic pulse',
              lambda a, m: 1.0 + m * (1.0 - a) * _safe_exp(-(1.0 - a)**2))
ALT['A18'] = ('Gaussian localised',
              lambda a, m: 1.0 + m * (1.0 - _safe_exp(-(1.0 - a)**2 /
                                                       np.clip(m, 1e-6, None))))
ALT['A19'] = ('Harmonic fraction',
              lambda a, m: 1.0 / np.clip(
                  1.0 - m * m * (1.0 - a) / (2.0 - a), 1e-6, None))
ALT['A20'] = ('Two-term geometric',
              lambda a, m: (1.0 + m * (1.0 - a)) /
                           np.clip(1.0 - 0.5 * m * (1.0 - a)**2, 1e-6, None))


def _erf(x):
    from scipy.special import erf
    return erf(x)


# ---------------------------------------------------------------------------
# Screen + fit + MCMC for one candidate
# ---------------------------------------------------------------------------

def evaluate(aid, name, f_ratio):
    build_E = _make_E(f_ratio)
    # L3 tight fit  (theta empty -> 2-D fit over Om, h)
    fit = tight_fit(build_E, theta_bounds=[], theta0=[], seeds_extra=0)
    if fit is None:
        return {'id': aid, 'name': name, 'verdict': 'KILL',
                'reason': 'tight_fit failed', 'chi2_total': None,
                'delta_chi2': None}
    Om = fit['Om']; h = fit['h']
    chi2 = fit['chi2_total']
    dchi2 = chi2 - LCDM_CHI2
    E_best = fit['E']

    # K1: LCDM reduction -- skip (structural: none of these reduce exactly)
    # K2: |w_a| >= 0.01 cosmological signature (soft)
    try:
        w0, wa = cpl_fit(E_best, Om)
    except Exception:
        w0, wa = (np.nan, np.nan)
    # K3 phantom crossing
    pc = phantom_crossing(E_best, Om)
    # K4 E(z>3) monotonic increasing, high-z behaviour sane
    ztest = np.array([3.0, 10.0, 100.0, 1100.0])
    try:
        E_hi = np.array([float(E_best(z)) for z in ztest])
        k4_ok = bool(np.all(np.isfinite(E_hi)) and np.all(np.diff(E_hi) > 0)
                     and E_hi[-1] > 10.0)
    except Exception:
        k4_ok = False

    # Verdict
    verdict = 'KEEP'
    kill_reason = []
    if dchi2 > 0.0:
        verdict = 'KILL'; kill_reason.append(f'Δχ²={dchi2:+.2f}>0')
    if pc:
        verdict = 'KILL'; kill_reason.append('phantom crossing')
    if not k4_ok:
        verdict = 'KILL'; kill_reason.append('K4 high-z')
    if np.isfinite(wa) and abs(wa) < 0.01:
        # borderline (K2 soft): downgrade to KEEP-BORDER but not kill
        if verdict == 'KEEP':
            verdict = 'KEEP-BORDER'

    result = {
        'id': aid,
        'name': name,
        'Om': Om,
        'h': h,
        'chi2_total': chi2,
        'chi2_bao': fit['chi2_bao'],
        'chi2_sn': fit['chi2_sn'],
        'chi2_cmb': fit['chi2_cmb'],
        'chi2_rsd': fit['chi2_rsd'],
        'delta_chi2': dchi2,
        'w0': w0,
        'wa': wa,
        'phantom_crossing': pc,
        'k4_high_z_ok': k4_ok,
        'verdict': verdict,
        'kill_reason': '; '.join(kill_reason) if kill_reason else None,
    }

    # MCMC only for KEEP / KEEP-BORDER, budget small since 2-D
    if verdict in ('KEEP', 'KEEP-BORDER'):
        def log_prob(x):
            om, hh = x
            if not (0.28 <= om <= 0.36 and 0.64 <= hh <= 0.71):
                return -np.inf
            omega_b = 0.02237
            omega_c = om * hh * hh - omega_b
            if omega_c <= 0:
                return -np.inf
            try:
                E = build_E([], om, hh)
                e_hi = float(E(1100.0))
                if not np.isfinite(e_hi) or e_hi < 1 or e_hi > 1e5:
                    return -np.inf
                r = chi2_joint(E, rd=147.09, Omega_m=om,
                               omega_b=omega_b, omega_c=omega_c, h=hh,
                               H0_km=100.0 * hh)
                tot = r['total']
                if not np.isfinite(tot):
                    return -np.inf
                return -0.5 * tot
            except Exception:
                return -np.inf

        mcmc = run_mcmc(log_prob, [Om, h], ['Om', 'h'],
                        nwalkers=24, nsteps=500, nburn=200, seed=42)
        result['mcmc'] = {
            'backend': mcmc['backend'],
            'means': mcmc['means'],
            'stds': mcmc['stds'],
            'rhat': mcmc['rhat'],
        }
    return result


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


def main():
    results = []
    for aid, (name, f_ratio) in ALT.items():
        print(f"[{aid}] {name}...", flush=True)
        try:
            res = evaluate(aid, name, f_ratio)
        except Exception as e:
            res = {'id': aid, 'name': name, 'verdict': 'KILL',
                   'reason': f'exception: {e}'}
        print(f"  -> verdict={res.get('verdict')}  "
              f"Δχ²={res.get('delta_chi2')}  "
              f"(w0,wa)=({res.get('w0')},{res.get('wa')})",
              flush=True)
        results.append(res)

    out = {
        'lcdm_chi2': LCDM_CHI2,
        'lcdm_Om': LCDM_OM,
        'lcdm_h': LCDM_H,
        'n_candidates': len(results),
        'results': results,
    }
    out_path = os.path.join(_THIS, 'alt20_results.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(_jsonify(out), f, indent=2)
    print(f"\nWrote {out_path}")

    # Summary table
    print("\n=== SUMMARY ===")
    print(f"{'ID':<5}{'Verdict':<14}{'Δχ²':>10}{'w0':>10}{'wa':>10}")
    for r in results:
        d = r.get('delta_chi2')
        d_s = f"{d:+.2f}" if isinstance(d, (int, float)) else "--"
        w0 = r.get('w0'); wa = r.get('wa')
        w0_s = f"{w0:+.3f}" if isinstance(w0, (int, float)) else "--"
        wa_s = f"{wa:+.3f}" if isinstance(wa, (int, float)) else "--"
        print(f"{r['id']:<5}{r.get('verdict','?'):<14}{d_s:>10}{w0_s:>10}{wa_s:>10}")


if __name__ == '__main__':
    main()
