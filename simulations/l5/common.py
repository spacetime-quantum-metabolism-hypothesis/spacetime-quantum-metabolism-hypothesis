# -*- coding: utf-8 -*-
"""
L5 common utilities.

Extends simulations/l5/common (no, l4/common) with:
  * production-grade MCMC wrapper (48x2000, R-hat<1.02)
  * dynesty nested sampling for Bayesian evidence
  * cosmic shear S8 channel loader + chi2 extension
  * DESI DR3 Fisher forecast helper
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')

_THIS = os.path.dirname(os.path.abspath(__file__))
_SIMS = os.path.dirname(_THIS)
for _p in (_SIMS, os.path.join(_SIMS, 'l3'), os.path.join(_SIMS, 'l4')):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Reuse L4 common
from l4.common import (  # noqa: E402
    LCDM_BASELINE, LCDM_CHI2, LCDM_OM, LCDM_H, OMEGA_R,
    E_lcdm, tight_fit, cpl_fit, phantom_crossing, growth_fs8, chi2_joint,
)


# ---------------------------------------------------------------------------
# Cosmic shear S_8 channel
# ---------------------------------------------------------------------------
# DES-Y3 cosmic shear (Abbott et al. 2022):  S_8 = 0.772 +/- 0.017
# KiDS-1000 (Asgari et al. 2021):            S_8 = 0.759 +/- 0.024
# Planck 2018 TT,TE,EE+lowE+lensing:         S_8 = 0.834 +/- 0.016
# Combined weak-lensing mean (inverse-var):  S_8 ~ 0.767 +/- 0.014
# (We use DES-Y3 + KiDS-1000 combined as the "WL" likelihood; Planck S_8
# is already folded into the compressed CMB constraint via theta*, omega_b,
# omega_c -- including it again here would double-count.)

S8_WL_MEAN = 0.7656  # DES-Y3 (0.772, s=0.017) + KiDS-1000 (0.759, s=0.024)
S8_WL_SIGMA = 0.0138  # inverse-variance combine


def s8_from_Efunc(E_func, Om, h, *, sigma8_0=0.811):
    """Compute S_8 = sigma_8 * sqrt(Om/0.3) at z=0.

    sigma_8(z=0) is approximated by sigma8_0 times the ratio D_model(a=1) /
    D_LCDM(a=1). For background-only modifications (mu=1, c_s^2=1) this is
    a small correction and we use the same growth ODE as `growth_fs8`.
    """
    from scipy.integrate import solve_ivp

    def _D0(Efun, Om_val):
        def rhs(a, y):
            D, Dp = y
            z = 1.0 / a - 1.0
            E = float(Efun(z))
            da = 1e-4 * a
            Ep = float(Efun(1.0 / (a + da) - 1.0))
            Em = float(Efun(1.0 / (a - da) - 1.0))
            dlnE_dlna = (np.log(Ep) - np.log(Em)) / (2 * da / a)
            Om_m_a = Om_val * a**(-3) / E**2
            Dpp = -(3.0 + dlnE_dlna) / a * Dp + 1.5 * Om_m_a * D / a**2
            return [Dp, Dpp]
        sol = solve_ivp(rhs, (1e-3, 1.0), [1e-3, 1.0], method='RK45',
                        rtol=1e-7, atol=1e-9, max_step=0.02, dense_output=True)
        if not sol.success:
            return None
        return float(sol.sol(1.0)[0])

    D0_model = _D0(E_func, Om)
    E_ref = E_lcdm(LCDM_OM, LCDM_H)
    D0_ref = _D0(E_ref, LCDM_OM)
    if D0_model is None or D0_ref is None or D0_ref == 0:
        return None
    sigma8 = sigma8_0 * (D0_model / D0_ref)
    return sigma8 * np.sqrt(Om / 0.3)


def chi2_shear(E_func, Om, h):
    """Return chi^2 contribution from DES-Y3 + KiDS-1000 S_8 WL combo."""
    S8 = s8_from_Efunc(E_func, Om, h)
    if S8 is None or not np.isfinite(S8):
        return 1e6
    return float(((S8 - S8_WL_MEAN) / S8_WL_SIGMA) ** 2)


def chi2_joint_with_shear(E_func, **kwargs):
    """BAO+SN+CMB+RSD (via chi2_joint) + WL S_8 term."""
    base = chi2_joint(E_func, **kwargs)
    Om = kwargs.get('Omega_m')
    h = kwargs.get('h')
    c_wl = chi2_shear(E_func, Om, h)
    total = base['total'] + c_wl
    out = dict(base)
    out['wl'] = c_wl
    out['total'] = total
    return out


# ---------------------------------------------------------------------------
# Production MCMC wrapper
# ---------------------------------------------------------------------------

def run_mcmc_production(log_prob, x0, param_names, *,
                        nwalkers=48, nsteps=2000, nburn=500, thin=10,
                        seed=42, rhat_target=1.02, max_retries=2):
    """emcee production MCMC with R-hat convergence guard.

    On R-hat > target: doubles nsteps up to max_retries and retries.
    """
    import emcee
    np.random.seed(seed)
    ndim = len(x0)
    x0 = np.asarray(x0, dtype=float)

    def _run(nw, ns, nb):
        p0 = x0 + 1e-3 * np.random.randn(nw, ndim) * np.maximum(np.abs(x0), 1e-2)
        sampler = emcee.EnsembleSampler(nw, ndim, log_prob)
        sampler.run_mcmc(p0, ns, progress=False)
        chain = sampler.get_chain(discard=nb, thin=thin, flat=True)
        full = sampler.get_chain(discard=nb)  # (steps, walkers, ndim)
        rhat = []
        for d in range(ndim):
            w_means = full[:, :, d].mean(axis=0)
            w_vars = full[:, :, d].var(axis=0)
            B = w_means.var() * full.shape[0]
            W = w_vars.mean()
            var_hat = (1.0 - 1.0 / full.shape[0]) * W + B / full.shape[0]
            rhat.append(float(np.sqrt(var_hat / max(W, 1e-30))))
        return chain, rhat

    steps = nsteps
    burn = nburn
    chain = None
    rhat = None
    for attempt in range(max_retries + 1):
        chain, rhat = _run(nwalkers, steps, burn)
        if max(rhat) <= rhat_target:
            break
        steps *= 2
        burn *= 2

    return {
        'backend': 'emcee',
        'samples': chain,
        'means': chain.mean(axis=0).tolist(),
        'stds': chain.std(axis=0).tolist(),
        'rhat': rhat,
        'names': param_names,
        'steps_final': steps,
        'nwalkers': nwalkers,
    }


# ---------------------------------------------------------------------------
# Bayesian evidence via dynesty
# ---------------------------------------------------------------------------

def nested_evidence(log_likelihood, prior_transform, ndim, *,
                    nlive=1000, seed=42):
    """Run dynesty static nested sampler.

    log_likelihood: callable(theta) -> float (NOT log prob, just log L)
    prior_transform: callable(u_cube) -> theta (maps [0,1]^ndim to parameter space)
    """
    import dynesty
    rstate = np.random.default_rng(seed)
    sampler = dynesty.NestedSampler(
        log_likelihood, prior_transform, ndim,
        nlive=nlive, rstate=rstate, sample='rwalk'
    )
    sampler.run_nested(print_progress=False, dlogz=0.01)
    res = sampler.results
    return {
        'logz': float(res.logz[-1]),
        'logz_err': float(res.logzerr[-1]),
        'niter': int(res.niter),
        'nlive': nlive,
    }


# ---------------------------------------------------------------------------
# DESI DR3 Fisher forecast
# ---------------------------------------------------------------------------

def dr3_fisher_forecast(E_func, Om, h, *, n_z=50, z_max=2.0,
                        sigma_DA_DR3=0.008, sigma_H_DR3=0.010):
    """Simple Fisher matrix on (w_0, w_a) from DESI DR3 projected precision.

    DR2 -> DR3 is expected ~2x improvement on w_a (DESI 2024 forecast).
    sigma_DA, sigma_H are fractional DR3 precisions on D_A(z) and H(z) at
    z ~ 0.5 (representative; we rescale (1+z) grid weights).

    Returns dict with sigma(w0), sigma(wa), correlation rho.
    """
    from scipy.integrate import cumulative_trapezoid
    z = np.linspace(0.01, z_max, n_z)
    c_mpc = 299792.458  # km/s

    # Fiducial (w0, wa) from CPL fit of the model
    w0_fid, wa_fid = cpl_fit(E_func, Om, z_lo=0.01, z_hi=1.2)

    # Build CPL background at (w0, wa)
    def _H_cpl(zv, w0, wa):
        f = (1.0 + zv) ** (3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * zv / (1.0 + zv))
        E2 = OMEGA_R * (1 + zv) ** 4 + Om * (1 + zv) ** 3 + (1.0 - Om - OMEGA_R) * f
        return (100.0 * h) * np.sqrt(E2)

    def _DA(zv, w0, wa):
        zg = np.linspace(0, zv, 512)
        integrand = c_mpc / _H_cpl(zg, w0, wa)
        d_c = np.trapezoid(integrand, zg)
        return d_c / (1.0 + zv)

    # Finite-difference partial derivatives at fiducial
    eps = 1e-4
    F = np.zeros((2, 2))
    for zi in z:
        DA_base = _DA(zi, w0_fid, wa_fid)
        H_base = _H_cpl(zi, w0_fid, wa_fid)
        DA_w0p = (_DA(zi, w0_fid + eps, wa_fid) - DA_base) / eps
        DA_wap = (_DA(zi, w0_fid, wa_fid + eps) - DA_base) / eps
        H_w0p = (_H_cpl(zi, w0_fid + eps, wa_fid) - H_base) / eps
        H_wap = (_H_cpl(zi, w0_fid, wa_fid + eps) - H_base) / eps
        sigma_DA_abs = sigma_DA_DR3 * DA_base
        sigma_H_abs = sigma_H_DR3 * H_base
        F[0, 0] += (DA_w0p / sigma_DA_abs) ** 2 + (H_w0p / sigma_H_abs) ** 2
        F[0, 1] += (DA_w0p * DA_wap / sigma_DA_abs ** 2
                    + H_w0p * H_wap / sigma_H_abs ** 2)
        F[1, 1] += (DA_wap / sigma_DA_abs) ** 2 + (H_wap / sigma_H_abs) ** 2
    F[1, 0] = F[0, 1]

    try:
        C = np.linalg.inv(F)
        s_w0 = float(np.sqrt(C[0, 0]))
        s_wa = float(np.sqrt(C[1, 1]))
        rho = float(C[0, 1] / (s_w0 * s_wa))
    except np.linalg.LinAlgError:
        s_w0 = s_wa = rho = float('nan')

    return {
        'w0_fid': w0_fid,
        'wa_fid': wa_fid,
        'sigma_w0': s_w0,
        'sigma_wa': s_wa,
        'rho': rho,
        'lcdm_sep_sigma': float(abs(wa_fid) / s_wa) if s_wa > 0 else 0.0,
    }


# ---------------------------------------------------------------------------
# JSON sanitizer (np.bool_/np.float_/np.ndarray)
# ---------------------------------------------------------------------------

def jsonify(obj):
    if isinstance(obj, dict):
        return {k: jsonify(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [jsonify(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    return obj


if __name__ == '__main__':
    print("L5 common smoke test")
    print(f"  LCDM chi2 = {LCDM_CHI2:.3f}")
    E = E_lcdm(LCDM_OM, LCDM_H)
    print(f"  S_8 LCDM = {s8_from_Efunc(E, LCDM_OM, LCDM_H):.4f}")
    print(f"  chi2_shear LCDM = {chi2_shear(E, LCDM_OM, LCDM_H):.3f}")
    f = dr3_fisher_forecast(E, LCDM_OM, LCDM_H)
    print(f"  DR3 Fisher LCDM: sigma(w_a)={f['sigma_wa']:.4f}")
