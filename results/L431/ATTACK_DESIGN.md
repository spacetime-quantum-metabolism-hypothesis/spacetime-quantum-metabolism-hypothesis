# L431 — ATTACK_DESIGN: PARTIAL #3 (4-pillar convergence) ↔ axiom 4 OPEN 종속

**Loop**: L431 (independent)
**Date**: 2026-05-01
**Scope**: paper/base.md §2.4 (4 microscopic pillars / "convergence" PARTIAL claim) ↔ §2.5 (axiom 4 5th-pillar OPEN) ↔ §6.1.1 row 11 (axiom 4 발현 metric 미시 OPEN) ↔ §6.1.2.1 (NOT_INHERITED chained root cause).
**Predecessors (정황)**: L320, L370, L385, L388, L389, L390, L400, L401, L404, L420, L427 (Dual foundation 제안), L432.
**정직 한 줄**: 본 design 은 "§2.4 4-pillar convergence 가 PARTIAL 등급인 *원인*이 axiom 4 OPEN 에 종속되어 있다는 reviewer 의 자연스러운 공격 vector" 만 매핑하며, 어떤 수식·파라미터 값·유도 경로 힌트도 도입하지 않는다 (CLAUDE.md [최우선-1] 준수).

---

## 0. 8인팀 자율 분담 원칙 (CLAUDE.md L17 이후)

본 attack design 은 8인팀의 토의에서 *자연 발생한* 분업의 결과만 기록한다. 사전 역할 지정 없음. 8인은 자유롭게 (i) "convergence" 의 의미, (ii) PARTIAL 등급의 채널, (iii) axiom 4 OPEN 이 그 등급에 *얼마나* 책임이 있는가의 세 면을 자율 분담하여 검토한다.

---

## 1. 공격 표적 정의

### 1.1 PARTIAL #3 의 본문 위치

paper/base.md §2.4 는 4 미시 축 (Schwinger-Keldysh / Wetterich FRG / Holographic dimensional bound / Z₂ SSB) 을 나열하고 §2.6 에서 "미시 4 축의 *상호 일관성* (동일 Lagrangian 도출 가능성) 부분 — 본문 1단락 명시 필요" 라는 caveat 를 단다. §6.1.1 row 11 은 "axiom 4 발현 metric 미시 OPEN" 을 OPEN 으로 분류하며, §6.1.2.1 는 NOT_INHERITED 8건 중 5건이 axiom 4 5번째 축 미결정에 *연쇄* 종속됨을 명시한다.

**Reviewer 의 자연 합성**: §2.4 의 "4 축 convergence" 는 PARTIAL 이며, PARTIAL 의 *주된 원인* 은 axiom 4 OPEN — 즉 4 축이 동일한 micro Lagrangian 으로 수렴하는지 확인할 수 있는 *5번째 (메소 ↔ 미시) 다리* 가 비어 있다.

### 1.2 핵심 공격면 (D 시리즈)

| ID | 공격 | 채널 |
|----|------|------|
| **D1** | "§2.4 가 4 축을 *나열* 만 하고 *수렴* 을 보이지 않는다. PARTIAL 등급은 사실상 'convergence 미입증' 의 완곡 표현 아닌가?" | R1 (theorist) |
| **D2** | "convergence PARTIAL 의 원인 중 axiom 4 OPEN 이 차지하는 *비중* 이 §2.4 본문에 정량 분리되어 있지 않다. 다른 원인 (1-loop hierarchy, conformal anomaly) 과 섞여서 '함께 future work' 로 미뤄지면 reviewer 는 어느 caveat 가 close 되는지 추적 불가." | R3 (statistician) |
| **D3** | "§2.5 의 'Causet meso 4/5 조건부 PASS' 가 §2.4 의 convergence 등급에 *어떻게* 반영되는가? PASS 면 PARTIAL → PASS_BY_INHERITANCE 로 격상되어야 하지 않는가? 격상이 일어나지 않는 이유 미명시." | R1 |
| **D4** | "L427 Dual foundation (두 micro 후보의 공동 등재) 가 채택되면 axiom 4 OPEN 이 *부분 close* 된다는 시나리오가 본문에 fold-in 안 되어 있다. Dual 채택 시 §2.4 등급 변화 경로 (PARTIAL → PASS_BY_INHERITANCE 부분) 가 미공개." | R1 + R3 |
| **D5** | "Dual foundation 시나리오의 cost (두 micro 의 *상호* 일관성 추가 부담) 가 vs single 5번째 축 채택 (Causet 또는 GFT 단독) cost 와 비교 안 됨. 'Dual 이 더 약한 commitment 라 안전' 인가, '두 부담을 동시에 진다' 인가 모호." | R1 |
| **D6** | "PARTIAL 등급의 정직 정의 (paper §6.5(e) 의 11-enum) 는 'caveat 명시' 인데, §2.4 caveat 가 §2.6 에서 *별도 절* 로 분리되어 있다. reviewer 는 §2.4 만 읽고 PARTIAL 임을 알아채지 못할 수 있다." | R2 (observer) |
| **D7** | "§2.4 row 2 의 Wetterich FRG '★★⅓ algebraic only' 는 그 자체로 PARTIAL. 이 PARTIAL 이 axiom 4 OPEN 과 *독립* 인가, *종속* 인가? 종속이면 axiom 4 close 시 자동 PASS, 독립이면 별도 future work. 본문 분리 미실시." | R1 |
| **D8** | "§6.1.2.1 의 'GFT 등재 시 5+ claim 회복' 주장과, §2.4 의 '4 축 convergence PARTIAL' 사이의 인과 화살표가 한 방향만 그려져 있다. *Causet* 등재 시 §2.4 등급은 어떻게 바뀌는가? 두 후보의 §2.4 영향 차이 미분리." | R1 + R3 |

