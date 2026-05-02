# Cover Letter v2 — JCAP Submission

**Manuscript**: Spacetime Quantum Metabolism Hypothesis (SQMH) — A Falsifiable, Pre-Registered Phenomenology Across Cosmic, Cluster, and Galactic Regimes

**Target journal**: JCAP (Journal of Cosmology and Astroparticle Physics)
**Positioning**: Honest falsifiable phenomenology. We do not claim PRD-Letter-level structural breakthroughs.
**Date**: 2026-05-01
**Internal cumulative loop count**: ~268 independent audit/recovery rounds (L77–L368).

---

## 1. What this submission is — and what it is not

This paper presents a phenomenological framework (SQMH) that predicts a regime-dependent metabolic-coupling parameter σ_0 across three regimes (cosmic, cluster, galactic). The predictions are tied to a single underlying axiom set; the eight pre-registered falsifiers in Appendix A make every quantitative claim refutable on near-term data (DESI DR3, Euclid Q1, LSST Y1, KiDS+, PSZ2 cross-checks).

We submit this as **honest falsifiable phenomenology**. We do **not** claim:

- a structural resolution of the S₈ tension (μ_eff ≈ 1 in the background-only sector; ΔS₈ < 0.01% in our analysis),
- a Bayesian preference over ΛCDM beyond Occam-uncorrected fixed-θ evidence,
- that an "extra parameter is preferred by data" (the Occam-corrected Δln Z is consistent with parameter agnosticism),
- that SQMH and the independent Maggiore-Mancarella RR non-local model (C28 in our internal taxonomy) are theoretically equivalent — the phenomenological alignment we document is not a derivation.

## 2. Honest disclosure (the core of v2)

Compared with v1 (cover letter circulated internally at the L321 milestone), v2 explicitly discloses every limitation surfaced by our internal audit rounds L322–L341. We list these in the body, not as supplementary material:

**L1. Effective dimensionality is ≈ 1 (sloppy posterior).** A multi-start Hessian + MBAM analysis on the BB σ_0 posterior (cosmic, cluster, galactic) shows the posterior is cluster-dominant with a stiff direction v_max ≈ 0.81–0.98. The three-σ_0 parameterisation is over-specified relative to the information content of current data.

**L2. Three-regime partition is not data-forced.** A two-regime (cosmic+cluster merged) baseline yields ΔAICc in the range −7 to −67 in forecasts; the three-regime split is justified narratively, not by current AICc. We adopt the two-regime model as baseline and treat the three-regime case as a forecast-tested extension (P11 NS forecast).

**L3. Pillar 4 (parameter parsimony) is downgraded.** RG fixed-point parameters (b, c) cannot be derived a priori from the SQMH axiom set as currently formulated; they are post-hoc fits. We rate pillar 4 at ★★ (down from ★★★).

**L4. Cluster constraint relies on a single source (A1689) at present.** A 13-cluster pool (LoCuSS / CLASH / PSZ2 archive) has been identified for follow-up; numerical results in this paper use A1689 only. The L350 PSZ2-vs-lensing selection-bias analysis is included as a separate companion check, not as a calibration.

**L5. Subset-Bayes 5-dataset MCMC is incomplete.** A 24–30-hour MCMC over five datasets with ϒ marginalisation (d = 181 → 6) is designed and pre-registered (F1–F4 gates) but not executed in this submission.

**L6. Microphysical theory is at an 80% completeness ceiling.** Four of five gap-closures are partial; the a4 emergent-metric channel remains OPEN. We do not claim a complete derivation from L0/L1.

**L7. SymG mock false-positive rate is in the 30–80% range** (preliminary). The cross-validation completion is deferred.

**L8. BMA model weights are robust but Occam-sensitive.** Under proper Bayesian model averaging the BB family receives BIC weight ≈ 92.6%, Laplace ≈ 81%, AIC ≈ 59% — robust to model framing but the Laplace-vs-fixed-θ gap is non-trivial; we flag it.

**L9. P17 pre-registration is two-tier.** Tier A (Λ-static predictions) is locked and is the basis of the eight falsifiers in Appendix A. Tier B (V(n,t) dynamic predictions) is conditional on a derivation gate that is currently OPEN — Tier B is listed as future, not as a co-equal claim.

