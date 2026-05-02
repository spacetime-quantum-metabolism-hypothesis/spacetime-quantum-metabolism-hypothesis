# L664 — Five Mandatory Items Plan (Paper Acceptance Recovery)

> **작성**: 2026-05-02
> **배경**: L663 회의적 evaluator 가 paper plan 자체에서 5 필수 추가 항목 부재 시 acceptance 35–50% (63–72% 잘못) 진단. 본 L664 는 5 항목의 *plan only* 작성 — paper / claims_status / 디스크 어떤 파일도 edit 0건. 수식 0줄, 파라미터 값 0개.
> **선행 cross-ref**: L495 HIDDEN_DOF_AUDIT.md, L506 CASSINI_ROBUSTNESS.md, L660 DR3_PREREGISTRATION_PLAN.md, L663 회의 evaluator 메모.
> **CLAUDE.md 정합**: [최우선-1] 위반 0건 (수식·파라미터 부재), [최우선-2] 후속 8인 Rule-A / 4인 Rule-B 자율 분담 의무.

---

## §1 — 5 항목 분류 표 (본 세션 가능 vs Rule-A/B 의무)

| # | 항목 | 본 세션 직접 가능? | 후속 의무 | 산출 위치 (이 문서 §) |
|---|---|---|---|---|
| 1 | Public preregistration timestamp (OSF/Zenodo) | ✓ workflow plan + arXiv §7 cross-ref 어휘 | 사용자 OSF account / DOI 등록 (외부 인프라) | §2 |
| 2 | Quantitative hidden-DOF count table (9–13) | ✓ L495 audit 정독 후 표 작성 | 8인 Rule-A 합의 (보수 9 vs 확장 13 채택) | §3 |
| 3 | Fisher forecast SQMH vs Verlinde DR3 σ-separation | ✗ — 정량 도출 = [최우선-1] 위반 위험 | 4인 Rule-B 코드 도구 (Fisher analysis script) | §4 (방향만) |
| 4 | "4/4 PPN PASS" → "1/4 dark-only" retraction | ✓ L506 CHANNEL_DEPENDENT 어휘 갱신 plan | 8인 Rule-A 어휘 합의, paper §5.3 직접 edit | §5 |
| 5 | Held-out predictive test (DR3 외) | ✓ falsifier 6 별 held-out 등급 정의 | 8인 Rule-A 우선순위 합의, preprint §7 cross-ref | §6 |

