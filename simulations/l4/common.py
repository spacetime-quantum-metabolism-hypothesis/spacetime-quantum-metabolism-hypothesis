# -*- coding: utf-8 -*-
"""
L4 common utilities.

Reuses L3 data_loader (BAO+SN+CMB+RSD joint chi^2). Adds:
  * LCDM baseline (loaded from l3)
  * tight-box Nelder-Mead fitter (Omega_m, h, *theta)
  * direct CPL extraction (E^2(z) -> CPL E^2 via least_squares on z in [0.01, 1.2])
  * simple MCMC wrapper (emcee if available, else fall back to multivariate-normal
    Laplace from Hessian)
  * Cassini gamma-1 numerical check wrapper
"""
from __future__ import annotations

import io
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import numpy as np
from scipy.optimize import least_squares, minimize

_THIS = os.path.dirname(os.path.abspath(__file__))
_SIMS = os.path.dirname(_THIS)
for _p in (_SIMS, os.path.join(_SIMS, 'l3'), os.path.join(_SIMS, 'phase2')):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import config  # noqa: E402
from l3.data_loader import chi2_joint, get_data  # noqa: E402


# ---------------------------------------------------------------------------
# LCDM baseline reference
# ---------------------------------------------------------------------------

_LCDM_PATH = os.path.join(_SIMS, 'l3', 'lcdm_baseline.json')
with open(_LCDM_PATH, 'r', encoding='utf-8') as _f:
    LCDM_BASELINE = json.load(_f)
LCDM_CHI2 = float(LCDM_BASELINE['chi2_total'])
LCDM_OM = float(LCDM_BASELINE['Omega_m'])
LCDM_H = float(LCDM_BASELINE['h'])
OMEGA_R = float(getattr(config, 'Omega_r', 9.2e-5))


def E_lcdm(Om: float, h: float):
    OL = 1.0 - Om - OMEGA_R
    def E(z):
        z = np.asarray(z, dtype=float)
        return np.sqrt(OMEGA_R * (1 + z)**4 + Om * (1 + z)**3 + OL)
    return E


# ---------------------------------------------------------------------------
# Tight-box fit
# ---------------------------------------------------------------------------

def tight_fit(build_E, theta_bounds, theta0, *, seeds_extra=4, rng_seed=42):
    """Multi-start Nelder-Mead.  Returns dict with Om, h, theta, chi2 decomp.

    build_E(theta, Om, h) -> callable E(z).  Returning None triggers penalty.
    theta_bounds = list of (lo, hi) for each theta component.
    theta0 = fiducial theta.
    """
    full_bounds = [(0.28, 0.36), (0.64, 0.71)] + list(theta_bounds)
    lo = np.array([b[0] for b in full_bounds])
    hi = np.array([b[1] for b in full_bounds])

    def _clip(x):
        return np.clip(np.asarray(x, dtype=float), lo, hi)

    def total(x_raw):
        x = _clip(x_raw)
        pen = float(np.sum(np.maximum(0.0, np.asarray(x_raw) - hi)**2) +
                    np.sum(np.maximum(0.0, lo - np.asarray(x_raw))**2)) * 1e4
        Om, h = x[0], x[1]
        theta = list(x[2:])
        omega_b = 0.02237
        omega_c = Om * h * h - omega_b
        if omega_c <= 0:
            return 1e6 + pen
        try:
            E = build_E(theta, Om, h)
            if E is None:
                return 1e6 + pen
            e_hi = E(1100.0)
            if not np.isfinite(e_hi) or e_hi > 1e5 or e_hi < 1:
                return 1e6 + pen
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

    rng = np.random.default_rng(rng_seed)
    starts = [
        [0.3204, 0.6691] + list(theta0),
        [0.310, 0.680] + list(theta0),
        [0.325, 0.668] + list(theta0),
        [0.3153, 0.6736] + list(theta0),
    ]
    for _ in range(seeds_extra):
        theta_r = [rng.uniform(b[0], b[1]) for b in theta_bounds]
        starts.append([0.315, 0.6736] + theta_r)

    best = None
    for s in starts:
        try:
            r = minimize(total, s, method='Nelder-Mead',
                         options={'xatol': 1e-5, 'fatol': 1e-4,
                                  'maxiter': 1500, 'adaptive': True})
            if r.fun < 5e5:
                if best is None or r.fun < best.fun:
                    best = r
        except Exception:
            continue
    if best is None:
        return None

    x = _clip(best.x)
    Om, h = float(x[0]), float(x[1])
    theta = [float(t) for t in x[2:]]
    omega_b = 0.02237
    omega_c = Om * h * h - omega_b
    E = build_E(theta, Om, h)
    res = chi2_joint(E, rd=147.09, Omega_m=Om,
                     omega_b=omega_b, omega_c=omega_c, h=h,
                     H0_km=100.0 * h)
    return {
        'Om': Om, 'h': h, 'theta': theta,
        'chi2_bao': float(res['bao']),
        'chi2_sn': float(res['sn']),
        'chi2_cmb': float(res['cmb']),
        'chi2_rsd': float(res['rsd']),
        'chi2_total': float(res['total']),
        'E': E,
    }


