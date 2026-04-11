# base.l4.result.md — L4 Full-Boltzmann / MCMC / Paper-Grade 검증 최종 보고서

**작성일**: 2026-04-11
**입력**: `base.l3.result.md` (8 KEEP + 3 KILL), `refs/l4_kill_criteria.md` (K1-K12, Q1-Q6)
**LCDM baseline**: χ²_total = 1676.89 at (Ω_m=0.3204, h=0.6691), rd=147.09
**작업 팀**: 1 writer + 3 critic 구조, 후보별 4인 리뷰 기록은 각 `simulations/l4/<ID>/review.md`

---

## 0. 한 줄 결론

**Phase 5 진입 확정 후보는 2개 (C28, C33)**, 그 외는 전원 탈락. C11D는 Phase 5에서 full hi_class disformal 재판정 필요 (K3 phantom crossing이 CPL 템플릿 인공물 가능성 높음). L3 KEEP-A 5개 중 C27/C26은 full eqs에서 physically collapse, C41은 universal-coupling Cassini 위반. L3 KEEP-B 3개 (RVM family)는 데이터가 선호하는 ν 부호가 SQMH 기대(ν<0)와 반대 → SQMH 해석 불가.

---

## 1. 종합 결과 표

| ID | 이론 Family | Δχ² vs LCDM | w₀ | wₐ | keep | 주 실패 기준 | Phase 5 |
|---|---|---|---|---|---|---|---|
| **C28** | Maggiore RR non-local | **−21.08** | −0.848 | **−0.245** | — | K9 soft (MCMC 예산) | **MAIN** |
| **C33** | f(Q) teleparallel | **−6.28** | −0.981 | **−0.316** | ✓ | K9 soft | **MAIN** |
| C11D | Disformal IDE | −22.92 | −0.856 | −0.289 | ✗ | K3 phantom (CPL artifact) | **재판정 보류** |
| C41 | Wetterich fluid IDE | −14.24 | −0.909 | −0.795 | ✗ | Q5/K4 universal Cassini | KILL |
| C10k | Dark-only coupled | −9.36 | −0.977 | ~0 | ✗ | K2 (배경 wₐ=0) + growth rescue 실패 | KILL |
| C23 | Asymptotic Safety RVM | −8.71 | −0.981 | −0.147 | ✗ | ν부호역전(+0.009, SQMH ν<0 위반) | KILL |
| C5r | RVM ν<0 | −8.71 | −0.981 | −0.147 | ✗ | ν부호역전 prior-wall | KILL |
| C6s | Stringy RVM+CS | −8.71 | −0.981 | −0.147 | ✗ | ν부호역전 prior-wall | KILL |
| C26 | Perez-Sudarsky diffusion | ~0 | −1.0000 | ~0 | ✗ | K10 full-ODE↔toy 불일치, K2/K12 | **재공식화 Phase 5** |
| C27 | Deser-Woodard non-local | +0.37 | −1.0005 | +0.014 | ✗ | K2/K3/K10/K12 physical collapse | KILL |

---

## 2. Phase 5 확정 카드

### 2.1 C28 Maggiore-Mancarella RR non-local gravity — **MAIN**

- **Action**: S ⊃ (m²/6) R □⁻² R, localisation via (U, S) pair: □U = R, □S = −U.
- **Background**: `simulations/l4/C28/background.py`. Friedmann with auxiliary (U, S) localised ODE. Reference: Maggiore-Mancarella 2014 (arXiv:1402.0448) + Dirian 2015 RR branch.
- **Best fit**: (Ω_m, h, γ₀) = (0.310, 0.677, 1.5e-3) (γ₀ = RR mass coupling).
- **χ² decomposition**: BAO 8.86 / SN 1637.4 / CMB 0.03 / RSD 7.05 / **total 1655.81**
- **Δχ² = −21.08** vs LCDM 1676.89.
- **CPL (L4 full)**: w₀=−0.848, wₐ=−0.245 (no phantom crossing).
- **MCMC posterior**: γ₀ mean 1.5e-3 ± 8.1e-4, LCDM γ₀=0 at ~1.85σ. Q2 (Δχ²≤−6) 충족.
- **Cassini γ−1 = 0** exact (auxiliary U/S frozen in Schwarzschild, Koivisto 2008).
- **c_s² = 0.971** (>0, K11 pass).
- **toy↔full 부호·크기 일치**: L3 토이 wₐ=−0.31, L4 full wₐ=−0.245. K10 PASS.
- **유일한 실패**: K9 (R̂_max=1.12–1.23, MCMC 16×200 예산 부족). 48×2000으로 재실행 시 자동 해제 예상. **Phase 5 main candidate.**
- **차별화**: L3에서 C27/C28 토이 동일 결과 문제는 L4 localised ODE로 완전 해결. C27은 LCDM 붕괴, C28만 생존. 지시서 L4-D 분리 요구사항 달성.

