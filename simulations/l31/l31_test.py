# -*- coding: utf-8 -*-
"""
l31_test.py -- L31: SQT-derived theories (FA/GB/VG/MC groups)
==============================================================
Framework: Spacetime Quanta Theory (SQT)
  A1: Matter annihilates spacetime quanta; Gamma_ann = sigma_eff * rho_m * rho_st
  A2: Spacetime quanta are generated; Gamma_gen = kappa*(rho0 - rho_st)
  C1: Lorentz invariance -- annihilation proportional to T^mu_mu (radiation decouples)
  B': H = (Gamma_gen - Gamma_ann)/3 (generation = expansion)

Core SQT equilibrium:
  psi*(z) = 1 / (1 + alpha*(1+z)^3),  alpha = Omega_m / Omega_DE
  Gamma_norm(z) = (1+alpha)*(1+z)^3 / (1 + alpha*(1+z)^3)

Key: rho_DE(z) = OL0 * (1 + delta(z)), delta from SQT physics.

Group FA (FA01-FA08): Fundamental Annihilation -- delta = f * [Gamma_norm(z) - 1]
Group GB (GB01-GB08): Generation-Balance -- psi-field + two-channel variants
Group VG (VG01-VG08): V(psi) Ginzburg-Landau potential
Group MC (MC01-MC06): Multi-channel SQT (matter + vacuum scale)

LCDM baseline: chi2=10.192, AICc=15.392 (k=2, n=13)
KILL if AICc >= 15.392
IDs: FA01-FA08, GB01-GB08, VG01-VG08, MC01-MC06
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
    # E(z) FACTORY: SQT-derived theories
    # -------------------------------------------------------------------------

    def sqt_gamma_norm(z_arr, Om, OR_W):
        """Core SQT annihilation function.
        Gamma_norm(z) = (1+alpha)*(1+z)^3 / (1 + alpha*(1+z)^3)
        alpha = Omega_m / Omega_DE (coupling = matter/DE ratio at z=0)
        Physical: Omega_DE/matter equilibrium scale.
        """
        OL0 = 1.0 - Om - OR_W
        if OL0 <= 0 or Om <= 0:
            return None, None
        alpha = Om / OL0
        num = (1.0 + alpha) * (1.0 + z_arr)**3
        den = 1.0 + alpha * (1.0 + z_arr)**3
        return num / den - 1.0, alpha  # delta_norm, alpha

    def build_E_fn(theory_tag):

        # =====================================================================
        # GROUP FA: Fundamental Annihilation
        # delta = f * Gamma_norm(z), Gamma_norm = (1+alpha)(1+z)^3/(1+alpha(1+z)^3) - 1
        # Physical: SQ annihilation energy feeds dark energy;
        #   C1 ensures radiation (T^mu_mu=0) decouples automatically.
        #   alpha = Om/OL0 is the only new scale (derived from A1+A2 balance).
        # =====================================================================

        if theory_tag == 'FA01':
            # f = 0.5: half the annihilation energy stored as DE
            # Physical: SQ -> 2 channels (SQ reservoir + DE); equal partition
            f = 0.5
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                delta, _ = sqt_gamma_norm(z_arr, Om, OR_W)
                if delta is None: return None
                rho_DE = OL0 * (1.0 + f * delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'FA02':
            # f = 1/3: 1/3 from 3D spatial annihilation channels
            f = 1.0 / 3.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                delta, _ = sqt_gamma_norm(z_arr, Om, OR_W)
                if delta is None: return None
                rho_DE = OL0 * (1.0 + f * delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'FA03':
            # f = 1/pi: quantum phase normalization (half-cycle)
            f = 1.0 / math.pi
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                delta, _ = sqt_gamma_norm(z_arr, Om, OR_W)
                if delta is None: return None
                rho_DE = OL0 * (1.0 + f * delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'FA04':
            # f = 1/e: Boltzmann suppression at the matter-DE equilibrium
            f = 1.0 / math.e
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                delta, _ = sqt_gamma_norm(z_arr, Om, OR_W)
                if delta is None: return None
                rho_DE = OL0 * (1.0 + f * delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'FA05':
            # f = OL0 (dynamically computed): DE fraction drives its own growth
            # Physical: generation rate proportional to available DE volume
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                delta, _ = sqt_gamma_norm(z_arr, Om, OR_W)
                if delta is None: return None
                f = OL0
                rho_DE = OL0 * (1.0 + f * delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'FA06':
            # f = Om: matter fraction drives annihilation DE coupling
            # Physical: more matter -> more annihilation -> more DE
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                delta, _ = sqt_gamma_norm(z_arr, Om, OR_W)
                if delta is None: return None
                f = Om
                rho_DE = OL0 * (1.0 + f * delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'FA07':
            # f = sqrt(Om * OL0): geometric mean -- balanced coupling
            # Physical: two-body SQ+matter interaction amplitude scales as sqrt product
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                delta, _ = sqt_gamma_norm(z_arr, Om, OR_W)
                if delta is None: return None
                f = math.sqrt(Om * OL0)
                rho_DE = OL0 * (1.0 + f * delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'FA08':
            # f = 1/(1+alpha): normalized to psi* range [0,1]
            # Physical: annihilation DE bounded by full depletion limit
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                delta, alpha = sqt_gamma_norm(z_arr, Om, OR_W)
                if delta is None: return None
                f = 1.0 / (1.0 + alpha)
                rho_DE = OL0 * (1.0 + f * delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        # =====================================================================
        # GROUP GB: Generation-Balance variants
        # Based on psi*(z) = 1/(1+alpha*(1+z)^3) equilibrium.
        # Different physical channels: radiation correction, two-scale, etc.
        # =====================================================================

        elif theory_tag == 'GB01':
            # C1 radiation correction: radiation has T^mu_mu=0 so it doesn't
            # annihilate SQ. Effective alpha should exclude radiation contribution.
            # alpha_eff = (Om - Or_eff) / OL0 where Or_eff is from C1 decoupling.
            # Radiation correction at z>z_eq_r; use alpha_matter = (Om - Or) / OL0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                # C1: radiation decouples -> effective matter coupling
                Om_matter = Om - OR_W  # radiation-corrected matter
                if Om_matter <= 0: Om_matter = Om
                alpha = Om_matter / OL0
                num = (1.0 + alpha) * (1.0 + z_arr)**3
                den = 1.0 + alpha * (1.0 + z_arr)**3
                delta = 0.5 * (num / den - 1.0)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'GB02':
            # Two-channel: matter (3D, n=3) + vacuum energy (0D, constant channel)
            # delta = f1*Gamma_norm_m + f2*Gamma_norm_vac
            # Gamma_norm_vac = 0 (vacuum energy doesn't annihilate SQ by A1)
            # Net: only matter channel, but with f = OL0/(Om+OL0)
            # Physical: generation from vacuum reservoir, balance at z_vac = (OL0/Om)^(1/3)-1
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                alpha = Om / OL0
                # Primary matter channel
                delta_m = 0.5 * ((1.0+alpha)*(1.0+z_arr)**3 / (1.0+alpha*(1.0+z_arr)**3) - 1.0)
                # Secondary: psi depletion drives vacuum restoring force
                # psi*(z)/psi*(0) = (1+alpha)/(1+alpha*(1+z)^3)
                # Vacuum restoring: delta_vac = f_vac * (1 - psi*(z)/psi*(0))
                f_vac = 1.0 / (2.0 * math.pi)
                psi_ratio = (1.0 + alpha) / (1.0 + alpha*(1.0+z_arr)**3)
                delta_vac = f_vac * (1.0 - psi_ratio)
                delta = delta_m + delta_vac
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'GB03':
            # psi saturation: equilibrium point shifts at matter-radiation equality
            # At z_eq_r = Om/Or - 1 (~3400), radiation also suppressed.
            # For z << z_eq_r: alpha_eff = Om/OL0 (pure matter)
            # Introduce soft cutoff: alpha_eff(z) = alpha_m * tanh(z_eq_r/z) (approx = alpha_m for low z)
            # For BAO z range (z<2.3): radiation negligible, but add alpha_r correction
            alpha_r_frac = OR_W / 0.3  # radiation fraction of matter
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                alpha_m = Om / OL0
                # Small radiation correction to alpha
                alpha_eff = alpha_m * (1.0 + alpha_r_frac * (1.0+z_arr))
                num = (1.0 + alpha_eff) * (1.0 + z_arr)**3
                den = 1.0 + alpha_eff * (1.0 + z_arr)**3
                delta = 0.5 * (num / den - 1.0)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'GB04':
            # Square-root Gamma_norm: slower saturation (diffusion-limited annihilation)
            # Physical: SQ annihilation in 3D diffusion regime -> sqrt scaling
            # delta = f * sqrt(Gamma_norm(z))
            f = 0.5
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                delta_raw, _ = sqt_gamma_norm(z_arr, Om, OR_W)
                if delta_raw is None: return None
                delta = f * np.sqrt(np.maximum(delta_raw, 0.0))
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'GB05':
            # Quadratic Gamma_norm: two-body annihilation (A1 is two-body process)
            # Physical: Gamma_ann = sigma*rho_m*rho_st -> 2nd order in densities
            # Near z=0, quadratic -> smaller correction; saturates more sharply
            f = 0.5
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                delta_raw, _ = sqt_gamma_norm(z_arr, Om, OR_W)
                if delta_raw is None: return None
                delta = f * delta_raw**2
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'GB06':
            # Logarithmic Gamma_norm: slower-than-linear saturation
            # Physical: log growth from cascaded secondary annihilation events
            # delta = f * log(1 + Gamma_norm(z)) / log(1 + Gamma_norm(inf))
            f = 0.5
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                alpha = Om / OL0
                delta_raw, _ = sqt_gamma_norm(z_arr, Om, OR_W)
                if delta_raw is None: return None
                sat_level = 1.0 / alpha  # Gamma_norm saturation at z->inf
                norm = math.log1p(sat_level)
                if norm <= 0: return None
                delta = f * np.log1p(np.maximum(delta_raw, 0.0)) / norm
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'GB07':
            # B' scenario: Friedmann from net generation rate
            # psi_dot = kappa*(1-psi) - sigma*rho_m*psi = kappa*(1-psi*)
            # In adiabatic limit: psi = psi*(z) tracks equilibrium
            # Net rate = 0 at equilibrium, but Hubble from psi depletion:
            # H^2 ~ H0^2 * [standard + f*(psi*(0) - psi*(z)) / (1-psi*(0))]
            # = H0^2 * [std + f * alpha*((1+z)^3-1)/(1+alpha)]
            f = 0.5
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                alpha = Om / OL0
                # psi*(0) = 1/(1+alpha), psi*(z) = 1/(1+alpha*(1+z)^3)
                psi0 = 1.0 / (1.0 + alpha)
                psi_z = 1.0 / (1.0 + alpha * (1.0+z_arr)**3)
                # DE modification: psi depletion drives extra expansion
                # normalize by (1-psi*(0)) = alpha/(1+alpha)
                norm = alpha / (1.0 + alpha)
                delta = f * (psi0 - psi_z) / norm
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'GB08':
            # Asymmetric B': generation regime (z<z_eq) vs annihilation regime (z>z_eq)
            # A4: three regimes from SQT. Balance at z_eq = (OL0/Om)^(1/3)-1.
            # Below z_eq: generation dominant -> slower delta growth (f_gen)
            # Above z_eq: annihilation dominant -> faster delta growth (f_ann)
            # From SQT: f_gen = OL0/(Om+OL0), f_ann = Om/(Om+OL0)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                alpha = Om / OL0
                z_eq = (OL0/Om)**(1.0/3.0) - 1.0
                if z_eq <= 0: z_eq = 0.3
                f_gen = OL0 / (Om + OL0)  # generation fraction
                f_ann = Om  / (Om + OL0)  # annihilation fraction
                # Smooth weight: w=1 past z_eq (annihilation), w=0 future (generation)
                sigma_w = z_eq / 4.0
                w = 0.5 * (1.0 + np.tanh((z_arr - z_eq) / sigma_w))
                f_eff = f_gen * (1.0 - w) + f_ann * w
                delta_raw, _ = sqt_gamma_norm(z_arr, Om, OR_W)
                if delta_raw is None: return None
                delta = f_eff * delta_raw
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        # =====================================================================
        # GROUP VG: V(psi) Ginzburg-Landau potential
        # V(psi) = (1/2)*mu^2*(psi-1)^2 + (gamma/6)*(psi-1)^3
        # psi*(z) = 1/(1+alpha*(1+z)^3) -- SQT equilibrium field
        # delta from: rho_DE = OL0*(1 + V_correction)
        # =====================================================================

        elif theory_tag == 'VG01':
            # Pure GL quadratic: V(psi) = (1/2)*mu^2*(psi-1)^2
            # psi deviation from 1 drives dark energy
            # rho_DE_extra = (mu^2/2)*(psi*-1)^2 * OL0
            # mu^2 = 1 (natural units, dimensionless SQT coupling)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                alpha = Om / OL0
                psi_z = 1.0 / (1.0 + alpha * (1.0+z_arr)**3)
                psi_0 = 1.0 / (1.0 + alpha)
                # delta from V(psi): quadratic potential energy
                dpsi = psi_z - 1.0  # psi deviation from equilibrium (negative)
                dpsi0 = psi_0 - 1.0
                # V normalized: V(psi*(z)) - V(psi*(0)) gives z-dependent DE correction
                delta = 0.5 * (dpsi**2 - dpsi0**2) / psi_0**2
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'VG02':
            # GL quadratic with amplitude f=0.5
            # delta = f * (dpsi^2 - dpsi0^2) normalized differently
            f = 0.5
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                alpha = Om / OL0
                psi_z = 1.0 / (1.0 + alpha * (1.0+z_arr)**3)
                psi_0 = 1.0 / (1.0 + alpha)
                dpsi   = psi_z - 1.0
                dpsi0  = psi_0 - 1.0
                # Normalized: (dpsi^2 - dpsi0^2) / dpsi0^2
                if abs(dpsi0) < 1e-10: return None
                delta = f * (dpsi**2 - dpsi0**2) / dpsi0**2
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'VG03':
            # GL cubic: V = (1/2)mu^2*(psi-1)^2 + (gamma/6)*(psi-1)^3
            # gamma = 1 (cubic term same order as quadratic)
            # Physical: next-order GL expansion captures asymmetry (black hole singularity avoidance)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                alpha = Om / OL0
                psi_z = 1.0 / (1.0 + alpha * (1.0+z_arr)**3)
                psi_0 = 1.0 / (1.0 + alpha)
                dpsi  = psi_z - 1.0
                dpsi0 = psi_0 - 1.0
                if abs(dpsi0) < 1e-10: return None
                V_z  = 0.5 * dpsi**2  + (1.0/6.0) * dpsi**3
                V_0  = 0.5 * dpsi0**2 + (1.0/6.0) * dpsi0**3
                delta = (V_z - V_0) / (0.5 * dpsi0**2)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'VG04':
            # V(psi): Mexican-hat type near psi=1 (spontaneous symmetry breaking analog)
            # V = (psi-1)^2 * (1 - psi)  [zero at psi=0, psi=1, max in between]
            # Physical: SQ vacuum has metastable state at psi=0 (BH) and true vacuum at psi=1
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                alpha = Om / OL0
                psi_z = 1.0 / (1.0 + alpha * (1.0+z_arr)**3)
                psi_0 = 1.0 / (1.0 + alpha)
                V_z  = (psi_z - 1.0)**2 * (1.0 - psi_z)
                V_0  = (psi_0 - 1.0)**2 * (1.0 - psi_0)
                norm  = (psi_0 - 1.0)**2  # ~ alpha^2/(1+alpha)^2
                if abs(norm) < 1e-10: return None
                delta = (V_z - V_0) / norm
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'VG05':
            # V(psi) = 1 - exp(-(psi-1)^2 / 2sigma^2), sigma = alpha/(1+alpha)
            # Gaussian well: smooth attractor to psi=1
            # Physical: quantum fluctuations give Gaussian distribution around equilibrium
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                alpha = Om / OL0
                psi_z = 1.0 / (1.0 + alpha * (1.0+z_arr)**3)
                psi_0 = 1.0 / (1.0 + alpha)
                sigma2 = (alpha / (1.0 + alpha))**2
                if sigma2 < 1e-10: return None
                V_z = 1.0 - np.exp(-(psi_z - 1.0)**2 / (2.0 * sigma2))
                V_0 = 1.0 - math.exp(-(psi_0 - 1.0)**2 / (2.0 * sigma2))
                norm = V_0
                if abs(norm) < 1e-10: return None
                delta = (V_z - V_0) / norm
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'VG06':
            # G_eff modification: L3 Lagrangian -> G_eff = G/psi
            # Friedmann: H^2 = (8piG/3) * rho_total / psi*(z)
            # E^2 = [Om*(1+z)^3 + Or*(1+z)^4 + OL0] / psi*(z)
            # But need E(0)=1: E^2 = [...] / psi*(z) * psi*(0)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                alpha = Om / OL0
                psi_z = 1.0 / (1.0 + alpha * (1.0+z_arr)**3)
                psi_0 = 1.0 / (1.0 + alpha)
                if psi_0 < 1e-10: return None
                rho_std = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
                E2 = rho_std * psi_0 / psi_z
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'VG07':
            # G_eff + DE coupling: combination of G_eff and Gamma_norm corrections
            # E^2 = [Om*(1+z)^3/psi + OL0*(1 + f*delta)] where psi from SQT
            # f=1/3, matter feels G_eff, DE has own correction
            f = 1.0 / 3.0
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                alpha = Om / OL0
                psi_z = 1.0 / (1.0 + alpha * (1.0+z_arr)**3)
                psi_0 = 1.0 / (1.0 + alpha)
                if psi_0 < 1e-10: return None
                delta_raw, _ = sqt_gamma_norm(z_arr, Om, OR_W)
                if delta_raw is None: return None
                # Matter + radiation feel G_eff, DE has Gamma_norm correction
                rho_m_geff = (OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3) * psi_0 / psi_z
                rho_DE = OL0 * (1.0 + f * delta_raw)
                E2 = rho_m_geff + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'VG08':
            # V(psi) = (psi-1)^2 * exp(-psi): singularity-safe potential
            # Goes to zero at psi=1, finite at psi=0, no divergence
            # Physical: exponential suppression ensures finite SQ density always
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                alpha = Om / OL0
                psi_z = 1.0 / (1.0 + alpha * (1.0+z_arr)**3)
                psi_0 = 1.0 / (1.0 + alpha)
                V_z = (psi_z - 1.0)**2 * np.exp(-psi_z)
                V_0 = (psi_0 - 1.0)**2 * math.exp(-psi_0)
                norm = (psi_0 - 1.0)**2
                if abs(norm) < 1e-10: return None
                delta = (V_z - V_0) / norm
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        # =====================================================================
        # GROUP MC: Multi-Channel SQT
        # Combining Gamma_norm with additional physical channels.
        # =====================================================================

        elif theory_tag == 'MC01':
            # Ricci+Weyl dual: annihilation (Ricci, local) + rearrangement (Weyl, nonlocal)
            # Ricci channel: delta_R = f_R * Gamma_norm (matter annihilation)
            # Weyl channel: delta_W = f_W * rho_DE_driven (void rearrangement)
            # f_R = 1/3, f_W = 1/(3*pi) (Weyl suppressed by quantum phase)
            f_R = 1.0 / 3.0
            f_W = 1.0 / (3.0 * math.pi)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                delta_raw, alpha = sqt_gamma_norm(z_arr, Om, OR_W)
                if delta_raw is None: return None
                # Weyl channel: grows as sqrt of Ricci (nonlocal damping)
                delta_R = f_R * delta_raw
                delta_W = f_W * np.sqrt(np.maximum(delta_raw, 0.0))
                delta = delta_R + delta_W
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'MC02':
            # Two-scale SQT: matter scale (alpha1=Om/OL0) + Hubble crossing scale (alpha2=Om^(1/2))
            # Physical: SQ annihilation has two channels at different z-scales
            # f1=1/3, f2=1/(3*pi)
            f1 = 1.0 / 3.0
            f2 = 1.0 / (3.0 * math.pi)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                alpha1 = Om / OL0
                alpha2 = math.sqrt(Om)  # Hubble crossing scale
                num1 = (1.0+alpha1)*(1.0+z_arr)**3
                den1 = 1.0 + alpha1*(1.0+z_arr)**3
                delta1 = f1 * (num1/den1 - 1.0)
                num2 = (1.0+alpha2)*(1.0+z_arr)**3
                den2 = 1.0 + alpha2*(1.0+z_arr)**3
                delta2 = f2 * (num2/den2 - 1.0)
                delta = delta1 + delta2
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'MC03':
            # Gamma_norm + erf correction (A12 erf diffusion canonical class from L5)
            # A12 is: delta = f*erf(z/z_eq)
            # Physical: SQT generates A12 via diffusion in psi field (§8 MSR)
            # delta = f1*Gamma_norm + f2*erf(z/z_eq)
            f1 = 0.4
            f2 = 0.1
            def E_fn(z_arr, Om):
                from scipy.special import erf
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                z_eq = (OL0/Om)**(1.0/3.0) - 1.0
                if z_eq <= 0: z_eq = 0.3
                delta_raw, _ = sqt_gamma_norm(z_arr, Om, OR_W)
                if delta_raw is None: return None
                delta = f1*delta_raw + f2*erf(z_arr/z_eq)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'MC04':
            # Gamma_norm + tanh (DD06 champion) superposition
            # Physical: SQT Gamma_norm is exact; tanh captures phenomenological correction
            # delta = f1*Gamma_norm + f2*tanh(z/z_eq)
            f1 = 0.35
            f2 = 0.15
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                z_eq = (OL0/Om)**(1.0/3.0) - 1.0
                if z_eq <= 0: z_eq = 0.3
                delta_raw, _ = sqt_gamma_norm(z_arr, Om, OR_W)
                if delta_raw is None: return None
                delta = f1*delta_raw + f2*np.tanh(z_arr/z_eq)
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'MC05':
            # Three-regime A4 + SQT equilibrium
            # Below z_eq: Gamma_norm_gen (generation dominated, f_gen)
            # Above z_eq: Gamma_norm_ann (annihilation dominated, f_ann)
            # At z_eq: balance
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                alpha = Om / OL0
                z_eq = (OL0/Om)**(1.0/3.0) - 1.0
                if z_eq <= 0: z_eq = 0.3
                f_gen = OL0 / (Om + OL0)
                f_ann = Om  / (Om + OL0)
                sigma_w = z_eq / 3.0
                w = 0.5 * (1.0 + np.tanh((z_arr - z_eq)/sigma_w))
                f_eff = f_gen*(1.0-w) + f_ann*w
                # Add Gaussian peak at z_eq (A4 balance point signature)
                A_peak = 1.0 / (2.0*math.pi)
                peak = A_peak * np.exp(-0.5*((z_arr-z_eq)/(z_eq/2.0))**2)
                delta_raw, _ = sqt_gamma_norm(z_arr, Om, OR_W)
                if delta_raw is None: return None
                delta = f_eff * delta_raw + peak
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
                return np.sqrt(np.maximum(E2, 1e-30))
            return E_fn

        elif theory_tag == 'MC06':
            # Full SQT + V(psi): Gamma_norm + GL correction
            # delta = f_ann*Gamma_norm + f_GL*(dpsi^2 - dpsi0^2)/norm_GL
            # Physical: L3 Lagrangian has both SQ annihilation and V(psi) terms
            f_ann = 1.0 / 3.0
            f_GL  = 1.0 / (3.0 * math.pi)
            def E_fn(z_arr, Om):
                OL0 = 1.0 - Om - OR_W
                if OL0 <= 0: return None
                alpha = Om / OL0
                psi_z = 1.0 / (1.0 + alpha * (1.0+z_arr)**3)
                psi_0 = 1.0 / (1.0 + alpha)
                dpsi  = psi_z - 1.0
                dpsi0 = psi_0 - 1.0
                if abs(dpsi0) < 1e-10: return None
                delta_raw, _ = sqt_gamma_norm(z_arr, Om, OR_W)
                if delta_raw is None: return None
                delta_ann = f_ann * delta_raw
                delta_GL  = f_GL  * (dpsi**2 - dpsi0**2) / dpsi0**2
                delta = delta_ann + delta_GL
                rho_DE = OL0 * (1.0 + delta)
                rho_DE = np.maximum(rho_DE, 1e-10)
                E2 = OR_W*(1+z_arr)**4 + Om*(1+z_arr)**3 + rho_DE
                if not np.all(np.isfinite(E2)) or np.any(E2 < 0): return None
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
        [0.35, 65.0],  [0.36, 63.0],
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

        try:
            bounds_de = [(0.20, 0.50), (60.0, 80.0)]
            res_de = differential_evolution(
                lambda p, ef=E_fn: chi2_w(p, ef),
                bounds=bounds_de,
                maxiter=300,
                tol=1e-6,
                seed=42,
                workers=1,
                popsize=10,
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

        # Estimate wa via CPL fit to rho_DE(z) profile
        try:
            z_test = np.linspace(0.01, 2.0, 20)
            E_test = E_fn(z_test, Om_best)
            wa_est = 0.0
            if E_test is not None and np.all(np.isfinite(E_test)):
                rho_m0  = Om_best
                rho_r0  = OR_W
                rde = E_test**2 - rho_r0*(1+z_test)**4 - rho_m0*(1+z_test)**3
                rde0_pt = float(E_fn(np.array([0.0]), Om_best)[0]**2 - rho_m0 - rho_r0)
                if rde0_pt > 0 and np.all(rde > 0):
                    # w(z) = dlnrho_DE / (-3*dlna) - 1
                    lna  = -np.log(1.0 + z_test)
                    lnrde = np.log(rde / rde0_pt)
                    # CPL: w = w0 + wa*z/(1+z)
                    # lnrde = -3*(1+w0)*lna - 3*wa*(ln(1+z)+z/(1+z)-... approx)
                    # Simplified fit: linear in lna
                    from numpy.polynomial import polynomial as P
                    A = np.column_stack([np.ones_like(lna), lna, lna**2])
                    coef, *_ = np.linalg.lstsq(A, lnrde, rcond=None)
                    # d(lnrde)/d(lna) = coef[1] + 2*coef[2]*lna
                    # at z=0 (lna=0): slope = coef[1] = -3*(1+w_eff_0)
                    slope_0 = coef[1]
                    w0_est  = -1.0 - slope_0 / 3.0
                    # at z=1 (lna=-log2): slope = coef[1] + 2*coef[2]*(-log2)
                    slope_1 = coef[1] + 2.0*coef[2]*(-math.log(2.0))
                    w1_est  = -1.0 - slope_1 / 3.0
                    # wa = w(z=1) - w(z=0) ... rough estimate
                    wa_est = float(w1_est - w0_est)
        except Exception:
            wa_est = 0.0

        status = 'PASS' if (aicc_best < LCDM_AICC) else 'KILL'
        return {
            'id': wid, 'name': theory_name, 'k': k,
            'chi2': chi2_best, 'aicc': aicc_best, 'd_aicc': d_aicc,
            'Om': Om_best, 'H0': H0_best,
            'wa_est': wa_est, 'status': status
        }

    except Exception as e:
        return {'id': wid, 'name': theory_name, 'k': k,
                'chi2': 1e8, 'aicc': 1e8, 'd_aicc': 1e8,
                'Om': None, 'H0': None,
                'status': f'ERROR:{e}'}


# ==============================================================================
# THEORY DEFINITIONS
# ==============================================================================

def build_sqt_tasks():
    tasks = []

    # GROUP FA: Fundamental Annihilation (FA01-FA08)
    tasks.append(('FA01', 'SQT-Ann: f=0.5, Gamma_norm(z) from A1+A2 equilibrium', 2, {'tag': 'FA01'}))
    tasks.append(('FA02', 'SQT-Ann: f=1/3 (3D spatial channels)', 2, {'tag': 'FA02'}))
    tasks.append(('FA03', 'SQT-Ann: f=1/pi (quantum phase normalization)', 2, {'tag': 'FA03'}))
    tasks.append(('FA04', 'SQT-Ann: f=1/e (Boltzmann suppression at z_eq)', 2, {'tag': 'FA04'}))
    tasks.append(('FA05', 'SQT-Ann: f=OL0 (DE-fraction weighted coupling)', 2, {'tag': 'FA05'}))
    tasks.append(('FA06', 'SQT-Ann: f=Om (matter-fraction weighted coupling)', 2, {'tag': 'FA06'}))
    tasks.append(('FA07', 'SQT-Ann: f=sqrt(Om*OL0) geometric mean coupling', 2, {'tag': 'FA07'}))
    tasks.append(('FA08', 'SQT-Ann: f=1/(1+alpha) normalized to psi* range', 2, {'tag': 'FA08'}))

    # GROUP GB: Generation-Balance variants (GB01-GB08)
    tasks.append(('GB01', 'SQT-GB: C1 radiation-corrected alpha_eff, f=0.5', 2, {'tag': 'GB01'}))
    tasks.append(('GB02', 'SQT-GB: two-channel matter+vacuum, psi depletion', 2, {'tag': 'GB02'}))
    tasks.append(('GB03', 'SQT-GB: radiation correction alpha(z)', 2, {'tag': 'GB03'}))
    tasks.append(('GB04', 'SQT-GB: sqrt(Gamma_norm) diffusion-limited', 2, {'tag': 'GB04'}))
    tasks.append(('GB05', 'SQT-GB: Gamma_norm^2 two-body process', 2, {'tag': 'GB05'}))
    tasks.append(('GB06', 'SQT-GB: log(1+Gamma_norm) cascaded annihilation', 2, {'tag': 'GB06'}))
    tasks.append(('GB07', 'SQT-B\': psi depletion drives Hubble f=0.5', 2, {'tag': 'GB07'}))
    tasks.append(('GB08', 'SQT-B\': A4 asymmetric gen/ann regimes', 2, {'tag': 'GB08'}))

    # GROUP VG: V(psi) Ginzburg-Landau (VG01-VG08)
    tasks.append(('VG01', 'SQT-GL: V=(psi-1)^2/2 quadratic potential', 2, {'tag': 'VG01'}))
    tasks.append(('VG02', 'SQT-GL: V quad normalized f=0.5', 2, {'tag': 'VG02'}))
    tasks.append(('VG03', 'SQT-GL: V cubic (1/2)(psi-1)^2+(1/6)(psi-1)^3', 2, {'tag': 'VG03'}))
    tasks.append(('VG04', 'SQT-GL: V=(psi-1)^2*(1-psi) Mexican-hat analog', 2, {'tag': 'VG04'}))
    tasks.append(('VG05', 'SQT-GL: V=1-exp(-(psi-1)^2/2sigma^2) Gaussian well', 2, {'tag': 'VG05'}))
    tasks.append(('VG06', 'SQT-GL: G_eff=G/psi*(z) L3 Lagrangian modification', 2, {'tag': 'VG06'}))
    tasks.append(('VG07', 'SQT-GL: G_eff + Gamma_norm DE coupling combined', 2, {'tag': 'VG07'}))
    tasks.append(('VG08', 'SQT-GL: V=(psi-1)^2*exp(-psi) singularity-safe', 2, {'tag': 'VG08'}))

    # GROUP MC: Multi-Channel SQT (MC01-MC06)
    tasks.append(('MC01', 'SQT-MC: Ricci(f=1/3) + Weyl(f=1/(3pi)) dual channels', 2, {'tag': 'MC01'}))
    tasks.append(('MC02', 'SQT-MC: two-scale alpha1=Om/OL + alpha2=sqrt(Om)', 2, {'tag': 'MC02'}))
    tasks.append(('MC03', 'SQT-MC: Gamma_norm(0.4) + erf@z_eq(0.1)', 2, {'tag': 'MC03'}))
    tasks.append(('MC04', 'SQT-MC: Gamma_norm(0.35) + tanh@z_eq(0.15)', 2, {'tag': 'MC04'}))
    tasks.append(('MC05', 'SQT-MC: A4 three-regime + Gaussian@z_eq peak', 2, {'tag': 'MC05'}))
    tasks.append(('MC06', 'SQT-MC: Gamma_norm(1/3) + GL-V(1/(3pi)) L3 full', 2, {'tag': 'MC06'}))

    return tasks


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print('=' * 70)
    print('L31 SQT-derived theories: FA/GB/VG/MC (30 theories)')
    print('=' * 70)
    print()
    print('Theory framework: Spacetime Quanta Theory (SQT)')
    print('  A1+A2 -> psi*(z) = 1/(1+alpha*(1+z)^3), alpha = Om/OL0')
    print('  Core: Gamma_norm(z) = (1+alpha)(1+z)^3/(1+alpha(1+z)^3) - 1')
    print()
    print('Group FA (FA01-FA08): Fundamental Annihilation amplitude variants')
    print('Group GB (GB01-GB08): Generation-Balance B-prime scenario')
    print('Group VG (VG01-VG08): V(psi) Ginzburg-Landau potential')
    print('Group MC (MC01-MC06): Multi-channel SQT combinations')
    print()
    print(f'LCDM baseline: chi2={LCDM_BASELINE_CHI2}, AICc={LCDM_BASELINE_AICC}')
    print()

    tasks = build_sqt_tasks()
    worker_args = [
        (t[0], t[1], t[2], 'sqt', t[3])
        for t in tasks
    ]
    print(f'Theories to test: {len(worker_args)}')
    print()

    print('Launching 9-worker multiprocessing pool (spawn)...')
    ctx = multiprocessing.get_context('spawn')
    with ctx.Pool(processes=9) as pool:
        raw_results = pool.map(worker_fn, worker_args)

    raw_results.sort(key=lambda r: r['aicc'])

    print()
    print('=' * 70)
    print('RESULTS sorted by AICc:')
    print('=' * 70)
    print(f"{'ID':>5} {'Theory':42s} {'k':>2} {'chi2':>9} {'AICc':>9} {'dAICc':>8} {'wa':>7} {'Status':>7}")
    print('-' * 96)

    pass_count = 0
    kill_count = 0
    champion   = None

    for r in raw_results:
        if r['status'] == 'PASS':
            pass_count += 1
            if champion is None or r['aicc'] < champion['aicc']:
                champion = r
        elif 'KILL' in str(r['status']):
            kill_count += 1

        chi2_s = f"{r['chi2']:.4f}"    if r['chi2']   < 1e7 else '  FAIL  '
        aicc_s = f"{r['aicc']:.4f}"    if r['aicc']   < 1e7 else '  FAIL  '
        dacc_s = f"{r['d_aicc']:+.4f}" if r['d_aicc'] < 1e7 else '  FAIL  '
        wa_s   = f"{r.get('wa_est', 0.0):+.4f}"
        print(f"{r['id']:>5} {r['name'][:42]:42s} {r['k']:>2} "
              f"{chi2_s:>9} {aicc_s:>9} {dacc_s:>8} {wa_s:>7} {r['status']:>7}")

    print()
    print(f'PASS: {pass_count}  /  KILL: {kill_count}')
    if champion:
        print(f"Champion: {champion['id']} | dAICc={champion['d_aicc']:.4f} | "
              f"chi2={champion['chi2']:.4f} | wa={champion.get('wa_est',0.0):.4f} | "
              f"Om={champion['Om']:.4f} | H0={champion['H0']:.4f}")
    print()

    out_json = os.path.join(_SCRIPT_DIR, 'l31_results.json')

    def jsonify(obj):
        if isinstance(obj, (np.integer,)):  return int(obj)
        if isinstance(obj, (np.floating,)): return float(obj)
        if isinstance(obj, np.ndarray):     return obj.tolist()
        if isinstance(obj, dict):           return {kk: jsonify(vv) for kk, vv in obj.items()}
        if isinstance(obj, (list, tuple)):  return [jsonify(v) for v in obj]
        return obj

    save_data = {
        'run': 'L31-SQT-FA-GB-VG-MC',
        'description': 'SQT-derived theories: Fundamental Annihilation, Generation-Balance, V(psi) GL, Multi-channel',
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
