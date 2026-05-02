# L495 — Hidden Free-Parameter Audit

> **작성**: 2026-05-01
> **범위**: paper/base.md 의 "0 free parameter" 광고가 22행 한계 표 + 32 claim 분포 + L482 RAR PASS_STRONG 후보에서 *얼마나 유효한가* 를 cold-blooded 로 재검증.
> **저자**: 단일 분석 에이전트 (cataloging only — 8인/4인 후속 라운드 검증 대상).
> **방법**: paper 본문 `0 free / zero-parameter` 광고가 등장하는 모든 위치를 직접 추출 (Bash grep), 각 광고가 *암묵적으로 고정* 한 *함수형 / anchor / Υ⋆ / ansatz / regime* 선택을 hidden DOF 로 카운트.

---

## 0. 정직 한 줄

**"0 free parameter" 광고는 *부정확*. 함수형·anchor·Υ⋆·B1 ansatz·three-regime structure 의 사전 비등록 선택이 *최소 9개* hidden DOF 를 숨긴다. paper/TABLES.md row 1 (L48–L54 / L191) 이 이미 "5 free parameters in Branch B" 정직 카운트를 채택했으나, abstract / 01_introduction / 10_appendix_alt20 / 08_discussion §8.4 / l5_A12_interpretation 은 여전히 "zero free parameters" 광고를 반복한다 — drift 발생 중.**

---

## 1. paper 내 "0 / zero free parameter" 광고 등장 위치 (canonical)

| 위치 | 광고 문자열 | 광고가 *암묵 고정* 하는 선택 |
|---|---|---|
| `00_abstract.md:8` | "introduces **zero free background parameters** beyond ΛCDM" | "background parameter" 의 정의 자체가 anchor / Υ⋆ / 함수형 선택 *외부화* — 사전 등록 없음 |
| `01_introduction.md:46` | "falsifiable zero-parameter predictions" | 함수형 ansatz (M16 interpolating, simple-nu, standard-mu) 비등록 |
| `05_desi_prediction.md:56` | "E(0)=1, making this truly zero-parameter beyond (Ω_m, h)" | E(0)=1 정규화는 물리법칙 아닌 *bookkeeping*. amplitude lock 도 동역학적 도출 아님 (L6 Q17 미달, CLAUDE.md 명시) |
| `06_mcmc_results.md:83,87` | "A17 / A04 (zero-parameter)" | A12 / A17 의 erf-diffusion / adiabatic-pulse 함수형 선택은 alt-20 cluster 14 후보 중 1개 — `m·(1-a)` drift basis 선택 자체가 hidden DOF (L5 SYNTHESIS) |
| `07_comparison_lcdm.md:135,143` | "zero-parameter A12 > C11D by 2.00 nats" | A12 함수형 선택이 14 alt-20 후보 중 *후보-pick* 임. canonical drift class 단일 representative 로 축약했다는 사실이 free param=0 을 의미하지 않음 |
| `08_discussion_limitations.md:54` | "strict SQMH has zero free background parameters (§2)" | "strict SQMH" = axiom 1–6 만. derived 1 (Newton) 의 B1 bilinear ansatz 가 §2.2.1 에서 *추가 postulate* 로 명시되었음에도 zero-parameter 표현 유지 |
| `10_appendix_alt20.md:50` | "All twenty have exactly zero free parameters" | alt-20 모두가 함수형 선택 단계에서 hidden DOF. SVD n_eff=1 결과는 "20 후보 → 1 drift" 즉 *함수형 자체가 자유롭게 골라진* 사실의 사후 정당화 |
| `l5_A12_interpretation.md:7` / `l5_A17_interpretation.md:7` | "Zero free parameters" | 위와 동일 |
| `arxiv_submission_checklist.md:70` | "All constants in `simulations/config.py` (zero free params at..." | `config.py` 자체가 anchor 값 (cosmic 8.37 / cluster 7.75 / galactic 9.56) 을 *데이터 fit point* 로 hardcode |
| `verification_audit/R5_quantum.md:48` | "0 free parameters" 광고는 **overclaim** 명시 | ★ 자체 audit 이 이미 인정 |
| `paper/base.md:622` | substantive 13% / raw 28% PASS_STRONG | substantive 4건 (Newton/BBN/Cassini/EP) 도 각각 axiom 외부 입력 필요 (mass-action, η_Z₂ scale, β_eff = Λ_UV/M_Pl, dark-only embedding) — 본문이 이미 자인 |
| `paper/TABLES.md:166` (row 1) | ★ "Zero free parameters claim is **false**; 5 free parameters in Branch B (3 σ₀ + Γ₀ + ε)" | ★ paper 가 자체적으로 채택한 정직 카운트. abstract/intro 와 drift |