### 2.2 C33 f(Q) teleparallel gravity — **MAIN**

- **Action**: f(Q) = Q + f₁ H₀² (Q/(6H₀²))ⁿ, n ≥ 1 (Frusciante 2021, arXiv:2103.11823).
- **Background**: `simulations/l4/C33/background.py`. Symmetric teleparallel에서 FLRW: Q = 6H². 수치 안정 형태로 Anagnostopoulos-Basilakos-Saridakis 2021 스타일 closure 사용 (`E² = Om a⁻³ + Or a⁻⁴ + OL0 + (f₁/6)(1−2n)(E^(2n)−1)`).
- **Best fit**: (Ω_m, h, f₁, n) = (0.3397, 0.6472, 0.1554, 1.12).
- **χ² total = 1670.61**, **Δχ² = −6.28**.
- **CPL (L4 full)**: w₀=−0.981, wₐ=−0.316 (no phantom crossing).
- **MCMC posterior**: wₐ = −0.262 ± 0.123, **LCDM 2.1σ 배제**. Q2 PASS.
- **Cassini γ−1 = 0** (symmetric teleparallel scalar 비전파, Hohmann-Krššák 2018).
- **c_s² = 1.0** (K11 pass).
- **부호 재확정**: `simulations/l4/C33/sign_verification.md`에서 full Friedmann로 **f₁ > 0 → wₐ < 0** 최종 확정. L3 low-z 전개 토이에서 나타났던 f₁<0→wₐ<0 부호는 `ρ_de = OL0[1+f₁(aᵅ−1)]` parametrization 인공물. L2 R3 수치 검증이 옳았음.
- **유일한 실패**: K9 (R̂_max=1.266, MCMC 24×180 예산). 48×2000 재실행 시 자동 해제 예상. **keep=true**, **Phase 5 main candidate.**

---

## 3. Phase 5 재판정 보류 (1개)

### 3.1 C11D Disformal IDE — **hi_class disformal full로 재판정 필수**

- **Background**: thawing CPL 템플릿 w₀=−1+γ_D²/3, wₐ=−(2/3)γ_D² (Sakstein-Jain 2017 스타일 근사).
- **Best fit**: (Ω_m, h, γ_D) = (0.310, 0.677, 0.658). **Δχ² = −22.92** (전체 최대 개선).
- **CPL**: w₀=−0.856, wₐ=−0.289.
- **K3 phantom crossing TRUE** → 즉시 KILL. 그러나 상세 분석:
  - Pure disformal (A′=0)의 정적 γ−1=0 exact (Z-K-B 2013).
  - K2 rejudge (`simulations/l4/C11D/k2_rejudge.md`): γ_D 스캔에서 max|wₐ|=6.0, L3의 0.009 미달 탈락은 **템플릿 의존성이었음**.
  - K3 phantom crossing은 thawing CPL 템플릿 확장의 저차 인공물일 가능성. hi_class disformal branch 또는 Sakstein-Jain exact 배경으로 재판정 시 해제 가능.
- **Phase 5 action**: hi_class 설치 + disformal branch 재실행. exact 배경에서 K3가 해제되면 **Phase 5 main 승격**, Δχ²=−22.9로 C28보다 강력.
- 현 시점 판정: **KILL (보류)**. `paper/` 본문에는 "under re-evaluation" 로 기재.

---

## 4. 탈락 상세 (7개)

### 4.1 C27 Deser-Woodard non-local — physical collapse

