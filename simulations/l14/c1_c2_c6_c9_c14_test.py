# -*- coding: utf-8 -*-
"""
L14-C: Structural Alternative Equations DESI Test (C1, C2, C6, C9, C14)

C1:  dn/dt + 4H*n = Gamma_0 - sigma*n*rho_m          [H2: w_sq=1/3]
     ODE: d(omega_de)/dz = (-4*omega_de + 4*OL0/E(z)) / (1+z)

C2:  dn/dt + 3*(1+w)*H*n = Gamma_0 - sigma*n*rho_m   [H2: general w_sq, scan]
     ODE: d(omega_de)/dz = (-3(1+w)*omega_de + 3(1+w)*OL0/E(z)) / (1+z)

C6:  dn/dt + 3Hn = Gamma_0 - sigma*n*rho_m - sigma_r*n*rho_r  [H7: radiation coupling]
     ODE: d(omega_de)/dz = (-3*omega_de + 3*OL0/E - eta_r*(1+z)^4*omega_de/E) / (1+z)
     eta_r = sigma_r/sigma (free parameter, ratio of radiation to matter coupling)

C9:  dn/dt + 3Hn = beta_PZ*(H_dot+2H^2) - sigma*n*rho_m       [H5: Parker-PZ Gamma_0]
     Gamma_0(z) = c_PZ * R(z) where R = 6*(H_dot+2H^2) = Ricci scalar
     ODE: d(omega_de)/dz = (-3*omega_de + c_PZ*6*(Hdot+2H^2)/(H0*E*(1+z))) / (1+z)
     Normalization: c_PZ set so omega_de(0)=OL0 condition is satisfied.

C14: Weyl sigma = 2*sigma (GR vs Newtonian matching)            [H6: sigma doubled]
     Phenomenological: omega_de_C14 = OL0*(1 + 2*Om*(1-a))
     (A01-analog with doubled matter-coupling amplitude)

CLAUDE.md rules:
  - No unicode in print()
  - numpy 2.x: trapezoid
  - h fixed at 0.677 (H0=67.7 km/s/Mpc)
  - 7-bin diagonal chi2, DESI DR2
  - odeint for ODEs
  - tight bounds Om in [0.25, 0.40]
"""
from __future__ import annotations
import os
import json
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize, curve_fit, brentq
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


# ---------------------------------------------------------------------------
# Distance calculation helpers
# ---------------------------------------------------------------------------

def chi2_from_ode(z_arr, ode_arr, Om):
    """Compute 7-bin diagonal chi2 given omega_de(z) array on z_arr."""
    E2 = OMEGA_R*(1+z_arr)**4 + Om*(1+z_arr)**3 + np.maximum(ode_arr, 0)
    E_arr = np.sqrt(np.maximum(E2, 1e-15))
    E_interp = interp1d(z_arr, E_arr, kind='cubic',
                        fill_value='extrapolate', bounds_error=False)

    # Comoving distance
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
    # DV/rs at z[0]=0.295
    DM0 = fac * chi_func(DESI_Z[0])
    DH0 = fac / E_interp(DESI_Z[0])
    DV0 = (DESI_Z[0] * DM0**2 * DH0)**(1.0/3.0)
    pred[0] = DV0 / rs_drag
    # DM/rs for rest
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


def fit_Om(make_ode_func, label, starts=None):
    """Fit Om (and possibly one extra param) to minimize chi2."""
    if starts is None:
        starts = [[0.290],[0.300],[0.310],[0.315],[0.320],[0.330]]
    best = (1e9, None)
    for p0 in starts:
        def obj(p):
            Om = p[0]
            if Om < 0.24 or Om > 0.42:
                return 1e8
            try:
                ode_arr = make_ode_func(p)
                if ode_arr is None:
                    return 1e8
                return chi2_from_ode(Z_ARR, ode_arr, Om)
            except Exception:
                return 1e8
        res = minimize(obj, p0, method='Nelder-Mead',
                       options={'xatol': 1e-5, 'fatol': 0.01, 'maxiter': 5000})
        if res.fun < best[0]:
            best = (res.fun, list(res.x))
    p_best, chi2_best = best[1], best[0]
    ode_arr = make_ode_func(p_best)
    w0, wa  = fit_cpl(Z_ARR, ode_arr)
    print(label + '  params=' + str([round(x,4) for x in p_best]) +
          '  chi2=' + str(round(chi2_best,3)) +
          '  w0=' + str(round(w0,3)) + '  wa=' + str(round(wa,3)))
    return p_best, chi2_best, w0, wa, ode_arr


