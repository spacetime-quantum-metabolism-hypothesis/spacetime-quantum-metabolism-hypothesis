# -*- coding: utf-8 -*-
"""
l30_k93_reeval.py -- K93 Re-evaluation for V~BB series (L30)
=============================================================
Correct wa_proxy formula:
  wa_proxy_correct = lnrho_diff / lna_diff / (-3.0)
  lna_diff = log(1/(1+0.5)) = log(2/3) ~ -0.405
  lnrho_diff = log(rde(z=0.5) / rde(z=0))
  rde(z) = E(z)^2 - OR*(1+z)^4 - Om*(1+z)^3

K93: KILLS if wa_proxy_correct >= 0

New status:
  PASS if (old_aicc < 15.392 AND wa_proxy_correct < 0)
  else KILL
"""

import os
import sys
import math
import json
import warnings
import numpy as np

warnings.filterwarnings('ignore')
np.seterr(all='ignore')

# ── paths ──────────────────────────────────────────────────────────────────────
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SIM_DIR    = os.path.dirname(_SCRIPT_DIR)
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

# ── constants ──────────────────────────────────────────────────────────────────
OR   = 9.15e-5   # radiation density (from ee2_fit.py / ee2_ode.py)
LCDM_AICC_BASELINE = 15.392

lna_diff = math.log(1.0 / (1.0 + 0.5))   # log(2/3) ~ -0.4055

# ── wa_proxy computation ────────────────────────────────────────────────────────
def compute_wa_proxy(E_func, Om):
    """Compute correct wa_proxy for a theory given E_func and Om."""
    z0  = 0.0
    z05 = 0.5

    try:
        E0  = float(E_func(np.array([z0]),  Om)[0])
        E05 = float(E_func(np.array([z05]), Om)[0])
    except Exception:
        return float('nan')

    if not math.isfinite(E0) or not math.isfinite(E05):
        return float('nan')

    rde0  = E0**2  - OR*(1+z0)**4  - Om*(1+z0)**3
    rde05 = E05**2 - OR*(1+z05)**4 - Om*(1+z05)**3

    if rde0 <= 1e-10 or rde05 <= 1e-10:
        return float('nan')   # numerical issue

    lnrho_diff = math.log(rde05 / rde0)
    wa_proxy   = lnrho_diff / lna_diff / (-3.0)
    return wa_proxy


# ==============================================================================
# THEORY E(z) FUNCTIONS -- copied inline from test files
# ==============================================================================

# ─────── V SERIES (from l30_test.py) ────────────────────────────────────────

def V01_E(z_arr, Om):
    gamma = 1.0 / math.pi
    OL0   = 1.0 - Om - OR
    ln1z  = np.log1p(z_arr)
    rho_DE = OL0 * np.exp(-gamma * ln1z**2)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0): return None
    return np.sqrt(np.maximum(E2, 1e-30))

def V04_E(z_arr, Om):
    kappa = Om / (3.0 * (1.0 + Om))
    OL0   = 1.0 - Om - OR
    w_eff = -1.0 + kappa
    rho_DE = OL0 * (1+z_arr)**(3*(1+w_eff))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))

def V09_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0: return None
    normfac = 1.0 - math.exp(-1.0)
    E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
    exponent = np.exp(-1.0 / np.maximum(E_lcdm, 1e-10))
    denom    = np.maximum(1.0 - exponent, 1e-15)
    rho_DE   = OL0 * normfac / denom
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))

def V14_E(z_arr, Om):
    eta_irr = 2.0 / (3.0 * math.pi)
    OL0     = 1.0 - Om - OR
    a_arr   = 1.0 / (1.0 + z_arr)
    rho_DE  = OL0 * (1.0 + eta_irr * (1.0 - a_arr))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))

def V16_E(z_arr, Om):
    OL0     = 1.0 - Om - OR
    Om_B    = 0.049
    f_asym  = 1.0/3.0
    rho_DE  = OL0 - Om_B * f_asym * ((1+z_arr)**3 - 1.0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0): return None
    return np.sqrt(np.maximum(E2, 1e-30))

def V17_E(z_arr, Om):
    OL0        = 1.0 - Om - OR
    if OL0 <= 0: return None
    alpha_meta = Om / (3.0 * max(OL0, 1e-6))
    rho_DE     = OL0 * (1.0 - alpha_meta * ((1+z_arr)**3 - 1.0))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0): return None
    return np.sqrt(np.maximum(E2, 1e-30))

