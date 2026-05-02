# L316 REVIEW — Section 6 honest-disclosure plan, 4-person verdict

**Loop**: L316 single
**Reviewed artifact**: `ATTACK_DESIGN.md` (Section 6 final architecture)
**Verdict**: **PROCEED to drafting** with three required edits captured below.

---

## Per-reviewer notes

### P (positive / framing)
- 6.1 limitations table is the right structure; magnitudes + direction-of-bias columns are exactly what reviewers want to see.
- 6.2 verbatim mock-injection sentence is strong — *do not weaken in copy-edit*.
- 6.5 explicit JCAP scope statement aligns with L6-T3 consensus.
- **One concern**: the design lists "amplitude-locking exact coefficient does not survive un-anchored". This must be reflected back into Sec 4 *before* Sec 6 is finalised, otherwise Sec 6 contradicts headline. **REQUIRED EDIT 1**.

### N (negative / attack-surface)
- L1 σ_8 row is correctly stated as "+1.14% structural worsening" (L242) and L286 "SQT worse than ΛCDM on S_8" is included. Good.
- L2 H_0 row reads "only ~10%" — this is honest. Reviewer cannot upgrade-attack this.
- 6.3 marginalized vs fixed-θ Δ ln Z disclosure is the single most important pre-emption in the section. **Recommend bolding the 0.8 value in the table caption** so a skim-reader cannot miss it. **REQUIRED EDIT 2**.
- BB false-detection 100% is the biggest external risk. The 6.2 disclosure is correct but I want to see the *un-anchored* Δ ln Z column actually computed and tabulated, not just promised. If we cannot provide the un-anchored number, 6.2 must say so plainly. **REQUIRED EDIT 3**.

### O (opportunity / accept probability)
- JCAP-style honest phenomenology positioning is the realistic ceiling given Q17 partial + Q13/Q14 not-joint. Sec 6.5 anchors this correctly.
- The structure (table → mock caveat → evidence honesty → open issues → scope) reads like a JCAP/PRD-D limitations section, not a Letter. Appropriate.

### H (consistency / CLAUDE.md compliance)
- L286 inclusion (SQT worse on S_8) ✓ — CLAUDE.md "결과가 base.md 주장과 다르면 정직하게 base.fix.md에 기록" rule honored.
- Marginalized vs fixed-θ separation ✓ — L6 rule "Occam-corrected evidence vs fixed-θ evidence 혼동 금지" honored.
- "robust" banned in Sec 6 ✓ — consistent with CLAUDE.md tone.
- mu_eff ≈ 1 / S_8 unsolvable rule (L6) ✓ — Sec 6.1 L1 row states this structurally.
- No equations introduced in Sec 6 (limitations are descriptive); 최우선-1 not triggered.

---

## Required edits before draft (3)

1. **Sec 4 reconciliation**: Confirm Sec 4 does not claim "exact coefficient = 1 amplitude locking from theory". If it does, downgrade to "phenomenological coefficient consistent with E(0)=1 normalisation" before finalising Sec 6.2. (CLAUDE.md L6 K20 미해당 rule.)
2. **Bold marginalized Δ ln Z = 0.8** in 6.3 / table caption to prevent skim-misread.
3. **Tabulate the un-anchored Δ ln Z**: either compute and report, or state "not yet computed, planned for revision" — do not leave the reader to infer.

---

## Decision

**APPROVED to draft Sec 6** following the architecture in `ATTACK_DESIGN.md` with edits 1–3 incorporated.

Drafting agent should:
- Write Sec 6 in LaTeX two-column form, ≈ 1450 words, target 2 pages.
- Cite L242, L243, L272, L281, L210, L286 by loop ID in supplementary footnote.
- Cross-check Sec 4 wording on amplitude-locking *before* committing Sec 6.

**Risk if Sec 6 omitted or softened**: high reviewer-rejection probability. Honest disclosure is the load-bearing element of the JCAP-style submission strategy.
