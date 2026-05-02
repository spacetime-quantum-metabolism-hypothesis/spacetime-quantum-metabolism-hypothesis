# L422 ATTACK_DESIGN — BTFR slope as SQT a priori test

## 8인 공격 설계 (자율 분담)

본 절은 SQT 의 BTFR (Baryonic Tully-Fisher Relation) slope=4 주장을 reviewer 입장에서 공격 가능한 모든 각도를 정리한다. 8인은 역할 사전 지정 없이 자율 분담; 결과 합의 항목만 기록.

### A. "이건 fit 이지 prediction 이 아니다" 공격 (★ 최강)

A1. **Postdiction 의심**. 1977 Tully-Fisher 가 알려진 후 30년 fit 으로 slope ≈ 4 가 관측 정착됨. SQT 가 "도출했다" 고 주장하려면 데이터를 보지 않은 상태의 a priori 도출이 가능했는지 입증해야 한다.

A2. **MOND 와의 형식 동일성**. V^4 = G·M·a_0 는 MOND deep-MOND 한계에서 정확히 같은 형태. SQT 의 도출이 MOND 보다 더 근본적이다는 증명 필요. 단순 동일 공식 재유도는 prediction 으로 인정 안 됨.

A3. **a_0 자유도 잔존**. SQT 가 a_0 = c·H_0/(2π) 를 도출하더라도, BTFR 정규화에 들어가는 실제 가속도는 SPARC sample-best-fit a_0 와 비교돼야 한다. 둘이 일치하지 않으면 normalization fit 으로 회귀.

### B. 데이터 처리 비판

B1. **Quality cut 종속성**. SPARC 175 전체와 Q=1 (90개) 결과가 다르면 sample 선택으로 slope 가 변동. 두 cut 을 모두 보고하지 않으면 cherry-picking 의심.

B2. **Υ_3.6 불확실성**. M_star = Υ × L_[3.6] 의 Υ 가 0.3–0.7 사이에서 불확실. Υ 조정만으로 slope 가 변동하면 자유 parameter.

B3. **Distance error**. SPARC distance modulus 는 e_D ~ 5–30%. log M_b 에 직접 들어가 BTFR 산점도 dominant scatter 원인. 거리오차 무시한 OLS fit 은 slope 편향.

B4. **Inclination correction**. V_flat 은 sin(i) 로 보정. e_Inc ~ 5–10° 이 포함된 V 오차 처리 필요.

B5. **Selection effect**. SPARC sample 은 Vflat 측정 가능한 disk-dominated galaxy 만. dwarf 와 massive 양 끝 절단 시 slope 가 hourglass 형태로 변동.

### C. 통계 비판

C1. **OLS vs orthogonal vs bivariate**. log-log 회귀는 어떤 estimator 를 쓰는가에 따라 slope 가 ±0.2 변동. 반드시 모든 3종 보고.

C2. **Inverse fit 이슈**. y|x vs x|y forward/reverse fit slope 의 평균은 orthogonal 과 다름. 한쪽만 보고하면 편향.

C3. **AICc / BIC**. slope=4 fixed 모델 vs slope free 모델 비교. Δχ² ≤ 2k 이면 free slope 를 쓸 정당성 없음 → fixed 4 채택. SQT 의 a priori slope=4 가 이 선에서 PASS 해야 한다.

### D. 이론적 비판

D1. **n^4 도출의 robustness**. SQT 가 어떤 미시 메커니즘으로 V^4 ∝ M·a_0 를 도출하는지. 다른 SQT 변형 (V^3, V^5) 가 가능하지 않은지.

D2. **Universe-scale a_0 vs galaxy-scale a_0**. c·H_0/(2π) 는 cosmological scale. 은하 회전 속도가 cosmological a_0 에 lock 되는 메커니즘이 SQT axiom 에서 자연 도출되는지.

D3. **scatter 예측 부재**. SQT 가 slope 만 예측하고 intrinsic scatter (~0.1 dex 관측) 를 예측하지 못하면 부분 PASS.

### 8인 합의 reviewer 시나리오

가장 치명적 비판: **A1 (postdiction) + A2 (MOND 와 동일 형식)**. 이 둘을 동시 회피하려면

1. SQT 의 V^4 = G·M·a_0 도출이 MOND 가속 보간함수 ν(x) 와 무관한 독립 경로임을 명시.
2. SPARC 정량 fit 결과가 slope = 4.00 ± δ (δ < 0.2) 와 a_0 = (1.2 ± 0.2) × 10⁻¹⁰ m/s² 동시 일치.
3. AICc 비교에서 "slope free" 모델이 "slope=4 fixed" 모델 대비 ΔAICc < 2 (free 가 정당화 안 됨).

위 3 조건 만족 시 PASS_STRONG 격상 가능. 하나라도 실패 시 현 등급 (§4.1 row 2 PASS_STRONG postdiction caveat) 유지.

## 정직 한 줄
8인 합의: BTFR slope=4 의 PASS_STRONG 격상은 SPARC 정량 fit 이 (slope, a_0) 동시 일치 + AICc 가 fixed-4 를 정당화할 때만 가능. fit 결과로 결정.