---

## 2. Hidden DOF — 정량 카운트 (사용자 지정 6 카테고리)

| # | Hidden DOF 출처 | 사전 등록 여부 | 카운트 | 근거 |
|---|---|---|---|---|
| 1 | **함수형 선택**: M16 interpolating `g_obs = g_bar/(1−exp(−√(g_bar/a₀)))` (L482 §Setup) | ✗ — paper §3 / §4 어디에도 사전 등록 없음 | **+1** | RAR 채널 carrier function 은 simple-nu / standard-mu / M16 / Bekenstein 중 임의 선택 가능. M16 선택 후 a₀ fit. 함수형이 a₀ best-fit 을 ±5% 이상 흔든다 (McGaugh 2016 Table 1). |
| 2 | **anchor 선택 (cosmic / cluster / galactic 3 anchor)**: D-3 표 (base.md:388) cosmic 8.37 (Planck CMB) / cluster 7.75 (A1689) / galactic 9.56 (SPARC) | ✗ — anchor *데이터 자체가 fit point* 로 들어감 (§3.5 anchor-circularity / mock false-detection 100% 명시) | **+3** | Three-regime σ₀(env) 의 saddle 위치는 "외부 anchor 만으로 결정" 됨 (base.md:813–815). anchor 가 priori 가 아니라 fit constraint → 3개 hidden DOF. paper 자체 §3.4 가 "saddle 위치 priori 도출 영구 불가" 명시. |
| 3 | **Υ⋆ choice (SPARC mass-to-light)**: Υ_disk = 0.5 / Υ_bul = 0.7 (L482 §Setup, M16 canonical) | △ — SPARC/M16 *카논* 따름. 그러나 "0 free param" 광고는 Υ 선택을 외부화 | **+1** | L482 §63 정직 disclose: "Υ ↑ 시 a₀_RAR ↓ (SQT 와 더 일치). 일치는 카논 default 에서 자연" — Υ 선택이 a₀ 를 직접 흔든다. L448 BTFR 결과는 Υ⋆=0.5 에서 a₀=1.53e−10 으로 5σ FAIL, L482 RAR 는 같은 Υ 에서 1.07e−10 으로 PASS. **같은 Υ 에서 채널만 바꿨을 때 a₀ 가 1.5× 변동** = Υ 가 사실상 1 DOF. |
| 4 | **B1 bilinear ansatz** (`R = σ·n·ρ_m`): paper §2.2.1, L430 추가 명시 | △ — L430 에서 비로소 *paper postulate (hidden until L430)* 로 분류 | **+1** | base.md:697 "B1 은 axiom 1–6 어느 것의 *결론* 도 아니다" 자인. 함수형 선택 (bilinear vs n²·ρ_m vs higher-order EFT). derived 1 (Newton 회복) 이 B1 ansatz-dependent. |
| 5 | **σ₀(env) three-regime parameterization** (3-regime structure 자체) | ✗ — postdiction (base.md:176, §3.4) | **+2** | 단일 universal σ₀ vs monotonic σ(ρ_env) vs 3-regime non-monotonic — 모형 선택이 Δχ²=288 (17σ 등가) 를 만든다. 3-regime *carrier* 자체가 1 DOF + saddle 위치 1 DOF (priori 영구 불가). mock injection FDR 100% (base.md:823) 가 anchor-driven 자유도 우위 정량 증명. |
| 6 | **각 PASS_STRONG claim 의 *진정* free parameter** | △ | **+1 (cumulative)** | base.md:1045 자인: substantive 4건 (Newton/BBN/Cassini/EP) 각각 σ₀ 항등식 *외* 추가 axiom 입력 필요 — mass-action (B1), η_Z₂ scale (BBN), β_eff = Λ_UV/M_Pl (Cassini), dark-only embedding (EP). 4 axioms 가 4개의 *조정 가능 scale* 을 도입하나 "∼Planck/UV order" 로 stipulated → 형식상 "측정 X but 선택 O" → 보수적으로 +1 만 카운트 (4 까지 펼치면 hidden DOF 13). |
| **합계** | | | **9 (보수) ~ 13 (확장)** | TABLES.md row 1 의 "5 free parameters in Branch B" 보다 *2배 많은* 카운트가 가능 |