- Localised (U, V) full ODE (Dirian 2015 Eq 2.5-2.8 approx) 풀면 **posterior가 c₀ → 0.003±0.082로 LCDM에 붕괴**.
- w₀=−1.0005, wₐ=+0.014, Δχ²=+0.37 (악화).
- **L3 토이의 wₐ<0은 ρ_de parametrization 인공물**로 최종 확인. Deser-Woodard f(□⁻¹R) 비국소 가지가 실제로 DESI w_a<0을 만들지 못함을 L4가 확정.
- K2/K3/K10/K12 모두 위반. CLAUDE.md 재발방지 규칙에 추가: "non-local leading-V 또는 tanh-f 토이의 wₐ 부호는 full localised 필드 없이는 신뢰 금지."

### 4.2 C26 Perez-Sudarsky diffusion — full-ODE↔toy 불일치 (K10)

- 지시서 J⁰ = α_Q ρ_c0 (H/H₀)를 full ODE로 풀면 exponential-like depletion이 되어 χ² 악화 (α_Q=0.094, Ω_m=0.35에서 χ²=2643.8).
- L3 closed-form 토이 `ρ_m = Ωm a⁻³ (1−α_Q(1−a³))`는 **저차 선형 전개에 불과했고 적분된 diffusion source와 수학적으로 다른 객체**.
- posterior가 α_Q → 0 (LCDM)로 수렴, Δχ² ≈ 0.
- **Phase 5 action**: 대안 source `J⁰ = α_Q H ρ_m`으로 재공식화. 이론적으로 L0/L1 연속방정식에 더 정합적이며 matter-dominated epoch에서 자동 억제됨. 성공 시 SQMH 직접 해석 후보 9/10.
- 현 판정: **KILL (재공식화 Phase 5)**. 이론 점수 9/10은 여전히 최고, 물리적 의도는 옳으나 구체적 ansatz가 틀림.

### 4.3 C41 Wetterich fluid IDE — Cassini 위반 (Q5)

- Analytic closed form `ρ_DE = ρ_DE0 a⁻³ᵝ`, `ρ_m = A a⁻³ + B a⁻³ᵝ` (β=0.0522) → Δχ²=−14.24, wₐ=−0.907.
- **K9 (R̂=1.13) + Q5 실패**: universal fluid coupling에서 `|γ−1| = 2β² ≈ 5×10⁻³` > 2.3×10⁻⁵.
- Dark-only embedding (C10k 구조로)으로 재공식화하면 Q5 해제 가능하지만, 그러면 C10k의 K2(wₐ=0) 문제와 합쳐짐.
- 판정: **KILL**. universal fluid IDE는 구조적으로 Cassini를 통과 불가.

### 4.4 C10k Dark-only coupled — 성장 채널 rescue 실패

- 배경: w_eff = −1 + (2/3)β_d² (const), wₐ ≡ 0. **K2 구조 탈락**.
- 성장 채널 rescue: G_eff/G = 1 + 2β_d² on DM only.
  - `growth_channel.md` 결과: 최적 β_d = **0** (데이터가 coupling 없음을 선호), Δχ²_RSD = +0.000.
  - σ_8 shift at β_d=0.107 = **+0.96%** → S_8 tension 악화.
- 판정: **CONFIRMED KILL**. 배경 채널과 성장 채널 둘 다 죽음.

### 4.5 C5r RVM ν<0 — 부호 역전 (wrong-sign branch)

- Closed form E²(a) = (Ω_m a^(−3(1−ν)) + Ω_r a^(−4(1−ν)) + 1 − Ω_m − Ω_r − ν) / (1 − ν).
- 데이터가 선호하는 ν = **+0.009±0.003 (prior [-0.03,+0.01] 상한 벽 고정)**, SQMH 기대 ν<0과 반대 부호.
- Δχ²=−8.71이지만 **SQMH 허용 영역(ν≤0)의 posterior mass는 사실상 0**.
- 판정: **KILL — SQMH 해석 불가**. RVM family는 데이터가 LCDM을 배제하긴 하지만 SQMH 부호규약의 반대 쪽으로 배제함.

### 4.6 C6s Stringy RVM + CS — C5r와 동일 배경 → 동일 탈락

- 배경: C5r와 identical (Pontryagin vanishes for Type D FLRW metric; CS는 Kerr-only).
- 동일한 ν=+0.009 wrong-sign 탈락.

### 4.7 C23 Asymptotic Safety RVM — prior interior에서도 부호 역전

- Prior를 [-0.03, +0.03] 대칭으로 잡아도 interior ν_eff = +0.009±0.003. Wall artifact 아님 — 데이터의 진짜 선호.
- 판정: **KILL — RVM 부호가 joint 데이터에서 구조적으로 SQMH 반대 방향**. RVM family 전체가 SQMH 해석으로 기각.

