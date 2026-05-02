# L378 — Single-anchor Leave-One-Out (LOO) on monotonic vs non-monotonic σ₀(ρ_env)

## Target

L342 baseline (3 anchors: cosmic / cluster / galactic) yields Δχ²(M1_linear − M2_parabola) ≈ 288 (formal "16.97σ"). We attack: **is this entirely driven by the single cluster anchor, or is it distributed?**

Honest expectation: with N=3 and a V-shape (cluster < cosmic < galactic in log σ₀), removing **cluster** must collapse Δχ². The forensic question is *how* the other two LOO subsets behave — if they also retain large Δχ², then non-monotonicity is genuinely 3-anchor structural; if only cluster matters, the "16.97σ" reduces to a single-point claim and the result is fragile.

## Models (identical to L342)

- M1: y = A + B·x (linear, monotonic, k=2)
- M2: y = C + D·(x − x_min)² (parabola, non-monotonic, k=3)

## LOO procedure (two complementary tests)

### Test A — direct N=2 fits (limit case)

Drop one anchor, refit both M1 and M2 on N=2.
- M1 (k=2, N=2): saturated → χ² = 0 (always).
- M2 (k=3, N=2): under-determined → χ² = 0 with x_min free, ill-defined.

Therefore Test A is uninformative *as a fit comparison* but anchors the saturation regime; we record it for transparency.

### Test B — LOO predictive χ² (the real test)

For each held-out anchor i:
1. Fit M1 on the remaining 2 points (saturated) → unique linear extrapolation.
2. For M2, fix x_min to the full-data MAP from L342 (x_min* = −24.7346) so M2 reduces to k=2 (C, D); fit on remaining 2 points (saturated) → unique parabola.
3. Predict y_i and form **predictive residual** χ²_pred,i = ((y_i − ŷ_i)/σ_i)².
4. Compare χ²_pred,i,M1 vs χ²_pred,i,M2.

The contribution of anchor i to the L342 Δχ² claim is then **δ_i = χ²_pred,i,M1 − χ²_pred,i,M2**.

If δ_cluster ≫ δ_cosmic + δ_galactic, the result is a single-point V-shape detection — **fragile**.
If all three δ_i are comparable, the V-shape is structurally supported by 3 directions.

### Test C — full-data ΔAICc with one σ_i → ∞

Equivalent to "remove anchor i" via likelihood marginalization while keeping N=3 in degree-of-freedom counting (so AICc is defined for k=2 and we can take the k=3 vs k=2 ΔAICc on the surviving 2 informative points + 1 noise point).

We report Δχ²(M1 − M2_xmin-fixed) with σ_i inflated by ×10⁶ for each i. This is the cleanest "leave-out" measure that keeps the AICc machinery alive.

## Honesty flags

- N=3 LOO is intrinsically a single-point predictive test, not a Bayesian cross-validation. We do NOT claim significance from LOO; we use it only as a **fragility diagnostic**.
- The cluster anchor (log10 σ₀ = 7.75) is the V-shape valley. By construction, removing it linearizes the data. The honest question is the **size** of δ_cluster vs δ_cosmic, δ_galactic, *not* whether δ_cluster > 0.
- "Driver" criterion (pre-registered): if max_i(δ_i) / Σ_j δ_j > 0.85, declare "single-anchor driver — fragile".
- This loop does NOT update the L371 grade until cluster pool (L347–L350) is executed; it only diagnoses fragility of the existing 3-anchor claim.

## Decision rules

- If cluster is the dominant driver (>0.85 share): L378 records FRAGILE flag. Paper Sec 3 (3-regime narrative) must add a sentence: "the 3-anchor χ² LRT is dominated (>85%) by the single cluster point; cluster pool expansion (L347–L350) is required for robust detection."
- If all three anchors contribute comparably: L378 records ROBUST-IN-3 flag (subject to systematics). Narrative unchanged.
- If cosmic or galactic dominates instead: surprising; investigate sigma assignments.

## Output

`results/L378/report.json` with:
- baseline (L342 reproduction),
- per-anchor (Test B) predictive residuals for M1 and M2 (x_min fixed),
- per-anchor (Test C) σ_i→∞ Δχ² values,
- driver share fractions,
- pre-registered FRAGILE/ROBUST flag.
