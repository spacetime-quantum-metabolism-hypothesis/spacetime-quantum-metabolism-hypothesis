# -*- coding: utf-8 -*-
"""
L14 Batch-6: 30 more new theories from A1+A2. Phases 51-60.
Focus: cos/oscillatory variants (AX3 family) + novel frameworks.

Phase 51: Josephson junction / Cooper pair (JJ1-JJ3)
Phase 52: Random matrix / Wigner (RM1-RM3)
Phase 53: KPZ / surface growth (KP1-KP3)
Phase 54: Fokker-Planck steady state (FP1-FP3)
Phase 55: Chern-Simons / topological field (CS1-CS3)
Phase 56: Quantum Fisher information (QF1-QF3)
Phase 57: Holographic entanglement wedge (GD1-GD3)
Phase 58: Chiral anomaly / Berry phase (AN1-AN3)
Phase 59: Emergent dark energy cos integral (EE1-EE3)
Phase 60: Superfluid vortex density (SF1-SF3)
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
                       options={'xatol':1e-6,'fatol':1e-6,'maxiter':5000})
        if res.fun < best[0]:
            best = (res.fun, res.x)
    if best[1] is None:
        return None
    p = best[1]
    Om = float(np.clip(p[0], 0.28, 0.36))
    arr = make_fn(p)
    if arr is None:
        return None
    chi2 = chi2_from_ode(Z_ARR, arr, Om)
    w0, wa = fit_cpl(Z_ARR, arr)
    return {'chi2': chi2, 'w0': w0, 'wa': wa, 'p': [float(x) for x in p]}


def _E_LCDM(Om, z_arr):
    return np.sqrt(OMEGA_R*(1+z_arr)**4 + Om*(1+z_arr)**3 + (1-Om-OMEGA_R))


def _precompute_integrals(Om, z_arr):
    OL0 = 1.0-Om-OMEGA_R
    E2  = OMEGA_R*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E   = np.sqrt(np.maximum(E2, 1e-15))
    integrand = (1+z_arr)**3 / np.maximum(E, 1e-10)
    I = np.zeros(len(z_arr))
    for i in range(1, len(z_arr)):
        dz = z_arr[i] - z_arr[i-1]
        I[i] = I[i-1] + 0.5*(integrand[i-1]+integrand[i])*dz
    return E, I


def make_D1_ref(p):
    Om=p[0]; beta=p[1]; lam=max(p[2],0.0)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    _, I_arr = _precompute_integrals(Om, Z_ARR)
    return OL0*(1.0+beta*(1.0-np.exp(-lam*Om*I_arr)))

def make_AX3_ref(p):
    """AX3 reference (Batch-5 best chi2=9.103)."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    theta_z = B*(Om*(1+Z_ARR)**3-Om)/max(OL0, 1e-10)
    return OL0*(1.0+A*(1.0-np.cos(np.minimum(theta_z, 20))))


# ============================================================
# Phase 51: Josephson junction / Cooper pair tunneling
# A1: 시공간 양자 = Cooper pair 위상 코히어런스.
# 물질 = Josephson 접합 바이어스. 공리 A2 = 임계전류 = QC 경계.
# ============================================================

def make_JJ1(p):
    """JJ1: Josephson phase-energy relation.
    omega_de = OL0*(1+A*(1-cos(B*Om*(1+z)^3/OL0))).
    A1: Josephson energy E_J*(1-cos(phi)). phi = B*rho_m/rho_DE.
    Variant of AX3 but without the -Om offset (grows faster)."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    theta_z = B*Om*(1+Z_ARR)**3/max(OL0, 1e-10)
    theta_0 = B*Om/max(OL0, 1e-10)
    return OL0*(1.0+A*(np.cos(np.minimum(theta_0, 20))-np.cos(np.minimum(theta_z, 20))))


def make_JJ2(p):
    """JJ2: AC Josephson oscillation.
    omega_de = OL0*(1+A*sin^2(B*(1+z)^(3/2))).
    Same as CD1/LQ1 but different starting point. B freely tuned."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    theta_z = B*(1+Z_ARR)**(1.5)
    theta_0 = B
    return OL0*(1.0+A*(np.sin(theta_z)**2-np.sin(theta_0)**2))


