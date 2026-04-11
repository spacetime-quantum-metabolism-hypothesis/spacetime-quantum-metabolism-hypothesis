# -*- coding: utf-8 -*-
"""
L13-U: SQMH Uniqueness -- coincidence or prediction?

Rule-B 4-person code review:
  R1 (competitor set): define class of "wa<0 phenomenological 1-parameter models"
  R2 (statistical comparison): AIC/BIC comparison A01 vs competitors
  R3 (amplitude locking): test whether Om amplitude uniquely determined by SQMH
  R4 (verdict): K86/Q86 judgment

The critical question:
  A01: rho_DE = OL0 * [1 + Om*(1-a)] is 0-parameter (Om, h already in LCDM).
  Can any "wa<0 arbitrary 1-parameter model" match DESI as well as A01?

Competitor class:
  Parameterize rho_DE = OL0 * [1 + A*(1-a)] where A is free parameter.
  This is a 1-parameter extension (A is free, unlike A01 where A=Om is theory-fixed).

  If best-fit A ≈ Om for this model, then:
  - K86: A01 is DEGENERATE with the 1-parameter class -> SQMH not unique
  - Q86: best-fit A significantly different from Om -> A01 is uniquely picked by SQMH

Additionally:
  If A01 (with A=Om fixed) fits significantly better than LCDM,
  and the 1-parameter model (with A free) fits only marginally better,
  then Bayesian evidence strongly favors A01.
"""
from __future__ import annotations
import os
import sys
import json
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize, curve_fit
from scipy.interpolate import interp1d

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')

_THIS = os.path.dirname(os.path.abspath(__file__))

OMEGA_R = 9.1e-5
c_SI = 2.998e8
Mpc_m = 3.086e22
rs_drag = 147.09  # Mpc

# DESI DR2 simplified 7-bin data (from l13_ode_compare.py)
DESI_Z = np.array([0.295, 0.510, 0.706, 0.930, 1.317, 1.491, 2.330])
DESI_OBS = np.array([7.93, 13.62, 16.85, 21.71, 27.79, 30.21, 39.71])
DESI_ERR = np.array([0.15, 0.17, 0.22, 0.22, 0.55, 0.49, 0.94])


def compute_DM_fast(z_arr, Om, h, rho_de_func):
    """Compute comoving distance DM(z) in Mpc."""
    H0 = h * 100e3 / Mpc_m
    OL0 = 1.0 - Om - OMEGA_R
    z_int = np.linspace(0, max(z_arr) * 1.001, 2000)
    a_int = 1.0 / (1.0 + z_int)
    rho_de = np.array([rho_de_func(a) for a in a_int])
    E2 = OMEGA_R * (1 + z_int)**4 + Om * (1 + z_int)**3 + rho_de
    E2 = np.where(E2 > 1e-10, E2, 1e-10)
    Ez = np.sqrt(E2)
    integrand = 1.0 / Ez
    cumul = np.zeros(len(z_int))
    for i in range(1, len(z_int)):
        cumul[i] = np.trapezoid(integrand[:i+1], z_int[:i+1])
    chi_func = interp1d(z_int, cumul, kind='cubic', fill_value='extrapolate')
    DM = (c_SI / H0) / Mpc_m * chi_func(z_arr)
    return DM


def compute_DV_fast(z, Om, h, rho_de_func):
    """Compute DV(z) in Mpc."""
    H0 = h * 100e3 / Mpc_m
    a = 1.0 / (1.0 + z)
    rho_de = rho_de_func(a)
    E2 = OMEGA_R * (1 + z)**4 + Om * (1 + z)**3 + rho_de
    E2 = max(E2, 1e-10)
    Ez = np.sqrt(E2)
    DH = c_SI / (H0 * Ez) / Mpc_m
    DM_arr = compute_DM_fast(np.array([z]), Om, h, rho_de_func)
    DM = DM_arr[0]
    DV = (z * DM**2 * DH) ** (1.0 / 3.0)
    return DV


def chi2_model(Om, h, rho_de_func):
    """Chi2 against DESI 7-bin."""
    try:
        DV_295 = compute_DV_fast(0.295, Om, h, rho_de_func)
        pred_0 = DV_295 / rs_drag
        DM_arr = compute_DM_fast(DESI_Z[1:], Om, h, rho_de_func)
        pred_rest = DM_arr / rs_drag
        pred = np.concatenate([[pred_0], pred_rest])
        resid = pred - DESI_OBS
        chi2 = np.sum((resid / DESI_ERR) ** 2)
        return chi2 if np.isfinite(chi2) else 1e8
    except Exception:
        return 1e8


def make_rho_de(A_amp, Om, OL0):
    """rho_DE(a) = OL0 * [1 + A_amp*(1-a)], general amplitude."""
    def f(a):
        return OL0 * (1.0 + A_amp * (1.0 - a))
    return f


