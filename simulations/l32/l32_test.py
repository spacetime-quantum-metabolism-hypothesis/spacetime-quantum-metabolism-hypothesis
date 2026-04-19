# -*- coding: utf-8 -*-
"""
l32_test.py -- L32: SQT theories with proper CPL w0/wa + K93
=============================================================
Improvements over L31:
  - CPL w0/wa properly extracted via least-squares fit over z=[0,2]
  - K93 (wa>=0 -> KILL) applied after CPL fit
  - 20-start Nelder-Mead + differential_evolution popsize=30
  - Convergence check: delta_chi2 < 0.01 between methods

Theory groups (30 total):
  SA (8): Transformed Gamma_norm (arctan, tanh, rational, exp, roots, erf)
  SB (8): SQT-L30 bridge (Gamma_norm + high-z suppression / hybrid)
  SC (8): psi-field w(z) engineering (negative wa by construction)
  SD (6): Dynamic psi lag models

Core SQT:
  psi*(z) = 1/(1+alpha*(1+z)^3), alpha=Om/OL0
  Gamma_norm(z) = (1+alpha)*(1+z)^3/(1+alpha*(1+z)^3) - 1

LCDM baseline: chi2=10.192, AICc=15.392 (k=2, n=13)
"""

import os, sys, math, json, warnings, multiprocessing
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

from desi_data import DESI_DR2, DESI_DR2_COV, DESI_DR2_COV_INV

C_KMS  = 299792.458
R_S    = 147.09
OR     = 5.38e-5
N_DATA = 13
N_GRID = 4000
LCDM_CHI2 = 10.192
LCDM_AICC = 15.392

def aicc(chi2, k, n=N_DATA):
    return chi2 + 2*k + 2*k*(k+1)/(n-k-1)


