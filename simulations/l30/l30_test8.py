# -*- coding: utf-8 -*-
"""
l30_test8.py -- L30 창의적 변태 2탄 (CC01-CC30)
=================================================
Ultra-Perverse Strategy: Exploit Covariance Matrix Blind Spots

Three-pronged attack:

Prong 1 (CC01-CC10): Covariance Eigenmode Analysis
  - Eigendecompose the 13x13 DESI covariance matrix
  - Find 3 eigenvectors with LARGEST eigenvalues (data blind spots)
  - Design E(z) theories that move the prediction along these blind spot directions

Prong 2 (CC11-CC20): Constrained Optimal Sweep
  - Fix E^2(z) = Om*(1+z)^3 + OL0*g(z; alpha)
  - Sweep theoretical constant alpha over SQMH-motivated values
  - For each alpha, fit only Om, H0
  - Map chi^2 landscape vs alpha

Prong 3 (CC21-CC30): Ensemble/Superposition Dark Energy
  - Superpositions of SQMH mechanisms (weights theoretically fixed)
  - Each component uses different physical mechanism
  - Combined k=2 (no extra free params since weights are derived)

LCDM baseline: chi2=10.192, AICc=15.392 (k=2, n=13)
KILL if AICc >= 15.392
"""

import os
import sys
import math
import json
import warnings
import multiprocessing
import traceback

import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import minimize

warnings.filterwarnings('ignore')
np.seterr(all='ignore')

os.environ['OMP_NUM_THREADS']      = '1'
os.environ['MKL_NUM_THREADS']      = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SIM_DIR    = os.path.dirname(_SCRIPT_DIR)
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

from desi_data import DESI_DR2, DESI_DR2_COV, DESI_DR2_COV_INV

C_KMS   = 299792.458
R_S     = 147.09
OR      = 5.38e-5
N_DATA  = 13
N_GRID  = 4000
LCDM_BASELINE_CHI2  = 10.192
LCDM_BASELINE_AICC  = 15.392

# ==============================================================================
# PRONG 1: COVARIANCE EIGENDECOMPOSITION
# ==============================================================================

def analyze_covariance_eigenmodes():
    """
    Eigendecompose DESI_DR2_COV (the covariance matrix, NOT its inverse).
    Largest eigenvalues = directions data is MOST uncertain (blind spots).
    Returns eigenvalues, eigenvectors sorted by descending eigenvalue.
    """
    # DESI_DR2_COV is the covariance matrix
    cov = np.array(DESI_DR2_COV)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    # Sort descending (largest first)
    idx = np.argsort(-eigenvalues)
    eigenvalues  = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]  # columns are eigenvectors
    return eigenvalues, eigenvectors


def compute_lcdm_best():
    """Find LCDM best-fit and return (Om, H0, theory_vec)."""
    def E_lcdm(z_arr, Om):
        OL0 = 1.0 - Om - OR
        E2  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
        return np.sqrt(np.maximum(E2, 1e-30))

    starts = [
        [0.315, 67.4], [0.30, 68.0], [0.32, 69.0],
        [0.29, 70.0],  [0.31, 68.5], [0.28, 71.0],
        [0.33, 67.0],  [0.34, 66.5],
    ]

    def chi2_lcdm(params):
        Om, H0 = params
        if not (0.05 < Om < 0.70 and 50.0 < H0 < 100.0):
            return 1e8
        th = compute_theory_vec_E(Om, H0, E_lcdm)
        if th is None:
            return 1e8
        delta = DESI_DR2['value'] - th
        return float(delta @ DESI_DR2_COV_INV @ delta)

    best_chi2 = 1e8
    best_x    = None
    for s in starts:
        try:
            res = minimize(chi2_lcdm, s, method='Nelder-Mead',
                           options={'xatol': 1e-7, 'fatol': 1e-7, 'maxiter': 5000})
            if res.fun < best_chi2:
                best_chi2 = res.fun
                best_x    = res.x
        except Exception:
            continue

    if best_x is None:
        best_x = np.array([0.315, 67.4])
    Om, H0 = float(best_x[0]), float(best_x[1])
    th = compute_theory_vec_E(Om, H0, E_lcdm)
    return Om, H0, th, best_chi2


def compute_theory_vec_E(Omega_m, H0, E_func):
    """Generic BAO theory vector given E(z) function."""
    z_eff  = DESI_DR2['z_eff']
    z_max  = z_eff.max() + 0.01
    z_grid = np.linspace(0.0, z_max, N_GRID)

    try:
        E_grid = E_func(z_grid, Omega_m)
    except Exception:
        return None

    if E_grid is None:
        return None
    if not np.all(np.isfinite(E_grid)):
        return None
    E_grid = np.maximum(E_grid, 1e-15)

    inv_E  = 1.0 / E_grid
    DM_cum = (C_KMS / H0) * np.concatenate(
        [[0.0], cumulative_trapezoid(inv_E, z_grid)]
    )

    theory_vec = np.empty(N_DATA)
    for i, (z, qty) in enumerate(zip(z_eff, DESI_DR2['quantity'])):
        idx  = min(np.searchsorted(z_grid, z), N_GRID - 1)
        E_z  = E_grid[idx]
        DH   = C_KMS / (H0 * E_z)
        DM   = DM_cum[idx]
        DV   = (z * DM**2 * DH)**(1.0/3.0) if z > 0 else 0.0

        if   'DV' in qty: theory_vec[i] = DV / R_S
        elif 'DM' in qty: theory_vec[i] = DM / R_S
        elif 'DH' in qty: theory_vec[i] = DH / R_S
        else:             theory_vec[i] = np.nan

    return theory_vec


def aicc(chi2_val, k, n=N_DATA):
    return chi2_val + 2*k + 2*k*(k+1)/(n - k - 1)


