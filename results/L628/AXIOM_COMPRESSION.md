# L628 — Axiom Compression Direction Scan

세션 일자: 2026-05-02
범위: SQT 의 6 axiom (a1-a6) + B1 bilinear ansatz 를 GR-analogue 의 *압축된 원리* 수준으로 줄일 수 있는지에 대한 *방향성* 평가.

[최우선-1] 절대 준수: 본 문서는 수식 0줄, 파라미터 값 0개, 유도 경로 힌트 0건. 압축 angle 의 *명칭과 방향*만 기록한다. 어떤 axiom 이 어떤 axiom 으로 흡수되는지의 *카테고리 매핑*만 서술하며, 그 매핑을 정당화하는 동역학적 도출은 본 문서 범위 밖이다.

---

## §1. 5 압축 angle 표

| # | Angle 이름 | 압축 방향 (카테고리만) | 압축 비율 (명목) | [최우선-1] 위험 | 1차 코멘트 |
|---|---|---|---|---|---|
| 1 | 2-axiom (geometric + balance) | `substrate-geometry` 와 `mass-energy balance` 의 두 카테고리로 흡수. 채널/ansatz 는 부수 도출 후보. | 7 → 2 | 낮음 (카테고리만 기술) | GR 의 `등가원리 + 일반공변성` 구도에 가장 가까움 |
| 2 | 3-axiom (substrate + dynamics + channel) | substrate, dynamics, matter-channel 의 세 축. 기하학적 구조와 ansatz 는 부수. | 7 → 3 | 낮음 | dark-only 채널 선택을 *axiom 수준* 으로 명시 유지 — 정직성 확보 |
| 3 | 1-axiom (single principle) | 단일 원리 (자기조절 dynamics) 로 모든 axiom 을 파생 카테고리로 격하. | 7 → 1 | 중간 (도출 chain 명시 의무 유발) | "유도 가능성" 주장이 곧 [최우선-1] 위반으로 미끄러질 위험 |
| 4 | 0-axiom (bootstrap) | axiom 폐기, self-consistency 만. L604 Bootstrap 와 정합. | 7 → 0 | 높음 (GR 4축 0.8/4 미달, L605) | 형식적 단순성 ↑ 그러나 falsifiability ↓ — 권장 안 함 |
| 5 | Layered (foundational + derived) | 핵심 2~3 + 도출 4~5 를 paper §3 에서 *명시 분리*. 압축이 아닌 *층화* (presentation 레벨). | 형식 7, 표시 2~3 | 매우 낮음 (presentation only) | 가장 안전. 수식/도출 없이 paper §3 재구성만으로 GR-analogue 단순성 인상 회수 |

압축 비율 의 분모 7 = a1-a6 (6) + B1 (1). 분자는 *명목* 핵심 axiom 수이며, 도출 chain 이 검증되기 전에는 hidden axiom 이 잠복할 수 있다.

---

## §2. Top-2 angle 선정 (안전 + 효과)

선정 기준: (i) [최우선-1] 위반 위험 낮음, (ii) GR 4축 (단순성/falsifiability/coherence/economy) 에 실질 기여, (iii) hidden DOF 정직 disclosure 강화.

**Top-1: Angle 5 (Layered presentation)**
- 위반 위험 *매우 낮음* — 압축이 아닌 *층화* 이므로 새 도출 의무 없음.
- 효과: paper §3 가 "핵심 2~3 + 도출 4~5" 로 재구성되며, 독자에게 GR analogue 의 단순성 인상을 *형식적으로* 전달.
- 단점: 실제 axiom 수는 변하지 않음 → "진정한 압축" 은 아님. 정직성 확보가 곧 한계.

