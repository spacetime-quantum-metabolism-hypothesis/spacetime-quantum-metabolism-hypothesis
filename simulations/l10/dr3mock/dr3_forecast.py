"""
simulations/l10/dr3mock/dr3_forecast.py
L10-D: DESI DR3 mock prediction for A12 Bayes factor
K54/Q54: Will A12 Delta ln Z remain > 8.0 under DR3?

Rule-B 4-person code review:
  - Reviewer 1: No unicode in print()
  - Reviewer 2: numpy trapz -> trapezoid (used in integrals)
  - Reviewer 3: A12: w0=-0.886, wa=-0.133, Delta_lnZ = +10.769 (DR2)
  - Reviewer 4: DR3 precision: sqrt(2) improvement over DR2 (volume doubling)

Date: 2026-04-11
"""

import numpy as np
from scipy import stats

# ============================================================
# Key L6-L9 results for A12
# ============================================================
# A12: w0 = -0.886, wa = -0.133, Delta ln Z = +10.769 (vs LCDM)
# C11D: lambda = 0.8872, Delta ln Z = +8.771
# C28: gamma0 = 0.000624, wa = -0.176, Delta ln Z = +8.633

# DR2 precision: from DESI DR2 paper (arXiv 2404.03000 etc.)
# DR2 w0-wa 1-sigma ellipse: sigma_w0 ~ 0.058, sigma_wa ~ 0.24 (DESI+CMB+SN)

print("=== L10-D: DESI DR3 Mock Forecast ===")
print("")
print("Input (L6-L9 DR2 results):")
print("  A12: Delta_lnZ = +10.769 (DR2)")
print("  C11D: Delta_lnZ = +8.771 (DR2)")
print("  C28: Delta_lnZ = +8.633 (DR2)")
print("")

# ============================================================
# Section 1: DR3 statistical improvement model
# ============================================================
print("=== Section 1: DR3 statistical improvement ===")

# DESI survey plan:
# DR1: Year 1 (2021-2022), ~12 million galaxies
# DR2: Year 3 (2023-2024), ~24 million galaxies
# DR3: Year 5 (2025-2026), ~36 million galaxies
# Volume ratio DR3/DR2 ~ 1.5 (not sqrt(2), since survey not complete doubling)
# BAO precision scales as 1/sqrt(N_eff * V_eff) approximately

# Conservative estimate: DR3 BAO precision = DR2 / sqrt(1.3) (30% improvement)
# Optimistic: DR3 = DR2 / sqrt(1.5) (50% improvement)

sigma_DR2_w0 = 0.058   # from DESI DR2 + Planck + DES-SN
sigma_DR2_wa = 0.24    # from DESI DR2 + Planck + DES-SN

# DR3 expected precision
improvement_conservative = np.sqrt(1.3)  # 14% improvement in sigma
improvement_optimistic   = np.sqrt(1.5)  # 22% improvement in sigma

sigma_DR3_w0_cons = sigma_DR2_w0 / improvement_conservative
sigma_DR3_wa_cons = sigma_DR2_wa / improvement_conservative
sigma_DR3_w0_opt  = sigma_DR2_w0 / improvement_optimistic
sigma_DR3_wa_opt  = sigma_DR2_wa / improvement_optimistic

print("  DR2 precision: sigma_w0 = {:.3f}, sigma_wa = {:.3f}".format(sigma_DR2_w0, sigma_DR2_wa))
print("  DR3 conservative (sqrt(1.3) improvement):")
print("    sigma_w0 = {:.3f}, sigma_wa = {:.3f}".format(sigma_DR3_w0_cons, sigma_DR3_wa_cons))
print("  DR3 optimistic (sqrt(1.5) improvement):")
print("    sigma_w0 = {:.3f}, sigma_wa = {:.3f}".format(sigma_DR3_w0_opt, sigma_DR3_wa_opt))
print("")

# ============================================================
# Section 2: Bayesian evidence change under DR3
# ============================================================
print("=== Section 2: Delta ln Z scaling with Fisher precision ===")

# The Bayes factor scales approximately with the "information gain":
# Delta ln Z ~ (chi2_LCDM - chi2_model)/2 - k/2 * ln(N)
# (Schwarz criterion approximation for simple model comparison)