def V25_E(z_arr, Om):
    lambda_p = -1.0 / (4.0 * math.pi)
    OL0      = 1.0 - Om - OR
    rho_DE   = OL0 + lambda_p * Om * ((1+z_arr)**3 - 1.0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0): return None
    return np.sqrt(np.maximum(E2, 1e-30))

def V27_E(z_arr, Om):
    epsilon_inf = -Om / (2.0 * math.pi)
    z_c         = 0.5
    OL0         = 1.0 - Om - OR
    E2_base     = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E_base      = np.sqrt(np.maximum(E2_base, 1e-30))
    E_eff       = E_base * (1.0 + epsilon_inf * np.exp(-z_arr / z_c))
    return E_eff

def V28_E(z_arr, Om):
    # Lense-Thirring Dark Energy (from l30_test.py V28 exact definition)
    # C3: cosmic angular momentum scales as Om*(1+z)^2; alpha_LT=1/(4*pi)
    alpha_LT = 1.0 / (4.0 * math.pi)
    OL0      = 1.0 - Om - OR
    rho_DE   = OL0 * (1.0 + alpha_LT * Om * ((1+z_arr)**2 - 1.0))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0): return None
    return np.sqrt(np.maximum(E2, 1e-30))

# ─────── W SERIES (from l30_test2.py) ───────────────────────────────────────

def W03_E(z_arr, Om):
    OL0       = 1.0 - Om - OR
    delta_CSD = 1.0 / (2.0 * math.pi)
    sigma_bal = 1.0 / math.sqrt(2.0 * math.pi)
    if Om <= 0 or OL0 <= 0: return None
    z_bal = max(0.1, (OL0 / Om)**(1.0/3.0) - 1.0)
    rho_DE = OL0 * (1.0 + delta_CSD * np.tanh((z_arr - z_bal) / sigma_bal))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0): return None
    return np.sqrt(np.maximum(E2, 1e-30))

def W19_E(z_arr, Om):
    A_T     = 1.0 / (4.0 * math.pi)
    omega_T = math.pi / 2.0
    OL0     = 1.0 - Om - OR
    rho_DE  = OL0 * (1.0 + A_T * np.sin(omega_T * z_arr) / (1.0 + z_arr))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0): return None
    return np.sqrt(np.maximum(E2, 1e-30))

def W20_E(z_arr, Om):
    delta_GW = 1.0 / (2.0 * math.pi**2)
    OL0      = 1.0 - Om - OR
    if OL0 <= 0: return None
    E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
    rho_DE  = OL0 * np.exp(-delta_GW * Om**2 * (E_lcdm**2 - 1.0))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    return np.sqrt(np.maximum(E2, 1e-30))

# ─────── X SERIES (from l30_test3.py) ───────────────────────────────────────

def X21_E(z_arr, Om):
    # Arnold Diffusion SQ Mixing DE (from l30_test3.py X21 exact definition)
    # rho_DE = OL0*(1 + A_Arn*exp(-1/(E^2-1+delta_r))) / norm0
    A_Arn   = 1.0 / (2.0 * math.pi)
    delta_r = 1.0 / math.pi
    OL0     = 1.0 - Om - OR
    if OL0 <= 0: return None
    E2_lcdm = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E_lcdm  = np.sqrt(np.maximum(E2_lcdm, 1e-30))
    eps     = np.maximum(E_lcdm**2 - 1.0 + delta_r, 1e-10)
    rho_DE  = OL0 * (1.0 + A_Arn * np.exp(-1.0 / eps))
    norm0   = 1.0 + A_Arn * math.exp(-1.0 / delta_r)
    rho_DE  = rho_DE / norm0
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0): return None
    return np.sqrt(np.maximum(E2, 1e-30))

# ─────── Y SERIES (from l30_test4.py) ───────────────────────────────────────
# Y series: no PASS entries (all KILL by AICc). Nothing to evaluate.

# ─────── Z SERIES (from l30_test5.py) ───────────────────────────────────────

def Z01_E(z_arr, Om):
    A1_pl = (3.0 / (4.0 * math.pi))**(1.0/3.0)
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0: return None
    num  = 1.0 + A1_pl * (Om * (1+z_arr)**3)**(1.0/3.0)
    den0 = 1.0 + A1_pl * Om**(1.0/3.0)
    rho_DE = OL0 * num / den0
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0): return None
    return np.sqrt(np.maximum(E2, 1e-30))

