"""
L407 — RG saddle FP location distribution.

Question: Given β(σ) = a σ - b σ² + c σ³ (cubic RG flow on log σ),
how naturally does the saddle (middle FP) land near log σ_cluster ≈ 7.75
when (a, b, c) are scanned over physically motivated ranges?

Method:
  - Fix the two outer FP roots at the cosmic/galactic anchors (log σ_cosmic=8.37,
    log σ_galactic=9.56) by reparametrising β = c (σ - σ_IR)(σ - σ_saddle)(σ - σ_UV).
  - The saddle position σ_saddle is then *one* free axis. We instead run the
    inverse problem: scan (a, b, c) freely on a grid, solve for the three real
    roots, and ask what fraction of triplets place the middle root within the
    "cluster band" [7.5, 8.0] (log10 m^2 kg^-1 s).
  - Naturalness metric: P(saddle ∈ cluster band | random a,b,c with three real roots).
  - Compare to a uniform-prior null on the band [log σ_IR, log σ_UV] = [8.37, 9.56].
    Note: the empirical cluster anchor 7.75 lies *below* the cosmic IR root —
    the cubic RG topology does NOT contain the cluster value between the two
    outer FPs. This is recorded as a structural finding.
  - Also probe the sign-flipped topology (saddle below IR, two outer above):
    β = -a σ + b σ² - c σ³ class, scanning negative leading coefficient.

Output: results/L407/saddle_distribution.json + .png histogram.
"""
from __future__ import annotations
import json, os, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "L407"
OUT.mkdir(parents=True, exist_ok=True)

# ---- anchors (log10 sigma_0) ----
LOG_COSMIC = 8.37
LOG_CLUSTER = 7.75
LOG_GALACTIC = 9.56

CLUSTER_BAND = (7.50, 8.00)   # +/- 0.25 dex around empirical cluster anchor
BETWEEN_BAND = (LOG_COSMIC + 0.05, LOG_GALACTIC - 0.05)  # naive "between IR and UV"

RNG = np.random.default_rng(20260501)


def cubic_roots(a: float, b: float, c: float):
    """Real roots of c x^3 - b x^2 + a x = 0  (β=0).
    One root is x=0; the other two come from c x^2 - b x + a = 0.
    We work in shifted variable x = log10 sigma to keep ranges sane.
    """
    # β(x) = a x - b x^2 + c x^3, factor x: x (a - b x + c x^2)
    # roots: 0, and quadratic c x^2 - b x + a = 0
    disc = b * b - 4 * c * a
    roots = [0.0]
    if disc >= 0 and c != 0:
        s = np.sqrt(disc)
        roots.append((b - s) / (2 * c))
        roots.append((b + s) / (2 * c))
    return sorted(roots)


def shifted_cubic_roots(a, b, c, x0):
    """β(x) = a (x-x0) - b (x-x0)^2 + c (x-x0)^3, return real roots in x."""
    rs = cubic_roots(a, b, c)
    return sorted([r + x0 for r in rs])


def run_scan(n_samples=200_000, x0=LOG_COSMIC):
    """Scan (a,b,c) coefficient grid; record middle-root distribution."""
    # log-uniform magnitudes; signs random
    log_a = RNG.uniform(-2.0, 2.0, n_samples)
    log_b = RNG.uniform(-2.0, 2.0, n_samples)
    log_c = RNG.uniform(-2.0, 2.0, n_samples)
    sa = RNG.choice([-1.0, 1.0], n_samples)
    sb = RNG.choice([-1.0, 1.0], n_samples)
    sc = RNG.choice([-1.0, 1.0], n_samples)

    a = sa * 10 ** log_a
    b = sb * 10 ** log_b
    c = sc * 10 ** log_c

    middles = []
    spans = []
    n_three_real = 0
    for i in range(n_samples):
        rs = shifted_cubic_roots(a[i], b[i], c[i], x0)
        if len(rs) != 3:
            continue
        n_three_real += 1
        middles.append(rs[1])
        spans.append(rs[2] - rs[0])
    return np.array(middles), np.array(spans), n_three_real, n_samples


def constrained_scan(n_samples=200_000):
    """Force two outer roots at cosmic/galactic anchors; saddle is the third.
    β(x) = c (x - x_IR)(x - x_S)(x - x_UV). x_S is uniform in some prior.
    Compare priors: (i) uniform on [x_IR, x_UV] (between), (ii) uniform on
    [x_IR - 1, x_UV + 1] (extended to allow cluster anchor below x_IR).
    """
    xIR, xUV = LOG_COSMIC, LOG_GALACTIC
    # prior i: between
    xs_between = RNG.uniform(xIR, xUV, n_samples)
    # prior ii: extended (allows cluster<IR)
    xs_extended = RNG.uniform(xIR - 1.0, xUV + 1.0, n_samples)
    # prior iii: log-flat on |x - midpoint| — mildly favors center
    return xs_between, xs_extended


