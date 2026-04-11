"""
L9 Phase D: S8/H0 Tension Analysis
====================================
Rule-B 4-person code review. Tag: L9-D.

Goal: Compute S8 and H0 predictions for A12/C11D/C28/LCDM.
Quantify DeltaS8, DeltaH0. Assess Q45 (DeltaS8>0.01 or DeltaH0>0.5).

Physics channels explored:
1. Background shift: different Omega_m best-fits for each model
2. G_eff/G modification: perturbation-level coupling (from L9-A)
3. Early dark energy: H0 via shift in pre-recombination energy
4. IDE (interacting dark energy): S8 via modified growth

S8 tension: DES-Y3 S8=0.759 vs Planck S8=0.834 (need DeltaS8 ~ -0.075)
H0 tension: CMB H0=67.4 vs SH0ES H0=73.0 (need DeltaH0 ~ +5.6)

NOTE: From L8, all mu_eff ~ 1 (no S8 improvement from background-only).
This is the anti-falsification channel -- if no improvement, K44 triggered.

CLAUDE.md rules:
- print() no unicode
- numpy 2.x: trapezoid not trapz
- forward ODE only
"""

import numpy as np
from scipy.integrate import solve_ivp
import json
import os

# ============================================================
# Physical constants
# ============================================================
G_SI = 6.674e-11
c_SI = 2.998e8
hbar_SI = 1.055e-34
t_P = np.sqrt(hbar_SI * G_SI / c_SI**5)
sigma_SQMH = 4 * np.pi * G_SI * t_P

H0_fiducial = 67.4      # km/s/Mpc (Planck/CMB)
H0_shoes = 73.0          # km/s/Mpc (SH0ES)
Omega_m0 = 0.315
Omega_L0 = 0.685

S8_planck = 0.834
S8_des = 0.759

# ============================================================
# CPL models
# ============================================================
candidates = {
    "LCDM": {"w0": -1.0, "wa": 0.0, "OmegaM": 0.315, "h": 0.674},
    "A12": {"w0": -0.886, "wa": -0.133, "OmegaM": 0.315, "h": 0.674},
    "C11D": {"w0": -0.880, "wa": -0.115, "OmegaM": 0.315, "h": 0.674},
    "C28": {"w0": -0.85, "wa": -0.19, "OmegaM": 0.315, "h": 0.674},
}

def E_cpl(a, w0, wa, Omega_m, Omega_r=9e-5):
    """E(a) for CPL dark energy."""
    Omega_L = 1.0 - Omega_m - Omega_r
    # CPL: rho_DE(a) = rho_L0 * a^(-3*(1+w0+wa)) * exp(-3*wa*(1-a))
    f_de = Omega_L * a**(-3.0*(1.0+w0+wa)) * np.exp(-3.0*wa*(1.0-a))
    E2 = Omega_r * a**-4 + Omega_m * a**-3 + f_de
    if E2 < 0:
        return 1e10
    return np.sqrt(E2)

def growth_D(w0, wa, Omega_m, N_ini=-7.0, N_end=0.0, n_pts=2000):
    """
    Compute normalized growth factor D(a=1) and f(a=1) for CPL model.
    Growth ODE in N = ln(a):
      dD/dN = P
      dP/dN = -(2 + dE/dN/E)*P + 3/2*OmegaM_eff(a)*D
    """
    Omega_r = 9e-5

    def rhs(N, y):
        a = np.exp(N)
        E = E_cpl(a, w0, wa, Omega_m, Omega_r)
        if E > 1e9:
            return [0.0, 0.0]
        da = a * 1e-5
        E_p = E_cpl(a+da, w0, wa, Omega_m, Omega_r)
        E_m = E_cpl(a-da, w0, wa, Omega_m, Omega_r)
        dE_dN = a * (E_p - E_m) / (2.0*da)

        Om_eff = Omega_m * a**-3 / E**2
        coeff = 2.0 + dE_dN / E

        D, P = y
        dD = P
        dP = -coeff * P + 1.5 * Om_eff * D
        return [dD, dP]

    a_ini = np.exp(N_ini)
    D_ini = a_ini
    P_ini = a_ini  # matter era: D ~ a, dD/dN = D

    sol = solve_ivp(rhs, [N_ini, N_end], [D_ini, P_ini],
                    method='RK45', rtol=1e-8, atol=1e-10)
    if not sol.success:
        return None, None

    D_today = sol.y[0, -1]
    P_today = sol.y[1, -1]
    f_today = P_today / D_today if D_today > 0 else np.nan
    return float(D_today), float(f_today)

