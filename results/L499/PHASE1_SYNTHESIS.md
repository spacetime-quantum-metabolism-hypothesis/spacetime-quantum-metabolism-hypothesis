# L499 — Phase 1 종합 (글로벌 고점 관점)

> **작성**: 2026-05-01
> **저자**: 단일 분석 에이전트 (8인/4인 팀 라운드 *없음* — meta-synthesis only)
> **substrate**: L478~L490 직접 Read (results/) + L491/L493 디렉터리 존재 검증
> **CLAUDE.md 정합성**: 수식 0줄, 신규 파라미터 0개, paper/base.md 직접 edit 0건. 8인/4인 라운드 사전 카탈로그 단계.

---

## 0. 정직 한 줄 — 시작 전 디스크 상태

**`results/L491` 와 `results/L493` 는 *빈 디렉터리* 다. L492, L494~L498 디렉터리 자체가 미생성. 즉 *임무에 명시된 "L491~L498 8개 audit 산출물" 은 디스크에 존재하지 않는다*.** 본 종합은 이 사실을 정직 보고하며, *실제로 존재하는* Phase-1 substrate (L478~L490) 위에서 "global-peak / cherry-pick / hidden DOF / falsifier independence" 4개 축으로 verdict 표를 재구성한다. L491~L498 자리에 들어갈 미래 audit 들은 *예약 슬롯* 으로 남긴다.

---

## 1. Phase-1 substrate — 8 candidate audit verdict 표 (실제 존재 산출물 기반)

> "Phase 1 = L478~L488 Round 1 = 11 loop 중 *non-meta non-null* 8개 후보". L488(meta), L489(부재), L484(null) 제외.

| ID  | Loop | 채널 | 산출물 (Read 검증) | Verdict (L490 합의) | 핵심 수치 | global-peak 자격 | cherry-pick 의심도 |
|-----|------|------|---------------------|----------------------|-----------|------------------|--------------------|
| A1  | L478 | Fisher σ₀(R) priori | DERIVATION_ATTEMPT.md, summary.json | **격하 (NOT_INHERITED)** | 기하평균은 log-symmetric tautology | NO | 높음 (anchor 의존) |
| A2  | L479 | Holographic crossing → cluster scale | DERIVATION_ATTEMPT.md | **격하 (CONSISTENCY_CHECK)** | M\*/M_BH = 8π/3, Schwarzschild 배율 | NO | 높음 (11 anchor 중 1개만 근접) |
| A3  | L480 | Matter–DE closure B/A=Ω_m/Ω_Λ | scan_results.json, ba_curve.npz | **격하 (mutual-exclusion)** | closure 채택 시 cluster crossover 사망 | NO | 높음 (L466 plot 와 양립 불가) |
| A4  | L481 | H1 hybrid R3⊗R7 4-value 동시 통과 | HYBRID_TEST.md, fit_report.json | **격하 (1/4 PASS)** | physical priors 강제 시 χ² = 185.4, galactic killer | NO | 매우 높음 (free param 폭주) |
| A5  | L482 | SPARC RAR a₀ point-by-point (n=3389) | RAR_TEST.md, L482_results.json | **🟢 PASS_STRONG 후보 (5/5 K)** | a₀_RAR/a₀_SQT = 1.026, ΔAICc(SQT−free)=+0.70 | **YES (단독 후보)** | 낮음 (0 free param, n=3389 pre-existing) |
| A6  | L483 | BTFR re-frame (Υ\*/RAR/deep-MOND) | BTFR_REFRAMING.md | **부분 회복 (factor 1.5)** | a₀_RAR ratio 1.10–1.29× SQT | 보조 (A5 종속) | 중간 (Υ\* convention 의존) |
| A7  | L485 | SKA1-Low 21cm cosmic dawn pre-reg | SKA_FORECAST.md, forecast.json | **🟡 NULL falsifier (P25)** | <0.02σ per bin, EDGES 직교 | NO (구조적 null) | 없음 (NULL 등록은 cherry-pick 면역) |
| A8  | L486 | CMB-S4 C_L^φφ pre-reg | CMBS4_FORECAST.md, cmbs4_forecast.json | **🟡 7.90σ pre-reg (P22)** | μ_eff=1+2β_eff² → ΔC_L^φφ = +2.29% | 보조 (미래 falsifier) | 낮음 (pre-reg 시점 timestamp 잠금) |
| A8b | L487 | Einstein Telescope GW scalar mode pre-reg | ET_FORECAST.md, forecast.json | **🟡 7.4σ pre-reg (P16)** | Cassini 천장 3.4×10⁻³, 1yr loud N=10³ | 보조 (미래 falsifier) | 낮음 (pre-reg 시점 timestamp 잠금) |