---

## 3. PASS_STRONG claim 별 진정 free parameter

| Claim | 광고 | 진정 free parameter | 정직 카운트 |
|---|---|---|---|
| Newton 회복 (derived 1) | "0 free param 으로 1/r² 도출" | B1 bilinear ansatz 함수형 (R ∝ n·ρ_m vs n²·ρ_m vs ...) + σ₀ amplitude (4πG·t_P 는 holographic identity 이지만 dimensional reduction 채널 선택 자체가 비유일 — verification_audit/R5 명시 "5 dimensionally consistent 후보, Q_macro 38 자릿수 변동") | **2 hidden** |
| BBN ΔN_eff | "η_Z₂ ≈ 10 MeV 로 ΔN_eff ≈ 10⁻⁴⁶" | η_Z₂ scale 이 *10 MeV 로 stipulated*. BBN bound 통과를 위해 사후 선택 가능 | **1 hidden** |
| Cassini |γ−1| < 2.3×10⁻⁵ | "β_eff ≈ 7.4×10⁻²¹ 로 자동 통과" | β_eff = Λ_UV/M_Pl 의 Λ_UV 선택 (Λ_UV ≈ Planck 가 자연 가정이나 구체값 비등록) | **1 hidden** |
| EP \|η\| < 10⁻¹⁵ | "dark-only embedding 으로 β_b=0" | dark-only embedding 자체가 sector-selective 선택 (C10k vs universal). L4 universal IDE 는 Cassini 자동 위반 — embedding 선택이 PPN 통과를 결정 | **1 hidden (구조적)** |
| L482 RAR a₀ 일치 (PASS_STRONG 후보) | "a₀ = c·H₀/(2π) priori" | 함수형 (M16) + Υ⋆ + H₀ anchor (Planck 67.4 vs Riess 73.0 → a₀ 8% 변동, Table §Results) | **3 hidden** |
| Bullet cluster offset | "qualitative PASS, MOND fail" | depletion-zone formalism 자체가 정성 — "150 kpc lens-vs-gas magnitude 는 gas ram-pressure (입력) echo" (base.md:881) | **1 hidden (정성-한정)** |
| ρ_q/ρ_Λ ≈ 1 (Λ origin) | ★ pre-L412 "exact" | n_∞ derivation 이 ρ_Λ_obs 를 input → CONSISTENCY_CHECK 강등 (base.md:1047) | ★ paper 가 이미 강등 처리 |

---

## 4. 22행 한계 표 vs "0 free param" 광고 — drift 정량

paper/TABLES.md row 1 (L48–L54, L191) 이 H-tier permanent 한계로 *이미 정직 채택*:

> ``Zero free parameters'' claim is false; 5 free parameters in Branch~B (3 σ₀ + Γ₀ + ε).

본 L495 audit 은 위 5 카운트가 **Branch B (three-regime) 한정** 이며, **Branch A (monotonic) + RAR + alt-20 + B1 ansatz** 까지 확장하면 9–13 까지 늘어남을 보인다. 즉 TABLES.md row 1 은 정직 방향이지만 *under-count*. abstract/intro 가 이 정직 카운트와 sync 안 됨.

| paper 위치 | 카운트 광고 | drift 평가 |
|---|---|---|
| `00_abstract.md` | "zero free background parameters beyond ΛCDM" | ✗ drift (TABLES.md row 1 미반영) |
| `01_introduction.md` | "falsifiable zero-parameter predictions" | ✗ drift |
| `08_discussion §8.4` | "strict SQMH has zero free background parameters" | △ "strict" qualifier 추가했으나 B1 / Υ⋆ / anchor 미언급 |
| `10_appendix_alt20.md` | "All twenty have exactly zero free parameters" | ✗ drift (함수형 선택 = 14-cluster pick) |
| `06_mcmc_results.md` | "A12 / A17 (zero-parameter)" | ✗ drift |
| `paper/TABLES.md row 1` | "5 free parameters in Branch B" | ✓ 정직 (H-tier) |
| `paper/base.md §6.5(e)` | "substantive 13% (4/32)" | ✓ 정직 (양면 표기 의무 명시) |
| `verification_audit/R5_quantum.md` | "'0 free params' overstated" | ✓ 정직 |

