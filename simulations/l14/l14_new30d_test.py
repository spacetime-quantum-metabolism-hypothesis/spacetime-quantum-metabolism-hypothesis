# -*- coding: utf-8 -*-
"""
L14 Batch-4: 30 more new theories from A1+A2. Phases 31-40.

Phase 31: Instanton / Path integral vacuum (IN1-IN3)
Phase 32: Conformal field theory scaling (CF1-CF3)
Phase 33: Quantum chaos / Lyapunov (LC1-LC3)
Phase 34: Levy flight / Heavy-tailed diffusion (LV1-LV3)
Phase 35: Directed percolation / Contact process (DP1-DP3)
Phase 36: Coulomb gas / Log potential (CG1-CG3)
Phase 37: Brane cosmology / Modified Friedmann (BR1-BR3)
Phase 38: Causal set / Poisson sprinkling (CS1-CS3)
Phase 39: Metastable vacuum / Bubble nucleation (VD1-VD3)
Phase 40: Loop quantum cosmology / Holonomy (LQ1-LQ3)
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


# --- D1 reference ---
def make_D1_ref(p):
    Om=p[0]; beta=p[1]; lam=max(p[2],0.0)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    _, I_arr = _precompute_integrals(Om, Z_ARR)
    return OL0*(1.0+beta*(1.0-np.exp(-lam*Om*I_arr)))


# ============================================================
# Phase 31: Instanton / Path integral vacuum
# A1: 시공간 양자 = 진공 인스탄톤. 물질 = 인스탄톤 소멸원.
# 공리 A2: 인스탄톤 응결 = QC 경계.
# ============================================================

def make_IN1(p):
    """IN1: Instanton gas density.
    omega_de = OL0*(1+A*exp(-B/E_LCDM^2)).
    A1: instanton density ~ exp(-S_inst) ~ exp(-B/E^2). Grows with E."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    f_z = np.exp(-B/np.maximum(E**2, 1e-10))
    f_0 = np.exp(-B)  # E(0)=1
    return OL0*(1.0+A*(f_z-f_0))


def make_IN2(p):
    """IN2: Path integral amplitude.
    omega_de = OL0*(1+A*(E_LCDM-1)*exp(-B*(E_LCDM^2-1))).
    A1: path integral weight ~ (E-1)*exp(-B*(E^2-1)). Peak at E~sqrt(1+1/(2B))."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    x = E - 1.0
    return OL0*(1.0+A*x*np.exp(-B*(E**2-1.0)))


def make_IN3(p):
    """IN3: WKB bounce action.
    omega_de = OL0*(1+A*(cosh(B*(E_LCDM-1))-1)).
    A1: bounce factor ~ cosh(S_bounce/hbar). Grows for any sign of A."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    return OL0*(1.0+A*(np.cosh(np.minimum(B*(E-1.0), 20))-1.0))


# ============================================================
# Phase 32: Conformal field theory scaling
# A1: 시공간 양자 = CFT 1차 연산자. 물질 = scaling dimension 변경.
# 공리 A2: 고정점 = 양자-고전 경계.
# ============================================================

def make_CF1(p):
    """CF1: CFT running dimension.
    omega_de = OL0*(1+z)^(-A*(ln(1+z))).
    A1: scaling dimension Delta = A*ln(1+z). Anomalous dilution."""
    Om=p[0]; A=p[1]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    ln1z = np.log(1.0+Z_ARR)
    return OL0*(1.0+Z_ARR)**(-A*ln1z)


def make_CF2(p):
    """CF2: CFT operator mixing.
    omega_de = OL0*(1+A*((1+z)^B-1)) with B freely tunable.
    A1: operator of dimension B mixes into vacuum energy."""
    Om=p[0]; A=p[1]; B=p[2]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    # For wa < 0 need omega_de to grow with z -> need A*(1+z)^B growth
    # B > 0 and A > 0 -> grows. Normalize so z=0 gives OL0.
    return OL0*(1.0+A*((1.0+Z_ARR)**B - 1.0))


