# L505 — Phase 2 종합 (RAR 글로벌 고점 자격 *최종* 판정)

> **작성**: 2026-05-01
> **저자**: 단일 메타-합성 에이전트 (8인/4인 라운드 *없음* — synthesis only)
> **substrate**: results/L497, results/L498, results/L499 직접 Read.
> **CLAUDE.md 정합성**: 수식 0줄, 신규 파라미터 0개, paper/base.md 직접 edit 0건.

---

## 0. 정직 한 줄 — 시작 전 디스크 상태

**임무가 가정한 "L500-L504 Phase 2 5 loop" 산출물은 *디스크에 존재하지 않는다*.** `results/L500/` 와 `results/L501/` 은 *빈 디렉터리*, `L502/L503/L504` 는 디렉터리 자체가 미생성. 실제로 존재하는 Phase 2 substrate 는 **L497 (INVARIANTS) + L498 (FALSIFIER_INDEPENDENCE) + L499 (PHASE1_SYNTHESIS)** 3건 뿐. 본 종합은 이를 정직 보고하며, *실재* 3 loop 위에서 RAR 글로벌 고점 자격 최종 판정을 수행한다. L500-L504 슬롯은 Round 3 예약으로 명시.

---

## 1. 5 loop verdict 표 (실재 3 + 예약 2)

| Slot | Loop | Status | 핵심 산출 | Verdict 영향 |
|------|------|--------|-----------|--------------|
| **R2-1** | L497 | EXECUTED | INVARIANTS.md — 5축(Υ★/ν-form/anchor/cuts/H₀) 변동 robustness audit | A5(L482 RAR) **PASS_STRONG → PASS_MODERATE 격하** 권고 (본 종합의 1차 압력) |
| **R2-2** | L498 | EXECUTED | FALSIFIER_INDEPENDENCE.md — 6 falsifier 채널 상관 분석 | N_eff = 4.44 (참여비) ; 8.87σ (corr) vs 11.25σ (naive) — "6 indep" headline 격하 |
| **R2-3** | L499 | EXECUTED (meta) | PHASE1_SYNTHESIS.md — 8 candidate verdict 표 + L491-L498 빈 슬롯 정직 인정 | A5 단독 후보 식별 ; A1/A2/A3/A4 즉시 격하 4건 ; effective N ≈ 3.5 ± 0.5 합의 (L498 재분석으로 4.4 로 상향) |
| R2-4 | **L500 RESERVED** | EMPTY DIR | — | 8인 라운드 K_R6 (cross-form |Δlog a₀| ≤ 0.04) 신규 도입 검증 슬롯 |
| R2-5 | **L501 RESERVED** | EMPTY DIR | — | 독립 채널 RAR 재현 (cluster / dwarf / low-z FRB) 슬롯 |

---

## 2. RAR 글로벌 고점 자격 — *최종* 판정

### 2.1 입력 신호 (3 loop substrate)

| 출처 | RAR 자격에 미치는 영향 |
|------|------------------------|
| L499 §2.1 | "A5 = 현 시점 SQMH Phase-1 의 *유일한* 글로벌 고점 *후보*. 단 cluster/dwarf/FRB 독립 채널 재현 *전까지는* '후보' 표기 의무." |
| L497 §2 C2 | "M16 + Υ canonical 한정 5/5 K-PASS — ν-form 변경 시 spread 16%, σ_sys 0.06 dex (σ_stat 0.006 dex 의 *10×*) → K_R2 정보량 0" |
| L497 §2 C5 | "ΔAICc(SQT − McGaugh) = −56 은 standard-μ 채택 시 *부호 반전* (McGaugh 1.20 이 정답) — cherry-pick risk" |
| L497 §2 C8/C1 | "Υ★=0.5 self-consistent + a₀ factor-≤1.5 invariant 두 항목만 진정 PASS_STRONG" |
| L498 §4-5 | "RAR 은 Euclid/LSST/DESI bloc 과 부분 상관 (cosmic-shear/BAO 공유), 다만 SPARC 자체는 8 observable basis 의 *외각* — 독립성 영향 미미" |
| L499 §4 | "Hidden DOF (Υ★+H₀+표본 cut) effective k ≈ 3 → ΔAICc(+0.70) 가 explicit penalty 시 −5.3 (free fit 우세)" |

### 2.2 최종 등급 — **PASS_MODERATE (격하 확정)**

**판정**: **PASS_STRONG 격하 → PASS_MODERATE 확정.**

**3 축 합의 근거**:

1. **L497 robustness 축** — ν-form 변경 시 a₀ spread 0.064 dex, σ_stat (0.006 dex) 의 10×. K_R2/K_R4 가 functional-form-한정. → PASS_MODERATE (격상 후보 자격 박탈).
2. **L499 hidden DOF 축** — Υ★+H₀+cut 의 effective k ≈ 3 미반영. explicit penalty 시 ΔAICc 부호 변동. → PASS_MODERATE (0-free-param 주장 자체가 effective k≈3 위에서만 성립).
3. **L499 §2.1 독립채널 축** — cluster/dwarf/FRB 독립 재현 부재. PASS_STRONG 격상은 이 3 채널 중 *최소 1개* 재현 후에만 가능. → 현 시점 *후보* 자격 자체도 "PASS_MODERATE + 향후 격상 가능" 으로 보수화.

