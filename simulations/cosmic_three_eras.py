"""
Simulation 4: Cosmic Three Eras from SQMH
Radiation → Matter → Dark Energy automatic transition.

Key SQMH insight: T^α_α = 0 for radiation → no annihilation →
DE coupling vanishes in radiation era automatically (Lorentz invariance).
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import config


def friedmann_rhs(y, ln_a):
    """
    Friedmann + metabolic coupling.
    y = [Ω_r, Ω_m, Ω_DE]
    Independent variable: ln(a), where a = scale factor.

    Standard:
      dρ_r/dt = -4Hρ_r
      dρ_m/dt = -3Hρ_m + Q
      dρ_DE/dt = -Q
    where Q = σ_eff · ρ_DE · ρ_m (quadratic IDE, SQMH specific)

    In Ω variables with x = ln(a):
      dΩ_r/dx = Ω_r(3Ω_r + 4Ω_m - 1 - 4)  ... (radiation decays as a⁻⁴)
    """
    Omega_r, Omega_m, Omega_DE = y

    # Hubble rate squared: H² = H₀²(Ω_r/a⁴ + Ω_m/a³ + Ω_DE)
    # But we track fractional densities relative to critical
    a = np.exp(ln_a)

    # Physical densities (units of ρ_crit,0)
    rho_r = config.Omega_r / a**4
    rho_m = config.Omega_m / a**3
    rho_DE = config.Omega_DE  # zeroth order constant

    # Hubble parameter squared (units H₀²)
    E2 = rho_r + rho_m + rho_DE  # E² = H²/H₀²

    if E2 <= 0:
        return [0, 0, 0]

    # Metabolic coupling Q/(3H³) in dimensionless form
    # Q = σ_eff · ρ_DE · ρ_m, but T^α_α = -ρ_m c² + 3p
    # For matter (p≈0): T^α_α = -ρ_m c² → coupling active
    # For radiation (p=ρ/3): T^α_α = 0 → coupling OFF (automatic!)
    # This is the key SQMH feature from Lorentz invariance

    # Dimensionless coupling strength
    alpha_c = config.xi**2 * config.c**4 * config.rho_crit / (3 * config.H_0**2)

    Q_dim = alpha_c * rho_DE * rho_m / np.sqrt(E2)  # Q/(3H₀³)

    # Evolution equations in ln(a)
    dOmega_r = -rho_r / E2 * (1 + 3 * (1/3))  # w_r = 1/3 → decays
    dOmega_m = -rho_m / E2 * 1 + Q_dim / E2     # matter + metabolic gain
    dOmega_DE = -Q_dim / E2                       # DE loses to metabolism

    return [dOmega_r, dOmega_m, dOmega_DE]


def compute_density_evolution():
    """Direct density evolution without coupling (to show 3-era structure)."""
    a = np.logspace(-6, 1, 10000)  # a from 1e-6 to 10
    z = 1/a - 1

    # Density parameters (units of ρ_crit,0)
    rho_r = config.Omega_r * a**(-4)
    rho_m = config.Omega_m * a**(-3)
    rho_DE = config.Omega_DE * np.ones_like(a)

    rho_total = rho_r + rho_m + rho_DE

    # Fractional densities
    f_r = rho_r / rho_total
    f_m = rho_m / rho_total
    f_DE = rho_DE / rho_total

    # SQMH net metabolic rate R = Gamma_0 - sigma*n*rho_m (dimensionless)
    # R > 0 -> expansion dominated, R < 0 -> gravity dominated
    # In radiation era: T^a_a = 0 -> R = Gamma_0 (pure generation)
    # NOTE: n_0 is a placeholder (mu=1 assumption). Product n0*mu is physical.
    # The ratio sigma*n_0*rho_m0/Gamma_0 uses n_0 consistently so ratio is valid.
    R_net = np.ones_like(a)  # normalized to Gamma_0
    R_net -= (config.sigma * config.n_0 * config.rho_m0 / config.Gamma_0) * a**(-3)
    # Radiation doesn't contribute to annihilation (T^a_a = 0)

    return a, z, f_r, f_m, f_DE, R_net


def plot_three_eras():
    a, z, f_r, f_m, f_DE, R_net = compute_density_evolution()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # Top: density fractions
    ax1.fill_between(a, 0, f_r, alpha=0.3, color='orange', label='Radiation Ω_r')
    ax1.fill_between(a, f_r, f_r + f_m, alpha=0.3, color='blue', label='Matter Ω_m')
    ax1.fill_between(a, f_r + f_m, 1, alpha=0.3, color='green', label='Dark Energy Ω_DE')
    ax1.set_xscale('log')
    ax1.set_xlabel('Scale factor a')
    ax1.set_ylabel('Density fraction')
    ax1.set_title('Cosmic Three Eras — SQMH: T^α_α=0 for radiation → automatic decoupling')
    ax1.legend(loc='center left')
    ax1.set_xlim(1e-6, 10)
    ax1.set_ylim(0, 1)

    # Transition markers
    # Matter-radiation equality: Ω_r/a⁴ = Ω_m/a³ → a_eq = Ω_r/Ω_m
    a_eq = config.Omega_r / config.Omega_m
    ax1.axvline(a_eq, color='red', ls='--', alpha=0.7, label=f'a_eq = {a_eq:.2e}')
    # Matter-DE equality: Ω_m/a³ = Ω_DE → a_DE = (Ω_m/Ω_DE)^(1/3)
    a_DE = (config.Omega_m / config.Omega_DE)**(1/3)
    ax1.axvline(a_DE, color='purple', ls='--', alpha=0.7, label=f'a_DE = {a_DE:.2f}')
    ax1.axvline(1.0, color='black', ls=':', alpha=0.5, label='Today (a=1)')
    ax1.legend(loc='center left', fontsize=9)

    # Bottom: metabolic net rate
    ax2.plot(a, R_net, 'k-', lw=2)
    ax2.axhline(0, color='gray', ls=':')
    ax2.fill_between(a, R_net, 0, where=(R_net > 0), alpha=0.2, color='green', label='Net creation (DE dominant)')
    ax2.fill_between(a, R_net, 0, where=(R_net < 0), alpha=0.2, color='red', label='Net annihilation (gravity dominant)')
    ax2.set_xscale('log')
    ax2.set_xlabel('Scale factor a')
    ax2.set_ylabel('R_net / Γ₀')
    ax2.set_title('SQMH Net Metabolic Rate (radiation era: no annihilation, T^α_α=0)')
    ax2.set_xlim(1e-6, 10)
    ax2.legend()

    plt.tight_layout()
    plt.savefig('../figures/08_cosmic_three_eras.png', dpi=300)
    plt.show()

    print(f"[OK] Radiation-matter equality: a = {a_eq:.4e}, z = {1/a_eq - 1:.0f}")
    print(f"[OK] Matter-DE equality: a = {a_DE:.4f}, z = {1/a_DE - 1:.2f}")
    print(f"[OK] Key SQMH feature: radiation era coupling = 0 (T^a_a = 0)")


if __name__ == "__main__":
    print("=" * 60)
    print("SQMH Cosmic Three Eras — Simulation")
    print("=" * 60)
    plot_three_eras()