def make_CF3(p):
    """CF3: Zamolodchikov c-theorem flow.
    omega_de = OL0*(1+A*ln(1+B*Om*(1+z)^3/OL0)).
    A1: c-function decreases along RG. Dark energy ~ c-function residual."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    arg_z = 1.0+B*Om*(1.0+Z_ARR)**3/max(OL0, 1e-10)
    return OL0*(1.0+A*np.log(np.maximum(arg_z, 1e-10)))


# ============================================================
# Phase 33: Quantum chaos / Lyapunov
# A1: 시공간 양자 밀도 = 양자 카오스 OTOC.
# 물질 = 스크램블러. 공리 A2 = 최대 Lyapunov = QC 경계.
# ============================================================

def make_LC1(p):
    """LC1: OTOC Lyapunov growth.
    omega_de = OL0*(1+A*tanh^2(B*(E_LCDM(z)-1))).
    A1: OTOC ~ tanh^2(lambda*t) ~ saturates at scrambling time."""
    Om=p[0]; A=p[1]; B=max(p[2],0.1)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    return OL0*(1.0+A*np.tanh(np.minimum(B*(E-1.0), 20))**2)


def make_LC2(p):
    """LC2: Rindler scrambling log.
    omega_de = OL0*(1+A*ln(cosh(B*(E_LCDM(z)-1)))).
    A1: scrambling entropy ~ ln(cosh(beta*t)). Grows linearly then logarithmically."""
    Om=p[0]; A=p[1]; B=max(p[2],0.1)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    arg = np.minimum(B*(E-1.0), 20)
    return OL0*(1.0+A*np.log(np.maximum(np.cosh(arg), 1e-10)))


def make_LC3(p):
    """LC3: SYK spectral form factor.
    omega_de = OL0*(1+A*(E_LCDM(z)^B-1)).
    A1: SYK density of states ~ E^B. Power B encodes quantum chaos."""
    Om=p[0]; A=p[1]; B=p[2]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    return OL0*(1.0+A*(E**B - 1.0))


# ============================================================
# Phase 34: Levy flight / Heavy-tailed diffusion
# A1: 시공간 양자 = Levy 안정 분포 확산자.
# 물질 = heavy-tail truncation. 공리 A2 = Gaussian 극한 = QC.
# ============================================================

def make_LV1(p):
    """LV1: Levy stable density tail.
    omega_de = OL0/(1+(Om*(1+z)^3/OL0)^A).
    A1: Levy stable CDF ~ 1/(1+x^alpha). omega_de = OL0 * CDF complement."""
    Om=p[0]; A=max(p[1],0.1)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    r_z = np.maximum(Om*(1+Z_ARR)**3/max(OL0, 1e-10), 1e-10)
    r_0 = Om/max(OL0, 1e-10)
    # normalize: at z=0, OL0/(1+(r_0)^A)
    f_z = 1.0/(1.0+r_z**A)
    f_0 = 1.0/(1.0+r_0**A)
    return OL0*f_z/f_0


def make_LV2(p):
    """LV2: Fractional diffusion anomalous scaling.
    omega_de = OL0*(1+A*((1+z)^(3*alpha)-1)) with alpha < 1.
    A1: sub-diffusion index alpha. Dark energy ~ anomalous volume."""
    Om=p[0]; A=p[1]; alpha=np.clip(p[2], 0.01, 0.99)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    return OL0*(1.0+A*((1+Z_ARR)**(3*alpha)-1.0))


def make_LV3(p):
    """LV3: Stretched exponential Levy.
    omega_de = OL0*exp(-A*(Om*(1+z)^3/OL0)^alpha).
    A1: Levy flight return probability ~ exp(-D*r^alpha). Decay ~ winding."""
    Om=p[0]; A=max(p[1],0.0); alpha=np.clip(p[2], 0.1, 1.0)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    r_z = np.maximum(Om*(1+Z_ARR)**3/max(OL0, 1e-10), 1e-10)
    r_0 = Om/max(OL0, 1e-10)
    return OL0*np.exp(-A*(r_z**alpha - r_0**alpha))


# ============================================================
# Phase 35: Directed percolation / Contact process
# A1: 시공간 양자 = 활성 site. 물질 = site 비활성화.
# 공리 A2: 비활성 비율 = 1/2 에서 DP 임계점 = QC 경계.
# ============================================================

def make_DP1(p):
    """DP1: DP order parameter near critical.
    omega_de = OL0*(1-A*(Om*(1+z)^3/OL0)^B*(1+Om*(1+z)^3/OL0)^(-B-1)).
    A1: DP density rho ~ (p-p_c)^beta_DP. Dark energy ~ vacuum density."""
    Om=p[0]; A=p[1]; B=max(p[2],0.1)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    r_z = np.maximum(Om*(1+Z_ARR)**3/max(OL0, 1e-10), 0)
    r_0 = Om/max(OL0, 1e-10)
    f_z = r_z**B/np.maximum((1.0+r_z)**(B+1), 1e-10)
    f_0 = r_0**B/max((1.0+r_0)**(B+1), 1e-10)
    return OL0*(1.0-A*(f_z-f_0))


def make_DP2(p):
    """DP2: Contact process survival probability.
    omega_de = OL0*(1+A*(1-(1+z)^(-B))).
    A1: survival prob S(t) ~ 1-t^(-delta). In redshift: S ~ 1-(1+z)^(-B)."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    return OL0*(1.0+A*(1.0-(1.0+Z_ARR)**(-B)))