def make_JJ3(p):
    """JJ3: Josephson plasma resonance.
    omega_de = OL0*(1+A*(1-cos(B*(E_LCDM^2-1)))).
    Same as AX1 structure but reparametrized A1 as Josephson plasma."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    return OL0*(1.0+A*(1.0-np.cos(np.minimum(B*(E**2-1.0), 20))))


# ============================================================
# Phase 52: Random matrix / Wigner semicircle
# A1: 시공간 양자 밀도 = RMT 고유값 분포. 물질 = 행렬 원소.
# 공리 A2 = 위그너 반원 가장자리 = QC 경계.
# ============================================================

def make_RM1(p):
    """RM1: Wigner semicircle density.
    omega_de = OL0*(1+A*sqrt(1-((E_LCDM(z)-1)/B)^2)) for E<1+B, else OL0.
    A1: eigenvalue density ~ sqrt(1-(x/2R)^2). Finite support [1, 1+B]."""
    Om=p[0]; A=p[1]; B=max(p[2],0.1)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    x = (E-1.0)/B
    under = np.maximum(1.0-x**2, 0)
    f_z = np.sqrt(under)
    f_0 = 1.0  # E(0)=1, x=0, sqrt(1)=1
    return OL0*(1.0+A*(f_z-f_0))


def make_RM2(p):
    """RM2: March-Pastur distribution.
    omega_de = OL0*(1+A*sqrt((B-x)(x-1/B))/x) where x=Om*(1+z)^3/OL0.
    For x in [1/B, B]. MP density for random Wishart matrices."""
    Om=p[0]; A=p[1]; B=max(p[2],1.1)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    x_z = np.maximum(Om*(1+Z_ARR)**3/max(OL0, 1e-10), 1e-10)
    x_0 = Om/max(OL0, 1e-10)
    lo = 1.0/B; hi = B
    under = np.maximum((hi-x_z)*(x_z-lo), 0)
    f_z = np.sqrt(under)/x_z
    under0 = max((hi-x_0)*(x_0-lo), 0)
    f_0 = np.sqrt(under0)/max(x_0, 1e-10)
    return OL0*(1.0+A*(f_z-f_0))


def make_RM3(p):
    """RM3: GUE level spacing.
    omega_de = OL0*(1+A*(E_LCDM(z)-1)^2*exp(-B*(E_LCDM(z)-1)^2)).
    A1: Wigner surmise P(s)=pi*s/2*exp(-pi*s^2/4). Similar shape."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    x = E - 1.0
    return OL0*(1.0+A*x**2*np.exp(-B*x**2))


# ============================================================
# Phase 53: KPZ / surface growth
# A1: 시공간 양자 = 성장 계면 높이. 물질 = 증착 원천.
# 공리 A2 = KPZ 거친화 전이 = QC 경계.
# ============================================================

def make_KP1(p):
    """KP1: KPZ 1/3 exponent growth.
    omega_de = OL0*(1+A*((1+z)^(1/3)-1)).
    A1: KPZ surface width ~ t^(1/3). In redshift: width ~ (1+z)^(1/3)."""
    Om=p[0]; A=p[1]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    return OL0*(1.0+A*((1+Z_ARR)**(1.0/3.0)-1.0))


def make_KP2(p):
    """KP2: Edwards-Wilkinson (linear KPZ).
    omega_de = OL0*(1+A*((1+z)^(1/4)-1)).
    A1: EW exponent 1/4 for diffusion-dominated surface."""
    Om=p[0]; A=p[1]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    return OL0*(1.0+A*((1+Z_ARR)**(0.25)-1.0))


def make_KP3(p):
    """KP3: KPZ with nonlinear saturation.
    omega_de = OL0*(1+A*(1-exp(-B*(1+z)^(1/3)))).
    A1: KPZ growth saturates at 1. Integrated effect."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    f_z = 1.0-np.exp(-B*(1+Z_ARR)**(1.0/3.0))
    f_0 = 1.0-np.exp(-B)
    return OL0*(1.0+A*(f_z-f_0))


# ============================================================
# Phase 54: Fokker-Planck steady state
# A1: 시공간 양자 = 확산 확률 밀도 정류 상태.
# 물질 = 외부 힘 (드리프트). 공리 A2 = 정류 확률 = QC 경계.
# ============================================================

def make_FP1(p):
    """FP1: Ornstein-Uhlenbeck steady state.
    omega_de = OL0*(1+A*(1-exp(-B*(E_LCDM(z)-1)))).
    A1: FP stationary distribution ~ exp(-V(x)) with V=B*(E-1).
    Saturating exponential growth."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    f_z = 1.0-np.exp(-B*(E-1.0))
    return OL0*(1.0+A*f_z)


