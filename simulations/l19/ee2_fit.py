# -*- coding: utf-8 -*-
"""
ee2_fit.py  --  EE2 Dark Energy BAO Fitting (Run 19 / L19)
===========================================================
EE2 formula:
    w_DE = OL0 * (1 + A * (1 - cos(B * ln(H/H0))))
    A   = 2*exp(-pi)   ~ 0.08643
    B   = 2*pi/ln2     ~ 9.0647
    OL0 = -1.0  (fixed)

NOTE: H_ref = H0  (EE2 equation of state uses H/H0 as oscillation argument.
      H0 is BOTH the fitting parameter and the normalization reference.)

Fixed parameters:
    r_s = 147.09 Mpc  (Planck 2018 sound horizon, BAO standard ruler)
    A, B, OL0         (EE2 theoretical values, no tuning)

Free parameters (optimized):
    Omega_m   -- matter density (dimensionless)
    H0        -- Hubble constant [km/s/Mpc]

BAO theory:
    D_H(z) = c / (H0 * E(z))              [Mpc]
    D_M(z) = (c/H0) * int_0^z dz'/E(z')  [Mpc]
    D_V(z) = (z * D_M^2 * D_H)^(1/3)     [Mpc]
    Data:    D_X / r_s  (dimensionless)

chi2 = Delta^T @ C_inv @ Delta  (full 13x13 covariance matrix)
AICc = chi2 + 2k + 2k(k+1)/(n-k-1),  k=2, n=13

Output files:
    ee2_fit_Hz.png        -- H(z) ratio EE2 vs LCDM
    ee2_fit_wz.png        -- w_DE(z) EE2 equation of state
    ee2_fit_residuals.png -- DESI DR2 BAO residuals (both models)

Team: 8-person design review, L19 Round 1-8 (2026-04-13)

CLAUDE.md compliance:
- ODE solver: ee2_ode.solve_ee2 (DOP853 forward-shooting)
- Full covariance matrix (no D_V-only fitting)
- D_H = c/(H0*E(z)) in Mpc, no double unit conversion
- numpy.trapezoid / scipy cumulative_trapezoid (numpy 2.x safe)
- ASCII only in print()
"""

import os
import sys
import math
import warnings

import numpy as np
import matplotlib
matplotlib.use('Agg')   # headless -- must come before any matplotlib imports
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import minimize

warnings.filterwarnings('ignore')

# Thread-safety for multiprocessing workers
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
np.seterr(all='ignore')

# ── Import paths ────────────────────────────────────────────────────────────────
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SIM_DIR    = os.path.dirname(_SCRIPT_DIR)   # simulations/

if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

from desi_data import DESI_DR2, DESI_DR2_COV, DESI_DR2_COV_INV
from ee2_ode   import (solve_ee2, E_LCDM,
                        A_EE2, B_EE2, OL0_EE2,
                        OMEGA_M_FID, OMEGA_R_FID, H0_KMS)

# ── Physical constants ──────────────────────────────────────────────────────────
C_KMS  = 299792.458    # speed of light [km/s]
R_S    = 147.09        # Planck 2018 BAO standard ruler [Mpc]  (fixed)
OR     = OMEGA_R_FID   # radiation density (fixed)

# ── EE2 fixed parameters ────────────────────────────────────────────────────────
# A = 2*exp(-pi), B = 2*pi/ln2, OL0 = -1 are all theory-determined.
# H_ref = H0  (the same H0 that is a free fitting parameter)

N_DATA = 13   # DESI DR2 data points
N_GRID = 4000 # integration grid resolution


# ═══════════════════════════════════════════════════════════════════════════════
# BAO DISTANCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def compute_E_grid(Omega_m, z_grid, mode='lcdm'):
    """
    Compute E(z) = H(z)/H0 on z_grid.

    Parameters
    ----------
    Omega_m : float
        Matter density parameter (dimensionless)
    z_grid  : ndarray
        Redshift grid (must start at or near 0)
    mode    : 'lcdm' | 'ee2'

    Returns
    -------
    E_grid : ndarray or None
        E(z) values; None on solver failure
    """
    if mode == 'lcdm':
        OL = 1.0 - Omega_m - OR
        if OL < -0.5:
            return None
        E2 = (OR * (1 + z_grid)**4
              + Omega_m * (1 + z_grid)**3
              + OL)
        E2 = np.maximum(E2, 1e-30)
        return np.sqrt(E2)

    elif mode == 'ee2':
        # NOTE: H_ref = H0 inside solve_ee2 (the ODE uses ln(E) = ln(H/H0))
        _, E_full, _ = solve_ee2(
            A=A_EE2, B=B_EE2, OL0=OL0_EE2,
            Omega_m=Omega_m, Omega_r=OR,
            z_arr=z_grid,
        )
        return E_full  # None if solver failed

    return None


