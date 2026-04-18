# -*- coding: utf-8 -*-
"""
l30_test7.py -- L30 7th Run: Adversarial Reverse Engineering + Brute-Force Random Search (BB01-BB30)
======================================================================================================
Adversarial two-step strategy:

Step 1: Adversarial Analysis (BB01-BB10)
  - Compute LCDM residuals for all 13 DESI DR2 data points
  - Find 3 worst-fit points
  - Design targeted theories to fix those specific weak points

Step 2: Systematic Random Search (BB11-BB30)
  - Generate 250 random E^2(z) functional form descriptors using np.random.seed(42)
  - Random combinations of: powers, log, exp, sin, erf, ...
  - Quick-evaluate all 250, keep top 20 (BB11-BB30)
  - Full Nelder-Mead optimization on each

NOTE: Random forms are serialized as (basis_ids, coeffs) tuples so spawn-safe.

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

# paths
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SIM_DIR    = os.path.dirname(_SCRIPT_DIR)
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

from desi_data import DESI_DR2, DESI_DR2_COV_INV

# constants
C_KMS   = 299792.458
R_S     = 147.09
OR      = 5.38e-5
N_DATA  = 13
N_GRID  = 4000
LCDM_BASELINE_CHI2  = 10.192
LCDM_BASELINE_AICC  = 15.392

# ==============================================================================
# BASIS FUNCTION REGISTRY
# Serializable as integer IDs. Each function computes f(z) where f(0)=0
# (so that OL0*(1 + sum c_i*f_i) = OL0 at z=0 automatically).
# ==============================================================================

# Basis function definitions (each returns array of same shape as z_arr)
# Note: f(0) must be 0 for the normalization trick to work.
# For functions not naturally zero at z=0, subtract f(0).
def _basis_func(bid, z_arr):
    """Evaluate basis function #bid at z_arr. All are zero at z=0."""
    z = z_arr
    if bid == 0:   return np.log1p(z)
    elif bid == 1: return z
    elif bid == 2: return z**2
    elif bid == 3: return z**3
    elif bid == 4: return np.sqrt(z + 1e-30) - 1.0          # sqrt(z)-0
    elif bid == 5: return np.exp(-z) - 1.0
    elif bid == 6: return np.exp(-z**2) - 1.0
    elif bid == 7: return np.tanh(z)
    elif bid == 8: return np.sin(np.pi * z / 2.0)
    elif bid == 9:
        from scipy.special import erf
        return erf(z)
    elif bid == 10: return z * np.log1p(z)
    elif bid == 11: return np.exp(z) - 1.0
    elif bid == 12: return np.log1p(z)**2
    elif bid == 13: return np.tanh(2*z)
    elif bid == 14: return np.sin(np.pi * z)
    elif bid == 15: return np.cos(np.pi * z) - 1.0
    elif bid == 16: return np.arctan(z)
    elif bid == 17: return z * np.sinh(z)
    elif bid == 18: return z * (np.cosh(z) - 1.0)
    # Power law: (1+z)^p - 1
    elif bid == 19: return (1+z)**0.25 - 1.0
    elif bid == 20: return (1+z)**0.5  - 1.0
    elif bid == 21: return (1+z)**0.75 - 1.0
    elif bid == 22: return (1+z)**1.5  - 1.0
    elif bid == 23: return (1+z)**2.0  - 1.0
    elif bid == 24: return (1+z)**2.5  - 1.0
    elif bid == 25: return (1+z)**3.0  - 1.0
    # More
    elif bid == 26: return np.log1p(z**2)
    elif bid == 27: return np.exp(-z/2.0) - 1.0
    elif bid == 28: return z / (1.0 + z)
    elif bid == 29: return np.tanh(z/2.0)
    else:
        raise ValueError(f'Unknown basis id {bid}')

N_BASIS = 30  # total basis functions (bid 0..29)

BASIS_NAMES = [
    'log1p', 'z', 'z2', 'z3', 'sqrt_m1', 'expnz_m1', 'expnz2_m1',
    'tanh', 'sin_pi2', 'erf', 'zlog1p', 'expz_m1', 'log1p2',
    'tanh2z', 'sinpiz', 'cospiz_m1', 'arctan', 'zsinhz', 'zcoshm1',
    'pow025_m1', 'pow05_m1', 'pow075_m1', 'pow15_m1', 'pow20_m1',
    'pow25_m1', 'pow30_m1', 'log1pz2', 'expnz2_m1b', 'z_over_1pz', 'tanh_h',
]


