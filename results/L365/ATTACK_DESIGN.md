# L365 ATTACK_DESIGN — Spin Foam (LQG) 가 SQT 의 5번째 pillar 가능?

## 0. 정직 한국어 한 줄
스핀 폼은 SQT 의 n 장(場)을 "이산 양자 거품의 통계적 평균"으로 재해석할 수 있는 유일한 비섭동 양자중력 후보지만, n↔spin foam 사전(dictionary)이 아직 존재하지 않으므로 5번째 pillar 승격 전에 그 사전을 먼저 구성해야 한다.

## 1. 배경 — 현재 SQT 4 pillar 구조 (참고)
- P1: BAO/SN/CMB phenomenology (L1~L33 계열)
- P2: 성장(RSD, σ8) 채널
- P3: PPN/Cassini 정합성 (C10k dark-only, disformal)
- P4: 정보-열역학적 소멸항 (n field metabolism postulate)

→ 4 pillar 모두 "거시-효과적" 수준. 미시 양자중력 기원이 비어 있음.

## 2. 핵심 질문
> Spin foam (EPRL/FK 모델, Rovelli-Vidotto 2014) 의 2-complex 양자 진폭이
> SQT 의 n 장(場) 의 미시적 정의를 줄 수 있는가?

세부 질문:
- Q-A. 스핀 폼의 면(face) 양자 (j 표현) 가 n 의 국소 quanta 와 동일시 가능한가?
- Q-B. 대사항(소멸률) 이 spin foam 진폭의 경계항/위상 인자로 자연 발생하는가?
- Q-C. 연속 극한 (large-j / refinement limit) 에서 SQT 의 IDE 형식이 회복되는가?
- Q-D. 스핀 폼의 양자 fluctuation 이 σ8/S8 채널을 새로 열 수 있는가? (background-only 한계 돌파 후보)

## 3. 탐색 방향 (지도 금지 — 방향만)

### 3.1 사전(dictionary) 구성 시도
- LQG 면(face) 양자 / 부피(volume) 연산자 스펙트럼 ↔ n 장의 국소 밀도
- 2-complex 의 vertex amplitude ↔ n 의 시공간 대사 사건(event)
- coherent state (Livine-Speziale) 위상 ↔ n field 의 연속 한계

방향: "상태합(partition sum)에서 거시 연속장이 출현하는 coarse-graining 절차" 를 따라가되, 어떤 결합상수도 미리 고정 금지.

### 3.2 대사항(metabolism) 의 미시 기원 탐색 방향
- spin foam 진폭의 boundary term / Hamiltonian constraint
- causal dynamical triangulation (CDT) 비교군
- group field theory (GFT) 응축(condensate) → cosmology 한도 (Oriti 2016 라인)

방향: GFT condensate cosmology 가 이미 "출현 우주론" 사전(dictionary) 을 제공하므로 진입점으로 우선 고려. 단, 방정식/계수 가져오기 금지 — SQT 팀이 독립 유도.

### 3.3 5th pillar 승격 기준 (사전 정의)
- C-1. n field 의 마이크로 정의가 spin foam state 로부터 ambiguity 없이 유도됨
- C-2. P4 의 소멸항이 spin foam vertex amplitude 의 imaginary part 로 자연 출현
- C-3. 연속 극한에서 P1~P3 의 거시 phenomenology 와 충돌하지 않음
- C-4. 새로운 falsifiable 예측 1개 이상 (예: σ8 채널 또는 GW 분산)

→ C-1, C-2 둘 다 통과해야 "pillar". 하나라도 실패면 "보조 motivation" 등급으로 격하.

## 4. 8인 자율팀 토의 의제 (역할 사전 지정 금지)
- T1. spin foam ↔ n field 사전 후보들을 자유롭게 제안
- T2. 각 후보의 ambiguity (Immirzi parameter, vertex amplitude 선택, measure) 정직하게 나열
- T3. C-1~C-4 4개 기준 각각에 대해 가장 가까운 후보 합의
- T4. 5th pillar 승격 / 보조 motivation / 거부 3-way 표결

토의 결과는 REVIEW.md 에 기록. 수식은 토의 산출물에만 등장 가능 (이 문서에는 금지).

## 5. 본 attack 의 한계
- 본 ATTACK_DESIGN 은 "방향" 만 제시. 어떤 방정식, 결합상수, 수치도 포함하지 않음 (CLAUDE.md 최우선-1).
- spin foam 자체가 비-수렴 / 비-유일 모델군이므로 단일 답 기대 금지.
- L365 는 "탐색 가능성 평가" 이지 "5th pillar 추가" 가 아님. 승격 결정은 별도 세션.

## 6. 산출물
- NEXT_STEP.md — 후속 세션 절차 (사전 후보별 독립 검증)
- REVIEW.md — 8인 팀 토의 / 4인 코드리뷰 결과 정직 기록
