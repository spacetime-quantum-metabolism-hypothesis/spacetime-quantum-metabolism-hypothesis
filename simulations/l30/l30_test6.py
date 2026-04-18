# -*- coding: utf-8 -*-
"""
l30_test6.py -- L30 6th Run SQMH Fundamental Simple Physical Logic (AA01-AA30)
================================================================================
근본적인 단순한 물리적 논리로 도출. 다른 분야에서 빌려온 수학 사용 금지.
SQMH 공리 A1-A4 에서 직접 도출한 가장 단순한 함수 형태.

Physical reasoning approach:
1. A1: matter density rho_m drives annihilation -> DE decreases where matter is dense
2. A3: generation is uniform -> rate_gen = const (set by current H)
3. A4: net rate = generation - annihilation -> DE evolves
4. Simplest math: linear, ratio, void fraction, rate equation

Functional form philosophy:
- Void fraction: f_void = 1 - Om*(1+z)^3 / (Om*(1+z)^3 + OL0)
- Rate balance: dρ_DE/dt = Γ_gen - Γ_ann(ρ_m)
- Conservation: ρ_DE + α*ρ_m = const
- Pressure: P_SQ = -ρ_SQ in voids, approaches 0 near matter
- Simple linear: ρ_DE = OL0*(1 - α*(ρ_m - ρ_m0)/ρ_crit)

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


# ==============================================================================
# THEORY DEFINITIONS (AA01-AA30)
# Each E_func signature: E_func(z_array, Omega_m) -> E_array
#
# Physical basis notation:
# - Om_z = Om*(1+z)^3  (matter density at z, normalized to crit today)
# - OL0 = 1 - Om - OR  (cosmological constant equivalent today)
# - f_void(z) = OL0 / (Om_z + OL0)  (void fraction at redshift z)
# ==============================================================================

# ==============================================================================
# DIRECTION 1: VOID FRACTION THEORIES
# A1: matter annihilates SQ quanta; A3: generation uniform.
# DE lives in voids -> proportional to void fraction.
# ==============================================================================

# AA01: Linear Void Fraction DE (k=2)
# From A1+A3: DE density proportional to void fraction f_void = OL0/(OL0+Om_z).
# At z=0: f_void = OL0/(OL0+Om), normalized to give OL0 today.
# rho_DE(z) = OL0 * f_void(z) / f_void(0)
# Physical statement: "DE occupies the void; where matter is, SQ quanta are annihilated."
def AA01_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    Om_z = Om * (1 + z_arr)**3
    f_void = OL0 / (Om_z + OL0)           # void fraction at z
    f_void0 = OL0 / (Om + OL0)            # void fraction at z=0
    if f_void0 < 1e-10:
        return None
    rho_DE = OL0 * f_void / f_void0
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# AA02: Squared Void Fraction DE (k=2)
# From A1+A3: SQ quanta annihilation is two-body (matter-SQ interaction).
# Rate alpha rho_m * rho_SQ -> equilibrium rho_DE ~ f_void^2.
# Physical statement: "Two-body annihilation rate gives f_void^2 dependence."
def AA02_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    Om_z = Om * (1 + z_arr)**3
    f_void = OL0 / (Om_z + OL0)
    f_void0 = OL0 / (Om + OL0)
    if f_void0 < 1e-10:
        return None
    rho_DE = OL0 * (f_void / f_void0)**2
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# AA03: Void Fraction Exponent Free (k=3)
# From A1+A3: The exponent of void fraction dependence is free (multi-body process).
# rho_DE = OL0 * (f_void/f_void0)^n. k=3.
def AA03_E_factory(n):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0 or n <= 0:
            return None
        Om_z = Om * (1 + z_arr)**3
        f_void = OL0 / (Om_z + OL0)
        f_void0 = OL0 / (Om + OL0)
        if f_void0 < 1e-10:
            return None
        rho_DE = OL0 * (f_void / f_void0)**n
        rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0):
            return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ==============================================================================
# DIRECTION 2: LINEAR MATTER-DENSITY CORRECTION
# A1: DE decreases linearly as matter density increases.
# Simplest possible: rho_DE = OL0 * (1 - alpha*(Om_z - Om)/rho_crit)
# ==============================================================================

# AA04: Linear Matter-Density Correction DE (k=2)
# From A1: DE annihilation rate ~ rho_m (A1 literally).
# Linear correction: rho_DE = OL0 - alpha*(Om_z - Om)
# Coefficient alpha = Om/OL0 (ratio at z=0, keeps rho_DE(0) = OL0 exact).
# Physical statement: "Each unit of matter-density increase depletes DE by fixed ratio."
def AA04_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    alpha = Om / OL0    # fixed by Om/OL0 at z=0
    Om_z  = Om * (1 + z_arr)**3
    rho_DE = OL0 - alpha * (Om_z - Om)
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# AA05: Fractional Linear Correction DE (k=2)
# From A1+A4: Rate eq. dρ_DE/dt = Γ_gen - Γ_ann; at steady state Γ_gen=Γ_ann.
# Off-equilibrium: rho_DE = OL0 * (1 - (Om_z/Om - 1) * (Om/OL0))
# = OL0 * (1 - (Om_z - Om)/OL0)
# Physical statement: "DE deficit equals fractional matter excess."
def AA05_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    Om_z  = Om * (1 + z_arr)**3
    rho_DE = OL0 * (1.0 - (Om_z - Om) / OL0)
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# AA06: Linear Correction Amplitude Free (k=3)
# From A1: Linear DE correction with free amplitude alpha.
# rho_DE = OL0 * (1 - alpha*(Om_z/Om - 1)). k=3.
def AA06_E_factory(alpha):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0:
            return None
        Om_z  = Om * (1 + z_arr)**3
        rho_DE = OL0 * (1.0 - alpha * (Om_z / Om - 1.0))
        rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0):
            return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ==============================================================================
# DIRECTION 3: CONSERVATION LAW THEORIES
# A1+A3: Total SQ quanta (matter-bound + void) = constant.
# Conservation: rho_DE + alpha*rho_m = const -> rho_DE = C - alpha*Om_z
# ==============================================================================

# AA07: SQ Conservation DE (k=2)
# From A1+A3: total rho_SQ is conserved. At z=0: rho_DE0 + alpha*Om = C.
# -> rho_DE(z) = rho_DE0 + alpha*(Om - Om_z) = OL0 - alpha*(Om_z - Om).
# alpha = OL0/Om (conservation ratio: DE and matter exchange SQ quanta 1:1 scaled).
# Physical statement: "SQ quanta conserved; matter increase depletes void SQ."
def AA07_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    alpha = OL0 / Om   # conservation ratio
    Om_z  = Om * (1 + z_arr)**3
    rho_DE = OL0 - alpha * (Om_z - Om)
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# AA08: Conservation with sqrt coupling (k=2)
# From A1+A3: SQ annihilation in 3D goes as rho_m^(1/2) (surface-to-volume crossing).
# rho_DE = OL0 - alpha*(sqrt(Om_z) - sqrt(Om))
# alpha = OL0 / (sqrt(OL0)) = sqrt(OL0): dimensional from rate equation.
# Physical statement: "SQ crossing rate scales as sqrt(rho_m) (surface flux)."
def AA08_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    alpha = math.sqrt(OL0)   # sqrt surface-flux coefficient
    Om_z  = Om * (1 + z_arr)**3
    rho_DE = OL0 - alpha * (np.sqrt(Om_z) - math.sqrt(Om))
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# AA09: Conservation coupling power free (k=3)
# From A1+A3: SQ conservation coupling rho_m^p with free exponent p.
# rho_DE = OL0 * (1 - alpha*(Om_z^p - Om^p)/Om^p). k=3.
def AA09_E_factory(p):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0 or p <= 0:
            return None
        Om_z  = Om * (1 + z_arr)**3
        rho_DE = OL0 * (1.0 - (Om_z**p - Om**p) / (Om**p + OL0**p))
        rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0):
            return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ==============================================================================
# DIRECTION 4: RATE EQUATION THEORIES
# A4: net rate = generation - annihilation -> dρ_DE/dz given by ODE.
# Simplest rate eq: dρ_DE/dz = -k_ann * rho_m * rho_DE / (1+z)
# Solution: rho_DE(z) = OL0 * exp(-k_ann * integral(rho_m dz/(1+z)))
# integral from 0 to z of Om*(1+z')^2 dz' = Om*((1+z)^3 - 1)/3
# ==============================================================================

# AA10: Rate Equation Exponential DE (k=2)
# From A4: dρ_DE/dN = -Gamma_ann = -k * Om_z (A1: ann rate prop to matter density).
# N = ln(a) -> dN = -dz/(1+z).
# Solution: rho_DE = OL0 * exp(-k * integral_0^z Om*(1+z')^2 dz')
# = OL0 * exp(-k * Om * ((1+z)^3 - 1) / 3)
# k = OL0/Om (set by OL0/Om ratio so that at high-z correction is O(1)).
# Physical statement: "DE depletes exponentially as matter accumulates SQ quanta."
def AA10_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    k_ann = OL0 / Om   # annihilation rate constant from OL0/Om ratio
    # integral from 0 to z: Om*(1+z')^2 dz' = Om*((1+z)^3-1)/3
    integral_val = Om * ((1 + z_arr)**3 - 1.0) / 3.0
    rho_DE = OL0 * np.exp(-k_ann * integral_val)
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# AA11: Rate Eq with generation term (k=2)
# From A3+A4: dρ_DE/dN = Gamma_gen - Gamma_ann.
# Gamma_gen = OL0 (constant, A3), Gamma_ann = OL0 * Om_z / Om (A1).
# Steady-state solution: rho_DE = OL0 * Om / Om_z = OL0 / (1+z)^3
# But normalized: rho_DE(z) = OL0 * (Om / Om_z) = OL0 / (1+z)^3.
# Physical statement: "Steady-state of uniform generation vs matter-proportional annihilation."
def AA11_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    # rho_DE at z=0: OL0 * Om/Om = OL0 (correct)
    # rho_DE at z: OL0 * Om / (Om*(1+z)^3) = OL0/(1+z)^3
    rho_DE = OL0 / (1 + z_arr)**3
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# AA12: Rate Eq with partial coupling (k=2)
# From A3+A4: generation partial, rate = Gamma_gen - beta*Gamma_ann.
# Intermediate between LCDM (beta=0) and full depletion.
# rho_DE = OL0 * (1 - beta_c * (1 - Om/Om_z))
# beta_c = Om/(Om+OL0) = Omega_m_today (fraction of total non-radiation).
# Physical statement: "Partial coupling: only fraction beta of matter annihilates SQ."
def AA12_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    beta_c = Om / (Om + OL0)   # coupling fraction fixed by matter/total ratio
    Om_z   = Om * (1 + z_arr)**3
    rho_DE = OL0 * (1.0 - beta_c * (1.0 - Om / Om_z))
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# ==============================================================================
# DIRECTION 5: PRESSURE ARGUMENT THEORIES
# A1: SQ quanta flow into matter exert pressure.
# P_SQ = -rho_SQ in voids (w=-1), P_SQ -> 0 near matter.
# Near matter: effective w_DE = -1 + delta_w where delta_w ~ rho_m/rho_crit.
# ==============================================================================

# AA13: Matter-Pressure Correction DE (k=2)
# From A1: SQ pressure near matter is reduced by matter infall.
# w_eff(z) = -1 + (Om_z/rho_crit) * (OL0/(OL0+Om_z))
# Integrate: rho_DE(a) from continuity eq dρ/da = -3(1+w)rho/a.
# Simple closed-form: rho_DE = OL0 * (OL0/(OL0+Om_z)) * exp((Om_z - Om)/(OL0+Om)).
# Physical statement: "SQ pressure in voids is -rho; near matter it is reduced."
def AA13_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    Om_z = Om * (1 + z_arr)**3
    # Void fraction * small exponential correction
    f_void   = OL0 / (OL0 + Om_z)
    f_void0  = OL0 / (OL0 + Om)
    exp_corr = np.exp((Om_z - Om) / (OL0 + Om))  # correction at z=0 is 1
    rho_DE   = OL0 * (f_void / f_void0) * exp_corr
    rho_DE   = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# AA14: Pressure with rate balance (k=2)
# From A1+A4: SQ pressure supports DE against matter infall.
# Balance: rho_DE = OL0 * exp(-Om_z/(OL0+Om_z) + Om/(OL0+Om))
# = OL0 * exp(-(Om_z/(OL0+Om_z) - Om/(OL0+Om)))
# = OL0 * exp(-(1-f_void(z)) + (1-f_void(0)))
# = OL0 * exp(f_void(z) - f_void(0))
# Physical statement: "DE decays as void fraction decreases (pressure argument)."
def AA14_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    Om_z   = Om * (1 + z_arr)**3
    f_void  = OL0 / (OL0 + Om_z)
    f_void0 = OL0 / (OL0 + Om)
    rho_DE  = OL0 * np.exp(f_void - f_void0)
    rho_DE  = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# AA15: Pressure amplitude free (k=3)
# From A1: pressure amplitude A in rho_DE = OL0 * exp(A*(f_void - f_void0)) is free.
def AA15_E_factory(A):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0:
            return None
        Om_z   = Om * (1 + z_arr)**3
        f_void  = OL0 / (OL0 + Om_z)
        f_void0 = OL0 / (OL0 + Om)
        rho_DE  = OL0 * np.exp(A * (f_void - f_void0))
        rho_DE  = np.maximum(rho_DE, 1e-10 * OL0)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0):
            return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ==============================================================================
# DIRECTION 6: SIMPLE RATIO THEORIES
# A1+A3: The ratio OL0/Om changes with z.
# DE tracks this ratio: rho_DE = OL0 * (OL0_z/OL0_0) in some sense.
# OL0_z = E^2 - Om_z is not closed-form, so use OL0/(OL0+Om_z) ratio.
# ==============================================================================

# AA16: Matter-to-DE ratio tracking (k=2)
# From A1+A3: At equilibrium, DE-to-matter ratio is maintained.
# rho_DE/rho_m = (OL0/Om) * correction.
# Simplest: rho_DE = OL0 * Om / Om_z = OL0 / (1+z)^3 (pure tracking).
# Same as AA11. Variant: harmonic mean rho_DE = 2*OL0*Om / (OL0 + Om_z).
# Physical statement: "DE tracks harmonic mean of today's OL0 and matter at z."
def AA16_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    Om_z   = Om * (1 + z_arr)**3
    norm0  = 2.0 * OL0 * Om / (OL0 + Om)   # at z=0: = OL0 * 2Om/(OL0+Om)
    if norm0 < 1e-10:
        return None
    rho_DE = 2.0 * OL0 * Om / (OL0 + Om_z)
    rho_DE = OL0 * rho_DE / norm0           # normalize so rho_DE(0) = OL0
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# AA17: Inverse matter density ratio (k=2)
# From A1: DE inversely proportional to matter density (A1 literally: more matter = less DE).
# rho_DE = OL0^2 / (OL0 + Om_z - Om)
# Interpretation: each matter quantum absorbed converts OL0 unit of DE.
# Physical statement: "DE inversely proportional to matter; 1-to-1 exchange at Hubble rate."
def AA17_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    Om_z = Om * (1 + z_arr)**3
    denom = OL0 + (Om_z - Om)
    denom = np.maximum(denom, 1e-10)
    rho_DE = OL0**2 / denom
    # at z=0: OL0^2/OL0 = OL0 (correct)
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# AA18: Ratio exponent free (k=3)
# From A1: DE ~ (OL0/(OL0+Om_z))^n with free exponent n.
# General power-law of void fraction. k=3.
def AA18_E_factory(n):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0 or n <= 0:
            return None
        Om_z = Om * (1 + z_arr)**3
        f_void  = OL0 / (OL0 + Om_z)
        f_void0 = OL0 / (OL0 + Om)
        if f_void0 < 1e-10:
            return None
        rho_DE = OL0 * (f_void / f_void0)**n
        rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0):
            return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ==============================================================================
# DIRECTION 7: GENERATION RATE THEORIES
# A3: generation is spatially uniform -> rate_gen = G_0 (constant).
# A4: net rate sign determines regime.
# If net rate > 0: DE grows; < 0: DE shrinks.
# At high z, more matter -> more annihilation -> DE was lower.
# ==============================================================================

# AA19: Generation Rate Balance DE (k=2)
# From A3+A4: Generation = G_0 = OL0 (sets z=0 equilibrium).
# Annihilation = G_0 * Om_z/Om (proportional to matter, A1).
# Net: dρ_DE/dz = -(G_0/Om) * Om_z / (1+z) [rate per comoving volume].
# Approximation: rho_DE = OL0 - OL0*(Om_z - Om)/Om
# = OL0*(1 - (Om_z/Om - 1)) = OL0*(2 - (1+z)^3).
# (only valid near z=0; clip negative to 0)
# Physical statement: "Net rate gives linear-in-matter-density DE evolution."
def AA19_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    rho_DE = OL0 * (2.0 - (1 + z_arr)**3)
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# AA20: Saturated Generation DE (k=2)
# From A3+A4: generation is uniform but saturates (max rate = OL0).
# Saturation: rho_DE = OL0 * OL0 / (OL0 + Om_z*(1 - Om/OL0))
# Physical statement: "Generation saturates at OL0; net rate reduces DE at high z."
def AA20_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    Om_z   = Om * (1 + z_arr)**3
    # generation scale: OL0; excess annihilation scale: Om_z - Om
    # rho_DE = OL0 / (1 + (Om_z - Om)/OL0^2 * Om)
    denom  = 1.0 + (Om_z - Om) * Om / OL0**2
    denom  = np.maximum(denom, 1e-10)
    rho_DE = OL0 / denom
    # normalize at z=0: 1/(1+0) = 1 -> rho_DE(0) = OL0 already
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# AA21: Generation coupling free (k=3)
# From A3+A4: coupling constant gamma between generation and annihilation is free.
# rho_DE = OL0 / (1 + gamma * (Om_z - Om) / OL0). k=3.
def AA21_E_factory(gamma):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0:
            return None
        Om_z  = Om * (1 + z_arr)**3
        denom = 1.0 + gamma * (Om_z - Om) / OL0
        denom = np.maximum(denom, 1e-10)
        rho_DE = OL0 / denom
        rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0):
            return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ==============================================================================
# DIRECTION 8: EQUILIBRIUM APPROACH THEORIES
# A4: Net rate = 0 gives equilibrium DE density.
# Near equilibrium: rho_DE = rho_eq + perturbation.
# rho_eq is where generation = annihilation.
# ==============================================================================

# AA22: Equilibrium + linear perturbation DE (k=2)
# From A4: rho_eq satisfies G_gen = G_ann. At z=0: rho_eq = OL0.
# At z>0: equilibrium shifts because matter increases.
# Simple: rho_DE = OL0 * (1 + correction) where correction = -(Om_z-Om)/(Om_z+OL0).
# Physical: equilibrium shifts proportional to matter excess / total density.
# Physical statement: "DE tracks equilibrium which shifts as matter-to-total ratio changes."
def AA22_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    Om_z   = Om * (1 + z_arr)**3
    om_tot  = Om_z + OL0
    # correction at z=0: -(Om-Om)/(Om+OL0) = 0 (correct)
    corr   = -(Om_z - Om) / om_tot
    rho_DE = OL0 * (1.0 + corr)
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# AA23: Equilibrium + squared perturbation DE (k=2)
# From A4: second-order equilibrium shift (matter excess squared).
# rho_DE = OL0 * (1 - ((Om_z-Om)/(OL0+Om))^2)
# Physical statement: "Equilibrium DE quadratically perturbed by matter excess."
def AA23_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    Om_z  = Om * (1 + z_arr)**3
    delta = (Om_z - Om) / (OL0 + Om)
    rho_DE = OL0 * (1.0 - delta**2)
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# AA24: Equilibrium perturbation amplitude free (k=3)
# From A4: amplitude of equilibrium shift is free parameter A.
# rho_DE = OL0 * (1 - A*(Om_z-Om)/(OL0+Om)). k=3.
def AA24_E_factory(A):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0:
            return None
        Om_z  = Om * (1 + z_arr)**3
        delta = (Om_z - Om) / (OL0 + Om)
        rho_DE = OL0 * (1.0 - A * delta)
        rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0):
            return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ==============================================================================
# DIRECTION 9: TOTAL DENSITY FRACTION THEORIES
# A2+A3: Quantum-classical boundary depends on total density.
# At high z, all is quantum; at low z, mostly classical (DE/voids).
# Transition: rho_DE = f(total density ratio).
# ==============================================================================

# AA25: Total Density Depletion DE (k=2)
# From A2+A3: quantum-to-classical transition at rho_total ~ rho_Planck.
# At low rho_total (low z): mostly classical voids (DE ≈ OL0).
# At high rho_total: quantum regime (DE suppressed).
# Simplest: rho_DE = OL0 * (OL0 / E2_est) where E2_est ~ Om_z + OL0.
# Physical statement: "DE fraction = OL0 fraction of total matter+DE density."
def AA25_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    Om_z    = Om * (1 + z_arr)**3
    total_z = Om_z + OL0          # total non-radiation density
    total_0 = Om + OL0
    # rho_DE = OL0^2 / total_z * (total_0/OL0) = OL0 * total_0 / total_z
    rho_DE  = OL0 * total_0 / total_z
    rho_DE  = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# AA26: Quantum transition threshold DE (k=2)
# From A2: quantum-classical boundary at rho_m = OL0.
# Below threshold (z < z*): classical, DE = OL0.
# Above threshold: DE suppressed proportionally to OL0/(Om_z).
# Smoothed: rho_DE = OL0 * OL0 / max(OL0, Om_z).
# Physical statement: "DE suppressed when matter exceeds OL0 (quantum regime)."
def AA26_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    Om_z   = Om * (1 + z_arr)**3
    denom  = np.maximum(OL0, Om_z)
    rho_DE = OL0**2 / denom
    # at z=0: Om < OL0 for typical params, so denom=OL0, rho_DE=OL0 (correct).
    # But need to normalize properly.
    denom0 = max(OL0, Om)
    rho_DE0_val = OL0**2 / denom0
    if rho_DE0_val < 1e-10:
        return None
    rho_DE = rho_DE * OL0 / rho_DE0_val
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# AA27: Quantum boundary free threshold (k=3)
# From A2: quantum threshold rho_th is free.
# rho_DE = OL0 * rho_th / max(rho_th, Om_z). k=3.
def AA27_E_factory(rho_th_frac):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0 or rho_th_frac <= 0:
            return None
        rho_th = rho_th_frac * OL0   # threshold as fraction of OL0
        Om_z   = Om * (1 + z_arr)**3
        denom  = np.maximum(rho_th, Om_z)
        rho_DE = rho_th * OL0 / denom
        denom0 = max(rho_th, Om)
        rho_DE0_val = rho_th * OL0 / denom0
        if rho_DE0_val < 1e-10:
            return None
        rho_DE = rho_DE * OL0 / rho_DE0_val
        rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0):
            return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ==============================================================================
# DIRECTION 10: SIMPLE MIXED THEORIES
# Combining two axioms for simple mixed functional forms.
# ==============================================================================

# AA28: Volume-weighted DE (k=2)
# From A1+A3: SQ density weighted by void volume fraction * total volume.
# Volume of voids scales as f_void; DE per unit volume scales as OL0.
# Total DE = OL0 * f_void * (1+z)^3 (because volume grows as (1+z)^{-3}).
# rho_DE = OL0 * f_void(z) * (1+z)^3 / (f_void(0) * 1)
# = OL0 * (OL0/(Om_z + OL0)) * (1+z)^3 / (OL0/(Om + OL0))
# = OL0 * (Om + OL0) / (Om*(1+z)^3 + OL0) * (1+z)^3.
# Hmm let me simplify:
# Physical statement: "DE energy density = SQ per void * void volume fraction."
def AA28_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    Om_z   = Om * (1 + z_arr)**3
    # f_void(z) * (1+z)^3 relative to f_void(0):
    # [OL0/(OL0+Om_z)] * (1+z)^3 / [OL0/(OL0+Om)]
    # = (OL0+Om) * (1+z)^3 / (OL0+Om_z)
    # = (OL0+Om) / (OL0/(1+z)^3 + Om)
    ratio   = (OL0 + Om) * (1 + z_arr)**3 / (OL0 + Om_z)
    ratio0  = 1.0   # at z=0: (OL0+Om)/(OL0+Om) = 1
    rho_DE  = OL0 * ratio / ratio0
    rho_DE  = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# AA29: Differential Depletion DE (k=2)
# From A1+A4: each time step dρ_DE = -Gamma_ann dt where Gamma_ann = OL0*Om_z/Om.
# Integrated from z=0 to z: net change proportional to integral of Om_z dz.
# Simple: rho_DE = OL0 * exp(-Om * ((1+z)^3 - 1) / (3 * (OL0 + Om)))
# Coefficient: Om/(3*(OL0+Om)) is the integrated rate relative to total.
# Physical statement: "Exponential depletion with rate = matter/(3*total)."
def AA29_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    # integral of Om*(1+z)^2 dz from 0 to z = Om*((1+z)^3 - 1)/3
    # rate constant: 1/(OL0 + Om) = 1/(1-OR) ~ 1
    k_rate = 1.0 / (OL0 + Om)
    integral_val = Om * ((1 + z_arr)**3 - 1.0) / 3.0
    rho_DE = OL0 * np.exp(-k_rate * integral_val)
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# AA30: Mixed void+rate DE (k=3)
# From A1+A3+A4: void fraction * rate equation combined.
# rho_DE = OL0 * (f_void/f_void0)^alpha * exp(-beta*(Om_z - Om)/OL0).
# Combined: alpha free. k=3.
def AA30_E_factory(alpha):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0 or alpha < 0:
            return None
        Om_z   = Om * (1 + z_arr)**3
        f_void  = OL0 / (OL0 + Om_z)
        f_void0 = OL0 / (OL0 + Om)
        beta   = Om / OL0   # fixed from Om/OL0 ratio
        if f_void0 < 1e-10:
            return None
        rho_DE = OL0 * (f_void / f_void0)**alpha * np.exp(-beta * (Om_z - Om) / OL0)
        rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0):
            return None
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
        # Direction 1: Void fraction (A1+A3)
        ('AA01', 'Linear Void Fraction DE',           2, AA01_E, None),
        ('AA02', 'Squared Void Fraction DE',          2, AA02_E, None),
        ('AA03', 'Void Fraction Exponent Free',       3, AA03_E_factory,
            [[0.5], [1.0], [1.5], [2.0], [3.0], [4.0]]),
        # Direction 2: Linear matter-density correction (A1)
        ('AA04', 'Linear Matter-Density Correction',  2, AA04_E, None),
        ('AA05', 'Fractional Linear Correction DE',   2, AA05_E, None),
        ('AA06', 'Linear Correction Amplitude Free',  3, AA06_E_factory,
            [[0.1], [0.3], [0.5], [0.7], [1.0], [1.5]]),
        # Direction 3: Conservation law (A1+A3)
        ('AA07', 'SQ Conservation DE',                2, AA07_E, None),
        ('AA08', 'Conservation Sqrt Coupling DE',     2, AA08_E, None),
        ('AA09', 'Conservation Coupling Power Free',  3, AA09_E_factory,
            [[0.25], [0.5], [0.75], [1.0], [1.5], [2.0]]),
        # Direction 4: Rate equation (A3+A4)
        ('AA10', 'Rate Equation Exponential DE',      2, AA10_E, None),
        ('AA11', 'Steady-State Rate Balance DE',      2, AA11_E, None),
        ('AA12', 'Partial Coupling Rate DE',          2, AA12_E, None),
        # Direction 5: Pressure argument (A1)
        ('AA13', 'Matter-Pressure Correction DE',     2, AA13_E, None),
        ('AA14', 'Pressure-Void Balance DE',          2, AA14_E, None),
        ('AA15', 'Pressure Amplitude Free',           3, AA15_E_factory,
            [[-2.0], [-1.0], [-0.5], [0.5], [1.0], [2.0]]),
        # Direction 6: Simple ratio (A1+A3)
        ('AA16', 'Harmonic Mean Tracking DE',         2, AA16_E, None),
        ('AA17', 'Inverse Matter Density DE',         2, AA17_E, None),
        ('AA18', 'Ratio Exponent Free DE',            3, AA18_E_factory,
            [[0.5], [1.0], [1.5], [2.0], [3.0], [4.0]]),
        # Direction 7: Generation rate (A3+A4)
        ('AA19', 'Linear Generation Rate DE',         2, AA19_E, None),
        ('AA20', 'Saturated Generation DE',           2, AA20_E, None),
        ('AA21', 'Generation Coupling Free',          3, AA21_E_factory,
            [[0.1], [0.3], [0.5], [1.0], [2.0], [5.0]]),
        # Direction 8: Equilibrium approach (A4)
        ('AA22', 'Equilibrium Linear Perturbation',   2, AA22_E, None),
        ('AA23', 'Equilibrium Squared Perturbation',  2, AA23_E, None),
        ('AA24', 'Equilibrium Amplitude Free',        3, AA24_E_factory,
            [[0.1], [0.5], [1.0], [2.0], [3.0], [5.0]]),
        # Direction 9: Total density fraction (A2+A3)
        ('AA25', 'Total Density Depletion DE',        2, AA25_E, None),
        ('AA26', 'Quantum Threshold Suppression DE',  2, AA26_E, None),
        ('AA27', 'Quantum Boundary Free Threshold',   3, AA27_E_factory,
            [[0.3], [0.5], [1.0], [2.0], [3.0], [5.0]]),
        # Direction 10: Mixed (A1+A3+A4)
        ('AA28', 'Volume-Weighted Void DE',           2, AA28_E, None),
        ('AA29', 'Differential Depletion DE',         2, AA29_E, None),
        ('AA30', 'Mixed Void+Rate Free Alpha',        3, AA30_E_factory,
            [[0.5], [1.0], [1.5], [2.0], [3.0], [4.0]]),
    ]
    return theories


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    out_dir   = _SCRIPT_DIR
    json_path = os.path.join(out_dir, 'l30_results6.json')

    theories  = build_theory_list()
    task_args = []
    for wid, name, k, E_func_or_factory, extra_starts in theories:
        task_args.append((wid, name, k, E_func_or_factory, extra_starts))

    print('=' * 65)
    print('L30 6th Run SQMH Fundamental Simple Physical Logic (AA01-AA30)')
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
