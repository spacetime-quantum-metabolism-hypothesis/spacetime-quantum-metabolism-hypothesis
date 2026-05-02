# L399 REVIEW — Appendix A outline (4-person adversarial)

자율 분담 4인 리뷰 (역할 사전 지정 없음). Independent session.
Honest one-liner: this review checks the L399 plan against CLAUDE.md rules
and the L272 CRITICAL finding without softening it.

## Reviewer P (overfitting / honesty audit)
- L272's "100% false BB detection" must appear in **Appendix A.1 first
  sentence**, not buried mid-paragraph. The ATTACK_DESIGN places it correctly.
  PASS.
- Anti-spin discipline includes "do not present L272 as resolved" — verified.
  PASS.
- One concern: the integration narrative (A.0) says L275/L278/L279/L280 are
  PASSes "given the L272 caveat is honored". This is correct but must be
  phrased so a referee cannot read it as conditional approval of BB itself.
  → **Action: A.0 must say the PASSes are *robustness of the fit*, not
  *evidence for BB over LCDM*.**

## Reviewer N (statistical rigor)
- L277 coverage 87% vs nominal 90% is marginal; ATTACK_DESIGN flags this
  honestly. PASS.
- L280 SBC: 100 rounds is below the 1000 recommended — flagged as
  budget-limited. Ensure APPENDIX_OUTLINE A.6 carries this caveat verbatim.
- L279 cluster anchor weakness (single A1689, ±0.15 dex log) is the single
  numerical fragility. APPENDIX_OUTLINE A.5 must keep this on the surface.
- L278 jackknife Q=1 subset ΔAICc 78 vs full 99 — a ~21-point drop. Not
  catastrophic but non-trivial. Must be disclosed in A.4 numerically, not
  qualitatively.

## Reviewer O (scope discipline / CLAUDE.md compliance)
- CLAUDE.md L6 rule: "mu_eff ≈ 1 → S_8 tension 해결 불가" — Appendix A
  scope explicitly excludes S_8 / K15. COMPLIANT.
- CLAUDE.md L5 rule: "Δ ln Z gap < Occam penalty for current data" — must
  not appear in Appendix A as that is a Bayesian-evidence claim, not a
  robustness claim. ATTACK_DESIGN keeps it out of scope. PASS.
- CLAUDE.md "정직 한 줄" rule — every L-session document carries one. Plan
  carries it. Output files must carry one each.
- 8인/4인 rule: Appendix A is a **code-output consolidation**, so 4-person
  review (Rule-B) is the correct gate. Plan complies.

## Reviewer H (cross-session consistency)
- L208 ΔAICc = 99 (real data) is the headline. L272 mock 132.95 is the
  worst-case-overfitting reference. The two numbers must be reported
  side-by-side in A.1 so a reader sees: real-data preference is *smaller*
  than the false-positive expectation under data-driven anchors. This is
  the precise piece that forces "anchor predetermined, not fitted" into
  the main text.
- L396 Sec 7.3 (companion paper) and L399 Appendix A are aligned: Appendix A
  is the falsifiable robustness layer, companion paper is the
  phenomenology-only fallback. No conflict.
- L275 ↔ L279 ↔ L280 form a self-consistent calibration triangle (prior
  sensitivity ↔ bootstrap CI ↔ SBC rank uniformity). APPENDIX_OUTLINE A.0
  intro should make this triangle explicit so the appendix reads as one
  argument, not six unrelated diagnostics.

## Joint verdict
PASS with the following required edits to APPENDIX_OUTLINE.md:

1. A.1 opening sentence quotes L272 result verbatim ("200/200 false
   BB preference under data-driven tertile split").
2. A.1 reports L208 ΔAICc = 99 vs L272 mock median 132.95 in the same
   table or paragraph.
3. A.0 distinguishes "robustness of fit" from "evidence for BB"
   (Reviewer P action).
4. A.4 reports Q=1 ΔAICc = 78 numerically.
5. A.5 keeps the single-A1689 weakness on the surface and lists "additional
   cluster anchors" as the named follow-up.
6. A.6 carries the "100 rounds, budget-limited, 1000 recommended" caveat
   verbatim.
7. A.7 (limitations) lists: (i) data-driven anchor mock not yet replaced
   by theory-prior anchor mock, (ii) high-mass / late-type / distance-bias
   strata not yet jackknifed, (iii) SBC under-sampled.

정직 한 줄: Appendix A consolidates six robustness sessions into one
falsifiable evidence layer; the L272 mock failure is the load-bearing
caveat and is preserved, not laundered.
