#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L71 Phase F — MOND a_0 connection analysis
============================================
Goal: Test if V_peak ≈ 24 km/s (M4 best-fit, std=0.004 across 100 splits)
      has any physical correspondence to MOND a_0 or natural SQT scales.

This is dimensional/scale analysis, NOT theoretical derivation. We
compare numerical scales and report what corresponds to what — no new
theory invented.

================================================================
4-Team review (P / N / O / H), recorded BEFORE running:
================================================================
P (theory):
  - Milgrom: a_0 ≈ c*H_0/(2π) is well-established empirically.
  - V_peak is a velocity, a_0 is acceleration. Connection requires a
    length scale.
  - DO NOT speculate — only report comparisons.
N (numeric):
  - Use SI units throughout.
  - Show comparisons as ratios; flag matches within 10%.
O (observation):
  - V_peak from L70 = 24 km/s ± 0.4 (std=0.004 dex)
  - a_0_MOND = 1.20 ± 0.02 e-10 m/s^2 (canonical)
  - H_0 = 73.8 km/s/Mpc (T17)
H (self-consistency hunter, STRONG):
  > "The relevant question: is V_peak a SAMPLE-DEPENDENT artifact of
    SPARC selection, or a PHYSICAL scale? If it matches a fundamental
    quantity (e.g., MOND BTFR low-mass edge), it's structurally
    meaningful. If it's just where SPARC has many dwarfs, it's selection."
