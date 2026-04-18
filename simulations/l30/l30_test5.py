# -*- coding: utf-8 -*-
"""
l30_test5.py -- L30 5th Run SQMH Fresh Theories (Z01-Z30)
==========================================================
30 new theories derived from SQMH axioms A1-A4 + C1-C3.
COMPLETELY different mechanisms from V, W, X, Y series.

Explored NEW directions (functional forms):
- Power-law corrections to LCDM from A1 annihilation rate
- Logarithmic corrections from quantum gravity of SQ field
- Polynomial dark energy from SQ density moments
- Rational function dark energy (Pade approximants)
- Exponential integral dark energy
- Trigonometric dark energy from SQ wave modes
- Hyperbolic function dark energy from SQ potential
- Bessel function dark energy from cylindrical void geometry
- Elliptic function dark energy from SQ lattice
- Error function (erf) dark energy from diffusion boundary layer

LCDM baseline: chi2=10.192, AICc=15.392 (k=2, n=13)
AICc(k=2): need chi2 < 10.192 to beat LCDM
AICc(k=3): need chi2 < 6.73
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
from scipy.special import erf, erfc, i0, i1, k0, k1

warnings.filterwarnings('ignore')
np.seterr(all='ignore')

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


def aicc(chi2_val, k, n=N_DATA):
    return chi2_val + 2*k + 2*k*(k+1)/(n - k - 1)


def compute_theory_vector(Omega_m, H0, E_func):
    """Generic BAO theory vector given E(z) callable."""
    z_eff = DESI_DR2['z_eff']
    z_max = z_eff.max() + 0.01
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

    inv_E = 1.0 / E_grid
    DM_cum = (C_KMS / H0) * np.concatenate(
        [[0.0], cumulative_trapezoid(inv_E, z_grid)]
    )

    theory_vec = np.empty(N_DATA)
    for i, (z, qty) in enumerate(zip(z_eff, DESI_DR2['quantity'])):
        idx = min(np.searchsorted(z_grid, z), N_GRID - 1)
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
    Omega_m = params[0]
    H0      = params[1]

    if not (0.05 < Omega_m < 0.70 and 50.0 < H0 < 100.0):
        return 1e8

    th = compute_theory_vector(Omega_m, H0, E_func)
    if th is None or not np.all(np.isfinite(th)):
        return 1e8
    delta = DESI_DR2['value'] - th
    return float(delta @ DESI_DR2_COV_INV @ delta)


# ==============================================================================
# THEORY DEFINITIONS (Z01-Z30)
# Each E_func signature: E_func(z_array, Omega_m) -> E_array
# ==============================================================================

# ── DIRECTION 1: Power-law corrections from A1 annihilation rate ──────────────

# Z01: Annihilation Rate Power-Law SQ DE (k=2)
# A1+A4: Matter annihilation rate scales as rho_m^(4/3) (SQ lattice saturation).
# The 4/3 exponent arises from 3D annihilation geometry (A1): each matter quantum
# contacts 4/3 * pi * r^3 volume of SQ lattice.
# rho_DE = OL0 * (1 + A1_pl * (Om*(1+z)^3)^(1/3)) / (1 + A1_pl * Om^(1/3))
# A1_pl = 1/(4*pi/3)^(1/3) = (3/(4pi))^(1/3): geometric packing factor.
# k=2
def Z01_E(z_arr, Om):
    A1_pl = (3.0 / (4.0 * math.pi))**(1.0/3.0)   # geometric packing factor
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    num  = 1.0 + A1_pl * (Om * (1+z_arr)**3)**(1.0/3.0)
    den0 = 1.0 + A1_pl * Om**(1.0/3.0)
    rho_DE = OL0 * num / den0
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Z02: Annihilation Rate Sqrt Correction SQ DE (k=2)
# A1+A4: SQ generation outpaces annihilation in low-density regions by sqrt law.
# A3 (uniform generation) vs A1 (local annihilation ~ rho_m):
# net rate = Gamma_gen - Gamma_ann ~ OL0 - sqrt(Om * OL0) * (1+z)^(3/2).
# rho_DE decays as: rho_DE = OL0 * exp(-sqrt(Om/OL0) * ((1+z)^(3/2) - 1)).
# A_sqrt = sqrt(Om/OL0) evaluated at fiducial. Fixed by Om/OL0 ratio (A1+A3).
# k=2
def Z02_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    A_sqrt = math.sqrt(Om / OL0)
    rho_DE = OL0 * np.exp(-A_sqrt * ((1+z_arr)**1.5 - 1.0))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Z03: Power-law exponent free (k=3)
# A1+A4: The annihilation-rate power-law exponent alpha is free.
# rho_DE = OL0 * exp(-A_pl * ((1+z)^alpha - 1)) with A_pl=sqrt(Om/OL0). k=3.
def Z03_E_factory(alpha):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0 or alpha <= 0:
            return None
        A_pl = math.sqrt(Om / OL0)
        rho_DE = OL0 * np.exp(-A_pl * ((1+z_arr)**alpha - 1.0))
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 2: Logarithmic corrections from SQ quantum gravity ──────────────

# Z04: Quantum Gravity Log Correction SQ DE (k=2)
# A1+A2: Quantum-classical boundary (A2) introduces loop-level log corrections.
# Loop expansion: rho_DE = OL0 * (1 + alpha_QG * ln(1 + Om*(1+z)^3 / OL0))
# alpha_QG = -1/(4*pi^2): one-loop coefficient from SQ field renormalization.
# At z=0: rho_DE = OL0*(1 + alpha_QG*ln(1+Om/OL0)). Normalize so rho_DE(0)=OL0.
# k=2
def Z04_E(z_arr, Om):
    alpha_QG = -1.0 / (4.0 * math.pi**2)   # one-loop QG coefficient
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    x     = Om * (1+z_arr)**3 / OL0
    x0    = Om / OL0
    raw   = 1.0 + alpha_QG * np.log1p(x)
    norm0 = 1.0 + alpha_QG * math.log1p(x0)
    if abs(norm0) < 1e-10:
        return None
    rho_DE = OL0 * raw / norm0
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Z05: Two-Loop Log^2 SQ DE (k=2)
# A1+A2: Two-loop correction adds (ln)^2 term.
# rho_DE = OL0 * exp(alpha_QG * ln^2(1 + Om*(1+z)^3/OL0)) / norm.
# Coefficient alpha_QG = -1/(8*pi^2): two-loop suppression.
# k=2
def Z05_E(z_arr, Om):
    alpha_2loop = -1.0 / (8.0 * math.pi**2)
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    x      = Om * (1+z_arr)**3 / OL0
    x0     = Om / OL0
    rho_DE = OL0 * np.exp(alpha_2loop * np.log1p(x)**2)
    norm0  = math.exp(alpha_2loop * math.log1p(x0)**2)
    if abs(norm0) < 1e-10:
        return None
    rho_DE = rho_DE / norm0
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Z06: Log-correction amplitude free (k=3)
# A1+A2: Log-correction coefficient alpha_QG is free.
# rho_DE = OL0 * (1 + alpha * ln(1 + Om*(1+z)^3/OL0)) / norm. k=3.
def Z06_E_factory(alpha):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0:
            return None
        x      = Om * (1+z_arr)**3 / OL0
        x0     = Om / OL0
        raw    = 1.0 + alpha * np.log1p(x)
        norm0  = 1.0 + alpha * math.log1p(x0)
        if abs(norm0) < 1e-10: return None
        rho_DE = OL0 * raw / norm0
        rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 3: Polynomial DE from SQ density moments ───────────────────────

# Z07: Quadratic SQ Density Moment DE (k=2)
# A1+A3: SQ density field has non-Gaussian fluctuations.
# Second moment correction: <rho_SQ^2> - <rho_SQ>^2 ~ OL0^2 * (Om*(1+z)^3/OL0)^2.
# rho_DE = OL0 / (1 + c2 * (Om*(1+z)^3/OL0)^2) normalized.
# c2 = 1/(4*pi): second-order SQ lattice packing.
# k=2
def Z07_E(z_arr, Om):
    c2 = 1.0 / (4.0 * math.pi)   # second-moment SQ packing
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    x      = Om * (1+z_arr)**3 / OL0
    x0     = Om / OL0
    rho_DE = OL0 / (1.0 + c2 * x**2)
    norm0  = 1.0 / (1.0 + c2 * x0**2)
    if abs(norm0) < 1e-10:
        return None
    rho_DE = rho_DE / norm0
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Z08: Cubic SQ Density Moment DE (k=2)
# A1+A3: Third cumulant (skewness) of SQ density field:
# rho_DE = OL0 / (1 + c2*x^2 + c3*x^3) where x=Om*(1+z)^3/OL0.
# c2 = 1/(4pi), c3 = 1/(6pi^2): third-order Gram-Charlier coefficient.
# Normalize so rho_DE(z=0) = OL0.
# k=2
def Z08_E(z_arr, Om):
    c2 = 1.0 / (4.0 * math.pi)
    c3 = 1.0 / (6.0 * math.pi**2)
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    x      = Om * (1+z_arr)**3 / OL0
    x0     = Om / OL0
    rho_DE = OL0 / np.maximum(1.0 + c2*x**2 + c3*x**3, 1e-10)
    norm0  = 1.0 / max(1.0 + c2*x0**2 + c3*x0**3, 1e-10)
    if abs(norm0) < 1e-10:
        return None
    rho_DE = rho_DE / norm0
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Z09: Polynomial moment coefficient free (k=3)
# A1+A3: Quadratic SQ moment coefficient c2 is free.
# rho_DE = OL0 / (1 + c2 * (Om*(1+z)^3/OL0)^2) / norm. k=3.
def Z09_E_factory(c2):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0:
            return None
        x      = Om * (1+z_arr)**3 / OL0
        x0     = Om / OL0
        rho_DE = OL0 / np.maximum(1.0 + c2 * x**2, 1e-10)
        norm0  = 1.0 / max(1.0 + c2 * x0**2, 1e-10)
        if abs(norm0) < 1e-10: return None
        rho_DE = rho_DE / norm0
        rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 4: Rational function DE (Pade approximants) ────────────────────

# Z10: Pade [1/1] SQ DE (k=2)
# A1+A4: Pade approximant [1/1] to SQ depletion function.
# Near LCDM, w(a) deviations captured by Pade: f(x) = (1 + a1*x) / (1 + b1*x).
# a1 = 1/pi (SQ period), b1 = 1/e (exponential SQ decay).
# x = Om*(1+z)^3/OL0 (matter-to-DE ratio).
# rho_DE = OL0 * (1 + a1*x) / (1 + b1*x) normalized at z=0.
# k=2
def Z10_E(z_arr, Om):
    a1 = 1.0 / math.pi   # SQ oscillation period coefficient
    b1 = 1.0 / math.e    # SQ exponential decay coefficient
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    x      = Om * (1+z_arr)**3 / OL0
    x0     = Om / OL0
    raw    = (1.0 + a1 * x) / np.maximum(1.0 + b1 * x, 1e-10)
    norm0  = (1.0 + a1 * x0) / max(1.0 + b1 * x0, 1e-10)
    if abs(norm0) < 1e-10:
        return None
    rho_DE = OL0 * raw / norm0
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Z11: Pade [2/1] SQ DE (k=2)
# A1+A4: Pade [2/1] captures second-order SQ corrections.
# f(x) = (1 + a1*x + a2*x^2) / (1 + b1*x).
# a1 = 1/pi, a2 = 1/(2*pi^2) (second-order), b1 = 1/e.
# rho_DE = OL0 * f(x) / f(x0). Normalize at z=0.
# k=2
def Z11_E(z_arr, Om):
    a1 = 1.0 / math.pi
    a2 = 1.0 / (2.0 * math.pi**2)
    b1 = 1.0 / math.e
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    x      = Om * (1+z_arr)**3 / OL0
    x0     = Om / OL0
    raw    = (1.0 + a1*x + a2*x**2) / np.maximum(1.0 + b1*x, 1e-10)
    norm0  = (1.0 + a1*x0 + a2*x0**2) / max(1.0 + b1*x0, 1e-10)
    if abs(norm0) < 1e-10:
        return None
    rho_DE = OL0 * raw / norm0
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Z12: Pade [1/2] free denominator (k=3)
# A1+A4: Pade [1/2] with free b2 coefficient.
# f(x) = (1 + a1*x) / (1 + b1*x + b2*x^2). k=3.
def Z12_E_factory(b2):
    a1 = 1.0 / math.pi
    b1 = 1.0 / math.e
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0:
            return None
        x      = Om * (1+z_arr)**3 / OL0
        x0     = Om / OL0
        raw    = (1.0 + a1*x) / np.maximum(1.0 + b1*x + b2*x**2, 1e-10)
        norm0  = (1.0 + a1*x0) / max(1.0 + b1*x0 + b2*x0**2, 1e-10)
        if abs(norm0) < 1e-10: return None
        rho_DE = OL0 * raw / norm0
        rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 5: Exponential integral DE ─────────────────────────────────────

# Z13: Exponential Integral SQ DE (k=2)
# A1+A3: SQ generation rate involves exponential integral Ei due to incomplete
# annihilation events (A1). Incomplete gamma function from Poisson statistics
# of discrete SQ quanta: Gamma(0,x) = -Ei(-x) for x>0.
# rho_DE = OL0 * exp(-x0) / exp(-x) where x = t_ann/t_H = Om*(1+z)^3 / (OL0 * e).
# Equivalently: rho_DE = OL0 * exp(-(x - x0)) normalized.
# x = Om*(1+z)^3/(OL0*e). k=2.
def Z13_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    scale = OL0 * math.e   # exponential integral scale
    x     = Om * (1+z_arr)**3 / scale
    x0    = Om / scale
    rho_DE = OL0 * np.exp(-(x - x0))
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Z14: Gamma function SQ incomplete DE (k=2)
# A1+A3: Incomplete gamma function from SQ Poisson counting.
# Fraction of SQ quanta not yet annihilated: f_surv = Gamma(1/3, x)/Gamma(1/3).
# x = (Om*(1+z)^3)^(1/3) / OL0^(1/3) (cube root: 3D SQ volume annihilation).
# rho_DE = OL0 * f_surv(z) / f_surv(0). Use upper incomplete gamma ratio.
# Gamma(1/3, x)/Gamma(1/3) ~ exp(-x) for large x, ~1 for small x.
# Approximate: erfc(sqrt(x)) as proxy for upper incomplete gamma (close for 1/2 order).
# k=2
def Z14_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    x      = (Om * (1+z_arr)**3)**(1.0/3.0) / OL0**(1.0/3.0)
    x0     = Om**(1.0/3.0) / OL0**(1.0/3.0)
    # erfc as proxy for upper incomplete gamma ratio
    surv   = erfc(np.sqrt(x))
    surv0  = erfc(math.sqrt(x0))
    if surv0 < 1e-10:
        return None
    rho_DE = OL0 * surv / surv0
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Z15: Exponential integral scale free (k=3)
# A1+A3: Scale parameter for exp-integral DE is free.
# rho_DE = OL0 * exp(-A*(x - x0)) where x = Om*(1+z)^3/OL0. k=3.
def Z15_E_factory(A_ei):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0 or A_ei < 0:
            return None
        x      = Om * (1+z_arr)**3 / OL0
        x0     = Om / OL0
        rho_DE = OL0 * np.exp(-A_ei * (x - x0))
        rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 6: Trigonometric DE from SQ wave modes ─────────────────────────

# Z16: SQ Wave Mode Cosine DE (k=2)
# A1+A3: Uniform SQ generation (A3) creates standing wave modes in cosmic volume.
# Fundamental mode wavelength: lambda_SQ = 2 * r_s / sqrt(OL0).
# In redshift space, wave accumulates phase: phi(z) = pi * ln(1+z) / sqrt(OL0).
# SQ wave energy: rho_DE = OL0 * cos^2(phi(z)/2) (half-angle: density node at z_node).
# Normalize so rho_DE(z=0) = OL0. k=2.
def Z16_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    sq_OL0 = math.sqrt(OL0)
    phi    = math.pi * np.log1p(z_arr) / sq_OL0
    rho_DE = OL0 * np.cos(phi / 2.0)**2
    # at z=0: cos^2(0) = 1, so rho_DE(0) = OL0 -- already normalized
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Z17: SQ Wave Mode Squared-Sine DE (k=2)
# A1+A3: Complementary wave mode: SQ generates as matter annihilates wave nodes.
# rho_DE = OL0 * (1 - A_sin * sin^2(pi * sqrt(Om*(1+z)^3 / OL0)))
# A_sin = 2/pi^2: mode normalization from SQ lattice Brillouin zone boundary.
# Normalize at z=0. k=2.
def Z17_E(z_arr, Om):
    A_sin = 2.0 / math.pi**2   # Brillouin zone mode coefficient
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    arg    = math.pi * np.sqrt(Om * (1+z_arr)**3 / OL0)
    arg0   = math.pi * math.sqrt(Om / OL0)
    rho_DE = OL0 * (1.0 - A_sin * np.sin(arg)**2)
    norm0  = 1.0 - A_sin * math.sin(arg0)**2
    if abs(norm0) < 1e-10:
        return None
    rho_DE = rho_DE / norm0
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Z18: Trigonometric wave frequency free (k=3)
# A1+A3: SQ wave frequency nu_w is free.
# rho_DE = OL0 * cos^2(nu_w * ln(1+z) / 2) normalized. k=3.
def Z18_E_factory(nu_w):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or nu_w <= 0:
            return None
        phi    = nu_w * np.log1p(z_arr)
        rho_DE = OL0 * np.cos(phi / 2.0)**2
        # rho_DE(0) = OL0 * cos^2(0) = OL0: already normalized
        rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 7: Hyperbolic function DE from SQ potential ────────────────────

# Z19: SQ Cosh Potential DE (k=2)
# A1+A4: SQ field potential V(phi) ~ cosh(phi/phi_0) (double-well structure).
# phi evolves as phi ~ phi_0 * arcsinh(sqrt(Om)*(1+z)^(3/2)/OL0^(1/2)).
# rho_DE = OL0 / cosh(phi/phi_0)^2 = OL0 * sech^2(phi) normalized.
# phi_0 = 1/sqrt(2): canonical scalar field normalization.
# phi(z) = arcsinh(sqrt(Om*(1+z)^3 / OL0)). k=2.
def Z19_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    phi    = np.arcsinh(np.sqrt(np.maximum(Om * (1+z_arr)**3 / OL0, 0)))
    phi0   = math.asinh(math.sqrt(Om / OL0))
    sech2  = 1.0 / np.cosh(phi)**2
    sech20 = 1.0 / math.cosh(phi0)**2
    if abs(sech20) < 1e-10:
        return None
    rho_DE = OL0 * sech2 / sech20
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Z20: SQ Sinh Decay Potential DE (k=2)
# A1+A4: SQ field potential V(phi) ~ exp(-phi)*sinh(phi) (asymmetric double-well).
# Effective: rho_DE = OL0 * exp(-x) * sinh(x) / (exp(-x0)*sinh(x0))
# x = sqrt(Om*(1+z)^3/OL0). k=2.
def Z20_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    x      = np.sqrt(Om * (1+z_arr)**3 / OL0)
    x0     = math.sqrt(Om / OL0)
    f      = np.exp(-x) * np.sinh(x)
    f0     = math.exp(-x0) * math.sinh(x0)
    if abs(f0) < 1e-10:
        return None
    rho_DE = OL0 * f / f0
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Z21: Hyperbolic potential steepness free (k=3)
# A1+A4: Steepness parameter p in sech^p is free.
# rho_DE = OL0 * sech(phi)^p / sech(phi0)^p. k=3.
def Z21_E_factory(p):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0 or p <= 0:
            return None
        phi    = np.arcsinh(np.sqrt(np.maximum(Om * (1+z_arr)**3 / OL0, 0)))
        phi0   = math.asinh(math.sqrt(Om / OL0))
        sechp  = (1.0 / np.cosh(phi))**p
        sech0  = (1.0 / math.cosh(phi0))**p
        if abs(sech0) < 1e-10: return None
        rho_DE = OL0 * sechp / sech0
        rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 8: Bessel function DE from cylindrical void geometry ────────────

# Z22: Bessel J0 Cylindrical Void SQ DE (k=2)
# A1+A3: SQ annihilation occurs along cylindrical cosmic filament boundaries.
# Cylindrical geometry -> Bessel equation for SQ density profile.
# J0(x_01 * r/R) where x_01 = 2.4048 (first zero of J0, fixed by BC).
# Effective: rho_DE = OL0 * J0(x_01 * sqrt(Om*(1+z)^3/OL0)) / J0(x_01 * sqrt(Om/OL0)).
# J0 normalized at z=0. k=2.
def Z22_E(z_arr, Om):
    from scipy.special import j0
    x_01 = 2.4048   # first zero of J0: fixed by cylindrical BC
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    arg    = x_01 * np.sqrt(Om * (1+z_arr)**3 / OL0)
    arg0   = x_01 * math.sqrt(Om / OL0)
    j0_arr = j0(arg)
    j0_0   = float(j0(np.array([arg0]))[0])
    if abs(j0_0) < 1e-10:
        return None
    rho_DE = OL0 * j0_arr / j0_0
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Z23: Bessel I0 Modified Void SQ DE (k=2)
# A1+A3: Modified Bessel I0 from imaginary-argument cylindrical void (growing modes).
# rho_DE = OL0 * exp(-x) * I0(x) / (exp(-x0)*I0(x0)) where x=sqrt(Om*(1+z)^3/OL0).
# exp(-x)*I0(x) is the scaled modified Bessel: monotone, starts at 1, decays.
# k=2.
def Z23_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    x      = np.sqrt(Om * (1+z_arr)**3 / OL0)
    x0     = math.sqrt(Om / OL0)
    # i0e = exp(-|x|)*I0(x) (scipy scaled)
    from scipy.special import i0e
    f      = i0e(x)
    f0     = float(i0e(np.array([x0]))[0])
    if abs(f0) < 1e-10:
        return None
    rho_DE = OL0 * f / f0
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Z24: Bessel argument scale free (k=3)
# A1+A3: Bessel argument scale nu_B is free.
# rho_DE = OL0 * j0(nu_B * sqrt(Om*(1+z)^3/OL0)) / j0(nu_B * sqrt(Om/OL0)). k=3.
def Z24_E_factory(nu_B):
    from scipy.special import j0
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0 or nu_B <= 0:
            return None
        arg    = nu_B * np.sqrt(Om * (1+z_arr)**3 / OL0)
        arg0   = nu_B * math.sqrt(Om / OL0)
        j0_arr = j0(arg)
        j0_0   = float(j0(np.array([arg0]))[0])
        if abs(j0_0) < 1e-10: return None
        rho_DE = OL0 * j0_arr / j0_0
        rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 9: Elliptic function DE from SQ lattice ────────────────────────

# Z25: Jacobi Elliptic SQ Lattice DE (k=2)
# A1+A3: SQ quanta arranged on a lattice with elliptic geometry.
# Jacobi elliptic sn(u,k) with modulus k_el = 1/sqrt(2) (equal-energy lattice).
# u = sqrt(OL0/Om) * ln(1+z) (SQ lattice phase).
# rho_DE = OL0 * (1 - sn^2(u, 1/sqrt(2))) = OL0 * cn^2(u, 1/sqrt(2)).
# Use scipy.special.ellipj. Normalize at z=0. k=2.
def Z25_E(z_arr, Om):
    from scipy.special import ellipj
    k_el = 1.0 / math.sqrt(2.0)   # equal-energy lattice modulus
    k_sq = k_el**2   # k^2 = 0.5
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    u      = math.sqrt(OL0 / Om) * np.log1p(z_arr)
    u0     = math.sqrt(OL0 / Om) * 0.0   # at z=0: u0=0
    # ellipj returns (sn, cn, dn, ph)
    sn, cn, dn, ph = ellipj(u, k_sq)
    rho_DE = OL0 * cn**2
    # at z=0: u=0, cn(0,k)=1, so rho_DE(0) = OL0: already normalized
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Z26: Jacobi Elliptic dn^2 SQ DE (k=2)
# A1+A3: Using dn^2 component of Jacobi elliptic (different oscillation mode).
# rho_DE = OL0 * dn^2(u, k_el) normalized. dn(0,k)=1 so already normalized.
# u = sqrt(OL0/Om) * ln(1+z). k_el = 1/sqrt(2). k=2.
def Z26_E(z_arr, Om):
    from scipy.special import ellipj
    k_el = 1.0 / math.sqrt(2.0)
    k_sq = k_el**2
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    u          = math.sqrt(OL0 / Om) * np.log1p(z_arr)
    sn, cn, dn, ph = ellipj(u, k_sq)
    rho_DE = OL0 * dn**2
    # dn(0,k)=1, so rho_DE(0)=OL0 -- already normalized
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Z27: Elliptic lattice modulus free (k=3)
# A1+A3: Elliptic modulus k_el is free.
# rho_DE = OL0 * cn^2(u, k_el^2) normalized. k=3.
def Z27_E_factory(k_el):
    from scipy.special import ellipj
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0 or not (0 < k_el < 1):
            return None
        k_sq       = k_el**2
        u          = math.sqrt(OL0 / Om) * np.log1p(z_arr)
        sn, cn, dn, ph = ellipj(u, k_sq)
        rho_DE = OL0 * cn**2
        rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 10: Error function (erf) DE from diffusion boundary layer ────────

# Z28: Erf Diffusion Boundary SQ DE (k=2)
# A1+A3: SQ generation front diffuses across matter-void interface (A3 uniform gen).
# Diffusion boundary layer: f_surv = 0.5 * erfc(x / sqrt(2))
# where x = (Om*(1+z)^3 - OL0) / sqrt(2 * Om * OL0) (normalized density contrast).
# rho_DE = OL0 * erfc(x/sqrt(2)) / erfc(x0/sqrt(2)) normalized. k=2.
def Z28_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    sigma  = math.sqrt(2.0 * Om * OL0)   # diffusion width
    x      = (Om * (1+z_arr)**3 - OL0) / sigma
    x0     = (Om - OL0) / sigma
    f      = erfc(x / math.sqrt(2.0))
    f0     = erfc(x0 / math.sqrt(2.0))
    if f0 < 1e-10:
        return None
    rho_DE = OL0 * f / f0
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Z29: Erf Sigmoid SQ Transition DE (k=2)
# A1+A2+A3: Quantum-classical transition (A2) creates erf-shaped crossover in rho_DE.
# rho_DE = OL0 * (1 - erf(x)) / (1 - erf(x0)) normalized.
# x = sqrt(Om*(1+z)^3 / OL0) - 1. Transition at Om*(1+z)^3 = OL0, i.e. z_eq.
# k=2.
def Z29_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    ratio  = Om * (1+z_arr)**3 / OL0
    ratio0 = Om / OL0
    x      = np.sqrt(np.maximum(ratio, 0)) - 1.0
    x0     = math.sqrt(ratio0) - 1.0
    f      = 1.0 - erf(x)
    f0     = 1.0 - erf(x0)
    if abs(f0) < 1e-10:
        return None
    rho_DE = OL0 * f / f0
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Z30: Erf diffusion width free (k=3)
# A1+A2+A3: Diffusion width sigma_d is free.
# rho_DE = OL0 * erfc((Om*(1+z)^3 - OL0)/sigma_d) / erfc((Om-OL0)/sigma_d). k=3.
def Z30_E_factory(sigma_d):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0 or sigma_d <= 0:
            return None
        x      = (Om * (1+z_arr)**3 - OL0) / sigma_d
        x0     = (Om - OL0) / sigma_d
        f      = erfc(x / math.sqrt(2.0))
        f0     = erfc(x0 / math.sqrt(2.0))
        if f0 < 1e-10: return None
        rho_DE = OL0 * f / f0
        rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ==============================================================================
# WORKER FUNCTION
# ==============================================================================

def worker_fn(args):
    """Runs in a separate process."""
    import sys, os, math, warnings
    import numpy as np

    os.environ['OMP_NUM_THREADS']      = '1'
    os.environ['MKL_NUM_THREADS']      = '1'
    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    np.seterr(all='ignore')
    warnings.filterwarnings('ignore')

    wid, theory_name, k, E_func_or_factory, extra_starts = args

    _SIM_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _SIM_DIR not in sys.path:
        sys.path.insert(0, _SIM_DIR)
    from desi_data import DESI_DR2, DESI_DR2_COV_INV
    from scipy.integrate import cumulative_trapezoid
    from scipy.optimize import minimize

    C_KMS  = 299792.458
    R_S    = 147.09
    OR     = 5.38e-5
    N_DATA = 13
    N_GRID = 4000
    LCDM_BASELINE_AICC = 15.392

    def aicc_w(chi2_val, k_in, n=N_DATA):
        return chi2_val + 2*k_in + 2*k_in*(k_in+1)/(n - k_in - 1)

    def compute_tv(Omega_m, H0, E_func):
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

    def chi2_w(params, E_func):
        Omega_m, H0 = params[0], params[1]
        if not (0.05 < Omega_m < 0.70 and 50.0 < H0 < 100.0):
            return 1e8
        th = compute_tv(Omega_m, H0, E_func)
        if th is None or not np.all(np.isfinite(th)):
            return 1e8
        delta = DESI_DR2['value'] - th
        return float(delta @ DESI_DR2_COV_INV @ delta)

    try:
        base_starts = [
            [0.315, 67.4], [0.30, 68.0], [0.32, 69.0],
            [0.29, 70.0],  [0.31, 68.5], [0.28, 71.0],
            [0.33, 67.0],  [0.34, 66.5],
        ]

        if k == 2:
            def wrapper(p):
                return chi2_w(p, E_func_or_factory)

            best_val = 1e8
            best_x   = None
            for s in base_starts:
                try:
                    res = minimize(wrapper, s, method='Nelder-Mead',
                                   options={'xatol': 1e-6, 'fatol': 1e-6, 'maxiter': 5000})
                    if res.fun < best_val:
                        best_val = res.fun
                        best_x   = res.x
                except Exception:
                    continue

            if best_x is None:
                return {'id': wid, 'name': theory_name, 'k': k,
                        'chi2': 1e8, 'aicc': 1e8, 'd_aicc': 1e8,
                        'Om': None, 'H0': None, 'extra': None, 'status': 'FAIL'}
            Om_best, H0_best = float(best_x[0]), float(best_x[1])
            chi2_best  = best_val
            extra_best = None

        else:  # k == 3
            combined_starts = [b + e for b in base_starts for e in extra_starts]

            def full_wrapper(p):
                try:
                    E_fn = E_func_or_factory(p[2])
                    return chi2_w(p[:2], E_fn)
                except Exception:
                    return 1e8

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
                return {'id': wid, 'name': theory_name, 'k': k,
                        'chi2': 1e8, 'aicc': 1e8, 'd_aicc': 1e8,
                        'Om': None, 'H0': None, 'extra': None, 'status': 'FAIL'}
            Om_best, H0_best = float(best_x[0]), float(best_x[1])
            chi2_best  = best_val
            extra_best = float(best_x[2])

        aicc_val = aicc_w(chi2_best, k)
        d_aicc   = aicc_val - LCDM_BASELINE_AICC
        status   = 'PASS' if aicc_val < LCDM_BASELINE_AICC else 'KILL'

        return {
            'id':     wid,
            'name':   theory_name,
            'k':      k,
            'chi2':   float(chi2_best),
            'aicc':   float(aicc_val),
            'd_aicc': float(d_aicc),
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
# THEORY LIST
# ==============================================================================

def build_theory_list():
    theories = [
        # Direction 1: Power-law corrections from A1 annihilation rate
        ('Z01', 'Annihilation Rate Power-Law SQ DE',        2, Z01_E,  None),
        ('Z02', 'Annihilation Rate Sqrt Correction SQ DE',  2, Z02_E,  None),
        ('Z03', 'Power-law Exponent Free',                  3, Z03_E_factory,
            [[0.5], [1.0], [1.5], [2.0], [3.0], [4.0]]),
        # Direction 2: Logarithmic corrections from SQ quantum gravity
        ('Z04', 'Quantum Gravity Log Correction SQ DE',     2, Z04_E,  None),
        ('Z05', 'Two-Loop Log-Sq SQ DE',                    2, Z05_E,  None),
        ('Z06', 'Log-Correction Amplitude Free',            3, Z06_E_factory,
            [[-0.5], [-0.1], [-0.01], [0.01], [0.1], [0.5]]),
        # Direction 3: Polynomial DE from SQ density moments
        ('Z07', 'Quadratic SQ Density Moment DE',           2, Z07_E,  None),
        ('Z08', 'Cubic SQ Density Moment DE',               2, Z08_E,  None),
        ('Z09', 'Polynomial Moment Coefficient Free',       3, Z09_E_factory,
            [[0.01], [0.05], [0.1], [0.5], [1.0], [5.0]]),
        # Direction 4: Rational function DE (Pade approximants)
        ('Z10', 'Pade [1/1] SQ DE',                        2, Z10_E,  None),
        ('Z11', 'Pade [2/1] SQ DE',                        2, Z11_E,  None),
        ('Z12', 'Pade [1/2] Free Denominator',             3, Z12_E_factory,
            [[0.01], [0.05], [0.1], [0.5], [1.0], [2.0]]),
        # Direction 5: Exponential integral DE
        ('Z13', 'Exponential Integral SQ DE',               2, Z13_E,  None),
        ('Z14', 'Gamma Function Incomplete SQ DE',          2, Z14_E,  None),
        ('Z15', 'Exponential Integral Scale Free',          3, Z15_E_factory,
            [[0.1], [0.3], [0.5], [1.0], [2.0], [5.0]]),
        # Direction 6: Trigonometric DE from SQ wave modes
        ('Z16', 'SQ Wave Mode Cosine DE',                   2, Z16_E,  None),
        ('Z17', 'SQ Wave Mode Squared-Sine DE',             2, Z17_E,  None),
        ('Z18', 'Trigonometric Wave Frequency Free',        3, Z18_E_factory,
            [[0.5], [1.0], [math.pi], [2.0*math.pi], [5.0], [10.0]]),
        # Direction 7: Hyperbolic function DE from SQ potential
        ('Z19', 'SQ Cosh Potential DE',                     2, Z19_E,  None),
        ('Z20', 'SQ Sinh Decay Potential DE',               2, Z20_E,  None),
        ('Z21', 'Hyperbolic Potential Steepness Free',      3, Z21_E_factory,
            [[0.5], [1.0], [2.0], [3.0], [4.0], [6.0]]),
        # Direction 8: Bessel function DE from cylindrical void geometry
        ('Z22', 'Bessel J0 Cylindrical Void SQ DE',        2, Z22_E,  None),
        ('Z23', 'Bessel I0 Modified Void SQ DE',           2, Z23_E,  None),
        ('Z24', 'Bessel Argument Scale Free',               3, Z24_E_factory,
            [[0.5], [1.0], [2.4048], [3.0], [5.0], [7.0]]),
        # Direction 9: Elliptic function DE from SQ lattice
        ('Z25', 'Jacobi Elliptic cn^2 SQ Lattice DE',      2, Z25_E,  None),
        ('Z26', 'Jacobi Elliptic dn^2 SQ Lattice DE',      2, Z26_E,  None),
        ('Z27', 'Elliptic Lattice Modulus Free',            3, Z27_E_factory,
            [[0.1], [0.3], [0.5], [0.7], [0.9], [0.99]]),
        # Direction 10: Error function (erf) DE from diffusion boundary layer
        ('Z28', 'Erf Diffusion Boundary SQ DE',             2, Z28_E,  None),
        ('Z29', 'Erf Sigmoid SQ Transition DE',             2, Z29_E,  None),
        ('Z30', 'Erf Diffusion Width Free',                 3, Z30_E_factory,
            [[0.1], [0.3], [0.5], [1.0], [2.0], [5.0]]),
    ]
    return theories


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    out_dir   = _SCRIPT_DIR
    json_path = os.path.join(out_dir, 'l30_results5.json')

    theories  = build_theory_list()
    task_args = []
    for wid, name, k, E_func_or_factory, extra_starts in theories:
        task_args.append((wid, name, k, E_func_or_factory, extra_starts))

    print('=' * 65)
    print('L30 5th Run SQMH Theory Test (Z01-Z30)')
    print('LCDM baseline: chi2={:.3f}  AICc={:.3f}'.format(
        LCDM_BASELINE_CHI2, LCDM_BASELINE_AICC))
    print('=' * 65)
    print('Launching {} theories with multiprocessing (9 workers max)...'.format(
        len(task_args)))

    ctx       = multiprocessing.get_context('spawn')
    n_workers = min(9, len(task_args))
    with ctx.Pool(n_workers) as pool:
        results = pool.map(worker_fn, task_args)

    # sort by AICc
    results.sort(key=lambda r: r['aicc'])

    # save JSON
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print('Saved: {}'.format(json_path))

    # print table
    print()
    print('{:<5} {:<44} {:>2} {:>9} {:>9} {:>8} {:>6}'.format(
        'ID', 'Theory', 'k', 'chi2', 'AICc', 'dAICc', 'Status'))
    print('-' * 88)
    pass_count = 0
    kill_count = 0
    for r in results:
        chi2_str  = '{:.4f}'.format(r['chi2'])   if r['chi2']   < 1e7 else 'FAIL'
        aicc_str  = '{:.4f}'.format(r['aicc'])   if r['aicc']   < 1e7 else 'FAIL'
        daicc_str = '{:.4f}'.format(r['d_aicc']) if r.get('d_aicc', 1e8) < 1e7 else 'FAIL'
        print('{:<5} {:<44} {:>2} {:>9} {:>9} {:>8} {:>6}'.format(
            r['id'], r['name'][:44], r['k'],
            chi2_str, aicc_str, daicc_str, r['status']))
        if r['status'] == 'PASS':
            pass_count += 1
        else:
            kill_count += 1

    print()
    print('PASS: {}  /  KILL: {}'.format(pass_count, kill_count))
    print()

    # Champion
    passed = [r for r in results if r['status'] == 'PASS']
    if passed:
        champ = passed[0]
        print('Champion: {} "{}"  chi2={:.4f}  AICc={:.4f}  dAICc={:.4f}'.format(
            champ['id'], champ['name'],
            champ['chi2'], champ['aicc'], champ['d_aicc']))
    else:
        print('No theory beat LCDM baseline.')

    return results


if __name__ == '__main__':
    main()