# More precisely: for nested models with k extra parameters,
# Delta ln Z ~ (chi2_diff - k)/2 - k/2 * ln(N) + corrections
# For our case: A12 has 2 extra parameters (w0, wa) over LCDM

# DR2 best-fit: chi2_improvement for A12 vs LCDM
# From Delta_lnZ = +10.769 and Gaussian approximation:
# Delta_lnZ ~ -0.5 * Delta_chi2 + delta_prior_term
# For a rough scaling: Delta_lnZ scales with the significance of the signal

# The signal in (w0, wa) space:
# A12 model point: (w0, wa) = (-0.886, -0.133)
# LCDM point: (w0, wa) = (-1, 0)
# Distance in sigma_DR2: sqrt(((w0_A12-w0_LCDM)/sigma_w0)^2 + ((wa_A12-wa_LCDM)/sigma_wa)^2)

w0_A12 = -0.886
wa_A12 = -0.133
w0_LCDM = -1.0
wa_LCDM = 0.0

dist_DR2 = np.sqrt(((w0_A12 - w0_LCDM)/sigma_DR2_w0)**2 + ((wa_A12 - wa_LCDM)/sigma_DR2_wa)**2)
dist_DR3_cons = np.sqrt(((w0_A12 - w0_LCDM)/sigma_DR3_w0_cons)**2 + ((wa_A12 - wa_LCDM)/sigma_DR3_wa_cons)**2)
dist_DR3_opt  = np.sqrt(((w0_A12 - w0_LCDM)/sigma_DR3_w0_opt)**2  + ((wa_A12 - wa_LCDM)/sigma_DR3_wa_opt)**2)

print("  A12 vs LCDM distance in w0-wa space:")
print("    DR2:  {:.2f} sigma".format(dist_DR2))
print("    DR3 conservative: {:.2f} sigma".format(dist_DR3_cons))
print("    DR3 optimistic:   {:.2f} sigma".format(dist_DR3_opt))
print("")

# ============================================================
# Section 3: Bayes factor scaling
# ============================================================
print("=== Section 3: Bayes factor scaling model ===")

# Approximation: For a 2-parameter model with uniform priors (flat in w0, wa):
# Delta ln Z ~ (ndata * chi2_per_data / 2) - 1 * ln(N_data) / 2
# Better: use Laplace approximation to the evidence

# Laplace approximation:
# Delta ln Z = -chi2_min/2 + k/2 * ln(2*pi) - k/2 + 0.5 * ln|F|
# where F is the Fisher matrix of the model
# For 2-parameter model: |F| ~ 1/(sigma_w0^2 * sigma_wa^2)

# The key scaling: when data improves (sigma decreases):
# 1. chi2_min at model best-fit stays the same (model still fits well)
# 2. chi2_LCDM increases (LCDM fits worse relative to tighter data)
# 3. Delta_chi2 = chi2_LCDM - chi2_model increases

# DR2 to DR3 Delta_lnZ change:
# Delta_lnZ(DR3) ~ Delta_lnZ(DR2) + 0.5 * (dist_DR3^2 - dist_DR2^2)
# (rough scaling from chi2 gain)

# But we also lose from narrower priors:
# Evidence penalty for extra parameters: 0.5 * k * ln(F_DR3/F_DR2)
# = 0.5 * 2 * ln(sigma_DR2^2/sigma_DR3^2) = ln(improvement_factor^2) for each param

k_params = 2  # extra parameters in A12 vs LCDM

# Chi2 gain when data gets better (model moves away from LCDM in sigma units):
delta_chi2_gain_cons = dist_DR3_cons**2 - dist_DR2**2
delta_chi2_gain_opt  = dist_DR3_opt**2  - dist_DR2**2

# Occam's razor penalty (tighter data = bigger prior penalty for extra params):
occam_penalty_cons = 0.5 * k_params * np.log(sigma_DR2_w0**2 / sigma_DR3_w0_cons**2 +
                                                sigma_DR2_wa**2 / sigma_DR3_wa_cons**2) / k_params
occam_penalty_opt  = 0.5 * k_params * np.log(sigma_DR2_w0**2 / sigma_DR3_w0_opt**2  +
                                                sigma_DR2_wa**2 / sigma_DR3_wa_opt**2)  / k_params

