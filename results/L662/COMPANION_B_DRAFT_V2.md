# Companion B — Methodology Paper, Draft v2

**Session**: L662
**Date**: 2026-05-02
**Target venue**: OJA (Open Journal of Astrophysics, primary), JOSS (secondary)
**Status**: draft v2, supersedes L539 COMPANION_DRAFT.md
**Mandatory review**: Rule-A 8-인 sequential review required before submission
**One-line honesty statement**: This paper presents a verification harness and disclosure protocol developed during a single-adopter case study (SQT). It does not claim general adoption, methodological novelty over all existing reproducibility tooling, or that the case-study theory is correct.

---

## §0 Abstract

We present a methodology bundle for cosmology framework reproducibility, refined through a single-adopter case study (the Spacetime Quantum Metabolism / SQT theory). The bundle has three components: (i) a seven-script verification harness (`verify_*.py`) producing JSON expected-output manifests, executed with last-pass status 7/7; (ii) a thirteen-tier claims-status schema (`claims_status.json` v1.3) including hidden degree-of-freedom (hidden-DOF) disclosure rows and an active-limitations register; (iii) an erratum protocol enabling retroactive vocabulary synchronization across versioned drafts. The paper is methodology-only — it introduces no new physics. The case study count is one (SQT); we do not claim broader adoption. We compare the bundle to ASCL, Zenodo, GitHub release pinning, and prereg.org-style preregistration, identifying the harness + schema combination as the contribution. Limitations are disclosed in §8.

---

## §1 Introduction

### 1.1 Reproducibility crisis in cosmology

Cosmology framework papers routinely report best-fit parameters, evidence ratios, and tension reductions without releasing the executable artifacts that produced them. Even when code is released, three failure modes recur: (a) silent dependency drift between draft revision and final acceptance; (b) hidden tunable degrees of freedom not counted in the AICc/BIC penalty; (c) vocabulary inconsistencies between abstract, body, and supplementary tables that survive peer review.

### 1.2 Methodology-only contribution

This paper contributes no new theory and no new data. It contributes only a workflow: a script harness, a status schema, an audit protocol, and an erratum protocol. The SQT case study is illustrative, not validating. Readers seeking the SQT theory itself are referred to the companion theory paper (Companion A).

### 1.3 Case study scope

The case study uses one adopter framework. We label this honestly: count = 1. We do not claim the methodology has been validated across multiple frameworks, and we do not claim the case-study theory has passed independent replication. We invite adoption by other framework authors and treat broader uptake as future work.

---

## §2 Verification harness

### 2.1 Seven-script architecture

The harness consists of seven `verify_*.py` scripts, each targeting a distinct claim category (background fit, growth, CMB compressed likelihood, BAO chi-square, SN distance modulus, joint posterior, evidence). Each script reads pinned input data, runs a deterministic computation, and emits a JSON manifest of expected outputs. Last full pass (L637): 7/7 PASS. The harness is intended as a minimum, not a maximum — adopters may extend it.

### 2.2 expected_outputs JSON convention

Each script writes a single JSON file with a fixed top-level schema: input hashes, code commit hash, library versions, numerical outputs at fixed key names, and a status field. Reviewers re-run the script and diff the JSON; numerical tolerances are declared per-key.

### 2.3 Docker + conda environment

A Docker image and a conda environment specification pin all numerical libraries to specific versions. The image is built from a publicly tagged base. Without environment pinning, the harness is advisory only; with it, byte-level reproducibility on CPU is achievable for the deterministic scripts.

---

## §3 claims_status.json v1.3 schema

### 3.1 Thirteen-tier enum

The schema (L638 plan, building on L557 audit) defines thirteen status values for each claim, ranging through provisional, in-review, partial, and various failure or moderation tiers. The full enum table is given in Appendix A. The intent is to replace the binary "PASS / FAIL" framing common in framework papers with a granular tier that distinguishes statistical from structural status.

### 3.2 PASS_STRONG enum permanently locked at zero

Following the L513 / L515 protocol, the PASS_STRONG tier is reserved and currently locked at zero. No claim in the case study qualifies. The tier remains in the schema as an aspirational ceiling; locking it at zero prevents grade inflation and signals to readers that "the strongest available label was deliberately not used."

### 3.3 Hidden-DOF disclosure rows

Schema rows nine through thirteen are reserved for hidden degree-of-freedom disclosure: one row per detected hidden DOF, with effective-k estimate and corresponding AICc penalty adjustment. See §4 for protocol.

### 3.4 Limitations rows 28-32

Rows 28 through 32 hold the active-limitations register: vocabulary corrections (L582 mass redefinition), provisional-status revocations (L549 / L552 / L562 / L566), and self-disclosed fabrication entries (L564). The register is required, not optional.

---

## §4 Hidden-DOF audit protocol

### 4.1 Effective-k estimation method

For each model, the effective number of free parameters k_eff is estimated jointly from (i) explicit fit parameters, (ii) functional-form choices made post-hoc to fit the data, (iii) ansatz selections among multiple candidates evaluated against the same dataset. Methods (ii) and (iii) are typically uncounted in standard AICc reporting; the audit protocol counts them.

