# -*- coding: utf-8 -*-
"""
EE2 Plotting Module (Run 16)
H(z), w_DE(z), delta-E/E_LCDM plots

CLAUDE.md: print() ASCII only, matplotlib labels OK for unicode.
numpy 2.x: trapezoid (not trapz).
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')  # headless FIRST, before any other matplotlib import
import matplotlib.pyplot as plt

_THIS = os.path.dirname(os.path.abspath(__file__))
_SIMS = os.path.dirname(_THIS)
if _SIMS not in sys.path:
    sys.path.insert(0, _SIMS)

from l19.ee2_ode import solve_ee2, E_LCDM, A_EE2, B_EE2, OL0_EE2
from l19.ee2_ode import OMEGA_M_FID, OMEGA_R_FID, H0_KMS


def plot_all(out_dir=None, show=False):
    if out_dir is None:
        out_dir = _THIS

    # ── z grids ──────────────────────────────────────────────────────────────
    z_full  = np.linspace(0.0, 3.0, 600)   # H(z), delta-E plot
    z_wide  = np.linspace(0.0, 4.0, 800)   # w_DE plot (wider range)

    # ── Solve ─────────────────────────────────────────────────────────────────
    _, E_ee2_full, w_ee2_full = solve_ee2(z_arr=z_full)
    _, E_ee2_wide, w_ee2_wide = solve_ee2(z_arr=z_wide)
    E_lcdm_full = E_LCDM(z_full, OMEGA_M_FID, OMEGA_R_FID)
    E_lcdm_wide = E_LCDM(z_wide, OMEGA_M_FID, OMEGA_R_FID)

    H_ee2  = H0_KMS * E_ee2_full
    H_lcdm = H0_KMS * E_lcdm_full

    delta_E = (E_ee2_full - E_lcdm_full) / E_lcdm_full * 100.0

    # ── Figure 1: H(z) ───────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(z_full, H_ee2,  'b-',  lw=2,   label='EE2 (ODE)')
    ax.plot(z_full, H_lcdm, 'k--', lw=1.5, label=r'$\Lambda$CDM')
    ax.set_xlabel('z', fontsize=13)
    ax.set_ylabel(r'$H(z)$ [km s$^{-1}$ Mpc$^{-1}$]', fontsize=13)
    ax.set_title(r'EE2 vs $\Lambda$CDM: Hubble parameter', fontsize=13)
    ax.legend(fontsize=11)
    ax.set_xlim(0, 3)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out1 = os.path.join(out_dir, 'ee2_Hz.png')
    fig.savefig(out1, dpi=150)
    plt.close(fig)
    print(f"Saved: {out1}")

    # ── Figure 2: w_DE(z) ────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(z_wide, w_ee2_wide, 'r-', lw=2, label=r'$\omega_\mathrm{DE}$ EE2')
    ax.axhline(-1.0,    color='k',   lw=1.0, ls='--', label=r'$w=-1$ (LCDM)')
    ax.axhline(OL0_EE2*(1+2*A_EE2), color='gray', lw=1.0, ls=':',
               label=rf'$w_\min={OL0_EE2*(1+2*A_EE2):.4f}$')
    ax.set_xlabel('z', fontsize=13)
    ax.set_ylabel(r'$\omega_\mathrm{DE}$', fontsize=13)
    ax.set_title(r'EE2 equation of state $\omega_\mathrm{DE}(z)$', fontsize=13)
    ax.legend(fontsize=11)
    ax.set_xlim(0, 4)
    ax.set_ylim(-1.25, -0.85)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out2 = os.path.join(out_dir, 'ee2_wz.png')
    fig.savefig(out2, dpi=150)
    plt.close(fig)
    print(f"Saved: {out2}")

    # ── Figure 3: delta E/E_LCDM ─────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(z_full, delta_E, 'g-', lw=2)
    ax.axhline(0, color='k', lw=1.0, ls='--')
    ax.set_xlabel('z', fontsize=13)
    ax.set_ylabel(r'$(E_\mathrm{EE2}-E_\mathrm{LCDM})/E_\mathrm{LCDM}$ [%]', fontsize=13)
    ax.set_title(r'EE2 deviation from $\Lambda$CDM', fontsize=13)
    ax.set_xlim(0, 2)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out3 = os.path.join(out_dir, 'ee2_deltaE.png')
    fig.savefig(out3, dpi=150)
    plt.close(fig)
    print(f"Saved: {out3}")

    # ── Summary stats ────────────────────────────────────────────────────────
    print()
    print("EE2 Summary (ODE solver)")
    print(f"  A = {A_EE2:.5f}, B = {B_EE2:.4f}, OL0 = {OL0_EE2}")
    print(f"  w_DE(z=0) = {w_ee2_full[0]:.4f}")
    print(f"  w_DE min  = {w_ee2_full.min():.4f}")
    print(f"  max |delta_E| over z=[0,2] = {np.abs(delta_E[z_full<=2]).max():.3f}%")


if __name__ == '__main__':
    plot_all()
