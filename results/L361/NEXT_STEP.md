# L361 — NEXT STEP (실행 계획)

## 목표
SQT truth 입력 mock 100 개 → 5-dataset joint MCMC → BB recovery rate / posterior coverage 산출.

## 데이터셋 구성 (5-dataset)
1. BAO: DESI DR2 13-pt (D_V/D_M/D_H + 전체 공분산, CobayaSampler 공식)
2. SN: DES-Y5 SN5YR (zHD, M analytic-marginalised, sn_data/DESY5)
3. CMB: compressed θ\* + Hu-Sugiyama (theory floor 0.3% 추가, chi2_joint 'cmb' 키 직접)
4. RSD: fσ_8 compilation (Phase3 와 동일, drift-guard assertion)
5. SPARC-like rotation curves (subset, BB anchor 검증용)

## 절차
1. **Truth 고정**: SQT champion (L33 Q93 계열, Om≈0.3 joint-driven 값 사용 — BAO-only Om=0.068 함정 회피).
2. **Mock 생성**: 각 데이터셋 covariance 로부터 multivariate Gaussian draw, 100 realisation × seed 0..99.
3. **Anchor 정책 분기**:
   - Branch P (theory-prior): σ_0 anchor 3 regime *데이터 보기 전 고정* — L272 권고.
   - Branch F (data-fit): σ_0 free — L272 와 동일 자유도.
4. **Fit**: 각 mock 에 BB(3 regime) + universal 양쪽 → emcee 48×2000 (Python 3.14 가드, np.random.seed(42), THREADS=1).
5. **Aggregate**:
   - Truth 1σ recovery rate (per-parameter histogram)
   - 68/95 % credible coverage empirical vs nominal
   - ΔAICc(BB-universal) median + IQR
   - R̂<1.05 통과 비율 (silent drop 금지, 비수렴 mock 별도 카운트)

## 병렬화
- multiprocessing spawn Pool(9), 워커당 OMP/MKL/OPENBLAS=1.
- Mock 단위 독립 — 워커 내부 데이터 독립 로드.
- 예상 wall-clock: ~60 시간 (joint chi² 100 ms × 48 × 2000 × 100 / 9).

## 산출물
- simulations/L361/run.py (mock 생성 + fit driver)
- simulations/L361/aggregate.py (recovery / coverage 통계)
- results/L361/recovery_table.json (per-mock truth-recovery flag)
- results/L361/coverage_plot.png (68/95% nominal vs empirical)
- results/L361/REVIEW.md (4인 코드리뷰 + 정직 평가)

## PASS / FAIL
- PASS: BB truth recovery ≥ 68%, 95% coverage 90–98%, Branch P ≥ Branch F → L272 처방 정당화 + paper anchor box 유지.
- FAIL: recovery < 50% 또는 coverage 극단 미달 → BB 식별력 무효, paper 에서 BB 강등.

## 주의 (CLAUDE.md 룰 준수)
- 8인 팀 역할 사전 지정 금지, 토의 자율 분담.
- AICc 패널티 명시.
- 시뮬 실패 → 4인 코드리뷰 후 재실행.
- 결과가 base.md 와 다르면 base.fix.md 에 정직 기록.
- 비SQMH-consistent branch (ξ_q<0 등) 발생 시 별도 표기.

핵심 한 줄: SQT mock 100 개에서 BB 회수율이 nominal 68% 에 미달하면 BB 는 paper 에서 강등 대상이다.
