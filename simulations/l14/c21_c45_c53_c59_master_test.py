# -*- coding: utf-8 -*-
"""
L14-C2: C21, C45, C53, C59, Master-form DESI Test

C21:  dn/dt + 4H*n = Gamma_0 - 2*sigma_eff*n*rho_m      [4H + 2x annihilation]
      ODE: du/dz = (-4*u - 2*A*Om*(1+z)^3*u/E + (4+2*A*Om)*OL0/E) / (1+z)
      Params: Om, A_21  [A=effective coupling amplitude]

C45:  dn/dt + 3H*n = Gamma_0 - sigma*(1+z)*n*rho_m       [redshift-boosted annihilation]
      ODE: du/dz = (-3*u - A*Om*(1+z)^4*u/E + (3+A*Om)*OL0/E) / (1+z)
      Params: Om, A_45

C53:  dn/dt + 3H*n = Gamma_0 - sigma*exp(-s8^2/(1+z)^2)*n*rho_m  [void topology]
      sigma_8 = 0.8 => s8^2 = 0.64
      ODE: du/dz = (-3*u - A*Om*(1+z)^3*exp(-0.64/(1+z)^2)*u/E + (3+A*Om*f0_53)*OL0/E) / (1+z)
      f0_53 = exp(-0.64)  [coupling at z=0]
      Params: Om, A_53

C59:  dn/dt + 3H*n = Gamma_0 - sigma*(1+z)^0.5*exp(-s8^2/(1+z)^2)*n*rho_m  [void+velocity]
      ODE: du/dz = (-3*u - A*Om*(1+z)^3.5*exp(-0.64/(1+z)^2)*u/E + (3+A*Om*f0_59)*OL0/E) / (1+z)
      f0_59 = exp(-0.64)  [coupling at z=0, (1+z)^0.5=1]
      Params: Om, A_59

Master: sigma_eff = sigma*(1 + B*(1+z))  [structural convergence of C45/C48/C60]
      ODE: du/dz = (-3*u - A*(1+B*(1+z))*Om*(1+z)^3*u/E + (3+A*(1+B)*Om)*OL0/E) / (1+z)
      A = overall amplitude (z=0 coupling), B = (1+z) growth slope
      Params: Om, A_M, B_M  [3 params total]

CLAUDE.md rules:
  - No unicode in print()
  - numpy 2.x: trapezoid
  - h fixed at 0.677 (H0=67.7 km/s/Mpc)
  - 7-bin diagonal chi2, DESI DR2
  - odeint for ODEs
  - Om in [0.28, 0.36]
"""
from __future__ import annotations
import os
import json
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize, curve_fit
from scipy.interpolate import interp1d

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
np.seterr(all='ignore')

_THIS = os.path.dirname(os.path.abspath(__file__))

# Constants
c_SI    = 2.998e8
Mpc_m   = 3.086e22
OMEGA_R = 9.1e-5
rs_drag = 147.09       # Mpc
H0_KMS  = 67.7
H0_SI   = H0_KMS * 1e3 / Mpc_m

# DESI DR2 7-bin diagonal
DESI_Z   = np.array([0.295, 0.510, 0.706, 0.930, 1.317, 1.491, 2.330])
DESI_OBS = np.array([7.93, 13.62, 16.85, 21.71, 27.79, 30.21, 39.71])
DESI_ERR = np.array([0.15,  0.17,  0.22,  0.22,  0.55,  0.49,  0.94])

N_Z  = 3000
Z_MAX = 6.0
Z_ARR = np.linspace(0.0, Z_MAX, N_Z)

# Precompute for C53/C59 normalization
S8_SQ  = 0.64   # sigma_8 = 0.8
F0_53  = float(np.exp(-S8_SQ))            # exp(-0.64) ~ 0.5273
F0_59  = float(np.exp(-S8_SQ))            # (1+z)^0.5 at z=0 is 1, so same as C53


# ---------------------------------------------------------------------------
# Distance calculation helpers
# ---------------------------------------------------------------------------

