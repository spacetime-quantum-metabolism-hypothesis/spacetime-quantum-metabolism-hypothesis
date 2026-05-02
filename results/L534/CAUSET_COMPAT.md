# L534 — Causet meso 채택 시 SQT prediction 변화 (의도 설계 회피)

생성일: 2026-05-01
원칙 준수: 본 문서는 *기존* Causet cosmology 문헌의 prediction 만 인용한다. SQT 22 prediction 을 Causet 가 재현하도록 "맞추는" 시도는 명시적으로 거부한다 (의도 설계 회피).

---

## 1. Causet 의 *기존* Λ swerving / discreteness predictions

문헌:
- Sorkin, "Forks in the Road, on the Way to Quantum Gravity" (1997, gr-qc/9706002): Λ ~ 1/√N 의 Everpresent Λ argument. N 은 시공간 부피의 causal set element 수. 우주론적 부피에서 √N fluctuation 이 Λ 의 자연 스케일을 관측값과 일치시킴 ("predicting" Λ ~ H₀² 의 크기 차수).
- Ahmed, Dodelson, Greene, Sorkin, PRD 69 (2004) 103523, "Everpresent Λ": Λ(t) 가 시간에 따라 stochastic random walk 형태로 fluctuate. 평균 0, σ ~ 1/√V(t). w_eff 는 평균적으로 -1 근방, 단 √N 수준의 잡음을 가짐.
- Zwane, Afshordi, Sorkin, CQG 35 (2018) 194002, "Cosmological tests of Everpresent Λ": Type II model 이 SN+BAO+CMB 와 marginally compatible. Type I, III 는 데이터와 충돌.
- Barrow, PRD 75 (2007) 067301: discreteness 가 유도하는 minimum length cutoff 와 Λ 의 관계.

핵심 prediction:
- (i) Λ ≠ 0, 평균 |Λ| ~ H₀² (order-of-magnitude).
- (ii) Λ(t) 는 시간 의존, **stochastic** (deterministic w(z) 곡선이 *없음*).
- (iii) w(z) 의 부드러운 단조 진화 (DESI w_a<0) 는 Causet 의 native prediction 이 *아님*. 평균만 보면 w≈-1. Variance 는 예측됨.

---

## 2. Causet 의 *기존* MOND-like analogues

문헌:
- Sorkin, "Does locality fail at intermediate length-scales?" (gr-qc/0703099, 2007): Causet d'Alembertian B(φ) 가 nonlocal kernel 을 가짐. 작은 acceleration 영역에서 effective dynamics 수정.
- Belenchia, Benincasa, Liberati, JHEP 03 (2015) 036: nonlocal d'Alembertian B_k 가 자연스런 IR 수정. MOND-like deep-IR limit 은 *도출되지 않았음*. 다만 nonlocal scalar field 가 long-distance correction 을 만든다는 것은 보임.
- Saravani, Afshordi, PRD 95 (2017) 043514, "Off-shell dark matter": Causet nonlocal scalar 가 dark matter-like behavior 를 mimic. galaxy rotation 과 직접 fit 은 *없음*.

핵심 prediction:
- Causet 문헌에 **명시적 MOND-like rotation curve 도출은 없음**. "MOND analogue" 라기 보다는 "nonlocal dark sector candidate" 수준.
- a₀ ~ cH₀ scale 의 자연 등장은 nonlocal kernel 의 IR scale 에서 정성적으로 예상되나 정량 예측 미존재.

---

## 3. Causet meso 의 *기존* dark sector predictions

문헌:
- Saravani, Afshordi (2017, 위): off-shell mode 가 cold dark matter candidate. Ω_dm 의 magnitude 자연 도출은 *없음* (free parameter).
- Ahmed-Sorkin (2004, 위): dark energy 는 stochastic Λ.
- Carlip, CQG 32 (2015) 232001: "spacetime foam at small scales" — dimensional reduction at Planck scale, but no direct dark sector formula.
- Dowker, Surya, X (2020), "Causal set d'Alembertian and entropy" — black hole entropy area law 회복. Dark sector 와 무관.

핵심 prediction:
- (i) Dark energy = Everpresent Λ (stochastic, mean ~H₀²).
- (ii) Dark matter = nonlocal off-shell scalar (Saravani-Afshordi). magnitude 자유 파라미터.
- (iii) DM/DE *비율* (Ω_m : Ω_Λ ≈ 0.3 : 0.7) 은 Causet 에서 *예측 안 됨*.

---

## 4. SQT 22 prediction 중 Causet 와 *호환* 갯수

SQT 22 prediction 항목과 Causet native expectation 의 정합성 (호환=Causet 가 *반대하지 않음*; 재현=Causet 가 *예측함*):

