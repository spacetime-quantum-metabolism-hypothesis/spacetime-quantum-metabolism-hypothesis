# -*- coding: utf-8 -*-
"""
l44_test.py -- L44: Model UB (Boundary Inflow + Ballistic Diffusion)
=====================================================================
Final SQT cosmological test.

Physical model: Dark energy arises from ballistic diffusion of SQT field
psi inward from a cosmic boundary R(z) = c/H(z).

Ballistic profile (dimensionless, s = r/R, mR = mu*R = muR0):
  f(s; mR) = [(1-s + 1/mR)*exp(-mR*(1-s)) - (1+s + 1/mR)*exp(-mR*(1+s))]
             / (2 * mR * s)
  f(0; mR) = exp(-mR)   [L'Hopital limit]

Path-averaged field (dimensionless):
  I(q) = integral_0^q f(s; mR) ds
  F_avg(z) = I(min(chi*E, 1)) / (chi*E)   where chi = integral_0^z dz'/E(z')

Dark energy density (self-consistent):
  rho_DE(z) = OL0 * F_avg(z) / exp(-muR0)    [normalized: rho_DE(0) = OL0]

Natural scale: muR0 = mu*R ~ 1 (boundary at ~1 Hubble radius, absorption ~1)

Models:
  LCDM   (k=2)  -- baseline
  CPL    (k=4)  -- reference (L43 confirmed dAICc=-107.02)
  UB2    (k=2)  -- Om, H0; muR0=1.0 fixed
  UB3    (k=3)  -- Om, H0, muR0 free

Tasks:
  Pre-Task: Profile validation (f(s;mR) plots, f(0)=exp(-mR) check)
  Task 0:   Baselines (LCDM + CPL -- confirm L43 AICc values)
  Task 1:   UB2 fit (k=2, muR0=1.0)
  Task 2:   UB3 fit (k=3, muR0 free)
  Task 3:   muR0 sensitivity scan (1D grid)
  Task 4:   E(z) shape comparison plot
  Task 5:   F_avg(z) + rho_DE(z) diagnostic plot
  Task 6:   Convergence diagnostics
  Task 7:   w(z) visualization
  Task 8:   Bootstrap (best UB model, N=200)
  Task 9:   w0-wa plane
  Task 10:  q0 comparison + L44 final verdict

DESY5SN_AgeCorr BUG FIX from L43:
  L43 BUG:  cov_raw = np.linalg.inv(self.cov_inv)  [triple 1829x1829 inversion]
  L44 FIX:  cov_raw = self.cov                      [base class forward covariance]
"""

import os, sys, time, json, warnings
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import minimize
from scipy.interpolate import interp1d
import multiprocessing as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')
np.seterr(all='ignore')
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_L35_DIR    = os.path.join(_SCRIPT_DIR, '../l35')
for _p in [os.path.dirname(_SCRIPT_DIR), _L35_DIR]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from l35_test import (
    chi2_bao, chi2_cmb, chi2_rsd,
    chi2_sn as chi2_sn_raw,
    get_sn, E_lcdm,
    OR, C_KMS, N_TOTAL,
    cpl_wa,
    Z_RSD, FS8_OBS, FS8_SIG,
    CMB_OBS, CMB_SIG,
    R_S, N_GRID,
    DESI_DR2, DESI_DR2_COV_INV,
)
from phase2.sn_likelihood import DESY5SN

# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────
LCDM_AICC_L43 = 1759.93   # L43 corrected-data LCDM AICc (target for Task 0)
CPL_AICC_L43  = 1652.91   # L43 CPL AICc (reference)
CPL_W0_L43    = -0.448
CPL_WA_L43    = -1.467

N_WORKERS  = 8
N_BOOT     = 200

# Son et al. 2025 age correction parameters (same as L43)
SON_SLOPE     = 0.030
SON_SLOPE_ERR = 0.004
SON_DAGE_AMP  = 5.3
SON_DAGE_TAU  = 2.5
SON_W0        = -0.34
SON_WA        = -1.90
SON_Q0        = +0.18
SON_W0_2SIG   = 0.12
SON_WA_2SIG   = 0.50

# Dense z-grid for self-consistent UB E(z)
UB_Z_GRID = np.concatenate([
    np.linspace(0.0, 3.5, 2000),
    np.linspace(3.5, 1200.0, 600)[1:],
])

N_UB_S = 2000   # s-grid resolution for ballistic integral I(q)
UB2_MUR0 = 1.0  # fixed muR0 for UB2 (natural scale)

# ──────────────────────────────────────────────────────────────────────────────
# Son et al. 2025 age-bias correction
# ──────────────────────────────────────────────────────────────────────────────
def son_age_correction(z):
    delta_age   = SON_DAGE_AMP * (1.0 - np.exp(-SON_DAGE_TAU * z))
    delta_m     = delta_age * SON_SLOPE
    sigma_extra = delta_age * SON_SLOPE_ERR
    return delta_m, sigma_extra


class DESY5SN_AgeCorr(DESY5SN):
    """DESY5SN with Son et al. 2025 age-bias correction (L44 bug-fixed version)."""

    def __init__(self):
        super().__init__()
        delta_m, sigma_extra = son_age_correction(self.z_hd)
        self.mu_obs = self.mu_obs - delta_m

        # BUG FIX from L43: use self.cov (forward covariance) directly,
        # not np.linalg.inv(self.cov_inv) which causes triple 1829x1829 inversion
        cov_corr     = self.cov + np.diag(sigma_extra**2)
        self.cov     = cov_corr
        self.cov_inv = np.linalg.inv(cov_corr)

        ones             = np.ones(self.N)
        self._C_inv_1    = self.cov_inv @ ones
        self._one_Cinv_1 = float(ones @ self._C_inv_1)


_SN_CORR = None
def get_sn_corr():
    global _SN_CORR
    if _SN_CORR is None:
        _SN_CORR = DESY5SN_AgeCorr()
    return _SN_CORR


def chi2_sn_corr(E_fn, Om, H0):
    def _E(z):
        v = E_fn(np.array([float(z)]), Om)
        return 1e30 if (v is None or not np.isfinite(v[0])) else float(v[0])
    return get_sn_corr().chi2(_E, H0_km=H0)


def _chi2_all(E_fn, Om, H0):
    cb = chi2_bao(E_fn, Om, H0)
    cc = chi2_cmb(E_fn, Om, H0)
    cs = chi2_sn_corr(E_fn, Om, H0)
    cr = chi2_rsd(E_fn, Om, H0)
    return cb, cc, cs, cr, cb + cc + cs + cr


# ──────────────────────────────────────────────────────────────────────────────
# Utilities
# ──────────────────────────────────────────────────────────────────────────────
def _at_boundary(params, bounds, tol=1e-3):
    for p, (lo, hi) in zip(params, bounds):
        span = hi - lo
        if span == 0:
            continue
        if abs(p - lo) < tol * span or abs(p - hi) < tol * span:
            return True
    return False


def _aicc(chi2_val, k):
    return chi2_val + 2*k + 2*k*(k+1) / (N_TOTAL - k - 1)


def _verdict(daicc, boundary=False, k2=False):
    if boundary:      return 'K92 INVALID'
    if daicc >= 0:    return 'K90 KILL'
    if daicc >= -2:   return 'Q90 PASS'
    if daicc >= -4:   return 'Q91 STRONG'
    if daicc >= -10:
        return 'Q92 GAME' if k2 else 'Q91 STRONG'
    if daicc >= -15:
        return 'Q93 TRIUMPH' if k2 else 'Q92 GAME'
    return 'Q94 DISCOVERY' if k2 else 'Q93 TRIUMPH'


