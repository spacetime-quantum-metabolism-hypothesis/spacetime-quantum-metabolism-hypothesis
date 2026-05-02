# L511 — Phase 3 종합 (글로벌 고점 관점)

> **작성**: 2026-05-01
> **저자**: 단일 분석 에이전트 (8인/4인 팀 라운드 *없음* — meta-synthesis only)
> **substrate**: 디스크에 *실재하는* L491~L498 audit 8건 직접 Read + L499 Phase-1 종합 cross-ref
> **CLAUDE.md 정합성**: 수식 0줄, 신규 파라미터 0개, paper/base.md 직접 edit 0건. simulations/ 신규 코드 0줄.

---

## 0. 정직 한 줄 — 시작 전 디스크 상태

**임무가 가정한 "results/L506~L510 의 5개 audit 산출물" 은 *디스크에 부재* 한다. `results/L500`~`L505` 는 빈 디렉터리이고, `L506`~`L510`/`L511` 은 디렉터리 자체가 없었다 (본 문서가 L511 을 신규 생성). 따라서 본 Phase-3 종합은 *실제로 존재하는* L491~L498 8건의 audit (RAR 4건 + 메타 4건) 를 Phase-2 substrate 로 재해석하고, L506~L510 5슬롯은 §6 에 *예약 슬롯* 으로 정직 명시한다. 글로벌 고점 결론은 이 substrate 위에서만 도출, 미존재 산출물에서 결과를 발명하지 *않는다*.**

L499 Phase-1 종합도 동일한 구조적 부재 (L491~L498 미생성) 를 만나 예약 슬롯 처리한 선례 — 본 L511 은 그 선례를 따른다.

---

## 1. Phase-3 가용 substrate — 8 audit verdict 표 (L491~L498, 디스크 실재)

> 본 표는 임무 명세의 "5 audit (L506~L510)" 가 아니라, *실재하는* L491~L498 8건을 Phase-3 종합 substrate 로 재구성한 것. RAR 채널 직접 검증 4건 (L491~L494) + 메타-감사 4건 (L495~L498).

| ID | Loop | 채널 / 임무 | 산출물 (Read 검증) | 핵심 verdict | 핵심 수치 | global-peak 영향 |
|----|------|-------------|---------------------|--------------|-----------|------------------|
| B1 | L491 | RAR functional-form 안정성 (7 forms) | RAR_FUNCFORM_AUDIT.md, L491_results.json | **GLOBAL_PARTIAL** | 7-form spread 0.368 dex, IQR 0.167 dex, median−SQT = +0.023 dex (SQT in band) | A5 (L482) 정량 격하 근거 |
| B2 | L492 | RAR cross-dataset (5 subsets) | RAR_DATASET_AUDIT.md, L492_results.json | **단일-dataset 한정 (1/4 PASS)** | spread 0.163 dex; D4 dwarf Δlog = −0.353 dex (×2.3); D2 Q=1 = +0.077 dex | A5 cross-sample 안정성 부정 |
| B3 | L493 | RAR out-of-sample (70/30 split) | OUT_OF_SAMPLE.md, L493_results.json | **5/5 PASS (held-out)** | χ²/dof_test_SQT = 1.283; |Δχ²/dof|_test−train = 0.016; ΔAICc(SQT−Newton) = −15974 | A5 hold-out robustness 강화 |
| B4 | L494 | RAR null-mock false-positive | MOCK_FALSE_RATE.md, L494_summary.json | **0/200 (Newton-null)** = FP < 1% per form, 0/1000 joint; positive control 100% recover | A5 cherry-pick 면역 강화 |
| B5 | L495 | Hidden DOF audit (paper 전체) | HIDDEN_DOF_AUDIT.md | **9 (보수) ~ 13 (확장) hidden DOF** | 함수형 1 + anchor 3 + Υ★ 1 + B1 1 + 3-regime 2 + axiom-scale 1 ≥ 9; TABLES.md row 1 의 5 카운트의 ~2배 | "0 free param" 광고 영구 정정 의무 |
| B6 | L496 | 8 anchor leave-one-out (글로벌 CV) | GLOBAL_CV.md, L496_results.json | **단일 anchor 의존 없음** | max\|Δpass-rate\| = 0.089 < fair-share 0.125; full-set strict PASS = 5/8 | A5 단독 의존 부정, 분산 OK |
| B7 | L497 | Invariance audit (5 분석축) | INVARIANTS.md | **진정 invariant 2건 (C1, C7)** | 정량 a₀=1.04±0.02 / 5/5 K / ΔAICc=−56 모두 PASS_MODERATE / PARTIAL 격하 권고 | A5 정량 claim 격하, factor-≤1.5 만 PASS_STRONG |
| B8 | L498 | 6 falsifier 독립성 (effective N) | FALSIFIER_INDEPENDENCE.md, l498_results.json | **N_eff = 4.44 (참여비) ~ 5.0 (Li-Ji)** | Euclid↔LSST ρ=0.80 / DESI↔Euclid ρ=0.54 / 결합 Z = 8.87σ (보정) vs 11.25σ (naive) | "6 독립 falsifier" 광고 over-count |

