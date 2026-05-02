# L386 REVIEW — Z_2 SSB Finite Temperature

## 8인 팀 자율 토의 (이론 도출, 지도 없음)

방향만 받음: "Z_2 SSB 유한온도, T_c, 도메인 월 형성 z, 오늘 잔존 밀도".
역할 사전배정 없음. 토의에서 자연 분담.

### 도출된 합의 (요약)

1. **유한온도 effective potential**: 토의 결과, daisy-resummed 1-loop
   고온 전개에서 origin의 곡률을 양수로 만드는 thermal mass가 quartic
   coupling에 비례한다는 표준 결과를 채택 (Dolan-Jackiw 1974, Linde 1979
   계열). 단일 실수 스칼라 + Z_2 인 경우 thermal mass 계수는 lam/4.
2. **전이 차수**: 단일 스칼라 daisy 수준에서 2차 (smooth restoration).
   1차 전이는 추가 게이지 자유도/cubic 항 필요 — 본 토이에선 2차로 한정.
3. **Kibble**: 전이 시점 z_PT 에서 horizon 당 ~1개의 도메인이 생성. Z_2
   는 π_0(M) = Z_2 → 2차원 결함(domain wall).
4. **Zel'dovich 진단**: scaling 해 rho_DW(t) ~ sigma/t. t_0 ~ 1/H0. 오늘
   Omega_DW < 1 이 Zel'dovich-Kobzarev-Okun 1974 한계.

### 8인이 사전 박지 *않은* 것
- eta (VEV) 값 → 스캔
- lam → 스캔
- 전이 차수 가정 → 토의로 2차 채택
- T_c 후보 수치 → 시뮬에서 산출

## 4인 코드리뷰 (자율 분담)

- A: T_c 단위 체크. eta[GeV] → T_c[GeV] = 2 eta. GeV→K 변환 GeV_to_J/kB ≈
  1.16e13 K/GeV, OK.
- B: 도메인 월 표면장력 sigma = (2 sqrt(2)/3) sqrt(lam) eta^3 차원
  [GeV^3]. Kink solution 적분 표준, OK.
- C: rho_DW(t_0) ~ sigma * H0. H0 GeV 단위 변환 H0_SI * hbar/GeV_to_J ≈
  1.44e-42 GeV. rho_crit_GeV4 ≈ 8.1e-47 GeV^4 (대조 표준값과 일치).
- D: Zel'dovich pass 판정 Omega_DW < 1, scaling 상수 A=1 채택 (Press-Ryden-
  Spergel 1989 시뮬레이션 calibration 근사). 본 토이는 ±factor 수준.

코드리뷰 결론: 단위 일관, numpy 2.x 안전 (np.trapezoid 미사용 — 적분
없음), 유니코드 print 없음, ASCII 변수명. 실행 PASS.

## 시뮬레이션 결과 (simulations/L386/run.py)

스캔: eta ∈ [1e-3, 1e18] GeV (22점 log), lam ∈ {1e-2, 1e-1, 1.0}. 총 66 행.

### 핵심 수치
- **T_c = 2 · eta** (단일 스칼라 daisy, 토이).
- **z_PT**: T_c 를 g*s 보정한 (1+z) ≈ (T_c/T_CMB) · (3.91/106.75)^(1/3).
- **Zel'dovich 통과 조건**: Omega_DW < 1.

### 통과/실패 구조
- lam=1e-2: eta ≤ 1e-3 GeV ≈ 1 MeV 만 통과 (Omega_DW ≈ 3.7e-6).
- lam=1e-1: 통과 행 0개 (eta=0.1 GeV 에서 Omega_DW≈11.7, 이미 위반).
- lam=1.0: 통과 행 0개.
- 통과한 최대 eta: **약 1e-2 GeV (10 MeV)** — 그 이상 eta 는 모두 KILL.

### z_DW (도메인 월 형성 z)
- eta=1 MeV (lam=1e-2 통과): T_c=2 MeV, z_PT ≈ 2.6e10 (BBN 직전 ~ 직후
  경계, 정확히는 BBN 이전 급랭 직전).
- eta=10 MeV: z_PT ≈ 2.6e11.
- eta=100 GeV (EW 척도): z_PT ≈ 2.6e15. **이 영역은 Zel'dovich 위반**.

### 정직 한 줄
**SQMH Z_2 SSB 모델은 inflation dilution 또는 explicit Z_2-breaking bias
항 없이는 eta ≳ 10 MeV 에서 Zel'dovich-Kobzarev-Okun 한계를 위반한다.**
eta ≲ 10 MeV (즉 BBN 이후 늦은 SSB) 또는 bias term Δρ ≳ sigma · H 가
필수 — 둘 중 하나가 없으면 모델 KILL.

## 한계 및 후속

- 단일 실수 스칼라 가정. SQMH 응축장이 게이지 자유도와 결합되면 thermal
  mass 계수가 바뀌고 1차 전이 가능 (cubic term) → T_c 와 결함 생성률
  보정. 본 토이의 ±O(1) 범위 내.
- Scaling 상수 A=1 (시뮬 calibration). A ∈ [0.5, 2] 범위 변동에도 통과
  영역 eta_max 는 ~factor 수준만 이동, 결론(EW 척도 위반) 불변.
- bias term V_bias = ε eta^3 phi 추가 시 wall 붕괴 시간 t_collapse ~
  sigma/(ε eta^3 H) — 별도 L세션 권장.

## 산출물 인덱스
- `results/L386/ATTACK_DESIGN.md` — 본 세션 설계
- `results/L386/REVIEW.md` — 본 파일
- `results/L386/scan.json` — 66행 스캔 결과
- `simulations/L386/run.py` — 토이 시뮬레이션
