"""L376 — proper Laplace ln Z BMA across 5 cosmology models.

Models:
    BB-3regime: chi2=1745.0, k=3 (L196 family best-fit, L340 input)
    BB-2regime: chi2=1746.23, k=2 (derived from L322 dAICc(M3-M2)=+0.77)
    smooth   :  chi2=1742.0, k=5 (L340 input)
    LCDM     :  chi2=1758.0, k=2 (L340 input)
    MOND     :  chi2=1762.0, k=2 (L340 input)

Laplace ln Z (uniform prior box, Gaussian posterior):
    ln Z = -0.5 chi2_min - k * (ln R - 0.5 ln(2 pi))
where R = W_prior / sigma_post (assumed uniform across params).

Reports R = 3, 5, 10 sensitivity. R=5 is L340 baseline.

Output: /Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L376/report.json
"""
import json
import math
from pathlib import Path

OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L376")
OUT.mkdir(parents=True, exist_ok=True)

models = {
    "BB-3regime": {"chi2": 1745.00, "k": 3,
                   "source": "L196/L281 family best-fit (joint BAO+SN+CMB+RSD)"},
    "BB-2regime": {"chi2": 1746.23, "k": 2,
                   "source": "derived from L322 dAICc(M3-M2)=+0.77, chi2_2 = chi2_3 + 1.23"},
    "smooth":     {"chi2": 1742.00, "k": 5,
                   "source": "L340 input (5-poly background)"},
    "LCDM":       {"chi2": 1758.00, "k": 2,
                   "source": "L340 input (Planck-LCDM)"},
    "MOND":       {"chi2": 1762.00, "k": 2,
                   "source": "L340 input (MOND-cosmo Bekenstein-Sanders)"},
}

N_data = 1756  # BAO 13 + SN 1735 + CMB 2 + RSD 6
lnN = math.log(N_data)
ln2pi = math.log(2 * math.pi)

# AIC, AICc, BIC
for m, d in models.items():
    k = d["k"]
    chi2 = d["chi2"]
    d["AIC"]  = chi2 + 2 * k
    d["AICc"] = chi2 + 2 * k + 2 * k * (k + 1) / max(N_data - k - 1, 1)
    d["BIC"]  = chi2 + k * lnN

def laplace_lnZ(chi2, k, R):
    """ln Z = -0.5 chi2 - k * (ln R - 0.5 ln 2pi)."""
    return -0.5 * chi2 - k * (math.log(R) - 0.5 * ln2pi)

def weights_from_lnZ(lnZ_dict):
    lnZ_max = max(lnZ_dict.values())
    unnorm = {m: math.exp(v - lnZ_max) for m, v in lnZ_dict.items()}
    Z = sum(unnorm.values())
    return {m: unnorm[m] / Z for m in lnZ_dict}

R_list = [3, 5, 10]
lnZ_by_R = {}
weights_by_R = {}
bb_family_by_R = {}
delta_by_R = {}
for R in R_list:
    lnZ = {m: laplace_lnZ(d["chi2"], d["k"], R) for m, d in models.items()}
    w   = weights_from_lnZ(lnZ)
    bb_family = w["BB-3regime"] + w["BB-2regime"]
    best_lnZ = max(lnZ.values())
    delta = {m: best_lnZ - v for m, v in lnZ.items()}  # delta = best - X (>= 0)
    lnZ_by_R[str(R)] = lnZ
    weights_by_R[str(R)] = w
    bb_family_by_R[str(R)] = bb_family
    delta_by_R[str(R)] = delta

# AIC weights for cross-check
AIC_min = min(d["AIC"] for d in models.values())
w_AIC_unnorm = {m: math.exp(-0.5 * (d["AIC"] - AIC_min)) for m, d in models.items()}
SA = sum(w_AIC_unnorm.values())
weights_AIC = {m: w_AIC_unnorm[m] / SA for m in models}

# AICc weights
AICc_min = min(d["AICc"] for d in models.values())
w_AICc_unnorm = {m: math.exp(-0.5 * (d["AICc"] - AICc_min)) for m, d in models.items()}
SAc = sum(w_AICc_unnorm.values())
weights_AICc = {m: w_AICc_unnorm[m] / SAc for m in models}

# BIC weights
BIC_min = min(d["BIC"] for d in models.values())
w_BIC_unnorm = {m: math.exp(-0.5 * (d["BIC"] - BIC_min)) for m, d in models.items()}
SBc = sum(w_BIC_unnorm.values())
weights_BIC = {m: w_BIC_unnorm[m] / SBc for m in models}