> Phase-1 (L499 표) 과의 차이: Phase-1 은 *후보 도출* 8개 audit, Phase-3 substrate 는 *후보 검증* 8개 audit. Phase-1 의 A5(L482) 단독 글로벌 고점 후보가 Phase-3 의 B1~B7 7개 audit 에서 *4 방향* (functional-form / dataset / hidden DOF / invariance) 으로 격하 압력 + 3 방향 (out-of-sample / mock-FP / leave-one-out) 으로 강화 압력 을 받는다.

---

## 2. RAR PASS_STRONG (L491~L494) vs 다른 PASS (L495~L498) — global robustness 비교

> 비교 축 4 개: (i) cherry-pick 면역, (ii) hidden DOF 노출, (iii) cross-channel 상관, (iv) invariance.

| Audit | (i) cherry-pick 면역 | (ii) hidden DOF | (iii) cross-channel | (iv) invariance | 종합 robustness |
|-------|----------------------|-----------------|---------------------|-----------------|-----------------|
| **B1 RAR functional-form** | 중 (7 form 중 M16 cherry 가능) | M16 선택 = +1 hidden | RAR 단일채널 | factor-≤1.5 invariant, 정량 NOT | **MED-LO** |
| **B2 RAR cross-dataset** | 낮음 (D1 full 이 sample 평균 우연) | Q-cut + Υ★ = +2 hidden | SPARC 단일 catalog | 단일 dataset, 부분표본 fail | **LO** |
| **B3 RAR out-of-sample** | **높음** (70/30 split, train 안 본 53 galaxy) | seed 의존 1 (확인 완료) | SPARC 내부 split | 5/5 K 유지 | **HI** |
| **B4 RAR null-mock** | **매우 높음** (0/1000 FP) | 0 (구조적 null injection) | 5 functional form × 200 mock | structural | **HI** |
| **B5 hidden-DOF audit** | (메타) | **9~13 자체 카탈로그** | paper 전체 cross-cut | 카운트 자체가 invariance 측정 | **메타-HI (정직성)** |
| **B6 anchor LOO** | **매우 높음** (단일 anchor 의존 부정) | shared param map 명시 | 8 anchor cross | max ΔPR = 0.089 | **HI** |
| **B7 5-axis invariance** | (메타) | 분석축 5개 명시 | RAR / BTFR / 4-channel | 진정 invariant 2건만 통과 | **메타-HI (격하 권고)** |
| **B8 falsifier indep** | 높음 (correlation matrix 정량) | observable basis 8 명시 | 6 미래 채널 cross | ρ-corrected Z = 8.87σ | **HI (forecast)** |

### 2.1 RAR (L491~L494) 종합

- **강 (B3+B4)**: out-of-sample 5/5 + null-mock 0/1000 → "L482 5/5 K 가 우연이 아닐 통계적 증거" 가 **확보**.
- **약 (B1+B2)**: functional-form spread 0.37 dex full / 0.17 dex IQR + 단일-dataset 한정 (D4 dwarf 2.3× off) → "정량 2.5% offset / 0.006 dex tightness" 는 **확보 안 됨**.
- **net**: A5 의 *order-of-magnitude / factor-≤1.5* 일치는 **글로벌**, 정량 (5/5 K, ΔAICc=−56) 은 **M16+canonical 한정**.

