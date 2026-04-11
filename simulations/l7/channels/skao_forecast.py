# -*- coding: utf-8 -*-
# CODE REVIEW: Bug-v Physics-v Repro-v Rules-v  [2026-04-11]
"""L7-X3: SKAO 21cm BAO sensitivity forecast vs SQMH E(z).

SKAO Phase-1 (2027-2030) 21cm intensity mapping BAO:
Redshift bins: z = 0.35, 0.47, 0.58, 0.68, 0.79, 0.90, 1.02, 1.15, 1.30, 1.45, 1.65, 1.85, 2.10
(Bull et al. 2015, Santos et al. 2015 sensitivity estimates)

Forecast: D_A(z)/r_d and H(z)*r_d predictions for C11D vs LCDM.
Check if SKAO can distinguish at >2sigma.
"""
from __future__ import annotations
import json, os, sys
import numpy as np
from scipy.integrate import quad

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIMS = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, _SIMS)
sys.path.insert(0, os.path.join(_SIMS, 'l4'))

# SKAO Phase-1 MID Band 1 forecast redshift bins and sigma_DA/r_d, sigma_H*r_d
# From SKA Cosmology SWG (Bacon et al. 2020), Table 1 (MID Band 1+2, optimistic)
SKAO_BINS = np.array([0.35, 0.47, 0.58, 0.68, 0.79, 0.90, 1.02, 1.15, 1.30, 1.45, 1.65, 1.85, 2.10])
# Fractional errors on D_A/r_d and H*r_d (percent, optimistic forecast)
SKAO_SIG_DA = np.array([0.62, 0.53, 0.52, 0.52, 0.53, 0.55, 0.56, 0.59, 0.63, 0.68, 0.77, 0.89, 1.10]) / 100
SKAO_SIG_H  = np.array([0.92, 0.81, 0.80, 0.79, 0.80, 0.82, 0.84, 0.88, 0.94, 1.02, 1.14, 1.32, 1.62]) / 100

# Comoving distance integrand
def chi_integrand(z, E_func):
    return 1.0 / E_func(z)

def compute_DA(z, Om, h, E_func, r_d=147.09):
    """Comoving angular diameter distance D_A(z)/r_d."""
    c_km = 2.998e5  # km/s
    H0 = 100.0 * h  # km/s/Mpc
    chi, _ = quad(chi_integrand, 0, z, args=(E_func,), limit=100)
    DA_Mpc = (c_km / H0) * chi
    return DA_Mpc / r_d

def compute_Hrs(z, h, E_func, r_d=147.09):
    """H(z)*r_d in units of c."""
    c_km = 2.998e5
    H0 = 100.0 * h
    return H0 * E_func(z) * r_d / c_km

# E(z) functions
def E_lcdm(Om):
    OL = 1.0 - Om
    def _E(z):
        return np.sqrt(Om * (1+z)**3 + OL)
    return _E

def E_cpl(Om, w0, wa):
    OL = 1.0 - Om
    def _E(z):
        a = 1.0 / (1.0 + z)
        fde = (1.0 + z)**(3*(1+w0+wa)) * np.exp(-3*wa*(1-a))
        return np.sqrt(Om * (1+z)**3 + OL * fde)
    return _E

def forecast_snr(label, E_func, Om, h, E_lcdm_func, r_d=147.09):
    """Compute SKAO pairwise SNR vs LCDM."""
    DA_model = np.array([compute_DA(z, Om, h, E_func, r_d) for z in SKAO_BINS])
    DA_lcdm  = np.array([compute_DA(z, Om, h, E_lcdm_func, r_d) for z in SKAO_BINS])
    Hr_model = np.array([compute_Hrs(z, h, E_func, r_d) for z in SKAO_BINS])
    Hr_lcdm  = np.array([compute_Hrs(z, h, E_lcdm_func, r_d) for z in SKAO_BINS])

    # Fractional difference
    dDA = (DA_model - DA_lcdm) / DA_lcdm
    dHr = (Hr_model - Hr_lcdm) / Hr_lcdm

    # Per-bin SNR
    snr_DA = dDA / SKAO_SIG_DA
    snr_Hr = dHr / SKAO_SIG_H

    # Total SNR (chi2 sum)
    snr_total = float(np.sqrt(np.sum(snr_DA**2) + np.sum(snr_Hr**2)))

    print('[L7-X3] %s: max|dDA|=%.4f%% max|dH|=%.4f%% total SNR=%.3f' % (
        label, np.max(np.abs(dDA))*100, np.max(np.abs(dHr))*100, snr_total), flush=True)

    return {
        'DA_model': DA_model.tolist(),
        'DA_lcdm': DA_lcdm.tolist(),
        'Hr_model': Hr_model.tolist(),
        'Hr_lcdm': Hr_lcdm.tolist(),
        'snr_DA_per_bin': snr_DA.tolist(),
        'snr_Hr_per_bin': snr_Hr.tolist(),
        'total_snr': snr_total,
        'distinguishable_2sigma': snr_total > 2.0,
        'z_bins': SKAO_BINS.tolist(),
    }

def main():
    print('[L7-X3] SKAO 21cm BAO forecast vs SQMH E(z)', flush=True)
    print('[L7-X3] Using SKA SWG Bacon+2020 sensitivity (MID Band 1+2, optimistic)', flush=True)

    r_d = 147.09  # Mpc (Planck 2018)

    # LCDM reference (SQMH Om, h)
    Om_sqmh = 0.3095; h_sqmh = 0.6776
    E_lcdm_sqmh = E_lcdm(Om_sqmh)

    candidates = [
        ('C11D', E_cpl(Om_sqmh, -0.877, -0.186), Om_sqmh, h_sqmh),
        ('A12',  E_cpl(Om_sqmh, -0.886, -0.133), Om_sqmh, h_sqmh),
        ('C28',  E_cpl(0.3081,  -0.849, -0.242), 0.3081,  0.6789),
    ]

    results = {}
    for label, E_func, Om, h in candidates:
        results[label] = forecast_snr(label, E_func, Om, h, E_lcdm_sqmh, r_d=r_d)

    # DESI DR3 comparison (additional context)
    print('\n[L7-X3] SKAO vs DESI DR3 context:', flush=True)
    for label, r in results.items():
        snr = r['total_snr']
        print('[L7-X3]   %s: SKAO SNR=%.2f (%s)' % (
            label, snr, '2sigma DIST' if r['distinguishable_2sigma'] else 'indistinct'), flush=True)

    out = {
        'phase': 'L7-X3',
        'method': 'SKAO_MID_Band12_Fisher_forecast',
        'reference': 'Bacon+2020 (SKA SWG), optimistic scenario',
        'r_d_Mpc': r_d,
        'z_bins': SKAO_BINS.tolist(),
        'sigma_DA_frac': SKAO_SIG_DA.tolist(),
        'sigma_Hr_frac': SKAO_SIG_H.tolist(),
        'results': results,
    }
    out_path = os.path.join(_HERE, 'skao_forecast.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, default=lambda x: float(x) if isinstance(x, np.floating) else x)
    print('\n[L7-X3] Done. Saved to %s' % out_path, flush=True)

if __name__ == '__main__':
    main()