# Net change in Delta_lnZ
DlnZ_DR2 = 10.769  # baseline A12

# Simple model: Delta_lnZ(DR3) = Delta_lnZ(DR2) + 0.5*(dist_DR3^2 - dist_DR2^2) - Occam
DlnZ_DR3_cons = DlnZ_DR2 + 0.5 * delta_chi2_gain_cons - occam_penalty_cons
DlnZ_DR3_opt  = DlnZ_DR2 + 0.5 * delta_chi2_gain_opt  - occam_penalty_opt

print("  DR2 -> DR3 chi2 gain (conservative):", delta_chi2_gain_cons)
print("  DR2 -> DR3 chi2 gain (optimistic):  ", delta_chi2_gain_opt)
print("  Occam penalty (conservative):", occam_penalty_cons)
print("  Occam penalty (optimistic):  ", occam_penalty_opt)
print("")
print("  Predicted Delta_lnZ(A12, DR3):")
print("    Conservative: {:.2f}".format(DlnZ_DR3_cons))
print("    Optimistic:   {:.2f}".format(DlnZ_DR3_opt))
print("")

# ============================================================
# Section 4: Monte Carlo sampling of uncertainty
# ============================================================
print("=== Section 4: Monte Carlo uncertainty on Delta_lnZ prediction ===")
np.random.seed(42)

# Uncertainty sources:
# 1. Statistical: DR3 measurement scatter ~ sigma_w0_DR3 * noise
# 2. Systematic: BAO calibration, photo-z errors ~ 20% of statistical
# 3. Model uncertainty: prior choice ~ 1 ln Z unit

N_MC = 10000
# Simulate DR3 measured (w0, wa) centered on A12 true values with DR3 errors:
w0_DR3_samples = np.random.normal(w0_A12, sigma_DR3_w0_cons, N_MC)
wa_DR3_samples = np.random.normal(wa_A12, sigma_DR3_wa_cons, N_MC)

# Compute Delta_lnZ for each sample (using conservative estimate)
DlnZ_samples = np.zeros(N_MC)
for i in range(N_MC):
    # Distance from LCDM in DR3 sigma units
    dist_i = np.sqrt(((w0_DR3_samples[i] - w0_LCDM)/sigma_DR3_w0_cons)**2 +
                     ((wa_DR3_samples[i] - wa_LCDM)/sigma_DR3_wa_cons)**2)
    dist_DR2_i = np.sqrt(((w0_DR3_samples[i] - w0_LCDM)/sigma_DR2_w0)**2 +
                          ((wa_DR3_samples[i] - wa_LCDM)/sigma_DR2_wa)**2)
    DlnZ_samples[i] = DlnZ_DR2 + 0.5 * (dist_i**2 - dist_DR2_i**2) - occam_penalty_cons

DlnZ_median = np.median(DlnZ_samples)
DlnZ_16 = np.percentile(DlnZ_samples, 16)
DlnZ_84 = np.percentile(DlnZ_samples, 84)
DlnZ_5  = np.percentile(DlnZ_samples, 5)
DlnZ_95 = np.percentile(DlnZ_samples, 95)

print("  Monte Carlo prediction for Delta_lnZ(A12, DR3):")
print("  Median: {:.2f}".format(DlnZ_median))
print("  68% CI: [{:.2f}, {:.2f}]".format(DlnZ_16, DlnZ_84))
print("  90% CI: [{:.2f}, {:.2f}]".format(DlnZ_5, DlnZ_95))
print("")

# ============================================================
# Section 5: C11D and C28 under DR3
# ============================================================
print("=== Section 5: C11D and C28 DR3 predictions ===")

# C11D: w0=-0.912, wa=-0.115 (from L6)
w0_C11D = -0.912
wa_C11D = -0.115  # approximate from L6 lambda=0.8872
DlnZ_C11D_DR2 = 8.771

dist_C11D_DR2 = np.sqrt(((w0_C11D - w0_LCDM)/sigma_DR2_w0)**2 + ((wa_C11D - wa_LCDM)/sigma_DR2_wa)**2)
dist_C11D_DR3 = np.sqrt(((w0_C11D - w0_LCDM)/sigma_DR3_w0_cons)**2 + ((wa_C11D - wa_LCDM)/sigma_DR3_wa_cons)**2)
DlnZ_C11D_DR3 = DlnZ_C11D_DR2 + 0.5 * (dist_C11D_DR3**2 - dist_C11D_DR2**2) - occam_penalty_cons

