# -*- coding: utf-8 -*-
"""
l30_test4.py -- L30 4th Run SQMH Fresh Theories (Y01-Y30)
==========================================================
30 new theories derived from SQMH axioms A1-A4 + C1-C3.
COMPLETELY different mechanisms from V, W, X series.

Explored NEW directions:
- SQ field renormalization group (RG) fixed points
- Bifurcation cascade (period-doubling) in generation rate
- Heteroclinic orbits connecting annihilation attractors
- Strange attractor in void dynamics (Lorenz-type)
- Excitable medium dynamics (FitzHugh-Nagumo type)
- Wavefront propagation of annihilation boundary
- Cellular automaton rules for SQ generation
- Graph-theoretic connectivity of void networks
- Epidemic spreading model for annihilation events
- Predator-prey dynamics (Lotka-Volterra) for matter-SQ interaction

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
# THEORY DEFINITIONS (Y01-Y30)
# Each E_func signature: E_func(z_array, Omega_m) -> E_array
# ==============================================================================

# ── DIRECTION 1: SQ field Renormalization Group fixed points ──────────────────

# Y01: RG Fixed Point SQ Dark Energy (k=2)
# A1+A4: SQ generation rate flows under cosmic RG toward an IR fixed point.
# Near-fixed-point RG flow: beta_RG(g) = -epsilon * g + g^2 (Wilson-Fisher).
# epsilon = 4 - D where D is effective dimension of annihilation manifold.
# At fixed point g* = epsilon. SQ effective DE density near fixed point:
# rho_DE = OL0 * (1 + epsilon * ln(E_lcdm)) / (1 + epsilon * ln(1)) -- at z=0 E=1.
# Use epsilon = 1/pi (sub-critical dimension from SQ lattice geometry).
# rho_DE = OL0 / (1 + epsilon * ln(E_lcdm)) clamped positive.
# k=2
def Y01_E(z_arr, Om):
    epsilon = 1.0 / math.pi   # fixed: sub-critical dimension
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
    denom   = np.maximum(1.0 + epsilon * np.log(np.maximum(E_lcdm, 1e-15)), 1e-10)
    rho_DE  = OL0 / denom
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Y02: RG Anomalous Dimension SQ DE (k=2)
# A1+A4: At the SQ RG fixed point, anomalous dimension eta_anom modifies
# the scaling of SQ density. eta_anom = 1/6 (Ising universality class in 3D).
# SQ field correlations: <phi(0)phi(r)> ~ r^(-(D-2+eta_anom)).
# Effective: rho_DE = OL0 * (1+z)^(-(2 - eta_anom)) = (1+z)^(-11/6).
# Exponent: 2 - eta_anom = 2 - 1/6 = 11/6 from RG fixed point.
# k=2
def Y02_E(z_arr, Om):
    eta_anom = 1.0 / 6.0   # fixed: Ising universality anomalous dimension
    exponent = 2.0 - eta_anom   # = 11/6
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    rho_DE = OL0 * (1+z_arr)**(-exponent)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Y03: RG Flow Crossover Free Exponent (k=3)
# A1+A4: RG flow has a crossover between UV and IR fixed points.
# Crossover at z_cross ~ sqrt(OL0/Om). Free parameter: crossover sharpness nu_rg.
# rho_DE = OL0 / (1 + (Om*(1+z)^3/OL0)^nu_rg). k=3.
def Y03_E_factory(nu_rg):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0 or nu_rg <= 0:
            return None
        x      = Om * (1+z_arr)**3 / OL0
        denom  = np.maximum(1.0 + x**nu_rg, 1e-10)
        # normalize: at z=0 denom0 = 1 + (Om/OL0)^nu_rg
        denom0 = 1.0 + (Om / OL0)**nu_rg
        rho_DE = OL0 * denom0 / denom
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 2: Bifurcation cascade (period-doubling) in generation rate ─────

# Y04: Period-Doubling Cascade SQ DE (k=2)
# A1+A3: SQ generation rate undergoes period-doubling bifurcation cascade.
# Feigenbaum constant delta_F = 4.6692 (universal). Period-doubling in SQ rate
# creates fractal-like alternations in rho_DE accumulation.
# Lyapunov exponent of map ~ (1/delta_F) * ln(r/r_c).
# rho_DE = OL0 * exp(-A_pd * (1+z)^(1/delta_F)) normalized to OL0 at z=0.
# A_pd = delta_F * (e - 1) from criticality condition. delta_F = 4.6692.
# k=2
def Y04_E(z_arr, Om):
    delta_F = 4.6692016   # Feigenbaum constant (universal, theory-derived)
    A_pd    = delta_F * (math.e - 1.0)
    exponent = 1.0 / delta_F
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    # rho_DE = OL0 * exp(-A_pd * ((1+z)^exponent - 1))
    rho_DE = OL0 * np.exp(-A_pd * ((1+z_arr)**exponent - 1.0))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Y05: Feigenbaum Scaling SQ DE (k=2)
# A1+A3: At the period-doubling accumulation point, scaling self-similar.
# Feigenbaum alpha = 2.5029 (universal, second Feigenbaum constant).
# SQ density at accumulation: rho_DE = OL0 * (1 - (ln(1+z)/ln(1+z_pd))^alpha_F).
# z_pd = delta_F (period-doubling scale in Hubble units). alpha_F = 1/(alpha_Feig).
# alpha_F = 1/2.5029 from universality.
# k=2
def Y05_E(z_arr, Om):
    alpha_Feig = 2.5029078   # 2nd Feigenbaum constant (universal)
    delta_F    = 4.6692016
    z_pd       = delta_F     # period-doubling scale
    alpha_F    = 1.0 / alpha_Feig
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    ln_ratio = np.log1p(z_arr) / math.log1p(z_pd)
    rho_DE   = OL0 * np.maximum(1.0 - ln_ratio**alpha_F, 0.0)
    # Clamp to avoid negative at high z
    rho_DE   = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Y06: Period-Doubling Free Scale (k=3)
# A1+A3: Period-doubling cascade scale z_pd is free.
# rho_DE = OL0 * exp(-A_pd * ((1+z)^(1/delta_F) - 1)) with A_pd free. k=3.
def Y06_E_factory(A_pd):
    delta_F  = 4.6692016
    exponent = 1.0 / delta_F
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or A_pd <= 0:
            return None
        rho_DE = OL0 * np.exp(-A_pd * ((1+z_arr)**exponent - 1.0))
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 3: Heteroclinic orbits connecting annihilation attractors ────────

# Y07: Heteroclinic Orbit SQ Transition DE (k=2)
# A1+A4: SQ phase space has two annihilation attractors connected by heteroclinic
# orbit. Trajectory spends exponentially distributed time near each attractor.
# Transition probability: P_trans ~ exp(-Delta_E / kT_SQ) where Delta_E ~ OL0.
# kT_SQ = Om (matter sector provides thermal bath for SQ).
# Net: rho_DE = OL0 * (exp(-Om/OL0) + (1+z)^3 * (1 - exp(-Om/OL0))) / (1+z)^3
# = OL0 * (exp(-Om/OL0) * (1+z)^(-3) + (1 - exp(-Om/OL0)))
# = OL0 * (1 - (1 - exp(-Om/OL0)) * (1 - (1+z)^(-3)))
# k=2
def Y07_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    p_trans = math.exp(-Om / OL0)   # transition weight
    rho_DE = OL0 * (1.0 - (1.0 - p_trans) * (1.0 - (1+z_arr)**(-3.0)))
    # normalize to OL0 at z=0
    norm0 = 1.0 - (1.0 - p_trans) * 0.0   # = 1 at z=0
    # already 1 at z=0
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Y08: Homoclinic Tangle SQ DE (k=2)
# A1+A4: Transverse homoclinic intersection creates Smale horseshoe chaos.
# Horseshoe structure: rho_DE oscillates with increasing frequency near attractor.
# In Hubble coords: theta_hom = sqrt(OL0/Om) * ln(1+z) (phase accumulated).
# rho_DE = OL0 * (1 - A_hom * sin^2(theta_hom / 2)) where A_hom = 2/pi^2.
# A_hom = 2/pi^2: fraction of phase space covered by horseshoe lobes.
# k=2
def Y08_E(z_arr, Om):
    A_hom = 2.0 / math.pi**2   # fixed: horseshoe lobe fraction
    OL0   = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    omega_hom = math.sqrt(OL0 / Om)
    theta     = omega_hom * np.log1p(z_arr)
    rho_DE    = OL0 * (1.0 - A_hom * np.sin(theta / 2.0)**2)
    rho_DE    = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Y09: Heteroclinic Orbit Free Amplitude (k=3)
# A1+A4: Heteroclinic connection amplitude A_het is free.
# rho_DE = OL0 * (1 - A_het * (1 - (1+z)^(-3))). k=3.
def Y09_E_factory(A_het):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or not (0 < A_het < 1):
            return None
        rho_DE = OL0 * np.maximum(1.0 - A_het * (1.0 - (1+z_arr)**(-3.0)), 1e-10)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 4: Strange attractor in void dynamics (Lorenz-type) ─────────────

# Y10: Lorenz Attractor Void DE (k=2)
# A1+A3+A4: Void expansion follows Lorenz-like attractor.
# Lorenz system: sigma_L=10, rho_L=28, beta_L=8/3 (canonical).
# Attractor fractal dimension D_L = 2.0627 (Kaplan-Yorke).
# DE effective scaling from attractor dimension:
# rho_DE = OL0 * (1 + A_L * ((1+z)^(-(D_L-2)) - 1))
# D_L - 2 = 0.0627. A_L = 1/sigma_L = 0.1.
# At z=0: rho_DE = OL0. At large z: grows ~ (1+z)^0.0627.
# Instead: rho_DE = OL0 * exp(-A_L * (D_L - 2) * ln(1+z)) = OL0*(1+z)^(-A_L*(D_L-2)).
# k=2
def Y10_E(z_arr, Om):
    sigma_L  = 10.0
    D_L      = 2.0627        # Lorenz attractor Kaplan-Yorke dimension
    A_L      = 1.0 / sigma_L # = 0.1
    exponent = A_L * (D_L - 2.0)   # = 0.00627
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    rho_DE = OL0 * (1+z_arr)**(-exponent)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Y11: Lorenz Sensitivity SQ Amplification DE (k=2)
# A1+A3+A4: Lorenz butterfly effect amplifies SQ fluctuations exponentially.
# Maximal Lyapunov exponent lambda_L1 = 0.9056 (canonical Lorenz).
# Amplification: delta_rho ~ exp(lambda_L1 * t_H). In ln(1+z) time:
# rho_DE = OL0 * (1 + A_bfly * exp(-lambda_L1 * ln^2(1+z)))
# A_bfly = 1/e from maximum amplification normalization.
# At z=0: rho_DE = OL0 * (1 + 1/e). Normalize.
# k=2
def Y11_E(z_arr, Om):
    lambda_L1 = 0.9056     # canonical Lorenz maximal Lyapunov exponent
    A_bfly    = 1.0 / math.e
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    rho_DE = OL0 * (1.0 + A_bfly * np.exp(-lambda_L1 * np.log1p(z_arr)**2))
    norm0  = 1.0 + A_bfly   # at z=0: exp(0)=1
    rho_DE = rho_DE / norm0   # normalize so rho_DE(z=0) = OL0
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Y12: Lorenz Dimension Free (k=3)
# A1+A3+A4: Lorenz attractor dimension D_L is free.
# rho_DE = OL0 * (1+z)^(-(D_L-2)/sigma_L). k=3.
def Y12_E_factory(D_L):
    sigma_L = 10.0
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or D_L <= 2.0:
            return None
        exponent = (D_L - 2.0) / sigma_L
        rho_DE = OL0 * (1+z_arr)**(-exponent)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 5: Excitable medium dynamics (FitzHugh-Nagumo type) ─────────────

# Y13: FitzHugh-Nagumo Excitable SQ DE (k=2)
# A1+A2+A4: SQ generation-annihilation system is excitable (FitzHugh-Nagumo).
# Excitable threshold: r_FHN = cubic nullcline maximum = 2/3*sqrt(3).
# Recovery variable tau_FHN = 12.5 (slow recovery in FHN).
# Below threshold (low z): SQ quiescent, rho_DE ~ OL0.
# Above threshold (high z): SQ fires, rapid depletion.
# Effective: rho_DE = OL0 / (1 + exp((x - x_thresh) / w_FHN))
# x = Om*(1+z)^3/OL0, x_thresh = 2/(3*sqrt(3)), w_FHN = 1/tau_FHN = 0.08.
# k=2
def Y13_E(z_arr, Om):
    x_thresh = 2.0 / (3.0 * math.sqrt(3.0))   # FHN cubic threshold
    w_FHN    = 1.0 / 12.5                      # = 0.08 (inverse recovery)
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    x      = Om * (1+z_arr)**3 / OL0
    # Sigmoid suppression above threshold
    rho_DE = OL0 / (1.0 + np.exp((x - x_thresh) / w_FHN))
    # normalize to OL0 at z=0
    x0    = Om / OL0
    norm0 = 1.0 / (1.0 + math.exp((x0 - x_thresh) / w_FHN))
    if norm0 < 1e-10:
        return None
    rho_DE = rho_DE / norm0
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Y14: FHN Recovery Oscillation DE (k=2)
# A1+A2+A4: Recovery variable in FHN model creates oscillatory rho_DE.
# Recovery: V_rec(t) ~ exp(-t/tau_FHN) * cos(omega_FHN * t).
# In Hubble units: tau_FHN = 1/sqrt(3), omega_FHN = pi/2.
# rho_DE = OL0 * (1 + A_rec * exp(-z/tau_FHN) * cos(omega_FHN * z))
# A_rec = 1/(2*sqrt(3)) from FHN amplitude of after-depolarization.
# Normalize so rho_DE(0) = OL0: at z=0, cos(0)=1, exp(0)=1 -> norm = 1 + A_rec.
# k=2
def Y14_E(z_arr, Om):
    tau_FHN   = 1.0 / math.sqrt(3.0)
    omega_FHN = math.pi / 2.0
    A_rec     = 1.0 / (2.0 * math.sqrt(3.0))
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    rho_DE = OL0 * (1.0 + A_rec * np.exp(-z_arr / tau_FHN) * np.cos(omega_FHN * z_arr))
    norm0  = 1.0 + A_rec
    rho_DE = rho_DE / norm0
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Y15: FHN Threshold Free (k=3)
# A1+A2+A4: FHN excitation threshold x_thresh is free.
# rho_DE = OL0 / (1 + exp((Om*(1+z)^3/OL0 - x_thresh)/w_FHN)) / norm. k=3.
def Y15_E_factory(x_thresh):
    w_FHN = 1.0 / 12.5
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0 or x_thresh <= 0:
            return None
        x      = Om * (1+z_arr)**3 / OL0
        rho_DE = OL0 / (1.0 + np.exp((x - x_thresh) / w_FHN))
        x0    = Om / OL0
        norm0 = 1.0 / (1.0 + math.exp((x0 - x_thresh) / w_FHN))
        if norm0 < 1e-10: return None
        rho_DE = rho_DE / norm0
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 6: Wavefront propagation of annihilation boundary ───────────────

# Y16: Annihilation Wavefront KPP DE (k=2)
# A1+A3: SQ annihilation propagates as a KPP-Fisher wavefront.
# KPP wave speed: v_KPP = 2 * sqrt(D_SQ * r_SQ) where D_SQ = diffusion, r_SQ = rate.
# In cosmic units: v_KPP / H0 = 2/pi (from pi-periodicity of SQ lattice).
# Wavefront position: z_front = v_KPP * t_H. Annihilated fraction:
# f_ann = 0.5 * (1 - tanh((z - z_front) / lambda_KPP))
# z_front = 2/pi (dimensionless Hubble crossing). lambda_KPP = 1/pi^2.
# rho_DE = OL0 * (1 - f_ann). Normalize to OL0 at z=0.
# k=2
def Y16_E(z_arr, Om):
    v_KPP   = 2.0 / math.pi      # KPP wave speed (Hubble units)
    lam_KPP = 1.0 / math.pi**2   # wavefront width
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    f_ann  = 0.5 * (1.0 - np.tanh((z_arr - v_KPP) / lam_KPP))
    f_ann0 = 0.5 * (1.0 - math.tanh((0.0 - v_KPP) / lam_KPP))
    # rho_DE = OL0 * (1 - f_ann) normalized
    rho_DE = OL0 * (1.0 - f_ann)
    norm0  = 1.0 - f_ann0
    if abs(norm0) < 1e-10:
        return None
    rho_DE = rho_DE / norm0
    rho_DE = np.maximum(rho_DE, 1e-10)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Y17: Allen-Cahn Wavefront SQ DE (k=2)
# A1+A3: Allen-Cahn equation describes SQ phase interface motion.
# Interface velocity: v_AC = -mu_AC * (kappa * H - F_drive).
# In Hubble units, interface position sweeps as phi_AC(z) = tanh(z/xi_AC).
# xi_AC = sqrt(2) (interface width from Allen-Cahn coefficient ratio = 1).
# rho_DE = OL0 * (1 - phi_AC^2) / (1 - tanh^2(0)) = OL0 * sech^2(z/xi_AC).
# But sech^2(0)=1 so rho_DE(z=0)=OL0 (correct).
# k=2
def Y17_E(z_arr, Om):
    xi_AC = math.sqrt(2.0)   # fixed: Allen-Cahn interface width
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    arg    = z_arr / xi_AC
    cosh_a = np.cosh(np.minimum(arg, 100.0))
    rho_DE = OL0 / cosh_a**2
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Y18: Wavefront Speed Free (k=3)
# A1+A3: KPP wavefront position z_front is free.
# rho_DE from wavefront annihilation fraction, z_front free. k=3.
def Y18_E_factory(z_front):
    lam_KPP = 1.0 / math.pi**2
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or z_front <= 0:
            return None
        f_ann  = 0.5 * (1.0 - np.tanh((z_arr - z_front) / lam_KPP))
        f_ann0 = 0.5 * (1.0 - math.tanh((0.0 - z_front) / lam_KPP))
        rho_DE = OL0 * (1.0 - f_ann)
        norm0  = 1.0 - f_ann0
        if abs(norm0) < 1e-10: return None
        rho_DE = rho_DE / norm0
        rho_DE = np.maximum(rho_DE, 1e-10)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 7: Cellular automaton rules for SQ generation ──────────────────

# Y19: Wolfram Rule 110 SQ DE (k=2)
# A1+A3: SQ generation follows cellular automaton Rule 110 (Turing complete).
# Rule 110 produces complex patterns with period-3 and period-14 structures.
# Effective: rule-average density has period-14 / (full rule cycle).
# In continuous limit: rho_DE = OL0 * (1 - A_ca * (1 - cos(2*pi*z/z_ca)))
# z_ca = 14 / (2*pi) from rule 110 dominant period. A_ca = 1/14 from rule density.
# k=2
def Y19_E(z_arr, Om):
    period_ca = 14.0          # Rule 110 primary period
    z_ca      = period_ca / (2.0 * math.pi)   # ~ 2.228
    A_ca      = 1.0 / period_ca               # = 1/14
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    rho_DE = OL0 * (1.0 - A_ca * (1.0 - np.cos(2.0 * math.pi * z_arr / z_ca)))
    # At z=0: cos(0)=1 -> rho_DE = OL0 (correct)
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Y20: Totalistic CA SQ DE (k=2)
# A1+A3: Outer totalistic CA: SQ generation density ~ fraction of active cells.
# For a 2-state 3-neighbor CA with B=3/8 average born fraction:
# Active fraction evolves: f_active(t) = 1 - (1 - f0) * (1 - B)^(N_steps).
# N_steps ~ ln(1+z) (logarithmic time). B = 3/8.
# Equilibrium active fraction f_eq = B/(1-B+B) = B = 3/8.
# rho_DE = OL0 * (f_eq + (1 - f_eq) * exp(-B * ln^2(1+z)))
# = OL0 * (3/8 + 5/8 * exp(-3/8 * ln^2(1+z))). k=2.
def Y20_E(z_arr, Om):
    B_ca  = 3.0 / 8.0   # fixed: CA born fraction (average totalistic rule)
    f_eq  = B_ca
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    ln_z   = np.log1p(z_arr)
    rho_DE = OL0 * (f_eq + (1.0 - f_eq) * np.exp(-B_ca * ln_z**2))
    # At z=0: rho_DE = OL0 * (f_eq + (1-f_eq)) = OL0 (correct)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Y21: CA Period Free (k=3)
# A1+A3: CA oscillation period z_ca is free.
# rho_DE = OL0 * (1 - A_ca*(1 - cos(2*pi*z/z_ca))). k=3.
def Y21_E_factory(z_ca):
    A_ca = 1.0 / 14.0
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or z_ca <= 0:
            return None
        rho_DE = OL0 * (1.0 - A_ca * (1.0 - np.cos(2.0 * math.pi * z_arr / z_ca)))
        rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 8: Graph-theoretic connectivity of void networks ────────────────

# Y22: Void Network Percolation SQ DE (k=2)
# A1+A3+A4: Void network undergoes percolation transition.
# Percolation threshold p_c = 0.3116 (site percolation on 3D cubic lattice).
# Below p_c: isolated voids. Above p_c: connected void network forms.
# Connected fraction: P_inf = (p - p_c)^beta_perc for p > p_c, beta_perc = 0.418.
# p ~ (1+z)^(-3) * (1/Om) (void filling fraction dilutes with expansion).
# At z=0: p = 1/Om, typically >> p_c.
# rho_DE = OL0 * P_inf^(1/3) (DE channeled through connected voids).
# P_inf = max(0, (p - p_c))^beta_perc, p = (1+z)^(-3)/(1+1/Om).
# k=2
def Y22_E(z_arr, Om):
    p_c       = 0.3116   # 3D site percolation threshold (universal)
    beta_perc = 0.418    # percolation order parameter exponent
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    # void fraction: scales inversely with matter ~ (1+z)^(-3) at each z
    p_void = OL0 / (OL0 + Om * (1+z_arr)**3)   # fraction in void at redshift z
    # percolation order parameter
    P_inf  = np.maximum(p_void - p_c, 0.0)**beta_perc
    # normalize: at z=0
    p0    = OL0 / (OL0 + Om)
    P_inf0 = max(p0 - p_c, 0.0)**beta_perc
    if P_inf0 < 1e-10:
        return None
    rho_DE = OL0 * (P_inf / P_inf0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Y23: Void Network Small-World SQ DE (k=2)
# A1+A3: Void network has small-world topology (Watts-Strogatz).
# Clustering coefficient C_SW = C0 * (1 - p_rew)^3 where p_rew = rewiring prob.
# In cosmic void network: p_rew ~ (1+z)^(-2) (fewer long-range connections at high z).
# C0 = 3*(k_graph-2)/(4*(k_graph-1)) ~ 0.5 (for k_graph=4 neighbors).
# Effective: C_SW modulates SQ annihilation efficiency.
# rho_DE = OL0 * (1 - C_SW * f_0) where f_0 = 1 - exp(-C0).
# k=2
def Y23_E(z_arr, Om):
    k_graph = 4.0
    C0      = 3.0 * (k_graph - 2.0) / (4.0 * (k_graph - 1.0))   # = 0.5
    f0      = 1.0 - math.exp(-C0)
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    p_rew  = (1+z_arr)**(-2.0)   # rewiring probability at redshift z
    C_SW   = C0 * (1.0 - p_rew)**3
    # At z=0: p_rew=1, C_SW=0 -> rho_DE = OL0 (correct)
    rho_DE = OL0 * (1.0 - C_SW * f0)
    rho_DE = np.maximum(rho_DE, 1e-10)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Y24: Percolation Threshold Free (k=3)
# A1+A3+A4: Percolation threshold p_c is free.
# rho_DE from percolation order parameter with free p_c. k=3.
def Y24_E_factory(p_c):
    beta_perc = 0.418
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0 or not (0.0 < p_c < 1.0):
            return None
        p_void = OL0 / (OL0 + Om * (1+z_arr)**3)
        P_inf  = np.maximum(p_void - p_c, 0.0)**beta_perc
        p0     = OL0 / (OL0 + Om)
        P_inf0 = max(p0 - p_c, 0.0)**beta_perc
        if P_inf0 < 1e-10: return None
        rho_DE = OL0 * (P_inf / P_inf0)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 9: Epidemic spreading model for annihilation events ─────────────

# Y25: SIR Epidemic SQ Annihilation DE (k=2)
# A1+A3: SQ annihilation events spread epidemically (SIR model).
# S=susceptible SQ, I=annihilating SQ, R=annihilated.
# Basic reproduction number R0_ep = beta_ep/gamma_ep.
# Epidemic peak at I_max = S0 - (1 + ln(R0_ep))/R0_ep.
# SQMH: R0_ep = e (Napier's number, from entropy maximization of spreading).
# gamma_ep = 1 (unit rate in Hubble time). beta_ep = e.
# Final size epidemic: 1 - exp(-R0_ep * R_inf) = R_inf -> R_inf ~ 0.9397 for R0_ep=e.
# rho_DE = OL0 * (1 - R_inf * S(z)) where S(z) ~ exp(-beta_ep * (1-exp(-z))).
# Approximate: rho_DE = OL0 * exp(-R0_ep * (1 - (1+z)^(-1))).
# At z=0: exp(0) = 1 -> rho_DE = OL0. k=2.
def Y25_E(z_arr, Om):
    R0_ep = math.e   # fixed: epidemic R0 from entropy maximization
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    rho_DE = OL0 * np.exp(-R0_ep * (1.0 - (1+z_arr)**(-1.0)))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Y26: SEIR Epidemic with Latency SQ DE (k=2)
# A1+A3: SEIR model adds exposed (E) latency period tau_E.
# Latency: tau_E = 1/sigma_ep. SQMH: sigma_ep = 1/pi (SQ uncertainty latency).
# In SEIR, effective R0_eff = R0 * sigma / (sigma + gamma) ~ R0_ep * pi/(pi+1).
# Effective DE depletion: rho_DE = OL0 * exp(-R0_eff * (1 - (1+z)^(-sigma_ep))).
# R0_eff = e * pi / (pi + 1), sigma_ep = 1/pi. k=2.
def Y26_E(z_arr, Om):
    R0_ep     = math.e
    sigma_ep  = 1.0 / math.pi   # fixed: latency rate
    R0_eff    = R0_ep * math.pi / (math.pi + 1.0)
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    rho_DE = OL0 * np.exp(-R0_eff * (1.0 - (1+z_arr)**(-sigma_ep)))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Y27: Epidemic R0 Free (k=3)
# A1+A3: Epidemic reproduction number R0_ep is free.
# rho_DE = OL0 * exp(-R0_ep * (1 - (1+z)^(-1))). k=3.
def Y27_E_factory(R0_ep):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or R0_ep <= 0:
            return None
        rho_DE = OL0 * np.exp(-R0_ep * (1.0 - (1+z_arr)**(-1.0)))
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── DIRECTION 10: Predator-prey dynamics (Lotka-Volterra) for matter-SQ ───────

# Y28: Lotka-Volterra Matter-SQ DE (k=2)
# A1+A3+C2: Matter (predator) depletes SQ (prey). Lotka-Volterra equilibrium:
# prey* = delta_LV / gamma_LV, pred* = alpha_LV / beta_LV.
# SQ steady-state rho_SQ* = delta/gamma. From SQMH: alpha_LV = H^2, beta_LV = Om*H^2,
# gamma_LV = OL0, delta_LV = Om.
# prey* = Om/OL0 (SQ equilibrium). Period of oscillation:
# T_LV = 2*pi / sqrt(alpha*delta) = 2*pi / (H * sqrt(Om)).
# rho_DE = OL0 * (1 + A_LV * cos(2*pi * ln(1+z) / T_eff))
# T_eff = 2*pi / sqrt(OL0 * Om) in Hubble units. A_LV = Om / OL0 (amplitude from LV).
# Normalize so rho_DE(z=0) = OL0. k=2.
def Y28_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None
    A_LV  = Om / OL0   # Lotka-Volterra amplitude
    T_eff = 2.0 * math.pi / math.sqrt(OL0 * Om)   # LV period in Hubble units
    rho_DE = OL0 * (1.0 + A_LV * np.cos(2.0 * math.pi * np.log1p(z_arr) / T_eff))
    # normalize: at z=0, cos(0)=1 -> rho_DE = OL0*(1+A_LV). Fix:
    norm0  = 1.0 + A_LV
    rho_DE = rho_DE / norm0
    rho_DE = np.maximum(rho_DE, 1e-10)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Y29: Lotka-Volterra Damped Oscillation DE (k=2)
# A1+A3+C2: LV system with dissipation (friction in SQ fluid).
# Damped oscillation: rho_DE = OL0 * exp(-zeta_LV * z) * cos(omega_LV * z) + OL0_inf.
# zeta_LV = 1/(2*pi) (critical damping ratio from SQ viscosity). omega_LV = pi.
# OL0_inf = OL0 / (1 + 1/(2*pi^2)) (long-time equilibrium).
# Normalize so rho_DE(z=0) = OL0. k=2.
def Y29_E(z_arr, Om):
    zeta_LV  = 1.0 / (2.0 * math.pi)   # damping ratio
    omega_LV = math.pi                   # oscillation frequency
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    OL0_inf = OL0 / (1.0 + 1.0 / (2.0 * math.pi**2))   # equilibrium
    A_damp  = OL0 - OL0_inf   # amplitude
    rho_DE = OL0_inf + A_damp * np.exp(-zeta_LV * z_arr) * np.cos(omega_LV * z_arr)
    rho_DE = np.maximum(rho_DE, 1e-10)
    # At z=0: rho_DE = OL0_inf + A_damp * 1 * 1 = OL0 (correct by construction)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# Y30: Lotka-Volterra Damping Free (k=3)
# A1+A3+C2: LV damping rate zeta_LV is free.
# rho_DE = OL0_inf + A_damp * exp(-zeta_LV*z) * cos(omega_LV*z). k=3.
def Y30_E_factory(zeta_LV):
    omega_LV = math.pi
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or zeta_LV < 0:
            return None
        OL0_inf = OL0 / (1.0 + 1.0 / (2.0 * math.pi**2))
        A_damp  = OL0 - OL0_inf
        rho_DE  = OL0_inf + A_damp * np.exp(-zeta_LV * z_arr) * np.cos(omega_LV * z_arr)
        rho_DE  = np.maximum(rho_DE, 1e-10)
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
        # Direction 1: RG Fixed Points
        ('Y01', 'RG Fixed Point SQ DE',                   2, Y01_E,  None),
        ('Y02', 'RG Anomalous Dimension SQ DE',            2, Y02_E,  None),
        ('Y03', 'RG Flow Crossover Free Exponent',         3, Y03_E_factory,
            [[0.1], [0.3], [0.5], [1.0], [2.0], [3.0]]),
        # Direction 2: Period-Doubling Cascade
        ('Y04', 'Period-Doubling Feigenbaum SQ DE',        2, Y04_E,  None),
        ('Y05', 'Feigenbaum Scaling SQ DE',                2, Y05_E,  None),
        ('Y06', 'Period-Doubling Free Scale',              3, Y06_E_factory,
            [[0.1], [0.5], [1.0], [2.0], [5.0], [10.0]]),
        # Direction 3: Heteroclinic Orbits
        ('Y07', 'Heteroclinic Orbit SQ Transition DE',     2, Y07_E,  None),
        ('Y08', 'Homoclinic Tangle SQ DE',                 2, Y08_E,  None),
        ('Y09', 'Heteroclinic Orbit Free Amplitude',       3, Y09_E_factory,
            [[0.1], [0.3], [0.5], [0.7], [0.9], [0.2]]),
        # Direction 4: Strange Attractor / Lorenz
        ('Y10', 'Lorenz Attractor Void DE',                2, Y10_E,  None),
        ('Y11', 'Lorenz Butterfly SQ Amplification DE',    2, Y11_E,  None),
        ('Y12', 'Lorenz Dimension Free',                   3, Y12_E_factory,
            [[2.1], [2.3], [2.5], [2.7], [3.0], [4.0]]),
        # Direction 5: FitzHugh-Nagumo Excitable
        ('Y13', 'FitzHugh-Nagumo Excitable SQ DE',        2, Y13_E,  None),
        ('Y14', 'FHN Recovery Oscillation DE',             2, Y14_E,  None),
        ('Y15', 'FHN Threshold Free',                      3, Y15_E_factory,
            [[0.1], [0.3], [0.5], [2.0/(3*math.sqrt(3))], [1.0], [2.0]]),
        # Direction 6: Wavefront Propagation
        ('Y16', 'Annihilation Wavefront KPP DE',           2, Y16_E,  None),
        ('Y17', 'Allen-Cahn Wavefront SQ DE',              2, Y17_E,  None),
        ('Y18', 'Wavefront Speed Free',                    3, Y18_E_factory,
            [[0.3], [0.5], [2.0/math.pi], [1.0], [2.0], [3.0]]),
        # Direction 7: Cellular Automaton
        ('Y19', 'Wolfram Rule 110 SQ DE',                  2, Y19_E,  None),
        ('Y20', 'Totalistic CA SQ DE',                     2, Y20_E,  None),
        ('Y21', 'CA Period Free',                          3, Y21_E_factory,
            [[0.5], [1.0], [2.0], [3.0], [5.0], [14.0/(2*math.pi)]]),
        # Direction 8: Graph-Theoretic Void Networks
        ('Y22', 'Void Network Percolation SQ DE',          2, Y22_E,  None),
        ('Y23', 'Void Network Small-World SQ DE',          2, Y23_E,  None),
        ('Y24', 'Percolation Threshold Free',              3, Y24_E_factory,
            [[0.1], [0.2], [0.3116], [0.4], [0.5], [0.6]]),
        # Direction 9: Epidemic Spreading
        ('Y25', 'SIR Epidemic SQ Annihilation DE',         2, Y25_E,  None),
        ('Y26', 'SEIR Epidemic Latency SQ DE',             2, Y26_E,  None),
        ('Y27', 'Epidemic R0 Free',                        3, Y27_E_factory,
            [[0.5], [1.0], [math.e], [3.0], [5.0], [10.0]]),
        # Direction 10: Lotka-Volterra Predator-Prey
        ('Y28', 'Lotka-Volterra Matter-SQ DE',             2, Y28_E,  None),
        ('Y29', 'Lotka-Volterra Damped Oscillation DE',    2, Y29_E,  None),
        ('Y30', 'Lotka-Volterra Damping Free',             3, Y30_E_factory,
            [[0.0], [0.05], [1.0/(2*math.pi)], [0.2], [0.5], [1.0]]),
    ]
    return theories


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    out_dir   = _SCRIPT_DIR
    json_path = os.path.join(out_dir, 'l30_results4.json')

    theories  = build_theory_list()
    task_args = []
    for wid, name, k, E_func_or_factory, extra_starts in theories:
        task_args.append((wid, name, k, E_func_or_factory, extra_starts))

    print('=' * 65)
    print('L30 4th Run SQMH Theory Test (Y01-Y30)')
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