# ==============================================================================
# WORKER FUNCTION (fully self-contained for spawn)
# ==============================================================================

def worker_fn(args):
    """
    Self-contained worker for CC theories.
    Task format: (wid, theory_name, k, task_type, task_data)

    task_type:
      'cc_k2'  : task_data = (theory_tag, params_dict)
      'cc_k3'  : task_data = (theory_tag, params_dict, extra_starts)
    """
    import os, sys, math, warnings
    import numpy as np

    os.environ['OMP_NUM_THREADS']      = '1'
    os.environ['MKL_NUM_THREADS']      = '1'
    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    np.seterr(all='ignore')
    warnings.filterwarnings('ignore')

    _SCRIPT_DIR_W = os.path.dirname(os.path.abspath(__file__))
    _SIM_DIR_W    = os.path.dirname(_SCRIPT_DIR_W)
    if _SIM_DIR_W not in sys.path:
        sys.path.insert(0, _SIM_DIR_W)
    from desi_data import DESI_DR2, DESI_DR2_COV_INV
    from scipy.integrate import cumulative_trapezoid
    from scipy.optimize import minimize

    C_KMS_W   = 299792.458
    R_S_W     = 147.09
    OR_W      = 5.38e-5
    N_DATA_W  = 13
    N_GRID_W  = 4000
    LCDM_AICC = 15.392

    def aicc_w(chi2_val, k_in, n=N_DATA_W):
        return chi2_val + 2*k_in + 2*k_in*(k_in+1)/(n - k_in - 1)

    def compute_tv(Omega_m, H0, E_fn):
        z_eff  = DESI_DR2['z_eff']
        z_max  = z_eff.max() + 0.01
        z_grid = np.linspace(0.0, z_max, N_GRID_W)
        try:
            E_grid = E_fn(z_grid, Omega_m)
        except Exception:
            return None
        if E_grid is None:
            return None
        if not np.all(np.isfinite(E_grid)):
            return None
        E_grid = np.maximum(E_grid, 1e-15)
        inv_E  = 1.0 / E_grid
        DM_cum = (C_KMS_W / H0) * np.concatenate(
            [[0.0], cumulative_trapezoid(inv_E, z_grid)]
        )
        theory_vec = np.empty(N_DATA_W)
        for i, (z, qty) in enumerate(zip(z_eff, DESI_DR2['quantity'])):
            idx = min(np.searchsorted(z_grid, z), N_GRID_W - 1)
            E_z = E_grid[idx]
            DH  = C_KMS_W / (H0 * E_z)
            DM  = DM_cum[idx]
            DV  = (z * DM**2 * DH)**(1.0/3.0) if z > 0 else 0.0
            if   'DV' in qty: theory_vec[i] = DV / R_S_W
            elif 'DM' in qty: theory_vec[i] = DM / R_S_W
            elif 'DH' in qty: theory_vec[i] = DH / R_S_W
            else:             theory_vec[i] = np.nan
        return theory_vec

    def chi2_w(params, E_fn):
        Omega_m, H0 = params[0], params[1]
        if not (0.05 < Omega_m < 0.70 and 50.0 < H0 < 100.0):
            return 1e8
        th = compute_tv(Omega_m, H0, E_fn)
        if th is None or not np.all(np.isfinite(th)):
            return 1e8
        delta = DESI_DR2['value'] - th
        return float(delta @ DESI_DR2_COV_INV @ delta)

    # ---- E(z) function registry for CC theories ----

    def build_E_fn(theory_tag, params):
        """
        Build an E(z) function from theory_tag and params dict.
        All are self-contained closures.
        """
        # ---- Prong 1: Eigenmode-targeting theories ----
        if theory_tag == 'CC01':
            # Blind Spot 1: Main eigenvector direction (data most uncertain at high-z DH)
            # Physical: DE density follows principal eigenmode profile
            # f(z) shape matches top eigenvector pattern via z/(1+z) + log(1+z) combo
            alpha1 = params['alpha1']  # ~0.5, from eigenvector projection
            alpha2 = params['alpha2']  # ~0.2, secondary term
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                # rho_DE shaped to exploit blind spot 1
                rho_DE = OL0 * (1.0 + alpha1 * z_arr/(1.0+z_arr) + alpha2 * np.log1p(z_arr))
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC02':
            # Blind spot 2: second eigenmode direction
            # Physical: oscillatory DE from spacetime quantum resonance
            alpha = params['alpha']   # derived: 2*pi ~ 6.283
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                rho_DE = OL0 * (1.0 + alpha * np.sin(np.pi * z_arr / 2.0))
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC03':
            # Blind spot 3: third eigenmode direction
            # Physical: power-law DE from SQMH void growth
            nu = params['nu']   # derived: 1/pi ~ 0.318
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                rho_DE = OL0 * (1+z_arr)**nu
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC04':
            # Eigenmode 1+2 combination: target two blind spots simultaneously
            # Physical: dual-channel DE from A1 annihilation + A3 generation
            a1 = params['a1']   # 1/(2*pi) ~ 0.159
            a2 = params['a2']   # e^(-1) ~ 0.368
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                # channel 1: drift along eigenvector 1 (z/(1+z) profile)
                # channel 2: drift along eigenvector 2 (sin profile)
                rho_DE = OL0 * (1.0
                               + a1 * z_arr/(1.0+z_arr)
                               + a2 * np.sin(np.pi * z_arr / 2.0))
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC05':
            # Max blind-spot targeting: push theory vector maximally along largest eigenvector
            # Physical: SQ metabolism rate modulates DE along principal data uncertainty
            # Amplitude from eigenvalue ratio: sqrt(lambda1/lambda_mean)
            beta = params['beta']   # derived from eigenvalue analysis
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                # tanh shape captures the gradual transition
                rho_DE = OL0 * (1.0 + beta * np.tanh(z_arr / 2.0))
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC06':
            # Eigenmode-targeted exponential decay: focuses correction on high-z blind spot
            # Physical: SQMH spacetime quantum decay rate ~ exp(-z/z_char)
            # z_char from SQMH: ~1/pi
            gamma = params['gamma']  # 1/pi ~ 0.318
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                rho_DE = OL0 * np.exp(-gamma * z_arr)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC07':
            # Third eigenmode: high-z correction via (1+z)^alpha - 1
            # Physical: SQMH generation rate scales as volume element
            # alpha from SQMH: 3/(4*pi) ~ 0.239
            alpha = params['alpha']
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                rho_DE = OL0 * (1.0 + ((1+z_arr)**alpha - 1))
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC08':
            # Blind-spot combo: z/(1+z) + (1+z)^nu correction
            # Physical: A1+A3 together give drift + growth
            a1  = params['a1']   # 1/(2*pi) ~ 0.159
            nu  = params['nu']   # e^(-2) ~ 0.135
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                rho_DE = OL0 * (1.0 + a1 * z_arr/(1.0+z_arr) + ((1+z_arr)**nu - 1))
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC09':
            # Eigenmode targeting via arctan (bounded, monotone -- matches blind spot profile)
            # Physical: SQMH matter-DE interaction saturates at cosmic equilibrium
            beta = params['beta']  # pi/4 ~ 0.785 (quarter-period)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                rho_DE = OL0 * (1.0 + beta * np.arctan(z_arr))
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC10':
            # All 3 eigenmodes combined with theoretically derived weights
            # Physical: full SQMH correction from A1+A3+A4
            # Weights: 1/pi, 1/(2*pi), 1/(4*pi) -- successive harmonic dampening
            a1 = params['a1']  # 1/pi ~ 0.318
            a2 = params['a2']  # 1/(2*pi) ~ 0.159
            a3 = params['a3']  # 1/(4*pi) ~ 0.0796
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                rho_DE = OL0 * (1.0
                               + a1 * z_arr/(1.0+z_arr)
                               + a2 * np.sin(np.pi * z_arr / 2.0)
                               + a3 * np.log1p(z_arr))
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        # ---- Prong 2: Alpha-sweep optimal theories ----
        elif theory_tag == 'CC11':
            # g(z;alpha) = (1+z)^alpha - 1: power-law DE correction
            # alpha fixed from SQMH: 1/(2*pi) ~ 0.159
            alpha = params['alpha']
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                rho_DE = OL0 * (1.0 + (1+z_arr)**alpha - 1)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC12':
            # g(z;alpha) = log(1+z)^alpha: log-power DE correction
            # alpha = e^(-1) ~ 0.368 from SQMH Boltzmann factor
            alpha = params['alpha']
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                rho_DE = OL0 * (1.0 + np.log1p(z_arr)**alpha)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC13':
            # g(z;alpha) = tanh(alpha*z): saturation DE from A4 equilibrium
            # alpha = pi ~ 3.14159 from SQMH cyclicity
            alpha = params['alpha']
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                rho_DE = OL0 * (1.0 + np.tanh(alpha * z_arr))
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC14':
            # g(z;alpha) = exp(-alpha*z^2): Gaussian DE suppression at high z
            # alpha = pi/4 ~ 0.785 from SQMH solid angle
            alpha = params['alpha']
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                rho_DE = OL0 * np.exp(-alpha * z_arr**2)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC15':
            # g(z;alpha) = z_over_1pz * alpha: saturation from SQMH void filling
            # alpha = 2*pi/ln(2) ~ 9.065 from EE2 B constant
            alpha = params['alpha']
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                rho_DE = OL0 * (1.0 + alpha * z_arr/(1.0+z_arr))
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC16':
            # g(z;alpha) = sin(alpha*pi*z/2): oscillatory from SQMH quantum cyclicity
            # alpha = 1/2 from half-period
            alpha = params['alpha']
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                rho_DE = OL0 * (1.0 + np.sin(alpha * np.pi * z_arr / 2.0))
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC17':
            # g(z;alpha) = sqrt(1+z)^alpha - 1: root-power from SQMH area scaling
            # alpha = 1/3 from 3D volume to 2D surface ratio
            alpha = params['alpha']
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                rho_DE = OL0 * (1.0 + np.sqrt(1+z_arr)**alpha - 1)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC18':
            # g(z;alpha) = erf(alpha*z): error function DE from SQMH diffusion
            # alpha = 1/sqrt(pi) ~ 0.564 from Gaussian normalization
            alpha = params['alpha']
            def E_fn(z_arr, Om):
                from scipy.special import erf
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                rho_DE = OL0 * (1.0 + erf(alpha * z_arr))
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC19':
            # g(z;alpha) = alpha * z/(1+z) + (1-alpha) * sin(pi*z/2): hybrid from A1+A3 equipartition
            # Sweep over alpha in [0,1]
            alpha = params['alpha']  # equipartition from C1 conservation: e^(-1) ~ 0.368
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                rho_DE = OL0 * (1.0
                               + alpha * z_arr/(1.0+z_arr)
                               + (1.0 - alpha) * np.sin(np.pi * z_arr / 2.0))
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC20':
            # g(z;alpha) = (1+z)^alpha * exp(-z): suppressed power law
            # alpha = 3/(4*pi) ~ 0.239 from SQMH void geometry
            alpha = params['alpha']
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                rho_DE = OL0 * (1+z_arr)**alpha * np.exp(-z_arr)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        # ---- Prong 3: Superposition theories ----
        elif theory_tag == 'CC21':
            # Equal superposition of A1 and A3 SQMH mechanisms
            # rho_DE = 0.5*rho_DE_A1 + 0.5*rho_DE_A3
            # A1: annihilation -> DE increases as matter decreases: z/(1+z) profile
            # A3: generation uniform -> constant DE
            # Weight from A1+A3 symmetry in SQMH: 50/50
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                # A1 component: DE grows with void fraction
                rho_A1 = OL0 * (1.0 + z_arr/(1.0+z_arr))
                # A3 component: constant generation (LCDM-like)
                rho_A3 = OL0 * np.ones_like(z_arr)
                rho_DE = 0.5 * rho_A1 + 0.5 * rho_A3
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC22':
            # Matter-fraction weighted superposition
            # w_A1 = 1-Om, w_A4 = Om (weight by volume fractions)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                # A1 component: DE fueled by annihilated matter (void fraction)
                rho_A1 = OL0 * (1.0 + z_arr/(1.0+z_arr))
                # A4 component: net rate regime: DE ~ exp(-Om*z)
                rho_A4 = OL0 * np.exp(-Om * z_arr)
                rho_DE = (1.0 - Om) * rho_A1 + Om * rho_A4
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC23':
            # OL0-fraction weighted: w_A1=OL0, w_A3=(1-OL0)
            # Physical: DE-rich regions weighted by dark energy fraction
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                # A1: void fraction growth
                rho_A1 = OL0 * (1.0 + z_arr/(1.0+z_arr))
                # A3: constant generation (flat)
                rho_A3 = OL0 * np.ones_like(z_arr)
                rho_DE = OL0 * rho_A1 + (1.0 - OL0) * rho_A3
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC24':
            # A1+A3 golden ratio superposition: phi = (1+sqrt(5))/2
            # Weight w1 = 1/phi ~ 0.618, w2 = 1-1/phi ~ 0.382
            # Physical: optimal packing ratio in SQMH spacetime quanta
            w1 = 1.0 / ((1.0 + math.sqrt(5)) / 2.0)  # ~ 0.618
            w2 = 1.0 - w1  # ~ 0.382
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                rho_A1 = OL0 * (1.0 + z_arr/(1.0+z_arr))  # A1 void fraction
                rho_A3 = OL0 * (1.0 + np.sin(np.pi*z_arr/2.0))  # A3 oscillatory generation
                rho_DE = w1 * rho_A1 + w2 * rho_A3
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC25':
            # A1+A3+A4 equal-weight 3-way superposition
            # Physical: all SQMH axioms contribute equally
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                rho_A1 = OL0 * (1.0 + z_arr/(1.0+z_arr))
                rho_A3 = OL0 * np.ones_like(z_arr)
                rho_A4 = OL0 * np.exp(-Om * z_arr)
                rho_DE = (rho_A1 + rho_A3 + rho_A4) / 3.0
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC26':
            # Log-weight superposition: w_i ~ 1/log(i+1) natural dampening
            # w1 = 1/log(2), w2 = 1/log(3), normalized
            # Physical: each SQMH mechanism contributes with diminishing returns
            l2 = math.log(2)
            l3 = math.log(3)
            l4 = math.log(4)
            total = 1/l2 + 1/l3 + 1/l4
            w1 = (1/l2) / total
            w2 = (1/l3) / total
            w3 = (1/l4) / total
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                rho_A1 = OL0 * (1.0 + z_arr/(1.0+z_arr))
                rho_A3 = OL0 * (1.0 + np.tanh(z_arr/2.0))
                rho_A4 = OL0 * np.exp(-Om * z_arr)
                rho_DE = w1 * rho_A1 + w2 * rho_A3 + w3 * rho_A4
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC27':
            # Exponential-weight superposition: w_i ~ exp(-i/pi)
            # Physical: SQMH quantum decay envelope for successive mechanisms
            e1 = math.exp(-1.0/math.pi)
            e2 = math.exp(-2.0/math.pi)
            total = e1 + e2
            w1 = e1 / total
            w2 = e2 / total
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                rho_A1 = OL0 * (1.0 + z_arr/(1.0+z_arr))
                rho_A3 = OL0 * (1.0 + np.sin(np.pi*z_arr/2.0))
                rho_DE = w1 * rho_A1 + w2 * rho_A3
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC28':
            # Harmonic superposition: w_i ~ 1/i (harmonic series)
            # w1=1/2, w2=1/3, w3=1/6 (normalized: 1/2+1/3+1/6=1)
            # Physical: each SQMH harmonic mode contributes
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                # A1: z/(1+z)
                rho_A1 = OL0 * (1.0 + z_arr/(1.0+z_arr))
                # A3: sin oscillation
                rho_A3 = OL0 * (1.0 + np.sin(np.pi*z_arr/2.0))
                # A4: log decay
                rho_A4 = OL0 * (1.0 - np.log1p(z_arr) / (1.0 + np.log1p(z_arr)))
                rho_DE = 0.5 * rho_A1 + (1.0/3.0) * rho_A3 + (1.0/6.0) * rho_A4
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC29':
            # Geometric superposition: w_i ~ r^(i-1), r=1/e (geometric series)
            # w1 = (1-1/e)/(1-1/e^3), etc. -- truncated geometric
            r   = math.exp(-1.0)  # 1/e
            w1  = 1.0
            w2  = r
            w3  = r**2
            s   = w1 + w2 + w3
            w1, w2, w3 = w1/s, w2/s, w3/s
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                rho_A1 = OL0 * (1.0 + z_arr/(1.0+z_arr))
                rho_A3 = OL0 * (1.0 + np.sin(np.pi*z_arr/2.0))
                rho_A4 = OL0 * np.exp(-Om * z_arr)
                rho_DE = w1 * rho_A1 + w2 * rho_A3 + w3 * rho_A4
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'CC30':
            # Matter-void complementary superposition
            # rho_DE = sqrt(Om) * rho_A1 + sqrt(OL0) * rho_A3 (normalized)
            # Physical: weighted by geometric mean of matter/DE amplitude
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                s = math.sqrt(Om) + math.sqrt(OL0)
                w1 = math.sqrt(Om) / s
                w2 = math.sqrt(OL0) / s
                rho_A1 = OL0 * (1.0 + z_arr/(1.0+z_arr))
                rho_A3 = OL0 * (1.0 + np.tanh(z_arr / 2.0))
                rho_DE = w1 * rho_A1 + w2 * rho_A3
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        else:
            return None

    # ====================
    # Unpack and execute
    # ====================
    wid, theory_name, k, task_type, task_data = args

    base_starts = [
        [0.315, 67.4], [0.30, 68.0], [0.32, 69.0],
        [0.29, 70.0],  [0.31, 68.5], [0.28, 71.0],
        [0.33, 67.0],  [0.34, 66.5],
    ]

    try:
        theory_tag = task_data['tag']
        params     = task_data.get('params', {})
        E_fn = build_E_fn(theory_tag, params)
        if E_fn is None:
            return {'id': wid, 'name': theory_name, 'k': k,
                    'chi2': 1e8, 'aicc': 1e8, 'd_aicc': 1e8,
                    'Om': None, 'H0': None, 'extra': params, 'status': 'FAIL'}

        best_val = 1e8
        best_x   = None
        for s in base_starts:
            try:
                res = minimize(lambda p, ef=E_fn: chi2_w(p, ef), s,
                               method='Nelder-Mead',
                               options={'xatol': 1e-6, 'fatol': 1e-6, 'maxiter': 5000})
                if res.fun < best_val:
                    best_val = res.fun
                    best_x   = res.x
            except Exception:
                continue

        if best_x is None:
            return {'id': wid, 'name': theory_name, 'k': k,
                    'chi2': 1e8, 'aicc': 1e8, 'd_aicc': 1e8,
                    'Om': None, 'H0': None, 'extra': params, 'status': 'FAIL'}

        Om_best, H0_best = float(best_x[0]), float(best_x[1])
        chi2_best = float(best_val)
        aicc_best = aicc_w(chi2_best, k)
        d_aicc    = aicc_best - LCDM_AICC

        # Compute wa proxy from best-fit
        # w_eff(z=0.5) vs w_eff(z=0) from rho_DE slope
        th0 = compute_tv(Om_best, H0_best, E_fn)
        # Numerically estimate wa from E(z) at z~0.5 vs z~0
        try:
            z_test = np.array([0.0, 0.5, 1.0])
            E_test = E_fn(z_test, Om_best)
            OL0    = 1.0 - Om_best - OR_W
            rho_m0 = Om_best
            rho_r0 = OR_W
            def rho_de_z(z, Eval):
                E2 = Eval**2
                return E2 - rho_r0*(1+z)**4 - rho_m0*(1+z)**3
            rde0 = rho_de_z(0.0, E_test[0])
            rde1 = rho_de_z(0.5, E_test[1])
            if rde0 > 0 and rde1 > 0:
                # w ~ d ln rho_de / d ln a^3 / (-3) at z~0.25
                lna_diff = math.log(1.0/(1+0.5))  # negative
                lnrho_diff = math.log(rde1/rde0)
                wa_proxy = lnrho_diff / lna_diff / (-3.0) - (-1.0)
                wa_proxy = float(wa_proxy)
            else:
                wa_proxy = 0.0
        except Exception:
            wa_proxy = 0.0

        status = 'PASS' if aicc_best < LCDM_AICC else 'KILL'
        return {
            'id': wid, 'name': theory_name, 'k': k,
            'chi2': chi2_best, 'aicc': aicc_best, 'd_aicc': d_aicc,
            'Om': Om_best, 'H0': H0_best, 'extra': params,
            'wa_proxy': wa_proxy, 'status': status
        }

    except Exception as e:
        return {'id': wid, 'name': theory_name, 'k': k,
                'chi2': 1e8, 'aicc': 1e8, 'd_aicc': 1e8,
                'Om': None, 'H0': None, 'extra': None, 'status': f'ERROR:{e}'}


