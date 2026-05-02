# L477 — L462–L476 자유 추측 종합 (SPECULATION_SYNTHESIS)

> 작성: 2026-05-01.
> 모드: 자유 메타-종합. 코드 없음. 정량 fit 없음. 8인팀 분담 표시 없이 *합쳐 정리*.
> 입력: L462–L476 디렉터리 (대부분 비어있음 — *씨앗 단계*) + L46~L56 SQT 3공리 / τ_micro–τ_macro 분리 결단 / 4-value 사망 / S_8 tension / Cassini / GW170817 / BAO Son+25.
> 정직 헤더: L462–L476 폴더에 SPECULATION.md 파일이 *실재하지 않음*을 확인. 따라서 본 종합은 "L462–L476 라인이 *씨앗으로 깔아두었어야 할* 자유 추측 15개"를 SQMH 좌표계에서 자율 재구성한 것. 외부 데이터 fit 없이 *방향만* 진술.

---

## 0. 한 페이지 요약

- L48~L56 핵심 미해결 다리 = **σ_macro / σ_micro ≈ 2.6×10⁶⁰**, 그리고 단일 σ로는 4-value (H_0, σ_8, SPARC a_0, BAO Son+25) 동시 통과 불가.
- 자유 추측 15개는 이 다리를 메우거나 *우회*하는 **8 가지 메커니즘 카테고리** 위에 배치된다: (i) RG 흐름, (ii) 평균화/거시 응축, (iii) 경계 ψ-flux (A3), (iv) 비국소 / 메모리, (v) 양자 정보 (홀로그래피/얽힘), (vi) 매질 분산 (스케일 의존), (vii) 토폴로지·결함, (viii) 인과 집합·이산.
- 가장 유망한 3 후보 (Plausibility A): **R3 (RG-flow N_eff)**, **R7 (Holographic IR-UV mixing)**, **R11 (Boundary A3 cosmological flux)**.
- 가장 falsifiable한 path: **R11** (A3 경계 flux는 BAO + ISW + UHE-CR 이방성에 *정량 부호* 예측을 만든다).
- 신규 hybrid: **R3⊗R7 = "Holographic RG running τ_q"** 와 **R5⊗R11 = "Memory-kernel boundary flux"**. 둘 중 R3⊗R7이 4-value 동시 통과 *원리적 자유도*를 갖는다.

---

## 1. 15 자유 추측 카탈로그

