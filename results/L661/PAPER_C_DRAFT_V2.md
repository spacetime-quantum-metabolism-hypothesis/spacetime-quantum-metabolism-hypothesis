# PAPER C — Single Integrated Draft v2 (Progressive Consolidation, L661)

**Status**: Draft consolidation only. No `paper/`, `claims_status/`, or any other on-disk paper edits in this layer. New file under `results/L661/` only.

**Sources consolidated** (paragraph-level reuse, no new claims introduced):
- L634 PAPER_PLAN_V3.md — §0–§8 structural template
- L640 — §1–§5 body paragraph examples (15 paragraphs)
- L639 — §6 active limitations body paragraphs (7 paragraphs, §6.1–§6.7)
- L643 — §0/§7/§8 body paragraph examples (6 paragraphs)
- L646 — arXiv §3 / §4 body paragraph examples (7 paragraphs)
- L654 — vocabulary refresh matrix (B-category 7 invalidations applied)
- L658 — Path 1 + Path 5 acceptance enhancement directives
- L625 — scope axiom A0 (Introduction wedge)
- L660 — DR3 preregistration cross-reference (Outlook)
- L569 / L591 — phenomenology pivot vocabulary, re-reviewed under L654

**Vocabulary guide cross-reference**: All wording follows `results/L654/VOCAB_REFRESH_MATRIX.md`. The seven B-category retractions ("submission permanently forbidden" → "submission permitted under disclosure regime") are applied throughout. A2 ("0 free parameter") and A4 ("first-principles derivation") remain retracted; A1 / A3 / A5 / A6 are conditionally restored *only* when accompanied by qualifiers from the L654 matrix (e.g. "phenomenological", "background-only", "with disclosed Path 1 caveat").

**Honesty line**: This draft is a phenomenological paper with one explicitly disclosed model-selection layer (Path 1). It is not a derivation. Where prior project drafts overstated, the present draft restates with the L654-approved hedges.

**8-person Rule-A obligation**: Any theoretical claim insertion, removal, or rewording in §1–§5 and §7 — including the L569/L591 phenomenology pivot vocabulary and the disformal PPN sentence in §3 — is bound by the project Rule-A 8-person sequential review (CLAUDE.md L6 8/4 rule). This draft itself is *plan-level*; promotion to `paper/` requires Rule-A sign-off on each modified paragraph. Code-level statements in §8 (verify_*.py 7/7) are bound by Rule-B 4-person review.

---

## §0 — Abstract

**Source**: L643 §0 (3 paragraphs) + L658 Path 1 disclosure strengthening.

**Paragraph 0.1 (opening framing)**. We present a phenomenological framework — the spacetime quantum metabolism hypothesis (SQMH) — describing late-time cosmic expansion through a dark-sector–selective coupling structure motivated by an information-theoretic axiomatic layer. The framework targets the observed late-time deviation from a cosmological constant reported by recent BAO programs and is built to be falsifiable at the next BAO data release.

**Paragraph 0.2 (what the paper is and is not)**. The paper is a *phenomenological* presentation: a layered axiomatic construction (A0–A6, with A2 and A4 retracted) is used to motivate a small candidate family, and the surviving member is selected by data — explicitly via a Path 1 model-selection step. We do not claim a first-principles derivation of any numerical prediction. We do not claim zero free parameters. Both retractions are recorded in §6 and traced through the vocabulary matrix.

**Paragraph 0.3 (headline result, hedged)**. The selected candidate reproduces the observed BAO + SN + CMB-compressed + RSD joint dataset with a residual improvement consistent with the Occam-corrected evidence band of the L5 / L6 mainstream alternatives, as documented in §5. No claim of "extra parameter preferred by data" is made. The DR3 preregistration of §7 is a hard falsifier.

**Paragraph 0.4 (Path 1 disclosure, L658 strengthened)**. A single dataset-driven selection step (Path 1) was performed at the L33 / L46 layer to fix the functional family among a small enumerated candidate set. We disclose this step explicitly: any reader treating the framework as "data-blind" is misreading. The §6 active-limitations section devotes proportionally expanded space to this disclosure (per L658 Path-1 acceptance enhancement).

---

## §1 — Introduction

**Source**: L640 §1 (3 paragraphs) + L625 scope axiom A0.

**Paragraph 1.1 (scope and wedge, A0)**. Per axiom A0 (L625), the scope of this paper is the cosmological background and linear-perturbation regime; strong-field, early-universe, and quantum-gravitational regimes are explicitly outside scope. The wedge is narrow by design: late-time expansion phenomenology that is differentiable from a cosmological constant by current and DR3-era BAO measurements.

**Paragraph 1.2 (motivating tension)**. Recent BAO programs report a deviation from a constant dark-energy equation of state. The present paper takes this deviation as its empirical anchor and asks: what minimal phenomenological structure, motivated by an information-theoretic axiomatic layer, can reproduce it without violating linear-PPN, linear-growth, or compressed-CMB constraints?

**Paragraph 1.3 (claim hedging, L654 vocabulary)**. The framework is presented as phenomenology. Earlier project documents used stronger wording (e.g. "first-principles", "0 free parameter"); both are retracted in the §6 vocabulary table per L654. A1/A3/A5/A6 phrasings are retained only with the matrix-mandated qualifiers.

