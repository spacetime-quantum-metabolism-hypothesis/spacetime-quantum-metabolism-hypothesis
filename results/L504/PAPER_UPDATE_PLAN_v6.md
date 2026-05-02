# L504 — paper/base.md update plan v6 (Phase 1 통합: L491–L499)

> **작성**: 2026-05-01
> **저자**: 단일 분석 에이전트 — meta-synthesis only
> **목적**: L491–L499 Phase-1 audit 결과를 paper/base.md 4개 절 (§4.1 / §6.1 / §4.6+ / abstract) 에 정직 반영하기 위한 *update plan*. 본 문서는 plan 단계 — paper 직접 edit 0건. 반영은 후속 8인 (이론 클레임) / 4인 (코드/표) 라운드 승인 후 별도 LXX 에서.
> **CLAUDE.md 정합성**: 수식 0 줄, 신규 파라미터 0개, 결과 왜곡 0건. abstract drift 차단은 [최우선-1] 정합 (지도 아닌 *구조적 정직 표기*).

---

## 0. 정직 한 줄

**L491–L498 8개 audit 의 메시지는 일관된다 — "L482 RAR PASS_STRONG candidate 는 *진정한 신호* (L493 OOS PASS / L494 0/1000 mock FP) 이지만, *광고된 정밀도와 자유도*는 부정확 (L491 cross-form 0.37 dex / L492 cross-dataset 0.35 dex / L495 hidden DOF 9개 / L497 진정 invariant 단 2개) — 따라서 grade 는 PASS_STRONG → PASS_MODERATE 격하, abstract `0 free parameter` drift 차단, falsifier independence 11.25σ → 8.87σ (N_eff=4.44) 정정 의무**.

---

## 1. Phase-1 audit 결과 한 줄 요약 (v6 입력)

| Loop | 산출물 | 핵심 수치 | grade 영향 |
|------|--------|-----------|------------|
| L491 | RAR_FUNCFORM_AUDIT.md | 함수형 7개 cross-form: median 0.023 dex 일치, full spread **0.368 dex** | K_R6 신규 → PASS_MODERATE 격하 근거 |
| L492 | RAR_DATASET_AUDIT.md | subset 5개 cross-dataset: D4 dwarf max\|Δlog\|=**0.353 dex**, K_X 1/4 PASS | RAR cross-dataset 불안정성 |
| L493 | OUT_OF_SAMPLE.md | 70/30 split: test χ²/dof=1.283, dAICc(SQT−trained)=−8.10, **5/5 K_OOS PASS** | OOS = real signal 증명 |
| L494 | MOCK_FALSE_RATE.md | Newton-null 200×5 mock: K_joint **0/1000 (FP=0.0%)**, MOND-inj F1/F2/F4 100% recovery | cherry-pick 면역, statistical power 충분 |
| L495 | HIDDEN_DOF_AUDIT.md | "0 free param" 광고 11곳 위치, hidden DOF **보수 9개 / 확장 13개** | abstract drift 차단 의무 |
| L496 | GLOBAL_CV.md | 8 anchor LOO max\|Δpass-rate\|=**0.089** < 0.125 fair share | 단일 anchor 의존 없음 |
| L497 | INVARIANTS.md | 진정 invariant **2개 (C1: factor-1.5 a₀ + C7: Newton 패배)**, 나머지 PASS_MODERATE/PARTIAL 격하 | grade 표 5건 격하 근거 |
| L498 | FALSIFIER_INDEPENDENCE.md | 6 falsifier participation ratio **N_eff=4.44**, ρ-corrected **8.87σ** (naive 11.25σ) | abstract / §4.6 정정 의무 |

---

## 2. paper/base.md 4-section update plan

본 plan 은 **§4.1 RAR row 신설 / §6.1 한계 표 hidden DOF 행 신설 / §4.6+ falsifier 정정 / abstract drift 차단** 4건을 다룬다.

### 2.1 § 4.1 — PASS 표에 RAR row 추가 (PASS_MODERATE)

**대상**: paper/base.md L172 인근 PASS 표 (현재 11행, README L225 에 따라 §4.1 으로 분리). 신규 1행 추가 → 12행.

**현 상태**: RAR a₀ row 가 §4.1 PASS 표에 *없음*. L172 의 "MOND a₀ | ✅ PASS | a₀ = c·H₀/(2π), ~1σ" 가 §1.2.2 에 머물러 있고 §4.1 row 로 정식 등록 안 됨.

**v6 권고 신규 행 (요지만, 본문은 8인 라운드에서 도출)**:

| # | Anchor / Channel | Status | 핵심 수치 | Caveat (의무) | Cross-ref |
|---|---|---|---|---|---|
| 12 | SPARC RAR a₀ | **PASS_MODERATE** | a₀_RAR / a₀_SQT = 1.025 (M16 + Υ canonical) | functional-form 한정 (cross-form spread 0.368 dex, L491) ; cross-dataset 불안정 (D4 dwarf Δlog=−0.353, L492) ; hidden DOF +3 (Υ⋆+anchor+func, L495) ; OOS 5/5 PASS 별도 (L493) ; mock FP 0/1000 (L494) | §4.1 row 12 신설; L491/L492/L493/L494/L497 cross-link |

**의무 caveat 본문 (4 줄)**:

1. "PASS_MODERATE — 정량 5/5 K_R PASS 는 (M16 interpolating function, Υ_disk=0.5/Υ_bul=0.7, SPARC 175 full sample, Planck H₀) 4-tuple 한정. 함수형 변경 시 spread 0.37 dex (L491), dwarf subset 변경 시 \|Δlog\|=0.35 dex (L492)."
2. "OOS validation — 70/30 train-test split 에서 SQT-locked a₀ 가 hold-out 30% 에 χ²/dof=1.283 (5/5 K_OOS), 진짜 신호 (L493)."
3. "Mock null 0/1000 — Newton-only mock 1000 trial 에서 K_R1∧K_R3∧K_R5 동시 PASS 0건. cherry-pick 면역 (L494). MOND-injection positive control F1/F2/F4 100% recovery."
4. "진정 invariant 는 'a₀ ~ c·H₀/(2π) factor-≤1.5 일치' (C1, L497) — 2.5% offset / 0.006 dex tightness / ΔAICc=−56 정량 claim 은 분석축 의존. PASS_STRONG 격상 *금지*."

**§1.2.2 와의 sync**: L172 "PASS (strong)" 표기를 "PASS_MODERATE (functional-form-한정)" 으로 동기화. §548 claims_status JSON `RAR_a0` 키 grade 업데이트.

**8인/4인 분담**:
- Rule-A (이론): caveat 문구 4줄 도출, "PASS_STRONG candidate" → "PASS_MODERATE" 격하 합의.
- Rule-B (코드/표): §4.1 표 row 12 markdown 추가, claims_status.json 키 갱신, cross-ref grep 검증.

---

### 2.2 §6.1 — 한계 표에 hidden DOF 행 신설 (9개)

**대상**: paper/base.md README L226 의 "§6.1.1 표 14행" (H-tier permanent 한계). TABLES.md row 1 가 이미 "5 free parameters in Branch B" 로 정직 채택. v6 는 *9 (full paper 확장)* 로 갱신.

**현 상태**: TABLES.md row 1 = "Zero free parameters claim is **false**; 5 free parameters in Branch B (3 σ₀ + Γ₀ + ε)". abstract / 01_introduction / 10_appendix_alt20 / 08_discussion §8.4 / l5_A12_interpretation 5개 위치가 drift (L495 §1).

**v6 권고 — 신규 1행 추가 + TABLES.md row 1 확장**:

| Hidden DOF (출처) | 카운트 | 영향 받는 claim | 사전 등록 | 근거 |
|---|---|---|---|---|
| 함수형 (M16 interpolating) | +1 | RAR a₀ (L482) | ✗ | cross-form spread 0.37 dex (L491) |
| anchor (cosmic/cluster/galactic) | +3 | three-regime σ₀ | ✗ (anchor=fit point) | base.md §3.4–3.5 명시 |
| Υ⋆ convention (disk/bul) | +1 | RAR a₀, BTFR | △ canonical | L482 §63 자인 |
| B1 bilinear ansatz | +1 | Newton derived 1 | △ L430 명시 | base.md §2.2.1 자인 |
| three-regime structure | +2 | Branch B | ✗ (postdiction) | base.md §3.4 자인 |
| axiom-scale stipulation | +1 | BBN/Cassini/EP | △ "Planck/UV order" | base.md §6.5(e) 양면 표기 |
| **합계 (보수)** | **9** | | | L495 §2 |
| **합계 (확장)** | **13** | | | L495 §2 (axiom-scale 펼침) |

**의무 본문 (3 줄)**:

1. "TABLES.md row 1 갱신: '5 (Branch B 한정) → 9 (전체 paper, L495 audit)'."
2. "abstract / 01_intro / 10_appendix_alt20 / 08_discussion §8.4 / l5_A12_interpretation 5개 drift 위치 모두 §6.1 hidden DOF row 로 cross-link, 'zero-parameter' 표어 사용 금지."
3. "single source of truth = §6.5(e) Self-audit. abstract 등은 §6.5(e) cross-ref 만 (L414 ATTACK A4 cross-ref guard 패턴 재사용)."

**8인/4인 분담**:
- Rule-A: 보수 9 vs 확장 13 카운트 결정, cross-ref guard 문구 도출.
- Rule-B: TABLES.md row 1 갱신, claims_status.json 신규 키 `hidden_dof_audit`, 5개 drift 위치 grep + edit.

