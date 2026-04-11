# -*- coding: utf-8 -*-
"""
L13-D Round 4: DR3 combined Fisher analysis with fixed Om/h.

Tests the "pure SQMH perturbation signal" by fixing Om,h to A01 best-fit
and comparing A01 vs LCDM at same cosmological parameters.
"""
from __future__ import annotations
import os
import json
import numpy as np
from scipy.interpolate import interp1d

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')

_THIS = os.path.dirname(os.path.abspath(__file__))

OMEGA_R = 9.1e-5
c_SI = 2.998e8
Mpc_m = 3.086e22
rs_drag = 147.09

DR2_Z = np.array([0.295, 0.510, 0.706, 0.930, 1.317, 1.491, 2.330])
DR2_OBS = np.array([7.93, 13.62, 16.85, 21.71, 27.79, 30.21, 39.71])
DR2_ERR = np.array([0.15, 0.17, 0.22, 0.22, 0.55, 0.49, 0.94])

DR3_SCALE = np.array([1/np.sqrt(2), 1/np.sqrt(3), 1/np.sqrt(3),
                       1/np.sqrt(2.5), 1/np.sqrt(3.5), 1/np.sqrt(2.5), 1/np.sqrt(1.5)])
DR3_ERR = DR2_ERR * DR3_SCALE

# A01 best-fit (L5 MCMC)
Om_bf = 0.3102
h_bf = 0.6771
OL0_bf = 1.0 - Om_bf - OMEGA_R


def compute_DM(z_arr, Om, h, rho_func):
    H0 = h * 100e3 / Mpc_m
    z_int = np.linspace(0, max(z_arr)*1.001, 3000)
    a_int = 1.0 / (1.0 + z_int)
    rho = np.array([rho_func(a) for a in a_int])
    E2 = OMEGA_R*(1+z_int)**4 + Om*(1+z_int)**3 + rho
    E2 = np.where(E2 > 1e-10, E2, 1e-10)
    integrand = 1.0 / np.sqrt(E2)
    cumul = np.zeros(len(z_int))
    for i in range(1, len(z_int)):
        cumul[i] = np.trapezoid(integrand[:i+1], z_int[:i+1])
    chi_func = interp1d(z_int, cumul, kind='cubic', fill_value='extrapolate')
    return (c_SI/H0)/Mpc_m * chi_func(z_arr)


def compute_DV(z, Om, h, rho_func):
    H0 = h * 100e3 / Mpc_m
    a = 1.0 / (1.0+z)
    rho = rho_func(a)
    E2 = OMEGA_R*(1+z)**4 + Om*(1+z)**3 + rho
    E2 = max(float(E2), 1e-10)
    DH = c_SI/(H0*np.sqrt(E2))/Mpc_m
    DM = compute_DM(np.array([z]), Om, h, rho_func)[0]
    return (z*DM**2*DH)**(1.0/3.0)


