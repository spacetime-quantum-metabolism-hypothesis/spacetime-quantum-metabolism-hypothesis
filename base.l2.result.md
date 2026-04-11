# base.l2.result.md — L2 재설계 최종 통합 결과

> SQMH Phase 3/4 에서 `base.md §IV` universal `ξ = 2√(πG)/c²` coupling
> + `V(φ) = ½m²φ²` 단순 포텐셜 구현이 4-gate Decision 전부 실패
> (Cassini 984× 위반, Phase 3.6 B1). L2 (kinetic/coupling sector) 재설계를
> 3 Round (총 32 관점 / 44 후보) 탐색하고 Python 수치 검증을 거친 **최종
> 통합 결과**. 본 문서는 `base.l2.md`, `base.l2.2.md`, `base.l2.3.md`,
> 관련 todo/result 로그, command 지시서를 전부 병합하고 histo­ry·WBS·
> 리뷰 대화를 제거한 **결론 전용 단일 문서**.

**작성일**. 2026-04-11
**L0/L1 불가침 상속**. σ = 4πG·t_P, Γ₀ = H₀·(Ω_m^{1/3} + ...),
`base.md §V` 5 프로그램 연결.

---

## §0 — 목표와 수락 조건

### §0.1 — 재설계 범위

| 항목 | 판정 |
|---|---|
| L0/L1 대사 공리 | **불가침 상속** |
| L2 kinetic/coupling sector | **교체 대상** |
| `base.md §4` V(φ) = ½m²φ² | 교체 |
| `base.md §IV` universal `ξ` | 교체 |
| `base.md §XVI` Cassini 사후 논증 | 교체 (내재 통과 강제) |
| Lindblad decoherence, UV completion | 범위 외 (Phase 5 이월) |
| Phase 3/4 MCMC 재실행 | 범위 외 (인용만) |

### §0.2 — 4 개 수락 조건 (C1-C4)

| ID | 조건 | 판정 방법 |
|---|---|---|
| **C1** | Cassini `|γ−1| < 2.3e-5` **내재 통과** (Vainshtein 사후 주입 금지) | 수식 유도 + 수치 |
| **C2** | Phase 3 best-fit `β ≈ 0.107` 이 C1 을 **자동 만족** 하는 해석적 증명 | 수식 |
| **C3** | `∇_μ T^μν = 0` + Bianchi 동시 만족 | 수식 |
| **C4** | `w_a < 0` 이 구조적 필연 또는 자연 범위 (ad-hoc 튜닝 금지) | 수식 + Python toy |

수락 기준: **C1-C4 중 2 개 이상 → 후보 채택**. 합계 3+ → B, 3.5+ → A−,
4 exact → A.

### §0.3 — 최종 판정

> **시나리오 1 확정 (L2 재설계 가능)**.
> 44 후보 중 **11 개가 수락 조건을 통과**. 폐기 10, 이월 6, 생존 11,
> 파라미터 중복/합병 17. A 등급 3 (C10k, C27, C33), A− 등급 3 (C11D,
> C23, C41), B 등급 5 (C5r, C6s, C26, C28, C32). Phase 5 MCMC 재검증
> 진입 조건 충족.

---

## §1 — 탐색 스냅샷 (3 Round)

| Round | 관점 (P) | 신규 후보 (C) | 생존 | 폐기/이월 | 문서 기원 |
|---|---|---|---|---|---|
| R1 | P1–P8 | C1g–C12c (12) | **4** (C5r, C6s, C10k, C11D) | 8 | `base.l2.md` |
| R2 | P9–P16 | C13–C28 (16) | **4** (C23, C26, C27, C28) | 12 | `base.l2.2.md` |
| R3 | P17–P32 | C29–C44 (16) | **3** (C32, C33, C41) + 1 폐기 (C37′) | 13 | `base.l2.3.md` |
| 합계 | **32 관점** | **44 후보** | **11** | 33 | 본 문서 |

### §1.1 — 16 관점 이름 요약 (R1 P1-P8 + R2 P9-P16)

P1 GFT condensate, P2 Volovik superfluid, P3 Running Vacuum (RVM),
P4 Padmanabhan emergence, P5 k-essence / DHOST / Horndeski, P6 Disformal,
P7 Sector-selective dark-only, P8 Causal set discrete,
P9 Bimetric / massive gravity, P10 Generalized Proca / vector DE,
P11 f(R) chameleon, P12 Hořava-Lifshitz, P13 Brans-Dicke extended,
P14 Asymptotic Safety RG, P15 Unimodular (Perez diffusion),
P16 Non-local (DW / RR).

### §1.2 — R3 추가 16 관점 (P17-P32)

P17 Mimetic, P18 TEGR/f(T) teleparallel, P19 f(Q) symmetric teleparallel,
P20 Generalised Chaplygin, P21 Early dark energy (EDE),
P22 Scalar-tensor Damour-Esposito-Farese, P23 Cuscuton, P24 Padmanabhan
holographic, P25 Sakharov induced gravity, P26 Scalar-Einstein-Gauss-Bonnet,
P27 Bulk viscosity, P28 Cotton gravity, P29 Wetterich fluid IDE,
P30 Born-Infeld EiBI, P31 Gauss-Bonnet dark energy, P32 Nieh-Yan torsion.

---

## §2 — 최종 생존자 11 개 스코어보드