def Z20_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0: return None
    x      = np.sqrt(Om * (1+z_arr)**3 / OL0)
    x0     = math.sqrt(Om / OL0)
    f      = np.exp(-x) * np.sinh(x)
    f0     = math.exp(-x0) * math.sinh(x0)
    if abs(f0) < 1e-10: return None
    rho_DE = OL0 * f / f0
    rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0): return None
    return np.sqrt(np.maximum(E2, 1e-30))

# ─────── AA SERIES (from l30_test6.py) ──────────────────────────────────────

def AA27_E_factory(rho_th_frac):
    def E_func(z_arr, Om):
        OL0 = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0 or rho_th_frac <= 0: return None
        rho_th = rho_th_frac * OL0
        Om_z   = Om * (1 + z_arr)**3
        denom  = np.maximum(rho_th, Om_z)
        rho_DE = rho_th * OL0 / denom
        denom0 = max(rho_th, Om)
        rho_DE0_val = rho_th * OL0 / denom0
        if rho_DE0_val < 1e-10: return None
        rho_DE = rho_DE * OL0 / rho_DE0_val
        rho_DE = np.maximum(rho_DE, 1e-10 * OL0)
        E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
        if np.any(E2 < 0): return None
        return np.sqrt(np.maximum(E2, 1e-30))
    return E_func

# ─────── BB SERIES (from l30_test7.py) ──────────────────────────────────────
# BB series uses E_random_from_descriptor with basis functions.
# Need to reconstruct each theory's descriptor from the JSON name field.

def _basis_func(bid, z_arr):
    z = z_arr
    if   bid == 0:  return np.log1p(z)
    elif bid == 1:  return z
    elif bid == 2:  return z**2
    elif bid == 3:  return z**3
    elif bid == 4:  return np.sqrt(1.0 + z) - 1.0
    elif bid == 5:  return np.exp(-z) - 1.0
    elif bid == 6:  return np.exp(-z**2) - 1.0
    elif bid == 7:  return np.tanh(z)
    elif bid == 8:  return np.sin(math.pi/2 * z)
    elif bid == 9:
        from scipy.special import erf
        return erf(z)
    elif bid == 10: return z * np.log1p(z)
    elif bid == 11: return np.exp(z) - 1.0
    elif bid == 12: return np.log1p(z)**2
    elif bid == 13: return np.tanh(2.0*z)
    elif bid == 14: return np.sin(math.pi * z)
    elif bid == 15: return np.cos(math.pi * z) - 1.0
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
    else: raise ValueError(f'Unknown basis id {bid}')

BASIS_NAMES = [
    'log1p', 'z', 'z2', 'z3', 'sqrt_m1', 'expnz_m1', 'expnz2_m1',
    'tanh', 'sin_pi2', 'erf', 'zlog1p', 'expz_m1', 'log1p2',
    'tanh2z', 'sinpiz', 'cospiz_m1', 'arctan', 'zsinhz', 'zcoshm1',
    'pow025_m1', 'pow05_m1', 'pow075_m1', 'pow15_m1', 'pow20_m1',
    'pow25_m1', 'pow30_m1', 'log1pz2', 'expnz2_m1b', 'z_over_1pz', 'tanh_h',
]
BASIS_MAP = {name: i for i, name in enumerate(BASIS_NAMES)}

def parse_bb_descriptor(name):
    """Parse BF[c1*f1,c2*f2,...] name string into (basis_ids, coeffs)."""
    if not name.startswith('BF['):
        return None, None
    inner = name[3:-1]   # strip BF[ and ]
    terms = inner.split(',')
    basis_ids = []
    coeffs    = []
    for term in terms:
        term = term.strip()
        # find the last '*' separator between coeff and basis name
        # coeff may be negative: e.g. -0.073*pow30_m1
        star_idx = term.rfind('*')
        if star_idx < 0:
            return None, None
        c_str   = term[:star_idx]
        b_name  = term[star_idx+1:]
        try:
            c = float(c_str)
        except ValueError:
            return None, None
        if b_name not in BASIS_MAP:
            return None, None
        coeffs.append(c)
        basis_ids.append(BASIS_MAP[b_name])
    return basis_ids, coeffs