### 4.2 ΔAICc penalty calculation

Once k_eff exceeds nominal k, the AICc penalty is recomputed and the model's relative ranking is updated. Models whose ranking flips under k_eff accounting are flagged for moderation.

### 4.3 Case study: SQT k_eff disclosed range

The SQT case study disclosed an effective-k range spanning low- and high-end estimates depending on which hidden choices are counted. Both ends are reported; no single point estimate is privileged. The disclosure was a precondition for any quantitative claim survival.

---

## §5 Active limitations protocol

### 5.1 Deliberately expanded limitations section

Standard practice is to compress limitations to a paragraph. The protocol inverts this: limitations are expanded, individually numbered, and cross-linked to the claims they constrain. The L591 active-limitations protocol formalizes this expansion.

### 5.2 Voluntary fabrication disclosure

Following L564, any prior fabricated or synthetically generated number that influenced an earlier draft is disclosed in a dedicated entry, with the corrected number and the impact on downstream conclusions. The disclosure is voluntary and retroactive; concealment is treated as a protocol violation.

### 5.3 Skeptical 0/4 disclosures

Where adversarial review (L578 / L587 / L588 / L589) produced zero of four "win" verdicts on a given claim, the 0/4 outcome is reported in-line, not buried in supplementary material. The convention is that adversarial null results are content, not noise.

---

## §6 Erratum protocol

### 6.1 Retroactive synchronization directory

A dedicated `erratum/` directory (L635) holds version-pinned diffs for vocabulary and numerical corrections that arrive after a draft has been circulated. Each erratum entry pairs the offending phrase with its replacement and the session in which the correction originated.

### 6.2 23-entry vocabulary correction matrix

The case study currently carries a 23-entry vocabulary correction matrix. Examples include over-strong adjectives downgraded to neutral, mis-attributed methods reattributed, and target-venue claims softened where the underlying support did not justify the original wording.

### 6.3 PRD Letter target → internal OR-gate

The original PRD Letter target was downgraded to an internal OR-gate condition: the framework targets PRD Letter only if either Q17 is fully achieved or Q13 and Q14 are simultaneously achieved. Neither precondition currently holds. The erratum matrix records the downgrade.

---

## §7 Comparison to existing tools

### 7.1 ASCL, Zenodo, GitHub release pinning

ASCL (Astrophysics Source Code Library) provides discoverability; Zenodo provides DOI-pinned snapshots; GitHub release tags provide commit-level pinning. None of these supply (a) a running verification harness, (b) a structured tiered-status schema, or (c) a hidden-DOF audit protocol. The methodology bundle is complementary, not competitive.

### 7.2 prereg.org-style preregistration

Preregistration platforms in cosmology remain rare. The claims-status schema overlaps with preregistration in spirit (committing to claims before final analysis) but differs in scope: the schema is post-hoc graded, not pre-committed, and it accommodates revocation tiers natively.

---

## §8 Limitations

### 8.1 Adopter count = 1

The methodology has been exercised by a single framework (SQT). N=1 is not a generalization base. We do not claim portability has been demonstrated; we claim it has been designed for.

### 8.2 Schema novelty bounded

The thirteen-tier enum, hidden-DOF rows, and erratum protocol are organizational, not algorithmic. There is no Verlinde-style structural novelty in the schema. Reviewers who require methodological novelty at the algorithmic level will find this paper insufficient on that axis; the contribution is workflow integration, not a new statistic.

### 8.3 Harness coverage bounded

Seven scripts do not cover every claim category in modern cosmology (e.g., full Boltzmann perturbations, lensing reconstruction, large N-body). The harness is a starting set, expandable.

### 8.4 Provisional CMB tier

The compressed-CMB verification step uses Hu-Sugiyama-style fitting formulae with declared theory-floor tolerance. Full hi_class integration is future work; the current tier is provisional (K19 in case-study notation).

---

## §9 Conclusion

Reproducibility tooling for cosmology framework papers is fragmented across discoverability, snapshot pinning, and ad-hoc supplementary scripts. We have integrated three layers — a seven-script verification harness, a thirteen-tier claims-status schema with hidden-DOF disclosure, and an erratum protocol — and exercised them on a single adopter framework. The methodology generalizes in principle; demonstration of generalization requires additional adopters. We invite framework authors to fork the harness skeleton, adapt the schema, and report back.

---

## Appendix A — schema enum reference (deferred to supplement)

## Appendix B — verify_*.py script index (deferred to supplement)

## Appendix C — erratum matrix snapshot (deferred to supplement)

---

**Mandatory review gate**: This draft v2 must pass Rule-A 8-인 sequential review before any external circulation. Code-side claims (harness behavior, schema validation logic) require Rule-B 4-인 review independently. No claim in this draft may be elevated above its current case-study tier without re-audit.

**One-line honesty statement (repeated)**: This paper presents a verification harness and disclosure protocol developed during a single-adopter case study. Adopter count = 1. Schema novelty is organizational, not algorithmic. PASS_STRONG is locked at zero. No physics claim is made.