def _jsonify(obj):
    if isinstance(obj, dict):        return {k: _jsonify(v) for k, v in obj.items()}
    if isinstance(obj, list):        return [_jsonify(v) for v in obj]
    if isinstance(obj, np.ndarray):  return _jsonify(obj.tolist())
    if isinstance(obj, bool):        return bool(obj)
    if isinstance(obj, np.integer):  return int(obj)
    if isinstance(obj, (np.floating, float)):
        f = float(obj)
        return None if not np.isfinite(f) else f
    return obj


def _q0(Om, w0_eff):
    OL0 = 1.0 - Om - OR
    return 0.5 * (Om + (1.0 + 3.0*w0_eff) * OL0)


def _bao_theory_vec(E_fn, Om, H0):
    from l35_test import DESI_DR2 as _D2, N_GRID as _NG
    z_eff  = _D2['z_eff']
    z_grid = np.linspace(0.0, z_eff.max() + 0.01, _NG)
    Eg = E_fn(z_grid, Om)
    if Eg is None or not np.all(np.isfinite(Eg)):
        return None
    Eg = np.maximum(Eg, 1e-15)
    DM = (C_KMS / H0) * np.concatenate([[0.],
           cumulative_trapezoid(1.0 / Eg, z_grid)])
    tv = np.empty(13)
    for i, (z, qty) in enumerate(zip(z_eff, _D2['quantity'])):
        idx = min(np.searchsorted(z_grid, z), _NG - 1)
        DH  = C_KMS / (H0 * Eg[idx])
        DV  = (z * DM[idx]**2 * DH)**(1./3.) if z > 0 else 0.
        if   'DV' in qty: tv[i] = DV / R_S
        elif 'DM' in qty: tv[i] = DM[idx] / R_S
        elif 'DH' in qty: tv[i] = DH / R_S
        else:              tv[i] = np.nan
    return None if not np.all(np.isfinite(tv)) else tv


# ──────────────────────────────────────────────────────────────────────────────
# Model UB: Ballistic diffusion profile
# ──────────────────────────────────────────────────────────────────────────────
def _f_ballistic(s_arr, mR):
    """
    Dimensionless ballistic profile f(s; mR).
    s = r/R, mR = mu*R = muR0 (const along trajectory).
    f(0; mR) = exp(-mR)  [L'Hopital limit, exact]
    """
    s_arr = np.asarray(s_arr, dtype=float)
    result = np.empty_like(s_arr)

    mask0 = s_arr < 1e-9
    result[mask0] = np.exp(-mR)

    sm = ~mask0
    sv = s_arr[sm]
    term1 = ((1.0 - sv) + 1.0/mR) * np.exp(-mR * (1.0 - sv))
    term2 = ((1.0 + sv) + 1.0/mR) * np.exp(-mR * (1.0 + sv))
    result[sm] = (term1 - term2) / (2.0 * mR * sv)

    return result


def _build_I_interp(muR0):
    """
    Build I(q) = integral_0^q f(s; muR0) ds, returned as interp1d on [0,1].
    """
    s_grid = np.concatenate([[0.0], np.linspace(1e-9, 1.0, N_UB_S)])
    f_grid = _f_ballistic(s_grid, muR0)
    I_grid = np.concatenate([[0.0], cumulative_trapezoid(f_grid, s_grid)])
    return interp1d(s_grid, I_grid, kind='linear',
                    bounds_error=False, fill_value=(0.0, float(I_grid[-1])))


def _compute_E_UB(z_arr, Om, muR0, max_iter=30, tol=1e-7):
    """
    Self-consistent Friedmann iteration for Model UB.

    rho_DE(z) = OL0 * F_avg(z) / F0
    F_avg(z)  = I(min(chi*E, 1)) / (chi*E)    [chi*E > 0]
    F_avg(0)  = F0 = exp(-muR0)                [L'Hopital]
    chi(z)    = integral_0^z dz'/E(z')          [dimensionless comoving distance]

    Normalization: rho_DE(0) = OL0, E(0) = 1 exact.
    """
    OL0 = 1.0 - Om - OR
    if OL0 <= 0.0 or Om <= 0.0 or muR0 <= 0.0:
        return None

    F0 = np.exp(-muR0)
    if F0 <= 0.0:
        return None

    I_interp = _build_I_interp(muR0)

    # Initial guess: LCDM-like
    E_prev = np.sqrt(np.maximum(
        OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0, 1e-30))

    for _ in range(max_iter):
        # chi(z) = integral_0^z dz'/E
        chi = np.concatenate([[0.0],
              cumulative_trapezoid(1.0 / E_prev, z_arr)])

        # q(z) = min(chi * E, 1)
        chiE = chi * E_prev
        q    = np.minimum(chiE, 1.0)

        # F_avg(z): handle chi*E -> 0 limit at z=0
        I_q   = I_interp(q)
        mask  = chiE > 1e-10
        F_avg = np.where(mask, I_q / chiE, F0)

        # rho_DE and E^2
        rho_DE = OL0 * F_avg / F0
        E2     = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 <= 0) or np.any(~np.isfinite(E2)):
            return None
        E_new = np.sqrt(E2)

        # Normalize E(0) = 1 (should be ~1 by construction, safety step)
        E0 = E_new[0]
        if E0 <= 0.0 or not np.isfinite(E0):
            return None
        E_new = E_new / E0

        if np.max(np.abs(E_new - E_prev)) < tol:
            return E_new
        E_prev = E_new

    # Did not converge -- return last iterate if finite
    if np.all(np.isfinite(E_prev)) and np.all(E_prev > 0):
        return E_prev
    return None


def _make_E_UB(Om, muR0):
    """Precompute UB E(z) on dense grid; return interpolant fn(z, _Om)."""
    E_arr = _compute_E_UB(UB_Z_GRID, Om, muR0)
    if E_arr is None:
        return None
    ifn = interp1d(UB_Z_GRID, E_arr, kind='linear',
                   bounds_error=False, fill_value=np.nan)
    def fn(z, _Om):
        za = np.atleast_1d(np.asarray(z, float))
        Ev = ifn(za)
        return None if (np.any(np.isnan(Ev)) or np.any(Ev <= 0)) else Ev
    return fn


def _make_E_cpl(Om, w0, wa):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    def fn(z_arr, _Om):
        za  = np.asarray(z_arr, float)
        cpl = (1.0+za)**(3.0*(1.0+w0+wa)) * np.exp(-3.0*wa*za/(1.0+za))
        rde = OL0 * cpl
        E2  = OR*(1+za)**4 + Om*(1+za)**3 + rde
        return None if np.any(E2 <= 0) else np.sqrt(E2)
    return fn


# ──────────────────────────────────────────────────────────────────────────────
# Parameter bounds
# ──────────────────────────────────────────────────────────────────────────────
_BND_LCDM = [(0.20, 0.55), (55., 82.)]
_BND_CPL  = [(0.20, 0.55), (55., 82.), (-3.0, 0.5), (-5.0, 3.0)]
_BND_UB2  = [(0.20, 0.55), (55., 82.)]
_BND_UB3  = [(0.20, 0.55), (55., 82.), (0.05, 15.0)]


# ──────────────────────────────────────────────────────────────────────────────
# Workers (module-level for spawn-safe pickling)
# ──────────────────────────────────────────────────────────────────────────────

