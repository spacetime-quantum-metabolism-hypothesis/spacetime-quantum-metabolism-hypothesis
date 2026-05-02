"""L340 — proper BMA across 5 models.

BIC-based marginalized evidence approximation:
    ln Z_i ≈ -0.5 * chi2_min_i - 0.5 * k_i * ln(N_data)

Posterior model weights:
    w_i = exp(ln Z_i - ln Z_max) / sum(...)

Cross-check with Laplace approximation assuming
prior width = 5 * posterior width (uninformative prior box).

Inputs (best-fit chi2 from L196/L281 family):
    BB (Branch B, 3-step):  chi2 = 1745.0,  k = 3
    smooth (5-poly):        chi2 = 1742.0,  k = 5
    LCDM:                   chi2 = 1758.0,  k = 2
    MOND-cosmo:             chi2 = 1762.0,  k = 2
    SymG (symmetron 4p):    chi2 = 1748.0,  k = 4

N_data ≈ 1756 (BAO 13 + SN 1735 + CMB 2 + RSD 6).
"""
import json
import math
from pathlib import Path

OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L340")

models = {
    "BB":     {"chi2": 1745.0, "k": 3},
    "smooth": {"chi2": 1742.0, "k": 5},
    "LCDM":   {"chi2": 1758.0, "k": 2},
    "MOND":   {"chi2": 1762.0, "k": 2},
    "SymG":   {"chi2": 1748.0, "k": 4},
}

N_data = 1756
lnN = math.log(N_data)

# BIC-based ln Z
for m, d in models.items():
    d["BIC"] = d["chi2"] + d["k"] * lnN
    d["lnZ_BIC"] = -0.5 * d["BIC"]

lnZ_max = max(d["lnZ_BIC"] for d in models.values())
Z_unnorm = {m: math.exp(d["lnZ_BIC"] - lnZ_max) for m, d in models.items()}
Z_sum = sum(Z_unnorm.values())
weights_BIC = {m: Z_unnorm[m] / Z_sum for m in models}

# Laplace cross-check: assume prior width = 5 * posterior width (per param).
# Then ln(prior/posterior volume) per param ≈ ln(5 * sqrt(2 pi)) − 0.5 ln(2 pi)
#                                            = ln(5) + 0.5 ln(2 pi) − 0.5 ln(2 pi)
#                                            = ln(5) ≈ 1.609.
# So Occam penalty per param = ln(5) ≈ 1.609 (instead of 0.5 lnN ≈ 3.74).
# This is a less aggressive penalty than BIC.
ln5 = math.log(5)
for m, d in models.items():
    d["lnZ_laplace"] = -0.5 * d["chi2"] - d["k"] * ln5

lnZ_max_L = max(d["lnZ_laplace"] for d in models.values())
Z_unnorm_L = {m: math.exp(d["lnZ_laplace"] - lnZ_max_L) for m, d in models.items()}
Z_sum_L = sum(Z_unnorm_L.values())
weights_laplace = {m: Z_unnorm_L[m] / Z_sum_L for m in models}

# Akaike weights (for comparison with L196)
for m, d in models.items():
    d["AIC"] = d["chi2"] + 2 * d["k"]
AIC_min = min(d["AIC"] for d in models.values())
w_unnorm_A = {m: math.exp(-0.5 * (d["AIC"] - AIC_min)) for m, d in models.items()}
w_sum_A = sum(w_unnorm_A.values())
weights_AIC = {m: w_unnorm_A[m] / w_sum_A for m in models}

# Model-averaged predictions (illustrative; uses representative model means)
# Per-model predicted (sigma8, H0). Values reflect each model's best-fit posture
# (BB raises sigma8 slightly via background, MOND lowers it, etc.).
pred = {
    "BB":     {"sigma8": 0.812, "H0": 67.8},
    "smooth": {"sigma8": 0.810, "H0": 67.9},
    "LCDM":   {"sigma8": 0.811, "H0": 67.4},
    "MOND":   {"sigma8": 0.795, "H0": 70.5},
    "SymG":   {"sigma8": 0.808, "H0": 68.1},
}

def model_avg(weights):
    s8 = sum(weights[m] * pred[m]["sigma8"] for m in models)
    H0 = sum(weights[m] * pred[m]["H0"] for m in models)
    return {"sigma8": s8, "H0": H0}

avg_BIC = model_avg(weights_BIC)
avg_laplace = model_avg(weights_laplace)
avg_AIC = model_avg(weights_AIC)

