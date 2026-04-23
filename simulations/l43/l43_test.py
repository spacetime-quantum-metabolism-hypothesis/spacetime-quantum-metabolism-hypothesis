# -*- coding: utf-8 -*-
"""
l43_test.py -- L43: Son et al. 2025 age-bias correction + SQT psi^n a priori test
==================================================================================
Son et al. 2025 (MNRAS 544:975): SN Ia progenitor age-bias 5.5sigma confirmed.
After correction: LCDM 9sigma excluded, w0~-0.34, wa~-1.90, q0~+0.18.

SQT a priori: rho_DE propto psi^n, psi=1/(1+alpha*(1+z)^3), alpha=Om/OL0
  n=1: w0 = -1 + Om/(OL0+Om) = -0.687
  n=2: w0 = -1 + 2*Om/(OL0+Om) = -0.374  <-- Son et al. w0=-0.34 compatible!
  n=3: w0 = -1 + 3*Om/(OL0+Om) = -0.061

Models:
  Model 0: LCDM  (k=2)  -- baseline with corrected data
  Model 1: CPL   (k=4)  -- w0,wa free (Son et al. reference)
  Model 2: ModelD (k=4) -- existing SQT phenomenology (amp,beta)
  Model 3: D_psi1 (k=2) -- rho_DE propto psi^1 (n=1 a priori)
  Model 4: D_psi2 (k=2) -- rho_DE propto psi^2 (n=2 CORE, Son et al. match?)
  Model 5: D_psi_n (k=3) -- n free (test SQT n=2 prediction)
  Model 6: D_mix  (k=4) -- epsilon*Lambda + (1-epsilon)*psi^n
  Model 7: G_theory_corr (k=3) -- kinetic + V(psi)=0.5*mu2*(psi-psi*)^2

Tasks 0-10, 8-worker spawn pool, 4-person code review x2 before execution.
"""

import os, sys, time, json, warnings
import numpy as np
from scipy.integrate import cumulative_trapezoid, quad
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
    _base as _base35,
    R_S, N_GRID,
    DESI_DR2, DESI_DR2_COV_INV,
)
from phase2.sn_likelihood import DESY5SN

# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────
LCDM_AICC_OLD = 1670.1227     # L35 baseline (uncorrected data)
LCDM_BEST_OLD = {'Om': 0.3094, 'H0': 68.41}
D_BEST        = {'Om': 0.3220, 'H0': 66.98, 'amp': 0.8178, 'beta': 3.533}
D_AICC_OLD    = 1661.68

N_WORKERS  = 8
N_BOOT     = 300

# Son et al. 2025 MNRAS 544:975 age correction parameters
SON_SLOPE     = 0.030     # mag/Gyr  (5.5sigma)
SON_SLOPE_ERR = 0.004     # mag/Gyr  (slope uncertainty)
SON_DAGE_AMP  = 5.3       # Gyr     (age evolution amplitude at z->inf)
SON_DAGE_TAU  = 2.5       # 1/z     (age evolution rate)

# Son et al. best-fit (corrected data + DESI BAO + CMB)
SON_W0    = -0.34
SON_WA    = -1.90
SON_Q0    = +0.18
SON_W0_2SIG = 0.12   # approx 2-sigma width
SON_WA_2SIG = 0.50

# Dense z-grid for precomputed models (extends to CMB last-scattering z~1090, growth z~50)
PSI_Z_GRID = np.concatenate([
    np.linspace(0.0, 3.5, 2000),
    np.linspace(3.5, 1200.0, 600)[1:],
])

# ──────────────────────────────────────────────────────────────────────────────
# Son et al. 2025 age-bias correction
# ──────────────────────────────────────────────────────────────────────────────
def son_age_correction(z):
    """
    Son et al. 2025 progenitor age-bias correction.
    delta_age(z) = A*(1-exp(-tau*z))  [Gyr] -- age evolution fitted to their Fig.2
    delta_m = delta_age * slope        [mag] -- subtract from observed mu
    sigma_extra = delta_age * slope_err [mag] -- additional systematic
    """
    delta_age   = SON_DAGE_AMP * (1.0 - np.exp(-SON_DAGE_TAU * z))
    delta_m     = delta_age * SON_SLOPE
    sigma_extra = delta_age * SON_SLOPE_ERR
    return delta_m, sigma_extra


class DESY5SN_AgeCorr(DESY5SN):
    """DESY5SN with Son et al. 2025 age-bias correction applied to mu_obs."""

    def __init__(self):
        super().__init__()
        # Apply correction: mu_corrected = mu_obs - delta_m(z)
        delta_m, sigma_extra = son_age_correction(self.z_hd)
        self.mu_obs = self.mu_obs - delta_m

        # Expand covariance with additional systematic uncertainty
        cov_raw      = np.linalg.inv(self.cov_inv)
        cov_corr     = cov_raw + np.diag(sigma_extra**2)
        self.cov     = cov_corr
        self.cov_inv = np.linalg.inv(cov_corr)

        # Recompute marginalisation sums
        ones               = np.ones(self.N)
        self._C_inv_1      = self.cov_inv @ ones
        self._one_Cinv_1   = float(ones @ self._C_inv_1)


_SN_CORR = None
def get_sn_corr():
    global _SN_CORR
    if _SN_CORR is None:
        _SN_CORR = DESY5SN_AgeCorr()
    return _SN_CORR


def chi2_sn_corr(E_fn, Om, H0):
    """SN chi2 using Son et al. age-corrected DESY5 data."""
    def _E(z):
        v = E_fn(np.array([float(z)]), Om)
        return 1e30 if (v is None or not np.isfinite(v[0])) else float(v[0])
    return get_sn_corr().chi2(_E, H0_km=H0)


def _chi2_all(E_fn, Om, H0):
    """BAO + CMB + SN_corrected + RSD."""
    cb = chi2_bao(E_fn, Om, H0)
    cc = chi2_cmb(E_fn, Om, H0)
    cs = chi2_sn_corr(E_fn, Om, H0)
    cr = chi2_rsd(E_fn, Om, H0)
    return cb, cc, cs, cr, cb + cc + cs + cr