def E_random_from_descriptor(z_arr, Om, basis_ids, coeffs):
    """
    Compute E(z) from a random descriptor:
      E^2(z) = OR*(1+z)^4 + Om*(1+z)^3 + OL0*(1 + sum_i c_i * f_i(z))
    where f_i(0) = 0 ensures E(0) = 1 exactly.
    """
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None

    delta = np.zeros_like(z_arr)
    for bid, c in zip(basis_ids, coeffs):
        try:
            delta += c * _basis_func(bid, z_arr)
        except Exception:
            return None

    rho_DE = OL0 * (1.0 + delta)
    rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


def aicc(chi2_val, k, n=N_DATA):
    return chi2_val + 2*k + 2*k*(k+1)/(n - k - 1)


def compute_theory_vector(Omega_m, H0, E_func):
    """Generic BAO theory vector given E(z) callable."""
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


def chi2_func(params, E_func):
    """Chi-squared with full covariance."""
    Omega_m, H0 = params[0], params[1]
    if not (0.05 < Omega_m < 0.70 and 50.0 < H0 < 100.0):
        return 1e8
    th = compute_theory_vector(Omega_m, H0, E_func)
    if th is None or not np.all(np.isfinite(th)):
        return 1e8
    delta = DESI_DR2['value'] - th
    return float(delta @ DESI_DR2_COV_INV @ delta)


# ==============================================================================
# STEP 1: LCDM RESIDUAL ANALYSIS
# ==============================================================================

def find_lcdm_worst_points():
    """Find LCDM best-fit and compute per-point residuals."""
    def E_lcdm(z_arr, Om):
        OL0 = 1.0 - Om - OR
        E2  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
        return np.sqrt(np.maximum(E2, 1e-30))

    starts = [
        [0.315, 67.4], [0.30, 68.0], [0.32, 69.0],
        [0.29, 70.0],  [0.31, 68.5], [0.28, 71.0],
        [0.33, 67.0],  [0.34, 66.5],
    ]
    best_chi2 = 1e8
    best_x    = None
    for s in starts:
        try:
            res = minimize(lambda p: chi2_func(p, E_lcdm), s,
                           method='Nelder-Mead',
                           options={'xatol': 1e-7, 'fatol': 1e-7, 'maxiter': 5000})
            if res.fun < best_chi2:
                best_chi2 = res.fun
                best_x    = res.x
        except Exception:
            continue

    if best_x is None:
        return 0.315, 67.4, None, None

    Om_best, H0_best = float(best_x[0]), float(best_x[1])
    th   = compute_theory_vector(Om_best, H0_best, E_lcdm)
    data = DESI_DR2['value']
    sig  = DESI_DR2['sigma']
    pull     = (data - th) / sig
    worst_idx = np.argsort(-np.abs(pull))
    return Om_best, H0_best, pull, worst_idx


# ==============================================================================
# STEP 2: RANDOM SEARCH (serializable descriptors)
# ==============================================================================

def generate_random_descriptors(n_candidates=250, seed=42):
    """
    Generate n_candidates random DE correction descriptors.
    Each descriptor is (basis_ids_list, coeffs_list).
    Returns list of (cand_id, name, basis_ids, coeffs).
    """
    rng = np.random.default_rng(seed)
    candidates = []
    for cand_idx in range(n_candidates):
        n_terms = int(rng.integers(1, 4))  # 1, 2 or 3 basis functions
        basis_ids = rng.choice(N_BASIS, size=n_terms, replace=False).tolist()
        coeffs    = rng.uniform(-0.8, 0.8, size=n_terms).tolist()

        names_used = [BASIS_NAMES[b] for b in basis_ids]
        term_parts = [f'{c:.3f}*{n}' for c, n in zip(coeffs, names_used)]
        name = f'BF[{",".join(term_parts)}]'
        candidates.append((f'RAND{cand_idx:03d}', name, basis_ids, coeffs))
    return candidates


def quick_chi2_descriptor(basis_ids, coeffs, Om0=0.315, H0_0=67.4):
    """Quick chi2 evaluation at fiducial point."""
    def E_fn(z_arr, Om):
        return E_random_from_descriptor(z_arr, Om, basis_ids, coeffs)
    th = compute_theory_vector(Om0, H0_0, E_fn)
    if th is None or not np.all(np.isfinite(th)):
        return 1e8
    delta = DESI_DR2['value'] - th
    return float(delta @ DESI_DR2_COV_INV @ delta)