def make_FP2(p):
    """FP2: Double-well FP stationary.
    omega_de = OL0*(1+A*arctan(B*(Om*(1+z)^3-Om)/OL0)).
    A1: double-well escape ~ arctan saturation. Grows then saturates."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    x_z = B*(Om*(1+Z_ARR)**3-Om)/max(OL0, 1e-10)
    return OL0*(1.0+A*np.arctan(x_z))


def make_FP3(p):
    """FP3: Kramers escape rate.
    omega_de = OL0*(1+A*exp(-B/E_LCDM(z))*(E_LCDM(z)-1)).
    A1: Kramers rate ~ exp(-B/E)*(E-1). Activation energy B, amplitude E-1."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    x = E - 1.0
    f_z = np.exp(-B/np.maximum(E, 1e-10))*x
    f_0 = np.exp(-B)*0.0  # E(0)=1, x=0
    return OL0*(1.0+A*(f_z-f_0))


# ============================================================
# Phase 55: Chern-Simons / topological field theory
# A1: 시공간 양자 = CS 위상 불변량. 물질 = 게이지 플럭스.
# 공리 A2 = Chern 수 전이 = QC 경계.
# ============================================================

def make_CT1(p):
    """CT1: Chern-Simons level shift.
    omega_de = OL0*(1+A*sin^2(B*E_LCDM(z))).
    A1: CS action S = k/(4pi)*int A^dA. Quantized level k. Dark energy ~ sin^2(k*phase)."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    f_z = np.sin(B*E)**2
    f_0 = np.sin(B)**2
    return OL0*(1.0+A*(f_z-f_0))


def make_CT2(p):
    """CT2: Berry phase holonomy.
    omega_de = OL0*(1+A*(1-cos(B*sqrt(Om*(1+z)^3/OL0)))).
    A1: Berry phase gamma = B*sqrt(matter/vacuum). (1-cos(gamma)) ~ oscillation."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    r_z = np.sqrt(np.maximum(Om*(1+Z_ARR)**3/max(OL0, 1e-10), 0))
    r_0 = np.sqrt(Om/max(OL0, 1e-10))
    return OL0*(1.0+A*(np.cos(B*r_0)-np.cos(np.minimum(B*r_z, 20))))


def make_CT3(p):
    """CT3: Chern number winding.
    omega_de = OL0*(1+A*sin(B*(E_LCDM-1))*cos(B*(E_LCDM-1))).
    = OL0*(1+A/2*sin(2B*(E-1))). Oscillatory, zero at E=1."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    x = E - 1.0
    return OL0*(1.0+A*np.sin(np.minimum(2.0*B*x, 20)))


# ============================================================
# Phase 56: Quantum Fisher information
# A1: 시공간 양자 = 양자 Fisher 메트릭 원소.
# 물질 = 매개변수 추정 정밀도. 공리 A2 = Heisenberg 한계 = QC 경계.
# ============================================================

def make_QF1(p):
    """QF1: Fisher saturating form.
    omega_de = OL0*(1+A*(E_LCDM^2-1)/(1+B*(E_LCDM^2-1))).
    A1: QFI F ~ Delta^2/(1+Bdelta^2). Saturates at A/B for large delta."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    x = E**2 - 1.0
    return OL0*(1.0+A*x/np.maximum(1.0+B*x, 1e-10))


def make_QF2(p):
    """QF2: Quantum Cramer-Rao bound.
    omega_de = OL0*(1+A*(1-1/(1+B*(E_LCDM-1))^2)).
    A1: estimation variance 1/F_Q ~ 1/(1+B*(E-1))^2. CR bound saturating."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    f_z = 1.0-1.0/np.maximum((1.0+B*(E-1.0))**2, 1e-10)
    return OL0*(1.0+A*f_z)


def make_QF3(p):
    """QF3: Fisher log growth.
    omega_de = OL0*(1+A*ln(1+B*(E_LCDM(z)-1))).
    A1: QFI logarithm growth. Classical -> quantum Fisher transition."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    return OL0*(1.0+A*np.log(np.maximum(1.0+B*(E-1.0), 1e-10)))