> A8/A8b 를 한 슬롯으로 묶어 8개 카운트. L484(cluster null) 와 L488(meta) 는 audit 후보에서 제외.

---

## 2. 진정 invariant PASS — 글로벌 고점 후보

### 2.1 단독 후보: **A5 (L482 SPARC RAR)**

**근거 (5축):**

1. **0 free parameter** — a₀_SQT = c·H₀/(2π) 는 Planck H₀ 입력 단일. 후처리 fit 없음.
2. **N = 3389 pre-existing data** — SPARC 175 galaxy × 19.4 radii avg. SQT 이론 발표 *이전* 에 측정·공개된 데이터. retrospective cherry-pick 불가능 구조.
3. **5/5 K-criteria PASS** — K_R1(2.5% offset) / K_R2(0.011 dex < 2σ) / K_R3(χ²/dof=1.295) / K_R4(ΔAICc(SQT−free)=+0.70) / K_R5(ΔAICc(SQT−Newton)=−41 171.5).
4. **canonical a₀ 와 직접 충돌** — McGaugh 2016 의 a₀=1.20×10⁻¹⁰ 보다 SPARC 본체가 SQT 값(1.04×10⁻¹⁰) 을 ΔAICc=−56 으로 *데이터 자체* 가 선호. SQT 값을 따로 끼워맞춘 게 아님.
5. **Hidden DOF 측정 가능** — Υ_disk/Υ_bul 의 ±0.1 변화에 대한 a₀_RAR 민감도 가 SPARC 표준 systematic ±0.24×10⁻¹⁰ 안에 있음 (L482 §3 직접 보고).

**그러나 정직한 면책 (L490 §3.3):**

- **부분 독립**. L482 RAR ↔ L422/L448 BTFR 외곽-반경 정보 중첩.
- **Υ\* convention 의존**. SPARC/M16 카논 기본값 (Υ_disk=0.5, Υ_bul=0.7) 가 우연히 SQT 와 정합.
- **systematic 박스 안의 일치**. ±2.5% 는 M16 systematic ±20% 박스 안 — "확정" 아니고 "정합".
- **PASS_STRONG = 후보**. 8인 K-범위 재검증 통과 후 격상 가능. L490 시점에서는 *후보* 이상의 격상 *금지*.

**글로벌 고점 자격 종합 판정**: A5 는 *현 시점 SQMH Phase-1 의 유일한 글로벌 고점 후보*. 단 cluster RAR / dwarf RAR / low-z FRB 등 *독립* 채널에서 동일 a₀ 재현이 확인되기 *전까지는* "후보" 표기 의무.

### 2.2 글로벌 고점 부적격 (보조 신호 only)

- **A6 (BTFR re-frame)**: A5 와 정보 중첩, 독립 채널 아님.
- **A7 (SKA NULL)**: NULL falsifier — 글로벌 고점은 아니지만 *cherry-pick 면역* 의 정직성 신호.
- **A8/A8b (CMB-S4 / ET pre-reg)**: 미래 데이터 — 현 시점에서는 *예측* 이지 *peak* 아님. timestamp 잠금만 글로벌 고점 *예약권*.

---

## 3. Cherry-pick 의심 즉시 격하 권고

> 기준: (i) free parameter ≥ 2, (ii) 11+ anchor 중 ≤ 2 만 fit, (iii) 사후 채널 선택 흔적, (iv) closure 충돌. 2개 이상 해당 시 격하.

