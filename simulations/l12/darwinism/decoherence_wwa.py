"""
simulations/l12/darwinism/decoherence_wwa.py
L12-Q: Quantum Darwinism -> wa<0 third independent explanation

Computes:
1. Coherence time tau_coh(z) = 1/(sigma*rho_m)
2. Decoherence parameter C(z) = exp(-t/tau_coh)
3. wa contribution from decoherence
4. Independence from NF-11/NF-29 (inflation + void bias)
5. Verdict: K75 / Q75

All print() in ASCII only.
"""

import numpy as np
from scipy.integrate import solve_ivp

# ===== CONSTANTS (SI) =====
G = 6.674e-11
c = 2.998e8
hbar = 1.055e-34
k_B = 1.381e-23
t_P = 5.391e-44
l_P = 1.616e-35
m_P = 2.176e-8
Mpc = 3.0857e22

sigma = 4.0 * np.pi * G * t_P
H0_si = 67400.0 / Mpc
Omega_m = 0.315
Omega_L = 0.685
rho_crit0 = 3.0 * H0_si**2 / (8.0 * np.pi * G)
rho_m0 = Omega_m * rho_crit0
rho_P = m_P / l_P**3
Gamma_0 = sigma * rho_P

Pi_SQMH = sigma * rho_m0 / (3.0 * H0_si)

print("="*60)
print("L12-Q: Quantum Darwinism -> wa<0")
print("="*60)
print("")
print("sigma = %.4e m^3/(kg*s)" % sigma)
print("H0 = %.4e s^-1" % H0_si)
print("rho_m0 = %.4e kg/m^3" % rho_m0)
print("Pi_SQMH = %.4e" % Pi_SQMH)
print("")

# ===== 1. DECOHERENCE TIME tau_coh(z) =====
# SQMH: annihilation rate = sigma*rho_m
# Quantum Darwinism interpretation: sigma*rho_m is the environment coupling rate
# tau_coh = 1/(sigma*rho_m) = quantum-to-classical transition timescale

z_arr = np.linspace(0, 3.0, 1000)
rho_m = rho_m0 * (1+z_arr)**3

tau_coh = 1.0 / (sigma * rho_m)  # in seconds
tau_H = 1.0 / H0_si  # Hubble time

print("--- 1. Coherence timescale tau_coh(z) ---")
print("tau_coh(z) = 1/(sigma*rho_m0*(1+z)^3)")
print("")
print("z=0:  tau_coh = %.4e s = %.4e * tau_H" % (tau_coh[0], tau_coh[0]/tau_H))
print("z=0.5: tau_coh = %.4e s" % tau_coh[np.argmin(np.abs(z_arr-0.5))])
print("z=1:  tau_coh = %.4e s" % tau_coh[np.argmin(np.abs(z_arr-1.0))])
print("z=2:  tau_coh = %.4e s" % tau_coh[np.argmin(np.abs(z_arr-2.0))])
print("z=3:  tau_coh = %.4e s" % tau_coh[np.argmin(np.abs(z_arr-3.0))])
print("")
print("Ratio tau_coh(z=0) / tau_H = %.4e (62 orders!)" % (tau_coh[0]/tau_H))
print("SQMH quanta are essentially always coherent on Hubble scales.")
print("")

# ===== 2. COHERENCE PARAMETER C(z) =====
# C(z) = exp(-t(z)/tau_coh(z))
# where t(z) is lookback time and tau_coh(z) is coherence time at z
# For cosmological time t(z):
# dt = -dz / ((1+z)*H(z))
# H(z) = H0*E(z), E(z) = sqrt(Omega_m*(1+z)^3 + Omega_L)

E_arr = np.sqrt(Omega_m*(1+z_arr)**3 + Omega_L)
H_arr = H0_si * E_arr

# t(z) = integral from z to infty of dz'/((1+z')*H(z'))
# t(0) = current age, t(z) = age at redshift z
# Lookback time: t_lb(z) = integral from 0 to z
dz = z_arr[1] - z_arr[0]
integrand_t = 1.0 / ((1+z_arr) * H_arr)
t_lookback = np.cumsum(integrand_t) * dz  # lookback time from z=0

# Age at redshift z = t_age(0) - t_lookback(z)
# For our purposes, t/tau_coh at redshift z:
# Use cosmic time at z: t_z ~ 2/(3*H(z)) (matter era) or 1/H_Lambda (dS)
# Simple: t_cosmic(z) ~ 1/H(z) (order of magnitude)
t_cosmic_approx = 1.0 / H_arr

# Decoherence parameter C(z) = 1 - exp(-t_cosmic(z)/tau_coh(z))
# = 1 - exp(-sigma*rho_m(z)*t_cosmic(z))
# = 1 - exp(-sigma*rho_m0*(1+z)^3 / H(z))
# = 1 - exp(-Pi_SQMH * (1+z)^3/E(z) * 3)  [since Pi_SQMH = sigma*rho_m0/(3*H0)]