def select_top_random_descriptors(n_keep=20, seed=42):
    """Generate 250 random candidates, quick-screen, return top n_keep."""
    candidates = generate_random_descriptors(n_candidates=250, seed=seed)
    scored = []
    for cand_id, name, basis_ids, coeffs in candidates:
        q = quick_chi2_descriptor(basis_ids, coeffs)
        if q < 1e7:
            scored.append((q, cand_id, name, basis_ids, coeffs))
    scored.sort(key=lambda x: x[0])
    return scored[:n_keep]


# ==============================================================================
# ADVERSARIAL THEORIES (BB01-BB10): named E_func signatures
# (These are module-level functions, picklable by spawn)
# ==============================================================================

def BB01_E(z_arr, Om):
    """LowZ Tilt: rho_DE = OL0*(1 - Om*z/(1+z))"""
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    rho_DE = OL0 * (1.0 - Om * z_arr / (1.0 + z_arr))
    rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


def BB03_E(z_arr, Om):
    """HighZ Lorentzian Suppression: rho_DE = OL0 / (1 + (z/1.0)^2)"""
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    rho_DE = OL0 / (1.0 + z_arr**2)  # z0=1, normalized at z=0: denom=1
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


def BB05_E(z_arr, Om):
    """LowZ Gaussian Bump at BGS: rho_DE = OL0*(1 + A*exp(-(z-0.3)^2/(2*0.15^2)) - A*exp(...0...))"""
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    z_peak = 0.30
    sig_z  = 0.15
    A_bump = Om * 0.5
    bump0  = A_bump * np.exp(-0.5 * (z_peak / sig_z)**2)
    bump   = A_bump * np.exp(-0.5 * ((z_arr - z_peak) / sig_z)**2)
    rho_DE = OL0 * (1.0 + bump - bump0)
    rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


def BB06_E(z_arr, Om):
    """HighZ Log Reduction: rho_DE = OL0*(1 - Om/2 * log(1+z))"""
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    rho_DE = OL0 * (1.0 - (Om * 0.5) * np.log1p(z_arr))
    rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


def BB08_E(z_arr, Om):
    """PullWeighted Gaussian Decay: rho_DE = OL0*exp(-Om^2/OL0 * z^2)"""
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    gamma  = Om**2 / OL0
    rho_DE = OL0 * np.exp(-gamma * z_arr**2)
    rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


def BB10_E(z_arr, Om):
    """Adversarial Tanh Transition: rho_DE = OL0*(1 - beta*(tanh(z/0.5) - tanh(0)))"""
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    beta  = Om / (1.0 + Om)
    z_tr  = 0.5
    rho_DE = OL0 * (1.0 - beta * np.tanh(z_arr / z_tr))
    rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Factory functions for k=3 theories
def BB02_E_factory(alpha):
    """LowZ Tilt Free: rho_DE = OL0*(1 - alpha*z/(1+z))"""
    # Note: cannot be inner function for pickle; use module-level registry approach
    return (2, alpha)   # signals type 2 to worker


def BB04_E_factory(z0):
    """HighZ Lorentzian Free Scale: z0 parameter"""
    return (4, z0)


def BB07_E_factory(alpha):
    """Log Tilt Free: rho_DE = OL0*(1 + alpha*log(1+z))"""
    return (7, alpha)


def BB09_E_factory(gamma):
    """Quadratic Gaussian Decay Free: rho_DE = OL0*exp(-gamma*z^2)"""
    return (9, gamma)


# ==============================================================================
# WORKER FUNCTION (fully self-contained for spawn)
# Uses task type tags to reconstruct functions
# ==============================================================================

