# L497 — SQT Predictions: Invariance Audit Across Analysis Choices

> **작성**: 2026-05-01
> **임무**: 어떤 SQT prediction 이 *모든* 분석 선택 (Υ★ convention, interpolating-function form, anchor 정의, datacuts) 에 *invariant* 한가? 진정 invariant 만 PASS_STRONG 자격 유지, 변동 claim 은 PASS_MODERATE / PARTIAL 격하.
> **소스**: L422/L448 (BTFR), L482 (RAR PASS_STRONG candidate), L483 (4-channel reframing), L489 (independent re-verification of L482), L478~L490 round-1 synthesis, L66~L76 Branch B regime structure, SQT_PROGRESS_SUMMARY.md.
> **참고**: 본 문서는 카탈로그/verdict only. 8인/4인 라운드 *전 단계*. paper/base.md 직접 수정 0건.

---

## 0. 정직 한 줄

**SQT 의 단일 진정 invariant 결과는 "a₀ ~ c·H₀/(2π) 의 *order-of-magnitude / factor-≤1.5* 일치" 뿐이다 — 이를 넘는 모든 정량 claim (5/5 K, ΔAICc=+0.70, 2.5% offset, 0.006 dex tightness) 은 functional-form / Υ★ convention / V_flat 정의 / cut quality 중 *최소 하나* 에 의존해 흔들리며 PASS_MODERATE 또는 PARTIAL 로 격하된다.**

---

## 1. Analysis-choice axes (5 축)

본 audit 가 변동시키는 분석 선택 축:

| Axis | Variation | 출처 |
|---|---|---|
| **A1 Υ★ convention** | Υ_disk ∈ {0.30, 0.40, 0.50 (canonical), 0.60, 0.70, 0.80} ; Υ_bul ∈ {0.5, 0.7 (canonical), 0.9} | L448 K_Z4 scan, L483 channel C, L489 §4 |
| **A2 Interpolating function** | M16 (`g_b/(1−exp(−√(g_b/a₀)))`), simple-ν (`0.5+√(0.25+1/y)`), standard-μ (Bekenstein 1984), power-law n free | L482 (M16 only), L483 channel A, L489 §2 |
| **A3 Anchor / aggregation** | Point-by-point RAR (n=3389) vs BTFR V_flat^4 (n=175) vs outermost-only RAR (n=175) vs innermost-only RAR (n=175) vs deep-MOND-only (g_b<a₀/10) | L422 (BTFR), L448 (BTFR meta), L482 (RAR), L483 channel B, L489 §5 |
| **A4 Quality cuts** | SPARC Q∈{1}, Q∈{1,2}, Q∈{1,2,3}; V_obs > {0, 5, 10} km/s; finite filters | L422 (Q≤2), L448 (Q12 cut), L482 (V_obs>5), L483 (163 galaxies subset) |
| **A5 H₀ anchor** | Planck H₀=67.4 → a₀_SQT=1.0422e−10 ; Riess H₀=73.0 → a₀_SQT=1.1294e−10 | L482 §Setup, L489 §3 |

---

## 2. Robustness Invariants Table — 본 audit 핵심