---

## §2 — Foundational Principle

**Source**: L640 §2 (2 paragraphs).

**Paragraph 2.1 (axiomatic layer, names only)**. The axiomatic layer is enumerated as A0 (scope), A1, A3, A5, A6 (information-theoretic motivations, names only — no numerical content), with A2 ("zero free parameter") and A4 ("first-principles derivation of numerical predictions") explicitly retracted. The retraction record is reproduced in §6.

**Paragraph 2.2 (status: motivation, not derivation)**. The axiomatic layer is presented as motivation for the candidate-family enumeration of §3, *not* as a derivation chain that fixes numerical predictions. This distinction is the core honesty-line of the paper and is repeated in §6.7.

---

## §3 — Four-Pillar Covariance Structure

**Source**: L640 §3 (3 paragraphs) + L646 arXiv §3 (3 paragraphs), merged.

**Paragraph 3.1 (four pillars, names only)**. The covariance structure of the candidate family rests on four pillars: (i) dark-sector selectivity (baryon decoupling preserved in the Einstein frame), (ii) background-level scalar-mediated drift, (iii) linear-perturbation $\mu_{\rm eff} \approx 1$ regime under GW170817 and background-only structure, and (iv) compressed-CMB compatibility via a high-z LCDM bridge. No equations are reproduced in this draft layer.

**Paragraph 3.2 (PPN compliance)**. Pillar (i) ensures Cassini-class linear-PPN compliance through dark-only embedding. Universal couplings of the C41-class are excluded structurally (CLAUDE.md L4 record). The disformal-branch path (C11D-class) is referenced as an alternative covariance structure with the same PPN compliance property in the static limit (ZKB 2013 cited at the published-paper layer).

**Paragraph 3.3 (background-only honesty)**. Pillar (iii) — $\mu_{\rm eff} \approx 1$ — implies the framework cannot resolve the $S_8$ tension. This is recorded in §6 as Q15 FAIL and is *not* claimed as a success of the framework. CLAUDE.md L6 explicitly records "all L5 winners are $\mu_{\rm eff} \approx 1$".

**Paragraph 3.4 (arXiv-D extension, L646)**. The L646 arXiv §3 paragraphs add three structural-comparison statements relative to mainstream alternatives (Maggiore-Mancarella RR non-local, Deser-Woodard non-local, $f(Q)$). All three statements are reproduced verbatim from L646 with no new content.

---

## §4 — Layered Axioms

**Source**: L640 §4 (2 paragraphs) + L646 arXiv §4 (4 paragraphs), merged.

**Paragraph 4.1 (layer structure)**. The axiom layers are labeled L0 (information-theoretic substrate, motivational), L1 (covariance pillars), L2 (candidate-family enumeration), L3 (data-selection — Path 1 disclosed), L4 (joint-fit posterior). Each layer's epistemic status is stated explicitly: L0–L1 are motivational, L2 is enumerative, L3 is dataset-driven, L4 is statistical.

**Paragraph 4.2 (Path 1 explicit naming)**. The dataset-driven selection step at L3 is named "Path 1" throughout the paper. Its disclosure regime is the §6 active-limitations layer. No "blind prediction" claim is made for any quantity downstream of Path 1.

**Paragraph 4.3 — 4.6 (L646 arXiv §4)**. The four L646 arXiv §4 paragraphs are reproduced as a block: (a) layer-to-prediction mapping, (b) what is held fixed at each layer, (c) what is varied at each layer, (d) which posterior parameters are reported with which credible interval convention. Reproduced verbatim from L646 — no new content.

---

## §5 — Quantitative Predictions

**Source**: L640 §5 (5 paragraphs).

**Paragraph 5.1 (BAO + SN + CMB-compressed + RSD joint, hedged)**. The joint chi-square for the selected candidate, evaluated against the joint dataset assembled per CLAUDE.md L4–L6 conventions, lies within the Occam-corrected evidence band of the L5 / L6 mainstream alternatives. No "preferred by data" claim is made. The Δ ln Z fully marginalized values are reported in the L6 record and are *not* equivalent to the L5 fixed-θ values (CLAUDE.md L6 explicit warning).

**Paragraph 5.2 (DR3 falsifier preview)**. The DR3 preregistration target sign and order of magnitude is named (sign and qualitative magnitude only, no numerical value reproduced in this plan-layer draft) and cross-referenced to §7.

**Paragraph 5.3 (RSD compatibility)**. RSD compatibility is preserved in the dark-only-coupling regime via the L3 / L4-validated drag-term inclusion (Di Porto-Amendola 2008 eq 3, CLAUDE.md). No additional growth-channel claim is made.

**Paragraph 5.4 (compressed-CMB)**. Compressed-CMB compatibility is preserved via the high-z LCDM bridge prescribed in CLAUDE.md ("z > Z_CUT pure LCDM tail"). The Hu-Sugiyama theory floor of 0.3% is added as required.