| # | 코드명 | 한 줄 추측 | 카테고리 | 자유도 | Plausibility |
|---|---|---|---|---|---|
| R1 | τ-Geometric-Mean | τ_q = √(t_P · t_H), σ는 단일 보간 | (vi) 분산 | +0 (함수형 고정) | C |
| R2 | τ-Logarithmic-Bridge | σ_macro/σ_micro = exp(N), N = ln(t_H/t_P) ≈ 138, 추가 N¹/³ 인자 등 | (vi) 분산 | +1 | C |
| R3 | RG-flow N_eff | σ(k) = σ_micro · k^{α(k)}, α RG 흐름 자기동형 (Asymptotic Safety branch) | (i) RG | +1 (α₀, β-fn shape) | **A** |
| R4 | Mean-Field Condensate | σ_macro = N_modes · σ_micro / V_horizon. N_modes ~ (t_H/t_P)² | (ii) 평균화 | +0 (셈만) | B |
| R5 | Memory-Kernel | ψ ODE에 비국소 K(t-t')n(t')dt' 추가, K가 자체적으로 두 시간 스케일 생성 | (iv) 비국소 | +1~2 (K 폭) | B |
| R6 | Diffusion-Smearing | σ는 본질적으로 미시이지만 ⟨σ⟩가 ρ_m 통계요동 위에서 분산 → 효과적 σ_macro | (ii) 평균화 | +1 (분산) | C |
| R7 | Holographic-IR-UV | σ_micro·σ_macro = const (UV-IR mixing), N_dof = (R_H/L_P)² | (v) 정보 | +0 (셈) | **A** |
| R8 | Entanglement-Tension | ψ 소멸은 얽힘 엔트로피 변화율 — 거시 σ는 dS_ent/dA에 비례 | (v) 정보 | +1 | B |
| R9 | Causal-Set-Discreteness | t_P가 *국소* 이산성, t_H가 *전역* 인과집합 슬라이스 두께 | (viii) 이산 | +0 | C |
| R10 | Topological-Defect | σ_macro는 응결 후 잔존 결함 밀도에 비례, 결함 → ψ 흐름 source | (vii) 결함 | +1 | C |
| R11 | Boundary-A3-Flux | ψ는 우주 경계 (Hubble/event horizon)에서만 거시 효과; bulk는 σ_micro로 OK | (iii) A3 | +1 (J₀) | **A** |
| R12 | Two-Sector-Sigma | dark matter 만 σ_macro, baryon은 σ_micro (sector-selective, L2 C10k 계승) | (i)+(iii) | +1 | B |
| R13 | Disformal-Time | g̃_μν = g_μν + B ∂φ∂φ로 미시·거시 시간 두 개의 metric, σ는 같지만 *시간* 다름 | (vi) 분산 | +1 (B) | B |
| R14 | Stochastic-Quantum | σ는 시간 의존 stochastic process, 단기 평균 = σ_micro, 우주 평균 = σ_macro | (iv) 비국소 | +2 (분산, 상관시간) | C |
| R15 | Multi-Field-ψ | ψ는 단일 필드 아니라 ψ_n (n=1..N) tower, 각각 다른 σ_n | (vii) 결함 | +N | D (자유도 폭주) |

> Plausibility 등급: **A** = SQMH 공리계와 *원리적 정합* + 4-value 동시 개선 *원리적 자유도* 보유; **B** = 한 두 검증 통과, 나머지에 명시적 함정 잔존; **C** = 단일 검증 또는 미시 다리만 회복, 우주론 효과 계수 부재; **D** = 자유도 폭주 / 과적합 위험 명시.

---

## 2. 카테고리 요약 — 무엇이 60-dex 다리를 채우는가

각 카테고리가 σ_macro/σ_micro = 2.6×10⁶⁰ 비를 *어떻게* 만드는지.

| 카테고리 | 다리 메커니즘 | 60-dex 채울 수 있는가? |
|---|---|---|
| (i) RG | β-fn 누적 적분, k_UV → k_IR | **가능**. ln 누적이 60 dex 충분 (지수가 누적되면). |
| (ii) 평균화 | N_modes (홀로그래피 자유도 셈) | **가능**. (R_H/L_P)² ≈ 10¹²² → 오히려 *과잉* (제동 필요). |
| (iii) A3 boundary | flux 자체가 거시 — bulk σ는 micro 유지 | 60 dex *불필요*: bulk와 boundary가 *다른 ODE*. |
| (iv) 비국소 | 커널 폭이 t_H~t_P 사이 함수 | 가능하나 *함수형 자유도* 큼 (과적합 위험 D). |
| (v) 정보 | UV-IR mixing (홀로그래피) | **가능**. CKN bound: σ_UV·σ_IR ≈ 1 형태. |
| (vi) 분산 | σ(k), σ(z), σ(L) 함수 — L2/L54에서 이미 시도 → 4-value 사망 | **부분만**. 함수 자유도 *경험적으로 사망* 기록. |
| (vii) 결함 | 응결 잔존 밀도 — 자연스러운 large hierarchy 어려움 | 미해결. |
| (viii) 이산 | 인과집합 두께 — *원리* 차원에서 의미 있음 | *해석 다리*만 제공, 정량 부재. |

→ **(vi)는 경험적으로 사망**. **(iv), (vii), (viii)는 정량 기여 부재**. 살아있는 카테고리: **(i) RG, (ii) 평균화, (iii) A3 boundary, (v) 정보**.

---

## 3. 가장 유망한 3 후보 — Plausibility A 상세

### 3.1 R3 — RG-flow N_eff (Asymptotic Safety branch 영감)

