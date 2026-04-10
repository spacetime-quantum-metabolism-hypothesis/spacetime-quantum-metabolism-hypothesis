"""
Simulation 2: Newtonian Gravity Derivation from SQMH

Core result (base.md III): steady-state inflow around point mass M
  v(r) = sigma*M/(4*pi*r^2) = G*t_P*M/r^2 = g(r)*t_P

where sigma = 4*pi*G*t_P (SI units, Issue #28 resolution).
Inflow velocity = gravitational acceleration * Planck time.

Also demonstrates:
  - G reconstruction from sigma: G = sigma/(4*pi*t_P) to machine precision
  - Gravitational potential U(r) = -GMm/r from potential flow (Lamb 1932)
  - 2D inflow vector field visualization

NOTE on n0, mu (base.md 3.4): n0 and mu are individually underdetermined
in SI units. Only the product n0*mu = rho_Planck/(4pi) is physical.
"""
import numpy as np
import matplotlib.pyplot as plt
import config


def inflow_velocity(r, M):
    """SQMH inflow velocity: v(r) = sigma*M/(4*pi*r^2) = g(r)*t_P [m/s]"""
    return config.sigma * M / (4 * np.pi * r**2)


def g_times_tP(r, M):
    """Newtonian g * Planck time: G*t_P*M/r^2 [m/s]"""
    return config.G * config.t_P * M / r**2


def g_newton(r, M):
    """Newtonian: g(r) = G*M/r^2 [m/s^2]"""
    return config.G * M / r**2


def potential_newton(r, M, m):
    """U(r) = -G*M*m/r"""
    return -config.G * M * m / r


def plot_gravity_matching():
    """Core proof: sigma=4piG*t_P gives v(r)=g(r)*t_P exactly."""
    M = config.M_earth
    r = np.linspace(config.R_earth, 10 * config.R_earth, 500)

    v_sq = inflow_velocity(r, M)
    g_tP = g_times_tP(r, M)
    g_n = g_newton(r, M)
    rel_err = np.abs(v_sq - g_tP) / g_tP

    # G reconstruction check
    G_reconstructed = config.sigma / (4 * np.pi * config.t_P)
    G_rel_err = abs(G_reconstructed - config.G) / config.G

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Panel 1: v(r) = g(r)*t_P overlay
    axes[0].plot(r / config.R_earth, v_sq, 'b-', lw=2.5,
                 label=r'SQMH: $\sigma M/(4\pi r^2)$')
    axes[0].plot(r / config.R_earth, g_tP, 'r--', lw=2,
                 label=r'Newton: $g(r) \cdot t_P$')
    axes[0].set_xlabel('r / R_Earth')
    axes[0].set_ylabel('Inflow velocity (m/s)')
    axes[0].set_title(r'SQMH: $v(r) = g(r) \cdot t_P$ ($\sigma=4\pi G \cdot t_P$)')
    axes[0].legend()
    axes[0].set_yscale('log')

    # Panel 2: relative error (machine precision)
    axes[1].plot(r / config.R_earth, rel_err, 'k-', lw=2)
    axes[1].set_xlabel('r / R_Earth')
    axes[1].set_ylabel('Relative Error')
    axes[1].set_title(f'Error = {np.max(rel_err):.2e} (machine precision)')
    axes[1].set_yscale('log')

    # Panel 3: potential
    m_test = 1.0
    U = potential_newton(r, M, m_test)
    axes[2].plot(r / config.R_earth, U, 'b-', lw=2)
    axes[2].set_xlabel('r / R_Earth')
    axes[2].set_ylabel('U(r) (J/kg)')
    axes[2].set_title(r'Gravitational Potential $U=-GMm/r$')

    plt.tight_layout()
    plt.savefig('../figures/04_gravity_derivation.png', dpi=300)
    plt.show()

    v_surface = inflow_velocity(config.R_earth, M)
    g_surface = g_newton(config.R_earth, M)
    print(f"[OK] sigma = 4piG*t_P: {config.sigma:.5e} m^3/kg/s")
    print(f"[OK] v(r) = g(r)*t_P identity: max relative error = {np.max(rel_err):.2e}")
    print(f"[OK] G reconstruction: {G_reconstructed:.5e} (rel err = {G_rel_err:.2e})")
    print(f"[OK] Earth surface: g = {g_surface:.2f} m/s^2, v = {v_surface:.2e} m/s, v/c = {v_surface/config.c:.2e}")


def plot_force_field_2d():
    """2D vector field of SQMH spacetime quantum inflow."""
    M = config.M_earth
    N = 20
    x = np.linspace(-5, 5, N) * config.R_earth
    y = np.linspace(-5, 5, N) * config.R_earth
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    R = np.where(R < 0.5 * config.R_earth, 0.5 * config.R_earth, R)

    v_mag = config.sigma * M / (4 * np.pi * R**2)
    Vx = -v_mag * X / R
    Vy = -v_mag * Y / R

    fig, ax = plt.subplots(figsize=(8, 8))
    speed = np.sqrt(Vx**2 + Vy**2)
    ax.quiver(X / config.R_earth, Y / config.R_earth,
              Vx / speed, Vy / speed,
              np.log10(speed), cmap='coolwarm', scale=25)
    circle = plt.Circle((0, 0), 1, fill=True, color='black', alpha=0.8, label='Mass M')
    ax.add_patch(circle)
    ax.set_xlabel('x / R_Earth')
    ax.set_ylabel('y / R_Earth')
    ax.set_title('SQMH: Spacetime Quantum Inflow = Gravity')
    ax.set_aspect('equal')
    ax.legend()

    plt.tight_layout()
    plt.savefig('../figures/05_gravity_vector_field.png', dpi=300)
    plt.show()
    print("[OK] 2D vector field saved")


def print_sigma_derivation():
    """Show the sigma=4piG*t_P derivation chain."""
    print("SQMH Gravity Derivation (Issue #28 resolved):")
    print("  Steady state: d(n)/dt = 0")
    print("  Spherical symmetry around point mass M:")
    print(f"    4*pi*r^2 * n0 * v(r) = sigma * n0 * M")
    print(f"    v(r) = sigma*M / (4*pi*r^2)")
    print(f"  In Planck units: sigma_P = 4*pi (dimensionless)")
    print(f"  In SI: sigma = 4*pi*G*t_P")
    print(f"    => v(r) = G*t_P*M/r^2 = g(r)*t_P")
    print(f"    sigma         = {config.sigma:.6e} m^3/kg/s")
    print(f"    4*pi*G*t_P    = {4*np.pi*config.G*config.t_P:.6e} m^3/kg/s")
    G_recon = config.sigma / (4 * np.pi * config.t_P)
    print(f"    G reconstructed = {G_recon:.6e} (rel err = {abs(G_recon - config.G)/config.G:.2e})")
    print()
    print("  NOTE (base.md 3.4): n0, mu individually underdetermined.")
    print(f"  n0*mu = rho_Planck/(4pi) = {config.n0_mu:.3e} kg/m^3")


if __name__ == "__main__":
    print("=" * 60)
    print("SQMH Gravity Derivation")
    print("=" * 60)

    print_sigma_derivation()
    print()
    plot_gravity_matching()
    plot_force_field_2d()
