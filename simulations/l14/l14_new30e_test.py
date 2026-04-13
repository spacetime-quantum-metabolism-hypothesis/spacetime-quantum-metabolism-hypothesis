# -*- coding: utf-8 -*-
"""
L14 Batch-5: 30 more new theories from A1+A2. Phases 41-50.

Phase 41: Fermi gas / Thomas-Fermi (TF1-TF3)
Phase 42: Allosteric enzyme / Hill cooperativity (AE1-AE3)
Phase 43: Ising / Mean-field order (IS1-IS3)
Phase 44: Wheeler-DeWitt / quantum gravity (WD1-WD3)
Phase 45: Cosmic string network / Kibble-Zurek (KZ1-KZ3)
Phase 46: Verlinde entropic gravity (VE1-VE3)
Phase 47: Lindblad decoherence (LD1-LD3)
Phase 48: Axionic dark energy / oscillation (AX1-AX3)
Phase 49: Landau-Ginzburg order parameter (LG1-LG3)
Phase 50: Composite / hybrid best-forms (HB1-HB3)
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


# ============================================================
# Phase 41: Fermi gas / Thomas-Fermi
# A1: 시공간 양자 = 축퇴 페르미 기체 준위.
# 물질 = 페르미 에너지 상승 원천. 공리 A2 = 페르미 에너지 = QC 경계.
# ============================================================

def make_TF1(p):
    """TF1: Fermi-Dirac distribution.
    omega_de = OL0/(1+exp(B*(E_LCDM(z)-C))).
    Normalized by OL0/(1+exp(B*(1-C))).
    A1: spacetime quanta fill Fermi sea. High E = excited above Fermi level."""
    Om=p[0]; B=max(p[1],0.1); C=p[2]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    f_z = 1.0/(1.0+np.exp(np.clip(B*(E-C), -50, 50)))
    f_0 = 1.0/(1.0+np.exp(np.clip(B*(1.0-C), -50, 50)))
    if abs(f_0) < 1e-10: return None
    return OL0*f_z/f_0


def make_TF2(p):
    """TF2: Thomas-Fermi screening power.
    omega_de = OL0*(1+A*(E_LCDM(z)^(2/3)-1)).
    A1: TF energy density ~ n^(5/3) -> E^(2/3) per quantum."""
    Om=p[0]; A=p[1]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    return OL0*(1.0+A*(E**(2.0/3.0)-1.0))


def make_TF3(p):
    """TF3: Fermi liquid quasiparticle.
    omega_de = OL0*(1+A*(E_LCDM(z)-1)*exp(-B*(E_LCDM(z)-1)^3)).
    A1: quasiparticle weight Z_qp ~ exp(-B*(E-1)^3). Peak at (1/(3B))^(1/2)."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    x = E - 1.0
    return OL0*(1.0+A*x*np.exp(-B*x**3))


# ============================================================
# Phase 42: Allosteric enzyme / Hill cooperativity
# A1: 시공간 양자 = 기질 (substrate). 물질 = 효소 (촉매 소멸).
# 공리 A2: Hill 전이 = QC 경계.
# ============================================================

def make_AE1(p):
    """AE1: Hill equation n=2 (cooperative).
    omega_de = OL0*(1+A*(Om*(1+z)^3)^2/(B^2+(Om*(1+z)^3)^2)).
    normalized at z=0. A1: cooperativity n=2."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    x_z = Om*(1+Z_ARR)**3
    x_0 = Om
    f_z = x_z**2/(B**2+x_z**2)
    f_0 = x_0**2/(B**2+x_0**2)
    return OL0*(1.0+A*(f_z-f_0))


def make_AE2(p):
    """AE2: Allosteric sigmoidal.
    omega_de = OL0*(1+A*(exp(B*(E_LCDM(z)-C))-exp(B*(1-C)))).
    A1: sigmoidal response. Grows for z > z_thresh where E=C."""
    Om=p[0]; A=p[1]; B=p[2]; C=p[3]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    delta = np.exp(np.clip(B*(E-C), -30, 30)) - np.exp(np.clip(B*(1.0-C), -30, 30))
    return OL0*(1.0+A*delta)


def make_AE3(p):
    """AE3: Product inhibition.
    omega_de = OL0*(1+A*(1-exp(-B*(Om*(1+z)^3)^C))).
    A1: substrate accumulation saturates -> inhibition. Power C = Hill coefficient."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01); C=max(p[3],0.1)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    x_z = np.maximum(Om*(1+Z_ARR)**3, 0)
    x_0 = Om
    f_z = 1.0-np.exp(-B*x_z**C)
    f_0 = 1.0-np.exp(-B*x_0**C)
    return OL0*(1.0+A*(f_z-f_0))