def make_DP3(p):
    """DP3: Reggeon field theory vacuum.
    omega_de = OL0*(1+A*E_LCDM(z)^(-B)*(E_LCDM(z)-1)).
    A1: Reggeon propagator ~ E^(-B)*(E-1). Pomeron exchange."""
    Om=p[0]; A=p[1]; B=max(p[2],0.0)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    return OL0*(1.0+A*E**(-B)*(E-1.0))


# ============================================================
# Phase 36: Coulomb gas / Log potential
# A1: 시공간 양자 = 대수 포텐셜 입자. 물질 = 전하 스크리닝.
# 공리 A2: Berezinskii-Kosterlitz-Thouless 전이 = QC 경계.
# ============================================================

def make_CG1(p):
    """CG1: Log-normal Coulomb.
    omega_de = OL0*exp(-A*(ln(E_LCDM(z)))^2).
    A1: Coulomb gas free energy ~ (ln E)^2. Grows then decays."""
    Om=p[0]; A=p[1]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    lnE = np.log(np.maximum(E, 1e-10))
    return OL0*np.exp(-A*lnE**2)


def make_CG2(p):
    """CG2: BKT vortex unbinding.
    omega_de = OL0*(1+A*exp(-B/ln(E_LCDM(z)+1))).
    A1: vortex free energy ~ exp(-pi*rho_s/T) ~ exp(-B/ln(E+1))."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    lnEp1 = np.log(np.maximum(E+1.0, 1.01))
    f_z = np.exp(-B/lnEp1)
    f_0 = np.exp(-B/np.log(2.0))  # E(0)=1, ln(2)
    return OL0*(1.0+A*(f_z-f_0))


def make_CG3(p):
    """CG3: Debye screening exponential.
    omega_de = OL0*exp(A*(1-E_LCDM(z))).
    A1: Debye screened potential ~ exp(-kappa*r) ~ exp(A*(1-E)). A<0 grows."""
    Om=p[0]; A=p[1]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    # At z=0: E=1, exp(A*0)=1 -> OL0. Normalizes automatically.
    return OL0*np.exp(A*(1.0-E))


# ============================================================
# Phase 37: Brane cosmology / Randall-Sundrum
# A1: 시공간 양자 = 여분차원 KK 모드. 물질 = brane 위 에너지.
# 공리 A2: KK 갭 = QC 경계.
# ============================================================

def make_BR1(p):
    """BR1: Randall-Sundrum brane tension correction.
    omega_de = OL0*(1+A*Om*(1+z)^3/sqrt(OL0+Om*(1+z)^3)).
    A1: RS dark energy ~ rho_m/sqrt(sigma_brane). Tension correction."""
    Om=p[0]; A=p[1]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    rho_m = Om*(1+Z_ARR)**3
    rho_m_0 = Om
    denom_z = np.sqrt(np.maximum(OL0+rho_m, 1e-10))
    denom_0 = np.sqrt(max(OL0+rho_m_0, 1e-10))
    delta = rho_m/denom_z - rho_m_0/denom_0
    return OL0*(1.0+A*delta)


def make_BR2(p):
    """BR2: DGP modified Friedmann.
    omega_de = OL0/(1+A*Om*(1+z)^3/OL0).
    A1: DGP vacuum energy ~ 1/(1+rho_m/rho_DE). Grows as matter dilutes."""
    Om=p[0]; A=max(p[1],0.0)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    r_z = Om*(1+Z_ARR)**3/max(OL0, 1e-10)
    r_0 = Om/max(OL0, 1e-10)
    return OL0*(1.0+A*r_0)/(1.0+A*r_z)


def make_BR3(p):
    """BR3: Gauss-Bonnet brane correction.
    omega_de = OL0*(1-A*(E_LCDM^2-1)/(1+B*E_LCDM^2)).
    A1: GB coupling alpha ~ A. Shifts vacuum energy."""
    Om=p[0]; A=p[1]; B=max(p[2],0.0)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    delta_z = (E**2-1.0)/(1.0+B*E**2)
    delta_0 = 0.0  # E(0)=1 -> E^2-1=0 -> delta_0=0
    return OL0*(1.0-A*(delta_z-delta_0))


# ============================================================
# Phase 38: Causal set / Poisson sprinkling
# A1: 시공간 양자 = causal set 원소 (sprinkling).
# 물질 = 원소 상관 소거. 공리 A2 = 연속 극한 = QC 경계.
# ============================================================

def make_CS1(p):
    """CS1: Causal set sprinkled volume.
    omega_de = OL0*(1+A*(chi_comoving(z)/chi_0)^B-A).
    A1: causal set density ~ comoving volume^B. Sprinkled quanta."""
    Om=p[0]; A=p[1]; B=max(p[2],0.1)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    # chi(z) ~ integral 1/E from 0 to z
    E = _E_LCDM(Om, Z_ARR)
    chi = np.zeros(len(Z_ARR))
    for i in range(1, len(Z_ARR)):
        dz = Z_ARR[i]-Z_ARR[i-1]
        chi[i] = chi[i-1]+0.5*(1/E[i-1]+1/E[i])*dz
    chi_max = max(chi[-1], 1e-10)
    frac = chi/chi_max
    # normalize at z=0: frac=0 -> f_z=0, so omega_de(0)=OL0*(1+A*0-A)=OL0*(1-A)? No.
    # Let's use delta form:
    return OL0*(1.0+A*(frac**B - 0.0))


def make_CS2(p):
    """CS2: Causal diamond entropy.
    omega_de = OL0*(1+A*(1-exp(-B*chi^2(z)))).
    A1: causal diamond entropy ~ chi^2. Dark energy ~ entropy accumulation."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    chi = np.zeros(len(Z_ARR))
    for i in range(1, len(Z_ARR)):
        dz = Z_ARR[i]-Z_ARR[i-1]
        chi[i] = chi[i-1]+0.5*(1/E[i-1]+1/E[i])*dz
    return OL0*(1.0+A*(1.0-np.exp(-B*chi**2)))


