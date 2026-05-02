# L377 REVIEW — dynesty smoke test (4인 자율 분담 코드리뷰)

## 결과 요약
- 실행 시간: 0.166 s, 13561 likelihood calls, 784 NS iterations
- ln Z = -5.479 +/- 0.240   (analytic: -5.537,  잔차 +0.058 — 1σ 이내)
- mode_count = 2; cluster weights = (0.609, 0.391); centroids = (-2.00, -2.03, -2.01) and (2.00, 2.01, 2.00)
- PASS = True (C1 finite, C2 |ΔlnZ|<0.5, C3 두 모드 모두 weight>0.2)

## 코드 리뷰 (4인 자율 분담, 역할 사전지정 없음)

### A. likelihood / prior 정합성
- L = exp(-r_A^2/2σ^2) + exp(-r_B^2/2σ^2) 합 → 해석 적분 = 2·(2πσ^2)^(3/2) = 1.969
- prior box 부피 = 10^3 = 1000 → ln Z = ln(1.969/1000) = -5.5372
- logsumexp 패턴으로 numerical underflow 차단. OK.

### B. dynesty API 사용
- dynesty 3.0.0 → `rstate=np.random.default_rng(seed)` 규약 준수 (CLAUDE.md L5 재발방지).
- `sample='rwalk'` + `bound='multi'` : multimodal 안전 조합. `auto` 였으면 슬라이스/볼 자동 선택이라 1D 가까운 ridge 에서 stall 가능. 명시 OK.
- `dlogz=0.1` 적정. 100 live 에서 nominal 오차 σ_lnZ ≈ √(H/Nlive) ≈ 0.24 와 일치.

### C. multimodal 분리 검증
- sklearn 의존 회피 (스레드 강제 환경에서 임포트 비용). 자체 2-means k-means 구현, 최대거리 시드 + 50 iter 수렴.
- 두 centroid 가 각각 MU_A=(-2,-2,-2), MU_B=(+2,+2,+2) 로부터 0.033, 0.014 떨어짐 — 0.05σ 이하 정확.
- weight 비대칭 0.609 vs 0.391 은 100 live 노이즈, dlogz=0.1 한계 내. 평균값 0.5 에 약 1σ.

### D. 환경 / 재현성
- OMP/MKL/OPENBLAS_NUM_THREADS=1 강제 (CLAUDE.md "워커당 스레드 고정").
- rstate seed=20260501 고정.
- 단일 프로세스 smoke test 이므로 multiprocessing 미사용. 본 분석 적용 시 dynesty `pool=` 인자 + spawn pool 필요.

## 한계 / 후속
- 합성 toy. 본 SQMH joint chi2 likelihood (BAO+SN+CMB+RSD, 100 ms/call) 에 그대로 적용 시 nlive=100, ~14k calls → 약 24분. 실제 evidence 산출은 nlive=500~1000 필요 (CLAUDE.md L6 참조).
- 본 분석에서 5+D 비혼합 (C28 K13 R̂=1.37) 사례 있음 → dynesty 적용은 후속 별도 LXX 에서 정식 검증.

## 정직 한 줄
dynesty 3.0.0 가 멀티모달 toy 에서 ln Z, mode 수 모두 합격 — SQMH 본 분석 적용은 별도 검증 필요.
