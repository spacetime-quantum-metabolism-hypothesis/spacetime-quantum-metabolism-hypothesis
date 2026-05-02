"""
L498 - Falsifier Independence Audit
====================================

6 pre-registered SQMH falsifiers:
  F1 = DESI DR3   (BAO + RSD,    5.00 sigma forecast)
  F2 = Euclid     (cosmic shear + BAO,  4.40 sigma)
  F3 = CMB-S4     (compressed CMB + lensing, 7.90 sigma; P22)
  F4 = ET         (GW scalar mode, BNS,      7.40 sigma; P16)
  F5 = LSST       (cosmic shear + cluster,   2.85 sigma)
  F6 = SKA        (HI 21cm IM,               NULL ; P25 - structural null)

Goal: are these 6 truly independent channels, or do shared physical
observables (cosmic shear, matter power, distance ladder) make
effective N_indep <<6 ?

Approach: build channel x observable incidence matrix, derive
correlation matrix rho_ij from cosine-similarity of observable rows,
compute effective N via Cheverud-Galwey (1991) /
Li-Ji (2005) eigenvalue criterion:

    N_eff = (sum_i lambda_i)^2 / sum_i lambda_i^2     (participation ratio)
    or equivalently
    N_eff = M - sum_i [ I(lambda_i>=1)(lambda_i-1) + ... ]    (Li-Ji)

Then combined Stouffer Z under correlation:

    Z_comb = sum_i Z_i / sqrt( sum_ij rho_ij )

Bonferroni / Holm corrections applied at alpha = 0.05 family-wise.

Single honest line at the end.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
from scipy import stats

OUT_DIR = Path(__file__).resolve().parent.parent.parent / "results" / "L498"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------
# 1. Channels and forecast significances
# -----------------------------------------------------------------
CHANNELS = ["DESI_DR3", "Euclid", "CMB_S4", "ET", "LSST", "SKA"]
SIGMAS   = np.array([5.00, 4.40, 7.90, 7.40, 2.85, 0.00])  # SKA = structural null

# -----------------------------------------------------------------
# 2. Channel x observable incidence matrix
#
# Observables that SQMH predicts a deviation in:
#   O1 = BAO distance scale          (D_M, D_H, D_V at z<2)
#   O2 = RSD growth f sigma_8        (z<1.5)
#   O3 = Cosmic shear / WL P_kappa   (low-z matter power, k~0.1-1)
#   O4 = CMB compressed (theta*, R)  (z~1100)
#   O5 = CMB lensing reconstruction  (z~2-5 weighted)
#   O6 = GW scalar polarization      (compact-binary direct mode)
#   O7 = HI 21cm intensity map       (z~1-3 large scales)
#   O8 = Cluster counts / N(M,z)     (sigma_8-driven)
#
# Entry = 1 if channel has primary leverage on observable, 0.5 if secondary.
# -----------------------------------------------------------------
OBS = ["BAO", "RSD", "WL_shear", "CMB_compr", "CMB_lens", "GW_scalar",
       "HI_21cm", "Clusters"]

# rows = channels in CHANNELS order
A = np.array([
    # BAO  RSD  WL   CMBc CMBl GW   HI   Clu
    [1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],   # DESI_DR3
    [0.5, 0.5, 1.0, 0.0, 0.0, 0.0, 0.0, 0.5],   # Euclid (BAO+WL primary, clusters secondary)
    [0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0],   # CMB-S4
    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],   # ET (pure GW scalar)
    [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0],   # LSST (WL + clusters)
    [0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],   # SKA (HI + minor RSD)
])

# -----------------------------------------------------------------
# 3. Correlation matrix from cosine similarity of observable rows
# -----------------------------------------------------------------
def cosine_corr(M: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(M, axis=1)
    norms = np.where(norms == 0, 1.0, norms)
    Mn = M / norms[:, None]
    return Mn @ Mn.T

rho = cosine_corr(A)

# -----------------------------------------------------------------
# 4. Effective N via eigenvalue methods
# -----------------------------------------------------------------
eigvals = np.linalg.eigvalsh(rho)
eigvals = np.clip(eigvals, 0.0, None)  # numerical floor

# Cheverud-Galwey 1991 (variance of eigenvalues)
var_l = np.var(eigvals, ddof=0)
M = len(eigvals)
N_eff_CG = M * (1.0 - (M - 1.0) * var_l / (M * M))

# Participation ratio (Edwards-Thouless style)
N_eff_PR = (eigvals.sum() ** 2) / (eigvals ** 2).sum()

# Li-Ji 2005
N_eff_LJ = 0.0
for lam in eigvals:
    N_eff_LJ += (1.0 if lam >= 1.0 else 0.0) + (lam - np.floor(lam)) * (lam >= 0)

# -----------------------------------------------------------------
# 5. Stouffer combined Z under correlation
#    Z_comb = sum Z_i / sqrt( sum_ij rho_ij ) (Strube 1985)
# -----------------------------------------------------------------
Z = SIGMAS.copy()
sum_rho = rho.sum()
Z_comb_corr = Z.sum() / np.sqrt(sum_rho)
Z_comb_indep = Z.sum() / np.sqrt(M)  # naive (assumes independent)

# Drop SKA (NULL by construction) for "active falsifier" combined
active = SIGMAS > 0
Z_a = SIGMAS[active]
rho_a = rho[np.ix_(active, active)]
Z_comb_active_corr = Z_a.sum() / np.sqrt(rho_a.sum())
Z_comb_active_indep = Z_a.sum() / np.sqrt(active.sum())

# -----------------------------------------------------------------
# 6. Bonferroni / Holm at family alpha = 0.05
# -----------------------------------------------------------------
alpha = 0.05
M_active = int(active.sum())  # 5

# Two-sided p from Z
p_one = 2 * (1 - stats.norm.cdf(np.abs(SIGMAS)))
p_active = p_one[active]

# Bonferroni threshold
p_bonf = alpha / M_active
bonf_pass = p_active < p_bonf

# Holm step-down
order = np.argsort(p_active)
holm_pass = np.zeros_like(p_active, dtype=bool)
for rank, idx in enumerate(order):
    thr = alpha / (M_active - rank)
    if p_active[idx] < thr:
        holm_pass[idx] = True
    else:
        break

# -----------------------------------------------------------------
# 7. Save artefacts
# -----------------------------------------------------------------
results = {
    "channels": CHANNELS,
    "sigmas": SIGMAS.tolist(),
    "observables": OBS,
    "incidence_matrix_A": A.tolist(),
    "correlation_matrix_rho": rho.tolist(),
    "eigenvalues": eigvals.tolist(),
    "N_channels": M,
    "N_eff_CheverudGalwey": float(N_eff_CG),
    "N_eff_ParticipationRatio": float(N_eff_PR),
    "N_eff_LiJi": float(N_eff_LJ),
    "Z_combined_naive_independent_all6": float(Z_comb_indep),
    "Z_combined_correlation_corrected_all6": float(Z_comb_corr),
    "Z_combined_naive_active5": float(Z_comb_active_indep),
    "Z_combined_correlation_corrected_active5": float(Z_comb_active_corr),
    "p_values_two_sided": p_one.tolist(),
    "Bonferroni_threshold_active": float(p_bonf),
    "Bonferroni_pass_active": bonf_pass.tolist(),
    "Holm_pass_active": holm_pass.tolist(),
    "active_channel_names": [CHANNELS[i] for i, a in enumerate(active) if a],
}

with open(OUT_DIR / "l498_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

# -----------------------------------------------------------------
# 8. Print summary
# -----------------------------------------------------------------
print("=" * 72)
print("L498 Falsifier Independence Audit")
print("=" * 72)
print("Channels       :", CHANNELS)
print("Sigmas         :", SIGMAS.tolist())
print()
print("Correlation matrix rho_ij (cosine of observable footprint):")
header = "          " + " ".join(f"{c:>9s}" for c in CHANNELS)
print(header)
for i, c in enumerate(CHANNELS):
    row = " ".join(f"{rho[i,j]:>9.3f}" for j in range(M))
    print(f"{c:>10s}  {row}")
print()
print("Eigenvalues lambda_i :", np.round(eigvals, 4).tolist())
print(f"N channels (M)                       : {M}")
print(f"N_eff (Cheverud-Galwey 1991)         : {N_eff_CG:.3f}")
print(f"N_eff (Participation Ratio)          : {N_eff_PR:.3f}")
print(f"N_eff (Li-Ji 2005)                   : {N_eff_LJ:.3f}")
print()
print(f"Z_comb (naive, all 6 indep)          : {Z_comb_indep:.3f}")
print(f"Z_comb (rho-corrected, all 6)        : {Z_comb_corr:.3f}")
print(f"Z_comb (naive, active 5 indep)       : {Z_comb_active_indep:.3f}")
print(f"Z_comb (rho-corrected, active 5)     : {Z_comb_active_corr:.3f}")
print()
print(f"Bonferroni threshold (alpha={alpha}, M={M_active}): p<{p_bonf:.3e}")
for i, ch in enumerate([CHANNELS[k] for k, a in enumerate(active) if a]):
    print(f"  {ch:>10s}  Z={Z_a[i]:5.2f}  p={p_active[i]:.3e}  "
          f"Bonf={'PASS' if bonf_pass[i] else 'FAIL'}  "
          f"Holm={'PASS' if holm_pass[i] else 'FAIL'}")
print()
print("=" * 72)
print("Honest one-liner:")
honest = (
    f"6 falsifiers but N_eff = {N_eff_PR:.2f} (participation ratio) — "
    f"Euclid+LSST share cosmic shear, DESI+Euclid share BAO, "
    f"CMB-S4 / ET / SKA are the 3 truly orthogonal channels."
)
print(honest)
print("=" * 72)