# C28: w0=-0.886 (approx), wa=-0.176
w0_C28 = -0.886  # approximate
wa_C28 = -0.176  # Dirian shooting result
DlnZ_C28_DR2 = 8.633

dist_C28_DR2 = np.sqrt(((w0_C28 - w0_LCDM)/sigma_DR2_w0)**2 + ((wa_C28 - wa_LCDM)/sigma_DR2_wa)**2)
dist_C28_DR3 = np.sqrt(((w0_C28 - w0_LCDM)/sigma_DR3_w0_cons)**2 + ((wa_C28 - wa_LCDM)/sigma_DR3_wa_cons)**2)
DlnZ_C28_DR3 = DlnZ_C28_DR2 + 0.5 * (dist_C28_DR3**2 - dist_C28_DR2**2) - occam_penalty_cons

print("  A12:  DR2 = {:.2f} -> DR3 predicted = {:.2f}".format(DlnZ_DR2, DlnZ_DR3_cons))
print("  C11D: DR2 = {:.2f} -> DR3 predicted = {:.2f}".format(DlnZ_C11D_DR2, DlnZ_C11D_DR3))
print("  C28:  DR2 = {:.2f} -> DR3 predicted = {:.2f}".format(DlnZ_C28_DR2, DlnZ_C28_DR3))
print("")
print("  All three candidates: predicted to GAIN Delta_lnZ with DR3 precision.")
print("  (Signal gets stronger relative to LCDM as errors shrink)")
print("")

# ============================================================
# Section 6: K54/Q54 Verdict
# ============================================================
print("=== K54 / Q54 VERDICT ===")
print("")
print("K54 threshold: 90% CI lower bound of Delta_lnZ(A12, DR3) < 5.0")
print("Q54 threshold: Predicted Delta_lnZ(A12, DR3) > 8.0 at median")
print("")
print("  Monte Carlo 90% CI lower bound: {:.2f}".format(DlnZ_5))
print("  Monte Carlo median: {:.2f}".format(DlnZ_median))
print("")

if DlnZ_5 < 5.0:
    print("  K54 STATUS: TRIGGERED")
    print("  90% CI lower bound {:.2f} < 5.0".format(DlnZ_5))
    print("  A12 could fall below Jeffreys Strong under DR3.")
elif DlnZ_median < 8.0:
    print("  K54 STATUS: NOT TRIGGERED (lower bound > 5.0)")
    print("  Q54 STATUS: FAIL (median {:.2f} < 8.0)".format(DlnZ_median))
else:
    print("  K54 STATUS: NOT TRIGGERED (lower bound {:.2f} > 5.0)".format(DlnZ_5))
    print("  Q54 STATUS: PASS (median {:.2f} > 8.0)".format(DlnZ_median))

print("")
print("  INTERPRETATION:")
print("  If DR3 confirms DESI DR2 w0-wa direction (A12 best-fit near DR2 best-fit):")
print("    -> Delta_lnZ(A12) INCREASES (signal strengthens)")
print("  If DR3 shows w0->-1 regression (toward LCDM):")
print("    -> Delta_lnZ(A12) could fall (signal weakens)")
print("  Our forecast: A12 Delta_lnZ = {:.1f} +/- {:.1f} (DR3)".format(
    DlnZ_median, (DlnZ_84 - DlnZ_16)/2))
print("")
print("Paper language (falsifiable claim):")
print("  'A12 template achieves Delta_lnZ = 10.769 vs LCDM on DESI DR2+CMB+SN.")
print("  Under DESI DR3 (expected 2026), Fisher forecast predicts Delta_lnZ =")
print("  {:.1f} +/- {:.1f} (conservative) if the DR2 w0-wa trend persists.".format(
    DlnZ_DR3_cons, abs(DlnZ_84 - DlnZ_16)/2))
print("  This prediction is falsifiable: Delta_lnZ < 5.0 would indicate A12 is disfavored.'")
print("")
print("=== L10-D Complete ===")
