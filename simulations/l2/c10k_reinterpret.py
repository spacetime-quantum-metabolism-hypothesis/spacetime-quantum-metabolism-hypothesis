# -*- coding: utf-8 -*-
"""
C10k: Phase 3 posterior reinterpretation as dark-only coupling beta_d.

Phase 3.5 (V_RP, r_d free) gave beta ~ 0.107 under universal coupling.
Under C10k (sector-selective dark-only), the SAME numerical posterior is
relabelled beta_d (baryons decouple). Cassini is trivially satisfied
(baryons follow GR geodesics independent of beta_d).

Residual constraint: S_8 tension from enhanced dark-sector growth.
Pourtsidou-Tram PRD 2016 / Amendola-Tsujikawa 2020 result for G_eff:
    G_eff_DM / G = 1 + 2 beta_d^2
acts only on DM clustering, yielding:
    Delta sigma_8 / sigma_8 ~ + beta_d^2 (enhancement)
against Planck sigma_8 = 0.811, local S_8 ~ 0.776 (KiDS-1000).
"""
import numpy as np

# Phase 3.5 V_RP posterior (from run_mcmc_rdfree outputs, hardcoded medians)
beta_median = 0.107
beta_std = 0.05

# Dark-only reinterpretation: numerical values unchanged
beta_d_median = beta_median
beta_d_std = beta_std

# Cassini check under C10k: identically zero (baryon decoupling)
cassini_bound = 2.3e-5
gamma_minus_1_C10k = 0.0  # exact, from c10k_ppn_gamma.py
cassini_margin = cassini_bound / max(gamma_minus_1_C10k, 1e-300)

# S_8 tension estimate
# LCDM Planck: sigma_8 = 0.811 +/- 0.006
# KiDS-1000: S_8 = sigma_8 sqrt(Om/0.3) = 0.766 +/- 0.020
sigma8_planck = 0.811
S8_kids = 0.766
S8_planck = 0.832  # Planck 2018 derived
# Enhancement from dark coupling (Di Porto-Amendola 2008)
# delta sigma_8 / sigma_8 ~ 2 beta_d^2 at linear scale (rough)
rel_enh = 2.0 * beta_d_median**2
sigma8_C10k = sigma8_planck * (1 + rel_enh)
S8_C10k = S8_planck * (1 + rel_enh)

# Tension in sigma: |S8_C10k - S8_kids| / sigma_comb
sigma_comb = np.sqrt(0.006**2 + 0.020**2)
S8_tension_sigma = (S8_C10k - S8_kids) / sigma_comb
delta_chi2_S8 = S8_tension_sigma**2 - ((S8_planck - S8_kids)/sigma_comb)**2

print("=" * 60)
print("C10k Phase 3 posterior reinterpretation")
print("=" * 60)
print(f"Phase 3.5 V_RP median beta    = {beta_median:.4f} +/- {beta_std:.4f}")
print(f"Re-labelled beta_d (dark-only) = {beta_d_median:.4f}")
print()
print(f"Cassini |gamma-1| under C10k  = {gamma_minus_1_C10k} (exact)")
print(f"Margin vs Cassini bound       = infinite (baryon decoupled)")
print()
print(f"sigma_8 (LCDM Planck)         = {sigma8_planck}")
print(f"sigma_8 (C10k enhanced)       = {sigma8_C10k:.4f}")
print(f"Enhancement factor            = {1+rel_enh:.4f}")
print(f"S_8 (Planck-derived)          = {S8_planck}")
print(f"S_8 (C10k)                    = {S8_C10k:.4f}")
print(f"S_8 (KiDS-1000)               = {S8_kids}")
print(f"Tension sigma (C10k vs KiDS)  = {S8_tension_sigma:+.2f}")
print(f"Delta chi^2 vs LCDM tension   = {delta_chi2_S8:+.2f}")
print()
if abs(delta_chi2_S8) < 4:
    print("VERDICT: S_8 tension increment < 4, within acceptable range.")
else:
    print("VERDICT: S_8 tension increment exceeds 4, requires Phase 5 check.")