---

### 2.3 §4.6 (또는 §6 forecasts) — falsifier independence 정정 (N_eff=4.44 / 8.87σ)

**대상**: paper/base.md L228 README "§4.6 22 예측 표" + §6 forecasts. 6 falsifier 의 "independent 5σ-class" 광고 *정정 의무*.

**현 상태**: paper 본문이 "6 independent falsifiers" 로 광고. 단순 결합 Z = √Σσ² = 11.25σ (naive) 이 *암묵 가정*.

**v6 권고 정정 (3 줄, 본문 정확 문구는 8인 라운드)**:

1. "naive count 6 → **active 5 + null 1** (SKA structural null), 단순 결합 Z=11.25σ 정정."
2. "observable footprint correlation matrix (BAO/RSD/WL/CMBc/CMBl/GW_s/HI/Cl 8 basis) 분해: Euclid×LSST ρ=0.80 (cosmic-shear redundancy), DESI×Euclid ρ=0.54 (BAO), DESI×SKA ρ=0.32 (RSD)."
3. "**N_eff = 4.44** (participation ratio, conservative) ~ 5.71 (Cheverud–Galwey). ρ-corrected Z_comb = **8.87σ (all 6) / 9.95σ (active 5)**, 11.25σ 미사용. CMB-S4 + ET + SKA 가 truly orthogonal load-bearing 3 (10.83σ at full independence)."

**의무 abstract / §6 추가 문구 (한 줄)**: "6 pre-registered falsifiers compress to N_eff ≈ 4.44 truly independent observable channels; honest correlation-corrected combined detection is 8.9σ (all six) / 9.95σ (active five), not the naive 11.25σ."

**LSST 처리**: L498 §8 권고 — LSST 를 primary falsifier 에서 *cosmic-shear bloc (Euclid+LSST)* 로 통합 또는 강등. Bonferroni Holm 에서 LSST 만 ~2× margin, Euclid×LSST ρ=0.8 가 .9+ 로 추정 시 LSST 추가 정보량 ≈ 0.

**8인/4인 분담**:
- Rule-A: "6 independent" → "5 active + 1 null, N_eff=4.44" 표기 합의, LSST 강등 결정.
- Rule-B: §4.6 22 예측 표 footnote 추가, claims_status.json `falsifier_count` / `Z_comb_rho_corrected` 키 추가, abstract 한 줄 갱신.

---

### 2.4 abstract — "0 free parameter" drift 차단

**대상**: paper/base.md 헤더 직접 광고 (3행 §1.2 / 헤드라인 / TL;DR L142–149) + paper/00_abstract.md L8.

**현 상태 (drift 5건, L495 §1)**:
- `00_abstract.md:8` — "introduces zero free background parameters beyond ΛCDM"
- `01_introduction.md:46` — "falsifiable zero-parameter predictions"
- `06_mcmc_results.md:83,87` — "A17 / A04 (zero-parameter)"
- `10_appendix_alt20.md:50` — "All twenty have exactly zero free parameters"
- `l5_A12_interpretation.md:7` / `l5_A17_interpretation.md:7` — "Zero free parameters"

**v6 권고 정정 — 3 옵션 (8인 라운드 선택)**:

| 옵션 | 표기 변경 | 장점 | 단점 |
|---|---|---|---|
| **OPT-1 (full disclosure)** | "zero free background parameters beyond ΛCDM" → "zero *background-parameter* extension beyond ΛCDM, conditional on (M16 interpolating function, Υ⋆=0.5/0.7 SPARC convention, three-regime σ₀ anchor pick, B1 bilinear ansatz)" | 정직 100% | abstract 길이 증가 |
| **OPT-2 (cross-ref)** | "zero free background parameters beyond ΛCDM (caveats: §6.5(e), L495 audit)" | 길이 유지 | 독자가 §6.5(e) 안 읽으면 drift 지속 |
| **OPT-3 (sci-bridge)** | "1-parameter free fit 과 ΔAICc=+0.70 통계 동등 — '0 free parameter' 표어 폐기" | overclaim 차단 명확 | 표어 effect 손실 |

**최우선 권고**: **OPT-2 + TABLES.md row 1 grep guard**. abstract / intro 등 5개 drift 위치 모두 § 6.5(e) cross-ref 한 줄 강제.

**의무 한 줄 (cross-ref guard)**: 모든 "zero / 0 free parameter" 광고 다음에 "(see §6.5(e) Self-audit; 9 hidden DOF disclosed in TABLES.md row 1)" footnote 의무.

