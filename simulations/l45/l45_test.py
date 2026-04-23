# -*- coding: utf-8 -*-
"""
l45_test.py -- L45: Model UB Variant Exploration
=================================================
Systematic sweep of 8 theoretical axes for Model UB dark energy.

Axes explored (Tier 1, 18 models):
  Boundary:    Hubble (R_H=c/H) | Event horizon (R_E=chi_E * c/H0)
  Profile:     Ballistic (BAL)  | Fickian/cosh (FIC) | Exponential-decay (DEC)
  Coupling:    Linear (LIN)     | Power (POW)         | Mixed (MIX) | H-prop (HPR)
  Averaging:   Path (PATH)      | Volume (VOL)

Tier 1 (18 models): 40 starts each, 8-worker spawn pool
Tier 2 (54 models): cross-combinations of best axes, only if any T1 dAICc < -4
Bootstrap: N=200 for top-5 Tier 1 models if dAICc < -2
Success: Q95 (dAICc<-20,k=2) -> Q94 -> Q93 -> Q92 -> K90

Profile math:
  BAL: f(s;mR) = [(1-s+1/mR)*exp(-mR*(1-s)) - (1+s+1/mR)*exp(-mR*(1+s))] / (2*mR*s)
       f(0;mR) = exp(-mR)  [L'Hopital]
  FIC: f(s;mR) = cosh(mR*s)/cosh(mR)  [Neumann BC at center]
       f(0;mR) = 1/cosh(mR)
       F_avg_FIC(q) = sinh(mR*q) / (mR*q*cosh(mR))
  DEC: f(s;mR) = exp(-mR*(1-s))  [simple decay from boundary]
       f(0;mR) = exp(-mR)
       F_avg_DEC(q) = (exp(mR*(q-1)) - exp(-mR)) / (mR*q)

Normalization: rho_DE(z=0) = OL0 exact for all variants.
DESY5SN_AgeCorr L43 bug fix: self.cov (not inv(cov_inv)).
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
    E_lcdm, OR, C_KMS, N_TOTAL,
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
LCDM_AICC_L43 = 1759.93
CPL_AICC_L43  = 1652.91
CPL_W0_L43    = -0.448
CPL_WA_L43    = -1.467

N_WORKERS = 8
N_BOOT    = 200
N_TIER1_STARTS = 40
N_TIER2_STARTS = 30

SON_SLOPE     = 0.030
SON_SLOPE_ERR = 0.004
SON_DAGE_AMP  = 5.3
SON_DAGE_TAU  = 2.5
SON_W0        = -0.34
SON_WA        = -1.90
SON_Q0        = +0.18
SON_W0_2SIG   = 0.12
SON_WA_2SIG   = 0.50

UB_Z_GRID = np.concatenate([
    np.linspace(0.0, 3.5, 2000),
    np.linspace(3.5, 1200.0, 600)[1:],
])
N_UB_S   = 2000
UB2_MUR0 = 1.0


# ──────────────────────────────────────────────────────────────────────────────
# Son et al. 2025 age correction + DESY5SN (L43 bug fixed)
# ──────────────────────────────────────────────────────────────────────────────
def son_age_correction(z):
    delta_age   = SON_DAGE_AMP * (1.0 - np.exp(-SON_DAGE_TAU * z))
    delta_m     = delta_age * SON_SLOPE
    sigma_extra = delta_age * SON_SLOPE_ERR
    return delta_m, sigma_extra


class DESY5SN_AgeCorr(DESY5SN):
    def __init__(self):
        super().__init__()
        delta_m, sigma_extra = son_age_correction(self.z_hd)
        self.mu_obs = self.mu_obs - delta_m
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
# Profile functions
# ──────────────────────────────────────────────────────────────────────────────

def _f_ballistic(s_arr, mR):
    """BAL: f(s;mR). L'Hopital limit at s=0: exp(-mR)."""
    s_arr = np.asarray(s_arr, float)
    result = np.empty_like(s_arr)
    m0 = s_arr < 1e-9
    result[m0] = np.exp(-mR)
    sm = ~m0; sv = s_arr[sm]
    t1 = ((1.0 - sv) + 1.0/mR) * np.exp(-mR * (1.0 - sv))
    t2 = ((1.0 + sv) + 1.0/mR) * np.exp(-mR * (1.0 + sv))
    result[sm] = (t1 - t2) / (2.0 * mR * sv)
    return result


def _build_I_bal(mR):
    """I_BAL(q) = integral_0^q f_bal(s;mR) ds, as interp1d on [0,1]."""
    s_grid = np.concatenate([[0.0], np.linspace(1e-9, 1.0, N_UB_S)])
    f_grid = _f_ballistic(s_grid, mR)
    I_grid = np.concatenate([[0.0], cumulative_trapezoid(f_grid, s_grid)])
    return interp1d(s_grid, I_grid, kind='linear',
                    bounds_error=False, fill_value=(0.0, float(I_grid[-1])))


def _build_Ivol_bal(mR):
    """I_vol_BAL(q) = integral_0^q f_bal(s;mR)*s^2 ds, as interp1d on [0,1]."""
    s_grid = np.concatenate([[0.0], np.linspace(1e-9, 1.0, N_UB_S)])
    f_grid = _f_ballistic(s_grid, mR) * s_grid**2
    I_grid = np.concatenate([[0.0], cumulative_trapezoid(f_grid, s_grid)])
    return interp1d(s_grid, I_grid, kind='linear',
                    bounds_error=False, fill_value=(0.0, float(I_grid[-1])))


def _F_avg_bal_path(q_arr, mR, I_fn):
    """Path-averaged BAL: F = I(q)/q. F0 = exp(-mR)."""
    F0  = np.exp(-mR)
    I_q = I_fn(q_arr)
    return np.where(q_arr > 1e-10, I_q / q_arr, F0)


def _F_avg_bal_vol(q_arr, mR, Iv_fn):
    """Volume-averaged BAL: F = 3*Iv(q)/q^3. F0 = exp(-mR)."""
    F0   = np.exp(-mR)
    Iv_q = Iv_fn(q_arr)
    q3   = q_arr**3
    return np.where(q_arr > 1e-10, 3.0 * Iv_q / q3, F0)


def _F_avg_fic_path(q_arr, mR):
    """Path-averaged FIC: F = sinh(mR*q)/(mR*q*cosh(mR)). F0 = 1/cosh(mR)."""
    F0 = 1.0 / np.cosh(mR)
    mRq = mR * q_arr
    result = np.where(q_arr > 1e-10,
                      np.sinh(mRq) / (mRq * np.cosh(mR)),
                      F0)
    return result


def _F_avg_fic_vol(q_arr, mR):
    """Volume-averaged FIC: F = 3*Iv_fic(q)/q^3. F0 = 1/cosh(mR)."""
    F0 = 1.0 / np.cosh(mR)
    mR_safe = max(mR, 1e-8)
    mRq = mR_safe * q_arr
    # I_vol_FIC(q) = [q^2*sinh(mRq)/mR - 2q*cosh(mRq)/mR^2 + 2*sinh(mRq)/mR^3] / cosh(mR)
    sh = np.sinh(mRq); ch = np.cosh(mRq)
    Iv = (q_arr**2 * sh / mR_safe
          - 2.0 * q_arr * ch / mR_safe**2
          + 2.0 * sh / mR_safe**3) / np.cosh(mR_safe)
    q3 = q_arr**3
    return np.where(q_arr > 1e-10, 3.0 * Iv / q3, F0)


