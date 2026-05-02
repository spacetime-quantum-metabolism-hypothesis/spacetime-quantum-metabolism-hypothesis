# SQMH / SQT — Frequently Asked Questions (English)

> Companion to `paper/base.md` §8. Three tiers: one-sentence answers (Q1–Q4),
> one-paragraph answers (Q5–Q9), and student / advanced answers (Q10–Q12).
> Wording is locked to the same honesty bar as the Korean mirror (`faq_ko.md`).

---

## Tier 1 — One-sentence answers

**Q1. What is SQT?**
A hypothesis that treats spacetime as a countable medium whose quantum
absorption and emission jointly source gravity and the cosmic acceleration
from a single set of axioms.

**Q2. Has it been tested?**
Four substantive checks pass (Newton recovery, BBN ΔN_eff, Cassini β_eff,
weak equivalence principle η = 0); the Λ-origin claim is downgraded to a
`CONSISTENCY_CHECK` (dimensional, *not* a prediction), and S_8 is
*structurally worsened* by +1.14% — pre-registered as a 4.4σ Euclid DR1
cosmic-shear falsifier.

**Q3. What is the decisive test?**
DESI DR3 w_a (2025–2026) for the background channel and Euclid DR1
cosmic-shear ξ_+ (2026–2027, central 4.38σ, 3σ falsification floor) for
the perturbation channel — both pre-registered with a triple timestamp
(arXiv ID + GitHub tag + OSF DOI) before data release.

**Q4. Is it trustworthy?**
All code and data are public on GitHub, the 22-row honest-limit table is
in the body of the paper, and any reader can reproduce the headline
numbers in five seconds of Python or thirty minutes of an LLM prompt.

---

## Tier 2 — One-paragraph answers

### Q5. How is SQT different from other theories?

Most modified-gravity proposals (MOND, TeVeS, f(R), Galileon …) *modify
the gravitational law*. SQT instead modifies the *dynamics of spacetime
itself*: a single set of six axioms (mass-action absorption + emission,
emergent metric, dark-only sector embedding) lets gravity *and* a
cosmological-constant-scale ρ_Λ emerge from the same underlying
process. The trade-off is that the Λ scale matches only at the level of
*dimensional consistency* (see Q11), not as a true a-priori prediction.

### Q6. What are the weaknesses?

We acknowledge three structural weaknesses up front. (a) S_8 is
*worsened* by +1.14% — this is structural, not a fit failure, and is
pre-registered as a 4.4σ Euclid DR1 cosmic-shear falsifier (central
4.38σ; 4.19σ after prediction-uncertainty quadrature; 3σ floor).
(b) The non-monotonic environmental dependence of σ₀(t) was *found in
the data* (postdiction), not predicted a priori; mock-injection studies
flag a 100% false-detection rate on this anchor. (c) The RG coefficients
b, c are not derived from first principles — they are anchor-fit. Of the
32-claim self-audit, only **13% (4 claims)** are substantive falsifiable
predictions (Newton recovery, BBN ΔN_eff, Cassini β_eff, EP η = 0); the
raw 28% PASS_STRONG headline must always be reported alongside this 13%.

### Q7. Will this affect daily life?

No direct effect. SQT departures from standard gravity are measurable
only on cluster (~10⁶ ly) and cosmological (~10¹⁰ ly) scales. Solar-system
gravity and laboratory physics are indistinguishable from
Newton/Einstein at all currently testable precisions (Cassini, lunar
laser ranging, MICROSCOPE).

### Q8. What if SQT is right?

The Λ scale would have a *partial* axiom-level origin (full a-priori
derivation is blocked by the circularity in Q11), and MOND-like
phenomenology would emerge from spacetime dynamics rather than from a
modified force law. The cosmological-constant problem would be reframed,
not fully solved — but the framing itself is a measurable advance.

### Q9. What if SQT is wrong?

The honest framework remains useful as a case study: the 22-row honest
limit table, the 32-claim self-audit (raw 28% / substantive 13%), the
mock-injection caveats, and the pre-registered Euclid 4.4σ falsifier
quantify *exactly how* the theory can fail. That structure — not the
theory itself — is meant to outlive any specific model.

---

## Tier 3 — Student / advanced answers

### Q10. What does it mean that axiom 4 (emergent metric) has an OPEN microscopic origin?

Axiom 4 states that the macroscopic metric *emerges* from a discrete
quantum substrate. At the macroscopic scale this reproduces general
relativity (PASS by inheritance for Newton, GW170817, LLR, EP). The
microscopic substrate, however, is not uniquely fixed: loop quantum
gravity, causal sets, and tensor networks are all candidate carriers,
and a coarse-grained causal-set ("causet meso") realisation passes 4 of
5 conditional checks. Resolving which substrate is correct is OPEN and
tagged `NOT_INHERITED` in the 22-row table.

### Q11. If ρ_q / ρ_Λ = 1.0000 is exact, why a circularity caveat?

Because the steady-state number density n_∞ is derived using ρ_Λ_obs
*as an input* (axiom 3 normalisation). The exact 1.0000 is therefore an
identity that follows from unit conversion, *not* a falsifiable a-priori
prediction. The L402 audit confirmed that an independent derivation
fails by 10⁶⁰. The L412 review accordingly downgraded the Λ-origin
status from `PASS_STRONG` to `CONSISTENCY_CHECK` (dimensional/order-unity
consistency only). What survives is (a) a dimensional-analysis match of
the ρ_Λ scale, and (b) order-of-magnitude naturalness — both worth
reporting, neither a prediction.

### Q12. How can I help?

Three concrete channels. (1) Reproduce the headline numbers: run the
five Python scripts shipped in the verification appendix or paste the
five LLM prompts into your preferred model. Open a GitHub issue if any
output disagrees. (2) Stress-test the 22-row honest limit table — every
row is meant to be falsifiable. (3) When DESI DR3 (2025–2026) and Euclid
DR1 cosmic shear (2026–2027) data are released, compare the
pre-registered SQT predictions (w_a sign and band; +1.14% S_8 excess
with the four-band two-sided decision rule of §4.6) against the
measurements and report the verdict publicly.