**격하의 "정직 한 줄" (L497 §0 인용)**: "SQT 의 단일 진정 invariant 결과는 'a₀ ~ c·H₀/(2π) factor-≤1.5 일치' 뿐."

### 2.3 "PASS_STRONG (factor-≤1.5 invariance only)" 보존 항목

L497 §4 의 두 항목은 별도로 PASS_STRONG 자격 *유지*:

- **C1**: a₀ ∈ [0.7, 1.6]×10⁻¹⁰ box, factor-≤1.5 invariant (모든 5축에서).
- **C7**: Newton-only SPARC 재현 불가 (정보량 낮음, 1970s 기존 사실).

→ paper §4.1 에서 "RAR PASS_STRONG candidate" 행은 두 sub-row 로 분리:
- `RAR_a0_orderof` — PASS_STRONG, scope: factor-1.5 invariance.
- `RAR_a0_quantitative` — **PASS_MODERATE**, scope: M16 + Υ canonical 한정.

---

## 3. Phase 1 + Phase 2 통합 paper update plan

### 3.1 paper/base.md §4.1 (RAR / BTFR 결과 행)

**현재 (Phase 1 기준)**:
> A5 (L482) — RAR 5/5 K PASS_STRONG candidate, 2.5% offset, ΔAICc(SQT−free)=+0.70.

**수정 권고 (Phase 2 통합)**:
> RAR 결과는 두 sub-claim 으로 분리:
> (a) **a₀ order-of-magnitude (factor-≤1.5)** invariance — PASS_STRONG (모든 Υ★/ν-form/anchor/cuts/H₀ 변동에서 [0.7, 1.6]×10⁻¹⁰ 유지).
> (b) **a₀ 정량 1.07e−10 (2.5% offset, 5/5 K)** — **PASS_MODERATE** (M16 + Υ canonical 한정 ; ν-form spread 0.064 dex ; effective k≈3 hidden DOF 미반영).
> 격상 조건: cluster RAR / dwarf RAR / low-z FRB DM-z 중 ≥1 채널 재현.

### 3.2 paper/base.md §6 (limitations) — 신규 4행 추가

L497 §6 + L498 §8 + L499 §3 합의:

1. "K_R2 σ_stat 0.006 dex 만 사용 — σ_sys 0.06 dex (cross-ν-form) 포함 시 정보량 0."
2. "L482 RAR ↔ L422/L448 BTFR 의 a₀ 차이는 V_flat 정의 systematic ; 새 물리 아님."
3. "0-free-parameter PASS_STRONG 주장은 Υ★+H₀+표본 cut effective k ≈ 3 위에서 성립."
4. "6 pre-reg falsifier 는 N_eff ≈ 4.44 (참여비) ; corr-corrected 결합 8.87σ (active 5 = 9.95σ), naive 11.25σ 인용 금지."

### 3.3 paper/base.md §6 (forecasts) — Phase 2 §8 권고 적용

- "6 independent 5σ-class falsifiers" → **"5 active + 1 null falsifier across N_eff ≈ 4.44 independent observable channels"**.
- 결합 significance: **8.87 σ (all six, ρ-corrected) / 9.95 σ (active five, ρ-corrected)**.
- LSST 를 Euclid 와 합쳐 "WL block" 으로 통합.
- 3 load-bearing orthogonal: CMB-S4 (P22, 7.9σ) + ET (P16, 7.4σ) + SKA (P25, NULL). 이 3개 결합 = 10.83σ at full independence.

### 3.4 paper/base.md §6 (cherry-pick 즉시 격하 4건)

L499 §3 표 그대로 §6 limitations 에 4행:

- A1 (L478 Fisher) — NOT_INHERITED 영구.
- A2 (L479 Holographic) — CONSISTENCY_CHECK 유지, cluster scale claim 폐기.
- A3 (L480 closure) — mutual-exclusion KILL.
- A4 (L481 H1 hybrid) — 3-criteria fail, "H1 → H1' (R12 sector-selective)" 신규 가설로만 잔존.

### 3.5 claims_status.json — 신규 키 4개

- `RAR_a0_orderof` : grade=PASS_STRONG, scope="factor-1.5 invariance, all 5 axes".
- `RAR_a0_quantitative` : grade=PASS_MODERATE, scope="M16+Υcanonical only, cross_form_spread=0.064 dex".
- `falsifier_Neff` : value=4.44, method="participation_ratio (L498)", naive_count=6.
- `combined_significance` : value=8.87, scope="all 6, ρ-corrected", active5=9.95, naive=11.25.

### 3.6 figures / tables 갱신

