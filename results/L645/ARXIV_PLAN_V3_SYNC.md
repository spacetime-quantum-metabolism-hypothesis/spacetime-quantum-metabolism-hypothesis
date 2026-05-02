# L645 — arXiv PREPRINT_DRAFT (L547) ↔ PAPER_PLAN_V3 (L634) Sync Analysis

**Status**: SINGLE-AGENT analysis only — requires Rule-A 8-reviewer pass before any sync edits.
**Date**: 2026-05-02
**Edits performed**: 0 (read-only sync verification, per task spec).
**Hard constraint**: Per CLAUDE.md [최우선-1], this document contains zero equations and zero new parameter values. Section labels and qualitative tier names are reproduced from the source documents only as identifiers, not as derivations.

---

## §1 Two-document read summary

### 1.1 `paper/arXiv_PREPRINT_DRAFT.md` (L547 D-path)

- 214 lines, single-agent draft saved 2026-05-01.
- Format: arXiv-shaped manuscript (Abstract → §1 Intro → §2 Axioms → §3 Derivation → §4 Four-channel evidence → §5 Falsifiers → §6 Hidden-DOF disclosure → §7 Discussion / Limitations / Conclusions → Submission metadata → Reference pointers → Honest one-liner).
- Posture: "transcribed values only — no new fits". Front-loads hidden-DOF AICc 0%-PASS_STRONG headline and Son+2025 cosmology contingency.
- Predictive grade everywhere: **PASS_MODERATE** (four channels: RAR a₀, BBN ΔN_eff, Cassini |γ−1| dark-only, EP |η|).
- Falsifier compression: six pre-registered channels → N_eff ≈ 4.44 (participation-ratio) / ρ-corrected 8.87σ.
- Audit chain referenced: L482, L491–L498, L502, L506, L513, L515, L526 R8, L537, L545.
- Submission metadata pre-filled (astro-ph.CO primary, gr-qc cross-list).

### 1.2 `results/L634/PAPER_PLAN_V3.md`

- 280 lines, single-agent plan dated 2026-05-02 (one day after L547 draft).
- Format: paper *plan* document — direction-only vocabulary guidance per section, zero equations, zero numerical values.
- Section topology: §0 Metadata → §1 Introduction (Scope Axiom A0) → §2 Foundational Principle (A1) → §3 Four-Pillar Covariance (A2 + L601) → §4 Layered Axioms (A5: core / derived / hidden DOF) → §5 Quantitative Predictions (A4) → §6 Active Limitations (expanded) → §7 External Verification Trigger (A5 + H2) → §8 Outlook → Appendices (audit log matrix, Rule-A reviewer assignment, targeting decision).
- Predecessors integrated: L625 (A0 scope), L628 (A5 layered), L629 (limitation expansion), L631 (GR-style rebuild A1–A5), L633 (H2 multi-session).
- Posture: "structural-honesty high / predictive-rigor moderate"; targeting decision deferred to Rule-A; JCAP default, PRD Letter conditional.
- Hidden-DOF count: 9–13 band (counting-convention-dependent).
- Falsifier count: six channels, pre-registered, tied to specific data releases.

---

## §2 Sync matrix (8 sections)