def make_CS3(p):
    """CS3: Poisson fluctuation vacuum.
    omega_de = OL0*(1+A*arctan(B*(Om*(1+z)^3/OL0-Om/OL0))).
    A1: Poisson fluctuation in sprinkled density -> arctan saturation."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    r_z = Om*(1+Z_ARR)**3/max(OL0, 1e-10)
    r_0 = Om/max(OL0, 1e-10)
    return OL0*(1.0+A*np.arctan(B*(r_z-r_0)))


# ============================================================
# Phase 39: Metastable vacuum / Bubble nucleation
# A1: 시공간 양자 = false vacuum 기포 핵생성.
# 물질 = true vacuum 전파. 공리 A2 = 핵생성 전이 = QC 경계.
# ============================================================

def make_VD1(p):
    """VD1: Coleman-de Luccia bubble nucleation.
    omega_de = OL0*(1-A*(1-exp(-B*(E_LCDM-1)^2))).
    A1: tunneling rate ~ exp(-S_E) ~ exp(-B*(E-1)^2). Vacuum decays."""
    Om=p[0]; A=max(p[1],0.0); B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    return OL0*(1.0-A*(1.0-np.exp(-B*(E-1.0)**2)))


def make_VD2(p):
    """VD2: Hawking-Moss instanton.
    omega_de = OL0*exp(-A*(1-exp(-B/E_LCDM^2))).
    A1: HM rate ~ exp(-24*pi^2/Lambda). Grows with E (vacuum energy tracks H)."""
    Om=p[0]; A=max(p[1],0.0); B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    f_z = 1.0-np.exp(-B/np.maximum(E**2, 1e-10))
    f_0 = 1.0-np.exp(-B)  # E(0)=1
    return OL0*np.exp(-A*(f_z-f_0))


def make_VD3(p):
    """VD3: Thin-wall bubble mass.
    omega_de = OL0*(1+A*Om*(1+z)^3/(B+Om*(1+z)^3))^C.
    A1: bubble nucleation rate ~ (matter density)^C / (tension+density)^C."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01); C=p[3]
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    x_z = Om*(1+Z_ARR)**3
    x_0 = Om
    f_z = x_z/(B+x_z)
    f_0 = x_0/(B+x_0)
    return OL0*(1.0+A*(f_z-f_0))**C


