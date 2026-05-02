# SQMH Notation / 기호 표기

영문/한국어 병기. 본 문서는 SQMH 논문에서 사용하는 핵심 기호의 정의와 단위를
통일한다. CLAUDE.md의 SI 규약과 일관(특히 σ = 4πG·t_P, n₀μ = ρ_Planck/(4π)).

---

## 1. Fundamental SQMH symbols / 기본 SQMH 기호

### σ₀  (sigma_0, creation cross-section / 생성 단면)
- **EN**: SQMH spacetime-quantum creation rate per unit volume per unit
  source. SI: σ₀ = 4πG·t_P  [m³ kg⁻¹ s⁻¹]. The Planck-unit shorthand
  σ = 4πG is reserved for natural units only.
- **KO**: 단위 부피·단위 원천당 시공간 양자 생성률. SI 단위로 σ₀ = 4πG·t_P
  [m³ kg⁻¹ s⁻¹]. σ = 4πG는 플랑크 단위 전용이며 SI에서 사용 금지.

### n_∞  (n_infty, asymptotic quantum density / 점근 양자 밀도)
- **EN**: High-z saturation density of SQMH quanta. Appears in the SQT
  ratio as ψ(z→∞) ≡ ψ_∞ ∝ n_∞^{1/2}. Dimension [m⁻³].
- **KO**: 고적색편이에서의 SQMH 양자 포화 밀도. SQT 비율에서 ψ(z→∞) ≡ ψ_∞
  ∝ n_∞^{1/2}로 등장. 차원 [m⁻³].

### ε  (epsilon, metabolism efficiency / 대사 효율)
- **EN**: Dimensionless ratio of useful work to total quantum throughput.
  Used in three-regime transitions; bounded 0 ≤ ε ≤ 1.
- **KO**: 총 양자 처리량 대비 유효 일의 무차원 비율. 세 영역 전이에서 사용,
  0 ≤ ε ≤ 1.

### τ_q  (tau_q, quantum relaxation time / 양자 이완 시간)
- **EN**: Characteristic timescale of single-quantum metabolism;
  τ_q ≃ 1/Γ_0 in the long-wavelength limit. SI [s].
- **KO**: 단일 양자 대사의 특성 시간 척도. 장파장 극한에서 τ_q ≃ 1/Γ_0.
  SI [s].

### Γ_0  (Gamma_0, annihilation rate / 소멸률)
- **EN**: SQMH spacetime-quantum annihilation rate per quantum. Companion
  of σ₀; the equilibrium n₀μ = ρ_Planck/(4π) ≈ 4.1×10⁹⁵ kg m⁻³ requires
  Γ_0 · n_∞ ≃ σ₀ · ρ_source. SI [s⁻¹].
- **KO**: 양자당 소멸률. σ₀의 짝. 평형 n₀μ = ρ_Planck/(4π) ≈ 4.1×10⁹⁵ kg m⁻³
  은 Γ_0·n_∞ ≃ σ₀·ρ_source 조건을 요구. SI [s⁻¹].

### ρ_q  (rho_q, quantum mass density / 양자 질량 밀도)
- **EN**: Effective mass density carried by the SQMH quantum bath; appears
  as the "(1+f) ρ_DE" reservoir in three-regime continuity equations.
  SI [kg m⁻³].
- **KO**: SQMH 양자 욕조가 운반하는 유효 질량 밀도. 세 영역 연속방정식에서
  "(1+f) ρ_DE" 저장소로 등장. SI [kg m⁻³].

---

## 2. Effective / phenomenological symbols / 유효·현상학 기호

### μ_eff  (mu_eff, effective Newton coupling / 유효 뉴턴 결합)
- **EN**: Linear-perturbation modification G_eff/G in the Poisson equation.
  In all post-L5 SQMH winners μ_eff ≈ 1 (background-only structure;
  GW170817 c_T = c). Caution: μ_eff ≈ 1 cannot resolve the S_8 tension.
- **KO**: 푸아송 방정식의 G_eff/G 선형 섭동 수정. L5 이후 모든 우승 후보에서
  μ_eff ≈ 1(배경 한정 + GW170817). 주의: μ_eff ≈ 1은 S_8 긴장을 해결하지 못한다.

### β_eff  (beta_eff, effective dark coupling / 유효 암흑 결합)
- **EN**: Coupled-quintessence-style coupling restricted to the dark sector
  (= β_d in C10k notation). Linear growth gets G_eff/G = 1 + 2β_eff² for
  DM only. Slow-roll input φ_N ≈ √(2/3)·β_eff·Ω_m(a).
- **KO**: 암흑부문 한정 coupled-quintessence 결합(C10k 표기로 β_d). DM에만
  G_eff/G = 1 + 2β_eff² 적용. slow-roll 입력 φ_N ≈ √(2/3)·β_eff·Ω_m(a).

### Λ_UV  (Lambda_UV, ultraviolet cutoff / 자외선 절단)
- **EN**: Energy scale beyond which SQMH coarse-graining breaks down; in
  practice tied to the Planck scale (Λ_UV ≲ M_P). All EFT statements are
  valid for k ≪ Λ_UV.