# ============================================================
# Phase 43: Ising / Mean-field order parameter
# A1: 시공간 양자 밀도 = 강자성 질서 매개변수 m.
# 물질 = 외부 자기장 (질서 방해). 공리 A2 = m=0 전이 = QC 경계.
# ============================================================

def make_IS1(p):
    """IS1: Ising mean-field order parameter.
    omega_de = OL0*tanh(A/E_LCDM(z)) / tanh(A).
    A1: m ~ tanh(J/T) ~ tanh(A/E). Grows at high E (high T -> disorder)? No.
    Actually tanh(A/E) DECREASES with E -> omega_de decreases with z -> wa > 0.
    Use complement: omega_de = OL0*(2-tanh(A/E)/tanh(A))?
    Or: A1 says HIGH E -> HIGH disorder -> LOW quanta density.
    So omega_de ~ tanh(A/(E*(1+B*(E-1)))) grows if denominator decreases."""
    Om=p[0]; A=max(p[1],0.01); B=p[2]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    # tanh decreases with E -> wa > 0 normally
    # Try: omega_de = OL0*(1+A*(tanh(B*E)-tanh(B))) -> grows if B > 0
    f_z = np.tanh(np.clip(B*E, -20, 20))
    f_0 = np.tanh(np.clip(B, -20, 20))
    return OL0*(1.0+A*(f_z-f_0))


def make_IS2(p):
    """IS2: Boltzmann occupation.
    omega_de = OL0*exp(-A*(E_LCDM(z)^2-1)).
    A1: Boltzmann factor ~ exp(-E^2/T). Decreasing for A>0.
    For A<0: omega_de grows with z. SQMH-compatible if A<0 allowed."""
    Om=p[0]; A=p[1]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    return OL0*np.exp(-A*(E**2-1.0))


def make_IS3(p):
    """IS3: Critical fluctuation.
    omega_de = OL0*(1+A*(E_LCDM(z)^(-B)-1)).
    A1: critical fluctuation ~ E^(-nu). For B>0: decreasing. For A<0, B>0: growing."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    return OL0*(1.0+A*(E**(-B)-1.0))


# ============================================================
# Phase 44: Wheeler-DeWitt / quantum cosmology
# A1: 시공간 양자 = WdW 파동함수 진폭.
# 물질 = WdW potential 기여. 공리 A2 = 고전 극한 = WdW turning point.
# ============================================================

def make_WD1(p):
    """WD1: WdW tunneling amplitude.
    omega_de = OL0*(1+A*(exp(-B/sqrt(E_LCDM(z)))-exp(-B))).
    A1: WdW tunneling ~ exp(-S_WdW) ~ exp(-B/sqrt(E)). Grows with E."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    f_z = np.exp(-B/np.sqrt(np.maximum(E, 1e-10)))
    f_0 = np.exp(-B)  # E(0)=1
    return OL0*(1.0+A*(f_z-f_0))


def make_WD2(p):
    """WD2: Hartle-Hawking no-boundary.
    omega_de = OL0*(1+A*exp(-B*(E_LCDM(z)^2-1)^2)).
    A1: HH wave function ~ exp(-S_E) ~ exp(-B*(E^2-1)^2). Peaks at E=1."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    # Note: at z=0, E=1, so (E^2-1)^2=0, exp=1.
    # For A>0: omega_de(z>0) < OL0. For A<0: grows.
    return OL0*(1.0+A*np.exp(-B*(E**2-1.0)**2))


def make_WD3(p):
    """WD3: Vilenkin tunneling from nothing.
    omega_de = OL0*(1+A*(E_LCDM(z)^2-1)*exp(-B*(E_LCDM(z)^2-1))).
    A1: Vilenkin probability ~ (E^2-1)*exp(-B*(E^2-1)). x*exp(-Bx) form."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    x = E**2 - 1.0
    return OL0*(1.0+A*x*np.exp(-B*x))