def chi2_from_ode(z_arr, ode_arr, Om):
    """Compute 7-bin diagonal chi2 given omega_de(z) array on z_arr."""
    E2 = OMEGA_R*(1+z_arr)**4 + Om*(1+z_arr)**3 + np.maximum(ode_arr, 0)
    E_arr = np.sqrt(np.maximum(E2, 1e-15))
    E_interp = interp1d(z_arr, E_arr, kind='cubic',
                        fill_value='extrapolate', bounds_error=False)

    z_int = np.linspace(0, Z_MAX*0.99, 5000)
    inv_E = 1.0/np.maximum(E_interp(z_int), 1e-10)
    dz    = np.diff(z_int)
    cum   = np.zeros(len(z_int))
    for i in range(1, len(z_int)):
        cum[i] = cum[i-1] + 0.5*(inv_E[i-1]+inv_E[i])*dz[i-1]
    chi_func = interp1d(z_int, cum, kind='cubic',
                        fill_value='extrapolate', bounds_error=False)

    fac = c_SI/(H0_SI*Mpc_m)

    pred = np.zeros(7)
    DM0 = fac * chi_func(DESI_Z[0])
    DH0 = fac / E_interp(DESI_Z[0])
    DV0 = (DESI_Z[0] * DM0**2 * DH0)**(1.0/3.0)
    pred[0] = DV0 / rs_drag
    for k, z in enumerate(DESI_Z[1:], 1):
        pred[k] = fac * chi_func(z) / rs_drag

    resid = pred - DESI_OBS
    c2 = float(np.sum((resid/DESI_ERR)**2))
    return c2 if np.isfinite(c2) and c2 < 1e8 else 1e8


def fit_cpl(z_arr, ode_arr):
    """Fit CPL w0, wa from omega_de(z) array."""
    z_fit = np.linspace(0.01, 1.5, 300)
    dz = 1e-4
    ode_i = interp1d(z_arr, ode_arr, kind='cubic',
                     fill_value='extrapolate', bounds_error=False)
    u   = np.array([float(ode_i(z)) for z in z_fit])
    u_p = np.array([float(ode_i(z+dz)) for z in z_fit])
    u_m = np.array([float(ode_i(max(z-dz, 1e-5))) for z in z_fit])
    dlnu = (u_p - u_m)/(2*dz*np.maximum(u, 1e-20))
    w_z  = (1+z_fit)*dlnu/3.0 - 1.0

    def w_cpl(z, w0, wa):
        return w0 + wa*(1 - 1/(1+z))

    try:
        popt, _ = curve_fit(w_cpl, z_fit, w_z, p0=[-0.95, -0.2],
                            bounds=([-3.0, -10.0], [0.5, 5.0]), maxfev=5000)
        return float(popt[0]), float(popt[1])
    except Exception:
        return float('nan'), float('nan')


def fit_params(make_ode_func, label, starts):
    """Fit parameters to minimize chi2. starts is list of initial guesses."""
    best = (1e9, None)
    for p0 in starts:
        def obj(p):
            Om = p[0]
            if Om < 0.28 or Om > 0.36:
                return 1e8
            try:
                ode_arr = make_ode_func(p)
                if ode_arr is None:
                    return 1e8
                return chi2_from_ode(Z_ARR, ode_arr, Om)
            except Exception:
                return 1e8
        res = minimize(obj, p0, method='Nelder-Mead',
                       options={'xatol': 1e-5, 'fatol': 0.01, 'maxiter': 8000})
        if res.fun < best[0]:
            best = (res.fun, list(res.x))

    if best[1] is None:
        print(label + '  FAILED (all starts failed)')
        return None, 1e8, float('nan'), float('nan'), None

    p_best, chi2_best = best[1], best[0]
    ode_arr = make_ode_func(p_best)
    if ode_arr is None:
        print(label + '  FAILED (ode_arr is None at best params)')
        return p_best, chi2_best, float('nan'), float('nan'), None

    w0, wa = fit_cpl(Z_ARR, ode_arr)
    print(label + '  params=' + str([round(x, 4) for x in p_best]) +
          '  chi2=' + str(round(chi2_best, 3)) +
          '  w0=' + str(round(w0, 3)) + '  wa=' + str(round(wa, 3)))
    return p_best, chi2_best, w0, wa, ode_arr