### 2.2 다른 PASS (L495~L498) — Phase-3 메타 결론

- **B5 (hidden DOF)**: paper "0 free parameter" 광고는 *부정확*. abstract / intro / appendix / l5_*_interpretation / arxiv_checklist 5개 위치 drift 상태. TABLES.md row 1 + §6.5(e) 가 이미 자체 정정.
- **B6 (anchor LOO)**: 8 anchor 어느 것도 단일 의존 없음 → *글로벌 일관*, 단 PARTIAL 3건 (Bullet/cosmic/cluster) 은 strict score 가 0 가공 → caveat 필수.
- **B7 (5-axis invariance)**: 진정 PASS_STRONG = C1 (factor-≤1.5) + C7 (Newton-only fail) 단 둘. 나머지 정량 claim 6건 격하.
- **B8 (falsifier indep)**: 6 → N_eff 4.44, "11+σ combined" → 8.87σ ρ-corrected. CMB-S4 / ET / SKA 3 채널만 진정 직교.

### 2.3 RAR vs 메타 — 글로벌 robustness 등급

| 기준 | RAR (B1~B4 평균) | 메타 (B5~B8 평균) | 결론 |
|------|-------------------|-------------------|------|
| 통계 strength | ΔAICc(SQT−Newton) = −15974 (held-out) | N/A (메타) | RAR 강 |
| cherry-pick 면역 | B4 0/1000 → 매우 강 | B5 카탈로그 → 정직 | 양쪽 수용 |
| hidden DOF | M16+Υ+H₀+cut = 4 노출 (B5 카운트) | 9~13 (paper 전체) | 메타 > RAR (전체 노출) |
| invariance | factor-≤1.5 만 진정 (B7 C1) | 5축 cross-cut | 메타 > RAR (분석축 모두) |
| 글로벌 등급 | **factor-≤1.5: PASS_STRONG / 정량: PASS_MODERATE** | **메타 정직성: 자체-자인 OK / 광고 drift: 격하 권고** | — |

**한 줄**: RAR (A5/L482) 의 *order-of-magnitude* 는 4 방향 (B1/B2/B3/B4) 모두에서 살아남지만, *정량* 은 B1/B2/B7 3 방향에서 격하. 메타 4건 (B5~B8) 은 paper 의 *광고 톤* 자체를 PASS_STRONG → PASS_MODERATE 로 격하시키는 *횡적* 압력.

---

## 3. *진정 invariant* PASS 후보 final list

> **기준**: (a) functional-form 변경 invariant, (b) dataset 변경 invariant, (c) hold-out test PASS, (d) null-mock FP < 1%, (e) hidden DOF explicit penalty 후 ΔAICc 양호, (f) 5-axis L497 invariance PASS, (g) leave-one-out anchor 의존 < fair-share. 7 기준 중 ≥ 5 PASS = 진정 invariant.