# ---------------------------------------------------------------------------
# B1 (A01 baseline)
# ---------------------------------------------------------------------------

def make_ode_B1(p):
    Om = p[0]
    OL0 = 1.0 - Om - OMEGA_R
    a = 1.0/(1.0+Z_ARR)
    return OL0*(1.0 + Om*(1.0 - a))


# ---------------------------------------------------------------------------
# C1: w_sq = 1/3  =>  coefficient 4H instead of 3H
# ODE: d(omega_de)/dz = (-4*u + 4*OL0/E) / (1+z)
# Gamma_0 normalization: Gamma_0_eff = 4*OL0*H0 (from equilibrium at z=0)
# ---------------------------------------------------------------------------

def _solve_C_wsq(Om, w_sq, z_arr=None):
    """
    Solve ODE for general w_sq:
    d(u)/dz = (-3(1+w)*u + 3(1+w)*OL0/E) / (1+z)
    """
    if z_arr is None:
        z_arr = Z_ARR
    OL0 = 1.0 - Om - OMEGA_R
    c   = 3.0*(1.0 + w_sq)

    def rhs(state, z):
        u = max(state[0], 1e-15)
        E2 = OMEGA_R*(1+z)**4 + Om*(1+z)**3 + u
        E  = max(E2**0.5, 1e-10)
        du = (-c*u + c*OL0/E) / (1.0 + z)
        return [du]

    sol = odeint(rhs, [OL0], z_arr, rtol=1e-10, atol=1e-12, mxstep=20000)
    return np.maximum(sol[:,0], 0.0)


def make_ode_C1(p):
    Om = p[0]
    return _solve_C_wsq(Om, 1.0/3.0)


def make_ode_C2_wsq(p):
    Om, w_sq = p[0], max(min(p[1], 1.0/3.0), 0.0)
    return _solve_C_wsq(Om, w_sq)


# ---------------------------------------------------------------------------
# C6: Radiation coupling
# ODE: d(u)/dz = (-3*u + 3*OL0/E - eta_r*OMEGA_R*(1+z)^4*u/E) / (1+z)
# eta_r >= 0 is a free parameter (radiation coupling strength relative to Gamma0)
# ---------------------------------------------------------------------------

def _solve_C6(Om, eta_r):
    OL0 = 1.0 - Om - OMEGA_R

    def rhs(state, z):
        u = max(state[0], 1e-15)
        Or = OMEGA_R*(1+z)**4
        E2 = Or + Om*(1+z)**3 + u
        E  = max(E2**0.5, 1e-10)
        rad_sink = eta_r * Or * u / E
        du = (-3.0*u + 3.0*OL0/E - rad_sink) / (1.0 + z)
        return [du]

    sol = odeint(rhs, [OL0], Z_ARR, rtol=1e-10, atol=1e-12, mxstep=20000)
    return np.maximum(sol[:,0], 0.0)


def make_ode_C6(p):
    Om, eta_r = p[0], max(p[1], 0.0)
    return _solve_C6(Om, eta_r)


