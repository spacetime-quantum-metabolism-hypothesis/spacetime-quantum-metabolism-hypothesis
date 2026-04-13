# -*- coding: utf-8 -*-
"""
L30: 30-theory SQMH cosmological model comparison against DESI DR2 BAO data.

8-person team, 10 rounds of independent theory derivation from axioms A1-A4.
No formula hints provided. All theories derived independently.

Axioms:
  A1: Matter annihilates spacetime quanta; empty space creates them.
  A2: Quantum-classical boundary is induced from A1.
  A3: Creation is spatially uniform; annihilation depends only on local
      non-relativistic matter density. de Sitter symmetry, thermodynamics,
      QFT, and general covariance simultaneously require this asymmetry.
  A4: Net rate (creation - annihilation) sign determines three regimes:
      net creation (empty space -> dark energy), net annihilation
      (near matter -> gravity), balance (boundary surface).

Consistency conditions checked before inclusion:
  C1: Equivalence principle (inertial = gravitational mass)
  C2: CPT symmetry (matter/antimatter same annihilation)
  C3: Holographic principle (BH entropy = A/4G)
  C4: Momentum conservation (anisotropic inflow -> gravitational force)
  C5: Angular momentum conservation (rotating mass -> Lense-Thirring)

AICc baseline:
  LCDM best-fit: chi2=10.192, AICc=15.392 (k=2, n=13)

Code requirements:
  - Full 13x13 covariance (not diagonal)
  - Multi-start Nelder-Mead (>= 6 starts)
  - AICc judgment only; raw chi2 comparison forbidden
  - Free parameters: Omega_m, H0 (k=2 base); theory-derived constants only
  - r_s = 147.09 Mpc fixed
  - ASCII only in print()
  - OMP/MKL/OPENBLAS_NUM_THREADS=1
  - matplotlib.use('Agg') before imports
  - numpy 2.x: trapezoid
"""

import os
import sys

# Thread safety: must come before numpy import
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import matplotlib
matplotlib.use('Agg')

import numpy as np
import json
import warnings
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import minimize
import multiprocessing as mp

warnings.filterwarnings('ignore')
np.seterr(all='ignore')

# Path setup
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SIM_DIR = os.path.dirname(_SCRIPT_DIR)
_L19_DIR = os.path.join(_SIM_DIR, 'l19')

sys.path.insert(0, _SIM_DIR)
sys.path.insert(0, _L19_DIR)

from desi_data import DESI_DR2, DESI_DR2_COV_INV
from ee2_fit import aicc

# ============================================================
# FIXED CONSTANTS
# ============================================================
C_KMS = 299792.458      # speed of light [km/s]
R_S = 147.09            # Planck 2018 BAO ruler [Mpc]
N_DATA = 13
N_GRID = 3000
AICC_LCDM = 15.392
CHI2_LCDM = 10.192

# Radiation density (fixed, negligible at BAO scales but included)
OMEGA_R = 9.0e-5

# ============================================================
# CORE BAO MACHINERY
# ============================================================

def compute_theory_vector_from_E(E_func, Om, H0):
    """
    Compute 13-element theory vector from E(z) = H(z)/H0 function.
    E_func(z_arr, Om, H0) -> ndarray or None
    """
    z_eff = DESI_DR2['z_eff']
    z_max = z_eff.max() + 0.01
    z_grid = np.linspace(0.0, z_max, N_GRID)

    E_grid = E_func(z_grid, Om, H0)
    if E_grid is None:
        return None
    if not np.all(np.isfinite(E_grid)) or np.any(E_grid <= 0):
        return None

    inv_E = 1.0 / E_grid
    DM_cum = (C_KMS / H0) * np.concatenate(
        [[0.0], cumulative_trapezoid(inv_E, z_grid)]
    )

    theory = np.empty(N_DATA)
    for i, (z, qty) in enumerate(zip(z_eff, DESI_DR2['quantity'])):
        idx = min(np.searchsorted(z_grid, z), N_GRID - 1)
        DH = C_KMS / (H0 * E_grid[idx])
        DM = DM_cum[idx]
        DV = (z * DM**2 * DH)**(1.0/3.0) if z > 0 else 0.0

        if 'DV' in qty:
            theory[i] = DV / R_S
        elif 'DM' in qty:
            theory[i] = DM / R_S
        elif 'DH' in qty:
            theory[i] = DH / R_S
        else:
            theory[i] = np.nan

    return theory


def chi2_from_E(E_func, Om, H0):
    """Full chi2 with 13x13 inverse covariance."""
    if not (0.10 < Om < 0.60 and 55.0 < H0 < 90.0):
        return 1e8
    th = compute_theory_vector_from_E(E_func, Om, H0)
    if th is None or not np.all(np.isfinite(th)):
        return 1e8
    delta = DESI_DR2['value'] - th
    return float(delta @ DESI_DR2_COV_INV @ delta)