| 후보 | (a) form | (b) data | (c) OOS | (d) FP | (e) hid-DOF | (f) 5-axis | (g) LOO | PASS 카운트 | **격상 결정** |
|------|----------|----------|---------|--------|-------------|------------|---------|-------------|---------------|
| **C1: a₀ ~ c·H₀/(2π) factor-≤1.5** | ✓ (B1 IQR 0.17 dex < 1.5×) | ✓ (B2 spread 0.16 dex < 1.5×) | ✓ (B3 5/5) | ✓ (B4 0/1000) | △ (B5 +4 노출) | ✓ (B7 C1) | ✓ (B6 max ΔPR 0.089) | **6/7 (△ 1)** | **PASS_STRONG (진정 invariant)** |
| C7: Newton-only SPARC fail | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | (해당없음) | **6/6** | **PASS_STRONG (단, 1970s pre-existing fact, 정보량 낮음)** |
| L482 정량 a₀ = (1.07±0.02) ×10⁻¹⁰ | ✗ (B1 7-form 16% spread) | ✗ (B2 D4 ×2.3) | ✓ (B3) | ✓ (B4) | ✗ (B5 +4) | ✗ (B7 C2 PASS_MODERATE) | ✓ (B6) | 3/7 | **PASS_MODERATE (M16+canonical 한정)** |
| 5/5 K-criteria PASS | ✗ (B1) | ✗ (B2) | ✓ (B3) | ✓ (B4) | ✗ (B5) | ✗ (B7 C3) | ✓ (B6) | 3/7 | **PASS_MODERATE → PARTIAL** |
| ΔAICc(SQT−McGaugh) = −56 | ✗ (B1 standard-μ 부호 반전) | △ (B2) | (B3 미해당) | (B4 미해당) | ✗ (B5 form 1 hidden) | ✗ (B7 C5) | (B6 미해당) | 0/4-applicable | **PARTIAL (cherry-pick risk)** |
| BBN ΔN_eff PASS_STRONG (claims_status) | (해당없음) | (해당없음) | (해당없음) | (해당없음) | ✗ (B5 η_Z2 stipulated) | (B7 미커버) | ✓ (B6 max ΔPR 0.089 시 LOO 안정) | 1/2-applicable | **PASS (메타 영향 없음)** |
| Cassini PPN PASS_STRONG | (동) | (동) | (동) | (동) | ✗ (β_eff = Λ_UV/M_Pl 선택) | (동) | ✓ (B6) | 1/2 | **PASS** |
| EP / GW170817 PASS | (동) | (동) | (동) | (동) | ✗ (dark-only embedding 선택) | (동) | △ (B6 §6 single-source param) | 0.5/2 | **PASS_MODERATE** (embedding 의존) |

### 3.1 진정 invariant final list

**오직 두 개 (Phase-1 L499 §2.1 결론과 동일, Phase-3 가 7-기준 검증으로 재확정):**

1. **C1 — a₀_RAR ↔ c·H₀/(2π) 의 factor-≤1.5 / order-of-magnitude 일치** (PASS_STRONG, 6/7 기준)
   - hidden DOF △ 만 미점, 나머지 6 기준 모두 PASS.
   - 단 "factor-≤1.5" 한정 — 정량 2.5% offset 은 별도 PASS_MODERATE.
2. **C7 — Newton-only SPARC RAR 재현 불가** (PASS_STRONG, 6/6 기준)
   - 정보량은 낮으나 (pre-existing fact) invariance 는 완벽.

### 3.2 부분 invariant (PASS / PASS_MODERATE)

- BBN ΔN_eff (B6 LOO 통과, B5 η_Z2 hidden DOF 1 — embedding 의존)
- Cassini PPN (동)
- EP / GW170817 (dark-only embedding 의존, B5 +1 hidden)
- L483 BTFR re-frame factor 1.5 (PASS_MODERATE 유지, B7 C8 mostly invariant)
- Branch B 3-regime σ_0 spectrum (PASS_MODERATE → PARTIAL, B7 C9: smooth quadratic 동률)

### 3.3 주의: hidden DOF 명시적 패널티 적용 시

L499 §4 가 이미 지적했듯, A5 의 ΔAICc(SQT−free) = +0.70 은 effective k ≈ 3 hidden DOF (Υ★ + H₀ choice + sample cut) 를 *카운트하지 않은* 값. explicit penalty 적용 시 ΔAICc ≈ +0.70 − 2·3 = **−5.3** 로 free-fit 우세. **따라서 진정 invariant final list 의 C1 도 "factor-≤1.5" 한정에서만 PASS_STRONG**, 정량 claim 은 hidden DOF 이후 PASS_MODERATE 로 자동 격하. 이 점이 Phase-3 의 가장 중요한 정직 결론.

---

## 4. Cherry-pick 의심 격하 final list

> **격하 기준** (L499 §3 의 (i)~(iv) 에 Phase-3 추가 기준 (v) hidden DOF ≥2 (vi) cross-form / dataset 흔들림 ≥0.10 dex (vii) 5-axis invariance NOT 추가):

