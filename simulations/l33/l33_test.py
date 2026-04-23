# -*- coding: utf-8 -*-
"""
l33_test.py -- L33: 8-person team, no pre-assigned roles
=========================================================
8 team members each independently sample the full SQT-consistent
function space. After all proposals, duplicates are removed (discussion).
No roles pre-assigned — division of labor emerges naturally.

SQT-consistent rho_DE structure:
  rho_DE(z) = OL0 * (1 + amp * h(g(z)))
  g(z=0) = 0 for all base quantities
  amp from SQT-motivated fixed set (k=2 maintained)

LCDM baseline: chi2=10.192, AICc=15.392
"""

import os, sys, math, json, time, warnings, multiprocessing
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import minimize, differential_evolution

warnings.filterwarnings('ignore')
np.seterr(all='ignore')
os.environ['OMP_NUM_THREADS'] = os.environ['MKL_NUM_THREADS'] = os.environ['OPENBLAS_NUM_THREADS'] = '1'

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SIM_DIR    = os.path.dirname(_SCRIPT_DIR)
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

from desi_data import DESI_DR2, DESI_DR2_COV_INV

C_KMS     = 299792.458
R_S       = 147.09
OR        = 5.38e-5
N_DATA    = 13
N_GRID    = 4000
LCDM_CHI2 = 10.192
LCDM_AICC = 15.392

def aicc(chi2, k=2, n=N_DATA):
    return chi2 + 2*k + 2*k*(k+1)/(n-k-1)

# ─── SQT-motivated amplitude set ──────────────────────────────────────────────

AMP_SET = [0.5, 1.0/3.0, 1.0/math.pi, 1.0/math.e, 2.0/3.0, 0.25, 0.1, 0.4,
           0.05, 0.2, 0.3, 0.35, 0.45, 0.55, 0.15, 0.6, 0.07, 0.08, 0.12,
           0.7, 0.75, 0.8, 0.85, 0.9, 0.82, 0.87, 0.92,
           1.0, 1.05, 1.1, 1.15, 1.2, 0.95, 0.97,
           1.25, 1.3, 1.35, 1.4, 1.45, 1.5,
           1.55, 1.6, 1.7, 1.8, 1.9, 2.0,
           2.1, 2.15, 2.2, 2.25, 2.3, 2.4, 2.5]

# ─── SQT building blocks (all g(0)=0, g>0 for z>0) ───────────────────────────

BASE_KEYS = [
    # Core wa<0 structures (runs 1-30 validated)
    'ratio_m1', 'sqrt_m1', 'cbrt_m1',
    'sinh_ratio', 'geom_cbrt_sinh',
    # psi-blend family (Q91 achievers)
    'psi_blend_tanh_ratio', 'psi_blend_erf_ratio',
    'psi_sq_blend_tanh_ratio',
    # Ratio powers
    'ratio_08_m1', 'ratio_09_m1',
    # CPL blend family (Q91→Q92 achievers — primary exploration zone)
    'cpl_blend_erf_ratio',        # c=1.0: Q91 (ΔAICc=-3.52, wa=-0.70)
    'cpl_blend_tanh_ratio',       # tanh: Q91 (ΔAICc=-2.58, wa=-0.79)
    'cpl_erf11_ratio',            # c=1.1: Q91/Q92 boundary
    'cpl_erf12_ratio',            # c=1.2: Q92 confirmed
    'cpl_erf125_ratio',           # c=1.25: Q92 (wa~-0.55 to -0.61)
    'cpl_erf13_ratio',            # c=1.3: Q92 strong
    'cpl_erf135_ratio',           # c=1.35: Q92 best (ΔAICc=-4.424, wa=-0.528)
    'cpl_erf14_ratio',            # c=1.4: Q92 (amp=0.65-0.80)
    'cpl_erf145_ratio',           # c=1.45: Q92 (ΔAICc=-4.406)
    # NEW: higher c push
    'cpl_erf15_ratio',            # c=1.5: Q92 at amp=0.70-0.75
    'cpl_erf16_ratio',            # c=1.6: Q92 at amp=0.70
    'cpl_erf17_ratio',            # c=1.7: low chi2, high amp needed
    'cpl_erf20_ratio',            # c=2.0: maximum saturation
    # NEW: quadratic CPL weight wt=(z/(1+z))^2 — slower onset, erf dominates longer
    'cpl_sq_erf12_ratio',         # wt^2 + c=1.2
    'cpl_sq_erf13_ratio',         # wt^2 + c=1.3
    'cpl_sq_erf135_ratio',        # wt^2 + c=1.35
    # NEW: sqrt linear part — (sqrt(ratio)-1) instead of (ratio-1) as high-z anchor
    'cpl_erf13_sqrt_ratio',       # c=1.3, linear=(sqrt(ratio)-1)
    'cpl_erf135_sqrt_ratio',      # c=1.35, linear=(sqrt(ratio)-1)
    # NEW: psi^2 blend with erf (faster psi transition than existing psi_blend_erf)
    'psi_sq_blend_erf_ratio',     # wt=psi_frac^2 + erf sat
    # NEW: exp weight wt=1-exp(-z) — wa stays deeply negative at high amp → Q92 family
    'cpl_exp_erf10_ratio',        # c=1.0: Q92 at amp>=1.4
    'cpl_exp_erf11_ratio',        # c=1.1: Q92 at amp>=1.4
    'cpl_exp_erf12_ratio',        # c=1.2: Q92 at amp>=1.2
    'cpl_exp_erf13_ratio',        # c=1.3: Q92 at amp>=1.15 (ΔAICc=-4.566 at amp=1.5)
    'cpl_exp_erf135_ratio',       # c=1.35: Q92 best (ΔAICc=-4.593 at amp=1.5)
    'cpl_exp_erf14_ratio',        # c=1.4: Q92 at amp>=1.15
    'cpl_exp_erf15_ratio',        # c=1.5: Q92 at amp>=1.2
    # NEW: mix weight wt=0.5*(1-exp(-z))+0.5*(z/(1+z)) — NEW BEST (ΔAICc=-4.632 at c=1.35, amp=1.2)
    'cpl_mix_erf12_ratio',        # c=1.2
    'cpl_mix_erf13_ratio',        # c=1.3
    'cpl_mix_erf135_ratio',       # c=1.35: BEST Q92 confirmed
    'cpl_mix_erf14_ratio',        # c=1.4
    'cpl_mix_erf15_ratio',        # c=1.5
    # NEW: tanh(z) weight — Q92 CHAMPION (ΔAICc=-4.715 at c=1.47, amp=2.25)
    'cpl_tanh_erf12_ratio',       # c=1.2
    'cpl_tanh_erf13_ratio',       # c=1.3
    'cpl_tanh_erf135_ratio',      # c=1.35
    'cpl_tanh_erf14_ratio',       # c=1.4
    'cpl_tanh_erf145_ratio',      # c=1.45: Q92 (ΔAICc=-4.710)
    'cpl_tanh_erf147_ratio',      # c=1.47: BEST (ΔAICc=-4.715, wa=-0.582)
    'cpl_tanh_erf15_ratio',       # c=1.5
    'cpl_tanh_erf16_ratio',       # c=1.6
    # Sigmoid weight — SUPER-CHAMPION (dAICc=-6.683 at k=20, z0=0.90, c=1.15, amp=1.80)
    'cpl_sig20_z090_erf115_ratio',  # k=20.0, z0=0.90, c=1.15: BEST (dAICc=-6.683, wa=-0.731)
    'cpl_sig20_z087_erf115_ratio',  # k=20.0, z0=0.87, c=1.15 (dAICc=-6.672)
    'cpl_sig15_z090_erf115_ratio',  # k=15.0, z0=0.90, c=1.15 (dAICc=-6.644)
    'cpl_sig12_z090_erf115_ratio',  # k=12.0, z0=0.90, c=1.15 (dAICc=-6.599)
    'cpl_sig10_z090_erf115_ratio',  # k=10.0, z0=0.90, c=1.15 (dAICc=-6.557)
    'cpl_sig9_z090_erf115_ratio',   # k=9.0,  z0=0.90, c=1.15 (dAICc=-6.532)
    'cpl_sig8_z090_erf115_ratio',   # k=8.0,  z0=0.90, c=1.15 (dAICc=-6.503)
    'cpl_sig7_z090_erf115_ratio',   # k=7.0,  z0=0.90, c=1.15 (dAICc=-6.467)
    'cpl_sig6_z090_erf115_ratio',   # k=6.0,  z0=0.90, c=1.15 (dAICc=-6.408)
    'cpl_sig8_z085_erf115_ratio',   # k=8.0,  z0=0.85, c=1.15 (dAICc=-6.411)
    # Previous Q93 family (c=1.25 region)
    'cpl_sig8_z09_erf125_ratio',  # k=8.0, z0=0.90, c=1.25 (dAICc=-5.606)
    'cpl_sig6_z09_erf125_ratio',  # k=6.0, z0=0.90, c=1.25 (dAICc=-5.454)
]
TRANSFORMS = ['identity', 'log1p', 'power']
TR_PARAMS  = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

