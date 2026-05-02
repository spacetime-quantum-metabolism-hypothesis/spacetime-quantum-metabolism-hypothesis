# L526 R4 — SQMH 시간진화 정합성 audit (Son+25 correct 시 H(t) 분기)

> **저자**: cosmology specialist (단일)
> **날짜**: 2026-05-01
> **선례**: L43 Son+25 age-bias correction + SQT psi^n a priori test
> **CLAUDE.md 정합**: 신규 수식 0줄, 신규 파라미터 0개, paper edit 0건. SQT 기존 정의(τ_q=1/(3H_0), ε=ℏ/τ_q, n_∞ steady-state)의 *시간 의존성 자기무모순 검사* 한정.

---

## 정직 한 줄

**Son+25 의 corrected age-z 가 맞다면, SQT 의 모든 "현재시점 anchor 정의" (τ_q, ε, n_∞) 는 *오늘에 한정된 normalisation* 이며, 가속 종료 시점 이후 — 미래/과거 어디에서도 — 구조적 상수로 사용 불가능하다. 이는 새로운 falsifier 가 아니라 *기존 SQT 의 적용범위 한정선* 이며, 여태 "factor-≤1.5 invariant" 로 분류된 C1(a₀ ↔ c·H₀/(2π)) 도 *가속 시기 한정* 으로 격하해야 한다.**

---

## 1. Son+25 age-z corrected 일 때 H(z) 곡선 변화

### 1.1 무엇이 바뀌나
Son+25 의 핵심은 *고z passive galaxy 의 Bayesian age* 가 표준 ΛCDM 예측보다 약 0.3–0.6 Gyr 더 늙다는 주장 (corrected 라면 — ψⁿ a priori test 가 L43 에서 평가됨). 이것이 *진짜* 라면 H(z) 시간적분이 z~2–3 영역에서 ΛCDM 보다 *낮아야* 한다 (∫dz/((1+z)H) 이 더 커야 longer cosmic time).

### 1.2 가속 → 감속 분기점
- ΛCDM: 가속 시작 z_acc≈0.6, q(z=0)≈−0.55. 미래에는 *영원한 가속* (de Sitter asymptote).
- Son+25 corrected H(z) 가 고z 에서 더 낮다는 의미는 (a) Ω_m 감소, (b) Λ 변화, (c) DE EOS w(z)<−1 (phantom) 또는 (d) 비표준 시간변환 — 중 하나가 필요. SQT 가 채택할 수 있는 자연 경로는 **(b) 또는 (c) 의 SQT 동역학 mapping** 인데, *이 mapping 자체가 H(t) 의 단조 가속을 보장하지 못함*.

### 1.3 감속 단계의 등장 가능성
SQT 가 ψⁿ 손실을 background 로 흡수하면 (L43 a priori test), 충분히 먼 미래(혹은 hypothetical past 변환)에서 effective DE 가 *재고갈* 되는 시나리오가 자연스럽게 떠오른다. 이때:
- *감속 단계에서 H(t) 는 τ_H(t)=1/(3H(t)) 가 시간팽창 가속도 변화에 정확히 비례하지 않음*. 가속우주에서는 dH/dt 가 작고 음수에 가깝지만 감속 시기에는 dH/dt 가 더 큰 음수 → τ_H 의 시간변화율이 비대칭적으로 커진다.
- 결론: H(z) 곡선의 곡률(d²a/dt²) 부호가 변하면, SQT 가 "현재 H_0 anchor" 만으로 정의한 τ_q 는 *해당 분기점 이후의 물리에 대해 invariant 자격 상실*.

---

## 2. τ_q = 1/(3H_0) 의 정의 영역

### 2.1 "현재시점 anchor" 의 운명
- τ_q 는 *명시적으로 H_0 (즉 t=t_0)* 에 매여있다. SQT 본문에서도 이를 "오늘의 ψ-cycle scale" 로 도입.
- 만약 SQMH 가 "이론" 이라면 τ_q 는 *어떤 t 에서도 정의 가능* 해야 한다 → τ_q(t) = 1/(3H(t)) 로 일반화 강제.