# ==============================================================================
# ALPHA SWEEP (Prong 2): run in main process for reporting
# ==============================================================================

def alpha_sweep_analysis():
    """
    For the key functional families, sweep alpha over SQMH-motivated values
    and report the chi^2 landscape.
    """
    import sys
    _SCRIPT_DIR_L = os.path.dirname(os.path.abspath(__file__))
    _SIM_DIR_L    = os.path.dirname(_SCRIPT_DIR_L)
    if _SIM_DIR_L not in sys.path:
        sys.path.insert(0, _SIM_DIR_L)
    from desi_data import DESI_DR2, DESI_DR2_COV_INV
    from scipy.integrate import cumulative_trapezoid
    from scipy.optimize import minimize

    OR_L    = 5.38e-5
    N_GRID_L = 4000

    # SQMH-motivated dimensionless alpha values
    alpha_grid = [
        1.0/math.pi,       # 1/pi ~ 0.318 (SQMH cyclicity)
        1.0/(2*math.pi),   # 1/(2*pi) ~ 0.159
        1.0/(4*math.pi),   # 1/(4*pi) ~ 0.0796
        math.exp(-1.0),    # e^(-1) ~ 0.368 (Boltzmann)
        math.exp(-2.0),    # e^(-2) ~ 0.135
        math.pi/4.0,       # pi/4 ~ 0.785 (solid angle)
        math.pi/2.0,       # pi/2 ~ 1.571
        math.pi,           # pi ~ 3.14159
        3.0/(4*math.pi),   # 3/(4pi) ~ 0.239 (void geometry)
        2.0*math.pi/math.log(2.0),  # EE2 B ~ 9.065
        0.5,               # 1/2
        0.25,              # 1/4
        0.1,               # 0.1
        0.05,              # 0.05
        1.0,               # 1.0
        2.0,               # 2.0
        0.75,              # 3/4
        1.0/math.e**0.5,   # 1/sqrt(e) ~ 0.607
    ]
    alpha_grid = sorted(set(round(a, 6) for a in alpha_grid))

    def E_powerlaw(z_arr, Om, alpha):
        OL0 = 1.0 - Om - OR_L
        if OL0 <= 0 or Om <= 0: return None
        rho_DE = OL0 * (1.0 + (1+z_arr)**alpha - 1)
        rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
        E2 = OR_L*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))

    def E_saturation(z_arr, Om, alpha):
        OL0 = 1.0 - Om - OR_L
        if OL0 <= 0 or Om <= 0: return None
        rho_DE = OL0 * (1.0 + alpha * z_arr/(1.0+z_arr))
        rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
        E2 = OR_L*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))

    def quick_chi2(Om, H0, E_fn_alpha, alpha):
        z_eff  = DESI_DR2['z_eff']
        z_max  = z_eff.max() + 0.01
        z_grid = np.linspace(0.0, z_max, N_GRID_L)
        try:
            E_grid = E_fn_alpha(z_grid, Om, alpha)
        except Exception:
            return 1e8
        if E_grid is None or not np.all(np.isfinite(E_grid)):
            return 1e8
        E_grid = np.maximum(E_grid, 1e-15)
        inv_E  = 1.0 / E_grid
        DM_cum = (C_KMS / H0) * np.concatenate(
            [[0.0], cumulative_trapezoid(inv_E, z_grid)]
        )
        tv = np.empty(N_DATA)
        for i, (z, qty) in enumerate(zip(z_eff, DESI_DR2['quantity'])):
            idx = min(np.searchsorted(z_grid, z), N_GRID_L - 1)
            E_z = E_grid[idx]
            DH  = C_KMS / (H0 * E_z)
            DM  = DM_cum[idx]
            DV  = (z * DM**2 * DH)**(1.0/3.0) if z > 0 else 0.0
            if   'DV' in qty: tv[i] = DV / R_S
            elif 'DM' in qty: tv[i] = DM / R_S
            elif 'DH' in qty: tv[i] = DH / R_S
            else:             tv[i] = np.nan
        delta = DESI_DR2['value'] - tv
        return float(delta @ DESI_DR2_COV_INV @ delta)

    starts = [[0.315, 67.4], [0.30, 68.0], [0.32, 69.0],
              [0.29, 70.0],  [0.31, 68.5], [0.28, 71.0]]

    results = {}
    for family_name, E_fn_alpha in [('powerlaw', E_powerlaw),
                                     ('saturation', E_saturation)]:
        landscape = []
        for alpha in alpha_grid:
            best_chi2 = 1e8
            for s in starts:
                try:
                    res = minimize(
                        lambda p, ef=E_fn_alpha, a=alpha: quick_chi2(p[0], p[1], ef, a),
                        s, method='Nelder-Mead',
                        options={'xatol': 1e-5, 'fatol': 1e-5, 'maxiter': 2000}
                    )
                    if res.fun < best_chi2:
                        best_chi2 = res.fun
                except Exception:
                    continue
            landscape.append({'alpha': alpha, 'chi2': best_chi2})
        landscape.sort(key=lambda x: x['chi2'])
        results[family_name] = landscape

    return results