# ---------------------------------------------------------------------------
# C9: Parker-Zel'dovich  Gamma_0 proportional to Ricci scalar R
# R = 6*(H_dot + 2*H^2)
# In FLRW: H_dot = -H*(1+z)*dH/dz  =>  H_dot/H^2 = -(1+z)/E * dE/dz
# H_dot + 2H^2 = H0^2 * E * (-(1+z)*dE/dz + 2*E)
#              = H0^2 * (2E^2 - (1+z)*E*dE/dz)
# dE/dz = (2*OMEGA_R*(1+z)^3 + 1.5*Om*(1+z)^2 + d(omega_de)/dz) / (2E)
#       ~ (2*OMEGA_R*(1+z)^3 + 1.5*Om*(1+z)^2) / (2E)   [LCDM background]
#
# At z=0: H_dot+2H^2 = H0^2*(2 - 1.5*Om - 2*OMEGA_R)  ~  H0^2*(2 - 0.46) ~ 1.54*H0^2
#
# Gamma_0_PZ = c_PZ * R = 6*c_PZ * (H_dot+2H^2)
# ODE: d(u)/dz = (-3*u + c_PZ*R(z)/H0^2 / E) / (1+z)
# Normalization: c_PZ set so that u(0) = OL0 (fixed point condition)
#   At z=0 equilibrium: -3*u + c_PZ*R0/H0^2 / E0 = 0  =>  c_PZ = 3*OL0*E0*H0^2/R0
#   R0 = 6*(2 - 1.5*Om*(1-OMEGA_R) - ...) ... compute numerically
# ---------------------------------------------------------------------------

def _compute_R_z(Om, z_arr=None):
    """
    Compute R(z)/H0^2 = 6*(H_dot+2H^2)/H0^2 = 6*(2E^2 - (1+z)*E*dE/dz)
    using LCDM background (omega_de = OL0 = const).
    """
    if z_arr is None:
        z_arr = Z_ARR
    OL0 = 1.0 - Om - OMEGA_R
    E2  = OMEGA_R*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    E   = np.sqrt(np.maximum(E2, 1e-15))
    # dE/dz from LCDM (no omega_de evolution)
    dE_dz = (2*OMEGA_R*(1+z_arr)**3 + 1.5*Om*(1+z_arr)**2) / (2.0*E)
    R_over_H02 = 6.0*(2.0*E2 - (1+z_arr)*E*dE_dz)
    return R_over_H02


def _solve_C9(Om):
    OL0 = 1.0 - Om - OMEGA_R
    R_z = _compute_R_z(Om)  # shape (N_Z,)
    R_interp = interp1d(Z_ARR, R_z, kind='cubic',
                        fill_value='extrapolate', bounds_error=False)

    # Normalization: at z=0, d(u)/dz = 0 => c_PZ = 3*OL0 / (R0/H02 / E0)
    E0  = np.sqrt(OMEGA_R + Om + OL0)
    R0  = float(R_interp(0.0))
    if abs(R0) < 1e-10:
        return None
    c_PZ = 3.0 * OL0 * E0 / R0   # dimensionless

    def rhs(state, z):
        u  = max(state[0], 1e-15)
        E2 = OMEGA_R*(1+z)**4 + Om*(1+z)**3 + u
        E  = max(E2**0.5, 1e-10)
        Rz = float(R_interp(z))
        gamma_eff = c_PZ * Rz / E    # Gamma_0_PZ / (H0 * (1+z))
        du = (-3.0*u + gamma_eff) / (1.0 + z)
        return [du]

    sol = odeint(rhs, [OL0], Z_ARR, rtol=1e-10, atol=1e-12, mxstep=20000)
    return np.maximum(sol[:,0], 0.0)


def make_ode_C9(p):
    Om = p[0]
    return _solve_C9(Om)


# ---------------------------------------------------------------------------
# C14: sigma -> 2*sigma (Weyl / GR vs Newtonian)
# Phenomenological analog: omega_de = OL0*(1 + 2*Om*(1-a))
# (Doubled matter-coupling amplitude in A01-like form)
# ---------------------------------------------------------------------------

def make_ode_C14(p):
    Om = p[0]
    OL0 = 1.0 - Om - OMEGA_R
    a = 1.0/(1.0+Z_ARR)
    return OL0*(1.0 + 2.0*Om*(1.0 - a))


# ---------------------------------------------------------------------------
# LCDM baseline
# ---------------------------------------------------------------------------

