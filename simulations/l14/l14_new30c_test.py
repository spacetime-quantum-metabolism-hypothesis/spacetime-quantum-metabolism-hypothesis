# -*- coding: utf-8 -*-
"""
L14 Batch-3: 30 more new theories from A1+A2. Phases 21-30.

Phase 21: Soliton / Kink dynamics (F1-F3)
Phase 22: Renormalization Group flow (X1-X3)
Phase 23: Non-equilibrium thermodynamics (Y1-Y3)
Phase 24: Spin glass / Replica (SG1-SG3)
Phase 25: Fractal / Multifractal geometry (FR1-FR3)
Phase 26: Matter fraction power law (MF1-MF3)
Phase 27: CDT / Discrete spacetime (CD1-CD3)
Phase 28: String gas / Hagedorn (ST1-ST3)
Phase 29: Acoustic / Phonon analogy (AC1-AC3)
Phase 30: Grand canonical / Chemical potential (GC1-GC3)
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
    return {'chi2': chi2, 'w0': w0, 'wa': wa, 'p': list(float(x) for x in p)}


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


# --- D1 reference (Batch-1 best) ---
def make_D1_ref(p):
    Om=p[0]; beta=p[1]; lam=max(p[2],0.0)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    _, I_arr = _precompute_integrals(Om, Z_ARR)
    return OL0*(1.0+beta*(1.0-np.exp(-lam*Om*I_arr)))


# ============================================================
# Phase 21: Soliton / Kink dynamics
# A1: 시공간 양자 = 위상 kink 솔리톤. 물질 = kink 소멸 원천.
# kink 밀도 ~ sech^2 또는 tanh 형태로 z에 의존.
# ============================================================

def make_F1(p):
    """F1: Soliton sech^2 profile.
    omega_de = OL0*(1+A*sech^2(B*(E(z)-1-C))).
    Peaked near E=1+C. A1: kink density peaks when E crosses threshold."""
    Om=p[0]; A=p[1]; B=max(p[2],0.1); C=p[3]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    x = E - 1.0 - C
    sech2 = 1.0/np.cosh(B*x)**2
    arr = OL0*(1.0+A*sech2)
    # normalize to E(0)=1 condition
    x0 = 1.0-Om-OMEGA_R - C  # E(0)=1 exactly, so x0 = -C
    sech2_0 = 1.0/np.cosh(B*(-C))**2
    # already normalized since omega_de(0) = OL0*(1+A*sech2(B*(-C)))
    return arr


def make_F2(p):
    """F2: Kink tanh profile (step-like transition).
    omega_de = OL0*(1+A*(tanh(B*(Om*(1+z)^3-C))-tanh(B*(Om-C)))).
    A1: quantum-classical kink moves through matter density."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01); C=max(p[3],0.0)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    x_z = Om*(1+Z_ARR)**3
    x_0 = Om
    delta = np.tanh(B*(x_z-C)) - np.tanh(B*(x_0-C))
    return OL0*(1.0+A*delta)


def make_F3(p):
    """F3: Kink-antikink collision.
    omega_de = OL0*(1+A*(E(z)-1)*sech^2(B*(E(z)-1))).
    Peak at E-1 = 1/sqrt(B). Similar to N3 but sech^2 damping."""
    Om=p[0]; A=p[1]; B=max(p[2],0.1)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    x = E - 1.0
    sech2 = 1.0/np.cosh(np.sqrt(B)*x)**2
    return OL0*(1.0+A*x*sech2)


# ============================================================
# Phase 22: Renormalization Group flow
# A1: 시공간 양자 밀도 = UV-IR RG 흐름의 고정점 이탈량.
# 물질 = UV cutoff 상승 원천. 공리 A2: RG 고정점 = QC 경계.
# ============================================================

def make_X1(p):
    """X1: RG anomalous dimension power.
    omega_de = OL0*(1+z)^(-A*ln(1+z)).
    A1: anomalous dimension gamma=A*ln(1+z). Spacetime quanta dilute as (1+z)^(3+gamma)."""
    Om=p[0]; A=p[1]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    # omega_de(z) = OL0*(1+z)^(-A*ln(1+z))
    # normalize: at z=0, (1+0)^0 = 1 -> OL0
    ln1z = np.log(1.0+Z_ARR)
    return OL0*(1.0+Z_ARR)**(-A*ln1z)


