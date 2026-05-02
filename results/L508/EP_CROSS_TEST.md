# L508 — EP |η|=0 PASS_STRONG cross-test robustness

## 임무 재서술
"SQT dark-only (C10k 류) 가 모든 EP 채널 (MICROSCOPE, LLR, Eot-Wash) 에서
|η|=0 PASS_STRONG 을 유지하는가?" 를 정직 평가.

기존 SQT EP 통과의 구조: **baryon 을 Einstein frame 에 분리 유지** + φ-coupling
이 dark sector (DM/DE) 에만 작용 → baryonic test mass 사이의 미분 가속도 구조적 0.

## 1. 채널별 전제와 SQT dark-only 예측

### 1.1 MICROSCOPE 2017 (위성, free-fall, Pt vs Ti)
- 관측 한계: η(Pt, Ti) = (-1 ± 9stat ± 9sys) × 10⁻¹⁵ (Touboul+ 2017, PRL 119 231101).
  업그레이드 2022 final: |η| ≤ 1.4 × 10⁻¹⁵ (95% CL).
- 시험질량: **두 핵자물질 (baryonic)**.
- SQT dark-only 예측: φ 결합이 T^μ_μ^(dark) 에만. baryonic stress-tensor 와는
  Jordan-frame conformal/disformal 인자 부재 → Δa/a = 0 *exact* (트리 레벨).
- **PASS_STRONG**: 한계와 무관하게 구조적 0.

### 1.2 LLR (Lunar Laser Ranging, η ≤ ~10⁻¹³)
- Williams+ 2012 / Hofmann-Müller 2018: |η_Earth-Moon| ≤ 1.4 × 10⁻¹³ (Nordtvedt
  parameter η_N 와 일부 결합).
- 시험질량: **지구 vs 달 — baryonic dominant 이지만 self-gravitational binding
  energy 차 (Nordtvedt 효과) 포함**.
- SQT dark-only 예측: **자기중력 결합 (gravitational self-energy) 은 metric
  level 효과** → φ-DM coupling 이 metric 을 통해 간접 영향.
  - Einstein frame 분리가 *coupling* level 분리이지 *metric source* 분리가
    아니므로, φ background 의 시간변화는 G_N(t) 변동을 만들 수 있음
    (β_dark ~ 0.1 이면 ΔG/G ~ 10⁻¹³/yr scale 가능).
- **PASS (조건부)**: η_LLR ≤ 10⁻¹³ 한계는 여유 있게 통과하나, 정확히 0 은 아님.
  Nordtvedt 채널은 *non-zero* 가능 (구조적 ≤ 10⁻¹⁴ 추정). PASS_STRONG 의 "0"
  주장은 MICROSCOPE 한정.

### 1.3 Eot-Wash (torsion balance, η ≤ ~10⁻¹³)
- Schlamminger+ 2008, Wagner+ 2012: |η| ≤ 1.4 × 10⁻¹³ (Be vs Ti, 지구장 + 태양장).
- 시험질량: **baryonic, 다양한 조성 (Be/Cu/Ti/Al/SiO₂)**.
- 외부장: 지구중력 + 은하 DM background (다섯 번째 힘 source 후보).
- SQT dark-only 예측:
  - baryon-baryon 상대가속도: 구조적 0 (MICROSCOPE 와 동일 논리).
  - **DM background → baryon test mass 가속도 성분**: dark-only 구조에서 baryon
    은 φ 와 결합 안 하므로 *DM 만이 다섯 번째 힘 느낌*. baryonic test mass 사이
    differential 0 보존.
- **PASS_STRONG**: composition-independent 조건 만족.

## 2. SQT dark-only 가 *모든* 테스트 통과? — 정직 답변

