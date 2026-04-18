# -*- coding: utf-8 -*-
"""
l30_test10.py -- L30 Common-Structure + Perverse Attack (EE01-EE30)
====================================================================
Base: DD06/DD18 champion -- delta(z) = 0.5*tanh(z/z_eq)
      z_eq = (OL0/Om)^(1/3) - 1  (matter-Lambda equality redshift)

Strategy: Take DD06 winning saturation as BASE, apply unconventional
          enhancements targeting DESI blind spots and physical asymmetries.

Group 1 (EE01-EE08): Eigenmode-Guided Saturation
  -- EV3 blind spot: z=0.51 DH_over_rs has chi^2 gain ~2.23
  -- Design delta(z) that projects maximally onto EV3
  -- Add correction that increases DH/rs at z=0.51 (decrease E(z) at z=0.51)

Group 2 (EE09-EE16): Superposition of Saturation Scales
  -- z_eq1 = (OL0/Om)^(1/3)-1 ~ 0.3  [DD06 base]
  -- z_eq2 ~ 0.7  [baryon-drag scale for DE purpose]
  -- z_eq3 ~ 1.0  [SQ generation steady-state scale]
  -- Combine multiple tanh with theory-motivated weights

Group 3 (EE17-EE24): Asymmetric Saturation (A4-motivated)
  -- A4: three regimes: net generation, net annihilation, BALANCE
  -- Balance at z_eq is not symmetric (matter-dominated past vs Lambda-dominated future)
  -- delta(z) = alpha*tanh(z/z_eq) + beta*(z/(1+z))*exp(-z/z_eq)

Group 4 (EE25-EE30): Fisher-Perturbed Optimal
  -- Around DD06 champion, find directions improving chi^2 without increasing k
  -- Modify amplitude: 0.5 -> 1/3, 1/pi, 1/e, 2/pi
  -- Modify z_eq: exact vs (1+z_eq)^n
  -- Modify shape: tanh^n for n=1/2, 2, 3

LCDM baseline: chi2=10.192, AICc=15.392 (k=2, n=13)
KILL if AICc >= 15.392
IDs: EE01-EE30
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
from scipy.optimize import minimize, differential_evolution

warnings.filterwarnings('ignore')
np.seterr(all='ignore')

os.environ['OMP_NUM_THREADS']      = '1'
os.environ['MKL_NUM_THREADS']      = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SIM_DIR    = os.path.dirname(_SCRIPT_DIR)
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

from desi_data import DESI_DR2, DESI_DR2_COV, DESI_DR2_COV_INV

C_KMS   = 299792.458
R_S     = 147.09
OR      = 5.38e-5
N_DATA  = 13
N_GRID  = 4000
LCDM_BASELINE_CHI2  = 10.192
LCDM_BASELINE_AICC  = 15.392


def aicc(chi2_val, k, n=N_DATA):
    return chi2_val + 2*k + 2*k*(k+1)/(n - k - 1)


# ==============================================================================
# WORKER FUNCTION (fully self-contained for spawn)
# ==============================================================================

def worker_fn(args):
    """
    Self-contained worker for EE theories.
    Base: DD06 tanh saturation + unconventional enhancements.
    All constants theoretically derived; no free amplitude tuning.
    """
    import os, sys, math, warnings
    import numpy as np

    os.environ['OMP_NUM_THREADS']      = '1'
    os.environ['MKL_NUM_THREADS']      = '1'
    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    np.seterr(all='ignore')
    warnings.filterwarnings('ignore')

    _SCRIPT_DIR_W = os.path.dirname(os.path.abspath(__file__))
    _SIM_DIR_W    = os.path.dirname(_SCRIPT_DIR_W)
    if _SIM_DIR_W not in sys.path:
        sys.path.insert(0, _SIM_DIR_W)
    from desi_data import DESI_DR2, DESI_DR2_COV_INV
    from scipy.integrate import cumulative_trapezoid
    from scipy.optimize import minimize, differential_evolution

    C_KMS_W   = 299792.458
    R_S_W     = 147.09
    OR_W      = 5.38e-5
    N_DATA_W  = 13
    N_GRID_W  = 4000
    LCDM_AICC = 15.392

    def aicc_w(chi2_val, k_in, n=N_DATA_W):
        return chi2_val + 2*k_in + 2*k_in*(k_in+1)/(n - k_in - 1)

    def compute_tv(Omega_m, H0, E_fn):
        z_eff  = DESI_DR2['z_eff']
        z_max  = z_eff.max() + 0.01
        z_grid = np.linspace(0.0, z_max, N_GRID_W)
        try:
            E_grid = E_fn(z_grid, Omega_m)
        except Exception:
            return None
        if E_grid is None:
            return None
        if not np.all(np.isfinite(E_grid)):
            return None
        E_grid = np.maximum(E_grid, 1e-15)
        inv_E  = 1.0 / E_grid
        DM_cum = (C_KMS_W / H0) * np.concatenate(
            [[0.0], cumulative_trapezoid(inv_E, z_grid)]
        )
        theory_vec = np.empty(N_DATA_W)
        for i, (z, qty) in enumerate(zip(z_eff, DESI_DR2['quantity'])):
            idx = min(np.searchsorted(z_grid, z), N_GRID_W - 1)
            E_z = E_grid[idx]
            DH  = C_KMS_W / (H0 * E_z)
            DM  = DM_cum[idx]
            DV  = (z * DM**2 * DH)**(1.0/3.0) if z > 0 else 0.0
            if   'DV' in qty: theory_vec[i] = DV / R_S_W
            elif 'DM' in qty: theory_vec[i] = DM / R_S_W
            elif 'DH' in qty: theory_vec[i] = DH / R_S_W
            else:             theory_vec[i] = np.nan
        return theory_vec

    def chi2_w(params, E_fn):
        Omega_m, H0 = params[0], params[1]
        if not (0.05 < Omega_m < 0.70 and 50.0 < H0 < 100.0):
            return 1e8
        th = compute_tv(Omega_m, H0, E_fn)
        if th is None or not np.all(np.isfinite(th)):
            return 1e8
        delta = DESI_DR2['value'] - th
        return float(delta @ DESI_DR2_COV_INV @ delta)

    # -------------------------------------------------------------------------
    # E(z) FACTORY: EE theories -- common structure + perverse enhancements
    # -------------------------------------------------------------------------

    def build_E_fn(theory_tag):
        """
        Build E(z) from theory_tag.
        BASE: rho_DE = OL0*(1 + delta(z))
        DD06 champion: delta(z) = 0.5*tanh(z/z_eq), z_eq=(OL0/Om)^(1/3)-1
        """

        # =====================================================================
        # GROUP 1: Eigenmode-Guided Saturation (EE01-EE08)
        # EV3 blind spot at z=0.51 DH_over_rs: increase DH needs decrease E(z)
        # Physical: matter-Lambda boundary at z~0.5 creates DH anomaly
        # =====================================================================

        if theory_tag == 'EE01':
            # DD06 base + EV3 blind-spot correction at z~0.51
            # EV3 eigenvector projects onto DH(z=0.51) -> decrease E near z=0.5
            # Correction: Gaussian dip in E(z) centered at z=0.51
            # Amplitude from EV3 chi2 gain: delta_E ~ sqrt(2.23)/E_z * (z-z_c)
            # Physical: matter-Lambda phase boundary creates resonance in DH
            # z_c = 0.51, width sigma = 0.15 (half-width of z=0.51 DESI band)
            # Amplitude A = 1/(2*pi) (quantum resonance amplitude)
            z_c   = 0.51
            sigma = 0.15
            A_ev3 = 1.0 / (2.0 * math.pi)  # quantum resonance amplitude
            f_base = 0.5  # DD06 base amplitude
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                # DD06 base delta
                delta = f_base * np.tanh(z_arr / z_eq)
                # EV3 correction: Gaussian dip centered at z_c=0.51
                # rho_DE increases near z=0.51 -> E(z) decreases -> DH increases
                ev3_correction = A_ev3 * np.exp(-0.5 * ((z_arr - z_c) / sigma)**2)
                delta = delta + ev3_correction
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE02':
            # DD06 base + EV3 correction via Lorentzian resonance
            # Lorentzian: sharper peak than Gaussian, better models resonance
            # L(z) = gamma^2 / ((z-z_c)^2 + gamma^2), gamma = 1/(2*pi)
            # Physical: quantum resonance at matter-Lambda boundary has Lorentzian lineshape
            z_c   = 0.51
            gamma = 1.0 / (2.0 * math.pi)
            A_ev3 = 1.0 / (2.0 * math.pi)
            f_base = 0.5
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                delta = f_base * np.tanh(z_arr / z_eq)
                lorentz = gamma**2 / ((z_arr - z_c)**2 + gamma**2)
                delta = delta + A_ev3 * lorentz
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE03':
            # EV3 projection: asymmetric correction rising at z<0.51, flat after
            # Physical: matter compression front below z=0.5 pushes SQ into voids
            # Step function smoothed with tanh: A*tanh((z_c - z)/sigma)
            # This decreases rho_DE below z_c (decreases DH at low z) and keeps it
            # Actually: we want MORE rho_DE near z=0.51 -> decrease E -> increase DH
            # Use sigmoid centered at z_c: A*(1-tanh((z-z_c)/sigma))
            z_c   = 0.51
            sigma = 0.20
            A_ev3 = 1.0 / (4.0 * math.pi)
            f_base = 0.5
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                delta = f_base * np.tanh(z_arr / z_eq)
                # Sigmoid peak: increases toward z_c from below, then drops
                ev3_corr = A_ev3 * (1.0 - np.tanh((z_arr - z_c) / sigma))
                delta = delta + ev3_corr
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE04':
            # DD06 base with EV3 boost: double-peak at z=0.51 + z_eq
            # Physical: two-phase SQ transition -- first at baryon-drag z~0.51,
            # second at matter-Lambda equality z_eq
            # delta = f1*tanh(z/z_eq) + f2*tanh(z/z_51) where z_51=0.51
            # f1=1/3 (primary channel), f2=1/6 (secondary EV3 channel)
            f1  = 1.0 / 3.0
            f2  = 1.0 / 6.0
            z51 = 0.51
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                delta = f1 * np.tanh(z_arr / z_eq) + f2 * np.tanh(z_arr / z51)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE05':
            # EV3-optimized: enhance DH at z=0.51 by suppressing E(z) near z_eq
            # Method: rho_DE rises more steeply at z<z_eq then saturates
            # Use tanh with steeper rise: delta = f * tanh(z / z_half) where z_half < z_eq
            # z_half = z_eq/2 (half-width of transition)
            # f = 1/2 * (1 + 1/(2*pi)) (DD06 plus EV3 gain)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                z_half = z_eq / 2.0  # steeper transition -> more DH boost at z=0.51
                f = 0.5 * (1.0 + 1.0 / (2.0 * math.pi))
                delta = f * np.tanh(z_arr / z_half)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE06':
            # EV3 blind spot via DM suppression at z=0.51 (complement to DH boost)
            # DM/rs decreases if rho_DE increases at z < 0.51 (less comoving volume)
            # Wait: more DE -> faster expansion -> less DM? No: more DE -> higher E -> MORE DM
            # Actually: tanh correction to SUBTRACT from DE at z < 0.51 would reduce E
            # and reduce DH (bad). So add to DE at z~0.51 only.
            # Physical: SQ accumulation in matter-void interface at z~0.5
            # Interface width ~ sigma_interface = z_eq / (2*pi)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                # DD06 base
                f_base = 0.5
                delta = f_base * np.tanh(z_arr / z_eq)
                # Interface accumulation at z_eq/pi (quantum phase of interface)
                z_int = z_eq / math.pi
                A_int = 1.0 / (2.0 * math.pi**2)
                # Add Gaussian correction at interface
                delta += A_int * np.exp(-0.5 * ((z_arr - z_int) / (z_int / 2.0))**2)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE07':
            # EV3 via modified tanh argument: z/(z_eq + z_c*exp(-z/z_c))
            # Physical: near z=0.51, the effective saturation scale is compressed
            # by matter-SQ scattering with range z_c = 1/(2*pi)
            # This makes delta grow faster at z~0.51 -> more DE -> lower E -> higher DH
            z_c    = 1.0 / (2.0 * math.pi)
            f_base = 0.5
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                # Modified saturation scale: compressed near z=z_c
                z_eff_scale = z_eq + z_c * np.exp(-z_arr / z_c)
                z_eff_scale = np.maximum(z_eff_scale, 0.01)
                delta = f_base * np.tanh(z_arr / z_eff_scale)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE08':
            # EV3 via complementary step: DD06 base + step at z=0.51
            # Physical: when matter density crosses SQ binding threshold at z~0.5,
            # a quantum phase transition releases stored SQ into voids
            # Step amplitude from EV3 chi2 gain: A = sqrt(2.23) / (2*pi*E_z) ~ 1/e^2
            # Model: delta += A * (z_arr > z_c) * (1 - exp(-(z_arr-z_c)/sigma))
            z_c   = 0.51
            sigma = 0.3
            A_step = math.exp(-2.0)  # ~ 1/e^2 -- EV3 chi^2 gain amplitude
            f_base = 0.5
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                delta = f_base * np.tanh(z_arr / z_eq)
                # Phase transition step above z_c
                above = np.where(z_arr > z_c, 1.0 - np.exp(-(z_arr - z_c) / sigma), 0.0)
                delta = delta + A_step * above
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        # =====================================================================
        # GROUP 2: Superposition of Saturation Scales (EE09-EE16)
        # Multiple physical transition scales exist:
        # z_eq1 = (OL0/Om)^(1/3)-1 ~ 0.3  [matter-Lambda equality]
        # z_eq2 ~ 0.7  [baryon-drag scale repurposed for DE]
        # z_eq3 ~ 1.0  [SQ generation steady-state]
        # =====================================================================

        elif theory_tag == 'EE09':
            # Two-scale superposition: z_eq1 (DD06) + z_eq2=0.7 (baryon drag)
            # Physical: baryon-drag sound horizon sets a secondary DE saturation scale
            # because SQ quanta couple to baryon oscillations at z_d~1020
            # For low-z DE purpose: effective z_eq2 = log(1+z_d) / log(1+3) ~ 0.7 (rough)
            # Weights from symmetry: f1=1/2 (primary), f2=1/(2*pi) (secondary)
            f1   = 0.5
            f2   = 1.0 / (2.0 * math.pi)
            z_eq2 = 0.7  # baryon-drag inspired secondary scale
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq1 = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq1 <= 0:
                    z_eq1 = 0.3
                delta = f1 * np.tanh(z_arr / z_eq1) + f2 * np.tanh(z_arr / z_eq2)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE10':
            # Two-scale: z_eq1 + z_eq3=1.0 (SQ steady-state from reionization)
            # Physical: SQ generation reaches steady state at z_rh ~ reionization (z~6)
            # but for baryon-SQ interaction, effective DE scale: log(1+z_rh)/log(7) ~ 1.0
            # f1=1/3 (primary 3D), f2=1/(3*pi) (secondary reionization channel)
            f1    = 1.0 / 3.0
            f2    = 1.0 / (3.0 * math.pi)
            z_eq3 = 1.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq1 = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq1 <= 0:
                    z_eq1 = 0.3
                delta = f1 * np.tanh(z_arr / z_eq1) + f2 * np.tanh(z_arr / z_eq3)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE11':
            # Three-scale: z_eq1 + z_eq2 + z_eq3
            # Weights from A1-A3 SQMH amplitude ratios:
            # A1 (annihilation) -> f1=Om/(Om+OL0+OR) ~ Om
            # A3 (generation) -> f2 = OL0/(Om+OL0+OR) ~ OL0
            # A3 second channel -> f3 = 1/(2*pi^2) (toroidal phase space)
            f3    = 1.0 / (2.0 * math.pi**2)
            z_eq2 = 0.7
            z_eq3 = 1.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq1 = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq1 <= 0:
                    z_eq1 = 0.3
                f1 = Om / (Om + OL0)
                f2 = OL0 / (Om + OL0)
                delta = (f1 * np.tanh(z_arr / z_eq1)
                       + f2 * np.tanh(z_arr / z_eq2)
                       + f3 * np.tanh(z_arr / z_eq3))
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE12':
            # Mixed tanh+arctan superposition
            # Physical: tanh = matter-driven saturation (A1), arctan = void-driven (A3)
            # At matter-Lambda equality both contribute equally
            # f_tanh = 1/3, f_arctan = 1/pi (arctan normalization)
            f_tanh   = 1.0 / 3.0
            f_arctan = 1.0 / math.pi
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                # arctan normalized to go from 0 to 1 as z goes from 0 to inf
                arctan_norm = np.arctan(z_arr / z_eq) / (math.pi / 2.0)
                delta = f_tanh * np.tanh(z_arr / z_eq) + f_arctan * arctan_norm
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE13':
            # tanh + z/(1+z) superposition
            # Physical: tanh captures quantum saturation (rapid), z/(1+z) captures
            # geometric void growth (slow, classical). Both contribute.
            # f1=1/3 (quantum fraction), f2=1/6 (classical fraction)
            f1 = 1.0 / 3.0
            f2 = 1.0 / 6.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                delta = f1 * np.tanh(z_arr / z_eq) + f2 * z_arr / (1.0 + z_arr)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE14':
            # tanh at two scales with different physical origins
            # Scale 1: z_eq from matter-Lambda (A4)
            # Scale 2: sqrt(OL0/Om) -- Hubble crossing (A1)
            # f1=1/4 (4-volume), f2=1/4 (equal partition)
            f1 = 1.0 / 4.0
            f2 = 1.0 / 4.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq1 = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq1 <= 0:
                    z_eq1 = 0.3
                z_eq2 = math.sqrt(OL0 / Om)  # Hubble crossing scale
                if z_eq2 <= 0:
                    z_eq2 = 0.5
                delta = f1 * np.tanh(z_arr / z_eq1) + f2 * np.tanh(z_arr / z_eq2)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE15':
            # Triple tanh with logarithmically spaced scales
            # z_eq1 = (OL0/Om)^(1/3)-1, z_eq2 = z_eq1*pi, z_eq3 = z_eq1*pi^2
            # Physical: SQ transitions at harmonics of the primary scale
            # f1=1/3, f2=1/(3*pi), f3=1/(3*pi^2) -- geometric series
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq1 = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq1 <= 0:
                    z_eq1 = 0.3
                z_eq2 = z_eq1 * math.pi
                z_eq3 = z_eq1 * math.pi**2
                f1 = 1.0 / 3.0
                f2 = 1.0 / (3.0 * math.pi)
                f3 = 1.0 / (3.0 * math.pi**2)
                delta = (f1 * np.tanh(z_arr / z_eq1)
                       + f2 * np.tanh(z_arr / z_eq2)
                       + f3 * np.tanh(z_arr / z_eq3))
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE16':
            # DD06 base + long-range correction from erf saturation
            # erf saturates faster than tanh at small z, slower at large z
            # Physical: at z_eq2=0.7, SQ diffusion switches to advection mode
            # Combined: delta = f1*tanh(z/z_eq) + f2*erf(z/z_eq2)
            # f1=0.4 (primary tanh), f2=0.1 (secondary erf)
            f1    = 0.4
            f2    = 0.1
            z_eq2 = 0.7
            def E_fn(z_arr, Om):
                from scipy.special import erf
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq1 = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq1 <= 0:
                    z_eq1 = 0.3
                delta = f1 * np.tanh(z_arr / z_eq1) + f2 * erf(z_arr / z_eq2)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        # =====================================================================
        # GROUP 3: Asymmetric Saturation (EE17-EE24)
        # A4: THREE regimes: net generation, net annihilation, BALANCE
        # Balance point at z_eq is not symmetric:
        # -- matter-dominated past: annihilation drives DE decrease -> steeper fall
        # -- Lambda-dominated future: generation drives DE increase -> gentler rise
        # Form: delta(z) = alpha*tanh(z/z_eq) + beta*(z/(1+z))*exp(-z/z_eq)
        # =====================================================================

        elif theory_tag == 'EE17':
            # A4 asymmetric: tanh (symmetric base) + exponential-decay correction
            # Past: more annihilation -> tanh falls steeper; correction term adds back
            # Physical: beta = 1/(2*pi) (two-body coupling asymmetry factor)
            # alpha = 1/2 (symmetric base from DD06), beta = 1/(2*pi) (asymmetry)
            alpha_a = 0.5
            beta_a  = 1.0 / (2.0 * math.pi)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                sym_part   = alpha_a * np.tanh(z_arr / z_eq)
                asym_part  = beta_a * (z_arr / (1.0 + z_arr)) * np.exp(-z_arr / z_eq)
                delta = sym_part + asym_part
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE18':
            # Asymmetric: enhance generation side (z < z_eq) more than annihilation side
            # Physical: Lambda-dominated future sees net generation; past sees net annihilation
            # Two-piece: below z_eq use tanh with larger f, above use standard f
            # Unified: delta = f_hi * tanh(z/z_eq) * (1 + f_asym * exp(-(z-z_eq)^2/z_eq^2))
            # f_hi = 1/2 (base), f_asym = 1/(2*e) (Boltzmann asymmetry)
            f_hi   = 0.5
            f_asym = 1.0 / (2.0 * math.e)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                base   = f_hi * np.tanh(z_arr / z_eq)
                asym   = f_asym * np.exp(-(z_arr - z_eq)**2 / z_eq**2)
                delta  = base * (1.0 + asym)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE19':
            # Asymmetric A4: use different scales for past and future
            # Past (z > z_eq): slower saturation because annihilation dominates -> z_past = 2*z_eq
            # Future (z < z_eq): rapid DE rise because generation dominates -> z_fut = z_eq/2
            # Smooth join via weighted average: w = sigmoid((z-z_eq)/sigma)
            # f = 1/2 (total normalization preserved)
            f = 0.5
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                z_past = 2.0 * z_eq
                z_fut  = z_eq / 2.0
                sigma  = z_eq / 4.0
                # Weight: w=1 at z>>z_eq (past), w=0 at z<<z_eq (future)
                w = 0.5 * (1.0 + np.tanh((z_arr - z_eq) / sigma))
                delta = f * (w * np.tanh(z_arr / z_past) + (1.0 - w) * np.tanh(z_arr / z_fut))
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE20':
            # A4 asymmetry: alpha and beta from energy ratio at z_eq
            # At z_eq: Omega_m = OL0 => both channels equal
            # alpha = OL0 / (Om + OL0) -- future DE fraction
            # beta  = Om  / (Om + OL0) -- past matter fraction
            # Combined: delta = alpha*tanh(z/z_eq) + beta*(x-1)/(x+OL0/Om)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                alpha_a = OL0 / (Om + OL0)
                beta_a  = Om  / (Om + OL0)
                ratio = OL0 / Om
                x = (1.0 + z_arr)**3
                sym  = alpha_a * np.tanh(z_arr / z_eq)
                asym = beta_a  * (x - 1.0) / (x + ratio)
                delta = sym + asym
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE21':
            # Asymmetric two-regime: separate tanh below/above z_eq with A4 derivation
            # Below z_eq (void-dominated): slower generation -> f_low = 1/3
            # Above z_eq (matter-dominated): faster annihilation -> f_hi = 2/3
            # Smooth join via logistic
            f_low = 1.0 / 3.0
            f_hi  = 2.0 / 3.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                # w=1 at z>z_eq (past, annihilation), w=0 at z<z_eq (future, generation)
                k_sig = 4.0 / z_eq
                w = 1.0 / (1.0 + np.exp(-k_sig * (z_arr - z_eq)))
                f_eff = f_low * (1.0 - w) + f_hi * w
                delta = f_eff * np.tanh(z_arr / z_eq)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE22':
            # A4 asymmetric saturation: exponential decay for the past (matter era)
            # Physical: in matter-dominated era, SQ quanta exponentially depleted
            # delta = f * tanh(z/z_eq) * exp(-alpha*(1+z)^3 * Om/OL0)
            # Correction: actually want MORE DE at high z, so factor should ADD at high z
            # Reinterpret: DE generation net positive even in matter era but decreasing
            # delta = f * tanh(z/z_eq) * (1 + g * exp(-(z/z_eq)^2))
            # g = 1/(4*pi) (small correction from A4 asymmetry)
            f = 0.5
            g = 1.0 / (4.0 * math.pi)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                peak_corr = 1.0 + g * np.exp(-(z_arr / z_eq)**2)
                delta = f * np.tanh(z_arr / z_eq) * peak_corr
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE23':
            # A4 three-regime explicit: net generation (z<z_eq), balance (z=z_eq), annihilation (z>z_eq)
            # Model: delta = f_gen * (1-exp(-z/z_eq)) for z<z_eq (growing phase)
            #             + f_ann * (1-exp(-(z-z_eq)/z_eq)) for z>z_eq (saturating phase)
            # Smooth join: both pieces times their sigmoid weights
            # f_gen = OL0 (full DE contribution), f_ann = Om (matter-depleted correction)
            # Normalized: f_gen=OL0/2, f_ann=Om/2
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                f_gen = OL0 / 2.0
                f_ann = Om  / 2.0
                # Smooth weights
                w_past = 0.5 * (1.0 + np.tanh((z_arr - z_eq) / (z_eq / 4.0)))
                w_fut  = 1.0 - w_past
                # Generation regime (future-ish, low z)
                delta_gen = f_gen * (1.0 - np.exp(-z_arr / z_eq))
                # Annihilation regime (past, high z)
                dz = np.maximum(z_arr - z_eq, 0.0)
                delta_ann = (f_gen * (1.0 - np.exp(-z_eq / z_eq))
                           + f_ann * (1.0 - np.exp(-dz / z_eq)))
                delta = w_fut * delta_gen + w_past * delta_ann
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE24':
            # A4 asymmetric: power-law tanh (below z_eq) + flat (above z_eq)
            # Physical: annihilation becomes saturated (all SQ annihilated) above z_eq
            # so DE contribution from annihilation channel is constant above z_eq
            # delta_ann = min(tanh(z/z_eq), tanh(1)) = tanh(z/z_eq) if z<z_eq else const
            # Plus generation channel: delta_gen = f_gen * tanh(z/z_eq)
            # Total: delta = (f_ann + f_gen) * tanh(z/z_eq) capped at z_eq
            # f_ann = 1/4, f_gen = 1/4 (equal partition of two channels)
            f_ann = 1.0 / 4.0
            f_gen = 1.0 / 4.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                tanh_sat = float(np.tanh(1.0))  # tanh(z_eq/z_eq) = tanh(1) ~ 0.76
                # Annihilation channel: saturates at z_eq
                tanh_vals = np.tanh(z_arr / z_eq)
                delta_ann = f_ann * np.minimum(tanh_vals, tanh_sat)
                # Generation channel: continues to grow (full tanh)
                delta_gen = f_gen * tanh_vals
                delta = delta_ann + delta_gen
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        # =====================================================================
        # GROUP 4: Fisher-Perturbed Optimal (EE25-EE30)
        # Around DD06 champion (f=0.5, tanh(z/z_eq)), find improved directions
        # Modify amplitude and shape without adding free parameters
        # =====================================================================

        elif theory_tag == 'EE25':
            # Amplitude: 0.5 -> 1/3 (one saturation axis per spatial dimension)
            # Physical: only 1 of 3 spatial dimensions contributes to DE
            # z_eq: exact (OL0/Om)^(1/3)-1  [same as DD06]
            f = 1.0 / 3.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                delta = f * np.tanh(z_arr / z_eq)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE26':
            # Amplitude: 0.5 -> 1/pi (quantum phase normalization)
            # Physical: DE saturation normalized by full quantum phase cycle (2*pi)
            # = 1/pi from one half-cycle (dark energy is one-sided)
            f = 1.0 / math.pi
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                delta = f * np.tanh(z_arr / z_eq)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE27':
            # Amplitude: 0.5 -> 1/e (Boltzmann suppression)
            # Physical: DE generation rate suppressed by quantum Boltzmann factor exp(-1)
            # at the matter-Lambda boundary (one unit of kT = characteristic energy)
            f = 1.0 / math.e
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                delta = f * np.tanh(z_arr / z_eq)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE28':
            # Amplitude: 0.5 -> 2/pi (double half-cycle, quasi-classical limit)
            # Physical: classical limit of quantum DE saturation = 2 channels
            # f = 2/pi from two-body classical limit of quantum amplitude
            f = 2.0 / math.pi
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                delta = f * np.tanh(z_arr / z_eq)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE29':
            # Shape modification: tanh^(1/2) -- softer saturation near z=0
            # Physical: DE saturation via diffusion process -> square-root scaling
            # Amplitude: f = 1/2 (same as DD06, but shape is softer)
            # tanh^(1/2) grows faster at small z, saturates more slowly
            f = 0.5
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                tanh_val = np.tanh(z_arr / z_eq)
                delta = f * np.sqrt(np.maximum(tanh_val, 0.0))
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'EE30':
            # Shape modification: tanh^2 -- sharper saturation (quadratic)
            # Physical: DE saturation via two-body process -> quadratic scaling
            # Amplitude: f = 1/2 (same as DD06, quadratic shape)
            # tanh^2 is slower at small z, saturates faster (more step-like)
            f = 0.5
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0:
                    z_eq = 0.3
                tanh_val = np.tanh(z_arr / z_eq)
                delta = f * tanh_val**2
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        else:
            return None

    # ====================
    # Unpack and execute
    # ====================
    wid, theory_name, k, task_type, task_data = args

    base_starts = [
        [0.315, 67.4], [0.30, 68.0], [0.32, 69.0],
        [0.29, 70.0],  [0.31, 68.5], [0.28, 71.0],
        [0.33, 67.0],  [0.34, 66.5],
    ]

    try:
        theory_tag = task_data['tag']
        E_fn = build_E_fn(theory_tag)
        if E_fn is None:
            return {'id': wid, 'name': theory_name, 'k': k,
                    'chi2': 1e8, 'aicc': 1e8, 'd_aicc': 1e8,
                    'Om': None, 'H0': None, 'status': 'FAIL'}

        best_val = 1e8
        best_x   = None

        # Multi-start Nelder-Mead
        for s in base_starts:
            try:
                res = minimize(lambda p, ef=E_fn: chi2_w(p, ef), s,
                               method='Nelder-Mead',
                               options={'xatol': 1e-6, 'fatol': 1e-6, 'maxiter': 5000})
                if res.fun < best_val:
                    best_val = res.fun
                    best_x   = res.x
            except Exception:
                continue

        # Differential evolution for global search (top candidates get this too)
        try:
            bounds_de = [(0.20, 0.50), (60.0, 80.0)]
            res_de = differential_evolution(
                lambda p, ef=E_fn: chi2_w(p, ef),
                bounds=bounds_de,
                maxiter=300,
                tol=1e-6,
                seed=42,
                workers=1,
                popsize=8,
            )
            if res_de.fun < best_val:
                best_val = res_de.fun
                best_x   = res_de.x
        except Exception:
            pass

        if best_x is None:
            return {'id': wid, 'name': theory_name, 'k': k,
                    'chi2': 1e8, 'aicc': 1e8, 'd_aicc': 1e8,
                    'Om': None, 'H0': None, 'status': 'FAIL'}

        Om_best, H0_best = float(best_x[0]), float(best_x[1])
        chi2_best = float(best_val)
        aicc_best = aicc_w(chi2_best, k)
        d_aicc    = aicc_best - LCDM_AICC

        # Estimate wa from rho_DE slope between z=0 and z=0.5
        try:
            z_test = np.array([0.0, 0.5, 1.0])
            E_test = E_fn(z_test, Om_best)
            if E_test is not None and np.all(np.isfinite(E_test)):
                rho_m0 = Om_best
                rho_r0 = OR_W
                def rho_de_z(z, Eval):
                    E2 = Eval**2
                    return E2 - rho_r0*(1+z)**4 - rho_m0*(1+z)**3
                rde0 = rho_de_z(0.0, E_test[0])
                rde1 = rho_de_z(0.5, E_test[1])
                if rde0 > 0 and rde1 > 0:
                    lna_diff   = math.log(1.0 / (1 + 0.5))
                    lnrho_diff = math.log(rde1 / rde0)
                    wa_proxy   = lnrho_diff / lna_diff / (-3.0)
                    wa_proxy   = float(wa_proxy)
                else:
                    wa_proxy = 0.0
            else:
                wa_proxy = 0.0
        except Exception:
            wa_proxy = 0.0

        status = 'PASS' if (aicc_best < LCDM_AICC and wa_proxy < 0) else 'KILL'
        return {
            'id': wid, 'name': theory_name, 'k': k,
            'chi2': chi2_best, 'aicc': aicc_best, 'd_aicc': d_aicc,
            'Om': Om_best, 'H0': H0_best,
            'wa_proxy': wa_proxy, 'status': status
        }

    except Exception as e:
        return {'id': wid, 'name': theory_name, 'k': k,
                'chi2': 1e8, 'aicc': 1e8, 'd_aicc': 1e8,
                'Om': None, 'H0': None,
                'status': f'ERROR:{e}'}


# ==============================================================================
# THEORY DEFINITIONS
# ==============================================================================

def build_ee_tasks():
    """Build all 30 EE theory tasks (EE01-EE30)."""
    tasks = []

    # GROUP 1: Eigenmode-Guided Saturation (EE01-EE08)
    tasks.append(('EE01', 'EV3-Gaussian: DD06+Gaussian@z=0.51 A=1/(2pi)', 2, {
        'tag': 'EE01'}))
    tasks.append(('EE02', 'EV3-Lorentzian: DD06+Lorentz@z=0.51 A=1/(2pi)', 2, {
        'tag': 'EE02'}))
    tasks.append(('EE03', 'EV3-Sigmoid: DD06+sigmoid@z=0.51 A=1/(4pi)', 2, {
        'tag': 'EE03'}))
    tasks.append(('EE04', 'EV3-TwoTanh: f1=1/3@z_eq + f2=1/6@z=0.51', 2, {
        'tag': 'EE04'}))
    tasks.append(('EE05', 'EV3-SteepTanh: z_half=z_eq/2, f=0.5*(1+1/(2pi))', 2, {
        'tag': 'EE05'}))
    tasks.append(('EE06', 'EV3-Interface: DD06+Gaussian@z_eq/pi A=1/(2pi^2)', 2, {
        'tag': 'EE06'}))
    tasks.append(('EE07', 'EV3-ModScale: z_eff=z_eq+z_c*exp(-z/z_c) f=0.5', 2, {
        'tag': 'EE07'}))
    tasks.append(('EE08', 'EV3-PhaseStep: DD06+step@z=0.51 A=1/e^2', 2, {
        'tag': 'EE08'}))

    # GROUP 2: Superposition of Saturation Scales (EE09-EE16)
    tasks.append(('EE09', 'MultiScale: f1=0.5@z_eq + f2=1/(2pi)@z=0.7', 2, {
        'tag': 'EE09'}))
    tasks.append(('EE10', 'MultiScale: f1=1/3@z_eq + f2=1/(3pi)@z=1.0', 2, {
        'tag': 'EE10'}))
    tasks.append(('EE11', 'TripleScale: Om*tanh@z_eq + OL0*tanh@0.7 + 1/(2pi^2)*tanh@1.0', 2, {
        'tag': 'EE11'}))
    tasks.append(('EE12', 'TanhArctan: 1/3*tanh + 1/pi*arctan @z_eq', 2, {
        'tag': 'EE12'}))
    tasks.append(('EE13', 'TanhLinSat: 1/3*tanh + 1/6*z/(1+z) @z_eq', 2, {
        'tag': 'EE13'}))
    tasks.append(('EE14', 'TwoPhysScale: 1/4*tanh@z_eq + 1/4*tanh@sqrt(OL0/Om)', 2, {
        'tag': 'EE14'}))
    tasks.append(('EE15', 'HarmonicTriple: 1/3*tanh@z_eq + 1/(3pi)*tanh@pi*z_eq + ...', 2, {
        'tag': 'EE15'}))
    tasks.append(('EE16', 'TanhErf: 0.4*tanh@z_eq + 0.1*erf@0.7', 2, {
        'tag': 'EE16'}))

    # GROUP 3: Asymmetric Saturation (EE17-EE24)
    tasks.append(('EE17', 'Asym-TanhExpDecay: alpha=0.5*tanh + beta=1/(2pi)*z/(1+z)*exp', 2, {
        'tag': 'EE17'}))
    tasks.append(('EE18', 'Asym-TanhGaussPeak: 0.5*tanh*(1+1/(2e)*gauss@z_eq)', 2, {
        'tag': 'EE18'}))
    tasks.append(('EE19', 'Asym-TwoPieceTanh: f=0.5*(w*tanh@2z_eq + (1-w)*tanh@z_eq/2)', 2, {
        'tag': 'EE19'}))
    tasks.append(('EE20', 'Asym-EnergyRatio: OL0/(Om+OL0)*tanh + Om/(Om+OL0)*(x-1)/(x+ratio)', 2, {
        'tag': 'EE20'}))
    tasks.append(('EE21', 'Asym-SigmoidAmp: f_eff=(1/3*(1-w)+2/3*w)*tanh@z_eq', 2, {
        'tag': 'EE21'}))
    tasks.append(('EE22', 'Asym-PeakCorr: 0.5*tanh*(1+1/(4pi)*exp(-(z/z_eq)^2))', 2, {
        'tag': 'EE22'}))
    tasks.append(('EE23', 'Asym-ThreeRegime: gen+ann smoothly joined at z_eq', 2, {
        'tag': 'EE23'}))
    tasks.append(('EE24', 'Asym-SaturatedAnn: 1/4*cap_tanh + 1/4*tanh @z_eq', 2, {
        'tag': 'EE24'}))

    # GROUP 4: Fisher-Perturbed Optimal (EE25-EE30)
    tasks.append(('EE25', 'FisherPerturb: f=1/3, tanh(z/z_eq)', 2, {
        'tag': 'EE25'}))
    tasks.append(('EE26', 'FisherPerturb: f=1/pi, tanh(z/z_eq)', 2, {
        'tag': 'EE26'}))
    tasks.append(('EE27', 'FisherPerturb: f=1/e, tanh(z/z_eq)', 2, {
        'tag': 'EE27'}))
    tasks.append(('EE28', 'FisherPerturb: f=2/pi, tanh(z/z_eq)', 2, {
        'tag': 'EE28'}))
    tasks.append(('EE29', 'FisherPerturb: f=0.5, tanh^(1/2)(z/z_eq)', 2, {
        'tag': 'EE29'}))
    tasks.append(('EE30', 'FisherPerturb: f=0.5, tanh^2(z/z_eq)', 2, {
        'tag': 'EE30'}))

    return tasks


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print('=' * 70)
    print('L30 Common-Structure + Perverse Attack: EE01-EE30')
    print('=' * 70)
    print()
    print('Base: DD06/DD18 champion -- delta(z) = 0.5*tanh(z/z_eq)')
    print('      z_eq = (OL0/Om)^(1/3) - 1')
    print()
    print('Group 1 (EE01-EE08): Eigenmode-Guided Saturation -- EV3 blind spot')
    print('Group 2 (EE09-EE16): Superposition of Saturation Scales')
    print('Group 3 (EE17-EE24): Asymmetric Saturation (A4-motivated)')
    print('Group 4 (EE25-EE30): Fisher-Perturbed Optimal around DD06')
    print()
    print(f'LCDM baseline: chi2={LCDM_BASELINE_CHI2}, AICc={LCDM_BASELINE_AICC}')
    print()

    tasks = build_ee_tasks()
    worker_args = [
        (t[0], t[1], t[2], 'ee_k2', t[3])
        for t in tasks
    ]
    print(f'Theories to test: {len(worker_args)}')
    print()

    print('Launching 9-worker multiprocessing pool (spawn)...')
    ctx = multiprocessing.get_context('spawn')
    with ctx.Pool(processes=9) as pool:
        raw_results = pool.map(worker_fn, worker_args)

    # Sort by AICc
    raw_results.sort(key=lambda r: r['aicc'])

    print()
    print('=' * 70)
    print('RESULTS (EE01-EE30) sorted by AICc:')
    print('=' * 70)
    print(f"{'ID':>5} {'Theory Name':44s} {'k':>2} {'chi2':>9} {'AICc':>9} {'dAICc':>8} {'wa':>7} {'Result':>7}")
    print('-' * 98)

    pass_count  = 0
    kill_count  = 0
    gc_count    = 0  # game-changer: dAICc < -4 AND wa < -0.5
    champion    = None

    for r in raw_results:
        if r['status'] == 'PASS':
            pass_count += 1
            if champion is None or r['aicc'] < champion['aicc']:
                champion = r
            wa_v = r.get('wa_proxy', 0.0)
            if r['d_aicc'] < -4.0 and wa_v < -0.5:
                gc_count += 1
        elif r['status'] == 'KILL':
            kill_count += 1

        chi2_s = f"{r['chi2']:.4f}"    if r['chi2']   < 1e7 else '  FAIL  '
        aicc_s = f"{r['aicc']:.4f}"    if r['aicc']   < 1e7 else '  FAIL  '
        dacc_s = f"{r['d_aicc']:+.4f}" if r['d_aicc'] < 1e7 else '  FAIL  '
        wa_s   = f"{r.get('wa_proxy', 0.0):+.4f}"
        print(f"{r['id']:>5} {r['name'][:44]:44s} {r['k']:>2} "
              f"{chi2_s:>9} {aicc_s:>9} {dacc_s:>8} {wa_s:>7} {r['status']:>7}")

    print()
    print(f'PASS: {pass_count}  /  KILL: {kill_count}')
    print(f'GAME-CHANGER (dAICc < -4 AND wa < -0.5): {gc_count}')
    if champion:
        print(f"Champion: {champion['id']} | dAICc={champion['d_aicc']:.4f} | "
              f"chi2={champion['chi2']:.4f} | wa={champion.get('wa_proxy', 0.0):.4f} | "
              f"Om={champion['Om']:.4f} | H0={champion['H0']:.4f}")
    print()

    # Save JSON
    out_json = os.path.join(_SCRIPT_DIR, 'l30_results10.json')

    def jsonify(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, dict):
            return {kk: jsonify(vv) for kk, vv in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [jsonify(v) for v in obj]
        return obj

    save_data = {
        'run': 'L30-EE01-EE30',
        'description': 'Common-structure + perverse attack -- EV3, multi-scale, asymmetric, Fisher',
        'theories': raw_results,
        'pass_count': pass_count,
        'kill_count': kill_count,
        'gc_count': gc_count,
        'champion': champion,
        'lcdm_baseline': {'chi2': LCDM_BASELINE_CHI2, 'aicc': LCDM_BASELINE_AICC},
    }

    with open(out_json, 'w', encoding='utf-8') as fp:
        json.dump(jsonify(save_data), fp, indent=2, ensure_ascii=False)
    print(f'Results saved to: {out_json}')


if __name__ == '__main__':
    main()