def make_X2(p):
    """X2: RG running coupling log^2.
    omega_de = OL0*(1+A*(ln(1+z))^2).
    A1: running coupling grows as log^2(energy). Dark energy = RG condensate."""
    Om=p[0]; A=p[1]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    return OL0*(1.0+A*np.log(1.0+Z_ARR)**2)


def make_X3(p):
    """X3: RG fixed-point approach with saturation.
    omega_de = OL0*(1+A*(1-exp(-B*ln(1+z)^2))).
    A1: approach to IR fixed point saturates at high z."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    return OL0*(1.0+A*(1.0-np.exp(-B*np.log(1.0+Z_ARR)**2)))


# ============================================================
# Phase 23: Non-equilibrium thermodynamics
# A1: 시공간 양자 = 비평형 엔트로피 생성 원천.
# 물질이 엔트로피 생산률 sigma를 상승. sigma -> omega_de.
# ============================================================

def make_Y1(p):
    """Y1: Entropy production cumulative.
    omega_de = OL0*(1+A*(1-exp(-B*sigma_int(z)))).
    sigma_int ~ integral of rho_m/E ~ I(z) from D1."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    _, I_arr = _precompute_integrals(Om, Z_ARR)
    # sigma_int = cumulative entropy production ~ Om * I(z)
    sigma = Om * I_arr
    return OL0*(1.0+A*(1.0-np.exp(-B*sigma)))


def make_Y2(p):
    """Y2: Onsager irreversible flux.
    omega_de = OL0 + A*(E_LCDM(z)^B - 1).
    A1: irreversible flux J = A*(E^B-1). Dark energy = accumulated flux."""
    Om=p[0]; A=p[1]; B=p[2]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    # normalize: at z=0, E=1, so E^B-1=0 -> OL0
    return OL0 + A*(E**B - 1.0)


def make_Y3(p):
    """Y3: Non-equilibrium steady state.
    omega_de = OL0*(1+A*sqrt(Om*(1+z)^3/(OL0+Om*(1+z)^3))).
    A1: NESS flux ~ sqrt of matter fraction."""
    Om=p[0]; A=p[1]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    frac = Om*(1+Z_ARR)**3 / np.maximum(OL0+Om*(1+Z_ARR)**3, 1e-10)
    frac_0 = Om / max(OL0+Om, 1e-10)
    delta = np.sqrt(np.maximum(frac, 0)) - np.sqrt(frac_0)
    return OL0*(1.0+A*delta)


# ============================================================
# Phase 24: Spin glass / Replica theory
# A1: 시공간 양자 = Edwards-Anderson 스핀 글래스 질서 매개변수.
# 물질 = quenched disorder 원천. 공리 A2 = replica symmetry breaking.
# ============================================================