| Claim | 격하 사유 (Phase-3 추가) | 권고 격하 |
|-------|----------------------------|------------|
| **L482 정량 2.5% offset (a₀ = 1.07×10⁻¹⁰)** | (vi) B1 form spread 0.37 dex / IQR 0.17 dex (vii) B7 C2 NOT invariant (v) B5 +4 hidden (M16+Υ+H₀+cut) | **PASS_STRONG candidate → PASS_MODERATE** |
| **K_R2 σ_log = 0.006 dex (정밀)** | (vi) B1 cross-form sys 0.06 dex 이 stat 0.006 dex 의 10× → 정보량 0 (v) B5 hidden DOF +4 | **PASS_STRONG → PARTIAL** |
| **ΔAICc(SQT−McGaugh) = −56** | B1 standard-μ 채택 시 a₀_fit=1.21 → McGaugh 정답, 부호 반전. (i) form selection 1 free, (vii) B7 C5 NOT | **PASS_STRONG → PARTIAL (cherry-pick risk)** |
| **BTFR slope=4 a priori** | L422/L448 V_flat 정의 systematic, B7 C6 NOT, slope 3.58→3.70 변동 | **FAIL (영구)** (L499 + Phase-3 재확인) |
| **Branch B "uniquely SQT" 3-regime** | B7 C9 smooth quadratic 통계 동률 (parsimony 시 smooth 우선) | **PASS → PASS_MODERATE → PARTIAL** |
| **L482 RAR ⊥ L448 BTFR (독립 채널)** | B7 C8 V_flat 정의 systematic 공유 → NOT INDEPENDENT | **independent → systematics-coupled** |
| **"0 free parameter" 광고 (abstract / intro / appendix / l5_*_interpretation / arxiv_checklist)** | B5 9~13 hidden DOF 카탈로그 → 5위치 drift | **abstract drift 차단 의무** (paper §6.5(e) cross-ref) |
| **"6 독립 falsifier 11+σ"** | B8 N_eff = 4.44, ρ-corrected Z = 8.87σ | **광고 정정**: "5 active + 1 null across N_eff ≈ 4.4, 8.9σ (all) / 9.9σ (active 5)" |
| **A1 L478 Fisher saddle priori** | L499 §3 격하 유지, Phase-3 추가 사유 없음 | **NOT_INHERITED 영구** |
| **A2 L479 Holographic** | L499 §3 격하 유지 | **CONSISTENCY_CHECK 유지, cluster claim 폐기** |
| **A3 L480 closure** | L499 §3 격하 유지 | **mutual-exclusion KILL** |
| **A4 L481 H1 hybrid** | L499 §3 격하 유지 | **3-criteria fail, R12 sector-selective 신가설로만 잔존** |

### 4.1 paper 광고 정정 의무 (B5 + B8 cross-cut)

- `00_abstract.md:8` "zero free background parameters" → "zero *background-parameter extension* beyond ΛCDM, conditional on M16 / Υ★ canonical / 3-regime anchor pick / B1 ansatz" 또는 §6.5(e) cross-ref
- `01_introduction.md:46` "falsifiable zero-parameter predictions" → "zero-parameter *background extension* with 6 pre-registered (N_eff ≈ 4.4) falsifiers"
- `06/07_*.md` "A12/A17 zero-parameter" → "alt-20 representative drift, 14-cluster pick"
- `10_appendix_alt20.md:50` "All twenty have exactly zero free parameters" → "All twenty share canonical drift basis; functional-form pick is itself a hidden DOF (L495)"
- `arxiv_submission_checklist.md:70` "All constants ... zero free params" → "All constants ... data-fit anchors with 9–13 hidden DOF (L495)"

5 위치 모두 8인 라운드에서 정직성 cross-ref 의무.

---

## 5. Hidden DOF 정직 인정 (Phase-1 L499 §4 → Phase-3 갱신)

