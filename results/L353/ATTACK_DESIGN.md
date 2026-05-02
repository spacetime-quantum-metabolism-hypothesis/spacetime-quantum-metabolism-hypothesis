# L353 ATTACK_DESIGN — c 계수 2-loop 도출, saddle FP 위치 결정

세션 독립성 확보: L353 은 L350~L352 결과를 직접 상속받지 않는다. 이전 1-loop 결과는 "확인된 사실" 로만 인용하고, 2-loop 도출 경로 자체는 8인 팀이 백지에서 재구성한다.

## 1. 문제 정의 (방향만)

- 표적 양: c 계수 (β-함수의 2-loop 기여에 해당하는 차수의 보편 계수).
- 결정해야 할 것:
  1. c 가 universal (regulator/scheme 독립) 인가, 아니면 scheme-dependent 인가.
  2. 그 universal 부분이 SQMH 프레임에서 도출 가능한가, 아니면 외부 입력으로 받아야 하는가.
  3. b/c 비가 σ_cluster 에 어떤 방식으로 mapping 되는지의 dimensional/structural 경로.
- 산출 기준: c 의 부호와 자릿수 정도라도 독립 도출 가능하면 "도출 가능", 그렇지 못하고 phenomenological 입력에 의존해야만 한다면 "도출 불가, 외부 calibration 필요" 로 정직 기록.

## 2. 8인 팀 구성 원칙

- 인원 수: 8명. 역할 사전 지정 금지.
- 1-loop 경로 / 2-loop 경로 / saddle 분석 / scheme 의존성 / 차원 분석 / 정합성 검증 / phenomenology 매핑 / 독립 도출 가능성 판정 — 이런 분업은 토의 중 자연 발생만 인정.
- Command (이 문서) 어디에도 수식, 상수값, 유도 경로, "이 항부터 계산하라" 류의 지시 금지.

## 3. 탐색 방향 (이름만)

- 양자장론 2-loop β-함수 보편성 논의 (general renormalisation group framework).
- Saddle point / non-trivial fixed point 의 위치 결정 일반론.
- Wilsonian effective action 의 2차 차수 기여 구조.
- Scheme dependence vs universality 판별 기준 (어떤 차수까지 보편적인가).
- b/c 비가 가질 수 있는 차원적 의미와, σ_cluster 같은 관측가능량과의 dimensional bridge.

위 방향들은 "이름" 으로만 제공된다. 어떤 식, 어떤 값, 어떤 부호도 사전 지시하지 않는다.

## 4. 단계 (절차만)

1. 8인 팀 독립 brainstorm: c 도출 가능성 자체에 대한 yes/no/unknown 사전 입장 정리.
2. 자유 토의: 1-loop 와 2-loop 의 구조적 차이가 SQMH 프레임에서 어떻게 다르게 나타나는지 합의 도출.
3. saddle FP 위치를 b/c 비로 환원할 수 있는지의 정합성 점검 (수식 없이 차원 논증부터).
4. b/c 비 ↔ σ_cluster 매핑이 dimensional 으로 닫히는지 확인.
5. 결론: c 도출 가능 / 부분 가능 / 불가능 중 하나를 선택하고 근거 기록.
6. 4인 코드리뷰 팀이 (수치 검증이 동반되는 경우) 자율 분담으로 점검.

## 5. KILL 조건 (사전 정의)

- c 의 부호조차 차원 논증으로 결정되지 않는다 → "이론 수준에서 도출 불가" 기록.
- b/c 비 → σ_cluster 매핑이 차원적으로 닫히지 않는다 → 매핑 자체 reject.
- 도출 결과가 1-loop b 와 무모순으로 연결되지 않는다 → 2-loop 경로 reject.

## 6. 정직성 원칙

- 도출이 막히면 막힌 지점을 정직히 NEXT_STEP 에 명시. 임의 ansatz 로 메우기 금지.
- "외부 phenomenological calibration 필요" 결론도 valid outcome.