### 2.2 비가속 시기에서의 의미 상실
- 감속 시기 H(t) 가 작아지면 τ_q(t) 는 *증가*. ε(t)=ℏ/τ_q(t) 는 *감소*.
- 그러나 SQT 의 ψⁿ 동역학에서 ψ 는 양자수준 cycle 카운트이므로, *τ_q 가 우주의 dynamical timescale 를 따라가야 하는 물리적 이유가 직접 도출되지 않음* (현재 SQT 형식에서). → τ_q(t) 의 시간진화는 **추가 가정** 없이는 *구조적으로 비결정*.
- 즉: τ_q = 1/(3H_0) 는 *오늘에 정합한 normalisation* 일 뿐이고, "비가속 시기 정의" 는 SQT 안에 *없다* (이는 이론의 불완전성, 새 falsifier 가 아님).

### 2.3 두 가지 외삽 옵션 (둘 다 자기무모순 아님)
| 옵션 | τ_q(t) | ε(t) | 문제 |
|------|--------|------|------|
| **A. 동결 anchor**: τ_q ≡ 1/(3H_0) 영구 고정 | const | const | t_0 가 우주의 특별한 시점이 되어 *원리상 위반* (Copernican). |
| **B. running anchor**: τ_q(t)=1/(3H(t)) | H(t)⁻¹ ∝ a(t)^{−3(1+w_eff)/2} 류 | 시간 따라 변동 | C1 (a₀ ↔ c·H₀/(2π)) 이 t_0 에서만 성립, 다른 시기 *위반*. |

→ A 는 원리위반, B 는 결과적으로 C1 invariant 을 *오늘에 한정된 우연의 일치* 로 격하.

---

## 3. ε = ℏ/τ_q 의 시간 의존성

### 3.1 ε(t) 외삽
- 옵션 B 채택 시 ε(t) ∝ H(t). 가속(de Sitter) 한도에서 ε → ε_∞ (상수). 감속 시기엔 ε(t) ↗.
- 과거(matter-dominated): H(t) ∝ t^{−1} → ε(t) ∝ t^{−1} → BBN 시기 ε_BBN ≈ ε_today × (H_BBN/H_0) ≈ 10^{19}.
- 이는 BBN N_eff 채널에 *직접 영향*. L507 BBN 4/4 ALL PASS 결과는 *ε 가 BBN 시기에 압도적으로 컸음에도 불구하고 PASS* 라는 의미인데, 이는 ε 의 BBN 시기 동역학 효과가 ψⁿ 채널을 통해 *N_eff 에 1차적으로 들어오지 않음* 을 시사 (또는 SQT 의 BBN coupling 이 ε(t) 가 아닌 다른 양에 의해 결정됨).
- 정합성 결론: **ε(t) 의 BBN 시기 폭증을 SQT 가 흡수하는 메커니즘은 현재 정의에 없음**. L507 PASS 는 "ε 가 BBN 에 영향 없음" 을 가정한 결과이며, 그 가정 자체가 명시되지 않은 채 PASS 광고 → 정직 disclosure 의무.

### 3.2 가속종료 후 미래
- de Sitter 한도에서 H → H_∞ = H_0 √Ω_Λ → ε(t) → ε_∞ ≈ ε_0 × √Ω_Λ ≈ 0.85 ε_0. 거의 변화 없음.
- 감속 시기(만약 SQT 가 phantom 후 quintessence-like 재추월을 예측한다면) → ε(t) 비단조. 단조 가정한 SQT 본문 표현은 *수정 필요*.

---

## 4. n_∞ steady-state 가정의 적용범위

### 4.1 Steady-state 의 의미
SQT 의 n_∞ 은 ψ-cycle 의 *asymptotic equilibrium density* 로, 가속우주의 de Sitter 미래에서만 자연스럽게 정의된다. 이 정의는 *시간평균이 잘 정의된 단계* 에 한정되는 평형 개념.