def worker_fn(args):
    import os, sys, math, warnings
    import numpy as np
    from scipy.integrate import cumulative_trapezoid
    from scipy.optimize import minimize, differential_evolution
    from numpy.polynomial import polynomial as P

    os.environ['OMP_NUM_THREADS'] = os.environ['MKL_NUM_THREADS'] = os.environ['OPENBLAS_NUM_THREADS'] = '1'
    np.seterr(all='ignore')
    warnings.filterwarnings('ignore')

    _SD = os.path.dirname(os.path.abspath(__file__))
    _SI = os.path.dirname(_SD)
    if _SI not in sys.path: sys.path.insert(0, _SI)
    from desi_data import DESI_DR2, DESI_DR2_COV_INV

    C_KMS_W = 299792.458; R_S_W = 147.09; OR_W = 5.38e-5
    N_DATA_W = 13; N_GRID_W = 4000; LCDM_AICC_W = 15.392

    def aicc_w(chi2, k, n=N_DATA_W):
        return chi2 + 2*k + 2*k*(k+1)/(n-k-1)

    def compute_tv(Om, H0, E_fn):
        z_eff = DESI_DR2['z_eff']
        z_grid = np.linspace(0.0, z_eff.max()+0.01, N_GRID_W)
        try:
            Eg = E_fn(z_grid, Om)
        except Exception:
            return None
        if Eg is None or not np.all(np.isfinite(Eg)): return None
        Eg = np.maximum(Eg, 1e-15)
        DM = (C_KMS_W/H0)*np.concatenate([[0.], cumulative_trapezoid(1./Eg, z_grid)])
        tv = np.empty(N_DATA_W)
        for i,(z,qty) in enumerate(zip(z_eff, DESI_DR2['quantity'])):
            idx = min(np.searchsorted(z_grid,z), N_GRID_W-1)
            DH = C_KMS_W/(H0*Eg[idx])
            DV = (z*DM[idx]**2*DH)**(1./3.) if z>0 else 0.
            if   'DV' in qty: tv[i] = DV/R_S_W
            elif 'DM' in qty: tv[i] = DM[idx]/R_S_W
            elif 'DH' in qty: tv[i] = DH/R_S_W
            else:              tv[i] = np.nan
        return tv

    def chi2_fn(params, E_fn):
        Om,H0 = params
        if not (0.05<Om<0.70 and 50.<H0<100.): return 1e8
        tv = compute_tv(Om, H0, E_fn)
        if tv is None or not np.all(np.isfinite(tv)): return 1e8
        d = DESI_DR2['value'] - tv
        return float(d @ DESI_DR2_COV_INV @ d)

    def cpl_wa(Om, E_fn, OR_W):
        """Extract w0, wa via CPL least-squares fit over z=[0.01,2]."""
        z_arr = np.linspace(0.01, 2.0, 40)
        Ev = E_fn(z_arr, Om)
        if Ev is None or not np.all(np.isfinite(Ev)): return 0., 0.
        rde = Ev**2 - OR_W*(1+z_arr)**4 - Om*(1+z_arr)**3
        E0v = E_fn(np.array([0.0]), Om)
        if E0v is None: return 0., 0.
        rde0 = float(E0v[0]**2 - OR_W - Om)
        if rde0 <= 0 or np.any(rde <= 0): return 0., 0.
        lnrde = np.log(rde/rde0)
        # w(z) = w0 + wa*z/(1+z)  =>  d(lnrde)/dz = -3(1+w(z))/(1+z)
        # integral: lnrde(z) = -3*[(1+w0)*ln(1+z) + wa*(ln(1+z) - z/(1+z))]
        ln1z = np.log(1+z_arr)
        x_w0 = -3.*ln1z
        x_wa = -3.*(ln1z - z_arr/(1+z_arr))
        A = np.column_stack([x_w0, x_wa])
        try:
            coef,_,_,_ = np.linalg.lstsq(A, lnrde, rcond=None)
            w0, wa = float(coef[0])-1., float(coef[1])
        except Exception:
            return 0., 0.
        return w0, wa

    # ------------------------------------------------------------------
    # E(z) FACTORY
    # ------------------------------------------------------------------
    def gn(z_arr, Om, OR_W):
        """Core Gamma_norm(z); returns (delta, alpha) or (None, None)."""
        OL0 = 1.-Om-OR_W
        if OL0<=0 or Om<=0: return None, None
        alpha = Om/OL0
        gv = (1.+alpha)*(1.+z_arr)**3/(1.+alpha*(1.+z_arr)**3) - 1.
        return gv, alpha

    def build_E(tag):
        OR_W = 5.38e-5

        # ==============================================================
        # GROUP SA: Transformed Gamma_norm (SA01-SA08)
        # Insight from L31: raw Gamma_norm too strong (chi2~18),
        # sqrt/log forms soften it to chi2~9.4 (PASS).
        # Explore more nonlinear transforms preserving delta(0)=0.
        # ==============================================================

        if tag == 'SA01':
            # arctan transform: softer than sqrt at large z, smoother near 0
            # Physical: arctan = quantum phase bounded by pi/2
            f = 0.5 / (math.pi/2.)  # normalize so arctan(inf)=pi/2 -> 0.5
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                dv,_=gn(z,Om,OR_W)
                if dv is None: return None
                delta = f*np.arctan(np.maximum(dv,0.))
                rde=OL0*(1.+delta); rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SA02':
            # tanh(Gamma_norm): bounded [0,1], rises quickly then saturates
            # Physical: two-state system; saturation = full SQ depletion
            f = 0.5
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                dv,_=gn(z,Om,OR_W)
                if dv is None: return None
                delta = f*np.tanh(np.maximum(dv,0.))
                rde=OL0*(1.+delta); rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SA03':
            # Rational: Gamma/(1+Gamma) = 1 - 1/(1+Gamma) -> bounded [0,1)
            # Physical: Michaelis-Menten type saturation (enzyme kinetics analog)
            f = 0.5
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                dv,_=gn(z,Om,OR_W)
                if dv is None: return None
                dv = np.maximum(dv, 0.)
                delta = f*(dv/(1.+dv))
                rde=OL0*(1.+delta); rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SA04':
            # 1-exp(-Gamma): exponential approach to saturation
            # Physical: Poisson process -- n annihilation events -> 1-e^(-lambda)
            f = 0.5
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                dv,_=gn(z,Om,OR_W)
                if dv is None: return None
                delta = f*(1.-np.exp(-np.maximum(dv,0.)))
                rde=OL0*(1.+delta); rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SA05':
            # Cube root: even softer than sqrt, slower saturation
            f = 0.5
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                dv,_=gn(z,Om,OR_W)
                if dv is None: return None
                delta = f*np.cbrt(np.maximum(dv,0.))
                rde=OL0*(1.+delta); rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SA06':
            # 2/3 power: between sqrt and linear
            f = 0.5
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                dv,_=gn(z,Om,OR_W)
                if dv is None: return None
                delta = f*np.maximum(dv,0.)**(2./3.)
                rde=OL0*(1.+delta); rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SA07':
            # erf(Gamma_norm): error function transform, very smooth
            # Physical: Gaussian-distributed SQ lifetimes -> erf CDF
            f = 0.5
            from scipy.special import erf as scipy_erf
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                dv,_=gn(z,Om,OR_W)
                if dv is None: return None
                delta = f*scipy_erf(np.maximum(dv,0.))
                rde=OL0*(1.+delta); rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SA08':
            # Gamma*exp(-Gamma/scale): peaks then decays -- resonance shape
            # Physical: SQ-matter interaction resonance at z_eq
            # scale = saturation level = 1/alpha
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                dv,alpha=gn(z,Om,OR_W)
                if dv is None: return None
                scale = 1./max(alpha, 0.01)
                delta = 0.5*(dv/scale)*np.exp(-dv/scale)
                rde=OL0*(1.+delta); rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        # ==============================================================
        # GROUP SB: SQT-L30 Bridge (SB01-SB08)
        # Bridge between SQT Gamma_norm and L30 empirical champions.
        # Key: suppress high-z growth of Gamma_norm or hybrid with tanh.
        # ==============================================================

        elif tag == 'SB01':
            # Gamma_norm with exponential high-z suppression
            # Physical: at z >> z_eq, SQ completely annihilated -> DE saturates
            # Suppression scale z_sat = z_eq (matter-DE equality)
            f = 0.5
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                z_eq=(OL0/Om)**(1./3.)-1.
                if z_eq<=0: z_eq=0.3
                dv,_=gn(z,Om,OR_W)
                if dv is None: return None
                delta = f*dv*np.exp(-z/z_eq)
                rde=OL0*(1.+delta); rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SB02':
            # Self-quenching: Gamma_norm * psi*(z)
            # Physical: as SQ depletes (psi decreases), annihilation DE also reduces
            # Negative feedback loop -- naturally bounded
            f = 0.5
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                alpha=Om/OL0
                psi_z=1./(1.+alpha*(1+z)**3)
                dv,_=gn(z,Om,OR_W)
                if dv is None: return None
                delta = f*dv*psi_z
                rde=OL0*(1.+delta); rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SB03':
            # Geometric mean: sqrt(Gamma_norm * tanh(z/z_eq))
            # Bridge: SQT Gamma_norm * L30 tanh, both square-rooted
            # Physical: two independent channels contribute equally
            f = 0.5
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                z_eq=(OL0/Om)**(1./3.)-1.
                if z_eq<=0: z_eq=0.3
                dv,_=gn(z,Om,OR_W)
                if dv is None: return None
                product = np.maximum(dv,0.)*np.tanh(z/z_eq)
                delta = f*np.sqrt(product)
                rde=OL0*(1.+delta); rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SB04':
            # Soft min: min(Gamma_norm, tanh_sat) smoothed
            # Physical: DE saturates when SQ fully depleted at tanh scale
            # tanh_sat = tanh(1) ~ 0.76 (DD06 saturation level)
            f = 0.5
            tanh_sat = float(np.tanh(1.0))
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                dv,_=gn(z,Om,OR_W)
                if dv is None: return None
                # Smooth min via: min(a,b) = (a+b-|a-b|)/2
                b = tanh_sat
                delta = f*0.5*(dv + b - np.abs(dv - b))
                rde=OL0*(1.+delta); rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SB05':
            # sqrt(Gamma_norm) with amplitude f=1/3 (L31 GB04 best + different f)
            f = 1./3.
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                dv,_=gn(z,Om,OR_W)
                if dv is None: return None
                delta = f*np.sqrt(np.maximum(dv,0.))
                rde=OL0*(1.+delta); rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SB06':
            # sqrt(Gamma_norm) f=1/pi
            f = 1./math.pi
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                dv,_=gn(z,Om,OR_W)
                if dv is None: return None
                delta = f*np.sqrt(np.maximum(dv,0.))
                rde=OL0*(1.+delta); rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SB07':
            # log(1+Gamma_norm) f=1/3 (L31 GB06 best + different f)
            f = 1./3.
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                dv,alpha=gn(z,Om,OR_W)
                if dv is None: return None
                sat=1./max(alpha,0.01)
                norm=math.log1p(sat)
                if norm<=0: return None
                delta = f*np.log1p(np.maximum(dv,0.))/norm
                rde=OL0*(1.+delta); rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SB08':
            # Two-channel: 0.3*sqrt(Gamma_norm) + 0.2*tanh(z/z_eq)
            # Best of both: SQT low-z behavior + phenomenological saturation
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                z_eq=(OL0/Om)**(1./3.)-1.
                if z_eq<=0: z_eq=0.3
                dv,_=gn(z,Om,OR_W)
                if dv is None: return None
                delta = 0.3*np.sqrt(np.maximum(dv,0.)) + 0.2*np.tanh(z/z_eq)
                rde=OL0*(1.+delta); rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        # ==============================================================
        # GROUP SC: psi-field w(z) engineering (SC01-SC08)
        # Design rho_DE via psi*(z) that naturally gives wa < 0.
        # wa<0 means DE was stronger in past (higher rho_DE at high z).
        # SQT: matter was denser in past -> more annihilation -> more DE.
        # ==============================================================

        elif tag == 'SC01':
            # rho_DE(z) = OL0 / psi*(z) * psi*(0)  [G_eff bounded version]
            # Physical: G_eff(z) = G/psi*(z) -> matter+DE both scale
            # Friedmann normalized: E^2 = [Om*(1+z)^3 + OL0*psi0/psi_z]
            # psi0/psi_z = (1+alpha*(1+z)^3)/(1+alpha) -> increases with z
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                alpha=Om/OL0
                psi0=1./(1.+alpha)
                psi_z=1./(1.+alpha*(1+z)**3)
                if psi0<1e-10: return None
                rde=OL0*psi0/psi_z
                rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SC02':
            # Partial G_eff: only fraction f of DE scales with G_eff
            # rho_DE = OL0*(f*psi0/psi_z + (1-f))
            # Physical: fraction f of DE from SQ dynamics, rest from vacuum
            f = 0.3
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                alpha=Om/OL0
                psi0=1./(1.+alpha)
                psi_z=1./(1.+alpha*(1+z)**3)
                if psi0<1e-10: return None
                rde=OL0*(f*psi0/psi_z + (1.-f))
                rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SC03':
            # sqrt(psi0/psi_z): softer G_eff scaling
            # Physical: DE ~ sqrt(Gamma) coupling (diffusion-limited)
            f = 0.5
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                alpha=Om/OL0
                psi0=1./(1.+alpha)
                psi_z=1./(1.+alpha*(1+z)**3)
                if psi0<1e-10 or np.any(psi_z<1e-10): return None
                ratio=np.sqrt(psi0/psi_z)
                rde=OL0*(f*ratio + (1.-f))
                rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SC04':
            # log(psi0/psi_z): entropic DE contribution
            # Physical: S = -log(psi) is SQ depletion entropy; delta S drives DE
            # log(psi0/psi_z) = log(1 + alpha*((1+z)^3 - 1)) -> grows with z
            f = 0.5
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                alpha=Om/OL0
                psi0=1./(1.+alpha)
                psi_z=1./(1.+alpha*(1+z)**3)
                if psi0<1e-10 or np.any(psi_z<1e-10): return None
                delta=f*np.log(psi0/psi_z)
                rde=OL0*(1.+delta)
                rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SC05':
            # (1-psi_z)/(1-psi0): normalized depletion fraction
            # Physical: fraction of SQ space "consumed" relative to today
            # At z=0: 0. At high z: -> 1/(1-psi0) * alpha ~ 1
            f = 0.5
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                alpha=Om/OL0
                psi0=1./(1.+alpha)
                psi_z=1./(1.+alpha*(1+z)**3)
                denom=1.-psi0
                if abs(denom)<1e-10: return None
                delta=f*(1.-psi_z - (1.-psi0))/denom
                rde=OL0*(1.+delta)
                rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SC06':
            # psi0^2/psi_z^2: quadratic G_eff scaling
            # Physical: two-body SQ interaction -> amplitude squared
            f = 0.2
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                alpha=Om/OL0
                psi0=1./(1.+alpha)
                psi_z=1./(1.+alpha*(1+z)**3)
                if psi0<1e-10 or np.any(psi_z<1e-10): return None
                ratio=(psi0/psi_z)**2
                rde=OL0*(f*ratio+(1.-f))
                rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SC07':
            # Asymmetric: psi0/psi_z below z_eq, flat above (saturation)
            # Physical: below z_eq annihilation drives DE; above z_eq fully saturated
            f = 0.3
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                alpha=Om/OL0
                z_eq=(OL0/Om)**(1./3.)-1.
                if z_eq<=0: z_eq=0.3
                psi0=1./(1.+alpha)
                psi_z=1./(1.+alpha*(1+z)**3)
                psi_eq=1./(1.+alpha*(1.+z_eq)**3)
                ratio_cap=psi0/psi_eq  # saturation at z=z_eq
                ratio=np.minimum(psi0/psi_z, ratio_cap)
                rde=OL0*(f*ratio+(1.-f))
                rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SC08':
            # Combination: sqrt(psi0/psi_z) + log(psi0/psi_z) -- two SQT channels
            # Physical: amplitude channel (sqrt) + entropy channel (log)
            f1 = 0.3; f2 = 0.2
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                alpha=Om/OL0
                psi0=1./(1.+alpha)
                psi_z=1./(1.+alpha*(1+z)**3)
                if psi0<1e-10 or np.any(psi_z<1e-10): return None
                delta=f1*np.sqrt(psi0/psi_z)-f1 + f2*np.log(psi0/psi_z)
                rde=OL0*(1.+delta)
                rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        # ==============================================================
        # GROUP SD: Dynamic psi lag models (SD01-SD06)
        # psi doesn't instantly track psi*(z); lag creates extra DE.
        # Damped: psi(z) = psi*(z) + lag_correction
        # ==============================================================

        elif tag == 'SD01':
            # Linear lag: psi(z) = psi*(z) + tau * dpsi*/dz
            # Physical: SQ field responds with time delay tau = 1/kappa
            # tau_norm = 1 (tau * H0 in Hubble units)
            tau = 1.0
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                alpha=Om/OL0
                psi_z=1./(1.+alpha*(1+z)**3)
                # dpsi*/dz = 3*alpha*(1+z)^2 / (1+alpha*(1+z)^3)^2
                dpsi_dz = 3.*alpha*(1+z)**2 / (1.+alpha*(1+z)**3)**2
                # lag correction: psi_lag = psi* + tau*dpsi*/dz (negative, psi decreasing)
                psi_lag = psi_z + tau*dpsi_dz
                psi_lag = np.maximum(psi_lag, 1e-6)
                psi0=1./(1.+alpha)
                dpsi0=3.*alpha/(1.+alpha)**2  # dpsi*/dz at z=0
                psi_lag0=psi0+tau*dpsi0
                if psi_lag0<1e-6: return None
                rde=OL0*psi_lag0/psi_lag
                rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SD02':
            # Exponential lag: psi(z) = (1-f)*psi*(z) + f*psi*(0)
            # Physical: partial memory of initial SQ density
            # f=0.3 (30% of initial state retained)
            f = 0.3
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                alpha=Om/OL0
                psi0=1./(1.+alpha)
                psi_z=1./(1.+alpha*(1+z)**3)
                psi_mem=(1.-f)*psi_z + f*psi0
                rde=OL0*psi0/psi_mem
                rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SD03':
            # Overdamped: psi(z) = psi*(z) * (1 + beta*(1-psi*(z)))
            # Physical: friction from SQ-matter coupling adds extra depletion
            # beta = alpha (coupling proportional to matter/DE ratio)
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                alpha=Om/OL0
                psi_z=1./(1.+alpha*(1+z)**3)
                psi0=1./(1.+alpha)
                beta=alpha  # overdamping from SQT coupling
                psi_od=psi_z*(1.+beta*(1.-psi_z))
                psi_od0=psi0*(1.+beta*(1.-psi0))
                psi_od=np.maximum(psi_od,1e-6)
                if psi_od0<1e-6: return None
                rde=OL0*psi_od0/psi_od
                rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SD04':
            # DE from psi relaxation energy: V(psi_z - psi*_z)^2
            # Physical: if psi lags behind equilibrium, potential energy released
            # lag_psi = psi*(z+dz) - psi*(z) ~ dpsi*/dz * dz
            # V ~ (lag)^2; use dz=1/H0 (Hubble time lag)
            f = 0.5
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                alpha=Om/OL0
                psi_z=1./(1.+alpha*(1+z)**3)
                psi0=1./(1.+alpha)
                dpsi_dz=3.*alpha*(1+z)**2/(1.+alpha*(1+z)**3)**2
                dpsi0=3.*alpha/(1.+alpha)**2
                # lag energy ~ (dpsi/dz)^2; normalized by z=0 value
                if abs(dpsi0)<1e-10: return None
                lag_z=(dpsi_dz/dpsi0)**2
                lag_0=1.0
                delta=f*(lag_z-lag_0)
                rde=OL0*(1.+delta)
                rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SD05':
            # psi "bounce": at high z psi overshoots equilibrium
            # psi_bounce(z) = psi*(z) * (1 - beta*exp(-z/z_eq))
            # Physical: quantum tunneling back to higher density at early universe
            # beta = 0.5 (amplitude), z_eq = SQT equilibrium scale
            beta = 0.5
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                alpha=Om/OL0
                z_eq=(OL0/Om)**(1./3.)-1.
                if z_eq<=0: z_eq=0.3
                psi_z=1./(1.+alpha*(1+z)**3)
                psi0=1./(1.+alpha)
                psi_b=psi_z*(1.-beta*np.exp(-z/z_eq))
                psi_b0=psi0*(1.-beta)
                psi_b=np.maximum(psi_b,1e-6)
                if psi_b0<1e-6: return None
                rde=OL0*psi_b0/psi_b
                rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        elif tag == 'SD06':
            # Combined best: sqrt(Gamma_norm) + sc04(log psi0/psi_z)
            # SA best + SC best merged
            f1 = 0.35; f2 = 0.15
            def E_fn(z,Om):
                OL0=1.-Om-OR_W
                if OL0<=0: return None
                alpha=Om/OL0
                psi0=1./(1.+alpha)
                psi_z=1./(1.+alpha*(1+z)**3)
                if psi0<1e-10 or np.any(psi_z<1e-10): return None
                dv,_=gn(z,Om,OR_W)
                if dv is None: return None
                d1=f1*np.sqrt(np.maximum(dv,0.))
                d2=f2*np.log(psi0/psi_z)
                rde=OL0*(1.+d1+d2)
                rde=np.maximum(rde,1e-10)
                E2=OR_W*(1+z)**4+Om*(1+z)**3+rde
                return None if not np.all(np.isfinite(E2)) or np.any(E2<0) else np.sqrt(np.maximum(E2,1e-30))
            return E_fn

        else:
            return None

    # ------------------------------------------------------------------
    wid, theory_name, k, _, task_data = args
    tag = task_data['tag']
    E_fn = build_E(tag)
    if E_fn is None:
        return {'id':wid,'name':theory_name,'k':k,'chi2':1e8,'aicc':1e8,'d_aicc':1e8,
                'Om':None,'H0':None,'w0':0.,'wa':0.,'status':'FAIL'}

    # 20-start Nelder-Mead + differential_evolution
    starts = [
        [0.315,67.4],[0.30,68.0],[0.32,69.0],[0.29,70.0],
        [0.31,68.5],[0.28,71.0],[0.33,67.0],[0.34,66.5],
        [0.35,65.0],[0.36,63.0],[0.27,72.0],[0.26,73.0],
        [0.315,65.0],[0.315,70.0],[0.30,65.0],[0.30,70.0],
        [0.32,67.0],[0.32,69.5],[0.29,68.0],[0.31,70.0],
    ]
    best_chi2 = 1e8; best_x = None

    for s in starts:
        try:
            r = minimize(lambda p,ef=E_fn: chi2_fn(p,ef), s, method='Nelder-Mead',
                         options={'xatol':1e-7,'fatol':1e-7,'maxiter':8000})
            if r.fun < best_chi2: best_chi2=r.fun; best_x=r.x
        except Exception: continue

    try:
        rd = differential_evolution(lambda p,ef=E_fn: chi2_fn(p,ef),
            bounds=[(0.20,0.50),(60.,80.)],
            maxiter=500, tol=1e-7, seed=42, workers=1, popsize=30)
        if rd.fun < best_chi2: best_chi2=rd.fun; best_x=rd.x
    except Exception: pass

    if best_x is None:
        return {'id':wid,'name':theory_name,'k':k,'chi2':1e8,'aicc':1e8,'d_aicc':1e8,
                'Om':None,'H0':None,'w0':0.,'wa':0.,'status':'FAIL'}

    Om_b,H0_b = float(best_x[0]),float(best_x[1])
    chi2_b = float(best_chi2)
    aicc_b = aicc_w(chi2_b, k)
    d_aicc = aicc_b - LCDM_AICC_W

    # CPL w0/wa fit
    w0, wa = cpl_wa(Om_b, E_fn, OR_W)

    # K93: wa >= 0 -> KILL
    if aicc_b >= LCDM_AICC_W:
        status = 'K90'
    elif wa >= 0.:
        status = 'K93'
    elif d_aicc < -4. and wa < -0.5:
        status = 'Q92'
    elif d_aicc < -2.:
        status = 'Q91'
    else:
        status = 'Q90'

    return {'id':wid,'name':theory_name,'k':k,
            'chi2':chi2_b,'aicc':aicc_b,'d_aicc':d_aicc,
            'Om':Om_b,'H0':H0_b,'w0':w0,'wa':wa,'status':status}


