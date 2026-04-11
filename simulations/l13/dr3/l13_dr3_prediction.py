# -*- coding: utf-8 -*-
"""
L13-D: DR3 prediction explicit calculation.

Rule-B 4-person code review:
  R1 (A01 predictions): compute A01 BAO distances at DR3 z-bins
  R2 (LCDM predictions): compute LCDM predictions at same bins
  R3 (Fisher SNR): compute expected SNR with DR3 uncertainties
  R4 (verdict): K85/Q85 judgment

DR3 expected improvements (from L10 dr3 forecast and DESI collaboration estimates):
  - BGS (z~0.3): 30% improvement in errors
  - LRG (z~0.5-0.9): 25-35% improvement
  - ELG (z~1.1-1.6): 40% improvement (biggest gain)
  - QSO (z~1.5): 30% improvement
  - Lya (z~2.3): 20% improvement
  Total DR3 data volume: ~3x DR2.

The Fisher SNR for A01 vs LCDM at bin i:
  SNR_i = |DM_A01(z_i) - DM_LCDM(z_i)| / sigma_DR3(z_i)
  where sigma_DR3 = sigma_DR2 * sqrt(N_DR2/N_DR3)
"""
from __future__ import annotations
import os
import sys
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
rs_drag = 147.09  # Mpc (Planck 2018)

# DESI DR2 z-bins and errors (from published DR2 data)
# Full 7-bin summary
DR2_Z = np.array([0.295, 0.510, 0.706, 0.930, 1.317, 1.491, 2.330])
DR2_OBS = np.array([7.93, 13.62, 16.85, 21.71, 27.79, 30.21, 39.71])
DR2_ERR = np.array([0.15, 0.17, 0.22, 0.22, 0.55, 0.49, 0.94])
DR2_TYPE = ['DV/rs', 'DM/rs', 'DM/rs', 'DM/rs', 'DM/rs', 'DM/rs', 'DM/rs']

# DR3 expected error scaling (from DESI Year 3 forecast papers)
# Approximate N_gal scaling: sigma_DR3 ~ sigma_DR2 * sqrt(N_DR2/N_DR3)
# DR3 volume ~ 3x DR2 for LRG/ELG, ~2x for BGS/QSO, ~1.5x for Lya
DR3_SCALE = np.array([
    1.0/np.sqrt(2.0),   # BGS z=0.295: 2x more BGS
    1.0/np.sqrt(3.0),   # LRG1 z=0.51: 3x more LRG
    1.0/np.sqrt(3.0),   # LRG2 z=0.71: 3x more LRG
    1.0/np.sqrt(2.5),   # LRG3+ELG1 z=0.93: 2.5x
    1.0/np.sqrt(3.5),   # ELG2 z=1.317: 3.5x (biggest gain)
    1.0/np.sqrt(2.5),   # QSO z=1.491: 2.5x
    1.0/np.sqrt(1.5),   # Lya z=2.33: 1.5x
])
DR3_ERR = DR2_ERR * DR3_SCALE

# A01 best-fit parameters (from L5 MCMC production)
Om_A01 = 0.3102
h_A01 = 0.6771
OL0_A01 = 1.0 - Om_A01 - OMEGA_R

# LCDM best-fit parameters
Om_LCDM = 0.326  # from L12 / standard LCDM fit
h_LCDM = 0.674
OL0_LCDM = 1.0 - Om_LCDM - OMEGA_R


def compute_DM(z_arr, Om, h, rho_de_func):
    """Comoving distance DM(z) in Mpc."""
    H0 = h * 100e3 / Mpc_m
    z_int = np.linspace(0, max(z_arr) * 1.001, 3000)
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


def compute_DH(z, Om, h, rho_de_func):
    """DH = c/(H0*E(z)) in Mpc."""
    H0 = h * 100e3 / Mpc_m
    a = 1.0 / (1.0 + z)
    rho_de = rho_de_func(a)
    E2 = OMEGA_R * (1 + z)**4 + Om * (1 + z)**3 + rho_de
    E2 = max(float(E2), 1e-10)
    Ez = np.sqrt(E2)
    DH = c_SI / (H0 * Ez) / Mpc_m
    return DH


def compute_DV(z, Om, h, rho_de_func):
    """DV(z) = [z * DM^2 * DH]^(1/3) in Mpc."""
    DH = compute_DH(z, Om, h, rho_de_func)
    DM_arr = compute_DM(np.array([z]), Om, h, rho_de_func)
    DM = DM_arr[0]
    DV = (z * DM**2 * DH) ** (1.0 / 3.0)
    return DV


def rho_de_A01(a):
    return OL0_A01 * (1.0 + Om_A01 * (1.0 - a))


def rho_de_LCDM(a):
    return OL0_LCDM