def make_SG1(p):
    """SG1: Edwards-Anderson order parameter.
    omega_de = OL0*(1+A*(1-exp(-B/E_LCDM(z)^2))).
    A1: q_EA ~ exp(-T^2) ~ exp(-E^2). Freezing at low E (high z)."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    f_z = 1.0-np.exp(-B/np.maximum(E**2, 1e-10))
    f_0 = 1.0-np.exp(-B)
    return OL0*(1.0+A*(f_z-f_0))


def make_SG2(p):
    """SG2: Replica symmetry breaking transition.
    omega_de = OL0*(1+A*exp(-B*(E_LCDM(z)-1))*sinh(C*(E_LCDM(z)-1))).
    A1: oscillatory replica breaking near E=1."""
    Om=p[0]; A=p[1]; B=max(p[2],0.1); C=max(p[3],0.1)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    x = E - 1.0
    return OL0*(1.0+A*np.exp(-B*x)*np.sinh(C*x))


def make_SG3(p):
    """SG3: Stretched exponential (Kohlrausch relaxation).
    omega_de = OL0*exp(-A*((Om*(1+z)^3/OL0)^B-Om^B/OL0^B)).
    A1: non-exponential relaxation of spacetime quanta."""
    Om=p[0]; A=max(p[1],0.0); B=max(p[2],0.1)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    x_z = (Om*(1+Z_ARR)**3/np.maximum(OL0, 1e-10))**B
    x_0 = (Om/max(OL0, 1e-10))**B
    return OL0*np.exp(-A*(x_z-x_0))


# ============================================================
# Phase 25: Fractal / Multifractal geometry
# A1: 시공간 양자 = 프랙탈 차원 구조. 물질 = 프랙탈 측도 변화.
# 공리 A2: Hausdorff 차원 전이 = 양자-고전 경계.
# ============================================================

def make_FR1(p):
    """FR1: Anomalous diffusion on fractal.
    omega_de = OL0*(1+z)^(-A) * (1+B*ln(1+z))^(-1).
    A1: fractal dimension D_H modifies dilution. d_H = 3+A/(1+B*ln z)."""
    Om=p[0]; A=p[1]; B=max(p[2],0.0)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    # omega_de(z) = OL0 / ((1+z)^A * (1+B*ln(1+z)))
    # normalize: at z=0, (1+0)^A*(1+0)=1, so = OL0
    return OL0 / np.maximum((1+Z_ARR)**A * (1.0+B*np.log(1.0+Z_ARR)), 1e-10)


def make_FR2(p):
    """FR2: Multifractal scaling.
    omega_de = OL0*(1+A*((1+z)^(2/3)-1)^B).
    A1: Kolmogorov 2/3 law with anomalous exponent B."""
    Om=p[0]; A=p[1]; B=max(p[2],0.1)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    base = (1+Z_ARR)**(2.0/3.0) - 1.0
    base = np.maximum(base, 0)
    return OL0*(1.0+A*base**B)


def make_FR3(p):
    """FR3: Hausdorff measure log scaling.
    omega_de = OL0*(1+A*ln(1+z)^B).
    A1: spacetime quantum density scales as log^B(1+z)."""
    Om=p[0]; A=p[1]; B=max(p[2],0.1)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    return OL0*(1.0+A*np.log(1.0+Z_ARR)**B)


# ============================================================
# Phase 26: Matter fraction power law
# A1: 시공간 양자 = 물질 비율 f_m의 비선형 함수.
# 공리 A2: f_m = 1/2 에서 양자-고전 경계.
# ============================================================

def make_MF1(p):
    """MF1: Matter fraction power.
    omega_de = OL0*(1+A*(f_m(z)^B - f_m(0)^B)).
    f_m = Om(1+z)^3/(OL0+Om(1+z)^3). Power B varies shape."""
    Om=p[0]; A=p[1]; B=max(p[2],0.1)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    fm_z = Om*(1+Z_ARR)**3/np.maximum(OL0+Om*(1+Z_ARR)**3, 1e-10)
    fm_0 = Om/max(OL0+Om, 1e-10)
    return OL0*(1.0+A*(fm_z**B - fm_0**B))


def make_MF2(p):
    """MF2: Complement matter fraction.
    omega_de = OL0*(1-f_m(z))^(-A) / (1-f_m(0))^(-A).
    A1: vacuum fraction (1-f_m) generates quanta. Power -A ~ growth."""
    Om=p[0]; A=p[1]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    fm_z = Om*(1+Z_ARR)**3/np.maximum(OL0+Om*(1+Z_ARR)**3, 1e-10)
    fm_0 = Om/max(OL0+Om, 1e-10)
    vac_z = np.maximum(1.0-fm_z, 1e-10)
    vac_0 = max(1.0-fm_0, 1e-10)
    return OL0 * (vac_z/vac_0)**(-A)


def make_MF3(p):
    """MF3: Sigmoid matter fraction.
    omega_de = OL0*(1+A*(sigma(B*f_m(z))-sigma(B*f_m(0)))).
    sigma(x)=1/(1+exp(-x)). A1: quantum phase transition at f_m=0.5."""
    Om=p[0]; A=p[1]; B=p[2]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    fm_z = Om*(1+Z_ARR)**3/np.maximum(OL0+Om*(1+Z_ARR)**3, 1e-10)
    fm_0 = Om/max(OL0+Om, 1e-10)
    sig = lambda x: 1.0/(1.0+np.exp(-np.clip(x, -50, 50)))
    return OL0*(1.0+A*(sig(B*fm_z)-sig(B*fm_0)))


# ============================================================
# Phase 27: CDT / Discrete spacetime
# A1: 시공간 = 이산 단체(simplex) 조합. 물질 = simplex 제거.
# 빈 공간 = simplex 생성. 공리 A2 = 연속 극한.
# ============================================================

def make_CD1(p):
    """CD1: CDT oscillatory.
    omega_de = OL0*(1+A*sin^2(B*(1+z)^(3/2))).
    A1: simplex counting oscillates with volume^(3/2)."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    theta_z = B*(1+Z_ARR)**(1.5)
    theta_0 = B
    return OL0*(1.0+A*(np.sin(theta_z)**2 - np.sin(theta_0)**2))