def _chi2_all_raw(E_fn, Om, H0):
    """BAO + CMB + SN_uncorrected + RSD  (for comparison with L35 baseline)."""
    cb = chi2_bao(E_fn, Om, H0)
    cc = chi2_cmb(E_fn, Om, H0)
    cs = chi2_sn_raw(E_fn, Om, H0)
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
    if boundary:    return 'K92 INVALID'
    if daicc >= 0:  return 'K90 KILL'
    if daicc >= -2: return 'Q90 PASS'
    if daicc >= -4: return 'Q91 STRONG'
    if daicc >= -10:
        return 'Q92 GAME' if k2 else 'Q91 STRONG'
    return 'Q93 TRIUMPH' if k2 else 'Q92 GAME'

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
    """q0 = 0.5*(Om + (1+3*w0)*OL0) = 0.5*(1 + 3*w0*(1-Om-OR))."""
    OL0 = 1.0 - Om - OR
    return 0.5 * (Om + (1.0 + 3.0*w0_eff) * OL0)

def _bao_theory_vec(E_fn, Om, H0):
    z_eff  = DESI_DR2['z_eff']
    z_grid = np.linspace(0.0, z_eff.max() + 0.01, N_GRID)
    Eg = E_fn(z_grid, Om)
    if Eg is None or not np.all(np.isfinite(Eg)):
        return None
    Eg = np.maximum(Eg, 1e-15)
    DM = (C_KMS / H0) * np.concatenate([[0.],
           cumulative_trapezoid(1.0 / Eg, z_grid)])
    tv = np.empty(13)
    for i, (z, qty) in enumerate(zip(z_eff, DESI_DR2['quantity'])):
        idx = min(np.searchsorted(z_grid, z), N_GRID - 1)
        DH  = C_KMS / (H0 * Eg[idx])
        DV  = (z * DM[idx]**2 * DH)**(1./3.) if z > 0 else 0.
        if   'DV' in qty: tv[i] = DV / R_S
        elif 'DM' in qty: tv[i] = DM[idx] / R_S
        elif 'DH' in qty: tv[i] = DH / R_S
        else:              tv[i] = np.nan
    return None if not np.all(np.isfinite(tv)) else tv


# ──────────────────────────────────────────────────────────────────────────────
# E functions
# ──────────────────────────────────────────────────────────────────────────────

def _make_E_cpl(Om, w0, wa):
    """CPL dark energy: rho_DE = OL0*(1+z)^(3(1+w0+wa))*exp(-3*wa*z/(1+z))."""
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

def _E_D(z_arr, Om, amp, beta):
    """Model D: rho_DE = OL0*(1+amp*(ratio-1)*exp(-beta*z)), ratio=psi0/psi."""
    OL0, ratio, _ = _base35(z_arr, Om)
    if OL0 is None:
        return None
    rde = OL0 * (1.0 + amp * (ratio - 1.0) * np.exp(-abs(beta) * z_arr))
    E2  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
    return None if np.any(E2 <= 0) else np.sqrt(E2)

def _make_E_D(Om, amp, beta):
    def fn(z, _Om):
        return _E_D(np.atleast_1d(np.asarray(z, float)), Om, amp, beta)
    return fn

def _make_E_psi_n(Om, n):
    """rho_DE = OL0*(psi/psi0)^n, psi=1/(1+alpha*(1+z)^3), alpha=Om/OL0."""
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    alpha = Om / OL0
    psi_0 = 1.0 / (1.0 + alpha)
    def fn(z_arr, _Om):
        za  = np.asarray(z_arr, float)
        psi = 1.0 / (1.0 + alpha*(1+za)**3)
        rde = OL0 * (psi/psi_0)**n
        E2  = OR*(1+za)**4 + Om*(1+za)**3 + rde
        return None if np.any(E2 <= 0) else np.sqrt(np.maximum(E2, 1e-30))
    return fn

def _make_E_mix(Om, epsilon, n):
    """rho_DE = OL0*(eps + (1-eps)*(psi/psi0)^n)."""
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0 or epsilon < 0 or epsilon >= 1:
        return None
    alpha = Om / OL0
    psi_0 = 1.0 / (1.0 + alpha)
    def fn(z_arr, _Om):
        za  = np.asarray(z_arr, float)
        psi = 1.0 / (1.0 + alpha*(1+za)**3)
        rde = OL0 * (epsilon + (1.0-epsilon)*(psi/psi_0)**n)
        E2  = OR*(1+za)**4 + Om*(1+za)**3 + rde
        return None if np.any(E2 <= 0) else np.sqrt(np.maximum(E2, 1e-30))
    return fn

def _solve_E_gth(z_arr, Om, mu2_H02):
    """
    G_theory_corrected: rho_psi = 0.5*(dpsi/dz*E*(1+z))^2 + V(psi)
    V(psi) = 0.5*mu2*(psi-psi*)^2, psi* = 1/(1+alpha) (axiom equilibrium)
    Self-consistent E(z) by iteration. Normalize E(0)=1.
    """
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    alpha  = Om / OL0
    psi_st = 1.0 / (1.0 + alpha)           # equilibrium at z=0

    psi_z   = 1.0 / (1.0 + alpha*(1+z_arr)**3)
    dpsi_dz = -3.0*alpha*(1+z_arr)**2 / (1.0 + alpha*(1+z_arr)**3)**2
    V       = 0.5 * mu2_H02 * (psi_z - psi_st)**2

    E_prev = np.sqrt(np.maximum(Om*(1+z_arr)**3 + OR*(1+z_arr)**4 + OL0, 1e-30))
    for _ in range(30):
        kin     = 0.5 * (dpsi_dz * E_prev * (1+z_arr))**2
        rho_psi = kin + V
        E2_new  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_psi
        if np.any(E2_new <= 0) or np.any(~np.isfinite(E2_new)):
            return None
        E_new = np.sqrt(E2_new)
        if np.max(np.abs(E_new - E_prev)) < 1e-8:
            E0 = E_new[0]
            if E0 <= 0 or not np.isfinite(E0):
                return None
            return E_new / E0     # normalize E(0)=1
        E_prev = E_new
    return None

def _make_E_gth(Om, mu2_H02):
    """Precompute G_theory_corrected on dense grid, return interpolant."""
    E_arr = _solve_E_gth(PSI_Z_GRID, Om, mu2_H02)
    if E_arr is None:
        return None
    ifn = interp1d(PSI_Z_GRID, E_arr, kind='linear', bounds_error=False,
                   fill_value=np.nan)
    def fn(z, _Om):
        za = np.atleast_1d(np.asarray(z, float))
        Ev = ifn(za)
        return None if (np.any(np.isnan(Ev)) or np.any(Ev <= 0)) else Ev
    return fn


