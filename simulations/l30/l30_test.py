# -*- coding: utf-8 -*-
"""
l30_test.py -- L30 SQMH Fresh Theories (V01-V30)
=================================================
30 new theories derived from SQMH axioms A1-A4 + C1-C3.
CPT symmetry and holographic principle removed.

Explored directions:
- Asymmetric generation-annihilation rates
- Time-irreversible spacetime quantum dynamics
- Non-equilibrium void thermodynamics
- Reaction-diffusion dark energy
- Spacetime quantum number density evolution
- Bulk viscous dark fluid from annihilation pressure
- Quantum depletion zones around matter
- Scaling behavior of generation rate with cosmic time
- Statistical mechanics of spacetime quanta
- Annihilation cascade effects

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

# ── paths ──────────────────────────────────────────────────────────────────────
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SIM_DIR    = os.path.dirname(_SCRIPT_DIR)
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

from desi_data import DESI_DR2, DESI_DR2_COV_INV

# ── constants ──────────────────────────────────────────────────────────────────
C_KMS   = 299792.458
R_S     = 147.09
OR      = 5.38e-5   # radiation density (OMEGA_R_FID from ee2_ode)
N_DATA  = 13
N_GRID  = 4000
LCDM_BASELINE_CHI2  = 10.192
LCDM_BASELINE_AICC  = 15.392

# ── AICc ───────────────────────────────────────────────────────────────────────
def aicc(chi2_val, k, n=N_DATA):
    return chi2_val + 2*k + 2*k*(k+1)/(n - k - 1)

# ── BAO engine ─────────────────────────────────────────────────────────────────
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


def chi2_func(params, E_func, n_params=2, extra_bounds=None):
    """Chi-squared with full covariance."""
    Omega_m = params[0]
    H0      = params[1]

    if not (0.05 < Omega_m < 0.70 and 50.0 < H0 < 100.0):
        return 1e8

    if extra_bounds is not None:
        for j, (lo, hi) in enumerate(extra_bounds):
            if not (lo < params[2+j] < hi):
                return 1e8

    th = compute_theory_vector(Omega_m, H0, E_func)
    if th is None or not np.all(np.isfinite(th)):
        return 1e8
    delta = DESI_DR2['value'] - th
    return float(delta @ DESI_DR2_COV_INV @ delta)


def multi_start_optimize(chi2_wrapper, n_params=2, extra_starts=None):
    """Multi-start Nelder-Mead. Returns (Om, H0, [extras], chi2)."""
    base_starts = [
        [0.315, 67.4],
        [0.30,  68.0],
        [0.32,  69.0],
        [0.29,  70.0],
        [0.31,  68.5],
        [0.28,  71.0],
        [0.33,  67.0],
        [0.34,  66.5],
    ]

    if extra_starts is None:
        starts = base_starts
    else:
        starts = [b + e for b in base_starts for e in extra_starts]

    best_val = 1e8
    best_x   = None

    for s in starts:
        try:
            res = minimize(
                chi2_wrapper, s,
                method='Nelder-Mead',
                options={'xatol': 1e-6, 'fatol': 1e-6, 'maxiter': 5000},
            )
            if res.fun < best_val:
                best_val = res.fun
                best_x   = res.x
        except Exception:
            continue

    if best_x is None:
        return None, 1e8
    return best_x, best_val


# ==============================================================================
# THEORY DEFINITIONS
# Each theory returns (name, k, E_func_or_wrapper, extra_starts_for_k3+)
# E_func signature: E_func(z_array, Omega_m) -> E_array
# For k=2 theories: wrapper = lambda p: chi2_func(p, E_func)
# For k=3 theories: wrapper uses p[2] as extra param
# ==============================================================================


# ── V01: Asymmetric Annihilation Power Law ─────────────────────────────────────
# A1: matter annihilates SQ. A3: generation uniform. A4: net rate determines regime.
# If annihilation rate scales as (1+z)^alpha with alpha != 3 (non-standard):
# rho_DE / rho_crit0 = OL0 * (1 + z)^(3*(alpha-1)) correction factor
# E^2 = OR(1+z)^4 + Om(1+z)^3 + OL0*(asymmetric correction)
# Asymmetric generation: generation scales as (1+z)^beta with beta != 0
# Net: rho_net = rho_gen - rho_ann. For small asymmetry near LCDM:
# rho_DE = OL0_eff * exp(-gamma * ln(1+z)^2) [Gaussian suppression from non-equilibrium]
# This is a k=2 theory (gamma fixed by SQ thermodynamics: gamma = 1/pi from equipartition)
def V01_E(z_arr, Om):
    gamma = 1.0 / math.pi  # fixed: SQ equipartition argument
    OL0   = 1.0 - Om - OR
    ln1z  = np.log1p(z_arr)
    rho_DE = OL0 * np.exp(-gamma * ln1z**2)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0): return None
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V02: Time-Irreversible SQ Drift (Linear in ln a) ──────────────────────────
# A1+A3: irreversibility means generation builds up monotonically.
# In thermodynamic arrow-of-time picture, SQ density grows as ~ln(a).
# rho_DE(a) = OL0 * (1 + epsilon * ln(a)), with epsilon = 2/pi (from SQ entropy)
# epsilon fixed: entropy argument gives coefficient 2/pi
def V02_E(z_arr, Om):
    epsilon = 2.0 / math.pi  # fixed: entropy-based coefficient
    a_arr   = 1.0 / (1.0 + z_arr)
    OL0     = 1.0 - Om - OR
    rho_DE  = OL0 * (1.0 + epsilon * np.log(a_arr))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V03: Void Expansion Non-Equilibrium Thermodynamics ────────────────────────
# A3: generation spatially uniform in voids. Non-equilibrium: partial DE generation
# only in void fraction f_void(z). Void fraction evolves with structure formation.
# f_void ~ 1 - (Om*(1+z)^3 / E^2). Use self-consistent approximation:
# rho_DE = OL0 * [1 - nu * (1 - 1/(1+z)^3)]  with nu = 1 - 1/e (SQ depletion)
def V03_E(z_arr, Om):
    nu  = 1.0 - math.exp(-1.0)   # fixed: SQ depletion = 1 - 1/e
    OL0 = 1.0 - Om - OR
    rho_DE = OL0 * (1.0 - nu * (1.0 - 1.0/(1+z_arr)**3))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V04: Reaction-Diffusion Dark Energy ───────────────────────────────────────
# A1+A3: annihilation (reaction) + spatial spreading (diffusion) of SQ.
# In mean-field: rho_DE satisfies d rho_DE/dt = D*nabla^2 rho_DE - k_ann*rho_m*rho_DE
# In homogeneous FRW, diffusion averages: rho_DE evolves with effective equation of state
# w_eff = -1 + kappa where kappa = k_ann*rho_m0/(3H0) ~ Om / (3 * (1+Om))
# This gives w_eff fixed but non-(-1): w = -1 + Om/(3*(1+Om))
def V04_E(z_arr, Om):
    kappa = Om / (3.0 * (1.0 + Om))  # fixed reaction-diffusion coupling
    OL0   = 1.0 - Om - OR
    w_eff = -1.0 + kappa
    rho_DE = OL0 * (1+z_arr)**(3*(1+w_eff))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V05: SQ Number Density Boltzmann Evolution ────────────────────────────────
# A1: matter annihilates SQ quanta. Statistical mechanics: SQ follow modified
# Boltzmann equation. In cosmic time: n_SQ ~ exp(-integral of Gamma_ann dt)
# Gamma_ann ~ H * Om / (1+z)^3 * (1+z)^3 = H0 * Om (constant in proper time).
# Integral: n_SQ(a) = n_SQ0 * exp(-Om * H0 * t(a)) = n_SQ0 * exp(-Om * (2/3H0) * ...)
# Simplified: rho_DE = OL0 * exp(-Om * ln(1+z) / 2) = OL0 * (1+z)^(-Om/2)
def V05_E(z_arr, Om):
    OL0    = 1.0 - Om - OR
    rho_DE = OL0 * (1+z_arr)**(-Om/2.0)  # Om/2 is theory-derived exponent
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V06: Bulk Viscous Dark Fluid (Annihilation Pressure) ──────────────────────
# A1: annihilation creates pressure. Bulk viscosity: xi ~ rho_DE^(1/2) / H.
# Full viscous pressure: P_visc = -3*xi*H. This modifies w_eff:
# w_eff = -1 - 3*xi_hat where xi_hat = 1/(3*sqrt(3)) from SQ kinetic theory.
# Fixed: xi_hat = 1/(3*sqrt(3)) ~ 0.19245
def V06_E(z_arr, Om):
    xi_hat = 1.0 / (3.0 * math.sqrt(3.0))  # fixed: kinetic theory
    w_eff  = -1.0 - 3.0 * xi_hat
    OL0    = 1.0 - Om - OR
    rho_DE = OL0 * (1+z_arr)**(3*(1+w_eff))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V07: Quantum Depletion Zone (Yukawa-screened) ─────────────────────────────
# A1: matter depletes SQ in local region. Depletion zone has Yukawa profile.
# In FRW homogeneous limit, cumulative depletion:
# rho_DE = OL0 * (1 - Om * (1+z)^3 / (E^2 + m_SQ^2))
# where m_SQ is SQ Compton scale. For massless SQ limit (m_SQ -> 0):
# Solve iteratively. Leading order: rho_DE = OL0 * (1 - Om*(1+z)^3/E0^2)
# E0^2 = OR(1+z)^4 + Om(1+z)^3 + OL0. This is effectively V03-type.
# Instead, use exponential depletion: rho_DE = OL0 * (1+z)^(-delta) with delta from SQ mass.
# delta = pi/4 from SQ zero-point fluctuations (Casimir-type argument).
def V07_E(z_arr, Om):
    delta  = math.pi / 4.0   # fixed: SQ zero-point depletion exponent
    OL0    = 1.0 - Om - OR
    rho_DE = OL0 * (1+z_arr)**(-delta)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V08: Generation Rate Power-Law Scaling with Cosmic Time ───────────────────
# A3: generation uniform but rate can scale with cosmic time t ~ 1/H.
# Generation rate Gamma_gen = Gamma_0 * (H/H0)^alpha with alpha from dimensional analysis.
# A4: net = gen - ann. If alpha=2 (quadratic H scaling), rho_DE satisfies:
# d(rho_DE)/da = -3*(1+w0)*rho_DE/a + beta*H^2 where beta ~ OL0/H0^2.
# Self-consistent: w_eff = -(1 - OL0/3) (generation-dominated).
# k=2: both Om, H0 free, w_eff fixed by theory as w_eff = -(1 - OL0/(3*(OL0+OR))).
def V08_E(z_arr, Om):
    OL0   = 1.0 - Om - OR
    # w_eff from generation-dominated balance at z=0
    w_eff = -(1.0 - OL0 / max(3.0*(OL0 + OR + Om), 1e-10))
    w_eff = max(-2.0, min(-0.5, w_eff))   # physical clamp
    rho_DE = OL0 * (1+z_arr)**(3*(1+w_eff))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V09: Canonical Ensemble SQ (Partition Function) ───────────────────────────
# A1+A3: SQ obey canonical ensemble at temperature T_SQ = T_Planck * (H/H0).
# Partition function Z = (1 - exp(-1/kT))^(-N) gives rho ~ 1/(exp(H0/H)-1).
# In limit H >> H0: rho_DE ~ OL0 * H/H0 ~ OL0 * E (early times).
# In limit H ~ H0: rho_DE ~ OL0 (today). Interpolation:
# rho_DE = OL0 / (1 - exp(-1/E)) * (1 - exp(-1))   [normalized to OL0 at z=0]
# Self-consistently solved with E appearing in both sides.
def V09_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    normfac = 1.0 - math.exp(-1.0)
    # Use LCDM E as first approximation (iteration would be slow, use analytic approx)
    E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
    # rho_DE from canonical ensemble
    exponent = np.exp(-1.0 / np.maximum(E_lcdm, 1e-10))
    denom    = 1.0 - exponent
    denom    = np.maximum(denom, 1e-15)
    rho_DE   = OL0 * normfac / denom
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V10: Annihilation Cascade (Avalanche Depletion) ───────────────────────────
# A1: each annihilation event can trigger secondary annihilations (cascade).
# In mean field: effective annihilation rate multiplied by branching factor b > 1.
# Net: rho_DE decreases faster at high z (more matter, more cascades).
# rho_DE(z) = OL0 * exp(-b * Om * ((1+z)^3 - 1) / (3 * OL0))
# b fixed by threshold condition: at z_eq (matter-DE equality), cascade stops.
# z_eq: Om*(1+z)^3 = OL0 -> (1+z)^3 = OL0/Om. b chosen so cascade = 1 at z_eq.
def V10_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    # Cascade branching factor from threshold condition: b = 3*OL0/(OL0-Om)
    b = 3.0 * OL0 / max(OL0 - Om, 0.1)
    b = min(b, 10.0)  # physical cap
    exponent = b * Om * ((1+z_arr)**3 - 1.0) / (3.0 * max(OL0, 1e-6))
    rho_DE   = OL0 * np.exp(-exponent)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V11: SQ Fermi-Dirac Statistics (Quantum Degeneracy) ───────────────────────
# A1+A3: If SQ are fermions, Fermi-Dirac statistics caps their density.
# rho_DE = OL0 / (1 + exp(beta*(E-mu))) where mu is chemical potential.
# At z=0: E=1, rho_DE=OL0. Normalize: mu = 1/(1+exp(0)) = 1/2? No.
# Normalize: rho_DE(z=0) = OL0 enforced.
# Fermi function: f(E) = 1/(exp((E-1)*eta)+1) with eta = pi (Fermi energy = kT_Planck).
# Normalized: rho_DE = OL0 * f(E) / f(1)
def V11_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    eta    = math.pi   # fixed: SQ Fermi energy scale
    # Use LCDM E as proxy
    E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
    f_E  = 1.0 / (np.exp((E_lcdm - 1.0)*eta) + 1.0)
    f_1  = 1.0 / (math.exp(0.0) + 1.0)   # f(E=1) = 0.5
    rho_DE = OL0 * f_E / f_1
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V12: Non-Equilibrium Void Pressure (Osmotic) ──────────────────────────────
# A3+A4: spatial uniformity of generation implies osmotic pressure at void/matter boundary.
# Osmotic pressure: P_osm = -n_SQ * k_B * T_SQ (ideal gas SQ).
# Effective w_SQ = -1 + 1/(3*ln(1+z)) for z > 0, -1 at z=0.
# rho_DE = OL0 * exp(-(1+z)^3 / (3 * exp(1)))  [exponential suppression, e = Euler]
def V12_E(z_arr, Om):
    e      = math.e
    OL0    = 1.0 - Om - OR
    rho_DE = OL0 * np.exp(-((1+z_arr)**3 - 1.0) / (3.0 * e))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V13: SQ Density Wave Oscillation ──────────────────────────────────────────
# A1+A3: generation-annihilation balance can produce density waves in SQ field.
# Wave mode with frequency omega_SQ = sqrt(k^2 + m_SQ^2) / a.
# For long-wavelength mode (k->0): rho_DE oscillates around OL0.
# rho_DE = OL0 * (1 + alpha_osc * sin(phi_osc * ln(1+z)))
# alpha_osc fixed = 1/(2*pi) from SQ mass ~ H0 (m_SQ ~ H0 -> Compton ~ Hubble).
# phi_osc = 2*pi/ln(2) from half-oscillation over matter domination.
# k=2: both Om, H0 free, oscillation params theory-fixed.
def V13_E(z_arr, Om):
    alpha_osc = 1.0 / (2.0 * math.pi)
    phi_osc   = 2.0 * math.pi / math.log(2.0)
    OL0       = 1.0 - Om - OR
    rho_DE    = OL0 * (1.0 + alpha_osc * np.sin(phi_osc * np.log1p(z_arr)))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V14: Irreversible Entropy Production (Caratheodory) ───────────────────────
# A1: annihilation is irreversible. Total entropy grows as S ~ a^3 * H.
# By 2nd law (A3), the entropy production rate dS/dt > 0 modifies dark energy:
# rho_DE = OL0 * (1 + eta_irr * (1 - a))  where eta_irr = 2/(3*pi) from Caratheodory.
def V14_E(z_arr, Om):
    eta_irr = 2.0 / (3.0 * math.pi)
    OL0     = 1.0 - Om - OR
    a_arr   = 1.0 / (1.0 + z_arr)
    rho_DE  = OL0 * (1.0 + eta_irr * (1.0 - a_arr))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V15: Spacetime Quantum Diffusion-Drift ────────────────────────────────────
# A1+A3: SQ undergo diffusion (from generation) and drift (from annihilation gradient).
# Fokker-Planck equation for SQ density. Steady-state:
# rho_DE(z) = OL0 * (1 + z)^(-3*D_drift) where D_drift = (sqrt(5)-1)/2 (golden ratio).
# Golden ratio arises from the fixed-point condition of the FP equation.
def V15_E(z_arr, Om):
    phi_gr  = (math.sqrt(5.0) - 1.0) / 2.0   # golden ratio
    OL0     = 1.0 - Om - OR
    rho_DE  = OL0 * (1+z_arr)**(-3*phi_gr)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V16: SQ Quantum Number Conservation (Charge Analog) ───────────────────────
# A1+A2: if SQ carry conserved quantum number Q_SQ, then total Q_SQ conserved.
# Matter annihilates SQ but creates anti-SQ. Net Q conserved.
# rho_DE = rho_SQ - rho_aSQ. Asymmetry from initial conditions.
# n_SQ - n_aSQ = const = n_B0 (baryon-like asymmetry, fixed by cosmic initial conditions).
# Contribution: rho_asym = n_B0 * m_SQ * c^2. In Hubble units:
# rho_asym / rho_crit0 = Omega_B * f_asym where f_asym = 1/3 (equipartition).
# Net: rho_DE = OL0 - Omega_B * (1+z)^3 / 3 where Omega_B = 0.049 (fixed Planck 2018).
def V16_E(z_arr, Om):
    OL0     = 1.0 - Om - OR
    Om_B    = 0.049   # fixed: Planck 2018 baryon density
    f_asym  = 1.0/3.0  # fixed: equipartition
    rho_DE  = OL0 - Om_B * f_asym * ((1+z_arr)**3 - 1.0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V17: Matter-SQ Symbiosis (Metabolic Equilibrium) ──────────────────────────
# A1+A4: matter and SQ reach metabolic equilibrium. Rate equation:
# d rho_DE/dt = k_gen * rho_void - k_ann * rho_m * rho_DE / rho_crit
# At equilibrium: rho_DE = k_gen/k_ann * rho_void / rho_m
# = (OL0/Om) * (1+z)^(-3) * f(z)  where f(z) accounts for void fraction.
# rho_void ~ rho_crit - rho_m = rho_crit * (1 - Omega_m/E^2 * (1+z)^3)
# Leading order: rho_DE = OL0 * (1 - alpha_meta * (1+z)^3) where alpha_meta = Om/(3*OL0).
def V17_E(z_arr, Om):
    OL0        = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    alpha_meta = Om / (3.0 * max(OL0, 1e-6))
    rho_DE     = OL0 * (1.0 - alpha_meta * ((1+z_arr)**3 - 1.0))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V18: SQ Bose-Einstein Condensation ────────────────────────────────────────
# A1+A2: SQ bosons can condense. BEC critical temperature T_c ~ rho^(2/3).
# Below T_c: condensate fraction f_BEC grows. Above T_c: no condensate.
# rho_DE = rho_condensate + rho_normal
# rho_condensate = OL0 * (1 - (T/T_c)^3)  for T < T_c
# T ~ H (cosmic temperature proxy), T_c ~ H0 (today's critical)
# f_BEC(z) = 1 - E(z)^3 / E_c^3 clipped to [0,1]. E_c = 1 (today BEC just starts).
def V18_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    E2_lcdm  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E_lcdm   = np.sqrt(np.maximum(E2_lcdm, 1e-30))
    # BEC fraction = max(0, 1 - E^3)
    f_BEC    = np.maximum(0.0, 1.0 - E_lcdm**3)
    rho_DE   = OL0 * f_BEC
    # At z=0: E_lcdm ~ 1, f_BEC ~ 0 -> rho_DE ~ 0. Problem.
    # Fix: rho_DE = OL0 * (1 - f_BEC * (1 - 1/E_lcdm))
    # Rethink: condensate IS the dark energy. Normal component decays.
    # rho_DE = OL0 * (1 + (1 - 1/E_lcdm^3) * correction)
    # Simple fix: rho_DE = OL0 / E_lcdm^2  (condensate dilutes as E^2)
    # This gives OL0 at z=0 and decreases at high z.
    rho_DE   = OL0 / (E_lcdm**2)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V19: SQ Recombination Era (Phase Transition) ─────────────────────────────
# A2+A4: quantum-classical boundary shifts with cosmic epoch. At z_* ~ 1100 (CMB)
# a phase transition occurred in SQ. Post-transition DE density:
# rho_DE(z) = OL0 * theta(z_* - z) + rho_DE_old(z) * theta(z - z_*)
# Effective: rho_DE = OL0 * (1 - erf(ln(1+z) / sigma_PT))
# sigma_PT = ln(1+z_*) / sqrt(2*pi) ~ 3.13 from SQ recombination width.
def V19_E(z_arr, Om):
    from scipy.special import erf
    z_star   = 1100.0
    sigma_PT = math.log(1.0 + z_star) / math.sqrt(2.0 * math.pi)  # ~2.11
    OL0      = 1.0 - Om - OR
    rho_DE   = OL0 * (1.0 - erf(np.log1p(z_arr) / sigma_PT))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V20: Cosmic Time Power-Law Generation Rate ────────────────────────────────
# A3: generation rate scales with cosmic time as Gamma_gen ~ t^n.
# For n = -2 (dimensional analysis from [Gamma] = [1/t]):
# rho_DE(t) = rho_DE0 * (t/t0)^(2/3) during matter dom.
# (t/t0)^(2/3) ~ a, so rho_DE ~ OL0 * a^(1) = OL0 * (1+z)^(-1).
# This gives w = -2/3 at all times (power-law quintessence, theory-derived).
def V20_E(z_arr, Om):
    OL0    = 1.0 - Om - OR
    w_eff  = -2.0/3.0   # fixed: t^(-2) generation scaling
    rho_DE = OL0 * (1+z_arr)**(3*(1+w_eff))  # = OL0 * (1+z)^1
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V21: Stochastic SQ Noise (k=3: free noise amplitude) ─────────────────────
# A1+A3: generation has stochastic component (quantum noise). Noise adds
# a random-walk contribution to rho_DE. Over many Hubble times:
# rho_DE = OL0 + sigma_noise^2 * t ~ OL0 + C * ln(a) / H0^2.
# sigma_noise is a free parameter (noise amplitude), C = sigma_noise^2/H0.
# k=3: Om, H0 free + C_noise free.
def V21_E_factory(C_noise):
    def E_func(z_arr, Om):
        OL0    = 1.0 - Om - OR
        a_arr  = 1.0 / (1.0 + z_arr)
        rho_DE = OL0 + C_noise * np.log(a_arr)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func

# ── V22: Annihilation Saturation (Logistic) ───────────────────────────────────
# A1+A4: annihilation can't exceed generation rate - saturation effect.
# Logistic growth: drho_DE/dt = r*rho_DE*(1 - rho_DE/K) - k_ann*rho_m*rho_DE.
# Steady state: rho_DE = K * (1 - k_ann*rho_m/r).
# K = OL0/(1 - alpha_sat) where alpha_sat = Om/3 from dimensional analysis.
# Result: rho_DE = OL0 * (1 - Om/3 * (1+z)^3 / E^2) iterative.
# Approximation using LCDM E: rho_DE = OL0 * (1 - Om*(1+z)^3 / (3*E0^2)).
def V22_E(z_arr, Om):
    OL0     = 1.0 - Om - OR
    E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E0      = np.sqrt(np.maximum(E2_lcdm, 1e-30))
    rho_DE  = OL0 * (1.0 - Om*(1+z_arr)**3 / (3.0 * E0**2))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V23: SQ Grand Canonical Ensemble (free chemical potential as free param) ───
# A1+A3: SQ in grand canonical ensemble. Chemical potential mu controls
# SQ number. rho_DE = OL0 * z_GC(mu, T) / z_GC(mu0, T0) where z_GC is partition fn.
# For classical regime: rho_DE ~ OL0 * exp(mu/kT) ~ OL0 * exp(xi * E).
# At z=0: xi must satisfy rho_DE(0) = OL0 -> xi * 1 = 0 (trivial).
# Instead: rho_DE = OL0 * exp(xi * (1 - E)) / exp(0) = OL0 * exp(-xi*(E-1)).
# xi = free parameter (chemical potential). k=3.
def V23_E_factory(xi):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0:
            return None
        E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
        E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
        rho_DE  = OL0 * np.exp(-xi * (E_lcdm - 1.0))
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func

# ── V24: SQ Viscosity-Driven Acceleration (k=2) ───────────────────────────────
# A1+C2: momentum conservation of infalling SQ creates viscous dissipation.
# Shear viscosity eta ~ rho_DE * tau_SQ where tau_SQ = 1/H0 (Planck coherence time).
# Viscous EOS: w = -1 - (4/3)*eta*H/rho_DE = -1 - (4/3) * H/(H0) * (rho_DE)^(-1) * eta_0.
# At z=0: w_eff = -1 - 4/3 (diverges). Use truncated form: w_eff = -1/(1 + 4*H/(3*H0)).
# rho_DE satisfies: d ln rho_DE / d ln a = -3*(1+w) ~ 4 at low z.
# Simplified: rho_DE = OL0 / (1 + (4/3)*ln(1+z))
def V24_E(z_arr, Om):
    OL0    = 1.0 - Om - OR
    rho_DE = OL0 / (1.0 + (4.0/3.0)*np.log1p(z_arr))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V25: SQ Pair Production Near Matter (k=2) ─────────────────────────────────
# A1: matter annihilates SQ. Reverse: in high-curvature regions, SQ pairs can form.
# Net: annihilation dominates in high-density, pair-production in low density.
# In FRW: rho_DE has a contribution from pair production ~ Om*(1+z)^3 * coupling.
# rho_DE = OL0 + lambda_pair * Om * (1+z)^3 where lambda_pair = -1/3 (Schwinger).
# lambda_pair = -1/(4*pi) from pair-production threshold in SQ field theory.
def V25_E(z_arr, Om):
    lambda_p = -1.0 / (4.0 * math.pi)  # fixed: SQ pair production
    OL0      = 1.0 - Om - OR
    rho_DE   = OL0 + lambda_p * Om * ((1+z_arr)**3 - 1.0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V26: Non-Equilibrium Dark Energy from Annihilation Pressure (k=3) ─────────
# A1+A4: Annihilation pressure drives DE away from equilibrium.
# rho_DE = OL0 * (1 + alpha_p * (1+z)^s - alpha_p) normalized to OL0 at z=0.
# Both alpha_p and s are free -> k=4 is too many. Fix s = 3/2 (half matter scaling).
# alpha_p is free parameter. k=3.
def V26_E_factory(alpha_p):
    s = 1.5  # fixed: half-matter scaling
    def E_func(z_arr, Om):
        OL0    = 1.0 - Om - OR
        rho_DE = OL0 * (1.0 + alpha_p * ((1+z_arr)**s - 1.0))
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func

# ── V27: Hubble-Tension Resolution via SQ Inflow (k=2) ────────────────────────
# A1+C2: SQ inflow asymmetry creates effective Hubble parameter shift.
# H_eff(z) = H(z) * (1 + epsilon_inf * exp(-z/z_c)) where z_c = 0.5 (inflow range).
# epsilon_inf = -Om/(2*pi) from SQ momentum conservation (C2).
# This modifies E_eff = H_eff/H0.
def V27_E(z_arr, Om):
    epsilon_inf = -Om / (2.0 * math.pi)
    z_c         = 0.5   # fixed: inflow coherence scale
    OL0         = 1.0 - Om - OR
    E2_base     = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E_base      = np.sqrt(np.maximum(E2_base, 1e-30))
    E_eff       = E_base * (1.0 + epsilon_inf * np.exp(-z_arr / z_c))
    E_eff       = np.maximum(E_eff, 1e-15)
    return E_eff

# ── V28: Lense-Thirring Dark Energy (C3 angular momentum) ─────────────────────
# C3: rotating matter creates asymmetric SQ annihilation -> Lense-Thirring.
# In cosmic average, random orientation. Net effect: DE density enhanced near
# angular momentum concentrations. Cosmic average:
# rho_DE = OL0 * (1 + alpha_LT * J_cosmic(z)) where J_cosmic ~ Om * (1+z)^2 (
# angular momentum scales as a^2 during structure formation).
# alpha_LT = 1/(4*pi) from LT precession formula in C3 limit.
def V28_E(z_arr, Om):
    alpha_LT = 1.0 / (4.0 * math.pi)
    OL0      = 1.0 - Om - OR
    rho_DE   = OL0 * (1.0 + alpha_LT * Om * ((1+z_arr)**2 - 1.0))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V29: SQ Thermal Equilibration Time-Scale (k=2) ───────────────────────────
# A1+A3: SQ reach thermal equilibrium on time-scale tau_eq ~ 1/(sigma_SQ * n_m).
# n_m ~ Om * H^2 / G. When H * tau_eq >> 1 (early times), SQ not in eq.
# rho_DE = OL0 * tanh(tau_eq * H)^2 = OL0 * tanh(E)^2 (normalized at z=0 via tanh(1)^2).
def V29_E(z_arr, Om):
    OL0      = 1.0 - Om - OR
    E2_lcdm  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E_lcdm   = np.sqrt(np.maximum(E2_lcdm, 1e-30))
    tanh_1_sq = math.tanh(1.0)**2
    rho_DE   = OL0 * np.tanh(E_lcdm)**2 / tanh_1_sq
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))

# ── V30: Interacting SQ+Matter with Free Coupling (k=3) ───────────────────────
# A1+A4: direct SQ-matter interaction with coupling strength q (free).
# drho_DE/dN = -3*rho_DE + q*rho_m (matter transfers to DE).
# drho_m/dN  = -3*rho_m - q*rho_m  (matter loses to DE).
# Coupled solution: rho_DE(z) = OL0*(1+z)^0 + q/(q+3) * Om * ((1+z)^(-q)-(1+z)^0)...
# Simplified: solve drho_DE/da numerically.
# ODE: y[0] = rho_m, y[1] = rho_DE.
# d y[0]/da = (-3/a) * y[0] - (q/a) * y[0]
# d y[1]/da = (q/a) * y[0]
# Analytic: y[0] = Om*(1+z)^(3+q), y[1] = OL0 + Om*q/(q)*(-(1+z)^(3+q) + 1)... careful.
# Exact: y[1] = OL0 + Om*q/(q) * ( (1+z)^3 / ... )
# Full analytic for d rho_DE / d ln a = q * rho_m:
# rho_m = Om * a^(-3-q), rho_DE = OL0 + Om*(a^(-3-q) - 1) * q/3 ...
# Careful: drho_m/dlna = -(3+q)*rho_m => rho_m = Om*(1+z)^(3+q).
# drho_DE/dlna = q*rho_m = q*Om*(1+z)^(3+q).
# Integrate: rho_DE(z) = OL0_eff + integral.
# rho_DE(z) = OL0 - q*Om/(3+q) * ((1+z)^(3+q) - 1)  + (initial cond at z=0)
# At z=0: rho_DE(0) = OL0 -> consistent. OL0_eff = 1 - Om - OR.
# For conservation: E^2 = OR(1+z)^4 + rho_m + rho_DE.
# rho_m + rho_DE = Om*(1+z)^(3+q) + OL0 - q*Om/(3+q)*((1+z)^(3+q)-1).
# = OL0 + Om*(1+z)^(3+q)*(1 - q/(3+q)) + q*Om/(3+q)
# = OL0 + q*Om/(3+q) + Om*(3/(3+q))*(1+z)^(3+q).
def V30_E_factory(q):
    def E_func(z_arr, Om):
        OL0    = 1.0 - Om - OR
        if abs(3+q) < 1e-8:
            return None
        rho_m   = Om * (1+z_arr)**(3+q)
        rho_DE  = OL0 - q * Om / (3+q) * ((1+z_arr)**(3+q) - 1.0)
        E2 = OR*(1+z_arr)**4 + rho_m + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ==============================================================================
# WORKER FUNCTION
# ==============================================================================

def worker_fn(args):
    """Runs in a separate process."""
    os.environ['OMP_NUM_THREADS']     = '1'
    os.environ['MKL_NUM_THREADS']     = '1'
    os.environ['OPENBLAS_NUM_THREADS']= '1'
    np.seterr(all='ignore')
    warnings.filterwarnings('ignore')

    vid, theory_name, k, E_func, extra_starts = args

    try:
        if k == 2:
            def wrapper(p):
                return chi2_func(p, E_func)
            x_best, chi2_best = multi_start_optimize(wrapper, n_params=2)
            if x_best is None:
                return {'id': vid, 'name': theory_name, 'k': k,
                        'chi2': 1e8, 'aicc': 1e8, 'Om': None, 'H0': None,
                        'extra': None, 'status': 'FAIL'}
            Om_best, H0_best = x_best[0], x_best[1]
            extra_best = None

        else:  # k == 3
            # extra_starts is list of [extra_param_guess]
            def wrapper(p):
                extra_p = [p[2]]
                E_fn    = E_func(p[2])  # factory call
                return chi2_func(p[:2], E_fn)

            def full_wrapper(p):
                try:
                    E_fn = E_func(p[2])
                    return chi2_func(p[:2], E_fn)
                except Exception:
                    return 1e8

            combined_starts = []
            base_Om_H0 = [
                [0.315, 67.4], [0.30, 68.0], [0.32, 69.0],
                [0.29, 70.0],  [0.31, 68.5], [0.28, 71.0],
                [0.33, 67.0],  [0.34, 66.5],
            ]
            for b in base_Om_H0:
                for e in extra_starts:
                    combined_starts.append(b + e)

            best_val = 1e8
            best_x   = None
            for s in combined_starts:
                try:
                    res = minimize(
                        full_wrapper, s,
                        method='Nelder-Mead',
                        options={'xatol': 1e-6, 'fatol': 1e-6, 'maxiter': 5000},
                    )
                    if res.fun < best_val:
                        best_val = res.fun
                        best_x   = res.x
                except Exception:
                    continue

            if best_x is None:
                return {'id': vid, 'name': theory_name, 'k': k,
                        'chi2': 1e8, 'aicc': 1e8, 'Om': None, 'H0': None,
                        'extra': None, 'status': 'FAIL'}
            Om_best, H0_best = best_x[0], best_x[1]
            chi2_best = best_val
            extra_best = float(best_x[2])

        aicc_val = aicc(chi2_best, k)
        d_aicc   = aicc_val - LCDM_BASELINE_AICC
        status   = 'PASS' if aicc_val < LCDM_BASELINE_AICC else 'KILL'

        return {
            'id':     vid,
            'name':   theory_name,
            'k':      k,
            'chi2':   float(chi2_best),
            'aicc':   float(aicc_val),
            'd_aicc': float(d_aicc),
            'Om':     float(Om_best),
            'H0':     float(H0_best),
            'extra':  extra_best,
            'status': status,
        }
    except Exception as ex:
        return {'id': vid, 'name': theory_name, 'k': k,
                'chi2': 1e8, 'aicc': 1e8, 'd_aicc': 1e8,
                'Om': None, 'H0': None, 'extra': None,
                'status': 'ERROR', 'error': str(ex)}


# ==============================================================================
# THEORY LIST
# ==============================================================================

def build_theory_list():
    theories = [
        # (vid, name, k, E_func_or_factory, extra_starts_for_k3)
        ('V01', 'Asymmetric Annihilation Gaussian', 2, V01_E, None),
        ('V02', 'Time-Irreversible SQ Drift', 2, V02_E, None),
        ('V03', 'Void Non-Equilibrium Thermodynamics', 2, V03_E, None),
        ('V04', 'Reaction-Diffusion Dark Energy', 2, V04_E, None),
        ('V05', 'SQ Boltzmann Evolution', 2, V05_E, None),
        ('V06', 'Bulk Viscous Annihilation Pressure', 2, V06_E, None),
        ('V07', 'Quantum Depletion Zone Yukawa', 2, V07_E, None),
        ('V08', 'Generation Rate H-Power Scaling', 2, V08_E, None),
        ('V09', 'Canonical Ensemble SQ', 2, V09_E, None),
        ('V10', 'Annihilation Cascade Avalanche', 2, V10_E, None),
        ('V11', 'SQ Fermi-Dirac Statistics', 2, V11_E, None),
        ('V12', 'Void Osmotic Pressure', 2, V12_E, None),
        ('V13', 'SQ Density Wave Oscillation', 2, V13_E, None),
        ('V14', 'Irreversible Entropy Production', 2, V14_E, None),
        ('V15', 'SQ Fokker-Planck Diffusion-Drift', 2, V15_E, None),
        ('V16', 'SQ Quantum Number Conservation', 2, V16_E, None),
        ('V17', 'Matter-SQ Metabolic Equilibrium', 2, V17_E, None),
        ('V18', 'SQ Bose-Einstein Condensation', 2, V18_E, None),
        ('V19', 'SQ Recombination Phase Transition', 2, V19_E, None),
        ('V20', 'Cosmic Time Power-Law Generation', 2, V20_E, None),
        # k=3 theories
        ('V21', 'Stochastic SQ Noise', 3, V21_E_factory, [[-0.5], [-0.1], [0.1], [0.5], [1.0], [-1.0]]),
        ('V22', 'Annihilation Saturation Logistic', 2, V22_E, None),
        ('V23', 'SQ Grand Canonical Ensemble', 3, V23_E_factory, [[0.5], [1.0], [2.0], [-0.5], [-1.0], [3.0]]),
        ('V24', 'SQ Viscosity-Driven Acceleration', 2, V24_E, None),
        ('V25', 'SQ Pair Production Near Matter', 2, V25_E, None),
        ('V26', 'Non-Equil DE Annihilation Pressure', 3, V26_E_factory, [[0.1], [0.3], [-0.1], [-0.3], [0.5], [-0.5]]),
        ('V27', 'SQ Inflow Hubble-Tension', 2, V27_E, None),
        ('V28', 'Lense-Thirring Dark Energy', 2, V28_E, None),
        ('V29', 'SQ Thermal Equilibration', 2, V29_E, None),
        ('V30', 'Interacting SQ+Matter Coupling', 3, V30_E_factory, [[0.1], [0.5], [-0.1], [-0.5], [1.0], [2.0]]),
    ]
    return theories


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    out_dir   = _SCRIPT_DIR
    json_path = os.path.join(out_dir, 'l30_results.json')

    theories  = build_theory_list()
    task_args = []
    for vid, name, k, E_func_or_factory, extra_starts in theories:
        task_args.append((vid, name, k, E_func_or_factory, extra_starts))

    print('=' * 65)
    print('L30 SQMH Theory Test (V01-V30)')
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
    print('{:<5} {:<38} {:>2} {:>9} {:>9} {:>8} {:>6}'.format(
        'ID', 'Theory', 'k', 'chi2', 'AICc', 'dAICc', 'Status'))
    print('-' * 82)
    pass_count = 0
    kill_count = 0
    for r in results:
        chi2_str  = '{:.4f}'.format(r['chi2'])  if r['chi2'] < 1e7 else 'FAIL'
        aicc_str  = '{:.4f}'.format(r['aicc'])  if r['aicc'] < 1e7 else 'FAIL'
        daicc_str = '{:.4f}'.format(r['d_aicc']) if r.get('d_aicc', 1e8) < 1e7 else 'FAIL'
        print('{:<5} {:<38} {:>2} {:>9} {:>9} {:>8} {:>6}'.format(
            r['id'], r['name'][:38], r['k'],
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