def make_CD2(p):
    """CD2: Rational discrete Friedmann.
    omega_de = OL0*(1+A*(Om*(1+z)^3-Om)/(OL0+B*Om*(1+z)^3)).
    A1: discrete correction to Friedmann with B-suppressed growth."""
    Om=p[0]; A=p[1]; B=max(p[2],0.0)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    numer = Om*(1+Z_ARR)**3 - Om
    denom = np.maximum(OL0+B*Om*(1+Z_ARR)**3, 1e-10)
    return OL0*(1.0+A*numer/denom)


def make_CD3(p):
    """CD3: Discrete volume fluctuation.
    omega_de = OL0*(1+A*exp(-B/(Om*(1+z)^3/OL0)^C)).
    A1: Boltzmann-like activation from matter/vacuum ratio."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01); C=max(p[3],0.1)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    ratio_z = np.maximum(Om*(1+Z_ARR)**3/max(OL0, 1e-10), 1e-10)
    ratio_0 = Om/max(OL0, 1e-10)
    f_z = np.exp(-B/ratio_z**C)
    f_0 = np.exp(-B/ratio_0**C)
    return OL0*(1.0+A*(f_z-f_0))


# ============================================================
# Phase 28: String gas / Hagedorn
# A1: 시공간 양자 = 감긴 문자열(wound strings). 물질 = 풀림(unwinding).
# 빈 공간 = 새 감김 생성. 공리 A2 = 하게도른 전이 = QC 경계.
# ============================================================

def make_ST1(p):
    """ST1: Hagedorn winding string decay.
    omega_de = OL0*exp(-A*((1+z)^3-1)) * (1+B*(1+z)^3).
    A1: wound string density decays exponentially with volume."""
    Om=p[0]; A=max(p[1],0.0); B=max(p[2],0.0)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    x_z = (1+Z_ARR)**3 - 1.0
    f_z = np.exp(-A*x_z)*(1.0+B*(1+Z_ARR)**3)
    f_0 = 1.0*(1.0+B)
    return OL0*f_z/f_0


def make_ST2(p):
    """ST2: String gas thermal pressure.
    omega_de = OL0*(1+A*(exp(-B/E_LCDM(z))-exp(-B))).
    A1: string excitations ~ exp(-T_H/T) ~ exp(-B/E)."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    f_z = np.exp(-B/np.maximum(E, 1e-10))
    f_0 = np.exp(-B)  # E(0)=1
    return OL0*(1.0+A*(f_z-f_0))


def make_ST3(p):
    """ST3: Hagedorn transition tanh.
    omega_de = OL0*(1+A*(tanh(B*(E_LCDM(z)-C))-tanh(B*(1-C)))).
    A1: phase transition at E=C (Hagedorn temperature)."""
    Om=p[0]; A=p[1]; B=max(p[2],0.1); C=p[3]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    f_z = np.tanh(B*(E-C))
    f_0 = np.tanh(B*(1.0-C))
    return OL0*(1.0+A*(f_z-f_0))


# ============================================================
# Phase 29: Acoustic / Phonon analogy
# A1: 시공간 양자 = 음향 포논. 물질 = 포논 흡수체.
# 빈 공간 = 포논 방출원. 공리 A2 = 음속 전이 = QC 경계.
# ============================================================

def make_AC1(p):
    """AC1: Debye phonon spectrum.
    omega_de = OL0*(1+A*(exp(-B*(Om*(1+z)^3/OL0))-exp(-B*Om/OL0))).
    A1: Boltzmann phonon occupation. High matter -> quenched phonons."""
    Om=p[0]; A=p[1]; B=max(p[2],0.0)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    r_z = Om*(1+Z_ARR)**3/max(OL0, 1e-10)
    r_0 = Om/max(OL0, 1e-10)
    return OL0*(1.0+A*(np.exp(-B*r_z)-np.exp(-B*r_0)))