def _worker_lcdm(start):
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    def obj(p):
        Om, H0 = p
        if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
            return 1e9
        fn = lambda z, _: E_lcdm(z, Om)
        cb, cc, cs, cr, tot = _chi2_all(fn, Om, H0)
        return tot if np.isfinite(tot) else 1e9
    try:
        r = minimize(obj, start, method='Nelder-Mead',
                     options={'xatol': 1e-5, 'fatol': 1e-5, 'maxiter': 800})
        return (float(r.fun), [float(x) for x in r.x])
    except Exception:
        return (1e9, None)


def _worker_cpl(start):
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    def obj(p):
        Om, H0, w0, wa = p
        if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
            return 1e9
        if w0 < -3.0 or w0 > 0.5 or wa < -5.0 or wa > 3.0:
            return 1e9
        fn = _make_E_cpl(Om, w0, wa)
        if fn is None:
            return 1e9
        cb, cc, cs, cr, tot = _chi2_all(fn, Om, H0)
        return tot if np.isfinite(tot) else 1e9
    try:
        r = minimize(obj, start, method='Nelder-Mead',
                     options={'xatol': 1e-4, 'fatol': 1e-4, 'maxiter': 800})
        return (float(r.fun), [float(x) for x in r.x])
    except Exception:
        return (1e9, None)


def _worker_ub2(start):
    """UB2: Om, H0; muR0=1.0 fixed; k=2."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    def obj(p):
        Om, H0 = p
        if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
            return 1e9
        fn = _make_E_UB(Om, UB2_MUR0)
        if fn is None:
            return 1e9
        cb, cc, cs, cr, tot = _chi2_all(fn, Om, H0)
        return tot if np.isfinite(tot) else 1e9
    try:
        r = minimize(obj, start, method='Nelder-Mead',
                     options={'xatol': 1e-5, 'fatol': 1e-5, 'maxiter': 800})
        return (float(r.fun), [float(x) for x in r.x])
    except Exception:
        return (1e9, None)


def _worker_ub3(start):
    """UB3: Om, H0, muR0; k=3."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    def obj(p):
        Om, H0, muR0 = p
        if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
            return 1e9
        if muR0 < 0.05 or muR0 > 15.0:
            return 1e9
        fn = _make_E_UB(Om, muR0)
        if fn is None:
            return 1e9
        cb, cc, cs, cr, tot = _chi2_all(fn, Om, H0)
        return tot if np.isfinite(tot) else 1e9
    try:
        r = minimize(obj, start, method='Nelder-Mead',
                     options={'xatol': 1e-4, 'fatol': 1e-4, 'maxiter': 1000})
        return (float(r.fun), [float(x) for x in r.x])
    except Exception:
        return (1e9, None)