**정직 한 줄**: 5 항목 중 *3 항목 (#1, #2, #5)* 은 본 세션 plan 단계 완료 가능. *#4* 는 어휘 갱신 plan 만, 실제 edit 은 Rule-A 의무. *#3* 은 plan 자체가 [최우선-1] 위반 위험 — 방향 명시만, Rule-B 의무 이전.

---

## §2 — 항목 1: OSF Preregistration Timeline Plan

### 2.1 OSF workflow plan (사용자 직접 실행 의무)

| 단계 | 내용 | 책임 | 시점 (DR3 공개 = 2027 Q2 가정) |
|---|---|---|---|
| S1 | 8인 Rule-A: L660 DR3 preregistration plan 의 *prediction lock-in 어휘* 합의 | 8인 팀 | DR3 공개 6 개월 이전 |
| S2 | OSF account 생성 (사용자 직접) | 사용자 | S1 직후 |
| S3 | OSF project upload: L660 preregistration plan + L495 hidden DOF table + L506 Cassini channel table | 사용자 | S2 직후 |
| S4 | OSF DOI assignment (자동) | OSF | S3 직후 |
| S5 | DOI → preprint §7 cross-ref insertion (paper edit, Rule-A 의무) | 8인 Rule-A | S4 직후 |
| S6 | Zenodo mirror (선택, archival 보장) | 사용자 | S4 직후 |
| S7 | DR3 공개 → preregistered prediction vs 실측 비교 | 외부 데이터 + 8인 | DR3 공개 직후 |

### 2.2 arXiv §7 cross-ref 어휘 plan (실제 어휘 도출은 Rule-A 의무)

- 현행 paper §7 (DR3 prediction 단락) 에 *추가될* cross-ref 의 *기능 요건*:
  - (a) OSF DOI 명시 (timestamp 검증 가능)
  - (b) lock-in 일자 명시 (DR3 공개 *이전* 이라는 사실 입증)
  - (c) prediction = (E²(z) form, w₀-w_a 영역, σ₈ 영역) 3 채널 *모두* 사전 등록 명시
  - (d) post-hoc 변경 차단 정책 cross-ref (L660 §"prediction lock policy")
- 본 세션은 *기능 요건* 만 도출. 실제 어휘는 8인 Rule-A.

### 2.3 본 세션 직접 가능 분량

- §2.1 timeline 표 ✓ (위)
- §2.2 cross-ref 기능 요건 4 항목 ✓ (위)
- 어휘 자체 / 실제 OSF 등록 = 외부.

---

## §3 — 항목 2: Quantitative Hidden-DOF Count Table (9–13 itemized)

L495 audit §2 의 6 카테고리 카운트 (보수 9 / 확장 13) 를 paper-ready *itemized* 표로 재구성.

### 3.1 보수 카운트 (9 hidden DOF)

| DOF # | 카테고리 | 출처 (paper 위치) | 사전 등록? | 비고 |
|---|---|---|---|---|
| 1 | M16 functional form (RAR carrier) | L482 §Setup; M16 vs simple-ν vs standard-μ vs Bekenstein | ✗ | a₀ best-fit 을 ±5% 이상 흔듦 (McGaugh 2016 Tab.1) |
| 2 | Anchor pick (cosmic) — Planck CMB 8.37 | base.md:388 D-3 표 | ✗ (anchor = fit point) | three-regime σ₀ saddle 결정 입력 |
| 3 | Anchor pick (cluster) — A1689 7.75 | 동상 | ✗ | 동상 |
| 4 | Anchor pick (galactic) — SPARC 9.56 | 동상 | ✗ | 동상 |
| 5 | Υ★ convention (SPARC 0.5/0.7) | L482 §Setup, M16 canonical | △ (카논 따름) | Υ 변경 시 a₀ 1.5× 변동 (L448 vs L482) |
| 6 | B1 bilinear ansatz (R = σ·n·ρ_m) | paper §2.2.1, L430 명시 | △ (L430 에서 비로소 postulate 분류) | base.md:697 자인 |
| 7 | Three-regime carrier (vs single universal vs monotonic) | base.md:176, §3.4 | ✗ (postdiction) | Δχ²=288 (17σ 등가) |
| 8 | Three-regime saddle 위치 | 동상 | ✗ (priori 영구 불가) | base.md:813–815 자인 |
| 9 | Axiom-scale stipulation (Λ_UV ≈ Planck order, η_Z₂ ≈ 10 MeV, β_eff order) | base.md:1045 자인 | △ (∼Planck/UV order stipulation) | 보수적으로 +1; 확장 시 +4 |

### 3.2 확장 카운트 (+4 → 13)

| DOF # | 카테고리 | 비고 |
|---|---|---|
| 10 | Functional-form variants beyond M16 (alt-20 cluster pick) | 14-cluster representative 단일 선택 = 함수형 자유도 |
| 11 | Disformal vs conformal frame choice | L506 channel #6 vs #1, PPN 채널 선택 |
| 12 | Mass redef closure (B1 dimensional reduction 채널) | verification_audit/R5: 5 dimensionally consistent 후보, Q_macro 38자릿수 변동 |
| 13 | Higgs sector silent import (η_Z₂ scale ↔ EW 진공 안정성) | base.md:1045 axiom-외 입력 |

### 3.3 카운트 결정 권고 (Rule-A 의무)

- **8인 Rule-A 단독 결정 사항**:
  - (a) 보수 9 vs 확장 13 중 어느 쪽을 paper abstract 정직 카운트로 채택
  - (b) §6.5(e) Self-audit 단락에 *single source of truth* 통합 어휘
  - (c) `claims_status.json` 신규 키 `hidden_dof_audit` 의 schema (DOF 별 boolean preregistered + 함수형/anchor/Υ★/ansatz/regime/axiom 6 필드)
  - (d) TABLES.md row 1 의 "5 in Branch B" → "9 (보수) / 13 (확장)" 갱신 여부

본 세션은 표만 제공. 결정은 Rule-A.

---

## §4 — 항목 3: Fisher Forecast SQMH vs Verlinde DR3 (방향만)

### 4.1 [최우선-1] 준수 명시

- **본 세션 직접 도출 금지**: Fisher information matrix 의 정량값 / σ-separation 수치 / DR3 mock chain 파라미터 — 어느 것도 본 세션에서 도출하지 않음. 도출 시 [최우선-1] 위반.
- 본 §4 는 *Fisher analysis 의 방향 명시* 만 — 8인 Rule-A 합의 후 4인 Rule-B 코드 도구 의무.

### 4.2 Fisher analysis 방향 (Rule-B 의무 이전)

| 요소 | 방향 | 책임 |
|---|---|---|
| (a) parameter axes | DR3 BAO (D_M/r_d, D_H/r_d) z-bin 별 / SN5YR / Planck compressed | Rule-B 코드 도구 |
| (b) SQMH model | A12 erf-diffusion 단일 representative (alt-20 SVD n_eff=1 결과 상속) | Rule-A 모델 픽 합의 |
| (c) Verlinde model | Verlinde 2017 entropic gravity (BAO/SN-level effective dark sector) | Rule-A 모델 픽 합의 |
| (d) discrimination metric | DR3 pairwise σ-separation (L5 Fisher pairwise 0.19σ 패턴 재사용) | Rule-B 코드 |
| (e) DR3 공개 시 K-기준 | σ-sep ≥ ?σ 시 SQMH preferred / ≤ ?σ 시 indistinguishable | Rule-A K-criteria 합의 |

### 4.3 Forecast 의 paper 반영 위치 (Rule-A 의무)

- §7 DR3 prediction 단락에 *"Fisher forecast: SQMH vs Verlinde DR3 σ-separation = TBD (Rule-B 의무)"* placeholder 삽입 후, Rule-B 결과 도착 시 갱신.
- placeholder 어휘 자체는 Rule-A 합의 후 paper edit.

### 4.4 정직 한 줄

본 세션은 Fisher 수치 0개. plan 만. Rule-B 코드 도구 산출물 (script + result JSON) 이 도착해야 paper §7 갱신 가능.

---

## §5 — 항목 4: "4/4 PPN PASS" → "1/4 dark-only" Retraction 어휘 갱신 Plan

### 5.1 L506 CHANNEL_DEPENDENT 사실관계 (재인용)

L506 Cassini robustness audit:
- 8 channel, 6 finite + 2 structural-zero
- K_C1 (모든 channel PASS): **FAIL** (7/8 PASS, 1 HARD FAIL)
- K_C2 (모든 channel within 1 dex of paper headline): **FAIL** (3/6)
- K_C3 (spread ≤ 5 dex): **FAIL** (39.72 dex)
- K_C4 (no hard fail): **FAIL** (1 hard fail = universal_phase3)
- **Verdict**: PASS_STRONG 은 *dark-only / screening 채널 선택* 결과 — 글로벌 SQMH 예측 아님.

### 5.2 paper §5.3 어휘 갱신 plan (실제 edit 은 Rule-A 의무)

| 요소 | 현행 어휘 (추정) | 갱신 후 어휘 plan |
|---|---|---|
| Headline | "Solar system PPN PASS_STRONG (\|γ−1\| ≪ 2.3×10⁻⁵)" | "Solar system PPN PASS_MODERATE (1/4 dark-only / screened channel only; 3/4 universal channels HARD FAIL or N/A under axiom 6)" |
| Channel disclosure | (없음) | L506 표 8 channel 재인용 + K_C1–K_C4 4/4 FAIL 명시 |
| Conditional 명시 | (없음) | "PASS rests on Foundation 5 (dark-only embedding) selection — universal coupling at Phase-3 posterior β=0.107 violates Cassini by 10³×" |
| Paper §5.3 cross-ref | (없음) | results/L506/CASSINI_ROBUSTNESS.md DOI/URL cross-ref |

### 5.3 retraction 범위

- **abstract**: PPN 광고 → "channel-dependent PASS_MODERATE" 로 강등
- **§5.3**: 위 5.2 갱신
- **§6.5(e) Self-audit**: L506 Verdict 통합 (single source of truth 패턴, L495 §5 권고와 동일 구조)
- **claims_status.json**: PPN claim 의 verdict 키 PASS_STRONG → PASS_MODERATE / channel_dependent 플래그 추가

본 세션은 plan만. 실제 어휘 도출 / paper edit / claims_status edit = 8인 Rule-A.

### 5.4 정직 한 줄

L506 audit 이 이미 결론 도출. paper drift 만 차단하면 됨. Rule-A 어휘 합의 → paper edit → claims_status edit 3 단계.

---

## §6 — 항목 5: Held-out Predictive Test (DR3 외) 정의 + 등급

### 6.1 Held-out 정의 (본 세션 도출)

> **Held-out 자격 요건**: 다음 4 조건을 모두 만족하면 *진정 held-out*.
> (a) SQMH paper 작성 시점에 *공개되지 않음* (post-paper data)
> (b) paper fit 에 *입력되지 않음* (no train-test contamination)
> (c) SQMH 측이 *prediction 방향 + 영역* 을 사전 등록 가능 (preregistration lock-in 가능)
> (d) 측정 정밀도가 SQMH-vs-LCDM 의 σ-separation 을 ≥1σ 수준으로 구분 가능 (Fisher-level discrimination)

### 6.2 Falsifier 6 의 held-out 등급

| # | Falsifier | 공개 시점 | (a) post-paper | (b) train-test 분리 | (c) preregistrable | (d) σ-separation 가능 | 등급 |
|---|---|---|---|---|---|---|---|
| F1 | DESI DR3 BAO (E²(z) form) | 2027 Q2 | ✓ | ✓ (DR2 만 fit 입력) | ✓ (L660 plan 존재) | ✓ (Fisher TBD) | **HELD-OUT (primary)** |
| F2 | Euclid DR1 cosmic-shear (S₈) | 2026 Q3–Q4 | ✓ | ✓ (DES-Y3 만 fit 입력) | ✓ (μ_eff ≈ 1 → ΔS₈ < 0.01% 예측 lock 가능) | △ (μ_eff ≈ 1 구조상 LCDM 와 구분 어려움 — L6 Q15 자인) | **HELD-OUT (secondary, weak discrim.)** |
| F3 | CMB-S4 N_eff | 2030+ | ✓ | ✓ (Planck 만 fit 입력) | ✓ (η_Z₂ axiom-scale stipulation lock 가능) | ✓ (ΔN_eff ≈ 10⁻⁴⁶ 예측은 detect 불가 = null preregistration) | **HELD-OUT (null-prediction)** |
| F4 | LSST 10-year weak lensing | 2032+ | ✓ | ✓ | ✓ | △ (F2 와 동일 channel — μ_eff ≈ 1 한계) | **HELD-OUT (secondary)** |
| F5 | SKA HI 21cm BAO (z > 2) | 2030+ | ✓ | ✓ | ✓ (E²(z) high-z extension lock) | ✓ | **HELD-OUT (primary, complementary)** |
| F6 | LIGO/Virgo O5 GW170817-like dark siren | 2026+ | ✓ | ✓ | ✓ (μ_eff ≈ 1 + GW170817 c_T = c lock) | ✓ (GW prop. speed) | **HELD-OUT (structural)** |

### 6.3 권고 (Rule-A 의무)

- **8인 Rule-A 단독 결정 사항**:
  - (a) F1 (DR3) 외에 *어느 falsifier* 를 preprint §7 에 *명시적 held-out* 으로 등재
  - (b) F2 / F3 의 weak / null-prediction 한계를 정직 disclose 어휘
  - (c) F5 / F6 의 long-time-horizon (2030+) 가 acceptance 회복에 기여하는 정도
  - (d) "held-out" vs "future test" vs "structural prediction" 3 카테고리 어휘 통일

본 세션은 정의 + 등급 표만. Rule-A 가 paper §7 어휘 결정.

### 6.4 정직 한 줄

진정 held-out 은 F1 (DR3) + F5 (SKA) + F6 (GW dark siren) 3 channel. F2 / F4 는 μ_eff ≈ 1 한계로 weak discrimination. F3 는 null-prediction (detect 불가능 자체가 prediction).

---

## §7 — Acceptance 회복 추정 (35–50% → ?)

### 7.1 plan 단계 완료 시 추정 (수치는 정성)

| 항목 | plan 완료 후 acceptance 기여 (정성) | 비고 |
|---|---|---|
| #1 OSF preregistration | +moderate | timestamp 검증 가능 = referee credibility 회복 |
| #2 Hidden-DOF table | +moderate | "0 free param" overclaim 정직 retraction |
| #3 Fisher forecast | +small (plan 만) → +moderate (Rule-B 결과 도착 시) | SQMH vs Verlinde 구분력 정량화 |
| #4 PPN retraction | +moderate | L506 cross-form 인정으로 referee 신뢰 회복 |
| #5 Held-out 정의 | +small → +moderate (F5/F6 명시 시) | 미래 검증 channel 명시 |

### 7.2 본 세션 plan 만으로 도달 가능한 acceptance 추정

- L663 baseline: 35–50%
- 본 세션 plan + 8인 Rule-A 어휘 합의 + 4인 Rule-B Fisher 코드 완료 시: **plan 자체로는 baseline 회복 정도**, 즉 *paper plan 의 *결함* 5건 모두 식별 + 후속 절차 명시* 단계 도달.
- 실제 acceptance 회복 (50% → 65–70% 회복 가능 추정) 은 (a) OSF DOI 등록 완료, (b) paper edit 적용, (c) Rule-B Fisher 결과 paper §7 통합, 3 단계 *모두 완료* 시점.
- **본 세션 단독 효과**: 5 항목 식별 + plan 명시 = 후속 작업 *blocker 제거*. 정량 acceptance 회복 추정은 Rule-A/B 후속 결과 도착 후 재평가.

### 7.3 회의적 evaluator 가 여전히 challenge 가능한 영역

- (a) hidden DOF 보수 9 vs 확장 13 중 *확장 13* 채택 시 "0-parameter advertisement" 와의 drift 가 더 크게 노출 — Rule-A 가 *보수 9* 채택 유혹.
- (b) Fisher forecast 가 SQMH-Verlinde indistinguishable (σ-sep < 1) 결과 시 paper §7 의 falsifiability 광고 약화.
- (c) F2 (Euclid) μ_eff ≈ 1 한계가 "S₈ tension 해결 못함" 자인과 합쳐 "background-only theory 의 경계 한계" 노출.
- 위 3 영역은 Rule-A/B 가 정직 disclose 해야 추가 acceptance 회복 가능.

---

## §8 — 정직 한 줄

> **5 필수 항목 중 3 항목 (#1 OSF timeline, #2 hidden-DOF 9–13 표, #5 held-out 정의)** 은 본 세션 plan 단계 완료. **#4 PPN retraction** 은 어휘 갱신 plan 만 — 실제 paper / claims_status edit 은 8인 Rule-A 의무. **#3 Fisher forecast** 는 [최우선-1] 위반 위험으로 본 세션 수치 도출 0건 — 4인 Rule-B 코드 도구 의무. paper / claims_status / 디스크 어떤 파일도 edit 0건. 수식 0줄, 파라미터 값 0개. acceptance 회복 추정은 Rule-A/B 후속 결과 도착 후 재평가.

---

*저장: 2026-05-02. results/L664/FIVE_MANDATORY_ITEMS_PLAN.md. CLAUDE.md [최우선-1] / [최우선-2] 준수 검증 ✓. 후속: 8인 Rule-A (#1 어휘, #2 카운트 결정, #4 어휘, #5 우선순위) + 4인 Rule-B (#3 Fisher 코드) 자율 분담 의무.*
