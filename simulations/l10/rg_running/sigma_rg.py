"""
simulations/l10/rg_running/sigma_rg.py
L10-RG: sigma RG running under Asymptotic Safety and LQC holonomy corrections
K58/Q58: Is sigma running cosmologically relevant?

Rule-B 4-person code review:
  - Reviewer 1: No unicode in print()
  - Reviewer 2: numpy trapz -> trapezoid (not needed)
  - Reviewer 3: sigma = 4*pi*G*t_P (SI), not Planck units
  - Reviewer 4: Asymptotic Safety: G(k) = G_N/(1 + omega*G_N*k^2/c^3)

Date: 2026-04-11
"""

import numpy as np

# ============================================================
# Physical constants
# ============================================================
G = 6.674e-11       # m^3 kg^-1 s^-2
c = 2.998e8         # m/s
hbar = 1.055e-34    # J s
k_B = 1.381e-23     # J/K
l_P = 1.616e-35     # m
t_P = 5.391e-44     # s
m_P = 2.176e-8      # kg

H0 = 67.4e3 / 3.086e22   # s^-1

sigma_0 = 4 * np.pi * G * t_P
k_P = 1.0 / l_P            # Planck wavenumber [m^-1]
k_H0 = H0 / c              # Hubble wavenumber [m^-1]
k_ratio = k_P / k_H0       # ratio (should be huge)

print("=== L10-RG: sigma RG Running Analysis ===")
print("")
print("sigma_0 = 4*pi*G*t_P =", sigma_0, "m^3 kg^-1 s^-1")
print("k_P (Planck wavenumber) =", k_P, "m^-1")
print("k_H0 (Hubble wavenumber) =", k_H0, "m^-1")
print("k_P / k_H0 =", k_ratio)
print("")

# ============================================================
# Approach 1: Asymptotic Safety (Bonanno-Platania 2018)
# ============================================================
print("=== Approach 1: Asymptotic Safety G(k) running ===")
# G(k) = G_N / (1 + omega * G_N * k^2 / c^3)
# where omega ~ O(1) (Reuter-Saueressig) -- typically omega ~ 1/Planck
# Physical identification: k = xi * H (running with Hubble scale, xi ~ O(1))

omega_AS = 1.0 / (G * k_P**2 / c**3)  # normalize: omega = 1 at k=k_P gives G(k_P) = G_N/2
print("  omega_AS (Planck normalized) =", omega_AS)

def G_AS(k, omega=None):
    """Asymptotic Safety running G"""
    if omega is None:
        # omega ~ 1/l_P^2 in Planck units (common parameterization)
        omega = 1.0 / (G * k_P**2 / c**3)
    return G / (1.0 + omega * G * k**2 / c**3)

# k at z=0: k = H0/c
# k at Planck era: k = k_P
G_today = G_AS(k_H0)
G_Planck = G_AS(k_P)
sigma_today_AS = 4 * np.pi * G_today * t_P
sigma_Planck_AS = 4 * np.pi * G_Planck * t_P

print("")
print("  G(k=H0/c) =", G_today, "m^3 kg^-1 s^-2")
print("  G(k=k_P)  =", G_Planck, "m^3 kg^-1 s^-2")
print("  G_today = G (no running at cosmological scales) to part per:", abs(G_today/G - 1))
print("  G_Planck = G/2 (significant running only near Planck scale)")
print("")
print("  sigma(k=H0/c) / sigma_0 =", sigma_today_AS / sigma_0)
print("  sigma(k=k_P)  / sigma_0 =", sigma_Planck_AS / sigma_0)
print("")

# Running from Planck to today:
Delta_sigma_AS = abs(sigma_today_AS - sigma_Planck_AS) / sigma_0
print("  Delta_sigma/sigma (Planck to today, AS) =", Delta_sigma_AS)
print("  log10 =", np.log10(Delta_sigma_AS + 1e-300))
print("")