def _worker_mur0_scan(args):
    """1D muR0 scan: optimize Om, H0 for fixed muR0."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    muR0, starts = args
    best_chi2 = 1e9
    best_par  = None
    for s0 in starts:
        def obj(p):
            Om, H0 = p
            if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
                return 1e9
            fn = _make_E_UB(Om, muR0)
            if fn is None:
                return 1e9
            cb, cc, cs, cr, tot = _chi2_all(fn, Om, H0)
            return tot if np.isfinite(tot) else 1e9
        try:
            r = minimize(obj, s0, method='Nelder-Mead',
                         options={'xatol': 1e-4, 'fatol': 1e-4, 'maxiter': 400})
            if r.fun < best_chi2:
                best_chi2 = float(r.fun)
                best_par  = [float(x) for x in r.x]
        except Exception:
            pass
    return (muR0, best_chi2, best_par)


def _best_of(results):
    valid = [(c, p) for c, p in results if p is not None and np.isfinite(c) and c < 1e8]
    if not valid:
        return 1e9, None
    return min(valid, key=lambda x: x[0])


def _make_starts_2d(n_rand, rng, extra=None):
    starts = []
    for Om0 in [0.27, 0.29, 0.31, 0.33, 0.35]:
        for H0_0 in [64., 66., 68., 70., 72.]:
            starts.append([Om0, H0_0])
    for _ in range(n_rand):
        starts.append([rng.uniform(0.22, 0.50), rng.uniform(58., 78.)])
    if extra:
        starts.extend(extra)
    return starts


# ──────────────────────────────────────────────────────────────────────────────
# Pre-Task: Ballistic profile validation
# ──────────────────────────────────────────────────────────────────────────────
def pretask_validate(out_dir):
    print('\n' + '='*60)
    print('Pre-Task: Ballistic profile validation')
    print('='*60)

    # Verify f(0; mR) = exp(-mR) for several mR values
    print('  f(0; mR) vs exp(-mR) check:')
    for mR in [0.5, 1.0, 2.0, 5.0]:
        f0_formula = float(_f_ballistic(np.array([0.0]), mR))
        f0_exact   = np.exp(-mR)
        err = abs(f0_formula - f0_exact) / f0_exact
        print(f'  mR={mR:.1f}: f(0)={f0_formula:.6f}  exp(-mR)={f0_exact:.6f}'
              f'  rel_err={err:.2e}  [{"OK" if err < 1e-4 else "FAIL"}]')

    # Verify F_avg(0) = exp(-muR0) = F0
    print()
    print('  F_avg(0) = exp(-muR0) check:')
    for muR0 in [0.5, 1.0, 2.0]:
        F0 = np.exp(-muR0)
        E_arr = _compute_E_UB(UB_Z_GRID, 0.30, muR0)
        if E_arr is not None:
            print(f'  muR0={muR0:.1f}: E(0)={E_arr[0]:.6f} [should be 1.0]', end='')
            I_interp = _build_I_interp(muR0)
            chi0 = 0.0
            chiE0 = chi0 * E_arr[0]
            F_avg_0 = F0  # by construction
            rho_DE_0 = 0.30 * 0 + OR  # wrong -- just check E(0)
            print(f'  [{"OK" if abs(E_arr[0] - 1.0) < 1e-6 else "FAIL"}]')
        else:
            print(f'  muR0={muR0:.1f}: E_UB failed')

    # Plot f(s; mR) profiles
    s_plot = np.linspace(0, 1, 500)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    ax = axes[0]
    for mR in [0.3, 0.5, 1.0, 2.0, 5.0]:
        f_vals = _f_ballistic(s_plot, mR)
        ax.plot(s_plot, f_vals, label=f'mR={mR}')
    ax.set_xlabel('s = r/R')
    ax.set_ylabel('f(s; mR)')
    ax.set_title('Ballistic diffusion profile')
    ax.legend(fontsize=8)
    ax.set_ylim(bottom=0)
    ax.grid(alpha=0.3)

    # Plot I(q) for several muR0
    ax2 = axes[1]
    q_plot = np.linspace(0, 1, 500)
    for muR0 in [0.3, 0.5, 1.0, 2.0, 5.0]:
        I_fn = _build_I_interp(muR0)
        I_vals = I_fn(q_plot)
        F_avg_vals = np.where(q_plot > 1e-10,
                              I_vals / q_plot, np.exp(-muR0))
        ax2.plot(q_plot, F_avg_vals / np.exp(-muR0),
                 label=f'muR0={muR0}')
    ax2.axhline(1.0, color='k', ls='--', lw=0.8, alpha=0.5)
    ax2.set_xlabel('q = min(chi*E, 1)')
    ax2.set_ylabel('F_avg(q) / exp(-muR0)')
    ax2.set_title('Normalized path-averaged field')
    ax2.legend(fontsize=8)
    ax2.grid(alpha=0.3)

    fig.tight_layout()
    out = os.path.join(out_dir, 'l44_pretask_profile.png')
    fig.savefig(out, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f'\n  Profile plot: {out}')
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 0: Baselines (LCDM + CPL, must match L43)
# ──────────────────────────────────────────────────────────────────────────────
def task0_baselines(pool):
    print('\n' + '='*60)
    print('Task 0: Baselines (confirm L43 corrected-data AICc)')
    print('='*60)
    t0 = time.time()
    rng = np.random.default_rng(0)

    print('  Warming corrected SN cache...')
    get_sn_corr()
    print('  SN_corr ready.')
    sys.stdout.flush()

    starts_lcdm = _make_starts_2d(10, rng,
                                   extra=[[0.32, 67.5], [0.31, 68.0], [0.33, 67.0]])
    starts_cpl = []
    for Om0 in [0.28, 0.30, 0.32, 0.36]:
        for H0_0 in [63., 67., 70.]:
            for w0_0 in [-0.45, -0.80, -0.34]:
                for wa_0 in [-1.5, -2.0, -0.5]:
                    starts_cpl.append([Om0, H0_0, w0_0, wa_0])
    starts_cpl += [[0.36, 63., -0.45, -1.47], [0.31, 68., -0.34, -1.90],
                   [0.35, 64., -0.40, -1.60]]

    print(f'  LCDM: {len(starts_lcdm)} starts')
    print(f'  CPL:  {len(starts_cpl)} starts')
    sys.stdout.flush()

    res_lcdm = pool.map(_worker_lcdm, starts_lcdm)
    res_cpl  = pool.map(_worker_cpl,  starts_cpl)

    chi2_lcdm, par_lcdm = _best_of(res_lcdm)
    Om_l = par_lcdm[0] if par_lcdm else 0.3236
    H0_l = par_lcdm[1] if par_lcdm else 67.52
    aicc_lcdm = _aicc(chi2_lcdm, 2)

    fn_l = lambda z, _: E_lcdm(z, Om_l)
    cb_l, cc_l, cs_l, cr_l, _ = _chi2_all(fn_l, Om_l, H0_l)
    print(f'\n  LCDM: Om={Om_l:.4f}, H0={H0_l:.4f}')
    print(f'  chi2: BAO={cb_l:.4f} CMB={cc_l:.4f} SN={cs_l:.4f} RSD={cr_l:.4f}')
    delta_lcdm = aicc_lcdm - LCDM_AICC_L43
    print(f'  AICc={aicc_lcdm:.4f}  L43_ref={LCDM_AICC_L43:.2f}  '
          f'delta={delta_lcdm:+.2f}  [{"OK" if abs(delta_lcdm) < 2 else "CHECK"}]')

    chi2_cpl, par_cpl = _best_of(res_cpl)
    if par_cpl:
        Om_c, H0_c, w0_c, wa_c = par_cpl
    else:
        Om_c, H0_c, w0_c, wa_c = None, None, None, None
    aicc_cpl    = _aicc(chi2_cpl, 4)
    daicc_cpl   = aicc_cpl - aicc_lcdm

    if par_cpl:
        fn_c = _make_E_cpl(Om_c, w0_c, wa_c)
        cb_c, cc_c, cs_c, cr_c, _ = _chi2_all(fn_c, Om_c, H0_c)
        print(f'\n  CPL: Om={Om_c:.4f}, H0={H0_c:.4f}, w0={w0_c:.4f}, wa={wa_c:.4f}')
        print(f'  chi2: BAO={cb_c:.4f} CMB={cc_c:.4f} SN={cs_c:.4f} RSD={cr_c:.4f}')
        delta_cpl = aicc_cpl - CPL_AICC_L43
        print(f'  AICc={aicc_cpl:.4f}  dAICc(vs LCDM)={daicc_cpl:.2f}')
        print(f'  L43_ref={CPL_AICC_L43:.2f}  delta={delta_cpl:+.2f}  '
              f'[{"OK" if abs(delta_cpl) < 2 else "CHECK"}]')
    else:
        print('  CPL: fit failed')

    elapsed = time.time() - t0
    print(f'  Elapsed: {elapsed:.1f}s')
    sys.stdout.flush()

    return {
        'lcdm': {'Om': Om_l, 'H0': H0_l, 'chi2': chi2_lcdm, 'aicc': aicc_lcdm,
                 'chi2_bao': cb_l, 'chi2_cmb': cc_l, 'chi2_sn': cs_l, 'chi2_rsd': cr_l},
        'cpl':  {'Om': Om_c, 'H0': H0_c, 'w0': w0_c, 'wa': wa_c,
                 'chi2': chi2_cpl, 'aicc': aicc_cpl, 'daicc_vs_lcdm': daicc_cpl,
                 'params': par_cpl},
        'lcdm_aicc': aicc_lcdm,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Tasks 1-2: UB model fits
# ──────────────────────────────────────────────────────────────────────────────
def tasks1to2_ub_fits(pool):
    print('\n' + '='*60)
    print('Tasks 1-2: UB model fits (parallel pool)')
    print('='*60)
    t0 = time.time()
    rng = np.random.default_rng(42)

    # UB2 starts (k=2): Om, H0
    starts_ub2 = _make_starts_2d(10, rng,
                                  extra=[[0.32, 67.5], [0.31, 68.0], [0.36, 63.5]])
    for _ in range(5):
        starts_ub2.append([rng.uniform(0.25, 0.45), rng.uniform(60., 76.)])

    # UB3 starts (k=3): Om, H0, muR0
    starts_ub3 = []
    for Om0 in [0.28, 0.30, 0.32, 0.34, 0.36]:
        for H0_0 in [63., 66., 69., 72.]:
            for mR0 in [0.3, 0.5, 1.0, 2.0, 4.0, 8.0]:
                starts_ub3.append([Om0, H0_0, mR0])
    starts_ub3 += [[0.32, 67.5, 1.0], [0.36, 63.5, 0.5], [0.30, 68., 2.0]]
    for _ in range(20):
        starts_ub3.append([rng.uniform(0.25, 0.45), rng.uniform(60., 76.),
                           rng.uniform(0.1, 12.0)])

    print(f'  UB2: {len(starts_ub2)} starts  (muR0=1.0 fixed, k=2)')
    print(f'  UB3: {len(starts_ub3)} starts  (muR0 free, k=3)')
    sys.stdout.flush()

    res_ub2 = pool.map(_worker_ub2, starts_ub2)
    res_ub3 = pool.map(_worker_ub3, starts_ub3)

    elapsed = time.time() - t0
    print(f'  UB fits done in {elapsed:.1f}s')
    sys.stdout.flush()

    return {
        'ub2': _best_of(res_ub2),
        'ub3': _best_of(res_ub3),
    }


# ──────────────────────────────────────────────────────────────────────────────
# Task 3: muR0 sensitivity scan
# ──────────────────────────────────────────────────────────────────────────────
def task3_mur0_scan(pool, lcdm_aicc):
    print('\n' + '='*60)
    print('Task 3: muR0 sensitivity scan')
    print('='*60)
    t0 = time.time()
    rng = np.random.default_rng(77)

    mur0_grid = np.concatenate([
        np.linspace(0.1, 1.0, 10),
        np.linspace(1.0, 5.0, 10)[1:],
        np.linspace(5.0, 15.0, 5)[1:],
    ])

    scan_args = []
    for muR0 in mur0_grid:
        starts = [[0.32, 67.5], [0.30, 68.0], [0.36, 63.5]]
        for _ in range(3):
            starts.append([rng.uniform(0.27, 0.42), rng.uniform(62., 76.)])
        scan_args.append((float(muR0), starts))

    results_raw = pool.map(_worker_mur0_scan, scan_args)

    print(f'\n  muR0  |  dAICc(vs LCDM)  |  Om     H0')
    print('  ' + '-'*45)
    scan_results = []
    for muR0, chi2, par in results_raw:
        if par is not None and np.isfinite(chi2) and chi2 < 1e8:
            aicc  = _aicc(chi2, 2)
            daicc = aicc - lcdm_aicc
            print(f'  {muR0:5.2f}  |  {daicc:+10.2f}      |  '
                  f'{par[0]:.4f}  {par[1]:.4f}')
            scan_results.append({'muR0': muR0, 'chi2': chi2,
                                 'aicc': aicc, 'daicc': daicc,
                                 'Om': par[0], 'H0': par[1]})
        else:
            print(f'  {muR0:5.2f}  |  FAILED')

    elapsed = time.time() - t0
    print(f'  Scan done in {elapsed:.1f}s')
    sys.stdout.flush()
    return scan_results


# ──────────────────────────────────────────────────────────────────────────────
# Report single model
# ──────────────────────────────────────────────────────────────────────────────
def _report_ub(tag, label, k, bounds, best_chi2, best_params, lcdm_aicc, cpl_result):
    print('\n' + '='*60)
    print(f'Task: {label} (k={k})')
    print('='*60)

    if best_params is None:
        print('  FAILED: no valid result')
        return {'aicc': None, 'daicc': None, 'boundary': True,
                'w0': None, 'wa': None, 'q0': None, 'params': None}

    aicc  = _aicc(best_chi2, k)
    daicc = aicc - lcdm_aicc
    bnd   = _at_boundary(best_params, bounds[:len(best_params)])

    Om, H0 = best_params[0], best_params[1]
    muR0   = best_params[2] if k >= 3 else UB2_MUR0

    param_names = ['Om', 'H0'] + (['muR0'] if k >= 3 else [])
    for name, val in zip(param_names, best_params):
        print(f'  {name}={val:.4f}', end='  ')
    print()

    fn = _make_E_UB(Om, muR0)
    w0, wa, q0_val = None, None, None
    if fn is not None:
        cb, cc, cs, cr, ct = _chi2_all(fn, Om, H0)
        print(f'  chi2: BAO={cb:.4f} CMB={cc:.4f} SN={cs:.4f} RSD={cr:.4f}')
        try:
            w0, wa = cpl_wa(fn, Om)
            if w0 is not None:
                q0_val = _q0(Om, w0)
        except Exception:
            pass
    else:
        print('  E_fn invalid')

    cpl_aicc     = cpl_result.get('aicc') if cpl_result else None
    daicc_vs_cpl = (aicc - cpl_aicc) if cpl_aicc else None
    vdict        = _verdict(daicc, boundary=bnd, k2=(k <= 2))

    print(f'  AICc={aicc:.4f}  dAICc(vs LCDM)={daicc:.2f}', end='')
    if daicc_vs_cpl is not None:
        print(f'  vs CPL: {daicc_vs_cpl:+.2f}', end='')
    print()
    print(f'  boundary={bnd}')

    if w0 is not None:
        print(f'  CPL: w0={w0:.4f}, wa={wa:.4f}')
        dson_w0 = (w0 - SON_W0) / SON_W0_2SIG
        dson_wa = (wa - SON_WA) / SON_WA_2SIG
        print(f'  Son+25 (w0={SON_W0}): dev={dson_w0:+.1f}sigma  wa dev={dson_wa:+.1f}sigma')
    if q0_val is not None:
        print(f'  q0={q0_val:.4f}  (Son+25 target={SON_Q0:+.2f})')
    print(f'  Verdict: {vdict}')
    sys.stdout.flush()

    return {
        'aicc': aicc, 'daicc': daicc, 'daicc_vs_cpl': daicc_vs_cpl,
        'boundary': bnd, 'w0': w0, 'wa': wa, 'q0': q0_val,
        'params': best_params, 'chi2': best_chi2, 'verdict': vdict,
        'muR0': muR0,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Tasks 4-5: Visualization (E(z), rho_DE(z), F_avg(z))
# ──────────────────────────────────────────────────────────────────────────────
def task4_ez_plot(res_ub2, res_ub3, cpl_result, lcdm_result, out_dir):
    print('\n' + '='*60)
    print('Task 4: E(z) shape comparison')
    print('='*60)

    z_plot = np.linspace(0.0, 3.0, 500)
    fig, ax = plt.subplots(figsize=(10, 5))

    # LCDM
    Om_l = lcdm_result['Om']
    E_lcdm_v = np.array([float(E_lcdm(z, Om_l)) for z in z_plot])
    ax.plot(z_plot, E_lcdm_v, 'k-', lw=2, label=f'LCDM (Om={Om_l:.3f})')

    # CPL
    if cpl_result.get('params'):
        Om_c, H0_c, w0_c, wa_c = cpl_result['params']
        fn_c = _make_E_cpl(Om_c, w0_c, wa_c)
        if fn_c:
            E_cpl = fn_c(z_plot, Om_c)
            if E_cpl is not None:
                ax.plot(z_plot, E_cpl, 'C5--', lw=1.5,
                        label=f'CPL (w0={w0_c:.2f}, wa={wa_c:.2f})')

    # UB2
    if res_ub2.get('params'):
        Om2, H02 = res_ub2['params'][:2]
        fn2 = _make_E_UB(Om2, UB2_MUR0)
        if fn2:
            E2 = fn2(z_plot, Om2)
            if E2 is not None:
                ax.plot(z_plot, E2, 'C0-', lw=1.5,
                        label=f'UB2 (muR0={UB2_MUR0}, Om={Om2:.3f})')

    # UB3
    if res_ub3.get('params'):
        Om3, H03, mR3 = res_ub3['params'][:3]
        fn3 = _make_E_UB(Om3, mR3)
        if fn3:
            E3 = fn3(z_plot, Om3)
            if E3 is not None:
                ax.plot(z_plot, E3, 'C1-.', lw=1.5,
                        label=f'UB3 (muR0={mR3:.3f}, Om={Om3:.3f})')

    ax.set_xlabel('z')
    ax.set_ylabel('E(z) = H(z)/H0')
    ax.set_title('L44: E(z) comparison')
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

    out = os.path.join(out_dir, 'l44_task4_ez.png')
    fig.savefig(out, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f'  Plot: {out}')
    sys.stdout.flush()


def task5_favg_plot(res_ub2, res_ub3, out_dir):
    print('\n' + '='*60)
    print('Task 5: F_avg(z) and rho_DE(z) diagnostics')
    print('='*60)

    z_plot = np.linspace(0.0, 3.0, 500)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    for tag, res, col, label in [
        ('ub2', res_ub2, 'C0', f'UB2 (muR0={UB2_MUR0})'),
        ('ub3', res_ub3, 'C1', 'UB3'),
    ]:
        if not res.get('params'):
            continue
        params = res['params']
        Om   = params[0]
        muR0 = params[2] if len(params) > 2 else UB2_MUR0
        OL0  = 1.0 - Om - OR
        F0   = np.exp(-muR0)

        E_arr = _compute_E_UB(UB_Z_GRID, Om, muR0)
        if E_arr is None:
            continue

        ifn = interp1d(UB_Z_GRID, E_arr, kind='linear',
                       bounds_error=False, fill_value=np.nan)
        E_v   = ifn(z_plot)
        chi_v = np.concatenate([[0.0],
                cumulative_trapezoid(1.0 / E_arr, UB_Z_GRID)])
        chi_interp = interp1d(UB_Z_GRID, chi_v, kind='linear',
                              bounds_error=False, fill_value=np.nan)
        chi_p  = chi_interp(z_plot)
        chiE_p = chi_p * E_v
        I_fn   = _build_I_interp(muR0)
        q_p    = np.minimum(chiE_p, 1.0)
        I_q    = I_fn(q_p)
        F_avg  = np.where(chiE_p > 1e-10, I_q / chiE_p, F0)
        rho_DE = OL0 * F_avg / F0

        axes[0].plot(z_plot, F_avg / F0, color=col,
                     label=f'{label} muR0={muR0:.2f}')
        axes[1].plot(z_plot, rho_DE / OL0, color=col,
                     label=f'{label} muR0={muR0:.2f}')

    for ax in axes:
        ax.axhline(1.0, color='k', ls='--', lw=0.8, alpha=0.5, label='LCDM (=1)')
        ax.set_xlabel('z')
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)
    axes[0].set_ylabel('F_avg(z) / F_avg(0)')
    axes[0].set_title('Path-averaged field (normalized)')
    axes[1].set_ylabel('rho_DE(z) / OL0')
    axes[1].set_title('Dark energy density (normalized)')

    fig.tight_layout()
    out = os.path.join(out_dir, 'l44_task5_favg.png')
    fig.savefig(out, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f'  Plot: {out}')
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 6: muR0 scan plot
# ──────────────────────────────────────────────────────────────────────────────
def task6_mur0_scan_plot(scan_results, lcdm_aicc, out_dir):
    print('\n' + '='*60)
    print('Task 6: muR0 sensitivity scan plot')
    print('='*60)

    if not scan_results:
        print('  No scan results to plot')
        return

    mur0_vals = [r['muR0'] for r in scan_results]
    daicc_vals = [r['daicc'] for r in scan_results]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(mur0_vals, daicc_vals, 'C0o-', ms=5, lw=1.5)
    ax.axhline(0, color='k', ls='--', lw=0.8, label='LCDM baseline')
    ax.axhline(-4, color='C2', ls=':', lw=0.8, label='dAICc=-4 (Q91)')
    ax.axhline(-10, color='C3', ls=':', lw=0.8, label='dAICc=-10 (Q92/Q93)')
    ax.axvline(1.0, color='C1', ls=':', lw=0.8, alpha=0.7, label='muR0=1 (natural)')
    ax.set_xlabel('muR0')
    ax.set_ylabel('dAICc vs LCDM')
    ax.set_title('L44: muR0 sensitivity (k=2, UB2 with optimized Om, H0)')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()

    out = os.path.join(out_dir, 'l44_task6_mur0scan.png')
    fig.savefig(out, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f'  Plot: {out}')
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 7: w(z) visualization
# ──────────────────────────────────────────────────────────────────────────────
def task7_wz_plot(res_ub2, res_ub3, cpl_result, out_dir):
    print('\n' + '='*60)
    print('Task 7: w(z) Visualization')
    print('='*60)

    z_plot = np.linspace(0.01, 2.0, 300)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axhline(-1.0, color='k', ls='--', lw=1, label='LCDM (w=-1)')

    # Son et al. CPL reference
    w_son = SON_W0 + SON_WA * z_plot / (1.0 + z_plot)
    ax.plot(z_plot, w_son, 'k-', lw=2,
            label=f'Son+25 (w0={SON_W0}, wa={SON_WA})')
    ax.fill_between(z_plot,
        (SON_W0 - SON_W0_2SIG) + (SON_WA - SON_WA_2SIG)*z_plot/(1+z_plot),
        (SON_W0 + SON_W0_2SIG) + (SON_WA + SON_WA_2SIG)*z_plot/(1+z_plot),
        alpha=0.12, color='k', label='Son+25 2-sigma')

    # CPL fit
    if cpl_result.get('w0') is not None:
        w0_c, wa_c = cpl_result['w0'], cpl_result['wa']
        ax.plot(z_plot, w0_c + wa_c*z_plot/(1+z_plot), 'C5-.',
                lw=1.5, label=f'CPL fit (w0={w0_c:.2f}, wa={wa_c:.2f})')

    # UB2
    for res, col, label in [
        (res_ub2, 'C0', f'UB2 (muR0={UB2_MUR0})'),
        (res_ub3, 'C1', 'UB3'),
    ]:
        w0 = res.get('w0'); wa = res.get('wa')
        if w0 is not None and wa is not None:
            ax.plot(z_plot, w0 + wa*z_plot/(1+z_plot), col, lw=1.5,
                    label=f'{label} (w0={w0:.2f}, wa={wa:.2f})')

    ax.set_xlabel('z')
    ax.set_ylabel('w(z)')
    ax.set_title('L44: UB Model w(z) vs Son et al. 2025')
    ax.legend(fontsize=8, loc='best')
    ax.set_ylim(-4.0, 0.5)
    ax.grid(alpha=0.3)

    out = os.path.join(out_dir, 'l44_task7_wz.png')
    fig.savefig(out, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f'  Plot: {out}')
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 8: Bootstrap
# ──────────────────────────────────────────────────────────────────────────────
def _boot_worker_ub(batch):
    """Bootstrap batch for UB model. Perturbs BAO, CMB, RSD only."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    import sys as _sys
    _l35 = _sys.modules.get('l35_test') or __import__('l35_test')
    orig_bao = dict(_l35.DESI_DR2)
    orig_cmb = _l35.CMB_OBS.copy()
    orig_rsd = _l35.FS8_OBS.copy()

    results = []
    np.random.seed(0)

    for item in batch:
        s0, new_bao, new_cmb, new_rsd, tag, best_params, k = item
        _l35.DESI_DR2 = {**orig_bao, 'value': new_bao}
        _l35.CMB_OBS  = new_cmb
        _l35.FS8_OBS  = new_rsd

        def _tot(fn, Om, H0):
            t = (chi2_bao(fn, Om, H0) + chi2_cmb(fn, Om, H0) +
                 chi2_sn_corr(fn, Om, H0) + chi2_rsd(fn, Om, H0))
            return t if (np.isfinite(t) and t < 1e7) else 1e9

        muR0_boot = best_params[2] if k >= 3 else UB2_MUR0

        def obj_win(p):
            Om, H0 = p[0], p[1]
            if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
                return 1e9
            mR = p[2] if k >= 3 else muR0_boot
            if k >= 3 and (mR < 0.05 or mR > 15.0):
                return 1e9
            fn = _make_E_UB(Om, mR)
            if fn is None:
                return 1e9
            return _tot(fn, Om, H0)

        def obj_lcdm(p):
            Om, H0 = p
            if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
                return 1e9
            fn = lambda z, _: E_lcdm(z, Om)
            t  = _tot(fn, Om, H0)
            return t

        try:
            r_w = minimize(obj_win, s0[:k], method='Nelder-Mead',
                           options={'xatol': 1e-3, 'fatol': 1e-3, 'maxiter': 300})
            r_l = minimize(obj_lcdm, s0[:2], method='Nelder-Mead',
                           options={'xatol': 1e-3, 'fatol': 1e-3, 'maxiter': 300})
            aicc_w = _aicc(r_w.fun, k)
            aicc_l = _aicc(r_l.fun, 2)
            results.append(float(aicc_w - aicc_l))
        except Exception:
            results.append(None)

    _l35.DESI_DR2 = orig_bao
    _l35.CMB_OBS  = orig_cmb
    _l35.FS8_OBS  = orig_rsd
    return results


