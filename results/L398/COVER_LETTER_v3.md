# Cover Letter v3 — JCAP Submission

**Manuscript**: Spacetime Quantum Metabolism Hypothesis (SQMH) — A Falsifiable, Pre-Registered Phenomenology Across Cosmic, Cluster, and Galactic Regimes

**Target journal**: JCAP (Journal of Cosmology and Astroparticle Physics)
**Positioning**: Honest falsifiable phenomenology. We do not claim PRD-Letter-level structural breakthroughs.
**Date**: 2026-05-01
**Internal cumulative loop count**: ~318 independent audit/recovery/execution rounds (L77–L391).
**Versioning**: v3 supersedes v2 (L369). v3 incorporates the L346 prediction-vs-fit audit on the non-monotonic σ_0(z) pattern and the L370–L391 execution-focused rounds.

---

## 1. What this submission is — and what it is not

This paper presents a phenomenological framework (SQMH) that predicts a regime-dependent metabolic-coupling parameter σ_0 across three regimes (cosmic, cluster, galactic). The predictions are tied to a single underlying axiom set; the eight pre-registered falsifiers in Appendix A make every quantitative claim refutable on near-term data (DESI DR3, Euclid Q1, LSST Y1, KiDS+, PSZ2 cross-checks).

We submit this as **honest falsifiable phenomenology**. We do **not** claim:

- a structural resolution of the S₈ tension (μ_eff ≈ 1 in the background-only sector; ΔS₈ < 0.01% in our analysis),
- a Bayesian preference over ΛCDM beyond Occam-uncorrected fixed-θ evidence,
- that an "extra parameter is preferred by data" (the Occam-corrected Δln Z is consistent with parameter agnosticism),
- that SQMH and the independent Maggiore-Mancarella RR non-local model (C28 in our internal taxonomy) are theoretically equivalent — the phenomenological alignment we document is not a derivation,
- **(new in v3)** that the non-monotonic σ_0(z) shape is an a priori prediction of the four SQT pillars; per the L346 audit, the non-monotonicity was first identified in fits (L67/L68) and is consistent with — but not forced by — the pillar set.

## 2. Honest disclosure (the core of v2 + v3)

Compared with v1 (L321 internal), v2 (L369) explicitly disclosed every limitation surfaced in audit rounds L322–L341. v3 adds one further item from L346 and updates the recovery-round inventory through L391.

**L1. Effective dimensionality is ≈ 1 (sloppy posterior).** Multi-start Hessian + MBAM analysis on the BB σ_0 posterior (cosmic, cluster, galactic) shows the posterior is cluster-dominant with a stiff direction v_max ≈ 0.81–0.98. The three-σ_0 parameterisation is over-specified relative to the information content of current data.

**L2. Three-regime partition is not data-forced.** A two-regime (cosmic+cluster merged) baseline yields ΔAICc in the range −7 to −67 in forecasts; the three-regime split is justified narratively, not by current AICc. We adopt the two-regime model as baseline and treat the three-regime case as a forecast-tested extension (P11 NS forecast).

**L3. Pillar 4 (parameter parsimony) is downgraded.** RG fixed-point parameters (b, c) cannot be derived a priori from the SQMH axiom set as currently formulated; they are post-hoc fits. We rate pillar 4 at ★★ (down from ★★★).

**L4. Cluster constraint relies on a single source (A1689) at present.** A 13-cluster pool (LoCuSS / CLASH / PSZ2 archive) has been identified for follow-up; numerical results in this paper use A1689 only. The L350 PSZ2-vs-lensing selection-bias analysis is included as a separate companion check, not as a calibration.

**L5. Subset-Bayes 5-dataset MCMC is incomplete.** A 24–30-hour MCMC over five datasets with ϒ marginalisation (d = 181 → 6) is designed and pre-registered (F1–F4 gates) but not executed in this submission.

**L6. Microphysical theory is at an 80% completeness ceiling.** Four of five gap-closures are partial; the a4 emergent-metric channel remains OPEN. We do not claim a complete derivation from L0/L1.

**L7. SymG mock false-positive rate is in the 30–80% range** (preliminary). The cross-validation completion is deferred.

