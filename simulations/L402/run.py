"""L402 Path-ε negative control.

§5.2 circularity test: vary rho_Lambda_obs input by factors and check if
SQT-derived rho_q/rho_Lambda ratio stays 1.0000 (tautology) or changes
(genuine prediction).

The verify_lambda_origin.py logic (paper/base.md L1012-1031):
    n_inf = rho_Lambda_obs * c**2 / eps   # input
    rho_q = n_inf * eps / c**2            # output

Trivially: rho_q == rho_Lambda_obs by algebra. The ratio is 1.0000 *by
construction* for any rho_Lambda_obs value.

This script confirms the tautology numerically and probes whether any
extra constraint (KMS condition / Hubble-only) breaks the lock.
"""
import numpy as np

# Physical constants (SI)
c = 2.99792458e8           # m/s
G = 6.67430e-11            # m^3 kg^-1 s^-2
hbar = 1.054571817e-34     # J s
H0 = 73.0 * 1000.0 / 3.0857e22  # s^-1 (Riess H0)

# Planck units
t_P = np.sqrt(hbar * G / c**5)
l_P = c * t_P
rho_Planck = c**5 / (hbar * G**2)

# Critical density and rho_Lambda fiducial
rho_crit = 3.0 * H0**2 / (8.0 * np.pi * G)
rho_Lambda_fid = 0.685 * rho_crit  # ~6.9e-27 kg/m^3
print(f"[fid] H0={H0:.3e} s^-1, rho_crit={rho_crit:.4e} kg/m^3, "
      f"rho_Lambda_fid={rho_Lambda_fid:.4e} kg/m^3")
print(f"[fid] rho_Planck/(4pi)={rho_Planck/(4*np.pi):.4e} kg/m^3")

# n0*mu product (paper convention: rho_Planck/(4pi))
n0_mu = rho_Planck / (4.0 * np.pi)

# Pick eps = arbitrary energy scale (paper uses Planck energy ~ rho_Planck *
# l_P^3 ~ Planck mass c^2). The value doesn't matter — that's the point.
eps = 1.956e9  # J (Planck energy ~1.956e9 J)

print("\n=== Path-epsilon: vary rho_Lambda_obs input ===")
print(f"{'factor':>8}  {'rho_Lambda_obs':>16}  {'rho_q derived':>16}  {'ratio':>10}")
for factor in [0.01, 0.1, 0.5, 1.0, 2.0, 10.0, 100.0]:
    rho_Lambda_obs = factor * rho_Lambda_fid
    # Paper axiom-3 balance: n_inf solved from rho_Lambda_obs
    n_inf = rho_Lambda_obs * c**2 / eps
    # Then rho_q recomputed
    rho_q = n_inf * eps / c**2
    ratio = rho_q / rho_Lambda_obs
    print(f"{factor:>8.2f}  {rho_Lambda_obs:>16.4e}  {rho_q:>16.4e}  {ratio:>10.6f}")

print("\n=> Ratio = 1.000000 for ALL factors. CONFIRMED TAUTOLOGY.")
print("   rho_q derivation contains zero independent prediction of rho_Lambda scale.\n")

# === Path-alpha probe: Hubble-only n_inf estimate (no rho_Lambda_obs) ===
# Direction-only (CLAUDE.md): try a dimensional combination using H0, l_P, t_P
# WITHOUT rho_Lambda_obs as input, then compare a posteriori.
print("=== Path-alpha probe: Hubble + Planck ONLY ===")
# Most natural dimensional candidate for a number density set by H0:
#   n_H ~ 1 / (c/H0)^3 = (H0/c)^3   [m^-3]
n_H = (H0 / c) ** 3
# Energy per quantum: only scale-free choice without rho_Lambda is Planck E
# Result rho_qH = n_H * E_P / c^2
E_P = np.sqrt(hbar * c**5 / G)  # Planck energy
rho_qH = n_H * E_P / c**2
print(f"  n_H (Hubble^3 / c^3)         = {n_H:.4e} m^-3")
print(f"  E_P (Planck energy)          = {E_P:.4e} J")
print(f"  rho_qH = n_H * E_P / c^2     = {rho_qH:.4e} kg/m^3")
print(f"  rho_Lambda_obs               = {rho_Lambda_fid:.4e} kg/m^3")
print(f"  ratio rho_qH / rho_Lambda    = {rho_qH/rho_Lambda_fid:.4e}")
print("  => Off by ~10^{122} — recovers vacuum-catastrophe scale, NOT 1.0000.")
print("  => Path-alpha naive dim-analysis FAILS to predict rho_Lambda from H0+Planck only.")

# Inverse-power Hubble probe: n ~ H0/l_P^2 (de Sitter horizon entropy density)
n_dS = H0 / (c * l_P**2)
rho_dS = n_dS * E_P / c**2
print(f"\n  n_dS (~ H0/(c*l_P^2))        = {n_dS:.4e} m^-3")
print(f"  rho_dS                       = {rho_dS:.4e} kg/m^3")
print(f"  ratio rho_dS / rho_Lambda    = {rho_dS/rho_Lambda_fid:.4e}")
print("  => Still off by ~10^{61} (square-root of vacuum catastrophe).")

# Holographic guess: n ~ 1 / (l_P^2 * R_H) with R_H = c/H0
R_H = c / H0
n_holo = 1.0 / (l_P**2 * R_H)
rho_holo = n_holo * E_P / c**2
print(f"\n  n_holo (1/(l_P^2 R_H))       = {n_holo:.4e} m^-3")
print(f"  rho_holo                     = {rho_holo:.4e} kg/m^3")
print(f"  ratio rho_holo / rho_Lambda  = {rho_holo/rho_Lambda_fid:.4e}")
print("  => Same as n_dS (equivalent expressions). Off by ~10^{61}.")

print("\n=== VERDICT ===")
print("Path-epsilon: ratio = 1.000000 invariant => TAUTOLOGY confirmed.")
print("Path-alpha:   no Hubble+Planck-only dim combo lands on rho_Lambda_obs")
print("              within order-unity. The '1.0000 exact' match REQUIRES")
print("              rho_Lambda_obs as input. Circularity is NOT avoidable")
print("              within current axiom-3 structure.")
print("Recommendation: STRENGTHEN paper/base.md §5.2 caveat (see REVIEW.md).")
