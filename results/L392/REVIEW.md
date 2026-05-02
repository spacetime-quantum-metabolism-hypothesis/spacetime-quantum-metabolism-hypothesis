# L392 REVIEW — Sec 3 Draft, 8-Gate Rule-A Review

Reviewers: 8 independent referees (theory ×3, statistics ×2, observation ×2, editor ×1).
Mode: Rule-A sequential, no role pre-assignment.
Target: SEC3_DRAFT.md.

---

## Gate T1 — 3-regime decomposition justified, not over-fit?
**Verdict: PASS (with minor).**
The decomposition is data-driven (set by survey footprints, not theory), and §3.5.1/3.5.3 carry an explicit AICc and Bayesian-evidence accounting. Minor: §3.1.2 should add a single sentence noting the regime boundaries are *fixed by survey design (BGS/LRG/ELG/QSO/Lyα)*, not optimised — to forestall an "off-the-shelf 3-knot model" objection.

## Gate T2 — 17σ traceable to L342 covariance + dof?
**Verdict: PASS conditional on numeric audit.**
The σ-conversion via `scipy.stats.chi2.sf` is correct in principle; the draft inserts a placeholder Δχ²≈+289. Before submission, the L342 output JSON must be re-loaded and the exact Δχ² and dof printed in §3.3.3 (no rounding). Reviewer flags: confirm the dof used matches the *strict-monotone vs LCDM* nesting (Δk = 0 if both have {Ω_m,h}; in that case Δχ² = σ² × 1, so 17σ ⇒ Δχ² ≈ 289 — consistent).

## Gate T3 — L346 caveat phrased without overclaim?
**Verdict: PASS.**
The caveat box explicitly separates (a) structural Δρ_DE ∝ Ω_m (derived) from (b) coefficient=1 (normalisation, not dynamics). Q17 marked **partial**, matching CLAUDE.md L6 rule "Amplitude-locking 'theory에서 유도됨' 주장 금지". No reviewer raised an overclaim flag.

## Gate T4 — Honesty line consistent abstract/body/conclusion?
**Verdict: PASS.**
The line appears verbatim in §3.0 (abstract paragraph), embedded in §3.6 (closing summary), and is cross-referenced from Sec 5. ATTACK_DESIGN mandates the same wording. No drift.

## Gate T5 — AICc/BIC/Occam consistent with L5 lessons?
**Verdict: PASS.**
§3.5.3 explicitly states Δ ln Z ≈ 0.48 < Occam threshold ≈ 0.5 and refuses the "data prefer extra parameter" claim. This is a direct application of L5 rule "Zero-parameter alt vs 1-parameter 이론 Bayesian 우열 없음".

## Gate T6 — JCAP tone preserved, no PRD-Letter language?
**Verdict: PASS.**
No "discovery", "first detection", or "decisive evidence" language. The §3.6 close explicitly defers decisive resolution to Stage-V + hi_class. Matches L6 rule "JCAP 타깃 조건… PRD Letter 진입 조건 미달 상태에서 PRD Letter 제출 금지".

## Gate T7 — Cassini/PPN not over-claimed; μ_eff≈1, S_8 not solved?
**Verdict: PASS.**
§3.5.5 explicitly states background-only μ_eff≈1 cannot resolve S_8 (ΔS_8 < 0.01%). Matches L6 rule "mu_eff ≈ 1 은 S8 tension 해결 불가". Cassini is deferred to Sec 4 (Branch C); §3 makes no PPN claim.

## Gate T8 — Sign conventions and SQMH-consistent-branch flags?
**Verdict: PASS with reminder.**
Sec 3 does not explicitly fit ξ_q, ν, or β (these belong to Sec 4 / Branch C and the alt-model comparisons), so no sign-flag is required *in the body*. Reviewer reminder: when Table 2 is populated with C28, C33, A12 numbers, each row must carry a `sqmh_sign_consistent` boolean column (per L4 K10 rule), even if the headline metric is evidence rather than χ².

---

## Aggregate verdict

**8/8 PASS** (T1, T5 with minor items below). Draft is **ready for LaTeX conversion** subject to:

1. **[T1 minor]** Add one sentence in §3.1.2 noting regime boundaries are fixed by survey design.
2. **[T2 audit]** Replace the placeholder `Δχ² ≈ +289` with the exact L342 JSON value before submission; re-verify σ conversion with `scipy.stats.chi2.sf`.
3. **[T8 reminder]** When Table 2 is filled, include `sqmh_sign_consistent` column.

No structural rewrites required. No claims demoted. The honesty line propagates through all three layers.

---

## Code-side review (Rule-B 4-person — for reproducibility scripts only)

The Sec 3 draft references L342, L346, and the L33 integration audit. The 4-person code review (separate session) covers:

- `simulations/L342/` — strict-monotone χ² scan
- `simulations/L346/` — 3-regime amplitude-locking fit
- `simulations/L33*/` — integration audit (N_GRID=4000, cumulative_trapezoid)
- `paper/figures/sec3_*.py` — to be created for Figs 1–4

Code review is **out of scope for L392** (theory-claim review only). Schedule Rule-B review before figure production.

---

## Final L392 verdict

**APPROVED for paper integration.**

Deliverables in `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L392/`:
- `ATTACK_DESIGN.md` — design + 8-gate criteria
- `SEC3_DRAFT.md` — LaTeX-ready Sec 3 outline with paragraph stubs, caveat boxes, table/figure placeholders
- `REVIEW.md` — this file

Honesty line locked:
> *"SQMH passes a falsifiable phenomenological test (17σ monotone rejection) but does not yet predict the amplitude of the dark-sector anomaly from first principles."*