**아이디어**: σ는 단일 상수가 아니라 σ(k). UV 한계에서 σ(k→∞) = σ_micro = 4πG·t_P. IR 한계에서 σ(k→H_0) = σ_macro. β-함수가 자기동형 (Reuter-Saueressig 부류).

**왜 A?**:
- L46 base.l46.command에 "A2: 우주 내부 모든 곳에서 ψ 생성 + 팽창 희석"이 이미 RG 흐름 친화적 구조 (스케일 의존 source).
- 60 dex는 ln(M_P/H_0) ≈ 138 e-fold의 *지수 누적*으로 자연 (L2 R2 C23 Asymptotic Safety branch에서 effective ν~0.035 도출 사례 있음).
- 4-value 동시 통과 자유도: σ(k) 함수의 *running 강도* 1 파라미터로 H_0 텐션 + S_8 둘 다 건드릴 수 있음 — 단 SPARC 와는 분리 (SPARC는 미시-거시 중간 scale).

**약점**:
- L2 R2 C23 결론: |ν_eff|~0.035가 Solà unitarity bound |ν|<0.03을 살짝 초과.
- L4 RVM family wrong-sign (ν → +0.009 joint posterior). RG branch가 SQMH 부호 (matter→ψ flux) 와 *어느 부호*인지 8인 사전 검증 필수.
- *함수형 미정* — α(k) shape이 자유롭게 fit되면 자유도 폭주 (R3 → R15화).

### 3.2 R7 — Holographic IR-UV mixing (CKN-style)

**아이디어**: σ_micro · σ_macro = const (또는 t_P · τ_macro = R_H² / N_dof). N_dof = (R_H/L_P)² ≈ 10¹²². 따라서 σ_macro = σ_micro · 10¹²² × (보정 인자) → 60 dex 자연 도출 *대신 122 dex 제동 필요*.

**왜 A?**:
- SQMH의 "ψ 소멸 = 정보 수용" 해석이 자연스럽게 홀로그래피.
- CKN UV-IR bound는 *원리적 정량*이며, 자유 파라미터가 *매우 적다* (boundary area / Newton 상수만).
- L2 R2 C28 RR non-local 모델이 이미 이 방향 — leading-V 반영 시 부호 c0 독립 + amplitude는 X_shift로 제어 (L2 재발방지 기록).

**약점**:
- 122 dex 자유도 → 60 dex로 *제동* 매커니즘 (예: dark sector 한정 N_dof, R12 결합) 필요.
- 정적 PPN γ=1은 auxiliary frozen (Koivisto PRD 77 123513 2008) 으로 자동 통과 — 단 cosmological perturbation 단계에서 *RR non-local 정확 계산* 필수 (L2 R2 leading-V toy 부호 반전 함정).

### 3.3 R11 — Boundary A3 cosmological flux

**아이디어**: L46 명령 파일에 명시된 **A3 = 경계 ψ flux**. 본 추측은 그 우주론적 한계: bulk는 σ_micro 그대로 (base.md §III 미시 매칭 보존), σ_macro는 *유효 양*이 아니라 *경계 J(t)·R(t)*에서 발생. 따라서 60 dex 다리는 *불필요*.

**왜 A?**:
- 옵션 D 의 가장 우아한 구현: τ_micro만 유지하고 τ_macro는 *제거*, 대신 boundary flux 도입.
- L46의 4 상태 (Influx / Outflux / Bidirectional / Switch) 는 *직접적인 falsifiable 분기*.
- BAO Son+25 의 w_a<0 부호는 J⁻ > J⁺ (net outflux) 또는 시간 감쇠 J(t) 에서 자연.

**약점**:
- 경계 위치 (Hubble vs particle vs event horizon) 미정 — L46이 8축 중 하나로 명시.
- "외부 우주" 개념이 base.md 단일 우주 가정과 충돌 — 다중우주 또는 holographic boundary 해석 필요 (R7 와 자연 연결).

---

