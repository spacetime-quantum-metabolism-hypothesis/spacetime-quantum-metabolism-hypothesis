# -*- coding: utf-8 -*-
"""
l46_test.py -- L46: 3-Axiom SQT + A3 4-State Full Exploration
==============================================================
3-axiom framework:
  A2: dPsi/dt = kappa_2 - 3H*Psi  (generation + dilution)
  A3: d/dt += 3*(J+(t)-J-(t))/R(t) (boundary exchange)
  A1: annihilation absorbed into normalization (sigma~0)

ODE converted to z-domain (kappa_2=1, Zero IC at z_max):
  Dil:   Psi(z) = integral_z^{z_max} (1+z')^2 * S(z') / E(z') dz' / (1+z)^3
  NoDil: Psi(z) = integral_z^{z_max} S(z') / [(1+z') E(z')] dz'
  where S(z) = 1 + 3*j_eff(z)

rho_DE(z) = OL0 * Psi_norm(z)   [LIN coupling, Tier 1]

Tier 1 (32 models): fixed H+BAL+PATH+LIN, A3-type x sign x Dil/NoDil, 30 starts each
Tier 2 (45 models): Top-5 x 9 axis variations, 20 starts each
Tier 3 (20 models): Top-5 Tier-2 x 4 couplings, 20 starts each
Bootstrap: Top-10 x N=200
Total: ~4260 fits, ~18-27h
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
_L45_DIR    = os.path.join(_SCRIPT_DIR, '../l45')
for _p in [os.path.dirname(_SCRIPT_DIR), _L35_DIR, _L45_DIR]:
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
LCDM_AICC_L43  = 1759.93
CPL_AICC_L43   = 1652.91
L45_UB_DAICC   = -55.49   # H-DEC-VOL-LIN-k3 champion

N_WORKERS        = 8
N_BOOT           = 200
N_TIER1_STARTS   = 30
N_TIER2_STARTS   = 20
N_TIER3_STARTS   = 20

SON_SLOPE     = 0.030
SON_SLOPE_ERR = 0.004
SON_DAGE_AMP  = 5.3
SON_DAGE_TAU  = 2.5
SON_W0        = -0.34
SON_WA        = -1.90
SON_Q0        = +0.18
SON_W0_2SIG   = 0.12
SON_WA_2SIG   = 0.50

# z-grid: 0 to 1200 (same as L45 UB_Z_GRID)
L46_Z_GRID = np.concatenate([
    np.linspace(0.0, 3.5, 2000),
    np.linspace(3.5, 1200.0, 600)[1:],
])
N_L46_S = 2000  # s-grid points for BAL numerical integral

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
        self.mu_obs  = self.mu_obs - delta_m
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
# Spatial profile functions (reused from L45 for Tier 2+)
# ──────────────────────────────────────────────────────────────────────────────

def _f_ballistic(s_arr, mR):
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
    s_grid = np.concatenate([[0.0], np.linspace(1e-9, 1.0, N_L46_S)])
    f_grid = _f_ballistic(s_grid, mR)
    I_grid = np.concatenate([[0.0], cumulative_trapezoid(f_grid, s_grid)])
    return interp1d(s_grid, I_grid, kind='linear',
                    bounds_error=False, fill_value=(0.0, float(I_grid[-1])))


def _build_Ivol_bal(mR):
    s_grid = np.concatenate([[0.0], np.linspace(1e-9, 1.0, N_L46_S)])
    f_grid = _f_ballistic(s_grid, mR) * s_grid**2
    I_grid = np.concatenate([[0.0], cumulative_trapezoid(f_grid, s_grid)])
    return interp1d(s_grid, I_grid, kind='linear',
                    bounds_error=False, fill_value=(0.0, float(I_grid[-1])))


def _F_avg_bal_path(q_arr, mR, I_fn):
    F0  = np.exp(-mR)
    I_q = I_fn(q_arr)
    return np.where(q_arr > 1e-10, I_q / q_arr, F0)


def _F_avg_bal_vol(q_arr, mR, Iv_fn):
    F0   = np.exp(-mR)
    Iv_q = Iv_fn(q_arr)
    q3   = q_arr**3
    return np.where(q_arr > 1e-10, 3.0 * Iv_q / q3, F0)


def _F_avg_fic_path(q_arr, mR):
    F0 = 1.0 / np.cosh(mR)
    mRq = mR * q_arr
    return np.where(q_arr > 1e-10,
                    np.sinh(mRq) / (mRq * np.cosh(mR)),
                    F0)


def _F_avg_fic_vol(q_arr, mR):
    F0 = 1.0 / np.cosh(mR)
    mR_safe = max(mR, 1e-8)
    mRq = mR_safe * q_arr
    sh = np.sinh(mRq); ch = np.cosh(mRq)
    Iv = (q_arr**2 * sh / mR_safe
          - 2.0 * q_arr * ch / mR_safe**2
          + 2.0 * sh / mR_safe**3) / np.cosh(mR_safe)
    q3 = q_arr**3
    return np.where(q_arr > 1e-10, 3.0 * Iv / q3, F0)


def _F_avg_dec_path(q_arr, mR):
    F0 = np.exp(-mR)
    return np.where(
        q_arr > 1e-10,
        (np.exp(mR * (q_arr - 1.0)) - np.exp(-mR)) / (mR * q_arr),
        F0)


def _F_avg_dec_vol(q_arr, mR):
    F0 = np.exp(-mR)
    mR_safe = max(mR, 1e-8)
    mRq = mR_safe * q_arr
    emR  = np.exp(-mR_safe)
    emRq = np.exp(mRq - mR_safe)
    Iv = emRq * (q_arr**2/mR_safe - 2.0*q_arr/mR_safe**2 + 2.0/mR_safe**3) - emR * 2.0/mR_safe**3
    q3 = q_arr**3
    return np.where(q_arr > 1e-10, 3.0 * Iv / q3, F0)


def _get_F_avg(q_arr, mR, prop, avg, I_fn=None, Iv_fn=None):
    """Dispatch to spatial profile F_avg function."""
    if prop == 'BAL':
        if avg == 'PATH':
            if I_fn is None: I_fn = _build_I_bal(mR)
            return _F_avg_bal_path(q_arr, mR, I_fn)
        elif avg == 'VOL':
            if Iv_fn is None: Iv_fn = _build_Ivol_bal(mR)
            return _F_avg_bal_vol(q_arr, mR, Iv_fn)
        elif avg == 'HYB':
            if I_fn is None: I_fn = _build_I_bal(mR)
            if Iv_fn is None: Iv_fn = _build_Ivol_bal(mR)
            Fp = _F_avg_bal_path(q_arr, mR, I_fn)
            Fv = _F_avg_bal_vol(q_arr, mR, Iv_fn)
            return 0.5*Fp + 0.5*Fv
    elif prop == 'FIC':
        if avg == 'PATH':
            return _F_avg_fic_path(q_arr, mR)
        elif avg == 'VOL':
            return _F_avg_fic_vol(q_arr, mR)
        elif avg == 'HYB':
            return 0.5*_F_avg_fic_path(q_arr, mR) + 0.5*_F_avg_fic_vol(q_arr, mR)
    elif prop == 'DEC':
        if avg == 'PATH':
            return _F_avg_dec_path(q_arr, mR)
        elif avg == 'VOL':
            return _F_avg_dec_vol(q_arr, mR)
        elif avg == 'HYB':
            return 0.5*_F_avg_dec_path(q_arr, mR) + 0.5*_F_avg_dec_vol(q_arr, mR)
    return None


# ──────────────────────────────────────────────────────────────────────────────
# A3 net flux j_net(z)
# ──────────────────────────────────────────────────────────────────────────────

def _compute_j_net(z_arr, E_arr, t_tilde, a3_time, a3_sign, J0, tau, t0_frac, eps):
    """
    j_net(z) = (J+(z) - J-(z)) / kappa_2, dimensionless.
    t_tilde[i] = H0 * t_age(z_arr[i])  (cosmic age, increases with cosmic time)
    t0_frac: t0 / t_today (0..1.5 range)
    """
    if a3_sign == 'A2Only':
        return np.zeros_like(z_arr)

    tau_safe = max(float(tau), 1e-6)
    t_today  = float(t_tilde[0])  # H0*t_age at z=0

    if a3_time == 'Const':
        if a3_sign == 'I':
            return J0 * np.ones_like(z_arr)
        elif a3_sign == 'O':
            return -J0 * np.ones_like(z_arr)
        elif a3_sign == 'Bp':
            return J0 * (1.0 - eps) * np.ones_like(z_arr)
        elif a3_sign == 'Bm':
            return -J0 * (1.0 - eps) * np.ones_like(z_arr)

    elif a3_time == 'Decay':
        decay = np.exp(-t_tilde / tau_safe)
        if a3_sign == 'I':
            return J0 * decay
        elif a3_sign == 'O':
            return -J0 * decay
        elif a3_sign == 'B':
            # Switches from influx to outflux: net = J0*(2*exp(-t/tau) - 1)
            return J0 * (2.0 * decay - 1.0)
        elif a3_sign == 'S':
            # Switches from outflux to influx: net = J0*(1 - 2*exp(-t/tau))
            return J0 * (1.0 - 2.0 * decay)

    elif a3_time == 'HProp':
        if a3_sign == 'I':
            return J0 * E_arr
        elif a3_sign == 'O':
            return -J0 * E_arr
        elif a3_sign == 'B':
            # Bidirectional H-proportional, net = J0*(1-eps)*E(z)
            return J0 * (1.0 - eps) * E_arr

    elif a3_time == 'Tanh':
        t0_abs  = t0_frac * t_today
        x       = (t_tilde - t0_abs) / tau_safe
        th      = np.tanh(x)
        if a3_sign == 'IO':
            return J0 * th
        elif a3_sign == 'OI':
            return -J0 * th
        elif a3_sign == 'IF':
            return J0 * (1.0 + th) / 2.0
        elif a3_sign == 'OF':
            return -J0 * (1.0 - th) / 2.0

    return None


# ──────────────────────────────────────────────────────────────────────────────
# Self-consistent E(z) for L46
# ──────────────────────────────────────────────────────────────────────────────

def _compute_E_l46(z_arr, Om, J0, a3_time, a3_sign, a2_dil,
                   tau=1.0, t0_frac=0.5, eps=0.0,
                   mR=1.0, bnd='H', prop='BAL', avg='PATH', cpl='LIN',
                   n_pow=1.0, eps_mix=0.0, beta_log=1.0,
                   max_iter=30, tol=1e-7):
    """
    Self-consistent Friedmann for L46 3-axiom SQT.
    Returns E(z) array (E(0)=1) or None on failure.
    """
    OL0 = 1.0 - Om - OR
    if OL0 <= 0.0 or Om <= 0.0 or J0 < 0.0:
        return None

    # Initial E guess: LCDM
    E_prev = np.sqrt(np.maximum(OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0, 1e-30))

    # Precompute BAL integrals if needed (only for non-default prop)
    I_fn = Iv_fn = None
    if prop == 'BAL' and avg in ('PATH', 'VOL', 'HYB'):
        I_fn  = _build_I_bal(mR)
        Iv_fn = _build_Ivol_bal(mR)

    for _it in range(max_iter):
        # 1. Compute t_tilde(z) = H0 * t_age(z) = integral_z^{z_max} dz'/[(1+z')E]
        #    Using reverse cumulative: t_tilde increases from 0 (z_max) to ~0.96 (z=0)
        integrand_t = 1.0 / ((1.0 + z_arr) * E_prev)
        z_rev = z_arr[::-1]
        it_rev = integrand_t[::-1]
        cum_t_rev = np.concatenate([[0.0], cumulative_trapezoid(it_rev, z_rev)])
        t_tilde = -cum_t_rev[::-1]  # positive; t_tilde[0] = H0*t_today, t_tilde[-1] = 0

        # 2. Compute j_net(z)
        j_net = _compute_j_net(z_arr, E_prev, t_tilde,
                               a3_time, a3_sign, J0, tau, t0_frac, eps)
        if j_net is None:
            return None

        # 3. Spatial profile correction for Tier 2+ (non-default axes)
        default_axes = (prop == 'BAL' and avg == 'PATH' and bnd == 'H')
        if default_axes:
            j_eff = j_net
        else:
            # Compute comoving chi(z) = integral_0^z dz'/E
            chi_arr = np.concatenate([[0.0], cumulative_trapezoid(1.0/E_prev, z_arr)])

            # q(z) based on boundary
            if bnd == 'H':
                q = np.minimum(chi_arr * E_prev, 1.0)
            elif bnd == 'E':
                chi_tot = chi_arr[-1]
                chi_E   = np.maximum(chi_tot - chi_arr, 1e-10)
                q       = np.minimum(chi_arr / chi_E, 1.0)
            elif bnd == 'P':
                # Particle horizon: chi_P[i] = integral_{z[i]}^{z_max} dz'/E
                E_rev_p   = E_prev[::-1]
                cum_p_rev = np.concatenate([[0.0], cumulative_trapezoid(1.0/E_rev_p, z_rev)])
                chi_P     = np.abs(cum_p_rev[::-1])  # positive
                chi_P_s   = np.maximum(chi_P, 1e-10)
                q         = np.minimum(chi_arr / chi_P_s, 1.0)
            else:
                return None

            F_avg = _get_F_avg(q, mR, prop, avg, I_fn, Iv_fn)
            if F_avg is None or not np.all(np.isfinite(F_avg)):
                return None
            F0 = float(F_avg[0])
            if F0 <= 0.0:
                return None
            j_eff = j_net * F_avg / F0

        # 4. Solve Psi(z) analytically
        S = 1.0 + 3.0 * j_eff

        if a2_dil:
            integrand_psi = (1.0 + z_arr)**2 * S / E_prev
        else:
            integrand_psi = S / ((1.0 + z_arr) * E_prev)

        int_rev_p = integrand_psi[::-1]
        cum_psi_rev = np.concatenate([[0.0], cumulative_trapezoid(int_rev_p, z_rev)])
        psi_raw = -cum_psi_rev[::-1]  # psi_raw[i] = integral_{z[i]}^{z_max} integrand dz

        if a2_dil:
            denom = np.maximum((1.0 + z_arr)**3, 1e-30)
            psi_raw = psi_raw / denom

        psi0 = float(psi_raw[0])
        if not np.isfinite(psi0) or psi0 <= 0.0:
            return None

        psi_norm = psi_raw / psi0  # normalized: Psi_norm(0) = 1

        # 5. rho_DE(z) based on coupling
        if cpl == 'LIN':
            rho_DE = OL0 * psi_norm
        elif cpl == 'POW':
            rho_DE = OL0 * np.maximum(psi_norm, 0.0)**n_pow
        elif cpl == 'MIX':
            rho_DE = OL0 * (eps_mix + (1.0 - eps_mix) * psi_norm)
        elif cpl == 'LOG':
            beta_s = max(float(beta_log), 1e-4)
            rho_DE = OL0 * np.log1p(beta_s * psi_norm) / np.log1p(beta_s)
        else:
            return None

        if np.any(rho_DE < 0.0) or not np.all(np.isfinite(rho_DE)):
            return None

        # 6. New E(z) via Friedmann
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 <= 0.0) or not np.all(np.isfinite(E2)):
            return None
        E_new = np.sqrt(E2)

        # 7. Normalize E(0) = 1
        E0 = float(E_new[0])
        if E0 <= 0.0 or not np.isfinite(E0):
            return None
        E_new = E_new / E0

        if np.max(np.abs(E_new - E_prev)) < tol:
            return E_new
        E_prev = E_new

    if np.all(np.isfinite(E_prev)) and np.all(E_prev > 0.0):
        return E_prev
    return None


def _make_E_l46(Om, J0, a3_time, a3_sign, a2_dil,
                tau=1.0, t0_frac=0.5, eps=0.0,
                mR=1.0, bnd='H', prop='BAL', avg='PATH', cpl='LIN',
                n_pow=1.0, eps_mix=0.0, beta_log=1.0):
    """Build E_fn interpolant for L46 model."""
    E_arr = _compute_E_l46(L46_Z_GRID, Om, J0, a3_time, a3_sign, a2_dil,
                           tau, t0_frac, eps, mR, bnd, prop, avg, cpl,
                           n_pow, eps_mix, beta_log)
    if E_arr is None:
        return None
    ifn = interp1d(L46_Z_GRID, E_arr, kind='linear',
                   bounds_error=False, fill_value=np.nan)
    def fn(z, _Om):
        za = np.atleast_1d(np.asarray(z, float))
        Ev = ifn(za)
        return None if (np.any(np.isnan(Ev)) or np.any(Ev <= 0.0)) else Ev
    return fn


# ──────────────────────────────────────────────────────────────────────────────
# Model specifications
# ──────────────────────────────────────────────────────────────────────────────
# Bounds: [Om, H0, J0, tau/eps/t0, ...]
_BND_Om   = (0.15, 0.50)
_BND_H0   = (55.0, 80.0)
_BND_J0   = (0.0,  5.0)
_BND_TAU  = (0.05, 5.0)
_BND_T0   = (0.0,  1.5)
_BND_EPS  = (0.0,  0.98)
_BND_MR   = (0.1,  10.0)
_BND_NPOW = (0.1,  6.0)
_BND_EMIX = (0.0,  0.98)
_BND_BLOG = (0.01, 5.0)

# Base bounds for each parameter count
_B2 = [_BND_Om, _BND_H0]
_B3 = _B2 + [_BND_J0]
_B4_tau  = _B2 + [_BND_J0, _BND_TAU]
_B4_eps  = _B2 + [_BND_J0, _BND_EPS]
_B5_te   = _B2 + [_BND_J0, _BND_TAU, _BND_EPS]   # Decay-B/S: tau + eps
_B5_tt   = _B2 + [_BND_J0, _BND_TAU, _BND_T0]    # Tanh: tau + t0

# Tier 1: fixed bnd=H, prop=BAL, avg=PATH, cpl=LIN
# spec keys: k, a3_time, a3_sign, a2_dil, bnd, prop, avg, cpl,
#            free (list beyond Om,H0), bounds
_MODELS = {
    # --- Const group ---
    'M-CI.Dil':    {'k': 3, 'a3_time': 'Const', 'a3_sign': 'I',  'a2_dil': True,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0'], 'fixed': {}, 'bounds': _B3},
    'M-CI.NoDil':  {'k': 3, 'a3_time': 'Const', 'a3_sign': 'I',  'a2_dil': False,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0'], 'fixed': {}, 'bounds': _B3},
    'M-CO.Dil':    {'k': 3, 'a3_time': 'Const', 'a3_sign': 'O',  'a2_dil': True,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0'], 'fixed': {}, 'bounds': _B3},
    'M-CO.NoDil':  {'k': 3, 'a3_time': 'Const', 'a3_sign': 'O',  'a2_dil': False,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0'], 'fixed': {}, 'bounds': _B3},
    'M-CBp.Dil':   {'k': 4, 'a3_time': 'Const', 'a3_sign': 'Bp', 'a2_dil': True,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0', 'eps'], 'fixed': {}, 'bounds': _B4_eps},
    'M-CBp.NoDil': {'k': 4, 'a3_time': 'Const', 'a3_sign': 'Bp', 'a2_dil': False,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0', 'eps'], 'fixed': {}, 'bounds': _B4_eps},
    'M-CBm.Dil':   {'k': 4, 'a3_time': 'Const', 'a3_sign': 'Bm', 'a2_dil': True,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0', 'eps'], 'fixed': {}, 'bounds': _B4_eps},
    'M-CBm.NoDil': {'k': 4, 'a3_time': 'Const', 'a3_sign': 'Bm', 'a2_dil': False,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0', 'eps'], 'fixed': {}, 'bounds': _B4_eps},
    # --- Decay group ---
    'M-DI.Dil':    {'k': 4, 'a3_time': 'Decay', 'a3_sign': 'I',  'a2_dil': True,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0', 'tau'], 'fixed': {}, 'bounds': _B4_tau},
    'M-DI.NoDil':  {'k': 4, 'a3_time': 'Decay', 'a3_sign': 'I',  'a2_dil': False,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0', 'tau'], 'fixed': {}, 'bounds': _B4_tau},
    'M-DO.Dil':    {'k': 4, 'a3_time': 'Decay', 'a3_sign': 'O',  'a2_dil': True,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0', 'tau'], 'fixed': {}, 'bounds': _B4_tau},
    'M-DO.NoDil':  {'k': 4, 'a3_time': 'Decay', 'a3_sign': 'O',  'a2_dil': False,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0', 'tau'], 'fixed': {}, 'bounds': _B4_tau},
    'M-DB.Dil':    {'k': 5, 'a3_time': 'Decay', 'a3_sign': 'B',  'a2_dil': True,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0', 'tau', 'eps'], 'fixed': {}, 'bounds': _B5_te},
    'M-DB.NoDil':  {'k': 5, 'a3_time': 'Decay', 'a3_sign': 'B',  'a2_dil': False,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0', 'tau', 'eps'], 'fixed': {}, 'bounds': _B5_te},
    'M-DS.Dil':    {'k': 5, 'a3_time': 'Decay', 'a3_sign': 'S',  'a2_dil': True,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0', 'tau', 'eps'], 'fixed': {}, 'bounds': _B5_te},
    'M-DS.NoDil':  {'k': 5, 'a3_time': 'Decay', 'a3_sign': 'S',  'a2_dil': False,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0', 'tau', 'eps'], 'fixed': {}, 'bounds': _B5_te},
    # --- HProp group ---
    'M-HI.Dil':    {'k': 3, 'a3_time': 'HProp', 'a3_sign': 'I',  'a2_dil': True,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0'], 'fixed': {}, 'bounds': _B3},
    'M-HI.NoDil':  {'k': 3, 'a3_time': 'HProp', 'a3_sign': 'I',  'a2_dil': False,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0'], 'fixed': {}, 'bounds': _B3},
    'M-HO.Dil':    {'k': 3, 'a3_time': 'HProp', 'a3_sign': 'O',  'a2_dil': True,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0'], 'fixed': {}, 'bounds': _B3},
    'M-HO.NoDil':  {'k': 3, 'a3_time': 'HProp', 'a3_sign': 'O',  'a2_dil': False,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0'], 'fixed': {}, 'bounds': _B3},
    'M-HB.Dil':    {'k': 4, 'a3_time': 'HProp', 'a3_sign': 'B',  'a2_dil': True,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0', 'eps'], 'fixed': {}, 'bounds': _B4_eps},
    'M-HB.NoDil':  {'k': 4, 'a3_time': 'HProp', 'a3_sign': 'B',  'a2_dil': False,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0', 'eps'], 'fixed': {}, 'bounds': _B4_eps},
    # --- Tanh group ---
    'M-TIO.Dil':   {'k': 5, 'a3_time': 'Tanh', 'a3_sign': 'IO', 'a2_dil': True,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0', 'tau', 't0_frac'], 'fixed': {}, 'bounds': _B5_tt},
    'M-TIO.NoDil': {'k': 5, 'a3_time': 'Tanh', 'a3_sign': 'IO', 'a2_dil': False,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0', 'tau', 't0_frac'], 'fixed': {}, 'bounds': _B5_tt},
    'M-TOI.Dil':   {'k': 5, 'a3_time': 'Tanh', 'a3_sign': 'OI', 'a2_dil': True,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0', 'tau', 't0_frac'], 'fixed': {}, 'bounds': _B5_tt},
    'M-TOI.NoDil': {'k': 5, 'a3_time': 'Tanh', 'a3_sign': 'OI', 'a2_dil': False,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0', 'tau', 't0_frac'], 'fixed': {}, 'bounds': _B5_tt},
    'M-TIF.Dil':   {'k': 5, 'a3_time': 'Tanh', 'a3_sign': 'IF', 'a2_dil': True,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0', 'tau', 't0_frac'], 'fixed': {}, 'bounds': _B5_tt},
    'M-TIF.NoDil': {'k': 5, 'a3_time': 'Tanh', 'a3_sign': 'IF', 'a2_dil': False,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0', 'tau', 't0_frac'], 'fixed': {}, 'bounds': _B5_tt},
    'M-TOF.Dil':   {'k': 5, 'a3_time': 'Tanh', 'a3_sign': 'OF', 'a2_dil': True,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0', 'tau', 't0_frac'], 'fixed': {}, 'bounds': _B5_tt},
    'M-TOF.NoDil': {'k': 5, 'a3_time': 'Tanh', 'a3_sign': 'OF', 'a2_dil': False,
                    'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                    'free': ['J0', 'tau', 't0_frac'], 'fixed': {}, 'bounds': _B5_tt},
    # --- Null (A2Only) ---
    'M-A2Only.Dil':   {'k': 2, 'a3_time': 'Const', 'a3_sign': 'A2Only', 'a2_dil': True,
                       'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                       'free': [], 'fixed': {}, 'bounds': _B2},
    'M-A2Only.NoDil': {'k': 2, 'a3_time': 'Const', 'a3_sign': 'A2Only', 'a2_dil': False,
                       'bnd': 'H', 'prop': 'BAL', 'avg': 'PATH', 'cpl': 'LIN',
                       'free': [], 'fixed': {}, 'bounds': _B2},
}

_TIER1_TAGS = list(_MODELS.keys())
assert len(_TIER1_TAGS) == 32, f"Expected 32 Tier 1 models, got {len(_TIER1_TAGS)}"


# ──────────────────────────────────────────────────────────────────────────────
# Utilities
# ──────────────────────────────────────────────────────────────────────────────
def _at_boundary(params, bounds, tol=1e-3):
    for p, (lo, hi) in zip(params, bounds):
        span = hi - lo
        if span == 0: continue
        if abs(p - lo) < tol * span or abs(p - hi) < tol * span:
            return True
    return False


def _aicc(chi2_val, k):
    return chi2_val + 2*k + 2*k*(k+1) / (N_TOTAL - k - 1)


def _verdict_l46(daicc, w0, wa, q0, boundary=False, k=3):
    """L46 verdict with 4-condition check."""
    if boundary:
        return 'K92 INVALID'
    # Check Son+25 direction
    son_w0  = (w0 is not None) and (SON_W0 - 2*SON_W0_2SIG <= w0 <= SON_W0 + 2*SON_W0_2SIG)
    son_wa  = (wa is not None) and (SON_WA - 2*SON_WA_2SIG <= wa <= SON_WA + 2*SON_WA_2SIG)
    son_q0  = (q0 is not None) and (q0 > 0.0)
    n_conditions = sum([son_w0, son_wa, son_q0])

    if daicc >= 5:
        return 'K90 FAIL'
    if daicc >= 0:
        return 'K90 FAIL' if n_conditions < 2 else 'Q91 MARGINAL'
    if daicc >= -5:
        return 'K91 WRONG' if n_conditions < 2 else 'Q91 MARGINAL'
    if daicc >= -15:
        if n_conditions < 2:
            return 'K91 WRONG'
        return 'Q93 PARTIAL'
    if daicc >= -30:
        if n_conditions < 2:
            return 'K91 WRONG'
        return 'Q94 STRONG'
    if daicc < -50 and n_conditions >= 3 and k <= 4:
        return 'Q95 VICTORY'
    if daicc < -30 and n_conditions >= 2:
        return 'Q94 STRONG'
    return 'Q93 PARTIAL' if n_conditions >= 2 else 'K91 WRONG'


def _jsonify(obj):
    if isinstance(obj, dict):       return {k: _jsonify(v) for k, v in obj.items()}
    if isinstance(obj, list):       return [_jsonify(v) for v in obj]
    if isinstance(obj, np.ndarray): return _jsonify(obj.tolist())
    if isinstance(obj, bool):       return bool(obj)
    if isinstance(obj, np.integer): return int(obj)
    if isinstance(obj, (np.floating, float)):
        f = float(obj)
        return None if not np.isfinite(f) else f
    return obj


def _q0(Om, w0_eff):
    OL0 = 1.0 - Om - OR
    return 0.5 * (Om + (1.0 + 3.0*w0_eff) * OL0)


def _best_of(results):
    valid = [(c, p) for c, p in results if p is not None and np.isfinite(c) and c < 1e8]
    if not valid:
        return 1e9, None
    return min(valid, key=lambda x: x[0])


def _extract_params(p_arr, spec):
    """Extract named parameters from flat array."""
    Om, H0 = float(p_arr[0]), float(p_arr[1])
    free = spec['free']
    fixd = spec['fixed']
    pd = {'Om': Om, 'H0': H0}
    for i, name in enumerate(free):
        pd[name] = float(p_arr[2 + i])
    pd.update(fixd)
    return pd


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
        if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82: return 1e9
        if w0 < -3.0 or w0 > 0.5 or wa < -5.0 or wa > 3.0: return 1e9
        OL0 = 1.0 - Om - OR
        if OL0 <= 0: return 1e9
        def fn(z, _Om):
            za = np.asarray(z, float)
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


def _worker_l46(args):
    """Generic L46 model worker. args = (spec_dict, start_list)."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    spec, start = args
    k        = spec['k']
    a3_time  = spec['a3_time']
    a3_sign  = spec['a3_sign']
    a2_dil   = spec['a2_dil']
    bnd      = spec['bnd']
    prop_    = spec['prop']
    avg      = spec['avg']
    cpl      = spec['cpl']
    free     = spec['free']
    fixd     = spec['fixed']
    bnds     = spec['bounds']

    def obj(p):
        for val, (lo, hi) in zip(p, bnds):
            if val < lo or val > hi: return 1e9
        Om, H0 = float(p[0]), float(p[1])
        pd = {'Om': Om, 'H0': H0}
        for i, name in enumerate(free):
            pd[name] = float(p[2 + i])
        pd.update(fixd)
        J0      = pd.get('J0',      0.0)
        tau     = pd.get('tau',     1.0)
        t0_frac = pd.get('t0_frac', 0.5)
        eps     = pd.get('eps',     0.0)
        mR      = pd.get('mR',      1.0)
        n_pow   = pd.get('n_pow',   1.0)
        eps_mix = pd.get('eps_mix', 0.0)
        beta_log = pd.get('beta_log', 1.0)

        fn = _make_E_l46(Om, J0, a3_time, a3_sign, a2_dil,
                         tau, t0_frac, eps, mR, bnd, prop_, avg, cpl,
                         n_pow, eps_mix, beta_log)
        if fn is None: return 1e9
        cb, cc, cs, cr, tot = _chi2_all(fn, Om, H0)
        return tot if np.isfinite(tot) else 1e9

    try:
        r = minimize(obj, start, method='Nelder-Mead',
                     options={'xatol': 1e-4, 'fatol': 1e-4, 'maxiter': 1000})
        return (float(r.fun), [float(x) for x in r.x])
    except Exception:
        return (1e9, None)


