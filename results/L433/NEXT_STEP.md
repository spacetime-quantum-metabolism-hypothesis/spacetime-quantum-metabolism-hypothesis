# L433 NEXT_STEP — 8인팀 자율 다음 단계 설계

**전제**: ATTACK_DESIGN.md 결론 = 현재 0.7% 는 fit-induced descriptive label.
**목표**: matter era φ 진화를 정량화하고 δr_d/r_d 와 δθ_*/θ_* 를 *axiom + 한 개의 BAO-fit 파라미터* 만으로 forward 계산하는 절차 정의.
**원칙 준수**: 수식/유도 경로/파라미터 값 사전 지정 금지 (CLAUDE.md 최우선-1, 최우선-2). 본 문서는 *방향 명시* 만 한다.

---

## A. 8인팀 자율 합의 — 정량화 단계 (방향만)

### Step 1 — matter era φ(z) 진화의 정의 채널 결정
- 8인팀이 자유롭게 도출할 채널 후보 (이름만 제공, 식은 팀이 도출):
  - quintessence slow-roll matter-era track (Phase 2 근사),
  - coupled IDE 잔여 channel (Phase-2 BAO ξ_q 직접 상속),
  - disformal pure-A'=0 한도 (배경에서 minimally coupled 와 동일).
- **금지**: Phase 2 sim 의 ξ_q 수치를 그대로 입력으로 박아넣기. 채널 형태만 일치, 파라미터는 새로 marginalise.

### Step 2 — drag epoch z_d 와 recombination z_* 분리
- 두 적분 (r_d = ∫_{z_d}^∞ c_s/H dz, r_s(z_*) = ∫_{z_*}^∞ c_s/H dz) 를 *각각* 계산.
- baryon-photon plasma 에서 c_s 는 SQMH 변형 *없음* (T^α_α≈0 radiation-era). 따라서 변화는 H(z) 뿐.
- δr_d/r_d 와 δr_s(z_*)/r_s(z_*) 의 *비율* 은 axiom 만으로 결정 (관측 입력 0).

### Step 3 — D_A(z_*) cancellation 정량화
- θ_* = r_s(z_*) / D_A(z_*). δθ_*/θ_* = δr_s/r_s − δD_A/D_A.
- late-time DE 변형이 D_A(z_*) 에 cancel 효과를 주는지 *부호와 자릿수* 만 확인 (값 사전 지정 금지).
- cancellation 이 부분적이면 δθ_* << δr_d 가능 → "Planck σ × 23" 자체가 over-statement 일 수 있음.

### Step 4 — BAO 채널 1개 파라미터로 인덱싱
- Phase 2 BAO posterior 가 제공하는 *최소 1개 dynamical 파라미터* (예: ξ_q 또는 β 중 팀이 선택) 를 input.
- 그 1개 파라미터로 δr_d 와 δr_s(z_*) 를 *동시* 도출 → 두 관측 사이 *상관* 이 prediction 의 핵심.
- "0.7%" 는 이때 *상관 함수의 한 점* 으로 도출되어야 하지, 절댓값이 자체 prediction 은 아님.

### Step 5 — 부호 prediction 명시
- matter→DE 에너지 흐름 부호 (axiom 4 mass-action 방향) 가 δr_d 부호를 결정한다.
- 8인팀이 axiom 부호규약 (xi_q ≥ 0, β ≥ 0) 으로부터 δr_d 부호를 *유도* — 결과 부호를 본 문서에 사전 기입 금지.

### Step 6 — Forecast band 작성
- LiteBIRD / CMB-S4 / SPT-3G 등 후속 CMB 의 *θ_* 정밀도 향상* 정량 (공개된 forecast 만 인용).
- (δr_d/r_d)_predicted 가 그 정밀도와 비교될 수 있는지 — 비교 불가능하면 falsifiability 부재 인정.

---

## B. 4인팀 코드리뷰 자율 분담 (Rule-B, 역할 사전 지정 없음)

simulations/L433/run.py 의 forecast 코드를 4인이 자유 분담으로 검토:

- (i) 적분 grid (z_d, z_* 분리, N_GRID, c_s(z) 적분 누락 여부),
- (ii) 단위 일관성 (Mpc / km/s/Mpc),
- (iii) sentinel 값 처리 (ODE 폭주 시 NaN 처리),
- (iv) "Planck σ × N" 의 σ 정의 명시 + 재현성.

**금지**: 역할 사전 배정 (ex: "데이터 로딩 담당", "chi² 담당"). 4인이 자율 분담.

---

## C. 결정 게이트

L433 forecast (simulations/L433/run.py) 결과로:

- (G1) matter-era φ 채널이 *axiom + 1 파라미터* 만으로 δr_d/r_d 를 forward 계산할 수 있는가?
- (G2) δθ_*/θ_* 가 D_A cancellation 후에도 Planck σ 의 몇 배인가?
- (G3) Forecast band 가 적어도 1 개 후속 CMB 실험에서 falsify 가능한가?

**G1 PASS + G2 ≥ 3σ + G3 PASS** → PARTIAL 유지 + caveat 약화.
**G1 PASS + G2 < 1σ** → 등급 격하 (PARTIAL → CONSISTENCY_CHECK).
**G1 FAIL** → PARTIAL → POSTDICTION 강제.

판정 식별자/숫자는 run.py 출력 후 REVIEW.md 에서 결정.