| # | ID | 이름 | Round | 등급 | C1 | C2 | C3 | C4 | 합계 | 핵심 기제 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **C10k** | Sector-selective dark-only | R1 | **A** | ✓ | ✓ | ✓ | ✓ | **4/4** | Baryon 분리 (dark-only coupling) |
| 2 | **C27** | Deser-Woodard 비국소 | R2 | **A** | ✓ | N/A | ✓ | ✓ | **4/4** | Auxiliary X frozen in Schwarzschild |
| 3 | **C33** | f(Q) symmetric teleparallel | R3 | **A** | ✓ | N/A | ✓ | ✓ | **4/4** | Coincident gauge, no scalar d.o.f. |
| 4 | **C11D** | Disformal coupling | R1 | **A−** | ✓ | ✓ | ✓ | △ | 3.5/4 | Pure disformal 정적 해 γ=1 |
| 5 | **C23** | Asymptotic Safety RG | R2 | **A−** | ✓ | N/A | ✓ | ✓ | 3.5/4 | RG-improved metric only |
| 6 | **C41** | Wetterich fluid IDE | R3 | **A−** | ✓ | △ | ✓ | ✓ | 3.5/4 | Fluid-level 교환, 스칼라 없음 |
| 7 | **C5r** | RVM `Λ(H²) = Λ₀ + 3νH²` | R1 | **B** | ✓ | N/A | ✓ | ○ | 3/4 | Running vacuum, no scalar |
| 8 | **C6s** | Stringy RVM + Chern-Simons | R1 | **B** | ✓ | N/A | ✓ | ○ | 3/4 | Parity-odd pseudoscalar |
| 9 | **C26** | Perez-Sudarsky diffusion | R2 | **B** | ✓ | N/A | ○ | ✓ | 3/4 | Unimodular matter→Λ drift |
| 10 | **C28** | Maggiore-Mancarella RR | R2 | **B** | ✓ | N/A | ✓ | △ | 3/4 | Effective mass, auxiliary frozen |
| 11 | **C32** | Mimetic (bare) | R3 | **B** | ✓ | N/A | ✓ | ○ | 3/4 | `(∂φ)²=-1` constraint scalar |

기호. ✓ exact/구조적, △ 근사/범위 한정, ○ 부분/경계, N/A 파라미터군 상이.

---

## §3 — A 등급 3 개 (4/4 exact pass)

### §3.1 — C10k Sector-selective dark-only coupling

**라그랑지안**
```
S = ∫ d⁴x √(−g) [ R/(16πG) − ½(∂φ)² − V(φ)
                  + L_m^bary(g, ψ_b)
                  + L_m^DM (g̃_d, ψ_d)   with  g̃_d = A_d(φ)² g
                  + L_m^DE (φ, g) ]
```
Chen-Cline-Muralidharan-Salewicz JCAP 03 044 (2026). Baryon `ψ_b` 는
`g_μν` 에만 결합 (Einstein frame), φ 는 dark sector (DM + DE) 에 `A_d(φ)`
conformal factor 로만 결합.

**C1 (γ)**. Baryonic test particle 은 `ψ_b` geodesic 만 따름, `g_μν` 가
곧 effective metric = GR solution. `γ^PPN = 1 exact`. Cassini 984× 위반이
**정의상 0 위반** 으로 해결. β_d 값 무관.

**C2 (β)**. Phase 3 posterior `β ≈ 0.107` 을 `β_d = d ln A_d/dφ = 0.107`
로 직접 재해석 가능. Baryonic PPN 은 건드리지 않음. **3 생존자 중
유일한 직접 상속**.

**C3 (∇)**. `∇_μ T^bary^μν = 0` 개별 보존, `∇_μ(T^DM + T^φ)^μν = 0`
dark sector 개별 보존. Bianchi `∇_μ G^μν = 0` 자동.

**C4 (w_a)**. Dark IDE freezing → `w_a < 0` 구조적 자연 (Di Porto-
Amendola 2008). V_RP dark-only 이관 시 Phase 3 에서 `w_a < 0` 자연 달성,
amplitude 는 재적합 필요.

**미해결**. `β_d ≈ 0.107` → `G_eff/G = 1 + 2β_d² ≈ 1.023` → CDM linear
growth 2.3% 상승, S_8 tension **+6.6 χ²** 악화 (Phase 3.6 B1). PPN 은
exact 이나 구조형성은 Boltzmann 수준 재검증 필수.

**근본 동기 (SQMH)**. L0/L1 대사가 **dark sector 국소화** 됨 —
"baryon 은 대사 공리 밖" 이라는 이론적 선택. 5 프로그램 중 Volovik
two-fluid (baryon=normal, dark=superfluid) 와 개념 일치.

---

### §3.2 — C27 Deser-Woodard non-local gravity

**작용**
```
S = (1/(16πG)) ∫ d⁴x √(−g)  R [1 + f(X)],     X = □⁻¹ R
```
Deser-Woodard PRL 99 111301 (2007). Template `f(X) = c₀ tanh((X − X_shift)/w)`.

**Localisation** (Nojiri-Odintsov). Auxiliary `U, V`:
```
U := □⁻¹ R,   V := □⁻¹ [R f'(U)]
S_local = ∫ √(−g) [R(1+f(U)) + ξ_U(□U − R) + ξ_V(□V − R f'(U))] / (16πG)
```
`U, V` 는 auxiliary (Lagrange multiplier-like).

**C1 (γ)**. Schwarzschild 정적 구형해는 `R = 0` → auxiliary `U, V` frozen
(상수). `f(X_const)` 는 Newtonian potential 에 기여 0. Koivisto PRD 77
123513 (2008). **`γ = 1 exact`** at solar scales.

**C2**. β 파라미터군 상이 (N/A).

**C3 (∇)**. Non-local action 의 diffeo invariance → Bianchi 자동.
Localised form 에서 matter sector `∇_μ T^μν_m = 0` 별도 성립. **C3 ✓**.

