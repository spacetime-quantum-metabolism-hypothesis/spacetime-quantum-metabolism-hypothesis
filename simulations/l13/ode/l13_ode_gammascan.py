# -*- coding: utf-8 -*-
"""
L13-O Round 2: ODE Gamma0 scan to find best-fit Gamma0 and compare to A01.

Scans Gamma0 in [0.1, 20] to find which G0 minimizes chi2 vs DESI.
Compares best ODE fit to A01 chi2.
"""
from __future__ import annotations
import os
import sys
import json
import numpy as np
from scipy.optimize import minimize
from scipy.interpolate import interp1d

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')

_THIS = os.path.dirname(os.path.abspath(__file__))

OMEGA_R = 9.1e-5
c_SI = 2.998e8
Mpc_m = 3.086e22
rs_drag = 147.09

DESI_Z = np.array([0.295, 0.510, 0.706, 0.930, 1.317, 1.491, 2.330])
DESI_OBS = np.array([7.93, 13.62, 16.85, 21.71, 27.79, 30.21, 39.71])
DESI_ERR = np.array([0.15, 0.17, 0.22, 0.22, 0.55, 0.49, 0.94])


def make_rho_ode(Om, G0):
    """Exact ODE solution: omega_de(a) = G0*Om/(6*a^3) + C*a^3."""
    OL0 = 1.0 - Om - OMEGA_R
    C = OL0 - G0 * Om / 6.0
    def f(a):
        val = G0 * Om / (6.0 * a**3) + C * a**3
        return max(float(val), -1.0)  # guard
    return f


def make_rho_a01(Om):
    """A01 form."""
    OL0 = 1.0 - Om - OMEGA_R
    def f(a):
        return OL0 * (1.0 + Om * (1.0 - a))
    return f


def compute_DM(z_arr, Om, h, rho_func):
    H0 = h * 100e3 / Mpc_m
    z_int = np.linspace(0, max(z_arr) * 1.001, 2000)
    a_int = 1.0 / (1.0 + z_int)
    rho = np.array([rho_func(a) for a in a_int])
    E2 = OMEGA_R * (1 + z_int)**4 + Om * (1 + z_int)**3 + rho
    E2 = np.where(E2 > 1e-10, E2, 1e-10)
    integrand = 1.0 / np.sqrt(E2)
    cumul = np.zeros(len(z_int))
    for i in range(1, len(z_int)):
        cumul[i] = np.trapezoid(integrand[:i+1], z_int[:i+1])
    chi_func = interp1d(z_int, cumul, kind='cubic', fill_value='extrapolate')
    DM = (c_SI / H0) / Mpc_m * chi_func(z_arr)
    return DM


def compute_DV(z, Om, h, rho_func):
    H0 = h * 100e3 / Mpc_m
    a = 1.0 / (1.0 + z)
    rho = rho_func(a)
    E2 = OMEGA_R * (1 + z)**4 + Om * (1 + z)**3 + rho
    E2 = max(float(E2), 1e-10)
    DH = c_SI / (H0 * np.sqrt(E2)) / Mpc_m
    DM_arr = compute_DM(np.array([z]), Om, h, rho_func)
    DV = (z * DM_arr[0]**2 * DH) ** (1.0/3.0)
    return DV


def chi2_model(Om, h, rho_func):
    try:
        DV_295 = compute_DV(0.295, Om, h, rho_func)
        pred_0 = DV_295 / rs_drag
        DM_arr = compute_DM(DESI_Z[1:], Om, h, rho_func)
        pred_rest = DM_arr / rs_drag
        pred = np.concatenate([[pred_0], pred_rest])
        resid = pred - DESI_OBS
        c2 = np.sum((resid / DESI_ERR)**2)
        return float(c2) if np.isfinite(c2) else 1e8
    except Exception:
        return 1e8


def fit_Om_h(rho_maker):
    """Fit Om, h for given rho_maker(Om) -> rho_func."""
    best_c2 = 1e8
    best_p = None
    for Om0, h0 in [(0.310, 0.677), (0.305, 0.680), (0.315, 0.673)]:
        def neg_ll(theta):
            Om, h = theta
            if Om < 0.25 or Om > 0.40 or h < 0.60 or h > 0.75:
                return 1e8
            return chi2_model(Om, h, rho_maker(Om))
        res = minimize(neg_ll, [Om0, h0], method='Nelder-Mead',
                       options={'xatol': 1e-5, 'fatol': 0.01, 'maxiter': 2000})
        if res.fun < best_c2:
            best_c2 = res.fun
            best_p = res.x
    if best_p is None:
        return 0.31, 0.677, 1e8
    return float(best_p[0]), float(best_p[1]), float(best_c2)


def main():
    print('=== L13-O Round 2: ODE Gamma0 Scan ===')
    print()

    # A01 reference
    Om_a01, h_a01, chi2_a01 = fit_Om_h(lambda Om: make_rho_a01(Om))
    print('A01: Om=' + str(round(Om_a01, 4)) + ' h=' + str(round(h_a01, 4)) +
          ' chi2=' + str(round(chi2_a01, 3)))

    # Gamma0 scan
    G0_vals = np.linspace(0.1, 15.0, 30)
    chi2_scan = []
    Om_scan = []
    h_scan = []

    for G0 in G0_vals:
        Om_f, h_f, c2_f = fit_Om_h(lambda Om, g=G0: make_rho_ode(Om, g))
        chi2_scan.append(c2_f)
        Om_scan.append(Om_f)
        h_scan.append(h_f)
        print('G0=' + str(round(G0, 2)) + ' Om=' + str(round(Om_f, 4)) +
              ' h=' + str(round(h_f, 4)) + ' chi2=' + str(round(c2_f, 3)))

    chi2_scan = np.array(chi2_scan)
    best_idx = np.argmin(chi2_scan)
    G0_best = G0_vals[best_idx]
    chi2_best_ode = chi2_scan[best_idx]

    print()
    print('Best ODE G0=' + str(round(G0_best, 3)) + ' chi2=' + str(round(chi2_best_ode, 3)))
    print('A01 chi2=' + str(round(chi2_a01, 3)))
    print('ODE(best) vs A01: ' + str(round(chi2_best_ode - chi2_a01, 3)))

    if abs(chi2_best_ode - chi2_a01) <= 0.5:
        verdict = 'K81 TRIGGERED: Best ODE G0 gives chi2 within 0.5 of A01'
    elif chi2_best_ode < chi2_a01 - 2.0:
        verdict = 'Q81 TRIGGERED: Best ODE improves chi2 by > 2 vs A01'
    else:
        verdict = 'Intermediate: Best ODE G0 vs A01 diff=' + str(round(chi2_best_ode - chi2_a01, 3))

    print('VERDICT: ' + verdict)

    results = {
        'chi2_a01': float(chi2_a01),
        'Om_a01': float(Om_a01),
        'h_a01': float(h_a01),
        'G0_scan': G0_vals.tolist(),
        'chi2_scan': chi2_scan.tolist(),
        'Om_scan': Om_scan,
        'h_scan': h_scan,
        'G0_best': float(G0_best),
        'chi2_best_ode': float(chi2_best_ode),
        'diff_ode_vs_a01': float(chi2_best_ode - chi2_a01),
        'verdict': verdict,
        'k81_triggered': bool(abs(chi2_best_ode - chi2_a01) <= 0.5),
        'q81_triggered': bool(chi2_best_ode < chi2_a01 - 2.0),
    }

    out_path = os.path.join(_THIS, 'l13_ode_gammascan_results.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print('Results saved to: ' + out_path)
    return results


if __name__ == '__main__':
    main()