# More general: scan k from k_P to k_H0
k_values = np.logspace(np.log10(k_H0), np.log10(k_P), 1000)
sigma_values_AS = np.array([4 * np.pi * G_AS(k) * t_P for k in k_values])
sigma_ratio_AS = sigma_values_AS / sigma_0

print("  sigma(k) range: [{:.6f}, {:.6f}] * sigma_0".format(sigma_ratio_AS.min(), sigma_ratio_AS.max()))
print("  Total sigma variation / sigma_0 (AS):", sigma_ratio_AS.max() - sigma_ratio_AS.min())
print("")

# ============================================================
# Approach 2: LQC holonomy corrections
# ============================================================
print("=== Approach 2: LQC holonomy correction ===")
# LQC effective Friedmann: H^2 = (8*pi*G/3) * rho * (1 - rho/rho_crit_LQC)
# This modifies G_eff only when rho ~ rho_crit_LQC = rho_P
# => sigma_eff = sigma_0 * (1 - rho/rho_crit_LQC)

# At z=0: rho_m0 << rho_P
rho_crit_LQC = rho_P = m_P / l_P**3  # kg/m^3
G_N = G
rho_c0 = 3 * H0**2 / (8 * np.pi * G)
rho_m0 = 0.315 * rho_c0

holonomy_corr_today = 1.0 - rho_m0 / rho_crit_LQC
holonomy_corr_Planck = 1.0 - rho_P / rho_crit_LQC  # = 0

sigma_LQC_today = sigma_0 * holonomy_corr_today
sigma_LQC_Planck = sigma_0 * holonomy_corr_Planck

print("  rho_P (LQC critical density) =", rho_P, "kg m^-3")
print("  rho_m0 =", rho_m0, "kg m^-3")
print("  rho_m0 / rho_P =", rho_m0 / rho_P)
print("")
print("  LQC holonomy correction at z=0: (1 - rho_m0/rho_P) =", holonomy_corr_today)
print("  sigma_LQC(z=0) / sigma_0 =", sigma_LQC_today / sigma_0)
print("  1 - sigma_LQC(z=0)/sigma_0 =", 1 - sigma_LQC_today/sigma_0, "=", rho_m0/rho_P)
print("")
print("  At Planck era (rho ~ rho_P): holonomy_corr = 0 => sigma_LQC = 0")
print("  At z=0: correction is rho_m0/rho_P ~", rho_m0/rho_P, "-- negligible")
print("  log10(rho_m0/rho_P) =", np.log10(rho_m0/rho_P))
print("")

# ============================================================
# Approach 3: Running with scale factor a
# ============================================================
print("=== Approach 3: sigma running with scale factor a (cosmological history) ===")
# Use Asymptotic Safety with k = xi * H(a) identification
xi = 1.0  # O(1) factor

def H_LCDM(a, H0=H0, Om=0.315, OL=0.685):
    """LCDM Hubble rate (ignoring radiation for simplicity)"""
    return H0 * np.sqrt(Om * a**(-3) + OL)

a_values = np.logspace(-10, 0, 1000)  # from a=1e-10 to a=1
H_values = np.array([H_LCDM(a) for a in a_values])
k_values_a = xi * H_values / c  # identification k = xi*H/c

sigma_values_a = np.array([4 * np.pi * G_AS(k) * t_P for k in k_values_a])
sigma_ratio_a = sigma_values_a / sigma_0

print("  Scale factor range: a from 1e-10 to 1")
print("  H range: {:.3e} to {:.3e} s^-1".format(H_values.max(), H_values.min()))
print("  k=xi*H/c range: {:.3e} to {:.3e} m^-1".format(k_values_a.max(), k_values_a.min()))
print("  sigma(a) range: [{:.10f}, {:.10f}] * sigma_0".format(sigma_ratio_a.min(), sigma_ratio_a.max()))
print("  Total Delta_sigma/sigma over cosmic history:", sigma_ratio_a.max() - sigma_ratio_a.min())
print("  log10(Delta_sigma/sigma):", np.log10(sigma_ratio_a.max() - sigma_ratio_a.min() + 1e-300))
print("")

