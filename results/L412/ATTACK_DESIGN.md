# L412 — 8인팀 reviewer attack 설계 (§5.2 강등 안 한 경우의 시나리오)

세션 일자: 2026-05-01
대상: paper/base.md §5.2 의 `ρ_q/ρ_Λ = 1.0000 *exact*` PASS_STRONG 광고가
README TL;DR / abstract 양면에서 그대로 유지된다고 가정한 시나리오.
원칙: CLAUDE.md [최우선-1, 2] — 방향만 제공, 8인팀 자율 토의 시뮬.

전제: L402 가 도달한 결론 "회피 불가능 confirmed (Path-α 10⁶⁰ 어긋남,
A1·A2·A3·A4·A8 회피 불가)" 을 받아들인 상태에서, *그래도* 광고를 유지한
경우의 referee attack 면을 사전 발굴.

---

## 1. 8인팀 토의 시뮬 (PR P0-1 미적용 시나리오)

**P1 (관측우주론):** "이미 L402 에서 회피 불가능이 확정된 항진명제를
abstract 1번 bullet 으로 두고 PASS_STRONG 으로 광고하는 것은
*L402 결론을 paper 가 알고도 무시했다* 는 형태로 referee 에게 읽힌다.
이건 단순 circularity 지적보다 한 단계 위의 critique — *self-aware
circularity advertising* 으로 분류된다."

**P2 (장이론):** "PRD/JCAP 두 channel 모두 referee 1번 항목으로 직격.
'authors acknowledge circularity in §5.2 yet promote PASS_STRONG in
abstract/TL;DR' 한 문장으로 major-revision 또는 reject 사유 성립.
편집자 desk-reject 가능성도 비-zero."

**P3 (통계):** "광고와 본문이 *불일치* 하는 구조는 statistical reporting
standards (ASA 2016, ICMJE) 의 ' fair representation' 위반. caveat 가
본문에 있어도 '주된 광고 channel (abstract/TL;DR/headline 표) 이 reader
의 first impression' 이라는 것이 표준 해석. 정정 요구 자동."

**P4 (현상론):** "변호 가능 line 은 'order-of-magnitude 일치는 trivial
아님' 한 가지뿐. 그러나 그 변호선은 1.0000 광고가 아닌 '~10⁰ order'
광고일 때만 작동. *exact* 1.0000 표기를 유지하면 이 변호선도 죽는다."

**P5 (수리물리):** "L402 NEXT_STEP 에서 시도한 Path-α (Hubble+Planck only
독립 도출) 는 10⁶⁰ 어긋남으로 실패. 즉 회피 path 가 닫혔음을 paper
authors 가 *이미 안다*. 이 사실이 L402 ATTACK_DESIGN.md 에 git 기록으로
남아 있어 referee 가 repository 를 보면 즉시 발견. 정직성 문제로 격상."

**P6 (철학·방법론):** "Popper falsifier 결여 (A4) + self-aware circularity
는 *demarcation* 차원의 문제. PRD Letter 의 'predict, don't postdict'
정책뿐 아니라 일반 PRD 도 'A is consistent with A' 류 항진명제는 contribution
으로 인정 안 함. abstract 1번 bullet 으로는 가장 약한 위치."

**P7 (편집자 시각):** "L411 REVIEW.md 에서 이미 '강등 전 acceptance 매우
낮음' 으로 정성 진단됨. 강등 안 하는 시나리오의 학계 수용 확률은
사실상 0. JCAP 도 same critique 적용."

**P8 (synthesizer):** "팀 합의:
1. *광고와 본문 불일치* 비판 (severity HIGH) 가 단일 sentence 로 reject
   사유 성립 — abstract/TL;DR 1번 bullet 이 가장 약한 위치.
2. L402 ATTACK_DESIGN 의 git 기록 자체가 *self-aware circularity* 증거로
   reviewer 가 활용 가능 (repo 공개시).
3. *exact* 1.0000 표기는 변호선 (order-of-magnitude) 까지 닫는다.
4. 따라서 PR P0-1 (PASS_STRONG → CONSISTENCY_CHECK) 은 *옵션이 아니라
   필수*. 강등 안 한 시나리오는 referee 1번 attack 으로 즉시 사망."

---

## 2. 공격선 정리 (강등 미적용 시 reviewer report 예측)

| # | 공격 | severity | 회피 가능? | 근거 |
|---|------|----------|------------|------|
| B1 | Abstract/TL;DR PASS_STRONG 광고와 §5.2 caveat 본문이 *위계 충돌* | CRITICAL | YES (강등 시) | L402 A5 연장선 |
| B2 | L402 ATTACK_DESIGN.md git 기록 = self-aware circularity 증거 | CRITICAL | YES (광고 강등으로 합치) | repo 공개 시 referee 활용 |
| B3 | "1.0000 *exact*" 표기는 order-unity 변호선까지 닫음 | HIGH | YES (`~10⁰ order` 표기로) | P4 line |
| B4 | Path-α 실패 (10⁶⁰) 가 회피 불가능 *증명* — paper authors 인지 | HIGH | NO (구조적) | L402 NEXT_STEP |
| B5 | TL;DR 첫 ✅ bullet 으로 배치 → reader first impression bias | HIGH | YES (bullet 위치/색 변경) | A5 변형 |
| B6 | claims_status table "Λ origin ✅ PASS_STRONG" enum mismatch | MEDIUM | YES (enum 변경) | enum 표 §룰 위반 |
| B7 | 자기-감사 (32 claim) 의 "PASS_STRONG 10/32" headline 에 본 항목 포함 → 전체 31% 광고 inflated | MEDIUM | YES (PASS_STRONG 9/32 로 재계산) | abstract 614 line, README 149 line |
| B8 | "verify_lambda_origin.py (1.0000 match)" Quickstart 광고 — verifier 명칭이 *predict* 함의 | MEDIUM | YES (script 명/주석 변경) | README L156 |

## 3. 정직 판정

B4 는 구조적 회피 불가 (L402 확정). B1, B2, B3, B5, B6, B7, B8 은 *전부*
광고 강등으로 동시 회피 가능. 즉 **PR P0-1 적용 단일 행위로 7/8 공격선
무력화** — 이것이 L412 NEXT_STEP 이 "강등 직접 시행" 을 권고하는 이유.

강등 미적용 시 referee 1번 항목 attack 면이 8개로 늘어 desk-reject ~
major-revision 확률이 거의 100% 로 수렴. 강등 적용 시 attack 면 1개
(B4, 구조적·정직 disclosed) 로 축소.
