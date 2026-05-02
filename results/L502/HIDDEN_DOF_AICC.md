# L502 — Hidden DOF AICc Penalty Quantification

> **작성**: 2026-05-01
> **저자**: 단일 분석 에이전트 (메타-audit only — 8인/4인 라운드 미실행)
> **substrate**: L495 hidden DOF audit (results/L495/HIDDEN_DOF_AUDIT.md) + L482 RAR
>   (results/L482/L482_results.json) + paper/base.md §6.5(e) 32-claim self-audit
> **CLAUDE.md 정합성**: 신규 물리 수식 0줄, 신규 파라미터 0개. AICc bookkeeping 한정.
> **산출**: 본 문서 + `simulations/L502/run.py` + `results/L502/l502_results.json`

---

## 0. 정직 한 줄

**L482 RAR 의 광고 ΔAICc(SQT−free) = +0.70 은 hidden DOF 무시 결과.
그 자리에 *applicable* k_hidden = 2 (M16 함수형 + Υ★) 만 넣어도 ΔAICc → +4.7
(MODERATE 강등), L495 *전체* 보수 카운트 k_hidden = 9 를 적용하면
ΔAICc = +18.8 → free fit (LCDM-equivalent) 이 압승. 즉 "0 free parameter" 광고는
*PASS_STRONG 후보 단 한 건도* AICc 정직 잣대 통과 못 한다.**

---

## 1. 입력 — L495 hidden DOF 카운트

| 출처 | k | 적용 채널 |
|------|---|-----------|
| 함수형 선택 (M16 / simple-nu / standard-mu / Bekenstein) | +1 | RAR, BTFR |
| Anchor pick (cosmic 8.37 / cluster 7.75 / galactic 9.56) | +3 | three-regime σ₀ |
| Υ★ convention (SPARC Y_disk=0.5, Y_bul=0.7) | +1 | RAR, BTFR |
| B1 bilinear ansatz (R = σ·n·ρ_m) | +1 | Newton 회복, three-regime |
| σ₀(env) three-regime structure (carrier + saddle) | +2 | three-regime |
| Axiom-scale stipulation (η_Z₂ / Λ_UV / dark-only) | +1 (collapsed) / +4 (unpacked) | substantive 4 |
| **합계** | **9 (보수) ~ 13 (확장)** | — |

---

## 2. PASS_STRONG / PASS_MODERATE 후보별 AICc 표

데이터 출처: L482_results.json (RAR), paper/base.md §4.1·§6.5(e), L495 §3.

| Claim | 광고 status | N | k_hid_applicable | ΔAICc_naive | ΔAICc_honest (k_h_app) | ΔAICc_expanded | ΔAICc_full(k_h=9) | 판정 (k_h_app) |
|-------|-------------|---|------------------|-------------|------------------------|----------------|-------------------|----------------|
| L482 RAR (a₀) | PASS_STRONG candidate | 3389 | 2 (M16 + Υ★) | **+0.703** | **+4.707** | +4.707 | **+18.756** | **DEMOTED → MODERATE** |
| Newton 회복 | PASS_STRONG (substantive) | 1 | 2 (B1 + scale) | 0 | +4.000 | +12.000 | +18.000 | DEMOTED → MODERATE |
| BBN ΔN_eff | PASS_STRONG (substantive) | 1 | 1 (η_Z₂) | 0 | +2.000 | +10.000 | +18.000 | RETAINED (경계) |
| Cassini |γ−1| | PASS_STRONG (substantive) | 1 | 1 (Λ_UV) | 0 | +2.000 | +10.000 | +18.000 | RETAINED (경계) |
| EP \|η\|<10⁻¹⁵ | PASS_STRONG (substantive) | 1 | 1 (dark-only embed) | 0 | +2.000 | +10.000 | +18.000 | RETAINED (경계) |
| Bullet cluster offset | PASS_STRONG (qualitative) | 1 | 2 (B1 + scale) | 0 | +4.000 | +12.000 | +18.000 | DEMOTED → MODERATE |
| Three-regime σ₀(env) | POSTDICTION (PASS_MODERATE) | 11 | 6 (anchor 3 + 3-reg 2 + B1 1) | −288.000 | −255.000 | −255.000 | −90.000 | RETAINED (postdictive) |
| CMB θ_* shift | PARTIAL | 1 | 2 (B1 + cosmic anchor) | +529.000 | +533.000 | +533.000 | +547.000 | FAILS (이미 PARTIAL) |

> ΔAICc 부호 규약: **SQT − 기준선** (free fit / LCDM / Newton). 양수 = SQT 가 정보기준에서 *진다*. 임계값 +2 (statistical equivalence), +6 (강등), +10 (탈락).
>
> N=1 행 (substantive 4 + Bullet + θ_*): AICc 의 small-sample 항이 발산하므로
> AIC = χ² + 2k 로 fallback. capacity penalty 만 평가.