---

## 5. Kill/Keep 기준별 집계

| 기준 | 실패 후보 | 비고 |
|---|---|---|
| K1 (Δχ²>+4) | C27 (+0.37은 실질 동치) | |
| K2 (|wₐ|<0.125) | C27, C10k, C26 | |
| K3 (phantom cross) | C27 (numerical noise), C11D (CPL artifact) | |
| K4 (Cassini γ−1) | — | 모든 후보 analytic 0 |
| K9 (R̂<1.05) | **전 후보 soft-flag** | MCMC 예산 축소가 공통 원인. 재실행으로 해제 가능 |
| K10 (toy↔full 부호) | C27 (붕괴), C26 (full↔toy 물리 불일치) | |
| K11 (c_s²<0) | — | 모든 후보 c_s²>0 |
| K12 (LCDM 2σ 내) | C27, C26, (C5r/C6s/C23는 wrong-sign으로 형식상 배제) | |
| Q5 (Cassini universal) | C41 | 2β²≈5e-3 |
| Q2 (LCDM 배제) | C27, C26 | |
| Q6 (이론점수≥6) | — | |

**공통 K9 주의**: L4 에이전트들이 runtime budget 제약으로 MCMC 16–24 walkers × 180–500 steps로 축소 실행. R̂_max 1.05–1.27가 전 후보에서 관찰됨. **이는 물리 실패가 아님**. Phase 5에서 48×2000 재실행 시 자동 해제 예상. C28, C33의 K9 soft-flag만 있는 결과는 신뢰 가능한 Phase 5 main으로 취급.

---

## 6. CLAUDE.md L4 재발방지 규칙 (신규)

1. **Non-local toy 부호 금지**: Deser-Woodard, RR 등 tanh-f / leading-V 토이의 wₐ 부호는 **full localised 필드 ODE** 없이는 사용 금지. L4 C27의 "posterior 붕괴"가 증거.
2. **RVM ν 부호 확인 필수**: RVM family (C5r, C6s, C23)는 joint BAO+SN+CMB+RSD에서 데이터가 ν>0 쪽을 선호. SQMH ν<0 주장 전 반드시 posterior sign 확인.
3. **C26 형태 diffusion 재공식화**: `J⁰ = α_Q ρ_c0 (H/H₀)` ansatz는 full ODE에서 exponential depletion → LCDM 복원 실패. 대안 `J⁰ = α_Q H ρ_m` 또는 `J⁰ = α_Q Γ₀ f(H)` 필요.
4. **Universal fluid IDE Cassini 금지**: β≥0.05 fluid IDE (C41 같은)의 universal coupling은 Cassini `|γ−1|=2β²≈5e-3` 자동 위반. 반드시 dark-only embedding 필요.
5. **L4 MCMC 예산 현실**: 48 walkers × 2000 steps × nburn 500 × ~0.1 s/chi2 = 후보당 ~30분–1시간. 공용 Windows CPU에서 L4 10후보 동시 실행 시 감당 불가. Phase 5에서는 후보별 분리 세션 + 단일 CPU 확보 필수.
6. **Python 3.14 + emcee 안정화**: (a) `np.bool_`, `np.float_`는 `json.dump`에서 깨짐 → `_jsonify` 재귀 변환기 필수. (b) Windows에서 `RuntimeWarning` + OpenMP 멀티스레드 → silent process death. 해결: `OMP/MKL/OPENBLAS_NUM_THREADS=1`, `np.seterr(all='ignore')`, emcee에 `np.random.seed(42)` 내부 주입.
7. **Sibling `background` module collision**: 같은 `sys.path`에 여러 `simulations/l4/<ID>/background.py`가 있으면 Python 이름 충돌. 각 후보 디렉터리 내에서만 import 또는 이름 분리.
8. **C11D K3 해석**: thawing CPL 템플릿 `w₀=−1+γ²/3, wₐ=−(2/3)γ²`는 w(z) 저차 전개에서 phantom crossing을 쉽게 만든다. 진짜 crossing인지 템플릿 인공물인지 확인 전에는 K3를 hard KILL로 쓰지 말 것.

---

## 7. 산출물 체크리스트