def worker_fn(args):
    """
    Runs in a separate process.
    Task format: (wid, theory_name, k, task_type, task_data)

    task_type:
      'named_k2'    : task_data = function name string (module-level function)
      'factory_k3'  : task_data = (factory_type_int, extra_starts_list)
      'descriptor'  : task_data = (basis_ids, coeffs)
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

    C_KMS   = 299792.458
    R_S     = 147.09
    OR_W    = 5.38e-5
    N_DATA  = 13
    N_GRID  = 4000
    LCDM_BASELINE_AICC = 15.392

    def aicc_w(chi2_val, k_in, n=N_DATA):
        return chi2_val + 2*k_in + 2*k_in*(k_in+1)/(n - k_in - 1)

    def _basis_func_w(bid, z_arr):
        """Worker-local basis function registry."""
        z = z_arr
        if bid == 0:   return np.log1p(z)
        elif bid == 1: return z
        elif bid == 2: return z**2
        elif bid == 3: return z**3
        elif bid == 4: return np.sqrt(z + 1e-30) - 1.0
        elif bid == 5: return np.exp(-z) - 1.0
        elif bid == 6: return np.exp(-z**2) - 1.0
        elif bid == 7: return np.tanh(z)
        elif bid == 8: return np.sin(np.pi * z / 2.0)
        elif bid == 9:
            from scipy.special import erf
            return erf(z)
        elif bid == 10: return z * np.log1p(z)
        elif bid == 11: return np.exp(z) - 1.0
        elif bid == 12: return np.log1p(z)**2
        elif bid == 13: return np.tanh(2*z)
        elif bid == 14: return np.sin(np.pi * z)
        elif bid == 15: return np.cos(np.pi * z) - 1.0
        elif bid == 16: return np.arctan(z)
        elif bid == 17: return z * np.sinh(z)
        elif bid == 18: return z * (np.cosh(z) - 1.0)
        elif bid == 19: return (1+z)**0.25 - 1.0
        elif bid == 20: return (1+z)**0.5  - 1.0
        elif bid == 21: return (1+z)**0.75 - 1.0
        elif bid == 22: return (1+z)**1.5  - 1.0
        elif bid == 23: return (1+z)**2.0  - 1.0
        elif bid == 24: return (1+z)**2.5  - 1.0
        elif bid == 25: return (1+z)**3.0  - 1.0
        elif bid == 26: return np.log1p(z**2)
        elif bid == 27: return np.exp(-z/2.0) - 1.0
        elif bid == 28: return z / (1.0 + z)
        elif bid == 29: return np.tanh(z/2.0)
        else:
            raise ValueError(f'Unknown basis id {bid}')

    def E_descriptor(z_arr, Om, basis_ids, coeffs):
        OL0 = 1.0 - Om - OR_W
        if OL0 <= 0 or Om <= 0:
            return None
        delta = np.zeros_like(z_arr, dtype=float)
        for bid, c in zip(basis_ids, coeffs):
            try:
                delta += c * _basis_func_w(bid, z_arr)
            except Exception:
                return None
        rho_DE = OL0 * (1.0 + delta)
        rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
        E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
            return None
        return np.sqrt(np.maximum(E2, 1e-30))

    def E_named_k2(z_arr, Om, func_name):
        """Reconstruct named k=2 theory."""
        OL0 = 1.0 - Om - OR_W
        if OL0 <= 0 or Om <= 0:
            return None

        if func_name == 'BB01':
            rho_DE = OL0 * (1.0 - Om * z_arr / (1.0 + z_arr))
        elif func_name == 'BB03':
            rho_DE = OL0 / (1.0 + z_arr**2)
        elif func_name == 'BB05':
            z_peak = 0.30; sig_z = 0.15; A_bump = Om * 0.5
            bump0  = A_bump * np.exp(-0.5 * (z_peak / sig_z)**2)
            bump   = A_bump * np.exp(-0.5 * ((z_arr - z_peak) / sig_z)**2)
            rho_DE = OL0 * (1.0 + bump - bump0)
        elif func_name == 'BB06':
            rho_DE = OL0 * (1.0 - (Om * 0.5) * np.log1p(z_arr))
        elif func_name == 'BB08':
            gamma  = Om**2 / OL0
            rho_DE = OL0 * np.exp(-gamma * z_arr**2)
        elif func_name == 'BB10':
            beta  = Om / (1.0 + Om)
            rho_DE = OL0 * (1.0 - beta * np.tanh(z_arr / 0.5))
        else:
            return None

        rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
        E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
            return None
        return np.sqrt(np.maximum(E2, 1e-30))

    def E_factory_k3(z_arr, Om, factory_type, extra_param):
        """Reconstruct k=3 theory with extra parameter."""
        OL0 = 1.0 - Om - OR_W
        if OL0 <= 0 or Om <= 0:
            return None

        if factory_type == 2:    # BB02: LowZ Tilt Free
            alpha  = extra_param
            rho_DE = OL0 * (1.0 - alpha * z_arr / (1.0 + z_arr))
        elif factory_type == 4:  # BB04: HighZ Lorentzian Free z0
            z0     = extra_param
            if z0 <= 0:
                return None
            rho_DE = OL0 / (1.0 + (z_arr / z0)**2)
        elif factory_type == 7:  # BB07: Log Tilt Free
            alpha  = extra_param
            rho_DE = OL0 * (1.0 + alpha * np.log1p(z_arr))
        elif factory_type == 9:  # BB09: Quadratic Gaussian Decay Free
            gamma  = extra_param
            rho_DE = OL0 * np.exp(-gamma * z_arr**2)
        else:
            return None

        rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
        E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
            return None
        return np.sqrt(np.maximum(E2, 1e-30))

    def compute_tv(Omega_m, H0, E_fn):
        z_eff  = DESI_DR2['z_eff']
        z_max  = z_eff.max() + 0.01
        z_grid = np.linspace(0.0, z_max, N_GRID)
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
        DM_cum = (C_KMS / H0) * np.concatenate(
            [[0.0], cumulative_trapezoid(inv_E, z_grid)]
        )
        theory_vec = np.empty(N_DATA)
        for i, (z, qty) in enumerate(zip(z_eff, DESI_DR2['quantity'])):
            idx = min(np.searchsorted(z_grid, z), N_GRID - 1)
            E_z = E_grid[idx]
            DH  = C_KMS / (H0 * E_z)
            DM  = DM_cum[idx]
            DV  = (z * DM**2 * DH)**(1.0/3.0) if z > 0 else 0.0
            if   'DV' in qty: theory_vec[i] = DV / R_S
            elif 'DM' in qty: theory_vec[i] = DM / R_S
            elif 'DH' in qty: theory_vec[i] = DH / R_S
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

    # Unpack args
    wid, theory_name, k, task_type, task_data = args

    base_starts = [
        [0.315, 67.4], [0.30, 68.0], [0.32, 69.0],
        [0.29, 70.0],  [0.31, 68.5], [0.28, 71.0],
        [0.33, 67.0],  [0.34, 66.5],
    ]

    try:
        if task_type == 'named_k2':
            func_name = task_data
            E_fn = lambda z, Om, fn=func_name: E_named_k2(z, Om, fn)

            best_val = 1e8
            best_x   = None
            for s in base_starts:
                try:
                    res = minimize(lambda p: chi2_w(p, E_fn), s,
                                   method='Nelder-Mead',
                                   options={'xatol': 1e-6, 'fatol': 1e-6, 'maxiter': 5000})
                    if res.fun < best_val:
                        best_val = res.fun
                        best_x   = res.x
                except Exception:
                    continue

            if best_x is None:
                return {'id': wid, 'name': theory_name, 'k': 2,
                        'chi2': 1e8, 'aicc': 1e8, 'd_aicc': 1e8,
                        'Om': None, 'H0': None, 'extra': None, 'status': 'FAIL'}

            Om_best, H0_best = float(best_x[0]), float(best_x[1])
            chi2_best  = float(best_val)
            extra_best = None

        elif task_type == 'factory_k3':
            factory_type, extra_starts = task_data

            combined_starts = [b + [e] for b in base_starts for e in extra_starts]

            def full_wrapper(p):
                E_fn = lambda z, Om, ft=factory_type, ep=p[2]: E_factory_k3(z, Om, ft, ep)
                return chi2_w(p[:2], E_fn)

            best_val = 1e8
            best_x   = None
            for s in combined_starts:
                try:
                    res = minimize(full_wrapper, s, method='Nelder-Mead',
                                   options={'xatol': 1e-6, 'fatol': 1e-6, 'maxiter': 5000})
                    if res.fun < best_val:
                        best_val = res.fun
                        best_x   = res.x
                except Exception:
                    continue

            if best_x is None:
                return {'id': wid, 'name': theory_name, 'k': 3,
                        'chi2': 1e8, 'aicc': 1e8, 'd_aicc': 1e8,
                        'Om': None, 'H0': None, 'extra': None, 'status': 'FAIL'}

            Om_best, H0_best = float(best_x[0]), float(best_x[1])
            chi2_best  = float(best_val)
            extra_best = float(best_x[2])

        elif task_type == 'descriptor':
            basis_ids, coeffs = task_data
            E_fn = lambda z, Om, bi=basis_ids, co=coeffs: E_descriptor(z, Om, bi, co)

            best_val = 1e8
            best_x   = None
            for s in base_starts:
                try:
                    res = minimize(lambda p: chi2_w(p, E_fn), s,
                                   method='Nelder-Mead',
                                   options={'xatol': 1e-6, 'fatol': 1e-6, 'maxiter': 5000})
                    if res.fun < best_val:
                        best_val = res.fun
                        best_x   = res.x
                except Exception:
                    continue

            if best_x is None:
                return {'id': wid, 'name': theory_name, 'k': 2,
                        'chi2': 1e8, 'aicc': 1e8, 'd_aicc': 1e8,
                        'Om': None, 'H0': None, 'extra': None, 'status': 'FAIL'}

            Om_best, H0_best = float(best_x[0]), float(best_x[1])
            chi2_best  = float(best_val)
            extra_best = None

        else:
            return {'id': wid, 'name': theory_name, 'k': k,
                    'chi2': 1e8, 'aicc': 1e8, 'd_aicc': 1e8,
                    'Om': None, 'H0': None, 'extra': None, 'status': 'ERROR',
                    'error': f'Unknown task_type: {task_type}'}

        aicc_val = aicc_w(chi2_best, k)
        d_aicc   = aicc_val - LCDM_BASELINE_AICC
        status   = 'PASS' if aicc_val < LCDM_BASELINE_AICC else 'KILL'

        return {
            'id':     wid,
            'name':   theory_name,
            'k':      k,
            'chi2':   chi2_best,
            'aicc':   aicc_val,
            'd_aicc': d_aicc,
            'Om':     Om_best,
            'H0':     H0_best,
            'extra':  extra_best,
            'status': status,
        }

    except Exception as ex:
        return {'id': wid, 'name': theory_name, 'k': k,
                'chi2': 1e8, 'aicc': 1e8, 'd_aicc': 1e8,
                'Om': None, 'H0': None, 'extra': None,
                'status': 'ERROR', 'error': str(ex)}


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    out_dir   = _SCRIPT_DIR
    json_path = os.path.join(out_dir, 'l30_results7.json')

    print('=' * 70)
    print('L30 7th Run: Adversarial Reverse Engineering + Brute-Force Search')
    print('  BB01-BB10: Adversarial from LCDM residuals')
    print('  BB11-BB30: Best 20 from 250 random functional forms')
    print('LCDM baseline: chi2={:.3f}  AICc={:.3f}'.format(
        LCDM_BASELINE_CHI2, LCDM_BASELINE_AICC))
    print('=' * 70)

    # ── Step 1: LCDM Residual Analysis ─────────────────────────────────────────
    print()
    print('=== STEP 1: LCDM RESIDUAL ANALYSIS ===')
    Om_lcdm, H0_lcdm, pull, worst_idx = find_lcdm_worst_points()
    print(f'LCDM best-fit: Om={Om_lcdm:.4f}, H0={H0_lcdm:.4f}')

    z_eff    = DESI_DR2['z_eff']
    qty_list = DESI_DR2['quantity']
    worst_3  = []

    if pull is not None and worst_idx is not None:
        print()
        print('Per-point LCDM residuals (sigma units), sorted by |pull|:')
        print(f"{'rank':>5} {'i':>3} {'z':>6} {'qty':>12} {'pull':>8}")
        print('-' * 40)
        for rank, i in enumerate(worst_idx):
            z_i = float(z_eff[i])
            q_i = qty_list[i]
            p_i = float(pull[i])
            if rank < 3:
                worst_3.append((int(i), z_i, q_i, p_i))
            marker = '***' if rank < 3 else ''
            print(f'{rank+1:>5} {i:>3} {z_i:>6.3f} {q_i:>12} {p_i:>8.3f} {marker}')

        print()
        print('Top 3 worst-fit DESI points (adversarial targets):')
        for rank, (i, z_i, q_i, p_i) in enumerate(worst_3):
            print(f'  #{rank+1}: i={i}, z={z_i:.3f}, {q_i}, pull={p_i:+.3f}sigma')

    # ── Step 2: Random search screening ─────────────────────────────────────────
    print()
    print('=== STEP 2: RANDOM SEARCH SCREENING (250 candidates, seed=42) ===')
    random_top = select_top_random_descriptors(n_keep=20, seed=42)
    print(f'  Top {len(random_top)} selected. Quick chi2 survey:')
    for rank, (q_chi2, cand_id, name, basis_ids, coeffs) in enumerate(random_top[:8]):
        print(f'  #{rank+1:>2} {cand_id}: q_chi2={q_chi2:.4f}  {name[:60]}')
    print('  ...')

    # ── Build task list ─────────────────────────────────────────────────────────
    task_args = []

    # BB01-BB10 adversarial theories
    # (wid, name, k, task_type, task_data)
    adversarial = [
        ('BB01', 'LowZ Tilt (alpha=Om)',                  2, 'named_k2',  'BB01'),
        ('BB02', 'LowZ Tilt Free Alpha',                  3, 'factory_k3', (2, [-1.0, -0.5, -0.2, 0.1, 0.5, 1.0])),
        ('BB03', 'HighZ Lorentzian Suppression (z0=1)',   2, 'named_k2',  'BB03'),
        ('BB04', 'HighZ Lorentzian Free Scale',           3, 'factory_k3', (4, [0.5, 1.0, 1.5, 2.0, 3.0, 5.0])),
        ('BB05', 'BGS-Targeted Gaussian Bump',            2, 'named_k2',  'BB05'),
        ('BB06', 'HighZ Log Reduction (alpha=-Om/2)',     2, 'named_k2',  'BB06'),
        ('BB07', 'Log Tilt Free Amplitude',               3, 'factory_k3', (7, [-1.5, -1.0, -0.5, 0.0, 0.5, 1.0])),
        ('BB08', 'PullWeighted Gaussian Decay',           2, 'named_k2',  'BB08'),
        ('BB09', 'Quadratic Gaussian Decay Free Gamma',   3, 'factory_k3', (9, [0.05, 0.1, 0.2, 0.5, 1.0, 2.0])),
        ('BB10', 'Adversarial Tanh Transition',           2, 'named_k2',  'BB10'),
    ]
    for entry in adversarial:
        task_args.append(entry)

    # BB11-BB30 random search winners
    for rank, (q_chi2, cand_id, name, basis_ids, coeffs) in enumerate(random_top):
        bb_id = f'BB{11 + rank:02d}'
        task_args.append((bb_id, name[:64], 2, 'descriptor', (basis_ids, coeffs)))

    print()
    print(f'Total: {len(task_args)} theories to optimize.')
    print('Launching multiprocessing pool (9 workers max)...')
    print()

    ctx       = multiprocessing.get_context('spawn')
    n_workers = min(9, len(task_args))
    with ctx.Pool(n_workers) as pool:
        results = pool.map(worker_fn, task_args)

    # Sort by AICc
    results.sort(key=lambda r: r.get('aicc', 1e8))

    # Save JSON
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f'Saved: {json_path}')

    # Print table
    print()
    print('{:<6} {:<48} {:>2} {:>9} {:>9} {:>8} {:>6}'.format(
        'ID', 'Theory', 'k', 'chi2', 'AICc', 'dAICc', 'Status'))
    print('-' * 92)

    pass_count = 0
    kill_count = 0
    for r in results:
        chi2_str  = '{:.4f}'.format(r['chi2'])   if r.get('chi2', 1e8) < 1e7 else 'FAIL'
        aicc_str  = '{:.4f}'.format(r['aicc'])   if r.get('aicc', 1e8) < 1e7 else 'FAIL'
        daicc_str = '{:.4f}'.format(r['d_aicc']) if r.get('d_aicc', 1e8) < 1e7 else 'FAIL'
        print('{:<6} {:<48} {:>2} {:>9} {:>9} {:>8} {:>6}'.format(
            r['id'], r['name'][:48], r['k'],
            chi2_str, aicc_str, daicc_str, r['status']))
        if r['status'] == 'PASS':
            pass_count += 1
        else:
            kill_count += 1

    print()
    print(f'PASS: {pass_count}  /  KILL: {kill_count}')
    print()

    # Champion
    passed = [r for r in results if r['status'] == 'PASS']
    if passed:
        champ = passed[0]
        print('Champion: {} "{}"  chi2={:.4f}  AICc={:.4f}  dAICc={:.4f}'.format(
            champ['id'], champ['name'],
            champ['chi2'], champ['aicc'], champ['d_aicc']))
        if champ.get('Om') is not None:
            print(f"  Om={champ['Om']:.4f}  H0={champ['H0']:.4f}")
    else:
        print('No theory beat LCDM baseline.')

    return results, worst_3, pass_count, kill_count


if __name__ == '__main__':
    main()
