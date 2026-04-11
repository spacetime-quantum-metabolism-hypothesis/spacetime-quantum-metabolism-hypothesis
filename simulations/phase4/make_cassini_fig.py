# -*- coding: utf-8 -*-
"""
Phase 3.6 B2.4 -- figures/14_cassini.png

Vainshtein pass/fail plot. x: source mass (kg), y: Vainshtein radius (m).
Overlay Cassini / LLR / lab-scale reference distances.
"""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..')))
from vainshtein import (r_vainshtein, schwarzschild_radius, suppression_factor,
                        M_SUN, M_EARTH, M_WD, AU, PARSEC, R_CASSINI)


def main():
    M_arr = np.logspace(20, 45, 200)  # kg
    rV = np.array([r_vainshtein(M) for M in M_arr])

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

    # --- Panel 1: r_V vs M ---
    ax = axes[0]
    ax.loglog(M_arr, rV / PARSEC, 'b-', lw=2, label=r'$r_V$ (cubic Galileon)')
    for name, M, color in [("Earth", M_EARTH, 'green'),
                            ("Sun", M_SUN, 'orange'),
                            ("WD", M_WD, 'red'),
                            ("MW", 1.5e12 * M_SUN, 'purple')]:
        rVp = r_vainshtein(M) / PARSEC
        ax.plot(M, rVp, 'o', color=color, markersize=10, label=name)
    ax.axhline(R_CASSINI / PARSEC, color='k', linestyle='--',
               label='Cassini dist (8 AU)')
    ax.set_xlabel('Source mass [kg]')
    ax.set_ylabel(r'$r_V$ [pc]')
    ax.set_title(r'Vainshtein radius for $M^4 = M_{\rm Pl}^2 H_0^2$')
    ax.legend(loc='lower right', fontsize=8)
    ax.grid(alpha=0.3)

    # --- Panel 2: suppression factor ---
    ax = axes[1]
    r_test = np.logspace(-3, 20, 300)  # meters (from lab to Mpc)
    rV_sun = r_vainshtein(M_SUN)
    S = np.array([suppression_factor(r, rV_sun) for r in r_test])
    ax.loglog(r_test / AU, S, 'b-', lw=2,
              label=r'$(r/r_V)^{3/2}$, Sun')
    ax.axvline(R_CASSINI / AU, color='orange', linestyle='--',
               label='Cassini r ~ 8 AU')
    ax.axhline(1.02e-3, color='red', linestyle=':',
               label='Required to pass Cassini')
    ax.set_xlabel('Distance from Sun [AU]')
    ax.set_ylabel(r'Fifth-force suppression')
    ax.set_title('Cubic Galileon suppression profile (Sun)')
    ax.legend(loc='lower right', fontsize=9)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    out = os.path.abspath(os.path.join(HERE, '..', '..', 'figures',
                                        '14_cassini.png'))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    plt.savefig(out, dpi=150, bbox_inches='tight')
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