| Section | arXiv draft (L547) | Plan v3 (L634) | Verdict |
|---|---|---|---|
| §0 Abstract / Metadata | "Abstract" block, ~250 words; states PASS_MODERATE × 4, hidden-DOF 0% PASS_STRONG, N_eff 4.44 / 8.87σ, no PRD Letter | "§0 Metadata" — status table + trajectory paragraph + qualitative honesty rating; defers fill until §6 finalized | STRUCTURAL MATCH; vocabulary mismatch (draft uses numbers; plan forbids them in body) |
| §1 Introduction (Scope Axiom A0) | §1.1 "what this preprint is *not*" + Son+2025 contingency + hidden-DOF audit motivation; §1.2 headline a₀; §1.3 MOND/MOG/TeVeS/Verlinde positioning | §1 explicit Scope Axiom A0 framing — domain restriction declared up front; forbids §5 extrapolation beyond A0 | DIRECTIONAL MATCH; draft does not name "A0" or "scope axiom" explicitly. Plan v3 is more disciplined |
| §2 Foundational Principle | §2 "minimal axioms used" — A1/A2/A4/A5 listed; A0/A3/A6 deferred | §2 single foundational principle, postulational, GR-style; §3 (covariance) deferred | MISMATCH: draft uses A1/A2/A4/A5 labels (galactic subset); plan uses L631 A1 single-foundational-principle layer. Label collision risk |
| §3 Four-pillar covariance | Not present as a section. Embedded implicitly in §2 axioms + §4 channel structure | Explicit §3: four pillars (relativistic / gauge-sector / thermodynamic / conservation-ledger), L601 unification *conjecture* tagged unproven, L578/L587/L588/L589 0/4 skeptical-audit axes | STRUCTURAL GAP: covariance angle is *missing* from the arXiv draft. Plan v3 is materially newer |
| §4 Layered axioms | Not present. Hidden-DOF disclosure is in draft §6, but core/derived/hidden separation is implicit, not formalized | Explicit §4.1 core / §4.2 derived (B1, a4, a6) / §4.3 hidden DOF (9–13) | STRUCTURAL GAP: draft conflates layers. Plan v3 enforces L628 separation |
| §5 Quantitative predictions (PASS_MODERATE) | §4.1–§4.4 (RAR a₀, BBN ΔN_eff, Cassini, EP) graded PASS_MODERATE | §5.1 acceleration scale (moderate-pass tier) + §5.2 coupling-scale dimensional uniqueness + §5.3 six-falsifier pre-registration | TIER MATCH (PASS_MODERATE ≈ moderate-pass). Coverage mismatch: draft has 4 channels; plan §5 names only 1 + 1 + 6-falsifier. BBN/Cassini/EP not explicitly slotted in plan §5 |
| §6 Active limitations | §7.3 Limitations (4 bullets: cosmology-conditional, channel-dependent PPN, postdiction risk, hidden DOFs lower-bound); §6 hidden-DOF separately | §6.1–§6.5 expanded: priori-path deprivations (L549/L552/L562/L566), fabrication audit (L564), skeptical 0/4 (L578/L587/L588/L589), hidden DOF as limitation, mass-redefinition closure (L582 permanent) | LARGE GAP: plan v3's §6 is materially expanded — covers L549/L552/L562/L566/L564/L578/L582/L587/L588/L589, none of which the draft surfaces |
| §7 Outlook / DR3 BCNF | §7.4 "Path forward" — DESI DR3 named (F2), Euclid DR1 (F1), 1/(2π) prefactor derivation as future work | §7.1 DR3 2027 Q2 BCNF protocol (pre-register pipeline / blinding / acceptance) + §7.2 multi-session derivation (L633 H2) + §7.3 paradigm-shift conditional + §8 outlook | DIRECTIONAL MATCH on DR3; plan v3 adds BCNF protocol + H2 multi-session + paradigm-shift conditional, none of which are in draft |
| §8 Reproducibility | "Submission metadata" + "Reference pointers" + ancillary files list (verify_milgrom_a0.py, verification_audit/*.json, L491/L495/L498/L502/L506/L513) | Appendix A (audit-log cross-reference matrix), B (Rule-A reviewer assignment), C (targeting decision deferred) | DIRECTIONAL MATCH: both invoke verification scripts and audit-log linkage; plan v3 formalizes reviewer assignment, draft does not |

**Summary**: 3 STRUCTURAL MATCH (§0, §1, §5 tier), 2 DIRECTIONAL MATCH (§7, §8), 3 STRUCTURAL GAPS (§3, §4, §6). Plan v3 is materially newer and more disciplined.

---

## §3 Mismatch identification

### 3.1 Vocabulary drift

- The arXiv draft uses **numerical values verbatim** (1.042 × 10⁻¹⁰ m s⁻², 4.44, 8.87σ, 2.5%, k_hidden=9, etc.) and labels A1/A2/A4/A5/A6 inherited from `paper/base.md` §3.
- Plan v3 forbids numerical values in body (CLAUDE.md [최우선-1]) and relabels axioms via L631 (A1=foundational principle, A2=four-pillar covariance, A4=quantitative predictions, A5=external verification, A0=scope) — which collides with the draft's A1/A2/A4/A5 (axiom-content labels).
- **Drift direction**: plan v3 is the newer governance layer; draft predates it.

### 3.2 Structural gaps in draft

- §3 four-pillar covariance — entirely missing from draft.
- §4 layered axioms (core / derived / hidden DOF) — implicit only; draft does not separate B1, a4, a6 as derived.
- §6 limitations — draft has 4 bullets; plan v3 mandates 5 expanded subsections including L549/L552/L562/L566 priori-path deprivations, L564 fabrication audit, L578/L587/L588/L589 0/4 skeptical, L582 mass-redefinition permanent closure. None of these LXXX entries appear in the draft.

### 3.3 Newer / more honest

- **Plan v3 is newer (2026-05-02 vs draft 2026-05-01) and integrates L549–L633** — a chain of audits that *postdate* the draft's L482–L545 chain.
- **Plan v3 is more honest**: explicitly enumerates priori-path failures (4 paths), fabrication audit (~90% retraction), skeptical 0/4. Draft is honest at the hidden-DOF AICc level but does not surface the priori-path / fabrication / 0/4 history.
- **Draft is more concrete**: contains the actual numbers, falsifier table, ancillary file list, submission metadata. Plan v3 is direction-only.

### 3.4 Sync target

- Plan v3 = governance / structure source of truth.
- Draft = transcription artifact; predates governance update.
- **Direction of sync**: the draft must be re-shaped to match plan v3's §0–§8 topology while preserving its concrete numerical content (which lives outside [최우선-1] because it is *transcribed* from audited LXXX results, not newly derived).

---

## §4 Integration plan (recommendation)

### 4.1 Document roles

- **`results/L634/PAPER_PLAN_V3.md`** = canonical paper plan (governance / structure).
- **`paper/arXiv_PREPRINT_DRAFT.md`** = submission-format conversion of the plan, populated with audited transcribed values.
- These are not redundant: the plan defines *what sections exist and what they may say*; the draft is *one rendering* into arXiv manuscript form.

### 4.2 Sync sequence (post-Rule-A only)

1. Rule-A 8-reviewer pass on plan v3 (precondition — currently DRAFT).
2. Identify sections in draft that need restructuring to match plan v3 topology:
   - Insert §3 four-pillar covariance section (currently absent).
   - Insert §4 layered axioms with explicit core / derived / hidden-DOF separation.
   - Expand §6 limitations to 5 subsections (priori-path, fabrication audit, skeptical 0/4, hidden DOF as limitation, mass-redefinition closure).
   - Insert §7.1 DR3 BCNF protocol and §7.2 multi-session H2 mandate.
3. Reconcile axiom labels (A0 / A1 / A2 / A4 / A5) — choose either L631 governance labels or paper/base.md §3 content labels; do not allow both conventions in one document.
4. Preserve all transcribed numerical values from L482 / L491 / L495 / L498 / L502 / L506 / L513 / L515 — they remain valid because they are audit-log-backed, not newly derived.
5. Cross-check abstract: ensure every §0 claim re-states with falsifier in §5 and limitation in §6 (plan v3 §0 author obligation).

### 4.3 Forbidden during sync

- Introducing any new equation or parameter value not present in the audited LXXX results.
- Promoting any PASS_MODERATE to PASS_STRONG.
- Removing any limitation from the expanded §6 list.
- Single-session theory edits — extensions of foundational principle, four pillars, or layered axioms must satisfy L633 H2 multi-session derivation requirement.

---

## §5 8-person Rule-A obligation

Per CLAUDE.md [최우선-2] and plan v3 Appendix B:

- **Theory-side reviewers** (§2, §3, §4, §5.1, §5.2): verify the layered-axiom separation in the synced draft, verify no derived axiom is silently promoted to core, verify no hidden DOF is silently fixed by a §5 prediction.
- **Honesty-side reviewers** (§0, §6, §7): verify §6 covers all priori-path failures, fabrication audit, 0/4 skeptical, mass-redefinition closure; verify §0 status table is consistent with §6.
- **Falsifier-side reviewers** (§5.3, §7.1, §7.3): verify the six falsifiers are pre-registerable (no open-ended placeholders), verify DR3 BCNF protocol references existing simulations/l6/dr3 scaffolding, verify paradigm-shift conditional pre-commits abandonment criteria.
- **Sync-specific reviewer obligation**: each reviewer signs against the [최우선-1] checklist (zero equations / zero new values introduced) *and* a sync-specific checklist (no audit-log-backed transcribed value silently dropped, no LXXX cross-ref orphaned).
- 8/8 PASS required before any edit to `paper/arXiv_PREPRINT_DRAFT.md`. 7/8 or lower → return to plan-v3-side for revision.
- 4-person Rule-B (code review) is not triggered by this sync because no code is changed; sync is documentation-only.

---

## §6 Honest one-liner

The arXiv draft (L547) and paper plan v3 (L634) share predictive-tier vocabulary (PASS_MODERATE × 4, N_eff ≈ 4.44, DR3 anchor) but diverge structurally — plan v3 mandates four-pillar covariance, layered-axiom separation, and an expanded limitation list (priori-path failures, fabrication audit, 0/4 skeptical, mass-redefinition closure) that the draft does not yet surface; sync must restructure the draft to match plan v3 topology without introducing any new equation or parameter value, and only after Rule-A 8/8 pass on plan v3 itself.

---

*L645 single-agent sync analysis. Edits to `paper/arXiv_PREPRINT_DRAFT.md` and `results/L634/PAPER_PLAN_V3.md`: 0. Per CLAUDE.md [최우선-1] no equations introduced; per [최우선-2] this document does not perform theory derivation, only structural sync verification. Subject to 8-person Rule-A independent review prior to any sync action.*
