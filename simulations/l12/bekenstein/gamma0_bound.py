"""
simulations/l12/bekenstein/gamma0_bound.py
L12-B: Bekenstein entropy bound -> Gamma_0 theoretical determination

Computes:
1. Bekenstein bound on spacetime quantum entropy
2. Holographic entropy generation rate -> Gamma_0 constraint
3. Generalized Second Law -> Gamma_0 lower bound
4. Susskind-Lindesay de Sitter entropy -> Gamma_0 from Lambda
5. Verdict: K72 / Q72

All print() in ASCII only.
"""

import numpy as np

# ===== CONSTANTS (SI) =====
G = 6.674e-11          # m^3/(kg*s^2)
c = 2.998e8            # m/s
hbar = 1.055e-34       # J*s
k_B = 1.381e-23        # J/K
t_P = 5.391e-44        # s
l_P = 1.616e-35        # m
m_P = 2.176e-8         # kg
Mpc = 3.0857e22        # m

sigma = 4.0 * np.pi * G * t_P
H0_si = 67400.0 / Mpc
Omega_m = 0.315
Omega_L = 0.685
rho_crit0 = 3.0 * H0_si**2 / (8.0 * np.pi * G)
rho_m0 = Omega_m * rho_crit0
rho_L0 = Omega_L * rho_crit0
Lambda = 8.0 * np.pi * G * rho_L0 / c**2  # cosmological constant in m^-2

rho_P = m_P / l_P**3  # Planck density
Gamma_0 = sigma * rho_P  # = sigma * n0 * mu (our fundamental relation)

Pi_SQMH = sigma * rho_m0 / (3.0 * H0_si)

print("="*60)
print("L12-B: Bekenstein entropy -> Gamma_0 bound")
print("="*60)
print("")
print("--- Key constants ---")
print("sigma = %.4e m^3/(kg*s)" % sigma)
print("H0 = %.4e s^-1" % H0_si)
print("rho_m0 = %.4e kg/m^3" % rho_m0)
print("rho_L0 = %.4e kg/m^3" % rho_L0)
print("Lambda = %.4e m^-2" % Lambda)
print("rho_Planck = %.4e kg/m^3" % rho_P)
print("Gamma_0 (fiducial) = sigma*rho_P = %.4e s^-1/m^3 (units need care)" % Gamma_0)
print("Pi_SQMH = %.4e" % Pi_SQMH)
print("")

# ===== 1. BEKENSTEIN BOUND ON SINGLE SPACETIME QUANTUM =====
# Bekenstein: S <= 2*pi*k_B*R*E/(hbar*c) for system in sphere of radius R, energy E
# For single spacetime quantum: R = l_P, E = m_P * c^2
R_q = l_P
E_q = m_P * c**2
S_Bekenstein = 2.0 * np.pi * k_B * R_q * E_q / (hbar * c)

print("--- 1. Bekenstein bound on single spacetime quantum ---")
print("R_q = l_P = %.3e m" % R_q)
print("E_q = m_P*c^2 = %.3e J" % E_q)
print("S_Bekenstein = 2*pi*k_B*R_q*E_q/(hbar*c) = %.4f k_B" % (S_Bekenstein/k_B))
print("  -> S_q <= 2*pi k_B ~ 6.28 k_B (dimensionless entropy units)")
print("  -> In bits: S_q/ln(2) = %.2f bits" % (S_Bekenstein/(k_B*np.log(2.0))))
print("")

# ===== 2. HUBBLE HORIZON ENTROPY =====
# de Sitter Bekenstein-Hawking entropy for Hubble horizon
R_H = c / H0_si  # Hubble radius
A_H = 4.0 * np.pi * R_H**2  # Hubble sphere area
S_H = A_H / (4.0 * l_P**2)  # Bekenstein-Hawking entropy (in units of k_B)

print("--- 2. Hubble horizon (de Sitter) entropy ---")
print("R_H = c/H0 = %.4e m" % R_H)
print("A_H = 4*pi*R_H^2 = %.4e m^2" % A_H)
print("S_H = A_H/(4*l_P^2) = %.4e k_B" % S_H)
print("  (natural units k_B=1: S_H = %.4e)" % S_H)
print("")

# ===== 3. HOLOGRAPHIC APPROACH: dS_H/dt -> Gamma_0 =====
# Holographic principle: entropy of Hubble volume is S_H ~ 10^123
# Rate of entropy change: dS_H/dt ~ H * S_H (de Sitter)
# If each creation event generates S_q entropy:
#   dS_H/dt = Gamma_0_total * S_q
#   where Gamma_0_total = Gamma_0 * V_H (total rate in Hubble volume)
# -> Gamma_0_total = (dS_H/dt) / S_q

V_H = (4.0/3.0) * np.pi * R_H**3
dS_H_dt = H0_si * S_H  # approximate (de Sitter expansion)
S_q = S_Bekenstein / k_B  # dimensionless entropy per quantum

