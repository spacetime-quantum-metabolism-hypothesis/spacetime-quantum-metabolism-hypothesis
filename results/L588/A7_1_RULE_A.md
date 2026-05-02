# L588 — A7-1 (Causality / Unitarity axiom) 8인 회의적 검증 (Rule-A)

**작성일**: 2026-05-02
**선행**: L585 §2 Top-2 (A7-1 Causality / Unitarity), L578 Path 3 (B), L583 R3+R4, L552 박탈 (anchor circularity).
**[최우선-1] 절대 준수**: 본 문서는 *방향* 평가만. 수식 0줄, 파라미터 값 0개, 유도 경로 힌트 0개. 등재 가/부 *판정* 만 산출.
**임무**: 8인 회의적 reviewer 가 A7-1 (SR/GR causality + unitarity 를 SQT 본문 axiom 으로 등재) 를 R1~R8 축에서 압박.

---

## §1. 8인 회의적 압박 (R1 ~ R8)

### R1 — 외부 import 범위
**Reviewer R1 (외부 framework 경계 감시)**:
- A7-1 은 "SR/GR causality" 라는 외부 framework 의 *부분* 을 import 한다고 주장하나, causality 는 *light-cone 정의 + signal speed bound + chronology protection* 패키지로만 의미를 갖는다.
- "causality 만" 떼어내려면 어떤 light-cone 을 쓰는지 (SR Minkowski / GR dynamical / SQT 자체 light-cone) 명세 필수.
- SQT 자체 light-cone 정의 미존재 → SR/GR light-cone 통째 import 강제. **부분 import 주장 거짓**.
- **판정**: A7-1 은 사실상 SR/GR 본문의 light-cone 구조 전체를 axiom 으로 들여오는 것과 동등. L585 §1 표의 "외부 import 위험 낮음" 은 과소평가.

### R2 — 4-pillar 정합 (SK propagator)
**Reviewer R2 (SK pillar 감시)**:
- SQT 의 SK (Schwinger-Keldysh) propagator 는 retarded/advanced 구조에서 이미 causality 를 *내포* 한다.
- A7-1 등재가 SK pillar 위에 무엇을 *추가* 하는지 명시 의무. 단순 "재명시" 라면 axiom *중복* — Occam 위반.
- A7-1 이 SK 너머의 *globally hyperbolic* 조건 (전역 Cauchy surface) 까지 요구한다면, 이는 4-pillar 외부 정보 — 큰 import.
- SK 가 이미 부분 causality 를 가지므로, A7-1 의 *증분 가치* 가 0 이거나 음수일 수 있음.
- **판정**: A7-1 의 SK pillar 대비 *추가 정보량* 이 명시되지 않음. 명세 의무 미충족 시 axiom 중복.

### R3 — Q17 도출 경로 (causality → amplitude)
**Reviewer R3 (도출 메커니즘 감시)**:
- causality constraint 는 "위반 회피" (negative result) 만 강제. amplitude 의 *양수성* 이나 *값* 을 직접 규정하지 않음.
- amplitude-locking 은 cross-coupling channel 의 *동역학적 등호* 를 요구. causality 는 등호가 아닌 *부등호 (cone 외부 신호 금지)* 만 제공.
- causality + unitarity 결합 시 Källén-Lehmann 양수성 / Froissart bound 같은 부등식 유도 가능 — 하지만 *등호 amplitude-locking* 까지는 거리 매우 멈.
- 실제 도출 시 unitarity 의 *어느 분해* (cutting rules / dispersion / partial-wave) 를 쓸지 선택 자유도가 hidden DOF.
- **판정**: causality 단독으로 Q17 amplitude 등호 도출 *불가능*. 추가 보조가정 (positivity bound + saturation) 필요 — 즉 hidden DOF 가 L585 §1 평가보다 큼.

### R4 — Hidden DOF 비용
**Reviewer R4 (DOF 회계 감시)**:
- A7-1 등재 시 명시 의무 항목:
  (a) light-cone 정의 (SR / GR / SQT 자체)
  (b) signal speed (c 또는 SQT effective)
  (c) unitarity choice (S-matrix / inclusive / Wightman positivity)
  (d) chronology protection 강도 (CTC 금지 / 약한 chronology / Hawking 강한 chronology)
  (e) macro/micro causality 구분
- 5개 의무 명세 → axiom 1개로 보이지만 hidden 선택 5개. L585 §1 의 "hidden DOF 낮음" 평가는 부정확.
- 각 선택은 L549 P3a 박탈 패턴 (단일 보조가정 → DOF 추가) 과 동형 위험.
- **판정**: A7-1 hidden DOF 비용 *중간~높음* 으로 재분류 필요.

