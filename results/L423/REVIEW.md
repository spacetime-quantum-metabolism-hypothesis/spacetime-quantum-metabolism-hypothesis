# L423 REVIEW — 4인 코드리뷰 + 실행 결과 (자율 분담)

목적: 8인 ATTACK_DESIGN + NEXT_STEP 단계 1+2 의 4인 자율 분담 실행 검토.

## CLAUDE.md 준수 확인
- 사전 역할 배정 없음. 4인이 자율 분담으로 (a) 데이터 파싱, (b) M_bar 산출,
  (c) WLS/AICc 피팅, (d) 결과 plot/JSON 저장 분담.
- 시뮬레이션 결과가 8인 가설과 다르면 정직 기록 (base.fix.md 정신).

## 입력
- SPARC catalog: simulations/l49/data/sparc_catalog.mrt (175 은하).
- Rotation curves: simulations/l49/data/sparc/*_rotmod.dat.

## 실행
- 명령: `python3 simulations/L423/run.py`
- 결과: `results/L423/L423_results.json`, `figures/L423_tully_fisher.png`.

## 처리 흐름
1. catalog 끝의 `------` 구분자 다음부터 whitespace split 으로 175 행 파싱.
2. 각 행에 대해 rotmod 파일 outer 점에서 baryonic mass 계산:
   `V_bar^2(R_out) = V_gas|V_gas| + Y_d V_disk|V_disk| + Y_b V_bul|V_bul|`,
   `M_bar(<R_out) = V_bar^2 R_out / G`. (Y_d=0.5, Y_b=0.7 SPARC 기본.)
3. Vflat>0 + Mbar>0 필터로 135 은하 분석 sample 확정 (40 은하는 카탈로그
   Vflat=0 이거나 outer V_bar^2≤0 으로 제외).
4. 모델 A (n=4, m=1 고정, a0_eff 만 자유) WLS 피팅.
5. 모델 B (slope a=m/n 자유, intercept 자유) WLS 피팅.
6. jackknife 로 slope σ.
7. AICc 비교 + Q-flag 분리 sub-fit.

## 핵심 결과
- N = 135.
- 모델 A: a0_eff = 1.356e-10 m/s^2 (MOND 기준값 1.2e-10 의 +13%).
- 모델 B: slope m/n = 0.2689 ± 0.0080 (jackknife 1σ).
  - MOND/SQT 사전 0.25 와의 거리 ≈ 2.4σ.
- ΔAICc (B - A) = -146.5 → 데이터가 자유 slope 를 강하게 정당화.

## Q-flag 분리 (sanity check)
- Q=1 (n=87, highest quality): slope = 0.2568 → MOND prior 0.25 와 1σ 내.
  implied a0 = 1.42e-10.
- Q=2 (n=42, medium): slope = 0.2853 → MOND prior 와 ~4σ 이탈.
  implied a0 = 1.27e-10.
- Q=3: 데이터 부족.
- 해석: 전체 sample 의 slope 이탈은 주로 Q=2 의 측정 잡음/계통오차에서
  유래. Q=1 only 분석에서는 (n=4, m=1) 형태가 통계적 등가.

## 8인 공격에 대한 응답
- 공격 1 (TF exponent uniqueness): 데이터는 sample 정의에 따라 0.25 또는
  0.27. SQT 만의 차별성이라고 주장 불가 — MOND deep limit 와 동일 phenomenology.
- 공격 5 (sub-leading correction): 본 실행은 outer 단일점만 사용. 미세항
  분석은 NEXT_STEP 단계 3-4 (잔차 R 의존, Σ_disk 상관) 에서 다음 사이클.
- 공격 8 (통계적 등가성): Q=1 sub-sample 에서 (4, 1) 등가, full sample
  에서 비등가. cutoff/품질 기준에 결과가 의존 — 데이터 정의 문제.

## 정직 한 줄
**SPARC outer V_flat = (G M a0)^{1/4} 형태는 SQT 만의 차별성이 아니다.
Q=1 sample 에서 (n=4, m=1) 등가, full sample 에서 slope 0.269 ± 0.008,
a0_eff = 1.36e-10 m/s^2 (MOND 1.2e-10 와 13% 일치). MOND/Verlinde/SQT 의
phenomenological 등가성 영역. SQT 차별성은 sub-leading 잔차 (NEXT_STEP
단계 3-4) 에서만 검증 가능.**

## 코드 검증 노트 (4인 자율)
- A: parse_catalog 가 fixed-byte 가 아닌 whitespace split — MRT 헤더
  byte 범위가 실제 파일 컬럼과 정확히 align 안 됨을 확인하고 수정.
- B: outer M_bar 추정 시 V_disk^2 부호 보존 (`V|V|`) 으로 counter-rotating
  bin 처리.
- C: σ_lnV 에 0.02 floor (e_Vflat=0 보고된 catalog 행 보호).
- D: AICc 패널티 명시 (CLAUDE.md 과적합 방지 규칙). chi2_A vs chi2_B
  단순 차이 아닌 AICc 로 비교.
- 추가 ToDo: NEXT_STEP 단계 3 (residual vs M_bar/Σ/Q 상관) 다음 세션.

## 산출물
- /Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L423/ATTACK_DESIGN.md
- /Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L423/NEXT_STEP.md
- /Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L423/REVIEW.md (this)
- /Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L423/L423_results.json
- /Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/simulations/L423/run.py
- /Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/figures/L423_tully_fisher.png