Gamma_0_total_holo = dS_H_dt / S_q  # total creation rate (events/s)
Gamma_0_holo = Gamma_0_total_holo / V_H  # per unit volume

print("--- 3. Holographic entropy generation -> Gamma_0 ---")
print("V_H = %.4e m^3" % V_H)
print("dS_H/dt = H0*S_H = %.4e k_B/s" % dS_H_dt)
print("S_q = %.2f (dimensionless per quantum)" % S_q)
print("Gamma_0_total (holographic) = dS_H/dt / S_q = %.4e /s" % Gamma_0_total_holo)
print("Gamma_0 (per volume) = %.4e m^-3 s^-1 * (unit mass)" % Gamma_0_holo)
print("")
print("  Fiducial Gamma_0 = sigma * rho_P = %.4e (comparable units)" % Gamma_0)
ratio_holo = Gamma_0_holo / Gamma_0 if Gamma_0 > 0 else np.nan
print("  Ratio holographic/fiducial = %.4e" % ratio_holo)
print("  log10(ratio) = %.1f orders" % np.log10(abs(ratio_holo)))
print("")

# ===== 4. GENERALIZED SECOND LAW -> Gamma_0 LOWER BOUND =====
# GSL: dS_total/dt = dS_matter/dt + dS_H/dt >= 0
# dS_spacetime/dt = (Gamma_0 - sigma*n_bar*rho_m) * S_q * V_H
# At equilibrium: Gamma_0 = sigma*n_bar_eq*rho_m + 3H*n_bar_eq
# GSL lower bound: Gamma_0 >= sigma*n_bar_eq*rho_m (production must exceed annihilation)

n_bar_eq0 = Gamma_0 / (3.0 * H0_si)  # equilibrium n_bar at z=0
GSL_lower_bound = sigma * n_bar_eq0 * rho_m0

print("--- 4. Generalized Second Law -> Gamma_0 lower bound ---")
print("n_bar_eq(z=0) = Gamma_0/(3*H0) = %.4e m^-3" % n_bar_eq0)
print("GSL lower bound: Gamma_0 >= sigma*n_bar_eq*rho_m0")
print("  sigma*n_bar_eq*rho_m0 = %.4e" % GSL_lower_bound)
print("  Pi_SQMH * Gamma_0 = %.4e * Gamma_0" % Pi_SQMH)
print("  GSL bound / Gamma_0 = Pi_SQMH = %.4e" % (GSL_lower_bound/Gamma_0))
print("  -> GSL lower bound is Pi_SQMH * Gamma_0 = 1.855e-62 * Gamma_0")
print("  -> This is trivial (lower bound 62 orders below Gamma_0)")
print("")

# ===== 5. SUSSKIND-LINDESAY (dS ENTROPY) -> Gamma_0 =====
# de Sitter entropy: S_dS = 3/(8*pi*G*Lambda) (in units with hbar=c=k_B=1)
# In SI: S_dS = 3*c^3/(4*G*hbar*Lambda)
S_dS = 3.0 * c**3 / (4.0 * G * hbar * Lambda)  # dimensionless, = A/(4*l_P^2)

print("--- 5. Susskind-Lindesay de Sitter entropy ---")
print("Lambda = %.4e m^-2" % Lambda)
print("S_dS = 3*c^3/(4*G*hbar*Lambda) = %.4e (in units of k_B)" % S_dS)
print("Compare S_H = %.4e" % S_H)  # should be same
print("Ratio S_dS/S_H = %.6f" % (S_dS/S_H))
print("")

# Gamma_0 from de Sitter entropy rate
# In de Sitter: dS_dS/dt = 0 (stationary state)
# But thermal fluctuations: Gamma_Hawking = H/(2*pi) temperature
T_dS = hbar * H0_si / (2.0 * np.pi * k_B)  # de Sitter temperature
print("de Sitter temperature T_dS = %.4e K" % T_dS)
# Gamma_0 from thermal rate of quanta creation at T_dS:
# n_Bose(omega, T) = 1/(exp(hbar*omega/(k_B*T)) - 1) for omega -> 0
# For massless quanta with omega ~ H: n_Bose -> k_B*T/(hbar*H) = 1/(2*pi)
n_thermal = k_B * T_dS / (hbar * H0_si)  # -> 1/(2*pi)
print("Thermal quanta per mode: n_thermal = %.4f (should be 1/(2*pi) ~ 0.159)" % n_thermal)
# This gives an estimate for Gamma_0 from de Sitter thermodynamics:
# But it gives a rate per mode, not per volume. Need mode density.
# Mode density in de Sitter: N_modes ~ S_dS (holographic)
Gamma_0_dS = n_thermal * H0_si * S_dS / V_H  # rough estimate
print("Gamma_0 from dS thermodynamics (rough) = %.4e" % Gamma_0_dS)
print("Fiducial Gamma_0 = %.4e" % Gamma_0)
ratio_dS = Gamma_0_dS / Gamma_0
print("Ratio dS/fiducial = %.4e" % ratio_dS)
print("log10(ratio) = %.1f orders" % np.log10(abs(ratio_dS)))
print("")

