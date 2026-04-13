# -*- coding: utf-8 -*-
"""
L14 New-30 DESI Test: 30 new theories from axioms A1+A2 only.
All base.md equations (sigma*n*rho_m, Gamma_0=const) discarded.

Axiom A1: Matter annihilates spacetime quanta; empty space creates them.
Axiom A2: From A1, the quantum-classical boundary is derivable.

10 phenomenological interpretations x 3 theories = 30 total.

CLAUDE.md rules:
  - No unicode in print()
  - numpy 2.x: trapezoid
  - H0=67.7 fixed
  - 7-bin diagonal chi2 DESI DR2
  - Om in [0.28, 0.36]
"""
from __future__ import annotations
import os, json
import numpy as np
from scipy.integrate import odeint
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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

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
    print(label + '  p=' + str([round(x, 4) for x in p_best]) +
          '  chi2=' + str(round(c2, 3)) +
          '  w0=' + str(round(w0, 3)) + '  wa=' + str(round(wa, 3)))
    return p_best, c2, w0, wa, arr


# Precompute J(z) = integral_0^z (1+z')^2 / E_LCDM(z') dz'
# and I(z) = integral_0^z (1+z')^3 / E_LCDM(z') dz'  [for D1]
# These use LCDM background (Om=0.315 typical)
def _precompute_integrals(Om, z_arr):
    OL0 = 1.0 - Om - OMEGA_R
    E2 = OMEGA_R*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E = np.sqrt(np.maximum(E2, 1e-15))
    # J(z): integrand = (1+z)^2 / E
    intg_J = (1+z_arr)**2 / E
    # I(z): integrand = (1+z)^3 / E
    intg_I = (1+z_arr)**3 / E
    # Cumulative trapezoidal
    J = np.zeros_like(z_arr)
    I = np.zeros_like(z_arr)
    for i in range(1, len(z_arr)):
        dz = z_arr[i] - z_arr[i-1]
        J[i] = J[i-1] + 0.5*(intg_J[i-1]+intg_J[i])*dz
        I[i] = I[i-1] + 0.5*(intg_I[i-1]+intg_I[i])*dz
    return J, I


# ---------------------------------------------------------------------------
# Reference models
# ---------------------------------------------------------------------------

def make_LCDM(p):
    Om = p[0]; OL0 = 1.0-Om-OMEGA_R
    return np.full(len(Z_ARR), OL0)

def make_A01(p):
    Om = p[0]; OL0 = 1.0-Om-OMEGA_R
    a = 1.0/(1+Z_ARR)
    return OL0*(1.0+Om*(1.0-a))

def make_C14(p):
    Om = p[0]; OL0 = 1.0-Om-OMEGA_R
    a = 1.0/(1+Z_ARR)
    return OL0*(1.0+2.0*Om*(1.0-a))


# ---------------------------------------------------------------------------
# Phase 1: Diffusion / Survival probability
# ---------------------------------------------------------------------------

def make_D1(p):
    """D1: Gaussian survival. omega_de = OL0*(1+beta*(1-exp(-lam*Om*I(z))))"""
    Om = p[0]; beta = p[1]; lam = max(p[2], 0.0)
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    _, I_arr = _precompute_integrals(Om, Z_ARR)
    return OL0 * (1.0 + beta * (1.0 - np.exp(-lam * Om * I_arr)))

def make_D2(p):
    """D2: MFPT lifetime: omega_de = OL0*exp(mu*Om*(1+z)^3*t_lookback/t0)
    Approximate: t_lookback ~ z/H0/E_avg. Use t(z)~=1/H0 * int_z^inf dz'/((1+z')E)
    Simplify: omega_de = OL0*(1 + mu*Om*z/(1+z))  [late-time approx of MFPT integral]
    """
    Om = p[0]; mu = p[1]
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    return OL0 * (1.0 + mu*Om*Z_ARR/(1.0+Z_ARR))

def make_D3(p):
    """D3: Levy flight power law. omega_de = OL0*(1+delta*((1+z)^rho-1))"""
    Om = p[0]; delta = max(p[1], 0.0); rho = max(p[2], 0.0)
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    return OL0 * (1.0 + delta * ((1+Z_ARR)**rho - 1.0))