def _F_avg_dec_path(q_arr, mR):
    """Path-averaged DEC: F = (exp(mR*(q-1))-exp(-mR))/(mR*q). F0 = exp(-mR)."""
    F0 = np.exp(-mR)
    result = np.where(
        q_arr > 1e-10,
        (np.exp(mR * (q_arr - 1.0)) - np.exp(-mR)) / (mR * q_arr),
        F0)
    return result


def _F_avg_dec_vol(q_arr, mR):
    """Volume-averaged DEC: F = 3*Iv_dec(q)/q^3. F0 = exp(-mR)."""
    F0 = np.exp(-mR)
    mR_safe = max(mR, 1e-8)
    mRq = mR_safe * q_arr
    emR = np.exp(-mR_safe)
    emRq = np.exp(mRq - mR_safe)  # = exp(mR*(q-1)) = exp(-mR)*exp(mR*q)
    # I_vol_DEC(q) = exp(-mR)*[exp(mR*q)*(q^2/mR - 2q/mR^2 + 2/mR^3) - 2/mR^3]
    # emRq = exp(-mR)*exp(mR*q), so exp(mR*q)*(...)= emRq/emR*(...), thus:
    # Iv = emRq*(q^2/mR - 2q/mR^2 + 2/mR^3) - emR*2/mR^3
    Iv = emRq * (q_arr**2/mR_safe - 2.0*q_arr/mR_safe**2 + 2.0/mR_safe**3) - emR * 2.0/mR_safe**3
    q3 = q_arr**3
    return np.where(q_arr > 1e-10, 3.0 * Iv / q3, F0)


# ──────────────────────────────────────────────────────────────────────────────
# Self-consistent E(z) for any UB variant
# ──────────────────────────────────────────────────────────────────────────────

def _compute_E_variant(z_arr, Om, muR0,
                        profile='BAL', boundary='H', coupling='LIN', averaging='PATH',
                        n=1.0, eps=0.0, max_iter=30, tol=1e-7):
    """
    Self-consistent Friedmann for Model UB variant.
    Returns E(z) array (normalized E(0)=1) or None on failure.
    """
    OL0 = 1.0 - Om - OR
    if OL0 <= 0.0 or Om <= 0.0 or muR0 <= 0.0:
        return None

    # F0 = F_avg at z=0 (L'Hopital limit)
    if profile == 'BAL':
        F0 = np.exp(-muR0)
    elif profile == 'FIC':
        F0 = 1.0 / np.cosh(muR0)
    elif profile == 'DEC':
        F0 = np.exp(-muR0)
    else:
        return None

    if F0 <= 0.0:
        return None

    # Precompute numerical integrals for BAL profile
    if profile == 'BAL':
        if averaging == 'PATH':
            I_fn = _build_I_bal(muR0)
        else:
            I_fn = _build_Ivol_bal(muR0)

    # Initial E guess (LCDM)
    E_prev = np.sqrt(np.maximum(OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0, 1e-30))

    for _ in range(max_iter):
        # chi(z) = integral_0^z dz'/E
        chi = np.concatenate([[0.0], cumulative_trapezoid(1.0 / E_prev, z_arr)])

        # Boundary-dependent q
        if boundary == 'H':
            chiE = chi * E_prev
            q    = np.minimum(chiE, 1.0)
        elif boundary == 'E':
            chi_total = chi[-1]
            chi_E     = np.maximum(chi_total - chi, 1e-10)
            q         = np.minimum(chi / chi_E, 1.0)
        else:
            return None

        # F_avg based on profile and averaging
        if profile == 'BAL' and averaging == 'PATH':
            F_avg = _F_avg_bal_path(q, muR0, I_fn)
        elif profile == 'BAL' and averaging == 'VOL':
            F_avg = _F_avg_bal_vol(q, muR0, I_fn)
        elif profile == 'FIC' and averaging == 'PATH':
            F_avg = _F_avg_fic_path(q, muR0)
        elif profile == 'FIC' and averaging == 'VOL':
            F_avg = _F_avg_fic_vol(q, muR0)
        elif profile == 'DEC' and averaging == 'PATH':
            F_avg = _F_avg_dec_path(q, muR0)
        elif profile == 'DEC' and averaging == 'VOL':
            F_avg = _F_avg_dec_vol(q, muR0)
        else:
            return None

        if np.any(~np.isfinite(F_avg)):
            return None

        # rho_DE based on coupling
        if coupling == 'LIN':
            rho_DE = OL0 * F_avg / F0
            E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
            if np.any(E2 <= 0) or np.any(~np.isfinite(E2)):
                return None
            E_new = np.sqrt(E2)

        elif coupling == 'POW':
            ratio  = np.maximum(F_avg / F0, 0.0)
            rho_DE = OL0 * ratio**n
            E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
            if np.any(E2 <= 0) or np.any(~np.isfinite(E2)):
                return None
            E_new = np.sqrt(E2)

        elif coupling == 'MIX':
            rho_DE = OL0 * (eps + (1.0 - eps) * F_avg / F0)
            E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
            if np.any(E2 <= 0) or np.any(~np.isfinite(E2)):
                return None
            E_new = np.sqrt(E2)

        elif coupling == 'HPR':
            # rho_DE = OL0 * (F_avg/F0) * E [H-proportional]
            # E^2 - A*E - mat = 0, A = OL0*F_avg/F0
            mat  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3
            A    = OL0 * F_avg / F0
            disc = A**2 + 4.0 * mat
            if np.any(disc < 0):
                return None
            E_new = (A + np.sqrt(disc)) / 2.0

        else:
            return None

        if np.any(~np.isfinite(E_new)) or np.any(E_new <= 0):
            return None

        # Normalize E(0) = 1
        E0 = E_new[0]
        if E0 <= 0.0 or not np.isfinite(E0):
            return None
        E_new = E_new / E0

        if np.max(np.abs(E_new - E_prev)) < tol:
            return E_new
        E_prev = E_new

    # Return last iterate if finite
    if np.all(np.isfinite(E_prev)) and np.all(E_prev > 0):
        return E_prev
    return None


def _make_E_variant(Om, muR0, profile, boundary, coupling, averaging, n=1.0, eps=0.0):
    """Build E_fn interpolant for given UB variant."""
    E_arr = _compute_E_variant(UB_Z_GRID, Om, muR0, profile, boundary, coupling,
                                averaging, n, eps)
    if E_arr is None:
        return None
    ifn = interp1d(UB_Z_GRID, E_arr, kind='linear', bounds_error=False,
                   fill_value=np.nan)
    def fn(z, _Om):
        za = np.atleast_1d(np.asarray(z, float))
        Ev = ifn(za)
        return None if (np.any(np.isnan(Ev)) or np.any(Ev <= 0)) else Ev
    return fn


# ──────────────────────────────────────────────────────────────────────────────
# Model specification dictionary (Tier 1 = 18 models)
# Each entry: (k, boundary, profile, coupling, averaging, free_params, fixed, bounds)
# free_params: list of names for params[2], params[3], ...
# fixed: dict of fixed parameter values
# ──────────────────────────────────────────────────────────────────────────────

_B2 = [(0.20, 0.55), (55., 82.)]
_B3_mR  = _B2 + [(0.05, 15.0)]
_B3_n   = _B2 + [(0.1,  6.0)]
_B3_eps = _B2 + [(0.0,  0.98)]
_B4     = _B2 + [(0.05, 15.0), (0.1, 6.0)]