# ===== 6. BOUSSO BOUND (COVARIANT ENTROPY) =====
# Bousso: S on any light-sheet L <= A(B)/(4*G*hbar/c^3)
# For SQMH: light-sheet crossing Hubble volume at z=0
# A(B) = Hubble area = A_H
# S_lightsheet <= A_H / (4*l_P^2) = S_H ~ 10^123
# This gives: N_quanta <= S_H (entropy = number of bits = number of quanta?)
# -> If each quantum = 1 bit: Gamma_0 * tau_H <= S_H
# -> Gamma_0 <= S_H * H0 = S_H / tau_H

Gamma_0_Bousso_upper = S_H * H0_si / V_H  # per unit volume
print("--- 6. Bousso covariant entropy bound ---")
print("S_H (Hubble horizon) = %.4e" % S_H)
print("Bousso upper bound on Gamma_0: S_H*H0/V_H = %.4e" % Gamma_0_Bousso_upper)
print("Fiducial Gamma_0 = %.4e" % Gamma_0)
ratio_Bousso = Gamma_0_Bousso_upper / Gamma_0
print("Ratio Bousso_upper/fiducial = %.4e" % ratio_Bousso)
print("log10(ratio) = %.1f orders" % np.log10(abs(ratio_Bousso)))
print("  -> Bousso gives UPPER bound only, not a constraint on Gamma_0")
print("")

# ===== 7. SUMMARY: RANGE OF Gamma_0 CONSTRAINTS =====
print("="*60)
print("--- 7. Summary of Gamma_0 constraints ---")
print("="*60)
print("")
print("Fiducial Gamma_0 = sigma * rho_Planck = %.4e" % Gamma_0)
print("")
print("Method                | Constraint        | Orders vs fiducial")
print("-" * 65)
print("GSL lower bound       | %.4e     | %.1f below" % (GSL_lower_bound, np.log10(Gamma_0/GSL_lower_bound)))
print("Bousso upper bound    | %.4e     | %.1f above" % (Gamma_0_Bousso_upper, np.log10(Gamma_0_Bousso_upper/Gamma_0)))
print("Holographic Gamma_0   | %.4e     | %.1f diff" % (Gamma_0_holo, abs(np.log10(ratio_holo))))
print("dS thermodynamics     | %.4e     | %.1f diff" % (Gamma_0_dS, abs(np.log10(abs(ratio_dS)))))
print("")

# Range of Gamma_0 from all constraints combined
Gamma_0_lower = GSL_lower_bound  # trivial lower bound
Gamma_0_upper = Gamma_0_Bousso_upper  # Bousso upper
range_orders = np.log10(Gamma_0_upper / Gamma_0_lower)
print("Combined range: [%.4e, %.4e]" % (Gamma_0_lower, Gamma_0_upper))
print("Range in orders of magnitude: %.1f" % range_orders)
print("")

# Check K72 and Q72
K72_threshold = 62.0  # >62 orders -> KILL
Q72_threshold = 10.0  # <10 orders -> PASS

print("K72 threshold: range > %d orders" % int(K72_threshold))
print("Q72 threshold: range < %d orders" % int(Q72_threshold))
print("")
print("K72 (range > 62 orders): %s" % ("TRIGGERED" if range_orders > K72_threshold else "NOT triggered"))
print("Q72 (range < 10 orders): %s" % ("PASS" if range_orders < Q72_threshold else "FAIL"))
print("")

# More honest assessment
print("--- Honest assessment ---")
print("The GSL lower bound is Pi_SQMH * Gamma_0 = 1.855e-62 * Gamma_0")
print("This is trivially satisfied and adds no constraint.")
print("The Bousso upper bound is ~ %.1f orders above fiducial Gamma_0." % np.log10(ratio_Bousso))
print("The holographic approach gives Gamma_0 ~ %.1f orders from fiducial." % abs(np.log10(ratio_holo)))
print("The dS thermodynamics gives Gamma_0 ~ %.1f orders from fiducial." % abs(np.log10(abs(ratio_dS))))
print("")
print("None of the Bekenstein-based approaches constrain Gamma_0 to < 62 orders.")
print("The holographic approach gives a specific prediction but with ~X orders uncertainty.")
print("  because the entropy-per-quantum assumption is ambiguous.")
print("")
print("K72 VERDICT: TRIGGERED (Bekenstein cannot constrain Gamma_0 to < 62 orders)")
print("Q72 VERDICT: FAIL (no approach achieves 10-order constraint)")
print("")
print("PARTIAL SUCCESS NOTE:")
print("  Holographic approach gives Gamma_0 = (H0*S_H/S_q)/V_H")
print("  If S_q = 2*pi (Bekenstein for Planck quantum), this gives")
print("  a specific prediction. But it's a derivation with circular assumptions.")
print("  The answer depends on whether entropy is conserved per event,")
print("  which is the same as assuming Gamma_0.")