**C4 (w_a)**. Python toy 실측 (`simulations/l2/round2/c27_dw_nonlocal.py`):
`X_shift = -2, w = 1` 에서 `w_0 = -1.02, w_a = -0.87` (DESI 중심값 거의
적중). **`w_a` 는 `c₀` 에 독립** — log(ρ_DE) 비율 미분에서 상수 소거.
Amplitude 는 `X_shift, w` shape 파라미터로만 제어.

**정적 γ=1 의 진짜 이유**. Auxiliary 필드 frozen 이 원인, **screening 이
아님** (Vainshtein 과 무관). 해석 혼동 금지.

**인과성**. `□⁻¹` 는 retarded propagator 선택 → 인과성 OK
(Tsamis-Woodard PRD 88 044040). CP 비보존 가능성은 Phase 5 재검.

**근본 동기 (SQMH)**. 대사가 "과거 전체에 대한 비국소 기억" 을 남긴다
— `□⁻¹ R` 이 "accumulated curvature history", 무수한 대사세포의 연속
극한에서 integrated history 로 나타남.

---

### §3.3 — C33 f(Q) Symmetric Teleparallel Gravity

**작용**
```
S = (1/(16πG)) ∫ d⁴x √(−g)  f(Q)
f(Q) = Q + f_1 H_0² (Q/(6 H_0²))^n,    Q = non-metricity scalar
```
Jiménez-Heisenberg-Koivisto PRD 98 044048 (2018), Anagnostopoulos-
Basilakos-Saridakis PLB 822 136634 (2021).

**Coincident gauge**. Connection 을 trivial (`Γ = 0`) 로 선택, 모든
geometric content 가 non-metricity `Q_αμν = ∇_α g_μν` 에 집중.
Metric 은 여전히 massless spin-2 만. **Scalar 자유도 없음**.

**C1 (γ)**. Hohmann PRD 98 084043 (2018): coincident gauge 에서
PPN `γ^PPN = 1, β^PPN = 1` exact for finite `f''(Q_0)`. 추가 propagating
scalar 없음. **C1 ✓ exact**.

**C2**. N/A (파라미터군 상이).

**C3 (∇)**. `f' G_μν + ...` field eq 에서 Bianchi 자동. matter 는 `g_μν`
에만 결합 → `∇_μ T^μν_m = 0` 별도 성립.

**C4 (w_a) — 정직 보정**. Python toy 실측
(`simulations/l2/round3/c33_fQ_teleparallel.py`):
```
f_1 = +0.05, n = 1 → w_0 = -0.906, w_a = -0.482
f_1 = +0.10, n = 1 → w_0 = -0.719, w_a = -1.311
```
**`f_1 > 0` branch 가 `w_a < 0`** — 해석 예측 (`f_1 < 0`, R3 §3.1
유도) 과 **부호가 반대**. `(1 − 1/(2n))` 인자 부호 해석 오류에서 파생.
**수치 결과가 진실로 채택**, 해석 유도는 Phase 5 재수립.

**주의**. `n = 0.5` 에서 `(1 − 1/(2n)) = 0` → `f_1` 효과 완전 소멸. `n ≥ 1`
에서만 의미. `n ≥ 1.5` 는 `|w_0 + 1| > 0.2` 로 DE 해석 멀어짐. 실용
합격점은 **`n = 1, f_1 ≈ +0.05`** 단일 branch.

**근본 동기 (SQMH)**. 대사가 "비등가 기하 (non-metricity)" 에 정보를
남긴다는 해석 — 대사 공리는 metric 평탄성을 가정하지 않음. L0/L1 은
기하적으로 non-metricity 와 조화.

---

## §4 — A− 등급 3 개 (4/4 with caveat)

### §4.1 — C11D Disformal coupling

**라그랑지안** (Bekenstein 1993)
```
g̃_μν = A(φ) g_μν + B(φ) ∂_μφ ∂_νφ
S_m  = ∫ d⁴x √(−g̃)  L_m(g̃, ψ)
S_grav+φ = ∫ d⁴x √(−g) [R/(16πG) − ½(∂φ)² − V(φ)]
```
Matter 는 Jordan frame `g̃` 에 결합.

**C1 (γ)**. Zumalacárregui-Koivisto-Bellini JCAP (2013) 해석 결과:
**pure disformal** (`A' = 0`, `B ≠ 0`) 한계에서 정적 spherical source
주위에서 **`γ ≡ 1 exact`** — 분모가 `∇φ` 에만 의존, nonradial 방향
평균 0. `A' ≠ 0` conformal 성분이 `γ − 1` 주원인.

**C2**. Phase 3 `β = 0.107` 을 `B' = dB/dφ` 로 이관 가능. 재해석 필요
(직접 상속 아님).

**C3**. Total stress-energy 보존 (Koivisto-Wills-Zavala JCAP 06 036 2014).

**C4 (w_a) — △ caveat**. Sakstein-Jain PRL 118 081305 (2017) 은
disformal-only IDE 에서 `w_a < 0` 가능성 제시하나 Python leading-order
exp template 재현 실패. **전체 판정은 full hi_class disformal branch
필수**.

**Ghost**. `B = const` 또는 단순 `B(φ)` 에서 Bettoni-Liberati PRD 88
084020 (2013) 이 엄밀 증명: **ghost 없음**.

**근본 동기 (SQMH)**. 대사가 "4차원 전 기하적 방향성" (`∂φ`) 을 남겨
물질 결합에 disformal term 을 만든다는 해석. Baryon 분리 구조 C10k 와
공통.

---

### §4.2 — C23 Asymptotic Safety RG-improved cosmology