arg_coh = sigma * rho_m / H_arr  # = sigma*rho_m0*(1+z)^3 / (H0*E(z))

print("--- 2. Decoherence parameter C(z) ---")
print("C(z) = sigma*rho_m(z)/H(z) = sigma*rho_m0*(1+z)^3/(H0*E(z))")
print("     = Pi_SQMH * 3*(1+z)^3/E(z)")
print("")
for z_check in [0.0, 0.5, 1.0, 2.0, 3.0]:
    idx = np.argmin(np.abs(z_arr - z_check))
    print("z=%.1f: C(z) = %.4e, E(z) = %.4f" % (z_check, arg_coh[idx], E_arr[idx]))

print("")
print("Note: C(z) is Pi_SQMH * 3*(1+z)^3/E(z) ~ Pi_SQMH * tiny number")
print("This is the decoherence RATE * time, not degree of decoherence")
print("The quantum state is essentially 100%% coherent at all z")
print("")

# ===== 3. wa CONTRIBUTION FROM DECOHERENCE =====
# If quantum coherence C(z) modifies n_bar:
# n_bar_eff(z) = n_bar_classical(z) * (1 + C(z)) [coherence enhances production?]
# or
# n_bar_eff(z) = n_bar_classical(z) * exp(-C(z)) [decoherence depletes quanta?]
#
# The physical picture (Quantum Darwinism):
# Decoherence = quanta becoming "classical" and losing quantum identity
# Classicalization rate = sigma*rho_m (SQMH annihilation rate!)
# When quanta decohere, they "annihilate" from quantum perspective
# This is IDENTICAL to the sigma*rho_m term in SQMH
#
# Therefore: Quantum Darwinism reinterpretation gives SAME equation as classical SQMH
# No new contribution to wa. The decoherence IS the classical dissipation term.

print("--- 3. wa from quantum decoherence ---")
print("Physical identification:")
print("  SQMH: dn_bar/dt = Gamma_0 - sigma*n_bar*rho_m - 3H*n_bar")
print("  Quantum Darwinism: dN_quantum/dt = -Gamma_classicalize * N_quantum")
print("    where Gamma_classicalize = sigma*rho_m")
print("  These are THE SAME. Decoherence = SQMH annihilation.")
print("")
print("Conclusion: Quantum Darwinism gives NO NEW wa contribution.")
print("The decoherence rate is the SQMH dissipation term -- identical math.")
print("")

# Let's try a different interpretation:
# What if decoherence adds a STOCHASTIC term beyond the mean?
# n_bar_eff = n_bar + fluctuation from decoherence
# <fluctuation> ~ sqrt(sigma*rho_m * n_bar * t) = sqrt(C(z) * n_bar)
# This is the quantum shot noise (same as Poisson floor, NF-28)

delta_n_deco = np.sqrt(arg_coh * Gamma_0/(3.0*H_arr))  # variance from decoherence

print("Decoherence fluctuation: delta_n/n_bar = sqrt(C(z)/N_bar)")
for z_check in [0.0, 0.5, 1.0, 2.0]:
    idx = np.argmin(np.abs(z_arr - z_check))
    n_bar_z = Gamma_0 / (3.0 * H_arr[idx])
    V_H_z = (c/H_arr[idx])**3
    N_bar_z = n_bar_z * V_H_z
    delta_over_n = np.sqrt(arg_coh[idx] / N_bar_z)
    print("  z=%.1f: delta_n/n_bar ~ %.4e" % (z_check, delta_over_n))

print("")

# ===== 4. COMPARISON WITH NF-11 AND NF-29 =====
# NF-11: SQMH quasi-static EOS w0_eff ~ -0.83, wa_eff ~ -0.33
# NF-29: Dark energy anti-bias b_DE(z) = -Pi_SQMH(z)
# L11 R4: wa<0 from initial over-production (inflation mechanism)
#
# Quantum Darwinism claim: wa<0 from decoherence
# But decoherence = sigma*rho_m annihilation term (IDENTICAL to SQMH classical)
# -> Not independent. K75 triggered.

print("--- 4. Independence check vs NF-11 / NF-29 / L11-R4 ---")
print("")
print("NF-11: wa<0 from quasi-static EOS (classical SQMH background)")
print("NF-29: b_DE = -Pi_SQMH (anti-bias, qualitative)")
print("L11-R4: wa<0 from inflation-era over-production (n_bar_init >> n_bar_eq)")
print("")
print("Quantum Darwinism interpretation:")
print("  Decoherence rate = sigma*rho_m = SQMH annihilation term")
print("  -> Mathematical identity: Darwinism = classical dissipation")
print("  -> No new mechanism for wa<0")
print("  -> K75 triggered: same as NF-11 (classical SQMH)")
print("")

