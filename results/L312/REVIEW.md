# L312 REVIEW — 4-Person Panel (P/N/O/H)

Panel: **P** (Proponent), **N** (Skeptic / Devil's advocate), **O** (Outsider / journal editor proxy), **H** (Honesty auditor — enforces CLAUDE.md L6 rules and L272 mock-injection finding).
Scope: ATTACK_DESIGN.md (V1–V8, R1–R3). No LaTeX edited; recommendations only.

---

## P — Proponent
- R1 (honesty-first Sec 1.2 restructuring) is the single highest-value change. Without it, the abstract→intro→conclusion chain inherits a credibility leak that no Sec 5 result can repair. Strong endorse.
- R2 (Sec 2 split) is structurally correct. Keeping a1–a6 + D1–D5 in Sec 2 and pushing σ_0 3-regime + 4 pillars to Sec 3/4/Appendix A matches JCAP single-column rhythm and lets each axiom carry its 4-tuple cleanly.
- R3 manifest is good defensive engineering — prevents L313+ number drift from desyncing abstract.
- Mild concern: V4 attack assumes Sec 2 is overflowing. If current draft is already ≤ 4 pages, the split is premature. **Recommend page-count audit before executing R2.**

## N — Skeptic
- V1 hook attack is partially aesthetic. Reviewers don't desk-reject for opening style; they desk-reject for missing falsifiers or known-wrong data citations. Down-weight V1, up-weight V6.
- V2 is correct but R1 phrasing risks **overcorrection**: "SQMH does not claim to resolve H_0/σ_8" can be quoted out of context as "the theory is uninteresting." Reframe as: "SQMH targets w(z) and BAO residuals; H_0 and σ_8 enter as **prior constraints** that the model satisfies without resolving."
- V3: Chaplygin family was KILLed in L2 R3; citing it as "completed survey" is fine, but do NOT list it in prior-art as a live competitor — that misrepresents the field.
- V5: BAO-only Δχ² of -0.065 is **★★★★★ marker**, not raw χ² units. Confirm units in manifest before publishing — repeated CLAUDE.md warning about "Δχ² vs Δ ln Z vs improvement-marker" confusion.
- V8: a3/a4 are the weakest axioms (metabolism rate σ_0 microscopic origin). Sec 2 must forward-reference Sec 4 cleanly or referee will demand it in revision.

## O — Outsider (journal editor proxy, JCAP target per L6 rule)
- L6 rule: JCAP target = "honest falsifiable phenomenology." PRD Letter requires Q17 OR (Q13 + Q14) — current state does NOT meet PRD Letter bar. R1 honesty-first framing is **necessary** for JCAP positioning.
- Reference adequacy (V6/R3): DESI DR2 (2503.14738), DESY5 SN (2401.02929), Planck 2018 compressed (1807.06209) are non-negotiable. Add Solà 2024 ApJ 975 64 (RVM ν-sign), Frusciante 2021 (f(Q)), Zumalacárregui-Koivisto-Bellini 2013 (disformal), Maggiore-Mancarella (RR non-local).
- Length: JCAP has no hard cap but referees prefer ≤ 30 pages excluding appendix. R2 split keeps total reasonable.
- V7 abstract-intro consistency: editors do notice claim drift. R3 manifest is editor-friendly.

## H — Honesty auditor
- **Mandatory inclusions** (CLAUDE.md L6 + L272):
  1. Sec 1 must state μ_eff ≈ 1 → S_8 tension structurally unresolvable (CLAUDE.md L6 rule).
  2. Sec 1 OR Sec 5 must disclose **L272 mock-injection 100% false-detection rate** as a Branch-B flexibility caveat. ATTACK_DESIGN R3 manifest includes FDR=100% — keep.
  3. Sec 6.4 σ_8/H_0 structural limitation must be cross-referenced from Sec 1.
  4. Δ ln Z numbers — fixed-θ vs fully marginalized — must be labeled per L6 G3 rule. Manifest must specify "marginalized" for the joint number. **No fixed-θ-only quotation in abstract.**
  5. C28 is an independent Maggiore-Mancarella model, NOT SQMH (L6-T3). Prior-art section must not blur the line.
- **Forbidden claims** (must NOT appear anywhere in Sec 1-2):
  - "SQMH solves H_0 tension"
  - "SQMH solves σ_8 tension"
  - "amplitude-locking is derived from theory" (Q17 partial only — CLAUDE.md L6).
  - PRD-Letter-tier language while Q17 incomplete.
- ATTACK_DESIGN as written satisfies these constraints. R1 wording per N's reframe is acceptable.

---

## 정직 결론 (Honest verdict)

**적용 권고 (apply)**: R1, R2, R3 모두 수용. 단:
1. R1 phrasing은 N의 reframe ("targets vs constraints") 채택 — 자기비하 톤 회피.
2. R2 실행 전 현재 Sec 2 draft 페이지 수 실측 (P 지적). ≤ 4 pages면 split 보류, > 5 pages면 즉시 split.
3. R3 manifest의 BAO 항목은 "★★★★★ marker -0.065 (BAO-only, 211-loop cumulative)"로 단위 명시. raw Δχ²와 혼동 금지 (N 지적).
4. H 강제 항목 5개 모두 manifest와 Sec 1 closing paragraph에 의무 포함.

**보류 / 추가 작업**: V1 hook은 R1 적용 후 자연 해결 가능. 별도 attack 불필요.

**Rule 적합성**:
- Rule-A 8인 리뷰 필요 항목: R1 (claim shift, 이론 포지셔닝). 본 4인 리뷰는 pre-screen일 뿐 — 8인 sequential 미실시 상태에서 LaTeX 반영 금지 (CLAUDE.md L6).
- Rule-B 4인 리뷰 필요 항목: R3 reference audit이 스크립트화될 경우 (BibTeX 정합성 체커 등). 본 loop 산출물은 outline only이므로 Rule-B 미발동.

**진실성 체크**: 본 리뷰는 가상 시뮬레이션 결과를 만들지 않았다. 실제 LaTeX 편집 없음, outline + 권고만 제공 — 사용자 정직 원칙 준수.