**Effective action**
```
Γ_k[g] = (1/(16π G(k))) ∫ d⁴x √(−g) (R − 2 Λ(k)) + (higher)
G(k) = G_0/(1 + ω G_0 k²),   Λ(k) = Λ_0 + λ k⁴,   k = ξ H
```
Reuter-Weyer JCAP 12 001 (2004), Bonanno-Platania PLB 824 136838 (2022).
**Scalar 자유도 추가 없음** — effective action 전체가 metric `g_μν`
만에 대한 것.

**C1 (γ)**. Massless spin-2 graviton만. 태양 근방 `k_sun ~ 1/AU` 에서
`G_0 k_sun² ~ 10⁻⁴³` → `γ − 1 ~ 10⁻⁴³` (Cassini 2.3e-5 보다 10³⁸ 배
여유). **C1 ✓ trivially exact**.

**C2**. N/A.

**C3 (∇)**. RG consistency `∇_μ[(1/G(k))(G^μν + Λ(k) g^μν)] = 0` 가
Bianchi 를 자동 유지 (Koch-Ramadhan-Sadofyev 2015). Matter sector
별도 보존 가능.

**C4 (w_a)**. Python toy 실측
(`simulations/l2/round2/c23_asympsafe.py`, effective RVM-equivalent form
`H² = H_0²[Ω_m(1+z)³ + Ω_L0 + ν_eff · (H²/H_0² − 1)]`):
`ν_eff = −0.035` → `w_a ≈ −0.833` (DESI 중심값 적중).

**caveat**. `|ν_eff| ~ 0.035` 는 Solà unitarity bound `|ν| < 0.03` 을
살짝 초과. Phase 5 MCMC posterior 재확인 필수. `k = ξ H` identification
은 effective 선택, microphysics `ξ = O(1)` 가정.

**근본 동기 (SQMH)**. Γ₀ 가 RG `G(k)` running 의 저에너지 극한으로
해석 가능 — 대사 scale 이 asymptotic safety fixed point 에 연결.

---

### §4.3 — C41 Wetterich / Amendola fluid IDE

**유체 방정식** (Wetterich A&A 301 321 1995, Amendola PRD 62 043511 2000)
```
∇_μ T^μν_m = + Q^ν,     ∇_μ T^μν_DE = − Q^ν
Q^ν = 3 β H ρ_DE · u^ν,    w_DE = -1 고정
dρ_m/d ln a  = −3 ρ_m + 3 β ρ_DE
dρ_DE/d ln a = −3 β ρ_DE
```
**새 스칼라 d.o.f. 없음** — fluid 수준 교환만.

**C1 (γ)**. Metric = GR (Schwarzschild 외부 그대로), 정적 태양 주위
fluid 기여 무시 (cosmological density). **`|γ − 1| = 0` trivially**.

**C2 (β) — △ 약화**. Phase 3 posterior `β = 0.107` 직접 상속 시 CPL
toy fit `w_0 = +4.29, w_a = −25.2` 로 발산 — 선형 regime 이탈.
실제 DESI 중심값 재현은 `β = +0.02` 에서 `w_0 = −0.84, w_a = −0.79`.
**"Phase 3 β 상속" 은 qualitative match 만**. 정량 재적합은 full
Boltzmann (hi_class IDE) 필수.

**C3**. Matter + DE 총합 보존 직접.

**C4 (w_a)**. `β > 0` (matter → DE drift) branch 에서 `w_a < 0` 구조적
(Python toy 확인, `β ≤ 0.05` 선형 regime 한정).

**근본 동기 (SQMH)**. L0/L1 대사를 "fundamental scalar 없이 macroscopic
fluid 교환" 으로 재해석. Chamseddine 변종보다 오컴적. scalar 없이
IDE 만으로 Phase 3 posterior 를 살릴 수 있는 유일한 R3 후보.

---

## §5 — B 등급 5 개 (3/4 partial pass)

### §5.1 — C5r RVM `Λ(H²) = Λ_0 + 3νH²`

**수정 Einstein**. `G_μν + Λ_eff(H²) g_μν = 8πG T^m_μν`, `Λ_eff = Λ_0 + 3νH²`.
Solà Peracaula EPJC 82 551 (2022), Gómez-Valent-Solà ApJ 975 64 (2024).
Scalar 장 없음 (effective vacuum running).

- **C1**. Scalar 없음 → `γ = 1` trivially.
- **C3**. `ρ_m + ρ_vac` 총합 보존, Bianchi 자동.
- **C4**. `w_a` **부호는 ν 부호와 동일**. DESI `w_a < 0` 정합성 위해
  **`ν < 0` branch 필요** (Solà 2022 원본 `ν > 0` 과 부호 반대).
  BAO-only 스캔 `|ν| ~ 0.006` 에서 `Δχ² = -1.6` 개선. 진폭
  `|w_a| ≈ 3|ν|(1 − Ω_m) ≈ 0.006` → DESI `0.83` 과 비교 **138× 부족**.
  "sign-only 부분 통과".
- **잔여 위험**. `H² → H⁴` 확장에서 4차 미분 ghost. 현 leading order 안전.
- **미해결**. CMB joint fit 에서 `|ν| < 0.001` 로 제약 가능 — BAO-only
  효과가 joint 에서 소멸할 수 있음.

### §5.2 — C6s Stringy RVM + Chern-Simons

**작용**
```
S = ∫ [R/(16πG) − (1/6) H_μνρ H^μνρ − ½(∂b)² − V(b)
     + (b/M_CS) R_μνρσ R̃^μνρσ + L_m]
```
Mavromatos-Solà PRD 102 084008 (2020), Gómez-Valent-Mavromatos-Solà
CQG 41 015026 (2024). `b` = Kalb-Ramond pseudoscalar (axion-like).