def E_random_from_descriptor(z_arr, Om, basis_ids, coeffs):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0: return None
    delta = np.zeros_like(z_arr)
    for bid, c in zip(basis_ids, coeffs):
        try:
            delta += c * _basis_func(bid, z_arr)
        except Exception:
            return None
    rho_DE = OL0 * (1.0 + delta)
    rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
    return np.sqrt(np.maximum(E2, 1e-30))

def BB_E_factory(basis_ids, coeffs):
    def E_func(z_arr, Om):
        return E_random_from_descriptor(z_arr, Om, basis_ids, coeffs)
    return E_func

# Named BB theories (adversarial, not BF descriptors)
def BB08_E(z_arr, Om):
    OL0 = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0: return None
    gamma  = Om**2 / OL0
    rho_DE = OL0 * np.exp(-gamma * z_arr**2)
    rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
    E2 = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
    if np.any(E2 < 0): return None
    return np.sqrt(np.maximum(E2, 1e-30))


# ==============================================================================
# MASTER THEORY REGISTRY
# ==============================================================================

def build_registry():
    """Build {id: (name, aicc, d_aicc, Om, E_func)} for all PASS theories."""
    registry = {}

    # ── V series ─────────────────────────────────────────────────────────────
    v_pass = [
        ("V14", "Irreversible Entropy Production",   14.2585, -1.1335, 0.29987, V14_E),
        ("V04", "Reaction-Diffusion Dark Energy",    14.2672, -1.1248, 0.29696, V04_E),
        ("V27", "SQ Inflow Hubble-Tension",          14.5259, -0.8661, 0.27318, V27_E),
        ("V28", "Lense-Thirring Dark Energy",        15.0744, -0.3176, 0.29278, V28_E),
        ("V09", "Canonical Ensemble SQ",             15.3301, -0.0619, 0.27134, V09_E),
        ("V25", "SQ Pair Production Near Matter",    15.3873, -0.0047, 0.32225, V25_E),
        ("V17", "Matter-SQ Metabolic Equilibrium",   15.3873, -0.0047, 0.44491, V17_E),
        ("V16", "SQ Quantum Number Conservation",    15.3873, -0.0047, 0.31294, V16_E),
    ]
    for entry in v_pass:
        iid, name, aicc_val, d_aicc, om_val, e_fn = entry
        registry[iid] = (name, aicc_val, d_aicc, om_val, e_fn)

    # ── W series ─────────────────────────────────────────────────────────────
    w_pass = [
        ("W19", "Turing Instability DE",         14.4737, -0.9183, 0.30109, W19_E),
        ("W03", "Critical Slowing Down Balance",  14.7919, -0.6001, 0.27692, W03_E),
        ("W20", "GW-Resonance SQ Depletion",     15.3885, -0.0035, 0.29752, W20_E),
    ]
    for entry in w_pass:
        iid, name, aicc_val, d_aicc, om_val, e_fn = entry
        registry[iid] = (name, aicc_val, d_aicc, om_val, e_fn)

    # ── X series ─────────────────────────────────────────────────────────────
    x_pass = [
        ("X21", "Arnold Diffusion SQ Mixing DE", 14.4227, -0.9693, 0.29651, X21_E),
    ]
    for entry in x_pass:
        iid, name, aicc_val, d_aicc, om_val, e_fn = entry
        registry[iid] = (name, aicc_val, d_aicc, om_val, e_fn)

    # ── Y series ─────────────────────────────────────────────────────────────
    # No PASS entries in Y series
    pass

    # ── Z series ─────────────────────────────────────────────────────────────
    z_pass = [
        ("Z20", "SQ Sinh Decay Potential DE",        14.0193, -1.3727, 0.31294, Z20_E),
        ("Z01", "Annihilation Rate Power-Law SQ DE", 14.6111, -0.7809, 0.29091, Z01_E),
    ]
    for entry in z_pass:
        iid, name, aicc_val, d_aicc, om_val, e_fn = entry
        registry[iid] = (name, aicc_val, d_aicc, om_val, e_fn)

    # ── AA series ─────────────────────────────────────────────────────────────
    # AA27 uses factory with extra=2.7539725
    AA27_extra = 2.7539725145430576
    aa_pass = [
        ("AA27", "Quantum Boundary Free Threshold", 14.8766, -0.5154, 0.32588,
         AA27_E_factory(AA27_extra)),
    ]
    for entry in aa_pass:
        iid, name, aicc_val, d_aicc, om_val, e_fn = entry
        registry[iid] = (name, aicc_val, d_aicc, om_val, e_fn)

    # ── BB series ─────────────────────────────────────────────────────────────
    bb_pass_json = [
        ("BB23", "BF[0.670*z_over_1pz,-0.073*pow30_m1,0.165*pow075_m1]", 12.1015, -3.2905, 0.33885),
        ("BB11", "BF[0.002*z_over_1pz,-0.556*pow05_m1,0.314*tanh2z]",    12.9631, -2.4289, 0.31453),
        ("BB20", "BF[0.048*sinpiz]",                                       13.8941, -1.4979, 0.30393),
        ("BB15", "BF[0.644*pow075_m1,-0.071*sin_pi2,-0.476*log1p2]",      13.9881, -1.4039, 0.30112),
        ("BB13", "BF[0.244*z_over_1pz]",                                   14.1608, -1.2312, 0.30037),
        ("BB12", "BF[0.098*sin_pi2]",                                       14.1730, -1.2190, 0.30330),
        ("BB14", "BF[-0.196*expnz_m1]",                                     14.2350, -1.1570, 0.29909),
        ("BB16", "BF[0.705*pow025_m1]",                                     14.3692, -1.0228, 0.29676),
        ("BB17", "BF[0.104*tanh_h,0.424*pow025_m1]",                       14.4282, -0.9638, 0.29646),
        ("BB18", "BF[0.321*tanh_h]",                                        14.4554, -0.9366, 0.29593),
        ("BB19", "BF[0.116*arctan]",                                        14.4588, -0.9332, 0.29760),
        ("BB30", "BF[0.256*tanh_h,0.160*pow075_m1]",                       14.4637, -0.9283, 0.29481),
        ("BB21", "BF[0.058*tanh_h,0.023*pow15_m1]",                        14.8874, -0.5046, 0.29494),
        ("BB27", "BF[0.240*pow025_m1]",                                     14.9160, -0.4760, 0.29663),
        ("BB24", "BF[0.028*pow20_m1]",                                      15.0198, -0.3722, 0.29193),
        ("BB26", "BF[-0.138*expnz2_m1]",                                    15.0210, -0.3710, 0.29333),
        ("BB22", "BF[0.146*expnz_m1,0.289*z,-0.170*tanh_h]",              15.0293, -0.3627, 0.28922),
        ("BB29", "BF[0.202*log1p2]",                                        15.0948, -0.2972, 0.29018),
        ("BB28", "BF[0.150*log1pz2]",                                       15.1547, -0.2373, 0.29002),
        ("BB08", "PullWeighted Gaussian Decay",                             15.3350, -0.0570, 0.30886),
    ]

    for iid, name, aicc_val, d_aicc, om_val in bb_pass_json:
        if name.startswith('BF['):
            basis_ids, coeffs = parse_bb_descriptor(name)
            if basis_ids is not None:
                e_fn = BB_E_factory(basis_ids, coeffs)
            else:
                print(f'  WARNING: could not parse descriptor for {iid}: {name}')
                continue
        elif iid == 'BB08':
            e_fn = BB08_E
        else:
            print(f'  WARNING: no E_func for {iid}: {name}')
            continue
        registry[iid] = (name, aicc_val, d_aicc, om_val, e_fn)

    return registry