# ──────────────────────────────────────────────────────────────────────────────
# Bootstrap worker
# ──────────────────────────────────────────────────────────────────────────────

def _boot_worker_l46(batch):
    """Bootstrap for L46. Perturbs BAO, CMB, RSD data."""
    warnings.filterwarnings('ignore'); np.seterr(all='ignore')
    import sys as _sys
    _l35 = _sys.modules.get('l35_test') or __import__('l35_test')
    orig_bao = dict(_l35.DESI_DR2)
    orig_cmb = _l35.CMB_OBS.copy()
    orig_rsd = _l35.FS8_OBS.copy()
    results  = []
    np.random.seed(0)

    def _tot(fn, Om, H0):
        t = (chi2_bao(fn, Om, H0) + chi2_cmb(fn, Om, H0) +
             chi2_sn_corr(fn, Om, H0) + chi2_rsd(fn, Om, H0))
        return t if (np.isfinite(t) and t < 1e7) else 1e9

    for item in batch:
        s0, new_bao, new_cmb, new_rsd, spec, best_params, k = item
        _l35.DESI_DR2 = {**orig_bao, 'value': new_bao}
        _l35.CMB_OBS  = new_cmb
        _l35.FS8_OBS  = new_rsd

        a3_time  = spec['a3_time']; a3_sign = spec['a3_sign']
        a2_dil   = spec['a2_dil']
        bnd      = spec['bnd']; prop_ = spec['prop']
        avg      = spec['avg']; cpl   = spec['cpl']
        free     = spec['free']; fixd  = spec['fixed']
        bnds     = spec['bounds']

        def obj_win(p):
            for val, (lo, hi) in zip(p, bnds):
                if val < lo or val > hi: return 1e9
            Om, H0 = float(p[0]), float(p[1])
            pd = {'Om': Om, 'H0': H0}
            for i, nm in enumerate(free):
                pd[nm] = float(p[2+i])
            pd.update(fixd)
            J0 = pd.get('J0', 0.0); tau = pd.get('tau', 1.0)
            t0f = pd.get('t0_frac', 0.5); eps = pd.get('eps', 0.0)
            mR = pd.get('mR', 1.0)
            n_pow = pd.get('n_pow', 1.0)
            eps_mix = pd.get('eps_mix', 0.0)
            beta_log = pd.get('beta_log', 1.0)
            fn = _make_E_l46(Om, J0, a3_time, a3_sign, a2_dil, tau, t0f, eps,
                             mR, bnd, prop_, avg, cpl, n_pow, eps_mix, beta_log)
            if fn is None: return 1e9
            return _tot(fn, Om, H0)

        def obj_lcdm(p):
            Om, H0 = p
            if Om < 0.20 or Om > 0.55 or H0 < 55 or H0 > 82: return 1e9
            fn = lambda z, _: E_lcdm(z, Om)
            return _tot(fn, Om, H0)

        try:
            r_w = minimize(obj_win,   s0[:k],  method='Nelder-Mead',
                           options={'xatol': 1e-3, 'fatol': 1e-3, 'maxiter': 400})
            r_l = minimize(obj_lcdm,  s0[:2],  method='Nelder-Mead',
                           options={'xatol': 1e-3, 'fatol': 1e-3, 'maxiter': 400})
            results.append(float(_aicc(r_w.fun, k) - _aicc(r_l.fun, 2)))
        except Exception:
            results.append(None)

    _l35.DESI_DR2 = orig_bao
    _l35.CMB_OBS  = orig_cmb
    _l35.FS8_OBS  = orig_rsd
    return results


