# L357 REVIEW — 8인 / 4인 리뷰 체크리스트

정직 한국어 한 줄: 이론 클레임 (cross-scale 정합성 주장, ϒ marginalization 정당성, SQMH 신호 파라미터 해석) 은 Rule-A 8인 순차 리뷰, 코드 (로더/chi2/emcee/marginal closed form) 는 Rule-B 4인 자율 리뷰가 모두 통과해야 production 진입한다.

---

## A. 8인 이론 리뷰 체크리스트 (Rule-A, 순차)

각 항목 8명 모두 PASS 요구. 한 명이라도 보류 시 재토의.

1. **데이터 lock 정합성**: 5개 채널이 같은 우주론 파라미터 정의 (Ω_m, h 등) 를 공유하는가? 단위·정의 충돌 없는가?
2. **SQMH 신호 파라미터 의미**: 6 파라미터 중 SQMH 신호 2개가 channel 5개에 모두 같은 의미로 진입하는가? (배경/섭동 양쪽?)
3. **ϒ marginalization 사전분포**: ϒ_disk, ϒ_bul 의 Gaussian prior 폭이 SPARC 표준 (Lelli+2016) 과 일치하는가?
4. **cluster pool 정의**: 어떤 stack/관측량이 SQMH 신호와 결합하는지 물리적 채널이 명시되었는가?
5. **anchor 선택 편향**: SH0ES H0 vs BBN ω_b 둘 중 어느 쪽도 결과를 사전 결정하지 않는가? 두 옵션 모두 별도 run 비교 가능한가?
6. **CMB compressed bridge**: 고z LCDM tail bridge 가 SQMH 모델과 충돌 시점 (Z_CUT) 이 합리적인가? rescale 금지 규칙 준수?
7. **cross-scale 일관성 주장 정직성**: 한 dataset 큰 tension 시 "cross-scale PASS" 주장 금지 합의 명문화.
8. **AICc / Bayesian evidence**: 6 param 모델이 LCDM 대비 dAICc/dBIC 양쪽 보고, fixed-θ 와 marginalized 구분 명시 (L6 재발방지).

---

## B. 4인 코드 리뷰 체크리스트 (Rule-B, 자율 분담)

4명 자율 분담, 역할 사전 지정 금지.

### B.1 데이터 로더
- [ ] DESI DR2 13pt + 전체 cov, D_V(BGS) + D_M/D_H 정확 매핑.
- [ ] SPARC 갤럭시별 (R, V_obs, σ_V, V_gas, V_disk, V_bul) 누락 없음, 단위 km/s 통일.
- [ ] Planck compressed cov 양정치 (eigenvalues > 0).
- [ ] cluster pool meta 에 핵 calibration nuisance 적용 위치 명시.
- [ ] anchor 단일 Gaussian, σ 출처 인용.

### B.2 chi2 함수
- [ ] 모든 chi2 함수 None/nan 시 즉시 return None, log_likelihood 가 -inf 로 변환.
- [ ] chi2 sentinel 1e6 합산 패턴 부재 (grep 검사).
- [ ] BAO 거리 단위: c[m/s]/(H0[s^-1]·E·Mpc[m]) = Mpc, 중간 km/s/Mpc 변환 없음.
- [ ] CMB θ_* 0.3% theory floor 더해짐.

### B.3 ϒ marginalization
- [ ] closed form 유도가 brute-force 2D ϒ 그리드 적분 (3 갤럭시) 과 1e-3 일치.
- [ ] log|det(M_g)| 항 누락 없음 (Bayesian evidence 정합).
- [ ] ϒ prior 평균/폭 외부 설정 가능 (hard-code 금지).

### B.4 emcee runner
- [ ] `multiprocessing.get_context('spawn').Pool(9)`.
- [ ] `OMP/MKL/OPENBLAS_NUM_THREADS=1` env 강제.
- [ ] `np.random.seed(42)` 가 run_mcmc 내부에 위치.
- [ ] 워커 안에서 데이터 독립 로드 (전역 singleton 미사용).
- [ ] JSON 저장 시 `_jsonify` 재귀 변환기 적용.
- [ ] R̂, τ 진단 자동 출력.

### B.5 일반 안전
- [ ] numpy 2.x: `np.trapezoid` 직접 호출 (trapz 미사용).
- [ ] print 에 비-ASCII 유니코드 없음 (cp949 안전).
- [ ] in-place 정규화 함정 (`D /= D[-1]`) 패턴 부재 — `.copy()` 강제.
- [ ] sibling background.py 충돌 없음 (l357 디렉터리 내 상대 import).

---

## C. 통과 조건

- A 8/8 + B 5 영역 모두 PASS → production run (Step D) 진입.
- 한 항목이라도 fail → 해당 항목 단독 재작업, 다른 영역 진행 금지.
- L6 재발방지: 리뷰 완료 전 결과 논문/보고서 반영 절대 금지.

---

## D. 기록 의무

본 리뷰 결과는 다음 세션에서 `results/L357/REVIEW_LOG.md` 에 8인 의견 + 4인 코드 코멘트 그대로 보존. 요약 금지, 원문 보존.
