# -*- coding: utf-8 -*-
"""
L14-B9-B15: Hubble-Modulated (B9) and Entropy-Based (B15) creation rate test.

B9:  dn/dt + 3Hn = Gamma_0*(H/H0)   - sigma*n*rho_m
     Quasi-static equilibrium: omega_de_B9(z) = OL0 * E(z)*(beta+1) / (beta*(1+z)^3 + E(z))

B15: dn/dt + 3Hn = Gamma_0*(H0/H)^2 - sigma*n*rho_m
     Quasi-static equilibrium: omega_de_B15(z) = OL0 * (beta+1) / (E(z)^2*(beta*(1+z)^3 + E(z)))

beta = sigma*rho_m0/(3*H0) is treated as a free parameter (physical value ~1e-62, negligible).
With beta free, we search for the best-fit over (Om, beta).

Also tested:
  B9_phenom:  omega_de = OL0 * (1+Om*(1-a)) * E(z)          [A01 x E, phenomenological]
  B15_phenom: omega_de = OL0 * (1+Om*(1-a)) / E(z)^2        [A01 / E^2, phenomenological]

The self-consistent E(z) is solved iteratively (fixed-point) from:
  E(z)^2 = OMEGA_R*(1+z)^4 + Om*(1+z)^3 + omega_de(z; E)

CLAUDE.md rules:
  - sigma = 4*pi*G*t_P (SI)
  - No unicode in print()
  - numpy 2.x: trapezoid
  - BAO: 7-bin diagonal chi2
  - h fixed at 0.677, Om in [0.25, 0.40]
  - odeint for ODE; scipy.optimize for fitting
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

# Physical constants (SI)
c_SI   = 2.998e8
Mpc_m  = 3.086e22
OMEGA_R = 9.1e-5
rs_drag = 147.09        # Mpc
H0_KMS  = 67.7
H0_SI   = H0_KMS * 1e3 / Mpc_m

# DESI DR2 7-bin diagonal
DESI_Z   = np.array([0.295, 0.510, 0.706, 0.930, 1.317, 1.491, 2.330])
DESI_OBS = np.array([7.93, 13.62, 16.85, 21.71, 27.79, 30.21, 39.71])
DESI_ERR = np.array([0.15,  0.17,  0.22,  0.22,  0.55,  0.49,  0.94])

# ---------------------------------------------------------------------------
# E(z) self-consistent solver
# ---------------------------------------------------------------------------

def E_lcdm(z, Om):
    """Background LCDM E(z) (used as initial guess for iteration)."""
    OL0 = 1.0 - Om - OMEGA_R
    return np.sqrt(np.maximum(
        OMEGA_R*(1+z)**4 + Om*(1+z)**3 + OL0, 1e-15))


def solve_E_selfconsistent(z_arr, Om, omega_de_func_of_E, max_iter=50, tol=1e-8):
    """
    Solve E(z)^2 = OM(z) + omega_de(z; E(z)) by fixed-point iteration.
    omega_de_func_of_E(z, E) -> scalar.
    """
    z_arr = np.asarray(z_arr, dtype=float)
    OM = OMEGA_R*(1+z_arr)**4 + Om*(1+z_arr)**3

    # Initial guess: LCDM
    E = E_lcdm(z_arr, Om)

    for _ in range(max_iter):
        ode_arr = np.array([omega_de_func_of_E(z_arr[i], E[i]) for i in range(len(z_arr))])
        ode_arr = np.maximum(ode_arr, 0.0)
        E_new = np.sqrt(np.maximum(OM + ode_arr, 1e-15))
        if np.max(np.abs(E_new - E)) < tol:
            E = E_new
            break
        E = 0.5*E_new + 0.5*E  # damped iteration
    return E, ode_arr


# ---------------------------------------------------------------------------
# Dark energy functional forms
# ---------------------------------------------------------------------------

def omega_de_A01(z, Om):
    """A01 (B1 phenomenological): OL0*(1+Om*(1-a))."""
    OL0 = 1.0 - Om - OMEGA_R
    a = 1.0/(1.0+z)
    return OL0*(1.0 + Om*(1.0 - a))


def omega_de_B9_qs(z, E, Om, beta):
    """
    B9 quasi-static equilibrium.
    omega_de_B9 = OL0 * E(z)*(beta+1) / (beta*(1+z)^3 + E(z))
    """
    OL0 = 1.0 - Om - OMEGA_R
    denom = beta*(1.0+z)**3 + E
    return OL0*E*(beta+1.0)/np.maximum(denom, 1e-15)


def omega_de_B15_qs(z, E, Om, beta):
    """
    B15 quasi-static equilibrium.
    omega_de_B15 = OL0*(beta+1) / (E^2 * (beta*(1+z)^3 + E))
    """
    OL0 = 1.0 - Om - OMEGA_R
    denom = (E**2) * (beta*(1.0+z)**3 + E)
    return OL0*(beta+1.0)/np.maximum(denom, 1e-15)


def omega_de_B9_phenom(z, E, Om):
    """
    B9 phenomenological: A01 * E(z)  (normalized at z=0 -> already OL0 since E(0)=1).
    """
    return omega_de_A01(z, Om) * E


def omega_de_B15_phenom(z, E, Om):
    """
    B15 phenomenological: A01 / E(z)^2 (normalized at z=0 -> OL0 since E(0)=1).
    """
    return omega_de_A01(z, Om) / np.maximum(E**2, 1e-15)


# ---------------------------------------------------------------------------
# Distance calculations
# ---------------------------------------------------------------------------

def compute_distances(z_targets, E_arr, z_arr):
    """Compute DV(z_targets[0]) and DM(z_targets[1:]) given E(z) on z_arr."""
    E_interp = interp1d(z_arr, E_arr, kind='cubic',
                        fill_value='extrapolate', bounds_error=False)

    z_int = np.linspace(0, max(z_targets)*1.001, 5000)
    dz_int = np.diff(z_int)
    inv_E = 1.0/E_interp(z_int)

    # Cumulative comoving distance
    cum = np.zeros(len(z_int))
    for i in range(1, len(z_int)):
        cum[i] = cum[i-1] + 0.5*(inv_E[i-1]+inv_E[i])*dz_int[i-1]
    chi_func = interp1d(z_int, cum, kind='cubic',
                        fill_value='extrapolate', bounds_error=False)

    DH_over_rs = c_SI/(H0_SI*E_interp(z_targets[0]))/Mpc_m/rs_drag
    DM_over_rs = c_SI/H0_SI/Mpc_m * chi_func(z_targets) / rs_drag

    # DV/rs at z_targets[0]
    DM_0 = DM_over_rs[0]*rs_drag
    DH_0 = DH_over_rs*rs_drag
    DV_0 = (z_targets[0]*DM_0**2*DH_0)**(1.0/3.0)/rs_drag

    return DV_0, DM_over_rs[1:]


def chi2_from_E(E_arr, z_arr):
    """7-bin diagonal chi2 given E(z) on z_arr."""
    try:
        DV_0, DM_rest = compute_distances(DESI_Z, E_arr, z_arr)
        pred = np.concatenate([[DV_0], DM_rest])
        resid = pred - DESI_OBS
        c2 = float(np.sum((resid/DESI_ERR)**2))
        return c2 if np.isfinite(c2) and c2 < 1e8 else 1e8
    except Exception:
        return 1e8


# ---------------------------------------------------------------------------
# w(z) -> CPL
# ---------------------------------------------------------------------------

def fit_cpl_from_E_ode(ode_interp, z_fit=None):
    """Fit CPL from omega_de(z) interpolator."""
    if z_fit is None:
        z_fit = np.linspace(0.01, 1.5, 300)
    dz = 1e-4
    u   = np.array([float(ode_interp(z)) for z in z_fit])
    u_p = np.array([float(ode_interp(z+dz)) for z in z_fit])
    u_m = np.array([float(ode_interp(max(z-dz,1e-5))) for z in z_fit])
    dlnu = (u_p - u_m)/(2*dz*np.maximum(u, 1e-20))
    w_z = (1+z_fit)*dlnu/3.0 - 1.0

    def w_cpl(z, w0, wa):
        return w0 + wa*(1 - 1/(1+z))
    try:
        popt, _ = curve_fit(w_cpl, z_fit, w_z, p0=[-0.95, -0.2],
                            bounds=([-3.0, -8.0], [0.5, 5.0]), maxfev=5000)
        return float(popt[0]), float(popt[1])
    except Exception:
        return float('nan'), float('nan')


# ---------------------------------------------------------------------------
# Generic model fitter
# ---------------------------------------------------------------------------

N_Z = 2000
Z_MAX = 5.0
Z_ARR_GLOBAL = np.linspace(0, Z_MAX, N_Z)


def make_E_and_ode(model_func_of_E, Om):
    """
    Solve E self-consistently for a model where omega_de = f(z, E; params).
    model_func_of_E(z, E) -> scalar.
    Returns (E_arr, ode_arr) on Z_ARR_GLOBAL.
    """
    E_arr, ode_arr = solve_E_selfconsistent(Z_ARR_GLOBAL, Om, model_func_of_E)
    return E_arr, ode_arr


def fit_model(label, make_E_func, param_bounds, param_start_list):
    """
    Fit model with make_E_func(params) -> (E_arr, ode_arr).
    params = list of free parameters (Om always first).
    Returns (best_params, chi2_best).
    """
    best_chi2 = 1e9
    best_params = param_start_list[0]

    for p0 in param_start_list:
        def obj(p):
            for i, (lo, hi) in enumerate(param_bounds):
                if p[i] < lo or p[i] > hi:
                    return 1e8
            try:
                E_arr, _ = make_E_func(p)
                return chi2_from_E(E_arr, Z_ARR_GLOBAL)
            except Exception:
                return 1e8

        res = minimize(obj, p0, method='Nelder-Mead',
                       options={'xatol': 1e-5, 'fatol': 0.01, 'maxiter': 5000})
        if res.fun < best_chi2:
            best_chi2 = res.fun
            best_params = list(res.x)

    # CPL at best params
    E_arr, ode_arr = make_E_func(best_params)
    ode_interp = interp1d(Z_ARR_GLOBAL, ode_arr, kind='cubic',
                          fill_value='extrapolate', bounds_error=False)
    w0, wa = fit_cpl_from_E_ode(ode_interp)

    print(label + '  params=' + str([round(x, 4) for x in best_params]) +
          '  chi2=' + str(round(best_chi2, 3)) +
          '  w0=' + str(round(w0, 3)) + '  wa=' + str(round(wa, 3)))
    return best_params, best_chi2, w0, wa


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print('=== L14-B9-B15: Hubble-Modulated and Entropy Creation Rate Tests ===')
    print()

    results = {}

    # ------------------------------------------------------------------
    # 1. LCDM
    # ------------------------------------------------------------------
    def make_E_lcdm(p):
        Om = p[0]
        OL0 = 1.0 - Om - OMEGA_R
        ode_arr = np.full(len(Z_ARR_GLOBAL), OL0)
        E_arr = np.sqrt(np.maximum(
            OMEGA_R*(1+Z_ARR_GLOBAL)**4 + Om*(1+Z_ARR_GLOBAL)**3 + OL0, 1e-15))
        return E_arr, ode_arr

    starts_1p = [[0.290],[0.300],[0.310],[0.315],[0.320],[0.330]]
    p_lcdm, chi2_lcdm, w0_lcdm, wa_lcdm = fit_model(
        'LCDM   ', make_E_lcdm,
        [(0.25, 0.40)], starts_1p)
    results['lcdm'] = {'Om': p_lcdm[0], 'chi2': chi2_lcdm, 'w0': w0_lcdm, 'wa': wa_lcdm}

    # ------------------------------------------------------------------
    # 2. B1 (A01, phenomenological, 1 param)
    # ------------------------------------------------------------------
    def make_E_B1(p):
        Om = p[0]
        ode_arr = np.array([omega_de_A01(z, Om) for z in Z_ARR_GLOBAL])
        E_arr = np.sqrt(np.maximum(
            OMEGA_R*(1+Z_ARR_GLOBAL)**4 + Om*(1+Z_ARR_GLOBAL)**3 + ode_arr, 1e-15))
        return E_arr, ode_arr

    p_b1, chi2_b1, w0_b1, wa_b1 = fit_model(
        'B1-A01 ', make_E_B1,
        [(0.25, 0.40)], starts_1p)
    results['b1'] = {'Om': p_b1[0], 'chi2': chi2_b1, 'w0': w0_b1, 'wa': wa_b1}

    # ------------------------------------------------------------------
    # 3. B9 quasi-static (2 params: Om, beta)
    # ------------------------------------------------------------------
    def make_E_B9_qs(p):
        Om, beta = p[0], max(p[1], 1e-8)
        def f(z, E):
            return omega_de_B9_qs(z, E, Om, beta)
        E_arr, ode_arr = make_E_and_ode(f, Om)
        return E_arr, ode_arr

    starts_2p = [[Om, b] for Om in [0.300, 0.310, 0.315, 0.320]
                          for b in [0.01, 0.1, 0.5, 1.0, 3.0]]
    p_b9, chi2_b9, w0_b9, wa_b9 = fit_model(
        'B9-qs  ', make_E_B9_qs,
        [(0.25, 0.40), (1e-6, 100.0)], starts_2p)
    results['b9_qs'] = {'Om': p_b9[0], 'beta': p_b9[1], 'chi2': chi2_b9, 'w0': w0_b9, 'wa': wa_b9}

    # ------------------------------------------------------------------
    # 4. B15 quasi-static (2 params: Om, beta)
    # ------------------------------------------------------------------
    def make_E_B15_qs(p):
        Om, beta = p[0], max(p[1], 1e-8)
        def f(z, E):
            return omega_de_B15_qs(z, E, Om, beta)
        E_arr, ode_arr = make_E_and_ode(f, Om)
        return E_arr, ode_arr

    p_b15, chi2_b15, w0_b15, wa_b15 = fit_model(
        'B15-qs ', make_E_B15_qs,
        [(0.25, 0.40), (1e-6, 100.0)], starts_2p)
    results['b15_qs'] = {'Om': p_b15[0], 'beta': p_b15[1], 'chi2': chi2_b15, 'w0': w0_b15, 'wa': wa_b15}

    # ------------------------------------------------------------------
    # 5. B9 phenomenological: A01 * E(z)  (1 param, same as B1)
    # ------------------------------------------------------------------
    def make_E_B9_phenom(p):
        Om = p[0]
        def f(z, E):
            return omega_de_B9_phenom(z, E, Om)
        E_arr, ode_arr = make_E_and_ode(f, Om)
        return E_arr, ode_arr

    p_b9p, chi2_b9p, w0_b9p, wa_b9p = fit_model(
        'B9-phenom', make_E_B9_phenom,
        [(0.25, 0.40)], starts_1p)
    results['b9_phenom'] = {'Om': p_b9p[0], 'chi2': chi2_b9p, 'w0': w0_b9p, 'wa': wa_b9p}

    # ------------------------------------------------------------------
    # 6. B15 phenomenological: A01 / E(z)^2  (1 param, same as B1)
    # ------------------------------------------------------------------
    def make_E_B15_phenom(p):
        Om = p[0]
        def f(z, E):
            return omega_de_B15_phenom(z, E, Om)
        E_arr, ode_arr = make_E_and_ode(f, Om)
        return E_arr, ode_arr

    p_b15p, chi2_b15p, w0_b15p, wa_b15p = fit_model(
        'B15-phenom', make_E_B15_phenom,
        [(0.25, 0.40)], starts_1p)
    results['b15_phenom'] = {'Om': p_b15p[0], 'chi2': chi2_b15p, 'w0': w0_b15p, 'wa': wa_b15p}

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print()
    print('=== SUMMARY (7-bin diagonal chi2, DESI DR2) ===')
    print('DESI target: w0=-0.757  wa=-0.83')
    print()
    fmt = '{:<14} chi2={:<7} Dchi2_vs_LCDM={:<7} w0={:<7} wa={:<7}'
    for name, r in results.items():
        dc = round(r['chi2'] - chi2_lcdm, 3)
        print(fmt.format(name, round(r['chi2'],3), dc,
                         round(r.get('w0', float('nan')),3),
                         round(r.get('wa', float('nan')),3)))

    print()
    print('B1  vs LCDM: Dchi2=' + str(round(chi2_b1 - chi2_lcdm, 3)))
    print('B9_qs  vs B1: Dchi2=' + str(round(chi2_b9 - chi2_b1, 3)) +
          '  (beta=' + str(round(p_b9[1], 4)) + ')')
    print('B15_qs vs B1: Dchi2=' + str(round(chi2_b15 - chi2_b1, 3)) +
          '  (beta=' + str(round(p_b15[1], 4)) + ')')
    print('B9_phenom  vs B1: Dchi2=' + str(round(chi2_b9p - chi2_b1, 3)))
    print('B15_phenom vs B1: Dchi2=' + str(round(chi2_b15p - chi2_b1, 3)))

    print()
    print('wa comparison (DESI target: -0.83):')
    print('  B1 wa=' + str(round(wa_b1, 3)))
    print('  B9_qs wa=' + str(round(wa_b9, 3)))
    print('  B15_qs wa=' + str(round(wa_b15, 3)))
    print('  B9_phenom wa=' + str(round(wa_b9p, 3)))
    print('  B15_phenom wa=' + str(round(wa_b15p, 3)))

    # Save
    out = os.path.join(_THIS, 'b9_b15_results.json')
    with open(out, 'w') as f:
        json.dump(results, f, indent=2)
    print()
    print('Saved: ' + out)
    return results


if __name__ == '__main__':
    main()