- §6 forecast 표: 6-row (DESI/Euclid/CMB-S4/ET/LSST/SKA) → 6-row + correlation matrix subtable + N_eff row.
- §4.1 RAR figure: a₀ point estimate 만 → a₀ ± [0.7, 1.6] box (factor-1.5 invariance) + M16-한정 1.07 marker.

### 3.7 CLAUDE.md 신규 재발방지 — 권고

본 종합이 발견한 *반복 가능* 함정 2건:

- "L500-L504 식 *미실행 슬롯* 에 가짜 결과 가정해 종합 시도 금지 — 디스크 검증 우선." (L499 의 L491-L498 부재 보고와 동질).
- "PASS_STRONG candidate 는 *invariance audit* 통과 전까지 'candidate' 표기 의무. ν-form / Υ★ / cuts 변동 spread 가 σ_stat 의 ≥3× 인 claim 은 자동 PASS_MODERATE."

---

## 4. Round 3 권고 (다음 5 loop)

L499 §6 예약 슬롯 + L497 §7 + L498 §8 통합. 우선순위 *최상* 표기 4건 + 추가 1건:

| Slot | 임무 | 우선순위 | 목적 |
|------|------|----------|------|
| **L502** | **L482 PASS_MODERATE 8인 K-범위 재검증 + K_R6 (cross-form \|Δlog a₀\| ≤ 0.04) 신규 도입** | **최상** | 본 §2.2 격하 확정의 *팀 합의* 절차 (Rule-A 8인). |
| **L503** | **cluster RAR 독립 재현 (A5 독립 채널 1)** | **최상** | RAR PASS_MODERATE → PASS_STRONG 격상의 *핵심* 채널. 11 anchor 중 cluster scale 직접. |
| **L504** | **dwarf galaxy RAR 독립 재현 (A5 독립 채널 2)** | **최상** | 독립 채널 2. low-mass deep-MOND limit 직접 test. |
| L505 (본 문서) | Phase 2 종합 — 격하 확정 + paper plan | (완료) | — |
| L506 | low-z FRB DM-z 채널 (A5 독립 채널 3) | 상 | 독립 채널 3. 비-갈락틱-동역학 채널. |
| L507 | hidden DOF (Υ★+H₀+cut) explicit AICc penalty 재계산 | **최상** | L499 §4 effective k≈3 정량화. ΔAICc 부호 확정. |
| L508 | OSF DOI 등록 + arXiv timestamp 잠금 (P22 / P16 pre-reg) | 상 | L499 L492 슬롯 승계. |
| L509 | Bayesian per-galaxy Υ marginalization (Li+18) | 중 | L497 §7-3 — Υ-axis systematic 분리. |
| L510 | L448 V_flat 정의 변경 재계산 (outermost RAR fit) | 중 | L497 §7-4 — BTFR 채널 부활 가능성. |

**핵심 4건 (L502/L503/L504/L507)** 통과 시 RAR 의 PASS_MODERATE → PASS_STRONG 격상 가능. 통과 실패 시 paper §4.1 에 "PASS_MODERATE 영구" 기록.

---

## 5. CLAUDE.md 정합성 체크

- **결과 왜곡 금지**: PASS_STRONG → PASS_MODERATE 격하 정직 기록. L500-L504 부재 정직 인정. ✓
- **[최우선-1] 방향만 제공, 지도 금지**: 본 문서 신규 수식 0줄, 신규 파라미터 0개, 새 이론 형태 0건. ✓
- **[최우선-2] 팀 독립**: 본 문서는 카탈로그/verdict only. 격하 *최종* 절차는 L502 8인 라운드. ✓
- **paper/base.md 직접 수정 금지**: §3 update plan 은 *권고*, edit 0건. ✓
- **L6 8인/4인 규칙**: PASS_STRONG → PASS_MODERATE 격하 (이론 클레임) → Rule-A 8인 라운드 필수. 본 문서는 *전 단계* 메타-합성. ✓

---

## 6. 한 줄 종합

**Phase 2 의 5 loop 중 실재 산출물은 L497/L498/L499 3건 (L500-L504 디렉터리는 빈/부재) ; 이 3건의 합의는 (i) L482 RAR PASS_STRONG candidate → **PASS_MODERATE 격하** 확정 (M16+Υcanonical 한정 ; effective k≈3 hidden DOF ; ν-form spread 0.064 dex), (ii) factor-≤1.5 a₀ invariance 만 PASS_STRONG 보존 (sub-row 분리), (iii) 6 falsifier headline 은 N_eff=4.44 / 8.87σ 로 격하 ; Round 3 우선순위 4건 = L502 8인 K-재검증 + L503 cluster RAR + L504 dwarf RAR + L507 explicit hidden DOF penalty 통과 시에만 PASS_STRONG 격상 가능.**

---

*저장: 2026-05-01. results/L505/PHASE2_SYNTHESIS.md. 단일 메타-합성, 8인/4인 라운드 미실행. paper/base.md edit 0건. simulations/ 신규 코드 0줄. CLAUDE.md [최우선-1]·[최우선-2]·결과 왜곡 금지 정합.*