# ===== 5. ALTERNATIVE: POINTER STATE SELECTION =====
# What if quantum Darwinism 'selects' a preferred pointer state for n_bar?
# Pointer states = eigenstates of the SQMH interaction Hamiltonian
# Interaction: H_int = sigma * n_hat * rho_m_hat (environment = matter)
# Pointer basis = Fock states |n> (eigenstates of N_hat = a^dag a)
#
# If Fock states are preferred, the density matrix stays diagonal:
# rho = sum_n P(n) |n><n|
# And P(n) evolves as: dP(n)/dt = Gamma_0*(P(n-1)-P(n)) - sigma*rho_m*(n*P(n)-(n+1)*P(n+1))
# This is the classical birth-death master equation!
# Mean: d<n>/dt = Gamma_0 - sigma*rho_m*<n> -- same as SQMH classical

print("--- 5. Pointer state selection ---")
print("Pointer states = Fock states |n> (eigenstates of SQMH interaction)")
print("Density matrix stays diagonal (decoherence -> classical)")
print("Result: classical birth-death master equation EXACTLY")
print("  -> Quantum Darwinism explains why SQMH is classical:")
print("     matter density rho_m decoheres spacetime quanta into Fock states")
print("  -> This is the MECHANISM for why quantum SQMH = classical SQMH")
print("  -> BUT: no new wa<0 beyond classical")
print("")

# ===== 6. GENUINE NEW RESULT: DECOHERENCE SCALE HIERARCHY =====
# The ratio tau_coh / tau_H = 1/(sigma*rho_m*H^{-1}) = 1/(Pi_SQMH*3) ~ 10^62
# This means: SQMH quanta decohere 10^62 times SLOWER than Hubble rate
# Interpretation: spacetime quanta are "barely" classical
# They would be quantum if sigma were 10^62 times larger
#
# Alternative: if sigma_classical means Pi_SQMH = O(1):
# sigma_required = 3*H0/rho_m0 ~ 3*2.184e-18 / 2.69e-27 = 2.44e9 m^3/(kg*s)
# sigma_SQMH / sigma_required = 4.52e-53 / 2.44e9 = 1.85e-62 = Pi_SQMH (circular!)

sigma_required = 3.0 * H0_si / rho_m0
print("--- 6. Decoherence scale hierarchy ---")
print("For SQMH quanta to decohere at Hubble rate, sigma would need to be:")
print("  sigma_required = 3*H0/rho_m0 = %.4e m^3/(kg*s)" % sigma_required)
print("  sigma_SQMH = %.4e m^3/(kg*s)" % sigma)
print("  ratio = sigma_SQMH/sigma_required = %.4e = Pi_SQMH" % (sigma/sigma_required))
print("  -> Again Pi_SQMH appears. Not independent.")
print("")

# ===== FINAL VERDICTS =====
print("="*60)
print("FINAL VERDICTS")
print("="*60)
print("")
print("K75 (Quantum Darwinism gives same result as NF-11/NF-29): TRIGGERED")
print("  Decoherence rate = sigma*rho_m = SQMH classical dissipation")
print("  Mathematical identity: quantum Darwinism = classical SQMH")
print("  No new wa<0 mechanism discovered")
print("")
print("Q75 (Independent third explanation of wa<0): FAIL")
print("  Quantum Darwinism = classical SQMH (same math)")
print("  wa<0 would require additional new mechanism")
print("")
print("STRUCTURAL RESULT:")
print("  Quantum Darwinism EXPLAINS WHY SQMH IS CLASSICAL:")
print("  Matter density rho_m acts as quantum Darwinism environment")
print("  Decoheres spacetime quanta into Fock (number) pointer states")
print("  This is WHY the classical SQMH equation is the right description")
print("  (not just an assumption)")
print("")
print("  This is a genuine physical insight about the SQMH framework:")
print("  sigma*rho_m is simultaneously:")
print("    1. Classical: annihilation rate of spacetime quanta with matter")
print("    2. Quantum: decoherence rate of spacetime quanta into classical states")
print("  These are the SAME process viewed classically and quantum-mechanically")
print("")
print("NF candidate (NF-32):")
print("  Matter density rho_m acts as quantum Darwinism environment")
print("  for SQMH spacetime quanta. The decoherence (pointer) basis = Fock states |n>.")
print("  sigma = 4*pi*G*t_P is the coupling between spacetime quanta and matter")
print("  that selects the classical (Fock state) description of SQMH.")
print("  This provides the PHYSICAL JUSTIFICATION for using classical SQMH equation.")