# ---------------------------------------------------------------------------
# LCDM baseline
# ---------------------------------------------------------------------------

def make_ode_LCDM(p):
    Om = p[0]
    OL0 = 1.0 - Om - OMEGA_R
    return np.full(len(Z_ARR), OL0)


# ---------------------------------------------------------------------------
# B1 (A01 baseline)
# ---------------------------------------------------------------------------

def make_ode_B1(p):
    Om = p[0]
    OL0 = 1.0 - Om - OMEGA_R
    a = 1.0/(1.0 + Z_ARR)
    return OL0*(1.0 + Om*(1.0 - a))


# ---------------------------------------------------------------------------
# C1 (reference: 4H, 0 params) -- from previous test, chi2=14.084
# ODE: du/dz = (-4*u + 4*OL0/E) / (1+z)
# ---------------------------------------------------------------------------

def make_ode_C1(p):
    Om = p[0]
    OL0 = 1.0 - Om - OMEGA_R
    c = 4.0  # 3*(1+w_sq) with w_sq=1/3

    def rhs(state, z):
        u  = max(state[0], 1e-15)
        E2 = OMEGA_R*(1+z)**4 + Om*(1+z)**3 + u
        E  = max(E2**0.5, 1e-10)
        du = (-c*u + c*OL0/E) / (1.0 + z)
        return [du]

    sol = odeint(rhs, [OL0], Z_ARR, rtol=1e-10, atol=1e-12, mxstep=20000)
    return np.maximum(sol[:, 0], 0.0)


# ---------------------------------------------------------------------------
# C14 (reference: 2x sigma phenom, 0 params) -- chi2=11.277
# ---------------------------------------------------------------------------

def make_ode_C14(p):
    Om = p[0]
    OL0 = 1.0 - Om - OMEGA_R
    a = 1.0/(1.0 + Z_ARR)
    return OL0*(1.0 + 2.0*Om*(1.0 - a))


# ---------------------------------------------------------------------------
# C21: 4H + 2*sigma_eff annihilation
# ODE: du/dz = (-4*u - 2*A*Om*(1+z)^3*u/E + (4+2*A*Om)*OL0/E) / (1+z)
# Normalization: at z=0 equilibrium, du/dz=0:
#   -4*OL0 - 2*A*Om*OL0/1 + (4+2*A*Om)*OL0 = 0  [CHECK: exact cancellation, correct]
# Params: Om, A_21
# ---------------------------------------------------------------------------

def _solve_C21(Om, A):
    """4H expansion + 2*A*sigma_eff matter annihilation."""
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None

    def rhs(state, z):
        u  = max(state[0], 1e-15)
        E2 = OMEGA_R*(1+z)**4 + Om*(1+z)**3 + u
        E  = max(E2**0.5, 1e-10)
        sink   = 2.0*A*Om*(1+z)**3 * u / E
        source = (4.0 + 2.0*A*Om) * OL0 / E
        du = (-4.0*u - sink + source) / (1.0 + z)
        return [du]

    sol = odeint(rhs, [OL0], Z_ARR, rtol=1e-10, atol=1e-12, mxstep=20000)
    return np.maximum(sol[:, 0], 0.0)


def make_ode_C21(p):
    Om = p[0]
    A  = max(p[1], 0.0)
    return _solve_C21(Om, A)


# ---------------------------------------------------------------------------
# C45: 3H + sigma*(1+z)*rho_m annihilation
# Physical: thermal velocity v ~ sqrt(T) ~ (1+z)^0.5, but annihilation cross
#   section * velocity ~ (1+z) from redshift (v_rel grows as (1+z)).
# ODE: du/dz = (-3*u - A*Om*(1+z)^4*u/E + (3+A*Om)*OL0/E) / (1+z)
# Normalization: A*Om*(1+z)^3*(1+z)|_{z=0} = A*Om at z=0 -> source = (3+A*Om)*OL0
# Params: Om, A_45
# ---------------------------------------------------------------------------