# ============================================================
# Phase 57: Holographic entanglement wedge
# A1: 시공간 양자 = Ryu-Takayanagi 극소 곡면 넓이.
# 물질 = 경계 엔트로피. 공리 A2 = 페이지 곡선 전이 = QC 경계.
# ============================================================

def make_GD1(p):
    """GD1: RT surface area cos-modulated.
    omega_de = OL0*(1+A*(1-cos(B*I_D1(z)))).
    A1: entanglement entropy S_EE ~ B*integral = B*I(z) (D1 integral).
    1-cos(S_EE) encodes Page-curve periodicity."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    _, I_arr = _precompute_integrals(Om, Z_ARR)
    theta = B*Om*I_arr  # same as D1 integral
    return OL0*(1.0+A*(1.0-np.cos(np.minimum(theta, 20))))


def make_GD2(p):
    """GD2: Entanglement wedge saturation.
    omega_de = OL0*(1+A*(1-exp(-B*I^2))).
    A1: EW entropy ~ 1-exp(-I^2/xi^2). Grows then saturates with integral I."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    _, I_arr = _precompute_integrals(Om, Z_ARR)
    sigma = Om*I_arr
    return OL0*(1.0+A*(1.0-np.exp(-B*sigma**2)))


def make_GD3(p):
    """GD3: Holographic complexity.
    omega_de = OL0*(1+A*(I^B-I0^B)) where I=Om*integral(1+z)^3/E.
    A1: holographic complexity ~ Volume^B. Power law growth."""
    Om=p[0]; A=p[1]; B=max(p[2],0.1)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    _, I_arr = _precompute_integrals(Om, Z_ARR)
    sigma = Om*I_arr
    I0 = sigma[0] if sigma[0] > 1e-10 else 1e-10
    # sigma[0] = 0 by construction, so I0=0 -> singularity for B<1
    # Use sigma+eps
    return OL0*(1.0+A*((sigma+1e-3)**B - (1e-3)**B))


# ============================================================
# Phase 58: Chiral anomaly / Berry phase
# A1: 시공간 양자 = 카이랄 비정상 플럭스. 물질 = 위상 결함.
# 공리 A2 = 아노말리 상쇄 = QC 경계.
# ============================================================

def make_AN1(p):
    """AN1: Chiral anomaly cos-sqrt.
    omega_de = OL0*(1+A*(1-cos(B*sqrt(Om*(1+z)^3-Om)/OL0))).
    A1: anomaly ~ cos(theta) with theta=B*sqrt(delta_rho/rho_DE)."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    delta = np.maximum(Om*(1+Z_ARR)**3-Om, 0)
    theta_z = B*np.sqrt(delta/max(OL0, 1e-10))
    return OL0*(1.0+A*(1.0-np.cos(np.minimum(theta_z, 20))))


def make_AN2(p):
    """AN2: Berry curvature integral.
    omega_de = OL0*(1+A*(1-cos(B*(E_LCDM-1)^(1/2)))).
    A1: Berry phase ~ B*sqrt(E-1). (1-cos) encodes Aharonov-Bohm-like accumulation."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    theta_z = B*np.sqrt(np.maximum(E-1.0, 0))
    return OL0*(1.0+A*(1.0-np.cos(np.minimum(theta_z, 20))))


def make_AN3(p):
    """AN3: Wess-Zumino-Witten term.
    omega_de = OL0*(1+A*(1-cos(B*I_D1(z)^(1/2)))).
    A1: WZW level k ~ sqrt(integral). 1-cos oscillates."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    _, I_arr = _precompute_integrals(Om, Z_ARR)
    sigma = Om*I_arr
    theta_z = B*np.sqrt(np.maximum(sigma, 0))
    return OL0*(1.0+A*(1.0-np.cos(np.minimum(theta_z, 20))))


# ============================================================
# Phase 59: Emergent dark energy cosine family
# A1: 시공간 양자 = 집단 자유도 위상. 물질 = 위상 변화율.
# 다양한 cos 변형으로 D1 integral 활용.
# ============================================================

def make_EE1(p):
    """EE1: Cos in D1 integral (AX3 variant).
    omega_de = OL0*(1+A*(1-cos(B*Om*I(z)))).
    Same as GD1 but without the sqrt."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    _, I_arr = _precompute_integrals(Om, Z_ARR)
    theta = B*Om*I_arr
    return OL0*(1.0+A*(1.0-np.cos(np.minimum(theta, 20))))


