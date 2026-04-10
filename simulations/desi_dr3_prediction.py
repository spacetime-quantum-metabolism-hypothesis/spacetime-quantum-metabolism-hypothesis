"""
Simulation 7: DESI DR3 Pre-diction (SQMH)

SQMH ROBUST predictions (model-independent):
1. w >= -1 always (NO phantom crossing) — from sigma*n*rho_m >= 0
2. Quadratic IDE form (Q ~ rho_DE * rho_m) — from 2-body mass action law
3. w0 > -1 — nonzero coupling at z=0

SQMH LEADING-ORDER predictions (may change with full V(phi) dynamics):
4. wa > 0 at leading order (w increases with z);
   wa < 0 requires V(phi) damping (base.md XVI.6).

DESI DR2 BAO fitting result:
  - SQMH-physical (xi_q>0) at Planck r_d: no improvement over LCDM
  - SQMH-physical (xi_q>0) + r_d free: Delta-chi2 = -4.83 (xi_q=0.04, r_d=149.8)
  - Only xi_q < 0 (phantom, non-SQMH) improves at fixed r_d

Key: publish BEFORE DR3 release (late 2026-2027).
"""
import numpy as np
import matplotlib.pyplot as plt
import config
import dark_energy_w as dew


def plot_dr3_prediction():
    # Both signs for completeness
    xi_values = [-0.05, 0.0, 0.04, 0.1, 0.2, 0.5]
    colors = ['#9C27B0', 'black', '#E91E63', '#4CAF50', '#FF9800', '#F44336']
    styles = [':', '-', '-', '--', '--', '--']

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # --- Panel 1: w(z) ---
    ax = axes[0, 0]
    results = {}
    for xi_q, col, ls in zip(xi_values, colors, styles):
        z, w, Om, Ode = dew.compute_w_eff(xi_q, z_max=3.0)
        w0, wa = dew.fit_cpl(z, w)
        results[xi_q] = (w0, wa, z, w)

        if xi_q == 0:
            lbl = 'LCDM'
        elif xi_q == 0.04:
            lbl = f'xi={xi_q} (DESI best-fit)'
        elif xi_q < 0:
            lbl = f'xi={xi_q} (phantom)'
        else:
            lbl = f'xi={xi_q}'
        ax.plot(z, w, color=col, lw=2 if xi_q in [0, 0.04] else 1.5, ls=ls, label=lbl)

    ax.axhline(-1, color='red', ls='-', lw=1.5, alpha=0.5)
    ax.axhspan(-1.2, -1.0, alpha=0.06, color='red')
    ax.set_xlabel('Redshift z')
    ax.set_ylabel('$w_{eff}(z)$')
    ax.set_title('SQMH $w(z)$ Prediction for DR3')
    ax.legend(fontsize=7)
    ax.set_ylim(-1.1, -0.5)

    # --- Panel 2: w0-wa plane ---
    ax = axes[0, 1]

    # DESI DR2 (DESI+CMB+SN combined)
    desi_w0, desi_wa = -0.752, -1.27
    desi_w0_err, desi_wa_err = 0.058, 0.37
    rho_corr = -0.8
    theta = np.linspace(0, 2*np.pi, 200)
    for nsig, alp in [(1, 0.2), (2, 0.08)]:
        cos_t, sin_t = np.cos(theta), np.sin(theta)
        x_ell = nsig * desi_w0_err * cos_t
        y_ell = nsig * desi_wa_err * (rho_corr * cos_t + np.sqrt(1 - rho_corr**2) * sin_t)
        ax.fill(desi_w0 + x_ell, desi_wa + y_ell, alpha=alp, color='blue')
    ax.text(desi_w0 + 0.08, desi_wa + 0.4, 'DESI DR2\n(+CMB+SN)', fontsize=7, color='blue')

    # SQMH physical trajectory
    xi_phys = [x for x in xi_values if x > 0]
    w0_list = [results[x][0] for x in xi_phys]
    wa_list = [results[x][1] for x in xi_phys]
    ax.plot(w0_list, wa_list, 'g-o', ms=8, lw=2, label='SQMH (xi>0)', zorder=5)
    for xi_q in xi_phys:
        w0, wa = results[xi_q][:2]
        ax.annotate(f'xi={xi_q}', (w0, wa), fontsize=7,
                    textcoords="offset points", xytext=(5, 5))

    # Non-physical (phantom)
    for xi_q in [x for x in xi_values if x < 0]:
        w0, wa = results[xi_q][:2]
        ax.plot(w0, wa, 'x', color='#9C27B0', ms=10, mew=2)

    ax.plot(-1, 0, 'k+', ms=15, mew=3, label='LCDM')
    ax.axvline(-1, color='red', ls='-', lw=1, alpha=0.4)
    ax.axhline(0, color='gray', ls=':', alpha=0.3)
    ax.axvspan(-1.5, -1.0, alpha=0.05, color='red')
    ax.set_xlabel('$w_0$')
    ax.set_ylabel('$w_a$')
    ax.set_title('$w_0$-$w_a$: SQMH vs DESI DR2')
    ax.legend(fontsize=7)
    ax.set_xlim(-1.2, -0.3)
    ax.set_ylim(-2.5, 1.5)

    # --- Panel 3: Phantom crossing test ---
    ax = axes[1, 0]
    for xi_q, col, ls in zip(xi_values, colors, styles):
        if xi_q == 0:
            continue
        z, w = results[xi_q][2], results[xi_q][3]
        lbl = f'xi={xi_q}'
        ax.plot(z, w + 1, color=col, lw=2, ls=ls, label=lbl)

    ax.axhline(0, color='red', ls='-', lw=2, label='phantom divide')
    ax.axhspan(-0.15, 0, alpha=0.1, color='red')
    ax.set_xlabel('Redshift z')
    ax.set_ylabel('$w(z) + 1$')
    ax.set_title('Phantom crossing test: SQMH requires $w+1 \\geq 0$')
    ax.legend(fontsize=7)
    ax.set_ylim(-0.1, 0.5)

    # --- Panel 4: Prediction summary ---
    ax = axes[1, 1]
    ax.axis('off')
    lines = [
        "SQMH Pre-dictions for DESI DR3",
        "=" * 42,
        "",
        "ROBUST (xi_q > 0, model-independent):",
        "  1. w >= -1 always (no phantom crossing)",
        "  2. Q ~ rho_DE * rho_m (quadratic IDE)",
        "  3. w0 > -1",
        "",
        "LEADING ORDER (V(phi) correction TBD):",
        "  4. wa > 0 (2-body leading order)",
        "     wa < 0 needs V(phi) damping",
        "",
        "DESI DR2 BAO RESULT:",
        "  xi_q>0 + Planck r_d: Delta-chi2 = 0",
        "  xi_q>0 + free r_d:   Delta-chi2 = -4.83",
        "  (xi_q=0.04, r_d=149.8 Mpc)",
        "",
        "FALSIFICATION:",
        "  w < -1 confirmed  -> SQMH ruled out",
        "  linear IDE better -> form prediction fails",
    ]
    for i, line in enumerate(lines):
        weight = 'bold' if i < 2 else 'normal'
        size = 11 if i < 2 else 8.5
        ax.text(0.02, 0.97 - i * 0.046, line, transform=ax.transAxes,
                fontsize=size, fontweight=weight, fontfamily='monospace',
                verticalalignment='top')

    plt.tight_layout()
    plt.savefig('../figures/12_desi_dr3_prediction.png', dpi=300)
    plt.show()

    print()
    for line in lines:
        print(line)


if __name__ == "__main__":
    print("=" * 60)
    print("SQMH DESI DR3 Pre-diction")
    print("=" * 60)
    plot_dr3_prediction()