# ============================================================
# Phase 45: Cosmic string / Kibble-Zurek
# A1: 시공간 양자 = 코스믹 스트링 길이 밀도.
# 물질 = 스트링 붕괴 촉진. 공리 A2 = 상관 길이 임계 = QC 경계.
# ============================================================

def make_KZ1(p):
    """KZ1: Kibble-Zurek correlation length.
    omega_de = OL0*(1+A*(E_LCDM(z)-1)*exp(-B*E_LCDM(z)*(E_LCDM(z)-1))).
    A1: KZ correlation ~ xi ~ (E-1)*exp(-B*E*(E-1)). Modified Gaussian."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    x = E - 1.0
    return OL0*(1.0+A*x*np.exp(-B*E*x))


def make_KZ2(p):
    """KZ2: String network scaling.
    omega_de = OL0*(1+A*exp(-B*(1+z)^3)*(1+C*(1+z)^3)).
    A1: string density ~ exp(-B*vol)*(1+C*vol). Same form as ST1 but reparametrized."""
    Om=p[0]; A=max(p[1],0.0); B=max(p[2],0.0); C=max(p[3],0.0)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    v_z = (1+Z_ARR)**3
    v_0 = 1.0
    f_z = np.exp(-B*v_z)*(1.0+C*v_z)
    f_0 = np.exp(-B*v_0)*(1.0+C*v_0)
    if abs(f_0) < 1e-10: return None
    return OL0*(1.0+A*(f_z/f_0-1.0))


def make_KZ3(p):
    """KZ3: Zurek freeze-out.
    omega_de = OL0*(1+A*(1-exp(-B*sqrt(Om*(1+z)^3)))).
    A1: freeze-out density ~ sqrt(matter density). QKZ mechanism."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    x_z = np.sqrt(np.maximum(Om*(1+Z_ARR)**3, 0))
    x_0 = np.sqrt(Om)
    f_z = 1.0-np.exp(-B*x_z)
    f_0 = 1.0-np.exp(-B*x_0)
    return OL0*(1.0+A*(f_z-f_0))


# ============================================================
# Phase 46: Verlinde entropic gravity
# A1: 시공간 양자 = 홀로그래픽 비트.
# 물질 = 엔트로피 그래디언트 원천. 공리 A2 = 엔트로피 포화 = QC 경계.
# ============================================================

def make_VE1(p):
    """VE1: Verlinde dark energy.
    omega_de = OL0*exp(-A*Om*(1+z)^3/OL0).
    A1: Verlinde dark energy ~ exp(-matter/vacuum). Decreases for A>0."""
    Om=p[0]; A=p[1]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    r_z = Om*(1+Z_ARR)**3/max(OL0, 1e-10)
    r_0 = Om/max(OL0, 1e-10)
    return OL0*np.exp(-A*(r_z-r_0))


def make_VE2(p):
    """VE2: Entropic force correction.
    omega_de = OL0*(1+A*sqrt(Om*(1+z)^3/OL0)-A*sqrt(Om/OL0)).
    A1: entropic force ~ sqrt(matter/vacuum). Grows as matter dilutes? No, grows with z.
    Actually sqrt grows with z for Om*(1+z)^3 increasing. So wa < 0."""
    Om=p[0]; A=p[1]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    r_z = np.sqrt(np.maximum(Om*(1+Z_ARR)**3/max(OL0, 1e-10), 0))
    r_0 = np.sqrt(Om/max(OL0, 1e-10))
    return OL0*(1.0+A*(r_z-r_0))


def make_VE3(p):
    """VE3: Information metric dark energy.
    omega_de = OL0*(1+A*(ln(OL0/(OL0+Om*(1+z)^3))-ln(OL0/(OL0+Om)))).
    A1: Fisher information I ~ -ln(P). P = vacuum fraction. Log grows with z."""
    Om=p[0]; A=p[1]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    vac_z = np.maximum(OL0/(OL0+Om*(1+Z_ARR)**3), 1e-10)
    vac_0 = OL0/(OL0+Om)
    ln_z = np.log(vac_z)
    ln_0 = np.log(vac_0)
    return OL0*(1.0+A*(ln_z-ln_0))