# ---------------------------------------------------------------------------
# Phase 2: Percolation / Network
# ---------------------------------------------------------------------------

def make_P1(p):
    """P1: Giant component. omega_de = OL0*(1+f*Om*((1+z)^3-1))
    [recovers A01 family when f~Om^{-1}/3, grows cubic -- different from A01's linear]"""
    Om = p[0]; f = max(p[1], 0.0)
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    return OL0 * (1.0 + f * Om * ((1+Z_ARR)**3 - 1.0))

def make_P2(p):
    """P2: Correlation length resonance. Extra ln(1+z) factor.
    omega_de = OL0*(1 + nu*(Om/OL0)*((1+z)^3-1)*ln(1+z))"""
    Om = p[0]; nu = p[1]
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    return OL0 * (1.0 + nu*(Om/OL0)*((1+Z_ARR)**3-1.0)*np.log1p(Z_ARR))

def make_P3(p):
    """P3: Bond percolation saturation.
    omega_de = OL0*(1-exp(-kap*(1+z)^3))/(1-exp(-kap))"""
    Om = p[0]; kap = max(p[1], 1e-6)
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    denom = 1.0 - np.exp(-kap)
    if abs(denom) < 1e-10:
        return None
    arr = OL0 * (1.0 - np.exp(-kap*(1+Z_ARR)**3)) / denom
    return np.maximum(arr, 0.0)


# ---------------------------------------------------------------------------
# Phase 3: Ecology / Predator-Prey
# ---------------------------------------------------------------------------

def make_E1(p):
    """E1: Logistic LV. omega_de = OL0*(1+xi*Om*(1+z)^{3/2}/OL0)"""
    Om = p[0]; xi = p[1]
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    return OL0 * (1.0 + xi * Om * (1+Z_ARR)**1.5 / OL0)

def make_E2(p):
    """E2: Holling Type II. omega_de = OL0*(1+phi*(Omega_m(z)-Om))
    Omega_m(z) = Om*(1+z)^3/E_LCDM(z)^2. phi > 0."""
    Om = p[0]; phi = p[1]
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    E2_LCDM = OMEGA_R*(1+Z_ARR)**4 + Om*(1+Z_ARR)**3 + OL0
    Omega_m_z = Om*(1+Z_ARR)**3 / np.maximum(E2_LCDM, 1e-15)
    return OL0 * (1.0 + phi * (Omega_m_z - Om))

def make_E3(p):
    """E3: Allee effect. omega_de = OL0*(1+zeta*Om*((1+z)^{3/2}-1)/OL0)"""
    Om = p[0]; zeta = p[1]
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    return OL0 * (1.0 + zeta * Om * ((1+Z_ARR)**1.5 - 1.0) / OL0)


# ---------------------------------------------------------------------------
# Phase 4: Reaction-Diffusion / Turing
# ---------------------------------------------------------------------------

def make_R1(p):
    """R1: Gierer-Meinhardt (Michaelis-Menten saturation).
    omega_de = OL0*(1+g*Om*((1+z)^3-1)/(OL0+Om*(1+z)^3))"""
    Om = p[0]; g = max(p[1], 0.0)
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    num = Om * ((1+Z_ARR)**3 - 1.0)
    den = OL0 + Om*(1+Z_ARR)**3
    return OL0 * (1.0 + g * num/np.maximum(den, 1e-15))

def make_R2(p):
    """R2: Gray-Scott square root. omega_de = OL0*sqrt((1+lam*(1+z)^3)/(1+lam))"""
    Om = p[0]; lam = max(p[1], 0.0)
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    arr = OL0 * np.sqrt((1.0 + lam*(1+Z_ARR)**3) / max(1.0+lam, 1e-10))
    return np.maximum(arr, 0.0)

def make_R3(p):
    """R3: Thomas substrate (same Michaelis-Menten form as R1, different origin).
    omega_de = OL0*(1+g*Om*((1+z)^3-1)/(OL0+Om*(1+z)^3)) -- same as R1."""
    # Identical structure to R1; test separately to confirm numerical consistency
    return make_R1(p)


# ---------------------------------------------------------------------------
# Phase 5: Condensed matter / Phase transition (Landau)
# ---------------------------------------------------------------------------

