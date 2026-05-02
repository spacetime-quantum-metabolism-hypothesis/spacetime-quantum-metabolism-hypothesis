# L433 ATTACK_DESIGN — 8인팀 reviewer 공격 설계

**주제**: paper/base.md README L177 / §4.1 row 8 의 PARTIAL #6 = CMB θ_* shift, 즉 *δr_d/r_d ≈ 0.7% (Planck σ × 23)* 가 **predicted** 인지 **fit** 인지.
**목표**: 0.7% 라는 숫자가 SQMH axiom 으로부터 a priori 도출된 *예측* 인지, 아니면 BAO/Planck 잔차에 맞춰 사후 조정된 *피팅* 인지에 대한 reviewer 비판 시뮬레이션.
**방법**: 8인 자율 토의 (Rule-A). 역할 사전 지정 없음. 자연 분담된 비판 채널 8개 정리.

---

## 8인팀 자율 발생 비판 채널

### 비판 #1 — "Planck σ × 23" 라벨의 자기 폭로
표시 자체가 *Planck 의 θ_* 측정 정밀도 (≈ 3×10⁻⁶) 를 분모로 한 비교 단위* 다.
즉 SQMH 가 먼저 0.7% 를 *내놓은* 것이 아니라, Planck 의 σ 와 비교한 *결과* 를 라벨에 박았다.
**predicted 결과** 라면 단위는 "δr_d/r_d in physical units" 또는 "δθ_*/θ_* with theoretical band" 여야 한다.
"σ × N" 표기는 이미 데이터를 본 후에만 작성 가능한 *posthoc descriptive number* 다.

### 비판 #2 — "Phase-2 BAO 와 동일 채널" = 채널 공유 ≠ 독립 예측
README L177 / §4.1 row 8 모두 *"matter-era φ evolution; same channel as Phase-2 BAO"* 로 명시.
Phase-2 BAO 채널은 이미 DESI BAO 데이터에 fit 된 IDE/quintessence 파라미터 (ξ_q, β 등) 를 사용한다.
같은 채널을 재사용해 r_d shift 를 계산하면 *입력 = BAO 잔차* 가 그대로 *출력 = θ_* 잔차* 로 흐를 뿐, 새로운 정보는 없다.
**따라서 0.7% 는 BAO 피팅의 그림자이지 독립 예측이 아니다.**

### 비판 #3 — matter-era φ 진화의 정량 부재
"matter-era φ 진화" 가 δr_d 의 mechanism 으로 거론되지만, paper/base.md 본문 어디에도
- φ(z=z_d) 의 axiom-도출 값
- dφ/dN 의 matter-era boundary 조건
- δr_d/r_d 를 φ 진화에서 *계산* 한 식
이 명시되어 있지 않다. 즉 0.7% 는 **수식으로부터 도출된 숫자가 아니다**. PARTIAL 등급의 근거 문서가 *비어 있다*.

### 비판 #4 — r_d 와 θ_* 의 분리 부재
δθ_*/θ_* = δr_s(z_*)/r_s(z_*) − δD_A(z_*)/D_A(z_*) 의 standard 분해가 부재.
paper 가 *r_d* (drag epoch, BAO sound horizon, z≈1060) 와 *r_s(z_*)* (recombination, z≈1090) 를 동일 채널로 처리하는 것은 부정확.
또 D_A(z_*) shift 가 late-time DE 변형으로 흡수돼 θ_* 가 *부분적으로 자동 보존* 될 수 있다 — 이 cancellation 을 무시한 0.7% 는 over-statement.

### 비판 #5 — Planck σ 정의의 모호성
"Planck σ × 23" 의 σ 가
- (a) Planck 2018 θ_* one-σ marginalised error (≈ 3×10⁻⁶ in 100 θ_*),
- (b) Planck r_d 추론 σ (≈ 0.18 Mpc / 147 Mpc ≈ 0.12%), 또는
- (c) compressed CMB likelihood θ_* error
중 어느 것인지 본문에 명시되어 있지 않다.
0.7% / 3×10⁻⁶ ≈ 2300σ (× 23 아님) 이고, 0.7% / 0.12% ≈ 6σ 다. **N=23 이라는 숫자 자체가 어느 σ 정의에서 나왔는지 재현 불가**.

### 비판 #6 — PARTIAL 등급 기준 자체가 fit-친화적
PARTIAL 정의 (§6.5 enum) 는 "caveat 명시 + 부분 일치" 다. *prediction failure* 가 아닌 *prediction 부재* 를 PARTIAL 로 흡수하면, 어떤 axiom 외부 fit 도 PARTIAL 로 통과 가능.
0.7% 가 *fit residual* 이라면 등급은 POSTDICTION 이 정직하다. PARTIAL 표기는 등급 인플레이션.

### 비판 #7 — Forecast 부재의 falsifiability 손상
"DESI DR3 w_a" (PENDING) 와 달리 CMB θ_* 행에는 *미래 falsifier* 가 없다.
Planck 측정은 이미 종료 (Planck Legacy 2018), 후속 LiteBIRD/CMB-S4 는 polarisation 위주.
0.7% 가 prediction 이라면 **어느 후속 실험이 어느 정밀도로 도달해야 falsify 되는가** 가 명시되어야 한다 — 부재.

### 비판 #8 — δr_d 부호의 결정 부재
matter-era φ 진화는 부호 자유도가 있다 (φ_N 부호, β 부호, V(φ) 형태).
0.7% 절댓값만 표기하고 *부호 prediction* 이 없으면, BAO + CMB joint 잔차가 어느 부호로 나타나든 사후 정렬 가능.
정직한 prediction 은 "δr_d/r_d = +0.7% (matter→DE 에너지 흐름 부호 → r_d 감소)" 와 같은 부호 명시.

---

## 8인팀 합의 결론

- 현재 **"δr_d/r_d ≈ 0.7%"는 predicted 가 아니라 fit-derived descriptive label** 이다.
- 근거: (i) "σ × 23" 라벨 자체가 사후 작성, (ii) "Phase-2 BAO 동일 채널" = BAO fit 그림자, (iii) matter-era φ 진화의 정량 식 부재, (iv) 부호/forecast 부재.
- 등급 유지 가능 조건:
  1. matter-era φ(z) 진화로부터 δr_d/r_d 를 axiom + (ξ_q | β) 만으로 *forward 계산* 한 식 추가,
  2. r_d (drag) 와 r_s(z_*) 분리 + D_A(z_*) cancellation 정량 평가,
  3. "Planck σ" 정의 명시 (어느 likelihood 의 어느 marginal),
  4. 부호 prediction 명시.
- 위 4가지 충족 실패 시 **PARTIAL → POSTDICTION 로 등급 격하** 가 정직 권고.
- 최소 단기 패치: §6.1 caveat row 추가 — "0.7% 는 BAO 채널 잔차로부터 induced descriptive number; independent forward-prediction 미달성".