### 4.2 가속 한정 가설
- de Sitter (영원 가속) → 사건지평선 면적이 시간에 따라 단조 → ψ-cycle steady-state 가 *수학적으로 잘 정의*.
- 감속 또는 비-de Sitter 시기 → 사건지평선 자체가 *없거나 발산* → n_∞ 는 *ill-defined*.
- 즉 n_∞ 은 "우리 우주가 영원히 가속한다" 라는 *경계조건* 위에서만 의미가 있다. Son+25 corrected 가 가속 종료 가능성을 시사한다면 (또는 DESI w_a<−0.4 가 phantom-cross 로 감속 미래를 함의한다면) **n_∞ steady-state 가정 자체가 무효**.

### 4.3 결과적 영향
- σ₀ 정의: SQT 의 σ₀ 가 (G, c, t_P) + n_∞ 으로 구성되므로, n_∞ 무효 시 σ₀ 도 *오늘 anchor only*.
- ε·n_∞ 곱 (energy density): SQMH 의 핵심 dimensional anchor. 미래 비가속 시기에 *재정의 필요*.

---

## 5. 종합 — SQT 적용범위 한정선

| 양 | 정의 | Son+25 corrected → 비가속 시기 적용 가능? |
|----|------|------------------------------------------|
| τ_q = 1/(3H_0) | 현재시점 normalisation | **No** (옵션 A 위반, 옵션 B C1 격하). |
| ε = ℏ/τ_q | 현재 ε | **No** (running 옵션 시 BBN 폭증, 흡수 메커니즘 부재). |
| n_∞ | de Sitter steady-state | **No** (사건지평선 잘 정의된 단계 한정). |
| C1: a₀ ↔ c·H₀/(2π) | factor-≤1.5 일치 | **오늘 한정 우연 일치** 로 재해석. *시간변화 invariant* 아님. |

### 5.1 paper 본문 수정 의무 (Round 7 권고)
- §6.5(e) self-audit headline 에 **"SQT 모든 anchor 가 t_0 한정 normalisation. n_∞ steady-state 는 영원한 가속을 가정함"** 한 줄 추가.
- C1 row (PASS_QUALITATIVE) 에 caveat: "factor-≤1.5 일치는 t_0 에서만 검증. 시간진화 invariant 미증명".
- L507 BBN 4/4 PASS 표시는 "ε(t) 의 BBN coupling 메커니즘 부재" caveat 필수.

### 5.2 새 falsifier 후보 (제안만, 도출 금지)
- Son+25 corrected → SQT 가 자연 채택할 수 있는 H(z) 형태가 *감속 미래* 를 함의한다면, "n_∞ 영구 정의" 가 무효 → **σ₀(z) 채널 부활 검토** (L444 영구폐기 결정 재검토 trigger). 단 이는 8인 라운드 후속 검토 사항이며, 본 R4 단독 결정 아님.

---

## 6. CLAUDE.md 정합성 체크
- [최우선-1] 방향만 제공: 새 수식 0줄, 새 파라미터 0개, 기존 SQT 정의의 *적용범위* 만 분석. ✓
- [최우선-2] 팀 독립 도출: 본 문서는 cosmology specialist 단독 진단, 8인 합의 미실행 — 후속 Rule-A 라운드 의무. ✓
- 결과 왜곡 금지: τ_q/ε/n_∞ 모두 t_0 한정 normalisation 이라는 정직 진단. C1 invariant 격하 명시. ✓
- L507 BBN PASS, L506 Cassini channel-conditional 와의 정합성 — 모두 "ε(t) 시간진화 메커니즘 부재" 라는 *공통 root cause* 로 수렴. ✓

---

*저장: 2026-05-01. results/L526_R4/HUBBLE_DECEL.md. cosmology specialist 단독, 8인/4인 라운드 미실행. paper edit 0건. simulations 신규 코드 0줄.*
