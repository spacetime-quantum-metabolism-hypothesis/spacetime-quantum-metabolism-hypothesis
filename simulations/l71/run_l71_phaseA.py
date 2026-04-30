#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L71 Phase A — Branch B settlement + decisive new predictions
==============================================================
Branch B definition (frozen from L67 / L68 / L69):
  Three independent sigma_0 regimes (cosmic / cluster / galactic).
  No single underlying sigma_0; each regime has its own value with
  its own uncertainty.

This script:
  1. Formalizes the Branch B model (parameters and uncertainties).
  2. Computes decisive predictions in three observation channels:
     - T35 environment-dependent inertia (MICROSCOPE-2 / STEP)
     - T36 a_0 redshift evolution (SKA future RC)
     - T26 GW dispersion (LIGO/ET/CE)
  3. For each prediction, records:
     - SQT/Branch B prediction
     - Standard physics (LCDM/GR) baseline
     - Discriminating signature
     - Required experimental sensitivity

================================================================
4-Team review (P / N / O / H), recorded BEFORE running:
================================================================
P (theory):
  - In Branch B, sigma_0 is REGIME-LOCAL. Earth lab is fully in the
    galactic regime; thus equivalence-principle tests on Earth or
    near-Earth orbit cannot probe SQT environmental dependence
    UNLESS the spacecraft transitions between regimes (impossible
    locally).
  - Real T35 prediction: equivalence principle SAFE to high precision.
    SQT does NOT predict violation under MICROSCOPE-2.
N (numeric):
  - Predictions should be quantitative whenever a sigma_0 ratio
    enters. Where Branch B predicts "no effect", state the bound.
O (observation):
  - For T36, SKA will measure rotation curves to z~3. Predict a_0(z)
    invariance under Branch B (galactic regime preserved).
  - For T26, LIGO/ET reach kHz; SQT GW dispersion bound from GW170817
    is |c_g - c|/c < 1e-15. This is an UPPER bound; SQT has no
    further specification yet.
H (self-consistency hunter, STRONG):
  > "Branch B predictions are mostly NULL (= no effect). This is a
    STRONG falsifiable prediction: any positive detection of EP
    violation, a_0 evolution, or GW dispersion KILLS Branch B."
  > "The single positive prediction worth fighting for: dwarf
    galaxies in CLUSTER environment vs FIELD environment should have
    THE SAME a_0 (since both are galactic regime). If a difference
    is found, Branch B fails."
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
# Branch B frozen parameters
# ============================================================
BRANCH_B = {
    'cosmic'  : dict(log_sigma=8.37, sigma=10**8.37, syst_dex=0.06,
                     domain="rho < 1e-26 kg/m^3 (intergalactic, voids)"),
    'cluster' : dict(log_sigma=7.75, sigma=10**7.75, syst_dex=0.06,
                     domain="1e-26 < rho < 1e-22 kg/m^3 (clusters, IGM)"),
    'galactic': dict(log_sigma=9.56, sigma=10**9.56, syst_dex=0.05,
                     domain="rho > 1e-22 kg/m^3 (galaxies, solar system, planets)"),
}

# Reference: sigma_0 spread across regimes
log_sig_arr = np.array([BRANCH_B[k]['log_sigma'] for k in BRANCH_B])
sigma_max_min = np.max(log_sig_arr) - np.min(log_sig_arr)

print("=" * 60)
print("L71 Phase A — Branch B frozen + decisive predictions")
print("=" * 60)

print("\nBranch B 3-regime sigma_0 (frozen):")
for name, p in BRANCH_B.items():
    print(f"  {name:9s}: log10 sigma_0 = {p['log_sigma']:.2f} +- {p['syst_dex']:.2f} dex")
    print(f"             sigma_0 = {p['sigma']:.3e} m^3/(kg·s)")
    print(f"             domain: {p['domain']}")
print(f"\n  Total span: {sigma_max_min:.2f} dex")