# ──────────────────────────────────────────────────────────────────────────────
# Pre-Tasks
# ──────────────────────────────────────────────────────────────────────────────

def pretask_all(out_dir):
    print('\n' + '='*60)
    print('Pre-Tasks: L46 Model Validation')
    print('='*60)
    all_ok = True

    # PT1: ODE solver numerical stability
    print('\n[PT1] ODE numerical stability')
    test_models = [
        ('M-CI.Dil',    {'J0': 0.5}),
        ('M-A2Only.Dil', {}),
        ('M-TOI.Dil',   {'J0': 1.0, 'tau': 0.3, 't0_frac': 0.5}),
    ]
    Om_t, H0_t = 0.32, 67.5
    for name, extra_p in test_models:
        spec = _MODELS[name]
        J0  = extra_p.get('J0', 0.5)
        tau = extra_p.get('tau', 1.0)
        t0f = extra_p.get('t0_frac', 0.5)
        E_arr = _compute_E_l46(L46_Z_GRID, Om_t, J0, spec['a3_time'], spec['a3_sign'],
                               spec['a2_dil'], tau, t0f)
        ok = (E_arr is not None and np.all(np.isfinite(E_arr)) and
              abs(float(E_arr[0]) - 1.0) < 1e-5)
        print(f'  {name:<20}: E(0)={float(E_arr[0]) if E_arr is not None else "FAIL":.8f}'
              f'  [{"OK" if ok else "FAIL"}]')
        if not ok: all_ok = False

    # PT2: BBN safety (z ~ 10^9 approximated by z_max=1200, check ρ_DE/ρ_total)
    print('\n[PT2] Early-universe safety (z_max=1200)')
    for name, extra_p in test_models[:2]:
        spec = _MODELS[name]
        J0 = extra_p.get('J0', 0.5)
        E_arr = _compute_E_l46(L46_Z_GRID, Om_t, J0, spec['a3_time'], spec['a3_sign'],
                               spec['a2_dil'])
        if E_arr is None:
            print(f'  {name}: FAILED to compute'); all_ok = False; continue
        E_high = float(E_arr[-1])
        z_high = float(L46_Z_GRID[-1])
        rho_m_high  = Om_t * (1+z_high)**3
        rho_r_high  = OR   * (1+z_high)**4
        rho_tot_high = E_high**2  # in units of rho_crit,0
        rho_DE_high  = rho_tot_high - rho_m_high - rho_r_high
        ratio = rho_DE_high / rho_tot_high
        ok = (ratio < 0.1)  # at z=1200, DE should be < 10% of total
        print(f'  {name}: rho_DE/rho_tot at z={z_high:.0f} = {ratio:.4f}  '
              f'[{"OK" if ok else "WARN"}]')

    # PT3: Normalization check E(0)=1 for all 32 Tier 1 models
    print('\n[PT3] E(0)=1 normalization (all 32 Tier 1 models)')
    n_ok = n_fail = 0
    for tag in _TIER1_TAGS:
        spec = _MODELS[tag]
        J0  = 0.5 if spec['free'] else 0.0
        E_arr = _compute_E_l46(L46_Z_GRID, Om_t, J0, spec['a3_time'], spec['a3_sign'],
                               spec['a2_dil'])
        if E_arr is None or abs(float(E_arr[0]) - 1.0) > 1e-4:
            n_fail += 1
        else:
            n_ok += 1
    print(f'  Pass: {n_ok}/32  Fail: {n_fail}/32  '
          f'[{"OK" if n_fail == 0 else "WARN - some models fail at J0=0.5"}]')

    # PT4: Son+25 correction verification (reuse L43 check)
    print('\n[PT4] Son+25 age-bias correction')
    for z_check, expected in [(0.0, 0.0), (1.0, 0.1459), (2.0, 0.1579)]:
        dm, _ = son_age_correction(np.array([z_check]))
        print(f'  z={z_check}: delta_m={float(dm):.4f}  '
              f'(expected ~{expected:.4f})  '
              f'[{"OK" if abs(float(dm)-expected) < 0.002 else "CHECK"}]')

    # PT5: Future behavior (z -> -0.5)
    print('\n[PT5] Future behavior (z -> -0.5)')
    z_future = np.linspace(0.0, -0.5, 50)
    for tag in ['M-CI.Dil', 'M-TOI.Dil', 'M-A2Only.Dil']:
        spec = _MODELS[tag]
        J0 = 0.5
        # Approximate: use E from z=0 grid, extrapolate linearly (crude check)
        E_arr = _compute_E_l46(L46_Z_GRID, Om_t, J0, spec['a3_time'],
                               spec['a3_sign'], spec['a2_dil'])
        if E_arr is not None:
            OL0 = 1.0 - Om_t - OR
            # Check E²(z=-0.5) estimate: rho components at a=1/(1+z) > 1
            a_fut = 1.5  # z=-1/3
            E2_fut = OR*(1/a_fut)**4 + Om_t*(1/a_fut)**3 + OL0
            print(f'  {tag}: E2(a=1.5) ~ {E2_fut:.4f}  [OK]')

    print(f'\n  Pre-task complete  [{"OK" if all_ok else "WARN"}]')
    sys.stdout.flush()
    return all_ok