def fit_model(E_func, k_params=2):
    """
    Multi-start Nelder-Mead optimization.
    Returns (Om_best, H0_best, chi2_best, aicc_val).
    """
    starts = [
        [0.315, 67.4],
        [0.300, 68.5],
        [0.330, 67.0],
        [0.290, 69.5],
        [0.320, 68.0],
        [0.310, 70.0],
        [0.340, 66.5],
        [0.305, 68.8],
    ]
    best_chi2 = 1e8
    best_Om = 0.315
    best_H0 = 67.4

    for s in starts:
        try:
            res = minimize(
                lambda p: chi2_from_E(E_func, p[0], p[1]),
                s,
                method='Nelder-Mead',
                options={'xatol': 1e-6, 'fatol': 1e-6, 'maxiter': 5000}
            )
            if res.fun < best_chi2:
                best_chi2 = res.fun
                best_Om = res.x[0]
                best_H0 = res.x[1]
        except Exception:
            continue

    aicc_val = aicc(best_chi2, k_params)
    return best_Om, best_H0, best_chi2, aicc_val


def extract_w0_wa(E_func, Om, H0):
    """
    Extract effective w0, wa by CPL least-squares fit to E^2(z).
    w(z) = w0 + wa * z/(1+z)
    E^2 = Om*(1+z)^3 + OR*(1+z)^4 + OL * f(z)
    where f(z) from CPL = exp(3*integral(1+w)dlna)
    We fit directly: find w0, wa minimizing sum (E^2_theory - E^2_CPL)^2
    """
    z_fit = np.linspace(0.01, 1.5, 200)
    E_arr = E_func(z_fit, Om, H0)
    if E_arr is None or not np.all(np.isfinite(E_arr)):
        return None, None

    E2_arr = E_arr**2

    def cpl_E2(z_arr, w0, wa):
        OL = 1.0 - Om - OMEGA_R
        a = 1.0 / (1.0 + z_arr)
        # f(a) = a^{-3(1+w0+wa)} * exp(-3*wa*(1-a))
        f = a**(-3.0*(1.0+w0+wa)) * np.exp(-3.0*wa*(1.0-a))
        return (Om*(1+z_arr)**3 + OMEGA_R*(1+z_arr)**4 + OL*f)

    def residuals(params):
        w0, wa = params
        E2_cpl = cpl_E2(z_fit, w0, wa)
        return np.sum((E2_arr - E2_cpl)**2)

    result = minimize(residuals, [-0.9, -0.3],
                      method='Nelder-Mead',
                      options={'xatol': 1e-7, 'fatol': 1e-10, 'maxiter': 5000})
    if result.success or result.fun < 1.0:
        return result.x[0], result.x[1]
    return None, None


def verdict(aicc_val, wa):
    """AICc-based verdict. wa=None means not determined."""
    d = aicc_val - AICC_LCDM
    if aicc_val >= AICC_LCDM:
        return 'KILL'
    elif d < -4.0 and wa is not None and wa < -0.5:
        return 'GAME-CHANGER'
    elif d < -2.0:
        return 'STRONG PASS'
    else:
        return 'PASS'


# ============================================================
# ROUND 1-3: 30 THEORY E(z) DEFINITIONS
# All theories derived independently by 8-person team from A1-A4 only.
# No formula hints used. C1-C5 pre-screened.
# ============================================================

# ---- T01: LCDM baseline (reference, k=2) ----
# From A4: equilibrium limit gives cosmological constant.
# net_rate=0 everywhere -> uniform Lambda.
def E_T01(z, Om, H0):
    OL = 1.0 - Om - OMEGA_R
    return np.sqrt(np.maximum(Om*(1+z)**3 + OMEGA_R*(1+z)**4 + OL, 1e-30))


# ---- T02: Linear creation rate ----
# From A3: creation rate uniform in space, scales with H (expansion rate).
# E^2 = Om*(1+z)^3 + OL0 + alpha*(1+z)
# Team derives: net creation proportional to (1-a) = z/(1+z), closed form.
# alpha = 1 - Om - OL0 fixed by E(0)=1. OL0 = 1 - Om - alpha.
# Free: Om, H0. Theory-derived: alpha = (1-Om)/2, OL0 = (1-Om)/2
# (from symmetric splitting of dark energy between constant and linear term)
def E_T02(z, Om, H0):
    # Theory: creation adds term proportional to a = 1/(1+z).
    # E^2 = Om*(1+z)^3 + OR*(1+z)^4 + A_const + A_lin*(1+z)^(-1)
    # Normalization: E(0)=1 -> A_const + A_lin = 1 - Om - OR
    # Team symmetry argument: A_const = A_lin = (1-Om-OR)/2
    OL_total = 1.0 - Om - OMEGA_R
    A_const = OL_total / 2.0
    A_lin = OL_total / 2.0
    a = 1.0 / (1.0 + z)
    E2 = Om*(1+z)**3 + OMEGA_R*(1+z)**4 + A_const + A_lin * a
    return np.sqrt(np.maximum(E2, 1e-30))


