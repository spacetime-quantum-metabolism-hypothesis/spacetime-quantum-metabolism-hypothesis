# L342 REVIEW — 4인 코드/통계 자율 분담 검토

대상: simulations/L342/run.py + run_output.json + ATTACK_DESIGN.md +
NEXT_STEP.md.

---

## R1 — 데이터/단위 (자율 담당 1)

- log10 ρ_env 매핑 (cosmic −27, cluster −24, galactic −21) 은 *대표값*.
  실제 cosmic IGM 평균 ≈ ρ_crit ≈ 0.85e−26 (log10 ≈ −26.07), cluster ICM
  ≈ 1e−24, galactic disc ≈ 1e−21 ~ 1e−20. 대표값이 ±1 dex 흔들려도 LRT
  는 dominated by cluster outlier — 결론 불변.
- log10 σ_0 값 출처 확인: `results/L33x` 와 `results/L1xx` 의 SPARC MCMC
  10^9.558 (galactic), branch B 분류 7.75 (cluster), 8.37 (cosmic) — 일관.
  L164/L294 와 동일 anchor.
- σ_y 단위 dex (log10 의 표준편차) — chi² 계산에서 (Δlog y / σ_y_dex)² 로
  맞음. PASS.

## R2 — 통계 검정 정당성 (자율 담당 2)

- N=3, k=3 saturation 문제 정직 표기 됨. AICc 미사용은 옳다 (정의 불가).
- BIC 의 N=3 사용은 점근식의 약한 적용 — 그러나 ΔBIC = 287 이라 점근
  보정이 결과를 뒤집을 수 없음. Kass-Raftery decisive 임계 (10) 의 30배.
- LRT 17σ 는 nested model (M1 ⊂ M2: D=0 한정 시 M2→linear 안 되므로
  엄밀히 nested 아님). 그러나 Δχ² = 288 자체는 모델-독립 statistic.
- Z stress test (σ_y_cluster 인플레이션) 정직 — systematic 0.3 dex 가정
  시 ≈ 3-4σ 라는 보수 결론 정확.

## R3 — 코드 정확성 (자율 담당 3)

- M1 closed-form WLS 는 표준 공식. Sw·Swxx − Swx² determinant 계산 OK.
- M2 multi-start (3×3×3 grid) 충분; saturated solution 으로 chi² ~ 0
  도달 확인. global minimum 자명 (3점 지나는 parabola 유일해).
- M1b tanh 의 x0=−24, w=2 fix 는 임의 선택. 그러나 M1 과 같은 chi² 로
  수렴하므로 monotonic family 의 cluster-fit 불가능성이 robust.
- 유니코드 print 없음 (cp949 안전). PASS.
- numpy 2.x 호환 OK (trapz 미사용).

## R4 — 해석/논문 정합성 (자율 담당 4)

- "17σ" 는 formal LRT 변환값 — frequentist p-value 로는 사실상 0. 그러나
  N=3 점에서의 p-value 는 점근 χ²₁ 분포가 정확하지 않을 수 있음. 보수적
  으로 "Δχ² = 288, BIC decisive" 로 보고 권고.
- "단조성 기각" claim 의 한계 명시 (cluster single-source, anchor post-hoc)
  ATTACK_DESIGN 과 NEXT_STEP 양쪽에 기록 — 정직.
- L341 종합점수 회복 +0.003~+0.005 추정은 합리적. 단 격하 회복은 8인
  L341 합의 재-vote 필요 (개별 loop 자의 변경 금지).
- CLAUDE.md "최우선-1" 위반 없음 — 본 loop 는 *기존 측정값* 통계 분석이며
  새 이론 수식 강제 없음.

---

## 4인 만장일치 권고

1. simulations/L342/run.py 결과 **수락**: Δχ² = 288, ΔBIC = 287, single-FP
   RG 가설은 현 데이터에서 강하게 기각.
2. 보고서 본문에서 "17σ" 표현 사용 시 반드시 "(formal LRT, N=3)" 부기.
3. cluster single-source caveat 와 L335 후속 의존 명시 (이미 수행).
4. L343 에서 P9 dSph anchor 추가 시뮬 권고 — N=4 면 AICc 정의 회복 +
   k=3 parabola 가 saturated 가 아니게 됨.

R1-R4 모두 GREEN. 한계 표기 정직성 OK.
