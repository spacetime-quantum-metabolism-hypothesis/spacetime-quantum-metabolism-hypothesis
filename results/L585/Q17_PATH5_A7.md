# L585 — Q17 단독 5번째 path 탐색 (4-pillar 외부 새 axiom A7)

**작성일**: 2026-05-02
**목적**: 4-pillar 외부에 새 axiom A7 추가 시나리오. Q17 amplitude-locking 동역학 도출의 *방향* 만 검토.
**[최우선-1] 절대 준수**: 수식 0줄, 파라미터 값 0개, 유도 경로 힌트 0개. 방향 + 위험만.
**선행 맥락**: L552 RG 패키지 박탈 (anchor circularity / postdiction 패턴), L578 Path 3 (B) 사전회의, L583 R3+R4 protocol, L584 mass redef 종결.

---

## §1. 6 path 비교 표

| Path | 방향 (이름만) | 외부 import 위험 | hidden DOF 비용 | anchor 의존성 | postdiction 위험 |
|------|---------------|------------------|------------------|----------------|------------------|
| A7-1 | Causality / Unitarity (SR/GR 인과율 본문 등재) | 낮음 (이미 4-pillar SR/GR 과 부분 중복 — 재명세 부담) | 낮음 (axiom statement 만; 새 dynamical DOF 없음) | 낮음 (anchor scale 불필요) | 중간 (인과율은 거의 모든 이론과 호환 — 식별력 부족) |
| A7-2 | Conservation Law (양자단위 보존량, 예: U(1) phase) | 중간 (게이지 구조 외부 import 회피 시) | 중간 (보존량 1개 → 결합 채널 1개) | 낮음 (보존량 자체는 anchor-free) | 낮음 (보존법칙 위반 시 직접 falsifiable) |
| A7-3 | Holographic Entropy Bound (홀로그래피 원리 흡수) | 높음 ('t Hooft / Susskind framework 직수입 위험) | 중간 (bound 1개 → 경계조건 추가) | 높음 (horizon scale anchor 필수 — L552 패턴 재발) | 높음 (entropy bound 는 여러 cosmology 와 호환 — postdict 가능) |
| A7-4 | Non-perturbative Ground State (양자단위 비섭동 진공) | 중간 (QFT vacuum structure import 부분) | 높음 (ground state spec 자체가 다중 파라미터) | 중간 (selection 기준 모호 → anchor 우회 가능하나 미정의) | 중간 (ground state 정의 자유도가 postdict 통로) |
| A7-5 | Anthropic Principle (직접 import) | **매우 높음** ([최우선-1] 위반 직격 — 외부 framework 통째 수입) | 낮음 (statement 1줄) | 없음 (anthropic 은 anchor 없이 작동) | **매우 높음** (anthropic 은 거의 모든 값 postdict — falsifiability 파괴) |
| A7-6 | Generalised Second Law / Bekenstein (열역학 제2법칙 강화) | 중간 (Bekenstein-Hawking framework 부분 import) | 중간 (entropy production 채널 1개) | 높음 (horizon entropy anchor — L552 RG 패키지와 동형 위험) | 중간~높음 (GSL 도 다수 cosmology 와 호환) |

---

## §2. Top-2 Path

**Top-1: A7-2 (Conservation Law)**
- 이유: hidden DOF 비용 중간선, anchor 의존성 낮음, postdiction 위험 낮음 (보존법칙 위반은 직접 검증 가능).
- L552 RG anchor circularity 패턴 회피: 보존량은 scale anchor 없이 정의 가능.
- L549 P3a 박탈 (단일 보조가정 → DOF 추가) 패턴 회피 가능성: 보존량 1개가 결합 채널 1개를 *제약* 하므로, DOF 추가가 아니라 DOF *감소* 로 작동할 여지.

**Top-2: A7-1 (Causality / Unitarity)**
- 이유: 외부 import 위험이 가장 낮음 (4-pillar SR/GR 에 이미 부분 내장). axiom statement 만 추가하므로 dynamical DOF 증가 없음.
- 한계: 식별력이 약해 amplitude-locking 도출의 *방향* 자체는 제공하지만 *유일성* 보장 어려움.

**탈락 그룹**:
- A7-5 anthropic: [최우선-1] 정신 위반 + falsifiability 파괴 → 즉시 배제.
- A7-3 holographic / A7-6 GSL: anchor 의존성 → L552 박탈 패턴 재발 위험 높음.
- A7-4 ground state: hidden DOF 비용 가장 큼 (ground state spec 자체가 다중 파라미터).

---

## §3. 사용자 axiom 추가 권한 활용 시 글로벌 고점 회복 가능성

**전제**: 사용자 새 권한 — axiom 수정/추가/외부 가정 수정 모두 가능.

**가능성 평가**:
- A7-2 Conservation Law 채택 시: 보존량이 amplitude-locking 의 *cross-coupling 채널* 을 자연스럽게 강제하는 방향이라면 (Q17 핵심 요건), L552 박탈 이전 글로벌 고점 *복원* 가능성 존재. 단, R3 (anchor-free) + R4 (postdiction-free) protocol 양쪽을 통과해야 함.
- A7-1 Causality 채택 시: 도출의 방향성은 제공하지만 amplitude *값* 의 유일성 결여 → 글로벌 고점 *부분* 회복.
- 그 외 path: 글로벌 고점 회복 가능성 낮음 (위험 비용 > 회복 이득).

**필수 protocol** (모든 path 공통):
- L583 R3 (anchor-free): 새 axiom 이 외부 anchor scale 도입 금지.
- L583 R4 (postdiction-free): 도출 결과가 관측 데이터 사후 fit 이 아닌 사전 예측이어야 함.
- 4-pillar cross-validation: 새 axiom 이 SR/GR/QM/통계 4-pillar 와 *모순 없이 공존* 확인.
- 단일 에이전트 결정 금지 → 8인 팀 R3+R4 사전회의 의무.

---

## §4. L578 Path 3 (B) vs L585 새 path 비교

| 항목 | L578 Path 3 (Wetterich anchor-free, 4-pillar 내부) | L585 A7-2 (Conservation Law, 4-pillar 외부) |
|------|------------------------------------------------------|--------------------------------------------|
| 4-pillar 위치 | 내부 (anchor 만 제거) | 외부 (axiom 자체 추가) |
| hidden DOF | 낮음 (anchor 제거 → DOF 감소 방향) | 중간 (보존량 1개 추가) |
| 박탈 패턴 재발 위험 | L552 패턴 직접 후속 — 이미 한 번 박탈된 계열의 sibling | L549/L552 패턴 회피 시도 — 새 위험군 |
| R3+R4 통과 가능성 | 중간 (anchor 제거가 R3 부분 충족하나 R4 미정) | 중간 (보존법칙 violation 검증 가능 → R4 유리) |
| 외부 import 비용 | 없음 | 중간 (게이지 구조 회피 명세 필요) |
| 도출 *방향* 명료성 | 높음 (Wetterich 계열 잘 알려진 구조) | 중간 (보존량 → cross-coupling 매핑이 비자명) |

**안전성 결론**:
- *재발 위험* 기준: L585 A7-2 가 더 안전 (L552 박탈 계열 회피).
- *친숙도/방향 명료성* 기준: L578 Path 3 (B) 가 더 안전 (이미 알려진 구조 위에서 anchor 만 조정).
- *글로벌 고점 회복 잠재력* 기준: L585 A7-2 가 약간 우위 (DOF 감소 방향 가능성).

**권장**: 두 path 를 병행 진행하되, 8인 팀 R3+R4 사전회의에서 각각 독립 검증. 단일 path 조기 확정 금지.

---

## §5. 정직 한 줄

> 외부 axiom 추가는 [최우선-1] 정신 위반 위험을 항상 수반하며, A7-2 (Conservation Law) 외 5개 path 는 anchor 의존성 / postdiction / 외부 framework 통수입 / DOF 폭증 중 하나 이상의 박탈 패턴을 재발시킬 수 있고, L578 Path 3 (B) 와 비교했을 때 글로벌 고점 회복은 *가능성* 일 뿐 *보장* 이 아니다.

---

**산출물**: 본 문서.
**도출 건수**: 0 (방향만, 수식 0줄, 파라미터 0개).
**단일 에이전트 결정**: 없음 (top-2 선정은 위험 표 기반 정성 평가 — 최종 선택은 8인 팀 R3+R4 사전회의 의무).
**다음 단계**: 8인 팀이 A7-2 와 L578 Path 3 (B) 병행 R3+R4 protocol 검증 (별도 Lxx 세션).