def make_L1(p):
    """L1: 2nd-order Landau + Ising. omega_de = OL0*(1+f*Om^{2/3}*((1+z)^2-1)/OL0^{2/3})"""
    Om = p[0]; f = p[1]
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    prefac = Om**(2.0/3.0) / OL0**(2.0/3.0)
    return OL0 * (1.0 + f * prefac * ((1+Z_ARR)**2 - 1.0))

def make_L2(p):
    """L2: 1st-order Landau / Maxwell construction. omega_de = OL0*exp(f*Om*((1+z)^3-1)/OL0)"""
    Om = p[0]; f = max(p[1], 0.0)
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    exponent = f * Om * ((1+Z_ARR)**3 - 1.0) / OL0
    arr = OL0 * np.exp(np.minimum(exponent, 50.0))
    return np.maximum(arr, 0.0)

def make_L3(p):
    """L3: Wilson RG running. omega_de = OL0*(1+z)^rho [pure power law].
    rho=0 recovers LCDM."""
    Om = p[0]; rho = p[1]
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    return OL0 * (1+Z_ARR)**rho


# ---------------------------------------------------------------------------
# Phase 6: Information / Entanglement
# ---------------------------------------------------------------------------

def make_I1(p):
    """I1: Entanglement entropy decoherence recoil.
    omega_de = OL0*(1+beta*Om*(1+z)^3)/(1+beta*Om)"""
    Om = p[0]; beta = max(p[1], 0.0)
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    arr = OL0 * (1.0 + beta*Om*(1+Z_ARR)**3) / max(1.0+beta*Om, 1e-10)
    return np.maximum(arr, 0.0)

def make_I2(p):
    """I2: Quantum discord cumulative.
    omega_de = OL0*(1+xi*J(z)) where J(z) = integral_0^z (1+z')^2/E_LCDM dz'"""
    Om = p[0]; xi = p[1]
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    J_arr, _ = _precompute_integrals(Om, Z_ARR)
    return OL0 * (1.0 + xi * J_arr)

def make_I3(p):
    """I3: Holevo ODE. d(u)/dz = phi*u*(1+z)^2 / sqrt(Om*(1+z)^3 + u)
    With u(0)=OL0."""
    Om = p[0]; phi = p[1]
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None

    def rhs(state, z):
        u = max(state[0], 1e-15)
        denom = max(Om*(1+z)**3 + u, 1e-15)**0.5
        du = phi * u * (1+z)**2 / denom
        return [du]

    sol = odeint(rhs, [OL0], Z_ARR, rtol=1e-9, atol=1e-12, mxstep=20000)
    arr = sol[:, 0]
    if not np.isfinite(arr).all() or arr.max() > 1e6:
        return None
    return np.maximum(arr, 0.0)


# ---------------------------------------------------------------------------
# Phase 7: Gauge field / Vacuum condensate
# ---------------------------------------------------------------------------

def make_G1(p):
    """G1: Mexican hat VEV shift. omega_de = OL0*(1+eta*((1+z)^3-1))^2"""
    Om = p[0]; eta = max(p[1], 0.0)
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    arr = OL0 * (1.0 + eta*((1+Z_ARR)**3 - 1.0))**2
    return np.maximum(arr, 0.0)

def make_G2(p):
    """G2: Nambu-Goldstone condensate. omega_de = OL0*(1+delta*Om*((1+z)^3-1))
    [Same structure as P1 with reparametrization f->delta; independent A1+A2 derivation]"""
    Om = p[0]; delta = max(p[1], 0.0)
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    return OL0 * (1.0 + delta * Om * ((1+Z_ARR)**3 - 1.0))

def make_G3(p):
    """G3: Higgs phase transition (peaked form).
    omega_de = OL0*(1+z)^3*exp((1-(1+z)^3)/OH). OH>0 sets peak redshift.
    Peak at z_c where d/dz[(1+z)^3*exp(...)]=0 => (1+z_c)^3 = OH."""
    Om = p[0]; OH = max(p[1], 0.1)
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    exponent = (1.0 - (1+Z_ARR)**3) / OH
    arr = OL0 * (1+Z_ARR)**3 * np.exp(np.maximum(exponent, -200.0))
    # Renormalize so u(0) = OL0
    arr0 = OL0 * 1.0 * np.exp(0.0)  # at z=0: (1)^3 * exp(0) = 1
    if abs(arr0) < 1e-15:
        return None
    return arr  # already = OL0 at z=0