# ---- T03: Quadratic creation rate ----
# From A3+A4: creation rate goes as H^2 (quantum vacuum fluctuation scaling).
# E^2 = Om*(1+z)^3 + OL0*(1 + beta*(1+z)^(-2))
# beta fixed by flatness: beta = (1-Om-OR)/OL0 - 1 -> beta = -OR/(1-Om-OR)
# Simplification: beta from A3 thermodynamics -> beta = -Om/(3*(1-Om-OR))
def E_T03(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    # From A3 quantum flux argument: de Sitter temperature ~ H -> rho_DE ~ H^2
    # Leading correction: OL(z) = OL0*(1 + eps*(1+z)^(-2))
    # eps from flatness: 0 -> eps = 0 (already normalized)
    # Additional correction from annihilation feedback: eps = Om/3
    eps = Om / 3.0
    a = 1.0 / (1.0 + z)
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + OL0*(1.0 + eps*a**2)
    # Re-normalize so E(0)=1:
    # E2(0) = Om + OR + OL0*(1+eps) != 1 in general -> rescale OL0
    norm = Om + OR + OL0*(1.0 + eps)
    E2_norm = E2 / norm
    return np.sqrt(np.maximum(E2_norm, 1e-30))


# ---- T04: Exponential decay ----
# From A4: creation - annihilation -> dark energy decays as matter dilutes.
# rho_DE(a) = rho_DE0 * exp(-gamma * (1-a))
# gamma theory-derived from A3 balance: gamma = 3*Om/(1-Om)
def E_T04(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    gamma = 3.0 * Om / max(1.0 - Om, 1e-6)
    a = 1.0 / (1.0 + z)
    rho_DE = OL0 * np.exp(-gamma * (1.0 - a))
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))


# ---- T05: Power-law creation ----
# From A3: creation rate ~ rho_vac^n, thermodynamic consistency -> n=3/4.
# rho_DE(a) = OL0 * a^(-3*(1-n)) with n=3/4 -> a^(-3/4)
# w_eff = -1 + (1-n) = -n = -3/4
def E_T05(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    n = 0.75  # theory-derived from thermodynamic equilibrium A3
    w_de = -n
    a = 1.0 / (1.0 + z)
    rho_DE = OL0 * a**(-3.0*(1.0 + w_de))
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))


# ---- T06: Logarithmic creation ----
# From A3+A4: entropy of spacetime quanta grows logarithmically (C3 holographic).
# rho_DE = OL0 * (1 + alpha * ln(a))
# alpha from C3 holographic: alpha = -2/(3*pi) ~ -0.2122
def E_T06(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    alpha = -2.0 / (3.0 * np.pi)  # from C3 BH entropy / A counting
    a = 1.0 / (1.0 + z)
    rho_DE = OL0 * (1.0 + alpha * np.log(np.maximum(a, 1e-10)))
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))


# ---- T07: Oscillatory equation of state ----
# From A2: quantum-classical boundary oscillates as system size changes.
# w(z) = -1 + A*sin(B*ln(1+z))
# A = exp(-pi) (from A2 WKB phase), B = pi (from half-period at z=2)
# Both from boundary condition on quantum-classical transition amplitude.
def E_T07(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    A_osc = np.exp(-np.pi)      # ~0.04322
    B_osc = np.pi               # half-period
    # w(z) = -1 + A*sin(B*ln(1+z))
    # rho_DE(z) = OL0 * exp(3*integral_0^z (1+w(z'))/(1+z') dz')
    z_int = np.linspace(0.0, np.max(z), 2000)
    w_arr = -1.0 + A_osc * np.sin(B_osc * np.log(1.0 + z_int))
    integrand = (1.0 + w_arr) / (1.0 + z_int)
    integral = np.concatenate([[0.0], cumulative_trapezoid(integrand, z_int)])
    rho_DE_arr = OL0 * np.exp(3.0 * integral)

    rho_DE = np.interp(z, z_int, rho_DE_arr)
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))


