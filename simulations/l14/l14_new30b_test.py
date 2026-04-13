# -*- coding: utf-8 -*-
"""
L14 Batch-2: 30 more new theories from A1+A2. Phases 11-20.

Phase 11: Bose-Einstein Condensation (B1-B3)
Phase 12: Quantum Tunneling / WKB (Q1-Q3)
Phase 13: Self-Organized Criticality (S1-S3)
Phase 14: Epidemic / SIR (EP1-EP3)
Phase 15: Polymer network / Gelation (PL1-PL3)
Phase 16: Stochastic gravity / Noise (N1-N3)
Phase 17: Holography / RT formula (H1-H3)
Phase 18: Quantum Error Correction (QE1-QE3)
Phase 19: Tensor network / MERA (TN1-TN3)
Phase 20: Discrete quantum walk (W1-W3)
"""
from __future__ import annotations
import os, json
import numpy as np
from scipy.optimize import minimize, curve_fit
from scipy.interpolate import interp1d

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
np.seterr(all='ignore')

_THIS = os.path.dirname(os.path.abspath(__file__))

c_SI    = 2.998e8
Mpc_m   = 3.086e22
OMEGA_R = 9.1e-5
rs_drag = 147.09
H0_KMS  = 67.7
H0_SI   = H0_KMS * 1e3 / Mpc_m

DESI_Z   = np.array([0.295, 0.510, 0.706, 0.930, 1.317, 1.491, 2.330])
DESI_OBS = np.array([7.93, 13.62, 16.85, 21.71, 27.79, 30.21, 39.71])
DESI_ERR = np.array([0.15,  0.17,  0.22,  0.22,  0.55,  0.49,  0.94])

N_Z  = 3000
Z_MAX = 6.0
Z_ARR = np.linspace(0.0, Z_MAX, N_Z)


def chi2_from_ode(z_arr, ode_arr, Om):
    E2 = OMEGA_R*(1+z_arr)**4 + Om*(1+z_arr)**3 + np.maximum(ode_arr, 0)
    E_arr = np.sqrt(np.maximum(E2, 1e-15))
    E_interp = interp1d(z_arr, E_arr, kind='cubic',
                        fill_value='extrapolate', bounds_error=False)
    z_int = np.linspace(0, Z_MAX*0.99, 5000)
    inv_E = 1.0/np.maximum(E_interp(z_int), 1e-10)
    dz = np.diff(z_int)
    cum = np.zeros(len(z_int))
    for i in range(1, len(z_int)):
        cum[i] = cum[i-1] + 0.5*(inv_E[i-1]+inv_E[i])*dz[i-1]
    chi_func = interp1d(z_int, cum, kind='cubic',
                        fill_value='extrapolate', bounds_error=False)
    fac = c_SI/(H0_SI*Mpc_m)
    pred = np.zeros(7)
    DM0 = fac * chi_func(DESI_Z[0])
    DH0 = fac / E_interp(DESI_Z[0])
    DV0 = (DESI_Z[0]*DM0**2*DH0)**(1.0/3.0)
    pred[0] = DV0/rs_drag
    for k, z in enumerate(DESI_Z[1:], 1):
        pred[k] = fac * chi_func(z)/rs_drag
    resid = pred - DESI_OBS
    c2 = float(np.sum((resid/DESI_ERR)**2))
    return c2 if np.isfinite(c2) and c2 < 1e8 else 1e8


def fit_cpl(z_arr, ode_arr):
    z_fit = np.linspace(0.01, 1.5, 300)
    dz = 1e-4
    ode_i = interp1d(z_arr, ode_arr, kind='cubic',
                     fill_value='extrapolate', bounds_error=False)
    u   = np.array([float(ode_i(z)) for z in z_fit])
    u_p = np.array([float(ode_i(z+dz)) for z in z_fit])
    u_m = np.array([float(ode_i(max(z-dz, 1e-5))) for z in z_fit])
    dlnu = (u_p-u_m)/(2*dz*np.maximum(u, 1e-20))
    w_z = (1+z_fit)*dlnu/3.0 - 1.0
    def w_cpl(z, w0, wa):
        return w0 + wa*(1-1/(1+z))
    try:
        popt, _ = curve_fit(w_cpl, z_fit, w_z, p0=[-0.95, -0.2],
                            bounds=([-3.0, -10.0], [0.5, 5.0]), maxfev=5000)
        return float(popt[0]), float(popt[1])
    except Exception:
        return float('nan'), float('nan')


