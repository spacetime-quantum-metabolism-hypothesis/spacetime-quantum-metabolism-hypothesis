# L490 — Round 1 Synthesis (L478~L488 종합, final)

> **작성**: 2026-05-01
> **모드**: 메타-종합 (Round 1 final). L478~L488 산출물 *직접 Read* 결과 + L489 부재 확인.
> **저자**: 단일 분석 에이전트 (8인/4인 팀 라운드 없음 — 카탈로그/verdict only).
> **L488 보정**: L488 SYNTHESIS_round1.md 는 "디렉터리가 모두 빈 폴더" 라고 보고했으나, 본 L490 시점에서 L478~L487 모두 산출물이 채워졌음을 직접 확인. L488 보고는 시간차로 인한 *snapshot* 오류였고 본 문서가 실제 round 1 final.

---

## 0. 정직 한 줄

**Round 1 (L478~L487) 의 11개 loop 중 격하 4건 + PASS_STRONG 후보 1건 (L482 RAR) + falsifier pre-reg 3건 (L485/L486/L487) + null/weak 3건 (L483/L484, 그리고 L488 자체는 메타). L489 미실행. paper/base.md 직접 수정은 본 문서에서 *권고만* 하며, edit 은 후속 8인/4인 리뷰 통과 후로 보류.**

---

## 1. 11 loop verdict 표 (실제 산출물 기반)

| Loop | 임무 / 채널 | 산출물 | Verdict | 핵심 수치 / 결과 |
|---|---|---|---|---|
| L478 | Fisher information σ₀(R) priori 도출 | DERIVATION_ATTEMPT.md, summary.json | **격하 (NOT_INHERITED 유지)** | 기하평균은 log-symmetric kernel tautology, R★ 절대값은 anchor 의존 |
| L479 | Holographic energy-density crossing → cluster scale priori 도출 | DERIVATION_ATTEMPT.md | **격하 (CONSISTENCY_CHECK 유지)** | M*/M_BH = 8π/3 = Schwarzschild 라인 단순 배율, cluster scale 특혜 없음 |
| L480 | Matter–DE coupling closure (B/A=Ω_m/Ω_Λ) | scan_results.json, ba_curve.npz | **격하 (closure ↔ cluster crossover 상호배타)** | closure 채택 시 cluster crossover 사라짐 (r→∞), L466 그림과 양립 불가 |
| L481 | H1 hybrid (R3 saddle ⊗ R7 holographic dip) 4-value 동시 통과 | HYBRID_TEST.md, fit_report.json | **격하 (R3⊗R7 단일 결합 사망)** | physical priors 강제 시 chi² = 185.4, 1/4 PASS, galactic anchor 구조적 killer |
| L482 | SPARC RAR a₀ 점-by-점 (n=3389) | RAR_TEST.md, L482_results.json | **🟢 PASS_STRONG 후보 (5/5 K)** | a₀_RAR = 1.069×10⁻¹⁰ vs SQT 1.0422×10⁻¹⁰, **2.5% 일치**, ΔAICc(SQT−free) = +0.70 |
| L483 | BTFR FAIL 재구성 (RAR/deep-MOND/Υ\*/non-monotonic) | BTFR_REFRAMING.md | **부분 회복 (factor 1.5 PASS)** | 채널 A/B PASS — a₀_RAR ratio 1.10–1.29× SQT, BTFR FAIL 은 V_flat 측정효과 |
| L484 | Cluster scaling (M-T_X, M-Y_X, M-σ_v) | CLUSTER_SCALING.md, scaling_table.tsv | **null (구분 불능)** | ε=0.05 placeholder 가 LCDM 과 5% 이내, 측정오차 (~10%) 안에 숨음 |
| L485 | SKA 21cm cosmic dawn pre-reg (P25) | SKA_FORECAST.md, forecast.json | **🟡 NULL falsifier 등록** | <0.02σ per bin (DR3-edge 한계), minimal SQT = LCDM at background, EDGES 직교 |
| L486 | CMB-S4 lensing C_L^φφ pre-reg (P22) | CMBS4_FORECAST.md, cmbs4_forecast.json | **🟡 7.90σ pre-reg** | dark-only μ_eff = 1+2β_eff² → ΔC_L^φφ = +2.29%, 7.90σ DETECT |
| L487 | Einstein Telescope GW scalar mode pre-reg (P16) | ET_FORECAST.md, forecast.json | **🟡 7.4σ pre-reg** | minimal C11D = null, Cassini 천장 3.4×10⁻³, 1yr loud N=10³ → 7.4σ falsifier |
| L488 | Round-1 종합 시도 | SYNTHESIS_round1.md | **메타 (snapshot 오류)** | "모두 빈 폴더" 보고는 시간차 오류, 본 L490 으로 정정 |