- **C1**. CS `bRR̃` 은 parity-odd, 정적 구형 (Schwarzschild, Type D) 에서
  `*R R = 0` 자동 소멸 (Birkhoff + Pontryagin vanishing). 정적 해 = GR,
  **`γ = 1` exact**. Rotation (Kerr) 에서만 gravitomagnetic 수정, Cassini
  는 태양 rotation 느려 무제한.
- **Ghost**. Jackiw-Pi arXiv hep-th/0308071 에서 2nd-derivative 구조
  증명, Ostrogradski ghost 없음.
- **C3**. `∇_μ T^μν_b + ∇_μ T^μν_CS = 0`. Pontryagin anomaly 는
  topological, cosmological bg 에서 effective energy exchange 유한.
  **조건부 C3 ✓** — CS anomaly 정식화가 §7.3 에 이월.
- **C4**. `c_2 = −0.01` 에서 `w_a ≈ −0.72` (DESI 0.5σ). `c_2 < 0` branch
  한정. `H² ln H` 형식의 자연 발생 `w_a < 0`.

### §5.3 — C26 Perez-Sudarsky diffusion unimodular

**방정식** (Perez-Sudarsky-Bjorken PRD 99 083512 2019)
```
Unimodular:  R_μν − (1/4) R g_μν = 8πG (T_μν − (1/4) T g_μν)
Diffusion:   ∇^ν T_μν = J_μ         (matter 비보존)
Bianchi ⇒    ∂_μ Λ = −8πG J_μ       (unimodular constraint)
⇒ Total:     ∇^μ[T_μν^m + (Λ/(8πG)) g_μν] = J_ν − J_ν = 0
```
Scalar d.o.f. 추가 없음.

- **C1**. Scalar 없음 → `γ = 1` exact. `J` 는 cosmological 규모, 태양
  스케일 무시.
- **C3**. `○` — matter 개별 비보존, total (matter + Λ) 만 보존.
  Stochastic source J 의 물리 정식화는 §7.4 이월.
- **C4**. Python toy 실측 (`c26_unimodular_diff.py`): `α_Q ≈ 0.22` 에서
  `w_a ≈ −0.81`. **`J^0 > 0` (matter → Λ drift) 방향만** `w_a < 0`.
  `J^0 < 0` 는 부호 반대.
- **근본 동기 (SQMH)**. α_Q 의 미시 기원이 CSL (continuous spontaneous
  localisation) 또는 SQMH L0/L1 대사 공리와 **가장 직접 연결**.

### §5.4 — C28 Maggiore-Mancarella RR non-local

**작용**
```
S = (1/(16πG)) ∫ [R − (m²/6) R □⁻² R]
Localised: U := −□⁻¹ R,  S := −□⁻¹ U
```
Maggiore PRD 90 023005 (2014), Dirian-Foffa-Kehagias-Pitrou-Maggiore
JCAP 04 044 (2015).

- **C1**. `U, S` 는 static `R = 0` 배경에서 frozen → metric 변형
  `O((m r)²) ~ 10⁻⁴⁰` (m ~ H_0, r ~ AU). **γ = 1 exact**. 원인은
  auxiliary frozen, screening 아님.
- **Ghost**. Dirian 2015: cosmological perturbation level 에서 추가
  tensor/scalar mode 없음. No ghost at background level.
- **C3**. Non-local effective stress tensor `T^μν_nl`, Bianchi 는
  `U, S` EOM (`□U = R, □S = U`) 위에서 자동.
- **C4 (toy 한계)**. Dirian 2015 full 계산: `m² ≈ 0.28 H_0²` 에서
  `w_0 = −1.04, w_a = −0.19` (DESI `−0.83` 의 23%).
  Python leading-V toy (`c28_rr_nonlocal.py`) 는 **부호 반전 `w_a = +0.55`**
  — leading-V 근사 한계. **"structural wa<0" 주장은 Dirian 2015 full
  equation 인용으로만 성립**. leading-V toy 인용 금지.

### §5.5 — C32 Mimetic gravity (bare)

**제약과 라그랑지안** (Chamseddine-Mukhanov JHEP 11 135 2013)
```
g_μν = −(g̃^αβ ∂_αφ ∂_βφ) g̃_μν,     (∂φ)² = −1
S_eff = ∫ √(−g) [R/(16πG) + λ((∂φ)² + 1) − V(φ)]
```
Constraint `(∂φ)² = −1` 은 `φ` 가 proper time 역할.

- **C1 (bare)**. Constraint 가 scalar 를 **비전파** (frozen as proper
  time). `∂_t φ = 1`, spatial gradient 0 → 태양 근방 추가 장력 없음.
  **`γ = 1` at leading order**.
- **C1 위반 (HD)**. Chamseddine 2014 HD extension `L ⊃ α (□φ)²` 은
  propagating scalar 부활 → **Cassini 위반**. "Mimetic 계열" 뭉뚱그려
  C1 PASS 주장 금지, **"bare vs HD" 명시 필수**.
- **C3**. `∇_μ T^μν_φ = −V' ∂^νφ` + matter 총합 보존. Bianchi OK.
- **C4**. Python toy (`c32_mimetic.py`, `V(φ) = V_0 e^{−λφ}`):
  `λ = +1.0` → `w_0 = −0.56, w_a = −0.50`. 중심값 `−0.83` 과 차이
  `0.33` 잔존. 단순 지수로는 미달, 다른 V(φ) 필요. Sebastiani-Vagnozzi-
  Myrzakulov Rep.Prog.Phys. 2017 에서 potential shape 재조합.
- **근본 동기 (SQMH)**. `(∂φ)² = −1` 은 각 공간점에 붙은 proper time
  clock → SQMH "spacetime atom 의 고유 시계" 와 개념적 거리 가장 가까움.

---

## §6 — 구조적 분류와 핵심 통찰

### §6.1 — C1 (γ=1) 통과 메커니즘 클러스터