# ============================================================
# Phase 47: Lindblad decoherence
# A1: 시공간 양자 = 개방 양자 계 밀도 행렬 코히어런스.
# 물질 = Lindblad 붕괴 연산자. 공리 A2 = 완전 decoherence = QC 경계.
# ============================================================

def make_LD1(p):
    """LD1: Lindblad exponential decay.
    omega_de = OL0*exp(-A*(1-exp(-B*Om*(1+z)^3))).
    A1: coherence ~ exp(-gamma*n_matter). Grows at high z for A>0? No.
    For omega_de to grow: need A<0 or nested exp with A>0.
    exp(-A*(1-exp(-Bx))): at z=0, x=Om, f=exp(-A*(1-exp(-BOm))). At z>>0, x>>1, f->exp(-A).
    If A<0: f grows from exp(-A*(1-exp(-BOm))) < exp(-A*(-1)) = exp(A) to exp(-A) -> grows."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    x_z = Om*(1+Z_ARR)**3
    x_0 = Om
    f_z = np.exp(-A*(1.0-np.exp(-B*x_z)))
    f_0 = np.exp(-A*(1.0-np.exp(-B*x_0)))
    if abs(f_0) < 1e-10: return None
    return OL0*f_z/f_0


def make_LD2(p):
    """LD2: Lindblad Gaussian decoherence.
    omega_de = OL0*(1+A*(exp(-B*E_LCDM(z)^2)-exp(-B))).
    A1: decoherence rate ~ exp(-gamma/E^2) or ~ exp(-B*E^2)?
    exp(-B*E^2) decreases. exp(-B*E^2)-exp(-B) < 0 for E>1.
    For A<0: grows with z. Or define: omega_de = OL0*(1+A*(exp(-B*(E-1)^2)-1)).
    At z=0: exp(0)-1=0 -> OL0. At z>0: (E-1)^2 > 0 -> f < 0. A<0 -> grows."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    return OL0*(1.0+A*(np.exp(-B*(E-1.0)**2)-1.0))


def make_LD3(p):
    """LD3: Non-Markovian memory.
    omega_de = OL0*(1+A*exp(-B*(E_LCDM-1))*cos(C*(E_LCDM-1))).
    A1: non-Markovian revival oscillations. cos dampened by exp."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01); C=max(p[3],0.1)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    x = E - 1.0
    return OL0*(1.0+A*np.exp(-B*x)*np.cos(C*x))


# ============================================================
# Phase 48: Axionic dark energy / oscillation
# A1: 시공간 양자 = 축이온 장 진폭. 물질 = 축이온 질량 획득.
# 공리 A2 = 축이온 위상 전이 = QC 경계.
# ============================================================

def make_AX1(p):
    """AX1: Axionic oscillation in E^2 space.
    omega_de = OL0*(1+A*(cos(B*(E_LCDM(z)^2-1))-1)).
    A1: axion field phi ~ cos(m*t). Dark energy ~ phi^2 ~ cos^2."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    return OL0*(1.0+A*(np.cos(B*(E**2-1.0))-1.0))


def make_AX2(p):
    """AX2: Axion misalignment angle.
    omega_de = OL0*(1+A*sin^2(B*E_LCDM(z))/sin^2(B)).
    A1: theta_a = B*E. V ~ (1-cos(theta)) ~ sin^2(theta/2) ~ sin^2(B*E/2)."""
    Om=p[0]; A=p[1]; B=np.clip(p[2], 0.01, np.pi/2)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    sin0_sq = np.sin(B)**2
    if sin0_sq < 1e-10: return None
    sin_z_sq = np.sin(np.minimum(B*E, np.pi-1e-6))**2
    return OL0*(1.0+A*(sin_z_sq/sin0_sq-1.0))