# ---------------------------------------------------------------------------
# Direct CPL extraction  (window z in [0.01, 1.2])
# ---------------------------------------------------------------------------

def cpl_fit(E_func, Om, *, z_lo=0.01, z_hi=1.2, npts=120):
    """Least-squares fit of model E^2(z) to CPL E^2(z) over [z_lo, z_hi].
    Returns (w0, wa).
    """
    z = np.linspace(z_lo, z_hi, npts)
    Ez_model = np.asarray([float(E_func(zi)) for zi in z])
    E2_model = Ez_model**2
    OL0 = 1.0 - Om - OMEGA_R

    def resid(p):
        w0, wa = p
        f = (1.0 + z)**(3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * z / (1.0 + z))
        E2_cpl = OMEGA_R * (1 + z)**4 + Om * (1 + z)**3 + OL0 * f
        return (E2_cpl - E2_model)

    try:
        r = least_squares(resid, x0=[-1.0, 0.0],
                          bounds=([-2.0, -3.0], [-0.3, 3.0]),
                          max_nfev=400)
        return float(r.x[0]), float(r.x[1])
    except Exception:
        return -1.0, 0.0


def phantom_crossing(E_func, Om, *, z_max=2.0, n=200):
    """Detect w(z) crossing -1 on z in [0, z_max] via numerical derivative."""
    z = np.linspace(0.001, z_max, n)
    lna = -np.log1p(z)
    OL0 = 1.0 - Om - OMEGA_R
    try:
        E2 = np.array([float(E_func(zi))**2 for zi in z])
        rho_de = E2 - OMEGA_R * (1 + z)**4 - Om * (1 + z)**3
        if np.any(rho_de <= 0):
            return False  # bookkeeping artifact; caller should use direct CPL
        ln_rho = np.log(rho_de)
        dlnrho_dlna = np.gradient(ln_rho, lna)
        w = -1.0 - dlnrho_dlna / 3.0
        # Guard: require |w+1| > 1e-3 on both sides of crossing to suppress
        # numerical noise around LCDM (w identically -1).
        above = np.where(w + 1.0 > 1e-3)[0]
        below = np.where(w + 1.0 < -1e-3)[0]
        return bool(len(above) > 0 and len(below) > 0)
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Simple MCMC wrapper
# ---------------------------------------------------------------------------

def run_mcmc(log_prob, x0, param_names, *,
             nwalkers=64, nsteps=4000, nburn=1000, seed=42):
    """Run emcee if installed; otherwise Laplace approximation via finite-diff
    Hessian around x0.  Returns dict with samples, means, stds, R-hat estimate.
    """
    np.random.seed(seed)
    try:
        import emcee  # type: ignore
    except Exception:
        emcee = None

    ndim = len(x0)
    x0 = np.asarray(x0, dtype=float)

    if emcee is not None:
        p0 = x0 + 1e-3 * np.random.randn(nwalkers, ndim) * np.maximum(np.abs(x0), 1e-2)
        sampler = emcee.EnsembleSampler(nwalkers, ndim, log_prob)
        sampler.run_mcmc(p0, nsteps, progress=False)
        chain = sampler.get_chain(discard=nburn, thin=10, flat=True)
        means = chain.mean(axis=0)
        stds = chain.std(axis=0)
        # crude R-hat using walker splits
        full = sampler.get_chain(discard=nburn)  # (steps, walkers, ndim)
        rhat = []
        for d in range(ndim):
            w_means = full[:, :, d].mean(axis=0)
            w_vars = full[:, :, d].var(axis=0)
            B = w_means.var() * full.shape[0]
            W = w_vars.mean()
            var_hat = (1.0 - 1.0 / full.shape[0]) * W + B / full.shape[0]
            rhat.append(float(np.sqrt(var_hat / max(W, 1e-30))))
        return {
            'backend': 'emcee',
            'samples': chain,
            'means': means.tolist(),
            'stds': stds.tolist(),
            'rhat': rhat,
            'names': param_names,
        }

    # Laplace fallback
    lp0 = log_prob(x0)
    H = np.zeros((ndim, ndim))
    eps = np.maximum(1e-3 * np.abs(x0), 1e-4)
    for i in range(ndim):
        for j in range(i, ndim):
            xp = x0.copy(); xm = x0.copy()
            xp[i] += eps[i]; xm[i] -= eps[i]
            if i == j:
                H[i, i] = (log_prob(xp) - 2 * lp0 + log_prob(xm)) / (eps[i]**2)
            else:
                xpp = x0.copy(); xpp[i] += eps[i]; xpp[j] += eps[j]
                xpm = x0.copy(); xpm[i] += eps[i]; xpm[j] -= eps[j]
                xmp = x0.copy(); xmp[i] -= eps[i]; xmp[j] += eps[j]
                xmm = x0.copy(); xmm[i] -= eps[i]; xmm[j] -= eps[j]
                H[i, j] = (log_prob(xpp) - log_prob(xpm) - log_prob(xmp)
                           + log_prob(xmm)) / (4 * eps[i] * eps[j])
                H[j, i] = H[i, j]
    try:
        cov = np.linalg.inv(-H)
        if not np.all(np.isfinite(cov)):
            raise ValueError
        cov = 0.5 * (cov + cov.T)
        w, V = np.linalg.eigh(cov)
        w = np.clip(w, 1e-14, None)
        cov = V @ np.diag(w) @ V.T
        samples = np.random.multivariate_normal(x0, cov, size=4000)
        return {
            'backend': 'laplace',
            'samples': samples,
            'means': x0.tolist(),
            'stds': np.sqrt(np.diag(cov)).tolist(),
            'rhat': [1.0] * ndim,
            'names': param_names,
        }
    except Exception:
        return {
            'backend': 'failed',
            'samples': np.tile(x0, (1, 1)),
            'means': x0.tolist(),
            'stds': [0.0] * ndim,
            'rhat': [np.nan] * ndim,
            'names': param_names,
        }