→ paper 본체는 *이미 자체적으로 over-claim 인정* 하나, abstract / intro / appendix / l5\_\*_interpretation / arxiv_submission_checklist 가 drift 상태로 "zero-parameter" 표어를 반복.

---

## 5. 권고 (paper 직접 edit 보류, 후속 8인 라운드 대상)

1. **abstract drift 차단**: `00_abstract.md:8` 의 "zero free background parameters" → "zero *background-parameter* extension beyond ΛCDM, conditional on (M16 interpolating function, Υ⋆ = 0.5/0.7 SPARC convention, three-regime σ₀ anchor pick, B1 bilinear ansatz)" 또는 TABLES.md row 1 cross-ref.
2. **single source of truth**: hidden DOF 카운트도 §6.5(e) Self-audit 단락 안에 통합 — abstract/intro/appendix 는 §6.5(e) 참조만 (drift 차단, L414 ATTACK A4 cross-ref guard 패턴 재사용).
3. **L482 PASS_STRONG 격상 시 disclosure**: §3 RAR row 추가 시 "함수형 = M16 / Υ⋆ = canonical / a₀ = c·H₀/(2π) prior" 3-line conditional 명시. "0 free parameter" 표어 사용 금지, "1-parameter free fit 과 ΔAICc=+0.70 통계 동등" 표현으로 대체 (이미 L482 RAR_TEST.md §ΔAICc 가 채택한 표현).
4. **`claims_status.json` 신규 키 `hidden_dof_audit`**: 본 L495 결과를 machine-readable 로 덧붙여 abstract / intro 에서 자동 cross-link.
5. **TABLES.md row 1 확장**: H-tier 단일 행을 "5 (Branch B) → 9 (전체 paper, L495 audit)" 으로 갱신, 본 문서 cross-link.

---

## 6. CLAUDE.md 정합성

- **결과 왜곡 금지**: paper 자체 광고를 부정직 → 정직으로 끌어올리는 audit. ✓
- **[최우선-1] 방향만 제공, 지도 금지**: 본 문서 수식 0줄, 신규 파라미터 도입 0개. hidden DOF *카운트* 만 (구조적 분류). ✓
- **[최우선-2] 팀 독립 도출**: 본 audit 은 verdict 카탈로그. 후속 8인팀이 자율 분담으로 (a) abstract drift 차단 문구 도출, (b) `claims_status.json` schema 확장, (c) 9 vs 13 카운트 결정 (보수 vs 확장) 의 K-범위 독립 합의. ✓
- **paper/base.md 직접 수정 금지** (L490 정책 상속): 본 문서 권고만, edit 0건. ✓

---

## 7. 한 줄 종합

**"0 free parameter" 광고는 *부정확*. paper 자체 TABLES.md row 1 + §6.5(e) + verification_audit/R5 가 이미 자인. abstract / intro / appendix / l5_*_interpretation / arxiv_checklist 5개 위치가 drift 상태. hidden DOF 보수 카운트 9개 (함수형 1 + anchor 3 + Υ⋆ 1 + B1 ansatz 1 + three-regime structure 2 + axiom-scale stipulation 1), 확장 카운트 최대 13개 — TABLES.md row 1 의 "5 in Branch B" 의 약 2배. 8인 라운드에서 abstract drift 차단 + claims_status.json `hidden_dof_audit` 신규 키 + TABLES.md row 1 확장 권고.**

---

*저장: 2026-05-01. results/L495/HIDDEN_DOF_AUDIT.md. 본 문서는 메타-audit 이며 simulations/ 신규 코드 0줄. paper/ 직접 수정 0건. L494 / L493 / L492 / L491 미실행 (L490 round-1 final 이후 첫 audit).*