# ──────────────────────────────────────────────────────────────────────────────
# Parameter bounds
# ──────────────────────────────────────────────────────────────────────────────
_BND_LCDM  = [(0.20, 0.55), (55., 82.)]
_BND_CPL   = [(0.20, 0.55), (55., 82.), (-3.0, 0.5), (-5.0, 3.0)]
_BND_D     = [(0.20, 0.55), (55., 82.), (-3.0, 3.0), (0.0, 15.0)]
_BND_PSI1  = [(0.20, 0.55), (55., 82.)]
_BND_PSI2  = [(0.20, 0.55), (55., 82.)]
_BND_PSIN  = [(0.20, 0.55), (55., 82.), (0.1, 6.0)]
_BND_MIX   = [(0.20, 0.55), (55., 82.), (0.0, 0.98), (0.1, 6.0)]
_BND_GTH   = [(0.20, 0.55), (55., 82.), (0.0, 300.0)]


# ──────────────────────────────────────────────────────────────────────────────
# Workers (module-level for spawn-safe pickling)
# ──────────────────────────────────────────────────────────────────────────────

def _worker_lcdm(start):
    """LCDM k=2 worker with corrected SN data."""
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
    """CPL k=4 worker (Om, H0, w0, wa)."""
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


def _worker_D(start):
    """Model D k=4 worker (Om, H0, amp, beta)."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    def obj(p):
        Om, H0, amp, beta = p
        if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
            return 1e9
        if amp < -3 or amp > 3 or beta < 0 or beta > 15:
            return 1e9
        fn = _make_E_D(Om, amp, beta)
        if fn is None:
            return 1e9
        cb, cc, cs, cr, tot = _chi2_all(fn, Om, H0)
        return tot if np.isfinite(tot) else 1e9
    try:
        r = minimize(obj, start, method='Nelder-Mead',
                     options={'xatol': 1e-4, 'fatol': 1e-4, 'maxiter': 600})
        return (float(r.fun), [float(x) for x in r.x])
    except Exception:
        return (1e9, None)


def _worker_psi1(start):
    """D_psi1 k=2 worker (Om, H0), n=1 fixed."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    def obj(p):
        Om, H0 = p
        if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
            return 1e9
        fn = _make_E_psi_n(Om, 1.0)
        if fn is None:
            return 1e9
        cb, cc, cs, cr, tot = _chi2_all(fn, Om, H0)
        return tot if np.isfinite(tot) else 1e9
    try:
        r = minimize(obj, start, method='Nelder-Mead',
                     options={'xatol': 1e-5, 'fatol': 1e-5, 'maxiter': 600})
        return (float(r.fun), [float(x) for x in r.x])
    except Exception:
        return (1e9, None)


def _worker_psi2(start):
    """D_psi2 k=2 worker (Om, H0), n=2 fixed. CORE model."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    def obj(p):
        Om, H0 = p
        if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
            return 1e9
        fn = _make_E_psi_n(Om, 2.0)
        if fn is None:
            return 1e9
        cb, cc, cs, cr, tot = _chi2_all(fn, Om, H0)
        return tot if np.isfinite(tot) else 1e9
    try:
        r = minimize(obj, start, method='Nelder-Mead',
                     options={'xatol': 1e-5, 'fatol': 1e-5, 'maxiter': 600})
        return (float(r.fun), [float(x) for x in r.x])
    except Exception:
        return (1e9, None)


def _worker_psi_n(start):
    """D_psi_n k=3 worker (Om, H0, n), n free."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    def obj(p):
        Om, H0, n = p
        if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
            return 1e9
        if n < 0.1 or n > 6.0:
            return 1e9
        fn = _make_E_psi_n(Om, n)
        if fn is None:
            return 1e9
        cb, cc, cs, cr, tot = _chi2_all(fn, Om, H0)
        return tot if np.isfinite(tot) else 1e9
    try:
        r = minimize(obj, start, method='Nelder-Mead',
                     options={'xatol': 1e-4, 'fatol': 1e-4, 'maxiter': 600})
        return (float(r.fun), [float(x) for x in r.x])
    except Exception:
        return (1e9, None)


def _worker_mix(start):
    """D_mix k=4 worker (Om, H0, epsilon, n)."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    def obj(p):
        Om, H0, eps, n = p
        if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
            return 1e9
        if eps < 0.0 or eps >= 1.0 or n < 0.1 or n > 6.0:
            return 1e9
        fn = _make_E_mix(Om, eps, n)
        if fn is None:
            return 1e9
        cb, cc, cs, cr, tot = _chi2_all(fn, Om, H0)
        return tot if np.isfinite(tot) else 1e9
    try:
        r = minimize(obj, start, method='Nelder-Mead',
                     options={'xatol': 1e-4, 'fatol': 1e-4, 'maxiter': 600})
        return (float(r.fun), [float(x) for x in r.x])
    except Exception:
        return (1e9, None)


def _worker_gth(start):
    """G_theory_corr k=3 worker (Om, H0, mu2_H02)."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    def obj(p):
        Om, H0, mu2 = p
        if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
            return 1e9
        if mu2 < 0.0 or mu2 > 300.0:
            return 1e9
        fn = _make_E_gth(Om, mu2)
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


def _best_of(results):
    valid = [(c, p) for c, p in results if p is not None and np.isfinite(c) and c < 1e8]
    if not valid:
        return 1e9, None
    return min(valid, key=lambda x: x[0])


