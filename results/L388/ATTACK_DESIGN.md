# L388 ATTACK_DESIGN — 2-loop n self-energy + setting-sun

세션: L388 (독립)
날짜: 2026-05-01
선행: L386~L387 (1-loop n self-energy, c 계수 first-principle 도출 미달)
원칙: CLAUDE.md 최우선-1 적용 — 방향만, 수식/파라미터/유도 경로 금지.

## 1. 핵심 질문 (Q-stmt)

SQT 효과 라그랑지언의 c 계수가 1-loop 수준에서 first-principle 로 닫히지 않았다면,
**2-loop n self-energy 전개에서 닫힐 수 있는가?**

판정 기준 (이 세션에서 결정해야 할 것):
- (a) 2-loop 가 c 계수에 새로운 독립 제약을 주는가
- (b) 그 제약이 1-loop counterterm 구조와 모순 없이 흡수되는가
- (c) renormalization 이후에도 c 가 자유 파라미터로 남는가

(a)~(c) 중 하나라도 명확한 No 로 닫히면 결과 — 정직하게 보고.

## 2. 공격 방향 (방향 only)

다음 분야의 도구를 자유롭게 활용 (구체 수식·계수 사전 제공 금지):

D1. n field 의 2-loop self-energy 위상 구조
D2. setting-sun diagram 의 일반 구조 (3-propagator topology) 및 IR/UV 분리
D3. counterterm renormalization (BPHZ 또는 동등 방식) 의 자유도 계산
D4. Symmetry-protected coefficient 후보 식별 — c 가 어떤 대칭에 의해 보호/고정되는지
D5. Effective action 일관성 — 1-loop 결과와 2-loop 결과의 매칭 조건

8인 팀은 위 D1~D5 를 자유 분담 (역할 사전 지정 금지). 토의에서 분업 자연 발생.

## 3. 수행 단계 (절차 only)

S1. 8인 팀 독립 도출 라운드: 2-loop n self-energy 와 setting-sun 의 일반 구조 정리
S2. c 계수가 어디서 들어오는지 동정 (1-loop counterterm 의 finite part 와의 관계)
S3. 2-loop divergence structure 가 c 의 값을 고정하는지 / 추가 자유도를 요구하는지 판정
S4. 4인 코드/유도 리뷰 (역할 자율 분담)
S5. REVIEW.md 에 정직 결론 — "닫혔다 / 부분 닫힘 / 닫히지 않음" 셋 중 하나로 단정

## 4. 정직성 게이트

- 결과가 c 를 first-principle 로 닫지 못하면 그렇게 적는다 (base.fix.md 패턴 준수)
- "다음 세션에서 가능" 같은 미래 약속으로 결론 회피 금지
- AICc 등 모델 비교 패널티가 등장하면 명시

## 5. 한 줄 사전 추정 (이론 가이드 아님, 위험 인식)

setting-sun 의 sub-divergence 구조는 1-loop counterterm 으로 흡수되는 것이 일반적이며,
2-loop 단독으로 c 의 절대값을 fix 할 가능성은 구조적으로 낮음 — 그러나 실증 도출 결과로 판단.