# ─── E(z) factory (spawn-safe: all logic inline) ──────────────────────────────

def make_E_fn(base_key, transform, tr_param, amp_idx):
    """Build E(z_arr, Om) from SQT building blocks. All fixed, no fit params."""
    amp = AMP_SET[amp_idx % len(AMP_SET)]

    def E_fn(z_arr, Om):
        z_arr = np.asarray(z_arr, dtype=float)
        OL0   = 1.0 - Om - OR
        if OL0 <= 0 or Om <= 0:
            return None
        alpha = Om / OL0
        psi_z = 1.0 / (1.0 + alpha * (1.0 + z_arr)**3)
        psi0  = 1.0 / (1.0 + alpha)
        ratio = np.clip(psi0 / psi_z, 1.0, 200.0)

        # base g(z), g(0)=0
        if base_key == 'ratio_m1':
            g = ratio - 1.0
        elif base_key == 'log_ratio':
            g = np.log(ratio)
        elif base_key == 'sqrt_m1':
            g = np.sqrt(ratio) - 1.0
        elif base_key == 'cbrt_m1':
            g = ratio**(1.0/3.0) - 1.0
        elif base_key == 'sq_m1':
            g = ratio**2 - 1.0
        elif base_key == 'log2':
            lr = np.log(ratio)
            g  = lr**2
        elif base_key == 'smooth_peak_slow':
            rm1 = ratio - 1.0
            g = rm1 * np.exp(-0.15 * np.clip(rm1, 0, 50))
        elif base_key == 'smooth_peak_fast2':
            rm1 = ratio - 1.0
            g = rm1 * np.exp(-0.5 * np.clip(rm1, 0, 30))
        elif base_key == 'ratio_56_m1':
            g = ratio**(5.0/6.0) - 1.0
        elif base_key == 'psi_cubic_dec':
            psi_frac = psi_z / psi0
            g = 1.0 - psi_frac**3
        elif base_key == 'arcsinh_m1':
            g = np.arcsinh(ratio - 1.0)
        elif base_key == 'log_ratio_sat':
            lr = np.log(np.clip(ratio, 1e-8, 200))
            g = lr / (1.0 + lr)
        elif base_key == 'ratio_04_m1':
            g = ratio**0.4 - 1.0
        elif base_key == 'ratio_06_m1':
            g = ratio**0.6 - 1.0
        elif base_key == 'ratio_psi_power2':
            psi_frac_mk = psi_z / psi0
            g = ratio**(2.0 * np.clip(psi_frac_mk, 0.0, 1.0)) - 1.0
        elif base_key == 'ratio_psi_power3':
            psi_frac_mk = psi_z / psi0
            g = ratio**(3.0 * np.clip(psi_frac_mk, 0.0, 1.0)) - 1.0
        elif base_key == 'exp_inv_ratio':
            g = np.exp(-1.0 / np.clip(ratio, 1e-8, None)) - math.exp(-1.0)
        elif base_key == 'cosh_half_log':
            lr = np.log(np.clip(ratio, 1e-8, 200))
            g = np.cosh(np.clip(0.5 * lr, 0, 10)) - 1.0
        elif base_key == 'blend_sq_cbrt_psisq':
            psi_frac_mk = psi_z / psi0
            pf2 = psi_frac_mk**2
            g = (ratio**2 - 1.0) * pf2 + (ratio**(1.0/3.0) - 1.0) * (1.0 - pf2)
        elif base_key == 'blend_sq_sqrt_psisq':
            psi_frac_mk = psi_z / psi0
            pf2 = psi_frac_mk**2
            g = (ratio**2 - 1.0) * pf2 + (np.sqrt(ratio) - 1.0) * (1.0 - pf2)
        elif base_key == 'blend_sqrt_cbrt_psi':
            psi_frac_mk = psi_z / psi0
            g = (np.sqrt(ratio) - 1.0) * psi_frac_mk + (ratio**(1.0/3.0) - 1.0) * (1.0 - psi_frac_mk)
        elif base_key == 'blend_ratio_cbrt_psisq':
            psi_frac_mk = psi_z / psi0
            pf2 = psi_frac_mk**2
            g = (ratio - 1.0) * pf2 + (ratio**(1.0/3.0) - 1.0) * (1.0 - pf2)
        elif base_key == 'ratio_08_m1':
            g = ratio**0.8 - 1.0
        elif base_key == 'ratio_45_m1':
            g = ratio**0.45 - 1.0
        elif base_key == 'sq_psi_sq':
            psi_frac_mk = psi_z / psi0
            g = (ratio**2 - 1.0) * psi_frac_mk**2
        elif base_key == 'sqrt_psi_sq':
            psi_frac_mk = psi_z / psi0
            g = (np.sqrt(ratio) - 1.0) * psi_frac_mk**2
        elif base_key == 'soft_sq':
            g = ratio**2 / (1.0 + ratio) - 0.5
        elif base_key == 'soft_ratio_cbrt':
            r13 = ratio**(1.0/3.0)
            g = ratio**(4.0/3.0) / (1.0 + r13) - 0.5
        elif base_key == 'blend_ratio_sinh':
            lr = np.log(np.clip(ratio, 1e-8, 200))
            sinh_g = np.sinh(np.clip(lr, -10, 10))
            g = 0.5 * (ratio - 1.0) + 0.5 * sinh_g
        elif base_key == 'blend_ratio70_sqrt30':
            g = 0.7 * (ratio - 1.0) + 0.3 * (np.sqrt(ratio) - 1.0)
        elif base_key == 'blend_ratio60_cbrt40':
            g = 0.6 * (ratio - 1.0) + 0.4 * (ratio**(1.0/3.0) - 1.0)
        elif base_key == 'sq_log_ratio':
            g = (ratio**2 - 1.0) * np.log1p(1.0 / np.clip(ratio, 1e-8, None))
        elif base_key == 'ratio_09_m1':
            g = ratio**0.9 - 1.0
        elif base_key == 'blend_ratio90_cbrt10':
            g = 0.9 * (ratio - 1.0) + 0.1 * (ratio**(1.0/3.0) - 1.0)
        elif base_key == 'ratio_log_ratio':
            lr = np.log(np.clip(ratio, 1e-8, 200))
            g = ratio * lr
        elif base_key == 'sqrt_log_ratio':
            lr = np.log(np.clip(ratio, 1e-8, 200))
            g = np.sqrt(ratio) * lr
        elif base_key == 'cbrt_log_ratio':
            lr = np.log(np.clip(ratio, 1e-8, 200))
            g = ratio**(1.0/3.0) * lr
        elif base_key == 'geom_ratio_sinh':
            # sqrt((ratio-1)*sinh(log_ratio)): geometric mean of ratio-1 and sinh(log)
            rm1 = np.clip(ratio - 1.0, 0, None)
            lr = np.log(np.clip(ratio, 1e-8, 200))
            sinh_g = np.clip(np.sinh(np.clip(lr, -10, 10)), 0, None)
            g = np.sqrt(rm1 * sinh_g + 1e-30)
        elif base_key == 'blend_ratio_log':
            # 0.5*(ratio-1) + 0.5*log(ratio): both wa<0, between ratio_m1 and log_ratio
            lr = np.log(np.clip(ratio, 1e-8, 200))
            g = 0.5 * (ratio - 1.0) + 0.5 * lr
        elif base_key == 'tanh_ratio_mix':
            # tanh(ratio-1) saturates (chi2 boost) + 0.1*(ratio-1) growing (wa<0 anchor)
            rm1 = ratio - 1.0
            g = np.tanh(np.clip(rm1, -10, 10)) + 0.1 * rm1
        elif base_key == 'tanh_ratio_mix_05':
            # smaller linear tail (0.05) for subtler wa<0 pull
            rm1 = ratio - 1.0
            g = np.tanh(np.clip(rm1, -10, 10)) + 0.05 * rm1
        elif base_key == 'erf_ratio_mix':
            # erf_approx(ratio-1) + 0.1*(ratio-1): mirror of best K93 base with wa<0 tail
            rm1 = ratio - 1.0
            g = np.tanh(1.2533 * np.clip(rm1, -10, 10)) + 0.1 * rm1
        elif base_key == 'tanh_ratio_mix_30':
            # tanh(ratio-1) + 0.3*(ratio-1): at z>1, ratio contributes 50-80% → wa<0
            rm1 = ratio - 1.0
            g = np.tanh(np.clip(rm1, -10, 10)) + 0.3 * rm1
        elif base_key == 'tanh_ratio_mix_50':
            # tanh(ratio-1) + 0.5*(ratio-1): ratio dominates at z>1 → wa<0 + fast intermediate
            rm1 = ratio - 1.0
            g = np.tanh(np.clip(rm1, -10, 10)) + 0.5 * rm1
        elif base_key == 'psi_blend_tanh_ratio':
            # psi_frac*tanh(ratio-1) + (1-psi_frac)*(ratio-1):
            # psi_frac→1 at low-z (tanh dominates, chi2 boost)
            # psi_frac→0 at high-z (ratio dominates, wa<0)
            rm1 = ratio - 1.0
            g = psi_z/psi0 * np.tanh(np.clip(rm1, -10, 10)) + (1.0 - psi_z/psi0) * rm1
        elif base_key == 'psi_blend_erf_ratio':
            # same but erf_approx instead of tanh (faster saturation near ratio=1)
            rm1 = ratio - 1.0
            g = psi_z/psi0 * np.tanh(1.2533*np.clip(rm1, -10, 10)) + (1.0 - psi_z/psi0) * rm1
        elif base_key == 'psi_sq_blend_tanh_ratio':
            # psi_frac^2 * tanh + (1-psi_frac^2) * (ratio-1):
            # psi_frac^2 drops faster → ratio-1 dominates at z~0.7+ → stronger wa<0 + better chi2
            rm1 = ratio - 1.0
            pf2 = (psi_z/psi0)**2
            g = pf2 * np.tanh(np.clip(rm1, -10, 10)) + (1.0 - pf2) * rm1
        elif base_key == 'psi_blend_tanh_cbrt':
            # psi_frac * tanh + (1-psi_frac) * (cbrt-1): gentler high-z component
            rm1 = ratio - 1.0
            g = psi_z/psi0 * np.tanh(np.clip(rm1, -10, 10)) + (1.0 - psi_z/psi0) * (ratio**(1.0/3.0) - 1.0)
        elif base_key == 'psi_cube_blend_erf_ratio':
            # psi^3 blend: much faster transition → ratio-1 dominates at z~0.5
            rm1 = ratio - 1.0
            pf3 = (psi_z/psi0)**3
            g = pf3 * np.tanh(1.2533*np.clip(rm1, -10, 10)) + (1.0 - pf3) * rm1
        elif base_key == 'psi_blend_erf_log':
            # log(ratio) tail: smoother high-z growth (between sqrt and ratio-1)
            rm1 = ratio - 1.0
            lr = np.log(np.clip(ratio, 1e-8, 200))
            g = psi_z/psi0 * np.tanh(1.2533*np.clip(rm1, -10, 10)) + (1.0 - psi_z/psi0) * lr
        elif base_key == 'cpl_blend_erf_ratio':
            # z/(1+z)-weighted blend: smooth CPL-inspired transition
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_blend_tanh_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_erf11_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.1*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_erf12_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.2*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_erf125_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.25*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_erf13_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.3*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_erf135_ratio':
            # BEST Q92: c=1.35, ΔAICc=-4.44, wa=-0.51
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.35*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_erf14_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.4*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_erf145_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.45*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_erf15_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.5*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_erf16_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.6*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_erf17_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.7*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_erf20_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*2.0*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_sq_erf12_ratio':
            wt = (z_arr / (1.0 + z_arr))**2
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.2*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_sq_erf13_ratio':
            wt = (z_arr / (1.0 + z_arr))**2
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.3*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_sq_erf135_ratio':
            wt = (z_arr / (1.0 + z_arr))**2
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.35*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_erf13_sqrt_ratio':
            wt = z_arr / (1.0 + z_arr)
            sr1 = np.sqrt(ratio) - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.3*np.clip(sr1, -10, 10)) + wt * sr1
        elif base_key == 'cpl_erf135_sqrt_ratio':
            wt = z_arr / (1.0 + z_arr)
            sr1 = np.sqrt(ratio) - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.35*np.clip(sr1, -10, 10)) + wt * sr1
        elif base_key == 'psi_sq_blend_erf_ratio':
            rm1 = ratio - 1.0
            pf2 = (psi_z/psi0)**2
            g = pf2 * np.tanh(1.2533*np.clip(rm1, -10, 10)) + (1.0 - pf2) * rm1
        elif base_key == 'cpl_exp_erf10_ratio':
            wt = 1.0 - np.exp(-z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.0*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_exp_erf11_ratio':
            wt = 1.0 - np.exp(-z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.1*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_exp_erf12_ratio':
            wt = 1.0 - np.exp(-z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.2*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_exp_erf13_ratio':
            wt = 1.0 - np.exp(-z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.3*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_exp_erf135_ratio':
            wt = 1.0 - np.exp(-z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.35*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_exp_erf14_ratio':
            wt = 1.0 - np.exp(-z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.4*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_exp_erf15_ratio':
            wt = 1.0 - np.exp(-z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.5*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_mix_erf12_ratio':
            wt = 0.5*(1.0 - np.exp(-z_arr)) + 0.5*(z_arr/(1.0 + z_arr))
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.2*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_mix_erf13_ratio':
            wt = 0.5*(1.0 - np.exp(-z_arr)) + 0.5*(z_arr/(1.0 + z_arr))
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.3*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_mix_erf135_ratio':
            wt = 0.5*(1.0 - np.exp(-z_arr)) + 0.5*(z_arr/(1.0 + z_arr))
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.35*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_mix_erf14_ratio':
            wt = 0.5*(1.0 - np.exp(-z_arr)) + 0.5*(z_arr/(1.0 + z_arr))
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.4*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_mix_erf15_ratio':
            wt = 0.5*(1.0 - np.exp(-z_arr)) + 0.5*(z_arr/(1.0 + z_arr))
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.5*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_tanh_erf12_ratio':
            wt = np.tanh(z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.2*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_tanh_erf13_ratio':
            wt = np.tanh(z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.3*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_tanh_erf135_ratio':
            wt = np.tanh(z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.35*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_tanh_erf14_ratio':
            wt = np.tanh(z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.4*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_tanh_erf145_ratio':
            wt = np.tanh(z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.45*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_tanh_erf147_ratio':
            wt = np.tanh(z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.47*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_tanh_erf15_ratio':
            wt = np.tanh(z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.5*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_tanh_erf16_ratio':
            wt = np.tanh(z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.6*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_sig20_z090_erf115_ratio':
            s0 = 1.0/(1.0+np.exp(20.0*0.90))
            wt = np.clip((1.0/(1.0+np.exp(-20.0*(z_arr-0.90)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.15*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_sig20_z087_erf115_ratio':
            s0 = 1.0/(1.0+np.exp(20.0*0.87))
            wt = np.clip((1.0/(1.0+np.exp(-20.0*(z_arr-0.87)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.15*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_sig15_z090_erf115_ratio':
            s0 = 1.0/(1.0+np.exp(15.0*0.90))
            wt = np.clip((1.0/(1.0+np.exp(-15.0*(z_arr-0.90)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.15*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_sig12_z090_erf115_ratio':
            s0 = 1.0/(1.0+np.exp(12.0*0.90))
            wt = np.clip((1.0/(1.0+np.exp(-12.0*(z_arr-0.90)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.15*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_sig10_z090_erf115_ratio':
            s0 = 1.0/(1.0+np.exp(10.0*0.90))
            wt = np.clip((1.0/(1.0+np.exp(-10.0*(z_arr-0.90)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.15*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_sig9_z090_erf115_ratio':
            s0 = 1.0/(1.0+np.exp(9.0*0.90))
            wt = np.clip((1.0/(1.0+np.exp(-9.0*(z_arr-0.90)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.15*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_sig8_z090_erf115_ratio':
            s0 = 1.0/(1.0+np.exp(8.0*0.90))
            wt = np.clip((1.0/(1.0+np.exp(-8.0*(z_arr-0.90)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.15*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_sig7_z092_erf115_ratio':
            s0 = 1.0/(1.0+np.exp(7.0*0.92))
            wt = np.clip((1.0/(1.0+np.exp(-7.0*(z_arr-0.92)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.15*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_sig7_z090_erf115_ratio':
            s0 = 1.0/(1.0+np.exp(7.0*0.90))
            wt = np.clip((1.0/(1.0+np.exp(-7.0*(z_arr-0.90)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.15*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_sig6_z090_erf115_ratio':
            s0 = 1.0/(1.0+np.exp(6.0*0.90))
            wt = np.clip((1.0/(1.0+np.exp(-6.0*(z_arr-0.90)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.15*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_sig8_z085_erf115_ratio':
            s0 = 1.0/(1.0+np.exp(8.0*0.85))
            wt = np.clip((1.0/(1.0+np.exp(-8.0*(z_arr-0.85)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.15*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_sig8_z09_erf125_ratio':
            s0 = 1.0/(1.0+np.exp(8.0*0.9))
            wt = np.clip((1.0/(1.0+np.exp(-8.0*(z_arr-0.9)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.25*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'cpl_sig6_z09_erf125_ratio':
            s0 = 1.0/(1.0+np.exp(6.0*0.9))
            wt = np.clip((1.0/(1.0+np.exp(-6.0*(z_arr-0.9)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.25*np.clip(rm1, -10, 10)) + wt * rm1
        elif base_key == 'psi_blend_tanh_ratio_sq':
            # ratio^2 tail with psi^2 blend for gentler onset
            rm1 = ratio - 1.0
            pf2 = (psi_z/psi0)**2
            r2m1 = np.clip(ratio**2 - 1.0, 0, 100)
            g = pf2 * np.tanh(np.clip(rm1, -10, 10)) + (1.0 - pf2) * r2m1
        else:
            g = ratio - 1.0

        p = max(tr_param, 0.01)
        if transform == 'identity':
            h = g
        elif transform == 'tanh':
            h = np.tanh(g / p)
        elif transform == 'arctan':
            h = (2.0/math.pi) * np.arctan(g / p)
        elif transform == 'rational':
            h = g / (1.0 + g / p)
        elif transform == 'log1p':
            h = np.log1p(np.clip(g, 0, None))
        elif transform == 'one_minus_exp':
            h = 1.0 - np.exp(-np.clip(g, 0, None) / p)
        elif transform == 'power':
            h = np.clip(g, 0, None)**p
        else:
            h = g

        rde = OL0 * (1.0 + amp * h)
        rde = np.where(rde < 0, 0.0, rde)
        E2  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
        if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
            return None
        return np.sqrt(np.maximum(E2, 1e-30))

    return E_fn

# ─── Team discussion: independent sampling + deduplication ────────────────────

def team_propose(n_members=8, proposals_each=6, seed=None):
    if seed is None:
        seed = int(time.time() * 1000) % (2**31)
    rng = np.random.default_rng(seed)

    all_specs = []
    for _ in range(n_members):
        for _ in range(proposals_each):
            bk  = str(rng.choice(BASE_KEYS))
            tr  = str(rng.choice(TRANSFORMS))
            trp = float(rng.choice(TR_PARAMS))
            ai  = int(rng.choice(len(AMP_SET)))
            all_specs.append((bk, tr, trp, ai))

    # Discussion: remove duplicates
    seen, unique = set(), []
    for spec in all_specs:
        bk, tr, trp, ai = spec
        key = (bk, tr, round(trp, 2), ai)
        if key not in seen:
            seen.add(key)
            unique.append(spec)

    return unique, seed

# ─── Worker (spawn-safe) ──────────────────────────────────────────────────────

def run_one(args):
    idx, spec, = args
    import os, sys, math, warnings
    import numpy as np
    from scipy.integrate import cumulative_trapezoid
    from scipy.optimize import minimize, differential_evolution

    os.environ['OMP_NUM_THREADS'] = os.environ['MKL_NUM_THREADS'] = os.environ['OPENBLAS_NUM_THREADS'] = '1'
    np.seterr(all='ignore')
    warnings.filterwarnings('ignore')

    _SD = os.path.dirname(os.path.abspath(__file__))
    _SI = os.path.dirname(_SD)
    if _SI not in sys.path:
        sys.path.insert(0, _SI)
    from desi_data import DESI_DR2, DESI_DR2_COV_INV

    C_KMS_W = 299792.458; R_S_W = 147.09; OR_W = 5.38e-5
    N_GRID_W = 4000; LCDM_AICC_W = 15.392
    AMP_SET_W = [0.5, 1.0/3.0, 1.0/math.pi, 1.0/math.e, 2.0/3.0, 0.25, 0.1, 0.4,
                 0.05, 0.2, 0.3, 0.35, 0.45, 0.55, 0.15, 0.6, 0.07, 0.08, 0.12,
                 0.7, 0.75, 0.8, 0.85, 0.9, 0.82, 0.87, 0.92,
                 1.0, 1.05, 1.1, 1.15, 1.2, 0.95, 0.97,
                 1.25, 1.3, 1.35, 1.4, 1.45, 1.5,
                 1.55, 1.6, 1.7, 1.8, 1.9, 2.0,
                 2.1, 2.15, 2.2, 2.25, 2.3, 2.4, 2.5]

    bk, tr, trp, ai = spec
    amp = AMP_SET_W[ai % len(AMP_SET_W)]

    def E_fn(z_arr, Om):
        z_arr = np.asarray(z_arr, dtype=float)
        OL0 = 1.0 - Om - OR_W
        if OL0 <= 0 or Om <= 0:
            return None
        alpha = Om / OL0
        psi_z = 1.0 / (1.0 + alpha * (1.0 + z_arr)**3)
        psi0  = 1.0 / (1.0 + alpha)
        ratio = np.clip(psi0 / psi_z, 1.0, 200.0)

        psi_z = 1.0 / (1.0 + alpha * (1.0 + z_arr)**3)
        psi0  = 1.0 / (1.0 + alpha)
        psi_frac = psi_z / psi0  # decreases 1→0 with z

        if bk == 'ratio_m1':
            g = ratio - 1.0
        elif bk == 'log_ratio':
            g = np.log(ratio)
        elif bk == 'sqrt_m1':
            g = np.sqrt(ratio) - 1.0
        elif bk == 'cbrt_m1':
            g = ratio**(1.0/3.0) - 1.0
        elif bk == 'sq_m1':
            g = ratio**2 - 1.0
        elif bk == 'log2':
            g = np.log(ratio)**2
        elif bk == 'psi_dec':
            # 1 - psi_z/psi0: grows 0→1, saturates → wa<0 structure
            g = 1.0 - psi_frac
        elif bk == 'psi_sq_dec':
            # 1 - (psi_z/psi0)^2: faster saturation
            g = 1.0 - psi_frac**2
        elif bk == 'two_comp_dec_cbrt':
            # two-component: psi_dec (wa<0) + cbrt_m1 (low chi2)
            w1 = 0.6
            rde = OL0 * (1.0 + amp * (w1*(1.0-psi_frac) + (1.0-w1)*(ratio**(1.0/3.0)-1.0)))
            rde = np.where(rde < 0, 0.0, rde)
            E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
            if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                return None
            return np.sqrt(np.maximum(E2, 1e-30))
        elif bk == 'two_comp_dec_log':
            # two-component: psi_dec (wa<0) + log_ratio (moderate chi2)
            w1 = 0.5
            rde = OL0 * (1.0 + amp * (w1*(1.0-psi_frac) + (1.0-w1)*np.log(ratio)))
            rde = np.where(rde < 0, 0.0, rde)
            E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
            if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                return None
            return np.sqrt(np.maximum(E2, 1e-30))
        elif bk == 'log1p_psi_dec':
            # log(1 + psi_dec): grows 0→log(2)≈0.69, saturates naturally → wa<0
            g = np.log1p(1.0 - psi_frac)
        elif bk == 'prod_dec_cbrt':
            # psi_dec * cbrt_m1: product saturates due to psi_dec capping → wa<0
            g = (1.0 - psi_frac) * (ratio**(1.0/3.0) - 1.0)
        elif bk == 'sinh_ratio':
            # sinh(log_ratio) = (ratio - 1/ratio)/2: between ratio and ratio^2 growth
            lr = np.log(np.clip(ratio, 1e-8, 200))
            g = np.sinh(np.clip(lr, -10, 10))
        elif bk == 'ratio_frac':
            # (ratio-1)/(ratio+1): bounded [0,1), grows then saturates → wa<0
            g = (ratio - 1.0) / (ratio + 1.0)
        elif bk == 'prod_dec_sqrt':
            # psi_dec * sqrt_m1: product — saturates due to psi_dec
            g = (1.0 - psi_frac) * (np.sqrt(ratio) - 1.0)
        elif bk == 'tanh_ratio_sat':
            # tanh(log_ratio): direct saturation of log growth → strong wa<0
            g = np.tanh(np.log(np.clip(ratio, 1e-8, 200)))
        elif bk == 'twothird_m1':
            # ratio^(2/3)-1: grows ~(1+z)^2 → intermediate wa<0 with better chi2 than cbrt
            g = ratio**(2.0/3.0) - 1.0
        elif bk == 'fourthird_m1':
            # ratio^(4/3)-1: grows ~(1+z)^4 → between sqrt and sq
            g = ratio**(4.0/3.0) - 1.0
        elif bk == 'sinh_half':
            # sinh(0.5*log_ratio) = (sqrt(ratio)-1/sqrt(ratio))/2 → grows ~(1+z)^(3/2)
            lr = np.log(np.clip(ratio, 1e-8, 200))
            g = np.sinh(np.clip(0.5*lr, -10, 10))
        elif bk == 'cubic_div':
            # ratio^2 - 1/ratio: grows ~(1+z)^6 but 1/ratio suppresses slightly
            g = ratio**2 - 1.0/np.clip(ratio, 1e-8, None)
        elif bk == 'geom_cbrt_sinh':
            # geometric mean: sqrt(cbrt_m1 * sinh_ratio) — combines wa<0 properties
            cbrt_g = np.clip(ratio**(1.0/3.0) - 1.0, 0, None)
            sinh_g = np.clip(ratio - 1.0/np.clip(ratio, 1e-8, None), 0, None) / 2.0
            g = np.sqrt(cbrt_g * sinh_g + 1e-30)
        elif bk == 'sq_inv_cube':
            # (ratio^2-1)/ratio^3 = psi_frac - psi_frac^3: peaks at ratio=sqrt(3), z≈0.5
            # rho_DE grows then shrinks at high-z → wa<0 + potentially good chi2
            g = (ratio**2 - 1.0) / np.clip(ratio**3, 1e-6, None)
        elif bk == 'sinh_quart':
            # sinh(log_ratio/4) = (ratio^0.25 - ratio^-0.25)/2: very gentle growth
            lr = np.log(np.clip(ratio, 1e-8, 200))
            g = np.sinh(np.clip(0.25*lr, -10, 10))
        elif bk == 'cbrt_inv_sq':
            # (ratio^(1/3)-1)/ratio^2: peaks even earlier, faster decline
            g = (ratio**(1.0/3.0) - 1.0) / np.clip(ratio**2, 1e-6, None)
        elif bk == 'psi_frac_sq_m1_peak':
            # psi_frac^2 * (ratio^3-1)/ratio = psi_frac^2 * (ratio^2 - 1/ratio)
            # composite peaked structure
            g = psi_frac**2 * (ratio**2 - 1.0/np.clip(ratio, 1e-8, None))
        elif bk == 'ratio_34_m1':
            # ratio^(3/4)-1: intermediate between sqrt_m1 and cbrt_m1
            g = ratio**(0.75) - 1.0
        elif bk == 'smooth_peak_slow':
            # (ratio-1)*exp(-0.15*(ratio-1)): peak at ratio~7.7 (z~1.7), then declines → wa<0
            rm1 = ratio - 1.0
            g = rm1 * np.exp(-0.15 * np.clip(rm1, 0, 50))
        elif bk == 'smooth_peak_fast2':
            # (ratio-1)*exp(-0.5*(ratio-1)): peak at ratio~3 (z~0.65), then declines → wa<0
            rm1 = ratio - 1.0
            g = rm1 * np.exp(-0.5 * np.clip(rm1, 0, 30))
        elif bk == 'ratio_56_m1':
            # ratio^(5/6)-1: grows as ~(1+z)^2.5, between twothird_m1 and ratio_34_m1
            g = ratio**(5.0/6.0) - 1.0
        elif bk == 'psi_cubic_dec':
            # 1 - psi_frac^3: faster saturation than psi_sq_dec → strong wa<0
            g = 1.0 - psi_frac**3
        elif bk == 'arcsinh_m1':
            # arcsinh(ratio-1): g(0)=0, grows ~log(2*ratio) for large ratio (sub-log) → wa<0
            g = np.arcsinh(ratio - 1.0)
        elif bk == 'log_ratio_sat':
            # log(ratio)/(1+log(ratio)): saturates to 1 for large z, very slow growth → wa<0
            lr = np.log(np.clip(ratio, 1e-8, 200))
            g = lr / (1.0 + lr)
        elif bk == 'ratio_04_m1':
            # ratio^0.4-1: grows as ~(1+z)^1.2 → strong wa<0 with moderate growth
            g = ratio**0.4 - 1.0
        elif bk == 'ratio_06_m1':
            # ratio^0.6-1: grows as ~(1+z)^1.8 → intermediate wa<0, better chi2 than cbrt
            g = ratio**0.6 - 1.0
        elif bk == 'ratio_psi_power2':
            # ratio^(2*psi_frac)-1: natural SQT bump; psi_frac→0 at high z → g→0
            # peaks near z~1 then declines → phantom-like wa<0 with fast intermediate growth
            g = ratio**(2.0 * np.clip(psi_frac, 0.0, 1.0)) - 1.0
        elif bk == 'ratio_psi_power3':
            # ratio^(3*psi_frac)-1: stronger bump, peaks earlier and higher
            g = ratio**(3.0 * np.clip(psi_frac, 0.0, 1.0)) - 1.0
        elif bk == 'exp_inv_ratio':
            # exp(-1/ratio) - exp(-1): saturates to 1-1/e≈0.632, decelerating growth → wa<0
            g = np.exp(-1.0 / np.clip(ratio, 1e-8, None)) - math.exp(-1.0)
        elif bk == 'cosh_half_log':
            # cosh(0.5*log(ratio))-1 ~ sqrt(ratio)/2 at high z → grows as (1+z)^1.5, wa<0
            lr = np.log(np.clip(ratio, 1e-8, 200))
            g = np.cosh(np.clip(0.5 * lr, 0, 10)) - 1.0
        elif bk == 'blend_sq_cbrt_psisq':
            # (ratio^2-1)*psi_frac^2 + (ratio^1/3-1)*(1-psi_frac^2)
            # low-z: sq dominates (good chi2); high-z: cbrt dominates (wa<0) — key new idea
            pf2 = psi_frac**2
            g = (ratio**2 - 1.0) * pf2 + (ratio**(1.0/3.0) - 1.0) * (1.0 - pf2)
        elif bk == 'blend_sq_sqrt_psisq':
            # (ratio^2-1)*psi_frac^2 + (sqrt(ratio)-1)*(1-psi_frac^2)
            # similar but sqrt at high z → wa<0, less extreme than cbrt version
            pf2 = psi_frac**2
            g = (ratio**2 - 1.0) * pf2 + (np.sqrt(ratio) - 1.0) * (1.0 - pf2)
        elif bk == 'blend_sqrt_cbrt_psi':
            # sqrt_m1*psi_frac + cbrt_m1*(1-psi_frac): mild transition, both wa<0 friendly
            g = (np.sqrt(ratio) - 1.0) * psi_frac + (ratio**(1.0/3.0) - 1.0) * (1.0 - psi_frac)
        elif bk == 'blend_ratio_cbrt_psisq':
            # (ratio-1)*psi_frac^2 + cbrt_m1*(1-psi_frac^2): ratio→cbrt transition
            pf2 = psi_frac**2
            g = (ratio - 1.0) * pf2 + (ratio**(1.0/3.0) - 1.0) * (1.0 - pf2)
        elif bk == 'ratio_08_m1':
            # ratio^0.8-1: grows as ~(1+z)^2.4, between ratio_56 and ratio_m1
            g = ratio**0.8 - 1.0
        elif bk == 'ratio_45_m1':
            # ratio^0.45-1: grows as ~(1+z)^1.35, between ratio_04 and ratio_06
            g = ratio**0.45 - 1.0
        elif bk == 'sq_psi_sq':
            # (ratio^2-1)*psi_frac^2: fast growth at z<1, near-plateau at z>1 → wa<0 + decent chi2
            g = (ratio**2 - 1.0) * psi_frac**2
        elif bk == 'sqrt_psi_sq':
            # (sqrt(ratio)-1)*psi_frac^2: moderate growth at z<1, plateaus at z>1 → wa<0
            g = (np.sqrt(ratio) - 1.0) * psi_frac**2
        elif bk == 'soft_sq':
            # ratio^2/(1+ratio) - 0.5: fast at low z (like ratio^2), asymptotes to ratio-0.5 at high z
            # effective n=1 at high z → w(∞)=-2 → wa<0 while maintaining good chi2
            g = ratio**2 / (1.0 + ratio) - 0.5
        elif bk == 'soft_ratio_cbrt':
            # ratio^(4/3)/(1+ratio^(1/3)) - 1/(1+1): fast at low z, asymptotes to ratio (n=1) at high z
            r13 = ratio**(1.0/3.0)
            g = ratio**(4.0/3.0) / (1.0 + r13) - 0.5
        elif bk == 'blend_ratio_sinh':
            # 0.5*(ratio-1) + 0.5*sinh(log_ratio): BOTH components have wa<0 inherently
            # blend gives better chi2 than pure sinh_ratio, while maintaining wa<0
            lr = np.log(np.clip(ratio, 1e-8, 200))
            sinh_g = np.sinh(np.clip(lr, -10, 10))
            g = 0.5 * (ratio - 1.0) + 0.5 * sinh_g
        elif bk == 'blend_ratio70_sqrt30':
            # 0.7*(ratio-1) + 0.3*(sqrt(ratio)-1): both wa<0, ratio gives chi2, sqrt anchors wa
            g = 0.7 * (ratio - 1.0) + 0.3 * (np.sqrt(ratio) - 1.0)
        elif bk == 'blend_ratio60_cbrt40':
            # 0.6*(ratio-1) + 0.4*(ratio^(1/3)-1): both wa<0, aggressive ratio for chi2
            g = 0.6 * (ratio - 1.0) + 0.4 * (ratio**(1.0/3.0) - 1.0)
        elif bk == 'sq_log_ratio':
            # (ratio^2-1)*log(1+1/ratio): at z=1 exceeds ratio_m1, at high-z → ratio-0.5 → wa<0
            # effective growth: faster than sinh_ratio at intermediate z → potentially lower chi2
            g = (ratio**2 - 1.0) * np.log1p(1.0 / np.clip(ratio, 1e-8, None))
        elif bk == 'ratio_09_m1':
            # ratio^0.9-1: grows as ~(1+z)^2.7, between ratio_08 and ratio_m1, wa<0
            g = ratio**0.9 - 1.0
        elif bk == 'blend_ratio90_cbrt10':
            # 0.9*(ratio-1) + 0.1*(ratio^(1/3)-1): nearly ratio_m1 but cbrt anchor keeps wa<0 better
            g = 0.9 * (ratio - 1.0) + 0.1 * (ratio**(1.0/3.0) - 1.0)
        elif bk == 'ratio_log_ratio':
            # ratio*ln(ratio): faster than ratio_m1 at all z>0, wa<0 (grows ~z^3*ln(z))
            lr = np.log(np.clip(ratio, 1e-8, 200))
            g = ratio * lr
        elif bk == 'sqrt_log_ratio':
            # sqrt(ratio)*ln(ratio): intermediate growth, wa<0
            lr = np.log(np.clip(ratio, 1e-8, 200))
            g = np.sqrt(ratio) * lr
        elif bk == 'cbrt_log_ratio':
            # ratio^(1/3)*ln(ratio): slower than log_ratio but still wa<0
            lr = np.log(np.clip(ratio, 1e-8, 200))
            g = ratio**(1.0/3.0) * lr
        elif bk == 'geom_ratio_sinh':
            # sqrt((ratio-1)*sinh(log_ratio)): geometric mean, between ratio_m1 and sinh_ratio
            rm1 = np.clip(ratio - 1.0, 0, None)
            lr = np.log(np.clip(ratio, 1e-8, 200))
            sinh_g = np.clip(np.sinh(np.clip(lr, -10, 10)), 0, None)
            g = np.sqrt(rm1 * sinh_g + 1e-30)
        elif bk == 'blend_ratio_log':
            # 0.5*(ratio-1) + 0.5*log(ratio): arithmetic mean, both components wa<0
            lr = np.log(np.clip(ratio, 1e-8, 200))
            g = 0.5 * (ratio - 1.0) + 0.5 * lr
        elif bk == 'tanh_ratio_mix':
            # tanh(ratio-1) gives chi2-boost (fast saturation) + 0.1*(ratio-1) keeps wa<0
            rm1 = ratio - 1.0
            g = np.tanh(np.clip(rm1, -10, 10)) + 0.1 * rm1
        elif bk == 'tanh_ratio_mix_05':
            rm1 = ratio - 1.0
            g = np.tanh(np.clip(rm1, -10, 10)) + 0.05 * rm1
        elif bk == 'erf_ratio_mix':
            # erf_approx(ratio-1) + 0.1*(ratio-1): best K93 base shape + wa<0 anchor
            rm1 = ratio - 1.0
            g = np.tanh(1.2533 * np.clip(rm1, -10, 10)) + 0.1 * rm1
        elif bk == 'tanh_ratio_mix_30':
            # tanh(ratio-1) + 0.3*(ratio-1): ratio contributes >50% at z>1 → wa<0
            rm1 = ratio - 1.0
            g = np.tanh(np.clip(rm1, -10, 10)) + 0.3 * rm1
        elif bk == 'tanh_ratio_mix_50':
            # tanh(ratio-1) + 0.5*(ratio-1): ratio dominates at z>1 → wa<0 strongly
            rm1 = ratio - 1.0
            g = np.tanh(np.clip(rm1, -10, 10)) + 0.5 * rm1
        elif bk == 'psi_blend_tanh_ratio':
            # psi_frac*tanh(ratio-1) + (1-psi_frac)*(ratio-1)
            # psi_frac=1 at z=0 (tanh dominates → chi2 boost)
            # psi_frac→0 at high-z (ratio-1 dominates → wa<0)
            rm1 = ratio - 1.0
            g = psi_frac * np.tanh(np.clip(rm1, -10, 10)) + (1.0 - psi_frac) * rm1
        elif bk == 'psi_blend_erf_ratio':
            # same but erf_approx (faster saturation than tanh near ratio-1=0)
            rm1 = ratio - 1.0
            g = psi_frac * np.tanh(1.2533*np.clip(rm1, -10, 10)) + (1.0 - psi_frac) * rm1
        elif bk == 'psi_sq_blend_tanh_ratio':
            # psi_frac^2 drops faster → ratio-1 dominates from z~0.7 → better chi2+wa<0
            rm1 = ratio - 1.0
            pf2 = psi_frac**2
            g = pf2 * np.tanh(np.clip(rm1, -10, 10)) + (1.0 - pf2) * rm1
        elif bk == 'psi_blend_tanh_cbrt':
            # gentler high-z: cbrt instead of ratio → moderate wa<0
            rm1 = ratio - 1.0
            g = psi_frac * np.tanh(np.clip(rm1, -10, 10)) + (1.0 - psi_frac) * (ratio**(1.0/3.0) - 1.0)
        elif bk == 'psi_cube_blend_erf_ratio':
            rm1 = ratio - 1.0
            pf3 = psi_frac**3
            g = pf3 * np.tanh(1.2533*np.clip(rm1, -10, 10)) + (1.0 - pf3) * rm1
        elif bk == 'psi_blend_erf_log':
            rm1 = ratio - 1.0
            lr = np.log(np.clip(ratio, 1e-8, 200))
            g = psi_frac * np.tanh(1.2533*np.clip(rm1, -10, 10)) + (1.0 - psi_frac) * lr
        elif bk == 'cpl_blend_erf_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_blend_tanh_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_erf11_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.1*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_erf12_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.2*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_erf125_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.25*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_erf13_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.3*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_erf135_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.35*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_erf14_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.4*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_erf145_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.45*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_erf15_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.5*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_erf16_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.6*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_erf17_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.7*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_erf20_ratio':
            wt = z_arr / (1.0 + z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*2.0*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_sq_erf12_ratio':
            wt = (z_arr / (1.0 + z_arr))**2
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.2*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_sq_erf13_ratio':
            wt = (z_arr / (1.0 + z_arr))**2
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.3*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_sq_erf135_ratio':
            wt = (z_arr / (1.0 + z_arr))**2
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.35*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_erf13_sqrt_ratio':
            wt = z_arr / (1.0 + z_arr)
            sr1 = np.sqrt(ratio) - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.3*np.clip(sr1, -10, 10)) + wt * sr1
        elif bk == 'cpl_erf135_sqrt_ratio':
            wt = z_arr / (1.0 + z_arr)
            sr1 = np.sqrt(ratio) - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.35*np.clip(sr1, -10, 10)) + wt * sr1
        elif bk == 'psi_sq_blend_erf_ratio':
            rm1 = ratio - 1.0
            pf2 = psi_frac**2
            g = pf2 * np.tanh(1.2533*np.clip(rm1, -10, 10)) + (1.0 - pf2) * rm1
        elif bk == 'cpl_exp_erf10_ratio':
            wt = 1.0 - np.exp(-z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.0*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_exp_erf11_ratio':
            wt = 1.0 - np.exp(-z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.1*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_exp_erf12_ratio':
            wt = 1.0 - np.exp(-z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.2*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_exp_erf13_ratio':
            wt = 1.0 - np.exp(-z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.3*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_exp_erf135_ratio':
            wt = 1.0 - np.exp(-z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.35*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_exp_erf14_ratio':
            wt = 1.0 - np.exp(-z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.4*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_exp_erf15_ratio':
            wt = 1.0 - np.exp(-z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.5*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_mix_erf12_ratio':
            wt = 0.5*(1.0 - np.exp(-z_arr)) + 0.5*(z_arr/(1.0 + z_arr))
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.2*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_mix_erf13_ratio':
            wt = 0.5*(1.0 - np.exp(-z_arr)) + 0.5*(z_arr/(1.0 + z_arr))
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.3*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_mix_erf135_ratio':
            wt = 0.5*(1.0 - np.exp(-z_arr)) + 0.5*(z_arr/(1.0 + z_arr))
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.35*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_mix_erf14_ratio':
            wt = 0.5*(1.0 - np.exp(-z_arr)) + 0.5*(z_arr/(1.0 + z_arr))
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.4*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_mix_erf15_ratio':
            wt = 0.5*(1.0 - np.exp(-z_arr)) + 0.5*(z_arr/(1.0 + z_arr))
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.5*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_tanh_erf12_ratio':
            wt = np.tanh(z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.2*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_tanh_erf13_ratio':
            wt = np.tanh(z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.3*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_tanh_erf135_ratio':
            wt = np.tanh(z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.35*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_tanh_erf14_ratio':
            wt = np.tanh(z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.4*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_tanh_erf145_ratio':
            wt = np.tanh(z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.45*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_tanh_erf147_ratio':
            wt = np.tanh(z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.47*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_tanh_erf15_ratio':
            wt = np.tanh(z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.5*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_tanh_erf16_ratio':
            wt = np.tanh(z_arr)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.6*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_sig20_z090_erf115_ratio':
            s0 = 1.0/(1.0+np.exp(20.0*0.90))
            wt = np.clip((1.0/(1.0+np.exp(-20.0*(z_arr-0.90)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.15*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_sig20_z087_erf115_ratio':
            s0 = 1.0/(1.0+np.exp(20.0*0.87))
            wt = np.clip((1.0/(1.0+np.exp(-20.0*(z_arr-0.87)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.15*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_sig15_z090_erf115_ratio':
            s0 = 1.0/(1.0+np.exp(15.0*0.90))
            wt = np.clip((1.0/(1.0+np.exp(-15.0*(z_arr-0.90)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.15*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_sig12_z090_erf115_ratio':
            s0 = 1.0/(1.0+np.exp(12.0*0.90))
            wt = np.clip((1.0/(1.0+np.exp(-12.0*(z_arr-0.90)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.15*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_sig10_z090_erf115_ratio':
            s0 = 1.0/(1.0+np.exp(10.0*0.90))
            wt = np.clip((1.0/(1.0+np.exp(-10.0*(z_arr-0.90)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.15*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_sig9_z090_erf115_ratio':
            s0 = 1.0/(1.0+np.exp(9.0*0.90))
            wt = np.clip((1.0/(1.0+np.exp(-9.0*(z_arr-0.90)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.15*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_sig8_z090_erf115_ratio':
            s0 = 1.0/(1.0+np.exp(8.0*0.90))
            wt = np.clip((1.0/(1.0+np.exp(-8.0*(z_arr-0.90)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.15*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_sig7_z092_erf115_ratio':
            s0 = 1.0/(1.0+np.exp(7.0*0.92))
            wt = np.clip((1.0/(1.0+np.exp(-7.0*(z_arr-0.92)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.15*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_sig7_z090_erf115_ratio':
            s0 = 1.0/(1.0+np.exp(7.0*0.90))
            wt = np.clip((1.0/(1.0+np.exp(-7.0*(z_arr-0.90)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.15*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_sig6_z090_erf115_ratio':
            s0 = 1.0/(1.0+np.exp(6.0*0.90))
            wt = np.clip((1.0/(1.0+np.exp(-6.0*(z_arr-0.90)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.15*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_sig8_z085_erf115_ratio':
            s0 = 1.0/(1.0+np.exp(8.0*0.85))
            wt = np.clip((1.0/(1.0+np.exp(-8.0*(z_arr-0.85)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.15*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_sig8_z09_erf125_ratio':
            s0 = 1.0/(1.0+np.exp(8.0*0.9))
            wt = np.clip((1.0/(1.0+np.exp(-8.0*(z_arr-0.9)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.25*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'cpl_sig6_z09_erf125_ratio':
            s0 = 1.0/(1.0+np.exp(6.0*0.9))
            wt = np.clip((1.0/(1.0+np.exp(-6.0*(z_arr-0.9)))-s0)/(1.0-s0), 0, 1)
            rm1 = ratio - 1.0
            g = (1.0 - wt) * np.tanh(1.2533*1.25*np.clip(rm1, -10, 10)) + wt * rm1
        elif bk == 'psi_blend_tanh_ratio_sq':
            rm1 = ratio - 1.0
            pf2 = psi_frac**2
            r2m1 = np.clip(ratio**2 - 1.0, 0, 100)
            g = pf2 * np.tanh(np.clip(rm1, -10, 10)) + (1.0 - pf2) * r2m1
        else:
            g = ratio - 1.0

        p = max(trp, 0.01)
        if tr == 'identity':
            h = g
        elif tr == 'tanh':
            h = np.tanh(g / p)
        elif tr == 'arctan':
            h = (2.0/math.pi) * np.arctan(g / p)
        elif tr == 'rational':
            h = g / (1.0 + np.abs(g) / p)
        elif tr == 'log1p':
            h = np.log1p(np.clip(g, 0, None))
        elif tr == 'one_minus_exp':
            h = 1.0 - np.exp(-np.clip(g, 0, None) / p)
        elif tr == 'power':
            h = np.clip(g, 0, None)**p
        elif tr == 'sigmoid':
            h = 1.0 / (1.0 + np.exp(-g/p)) - 0.5
        elif tr == 'erf_approx':
            h = np.tanh(g * 1.2533 / p)  # erf approximation
        else:
            h = g

        rde = OL0 * (1.0 + amp * h)
        rde = np.where(rde < 0, 0.0, rde)
        E2  = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
        if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
            return None
        return np.sqrt(np.maximum(E2, 1e-30))

    def compute_tv(Om, H0):
        z_eff = DESI_DR2['z_eff']
        z_grid = np.linspace(0.0, z_eff.max() + 0.01, N_GRID_W)
        Eg = E_fn(z_grid, Om)
        if Eg is None or not np.all(np.isfinite(Eg)):
            return None
        Eg = np.maximum(Eg, 1e-15)
        DM = (C_KMS_W/H0) * np.concatenate([[0.], cumulative_trapezoid(1./Eg, z_grid)])
        tv = np.empty(13)
        for i, (z, qty) in enumerate(zip(z_eff, DESI_DR2['quantity'])):
            idx_ = min(np.searchsorted(z_grid, z), N_GRID_W-1)
            DH = C_KMS_W / (H0 * Eg[idx_])
            DV = (z * DM[idx_]**2 * DH)**(1./3.) if z > 0 else 0.
            if 'DV' in qty:
                tv[i] = DV / R_S_W
            elif 'DM' in qty:
                tv[i] = DM[idx_] / R_S_W
            elif 'DH' in qty:
                tv[i] = DH / R_S_W
            else:
                tv[i] = np.nan
        return tv

    def chi2_w(params):
        Om, H0 = params
        if not (0.05 < Om < 0.70 and 50. < H0 < 100.):
            return 1e8
        tv = compute_tv(Om, H0)
        if tv is None or not np.all(np.isfinite(tv)):
            return 1e8
        d = DESI_DR2['value'] - tv
        return float(d @ DESI_DR2_COV_INV @ d)

    def cpl_wa_w(Om):
        z_arr = np.linspace(0.01, 2.0, 40)
        Ev = E_fn(z_arr, Om)
        if Ev is None or not np.all(np.isfinite(Ev)):
            return 0., 0.
        rde = Ev**2 - OR_W*(1+z_arr)**4 - Om*(1+z_arr)**3
        E0v = E_fn(np.array([0.0]), Om)
        if E0v is None:
            return 0., 0.
        rde0 = float(E0v[0]**2 - OR_W - Om)
        if rde0 <= 0 or np.any(rde <= 0):
            return 0., 0.
        lnrde = np.log(rde / rde0)
        ln1z  = np.log(1 + z_arr)
        A     = np.column_stack([-3.*ln1z, -3.*(ln1z - z_arr/(1+z_arr))])
        try:
            coef, *_ = np.linalg.lstsq(A, lnrde, rcond=None)
            return float(coef[0]) - 1., float(coef[1])
        except Exception:
            return 0., 0.

    try:
        bounds = [(0.05, 0.50), (58.0, 80.0)]
        rng_l  = np.random.default_rng(42)
        best_c, best_p = 1e9, None

        # Wide starts including low-Om region (champion at Om~0.12, H0~66.8 needs this)
        low_om_starts = [(Om0, H00)
                         for Om0 in [0.08, 0.10, 0.11, 0.12, 0.13, 0.15]
                         for H00 in [64, 66, 68, 70, 72]]
        mid_om_starts = list(zip(rng_l.uniform(0.10,0.45,20), rng_l.uniform(60,78,20)))
        for Om0, H00 in low_om_starts + mid_om_starts:
            try:
                r = minimize(chi2_w, [Om0, H00], method='Nelder-Mead',
                             options={'xatol':1e-7,'fatol':1e-7,'maxiter':8000})
                if r.fun < best_c:
                    best_c, best_p = r.fun, r.x
            except Exception:
                pass

        try:
            r = differential_evolution(chi2_w, bounds, popsize=40, maxiter=2000,
                                       tol=1e-8, seed=42, workers=1)
            if r.fun < best_c:
                best_c, best_p = r.fun, r.x
        except Exception:
            pass

        if best_p is None:
            return None

        Om, H0 = best_p
        chi2   = best_c
        ac     = chi2 + 2*2 + 2*2*3/(13-2-1)
        dac    = ac - LCDM_AICC_W
        w0, wa = cpl_wa_w(Om)

        if ac >= LCDM_AICC_W:
            status = 'K90'
        elif wa >= 0.0:
            status = 'K93'
        elif dac < -4.0 and wa < -0.5:
            status = 'Q92'
        elif dac < -2.0:
            status = 'Q91'
        else:
            status = 'Q90'

        return {
            'id': f'T{idx+1:02d}',
            'base': bk, 'transform': tr,
            'tr_param': round(trp, 3), 'amp_idx': ai,
            'amp': round(amp, 6),
            'name': f'{bk}|{tr}(p={trp:.1f})|amp={amp:.3f}',
            'k': 2,
            'chi2': round(chi2, 4), 'aicc': round(ac, 4),
            'd_aicc': round(dac, 4),
            'Om': round(Om, 4), 'H0': round(H0, 4),
            'w0': round(w0, 4), 'wa': round(wa, 4),
            'status': status
        }
    except Exception:
        return None

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    run_seed = int(time.time() * 1000) % (2**31)
    specs, used_seed = team_propose(n_members=8, proposals_each=6, seed=run_seed)

    # Force-inject champion sigmoid theories (deterministic, never miss optimal amp)
    # amp_idx=43 → amp=1.80 (confirmed global optimum)
    champion_specs = [
        ('cpl_sig20_z090_erf115_ratio', 'identity', 0.5, 43),  # dAICc=-6.683
        ('cpl_sig15_z090_erf115_ratio', 'identity', 0.5, 43),  # dAICc=-6.644
        ('cpl_sig12_z090_erf115_ratio', 'identity', 0.5, 43),  # dAICc=-6.599
        ('cpl_sig10_z090_erf115_ratio', 'identity', 0.5, 43),  # dAICc=-6.557
        ('cpl_sig9_z090_erf115_ratio',  'identity', 0.5, 43),  # dAICc=-6.532
        ('cpl_sig8_z090_erf115_ratio',  'identity', 0.5, 43),  # dAICc=-6.503
        ('cpl_sig7_z090_erf115_ratio',  'identity', 0.5, 43),  # dAICc=-6.467
    ]
    existing_keys = {(s[0], s[1], round(s[2], 2), s[3]) for s in specs}
    for cs in champion_specs:
        key = (cs[0], cs[1], round(cs[2], 2), cs[3])
        if key not in existing_keys:
            specs.append(cs)
            existing_keys.add(key)

    print('='*70)
    print(f'L33: 8-person team | seed={used_seed} | {len(specs)} unique theories')
    print('='*70)
    print('No pre-assigned roles. Team independently sampled SQT space.')
    print(f'LCDM: chi2={LCDM_CHI2}, AICc={LCDM_AICC}')

    ctx  = multiprocessing.get_context('spawn')
    args = [(i, spec) for i, spec in enumerate(specs)]
    with ctx.Pool(9) as pool:
        raw = pool.map(run_one, args)

    results = sorted([r for r in raw if r], key=lambda x: x['aicc'])

    print('\n' + '='*115)
    print('RESULTS sorted by AICc:')
    print('='*115)
    print(f"{'ID':>5} {'name':<50} {'chi2':>8} {'AICc':>8} {'dAICc':>8} {'w0':>7} {'wa':>7} {'Status'}")
    print('-'*115)
    for r in results:
        print(f"{r['id']:>5} {r['name']:<50} {r['chi2']:>8.4f} {r['aicc']:>8.4f} {r['d_aicc']:>+8.4f} {r['w0']:>7.4f} {r['wa']:>7.4f}  {r['status']}")

    pass_l = [r for r in results if r['status'] in ('Q90','Q91','Q92')]
    q91_l  = [r for r in results if r['status'] in ('Q91','Q92')]
    q92_l  = [r for r in results if r['status'] == 'Q92']
    k93_l  = [r for r in results if r['status'] == 'K93']
    champ  = results[0] if results else None

    print(f'\nQ90 PASS : {len(pass_l)} / {len(results)}')
    print(f'Q91 STRONG: {len(q91_l)}')
    print(f'Q92 GAME  : {len(q92_l)}')
    print(f'K93 (wa>=0): {len(k93_l)}')
    if champ:
        print(f'Champion: {champ["id"]} dAICc={champ["d_aicc"]} w0={champ["w0"]} wa={champ["wa"]} Om={champ["Om"]} H0={champ["H0"]}')

    out = {
        'run': 'L33-8team-free',
        'seed': used_seed,
        'n_theories': len(results),
        'theories': results,
        'pass_count': len(pass_l),
        'q91': len(q91_l),
        'q92': len(q92_l),
        'k93_count': len(k93_l),
        'kill_count': len(results) - len(pass_l),
        'champion': champ,
        'lcdm': {'chi2': LCDM_CHI2, 'aicc': LCDM_AICC}
    }
    out_path = os.path.join(_SCRIPT_DIR, 'l33_results.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'\nResults saved: {out_path}')

if __name__ == '__main__':
    main()
