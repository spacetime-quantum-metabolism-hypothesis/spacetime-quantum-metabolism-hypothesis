# -*- coding: utf-8 -*-
"""
l30_test2.py -- L30 2nd Run SQMH Fresh Theories (W01-W30)
==========================================================
30 new theories derived from SQMH axioms A1-A4 + C1-C3.
COMPLETELY different mechanisms from V-series.

Explored NEW directions:
- Spacetime quantum mean free path effects
- Percolation threshold of annihilation network
- Critical slowing down near generation-annihilation balance
- Quantum walk dynamics of spacetime quanta
- Self-organized criticality in annihilation events
- Renormalization group flow of annihilation rate
- Fractal dimension of void boundaries
- Levy flight statistics of quantum generation events
- Network topology of spacetime quantum connectivity
- Ising-like phase transition in quantum vacuum

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
OR      = 5.38e-5   # radiation density
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
# THEORY DEFINITIONS (W01-W30)
# Each theory returns (name, k, E_func_or_wrapper, extra_starts_for_k3+)
# E_func signature: E_func(z_array, Omega_m) -> E_array
# ==============================================================================


# ── W01: Mean Free Path Modulated Dark Energy ─────────────────────────────────
# A1+A3: SQ quanta travel mean free path lambda_mfp before annihilation.
# lambda_mfp ~ 1/(n_m * sigma_SQ). As n_m = Om*(1+z)^3*rho_crit, lambda_mfp ~ 1/(1+z)^3.
# Dark energy density modulated by fraction of SQ that escape annihilation.
# Escape fraction: f_esc = exp(-1/lambda_mfp_normalized) = exp(-(1+z)^3 * alpha_mfp).
# alpha_mfp = ln(2)/3 from half-depletion at z_eq (matter-Lambda equality).
# k=2 (Om, H0 free; alpha_mfp theory-fixed)
def W01_E(z_arr, Om):
    OL0       = 1.0 - Om - OR
    alpha_mfp = math.log(2.0) / 3.0   # fixed: half-depletion at z_eq
    f_esc     = np.exp(-alpha_mfp * ((1+z_arr)**3 - 1.0))
    rho_DE    = OL0 * f_esc
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# ── W02: Percolation Threshold Dark Energy ────────────────────────────────────
# A1+A4: Annihilation network has percolation threshold p_c.
# Below p_c: SQ form disconnected clusters -> DE acts as cosmological constant.
# Above p_c: SQ network percolates -> annihilation becomes global.
# p ~ Om*(1+z)^3 / (Om*(1+z)^3 + OL0). Percolation order parameter:
# phi_perc = max(0, 1 - p_c/p)^beta_perc where p_c = 1/2 (Bethe lattice), beta_perc = 1.
# DE density: rho_DE = OL0 * (1 - phi_perc).
# k=2
def W02_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    p_c = 0.5   # Bethe lattice percolation threshold
    beta_perc = 1.0
    # occupation probability for annihilation network
    num = Om * (1+z_arr)**3
    den = num + OL0
    p   = num / np.maximum(den, 1e-15)
    phi_perc = np.maximum(0.0, 1.0 - p_c / np.maximum(p, 1e-10))**beta_perc
    phi_perc = np.minimum(phi_perc, 1.0)
    rho_DE   = OL0 * (1.0 - phi_perc)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# ── W03: Critical Slowing Down (Generation-Annihilation Balance) ──────────────
# A4: Near the balance point (generation rate ~ annihilation rate), critical slowing
# down occurs (like a critical point). Relaxation time tau_rel ~ |r - r_c|^(-nu_crit).
# As cosmic evolution passes through balance, DE relaxes slowly.
# In FRW: rho_DE = OL0 * (1 + delta_CSD * tanh((z - z_bal)/sigma_bal))
# z_bal ~ 0.4 (matter-DE equality), sigma_bal = 1/sqrt(2*pi) (critical width).
# delta_CSD = 1/(2*pi) from fluctuation-dissipation theorem.
# k=2
def W03_E(z_arr, Om):
    OL0       = 1.0 - Om - OR
    delta_CSD = 1.0 / (2.0 * math.pi)
    sigma_bal = 1.0 / math.sqrt(2.0 * math.pi)
    # z_bal where Om*(1+z)^3 ~ OL0: (OL0/Om)^(1/3) - 1
    if Om <= 0 or OL0 <= 0:
        return None
    z_bal = (OL0 / Om)**(1.0/3.0) - 1.0
    z_bal = max(0.1, z_bal)
    rho_DE = OL0 * (1.0 + delta_CSD * np.tanh((z_arr - z_bal) / sigma_bal))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# ── W04: Quantum Walk Dark Energy ─────────────────────────────────────────────
# A1+A3: SQ quanta undergo quantum walk on spacetime lattice.
# Quantum walk spreads faster than classical (sigma ~ t vs sigma ~ sqrt(t)).
# This modifies SQ density profile. In cosmic time:
# n_SQ(t) ~ n_SQ0 / (H * t)^d_qw where d_qw = 1 (1D quantum walk exponent).
# n_SQ(t) / n_SQ0 = (H0/H)^1 = 1/E.
# rho_DE = OL0 / E_lcdm (normalized so rho_DE(0) = OL0 since E_lcdm(0)=1).
# k=2
def W04_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
    rho_DE  = OL0 / E_lcdm   # quantum walk: n_SQ ~ 1/E
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))


# ── W05: Self-Organized Criticality (Avalanche Size Distribution) ─────────────
# A1+A4: Annihilation events form avalanches following power-law distribution
# (SOC): P(s) ~ s^(-tau_SOC) with tau_SOC = 3/2 (mean-field SOC exponent).
# Average annihilation depletion: <s> ~ (1 - p/p_c)^(-gamma_soc).
# In Hubble units: depletion ~ (1 + z)^(3/2) from SOC scaling.
# rho_DE = OL0 * (1 + z)^(-3/2) * C_soc where C_soc normalizes to OL0 at z=0.
# k=2
def W05_E(z_arr, Om):
    tau_SOC = 3.0/2.0   # mean-field SOC exponent (fixed)
    OL0     = 1.0 - Om - OR
    rho_DE  = OL0 * (1+z_arr)**(-tau_SOC)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))


# ── W06: Renormalization Group Flow of Annihilation Rate ─────────────────────
# A1+A3: Annihilation coupling runs with energy scale mu ~ H.
# RG equation: d lambda/d ln mu = beta_RG * lambda^2.
# Solution: lambda(H) = lambda_0 / (1 - beta_RG * lambda_0 * ln(H/H0)).
# Effective DE density modified by running coupling:
# rho_DE = OL0 / (1 + nu_RG * ln E)^2 where nu_RG = 1/pi (one-loop SQ RG).
# k=2
def W06_E(z_arr, Om):
    nu_RG = 1.0 / math.pi   # fixed: one-loop SQ RG coefficient
    OL0   = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
    ln_E    = np.log(np.maximum(E_lcdm, 1e-10))
    denom   = (1.0 + nu_RG * ln_E)**2
    denom   = np.maximum(denom, 1e-10)
    rho_DE  = OL0 / denom
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))


# ── W07: Fractal Void Boundary Dark Energy ────────────────────────────────────
# A3: generation uniform in voids. Void boundaries are fractal with dimension D_f.
# D_f = 2 + 1/3 ~ 2.33 from cosmic void simulations (fractal void surfaces).
# Volume accessible for SQ generation scales as V_gen ~ L^D_f * L^(3-D_f).
# Effective rho_DE = OL0 * (L_void / L_Hubble)^(3 - D_f) = OL0 * (H/H0)^(3-D_f).
# (3 - D_f) = 3 - 7/3 = 2/3. rho_DE = OL0 * E^(2/3) at LCDM proxy.
# Fixed exponent from fractal dimension D_f = 7/3.
# k=2
def W07_E(z_arr, Om):
    D_f    = 7.0/3.0   # fractal dimension of void boundaries
    alpha  = 3.0 - D_f  # = 2/3
    OL0    = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
    rho_DE  = OL0 * E_lcdm**alpha   # normalized: E_lcdm(0)=1, rho_DE(0)=OL0
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))


# ── W08: Levy Flight Generation Statistics ────────────────────────────────────
# A3: Generation events have heavy-tail spatial distribution (Levy flight).
# Levy exponent alpha_L = 3/2 (stable distribution, minimal assumptions).
# SQ generated in Levy-stable bursts: effective generation rate enhanced.
# Enhancement ~ (1+z)^(-(3 - alpha_L)) = (1+z)^(-3/2) from Levy tail scaling.
# rho_DE = OL0 * (1 - f_levy * (1 - (1+z)^(-1/2)))
# f_levy = 1 - 1/sqrt(e) from equipartition in Levy ensemble.
# k=2
def W08_E(z_arr, Om):
    f_levy = 1.0 - 1.0/math.sqrt(math.e)   # fixed: Levy equipartition
    OL0    = 1.0 - Om - OR
    rho_DE = OL0 * (1.0 - f_levy * (1.0 - (1+z_arr)**(-0.5)))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# ── W09: SQ Network Topology (Small-World Connectivity) ──────────────────────
# A1+A3: SQ quanta form a network. Small-world network: characteristic path length
# L_net ~ ln(N_SQ) where N_SQ ~ rho_DE * V. Annihilation rate ~ L_net^(-1).
# Effective: annihilation efficiency ~ 1/ln(1/OL0_frac).
# rho_DE = OL0 * exp(-sigma_net * ln^2(1+z))
# sigma_net = 1/(2*ln(2)) from network diameter doubling at matter-domination.
# k=2
def W09_E(z_arr, Om):
    sigma_net = 1.0 / (2.0 * math.log(2.0))   # fixed: network topology
    OL0       = 1.0 - Om - OR
    rho_DE    = OL0 * np.exp(-sigma_net * np.log1p(z_arr)**2)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# ── W10: Ising-Like Phase Transition in Quantum Vacuum ───────────────────────
# A2+A4: SQ vacuum has two-state Ising-like model (generation vs annihilation regime).
# Near critical temperature T_c ~ H0/k_B: magnetization m ~ (T_c - T)^beta_Ising.
# T ~ H (Hubble as cosmic temperature). Below T_c: ordered phase (DE dominated).
# m(z) = (1 - E(z))^beta_Ising for E < 1 (only at z=0 region).
# rho_DE = OL0 * (1 + gamma_I * m) where gamma_I = 1/(2*pi).
# At z=0: E=1, m=0, rho_DE=OL0 (correct normalization).
# At high z: E > 1, ordered phase vanishes: rho_DE = OL0 / E^beta_Ising.
# beta_Ising = 1/8 (2D Ising exact) or 1/2 (mean field).
# Use beta_Ising = 1/2 (mean-field SQ vacuum).
# k=2
def W10_E(z_arr, Om):
    beta_I = 0.5   # mean-field Ising exponent
    OL0    = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
    # ordered phase (z>0): rho_DE decays as E^(-beta_I)
    rho_DE  = OL0 / (E_lcdm**beta_I)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))


# ── W11: SQ Percolation with Free Threshold (k=3) ────────────────────────────
# A1+A4: Percolation threshold p_c is not fixed but depends on network coordination.
# p_c is a free parameter (coordination number uncertainty).
# rho_DE = OL0 * max(0, 1 - (Om*(1+z)^3 / OL0) / p_c)^beta_p
# beta_p = 5/36 (2D percolation) fixed; p_c free. k=3.
def W11_E_factory(p_c):
    beta_p = 5.0/36.0   # 2D percolation order parameter exponent
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or p_c <= 0:
            return None
        ratio  = Om * (1+z_arr)**3 / (OL0 * p_c)
        phi    = np.maximum(0.0, 1.0 - ratio)**beta_p
        rho_DE = OL0 * phi
        # normalize: at z=0 ratio~0 so phi~1, rho_DE~OL0 (correct)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── W12: Mean Free Path with Free Opacity (k=3) ──────────────────────────────
# A1+A3: SQ opacity kappa (cross-section per unit density) is a free parameter.
# Escape fraction f_esc = exp(-kappa * Om * (1+z)^3).
# rho_DE = OL0 * f_esc / f_esc_0 where f_esc_0 = exp(-kappa * Om) (at z=0 normalization).
# k=3: Om, H0, kappa free.
def W12_E_factory(kappa):
    def E_func(z_arr, Om):
        OL0    = 1.0 - Om - OR
        f_esc  = np.exp(-kappa * Om * ((1+z_arr)**3 - 1.0))
        rho_DE = OL0 * f_esc
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── W13: RG Flow with Free Anomalous Dimension (k=3) ─────────────────────────
# A1+A3: Annihilation coupling runs with anomalous dimension eta_anom (free).
# rho_DE = OL0 / (1 + eta_anom * ln E)^2.
# Same structure as W06 but eta_anom is free. k=3.
def W13_E_factory(eta_anom):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0: return None
        E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
        E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
        ln_E    = np.log(np.maximum(E_lcdm, 1e-10))
        denom   = (1.0 + eta_anom * ln_E)**2
        denom   = np.maximum(denom, 1e-10)
        rho_DE  = OL0 / denom
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── W14: Quantum Walk with Free Dimension (k=3) ──────────────────────────────
# A1+A3: Quantum walk dimension d_qw is free (between 1 and 3).
# rho_DE = OL0 / E^d_qw (normalized to OL0 at z=0).
# d_qw free. k=3.
def W14_E_factory(d_qw):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0: return None
        E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
        E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
        rho_DE  = OL0 / (E_lcdm**d_qw)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── W15: SQ Network with Free Clustering Coefficient (k=3) ───────────────────
# A1+A3: Network clustering coefficient C_clust controls annihilation efficiency.
# rho_DE = OL0 * exp(-C_clust * ln^2(1+z)).
# C_clust free. k=3.
def W15_E_factory(C_clust):
    def E_func(z_arr, Om):
        OL0    = 1.0 - Om - OR
        rho_DE = OL0 * np.exp(-C_clust * np.log1p(z_arr)**2)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── W16: Diffusion-Limited Aggregation Dark Energy ────────────────────────────
# A1+A3: DLA fractal growth of annihilation clusters.
# DLA fractal dimension D_DLA = 1.71 (2D) or 2.5 (3D).
# Use D_DLA = 5/2 (3D). Effective SQ density ~ r^(D_DLA - 3) ~ r^(-1/2).
# In Hubble units: r ~ c/H, so n_SQ ~ (H/H0)^(1/2) = E^(1/2).
# rho_DE = OL0 * E_lcdm^(D_DLA - 3) = OL0 * E_lcdm^(-1/2).
# k=2
def W16_E(z_arr, Om):
    D_DLA = 2.5   # 3D DLA fractal dimension
    exp   = D_DLA - 3.0   # = -0.5
    OL0   = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
    rho_DE  = OL0 * E_lcdm**exp   # E^(-1/2), normalized at z=0 since E(0)=1
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))


# ── W17: Spin-Glass SQ Vacuum ─────────────────────────────────────────────────
# A2+A4: SQ quanta form spin-glass below T_sg (spin-glass temperature).
# Below T_sg: free energy landscape freezes -> DE "frozen" near constant value.
# Order parameter q_EA (Edwards-Anderson) = OL0 * f_sg.
# f_sg = 1 - (H/H0)^2 = 1 - E^2 for H < H0, else 0.
# At z=0: H=H0, q_EA=0 (marginal). At z>0: H>H0, no spin-glass (disordered).
# rho_DE = OL0 / (1 + (E^2 - 1) / tau_sg) where tau_sg = pi (SQ decoherence time).
# k=2
def W17_E(z_arr, Om):
    tau_sg = math.pi   # fixed: SQ decoherence time
    OL0    = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
    denom   = 1.0 + (E_lcdm**2 - 1.0) / tau_sg
    denom   = np.maximum(denom, 1e-10)
    rho_DE  = OL0 / denom
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))


# ── W18: Topological Defect-Mediated Annihilation ─────────────────────────────
# A1+A4: Annihilation concentrated at topological defects (domain walls, strings).
# String network: defect density rho_string ~ mu_s * (1+z)^2 / t^2 ~ mu_s * H^2 * (1+z)^(-2).
# Extra annihilation channel: d rho_DE / dt += -Gamma_def * rho_string * rho_DE.
# Net: rho_DE = OL0 * (1+z)^(-alpha_def) where alpha_def from defect scaling.
# alpha_def = 2/(3*pi) from string network power-law decay.
# k=2
def W18_E(z_arr, Om):
    alpha_def = 2.0 / (3.0 * math.pi)   # fixed: topological defect exponent
    OL0       = 1.0 - Om - OR
    rho_DE    = OL0 * (1+z_arr)**(-alpha_def)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))


# ── W19: Reaction-Diffusion with Turing Instability ──────────────────────────
# A1+A3: SQ generation-annihilation can develop Turing instability (pattern formation).
# At cosmic scale: Turing modes suppressed by Hubble horizon. Net homogeneous mode:
# rho_DE(z) = OL0 * (1 + A_T * (sin(omega_T * z) / (1 + z)))
# omega_T = sqrt(k_T^2 - mu_T^2) / H0. For critical mode (k_T = mu_T): damped sine.
# Amplitude A_T = 1/(4*pi) (Turing threshold coefficient).
# omega_T = pi/2 from Turing critical wavenumber condition.
# k=2
def W19_E(z_arr, Om):
    A_T     = 1.0 / (4.0 * math.pi)   # Turing amplitude (fixed)
    omega_T = math.pi / 2.0           # critical Turing frequency (fixed)
    OL0     = 1.0 - Om - OR
    rho_DE  = OL0 * (1.0 + A_T * np.sin(omega_T * z_arr) / (1.0 + z_arr))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0):
        return None
    return np.sqrt(np.maximum(E2, 1e-30))


# ── W20: SQ Density Depletion by Gravitational Waves ─────────────────────────
# A1+C2: Gravitational waves carry momentum (C2). GW background generated by structure
# formation can resonantly deplete SQ quanta. GW energy density:
# Omega_GW ~ Omega_m^2 * (H/H0)^2. Resonant depletion rate ~ Omega_GW.
# rho_DE = OL0 * exp(-delta_GW * Om^2 * (E^2 - 1)) where delta_GW = 1/(2*pi^2).
# k=2
def W20_E(z_arr, Om):
    delta_GW = 1.0 / (2.0 * math.pi**2)   # fixed: GW resonance coupling
    OL0      = 1.0 - Om - OR
    if OL0 <= 0:
        return None
    E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
    rho_DE  = OL0 * np.exp(-delta_GW * Om**2 * (E_lcdm**2 - 1.0))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))


# ── W21: Levy Exponent Free Parameter (k=3) ───────────────────────────────────
# A3: Levy flight exponent alpha_L is free.
# rho_DE = OL0 * (1 - f_levy * (1 - (1+z)^(-alpha_L/2))).
# f_levy = 1 - 1/sqrt(e) (fixed); alpha_L free. k=3.
def W21_E_factory(alpha_L):
    f_levy = 1.0 - 1.0/math.sqrt(math.e)
    def E_func(z_arr, Om):
        OL0    = 1.0 - Om - OR
        rho_DE = OL0 * (1.0 - f_levy * (1.0 - (1+z_arr)**(-alpha_L/2.0)))
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── W22: DLA Fractal with Free Dimension (k=3) ────────────────────────────────
# A1+A3: DLA fractal dimension D_DLA is free in [2, 3].
# rho_DE = OL0 * E_lcdm^(D_DLA - 3). k=3.
def W22_E_factory(D_DLA):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0: return None
        exp = D_DLA - 3.0
        E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
        E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
        rho_DE  = OL0 * E_lcdm**exp
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── W23: Topological Defect with Free Exponent (k=3) ─────────────────────────
# A1+A4: Topological defect annihilation exponent alpha_def is free.
# rho_DE = OL0 * (1+z)^(-alpha_def). k=3.
def W23_E_factory(alpha_def):
    def E_func(z_arr, Om):
        OL0    = 1.0 - Om - OR
        rho_DE = OL0 * (1+z_arr)**(-alpha_def)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── W24: Ising Coupling with Free Beta (k=3) ─────────────────────────────────
# A2+A4: Ising order parameter exponent beta_I is free.
# rho_DE = OL0 / E^beta_I. k=3.
def W24_E_factory(beta_I):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0: return None
        E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
        E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
        rho_DE  = OL0 / (E_lcdm**beta_I)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── W25: Spin-Glass Decoherence with Free Tau (k=3) ──────────────────────────
# A2+A4: SQ decoherence time tau_sg is free.
# rho_DE = OL0 / (1 + (E^2 - 1) / tau_sg). k=3.
def W25_E_factory(tau_sg):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or tau_sg <= 0: return None
        E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
        E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
        denom   = 1.0 + (E_lcdm**2 - 1.0) / tau_sg
        denom   = np.maximum(denom, 1e-10)
        rho_DE  = OL0 / denom
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── W26: Turing-Hubble Resonance with Free Frequency (k=3) ───────────────────
# A1+A3: Turing frequency omega_T is free.
# rho_DE = OL0 * (1 + A_T * sin(omega_T * z) / (1+z)). A_T = 1/(4*pi) fixed. k=3.
def W26_E_factory(omega_T):
    A_T = 1.0 / (4.0 * math.pi)
    def E_func(z_arr, Om):
        OL0    = 1.0 - Om - OR
        rho_DE = OL0 * (1.0 + A_T * np.sin(omega_T * z_arr) / (1.0 + z_arr))
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── W27: GW Depletion with Free Coupling (k=3) ────────────────────────────────
# A1+C2: GW depletion coupling delta_GW is free.
# rho_DE = OL0 * exp(-delta_GW * Om^2 * (E^2 - 1)). k=3.
def W27_E_factory(delta_GW):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0: return None
        E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
        E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
        rho_DE  = OL0 * np.exp(-delta_GW * Om**2 * (E_lcdm**2 - 1.0))
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── W28: SOC with Free Avalanche Exponent (k=3) ──────────────────────────────
# A1+A4: SOC avalanche exponent tau_SOC is free.
# rho_DE = OL0 * (1+z)^(-tau_SOC). k=3.
def W28_E_factory(tau_SOC):
    def E_func(z_arr, Om):
        OL0    = 1.0 - Om - OR
        rho_DE = OL0 * (1+z_arr)**(-tau_SOC)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── W29: Critical Slowing Down with Free Width (k=3) ─────────────────────────
# A4: Near balance point, critical slowing width sigma_bal is free.
# rho_DE = OL0 * (1 + delta_CSD * tanh((z - z_bal)/sigma_bal)).
# delta_CSD = 1/(2*pi) fixed; sigma_bal free. k=3.
def W29_E_factory(sigma_bal):
    delta_CSD = 1.0 / (2.0 * math.pi)
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0 or sigma_bal <= 0: return None
        z_bal  = max(0.1, (OL0/Om)**(1.0/3.0) - 1.0)
        rho_DE = OL0 * (1.0 + delta_CSD * np.tanh((z_arr - z_bal) / sigma_bal))
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ── W30: Percolation + Mean Free Path Composite (k=3) ────────────────────────
# A1+A3+A4: Combines percolation network topology with mean free path escape.
# rho_DE = OL0 * exp(-kappa * Om * ((1+z)^3 - 1)) * (1 - phi_perc)
# where phi_perc = max(0, 1 - p_c_fixed / (Om*(1+z)^3 / OL0))^1.
# p_c_fixed = 1/2 (Bethe). kappa is free. k=3.
def W30_E_factory(kappa):
    p_c = 0.5   # fixed percolation threshold
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0: return None
        f_esc   = np.exp(-kappa * Om * ((1+z_arr)**3 - 1.0))
        num     = Om * (1+z_arr)**3
        den     = num + OL0
        p       = num / np.maximum(den, 1e-15)
        phi     = np.maximum(0.0, 1.0 - p_c / np.maximum(p, 1e-10))
        rho_DE  = OL0 * f_esc * (1.0 - phi)
        # Normalize so that at z=0: f_esc~1, phi~0, rho_DE~OL0 (for small z)
        # Actually at z=0 phi=max(0,1-p_c*OL0/Om): could be nonzero. Renormalize.
        f0      = math.exp(0.0)   # =1
        p0      = Om / (Om + OL0)
        phi0    = max(0.0, 1.0 - p_c / max(p0, 1e-10))
        norm    = (1.0 - phi0)
        if norm < 1e-10: return None
        rho_DE  = OL0 * f_esc * (1.0 - phi) / norm
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func


# ==============================================================================
# WORKER FUNCTION
# ==============================================================================

def worker_fn(args):
    """Runs in a separate process."""
    os.environ['OMP_NUM_THREADS']      = '1'
    os.environ['MKL_NUM_THREADS']      = '1'
    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    np.seterr(all='ignore')
    warnings.filterwarnings('ignore')

    wid, theory_name, k, E_func_or_factory, extra_starts = args

    try:
        if k == 2:
            def wrapper(p):
                return chi2_func(p, E_func_or_factory)
            x_best, chi2_best = multi_start_optimize(wrapper, n_params=2)
            if x_best is None:
                return {'id': wid, 'name': theory_name, 'k': k,
                        'chi2': 1e8, 'aicc': 1e8, 'd_aicc': 1e8,
                        'Om': None, 'H0': None, 'extra': None, 'status': 'FAIL'}
            Om_best, H0_best = float(x_best[0]), float(x_best[1])
            extra_best = None

        else:  # k == 3
            def full_wrapper(p):
                try:
                    E_fn = E_func_or_factory(p[2])
                    return chi2_func(p[:2], E_fn)
                except Exception:
                    return 1e8

            base_Om_H0 = [
                [0.315, 67.4], [0.30, 68.0], [0.32, 69.0],
                [0.29, 70.0],  [0.31, 68.5], [0.28, 71.0],
                [0.33, 67.0],  [0.34, 66.5],
            ]
            combined_starts = []
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
                return {'id': wid, 'name': theory_name, 'k': k,
                        'chi2': 1e8, 'aicc': 1e8, 'd_aicc': 1e8,
                        'Om': None, 'H0': None, 'extra': None, 'status': 'FAIL'}
            Om_best, H0_best = float(best_x[0]), float(best_x[1])
            chi2_best  = best_val
            extra_best = float(best_x[2])

        aicc_val = aicc(chi2_best, k)
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
        # k=2 theories (W01-W20)
        ('W01', 'Mean Free Path Modulated DE',         2, W01_E,  None),
        ('W02', 'Percolation Threshold Network',        2, W02_E,  None),
        ('W03', 'Critical Slowing Down Balance',        2, W03_E,  None),
        ('W04', 'Quantum Walk Dark Energy',             2, W04_E,  None),
        ('W05', 'SOC Avalanche Distribution',           2, W05_E,  None),
        ('W06', 'RG Flow Annihilation Rate',            2, W06_E,  None),
        ('W07', 'Fractal Void Boundary DE',             2, W07_E,  None),
        ('W08', 'Levy Flight Generation Stats',         2, W08_E,  None),
        ('W09', 'Small-World SQ Network',               2, W09_E,  None),
        ('W10', 'Ising Vacuum Phase Transition',        2, W10_E,  None),
        ('W16', 'DLA Fractal Annihilation',             2, W16_E,  None),
        ('W17', 'Spin-Glass SQ Vacuum',                 2, W17_E,  None),
        ('W18', 'Topological Defect Annihilation',      2, W18_E,  None),
        ('W19', 'Turing Instability DE',                2, W19_E,  None),
        ('W20', 'GW-Resonance SQ Depletion',            2, W20_E,  None),
        # k=3 theories (W11-W15, W21-W30)
        ('W11', 'Percolation Free Threshold',           3, W11_E_factory,
            [[0.3], [0.5], [0.7], [1.0], [1.5], [2.0]]),
        ('W12', 'MFP Free Opacity',                     3, W12_E_factory,
            [[0.1], [0.5], [1.0], [2.0], [3.0], [5.0]]),
        ('W13', 'RG Free Anomalous Dimension',          3, W13_E_factory,
            [[0.1], [0.5], [1.0], [2.0], [-0.5], [-1.0]]),
        ('W14', 'Quantum Walk Free Dimension',          3, W14_E_factory,
            [[0.3], [0.5], [1.0], [1.5], [2.0], [0.1]]),
        ('W15', 'Network Free Clustering',              3, W15_E_factory,
            [[0.1], [0.3], [0.5], [1.0], [2.0], [0.05]]),
        ('W21', 'Levy Free Exponent',                   3, W21_E_factory,
            [[0.5], [1.0], [1.5], [2.0], [0.2], [3.0]]),
        ('W22', 'DLA Free Fractal Dimension',           3, W22_E_factory,
            [[2.1], [2.3], [2.5], [2.7], [2.9], [2.0]]),
        ('W23', 'Topological Defect Free Exponent',    3, W23_E_factory,
            [[0.1], [0.3], [0.5], [1.0], [2.0], [0.05]]),
        ('W24', 'Ising Free Beta Exponent',             3, W24_E_factory,
            [[0.1], [0.3], [0.5], [1.0], [2.0], [0.05]]),
        ('W25', 'Spin-Glass Free Decoherence Time',     3, W25_E_factory,
            [[0.5], [1.0], [2.0], [math.pi], [5.0], [0.2]]),
        ('W26', 'Turing Free Frequency',                3, W26_E_factory,
            [[0.5], [1.0], [math.pi/2], [math.pi], [2.0], [3.0]]),
        ('W27', 'GW Depletion Free Coupling',           3, W27_E_factory,
            [[0.01], [0.05], [0.1], [0.5], [1.0], [0.005]]),
        ('W28', 'SOC Free Avalanche Exponent',          3, W28_E_factory,
            [[0.5], [1.0], [1.5], [2.0], [0.2], [3.0]]),
        ('W29', 'CSD Free Balance Width',               3, W29_E_factory,
            [[0.1], [0.3], [0.5], [1.0], [2.0], [0.05]]),
        ('W30', 'Percolation+MFP Composite',            3, W30_E_factory,
            [[0.1], [0.5], [1.0], [2.0], [3.0], [5.0]]),
    ]
    return theories


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    out_dir   = _SCRIPT_DIR
    json_path = os.path.join(out_dir, 'l30_results2.json')

    theories  = build_theory_list()
    task_args = []
    for wid, name, k, E_func_or_factory, extra_starts in theories:
        task_args.append((wid, name, k, E_func_or_factory, extra_starts))

    print('=' * 65)
    print('L30 2nd Run SQMH Theory Test (W01-W30)')
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
    print('{:<5} {:<40} {:>2} {:>9} {:>9} {:>8} {:>6}'.format(
        'ID', 'Theory', 'k', 'chi2', 'AICc', 'dAICc', 'Status'))
    print('-' * 84)
    pass_count = 0
    kill_count = 0
    for r in results:
        chi2_str  = '{:.4f}'.format(r['chi2'])   if r['chi2']   < 1e7 else 'FAIL'
        aicc_str  = '{:.4f}'.format(r['aicc'])   if r['aicc']   < 1e7 else 'FAIL'
        daicc_str = '{:.4f}'.format(r['d_aicc']) if r.get('d_aicc', 1e8) < 1e7 else 'FAIL'
        print('{:<5} {:<40} {:>2} {:>9} {:>9} {:>8} {:>6}'.format(
            r['id'], r['name'][:40], r['k'],
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