def _solve_C45(Om, A):
    """3H + sigma*(1+z) matter annihilation."""
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None

    def rhs(state, z):
        u  = max(state[0], 1e-15)
        zp = 1.0 + z
        E2 = OMEGA_R*zp**4 + Om*zp**3 + u
        E  = max(E2**0.5, 1e-10)
        sink   = A * Om * zp**4 * u / E      # (1+z)^3 from rho_m, (1+z) from coupling
        source = (3.0 + A*Om) * OL0 / E      # normalized so u(0)=OL0
        du = (-3.0*u - sink + source) / zp
        return [du]

    sol = odeint(rhs, [OL0], Z_ARR, rtol=1e-10, atol=1e-12, mxstep=20000)
    return np.maximum(sol[:, 0], 0.0)


def make_ode_C45(p):
    Om = p[0]
    A  = max(p[1], 0.0)
    return _solve_C45(Om, A)


# ---------------------------------------------------------------------------
# C53: 3H + sigma*exp(-sigma8^2/(1+z)^2)*rho_m annihilation
# Physical: void-biased quanta, annihilation suppressed in voids by topology.
# sigma_8 = 0.8, so s8^2 = 0.64
# f(z) = exp(-0.64/(1+z)^2); f(0) = exp(-0.64) ~ 0.5273
# ODE: du/dz = (-3*u - A*Om*(1+z)^3*f(z)*u/E + (3+A*Om*f(0))*OL0/E) / (1+z)
# Params: Om, A_53
# ---------------------------------------------------------------------------

def _solve_C53(Om, A):
    """3H + sigma*exp(-s8^2/(1+z)^2) matter annihilation [void topology]."""
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None

    def rhs(state, z):
        u  = max(state[0], 1e-15)
        zp = 1.0 + z
        E2 = OMEGA_R*zp**4 + Om*zp**3 + u
        E  = max(E2**0.5, 1e-10)
        fz     = np.exp(-S8_SQ / zp**2)
        sink   = A * Om * zp**3 * fz * u / E
        source = (3.0 + A*Om*F0_53) * OL0 / E
        du = (-3.0*u - sink + source) / zp
        return [du]

    sol = odeint(rhs, [OL0], Z_ARR, rtol=1e-10, atol=1e-12, mxstep=20000)
    return np.maximum(sol[:, 0], 0.0)


def make_ode_C53(p):
    Om = p[0]
    A  = max(p[1], 0.0)
    return _solve_C53(Om, A)


# ---------------------------------------------------------------------------
# C59: 3H + sigma*(1+z)^0.5*exp(-s8^2/(1+z)^2)*rho_m annihilation
# Physical: void topology + thermal velocity
# f(z) = (1+z)^0.5 * exp(-0.64/(1+z)^2); f(0) = exp(-0.64) ~ 0.5273
# ODE: du/dz = (-3*u - A*Om*(1+z)^3.5*exp(-0.64/(1+z)^2)*u/E + (3+A*Om*f(0))*OL0/E) / (1+z)
# Params: Om, A_59
# ---------------------------------------------------------------------------

def _solve_C59(Om, A):
    """3H + sigma*(1+z)^0.5*exp(-s8^2/(1+z)^2) annihilation [void+velocity]."""
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None

    def rhs(state, z):
        u  = max(state[0], 1e-15)
        zp = 1.0 + z
        E2 = OMEGA_R*zp**4 + Om*zp**3 + u
        E  = max(E2**0.5, 1e-10)
        fz     = zp**0.5 * np.exp(-S8_SQ / zp**2)
        sink   = A * Om * zp**3 * fz * u / E
        source = (3.0 + A*Om*F0_59) * OL0 / E   # F0_59 = f(z=0) = exp(-0.64)
        du = (-3.0*u - sink + source) / zp
        return [du]

    sol = odeint(rhs, [OL0], Z_ARR, rtol=1e-10, atol=1e-12, mxstep=20000)
    return np.maximum(sol[:, 0], 0.0)


