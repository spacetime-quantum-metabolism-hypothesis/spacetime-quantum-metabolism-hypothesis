"""L327 — Systematic uncertainty inflation attack on Branch B vs LCDM ΔAICc.

Question: L208 reported ΔAICc=99.49 driven entirely by 3 anchors (chi2_anchor_LCDM=103.61).
If anchor σ are inflated by factors f ∈ {1, 2, 5, 10}, does the BB advantage survive?

Logic:
- Anchor χ² for LCDM scales as 1/f² when σ → f·σ (residuals fixed).
- Anchor χ² for BB stays 0 (by construction perfect fit).
- SPARC χ² is identical for both models (universal a0 ≈ 1.2e-10 m/s²).
- AICc penalty: BB has +3 anchor params, so kBB-kLCDM = +3 (after subtracting LCDM 0 anchor params for matching scope).

We additionally explore:
  (a) SPARC log_a0 σ inflation (per-galaxy intrinsic scatter expansion).
  (b) Combined inflation (anchor & SPARC).
  (c) Robust statistics — Huber loss (mid-cap) on anchor residuals.

Output: results/L327/report.json + ATTACK_DESIGN.md/REVIEW.md/NEXT_STEP.md (separately).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

# --- L208 baseline numbers (from results/L208/report.json) -----------------
N_SPARC = 163
N_ANCHOR = 3
CHI2_SPARC = 7503.046571608098            # identical for BB and LCDM
CHI2_ANCHOR_LCDM_BASE = 103.61            # at f=1
CHI2_ANCHOR_BB = 0.0                      # by-construction
K_BB = 3        # 3 anchor params
K_LCDM = 0      # universal a0 fixed externally

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "L327"
OUT.mkdir(parents=True, exist_ok=True)


def aicc(chi2: float, k: int, n: int) -> float:
    if n - k - 1 <= 0:
        return chi2 + 2 * k
    return chi2 + 2 * k + 2 * k * (k + 1) / (n - k - 1)


def scan_anchor_inflation(factors):
    n = N_SPARC + N_ANCHOR
    rows = []
    for f in factors:
        chi2_anchor_lcdm = CHI2_ANCHOR_LCDM_BASE / (f ** 2)
        chi2_total_bb = CHI2_SPARC + CHI2_ANCHOR_BB
        chi2_total_lcdm = CHI2_SPARC + chi2_anchor_lcdm
        aicc_bb = aicc(chi2_total_bb, K_BB, n)
        aicc_lcdm = aicc(chi2_total_lcdm, K_LCDM, n)
        rows.append({
            "factor": f,
            "chi2_anchor_LCDM": chi2_anchor_lcdm,
            "delta_chi2": chi2_total_lcdm - chi2_total_bb,
            "aicc_BB": aicc_bb,
            "aicc_LCDM": aicc_lcdm,
            "delta_aicc": aicc_lcdm - aicc_bb,
        })
    return rows


def scan_sparc_inflation(factors):
    """SPARC σ inflation: residuals fixed, chi2_sparc → chi2_sparc / f².

    SPARC χ² identical for both models, so this *cannot* change Δχ². But it
    changes total AICc denominator (n unchanged) — only effect is on absolute
    chi² scale, leaving ΔAICc invariant. Reported for transparency.
    """
    rows = []
    n = N_SPARC + N_ANCHOR
    for f in factors:
        chi2_sparc = CHI2_SPARC / (f ** 2)
        chi2_bb = chi2_sparc + CHI2_ANCHOR_BB
        chi2_lcdm = chi2_sparc + CHI2_ANCHOR_LCDM_BASE
        rows.append({
            "factor": f,
            "chi2_sparc": chi2_sparc,
            "delta_aicc": aicc(chi2_lcdm, K_LCDM, n) - aicc(chi2_bb, K_BB, n),
        })
    return rows


def scan_combined(anchor_factors, sparc_factors):
    n = N_SPARC + N_ANCHOR
    rows = []
    for fa in anchor_factors:
        for fs in sparc_factors:
            chi2_sparc = CHI2_SPARC / (fs ** 2)
            chi2_anchor_lcdm = CHI2_ANCHOR_LCDM_BASE / (fa ** 2)
            chi2_bb = chi2_sparc
            chi2_lcdm = chi2_sparc + chi2_anchor_lcdm
            rows.append({
                "anchor_factor": fa,
                "sparc_factor": fs,
                "delta_aicc": aicc(chi2_lcdm, K_LCDM, n) - aicc(chi2_bb, K_BB, n),
            })
    return rows


def huber_chi2(residual_sigma: float, k: float = 1.345) -> float:
    """Huber loss in chi² units for a single residual at |z|=residual_sigma.

    Standard Huber: ρ(z) = z²/2 if |z|≤k, else k(|z|-k/2). Multiply by 2 for chi² units.
    """
    z = abs(residual_sigma)
    if z <= k:
        return z ** 2
    return 2 * k * z - k ** 2


def robust_anchor_chi2():
    """L208 anchor residual breakdown.

    chi2_anchor_LCDM = 103.61 with 3 anchors. Cluster (A1689) anchor dominates.
    From L275: cluster anchor σ wide (log_σ_cluster ± 0.045), giving largest residual.
    Reconstruct individual residuals (assume galactic ≈ 1σ, cluster ≈ 10σ, cosmic ≈ 1σ
    consistent with 1+100+1 ≈ 103).
    """
    # Approximate individual residuals consistent with sum 103.61
    # (galactic ~ 1, cluster ~ 101, cosmic ~ 1)
    z_galactic = 1.0
    z_cluster = math.sqrt(101.0)   # ≈ 10.05σ
    z_cosmic = 1.0
    gauss_sum = z_galactic ** 2 + z_cluster ** 2 + z_cosmic ** 2

    huber_sum = (huber_chi2(z_galactic) + huber_chi2(z_cluster)
                 + huber_chi2(z_cosmic))
    tukey_cap = 9.0  # Tukey biweight saturates at z=4.685; cap residual contribution
    tukey_sum = (min(z_galactic ** 2, tukey_cap)
                 + min(z_cluster ** 2, tukey_cap)
                 + min(z_cosmic ** 2, tukey_cap))

    n = N_SPARC + N_ANCHOR
    return {
        "z_residuals_assumed": [z_galactic, z_cluster, z_cosmic],
        "gaussian_sum_check": gauss_sum,
        "huber_chi2_LCDM": huber_sum,
        "tukey_chi2_LCDM": tukey_sum,
        "delta_aicc_huber":
            aicc(CHI2_SPARC + huber_sum, K_LCDM, n)
            - aicc(CHI2_SPARC, K_BB, n),
        "delta_aicc_tukey":
            aicc(CHI2_SPARC + tukey_sum, K_LCDM, n)
            - aicc(CHI2_SPARC, K_BB, n),
    }


def main():
    factors = [1, 2, 5, 10]

    anchor_scan = scan_anchor_inflation(factors)
    sparc_scan = scan_sparc_inflation(factors)
    combined = scan_combined(factors, factors)
    robust = robust_anchor_chi2()

    # Threshold at which BB advantage falls below conventional ΔAICc=10.
    # Δchi² = 103.61/f² ; ΔAICc = Δchi² + 2(k_BB - k_LCDM corrections)
    # With finite-sample corrections, K_BB=3 adds small AICc penalty (~6).
    # Solve 103.61/f² + (aicc_pen_BB - aicc_pen_LCDM) = 10 → f_crit.
    n = N_SPARC + N_ANCHOR
    pen_bb = 2 * K_BB + 2 * K_BB * (K_BB + 1) / (n - K_BB - 1)
    pen_lcdm = 0.0
    pen_diff = pen_bb - pen_lcdm  # AICc penalty BB pays
    # ΔAICc = χ²_LCDM(f) - 0 + (pen_lcdm - pen_bb) = 103.61/f² - pen_diff
    f_crit_10 = math.sqrt(CHI2_ANCHOR_LCDM_BASE / (10 + pen_diff))
    f_crit_2 = math.sqrt(CHI2_ANCHOR_LCDM_BASE / (2 + pen_diff))
    f_crit_0 = math.sqrt(CHI2_ANCHOR_LCDM_BASE / pen_diff)  # ΔAICc = 0

    report = {
        "L327": "Systematic uncertainty inflation attack on BB vs LCDM",
        "baseline_L208": {
            "delta_aicc": 99.49,
            "chi2_anchor_LCDM": CHI2_ANCHOR_LCDM_BASE,
            "n_total": n,
            "k_BB": K_BB, "k_LCDM": K_LCDM,
        },
        "anchor_inflation_scan": anchor_scan,
        "sparc_inflation_scan": sparc_scan,
        "combined_scan": combined,
        "robust_statistics": robust,
        "aicc_penalty_BB": pen_bb,
        "f_crit_AICc_10": f_crit_10,
        "f_crit_AICc_2": f_crit_2,
        "f_crit_AICc_0": f_crit_0,
        "interpretation": (
            "ΔAICc(f) ≈ 103.61/f² − {:.3f}. ".format(pen_diff)
            + "f=2 → ΔAICc≈{:.1f}, f=5 → {:.2f}, f=10 → {:.2f}. ".format(
                anchor_scan[1]["delta_aicc"],
                anchor_scan[2]["delta_aicc"],
                anchor_scan[3]["delta_aicc"],
            )
            + "Critical inflation: f≈{:.2f} drops ΔAICc below 10; f≈{:.2f} below 2; f≈{:.2f} ties.".format(
                f_crit_10, f_crit_2, f_crit_0,
            )
        ),
    }

    out_path = OUT / "report.json"
    with out_path.open("w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)

    print("L327 inflation scan complete.")
    print("  f=1 ΔAICc =", anchor_scan[0]["delta_aicc"])
    print("  f=2 ΔAICc =", anchor_scan[1]["delta_aicc"])
    print("  f=5 ΔAICc =", anchor_scan[2]["delta_aicc"])
    print("  f=10 ΔAICc =", anchor_scan[3]["delta_aicc"])
    print("  f_crit (ΔAICc=10):", f_crit_10)
    print("  f_crit (ΔAICc=2):", f_crit_2)
    print("  f_crit (ΔAICc=0):", f_crit_0)
    print("  Huber ΔAICc:", robust["delta_aicc_huber"])
    print("  Tukey ΔAICc:", robust["delta_aicc_tukey"])
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