**8인/4인 분담**:
- Rule-A: OPT-1 / OPT-2 / OPT-3 결정, cross-ref guard 문구 합의.
- Rule-B: 5개 drift 위치 grep + edit, `verification_audit/R5_quantum.md` 의 "overstated" 자체 audit 와 sync, arxiv_submission_checklist.md L70 sync.

---

## 3. v6 vs 이전 버전 — 변경 요약

> v1–v5 plan 은 디스크 미존재 (results/L504 신규). 본 v6 는 *최초 plan*.

핵심 신규 (Phase-1 audit 8건 직접 인용):

1. **§4.1 신규 row 12 (RAR PASS_MODERATE)** — caveat 4줄 의무.
2. **§6.1 hidden DOF 행 9개** — TABLES.md row 1 (5 → 9) 확장.
3. **§4.6 / §6 falsifier — N_eff 4.44 / Z_comb 8.87σ** 정정.
4. **abstract drift 차단** — 5개 위치 cross-ref guard.

---

## 4. 우선순위 / 시점

| 우선순위 | 항목 | 의무 시점 |
|---|---|---|
| **P0** | abstract drift 차단 (§ 2.4 OPT-2) | arxiv 제출 전 의무 (overclaim risk) |
| **P0** | §4.6 falsifier N_eff 정정 (§2.3) | arxiv 제출 전 의무 (numerical claim) |
| **P1** | §4.1 RAR row 12 신설 (§2.1) | 8인 라운드 후 |
| **P1** | §6.1 hidden DOF row (§2.2) | 8인 라운드 후 |
| **P2** | claims_status.json 키 4종 추가 | 4인 코드 라운드 |

---

## 5. CLAUDE.md 정합성

- **결과 왜곡 금지**: PASS_STRONG → PASS_MODERATE 격하 / 11.25σ → 8.87σ 정정 / "0 free param" → "9 hidden DOF" 정직 재기록. ✓
- **[최우선-1] 방향만 제공, 지도 금지**: 본 plan 신규 수식 0 줄, 신규 파라미터 0개, 새 이론 형태 0건. 표기 *변경* 만. ✓
- **[최우선-2] 팀 독립 도출**: 본 plan 은 *후보 옵션* 카탈로그 (특히 abstract OPT-1/2/3). 8인팀이 최종 표기 자율 선택. ✓
- **paper/base.md 직접 수정 0건**: ✓ (본 문서는 plan 단계).
- **L6 8인/4인 규칙**: 격하 + 표기 변경 = 이론 클레임 → Rule-A 8인. 표/JSON/grep edit = 코드 → Rule-B 4인. ✓

---

## 6. 다음 LXX 권고 (Phase-2 진입)

1. **L505 8인 Rule-A 라운드** — §2.1 PASS_MODERATE caveat 4줄 + §2.4 abstract OPT 결정.
2. **L506 4인 Rule-B 라운드** — § 2.2 / §2.3 / §2.4 markdown + JSON edit, grep guard 검증.
3. **L507** — paper/base.md 실제 edit (P0 2건 우선) + verification_audit/R5_quantum.md sync.
4. **L508** — claims_status.json 4 신규 키 + arxiv_submission_checklist.md L70 sync.

---

## 7. 한 줄 종합

**v6 = Phase-1 audit 8건 (L491 cross-form 0.37 dex / L492 cross-dataset 0.35 dex / L493 OOS 5/5 PASS / L494 0/1000 mock FP / L495 hidden DOF 9개 / L496 LOO 0.089 글로벌 일관 / L497 진정 invariant 2개 / L498 N_eff=4.44 / 8.87σ) 를 paper/base.md 4 절 (§4.1 RAR row PASS_MODERATE / §6.1 hidden DOF 9개 / §4.6+ falsifier 정정 / abstract drift 차단) update plan 으로 통합. P0=abstract+falsifier (arxiv 의무), P1=§4.1+§6.1 (8인 라운드), P2=claims_status JSON. paper/base.md 직접 edit 0건.**

---

*저장: 2026-05-01. results/L504/PAPER_UPDATE_PLAN_v6.md. 단일 분석 에이전트, 8인/4인 라운드 미실행. paper/base.md edit 0건. simulations/ 신규 코드 0줄. CLAUDE.md [최우선-1] (수식 0줄), [최우선-2] (팀 자율 도출) 정합.*

*정직 한 줄: L491–L498 결과는 SQMH 의 L482 RAR PASS_STRONG candidate 가 진정 신호임을 확정 (L493 OOS / L494 mock 0/1000) 하면서 동시에 그 광고된 정밀도와 자유도를 부정확으로 격하 (L491 functional-form / L492 cross-dataset / L495 hidden DOF / L497 invariant 2 only) 하며, falsifier 11.25σ 헤드라인을 8.87σ 로 정정 (L498) 하라고 일관되게 요구한다 — paper/base.md 4 절 update 가 obligatory.*