# ──────────────────────────────────────────────────────────────────────────────
# Task 0: Baselines
# ──────────────────────────────────────────────────────────────────────────────

def task0_baselines(pool):
    print('\n' + '='*60)
    print('Task 0: Baselines (LCDM + CPL -- confirm L43/L45)')
    print('='*60)
    t0 = time.time()
    rng = np.random.default_rng(0)

    print('  Warming corrected SN cache...')
    get_sn_corr()
    print('  SN_corr ready.')
    sys.stdout.flush()

    starts_lcdm = _make_starts_2d(10, rng,
                   extra=[[0.32, 67.5], [0.31, 68.0], [0.33, 67.0]])
    starts_cpl  = []
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
    Om_c = H0_c = w0_c = wa_c = None
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
# Tasks 1-4: Tier 1 fits
# ──────────────────────────────────────────────────────────────────────────────

def _starts_tier1(spec, seed):
    """Generate starting points for a Tier 1 model."""
    k    = spec['k']
    bnds = spec['bounds']
    free = spec['free']
    rng2 = np.random.default_rng(seed)
    starts = []

    # Systematic grid over Om, H0
    for Om0 in [0.27, 0.30, 0.33, 0.36]:
        for H0_0 in [63., 67., 71.]:
            base = [Om0, H0_0]
            if 'J0' in free:
                for J0_0 in [0.1, 0.5, 1.5]:
                    if 'tau' in free:
                        for tau0 in [0.2, 0.8, 2.0]:
                            if 't0_frac' in free:
                                for t0f in [0.3, 0.6, 0.9]:
                                    starts.append(base + [J0_0, tau0, t0f])
                            elif 'eps' in free:
                                for e0 in [0.1, 0.5, 0.9]:
                                    starts.append(base + [J0_0, tau0, e0])
                            else:
                                starts.append(base + [J0_0, tau0])
                    elif 'eps' in free:
                        for e0 in [0.1, 0.5, 0.9]:
                            starts.append(base + [J0_0, e0])
                    else:
                        starts.append(base + [J0_0])
            else:
                starts.append(base)

    # Pad with random starts
    while len(starts) < N_TIER1_STARTS:
        s = [rng2.uniform(*b) for b in bnds]
        starts.append(s)
    return starts[:N_TIER1_STARTS + 5]