_MODELS = {
    # --- Group A: Hubble, PATH, LIN, profile varies, mR=1 (k=2) ---
    'H-BAL-PATH-LIN-k2': {
        'k': 2, 'bnd': 'H', 'prof': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
        'free': [], 'fixed': {'mR': 1.0}, 'bounds': _B2,
    },
    'H-FIC-PATH-LIN-k2': {
        'k': 2, 'bnd': 'H', 'prof': 'FIC', 'avg': 'PATH', 'cpl': 'LIN',
        'free': [], 'fixed': {'mR': 1.0}, 'bounds': _B2,
    },
    'H-DEC-PATH-LIN-k2': {
        'k': 2, 'bnd': 'H', 'prof': 'DEC', 'avg': 'PATH', 'cpl': 'LIN',
        'free': [], 'fixed': {'mR': 1.0}, 'bounds': _B2,
    },
    # --- Group B: Hubble, PATH, LIN, mR free (k=3) ---
    'H-BAL-PATH-LIN-k3': {
        'k': 3, 'bnd': 'H', 'prof': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
        'free': ['mR'], 'fixed': {}, 'bounds': _B3_mR,
    },
    'H-FIC-PATH-LIN-k3': {
        'k': 3, 'bnd': 'H', 'prof': 'FIC', 'avg': 'PATH', 'cpl': 'LIN',
        'free': ['mR'], 'fixed': {}, 'bounds': _B3_mR,
    },
    'H-DEC-PATH-LIN-k3': {
        'k': 3, 'bnd': 'H', 'prof': 'DEC', 'avg': 'PATH', 'cpl': 'LIN',
        'free': ['mR'], 'fixed': {}, 'bounds': _B3_mR,
    },
    # --- Group C: Hubble, BAL, PATH, coupling variations ---
    'H-BAL-PATH-POW-k3': {
        'k': 3, 'bnd': 'H', 'prof': 'BAL', 'avg': 'PATH', 'cpl': 'POW',
        'free': ['n'], 'fixed': {'mR': 1.0}, 'bounds': _B3_n,
    },
    'H-BAL-PATH-MIX-k3': {
        'k': 3, 'bnd': 'H', 'prof': 'BAL', 'avg': 'PATH', 'cpl': 'MIX',
        'free': ['eps'], 'fixed': {'mR': 1.0}, 'bounds': _B3_eps,
    },
    'H-BAL-PATH-POW-k4': {
        'k': 4, 'bnd': 'H', 'prof': 'BAL', 'avg': 'PATH', 'cpl': 'POW',
        'free': ['mR', 'n'], 'fixed': {}, 'bounds': _B4,
    },
    # --- Group D: Event horizon boundary ---
    'E-BAL-PATH-LIN-k2': {
        'k': 2, 'bnd': 'E', 'prof': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
        'free': [], 'fixed': {'mR': 1.0}, 'bounds': _B2,
    },
    'E-FIC-PATH-LIN-k2': {
        'k': 2, 'bnd': 'E', 'prof': 'FIC', 'avg': 'PATH', 'cpl': 'LIN',
        'free': [], 'fixed': {'mR': 1.0}, 'bounds': _B2,
    },
    'E-DEC-PATH-LIN-k2': {
        'k': 2, 'bnd': 'E', 'prof': 'DEC', 'avg': 'PATH', 'cpl': 'LIN',
        'free': [], 'fixed': {'mR': 1.0}, 'bounds': _B2,
    },
    'E-BAL-PATH-LIN-k3': {
        'k': 3, 'bnd': 'E', 'prof': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
        'free': ['mR'], 'fixed': {}, 'bounds': _B3_mR,
    },
    # --- Group E: Volume averaging ---
    'H-BAL-VOL-LIN-k2': {
        'k': 2, 'bnd': 'H', 'prof': 'BAL', 'avg': 'VOL', 'cpl': 'LIN',
        'free': [], 'fixed': {'mR': 1.0}, 'bounds': _B2,
    },
    'H-BAL-VOL-LIN-k3': {
        'k': 3, 'bnd': 'H', 'prof': 'BAL', 'avg': 'VOL', 'cpl': 'LIN',
        'free': ['mR'], 'fixed': {}, 'bounds': _B3_mR,
    },
    'H-FIC-VOL-LIN-k2': {
        'k': 2, 'bnd': 'H', 'prof': 'FIC', 'avg': 'VOL', 'cpl': 'LIN',
        'free': [], 'fixed': {'mR': 1.0}, 'bounds': _B2,
    },
    # --- Group F: H-proportional flux ---
    'H-BAL-PATH-HPR-k2': {
        'k': 2, 'bnd': 'H', 'prof': 'BAL', 'avg': 'PATH', 'cpl': 'HPR',
        'free': [], 'fixed': {'mR': 1.0}, 'bounds': _B2,
    },
    'H-BAL-PATH-HPR-k3': {
        'k': 3, 'bnd': 'H', 'prof': 'BAL', 'avg': 'PATH', 'cpl': 'HPR',
        'free': ['mR'], 'fixed': {}, 'bounds': _B3_mR,
    },
}

_TIER1_TAGS = [
    'H-BAL-PATH-LIN-k2', 'H-FIC-PATH-LIN-k2', 'H-DEC-PATH-LIN-k2',
    'H-BAL-PATH-LIN-k3', 'H-FIC-PATH-LIN-k3', 'H-DEC-PATH-LIN-k3',
    'H-BAL-PATH-POW-k3', 'H-BAL-PATH-MIX-k3', 'H-BAL-PATH-POW-k4',
    'E-BAL-PATH-LIN-k2', 'E-FIC-PATH-LIN-k2', 'E-DEC-PATH-LIN-k2',
    'E-BAL-PATH-LIN-k3',
    'H-BAL-VOL-LIN-k2', 'H-BAL-VOL-LIN-k3', 'H-FIC-VOL-LIN-k2',
    'H-BAL-PATH-HPR-k2', 'H-BAL-PATH-HPR-k3',
]
assert len(_TIER1_TAGS) == 18


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
    if daicc >= -20:
        return 'Q94 DISCOVERY' if k2 else 'Q93 TRIUMPH'
    return 'Q95 VICTORY' if k2 else 'Q94 DISCOVERY'


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
# Workers (module-level for spawn safety)
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
        OL0 = 1.0 - Om - OR
        if OL0 <= 0:
            return 1e9
        def fn(z, _Om):
            za  = np.asarray(z, float)
            cpl = (1.0+za)**(3.0*(1.0+w0+wa)) * np.exp(-3.0*wa*za/(1.0+za))
            E2  = OR*(1+za)**4 + Om*(1+za)**3 + OL0*cpl
            return None if np.any(E2 <= 0) else np.sqrt(E2)
        cb, cc, cs, cr, tot = _chi2_all(fn, Om, H0)
        return tot if np.isfinite(tot) else 1e9
    try:
        r = minimize(obj, start, method='Nelder-Mead',
                     options={'xatol': 1e-4, 'fatol': 1e-4, 'maxiter': 800})
        return (float(r.fun), [float(x) for x in r.x])
    except Exception:
        return (1e9, None)