def fit_Om_h(rho_de_maker, extra_params=None, starts=None):
    """Fit Om, h (and optionally extra params) to minimize chi2."""
    if starts is None:
        starts = [(0.310, 0.677), (0.305, 0.680), (0.315, 0.673)]

    best_chi2 = 1e8
    best_params = None

    for Om0, h0 in starts:
        def neg_ll(theta):
            Om, h = theta[0], theta[1]
            if Om < 0.25 or Om > 0.40 or h < 0.60 or h > 0.75:
                return 1e8
            OL0 = 1.0 - Om - OMEGA_R
            if extra_params is None:
                rho_f = rho_de_maker(Om, OL0)
            else:
                rho_f = rho_de_maker(Om, OL0, *extra_params)
            return chi2_model(Om, h, rho_f)

        res = minimize(neg_ll, [Om0, h0], method='Nelder-Mead',
                       options={'xatol': 1e-5, 'fatol': 0.01, 'maxiter': 2000})
        if res.fun < best_chi2:
            best_chi2 = res.fun
            best_params = res.x

    return best_params[0], best_params[1], best_chi2


def fit_Om_h_A(starts=None):
    """Fit Om, h, A_amp to minimize chi2 (1-parameter model with free A)."""
    if starts is None:
        starts = [(0.310, 0.677, 0.31), (0.305, 0.680, 0.25), (0.315, 0.673, 0.40)]

    best_chi2 = 1e8
    best_params = None

    for Om0, h0, A0 in starts:
        def neg_ll(theta):
            Om, h, A = theta
            if Om < 0.25 or Om > 0.40 or h < 0.60 or h > 0.75 or A < -1.0 or A > 2.0:
                return 1e8
            OL0 = 1.0 - Om - OMEGA_R
            rho_f = make_rho_de(A, Om, OL0)
            return chi2_model(Om, h, rho_f)

        res = minimize(neg_ll, [Om0, h0, A0], method='Nelder-Mead',
                       options={'xatol': 1e-5, 'fatol': 0.01, 'maxiter': 3000})
        if res.fun < best_chi2:
            best_chi2 = res.fun
            best_params = res.x

    return best_params[0], best_params[1], best_params[2], best_chi2


