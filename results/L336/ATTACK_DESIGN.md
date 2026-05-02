# L336 ATTACK DESIGN — SPARC + DESI + Planck + Cluster + Anchor Full Joint MCMC

## 1. 동기

L328 결과: subset-specific Bayes factor 가 데이터셋마다 일치하지 않음.
- ΔlnZ_full ≈ +0.8 (전체 marginalized, 약한 선호)
- ΔlnZ_SPARC-only effectively negative (SPARC 단독에서는 LCDM/MOND 가 우위)
- BAO/CMB 단독 ΔlnZ 는 SQT 쪽이 marginal positive

→ 후보 모델이 "데이터셋 평균" 으로만 살아 있는지, 아니면 *진짜 global posterior* 에서 단일 점이 모든 채널을 동시에 설명하는지 확인 필요.

L336 의 목적은 5개 데이터셋을 단일 likelihood 로 결합한 **full joint posterior** 를 산출하여 다음을 답하는 것이다.
1. 전체 데이터에서 SQT 파라미터의 1D/2D marginal 이 실제로 LCDM 영점(예: psi^n 결합 0)과 분리되는가?
2. 채널 간 tension (Q_DMAP) 이 LCDM 대비 줄어드는가, 늘어나는가?
3. ΔlnZ_full 의 부호가 SPARC inclusion 후에도 양으로 유지되는가?

## 2. 데이터셋 구조 (5채널)

| Tag | 데이터 | N (effective) | Likelihood 형태 |
|---|---|---|---|
| D1 SPARC | 175 회전곡선 (Lelli+16) | ~3000 v(r) 점 | per-galaxy Gaussian + ϒ⋆ nuisance |
| D2 BAO  | DESI DR2 13pt + cov | 13 | full Gaussian (D_M/r_d, D_H/r_d, D_V/r_d) |
| D3 SN   | DES-Y5 (zHD frame) | ~1800 | analytic-marginalized M, full cov |
| D4 CMB  | Planck compressed (R, l_A, ω_b, n_s) | 4 | Gaussian + Hu-Sugiyama z_* + 0.3% theory floor |
| D5 RSD  | fσ8 compilation (BOSS+eBOSS+DESI) | ~12 | Gaussian + growth ODE |

> Cluster (mass function / counts) 와 cosmic anchor (SH0ES H0, BAO+BBN sound-horizon prior) 는 D4/D5 옆에 옵션 채널 (D6, D7) 로 두지만, 메인 run 에서는 D4 의 ω_b prior 와 RSD 만 사용. D6/D7 은 ablation 으로.

전체 nuisance:
- 175 × ϒ⋆ (SPARC) — 각 갤럭시 lognormal prior σ=0.11 dex
- M_B (SN)  — 해석 marginalize
- A_planck-like 없음 (compressed)
→ free nuisance ≈ 175.

cosmology + theory:
- Ω_m, h, ω_b
- SQT 파라미터 (4–6개): {n_index, A_amp, z_pivot, β_dark, …} 후보별로 다름

총 차원 d ≈ 6 + 175 = 181.

## 3. 결합 likelihood

ln L_total(θ_cosmo, {ϒ⋆,i}) =
  Σ_i ln L_SPARC,i(ϒ⋆,i, θ_cosmo)
  + ln L_BAO(θ)
  + ln L_SN(θ)            (M analytic-marg)
  + ln L_CMB(θ)
  + ln L_RSD(θ)

가드:
- chi2 실패 / E(z) ODE 폭주 / c_s² < 0 / G_eff 음수 → 즉시 -inf return (sentinel 합산 금지, L4 재발방지).
- SPARC ϒ⋆ 는 hierarchical Gaussian prior (no flat).

## 4. 샘플러 선택

### 4.1 emcee (1차 후보)
- 1000 walker × 10000 step (요청).
- d=181 에 대해 walker ≥ 2d 권장 → 1000 충분.
- thin=20, burn-in=2000.
- stretch move 만 쓰면 ϒ⋆ subspace 가 거의 conditional Gaussian → DE-MCMC 더 효율, 그러나 첫 시도는 stretch 그대로.
- np.random.seed(42) emcee 내부 강제 (L4 재발방지).
- backend = HDF5 (`.h5`, blob = 채널별 chi².)

### 4.2 dynesty (2차, evidence 정밀)
- 5채널 ΔlnZ 를 직접 얻으려면 nested sampling 이 필수.
- d=181 직접 nested 는 비현실 → **two-stage**:
  1. SPARC ϒ⋆ 175개를 per-galaxy analytic profile likelihood 로 marginalize (Gaussian-in-ϒ⋆ 닫힌 형식).
  2. 남는 d ≈ 6–10 차원에서 dynesty `dynamic` (nlive=1500, dlogz=0.05).