| 채널 | 한계 | SQT dark-only 예측 | 등급 |
|---|---|---|---|
| MICROSCOPE | 1.4×10⁻¹⁵ | η = 0 (트리, baryon-baryon) | **PASS_STRONG** |
| Eot-Wash (지구장) | 1.4×10⁻¹³ | η = 0 (baryon-baryon) | **PASS_STRONG** |
| Eot-Wash (DM background) | 약 10⁻⁵ (Adelberger fifth-force) | η = 0 (baryon decouple) | **PASS** |
| LLR Nordtvedt | 1.4×10⁻¹³ | η ≲ 10⁻¹⁴ (G_N(t) drift, non-zero) | **PASS (구조적 0 아님)** |
| Pulsar timing (PSR J0337+1715, η ≤ 1.8×10⁻⁶ for NS) | 1.8e-6 | NS self-energy 큼, dark-only 무관 | **PASS** |

## 3. Composition-dependent EP violation 가능성

dark-only 구조에서 *baryonic* composition-dependence 는 트리 레벨 0. 그러나:

(a) **Loop level**: DM-baryon 산란 (만약 micro-physics 가 nucleon 수준 cross-section
    을 허용하면) 은 nuclear binding energy 비례 항을 만든다. SQT 가 micro-physics
    에 침묵 → 이 채널은 *predict 불가*. 광고 시 "tree-level PASS_STRONG, loop-level
    silent" 명시 필수.

(b) **Self-gravitational binding (Nordtvedt)**: G_N(t) drift → composition-INdependent
    이지만 *body-mass-dependent* (binding fraction). LLR 에서 측정 가능. SQT
    배경 dynamics (φ̇ ≠ 0) 가 |Ġ/G| ≲ 10⁻¹³/yr 에 묶여야 함 — 현재 한계 통과.

(c) **Disformal branch (C11D)**: g̃ = Ag + B∂φ∂φ. baryon 을 Einstein frame 에
    두면 정적 γ=1 (ZKB 2013), composition-dependent EP 0. 그러나 동적 (시간변화
    φ background) 에서 baryon proper time 에 (1 + B φ̇²/2) factor — universal
    이라 EP 위반 없음 (composition-independent).

## 4. 정직 결론

> "EP |η|=0 PASS_STRONG" 광고는 **MICROSCOPE-style baryon-baryon differential
> acceleration 채널** 에 한해 트리 레벨 정확히 성립.
>
> LLR Nordtvedt 채널 은 **구조적 0 이 아님** — G_N(t) drift 와 dark background
> 의 metric 효과로 |η_N| ≲ 10⁻¹⁴ 수준 *예측*. 현재 LLR 한계 (1.4×10⁻¹³) 는
> 여유 있게 통과하나, 차세대 LLR (η ≤ 10⁻¹⁴) 에서 *positive signal* 가능성.
>
> Eot-Wash (DM background source 변종 포함) 는 baryon decoupling 으로 PASS_STRONG.
>
> Composition-dependent EP violation 은 tree-level 0, **loop-level silent**
> (micro-physics 부재). 광고 시 "tree-level, dark-only, baryon-Einstein-frame
> separation 가정 하" 한정 명시.

## 5. Cross-test robustness 등급

- 통과: 3/3 모든 현존 한계 통과 (MICROSCOPE / Eot-Wash / LLR).
- 구조적 0: 2/3 (MICROSCOPE, Eot-Wash). LLR 은 *작지만 nonzero*.
- Falsifiable handle: **차세대 LLR (~10⁻¹⁴), MICROSCOPE-2 (~10⁻¹⁷), STEP (~10⁻¹⁸)**
  에서 LLR Nordtvedt nonzero detection 시 SQT dark-only 의 *positive* 검증 (반대로
  detection 없으면 |β_dark| 또는 φ̇ 제약 강화).

---

**정직 한 줄**: SQT dark-only 는 *baryon-baryon EP 채널 (MICROSCOPE, Eot-Wash) 만
구조적 |η|=0*; LLR Nordtvedt 채널은 G_N(t) drift 로 *작지만 nonzero* 라 PASS_STRONG
주장은 MICROSCOPE 한정으로 좁혀야 한다.
