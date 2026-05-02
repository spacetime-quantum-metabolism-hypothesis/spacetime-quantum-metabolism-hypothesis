# L587 — A7-2 (Conservation Law axiom) 8인 회의적 검증 (Rule-A)

**작성일**: 2026-05-02
**대상**: L585 §2 Top-1 (A7-2 Conservation Law).
**모드**: 회의적 reviewer 압박. 좋은 점 생략. 결함만 기록.
**[최우선-1] 절대 준수**: 수식 0줄, 파라미터 값 0개, 유도 경로 힌트 0개. 위험명 + 방향만.
**선행**: L549 P3a 박탈, L552 anchor circularity 박탈, L578 Path 3 (B) 사전회의, L583 R3+R4 protocol, L585 5th-path 도출.

---

## §0. 8인 회의적 reviewer 압박 요약

8인은 사전 역할 배정 없이 R1~R8 8개 축을 자율 분담. 아래는 자유토의 후 압박 결론.

---

## §1. R1 — 보존량의 정체 (Noether origin)

**압박**:
- L585 표는 보존량의 *예시* 로 "U(1) phase" 만 한 줄 적어두었을 뿐, 어떤 **물리적 conserved current** 인지 미정의. Noether 정리에 의한 자동 도출을 주장하려면 그에 대응하는 **연속 대칭** 을 SQT 본문에서 식별해야 하는데, 본문에는 4-pillar (SR/GR/QM/통계) 외 별도 연속 대칭이 명시되어 있지 않음.
- 만약 새 연속 대칭을 도입한다면 그 자체가 추가 hidden DOF — "보존량 1개 추가" 라는 L585 §1 표 평가가 **과소평가**. 대칭 + 그 표현공간 + coupling channel 까지 묶음 비용.
- "양자단위 phase" 라는 phrasing 은 QM-pillar 의 글로벌 phase (관측 불가능, 물리 무영향) 와 게이지 phase (국소화 시 게이지장 강제) 사이를 구분하지 않음. 어느 쪽이든 SQT 외부 구조 import 또는 새 DOF 발생.

**판정**: R1 명확히 미해결. axiom statement 단계에서 이미 "어떤 대칭의 Noether 보존량인가" 가 공란.

---

## §2. R2 — 4-pillar 정합성 (특히 Z_2 SSB pillar 와 충돌)

**압박**:
- 4-pillar 중 **Z_2 SSB pillar** 는 *이산* 대칭의 자발 깨짐을 이미 axiom 화. A7-2 가 *연속* 보존량을 추가하려는 순간, 두 pillar 간 위상이 상이한 대칭 구조를 동시에 axiom 화해야 함 — 양립 자체는 형식적으로 가능하지만, **어느 것이 더 근본적인가** 의 우선순위 미정의.
- Z_2 깨짐 뒤 남은 잔존 대칭이 A7-2 의 보존량과 어떻게 정합하는지 명세 부재. SSB 가 A7-2 보존량을 깨는 시나리오면 "보존" 자체가 cosmic-only / late-time-only 로 regime 화됨 → R7 (3-regime universal) 직격.
- SK pillar (Schwinger-Keldysh, 비평형) 는 보존량을 source/sink 로 변형 가능. Wetterich pillar (RG flow) 는 scale 에 따라 effective conserved current 가 변할 수 있음 — A7-2 의 "보존" 이 어느 RG scale 에서의 보존인지 무명세.
- Holographic pillar 와는 boundary current 정합성 추가 검증 필요. 4-pillar 모두에 대해 *동시에* 정합 명세는 L585 §1 의 "낮은~중간" 평가가 감추고 있는 부담.

**판정**: R2 4-pillar 동시 정합성은 미증명. 특히 Z_2 SSB 와 본질적 긴장.

---

## §3. R3 — Q17 도출 진정성 (cross-coupling = 동역학 vs normalization)