- **KO**: SQMH 거친화(coarse-graining)가 깨지는 에너지 척도. 실제로는
  플랑크 스케일에 종속(Λ_UV ≲ M_P). 모든 EFT 주장은 k ≪ Λ_UV 영역 한정.

### ξ  (xi, ψ-T coupling constant / ψ-T 결합 상수)
- **EN**: Coupling in the universal-form ξ ψ T^μ_μ Lagrangian. Cassini
  forbids the universal version (FRAMEWORK-FAIL via |γ-1| > 2.3×10⁻⁵);
  surviving uses are dark-only (ξ_d) or disformal (ξ_disf).
- **KO**: 보편형 라그랑지언 ξ ψ T^μ_μ의 결합. Cassini 제약으로 보편형은
  FRAMEWORK-FAIL(|γ-1| > 2.3×10⁻⁵). 생존 사용처는 dark-only(ξ_d) 또는
  disformal(ξ_disf).

### ξ_q  (xi_q, IDE energy-flow coupling / IDE 에너지 흐름 결합)
- **EN**: Fluid-IDE coupling sign convention: ξ_q > 0 = matter→DE energy
  transfer (SQMH-consistent); ξ_q < 0 = phantom branch (forbidden).
  Always report ξ_q ≥ 0 branch separately.
- **KO**: 유체 IDE 결합 부호 규약: ξ_q > 0 = 물질→DE 에너지 이전(SQMH 정합),
  ξ_q < 0 = phantom branch(금지). ξ_q ≥ 0 branch는 항상 분리 보고.

---

## 3. Cosmological background quantities / 우주론 배경량

### E(z) ≡ H(z)/H_0
- **EN**: Dimensionless Hubble. SQMH三영역에서는 coupled ODE(odeint)로
  계산. ad hoc perturbative 근사 금지.
- **KO**: 무차원 허블. SQMH 세 영역에서는 coupled ODE(odeint) 필수, ad hoc
  근사 금지.

### ω_X  (omega_X, dimensionless density / 무차원 밀도)
- **EN**: ω_X ≡ ρ_X/ρ_crit,0. **Not** Ω_X(a). E²(z) = ω_r(1+z)⁴ + ω_m + ω_de(z)
  in IDE convention. **Never** double-count as ω_m(1+z)³.
- **KO**: ω_X ≡ ρ_X/ρ_crit,0 (오늘 임계밀도 기준). Ω_X(a)와 구분. IDE
  관례에서 E²(z) = ω_r(1+z)⁴ + ω_m + ω_de(z). ω_m(1+z)³ 이중 카운팅 금지.

### r  (ratio, ψ-saturation ratio / ψ 포화 비)
- **EN**: r ≡ ψ₀/ψ(z). Used in L33 SQT three-regime g-function. Always
  clipped: r = clip(ψ₀/ψ(z), 1.0, 200.0).
- **KO**: r ≡ ψ₀/ψ(z). L33 SQT 세 영역 g-함수 입력. 반드시 클리핑:
  r = clip(ψ₀/ψ(z), 1.0, 200.0).

### amp  (global SQT amplitude / 전역 SQT 진폭)
- **EN**: Global multiplicative amplitude in ρ_DE = Ω_Λ,0·(1 + amp · g(r)).
  amp must multiply g globally; per-mask amplitudes must be nested
  inside g, never replace the global amp.
- **KO**: ρ_DE = Ω_Λ,0·(1 + amp · g(r))의 전역 곱셈 진폭. amp는 g 전체에
  곱한다. mask별 amp는 g 내부에 중첩될 뿐, 전역 amp를 대체할 수 없다.

---

## 4. Forbidden / deprecated symbols / 금지·폐기 기호

| Symbol / 기호 | Reason / 사유 |
|-------------|-------------|
| σ = 4πG (in SI) | Planck-unit shorthand only; SI requires σ₀ = 4πG·t_P |
| n₀μ = 6.6×10⁻⁴⁴ | Derived from sigma=4πG bug; use 4.1×10⁹⁵ kg m⁻³ |
| Branch B | Replaced by "three-regime" (post-L100) |
| ξ (universal) | Cassini FRAMEWORK-FAIL; use ξ_d or ξ_disf |
| ξ_q < 0 | Phantom branch; report only ξ_q ≥ 0 as SQMH-consistent |
| ν > 0 (RVM) | DESI w_a < 0 needs ν < 0 branch; ν > 0 = wrong sign |
| trapz (numpy 2.x) | Use np.trapezoid directly |

---

## 5. Cross-reference / 상호 참조

- Glossary entries (status, methodology): see paper/GLOSSARY.md
- Numerical constants and SI conversions: CLAUDE.md "재발방지" section
- Three-regime g-function exact form: simulations/L33/, simulations/L34/
- Joint χ² channel decomposition: simulations/Lxx/chi2_joint(_with_shear)

---