def make_ode_C59(p):
    Om = p[0]
    A  = max(p[1], 0.0)
    return _solve_C59(Om, A)


# ---------------------------------------------------------------------------
# Master: sigma_eff = sigma*(1 + B*(1+z))  -- structural convergence
# ODE: du/dz = (-3*u - A*(1+B*(1+z))*Om*(1+z)^3*u/E + (3+A*(1+B)*Om)*OL0/E) / (1+z)
# A = overall coupling amplitude, B = (1+z) growth coefficient
# Params: Om, A_M, B_M
# ---------------------------------------------------------------------------

def _solve_master(Om, A, B):
    """3H + A*(1+B*(1+z))*rho_m annihilation [structural convergence form]."""
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01:
        return None

    # Normalization: at z=0, sink = A*(1+B)*Om*OL0/E0
    # source must match: (3 + A*(1+B)*Om)*OL0/E(z)
    src_coeff = 3.0 + A*(1.0 + B)*Om

    def rhs(state, z):
        u  = max(state[0], 1e-15)
        zp = 1.0 + z
        E2 = OMEGA_R*zp**4 + Om*zp**3 + u
        E  = max(E2**0.5, 1e-10)
        coupling = A * (1.0 + B*zp)
        sink     = coupling * Om * zp**3 * u / E
        source   = src_coeff * OL0 / E
        du = (-3.0*u - sink + source) / zp
        return [du]

    sol = odeint(rhs, [OL0], Z_ARR, rtol=1e-10, atol=1e-12, mxstep=20000)
    return np.maximum(sol[:, 0], 0.0)