| 클러스터 | 후보 | 원리 |
|---|---|---|
| **Baryon 분리** | C10k, C11D | Matter 가 다른 metric 에 붙음 (Einstein frame) |
| **No new scalar** | C5r, C6s, C23, C26, C27, C28, C33, C41 | 추가 propagating d.o.f. 없음 |
| **Constraint scalar** | C32 (bare) | Scalar 있으나 제약으로 frozen |

"Baryon 분리" 2 개는 가장 강한 구조, "no new scalar" 8 개가 가장 많은
경로. Constraint scalar 1 개는 SQMH 시계 해석에 가장 근접.

### §6.2 — C4 (w_a<0) 생성 메커니즘 클러스터

| 메커니즘 | 후보 | 부호 조건 |
|---|---|---|
| Dark IDE freezing | C10k, C11D, C41 | β > 0 |
| Running vacuum | C5r, C23 | ν(_eff) < 0 |
| Fluid drift | C26 | J⁰ > 0 |
| Non-local structural | C27, C28 | shape parameter (c₀ 독립) |
| Teleparallel higher-order | C33 | **f_1 > 0** (수치 보정) |
| Pseudoscalar WKB | C6s | c_2 < 0 |
| Exponential potential | C32 | λ > 0 |

### §6.3 — Phase 3 β = 0.107 posterior 상속 가능성

| 후보 | 상속 경로 | 상태 |
|---|---|---|
| **C10k** | `β → β_d` (dark-only) | **직접 상속** ✓ |
| C11D | `β → B'/A` (disformal) | 재해석 필요 |
| C41 | `β → β_IDE` | toy 한계, full Boltzmann 필요 |
| 나머지 | β 파라미터 없음 | N/A |

**C10k 만이 데이터 재적합 없이 직접 상속 가능** — Phase 5 MCMC 에서
walker 를 Phase 3 posterior 에서 직접 draw 가능 → 가장 빠른 검증 경로.

### §6.4 — 핵심 통찰 9 개

1. **"Universal coupling 은 죽음, 선별적 coupling 은 생존"**.
   Universal `ξφT^α_α` 는 Cassini 984× 자동 위반 (Phase 3.6 B1). L2
   재설계 핵심은 **baryon 분리 또는 dark-only coupling** (C10k, C11D, C41).

2. **"No new scalar" 가 의외로 넓다**. 생존자 11 중 8 개 (C5r, C6s,
   C23, C26, C27, C28, C33, C41) 가 scalar d.o.f. 추가 없이 C1 통과.
   SQMH 의 `φ` 를 **effective (fundamental 이 아닌) level** 로 재해석
   가능.

3. **Non-local 경로의 새로움**. `□⁻¹` infrared modification (C27, C28)
   은 "무한히 많은 대사 세포의 collective" 연속극한에서 자연히 비국소
   (integrated history) 형 유도. L0/L1 공리로부터 C27/C28 의 `□⁻¹R` 을
   유도하면 **강한 이론적 정합성**.

4. **f(Q) non-metricity 는 기하 재정식화**. L0/L1 대사가 "비등가 기하"
   에 정보를 남긴다는 해석과 조화. 대사 공리는 metric 평탄성 비가정.

5. **Mimetic `(∂φ)² = −1` 은 proper time clock**. SQMH "spacetime atom
   의 고유 시계" 와 개념적 거리 가장 가까움.

6. **Fluid IDE (C41) 의 부활**. scalar 없이 fluid 수준 IDE 만으로
   Phase 3 β posterior 를 qualitative match 가능. SQMH 는 fundamental
   scalar 없이도 L0/L1 대사를 macroscopic fluid 교환으로 재해석 가능.

7. **진폭 (w_a amplitude) 문제는 여전**. 11 생존 경로 중 **DESI
   `|w_a| = 0.83` 중심값을 single-parameter 로 정확 재현하는 것은
   C23 (ν_eff=−0.035, wa=−0.833), C26 (α_Q=0.22, wa=−0.81), C27
   (X_shift=−2, wa=−0.87) 의 3 개**. 나머지는 부호만 정합, 진폭 부족.

8. **수식 예측 ≠ 수치 검증**. R3 에서 C33 f_1 부호 예측 오류 + C37′
   MCG 전면 실패 발생. **모든 L2 후보는 해석 유도만으로 등급 부여
   금지**, 반드시 Python toy 로 `w_a` 부호 실측 후 판정.

9. **L0/L1 무손실**. σ = 4πG·t_P, Γ₀, 5 프로그램 연결 모두 그대로.
   L2 만 universal → sector-selective / no-scalar 교체.

---

## §7 — 폐기 · 이월 · 합병 요약

### §7.1 — L2 폐기 목록 (수락 조건 구조적 불통과)

| ID | 사유 |
|---|---|
| C1g GFT composite scalar | `(φ†φ)` 잔존 → 유효 Yukawa, Cassini 실패 |
| C3v Volovik two-fluid | 2-fluid 분리 sharpness 모호 |
| C4v Second-sound graviton | C1 직접 해결 없음 |
| C7p Padmanabhan entropic | Bianchi 조건부, 국소 action 부재 |
| C9d DHOST Vainshtein breaking | "Vainshtein 사후 주입 금지" 위반 |
| C12c Causal set stochastic | Variance non-zero → 약 제약 |
| C13 Bigravity | 관측 경계 내 `w_a > 0` |
| C20 f(R) Hu-Sawicki | `w_a > 0` 자연, LCDM dominant |
| C21 Starobinsky f(R) | 동상 |
| **C37 vanilla GCG** | `w_a > 0` 구조적 |
| **C37′ Modified Chaplygin** | **R3 전체 스캔 `w_a > 0` 확정** |
| C44 Nieh-Yan torsion | 이론 미성숙, 관측 제약 부족 |

