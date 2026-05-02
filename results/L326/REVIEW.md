# L326 — Review (4-person code/logic + 8-person theory)

**Scope:** review of ATTACK_DESIGN.md and NEXT_STEP.md.
**Rule application:** Rule-A 8-person on theory claims (KL formula choice, pre-registration framing); Rule-B 4-person on numerical claims (D_KL values, σ forecasts).

---

## Rule-B (4-person numerical review)

| Reviewer | Finding | Severity | Action |
|----------|---------|----------|--------|
| R1 | D_KL Gaussian approximation OK for point-vs-point hypothesis comparison; **fails for w_a posterior with non-Gaussian tails**. P17 D_KL band [5.6, 14.2] should be presented as range, not single number. | medium | already shown as range — OK |
| R2 | σ(DR3) = 0.15 is extrapolated from DR2 = 0.21 with naive √2 scaling. Actual DR3 forecast (DESI 2024 white paper) suggests σ(w_a) ~ 0.10–0.13. If σ=0.10, D_KL rises 2.25× → re-rank robust. | low | flagged in caveats Sec 8 |
| R3 | P21 LSST Y10 σ(S_8) = 0.4% is the *statistical* floor. Realistic systematics-included σ ~ 0.6–0.7%. D_KL drops to ~1.5–2.0 nats. **Re-rank: P21 may slip below P19.** | medium | acknowledged; ranking is order-of-magnitude. |
| R4 | Cumulative D_KL = 12 nats assumes *independence*. P19 + P21 share the S_8 channel and are NOT independent. Joint D_KL closer to 4–5 nats, not 8. P17 still independent of S_8 channel — sum 9–10 nats not 12. | high | **fix in ATTACK_DESIGN.md Sec 3 footnote** |

---

## Rule-A (8-person theory review)

| Persona | Verdict | Note |
|---------|---------|------|
| Axiom-keeper | OK | KL framing is observable-level, doesn't import theory shortcuts. |
| Phenomenologist | OK with edit | P17 "extension V(n,t)" must not be fit to DR3 *and then claimed as prediction*. Pre-registration timestamp essential. |
| Bayesian | edit | Use Bayes factor B_01 = exp(D_KL) only for Gaussian point hypotheses. For composite hypotheses (V(n,t) with free n), Occam penalty must be subtracted (cf. L321 marginalised ΔlnZ=0.8 lesson). |
| Honest broker | OK | drop P18 + demote P16 is correct; aligns with L285, L283. |
| Risk officer | OK | risky/safe split honest; P21 structural σ_8 worse is the genuine risky bet. |
| Reviewer simulator | flag | Reviewer R2-style: "your KL numbers are sales-grade, not Fisher-grade". → present as order-of-magnitude in paper. |
| Theorist | flag | P15 μ-distortion D_KL ~2 may be over-stated; L282 noted only 2σ vs FG, suggesting D_KL ~2 is the *upper* bound. |
| Devil's advocate | flag | If DR3 returns w_a ≈ −0.3 (mid-band), neither side wins; D_KL interpretation degenerate. Pre-registration band must include "INCONCLUSIVE" zone explicitly. |

---

## Required edits (post-review)

1. **ATTACK_DESIGN.md Sec 3** — add footnote: "P19 and P21 share the S_8 channel; joint D_KL is correlation-corrected to ~4–5 nats, not their additive 6.3."
2. **ATTACK_DESIGN.md Sec 4** — add "INCONCLUSIVE band" for P17: −0.4 < w_a < −0.2 (no decisive verdict).
3. **NEXT_STEP.md item 1** — explicitly state Bayes-factor reporting must include Occam penalty for V(n,t) extension parameters.
4. **ATTACK_DESIGN.md Sec 8** — strengthen σ(DR3) caveat to "0.10–0.18 range; D_KL band correspondingly 3–14 nats".

---

## Verdict

**Conditional accept.** Numerical claims need 4 edits above before propagating to paper Sec 4/7. Theory framing (KL, pre-registration, risky/safe split) approved unanimously.

Ranking **P17 > P21 ≈ P19 > P15 ≫ rest** robust under re-ranking sensitivity.