# ==============================================================================
# SERIES MEMBERSHIP
# ==============================================================================

SERIES_MAP = {
    'V': ['V14', 'V04', 'V27', 'V28', 'V09', 'V25', 'V17', 'V16'],
    'W': ['W19', 'W03', 'W20'],
    'X': ['X21'],
    'Y': [],
    'Z': ['Z20', 'Z01'],
    'AA': ['AA27'],
    'BB': ['BB23', 'BB11', 'BB20', 'BB15', 'BB13', 'BB12', 'BB14', 'BB16',
           'BB17', 'BB18', 'BB19', 'BB30', 'BB21', 'BB27', 'BB24', 'BB26',
           'BB22', 'BB29', 'BB28', 'BB08'],
}

# Total AICc-PASS counts from JSON files (for summary table)
AICC_PASS_COUNTS = {
    'V': 8, 'W': 3, 'X': 1, 'Y': 0, 'Z': 2, 'AA': 1, 'BB': 20,
}

SERIES_LABELS = {
    'V': 'V (l30_test.py)',
    'W': 'W (l30_test2.py)',
    'X': 'X (l30_test3.py)',
    'Y': 'Y (l30_test4.py)',
    'Z': 'Z (l30_test5.py)',
    'AA': 'AA (l30_test6.py)',
    'BB': 'BB (l30_test7.py)',
}


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("=" * 70)
    print("L30 K93 Re-evaluation: V~BB series")
    print("=" * 70)
    print(f"OR = {OR}")
    print(f"lna_diff = log(1/(1+0.5)) = {lna_diff:.6f}")
    print(f"LCDM AICc baseline = {LCDM_AICC_BASELINE}")
    print()

    registry = build_registry()

    results = {}   # iid -> {name, aicc, d_aicc, Om, wa, new_status}

    for iid, (name, aicc_val, d_aicc, om_val, e_fn) in registry.items():
        wa = compute_wa_proxy(e_fn, om_val)
        new_status = 'PASS' if (aicc_val < LCDM_AICC_BASELINE and
                                math.isfinite(wa) and wa < 0.0) else 'KILL'
        results[iid] = {
            'name': name, 'aicc': aicc_val, 'd_aicc': d_aicc,
            'Om': om_val, 'wa': wa, 'new_status': new_status,
        }

    # ── per-series summary ──────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("PER-SERIES SUMMARY")
    print("=" * 70)
    series_summaries = {}
    for series in ['V', 'W', 'X', 'Y', 'Z', 'AA', 'BB']:
        ids = SERIES_MAP[series]
        pass_ids = [iid for iid in ids if iid in results and results[iid]['new_status'] == 'PASS']
        series_summaries[series] = pass_ids
        n_aicc = AICC_PASS_COUNTS[series]
        print(f"  {series:4s}: AICc PASS = {n_aicc:2d}  |  K93 PASS = {len(pass_ids):2d}")

    # ── K93-passing theories ────────────────────────────────────────────────
    k93_pass = [(iid, r) for iid, r in results.items() if r['new_status'] == 'PASS']
    k93_pass.sort(key=lambda x: x[1]['aicc'])

    print(f"\n{'='*70}")
    print(f"K93-PASSING THEORIES (total = {len(k93_pass)})")
    print(f"{'='*70}")
    hdr = f"{'ID':8s} {'Series':4s} {'AICc':8s} {'dAICc':8s} {'wa_correct':12s} {'Om':8s} {'Name'}"
    print(hdr)
    print("-" * 90)
    for iid, r in k93_pass:
        series = ''.join([c for c in iid if not c.isdigit()])
        wa_str = f"{r['wa']:+.4f}" if math.isfinite(r['wa']) else "  NaN"
        print(f"{iid:8s} {series:4s} {r['aicc']:8.4f} {r['d_aicc']:+8.4f} {wa_str:12s} {r['Om']:8.5f} {r['name'][:40]}")

    # ── all evaluated (including K93 kill) ──────────────────────────────────
    print(f"\n{'='*70}")
    print(f"ALL AICc-PASS THEORIES WITH wa_correct")
    print(f"{'='*70}")
    all_ids = list(results.keys())
    all_ids.sort(key=lambda x: results[x]['aicc'])
    hdr2 = f"{'ID':8s} {'AICc':8s} {'wa_correct':12s} {'K93':6s} {'Name'}"
    print(hdr2)
    print("-" * 80)
    for iid in all_ids:
        r = results[iid]
        wa_str = f"{r['wa']:+.4f}" if math.isfinite(r['wa']) else "   NaN"
        print(f"{iid:8s} {r['aicc']:8.4f} {wa_str:12s} {r['new_status']:6s} {r['name'][:40]}")

    # ── champion ─────────────────────────────────────────────────────────────
    if k93_pass:
        champ_id, champ_r = k93_pass[0]
        print(f"\n{'='*70}")
        print(f"CHAMPION K93-COMPLIANT THEORY")
        print(f"  ID         : {champ_id}")
        print(f"  Name       : {champ_r['name']}")
        print(f"  AICc       : {champ_r['aicc']:.4f}  (dAICc = {champ_r['d_aicc']:+.4f})")
        print(f"  wa_correct : {champ_r['wa']:+.6f}")
        print(f"  Om         : {champ_r['Om']:.5f}")
    else:
        print("\nNo K93-passing theories found.")

    # ── return data for base.md append ──────────────────────────────────────
    return results, k93_pass, series_summaries


if __name__ == '__main__':
    results, k93_pass, series_summaries = main()
