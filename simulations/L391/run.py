"""L391 — b/c ratio numerical extraction attempt.

Background
----------
RG ansatz: beta(sigma) = a*sigma - b*sigma**2 + c*sigma**3.
Nontrivial fixed points (FPs) solve sigma**2 - (b/c)*sigma + (a/c) = 0,
i.e. sigma_- + sigma_+ = b/c and sigma_- * sigma_+ = a/c.
The cubic ansatz can host at most TWO nontrivial FPs.

The BB analysis (L322) reports three anchor values:
    sigma_cosmic   ~ 8.37
    sigma_cluster  ~ 7.75
    sigma_galactic ~ 9.56
(treated here as dimensionless numerical labels; semantics belongs to upstream
loops and is not asserted again here.)

Strategy (Sc-A from ATTACK_DESIGN)
----------------------------------
Cubic supports only 2 nontrivial FPs.  We therefore test all C(3,2)=3 ways of
mapping two of the three anchors to (sigma_-, sigma_+) and report

    r = b/c = sigma_- + sigma_+
    q = a/c = sigma_- * sigma_+

for each pairing.  No assertion about which pairing is "correct" is made here;
the team decides downstream.  The "third" anchor is treated as either an
inflection, an outer-scale anchor, or evidence that the cubic ansatz is
insufficient (in which case the result is reported as FAIL territory).

Honest output
-------------
Three (r, q) point estimates plus the spread (max/min ratio).  We report
*ranges*, not single numbers.  Per CLAUDE.md L33+ rules: no scheme/sign claims
beyond what the algebra above forces.
"""

from __future__ import annotations

import json
import os
from itertools import combinations
from pathlib import Path

# Force single-thread per CLAUDE.md repeatability rules.
for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np

ANCHORS = {
    "cosmic":   8.37,
    "cluster":  7.75,
    "galactic": 9.56,
}

OUT_DIR = Path(__file__).resolve().parent.parent.parent / "results" / "L391"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def pairwise_ratios(anchors: dict[str, float]) -> list[dict]:
    """For every C(n,2) pair (s_-, s_+) report b/c = sum, a/c = product."""
    rows = []
    items = list(anchors.items())
    for (n1, s1), (n2, s2) in combinations(items, 2):
        third = [(n, s) for n, s in items if n not in (n1, n2)][0]
        rows.append({
            "FP_pair":      f"{n1}+{n2}",
            "sigma_minus":  float(min(s1, s2)),
            "sigma_plus":   float(max(s1, s2)),
            "r_b_over_c":   float(s1 + s2),
            "q_a_over_c":   float(s1 * s2),
            "third_anchor": {"name": third[0], "value": float(third[1])},
        })
    return rows


def cubic_consistency_check(rows: list[dict]) -> dict:
    """If cubic is correct, the third anchor must be NOT a root.
    Report beta(sigma_third) / |beta_max on [0, max(anchor)]| as
    a dimensionless residual.  Only the *ratio* is meaningful since a, b, c
    individually are not priori-derived.  We normalise to c, i.e. set c=1 and
    use b = r*c, a = q*c.
    """
    diagnostics = []
    for row in rows:
        a_over_c = row["q_a_over_c"]
        b_over_c = row["r_b_over_c"]
        s_third = row["third_anchor"]["value"]

        # beta(s)/c = a/c * s - b/c * s**2 + s**3
        beta_third_over_c = a_over_c * s_third - b_over_c * s_third**2 + s_third**3

        # normalise by max |beta/c| on a coarse grid up to max anchor
        s_grid = np.linspace(0.0, max(ANCHORS.values()) * 1.1, 4000)
        beta_grid_over_c = a_over_c * s_grid - b_over_c * s_grid**2 + s_grid**3
        scale = float(np.max(np.abs(beta_grid_over_c))) or 1.0

        diagnostics.append({
            "FP_pair":              row["FP_pair"],
            "third_anchor":         row["third_anchor"]["name"],
            "third_anchor_value":   s_third,
            "beta_third_over_c":    float(beta_third_over_c),
            "residual_normalised":  float(abs(beta_third_over_c) / scale),
        })
    return {"diagnostics": diagnostics}


def summarise(rows: list[dict]) -> dict:
    rs = np.array([r["r_b_over_c"] for r in rows])
    qs = np.array([r["q_a_over_c"] for r in rows])
    return {
        "r_b_over_c_min":     float(rs.min()),
        "r_b_over_c_max":     float(rs.max()),
        "r_b_over_c_spread":  float(rs.max() / rs.min()),
        "q_a_over_c_min":     float(qs.min()),
        "q_a_over_c_max":     float(qs.max()),
        "q_a_over_c_spread":  float(qs.max() / qs.min()),
        "n_pairings":         len(rows),
        "verdict":            classify(float(rs.max() / rs.min())),
    }


def classify(spread: float) -> str:
    """ATTACK_DESIGN PASS criterion: spread <= 1.20 (i.e. ±20% band)."""
    if spread <= 1.20:
        return "PASS"
    if spread <= 2.00:
        return "PARTIAL"
    return "FAIL"


def main() -> None:
    rows = pairwise_ratios(ANCHORS)
    summary = summarise(rows)
    diag = cubic_consistency_check(rows)

    out = {
        "input_anchors": ANCHORS,
        "ansatz":        "beta(sigma) = a*sigma - b*sigma^2 + c*sigma^3",
        "scenario":      "Sc-A: pick 2 of 3 anchors as nontrivial FPs",
        "pairings":      rows,
        "summary":       summary,
        "diagnostics":   diag,
        "honest_note":   (
            "Only b/c and a/c ratios are extracted; absolute b, c remain "
            "non-priori (L352 PARTIAL boundary respected). Selecting the "
            "'correct' pairing requires data beyond this script."
        ),
    }

    out_path = OUT_DIR / "extraction_result.json"
    out_path.write_text(json.dumps(out, indent=2))

    # Console report (ASCII only, per cp949 safety rule)
    print("L391 b/c ratio numerical extraction")
    print("-" * 56)
    for row in rows:
        print(
            f"  pair={row['FP_pair']:<22} "
            f"r=b/c={row['r_b_over_c']:.3f}  "
            f"q=a/c={row['q_a_over_c']:.3f}  "
            f"third={row['third_anchor']['name']}({row['third_anchor']['value']:.2f})"
        )
    print("-" * 56)
    print(
        f"  r range  : [{summary['r_b_over_c_min']:.3f}, "
        f"{summary['r_b_over_c_max']:.3f}]  spread x {summary['r_b_over_c_spread']:.3f}"
    )
    print(
        f"  q range  : [{summary['q_a_over_c_min']:.3f}, "
        f"{summary['q_a_over_c_max']:.3f}]  spread x {summary['q_a_over_c_spread']:.3f}"
    )
    print(f"  verdict  : {summary['verdict']}")
    print(f"  output   : {out_path}")


if __name__ == "__main__":
    main()