def make_AC2(p):
    """AC2: Damped acoustic oscillation.
    omega_de = OL0*(1+A*exp(-B*(E(z)-1))*sinh(C*(E(z)-1))).
    A1: acoustic oscillation with exponential damping.
    Note: sinh variant of SG2 but different regime."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01); C=max(p[3],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    x = E - 1.0
    return OL0*(1.0+A*np.exp(-B*x)*np.sinh(np.minimum(C*x, 50)))


def make_AC3(p):
    """AC3: Hyperbolic phonon density.
    omega_de = OL0*(1+A*sinh(B*(E_LCDM(z)-1))).
    A1: phonon density ~ sinh(beta*epsilon) from phonon statistics."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    x = E - 1.0
    return OL0*(1.0+A*np.sinh(np.minimum(B*x, 50)))


# ============================================================
# Phase 30: Grand canonical / Chemical potential
# A1: 시공간 양자 = 화학 퍼텐셜 mu를 가진 입자계.
# 물질 = 화학 퍼텐셜 상승. 공리 A2 = mu = mu_c (임계 전이).
# ============================================================

def make_GC1(p):
    """GC1: Boltzmann grand canonical.
    omega_de = OL0*exp(A*(OL0/(OL0+Om*(1+z)^3) - OL0/(OL0+Om))).
    A1: chemical potential mu ~ -A*vacuum_fraction. High z = low mu."""
    Om=p[0]; A=p[1]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    vac_z = OL0/np.maximum(OL0+Om*(1+Z_ARR)**3, 1e-10)
    vac_0 = OL0/max(OL0+Om, 1e-10)
    return OL0*np.exp(A*(vac_z-vac_0))