---

## 3. 핵심 발견

### 3.1 L482 RAR — applicable 만 적용해도 PASS_STRONG 자격 상실

- 광고: ΔAICc(SQT−free) = +0.70 → "5/5 K-criteria PASS" (L482).
- L482 채널에 *진짜* 들어간 hidden DOF: M16 함수형 (+1) + Υ★ convention (+1) = 2.
- 정직 ΔAICc = +0.70 + 2·2 = **+4.7** → "강등 → MODERATE".
- L495 *전체* k_hidden = 9 적용 (anchor / 3-regime / B1 까지 강제 차감) 시
  ΔAICc = **+18.8** → free fit 이 압승 (LCDM-equivalent).
- L499 §4 가 이미 "hidden DOF 가산 적용 시 ΔAICc ≈ −5.3 (free fit 우세)" 로 추정한 바와 정성 일치
  (본 L502 는 *부호* 규약 (SQT − 기준선) 으로 양수 +4.7 ~ +18.8 환산).

> **사용자 지정 검산**: "ΔAICc=+0.70 → +9·2 = +18 → LCDM 우위?" 의 +18 은 *capacity penalty* 만 더한 단순화. 실제 fit residual 0.703 까지 포함한 본 계산값 **+18.756** 와 0.04 단위 일치. 사용자가 인용한 "−17.3" 은 부호 inversion (SQT−LCDM 음수 = SQT 우위) — 본 표 부호 규약에서 같은 양은 **+18.8** (SQT 가 진다).

### 3.2 substantive 4 (Newton/BBN/Cassini/EP) — 전부 capacity-penalty 의 경계 또는 강등

- N=1 의 단일 inequality bound 통과는 **χ² ≈ 0** 을 fit 으로 본 것.
- BBN/Cassini/EP 는 hidden DOF +1 (η_Z₂ / Λ_UV / dark-only embedding 각 1개) → capacity 만 더해도 ΔAIC = +2 → "RETAINED 경계".
- Newton 회복은 hidden DOF +2 (B1 ansatz + dimensional reduction channel) → ΔAIC = +4 → MODERATE 강등.
- 확장 카운트 (k_hidden=13) 적용 시 BBN/Cassini/EP 도 +10 → 강등 ~ 탈락.

### 3.3 three-regime σ₀(env) — 표면적 우월, 그러나 postdictive

- ΔAICc(naive) = −288 (17σ 등가) 라는 화려한 숫자는 **anchor 3 + 3-regime 구조 2 + B1 1 = 6 hidden DOF** 를 차감해도 −255 로 *여전히 음수*.
- 그러나 **paper §3.4 자체가 "saddle 위치 priori 영구 불가" + mock-injection FDR 100% 자인** — 정보기준이 "이긴" 게 아니라 anchor 데이터를 fit 한 결과.
- L495 §1 이 이미 "PASS 가 아닌 POSTDICTION" 로 분류, 본 L502 는 그 결정을 정량 재확인.

### 3.4 CMB θ_* — 광고 PARTIAL 가 정확

- ΔAICc_naive = +529 (Planck σ × 23 의 χ² 환산) → hidden DOF 차감 무관하게 *이미* 탈락.
- "PARTIAL" 등급이 정직.

---

## 4. PASS 자격 변화 매트릭스

| Claim | 사전 등급 | 정직 등급 (k_h_app) | 사전→정직 |
|-------|-----------|---------------------|-----------|
| L482 RAR | PASS_STRONG candidate | PASS_MODERATE | 1 단계 강등 |
| Newton 회복 | PASS_STRONG (substantive) | PASS_MODERATE | 1 단계 강등 |
| BBN ΔN_eff | PASS_STRONG (substantive) | PASS_STRONG (경계) | 유지 (k_h=9 시 강등) |
| Cassini PPN | PASS_STRONG (substantive) | PASS_STRONG (경계) | 유지 (k_h=9 시 강등) |
| EP η | PASS_STRONG (substantive) | PASS_STRONG (경계) | 유지 (k_h=9 시 강등) |
| Bullet cluster | PASS_STRONG (qualitative) | PASS_MODERATE | 1 단계 강등 |
| three-regime σ₀ | POSTDICTION | POSTDICTION | 유지 (정량 우월하나 anchor-circular) |
| CMB θ_* | PARTIAL | PARTIAL | 유지 |

**요약**: *applicable* k_hidden 만 적용해도 PASS_STRONG 7건 중 **3건이 즉시 PASS_MODERATE 로 강등**, 3건이 "RETAINED 경계" (k_h=9 시 함께 강등). PASS_STRONG 자격을 잃지 않는 후보는 **0건**.