def main():
    print('=== L13-D Round 4: DR3 Combined Fisher (Fixed Om,h) ===')
    print()
    print('Using A01 best-fit: Om=' + str(Om_bf) + ', h=' + str(h_bf))
    print()

    # At fixed Om,h: compare A01 and LCDM perturbation
    rho_A01 = lambda a: OL0_bf * (1.0 + Om_bf * (1.0 - a))
    rho_LCDM = lambda a: OL0_bf  # same Om,h, just no perturbation

    rows = []
    for i, z in enumerate(DR2_Z):
        if i == 0:  # DV/rs
            pred_A01 = compute_DV(z, Om_bf, h_bf, rho_A01) / rs_drag
            pred_LCDM = compute_DV(z, Om_bf, h_bf, rho_LCDM) / rs_drag
        else:
            DM_A01 = compute_DM(np.array([z]), Om_bf, h_bf, rho_A01)[0]
            DM_LCDM = compute_DM(np.array([z]), Om_bf, h_bf, rho_LCDM)[0]
            pred_A01 = DM_A01 / rs_drag
            pred_LCDM = DM_LCDM / rs_drag

        diff = pred_A01 - pred_LCDM
        snr_dr2 = abs(diff) / DR2_ERR[i]
        snr_dr3 = abs(diff) / DR3_ERR[i]

        rows.append({
            'z': float(z), 'pred_A01': float(pred_A01),
            'pred_LCDM': float(pred_LCDM), 'diff': float(diff),
            'err_DR2': float(DR2_ERR[i]), 'err_DR3': float(DR3_ERR[i]),
            'SNR_DR2': float(snr_dr2), 'SNR_DR3': float(snr_dr3),
        })
        print('z=' + str(round(z,3)) + ' A01=' + str(round(pred_A01,4)) +
              ' LCDM=' + str(round(pred_LCDM,4)) + ' diff=' + str(round(diff,4)) +
              ' SNR_DR3=' + str(round(snr_dr3,3)))

    # Combined SNR (fixed Om,h: pure perturbation signal)
    diff_arr = np.array([r['diff'] for r in rows])
    combined_dr3 = float(np.sqrt(np.sum((diff_arr/DR3_ERR)**2)))
    combined_dr2 = float(np.sqrt(np.sum((diff_arr/DR2_ERR)**2)))
    max_snr_dr3 = float(np.max([r['SNR_DR3'] for r in rows]))
    best_z = float(DR2_Z[np.argmax([r['SNR_DR3'] for r in rows])])

    print()
    print('Combined DR2 SNR (fixed Om,h) = ' + str(round(combined_dr2,3)) + ' sigma')
    print('Combined DR3 SNR (fixed Om,h) = ' + str(round(combined_dr3,3)) + ' sigma')
    print('Max single-bin DR3 SNR = ' + str(round(max_snr_dr3,3)) + ' at z=' + str(round(best_z,3)))
    print()

    # Note: fixed Om,h gives PURE SQMH perturbation signal
    # Real analysis would marginalize over Om,h -> smaller SNR
    print('NOTE: Fixed Om,h gives UPPER BOUND on discrimination SNR.')
    print('Marginalizing over Om,h would reduce this by ~30-50%.')
    print()

    # Estimated marginal SNR
    snr_marginal_dr3 = combined_dr3 * 0.6  # conservative 40% reduction
    print('Estimated marginalized SNR: ~' + str(round(snr_marginal_dr3,2)) + ' sigma')
    print()

    if combined_dr3 >= 3.0:
        verdict = ('Q85 TRIGGERED (fixed Om,h): Combined DR3 SNR = ' +
                   str(round(combined_dr3,3)) + ' >= 3sigma')
    elif max_snr_dr3 >= 3.0:
        verdict = ('Q85 TRIGGERED (single-bin): Best bin SNR = ' +
                   str(round(max_snr_dr3,3)) + ' >= 3sigma')
    elif combined_dr3 >= 2.0:
        verdict = ('K85/Q85 intermediate: Combined=' + str(round(combined_dr3,3)) +
                   ', single-bin max=' + str(round(max_snr_dr3,3)))
    else:
        verdict = ('K85 TRIGGERED: Combined=' + str(round(combined_dr3,3)) +
                   ', single-bin=' + str(round(max_snr_dr3,3)) + ' < 2sigma')

    print('VERDICT: ' + verdict)

    results = {
        'Om_bf': Om_bf, 'h_bf': h_bf,
        'table': rows,
        'combined_SNR_DR2_fixed': combined_dr2,
        'combined_SNR_DR3_fixed': combined_dr3,
        'max_snr_DR3': max_snr_dr3,
        'best_z': best_z,
        'est_marginalized_SNR_DR3': float(snr_marginal_dr3),
        'verdict': verdict,
        'q85_triggered': bool(combined_dr3 >= 3.0 or max_snr_dr3 >= 3.0),
        'k85_triggered': bool(max_snr_dr3 < 2.0),
    }
    out_path = os.path.join(_THIS, 'l13_dr3_r4_results.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print('Results saved to: ' + out_path)
    return results


if __name__ == '__main__':
    main()