### R5 — Anchor 의존 (L552 패턴)
**Reviewer R5 (L552 anchor circularity 감시)**:
- causality 의 light-cone 은 *signal speed* 를 정의해야 의미. SR 에서는 c 가 절대 anchor.
- SQT 본문에 c 를 axiom-level 로 박으면 anchor 는 c (Lorentz-invariant) — H₀ 의존이 아니므로 L552 패턴 직접 재발은 *없음*.
- 단, GR causality (dynamical light-cone) 까지 포함하면 light-cone 이 metric 에 의존, metric 은 background scale 에 의존 → *간접* anchor 회귀 가능성.
- "SR causality 만" 으로 한정하면 R5 통과. "SR+GR 둘 다" 면 L552 sibling 위험.
- **판정**: SR-only 한정 시 R5 통과, GR 포함 시 위험. *명세 강제* 필요.

### R6 — 관측 가능성 / Falsifiability
**Reviewer R6 (R4 protocol 감시)**:
- causality 자체는 *모든 SR/GR 실험의 해석 전제* — 검증 불가능 (가정 없이 데이터 분석 자체가 안 됨).
- A7-1 을 falsifiable 하게 만들려면 SQT-specific predicción 필요: 예) 양자 단위 신호 속도가 c 와 다르면 위반, 특정 amplitude 가 unitarity bound 를 깨면 위반.
- 하지만 "unitarity bound 를 깨는 amplitude" 자체가 Q17 amplitude-locking 을 가정해야 정의됨 → **순환 논법**.
- L583 R4 (postdiction-free) protocol 통과 여부 불명. amplitude 결과를 알고 axiom 을 선택했다면 R4 위반 직격.
- **판정**: A7-1 의 falsifiability protocol *미정의*. R4 통과 입증 책임 axiom 제안자에게.

### R7 — Z_2 SSB pillar 충돌
**Reviewer R7 (Z_2 domain wall 감시)**:
- SQT 의 Z_2 SSB pillar 는 domain wall 동역학을 핵심으로 함. wall 통과 시 light-cone 구조 변형 가능.
- A7-1 causality (특히 strong chronology protection) 는 wall 횡단 시 신호 전달이 *단순 SR cone* 일 것을 강제 → wall 동역학과 충돌 가능성.
- wall 내부에서 effective signal speed 가 c 와 다르면 A7-1 (SR causality) 위반. SQT 의 SSB pillar 는 wall 내부 동역학 자유도를 요구.
- **판정**: A7-1 (SR strict) 과 Z_2 SSB pillar 가 *동역학적 충돌 가능*. 명세 보정 (effective causality / wall-modified light-cone) 없이는 4-pillar 정합 미달성.

### R8 — Postdiction / Cherry-pick 위험
**Reviewer R8 (cherry-pick 감시)**:
- A7-1 은 "Causality / Unitarity" 라는 *복합* axiom — Coleman-Mandula / Lorentz invariance / Wightman positivity / S-matrix unitarity / Froissart bound 중 어느 부분집합인가?
- Q17 amplitude-locking 결과를 *알고서* causality 패키지의 어느 component 가 도출에 필요한지 역추적했다면 cherry-pick.
- L552 RG 패키지 박탈 사유 (anchor circularity + postdiction) 와 패턴 동형: 결과 → axiom 역방향 선택.
- 실제 axiom 등재 전 protocol: amplitude 결과를 *모른 상태에서* causality 의 어느 부분집합이 SQT 의 SK + Z_2 + 양자단위 + 통계 4-pillar 와 minimal 정합하는지 *독립 도출* 의무.
- **판정**: 현재 시점 A7-1 은 cherry-pick 의심 강함. 사전회의 전 독립 도출 입증 필요.

---

## §2. 종합 위험 매트릭스 (R1~R8)

| 축 | 위험 | 명세 의무 충족 시 완화 가능 |
|----|------|----------------------------|
| R1 외부 import | **중간** (light-cone 패키지 통수입) | 예 (SQT 자체 light-cone 정의 시) |
| R2 SK pillar 정합 | **중간** (axiom 중복 의심) | 예 (증분 정보량 명시 시) |
| R3 도출 경로 | **높음** (causality 단독 amplitude 등호 불가) | 부분 (positivity bound 추가 필요 — DOF 증가) |
| R4 hidden DOF | **중간~높음** (5개 hidden 선택) | 예 (5개 모두 명시 시) |
| R5 anchor 의존 | **낮음 (SR-only) / 중간 (GR 포함)** | 예 (SR 한정 명시 시) |
| R6 관측 가능성 | **높음** (순환 논법 위험) | 부분 (SQT-specific 예측 정의 시) |
| R7 Z_2 충돌 | **중간** (wall 동역학과 충돌 가능) | 예 (effective causality 보정 시) |
| R8 postdiction | **높음** (cherry-pick 의심) | 부분 (사전 독립 도출 입증 시) |

**고위험 (R3 / R6 / R8) 3축이 동시 미해결** — L552 박탈 패턴과 동형 위험 신호.

---

## §3. A7-1 vs A7-2 vs Q17 Path 3 비교