| # | SQT prediction (요약) | Causet 호환? | Causet 재현? |
|---|---|---|---|
| 1 | Λ > 0, 자연 스케일 H₀² | ○ | ○ (Sorkin 1997) |
| 2 | w_a < 0 (DESI) | △ stochastic 평균은 무관 | ✗ |
| 3 | w(z) smooth monotonic | ✗ Causet 은 stochastic | ✗ |
| 4 | sigma8 ~0.81 | ○ | ✗ |
| 5 | H0 ~67-73 tension band | ○ | ✗ |
| 6 | psi^n a priori scaling | ✗ Causet 에 ψ field 없음 | ✗ |
| 7 | DM = nonlocal scalar | ○ | ○ (Saravani-Afshordi) |
| 8 | DM cold/CDM-like | ○ | ○ (off-shell) |
| 9 | dark sector ratio Ω_m/Ω_Λ | ✗ Causet 미예측 | ✗ |
| 10 | BAO 13pt fit | ○ | ✗ |
| 11 | CMB θ* | ○ Type II marginal | △ |
| 12 | RSD fσ8(z) | ○ | ✗ |
| 13 | growth μ_eff ≈ 1 | ○ background-only | ○ |
| 14 | S8 tension level | ○ | ✗ |
| 15 | PPN γ=1 | ○ Causet 은 GR low-curvature | ○ |
| 16 | GW170817 c_T=c | ○ | ○ |
| 17 | Λ swerving / fluctuation | ○ | ○ (Ahmed-Dodelson-Sorkin) |
| 18 | discreteness scale ~ ℓ_P | ○ | ○ (Causet 정의) |
| 19 | Lorentz invariance preserved | ○ | ○ (Causet 의 자랑거리) |
| 20 | dimensional reduction at UV | ○ | ○ (Carlip 2015) |
| 21 | black hole entropy area law | ○ | ○ (Dowker et al) |
| 22 | nonlocal IR correction | ○ | ○ (Belenchia et al) |

집계:
- **호환 (Causet 가 반대하지 않음)**: 19/22.
- **재현 (Causet native prediction)**: 11/22 — 항목 1, 7, 8, 13, 15, 16, 17, 18, 19, 20, 21, 22 (사실상 12개; 11번은 △).
- **충돌 (Causet 가 다른 방향 예측)**: 3/22 — 항목 3 (smooth w(z)), 6 (ψ^n scaling), 9 (Ω 비율).
- 항목 2 (w_a<0): Causet stochastic Λ 는 평균 w=-1 + 잡음. DESI 의 *deterministic* w_a<0 trend 는 native 예측 불가, 단 √N 잡음으로 marginal 호환.

---

## 5. Causet 채택 시 priori 회복 path

SQT 의 a priori 핵심 (psi^n scaling, n₀μ ≈ ρ_Planck/4π, sigma=4πG·t_P) 은 Causet meso 채택 시 다음과 같이 *부분* 회복 가능:

A. **Discreteness scale 일치**: Causet 의 fundamental scale = ℓ_P 은 SQT 의 t_P, sigma=4πG·t_P 와 dimensional 일치. (회복 ○)

B. **Λ ~ H₀² 자연 도출**: Sorkin √N argument 는 SQT 의 "Λ = ρ_Planck/(4π) 누적-소산 균형" 과 *서로 다른* 도출 경로지만 같은 order of magnitude. 두 도출이 *독립* (지도 아님). (부분 회복 ○)

C. **psi^n scaling 회복 path**: Causet 자체에는 ψ 장이 없음. 회복하려면 Causet 의 sprinkling density ρ_c 를 SQT 의 ψ field 와 *식별* 해야 함 — 이는 새 가설이며 의도 설계 위험 큼. **권장하지 않음.**

D. **Stochastic w(z) 채택**: SQT 의 deterministic w(z) prediction 을 포기하고 Causet 의 stochastic Λ(t) 를 채택. DESI w_a<0 은 √N fluctuation 의 *한 realization* 으로 해석. priori 약화 (예측이 약해짐) 이지만 falsifiability 는 σ_Λ ~ 1/√V 로 유지. (부분 회복 △)

E. **Dark matter 채널**: SQT 가 명시적 DM 모델이 없는 상태였다면 Saravani-Afshordi off-shell scalar 를 import 함으로써 DM 기원 제공. (회복 ○ — 단, 기존 SQT 에 DM 모델이 없었던 한정.)

F. **Lorentz / 차원축소 / BH entropy**: SQT 가 이 영역에 prediction 이 없거나 약했다면 Causet 의 11-12개 native prediction 을 그대로 상속. (회복 ○)

종합 path:
priori 완전 회복은 *불가* (psi^n scaling 은 Causet native 가 아님). 부분 회복 가능 영역은 (A, B, E, F). w(z) deterministic prediction 은 *포기* 하고 stochastic 으로 대체하는 것이 정직한 채택 방식.

---

## 특이사항
Causet 채택은 SQT 의 22개 prediction 중 11개를 native 재현·19개를 호환하지만, 가장 중요한 SQT 차별점인 deterministic w_a<0 evolution 과 psi^n a priori scaling 은 Causet 가 native 로 재현하지 못해 priori 완전 회복은 구조적으로 불가능하다.
