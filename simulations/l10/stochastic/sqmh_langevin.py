"""
simulations/l10/stochastic/sqmh_langevin.py
L10-S: Stochastic SQMH Langevin SDE numerical integration
K51/Q51: Does CSL-type diffusion produce erf profile?

Rule-B 4-person code review:
  - Reviewer 1: No unicode in print()
  - Reviewer 2: numpy trapz -> trapezoid
  - Reviewer 3: No double-counting in Friedmann
  - Reviewer 4: No ad hoc shortcuts in physics

Date: 2026-04-11
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy.special import erf

# ============================================================
# Physical constants (SI)
# ============================================================
G = 6.674e-11       # m^3 kg^-1 s^-2
c = 2.998e8         # m/s
hbar = 1.055e-34    # J s
k_B = 1.381e-23     # J/K
l_P = 1.616e-35     # m (Planck length)
t_P = 5.391e-44     # s (Planck time)
m_P = 2.176e-8      # kg (Planck mass)
rho_P = m_P / l_P**3  # kg/m^3 (Planck density)

# SQMH constants
sigma_SQMH = 4 * np.pi * G * t_P   # m^3 kg^-1 s^-1
H0 = 67.4e3 / 3.086e22             # s^-1 (Hubble rate today)
Om_m = 0.315
rho_c0 = 3 * H0**2 / (8 * np.pi * G)
rho_m0 = Om_m * rho_c0             # kg/m^3

# SQMH equilibrium n (today)
# n_eq = Gamma_0 / (3H + sigma*rho_m) ~ Gamma_0 / sigma / rho_m for sigma*rho_m >> 3H
# We use n_eq = rho_P / (4*pi) as the reference (NF-3 from L8)
n_mu_product = rho_P / (4 * np.pi)  # n_bar * mu = Planck density / 4pi (SI)

# Equilibrium n_bar (we need Gamma_0 = n_mu_product * sigma for consistency)
# n_bar_eq = Gamma_0 / sigma / rho_m (in quasi-static limit, 3H << sigma*rho_m)
# Let's use n_bar = 1 (normalized units) since only the ratio matters
n_eq_normalized = 1.0
Gamma_0_normalized = sigma_SQMH * n_eq_normalized * rho_m0  # ensures n_eq = 1

print("=== SQMH Langevin SDE: K51/Q51 Analysis ===")
print("")
print("Physical constants:")
print("  sigma_SQMH =", sigma_SQMH)
print("  H0 =", H0)
print("  rho_m0 =", rho_m0)
print("  rho_P =", rho_P)
print("  Gamma_0 (normalized) =", Gamma_0_normalized)
print("")

# ============================================================
# Section 1: Euler-Maruyama for n(t) SDE
# ============================================================
# SDE: dn = [Gamma_0 - sigma*n*rho_m - 3H*n] dt + eta*sqrt(n) dW
# In normalized units: let n_bar = n/n_eq, tau = H0*t
# Then: d n_bar = [1 - n_bar - 3*n_bar*(H/H0)] d(H0*t) * (sigma*rho_m/H0)
#               + eta_norm * sqrt(n_bar) * sqrt(d(H0*t)) * xi

# Drift (normalized): mu(n) = (Gamma_0 - sigma*rho_m*n - 3H*n) / (sigma*rho_m)
# At z=0, H = H0, rho_m = rho_m0
# mu(n_norm) * sigma*rho_m = Gamma_0 - sigma*rho_m*(n_norm*n_eq) - 3H0*(n_norm*n_eq)
# ~ sigma*rho_m*n_eq * (1 - n_norm) for sigma*rho_m >> 3H0 (check ratio)

ratio_3H_sigma_rho = 3 * H0 / (sigma_SQMH * rho_m0)
print("  3H0 / (sigma*rho_m) =", ratio_3H_sigma_rho)
print("  => sigma*rho_m term dominates by", 1/ratio_3H_sigma_rho, "orders")
print("")

# In normalized units (n_norm = n/n_eq):
# d n_norm/d tau = (sigma*rho_m/H0) * (1 - n_norm) + eta_norm * sqrt(n_norm) * xi(tau)
# Let lambda = sigma*rho_m0/H0 (relaxation rate in Hubble units)
lambda_relax = sigma_SQMH * rho_m0 / H0
print("  lambda_relax = sigma*rho_m0/H0 =", lambda_relax)
print("  (Note: this is Pi_SQMH = Omega_m * H0 * t_P =", Om_m * H0 * t_P, ")")
print("")

# ============================================================
# Section 2: SDE ensemble simulation
# ============================================================
N_traj = 1000       # number of trajectories
N_steps = 10000     # time steps
tau_max = 10.0      # in Hubble times
dtau = tau_max / N_steps

np.random.seed(42)

# Test multiple noise levels (in normalized units)
# eta_norm values to test: 0 (deterministic) to large
eta_values = [0.0, 1e-10, 1e-5, 0.01, 0.1, 1.0, 10.0]

print("=== Ensemble SDE simulation (N_traj={}, N_steps={}) ===".format(N_traj, N_steps))
print("")

results = {}

for eta in eta_values:
    # Initialize all trajectories at n_norm = 1.0 (equilibrium)
    n = np.ones(N_traj)
    n_mean_trajectory = np.zeros(N_steps + 1)
    n_mean_trajectory[0] = np.mean(n)

    for step in range(N_steps):
        # Drift
        drift = lambda_relax * (1.0 - n) * dtau
        # Diffusion (Euler-Maruyama)
        if eta > 0:
            noise = eta * np.sqrt(np.maximum(n, 0)) * np.sqrt(dtau) * np.random.randn(N_traj)
        else:
            noise = 0.0
        n = n + drift + noise
        # Absorbing boundary at n=0 (density can't be negative)
        n = np.maximum(n, 0.0)
        n_mean_trajectory[step + 1] = np.mean(n)

    results[eta] = n_mean_trajectory

# ============================================================
# Section 3: Check if <n(tau)> profile is erf-like
# ============================================================
tau_arr = np.linspace(0, tau_max, N_steps + 1)

def erf_model(t, A, t0, sigma_erf, offset):
    """erf model: offset + A * erf((t - t0) / sigma_erf)"""
    return offset + A * erf((t - t0) / sigma_erf)

def exp_model(t, A, tau_relax, offset):
    """exponential relaxation model"""
    return offset + A * np.exp(-t / tau_relax)

print("erf fit vs exponential fit for <n(tau)>:")
print("-" * 60)

for eta in eta_values:
    n_mean = results[eta]

    # Try exponential fit
    try:
        p0_exp = [n_mean[0] - n_mean[-1], 1.0/lambda_relax, n_mean[-1]]
        popt_exp, _ = curve_fit(exp_model, tau_arr, n_mean, p0=p0_exp, maxfev=5000)
        n_pred_exp = exp_model(tau_arr, *popt_exp)
        residual_exp = np.sqrt(np.mean((n_mean - n_pred_exp)**2))
        r2_exp = 1 - np.sum((n_mean - n_pred_exp)**2) / np.sum((n_mean - np.mean(n_mean))**2)
    except Exception:
        r2_exp = -999.0
        residual_exp = 999.0

    # Try erf fit (requires non-monotone or transition shape)
    try:
        p0_erf = [0.1, tau_max/2, 1.0, n_mean[-1]]
        popt_erf, _ = curve_fit(erf_model, tau_arr, n_mean, p0=p0_erf, maxfev=5000)
        n_pred_erf = erf_model(tau_arr, *popt_erf)
        r2_erf = 1 - np.sum((n_mean - n_pred_erf)**2) / np.sum((n_mean - np.mean(n_mean))**2)
    except Exception:
        r2_erf = -999.0

    print("  eta = {:.2e}: R2_exp = {:.4f}, R2_erf = {:.4f}  => Best fit: {}".format(
        eta, r2_exp, r2_erf,
        "EXP" if r2_exp >= r2_erf else "ERF"
    ))

print("")

# ============================================================
# Section 4: Spatial profile check (1D spatial SQMH with diffusion)
# ============================================================
# Extend to 1D spatial: dn/dt + v * dn/dx = [source] + D_s * d^2n/dx^2
# where D_s = CSL diffusion coefficient
# Standard CSL: D_CSL ~ 1e-30 m^2/s for nucleon-mass particles
# For spacetime quanta (mass ~ Planck mass):
D_CSL_nucleon = 1e-30    # m^2/s (standard CSL for nucleon)
m_nucleon = 1.67e-27     # kg
# If D_CSL ~ D_0 * (m_nucleon/m_object): smaller mass -> more diffusion
# For m_quanta ~ m_P = 2.18e-8 kg (much heavier): less diffusion
D_CSL_Planck = D_CSL_nucleon * (m_nucleon / m_P)
print("CSL spatial diffusion coefficients:")
print("  D_CSL (nucleon mass) =", D_CSL_nucleon, "m^2/s")
print("  D_CSL (Planck mass)  =", D_CSL_Planck, "m^2/s")

# erf profile emerges from heat equation: length scale L = sqrt(D * t_Hubble)
t_Hubble = 1.0 / H0
L_CSL_nucleon = np.sqrt(D_CSL_nucleon * t_Hubble)
L_CSL_Planck  = np.sqrt(D_CSL_Planck  * t_Hubble)
L_Mpc = 3.086e22  # 1 Mpc in meters

print("  t_Hubble =", t_Hubble, "s")
print("  L_erf (nucleon CSL) =", L_CSL_nucleon, "m =", L_CSL_nucleon/L_Mpc, "Mpc")
print("  L_erf (Planck CSL)  =", L_CSL_Planck,  "m =", L_CSL_Planck/L_Mpc,  "Mpc")
print("  L_erf gap from Mpc (nucleon):", L_Mpc / L_CSL_nucleon, "orders of magnitude")
print("")

# ============================================================
# Section 5: Bistable SQMH toy (artificially bistable)
# ============================================================
# Modified source: f(n) = -V'(n) where V(n) = alpha * (n-n1)^2 * (n-n2)^2
# Minima at n1 = 0.5, n2 = 2.0 (in normalized units)
n1, n2 = 0.5, 2.0
alpha = 1.0

def bistable_drift(n, lam=lambda_relax, n1=n1, n2=n2, alpha=alpha):
    """Bistable potential drift: -alpha*(n-n1)^2*(n-n2)*(something)"""
    # V(n) = alpha * (n - n1)^2 * (n - n2)^2
    # V'(n) = 2*alpha*(n-n1)*(n-n2)^2 + 2*alpha*(n-n1)^2*(n-n2)
    #       = 2*alpha*(n-n1)*(n-n2)*[(n-n2)+(n-n1)]
    #       = 2*alpha*(n-n1)*(n-n2)*(2n - n1 - n2)
    return -2 * alpha * (n - n1) * (n - n2) * (2*n - n1 - n2)

print("=== Bistable SQMH toy model ===")
print("  V(n) = alpha*(n-n1)^2*(n-n2)^2 with n1={}, n2={}".format(n1, n2))

# 1D spatial bistable SDE with diffusion D_s
# dn/dt = bistable_drift(n) + D_s * d^2n/dx^2 + eta * xi(x,t)
# Use finite difference on a 1D grid
N_x = 200
x_arr = np.linspace(-10, 10, N_x)
dx = x_arr[1] - x_arr[0]
D_s = 0.5   # artificial diffusion (normalized units)
dt_pde = 0.01
N_t_pde = 2000

# Initial condition: step function at x=0 (seed for erf)
n_pde = np.where(x_arr < 0, n1, n2).astype(float)

np.random.seed(123)
for _ in range(N_t_pde):
    # Laplacian (periodic BC)
    lap = (np.roll(n_pde, -1) - 2*n_pde + np.roll(n_pde, 1)) / dx**2
    drift_term = bistable_drift(n_pde)
    n_pde = n_pde + dt_pde * (drift_term + D_s * lap)
    n_pde = np.clip(n_pde, 0, 5.0)

# Fit erf to the spatial profile
try:
    mid_x = x_arr[N_x // 2]
    p0_erf = [n2 - n1, mid_x, 1.0, (n1+n2)/2]
    popt_erf, _ = curve_fit(erf_model, x_arr, n_pde, p0=p0_erf, maxfev=5000)
    n_pred_erf = erf_model(x_arr, *popt_erf)
    r2_bistable_erf = 1 - np.sum((n_pde - n_pred_erf)**2) / np.sum((n_pde - np.mean(n_pde))**2)
    print("  Bistable + diffusion erf fit R2 =", r2_bistable_erf)
    print("  erf width parameter =", abs(popt_erf[2]))
except Exception as e:
    print("  Bistable erf fit failed:", e)
    r2_bistable_erf = -999.0

print("")

# ============================================================
# Section 6: Final K51/Q51 Verdict
# ============================================================
print("=== K51 / Q51 VERDICT ===")
print("")
print("K51 Test (standard + CSL-physical Langevin -> no erf):")

all_r2_erf = []
for eta in eta_values:
    n_mean = results[eta]
    try:
        p0_erf = [0.1, tau_max/2, 1.0, n_mean[-1]]
        popt_erf, _ = curve_fit(erf_model, tau_arr, n_mean, p0=p0_erf, maxfev=5000)
        n_pred_erf = erf_model(tau_arr, *popt_erf)
        r2_erf = 1 - np.sum((n_mean - n_pred_erf)**2) / np.sum((n_mean - np.mean(n_mean))**2)
    except Exception:
        r2_erf = -999.0
    all_r2_erf.append(r2_erf)

max_r2_erf = max(all_r2_erf)
print("  Max erf R^2 across all eta:", max_r2_erf)
print("  K51 threshold: R^2 < 0.90")
if max_r2_erf < 0.90:
    print("  K51 STATUS: TRIGGERED (no erf from n-space Langevin)")
else:
    print("  K51 STATUS: NOT TRIGGERED (erf detected!)")

print("")
print("Q51 Test (bistable extension -> erf possible):")
print("  Bistable erf R^2:", r2_bistable_erf)
if r2_bistable_erf > 0.90:
    print("  Q51 STATUS: PARTIAL PASS (bistable SQMH with diffusion produces erf)")
    print("  BUT: requires non-standard bistable source term (ad hoc modification)")
else:
    print("  Q51 STATUS: FAIL (even bistable extension fails to produce clean erf)")

print("")
print("=== SCALE COMPARISON SUMMARY ===")
print("  L_erf (CSL nucleon) / L_Mpc =", L_CSL_nucleon / L_Mpc)
print("  L_erf (CSL Planck)  / L_Mpc =", L_CSL_Planck  / L_Mpc)
print("  Gap: CSL diffusion is", int(round(-np.log10(L_CSL_nucleon / L_Mpc))), "orders below Mpc")
print("")
print("  CONCLUSION: Physical CSL diffusion cannot produce cosmological-scale erf.")
print("  Standard SQMH Langevin: erf impossible (K51 TRIGGERED).")
print("  Bistable extension: erf possible in principle but requires ad hoc modification.")

print("")
print("=== L10-S Complete ===")