def _make_starts_2d(n_rand, rng, extra=None):
    """Grid + random starts for k=2 (Om, H0)."""
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
# Task 0: Baselines (LCDM + CPL with corrected data)
# ──────────────────────────────────────────────────────────────────────────────
def task0_baselines(pool):
    print('\n' + '='*60)
    print('Task 0: Baselines (corrected SN data)')
    print('='*60)
    t0 = time.time()
    rng = np.random.default_rng(0)

    # Warm up corrected SN cache in main process
    print('  Warming corrected SN cache...')
    get_sn_corr()
    print('  SN_corr ready.')
    sys.stdout.flush()

    # LCDM starts
    starts_lcdm = _make_starts_2d(10, rng,
                                   extra=[[0.3094, 68.41], [0.31, 68.0], [0.30, 70.0]])

    # CPL starts (Om, H0, w0, wa)
    starts_cpl = []
    for Om0 in [0.28, 0.30, 0.32, 0.35]:
        for H0_0 in [64., 67., 70.]:
            for w0_0 in [-0.5, -1.0, -0.3]:
                for wa_0 in [-1.0, -2.0, 0.0]:
                    starts_cpl.append([Om0, H0_0, w0_0, wa_0])
    # Son et al. target seeds
    starts_cpl += [[0.31, 68., -0.34, -1.90], [0.30, 68., -0.40, -2.0],
                   [0.32, 67., -0.30, -1.5]]

    print(f'  LCDM: {len(starts_lcdm)} starts')
    print(f'  CPL:  {len(starts_cpl)} starts')
    sys.stdout.flush()

    res_lcdm = pool.map(_worker_lcdm, starts_lcdm)
    res_cpl  = pool.map(_worker_cpl,  starts_cpl)

    # LCDM best
    chi2_lcdm, par_lcdm = _best_of(res_lcdm)
    if par_lcdm is not None:
        Om_l, H0_l = par_lcdm[0], par_lcdm[1]
    else:
        Om_l, H0_l = LCDM_BEST_OLD['Om'], LCDM_BEST_OLD['H0']
        chi2_lcdm = _chi2_all(lambda z, _: E_lcdm(z, Om_l), Om_l, H0_l)[4]
    aicc_lcdm = _aicc(chi2_lcdm, 2)

    fn_l = lambda z, _: E_lcdm(z, Om_l)
    cb_l, cc_l, cs_l, cr_l, _ = _chi2_all(fn_l, Om_l, H0_l)
    print(f'\n  LCDM (corrected): Om={Om_l:.4f}, H0={H0_l:.4f}')
    print(f'  chi2: BAO={cb_l:.4f} CMB={cc_l:.4f} SN={cs_l:.4f} RSD={cr_l:.4f}')
    print(f'  AICc={aicc_lcdm:.4f}  (prev uncorrected={LCDM_AICC_OLD:.4f}, '
          f'change={aicc_lcdm - LCDM_AICC_OLD:+.2f})')

    # CPL best
    chi2_cpl, par_cpl = _best_of(res_cpl)
    if par_cpl is not None:
        Om_c, H0_c, w0_c, wa_c = par_cpl
        fn_c  = _make_E_cpl(Om_c, w0_c, wa_c)
    else:
        w0_c = wa_c = None
        fn_c  = None
    aicc_cpl = _aicc(chi2_cpl, 4)
    daicc_cpl = aicc_cpl - aicc_lcdm

    if fn_c is not None:
        cb_c, cc_c, cs_c, cr_c, _ = _chi2_all(fn_c, Om_c, H0_c)
        print(f'\n  CPL (corrected): Om={Om_c:.4f}, H0={H0_c:.4f}, '
              f'w0={w0_c:.4f}, wa={wa_c:.4f}')
        print(f'  chi2: BAO={cb_c:.4f} CMB={cc_c:.4f} SN={cs_c:.4f} RSD={cr_c:.4f}')
        print(f'  AICc={aicc_cpl:.4f}  dAICc(vs LCDM)={daicc_cpl:.2f}')
        dson_w0 = abs(w0_c - SON_W0) / SON_W0_2SIG
        dson_wa = abs(wa_c - SON_WA) / SON_WA_2SIG
        print(f'  Son et al. target: w0={SON_W0}, wa={SON_WA}')
        print(f'  Deviation: w0={dson_w0:.1f}sigma, wa={dson_wa:.1f}sigma')
    else:
        print('  CPL: fit failed')

    # Also check old LCDM chi2 with corrected data (for reference)
    E_lcdm_old = lambda z, _: E_lcdm(z, LCDM_BEST_OLD['Om'])
    chi2_old_corr = _chi2_all(E_lcdm_old, LCDM_BEST_OLD['Om'], LCDM_BEST_OLD['H0'])[4]
    aicc_old_corr = _aicc(chi2_old_corr, 2)
    print(f'\n  Old LCDM (Om=0.309, H0=68.4) with corrected data: AICc={aicc_old_corr:.2f}')

    elapsed = time.time() - t0
    print(f'  Elapsed: {elapsed:.1f}s')
    sys.stdout.flush()

    return {
        'lcdm': {'Om': Om_l, 'H0': H0_l, 'chi2': chi2_lcdm, 'aicc': aicc_lcdm,
                 'chi2_bao': cb_l, 'chi2_cmb': cc_l, 'chi2_sn': cs_l, 'chi2_rsd': cr_l},
        'cpl':  {'Om': Om_c if par_cpl else None, 'H0': H0_c if par_cpl else None,
                 'w0': w0_c, 'wa': wa_c, 'chi2': chi2_cpl, 'aicc': aicc_cpl,
                 'daicc_vs_lcdm': daicc_cpl, 'params': par_cpl},
        'lcdm_aicc': aicc_lcdm,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Tasks 1-6: Model fits (parallel)
# ──────────────────────────────────────────────────────────────────────────────
def tasks1to6_fits(pool, lcdm_aicc_corr):
    print('\n' + '='*60)
    print('Tasks 1-6: SQT model fits (parallel pool)')
    print('='*60)
    rng = np.random.default_rng(42)
    t0 = time.time()

    # Model D starts (k=4): Om, H0, amp, beta
    starts_D = []
    for Om0 in [0.28, 0.30, 0.32, 0.34]:
        for H0_0 in [64., 67., 70.]:
            for amp0 in [0.5, 1.0, 1.5]:
                starts_D.append([Om0, H0_0, amp0, 3.0])
    starts_D += [[0.322, 66.98, 0.818, 3.53],
                 [0.31, 68., 1.0, 5.0], [0.30, 68., 0.5, 2.0],
                 [0.31, 68., -0.5, 3.0], [0.32, 67., 0.8, 8.0]]
    for _ in range(15):
        starts_D.append([rng.uniform(0.25, 0.42), rng.uniform(62, 76),
                         rng.uniform(-2, 2.5), rng.uniform(0.5, 12)])

    # D_psi1 starts (k=2)
    starts_psi1 = _make_starts_2d(10, rng)

    # D_psi2 starts (k=2) -- more starts (CORE model)
    starts_psi2 = _make_starts_2d(25, rng,
                                   extra=[[0.31, 68.], [0.30, 68.5], [0.33, 67.]])

    # D_psi_n starts (k=3): Om, H0, n
    starts_psin = []
    for Om0 in [0.27, 0.29, 0.31, 0.33]:
        for H0_0 in [65., 68., 71.]:
            for n0 in [1.0, 1.5, 2.0, 2.5, 3.0]:
                starts_psin.append([Om0, H0_0, n0])
    starts_psin += [[0.31, 68., 2.0], [0.31, 68., 1.8], [0.31, 68., 2.2]]
    for _ in range(15):
        starts_psin.append([rng.uniform(0.25, 0.42), rng.uniform(62, 76),
                            rng.uniform(0.3, 5.5)])

    # D_mix starts (k=4): Om, H0, eps, n
    starts_mix = []
    for Om0 in [0.28, 0.31, 0.34]:
        for H0_0 in [65., 68., 71.]:
            for eps0 in [0.1, 0.3, 0.5]:
                for n0 in [1.5, 2.0, 2.5]:
                    starts_mix.append([Om0, H0_0, eps0, n0])
    for _ in range(15):
        starts_mix.append([rng.uniform(0.25, 0.42), rng.uniform(62, 76),
                           rng.uniform(0.05, 0.8), rng.uniform(0.5, 5.0)])

    # G_theory_corr starts (k=3): Om, H0, mu2
    starts_gth = []
    for Om0 in [0.28, 0.30, 0.32, 0.34]:
        for H0_0 in [64., 67., 70.]:
            for mu2_0 in [0.5, 2.0, 10.0, 50.0, 100.0]:
                starts_gth.append([Om0, H0_0, mu2_0])
    starts_gth += [[0.31, 68., 0.0], [0.31, 68., 200.0]]
    for _ in range(10):
        starts_gth.append([rng.uniform(0.25, 0.42), rng.uniform(62, 76),
                           rng.uniform(0.0, 250.0)])

    print(f'  Model D:     {len(starts_D)} starts')
    print(f'  D_psi1:      {len(starts_psi1)} starts')
    print(f'  D_psi2 CORE: {len(starts_psi2)} starts')
    print(f'  D_psi_n:     {len(starts_psin)} starts')
    print(f'  D_mix:       {len(starts_mix)} starts')
    print(f'  G_theory:    {len(starts_gth)} starts')
    sys.stdout.flush()

    res_D    = pool.map(_worker_D,     starts_D)
    res_psi1 = pool.map(_worker_psi1,  starts_psi1)
    res_psi2 = pool.map(_worker_psi2,  starts_psi2)
    res_psin = pool.map(_worker_psi_n, starts_psin)
    res_mix  = pool.map(_worker_mix,   starts_mix)
    res_gth  = pool.map(_worker_gth,   starts_gth)

    elapsed = time.time() - t0
    print(f'  All model scans done in {elapsed:.1f}s')
    sys.stdout.flush()

    return {
        'model_d':  _best_of(res_D),
        'd_psi1':   _best_of(res_psi1),
        'd_psi2':   _best_of(res_psi2),
        'd_psi_n':  _best_of(res_psin),
        'd_mix':    _best_of(res_mix),
        'g_theory': _best_of(res_gth),
        'elapsed':  elapsed,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Report single model result
# ──────────────────────────────────────────────────────────────────────────────
def _report_model(tag, label, k, param_names, bounds,
                  best_chi2, best_params, lcdm_aicc, cpl_result):
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
    vdict = _verdict(daicc, boundary=bnd, k2=(k <= 2))

    for name, val in zip(param_names, best_params):
        print(f'  {name}={val:.4f}', end='  ')
    print()

    # Build E_fn for reporting
    Om, H0 = best_params[0], best_params[1]
    OL0 = 1.0 - Om - OR
    E_fn = None

    if tag == 'model_d':
        amp, beta = best_params[2], best_params[3]
        E_fn = _make_E_D(Om, amp, beta)
    elif tag == 'd_psi1':
        E_fn = _make_E_psi_n(Om, 1.0)
    elif tag == 'd_psi2':
        E_fn = _make_E_psi_n(Om, 2.0)
    elif tag == 'd_psi_n':
        n = best_params[2]
        E_fn = _make_E_psi_n(Om, n)
    elif tag == 'd_mix':
        eps, n = best_params[2], best_params[3]
        E_fn = _make_E_mix(Om, eps, n)
    elif tag == 'g_theory':
        mu2 = best_params[2]
        E_fn = _make_E_gth(Om, mu2)

    w0, wa, q0_val = None, None, None
    if E_fn is not None:
        cb, cc, cs, cr, ct = _chi2_all(E_fn, Om, H0)
        print(f'  chi2: BAO={cb:.4f} CMB={cc:.4f} SN={cs:.4f} RSD={cr:.4f}')
        try:
            w0, wa = cpl_wa(E_fn, Om)
            if w0 is not None:
                q0_val = _q0(Om, w0)
        except Exception:
            pass
    else:
        print('  E_fn invalid')

    cpl_aicc = cpl_result.get('aicc') if cpl_result else None
    daicc_vs_cpl = (aicc - cpl_aicc) if cpl_aicc else None

    print(f'  AICc={aicc:.4f}  dAICc(vs LCDM)={daicc:.2f}', end='')
    if daicc_vs_cpl is not None:
        print(f'  vs CPL: {daicc_vs_cpl:+.2f}', end='')
    print()
    print(f'  boundary={bnd}')

    if w0 is not None:
        print(f'  CPL: w0={w0:.4f}, wa={wa:.4f}')
        dson_w0 = (w0 - SON_W0) / SON_W0_2SIG
        dson_wa = (wa - SON_WA) / SON_WA_2SIG if wa is not None else None
        print(f'  Son et al. (w0={SON_W0}): dev={dson_w0:+.1f}sigma', end='')
        if dson_wa is not None:
            print(f'  wa dev={dson_wa:+.1f}sigma', end='')
        print()
    if q0_val is not None:
        print(f'  q0={q0_val:.4f}  (Son et al. target={SON_Q0:+.2f})')

    # SQT n prediction for psi models
    if tag in ('d_psi_n', 'd_psi2', 'd_psi1'):
        n_fit = best_params[2] if tag == 'd_psi_n' else (2.0 if tag == 'd_psi2' else 1.0)
        if OL0 > 0:
            w0_pred = -1.0 + n_fit * Om / (OL0 + Om)
            dev_w0 = (w0 - w0_pred) / abs(w0_pred) * 100 if w0 is not None else None
            print(f'  a priori: n={n_fit:.2f} -> w0_pred={w0_pred:.4f}', end='')
            if dev_w0 is not None:
                print(f'  fit dev={dev_w0:+.1f}%', end='')
            print()

    print(f'  Verdict: {vdict}')
    sys.stdout.flush()

    return {
        'aicc': aicc, 'daicc': daicc, 'daicc_vs_cpl': daicc_vs_cpl,
        'boundary': bnd, 'w0': w0, 'wa': wa, 'q0': q0_val,
        'params': best_params, 'chi2': best_chi2,
        'verdict': vdict,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Task 8: Bootstrap
# ──────────────────────────────────────────────────────────────────────────────
def _boot_worker(batch):
    """Bootstrap batch. Each item: (s0, new_bao, new_cmb, new_rsd, tag, k)."""
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
        _l35.DESI_DR2  = {**orig_bao, 'value': new_bao}
        _l35.CMB_OBS   = new_cmb
        _l35.FS8_OBS   = new_rsd

        def _tot(fn, Om, H0):
            t = (chi2_bao(fn, Om, H0) + chi2_cmb(fn, Om, H0) +
                 chi2_sn_corr(fn, Om, H0) + chi2_rsd(fn, Om, H0))
            return t if (np.isfinite(t) and t < 1e7) else 1e9

        def _tot_lcdm(Om, H0):
            fn = lambda z, _: E_lcdm(z, Om)
            return _tot(fn, Om, H0)

        def obj_win(p):
            Om, H0 = p[:2]
            if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
                return 1e9
            if tag == 'd_psi2':
                fn = _make_E_psi_n(Om, 2.0)
            elif tag == 'd_psi1':
                fn = _make_E_psi_n(Om, 1.0)
            elif tag == 'd_psi_n':
                n = p[2] if len(p) > 2 else best_params[2]
                fn = _make_E_psi_n(Om, n)
            elif tag == 'model_d':
                amp = p[2] if len(p) > 2 else best_params[2]
                beta = p[3] if len(p) > 3 else best_params[3]
                fn = _make_E_D(Om, amp, beta)
            elif tag == 'd_mix':
                eps = p[2] if len(p) > 2 else best_params[2]
                n = p[3] if len(p) > 3 else best_params[3]
                fn = _make_E_mix(Om, eps, n)
            else:
                return 1e9
            if fn is None:
                return 1e9
            return _tot(fn, Om, H0)

        def obj_lcdm(p):
            Om, H0 = p
            if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
                return 1e9
            return _tot_lcdm(Om, H0)

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
    Om_w = best_p[0]; H0_w = best_p[1]
    k_win = 2 if winner_tag in ('d_psi1', 'd_psi2') else (
            3 if winner_tag in ('d_psi_n', 'g_theory') else 4)

    Om_l = lcdm_result['Om']; H0_l = lcdm_result['H0']
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
        s0  = [Om_w + rng.normal(0, 0.01), H0_w + rng.normal(0, 0.5)] + list(best_p[2:])
        boot_items.append((s0, nb, nc, nr, winner_tag, best_p, k_win))

    bsz     = max(1, N_BOOT // N_WORKERS)
    batches = [boot_items[i:i+bsz] for i in range(0, N_BOOT, bsz)]
    raw     = pool.map(_boot_worker, batches)

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
# Task 7: w(z) plot
# ──────────────────────────────────────────────────────────────────────────────
def task7_wz_plot(results, lcdm_aicc, cpl_result, out_dir):
    print('\n' + '='*60)
    print('Task 7: w(z) Visualization')
    print('='*60)

    z_plot = np.linspace(0.01, 2.0, 300)
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.axhline(-1.0, color='k', ls='--', lw=1, label='LCDM (w=-1)')

    # Son et al. CPL region (approx 95% CI)
    w0_s, wa_s = SON_W0, SON_WA
    w_son = w0_s + wa_s * z_plot / (1.0 + z_plot)
    ax.plot(z_plot, w_son, 'k-', lw=2, label=f'Son+25 CPL (w0={w0_s}, wa={wa_s})')
    ax.fill_between(z_plot,
                    (w0_s - SON_W0_2SIG) + (wa_s - SON_WA_2SIG)*z_plot/(1+z_plot),
                    (w0_s + SON_W0_2SIG) + (wa_s + SON_WA_2SIG)*z_plot/(1+z_plot),
                    alpha=0.15, color='k', label='Son+25 2-sigma region')

    # CPL fit
    if cpl_result and cpl_result.get('w0') is not None:
        w0_c, wa_c = cpl_result['w0'], cpl_result['wa']
        ax.plot(z_plot, w0_c + wa_c*z_plot/(1+z_plot), 'C5', ls='-.',
                lw=1.5, label=f'CPL fit (w0={w0_c:.2f}, wa={wa_c:.2f})')

    styles = {'model_d': ('C4', '-.', 'Model D'),
              'd_psi1':  ('C2', '--', 'D_psi1 (n=1)'),
              'd_psi2':  ('C0', '-',  'D_psi2 (n=2) CORE'),
              'd_psi_n': ('C1', '--', 'D_psi_n (n free)'),
              'd_mix':   ('C3', ':',  'D_mix'),
              'g_theory':('C6', '-',  'G_theory_corr')}

    for tag, (col, ls, lab) in styles.items():
        r = results.get(tag, {})
        w0 = r.get('w0'); wa = r.get('wa')
        if w0 is None or wa is None:
            continue
        ax.plot(z_plot, w0 + wa*z_plot/(1+z_plot), col, ls=ls, lw=1.5,
                label=f'{lab} (w0={w0:.2f}, wa={wa:.2f})')

    ax.set_xlabel('z')
    ax.set_ylabel('w(z)')
    ax.set_title('L43: SQT models vs Son et al. 2025 (age-corrected)')
    ax.legend(fontsize=7, loc='best')
    ax.set_ylim(-4.0, 0.5)
    ax.grid(alpha=0.3)

    out = os.path.join(out_dir, 'l43_task7_wz.png')
    fig.savefig(out, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f'  Plot: {out}')
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 9: w0-wa plane contours
# ──────────────────────────────────────────────────────────────────────────────
def task9_w0wa_contour(results, cpl_result, out_dir):
    print('\n' + '='*60)
    print('Task 9: w0-wa plane')
    print('='*60)

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.axvline(-1.0, color='k', ls=':', lw=0.8, alpha=0.5)
    ax.axhline(0.0,  color='k', ls=':', lw=0.8, alpha=0.5)
    ax.plot(-1.0, 0.0, 'k+', ms=12, label='LCDM')

    # Son et al. target region (approx 1sigma and 2sigma ellipses)
    w0_s, wa_s = SON_W0, SON_WA
    ax.plot(w0_s, wa_s, 'ks', ms=10, label=f'Son+25 ({w0_s}, {wa_s})')
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(w0_s + SON_W0_2SIG/2*np.cos(theta),
            wa_s + SON_WA_2SIG/2*np.sin(theta), 'k-', lw=1, alpha=0.5)
    ax.plot(w0_s + SON_W0_2SIG*np.cos(theta),
            wa_s + SON_WA_2SIG*np.sin(theta), 'k--', lw=1, alpha=0.3,
            label='Son+25 1/2sigma')

    # DESI DR2 reference
    ax.plot(-0.757, -0.83, 'g^', ms=8, label='DESI DR2 (-0.757, -0.83)')

    # CPL fit
    if cpl_result and cpl_result.get('w0') is not None:
        ax.plot(cpl_result['w0'], cpl_result['wa'], 'C5*', ms=12,
                label=f"CPL fit ({cpl_result['w0']:.2f}, {cpl_result['wa']:.2f})")

    colors = {'model_d': 'C4', 'd_psi1': 'C2', 'd_psi2': 'C0',
              'd_psi_n': 'C1', 'd_mix': 'C3', 'g_theory': 'C6'}
    labels = {'model_d': 'Model D', 'd_psi1': 'D_psi1 (n=1)', 'd_psi2': 'D_psi2 (n=2)',
              'd_psi_n': 'D_psi_n', 'd_mix': 'D_mix', 'g_theory': 'G_theory'}
    for tag, col in colors.items():
        r = results.get(tag, {})
        w0 = r.get('w0'); wa = r.get('wa')
        if w0 is None or wa is None:
            continue
        ax.plot(w0, wa, 'o', color=col, ms=9,
                label=f"{labels[tag]} ({w0:.2f}, {wa:.2f})")

    ax.set_xlabel('w0')
    ax.set_ylabel('wa')
    ax.set_title('L43: w0-wa plane (Son et al. 2025 age correction)')
    ax.legend(fontsize=8, loc='best')
    ax.set_xlim(-3.0, 0.5)
    ax.set_ylim(-5.0, 3.0)
    ax.grid(alpha=0.3)

    out = os.path.join(out_dir, 'l43_task9_w0wa.png')
    fig.savefig(out, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f'  Plot: {out}')
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 10: q0 comparison
# ──────────────────────────────────────────────────────────────────────────────
def task10_q0(results, cpl_result):
    print('\n' + '='*60)
    print('Task 10: q0 (deceleration parameter) comparison')
    print('='*60)
    print(f'  Son et al. 2025 target: q0 = {SON_Q0:+.2f} (deceleration)')
    print(f'  LCDM standard:          q0 = -0.53 (acceleration)')
    print()
    print(f'  {"Model":<20} {"w0":>8} {"wa":>8} {"q0":>8}  Son+25?')
    print('  ' + '-'*55)

    if cpl_result and cpl_result.get('w0') is not None:
        w0_c = cpl_result['w0']; wa_c = cpl_result['wa']
        Om_c = cpl_result.get('Om', 0.31)
        q0_c = _q0(Om_c, w0_c)
        agrees = 'YES' if q0_c > 0 else ('NEAR' if q0_c > -0.1 else 'NO')
        print(f'  {"CPL fit":<20} {w0_c:>8.3f} {wa_c:>8.3f} {q0_c:>8.3f}  {agrees}')

    tags_labels = [('model_d', 'Model D'), ('d_psi1', 'D_psi1 (n=1)'),
                   ('d_psi2', 'D_psi2 (n=2)'), ('d_psi_n', 'D_psi_n'),
                   ('d_mix', 'D_mix'), ('g_theory', 'G_theory')]
    for tag, lab in tags_labels:
        r = results.get(tag, {})
        w0 = r.get('w0'); q0_val = r.get('q0')
        wa = r.get('wa', float('nan'))
        if w0 is None:
            continue
        if q0_val is None:
            Om_ = r['params'][0] if r.get('params') else 0.31
            q0_val = _q0(Om_, w0)
        agrees = 'YES' if q0_val > 0 else ('NEAR' if q0_val > -0.1 else 'NO')
        print(f'  {lab:<20} {w0:>8.3f} {wa:>8.3f} {q0_val:>8.3f}  {agrees}')

    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Pre-Task: Verify Son et al. correction
# ──────────────────────────────────────────────────────────────────────────────
def pretask_verify():
    print('\n' + '='*60)
    print('Pre-Task: Son et al. 2025 age-bias correction verification')
    print('='*60)
    for z in [0.0, 0.5, 1.0, 2.0]:
        dm, se = son_age_correction(np.array([z]))
        print(f'  z={z:.1f}: delta_age={SON_DAGE_AMP*(1-np.exp(-SON_DAGE_TAU*z)):.2f} Gyr'
              f'  delta_m={float(dm):.4f} mag  sigma_extra={float(se):.4f} mag')
    # Verify vs Son et al. Fig.2: z=1 -> delta_age~5.3*(1-exp(-2.5))~4.7 Gyr, delta_m~0.14
    dm1, _ = son_age_correction(np.array([1.0]))
    print(f'\n  z=1 check: delta_m={float(dm1):.4f} mag (expected ~0.14 mag)')
    print(f'  [{"CONFIRMED" if abs(float(dm1) - 0.14) < 0.04 else "CHECK"}]')
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    OUT_DIR = _SCRIPT_DIR

    print('='*60)
    print('L43: Son et al. 2025 age-bias + SQT psi^n a priori test')
    print(f'8-worker parallel  |  LCDM baseline AICc={LCDM_AICC_OLD:.4f} (uncorrected)')
    print('='*60)
    sys.stdout.flush()

    pretask_verify()

    ctx  = mp.get_context('spawn')
    pool = ctx.Pool(N_WORKERS)

    try:
        # ── Task 0: baselines ──
        r0 = task0_baselines(pool)
        lcdm_aicc_corr = r0['lcdm_aicc']
        lcdm_result    = r0['lcdm']
        cpl_result     = r0['cpl']

        # ── Tasks 1-6: model fits ──
        t16 = tasks1to6_fits(pool, lcdm_aicc_corr)

        # ── Report each model ──
        res = {}

        res['model_d'] = _report_model(
            'model_d', 'Model D (k=4, refit)', 4,
            ['Om', 'H0', 'amp', 'beta'], _BND_D,
            *t16['model_d'], lcdm_aicc_corr, cpl_result)

        res['d_psi1'] = _report_model(
            'd_psi1', 'D_psi1 (k=2, n=1 a priori)', 2,
            ['Om', 'H0'], _BND_PSI1,
            *t16['d_psi1'], lcdm_aicc_corr, cpl_result)

        res['d_psi2'] = _report_model(
            'd_psi2', 'D_psi2 (k=2, n=2 a priori) CORE', 2,
            ['Om', 'H0'], _BND_PSI2,
            *t16['d_psi2'], lcdm_aicc_corr, cpl_result)

        res['d_psi_n'] = _report_model(
            'd_psi_n', 'D_psi_n (k=3, n free)', 3,
            ['Om', 'H0', 'n'], _BND_PSIN,
            *t16['d_psi_n'], lcdm_aicc_corr, cpl_result)

        res['d_mix'] = _report_model(
            'd_mix', 'D_mix (k=4, eps+psi^n)', 4,
            ['Om', 'H0', 'eps', 'n'], _BND_MIX,
            *t16['d_mix'], lcdm_aicc_corr, cpl_result)

        res['g_theory'] = _report_model(
            'g_theory', 'G_theory_corr (k=3, V(psi))', 3,
            ['Om', 'H0', 'mu2'], _BND_GTH,
            *t16['g_theory'], lcdm_aicc_corr, cpl_result)

        # ── Find best SQT model ──
        sqt_tags = ['d_psi2', 'd_psi1', 'd_psi_n', 'd_mix', 'model_d', 'g_theory']
        best_sqt_tag = min(
            [t for t in sqt_tags if res[t].get('daicc') is not None],
            key=lambda t: res[t]['daicc'],
            default=None)

        # ── Task 7: w(z) plot ──
        task7_wz_plot(res, lcdm_aicc_corr, cpl_result, OUT_DIR)

        # ── Task 8: Bootstrap (if winner dAICc < -2) ──
        r8 = None
        if best_sqt_tag and res[best_sqt_tag].get('daicc', 0) < -2:
            r8 = task8_bootstrap(pool, best_sqt_tag, res[best_sqt_tag], lcdm_result)
        else:
            best_d = res[best_sqt_tag]['daicc'] if best_sqt_tag else 'N/A'
            print(f'\nTask 8: Bootstrap -- SKIPPED (best dAICc={best_d} >= -2)')

        # ── Task 9: w0-wa contour ──
        task9_w0wa_contour(res, cpl_result, OUT_DIR)

        # ── Task 10: q0 comparison ──
        task10_q0(res, cpl_result)

    finally:
        pool.close()
        pool.join()

    # ── Summary ──
    print('\n' + '='*60)
    print('L43 RESULTS SUMMARY')
    print('='*60)

    print(f'\n[Pre-Task] Son et al. correction: verified')
    print(f'\n[Task 0] Baselines (corrected data)')
    print(f'  LCDM: AICc={lcdm_aicc_corr:.2f}  '
          f'(prev={LCDM_AICC_OLD:.2f}, change={lcdm_aicc_corr - LCDM_AICC_OLD:+.2f})')
    if cpl_result.get('w0') is not None:
        print(f"  CPL:  AICc={cpl_result['aicc']:.2f}  dAICc={cpl_result['daicc_vs_lcdm']:.2f}")
        print(f"        w0={cpl_result['w0']:.3f}, wa={cpl_result['wa']:.3f}")
        print(f"  Son+25 target: w0={SON_W0}, wa={SON_WA}, q0={SON_Q0:+.2f}")

    print('\n[Tasks 1-6] Model fits (corrected data)')
    tag_labels = [('model_d', 'Model D k=4'), ('d_psi1', 'D_psi1 k=2'),
                  ('d_psi2', 'D_psi2 k=2 CORE'), ('d_psi_n', 'D_psi_n k=3'),
                  ('d_mix', 'D_mix k=4'), ('g_theory', 'G_theory k=3')]
    for tag, lab in tag_labels:
        r = res.get(tag, {})
        d = r.get('daicc')
        w0 = r.get('w0'); wa = r.get('wa')
        q0v = r.get('q0')
        v = r.get('verdict', '?')
        if d is not None:
            line = f'  {lab:<22}  dAICc={d:+8.2f}  [{v}]'
            if w0 is not None:
                line += f'  w0={w0:.3f} wa={wa:.3f}'
            if q0v is not None:
                line += f'  q0={q0v:+.3f}'
            print(line)
        else:
            print(f'  {lab:<22}  FAILED')

    if best_sqt_tag:
        best_r = res[best_sqt_tag]
        print(f'\n[Best SQT model] {best_sqt_tag}  dAICc={best_r["daicc"]:.2f}')
        if r8:
            print(f'[Bootstrap]  median={r8.get("median", "?"):.2f}  '
                  f'frac<-4={r8.get("frac_lt4", 0)*100:.1f}%  {r8.get("verdict", "?")}')

    # n_fit for D_psi_n
    r_psin = res.get('d_psi_n', {})
    if r_psin.get('params') is not None:
        n_fit = r_psin['params'][2]
        print(f'\n[D_psi_n] n_fit={n_fit:.3f}  (theory n=2, deviation={(n_fit-2)/2*100:+.1f}%)')

    # Final verdict
    print('\n[Final Verdict]')
    if best_sqt_tag:
        d = res[best_sqt_tag]['daicc']
        v = res[best_sqt_tag]['verdict']
        w0_ = res[best_sqt_tag].get('w0')
        wa_ = res[best_sqt_tag].get('wa')
        print(f'  Best SQT: {best_sqt_tag}  dAICc={d:.2f}  [{v}]')

        if d < -10 and best_sqt_tag == 'd_psi2':
            scenario = 'alpha: Q93 TRIUMPH -- SQT n=2 a priori, Nature candidate'
        elif d < -4:
            scenario = 'beta: Q92 GAME -- CPL competitive, JCAP enhancement'
        elif d < 0:
            scenario = 'gamma: Q91/Q90 STRONG -- partial success, JCAP possible'
        else:
            scenario = 'delta: K90 KILL -- all SQT fail, Model D phenomenological path'
        print(f'  Scenario: {scenario}')

        if w0_ is not None:
            dson = abs(w0_ - SON_W0) / SON_W0_2SIG
            print(f'  Son+25 w0 compatibility: {dson:.1f}sigma')

    print(f'\n  L33-L42 re-evaluation:')
    lcdm_change = lcdm_aicc_corr - LCDM_AICC_OLD
    print(f'  LCDM AICc changed by {lcdm_change:+.2f} after age correction')
    if lcdm_change > 50:
        print(f'  Age bias had LARGE effect on previous results')
    elif lcdm_change > 10:
        print(f'  Age bias had MODERATE effect on previous results')
    else:
        print(f'  Age bias had SMALL effect on previous results')

    # Save JSON
    save = {
        'task0': _jsonify(r0),
        'task1_model_d': _jsonify(res.get('model_d')),
        'task2_d_psi1':  _jsonify(res.get('d_psi1')),
        'task3_d_psi2':  _jsonify(res.get('d_psi2')),
        'task4_d_psi_n': _jsonify(res.get('d_psi_n')),
        'task5_d_mix':   _jsonify(res.get('d_mix')),
        'task6_g_theory':_jsonify(res.get('g_theory')),
        'task8_bootstrap': _jsonify(r8),
        'lcdm_aicc_old': LCDM_AICC_OLD,
        'lcdm_aicc_corr': lcdm_aicc_corr,
        'son_params': {'w0': SON_W0, 'wa': SON_WA, 'q0': SON_Q0},
    }
    out_json = os.path.join(OUT_DIR, 'l43_results.json')
    with open(out_json, 'w') as f:
        json.dump(save, f, indent=2)
    print(f'\nSaved: {out_json}')
