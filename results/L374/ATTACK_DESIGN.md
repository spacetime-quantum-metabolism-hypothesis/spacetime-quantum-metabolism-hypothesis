# L374 ATTACK_DESIGN — 5-dataset joint MCMC smoke test

## 목적
emcee 기반 5-dataset joint chi^2 MCMC 파이프라인의 수렴(convergence) smoke test.
n_walkers=200, n_steps=200 의 소규모 chain 으로 R-hat, ESS, autocorr 측정.
실제 SQMH 모델 fit 이 아닌 toy likelihood 로 파이프라인 자체의 정상 동작을 검증한다.

## 토이 likelihood 구성
- 파라미터: 6 차원 BB (Big-Bang nuisance toy) θ = (θ1..θ6), Gaussian prior N(0,1) 박스 prior [-5,5].
- 5 개 mock dataset, 각각 chi^2_i(θ) = (θ - μ_i)^T A_i^T A_i (θ - μ_i).
  - μ_i: 각 데이터셋별로 다른 작은 offset (재현가능한 seed=374+i).
  - A_i: 6x6 random matrix (seed 고정) → 양의 정부호 Σ_i^{-1} = A_i^T A_i.
- log L = -0.5 * Σ_i chi^2_i(θ).
- log posterior = log prior (uniform on box, Gaussian N(0,1)) + log L.

## 실행 사양
- emcee.EnsembleSampler, n_walkers=200, n_steps=200.
- moves: 기본 stretch.
- 초기값: prior 박스 내 균등 random (seed=374).
- np.random.seed(374) 강제, OMP/MKL/OPENBLAS_NUM_THREADS=1.

## convergence 지표
- per-parameter Gelman-Rubin R-hat (split-half across walker 그룹 2 등분).
- per-parameter integrated autocorrelation time τ (emcee get_autocorr_time, tol=0).
- ESS = n_walkers * n_steps_after_burn / τ.
- burn-in = 50 step (200 의 25%).
- pass criteria (smoke test): R-hat<1.2 (느슨), τ<n_steps/2, ESS>50.

## 산출물
- simulations/L374/run.py — emcee 실행 + 진단.
- results/L374/report.json — 수치 결과.
- results/L374/REVIEW.md — 4 인 코드리뷰 자율 분담 결과.
- results/L374/ATTACK_DESIGN.md — 본 문서.

## 정직성 한 줄
이건 SQMH 물리 fit 이 아니라 emcee 파이프라인 smoke test 다. R-hat/ESS 가 통과해도
SQMH 이론에 대해서는 어떤 결론도 주장하지 않는다.
