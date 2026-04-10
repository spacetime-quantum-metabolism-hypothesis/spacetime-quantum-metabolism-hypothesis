"""
Simulation 3: Dark Energy Equation of State w(z) from SQMH

SQMH predicts the FUNCTIONAL FORM of dark energy interaction:
  Q = 3H * xi_q * rho_DE * rho_m / rho_crit   (quadratic IDE)

Derived from the two-body mass action law (sigma * n * rho_m).
Coupling strength xi_q fitted — theory predicts quadratic form only.

Results:
  xi_q > 0 (SQMH physical): w0 > -1, wa > 0
  xi_q < 0 (reversed, non-SQMH): w0 < -1 (phantom), wa < 0
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import config


def solve_coupled_de_matter(xi_q, z_max=5.0, N=5000):
    """
    Solve coupled DE-matter evolution with quadratic IDE.

    Variables: omega_m(z), omega_de(z) = rho(z)/rho_crit_0 (physical density)
    E^2(z) = Omega_r*(1+z)^4 + omega_m(z) + omega_de(z)

    Q = 3*H0*xi_q*omega_de*omega_m (quadratic IDE, 2-body mass action)

    d(omega_m)/dz  = 3*omega_m/(1+z) - 3*xi_q*omega_de*omega_m/(E*(1+z))
    d(omega_de)/dz = 3*xi_q*omega_de*omega_m/(E*(1+z))
    """
    def rhs(y, z):
        omega_m, omega_de = y
        omega_de_safe = max(omega_de, 1e-15)
        E2 = config.Omega_r * (1+z)**4 + omega_m + omega_de_safe
        if E2 <= 1e-30:
            return [0, 0]
        E = np.sqrt(E2)

        Q_term = 3.0 * xi_q * omega_de_safe * omega_m / (E * (1+z))

        d_omega_m = 3.0 * omega_m / (1+z) - Q_term
        d_omega_de = Q_term

        return [d_omega_m, d_omega_de]

    z_arr = np.linspace(0, z_max, N)
    y0 = [config.Omega_m, config.Omega_DE]
    sol = odeint(rhs, y0, z_arr, rtol=1e-10, atol=1e-12)

    return z_arr, sol[:, 0], sol[:, 1]


def compute_w_eff(xi_q, z_max=5.0, N=5000):
    """
    Compute effective w(z) from coupled evolution.
    w_eff = -1 + (1+z)/(3*omega_de) * d(omega_de)/dz
    """
    z, Om, Ode = solve_coupled_de_matter(xi_q, z_max, N)

    dOde_dz = np.gradient(Ode, z)

    w = np.full_like(z, -1.0)
    mask = np.abs(Ode) > 1e-30
    w[mask] = -1 + (1 + z[mask]) / (3 * Ode[mask]) * dOde_dz[mask]

    return z, w, Om, Ode


def fit_cpl(z, w):
    """Extract w0, wa from w(z) via least-squares CPL fit over z=[0, 1]."""
    w0 = w[0]
    # Fit wa using w(z) = w0 + wa * z/(1+z) over z in [0, 1]
    mask = (z > 0.01) & (z < 1.0)
    if np.sum(mask) > 5:
        u = z[mask] / (1 + z[mask])
        dw = w[mask] - w0
        # Least-squares: wa = sum(u*dw) / sum(u^2)
        wa = float(np.sum(u * dw) / np.sum(u**2))
    else:
        wa = 0
    return w0, wa


def plot_w_z():
    # Both signs: positive = SQMH physical, negative = reversed (phantom)
    xi_values = [-0.05, 0.0, 0.02, 0.05, 0.1, 0.2]
    colors = ['#9C27B0', 'black', '#2196F3', '#4CAF50', '#FF9800', '#F44336']
    styles = [':', '-', '--', '--', '--', '--']

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    results = {}
    for xi_q, col, ls in zip(xi_values, colors, styles):
        z, w, Om, Ode = compute_w_eff(xi_q)
        w0, wa = fit_cpl(z, w)
        results[xi_q] = (w0, wa)

        if xi_q == 0:
            label = 'LCDM (xi_q=0)'
        elif xi_q < 0:
            label = f'xi_q={xi_q} (reversed, phantom)'
        else:
            label = f'xi_q={xi_q} (SQMH physical)'
        axes[0].plot(z, w, color=col, lw=2, ls=ls, label=label)
        axes[1].plot(z, Ode, color=col, lw=2, ls=ls, label=label)

    # Panel 1: w(z)
    axes[0].axhline(-1, color='red', ls='-', lw=1.5, alpha=0.7, label='phantom divide (w=-1)')
    axes[0].axhspan(-1.3, -1.0, alpha=0.07, color='red')
    axes[0].text(2.5, -1.08, 'phantom\n(w<-1)', fontsize=8, color='red', ha='center')
    axes[0].text(2.5, -0.93, 'SQMH\nallowed', fontsize=8, color='green', ha='center')
    axes[0].set_xlabel('Redshift z')
    axes[0].set_ylabel('$w_{eff}(z)$')
    axes[0].set_title('SQMH: $w_{eff}(z)$ for different coupling strengths')
    axes[0].legend(fontsize=7, loc='upper left')
    axes[0].set_ylim(-1.15, -0.6)
    axes[0].set_xlim(0, 3)

    # Panel 2: omega_de(z)
    axes[1].set_xlabel('Redshift z')
    axes[1].set_ylabel('$\\omega_{DE}(z) = \\rho_{DE}/\\rho_{crit,0}$')
    axes[1].set_title('DE physical density evolution')
    axes[1].legend(fontsize=7)

    # Panel 3: w0-wa plane
    ax = axes[2]

    # DESI DR2 ellipse (DESI+Planck+DES-all combined, NOT BAO-only)
    # Source: arXiv:2503.14738 + arXiv:2507.09981 cross-check
    desi_w0, desi_wa = -0.757, -0.83
    desi_w0_err, desi_wa_err = 0.058, 0.24  # conservative: max(+0.24, 0.21)
    rho_corr = -0.8  # approximate w0-wa correlation
    theta = np.linspace(0, 2*np.pi, 200)
    for nsig, alp in [(1, 0.2), (2, 0.08)]:
        # Correlated ellipse
        cos_t, sin_t = np.cos(theta), np.sin(theta)
        x_ell = nsig * desi_w0_err * cos_t
        y_ell = nsig * desi_wa_err * (rho_corr * cos_t + np.sqrt(1-rho_corr**2) * sin_t)
        ax.fill(desi_w0 + x_ell, desi_wa + y_ell, alpha=alp, color='blue')
    ax.text(desi_w0 + 0.08, desi_wa + 0.5, 'DESI DR2\n(+CMB+SN)', fontsize=7, color='blue')

    # SQMH trajectory (positive xi only = physical)
    xi_pos = [x for x in xi_values if x > 0]
    w0_pos = [results[x][0] for x in xi_pos]
    wa_pos = [results[x][1] for x in xi_pos]
    ax.plot(w0_pos, wa_pos, 'g-o', ms=8, lw=2, label='SQMH (xi_q>0, physical)', zorder=5)
    for xi_q in xi_pos:
        w0, wa = results[xi_q]
        ax.annotate(f'xi={xi_q}', (w0, wa), fontsize=7,
                    textcoords="offset points", xytext=(5, 5))

    # Negative xi (non-SQMH, phantom)
    xi_neg = [x for x in xi_values if x < 0]
    for xi_q in xi_neg:
        w0, wa = results[xi_q]
        ax.plot(w0, wa, 'x', color='#9C27B0', ms=10, mew=2,
                label=f'xi={xi_q} (phantom, non-SQMH)')

    ax.plot(-1, 0, 'k+', ms=15, mew=3, label='LCDM')
    ax.axvline(-1, color='red', ls='-', lw=1, alpha=0.5)
    ax.axhline(0, color='gray', ls=':', alpha=0.3)

    # Shade phantom region
    ax.axvspan(-1.5, -1.0, alpha=0.05, color='red')
    ax.text(-1.15, 1.2, 'phantom\nregion', fontsize=7, color='red', ha='center')

    ax.set_xlabel('$w_0$')
    ax.set_ylabel('$w_a$')
    ax.set_title('$w_0$-$w_a$ plane: SQMH vs DESI DR2')
    ax.legend(fontsize=6, loc='lower left')
    ax.set_xlim(-1.3, -0.4)
    ax.set_ylim(-2.5, 1.5)

    plt.tight_layout()
    plt.savefig('../figures/06_dark_energy_w.png', dpi=300)
    plt.show()

    print("SQMH w0-wa predictions (quadratic IDE: Q ~ rho_DE * rho_m):")
    for xi_q in xi_values:
        w0, wa = results[xi_q]
        phys = "SQMH" if xi_q > 0 else ("LCDM" if xi_q == 0 else "phantom")
        print(f"  xi_q={xi_q:+.2f}: w0={w0:.4f}, wa={wa:+.4f}  [{phys}]")

    return results


if __name__ == "__main__":
    print("=" * 60)
    print("SQMH Dark Energy w(z) -- Quadratic IDE")
    print("=" * 60)
    plot_w_z()