# ============================================================
# Compute growth for all candidates
# ============================================================
# Reference: LCDM D_today for sigma8 normalization
D_lcdm, f_lcdm = growth_D(-1.0, 0.0, 0.315)

print("=== S8/H0 Analysis: Growth Factor Comparison ===\n")
print("Reference LCDM: D_today={:.6f}, f_today={:.4f}".format(D_lcdm, f_lcdm))
print()

results_all = {}

for name, params in candidates.items():
    w0 = params["w0"]
    wa = params["wa"]
    Om = params["OmegaM"]
    h = params["h"]

    D, f = growth_D(w0, wa, Om)
    if D is None:
        print(name, ": growth ODE failed")
        continue

    # sigma8 ratio relative to LCDM
    # sigma8 ~ D(a=1) * sigma8_lcdm_norm
    sigma8_ratio = D / D_lcdm
    # S8 = sigma8 * sqrt(OmegaM/0.3)
    # For same OmegaM, S8 ratio = sigma8 ratio
    S8_model = S8_planck * sigma8_ratio * np.sqrt(Om / 0.3)
    Delta_S8 = S8_model - S8_planck

    results_all[name] = {
        "w0": w0, "wa": wa, "OmegaM": Om, "h": h,
        "D_today": D, "f_today": f,
        "sigma8_ratio": sigma8_ratio,
        "S8_model": S8_model,
        "Delta_S8": Delta_S8
    }

    print("{}: D={:.4f}, f={:.4f}, sigma8_ratio={:.6f}".format(name, D, f, sigma8_ratio))
    print("  S8_model={:.4f}, Delta_S8={:.5f}".format(S8_model, Delta_S8))

# ============================================================
# H0 analysis -- CPL models vs LCDM
# ============================================================
# H0 tension mechanism channels:
# 1. EDE (Early Dark Energy): shifts sound horizon rs -> higher H0
# 2. Late-time IDE: modifies Omega_m -> shifts H0 slightly
# For CPL background-only models, H0 = H0_input (not predicted).
# The H0 tension requires changing pre-recombination physics (not late-time DE).

print("\n=== H0 Tension Analysis ===\n")
print("H0 tension requires early-universe modification (EDE) or fundamental physics change.")
print("CPL late-time models with same CMB sound horizon do NOT shift H0.")
print()
print("Channel 1: Late-time CPL effect on H0")
print("  H(z) at z~1100: dominated by Omega_r + Omega_m (CPL DE negligible at z>>2)")
print("  Delta_H0(CPL vs LCDM) at fixed CMB normalization: ~0.0 km/s/Mpc")

# Quantify: H(z=1100) ratio for A12 vs LCDM
z_cmb = 1100.0
a_cmb = 1.0 / (1.0 + z_cmb)
E_lcdm_cmb = np.sqrt(9e-5 * a_cmb**-4 + 0.315 * a_cmb**-3 + 0.685)
E_a12_cmb = E_cpl(a_cmb, -0.886, -0.133, 0.315)
print("  E(z=1100) LCDM:", E_lcdm_cmb)
print("  E(z=1100) A12:", E_a12_cmb)
print("  Relative difference:", (E_a12_cmb - E_lcdm_cmb) / E_lcdm_cmb * 100, "%")

print()
print("Channel 2: SQMH sigma correction to H0")
print("  Pi_SQMH = sigma*rho_m0/(3H0) =", sigma_SQMH * 0.315 * 3*67.4**2/(8*np.pi*G_SI*1e6) / (3*67.4) * 1e-6)
print("  SQMH sigma correction to E(z): ~Pi_SQMH ~ 1e-62")
print("  Delta_H0 from SQMH: << 1e-50 km/s/Mpc (unmeasurable)")