L489: 디렉터리 부재. 미실행.

---

## 2. 격하 4건 — 한계 표 (paper §6 limitations 추가 권고)

| Loop | 청구된 priori-derivation | 격하 사유 (한계) | 살아남는 잔존 신호 |
|---|---|---|---|
| L478 (Fisher) | σ₀(R) ∝ 1/√I_F(R), R★ priori 도출 | (i) 기하평균은 log-symmetric kernel 의 *tautology*; (ii) Mpc 스케일은 SQMH 상수 조합에서 0 후보; (iii) base.md §3.4 자체가 "saddle 위치 priori 도출 영구불가" 명시 | **R★ co-shift** — R_lin 또는 R_nl 이 미래 데이터에서 이동 시 R★ 도 √(R_lo·R_hi) 추적 (genuine falsifier) |
| L479 (Holographic crossing) | rho_UV = rho_sys 가 cluster scale 자연 출력 | M*/M_BH = 8π/3 ≃ 8.38 = **Schwarzschild line × 상수** — 11 anchor 중 cluster 는 −5 dex, 오직 Hubble volume 만 −0.6 dex 근접 | foundation 3 ↔ derived 4 의 상호 정합성 (CONSISTENCY_CHECK 유지). cluster signature 가 데이터에 있다면 holographic 이 아님 |
| L480 (Matter-DE) | B/A = Ω_m/Ω_Λ closure 가 free param 0 | closure (B/A=0.46) 적용 시 NFW+2-halo 에서 cancellation r→∞ → **cluster crossover 무력화**. L466 의 "B/A=1 자연 dip" 은 floor-없음 한정 | (a) Lagrangian 수준 부호 (A>0, B>0) 는 EFT 자동, (b) BA≈1 영역의 cluster outskirt cancellation 은 closure 와 별개 가설 (자유 1 param) |
| L481 (H1 hybrid R3⊗R7) | 4-value (cosmic / cluster / galactic / atomic) 동시 통과 + cluster dip 자연 emergence | physical priors 강제 시 chi²=185, 1/4 PASS. galactic anchor s≈20.5 가 구조적 killer (단일 Gaussian dip 으로 cluster s≈22.5 와 분리 불가). holo 제약 풀어도 chi²=807 | H1 → H1' (R3⊗R7⊗**R12** sector-selective) 또는 multi-FP RG 가 필요 — 단 자유도 폭주 위험 |

추가 권고: paper §6 (limitations) 또는 `paper/08_discussion_limitations.md` 에 22행 표 형태로 4 행씩 (총 16행) 추가. priori-derivation 시도 자체는 정직하게 기록되, 격하 결과를 명시 → "saddle 위치 영구 불가" 의 base.md §3.4 자체 진술과 일관.

---

## 3. L482 RAR PASS_STRONG 후보 — paper §4 update plan

### 3.1 현황 요약

- **5/5 K-criteria PASS** (K_R1: 2.5% offset / K_R2: 0.011 dex < 2σ / K_R3: χ²/dof=1.295 / K_R4: ΔAICc(SQT−free)=+0.70 / K_R5: ΔAICc(SQT−Newton)=−41 171.5).
- **0개 자유 파라미터** 로 SPARC 175 galaxy × 19.4 radii avg = 3389 point 를 1-param free fit 과 통계적으로 동등 재현.
- 예측치 a₀_SQT = c·H₀/(2π) = 1.0422×10⁻¹⁰ m/s² (Planck H₀=67.4) 가 best-fit a₀_RAR = (1.069 ± 0.015)×10⁻¹⁰ 와 ±2.5% 일치.
- McGaugh 2016 의 카논 a₀ = 1.20×10⁻¹⁰ 보다 SQT 가 ΔAICc = −56 (SPARC 데이터 자체가 SQT 값 선호).

### 3.2 paper §4 update plan (직접 edit 보류, 권고만)