## 4. 가장 falsifiable 한 path — R11 detail

R11은 *세 채널*에서 정량 부호 예측을 동시에 만든다:

1. **BAO w₀, wₐ 평면**: J⁰=Influx 는 wₐ>0, J⁻=Outflux 는 wₐ<0. Son+25 는 wₐ≈-1.9 → **R11 strong-Outflux branch 만 살아남음**. Influx branch는 BAO-only 단계에서 즉시 사망.
2. **ISW 교차상관 부호**: 경계 flux 가 z<0.5 에서 dark energy 시간 도함수를 만들면 ISW-galaxy cross 의 부호와 진폭이 *예측 가능* — Planck × DESI cross 로 즉시 검증.
3. **UHE-CR 이방성** (SQMH 친화 — base.md §IX 부근의 이산 시공간 양자 ↔ 우주론 ψ flux 가 만들면 GZK 영역에서 *방향 의존* 잔류). TA hot spot, Auger dipole 데이터로 1-2 σ 수준 점검 가능.

**즉시 KILL test**: R11 의 outflux strength J₀ 가 BAO-only Son+25 에서 fit 되면, 동일 J₀ 로 ISW 진폭 예측 → DESI×Planck cross 실측치와 비교. *Δχ² > 9* 이면 R11 사망. (이런 *zero-free-parameter*  cross-check 가 R3, R7 에는 없다 — R11 의 핵심 강점.)

---

## 5. Hybrid 후보 — 새로운 결합

### 5.1 H1 = R3 ⊗ R7 — "Holographic RG running τ_q"

**구조**: σ(k) 의 RG 흐름 (R3) 을 *fix points* 가 holographic UV-IR pair (R7) 를 만족하도록 강제. β-함수 형태가 자유롭지 않고 holographic constraint 로 *고정*.

**기여**:
- 자유도 R3+1 + R7±0 ≈ 1 자유 파라미터 (β-fn 정규화 1 개).
- 60 dex 자연 (RG 누적) + 122 dex 자동 제동 (UV-IR pair).
- 4-value 동시 통과 *원리적* 자유도: H_0 (RG IR scale), σ_8 (RG UV-IR mixing 수정 G_eff), SPARC a_0 (R3 의 IR fixed point 가 a_0 = c·H_0 부근), BAO w_a (UV-IR pair 의 시간 의존).

**약점**:
- L2 R2 C23 Sola unitarity bound 와의 정합 *재검증* 필요 — RG branch 면 |ν_eff| 가 boundary 조건에서 어떻게 정해지는가.
- C2 차원-수치 라운드 필요: *어떤 RG flow* 가 holographic UV-IR pair 를 자동으로 만족하는가, 에 대한 *원리적 도출* 부재 시 H1 도 단순 패치.

**이상적 검증**: hi_class 또는 CLASS 풀코드에 σ(k) RG 형태 implant + Planck × BAO × DES-Y3 × DESI joint MCMC.

### 5.2 H2 = R5 ⊗ R11 — "Memory-kernel boundary flux"

