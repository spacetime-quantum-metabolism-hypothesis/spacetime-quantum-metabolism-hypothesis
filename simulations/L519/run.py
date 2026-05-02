"""L519 — final priori attempt: Schwinger-Keldysh propagator IR pole +
thermal occupation at de Sitter (Gibbons-Hawking) temperature → Lambda scale.

Goal: derive n_infty (and thus rho_q ≡ n_infty * eps / c^2) using ONLY
    - H_0  (observed Hubble rate, today)
    - Planck constants  (hbar, G, c)
    - KMS thermal-equilibrium condition for a quantum field in de Sitter

WITHOUT using rho_Lambda_obs as input.  If the result lands within order
unity of rho_Lambda_obs, we have a genuine priori.  If it overshoots/
undershoots by many decades, this path joins L402 Path-alpha as a failed
attempt and the §5.2 circularity stays unavoidable.

Physics setup (KMS-only, no formula injection):

  1. The retarded Green's function G_R(omega, k) of a quantum field in de
     Sitter has an IR structure: at zero spatial momentum and zero
     frequency, the propagator picks up the horizon scale H_0.  This is
     the Schwinger-Keldysh CTP "soft" mode.

  2. KMS detailed-balance fixes the thermal occupation
        n_th(omega) = 1 / (exp(hbar*omega / k_B T_dS) - 1)
     with the Gibbons-Hawking temperature
        k_B T_dS = hbar * H_0 / (2 pi).

  3. For the SQT n-quantum of energy eps (Planck energy by hypothesis),
     hbar*omega = eps  =>  x = 2 pi eps / (hbar H_0).
     With eps = E_P, x = 2 pi sqrt(c^5 / (hbar G)) / H_0  ~ 10^61.
     Thermal occupation n_th ~ exp(-x) is COMPLETELY suppressed.

  4. The IR-pole density (zero-mode contribution) per Hubble volume is
     of order 1 quantum per Hubble volume V_H = (4pi/3)(c/H_0)^3:
        n_IR ~ 1 / V_H.

  5. Two extreme estimates for rho_q via SK + KMS:
        rho_q^thermal = n_th * eps / c^2     (Boltzmann-suppressed)
        rho_q^IR-pole = n_IR * eps / c^2     (one zero-mode per horizon)

  6. Compare to rho_Lambda_obs.  Genuine priori requires order-unity
     agreement WITHOUT eps tuned to rho_Lambda_obs.
"""
import numpy as np

# Physical constants (SI)
c        = 2.99792458e8
G        = 6.67430e-11
hbar     = 1.054571817e-34
k_B      = 1.380649e-23
H0       = 73.0 * 1000.0 / 3.0857e22       # s^-1 (Riess)

# Planck units
t_P      = np.sqrt(hbar * G / c**5)
l_P      = c * t_P
m_P      = np.sqrt(hbar * c / G)
E_P      = m_P * c**2                       # ~1.956e9 J
rho_Pl   = c**5 / (hbar * G**2)

# Reference
rho_crit       = 3.0 * H0**2 / (8.0 * np.pi * G)
rho_Lambda_obs = 0.685 * rho_crit            # ~6.0e-27 kg/m^3 (NOT used as input)

print("="*72)
print(" L519 — Schwinger-Keldysh + KMS priori for Lambda")
print("="*72)
print(f"  H_0           = {H0:.4e} s^-1")
print(f"  E_P           = {E_P:.4e} J")
print(f"  l_P           = {l_P:.4e} m")
print(f"  rho_Lambda_obs (target, NOT input) = {rho_Lambda_obs:.4e} kg/m^3")
print()

# ----- (a) Gibbons-Hawking temperature -----
T_dS  = hbar * H0 / (2.0 * np.pi * k_B)        # K
kT_dS = hbar * H0 / (2.0 * np.pi)              # J
print("--- (a) Gibbons-Hawking de Sitter temperature ---")
print(f"  T_dS  = {T_dS:.4e} K")
print(f"  kT_dS = {kT_dS:.4e} J  =  hbar*H_0/(2*pi)")
print()

# ----- (b) Thermal occupation of a Planck-energy quantum -----
eps_choices = {
    "E_P (Planck energy)"          : E_P,
    "kT_dS (de Sitter scale)"      : kT_dS,
    "hbar*H_0 (Hubble quantum)"    : hbar * H0,
}
print("--- (b) KMS thermal occupation n_th(eps) at T_dS ---")
print(f"{'eps choice':35s}  {'eps [J]':>12s}  {'x=eps/kT_dS':>14s}  {'n_th':>14s}")
for name, eps in eps_choices.items():
    x = eps / kT_dS
    # safe Bose-Einstein eval
    if x > 700:
        n_th = np.exp(-x)
    elif x < 1e-6:
        n_th = 1.0 / x          # Rayleigh-Jeans
    else:
        n_th = 1.0 / (np.exp(x) - 1.0)
    print(f"{name:35s}  {eps:12.4e}  {x:14.4e}  {n_th:14.4e}")
print()

