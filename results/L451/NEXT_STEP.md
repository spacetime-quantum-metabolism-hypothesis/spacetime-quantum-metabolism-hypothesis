# L451 NEXT_STEP — 4인팀 실행 task list

**입력**: ATTACK_DESIGN B1–B8 + 8인팀 합의.
**출력**: simulations/L451/run.py + results/L451/{REVIEW.md, report.json}.

## 4인팀 자율 분담 (CLAUDE.md Rule-B)
- 역할 사전 지정 없음. 데이터 매핑 / mock 생성 / Laplace fit / 분포 통계 /
  해석 자연 분담.

## Task 매트릭스

### T1. Truth model 2 종
- T1a: **LCDM null** — σ_truth = 0.85 (L424 mock_false_rate 와 동일 baseline).
- T1b: **SQT pre-fit** — baseline 8 anchor 에 three-regime fit (R=5 MAP)
  의 σ_predict(log_rho_i) 를 truth 로.

### T2. ρ_env 매핑 2 종
- T2a: dSph local-group (kpc-outer) 매핑 (L424 LG mode).
- T2b: dSph galactic-internal 매핑 (L424 INT mode).

### T3. Anchor pool 2 종
- T3a: 8-pool (baseline only) — control.
- T3b: 13-pool (baseline + 5 dSph) — treatment.

### T4. Mock 횟수
- N_MOCK = 200 (Rule-A B4: σ_ΔlnZ ~ 5 가정 시 sub-σ 검출 가능).
- 시드 고정 (seed=4242, mock_idx 별 child seed).

### T5. 측정량 (per cell)
- ΔlnZ_i = lnZ(three_regime, anchors_i) − lnZ(lcdm, anchors_i).
- Laplace 실패 시 NaN 기록. 셀별 (성공률, mean, std, [5,50,95] percentile).

### T6. 비교 차이
- ΔΔlnZ(treatment − control) per truth × mapping = 4 분포.
- (a) 분포 평균이 음수면 model penalty 작동 신호.
- (b) 분포 std < 5 면 cherry-pick 폭 ±34 보다 좁음.
- (c) mapping 두 종 분포가 서로 차이 < 1σ_pooled 면 매핑 자유도 흡수.

## 산출 파일
- simulations/L451/run.py — multiprocessing.spawn pool, OMP=1.
- results/L451/report.json — 8 셀 분포 통계 + 4 ΔΔlnZ 분포.
- results/L451/run_log.txt — 콘솔 로그.
- results/L451/REVIEW.md — 4인팀 정량 결과 + B7 평가.

## 병렬 실행
- multiprocessing.get_context('spawn').Pool(8) — 200 mock × 4 cell mapping
  = ~800 Laplace fit 호출. 각 fit ~0.2s 가정 시 직렬 ~160s, 8병렬 ~25s.
- 각 워커 OMP/MKL/OPENBLAS = 1 강제.
- mock 단위로 work 분할 (각 worker 가 mock_idx range 받아 4 cell 모두 실행).

## 사전등록 (post-hoc 방지)
- 본 NEXT_STEP 작성 시점 (run.py 실행 *전*) 에 이미 B7 의 (a)/(b)/(c)
  판정 기준 등록. 결과 본 후 기준 변경 금지.
- 정직 한 줄: "셋 중 어느 것이 PASS 되었는지 + 셋 모두 FAIL 시 negative
  결론" 그대로 기록.
