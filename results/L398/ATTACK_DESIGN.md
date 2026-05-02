# L398 ATTACK DESIGN — JCAP Cover Letter v3

**Loop**: L398 (single, 독립)
**Date**: 2026-05-01
**Target**: JCAP cover letter v3 — L369 v2 를 baseline 으로, L342-L391 정직 reflection 갱신. 핵심 추가: **L346 비단조 σ_0(z) fit caveat** 명시 + L370-L391 execution-focused 라운드 흡수.

---

## 상위 컨텍스트 (L369 v2 → L398 v3 차이)

L369 v2 (2026-05-01 작성) 시점:
- 누적 ~268 loop, L341 audit, L342-L368 회복 27라운드 흡수.
- 9 limitations (L1-L9) 정직 disclosure.
- P17 Tier A/B pre-registration 구조 letter 본문화.

L370-L391 사이 새로 누적된 정직 발견 (results/L346 포함, L369 작성 시점에 letter 본문에 흡수되지 않은 항목):

1. **L346 (비단조 fit caveat, 최우선 추가)**: σ_0(z) 비단조 패턴은 SQT 4 pillar 의 **a priori 예측이 아니라 데이터에서 발견된 fit**. 4 pillar 는 비단조를 *허용*하나 *강제*하지 않는다 (정성 등급 L 5/0 2/M 1/Posterior 1). L67 시점에서 데이터 발견 → L68 잔차 → 메커니즘 탐색 순서로 retro-rationalized. P17 Tier B (V(n,t) derivation gate) 미완 상태에서 비단조 *형상 자체*는 lock 되어 있지 않다.

2. **L342-L391 execution-focused 라운드**: 일부 라운드는 디자인이 아니라 시뮬레이션 실행 / MCMC 진행 / 데이터 검증으로 분류. 빈 디렉터리 (L364, L376, L390, L392, L393, L396) 와 단일-아티팩트 라운드 정직 인벤토리 갱신 필요.

3. **JCAP 등급 영향 (L346 한정)**: -0.005~-0.010 보수, -0.015 적극. v3 는 보수 채택, pillar 4 ★★ 유지하되 비단조 prediction 표현 약화.

---

## 8인 공격 (자율 분담, 역할 사전지정 없음)

- **A1 (L346 caveat 본문화)**: §2 "Honest disclosure" 에 L10 항목으로 L346 결과 추가. "비단조 σ_0(z) 는 prediction 이 아니라 fit-driven, 4 pillar 와 모순되지 않을 뿐" 직접 인용. R1 sloppy 와 별개 항목으로 분리 (sloppy 는 차원성, L346 은 prediction-vs-fit 시간선).

- **A2 (Sec 3 P17 표현 약화)**: P17 Tier A 카드 중 σ_0(z) 형상 관련 falsifier 가 "비단조성 자체"가 아니라 "BB 진폭 + 극값 *추정*" 만 lock 한다는 점 명시. v2 에서는 이 미세 구분이 letter 본문에 노출되지 않았음.

- **A3 (R0 reviewer objection 신설)**: §5 anticipated objections 에 "R0 (예측이냐 fit 이냐)" 추가. L346 의 fit-driven discovery 시간선을 정직 인정하며, 4 pillar 의 prior strength 가 비단조에 약함을 명기.

- **A4 (Recovery 인벤토리 갱신)**: L342-L368 인벤토리 → L342-L391 인벤토리. execution-focused 라운드 (시뮬레이션 실행) 를 별도 카테고리로 분리. 빈 디렉터리 카운트 갱신.

- **A5 (등급 갱신)**: ★★★★★ -0.08 (L341) → -0.085~-0.090 (L346 보수 반영). "★★★★★ -0.085 at L391 audit close" 표기. 임의 상향 금지.

- **A6 (Tier B derivation gate 강조)**: P17 Tier B (V(n,t) full derivation) 가 비단조 형상 lock 의 *전제조건*임을 §3 에 1문장 추가. derivation gate 통과 전까지는 Tier B 가 Tier A 와 동격 아님 — v2 에서 이미 명시되어 있으나 L346 결과로 이 게이트의 *비단조 책임* 이 추가됨.

- **A7 (정직 한 줄)**: 한국어 한 줄 정직 line — "비단조 σ_0(z) 는 SQT 4 pillar 의 a priori 예측이 아니라 데이터에서 발견된 fit 이며, v3 는 이를 letter 본문에 명기한다." (L346 §J3 인용)

- **A8 (Format 유지)**: v2 의 1.5-2 page 본문 + 별첨 P17 카드 + Limitations 박스 구조 유지. v2 → v3 변경분만 diff 로 식별 가능하도록 §2 L10 / §5 R0 추가, §3 약화, §4 인벤토리 갱신, 등급 -0.005 의 **5 군데** 만 손댐.

---

## Top-3 (8인 합의)

**A1 + A3 + A5**. 이유:
- A1 = L346 결과를 letter 본문에 흡수 (제출자 정직성 핵심 채널).
- A3 = referee 의 가장 자연스러운 objection (예측이냐 fit 이냐) 에 사전 응답.
- A5 = 등급 임의 유지 금지, L346 영향 보수 반영.

(A2/A6 은 §3 미세 표현 수정으로 흡수, A4 는 §4 본문 갱신, A7/A8 은 letter tone/format 으로 흡수.)

---

## 통과 기준

- COVER_LETTER_v3.md 가 v2 를 baseline 으로 다음 5 변경분 모두 반영:
  1. §2 L10 항목 (L346 비단조 fit caveat) 추가.
  2. §3 P17 표현 약화 (Tier A 가 비단조 *형상* 이 아니라 *진폭+극값 추정* 만 lock).
  3. §5 R0 (prediction vs fit) anticipated objection 추가.
  4. §4 recovery 인벤토리 L342-L391 로 갱신, execution-focused 라운드 분리.
  5. 등급 -0.08 → -0.085 (보수 반영).
- L346 결과를 letter 본문에 노출 (별첨 아님).
- P17 Tier B derivation gate 가 비단조 형상 lock 의 전제조건임을 1문장 이상 명기.
- 정직 한국어 한 줄 REVIEW.md 에 포함.
- 등급 임의 상향 금지. 이론 prediction 강화 표현 추가 금지.

## 실패 시 처리

- L346 caveat 이 letter 본문에 흡수되지 않으면 → 재작성.
- P17 Tier A 가 비단조 형상 자체를 lock 하는 것처럼 표현되면 → 재작성.
- 등급이 v2 의 -0.08 그대로 유지되면 (L346 영향 0) → 재작성.
- 빈 디렉터리 (L364, L376, L390, L392, L393, L396 등) 가 인벤토리에서 누락되면 → 재작성.