# ----- (c) IR-pole zero-mode density (1 quantum per Hubble volume) -----
R_H = c / H0
V_H = (4.0/3.0) * np.pi * R_H**3
n_IR = 1.0 / V_H
print("--- (c) Schwinger-Keldysh IR pole: 1 zero-mode per Hubble volume ---")
print(f"  R_H = c/H_0 = {R_H:.4e} m")
print(f"  V_H         = {V_H:.4e} m^3")
print(f"  n_IR        = 1/V_H = {n_IR:.4e} m^-3")
print()

# ----- (d) rho_q estimates from SK+KMS, NO rho_Lambda_obs input -----
print("--- (d) rho_q candidates (NO rho_Lambda_obs input) ---")
print(f"{'channel':45s}  {'rho_q [kg/m^3]':>18s}  {'rho_q/rho_Lambda':>20s}")

results = []

for name, eps in eps_choices.items():
    x = eps / kT_dS
    if x > 700:
        n_th = np.exp(-x)
    elif x < 1e-6:
        n_th = 1.0 / x
    else:
        n_th = 1.0 / (np.exp(x) - 1.0)
    # thermal channel: n_th occupation per de-Broglie volume (eps/c)^-3
    # but more honestly: KMS fixes occupation per mode; mode density at
    # IR is ~1/V_H.  Combined:
    rho_th_perH = n_th * eps / (c**2 * V_H)     # one IR mode, occupied n_th
    results.append((f"thermal (eps={name}, 1 IR mode)", rho_th_perH))

# IR-pole at Planck quantum
rho_IR_E_P  = n_IR * E_P    / c**2
rho_IR_kT   = n_IR * kT_dS  / c**2
rho_IR_hH   = n_IR * hbar*H0 / c**2
results.append(("IR pole, 1 quantum @ E_P    per V_H",   rho_IR_E_P))
results.append(("IR pole, 1 quantum @ kT_dS  per V_H",   rho_IR_kT))
results.append(("IR pole, 1 quantum @ hbar*H per V_H",   rho_IR_hH))

# Holographic / Bekenstein-Hawking horizon entropy density:
#   S_dS = pi R_H^2 / l_P^2 ; entropy density s = S/V_H ; n ~ s/k_B
n_holo = (np.pi * R_H**2 / l_P**2) / V_H
rho_holo_kT = n_holo * kT_dS / c**2
rho_holo_hH = n_holo * hbar * H0 / c**2
results.append(("holographic n_holo @ kT_dS",            rho_holo_kT))
results.append(("holographic n_holo @ hbar*H_0",         rho_holo_hH))

for name, rho in results:
    ratio = rho / rho_Lambda_obs
    print(f"{name:45s}  {rho:18.4e}  {ratio:20.4e}")

print()

# ----- (e) The "miracle" combo: does any SK+KMS combination land at O(1)? -----
print("--- (e) Verdict ---")
best = min(results, key=lambda r: abs(np.log10(r[1]/rho_Lambda_obs)))
worst= max(results, key=lambda r: abs(np.log10(r[1]/rho_Lambda_obs)))
print(f"  closest channel:  {best[0]}")
print(f"     rho_q/rho_Lambda = {best[1]/rho_Lambda_obs:.4e}  "
      f"(log10 = {np.log10(best[1]/rho_Lambda_obs):+.2f})")
print(f"  farthest channel: {worst[0]}")
print(f"     rho_q/rho_Lambda = {worst[1]/rho_Lambda_obs:.4e}  "
      f"(log10 = {np.log10(worst[1]/rho_Lambda_obs):+.2f})")
print()

# Order-unity (within decade)?
order_unity = abs(np.log10(best[1]/rho_Lambda_obs)) < 1.0
if order_unity:
    print("  *** ORDER-UNITY MATCH WITHOUT rho_Lambda_obs INPUT ***")
    print("      => SK+KMS is a CANDIDATE priori channel.  Needs rigour.")
else:
    print("  No SK+KMS channel lands within one decade of rho_Lambda_obs")
    print("  WITHOUT eps tuned to rho_Lambda_obs.  Channel decades off:")
    print(f"      best  channel off by 10^{np.log10(best[1]/rho_Lambda_obs):+.1f}")
    print(f"      worst channel off by 10^{np.log10(worst[1]/rho_Lambda_obs):+.1f}")
    print()
    print("  CONCLUSION: SK+KMS reproduces the same vacuum-catastrophe")
    print("  hierarchy as L402 Path-alpha.  Without an additional structure")
    print("  that selects eps ~ kT_dS (i.e. lambda-scale quantum), KMS alone")
    print("  does not predict rho_Lambda.  And selecting eps = kT_dS is")
    print("  itself a hidden circular input (it equals rho_Lambda by")
    print("  dimensional construction up to (4 pi)^2 factors).")
print()

# ----- (f) Honest one-liner -----
print("="*72)
# Check the kT_dS IR-pole channel specifically — it is the "natural" KMS pick
ratio_kT = rho_IR_kT / rho_Lambda_obs
print(f"  IR-pole @ kT_dS ratio      = {ratio_kT:.4e}")
print(f"  IR-pole @ kT_dS log10 off  = {np.log10(ratio_kT):+.2f}")
if abs(np.log10(ratio_kT)) < 1.0:
    print("  >>> kT_dS pick lands O(1).  But eps=kT_dS = hbar H_0/(2pi)")
    print("      already encodes the Hubble scale — circularity returns")
    print("      via the choice of eps, not via rho_Lambda_obs.")
print("="*72)