def main():
    print('=== L13-D: DR3 Prediction Explicit Calculation ===')
    print()
    print('A01: Om=' + str(Om_A01) + ' h=' + str(h_A01))
    print('LCDM: Om=' + str(Om_LCDM) + ' h=' + str(h_LCDM))
    print('rs_drag = ' + str(rs_drag) + ' Mpc (fiducial)')
    print()

    results = {}
    table_rows = []

    for i, z in enumerate(DR2_Z):
        # A01 prediction
        if DR2_TYPE[i] == 'DV/rs':
            pred_A01 = compute_DV(z, Om_A01, h_A01, rho_de_A01) / rs_drag
            pred_LCDM = compute_DV(z, Om_LCDM, h_LCDM, rho_de_LCDM) / rs_drag
            obs_type = 'DV/rs'
        else:
            DM_A01 = compute_DM(np.array([z]), Om_A01, h_A01, rho_de_A01)[0]
            DM_LCDM = compute_DM(np.array([z]), Om_LCDM, h_LCDM, rho_de_LCDM)[0]
            pred_A01 = DM_A01 / rs_drag
            pred_LCDM = DM_LCDM / rs_drag
            obs_type = 'DM/rs'

        obs = DR2_OBS[i]
        err_dr2 = DR2_ERR[i]
        err_dr3 = DR3_ERR[i]

        diff_A01 = pred_A01 - obs
        diff_LCDM = pred_LCDM - obs
        diff_models = pred_A01 - pred_LCDM

        SNR_dr2 = abs(diff_models) / err_dr2
        SNR_dr3 = abs(diff_models) / err_dr3

        row = {
            'z': float(z),
            'type': obs_type,
            'observed': float(obs),
            'pred_A01': float(pred_A01),
            'pred_LCDM': float(pred_LCDM),
            'diff_A01_obs': float(diff_A01),
            'diff_LCDM_obs': float(diff_LCDM),
            'diff_A01_LCDM': float(diff_models),
            'err_DR2': float(err_dr2),
            'err_DR3': float(err_dr3),
            'SNR_DR2': float(SNR_dr2),
            'SNR_DR3': float(SNR_dr3),
        }
        table_rows.append(row)

        print('z=' + str(round(z, 3)) + ' (' + obs_type + '):')
        print('  Obs=' + str(round(obs, 3)) +
              '  A01=' + str(round(pred_A01, 3)) +
              '  LCDM=' + str(round(pred_LCDM, 3)))
        print('  Diff(A01-LCDM)=' + str(round(diff_models, 4)) +
              '  DR2_err=' + str(round(err_dr2, 3)) +
              '  DR3_err=' + str(round(err_dr3, 3)))
        print('  SNR DR2=' + str(round(SNR_dr2, 3)) +
              '  SNR DR3=' + str(round(SNR_dr3, 3)))
        print()

    # Combined Fisher SNR
    diff_arr = np.array([r['diff_A01_LCDM'] for r in table_rows])
    err_dr3_arr = np.array([r['err_DR3'] for r in table_rows])
    err_dr2_arr = np.array([r['err_DR2'] for r in table_rows])

    # Total chi2 (diagonal)
    chi2_diff_dr3 = np.sum((diff_arr / err_dr3_arr) ** 2)
    chi2_diff_dr2 = np.sum((diff_arr / err_dr2_arr) ** 2)
    total_SNR_dr2 = np.sqrt(chi2_diff_dr2)
    total_SNR_dr3 = np.sqrt(chi2_diff_dr3)

    print('Combined Fisher SNR:')
    print('  DR2 combined SNR = sqrt(sum(dchi2)) = ' + str(round(total_SNR_dr2, 3)) + 'sigma')
    print('  DR3 combined SNR = ' + str(round(total_SNR_dr3, 3)) + 'sigma')
    print()

    # Best z-bin for discrimination
    SNR_dr3_arr = np.array([r['SNR_DR3'] for r in table_rows])
    best_bin_idx = np.argmax(SNR_dr3_arr)
    best_z = DR2_Z[best_bin_idx]
    best_SNR = SNR_dr3_arr[best_bin_idx]

    print('Best z-bin for A01 vs LCDM discrimination:')
    print('  z=' + str(round(best_z, 3)) +
          '  DR3 SNR=' + str(round(best_SNR, 3)) + 'sigma')
    print()

    # K85/Q85 verdict
    max_SNR_dr3 = float(np.max(SNR_dr3_arr))
    if max_SNR_dr3 < 2.0:
        verdict = ('K85 TRIGGERED: Max DR3 SNR = ' + str(round(max_SNR_dr3, 3)) +
                   ' < 2sigma. DR3 cannot discriminate A01 from LCDM.')
    elif max_SNR_dr3 >= 3.0:
        verdict = ('Q85 TRIGGERED: Max DR3 SNR = ' + str(round(max_SNR_dr3, 3)) +
                   ' >= 3sigma at z=' + str(round(best_z, 3)) +
                   '. DR3 CAN discriminate A01 from LCDM.')
    else:
        verdict = ('K85/Q85 intermediate: Max DR3 SNR = ' + str(round(max_SNR_dr3, 3)) +
                   ' sigma (2-3 range).')

    print('VERDICT: ' + verdict)

    results = {
        'Om_A01': Om_A01,
        'h_A01': h_A01,
        'Om_LCDM': Om_LCDM,
        'h_LCDM': h_LCDM,
        'rs_drag': rs_drag,
        'dr2_z_bins': DR2_Z.tolist(),
        'table_rows': table_rows,
        'combined_SNR_DR2': float(total_SNR_dr2),
        'combined_SNR_DR3': float(total_SNR_dr3),
        'max_SNR_DR3': max_SNR_dr3,
        'best_z_bin': float(best_z),
        'best_z_SNR_DR3': float(best_SNR),
        'verdict': verdict,
        'k85_triggered': max_SNR_dr3 < 2.0,
        'q85_triggered': max_SNR_dr3 >= 3.0,
    }

    out_path = os.path.join(_THIS, 'l13_dr3_results.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print('Results saved to: ' + out_path)
    return results


if __name__ == '__main__':
    main()