# Compare to 62-order gap
gap_62 = 1e-62
print("  K58 threshold: Delta_sigma/sigma < 1e-60")
print("  Actual Delta_sigma/sigma:", sigma_ratio_a.max() - sigma_ratio_a.min())
print("")

# ============================================================
# Approach 4: NF-1 hypothesis check (sigma ~ mu^-1)
# ============================================================
print("=== Approach 4: NF-1 hypothesis (sigma ~ mu^-1 RG running) ===")
print("  NF-1 (L8): If sigma ~ mu^-1, then sigma(H_0) = sigma(m_P) * (m_P*c^2/H_0)")
# m_P * c^2 = energy at Planck scale
# hbar * H_0 = energy at Hubble scale
ratio_scales = m_P * c**2 / (hbar * H0)
print("  m_P*c^2 =", m_P*c**2, "J")
print("  hbar*H0 =", hbar*H0, "J")
print("  m_P*c^2 / (hbar*H0) =", ratio_scales, "(should bridge 62-order gap)")
print("  log10(m_P*c^2 / hbar*H0) =", np.log10(ratio_scales))
print("")
print("  NF-1: sigma ~ mu^-1 would require RG group breaking from Planck to Hubble scale.")
print("  No standard QFT RG gives this running for a dimensionful coupling.")
print("  Would require new BSM mechanism (large extra dimensions, etc.).")
print("  Status: SPECULATIVE, no framework generates this.")
print("")

# ============================================================
# Approach 5: Background independence
# ============================================================
print("=== Approach 5: Background independence argument ===")
print("  In background-independent QG (LQG, CDT, Causal Sets):")
print("  sigma cannot depend on H(a) because H is a background quantity.")
print("  Background independence => sigma is constant (universal coupling).")
print("  This provides a theoretical UPPER BOUND on sigma running.")
print("  From background independence: Delta_sigma/sigma = 0 exactly.")
print("  (But sigma can still run with quantum energy scale k, not background H.)")
print("")

# ============================================================
# K58/Q58 Verdict
# ============================================================
print("=== K58 / Q58 VERDICT ===")
print("")
print("Asymptotic Safety (k identification k=H/c):")
delta_AS = sigma_ratio_a.max() - sigma_ratio_a.min()
print("  Delta_sigma/sigma =", delta_AS)
print("  log10 =", np.log10(delta_AS + 1e-300))

print("")
print("LQC holonomy (rho correction):")
delta_LQC = rho_m0 / rho_P
print("  Delta_sigma/sigma = rho_m0/rho_P =", delta_LQC)
print("  log10 =", np.log10(delta_LQC))

print("")
print("NF-1 (sigma ~ mu^-1):")
print("  Would give Delta_sigma/sigma = ratio_scales =", ratio_scales)
print("  But no physical mechanism. SPECULATIVE.")
print("")

if delta_AS < 1e-60 and delta_LQC < 1e-60:
    print("  K58 STATUS: TRIGGERED")
    print("  AS running: Delta_sigma/sigma <<< 1e-60 (cosmologically irrelevant)")
    print("  LQC holonomy: Delta_sigma/sigma = rho_m0/rho_P ~", delta_LQC, "<<< 1e-60")
    print("  Both within 62-order gap. sigma running cosmologically irrelevant.")
else:
    print("  K58 STATUS: NOT TRIGGERED (unexpected)")

print("")
print("  Q58 STATUS: FAIL")
print("  No mechanism produces Delta_sigma/sigma > 1e-50.")
print("  NF-1 would produce it but has no physical mechanism.")
print("")
print("  CONCLUSION: sigma is constant to 62+ orders across cosmic history.")
print("  Paper: 'We find no evidence for sigma running under AS or LQC.")
print("  sigma = 4*pi*G*t_P is effectively constant throughout cosmic evolution.")
print("  The NF-1 hypothetical mu^-1 running remains speculative (L8).'")
print("")
print("=== L10-RG Complete ===")