# Constants
c     = 2.998e8
H0_SI = 73.8e3 / 3.086e22
G     = 6.674e-11
A0_MOND = 1.20e-10

# ============================================================
# T35 — Environment-dependent inertia (MICROSCOPE-2)
# ============================================================
print("\n" + "=" * 60)
print("T35: Environment-dependent inertia (MICROSCOPE-2 / STEP)")
print("=" * 60)

T35 = {}

# Earth lab and LEO are both in galactic regime (rho > 1e-22)
# No regime crossing => no SQT-induced EP violation
T35['regime_lab']      = 'galactic'
T35['regime_LEO']      = 'galactic'
T35['regime_crossing'] = False
# Bound from MICROSCOPE-1: eta < 1e-15 (Touboul+2017)
T35['MICROSCOPE_1_bound']  = 1e-15
# Branch B predicts no further violation; eta_SQT < eta_observed
T35['Branch_B_prediction'] = "eta_EP < 1e-15 (no SQT violation in galactic regime)"
T35['Branch_B_signature']  = ("EP violation if and only if test masses "
                               "differ in environmental regime — "
                               "impossible on Earth or LEO.")
T35['MICROSCOPE_2_target'] = 1e-17  # planned
T35['discriminator']       = ("Detection of eta > 1e-17 in MICROSCOPE-2 "
                               "would falsify Branch B (no regime crossing "
                               "available).")

print("  Lab regime       : galactic")
print("  LEO regime       : galactic (same)")
print("  No regime crossing => no SQT-induced EP violation locally")
print("  Branch B: eta < 1e-15 (consistent with MICROSCOPE-1)")
print("  Falsifier: any positive eta detection by MICROSCOPE-2")

# ============================================================
# T36 — a_0 redshift evolution (SKA, JWST)
# ============================================================
print("\n" + "=" * 60)
print("T36: a_0(z) evolution (SKA RC at z>1)")
print("=" * 60)

T36 = {}

# In Branch B, galactic regime is defined by LOCAL density (rho > 1e-22)
# A galaxy at z=2 with similar local rho is still in galactic regime
# => sigma_0_galactic invariant => a_0 invariant

# But: at high z, galaxies have SYSTEMATICALLY different baryon densities
# (more compact, higher central density). Test if a_0 measured for
# z~2 galaxies matches z~0 SPARC value.
T36['Branch_B_a0_z']  = "a_0(z) = a_0(0) (constant)"
T36['Branch_B_basis'] = ("Galactic regime is LOCAL density-defined; "
                          "high-z galaxies still satisfy rho > 1e-22.")
T36['SKA_target']     = "Measure a_0 to ~5% at z=1, ~15% at z=2"
T36['discriminator']  = ("a_0(z=2)/a_0(z=0) different from 1.0 at >2sigma "
                          "would falsify Branch B's regime stability claim.")

# Quantitative: log(sigma_0) varies < 0.05 dex across z under Branch B
# => log(a_0) varies < 0.05 dex => a_0(z)/a_0(0) within 12%
T36['allowed_a0_variation_dex'] = 0.05
T36['allowed_a0_ratio']         = 10**0.05  # 1.122
print(f"  Branch B prediction: a_0(z) constant within {0.05*100:.0f}% (sigma_0 syst)")
print(f"  SKA precision needed: ~5% at z=1 -> just barely discriminating")
print(f"  Falsifier: a_0(z=2) > 1.12 * a_0(0) at >2 sigma")

# ============================================================
# T26 — GW dispersion (LIGO, ET, CE)
# ============================================================
print("\n" + "=" * 60)
print("T26: GW dispersion (LIGO/ET/CE)")
print("=" * 60)

T26 = {}

# GW170817 (LIGO + EM counterpart) constrained |c_gw - c|/c < 1e-15 at ~100 Hz
# (Abbott+2017)
T26['GW170817_bound']  = 1e-15

