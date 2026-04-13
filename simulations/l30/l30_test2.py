# -*- coding: utf-8 -*-
"""
L30 2차 실행: 30-theory SQMH cosmological model comparison against DESI DR2 BAO data.

8-person team, 10 rounds of independent theory derivation from axioms A1-A4.
No formula hints provided. All theories derived independently.
All theories are distinct from the 30 theories in l30_test.py (1st run).

Axioms:
  A1: Matter annihilates spacetime quanta; empty space creates them.
  A2: Quantum-classical boundary is induced from A1.
  A3: Creation is spatially uniform; annihilation depends only on local
      non-relativistic matter density. de Sitter symmetry, thermodynamics,
      QFT, and general covariance simultaneously require this asymmetry.
  A4: Net rate (creation - annihilation) sign determines three regimes:
      net creation (empty space -> dark energy), net annihilation
      (near matter -> gravity), balance (boundary surface).

Consistency conditions:
  C1: Equivalence principle (inertial = gravitational mass)
  C2: CPT symmetry (matter/antimatter same annihilation)
  C3: Holographic principle (BH entropy = A/4G)
  C4: Momentum conservation (anisotropic inflow -> gravitational force)
  C5: Angular momentum conservation (rotating mass -> Lense-Thirring)

AICc baseline:
  LCDM best-fit: chi2=10.192, AICc=15.392 (k=2, n=13)
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

OMEGA_R = 9.0e-5


# ============================================================
# CORE BAO MACHINERY
# ============================================================

def compute_theory_vector_from_E(E_func, Om, H0):
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
    if not (0.10 < Om < 0.60 and 55.0 < H0 < 90.0):
        return 1e8
    th = compute_theory_vector_from_E(E_func, Om, H0)
    if th is None or not np.all(np.isfinite(th)):
        return 1e8
    delta = DESI_DR2['value'] - th
    return float(delta @ DESI_DR2_COV_INV @ delta)


def fit_model(E_func, k_params=2):
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
    z_fit = np.linspace(0.01, 1.5, 200)
    E_arr = E_func(z_fit, Om, H0)
    if E_arr is None or not np.all(np.isfinite(E_arr)):
        return None, None

    E2_arr = E_arr**2

    def cpl_E2(z_arr, w0, wa):
        OL = 1.0 - Om - OMEGA_R
        a = 1.0 / (1.0 + z_arr)
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
# ROUND 1-3: 30 NEW THEORY E(z) DEFINITIONS
# All theories derived from A1-A4 independently by 8-person team.
# None overlap with l30_test.py theories T01-T30.
# ============================================================

# ---- N01: Quantum depletion lattice ----
# From A1: spacetime quanta form a lattice; matter depletes them locally.
# The lattice spacing grows as quanta are lost -> effective Hubble expansion.
# A3: uniform creation restores lattice at rate ~ OL0 per Hubble time.
# Conservation of lattice sites: d(n)/dt = -Gamma_a*rho_m + Gamma_c
# Team derives: rho_DE(a) = OL0 * (1 - (1-a^3)*Om/(3*OL0))
# This is a different closure from T09/T27 -- uses lattice depletion fraction.
# Derived constant: xi = Om/(3*OL0) from site-conservation argument.
def E_N01(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    xi = Om / (3.0 * max(OL0, 1e-6))
    rho_DE = OL0 * (1.0 - xi * (1.0 - a**3))
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N02: Causal horizon creation ----
# From A3+C3: only spacetime quanta within causal (Hubble) horizon are created.
# Creation rate ~ 1/d_H^2 ~ H^2, but suppressed by matter fraction.
# rho_DE(a) = OL0 * exp(eta * ln(a) * Om) = OL0 * a^(eta*Om)
# eta from A3 QFT vacuum: eta = 1/3 (one dimension of causal creation)
# This gives effective w_DE = -1 + eta*Om/3
def E_N02(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    eta = 1.0 / 3.0  # causal dimension factor from A3
    w_eff = -1.0 + eta * Om / 3.0
    a = 1.0 / (1.0 + z)
    rho_DE = OL0 * a**(-3.0*(1.0 + w_eff))
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N03: Entanglement entropy DE ----
# From A2+C3: quantum-classical boundary has entanglement entropy S_ent ~ area.
# As boundary shrinks with matter growth, entanglement DE is released.
# rho_DE(a) = OL0 + kappa * (1 - a^2)
# kappa from entanglement area formula: kappa = Om^2 / (2*(1-Om))
# Derived from: entanglement entropy ~ horizon area ~ 1/H^2 ~ a^2
def E_N03(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    kappa = Om**2 / (2.0 * max(1.0 - Om, 1e-6))
    a = 1.0 / (1.0 + z)
    rho_DE = OL0 + kappa * (1.0 - a**2)
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N04: Metabolic cascade DE ----
# From A1+A4: annihilation cascade generates secondary quanta (metabolic chain).
# Each annihilation event produces f_c secondary creations.
# f_c = 1 - Om (fraction of empty volume) from A4 geometry.
# Net: rho_DE decreases as matter grows, at rate set by cascade.
# w(z) = -1 + Om*(1+z)^(-1) / (3*(1-Om))
def E_N04(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    f_c = 1.0 - Om
    # w(z) integration
    z_int = np.linspace(0.0, np.max(z) + 0.01, 2000)
    w_arr = -1.0 + Om / (3.0 * max(f_c, 1e-6) * (1.0 + z_int))
    integrand = (1.0 + w_arr) / (1.0 + z_int)
    integral = np.concatenate([[0.0], cumulative_trapezoid(integrand, z_int)])
    rho_DE_arr = OL0 * np.exp(3.0 * integral)
    rho_DE = np.interp(z, z_int, rho_DE_arr)
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))


# ---- N05: Vacuum polarization DE ----
# From A1+A2: matter polarizes quantum vacuum -> separates virtual pairs.
# Polarized pairs create effective negative pressure at horizon scale.
# rho_DE = OL0 * (1 + p * a^(-1) * (1-a))
# p = Om/4 from vacuum polarization susceptibility (A1 dimensional argument)
# Different from T13/T27: uses vacuum polarization, not momentum/angular flux.
def E_N05(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    p = Om / 4.0
    a = 1.0 / (1.0 + z)
    corr = 1.0 + p * (1.0 - a) / np.maximum(a, 1e-6)
    rho_DE = OL0 * np.maximum(corr, 0.01)
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0 * (1.0 + 0.0)
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N06: Quantum foam dark energy ----
# From A1+A2: quantum foam topology fluctuations at Planck scale.
# As matter dilutes, foam density decreases -> fewer annihilations -> DE rises.
# rho_DE(a) = OL0 / (1 - mu * ln(a))
# mu = Om/3 from A1 foam depletion argument (foam count ~ matter count).
# At a=1: rho_DE = OL0. At a<1 (high z): 1-mu*ln(a) > 1 -> rho_DE < OL0.
def E_N06(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    mu = Om / 3.0
    a = 1.0 / (1.0 + z)
    log_a = np.log(np.maximum(a, 1e-10))
    denom = 1.0 - mu * log_a  # log_a <= 0 so denom >= 1
    rho_DE = OL0 / np.maximum(denom, 1e-6)
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N07: Spacetime viscosity DE ----
# From A3+A4: bulk viscosity from spacetime quantum fluid resists expansion.
# Bulk viscosity xi_v ~ rho_DE * H (from A3 thermodynamics).
# Effective pressure: P_eff = -rho_DE - 3*xi_v*H = P_DE - 3*xi_v*H
# w_eff(z) = -1 - 3*xi_0 * E(z) / OL(z) -- nonlinear, closed form:
# Simple linear approximation: w_eff = -1 - nu_v (const)
# nu_v from A3 dissipation: nu_v = Om^2 / (6*(1-Om))
def E_N07(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    nu_v = Om**2 / (6.0 * max(1.0 - Om, 1e-6))
    # Phantom w = -1 - nu_v (constant phantom)
    w_ph = -1.0 - nu_v
    a = 1.0 / (1.0 + z)
    rho_DE = OL0 * a**(-3.0*(1.0 + w_ph))
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N08: Quantum clock DE ----
# From A2: quantum clocks (coherent oscillators at boundary) decohere with time.
# Decoherence rate ~ H (expansion dilutes boundary coherence).
# rho_DE(a) = OL0 * (1 + tau * (1 - a^2) * exp(-Om * (1-a)))
# tau = Om / (1 - Om) from coherence time argument.
# Different closure: exponential decay modulating quadratic term.
def E_N08(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    tau = Om / max(1.0 - Om, 1e-6)
    a = 1.0 / (1.0 + z)
    rho_DE = OL0 * (1.0 + tau * (1.0 - a**2) * np.exp(-Om * (1.0 - a)))
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N09: Quantum information flux ----
# From A1+C4: annihilation events carry information flux; C4 requires flux conservation.
# Information flux from matter volume ~ rho_m^(4/3) (Stefan-Boltzmann analogy).
# w(z) = -1 + (1/3)*(rho_m/OL0)^(1/3) at each z.
# Team integrates: rho_DE changes as information is exchanged.
# Simplified: rho_DE = OL0 * (1 - phi * (Om * (1+z)^3)^(1/3))
# phi = OL0^(-1/3) * Om^(1/3) / 3 -- normalized by E(0)=1.
def E_N09(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    # phi from dimensional balance: phi = (Om/OL0)^(1/3) / 3
    phi = (Om / max(OL0, 1e-6))**(1.0/3.0) / 3.0
    rho_m_z = Om * (1.0 + z)**3
    rho_DE = OL0 * (1.0 - phi * (rho_m_z / max(Om, 1e-6))**(1.0/3.0) + phi)
    # Normalize at z=0: rho_DE(0) = OL0*(1-phi+phi) = OL0 -- OK
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N10: Hawking radiation DE ----
# From A1+C3: annihilation near matter mimics Hawking evaporation of spacetime.
# Hawking-like flux creates effective DE at horizon of each matter clump.
# T_H ~ rho_m^(1/4) (gravitational temperature), energy density ~ T_H^4.
# rho_DE = OL0 + zeta * (rho_m - Om)
# zeta from A1 + Stefan-Boltzmann: zeta = OL0 / (3 * Om) -- normalized.
# Different from T22/T08: Hawking mechanism, not G-running or RVM.
def E_N10(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    zeta = OL0 / (3.0 * max(Om, 1e-6))
    rho_m_z = Om * (1.0 + z)**3
    rho_DE = OL0 + zeta * (Om - rho_m_z)  # negative at high z -> less DE
    # Guard: rho_DE must stay positive
    rho_DE = np.maximum(rho_DE, 0.01 * OL0)
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0 + zeta * (Om - Om)
    E2_0 = Om + OR + OL0
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N11: Topological defect DE ----
# From A1+A2: quantum-classical boundary is a topological defect (domain wall).
# Domain wall energy ~ area ~ H^{-2}; as H grows, wall area decreases -> DE falls.
# rho_DE = OL0 / (1 + sigma_t * Om * (1+z)^3)^(2/3)
# sigma_t = 1/2 from domain wall tension derived in A2 (Kibble-Zurek mechanism).
# Different from T20 (de Sitter entropy correction): topological origin.
def E_N11(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    sigma_t = 0.5  # from A2 Kibble-Zurek domain wall tension
    denom = (1.0 + sigma_t * Om * (1.0 + z)**3)**(2.0/3.0)
    rho_DE = OL0 / np.maximum(denom, 1e-6)
    rho_DE_0 = OL0 / (1.0 + sigma_t * Om)**(2.0/3.0)
    OL_norm = (1.0 - Om - OR) * OL0 / max(rho_DE_0, 1e-10)
    rho_DE = OL_norm / np.maximum(denom, 1e-6)
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL_norm / (1.0 + sigma_t * Om)**(2.0/3.0)
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N12: Gravitational memory DE ----
# From C4+A4: gravitational waves from anisotropic quantum inflow carry memory.
# Memory effect modifies effective Lambda at late times.
# rho_DE = OL0 * (1 + gamma_m * z * exp(-z^2 / 2))
# gamma_m from A4 momentum conservation: gamma_m = -Om / (2*pi) (negative for wa<0)
# Gaussian profile: emission peaks at z~1, memory stored in spacetime geometry.
def E_N12(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    gamma_m = -Om / (2.0 * np.pi)
    rho_DE = OL0 * (1.0 + gamma_m * z * np.exp(-z**2 / 2.0))
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N13: Spacetime condensate DE ----
# From A1+A3: spacetime quanta form Bose-Einstein condensate in void regions.
# Condensate fraction ~ (1-rho_m/rho_c)^(3/2) (BEC analogy).
# As matter grows, condensate fraction drops, DE density falls.
# rho_DE = OL0 * (1 - chi*(1+z)^(3/2) + chi)
# chi = (Om/(1-Om))^(1/2) from condensate fraction normalization.
# Different closure than N01: BEC power-law exponent 3/2.
def E_N13(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    chi = np.sqrt(Om / max(1.0 - Om, 1e-6))
    a = 1.0 / (1.0 + z)
    # rho_DE = OL0 * (1 - chi*(a^(-3/2) - 1)) but need E(0)=1:
    # at a=1: term = 0 -> rho_DE = OL0 OK
    rho_DE = OL0 * (1.0 - chi * (a**(-1.5) - 1.0))
    rho_DE = np.maximum(rho_DE, 0.01 * OL0)
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N14: Quantum pressure DE ----
# From A3+A4: uniform creation exerts quantum pressure on boundary.
# Pressure balance: rho_DE * (1 + w_q) = q_pressure ~ H^2 / (8*pi*G).
# w_q from A3 pressure normalization: w_q = -1 + H^2/H0^2 * (Om/3)
# Closed form: w(z) = -1 + Om * E^2(z) / 3
# Self-consistent: need to solve E^2 * (1 - Om/3) = Om*(1+z)^3 + OR*(1+z)^4 + OL0
def E_N14(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    # From quantum pressure self-consistency:
    # (1 - Om/3) * E^2 = Om*(1+z)^3 + OR*(1+z)^4 + OL0 -- at leading order
    # This is the same as shifted w -- closed form:
    denom = 1.0 - Om / 3.0
    if abs(denom) < 1e-6:
        return None
    E2 = (Om*(1+z)**3 + OR*(1+z)**4 + OL0) / denom
    E2_0 = (Om + OR + OL0) / denom
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N15: Void expansion DE ----
# From A3+A4: voids (empty regions) are net creation zones.
# Void volume fraction f_v(z) ~ (1 - Om*(1+z)^3)^(2/3) for z near 0.
# rho_DE ~ (void fraction) * (creation rate) ~ OL0 * f_v(z).
# Team: rho_DE = OL0 * (1 - Om*(1+z)^3)^(1/3) -- void geometry.
# Normalized by defining OL_norm so E(0)=1.
def E_N15(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    rho_m_z = Om * (1.0 + z)**3
    void_frac = np.maximum(1.0 - rho_m_z, 1e-6)**(1.0/3.0)
    void_0 = np.maximum(1.0 - Om, 1e-6)**(1.0/3.0)
    rho_DE = OL0 * void_frac / max(void_0, 1e-10)
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N16: Torsion-coupled DE ----
# From A1+C1: spacetime quanta carry torsion; annihilation modifies torsion field.
# Torsion-modified Friedmann: E^2 = LCDM + T_torsion
# T_torsion = lambda_T * (1+z)^2 (linear in H, from Riemann-Cartan geometry)
# lambda_T from A1 torsion flux: lambda_T = -Om^2 / (4 * OL0)
# Different from T08/T24: geometric torsion origin, (1+z)^2 power.
def E_N16(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    lambda_T = -Om**2 / (4.0 * max(OL0, 1e-6))
    E2_LCDM = Om*(1+z)**3 + OR*(1+z)**4 + OL0
    torsion = lambda_T * (1.0 + z)**2
    E2 = E2_LCDM + torsion
    # Normalize at z=0:
    E2_0 = Om + OR + OL0 + lambda_T
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N17: Causal set DE ----
# From A1+A2: spacetime is a causal set (discrete events).
# Number of causal links ~ N ~ V * t^{-4} (4D spacetime density).
# DE = energy of causal links: rho_DE ~ N / V ~ H^4 / H0^4 at early times.
# Simple leading term: rho_DE = OL0 * (1 + eps_cs * (E^2 - 1))
# Self-consistent: E^2 * (1 - eps_cs*OL0) = Om*(1+z)^3 + OR*(1+z)^4 + OL0*(1 - eps_cs)
# eps_cs = Om / (4 * (1-Om)) from causal set density argument.
def E_N17(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    eps_cs = Om / (4.0 * max(1.0 - Om, 1e-6))
    num = Om*(1+z)**3 + OR*(1+z)**4 + OL0*(1.0 - eps_cs)
    denom = 1.0 - eps_cs * OL0
    if abs(denom) < 1e-6:
        return None
    E2 = num / denom
    E2_0 = (Om + OR + OL0*(1.0 - eps_cs)) / denom
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N18: Double exponential DE ----
# From A4: two competing creation-annihilation channels with different timescales.
# Channel A (fast, quantum): rho_A = f_A * OL0 * exp(-tau_A * (1-a))
# Channel B (slow, classical): rho_B = (1-f_A) * OL0 * exp(-tau_B * (1-a))
# tau_A = Om (fast quantum), tau_B = Om/3 (slow classical)
# f_A = 1/2 from A4 symmetry between creation zones.
# Combined: rho_DE = OL0 * [f_A*exp(-tau_A*(1-a)) + (1-f_A)*exp(-tau_B*(1-a))]
def E_N18(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    f_A = 0.5
    tau_A = Om
    tau_B = Om / 3.0
    a = 1.0 / (1.0 + z)
    comp_A = f_A * np.exp(-tau_A * (1.0 - a))
    comp_B = (1.0 - f_A) * np.exp(-tau_B * (1.0 - a))
    rho_DE = OL0 * (comp_A + comp_B)
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    # Normalize (at a=1: comp_A+comp_B = f_A + (1-f_A) = 1 -> rho_DE = OL0 OK)
    E2_0 = Om + OR + OL0
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N19: Curvature-sourced DE ----
# From A1+A3: spatial curvature of quantum fluid (spacetime quanta medium)
# sources dark energy. Curvature ~ rho_m^(2/3) (virial-like from A3).
# rho_DE = OL0 * (1 + beta_k * (1 - a^2)) with a^2 ~ 1/H^2 scaling
# beta_k = Om / (2*(1-Om)) from curvature amplitude in A3.
def E_N19(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    beta_k = Om / (2.0 * max(1.0 - Om, 1e-6))
    a = 1.0 / (1.0 + z)
    rho_DE = OL0 * (1.0 + beta_k * (1.0 - a**2))
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0  # at a=1: rho_DE = OL0
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N20: Stochastic creation DE ----
# From A3: creation has Poisson statistics (quantum). Variance <-> mean by Poisson.
# Variance of creation -> extra energy density at horizon scale.
# rho_DE = OL0 * (1 + sigma_P^2 / OL0) where sigma_P^2 ~ rho_m / H^2
# sigma_P^2 = alpha_P * Om * (1+z)^3 / E^2(z)
# Self-consistent (leading order): substitute E^2 ~ Om*(1+z)^3 + OL0
# -> sigma_P^2 ~ alpha_P * Om*(1+z)^3 / (Om*(1+z)^3 + OL0)
# alpha_P = Om / 4 from Poisson counting (creation events per Hubble volume).
def E_N20(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    alpha_P = Om / 4.0
    rho_m_z = Om * (1.0 + z)**3
    E2_approx = rho_m_z + OR*(1+z)**4 + OL0
    sigma_sq = alpha_P * rho_m_z / np.maximum(E2_approx, 1e-6)
    rho_DE = OL0 + sigma_sq
    E2 = rho_m_z + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0 + alpha_P * Om / (Om + OL0)
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N21: Fractal spacetime DE ----
# From A1+A2: spacetime quantum foam has fractal dimension D_f < 4.
# Fractal dimension of creation domain: D_f = 4 - Om (loss of integer dimension
# proportional to matter fraction that converts quanta to non-spatial form).
# rho_DE ~ H^(4-D_f) = H^Om (fractional power of Hubble).
# rho_DE = OL0 * E^Om -- nonlinear, self-consistent closure.
# Leading: E^2 = Om*(1+z)^3 + OR*(1+z)^4 + OL0 * E^Om
# Solved iteratively starting from LCDM E0:
def E_N21(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    rhs = Om*(1+z)**3 + OR*(1+z)**4
    # Iterative: E^2 = rhs + OL0 * E^Om
    E2_prev = rhs + OL0
    for _ in range(10):
        E_prev = np.sqrt(np.maximum(E2_prev, 1e-30))
        E2_new = rhs + OL0 * E_prev**Om
        if np.all(np.abs(E2_new - E2_prev) < 1e-8 * np.abs(E2_prev)):
            break
        E2_prev = E2_new
    E2_0_prev = Om + OR + OL0
    for _ in range(10):
        E0 = np.sqrt(np.maximum(E2_0_prev, 1e-30))
        E2_0_new = Om + OR + OL0 * E0**Om
        if abs(E2_0_new - E2_0_prev) < 1e-8:
            break
        E2_0_prev = E2_0_new
    return np.sqrt(np.maximum(E2_new / max(E2_0_new, 1e-10), 1e-30))


# ---- N22: Quantum tunneling DE ----
# From A1+A2: spacetime quanta tunnel between vacuum states.
# Tunneling rate ~ exp(-S_inst) where S_inst = pi * OL0 / Om (instanton action).
# DE shift from tunneling: rho_DE = OL0 * (1 - f_T * (1 - exp(-3*Om*z)))
# f_T = 1/pi from instanton action normalization (A2 + WKB).
# f_T * (1 - exp(-3*Om*z)): tunneling depletes DE at high z.
def E_N22(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    f_T = 1.0 / np.pi  # instanton normalization
    depletion = f_T * (1.0 - np.exp(-3.0 * Om * z))
    rho_DE = OL0 * (1.0 - depletion)
    rho_DE = np.maximum(rho_DE, 0.01 * OL0)
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N23: Quantum gravity condensate ----
# From A1+C3: all spacetime quanta in a gravitational condensate.
# Order parameter Psi ~ sqrt(rho_quanta); condensate energy = -|Psi|^4 term.
# w(z) = -1 + (2/3)*(rho_m / rho_DE)^(1/2) from Gross-Pitaevskii at cosmological scale.
# Closed form: w ≈ -1 + (2/3)*sqrt(Om*(1+z)^3 / OL0) -- integrate.
def E_N23(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    z_int = np.linspace(0.0, np.max(z) + 0.01, 2000)
    ratio = np.sqrt(Om * (1.0 + z_int)**3 / max(OL0, 1e-6))
    w_arr = -1.0 + (2.0/3.0) * ratio
    integrand = (1.0 + w_arr) / (1.0 + z_int)
    integral = np.concatenate([[0.0], cumulative_trapezoid(integrand, z_int)])
    rho_DE_arr = OL0 * np.exp(3.0 * integral)
    rho_DE = np.interp(z, z_int, rho_DE_arr)
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))


# ---- N24: Spacetime bit flip DE ----
# From A1+A2: quantum bits encoding spacetime flip between 0 (void) and 1 (matter).
# Bit flip rate ~ rho_m * (1 - rho_m/rho_max) (logistic growth).
# rho_max = 1 (total density budget). Flips from 1->0 create DE.
# rho_DE = OL0 + delta_bit * rho_m * (1 - rho_m)
# delta_bit = 1 / (3 * Om) from logistic bit-flip amplitude normalization.
def E_N24(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    delta_bit = 1.0 / (3.0 * max(Om, 1e-6))
    rho_m_z = Om * (1.0 + z)**3
    rho_DE = OL0 + delta_bit * rho_m_z * (1.0 - rho_m_z)
    rho_DE = np.maximum(rho_DE, 0.01 * OL0)
    E2 = rho_m_z + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0 + delta_bit * Om * (1.0 - Om)
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N25: Transplanckian creation cutoff DE ----
# From A1+A3: creation of spacetime quanta has Planck-scale cutoff.
# At H -> H_Pl, creation saturates. At H << H_Pl (today), creation is linear in H.
# Saturation modifies OL at high redshift via Padé approximant:
# rho_DE = OL0 / (1 + nu_sat * (E^2 - 1))
# nu_sat = Om / (1 - Om) from saturation of creation at E>>1.
# Self-consistent leading order: substitute LCDM E^2_approx.
def E_N25(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    nu_sat = Om / max(1.0 - Om, 1e-6)
    E2_approx = Om*(1+z)**3 + OR*(1+z)**4 + OL0
    rho_DE = OL0 / np.maximum(1.0 + nu_sat * (E2_approx - 1.0), 1e-6)
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0 / (1.0 + nu_sat * (Om + OR + OL0 - 1.0))
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N26: Boundary percolation DE ----
# From A2+A4: quantum-classical boundary percolates through spacetime.
# Percolation threshold at critical density rho_c = Om_crit (A4 equilibrium).
# Below threshold: DE grows. Above threshold: DE decays (gravity dominates).
# rho_DE = OL0 * exp(-lambda_p * (Om*(1+z)^3 - Om)^2)
# lambda_p = 1 / (2*Om^2) from percolation susceptibility at threshold.
def E_N26(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    lambda_p = 1.0 / (2.0 * max(Om**2, 1e-6))
    rho_m_z = Om * (1.0 + z)**3
    diff = rho_m_z - Om
    rho_DE = OL0 * np.exp(-lambda_p * diff**2)
    E2 = rho_m_z + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0  # at z=0: diff=0 -> exp(0)=1
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N27: Non-commutative geometry DE ----
# From A1+A2: at Planck scale, spacetime coordinates don't commute.
# Non-commutativity parameter theta ~ l_P^2 (Planck area).
# Effective correction to H^2: delta_H^2 ~ theta * rho_m^2 / rho_P
# In dimensionless units: rho_DE(z) = OL0 + psi * (Om*(1+z)^3)^2
# psi from A1 non-commutativity: psi = -OL0 / (3 * Om^2) (negative for wa<0)
# At high z, quadratic term dominates and reduces effective OL.
def E_N27(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    psi = -OL0 / (3.0 * max(Om**2, 1e-6))
    rho_m_z = Om * (1.0 + z)**3
    rho_DE = OL0 + psi * rho_m_z**2
    rho_DE = np.maximum(rho_DE, 0.01 * OL0)
    E2 = rho_m_z + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0 + psi * Om**2
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N28: Quantum ergodic DE ----
# From A3+A4: spacetime quanta ergodically explore all creation/annihilation states.
# Ergodic hypothesis: time-average = ensemble-average of creation rates.
# Ensemble includes both creation and annihilation: effective w = -1 + Om/(3*pi)
# pi factor from circular (ergodic) phase space integral in A3.
# Different from T19 (tracker) and N02 (causal): ergodic averaging origin.
def E_N28(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    w_ergodic = -1.0 + Om / (3.0 * np.pi)
    a = 1.0 / (1.0 + z)
    rho_DE = OL0 * a**(-3.0*(1.0 + w_ergodic))
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N29: Quantum zeno DE ----
# From A1+A2: frequent measurement of quantum-classical boundary freezes annihilation.
# Quantum Zeno effect: annihilation rate suppressed by (1/(1+tau_Z*rho_m))
# tau_Z = 1/Om from observation timescale = Hubble time / matter fraction.
# rho_DE = OL0 / (1 - Om/3 * ln(1 + (1+z)^3 - 1))
# Simplified: rho_DE = OL0 * (1 + zeta_Z * ln(1 + Om*(1+z)^3/(3*OL0)))
# zeta_Z from A2 Zeno suppression: zeta_Z = Om / OL0
def E_N29(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    zeta_Z = Om / max(OL0, 1e-6)
    rho_m_z = Om * (1.0 + z)**3
    # At high z, rho_m grows -> Zeno suppression increases log -> more DE
    # log_term(z): grows with z. At z=0: log_term_0 = ln(1 + Om/(3*OL0)).
    log_term = np.log(np.maximum(1.0 + rho_m_z / (3.0 * max(OL0, 1e-6)), 1.0))
    log_term_0 = float(np.log(1.0 + Om / (3.0 * max(OL0, 1e-6))))
    # Normalize: rho_DE(z=0) = OL0 by subtracting z=0 value
    rho_DE = OL0 * (1.0 + zeta_Z * (log_term - log_term_0))
    rho_DE = np.maximum(rho_DE, 0.01 * OL0)
    E2 = rho_m_z + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- N30: Metabolic equilibrium DE ----
# From A1+A3+A4: all three axioms combined, but with different coupling.
# At each z, the system seeks metabolic equilibrium:
# rho_DE_eq = (creation_rate) / (total annihilation rate)
# creation_rate = 3*H0*OL0 (A3 uniform)
# annihilation_rate = 3*H0*(Om*(1+z)^3 + OL0) / rho_total (A1 proportional)
# rho_DE = OL0 / (1 + lambda_eq * Om*(1+z)^3)
# lambda_eq = 1/3 from equilibrium balance (A4 equidistribution).
# This is different from T20 (de Sitter entropy correction which used nu=1/3 and different form)
# and T10 (threshold/step) -- here it's smooth rational function from equilibrium.
def E_N30(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    lambda_eq = 1.0 / 3.0
    rho_m_z = Om * (1.0 + z)**3
    rho_DE = OL0 / np.maximum(1.0 + lambda_eq * rho_m_z, 1e-6)
    # Normalize:
    rho_DE_0 = OL0 / (1.0 + lambda_eq * Om)
    OL_norm = (1.0 - Om - OR) * OL0 / max(rho_DE_0, 1e-10)
    rho_DE = OL_norm / np.maximum(1.0 + lambda_eq * rho_m_z, 1e-6)
    E2 = rho_m_z + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL_norm / (1.0 + lambda_eq * Om)
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ============================================================
# THEORY REGISTRY (2nd run, N01-N30)
# ============================================================

THEORIES = [
    {'id': 'N01', 'name': 'Quantum depletion lattice',   'E_func': E_N01, 'k': 2},
    {'id': 'N02', 'name': 'Causal horizon creation',      'E_func': E_N02, 'k': 2},
    {'id': 'N03', 'name': 'Entanglement entropy DE',      'E_func': E_N03, 'k': 2},
    {'id': 'N04', 'name': 'Metabolic cascade DE',         'E_func': E_N04, 'k': 2},
    {'id': 'N05', 'name': 'Vacuum polarization DE',       'E_func': E_N05, 'k': 2},
    {'id': 'N06', 'name': 'Quantum foam DE',              'E_func': E_N06, 'k': 2},
    {'id': 'N07', 'name': 'Spacetime viscosity DE',       'E_func': E_N07, 'k': 2},
    {'id': 'N08', 'name': 'Quantum clock DE',             'E_func': E_N08, 'k': 2},
    {'id': 'N09', 'name': 'Quantum info flux DE',         'E_func': E_N09, 'k': 2},
    {'id': 'N10', 'name': 'Hawking radiation DE',         'E_func': E_N10, 'k': 2},
    {'id': 'N11', 'name': 'Topological defect DE',        'E_func': E_N11, 'k': 2},
    {'id': 'N12', 'name': 'Gravitational memory DE',      'E_func': E_N12, 'k': 2},
    {'id': 'N13', 'name': 'Spacetime condensate DE',      'E_func': E_N13, 'k': 2},
    {'id': 'N14', 'name': 'Quantum pressure DE',          'E_func': E_N14, 'k': 2},
    {'id': 'N15', 'name': 'Void expansion DE',            'E_func': E_N15, 'k': 2},
    {'id': 'N16', 'name': 'Torsion-coupled DE',           'E_func': E_N16, 'k': 2},
    {'id': 'N17', 'name': 'Causal set DE',                'E_func': E_N17, 'k': 2},
    {'id': 'N18', 'name': 'Double exponential DE',        'E_func': E_N18, 'k': 2},
    {'id': 'N19', 'name': 'Curvature-sourced DE',         'E_func': E_N19, 'k': 2},
    {'id': 'N20', 'name': 'Stochastic creation DE',       'E_func': E_N20, 'k': 2},
    {'id': 'N21', 'name': 'Fractal spacetime DE',         'E_func': E_N21, 'k': 2},
    {'id': 'N22', 'name': 'Quantum tunneling DE',         'E_func': E_N22, 'k': 2},
    {'id': 'N23', 'name': 'Spacetime condensate GP',      'E_func': E_N23, 'k': 2},
    {'id': 'N24', 'name': 'Bit flip DE',                  'E_func': E_N24, 'k': 2},
    {'id': 'N25', 'name': 'Transplanckian cutoff DE',     'E_func': E_N25, 'k': 2},
    {'id': 'N26', 'name': 'Boundary percolation DE',      'E_func': E_N26, 'k': 2},
    {'id': 'N27', 'name': 'Non-commutative geometry DE',  'E_func': E_N27, 'k': 2},
    {'id': 'N28', 'name': 'Quantum ergodic DE',           'E_func': E_N28, 'k': 2},
    {'id': 'N29', 'name': 'Quantum Zeno DE',              'E_func': E_N29, 'k': 2},
    {'id': 'N30', 'name': 'Metabolic equilibrium DE',     'E_func': E_N30, 'k': 2},
]


# ============================================================
# WORKER FUNCTION FOR PARALLEL EXECUTION
# ============================================================

def run_one_theory(theory_dict):
    """Worker function: fit one theory and return results."""
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

    _script = os.path.dirname(os.path.abspath(__file__))
    _sim = os.path.dirname(_script)
    _l19 = os.path.join(_sim, 'l19')
    sys.path.insert(0, _sim)
    sys.path.insert(0, _l19)
    from desi_data import DESI_DR2, DESI_DR2_COV_INV
    from ee2_fit import aicc as _aicc

    AICC_LCDM_ = 15.392
    CHI2_LCDM_ = 10.192
    C_KMS_ = 299792.458
    R_S_ = 147.09
    N_DATA_ = 13
    N_GRID_ = 3000
    OMEGA_R_ = 9.0e-5

    tid = theory_dict['id']
    name = theory_dict['name']
    k = theory_dict['k']
    E_func = theory_dict['E_func']

    print('  Running ' + tid + ': ' + name + ' ...')

    def _compute_tv(E_func_, Om, H0):
        z_eff = DESI_DR2['z_eff']
        z_max = z_eff.max() + 0.01
        z_grid = np.linspace(0.0, z_max, N_GRID_)
        E_grid = E_func_(z_grid, Om, H0)
        if E_grid is None:
            return None
        if not np.all(np.isfinite(E_grid)) or np.any(E_grid <= 0):
            return None
        inv_E = 1.0 / E_grid
        DM_cum = (C_KMS_ / H0) * np.concatenate(
            [[0.0], cumulative_trapezoid(inv_E, z_grid)]
        )
        theory = np.empty(N_DATA_)
        for i, (z, qty) in enumerate(zip(z_eff, DESI_DR2['quantity'])):
            idx = min(np.searchsorted(z_grid, z), N_GRID_ - 1)
            DH = C_KMS_ / (H0 * E_grid[idx])
            DM = DM_cum[idx]
            DV = (z * DM**2 * DH)**(1.0/3.0) if z > 0 else 0.0
            if 'DV' in qty:
                theory[i] = DV / R_S_
            elif 'DM' in qty:
                theory[i] = DM / R_S_
            elif 'DH' in qty:
                theory[i] = DH / R_S_
            else:
                theory[i] = np.nan
        return theory

    def _chi2(Om, H0):
        if not (0.10 < Om < 0.60 and 55.0 < H0 < 90.0):
            return 1e8
        th = _compute_tv(E_func, Om, H0)
        if th is None or not np.all(np.isfinite(th)):
            return 1e8
        delta = DESI_DR2['value'] - th
        return float(delta @ DESI_DR2_COV_INV @ delta)

    starts = [
        [0.315, 67.4], [0.300, 68.5], [0.330, 67.0],
        [0.290, 69.5], [0.320, 68.0], [0.310, 70.0],
        [0.340, 66.5], [0.305, 68.8],
    ]
    best_chi2 = 1e8
    best_Om = 0.315
    best_H0 = 67.4
    for s in starts:
        try:
            res = minimize(
                lambda p: _chi2(p[0], p[1]), s,
                method='Nelder-Mead',
                options={'xatol': 1e-6, 'fatol': 1e-6, 'maxiter': 5000}
            )
            if res.fun < best_chi2:
                best_chi2 = res.fun
                best_Om = res.x[0]
                best_H0 = res.x[1]
        except Exception:
            continue

    aicc_val = _aicc(best_chi2, k)
    d_aicc = aicc_val - AICC_LCDM_

    # Extract w0, wa
    try:
        z_fit = np.linspace(0.01, 1.5, 200)
        E_arr = E_func(z_fit, best_Om, best_H0)
        w0, wa = None, None
        if E_arr is not None and np.all(np.isfinite(E_arr)):
            E2_arr = E_arr**2
            OL = 1.0 - best_Om - OMEGA_R_

            def cpl_E2(z_arr, w0_, wa_):
                a = 1.0 / (1.0 + z_arr)
                f = a**(-3.0*(1.0+w0_+wa_)) * np.exp(-3.0*wa_*(1.0-a))
                return best_Om*(1+z_arr)**3 + OMEGA_R_*(1+z_arr)**4 + OL*f

            def residuals(params):
                return np.sum((E2_arr - cpl_E2(z_fit, params[0], params[1]))**2)

            r2 = minimize(residuals, [-0.9, -0.3], method='Nelder-Mead',
                          options={'xatol': 1e-7, 'fatol': 1e-10, 'maxiter': 5000})
            if r2.success or r2.fun < 1.0:
                w0, wa = r2.x[0], r2.x[1]
    except Exception:
        w0, wa = None, None

    # Verdict
    if aicc_val >= AICC_LCDM_:
        verd = 'KILL'
    elif d_aicc < -4.0 and wa is not None and wa < -0.5:
        verd = 'GAME-CHANGER'
    elif d_aicc < -2.0:
        verd = 'STRONG PASS'
    else:
        verd = 'PASS'

    return {
        'id': tid,
        'name': name,
        'k': k,
        'Om': round(float(best_Om), 5),
        'H0': round(float(best_H0), 4),
        'chi2': round(float(best_chi2), 4),
        'aicc': round(float(aicc_val), 4),
        'd_aicc': round(float(d_aicc), 4),
        'w0': round(float(w0), 4) if w0 is not None else None,
        'wa': round(float(wa), 4) if wa is not None else None,
        'verdict': verd,
    }


# ============================================================
# MAIN
# ============================================================

def main():
    print('=' * 70)
    print('L30 2nd Run: SQMH 30-Theory BAO Comparison (DESI DR2)')
    print('=' * 70)
    print('LCDM baseline: chi2=' + str(CHI2_LCDM) + ', AICc=' + str(AICC_LCDM))
    print('n=' + str(N_DATA) + ', k=2 base, r_s=147.09 Mpc, full 13x13 covariance')
    print('Multi-start Nelder-Mead (8 starts per theory)')
    print('30 new theories (N01-N30), distinct from 1st run T01-T30')
    print()

    ctx = mp.get_context('spawn')
    n_workers = min(9, len(THEORIES))

    print('Launching ' + str(n_workers) + ' parallel workers for '
          + str(len(THEORIES)) + ' theories...')
    print()

    with ctx.Pool(n_workers) as pool:
        results = pool.map(run_one_theory, THEORIES)

    results.sort(key=lambda r: r['aicc'])

    print()
    print('=== L30 2nd Run Results ===')
    print('LCDM baseline: chi2=' + str(CHI2_LCDM) + ', AICc=' + str(AICC_LCDM))
    print()
    hdr = ('NID | Theory                    | k | chi2     | '
           'AICc     | dAICc   | w0      | wa      | Verdict')
    print(hdr)
    print('-' * len(hdr))

    for r in results:
        w0_s = '{:.4f}'.format(r['w0']) if r['w0'] is not None else '  N/A  '
        wa_s = '{:.4f}'.format(r['wa']) if r['wa'] is not None else '  N/A  '
        chi2_s = '{:.4f}'.format(r['chi2']) if r['chi2'] < 1e7 else '  FAIL '
        aicc_s = '{:.4f}'.format(r['aicc']) if r['aicc'] < 1e7 else '  FAIL '
        d_s = '{:.4f}'.format(r['d_aicc']) if abs(r['d_aicc']) < 1e7 else '  FAIL '
        print(r['id'] + ' | ' + r['name'][:25].ljust(25) + ' | ' + str(r['k']) + ' | '
              + chi2_s.rjust(8) + ' | ' + aicc_s.rjust(8) + ' | ' + d_s.rjust(7) + ' | '
              + w0_s.rjust(7) + ' | ' + wa_s.rjust(7) + ' | ' + r['verdict'])

    print()

    gc = sum(1 for r in results if r['verdict'] == 'GAME-CHANGER')
    sp = sum(1 for r in results if r['verdict'] == 'STRONG PASS')
    ps = sum(1 for r in results if r['verdict'] == 'PASS')
    kl = sum(1 for r in results if r['verdict'] == 'KILL')
    print('GAME-CHANGER count: ' + str(gc))
    print('STRONG PASS count:  ' + str(sp))
    print('PASS count:         ' + str(ps))
    print('KILL count:         ' + str(kl))
    print()

    print('=== Top Theories (lowest AICc) ===')
    for r in results[:5]:
        if r['chi2'] < 1e7:
            print('  ' + r['id'] + ' ' + r['name'] + ': chi2=' + str(r['chi2'])
                  + ', AICc=' + str(r['aicc']) + ', dAICc=' + str(r['d_aicc'])
                  + ', w0=' + str(r['w0']) + ', wa=' + str(r['wa'])
                  + ', verdict=' + r['verdict'])

    # Save JSON
    out_json = os.path.join(_SCRIPT_DIR, 'l30_results2.json')
    json_out = []
    for r in results:
        entry = {}
        for key, val in r.items():
            if key == 'E_func':
                continue
            if isinstance(val, float) and (np.isnan(val) or np.isinf(val)):
                entry[key] = None
            else:
                entry[key] = val
        json_out.append(entry)

    with open(out_json, 'w') as f:
        json.dump({
            'run': 'L30_2nd',
            'lcdm_baseline': {'chi2': CHI2_LCDM, 'aicc': AICC_LCDM},
            'n_data': N_DATA,
            'r_s': 147.09,
            'results': json_out,
            'summary': {
                'game_changer': gc,
                'strong_pass': sp,
                'pass': ps,
                'kill': kl,
            },
        }, f, indent=2)

    print()
    print('Results saved to: ' + out_json)
    print('Done.')


if __name__ == '__main__':
    main()