# ---------------------------------------------------------------------------
# Linear growth (LCDM reference + optional mu(a,k))
# ---------------------------------------------------------------------------

def growth_fs8(E_func, Om, *, mu_func=None, sigma8_0=0.811):
    """fsigma_8 at the 8 RSD redshifts using ODE d'' + (2 + H'/H) d' - (3/2) Om_m mu d = 0.

    mu_func(a) -> G_eff/G. If None, assumes LCDM (mu=1). Returns array
    matching rsd_z ordering.
    """
    d = get_data()
    z_obs = d.rsd_z

    from scipy.integrate import solve_ivp
    a_ini = 1e-3
    a_end = 1.0

    def rhs(a, y):
        D, Dp = y
        z = 1.0 / a - 1.0
        E = float(E_func(z))
        # dlnE/dlna via finite diff
        da = 1e-4 * a
        E_p = float(E_func(1.0 / (a + da) - 1.0))
        E_m = float(E_func(1.0 / (a - da) - 1.0))
        dlnE_dlna = (np.log(E_p) - np.log(E_m)) / (2 * da / a)
        Om_m_a = Om * a**(-3) / E**2
        mu = 1.0 if mu_func is None else float(mu_func(a))
        Dpp = -(3.0 + dlnE_dlna) / a * Dp + 1.5 * Om_m_a * mu * D / a**2
        return [Dp, Dpp]

    sol = solve_ivp(rhs, (a_ini, a_end), [a_ini, 1.0], method='RK45',
                    dense_output=True, rtol=1e-7, atol=1e-9, max_step=0.02)
    if not sol.success:
        return np.full_like(z_obs, np.nan)

    def D(a):
        return float(sol.sol(a)[0])
    def Dp(a):
        return float(sol.sol(a)[1])

    D0 = D(1.0)
    sigma8 = sigma8_0 * (D(1.0) / D0)  # identically sigma8_0

    fs8 = np.zeros_like(z_obs)
    for i, z in enumerate(z_obs):
        a = 1.0 / (1.0 + z)
        f = a * Dp(a) / D(a)
        fs8[i] = f * sigma8_0 * D(a) / D0
    return fs8


# ---------------------------------------------------------------------------
# Cassini gamma-1 numerical spec (placeholder — analytic per-model)
# ---------------------------------------------------------------------------

def cassini_ok(gamma_minus_one: float) -> bool:
    return abs(gamma_minus_one) < 2.3e-5


if __name__ == '__main__':
    print(f"L4 common smoke test")
    print(f"  LCDM baseline chi2 = {LCDM_CHI2:.3f}")
    print(f"  Omega_m={LCDM_OM:.4f}, h={LCDM_H:.4f}")
    E = E_lcdm(LCDM_OM, LCDM_H)
    w0, wa = cpl_fit(E, LCDM_OM)
    print(f"  LCDM CPL: w0={w0:.4f}, wa={wa:.4f}")
    pc = phantom_crossing(E, LCDM_OM)
    print(f"  phantom cross: {pc}")
    fs8 = growth_fs8(E, LCDM_OM)
    print(f"  fs8 (LCDM): {fs8}")