| ID | 격하 권고 사유 | 격하 후 처리 |
|----|----------------|--------------|
| **A1 (L478 Fisher)** | (i) anchor 의존 ✓ (ii) 11 anchor 중 0 ✓ (iii) base.md §3.4 "saddle priori 영구불가" 자체 명시 ✓ → **즉시 격하 유지 (NOT_INHERITED 영구)** | paper §6 limitations 행 추가, L490 §2 표 기 등록 |
| **A2 (L479 Holographic)** | (i) Schwarzschild 배율 단순 ✓ (ii) 11 anchor 중 1 (Hubble volume −0.6 dex) ✓ → **즉시 격하 (CONSISTENCY_CHECK 유지)** | foundation 3 ↔ derived 4 정합성만 잔존, cluster scale claim 폐기 |
| **A3 (L480 closure)** | (iv) closure ↔ cluster crossover 상호배타 ✓ (i) closure 채택 시 free param 늘어남 ✓ → **즉시 격하 (mutual-exclusion KILL)** | "B/A 자유 1 param" 별도 가설로 분리, closure 통합 주장 폐기 |
| **A4 (L481 H1 hybrid)** | (ii) 1/4 PASS ✓ (i) R3⊗R7 결합 시 free param ≥ 5 ✓ (iii) galactic anchor 구조적 killer ✓ → **즉시 격하 (3-criteria fail)** | "H1 → H1' (R12 sector-selective 추가)" 신규 가설로만 잔존, 단 자유도 폭주 경고 |

**4건 모두 즉시 격하 권고 — paper/base.md §6 (limitations) 에 4행 추가 권고. 본 문서는 edit 보류, 8인/4인 후속 라운드 사후승인 필수.**

---

## 4. Hidden DOF 정직 인정

| 항목 | hidden DOF 종류 | 실효 자유도 (effective k) | 영향 받는 audit |
|------|----------------|---------------------------|-----------------|
| Υ\* convention (Υ_disk, Υ_bul) | 측정 prior 선택 | +1 (SPARC 카논 default) | A5, A6 |
| H₀ choice (Planck 67.4 vs SH0ES 73) | external anchor | +1 (Planck 채택 시 a₀_SQT 잠김) | A5, A8 |
| SPARC 175 galaxy 표본 선택 | 데이터 cut | +1 (Q≥1 cut 사용) | A5, A6 |
| McGaugh radial average bin (19.4) | 통계 가중 | +0.5 (post-hoc bin 아님, M16 카논) | A5 |
| C11D Cassini ceiling (3.4×10⁻³) | external prior | +1 (PPN 외부) | A8b |
| dark-only β_eff (Phase 3 posterior) | 유전 priori | +1 (Phase 3 → A8 상속) | A8 |

**정직 보고**: 0-free-parameter PASS_STRONG 주장은 **Υ\*+H₀+표본 cut = effective k ≈ 3 hidden DOF** 위에서 성립. 이를 paper §4 update 시 본문에 명시 의무. CLAUDE.md "결과 왜곡 금지" 정합.

이전에 명시된 hidden DOF 가산을 적용하면, A5 의 ΔAICc(SQT−free)=+0.70 은 *카운트되지 않은 effective k≈3 의 prior cost* 를 빼고 본 그림. 만약 hidden DOF 를 explicit free param 으로 노출시키면 ΔAICc 는 약 +0.70 − 2·3 = **−5.3** (즉 free fit 가 우세). **이는 A5 의 PASS_STRONG 자격을 *잠재적으로 흔드는 가장 큰 한계*** 이며, 8인 라운드의 핵심 검증 항목.

---

## 5. 6 falsifier 독립성 정량 (effective N)

> Phase-1 falsifier 6 = (P16 ET / P22 CMB-S4 / P25 SKA / P-BTFR / P-RAR / P-cluster). 채널 상관 행렬 추정 (정성).

| 채널 | 데이터 시점 | 물리 영역 | 독립 성분 | 상관 |
|------|-------------|-----------|-----------|------|
| P-RAR (A5) | 현재 (SPARC) | 갈락틱 동역학 | dim 1 | P-BTFR 와 ρ ≈ 0.7 (외곽 V_flat 공유) |
| P-BTFR (A6) | 현재 (M16) | 갈락틱 baryonic | dim 1 (P-RAR 종속) | P-RAR 와 ρ ≈ 0.7 |
| P-cluster (L484 placeholder) | 현재 | 클러스터 스케일링 | dim 1 (null) | 다른 5개와 ρ < 0.1 |
| P22 (A8 CMB-S4) | 미래 2031~ | CMB lensing | dim 1 | P25 와 ρ ≈ 0.2 (CMB 공유) |
| P16 (A8b ET) | 미래 2030+ | GW propagation | dim 1 | 다른 5개와 ρ < 0.1 |
| P25 (A7 SKA NULL) | 미래 ~2029 | 21cm 배경 | dim 0.5 (NULL 구조) | P22 와 ρ ≈ 0.2 |