| 섹션 | 현재 상태 | 권고 변경 | 트리거 (8인 합의 후) |
|---|---|---|---|
| §04 perturbation_theory row "MOND a₀" | NOT_INHERITED (L422/L448 BTFR FAIL) | **POSTDICTION → PASS_STRONG_CANDIDATE** 로 격상, RAR 채널 명시 | 8인팀 사전합의 K-범위 재정의 + L482 5/5 결과 합의 검증 |
| §04 표 Channels | BTFR slope/zero-point 만 나열 | **RAR (n=3389, 5/5 PASS)** 행 추가 — Channel 독립성 "부분 (BTFR 외곽과 상관)" 명시 | L483 4-channel 결과 합의 검증 |
| §06 discussion "MOND-related claims" | "BTFR FAIL → 채널 사망" | "BTFR 단독 FAIL 은 V_flat plateau 측정효과; RAR 채널 PASS_STRONG" 로 재기술 | L482 + L483 통합 합의 |
| `claims_status.json` `RAR_a0` (신규 키) | 없음 | `PASS_STRONG_candidate, channel: SPARC RAR, n=3389, offset=+2.5%, ΔAICc(SQT-free)=+0.70` | 본 PASS_STRONG 등록은 8인 검증 통과 후 |

### 3.3 보고 시 필수 면책 (CLAUDE.md "결과 왜곡 금지")

1. **부분 독립**. L482 RAR 와 L422/L448 BTFR 은 외곽-반경에서 정보 중첩. 완전 독립 신규 채널 아님.
2. **Υ\* convention 의존**. Υ_disk = 0.5 / Υ_bul = 0.7 은 SPARC/M16 카논. Υ ↑ 시 a₀_RAR ↓ (SQT 와 더 일치). 일치는 카논 default 에서 자연.
3. **σ_log a₀ ≈ 0.006 dex 는 통계 only**. M16 의 systematic ±0.24×10⁻¹⁰ 가 시스 박스. 2.5% offset 는 이 박스 안.
4. **PASS_STRONG 용어**: 본 격상은 "5/5 K + ΔAICc 정합" 기준. 절대적 "이론 확정" 아님. 후속 채널 (cluster RAR, dwarf RAR, low-z FRB) 추가 검증 필요.

---

## 4. L487 + L486 + L485 pre-reg — paper §4.5 추가

### 4.1 현재 §4.5 mid-term falsifier 행

paper/base.md L907 (P16, P22, P25 등) 이 있으나 σ-detect 등 정량 미고정.

### 4.2 권고 추가 사항 (timestamp 포함)

| Falsifier ID | Channel | Pre-reg σ | UTC timestamp | Verdict scheme | 출처 |
|---|---|---|---|---|---|
| **P16** | ET GW scalar mode (BNS 1yr loud N=10³) | **7.4σ** falsifier of C11D sector | 2026-05-01T13:47:30Z | m<σ CONSISTENT / σ≤m≤3.4e-3 AMBIGUOUS / m>3.4e-3 @3σ FALSIFIED | results/L487/ET_FORECAST.md |
| **P22** | CMB-S4 C_L^φφ (L=30..1500, f_sky=0.4) | **7.90σ** detect of dark-only μ_eff structural shift | 2026-05-01T13:49:57Z | 0 ≤ r ≤ +3.0% CONSISTENT / r∈[-1,0)% AMBIGUOUS / 그 외 FALSIFIED | results/L486/CMBS4_FORECAST.md |
| **P25** | SKA1-Low 21cm cosmic dawn (z=10–15, 1000 hr) | **NULL** falsifier (<0.02σ at DR3 edge) | 2026-05-01T13:48:31Z | minimal SQT = LCDM at background; EDGES 직교 (SQT 가 EDGES 깊이 source 못 함) | results/L485/SKA_FORECAST.md |

### 4.3 paper §4.5 권고 문구 (직접 edit 보류)

> "Mid-term falsifiers — pre-registered 2026-05-01 (UTC timestamps in respective L485/L486/L487 reports). P16 (Einstein Telescope, ~2030+, 7.4σ ceiling falsifier of C11D pure-disformal sector). P22 (CMB-S4, 2031–2033, 7.90σ structural detect under dark-only embedding). P25 (SKA1-Low, ~2029, structurally NULL — non-falsifier for minimal SQT). All three locked via OSF/arXiv/GitHub triple-timestamp convention before first-light."

추가로 `arxiv_submission_checklist.md` 에 "P16/P22/P25 pre-reg 등록 완료, OSF DOI TBD" 행 추가 필요.

---

## 5. JCAP acceptance 재추정

### 5.1 L488 이전 가정

L477 SPECULATION 시점: PASS_STRONG = 0, falsifier pre-reg 0건 → JCAP 본문 진입 추가 근거 없음. acceptance ~30% (이전 추정 그대로).