def make_EE2(p):
    """EE2: Cos in log(E).
    omega_de = OL0*(1+A*(1-cos(B*ln(E_LCDM(z))))).
    A1: phase accumulation ~ B*ln(E). Log-oscillatory."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    theta_z = B*np.log(np.maximum(E, 1e-10))
    return OL0*(1.0+A*(1.0-np.cos(np.minimum(theta_z, 20))))


def make_EE3(p):
    """EE3: Cos in cuberoot matter fraction.
    omega_de = OL0*(1+A*(1-cos(B*(Om*(1+z)^3/OL0)^(1/3)))).
    A1: phase ~ (rho_m/rho_DE)^(1/3). Different power from AX3."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    r_z = (np.maximum(Om*(1+Z_ARR)**3/max(OL0, 1e-10), 0))**(1.0/3.0)
    r_0 = (Om/max(OL0, 1e-10))**(1.0/3.0)
    return OL0*(1.0+A*(np.cos(B*r_0)-np.cos(np.minimum(B*r_z, 20))))


# ============================================================
# Phase 60: Superfluid vortex density (different from vortex Phase 9)
# A1: 시공간 양자 = 초유체 와류 선속 밀도.
# 물질 = 쌍소멸 원천. 공리 A2 = 베레진스키 전이 = QC 경계.
# ============================================================

def make_SF1(p):
    """SF1: Superfluid 2/3-power cos.
    omega_de = OL0*(1+A*(1-cos(B*E_LCDM(z)^(2/3)))).
    A1: superfluid coherence ~ cos(B*E^(2/3)). Kolmogorov spectrum."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    f_z = 1.0-np.cos(np.minimum(B*E**(2.0/3.0), 20))
    f_0 = 1.0-np.cos(B)
    return OL0*(1.0+A*(f_z-f_0))


def make_SF2(p):
    """SF2: Vortex nucleation threshold.
    omega_de = OL0*(1+A*(1-exp(-B*(E_LCDM-1)^(1/2)))).
    A1: vortex nucleation rate ~ 1-exp(-B*sqrt(E-1)). Half-power threshold."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    f_z = 1.0-np.exp(-B*np.sqrt(np.maximum(E-1.0, 0)))
    return OL0*(1.0+A*f_z)


def make_SF3(p):
    """SF3: Superfluid healing length.
    omega_de = OL0*(1+A*(E_LCDM(z)^(1/2)-1)).
    A1: healing length xi ~ 1/sqrt(n) ~ 1/sqrt(E). Dark energy ~ sqrt(E)-1."""
    Om=p[0]; A=p[1]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    return OL0*(1.0+A*(np.sqrt(E)-1.0))


# ============================================================
# MAIN
# ============================================================

print("=== L14 Batch-6: 30 new theories (Phases 51-60) ===")
print("DESI DR2 7-bin chi2. H0=67.7 fixed.\n")

print("--- REFERENCES ---")
_r = fit_model(make_D1_ref, 'D1-prev',
               [[0.28, 0.30, 4.0], [0.30, 0.50, 3.0]])
if _r:
    print(f"D1-prev    chi2={_r['chi2']:.3f}  w0={_r['w0']:.3f}  wa={_r['wa']:.3f}")
_r2 = fit_model(make_AX3_ref, 'AX3-ref',
                [[0.28, 0.186, 2.433], [0.28, 0.2, 2.5], [0.28, 0.15, 3.0]])
if _r2:
    print(f"AX3-ref    chi2={_r2['chi2']:.3f}  w0={_r2['w0']:.3f}  wa={_r2['wa']:.3f}")