def make_ode_LCDM(p):
    Om = p[0]
    OL0 = 1.0 - Om - OMEGA_R
    return np.full(len(Z_ARR), OL0)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print('=== L14-C: Structural Alternative Equations vs DESI ===')
    print('DESI DR2 7-bin diagonal chi2.  H0=67.7 km/s/Mpc fixed.')
    print()

    results = {}
    starts_1 = [[0.290],[0.300],[0.310],[0.315],[0.320],[0.330]]
    starts_2 = [[Om, x] for Om in [0.295,0.305,0.315,0.325]
                         for x in [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.30, 0.33]]
    starts_C6 = [[Om, eta] for Om in [0.295,0.310,0.325]
                            for eta in [0.0, 0.1, 0.5, 1.0, 2.0, 5.0]]

    # LCDM
    p, c2, w0, wa, ode = fit_Om(make_ode_LCDM, 'LCDM   ', starts_1)
    results['LCDM']   = {'Om':p[0], 'chi2':c2, 'w0':w0, 'wa':wa}

    # B1 (A01)
    p, c2, w0, wa, ode = fit_Om(make_ode_B1, 'B1-A01 ', starts_1)
    results['B1_A01'] = {'Om':p[0], 'chi2':c2, 'w0':w0, 'wa':wa}

    # C1 (w_sq=1/3, 4H coefficient)
    p, c2, w0, wa, ode = fit_Om(make_ode_C1, 'C1-4H  ', starts_1)
    results['C1']     = {'Om':p[0], 'chi2':c2, 'w0':w0, 'wa':wa}

    # C2 (general w_sq scan)
    p, c2, w0, wa, ode = fit_Om(make_ode_C2_wsq, 'C2-wsq ', starts_2)
    results['C2']     = {'Om':p[0], 'w_sq':p[1], 'chi2':c2, 'w0':w0, 'wa':wa}

    # C6 (radiation coupling, free eta_r)
    p, c2, w0, wa, ode = fit_Om(make_ode_C6, 'C6-rad ', starts_C6)
    results['C6']     = {'Om':p[0], 'eta_r':p[1], 'chi2':c2, 'w0':w0, 'wa':wa}

    # C9 (Parker-PZ Gamma_0 from Ricci scalar)
    p, c2, w0, wa, ode = fit_Om(make_ode_C9, 'C9-PZ  ', starts_1)
    results['C9']     = {'Om':p[0], 'chi2':c2, 'w0':w0, 'wa':wa}

    # C14 (sigma->2*sigma phenomenological: A01 with 2x amplitude)
    p, c2, w0, wa, ode = fit_Om(make_ode_C14, 'C14-2s ', starts_1)
    results['C14']    = {'Om':p[0], 'chi2':c2, 'w0':w0, 'wa':wa}

    # Summary
    print()
    print('=== SUMMARY ===')
    print('DESI target: w0=-0.757  wa=-0.83')
    print()
    chi2_lcdm = results['LCDM']['chi2']
    chi2_b1   = results['B1_A01']['chi2']
    fmt = '{:<10} chi2={:<8} dLCDM={:<8} dB1={:<7} w0={:<8} wa={:<7}'
    for k, r in results.items():
        dl = round(r['chi2'] - chi2_lcdm, 3)
        db = round(r['chi2'] - chi2_b1, 3)
        print(fmt.format(k, round(r['chi2'],3), dl, db,
                         round(r.get('w0', float('nan')),3),
                         round(r.get('wa', float('nan')),3)))

    print()
    print('wa gap to DESI (-0.83):')
    for k, r in results.items():
        wa = r.get('wa', float('nan'))
        gap = round(-0.83 - wa, 3) if not np.isnan(wa) else 'nan'
        print('  ' + k + ': wa=' + str(round(wa,3)) + '  gap=' + str(gap))

    # Save
    out = os.path.join(_THIS, 'c1_c2_c6_c9_c14_results.json')
    with open(out, 'w') as f:
        json.dump(results, f, indent=2)
    print()
    print('Saved: ' + out)
    return results


if __name__ == '__main__':
    main()