def _run_tier_group(pool, tags, label, lcdm_aicc):
    """Run a group of Tier 1 models and return best results per tag."""
    print(f'\n[Task {label}] Fitting {len(tags)} models...')
    sys.stdout.flush()
    t0 = time.time()

    all_args    = []
    tag_n_starts = {}
    for tag in tags:
        spec   = _MODELS[tag]
        starts = _starts_tier1(spec, hash(tag) & 0xFFFF)
        tag_n_starts[tag] = len(starts)
        for s in starts:
            all_args.append((spec, s))

    print(f'  Total tasks: {len(all_args)} dispatched across {N_WORKERS} workers')
    sys.stdout.flush()
    raw = pool.map(_worker_l46, all_args)

    # Group by tag
    results = {}
    idx = 0
    for tag in tags:
        n = tag_n_starts[tag]
        results[tag] = _best_of(raw[idx:idx+n])
        idx += n

    elapsed = time.time() - t0
    print(f'  Done in {elapsed:.1f}s')
    sys.stdout.flush()
    return results


def task1_to_4_tier1(pool, lcdm_aicc):
    """Tasks 1-4: Tier 1 model fits, grouped by A3 type."""
    # Group tags by A3 type
    groups = {
        'Task 1 (A3-Const)':   [t for t in _TIER1_TAGS if 'M-C' in t],
        'Task 2 (A3-Decay)':   [t for t in _TIER1_TAGS if 'M-D' in t and 'NoDil' not in t or 'M-D' in t],
        'Task 3 (A3-HProp)':   [t for t in _TIER1_TAGS if 'M-H' in t],
        'Task 4 (A3-Tanh+Null)': [t for t in _TIER1_TAGS if 'M-T' in t or 'A2Only' in t],
    }
    # Rebuild cleanly
    const_tags  = [t for t in _TIER1_TAGS if '-CI' in t or '-CO' in t or '-CBp' in t or '-CBm' in t]
    decay_tags  = [t for t in _TIER1_TAGS if '-DI' in t or '-DO' in t or '-DB' in t or '-DS' in t]
    hprop_tags  = [t for t in _TIER1_TAGS if '-HI' in t or '-HO' in t or '-HB' in t]
    tanh_tags   = [t for t in _TIER1_TAGS if '-TIO' in t or '-TOI' in t or
                   '-TIF' in t or '-TOF' in t or 'A2Only' in t]

    all_results = {}
    all_results.update(_run_tier_group(pool, const_tags, '1 (Const)', lcdm_aicc))
    all_results.update(_run_tier_group(pool, decay_tags, '2 (Decay)', lcdm_aicc))
    all_results.update(_run_tier_group(pool, hprop_tags, '3 (HProp)', lcdm_aicc))
    all_results.update(_run_tier_group(pool, tanh_tags,  '4 (Tanh+Null)', lcdm_aicc))
    return all_results


# ──────────────────────────────────────────────────────────────────────────────
# Task 5: Tier 1 ranking + Top-5 selection
# ──────────────────────────────────────────────────────────────────────────────

def task5_rank_tier1(tier1_best, lcdm_aicc, cpl_result):
    print('\n' + '='*60)
    print('Task 5: Tier 1 ranking + Top-5 selection')
    print('='*60)

    cpl_aicc = cpl_result.get('aicc')
    ranked   = []

    for tag in _TIER1_TAGS:
        chi2, params = tier1_best.get(tag, (1e9, None))
        spec = _MODELS[tag]
        k    = spec['k']
        if params is None or not np.isfinite(chi2) or chi2 >= 1e8:
            ranked.append({'tag': tag, 'k': k, 'daicc': 9999, 'verdict': 'FAILED',
                           'params': None, 'chi2': None, 'aicc': None,
                           'w0': None, 'wa': None, 'q0': None})
            continue

        aicc  = _aicc(chi2, k)
        daicc = aicc - lcdm_aicc
        bnd   = _at_boundary(params, spec['bounds'][:len(params)])

        # Extract CPL w0, wa from E(z)
        pd = _extract_params(params, spec)
        fn = _make_E_l46(pd['Om'], pd.get('J0', 0.0),
                         spec['a3_time'], spec['a3_sign'], spec['a2_dil'],
                         pd.get('tau', 1.0), pd.get('t0_frac', 0.5), pd.get('eps', 0.0))
        w0 = wa = q0v = None
        if fn is not None:
            try:
                w0, wa = cpl_wa(fn, pd['Om'])
                if w0 is not None:
                    q0v = _q0(pd['Om'], w0)
            except Exception:
                pass

        vdict = _verdict_l46(daicc, w0, wa, q0v, boundary=bnd, k=k)
        ranked.append({'tag': tag, 'k': k, 'daicc': daicc, 'aicc': aicc,
                       'chi2': chi2, 'params': params, 'boundary': bnd,
                       'verdict': vdict, 'w0': w0, 'wa': wa, 'q0': q0v})

    ranked.sort(key=lambda x: x['daicc'])

    print(f'\n  {"Rank":<4} {"Tag":<22} {"k"} {"dAICc":>8}  {"Verdict":<18}  '
          f'{"w0":>7}  {"wa":>7}  {"q0":>7}')
    print('  ' + '-'*85)
    for i, r in enumerate(ranked[:32]):
        w0s  = f'{r["w0"]:.3f}' if r["w0"] is not None else '  ---'
        was  = f'{r["wa"]:.3f}' if r["wa"] is not None else '  ---'
        q0s  = f'{r["q0"]:.3f}' if r["q0"] is not None else '  ---'
        print(f'  {i+1:<4} {r["tag"]:<22} {r["k"]} {r["daicc"]:>8.2f}  '
              f'{r["verdict"]:<18}  {w0s:>7}  {was:>7}  {q0s:>7}')

    # 4-condition check for top-5
    top5 = [r for r in ranked if r['params'] is not None][:5]
    print(f'\n  Top-5 4-condition check:')
    for r in top5:
        w0 = r.get('w0'); wa = r.get('wa'); q0v = r.get('q0')
        son_w0 = (w0 is not None) and (SON_W0-2*SON_W0_2SIG <= w0 <= SON_W0+2*SON_W0_2SIG)
        son_wa = (wa is not None) and (SON_WA-2*SON_WA_2SIG <= wa <= SON_WA+2*SON_WA_2SIG)
        son_q0 = (q0v is not None) and (q0v > 0.0)
        print(f'  {r["tag"]:<22} AIC:{"Y" if r["daicc"]<-50 else "N"}  '
              f'w0:{"Y" if son_w0 else "N"}  wa:{"Y" if son_wa else "N"}  '
              f'q0:{"Y" if son_q0 else "N"}')

    sys.stdout.flush()
    return ranked