**압박**:
- L585 §2 Top-1 사유 중 핵심: "보존량이 amplitude-locking cross-coupling 채널을 자연스럽게 강제". 그러나 "보존량이 결합을 강제" 와 "boundary 조건이 normalization 으로 fix" 는 외형이 매우 유사 — L578 R3 가 이미 지적한 L513 §6.5(e) "E(0)=1 정규화 귀결" 패턴 재발 위험.
- Δρ_DE 와 Ω_m 의 cross-coupling 이 보존량의 *동역학적 결과* 인지 검증하려면, 보존량을 변경했을 때 amplitude 가 *동역학적으로* 다른 값으로 흘러야 함. 단순히 "보존량을 부여 → 합이 고정 → amplitude 가 normalization 으로 결정" 패턴이면 Q17 부분달성 (L6 K20 기준 amplitude-locking 동역학 도출 미충족) 그대로.
- 반증 protocol (예: 보존량 위반/변경 시 amplitude 가 다른 값으로 이동하는지의 사전 예측) 이 axiom 단계에서 명세되어 있지 않음 — R4 (postdiction-free) 통로 약함.

**판정**: R3 Q17 동역학 도출 진정성은 **현재 axiom 명세로는 검증 불가**. normalization 귀결 위험은 L513 §6.5(e) 와 동형.

---

## §4. R4 — 외부 import ([최우선-1] 위반 위험)

**압박**:
- "U(1) phase" 라는 예시는 표준 게이지 이론에서 곧장 빌려온 용어. SQT 본문에서 자체 도출되지 않은 채 reviewer 가 "예시" 로 언급한 시점에서 이미 외부 framework 의 *발상* 이 도입됨. [최우선-1] "지도 절대 금지" 의 정신적 위반에 해당될 수 있음 — 명시적 수식 없어도 "어떤 종류의 보존량을 찾을지" 의 *방향* 이 외부에서 주입.
- 자체 도출 가능성 주장 (4-pillar 만으로 보존량 induced) 은 현재 입증 없음. 4-pillar 본문에 연속 대칭이 명시 안 된 상태에서 보존량을 자체 도출하려면 추가 axiom 또는 추가 구조 필요 — 결국 hidden DOF 증가.
- L585 §1 의 "외부 import 위험: 중간 (게이지 구조 외부 import 회피 시)" 평가는 *회피 가능성* 만 적시했을 뿐, *회피 방법* 미명세. 회피 방법이 없으면 "중간" 이 아니라 "높음" 으로 재평가 필요.

**판정**: R4 외부 import 위험 L585 §1 평가는 **과소평가**. 자체 도출 경로 명세 없으면 [최우선-1] 위반 가능성 유의.

---

## §5. R5 — Conservation 정의의 모호성 (hidden DOF)

**압박**:
- "무엇이 보존되는가" 가 미정의 상태. 후보: energy-momentum / electric-charge-analog / quantum-phase / entropy / particle-number / something-else. 후보군 자체가 다수라는 사실이 **모호성 = hidden DOF +1 이상**.
- 후보 선택은 어느 4-pillar 와 정합하는지에 따라 달라짐 (R2 와 직결). 선택 기준 자체가 anchor 또는 관측 적합성에 의존하면 R8 (anchor circularity) 직격.
- 보존량의 "양" 만 axiom 화 하고 "종류" 를 미루는 phrasing 은 axiom 자체의 식별력 부재. 식별력 부재는 5번째 path 의 핵심 약점.

**판정**: R5 정의 모호성은 axiom 채택 전에 *반드시* 해소해야 함. 미해소 시 hidden DOF 비용은 L585 §1 표의 "중간" 보다 큼.

---

## §6. R6 — 관측 가능성 (직접 vs hidden current)

**압박**:
- 보존된 current 가 직접 관측 가능하지 않으면 (hidden conserved quantity), 보존법칙 위반은 영원히 falsification path 가 닫힘 — L585 §1 의 "postdiction 위험: 낮음 (보존법칙 위반 시 직접 falsifiable)" 주장이 무효화됨.
- 직접 관측 가능한 current 라면 그것은 이미 표준모형 / 우주론 관측에서 측정된 보존량 (energy-momentum, baryon number, lepton number 등) 일 가능성 — 외부 framework 직접 import (R4) 와 동치.
- "관측 가능 + 자체 도출" 은 동시에 만족하기 어려운 조합. 두 조건 중 하나는 양보해야 하며, 어느 쪽을 양보하든 다른 R 항목으로 비용 전가.

**판정**: R6 hidden vs observable trade-off 미해결. L585 §1 의 postdiction risk 평가는 **observable 가정에 의존** — hidden 인 경우 평가 즉시 악화.

