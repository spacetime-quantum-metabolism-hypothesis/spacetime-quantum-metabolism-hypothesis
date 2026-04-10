# -*- coding: utf-8 -*-
"""
SQMH Physical Constants & Parameters
All values from PDG 2024 / Planck 2018 — zero free parameters.
"""
import numpy as np

# --- Fundamental constants ---
G = 6.67430e-11        # m³ kg⁻¹ s⁻²  (gravitational constant)
c = 2.99792458e8       # m/s            (speed of light)
hbar = 1.054571817e-34 # J·s            (reduced Planck)
k_B = 1.380649e-23     # J/K            (Boltzmann)

# --- Planck units ---
l_P = np.sqrt(hbar * G / c**3)          # 1.616e-35 m
t_P = np.sqrt(hbar * G / c**5)          # 5.391e-44 s
m_P = np.sqrt(hbar * c / G)             # 2.176e-8 kg
E_P = m_P * c**2                        # 1.956e9 J

# --- Cosmological parameters (Planck 2018) ---
H_0_km = 67.36                          # km/s/Mpc
Mpc = 3.0857e22                         # m
H_0 = H_0_km * 1e3 / Mpc               # s⁻¹  (2.184e-18)
Omega_m = 0.3153                        # matter density parameter
Omega_DE = 0.6847                       # dark energy density parameter
Omega_r = 9.15e-5                       # radiation density parameter
rho_crit = 3 * H_0**2 / (8 * np.pi * G)  # kg/m³ (critical density)
rho_m0 = Omega_m * rho_crit            # present matter density
rho_DE0 = Omega_DE * rho_crit          # present DE density

# --- SQMH derived parameters (zero free params) ---
# IMPORTANT: sigma = 4*pi*G is ONLY valid in Planck units (c=G=hbar=1).
# In SI: sigma = 4*pi*G*t_P, where t_P = Planck time.
sigma = 4 * np.pi * G * t_P             # annihilation cross-section [m³kg⁻¹s⁻¹]

# n₀μ = rho_Planck/(4pi) — Planck-scale medium density.
# Individual n₀, μ underdetermined (base.md §3.4).
n0_mu = 1.0 / (4 * np.pi * G * t_P**2) # kg/m³ (= rho_P / (4pi))
# Legacy individual values (for display only, product is what matters):
n_0 = m_P / (4 * np.pi * G * t_P**2)   # m^-3 (if mu = 1 kg, placeholder)
mu = n0_mu / n_0                        # kg (placeholder, product n0*mu is physical)

# Generation rate: Γ₀ = σ n₀ ρ_m0 + 3 H₀ n₀
Gamma_0 = sigma * n_0 * rho_m0 + 3 * H_0 * n_0  # m⁻³ s⁻¹

# Coupling constant
xi = 2 * np.sqrt(np.pi * G) / c**2      # metabolic field coupling

# Metabolic field mass scale
m_phi = H_0 / c                          # ~7.3e-27 m⁻¹ (cosmological)

# --- Solar system test masses ---
M_sun = 1.989e30    # kg
M_earth = 5.972e24  # kg
R_earth = 6.371e6   # m
AU = 1.496e11        # m

# --- Utility ---
def print_params():
    """Print all SQMH parameters for verification."""
    print(f"G      = {G:.5e} m^3/kg/s^2")
    print(f"sigma  = {sigma:.5e} m^3/kg/s")
    print(f"n_0    = {n_0:.3e} m^-3")
    print(f"mu     = {mu:.3e} kg")
    print(f"Gamma0 = {Gamma_0:.3e} m^-3 s^-1")
    print(f"xi     = {xi:.3e}")
    print(f"H_0    = {H_0:.3e} s^-1")
    print(f"rho_m0 = {rho_m0:.3e} kg/m^3")
    print(f"rho_DE = {rho_DE0:.3e} kg/m^3")
    print(f"n0*mu*c^2 = {n_0 * mu * c**2:.3e} J/m^3  (ratio to rho_DE*c^2: {n_0 * mu * c**2 / (rho_DE0 * c**2):.2f})")


if __name__ == "__main__":
    print_params()
