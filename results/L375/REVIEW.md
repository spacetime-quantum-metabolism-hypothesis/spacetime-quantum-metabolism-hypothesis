# L375 — 4인 코드리뷰 (자율 분담, 역할 사전 지정 없음)

대상: simulations/L375/run.py + results/L375/report.json (실행 후 review).

## 결과 요약 (실측)
- recovery rate = 100/100 = 1.000 (PASS_THRESHOLD 0.68 대비 +0.32)
- binomial SE = 0.000
- bias (mean log10 σ_0 MAP − truth) = −0.0058 dex
- bias (median) = −0.0061 dex
- RMSE = 0.0173 dex
- err_dex p50 = 0.014, p95 = 0.039
- wall-clock ≈ 0.1 s (1D MAP, 100 mock)
- 판정: **PASS** — recovery rate (1.000) > 0.68

## 4인 자율 분담 review

### P (방법론/설계 정합성)
- SQT generative (α=0.05, β=0.01) vs BB fit (α=0.07, β=0.005) mismatch 가
  η=0.10 noise 와 z∈[0.1, 2.0] 범위에서 σ_0 best-fit 에 흡수되는 미세 양 (~0.006 dex).
  ATTACK_DESIGN A1 가드는 형식적으로 살아 있으나, **임계 0.1 dex 가 noise σ ≈ 0.017 dex
  대비 5.8배 넓어** 사실상 항상 PASS 하는 조건이 됨. **인공 PASS 위험 명시.**
- ±0.1 dex 임계는 task spec 그대로이며, 더 좁히는 것은 spec 변경이라 회피.
  대신 RMSE / p50 / p95 같이 보고하여 정직 평가 가능.

### N (코드 함정 점검)
- numpy 2.x 호환: `np.random.default_rng`, `np.percentile` 직접 사용. trapz 미사용.
- seed: mock seed = 0..99, RNG 인스턴스 분리 → 전역 collision 없음.
- scipy `minimize_scalar` bounded Brent: bounds 박힘 점검 — log10 ∈ (−1, 1), MAP p95 = 0.04
  로 경계 멀리. 안전.
- MAP 단일 추정이라 emcee 가드 (np.random.seed, R̂) 적용 대상 아님.
- 워커 OMP 변수 setdefault 호출했으나 multiprocessing 미사용 (1D MAP·100 mock = 0.1s).
- 비ASCII 식별자 없음, print 비ASCII 없음 (cp949 가드 통과).

### O (통계 정합성)
- N=100, recovery rate = 1.000 → binomial 95% CI (Wilson) ≈ [0.963, 1.000].
  PASS 경계 (0.68) 와는 명확히 분리 → 통계 noise 로 PASS/FAIL 가 뒤집힐 우려 없음.
- 그러나 noise σ ≪ 임계라 검정력 (power) 측면에서 trivial.
- AICc 패널티 항목은 본 task 가 BB 단일 모델 MAP 회수율만 묻기 때문에 미해당.
  L361 후속 (BB vs universal) 에서 다룰 사항.

### H (이론/해석 정합성)
- toy 검증 한정 — 실데이터 BAO/SN/CMB 미사용. SQMH 우위 주장 금지.
- L361 ATTACK A1 ("SQT truth → BB recovery") 의 **최소 자족 조건** 만 확인:
  `BB MAP 가 근사적으로 unbiased 임`. 이는 필요조건이지 충분조건 아님 — 실데이터에서
  BB 가 universal 보다 우위라는 별개 증거가 추가로 필요.
- Branch P (theory-prior anchor) 는 α/β fix 로 구현됨. Branch F (data-fit) 비교는 본 task spec 미포함.

## 정직 결론
- spec 정의대로 PASS. 그러나 임계 ±0.1 dex 가 노이즈 폭 (~0.017 dex) 대비 매우 넓어
  PASS 자체의 정보량은 제한적. **"BB MAP 가 SQT truth 와 정합한다"** 정도의 약한 확증.
- L361 의 5-dataset 풀버전 injection-recovery 와 무관하지 않으나, 그 결과를 대체하지 않음.
- 등급 영향: paper 본문에 "L375 toy injection-recovery 에서 BB MAP recovery 100% (RMSE 0.017 dex)"
  로 주석 추가 가능. SQMH 본 등급 변화 없음.

핵심 한 줄: 회수율은 100% PASS 이나, 임계가 노이즈 폭의 5.8배라 검정력은 약하다 — 정직 표기 필수.