def fit_model(make_fn, label, starts):
    best = (1e9, None)
    for p0 in starts:
        def obj(p):
            Om = p[0]
            if Om < 0.28 or Om > 0.36:
                return 1e8
            try:
                arr = make_fn(p)
                if arr is None:
                    return 1e8
                return chi2_from_ode(Z_ARR, arr, Om)
            except Exception:
                return 1e8
        res = minimize(obj, p0, method='Nelder-Mead',
                       options={'xatol':1e-5,'fatol':0.01,'maxiter':8000})
        if res.fun < best[0]:
            best = (res.fun, list(res.x))
    if best[1] is None:
        print(label + '  FAILED')
        return None, 1e8, float('nan'), float('nan'), None
    p_best, c2 = best[1], best[0]
    arr = make_fn(p_best)
    if arr is None:
        return p_best, c2, float('nan'), float('nan'), None
    w0, wa = fit_cpl(Z_ARR, arr)
    print(label + '  p=' + str([round(x,4) for x in p_best]) +
          '  chi2=' + str(round(c2,3)) +
          '  w0=' + str(round(w0,3)) + '  wa=' + str(round(wa,3)))
    return p_best, c2, w0, wa, arr


def _E_LCDM(Om, z_arr):
    OL0 = 1.0 - Om - OMEGA_R
    return np.sqrt(np.maximum(OMEGA_R*(1+z_arr)**4+Om*(1+z_arr)**3+OL0, 1e-15))

def _J(Om, z_arr):
    """J(z) = integral_0^z (1+z')^2/E_LCDM dz'"""
    E = _E_LCDM(Om, z_arr)
    intg = (1+z_arr)**2 / E
    J = np.zeros_like(z_arr)
    for i in range(1, len(z_arr)):
        dz = z_arr[i]-z_arr[i-1]
        J[i] = J[i-1]+0.5*(intg[i-1]+intg[i])*dz
    return J


# ---------------------------------------------------------------------------
# Phase 11: Bose-Einstein Condensation
# ---------------------------------------------------------------------------

def make_B1(p):
    """B1: BEC condensate threshold (hard cutoff).
    omega_de = OL0 * max(1-(1+z)^{3/2}/sqrt(A), 0)^{2/3} -- normalized.
    For A > 1: condensate survives at z=0. Decreases → use A<1 regime or negative.
    Reinterpret: A = critical density ratio. omega_de = OL0*(1-Om*(1+z)^3/(A*OL0))^{2/3}
    when Om*(1+z)^3 < A*OL0, else 0. --> DECREASES, wa>0.
    ALTERNATIVE: treat as fluctuation above minimum: omega_de = OL0*(1+A*exp(-B*(1+z)^{3/2}))
    normalized at z=0."""
    Om = p[0]; A = p[1]; B = max(p[2], 0.01)
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    denom = 1.0+A*np.exp(-B)
    if abs(denom) < 1e-10:
        return None
    arr = OL0*(1.0+A*np.exp(-B*(1+Z_ARR)**1.5))/denom
    return np.maximum(arr, 0.0)

def make_B2(p):
    """B2: BEC order parameter power 2/3.
    omega_de = OL0*(1+A*((1+z)^3-1))^{2/3} normalized at z=0.
    For A>0: grows with z (phantom). For A<0: decreasing (quintessence)."""
    Om = p[0]; A = p[1]
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    base = 1.0+A*((1+Z_ARR)**3-1.0)
    if np.any(base <= 0):
        base = np.maximum(base, 0.01)
    arr = OL0*base**(2.0/3.0)
    return np.maximum(arr, 0.0)

def make_B3(p):
    """B3: Bogoliubov exponential depletion.
    omega_de = OL0*exp(-A*((1+z)^3-1)).
    A<0: GROWS with z (phantom). A>0: shrinks."""
    Om = p[0]; A = p[1]
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    exponent = -A*((1+Z_ARR)**3-1.0)
    arr = OL0*np.exp(np.minimum(exponent, 50.0))
    return np.maximum(arr, 0.0)


# ---------------------------------------------------------------------------
# Phase 12: Quantum Tunneling / WKB
# ---------------------------------------------------------------------------

def make_Q1(p):
    """Q1: WKB action sqrt(barrier). omega_de = OL0*exp(-A*((1+z)^{3/2}-1)).
    A<0: GROWS."""
    Om = p[0]; A = p[1]
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    exponent = -A*((1+Z_ARR)**1.5-1.0)
    arr = OL0*np.exp(np.minimum(exponent, 50.0))
    return np.maximum(arr, 0.0)

def make_Q2(p):
    """Q2: Gamow factor with thermal velocity.
    omega_de = OL0*(1+A*(exp(-C/sqrt(1+z))-exp(-C))).
    exp(-C/sqrt(1+z)) INCREASES with z (from exp(-C) to 1).
    For A>0: omega_de GROWS with z (phantom). For A<0: shrinks."""
    Om = p[0]; A = p[1]; C = max(p[2], 0.01)
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    f_z = np.exp(-C/np.sqrt(1.0+Z_ARR))
    f_0 = np.exp(-C)
    arr = OL0*(1.0+A*(f_z-f_0))
    return np.maximum(arr, 0.0)