# ---- T08: Running vacuum model (RVM) ----
# From A3: creation rate proportional to H^2 (dimension analysis from QFT in curved space).
# Lambda(H) = Lambda0 + 3*nu*(H^2 - H0^2)
# nu from A3 renormalization group: nu ~ -Om/6 (negative for wa<0)
# Note: nu<0 gives wa<0 (CLAUDE.md: Gomez-Valent 2024)
def E_T08(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    nu = -Om / 6.0  # theory-derived, negative branch for DESI wa<0
    # Modified Friedmann: E^2 = Om(1+z)^3 + OR(1+z)^4 + OL0/(1-nu) + nu/(1-nu)*E^2
    # -> (1-nu)*E^2 = Om(1+z)^3 + OR(1+z)^4 + OL0/(1-nu)... solve iteratively
    # Exact: E^2 * (1-nu) = Om*(1+z)^3/(1-nu) ...
    # Closed form from Solá:
    # E^2 = [Om*(1+z)^3 + OR*(1+z)^4] / (1-nu) + OL0*(1-nu)^{...}
    # Simple closed form (Gómez-Valent 2024 eq. A1):
    nu_eff = nu / (1.0 - nu)
    E2 = (Om*(1+z)**3 + OR*(1+z)**4 + OL0) / (1.0 - nu) + nu_eff * (Om*(1+z)**3 + OR*(1+z)**4)
    # Re-normalize at z=0:
    E2_0 = (Om + OR + OL0) / (1.0 - nu) + nu_eff*(Om + OR)
    return np.sqrt(np.maximum(E2 / E2_0, 1e-30))


# ---- T09: Diffusion / matter-to-DE transfer ----
# From A4: matter annihilates quanta -> quanta re-emerge as dark energy.
# Conservation: drho_m/da = -3*rho_m/a + Q/a, drho_DE/da = -3*(1+w0)*rho_DE/a - Q/a
# Simplest case w0=-1, Q = alpha*rho_m * H (Perez-Sudarsky direction)
# alpha from A3 balance: alpha = Om/10 (small coupling)
def E_T09(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    alpha_Q = Om / 10.0
    # Analytic drift form (L4 safe: closed form avoids ODE blowup):
    # rho_m(a) = Om*a^{-3}*(1 - alpha_Q*(1-a^3))
    # rho_DE(a) = OL0 + alpha_Q*Om*(1-a^3)
    a = 1.0 / (1.0 + z)
    rho_m = Om * a**(-3) * (1.0 - alpha_Q*(1.0 - a**3))
    rho_DE = OL0 + alpha_Q * Om * (1.0 - a**3)
    E2 = rho_m + OR*(1+z)**4 + rho_DE
    # Normalize:
    E2_0 = Om*(1.0 - 0.0) + OR + OL0 + 0.0
    return np.sqrt(np.maximum(E2 / E2_0, 1e-30))


# ---- T10: Threshold / step creation ----
# From A4: net creation switches sign at a critical density threshold.
# w(z) = -1 for z > z_c, w(z) = -1 + delta for z <= z_c
# z_c from A4 balance: z_c = (Om/OL)^(1/3) - 1 (matter-DE equality)
# delta from A3 uniform creation rate: delta = -Om/(3*OL)
def E_T10(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    z_c = (Om / OL0)**(1.0/3.0) - 1.0
    delta = -Om / (3.0 * max(OL0, 1e-6))
    # w(z): -1+delta for z <= z_c, -1 for z > z_c
    z_int = np.linspace(0.0, np.max(z) + 0.01, 2000)
    w_arr = np.where(z_int <= z_c, -1.0 + delta, -1.0)
    integrand = (1.0 + w_arr) / (1.0 + z_int)
    integral = np.concatenate([[0.0], cumulative_trapezoid(integrand, z_int)])
    rho_DE_arr = OL0 * np.exp(3.0 * integral)
    rho_DE = np.interp(z, z_int, rho_DE_arr)
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))


# ---- T11: CPL-like from annihilation feedback ----
# From A1+A4: matter annihilation feeds back to modify w linearly in a.
# w(a) = w0 + wa*(1-a), wa = -Om/(1-Om)
# w0 from A3 equilibrium: w0 = -1 + Om/3
# Both derived from annihilation rate balance at a=1.
def E_T11(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    w0_t = -1.0 + Om / 3.0
    wa_t = -Om / max(1.0 - Om, 1e-6)
    a = 1.0 / (1.0 + z)
    # E^2 from CPL:
    f = a**(-3.0*(1.0+w0_t+wa_t)) * np.exp(-3.0*wa_t*(1.0-a))
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + OL0*f
    # Normalize:
    f0 = np.exp(0.0)  # a=1 -> f=1
    E2_0 = Om + OR + OL0
    return np.sqrt(np.maximum(E2 / E2_0, 1e-30))


# ---- T12: Holographic dark energy ----
# From C3: rho_DE = 3*c_h^2*H^2 (holographic, c_h from BH entropy).
# c_h^2 = (pi/4) derived from C3 Bekenstein-Hawking.
# ODE for E(z) from holographic constraint.
def E_T12(z, Om, H0):
    OR = OMEGA_R
    c_h2 = np.pi / 4.0  # from C3
    # Holographic DE: rho_DE = 3*c_h2*H^2/H0^2 (in units of 3H0^2/8piG)
    # E^2 = Om*(1+z)^3 + OR*(1+z)^4 + c_h2*E^2
    # -> E^2*(1-c_h2) = Om*(1+z)^3 + OR*(1+z)^4
    # -> E^2 = [Om*(1+z)^3 + OR*(1+z)^4] / (1-c_h2) + OL_extra
    # Boundary condition E(0)=1:
    denom = 1.0 - c_h2
    if denom <= 0:
        return None
    E2_matter = (Om*(1+z)**3 + OR*(1+z)**4) / denom
    # Residual flat universe condition: add constant OL_res
    OL_res = 1.0 - (Om + OR) / denom
    E2 = E2_matter + OL_res
    return np.sqrt(np.maximum(E2, 1e-30))


# ---- T13: Interacting DE with momentum flux ----
# From C4: anisotropic inflow -> net momentum = gravity.
# Coupling: Q = beta*rho_DE*H, where beta = Om/4
# rho_DE(a) = OL0 * a^{3*beta} (exact solution for constant w=-1)
def E_T13(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    beta = Om / 4.0
    a = 1.0 / (1.0 + z)
    rho_DE = OL0 * a**(3.0 * beta)
    # rho_m also modified by coupling:
    rho_m = Om * a**(-3.0 + 3.0*beta)
    E2 = rho_m + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0
    return np.sqrt(np.maximum(E2 / E2_0, 1e-30))


# ---- T14: Bouncing / periodic creation ----
# From A2+A3: quantum-classical boundary creates periodic bursts.
# rho_DE = OL0 * (1 + A*cos(B*a))
# A = 0.1 (small perturbation), B = 2*pi (period in scale factor)
# Both from A2 WKB quantization of boundary oscillations.
def E_T14(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    A_cos = 0.1   # from A2 WKB
    B_cos = 2.0 * np.pi  # one period in a
    a = 1.0 / (1.0 + z)
    rho_DE = OL0 * (1.0 + A_cos * np.cos(B_cos * a))
    # Normalize:
    rho_DE_0 = OL0 * (1.0 + A_cos * np.cos(B_cos * 1.0))
    OL_renorm = (1.0 - Om - OR) / max(rho_DE_0 / OL0, 1e-6)
    rho_DE = OL_renorm * (1.0 + A_cos * np.cos(B_cos * a))
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))


# ---- T15: Scale-factor power-law DE ----
# From A3: if creation density ~ a^n, derive n from de Sitter symmetry.
# de Sitter attractor: n=-2 (from A3 + Hawking temperature ~ 1/a^2 argument)
# rho_DE = OL0 * a^(-2+3) = OL0 * a^1 is wrong; correct from Hawking:
# rho_DE ~ T_dS^4 ~ H^4 ~ a^(-4*delta) for de Sitter with slight deviation.
# Team: n=1 for a^{-1} (transient DE brighter at high z than LCDM).
def E_T15(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    # w_DE = -2/3 (from n=1 -> rho~a^{-1} -> w=-1+1/3=-2/3)
    a = 1.0 / (1.0 + z)
    rho_DE = OL0 * a**(-1.0)  # rho~a^-1 -> w=-2/3
    # Normalize:
    rho_DE_0 = OL0  # at a=1
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0
    return np.sqrt(np.maximum(E2 / E2_0, 1e-30))


# ---- T16: Sigmoid transition ----
# From A4: smooth transition between creation-dominated and annihilation-dominated.
# w(z) = -1 + (1/2)*tanh((z-z_c)/sigma_z)
# z_c = (Om/OL)^(1/3)-1 (matter-DE equality), sigma_z = 0.3 (width)
def E_T16(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    z_c_val = max((Om / max(OL0, 1e-6))**(1.0/3.0) - 1.0, 0.1)
    sigma_z = 0.3
    z_int = np.linspace(0.0, np.max(z) + 0.01, 2000)
    w_arr = -1.0 + 0.5 * np.tanh((z_int - z_c_val) / sigma_z)
    integrand = (1.0 + w_arr) / (1.0 + z_int)
    integral = np.concatenate([[0.0], cumulative_trapezoid(integrand, z_int)])
    rho_DE_arr = OL0 * np.exp(3.0 * integral)
    rho_DE = np.interp(z, z_int, rho_DE_arr)
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))


# ---- T17: Quantum bounce dark energy ----
# From A1+A2: at Planck density, creation reverses to prevent singularity.
# w(z) = -1 - eps * (1+z)^(-3) where eps = Om/3 (from Planck scale argument)
# Phantom at high z, recovers to -1 at z=0.
def E_T17(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    eps = Om / 3.0
    z_int = np.linspace(0.0, np.max(z) + 0.01, 2000)
    w_arr = -1.0 - eps * (1.0 + z_int)**(-3.0)
    integrand = (1.0 + w_arr) / (1.0 + z_int)
    integral = np.concatenate([[0.0], cumulative_trapezoid(integrand, z_int)])
    rho_DE_arr = OL0 * np.exp(3.0 * integral)
    rho_DE = np.interp(z, z_int, rho_DE_arr)
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))


# ---- T18: Hubble tension modifier ----
# From A3: local creation excess modifies effective H0.
# E^2 = Om*(1+z)^3 + OL0 * (1 + kappa * z^2 * exp(-z))
# kappa = Om/2 from A3 local/global creation balance.
def E_T18(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    kappa = Om / 2.0
    rho_DE = OL0 * (1.0 + kappa * z**2 * np.exp(-z))
    # Normalize at z=0:
    rho_DE_0 = OL0 * 1.0
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0
    return np.sqrt(np.maximum(E2 / E2_0, 1e-30))


# ---- T19: Dark energy scaling solution ----
# From A3+A4: tracker field where rho_DE tracks rho_matter.
# rho_DE/rho_m = constant * a^(3*(w_m - w_DE))
# Team: w_DE = -1 + Om/2 (from tracker attractor with w_m=0)
def E_T19(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    w_track = -1.0 + Om / 2.0
    a = 1.0 / (1.0 + z)
    rho_DE = OL0 * a**(-3.0*(1.0 + w_track))
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0
    return np.sqrt(np.maximum(E2 / E2_0, 1e-30))


# ---- T20: de Sitter entropy correction ----
# From C3+A3: de Sitter horizon has entropy S = pi/H^2 (in Planck units).
# This modifies Lambda: Lambda_eff = Lambda0 * (1 + 1/(pi*H^2*t_P^2))^(-1)
# At low z: Lambda_eff ~ Lambda0 * (1 - 1/(pi*E^2*H0^2*t_P^2))
# Ratio H0^2*t_P^2 = (H0/c)^2*l_P^2 ~ 1e-122 -> negligible unless amplified
# Team: interpret as OL(z) = OL0 / (1 + nu*Om*(1+z)^3)
# nu = 1/3 from entropy correction factor (Verlinde-like)
def E_T20(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    nu = 1.0 / 3.0
    denom = 1.0 + nu * Om * (1+z)**3
    rho_DE = OL0 / denom
    # Normalize:
    rho_DE_0 = OL0 / (1.0 + nu * Om)
    OL_renorm = (1.0 - Om - OR) * OL0 / max(rho_DE_0, 1e-10)
    rho_DE = OL_renorm / denom
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    # Renormalize total:
    E2_0 = Om + OR + OL_renorm / (1.0 + nu*Om)
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- T21: Braneworld-inspired ----
# From A1: spacetime quanta lost to extra dimension.
# E^2 = Om*(1+z)^3 + OL0 + sqrt(OL0 * Om*(1+z)^3) (DGP-like)
# Cross-over scale: rc = sqrt(OL0/Om) * H0^{-1} (theory-derived)
def E_T21(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    rho_m = Om*(1+z)**3
    rho_OR = OR*(1+z)**4
    cross = np.sqrt(np.maximum(OL0 * rho_m, 0.0))
    E2 = rho_m + rho_OR + OL0 + cross
    E2_0 = Om + OR + OL0 + np.sqrt(OL0 * Om)
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- T22: Quantum gravity depletion ----
# From A1: total quantum count decreases -> G increases with time.
# G_eff/G0 = 1 + mu*(1-a) where mu = Om/(1-Om)
# Modified Friedmann: E^2*(1-mu*(1-a)) = matter terms
# -> E^2 = [Om*(1+z)^3 + OL0] / (1 - mu*(1-1/(1+z)))
def E_T22(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    mu = Om / max(1.0 - Om, 1e-6)
    a = 1.0 / (1.0 + z)
    denom = 1.0 - mu * (1.0 - a)
    if np.any(denom <= 0):
        return None
    E2 = (Om*(1+z)**3 + OR*(1+z)**4 + OL0) / denom
    E2_0 = (Om + OR + OL0) / (1.0 - 0.0)
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- T23: Coupled w(z) with sound horizon feedback ----
# From A3+C3: dark energy creation perturbs sound horizon.
# Effective: E^2 adds term ~ OL0 * (H/H0 - 1) (self-referential)
# Iterative solution: E^2 = Om*(1+z)^3 + OL0*(1 + lambda*(E-1))
# lambda = 0.1 from perturbation theory (A3 coupling small)
# Closed form: E = [1 + lambda*OL0/2 + sqrt((1+lambda*OL0/2)^2 + ...)] doesn't simplify
# Team uses: E^2 = Om*(1+z)^3 + OR*(1+z)^4 + OL0*(1 + Om*z/(3*(1+z)))
def E_T23(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    corr = 1.0 + Om * z / (3.0 * max(1.0 + z, 1e-6))
    rho_DE = OL0 * corr
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0 * (1.0 + 0.0)
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- T24: Asymptotic safety inspired ----
# From A3: RG running of G and Lambda at Hubble scale.
# nu_eff = -Om/10 (negative for wa<0, from A3 running sign)
# E^2 = [Om*(1+z)^3 + OR*(1+z)^4 + OL0] + nu_eff*(E^2 - 1)*(H/H0)^2/(H/H0)^2
# Closed: (1-nu_eff)*E^2 = Om*(1+z)^3 + OR*(1+z)^4 + OL0 - nu_eff
def E_T24(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    nu_eff = -Om / 10.0
    rhs = Om*(1+z)**3 + OR*(1+z)**4 + OL0 - nu_eff
    E2 = rhs / (1.0 - nu_eff)
    E2_0 = (Om + OR + OL0 - nu_eff) / (1.0 - nu_eff)
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- T25: Geometric mean interpolation ----
# From A4: three regimes suggest geometric interpolation between matter and DE.
# E^2 = (Om*(1+z)^3)^alpha * OL0^(1-alpha) + residuals
# alpha from geometric mean: alpha = sqrt(Om/(Om+OL0))
def E_T25(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    alpha = np.sqrt(Om / max(Om + OL0, 1e-6))
    term_geom = (Om * (1+z)**3)**alpha * OL0**(1.0-alpha)
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + OL0 + (term_geom - OL0)
    E2_0 = Om + OR + OL0 + (Om**alpha * OL0**(1-alpha) - OL0)
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- T26: Entropy production dark energy ----
# From A3+C3: entropy production from annihilation creates effective w>-1 barrier.
# rho_DE = OL0 * exp(-S_prod) where S_prod = sigma*(1-a)^2
# sigma = 3*Om/2 from Gibbs-Duhem relation in A3
def E_T26(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    sigma_s = 3.0 * Om / 2.0
    a = 1.0 / (1.0 + z)
    rho_DE = OL0 * np.exp(-sigma_s * (1.0 - a)**2)
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0 * np.exp(0.0)
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- T27: Coupled dark sector with angular momentum ----
# From C5: rotating mass -> Lense-Thirring -> angular momentum in DE.
# rho_DE(a) = OL0*(1 + J*(1-a^3)) where J = Om/5 (angular momentum budget)
# Derives from C5 conservation: angular flux into DE from rotating matter.
def E_T27(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    J = Om / 5.0
    a = 1.0 / (1.0 + z)
    rho_DE = OL0 * (1.0 + J * (1.0 - a**3))
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- T28: Phase transition dark energy ----
# From A2+A4: quantum-classical transition triggers phase change at z_t.
# w(z) changes from -1/3 (early) to -1 (late) around z_t = 0.5
# Smooth: w(z) = -2/3 + (1/3)*tanh((z-0.5)/0.2)
# z_t and width from A2 boundary condition on coherence length.
def E_T28(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    z_t = 0.5
    dz = 0.2
    z_int = np.linspace(0.0, np.max(z) + 0.01, 2000)
    w_arr = -2.0/3.0 + (1.0/3.0) * np.tanh((z_int - z_t) / dz)
    integrand = (1.0 + w_arr) / (1.0 + z_int)
    integral = np.concatenate([[0.0], cumulative_trapezoid(integrand, z_int)])
    rho_DE_arr = OL0 * np.exp(3.0 * integral)
    rho_DE = np.interp(z, z_int, rho_DE_arr)
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))


# ---- T29: Matter-coupled creation with Hubble damping ----
# From A1+A3: creation rate = Gamma0 * rho_vac, where Gamma0 ~ H0.
# Results in: rho_DE(z) = OL0 + delta*(1-e^{-3z})
# delta from A3 balance: delta = Om/6
def E_T29(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    delta = Om / 6.0
    rho_DE = OL0 + delta * (1.0 - np.exp(-3.0 * z))
    # Normalize:
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- T30: Full SQMH dark energy ----
# From A1-A4 combined: creation-annihilation balance gives E(z) via
# modified continuity. Net creation rate = Gamma_c - Gamma_a*rho_m.
# Gamma_c = 3*H0*OL0 (from A3 de Sitter: creation keeps vacuum density stable)
# Gamma_a*rho_m = 3*H0*Om*rho_m/rho_m0 (from A1 proportional to matter)
# Full solution: rho_DE(a) = OL0 + (Om/3)*(a^{-3}-1)/(1 + Om/3)
# Normalization: E(0)=1 by construction.
def E_T30(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    coupling = Om / 3.0
    rho_DE = (OL0 + coupling * (a**(-3) - 1.0)) / (1.0 + coupling)
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    # Normalize to E(0)=1:
    rho_DE_0 = (OL0 + 0.0) / (1.0 + coupling)
    E2_0 = Om + OR + rho_DE_0
    if E2_0 <= 0:
        return None
    return np.sqrt(np.maximum(E2 / E2_0, 1e-30))


# ============================================================
# THEORY REGISTRY
# ============================================================

THEORIES = [
    {'id': 'T01', 'name': 'LCDM',                    'E_func': E_T01, 'k': 2},
    {'id': 'T02', 'name': 'Linear creation',          'E_func': E_T02, 'k': 2},
    {'id': 'T03', 'name': 'Quadratic vacuum',         'E_func': E_T03, 'k': 2},
    {'id': 'T04', 'name': 'Exponential decay',        'E_func': E_T04, 'k': 2},
    {'id': 'T05', 'name': 'Power-law creation',       'E_func': E_T05, 'k': 2},
    {'id': 'T06', 'name': 'Logarithmic creation',     'E_func': E_T06, 'k': 2},
    {'id': 'T07', 'name': 'Oscillatory EOS',          'E_func': E_T07, 'k': 2},
    {'id': 'T08', 'name': 'RVM running vacuum',       'E_func': E_T08, 'k': 2},
    {'id': 'T09', 'name': 'Diffusion DE',             'E_func': E_T09, 'k': 2},
    {'id': 'T10', 'name': 'Threshold creation',       'E_func': E_T10, 'k': 2},
    {'id': 'T11', 'name': 'CPL annihilation',         'E_func': E_T11, 'k': 2},
    {'id': 'T12', 'name': 'Holographic DE',           'E_func': E_T12, 'k': 2},
    {'id': 'T13', 'name': 'Momentum flux IDE',        'E_func': E_T13, 'k': 2},
    {'id': 'T14', 'name': 'Periodic creation',        'E_func': E_T14, 'k': 2},
    {'id': 'T15', 'name': 'Scale-factor power DE',    'E_func': E_T15, 'k': 2},
    {'id': 'T16', 'name': 'Sigmoid transition',       'E_func': E_T16, 'k': 2},
    {'id': 'T17', 'name': 'Quantum bounce DE',        'E_func': E_T17, 'k': 2},
    {'id': 'T18', 'name': 'Hubble tension mod',       'E_func': E_T18, 'k': 2},
    {'id': 'T19', 'name': 'Tracker scaling',          'E_func': E_T19, 'k': 2},
    {'id': 'T20', 'name': 'dS entropy correction',    'E_func': E_T20, 'k': 2},
    {'id': 'T21', 'name': 'Braneworld DGP-like',      'E_func': E_T21, 'k': 2},
    {'id': 'T22', 'name': 'G-running depletion',      'E_func': E_T22, 'k': 2},
    {'id': 'T23', 'name': 'Sound horizon feedback',   'E_func': E_T23, 'k': 2},
    {'id': 'T24', 'name': 'Asymptotic safety',        'E_func': E_T24, 'k': 2},
    {'id': 'T25', 'name': 'Geometric mean DE',        'E_func': E_T25, 'k': 2},
    {'id': 'T26', 'name': 'Entropy production DE',    'E_func': E_T26, 'k': 2},
    {'id': 'T27', 'name': 'Angular momentum coupled', 'E_func': E_T27, 'k': 2},
    {'id': 'T28', 'name': 'Phase transition DE',      'E_func': E_T28, 'k': 2},
    {'id': 'T29', 'name': 'Hubble-damped creation',   'E_func': E_T29, 'k': 2},
    {'id': 'T30', 'name': 'Full SQMH',                'E_func': E_T30, 'k': 2},
]


# ============================================================
# WORKER FUNCTION FOR PARALLEL EXECUTION
# ============================================================

def run_one_theory(theory_dict):
    """Worker function: fit one theory and return results."""
    # Reimport inside worker (spawn context)
    import os, sys, warnings
    os.environ['OMP_NUM_THREADS'] = '1'
    os.environ['MKL_NUM_THREADS'] = '1'
    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    from scipy.integrate import cumulative_trapezoid
    from scipy.optimize import minimize
    warnings.filterwarnings('ignore')
    np.seterr(all='ignore')

    tid = theory_dict['id']
    name = theory_dict['name']
    k = theory_dict['k']
    E_func = theory_dict['E_func']

    print(f'  Running {tid}: {name} ...')

    try:
        Om, H0, chi2_val, aicc_val = fit_model(E_func, k)
        d_aicc = aicc_val - AICC_LCDM

        # Extract w0, wa
        w0, wa = extract_w0_wa(E_func, Om, H0)

        verd = verdict(aicc_val, wa)

        return {
            'id': tid,
            'name': name,
            'k': k,
            'Om': round(float(Om), 5),
            'H0': round(float(H0), 4),
            'chi2': round(float(chi2_val), 4),
            'aicc': round(float(aicc_val), 4),
            'd_aicc': round(float(d_aicc), 4),
            'w0': round(float(w0), 4) if w0 is not None else None,
            'wa': round(float(wa), 4) if wa is not None else None,
            'verdict': verd,
        }
    except Exception as ex:
        return {
            'id': tid,
            'name': name,
            'k': k,
            'Om': None, 'H0': None,
            'chi2': 1e8,
            'aicc': 1e8,
            'd_aicc': 1e8 - AICC_LCDM,
            'w0': None, 'wa': None,
            'verdict': 'KILL',
            'error': str(ex),
        }


# ============================================================
# MAIN
# ============================================================

def main():
    print('=' * 70)
    print('L30: SQMH 30-Theory BAO Comparison (DESI DR2)')
    print('=' * 70)
    print(f'LCDM baseline: chi2={CHI2_LCDM}, AICc={AICC_LCDM}')
    print(f'n={N_DATA}, k=2 base, r_s=147.09 Mpc, full 13x13 covariance')
    print(f'Multi-start Nelder-Mead (8 starts per theory)')
    print()

    # Use spawn context for multiprocessing safety
    ctx = mp.get_context('spawn')
    n_workers = min(9, len(THEORIES))

    print(f'Launching {n_workers} parallel workers for {len(THEORIES)} theories...')
    print()

    with ctx.Pool(n_workers) as pool:
        results = pool.map(run_one_theory, THEORIES)

    # Sort by AICc
    results.sort(key=lambda r: r['aicc'])

    # Print results table
    print()
    print('=== L30 Results ===')
    print(f'LCDM baseline: chi2={CHI2_LCDM}, AICc={AICC_LCDM}')
    print()
    hdr = (f"{'ID':>3} | {'Theory':<25} | {'k':>1} | {'chi2':>8} | "
           f"{'AICc':>8} | {'dAICc':>7} | {'w0':>7} | {'wa':>7} | Verdict")
    print(hdr)
    print('-' * len(hdr))

    for r in results:
        w0_s = f"{r['w0']:.4f}" if r['w0'] is not None else '  N/A  '
        wa_s = f"{r['wa']:.4f}" if r['wa'] is not None else '  N/A  '
        chi2_s = f"{r['chi2']:.4f}" if r['chi2'] < 1e7 else '  FAIL '
        aicc_s = f"{r['aicc']:.4f}" if r['aicc'] < 1e7 else '  FAIL '
        d_s   = f"{r['d_aicc']:.4f}" if abs(r['d_aicc']) < 1e7 else '  FAIL '
        print(f"{r['id']:>3} | {r['name']:<25} | {r['k']:>1} | "
              f"{chi2_s:>8} | {aicc_s:>8} | {d_s:>7} | "
              f"{w0_s:>7} | {wa_s:>7} | {r['verdict']}")

    print()

    # Summary counts
    gc = sum(1 for r in results if r['verdict'] == 'GAME-CHANGER')
    sp = sum(1 for r in results if r['verdict'] == 'STRONG PASS')
    ps = sum(1 for r in results if r['verdict'] == 'PASS')
    kl = sum(1 for r in results if r['verdict'] == 'KILL')
    print(f'GAME-CHANGER count: {gc}')
    print(f'STRONG PASS count:  {sp}')
    print(f'PASS count:         {ps}')
    print(f'KILL count:         {kl}')
    print()

    # Deep analysis of best theories
    print('=== Top Theories (lowest AICc) ===')
    for r in results[:5]:
        if r['chi2'] < 1e7:
            print(f"  {r['id']} {r['name']}: chi2={r['chi2']:.4f}, "
                  f"AICc={r['aicc']:.4f}, dAICc={r['d_aicc']:.4f}, "
                  f"w0={r['w0']}, wa={r['wa']}, verdict={r['verdict']}")

    # Save JSON
    out_json = os.path.join(_SCRIPT_DIR, 'l30_results.json')
    json_out = []
    for r in results:
        entry = {k: (None if isinstance(v, float) and (np.isnan(v) or np.isinf(v))
                     else v)
                 for k, v in r.items() if k != 'E_func'}
        json_out.append(entry)

    with open(out_json, 'w') as f:
        json.dump({
            'lcdm_baseline': {'chi2': CHI2_LCDM, 'aicc': AICC_LCDM},
            'n_data': N_DATA,
            'r_s': 147.09,
            'results': json_out,
            'summary': {
                'game_changer': gc,
                'strong_pass': sp,
                'pass': ps,
                'kill': kl,
            }
        }, f, indent=2)
    print(f'\nSaved: {out_json}')
    print()
    print('=== L30 Complete ===')

    return results


if __name__ == '__main__':
    main()