def compute_theory_vector(Omega_m, H0, mode='lcdm'):
    """
    Compute theoretical BAO distance vector for DESI DR2 data points.

    D_H(z) = c / (H0 * E(z))                     [Mpc]
    D_M(z) = (c/H0) * int_0^z dz'/E(z')          [Mpc]
    D_V(z) = (z * D_M^2 * D_H)^(1/3)             [Mpc]
    theory_i = D_X(z_i) / r_s                    (dimensionless)

    Parameters
    ----------
    Omega_m : float
    H0      : float  [km/s/Mpc]
    mode    : 'lcdm' | 'ee2'

    Returns
    -------
    theory_vec : ndarray of shape (13,) or None
    """
    z_eff = DESI_DR2['z_eff']
    z_max = z_eff.max() + 0.01
    z_grid = np.linspace(0.0, z_max, N_GRID)

    E_grid = compute_E_grid(Omega_m, z_grid, mode)
    if E_grid is None:
        return None

    inv_E = 1.0 / np.maximum(E_grid, 1e-15)

    # Cumulative comoving distance: D_M = (c/H0) * int_0^z dz'/E(z')
    # scipy cumulative_trapezoid returns shape (N_GRID-1,); prepend 0 at z=0
    DM_cum = (C_KMS / H0) * np.concatenate(
        [[0.0], cumulative_trapezoid(inv_E, z_grid)]
    )

    theory_vec = np.empty(N_DATA)
    for i, (z, qty) in enumerate(zip(z_eff, DESI_DR2['quantity'])):
        idx = min(np.searchsorted(z_grid, z), N_GRID - 1)
        E_z = E_grid[idx]
        DH  = C_KMS / (H0 * E_z)          # [Mpc]
        DM  = DM_cum[idx]                  # [Mpc]
        DV  = (z * DM**2 * DH)**(1.0/3.0) if z > 0 else 0.0

        if   'DV' in qty:
            theory_vec[i] = DV / R_S
        elif 'DM' in qty:
            theory_vec[i] = DM / R_S
        elif 'DH' in qty:
            theory_vec[i] = DH / R_S
        else:
            theory_vec[i] = np.nan

    return theory_vec


# ═══════════════════════════════════════════════════════════════════════════════
# CHI-SQUARED
# ═══════════════════════════════════════════════════════════════════════════════

def chi2(Omega_m, H0, mode='lcdm'):
    """
    Full chi2 using 13x13 inverse covariance matrix (DESI DR2).

    chi2 = Delta^T C_inv Delta,  Delta = data - theory
    """
    if not (0.05 < Omega_m < 0.70 and 50.0 < H0 < 100.0):
        return 1e8
    th = compute_theory_vector(Omega_m, H0, mode)
    if th is None or not np.all(np.isfinite(th)):
        return 1e8
    delta = DESI_DR2['value'] - th
    return float(delta @ DESI_DR2_COV_INV @ delta)


def chi2_wrapper(params, mode='lcdm'):
    return chi2(params[0], params[1], mode)


# ═══════════════════════════════════════════════════════════════════════════════
# AICC
# ═══════════════════════════════════════════════════════════════════════════════

def aicc(chi2_val, k, n=N_DATA):
    """
    Corrected Akaike Information Criterion.
    AICc = chi2 + 2k + 2k(k+1)/(n-k-1)
    """
    return chi2_val + 2*k + 2*k*(k+1)/(n - k - 1)


# ═══════════════════════════════════════════════════════════════════════════════
# OPTIMIZATION
# ═══════════════════════════════════════════════════════════════════════════════