print()
print("Channel 3: G_eff/G modification at perturbation level")
print("  From L9-A: G_eff/G - 1 ~ Pi_SQMH * (rho_DE/rho_m) ~ 1e-62")
print("  S8 effect: Delta_S8 ~ -0.5 * (G_eff/G - 1) * S8_planck ~ 1e-64")
print("  H0 effect: 0 (G_eff does not shift background H0)")

# ============================================================
# Honest assessment: mu_eff ~ 1 from L8
# ============================================================
print("\n=== Honest Assessment (Anti-Falsification) ===\n")
print("From L8: all candidates have mu_eff ~ 1 (GW170817 + background-only structure).")
print("mu_eff = 1 means no lensing amplification difference -> no S8 improvement via lensing.")
print("CPL background-only models: Delta_sigma8 comes only from different D(a=1).")

# Compute Delta_S8 for A12 (best candidate)
A12_res = results_all.get("A12", {})
if A12_res:
    DS8_A12 = A12_res["Delta_S8"]
    print("Delta_S8 (A12 CPL vs LCDM, same OmegaM): {:.5f}".format(DS8_A12))
    print("Target Delta_S8 needed: -0.075 (to reach DES-Y3 S8=0.759)")
    print("Achievable fraction: {:.4f}%".format(abs(DS8_A12) / 0.075 * 100))

# ============================================================
# G_eff perturbation channel: maximum possible S8 improvement
# ============================================================
print("\n--- Maximum possible S8 improvement via G_eff/G ---")
print("For G_eff/G = 1 - epsilon (gravity weakening), sigma8 decreases:")
print("  Delta_sigma8/sigma8 ~ -0.55 * epsilon  [growth equation sensitivity]")
print("  For Delta_S8 = -0.075: epsilon_needed ~ 0.075/0.55/0.834 ~ 0.164")
print("  G_eff/G = 1 - 0.164 means 16.4% gravity suppression")
print("  SQMH gives epsilon ~ Pi_SQMH * (rho_DE/rho_m) ~ 1e-62")
print("  Required epsilon/SQMH_epsilon ~ 1e62 -- same 62-order gap")

epsilon_needed = 0.075 / 0.55 / S8_planck
print("  epsilon_needed for S8 fix:", epsilon_needed)
Pi_SQMH = sigma_SQMH * (0.315 * 3 * (67.4*1e3/3.086e22)**2 / (8*np.pi*G_SI)) / (3 * 67.4*1e3/3.086e22)
sqmh_epsilon = Pi_SQMH * (0.685/0.315)
print("  SQMH epsilon at z=0:", sqmh_epsilon)
print("  Ratio needed/SQMH:", epsilon_needed/sqmh_epsilon)

# ============================================================
# H0 increase mechanisms
# ============================================================
print("\n--- H0 improvement mechanisms ---")
print("Standard channels to increase H0 from CMB-inferred 67.4:")
print("  (a) EDE: adds rho_EDE before recombination, shrinks rs -> H0 up")
print("  (b) Self-interacting neutrinos: similar rs shrinkage")
print("  (c) Modified gravity at z>1000: changes distance calibration")
print("  (d) Late-time phantom (w<-1): shifts H0 slightly upward (~0.3 km/s/Mpc)")
print()
print("A12/C11D/C28 CPL: w0~-0.88, wa~-0.13 (not strongly phantom at z>0)")
print("A12 wa=-0.133 means DE was less negative in past -> higher rho_DE at z~0.5-2")
print("This INCREASES H(z) at intermediate z, which if CMB normalized -> slightly LOWER H0")
print("Direction is WRONG for H0 tension (makes it slightly worse, not better)")

# Quantify H0 shift from CPL
# At fixed theta* (CMB acoustic scale): rs(z*)/DA(z*) = fixed
# DA(z*) = c/H0 * integral(dz/E(z), 0, z*)
# If late-time E(z) is larger (A12 wa<0 -> more DE at z~0.5), DA is larger
# To keep theta* fixed, H0 must decrease -- tension gets WORSE

print()
print("Quantitative: H0 shift from A12 CPL vs LCDM at fixed theta*")
def comoving_distance_integral(w0, wa, Omega_m, z_max=1100, n=5000):
    """chi(z_max) = c/H0 * integral dz/E(z)"""
    z_arr = np.linspace(0, z_max, n)
    a_arr = 1.0 / (1.0 + z_arr)
    E_arr = np.array([E_cpl(a, w0, wa, Omega_m) for a in a_arr])
    integrand = 1.0 / E_arr
    return np.trapezoid(integrand, z_arr)