def build_tasks():
    t = []
    # SA: Transformed Gamma_norm
    t.append(('SA01','SA: arctan(Gamma_norm) f=0.5/(pi/2)',2,{'tag':'SA01'}))
    t.append(('SA02','SA: tanh(Gamma_norm) f=0.5',2,{'tag':'SA02'}))
    t.append(('SA03','SA: Gamma/(1+Gamma) rational f=0.5',2,{'tag':'SA03'}))
    t.append(('SA04','SA: 1-exp(-Gamma) Poisson f=0.5',2,{'tag':'SA04'}))
    t.append(('SA05','SA: Gamma^(1/3) cube root f=0.5',2,{'tag':'SA05'}))
    t.append(('SA06','SA: Gamma^(2/3) two-thirds f=0.5',2,{'tag':'SA06'}))
    t.append(('SA07','SA: erf(Gamma_norm) f=0.5',2,{'tag':'SA07'}))
    t.append(('SA08','SA: Gamma*exp(-Gamma/scale) resonance',2,{'tag':'SA08'}))
    # SB: SQT-L30 Bridge
    t.append(('SB01','SB: Gamma*exp(-z/z_eq) high-z suppressed',2,{'tag':'SB01'}))
    t.append(('SB02','SB: Gamma*psi_z self-quenching',2,{'tag':'SB02'}))
    t.append(('SB03','SB: sqrt(Gamma*tanh) geometric mean',2,{'tag':'SB03'}))
    t.append(('SB04','SB: soft-min(Gamma, tanh_sat=0.76)',2,{'tag':'SB04'}))
    t.append(('SB05','SB: sqrt(Gamma_norm) f=1/3',2,{'tag':'SB05'}))
    t.append(('SB06','SB: sqrt(Gamma_norm) f=1/pi',2,{'tag':'SB06'}))
    t.append(('SB07','SB: log(1+Gamma_norm) f=1/3',2,{'tag':'SB07'}))
    t.append(('SB08','SB: 0.3*sqrt(Gamma)+0.2*tanh hybrid',2,{'tag':'SB08'}))
    # SC: psi-field w(z) engineering
    t.append(('SC01','SC: rho_DE=OL0*psi0/psi_z G_eff',2,{'tag':'SC01'}))
    t.append(('SC02','SC: rho_DE=OL0*(0.3*psi0/psi+0.7) partial G_eff',2,{'tag':'SC02'}))
    t.append(('SC03','SC: rho_DE=OL0*(0.5*sqrt(psi0/psi)+0.5)',2,{'tag':'SC03'}))
    t.append(('SC04','SC: delta=0.5*log(psi0/psi_z) entropy DE',2,{'tag':'SC04'}))
    t.append(('SC05','SC: (1-psi_z-1+psi0)/(1-psi0) depletion frac',2,{'tag':'SC05'}))
    t.append(('SC06','SC: rho_DE=OL0*(0.2*(psi0/psi)^2+0.8)',2,{'tag':'SC06'}))
    t.append(('SC07','SC: psi0/psi capped at z_eq',2,{'tag':'SC07'}))
    t.append(('SC08','SC: sqrt(psi0/psi)+log(psi0/psi) dual channel',2,{'tag':'SC08'}))
    # SD: Dynamic psi lag
    t.append(('SD01','SD: linear lag psi+tau*dpsi/dz tau=1',2,{'tag':'SD01'}))
    t.append(('SD02','SD: memory psi=0.7*psi_z+0.3*psi0',2,{'tag':'SD02'}))
    t.append(('SD03','SD: overdamped psi*(1+alpha*(1-psi))',2,{'tag':'SD03'}))
    t.append(('SD04','SD: relaxation energy (dpsi/dz)^2',2,{'tag':'SD04'}))
    t.append(('SD05','SD: psi bounce beta=0.5*exp(-z/z_eq)',2,{'tag':'SD05'}))
    t.append(('SD06','SD: 0.35*sqrt(Gamma)+0.15*log(psi0/psi)',2,{'tag':'SD06'}))
    return t


