# L344 NEXT STEP — P9+P11 forecast 후속 작업

## 즉시 실행 (next 1-2 loop)

1. **P11 NS saturation mock FIM 재실행**
   - 1000 realization, 노이즈 시나리오 3종 (낙관 σ=2%, 중립 5%, 비관 10%).
   - EOS marginalize (Λ-CDM polytrope family + nuclear-physics prior).
   - 2-regime/3-regime 동시 fit, AICc 분포 산출.
   - 산출: ΔAICc histogram + 5/50/95 percentile.

2. **P9 dSph mock FIM 독립 forecast**
   - dSph kinematics 13 archive (Fornax, Sculptor, Draco, ...) 모의 데이터.
   - stellar M/L + anisotropy systematic 통합 marginalize.
   - SQT g(rm1) 저-ψ 곡률 신호 vs H0 prior degeneracy 정량.

3. **P9+P11 joint mock**
   - 두 anchor 동시 fit, cross-term covariance 추정.
   - 직교 정보 채널 가정의 검증 (cross corr 행렬 < 0.2 인지).
   - 결합 ΔAICc 의 단순합 vs 실측 차이 (bonus or penalty) 측정.

## 중기 (3-5 loop)

4. **systematic 보정된 robust ΔAICc** 산출
   - 가짜 신호 (false-positive) CV: data 가 2-regime 일 때 3-regime 가 우연히
     ΔAICc < -2 도달하는 비율 ≤ 5% 보장.
   - 가짜 null (false-negative) CV: data 가 3-regime 일 때 P9+P11 forecast 가
     2-regime 우세로 잘못 가는 비율.

5. **kill switch 판정**
   - 결합 forecast median ΔAICc > -1 이면 3-regime 강제 단념 → 논문 본문
     "2-regime baseline 확정, 3-regime alternative 부록 한정" 으로 lock.
   - median < -2 이면 P11 실측 우선순위 최상단.

## 장기 (실측)

6. **P11 실측 데이터 확보**
   - NICER + LIGO post-merger 최신 NS mass-radius posterior.
   - max-mass scaling vs SQT ψ-ratio 회귀.

7. **P9 실측 데이터 확보**
   - LMC/SMC + Local Group dSph kinematics 통합 catalog (Gaia DR4 등 활용).

8. **재판정 loop**
   - 실측 데이터 도착 시 본 forecast 와 실제 ΔAICc 비교, 글로벌 입증 여부 결정.

## 산출물 chain
- L345: P11 mock 재실행 결과 (실제 시뮬).
- L346: P9 mock 결과.
- L347: joint mock + cross-term.
- L348: systematic 보정 robust forecast.
- L349: kill switch 판정 + 논문 sec 3/7 update 권고.

## 정직 기록
- 본 loop (L344) 는 **forecast 만**, 실측 없음. 등급 변경 없음 (carry-over -0.08).
- 8인 중앙값 추정은 사전 분석 (FIM 미실행) 기반 — 실제 mock 후 ±50% 변동 가능.
- P9 의 ΔAICc 기여 (+0.3 ~ +0.5) 는 H0 marginalization 가정 의존, 실제로는
  -0.5 ~ +0.5 spread.