def make_Q3(p):
    """Q3: Resonant tunneling Lorentzian.
    omega_de = OL0*(1+A*Om*(1+z)^3/(B^2+(Om*(1+z)^3)^2)) normalized.
    Peaks at Om*(1+z)^3 = B."""
    Om = p[0]; A = p[1]; B = max(p[2], 0.01)
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    x_z = Om*(1+Z_ARR)**3
    x_0 = Om
    f_z = x_z/(B**2+x_z**2)
    f_0 = x_0/(B**2+x_0**2)
    denom = max(1.0+A*f_0, 1e-10)
    arr = OL0*(1.0+A*f_z)/denom
    return np.maximum(arr, 0.0)


# ---------------------------------------------------------------------------
# Phase 13: Self-Organized Criticality
# ---------------------------------------------------------------------------

def make_S1(p):
    """S1: SOC avalanche power law (tau=5/3 -> exponent 2/3).
    omega_de = OL0*(1+A*((1+z)^{2/3}-1)).
    A>0: GROWS with z (phantom)."""
    Om = p[0]; A = p[1]
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    arr = OL0*(1.0+A*((1+Z_ARR)**(2.0/3.0)-1.0))
    return np.maximum(arr, 0.0)

def make_S2(p):
    """S2: SOC logarithmic scale invariance (like T3 with extra B parameter).
    omega_de = OL0*(1+A*ln(1+B*Om*(1+z)^3/OL0))/(1+A*ln(1+B*Om/OL0))."""
    Om = p[0]; A = p[1]; B = max(p[2], 0.01)
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    ln_z = np.log1p(B*Om*(1+Z_ARR)**3/max(OL0, 1e-10))
    ln_0 = np.log1p(B*Om/max(OL0, 1e-10))
    denom = max(1.0+A*ln_0, 1e-10)
    arr = OL0*(1.0+A*ln_z)/denom
    return np.maximum(arr, 0.0)

def make_S3(p):
    """S3: BTW critical arctanh saturation.
    omega_de = OL0*(1+A*arctanh(B*Om*(1+z)^3/(OL0+Om*(1+z)^3)))
               / (1+A*arctanh(B*Om/(OL0+Om))).
    arctanh INCREASES with z if B>0 -> grows (phantom)."""
    Om = p[0]; A = p[1]; B = max(min(p[2], 0.99), 0.01)
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    x_z = B*Om*(1+Z_ARR)**3/(OL0+Om*(1+Z_ARR)**3)
    x_0 = B*Om/(OL0+Om)
    # arctanh requires |x|<1
    x_z = np.clip(x_z, -0.999, 0.999)
    x_0 = max(min(float(x_0), 0.999), -0.999)
    ath_z = np.arctanh(x_z)
    ath_0 = float(np.arctanh(x_0))
    denom = max(1.0+A*ath_0, 1e-10)
    arr = OL0*(1.0+A*ath_z)/denom
    return np.maximum(arr, 0.0)


# ---------------------------------------------------------------------------
# Phase 14: Epidemic / SIR
# ---------------------------------------------------------------------------

def make_EP1(p):
    """EP1: SIR equilibrium Michaelis-Menten (DECREASES with z normally).
    omega_de = OL0*(OL0+A*Om)/(OL0+A*Om*(1+z)^3).
    A<0: can GROW with z."""
    Om = p[0]; A = p[1]
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    denom = OL0+A*Om*(1+Z_ARR)**3
    if np.any(np.abs(denom) < 1e-10):
        return None
    arr = OL0*(OL0+A*Om)/np.maximum(np.abs(denom), 1e-15)*np.sign(denom)
    # Restrict to positive
    numer = OL0+A*Om
    if numer <= 0:
        return None
    arr = OL0*numer/np.maximum(denom, 1e-10)
    return np.maximum(arr, 0.0)

def make_EP2(p):
    """EP2: SIS rational decay.
    omega_de = OL0^2/(OL0+A*Om*(1+z)^3).
    A<0: denominator decreases -> omega_de GROWS."""
    Om = p[0]; A = p[1]
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    denom = OL0+A*Om*(1+Z_ARR)**3
    if np.any(denom <= 0.01):
        return None
    arr = OL0**2/denom
    return np.maximum(arr, 0.0)

def make_EP3(p):
    """EP3: SIR vaccination exponential.
    omega_de = OL0*(1+A*exp(-B*Om*(1+z)^3/OL0))/(1+A*exp(-B*Om/OL0))."""
    Om = p[0]; A = p[1]; B = max(p[2], 0.01)
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    f_z = np.exp(-B*Om*(1+Z_ARR)**3/max(OL0, 1e-10))
    f_0 = float(np.exp(-B*Om/max(OL0, 1e-10)))
    denom = max(1.0+A*f_0, 1e-10)
    arr = OL0*(1.0+A*f_z)/denom
    return np.maximum(arr, 0.0)