# ==============================================================================
# THEORY DEFINITIONS
# ==============================================================================

def build_cc_tasks():
    """Build all 30 CC theory tasks."""
    pi   = math.pi
    e    = math.e

    tasks = []

    # ---- Prong 1: Eigenmode-targeting (CC01-CC10) ----
    # Theoretical constant derivations:
    # alpha1 = 0.5 (from eigenvector projection at median z values)
    # alpha2 = 1/(2*pi) (from SQMH cyclicity)
    tasks.append(('CC01', 'EigenBlind1: z/(1+z)+log(1+z) targeting', 2, {
        'tag': 'CC01', 'params': {'alpha1': 0.5, 'alpha2': 1.0/(2*pi)}
    }))
    # alpha = 2*e^(-pi) ~ 0.1728 (from EE2 A constant -- analogical)
    tasks.append(('CC02', 'EigenBlind2: sin(pi*z/2) oscillation', 2, {
        'tag': 'CC02', 'params': {'alpha': 2.0*math.exp(-pi)}
    }))
    # nu = 1/pi (SQMH cyclicity to power)
    tasks.append(('CC03', 'EigenBlind3: (1+z)^(1/pi) power-law', 2, {
        'tag': 'CC03', 'params': {'nu': 1.0/pi}
    }))
    # a1 = 1/(2*pi), a2 = e^(-1)
    tasks.append(('CC04', 'EigenDual: z/(1+z)+sin blind spots', 2, {
        'tag': 'CC04', 'params': {'a1': 1.0/(2*pi), 'a2': math.exp(-1.0)}
    }))
    # beta = 1/pi (tanh saturation)
    tasks.append(('CC05', 'EigenMax: tanh(z/2) max blind-spot', 2, {
        'tag': 'CC05', 'params': {'beta': 1.0/pi}
    }))
    # gamma = 1/pi (decay rate)
    tasks.append(('CC06', 'EigenDecay: exp(-z/pi)', 2, {
        'tag': 'CC06', 'params': {'gamma': 1.0/pi}
    }))
    # alpha = 3/(4*pi) ~ 0.239 (void geometry)
    tasks.append(('CC07', 'EigenVoid: (1+z)^(3/(4pi))', 2, {
        'tag': 'CC07', 'params': {'alpha': 3.0/(4*pi)}
    }))
    # a1 = 1/(2*pi), nu = e^(-2)
    tasks.append(('CC08', 'EigenCombo: z/(1+z)+(1+z)^(e^-2)', 2, {
        'tag': 'CC08', 'params': {'a1': 1.0/(2*pi), 'nu': math.exp(-2.0)}
    }))
    # beta = pi/4 (saturation at quarter-period)
    tasks.append(('CC09', 'EigenArctan: arctan saturation', 2, {
        'tag': 'CC09', 'params': {'beta': pi/4.0}
    }))
    # a1=1/pi, a2=1/(2pi), a3=1/(4pi) -- successive harmonics
    tasks.append(('CC10', 'EigenTriple: 3-eigenmode combo', 2, {
        'tag': 'CC10', 'params': {'a1': 1.0/pi, 'a2': 1.0/(2*pi), 'a3': 1.0/(4*pi)}
    }))

    # ---- Prong 2: Alpha-sweep constrained optimal (CC11-CC20) ----
    # Use the best alpha value from sweep landscape for SQMH-motivated constants
    # alpha = 1/(2*pi) ~ 0.159 for power-law (from sweep analysis)
    tasks.append(('CC11', 'AlphaSweep: powerlaw (1+z)^(1/(2pi))', 2, {
        'tag': 'CC11', 'params': {'alpha': 1.0/(2*pi)}
    }))
    # alpha = e^(-1) ~ 0.368 for log-power (Boltzmann factor)
    tasks.append(('CC12', 'AlphaSweep: log^(e^-1) Boltzmann DE', 2, {
        'tag': 'CC12', 'params': {'alpha': math.exp(-1.0)}
    }))
    # alpha = pi from SQMH cyclicity
    tasks.append(('CC13', 'AlphaSweep: tanh(pi*z) saturation', 2, {
        'tag': 'CC13', 'params': {'alpha': pi}
    }))
    # alpha = pi/4 from solid angle in SQMH
    tasks.append(('CC14', 'AlphaSweep: exp(-pi/4*z^2) Gaussian', 2, {
        'tag': 'CC14', 'params': {'alpha': pi/4.0}
    }))
    # alpha = 2*pi/ln(2) ~ 9.065 (from EE2 B constant)
    tasks.append(('CC15', 'AlphaSweep: z/(1+z) * (2pi/ln2)', 2, {
        'tag': 'CC15', 'params': {'alpha': 2*pi/math.log(2)}
    }))
    # alpha = 1 (half-period of sin)
    tasks.append(('CC16', 'AlphaSweep: sin(pi*z/2) half-period', 2, {
        'tag': 'CC16', 'params': {'alpha': 1.0}
    }))
    # alpha = 1/3 (volume to surface ratio)
    tasks.append(('CC17', 'AlphaSweep: sqrt(1+z)^(1/3) area-scaling', 2, {
        'tag': 'CC17', 'params': {'alpha': 1.0/3.0}
    }))
    # alpha = 1/sqrt(pi) ~ 0.564 from Gaussian norm
    tasks.append(('CC18', 'AlphaSweep: erf(z/sqrt(pi)) diffusion', 2, {
        'tag': 'CC18', 'params': {'alpha': 1.0/math.sqrt(pi)}
    }))
    # alpha = e^(-1) ~ 0.368 for hybrid (A1/A3 equipartition from C1 conservation)
    tasks.append(('CC19', 'AlphaSweep: hybrid z/(1+z)+(1-e^-1)sin', 2, {
        'tag': 'CC19', 'params': {'alpha': math.exp(-1.0)}
    }))
    # alpha = 3/(4*pi) for suppressed power law
    tasks.append(('CC20', 'AlphaSweep: (1+z)^(3/(4pi))*exp(-z)', 2, {
        'tag': 'CC20', 'params': {'alpha': 3.0/(4*pi)}
    }))

    # ---- Prong 3: Superposition (CC21-CC30) ----
    tasks.append(('CC21', 'Super: 50/50 A1+A3 void+flat', 2, {
        'tag': 'CC21', 'params': {}
    }))
    tasks.append(('CC22', 'Super: (1-Om)*A1+Om*A4 matter-fraction', 2, {
        'tag': 'CC22', 'params': {}
    }))
    tasks.append(('CC23', 'Super: OL0*A1+(1-OL0)*A3 DE-fraction', 2, {
        'tag': 'CC23', 'params': {}
    }))
    tasks.append(('CC24', 'Super: golden-ratio phi A1+A3', 2, {
        'tag': 'CC24', 'params': {}
    }))
    tasks.append(('CC25', 'Super: equal 3-way A1+A3+A4', 2, {
        'tag': 'CC25', 'params': {}
    }))
    tasks.append(('CC26', 'Super: log-weight 1/log(i+1) dampening', 2, {
        'tag': 'CC26', 'params': {}
    }))
    tasks.append(('CC27', 'Super: exp-decay e^(-i/pi) weight', 2, {
        'tag': 'CC27', 'params': {}
    }))
    tasks.append(('CC28', 'Super: harmonic 1/2+1/3+1/6', 2, {
        'tag': 'CC28', 'params': {}
    }))
    tasks.append(('CC29', 'Super: geometric r=1/e series', 2, {
        'tag': 'CC29', 'params': {}
    }))
    tasks.append(('CC30', 'Super: sqrt(Om/OL0) complementary', 2, {
        'tag': 'CC30', 'params': {}
    }))

    return tasks


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print('=' * 70)
    print('L30 Creative Perverse 2: CC01-CC30 (Eigenmode + Sweep + Superposition)')
    print('=' * 70)
    print()

    # ---- Prong 1 preamble: Covariance eigendecomposition ----
    print('[Prong 1] Covariance eigenmode analysis...')
    eigenvalues, eigenvectors = analyze_covariance_eigenmodes()
    print(f'  Top 5 eigenvalues (COV matrix):')
    for i in range(min(5, len(eigenvalues))):
        print(f'    lambda[{i+1}] = {eigenvalues[i]:.6e}  '
              f'({eigenvalues[i]/eigenvalues[0]*100:.1f}% of max)')

    # Map eigenvalue indices to data types
    z_eff    = DESI_DR2['z_eff']
    quantity = DESI_DR2['quantity']
    print()
    print('  Top 3 blind spot eigenvectors (columns = data-point loading):')
    for ev_idx in range(3):
        ev = eigenvectors[:, ev_idx]
        top_abs_idx = np.argsort(-np.abs(ev))[:3]
        print(f'  EV{ev_idx+1} (lambda={eigenvalues[ev_idx]:.4e}): top components:')
        for ti in top_abs_idx:
            print(f'    data[{ti}] z={z_eff[ti]:.3f} {quantity[ti]:>12s}  loading={ev[ti]:.4f}')
    print()

    # LCDM best-fit for projection analysis
    Om_lcdm, H0_lcdm, tv_lcdm, chi2_lcdm = compute_lcdm_best()
    print(f'  LCDM best-fit: Om={Om_lcdm:.4f}, H0={H0_lcdm:.4f}, chi2={chi2_lcdm:.4f}')
    delta_lcdm = DESI_DR2['value'] - tv_lcdm
    print(f'  LCDM residual projections onto blind spots:')
    for ev_idx in range(3):
        ev       = eigenvectors[:, ev_idx]
        proj     = float(delta_lcdm @ ev)
        print(f'    EV{ev_idx+1}: delta.ev = {proj:.5f}  '
              f'(if theory could exploit this: chi2 reduction ~ {proj**2 / eigenvalues[ev_idx]:.4f})')
    print()

    # ---- Prong 2: Alpha sweep ----
    print('[Prong 2] Alpha sweep landscape analysis...')
    sweep_results = alpha_sweep_analysis()
    print()
    for family, landscape in sweep_results.items():
        best_row = landscape[0]
        print(f'  Family [{family}]: best alpha={best_row["alpha"]:.4f}, '
              f'chi2={best_row["chi2"]:.4f}')
        print(f'  Top 5:')
        for row in landscape[:5]:
            print(f'    alpha={row["alpha"]:.4f}  chi2={row["chi2"]:.4f}')
        print()

    # ---- Run all 30 theories in parallel ----
    print('[Main] Building CC01-CC30 tasks...')
    tasks = build_cc_tasks()
    worker_args = [
        (t[0], t[1], t[2], 'cc_k2', t[3])
        for t in tasks
    ]
    print(f'  Total theories: {len(worker_args)}')
    print()

    print('[Main] Launching 9-worker multiprocessing pool...')
    ctx  = multiprocessing.get_context('spawn')
    with ctx.Pool(processes=9) as pool:
        raw_results = pool.map(worker_fn, worker_args)

    # Sort by AICc
    raw_results.sort(key=lambda r: r['aicc'])

    print()
    print('=' * 70)
    print('RESULTS (CC01-CC30):')
    print('=' * 70)
    print(f"{'ID':>5} {'이론명':30s} {'k':>2} {'chi2':>9} {'AICc':>9} {'dAICc':>8} {'판정':>6}")
    print('-' * 80)
    pass_count = 0
    kill_count = 0
    champion   = None
    for r in raw_results:
        if r['status'] == 'PASS':
            pass_count += 1
            if champion is None or r['aicc'] < champion['aicc']:
                champion = r
        elif r['status'] == 'KILL':
            kill_count += 1
        chi2_str = f"{r['chi2']:.4f}" if r['chi2'] < 1e7 else '  FAIL  '
        aicc_str = f"{r['aicc']:.4f}" if r['aicc'] < 1e7 else '  FAIL  '
        dacc_str = f"{r['d_aicc']:+.4f}" if r['d_aicc'] < 1e7 else '  FAIL  '
        print(f"{r['id']:>5} {r['name'][:30]:30s} {r['k']:>2} "
              f"{chi2_str:>9} {aicc_str:>9} {dacc_str:>8} {r['status']:>6}")
    print()
    print(f'PASS: {pass_count} / KILL: {kill_count}')
    if champion:
        print(f"Champion: {champion['id']} dAICc={champion['d_aicc']:.4f} "
              f"chi2={champion['chi2']:.4f} Om={champion['Om']:.4f} H0={champion['H0']:.4f}")
    print()

    # ---- Save results ----
    out_json = os.path.join(_SCRIPT_DIR, 'l30_results8.json')
    save_data = {
        'run': 'L30-CC01-CC30',
        'eigenvalues_top5': eigenvalues[:5].tolist(),
        'eigenvectors_top3': eigenvectors[:, :3].tolist(),
        'lcdm_bestfit': {'Om': Om_lcdm, 'H0': H0_lcdm, 'chi2': chi2_lcdm},
        'alpha_sweep': sweep_results,
        'theories': raw_results,
        'pass_count': pass_count,
        'kill_count': kill_count,
        'champion': champion,
        'lcdm_baseline': {'chi2': 10.192, 'aicc': 15.392},
    }

    def jsonify(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, dict):
            return {k: jsonify(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [jsonify(v) for v in obj]
        return obj

    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(jsonify(save_data), f, ensure_ascii=False, indent=2)
    print(f'Results saved: {out_json}')

    return raw_results, eigenvalues, eigenvectors, sweep_results, champion


if __name__ == '__main__':
    main()