def fraction_in(arr, lo, hi):
    return float(np.mean((arr >= lo) & (arr <= hi)))


def main():
    print("[L407] running RG saddle FP distribution scan ...")
    middles, spans, n3, ntot = run_scan(n_samples=300_000)
    p_three = n3 / ntot

    # naturalness metrics
    frac_cluster_band = fraction_in(middles, *CLUSTER_BAND)
    frac_between = fraction_in(middles, *BETWEEN_BAND)
    # narrow band around empirical cluster anchor
    frac_pm005 = fraction_in(middles, LOG_CLUSTER - 0.05, LOG_CLUSTER + 0.05)
    frac_pm010 = fraction_in(middles, LOG_CLUSTER - 0.10, LOG_CLUSTER + 0.10)

    # constrained-anchor null
    xs_between, xs_extended = constrained_scan(300_000)
    null_between_cluster = fraction_in(xs_between, *CLUSTER_BAND)
    null_extended_cluster = fraction_in(xs_extended, *CLUSTER_BAND)

    # KEY structural finding: cluster anchor 7.75 lies BELOW cosmic IR 8.37.
    # If the cubic RG topology saddle is forced to lie BETWEEN x_IR and x_UV
    # (standard Wetterich monotone flow assumption), then P(saddle ∈ cluster
    # band | between-prior) = 0 by construction.
    structural_zero = (CLUSTER_BAND[1] < LOG_COSMIC)

    summary = {
        "anchors": {
            "log_sigma_cosmic": LOG_COSMIC,
            "log_sigma_cluster": LOG_CLUSTER,
            "log_sigma_galactic": LOG_GALACTIC,
        },
        "cluster_band": CLUSTER_BAND,
        "scan": {
            "n_total": ntot,
            "n_three_real": int(n3),
            "p_three_real": p_three,
        },
        "free_scan_naturalness": {
            "P_saddle_in_cluster_band[7.50,8.00]": frac_cluster_band,
            "P_saddle_in_between_IR_UV[8.42,9.51]": frac_between,
            "P_saddle_within_pm0.05_of_7.75": frac_pm005,
            "P_saddle_within_pm0.10_of_7.75": frac_pm010,
        },
        "constrained_anchor_null": {
            "P_uniform_between[8.37,9.56]_in_cluster_band": null_between_cluster,
            "P_uniform_extended[7.37,10.56]_in_cluster_band": null_extended_cluster,
        },
        "structural_finding": {
            "cluster_below_cosmic_IR": structural_zero,
            "note": (
                "log sigma_cluster=7.75 < log sigma_cosmic=8.37. The standard "
                "Wetterich monotone-RG cubic-saddle topology places the saddle "
                "BETWEEN the IR and UV fixed points. The empirical cluster "
                "anchor lies BELOW the IR root, so a strictly-between-FP "
                "saddle topology CANNOT host the cluster anchor. RG saddle "
                "naturalness is therefore P=0 under the standard topology, "
                "and requires either (a) reordering anchors (cluster as a "
                "deeper IR FP, cosmic as saddle), or (b) an off-axis / extra "
                "operator extension."
            ),
        },
    }
    # Histogram of free-scan middle roots, restricted to a reasonable window
    fig, ax = plt.subplots(figsize=(7, 4))
    msel = middles[(middles > 5) & (middles < 12)]
    ax.hist(msel, bins=80, density=True, color="#3a7", alpha=0.75,
            label=f"free RG scan (n={len(msel)})")
    for x, lbl, col in [
        (LOG_COSMIC, "cosmic IR (8.37)", "#1f77b4"),
        (LOG_CLUSTER, "cluster (7.75)", "#d62728"),
        (LOG_GALACTIC, "galactic UV (9.56)", "#2ca02c"),
    ]:
        ax.axvline(x, color=col, ls="--", lw=1.5, label=lbl)
    ax.axvspan(*CLUSTER_BAND, color="#d62728", alpha=0.10,
               label=f"cluster band {CLUSTER_BAND}")
    ax.set_xlabel(r"$\log_{10}\sigma_0$ at saddle (middle root)")
    ax.set_ylabel("density")
    ax.set_title("L407 — RG cubic saddle FP location distribution")
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    fig.savefig(OUT / "saddle_distribution.png", dpi=130)
    plt.close(fig)

    with open(OUT / "saddle_distribution.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))
    print(f"[L407] wrote {OUT/'saddle_distribution.json'}")
    print(f"[L407] wrote {OUT/'saddle_distribution.png'}")


if __name__ == "__main__":
    main()