bb_family_AIC  = weights_AIC["BB-3regime"]  + weights_AIC["BB-2regime"]
bb_family_AICc = weights_AICc["BB-3regime"] + weights_AICc["BB-2regime"]
bb_family_BIC  = weights_BIC["BB-3regime"]  + weights_BIC["BB-2regime"]

# verdict
w5 = weights_by_R["5"]
bb_5 = bb_family_by_R["5"]
bb_3 = bb_family_by_R["3"]
bb_10 = bb_family_by_R["10"]

if bb_3 >= 0.5 and bb_5 >= 0.5 and bb_10 >= 0.5:
    verdict = "BB family Laplace BMA dominant (>=50%) across R=3..10 — robust BB preference"
elif bb_5 >= 0.5 and bb_10 >= 0.5:
    verdict = ("BB family dominant at R=5 and R=10 but minority at R=3 (smooth competitive "
               "under tight prior)")
elif bb_5 >= 0.3:
    verdict = ("BB family preferred but not dominant under Laplace baseline (smooth "
               "competitive); strongly prior-sensitive across R=3..10")
else:
    verdict = "BB family minority under Laplace BMA — narrative reset required"

report = {
    "loop": "L376",
    "purpose": "proper Laplace ln Z BMA across 5 models (BB-3regime, BB-2regime, smooth, LCDM, MOND)",
    "N_data": N_data,
    "ln_N_data": lnN,
    "models": {m: {"chi2": d["chi2"], "k": d["k"],
                   "AIC": d["AIC"], "AICc": d["AICc"], "BIC": d["BIC"],
                   "source": d["source"]}
               for m, d in models.items()},
    "R_values_tested": R_list,
    "Laplace_lnZ_by_R": lnZ_by_R,
    "Laplace_weights_by_R": weights_by_R,
    "delta_lnZ_best_minus_X_by_R": delta_by_R,
    "BB_family_weight_by_R": bb_family_by_R,
    "AIC_weights_for_comparison": weights_AIC,
    "AICc_weights_for_comparison": weights_AICc,
    "BIC_weights_for_comparison": weights_BIC,
    "BB_family_weight_AIC": bb_family_AIC,
    "BB_family_weight_AICc": bb_family_AICc,
    "BB_family_weight_BIC": bb_family_BIC,
    "verdict": verdict,
    "honesty_note_one_line": (
        "BB-2regime chi2=1746.23 is derived from L322 synthetic dAICc=+0.77 (not from "
        "an independent joint MCMC fit). Other chi2 values are L340/L196 inputs."
    ),
}

with open(OUT / "report.json", "w") as f:
    json.dump(report, f, indent=2)

# Pretty print
def pct(x): return f"{100*x:6.2f}%"
print("=== L376 proper Laplace ln Z BMA ===")
print(f"N_data={N_data}, ln N={lnN:.4f}\n")

print(f"{'Model':12s} {'chi2':>9s} {'k':>3s} {'AIC':>9s} {'AICc':>9s} {'BIC':>9s}")
for m, d in models.items():
    print(f"{m:12s} {d['chi2']:9.2f} {d['k']:3d} {d['AIC']:9.2f} {d['AICc']:9.2f} {d['BIC']:9.2f}")

for R in R_list:
    print(f"\n--- Laplace (R={R}, prior/posterior width ratio) ---")
    print(f"{'Model':12s} {'lnZ':>10s} {'dlnZ(best-X)':>14s} {'weight':>9s}")
    lnZ = lnZ_by_R[str(R)]
    w = weights_by_R[str(R)]
    delta = delta_by_R[str(R)]
    for m in models:
        print(f"{m:12s} {lnZ[m]:10.3f} {delta[m]:14.3f} {pct(w[m])}")
    print(f"  BB family (3reg + 2reg) weight = {pct(bb_family_by_R[str(R)])}")

print(f"\n--- AIC weights (cross-check) ---")
for m in models: print(f"  {m:12s} {pct(weights_AIC[m])}")
print(f"  BB family weight = {pct(bb_family_AIC)}")
print(f"\n--- AICc weights ---")
for m in models: print(f"  {m:12s} {pct(weights_AICc[m])}")
print(f"  BB family weight = {pct(bb_family_AICc)}")
print(f"\n--- BIC weights ---")
for m in models: print(f"  {m:12s} {pct(weights_BIC[m])}")
print(f"  BB family weight = {pct(bb_family_BIC)}")

print(f"\nverdict: {verdict}")
print(f"honesty: {report['honesty_note_one_line']}")