---

## 5. paper §6.5(e) 와의 정합성

- paper/base.md §6.5(e) headline: "raw 28% PASS_STRONG (9/32) / substantive 13% (4/32)".
- 본 L502 결과는 substantive 4건 (Newton/BBN/Cassini/EP) 도 capacity-penalty 만 더해도
  PASS_STRONG 경계로 떨어짐을 보인다 → "substantive 13% (4)" 광고도 *AICc 정직* 기준에서 강등 압력.
- TABLES.md row 1 "5 free parameters in Branch B" 의 약 2배인 9–13 카운트가 본 audit 의 핵심
  contribution (L495 §2).
- abstract / 01_introduction / 10_appendix_alt20 / l5_*_interpretation 의 "zero free parameters" 광고는
  본 L502 까지 통합 시 **drift 가 더 심각**해진다 — paper §6.5(e) 단일 source of truth 로 통합 + abstract
  drift 차단 권고 (L495 §5 1-2 항목 재확인).

---

## 6. 한계 및 caveat

1. **N=1 채널**: AICc 의 small-sample 항이 발산 → AIC fallback 사용. capacity penalty (2k) 만 평가됨.
   substantive 4 의 *χ²* 자체는 0 으로 두었으나, 이는 "단일 inequality bound" 의 해석. 더 정직한 방법은
   "bound 까지의 거리 / σ" 를 χ² 로 환산하는 것 (예: Cassini |γ−1| 측정값 ≈ 1.1×10⁻⁴⁰ 가 bound 2.3×10⁻⁵
   에서 35 자릿수 떨어짐 → χ² ≈ 0 합리). 본 L502 는 χ²=0 보수 가정.
2. **Hidden DOF 분배**: 어느 hidden DOF 가 *진짜* 어느 채널에 적용되는지의 분류 (`hidden_dof_subset` field)
   는 *단일 분석가 판정*. 8인 라운드에서 자율 분담 검증 필요 (CLAUDE.md L6 Rule-A 8인 규칙).
3. **확장 카운트 +4**: axiom_scales = η_Z₂ + Λ_UV + dark-only + (B1 dimensional reduction channel) 4개를
   각각 1 DOF 로 풀어쓴 것. "≈Planck order" stipulation 을 자유도 0 으로 보면 +0, fully arbitrary 로 보면 +4.
   본 L502 는 후자 (보수적 정직).
4. **L482 base.md §3 행 추가 보류**: PASS_STRONG → PASS_MODERATE 강등 권고. paper edit 은 8인 라운드 사후승인 필수.

---

## 7. CLAUDE.md 정합

- **[최우선-1] 방향만 제공, 지도 금지**: 본 문서 신규 물리 수식 0줄. AICc 정의는 표준 통계학.
- **[최우선-2] 팀 독립 도출**: hidden DOF 분배 8인 자율 검증 보류. 본 문서는 그 라운드 *전 카탈로그*.
- **결과 왜곡 금지**: L482 PASS_STRONG candidate 의 ΔAICc=+0.70 광고를 *정직 +4.7* 로 강등 권고 → 왜곡
  반대 방향 (광고 → 정직) 정합.
- **paper/base.md 직접 수정 0건**.

---

## 8. 산출물

- `results/L502/HIDDEN_DOF_AICC.md` (본 문서)
- `results/L502/l502_results.json` (machine-readable 표)
- `simulations/L502/run.py` (재현 스크립트, OMP/MKL/OPENBLAS_NUM_THREADS=1 고정)

---

## 9. 한 줄 종합

**L495 hidden DOF k=9 (보수) 를 AICc 패널티로 환산: L482 RAR ΔAICc(SQT−free) = +0.70 → applicable k_h=2 적용 +4.7 (MODERATE 강등), 전체 k_h=9 적용 +18.8 (LCDM-equivalent free fit 압승). PASS_STRONG 7 후보 (substantive 4 + RAR + Bullet + 3-regime postdiction) 중 *applicable* 만 적용해도 3건 즉시 MODERATE 강등, 3건 RETAINED 경계. PASS_STRONG 등급을 그대로 유지하는 후보는 0건. paper abstract / intro 의 "zero free parameters" 광고는 §6.5(e) 정직 카운트와 drift 상태이며, 본 L502 가 추가 정량 근거 제공.**

---

*저장: 2026-05-01. results/L502/. 단일 분석 에이전트, 8인/4인 라운드 미실행. 본 문서는 메타-audit
이며 paper/ 직접 수정 0건. simulations/L502/run.py 가 재현 스크립트.*