def make_AX3(p):
    """AX3: Axion potential modulated.
    omega_de = OL0*(1+A*(1-cos(B*(Om*(1+z)^3-Om)/OL0))).
    A1: axion vacuum energy ~ 1-cos(theta). theta grows with matter density change."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    theta_z = B*(Om*(1+Z_ARR)**3-Om)/max(OL0, 1e-10)
    return OL0*(1.0+A*(1.0-np.cos(np.minimum(theta_z, 20))))


# ============================================================
# Phase 49: Landau-Ginzburg order parameter
# A1: 시공간 양자 밀도 = LG 질서 매개변수 psi.
# 물질 = LG 자유에너지 변화. 공리 A2 = psi=0 전이 = QC 경계.
# ============================================================

def make_LG1(p):
    """LG1: LG potential near transition.
    omega_de = OL0*(1+A*(E_LCDM(z)^2-1)*exp(-B*(E_LCDM(z)^2-1))).
    A1: LG free energy F ~ psi^2 - psi^4 -> order parameter ~ x*exp(-Bx)."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    x = E**2 - 1.0
    return OL0*(1.0+A*x*np.exp(-B*x))


def make_LG2(p):
    """LG2: LG free energy Mexican hat.
    omega_de = OL0*(1+A*(1-(E_LCDM(z)^2-r0^2)^2/B^2)).
    A1: psi = minimum of -alpha*psi^2 + beta*psi^4. Near minimum."""
    Om=p[0]; A=max(p[1],0.0); r0=max(p[2],0.5); B=max(p[3],0.1)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    x = (E**2 - r0**2)**2/B**2
    # normalize at z=0: x0 = (1-r0^2)^2/B^2
    x0 = (1.0-r0**2)**2/B**2
    return OL0*(1.0+A*(1.0-x)-(1.0+A*(1.0-x0)-1.0))


def make_LG3(p):
    """LG3: LG Gaussian fluctuation near T_c.
    omega_de = OL0*exp(-A*(E_LCDM(z)-1)^2).
    A1: Gaussian fluctuation ~ exp(-psi^2/(2*xi^2)) ~ exp(-A*(E-1)^2).
    For A<0: grows with z."""
    Om=p[0]; A=p[1]
    B = 0.0  # unused, keep signature consistent
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    x = E - 1.0
    # LG3 = pure Gaussian, no (E-1) prefactor
    arr = OL0*np.exp(-A*x**2)
    # normalize: at z=0, E=1, x=0, arr=OL0. Good.
    # But for A>0: decreasing. Need A<0 for growth.
    return arr


# ============================================================
# Phase 50: Composite hybrid forms (novel combinations)
# Building on best performers (N3-like, ST1-like, Q3-like)
# with new structural modifications.
# ============================================================

def make_HB1(p):
    """HB1: N3-variant with cubic Gaussian.
    omega_de = OL0*(1+A*(E_LCDM-1)*exp(-B*(E_LCDM-1)^3)).
    N3 uses (E-1)*exp(-B*(E-1)^2). HB1 uses cubic damping -> wider peak."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    x = E - 1.0
    return OL0*(1.0+A*x*np.exp(-B*np.maximum(x**3, -20)))


def make_HB2(p):
    """HB2: ST1-variant with quadratic volume.
    omega_de = OL0*exp(-A*((1+z)^2-1))*(1+B*(1+z)^2).
    ST1 uses (1+z)^3. HB2 uses (1+z)^2 -> gentler growth/decay."""
    Om=p[0]; A=max(p[1],0.0); B=max(p[2],0.0)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    v_z = (1+Z_ARR)**2
    f_z = np.exp(-A*(v_z-1.0))*(1.0+B*v_z)
    f_0 = np.exp(-A*0.0)*(1.0+B)
    if abs(f_0) < 1e-10: return None
    return OL0*f_z/f_0


def make_HB3(p):
    """HB3: Q3-variant with higher-order Lorentzian.
    omega_de = OL0*(1+A*(Om*(1+z)^3)^2/((B^2+(Om*(1+z)^3)^2)^2))/norm.
    Q3 uses x/(B^2+x^2). HB3 uses x^2/(B^2+x^2)^2 -> narrower resonance."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    x_z = Om*(1+Z_ARR)**3
    x_0 = Om
    f_z = x_z**2/(B**2+x_z**2)**2
    f_0 = x_0**2/(B**2+x_0**2)**2
    return OL0*(1.0+A*(f_z-f_0))


# ============================================================
# MAIN
# ============================================================