# ---------------------------------------------------------------------------
# Phase 8: Discrete / Cellular automaton
# ---------------------------------------------------------------------------

def make_CA1(p):
    """CA1: Mean-field automaton.
    omega_de = OL0*(1+lam*Om*(1-exp(-tau*Om*((1+z)^3-1))))
    1-param: combine lam*tau -> effective A (tau=1/Om for simplicity)."""
    Om = p[0]; A = max(p[1], 0.0)
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    # Set tau so that saturation scale ~ 1 at z~1: tau*Om*((2)^3-1)=1 => tau=1/(7*Om)
    tau_eff = 1.0 / max(7.0*Om, 1e-10)
    arr = OL0 * (1.0 + A * Om * (1.0 - np.exp(-tau_eff * Om * ((1+Z_ARR)**3 - 1.0))))
    return np.maximum(arr, 0.0)

def make_CA2(p):
    """CA2: Rule-110 interface density (peaked rational form).
    omega_de = OL0*(1+mu)^2*(1+z)^3/(1+mu*(1+z)^3)^2"""
    Om = p[0]; mu = max(p[1], 1e-6)
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    z3 = (1+Z_ARR)**3
    arr = OL0 * (1.0+mu)**2 * z3 / np.maximum((1.0+mu*z3)**2, 1e-15)
    # Normalize: at z=0, u = OL0*(1+mu)^2/(1+mu)^2 = OL0 ✓
    return np.maximum(arr, 0.0)

def make_CA3(p):
    """CA3: Game of Life peaked.
    omega_de = OL0*(1+z)^3*exp((1-(1+z)^3)/OGoL) -- same as G3 structure."""
    return make_G3(p)  # structurally identical to G3


# ---------------------------------------------------------------------------
# Phase 9: Fluid / Vortex
# ---------------------------------------------------------------------------

def make_V1(p):
    """V1: Turbulent vortex cascade.
    omega_de = OL0*sqrt((E_LCDM(z) + psi*(1+z)^3)/(1+psi))"""
    Om = p[0]; psi = max(p[1], 0.0)
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    E2_LCDM = OMEGA_R*(1+Z_ARR)**4 + Om*(1+Z_ARR)**3 + OL0
    E_LCDM = np.sqrt(np.maximum(E2_LCDM, 1e-15))
    arr = OL0 * np.sqrt((E_LCDM + psi*(1+Z_ARR)**3) / max(1.0+psi, 1e-10))
    return np.maximum(arr, 0.0)

def make_V2(p):
    """V2: Kelvin circulation theorem.
    omega_de = OL0*exp(nu*J(z)) where J(z) = integral_0^z (1+z')^2/E_LCDM dz'"""
    Om = p[0]; nu = p[1]
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    J_arr, _ = _precompute_integrals(Om, Z_ARR)
    arr = OL0 * np.exp(np.minimum(nu * J_arr, 50.0))
    return np.maximum(arr, 0.0)

def make_V3(p):
    """V3: Quantum vortex reconnection.
    omega_de = OL0/(1 - zeta*J(z)). Diverges when zeta*J(z_max)->1.
    Restrict zeta < 1/J_max for convergence."""
    Om = p[0]; zeta = p[1]
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    J_arr, _ = _precompute_integrals(Om, Z_ARR)
    denom = 1.0 - zeta * J_arr
    if np.any(denom <= 0.05):
        # Divergence: clip zeta
        zeta = 0.9 / max(J_arr[-1], 1e-10)
        denom = 1.0 - zeta * J_arr
    arr = OL0 / np.maximum(denom, 0.01)
    return np.maximum(arr, 0.0)


# ---------------------------------------------------------------------------
# Phase 10: Topological defects
# ---------------------------------------------------------------------------

