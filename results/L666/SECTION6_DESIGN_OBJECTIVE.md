# L666 — Paper C §6 Limitations Design Objective 갱신

**Date**: 2026-05-02
**Scope**: §6 limitations 의 *design objective* 재정의 — *acceptance optimization* 제거,
*genuine honesty* 만 primary objective.
**Status**: Plan-only (paper / claims_status / 디스크 edit 0건)

---

## §1. Old vs New Design Objective

### §1.1 Old design objective (L658 / L661 implicit)

L658 Path 1+5 framing 과 L661 PAPER_C_DRAFT_V2 implicit 설계는 다음을 *내포* 했음:

- "§6 limitations 의 자발적 disclosure → reviewer trust 상승 → acceptance 상승"
- "Path 1 disclosure 강화 = acceptance 향상 추정 (~63–72%)"
- limitations 가 *acceptance 도구* 로 기능
- *honesty* 는 *means*, *acceptance* 가 *end*

→ L663 #1 비판 ("marketing tool" 위험): 학계가 *detect 가능* (R3 / R7 응답에서
"voluntary disclosure 가 reputational hedge 처럼 보인다" 류 reaction 가능).
→ design objective 자체가 *honesty 를 도구화* 하므로 *진짜 정직* 이 아님.

### §1.2 New design objective (L666)

§6 limitations 의 *purpose 단일화*:

> **§6 의 primary objective 는 학계 정직성 standard 에 기여하고,
> future researcher 가 SQT 의 진짜 약점을 인지할 수 있도록 하는 것이다.
> Acceptance 결과는 부수 효과이며, primary objective 가 아니다.**

- "marketing 의도 0" 본문 명시 (§6 도입부 또는 §6.0 footnote)
- L658 Path 1+5 *acceptance 향상 추정* 본문 인용 0건
- *only objective*: 학계 honesty standard 기여 + future researcher 가 SQT 진짜 약점 인지

---

## §2. §6 재구성 plan (L661 PAPER_C_DRAFT_V2 → L666 갱신)

기반 source: L661 PAPER_C_DRAFT_V2 §6 골격. L664 항목별 정직성 의무 통합.

### §2.1 §6.1 — Hidden DOF quantitative table (lead)

- §6 *맨 앞* 에 *정량* hidden-DOF table 배치 (L664 항목 2)
- 9–13 DOF itemized (L495 / L502 인용)
- 각 DOF 별 ΔAICc penalty 정량 명시 (L502 audit 결과)
- "0 free parameter" 어휘 *영구 폐기* (L569 / L591 / L654)
- table caption 에 "이 DOF 들은 fit 전에 fix 되었으나, theoretical DOF 로 counted 되어야 한다" 명시

### §2.2 §6.2 — Channel-dependence retraction

- 종전 "4/4 PPN PASS" 표현 → *retraction*
- 갱신 표현: "1/4 dark-only PASS, 3/4 N/A under axiom 6" (L664 항목 4)
- L506 Cassini cross-form 재인용 (universal coupling 위반 경로)
- "axiom 6 dark-sector restriction 이 baryon channel 을 *evade* 하는 것이 아니라
  *redefine* 하는 의도적 선택" 명시

### §2.3 §6.3 — Postdiction admission

- 3-regime σ₀(env) 가 *사후* (post-hoc) 발견된 사실 정직 기재
- "out-of-sample test 부재" 명시 (L664 항목 5: held-out test 미달 인정)
- future test 조건 (DR3 등) 만 명시, "DR3 가 통과하면 우리가 옳다" 류 confident claim 금지

### §2.4 §6.4 — Fabrication disclosure (L564)

- 자발적 disclosure ratio ~90% (L564 audit)
- *retraction 의무* 는 paper A 의무로 분리
- paper C 는 *cross-mention* 만 ("paper A 에서 별도 retraction 진행 중")
- paper C 본문에서 fabricated result 직접 사용 0건 재확인 footnote

### §2.5 §6.5 — A-priori 4 박탈 (L549 / L552 / L562 / L566)

- 박탈된 a-priori 4건의 박탈 사유 정직 기재
- multi-session a-priori 의무 (L633 H2) 명시
- "single-session a-priori 는 자기 검증 불가" 정직

### §2.6 §6.6 — Mass redefinition 영구 종결 (L582)

- 7 path 박탈 자발 disclosure
- 각 path 가 박탈된 사유 1줄씩 (L582 audit table 인용)
- "mass redefinition 노선 전체 closed" 영구 commitment

### §2.7 §6.7 — Paradigm shift 박탈 risk (Phase 31–40)

- A3+Time emergent 후보 박탈 risk
- Bootstrap 후보 박탈 risk
- Self-incompleteness 후보 박탈 risk
- L621 (B) 박탈 정직 기재
- "paradigm shift claim 은 현 단계 데이터로 지지 불가" 명시

---

## §3. Acceptance optimization 제거

다음 사항을 §6 본문 / §6 frontmatter / abstract 모두에서 *명시* 제거:

1. "voluntary disclosure → reviewer trust" 류 framing 0건
2. L658 Path 1+5 acceptance 향상 추정 (63–72%) 인용 0건
3. "limitations 강화로 reception 개선" 류 어휘 0건
4. cover letter / response template 에서도 동일 제거 (L666 follow-up scope)

§6 도입부 1줄 명시 (수식 0줄, 어휘만):

> "본 §6 의 목적은 학계 정직성 standard 에 대한 기여이며,
> reviewer reception 향상을 의도하지 않는다."

---

## §4. Genuine honesty effect (간접)

L666 design objective 는 *acceptance 를 직접 목표 삼지 않음* 을 원칙으로 하나,
*간접 효과* 로 다음이 *발생할 수 있음*:

- 진정 honest §6 → 학계가 *detect 어려운* marketing tone 부재 → 진짜 reception 향상 *가능*
- 그러나 이는 *부수 효과*, paper 내 본문 / cover letter / abstract 에서
  *직접 claim 금지*
- "Path 1 효과 부활" 류 표현 0건

---

## §5. 8인 Rule-A 의무

본 design objective 갱신은 *이론 클레임 수정* (limitations 정직성 재정의) 에 해당하므로
**Rule-A 8인 순차 리뷰 필수** (L6 재발방지 마지막 항목).

리뷰 대상:
- §1 Old vs New design objective (단일화 정당성)
- §2 §6.1–§6.7 재구성 plan (각 항목 정직성 의무 충족 여부)
- §3 acceptance optimization 제거 (본문 / cover letter / abstract 일괄 적용)
- §4 genuine honesty effect 간접화 (직접 claim 0건 보장)

8인 합의 도달 전 paper / claims_status / draft 디스크 edit 금지.

---

## §6. 정직 한 줄

본 L666 design objective 갱신은 §6 limitations 를 *acceptance tool* 에서
*honesty standard contribution* 으로 재정의한다.
정직성이 acceptance 를 *유발* 할 수 있으나, 이는 *목적이 아닌 부수 효과*이다.