# Pairwise Bayes factors vs BB
deltas_BIC = {m: models["BB"]["lnZ_BIC"] - d["lnZ_BIC"] for m, d in models.items()}
deltas_laplace = {m: models["BB"]["lnZ_laplace"] - d["lnZ_laplace"] for m, d in models.items()}

report = {
    "N_data": N_data,
    "models": {m: {"chi2": d["chi2"], "k": d["k"], "BIC": d["BIC"],
                   "lnZ_BIC": d["lnZ_BIC"], "lnZ_laplace": d["lnZ_laplace"],
                   "AIC": d["AIC"]}
               for m, d in models.items()},
    "weights_BIC": weights_BIC,
    "weights_laplace": weights_laplace,
    "weights_AIC_for_comparison": weights_AIC,
    "delta_lnZ_BB_minus_X_BIC": deltas_BIC,
    "delta_lnZ_BB_minus_X_laplace": deltas_laplace,
    "model_averaged_predictions": {
        "BIC_weights":     avg_BIC,
        "laplace_weights": avg_laplace,
        "AIC_weights":     avg_AIC,
    },
}

OUT.mkdir(parents=True, exist_ok=True)
with open(OUT / "bma_report.json", "w") as f:
    json.dump(report, f, indent=2)

# Pretty print
def pct(x): return f"{100*x:6.2f}%"
print("=== L340 BMA ===")
print(f"N_data={N_data}, lnN={lnN:.4f}")
print(f"\n{'Model':8s} {'chi2':>8s} {'k':>3s} {'BIC':>10s} {'lnZ_BIC':>10s} {'lnZ_Lap':>10s}")
for m, d in models.items():
    print(f"{m:8s} {d['chi2']:8.1f} {d['k']:3d} {d['BIC']:10.2f} "
          f"{d['lnZ_BIC']:10.2f} {d['lnZ_laplace']:10.2f}")

print(f"\nBIC-based weights:")
for m in models: print(f"  {m:8s} {pct(weights_BIC[m])}")
print(f"\nLaplace-based weights (prior=5σ):")
for m in models: print(f"  {m:8s} {pct(weights_laplace[m])}")
print(f"\nAIC weights (for comparison vs L196):")
for m in models: print(f"  {m:8s} {pct(weights_AIC[m])}")

print(f"\nΔlnZ (BB − X) under BIC:")
for m in models:
    if m == "BB": continue
    bf = math.exp(deltas_BIC[m])
    print(f"  BB vs {m:8s}  ΔlnZ = {deltas_BIC[m]:+7.2f}   BF = {bf:9.2e}")

print(f"\nΔlnZ (BB − X) under Laplace (5σ prior):")
for m in models:
    if m == "BB": continue
    bf = math.exp(deltas_laplace[m])
    print(f"  BB vs {m:8s}  ΔlnZ = {deltas_laplace[m]:+7.2f}   BF = {bf:9.2e}")

print(f"\nModel-averaged predictions:")
print(f"  BIC:     sigma8 = {avg_BIC['sigma8']:.4f}, H0 = {avg_BIC['H0']:.3f}")
print(f"  Laplace: sigma8 = {avg_laplace['sigma8']:.4f}, H0 = {avg_laplace['H0']:.3f}")
print(f"  AIC:     sigma8 = {avg_AIC['sigma8']:.4f}, H0 = {avg_AIC['H0']:.3f}")

# Honesty verdict
bb_w_BIC = weights_BIC["BB"]
bb_w_lap = weights_laplace["BB"]
print("\n=== 정직 판정 ===")
print(f"BB weight (BIC):     {pct(bb_w_BIC)}")
print(f"BB weight (Laplace): {pct(bb_w_lap)}")
print(f"L196 BB Akaike weight (4-model): 99.9998%")
print(f"L340 BB AIC weight  (5-model):   {pct(weights_AIC['BB'])}")

if bb_w_BIC >= 0.5 and bb_w_lap >= 0.5:
    verdict = "narrative 유지: BB favored, modest"
elif bb_w_BIC >= 0.2 or bb_w_lap >= 0.2:
    verdict = "격하: 'preferred but not dominant'"
else:
    verdict = "추가 격하: BB weight < 20%, paper narrative 재작성 필요"
print(f"verdict: {verdict}")

report["verdict"] = verdict
report["bb_weight_BIC"] = bb_w_BIC
report["bb_weight_laplace"] = bb_w_lap
with open(OUT / "bma_report.json", "w") as f:
    json.dump(report, f, indent=2)
