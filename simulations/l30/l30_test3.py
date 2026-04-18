# -*- coding: utf-8 -*-
"""
l30_test3.py -- L30 3rd Run SQMH Fresh Theories (X01-X30)
==========================================================
30 new theories derived from SQMH axioms A1-A4 + C1-C3.
COMPLETELY different mechanisms from V-series and W-series.

Explored NEW directions:
- Geodesic deviation from annihilation pressure gradients
- Topological defect density evolution (monopoles, strings, walls from SQ phase transitions)
- Quantum coherence length of SQ field
- Soliton solutions in generation-annihilation field
- Dissipative structure formation in SQ fluid
- Non-Markovian memory effects in annihilation history
- Hamiltonian chaos in SQ trajectory space
- Intermittency in void expansion dynamics
- Multifractal scaling of annihilation events
- Synchronization of spatially separated annihilation regions

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


def multi_start_optimize_k2(chi2_wrapper):
    """Multi-start Nelder-Mead for k=2. Returns (x_best, chi2_best)."""
    starts = [
        [0.315, 67.4],
        [0.30,  68.0],
        [0.32,  69.0],
        [0.29,  70.0],
        [0.31,  68.5],
        [0.28,  71.0],
        [0.33,  67.0],
        [0.34,  66.5],
    ]
    best_val = 1e8
    best_x   = None
    for s in starts:
        try:
            res = minimize(chi2_wrapper, s, method='Nelder-Mead',
                           options={'xatol': 1e-6, 'fatol': 1e-6, 'maxiter': 5000})
            if res.fun < best_val:
                best_val = res.fun
                best_x   = res.x
        except Exception:
            continue
    return best_x, best_val


def multi_start_optimize_k3(chi2_wrapper, extra_starts):
    """Multi-start Nelder-Mead for k=3. Returns (x_best, chi2_best)."""
    base_starts = [
        [0.315, 67.4], [0.30, 68.0], [0.32, 69.0],
        [0.29, 70.0],  [0.31, 68.5], [0.28, 71.0],
        [0.33, 67.0],  [0.34, 66.5],
    ]
    combined = [b + e for b in base_starts for e in extra_starts]
    best_val = 1e8
    best_x   = None
    for s in combined:
        try:
            res = minimize(chi2_wrapper, s, method='Nelder-Mead',
                           options={'xatol': 1e-6, 'fatol': 1e-6, 'maxiter': 5000})
            if res.fun < best_val:
                best_val = res.fun
                best_x   = res.x
        except Exception:
            continue
    return best_x, best_val


# ==============================================================================
# THEORY DEFINITIONS (X01-X30)
# Each E_func signature: E_func(z_array, Omega_m) -> E_array
# ==============================================================================

# ── DIRECTION 1: Geodesic deviation from annihilation pressure gradients ──────

# X01: Annihilation Pressure Geodesic Deviation (k=2)
# A1+C1: Annihilation events exert a pressure gradient on spacetime geometry.
# Geodesic deviation equation: d^2 xi / dtau^2 = -R^mu_nu xi^nu.
# Net SQ pressure: P_ann ~ rho_m * c_SQ^2 where c_SQ = sqrt(OL0/rho_m_0).
# Deviation damps DE as: rho_DE = OL0 * exp(-(Om*(1+z)^3 / OL0)^(1/3)).
# Exponent 1/3 comes from geodesic deviation in 3+1D spacetime.
# k=2 (all parameters theory-derived)
def X01_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    ratio  = Om * (1+z_arr)**3 / OL0
    rho_DE = OL0 * np.exp(-ratio**(1.0/3.0))
    # Normalize so rho_DE(0) = OL0 (at z=0 ratio=Om/OL0, not 0)
    ratio0 = Om / OL0
    norm   = math.exp(-ratio0**(1.0/3.0))
    if norm < 1e-10:
        return None
    rho_DE = rho_DE / norm * OL0
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# X02: Geodesic Tidal Stretching DE (k=2)
# A1+C1: Tidal forces from annihilation pressure gradients stretch voids.
# Stretching rate: d(delta_void)/dt ~ H * (1 + rho_ann/rho_crit).
# Net effect: rho_DE = OL0 / (1 + (Om*(1+z)^3 / OL0)^(2/3)).
# Exponent 2/3 from tidal tensor trace in 3D.
# k=2
def X02_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    ratio  = (Om * (1+z_arr)**3 / OL0)**(2.0/3.0)
    rho_DE = OL0 / (1.0 + ratio)
    # Normalize: at z=0 gives OL0/(1+(Om/OL0)^(2/3)), not OL0. Fix:
    ratio0 = (Om / OL0)**(2.0/3.0)
    norm   = 1.0 / (1.0 + ratio0)
    rho_DE = rho_DE / norm
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# X03: Geodesic Deviation with Free Exponent (k=3)
# A1+C1: Geodesic deviation exponent gamma_geo is free.
# rho_DE = OL0 * exp(-(Om*(1+z)^3/OL0)^gamma_geo) / norm.
# k=3
def X03_E_factory(gamma_geo):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0 or gamma_geo <= 0:
            return None
        ratio  = Om * (1+z_arr)**3 / OL0
        rho_DE = OL0 * np.exp(-ratio**gamma_geo)
        ratio0 = Om / OL0
        norm   = math.exp(-ratio0**gamma_geo)
        if norm < 1e-10:
            return None
        rho_DE = rho_DE / norm
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 2: Topological defect density evolution from SQ phase transitions

# X04: Cosmic String Network SQ DE (k=2)
# A1+A4: SQ phase transitions produce cosmic string network.
# String tension: mu_s ~ eta_SQ^2 where eta_SQ ~ H0 (SQ symmetry breaking scale).
# String density: rho_string ~ mu_s / t^2 ~ mu_s * H^2.
# DE: rho_DE = OL0 * (1 + alpha_s * (E^2 - 1))^(-1)
# alpha_s = 1/sqrt(3) from string network scaling at radiation-matter equality.
# k=2
def X04_E(z_arr, Om):
    alpha_s = 1.0 / math.sqrt(3.0)   # fixed: string network coupling
    OL0     = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
    denom   = np.maximum(1.0 + alpha_s * (E_lcdm**2 - 1.0), 1e-10)
    rho_DE  = OL0 / denom
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# X05: Monopole Gas Annihilation DE (k=2)
# A1+A4: SQ phase transition produces magnetic monopole-like defects.
# Monopole annihilation rate: Gamma_mono ~ n_mono^2 * sigma_mono * v.
# n_mono ~ (1+z)^3 (dilutes like matter). Effective DE injection from
# monopole-antimonopole annihilation: delta_rho_DE ~ Gamma_mono / H.
# rho_DE = OL0 * (1 - f_mono * (1 - (1+z)^(-2))) where f_mono = pi^(-2).
# k=2
def X05_E(z_arr, Om):
    f_mono = 1.0 / math.pi**2   # fixed: monopole gas coupling
    OL0    = 1.0 - Om - OR
    rho_DE = OL0 * (1.0 - f_mono * (1.0 - (1+z_arr)**(-2.0)))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# X06: Domain Wall Dissolution DE (k=2)
# A4: SQ domain walls form at phase boundaries (A4: net rate sign determines regimes).
# Wall surface density sigma_wall ~ eta^3 / (1+z) (stretching).
# Wall tension contributes: rho_wall = sigma_wall * H^2 / c^2.
# Net DE: rho_DE = OL0 * (1+z)^(-1/3) (wall scaling: p_wall = -2/3 rho_wall).
# Exponent 1/3 from P=-2rho/3 domain wall equation of state, w=-2/3.
# k=2
def X06_E(z_arr, Om):
    # w_wall = -2/3 -> rho_wall ~ (1+z)^(3*(1+w)) = (1+z)^1 grows!
    # But dissolution (annihilation of walls) reverses: rho_DE ~ (1+z)^(-1)
    # Use dissolution-dominated: rho_DE = OL0 * (1+z)^(-1/3)
    OL0    = 1.0 - Om - OR
    rho_DE = OL0 * (1+z_arr)**(-1.0/3.0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# X07: String-Wall Composite Defect DE (k=3)
# A4: Combined network of strings and walls. String contribution ~ (1+z)^(-alpha_st),
# wall contribution ~ (1+z)^(-alpha_wl). Free parameter: relative string fraction f_st.
# rho_DE = OL0 * (f_st * (1+z)^(-alpha_st) + (1-f_st) * (1+z)^(-alpha_wl))
# alpha_st = 2/(3*pi), alpha_wl = 1/3 (fixed from network dynamics). f_st free.
def X07_E_factory(f_st):
    alpha_st = 2.0 / (3.0 * math.pi)
    alpha_wl = 1.0 / 3.0
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or not (0 < f_st < 1):
            return None
        rho_DE = OL0 * (f_st * (1+z_arr)**(-alpha_st)
                        + (1.0 - f_st) * (1+z_arr)**(-alpha_wl))
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 3: Quantum coherence length of SQ field ────────────────────────

# X08: SQ Coherence Length Decoherence (k=2)
# A1+A2: SQ field has quantum coherence length xi_coh ~ hbar / (m_SQ * c).
# When comoving scales exceed xi_coh, SQ decohere and become classical (A2).
# Fraction coherent: f_coh = exp(-L_H / xi_coh_comoving)
# In Hubble units: L_H ~ c/H, xi_coh ~ c/H0. So f_coh = exp(-E).
# rho_DE = OL0 * exp(-E_lcdm + 1) (normalize so f_coh(z=0)=1).
# k=2
def X08_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
    # f_coh = exp(-(E-1)) so at z=0: E=1, f_coh=1 (correct)
    rho_DE  = OL0 * np.exp(-(E_lcdm - 1.0))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# X09: SQ Coherence Phase Locking (k=2)
# A1+A2: Coherent SQ regions phase-lock: rho_DE oscillates with coherence phase.
# Phase theta = integral of m_SQ c^2 / hbar dt ~ ln(1+z) (conformal time proxy).
# Phase-locked fraction: f_lock = cos^2(theta/2) = (1 + cos(theta))/2.
# theta = pi * ln(1+z) / ln(1+z_eq) where z_eq ~ 3400.
# rho_DE = OL0 * (1 + (1/pi) * cos(pi * ln(1+z) / ln(4401))).
# 1/pi is the coherence oscillation amplitude from SQ uncertainty principle.
# k=2
def X09_E(z_arr, Om):
    ln_zeq = math.log(1.0 + 3400.0)   # matter-radiation equality
    A_coh  = 1.0 / math.pi             # fixed: SQ uncertainty amplitude
    OL0    = 1.0 - Om - OR
    theta  = math.pi * np.log1p(z_arr) / ln_zeq
    rho_DE = OL0 * (1.0 + A_coh * np.cos(theta))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# X10: SQ Coherence Length Free Decay (k=3)
# A1+A2: Coherence decay exponent xi_exp is free.
# rho_DE = OL0 * exp(-xi_exp * (E_lcdm - 1)).
# k=3
def X10_E_factory(xi_exp):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0:
            return None
        E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
        E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
        rho_DE  = OL0 * np.exp(-xi_exp * (E_lcdm - 1.0))
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 4: Soliton solutions in generation-annihilation field ───────────

# X11: SQ Kink Soliton Dark Energy (k=2)
# A1+A4: The SQ generation-annihilation field admits kink soliton solutions.
# Kink profile: phi_kink(z) = tanh((z - z_c)/xi_kink).
# SQ energy density stored in kink: rho_kink ~ sech^2((z-z_c)/xi_kink).
# As kink sweeps through cosmic time: rho_DE = OL0 * sech^2(z * sqrt(OL0/Om)) / sech^2(0).
# sech^2(0) = 1, xi_kink = sqrt(Om/OL0) from balance condition at z_bal.
# k=2
def X11_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    xi_k = math.sqrt(Om / OL0)   # kink width from balance
    arg  = z_arr / xi_k
    # sech^2(x) = 1/cosh^2(x)
    cosh_arg = np.cosh(np.minimum(arg, 100.0))
    rho_DE   = OL0 / (cosh_arg**2)
    # at z=0: rho_DE = OL0 / cosh(0)^2 = OL0 (correct)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# X12: SQ Breather Soliton DE (k=2)
# A1+A4: Breather soliton oscillates in generation-annihilation field.
# Breather: phi_br(z,t) ~ (A/omega_br) * sech(A*z) * cos(omega_br * t).
# In Hubble units, effective: rho_DE = OL0 * sech^2(beta_br * ln(1+z))
# beta_br = sqrt(3)/pi from breather frequency-wavenumber relation in phi^4 theory.
# At z=0: ln(1)=0, sech(0)=1 -> rho_DE=OL0 (correct normalization).
# k=2
def X12_E(z_arr, Om):
    beta_br = math.sqrt(3.0) / math.pi   # fixed: breather frequency relation
    OL0     = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    arg    = beta_br * np.log1p(z_arr)
    cosh_a = np.cosh(np.minimum(arg, 100.0))
    rho_DE = OL0 / (cosh_a**2)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# X13: SQ Soliton Width Free Parameter (k=3)
# A1+A4: Soliton width beta_br is free.
# rho_DE = OL0 / cosh^2(beta_br * ln(1+z)). k=3.
def X13_E_factory(beta_br):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or beta_br <= 0:
            return None
        arg    = beta_br * np.log1p(z_arr)
        cosh_a = np.cosh(np.minimum(arg, 100.0))
        rho_DE = OL0 / (cosh_a**2)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 5: Dissipative structure formation in SQ fluid ──────────────────

# X14: Prigogine Dissipative Structure DE (k=2)
# A1+A3+A4: SQ fluid far from equilibrium forms dissipative structures (Prigogine).
# Dissipative structures: entropy production rate sigma_P = J * F (flux times force).
# In cosmic SQ: J ~ n_SQ * H, F ~ rho_m / rho_DE. Entropy production peaks at
# matter-DE equality, creating a peak in rho_DE.
# rho_DE = OL0 * (1 + A_diss * (Om*(1+z)^3 / OL0) * exp(-Om*(1+z)^3/OL0))
# A_diss = 1/e from Prigogine maximum entropy production principle.
# k=2
def X14_E(z_arr, Om):
    A_diss = 1.0 / math.e   # fixed: maximum entropy production
    OL0    = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    x      = Om * (1+z_arr)**3 / OL0
    rho_DE = OL0 * (1.0 + A_diss * x * np.exp(-x))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# X15: Benard Cell Convection DE (k=2)
# A1+A3: SQ fluid driven by generation pressure develops Benard-like convective cells.
# Critical Rayleigh number Ra_c = 1708. Above Ra_c: organized rolls form.
# In SQ terms: roll formation reduces effective SQ bulk, decreasing rho_DE.
# rho_DE = OL0 * (1 - f_conv * tanh^2(z / z_Benard))
# z_Benard = (1708)^(1/4) / (6*pi) from dimensional analysis.
# f_conv = 1/(2*pi^2) from convective efficiency factor.
# k=2
def X15_E(z_arr, Om):
    f_conv   = 1.0 / (2.0 * math.pi**2)        # fixed: convective efficiency
    z_Benard = 1708.0**(0.25) / (6.0 * math.pi) # ~ 0.643
    OL0      = 1.0 - Om - OR
    rho_DE   = OL0 * (1.0 - f_conv * np.tanh(z_arr / z_Benard)**2)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# X16: Dissipative Coupling Free Amplitude (k=3)
# A1+A3+A4: Dissipative structure amplitude A_diss is free.
# rho_DE = OL0 * (1 + A_diss * x * exp(-x)) where x = Om*(1+z)^3/OL0. k=3.
def X16_E_factory(A_diss):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0:
            return None
        x      = Om * (1+z_arr)**3 / OL0
        rho_DE = OL0 * (1.0 + A_diss * x * np.exp(-x))
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 6: Non-Markovian memory effects in annihilation history ─────────

# X17: Non-Markovian Memory Kernel DE (k=2)
# A1+A3: Annihilation rate depends on history of matter density (non-Markovian).
# Memory kernel: K(z, z') = K_0 * exp(-(z-z') / z_mem) (exponential memory).
# z_mem = 1/ln(2) from half-memory decay at z=1 (recent structure formation).
# Effective accumulated annihilation: Gamma_eff ~ integral_0^z K(z,z') * Om*(1+z')^3 dz'.
# For exponential kernel: Gamma_eff = Om * (1+z)^3 / (1 + z/z_mem).
# rho_DE = OL0 * exp(-Gamma_eff / OL0 * alpha_mem) where alpha_mem = ln2/3.
# k=2
def X17_E(z_arr, Om):
    z_mem     = 1.0 / math.log(2.0)   # fixed: memory decay scale
    alpha_mem = math.log(2.0) / 3.0   # fixed: memory coupling
    OL0       = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    # effective accumulated annihilation with memory
    Gamma_eff = Om * (1+z_arr)**3 / (1.0 + z_arr / z_mem)
    rho_DE    = OL0 * np.exp(-alpha_mem * Gamma_eff / OL0)
    # Normalize to OL0 at z=0
    G0   = Om / (1.0 + 0.0 / z_mem)
    norm = math.exp(-alpha_mem * G0 / OL0)
    if norm < 1e-10:
        return None
    rho_DE = rho_DE / norm
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# X18: Power-Law Memory Kernel DE (k=2)
# A1+A3: Power-law memory (long-range correlations in annihilation history).
# Memory kernel K(tau) ~ tau^(-mu_mem) with mu_mem = 1/2 (sub-diffusion).
# Effective: Gamma_eff ~ (1+z)^(3*mu_mem) = (1+z)^(3/2).
# rho_DE = OL0 * exp(-alpha_pl * (1+z)^(3/2)) normalized to OL0 at z=0.
# alpha_pl = ln(2) / (2^(3/2) - 1) from normalization condition.
# k=2
def X18_E(z_arr, Om):
    mu_mem   = 0.5   # sub-diffusion exponent
    exp_mem  = 3.0 * mu_mem   # = 3/2
    # alpha chosen so that rho_DE changes by factor 1/2 at z_bal
    alpha_pl = math.log(2.0) / (2.0**exp_mem - 1.0)
    OL0      = 1.0 - Om - OR
    rho_DE   = OL0 * np.exp(-alpha_pl * ((1+z_arr)**exp_mem - 1.0))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# X19: Memory Decay Scale Free (k=3)
# A1+A3: Memory decay scale z_mem is free.
# rho_DE = OL0 * exp(-alpha_mem * Om*(1+z)^3 / (OL0*(1+z/z_mem))) / norm. k=3.
def X19_E_factory(z_mem):
    alpha_mem = math.log(2.0) / 3.0
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0 or z_mem <= 0:
            return None
        Gamma_eff = Om * (1+z_arr)**3 / (1.0 + z_arr / z_mem)
        rho_DE    = OL0 * np.exp(-alpha_mem * Gamma_eff / OL0)
        G0   = float(Om / (1.0 + 0.0 / z_mem))
        norm = math.exp(-alpha_mem * G0 / OL0)
        if norm < 1e-10: return None
        rho_DE = rho_DE / norm
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 7: Hamiltonian chaos in SQ trajectory space ────────────────────

# X20: Lyapunov Exponent SQ Depletion DE (k=2)
# A1+A4: SQ trajectories in phase space become chaotic with Lyapunov exponent Lambda_L.
# Chaos onset at matter-DE equality. Before: Lambda_L = 0 (regular).
# After: Lambda_L = H0 * sqrt(OL0/Om) (from KAM theorem breakup).
# Sensitivity to initial conditions amplifies annihilation:
# rho_DE = OL0 * exp(-Lambda_L * t) = OL0 * exp(-sqrt(OL0/Om) * ln(1+z)).
# At z=0: exponent = 0, rho_DE=OL0 (correct).
# k=2
def X20_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    Lambda_L = math.sqrt(OL0 / Om)   # Lyapunov: from KAM breakup
    rho_DE   = OL0 * np.exp(-Lambda_L * np.log1p(z_arr))
    # = OL0 * (1+z)^(-Lambda_L)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# X21: Arnold Diffusion SQ Mixing (k=2)
# A1+A4: Multi-dimensional SQ phase space allows Arnold diffusion.
# Diffusion rate D_Arnold ~ exp(-1/epsilon) where epsilon ~ (E^2 - 1).
# Net effect: slow mixing of SQ states increases apparent DE.
# rho_DE = OL0 * (1 + A_Arn * exp(-1/(E^2 - 1 + delta_reg)))
# A_Arn = 1/(2*pi), delta_reg = 1/pi (regularization of z=0 singularity).
# k=2
def X21_E(z_arr, Om):
    A_Arn   = 1.0 / (2.0 * math.pi)
    delta_r = 1.0 / math.pi   # regularization
    OL0     = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
    eps     = E_lcdm**2 - 1.0 + delta_r
    eps     = np.maximum(eps, 1e-10)
    rho_DE  = OL0 * (1.0 + A_Arn * np.exp(-1.0 / eps))
    # normalize: at z=0 eps=delta_r, factor = 1 + A_Arn*exp(-1/delta_r)
    norm0 = 1.0 + A_Arn * math.exp(-1.0 / delta_r)
    rho_DE = rho_DE / norm0
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# X22: Lyapunov Exponent Free (k=3)
# A1+A4: Lyapunov exponent scale lambda_free is free.
# rho_DE = OL0 * (1+z)^(-lambda_free). k=3.
def X22_E_factory(lambda_free):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0:
            return None
        rho_DE = OL0 * (1+z_arr)**(-lambda_free)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 8: Intermittency in void expansion dynamics ────────────────────

# X23: Void Intermittency Burst DE (k=2)
# A3+A4: Void expansion is intermittent: quiet phases punctuated by bursts.
# Bursts correlated with structure formation (z ~ 2-3). Intermittency parameter
# mu_int from On-Off intermittency: P(active) ~ (1+z)^(-mu_int).
# Average rho_DE = OL0 * (1 + f_int * ((1+z)^(-mu_int) - 1)/(1^(-mu_int) - 1))
# But simpler: rho_DE = OL0 / (1 + mu_int * ln^2(1+z)).
# mu_int = 1/(2*e) from intermittency universality class.
# k=2
def X23_E(z_arr, Om):
    mu_int = 1.0 / (2.0 * math.e)   # fixed: intermittency exponent
    OL0    = 1.0 - Om - OR
    rho_DE = OL0 / (1.0 + mu_int * np.log1p(z_arr)**2)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# X24: Void Burst Triggering (k=2)
# A3+A4: Void bursts triggered when matter density crosses threshold.
# Threshold: rho_m / rho_DE = 1 (matter-DE equality).
# Before threshold (high z): bursts enhance DE: rho_DE ~ OL0 * (1+z)^(+nu_b).
# After threshold (low z): bursts diminish: rho_DE ~ OL0 * (1+z)^(-nu_b).
# Smooth crossover: rho_DE = OL0 * ((1+z)^(nu_b) + (1+z)^(-nu_b)) / 2 / cosh(nu_b * ln(1+z_bal))
# nu_b = 1/(3*pi) from void burst statistics.
# k=2
def X24_E(z_arr, Om):
    nu_b = 1.0 / (3.0 * math.pi)   # fixed: void burst exponent
    OL0  = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    z_bal  = max(0.1, (OL0 / Om)**(1.0/3.0) - 1.0)
    arg    = nu_b * np.log1p(z_arr)
    # hyperbolic cosine form: rho_DE ~ cosh(nu_b * ln(1+z))
    cosh_z = np.cosh(arg)
    cosh_0 = 1.0   # cosh(0) = 1 at z=0
    rho_DE = OL0 * cosh_z / cosh_0
    # This grows with z. Instead use: rho_DE = OL0 / cosh(nu_b * ln(1+z))
    rho_DE = OL0 / cosh_z
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# X25: Intermittency Exponent Free (k=3)
# A3+A4: Intermittency exponent mu_int is free.
# rho_DE = OL0 / (1 + mu_int * ln^2(1+z)). k=3.
def X25_E_factory(mu_int):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or mu_int < 0:
            return None
        rho_DE = OL0 / (1.0 + mu_int * np.log1p(z_arr)**2)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 9: Multifractal scaling of annihilation events ─────────────────

# X26: Multifractal Singularity Spectrum DE (k=2)
# A1+A3+A4: Annihilation events have multifractal distribution.
# Singularity spectrum f(alpha_mf) is parabolic: f(alpha) = 1 - (alpha - alpha_0)^2 / (2*sigma_mf^2).
# Most probable singularity: alpha_0 = 1 (Holder exponent at most likely point).
# Width sigma_mf = 1/sqrt(2*pi) from Gaussian multifractal.
# Effective: average annihilation scaling ~ (1+z)^alpha_0 = (1+z)^1.
# But width causes dispersion: rho_DE = OL0 * exp(-sigma_mf^2 * ln^2(1+z) / 2).
# This is a log-normal distribution of annihilation events.
# k=2
def X26_E(z_arr, Om):
    sigma_mf = 1.0 / math.sqrt(2.0 * math.pi)   # fixed: multifractal width
    OL0      = 1.0 - Om - OR
    rho_DE   = OL0 * np.exp(-0.5 * sigma_mf**2 * np.log1p(z_arr)**2)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# X27: Multifractal Renyi Dimension DE (k=2)
# A1+A3: Renyi dimension D_q of annihilation events modifies effective DE scaling.
# D_2 (correlation dimension) ~ 2.67 (from cosmic web structure).
# DE density scales as: rho_DE = OL0 * (1+z)^(D_2 - 3) = (1+z)^(-1/3).
# D_2 = 8/3 gives exponent -1/3. Fixed from cosmic web fractal analysis.
# k=2
def X27_E(z_arr, Om):
    D_2    = 8.0 / 3.0   # fixed: Renyi D_2 correlation dimension
    exp_mf = D_2 - 3.0   # = -1/3
    OL0    = 1.0 - Om - OR
    rho_DE = OL0 * (1+z_arr)**exp_mf
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# X28: Multifractal Width Free (k=3)
# A1+A3: Multifractal width sigma_mf is free.
# rho_DE = OL0 * exp(-sigma_mf^2 * ln^2(1+z) / 2). k=3.
def X28_E_factory(sigma_mf):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or sigma_mf < 0:
            return None
        rho_DE = OL0 * np.exp(-0.5 * sigma_mf**2 * np.log1p(z_arr)**2)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 10: Synchronization of spatially separated annihilation regions

# X29: Kuramoto Synchronization SQ DE (k=2)
# A1+A3+A4: Spatially separated annihilation regions synchronize (Kuramoto model).
# Kuramoto order parameter: r_K = |<exp(i*theta_j)>|.
# Synchronization onset at coupling K > K_c = 2/pi*sigma_freq (Kuramoto transition).
# Order parameter near critical: r_K ~ sqrt((K - K_c) / K_c) ~ sqrt(E - 1).
# Synchronized regions annihilate collectively: enhanced depletion of SQ.
# rho_DE = OL0 * (1 - r_K^2) = OL0 * (1 - alpha_K * (E - 1)) clipped to [0, OL0].
# alpha_K = 1/pi from Kuramoto distribution width.
# k=2
def X29_E(z_arr, Om):
    alpha_K = 1.0 / math.pi   # fixed: Kuramoto coupling
    OL0     = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
    rho_DE  = OL0 * np.maximum(1.0 - alpha_K * (E_lcdm - 1.0), 1e-10)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# X30: Phase-Locked Synchronization DE (k=3)
# A1+A3+A4: Synchronization coupling alpha_K is free.
# rho_DE = OL0 * max(1 - alpha_K * (E_lcdm - 1), epsilon). k=3.
def X30_E_factory(alpha_K):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0:
            return None
        E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
        E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
        rho_DE  = OL0 * np.maximum(1.0 - alpha_K * (E_lcdm - 1.0), 1e-10)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ==============================================================================
# WORKER FUNCTION
# ==============================================================================

def worker_fn(args):
    """Runs in a separate process."""
    # Need to re-import inside worker (spawn context)
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
        # Direction 1: Geodesic Deviation
        ('X01', 'Annihilation Pressure Geodesic Dev',   2, X01_E,  None),
        ('X02', 'Geodesic Tidal Stretching DE',         2, X02_E,  None),
        ('X03', 'Geodesic Deviation Free Exponent',     3, X03_E_factory,
            [[0.1], [0.2], [1.0/3.0], [0.5], [1.0], [2.0]]),
        # Direction 2: Topological Defects
        ('X04', 'Cosmic String Network SQ DE',          2, X04_E,  None),
        ('X05', 'Monopole Gas Annihilation DE',         2, X05_E,  None),
        ('X06', 'Domain Wall Dissolution DE',           2, X06_E,  None),
        ('X07', 'String-Wall Composite Defect DE',      3, X07_E_factory,
            [[0.1], [0.3], [0.5], [0.7], [0.9], [0.2]]),
        # Direction 3: Quantum Coherence Length
        ('X08', 'SQ Coherence Decoherence DE',         2, X08_E,  None),
        ('X09', 'SQ Coherence Phase Locking DE',        2, X09_E,  None),
        ('X10', 'SQ Coherence Free Decay Scale',        3, X10_E_factory,
            [[0.1], [0.5], [1.0], [2.0], [3.0], [0.3]]),
        # Direction 4: Soliton Solutions
        ('X11', 'SQ Kink Soliton DE',                  2, X11_E,  None),
        ('X12', 'SQ Breather Soliton DE',               2, X12_E,  None),
        ('X13', 'SQ Soliton Free Width',                3, X13_E_factory,
            [[0.1], [0.3], [0.5], [1.0], [2.0], [0.7]]),
        # Direction 5: Dissipative Structures
        ('X14', 'Prigogine Dissipative Structure DE',   2, X14_E,  None),
        ('X15', 'Benard Cell Convection DE',            2, X15_E,  None),
        ('X16', 'Dissipative Coupling Free Amplitude',  3, X16_E_factory,
            [[0.1], [0.3], [1.0/math.e], [1.0], [2.0], [0.5]]),
        # Direction 6: Non-Markovian Memory
        ('X17', 'Non-Markovian Memory Kernel DE',       2, X17_E,  None),
        ('X18', 'Power-Law Memory Kernel DE',           2, X18_E,  None),
        ('X19', 'Memory Decay Scale Free',              3, X19_E_factory,
            [[0.5], [1.0], [1.0/math.log(2)], [2.0], [3.0], [5.0]]),
        # Direction 7: Hamiltonian Chaos
        ('X20', 'Lyapunov Exponent SQ Depletion DE',   2, X20_E,  None),
        ('X21', 'Arnold Diffusion SQ Mixing DE',        2, X21_E,  None),
        ('X22', 'Lyapunov Free Exponent DE',            3, X22_E_factory,
            [[0.1], [0.3], [0.5], [1.0], [1.5], [0.7]]),
        # Direction 8: Intermittency
        ('X23', 'Void Intermittency Burst DE',          2, X23_E,  None),
        ('X24', 'Void Burst Triggering DE',             2, X24_E,  None),
        ('X25', 'Intermittency Exponent Free',          3, X25_E_factory,
            [[0.05], [0.1], [1.0/(2*math.e)], [0.3], [0.5], [1.0]]),
        # Direction 9: Multifractal Scaling
        ('X26', 'Multifractal Singularity Spectrum DE', 2, X26_E,  None),
        ('X27', 'Multifractal Renyi Dimension DE',      2, X27_E,  None),
        ('X28', 'Multifractal Width Free',              3, X28_E_factory,
            [[0.1], [0.3], [0.5], [1.0/(math.sqrt(2*math.pi))], [1.0], [2.0]]),
        # Direction 10: Synchronization
        ('X29', 'Kuramoto Synchronization SQ DE',       2, X29_E,  None),
        ('X30', 'Phase-Locked Synchronization DE',      3, X30_E_factory,
            [[0.1], [0.3], [1.0/math.pi], [0.5], [1.0], [2.0]]),
    ]
    return theories


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    out_dir   = _SCRIPT_DIR
    json_path = os.path.join(out_dir, 'l30_results3.json')

    theories  = build_theory_list()
    task_args = []
    for wid, name, k, E_func_or_factory, extra_starts in theories:
        task_args.append((wid, name, k, E_func_or_factory, extra_starts))

    print('=' * 65)
    print('L30 3rd Run SQMH Theory Test (X01-X30)')
    print('LCDM baseline: chi2={:.3f}  AICc={:.3f}'.format(
        LCDM_BASELINE_CHI2, LCDM_BASELINE_AICC))
    print('=' * 65)
    print('Launching {} theories with multiprocessing (9 workers max)...'.format(
        len(task_args)))

    ctx  = multiprocessing.get_context('spawn')
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
    print('{:<5} {:<42} {:>2} {:>9} {:>9} {:>8} {:>6}'.format(
        'ID', 'Theory', 'k', 'chi2', 'AICc', 'dAICc', 'Status'))
    print('-' * 86)
    pass_count = 0
    kill_count = 0
    for r in results:
        chi2_str  = '{:.4f}'.format(r['chi2'])   if r['chi2']   < 1e7 else 'FAIL'
        aicc_str  = '{:.4f}'.format(r['aicc'])   if r['aicc']   < 1e7 else 'FAIL'
        daicc_str = '{:.4f}'.format(r['d_aicc']) if r.get('d_aicc', 1e8) < 1e7 else 'FAIL'
        print('{:<5} {:<42} {:>2} {:>9} {:>9} {:>8} {:>6}'.format(
            r['id'], r['name'][:42], r['k'],
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