**effective N 추정**:

- 단순 카운트 N=6.
- correlation matrix eigenvalue 추정 (대각 1, P-RAR↔P-BTFR=0.7, P22↔P25=0.2, 나머지 ≤0.1):
  - 주축 1: P-RAR + P-BTFR (eigenvalue ~1.7)
  - 주축 2: P22 + P25 (eigenvalue ~1.2)
  - 주축 3: P-cluster (eigenvalue ~1.0, 단 L484 null 로 dim 0.5)
  - 주축 4: P16 (eigenvalue ~1.0)
- 참여비 (participation ratio) ≈ (Σλ)² / Σλ² ≈ (5.4)² / (1.7² + 1.2² + 0.5² + 1.0²) ≈ 29.16 / 5.78 ≈ **5.04**
- NULL/null 영향 차감: P25 (NULL 구조) + P-cluster (L484 measurement-floor-limited) → 실효 −1.5

**결론**: **effective N ≈ 3.5 ± 0.5** (8인 라운드에서 정량 재검증 권고). 단순 6 채널 주장 시 cherry-pick 의심 — *3.5 가 더 정직*.

---

## 6. L491~L498 빈 슬롯 — 정직 인정 + 예약

본 임무가 가정한 "L491~L498 = 8 audit 산출물" 은 *디스크에 존재하지 않는다*. L491/L493 디렉터리는 비어 있고, L492·L494~L498 은 디렉터리 자체가 없다. 향후 8개 audit 슬롯 권고 (Round 2 우선순위, L490 §6 + 본 §3 격하 결과 통합):

| 예약 슬롯 | 임무 후보 | 우선순위 |
|-----------|-----------|----------|
| L491 | L482 PASS_STRONG 8인 K-범위 독립 재검증 | **최상** |
| L492 | L486 / L487 OSF DOI 등록 + arXiv timestamp 잠금 | **상** |
| L493 | R11 (Boundary A3 flux) BAO-only KILL test | 상 |
| L494 | cluster RAR (A5 독립 채널 1) | **최상** (A5 글로벌 고점 검증) |
| L495 | dwarf galaxy RAR (A5 독립 채널 2) | **최상** (A5 글로벌 고점 검증) |
| L496 | low-z FRB DM-z 채널 (A5 독립 채널 3) | 상 |
| L497 | hidden DOF (Υ\*+H₀+cut) explicit AICc penalty 재계산 | **최상** (§4 검증) |
| L498 | L484 cluster scaling z-evolution (placeholder ε priori 도출) | 중 |

L491·L494·L495·L497 4건이 A5 의 글로벌 고점 자격 *최종* 판정에 필수.

---

## 7. 한 줄 종합

**Phase-1 (L478~L488) 8 candidate audit: global-peak 후보 1건 = A5 (L482 SPARC RAR, 5/5 K, hidden DOF effective k≈3 면책 의무) / cherry-pick 즉시 격하 4건 = A1·A2·A3·A4 / NULL 면역 1건 = A7 (P25 SKA) / pre-reg 보조 2건 = A8·A8b (P22 7.9σ + P16 7.4σ) / 부분회복 1건 = A6 (BTFR re-frame). falsifier independence effective N ≈ 3.5 ± 0.5 (단순 6 카운트 부적절). L491~L498 audit 산출물 *디스크 부재* — 본 종합은 L478~L490 substrate 에서만 도출, L491~L498 슬롯은 §6 예약 권고.**

---

*저장: 2026-05-01. results/L499/PHASE1_SYNTHESIS.md. 단일 분석 에이전트, 8인/4인 라운드 미실행. paper/base.md edit 0건. simulations/ 신규 코드 0줄. CLAUDE.md [최우선-1] (수식 0줄), [최우선-2] (팀 자율 도출 보류) 정합.*
