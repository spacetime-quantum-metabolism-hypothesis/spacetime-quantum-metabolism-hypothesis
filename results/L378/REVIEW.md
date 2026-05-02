# L378 — REVIEW: which anchor drives the non-monotonicity claim?

## Headline

**Decision: ROBUST-IN-3 (distributed driver).**
Pre-registered fragility criterion (max share of positive Δχ² > 0.85) is **not met**. No single anchor accounts for ≥85% of the L342 LRT signal under leave-one-out predictive χ².

## Numbers (Test B — LOO predictive χ²)

| Left-out anchor | χ²_pred(M1, linear) | χ²_pred(M2, x_min fixed) | Δχ² | share |
|---|---:|---:|---:|---:|
| cosmic   | 1640.250 | 0.000 | 1640.250 | 0.372 |
| cluster  |  410.063 | 0.000 |  410.063 | 0.093 |
| galactic | 2361.960 | 0.000 | 2361.960 | 0.535 |
| **total** |          |       | 4412.273 | 1.000 |

The L342 baseline Δχ²(M1−M2) = 288.04 is reproduced exactly.

## Interpretation — and the surprise

The user's pre-task hypothesis ("likely cluster is driver, fragile") is **not** supported by Test B. The cluster anchor contributes the *smallest* predictive Δχ² (9.3%), not the largest. The two **endpoints** (galactic 53.5%, cosmic 37.2%) carry the V-shape signal under LOO.

Reason (honest geometric reading):
- The L342 V-shape has its valley near x = −24.73 (between cluster and galactic-side, very close to cluster's x = −24).
- When **cluster** is held out, the M1 linear fit on (cosmic, galactic) extrapolates *toward* cluster's x = −24 with slope (9.56 − 8.37)/6 ≈ 0.198, predicting y(−24) ≈ 8.965; the parabola with x_min fixed near cluster naturally bends back to ≈ 7.75 — but cluster is *next to* the valley, so the linear miss is "only" Δy ≈ 1.21 → χ² ≈ 410.
- When **cosmic** or **galactic** is held out, the linear extrapolation from the remaining two has to traverse the valley either inward or outward, accruing very large predictive miss → χ² > 1640.

So under LOO, **the V-shape signal is carried by the asymmetry between the two endpoints relative to the valley**, not by the valley point itself. Removing the valley (cluster) actually leaves the LOO predictive χ² for M1 *smaller* (because the remaining endpoints can be fit linearly with less violence).

## Caveat — Test B is M2-friendly

Test B fixes x_min to the full-data MAP (x_min* = −24.7346). The held-out point therefore *informed* x_min, which leaks information into the M2 prediction (M2 always achieves χ² = 0 on the kept pair, and produces a sensible prediction at the held-out point). This biases Test B toward M2 uniformly. The diagnostic is valid as a **fragility floor**: if even with this M2-friendly setup one anchor exceeded 85% share, that would be definitive fragility. Inverse interpretation (low share ⇒ robust) is *weakly* supported only.

## Test C — uninformative as designed

With N=3 and one σ_i → ∞, only 2 points are informative. Both M1 (k=2) and M2 (k=3, x_min free) saturate to χ² = 0. Test C contributes nothing beyond confirming the saturation regime, exactly as flagged in ATTACK_DESIGN.md.

## Honest fragility verdict

The L342 "16.97σ-equivalent" Δχ² = 288 LRT remains a 3-point claim — it cannot, by construction with N=3, be decisively LOO-validated. What L378 establishes is:

1. **No single-anchor monopoly**: under the pre-registered criterion, the signal is *not* dominated by one anchor (max share 53.5% < 85%).
2. **Cluster is NOT the driver**: contrary to a-priori intuition, cluster contributes only 9.3% of the LOO Δχ². The endpoints (cosmic, galactic) carry most of the V-shape signal.
3. **Real fragility lies elsewhere**: the result is fragile to (a) systematic shifts in y_galactic or y_cosmic (53.5% and 37.2% leverage respectively), (b) the σ assignments (0.05–0.06 dex), and (c) the x_env mapping (±1 dex shifts not tested here — flagged for L347–L350 cluster pool follow-up).

## Action items (paper / next loops)

- Sec 3 narrative: do NOT add the "single cluster point dominates" sentence — it's empirically false under LOO.
- Sec 6 limitations: add "L378 LOO shows the 3-anchor LRT signal is carried 89% by the two endpoints (cosmic + galactic); endpoint systematics dominate the fragility budget; cluster pool expansion (L347–L350) addresses cluster but does not address endpoint robustness."
- L379+ candidates: (a) galactic anchor systematics audit (lab/disc σ₀ choice), (b) cosmic anchor systematics audit (void/IGM σ₀ choice), (c) re-examine x_env mapping uncertainty.

## One-line summary

> Under LOO, the L342 non-monotonicity LRT is carried by the two **endpoint** anchors (cosmic 37%, galactic 54%), not by the cluster valley point (9%); no single anchor exceeds the 85% fragility threshold, but endpoint systematics — not cluster systematics — are the real fragility budget.