# ---------------------------------------------------------------------------
# Phase 15: Polymer network / Gelation
# ---------------------------------------------------------------------------

def make_PL1(p):
    """PL1: Flory-Stockmayer gelation (f=3).
    omega_de = OL0*(1-(1-exp(-A/(1+z)^3))^3)/(1-(1-exp(-A))^3).
    At high z: A/(1+z)^3->0, exp->1, (1-1)^3=0, numerator->1. GROWS with z."""
    Om = p[0]; A = max(p[1], 0.01)
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    numer = 1.0-(1.0-np.exp(-A/(1+Z_ARR)**3))**3
    denom = 1.0-(1.0-np.exp(-A))**3
    if abs(denom) < 1e-10:
        return None
    arr = OL0*numer/denom
    return np.maximum(arr, 0.0)

def make_PL2(p):
    """PL2: de Gennes critical scaling power law.
    omega_de = OL0*((OL0+Om)/(OL0+Om*(1+z)^3))^nu.
    nu>0: DECREASES with z. nu<0: GROWS."""
    Om = p[0]; nu = p[1]
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    base = (OL0+Om)/np.maximum(OL0+Om*(1+Z_ARR)**3, 1e-10)
    arr = OL0*base**nu
    if not np.isfinite(arr).all():
        return None
    return np.maximum(arr, 0.0)

def make_PL3(p):
    """PL3: Zimm-Rouse cube root.
    omega_de = OL0*(1+A*(Om/(Om*(1+z)^3+OL0))^{1/3})/(1+A*(Om/(Om+OL0))^{1/3}).
    Om/(Om*(1+z)^3+OL0) DECREASES with z.
    A<0: numerator GROWS with z (phantom)."""
    Om = p[0]; A = p[1]
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    fz = (Om/np.maximum(Om*(1+Z_ARR)**3+OL0, 1e-10))**(1.0/3.0)
    f0 = (Om/max(Om+OL0, 1e-10))**(1.0/3.0)
    denom = max(1.0+A*f0, 1e-10)
    arr = OL0*(1.0+A*fz)/denom
    return np.maximum(arr, 0.0)


# ---------------------------------------------------------------------------
# Phase 16: Stochastic gravity / Noise
# ---------------------------------------------------------------------------

def make_N1(p):
    """N1: Fokker-Planck.
    omega_de = OL0*exp(-A*(Omega_m(z)-Om)) where Omega_m(z)=Om*(1+z)^3/E_LCDM^2.
    A<0: exp grows as Omega_m(z) increases."""
    Om = p[0]; A = p[1]
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    E_lcdm = _E_LCDM(Om, Z_ARR)
    Omega_m_z = Om*(1+Z_ARR)**3/np.maximum(E_lcdm**2, 1e-15)
    exponent = -A*(Omega_m_z-Om)
    arr = OL0*np.exp(np.minimum(exponent, 50.0))
    return np.maximum(arr, 0.0)

def make_N2(p):
    """N2: Noise-induced phase transition.
    omega_de = OL0*exp(A*(OL0/(Om*(1+z)^3+OL0)-OL0/(Om+OL0))).
    Second term = constant (z=0 value). OL0/(Om*(1+z)^3+OL0) DECREASES.
    A<0: exp grows (phantom)."""
    Om = p[0]; A = p[1]
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    fz = OL0/np.maximum(Om*(1+Z_ARR)**3+OL0, 1e-10)
    f0 = OL0/max(Om+OL0, 1e-10)
    exponent = A*(fz-f0)
    arr = OL0*np.exp(np.minimum(exponent, 50.0))
    return np.maximum(arr, 0.0)

def make_N3(p):
    """N3: Stochastic resonance Gaussian peak in E(z).
    omega_de = OL0*(1+A*(E(z)-1)*exp(-B*(E(z)-1)^2)).
    Peak at E(z)=1+1/sqrt(2B). Decays at high E."""
    Om = p[0]; A = p[1]; B = max(p[2], 0.01)
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    E = _E_LCDM(Om, Z_ARR)
    x = E-1.0
    arr = OL0*(1.0+A*x*np.exp(-B*x**2))
    return np.maximum(arr, 0.0)


# ---------------------------------------------------------------------------
# Phase 17: Holography / RT formula
# ---------------------------------------------------------------------------