MODELS = [
    # Phase 51: Josephson
    ('JJ1-JosephE', make_JJ1, [[0.28, 0.2, 2.5], [0.28, 0.15, 3.0], [0.28, 0.3, 2.0],
                                [0.28, 0.1, 4.0]]),
    ('JJ2-JosephAC',make_JJ2, [[0.28, 0.5, 0.5], [0.28, 0.4, 0.6], [0.28, 0.3, 0.7]]),
    ('JJ3-JosephPR',make_JJ3, [[0.28, 0.2, 3.0], [0.28, 0.15, 3.5], [0.28, 0.25, 2.5]]),
    # Phase 52: Random matrix
    ('RM1-Wigner',  make_RM1, [[0.28, -0.5, 0.5], [0.28, -1.0, 1.0], [0.28, -0.3, 0.3]]),
    ('RM2-MarchPas',make_RM2, [[0.28, 0.5, 2.0], [0.28, 1.0, 3.0], [0.28, 0.3, 1.5]]),
    ('RM3-GUElevl', make_RM3, [[0.28, 1.0, 1.0], [0.28, 2.0, 0.5], [0.28, 3.0, 0.3]]),
    # Phase 53: KPZ
    ('KP1-KPZ13',   make_KP1, [[0.28, 0.5], [0.28, 1.0], [0.28, -0.5], [0.28, 2.0]]),
    ('KP2-EW14',    make_KP2, [[0.28, 0.5], [0.28, 1.0], [0.28, -0.5]]),
    ('KP3-KPZsat',  make_KP3, [[0.28, 0.5, 1.0], [0.28, 1.0, 0.5], [0.28, 0.3, 2.0]]),
    # Phase 54: Fokker-Planck
    ('FP1-OU',      make_FP1, [[0.28, 0.5, 1.0], [0.28, 1.0, 0.5], [0.28, 0.3, 2.0]]),
    ('FP2-DblWell', make_FP2, [[0.28, 0.3, 1.0], [0.28, 0.5, 0.5], [0.28, 0.2, 2.0]]),
    ('FP3-Kramers', make_FP3, [[0.28, 1.0, 1.0], [0.28, 0.5, 2.0], [0.28, 2.0, 0.5]]),
    # Phase 55: Chern-Simons
    ('CT1-CSsin2',  make_CT1, [[0.28, 0.5, 1.0], [0.28, 0.3, 1.5], [0.28, 0.7, 0.7]]),
    ('CT2-BerryPh', make_CT2, [[0.28, 0.3, 1.0], [0.28, 0.5, 0.5], [0.28, 0.2, 1.5]]),
    ('CT3-WindNum', make_CT3, [[0.28, 0.3, 1.0], [0.28, 0.5, 0.5], [0.28, 0.2, 2.0]]),
    # Phase 56: Quantum Fisher
    ('QF1-FisherS',  make_QF1, [[0.28, 0.5, 0.5], [0.28, 1.0, 0.3], [0.28, 0.3, 1.0]]),
    ('QF2-CRbound',  make_QF2, [[0.28, 0.5, 1.0], [0.28, 1.0, 0.5], [0.28, 0.3, 2.0]]),
    ('QF3-FisherL',  make_QF3, [[0.28, 0.5, 1.0], [0.28, 1.0, 0.5], [0.28, 0.3, 2.0]]),
    # Phase 57: Holographic
    ('GD1-RTcos',   make_GD1, [[0.28, 0.2, 2.5], [0.28, 0.15, 3.0], [0.28, 0.3, 2.0]]),
    ('GD2-EWsat',   make_GD2, [[0.28, 0.5, 0.5], [0.28, 0.3, 1.0], [0.28, 0.7, 0.3]]),
    ('GD3-HoloC',   make_GD3, [[0.28, 0.2, 0.5], [0.28, 0.1, 0.3], [0.28, 0.3, 0.7]]),
    # Phase 58: Chiral anomaly
    ('AN1-ChiAno',  make_AN1, [[0.28, 0.3, 1.5], [0.28, 0.5, 1.0], [0.28, 0.2, 2.0]]),
    ('AN2-BerryC',  make_AN2, [[0.28, 0.3, 2.0], [0.28, 0.5, 1.5], [0.28, 0.2, 3.0]]),
    ('AN3-WZW',     make_AN3, [[0.28, 0.3, 2.0], [0.28, 0.5, 1.5], [0.28, 0.2, 3.0]]),
    # Phase 59: Emergent DE cos
    ('EE1-CosInt',  make_EE1, [[0.28, 0.2, 2.5], [0.28, 0.15, 3.0], [0.28, 0.3, 2.0]]),
    ('EE2-CosLog',  make_EE2, [[0.28, 0.5, 2.0], [0.28, 1.0, 1.5], [0.28, 0.3, 3.0]]),
    ('EE3-CosCbrt', make_EE3, [[0.28, 0.3, 1.5], [0.28, 0.5, 1.0], [0.28, 0.2, 2.0]]),
    # Phase 60: Superfluid
    ('SF1-SFcos23', make_SF1, [[0.28, 0.5, 1.0], [0.28, 0.3, 1.5], [0.28, 0.7, 0.7]]),
    ('SF2-VortNuc', make_SF2, [[0.28, 0.5, 1.0], [0.28, 1.0, 0.5], [0.28, 0.3, 2.0]]),
    ('SF3-SFsqrtE', make_SF3, [[0.28, 0.5], [0.28, 1.0], [0.28, -0.5]]),
]