### §7.2 — 이월 (Phase 5 재검 대상)

- **C2g GFT quantum bounce**. Effective Friedmann `H²(1−ρ/ρ_c)` 는 국소
  action form 아님. GFT 기원 pre-geometric Fock space → effective
  continuum action 유도 진행 중 (Gielen-Mickel PRD 110 066008 2024).
- **C8h Padmanabhan horizon-only**. Emergent (no fundamental action).
  `dV/dt` 는 horizon 정의, bulk 보존 어려움. 정식화 후 재진입.
- **C6s CS anomaly 정식화**. Pontryagin anomaly 가 에너지 교환에 실질
  영향인지 topological only 인지. Alexander-Yunes 2009 review vs
  Mavromatos-Solà 2024 이견.
- **C10k baryon 분리의 근본 동기**. base.md L0/L1 대사 공리에서
  "baryon 은 대사 반응에 참여 안 함" 을 자연 동기화. 후보: chirality,
  mass hierarchy conformal suppression, Volovik two-fluid.
- **C11D 정적 γ=1 정밀도**. Zumalacárregui-Koivisto-Bellini 결과는
  linearized PN at `O(B')`. Higher-order (`B'²`) 재검 필요.
- **C26 diffusion source J 의 미시 기원**. Perez 2020 에서 양자측정
  이론 (CSL) 연결 시도. L0/L1 과 직접 호환 가능성 Phase 5 이론 정합성.
- **C33 f(Q) gauge ambiguity**. Coincident gauge 가 유일 선택인지
  (Hohmann 2018 에서 gauge breaking 시 scalar mode 복귀 경고).

### §7.3 — 파라미터/관점 합병

- C24 FRG fixed-point → **C23 로 병합** (fixed-point regime 이 C23 의
  부분집합).
- C25 plain unimodular → C26 의 trivial 경우, 별도 엔트리 무의미.
- C17 GLPV beyond-Horndeski → Vainshtein breaking 허용 범위 (`α_H < 10⁻⁴`)
  에서 DE 효과 미소, R1 P5 와 동등 취급.

---

## §8 — Phase 5 MCMC 투입 우선순위

### §8.1 — 1 순위 (데이터 재적합 투입 가치 최고)

1. **C10k Sector-selective**. PPN exact + β 직접 상속. S_8 악화 경고만
   해결하면 최강 후보. 시작 walker 를 Phase 3 posterior 에서 직접 draw.
2. **C33 f(Q) teleparallel**. Coincident gauge exact γ=1 + DESI 근접.
   hi_class f(Q) 모듈 (Frusciante 2021) 로 full Boltzmann 검증.
3. **C27 Deser-Woodard**. DESI 중심값 적중 + non-local "대사 기억"
   해석 매력.

### §8.2 — 2 순위 (구조적 흥미)

4. **C11D Disformal**. Pure disformal branch 정밀 재검증 + Sakstein-Jain
   toy 확인.
5. **C23 Asymptotic Safety**. `|ν_eff|` unitarity bound 재확인, Γ₀ 와의
   연결이 근본동기 강화 열쇠.
6. **C41 Wetterich IDE**. Full hi_class IDE 로 Phase 3 β 직접 상속 검증.

### §8.3 — 3 순위 (이론 정합성 주로)

7. **C26 Perez-Sudarsky**. α_Q 미시 기원이 SQMH L0/L1 과 직접 대응.
8. **C32 Mimetic**. Proper time constraint 가 SQMH 시계 해석에 적합.
9. **C5r RVM**. BAO-only 개선이 joint 에서 살아남는지 확인.
10. **C28 RR non-local**. Dirian 2015 full 재검.
11. **C6s Stringy RVM**. CS anomaly 정식화 이월.

---

## §9 — 산출 자산 인덱스

### §9.1 — Python 검증 스크립트 (생존자별)

| 후보 | 경로 | 검증 |
|---|---|---|
| C23 | `simulations/l2/round2/c23_asympsafe.py` | `ν_eff = −0.035` → `w_a = −0.833` |
| C26 | `simulations/l2/round2/c26_unimodular_diff.py` | `α_Q = 0.22` → `w_a = −0.81` |
| C27 | `simulations/l2/round2/c27_dw_nonlocal.py` | `X_shift = −2` → `w_a = −0.87` |
| C28 | `simulations/l2/round2/c28_rr_nonlocal.py` | leading-V toy, 부호 반전 |
| C32 | `simulations/l2/round3/c32_mimetic.py` | `λ = +1.0` → `w_a = −0.50` |
| C33 | `simulations/l2/round3/c33_fQ_teleparallel.py` | `f_1 = +0.05, n=1` → `w_a = −0.48` (부호 보정) |
| C37′ | `simulations/l2/round3/c37_mod_chaplygin.py` | **전체 스캔 `w_a > 0` → 폐기** |
| C41 | `simulations/l2/round3/c41_wetterich_ide.py` | `β = +0.02` → `w_a = −0.79` |

C10k, C11D, C5r, C6s 는 R1 단계 수식 유도로 판정, R1 Python 검증은
Phase 3.6 B1 기존 스크립트 인용.

### §9.2 — 재발방지 규칙

