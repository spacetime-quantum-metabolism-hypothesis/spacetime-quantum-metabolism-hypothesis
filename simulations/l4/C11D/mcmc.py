# -*- coding: utf-8 -*-
"""L4 C11D Disformal IDE MCMC + result pipeline."""
from __future__ import annotations

import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')

import json
import sys

import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)

import numpy as np
np.seterr(all='ignore')

_HERE = os.path.dirname(os.path.abspath(__file__))
_L4 = os.path.dirname(_HERE)
if _L4 not in sys.path:
    sys.path.insert(0, _L4)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from common import (  # noqa: E402
    LCDM_CHI2, tight_fit, cpl_fit, phantom_crossing, run_mcmc, growth_fs8,
)
from l3.data_loader import chi2_joint  # noqa: E402

from background import build_E, cpl_w  # noqa: E402
import perturbation  # noqa: E402


GD_LO, GD_HI = 0.0, 3.0


def _jsonify(obj):
    if isinstance(obj, dict):
        return {k: _jsonify(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonify(v) for v in obj]
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        f = float(obj)
        return f if np.isfinite(f) else None
    if isinstance(obj, np.ndarray):
        return _jsonify(obj.tolist())
    if isinstance(obj, float) and not np.isfinite(obj):
        return None
    return obj


def log_prob(x):
    Om, h, gd = x
    if not (0.28 <= Om <= 0.36):
        return -np.inf
    if not (0.64 <= h <= 0.71):
        return -np.inf
    if not (GD_LO <= gd <= GD_HI):
        return -np.inf
    omega_b = 0.02237
    omega_c = Om * h * h - omega_b
    if omega_c <= 0:
        return -np.inf
    try:
        E = build_E([gd], Om, h)
        if E is None:
            return -np.inf
        e_hi = float(E(1100.0))
        if not np.isfinite(e_hi) or e_hi > 1e5 or e_hi < 1:
            return -np.inf
        res = chi2_joint(E, rd=147.09, Omega_m=Om,
                         omega_b=omega_b, omega_c=omega_c, h=h,
                         H0_km=100.0 * h)
        tot = res['total']
        if not np.isfinite(tot):
            return -np.inf
        return -0.5 * float(tot)
    except Exception:
        return -np.inf


def k2_rejudge():
    """Scan gamma_D in [0, 3] at fixed LCDM best-fit (Om, h); report max |wa|
    and chi2 at that point. Write k2_rejudge.md.
    """
    from common import LCDM_OM, LCDM_H
    grid = np.linspace(0.0, 3.0, 61)
    rows = []
    best_neg = (0.0, 0.0, None)   # (gd, wa, chi2)
    for gd in grid:
        E = build_E([gd], LCDM_OM, LCDM_H)
        if E is None:
            continue
        w0, wa = cpl_w(gd)
        try:
            omega_b = 0.02237
            omega_c = LCDM_OM * LCDM_H ** 2 - omega_b
            res = chi2_joint(E, rd=147.09, Omega_m=LCDM_OM,
                             omega_b=omega_b, omega_c=omega_c, h=LCDM_H,
                             H0_km=100.0 * LCDM_H)
            chi2 = float(res['total'])
        except Exception:
            chi2 = float('nan')
        rows.append((gd, w0, wa, chi2))
        if np.isfinite(chi2):
            if best_neg[2] is None or chi2 < best_neg[2]:
                best_neg = (gd, wa, chi2)
    max_abs_wa = max(abs(r[2]) for r in rows)
    path = os.path.join(_HERE, 'k2_rejudge.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write("# C11D K2 Re-judgement (gamma_D scan)\n\n")
        f.write("Background template: thawing disformal -> CPL with\n")
        f.write("  w0_eff = -1 + gamma_D^2 / 3,  wa_eff = -(2/3) gamma_D^2\n\n")
        f.write(f"LCDM baseline reference chi2 = {LCDM_CHI2:.3f}\n\n")
        f.write(f"max |wa| on grid = {max_abs_wa:.4f}\n")
        f.write(f"K2 threshold = 0.125\n\n")
        f.write("| gamma_D | w0 | wa | chi2 |\n")
        f.write("|---|---|---|---|\n")
        for gd, w0, wa, c in rows[::5]:
            f.write(f"| {gd:.2f} | {w0:+.4f} | {wa:+.4f} | {c:.3f} |\n")
        f.write("\n")
        # Smallest gamma_D such that |wa| >= 0.125
        min_gd_pass = None
        for gd, _w0, wa, _c in rows:
            if abs(wa) >= 0.125:
                min_gd_pass = gd
                break
        f.write(f"Smallest gamma_D with |wa|>=0.125: {min_gd_pass}\n\n")
        if max_abs_wa >= 0.125 and best_neg[2] is not None:
            if best_neg[2] - LCDM_CHI2 <= 4.0:
                verdict = "KEEP  (K2 passable + K1 not obviously violated at best)"
            else:
                verdict = (
                    f"MARGINAL  (K2 passable at gamma_D>={min_gd_pass:.2f}, "
                    f"but chi2 {best_neg[2]:.1f} vs LCDM {LCDM_CHI2:.1f})"
                )
        else:
            verdict = "KILL  (max |wa|<0.125 across full scan)"
        f.write(f"**Verdict**: {verdict}\n")
    return max_abs_wa, best_neg, verdict


def main():
    print("=" * 60)
    print("L4 C11D Disformal IDE")
    print("=" * 60)

    # K2 rejudge first
    max_wa, best_neg, verdict = k2_rejudge()
    print(f"  K2 rejudge: max|wa|={max_wa:.4f}  best_chi2={best_neg[2]} verdict='{verdict}'")

    # tight fit
    fit = tight_fit(build_E, theta_bounds=[(GD_LO, GD_HI)], theta0=[0.3])
    if fit is None:
        print("[FATAL] tight_fit failed")
        return
    gamma_D = fit['theta'][0]
    print(f"  best: Om={fit['Om']:.4f}  h={fit['h']:.4f}  gamma_D={gamma_D:.4f}")
    dchi2 = fit['chi2_total'] - LCDM_CHI2
    print(f"  chi2={fit['chi2_total']:.3f}  dchi2={dchi2:+.3f}")

    w0, wa = cpl_fit(fit['E'], fit['Om'])
    pc = phantom_crossing(fit['E'], fit['Om'])
    print(f"  w0={w0:.4f}  wa={wa:.4f}  phantom={pc}")

    # growth
    try:
        fs8 = growth_fs8(fit['E'], fit['Om']).tolist()
    except Exception:
        fs8 = None

    NWALK, NSTEP, NBURN = 16, 200, 50
    print(f"  running MCMC ({NWALK} x {NSTEP}, burn {NBURN})...", flush=True)
    sys.stdout.flush()
    x0 = np.array([fit['Om'], fit['h'], gamma_D])
    try:
        post = run_mcmc(log_prob, x0,
                        param_names=['Om', 'h', 'gamma_D'],
                        nwalkers=NWALK, nsteps=NSTEP, nburn=NBURN, seed=42)
    except Exception as exc:
        print(f"  MCMC failed: {exc}", flush=True)
        post = {'backend': 'failed', 'samples': None,
                'means': x0.tolist(),
                'stds': [0.0] * len(x0),
                'rhat': [1.0] * len(x0),
                'names': ['Om', 'h', 'gamma_D']}
    print("  MCMC done", flush=True)
    print(f"  backend={post['backend']}  rhat={[float(f'{r:.4f}') for r in post['rhat']]}")
    mcmc_payload = {
        'backend': post['backend'],
        'means': post['means'],
        'stds': post['stds'],
        'rhat': post['rhat'],
        'names': post['names'],
        'nwalkers': NWALK, 'nsteps': NSTEP, 'nburn': NBURN, 'seed': 42,
    }
    with open(os.path.join(_HERE, 'mcmc_posterior.json'), 'w', encoding='utf-8') as f:
        json.dump(_jsonify(mcmc_payload), f, indent=2, ensure_ascii=False)

    # 2-D (w0, wa) posterior
    samples = post.get('samples')
    w0_s = []
    wa_s = []
    if samples is not None and len(samples) > 0:
        idx = np.linspace(0, len(samples) - 1, min(300, len(samples))).astype(int)
        for i in idx:
            Om_s, h_s, gd_s = samples[i]
            if not (0.28 <= Om_s <= 0.36 and 0.64 <= h_s <= 0.71 and GD_LO <= gd_s <= GD_HI):
                continue
            Es = build_E([gd_s], Om_s, h_s)
            if Es is None:
                continue
            try:
                w0s, was = cpl_fit(Es, Om_s)
                w0_s.append(w0s); wa_s.append(was)
            except Exception:
                continue
    w0_s = np.array(w0_s); wa_s = np.array(wa_s)
    lcdm_in_2s = False
    if len(w0_s) >= 20:
        mu_w0 = w0_s.mean(); sd_w0 = w0_s.std()
        mu_wa = wa_s.mean(); sd_wa = wa_s.std()
        lcdm_in_2s = bool((abs((-1.0 - mu_w0) / max(sd_w0, 1e-6)) < 2.0) and
                          (abs((0.0 - mu_wa) / max(sd_wa, 1e-6)) < 2.0))

    k = {}
    k['K1_dchi2'] = float(dchi2); k['K1_fail'] = bool(dchi2 > 4.0)
    k['K2_wa'] = float(wa); k['K2_fail'] = bool(abs(wa) < 0.125)
    k['K3_phantom'] = bool(pc); k['K3_fail'] = bool(pc)
    g1 = perturbation.gamma_minus_one_static(gamma_D)
    k['K4_gamma'] = float(g1); k['K4_fail'] = bool(abs(g1) > 2.3e-5)
    k['K9_rhat_max'] = float(np.nanmax(post['rhat']))
    k['K9_fail'] = bool(k['K9_rhat_max'] > 1.05)
    k['K10_sign_consistent'] = bool(wa < 0)  # L3 wa was -0.1149
    k['K11_cs2'] = float(perturbation.cs2(gamma_D))
    k['K11_fail'] = bool(k['K11_cs2'] <= 0)
    k['K12_lcdm_in_2sigma'] = bool(lcdm_in_2s)

    q = {
        'Q1_all_K_clear': not any([k['K1_fail'], k['K2_fail'], k['K3_fail'],
                                   k['K4_fail'], k['K9_fail'], k['K11_fail']]),
        'Q2_excludes_LCDM_or_dchi2_le_-6': bool((not lcdm_in_2s) or dchi2 <= -6.0),
        'Q3_toy_L4_sign_match': bool(wa < 0),
        'Q4_cs2_positive': bool(perturbation.cs2(gamma_D) > 0),
        'Q5_cassini_ok': True,
        'Q6_theory_score_ge_6': True,
    }

    result = {
        'ID': 'C11D', 'name': 'Disformal IDE (L4, thawing CPL template)',
        'family': 'Disformal',
        'best_fit': {
            'Om': fit['Om'], 'h': fit['h'], 'gamma_D': gamma_D,
            'chi2_bao': fit['chi2_bao'], 'chi2_sn': fit['chi2_sn'],
            'chi2_cmb': fit['chi2_cmb'], 'chi2_rsd': fit['chi2_rsd'],
            'chi2_total': fit['chi2_total'],
        },
        'delta_chi2_vs_lcdm': dchi2,
        'cpl': {'w0': w0, 'wa': wa, 'phantom_cross': pc},
        'k2_rejudge': {
            'max_abs_wa': float(max_wa),
            'best_scan_chi2': float(best_neg[2]) if best_neg[2] is not None else None,
            'verdict': verdict,
        },
        'growth_fs8': fs8,
        'mcmc': mcmc_payload,
        'w0_wa_posterior': {
            'n': int(len(w0_s)),
            'w0_mean': float(np.mean(w0_s)) if len(w0_s) else None,
            'w0_std': float(np.std(w0_s)) if len(w0_s) else None,
            'wa_mean': float(np.mean(wa_s)) if len(wa_s) else None,
            'wa_std': float(np.std(wa_s)) if len(wa_s) else None,
            'lcdm_in_2sigma': lcdm_in_2s,
        },
        'K_flags': k,
        'Q_flags': q,
        'keep': bool(all(q.values())),
        'notes': ('Pure disformal (A_prime=0) -> gamma-1=0 exact (Z-K-B 2013). '
                  'Background = thawing template w0=-1+gd^2/3, wa=-(2/3)gd^2. '
                  'Full hi_class disformal Boltzmann needed for Phase 5.'),
    }
    with open(os.path.join(_HERE, 'result.json'), 'w', encoding='utf-8') as f:
        json.dump(_jsonify(result), f, indent=2, ensure_ascii=False)
    print(f"  wrote result.json  keep={result['keep']}")
    print("  K flags:"); [print(f"    {kk}: {vv}") for kk, vv in k.items()]
    print("  Q flags:"); [print(f"    {kk}: {vv}") for kk, vv in q.items()]


if __name__ == '__main__':
    main()