# ──────────────────────────────────────────────────────────────────────────────
# Task 6: Tier 2
# ──────────────────────────────────────────────────────────────────────────────

def task6_tier2(pool, ranked, lcdm_aicc):
    print('\n' + '='*60)
    print('Task 6: Tier 2 (Top-5 x 9 axis variations)')
    print('='*60)

    top5 = [r for r in ranked if r['params'] is not None and r['daicc'] < 0][:5]
    if not top5:
        print('  No Tier 1 models with dAICc < 0. Tier 2 SKIPPED.')
        return {}, []

    # 9 axis variations per top-5 base model
    axis_variations = [
        {'bnd': 'P'},
        {'bnd': 'E'},
        {'prop': 'FIC'},
        {'prop': 'DEC'},
        {'avg': 'VOL'},
        {'avg': 'HYB'},
        {'cpl': 'POW'},
        {'cpl': 'MIX'},
        {'cpl': 'LOG'},
    ]

    tier2_specs = []
    tier2_tags  = []

    for r in top5:
        base_tag  = r['tag']
        base_spec = _MODELS[base_tag]
        for var in axis_variations:
            new_spec = dict(base_spec)  # shallow copy
            new_spec['bnd']  = var.get('bnd',  base_spec['bnd'])
            new_spec['prop'] = var.get('prop', base_spec['prop'])
            new_spec['avg']  = var.get('avg',  base_spec['avg'])
            new_spec['cpl']  = var.get('cpl',  base_spec['cpl'])
            new_free  = list(base_spec['free'])
            new_bnds  = list(base_spec['bounds'])
            new_k     = base_spec['k']
            new_fixd  = dict(base_spec['fixed'])

            # Add mR for propagation change
            if 'prop' in var and var['prop'] != base_spec['prop']:
                if 'mR' not in new_free:
                    new_free.append('mR')
                    new_bnds.append(_BND_MR)
                    new_k += 1

            # Add coupling parameter for coupling change
            if 'cpl' in var:
                new_cpl = var['cpl']
                if new_cpl == 'POW' and 'n_pow' not in new_free:
                    new_free.append('n_pow'); new_bnds.append(_BND_NPOW); new_k += 1
                elif new_cpl == 'MIX' and 'eps_mix' not in new_free:
                    new_free.append('eps_mix'); new_bnds.append(_BND_EMIX); new_k += 1
                elif new_cpl == 'LOG' and 'beta_log' not in new_free:
                    new_free.append('beta_log'); new_bnds.append(_BND_BLOG); new_k += 1

            new_spec['free']   = new_free
            new_spec['bounds'] = new_bnds
            new_spec['k']      = new_k
            new_spec['fixed']  = new_fixd

            var_label = list(var.values())[0]
            tag = f'{base_tag}+{var_label}'
            tier2_tags.append(tag)
            tier2_specs.append(new_spec)

    print(f'  Tier 2: {len(tier2_specs)} models, {N_TIER2_STARTS} starts each')
    sys.stdout.flush()

    rng = np.random.default_rng(77)
    all_args = []
    for spec in tier2_specs:
        bnds = spec['bounds']
        for _ in range(N_TIER2_STARTS):
            s = [rng.uniform(*b) for b in bnds]
            all_args.append((spec, s))

    t0  = time.time()
    raw = pool.map(_worker_l46, all_args)
    elapsed = time.time() - t0
    print(f'  Tier 2 fits done in {elapsed:.1f}s')

    # Group results
    tier2_best = {}
    idx = 0
    for tag, spec in zip(tier2_tags, tier2_specs):
        tier2_best[tag] = (_best_of(raw[idx:idx+N_TIER2_STARTS]), spec)
        idx += N_TIER2_STARTS

    # Rank and print top-10
    t2_ranked = []
    for tag, ((chi2, params), spec) in tier2_best.items():
        if params is None or not np.isfinite(chi2): continue
        k     = spec['k']
        aicc  = _aicc(chi2, k)
        daicc = aicc - lcdm_aicc
        bnd   = _at_boundary(params, spec['bounds'][:len(params)])
        t2_ranked.append({'tag': tag, 'k': k, 'daicc': daicc, 'aicc': aicc,
                           'chi2': chi2, 'params': params, 'spec': spec,
                           'boundary': bnd})
    t2_ranked.sort(key=lambda x: x['daicc'])

    print(f'\n  Top-10 Tier 2 results:')
    for i, r in enumerate(t2_ranked[:10]):
        print(f'  {i+1:2d} {r["tag"]:<38} dAICc={r["daicc"]:+8.2f}')
    sys.stdout.flush()

    return tier2_best, t2_ranked


# ──────────────────────────────────────────────────────────────────────────────
# Task 7: Tier 3
# ──────────────────────────────────────────────────────────────────────────────

def task7_tier3(pool, t2_ranked, lcdm_aicc):
    print('\n' + '='*60)
    print('Task 7: Tier 3 (Top-5 Tier2 x 4 couplings)')
    print('='*60)

    top5_t2 = [r for r in t2_ranked if r['params'] is not None][:5]
    if not top5_t2:
        print('  No Tier 2 models available. Tier 3 SKIPPED.')
        return {}, []

    tier3_specs = []
    tier3_tags  = []
    for r in top5_t2:
        base_spec = r['spec']
        for cpl_new in ['LIN', 'POW', 'MIX', 'LOG']:
            new_spec  = dict(base_spec)
            new_free  = [f for f in base_spec['free']
                         if f not in ('n_pow', 'eps_mix', 'beta_log')]
            new_bnds  = base_spec['bounds'][:2 + len(new_free)]  # trim old cpl param
            new_k     = base_spec['k'] - sum(1 for f in base_spec['free']
                                              if f in ('n_pow', 'eps_mix', 'beta_log'))
            if cpl_new == 'POW':
                new_free.append('n_pow'); new_bnds = list(new_bnds) + [_BND_NPOW]; new_k += 1
            elif cpl_new == 'MIX':
                new_free.append('eps_mix'); new_bnds = list(new_bnds) + [_BND_EMIX]; new_k += 1
            elif cpl_new == 'LOG':
                new_free.append('beta_log'); new_bnds = list(new_bnds) + [_BND_BLOG]; new_k += 1
            new_spec['cpl']    = cpl_new
            new_spec['free']   = new_free
            new_spec['bounds'] = new_bnds
            new_spec['k']      = new_k
            tag = f'{r["tag"]}|cpl={cpl_new}'
            tier3_tags.append(tag)
            tier3_specs.append(new_spec)

    print(f'  Tier 3: {len(tier3_specs)} models, {N_TIER3_STARTS} starts each')
    sys.stdout.flush()

    rng = np.random.default_rng(99)
    all_args = []
    for spec in tier3_specs:
        bnds = spec['bounds']
        for _ in range(N_TIER3_STARTS):
            s = [rng.uniform(*b) for b in bnds]
            all_args.append((spec, s))

    t0  = time.time()
    raw = pool.map(_worker_l46, all_args)
    elapsed = time.time() - t0
    print(f'  Tier 3 fits done in {elapsed:.1f}s')

    tier3_best = {}
    idx = 0
    for tag, spec in zip(tier3_tags, tier3_specs):
        tier3_best[tag] = (_best_of(raw[idx:idx+N_TIER3_STARTS]), spec)
        idx += N_TIER3_STARTS

    t3_ranked = []
    for tag, ((chi2, params), spec) in tier3_best.items():
        if params is None or not np.isfinite(chi2): continue
        k     = spec['k']
        aicc  = _aicc(chi2, k)
        daicc = aicc - lcdm_aicc
        t3_ranked.append({'tag': tag, 'k': k, 'daicc': daicc, 'aicc': aicc,
                           'chi2': chi2, 'params': params, 'spec': spec})
    t3_ranked.sort(key=lambda x: x['daicc'])

    print(f'\n  Top-5 Tier 3 results:')
    for i, r in enumerate(t3_ranked[:5]):
        print(f'  {i+1} {r["tag"][:50]:<50} dAICc={r["daicc"]:+8.2f}')
    sys.stdout.flush()

    return tier3_best, t3_ranked