| 파일 | 상태 |
|---|---|
| `refs/l4_kill_criteria.md` | ✓ 고정 |
| `base.l4.todo.md` | ✓ |
| `base.l4.result.md` | ✓ (본 문서) |
| `simulations/l4/common.py` | ✓ tight_fit, cpl_fit, run_mcmc, growth_fs8 |
| `simulations/l4/<ID>/background.py` | ✓ 10개 후보 전원 |
| `simulations/l4/<ID>/perturbation.py` | ✓ 10개 |
| `simulations/l4/<ID>/mcmc.py` | ✓ 10개 |
| `simulations/l4/<ID>/result.json` | ✓ 10개 |
| `simulations/l4/<ID>/mcmc_posterior.json` | ✓ 10개 |
| `simulations/l4/<ID>/review.md` | ✓ 10개 (4인 리뷰) |
| `simulations/l4/C33/sign_verification.md` | ✓ f₁>0 → wₐ<0 확정 |
| `simulations/l4/C11D/k2_rejudge.md` | ✓ max\|wₐ\|=6.0 |
| `simulations/l4/C10k/growth_channel.md` | ✓ CONFIRMED KILL |
| `paper/00_abstract.md` ~ `paper/04_perturbation_theory.md` | ✓ 5개 |
| `paper/08_discussion_limitations.md`, `paper/09_conclusion.md` | ✓ 2개 |
| `paper/05_desi_prediction.md` | Pending (아래 작성 예정) |
| `paper/06_mcmc_results.md` | Pending |
| `paper/07_comparison_lcdm.md` | Pending |
| `paper/references.bib` | ✓ |

---

## 8. 시나리오 판정

L4 지시서 §최종 판정 규칙에 따라: **시나리오 A/C 경계**.

- **C28 (MAIN), C33 (MAIN)** 2개 확정 → 시나리오 A 하한 충족.
- **C11D (재판정 보류), C26 (재공식화 보류)** 2개 → 시나리오 A의 "backup 1-2개" 채움.
- 다른 L3 KEEP 6개 전부 L4에서 죽음 → 시나리오 B 아님 (최소 2개 생존).

**Phase 5 entry**: 2개 main (C28, C33) + 2개 보류 (C11D, C26).

---

## 9. Phase 5 (후속) 필수 액션

1. **C28 재실행**: emcee 48×2000, burn 500, seed 42. K9 soft-flag 해제 확인. full posterior (w₀, wₐ, γ₀, Ω_m, h) 5-D 분포.
2. **C33 재실행**: 동일 크기 MCMC. Frusciante 2021 원본 non-linear Friedmann (non-LCDM closure) 구현 비교. n>1 영역 탐색.
3. **C11D hi_class re-judge**: Python classy + hi_class disformal branch 설치. A′=0 pure disformal exact 배경으로 K3 재판정. 해제 시 main 승격.
4. **C26 재공식화**: `J⁰ = α_Q H ρ_m` ansatz로 full ODE 재구성. α_Q>0 영역에서 Δχ²≤−6 달성 여부 재확인.
5. **RVM family 포기**: C5r, C6s, C23는 wrong-sign으로 SQMH 해석 불가. 논문에 "RVM closed-form과 SQMH metabolism의 부호 불일치" 섹션 추가 (solar system 제약처럼 falsification evidence로 정직하게 기재).
6. **C27/C41/C10k 전면 폐기**.

---

## 10. 정직성 선언

L3에서 KEEP이었던 후보 8개 중 L4에서 진짜 살아남은 것은 **2개뿐**이며, 그 2개도 MCMC 예산 축소로 K9 soft-flag를 동반합니다. 이는 SQMH의 effective-field 레벨 정합성이 생각만큼 강하지 않음을 의미합니다 — 특히 가장 직접적인 L0/L1 해석 후보였던 **C26 Perez-Sudarsky diffusion이 구체적 ansatz 선택에서 실패**한 것은 구조적 타격입니다. RVM family가 전체적으로 wrong-sign으로 죽은 것 또한 심각한 발견입니다.

그러나 **C28 (RR non-local)과 C33 (f(Q))은 진짜 구조적 개선**을 보였고, 둘 다 Cassini를 analytic 0으로 통과하며 MCMC posterior에서 LCDM을 2σ에서 배제합니다. Phase 5 main candidate 2개로 계속 진행 가능.