def make_H1(p):
    """H1: RT area 2/3 scaling.
    omega_de = OL0*(f_de(z)/f_de(0))^{2/3} where f_de=OL0/(Om*(1+z)^3+OL0).
    f_de DECREASES -> omega_de DECREASES -> wa>0. Scale by nu to fit."""
    Om = p[0]; nu = p[1]
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    fz = OL0/np.maximum(Om*(1+Z_ARR)**3+OL0, 1e-10)
    f0 = OL0/max(Om+OL0, 1e-10)
    base = fz/max(f0, 1e-10)
    arr = OL0*base**nu
    if not np.isfinite(arr).all():
        return None
    return np.maximum(arr, 0.0)

def make_H2(p):
    """H2: Page curve (growth then decay).
    omega_de = OL0*(1+A*f_m(z))*(1-exp(-B/(1+z)^3))/(1+A*f_m(0))/(1-exp(-B))
    where f_m(z)=Om*(1+z)^3/(OL0+Om*(1+z)^3)."""
    Om = p[0]; A = p[1]; B = max(p[2], 0.1)
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    fm_z = Om*(1+Z_ARR)**3/np.maximum(OL0+Om*(1+Z_ARR)**3, 1e-10)
    fm_0 = Om/max(OL0+Om, 1e-10)
    growth = 1.0+A*fm_z
    decay = 1.0-np.exp(-B/(1+Z_ARR)**3)
    decay_0 = 1.0-np.exp(-B)
    if abs(decay_0) < 1e-10:
        return None
    denom_0 = max((1.0+A*fm_0)*decay_0, 1e-10)
    arr = OL0*growth*decay/denom_0
    if not np.isfinite(arr).all():
        return None
    return np.maximum(arr, 0.0)

def make_H3(p):
    """H3: Holographic screen sqrt form.
    omega_de = OL0*sqrt((1+A*Om/OL0)/(1+A*Om*(1+z)^3/OL0)).
    A>0: DECREASES. A<0: GROWS (phantom)."""
    Om = p[0]; A = p[1]
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    numer = max(1.0+A*Om/max(OL0, 1e-10), 1e-10)
    denom = 1.0+A*Om*(1+Z_ARR)**3/max(OL0, 1e-10)
    if np.any(denom <= 0.01):
        return None
    arr = OL0*np.sqrt(numer/np.maximum(denom, 1e-10))
    return np.maximum(arr, 0.0)


# ---------------------------------------------------------------------------
# Phase 18: Quantum Error Correction
# ---------------------------------------------------------------------------

def make_QE1(p):
    """QE1: Error threshold exponential.
    omega_de = OL0*exp(-A*Om*((1+z)^3-1)).
    A<0: GROWS (phantom)."""
    Om = p[0]; A = p[1]
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    exponent = -A*Om*((1+Z_ARR)**3-1.0)
    arr = OL0*np.exp(np.minimum(exponent, 50.0))
    return np.maximum(arr, 0.0)

def make_QE2(p):
    """QE2: Toric code tanh transition.
    omega_de = OL0*(1+A*tanh(-B*Om*(1+z)^3/OL0))/(1+A*tanh(-B*Om/OL0)).
    Saturates at -1 for large z; omega_de = OL0*(1-A)/(1+A*tanh(-B*Om/OL0)).
    A<0: (1+A*tanh(positive)) -> could grow if tanh is positive -> need -B < 0 i.e. B>0."""
    Om = p[0]; A = p[1]; B = p[2]
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    arg_z = -B*Om*(1+Z_ARR)**3/max(OL0, 1e-10)
    arg_0 = -B*Om/max(OL0, 1e-10)
    th_z = np.tanh(np.clip(arg_z, -10, 10))
    th_0 = float(np.tanh(float(arg_0)))
    denom = max(1.0+A*th_0, 1e-10)
    arr = OL0*(1.0+A*th_z)/denom
    return np.maximum(arr, 0.0)

def make_QE3(p):
    """QE3: Surface code double exponential.
    omega_de = OL0*exp(A*(exp(-B*Om*(1+z)^3)-exp(-B*Om))).
    exp(-B*Om*(1+z)^3) DECREASES with z.
    A<0: the argument decreases -> exp(negative) = GROWS if |decrease| large enough...
    At z=0: exp(A*(exp(-B*Om)-exp(-B*Om)))=exp(0)=1 -> omega_de=OL0 ✓
    For A>0: exp(A*(f_z-f_0)) where f_z<f_0 at high z -> argument negative -> DECREASES.
    For A<0: GROWS."""
    Om = p[0]; A = p[1]; B = max(p[2], 0.01)
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    fz = np.exp(-B*Om*(1+Z_ARR)**3)
    f0 = float(np.exp(-B*Om))
    exponent = A*(fz-f0)
    arr = OL0*np.exp(np.minimum(exponent, 50.0))
    return np.maximum(arr, 0.0)


# ---------------------------------------------------------------------------
# Phase 19: Tensor network / MERA
# ---------------------------------------------------------------------------