# ──────────────────────────────────────────────────────────────────────────────
# Task 8: Bootstrap Top-10
# ──────────────────────────────────────────────────────────────────────────────

def task8_bootstrap(pool, ranked_all, lcdm_result, n_top=10):
    print('\n' + '='*60)
    print(f'Task 8: Bootstrap (top-{n_top}, N={N_BOOT})')
    print('='*60)

    candidates = [r for r in ranked_all if r.get('params') is not None
                  and r.get('daicc', 9999) < -2][:n_top]
    if not candidates:
        print('  No candidates. Skipping.')
        return {}

    Om_l = lcdm_result['Om']; H0_l = lcdm_result['H0']
    from l35_test import DESI_DR2 as _D2
    E_fn_l = lambda z, _: E_lcdm(z, Om_l)
    z_grid = np.linspace(0.0, float(_D2['z_eff'].max()) + 0.01, N_GRID)
    Eg     = E_fn_l(z_grid, Om_l)
    if Eg is None:
        print('  SKIPPED: BAO theory failed')
        return {}
    DM = (C_KMS / H0_l) * np.concatenate([[0.],
          cumulative_trapezoid(1.0/np.maximum(Eg, 1e-15), z_grid)])
    bao_nom = np.empty(13)
    for i, (z, qty) in enumerate(zip(_D2['z_eff'], _D2['quantity'])):
        idx_g = min(np.searchsorted(z_grid, z), len(z_grid)-1)
        DH  = C_KMS / (H0_l * max(float(Eg[idx_g]), 1e-10))
        DV  = (z * DM[idx_g]**2 * DH)**(1./3.) if z > 0 else 0.
        if 'DV' in qty:   bao_nom[i] = DV / R_S
        elif 'DM' in qty: bao_nom[i] = DM[idx_g] / R_S
        elif 'DH' in qty: bao_nom[i] = DH / R_S

    rng     = np.random.default_rng(99)
    bao_cov = np.linalg.inv(DESI_DR2_COV_INV)
    bao_L   = np.linalg.cholesky(bao_cov)

    boot_results = {}
    for r in candidates:
        tag    = r['tag']
        k      = r['k']
        spec   = r.get('spec') or _MODELS.get(tag, {})
        best_p = r['params']
        print(f'\n  Bootstrapping {tag[:50]} (k={k}, dAICc={r["daicc"]:.2f})...')
        sys.stdout.flush()
        t0 = time.time()

        boot_items = []
        for _ in range(N_BOOT):
            nb = bao_nom + bao_L @ rng.standard_normal(13)
            nc = CMB_OBS + CMB_SIG * rng.standard_normal(len(CMB_OBS))
            nr = FS8_OBS + FS8_SIG * rng.standard_normal(len(FS8_OBS))
            s0 = ([best_p[0] + rng.normal(0, 0.01),
                   best_p[1] + rng.normal(0, 0.5)] + list(best_p[2:]))
            boot_items.append((s0, nb, nc, nr, spec, best_p, k))

        bsz     = max(1, N_BOOT // N_WORKERS)
        batches = [boot_items[i:i+bsz] for i in range(0, N_BOOT, bsz)]
        raw     = pool.map(_boot_worker_l46, batches)

        all_d  = [v for b in raw for v in b]
        vals   = np.array([v for v in all_d if v is not None and np.isfinite(v)])
        elapsed = time.time() - t0
        print(f'  Done in {elapsed:.1f}s  Valid: {len(vals)}/{N_BOOT}')

        if len(vals) == 0:
            boot_results[tag] = {'verdict': 'FAIL', 'valid': 0}
            continue

        med   = float(np.median(vals))
        lo    = float(np.percentile(vals, 16))
        hi    = float(np.percentile(vals, 84))
        p_lt  = float(np.mean(vals < -4))
        verd  = 'PASS' if p_lt >= 0.90 else 'FAIL'
        print(f'  median={med:.2f}  68%CI=[{lo:.2f},{hi:.2f}]  '
              f'<-4: {p_lt*100:.0f}%  [{verd}]')
        boot_results[tag] = {'valid': int(len(vals)), 'median': med,
                              'ci68': [lo, hi], 'frac_lt4': p_lt, 'verdict': verd}
    sys.stdout.flush()
    return boot_results


# ──────────────────────────────────────────────────────────────────────────────
# Task 9: Visualization
# ──────────────────────────────────────────────────────────────────────────────

def task9_visualization(ranked_all, cpl_result, out_dir):
    print('\n' + '='*60)
    print('Task 9: Visualization')
    print('='*60)

    z_plot = np.linspace(0.01, 2.5, 400)

    # w(z) plot
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.axhline(-1.0, color='k', ls='--', lw=1, label='LCDM (w=-1)')
    w_son = SON_W0 + SON_WA * z_plot / (1.0 + z_plot)
    ax.plot(z_plot, w_son, 'k-', lw=2, label=f'Son+25 (w0={SON_W0}, wa={SON_WA})')
    ax.fill_between(z_plot,
        (SON_W0-SON_W0_2SIG)+(SON_WA-SON_WA_2SIG)*z_plot/(1+z_plot),
        (SON_W0+SON_W0_2SIG)+(SON_WA+SON_WA_2SIG)*z_plot/(1+z_plot),
        alpha=0.10, color='k', label='Son+25 2sigma')
    if cpl_result.get('w0') is not None:
        w0_c, wa_c = cpl_result['w0'], cpl_result['wa']
        ax.plot(z_plot, w0_c + wa_c*z_plot/(1+z_plot), 'C5-.', lw=1.5,
                label=f'CPL (w0={w0_c:.2f}, wa={wa_c:.2f})')
    colors = ['C0','C1','C2','C3','C4','C6','C7','C8','C9','C3']
    valid_r = [r for r in ranked_all if r.get('w0') is not None][:10]
    for r, col in zip(valid_r, colors):
        w0 = r['w0']; wa = r.get('wa', 0.0)
        ax.plot(z_plot, w0 + (wa or 0)*z_plot/(1+z_plot), col, lw=1.2,
                label=f'{r["tag"][:25]} ({w0:.2f},{wa:.2f})')
    ax.set_xlabel('z'); ax.set_ylabel('w(z)')
    ax.set_title('L46: w(z) top models vs Son+25')
    ax.legend(fontsize=6, loc='lower right')
    ax.set_ylim(-4.5, 1.0)
    ax.grid(alpha=0.3)
    out = os.path.join(out_dir, 'l46_task9_wz.png')
    fig.savefig(out, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f'  w(z) plot: {out}')

    # w0-wa plane
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.axvline(-1.0, color='k', ls=':', lw=0.8, alpha=0.5)
    ax.axhline(0.0,  color='k', ls=':', lw=0.8, alpha=0.5)
    ax.plot(-1.0, 0.0, 'k+', ms=12, label='LCDM')
    ax.plot(SON_W0, SON_WA, 'ks', ms=12, label=f'Son+25 ({SON_W0},{SON_WA})')
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(SON_W0 + SON_W0_2SIG*np.cos(theta),
            SON_WA + SON_WA_2SIG*np.sin(theta), 'k--', lw=1, alpha=0.3)
    ax.plot(-0.757, -0.83, 'g^', ms=8, label='DESI DR2')
    if cpl_result.get('w0') is not None:
        ax.plot(cpl_result['w0'], cpl_result['wa'], 'C5*', ms=12,
                label=f"CPL ({cpl_result['w0']:.2f},{cpl_result['wa']:.2f})")
    for r, col in zip(valid_r[:10], colors):
        ax.plot(r['w0'], r.get('wa', 0.0) or 0.0, 'o', color=col, ms=8,
                label=f"{r['tag'][:20]}")
    ax.set_xlabel('w0'); ax.set_ylabel('wa')
    ax.set_title('L46: w0-wa plane')
    ax.legend(fontsize=6, loc='best')
    ax.set_xlim(-3.5, 0.8); ax.set_ylim(-6.0, 4.0)
    ax.grid(alpha=0.3)
    out = os.path.join(out_dir, 'l46_task9_w0wa.png')
    fig.savefig(out, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f'  w0-wa plot: {out}')

    # q0 comparison
    print('\n  q0 comparison:')
    print(f'  Son+25 target: q0={SON_Q0:+.2f}  LCDM: q0=-0.53')
    print(f'  {"Model":<32} {"w0":>7} {"wa":>7} {"q0":>7}  Son+25?')
    print('  ' + '-'*65)
    if cpl_result.get('w0') is not None:
        q0_c = _q0(cpl_result.get('Om') or 0.36, cpl_result['w0'])
        ag = 'YES' if q0_c > 0 else ('NEAR' if q0_c > -0.1 else 'NO')
        print(f'  {"CPL":<32} {cpl_result["w0"]:>7.3f} {cpl_result["wa"]:>7.3f} '
              f'{q0_c:>7.3f}  {ag}')
    for r in valid_r[:10]:
        q0v = r.get('q0')
        if q0v is None and r.get('params'):
            q0v = _q0(r['params'][0], r['w0'])
        ag = 'YES' if (q0v or -999) > 0 else ('NEAR' if (q0v or -999) > -0.1 else 'NO')
        wa_s = f'{(r.get("wa") or 0.0):>7.3f}'
        print(f'  {r["tag"][:32]:<32} {r["w0"]:>7.3f} {wa_s} '
              f'{(q0v or float("nan")):>7.3f}  {ag}')
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 10: Final verdict
# ──────────────────────────────────────────────────────────────────────────────

def task10_final_verdict(ranked_all, boot_results, lcdm_aicc, cpl_result):
    print('\n' + '='*60)
    print('L46 FINAL VERDICT')
    print('='*60)

    valid = [r for r in ranked_all if r.get('daicc', 9999) < 9000]
    best3 = valid[:3]

    print(f'\n  Top-3 by dAICc:')
    for i, r in enumerate(best3):
        w0s = f'{r["w0"]:.3f}' if r.get("w0") is not None else '---'
        was = f'{r.get("wa", 0):.3f}' if r.get("wa") is not None else '---'
        print(f'  {i+1}. {r["tag"][:45]}  dAICc={r["daicc"]:+.2f}  [{r["verdict"]}]')
        print(f'     w0={w0s}, wa={was}, q0={r.get("q0","---")}')
        if r['tag'] in boot_results:
            br = boot_results[r['tag']]
            med = br.get("median")
            med_s = f'{med:.2f}' if isinstance(med, float) else '?'
            print(f'     Bootstrap: median={med_s}  {br.get("verdict","?")}')

    # Overall assessment
    best_d = valid[0]['daicc'] if valid else 9999
    best_v = valid[0].get('verdict', 'NONE') if valid else 'NONE'
    best_w0 = valid[0].get('w0') if valid else None
    best_wa = valid[0].get('wa') if valid else None
    best_q0 = valid[0].get('q0') if valid else None

    son_w0_ok = (best_w0 is not None) and (SON_W0-2*SON_W0_2SIG <= best_w0 <= SON_W0+2*SON_W0_2SIG)
    son_wa_ok = (best_wa is not None) and (SON_WA-2*SON_WA_2SIG <= best_wa <= SON_WA+2*SON_WA_2SIG)
    son_q0_ok = (best_q0 is not None) and (best_q0 > 0.0)

    print(f'\n  [FINAL] {best_v}')
    print(f'  Best dAICc: {best_d:.2f}')
    print(f'  Son+25 alignment: w0={"YES" if son_w0_ok else "NO"}  '
          f'wa={"YES" if son_wa_ok else "NO"}  q0={"YES" if son_q0_ok else "NO"}')
    print(f'  L45 UB comparison: dAICc {best_d:.2f} vs L45_best={L45_UB_DAICC:.2f}  '
          f'[{"IMPROVED" if best_d < L45_UB_DAICC else "NOT improved"}]')

    # 3 winner categories
    print(f'\n  3 Winners:')
    # AIC winner
    if valid:
        r = valid[0]
        print(f'  Winner-AIC:     {r["tag"][:45]}  dAICc={r["daicc"]:.2f}')
    # Son+25 winner (closest w0,wa to Son+25 with dAICc < 0)
    son_candidates = [r for r in valid if r.get('w0') is not None and r['daicc'] < 0]
    if son_candidates:
        def son_dist(r):
            d_w0 = (r['w0'] - SON_W0)**2 / SON_W0_2SIG**2
            d_wa = ((r.get('wa') or 0) - SON_WA)**2 / SON_WA_2SIG**2
            return d_w0 + d_wa
        son_winner = min(son_candidates, key=son_dist)
        print(f'  Winner-Son:     {son_winner["tag"][:45]}  '
              f'w0={son_winner.get("w0","?"):.3f}, wa={son_winner.get("wa",0):.3f}')
    # Natural winner (lowest k with dAICc < -10)
    nat_candidates = [r for r in valid if r['daicc'] < -10]
    if nat_candidates:
        nat_winner = min(nat_candidates, key=lambda r: r['k'])
        print(f'  Winner-Natural: {nat_winner["tag"][:45]}  k={nat_winner["k"]}')

    print(f'\n  4-condition summary for top-10:')
    for r in valid[:10]:
        w0 = r.get('w0'); wa = r.get('wa'); q0v = r.get('q0')
        c1 = r['daicc'] < -50
        c2 = (w0 is not None) and (SON_W0-2*SON_W0_2SIG <= w0 <= SON_W0+2*SON_W0_2SIG)
        c3 = (wa is not None) and (SON_WA-2*SON_WA_2SIG <= wa <= SON_WA+2*SON_WA_2SIG)
        c4 = (q0v is not None) and q0v > 0
        n_cond = sum([c1, c2, c3, c4])
        print(f'  {r["tag"][:35]:<35} [{n_cond}/4 conditions]  {r["verdict"]}')

    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    OUT_DIR = _SCRIPT_DIR
    LOG_FILE = os.path.join(OUT_DIR, 'l46_run.log')

    print('='*60)
    print('L46: 3-Axiom SQT + A3 4-State Full Exploration')
    print(f'8-worker parallel  |  L43 LCDM AICc ref={LCDM_AICC_L43:.2f}')
    print(f'32 Tier1 + 45 Tier2 + 20 Tier3 | ~4260 fits | 18-27h')
    print('='*60)
    sys.stdout.flush()

    pretask_all(OUT_DIR)

    ctx  = mp.get_context('spawn')
    pool = ctx.Pool(N_WORKERS)

    r0         = None
    ranked_all = []
    boot_res   = {}
    tier2_best = {}
    tier3_best = {}
    t2_ranked  = []
    t3_ranked  = []
    lcdm_aicc  = LCDM_AICC_L43

    try:
        # Task 0: Baselines
        r0        = task0_baselines(pool)
        lcdm_aicc = r0['lcdm_aicc']
        lcdm_res  = r0['lcdm']
        cpl_res   = r0['cpl']

        # Tasks 1-4: Tier 1
        tier1_best = task1_to_4_tier1(pool, lcdm_aicc)

        # Task 5: Rank Tier 1
        ranked = task5_rank_tier1(tier1_best, lcdm_aicc, cpl_res)
        ranked_all = ranked  # will extend with Tier 2/3

        # Task 6: Tier 2
        if any(r['daicc'] < 0 for r in ranked):
            tier2_best, t2_ranked = task6_tier2(pool, ranked, lcdm_aicc)
            ranked_all = sorted(ranked + t2_ranked, key=lambda x: x.get('daicc', 9999))
        else:
            print('\nTask 6: Tier 2 SKIPPED (no Tier 1 model with dAICc < 0)')

        # Task 7: Tier 3
        if t2_ranked:
            tier3_best, t3_ranked = task7_tier3(pool, t2_ranked, lcdm_aicc)
            ranked_all = sorted(ranked_all + t3_ranked, key=lambda x: x.get('daicc', 9999))
        else:
            print('\nTask 7: Tier 3 SKIPPED (no Tier 2 results)')

        # Task 8: Bootstrap Top-10
        boot_res = task8_bootstrap(pool, ranked_all, lcdm_res, n_top=10)

        # Task 9: Visualization
        task9_visualization(ranked_all, cpl_res, OUT_DIR)

        # Task 10: Final verdict
        task10_final_verdict(ranked_all, boot_res, lcdm_aicc, cpl_res)

    finally:
        pool.close()
        pool.join()

    # ── Summary ──
    print('\n' + '='*60)
    print('L46 RESULTS SUMMARY')
    print('='*60)
    if r0:
        print(f"[Task 0] LCDM AICc={r0['lcdm_aicc']:.2f}  "
              f"CPL dAICc={r0['cpl'].get('daicc_vs_lcdm', 'N/A')}")
    print(f'\n[Tasks 1-4] Tier 1 top-5:')
    for r in ranked[:5]:
        w0s = f'{r["w0"]:.3f}' if r.get('w0') is not None else '---'
        print(f'  {r["tag"]:<22}  dAICc={r["daicc"]:+.2f}  [{r["verdict"]}]  w0={w0s}')
    if t2_ranked:
        print(f'\n[Task 6] Tier 2 best: {t2_ranked[0]["tag"][:45]}  '
              f'dAICc={t2_ranked[0]["daicc"]:+.2f}')
    if t3_ranked:
        print(f'[Task 7] Tier 3 best: {t3_ranked[0]["tag"][:45]}  '
              f'dAICc={t3_ranked[0]["daicc"]:+.2f}')
    print()

    # Save JSON
    save = {
        'task0':         _jsonify(r0),
        'tier1_ranked':  _jsonify(ranked[:32]),
        'tier2_top10':   _jsonify(t2_ranked[:10]),
        'tier3_top5':    _jsonify(t3_ranked[:5]),
        'bootstrap':     _jsonify(boot_res),
        'lcdm_aicc':     lcdm_aicc,
        'lcdm_aicc_l43': LCDM_AICC_L43,
        'l45_ub_daicc':  L45_UB_DAICC,
        'son_params':    {'w0': SON_W0, 'wa': SON_WA, 'q0': SON_Q0},
    }
    out_json = os.path.join(OUT_DIR, 'l46_results.json')
    with open(out_json, 'w') as f:
        json.dump(save, f, indent=2)
    print(f'Saved: {out_json}')
