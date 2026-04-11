"""
L9 Phase B: Non-uniform SQMH Gradient Term
============================================
Rule-B 4-person code review. Tag: L9-B.

Goal: Solve spherically symmetric SQMH PDE with gradient term.
Check if integral gives erf-like profile. Assess Q43.

Full SQMH equation (non-uniform):
  dn/dt + nabla.(n*v) = Gamma0 - sigma*n*rho_m(r,t)

In spherical symmetry (FLRW background + perturbation):
  dn/dt + (3H)n + (1/r^2)*d/dr(r^2*n*v_r) = Gamma0 - sigma*n*rho_m

where:
  v_r(r) = g(r)*t_P = (GM(<r)/r^2)*t_P  [infall velocity ~ gravity * Planck time]
  rho_m(r,t) = rho_m0(t) * (1 + delta(r,t))  [perturbed density]

For the gradient term contribution to rho_DE:
  rho_DE_grad(r,t) = mu * int n(r,t) d^3r / V

The key question: does n(r,t) develop an erf-like spatial profile?

Erf arises from diffusion equations:
  dn/dt = D * nabla^2(n)  [heat equation solution is erf]

The SQMH advection term v_r*dn/dr acts like a directed transport.
If we write nabla.(n*v) = v*dn/dr + n*nabla.v, and v ~ r (radial outflow/inflow):
  nabla.v = 3H (Hubble flow) + infall part
  v_infall = -g(r)*t_P = -(GM/r^2)*t_P  [negative = infall]

For a linear velocity field v ~ r (Hubble-like):
  nabla.(n*v) = n*H + r*H*dn/dr -> pure advection, no erf

For the infall velocity v_infall(r) = -(GM_sphere/r^2)*t_P:
  nabla.v_infall = -(4*pi*G*rho_m/3 - 2*GM/r^3)*t_P [divergence]
  This is non-trivial spatially.

Mathematical structure for erf appearance:
  If we decompose n(r,t) = n_bar(t) + delta_n(r,t):
  The perturbation equation:
  d(delta_n)/dt + v_infall * d(delta_n)/dr + delta_n * nabla.v_infall
    = -sigma*n_bar*delta_rho_m  [linear in delta_n and delta_rho_m]

  For a top-hat overdensity: delta_rho_m = Theta(R-r) * delta_rho_0
  The boundary response of delta_n at r=R is erf-like due to the
  advection of the step function by the infall velocity.

CLAUDE.md rules:
- print() no unicode
- numpy 2.x: trapezoid not trapz
- forward time integration
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import erf
import json
import os

# ============================================================
# Physical constants (SI)
# ============================================================
G_SI = 6.674e-11
c_SI = 2.998e8
hbar_SI = 1.055e-34
t_P = np.sqrt(hbar_SI * G_SI / c_SI**5)
sigma_SQMH = 4 * np.pi * G_SI * t_P

H0_SI = 67.4e3 / 3.0857e22   # s^-1
rho_crit0 = 3 * H0_SI**2 / (8*np.pi*G_SI)  # kg/m^3
Omega_m0 = 0.315
rho_m0_SI = Omega_m0 * rho_crit0
Omega_L0 = 0.685

# Gamma0 (SQMH production rate)
# From SQMH quasi-static: n_bar ~ Gamma0/(3H) -> rho_DE ~ mu*Gamma0/(3H)
# At z=0: rho_DE = Omega_L0 * rho_crit0
# mu*Gamma0 = 3*H0 * Omega_L0 * rho_crit0
mu_Gamma0 = 3 * H0_SI * Omega_L0 * rho_crit0  # kg/(m^3*s)

print("t_P =", t_P, "s")
print("sigma_SQMH =", sigma_SQMH, "m^3/(kg*s)")
print("Pi_SQMH =", sigma_SQMH * rho_m0_SI / (3*H0_SI))
print("mu*Gamma0 =", mu_Gamma0, "kg/(m^3*s)")

# ============================================================
# Dimensionless setup
# ============================================================
# Use Hubble units: r in units of c/H0, t in units of H0^-1
# Define: rho_m_dimless = rho_m / rho_crit0
# Gamma0_dimless = Gamma0 * H0^-1 / n_bar_scale
# sigma_dimless = sigma_SQMH * rho_crit0 / H0

r_H = c_SI / H0_SI  # Hubble radius [m] ~ 1.37e26 m
sigma_dimless = sigma_SQMH * rho_crit0 / H0_SI
print("\nsigma_dimless =", sigma_dimless, "(62-order suppressed)")

# ============================================================
# Spherically symmetric SQMH PDE
# Use comoving coordinates x = r/a (physical = comoving * a)
# n field in units of mu*Gamma0 / (3*H0)
# ============================================================

# Grid setup
Nr = 200
N_time = 500
# Comoving radius in units of Mpc (dimensionless Hubble units)
x_max = 200.0   # Mpc / (c/H0) ~ 200 Mpc
x_min = 0.1
x_arr = np.linspace(x_min, x_max, Nr)
dx = x_arr[1] - x_arr[0]

# Time: N = ln(a), from N_ini=-7 to 0
N_ini = -3.0  # start at z=19 (z>20 has blow-up issues per CLAUDE.md)
N_end = 0.0

def H_over_H0(a):
    """E(a) = H(a)/H0 for LCDM."""
    return np.sqrt(Omega_m0*a**-3 + Omega_L0)

def dH_dN_over_H0(a):
    """dE/dN where N=ln(a)."""
    E = H_over_H0(a)
    return (-1.5*Omega_m0*a**-3) / E

# ============================================================
# Infall velocity (Planck-suppressed)
# v_infall(x) = (GM(<x)/x^2) * t_P [physical]
# In comoving coords, the velocity contribution to n evolution:
# dn/dN + (3 + v_r/Hr)*n + v_r/(Hr)*x*dn/dx = source
# The infall velocity: v_r = -(G*M_sphere(r)/r^2)*t_P
#   For mean density: M_sphere(r) = (4pi/3)*rho_m*r^3
#   v_r = -(4pi*G*rho_m/3)*r * t_P = -H^2 * Omega_m/2 * r * t_P/H^2
#   In Hubble units: v_r / (H*r) = -Omega_m/2 * H0*t_P / E(a)
#                                ~ -Omega_m/2 * Pi_SQMH / (Omega_m * E(a))
#   = -Pi_SQMH / (2*E(a))  [62 orders suppressed]
# ============================================================

Pi_SQMH = sigma_SQMH * rho_m0_SI / (3*H0_SI)
# Infall velocity amplitude in Hubble units:
v_amp = Pi_SQMH  # ~ 1e-62 (same suppression!)
print("Infall velocity amplitude (Pi_SQMH):", v_amp)
print("This is 62 orders suppressed: gradient term also negligible")

# ============================================================
# Mathematical structure analysis: does the integral give erf?
# ============================================================
print("\n=== Mathematical Structure Analysis ===")
print("\n1. Uniform SQMH: n_bar = Gamma0/(3H) + ..., no spatial structure")
print("\n2. Linear perturbation: delta_n(x, N) satisfies:")
print("   d(delta_n)/dN = -3*delta_n - (v_amp/E)*x*d(delta_n)/dx")
print("   + source: -sigma_dimless*delta_rho_m(x)")
print("   where sigma_dimless ~ 1e-62")
print("\n3. If source = Theta(x - R)*delta_rho_0 (top-hat step function):")
print("   The solution is an advected step function (NOT erf)")
print("   For advection equation with v ~ x: solution is delta_n(x-v_eff*t)")
print("   Erf requires DIFFUSION (Laplacian term), not advection")
print("\n4. The nabla.(n*v) term in SQMH:")
print("   nabla.(n*v_infall) = v_infall * grad(n) + n * nabla.v_infall")
print("   nabla.v_infall = d/dr(v_r) + 2*v_r/r [spherical]")
print("   For v_r = -v_amp*r: nabla.v_infall = -3*v_amp")
print("   This is a pure negative dilution, NOT a diffusion term")
print("\n5. Erf CANNOT emerge from advection without diffusion!")
print("   SQMH PDE is first-order in space -> no erf from pure advection")
print("   Unless: stochastic SQMH adds noise -> Fokker-Planck has diffusion")

# ============================================================
# Numerical PDE: simplified spherical SQMH
# ============================================================
print("\n=== Numerical PDE Solution ===")

# Simplified: ignore Planck-suppressed infall (it's 1e-62 anyway)
# Focus on whether ANY spatial structure can emerge from production-destruction coupling

# Use a spatially varying rho_m (overdensity profile):
# rho_m(x) = rho_m0 * (1 + delta_rho * exp(-x^2 / (2*sigma_r^2)))
# Gaussian overdensity at center

delta_rho_amp = 1.0    # 100% overdensity at center (nonlinear, for illustration)
sigma_r = 20.0          # Mpc scale (in comoving Hubble units: ~ 20/4300 << 1, normalize)

def rho_m_profile(x_arr, a):
    """Spatially varying matter density (dimensionless)."""
    # Gaussian overdensity in comoving coords (decays as a^-3)
    delta = delta_rho_amp * np.exp(-x_arr**2 / (2.0 * sigma_r**2))
    return Omega_m0 * a**-3 * (1.0 + delta)

# Erf profile for comparison
def erf_profile(x_arr, x0, width):
    """Error function profile centered at x0."""
    return 0.5 * (1.0 + erf((x_arr - x0) / width))

# Integrate the n field (without Planck-suppressed infall):
# dn/dN = -3*n + (Gamma0_dimless) - sigma_dimless * n * rho_m(x)
# This decouples from spatial structure entirely since sigma_dimless ~ 1e-62
# n(x, N) ~ n_bar(N) * exp(-sigma_dimless * rho_m_perturb(x) * time)
#          ~ n_bar(N) * (1 - sigma_dimless * rho_m_perturb * delta_N)
# The perturbation is proportional to sigma_dimless ~ 1e-62

N_arr_time = np.linspace(N_ini, N_end, N_time)
a_arr_time = np.exp(N_arr_time)

# Background n_bar (uniform)
n_bar_arr = np.zeros(N_time)
# Quasi-static solution: n_bar = Gamma0/(3*H)
# In dimensionless units: n_bar ~ 1/(3*E(a))
n_bar_arr = 1.0 / (3.0 * np.array([H_over_H0(a) for a in a_arr_time]))

# Spatial perturbation at final time
a_end = 1.0
rho_m_x = rho_m_profile(x_arr, a_end)
delta_rho_m = rho_m_x - Omega_m0  # excess rho_m
delta_N = N_end - N_ini  # time integrated

# SQMH perturbation:
delta_n_sqmh = -sigma_dimless * n_bar_arr[-1] * delta_rho_m * delta_N
n_total = n_bar_arr[-1] + delta_n_sqmh

print("Background n_bar at z=0 (dimensionless):", n_bar_arr[-1])
print("Max |delta_n_sqmh|:", np.max(np.abs(delta_n_sqmh)))
print("Ratio delta_n/n_bar:", np.max(np.abs(delta_n_sqmh)) / n_bar_arr[-1])

# Compare n_total profile to erf:
# Erf centered at sigma_r (edge of overdensity)
erf_comp = erf_profile(x_arr, sigma_r, sigma_r/3.0)

# Normalize for comparison
n_norm = (n_total - n_total.min()) / (n_total.max() - n_total.min() + 1e-100)
erf_norm = erf_profile(x_arr, sigma_r, sigma_r)

# Compute correlation
corr = np.corrcoef(n_norm, erf_norm)[0,1]
print("\nCorrelation of SQMH n(x) with erf profile:", corr)

print("\n--- Structure of n(x) ---")
print("n_total profile: uniform + tiny SQMH correction")
print("Shape of correction: -sigma_dimless * delta_rho_m(x)")
print("Shape of delta_rho_m(x): Gaussian (NOT erf!)")
print("Therefore: SQMH n(x) ~ Gaussian profile, NOT erf")
print("The erf would require n to respond to STEP function in rho_m")
print("Even then: the response is attenuated by sigma_dimless ~ 1e-62")

# ============================================================
# Stochastic extension: does noise give diffusion?
# ============================================================
print("\n=== Stochastic Extension: Fokker-Planck Diffusion ===")
print("Stochastic SQMH (from NF-8, L8):")
print("  dn = [-3Hn + Gamma0 - sigma*n*rho_m]*dt + sqrt(n)*dW")
print("  This is a multiplicative-noise SDE (Ito convention)")
print("  Fokker-Planck for P(n,t):")
print("  dP/dt = -d/dn[(drift)*P] + (1/2)*d^2/dn^2[(n)*P]")
print("  This IS a diffusion equation in n-space, NOT in position space!")
print("  So stochastic SQMH gives erf in n-space, NOT in x-space")
print("  For spatial erf: need position-dependent noise, not used in SQMH")

# ============================================================
# Erf-like structure from step-function rho_m
# ============================================================
print("\n=== Erf-like structure from step-function source ===")
print("If rho_m(x) = rho_m0 * (1 + delta*Theta(x-R)):")
print("The perturbation delta_n = -sigma_dimless*n_bar*delta*Theta(x-R)*delta_t")
print("This is a STEP function (Theta), not erf")
print("For erf to appear: need DIFFUSION of the step -> heat equation")
print("SQMH is purely REACTIVE (no second-order spatial derivative)")
print("Conclusion: erf cannot emerge from SQMH alone (no diffusion term)")

# Verify: the integral of n(x) over a spherical volume
# rho_DE_eff(t) = mu * int n(r) * 4*pi*r^2 dr
# For n(r) = n_bar + delta_n(r):
# rho_DE_eff(t) = mu*n_bar * V + mu * int delta_n(r) dr^3
# = rho_DE_uniform + delta_rho_DE_spatial

rho_DE_spatial = np.trapezoid(4*np.pi*x_arr**2 * delta_n_sqmh, x_arr)
print("\nSpatial correction to rho_DE (integrated):", rho_DE_spatial)
print("Relative correction:", rho_DE_spatial / (n_bar_arr[-1] * (4*np.pi/3)*x_max**3))

# ============================================================
# Q43 Judgment
# ============================================================
print("\n=== Q43 Judgment ===")
print("Q43 threshold: non-uniform SQMH gradient term produces erf-like integral structure")
print()
print("Result: NO erf-like structure from SQMH gradient term.")
print("Reasons:")
print("  1. SQMH is first-order in space (advection, no diffusion)")
print("  2. Infall velocity v_r ~ Pi_SQMH * r (62-order suppressed)")
print("  3. Response to overdensity: Gaussian, not erf")
print("  4. Stochastic noise gives erf in n-space, NOT position-space")
print("  5. K43 condition met: gradient term also 62-order suppressed")

Q43_pass = False
K43_triggered = True

print("\nQ43 PASS:", Q43_pass)
print("K43 TRIGGERED:", K43_triggered)

# ============================================================
# What CAN produce erf in cosmological context?
# ============================================================
print("\n=== What could produce erf? (theoretical analysis) ===")
print("1. Perez-Sudarsky diffusion (C26): dn_Lambda/dt = D*nabla^2(n_Lambda)")
print("   -> True diffusion -> erf profile. But C26 is killed by CMB constraint (L5).")
print("2. Phase transition front: domain wall between n=0 and n=n_bar")
print("   -> Kink solution erf-like near interface. Requires spontaneous symmetry breaking.")
print("3. Non-equilibrium SQMH with spatial correlation: if Gamma0(x) = Gamma0*erf(r/L)")
print("   -> n_bar(x) ~ erf profile. But then erf is INPUT, not OUTPUT.")
print("4. Diffusion in quintessence potential: V''*phi = diffusion-like in field space")
print("   -> Not applicable to SQMH (SQMH has no kinetic term for n).")
print("\nConclusion: A12 erf proxy shape NOT derivable from SQMH structure.")
print("erf in w(a) context is a phenomenological observation (A12), not a prediction.")

# ============================================================
# Save results
# ============================================================
results = {
    "Pi_SQMH": float(Pi_SQMH),
    "sigma_dimless": float(sigma_dimless),
    "infall_velocity_amp": float(v_amp),
    "max_delta_n_over_n_bar": float(np.max(np.abs(delta_n_sqmh)) / n_bar_arr[-1]),
    "correlation_n_with_erf": float(corr),
    "rho_DE_spatial_correction": float(rho_DE_spatial),
    "Q43_pass": bool(Q43_pass),
    "K43_triggered": bool(K43_triggered),
    "structural_reasons": [
        "SQMH is first-order in space (advection only, no diffusion)",
        "Infall velocity Pi_SQMH ~ 1e-62 (62-order suppressed, same as background)",
        "Response to overdensity: Gaussian profile, not erf",
        "Stochastic SQMH gives erf in n-space (fluctuation amplitude), not position space",
        "No mechanism within SQMH generates spatial erf profile"
    ],
    "verdict": "K43_triggered",
    "note": ("Non-uniform SQMH gradient term is 62-order suppressed. "
             "No erf-like spatial structure can emerge from SQMH advection. "
             "K43 condition met: all SQMH levels background-level useless.")
}

out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, "sqmh_gradient_results.json")
with open(out_path, "w") as f:
    json.dump(results, f, indent=2)

print("\nResults saved to", out_path)
print("\n=== L9-B COMPLETE ===")