# In SQT, GW propagation through quantum substrate has a frequency-
# dependent coupling u_0 (free parameter). Constrained by:
T26['Branch_B_u_0_bound']  = "|u_0| < 1e-15 at ~100 Hz (LIGO/Virgo)"

# At higher frequency (kHz, ET) or lower (mHz, LISA), bound may
# weaken or strengthen. SQT does not yet specify frequency dependence.
T26['ET_target']      = "kHz, sensitive to ~10x better dispersion bound"
T26['LISA_target']    = "mHz, sensitive to dispersion at low f"
T26['discriminator']  = ("Frequency-dependent c_gw - c detection by "
                          "ET or LISA would discover SQT GW coupling. "
                          "Null result tightens u_0 bound.")

print(f"  GW170817 bound: |c_gw-c|/c < 1e-15")
print(f"  Branch B prediction: same bound applies in galactic regime")
print(f"  ET / LISA: extend to other frequencies")
print(f"  Falsifier: frequency-dependent GW dispersion at f != 100 Hz")

# ============================================================
# Aggregate decisive signatures
# ============================================================
print("\n" + "=" * 60)
print("Aggregate decisive signatures (Branch B falsifiers)")
print("=" * 60)

signatures = [
    ("MICROSCOPE-2 EP violation", "eta > 1e-17", T35['MICROSCOPE_2_target']),
    ("a_0(z) evolution",          ">12% deviation",
                                   "SKA z=2 RCs"),
    ("GW dispersion (any f)",     ">1e-15 at any f",
                                   "ET/CE/LISA"),
    ("Field vs cluster dwarf a_0", ">0.05 dex difference",
                                   "Future SPARC + cluster surveys"),
    ("Within-galactic-regime EP", "any violation",
                                   "Spacecraft EP test in deep space"),
]
for sig, threshold, expt in signatures:
    print(f"  - {sig:40s}: {threshold:25s} via {expt}")

# ============================================================
# Visualization
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(16, 11))

# (a) Branch B sigma_0 spectrum
ax = axes[0, 0]
names = list(BRANCH_B.keys())
log_sigs = [BRANCH_B[k]['log_sigma'] for k in names]
errs     = [BRANCH_B[k]['syst_dex'] for k in names]
log_rho  = [-26.5, -23.5, -20.8]
ax.errorbar(log_rho, log_sigs, yerr=errs, fmt='ks',
            markersize=14, capsize=8, label='Branch B regimes')
for x, y, n in zip(log_rho, log_sigs, names):
    ax.annotate(n, (x, y), textcoords='offset points', xytext=(8, 8),
                fontsize=11)
# Show regime boundaries
ax.axvline(-26, color='gray', ls=':', alpha=0.5)
ax.axvline(-22, color='gray', ls=':', alpha=0.5)
ax.fill_betweenx([7, 10], -32, -26, alpha=0.1, color='blue', label='cosmic')
ax.fill_betweenx([7, 10], -26, -22, alpha=0.1, color='orange', label='cluster')
ax.fill_betweenx([7, 10], -22, -18, alpha=0.1, color='red', label='galactic')
ax.set_xlim(-30, -19)
ax.set_xlabel('log10(rho) [kg/m^3]')
ax.set_ylabel('log10(sigma_0)')
ax.set_title('(a) Branch B frozen sigma_0 spectrum')
ax.legend(fontsize=9)
ax.grid(alpha=0.3)

# (b) T35 EP bounds
ax = axes[0, 1]
labels = ['MICROSCOPE-1\n(2017)', 'MICROSCOPE-2\n(target)', 'STEP\n(planned)',
          'Branch B\nprediction']
bounds = [1e-15, 1e-17, 1e-18, 1e-15]   # last is Branch B's claim it's ≤ existing
colors = ['gray', 'tab:orange', 'tab:red', 'tab:green']
ax.bar(labels, bounds, color=colors, alpha=0.7, log=True)
ax.set_ylabel('|eta| EP violation bound')
ax.set_yscale('log')
ax.axhline(1e-15, color='red', ls='--', alpha=0.5,
           label='Branch B claims eta < 1e-15')