def task8_bootstrap(pool, winner_tag, winner_result, lcdm_result):
    print('\n' + '='*60)
    print(f'Task 8: Bootstrap ({winner_tag}, N={N_BOOT})')
    print('='*60)
    t0 = time.time()

    best_p = winner_result['params']
    k_win  = 2 if winner_tag == 'ub2' else 3
    Om_l   = lcdm_result['Om']
    H0_l   = lcdm_result['H0']

    E_fn_lcdm = lambda z, _: E_lcdm(z, Om_l)
    bao_nom_l = _bao_theory_vec(E_fn_lcdm, Om_l, H0_l)
    if bao_nom_l is None:
        print('  SKIPPED: BAO theory vector failed')
        return None

    rng     = np.random.default_rng(99)
    bao_cov = np.linalg.inv(DESI_DR2_COV_INV)
    bao_L   = np.linalg.cholesky(bao_cov)

    boot_items = []
    for _ in range(N_BOOT):
        nb  = bao_nom_l + bao_L @ rng.standard_normal(13)
        nc  = CMB_OBS + CMB_SIG * rng.standard_normal(len(CMB_OBS))
        nr  = FS8_OBS + FS8_SIG * rng.standard_normal(len(FS8_OBS))
        s0  = ([best_p[0] + rng.normal(0, 0.01),
                best_p[1] + rng.normal(0, 0.5)] + list(best_p[2:]))
        boot_items.append((s0, nb, nc, nr, winner_tag, best_p, k_win))

    bsz     = max(1, N_BOOT // N_WORKERS)
    batches = [boot_items[i:i+bsz] for i in range(0, N_BOOT, bsz)]
    raw     = pool.map(_boot_worker_ub, batches)

    all_d = []
    for b in raw:
        all_d.extend(b)

    vals    = np.array([v for v in all_d if v is not None and np.isfinite(v)])
    elapsed = time.time() - t0
    print(f'  Bootstrap done in {elapsed:.1f}s')
    print(f'  Valid: {len(vals)}/{N_BOOT}')

    if len(vals) == 0:
        print('  Verdict: FAIL (no valid samples)')
        return {'valid': 0, 'verdict': 'FAIL'}

    med   = float(np.median(vals))
    lo    = float(np.percentile(vals, 16))
    hi    = float(np.percentile(vals, 84))
    p_lt4 = float(np.mean(vals < -4))
    verd  = 'PASS' if p_lt4 >= 0.90 else 'FAIL'
    print(f'  dAICc median={med:.2f}  68%CI=[{lo:.2f},{hi:.2f}]')
    print(f'  dAICc<-4: {p_lt4*100:.1f}%  Verdict: {verd}')
    sys.stdout.flush()

    return {'valid': int(len(vals)), 'median': med, 'ci68': [lo, hi],
            'frac_lt4': p_lt4, 'verdict': verd}


# ──────────────────────────────────────────────────────────────────────────────
# Task 9: w0-wa plane
# ──────────────────────────────────────────────────────────────────────────────
def task9_w0wa_contour(res_ub2, res_ub3, cpl_result, out_dir):
    print('\n' + '='*60)
    print('Task 9: w0-wa plane')
    print('='*60)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axvline(-1.0, color='k', ls=':', lw=0.8, alpha=0.5)
    ax.axhline(0.0,  color='k', ls=':', lw=0.8, alpha=0.5)
    ax.plot(-1.0, 0.0, 'k+', ms=12, label='LCDM')

    # Son et al. target
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(SON_W0, SON_WA, 'ks', ms=10, label=f'Son+25 ({SON_W0}, {SON_WA})')
    ax.plot(SON_W0 + SON_W0_2SIG/2*np.cos(theta),
            SON_WA + SON_WA_2SIG/2*np.sin(theta), 'k-', lw=1, alpha=0.5)
    ax.plot(SON_W0 + SON_W0_2SIG*np.cos(theta),
            SON_WA + SON_WA_2SIG*np.sin(theta), 'k--', lw=1, alpha=0.3,
            label='Son+25 1/2-sigma')

    # DESI DR2
    ax.plot(-0.757, -0.83, 'g^', ms=8, label='DESI DR2 (-0.757, -0.83)')

    # CPL fit
    if cpl_result.get('w0') is not None:
        ax.plot(cpl_result['w0'], cpl_result['wa'], 'C5*', ms=12,
                label=f"CPL fit ({cpl_result['w0']:.2f}, {cpl_result['wa']:.2f})")

    # UB models
    for res, col, label in [
        (res_ub2, 'C0', f'UB2 (muR0={UB2_MUR0})'),
        (res_ub3, 'C1', 'UB3'),
    ]:
        w0 = res.get('w0'); wa = res.get('wa')
        if w0 is not None and wa is not None:
            ax.plot(w0, wa, 'o', color=col, ms=10,
                    label=f'{label} ({w0:.2f}, {wa:.2f})')

    ax.set_xlabel('w0')
    ax.set_ylabel('wa')
    ax.set_title('L44: w0-wa plane (UB model vs Son+25 + DESI DR2)')
    ax.legend(fontsize=8, loc='best')
    ax.set_xlim(-3.0, 0.5)
    ax.set_ylim(-5.0, 3.0)
    ax.grid(alpha=0.3)

    out = os.path.join(out_dir, 'l44_task9_w0wa.png')
    fig.savefig(out, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f'  Plot: {out}')
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 10: q0 comparison + final verdict
# ──────────────────────────────────────────────────────────────────────────────
def task10_q0_and_verdict(res_ub2, res_ub3, cpl_result, lcdm_result,
                           r8, lcdm_aicc):
    print('\n' + '='*60)
    print('Task 10: q0 comparison + L44 final verdict')
    print('='*60)
    print(f'  Son+25 target: q0 = {SON_Q0:+.2f} (deceleration)')
    print(f'  LCDM standard: q0 = -0.53 (acceleration)')
    print()
    print(f'  {"Model":<25} {"w0":>8} {"wa":>8} {"q0":>8}  Son+25?')
    print('  ' + '-'*60)

    if cpl_result.get('w0') is not None:
        w0_c = cpl_result['w0']; wa_c = cpl_result['wa']
        Om_c = cpl_result.get('Om') or 0.36
        q0_c = _q0(Om_c, w0_c)
        agrees = 'YES' if q0_c > 0 else ('NEAR' if q0_c > -0.1 else 'NO')
        print(f'  {"CPL fit":<25} {w0_c:>8.3f} {wa_c:>8.3f} {q0_c:>8.3f}  {agrees}')

    for res, label in [(res_ub2, f'UB2 (muR0={UB2_MUR0})'), (res_ub3, 'UB3')]:
        w0 = res.get('w0'); wa = res.get('wa'); q0v = res.get('q0')
        if w0 is None:
            continue
        if q0v is None and res.get('params'):
            q0v = _q0(res['params'][0], w0)
        agrees = 'YES' if (q0v or -999) > 0 else ('NEAR' if (q0v or -999) > -0.1 else 'NO')
        print(f'  {label:<25} {w0:>8.3f} {(wa or float("nan")):>8.3f} '
              f'{(q0v or float("nan")):>8.3f}  {agrees}')

    # Final verdict
    print('\n' + '='*60)
    print('L44 FINAL VERDICT')
    print('='*60)

    models = [('UB2', res_ub2, 2), ('UB3', res_ub3, 3)]
    for name, res, k in models:
        d  = res.get('daicc')
        v  = res.get('verdict', '?')
        mR = res.get('muR0', UB2_MUR0)
        print(f'  {name} (k={k}, muR0={mR:.3f}): dAICc={d:+.2f}  [{v}]')

    # Best UB
    valid_models = [(name, res) for name, res, k in models
                    if res.get('daicc') is not None]
    if valid_models:
        best_name, best_res = min(valid_models, key=lambda x: x[1]['daicc'])
        d_best = best_res['daicc']
        v_best = best_res['verdict']
        print(f'\n  Best UB: {best_name}  dAICc={d_best:.2f}  [{v_best}]')

        if r8:
            print(f'  Bootstrap: median={r8.get("median", "?"):.2f}  '
                  f'frac<-4={r8.get("frac_lt4", 0)*100:.1f}%  {r8.get("verdict", "?")}')

        if d_best < -15:
            scenario = 'Q94 DISCOVERY -- ballistic boundary inflow: Nobel-level'
        elif d_best < -10:
            scenario = 'Q93 TRIUMPH -- strong UB evidence, Nature Letter candidate'
        elif d_best < -4:
            scenario = 'Q92 GAME -- competitive with CPL, JCAP paper'
        elif d_best < 0:
            scenario = 'Q91/Q90 -- marginal improvement, soft evidence only'
        else:
            scenario = 'K90 KILL -- UB rejected, SQT boundary inflow falsified'
        print(f'  Scenario: {scenario}')

    w0_best = best_res.get('w0') if valid_models else None
    if w0_best is not None:
        dson = abs(w0_best - SON_W0) / SON_W0_2SIG
        print(f'  Son+25 w0 compatibility: {dson:.1f}sigma')

    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    OUT_DIR = _SCRIPT_DIR

    print('='*60)
    print('L44: Model UB -- Boundary Inflow + Ballistic Diffusion')
    print(f'8-worker parallel  |  L43 LCDM AICc ref={LCDM_AICC_L43:.2f}')
    print('='*60)
    sys.stdout.flush()

    pretask_validate(OUT_DIR)

    ctx  = mp.get_context('spawn')
    pool = ctx.Pool(N_WORKERS)

    r0        = None
    r8        = None
    res_ub2   = {}
    res_ub3   = {}
    cpl_res   = {}
    lcdm_res  = {}
    scan_res  = []
    lcdm_aicc = LCDM_AICC_L43

    try:
        # Task 0: Baselines
        r0 = task0_baselines(pool)
        lcdm_aicc = r0['lcdm_aicc']
        lcdm_res  = r0['lcdm']
        cpl_res   = r0['cpl']

        # Tasks 1-2: UB fits
        t12 = tasks1to2_ub_fits(pool)

        # Report UB2
        res_ub2 = _report_ub(
            'ub2', 'UB2 (k=2, muR0=1.0 fixed)', 2,
            _BND_UB2, *t12['ub2'], lcdm_aicc, cpl_res)

        # Report UB3
        res_ub3 = _report_ub(
            'ub3', 'UB3 (k=3, muR0 free)', 3,
            _BND_UB3, *t12['ub3'], lcdm_aicc, cpl_res)

        # Task 3: muR0 sensitivity scan
        scan_res = task3_mur0_scan(pool, lcdm_aicc)

        # Task 4: E(z) plot
        task4_ez_plot(res_ub2, res_ub3, cpl_res, lcdm_res, OUT_DIR)

        # Task 5: F_avg / rho_DE plot
        task5_favg_plot(res_ub2, res_ub3, OUT_DIR)

        # Task 6: muR0 scan plot
        task6_mur0_scan_plot(scan_res, lcdm_aicc, OUT_DIR)

        # Task 7: w(z) plot
        task7_wz_plot(res_ub2, res_ub3, cpl_res, OUT_DIR)

        # Task 8: Bootstrap (best UB model)
        best_res = res_ub2 if (res_ub2.get('daicc') or 1e9) <= (res_ub3.get('daicc') or 1e9) else res_ub3
        best_tag = 'ub2' if best_res is res_ub2 else 'ub3'
        if best_res.get('daicc') is not None and best_res['daicc'] < -2:
            r8 = task8_bootstrap(pool, best_tag, best_res, lcdm_res)
        else:
            best_d = best_res.get('daicc', 'N/A')
            print(f'\nTask 8: Bootstrap -- SKIPPED (best dAICc={best_d} >= -2)')

        # Task 9: w0-wa plane
        task9_w0wa_contour(res_ub2, res_ub3, cpl_res, OUT_DIR)

        # Task 10: q0 + final verdict
        task10_q0_and_verdict(res_ub2, res_ub3, cpl_res, lcdm_res,
                               r8, lcdm_aicc)

    finally:
        pool.close()
        pool.join()

    # ── Summary ──
    print('\n' + '='*60)
    print('L44 RESULTS SUMMARY')
    print('='*60)
    print(f'\n[Task 0] Baselines (corrected data)')
    print(f'  LCDM: AICc={lcdm_aicc:.2f}  (L43_ref={LCDM_AICC_L43:.2f})')
    if cpl_res.get('w0') is not None:
        print(f"  CPL:  AICc={cpl_res['aicc']:.2f}  dAICc={cpl_res['daicc_vs_lcdm']:.2f}")
        print(f"        w0={cpl_res['w0']:.3f}, wa={cpl_res['wa']:.3f}")

    print('\n[Tasks 1-2] UB model fits')
    for name, res, k in [('UB2 k=2', res_ub2, 2), ('UB3 k=3', res_ub3, 3)]:
        d = res.get('daicc')
        v = res.get('verdict', '?')
        w0 = res.get('w0'); wa = res.get('wa'); q0v = res.get('q0')
        mR = res.get('muR0', UB2_MUR0)
        if d is not None:
            line = f'  {name:<12}  muR0={mR:.3f}  dAICc={d:+8.2f}  [{v}]'
            if w0 is not None:
                line += f'  w0={w0:.3f} wa={wa:.3f}'
            if q0v is not None:
                line += f'  q0={q0v:+.3f}'
            print(line)
        else:
            print(f'  {name:<12}  FAILED')

    if r8:
        print(f'\n[Bootstrap]  median={r8.get("median","?"):.2f}  '
              f'frac<-4={r8.get("frac_lt4",0)*100:.1f}%  {r8.get("verdict","?")}')

    # Save JSON
    save = {
        'task0':        _jsonify(r0),
        'task1_ub2':    _jsonify(res_ub2),
        'task2_ub3':    _jsonify(res_ub3),
        'task3_scan':   _jsonify(scan_res),
        'task8_boot':   _jsonify(r8),
        'lcdm_aicc_l43': LCDM_AICC_L43,
        'cpl_aicc_l43':  CPL_AICC_L43,
        'lcdm_aicc':     lcdm_aicc,
        'son_params':    {'w0': SON_W0, 'wa': SON_WA, 'q0': SON_Q0},
        'ub2_mur0_fixed': UB2_MUR0,
    }
    out_json = os.path.join(OUT_DIR, 'l44_results.json')
    with open(out_json, 'w') as f:
        json.dump(save, f, indent=2)
    print(f'\nSaved: {out_json}')