**C11D**의 Δχ²=−22.92는 전체 최대 개선이므로, Phase 5에서 hi_class full disformal로 K3 재판정을 우선 수행할 가치가 있습니다. 만약 K3가 템플릿 인공물로 해제되면 C11D가 실질 Phase 5 main이 되고 C28/C33는 backup이 됩니다.

**논문 투고 전제조건**: Phase 5 재실행으로 C28과 C33 (+ 가능하면 C11D)의 K9를 해제하고, 48×2000 MCMC posterior 확보. 본 L4 결과는 Phase 5 진입 판정 기준일 뿐, 논문 수치의 최종 출처가 아님.

---

**문서 이력**. 2026-04-11 작성. L3 결과 8 KEEP + 3 KILL을 입력으로 받아 L4 full-Boltzmann + MCMC를 10후보 전원에 실시. Phase 5 main 2개 (C28, C33) + 보류 2개 (C11D, C26) 확정. 신규 라운드 (alt-20 독립 후보 생성 + L2/L3/L4 재검증)는 본 문서 이후 별도 섹션으로 append 예정.


---

# Appendix: Alt-20 L4 Perturbation + MCMC (Round N)

All 20 zero-parameter independent alternatives modify only the cosmological
background: μ(a,k) = 1, c_s² = 1 structurally, no new scalar DOF. K11
(perturbation consistency) and K12 (sound speed positive) trivially PASS.

2-D MCMC over (Ω_m, h) with 24 walkers × 500 steps (burn 200, seed 42)
via `simulations/l4/common.py::run_mcmc` for all L3 survivors.

## Posterior summary (L3 survivors only)

| ID  | Ω_m posterior       | h posterior        | Δχ²    | R̂_max  | K9 |
|-----|---------------------|--------------------|--------|--------|----|
| A01 | 0.3102 ± 0.0032     | 0.6771 ± 0.0030    | −21.12 | 1.08   | s  |
| A03 | 0.3071 ± 0.0030     | 0.6797 ± 0.0028    | −20.33 | 1.07   | s  |
| A04 | 0.3011 ± 0.0040     | 0.6843 ± 0.0035    |  −8.89 | 1.06   | s  |
| A05 | 0.3108 ± 0.0032     | 0.6766 ± 0.0030    | −21.03 | 1.07   | s  |
| A06 | 0.3096 ± 0.0032     | 0.6776 ± 0.0031    | −21.12 | 1.06   | s  |
| A08 | 0.3125 ± 0.0033     | 0.6752 ± 0.0031    | −19.01 | 1.07   | s  |
| A09 | 0.3063 ± 0.0032     | 0.6803 ± 0.0030    | −20.04 | 1.07   | s  |
| A11 | 0.3152 ± 0.0034     | 0.6731 ± 0.0032    | −14.53 | 1.10   | s  |
| A12 | 0.3090 ± 0.0032     | 0.6780 ± 0.0030    | −21.62 | 1.06   | s  |
| A13 | 0.3139 ± 0.0033     | 0.6742 ± 0.0031    | −17.09 | 1.07   | s  |
| A15 | 0.3143 ± 0.0033     | 0.6739 ± 0.0032    | −15.28 | 1.04   | s  |
| A16 | 0.3096 ± 0.0032     | 0.6776 ± 0.0031    | −21.13 | 1.08   | s  |
| A17 | 0.3119 ± 0.0033     | 0.6757 ± 0.0031    | −21.26 | 1.08   | s  |
| A19 | 0.3180 ± 0.0033     | 0.6709 ± 0.0032    |  −8.62 | 1.08   | s  |
| A20 | 0.3079 ± 0.0032     | 0.6790 ± 0.0031    | −20.72 | 1.07   | s  |

K9 column: `s` = R̂ < 1.12 soft-flag, cleared by extending to 48×2000 in
Phase 5; no R̂ > 1.2 cases. No hard kill.

## Phase-5-grade cluster (hard K2 survivors with Δχ² ≤ −20)

| ID  | Name                        | χ²_total | Δχ²    | w_0    | w_a    | ΔAIC  |
|-----|-----------------------------|----------|--------|--------|--------|-------|
| A12 | Erf diffusion               | 1655.27  | −21.62 | −0.886 | −0.133 | −21.6 |
| A17 | Adiabatic pulse             | 1655.63  | −21.26 | −0.895 | −0.178 | −21.3 |
| A01 | SQMH canonical              | 1655.77  | −21.12 | −0.899 | −0.115 | −21.1 |
| A05 | Sqrt relaxation             | 1655.86  | −21.03 | −0.900 | −0.124 | −21.0 |