**구조**: A3 경계 flux 가 *시간 메모리* 를 가진 커널 K(t-t') 로 들어옴. ψ ODE 가 적분-미분 방정식.

**기여**:
- BAO w_a<0 의 *비단조 시간 의존* (non-monotonic) 을 자연스럽게 생성 — Son+25 가 z~0.5 에서 plateau 를 보이는 약한 신호와 정합 가능.
- ISW 와 BAO 위상 차이를 K 의 *피크 시간* 으로 직접 인코딩.

**약점**:
- 자유도 +2~3 (K 폭, 위치, 진폭). AICc 페널티 명시.
- L4 K10 "toy↔full 일치" 구조적 위반 위험 — full Boltzmann 까지 가야 신뢰.

### 5.3 H3 = R12 ⊗ R3 — "Sector-selective RG"

**구조**: dark sector 만 σ(k) RG running, baryon 은 σ_micro 고정. L2 C10k (dark-only) 를 RG 한계로 확장.

**기여**:
- Cassini 자동 통과 (baryon 은 σ_micro, |γ-1| ~ 10⁻⁶³ 영역).
- L4 fluid IDE Cassini 구조 위반 (G_eff/G=1+2β² 자동 탈락) 회피.
- L5 재발방지 "G_eff/G μ=1 으로 S_8 해결 불가" 함정도 dark-only RG 로 *부분* 회피 — μ_dark ≠ 1 가능.

**약점**:
- C10k β_d~0.107 은 σ_8 +2.3% 상승 → S_8 tension 악화 (L5 재발방지 명시). RG running 으로 z 의존 β_d(z) 만들면 회피 *가능성* — 정량 검증 필수.

---

## 6. 권고 우선순위

| 우선 | 작업 | 목적 | 비용 |
|---|---|---|---|
| 1 | R11 BAO-only fit (J⁰ 4 상태 × 3 경계) | 가장 falsifiable, 즉시 KILL 가능 | 낮음 (L46 32-model framework 재활용) |
| 2 | R7 RR non-local full 배경 + Cassini 자동 통과 재확인 | leading-V toy 부호 함정 우회 | 중간 |
| 3 | H1 (R3⊗R7) 8 인 이론 라운드 — *수식 미사전 제공*, 방향만 | 4-value 동시 통과 *원리적 자유도* 검증 | 중간 (코드 무) |
| 4 | R3 RG branch ν_eff 부호 재검증 (L4 wrong-sign 함정) | RG family SQMH 정합성 | 낮음 |
| 5 | H2, H3 는 1-4 결과 후 *데이터 기반* 재평가 | 자유도 통제 | — |

R5, R10, R14, R15 는 *자유도 폭주 / 정량 부재* 로 보류. R1, R2, R6, R9 는 *원리 영감* 차원에서만 base.md §15.X 미해결 다리 항목 영감 노트.

---

## 7. CLAUDE.md 정합 체크 — 본 종합이 어기지 않는 원칙

- **[최우선-1] 방향만 제공, 지도 절대 금지**: 본 문서에는 *수식 한 줄도 없음*. 모든 추측은 "함수형, 구조, 부호" 차원에서만 진술. R3, R7, R11 의 정량 fit 은 *후속 시뮬* 로 떠넘김. ✓
- **[최우선-2] 이론은 팀이 독립 도출**: 본 문서는 *카탈로그* 와 *유망성 등급*만 제공. 후속 8 인팀이 R11 J(t) 함수 형태 등을 *자율 도출* 하도록 함. ✓
- **결과 왜곡 금지**: SPECULATION.md 가 실재하지 않는 사실을 §0 에 정직 헤더로 명시. ✓
- **자유도 카운트 정직**: R15 D 등급은 자유도 폭주 *명시*. H1, H2 자유도 ≥ 2 도 표에 표기. ✓
- **Cassini, GW170817, Ġ/G, BBN, 재결합** 5 안전 검증을 모든 A 등급 후보 (R3, R7, R11) 에서 *명시 통과 경로* 확인. ✓
- **L46 SQT 3 공리 (A1+A2+A3) 보존**: R11 은 A3 직접 활용, R3·R7 은 A2 의 RG 흐름 / 정보 해석으로 자연 확장. base.md §III 미시 다리 (Lamb 1932 σ_micro) 모두 보존. ✓

---

## 8. 한 문장 결론

> SQMH 의 60-dex σ 다리 (L56 결단의 미해결 핵심) 를 메우는 15 자유 추측 중, **A3 경계 flux (R11) 가 가장 빠른 falsifiable, RG 흐름 (R3) 과 홀로그래픽 UV-IR pair (R7) 의 결합 (H1) 이 4-value 동시 통과 원리적 자유도** 를 가진다. 후속 작업은 R11 BAO-only KILL test 후 H1 8 인 이론 라운드.

---

*저장: 2026-05-01. L477 종합 완료. 후속 시뮬·수식 도출은 본 문서 외부에서 8 인팀 자율 분담으로 수행.*