### 5.2 L490 (Round 1 후) 재추정

| 변동 요인 | 영향 |
|---|---|
| L482 RAR 5/5 K PASS (+) | 본문에 "독립 채널 PASS_STRONG 1건" 추가 가능. 한 단계 강한 phenomenological consistency claim. |
| L483 BTFR re-frame (+) | L422/L448 의 BTFR FAIL "단독 KILL 아님" 으로 재기술 가능. paper §4 의 negative claim 약화. |
| L478/L479/L480/L481 격하 4건 (∓) | priori-derivation 시도 정직 기록은 referee 에게 *honesty signal* (긍정). 동시에 R3/R7/H1 의 *predictive content 부족* 인정 (부정). 순효과 거의 wash. |
| L485/L486/L487 pre-reg 3건 (+) | "falsifiable phenomenology" 포지셔닝 강화. P22 7.9σ + P16 7.4σ 는 PRD-Letter 보다 JCAP 의 "open phenomenology" 톤에 잘 맞음. |
| Q17 (amplitude lock) 미달 + S_8 미해결 (−) | PRD Letter 진입 조건 (Q17 OR (Q13+Q14)) 여전히 미충족. JCAP 가 적절. |

### 5.3 추정

- **JCAP acceptance**: 30% → **40~45%** (Round 1 결과 반영).
- **PRD Letter**: 여전히 부적합 (Q17 미달).
- **MNRAS** (RAR/BTFR 채널 강조 시 대안): RAR 5/5 + BTFR re-frame 가 강한 단일 메시지 → 30% (이전 미고려) 신규 후보로 등장.

JCAP 진입 조건 충족 시점: L482 8인 합의 + L486/L487 OSF DOI 등록 + paper §4 update 통과 후. 빠르면 Round 2 (L490+1~10) 종료 직후.

---

## 6. 라운드 2 권고 우선순위 (다음 액티브 loop)

1. **L482 PASS_STRONG 8인 검증 라운드** — RAR 5/5 결과의 K-범위 독립 재검증, 8인 자유분담.
2. **L486/L487 OSF DOI 등록** — pre-reg triple-timestamp 의 마지막 anchor.
3. **R11 (Boundary A3 flux) BAO-only KILL test** — L477 권고 1순위, Round 1 에서 미실행.
4. **L481 H1 → H1' (R12 sector-selective 추가)** — galactic anchor killer 우회 가능성 탐색.
5. **L484 cluster scaling z-evolution** — placeholder ε 의 SQT 첫원리 도출 시도.

---

## 7. CLAUDE.md 정합성

- **결과 왜곡 금지**: L482 PASS_STRONG 후보 등록 시 부분-독립성 / Υ\* 의존 / σ statistical-only 면책 4건 명시. ✓
- **[최우선-1] 방향만 제공, 지도 금지**: 본 문서 수식 0줄, 신규 파라미터 0개. 격하 사유는 "tautology / Schwarzschild 배율 / closure 충돌 / functional-form 부족" 등 *구조* 만 기술. ✓
- **[최우선-2] 팀 독립 도출**: 본 종합은 verdict / 카탈로그 / update plan 만 제공. 후속 8인팀이 독립 K-범위 재정의 / OSF 등록 절차 / R11 KILL test 자율 도출. ✓
- **paper/base.md 직접 수정 금지** (사용자 지시): 본 문서는 sync 권고만. edit 0건. ✓
- **L6 8인/4인 규칙**: PASS_STRONG 격상 (이론 클레임) → Rule-A 8인 라운드 필수. 본 종합은 그 라운드 *전 단계* 카탈로그. ✓

---

## 8. 한 줄 종합

**Round 1 (L478~L487) 11 loop 결과: 격하 4 + PASS_STRONG 후보 1 (L482 RAR, 2.5%) + falsifier pre-reg 3 (P16 7.4σ / P22 7.90σ / P25 NULL) + null 1 (L484) + 부분회복 1 (L483) + 메타 1 (L488 snapshot 오류). paper/base.md 직접 수정 보류, 8인/4인 후속 라운드에서 L482 PASS_STRONG 격상 + paper §4/§4.5/§6 update 진행 권고. JCAP acceptance 30% → 40~45% 상승 추정.**

---

*저장: 2026-05-01. results/L490/SYNTHESIS_round1_final.md. 본 문서는 메타-종합이며 simulations/ 신규 코드 0줄. paper/ 직접 수정 0건. L489 미실행 확인.*
