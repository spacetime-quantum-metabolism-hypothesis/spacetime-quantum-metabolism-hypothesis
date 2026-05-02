# L340 — Bayesian Model Averaging (proper, 5 모델)

## 컨텍스트
- L196: Akaike weight BB=99.9998%, Gaussian dip=1.9e-6, Quadratic/Cubic ~0. → "BB 100%" narrative.
- L281: marginalized Laplace ΔlnZ(BB−smooth)=+0.8 (Bayes factor ~2.2). 격하.
- L340: smooth/LCDM/MOND/SymG 까지 후보 확장한 *proper* BMA. Akaike weight 폐기, marginalized lnZ 사용.

## 8인 공격 라인업
- A1 (P, proponent): BB 5-모델 비교에서도 살아남는가?
- A2 (N, nihilist): MOND 가 BB 와 유사한 wa<0 을 만든다면 BMA 가 BB weight 을 절반 이하로 깎는다.
- A3 (O, Occam): 모델별 자유 파라미터 수 (k_BB=3, k_smooth=5, k_LCDM=2, k_MOND=2, k_SymG=4) 패널티 정확 적용.
- A4 (H, honesty): "BB 100%" 라는 이전 narrative 가 marginalized 5-모델에서 정량 얼마인가?
- A5 (B, Bayesian): prior volume ratio — flat prior box 동등 폭 가정 정당화.
- A6 (S, sampler): Laplace 근사가 multi-modal 사후에서 깨지는 위험.
- A7 (D, data): 데이터 (BAO+SN+CMB+RSD compressed) 동일 채널 사용 — chi² 비교 fair.
- A8 (T, theorist): SymG 4-param 이 over-fit 되어 lnZ 가 패널티로 BB 보다 낮게 나오는지 확인.

## Top 3 (A1, A3, A4)
- A1: BB 가 5-모델 BMA 에서 50% 이상이면 paper narrative "BB favored, modest" 유지 가능.
- A3: Occam penalty per param ≈ 0.5 ln(N_eff) ≈ 0.5·ln(40) ≈ 1.85 per added param.
- A4: 정량 weight 발표. 50% 미만이면 narrative 다시 격하.

## 방법
1. 각 모델의 best-fit chi² 와 |Hessian|^(-1/2) (Fisher) 로 Laplace lnZ 계산:
   ln Z ≈ −0.5 chi²_min + 0.5 k ln(2π) + ln|Σ|^(1/2) − ln V_prior.
2. 모든 모델 동일 prior volume box 가정 → V_prior 항 캔슬은 *불가능* (k 다를 때).
   대신 각 파라미터당 fiducial prior width σ_pri = 5 σ_post 가정 (uninformative).
   → ln V_prior_i = k_i · ln(5 √(2π) σ_post) 와 정확 캔슬되지 않음.
   실용 근사: ln Z_i ≈ −0.5 chi²_min,i − 0.5 k_i ln(N_data) (BIC-like) 로 전환.
3. 가장 보수적: BIC. ΔBIC = Δchi² + Δk·ln(N).
4. Posterior weight w_i = exp(−0.5 ΔBIC_i) / Σ exp(−0.5 ΔBIC_j).

## 데이터 가정
- N_data = 13 (DESI BAO) + 1735 (DESY5 SN) + 2 (compressed CMB θ*, R) + 6 (RSD) ≈ 1756.
- chi² 값은 L281/L196 family 에서 확인된 best-fit 사용.
  - BB (3-step): chi²_min ≈ 1745 (joint, L196 family)
  - smooth (5-poly): chi²_min ≈ 1742
  - LCDM (Om, h): chi²_min ≈ 1758
  - MOND (a0, M*): chi²_min ≈ 1762 (BAO+SN 만 fit, RSD/CMB 패널티)
  - SymG (4-param symmetron): chi²_min ≈ 1748

## 정직 조건
- BB weight ≥ 0.5 → narrative 유지
- 0.2 ≤ BB weight < 0.5 → "preferred but not dominant" 격하
- BB weight < 0.2 → narrative 또 격하 (paper 본문 재작성)
