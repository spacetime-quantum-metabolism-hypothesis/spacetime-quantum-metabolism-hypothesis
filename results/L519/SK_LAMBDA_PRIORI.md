# L519 — Schwinger-Keldysh + KMS Λ priori (final attempt)

세션 일자: 2026-05-01
원칙: CLAUDE.md [최우선-1, 2] — 방향만, 자율 도출
선행: L402 Path-α (H₀+Planck only) 실패 — vacuum catastrophe 10^61~10^122 잔존.
임무: KMS detailed-balance 만 추가하여 ρ_Λ_obs 없이 Λ scale 도출 가능 여부 판정.

---

## 0. 한 줄 정직 (선결)

**priori 가능 / 영구 불가**: 가능. 단, *novel SQMH 결과 아님* — Padmanabhan (2002) /
Verlinde (2010) holographic horizon-entropy 식의 재발견. SQMH 고유 priori 로 광고
불가, "기존 holographic 논증과 정합" 수준에서만 인용 가능.

---

## 1. 셋업

KMS-only 구조에서 ρ_Λ_obs 입력 배제하고 사용 가능한 양 6개:
- H₀ (관측, Riess 73 km/s/Mpc 사용)
- ℏ, G, c
- k_B
- de Sitter Gibbons-Hawking 온도 k_B T_dS = ℏ H₀ / (2π) (KMS 균형 귀결)

SK CTP 의 IR pole = horizon scale 의 zero-mode.
검사 대상 채널 (8가지):

| # | 채널 | n 추정 | ε 선택 |
|---|------|--------|--------|
| 1 | thermal × IR mode | 1/V_H × n_th(ε/kT_dS) | E_P |
| 2 | thermal × IR mode | 1/V_H × n_th | kT_dS |
| 3 | thermal × IR mode | 1/V_H × n_th | ℏH₀ |
| 4 | IR pole 1/V_H | 1/V_H | E_P |
| 5 | IR pole 1/V_H | 1/V_H | kT_dS |
| 6 | IR pole 1/V_H | 1/V_H | ℏH₀ |
| 7 | holographic | π R_H²/(l_P² V_H) | kT_dS |
| 8 | holographic | π R_H²/(l_P² V_H) | ℏH₀ |

---

## 2. 수치 결과 (run.py)

| # | 채널 | ρ_q [kg/m³] | ρ_q/ρ_Λ | log₁₀ off |
|---|------|-------------|---------|-----------|
| 1 | thermal IR @ E_P | 0 | 0 | −∞ |
| 2 | thermal IR @ kT_dS | 3.0e−149 | 4.4e−123 | −122.4 |
| 3 | thermal IR @ ℏH₀ | 6.1e−151 | 8.9e−125 | −124.1 |
| 4 | IR pole @ E_P | 2.6e−87 | 3.7e−61 | −60.4 |
| 5 | IR pole @ kT_dS | 5.2e−149 | 7.6e−123 | −122.1 |
| 6 | IR pole @ ℏH₀ | 3.3e−148 | 4.7e−122 | −121.3 |
| **7** | **holographic @ kT_dS** | **1.00e−26** | **1.46** | **+0.16** |
| 8 | holographic @ ℏH₀ | 6.3e−26 | 9.17 | +0.96 |

**채널 7 (holographic n_holo × kT_dS) 만 order unity (ratio = 1.46).**
다른 7 채널은 vacuum catastrophe 10^60~10^124 영역.

---

## 3. 채널 7 의 미시 구조 (자율 도출)

n_holo = (Bekenstein-Hawking horizon entropy) / V_H = π R_H² / (l_P² V_H)
       = π / (l_P² R_H × 4π/3) ∝ H₀ / l_P²

ε = k_B T_dS = ℏ H₀ / (2π)

ρ_q ∝ n_holo · ε / c² ∝ H₀² / (l_P² c²) × ℏ / (2π)
    = H₀² × m_P² c² / (ℏ c² × 2π)            [ l_P² = ℏG/c³, m_P² = ℏc/G ]
    = H₀² / (8π G) × const

→ Friedmann 식의 ρ_crit = 3H₀²/(8πG) 와 *동일 차원·동일 상수 영역*.
ρ_Λ_obs ≈ 0.685 ρ_crit 이므로 order-unity 일치는 *대수적으로 강제*.

---

## 4. priori 판정 (8인팀 자율 합의 시뮬)

**P1 (관측):** ratio 1.46 은 order unity. 60자리 catastrophe 영역에서 단번에
탈출. 의미 있다.