**Internal grading (informational, not a journal claim):** ★★★★★ − 0.08 at L341 audit close. Pillars: clarity ★★★★★ / derivation chain ★★★★ / self-consistency ★★★★★ / quantitative predictions ★★★★★ / observational match ★★★½ / parameter parsimony ★★ / micro theory ★★★½ / falsifiability ★★★★★.

## 3. The novel content of v2 — P17 pre-registration

The single feature that distinguishes this submission from any earlier SQMH circulation is **P17 pre-registration**: eight quantitative predictions, with locked datasets, locked thresholds, locked decision rules, and locked sign conventions. Appendix A is a one-page card per falsifier:

- **F1.** Cosmic-regime σ_0 from BAO+SN+CMB+RSD compressed-likelihood joint, threshold and decision-rule locked, dataset = DESI DR3 BAO + DES-Y5 SN + Planck PR4 compressed CMB + DESI DR2 RSD (post-release).
- **F2.** Cluster-regime σ_0 from PSZ2-vs-lensing joint (L350 framework), with hydrostatic-mass-bias (1−b) marginalised.
- **F3.** Galactic-regime σ_0 from SPARC + DiskMass joint with ϒ-disk marginalised.
- **F4–F6.** Cross-regime consistency tests (cosmic ↔ cluster, cluster ↔ galactic, three-way) with locked χ² and locked AICc thresholds.
- **F7.** RG-fixed-point flow signature (post-hoc parameters but pre-registered observable).
- **F8.** SymG cell signature (with the L339 false-positive rate disclosed).

For each falsifier, a fail outcome is defined in advance and fail outcomes are honoured — no post-hoc threshold relaxation. This is the central commitment of v2.

## 4. Recovery rounds (L342–L368) — honest accounting

Following the L322–L341 audit, we ran 27 recovery loops (L342–L368) targeting the nine limitations above. Disk inspection of these rounds shows:

- 21 of 27 produced ≥ 2 of {ATTACK_DESIGN, NEXT_STEP, REVIEW};
- 2 of 27 (L346, L363) produced a single artefact only (incomplete);
- 1 of 27 (L364) is empty (not executed);
- selected runs (L350 PSZ2-vs-lensing, L342 production output, L353/L354/L358–L360 design) advanced the state of the corresponding limitation.

We disclose this distribution rather than claiming uniform completion. The substantive recovery products (L350 framework, L338 P17 two-tier pre-registration, L340 BMA proper, L333 sloppy-dim reparameterisation, L335 13-cluster pool) are integrated into the manuscript; the incomplete loops are flagged in the limitations table and are not claimed as supporting evidence.

## 5. Anticipated reviewer objections — pre-empted

- **R1 (sloppy posterior).** Acknowledged in §2-L1 and reflected by adopting the two-regime baseline; the three-regime split is forecast-tested (P11), not claimed as current evidence.
- **R2 (cluster single-source).** Acknowledged in §2-L4; the L350 selection-bias check is included as a separate channel, and the 13-cluster follow-up is named in P17 F2.
- **R3 (multimodality / dynesty).** A dynesty multimodal pass (ndim = 3) is reported in the supplementary; mode count and lnZ are quoted directly without narrative selection.
- **R4 (BMA framing).** §2-L8 reports BIC, Laplace, and AIC weights jointly; we do not cherry-pick.
- **R5 (microphysics gap).** §2-L6 caps the claim at 80%; Tier B in P17 is gated by the derivation, not co-equal.
- **R6 (3-regime priori).** §2-L2 — two-regime is baseline; three-regime is a forecast.

## 6. Why JCAP

JCAP is the appropriate venue because the manuscript's contribution is a **falsifiable phenomenology with an explicit pre-registration**, not a structural theoretical breakthrough. The eight falsifiers will be decided on near-term data; the manuscript is designed so that any of those decisions can be cited unambiguously.

We thank the editors and referees for their consideration.

---

## Appendix A — P17 Pre-Registration Cards (8 falsifiers)
*[separate one-page card per falsifier; each card fixes: prediction, dataset+release, threshold, decision rule, sign convention, registration date, hash]*

## Appendix B — Known Limitations (mirror of §2)
*[the nine items L1–L9 as a stand-alone reference table for citation]*

## Appendix C — Recovery-round inventory (L342–L368)
*[per-loop status: complete / partial / single-artefact / empty]*

---

*End of cover letter v2.*