- rstate = np.random.default_rng(seed) (L5 재발방지).

권장: emcee 로 posterior, dynesty 로 evidence (양쪽 cross-check).

## 5. Convergence Diagnostics

- Gelman-Rubin R̂: walker 를 4 sub-chain 으로 나눠 cosmology 6차원 + 대표 ϒ⋆ 5개에 대해 계산. 통과 기준 R̂ < 1.05 (L6 K13 의 1.3 fail 재발방지).
- IAT (autocorr_time): N_eff = N_step / τ ≥ 50 per param.
- KS test on second-half vs first-half walkers.
- Posterior predictive: BAO, RSD, CMB compressed 잔차의 χ²_pred 분포가 각 채널 N_dof 와 일관한지.

## 6. Cross-Dataset Tension Metrics

### 6.1 Q_DMAP (Raveri-Hu 2019)
Q_DMAP = 2 [ln L_max(combined) − Σ_d ln L_max(d alone)]
- 채널별 단독 best-fit 대비 결합시 likelihood penalty.
- LCDM 과 SQT 모델 두 값 비교, ΔQ_DMAP = Q_SQT − Q_LCDM.
- ΔQ_DMAP < 0 → SQT 가 채널간 tension 을 완화.

### 6.2 Suspiciousness S
S = D − d_eff, D = 2 KL(P || π).
- BAO+CMB+SN+RSD vs SPARC pair 에 대해 따로 계산.

### 6.3 Posterior shift
SPARC inclusion 전후 cosmology 6D posterior mean shift / σ. > 2σ 이면 SPARC ↔ 우주론 채널 tension.

## 7. Computational Budget

per likelihood call:
- BAO: ODE solver E(z) (z up to 1100) ~ 5 ms
- SN: integral over 1800 zHD with cached E(z) ~ 1 ms
- CMB: theta_* + R, l_A ~ 2 ms (재사용)
- RSD: growth ODE ~ 3 ms
- SPARC: 175 gal × MOND/SQT mass-model eval ~ 80 ms (dominant)
→ total ≈ 90 ms / call.

emcee:
- 1000 walker × 10000 step = 10^7 calls.
- 90 ms / call × 10^7 = 9×10^5 s ≈ 250 hr single-thread.
- 9-process pool (10코어, OMP=1, L0 규칙) → 28 hr.
- ϒ⋆ analytic-marg 적용 시 SPARC 비용이 1/5 → 6 hr.
→ **현실 budget: ~18–24 hr (analytic-marg 미적용시), ~6 hr (적용시).**

dynesty 2nd stage (d≈8, nlive=1500):
- 통상 ~10^5–10^6 calls.
- analytic-marg 후 30 ms/call → 1–8 hr.

총 walltime: **12–28 hr (SQMH 기준 budget 12–24 hr 부합).**

## 8. 실행 단계 (proposed)

1. **Stage A** (1 hr): SPARC per-galaxy Gaussian-in-ϒ⋆ analytic marginalizer 작성 + 단위테스트. LCDM/MOND/SQT 각 ϒ⋆ profile 일치 검증.
2. **Stage B** (2 hr): 5채널 결합 likelihood 빌드. 채널별 chi² blob 저장. -inf 가드.
3. **Stage C** (1 hr): smoke-test — 100 walker × 200 step 에서 R̂, IAT 측정, time/call 실측.
4. **Stage D** (18 hr): production emcee 1000 × 10000.
5. **Stage E** (6 hr): dynesty nested (cosmology only, ϒ⋆ marg 후).
6. **Stage F** (2 hr): Q_DMAP, Suspiciousness, posterior plots, cross-dataset shifts.

## 9. Falsifiable Pass/Fail

후보 SQT 모델은 다음 4개 동시 통과해야 L337 진출.
- F1. R̂ < 1.05 (모든 cosmology 파라미터)
- F2. ΔlnZ_full > +1 (Jeffreys "substantial")
- F3. ΔQ_DMAP < 0 (tension 비악화)
- F4. SPARC subset Bayes factor 와 BAO/CMB subset Bayes factor 부호 일치 (L328 모순 해소)

하나라도 fail 시 L336 결과는 "global 단일 점에서 sustainable 하지 않음" 으로 정직 보고.

## 10. 8인/4인 리뷰 게이트

- Rule-A 8인: F1–F4 판정, Q_DMAP 해석, paper-level claim.
- Rule-B 4인: likelihood 모듈, ϒ⋆ analytic-marg 식, dynesty rstate, R̂ 계산 코드.
리뷰 통과 전 논문 본문 반영 금지 (L6 재발방지).