### 1.3 reviewer 별 우선순위

- **R1 (theorist)**: D1, D3, D4, D5, D7, D8 — convergence 의미 + axiom 4 종속 메커니즘 + Dual cost
- **R2 (observer)**: D6 — 본문 가독성 / 등급 추적성
- **R3 (statistician)**: D2, D4, D8 — 종속 비중 정량 분리 + 등급 변화 경로

---

## 2. 4-pillar convergence PARTIAL 의 axiom 4 OPEN 종속 *방향* (정성, 수치 미부여)

8인팀 토의에서 자율 분담된 정성 검토 결과만 기록. 정량 비중 분리는 NEXT_STEP.md 의 "Dual foundation 채택 시 부분 close" 시나리오로 넘긴다.

### 2.1 종속 채널 매핑 (★ 화살표 방향만)

| 종속 채널 | 방향 (axiom 4 OPEN → §2.4 PARTIAL) |
|-----------|------------------------------------|
| **C-α** | axiom 4 의 micro origin 부재 → 4 축이 *공통 Lagrangian* 으로 수렴하는지 확인 불가 → §2.6 caveat 1 |
| **C-β** | 미시 다리 부재 → SK / FRG / Holographic 사이의 *cross-channel* 정합성 비교가 phenomenology 수준에 머물러 §2.4 동급 PARTIAL |
| **C-γ** | NOT_INHERITED 5건 (§6.1.2.1) 의 회복 경로가 axiom 4 5번째 축 결정에 매여 있어 §2.4 가 *future-conditional* PARTIAL |

### 2.2 *독립* 잔여 채널 (axiom 4 close 와 무관하게 PARTIAL 유지 가능)

- 1-loop quadratic hierarchy (§2.6)
- Conformal anomaly 의 Λ_obs 대비 무시 가능성 (§2.6)
- Wetterich β-function 계수의 algebraic-only 한계 (§2.4 row 2)

→ 이 잔여 채널은 axiom 4 OPEN close 와 *분리* 되어야 §2.4 등급 변화가 정직.

---

## 3. Dual foundation (L427) 시나리오의 공격면 흡수 능력 *방향*

**가설** (수식 부재): L427 이 두 micro 후보를 *공동* 등재하는 구조라면, axiom 4 OPEN 의 *origin* 채널 (C-α, C-β) 일부가 close 되어 §2.4 PARTIAL 의 종속분 → PASS_BY_INHERITANCE 부분 격상이 *방향성* 으로 가능.

| D ID | Dual 시나리오 흡수 가능성 | 방향 |
|------|---------------------------|------|
| D1 | 부분 흡수 | 두 후보의 cross-check 자체가 convergence 증거의 *부분 substitute* |
| D2 | 흡수 안 됨 | "비중 분리" 본문 명시는 별도 작업 (NEXT_STEP) |
| D3 | 부분 흡수 | Dual 시 4/5 조건부 PASS 의 의미 재정의 가능 |
| D4 | 직접 해당 | Dual 채택이 곧 D4 의 답변 |
| D5 | 흡수 안 됨 | Dual cost 정량 비교는 별도 분석 |
| D6 | 흡수 안 됨 | 본문 가독성은 §2.4 절 자체 수정 (4인팀 작업) |
| D7 | 흡수 안 됨 | Wetterich algebraic-only 는 axiom 4 OPEN 과 독립 |
| D8 | 부분 흡수 | 두 후보의 §2.4 영향이 Dual 에서 *공통* 로 묶이므로 차이 분리 부담 감소 |

→ Dual 채택은 D1, D3, D4, D8 의 *부분* close, D2/D5/D6/D7 은 *별도* 작업 필요.

---

## 4. 정직 정량화 의무 (본 design 단계 미실행, NEXT_STEP 으로 이관)

본 attack design 은 *방향* 만 제공. 다음 항목은 NEXT_STEP.md 에서 다룬다.

1. axiom 4 OPEN 종속분 (C-α, C-β, C-γ) vs 독립 잔여분 (1-loop, anomaly, Wetterich algebraic) 의 *상대 비중 분리* 본문 문장.
2. Dual foundation 채택 시 §2.4 등급 변화 *경로 명시* (PARTIAL → PARTIAL\* with footnote, 또는 PARTIAL → PASS_BY_INHERITANCE 부분).
3. §2.4 절 자체의 본문 가독성 수정 (D6 응답).

---

## 5. 본 design 의 [최우선-1] 자체 점검

- 수식 0줄 ✓
- 파라미터 값 0개 ✓
- "이 방정식을 써라" 류 0건 ✓
- 과거 결과 (L14/L22) 의 이론 형태 차용 0건 ✓
- 방향·물리/수학 분야 이름·공격 channel 이름만 사용 ✓