| # | SQT prediction (claim) | 구체 정량 | A1 Υ★ | A2 ν-form | A3 anchor | A4 cuts | A5 H₀ | **Invariance** | **Verdict 격상** |
|---|---|---|---|---|---|---|---|---|---|
| **C1** | a₀ ~ c·H₀/(2π) — order of magnitude / factor-≤1.5 | a₀ ∈ [0.7, 1.6]×10⁻¹⁰ across all axes | ✓ | ✓ | ✓ | ✓ | △ (H₀ 자체 입력) | **TRUE INVARIANT** | **PASS_STRONG** (단, "order/factor" 한정) |
| **C2** | a₀ best-fit = (1.07 ± 0.015)×10⁻¹⁰ , 2.5% offset | M16 + Υ=0.5/0.7 + Q12 + V>5 + Planck H₀ | ✗ Υ↑→a₀↓, Υ↓→a₀↑ (L448 scan) | ✗ M16=1.069 / simple-ν=1.043 / std-μ=1.208 (spread 16%) | ✗ BTFR V_flat=1.53, outer-only RAR=0.86, inner-only=0.69 | △ Q-cut 의존 약함 | △ 67.4→73 시 a₀_SQT↑8.4% | **NOT INVARIANT** | **PASS_MODERATE** (M16 + Υ canonical 한정) |
| **C3** | 5/5 K-criteria PASS (L482) | K_R1~K_R5 모두 PASS | ✗ Υ scan 시 30%/PASS K_R1 만 invariant; K_R2/K_R4 흔들림 | ✗ standard-μ 시 K_R4 = +83 (FAIL) | ✗ BTFR-only (L448) 시 5/5 → 0/5 | △ | △ | **NOT INVARIANT** | **PASS_MODERATE → PARTIAL** (M16 한정) |
| **C4** | σ(log a₀) = 0.006 dex (statistical) → K_R2 PASS at 2σ | M16 + canonical | △ statistical only, sys 무시 | ✗ cross-form spread 0.064 dex (10× 더 큼) | ✗ aggregation 변경 시 spread 0.25 dex | △ | ✓ | **NOT INVARIANT** | **PARTIAL — K_R2 정보량 0** (L489 §4) |
| **C5** | ΔAICc(SQT − McGaugh) = −56 (SPARC 가 M16 보다 SQT a₀ 선호) | M16 한정 | △ | ✗ standard-μ 채택 시 McGaugh 1.20 이 *정답* (a₀_fit=1.208) — 부호 반전 | △ | △ | △ | **NOT INVARIANT** | **PARTIAL** — cherry-pick 의혹 (L489 §3) |
| **C6** | BTFR slope = 4 a priori | L422 K1 [3.8, 4.2] | △ Υ-tension | △ slope-4 는 deep-MOND limit 구조적 | ✗ V_flat 정의 (asymptotic vs R_max sample) 으로 slope 3.58 → 3.70 변동 | ✗ Q≤2 vs Q=1 으로 slope 변동 | ✓ | **NOT INVARIANT** | **FAIL (영구)** — L422/L448 slope mismatch 유지 |
| **C7** | RAR exists (Newton 단독 SPARC 재현 불가) | ΔAICc(SQT − Newton) = −41 171 | ✓ | ✓ (Newton은 모든 ν 에서 패배) | ✓ (BTFR/RAR/cuts 무관) | ✓ | ✓ | **TRUE INVARIANT** | **PASS_STRONG** — but "Newton 패배"는 1970s SPARC pre-existing fact, **정보량 낮음** (L489 §4 K_R5 free-pass 지적) |
| **C8** | Υ★=0.5 가 RAR-self-consistent (BTFR 의 Υ★-tension 은 V_flat-효과) | L483 channel C | ✓ Υ grid scan min χ² @ Υ=0.50 | △ M16 / simple-ν 양쪽에서 Υ=0.5 선호 | △ RAR 한정 | ✓ | ✓ | **MOSTLY INVARIANT** | **PASS_MODERATE** |
| **C9** | Branch B 3-regime σ_0 spectrum (cosmic / cluster / galactic, span 1.81 dex) | L66~L70 multivariate + cross-validation | ✓ Υ 무관 (data-driven binning) | ✓ ν-form 무관 | △ V_flat-axis 위에서 비단조 (L67 단조 KILL) | ✓ Q-cut 무관 | ✓ | **STRUCTURAL INVARIANT** | **PASS_MODERATE** (단, "3-regime" 자체는 phenomenological choice; smooth quadratic 도 동률 — L187, L194) |
| **C10** | Branch B 와 smooth quadratic σ_0(ρ) 통계 동률 | L194/L195/L196 | ✓ | ✓ | ✓ | ✓ | ✓ | **TRUE INVARIANT** | **PASS_STRONG** (단, "data 가 둘 구분 못 함" 의미 — Branch B 우월성 주장 폐기) |

---

## 3. Verdict 격하 권고

| 원래 claim | 원래 grade | 본 audit 격하 | 사유 |
|---|---|---|---|
| L482 a₀_RAR = 1.07e−10 ↔ SQT 1.04e−10, 2.5% 일치 (5/5 K PASS) | PASS_STRONG candidate | **PASS_MODERATE** | A2 ν-form 변경 시 16% spread, σ_sys 0.06 dex 가 σ_stat 0.006 dex 의 10× — K_R2 정보량 0 |
| ΔAICc(SQT − McGaugh) = −56 | PASS_STRONG | **PARTIAL — cherry-pick risk** | standard-μ 채택 시 부호 반전 (McGaugh 1.20 이 정답) |
| L483 4-channel revival (BTFR 부활) | PASS (factor 1.5) | **PASS_MODERATE 유지** | A2/A3 변경 시 ratio 1.10–1.29× 안정 (B 채널 1.29×는 경계) |
| L482 RAR ↔ L422/L448 BTFR independence | "partly independent" | **NOT INDEPENDENT** | A3 변경 (outermost-only RAR=0.86 vs BTFR=1.53) 으로 둘 차이 = V_flat 추출 정의 시스테매틱, 새 물리 아님 (L489 §5) |
| Branch B 3-regime "uniquely SQT" | PASS | **PASS_MODERATE → PARTIAL** | smooth quadratic 과 통계 동률, parsimony 로 smooth 우선 (L194/L200) |

---

## 4. 진정 PASS_STRONG 자격 — 격상 유지 claim

**오직 두 개**:

1. **C1 (a₀ order-of-magnitude / factor-≤1.5 일치)**: 모든 ν-form, 모든 Υ★, 모든 anchor (RAR/BTFR/outer/inner/deep) 에서 a₀_fit ∈ [0.7, 1.6]×10⁻¹⁰ 박스 내. SQT 1.04 는 박스 중앙. **이 부분만 진정 prediction**.
2. **C7 (Newton-only SPARC 재현 불가)**: 모든 분석 선택에서 ΔAICc(non-Newton − Newton) ≪ 0. 단 정보량 낮음 (1970s 기존 사실).

---

## 5. PASS_MODERATE / PARTIAL 격하 claim

| Claim | 격하 |
|---|---|
| 정량 a₀ = 1.04 ± 0.02 (5/5 K) | PASS_MODERATE (M16 한정) |
| ΔAICc(SQT − McGaugh) = −56 | PARTIAL (cherry-pick 위험) |
| BTFR slope=4 a priori | FAIL (영구) |
| Branch B "uniquely SQT" | PASS_MODERATE (smooth 동률) |
| L482 RAR ⊥ L448 BTFR (독립 채널) | NOT INDEPENDENT |
| σ(log a₀) = 0.006 dex 정밀 | PARTIAL (sys 0.06 dex 포함 시 정보량 ↓) |

---

## 6. paper/base.md update 권고 (직접 edit 보류)

**§4.1 RAR row**: 현재 "PASS_STRONG candidate (5/5 K)" → 권고 "PASS_MODERATE (M16-functional-form-한정 5/5; cross-form spread 0.064 dex; order-of-magnitude factor ≤1.5 invariant — see L489 / L497)".

**§6 limitations**:
- "K_R2 σ_stat 0.006 dex 만 사용 — σ_sys 0.06 dex (cross-ν-form) 포함 시 정보량 0" 한 줄 추가.
- "L482 RAR 와 L448 BTFR 의 a₀ 차이 는 V_flat 정의 systematic 이며 새 물리 아님" 한 줄 추가.
- "Branch B 와 smooth quadratic 통계 동률 — L194 cross-validation" 한 줄 추가.

**claims_status.json**:
- `RAR_a0_strong`: 신규 키, `grade: PASS_MODERATE, scope: M16+Υcanonical, cross_form_spread: 0.064 dex`.
- `RAR_a0_orderof`: 신규 키, `grade: PASS_STRONG, scope: factor-1.5 invariance across (Υ, ν, anchor, cuts)`.

---

## 7. 다음 라운드 권고 (Round 2 우선순위)

1. **L482 8인 라운드** 시 Rule-A 본 audit 결과 (functional-form 의존성) 반드시 검토. K_R2 재정의 (sys 0.06 dex floor) 합의.
2. **K_R6 (cross-form |Δlog a₀| ≤ 0.04) 신규 추가**: L489 § 4 권고. 본 audit 채택 시 격하 자동.
3. **Bayesian per-galaxy Υ marginalization** (Li+18 방식): Υ-axis 시스테매틱 분리.
4. **L448 V_flat 정의 변경 재계산** (outermost RAR fit): 1.53 → 0.86 예상, BTFR 채널 부활 가능성 확인.

---

## 8. CLAUDE.md 정합성

- **결과 왜곡 금지**: PASS_STRONG → PASS_MODERATE 격하 정직 기록. ✓
- **[최우선-1] 방향만 제공, 지도 금지**: 본 문서 신규 수식 0줄, 신규 파라미터 0개, 새 이론 형태 0건. 격하 사유는 *분석-축* 만 명시. ✓
- **[최우선-2] 팀 독립**: 본 audit 은 카탈로그/verdict only. 후속 8인팀이 K_R2/K_R6 재정의를 자율 도출. ✓
- **paper/base.md 직접 수정 금지**: 권고만, edit 0건. ✓
- **L6 8인/4인 규칙**: PASS_STRONG → PASS_MODERATE 격하 (이론 클레임) → Rule-A 8인 라운드 필수. 본 문서는 *전 단계* 카탈로그. ✓

---

## 9. 한 줄 종합

**SQT 의 진정 invariant 는 "a₀ ~ c·H₀/(2π) factor-≤1.5 일치 (C1)" 와 "Newton-only SPARC 재현 불가 (C7)" 단 둘. 나머지 정량 claim (2.5% offset, 5/5 K, ΔAICc=−56, BTFR slope=4, Branch B uniqueness, σ_log=0.006 dex 정밀, RAR⊥BTFR 독립) 은 모두 분석-축 (Υ★ / ν-form / anchor / cuts / H₀) 중 최소 하나에 의존해 흔들리며 PASS_MODERATE 또는 PARTIAL 로 격하 권고.**

---

*저장: 2026-05-01. results/L497/INVARIANTS.md. 본 문서는 메타-audit 이며 simulations/ 신규 코드 0줄. paper/ 직접 수정 0건. L498~L499 미실행.*
