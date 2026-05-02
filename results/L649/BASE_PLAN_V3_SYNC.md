# L649 — paper/base.md ↔ Paper Plan v3 (L634) Sync Audit

**Date**: 2026-05-02
**Auditor**: single-agent (L649 session)
**Scope**: structural sync audit only — zero edits, zero equations, zero parameter values.
**Constraint**: [최우선-1] adherence. This document records mismatches and a recommended sync plan; *all paper-side edits remain blocked* until 8-인 Rule-A pass.

---

## §1 base.md current state — grep results

Source: `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/paper/base.md`
Length: **1605 lines**, last sync anchor reported as L515 (per task framing).

### §1.1 Vocabulary still present in base.md (would conflict with v3 direction)

| Term / phrase | base.md location (sample line) | v3 stance |
|---|---|---|
| `PASS_STRONG` (advertised raw counts) | lines 149, 173–179, 483, 491, 495, 514, 546, 624–625, 740, 848, 887, 891–893, 896, 899–900, 985, 1078, 1099–1101, 1109–1111, 1588 (≥30 occurrences) | v3 §0/§4/§5 use *qualitative tier descriptors* only; no enum-named status in body. **Major drift.** |
| `PASS_TRIVIAL` legacy alias | lines 173, 449, 887, 1111 | v3 forbids enum names in body — legacy alias should not surface in paper text at all. |
| `PASS_BY_INHERITANCE`, `PASS_IDENTITY`, `CONSISTENCY_CHECK`, `POSTDICTION`, `NOT_INHERITED`, `OBS-FAIL`, `FRAMEWORK-FAIL` | lines 449, 483–514, 887, 1099–1111 | Same: v3 keeps these as *internal reviewer tags*, paraphrased for readers. |
| `0 free parameter` (advertised) | line 626 (already flagged "부정확"); line 1076 (drift identified, L515 차단) | v3 §4.3 (hidden DOF 9–13) replaces this slogan; base.md already partially corrected via L515 guard, but the slogan vocabulary itself still cited rather than removed. |
| `통합 이론` / "unified-theory" framing | not located via direct grep (no hit on the literal phrase). L601 unification appears as *conjecture* — partially aligned with v3 §3 stance, but base.md §2.4.1 references `4-pillar convergence PARTIAL` without the v3-style "demanded vs derived" tagging. | Partial alignment; vocabulary upgrade needed in §3. |
| `priori` framing | lines 147, 488, 625–637, 823–837, 874, 988, 1080, 1086, 1097, 1110, 1167, 1187, 1241 | base.md acknowledges priori-path failures piecewise (Path-α / saddle-priori-impossible / σ₀ postdiction), but **does not collect them into a single §6.1 "four atomic-priori deprivation" subsection** as v3 mandates. |

### §1.2 Predecessor LXXX entries that v3 cites — base.md references

| LXXX | v3 role | base.md reference |
|---|---|---|
| L582 (mass-redef closure) | v3 §2 Cross-ref + §6.5 permanent termination | **0 hits** in base.md grep. Major absence. |
| L584 (mass redef permanent termination) | per task framing (재발방지 anchor) | **0 hits**. Absent. |
| L564 (fabrication audit, ~90% disclosure) | v3 §6.2 dedicated subsection | **0 hits**. Absent — base.md has no fabrication-audit subsection. |
| L625 (scope axiom A0) | v3 §1 introduction core | **0 hits**. Absent. |
| L628 (layered axioms A5) | v3 §4 entire section | **0 hits**. Absent. |
| L629 (active limitations expansion) | v3 §6 frame | **0 hits**. Absent. |
| L631 (GR-style A1–A5 rebuild) | v3 §2/§3/§4/§5/§7 backbone | **0 hits**. Absent. |
| L633 (multi-session H2) | v3 §0/§5/§7.2 obligation | **0 hits**. Absent. |
| L634 itself | v3 plan document | n/a (post-base.md). |
| L549 / L552 / L562 / L566 (four atomic-priori paths) | v3 §1 + §6.1 | **0 hits as a collected set**. Individual references not located. |

**Diagnosis**: base.md is anchored at the **L515 / L498 / L502 / L513 horizon** (hidden-DOF audit, falsifier-independence). Everything from **L549 onward (paradigm shift, scope axiom, layered axioms, multi-session)** is **not yet integrated** into base.md.

---

## §2 Sync matrix (8 sections)

Legend: ✅ aligned · ⚠️ partial · ❌ drift / absent