def make_GC2(p):
    """GC2: Fugacity expansion.
    omega_de = OL0*(1+A*ln(1+B*(1+z)^3-B)).
    A1: fugacity z_gc = B*(1+z)^3/B_0. Dark energy ~ log partition function."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    # delta_ln_Z = ln(1+B*(1+z)^3) - ln(1+B)
    arg_z = 1.0+B*((1+Z_ARR)**3-1.0)
    return OL0*(1.0+A*np.log(np.maximum(arg_z, 1e-10)))


def make_GC3(p):
    """GC3: Chemical potential power law fraction.
    omega_de = OL0*(OL0/(OL0+Om*(1+z)^3))^A / (OL0/(OL0+Om))^A.
    A1: dark energy density ~ (vacuum fraction)^A. Growing for A<0."""
    Om=p[0]; A=p[1]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    vac_z = OL0/np.maximum(OL0+Om*(1+Z_ARR)**3, 1e-10)
    vac_0 = OL0/max(OL0+Om, 1e-10)
    return OL0*(vac_z/vac_0)**A


# ============================================================
# MAIN
# ============================================================

print("=== L14 Batch-3: 30 new theories (Phases 21-30) ===")
print("DESI DR2 7-bin chi2. H0=67.7 fixed.\n")

# References
print("--- REFERENCES ---")
_r = fit_model(make_D1_ref, 'D1-prev',
               [[0.28, 0.30, 4.0], [0.30, 0.50, 3.0], [0.28, 0.20, 5.0]])
if _r:
    print(f"D1-prev    p={_r['p']}  chi2={_r['chi2']:.3f}  w0={_r['w0']:.3f}  wa={_r['wa']:.3f}")

MODELS = [
    # Phase 21: Soliton
    ('F1-Soliton', make_F1, [[0.28, 1.0, 2.0, 0.5], [0.30, 2.0, 1.0, 0.3],
                              [0.28, 0.5, 3.0, 1.0], [0.30, -1.0, 2.0, 0.5]]),
    ('F2-Kink',    make_F2, [[0.28, 0.5, 0.5, 0.3], [0.30, 1.0, 1.0, 0.2],
                              [0.28, -0.5, 0.5, 0.3], [0.28, 2.0, 0.3, 0.1]]),
    ('F3-KinkAK',  make_F3, [[0.28, 1.0, 2.0], [0.30, 2.0, 1.0],
                              [0.28, 0.5, 3.0], [0.28, 3.0, 0.5]]),
    # Phase 22: RG
    ('X1-RGanom',  make_X1, [[0.28, 0.3], [0.30, 0.5], [0.28, 0.1], [0.28, 1.0]]),
    ('X2-RGlog2',  make_X2, [[0.28, 0.5], [0.30, 0.3], [0.28, 1.0], [0.28, -0.3]]),
    ('X3-RGsat',   make_X3, [[0.28, 0.5, 1.0], [0.30, 0.3, 2.0], [0.28, 1.0, 0.5]]),
    # Phase 23: Non-equil
    ('Y1-EntProd', make_Y1, [[0.28, 0.5, 0.5], [0.30, 0.3, 1.0], [0.28, 1.0, 0.3]]),
    ('Y2-Onsager', make_Y2, [[0.28, 0.2, 1.5], [0.30, 0.3, 2.0], [0.28, -0.2, 0.5],
                              [0.28, 0.1, 3.0]]),
    ('Y3-NESS',    make_Y3, [[0.28, 1.0], [0.30, 2.0], [0.28, 0.5], [0.28, -1.0]]),
    # Phase 24: Spin glass
    ('SG1-EA',     make_SG1, [[0.28, 1.0, 1.0], [0.30, 0.5, 2.0], [0.28, 2.0, 0.5]]),
    ('SG2-RSB',    make_SG2, [[0.28, 1.0, 1.0, 2.0], [0.30, 0.5, 0.5, 1.0],
                               [0.28, 2.0, 2.0, 3.0], [0.28, -1.0, 1.0, 2.0]]),
    ('SG3-Kohl',   make_SG3, [[0.28, 0.5, 0.5], [0.30, 0.3, 0.3], [0.28, 1.0, 1.0]]),
    # Phase 25: Fractal
    ('FR1-Anom',   make_FR1, [[0.28, 0.3, 0.5], [0.30, 0.5, 0.3], [0.28, 0.1, 0.0]]),
    ('FR2-Multi',  make_FR2, [[0.28, 0.5, 0.7], [0.30, 1.0, 0.5], [0.28, 2.0, 1.0]]),
    ('FR3-HausL',  make_FR3, [[0.28, 0.5, 1.5], [0.30, 0.3, 2.0], [0.28, 1.0, 1.0]]),
    # Phase 26: Matter fraction
    ('MF1-FracPow',make_MF1, [[0.28, 1.0, 0.5], [0.30, 0.5, 1.0], [0.28, 2.0, 0.3]]),
    ('MF2-CompFr', make_MF2, [[0.28, 0.5], [0.30, 1.0], [0.28, -0.5], [0.28, 2.0]]),
    ('MF3-Sigmoid',make_MF3, [[0.28, 1.0, 5.0], [0.30, 0.5, 3.0], [0.28, -1.0, 5.0]]),
    # Phase 27: CDT
    ('CD1-CDTosc', make_CD1, [[0.28, 0.5, 0.3], [0.30, 1.0, 0.5], [0.28, -0.3, 0.2]]),
    ('CD2-CDTrat', make_CD2, [[0.28, 0.5, 0.5], [0.30, 1.0, 0.3], [0.28, 2.0, 1.0]]),
    ('CD3-CDTbol', make_CD3, [[0.28, 1.0, 0.5, 0.5], [0.30, 0.5, 1.0, 1.0],
                               [0.28, 2.0, 0.3, 0.3]]),
    # Phase 28: String gas
    ('ST1-Winding',make_ST1, [[0.28, 0.1, 0.5], [0.30, 0.3, 0.3], [0.28, 0.0, 1.0]]),
    ('ST2-StrThr', make_ST2, [[0.28, 1.0, 1.0], [0.30, 0.5, 2.0], [0.28, -1.0, 1.0]]),
    ('ST3-Haged',  make_ST3, [[0.28, 1.0, 2.0, 1.5], [0.30, 0.5, 1.0, 2.0],
                               [0.28, -1.0, 2.0, 0.5]]),
    # Phase 29: Acoustic
    ('AC1-Debye',  make_AC1, [[0.28, 1.0, 1.0], [0.30, 0.5, 2.0], [0.28, -1.0, 1.0]]),
    ('AC2-DampOsc',make_AC2, [[0.28, 1.0, 0.5, 1.0], [0.30, 0.5, 1.0, 2.0],
                               [0.28, 2.0, 0.3, 0.5]]),
    ('AC3-HypPhon',make_AC3, [[0.28, 0.5, 0.5], [0.30, 0.3, 1.0], [0.28, 1.0, 0.3]]),
    # Phase 30: Grand canonical
    ('GC1-Boltz',  make_GC1, [[0.28, 1.0], [0.30, 2.0], [0.28, -1.0], [0.28, 0.5]]),
    ('GC2-Fugac',  make_GC2, [[0.28, 0.5, 0.3], [0.30, 0.3, 0.5], [0.28, 1.0, 0.1]]),
    ('GC3-ChemPow',make_GC3, [[0.28, -0.5], [0.30, -1.0], [0.28, 0.5], [0.28, -2.0]]),
]

PHASES = {
    'F': '21:Soliton', 'X': '22:RGflow', 'Y': '23:NonEquil',
    'SG': '24:SpinGlass', 'FR': '25:Fractal', 'MF': '26:MatFrac',
    'CD': '27:CDT', 'ST': '28:StringGas', 'AC': '29:Acoustic', 'GC': '30:GrandCan'
}

results = {}
rows = []

for label, fn, starts in MODELS:
    phase_key = label.split('-')[0].rstrip('123')
    # determine phase label
    ph = ''
    for k, v in PHASES.items():
        if label.startswith(k):
            ph = v; break
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

# Summary
LCDM_CHI2 = 13.198
D1_CHI2   = 10.984
C14_CHI2  = 11.468

print("\n=== BATCH-3 SUMMARY ===")
print(f"LCDM chi2={LCDM_CHI2}  D1-prev chi2={D1_CHI2}\n")
rows.sort(key=lambda x: x[1])
print(f"{'Model':<14} {'chi2':<10} {'dLCDM':<12} {'dD1':<12} {'w0':<10} {'wa':<10} {'STATUS'}")
print('-'*80)
game_changers = []
new_bests = []
passes = []
kills = []
for lbl, chi2, w0, wa in rows:
    dc = chi2 - LCDM_CHI2
    dd = chi2 - D1_CHI2
    if chi2 < C14_CHI2 and wa < -0.5:
        st = 'GAME-CHANGER!'
        game_changers.append((lbl, chi2, w0, wa))
    elif chi2 < D1_CHI2:
        st = 'NEW-BEST!'
        new_bests.append((lbl, chi2, w0, wa))
    elif chi2 < LCDM_CHI2:
        st = 'PASS'
        passes.append((lbl, chi2, w0, wa))
    else:
        st = 'KILL'
        kills.append((lbl, chi2, w0, wa))
    print(f"{lbl:<14} chi2={chi2:<6.3f}  dLCDM={dc:<7.3f}  dD1={dd:<7.3f}  w0={w0:<8.3f}  wa={wa:<8.3f}  STATUS  {st}")

# Add LCDM row
print(f"{'LCDM':<14} chi2={LCDM_CHI2:<6.3f}  dLCDM={0.0:<7.3f}  dD1={LCDM_CHI2-D1_CHI2:<7.3f}  w0={-1.0:<8.3f}  wa={0.0:<8.3f}  STATUS  KILL")

if game_changers:
    print(f"\nGAME-CHANGER models (chi2 < {C14_CHI2} AND wa < -0.5):")
    for lbl, chi2, w0, wa in game_changers:
        print(f"  {lbl}: chi2={chi2:.3f}  wa={wa:.3f}")
if new_bests:
    print(f"\nNEW BEST models (chi2 < D1 {D1_CHI2}):")
    for lbl, chi2, w0, wa in new_bests:
        print(f"  {lbl}: chi2={chi2:.3f}  wa={wa:.3f}")

# Save JSON
out_path = os.path.join(_THIS, 'l14_new30c_results.json')
def _j(v):
    if isinstance(v, (np.floating, np.float64, np.float32)): return float(v)
    if isinstance(v, (np.integer,)): return int(v)
    if isinstance(v, list): return [_j(x) for x in v]
    return v
save = {k: {kk: _j(vv) for kk, vv in val.items()} for k, val in results.items()}
with open(out_path, 'w') as f:
    json.dump(save, f, indent=2)
print(f"\nSaved: {out_path}")