---

## §7. R7 — 3-regime universal 적용성

**압박**:
- A7-2 가 cosmic / cluster / galactic 3-regime 모두에 같은 보존량을 강제하는지 미명세. regime 별로 effective conserved current 가 달라지면 (RG flow 또는 환경 의존), regime 별 coupling 추가 → **hidden DOF +2 이상**.
- 특히 galactic regime 의 SQMH 유체 흐름은 비평형 (SK pillar) 색채가 강함 — 비평형에서 "엄밀 보존" 은 통상 source/sink 가정 추가 필요. 이 가정 자체가 axiom 추가.
- regime universal 보존량을 가정하면 cluster 스케일 (S_8 tension regime) 에서 제약이 너무 강해 기존 L5/L6 winner 패턴과 충돌 가능. universal 포기 시 식별력/예측력 약화.

**판정**: R7 universal 정합성 미보장. universal vs regime-specific 양 갈래 모두 비용 큼.

---

## §8. R8 — Anchor circularity 재발 위험

**압박**:
- "양자단위 보존량" 의 단위가 어느 scale 에서 정의되는가 미명세. 만약 보존량의 정의 또는 normalization 이 Λ_obs / σ_8 / a₀ / r_d 등 관측 anchor 에 의존하면 L552 RG 패키지 박탈 패턴 직접 재발.
- L585 §1 표의 "anchor 의존성: 낮음 (보존량 자체는 anchor-free)" 은 *원리적* anchor-free 만 평가. *실제 정량화* 단계에서 anchor 가 슬그머니 들어올 통로 (예: cross-coupling 강도의 normalization) 가 봉쇄되어 있는지 미증명.
- L552 의 박탈 사유는 "anchor 가 없으면 정량화 불가, 있으면 circularity" 양날의 칼이었음. A7-2 가 같은 칼 위에 서 있지 않다는 증명 부재.

**판정**: R8 anchor circularity 회피는 *주장* 만 있고 *증명* 없음. L552 박탈 패턴 재발 위험 잠재.

---

## §9. A7-2 vs Q17 Path 3 (Wetterich anchor-free) 안전성 비교

| 축 | A7-2 (Conservation Law) | Path 3 (Wetterich anchor-free, L578) |
|---|---|---|
| R1 (도출 기원) | Noether origin 미정의 | RG-flow 기원, 4-pillar 내부 |
| R2 (4-pillar 정합) | Z_2 SSB 와 위상 긴장 | 4-pillar 내부 — 정합성 자명 |
| R3 (동역학 vs normalization) | normalization 귀결 위험 (L513 §6.5(e) 동형) | anchor 제거가 normalization 우회 — 부분 유리 |
| R4 (외부 import) | "U(1)" 예시 자체가 외부 향기 | 외부 import 0 |
| R5 (정의 모호성) | 보존량 "종류" 미정 → hidden DOF | RG flow 자체는 4-pillar 내 정의됨 |
| R6 (관측가능성) | observable vs hidden trade-off 미해결 | observable proxy (RG scale) 명료 |
| R7 (3-regime universal) | regime universal 미보장 | RG flow 가 자연스럽게 multi-scale |
| R8 (anchor circularity) | 회피 *주장* 만 — 증명 부재 | L552 의 sibling — *명시적* 회피 protocol 필요 |

**비교 결론 (회의적 관점)**:
- A7-2 는 R1/R2/R4/R5 에서 **새로운** 미해결 부담 (특히 외부 import 향기와 정의 모호성).
- Path 3 (B) 는 L552 sibling 이라는 **이미 알려진** 위험 (R8) 1축에 집중되어 있고, 그 위험은 명시적 protocol (anchor-free 명세) 로 봉쇄 시도가 진행 중.
- "새로운 4축 미해결" vs "알려진 1축 집중" 비교 시 **Path 3 (B) 가 더 안전**. L585 §4 의 "재발 위험 기준 A7-2 우위" 결론은 R1/R2/R4/R5 를 과소평가한 결과.
- 단, Path 3 (B) 도 R3 (anchor-free) + R4 (postdiction-free) 양 protocol 통과 전까지 자동 안전 아님.

---

## §10. 최종판정

### 결론: **(B) 사전회의 의무**