def make_T1(p):
    """T1: Kibble-Zurek power law.
    omega_de = OL0*(Om*(1+z)^3+OL0)^kappa [= OL0*E_LCDM_noR^{2*kappa}]
    At z=0: OL0*(Om+OL0)^kappa ~ OL0 for kappa=0. Normalized: use kappa as small."""
    Om = p[0]; kappa = p[1]
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    base = Om*(1+Z_ARR)**3 + OL0
    norm = (Om + OL0)**kappa
    arr = OL0 * base**kappa / max(norm, 1e-15)
    return np.maximum(arr, 0.0)

def make_T2(p):
    """T2: Defect network scaling (zero-parameter prediction).
    omega_de = OL0*sqrt(Om*(1+z)^3+OL0) = OL0*E_LCDM_noR(z).
    omega_de(0) = OL0*sqrt(Om+OL0) ~ OL0; normalized exactly if Om+OL0=1."""
    Om = p[0]
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    E_noR = np.sqrt(np.maximum(Om*(1+Z_ARR)**3 + OL0, 1e-15))
    E0_noR = max((Om + OL0)**0.5, 1e-15)
    arr = OL0 * E_noR / E0_noR  # normalize to OL0 at z=0
    return np.maximum(arr, 0.0)

def make_T3(p):
    """T3: Kosterlitz-Thouless logarithmic.
    omega_de = OL0*(1+nu*ln(1+Om*(1+z)^3/OL0))/(1+nu*ln(1+Om/OL0))"""
    Om = p[0]; nu = p[1]
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None
    ln_z = np.log1p(Om*(1+Z_ARR)**3 / max(OL0, 1e-10))
    ln_0 = np.log1p(Om / max(OL0, 1e-10))
    denom = max(1.0 + nu*ln_0, 1e-10)
    arr = OL0 * (1.0 + nu * ln_z) / denom
    return np.maximum(arr, 0.0)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print('=== L14 New-30 Theories vs DESI ===')
    print('Axioms A1+A2 only. All base.md equations discarded.')
    print('DESI DR2 7-bin diagonal chi2. H0=67.7 fixed.')
    print()

    results = {}

    s1 = [[Om] for Om in [0.290, 0.300, 0.310, 0.315, 0.320, 0.330]]
    s2 = [[Om, A] for Om in [0.295, 0.305, 0.315, 0.325]
                   for A in [-0.5, -0.1, 0.0, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]]
    s2_log = [[Om, nu] for Om in [0.295, 0.310, 0.325]
                        for nu in [-1.0, -0.5, 0.0, 0.1, 0.5, 1.0, 2.0, 5.0]]
    s3 = [[Om, a, b] for Om in [0.300, 0.315, 0.325]
                      for a in [0.0, 0.1, 0.5, 1.0]
                      for b in [0.0, 0.5, 1.0, 2.0]]
    s_kap = [[Om, k] for Om in [0.295, 0.310, 0.325]
                      for k in [-0.5, -0.2, 0.0, 0.1, 0.2, 0.5, 1.0]]
    s_nu = [[Om, nu] for Om in [0.295, 0.310, 0.325]
                      for nu in [-2.0, -0.5, -0.1, 0.0, 0.05, 0.1, 0.2, 0.5]]

    # References
    print('--- REFERENCES ---')
    p, c2, w0, wa, _ = fit_model(make_LCDM, 'LCDM     ', s1)
    results['LCDM']  = {'Om': p[0], 'chi2': c2, 'w0': w0, 'wa': wa}
    p, c2, w0, wa, _ = fit_model(make_A01, 'A01-B1   ', s1)
    results['A01']   = {'Om': p[0], 'chi2': c2, 'w0': w0, 'wa': wa}
    p, c2, w0, wa, _ = fit_model(make_C14, 'C14      ', s1)
    results['C14']   = {'Om': p[0], 'chi2': c2, 'w0': w0, 'wa': wa}

    # Phase 1: Diffusion
    print('--- PHASE 1: Diffusion ---')
    p, c2, w0, wa, _ = fit_model(make_D1, 'D1-Gauss ', s3)
    if p is not None: results['D1'] = {'Om':p[0],'A':p[1],'B':p[2],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_D2, 'D2-MFPT  ', s2)
    if p is not None: results['D2'] = {'Om':p[0],'A':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_D3, 'D3-Levy  ', s3)
    if p is not None: results['D3'] = {'Om':p[0],'A':p[1],'B':p[2],'chi2':c2,'w0':w0,'wa':wa}

    # Phase 2: Percolation
    print('--- PHASE 2: Percolation ---')
    p, c2, w0, wa, _ = fit_model(make_P1, 'P1-Giant ', s2)
    if p is not None: results['P1'] = {'Om':p[0],'f':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_P2, 'P2-CorrL ', s2_log)
    if p is not None: results['P2'] = {'Om':p[0],'nu':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_P3, 'P3-Bond  ', s2)
    if p is not None: results['P3'] = {'Om':p[0],'kap':p[1],'chi2':c2,'w0':w0,'wa':wa}

    # Phase 3: Ecology
    print('--- PHASE 3: Ecology ---')
    p, c2, w0, wa, _ = fit_model(make_E1, 'E1-LV    ', s2)
    if p is not None: results['E1'] = {'Om':p[0],'xi':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_E2, 'E2-Holling', s2)
    if p is not None: results['E2'] = {'Om':p[0],'phi':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_E3, 'E3-Allee ', s2)
    if p is not None: results['E3'] = {'Om':p[0],'zeta':p[1],'chi2':c2,'w0':w0,'wa':wa}

    # Phase 4: Reaction-Diffusion
    print('--- PHASE 4: Reaction-Diffusion ---')
    p, c2, w0, wa, _ = fit_model(make_R1, 'R1-GM    ', s2)
    if p is not None: results['R1'] = {'Om':p[0],'g':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_R2, 'R2-GS    ', s2)
    if p is not None: results['R2'] = {'Om':p[0],'lam':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_R3, 'R3-Thomas', s2)
    if p is not None: results['R3'] = {'Om':p[0],'g':p[1],'chi2':c2,'w0':w0,'wa':wa}

    # Phase 5: Phase Transition
    print('--- PHASE 5: Phase Transition ---')
    p, c2, w0, wa, _ = fit_model(make_L1, 'L1-Landau', s2)
    if p is not None: results['L1'] = {'Om':p[0],'f':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_L2, 'L2-1stOrd', s2)
    if p is not None: results['L2'] = {'Om':p[0],'f':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_L3, 'L3-RG    ', s_kap)
    if p is not None: results['L3'] = {'Om':p[0],'rho':p[1],'chi2':c2,'w0':w0,'wa':wa}

    # Phase 6: Information
    print('--- PHASE 6: Information ---')
    p, c2, w0, wa, _ = fit_model(make_I1, 'I1-Entang', s2)
    if p is not None: results['I1'] = {'Om':p[0],'beta':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_I2, 'I2-Discord', s_nu)
    if p is not None: results['I2'] = {'Om':p[0],'xi':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_I3, 'I3-Holevo', s_nu)
    if p is not None: results['I3'] = {'Om':p[0],'phi':p[1],'chi2':c2,'w0':w0,'wa':wa}

    # Phase 7: Gauge
    print('--- PHASE 7: Gauge ---')
    p, c2, w0, wa, _ = fit_model(make_G1, 'G1-MexHat', s2)
    if p is not None: results['G1'] = {'Om':p[0],'eta':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_G2, 'G2-NGB   ', s2)
    if p is not None: results['G2'] = {'Om':p[0],'delta':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_G3, 'G3-Higgs ', s2)
    if p is not None: results['G3'] = {'Om':p[0],'OH':p[1],'chi2':c2,'w0':w0,'wa':wa}

    # Phase 8: Automaton
    print('--- PHASE 8: Automaton ---')
    p, c2, w0, wa, _ = fit_model(make_CA1, 'CA1-MF   ', s2)
    if p is not None: results['CA1'] = {'Om':p[0],'A':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_CA2, 'CA2-R110 ', s2)
    if p is not None: results['CA2'] = {'Om':p[0],'mu':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_CA3, 'CA3-GoL  ', s2)
    if p is not None: results['CA3'] = {'Om':p[0],'OH':p[1],'chi2':c2,'w0':w0,'wa':wa}

    # Phase 9: Vortex
    print('--- PHASE 9: Vortex ---')
    p, c2, w0, wa, _ = fit_model(make_V1, 'V1-Turb  ', s2)
    if p is not None: results['V1'] = {'Om':p[0],'psi':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_V2, 'V2-Kelvin', s_nu)
    if p is not None: results['V2'] = {'Om':p[0],'nu':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_V3, 'V3-Reconn', s_nu)
    if p is not None: results['V3'] = {'Om':p[0],'zeta':p[1],'chi2':c2,'w0':w0,'wa':wa}

    # Phase 10: Topological
    print('--- PHASE 10: Topological ---')
    p, c2, w0, wa, _ = fit_model(make_T1, 'T1-KZ    ', s_kap)
    if p is not None: results['T1'] = {'Om':p[0],'kappa':p[1],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_T2, 'T2-Defect', s1)
    if p is not None: results['T2'] = {'Om':p[0],'chi2':c2,'w0':w0,'wa':wa}
    p, c2, w0, wa, _ = fit_model(make_T3, 'T3-KT    ', s2_log)
    if p is not None: results['T3'] = {'Om':p[0],'nu':p[1],'chi2':c2,'w0':w0,'wa':wa}

    # Summary
    chi2_lcdm = results.get('LCDM',{}).get('chi2', float('nan'))
    chi2_c14  = results.get('C14',{}).get('chi2', float('nan'))

    print()
    print('=== FULL SUMMARY ===')
    print('Kill:  chi2 >= LCDM (%.3f)' % chi2_lcdm)
    print('Pass:  chi2 < LCDM')
    print('Strong: chi2 < A01 (%.3f)' % results.get('A01',{}).get('chi2',float('nan')))
    print('Game-changer: chi2 < C14 (%.3f) AND wa < -0.5' % chi2_c14)
    print()

    passed = []
    killed = []
    fmt = '{:<12} chi2={:<8} dLCDM={:<8} w0={:<8} wa={:<8} STATUS'
    print(fmt.format('Model','chi2','dLCDM','w0','wa'))
    print('-'*72)
    for k, r in sorted(results.items(), key=lambda x: x[1].get('chi2',1e9)):
        c2v = r.get('chi2', float('nan'))
        dl  = round(c2v - chi2_lcdm, 3) if np.isfinite(chi2_lcdm) else float('nan')
        w0v = r.get('w0', float('nan'))
        wav = r.get('wa', float('nan'))
        if np.isfinite(c2v) and c2v < chi2_lcdm:
            status = 'PASS'
            if c2v < chi2_c14 and np.isfinite(wav) and wav < -0.5:
                status = 'GAME-CHANGER!'
            elif c2v < results.get('A01',{}).get('chi2',1e9):
                status = 'STRONG'
            passed.append(k)
        else:
            status = 'KILL'
            killed.append(k)
        print(fmt.format(k, round(c2v,3), dl,
                         round(w0v,3) if np.isfinite(w0v) else 'nan',
                         round(wav,3) if np.isfinite(wav) else 'nan') + '  ' + status)

    print()
    print('PASS count: %d / %d' % (len(passed), len(results)-3))
    print('PASS models: ' + str(passed))
    print('KILL models: ' + str(killed))

    print()
    print('wa gap to DESI -0.83:')
    for k in sorted(results.keys(), key=lambda x: results[x].get('chi2',1e9)):
        r = results[k]
        if r.get('chi2', 1e9) < chi2_lcdm:
            wav = r.get('wa', float('nan'))
            if np.isfinite(wav):
                gap = round(-0.83-wav, 3)
                pct = round(100*abs(gap)/0.83, 1)
                print('  %s: wa=%.3f  gap=%.3f  (%s%% remaining)' % (k, wav, gap, pct))

    # Save
    out = os.path.join(_THIS, 'l14_new30_results.json')
    def _j(v):
        if isinstance(v, (np.floating, np.integer)):
            return float(v)
        if isinstance(v, float) and not np.isfinite(v):
            return None
        return v
    clean = {k: {rk: _j(rv) for rk, rv in r.items()} for k, r in results.items()}
    with open(out, 'w') as f:
        json.dump(clean, f, indent=2)
    print()
    print('Saved: ' + out)
    return results


if __name__ == '__main__':
    main()