**Top-2: Angle 1 (2-axiom, geometric + balance)**
- 위반 위험 *낮음* — 카테고리 수준 매핑만 본 문서에 적힌다면 안전.
- 효과: SQT 가 GR 의 2 원리 구도와 *구조적 친화성* 을 가짐을 시사. paper §3 의 단순성 +α.
- 단점: a6 (dark-only) 와 B1 (bilinear) 의 흡수 정당화가 후속 세션에서 동역학적 도출을 요구. 그 단계에서 [최우선-1] 위반 위험이 *상승* 한다 — 별도 가드가 필요.

권장: **Angle 5 를 즉시 채택**, Angle 1 은 *후속 가드 세션* 에서 도출 가능성만 별도 검토.

---

## §3. GR 4축 충족도 (단순성 +α 가능?)

L605 의 GR 4축 평가에서 SQT 는 단순성 축에서 GR 대비 열세였다. 본 §3 은 5 angle 채택 시 *형식 단순성* 이동 방향만 기록한다.

| Angle | 단순성 | falsifiability | coherence | economy | 종합 방향 |
|---|---|---|---|---|---|
| 1 (2-axiom) | ↑↑ | → (도출 위험 의존) | ↑ (압축이 일관성 강조) | ↑ | 잠재적 +α, 위험 부담 |
| 2 (3-axiom) | ↑ | → | ↑ | → | 중립적 +0.5 |
| 3 (1-axiom) | ↑↑↑ (명목) | ↓ (검증 가능 항목 흐려짐) | ↓ (도출 chain 미공개) | ↑ | -α 위험 더 큼 |
| 4 (0-axiom) | 형식 ∞ | ↓↓ (L605) | ↓ | ↓ | 권장 안 함 |
| 5 (Layered) | ↑ (presentation) | → | ↑ | ↑ | 안전 +α |

`↑` 는 정성적 방향 표시이며 정량 점수는 본 문서 범위 밖.

---

## §4. paper §3 재구성 가능성

현행 paper §3 는 a1-a6 + B1 을 평면적으로 나열. Angle 5 채택 시 §3 재구성 *방향*:

- §3.1 — *핵심 원리* (2~3 항) 만 서술. SQT 의 substrate-balance 또는 substrate-dynamics-channel 카테고리 표제.
- §3.2 — *도출/부수 axiom* (4~5 항) 을 별도 절에서 명시. 도출 chain 이 *현재 미완* 임을 정직 disclosure.
- §3.3 — *hidden DOF disclosure*. axiom 수 ≠ 자유도 수 임을 명시. L569/L591 phenomenology pivot 와 정합.

이 재구성은 코드/시뮬레이션 변경을 수반하지 않으며, 논문 본문 presentation 만 변경. 따라서 본 세션에서 *결정* 할 사안 아니고, 8인 팀 Rule-A 합의 안건으로 이관 권장.

---

## §5. 정직 한 줄

> SQT 는 *형식적 압축* (Angle 5) 으로 GR-analogue 단순성 인상을 회수할 수 있으나, *실질적 압축* (Angle 1~3) 은 도출 chain 이 [최우선-1] 가드 안에서 검증되기 전까지 hidden DOF 손실 위험과 분리 불가능하다.

---

## §6. CLAUDE.md 정합 체크

- [최우선-1] 수식 0줄: 준수.
- [최우선-1] 파라미터 값 0개: 준수.
- [최우선-1] 유도 경로 힌트 0건: 준수 (카테고리 매핑만, 동역학적 도출 없음).
- [최우선-2] 단일 에이전트 결정 금지: 본 문서는 *방향 스캔* 이며 Angle 채택 결정은 8인 팀 Rule-A 합의로 이관.
- LXX 공통 원칙: 역할 사전 지정 없음, 시뮬레이션 변경 없음.

다음 단계 (권장):
1. 8인 팀 Rule-A 에 Angle 5 (Layered) 채택 안건 상정.
2. Angle 1 (2-axiom) 은 별도 가드 세션에서 *도출 가능성만* 평가, 동역학적 유도는 [최우선-1] 위험으로 본 시점 보류.