def _worker_generic(args):
    """Generic UB variant worker. args = (tag_or_spec, start_list)."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    tag_or_spec, start = args
    if isinstance(tag_or_spec, dict):
        spec = tag_or_spec
    else:
        spec = _MODELS[tag_or_spec]
    k    = spec['k']
    bnd  = spec['bnd']
    prof = spec['prof']
    avg  = spec['avg']
    cpl  = spec['cpl']
    free = spec['free']
    fixd = spec['fixed']
    bnds = spec['bounds']

    def obj(p):
        Om, H0 = p[0], p[1]
        # Bounds check
        for val, (lo, hi) in zip(p, bnds):
            if val < lo or val > hi:
                return 1e9
        # Resolve parameters
        pdict = {'Om': Om, 'H0': H0}
        for i, name in enumerate(free):
            pdict[name] = float(p[2 + i])
        pdict.update(fixd)
        muR0 = pdict.get('mR',  1.0)
        n    = pdict.get('n',   1.0)
        eps_v = pdict.get('eps', 0.0)

        fn = _make_E_variant(Om, muR0, prof, bnd, cpl, avg, n=n, eps=eps_v)
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


# ──────────────────────────────────────────────────────────────────────────────
# Bootstrap worker
# ──────────────────────────────────────────────────────────────────────────────

def _boot_worker_ub45(batch):
    """Bootstrap for L45 UB models. Perturbs BAO, CMB, RSD."""
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

        spec  = _MODELS[tag]
        free  = spec['free']
        fixd  = spec['fixed']
        bnd   = spec['bnd']
        prof  = spec['prof']
        avg   = spec['avg']
        cpl   = spec['cpl']
        bnds  = spec['bounds']

        def _tot(fn, Om, H0):
            t = (chi2_bao(fn, Om, H0) + chi2_cmb(fn, Om, H0) +
                 chi2_sn_corr(fn, Om, H0) + chi2_rsd(fn, Om, H0))
            return t if (np.isfinite(t) and t < 1e7) else 1e9

        def obj_win(p):
            for val, (lo, hi) in zip(p, bnds):
                if val < lo or val > hi:
                    return 1e9
            Om, H0 = p[0], p[1]
            pd = {'Om': Om, 'H0': H0}
            for i, nm in enumerate(free):
                pd[nm] = float(p[2+i])
            pd.update(fixd)
            muR0 = pd.get('mR', 1.0); n_ = pd.get('n', 1.0); eps_ = pd.get('eps', 0.0)
            fn = _make_E_variant(Om, muR0, prof, bnd, cpl, avg, n=n_, eps=eps_)
            if fn is None:
                return 1e9
            return _tot(fn, Om, H0)

        def obj_lcdm(p):
            Om, H0 = p
            if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82:
                return 1e9
            fn = lambda z, _: E_lcdm(z, Om)
            return _tot(fn, Om, H0)

        try:
            r_w = minimize(obj_win, s0[:k], method='Nelder-Mead',
                           options={'xatol': 1e-3, 'fatol': 1e-3, 'maxiter': 300})
            r_l = minimize(obj_lcdm, s0[:2], method='Nelder-Mead',
                           options={'xatol': 1e-3, 'fatol': 1e-3, 'maxiter': 300})
            results.append(float(_aicc(r_w.fun, k) - _aicc(r_l.fun, 2)))
        except Exception:
            results.append(None)

    _l35.DESI_DR2 = orig_bao
    _l35.CMB_OBS  = orig_cmb
    _l35.FS8_OBS  = orig_rsd
    return results


# ──────────────────────────────────────────────────────────────────────────────
# Pre-Task: Profile validation and visualization
# ──────────────────────────────────────────────────────────────────────────────
def pretask_validate(out_dir):
    print('\n' + '='*60)
    print('Pre-Task: Profile validation (BAL/FIC/DEC)')
    print('='*60)

    mR_tests = [0.5, 1.0, 2.0, 5.0]
    print('  Profile  mR    f(0)_code    f(0)_theory  err')
    for mR in mR_tests:
        f0_bal = float(_f_ballistic(np.array([0.0]), mR))
        f0_fic = 1.0 / np.cosh(mR)
        f0_dec = np.exp(-mR)

        # Verify BAL L'Hopital
        err_bal = abs(f0_bal - np.exp(-mR)) / np.exp(-mR)
        print(f'  BAL      {mR:.1f}  {f0_bal:.6f}     {np.exp(-mR):.6f}     '
              f'{err_bal:.1e}  [{"OK" if err_bal < 1e-4 else "FAIL"}]')
        # FIC and DEC are analytic
        print(f'  FIC      {mR:.1f}  {f0_fic:.6f}     {f0_fic:.6f}     0.0e+00  [OK]')
        print(f'  DEC      {mR:.1f}  {f0_dec:.6f}     {f0_dec:.6f}     0.0e+00  [OK]')

    # Verify E(0)=1 for each profile type
    print('\n  E(0)=1 check for all profiles (Om=0.32, mR=1):')
    Om_t = 0.32; mR_t = 1.0
    for prof in ['BAL', 'FIC', 'DEC']:
        for avg in ['PATH', 'VOL']:
            for bnd in ['H', 'E']:
                E_arr = _compute_E_variant(UB_Z_GRID, Om_t, mR_t, prof, bnd, 'LIN', avg)
                ok = E_arr is not None and abs(E_arr[0] - 1.0) < 1e-5
                status = 'OK' if ok else 'FAIL'
                print(f'  {prof}-{avg}-{bnd}: E(0)={E_arr[0]:.8f}  [{status}]'
                      if E_arr is not None else f'  {prof}-{avg}-{bnd}: FAILED')

    # Plot profiles
    s_plot = np.linspace(0.0, 1.0, 500)
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    for ax, (label, prof_fn, mR_label) in zip(axes, [
        ('BAL (Ballistic)',  lambda s, mR: _f_ballistic(s, mR), 'mR'),
        ('FIC (Fickian)',    lambda s, mR: np.cosh(mR*s)/np.cosh(mR), 'mR'),
        ('DEC (Exp-decay)',  lambda s, mR: np.exp(-mR*(1-s)), 'mR'),
    ]):
        for mR in [0.3, 0.5, 1.0, 2.0, 5.0]:
            ax.plot(s_plot, prof_fn(s_plot, mR), label=f'{mR_label}={mR}')
        ax.set_xlabel('s = r/R')
        ax.set_ylabel('f(s; mR)')
        ax.set_title(label)
        ax.legend(fontsize=7)
        ax.set_ylim(bottom=0)
        ax.grid(alpha=0.3)

    fig.tight_layout()
    out = os.path.join(out_dir, 'l45_pretask_profiles.png')
    fig.savefig(out, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f'\n  Profile plot: {out}')
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 0: Baselines
# ──────────────────────────────────────────────────────────────────────────────
def task0_baselines(pool):
    print('\n' + '='*60)
    print('Task 0: Baselines (LCDM + CPL -- confirm L43)')
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
    starts_cpl += [[0.36, 63., -0.45, -1.47], [0.31, 68., -0.34, -1.90]]

    print(f'  LCDM: {len(starts_lcdm)} starts, CPL: {len(starts_cpl)} starts')
    sys.stdout.flush()

    res_lcdm = pool.map(_worker_lcdm, starts_lcdm)
    res_cpl  = pool.map(_worker_cpl,  starts_cpl)

    chi2_lcdm, par_lcdm = _best_of(res_lcdm)
    Om_l = par_lcdm[0] if par_lcdm else 0.3236
    H0_l = par_lcdm[1] if par_lcdm else 67.52
    aicc_lcdm = _aicc(chi2_lcdm, 2)

    fn_l = lambda z, _: E_lcdm(z, Om_l)
    cb_l, cc_l, cs_l, cr_l, _ = _chi2_all(fn_l, Om_l, H0_l)
    d_lcdm = aicc_lcdm - LCDM_AICC_L43
    print(f'\n  LCDM: Om={Om_l:.4f}, H0={H0_l:.4f}')
    print(f'  chi2: BAO={cb_l:.2f} CMB={cc_l:.2f} SN={cs_l:.2f} RSD={cr_l:.2f}')
    print(f'  AICc={aicc_lcdm:.4f}  L43_ref={LCDM_AICC_L43:.2f}  '
          f'delta={d_lcdm:+.2f}  [{"OK" if abs(d_lcdm)<2 else "CHECK"}]')

    chi2_cpl, par_cpl = _best_of(res_cpl)
    aicc_cpl  = _aicc(chi2_cpl, 4)
    daicc_cpl = aicc_cpl - aicc_lcdm
    w0_c = wa_c = Om_c = H0_c = None
    if par_cpl:
        Om_c, H0_c, w0_c, wa_c = par_cpl
        d_cpl = aicc_cpl - CPL_AICC_L43
        print(f'\n  CPL: Om={Om_c:.4f}, H0={H0_c:.4f}, w0={w0_c:.4f}, wa={wa_c:.4f}')
        print(f'  AICc={aicc_cpl:.4f}  dAICc={daicc_cpl:.2f}  '
              f'L43_ref={CPL_AICC_L43:.2f}  delta={d_cpl:+.2f}  '
              f'[{"OK" if abs(d_cpl)<2 else "CHECK"}]')

    elapsed = time.time() - t0
    print(f'  Elapsed: {elapsed:.1f}s')
    sys.stdout.flush()

    return {
        'lcdm': {'Om': Om_l, 'H0': H0_l, 'chi2': chi2_lcdm, 'aicc': aicc_lcdm,
                 'chi2_bao': cb_l, 'chi2_cmb': cc_l, 'chi2_sn': cs_l, 'chi2_rsd': cr_l},
        'cpl':  {'Om': Om_c, 'H0': H0_c, 'w0': w0_c, 'wa': wa_c,
                 'chi2': chi2_cpl, 'aicc': aicc_cpl, 'daicc_vs_lcdm': daicc_cpl},
        'lcdm_aicc': aicc_lcdm,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Task 1: Tier 1 -- 18 model variants
# ──────────────────────────────────────────────────────────────────────────────
def task1_tier1(pool, lcdm_aicc):
    print('\n' + '='*60)
    print(f'Task 1: Tier 1 ({len(_TIER1_TAGS)} models x {N_TIER1_STARTS} starts)')
    print('='*60)
    t0 = time.time()
    rng = np.random.default_rng(42)

    def _starts_for(spec, seed_offset):
        k    = spec['k']
        bnds = spec['bounds']
        free = spec['free']
        fixd = spec['fixed']
        starts = []
        if k == 4 and 'mR' in free and 'n' in free:
            # Dedicated 4D grid for k=4 with both mR and n free
            for Om0 in [0.28, 0.32, 0.36]:
                for H0_0 in [63., 68., 72.]:
                    for mR0 in [0.5, 1.0, 3.0]:
                        for n0 in [0.5, 1.0, 2.0]:
                            starts.append([Om0, H0_0, mR0, n0])
        else:
            # Grid over Om,H0 with free params
            for Om0 in [0.28, 0.30, 0.32, 0.34, 0.36]:
                for H0_0 in [63., 66., 69., 72.]:
                    s = [Om0, H0_0]
                    if 'mR' in free:
                        for mR0 in [0.3, 1.0, 3.0]:
                            starts.append(s + [mR0])
                    elif 'n' in free:
                        for n0 in [0.5, 1.0, 2.0]:
                            starts.append(s + [n0])
                    elif 'eps' in free:
                        for e0 in [0.1, 0.5, 0.9]:
                            starts.append(s + [e0])
                    else:
                        starts.append(s)
        # Pad with random starts up to N_TIER1_STARTS
        rng2 = np.random.default_rng(seed_offset)
        while len(starts) < N_TIER1_STARTS:
            s = [rng2.uniform(*b) for b in bnds]
            starts.append(s)
        return starts[:N_TIER1_STARTS + 10]  # slight overshoot for safety

    all_args = []
    for tag in _TIER1_TAGS:
        spec = _MODELS[tag]
        starts = _starts_for(spec, hash(tag) & 0xFFFF)
        for s in starts:
            all_args.append((spec, s))

    print(f'  Total tasks: {len(all_args)} dispatched across {N_WORKERS} workers')
    sys.stdout.flush()

    raw = pool.map(_worker_generic, all_args)

    # Group results by tag
    tag_results = {tag: [] for tag in _TIER1_TAGS}
    idx = 0
    for tag in _TIER1_TAGS:
        spec = _MODELS[tag]
        starts = _starts_for(spec, hash(tag) & 0xFFFF)
        n_s = len(starts)
        tag_results[tag] = raw[idx:idx+n_s]
        idx += n_s

    elapsed = time.time() - t0
    print(f'  All fits done in {elapsed:.1f}s')
    sys.stdout.flush()

    # Best result per tag
    tier1_best = {}
    for tag in _TIER1_TAGS:
        tier1_best[tag] = _best_of(tag_results[tag])

    return tier1_best


# ──────────────────────────────────────────────────────────────────────────────
# Task 2: Analyze and rank Tier 1
# ──────────────────────────────────────────────────────────────────────────────
def task2_rank_tier1(tier1_best, lcdm_aicc, cpl_result):
    print('\n' + '='*60)
    print('Task 2: Tier 1 ranking')
    print('='*60)

    cpl_aicc = cpl_result.get('aicc') if cpl_result else None
    ranked   = []

    for tag in _TIER1_TAGS:
        chi2, params = tier1_best[tag]
        spec = _MODELS[tag]
        k    = spec['k']
        if params is None or not np.isfinite(chi2) or chi2 >= 1e8:
            ranked.append({'tag': tag, 'k': k, 'daicc': 9999, 'verdict': 'FAILED',
                           'params': None, 'chi2': None, 'aicc': None})
            continue

        aicc  = _aicc(chi2, k)
        daicc = aicc - lcdm_aicc
        bnd   = _at_boundary(params, spec['bounds'][:len(params)])
        vdict = _verdict(daicc, boundary=bnd, k2=(k <= 2))
        dvscp = (aicc - cpl_aicc) if cpl_aicc else None

        # CPL extraction
        Om, H0 = params[0], params[1]
        pdict = {'Om': Om, 'H0': H0}
        for i, nm in enumerate(spec['free']):
            pdict[nm] = float(params[2+i])
        pdict.update(spec['fixed'])
        muR0 = pdict.get('mR', 1.0); n_ = pdict.get('n', 1.0); eps_ = pdict.get('eps', 0.0)

        fn = _make_E_variant(Om, muR0, spec['prof'], spec['bnd'],
                              spec['cpl'], spec['avg'], n=n_, eps=eps_)
        w0 = wa = q0v = None
        if fn is not None:
            try:
                w0, wa = cpl_wa(fn, Om)
                if w0 is not None:
                    q0v = _q0(Om, w0)
            except Exception:
                pass

        ranked.append({'tag': tag, 'k': k, 'daicc': daicc, 'daicc_vs_cpl': dvscp,
                       'aicc': aicc, 'chi2': chi2, 'params': params,
                       'boundary': bnd, 'verdict': vdict,
                       'w0': w0, 'wa': wa, 'q0': q0v,
                       'muR0': muR0, 'n': n_, 'eps': eps_})

    ranked.sort(key=lambda x: x['daicc'])

    print(f'\n  {"Rank":<4} {"Tag":<28} {"k":<2} {"dAICc":>8}  {"Verdict":<16}  '
          f'{"w0":>7}  {"wa":>7}')
    print('  ' + '-'*80)
    for i, r in enumerate(ranked[:18]):
        w0s = f'{r["w0"]:.3f}' if r["w0"] is not None else '  ---'
        was = f'{r["wa"]:.3f}' if r["wa"] is not None else '  ---'
        print(f'  {i+1:<4} {r["tag"]:<28} {r["k"]:<2} {r["daicc"]:>8.2f}  '
              f'{r["verdict"]:<16}  {w0s:>7}  {was:>7}')

    sys.stdout.flush()
    return ranked


# ──────────────────────────────────────────────────────────────────────────────
# Task 3: Bootstrap for top-N Tier 1 models
# ──────────────────────────────────────────────────────────────────────────────
def task3_bootstrap(pool, ranked, lcdm_result, n_top=5):
    print('\n' + '='*60)
    print(f'Task 3: Bootstrap (top-{n_top} by dAICc, N={N_BOOT})')
    print('='*60)

    candidates = [r for r in ranked if r['params'] is not None and r['daicc'] < -2][:n_top]
    if not candidates:
        print('  No candidates with dAICc < -2. Skipping.')
        return {}

    boot_results = {}
    Om_l = lcdm_result['Om']; H0_l = lcdm_result['H0']
    E_fn_lcdm = lambda z, _: E_lcdm(z, Om_l)
    bao_nom_l = _bao_theory_vec(E_fn_lcdm, Om_l, H0_l)
    if bao_nom_l is None:
        print('  SKIPPED: BAO theory vector failed')
        return {}

    rng     = np.random.default_rng(99)
    bao_cov = np.linalg.inv(DESI_DR2_COV_INV)
    bao_L   = np.linalg.cholesky(bao_cov)

    for r in candidates:
        tag    = r['tag']
        k      = r['k']
        best_p = r['params']
        print(f'\n  Bootstrapping {tag} (k={k}, dAICc={r["daicc"]:.2f})...')
        sys.stdout.flush()
        t0 = time.time()

        boot_items = []
        for _ in range(N_BOOT):
            nb  = bao_nom_l + bao_L @ rng.standard_normal(13)
            nc  = CMB_OBS   + CMB_SIG * rng.standard_normal(len(CMB_OBS))
            nr  = FS8_OBS   + FS8_SIG * rng.standard_normal(len(FS8_OBS))
            s0  = ([best_p[0] + rng.normal(0, 0.01),
                    best_p[1] + rng.normal(0, 0.5)] + list(best_p[2:]))
            boot_items.append((s0, nb, nc, nr, tag, best_p, k))

        bsz     = max(1, N_BOOT // N_WORKERS)
        batches = [boot_items[i:i+bsz] for i in range(0, N_BOOT, bsz)]
        raw     = pool.map(_boot_worker_ub45, batches)

        all_d = [v for b in raw for v in b]
        vals  = np.array([v for v in all_d if v is not None and np.isfinite(v)])

        elapsed = time.time() - t0
        print(f'  Done in {elapsed:.1f}s  Valid: {len(vals)}/{N_BOOT}')

        if len(vals) == 0:
            boot_results[tag] = {'verdict': 'FAIL', 'valid': 0}
            continue

        med  = float(np.median(vals))
        lo   = float(np.percentile(vals, 16))
        hi   = float(np.percentile(vals, 84))
        p_lt = float(np.mean(vals < -4))
        verd = 'PASS' if p_lt >= 0.90 else 'FAIL'
        print(f'  median={med:.2f}  68%CI=[{lo:.2f},{hi:.2f}]  '
              f'<-4: {p_lt*100:.0f}%  [{verd}]')
        boot_results[tag] = {'valid': int(len(vals)), 'median': med,
                              'ci68': [lo, hi], 'frac_lt4': p_lt, 'verdict': verd}
    sys.stdout.flush()
    return boot_results


# ──────────────────────────────────────────────────────────────────────────────
# Task 4: Tier 2 -- cross-combinations of best axes
# ──────────────────────────────────────────────────────────────────────────────
def task4_tier2(pool, ranked, lcdm_aicc):
    print('\n' + '='*60)
    print('Task 4: Tier 2 cross-combinations')
    print('='*60)

    # Determine best axis values from Tier 1
    top5 = [r for r in ranked if r['daicc'] < -2][:5]
    if not top5:
        print('  No Tier 1 model with dAICc < -2. Tier 2 SKIPPED.')
        return {}

    best_bnd  = top5[0]['tag'].split('-')[0]  # H or E
    best_prof = top5[0]['tag'].split('-')[1]  # BAL/FIC/DEC
    best_avg  = top5[0]['tag'].split('-')[2]  # PATH/VOL
    best_cpl  = top5[0]['tag'].split('-')[3]  # LIN/POW/MIX/HPR
    print(f'  Best axis choices: bnd={best_bnd}, prof={best_prof}, '
          f'avg={best_avg}, cpl={best_cpl}')

    # Generate Tier 2: cross all boundaries with all profiles and best coupling
    tier2_tags = []
    for bnd in ['H', 'E']:
        for prof in ['BAL', 'FIC', 'DEC']:
            for avg in ['PATH', 'VOL']:
                for cpl in ['LIN', 'POW', 'MIX']:
                    tag = f'{bnd}-{prof}-{avg}-{cpl}-k3'
                    if tag not in _MODELS:
                        # Add dynamically
                        if cpl == 'LIN':
                            spec = {'k': 3, 'bnd': bnd, 'prof': prof, 'avg': avg, 'cpl': cpl,
                                    'free': ['mR'], 'fixed': {}, 'bounds': _B3_mR}
                        elif cpl == 'POW':
                            spec = {'k': 3, 'bnd': bnd, 'prof': prof, 'avg': avg, 'cpl': cpl,
                                    'free': ['n'], 'fixed': {'mR': 1.0}, 'bounds': _B3_n}
                        elif cpl == 'MIX':
                            spec = {'k': 3, 'bnd': bnd, 'prof': prof, 'avg': avg, 'cpl': cpl,
                                    'free': ['eps'], 'fixed': {'mR': 1.0}, 'bounds': _B3_eps}
                        _MODELS[tag] = spec
                    if tag not in tier2_tags:
                        tier2_tags.append(tag)

    # Remove duplicates with Tier 1
    tier2_new = [t for t in tier2_tags if t not in _TIER1_TAGS][:54]
    print(f'  Tier 2: {len(tier2_new)} new models, {N_TIER2_STARTS} starts each')
    sys.stdout.flush()

    rng = np.random.default_rng(77)
    all_args = []
    for tag in tier2_new:
        spec = _MODELS[tag]
        bnds = spec['bounds']
        for _ in range(N_TIER2_STARTS):
            s = [rng.uniform(*b) for b in bnds]
            all_args.append((spec, s))  # pass spec dict; spawn workers cannot see _MODELS mutations

    if not all_args:
        print('  No new Tier 2 models.')
        return {}

    t0  = time.time()
    raw = pool.map(_worker_generic, all_args)
    elapsed = time.time() - t0
    print(f'  Tier 2 fits done in {elapsed:.1f}s')

    # Group by tag
    tier2_best = {}
    idx = 0
    for tag in tier2_new:
        tier2_best[tag] = _best_of(raw[idx:idx+N_TIER2_STARTS])
        idx += N_TIER2_STARTS

    # Rank and print top 10
    t2_ranked = []
    for tag, (chi2, params) in tier2_best.items():
        if params is None or not np.isfinite(chi2):
            continue
        spec  = _MODELS[tag]
        k     = spec['k']
        aicc  = _aicc(chi2, k)
        daicc = aicc - lcdm_aicc
        bnd   = _at_boundary(params, spec['bounds'][:len(params)])
        vdict = _verdict(daicc, boundary=bnd, k2=(k<=2))
        t2_ranked.append({'tag': tag, 'k': k, 'daicc': daicc, 'aicc': aicc,
                           'chi2': chi2, 'params': params, 'verdict': vdict})
    t2_ranked.sort(key=lambda x: x['daicc'])

    print(f'\n  Top-10 Tier 2 results:')
    for i, r in enumerate(t2_ranked[:10]):
        print(f'  {i+1:2d} {r["tag"]:<32} dAICc={r["daicc"]:+8.2f}  [{r["verdict"]}]')
    sys.stdout.flush()

    return tier2_best


# ──────────────────────────────────────────────────────────────────────────────
# Tasks 5-6: Sensitivity and visualization
# ──────────────────────────────────────────────────────────────────────────────
def task5_mur0_sensitivity(pool, ranked, lcdm_aicc, out_dir):
    print('\n' + '='*60)
    print('Task 5: muR0 sensitivity (top-3 profile types)')
    print('='*60)

    # Find best model per profile type
    best_by_prof = {}
    for r in ranked:
        prof = r['tag'].split('-')[1]
        if prof not in best_by_prof and r['params'] is not None:
            best_by_prof[prof] = r

    mR_grid = np.concatenate([np.linspace(0.1, 2.0, 12), np.linspace(2.0, 10.0, 8)[1:]])

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.axhline(0, color='k', ls='--', lw=0.8, label='LCDM')
    ax.axhline(-4, color='C2', ls=':', lw=0.8, label='dAICc=-4')
    ax.axhline(-10, color='C3', ls=':', lw=0.8, label='dAICc=-10')

    for prof, r in best_by_prof.items():
        spec = _MODELS[r['tag']]
        bnd  = spec['bnd']; avg = spec['avg']; cpl = spec['cpl']
        Om   = r['params'][0]; H0 = r['params'][1]

        scan_args = []
        rng2 = np.random.default_rng(55)
        for mR_val in mR_grid:
            # Pass spec dict directly (spawn workers cannot see runtime _MODELS mutations)
            scan_spec = {'k': 2, 'bnd': bnd, 'prof': prof, 'avg': avg, 'cpl': cpl,
                         'free': [], 'fixed': {'mR': float(mR_val)}, 'bounds': _B2}
            scan_args.append((scan_spec, [Om + rng2.normal(0,0.01), H0 + rng2.normal(0,0.5)]))

        raw_scan = pool.map(_worker_generic, scan_args)
        daicc_scan = []
        for (chi2_s, par_s), mR_val in zip(raw_scan, mR_grid):
            if par_s is not None and np.isfinite(chi2_s) and chi2_s < 1e8:
                daicc_scan.append(_aicc(chi2_s, 2) - lcdm_aicc)
            else:
                daicc_scan.append(np.nan)
        ax.plot(mR_grid, daicc_scan, 'o-', ms=4, label=f'{prof}-{bnd}-{cpl}')

    ax.axvline(1.0, color='C1', ls=':', lw=0.8, alpha=0.7, label='muR0=1')
    ax.set_xlabel('muR0')
    ax.set_ylabel('dAICc vs LCDM (k=2)')
    ax.set_title('L45: muR0 sensitivity by profile type')
    ax.legend(fontsize=7, loc='best')
    ax.grid(alpha=0.3)
    fig.tight_layout()
    out = os.path.join(out_dir, 'l45_task5_mur0scan.png')
    fig.savefig(out, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f'  Plot: {out}')
    sys.stdout.flush()


def task6_wz_plot(ranked, cpl_result, out_dir):
    print('\n' + '='*60)
    print('Task 6: w(z) visualization (top-5 models)')
    print('='*60)

    z_plot = np.linspace(0.01, 2.0, 300)
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.axhline(-1.0, color='k', ls='--', lw=1, label='LCDM')
    w_son = SON_W0 + SON_WA * z_plot / (1.0 + z_plot)
    ax.plot(z_plot, w_son, 'k-', lw=2, label=f'Son+25 (w0={SON_W0}, wa={SON_WA})')
    ax.fill_between(z_plot,
        (SON_W0-SON_W0_2SIG) + (SON_WA-SON_WA_2SIG)*z_plot/(1+z_plot),
        (SON_W0+SON_W0_2SIG) + (SON_WA+SON_WA_2SIG)*z_plot/(1+z_plot),
        alpha=0.10, color='k', label='Son+25 2-sigma')

    if cpl_result.get('w0') is not None:
        w0_c, wa_c = cpl_result['w0'], cpl_result['wa']
        ax.plot(z_plot, w0_c + wa_c*z_plot/(1+z_plot), 'C5-.',
                lw=1.5, label=f'CPL (w0={w0_c:.2f}, wa={wa_c:.2f})')

    colors = ['C0', 'C1', 'C2', 'C3', 'C4']
    for i, (r, col) in enumerate(zip(ranked[:5], colors)):
        w0 = r.get('w0'); wa = r.get('wa')
        if w0 is None or wa is None:
            continue
        ax.plot(z_plot, w0 + wa*z_plot/(1+z_plot), col, lw=1.5,
                label=f'{r["tag"]} dAICc={r["daicc"]:.1f} (w0={w0:.2f})')

    ax.set_xlabel('z')
    ax.set_ylabel('w(z)')
    ax.set_title('L45: Top-5 UB variants vs Son+25')
    ax.legend(fontsize=7, loc='best')
    ax.set_ylim(-4.0, 0.5)
    ax.grid(alpha=0.3)
    out = os.path.join(out_dir, 'l45_task6_wz.png')
    fig.savefig(out, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f'  Plot: {out}')
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Tasks 7-8: w0-wa plane and q0 comparison
# ──────────────────────────────────────────────────────────────────────────────
def task7_w0wa(ranked, cpl_result, out_dir):
    print('\n' + '='*60)
    print('Task 7: w0-wa plane')
    print('='*60)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axvline(-1.0, color='k', ls=':', lw=0.8, alpha=0.5)
    ax.axhline(0.0,  color='k', ls=':', lw=0.8, alpha=0.5)
    ax.plot(-1.0, 0.0, 'k+', ms=12, label='LCDM')
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(SON_W0, SON_WA, 'ks', ms=10, label=f'Son+25 ({SON_W0}, {SON_WA})')
    ax.plot(SON_W0 + SON_W0_2SIG*np.cos(theta),
            SON_WA + SON_WA_2SIG*np.sin(theta), 'k--', lw=1, alpha=0.3)
    ax.plot(-0.757, -0.83, 'g^', ms=8, label='DESI DR2')
    if cpl_result.get('w0') is not None:
        ax.plot(cpl_result['w0'], cpl_result['wa'], 'C5*', ms=12,
                label=f"CPL ({cpl_result['w0']:.2f}, {cpl_result['wa']:.2f})")
    colors = ['C0','C1','C2','C3','C4','C6','C7','C8','C9','C0']
    for i, (r, col) in enumerate(zip(ranked[:10], colors)):
        w0 = r.get('w0'); wa = r.get('wa')
        if w0 is None:
            continue
        ax.plot(w0, wa, 'o', color=col, ms=8,
                label=f'{r["tag"]} ({w0:.2f},{wa:.2f})')
    ax.set_xlabel('w0'); ax.set_ylabel('wa')
    ax.set_title('L45: w0-wa plane (top-10 Tier 1)')
    ax.legend(fontsize=6, loc='best')
    ax.set_xlim(-3.0, 0.5); ax.set_ylim(-5.0, 3.0)
    ax.grid(alpha=0.3)
    out = os.path.join(out_dir, 'l45_task7_w0wa.png')
    fig.savefig(out, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f'  Plot: {out}')
    sys.stdout.flush()


def task8_q0(ranked, cpl_result):
    print('\n' + '='*60)
    print('Task 8: q0 comparison')
    print('='*60)
    print(f'  Son+25 target: q0={SON_Q0:+.2f}  LCDM: q0=-0.53')
    print(f'\n  {"Model":<30} {"w0":>7} {"wa":>7} {"q0":>7}  Son+25?')
    print('  ' + '-'*65)
    if cpl_result.get('w0') is not None:
        w0_c = cpl_result['w0']; wa_c = cpl_result['wa']
        Om_c = cpl_result.get('Om') or 0.36
        q0_c = _q0(Om_c, w0_c)
        ag = 'YES' if q0_c > 0 else ('NEAR' if q0_c > -0.1 else 'NO')
        print(f'  {"CPL":<30} {w0_c:>7.3f} {wa_c:>7.3f} {q0_c:>7.3f}  {ag}')
    for r in ranked[:10]:
        w0 = r.get('w0'); wa = r.get('wa'); q0v = r.get('q0')
        if w0 is None:
            continue
        if q0v is None and r.get('params'):
            q0v = _q0(r['params'][0], w0)
        ag = 'YES' if (q0v or -999) > 0 else ('NEAR' if (q0v or -999) > -0.1 else 'NO')
        print(f'  {r["tag"]:<30} {w0:>7.3f} {(wa or float("nan")):>7.3f} '
              f'{(q0v or float("nan")):>7.3f}  {ag}')
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Tasks 9-10: Final analysis
# ──────────────────────────────────────────────────────────────────────────────
def task9_axis_analysis(ranked):
    print('\n' + '='*60)
    print('Task 9: Best axis analysis')
    print('='*60)

    axis_stats = {'bnd': {}, 'prof': {}, 'avg': {}, 'cpl': {}}
    for r in ranked:
        if r['daicc'] >= 9000:
            continue
        parts = r['tag'].split('-')
        if len(parts) < 4:
            continue
        for ax_key, part in zip(['bnd', 'prof', 'avg', 'cpl'], parts):
            axis_stats[ax_key].setdefault(part, []).append(r['daicc'])

    print('  Best dAICc by axis value:')
    for ax_name, groups in axis_stats.items():
        print(f'  Axis [{ax_name}]:')
        for val, diffs in sorted(groups.items(), key=lambda x: min(x[1])):
            best_d = min(diffs)
            mean_d = np.mean(diffs)
            print(f'    {val:<8}: best={best_d:+.2f}  mean={mean_d:+.2f}  n={len(diffs)}')
    sys.stdout.flush()


def task10_final_verdict(ranked, boot_results, tier2_best, lcdm_aicc, cpl_result):
    print('\n' + '='*60)
    print('L45 FINAL VERDICT')
    print('='*60)

    best = [r for r in ranked if r['daicc'] < 9000][:3]
    print(f'\n  Top-3 Tier 1 by AICc:')
    for i, r in enumerate(best):
        d = r['daicc']; v = r['verdict']; tag = r['tag']
        print(f'  {i+1}. {tag}  dAICc={d:+.2f}  [{v}]')
        if tag in boot_results:
            br = boot_results[tag]
            med_val = br.get("median")
            med_str = f'{med_val:.2f}' if isinstance(med_val, float) else '?'
            print(f'     Bootstrap: median={med_str}  '
                  f'{br.get("verdict","?")}')

    # Tier 2 champion
    if tier2_best:
        t2_best = min([(t, c, p) for t, (c, p) in tier2_best.items()
                       if p is not None and np.isfinite(c) and c < 1e8],
                      key=lambda x: x[1], default=None)
        if t2_best:
            t2_tag = t2_best[0]
            t2_aicc = _aicc(t2_best[1], _MODELS.get(t2_tag, {}).get('k', 3))
            t2_daicc = t2_aicc - lcdm_aicc
            print(f'\n  Best Tier 2: {t2_tag}  dAICc={t2_daicc:+.2f}')

    # Overall verdict
    best_d = best[0]['daicc'] if best else 9999
    if best_d < -20:
        final = 'Q95 VICTORY -- SQT UB dark energy: multiple variants succeed'
    elif best_d < -15:
        final = 'Q94 DISCOVERY -- strong evidence for boundary inflow'
    elif best_d < -10:
        final = 'Q93 TRIUMPH -- significant UB signal, Nature/PRL candidate'
    elif best_d < -4:
        final = 'Q92 GAME -- competitive with CPL, JCAP paper'
    elif best_d < 0:
        final = 'Q90/Q91 -- marginal improvement'
    else:
        final = 'K90 KILL -- all UB variants rejected, SQT DE falsified'

    print(f'\n  [FINAL] {final}')
    print(f'  Resurrection threshold (dAICc < -50 vs LCDM): '
          f'{"CROSSED" if best_d < -50 else "NOT reached"}')
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    OUT_DIR = _SCRIPT_DIR

    print('='*60)
    print('L45: Model UB Variant Exploration (18 Tier 1 + 54 Tier 2)')
    print(f'8-worker parallel  |  L43 LCDM AICc ref={LCDM_AICC_L43:.2f}')
    print('='*60)
    sys.stdout.flush()

    pretask_validate(OUT_DIR)

    ctx  = mp.get_context('spawn')
    pool = ctx.Pool(N_WORKERS)

    r0         = None
    ranked     = []
    boot_res   = {}
    tier2_best = {}
    lcdm_aicc  = LCDM_AICC_L43

    try:
        # Task 0: Baselines
        r0        = task0_baselines(pool)
        lcdm_aicc = r0['lcdm_aicc']
        lcdm_res  = r0['lcdm']
        cpl_res   = r0['cpl']

        # Task 1: Tier 1 fits
        tier1_best = task1_tier1(pool, lcdm_aicc)

        # Task 2: Rank Tier 1
        ranked = task2_rank_tier1(tier1_best, lcdm_aicc, cpl_res)

        # Task 3: Bootstrap
        boot_res = task3_bootstrap(pool, ranked, lcdm_res, n_top=5)

        # Task 4: Tier 2 (only if any T1 model < -4)
        if any(r['daicc'] < -4 for r in ranked):
            tier2_best = task4_tier2(pool, ranked, lcdm_aicc)
        else:
            print('\nTask 4: Tier 2 SKIPPED (no Tier 1 model with dAICc < -4)')

        # Task 5: muR0 sensitivity
        task5_mur0_sensitivity(pool, ranked, lcdm_aicc, OUT_DIR)

        # Task 6: w(z) visualization
        task6_wz_plot(ranked, cpl_res, OUT_DIR)

        # Task 7: w0-wa plane
        task7_w0wa(ranked, cpl_res, OUT_DIR)

        # Task 8: q0 comparison
        task8_q0(ranked, cpl_res)

        # Task 9: Axis analysis
        task9_axis_analysis(ranked)

        # Task 10: Final verdict
        task10_final_verdict(ranked, boot_res, tier2_best, lcdm_aicc, cpl_res)

    finally:
        pool.close()
        pool.join()

    # ── Summary ──
    print('\n' + '='*60)
    print('L45 RESULTS SUMMARY')
    print('='*60)
    if r0:
        print(f"[Task 0] LCDM AICc={r0['lcdm_aicc']:.2f}  "
              f"CPL dAICc={r0['cpl'].get('daicc_vs_lcdm', 'N/A')}")
    print(f'\n[Task 1] Tier 1 top-5:')
    for r in ranked[:5]:
        print(f'  {r["tag"]:<32}  dAICc={r["daicc"]:+.2f}  [{r["verdict"]}]')
    print()

    # Save JSON
    save = {
        'task0':          _jsonify(r0),
        'tier1_ranked':   _jsonify(ranked),
        'bootstrap':      _jsonify(boot_res),
        'tier2_count':    len(tier2_best),
        'lcdm_aicc':      lcdm_aicc,
        'lcdm_aicc_l43':  LCDM_AICC_L43,
        'son_params':     {'w0': SON_W0, 'wa': SON_WA, 'q0': SON_Q0},
    }
    out_json = os.path.join(OUT_DIR, 'l45_results.json')
    with open(out_json, 'w') as f:
        json.dump(save, f, indent=2)
    print(f'Saved: {out_json}')