def optimize_model(mode='lcdm', verbose=False):
    """
    Multi-start Nelder-Mead optimization of chi2.

    Returns
    -------
    (Om_best, H0_best, chi2_best)
    """
    starts = [
        [0.315, 67.4],
        [0.30,  68.0],
        [0.32,  69.0],
        [0.29,  70.0],
        [0.31,  68.5],
        [0.28,  71.0],
    ]
    best = (1e8, None, None)

    for s in starts:
        try:
            res = minimize(
                chi2_wrapper, s, args=(mode,),
                method='Nelder-Mead',
                options={'xatol': 1e-5, 'fatol': 1e-5, 'maxiter': 3000},
            )
            if res.fun < best[0]:
                best = (res.fun, res.x[0], res.x[1])
        except Exception:
            continue

    if best[1] is None:
        return OMEGA_M_FID, H0_KMS, 1e8
    return best[1], best[2], best[0]


# ═══════════════════════════════════════════════════════════════════════════════
# PLOTTING
# ═══════════════════════════════════════════════════════════════════════════════

def plot_Hz(Om_ee2, H0_ee2, Om_lcdm, H0_lcdm, outfile):
    """H(z) comparison plot (2-panel: absolute + ratio)."""
    z_arr = np.linspace(0, 3.0, 800)
    _, E_ee2_arr, _ = solve_ee2(A=A_EE2, B=B_EE2, OL0=OL0_EE2,
                                  Omega_m=Om_ee2, Omega_r=OR, z_arr=z_arr)
    E_lcdm_arr = E_LCDM(z_arr, Omega_m=Om_lcdm, Omega_r=OR)

    H_ee2  = H0_ee2  * E_ee2_arr
    H_lcdm = H0_lcdm * E_lcdm_arr

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 9),
                                    gridspec_kw={'height_ratios': [2, 1]})
    fig.suptitle('H(z) Comparison: EE2 vs LCDM (DESI DR2 Best-Fit)',
                 fontsize=13, fontweight='bold')

    ax1.plot(z_arr, H_ee2,  'b-',  lw=2.0,
             label=f'EE2  ($\\Omega_m$={Om_ee2:.3f}, $H_0$={H0_ee2:.2f})')
    ax1.plot(z_arr, H_lcdm, 'r--', lw=2.0,
             label=f'LCDM ($\\Omega_m$={Om_lcdm:.3f}, $H_0$={H0_lcdm:.2f})')
    ax1.set_ylabel('H(z) [km/s/Mpc]', fontsize=12)
    ax1.set_xlim(0, 3)
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.set_title('Best-fit to DESI DR2 BAO (13 points, full covariance)',
                  fontsize=10)

    ratio = H_ee2 / H_lcdm - 1.0
    ax2.plot(z_arr, ratio * 100, 'b-', lw=1.5)
    ax2.axhline(0, color='r', ls='--', lw=1)
    ax2.set_xlabel('Redshift z', fontsize=12)
    ax2.set_ylabel('$(H_{EE2}/H_{LCDM} - 1)\\times 100$ [%]', fontsize=11)
    ax2.set_xlim(0, 3)
    ax2.grid(True, alpha=0.3)
    ax2.set_title('Relative deviation from LCDM', fontsize=10)

    plt.tight_layout()
    plt.savefig(outfile, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'Saved: {outfile}')


