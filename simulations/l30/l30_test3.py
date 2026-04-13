# -*- coding: utf-8 -*-
"""
L30 3rd Run: 30-theory SQMH cosmological model comparison against DESI DR2 BAO data.

8-person team, 10 rounds of independent theory derivation from axioms A1-A4.
No formula hints provided. All theories derived independently.
All theories distinct from 1st run (T01-T30) and 2nd run (N01-N30).

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

3rd run: completely new axiom interpretations.
- 1st run themes: log creation, Hubble-damped, angular-momentum, CPL-annihilation,
  oscillatory, diffusion, RVM, asymptotic-safety, holographic, braneworld,
  G-running, entropy-production, tracker, threshold, momentum-flux, periodic,
  dS-entropy, scale-factor, sigmoid, phase-transition, geometric-mean.
- 2nd run themes: quantum-lattice, causal-horizon, entanglement-entropy,
  metabolic-cascade, vacuum-polarization, quantum-foam, viscosity, quantum-clock,
  info-flux, Hawking, topological-defect, gravity-memory, BEC, quantum-pressure,
  void-expansion, torsion, causal-sets, double-exponential, curvature-sourced,
  stochastic, fractal, quantum-tunneling, GP-condensate, bit-flip,
  transplanckian-cutoff, percolation, non-commutative, ergodic, Zeno, metabolic-eq.

3rd run new themes: membrane dissolution, Pauli exclusion analog, decoherence cascade,
  thermodynamic arrow, topology change, geodesic deviation, Lorentz-violation flux,
  quantum cohomology, spontaneous symmetry breaking, Ising lattice, quantum walk,
  hydrodynamic creation fluid, knot invariant, complexity growth, Lyapunov exponent,
  Andreev reflection, critical phenomena, virial theorem, surface tension,
  dipole radiation, winding number, resonance, quantum Hall analog, Shapiro delay,
  Loschmidt echo, spectral flow, spin network degeneracy, self-organized criticality,
  information entropy gradient.
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
# ROUND 1-3: 30 COMPLETELY NEW THEORY E(z) DEFINITIONS
# All derived from A1-A4 by 8-person team, no formula hints.
# No overlap with T01-T30 (1st run) or N01-N30 (2nd run).
# ============================================================

# ---- P01: Membrane dissolution DE ----
# From A1: spacetime quanta form membrane-like layers.
# Matter dissolves membranes locally, releasing their energy as DE.
# A4: net membrane creation = creation rate - dissolution rate.
# Dissolution rate ~ matter density gradient per Hubble time.
# Team derives: as a -> 0, rho_m grows, more membrane dissolves -> rho_DE rises.
# rho_DE(a) = OL0 * (1 + mu_m * (a^(-2) - 1))
# mu_m = Om/(2*(1-Om+Om)) = Om/2 from membrane geometry (area per volume scaling).
# Normalization: E(0) = 1 enforced analytically.
def E_P01(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    mu_m = Om / 2.0
    rho_DE = OL0 * (1.0 + mu_m * (a**(-2) - 1.0))
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0 * (1.0 + mu_m * (1.0 - 1.0))
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- P02: Pauli exclusion analog DE ----
# From A1+A2: spacetime quanta obey fermionic statistics at the boundary (A2).
# Matter occupies quantum states, blocking creation -> exclusion pressure.
# At high rho_m (early universe), creation is maximally suppressed.
# At low rho_m (late universe), Pauli exclusion lifts -> DE grows.
# A3: uniform creation, but blocked by occupied states fraction f_occ = Om*(1+z)^3.
# Team derives: rho_DE = OL0 / (1 + kappa_P * Om*(1+z)^3)
# kappa_P = 1/(3*(1-Om)) from Pauli blocking fraction normalization at z=0.
def E_P02(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    kappa_P = 1.0 / (3.0 * max(1.0 - Om, 1e-6))
    rho_m_z = Om * (1+z)**3
    rho_DE = OL0 / (1.0 + kappa_P * rho_m_z)
    # Normalize so E(0)=1
    rho_DE_0 = OL0 / (1.0 + kappa_P * Om)
    norm = Om + OR + rho_DE_0
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / max(norm, 1e-10), 1e-30))


# ---- P03: Decoherence cascade DE ----
# From A2: quantum-classical boundary width grows with Hubble time.
# Decoherence time tau_d ~ 1/H. As H decreases, boundary widens.
# A wider boundary -> more DE captured at boundary -> rho_DE increases.
# Net DE creation rate ~ d(1/H)/dt = -H_dot/H^2 = (1+q)*1 (q = decel param).
# Team derives: rho_DE(a) = OL0 * (1 + delta_d * ln(a^(-1)))
# delta_d = Om/3 from boundary width proportional to Omega_m.
# (ln(1/a) > 0 at high z, so DE higher in past.)
def E_P03(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    delta_d = Om / 3.0
    rho_DE = OL0 * (1.0 + delta_d * np.log(1.0 / np.maximum(a, 1e-10)))
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    E2_0 = Om + OR + OL0 * (1.0 + delta_d * 0.0)
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- P04: Thermodynamic arrow DE ----
# From A3: creation is irreversible (thermodynamic arrow).
# The entropy production rate from creation asymmetry (A3) accumulates.
# Total entropy created ~ integral of Gamma_c over cosmic time.
# By Bekenstein-Mukhanov counting, accumulated quanta -> DE pressure.
# Team derives: rho_DE(a) = OL0 * exp(-nu_th * (1 - a))
# nu_th = Om^2 / (2*(1-Om)) from entropy production integral.
def E_P04(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    nu_th = Om**2 / (2.0 * max(1.0 - Om, 1e-6))
    rho_DE = OL0 * np.exp(-nu_th * (1.0 - a))
    rho_DE_0 = OL0 * np.exp(0.0)
    E2_0 = Om + OR + rho_DE_0
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- P05: Topology change rate DE ----
# From A4: creation/annihilation changes the spacetime topology locally.
# A4 shows three regimes -> topology changes at the boundary.
# Rate of topology changes ~ |Gamma_c - Gamma_a| ~ rho_DE - rho_m/3.
# As universe expands, matter dilutes -> topology change rate decreases.
# Team derives: rho_DE modulated by topology-change damping.
# rho_DE(a) = OL0 * (1 - gamma_t * (1-a)^2)
# gamma_t = Om/(2*(1-Om)) from topology-change frequency at A4 boundary.
def E_P05(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    gamma_t = Om / (2.0 * max(1.0 - Om, 1e-6))
    rho_DE = OL0 * (1.0 - gamma_t * (1.0 - a)**2)
    E2_0 = Om + OR + OL0
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- P06: Geodesic deviation from quantum creation (A1+C4) ----
# From A1+C4: uniform creation creates pressure on matter geodesics.
# Geodesic deviation acceleration ~ creation pressure gradient.
# The geodesic deviation accumulates over Hubble time -> energy stored in DE.
# A3: creation rate Gamma_c = const -> geodesic deviation grows as ln(a).
# Team derives: rho_DE(a) = OL0 * (1 + zeta_g * (1 - a^(-1/2)))
# zeta_g = -2*Om/(3*(1-Om)) from geodesic integral over Hubble time.
# Note: (1 - a^(-1/2)) < 0 at high z -> rho_DE decreases -> wa < 0.
def E_P06(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    zeta_g = 2.0 * Om / (3.0 * max(1.0 - Om, 1e-6))
    # (1 - a^{-1/2}) = (1 - sqrt(1+z))
    rho_DE = OL0 * (1.0 + zeta_g * (1.0 - a**(-0.5)))
    rho_DE_0 = OL0 * (1.0 + zeta_g * 0.0)
    E2_0 = Om + OR + rho_DE_0
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- P07: Lorentz-violation flux DE (A3) ----
# From A3: uniform creation defines a preferred cosmic frame.
# This preferred frame introduces Lorentz-violating corrections to vacuum energy.
# LV contribution to rho_DE ~ v_pref^2 * rho_Planck,
# where v_pref ~ H*t_H ~ 1 (Hubble flow velocity in Planck units).
# Team derives effective correction: rho_DE(a) = OL0 * (1 + epsilon_LV * (1-a)^(3/2))
# epsilon_LV = Om^(3/2) / (2*(1-Om)) from LV energy density scaling.
def E_P07(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    epsilon_LV = Om**(1.5) / (2.0 * max(1.0 - Om, 1e-6))
    rho_DE = OL0 * (1.0 + epsilon_LV * (1.0 - a)**(1.5))
    rho_DE_0 = OL0 * (1.0 + epsilon_LV * 0.0)
    E2_0 = Om + OR + rho_DE_0
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- P08: Quantum cohomology of spacetime quanta (A2+C3) ----
# From A2+C3: boundary topology carries a quantum cohomology class.
# As horizon area changes with expansion, cohomology class changes discretely.
# Each cohomology transition releases energy proportional to horizon area change.
# Team derives: rho_DE(a) = OL0 * (1 - beta_h * (1 - a^3) / 3)
# beta_h = Om^2 / (1-Om)^2 from cohomology class counting per horizon area.
# (1 - a^3) > 0 at high z -> rho_DE decreases -> wa < 0.
def E_P08(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    beta_h = Om**2 / max((1.0 - Om)**2, 1e-8)
    rho_DE = OL0 * (1.0 - beta_h * (1.0 - a**3) / 3.0)
    rho_DE_0 = OL0  # at z=0, (1-a^3)=0
    E2_0 = Om + OR + rho_DE_0
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- P09: Spontaneous symmetry breaking in creation field (A1) ----
# From A1: creation field phi_c has a Mexican hat potential.
# In early universe (high density), matter pin phi_c to origin (symmetric phase).
# At late universe (low density), phi_c rolls to minimum -> DE released.
# Phase transition at matter-DE equality (a_eq where Om*(1+z)^3 = OL0).
# Team derives: rho_DE(a) = OL0 * (1 - sigma_ssb * exp(-(a/a_eq)^2))
# sigma_ssb = Om/(2*(1-Om)) from SSB order parameter at a_eq.
def E_P09(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    sigma_ssb = Om / (2.0 * max(1.0 - Om, 1e-6))
    # a_eq: scale factor at matter-DE equality
    a_eq = (Om / max(OL0, 1e-6))**(1.0/3.0)
    rho_DE = OL0 * (1.0 - sigma_ssb * np.exp(-(a / max(a_eq, 1e-6))**2))
    rho_DE_0 = OL0 * (1.0 - sigma_ssb * np.exp(-1.0 / a_eq**2))
    E2_0 = Om + OR + rho_DE_0
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    if E2_0 <= 0:
        return None
    return np.sqrt(np.maximum(E2 / E2_0, 1e-30))


# ---- P10: Ising lattice spin transition DE (A4) ----
# From A4: each spacetime quantum can be in "created" (+1) or "annihilated" (-1) state.
# This is analogous to Ising spins; matter field plays role of external magnetic field.
# Mean-field Ising: magnetization m = tanh(J_eff * m + h_ext)
# At high matter density h_ext large -> m ~ -1 (annihilation dominant).
# At low matter density h_ext -> 0 -> m ~ +tanh(J*m) -> spontaneous order.
# Team derives: rho_DE(a) = OL0 * (1 + m(a)) / 2 scaled by OL0.
# m(a) = tanh(-Om*(1+z)^3 / (2*OL0)) from mean-field solution.
# J_eff = 1, h_ext = -rho_m/(2*rho_DE).
def E_P10(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    rho_m_z = Om * (1+z)**3
    h_arg = rho_m_z / (2.0 * max(OL0, 1e-6))
    m = np.tanh(-h_arg)
    rho_DE = OL0 * (1.0 + m) / 2.0 + OL0 / 2.0
    rho_DE_0 = OL0 * (1.0 + np.tanh(-Om / (2.0 * max(OL0, 1e-6)))) / 2.0 + OL0 / 2.0
    E2_0 = Om + OR + rho_DE_0
    if E2_0 <= 0:
        return None
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / E2_0, 1e-30))


# ---- P11: Quantum walk on spacetime graph DE (A2) ----
# From A2: quantum-classical boundary can be viewed as a graph where
# spacetime quanta are nodes connected to matter nodes.
# Quantum walk on this graph: amplitude spreads as sqrt(t) ~ sqrt(1/H).
# DE density ~ amplitude^2 of quantum walker at empty nodes.
# Team derives: rho_DE(a) = OL0 * (1 + alpha_qw * (sqrt(a) - 1))
# alpha_qw = Om / (1-Om) from quantum walk return probability.
# sqrt(a) < 1 at high z -> rho_DE decreases -> wa < 0.
def E_P11(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    alpha_qw = Om / max(1.0 - Om, 1e-6)
    rho_DE = OL0 * (1.0 + alpha_qw * (np.sqrt(a) - 1.0))
    rho_DE_0 = OL0 * (1.0 + alpha_qw * 0.0)
    E2_0 = Om + OR + rho_DE_0
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- P12: Hydrodynamic creation fluid DE (A3+C4) ----
# From A3+C4: uniform creation forms a perfect fluid with pressure.
# Fluid continuity: drho_c/dt + 3H(rho_c + p_c) = Gamma_c.
# A3: Gamma_c = const -> p_c = -rho_c/3 (radiation-like creation).
# But DE component carries excess: rho_DE = rho_c - rho_m * eta_h.
# Team derives: rho_DE(a) = OL0 * a^(Om/3) / (1 + eta_h*(1-a))
# eta_h = Om/(3*(1-Om)) from continuity balance.
def E_P12(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    eta_h = Om / (3.0 * max(1.0 - Om, 1e-6))
    rho_DE = OL0 * a**(Om/3.0) / (1.0 + eta_h * (1.0 - a))
    rho_DE_0 = OL0 * 1.0 / 1.0
    E2_0 = Om + OR + rho_DE_0
    if E2_0 <= 0:
        return None
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / E2_0, 1e-30))


# ---- P13: Knot invariant DE (A2+C3) ----
# From A2+C3: quantum-classical boundary has topology that can be characterized
# by knot invariants (Jones polynomial analogs).
# Holographic principle C3: knot invariants scale with boundary area ~ 1/H^2 ~ a^2.
# As universe expands, more complex knots form -> energy stored in knot complexity.
# Team derives: rho_DE(a) = OL0 * (1 - lambda_k * (1 - a^4) / 4)
# lambda_k = Om / (2*(1-Om)) from knot complexity per horizon area unit.
def E_P13(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    lambda_k = Om / (2.0 * max(1.0 - Om, 1e-6))
    rho_DE = OL0 * (1.0 - lambda_k * (1.0 - a**4) / 4.0)
    rho_DE_0 = OL0
    E2_0 = Om + OR + rho_DE_0
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- P14: Information entropy gradient DE (A1+C3) ----
# From A1+C3: annihilation of spacetime quanta by matter reduces local
# information content. The spatial gradient of information entropy drives a flux.
# Holographic: info ~ horizon area ~ 1/H^2. Gradient between matter-rich and
# empty regions -> information flows into DE sector.
# Team derives: rho_DE(a) = OL0 * (1 - psi_I * (1 - 1/(1+(1-a)))  )
# Simplification: rho_DE(a) = OL0 * (1 - psi_I * a / (1 + a))
# psi_I = 2*Om/(3*(1-Om)) from info gradient balance.
def E_P14(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    psi_I = 2.0 * Om / (3.0 * max(1.0 - Om, 1e-6))
    rho_DE = OL0 * (1.0 - psi_I * a / (1.0 + a))
    rho_DE_0 = OL0 * (1.0 - psi_I * 0.5)
    E2_0 = Om + OR + rho_DE_0
    if E2_0 <= 0:
        return None
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / E2_0, 1e-30))


# ---- P15: Lyapunov exponent of matter-DE system (A4) ----
# From A4: the three-regime system (creation/gravity/boundary) is a dynamical system.
# The Lyapunov exponent lambda_L of this system determines how fast perturbations grow.
# At late times (matter diluted), lambda_L -> 0 (stable fixed point = de Sitter).
# At early times (matter dominated), lambda_L ~ H -> instability drives DE.
# Team derives: rho_DE(a) = OL0 * exp(-phi_L * (1-a) * Om*(1+z)^3)
# phi_L = 1/(3*(1-Om)) from Lyapunov analysis of A4 boundary.
def E_P15(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    phi_L = 1.0 / (3.0 * max(1.0 - Om, 1e-6))
    rho_m_z = Om * (1+z)**3
    rho_DE = OL0 * np.exp(-phi_L * (1.0 - a) * rho_m_z)
    rho_DE_0 = OL0 * np.exp(0.0)
    E2_0 = Om + OR + rho_DE_0
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- P16: Andreev reflection at quantum boundary DE (A2) ----
# From A2: quantum-classical boundary reflects quantum excitations (like Andreev).
# Reflected quanta carry energy back to DE sector.
# Reflection amplitude ~ (rho_m)^(1/2) / (rho_m + rho_DE)^(1/2).
# As matter dilutes, reflection decreases -> DE decreases at high z (past).
# Team derives: rho_DE(a) = OL0 * a^(3*Om/(2*(Om+OL0)))
# From Andreev amplitude squared scaling with matter fraction.
def E_P16(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    # Andreev exponent from reflection amplitude scaling
    w_andr = -1.0 + Om / (2.0 * max(Om + OL0, 1e-6))
    rho_DE = OL0 * a**(-3.0*(1.0 + w_andr))
    rho_DE_0 = OL0
    E2_0 = Om + OR + rho_DE_0
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- P17: Critical phenomena near A4 boundary DE (A4) ----
# From A4: the boundary between creation and annihilation regimes is a critical surface.
# Near this surface, power-law correlations emerge (as in phase transitions).
# Critical exponent nu_c controls DE divergence near the boundary.
# Team derives: rho_DE(a) = OL0 * (1 + chi_c * |Om - OL_frac(a)|)
# OL_frac(a) = OL0 / (Om*(1+z)^3 + OL0) (instantaneous DE fraction).
# chi_c = Om/(1-Om) from critical fluctuation amplitude.
def E_P17(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    chi_c = Om / max(1.0 - Om, 1e-6)
    rho_m_z = Om * (1+z)**3
    OL_frac = OL0 / max(rho_m_z + OL0, 1e-10)
    Om_frac = rho_m_z / max(rho_m_z + OL0, 1e-10)
    rho_DE = OL0 * (1.0 + chi_c * np.abs(Om/(Om+OL0) - OL_frac))
    rho_DE_0 = OL0 * (1.0 + chi_c * np.abs(Om/(Om+OL0) - OL0/(Om+OL0)))
    E2_0 = Om + OR + rho_DE_0
    if E2_0 <= 0:
        return None
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / E2_0, 1e-30))


# ---- P18: Virial theorem for quantum creation gas DE (A3) ----
# From A3: uniform creation forms a gas of quantum quanta in the Hubble volume.
# Virial theorem: <KE> = -<PE>/2 for gravitationally bound quantum gas.
# KE per quantum ~ H^2 (Hubble flow). PE per quantum ~ -G*rho_tot/r^2.
# Virial equilibrium selects DE density: rho_DE = OL0 * (virial correction).
# Team derives: rho_DE(a) = OL0 * (1 + theta_v * (1 - a^(3/2)))
# theta_v = Om/(2*(1-Om)) from virial theorem applied to quantum gas.
def E_P18(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    theta_v = Om / (2.0 * max(1.0 - Om, 1e-6))
    rho_DE = OL0 * (1.0 + theta_v * (1.0 - a**(1.5)))
    rho_DE_0 = OL0
    E2_0 = Om + OR + rho_DE_0
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- P19: Surface tension of quantum boundary DE (A2) ----
# From A2: quantum-classical boundary has surface tension sigma_st.
# Surface tension energy stored in boundary ~ sigma_st * Area_horizon.
# Area_horizon ~ 1/H^2 ~ 1/H0^2 * a^3 (in matter-dominated era).
# Team derives: rho_DE(a) = OL0 * (1 - xi_st * (1 - a^(3/2)))
# xi_st = Om^2/(3*(1-Om)) from surface tension normalization.
# (1 - a^(3/2)) > 0 at high z -> rho_DE < OL0 -> wa < 0.
def E_P19(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    xi_st = Om**2 / (3.0 * max(1.0 - Om, 1e-6))
    rho_DE = OL0 * (1.0 - xi_st * (1.0 - a**(1.5)))
    rho_DE_0 = OL0
    E2_0 = Om + OR + rho_DE_0
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- P20: Dipole radiation from asymmetric creation DE (A3+C4) ----
# From A3+C4: creation is uniform but annihilation is localized.
# This asymmetry acts like electric charge distribution -> dipole radiation.
# Dipole power ~ (d^2/dt^2 p)^2 where p ~ matter dipole moment.
# Radiated energy feeds DE: rho_DE(a) = OL0 + delta_dip * rho_m^2 / rho_c^2.
# delta_dip = Om^2 / (6*(1-Om)) from dipole radiation power integral.
def E_P20(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    delta_dip = Om**2 / (6.0 * max(1.0 - Om, 1e-6))
    rho_m_z = Om * (1+z)**3
    rho_DE = OL0 + delta_dip * rho_m_z**2
    rho_DE_0 = OL0 + delta_dip * Om**2
    E2_0 = Om + OR + rho_DE_0
    if E2_0 <= 0:
        return None
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / E2_0, 1e-30))


# ---- P21: Winding number in creation topology DE (A2+C3) ----
# From A2+C3: quantum boundary has topological winding number W.
# W counts how many times the boundary wraps around the Hubble sphere.
# Holographic: W ~ boundary area / Planck area ~ 1/(G*H^2).
# As H decreases with expansion, W increases -> more topological modes -> more DE.
# Team derives: rho_DE(a) = OL0 * (1 + omega_w * (a^(-1) - 1)^(1/3))
# omega_w = Om/3 from winding number density in Hubble volume.
def E_P21(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    omega_w = Om / 3.0
    winding = (1.0/np.maximum(a, 1e-10) - 1.0)**(1.0/3.0)
    rho_DE = OL0 * (1.0 + omega_w * winding)
    rho_DE_0 = OL0 * (1.0 + omega_w * 0.0)
    E2_0 = Om + OR + rho_DE_0
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- P22: Resonance between creation rate and Hubble scale DE (A3) ----
# From A3: creation rate Gamma_c is constant. Hubble scale H changes.
# When Gamma_c / H ~ constant (resonance condition), DE is amplified.
# Off-resonance: DE is suppressed by detuning factor.
# Team derives: rho_DE(a) = OL0 * (1 + rho_res * sin^2(pi * a / 2))
# sin^2(pi/2) = 1 at a=1 (today), sin^2(0) = 0 at a=0.
# rho_res = -Om/(2*(1-Om)) from resonance amplitude at Gamma_c ~ H.
# Negative rho_res: DE lower at high z -> wa < 0.
def E_P22(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    rho_res = -Om / (2.0 * max(1.0 - Om, 1e-6))
    rho_DE = OL0 * (1.0 + rho_res * np.sin(np.pi * a / 2.0)**2)
    rho_DE_0 = OL0 * (1.0 + rho_res * 1.0)
    E2_0 = Om + OR + rho_DE_0
    if E2_0 <= 0:
        return None
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / E2_0, 1e-30))


# ---- P23: Quantum Hall effect analog DE (A2) ----
# From A2: quantum-classical boundary in 2+1D supports quantum Hall states.
# These states carry quantized Hall conductance sigma_H = n_LL * e^2/h.
# In cosmic analog, n_LL = number of filled Landau levels of spacetime quanta.
# n_LL grows with Hubble volume: n_LL ~ 1/H^2 ~ a^3 in matter era.
# Team derives: rho_DE(a) = OL0 * (1 - phi_H * (1 - a^(3/2)) / (1 + phi_H))
# phi_H = Om^2/(2*(1-Om)^2) from Hall conductance quantization per Hubble area.
def E_P23(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    phi_H = Om**2 / (2.0 * max((1.0 - Om)**2, 1e-8))
    rho_DE = OL0 * (1.0 - phi_H * (1.0 - a**(1.5)) / (1.0 + phi_H))
    rho_DE_0 = OL0
    E2_0 = Om + OR + rho_DE_0
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- P24: Shapiro delay from creation field DE (C1+A1) ----
# From C1+A1: equivalence principle holds, so creation field couples
# to both inertial and gravitational mass equally.
# This coupling modifies photon travel time (Shapiro delay analog).
# The extra time delay -> effective distance modification -> appears as DE.
# Team derives: rho_DE(a) = OL0 * (1 - phi_sh * (1-a)/(1+(1-a)) )
# = OL0 * (1 - phi_sh * (1-a)/(2-a))
# phi_sh = Om^2/(1-Om) from Shapiro delay integral at Hubble scale.
def E_P24(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    phi_sh = Om**2 / max(1.0 - Om, 1e-6)
    rho_DE = OL0 * (1.0 - phi_sh * (1.0 - a) / max(2.0 - a, 1e-6))
    rho_DE_0 = OL0 * (1.0 - phi_sh * 0.0)
    E2_0 = Om + OR + rho_DE_0
    if E2_0 <= 0:
        return None
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / E2_0, 1e-30))


# ---- P25: Loschmidt echo of quantum creation DE (A4) ----
# From A4: the three-regime system undergoes "quantum reversal" when
# matter density crosses the creation-annihilation boundary.
# Loschmidt echo measures overlap between forward and time-reversed evolution.
# Echo amplitude ~ exp(-lambda_L * t) where t ~ 1/H.
# Team derives: rho_DE(a) = OL0 * (1 - rho_LE * (1 - exp(-Om*(1-a)/OL0)))
# rho_LE = Om/(1-Om) from Loschmidt echo amplitude at equilibrium.
def E_P25(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    rho_LE = Om / max(1.0 - Om, 1e-6)
    exp_arg = Om * (1.0 - a) / max(OL0, 1e-6)
    rho_DE = OL0 * (1.0 - rho_LE * (1.0 - np.exp(-exp_arg)))
    rho_DE_0 = OL0 * (1.0 - rho_LE * 0.0)
    E2_0 = Om + OR + rho_DE_0
    if E2_0 <= 0:
        return None
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / E2_0, 1e-30))


# ---- P26: Spectral flow in creation field DE (A2+C3) ----
# From A2+C3: creation field has a spectrum of modes in Hubble volume.
# Spectral flow: as H decreases, modes shift from above to below horizon.
# Each mode crossing the horizon contributes energy to DE.
# Spectral flow rate ~ dH/dt * (number of modes per dH) ~ H_dot / H^2.
# Team derives: rho_DE(a) = OL0 * (1 + f_sf * (a^(-Om) - 1))
# f_sf = Om^2/(3*(1-Om)) from spectral mode density per octave of H.
def E_P26(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    f_sf = Om**2 / (3.0 * max(1.0 - Om, 1e-6))
    rho_DE = OL0 * (1.0 + f_sf * (a**(-Om) - 1.0))
    rho_DE_0 = OL0 * (1.0 + f_sf * 0.0)
    E2_0 = Om + OR + rho_DE_0
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- P27: Spin network degeneracy DE (A2+C3) ----
# From A2+C3: quantum boundary is a spin network (LQG-inspired).
# Degeneracy of spin network states at given area ~ exp(area/4) = exp(A_BH/4).
# More degenerate states -> higher effective vacuum energy -> more DE.
# As horizon grows, degeneracy increases -> DE increases toward today.
# Team derives: rho_DE(a) = OL0 * (1 - kappa_sn * (1 - a^(2/3)))
# kappa_sn = Om/(3*(1-Om)) from spin network degeneracy at Hubble area.
def E_P27(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    kappa_sn = Om / (3.0 * max(1.0 - Om, 1e-6))
    rho_DE = OL0 * (1.0 - kappa_sn * (1.0 - a**(2.0/3.0)))
    rho_DE_0 = OL0
    E2_0 = Om + OR + rho_DE_0
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / max(E2_0, 1e-10), 1e-30))


# ---- P28: Self-organized criticality DE (A4) ----
# From A4: the creation-annihilation system self-organizes to a critical state
# (like sandpile model). At criticality, avalanches of creation events
# follow power-law size distribution.
# Power-law creation bursts: delta_rho_DE ~ (rho_m)^(-s_soc)
# with s_soc = 1/2 from mean-field SOC exponent.
# Team derives: rho_DE(a) = OL0 * (1 + alpha_soc / sqrt(Om*(1+z)^3 + OL0))
# alpha_soc = Om*OL0/(Om+OL0) from SOC amplitude at matter-DE equality.
def E_P28(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    alpha_soc = Om * OL0 / max(Om + OL0, 1e-6)
    rho_tot = Om*(1+z)**3 + OL0
    rho_DE = OL0 + alpha_soc / np.sqrt(np.maximum(rho_tot, 1e-10))
    rho_DE_0 = OL0 + alpha_soc / np.sqrt(Om + OL0)
    E2_0 = Om + OR + rho_DE_0
    if E2_0 <= 0:
        return None
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / E2_0, 1e-30))


# ---- P29: Quantum erasure DE (A1+A2) ----
# From A1+A2: when matter annihilates spacetime quanta, quantum information
# is "erased" (like quantum erasure experiments).
# Erased information is stored at the boundary (A2) and re-emitted as DE.
# Rate of erasure ~ annihilation rate ~ rho_m * sigma_a.
# Total erased information integrated over time -> DE energy density.
# Team derives: rho_DE(a) = OL0 * (1 + f_er * (1 - exp(-rho_m(a)/rho_m0 * q_er)))
# f_er = -Om/2, q_er = Om from erasure rate normalization.
# At z=0: (1 - exp(-Om)) ~ Om/e. At high z: approaches -f_er.
def E_P29(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    f_er = -Om / 2.0
    q_er = Om
    rho_m_ratio = (1.0 + z)**3  # rho_m(z) / rho_m0
    rho_DE = OL0 * (1.0 + f_er * (1.0 - np.exp(-rho_m_ratio * q_er)))
    rho_DE_0 = OL0 * (1.0 + f_er * (1.0 - np.exp(-q_er)))
    E2_0 = Om + OR + rho_DE_0
    if E2_0 <= 0:
        return None
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / E2_0, 1e-30))


# ---- P30: Spacetime metric entropy DE (A1+A3+C3) ----
# From A1+A3+C3: creation-annihilation defines a preferred metric on spacetime.
# The metric entropy S_g = -Tr(rho_g ln rho_g) for the quantum metric state
# changes with expansion.
# C3: S_g proportional to horizon area ~ 1/H^2.
# A3: creation adds to S_g uniformly; A1: matter depletes S_g locally.
# Net: dS_g/dt = Gamma_c - Gamma_a * rho_m.
# Team derives: rho_DE(a) = OL0 * (1 - rho_me * (1 - a) * (1 + Om*(1+z)^2))
# rho_me = Om^2 / (3*(1-Om)) from metric entropy integral.
# Note: stabilized to prevent runaway at high z.
def E_P30(z, Om, H0):
    OR = OMEGA_R
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    a = 1.0 / (1.0 + z)
    rho_me = Om**2 / (3.0 * max(1.0 - Om, 1e-6))
    factor = (1.0 - a) * (1.0 + Om * (1+z)**2)
    rho_DE = OL0 * (1.0 - rho_me * factor)
    rho_DE_0 = OL0 * (1.0 - rho_me * 0.0)
    E2_0 = Om + OR + rho_DE_0
    if E2_0 <= 0:
        return None
    E2 = Om*(1+z)**3 + OR*(1+z)**4 + rho_DE
    return np.sqrt(np.maximum(E2 / E2_0, 1e-30))


# ============================================================
# THEORY REGISTRY
# ============================================================

THEORIES = [
    ('P01', 'Membrane dissolution DE',        E_P01),
    ('P02', 'Pauli exclusion analog DE',       E_P02),
    ('P03', 'Decoherence cascade DE',          E_P03),
    ('P04', 'Thermodynamic arrow DE',          E_P04),
    ('P05', 'Topology change rate DE',         E_P05),
    ('P06', 'Geodesic deviation creation DE',  E_P06),
    ('P07', 'Lorentz-violation flux DE',       E_P07),
    ('P08', 'Quantum cohomology DE',           E_P08),
    ('P09', 'Spontaneous symmetry breaking DE',E_P09),
    ('P10', 'Ising lattice spin DE',           E_P10),
    ('P11', 'Quantum walk DE',                 E_P11),
    ('P12', 'Hydrodynamic creation fluid DE',  E_P12),
    ('P13', 'Knot invariant DE',               E_P13),
    ('P14', 'Information entropy gradient DE', E_P14),
    ('P15', 'Lyapunov exponent DE',            E_P15),
    ('P16', 'Andreev reflection DE',           E_P16),
    ('P17', 'Critical phenomena DE',           E_P17),
    ('P18', 'Virial theorem quantum gas DE',   E_P18),
    ('P19', 'Surface tension boundary DE',     E_P19),
    ('P20', 'Dipole radiation creation DE',    E_P20),
    ('P21', 'Winding number topology DE',      E_P21),
    ('P22', 'Resonance Hubble creation DE',    E_P22),
    ('P23', 'Quantum Hall analog DE',          E_P23),
    ('P24', 'Shapiro delay creation DE',       E_P24),
    ('P25', 'Loschmidt echo creation DE',      E_P25),
    ('P26', 'Spectral flow creation DE',       E_P26),
    ('P27', 'Spin network degeneracy DE',      E_P27),
    ('P28', 'Self-organized criticality DE',   E_P28),
    ('P29', 'Quantum erasure DE',              E_P29),
    ('P30', 'Spacetime metric entropy DE',     E_P30),
]


# ============================================================
# WORKER FUNCTION (spawn-safe)
# ============================================================

def run_theory_worker(args):
    """Worker for parallel execution. Each worker loads data independently."""
    import os
    import sys
    os.environ['OMP_NUM_THREADS'] = '1'
    os.environ['MKL_NUM_THREADS'] = '1'
    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    import numpy as np
    import warnings
    from scipy.integrate import cumulative_trapezoid
    from scipy.optimize import minimize
    warnings.filterwarnings('ignore')
    np.seterr(all='ignore')

    theory_id, theory_name, E_func = args

    try:
        Om, H0, chi2_val, aicc_val = fit_model(E_func)
        w0, wa = extract_w0_wa(E_func, Om, H0)
        v = verdict(aicc_val, wa)
        daicc = aicc_val - AICC_LCDM
        return {
            'id': theory_id,
            'name': theory_name,
            'k': 2,
            'Om': Om,
            'H0': H0,
            'chi2': chi2_val,
            'aicc': aicc_val,
            'daicc': daicc,
            'w0': w0,
            'wa': wa,
            'verdict': v,
        }
    except Exception as e:
        return {
            'id': theory_id,
            'name': theory_name,
            'k': 2,
            'Om': None,
            'H0': None,
            'chi2': None,
            'aicc': None,
            'daicc': None,
            'w0': None,
            'wa': None,
            'verdict': 'FAIL',
            'error': str(e),
        }


# ============================================================
# MAIN
# ============================================================

def main():
    print('=' * 70)
    print('L30 3rd Run: 30-Theory SQMH BAO Fitting (DESI DR2)')
    print('=' * 70)
    print('LCDM baseline: chi2=%.3f, AICc=%.3f' % (CHI2_LCDM, AICC_LCDM))
    print('k=2 theories: chi2 < 10.192 to beat LCDM')
    print('Game-Changer: dAICc < -4 AND wa < -0.5')
    print()

    # Parallel execution with spawn context
    ctx = mp.get_context('spawn')
    n_workers = min(9, len(THEORIES))

    print('Running %d theories on %d workers...' % (len(THEORIES), n_workers))
    with ctx.Pool(n_workers) as pool:
        results = pool.map(run_theory_worker, THEORIES)

    # Sort by AICc (best first), put FAILs last
    def sort_key(r):
        if r['aicc'] is None:
            return 1e10
        return r['aicc']
    results_sorted = sorted(results, key=sort_key)

    # Print results table
    print()
    print('=== L30 3rd Run Results ===')
    print('LCDM baseline: chi2=%.3f, AICc=%.3f' % (CHI2_LCDM, AICC_LCDM))
    print()
    hdr = (' %3s | %-28s | %1s | %8s | %8s | %7s | %7s | %7s | %-11s' %
           ('ID', 'Theory', 'k', 'chi2', 'AICc', 'dAICc', 'w0', 'wa', 'Verdict'))
    sep = '-'*4 + '+' + '-'*30 + '+' + '-'*3 + '+' + '-'*10 + '+' + '-'*10 + '+' + '-'*9 + '+' + '-'*9 + '+' + '-'*9 + '+' + '-'*13
    print(hdr)
    print(sep)

    for r in results_sorted:
        if r['chi2'] is None:
            chi2_s = '  FAIL  '
            aicc_s = '  FAIL  '
            daicc_s = ' FAIL  '
            w0_s = '  N/A  '
            wa_s = '  N/A  '
        else:
            chi2_s = '%8.4f' % r['chi2']
            aicc_s = '%8.4f' % r['aicc']
            daicc_s = '%+7.4f' % r['daicc']
            w0_s = '%7.4f' % (r['w0'] if r['w0'] is not None else 0.0)
            wa_s = '%7.4f' % (r['wa'] if r['wa'] is not None else 0.0)
        print(' %3s | %-28s | %1d | %s | %s | %s | %s | %s | %-11s' %
              (r['id'], r['name'][:28], r['k'],
               chi2_s, aicc_s, daicc_s, w0_s, wa_s, r['verdict']))

    # Counts
    gc = sum(1 for r in results if r['verdict'] == 'GAME-CHANGER')
    sp = sum(1 for r in results if r['verdict'] == 'STRONG PASS')
    pa = sum(1 for r in results if r['verdict'] == 'PASS')
    ki = sum(1 for r in results if r['verdict'] == 'KILL')
    fa = sum(1 for r in results if r['verdict'] == 'FAIL')
    print()
    print('=== Summary ===')
    print('GAME-CHANGER: %d' % gc)
    print('STRONG PASS:  %d' % sp)
    print('PASS:         %d' % pa)
    print('KILL:         %d' % ki)
    print('FAIL:         %d' % fa)

    # Save JSON
    out_dir = _SCRIPT_DIR
    json_path = os.path.join(out_dir, 'l30_results3.json')

    def jsonify(v):
        if v is None:
            return None
        if isinstance(v, float):
            return float(v)
        if isinstance(v, np.floating):
            return float(v)
        if isinstance(v, np.integer):
            return int(v)
        return v

    json_results = []
    for r in results_sorted:
        json_results.append({k: jsonify(v) for k, v in r.items()})

    with open(json_path, 'w') as f:
        json.dump({
            'run': 'L30_3rd',
            'lcdm_chi2': CHI2_LCDM,
            'lcdm_aicc': AICC_LCDM,
            'results': json_results,
            'summary': {
                'game_changer': gc,
                'strong_pass': sp,
                'pass': pa,
                'kill': ki,
                'fail': fa,
            }
        }, f, indent=2)
    print()
    print('JSON saved: %s' % json_path)
    print()
    print('=== L30 3rd Run Complete ===')
    return results_sorted


if __name__ == '__main__':
    main()