**L8. BMA model weights are robust but Occam-sensitive.** Under proper Bayesian model averaging the BB family receives BIC weight ≈ 92.6%, Laplace ≈ 81%, AIC ≈ 59% — robust to model framing but the Laplace-vs-fixed-θ gap is non-trivial; we flag it.

**L9. P17 pre-registration is two-tier.** Tier A (Λ-static predictions) is locked and is the basis of the eight falsifiers in Appendix A. Tier B (V(n,t) dynamic predictions) is conditional on a derivation gate that is currently OPEN — Tier B is listed as future, not as a co-equal claim.

**L10 (new in v3 — L346 prediction-vs-fit audit). The non-monotonic σ_0(z) pattern is fit-driven, not a pillar-derived prediction.** A historical trace of our internal audit (L67 first reports the non-monotonic pattern as a fit result; L68 attributes the residual to physical non-monotonicity; pillar-mechanism searches follow only afterwards) shows the pattern was first identified in data and subsequently retro-rationalised. Per the L346 axis-by-axis assessment, none of the four SQT pillars (RG saddle, holographic, Z₂, a4 / scaling – the last OPEN) *forces* a sign change of σ_0(z), and the position of the extremum z_* ≈ O(0.5) is not derivable a priori from any pillar. The Bayesian theory-prior P(non-monotonic | 4 pillars) is therefore weak. We acknowledge this in v3 by (i) restating the non-monotonic σ_0(z) shape as "consistent with — not forced by — the pillar set", (ii) restricting Tier-A pre-registration to amplitude and extremum-position *estimates* (see §3), and (iii) listing L346's headline finding under §5 R0.

**Internal grading (informational, not a journal claim):** ★★★★★ − 0.085 at L391 audit close (v2 quoted −0.08 at L341; v3 applies a conservative Δ = −0.005 reflecting the L346 caveat without double-counting pillar 4, which was already downgraded under L3). Pillars: clarity ★★★★★ / derivation chain ★★★★ / self-consistency ★★★★★ / quantitative predictions ★★★★★ / observational match ★★★½ / parameter parsimony ★★ / micro theory ★★★½ / falsifiability ★★★★★.

## 3. The novel content — P17 pre-registration (clarified in v3)

The single feature that distinguishes this submission from any earlier SQMH circulation is **P17 pre-registration**: eight quantitative predictions, with locked datasets, locked thresholds, locked decision rules, and locked sign conventions. Appendix A is a one-page card per falsifier:

- **F1.** Cosmic-regime σ_0 from BAO+SN+CMB+RSD compressed-likelihood joint, threshold and decision-rule locked, dataset = DESI DR3 BAO + DES-Y5 SN + Planck PR4 compressed CMB + DESI DR2 RSD (post-release).
- **F2.** Cluster-regime σ_0 from PSZ2-vs-lensing joint (L350 framework), with hydrostatic-mass-bias (1−b) marginalised.
- **F3.** Galactic-regime σ_0 from SPARC + DiskMass joint with ϒ-disk marginalised.
- **F4–F6.** Cross-regime consistency tests (cosmic ↔ cluster, cluster ↔ galactic, three-way) with locked χ² and locked AICc thresholds.
- **F7.** RG-fixed-point flow signature (post-hoc parameters but pre-registered observable).
- **F8.** SymG cell signature (with the L339 false-positive rate disclosed).

**Scope of Tier A (clarified in v3, per L346).** The Tier-A cards lock *amplitudes* and *extremum-position estimates* of σ_0(z), not the qualitative non-monotonic *shape itself*. Locking the shape would require Tier B (V(n,t) full derivation), whose derivation gate remains OPEN. Until Tier B is closed, the non-monotonicity of σ_0(z) is a phenomenological observation in our data, not a pre-registered prediction — and therefore is not claimed as such anywhere in this manuscript.

For each falsifier, a fail outcome is defined in advance and fail outcomes are honoured — no post-hoc threshold relaxation. This is the central commitment of v3.

## 4. Recovery and execution rounds (L342–L391) — honest accounting

Following the L322–L341 audit, we ran approximately fifty internal rounds (L342–L391) targeting the limitations above. These split into two categories:

- **Design rounds (audit / recovery)**: produce ATTACK_DESIGN, REVIEW, NEXT_STEP triplets.
- **Execution-focused rounds (simulation / MCMC / data validation)**: produce computational artefacts rather than design triplets.

