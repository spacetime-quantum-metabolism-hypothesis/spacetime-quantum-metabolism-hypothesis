# L448 — BTFR Zero-Point (a_0 Intercept) A Priori Test

## 배경

- **L422 (slope test)**: SPARC 175갤럭시 BTFR slope 결과
  - bisector slope = 3.576 (Q≤2, n=129) / 3.700 (Q=1, n=87)
  - 예측 4.0 대비 −10 ~ −7%, K1/K2 모두 FAIL
  - 그러나 "intercept_fixed4" 채널은 slope=4 강제 시 a_0 회수 가능
- **L423 (a_0_eff fit)**: deep-MOND `V^4 = G·M_b·a_0_eff` 직접 피팅
  - 전체 n=135 → a_0_eff = 1.356e-10 m/s²
  - Q1 (n=87) → 1.420e-10
  - Q2 (n=42) → 1.269e-10
- **SQT a priori (H_0 = 67.4)**: a_0_SQT = c·H_0/(2π) = 1.0422e-10 m/s²
- **McGaugh 관측값**: 1.20e-10 m/s²

→ slope 채널은 죽었다. **intercept(zero-point) 채널만 단독 평가**.

## 핵심 질문

zero-point 일치도 a priori 정량화:
1. SPARC a_0_eff 대비 SQT a_0 의 비율 = 1.0422/1.357 ≈ **0.768** (≈ −23%)
2. McGaugh 관측 1.20e-10 대비 SQT 0.868 ≈ −13%
3. 이 차이가 통계적 유의(>2σ)인가, 체계오차 안인가?

## 후보 PASS 시나리오

A. **순수 a priori PASS (Tier-1)**: a_0_eff = 1.04e-10 ± < 30% 범위에 SQT 가 들어감 (jackknife/bootstrap σ 기준)
B. **체계오차 흡수 PASS (Tier-2)**: Υ★ ∈ [0.3, 0.7] 또는 H_0 ∈ [67.4, 73.0] 변동으로 SQT-관측 거리 1σ 이내
C. **FAIL**: 모든 합리적 nuisance 범위에서 ≥ 2σ 차이

## 측정 항목 (코드 출력)

1. **fixed-slope-4 intercept** + jackknife σ + bootstrap σ → a_0_eff ± σ
   - cut A (Q≤2), cut B (Q=1), cut C (Q≤3, 전체)
2. **distance from SQT a_0** in σ units (sigma_distance)
3. **Υ★ sensitivity scan**: Υ★ ∈ {0.30, 0.40, 0.50, 0.60, 0.70} 에서 a_0_eff 재계산
4. **H_0 sensitivity**: SQT a_0 가 a_0_eff 를 재현하는 H_0_required 역산
5. **ratio histogram**: 갤럭시별 a_per = V^4 / (G·M_b) 의 분포 → median, 16/84 percentile
6. **K-기준 (zero-point only)**:
   - K_Z1: |a_0_eff − a_0_SQT| / a_0_eff ≤ 0.30 (30% band)
   - K_Z2: a_0_SQT 가 a_0_eff 의 bootstrap 2σ 안
   - K_Z3: McGaugh 1.20e-10 까지 포함하면 SQT 가 1σ 안
   - K_Z4: 합리적 Υ★ ∈ [0.4, 0.6] 변동에서 K_Z1 안정

## 팀 운영

L448 단일 세션 — 코드 작성 + 결과 해석. 4인팀 코드리뷰 자율 분담은 NEXT_STEP 에서 명시 (실제 별도 세션 트리거).

## 정직 한 줄

slope 가 죽은 BTFR 에서 intercept(zero-point) 만 단독으로 SQT a priori 가 통과 가능한가를 정량 측정한다.