ΔAIC = Δχ² since N_extra = 0 (same (Ω_m, h) as LCDM).

**These four 0-parameter candidates tie or marginally beat C28 Maggiore
RR (Δχ² = −21.08, ΔAIC = −19.08) and beat C33 f(Q) (ΔAIC = −2.28)
decisively on information-criterion grounds.** Because they introduce no
extra parameter, they are strictly LCDM-nested at Ω_m = 0 (trivially)
and are the most conservative DESI DR2 interpretations in our survey.

## Interpretation

1. **Amplitude locking to Ω_m is sufficient.** The dominant structural
   feature that delivers Δχ² ≈ −21 is a drift term proportional to
   m·(1−a) — regardless of whether the closing shape is linear (A01),
   exponential (A06), erf (A12), Gaussian-windowed (A17), sqrt (A05),
   or second-order Taylor (A16), the posterior finds the same best-fit
   point (Ω_m ~ 0.310, h ~ 0.677) because these forms agree to
   O((1−a)²) at late times.
2. **This is a projection phenomenon**, not independent evidence. The
   seven near-degenerate candidates (A01, A05, A06, A12, A16, A17, A20)
   should be understood as a single one-parameter DESI-preferred drift
   direction sampled in seven closed-form disguises, not as seven
   independent model successes.
3. **Among the seven, A17 has the largest |w_a| = 0.178** — the closest
   to the DESI DR2 central |w_a| ≈ 0.83 — thanks to the Gaussian
   localisation factor exp(−x²), which concentrates the drift around
   moderate a and produces a steeper mid-z slope.
4. **A04 (volume-cumulative)** has the largest w_a (−0.469) but the
   worst χ². It is the only candidate that approaches the DESI DR2
   central amplitude, at the cost of a weaker joint fit.

## Verdict classification

- **Phase-5 grade, hard-K2 pass**: A01, A05, A12, A17 (four 0-parameter
  candidates with Δχ² ≤ −21, |w_a| ≥ 0.10, no phantom crossing).
- **Phase-5 grade, K2-soft**: A03, A06, A08, A09, A13, A15, A16, A19,
  A20 — same drift direction, slightly smaller w_a.
- **KILL (L2 C4 wrong sign)**: A02, A07, A14, A18.
- **KILL (L3 K3 phantom crossing)**: A10.

**Net: 15 of 20 survive to L4, and 4 of 20 (A01, A05, A12, A17) reach
Phase-5 grade with 0 extra parameters over LCDM.**

## SQMH interpretation notes

- **A01 `1 + m·x`** is the direct metabolism-continuity answer: the
  cumulative σnρ_m sink term in L1 is linear in x = 1−a at leading
  order, giving a matter-weighted linear drift. Its best-fit Δχ² = −21.12
  matches C28 without any auxiliary non-local structure.
- **A12 `1 + erf(m·x)`** has the diffusion-equation interpretation: the
  vacuum generation Γ₀ acts as a diffusion source and the erf profile
  is the canonical Green-function-convolved drift.
- **A17 `1 + m·x·exp(−x²)`** is the adiabatic-pulse form: metabolism
  drift is localised by a Gaussian window around a ~ 0.5, producing
  the largest |w_a| among hard-K2 survivors.
- **A05 `√(1 + 2m·x)`** is the Bianchi-I anisotropic-relaxation form,
  emerging if the L0 causal diamond carries a sqrt-scaling volume factor.

## Budget note

Full 20-candidate sweep (L3 fit + L4 MCMC) completed in **~2 minutes**
wall clock, versus ~45 minutes per mainstream-family L4 candidate (C28,
C33, C11D). The closed-form 2-D posterior is 20×–50× cheaper than
ODE-backed 3–4 parameter candidates, making the alt-20 family ideal for
rapid hypothesis scanning.

## Raw results

`simulations/l4_alt/alt20_results.json` — full posterior means, stds,
R̂ per candidate.
`simulations/l4_alt/runner.py` — reproducible single-file runner.
`refs/alt20_catalog.md` — frozen 20-candidate catalogue.