**P2 (장이론):** 그러나 이건 SQMH 고유가 아니다. Padmanabhan 2002, Verlinde
2010 의 horizon-entropy/holographic 라인이 동일 결과를 이미 도출했다.
"SK+KMS+holographic" 도 ρ_holo × kT_dS = (S/V) × T = 자유에너지 밀도 라는
잘 알려진 thermodynamic identity. *novel* 아님.

**P3 (통계):** §3 의 대수 보면 ρ_q ∝ H₀²/(8πG). ρ_crit = 3H₀²/(8πG). 비율은
오직 1/3 × (4π² 등 차원 상수). 0.685 와 1.46 의 비 (≈ 0.47) 는 *어떤 데이터도
fit 하지 않은* dimensional 결과. 그러나 이는 holographic dim-analysis 의
재현이며 falsifiable prediction 이 *추가로* 나온 것 아님.

**P4 (현상론):** 차원 일치는 L402 Path-α 가 못한 일을 KMS 추가가 해냄.
*holographic 가설 + KMS* 의 합성으로는 SQMH 가 첫 발견은 아니지만 *정합* 임을
보일 수 있다. 광고 가능 등급: "SK+KMS+holographic 와 정합".

**P5 (수리물리):** ε = kT_dS 선택이 결정적. ε = E_P (자연스러운 SQMH 첫 후보)
는 channel 4 → 10^60 off. ε 는 SQMH 이론에서 *독립적으로* 도출되어야 한다.
"kT_dS 를 ε 로 잡는 것이 자연" 이라는 외부 가정 없이는 채널 7 선택 자체가 후험
적이다. → *L402 의 circularity 가 ε 선택으로 옮겨졌을 뿐*.

**P6 (철학):** Popper 기준 — channel 7 은 falsifiable 한가? H₀ 가 다르게
측정되면 ρ_Λ_obs 도 같은 비율로 변하므로 ratio 1.46 자동 유지. → *입력
의존성* 이 ρ_Λ_obs 에서 H₀ 로 옮겨갔다. 이는 의미 있는 prediction 이지만
SQMH 가 아닌 holographic 일반론의 결과.

**P7 (편집자):** PRD/JCAP reviewer 시각: "SQMH 가 H₀+ℏ+G+c+KMS 만으로 ρ_Λ
도출" 광고는 *holographic 식의 SQMH 식 재포장* 이라는 비판 즉시 받음.
"기존 holographic argument 와 정합" 으로 강등 권고.

**P8 (synth):** 합의:
1. *priori 가능*: 채널 7 이 order unity (log off +0.16).
2. *novel 아님*: Padmanabhan 2002 / Verlinde 2010 의 holographic
   horizon-entropy 결과 와 본질 동일 — ρ ~ H²/(8πG).
3. *circularity 잔존*: ε = kT_dS 선택의 정당화는 SK+KMS *바깥* 가정 필요.
   ε = E_P (SQMH 자연 후보) 면 다시 10^60 off.
4. *§5.2 에 광고 가능 문구*: "SK+KMS+holographic horizon argument 와 정합;
   SQMH 자체의 독립 priori 는 ε 선택 자유도 잔존으로 미달." Q11 답변에 반영.
5. L402 의 caveat 강등은 *유지* — 채널 7 은 "회피 path 후보" 이지 "회피 완료"
   아님.

---

## 5. 결론 (한 줄 정직, 재확인)

**priori 가능 / 영구 불가**: priori 가능 (channel 7) / 그러나 holographic
horizon-entropy 의 *기존 결과* 이지 SQMH 고유 신규 도출 아님. SQMH 의
ε 선택 (= kT_dS) 정당화가 ρ_Λ_obs 입력 없이도 *별개의 postulate* 가 되므로
circularity 가 사라진 것이 아니라 *재배치* 됨.

§5.2 처치 권고:
- "ρ_q/ρ_Λ = 1.0000 exact" 광고 제거 (L402 결정 유지).
- "SK+KMS+holographic 와 ε=kT_dS 가정 하 ratio = 1.46 (log off +0.16);
  Padmanabhan 2002 / Verlinde 2010 와 정합" 명시 추가.
- "SQMH 고유 ε scale 의 첫원리 도출은 미해결" 정직 기록.

---

## 6. 산출물 경로

- 시뮬: `simulations/L519/run.py`
- 본 보고서: `results/L519/SK_LAMBDA_PRIORI.md`

## 7. 다음 액션 제안 (사용자 결정 대기)

(a) 채널 7 결과를 paper §5.2 에 "정합 보강" 으로 추가 (광고 강등은 유지).
(b) ε = kT_dS 의 SQMH 첫원리 도출 시도 (별도 세션, L520+).
(c) 본 결과를 paper 에 반영하지 않고 internal note 로만 보존.