results = {}
rows = []

for label, fn, starts in MODELS:
    r = fit_model(fn, label, starts)
    if r is None:
        print(f"{label:<14} FAILED")
        continue
    chi2 = r['chi2']
    w0   = round(r['w0'], 3)
    wa   = round(r['wa'], 3)
    p    = r['p']
    print(f"{label:<14} p={p}  chi2={chi2:.3f}  w0={w0}  wa={wa}")
    results[label] = r
    rows.append((label, chi2, w0, wa))

LCDM_CHI2 = 13.198
D1_CHI2   = 10.984
C14_CHI2  = 11.468
AX3_CHI2  = 9.103  # new best from Batch-5

print("\n=== BATCH-6 SUMMARY ===")
print(f"LCDM chi2={LCDM_CHI2}  AX3-best chi2={AX3_CHI2}\n")
rows.sort(key=lambda x: x[1])
print(f"{'Model':<15} {'chi2':<8} {'dLCDM':<10} {'dAX3':<10} {'w0':<9} {'wa':<9} STATUS")
print('-'*78)
game_changers = []; new_bests = []
for lbl, chi2, w0, wa in rows:
    dc = chi2 - LCDM_CHI2
    da = chi2 - AX3_CHI2
    if chi2 < C14_CHI2 and wa < -0.5:
        st = 'GAME-CHANGER!'
        if chi2 < AX3_CHI2: st = 'NEW-RECORD!'
        game_changers.append((lbl, chi2, w0, wa))
    elif chi2 < AX3_CHI2:
        st = 'NEW-RECORD!'
        new_bests.append((lbl, chi2, w0, wa))
    elif chi2 < D1_CHI2:
        st = 'NEW-BEST!'
        new_bests.append((lbl, chi2, w0, wa))
    elif chi2 < LCDM_CHI2:
        st = 'PASS'
    else:
        st = 'KILL'
    print(f"{lbl:<15} {chi2:<8.3f} {dc:<10.3f} {da:<10.3f} {w0:<9.3f} {wa:<9.3f} {st}")

print(f"{'LCDM':<15} {LCDM_CHI2:<8.3f} {0.0:<10.3f} {LCDM_CHI2-AX3_CHI2:<10.3f} {-1.0:<9.3f} {0.0:<9.3f} KILL")

if [x for x in game_changers if x[1]<AX3_CHI2]:
    print(f"\nNEW RECORD (chi2 < AX3={AX3_CHI2} AND wa<-0.5):")
    for lbl, chi2, w0, wa in game_changers:
        if chi2 < AX3_CHI2:
            print(f"  {lbl}: chi2={chi2:.3f}  w0={w0}  wa={wa}")
if game_changers:
    print(f"\nGAME-CHANGER (chi2<{C14_CHI2} AND wa<-0.5):")
    for lbl, chi2, w0, wa in game_changers:
        print(f"  {lbl}: chi2={chi2:.3f}  w0={w0}  wa={wa}")
if new_bests:
    print(f"\nNEW BEST chi2:")
    for lbl, chi2, w0, wa in new_bests:
        print(f"  {lbl}: chi2={chi2:.3f}  wa={wa:.3f}")

out_path = os.path.join(_THIS, 'l14_new30f_results.json')
def _j(v):
    if isinstance(v,(np.floating,np.float64,np.float32)): return float(v)
    if isinstance(v,(np.integer,)): return int(v)
    if isinstance(v,list): return [_j(x) for x in v]
    return v
save={k:{kk:_j(vv) for kk,vv in val.items()} for k,val in results.items()}
with open(out_path,'w') as f: json.dump(save,f,indent=2)
print(f"\nSaved: {out_path}")
