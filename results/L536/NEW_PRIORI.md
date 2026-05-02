# L536 — *진정 priori* 신규 prediction 탐색 (Path-α + GFT/Causet 결합)

> **작성**: 2026-05-01. 단일 메타-감사 에이전트. 8인/4인 라운드 *미실행*.
> **substrate**: results/L527/PATH_ALPHA.md (Path-α: axiom 3 → axiom 3' Γ₀(t)),
> results/L530/NEW_AXIOM_SYSTEMS.md (E = GFT BEC, C = Causet meso, B = Volovik 비교),
> results/L531/AXIOM_MODIFY_SYNTHESIS.md (Path 합성), L526_R6/PREDICTION_RECHECK,
> L526_R8/HIDDEN_ASSUMPTIONS, paper/base.md §2 (4 pillar).
> **CLAUDE.md 정합**: 신규 수식 0줄, 신규 파라미터 0개, paper/base.md edit 0건,
> simulations/ 코드 0줄, claims_status edit 0건. 본 문서는 *방향* + *priori 자격 감사* 만 — [최우선-1] (지도 금지) / [최우선-2] (팀 독립 도출) 정합.

---

## 0. 정직 한 줄 (사용자 요구 형식)

**hybrid (Path-α + GFT BEC 또는 Causet meso) 채택 시 *진정 priori* 자격 후보 = 1개 (P3: Z₂ SSB → matter-antimatter asymmetric domain wall scar) — 단 "도출 가능" 단계이며 "도출됨" 아님; 나머지 7 후보는 모두 *postdiction* 또는 *parametric prediction* (priori 자격 부정).**

---

## 1. *priori* 자격 정의 (감사 기준)

본 감사가 사용하는 4 단계 엄격 기준 (CLAUDE.md L6 §"Q17 amplitude-locking", base.md §2.2 "도출" 정의):

- **(L0) genuine priori**: axiom-set 만으로 (a) *부호*, (b) *차원*, (c) *order-of-magnitude (OOM)* 가 *데이터 fit 없이* 결정되며, (d) 관측 *전*에 명시 가능.
- **(L1) structural priori**: 부호 + 차원 + OOM 중 2/3 만 axiom 으로부터, 1/3 은 단일 보조 가정.
- **(L2) parametric prediction**: 함수 *형태* 는 axiom, amplitude 는 fit (Q17 미달 — L4/L5/L6 재발방지에 따라 priori 아님).
- **(L3) postdiction**: 관측값을 *알고서* 식 형태를 reverse-engineer.

**priori = L0 또는 L1 만 인정. L2/L3 는 priori 아님.**

추가 control 변수:
- **CLAUDE.md L4 K10 sign-consistency**: w_a 부호가 *toy* 와 *full* 모두 동일해야 진정 부호 예측.
- **L6 fixed-θ vs marginalized**: 어느 evidence 인가 명시 의무.

---

## 2. 4 채널 × 후보 16 매트릭스 (요구 임무 1–4)

> 임무 정의에 따라 4 채널 × {axiom-set 1: Path-α + GFT BEC, axiom-set 2: Path-α + Causet meso} = 8 후보.
> 추가로 *channel-cross* 후보 4 개 (한 채널이 다른 채널 amplitude 결정) 및 *Volovik companion* 4 개는 §6 부록.

### 채널 1: SK propagator → 새 cosmological observable

**SK = Sakharov-Komar (paper §2.4 first pillar)**. SK 는 zero-point 합산이며 cosmological time-evolution 채널이 *원래 부재* (L527 Path-α §3 표). hybrid 도입 효과:

| ID | 후보 (방향) | hybrid 추가 효과 | 자격 감사 | priori 등급 |
|----|-------------|-----------------|-----------|-------------|
| **P1a** (Path-α + GFT) | SK cutoff 가 GFT condensate mode 수 j_max 로 *동역학화* → SK propagator 의 IR/UV 분리 면이 시간 의존 → *cosmic-scale Casimir-like correction* (지표: 진공 압력 scale 의 **z-evolution slope dlogP_vac/dlna**) | 부호: GFT depletion 방향 (positive sign 후보, 단 hexagon Hamiltonian 부호 자유 도출 의무). 차원: ✓ (energy density). OOM: GFT coupling λ_GFT 입력 *필요* → fit 없으면 결정 불가 | **L2 (parametric)** | priori 아님 |
| **P1b** (Path-α + Causet) | Sorkin-style ⟨Λ⟩ ~ √N 변동의 *시간 의존* 이 SK 합산의 *분산* 에 추가 — 지표: **Λ 분산 σ_Λ(z)** 의 cosmic-time scaling exponent | 부호: ✓ (variance ≥ 0 자명). 차원: ✓. OOM: Sorkin 1992 N ~ V₀/l_P⁴ 입력만으로 σ_Λ/Λ ~ N⁻¹ᐟ² OOM 결정 가능 | **L1 candidate** (보조 가정 = "manifoldlike causal set" + "Poisson sprinkling") | **L1 conditional** |

**P1b** 는 OOM 이 1 axiom (Poisson sprinkling rate) 으로 결정되는 점에서 L1 자격 *후보*. 단 이는 L379 의 기존 결과 inheritance 이며 hybrid 의 *신규* 도출 아님 — L530 §특이사항 ("재상속 vs brainstorm") 에 따라 **신규 priori 부정**, *재상속 priori* 로 분류. **임무 1 의 진정 신규 priori = 0**.

### 채널 2: RG flow → galactic-cosmic 매개 prediction

**RG = paper §2.4 second pillar**. RG flow 는 algebraic, *현재 scale* 에서 정의 (L527 §3 — 시간 의존 무관 살아남음). hybrid 가 추가하는 *galactic-cosmic 매개* (galaxy-scale RG running 이 cosmic observable 결정) 가능성:

| ID | 후보 (방향) | hybrid 추가 효과 | 자격 감사 | priori 등급 |
|----|-------------|-----------------|-----------|-------------|
| **P2a** (Path-α + GFT) | GFT condensate fraction 의 RG running 이 galactic regime (RAR a₀) 와 cosmic regime (Λ scale) 사이 **bridging exponent η_RG** 도출. 지표: a₀ × Λ_obs / (cH₀)² 의 dimensionless ratio (현재 ≈ O(1) coincidence, base.md §2.4 4 pillar convergence) 가 *RG fixed point* 결과로 자연. 새 prediction = **η_RG 의 redshift drift** | 부호: GFT asymptotic safety 가 IR-attractive 이면 양 (Bonanno-Platania 부호) — 단 CLAUDE.md L2 R2 C23 재발방지 "ν_eff<0 만 w_a<0" — *부호 자체가 GFT formalism 의 IR/UV 선택에 종속*, axiom 만으로 결정 불가. 차원: ✓. OOM: ratio ≈ 1 coincidence 는 이미 *알고 있는* 입력 | **L2/L3 경계** (postdiction 위험: a₀ × Λ ≈ (cH₀)² coincidence 가 *동기*) | priori 아님 |
| **P2b** (Path-α + Causet) | Causet meso scale 가 RG flow 의 *cutoff* 역할 → galactic disk 내 Newtonian 한계와 cosmic Λ 사이 **연속 RG 흐름**이 단일 sprinkling rate 로 매개. 지표: Newton G_N 의 *galaxy-cluster scale 변화* (∼kpc) | 부호: causal set IR limit 에서 G_N 단조성 — Sorkin 부호 자유 (axiom 으로 결정 불가). 차원: ✓. OOM: Cassini |γ−1|<2.3e-5 이미 알려진 제약을 *통과해야 함* — postdiction 동기 강함 | **L2** | priori 아님 |

**임무 2 진정 신규 priori = 0**. P2a/P2b 모두 4-pillar coincidence (paper §2.4) 가 이미 알려진 ratio 이며, 그 *재해석* 은 postdiction. CLAUDE.md L6 §"Amplitude-locking 이론에서 유도됨 주장 금지" 에 따라 priori 자격 부인.

### 채널 3: Z₂ SSB + GFT/Causet → matter formation prediction

**Z₂ = paper §2.4 fourth pillar (matter–anti-matter discrete symmetry)**. Path-α 의 시간 의존 Γ₀(t) 와 결합 시 hybrid 효과:

| ID | 후보 (방향) | hybrid 추가 효과 | 자격 감사 | priori 등급 |
|----|-------------|-----------------|-----------|-------------|
| **P3a** (Path-α + GFT) | GFT BEC 의 *condensate phase* 가 Z₂ SSB 를 일으킬 때 **domain wall 잔재 (scar)** 발생. SSB 가 *시간 의존* 인 Γ₀(t) 환경에서 일어나므로, scar 는 cosmic time 에 따라 *생성 → 진화 → 부분 소멸*. 지표: **CMB B-mode polarization 의 비-가우시안 anisotropy** (domain wall network) — *부호*: 양수 (anisotropy ≥ 0 자명), *차원*: ✓ (μK²), *OOM*: GFT condensate scale × Hubble volume 비로 결정 시도 가능. 관측 미예측 영역 (LiteBIRD/CMB-S4 미래 채널) | 부호 ✓ (자명). 차원 ✓. OOM: GFT mode count (j_max) + sprinkling rate *없이* "domain wall 면적 ∝ 1 horizon²" 면적-bound 만으로 OOM 추정 가능 — *holographic axiom (4-pillar 3rd)* 단일 보조 가정으로 충족. 관측 *미존재* (LiteBIRD 2032+) → postdiction 불가능 — *진정 priori 시간 정합* ✓ | **L1 (genuine priori candidate)** | **★ priori 후보** |
| **P3b** (Path-α + Causet) | Causet meso 의 manifoldlike 회복이 Z₂ 깨짐과 결합 → **이산 인과 그래프 위 domain 경계** 가 후속 manifold limit 에서 cosmic string-like 잔재 또는 *bulk 흐름 비대칭* 으로 surface. 지표: **UHE-CR 도착 방향 dipole** (Auger upper limit 와 정합 또는 차세대 GCOS 검증). | 부호: Causet sprinkling 의 매개변수 자유도 — 부호 자유. 차원: ✓. OOM: sprinkling rate 1 axiom + horizon 부피 → OOM 결정 가능. 관측: claims_status v1.2 의 `uhe-cr-anisotropy` 가 이미 *pre-reg* — postdiction 위험 *낮음* (관측 미확정) | **L1 candidate (조건부)** | priori 후보 (단 dormant) |

**임무 3 진정 신규 priori = 1 강 (P3a) + 1 약 (P3b)**. P3a 는 LiteBIRD/CMB-S4 가 아직 관측 *전* 인 영역이므로 시간 정합 ✓. P3b 는 pre-reg 상태로 dormant.

**P3a 는 본 감사의 유일한 *진정 priori* 후보** — 단 "도출 가능" 이며 "도출됨" 아님. 8인 Rule-A 라운드의 자유 도출 의무 (CLAUDE.md [최우선-2]) 가 부호/OOM 검증 후 등급 확정.

### 채널 4: holographic → entropy bound prediction

**holographic = paper §2.4 third pillar**. base.md 4-pillar 와 L530 후보 A (holographic-only) 가 이미 다수 다룸.

| ID | 후보 (방향) | hybrid 추가 효과 | 자격 감사 | priori 등급 |
|----|-------------|-----------------|-----------|-------------|
| **P4a** (Path-α + GFT) | GFT condensate 의 *유한 정보 용량* 이 horizon entropy bound 와 결합 → **CEB (covariant entropy bound) 의 saturation rate** 가 cosmic time 의 단조 함수. 지표: gravitational wave background 의 stochastic spectrum 에서 **horizon-saturation feature** | 부호: Bousso CEB ≥ 0 자명. 차원: ✓. OOM: Planck area + Hubble area 만으로 결정 — *그러나* L530 §A 는 이미 holographic-only 가 OOM 결정 가능을 인정 (B/B/B). hybrid 의 *신규성* = GFT depletion 이 saturation 의 *시간 derivative* 결정. 그런데 derivative 의 부호는 GFT formalism 자유도. 관측: nano-Hz GW (NANOGrav) 시대에 fit 가능 = postdiction 위험 *높음* | **L2** (postdiction 동기 — NANOGrav 결과 알려짐) | priori 아님 |
| **P4b** (Path-α + Causet) | Causet sprinkling 이 *area* 가 아닌 *causal diamond volume* 으로 entropy bound 정의 → 전통 Bekenstein-Hawking 과 **OOM 1 차이** 의 새 bound. 지표: black-hole evaporation rate 의 **late-stage 편차** (LISA 시대 조건) | 부호: Sorkin 부호 자유 (변동 분산). 차원: ✓. OOM: Planck⁴ × diamond volume — 1 axiom (sprinkling rate) 결정 ✓. 관측: LISA 2035+ → 시간 정합 ✓ | **L1 candidate** | **★★ priori 후보 (약)** |

**임무 4 진정 신규 priori = 1 약 (P4b)**. 단 P4b 는 Sorkin BH 라인의 *재상속* (L530 §C 특이사항) 이며 hybrid 의 *Path-α 기여* 가 미미 — Causet 단독으로도 도출 가능. **hybrid-귀속 신규 priori = 부분**.

---

## 3. 종합 자격 감사 표

| ID | 채널 | hybrid 조합 | 등급 | priori? | hybrid-귀속? | 시간 정합 | 신규성 |
|----|------|-------------|------|---------|--------------|-----------|--------|
| P1a | SK | α + GFT | L2 | ✗ | – | – | – |
| P1b | SK | α + Causet | L1* | (재상속) | 부분 | – | L379 inherit |
| P2a | RG | α + GFT | L2/L3 | ✗ | – | postdiction 동기 | – |
| P2b | RG | α + Causet | L2 | ✗ | – | – | – |
| **P3a** | **Z₂ SSB + GFT** | **α + GFT** | **L1** | **✓ 후보** | **✓ 강** | **✓ (LiteBIRD 미관측)** | **신규** |
| P3b | Z₂ SSB + Causet | α + Causet | L1 cond | △ (dormant) | 부분 | △ (pre-reg) | dormant |
| P4a | holographic | α + GFT | L2 | ✗ | – | postdiction 위험 (NANOGrav) | – |
| P4b | holographic | α + Causet | L1* | (재상속) | 부분 | ✓ (LISA 미관측) | Sorkin BH inherit |

`*` = 재상속 (L379 / Sorkin BH 라인 inheritance, hybrid 신규성 부정)

**진정 *priori 후보* = P3a 1 건 (강), P3b 1 건 (약·dormant). 재상속 = P1b, P4b. 나머지 4 건 priori 부인.**

---

## 4. *priori* vs *postdiction* 정직 audit (요구 임무 직접 응답)

| 후보 | priori? | postdiction 위험원 |
|------|---------|---------------------|
| P1a | ✗ | GFT λ 가 fit 입력 |
| P1b | inherited priori | L379 결과 사전 사용 (신규 도출 아님) |
| P2a | ✗ postdiction | 4-pillar coincidence ratio ≈ O(1) 이 *동기* (paper §2.4 알려진 사실) |
| P2b | ✗ | Cassini 통과 *동기* (관측값 알고 reverse-engineer) |
| **P3a** | **✓ priori 후보** | LiteBIRD/CMB-S4 미관측 → 부호/OOM 사전 명시 가능 시간 ✓. 단 "도출됨" 은 8인 라운드 통과 후 |
| P3b | △ priori 후보 (dormant) | claims_status `uhe-cr-anisotropy` 가 이미 pre-reg — 형식적 priori 자격 ✓, 단 8인 도출 미실행 |
| P4a | ✗ postdiction 위험 | NANOGrav 2023 결과가 *알려진* 입력 |
| P4b | inherited priori | Sorkin BH variance 라인 사전 사용 |

---

## 5. CLAUDE.md 재발방지 매핑

- **L4 K10 (sign-consistency)**: P3a 부호 ✓ 자명 (anisotropy ≥ 0). P4b 부호는 sprinkling 자유도 — 8인 라운드 의무 검증.
- **L6 §"Amplitude-locking 이론에서 유도됨 주장 금지"**: P2a (a₀×Λ ratio) 는 본 규칙에 직접 저촉 — priori 자격 부인 정합.
- **L6 §"PRD Letter 진입 조건 (Q17 + Q13/Q14)"**: P3a 가 8인 라운드 통과 → CMB-S4 detection 시 *Q14 후보* (외부 검증). 단 Q17 (amplitude-locking) 미해결 — PRD Letter 진입 자격 *부분 충족*.
- **L530 §특이사항 ("재상속")**: P1b, P4b 는 inheritance 이므로 hybrid 의 *진정 신규* 아님 — 본 감사 §3 표에 명시.
- **[최우선-1] 지도 금지**: 본 문서는 부호/등급/시간정합 *방향* 만 제시, 함수형·파라미터 *값* 0건. ✓
- **[최우선-2] 팀 독립 도출**: P3a 의 부호/OOM 도출은 8인 Rule-A 라운드 의무 — 본 감사는 *후보 명단* 만.

---

## 6. 부록 — channel-cross 및 Volovik companion (요청 외 보조)

> 임무 4 채널을 넘어선 추가 후보. 본 감사 결론에 영향 없음 — 보강 자료.

- **X1 (channel-cross 1×3)**: SK propagator 의 cutoff scale 이 Z₂ SSB 시점 결정 — domain wall scar amplitude 와 SK Λ 가 *동일 axiom* (axiom 3' Γ₀(t)) 으로 동시 결정 시 Q17 amplitude-locking *진정 도출* 가능. **추정 등급 L0 후보** (단 "도출 가능" 단계 — 6 후보 중 유일하게 L0 도달 가능성).
- **X2 (channel-cross 4×2)**: holographic CEB saturation × RG flow → galactic-cosmic 4-pillar coincidence 가 *RG fixed point + horizon area saturation* 동시 만족조건으로 자동. **L1 candidate** (단 P2 의 postdiction 위험 상속).
- **V1 (Volovik companion, L530 후보 B)**: Two-fluid normal-fraction 이 S₈ 성장 채널에 *직접* 진입 — μ_eff ≠ 1 자연 발생. CLAUDE.md L5/L6 "S₈ 해결 불가" 재발방지 *부분 회피* 가능. 단 priori 자격은 두 상 EOS 가 fit 입력이므로 **L2** (priori 아님). companion 은 phenomenology 보강용이며 priori 후보 아님.

X1 은 본 감사가 *방향만* 제시한 추가 cross-channel 으로, 8인 Rule-A 라운드의 자유 도출 의무에 위임. 본 문서가 X1 의 함수형·부호 *지도* 제공 금지 ([최우선-1]).

---

## 7. 정직 한 줄 (재진술)

**hybrid (Path-α + GFT BEC 또는 Causet meso) 의 4 채널 8 후보 + cross 2 + Volovik companion 1 = 11 후보 중 *진정 priori 후보* = P3a (Z₂ SSB + GFT BEC → CMB-S4 domain-wall scar) 1 건이 강·신규·시간정합. P3b (Causet UHE-CR dipole) 1 건이 약·dormant. P1b/P4b 는 재상속 (L379/Sorkin) 이며 hybrid 신규성 부정. 나머지 6 건 (P1a/P2a/P2b/P4a + V1) 은 L2/L3 — priori 자격 부인. cross-channel X1 (SK × Z₂ × axiom 3' Γ₀(t)) 가 유일한 L0 도달 가능성 후보 — 단 8인 Rule-A 자유 도출 의무. 본 감사는 *후보 명단* 만 제시하며 함수형·OOM 수치 0건 ([최우선-1] 정합).**

---

## 8. 산출물 정직성 체크

- 신규 수식 0줄, 신규 파라미터 0개. ✓
- paper/base.md edit 0건, simulations/ 코드 0줄, claims_status edit 0건. ✓
- L527/L530/L531 substrate 만 사용 (L528–L529, L532–L535 디스크 부재 정직 미시도). ✓
- L527 L530 인용 페이지 § 명시 §1.2, §2.2, §3, §A, §C, §특이사항. ✓
- 8인/4인 라운드 결과 *없음* — 본 문서는 *후보 명단* 으로 한정. priori 등급 확정은 후속 Rule-A 통과 의무. ✓
- 결과 왜곡 금지 (CLAUDE.md): "1 건 진정 priori" 대신 "도출 가능 1 건, 도출됨 0 건" 정직 명시. ✓

---

*저장: 2026-05-01. results/L536/NEW_PRIORI.md. 단일 메타-감사 에이전트. CLAUDE.md [최우선-1] / [최우선-2] / 결과 왜곡 금지 / L4 K10 / L5 L6 재발방지 / disk-absence 정직 인정 모두 정합.*