**근거**:
- (A) Round 11 즉시 진입은 R1/R2/R3/R4/R5/R8 6축에서 미해결 잔존 — 부적격.
- (C) 자동 박탈은 과도. axiom 자체의 *완전한* 모순은 발견되지 않음. R6/R7 은 명세 보강으로 해결 가능성 존재.
- 따라서 (B) 사전회의 의무. 다만 사전회의는 **단순 통과식이 아니라 R1/R4/R5 우선 해소 조건부**.

### (B) 진입 조건 (모두 만족 시 사전회의 자격)

1. **R1 해소**: A7-2 보존량의 Noether 기원 — 어느 4-pillar 내부 *연속 대칭* 에서 도출되는지 명세. 새 대칭 도입 시 그 비용을 hidden DOF 합산에 명시.
2. **R4 해소**: "U(1) phase" 예시 폐기 또는 SQT 본문 자체 도출 경로 명세. 외부 게이지 framework import 회피 방법 (회피 *가능성* 이 아닌 *방법*) 명문화.
3. **R5 해소**: 보존량의 "종류" 확정 (energy-momentum / charge-analog / phase / etc 중 단일 선택 + 사유). 후보 다수 유지는 hidden DOF 누적.
4. **R3 protocol**: amplitude-locking 도출이 normalization 귀결이 아닌 *동역학적 결과* 임을 사전 검증할 반증 protocol (보존량 변경 시 amplitude 이동 예측) 명세.
5. **R8 protocol**: 정량화 단계의 anchor 무유입 증명 (L552 박탈 패턴 회피).
6. **R2 protocol**: Z_2 SSB pillar 와의 위상 정합 — SSB 후 잔존 대칭과 A7-2 보존량의 관계 명세.
7. **R7 검토**: 3-regime universal vs regime-specific 명시 — universal 시 SK 비평형에서의 source/sink 가정 추가 비용 합산.
8. **8인 R3+R4 사전회의**: 단일 에이전트 결정 금지. 위 1~7 조건을 8인이 자율 분담 검토 후 합의.

### A7-2 vs Path 3 (B) 권장

- **현 시점 권장**: **Path 3 (B) 우선**, A7-2 는 위 조건 1~7 충족 후 병행.
- 이유: Path 3 (B) 는 **알려진 1축 위험 (R8 anchor circularity, L552 sibling)** 에 집중되어 명시적 protocol 로 봉쇄 진행 중. A7-2 는 **R1/R2/R4/R5 4축의 미해결 부담** 을 한꺼번에 안고 있어 Round 11 결과 전 axiom 단계 정리 비용이 큼.
- L585 §4 "재발 위험 기준 A7-2 우위" 평가는 본 L587 검증으로 **부분 무효화**. "친숙도/방향 명료성" 기준은 여전히 Path 3 (B) 우위.

---

## §11. 정직 한 줄

> A7-2 (Conservation Law) 는 axiom statement 단계에서 R1 (보존량의 Noether 기원), R2 (Z_2 SSB pillar 와 위상 정합), R4 ("U(1) phase" 예시의 외부 import 향기), R5 (보존량 종류 미정 = hidden DOF), R8 (정량화 단계 anchor 무유입 증명 부재) 5축이 미해결이며, L585 §1 표의 "hidden DOF 중간 / anchor 의존성 낮음 / postdiction 낮음" 평가는 이 5축을 과소평가한 결과로 — Round 11 즉시 진입은 부적격, (B) 사전회의 의무 + 진입 조건 7항 충족 + 8인 R3+R4 사전회의 합의 전까지 axiom 채택 보류, 동일 시점 비교에서는 L578 Path 3 (B) 가 더 안전하다.

---

**산출물**: 본 문서.
**판정**: **(B) 사전회의 의무 — 진입 조건 7항 충족 후**.
**[최우선-1] 준수**: 수식 0줄, 파라미터 값 0개, 유도 경로 힌트 0개.
**단일 에이전트 결정**: 없음 (본 문서는 회의적 reviewer 압박 기록 — 최종 axiom 채택 결정은 8인 사전회의 의무).
**다음 단계**: (i) §10 진입 조건 1~7 작업, (ii) 충족 시 8인 R3+R4 사전회의, (iii) Path 3 (B) 와 병행 — 단, A7-2 단독 우선 진행 금지.