def make_ode_master(p):
    Om = p[0]
    A  = max(p[1], 0.0)
    B  = max(p[2], 0.0)
    return _solve_master(Om, A, B)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print('=== L14-C2: C21/C45/C53/C59/Master vs DESI ===')
    print('DESI DR2 7-bin diagonal chi2.  H0=67.7 km/s/Mpc fixed.')
    print('DESI target: w0=-0.757  wa=-0.83')
    print()

    results = {}

    # Common starts for 1-param (Om only)
    s1 = [[Om] for Om in [0.290, 0.300, 0.310, 0.315, 0.320, 0.330]]

    # 2-param starts: Om, A
    s2 = [[Om, A] for Om in [0.295, 0.305, 0.315, 0.325]
                   for A in [0.0, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0]]

    # 3-param starts: Om, A, B
    s3 = [[Om, A, B] for Om in [0.300, 0.315, 0.325]
                      for A in [0.5, 1.0, 2.0, 5.0]
                      for B in [0.0, 0.5, 1.0, 2.0]]

    # --- LCDM reference ---
    p, c2, w0, wa, ode = fit_params(make_ode_LCDM, 'LCDM    ', s1)
    results['LCDM']   = {'Om': p[0], 'chi2': c2, 'w0': w0, 'wa': wa}

    # --- B1 reference ---
    p, c2, w0, wa, ode = fit_params(make_ode_B1, 'B1-A01  ', s1)
    results['B1_A01'] = {'Om': p[0], 'chi2': c2, 'w0': w0, 'wa': wa}

    # --- C1 reference (0 params, already tested) ---
    p, c2, w0, wa, ode = fit_params(make_ode_C1, 'C1-ref  ', s1)
    results['C1_ref'] = {'Om': p[0], 'chi2': c2, 'w0': w0, 'wa': wa}

    # --- C14 reference (0 params, already tested) ---
    p, c2, w0, wa, ode = fit_params(make_ode_C14, 'C14-ref ', s1)
    results['C14_ref'] = {'Om': p[0], 'chi2': c2, 'w0': w0, 'wa': wa}

    # --- C21: 4H + 2*sigma_eff (2 params) ---
    p, c2, w0, wa, ode = fit_params(make_ode_C21, 'C21-4H2s', s2)
    if p is not None:
        results['C21'] = {'Om': p[0], 'A': p[1], 'chi2': c2, 'w0': w0, 'wa': wa}

    # --- C45: sigma*(1+z) (2 params) ---
    p, c2, w0, wa, ode = fit_params(make_ode_C45, 'C45-1+z ', s2)
    if p is not None:
        results['C45'] = {'Om': p[0], 'A': p[1], 'chi2': c2, 'w0': w0, 'wa': wa}

    # --- C53: sigma*exp(-s8^2/(1+z)^2) [void] (2 params) ---
    p, c2, w0, wa, ode = fit_params(make_ode_C53, 'C53-void', s2)
    if p is not None:
        results['C53'] = {'Om': p[0], 'A': p[1], 'chi2': c2, 'w0': w0, 'wa': wa}

    # --- C59: sigma*(1+z)^0.5*exp(-s8^2/(1+z)^2) [void+v] (2 params) ---
    p, c2, w0, wa, ode = fit_params(make_ode_C59, 'C59-vv  ', s2)
    if p is not None:
        results['C59'] = {'Om': p[0], 'A': p[1], 'chi2': c2, 'w0': w0, 'wa': wa}

    # --- Master: sigma*(1+B*(1+z)) (3 params) ---
    p, c2, w0, wa, ode = fit_params(make_ode_master, 'Master  ', s3)
    if p is not None:
        results['Master'] = {'Om': p[0], 'A': p[1], 'B': p[2], 'chi2': c2, 'w0': w0, 'wa': wa}

    # Summary
    print()
    print('=== SUMMARY ===')
    print('DESI target: w0=-0.757  wa=-0.83')
    print()
    chi2_lcdm = results.get('LCDM', {}).get('chi2', float('nan'))
    chi2_b1   = results.get('B1_A01', {}).get('chi2', float('nan'))
    chi2_c14  = results.get('C14_ref', {}).get('chi2', float('nan'))
    fmt = '{:<12} chi2={:<8} dLCDM={:<8} dC14={:<7} w0={:<8} wa={:<7}'
    print(fmt.format('Model', 'chi2', 'dLCDM', 'dC14', 'w0', 'wa'))
    print('-'*65)
    for k, r in results.items():
        c2v = r.get('chi2', float('nan'))
        dl  = round(c2v - chi2_lcdm, 3) if np.isfinite(chi2_lcdm) else float('nan')
        dc  = round(c2v - chi2_c14, 3) if np.isfinite(chi2_c14) else float('nan')
        print(fmt.format(k, round(c2v, 3), dl, dc,
                         round(r.get('w0', float('nan')), 3),
                         round(r.get('wa', float('nan')), 3)))

    print()
    print('wa gap to DESI (-0.83):')
    for k, r in results.items():
        wa = r.get('wa', float('nan'))
        if not np.isnan(wa):
            gap = round(-0.83 - wa, 3)
            pct = round(100.0*abs(gap)/0.83, 1)
            print('  ' + k + ': wa=' + str(round(wa, 3)) +
                  '  gap=' + str(gap) + '  (' + str(pct) + '% remaining)')
        else:
            print('  ' + k + ': wa=nan')

    print()
    print('Extra params per model:')
    print('  LCDM/B1/C1_ref/C14_ref: 1 param (Om only)')
    print('  C21/C45/C53/C59: 2 params (Om, A)')
    print('  Master: 3 params (Om, A, B)')

    # Save
    out = os.path.join(_THIS, 'c21_c45_c53_c59_master_results.json')
    with open(out, 'w') as f:
        # Convert to JSON-serializable
        def _j(v):
            if isinstance(v, float) and not np.isfinite(v):
                return None
            if isinstance(v, (np.floating, np.integer)):
                return float(v)
            return v
        clean = {}
        for k, r in results.items():
            clean[k] = {rk: _j(rv) for rk, rv in r.items()}
        json.dump(clean, f, indent=2)
    print()
    print('Saved: ' + out)
    return results


if __name__ == '__main__':
    main()
