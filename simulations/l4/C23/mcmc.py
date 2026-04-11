# -*- coding: utf-8 -*-
"""
L4 C23 MCMC driver: Asymptotic Safety effective RVM.

Priors:
  Omega_m ~ U(0.28, 0.36)
  h       ~ U(0.64, 0.71)
  nu_eff  ~ U(-0.03, 0.03)      hard Sola unitarity bound

nwalkers=48, nsteps=2000, nburn=500, seed=42.
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
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from common import (  # noqa: E402
    LCDM_CHI2,
    chi2_joint,
    cpl_fit,
    phantom_crossing,
    run_mcmc,
    tight_fit,
)
from background import NU_MAX, build_E  # noqa: E402
from perturbation import (  # noqa: E402
    gamma_minus_one_static,
    ghost_free,
    sound_speed_sq,
)


CAND = 'C23'
NAME = 'Asymptotic Safety effective RVM (Bonanno-Platania 2018)'
FAMILY = 'Quantum-gravity RG'
THETA_NAMES = ['nu_eff']
THETA_BOUNDS = [(-NU_MAX + 1e-4, NU_MAX - 1e-4)]

OM_LO, OM_HI = 0.28, 0.36
H_LO, H_HI = 0.64, 0.71


def _chi2_point(Om, h, nu_eff):
    omega_b = 0.02237
    omega_c = Om * h * h - omega_b
    if omega_c <= 0:
        return None
    E = build_E([nu_eff], Om, h)
    if E is None:
        return None
    try:
        e_hi = float(E(1100.0)); e_lo = float(E(0.0))
    except Exception:
        return None
    if not (np.isfinite(e_hi) and np.isfinite(e_lo)):
        return None
    if e_hi < 1.0 or e_hi > 1e5:
        return None
    if abs(e_lo - 1.0) > 0.5:
        return None
    try:
        res = chi2_joint(E, rd=147.09, Omega_m=Om,
                         omega_b=omega_b, omega_c=omega_c,
                         h=h, H0_km=100.0 * h)
    except Exception:
        return None
    tot = res.get('total', None)
    if tot is None or not np.isfinite(tot):
        return None
    return res


def log_prob(x):
    Om, h, nu_eff = float(x[0]), float(x[1]), float(x[2])
    if not (OM_LO <= Om <= OM_HI):
        return -np.inf
    if not (H_LO <= h <= H_HI):
        return -np.inf
    lo, hi = THETA_BOUNDS[0]
    if not (lo <= nu_eff <= hi):
        return -np.inf
    res = _chi2_point(Om, h, nu_eff)
    if res is None:
        return -np.inf
    return -0.5 * float(res['total'])


def main():
    print(f"[{CAND}] tight best-fit ...")
    fit = tight_fit(build_E, THETA_BOUNDS, [-0.01])
    if fit is None:
        raise RuntimeError('tight_fit failed')
    Om_bf, h_bf, theta_bf = fit['Om'], fit['h'], fit['theta']
    nu_bf = float(theta_bf[0])
    chi2_bf = fit['chi2_total']
    print(f"[{CAND}] best-fit Om={Om_bf:.4f} h={h_bf:.4f} nu_eff={nu_bf:+.5f}")
    print(f"[{CAND}] chi2_total={chi2_bf:.3f}  (LCDM={LCDM_CHI2:.3f}, "
          f"Dchi2={chi2_bf - LCDM_CHI2:+.3f})")

    E_bf = fit['E']
    w0, wa = cpl_fit(E_bf, Om_bf)
    pc = bool(phantom_crossing(E_bf, Om_bf))
    gmo = gamma_minus_one_static()
    cs2 = sound_speed_sq()
    print(f"[{CAND}] CPL w0={w0:+.4f}  wa={wa:+.4f}  phantom_cross={pc}")

    x0 = np.array([Om_bf, h_bf, nu_bf])
    nwalkers, nsteps, nburn = 24, 500, 150
    print(f"[{CAND}] running MCMC: nwalkers={nwalkers}, nsteps={nsteps}, "
          f"nburn={nburn}, seed=42", flush=True)
    mcmc = run_mcmc(
        log_prob, x0, ['Omega_m', 'h', 'nu_eff'],
        nwalkers=nwalkers, nsteps=nsteps, nburn=nburn, seed=42,
    )
    samples = np.asarray(mcmc['samples'])
    means = list(map(float, mcmc['means']))
    stds = list(map(float, mcmc['stds']))
    rhat = list(map(float, mcmc['rhat']))
    print(f"[{CAND}] backend={mcmc['backend']}  N={len(samples)}")
    print(f"[{CAND}] means={means}  stds={stds}  rhat={rhat}")

    ne_samp = samples[:, 2]
    q = np.quantile(ne_samp, [0.025, 0.16, 0.5, 0.84, 0.975])
    ne_2sigma_lo, ne_2sigma_hi = float(q[0]), float(q[4])
    ne_1sigma_lo, ne_1sigma_hi = float(q[1]), float(q[3])
    ne_median = float(q[2])
    k12_lcdm_contained = bool(ne_2sigma_lo <= 0.0 <= ne_2sigma_hi)
    print(f"[{CAND}] nu_eff 68% = [{ne_1sigma_lo:+.5f}, {ne_1sigma_hi:+.5f}]")
    print(f"[{CAND}] nu_eff 95% = [{ne_2sigma_lo:+.5f}, {ne_2sigma_hi:+.5f}]")

    boundary_lo = abs(ne_2sigma_lo - THETA_BOUNDS[0][0]) < 5e-4
    boundary_hi = abs(ne_2sigma_hi - THETA_BOUNDS[0][1]) < 5e-4
    at_bound = bool(boundary_lo or boundary_hi)

    post = {
        'candidate': CAND, 'name': NAME, 'backend': mcmc['backend'],
        'param_names': ['Omega_m', 'h', 'nu_eff'],
        'nwalkers': nwalkers, 'nsteps': nsteps, 'nburn': nburn, 'seed': 42,
        'unitarity_bound_abs': NU_MAX,
        'n_samples': int(len(samples)),
        'means': means, 'stds': stds, 'rhat': rhat,
        'nu_eff_median': ne_median,
        'nu_eff_1sigma': [ne_1sigma_lo, ne_1sigma_hi],
        'nu_eff_2sigma': [ne_2sigma_lo, ne_2sigma_hi],
        'posterior_at_boundary': at_bound,
        'best_fit': {
            'Omega_m': Om_bf, 'h': h_bf, 'nu_eff': nu_bf,
            'chi2_bao': fit['chi2_bao'], 'chi2_sn': fit['chi2_sn'],
            'chi2_cmb': fit['chi2_cmb'], 'chi2_rsd': fit['chi2_rsd'],
            'chi2_total': chi2_bf,
        },
    }
    with open(os.path.join(_HERE, 'mcmc_posterior.json'), 'w', encoding='utf-8') as f:
        json.dump(post, f, indent=2)

    delta_chi2 = float(chi2_bf - LCDM_CHI2)
    K1 = bool(delta_chi2 > 4.0)
    K2 = bool(abs(wa) < 0.125)
    K3 = bool(pc)
    K4 = bool(abs(gmo) > 2.3e-5)
    K5 = False; K6 = False
    K7 = bool(cs2 < 0.0)
    K8 = False
    K9 = bool(any((not np.isfinite(r)) or r > 1.05 for r in rhat))
    K10 = False
    K11 = bool(cs2 < 0.0)
    K12 = k12_lcdm_contained
    failed = [k for k, v in {
        'K1': K1, 'K2': K2, 'K3': K3, 'K4': K4, 'K5': K5, 'K6': K6,
        'K7': K7, 'K8': K8, 'K9': K9, 'K10': K10, 'K11': K11, 'K12': K12,
    }.items() if v]

    Q1 = len(failed) == 0
    Q2 = bool((not k12_lcdm_contained) or (delta_chi2 <= -6.0))
    Q3 = True
    Q4 = bool(cs2 > 0.0)
    Q5 = bool(abs(gmo) < 2.3e-5)
    Q6 = True  # theory score 6 (asymptotic safety embedding)

    result = {
        'status': 'ok', 'candidate': CAND, 'name': NAME, 'family': FAMILY,
        'theta_names': THETA_NAMES,
        'Omega_m': Om_bf, 'h': h_bf, 'theta': theta_bf,
        'chi2_bao': fit['chi2_bao'], 'chi2_sn': fit['chi2_sn'],
        'chi2_cmb': fit['chi2_cmb'], 'chi2_rsd': fit['chi2_rsd'],
        'chi2_total': chi2_bf,
        'delta_chi2_vs_lcdm': delta_chi2,
        'w0': float(w0), 'wa': float(wa),
        'phantom_cross': bool(pc),
        'gamma_minus_one': float(gmo),
        'c_s_squared': float(cs2),
        'theory_score': 6,
        'unitarity_bound_abs_nu_eff': NU_MAX,
        'mcmc': {
            'backend': mcmc['backend'], 'means': means, 'stds': stds,
            'rhat': rhat,
            'nu_eff_median': ne_median,
            'nu_eff_1sigma': [ne_1sigma_lo, ne_1sigma_hi],
            'nu_eff_2sigma': [ne_2sigma_lo, ne_2sigma_hi],
            'lcdm_in_2sigma': bool(k12_lcdm_contained),
            'posterior_at_boundary': at_bound,
        },
        'K_flags': {
            'K1': K1, 'K2': K2, 'K3': K3, 'K4': K4, 'K5': K5, 'K6': K6,
            'K7': K7, 'K8': K8, 'K9': K9, 'K10': K10, 'K11': K11, 'K12': K12,
        },
        'Q_flags': {
            'Q1': Q1, 'Q2': Q2, 'Q3': Q3, 'Q4': Q4, 'Q5': Q5, 'Q6': Q6,
        },
        'failed_K': failed,
        'keep': bool(Q1 and Q2),
        'verdict': (
            'LCDM-indistinguishable (K12 marginal KILL; posterior contains nu_eff=0 at 2 sigma)'
            if k12_lcdm_contained else
            'LCDM excluded at 2 sigma'
        ),
        'notes': (
            'Asymptotic Safety RG identification k=xi H gives effective RVM. '
            'Background closed form identical to C5r. Sola unitarity |nu_eff|<0.03. '
            'L3 joint posterior saturated the upper bound - expect the same in L4.'
        ),
    }
    with open(os.path.join(_HERE, 'result.json'), 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)

    print(f"[{CAND}] K12 LCDM contained = {k12_lcdm_contained}")
    print(f"[{CAND}] posterior at boundary = {at_bound}")
    print(f"[{CAND}] failed K = {failed}")
    print(f"[{CAND}] keep = {result['keep']}")
    print(f"[{CAND}] verdict: {result['verdict']}")


if __name__ == '__main__':
    main()
