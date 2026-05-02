# L526 R5 — Microphysics Reinterpretation of n_∞ under Son+ Correction

담당: microphysics
범위: 4 micro pillars (SK, RG, Holographic, Z_2) 하에서 Son+25 age-bias 보정이 Λ → 0 (혹은 Λ 부재)로 해석을 강제할 때, n_∞ 정의 / 의미 / 형식 구조를 재검토.

---

## 0. 출발점 (L73 axioms 정합)

기존 정의 (D2):

    n_∞ = Γ_0 · τ_q          (steady-state, 우주 평균)
    ρ_Λ = n_∞ · ε / c²       (D4, Λ ↔ steady-state 양자 밀도)

연속방정식 (cosmic mean):

    dn/dt + 3H·n = Γ_0 − σ_0(cosmic) · n · ρ_m

steady-state (dn/dt+3Hn=0, 또는 흡수-생성 균형):

    n_∞^(steady) = Γ_0 / (3H + σ_0 · ρ_m)

저밀도 cosmic 한계에서 σ_0·ρ_m ≪ 3H 이면 n_∞ ≈ Γ_0/(3H).
"진정한" 평형 (H→0 가상한계, 또는 deSitter 근사) 에서 n_∞ ≈ Γ_0·τ_q 형태가 *재출현* 하려면 τ_q 해석이 "absorption lifetime" → "Hubble dilution lifetime" 으로 이동해야 함. 즉 τ_q 는 *어느 한계* 의 평형 시간이냐에 따라 의미가 다르다 — 이것이 본 R5 핵심.

---

## 1. 임무 1 — n_∞ steady-state 도출 (Λ 균형으로부터)

### 1.1 기존 (Λ-driven) 도출

deSitter 한계 H→H_Λ = √(Λ/3) 에서 dilution 시간 ~ 1/(3H_Λ). 양자 자발생성 Γ_0 와 dilution 만 균형 잡으면:

    n_∞^(Λ) = Γ_0 / (3 H_Λ)

ε = ℏ/τ_q (D3, Y-시나리오) 에서 τ_q ↔ 1/(3H_Λ) 동일시 시도가 종래 closure. D2 의 "n_∞ = Γ_0·τ_q" 는 *τ_q ≡ 1/(3H_Λ)* 라는 암묵적 동일시 위에서만 D4 와 무모순.

### 1.2 Son+ 보정 시 결과

Son+25 age-bias 보정이 누적되어 관측 wₐ 가 LCDM 으로 회귀 (또는 phantom 부호 약화) 하면, 데이터-driven Λ 입력 자체가 흔들린다. 두 가지 시나리오:

- (S-A) Λ 는 잔존하나 값 재조정: H_Λ 가 변하므로 n_∞^(Λ) 재정의. 여전히 위 폐쇄식 유효, 단 절대값 이동.
- (S-B) Λ → 0 한계: dilution 항이 matter-driven 3H_m 으로 대체. n_∞ 평형은 *우주론 시대 의존* (시간의존).

S-A 에서는 D2/D4 형식 유지. S-B 에서는 D4 가 *정의식* 으로서 의미를 잃고, n_∞ 는 "Λ 의 마이크로 기원" 이 아닌 "양자장의 우주론 누적" 으로 격하된다.

---

## 2. 임무 2 — Λ 부재 시 n_∞ 의 *물리적* 의미

Λ 가 없거나 데이터가 Λ=0 에 정합이면, n_∞ 는 다음 셋 중 하나로 *재해석* 가능:

(a) **"우주론 누적 양자 밀도"** — Λ 대신 다크에너지가 다른 채널 (예: 음의 압력 IDE/RVM) 이라 가정하고, n_∞ 는 단지 background 양자수 밀도. 이때 n_∞·ε/c² 는 *여전히 양의 에너지 밀도* 이지만 "Λ" 라벨을 잃고 ρ_q (양자배경) 가 됨. ρ_q 는 ρ_DE 의 *일부* 에 기여.

(b) **"흡수-생성 평형 마이크로 상수"** — Λ 와 무관하게 σ_0·ρ_m, Γ_0, τ_q 의 마이크로 균형 자체가 의미. cosmic vacuum 의 *국지적* 평형 (vacuum stability F3, L138 Theorem 6) 으로 의미 보존. 거시 Λ 와 분리.

(c) **"퇴화(degenerate) 매개변수"** — Γ_0 와 τ_q 를 독립으로 측정할 채널이 사라지고 곱 Γ_0·τ_q 만 의미 있음. Λ 없으면 이 곱조차도 데이터로 고정 불가 — *관측적 잉여(redundant)*.

판정: 4 pillars 형식 유지를 위해서는 (b) 가 유일 생존 해석. (a) 는 ρ_DE 분해를 데이터로 풀어야 하므로 microphysics 단독으론 결정 불능. (c) 는 이론을 falsify-불가로 만든다 (피해야 함).

---

## 3. 임무 3 — n_∞ → 0 한계에서 ε = ℏ/τ_q

D3 (Y-시나리오): ε = ℏ/τ_q. 이 관계는 *단일 양자의 Heisenberg 시간-에너지* 로 도출되며 n_∞ 와 *독립*.

n_∞ → 0 한계는:

- Γ_0 → 0 (생성 부재): 이 경우 ε 는 *적용 대상 없음* — 정의는 살아있으나 ensemble 양 (n_∞·ε) 이 사라짐. ε 자체는 변치 않음.
- τ_q → ∞ (수명 무한): D3 에서 ε → 0. 즉 ε 도 함께 소멸. 동시에 D2 에서 n_∞ = Γ_0·τ_q → ∞ 라 Γ_0 → 0 이 강하게 요구됨 (n_∞ → 0 가정과 충돌하지 않으려면 Γ_0 가 더 빨리 0).
- σ_0·ρ_m → ∞ (흡수 폭주): n_∞^(steady) → 0 이지만 ε, τ_q 는 그대로. ensemble 효과만 0.