| 항목 | hidden DOF 종류 | 실효 k | 영향 받는 audit | Phase-1 카운트 | Phase-3 갱신 (B5 기준) |
|------|----------------|--------|-----------------|---------------|----------------------|
| Υ★ (disk, bul) | 측정 prior | +1 | A5, A6, B1, B2 | +1 | +1 (변동 없음) |
| H₀ choice | external anchor | +1 | A5, A8, B1 | +1 | +1 |
| 함수형 ν / μ / M16 | 사후 선택 | +1 | A5, B1 | (Phase-1 누락) | **+1 (B5 신규 카탈로그)** |
| SPARC sample cut | 데이터 cut | +1 | A5, A6, B2 | +1 | +1 |
| McGaugh 19.4 bin | 통계 가중 | +0.5 | A5 | +0.5 | +0.5 |
| C11D Cassini ceiling | external prior | +1 | A8b | +1 | +1 |
| dark-only β_eff | 유전 priori | +1 | A8 | +1 | +1 |
| **anchor 3 (cosmic / cluster / galactic)** | fit point | +3 | A5, B6 | (Phase-1 누락) | **+3 (B5 §2 카탈로그)** |
| **B1 bilinear ansatz** | derived 1 postulate | +1 | A5, B5 | (Phase-1 누락) | **+1 (B5 §2)** |
| **3-regime structure** | parameterization choice | +2 | A6, A7, B6, B7 | (Phase-1 누락) | **+2 (B5 §2)** |
| **axiom-scale stipulation (η_Z2 / Λ_UV / β_eff / dark-only)** | scale choice | +1~+4 | A8, B6 | (Phase-1 누락) | **+1 (보수) ~ +4 (확장)** |

**Phase-1 합계 (L499)**: 5.5
**Phase-3 갱신 (B5 카탈로그)**: **9 (보수) ~ 13 (확장)** — Phase-1 보다 +4~+8 더 노출.

**A5 ΔAICc 보정**:
- Phase-1: ΔAICc(SQT−free) = +0.70 − 2·3 (k≈3) = **−5.3** (free-fit 우세)
- Phase-3: hidden DOF k ≥ 4 (form + Υ + H₀ + cut) → ΔAICc = +0.70 − 8 = **−7.3** (free-fit 더 우세)

→ **A5 의 PASS_STRONG candidate 자격은 hidden DOF explicit 시 자동 격하**. 이는 Phase-3 의 가장 강한 격하 압력. C1 (factor-≤1.5) 만 hidden DOF 보정 후에도 PASS_STRONG 유지 (광범위 박스 안 → invariance 직접 측정).

---

## 6. L500~L510 빈 슬롯 — 정직 인정 + 예약

| 슬롯 | 디스크 상태 | 권고 임무 (Round 3 우선순위) | 우선순위 |
|------|-------------|-----------------------------|----------|
| L500 | empty dir | L482 8인 라운드 K-범위 독립 재검증 (B1+B7 결과 반영) | **최상** |
| L501 | empty dir | cluster RAR (Tian-Ko 2016 재분석, L499 §6 슬롯) | **최상** |
| L502 | empty dir | dwarf RAR (LITTLE THINGS / SHIELD, B2 D4 후속) | **최상** |
| L503 | empty dir | low-z FRB DM-z 채널 (A5 독립 채널 3) | 상 |
| L504 | empty dir | hidden DOF (B5) explicit AICc penalty 재계산 | **최상** |
| L505 | empty dir | abstract drift 차단 + claims_status.json hidden_dof_audit 키 | 상 |
| **L506** | **부재** | OSF DOI 등록 + arXiv timestamp 잠금 (L486/L487 pre-reg) | 상 |
| **L507** | **부재** | Bayesian per-galaxy Υ marginalization (Li+18) | 중 |
| **L508** | **부재** | L448 V_flat 정의 변경 재계산 (outer-only RAR) | 중 |
| **L509** | **부재** | NFW-injected mock null (B4 의 caveat 1) | 상 |
| **L510** | **부재** | falsifier independence 갱신: Euclid-LSST WL block 통합 (B8 §8) | 중 |

**임무 명세의 "L506~L510 5 audit"** 는 위 5 슬롯 (L506~L510) 으로 예약. 8인/4인 라운드에서 우선순위 최종 합의 권고.

---

## 7. 글로벌 고점 final 판정 (Phase-1 + Phase-3 통합)

### 7.1 진정 글로벌 고점

- **C1 (a₀ ~ c·H₀/(2π) factor-≤1.5 invariant)** — Phase-1 (L499 §2.1) 결론을 Phase-3 (B1~B7 7-기준) 가 6/7 기준 PASS 로 재확인. *유일한 진정 글로벌 고점*.
- C7 (Newton-only SPARC fail) — invariance 완벽하나 정보량 낮음, 보조 신호.

### 7.2 Phase-3 추가 강화