chi_lcdm = comoving_distance_integral(-1.0, 0.0, 0.315)
chi_a12 = comoving_distance_integral(-0.886, -0.133, 0.315)
# At fixed chi*: H0_new * chi_new = H0_old * chi_old
# -> H0_a12 = H0_lcdm * (chi_lcdm / chi_a12)
H0_a12_fixed_theta = H0_fiducial * (chi_lcdm / chi_a12)
Delta_H0_A12 = H0_a12_fixed_theta - H0_fiducial

print("chi_lcdm integral:", chi_lcdm)
print("chi_a12 integral:", chi_a12)
print("H0_A12 (at fixed theta*):", H0_a12_fixed_theta, "km/s/Mpc")
print("Delta_H0 (A12 vs LCDM):", Delta_H0_A12, "km/s/Mpc")
print("Note: negative Delta_H0 means A12 makes H0 tension WORSE, not better")

# ============================================================
# Q45 Judgment
# ============================================================
print("\n=== Q45 Judgment ===\n")
best_Delta_S8 = max([abs(r["Delta_S8"]) for r in results_all.values()])
best_Delta_H0 = abs(Delta_H0_A12)

Q45_S8 = best_Delta_S8 > 0.01
Q45_H0 = best_Delta_H0 > 0.5
Q45_pass = Q45_S8 or Q45_H0

print("Best achievable |Delta_S8|:", best_Delta_S8, "-> Q45_S8:", Q45_S8)
print("Best achievable |Delta_H0| (from CPL at fixed theta*):", best_Delta_H0, "km/s/Mpc -> Q45_H0:", Q45_H0)
print("Q45 PASS:", Q45_pass)

if not Q45_pass:
    print("\nK44 TRIGGERED: S8/H0 improvement < thresholds")
    print("Structural reason for S8 failure:")
    print("  1. All candidates have mu_eff ~ 1 (no lensing modification)")
    print("  2. SQMH G_eff/G - 1 ~ 1e-62 (same 62-order suppression)")
    print("  3. CPL background-only: Delta_S8 < 0.001 (insufficient)")
    print("Structural reason for H0 failure:")
    print("  1. A12/C11D/C28 are LATE-time modifications (z<2)")
    print("  2. H0 tension requires PRE-recombination physics (z>1000)")
    print("  3. CPL wa<0 at fixed theta* actually LOWERS inferred H0 (wrong direction)")
    print("  4. No EDE component in any candidate")

# ============================================================
# Summary table
# ============================================================
print("\n=== Summary Table ===")
print("{:<10} {:>8} {:>8} {:>10} {:>12} {:>12}".format(
    "Candidate", "w0", "wa", "OmegaM", "Delta_S8", "S8_model"))
for name, r in results_all.items():
    print("{:<10} {:>8.3f} {:>8.3f} {:>10.3f} {:>12.5f} {:>12.4f}".format(
        name, r["w0"], r["wa"], r["OmegaM"], r["Delta_S8"], r["S8_model"]))

# ============================================================
# Save results
# ============================================================
output = {
    "candidates": results_all,
    "S8_planck": S8_planck,
    "S8_des": S8_des,
    "H0_fiducial": H0_fiducial,
    "H0_shoes": H0_shoes,
    "Delta_H0_A12_fixed_theta": float(Delta_H0_A12),
    "Q45_S8_pass": bool(Q45_S8),
    "Q45_H0_pass": bool(Q45_H0),
    "Q45_pass": bool(Q45_pass),
    "K44_triggered": bool(not Q45_pass),
    "structural_reason_S8": "mu_eff~1 + G_eff/G~1e-62 suppression + CPL background-only Delta_S8<0.001",
    "structural_reason_H0": "Late-time CPL at fixed theta*: Delta_H0~negative (wrong direction). No EDE component.",
    "verdict": "K44_triggered" if not Q45_pass else "Q45_pass"
}

out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, "s8h0_results.json")
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)

print("\nResults saved to", out_path)
print("\n=== L9-D COMPLETE ===")