| § | v3 directive (L634) | base.md current state | Status |
|---|---|---|---|
| §0 Abstract | Honesty posture first; status table; trajectory paragraph (L549→L634); qualitative honesty band; multi-session disclosure. | Lines 610–642 (초록) carry self-audit headline + raw 28%/31% counts. Has hidden-DOF 0% headline (good). Lacks: trajectory paragraph, multi-session disclosure (L633), qualitative-band rephrasing (still uses raw enums). | ⚠️ |
| §1 Introduction (A0 scope) | Mpc/galactic envelope declared up front; *atomic / sub-galactic / table-top / EP regimes excluded*; framed as deliberate restriction forced by failed priori paths. | Lines 643–681 (1장 서론, 1.1–1.5). 6대 동기 난제 list, SQT one-line def, prior comparison. **No A0 scope-axiom subsection. No exclusion declaration. No "deliberate domain restriction" framing.** | ❌ |
| §2 Foundational principle (L631 A1) | One paragraph; postulate, not derivation; cross-ref L582 (*not* a mass redefinition). | Lines 683–705 (2.1 6 공리 + 2.2 도출 graph). Treats axioms 1–6 + derived 1–5 directly; lacks the *single foundational-principle* compression that v3 §2 mandates; **no L582 mass-redef cross-ref**. | ❌ |
| §3 Four-pillar covariance (L631 A2 + L601) | Four pillars as *demands*; tag each as demanded vs derived; L601 unification = conjecture, flagged unproven. | Lines 753–793 (2.4 미시 4 축). Has 4-pillar PARTIAL acknowledgment (line 762), but pillars are framed as *microscopic axes*, not as *covariance demands*. Demanded/derived split not present. L601 unification = mentioned but not collected here. | ⚠️ |
| §4 Layered axioms (L628 A5) | Core / derived (B1, a4, a6) / hidden DOF (9–13) — three-tier separation, per-axiom falsifier. | Lines 685–706 mix axioms + derivations without v3's three-tier separation. B1 is present (2.2.1, line 706+) but not labeled "derived axiom" per L628 framing. Hidden DOF 9–13 is acknowledged (lines 626, 1076) but only in audit row, *not as a structural §4.3 subsection*. | ❌ |
| §5 Quantitative predictions (L631 A4) | a₀ (moderate-pass tier), σ₀ dimensional uniqueness (O(1) coefficient = hidden DOF), six-falsifier pre-registration. | a₀ appears at line 657, 901 (RAR PASS_MODERATE with caveats — partially aligned with v3's "moderate-pass tier" framing). σ₀ regime structure at line 891, with postdiction caveat (line 176). 6 pre-registered falsifiers tracked at line 949–967, 1077. **But predictions are not gated through A0 scope envelope, and the "dimensional uniqueness ≠ derivation" disclaimer required by v3 §5.2 is not present in §5 location** (it appears only in §5.2 / footnote-style around line 988, 1167). | ⚠️ |
| §6 Active limitations | (a) four priori-path deprivations (L549/552/562/566), (b) fabrication audit (L564, ~90% retracted), (c) skeptical 0/4 (L578/587/588/589), (d) hidden DOF as limitation, (e) mass-redef permanent closure (L582). | base.md has §6.1 22-row + §6.5(e) self-audit (existing single-source-of-truth). Hidden DOF (d) covered (rows 23, 25). **(a) four-priori-deprivation subsection: absent**. **(b) fabrication-audit (L564) subsection: absent**. **(c) skeptical 0/4 with L578/587/588/589 mapping: absent**. **(e) mass-redef permanent closure (L582/L584): absent**. | ❌ (4 of 5 v3 sub-topics missing) |
| §7 Outlook / external verification | DR3 BCNF protocol; multi-session derivation requirement (L633 H2); paradigm-shift conditional (pre-committed retirement criteria). | Lines 1117–1170 (7장 + Q&A). DR3 timeline present. **Multi-session H2 obligation: absent**. **Paradigm-shift conditional / pre-committed abandonment criteria: absent.** | ❌ |
| §8 Reproducibility | verify_*.py 7/7, single-agent disclosure, honesty close. | base.md has reproducibility scaffolding (Layer C, lines 296–366) and 8장 references. Verifier scripts listed (5 scripts, line 1170). v3 expects 7 verifier scripts — **count drift (5 vs 7) needs reconciliation**. Single-agent disclosure not in §8 location. | ⚠️ |

**Aggregate**: 0 ✅ · 4 ⚠️ · 5 ❌ across 9 rows (§5 split into §5.1/§5.2 collapsed here).

---

## §3 Mismatch identification

### §3.1 Vocabulary drift (status enum still in body)
- 30+ occurrences of `PASS_STRONG` plus full enum vocabulary (`PASS_IDENTITY`, `PASS_BY_INHERITANCE`, `CONSISTENCY_CHECK`, `POSTDICTION`, `NOT_INHERITED`, `OBS-FAIL`, `FRAMEWORK-FAIL`, `PASS_TRIVIAL`) inline in base.md body.
- v3 §0 vocabulary guidance: keep enum as **internal reviewer tag only**, paraphrase for readers.
- **Conflict**: base.md uses enum-named status as the primary reader-facing classification; v3 mandates qualitative-band paraphrase. Heavy rewrite needed in §0, §4.1 PASS table, §6.5(e).

### §3.2 Section structure drift
- base.md sections: 0 (초록), 1 (서론), 2 (공리), 3 (σ₀ regime), 4 (PASS table + DESI), 5 (predictions), 6 (limitations), 7 (outlook), 8 (verification), 9 (Q&A).
- v3 sections: §0 metadata, §1 intro+A0, §2 foundational principle, §3 four-pillar covariance, §4 layered axioms, §5 quantitative predictions, §6 active limitations, §7 external verification trigger, §8 outlook.
- **Reorganization required**: base.md §2 (6 axioms) needs to split into v3 §2 (foundational principle) + §3 (four pillars) + §4 (layered axioms). base.md current §3 (σ₀ regime) and §4 (PASS table) need redistribution into v3 §5 (predictions) and §6 (limitations).

### §3.3 Predecessor LXXX integration absent
- **L582 mass-redef permanent termination**: 0 references. v3 §2 cross-ref + §6.5 dedicated subsection both blocked.
- **L584 mass redef영구 종결**: 0 references.
- **L564 fabrication 90% disclosure**: 0 references — *no fabrication-audit subsection exists in base.md*.
- **L625 / L628 / L629 / L631 / L633 / L634**: 0 references each. Entire post-L549 paradigm-shift integration is missing.

### §3.4 Falsifiable / honesty-posture asymmetry
- base.md *does* carry: hidden-DOF AICc 0% headline (L502/L513/L515), 6-falsifier N_eff=4.44 correction (L498), σ₀ postdiction caveat, saddle-priori-impossible (L407), Λ-origin circularity downgrade (L412).
- base.md does *not* carry: scope axiom A0 (L625), four-atomic-priori-deprivation collected set (L549/552/562/566), fabrication audit (L564), skeptical 0/4 with axis mapping (L578/587/588/589), mass-redef permanent closure (L582/584), layered-axioms 3-tier (L628), multi-session H2 (L633).
- **Asymmetry**: hidden-DOF / falsifier-independence honesty channels are deeply integrated; paradigm-shift / scope-restriction / multi-session honesty channels are not.

### §3.5 Specific verifier-count drift
- base.md (line 1170 / Layer C): 5 verifier scripts.
- v3 §8 reproducibility: 7 verifier scripts (verify_*.py 7/7).
- Reconciliation needed.

### §3.6 base.md *correct* anchors that v3 must preserve
- §6.5(e) 32-claim audit single-source-of-truth (line 1099–1111) — v3 §6 must keep this as the anchor.
- §6.1 22-row + §6.5(e) overlay (line 887, 1078) — preserve.
- Hidden-DOF 0% headline (line 149, 624) — preserve.
- 6-falsifier N_eff=4.44 / 8.87σ ρ-corrected (line 961, 1077) — preserve.
- Λ-origin CONSISTENCY_CHECK downgrade (line 985, 988, 1167) — preserve.

---

## §4 Sync recommendation plan

**Plan only — no edits in this audit. All edits below are blocked behind 8-인 Rule-A.**

### §4.1 Phase A — section-structure rewrite (high-risk)
- A1. Insert new §1 subsection: "Scope axiom A0" — derive language from L625; declare Mpc/galactic envelope, exclude atomic / table-top / EP / sub-galactic regimes; close with "forced by failed priori paths" paragraph.
- A2. Restructure base.md §2 into v3 §2 + §3 + §4:
  - §2 = single foundational-principle paragraph (L631 A1).
  - §3 = four-pillar covariance (L631 A2 + L601 conjecture flag).
  - §4 = layered axioms (L628 A5: core / derived B1+a4+a6 / hidden DOF 9–13).
- A3. Re-anchor §5: gate every prediction through A0 scope tag; preserve a₀ moderate-pass tier; preserve σ₀ postdiction + saddle-priori-impossible caveats; expose six-falsifier pre-registration as a stand-alone §5.3.

### §4.2 Phase B — limitations expansion (§6, L629)
- B1. Add §6.1 "Four atomic-priori-path deprivations" — collect L549 / L552 / L562 / L566 references that are currently absent.
- B2. Add §6.2 "Fabrication audit (L564)" — disclose ~90% retraction rate.
- B3. Add §6.3 "Skeptical-audit 0/4 (L578/587/588/589)" — map four failed pillars to §3 four-pillar covariance.
- B4. Promote hidden DOF 9–13 from audit-row inline to a dedicated §6.4 subsection (cross-ref §4.3).
- B5. Add §6.5 "Mass-redefinition permanent closure (L582 / L584)" — state commitment, not just limitation.
- B6. Preserve existing §6.5(e) single-source-of-truth as the audit-overlay anchor (rename to avoid §6.5 collision with B5; e.g., move to §6.6 or appendix).

### §4.3 Phase C — vocabulary cleanup (status enum)
- C1. In §0/§4.1/§6.5(e), replace enum-named status (`PASS_STRONG`, `PASS_BY_INHERITANCE`, etc.) with qualitative band descriptors. Keep enum strictly in `claims_status.json` and per-row audit-overlay table.
- C2. Remove `PASS_TRIVIAL` legacy alias from all body locations (deprecate as machine-only).
- C3. Replace `0 free parameter` slogan with `9–13 hidden DOF` framing where it still surfaces unguarded.

### §4.4 Phase D — external-verification & outlook
- D1. Add §7.2 "Multi-session derivation requirement (L633 H2)" — single-session theory claims become inadmissible; author role = adjudication/synthesis across independent sessions.
- D2. Add §7.3 "Paradigm-shift conditional" — pre-commit retirement criteria (which falsifier firings cause framework retirement vs patching).
- D3. Reconcile verifier-count: confirm 5 vs 7 mismatch with the actual `paper/verification/` directory contents before editing.

### §4.5 Phase E — appendices / cross-ref matrix
- E1. Update appendix A (audit log cross-reference matrix) to include L549–L634 entries currently absent.
- E2. Confirm `claims_status.json` ↔ §0 ↔ §6.5(e) ↔ TL;DR sync after Phase C vocabulary cleanup (avoid L414 ATTACK A4 cross-ref drift).

### §4.6 Ordering invariant
- v3 mandates §0 ≼ §6 (status table only finalized after §6 limitation list). All Phase A edits must wait for Phase B completion.
- Phase A2 (axiom restructure) and Phase B (limitations) are *coupled* — the layered-axiom hidden DOF subsection (§4.3) and the §6.4 hidden-DOF-as-limitation subsection share content; co-edit.

---

## §5 8-인 Rule-A obligation

Per CLAUDE.md (LXX Command 공통 원칙) + L634 hand-off:

- **Theory-side reviewers (5)**: §2 foundational principle, §3 four pillars, §4 layered axioms, §5.1 a₀, §5.2 σ₀.
- **Honesty-side reviewers (3)**: §0 metadata, §6 limitations, §7 external-verification.
  *(L634 Appendix B assigns this 5+3 split; total 8.)*
- Each reviewer signs against [최우선-1] checklist (zero equations / zero parameter values).
- Reviewers verify no Phase-A/B/C edit reintroduces equations or parameter targets.
- Targeting decision (JCAP default vs PRD Letter conditional on Q17 + Q13/Q14) is a Rule-A output, not a v3-plan output (per L6 재발방지).

**Blocked until 8/8 pass**: every paper-side edit listed in §4 above. Until then, base.md remains unchanged.

This L649 audit is a single-agent output (per [최우선-2] independence requirement, L633 multi-session). It is **not admissible as a sync trigger**; it is a *map* for the 8-인 reviewers, not a decision.

---

## §6 정직 한 줄

> base.md 는 L515 horizon 에 anchored 되어 있고, L549 이후 paradigm-shift / scope-axiom / layered-axiom / multi-session 라인의 7개 LXXX (L582 / L584 / L564 / L625 / L628 / L629 / L631 / L633) 가 **0 references** 로 부재 — sync 율은 *vocabulary 30+ 충돌 + section 구조 5 ❌ / 4 ⚠️ / 0 ✅* 로 측정되며, 본 L649 단일-에이전트 audit 은 8-인 Rule-A 검토 *전까지* paper-side edit 을 일체 트리거하지 않는다.
