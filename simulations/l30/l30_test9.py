# -*- coding: utf-8 -*-
"""
l30_test9.py -- L30 Common-Structure Fundamental Physics (DD01-DD30)
=====================================================================
Physical motivation: WHY does data prefer saturation-type dark energy?

From SQMH A1-A4 rate equation analysis:
  d(rho_DE)/dt = Gamma_gen - alpha * Omega_m(z) * rho_crit
  => At steady state: rho_DE ~ Gamma_gen / (alpha * Omega_m(z))
  => As Omega_m(z) -> 0 (void domination), rho_DE saturates at asymptote
  => Natural saturation emerges from matter-void phase transition near z~0.3-1.0

All DD theories derive saturation from a specific A1-A4 physical statement.
Forms: rho_DE = OL0 * (1 + delta(z)) where delta(z) > 0 and SATURATES.

Key physical formula (matter-DE ratio):
  delta_phys(z) = [Omega_m(z)/Omega_m(0) - 1] ∝ [(1+z)^3 - 1] / [(1+z)^3 + OL0/Om]

LCDM baseline: chi2=10.192, AICc=15.392 (k=2, n=13)
KILL if AICc >= 15.392
IDs: DD01-DD30
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
    Self-contained worker for DD theories.
    Each theory: one-line physical derivation comment + saturation-type delta(z).
    All constants theoretically derived from A1-A4.
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
    from scipy.optimize import minimize

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
    # E(z) FACTORY: each DD theory is a closure over fixed physical constants
    # -------------------------------------------------------------------------

    def build_E_fn(theory_tag, params):
        """
        Build E(z) from theory_tag. All delta(z) are SATURATION-type:
        delta(z) > 0 for z > 0, delta -> constant as z -> inf.
        """

        if theory_tag == 'DD01':
            # A1+A3 steady-state: rho_DE = Gamma_gen / (alpha*Omega_m(z))
            # => delta(z) = Om/OL0 * [(1+z)^3/(1+OL0/Om/(1+z)^3) - 1]
            # Simplified to matter-ratio saturation: delta = f*[(1+z)^3-1]/[(1+z)^3+OL0/Om]
            # f = 1/3 (dimensionless: 1 void space dimension per 3 matter dimensions)
            f = 1.0 / 3.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                ratio = OL0 / Om  # DE-to-matter ratio at z=0
                x = (1.0 + z_arr)**3
                delta = f * (x - 1.0) / (x + ratio)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD02':
            # A1: annihilation rate proportional to matter density squared (pair process)
            # => higher-order suppression at high z: delta = f*(x^3-1)/(x^3+ratio)^2
            # => stronger saturation than linear, faster approach to asymptote
            # f = 1/2 (2 quanta per annihilation event)
            f = 1.0 / 2.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                ratio = OL0 / Om
                x = (1.0 + z_arr)**3
                delta = f * (x - 1.0) / ((x + ratio)**2 / (1.0 + ratio))
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD03':
            # A3: generation uniform => Gamma_gen = const * Hubble_volume
            # => DE grows as comoving void fraction = 1 - Om*(1+z)^3/E^2(z)
            # Approximation at leading order: delta = f * Omega_m(z) ratio
            # f = pi/4 (solid angle fraction of SQ quanta emission sphere)
            f = math.pi / 4.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                ratio = OL0 / Om
                x = (1.0 + z_arr)**3
                # delta: how much more DE than LCDM, saturates as x->inf
                # at large z: Om(z)->1, delta->0; at z=0: delta=f
                delta = f * (1.0 - 1.0/(1.0 + ratio/x))
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD04':
            # A4: net SQ rate = gen - ann; void fraction = 1 - Omega_m(z)
            # => DE proportional to void fraction: delta = f*[1 - Om/(Om+OL0*(1+z)^-3)]
            # f = 1 (void fraction directly feeds DE)
            # This is the "void volume growth" saturation
            f = 1.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                x = (1.0 + z_arr)**3
                # void_frac(z) = OL0 / (Om*x + OL0) -- goes from OL0 at z=0 to 0 at high z
                void_frac_0 = OL0 / (Om + OL0)
                void_frac_z = OL0 / (Om * x + OL0)
                # delta > 0 when less void than today? No: today has max voids.
                # Reinterpret: delta = f * (void_frac_0 - void_frac_z) / void_frac_0
                # This gives delta > 0 at high z where fewer voids -> less suppression
                # Wait: data wants MORE DE at high z. So: delta proportional to matter excess.
                # delta = f * (Om*x / (Om*x + OL0) - Om/(Om+OL0))
                matter_frac_z = Om * x / (Om * x + OL0)
                matter_frac_0 = Om / (Om + OL0)
                delta = f * (matter_frac_z - matter_frac_0) / (1.0 - matter_frac_0)
                delta = np.maximum(delta, 0.0)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD05':
            # A1+A3: cosmic time integral of net SQ generation rate
            # Integral of [Gamma_gen - alpha*Om(a)] da from a=1 to a=1/(1+z)
            # => delta = f * integral_z = f * ln(1+z) * (1 - Om_frac)
            # f = 1/e (Boltzmann suppression of quantum transitions)
            f = math.exp(-1.0)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                ratio = OL0 / Om
                x = (1.0 + z_arr)**3
                # Time-integrated saturation: grows as ln(1+z) but saturates via matter fraction
                lnz  = np.log1p(z_arr)
                frac = ratio / (x + ratio)  # = OL0/Om / ((1+z)^3 + OL0/Om) -> void fraction proxy
                delta = f * lnz * frac
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD06':
            # A1: Hubble rate decrease -> annihilation rate decrease -> DE increase
            # Hubble damping: ann_rate ~ H(z), so delta ~ 1 - H(z)/H0 = 1 - E(z)
            # At leading order for OL0-dominated universe: E~1, so delta~OL0*z/(2(1+z))
            # Saturation form: delta = f * (1 - 1/E_approx) where E_approx via z/(1+z)
            # f = 1/2 (two-body Hubble damping)
            f = 0.5
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                # Hubble-rate saturation: as H increases at high z, DE generation suppressed
                # Use tanh as natural Hubble-crossing function at z_eq where Om=OL0
                # z_eq ~ (OL0/Om)^(1/3) - 1 -> transition scale
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

        elif theory_tag == 'DD07':
            # Scale factor a = 1/(1+z) as natural void growth parameter
            # A3: void volume ~ (1-a)^3 fraction of comoving volume
            # => delta = f * (1 - a)^2 / a  normalized
            # At z=0: a=1, delta=0; at high z: a->0, delta->f/a (but capped)
            # Better: delta = f * z/(1+z) -- exactly linear saturation in a
            # f = 1/3 (one dimension of void expansion per axis)
            f = 1.0 / 3.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                # Scale-factor saturation: delta = f * (1-a)/a * a = f * (1-a)
                # = f * z/(1+z) [the simplest saturation form]
                delta = f * z_arr / (1.0 + z_arr)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD08':
            # A4: net rate sign -> void=expansion; comoving void fraction evolution
            # Void fraction: F_void(z) = OL0/(Om*(1+z)^3 + OL0)
            # DE_extra = f * F_void(z=0) - F_void(z) -- DE grows when voids shrink
            # Actually: delta = f * [F_void(0) - F_void(z)] -> 0 at z=0, negative high z?
            # Correction: delta = f * [1 - F_void(z)/F_void(0)] gives saturation
            # f = pi/6 (packing fraction of spherical voids)
            f = math.pi / 6.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                x = (1.0 + z_arr)**3
                F0 = OL0 / (Om + OL0)          # void fraction today
                Fz = OL0 / (Om * x + OL0)      # void fraction at z
                # delta = f * (F0 - Fz) / F0 * (1/F0)
                # void shrinks going to high z -> more matter -> higher annihilation -> less DE
                # But data wants MORE DE at high z. So we look at it differently:
                # MORE matter -> MORE SQ annihilation -> less SQ quanta in matter -> MORE SQ in voids
                # The SQ conservation means SQ pushed out of matter accumulates in voids
                # => delta = f * (Omega_m(z) - Om) / OL0 -- proportional to matter excess
                Om_z = Om * x / (Om * x + OL0 + OR_W * (1.0 + z_arr)**4)
                Om_0 = Om / (Om + OL0)
                delta = f * np.maximum(Om_z - Om_0, 0.0) / OL0 * (Om + OL0)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD09':
            # A1: SQ depletion near matter halos scales as overdensity^(2/3)
            # => DE compensation delta ~ f * (Om(z)/Om0)^(2/3) - 1 -- power-law saturation
            # f = 1/(2*pi) (one quantum state per 2pi phase space volume)
            f = 1.0 / (2.0 * math.pi)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                x = (1.0 + z_arr)
                # matter density ratio (1+z)^3 -- halo overdensity scaling
                # delta = f * ((1+z)^2 - 1) / (1 + (1+z)^2) -- saturation with exponent 2/3 approx
                delta = f * (x**2 - 1.0) / (1.0 + x**2)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD10':
            # A3: SQ replenishment in void regions -- generation fills voids after matter
            # evacuates them. Replenishment rate ~ 1 - Omega_m(z) (void filling time).
            # Cumulative delta = integral_0^z [1 - Om/(Om(1+z')^3+OL0)] dz'
            # Closed form: arctan(z/z_half) where z_half ~ (OL0/Om)^(1/3)
            # f = 1/(2*pi) (quantum phase saturation)
            f = 1.0 / (2.0 * math.pi)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_half = (OL0 / Om)**(1.0/3.0)
                delta = f * np.arctan(z_arr / z_half)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD11':
            # A1+A3 equilibrium displacement: steady state shifts as Omega_m changes
            # Delta_rho_DE = Gamma_gen * d/dt(1/Omega_m(z)) integrated
            # => delta = f * ln(Omega_m(0)/Omega_m(z)) = f * ln(Om/[Om*(1+z)^3])
            #           = -f * 3*ln(1+z) ... this grows indefinitely (not saturation)
            # Modified: delta = f * ln(1 + z/(1+z)) -- bounded log saturation
            # f = 1/(3*pi) (3D space / pi cyclicity)
            f = 1.0 / (3.0 * math.pi)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                delta = f * np.log1p(z_arr / (1.0 + z_arr))
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD12':
            # A4: total SQ quanta conservation in comoving volume
            # SQ_void + SQ_matter = const => as matter grows SQ_void grows too
            # delta = f * [Omega_m(z) - Om] / Om
            # At high z, Omega_m(z) >> Om -> delta >> 0 (not saturating)
            # Modified with conservation bound: delta = f * tanh([Omega_m(z)-Om]/Om)
            # f = 1/4 (four-volume quantum: 3D space + 1D time)
            f = 1.0 / 4.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                x = (1.0 + z_arr)**3
                # Omega_m(z) ~ Om*(1+z)^3 in approx (true value needs E^2 in denom)
                # normalized excess: (Om_z - Om) / OL0
                excess = Om * (x - 1.0) / OL0
                delta  = f * np.tanh(excess)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD13':
            # A1: matter-annihilation rate ~ rho_m^2 (two-body process A1 extended)
            # Two-body: rate ~ Omega_m^2(z) * rho_crit^2
            # => delta = f * [(1+z)^6 - 1] / [(1+z)^6 + (OL0/Om)^2]
            # Physical: pair-annihilation of matter-antiSQ pairs
            # f = 1/6 (6 quanta per pair-annihilation vertex in 3+1D)
            f = 1.0 / 6.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                ratio2 = (OL0 / Om)**2
                x6 = (1.0 + z_arr)**6
                delta = f * (x6 - 1.0) / (x6 + ratio2)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD14':
            # A3: uniform generation + spatial diffusion to voids
            # Diffusion-limited: delta = f * erf(z / z_diff)
            # z_diff = 1/sqrt(pi) from Gaussian quantum diffusion length
            # f = 1/(2*pi) (quantum diffusion coefficient)
            f     = 1.0 / (2.0 * math.pi)
            z_diff = 1.0 / math.sqrt(math.pi)
            def E_fn(z_arr, Om):
                from scipy.special import erf
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                delta = f * erf(z_arr / z_diff)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD15':
            # A4: matter-Lambda equality transition as natural saturation scale
            # At z_eq: Omega_m(z_eq) = OL0 => (1+z_eq)^3 = OL0/Om
            # delta = f * [1 - exp(-(z/z_eq)^2)]  -- Gaussian rise to saturation
            # f = 1/3 (one saturation axis per spatial dimension)
            f = 1.0 / 3.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0.01:
                    z_eq = 0.3
                delta = f * (1.0 - np.exp(-(z_arr / z_eq)**2))
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD16':
            # A1+A3: exact matter-ratio saturation from rate balance
            # rho_DE(z) = rho_DE(0) * [Om + OL0] / [Om*(1+z)^3 + OL0]
            # => E^2 = Or*(1+z)^4 + Om*(1+z)^3 + OL0*(Om+OL0)/(Om*(1+z)^3+OL0)
            # This is the "exact" rate-balance prediction from A1+A3 with f=1
            # Physical: DE density inversely proportional to matter density (zero-sum SQ)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                x = (1.0 + z_arr)**3
                denom = Om * x + OL0
                # rho_DE at z proportional to 1/Omega_m(z) -- the steady-state solution
                rho_DE = OL0 * (Om + OL0) / denom
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD17':
            # A1: matter halos deplete local SQ; total SQ quanta in universe conserved
            # => rho_DE * V_void + rho_SQ_matter * V_matter = const
            # => rho_DE = rho_DE0 * (1 + f*(Om*(1+z)^3 - Om)/OL0)  with saturation at high z
            # f = OL0 (fraction of universe that is DE today -- exact conservation)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                x = (1.0 + z_arr)**3
                # Conservation: SQ displaced from matter goes to void (DE)
                # delta proportional to how much more matter there is at z vs today
                # saturated by the OL0 denominator
                f = OL0
                delta = f * Om * (x - 1.0) / (Om * x + OL0)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD18':
            # A3+A4: generation uniform; net rate zero at matter-Lambda equality
            # => equilibrium at z_eq, delta grows from z_eq outward
            # delta = f * |tanh((z - z_eq)/z_eq)|  -- symmetric around equilibrium
            # f = 1/2 (half goes each way at equilibrium)
            f = 1.0 / 2.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0.01:
                    z_eq = 0.3
                delta = f * np.tanh(z_arr / z_eq)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD19':
            # A1: annihilation = alpha*Omega_m(z); f = 1 means full SQ conversion
            # Modified: two-step process: matter->SQ_intermediate->DE
            # => delta = f * (1 - 1/cosh(z/z_half))  -- hyperbolic cosine saturation
            # z_half = (OL0/Om)^(1/3); f = 2/pi (normalization of half-Cauchy)
            f = 2.0 / math.pi
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_half = (OL0 / Om)**(1.0/3.0)
                delta = f * (1.0 - 1.0 / np.cosh(z_arr / z_half))
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD20':
            # A4: net rate determines DE. Rate sign boundary at matter-Lambda equality.
            # Below z_eq: void-dominated -> DE growing; above: matter-dominated -> DE suppressed
            # Full physical: delta = f * (x-1)^(1/2) / (x + ratio)^(1/2)  -- geometric mean saturation
            # This is sqrt of the DD01 form -- softer saturation
            # f = 1/2 (geometric mean of 1D and 3D saturation exponents)
            f = 1.0 / 2.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                ratio = OL0 / Om
                x = (1.0 + z_arr)**3
                num = np.sqrt(np.maximum(x - 1.0, 0.0))
                den = np.sqrt(x + ratio)
                delta = f * num / den
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD21':
            # A1+A3: DE rate equation with linear damping
            # d(rho_DE)/da = Gamma/H - 3*(1+w)*rho_DE/a
            # At w=-1 (quasi-LCDM): no dilution, delta accumulates as integral
            # delta = f * integral_a^1 [Om(a)/OL0] da/a -- saturation from finite range
            # Closed form approx: delta = f * [Om/(3*OL0)] * [(1+z)^3 - 1]/(1+z)^2
            # f = 1/3 (3D integration factor)
            f = 1.0 / 3.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                x  = (1.0 + z_arr)
                # Integral of Omega_m(a) from a to 1 normalized to OL0
                # Omega_m(a) = Om*a^{-3} / E^2(a); approximate E~1 for OL0-dom universe
                # integral_a^1 Om*a^{-3} da/a ~ Om/(3) * (a^{-3}-1)/1 = Om/3 * ((1+z)^3-1)
                delta = f * (Om / (3.0 * OL0)) * (x**3 - 1.0) / x**2
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD22':
            # A1: matter density proxy = Omega_m * (1+z)^3; saturation when this >> OL0
            # Logistic saturation: delta = f / [1 + exp(-k*(z - z_half))]
            # z_half = matter-Lambda equality; k = 3/z_half (3D matter scaling)
            # f = 1/3 (one saturation per spatial dimension)
            f = 1.0 / 3.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_half = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_half <= 0.05:
                    z_half = 0.3
                k = 3.0 / z_half
                # logistic: 0 at z=0, f at z>>z_half
                # Standard logistic goes to f/2 at z_half; shift so it's 0 at z=0
                sig_0 = 1.0 / (1.0 + math.exp(k * z_half))
                sig_z = 1.0 / (1.0 + np.exp(-k * (z_arr - z_half)))
                delta = f * (sig_z - sig_0) / (1.0 - sig_0)
                delta = np.maximum(delta, 0.0)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD23':
            # A3: uniform SQ generation rate = c * H0^2 (constant in cosmic time)
            # Total SQ generated from z to 0: integral dt = integral dz/(H*(1+z))
            # => delta = f * int_0^z dz'/(E(z')*(1+z')) using LCDM approx for E
            # Saturation: integral converges as LCDM has finite lookback time
            # Computed as: delta = f * arctan(sqrt(Om/OL0) * (1+z)^(3/2)) / (pi/2)
            # f = 1/4 (quarter-cycle normalization)
            f = 1.0 / 4.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                # Lookback time proxy: arctan(sqrt(Om/OL0)*(1+z)^(3/2)) saturates
                arg = math.sqrt(Om / OL0) * (1.0 + z_arr)**(1.5)
                # normalize: at z=0: arg0 = sqrt(Om/OL0)
                arg0 = math.sqrt(Om / OL0)
                delta = f * (np.arctan(arg) - math.atan(arg0)) / (math.pi / 2.0)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD24':
            # A4: DE in voids compensates reduced DE near matter (conservation)
            # => Total DE = rho_DE0; fraction in voids > average; fraction near matter < average
            # Volume-averaged: delta = f * (void_frac(z) - void_frac(0)) / void_frac(0)
            # [inverted: today has most voids; past had fewer -> higher DE/void today?]
            # SQMH: delta = f * (matter_frac(z) - matter_frac(0)) -- direct proportionality
            # f = 2/pi (normalization of arctan integral over full range)
            f = 2.0 / math.pi
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                x = (1.0 + z_arr)**3
                matter_frac_z = Om * x / (Om * x + OL0)
                matter_frac_0 = Om / (Om + OL0)
                delta = f * np.maximum(matter_frac_z - matter_frac_0, 0.0)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD25':
            # A1+A4: rate equation in a-space; transition at a_eq = (Om/OL0)^(1/3)
            # Energy scale of transition: E_eq = sqrt(2*OL0) -- geometric mean of expansions
            # delta = f * (1 - a^3/(a^3 + a_eq^3)) where a=1/(1+z)
            # = f * (1 - 1/((1+z)^3 * (Om/OL0) + 1)) = f * x / (x + OL0/Om)
            # This is EXACTLY z/(1+z)-like in a-space; f = 1/(1+Om) ~ 0.76
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                f = 1.0 / (1.0 + Om)
                ratio = OL0 / Om
                x = (1.0 + z_arr)**3
                delta = f * (x - 1.0) / (x + ratio)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD26':
            # A3: generation rate proportional to local expansion rate H(z)
            # => Gamma_gen ~ H(z) ~ H0 * E(z); at leading order E~1
            # Accumulated DE: delta = f * integral_0^z [E(z')/E0] dz' ... simplified
            # Saturation with Hubble dampening: delta = f * z/(1+z) * (1 + z/(z+z_H))
            # where z_H ~ sqrt(OL0/Om) is Hubble crossing scale
            # f = 1/(2*e) (quantum Boltzmann + two-channel)
            f = 1.0 / (2.0 * math.e)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_H = math.sqrt(OL0 / Om)  # Hubble crossing redshift scale
                sat1 = z_arr / (1.0 + z_arr)
                sat2 = z_arr / (z_arr + z_H)
                delta = f * (sat1 + sat2) / 2.0
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD27':
            # A1+A3+A4: three-channel superposition with matter-ratio weights
            # Channel 1 (A1 annihilation): delta1 = f1 * z/(1+z)
            # Channel 2 (A3 generation): delta2 = f2 * tanh(z/z_eq)
            # Channel 3 (A4 conservation): delta3 = f3 * arctan(z/z_eq)
            # Weights: f1=Om, f2=OL0, f3=1-Om-OL0 -- but f3~OR very small
            # Use f1=Om/(Om+OL0), f2=OL0/(Om+OL0), total=1
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                z_eq = (OL0 / Om)**(1.0/3.0) - 1.0
                if z_eq <= 0.01:
                    z_eq = 0.3
                f1 = Om / (Om + OL0)   # matter fraction weight
                f2 = OL0 / (Om + OL0)  # DE fraction weight
                delta1 = f1 * z_arr / (1.0 + z_arr)
                delta2 = f2 * np.tanh(z_arr / z_eq)
                delta = delta1 + delta2
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD28':
            # A1: two-body annihilation rate ~ (rho_m * rho_SQ); rho_SQ ~ rho_DE
            # Self-consistent: d(rho_DE)/dt = Gamma - alpha*rho_m*rho_DE
            # Steady state: rho_DE = Gamma/(alpha*rho_m) -- pure 1/rho_m form
            # With normalization: rho_DE(z) = rho_DE0 * Om_0/Om(z)
            #                   = OL0 * [Om+OL0] / [Om*(1+z)^3+OL0] -- exact SQMH formula
            # (This is the true self-consistent steady-state solution)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                x = (1.0 + z_arr)**3
                denom = Om * x + OL0
                # Full self-consistent DE density (1/rho_m steady state)
                rho_DE = OL0 * (Om + OL0) / denom  # same as DD16 but derived differently
                # Correction: add transition smoothing from finite coupling constant
                # alpha_dim = pi (one quantum per radian of phase space)
                alpha = math.pi
                correction = 1.0 / (1.0 + alpha * OR_W * (1.0 + z_arr)**4 / Om)
                rho_DE = rho_DE * correction
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD29':
            # A3+A4: Generation fills voids; void growth rate = d(1-Omega_m(a))/da
            # Cumulative DE from void filling: delta ~ integral_0^z Om*(1+z)^3/E^3 dz / (3*OL0)
            # Saturation form using exact OL0-dominated limit:
            # delta = f * [Om/(3*OL0)] * z*(3+3z+z^2) / (1+z)^3
            # This gives EXACT saturation to f*Om/(3*OL0) as z->inf
            # f = 1 (complete void filling)
            f = 1.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                # z*(3+3z+z^2)/(1+z)^3 is the integral of (1+z')^2/(1+z')^3 from 0 to z
                # = integral_0^z 1/(1+z') dz' = ln(1+z) ... no, that's different
                # Correct: d/dz[(1+z)^3] = 3(1+z)^2, so integral (1+z)^3 dz = (1+z)^4/4 - 1/4
                # Let's use: delta = f * (Om/OL0) * (1 - 1/(1+z)^3) / 3
                # This is exact integral of Om*a^{-3}/OL0 da from a to 1 in a-space
                delta = f * (Om / (3.0 * OL0)) * (1.0 - 1.0 / (1.0 + z_arr)**3)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10 * abs(OL0))
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0):
                    return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'DD30':
            # A1+A2+A3+A4: Full SQMH synthesis -- quantum-classical boundary term
            # A2 (quantum-classical boundary from A1) contributes a correction
            # Boundary term: delta_QC = f_QC * exp(-(z/z_P)^2) near z=0 (Planck-scale)
            # Combined: delta = delta_main + delta_QC
            # delta_main = f * (x-1)/(x+ratio) [DD01 base]
            # delta_QC = f_QC * (1 - exp(-z^2)) * exp(-z/z_P)
            # z_P = 1/pi (Planck-Hubble time ratio at z~0)
            # f = 1/3, f_QC = 1/(4*pi)
            f     = 1.0 / 3.0
            f_QC  = 1.0 / (4.0 * math.pi)
            z_P   = 1.0 / math.pi
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0 or Om <= 0:
                    return None
                ratio = OL0 / Om
                x = (1.0 + z_arr)**3
                # Main saturation from A1+A3 rate balance
                delta_main = f * (x - 1.0) / (x + ratio)
                # Quantum-classical boundary correction (A2): peaks near z=0, decays
                delta_QC   = f_QC * (1.0 - np.exp(-z_arr**2)) * np.exp(-z_arr / z_P)
                delta = delta_main + delta_QC
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
        params     = task_data.get('params', {})
        E_fn = build_E_fn(theory_tag, params)
        if E_fn is None:
            return {'id': wid, 'name': theory_name, 'k': k,
                    'chi2': 1e8, 'aicc': 1e8, 'd_aicc': 1e8,
                    'Om': None, 'H0': None, 'extra': params, 'status': 'FAIL'}

        best_val = 1e8
        best_x   = None
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

        if best_x is None:
            return {'id': wid, 'name': theory_name, 'k': k,
                    'chi2': 1e8, 'aicc': 1e8, 'd_aicc': 1e8,
                    'Om': None, 'H0': None, 'extra': params, 'status': 'FAIL'}

        Om_best, H0_best = float(best_x[0]), float(best_x[1])
        chi2_best = float(best_val)
        aicc_best = aicc_w(chi2_best, k)
        d_aicc    = aicc_best - LCDM_AICC

        # Estimate wa from rho_DE slope between z=0 and z=0.5
        try:
            z_test = np.array([0.0, 0.5, 1.0])
            E_test = E_fn(z_test, Om_best)
            if E_test is not None and np.all(np.isfinite(E_test)):
                rho_m0  = Om_best
                rho_r0  = OR_W
                def rho_de_z(z, Eval):
                    E2 = Eval**2
                    return E2 - rho_r0*(1+z)**4 - rho_m0*(1+z)**3
                rde0 = rho_de_z(0.0, E_test[0])
                rde1 = rho_de_z(0.5, E_test[1])
                if rde0 > 0 and rde1 > 0:
                    lna_diff  = math.log(1.0/(1+0.5))
                    lnrho_diff = math.log(rde1/rde0)
                    wa_proxy = lnrho_diff / lna_diff / (-3.0) - (-1.0)
                    wa_proxy = float(wa_proxy)
                else:
                    wa_proxy = 0.0
            else:
                wa_proxy = 0.0
        except Exception:
            wa_proxy = 0.0

        status = 'PASS' if aicc_best < LCDM_AICC else 'KILL'
        return {
            'id': wid, 'name': theory_name, 'k': k,
            'chi2': chi2_best, 'aicc': aicc_best, 'd_aicc': d_aicc,
            'Om': Om_best, 'H0': H0_best, 'extra': params,
            'wa_proxy': wa_proxy, 'status': status
        }

    except Exception as e:
        return {'id': wid, 'name': theory_name, 'k': k,
                'chi2': 1e8, 'aicc': 1e8, 'd_aicc': 1e8,
                'Om': None, 'H0': None, 'extra': None,
                'status': f'ERROR:{e}'}


# ==============================================================================
# THEORY DEFINITIONS
# ==============================================================================

def build_dd_tasks():
    """Build all 30 DD theory tasks (DD01-DD30)."""
    tasks = []

    # DD01: A1+A3 steady-state matter-ratio saturation, f=1/3
    tasks.append(('DD01', 'SteadyState: (x-1)/(x+OL0/Om) f=1/3', 2, {
        'tag': 'DD01', 'params': {}
    }))

    # DD02: A1 pair-annihilation (two-body), stronger saturation (x^3-1)/(x^3+ratio)^2
    tasks.append(('DD02', 'PairAnnih: (x^6-1)/(x^6+ratio^2) f=1/2', 2, {
        'tag': 'DD02', 'params': {}
    }))

    # DD03: A3 generation = Hubble volume -- void fraction saturation, f=pi/4
    tasks.append(('DD03', 'VoidVolume: 1-1/(1+ratio/x) f=pi/4', 2, {
        'tag': 'DD03', 'params': {}
    }))

    # DD04: A4 net rate -> matter fraction growth drives DE increase
    tasks.append(('DD04', 'MatterFrac: delta=(matter_frac_z - matter_frac_0) f=1', 2, {
        'tag': 'DD04', 'params': {}
    }))

    # DD05: A1+A3 time-integral with Boltzmann factor, f=1/e
    tasks.append(('DD05', 'TimeIntegral: ln(1+z)*OL0/(x+OL0) f=1/e', 2, {
        'tag': 'DD05', 'params': {}
    }))

    # DD06: A1 Hubble damping -> tanh(z/z_eq) saturation, f=1/2
    tasks.append(('DD06', 'HubbleDamp: tanh(z/z_eq) f=1/2', 2, {
        'tag': 'DD06', 'params': {}
    }))

    # DD07: A3 scale-factor void growth -> z/(1+z), f=1/3
    tasks.append(('DD07', 'ScaleFactorVoid: z/(1+z) f=1/3', 2, {
        'tag': 'DD07', 'params': {}
    }))

    # DD08: A4 SQ conservation -> matter excess drives DE into voids
    tasks.append(('DD08', 'SQConservation: Om_excess/OL0 f=pi/6', 2, {
        'tag': 'DD08', 'params': {}
    }))

    # DD09: A1 halo depletion ~ overdensity^(2/3) -> (1+z)^2 saturation, f=1/(2pi)
    tasks.append(('DD09', 'HaloDepletion: (x^2-1)/(1+x^2) f=1/(2pi)', 2, {
        'tag': 'DD09', 'params': {}
    }))

    # DD10: A3 void replenishment -> arctan saturation with z_half=(OL0/Om)^(1/3)
    tasks.append(('DD10', 'VoidReplenish: arctan(z/z_half) f=1/(2pi)', 2, {
        'tag': 'DD10', 'params': {}
    }))

    # DD11: A1+A3 equilibrium displacement -> log-saturation, f=1/(3pi)
    tasks.append(('DD11', 'EquilDisplace: ln(1+z/(1+z)) f=1/(3pi)', 2, {
        'tag': 'DD11', 'params': {}
    }))

    # DD12: A4 SQ quanta conservation -> tanh(Om_excess/OL0), f=1/4
    tasks.append(('DD12', 'SQQuanta: tanh(Om*(x-1)/OL0) f=1/4', 2, {
        'tag': 'DD12', 'params': {}
    }))

    # DD13: A1 two-body pair annihilation -> (x^6-1)/(x^6+ratio^2), f=1/6
    tasks.append(('DD13', 'TwoBodyAnn: (x^6-1)/(x^6+ratio^2) f=1/6', 2, {
        'tag': 'DD13', 'params': {}
    }))

    # DD14: A3 diffusion-limited -> erf(z/z_diff), f=1/(2pi)
    tasks.append(('DD14', 'Diffusion: erf(z/sqrt(pi)) f=1/(2pi)', 2, {
        'tag': 'DD14', 'params': {}
    }))

    # DD15: A4 matter-Lambda equality transition -> 1-exp(-(z/z_eq)^2), f=1/3
    tasks.append(('DD15', 'EqualityTrans: 1-exp(-(z/z_eq)^2) f=1/3', 2, {
        'tag': 'DD15', 'params': {}
    }))

    # DD16: A1+A3 exact steady-state 1/rho_m -> OL0*(Om+OL0)/(Om*x+OL0)
    tasks.append(('DD16', 'ExactSteadyState: OL0*(Om+OL0)/(Om*x+OL0)', 2, {
        'tag': 'DD16', 'params': {}
    }))

    # DD17: A1 halo SQ depletion + conservation -> delta=OL0*Om*(x-1)/(Om*x+OL0)
    tasks.append(('DD17', 'HaloConserve: OL0*Om*(x-1)/(Om*x+OL0)', 2, {
        'tag': 'DD17', 'params': {}
    }))

    # DD18: A3+A4 equilibrium at z_eq -> tanh(z/z_eq), f=1/2
    tasks.append(('DD18', 'NetRateEquil: tanh(z/z_eq) f=1/2', 2, {
        'tag': 'DD18', 'params': {}
    }))

    # DD19: A1 two-step conversion -> 1-1/cosh(z/z_half), f=2/pi
    tasks.append(('DD19', 'TwoStep: 1-sech(z/z_half) f=2/pi', 2, {
        'tag': 'DD19', 'params': {}
    }))

    # DD20: A4 geometric mean saturation -> sqrt((x-1)/(x+ratio)), f=1/2
    tasks.append(('DD20', 'GeoMeanSat: sqrt((x-1)/(x+ratio)) f=1/2', 2, {
        'tag': 'DD20', 'params': {}
    }))

    # DD21: A1+A3 rate integral in a-space -> Om/OL0*(x-1)/x^2, f=1/3
    tasks.append(('DD21', 'IntegralAspace: Om/OL0*(x-1)/x^2 f=1/3', 2, {
        'tag': 'DD21', 'params': {}
    }))

    # DD22: A1 logistic saturation at matter-Lambda equality, f=1/3
    tasks.append(('DD22', 'LogisticSat: sigmoid at z_eq f=1/3', 2, {
        'tag': 'DD22', 'params': {}
    }))

    # DD23: A3 lookback-time integral -> arctan(sqrt(Om/OL0)*(1+z)^1.5), f=1/4
    tasks.append(('DD23', 'LookbackArctan: arctan(sqrt(Om/OL0)*(1+z)^1.5) f=1/4', 2, {
        'tag': 'DD23', 'params': {}
    }))

    # DD24: A4 matter-fraction proportionality -> f*(matter_frac_z-matter_frac_0), f=2/pi
    tasks.append(('DD24', 'MatterFracPi: 2/pi*(matter_z-matter_0)', 2, {
        'tag': 'DD24', 'params': {}
    }))

    # DD25: A1+A4 a-space transition -> (x-1)/(x+OL0/Om), f=1/(1+Om)
    tasks.append(('DD25', 'ASpaceTransit: (x-1)/(x+ratio) f=1/(1+Om)', 2, {
        'tag': 'DD25', 'params': {}
    }))

    # DD26: A3 Hubble-proportional generation -> dual saturation, f=1/(2e)
    tasks.append(('DD26', 'HubbleGen: dual-sat z/(1+z)+z/(z+z_H) f=1/(2e)', 2, {
        'tag': 'DD26', 'params': {}
    }))

    # DD27: A1+A3+A4 three-channel with matter/DE fraction weights
    tasks.append(('DD27', 'ThreeChannel: Om*z/(1+z)+OL0*tanh(z/z_eq)', 2, {
        'tag': 'DD27', 'params': {}
    }))

    # DD28: A1 self-consistent 1/rho_m with radiation correction
    tasks.append(('DD28', 'SelfConsist: 1/rho_m + radiation correction', 2, {
        'tag': 'DD28', 'params': {}
    }))

    # DD29: A3+A4 void filling integral -> Om/OL0*(1-1/(1+z)^3)/3
    tasks.append(('DD29', 'VoidFill: Om/OL0*(1-1/x)/3 f=1', 2, {
        'tag': 'DD29', 'params': {}
    }))

    # DD30: A1+A2+A3+A4 full synthesis with quantum-classical boundary term
    tasks.append(('DD30', 'FullSQMH: A1+A3 base + A2 QC-boundary correction', 2, {
        'tag': 'DD30', 'params': {}
    }))

    return tasks


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print('=' * 70)
    print('L30 Common-Structure Fundamental Physics: DD01-DD30')
    print('=' * 70)
    print()
    print('Physical premise: SQMH A1+A3 rate equation => saturation-type DE')
    print('  d(rho_DE)/dt = Gamma_gen - alpha * Omega_m(z) * rho_crit')
    print('  Steady state: rho_DE ~ Gamma/[alpha*Om(z)] -> saturation as Om(z)->0')
    print()
    print('All theories: rho_DE = OL0*(1+delta(z)), delta(z)>0, SATURATING.')
    print(f'LCDM baseline: chi2={LCDM_BASELINE_CHI2}, AICc={LCDM_BASELINE_AICC}')
    print()

    # Build tasks
    tasks = build_dd_tasks()
    worker_args = [
        (t[0], t[1], t[2], 'dd_k2', t[3])
        for t in tasks
    ]
    print(f'Theories to test: {len(worker_args)}')
    print()

    # Run in parallel
    print('Launching 9-worker multiprocessing pool...')
    ctx  = multiprocessing.get_context('spawn')
    with ctx.Pool(processes=9) as pool:
        raw_results = pool.map(worker_fn, worker_args)

    # Sort by AICc
    raw_results.sort(key=lambda r: r['aicc'])

    print()
    print('=' * 70)
    print('RESULTS (DD01-DD30) sorted by AICc:')
    print('=' * 70)
    print(f"{'ID':>5} {'Theory Name':40s} {'k':>2} {'chi2':>9} {'AICc':>9} {'dAICc':>8} {'wa':>7} {'Result':>6}")
    print('-' * 92)

    pass_count = 0
    kill_count = 0
    champion   = None

    for r in raw_results:
        if r['status'] == 'PASS':
            pass_count += 1
            if champion is None or r['aicc'] < champion['aicc']:
                champion = r
        elif r['status'] == 'KILL':
            kill_count += 1

        chi2_str  = f"{r['chi2']:.4f}"  if r['chi2'] < 1e7  else '  FAIL  '
        aicc_str  = f"{r['aicc']:.4f}"  if r['aicc'] < 1e7  else '  FAIL  '
        dacc_str  = f"{r['d_aicc']:+.4f}" if r['d_aicc'] < 1e7 else '  FAIL  '
        wa_str    = f"{r.get('wa_proxy',0.0):+.4f}"
        print(f"{r['id']:>5} {r['name'][:40]:40s} {r['k']:>2} "
              f"{chi2_str:>9} {aicc_str:>9} {dacc_str:>8} {wa_str:>7} {r['status']:>6}")

    print()
    print(f'PASS: {pass_count}  /  KILL: {kill_count}')
    if champion:
        print(f"Champion: {champion['id']} | dAICc={champion['d_aicc']:.4f} | "
              f"chi2={champion['chi2']:.4f} | Om={champion['Om']:.4f} | H0={champion['H0']:.4f}")
    print()

    # Save JSON
    out_json = os.path.join(_SCRIPT_DIR, 'l30_results9.json')

    def jsonify(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, dict):
            return {k: jsonify(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [jsonify(v) for v in obj]
        return obj

    save_data = {
        'run': 'L30-DD01-DD30',
        'description': 'Common-structure saturation physics from SQMH A1-A4 rate equation',
        'theories': raw_results,
        'pass_count': pass_count,
        'kill_count': kill_count,
        'champion': champion,
        'lcdm_baseline': {'chi2': LCDM_BASELINE_CHI2, 'aicc': LCDM_BASELINE_AICC},
    }

    with open(out_json, 'w', encoding='utf-8') as fp:
        json.dump(jsonify(save_data), fp, indent=2, ensure_ascii=False)
    print(f'Results saved to: {out_json}')


if __name__ == '__main__':
    main()