def plot_wz(Om_ee2, H0_ee2, outfile):
    """w_DE(z) equation of state plot."""
    z_arr = np.linspace(0, 3.0, 800)
    _, _, w_arr = solve_ee2(A=A_EE2, B=B_EE2, OL0=OL0_EE2,
                             Omega_m=Om_ee2, Omega_r=OR, z_arr=z_arr)

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.suptitle('EE2 Dark Energy Equation of State $\\omega_{DE}(z)$',
                 fontsize=13, fontweight='bold')

    ax.plot(z_arr, w_arr, 'b-', lw=2.0, label='EE2 $\\omega_{DE}(z)$')
    ax.axhline(-1.0, color='r', ls='--', lw=1.5, label='LCDM $\\omega=-1$')
    ax.fill_between(z_arr, -1.02, -0.98, color='r', alpha=0.1,
                    label='LCDM $\\pm$2%')
    w_min = OL0_EE2 * (1 + 2 * A_EE2)
    ax.axhline(w_min, color='gray', ls=':', lw=1.2,
               label=f'$\\omega_{{min}}$ = {w_min:.4f}')

    ax.set_xlabel('Redshift z', fontsize=12)
    ax.set_ylabel('$\\omega_{DE}(z)$', fontsize=12)
    ax.set_xlim(0, 3)
    ax.set_ylim(-1.30, -0.70)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    ann = (f'A = 2exp(-pi) = {A_EE2:.5f}\n'
           f'B = 2pi/ln2 = {B_EE2:.5f}\n'
           f'H_ref = H0 (EE2 normalization)\n'
           f'$\\Omega_m$ = {Om_ee2:.4f},  $H_0$ = {H0_ee2:.3f}')
    ax.text(0.62, 0.05, ann, transform=ax.transAxes, fontsize=9,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.tight_layout()
    plt.savefig(outfile, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'Saved: {outfile}')


def plot_residuals(Om_ee2, H0_ee2, Om_lcdm, H0_lcdm,
                   chi2_ee2_v, chi2_lcdm_v, outfile):
    """DESI DR2 BAO residuals comparison (both models, 2-panel)."""
    th_ee2  = compute_theory_vector(Om_ee2,  H0_ee2,  'ee2')
    th_lcdm = compute_theory_vector(Om_lcdm, H0_lcdm, 'lcdm')

    data     = DESI_DR2['value']
    sig      = DESI_DR2['sigma']
    z_eff    = DESI_DR2['z_eff']
    qty_list = DESI_DR2['quantity']

    res_ee2  = (data - th_ee2)  / sig
    res_lcdm = (data - th_lcdm) / sig

    colors  = {'DV_over_rs': 'green',
               'DM_over_rs': 'steelblue',
               'DH_over_rs': 'darkorange'}
    markers = {'DV_over_rs': 'D',
               'DM_over_rs': 'o',
               'DH_over_rs': 's'}
    labels  = {'DV_over_rs': '$D_V/r_s$',
               'DM_over_rs': '$D_M/r_s$',
               'DH_over_rs': '$D_H/r_s$'}

    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    fig.suptitle('DESI DR2 BAO Residuals: EE2 vs LCDM Best-Fit',
                 fontsize=13, fontweight='bold')

    n, k = N_DATA, 2
    for ax, res_arr, model_name, chi2v in [
        (axes[0], res_ee2,  'EE2',  chi2_ee2_v),
        (axes[1], res_lcdm, 'LCDM', chi2_lcdm_v),
    ]:
        seen = set()
        for i in range(N_DATA):
            q   = qty_list[i]
            lab = labels[q] if q not in seen else None
            seen.add(q)
            ax.errorbar(z_eff[i], res_arr[i], yerr=1.0,
                        fmt=markers[q], color=colors[q],
                        ms=8, lw=1.5, label=lab, capsize=4)

        ax.axhline(0,  color='k',    ls='-',  lw=0.8)
        ax.axhline(+1, color='gray', ls=':',  lw=0.8)
        ax.axhline(-1, color='gray', ls=':',  lw=0.8)
        ax.set_ylabel('(data - theory) / sigma', fontsize=11)
        AICc_v = aicc(chi2v, k, n)
        ax.set_title(f'{model_name} best-fit  chi2={chi2v:.3f}  AICc={AICc_v:.3f}',
                     fontsize=11)
        ax.legend(fontsize=9, loc='upper right')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-3.5, 3.5)

    axes[1].set_xlabel('Redshift z', fontsize=12)
    plt.tight_layout()
    plt.savefig(outfile, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'Saved: {outfile}')


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    OUT_DIR = _SCRIPT_DIR

    print('=' * 60)
    print('EE2 Dark Energy BAO Fitting -- L19')
    print('=' * 60)
    print()
    print('EE2 fixed parameters:')
    print(f'  A   = 2*exp(-pi) = {A_EE2:.6f}')
    print(f'  B   = 2*pi/ln2  = {B_EE2:.6f}')
    print(f'  OL0 = {OL0_EE2}')
    print(f'  r_s = {R_S} Mpc  (Planck 2018, fixed)')
    print()
    print('H_ref = H0  (EE2 uses H/H0; H0 is both fitting param and ref)')
    print()
    print('Free parameters: Omega_m, H0')
    print(f'Data: DESI DR2, n={N_DATA}, full {N_DATA}x{N_DATA} covariance')
    print()

    # ── Optimize EE2 ──────────────────────────────────────────────────────────
    print('Optimizing EE2 (multi-start Nelder-Mead)...')
    Om_ee2, H0_ee2, chi2_ee2 = optimize_model('ee2', verbose=True)
    AICc_ee2 = aicc(chi2_ee2, k=2)
    print(f'  Omega_m = {Om_ee2:.5f}')
    print(f'  H0      = {H0_ee2:.4f} km/s/Mpc')
    print(f'  chi2    = {chi2_ee2:.5f}')
    print(f'  AICc    = {AICc_ee2:.5f}  (k=2, n={N_DATA})')
    print()

    # ── Optimize LCDM ─────────────────────────────────────────────────────────
    print('Optimizing LCDM (multi-start Nelder-Mead)...')
    Om_lcdm, H0_lcdm, chi2_lcdm = optimize_model('lcdm', verbose=True)
    AICc_lcdm = aicc(chi2_lcdm, k=2)
    print(f'  Omega_m = {Om_lcdm:.5f}')
    print(f'  H0      = {H0_lcdm:.4f} km/s/Mpc')
    print(f'  chi2    = {chi2_lcdm:.5f}')
    print(f'  AICc    = {AICc_lcdm:.5f}  (k=2, n={N_DATA})')
    print()

    # ── Fixed-parameter reference (Planck 2018 priors) ────────────────────────
    chi2_ee2_fixed  = chi2(OMEGA_M_FID, H0_KMS, 'ee2')
    chi2_lcdm_fixed = chi2(OMEGA_M_FID, H0_KMS, 'lcdm')
    print('Reference chi2 (Omega_m=0.315, H0=67.4 fixed):')
    print(f'  chi2(EE2  fixed) = {chi2_ee2_fixed:.4f}')
    print(f'  chi2(LCDM fixed) = {chi2_lcdm_fixed:.4f}')
    print()

    # ── AICc comparison ───────────────────────────────────────────────────────
    dAICc = AICc_ee2 - AICc_lcdm
    print('=== AICc Summary ===')
    print(f'  AICc(EE2)        = {AICc_ee2:.4f}')
    print(f'  AICc(LCDM)       = {AICc_lcdm:.4f}')
    print(f'  Delta_AICc       = {dAICc:.4f}  (EE2 - LCDM)')
    print(f'  Delta_chi2       = {chi2_ee2 - chi2_lcdm:.4f}')
    print()
    if dAICc > 6:
        print('  Verdict: LCDM strongly preferred over EE2 by DESI DR2 BAO')
    elif dAICc > 2:
        print('  Verdict: LCDM moderately preferred over EE2')
    elif dAICc > 0:
        print('  Verdict: LCDM slightly preferred; EE2 not ruled out')
    else:
        print('  Verdict: EE2 preferred over LCDM')
    print()

    # ── Per-point residuals ───────────────────────────────────────────────────
    th_ee2  = compute_theory_vector(Om_ee2,  H0_ee2,  'ee2')
    th_lcdm = compute_theory_vector(Om_lcdm, H0_lcdm, 'lcdm')
    sig     = DESI_DR2['sigma']
    data    = DESI_DR2['value']
    print('Per-point residuals (sigma units):')
    hdr = f"{'i':>2} {'z':>5} {'quantity':>12} {'data':>10} {'EE2':>10} {'LCDM':>10} {'res_EE2':>8} {'res_LCDM':>9}"
    print(hdr)
    print('-' * len(hdr))
    for i in range(N_DATA):
        z   = DESI_DR2['z_eff'][i]
        qty = DESI_DR2['quantity'][i]
        d   = data[i]
        e2  = th_ee2[i]
        lc  = th_lcdm[i]
        s   = sig[i]
        print(f'{i:>2} {z:>5.3f} {qty:>12s} {d:>10.5f} {e2:>10.5f} {lc:>10.5f} '
              f'{(d-e2)/s:>8.3f} {(d-lc)/s:>9.3f}')
    print()

    # ── Generate plots ────────────────────────────────────────────────────────
    print('Generating plots...')
    plot_Hz(Om_ee2, H0_ee2, Om_lcdm, H0_lcdm,
            os.path.join(OUT_DIR, 'ee2_fit_Hz.png'))
    plot_wz(Om_ee2, H0_ee2,
            os.path.join(OUT_DIR, 'ee2_fit_wz.png'))
    plot_residuals(Om_ee2, H0_ee2, Om_lcdm, H0_lcdm,
                   chi2_ee2, chi2_lcdm,
                   os.path.join(OUT_DIR, 'ee2_fit_residuals.png'))
    print()
    print('=== ee2_fit.py complete ===')


if __name__ == '__main__':
    main()