| 항목 | A7-1 (Causality / Unitarity) | A7-2 (Conservation Law) | Q17 Path 3 (Wetterich anchor-free) |
|------|------------------------------|-------------------------|--------------------------------------|
| 4-pillar 위치 | 외부 (axiom 추가) | 외부 (axiom 추가) | 내부 (anchor 만 제거) |
| 도출 메커니즘 명료성 | **낮음** (부등식 → 등호 갭) | 중간 (보존량 → cross-coupling 매핑 비자명) | **높음** (Wetterich 잘 알려진 구조) |
| Hidden DOF | 중간~높음 (5 hidden 선택) | 중간 (보존량 1개) | **낮음** (DOF 감소 방향) |
| Anchor 의존 | 낮음 (SR-only) | **낮음** | 낮음 (anchor 제거) |
| Postdiction 위험 | **높음** (R8 cherry-pick) | 낮음 (위반 직접 검증) | 중간 (L552 sibling) |
| Falsifiability | **낮음** (순환 논법) | **높음** (보존법칙 위반 검증) | 중간 |
| L552 박탈 패턴 재발 | **부분 동형** (R3+R6+R8) | 회피 가능 | sibling — 직접 후속 |
| 4-pillar 충돌 | **R7 Z_2 SSB 충돌 가능** | 충돌 신호 없음 | 충돌 신호 없음 |
| 글로벌 고점 회복 잠재력 | **부분** (L585 §3 평가) | 약간 우위 | 중간 |

**상대 순위** (회의적 reviewer 합의):
1. **A7-2 (Conservation Law)** — 가장 안전 (R6 falsifiability 강함, R8 postdiction 약함).
2. **Q17 Path 3 (Wetterich anchor-free)** — 4-pillar 내부 유지, DOF 감소 방향.
3. **A7-1 (Causality / Unitarity)** — R3+R6+R8 3축 동시 고위험. 명세 의무 미충족 시 박탈 가능성 가장 큼.

---

## §4. 최종 판정

### 후보지: (A) Round 11 진입 / (B) 사전회의 의무 / (C) 자동 박탈

**8인 합의 판정**: **(B) 사전회의 의무**

**근거**:
- R1 (외부 import) 명세 의무 미충족 — light-cone 정의 / SR vs GR 한정 명시 필요.
- R2 (SK pillar 증분 정보량) 명시 의무 미충족 — axiom 중복 의심.
- R3 (도출 경로) 갭 — causality 단독 amplitude 등호 불가, 보조가정 필요성 명시 의무.
- R4 (hidden DOF 5개) 명시 의무 — light-cone / signal speed / unitarity choice / chronology / macro-micro 5개 선택 모두 사전 고정.
- R6 (falsifiability) protocol 정의 의무 — 순환 논법 회피 명세.
- R7 (Z_2 SSB 충돌) 정합성 명시 의무 — effective causality 보정 또는 wall 동역학과의 양립 명세.
- R8 (postdiction) 사전 독립 도출 입증 의무 — Q17 amplitude 결과를 *모른 상태에서* causality 부분집합 선택 입증.

**(A) Round 11 진입 거부 사유**: R3+R6+R8 고위험 3축 미해결 상태에서 본문 axiom 등재는 L552 박탈 패턴 재발 위험 직격.

**(C) 자동 박탈 거부 사유**: R5 anchor 의존이 SR-only 한정 시 통과 가능성 — 명세 정비 시 회생 여지 존재. A7-2 / Path 3 (B) 와 함께 *병행 protocol* 대상으로 유지.

**사전회의 의무사항**:
1. R1~R8 8축 명세 의무 충족 입증 산출물 사전 제출.
2. amplitude 결과를 모르는 reviewer 부분집합 (예: 8인 중 4인) 이 *독립적으로* causality 부분집합을 선택하는 blind protocol 실행 → R8 cherry-pick 차단.
3. A7-2 (Conservation Law) 와 Q17 Path 3 (Wetterich) 양쪽과 병행 비교. 단독 채택 금지.
4. 사전회의 통과 후에도 Round 11 진입은 별도 의결 — 본 L588 은 진입 자동 승인 아님.

---

## §5. 정직 한 줄

> A7-1 (Causality / Unitarity) 은 외부 import 가 가장 적어 보이는 path 라는 L585 §2 평가에도 불구하고, R3 (causality 부등식 → amplitude 등호 갭) + R6 (falsifiability 순환 논법) + R8 (postdiction cherry-pick) 3축 고위험이 동시 미해결이며, R7 (Z_2 SSB pillar 와의 동역학적 충돌 가능성) 까지 더해 4-pillar 정합도 자동 보장되지 않으므로, 본문 axiom 등재 전 8인 사전회의에서 R1~R8 8축 명세 의무 + blind protocol + A7-2 / Path 3 (B) 병행 비교를 통과해야 한다.

---

**산출물**: 본 문서.
**판정**: (B) 사전회의 의무.
**도출 건수**: 0 (회의적 압박 + 위험 매트릭스만, 수식 0줄, 파라미터 0개, 유도 경로 0).
**[최우선-1] 준수**: 확인.
**다음 단계**: 사전회의 (별도 Lxx 세션) — A7-1 R1~R8 명세 의무 + blind protocol 실행, A7-2 / Path 3 (B) 병행.