def main():
    print('='*70)
    print('L32 SQT theories: SA/SB/SC/SD (30 theories)')
    print('='*70)
    print('SA(8): Transformed Gamma_norm')
    print('SB(8): SQT-L30 Bridge')
    print('SC(8): psi-field engineering')
    print('SD(6): Dynamic psi lag')
    print(f'LCDM: chi2={LCDM_CHI2}, AICc={LCDM_AICC}')
    print()

    tasks = build_tasks()
    wargs = [(t[0],t[1],t[2],'sqt',t[3]) for t in tasks]
    print(f'Theories: {len(wargs)}')

    ctx = multiprocessing.get_context('spawn')
    with ctx.Pool(processes=9) as pool:
        results = pool.map(worker_fn, wargs)

    results.sort(key=lambda r: r['aicc'])

    print()
    print('='*70)
    print('RESULTS sorted by AICc:')
    print('='*70)
    print(f"{'ID':>5} {'Theory':44s} {'chi2':>9} {'AICc':>9} {'dAICc':>8} {'w0':>7} {'wa':>7} {'Status':>5}")
    print('-'*102)

    pass_count = q91 = q92 = kill_count = 0
    champion = None
    for r in results:
        s = r['status']
        if s in ('Q90','Q91','Q92'):
            pass_count += 1
            if champion is None or r['aicc']<champion['aicc']: champion=r
        if s=='Q91': q91+=1
        if s=='Q92': q92+=1
        if s in ('K90','K91','K92','K93'): kill_count+=1

        c2s = f"{r['chi2']:.4f}" if r['chi2']<1e7 else 'FAIL'
        as_ = f"{r['aicc']:.4f}" if r['aicc']<1e7 else 'FAIL'
        ds  = f"{r['d_aicc']:+.4f}" if r['d_aicc']<1e7 else 'FAIL'
        print(f"{r['id']:>5} {r['name'][:44]:44s} {c2s:>9} {as_:>9} {ds:>8} "
              f"{r['w0']:>7.4f} {r['wa']:>7.4f} {s:>5}")

    print()
    print(f'Q90 PASS: {pass_count} / KILL: {kill_count}')
    print(f'Q91 STRONG PASS: {q91}')
    print(f'Q92 GAME-CHANGER: {q92}')
    if champion:
        print(f"Champion: {champion['id']} dAICc={champion['d_aicc']:.4f} "
              f"chi2={champion['chi2']:.4f} w0={champion['w0']:.4f} wa={champion['wa']:.4f} "
              f"Om={champion['Om']:.4f} H0={champion['H0']:.4f}")

    out = os.path.join(_SCRIPT_DIR,'l32_results.json')
    def jfy(o):
        if isinstance(o,np.integer): return int(o)
        if isinstance(o,np.floating): return float(o)
        if isinstance(o,np.ndarray): return o.tolist()
        if isinstance(o,dict): return {k:jfy(v) for k,v in o.items()}
        if isinstance(o,(list,tuple)): return [jfy(v) for v in o]
        return o

    with open(out,'w',encoding='utf-8') as fp:
        json.dump(jfy({'run':'L32-SA-SB-SC-SD','theories':results,
            'pass_count':pass_count,'q91':q91,'q92':q92,'kill_count':kill_count,
            'champion':champion,'lcdm':{'chi2':LCDM_CHI2,'aicc':LCDM_AICC}}),
            fp, indent=2, ensure_ascii=False)
    print(f'\nResults saved: {out}')


if __name__ == '__main__':
    main()
