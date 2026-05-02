# L381 — Cosmic shear xi_+(theta=10') SQT vs LCDM (L286 follow-up)

## 배경
L286 P19: Euclid σ_8 sensitivity 0.005, SQT μ_eff=1 (dark-only structural), Δμ_eff~1e-4. SQT는 ΔS_8 ≈ +1.14% (worsen). 그러나 σ_8/S_8 만으로는 cosmic shear 의 `theta` 의존성을 잡지 못함. real-space 2-point xi_+(theta) 가 Euclid/LSST 의 직접 관측량.

## 8인 공격 방향 (수식 금지)
A1: μ_eff(k,z) ≈ 1 (dark-only) 가정 하에서 P_m(k,z) 에 미치는 잔여효과는 sigma_8 shift 로 흡수되는가, 아니면 scale-dependent residual 이 있는가.
A2: SQT 배경 H(z), Omega_m(z) shift 가 lensing kernel q(z) 에 미치는 distance 효과.
A3: source redshift distribution n(z) Euclid (z_med~0.9) vs LSST Y10 (z_med~0.7) 이 차이 증폭/희석 방향.
A4: theta=10 arcmin 스케일 (l ~ 1000~2000) 에서 nonlinear regime 영향 (halofit / HMcode).
A5: Limber approximation 정확도 (theta=10' 에서 % 수준).
A6: tomographic vs single-bin signal-to-noise.
A7: shape noise (sigma_e, n_eff) — Euclid n_eff~30 / arcmin² , LSST Y10 n_eff~27.
A8: cosmic variance (survey area Euclid 15000 deg² , LSST 18000 deg²).

## Top-3 (실측 가능한 핵심)
A1+A2 통합: SQT 의 P_m(k,z) 와 H(z) 만으로 xi_+(theta) 직접 계산 → LCDM 차이 |Δxi_+/xi_+| 측정.
A4: nonlinear regime 처리 — halofit linear+nonlinear 모두 비교.
A7+A8: Euclid/LSST 의 1σ 통계오차 (cosmic variance + shape noise) 와 비교 → 신호/잡음.

## 권고
1. SQT 배경: L242 confirmed S_8 +1.14% shift 를 효과적 sigma_8 rescale 로 적용. dark-only μ_eff=1 가정 하에 P_m(k,z) shape 변경 없음 (linear theory 하).
2. LCDM fiducial: Planck 18 (Om=0.315, h=0.674, ns=0.965, sigma_8=0.811).
3. xi_+(theta) 계산: Limber + Hankel transform (J_0). theta = 10 arcmin. linear P_m 으로 충분 (10' ~ 1 Mpc/h scale, mildly nonlinear, linear approximation 으로 % 수준 비교는 정직).
4. n(z): Euclid Smail-type (alpha=2, beta=1.5, z0=0.64), LSST Y10 (z0=0.28, alpha=0.9, beta=2).
5. 1σ 추정: Gaussian covariance — sample variance (f_sky, l-binning) + shape noise. theta=10' 단일 bin 비교.
6. 산출: xi_+_SQT, xi_+_LCDM, Δxi/xi, sigma_Euclid, sigma_LSST, SNR_sigma = |Δxi|/sigma.

## 정직 한 줄
xi_+(10') 의 SQT vs LCDM 차이는 S_8 shift 1.14% 의 직접 결과 (xi_+ ∝ S_8^~2). Euclid/LSST 가 1σ 안에 검출 가능한지 정량.