def make_TN1(p):
    """TN1: MERA log entanglement.
    omega_de = OL0*(1+A*ln(E_LCDM(z))).
    A>0: GROWS (since ln(E)>0 for z>0). A<0: DECREASES."""
    Om = p[0]; A = p[1]
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    E = _E_LCDM(Om, Z_ARR)
    arr = OL0*(1.0+A*np.log(np.maximum(E, 1e-10)))
    return np.maximum(arr, 0.0)

def make_TN2(p):
    """TN2: Bond dimension rational.
    omega_de = OL0*(OL0+A*Om)/(OL0+A*Om*(1+z)^3).
    A<0 and |A| > OL0/Om: denominator decreases -> numerator fixed -> GROWS."""
    Om = p[0]; A = p[1]
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    numer = OL0+A*Om
    if numer <= 0:
        return None
    denom = OL0+A*Om*(1+Z_ARR)**3
    if np.any(denom <= 0.01):
        return None
    arr = OL0*numer/denom
    return np.maximum(arr, 0.0)

def make_TN3(p):
    """TN3: Causal cone power of E.
    omega_de = OL0*((E0/E(z))^A) = OL0*E_LCDM(z)^{-A}.
    A>0: DECREASES (quintessence). A<0: GROWS (phantom)."""
    Om = p[0]; A = p[1]
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    E = _E_LCDM(Om, Z_ARR)
    E0 = max(float(E[0]), 1e-10)
    arr = OL0*(E0/np.maximum(E, 1e-10))**A
    if not np.isfinite(arr).all():
        return None
    return np.maximum(arr, 0.0)


# ---------------------------------------------------------------------------
# Phase 20: Discrete quantum walk
# ---------------------------------------------------------------------------

def make_W1(p):
    """W1: Grover search sqrt.
    omega_de = OL0*(1+A*Om*(1-1/sqrt(1+z))).
    (1-1/sqrt(1+z)) INCREASES from 0 to 1 as z->inf.
    A>0: GROWS (phantom)."""
    Om = p[0]; A = p[1]
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    arr = OL0*(1.0+A*Om*(1.0-1.0/np.sqrt(1.0+Z_ARR)))
    return np.maximum(arr, 0.0)

def make_W2(p):
    """W2: Anderson localization.
    omega_de = OL0*(1+A*(exp(-B*(1+z)^3)-exp(-B))).
    exp term DECREASES from exp(-B) toward 0.
    A<0: exp(positive value)... correction becomes positive -> GROWS. Wait:
    At z=0: A*(exp(-B)-exp(-B))=0 -> omega_de=OL0 ✓.
    As z->inf: A*(0-exp(-B)) = -A*exp(-B).
    A>0: -A*exp(-B) < 0 -> DECREASES. A<0: +|A|*exp(-B) > 0 -> GROWS."""
    Om = p[0]; A = p[1]; B = max(p[2], 0.01)
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    fz = np.exp(-B*(1+Z_ARR)**3)
    f0 = float(np.exp(-B))
    arr = OL0*(1.0+A*(fz-f0))
    return np.maximum(arr, 0.0)

def make_W3(p):
    """W3: Quantum walk 3/2 rational.
    omega_de = OL0*(OL0+A*Om)/(OL0+A*Om*(1+z)^{3/2}).
    A<0: denominator decreases -> GROWS."""
    Om = p[0]; A = p[1]
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    numer = OL0+A*Om
    if numer <= 0:
        return None
    denom = OL0+A*Om*(1+Z_ARR)**1.5
    if np.any(denom <= 0.01):
        return None
    arr = OL0*numer/denom
    return np.maximum(arr, 0.0)


# ---------------------------------------------------------------------------
# References
# ---------------------------------------------------------------------------

def make_LCDM(p):
    Om = p[0]; OL0 = 1.0-Om-OMEGA_R
    return np.full(len(Z_ARR), OL0)