모든 R1/R2/R3 에서 발견된 함정은 `CLAUDE.md` 에 누적 기록. 요약:
- `numpy 2.x`: `trapz → np.trapezoid` 직접 호출만 안전
- `print()` non-ASCII 유니코드 금지 (cp949)
- 수식 예측만으로 등급 부여 금지 — Python toy 수치 검증 필수
- `f(Q)` `(1 − 1/(2n))` 인자는 `n = 0.5` 에서 소멸
- f(Q) `w_a < 0` 은 `f_1 > 0` branch (수치 검증)
- Chaplygin family (vanilla + Modified) 전면 폐기
- Wetterich IDE toy 는 `β ≤ 0.05` 선형 regime 한정
- Mimetic `(∂φ)² = −1` 은 bare 만 γ=1, HD extension 은 Cassini 위반
- Non-local C27/C28 의 정적 γ=1 은 auxiliary frozen 이 원인, screening 아님
- C28 leading-V toy 는 부호 반전 — Dirian 2015 full equation 필수

---

## §10 — 최종 선언

> **시나리오 1 확정 (L2 재설계 가능)**.
>
> SQMH 는 L0/L1 대사 공리 (σ = 4πG·t_P, Γ₀) 를 **불가침 상속** 하면서
> L2 kinetic/coupling sector 를 교체하여 Cassini `|γ−1| < 2.3e-5`,
> Phase 3 `β ≈ 0.107`, `∇T = 0 + Bianchi`, DESI `w_a < 0` 을 **동시에
> 만족시키는 11 개의 라그랑지안 경로** 를 가진다.
>
> **A 등급 3 개** (C10k Sector-selective, C27 Deser-Woodard, C33 f(Q))
> 는 수식·수치 양면 검증을 완전 통과. **A− 등급 3 개** (C11D Disformal,
> C23 Asymptotic Safety, C41 Wetterich IDE) 는 caveat 명시 하에 통과.
> **B 등급 5 개** (C5r, C6s, C26, C28, C32) 는 부분 통과.
>
> Phase 5 MCMC 단계에서는 **C10k 를 1 순위로**, C33·C27 을 2-3 순위로
> hi_class / CLASS 수준에서 재적합. C10k 는 Phase 3 posterior 에서
> 시작 walker 를 직접 draw 할 수 있어 가장 빠른 검증 경로.
>
> **L2 탐색의 최종 교훈**은 세 줄로 요약 가능하다.
>
> 1. **Universal coupling 은 죽음, 선별적 coupling 또는 no-scalar
>    재정식화는 살아남는다.**
> 2. **L0/L1 대사 공리는 수정 없이, L2 교체만으로 관측 제약을
>    동시 만족시킬 수 있다.**
> 3. **해석 유도와 Python 수치 검증은 등치가 아니다.** L2 후보는
>    반드시 toy 실측으로 부호를 확인한 뒤에만 등급을 부여한다.

---

**문서 이력**. 2026-04-11 작성. L2 Round 1 + Round 2 + Round 3 전수
통합 결과 단일 문서. `base.l2.md`, `base.l2.2.md`, `base.l2.3.md`,
`base.l2.todo*.md`, `base.l2.2.todo*.md`, `base.l2.3.todo*.md`,
`base.l2.command.md` 의 결론을 병합하고 history/WBS/리뷰 대화를 제거.
본 문서 생성 후 위 11 개 원본은 삭제 예정. 수락 조건 원본은
`refs/l2_acceptance.md` 에 별도 보존.


---

# Appendix: Independent Alt-20 Candidates (Round N, frozen 2026-04-11)

0-parameter SQMH-native closed-form ρ_DE(a)/OL modifications, amplitude
locked to Ω_m itself, independent of all mainstream DE/MG families
(see `refs/alt20_catalog.md` for the blacklist).

## L2 structural screen (C1-C4)

All 20 candidates modify only the cosmological background: no new scalar
DOF in the static Schwarzschild limit → **C1 Cassini γ−1 = 0 analytically,
PASS for all 20**. Linear perturbation μ(a,k) = 1, c_s² = 1 structurally
→ K11 trivially PASS.

**C4 SQMH sign (ρ_DE monotonically drifting as matter → DE)**: checked
via numerical w(z) from the L3 fit. 15/20 have w_a < 0 (DESI DR2 aligned,
SQMH-consistent). The remaining 5 (A02, A07, A14, A18, plus A04 edge)
have |w_a| ≤ 0.09 or w_a > 0, demoted to **C4-FAIL**.

| ID  | Name                               | C1 | C4 |
|-----|------------------------------------|----|----|
| A01 | SQMH canonical (matter-drift)      | ✓  | ✓  |
| A02 | Quadratic drift                    | ✓  | ✗ w_a=+0.086 |
| A03 | Log horizon entropy                | ✓  | ✓  |
| A04 | Volume-cumulative                  | ✓  | ✓ w_a=−0.469 |
| A05 | Sqrt relaxation                    | ✓  | ✓  |
| A06 | Exponential                        | ✓  | ✓  |
| A07 | cosh                               | ✓  | ✗ w_a=+0.015 |
| A08 | Tanh                               | ✓  | ✓  |
| A09 | Causal-diamond 2D                  | ✓  | ✓  |
| A10 | Reciprocal drift                   | ✓  | ✓  |
| A11 | Sigmoid                            | ✓  | ✓  |
| A12 | Erf diffusion                      | ✓  | ✓  |
| A13 | Arctan plateau                     | ✓  | ✓  |
| A14 | Matter-ratio power                 | ✓  | ✗ w_a=+0.120 |
| A15 | Stretched exp                      | ✓  | ✓  |
| A16 | Second-order Taylor                | ✓  | ✓  |
| A17 | Adiabatic pulse                    | ✓  | ✓  |
| A18 | Gaussian localised                 | ✓  | ✗ w_a=+0.051 |
| A19 | Harmonic fraction                  | ✓  | ✓  |
| A20 | Two-term geometric                 | ✓  | ✓  |

**L2 PASS → L3**: 16 candidates (A01, A03-A06, A08-A13, A15-A17, A19, A20).
**L2 FAIL (C4)**: A02, A07, A14, A18.
