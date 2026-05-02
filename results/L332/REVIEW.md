# L332 REVIEW — 4인 P/N/O/H

## P (Positive, 옹호자)
ATTACK_DESIGN A1, A3, A8 의 P11 NS saturation 우선순위는 정보론적으로 타당.
고 ψ regime 에서 g 곡률 차이가 sigmoid-weight 모델 (2-regime) 와 separate-amp
(3-regime) 사이 ~15% 식별가능 → NS M_max 정밀화 (예: NICER + Cromartie pulsar
조합) 0.05 M_sun 수준이면 5σ 분리. forecast 중앙값 ΔAICc ≈ −1.8 은 보수적이며,
EOS chiral EFT prior 적용 시 −2.5 ~ −3 까지 도달 가능. 정직 명시 (글로벌 입증
불가, 조건부) 도 학술적 신뢰성에 필수. JCAP 91-95% 유지 합리.

## N (Negative, 반박자)
P11 forecast 의 "ΔAICc ≈ −1.8" 는 g(ψ) ↔ NS M_max 매핑이 *모델 의존*. SQT 자체
가 NS 내부 핵물질 ψ 영역까지 외삽 신뢰도가 낮음 (extrapolation 5+ orders of
magnitude in density). EOS systematic ±0.30 M_sun 시나리오에서 forecast 가
±2 σ 이상 흔들리면 anchor 정보가 소진됨. 또한 A4 의 "단순한 단일 transition 이
진짜" 가설은 진지하게 받아야 함 — Occam 적으로 2-regime 이 기각되지 않는 한
3-regime 추구는 confirmation bias. *글로벌 입증 시도 자체* 가 과적합 risk.

## O (Objective, 중재자)
양측 합의 가능 영역:
1. 본문 baseline = 2-regime merge (정직).
2. P11 anchor forecast 는 *예비 sensitivity 분석* 으로만 보고. 결정적 주장 금지.
3. ΔAICc 임계 −2 (P/N 합의), 도달 시 supplementary 에 3-regime 옵션 기록.
4. EOS systematic 두 시나리오 (tight/loose) 를 모두 보고 — 정직성 강화.
불일치: P 는 "P11 만으로 충분", N 은 "P11+P9+void 합쳐도 부족". Objective 판정:
*P11 단독* 으로는 50/50, *P11+EOS tight prior* 시 60-70% 3-regime favor.

## H (Honesty, 정직 검토자)
- "글로벌 최적합 입증 시도" 라는 주제 표현 자체가 confirmation bias 유발 위험.
  ATTACK_DESIGN A7 "글로벌 입증 불가능" 명시는 정직.
- 누적 245 loop, 등급 -0.07 변화 없음 — 새 결정적 결과 부재 정직 보고 필수.
- forecast 숫자 (ΔAICc ≈ −1.8) 는 *expert prior estimate* 이며 실제 mock
  실행 결과 아님. simulations/L332/run.py 가 단일 forecast 만 산출 — 이것이
  엄밀 forecast 가 아닌 *order-of-magnitude scoping* 임을 본문에 명시 필수.
- "JCAP 91-95%" 는 변화 없음. 부풀림 없음 확인.
- 권고: "L332: 3-regime 강제 anchor 부재 확인, 2-regime baseline 채택, P11 은
  미래 작업" 으로 정직 한 줄 보고.

## 합의
4/4 합의: **2-regime baseline 채택, 3-regime 은 P11 조건부 reserve, 글로벌
입증 현 시점 불가능 정직 명시**. ATTACK_DESIGN, NEXT_STEP 모두 승인.