print("=== L14 Batch-5: 30 new theories (Phases 41-50) ===")
print("DESI DR2 7-bin chi2. H0=67.7 fixed.\n")

print("--- REFERENCES ---")
_r = fit_model(make_D1_ref, 'D1-prev',
               [[0.28, 0.30, 4.0], [0.30, 0.50, 3.0], [0.28, 0.20, 5.0]])
if _r:
    print(f"D1-prev    p={_r['p']}  chi2={_r['chi2']:.3f}  w0={_r['w0']:.3f}  wa={_r['wa']:.3f}")

MODELS = [
    # Phase 41: Fermi gas
    ('TF1-FermiD',  make_TF1, [[0.28, 2.0, 1.5], [0.30, 5.0, 2.0], [0.28, 3.0, 0.8],
                                [0.28, 1.0, 1.2]]),
    ('TF2-TFpower', make_TF2, [[0.28, 0.5], [0.30, 0.3], [0.28, -0.5], [0.28, 1.0]]),
    ('TF3-FLiquid', make_TF3, [[0.28, 1.0, 0.5], [0.30, 0.5, 1.0], [0.28, 2.0, 0.2],
                                [0.28, 3.0, 0.1]]),
    # Phase 42: Allosteric
    ('AE1-Hill2',   make_AE1, [[0.28, 1.0, 0.3], [0.30, 0.5, 0.5], [0.28, 2.0, 0.1]]),
    ('AE2-Alloste', make_AE2, [[0.28, 0.5, 2.0, 1.5], [0.30, 0.3, 3.0, 2.0],
                                [0.28, 1.0, 1.0, 1.2]]),
    ('AE3-ProdInh', make_AE3, [[0.28, 1.0, 0.3, 0.5], [0.30, 0.5, 0.5, 1.0],
                                [0.28, 2.0, 0.1, 0.3]]),
    # Phase 43: Ising
    ('IS1-IsingMF', make_IS1, [[0.28, 1.0, 2.0], [0.30, 0.5, 3.0], [0.28, 2.0, 1.0]]),
    ('IS2-Boltzman', make_IS2, [[0.28, -0.5], [0.30, -1.0], [0.28, 0.5], [0.28, -2.0]]),
    ('IS3-CritFluc', make_IS3, [[0.28, 0.5, 0.5], [0.30, 0.3, 1.0], [0.28, -0.5, 0.5]]),
    # Phase 44: WdW
    ('WD1-WdWtun',  make_WD1, [[0.28, 1.0, 1.0], [0.30, 0.5, 2.0], [0.28, -1.0, 1.0],
                                [0.28, 2.0, 0.5]]),
    ('WD2-HartHaw', make_WD2, [[0.28, 1.0, 1.0], [0.30, -1.0, 0.5], [0.28, -2.0, 1.0]]),
    ('WD3-Vilenki', make_WD3, [[0.28, 1.0, 0.5], [0.30, 0.5, 1.0], [0.28, 2.0, 0.3],
                                [0.28, 3.0, 0.2]]),
    # Phase 45: Kibble-Zurek
    ('KZ1-KZcorr',  make_KZ1, [[0.28, 1.0, 0.5], [0.30, 0.5, 1.0], [0.28, 2.0, 0.3],
                                [0.28, 3.0, 0.2]]),
    ('KZ2-StrNet',  make_KZ2, [[0.28, 0.3, 0.1, 0.3], [0.30, 0.5, 0.05, 0.2],
                                [0.28, 0.1, 0.0, 0.5]]),
    ('KZ3-ZurekFO', make_KZ3, [[0.28, 1.0, 0.5], [0.30, 0.5, 1.0], [0.28, 2.0, 0.3]]),
    # Phase 46: Verlinde
    ('VE1-Verldark',make_VE1, [[0.28, 0.5], [0.30, 1.0], [0.28, -0.5], [0.28, 2.0]]),
    ('VE2-EntForce',make_VE2, [[0.28, 0.5], [0.30, 1.0], [0.28, 0.3], [0.28, -0.5]]),
    ('VE3-InfoMet', make_VE3, [[0.28, 0.5], [0.30, 1.0], [0.28, -0.5], [0.28, 2.0]]),
    # Phase 47: Lindblad
    ('LD1-Lindbexp',make_LD1, [[0.28, -0.5, 1.0], [0.30, 0.5, 1.0], [0.28, -1.0, 2.0]]),
    ('LD2-LindbGau',make_LD2, [[0.28, -0.5, 1.0], [0.30, -1.0, 0.5], [0.28, 0.5, 1.0]]),
    ('LD3-NonMark', make_LD3, [[0.28, 1.0, 0.5, 2.0], [0.30, 0.5, 1.0, 3.0],
                                [0.28, -1.0, 0.5, 1.0]]),
    # Phase 48: Axion
    ('AX1-AxCosE2', make_AX1, [[0.28, -1.0, 0.5], [0.30, -0.5, 1.0], [0.28, 1.0, 0.5]]),
    ('AX2-AxMisAl', make_AX2, [[0.28, 0.5, 0.5], [0.30, 1.0, 1.0], [0.28, -0.5, 0.5]]),
    ('AX3-AxPotMod',make_AX3, [[0.28, 0.5, 1.0], [0.30, 0.3, 2.0], [0.28, 1.0, 0.5]]),
    # Phase 49: LG
    ('LG1-LGpot',   make_LG1, [[0.28, 1.0, 0.5], [0.30, 0.5, 1.0], [0.28, 2.0, 0.3],
                                [0.28, 3.0, 0.2]]),
    ('LG2-MexHat',  make_LG2, [[0.28, 0.5, 1.2, 0.5], [0.30, 0.3, 1.5, 1.0],
                                [0.28, 1.0, 0.8, 0.3]]),
    ('LG3-LGGauss', make_LG3, [[0.28, -0.5, 0], [0.30, -1.0, 0], [0.28, 0.5, 0], [0.28, -2.0, 0]]),
    # Phase 50: Hybrid
    ('HB1-N3cubic', make_HB1, [[0.28, 1.0, 0.3], [0.30, 0.5, 0.5], [0.28, 2.0, 0.1],
                                [0.28, 3.0, 0.05]]),
    ('HB2-ST1quad', make_HB2, [[0.28, 0.1, 0.3], [0.30, 0.05, 0.5], [0.28, 0.2, 0.1]]),
    ('HB3-Q3high',  make_HB3, [[0.28, 5.0, 0.3], [0.30, 3.0, 0.5], [0.28, 10.0, 0.1]]),
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

print("\n=== BATCH-5 SUMMARY ===")
print(f"LCDM chi2={LCDM_CHI2}  D1-prev chi2={D1_CHI2}\n")
rows.sort(key=lambda x: x[1])
print(f"{'Model':<15} {'chi2':<8} {'dLCDM':<10} {'dD1':<10} {'w0':<9} {'wa':<9} STATUS")
print('-'*78)
game_changers = []
new_bests = []
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
    else:
        st = 'KILL'
    print(f"{lbl:<15} {chi2:<8.3f} {dc:<10.3f} {dd:<10.3f} {w0:<9.3f} {wa:<9.3f} {st}")

print(f"{'LCDM':<15} {LCDM_CHI2:<8.3f} {0.0:<10.3f} {LCDM_CHI2-D1_CHI2:<10.3f} {-1.0:<9.3f} {0.0:<9.3f} KILL")

if game_changers:
    print(f"\nGAME-CHANGER (chi2<{C14_CHI2} AND wa<-0.5):")
    for lbl, chi2, w0, wa in game_changers:
        print(f"  {lbl}: chi2={chi2:.3f}  wa={wa:.3f}")
if new_bests:
    print(f"\nNEW BEST (chi2<D1 {D1_CHI2}):")
    for lbl, chi2, w0, wa in new_bests:
        print(f"  {lbl}: chi2={chi2:.3f}  wa={wa:.3f}")

out_path = os.path.join(_THIS, 'l14_new30e_results.json')
def _j(v):
    if isinstance(v, (np.floating, np.float64, np.float32)): return float(v)
    if isinstance(v, (np.integer,)): return int(v)
    if isinstance(v, list): return [_j(x) for x in v]
    return v
save = {k: {kk: _j(vv) for kk, vv in val.items()} for k, val in results.items()}
with open(out_path, 'w') as f:
    json.dump(save, f, indent=2)
print(f"\nSaved: {out_path}")