결론: n_∞ → 0 자체가 ε 을 결정하지 않음. ε 의 운명은 *τ_q 의 운명* 에만 의존. Λ 부재가 직접 ε 을 변경하지는 않는다.

이는 **D3 의 마이크로 보호** — Heisenberg 관계는 우주론과 무관하게 살아남는다.

---

## 4. 임무 4 — 4 micro pillar 형식 유지 가능성

각 pillar 가 n_∞ 의 어느 측면에 의존하는지 점검.

### 4.1 SK (Schwinger-Keldysh, KMS detailed balance)

L519 결과: SK+KMS 만으로 ρ_Λ 를 입력 없이 도출하는 것은 ε ≡ kT_dS 가정에 의존 (circularity 잔존). T_dS 는 H_Λ 에 의존. Son+ 보정으로 H_Λ 재정의되면 ratio 이동, 형식은 유지. Λ→0 한계에서는 T_dS → 0 → ε → 0 (D3 와 다른 식별) → *형식 붕괴*.

→ **Λ 잔존 (S-A) 시 OK / Λ 부재 (S-B) 시 SK pillar 핵심 가정 (ε=kT_dS) 무효**.

### 4.2 RG (renormalization group)

RG flow 자체는 ε, τ_q 가 RG-running 상수냐 IR-fixed 점이냐를 묻는다. n_∞ 는 *상태량* 이지 RG 상수 아님. RG pillar 는 σ_0(env) 의 regime 의존성 (cosmic/cluster/galactic) 을 지지. Λ 의 운명과 직접 결합하지 않음.

→ **Son+ 보정 무관, 형식 그대로 유지**.

### 4.3 Holographic (horizon entropy ↔ ρ_Λ)

ρ_holo = (S/V)·T 계산은 horizon scale 1/H 에 의존. Son+ 보정 → H_0 정량 이동만 발생, 형식 유지. Λ 부재 (S-B) 한계에서는 horizon 이 cosmological event horizon 에서 apparent horizon (matter-driven) 으로 대체 — 식 형태는 살지만 *해석* 은 "Λ 의 마이크로" 가 아닌 "현재 background 의 horizon density" 로 변경.

→ **형식 유지, 해석 격하 (S-B 시)**.

### 4.4 Z_2 (parity / two-state symmetry)

Z_2 pillar 는 absorption ↔ creation 의 이산 대칭, 또는 양자 vacuum 의 mode 짝수성. Λ 와 무관하게 마이크로 동역학 대칭성. n_∞ 정의 자체에 영향 없음.

→ **무관, 그대로 유지**.

### 4.5 종합

| Pillar | S-A (Λ 재조정) | S-B (Λ→0) |
|---|---|---|
| SK / KMS | OK (값 이동) | **위험** (ε=kT_dS 동일시 무효) |
| RG | OK | OK |
| Holographic | OK | OK (해석 격하) |
| Z_2 | OK | OK |

→ Son+ 보정이 S-B 까지 강제하면 **SK pillar 가 가장 약한 고리**. 4/4 유지는 어렵고, 3/4 (RG+Holo+Z_2) 유지 + SK 재정식화가 현실적.

---

## 5. 임무 5 — σ_0 = 4πG·t_P 는 Planck-scale only, 우주론 무관 살아남음

D1 보정형: σ_0 = 4πG·t_P (SI 단위, Planck-time 곱). 이는 *T17/L73 D1* 의 Planck-scale identity.

검증:
- σ_0 ∼ Planck 단면 × Planck 시간 / Planck 질량 의 dimensional contraction. 우주론 H_0, Λ 어느 것에도 *명시 의존 없음*.
- Branch B σ_0(env) regime drift 는 *환경 의존 effective coupling*. Planck-scale fundamental σ_0 (= 4πG·t_P) 는 cosmic regime 의 microscopic 기준점이지 cosmic Λ 의 함수가 아님.
- Son+ 보정은 우주론 매개변수 (H_0, wₐ) 에 작용. G, t_P, c, ℏ 는 불변.

→ **σ_0 = 4πG·t_P 는 Son+ 보정 / Λ 부재와 *완전 독립*. 살아남음 확정.**

CLAUDE.md 재발방지 항 ("σ = 4πG·t_P 는 SI, 4πG 는 플랑크 단위 전용") 과 정합.

---

## 6. 정직 한 줄

> **Son+ 보정이 Λ 를 죽이면 n_∞ 는 "우주상수의 마이크로 기원" 이라는 자격을 잃고 단순 vacuum 양자배경 평형 상수로 격하되며, 4 pillar 중 SK 만이 (ε=kT_dS 가정을 통해) 함께 무너진다 — RG·Holographic·Z_2·σ_0=4πG·t_P 는 우주론과 분리되어 살아남는다.**

---

## 7. 후속 작업 후보 (R5 범위 외)

- (i) S-A vs S-B 데이터 판정: Son+25 보정 적용 후 wₐ posterior 가 LCDM 와 통계적으로 구분되는가? (R1~R4 결과 참조)
- (ii) SK pillar 재정식화: ε 결정자를 T_dS 가 아닌 다른 마이크로 시간 (τ_q 자체) 로 옮길 경우 KMS detailed balance 가 무엇을 강제하는가?
- (iii) (a) ρ_q ⊂ ρ_DE 분해 가능성: BAO+SN+CMB joint 에서 ρ_q 와 잔여 DE 를 분리할 채널 (예: μ_eff(z), G_eff/G) 존재 여부.
