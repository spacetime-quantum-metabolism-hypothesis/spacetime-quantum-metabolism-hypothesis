# L357 ATTACK DESIGN — 5-dataset Joint Likelihood (emcee spec)

정직 한국어 한 줄: 본 문서는 SPARC + DESI BAO + Planck CMB compressed + cluster pool + cosmic anchor 다섯 데이터를 동시에 묶는 joint posterior 의 emcee 구현 spec 만 정의한다 (이론 수식·파라미터 값 일절 미기재, CLAUDE.md 최우선-1 준수).

---

## 1. 목적

5개 독립 관측 채널을 같은 파라미터 공간 위에서 동시에 평가해 SQMH 후보 모델의 cross-scale 일관성을 검증한다. 한 데이터셋이라도 빠지면 cross-scale 주장이 성립하지 않는다.

본 spec 은 데이터 인터페이스, likelihood 합산 규칙, marginalization 구조, 샘플러 설정, 산출물 형식만 정의한다. 모델의 함수형은 팀이 독립 도출한다.

---

## 2. 파라미터 공간

총 6 자유 파라미터. 명칭과 의미만 지정, 값/사전분포 폭은 팀 토의에서 결정.

| idx | 이름 | 채널 분류 | 비고 |
|-----|------|-----------|------|
| 1 | 우주론 배경 #1 | BAO + CMB + anchor | 표준 배경 파라미터 |
| 2 | 우주론 배경 #2 | BAO + CMB + anchor | 표준 배경 파라미터 |
| 3 | SQMH 신호 #1 | 모든 채널 공유 | 팀 도출 모델 자유도 |
| 4 | SQMH 신호 #2 | 모든 채널 공유 | 팀 도출 모델 자유도 |
| 5 | 클러스터 핵 nuisance | cluster pool 전용 | scaling/calibration |
| 6 | SPARC nuisance (galaxy-level) | SPARC 전용 | hyperparameter, 갈ax 별 ϒ 는 analytic marginalize 후 제외 |

ϒ (mass-to-light ratio, SPARC 갤럭시별) 은 6 파라미터에 포함되지 않는다 — Section 4.2 의 analytic marginalization 으로 likelihood 레벨에서 소거.

---

## 3. 5개 데이터셋 인터페이스

각 데이터셋은 `(observable_vector, covariance_or_sigma, model_predictor)` 삼중조로 추상화. 모듈 경계 명확화.

### 3.1 SPARC (회전곡선)
- 입력: 175 갤럭시, (R_i, V_obs_i, σ_V_i) 및 baryonic 분해 (V_gas, V_disk, V_bul).
- 갤럭시별 ϒ_disk, ϒ_bul nuisance → analytic marginalize.
- chi2_SPARC = Σ_galaxy chi2_galaxy(ϒ-marginalized).

### 3.2 DESI BAO (DR2 13-point)
- CobayaSampler/bao_data 공식 파일. D_V(BGS) + D_M/D_H 13 point + 전체 cov matrix.
- chi2_BAO = Δ^T C^{-1} Δ.

### 3.3 Planck CMB compressed
- compressed θ_*, R, ω_b 3-vector + cov.
- Hu-Sugiyama z_* fit formula 정확도 0.3% theory floor 추가 (CLAUDE.md 규칙 준수).
- 고z 적분은 LCDM tail bridge (Z_CUT 이상은 pure LCDM, low/high rescale 금지).

### 3.4 Cluster pool
- 클러스터 stacking 관측량 (참여 클러스터 set 과 관측량 종류는 데이터 lock 단계에서 확정).
- nuisance: 핵 calibration scaling 1 자유도 (param idx 5).
- chi2_cluster = Δ^T C^{-1} Δ (혹은 diagonal σ).

### 3.5 Cosmic anchor (H0 / SH0ES-like 또는 BBN ω_b prior)
- 선택은 팀 결정. 단일 (또는 소수) Gaussian prior 형태.
- chi2_anchor = ((x - x_obs) / σ_obs)^2.

---

## 4. Joint Likelihood 구조

### 4.1 합산 규칙

```
log_likelihood(θ) = -0.5 * Σ_d chi2_d(θ)
                   for d ∈ {SPARC, BAO, CMB, cluster, anchor}
```

- 데이터셋 간 독립 가정 (서로 다른 sky/scale, cov 공유 없음).
- chi2 계산 실패 (ODE divergence, 음수 ρ 등) 시 즉시 `return -np.inf`. sentinel 1e6 합산 절대 금지 (CLAUDE.md 재발방지 항목).

### 4.2 ϒ analytic marginalization (SPARC)

각 갤럭시 g 에 대해 V_model^2 = ϒ_d V_disk^2 + ϒ_b V_bul^2 + V_gas^2 형태에서 V^2 가 ϒ 의 선형결합이므로 (ϒ_d, ϒ_b) 에 대한 Gaussian prior 하에 chi2 의 ϒ 적분이 closed form. 결과: 각 갤럭시당 modified chi2 + log|det(M_g)| 항 (Bayesian evidence contribution 보존).

구체 표현은 팀이 도출. spec 은 "갤럭시별로 ϒ 를 sampler 차원에 추가하지 않는다" 만 강제.

### 4.3 샘플러 호출

```
log_posterior(θ) = log_prior(θ) + log_likelihood(θ)
```

prior 가 box 외부면 -inf 즉시 리턴. log_likelihood 내부에서 `np.isfinite` 체크 필수.

---

## 5. emcee 구성

| 항목 | 값 |
|------|-----|
| n_dim | 6 |
| n_walkers | 48 (= 8 × n_dim) |
| n_steps (production) | 5000 |
| burn-in | 2000 |
| moves | StretchMove (default) |
| seed | `np.random.seed(42)` + 워커 초기값 별도 seed |
| 병렬 | multiprocessing spawn Pool, 9 워커 (10코어 환경 main 1코어 확보) |
| thread guard | `OMP/MKL/OPENBLAS_NUM_THREADS=1` env 강제 |
| 수렴 진단 | autocorr τ × 50 < n_steps, R̂ < 1.01 (chain split) |

emcee stretch move 는 np.random 전역을 쓰므로 `run_mcmc` 내부에 `np.random.seed(...)` 추가 필수 (CLAUDE.md 재발방지).

산출 chain → corner plot, 1D marginal, 2D contour. JSON 직렬화 시 `_jsonify` 재귀 변환기 (np.bool_/np.float_ 직렬화 깨짐 방지).

---

## 6. 검증 게이트 (사전 정의)

본 단계는 spec 만이며 합격/불합격 기준은 다음 LXX 단계에서 확정. 다만 다음은 강제:

1. R̂ < 1.01 미달 시 production 결과로 인용 불가 (provisional 표기).
2. 5개 데이터셋 chi2 가 각각 따로 보고되어야 함 (joint chi2 만 보고 금지). dataset 별 pull 분포 첨부.
3. SPARC ϒ marginalization 의 closed form 유도 검산은 4인 코드리뷰 필수.
4. cluster pool 핵 calibration 1 nuisance 가 강한 degeneracy 를 만들면 sampling 실패 가능 — 사전 1D profile 진단 후 진입.

---

## 7. 산출 산출물 (이번 단계)

- ATTACK_DESIGN.md (이 파일)
- NEXT_STEP.md (다음 실행 단계)
- REVIEW.md (8/4 인 리뷰 체크리스트)

코드는 본 단계에서 작성하지 않는다. 다음 단계에서 데이터 로더 + chi2 함수 + emcee runner 분리 구현.