def make_D1(p):
    """Previous batch winner. 3-param."""
    Om = p[0]; beta = p[1]; lam = max(p[2], 0.0)
    OL0 = 1.0-Om-OMEGA_R
    if OL0 < 0.01:
        return None
    E2 = OMEGA_R*(1+Z_ARR)**4 + Om*(1+Z_ARR)**3 + OL0
    E = np.sqrt(np.maximum(E2, 1e-15))
    intg = (1+Z_ARR)**3/E
    I_arr = np.zeros(len(Z_ARR))
    for i in range(1, len(Z_ARR)):
        dz = Z_ARR[i]-Z_ARR[i-1]
        I_arr[i] = I_arr[i-1]+0.5*(intg[i-1]+intg[i])*dz
    return OL0*(1.0+beta*(1.0-np.exp(-lam*Om*I_arr)))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print('=== L14 Batch-2: 30 new theories (Phases 11-20) ===')
    print('DESI DR2 7-bin chi2. H0=67.7 fixed.')
    print()

    results = {}

    s1 = [[Om] for Om in [0.290,0.300,0.310,0.315,0.320,0.330]]
    s2 = [[Om,A] for Om in [0.295,0.305,0.315,0.325]
                  for A in [-5.0,-2.0,-1.0,-0.5,-0.2,-0.1,0.0,0.1,0.2,0.5,1.0,2.0,5.0]]
    s3 = [[Om,A,B] for Om in [0.295,0.310,0.325]
                    for A in [-2.0,-0.5,0.0,0.5,1.0,2.0]
                    for B in [0.1,0.5,1.0,2.0,5.0]]
    s3b = [[Om,A,B] for Om in [0.295,0.310,0.325]
                     for A in [-1.0,-0.3,0.0,0.3,0.5,1.0]
                     for B in [0.1,0.3,0.5,1.0]]

    # References
    print('--- REFERENCES ---')
    p, c2, w0, wa, _ = fit_model(make_LCDM, 'LCDM     ', s1)
    results['LCDM'] = {'Om':p[0],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_D1, 'D1-prev  ', [[0.28,0.3,4.0],[0.28,0.25,3.0],[0.29,0.3,4.5]])
    results['D1_ref'] = {'Om':p[0],'chi2':c2,'w0':w0,'wa':wa}

    # Phase 11: BEC
    print('--- PHASE 11: BEC ---')
    p, c2, w0, wa, _ = fit_model(make_B1, 'B1-BEC   ', s3b)
    if p is not None: results['B1'] = {'Om':p[0],'A':p[1],'B':p[2],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_B2, 'B2-Order ', s2)
    if p is not None: results['B2'] = {'Om':p[0],'A':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_B3, 'B3-Bogol ', s2)
    if p is not None: results['B3'] = {'Om':p[0],'A':p[1],'chi2':c2,'w0':w0,'wa':wa}

    # Phase 12: Tunneling
    print('--- PHASE 12: Tunneling ---')
    p, c2, w0, wa, _ = fit_model(make_Q1, 'Q1-WKB   ', s2)
    if p is not None: results['Q1'] = {'Om':p[0],'A':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_Q2, 'Q2-Gamow ', s3b)
    if p is not None: results['Q2'] = {'Om':p[0],'A':p[1],'C':p[2],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_Q3, 'Q3-Reson ', s3b)
    if p is not None: results['Q3'] = {'Om':p[0],'A':p[1],'B':p[2],'chi2':c2,'w0':w0,'wa':wa}

    # Phase 13: SOC
    print('--- PHASE 13: SOC ---')
    p, c2, w0, wa, _ = fit_model(make_S1, 'S1-Aval  ', s2)
    if p is not None: results['S1'] = {'Om':p[0],'A':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_S2, 'S2-LogSOC', s3b)
    if p is not None: results['S2'] = {'Om':p[0],'A':p[1],'B':p[2],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_S3, 'S3-Atanh ', s3b)
    if p is not None: results['S3'] = {'Om':p[0],'A':p[1],'B':p[2],'chi2':c2,'w0':w0,'wa':wa}

    # Phase 14: Epidemic
    print('--- PHASE 14: Epidemic ---')
    p, c2, w0, wa, _ = fit_model(make_EP1, 'EP1-SIR  ', s2)
    if p is not None: results['EP1'] = {'Om':p[0],'A':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_EP2, 'EP2-SIS  ', s2)
    if p is not None: results['EP2'] = {'Om':p[0],'A':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_EP3, 'EP3-SIRv ', s3b)
    if p is not None: results['EP3'] = {'Om':p[0],'A':p[1],'B':p[2],'chi2':c2,'w0':w0,'wa':wa}

    # Phase 15: Polymer
    print('--- PHASE 15: Polymer ---')
    p, c2, w0, wa, _ = fit_model(make_PL1, 'PL1-Flory', s2)
    if p is not None: results['PL1'] = {'Om':p[0],'A':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_PL2, 'PL2-deGen', s2)
    if p is not None: results['PL2'] = {'Om':p[0],'nu':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_PL3, 'PL3-Zimm ', s2)
    if p is not None: results['PL3'] = {'Om':p[0],'A':p[1],'chi2':c2,'w0':w0,'wa':wa}

    # Phase 16: Stochastic
    print('--- PHASE 16: Stochastic ---')
    p, c2, w0, wa, _ = fit_model(make_N1, 'N1-FP    ', s2)
    if p is not None: results['N1'] = {'Om':p[0],'A':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_N2, 'N2-Noise ', s2)
    if p is not None: results['N2'] = {'Om':p[0],'A':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_N3, 'N3-SR    ', s3b)
    if p is not None: results['N3'] = {'Om':p[0],'A':p[1],'B':p[2],'chi2':c2,'w0':w0,'wa':wa}

    # Phase 17: Holography
    print('--- PHASE 17: Holography ---')
    p, c2, w0, wa, _ = fit_model(make_H1, 'H1-RT    ', s2)
    if p is not None: results['H1'] = {'Om':p[0],'nu':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_H2, 'H2-Page  ', s3b)
    if p is not None: results['H2'] = {'Om':p[0],'A':p[1],'B':p[2],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_H3, 'H3-Screen', s2)
    if p is not None: results['H3'] = {'Om':p[0],'A':p[1],'chi2':c2,'w0':w0,'wa':wa}

    # Phase 18: QEC
    print('--- PHASE 18: QEC ---')
    p, c2, w0, wa, _ = fit_model(make_QE1, 'QE1-Thr  ', s2)
    if p is not None: results['QE1'] = {'Om':p[0],'A':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_QE2, 'QE2-Toric', s3)
    if p is not None: results['QE2'] = {'Om':p[0],'A':p[1],'B':p[2],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_QE3, 'QE3-Surf ', s3b)
    if p is not None: results['QE3'] = {'Om':p[0],'A':p[1],'B':p[2],'chi2':c2,'w0':w0,'wa':wa}

    # Phase 19: Tensor Network
    print('--- PHASE 19: Tensor Network ---')
    p, c2, w0, wa, _ = fit_model(make_TN1, 'TN1-MERA ', s2)
    if p is not None: results['TN1'] = {'Om':p[0],'A':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_TN2, 'TN2-Bond ', s2)
    if p is not None: results['TN2'] = {'Om':p[0],'A':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_TN3, 'TN3-Cone ', s2)
    if p is not None: results['TN3'] = {'Om':p[0],'A':p[1],'chi2':c2,'w0':w0,'wa':wa}

    # Phase 20: Quantum Walk
    print('--- PHASE 20: Quantum Walk ---')
    p, c2, w0, wa, _ = fit_model(make_W1, 'W1-Grover', s2)
    if p is not None: results['W1'] = {'Om':p[0],'A':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_W2, 'W2-AndLoc', s3b)
    if p is not None: results['W2'] = {'Om':p[0],'A':p[1],'B':p[2],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_W3, 'W3-QWalk ', s2)
    if p is not None: results['W3'] = {'Om':p[0],'A':p[1],'chi2':c2,'w0':w0,'wa':wa}

    # Summary
    chi2_lcdm = results.get('LCDM',{}).get('chi2', 13.198)
    chi2_d1   = results.get('D1_ref',{}).get('chi2', 10.984)

    print()
    print('=== BATCH-2 SUMMARY ===')
    print('LCDM chi2=%.3f  D1-prev chi2=%.3f' % (chi2_lcdm, chi2_d1))
    print()
    fmt = '{:<12} chi2={:<8} dLCDM={:<8} dD1={:<8} w0={:<8} wa={:<8} STATUS'
    print(fmt.format('Model','chi2','dLCDM','dD1','w0','wa'))
    print('-'*80)
    new_best = []
    for k, r in sorted(results.items(), key=lambda x: x[1].get('chi2',1e9)):
        c2v = r.get('chi2', float('nan'))
        dl  = round(c2v-chi2_lcdm, 3) if np.isfinite(chi2_lcdm) else float('nan')
        dd1 = round(c2v-chi2_d1, 3) if np.isfinite(chi2_d1) else float('nan')
        w0v = r.get('w0', float('nan'))
        wav = r.get('wa', float('nan'))
        status = 'KILL'
        if np.isfinite(c2v) and c2v < chi2_lcdm:
            status = 'PASS'
            if c2v < chi2_d1:
                status = 'NEW-BEST!'
                new_best.append(k)
            if c2v < 11.468 and np.isfinite(wav) and wav < -0.5:
                status = 'GAME-CHANGER!'
        print(fmt.format(k, round(c2v,3), dl, dd1,
                         round(w0v,3) if np.isfinite(w0v) else 'nan',
                         round(wav,3) if np.isfinite(wav) else 'nan') + '  ' + status)

    if new_best:
        print()
        print('NEW BEST models (chi2 < D1 %.3f):' % chi2_d1)
        for k in new_best:
            r = results[k]
            print('  %s: chi2=%.3f  wa=%.3f' % (k, r.get('chi2',float('nan')), r.get('wa',float('nan'))))

    out = os.path.join(_THIS, 'l14_new30b_results.json')
    def _j(v):
        if isinstance(v, (np.floating, np.integer)):
            return float(v)
        if isinstance(v, float) and not np.isfinite(v):
            return None
        return v
    clean = {k:{rk:_j(rv) for rk,rv in r.items()} for k,r in results.items()}
    with open(out, 'w') as f:
        json.dump(clean, f, indent=2)
    print()
    print('Saved: ' + out)
    return results


if __name__ == '__main__':
    main()