ax.set_title('(b) T35: EP violation bounds')
ax.legend(fontsize=9)
ax.grid(alpha=0.3, axis='y', which='both')
plt.setp(ax.xaxis.get_majorticklabels(), rotation=15)

# (c) T36 a_0(z)
ax = axes[1, 0]
zs = np.linspace(0, 3, 100)
ax.fill_between(zs, A0_MOND * 10**(-0.05), A0_MOND * 10**(0.05),
                alpha=0.3, color='tab:green', label='Branch B (constant ±5%)')
ax.axhline(A0_MOND, color='black', label='a_0 today')
# Hypothetical evolving a_0 (10% per unit z)
a0_evolving = A0_MOND * (1 + 0.1*zs)
ax.plot(zs, a0_evolving, 'r--', label='Falsifier: 10%/z evolution')
ax.set_xlabel('redshift z')
ax.set_ylabel('a_0 (m/s^2)')
ax.set_title('(c) T36: a_0(z) — Branch B vs falsifier')
ax.legend(fontsize=9)
ax.grid(alpha=0.3)

# (d) Verdict / summary
ax = axes[1, 1]
ax.axis('off')
lines = [
    "L71 Phase A — Branch B Settlement",
    "=" * 40,
    "",
    "FROZEN PARAMETERS:",
    f"  cosmic   sigma_0 = 10^8.37 ± 0.06",
    f"  cluster  sigma_0 = 10^7.75 ± 0.06",
    f"  galactic sigma_0 = 10^9.56 ± 0.05",
    "",
    "DECISIVE PREDICTIONS:",
    "",
    "T35 (MICROSCOPE-2):",
    "  eta_EP < 1e-15 (NULL prediction)",
    "  Falsifier: any eta > 1e-17 detection",
    "",
    "T36 (SKA, RC at z>1):",
    "  a_0(z)/a_0(0) = 1.000 ± 0.122",
    "  Falsifier: deviation > 12% at >2sigma",
    "",
    "T26 (LIGO/ET/CE):",
    "  |c_gw - c|/c < 1e-15 (current bound)",
    "  Falsifier: freq-dependent dispersion",
    "",
    "POSITIVE TEST (Field vs Cluster Dwarf):",
    "  a_0(field) = a_0(cluster) within ±0.05 dex",
    "  Falsifier: different a_0 at >2sigma",
    "",
    "STATUS:",
    "  Branch B = phenomenological 'safe haven'",
    "  All predictions are FALSIFIABLE (***5)",
    "  No undertheorised free parameters added",
    "",
    "Branch A (M4 resonance) BOOK-MARKED",
    "for L72 if dwarf data extended (option B).",
]
ax.text(0.02, 0.98, "\n".join(lines), family='monospace', fontsize=9,
        transform=ax.transAxes, va='top')

plt.suptitle('L71 Phase A: Branch B settlement + decisive predictions', fontsize=13)
plt.tight_layout()
plt.savefig(OUT / 'L71_phaseA.png', dpi=140, bbox_inches='tight')
plt.close()
print(f"\nSaved: {OUT/'L71_phaseA.png'}")

# Save report
def _j(o):
    if isinstance(o, (np.bool_, bool)): return bool(o)
    if isinstance(o, (np.integer, int)): return int(o)
    if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else None
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, dict): return {k: _j(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_j(x) for x in o]
    return o

report = dict(
    branch_B=BRANCH_B,
    sigma_span_dex=float(sigma_max_min),
    T35=T35,
    T36=T36,
    T26=T26,
    decisive_signatures=signatures,
)
with open(OUT / 'l71_phaseA_report.json', 'w') as f:
    json.dump(_j(report), f, indent=2)
print(f"Saved: {OUT/'l71_phaseA_report.json'}")