def main():
    print('=== L13-U: SQMH Uniqueness Analysis ===')
    print()

    Om_ref = 0.3102
    OL0_ref = 1.0 - Om_ref - OMEGA_R

    # --- Model 0: LCDM ---
    rho_lcdm = make_rho_de(0.0, Om_ref, OL0_ref)  # A=0: pure Lambda
    Om_lcdm, h_lcdm, chi2_lcdm = fit_Om_h(
        lambda Om, OL0: make_rho_de(0.0, Om, OL0))
    print('LCDM: Om=' + str(round(Om_lcdm, 4)) + ' h=' + str(round(h_lcdm, 4)) +
          ' chi2=' + str(round(chi2_lcdm, 3)))

    # --- Model 1: A01 (A_amp = Om, SQMH theory-fixed) ---
    Om_a01, h_a01, chi2_a01 = fit_Om_h(
        lambda Om, OL0: make_rho_de(Om, Om, OL0))
    print('A01 (A=Om fixed): Om=' + str(round(Om_a01, 4)) + ' h=' + str(round(h_a01, 4)) +
          ' chi2=' + str(round(chi2_a01, 3)))

    # --- Model 2: Free amplitude (A_amp free, 1 extra parameter) ---
    Om_free, h_free, A_free, chi2_free = fit_Om_h_A()
    print('Free-A (A free): Om=' + str(round(Om_free, 4)) + ' h=' + str(round(h_free, 4)) +
          ' A=' + str(round(A_free, 4)) + ' chi2=' + str(round(chi2_free, 3)))

    print()
    dchi2_a01 = chi2_a01 - chi2_lcdm
    dchi2_free = chi2_free - chi2_lcdm
    dchi2_a01_vs_free = chi2_a01 - chi2_free
    print('Dchi2 A01 vs LCDM: ' + str(round(dchi2_a01, 3)))
    print('Dchi2 Free-A vs LCDM: ' + str(round(dchi2_free, 3)))
    print('Dchi2 A01 vs Free-A: ' + str(round(dchi2_a01_vs_free, 3)) +
          ' (positive means Free-A better)')

    # AIC comparison (AIC = chi2 + 2k)
    k_a01 = 2    # Om, h
    k_free = 3   # Om, h, A
    AIC_a01 = chi2_a01 + 2 * k_a01
    AIC_free = chi2_free + 2 * k_free
    delta_AIC = AIC_a01 - AIC_free  # positive: A01 better (less parameters)
    print()
    print('AIC A01: ' + str(round(AIC_a01, 3)))
    print('AIC Free-A: ' + str(round(AIC_free, 3)))
    print('Delta AIC (A01-Free): ' + str(round(delta_AIC, 3)) +
          ' (>0 means A01 preferred by AIC)')

    # BIC comparison (BIC = chi2 + k*ln(N))
    N_data = 7  # number of DESI z-bins
    BIC_a01 = chi2_a01 + k_a01 * np.log(N_data)
    BIC_free = chi2_free + k_free * np.log(N_data)
    delta_BIC = BIC_a01 - BIC_free
    print('BIC A01: ' + str(round(BIC_a01, 3)))
    print('BIC Free-A: ' + str(round(BIC_free, 3)))
    print('Delta BIC (A01-Free): ' + str(round(delta_BIC, 3)) +
          ' (>0 means A01 preferred by BIC)')

    print()

    # Check if A_free ~ Om (SQMH prediction)
    A_sqmh_pred = Om_a01  # A01 predicts A = Om
    A_dev = abs(A_free - A_sqmh_pred)
    print('SQMH-predicted A = Om = ' + str(round(A_sqmh_pred, 4)))
    print('Free-A best-fit A = ' + str(round(A_free, 4)))
    print('Deviation |A_free - Om| = ' + str(round(A_dev, 4)))
    print()

    # Uniqueness test: scan A values
    print('Scanning chi2 vs A amplitude...')
    A_scan = np.linspace(-0.5, 1.5, 40)
    chi2_scan = []
    for A_val in A_scan:
        def neg_ll_A(theta):
            Om, h = theta
            if Om < 0.25 or Om > 0.40 or h < 0.60 or h > 0.75:
                return 1e8
            OL0 = 1.0 - Om - OMEGA_R
            rho_f = make_rho_de(A_val, Om, OL0)
            return chi2_model(Om, h, rho_f)
        res = minimize(neg_ll_A, [0.310, 0.677], method='Nelder-Mead',
                       options={'xatol': 1e-4, 'fatol': 0.1, 'maxiter': 1000})
        chi2_scan.append(float(res.fun))

    chi2_scan = np.array(chi2_scan)
    A_best_scan = float(A_scan[np.argmin(chi2_scan)])
    chi2_best_scan = float(np.min(chi2_scan))

    print('Best A from scan: ' + str(round(A_best_scan, 3)) + ' (chi2=' +
          str(round(chi2_best_scan, 3)) + ')')
    print('A01 A = Om = ' + str(round(Om_ref, 3)))

    # Chi2 at A = Om vs global minimum
    idx_om = np.argmin(np.abs(A_scan - Om_ref))
    chi2_at_om = float(chi2_scan[idx_om])
    print('Chi2 at A=Om: ' + str(round(chi2_at_om, 3)))
    print('Chi2 global min: ' + str(round(chi2_best_scan, 3)))
    print('Delta chi2 (A=Om vs global): ' + str(round(chi2_at_om - chi2_best_scan, 3)))

    print()

    # K86/Q86 verdict
    # K86: A01 indistinguishable from arbitrary 1-param model
    # Q86: A01 uniquely determined by SQMH
    # Key metric: does best-fit A ≈ Om? And is AIC/BIC favorable to A01?

    # If A_free ≈ Om AND AIC_free < AIC_a01:
    #   Free-A marginally better but best-fit A ~ Om => SQMH motivated
    # If A_free != Om AND AIC/BIC favor A01:
    #   SQMH preferred (fewer params, same chi2)

    k86_triggered = (AIC_a01 > AIC_free and dchi2_a01_vs_free > 2.0)
    q86_triggered = (AIC_a01 <= AIC_free and A_dev < 0.05)

    if k86_triggered:
        verdict = ('K86 TRIGGERED: Free-A improves chi2 by > 2 AND AIC favors free model. '
                   'A01 is not uniquely preferred over arbitrary 1-param model.')
    elif q86_triggered:
        verdict = ('Q86 TRIGGERED: AIC favors A01 (zero extra params) AND best-fit A ~ Om. '
                   'SQMH uniquely determines amplitude to match theory prediction.')
    else:
        verdict = ('K86/Q86 intermediate: delta_AIC=' + str(round(delta_AIC, 2)) +
                   ', A_free=' + str(round(A_free, 3)) + ', Om=' + str(round(Om_ref, 3)) +
                   ', A_dev=' + str(round(A_dev, 3)))

    print('VERDICT: ' + verdict)

    results = {
        'chi2_lcdm': float(chi2_lcdm),
        'chi2_a01': float(chi2_a01),
        'chi2_free': float(chi2_free),
        'dchi2_a01_vs_lcdm': float(dchi2_a01),
        'dchi2_free_vs_lcdm': float(dchi2_free),
        'dchi2_a01_vs_free': float(dchi2_a01_vs_free),
        'AIC_a01': float(AIC_a01),
        'AIC_free': float(AIC_free),
        'delta_AIC': float(delta_AIC),
        'BIC_a01': float(BIC_a01),
        'BIC_free': float(BIC_free),
        'delta_BIC': float(delta_BIC),
        'A_free_bestfit': float(A_free),
        'Om_a01': float(Om_a01),
        'A_sqmh_pred': float(A_sqmh_pred),
        'A_deviation': float(A_dev),
        'A_scan': A_scan.tolist(),
        'chi2_scan': chi2_scan.tolist(),
        'A_best_scan': A_best_scan,
        'chi2_best_scan': chi2_best_scan,
        'verdict': verdict,
        'k86_triggered': bool(k86_triggered),
        'q86_triggered': bool(q86_triggered),
    }

    out_path = os.path.join(_THIS, 'l13_uniqueness_results.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print('Results saved to: ' + out_path)
    return results


if __name__ == '__main__':
    main()
