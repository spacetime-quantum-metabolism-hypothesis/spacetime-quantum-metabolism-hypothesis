# L387 ATTACK DESIGN — n field 1-loop self-energy Π(p²) and m_n correction

> ⚠️ CLAUDE.md 최우선-1: 본 문서는 **방향만** 제공한다. 구체 수식, 결합 상수 값,
> regulator 계수, 종결 답을 사전 지정하지 않는다. 8인 팀이 독립 도출한다.

---

## 1. Independence statement

L387 is run **independently** from L380~L386. No prior session imports of
finalized Π(p²), counter-terms, or m_n shift formulae. The team derives the
self-energy from scratch with only the inputs listed in §3.

## 2. Goal (single-line, honest)

n 장(metabolism field n)의 1-loop self-energy Π(p²)를 계산하여,
재규격화된 질량 보정 Π_1-loop / m_n² 가 (Λ_UV / M_Pl)² 스케일에 어떤
의존성을 갖는지 정량 판정한다.

성공 판정: Π_1-loop / m_n² 의 Λ_UV-dependence 가 (Λ_UV/M_Pl)² 의
"단순 거듭제곱" 인지, 로그 보정이 지배적인지, 혹은 둘이 같은 차수인지를
숫자로 구분.

## 3. Inputs allowed (방향 only)

팀에게 주어지는 입력은 다음 **명칭** 뿐:

- n 장의 effective Lagrangian 카테고리: scalar metabolism field 결합 형태 (자기상호작용, gravity portal, matter portal 중 어떤 것을 우세 채널로 볼지 팀이 합의).
- regulator: 차원정규화 vs hard cutoff Λ_UV 둘 다 시도 (상호 검증).
- 두 스케일 비: Λ_UV, M_Pl, m_n. 비율 r = Λ_UV / M_Pl 의 함수로 결과 정리.

명시적으로 **금지**:

- "Π(p²) = ... " 형태의 출발 수식 제공 금지.
- counter-term 형태 사전 지시 금지.
- 결합 상수의 수치 값(예: g, λ) 사전 고정 금지. 팀이 차원분석으로 자연스러운
  조합을 택한다.

## 4. Team composition (8인 + 4인 코드리뷰)

CLAUDE.md LXX 공통원칙에 따라:

- 8인 이론팀: 역할 사전 지정 없음. 인원 수만 8. Π 계산, 정규화 선택, 부호,
  m_n 재정의, 해석은 토의에서 자율 분담.
- 4인 코드리뷰팀: simulations/L387/run.py 의 적분/regulator 구현, 단위 일관성,
  Λ_UV 의존성 추출 로직을 자율 분담 검증.

## 5. Acceptance keys

- K1 — Π(p²) 가 Lorentz-scalar 함수로 표현되고 p² 의존성 분리 명확.
- K2 — UV regulator 두 가지(dim-reg 와 cutoff)에서 같은 m_n shift 부호.
- K3 — Π_1-loop / m_n² 의 r = Λ_UV/M_Pl 의존성 추출 (멱지수 ± 1 정확도).
- K4 — m_n^bare 와 m_n^renorm 사이 finite, well-defined relation.
- K5 — fine-tuning 정도 정직 보고 (자연스러움 vs hierarchy 문제).

## 6. Honesty clause

결과가 SQMH 의 다른 결과와 충돌하면 base.fix.md 패턴으로 정직 기록한다.
Π_1-loop / m_n² ~ O(1)·r² (단순 quadratic) 이 나오면 hierarchy problem 으로
정직 보고. 로그 지배면 그것대로 보고. 작위적 cancellation 금지.

## 7. Deliverables

- results/L387/ATTACK_DESIGN.md — 본 문서.
- results/L387/REVIEW.md — 8인 토의 + 4인 코드리뷰 종합 + K1~K5 판정.
- simulations/L387/run.py — 두 regulator 에서 Π(p²) 수치 평가, Λ_UV scan,
  Π/m_n² 의 r 의존성 추출.

## 8. Out of scope

- 2-loop 이상.
- gravity portal 의 spin-2 graviton loop full GR 계산 (linearised graviton
  exchange 까지만).
- 실험 데이터 fit (L387 은 이론-내적 정합성 한 단계).