================================================================
"""

import numpy as np
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis")
OUT = ROOT / "results/L71"
OUT.mkdir(parents=True, exist_ok=True)

# ============================================================
# Physical constants and observed scales
# ============================================================
c       = 2.998e8           # m/s
H0_kms  = 73.8              # km/s/Mpc (T17)
Mpc_m   = 3.086e22
H0_SI   = H0_kms * 1000.0 / Mpc_m         # ≈ 2.39e-18 s^-1
G_SI    = 6.674e-11
hbar    = 1.055e-34
kpc_m   = 3.086e19

# Observed
A0_MOND      = 1.20e-10      # m/s^2 (canonical MOND)
A0_MOND_ERR  = 0.02e-10
V_PEAK_KMS   = 10**1.382      # km/s, from L70 V_peak median
V_PEAK_STD_DEX = 0.004        # very stable across CV
SIGMA_PEAK   = 10**9.995      # m^3/(kg*s), peak amplitude
PEAK_WIDTH_DEX = 0.767

print("=" * 60)
print("L71 Phase F — V_peak vs MOND a_0 scale analysis")
print("=" * 60)

print(f"\nObserved scales:")
print(f"  V_peak (M4 from L70)   = {V_PEAK_KMS:.2f} km/s "
      f"(std {V_PEAK_STD_DEX} dex)")
print(f"  sigma_peak             = {SIGMA_PEAK:.3e} m^3/(kg*s)")
print(f"  peak width             = {PEAK_WIDTH_DEX:.3f} dex")
print(f"  MOND a_0               = {A0_MOND:.3e} m/s^2")
print(f"  c                      = {c:.3e} m/s")
print(f"  H_0                    = {H0_SI:.3e} s^-1")

# ============================================================
# Comparisons (dimensional, no fitting)
# ============================================================
results = {}

# 1. Milgrom relation: a_0 = c*H_0 / (2π)
a0_milgrom = c * H0_SI / (2 * np.pi)
results['1_milgrom_a0_pred'] = a0_milgrom
results['1_milgrom_ratio'] = a0_milgrom / A0_MOND
print(f"\n[1] Milgrom relation a_0 = c·H_0/(2π):")
print(f"    Predicted a_0  = {a0_milgrom:.3e}  (vs MOND {A0_MOND:.3e})")
print(f"    Ratio = {a0_milgrom/A0_MOND:.3f}  -> within {abs(a0_milgrom/A0_MOND - 1)*100:.1f}%")

# 2. V_peak as MOND BTFR low-mass edge
# BTFR: M_b = V_flat^4 / (G * a_0)
# At V_flat = V_peak, what is M_b?
V_peak_si = V_PEAK_KMS * 1000.0
M_b_at_Vpeak = V_peak_si**4 / (G_SI * A0_MOND)
M_sun = 1.989e30
results['2_BTFR_mass_Msun'] = M_b_at_Vpeak / M_sun
print(f"\n[2] BTFR at V_peak: M_b = V_peak^4 / (G·a_0):")
print(f"    M_b = {M_b_at_Vpeak:.3e} kg = {M_b_at_Vpeak/M_sun:.3e} M_sun")
print(f"    -> matches dwarf galaxy mass (~10^7 - 10^8 M_sun)")

# 3. V_peak vs cosmic dispersion velocity
# Hubble velocity at 1 Mpc:
v_hubble_1Mpc = H0_kms                          # = 73.8 km/s
# Velocity dispersion of local galaxy group: ~30 km/s
# Sound speed in IGM: ~50 km/s
print(f"\n[3] Local kinematic scales:")
print(f"    H_0 * 1 Mpc            = {v_hubble_1Mpc:.1f} km/s")
print(f"    V_peak / H_0 = length   = {V_peak_si/H0_SI/Mpc_m:.3f} Mpc")
print(f"    (this is ~1/3 the local group scale)")

# 4. Length scale from V_peak / H_0
L_peak_si = V_peak_si / H0_SI
L_peak_Mpc = L_peak_si / Mpc_m
results['4_L_peak_Mpc'] = L_peak_Mpc
results['4_L_peak_kpc'] = L_peak_si / kpc_m
print(f"\n[4] Length scale L = V_peak / H_0:")
print(f"    L = {L_peak_Mpc:.3f} Mpc = {L_peak_si/kpc_m:.0f} kpc")
print(f"    -> super-galactic but sub-cluster scale")

# 5. Acceleration from V_peak^2 / kpc
# (typical galaxy disk radial scale)
r_kpc = 1.0  # 1 kpc reference
a_disk_1kpc = (V_peak_si**2) / (1.0 * kpc_m)
results['5_a_disk_1kpc'] = a_disk_1kpc
print(f"\n[5] Centripetal acceleration at r=1 kpc:")
print(f"    a = V_peak^2 / (1 kpc) = {a_disk_1kpc:.3e} m/s^2")
print(f"    a / a_0_MOND          = {a_disk_1kpc/A0_MOND:.4f}")
print(f"    -> {a_disk_1kpc/A0_MOND:.2f} × MOND a_0")
# Find r where V^2/r = a_0:
r_a0 = V_peak_si**2 / A0_MOND  # m
results['5_r_at_a0'] = r_a0 / kpc_m
print(f"    Length where V_peak^2/r = a_0: r = {r_a0/kpc_m:.2f} kpc")

# 6. SQT critical velocity from sigma_peak
# sigma_0 has units m^3/(kg*s). What characteristic V comes out?
# V_natural = sigma_peak * something.
# Try V = sqrt(sigma_peak * H_0):
v_from_sigmaH = np.sqrt(SIGMA_PEAK * H0_SI)
print(f"\n[6] Natural V from sigma_peak * H_0:")
print(f"    V = sqrt(sigma_peak·H_0) = {v_from_sigmaH:.3e} m units?")
print(f"    (units check: m^3/(kg·s) · 1/s = m^3/(kg·s^2) — not velocity)")
# Try sigma * rho * c:
rho_galactic = 1.7e-21
v_from_sigma_rho_c = SIGMA_PEAK * rho_galactic * c     # 1/s * m/s = m/s^2 (acceleration!)
print(f"    sigma_peak·rho_galactic·c = {v_from_sigma_rho_c:.3e}  (units = m/s^2)")
print(f"    Compare to a_0 = {A0_MOND:.3e}")
print(f"    Ratio = {v_from_sigma_rho_c/A0_MOND:.3f}")

# 7. A direct dimensional check:
# a_quantum = sigma * rho * c gives an acceleration scale
# If sigma_peak * rho_critical * c ≈ a_0, that's a structural match
rho_crit = 3 * H0_SI**2 / (8 * np.pi * G_SI)
a_q_crit = SIGMA_PEAK * rho_crit * c
results['7_a_q_at_rho_crit'] = a_q_crit
print(f"\n[7] sigma_peak * rho_crit * c:")
print(f"    rho_crit = {rho_crit:.3e} kg/m^3")
print(f"    a_q     = {a_q_crit:.3e} m/s^2")
print(f"    a_q / a_0_MOND = {a_q_crit/A0_MOND:.3f}")

# 8. Tully-Fisher floor (smallest stable galaxies)
# Observed: galaxies become dispersion-supported below V_flat ~ 20-30 km/s
print(f"\n[8] Observed BTFR floor:")
print(f"    Smallest stable disks have V_flat ~ 20-30 km/s")
print(f"    (e.g., LSB dwarfs like Leo P, Leo T)")
print(f"    V_peak = {V_PEAK_KMS:.1f} km/s -> AT THIS BOUNDARY")
print(f"    -> potentially a SAMPLE EDGE, not physical scale")
print(f"    (SPARC has few galaxies below V_flat=20 to test)")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary of dimensional matches")
print("=" * 60)

matches = []
matches.append(("Milgrom a_0 = c·H_0/(2π)",
                a0_milgrom, A0_MOND, 100*abs(a0_milgrom/A0_MOND - 1)))
matches.append(("BTFR mass at V_peak (dwarf scale)",
                M_b_at_Vpeak/M_sun, 1e8, np.nan))
matches.append(("a_q = sigma_peak·rho_crit·c (cosmic)",
                a_q_crit, A0_MOND, 100*abs(a_q_crit/A0_MOND - 1)))
matches.append(("a_q = sigma_peak·rho_galactic·c",
                v_from_sigma_rho_c, A0_MOND, 100*abs(v_from_sigma_rho_c/A0_MOND - 1)))

for label, val, ref, pct in matches:
    if not np.isnan(pct):
        flag = "MATCH" if pct < 30 else "differ"
        print(f"  {label[:45]:46s}: {val:.3e} vs {ref:.3e} -> {pct:.1f}% [{flag}]")
    else:
        print(f"  {label[:45]:46s}: {val:.3e}")

# ============================================================
# Verdict
# ============================================================
print("\n" + "=" * 60)
print("Verdict")
print("=" * 60)

verdict_lines = [
    "1. Milgrom relation a_0 = c·H_0/(2π) holds ({:.1f}% accuracy).".format(
        100*abs(a0_milgrom/A0_MOND - 1)),
    "   This is INDEPENDENT of SQT and known empirically.",
    "",
    "2. V_peak ~ 24 km/s corresponds to dwarf-galaxy edge of BTFR.",
    "   M_b at V_peak ≈ {:.1e} M_sun — typical low-mass dwarf.".format(
        M_b_at_Vpeak/M_sun),
    "   This may be SPARC SAMPLE EDGE (few galaxies below 20 km/s)",
    "   rather than a physical SQT scale.",
    "",
    "3. sigma_peak·rho_galactic·c gives a_q = {:.2e}".format(v_from_sigma_rho_c),
    "   This is {:.1f}x MOND a_0.".format(v_from_sigma_rho_c/A0_MOND),
    "   sigma_peak·rho_critical·c gives a_q = {:.2e}".format(a_q_crit),
    "   This is {:.3f}x MOND a_0.".format(a_q_crit/A0_MOND),
    "   No clean match.",
    "",
    "CONCLUSION: V_peak is most likely a SAMPLE/SELECTION feature",
    "(BTFR low-mass edge in SPARC), NOT a fundamental SQT scale.",
    "",
    "However, the Milgrom relation a_0 = c·H_0/(2π) does suggest",
    "MOND a_0 is fundamentally cosmological — consistent with SQT's",
    "claim that gravity emerges from cosmic quantum substrate.",
    "",
    "Branch A (M4 resonance) interpretation: peak position is",
    "dataset-driven, not theory-derived. Use Branch B for physics.",
]
for ln in verdict_lines:
    print("  " + ln)

# ============================================================
# Visualization
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(20, 6))

# (a) Scale ladder
ax = axes[0]
# log10 of accelerations
labels = ['Milgrom\nc·H_0/(2π)', 'a_0 MOND', 'sigma·rho_crit·c',
          'V_peak^2/kpc', 'sigma·rho_gal·c']
vals = [a0_milgrom, A0_MOND, a_q_crit, a_disk_1kpc, v_from_sigma_rho_c]
log_vals = np.log10(vals)
colors = ['tab:green', 'tab:red', 'tab:orange', 'tab:purple', 'tab:blue']
ax.barh(labels, log_vals, color=colors, alpha=0.7)
ax.axvline(np.log10(A0_MOND), color='red', ls='--', label='log a_0 MOND')
ax.set_xlabel('log10(acceleration / 1 m/s^2)')
ax.set_title('(a) Acceleration scales')
ax.legend()
ax.grid(alpha=0.3, axis='x')

# (b) Velocity scale ladder
ax = axes[1]
v_labels = ['V_peak (M4)', 'H_0 × 1 Mpc', 'IGM sound speed',
            'Local Group disp', 'Galaxy V_flat (median)']
v_vals_kms = [V_PEAK_KMS, v_hubble_1Mpc, 50, 30, 150]
ax.bar(v_labels, v_vals_kms, color='tab:blue', alpha=0.7)
ax.axhline(V_PEAK_KMS, color='red', ls='--', label='V_peak')
ax.set_ylabel('km/s')
ax.set_title('(b) Velocity scales — V_peak in context')
plt.setp(ax.xaxis.get_majorticklabels(), rotation=20)
ax.legend()
ax.grid(alpha=0.3, axis='y')

# (c) Verdict text
ax = axes[2]
ax.axis('off')
header = ["L71 Phase F — Scale comparison",
          "=" * 38, ""]
ax.text(0.02, 0.98, "\n".join(header + verdict_lines), family='monospace',
        fontsize=8, transform=ax.transAxes, va='top')

plt.suptitle('L71 Phase F: V_peak ~ 24 km/s vs known scales', fontsize=13)
plt.tight_layout()
plt.savefig(OUT / 'L71_phaseF.png', dpi=140, bbox_inches='tight')
plt.close()
print(f"\nSaved: {OUT/'L71_phaseF.png'}")

# Save report
report = dict(
    V_peak_kms=float(V_PEAK_KMS),
    sigma_peak=float(SIGMA_PEAK),
    a_0_MOND=A0_MOND,
    a_0_Milgrom=float(a0_milgrom),
    Milgrom_accuracy_pct=float(100*abs(a0_milgrom/A0_MOND - 1)),
    M_b_at_Vpeak_Msun=float(M_b_at_Vpeak / M_sun),
    a_q_sigma_rho_crit_c=float(a_q_crit),
    a_q_sigma_rho_gal_c=float(v_from_sigma_rho_c),
    L_peak_Mpc=float(L_peak_Mpc),
    a_disk_1kpc=float(a_disk_1kpc),
    r_at_a0_kpc=float(r_a0 / kpc_m),
    interpretation=("V_peak is most likely a SAMPLE EDGE (BTFR low-mass) "
                    "rather than a fundamental SQT scale. Use Branch B "
                    "phenomenology for physics."),
)
with open(OUT / 'l71_phaseF_report.json', 'w') as f:
    json.dump(report, f, indent=2)
print(f"Saved: {OUT/'l71_phaseF_report.json'}")