Disk inspection of the L342–L391 range gives:

- ~21 of ~50 rounds produced ≥ 2 of {ATTACK_DESIGN, NEXT_STEP, REVIEW};
- ~22 of ~50 rounds produced a single artefact only or are execution-focused (single-output by design);
- ~6 of ~50 rounds (e.g. L364, L376 absent, L390, L392, L393, L396) are empty or unrun;
- selected runs (L350 PSZ2-vs-lensing framework; L342 production output; L353/L354/L358–L360 design; L346 prediction-vs-fit audit) advanced the state of the corresponding limitation.

We disclose this distribution rather than claiming uniform completion. The substantive recovery products (L350 framework, L338 P17 two-tier pre-registration, L340 BMA proper, L333 sloppy-dim reparameterisation, L335 13-cluster pool, **L346 prediction-vs-fit audit**) are integrated into the manuscript or this cover letter; incomplete and empty rounds are flagged in Appendix C and are not claimed as supporting evidence.

## 5. Anticipated reviewer objections — pre-empted

- **R0 (new in v3 — prediction vs fit).** Acknowledged in §2-L10 and §3. The non-monotonic σ_0(z) pattern was first surfaced in fits (L67/L68) and is consistent with — but not forced by — the four-pillar set; we do not claim it as an a priori prediction. Tier-A pre-registration locks amplitude and extremum-position *estimates*, not the qualitative shape; the qualitative shape would require Tier-B derivation, currently OPEN.
- **R1 (sloppy posterior).** Acknowledged in §2-L1 and reflected by adopting the two-regime baseline; the three-regime split is forecast-tested (P11), not claimed as current evidence.
- **R2 (cluster single-source).** Acknowledged in §2-L4; the L350 selection-bias check is included as a separate channel, and the 13-cluster follow-up is named in P17 F2.
- **R3 (multimodality / dynesty).** A dynesty multimodal pass (ndim = 3) is reported in the supplementary; mode count and lnZ are quoted directly without narrative selection.
- **R4 (BMA framing).** §2-L8 reports BIC, Laplace, and AIC weights jointly; we do not cherry-pick.
- **R5 (microphysics gap).** §2-L6 caps the claim at 80%; Tier B in P17 is gated by the derivation, not co-equal.
- **R6 (3-regime priori).** §2-L2 — two-regime is baseline; three-regime is a forecast.

## 6. Why JCAP

JCAP is the appropriate venue because the manuscript's contribution is a **falsifiable phenomenology with an explicit pre-registration**, not a structural theoretical breakthrough. The eight falsifiers will be decided on near-term data; the manuscript is designed so that any of those decisions can be cited unambiguously. v3 reinforces this positioning by formally distinguishing fit-derived observations (the non-monotonic σ_0(z) shape) from pre-registered predictions (Tier A amplitudes / extremum-position estimates; Tier B gated).

We thank the editors and referees for their consideration.

---

## Appendix A — P17 Pre-Registration Cards (8 falsifiers)
*[separate one-page card per falsifier; each card fixes: prediction, dataset+release, threshold, decision rule, sign convention, registration date, hash. Tier A cards lock amplitude / extremum-position estimates; qualitative shape is not locked at Tier A — see §3.]*

## Appendix B — Known Limitations (mirror of §2)
*[the ten items L1–L10 as a stand-alone reference table for citation. L10 added in v3 from the L346 audit.]*

## Appendix C — Recovery / execution-round inventory (L342–L391)
*[per-loop status: complete / partial / single-artefact / execution-focused / empty. Empty rounds explicitly listed, not concealed.]*

---

## v2 → v3 changelog

1. §1 disclaimers — added the L346-derived non-monotonicity caveat as a fifth bullet.
2. §2 — added L10 (L346 prediction-vs-fit audit). Internal grade −0.08 → −0.085 (conservative; no double-counting of pillar 4).
3. §3 — clarified that Tier-A cards lock amplitude and extremum-position *estimates*, not the qualitative shape.
4. §4 — recovery inventory extended from L342–L368 (~27 loops) to L342–L391 (~50 loops); execution-focused rounds split out; empty rounds enumerated.
5. §5 — R0 (prediction vs fit) added as the leading anticipated objection.

No structural claim has been strengthened. No grade has been raised.

---

*End of cover letter v3.*