- B3 (out-of-sample 5/5) + B4 (null-mock 0/1000) → C1 의 "통계적 우연 가능성" 을 **<1%** 로 압축.
- B6 (anchor LOO) → C1 단독 의존 부정, 8-anchor 평균에서 균형.

### 7.3 Phase-3 추가 격하

- B1 (form spread 0.37 dex) + B2 (D4 dwarf ×2.3) + B5 (hidden DOF 9~13) + B7 (5-axis only 2 invariant) → **정량 claim 4건** (2.5% offset / 5/5 K / σ_log 0.006 / ΔAICc=−56) 모두 PASS_MODERATE 이하.
- B8 (N_eff = 4.44) → "6 독립 falsifier 11+σ" 광고 over-count, 8.87σ 정정.

### 7.4 cherry-pick 즉시 격하 (Phase-3 추가)

- L482 정량 5/5 K → PASS_MODERATE
- ΔAICc(SQT−McGaugh) = −56 → PARTIAL (cherry-pick risk)
- "0 free parameter" 광고 (5 위치) → drift 차단 의무
- "6 독립 falsifier" 광고 → "5 active + 1 null, N_eff ≈ 4.4, 8.9σ" 정정 의무

### 7.5 글로벌 고점 표 (final)

| 후보 | Phase-1 (L499) | Phase-3 (L511) | 최종 |
|------|----------------|----------------|------|
| C1 (factor-≤1.5) | PASS_STRONG candidate (단독) | PASS_STRONG (6/7 기준 확인) | **PASS_STRONG (진정 invariant)** |
| C7 (Newton fail) | (L499 미카운트) | PASS_STRONG (6/6 기준) | **PASS_STRONG (보조)** |
| L482 정량 (2.5% / 5/5 K / ΔAICc=−56) | PASS_STRONG candidate | 격하 (3/7) | **PASS_MODERATE (M16+canonical 한정)** |
| BBN / Cassini | PASS_STRONG | LOO PASS, hidden DOF 노출 | **PASS_STRONG (embedding 의존 명시)** |
| EP / GW170817 | PASS | dark-only embedding 의존 | **PASS_MODERATE** |
| BTFR slope=4 | FAIL | FAIL 재확인 | **FAIL (영구)** |
| Branch B 3-regime "uniquely SQT" | PASS | smooth 동률 | **PARTIAL** |
| Pre-reg falsifier (P16/P22/P25) | 보조 (timestamp 잠금) | N_eff 보정 | **보조 (8.87σ 보정)** |

---

## 8. 한 줄 종합

**Phase-3 의 *실재* substrate 는 L491~L498 8 audit (RAR 4 + 메타 4); 임무 명세의 L506~L510 5 audit 는 디스크 부재 → §6 예약. 글로벌 고점 final list = {C1 (a₀ ~ c·H₀/(2π) factor-≤1.5 invariant, 7-기준 6/7 PASS), C7 (Newton-only SPARC fail, 6/6 PASS, 정보량 낮음)} — 단 둘. cherry-pick 즉시 격하 final list = {L482 정량 2.5%/5/5 K/ΔAICc=−56 → PASS_MODERATE; "0 free parameter" 광고 5 위치 drift; "6 독립 falsifier 11+σ" → 8.87σ 보정; BTFR slope=4; Branch B uniqueness; L482 ⊥ L448 독립성}. hidden DOF 보수 9 ~ 확장 13 (Phase-1 의 5.5 의 ~2배), explicit penalty 시 A5 ΔAICc = −7.3 (free-fit 우세) → 정량 claim 자동 격하. 8인/4인 라운드에서 paper §4.1 RAR row 격하 + abstract drift 차단 + claims_status.json hidden_dof_audit 신규 키 + TABLES.md row 1 5→9 갱신 의무.**

---

*저장: 2026-05-01. results/L511/PHASE3_SYNTHESIS.md. 단일 분석 에이전트, 8인/4인 라운드 미실행. paper/base.md edit 0건. simulations/ 신규 코드 0줄. CLAUDE.md [최우선-1] (수식 0줄), [최우선-2] (팀 자율 도출 보류) 정합. L499 (Phase-1 종합) 의 disk-absence 정직 보고 선례 계승.*