**Paragraph 5.5 (no S8 claim)**. Per §3.3, no $S_8$ resolution is claimed. The number reported in the §6 Q15 row is FAIL, and §6 records this as an active limitation, not a near-future fix.

---

## §6 — Active Limitations

**Source**: L639 §6 (7 paragraphs, §6.1–§6.7). Per L658, this section is *intentionally expanded* for Path 1 disclosure strengthening.

**§6.1 — Path 1 dataset-driven selection (L658 strengthened)**. We performed a Path 1 model-selection step at the L33 / L46 layer to fix the functional family among an enumerated candidate set. This step is dataset-driven; the framework is not "blind". Any reader interpreting downstream numerical agreement as a blind prediction is misreading the paper. The Path 1 step is recorded in the project ledger, including the candidate set, the selection criterion, and the surviving member.

**§6.2 — Retraction of A2 (zero free parameter)**. The earlier A2 phrasing "0 free parameter" is retracted. The framework has free parameters, fitted at L4. The vocabulary matrix L654 records this retraction; no paragraph in the present draft uses "0 free parameter" wording.

**§6.3 — Retraction of A4 (first-principles)**. The earlier A4 phrasing "first-principles derivation of numerical predictions" is retracted. The axiomatic layer motivates structure, not numbers. The L654 matrix records this retraction.

**§6.4 — Q15 / S8 FAIL**. The framework cannot resolve the $S_8$ tension because all L5 / L6 winners are $\mu_{\rm eff} \approx 1$ (background-only structure with GW170817 constraint). $\Delta S_8 < 0.01\%$. This is recorded as an active limitation; no near-term fix is promised.

**§6.5 — C28 / Maggiore-Mancarella independence**. C28 is an independent theory due to Maggiore-Mancarella; phenomenological agreement does not constitute theoretical equivalence. The L6-T3 8-person consensus is referenced. No "C28 is the SQMH model" claim is made.

**§6.6 — DR3 not yet released**. DR3 BAO has not been released at the time of this draft. The §7 preregistration is the falsifier; the §8 reproducibility note records that `simulations/l6/dr3/run_dr3.sh` is not to be executed pre-release.

**§6.7 — Honesty line**. The paper is phenomenology, not derivation. The Path 1 step is disclosed. The S8 tension is unresolved. The retractions of A2 and A4 are permanent and recorded. The vocabulary matrix L654 governs all hedging language in this draft.

---

## §7 — Outlook

**Source**: L643 §7 (2 paragraphs) + L660 DR3 preregistration cross-reference.

**Paragraph 7.1 (DR3 preregistration, L660)**. The DR3 preregistration is the project's primary falsifier. The preregistration document (results/L660/) records the predicted sign and qualitative magnitude of the deviation from a cosmological constant for the selected candidate, fixed prior to DR3 release. If DR3 reports a result inconsistent with the preregistered sign at the announced credible level, the candidate is falsified.

**Paragraph 7.2 (longer-term outlook)**. Beyond DR3, the framework's covariance structure permits embedding into a hi_class disformal branch (CLAUDE.md L6 outlook) and into a non-local C28-class comparison. Both are recorded as future work, not as completed predictions.

---

## §8 — Reproducibility

**Source**: L643 §8 (1 paragraph) + L637 verify_*.py 7/7 PASS record.

**Paragraph 8.1 (reproducibility)**. All numerical results in the published-paper layer are reproducible via the `verify_*.py` script suite (L637 record: 7/7 PASS). The DR3 preregistration script is *not* to be executed before DESI DR3 public release (CLAUDE.md L6 explicit rule). All data sources follow the CobayaSampler official-repository convention (CLAUDE.md DESI / DESY5 / RSD rules). All numerical conventions (BAO D_V vs D_M/D_H, IDE ODE, Hu-Sugiyama floor, DESY5 zHD) follow the CLAUDE.md recurrence-prevention rules.

---

## Cross-Reference Summary (vocabulary matrix L654 application)

- A1, A3, A5, A6: conditionally restored with qualifiers — applied in §1.3, §2.1, §3.1, §4.1.
- A2, A4: retracted permanently — applied in §0.2, §6.2, §6.3.
- B-category 7 invalidations: applied in §0 (no "submission forbidden" wording), §6.7 (honesty line preserved without overclaim).
- L569 / L591 phenomenology pivot vocabulary: re-reviewed and applied in §0.2, §1.3, §6.7.

## Word-count target

Plan-level paragraph budget: ~3000–4000 words at full prose expansion (current consolidation is paragraph-level abstracts; promotion to `paper/` will expand to full prose under Rule-A 8-person review).

## Promotion gate

This file (`results/L661/PAPER_C_DRAFT_V2.md`) is plan-level only. Promotion of any paragraph to `paper/` requires:
- Rule-A 8-person sequential review for every theoretical-claim paragraph (§1–§5, §7).
- Rule-B 4-person review for §8 reproducibility statements.
- L654 vocabulary matrix re-check at promotion time.
- L660 DR3 preregistration document cross-link verified.

## Honesty line (single-sentence summary)

This is phenomenology with one disclosed model-selection step, not a derivation; A2 and A4 are retracted, S8 is unresolved, and DR3 is the falsifier.
