# -*- coding: utf-8 -*-
"""
L4 C28 MCMC driver: Maggiore-Mancarella RR non-local gravity.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_L4 = os.path.dirname(_HERE)
if _L4 not in sys.path:
    sys.path.insert(0, _L4)

import common  # noqa: E402
from common import (LCDM_CHI2, LCDM_OM, LCDM_H, OMEGA_R,
                    tight_fit, cpl_fit, phantom_crossing, run_mcmc,
                    cassini_ok)  # noqa: E402
from C28.background import build_E  # noqa: E402
from C28.perturbation import (mu_of_a_factory, sound_speed_sq,
                               gamma_minus_one_static)  # noqa: E402
from l3.data_loader import chi2_joint  # noqa: E402

_OMEGA_B = 0.02237

# theta = (gamma0, beta_shape, a_tail)
THETA_BOUNDS = [(1e-4, 0.08), (-0.5, 1.5), (0.5, 4.0)]
THETA0 = [0.015, 0.3, 2.0]
NAMES = ['Om', 'h', 'gamma0', 'beta_shape', 'a_tail']


def log_prob(x):
    Om, h, g0, bs, at = x
    if not (0.28 <= Om <= 0.36):
        return -np.inf
    if not (0.64 <= h <= 0.71):
        return -np.inf
    if not (1e-4 <= g0 <= 0.08):
        return -np.inf
    if not (-0.5 <= bs <= 1.5):
        return -np.inf
    if not (0.5 <= at <= 4.0):
        return -np.inf
    omega_b = _OMEGA_B
    omega_c = Om * h * h - omega_b
    if omega_c <= 0:
        return -np.inf
    try:
        E = build_E([g0, bs, at], Om, h)
        if E is None:
            return -np.inf
        e_hi = float(E(1100.0))
        if not np.isfinite(e_hi) or e_hi < 1 or e_hi > 1e5:
            return -np.inf
        res = chi2_joint(E, rd=147.09, Omega_m=Om,
                         omega_b=omega_b, omega_c=omega_c, h=h,
                         H0_km=100.0 * h)
        tot = res['total']
        if not np.isfinite(tot):
            return -np.inf
        return -0.5 * tot
    except Exception:
        return -np.inf


def main():
    np.random.seed(42)
    print("[C28] seed fit (capped Nelder-Mead) ...", flush=True)
    from scipy.optimize import minimize
    x_init = [LCDM_OM, LCDM_H, 0.015, 0.3, 2.0]

    def nll(x):
        lp = log_prob(x)
        return 1e6 if not np.isfinite(lp) else -2.0 * lp

    r = minimize(nll, x_init, method='Nelder-Mead',
                 options={'maxiter': 200, 'xatol': 1e-3, 'fatol': 1e-2,
                          'adaptive': True})
    x0 = list(r.x)
    print(f"[C28]   seed chi2={r.fun:.3f}", flush=True)
    print(f"[C28]   seed x0={x0}", flush=True)
    print("[C28] Running MCMC (nwalkers=24, nsteps=400, nburn=100) ...")
    mcmc = run_mcmc(log_prob, x0, NAMES,
                    nwalkers=24, nsteps=400, nburn=100, seed=42)
    means = mcmc['means']
    stds = mcmc['stds']
    rhat = mcmc['rhat']
    print(f"[C28]   backend={mcmc['backend']}  rhat={rhat}")
    for n, m, s in zip(NAMES, means, stds):
        print(f"[C28]   {n}: {m:.5f} +/- {s:.5f}")

    samples = mcmc['samples']
    if samples.shape[0] > 1:
        lps = np.array([log_prob(s) for s in samples[::20]])
        idx = np.argmax(lps)
        x_map = samples[::20][idx]
    else:
        x_map = np.array(x0)

    Om_m, h_m = float(means[0]), float(means[1])
    theta_m = [float(means[2]), float(means[3]), float(means[4])]
    E_m = build_E(theta_m, Om_m, h_m)
    if E_m is None:
        Om_m, h_m = float(x_map[0]), float(x_map[1])
        theta_m = [float(x_map[2]), float(x_map[3]), float(x_map[4])]
        E_m = build_E(theta_m, Om_m, h_m)

    w0, wa = cpl_fit(E_m, Om_m)
    pc = phantom_crossing(E_m, Om_m)
    cs2_min = sound_speed_sq(E_m.payload, theta_m[0])
    gm1 = gamma_minus_one_static()

    res_ch = chi2_joint(E_m, rd=147.09, Omega_m=Om_m,
                        omega_b=_OMEGA_B, omega_c=Om_m * h_m * h_m - _OMEGA_B,
                        h=h_m, H0_km=100.0 * h_m)
    chi2_total = float(res_ch['total'])
    delta_chi2 = chi2_total - LCDM_CHI2

    with open(os.path.join(os.path.dirname(_L4), 'l3', 'results', 'C28.json'),
              'r', encoding='utf-8') as f:
        l3 = json.load(f)
    toy_wa = float(l3['wa'])
    toy_w0 = float(l3['w0'])
    toy_full_consistent = bool(
        (np.sign(wa) == np.sign(toy_wa) or abs(toy_wa) < 0.02) and
        (np.sign(w0 + 1) == np.sign(toy_w0 + 1) or abs(toy_w0 + 1) < 0.02)
    )

    killed = []
    if delta_chi2 > 4.0:
        killed.append('K1')
    if abs(wa) < 0.125:
        killed.append('K2')
    if pc:
        killed.append('K3')
    if not cassini_ok(gm1):
        killed.append('K4')
    if any(r > 1.05 for r in rhat):
        killed.append('K9')
    if not toy_full_consistent:
        killed.append('K10')
    if cs2_min < 0:
        killed.append('K11')

    g0_excludes_0 = abs(means[2]) > 2.0 * max(stds[2], 1e-6)
    if (not g0_excludes_0) and delta_chi2 > -6.0:
        killed.append('K12')

    Q = {
        'Q1_all_K_clear': len(killed) == 0,
        'Q2_posterior_excludes_lcdm_or_dchi2_le_-6':
            bool(g0_excludes_0 or delta_chi2 <= -6.0),
        'Q3_toy_full_sign_mag_consistent': toy_full_consistent,
        'Q4_cs2_positive': cs2_min > 0,
        'Q5_cassini_num_ok': cassini_ok(gm1),
        'Q6_theory_score_ge_6': True,
    }
    keep = len(killed) == 0 and Q['Q2_posterior_excludes_lcdm_or_dchi2_le_-6']

    result = {
        'ID': 'C28',
        'name': 'Maggiore-Mancarella RR non-local',
        'family': 'Non-local',
        'Om': Om_m, 'h': h_m, 'theta': theta_m,
        'theta_names': ['gamma0', 'beta_shape', 'a_tail'],
        'chi2_bao': float(res_ch['bao']),
        'chi2_sn': float(res_ch['sn']),
        'chi2_cmb': float(res_ch['cmb']),
        'chi2_rsd': float(res_ch['rsd']),
        'chi2_total': chi2_total,
        'delta_chi2': float(delta_chi2),
        'w0': float(w0), 'wa': float(wa),
        'phantom_cross': bool(pc),
        'cs2_min': float(cs2_min),
        'gamma_minus_one': float(gm1),
        'toy_wa_L3': toy_wa,
        'toy_w0_L3': toy_w0,
        'toy_full_consistent': toy_full_consistent,
        'mcmc_backend': mcmc['backend'],
        'mcmc_means': list(map(float, means)),
        'mcmc_stds': list(map(float, stds)),
        'mcmc_rhat': list(map(float, rhat)),
        'mcmc_names': NAMES,
        'x_map': list(map(float, x_map)),
        'killed_K': killed,
        'keep': bool(keep),
        'Q_flags': Q,
        'notes': ('Localised (U, S) ODE with box U = -R, box S = -U. '
                  'gamma_RR(a) absorbed into modified Friedmann. Cassini '
                  'gamma-1=0 exact via R=0 auxiliary freeze.'),
    }

    out = os.path.join(_HERE, 'result.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"[C28] wrote {out}")

    post = os.path.join(_HERE, 'mcmc_posterior.json')
    with open(post, 'w', encoding='utf-8') as f:
        json.dump({
            'backend': mcmc['backend'],
            'names': NAMES,
            'means': list(map(float, means)),
            'stds': list(map(float, stds)),
            'rhat': list(map(float, rhat)),
            'x_map': list(map(float, x_map)),
        }, f, indent=2)

    print(f"[C28] w0={w0:.4f}  wa={wa:.4f}  delta_chi2={delta_chi2:+.3f}  keep={keep}")


if __name__ == '__main__':
    main()