# ============================================================
# Phase 40: Loop quantum cosmology / Holonomy
# A1: 시공간 양자 = spin foam 꼭짓점. 물질 = 홀로노미 변형.
# 공리 A2: 홀로노미 임계 밀도 = QC 경계.
# ============================================================

def make_LQ1(p):
    """LQ1: LQC holonomy correction.
    omega_de = OL0*(1+A*sin^2(B*sqrt(Om*(1+z)^3/OL0))).
    A1: LQC Friedmann: H^2 = (8piG/3)*rho*(1-rho/rho_c).
    sin^2 structure from holonomy."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    r_z = np.maximum(Om*(1+Z_ARR)**3/max(OL0, 1e-10), 0)
    r_0 = Om/max(OL0, 1e-10)
    f_z = np.sin(B*np.sqrt(r_z))**2
    f_0 = np.sin(B*np.sqrt(r_0))**2
    return OL0*(1.0+A*(f_z-f_0))


def make_LQ2(p):
    """LQ2: Spin foam vertex amplitude.
    omega_de = OL0*(1+A*(1-cos(B*(E_LCDM(z)-1)))).
    A1: spin foam amplitude ~ (1-cos(theta)). Area quantization."""
    Om=p[0]; A=p[1]; B=max(p[2],0.01)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    return OL0*(1.0+A*(1.0-np.cos(B*(E-1.0))))


def make_LQ3(p):
    """LQ3: Polymer quantization.
    omega_de = OL0*(sin(B*E_LCDM(z))/sin(B))^2 / E_LCDM(z)^2.
    A1: polymer quantized momentum -> sin(mu*p)/mu. Vacuum energy ~ (sin/sin)^2."""
    Om=p[0]; A=p[1]; B=np.clip(p[2], 0.01, 1.5)
    OL0=1.0-Om-OMEGA_R
    if OL0 < 0.01: return None
    E = _E_LCDM(Om, Z_ARR)
    sin0 = np.sin(B)
    if abs(sin0) < 1e-10: return None
    sin_z = np.sin(np.minimum(B*E, np.pi-1e-6))
    return OL0*A*(sin_z/sin0)**2 / np.maximum(E**2, 1e-10) + OL0*(1-A)


# ============================================================
# MAIN
# ============================================================

print("=== L14 Batch-4: 30 new theories (Phases 31-40) ===")
print("DESI DR2 7-bin chi2. H0=67.7 fixed.\n")

print("--- REFERENCES ---")
_r = fit_model(make_D1_ref, 'D1-prev',
               [[0.28, 0.30, 4.0], [0.30, 0.50, 3.0], [0.28, 0.20, 5.0]])
if _r:
    print(f"D1-prev    p={_r['p']}  chi2={_r['chi2']:.3f}  w0={_r['w0']:.3f}  wa={_r['wa']:.3f}")

MODELS = [
    # Phase 31: Instanton
    ('IN1-InstGas', make_IN1, [[0.28, 1.0, 1.0], [0.30, 0.5, 2.0], [0.28, -1.0, 1.0],
                                [0.28, 2.0, 0.5]]),
    ('IN2-PathInt', make_IN2, [[0.28, 1.0, 1.0], [0.30, 0.5, 2.0], [0.28, 2.0, 0.5],
                                [0.28, 3.0, 0.3]]),
    ('IN3-WKBboun', make_IN3, [[0.28, 0.5, 1.0], [0.30, 0.3, 2.0], [0.28, 1.0, 0.5],
                                [0.28, -0.5, 1.0]]),
    # Phase 32: CFT
    ('CF1-CFTanom', make_CF1, [[0.28, 0.3], [0.30, 0.5], [0.28, 0.1], [0.28, 1.0]]),
    ('CF2-CFTmix',  make_CF2, [[0.28, 0.5, 0.3], [0.30, 0.3, 0.5], [0.28, 0.1, 1.0],
                                [0.28, 0.2, 0.5], [0.28, -0.1, 0.3]]),
    ('CF3-Zamolo',  make_CF3, [[0.28, 0.5, 0.3], [0.30, 0.3, 0.5], [0.28, 1.0, 0.1]]),
    # Phase 33: Lyapunov
    ('LC1-OTOC',    make_LC1, [[0.28, 1.0, 1.0], [0.30, 0.5, 2.0], [0.28, 2.0, 0.5]]),
    ('LC2-Rindler', make_LC2, [[0.28, 0.5, 1.0], [0.30, 0.3, 2.0], [0.28, 1.0, 0.5]]),
    ('LC3-SYK',     make_LC3, [[0.28, 0.5, 1.5], [0.30, 0.3, 2.0], [0.28, 0.1, 3.0],
                                [0.28, -0.1, 0.5]]),
    # Phase 34: Levy
    ('LV1-LevyCDF', make_LV1, [[0.28, 0.3], [0.30, 0.5], [0.28, 0.1], [0.28, 1.0]]),
    ('LV2-FracDiff',make_LV2, [[0.28, 0.5, 0.7], [0.30, 0.3, 0.5], [0.28, 1.0, 0.3]]),
    ('LV3-StrExp',  make_LV3, [[0.28, 0.5, 0.5], [0.30, 0.3, 0.7], [0.28, 1.0, 0.3]]),
    # Phase 35: DP
    ('DP1-DPorder', make_DP1, [[0.28, 1.0, 0.5], [0.30, 0.5, 1.0], [0.28, 2.0, 0.3]]),
    ('DP2-Contact', make_DP2, [[0.28, 0.5, 0.5], [0.30, 0.3, 1.0], [0.28, 1.0, 0.2]]),
    ('DP3-Reggeon', make_DP3, [[0.28, 0.5, 0.5], [0.30, 0.3, 1.0], [0.28, 1.0, 0.0]]),
    # Phase 36: Coulomb gas
    ('CG1-LogNorm', make_CG1, [[0.28, 1.0], [0.30, 0.5], [0.28, 2.0], [0.28, -1.0]]),
    ('CG2-BKTvort', make_CG2, [[0.28, 1.0, 1.0], [0.30, 0.5, 2.0], [0.28, -1.0, 1.0]]),
    ('CG3-Debye',   make_CG3, [[0.28, -0.5], [0.30, -1.0], [0.28, 0.5], [0.28, -2.0]]),
    # Phase 37: Brane
    ('BR1-RStens',  make_BR1, [[0.28, 0.5], [0.30, 1.0], [0.28, -0.5], [0.28, 2.0]]),
    ('BR2-DGP',     make_BR2, [[0.28, 0.5], [0.30, 1.0], [0.28, 2.0], [0.28, 0.1]]),
    ('BR3-GaussBon',make_BR3, [[0.28, 0.5, 0.5], [0.30, 0.3, 1.0], [0.28, 1.0, 0.0]]),
    # Phase 38: Causal set
    ('CS1-CausalV', make_CS1, [[0.28, 0.5, 0.5], [0.30, 1.0, 1.0], [0.28, 0.3, 2.0]]),
    ('CS2-DiamEnt', make_CS2, [[0.28, 0.5, 0.5], [0.30, 0.3, 1.0], [0.28, 1.0, 0.2]]),
    ('CS3-Poisson', make_CS3, [[0.28, 0.5, 0.5], [0.30, 0.3, 1.0], [0.28, 1.0, 0.2]]),
    # Phase 39: Vacuum decay
    ('VD1-CdL',     make_VD1, [[0.28, 0.3, 1.0], [0.30, 0.5, 0.5], [0.28, 0.1, 2.0]]),
    ('VD2-HawkMos', make_VD2, [[0.28, 0.5, 1.0], [0.30, 0.3, 2.0], [0.28, 1.0, 0.5]]),
    ('VD3-ThinWal', make_VD3, [[0.28, 1.0, 0.3, 1.0], [0.30, 0.5, 0.5, 2.0],
                                [0.28, 2.0, 0.1, 0.5]]),
    # Phase 40: LQC
    ('LQ1-LQChol',  make_LQ1, [[0.28, 0.5, 0.5], [0.30, 1.0, 1.0], [0.28, 0.3, 0.3]]),
    ('LQ2-SpinFoam',make_LQ2, [[0.28, 0.5, 1.0], [0.30, 0.3, 2.0], [0.28, 1.0, 0.5]]),
    ('LQ3-Polymer', make_LQ3, [[0.28, 1.0, 0.5], [0.30, 0.5, 1.0], [0.28, 2.0, 0.3]]),
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

print("\n=== BATCH-4 SUMMARY ===")
print(f"LCDM chi2={LCDM_CHI2}  D1-prev chi2={D1_CHI2}\n")
rows.sort(key=lambda x: x[1])
print(f"{'Model':<14} {'chi2':<10} {'dLCDM':<12} {'dD1':<12} {'w0':<10} {'wa':<10} STATUS")
print('-'*80)
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
    print(f"{lbl:<14} chi2={chi2:<6.3f}  dLCDM={dc:<7.3f}  dD1={dd:<7.3f}  w0={w0:<8.3f}  wa={wa:<8.3f}  {st}")

print(f"{'LCDM':<14} chi2={LCDM_CHI2:<6.3f}  dLCDM=0.000    dD1={LCDM_CHI2-D1_CHI2:<7.3f}  w0=-1.000    wa=0.000     KILL")

if game_changers:
    print(f"\nGAME-CHANGER (chi2<{C14_CHI2} AND wa<-0.5):")
    for lbl, chi2, w0, wa in game_changers:
        print(f"  {lbl}: chi2={chi2:.3f}  wa={wa:.3f}")
if new_bests:
    print(f"\nNEW BEST (chi2<D1 {D1_CHI2}):")
    for lbl, chi2, w0, wa in new_bests:
        print(f"  {lbl}: chi2={chi2:.3f}  wa={wa:.3f}")

out_path = os.path.join(_THIS, 'l14_new30d_results.json')
def _j(v):
    if isinstance(v, (np.floating, np.float64, np.float32)): return float(v)
    if isinstance(v, (np.integer,)): return int(v)
    if isinstance(v, list): return [_j(x) for x in v]
    return v
save = {k: {kk: _j(vv) for kk, vv in val.items()} for k, val in results.items()}
with open(out_path, 'w') as f:
    json.dump(save, f, indent=2)
print(f"\nSaved: {out_path}")
