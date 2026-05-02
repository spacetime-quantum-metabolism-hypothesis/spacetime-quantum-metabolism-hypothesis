# L376 ATTACK DESIGN — proper Laplace lnZ for 5 cosmology models (BMA)

## 상위 컨텍스트
- L340 baseline: BIC + Laplace(5sigma prior) + AIC 셋으로 4-model BMA 산출.
  BB(3-regime) BIC weight 92.6%, Laplace weight 81.1%.
- L341 SYNTHESIS: 본문 baseline 은 BB *2-regime* (3-regime alternative + 부록).
- L367 reverse: baseline 을 다시 *3-regime* 로 (RG saddle 동기, caveat 명시).
- 사용자 요청 (L376): BB-3regime 와 BB-2regime 을 *함께* 5-model BMA 에 포함.
  smooth, LCDM, MOND 까지 5 모델. proper Laplace lnZ 와 posterior weight 정량.

L340 의 5 모델은 (BB, smooth, LCDM, MOND, SymG) 였다. L376 은 (BB-3regime,
BB-2regime, smooth, LCDM, MOND) — SymG 빼고 BB 변종 두 개 분리.

## 입력 chi2, k

| 모델          | chi2     | k | 출처                                                 |
|---------------|----------|---|------------------------------------------------------|
| BB-3regime    | 1745.00  | 3 | L196/L281 family best-fit (L340 입력값과 동일)       |
| BB-2regime    | 1746.23  | 2 | L322 ΔAICc(M3-M2)=+0.77 → chi2_2 = chi2_3 + 1.23     |
| smooth (5p)   | 1742.00  | 5 | L340 입력값                                          |
| LCDM          | 1758.00  | 2 | L340 입력값                                          |
| MOND          | 1762.00  | 2 | L340 입력값                                          |

N_data = 1756 (BAO 13 + SN 1735 + CMB 2 + RSD 6).

BB-2regime chi2 도출 근거:
- L322 multistart_result.json: 합성 chi^2 표면에서 chi2_M3=0, chi2_M2=1.281,
  AIC = chi2 + 2k → ΔAIC(M3-M2) = (0+6) - (1.281+4) = +0.719 ≈ +0.77 (AICc 보정 후).
- 따라서 실측 joint chi2 차이 chi2(2-reg) - chi2(3-reg) ≈ +1.23.
- BB-3regime chi2=1745.0 이면 BB-2regime chi2 ≈ 1746.23.

## 방법: proper Laplace ln Z

표준 Laplace 근사 (Gauss posterior 가정):
    ln Z ≈ -0.5 chi2_min + 0.5 k ln(2 pi) - 0.5 ln det(Fisher) + ln(1/V_prior)

prior box width W_i 와 posterior std sigma_i (Fisher^{-1/2}) 비율을 r_i = W_i/sigma_i
로 두면, k 차원에서 두 항이 합쳐:
    ln Z ≈ -0.5 chi2_min + sum_i ln(sigma_i sqrt(2 pi) / W_i)
         = -0.5 chi2_min - sum_i ln(r_i / sqrt(2 pi))

prior 가 모든 파라미터에 대해 균일하게 r_i = R (같은 ratio) 라 가정하면:
    ln Z ≈ -0.5 chi2_min - k * ln(R / sqrt(2 pi))
         = -0.5 chi2_min - k * (ln R - 0.5 ln(2 pi))

L340 의 R=5 가정 (prior=5 sigma) 을 그대로 쓰면:
    ln(5/sqrt(2 pi)) = ln 5 - 0.5 ln(2 pi) = 1.6094 - 0.9189 = 0.6905

→ Occam 패널티 per param ≈ 0.69 (Bayesian)
   참고: BIC 패널티 per param = 0.5 ln(N) = 0.5 * 7.471 = 3.74 (훨씬 강함)

L376 은 R=5 baseline 외에 R=3, R=10 sensitivity 를 함께 보고 → robustness 확인.

## 산출 항목 (report.json)

1. 모델별 (chi2, k, AIC, AICc, BIC).
2. 모델별 ln Z (Laplace) 세 가지: R=3, R=5, R=10.
3. 5-model posterior weight (각 R 마다).
4. BB 합산 weight (BB-3regime + BB-2regime) — "BB family" 정량.
5. delta lnZ (best - X) 표.
6. 정직 verdict 한 줄.

## 합격 기준 / 정직 가드
- C1: 모든 lnZ finite, 합산 weight = 1.0 (1e-9 이내).
- C2: BB family weight 가 R 에 강하게 의존 (R=3: BB 강세, R=10: smooth 약진).
- C3: BB-2regime vs BB-3regime 비교: AIC 패널티는 Akaike-equivalent, Bayesian
  Occam 으로는 BB-2regime 이 k=2 로 더 simple → R 작아질수록 BB-2regime 우세.
- C4: 정직 한 줄 — "어떤 R 에서 BB family 가 dominant 인지, 어디서 깨지는지"
  명시.

## 8인 사전 합의 (방향만)
- 본 loop 는 L340 후속, BB family 분해 정량화. 새 이론 없음.
- chi2 입력값은 기존 결과 인용 — 재계산 아님.
- BB-2regime chi2 는 L322 ΔAICc 로부터 *유도* — 실제 joint MCMC fit 결과 아님.
  caveat 명시.

## 정직성 한 줄
실측 chi2 는 L340/L196 인용. BB-2regime chi2 는 L322 합성 ΔAICc 로 유도된 *근사*
이며 joint MCMC 직접 fit 아님. R=5 baseline 외 sensitivity (R=3, R=10) 함께 보고.
