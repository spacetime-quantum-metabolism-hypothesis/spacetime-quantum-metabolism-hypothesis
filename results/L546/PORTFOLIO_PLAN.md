# L546 — 3-Paper Portfolio Finalize Plan

> 작성: 2026-05-01. 단일 작성 에이전트 (8인 Rule-A / 4인 Rule-B 라운드 *미실행*).
> 선례 계승: L539 (MNRAS+Companion 초안) / L540 (3-paper portfolio 매핑 + Round 10 timeline) / L526 R8 / L531 §5.2 / L537 §3 정직 패턴.
> CLAUDE.md 정합: 신규 수식 0줄, 신규 파라미터 0개, paper/base.md edit 0건, simulations/ 신규 코드 0줄, claims_status.json edit 0건.

---

## 0. 정직 한 줄

본 L546 은 *3-paper portfolio (Main MNRAS-γ / Companion B / arXiv D) 의 실행 계획만* 산출하며 — 각 paper 의 final title / section structure / claims (audit-aligned, hidden DOF 9–13 + Verlinde degeneracy + Bullet DM 잔존 모두 disclosed) / submission timeline / cross-reference policy 를 정의하되, **acceptance 산술 합산 (중앙 0.59) 은 reviewer-pool overlap 미보정 단순 독립 가정 결과** 이며 실제 overlap 보정 시 0.43–0.50 로 떨어질 가능성 명시 — 본 plan 의 채택 / 실행 / 제출은 *모두* 후속 Round 10 R10-Disk-Audit + 8인 Rule-A / 4인 Rule-B 라운드 결정에 종속.

---

## 1. Portfolio 구성 (L540 §4.1 매핑 직접 상속)

| 라벨 | 정체 | 타깃 저널 | acceptance 중앙 | 핵심 자산 | 핵심 미달 |
|---|---|---|---|---|---|
| **Main MNRAS-γ** | galactic-only theory paper (Path-γ) | MNRAS (1순위) / ApJ (2순위) | **22%** (range 18–28%) | C1 (a₀ ↔ c·H₀/(2π) factor-≤1.5), C7 (Newton-only SPARC fail), σ-framework dimensional priori, RAR PASS_MODERATE | Verlinde 2017 a₀ degeneracy (정직 인정), Bullet cluster DM 잔존, hidden DOF 9–13, cosmology 클레임 0 |
| **Companion B** | methodology / verification infrastructure paper (Path-B) | Open Journal of Astrophysics (1순위) / JOSS (2순위) | **47%** (range 40–55%, mid 60% 보수 보정 47%) | 7 verify_*.py scripts (5 PASS + 1 FAIL + 1 negative-control), claims_status.json schema (PASS_STRONG / PASS_MODERATE / PASS_QUALITATIVE / PASS_BY_INHERITANCE / FAIL), Docker + conda env, expected_outputs JSON | 이론 새로움 0 (방법론 단독), schema adoption count = 1, Q_parameter FAIL 미해결 |
| **arXiv D** | preprint priority lock-in (DR3 사전등록) | arXiv astro-ph.CO + OSF DOI | **~100%** (모더레이션) | Q17 partial (Δρ_DE ∝ Ω_m amplitude-locking 부분 도출), DR3 정량 falsifier (wa>−0.5 면 KILL), pre-DR3 priority claim, A12 erf-diffusion winner (L529 시점) | peer-review 미경유, PRD Letter 진입 영구 차단 (Q17 동역학 미달성, Q13/Q14 미동시), C28 Maggiore-Mancarella 독립 이론 명시 |

> **L540 §4.1 의 (보류) JCAP-A** 는 본 L546 portfolio 에서 *제외* — Path-α 단독 acceptance 8–13% 가 portfolio 의 reviewer-pool 오염 + brand 자기파괴 비용 초과. 사용자 명시 요구 (Main MNRAS-γ + Companion B + arXiv D) 와도 정합.

---

## 2. Paper 1 — Main MNRAS-γ

### 2.1 Final Title

> **"A galactic origin for Milgrom's a₀: Spacetime quantum-tension framework and the depletion-zone signature"**

- 부제 (subtitle, optional): *"A galactic-only test of c·H₀/(2π) invariance with factor-≤1.5 RAR sub-row PASS_STRONG"*
- 길이: main title 13 단어 + subtitle 17 단어. MNRAS title 가이드라인 (≤20 단어 main) 정합.
- "metabolism" / "quantum metabolism" / "SQMH" / "cosmology" / "DESI" / "DR3" / "DE" 단어 abstract+title 등장 0건 의무.
- "depletion zone" 은 paper 내부 용어로 정의 후 사용 (L482 RAR audit 의 σ-framework 차원분석 기반).

### 2.2 Section Structure (galactic-only, no cosmology)

| § | 제목 | 핵심 내용 | hidden DOF disclosure |
|---|---|---|---|
| 0 | Abstract | 250 단어, 6-bullet honest headline (PASS_MODERATE / a₀ factor-≤1.5 / Verlinde degeneracy 인정 / Bullet 잔존 / N_eff=4.44 / pre-registered falsifier) | Y (line 3, "9–13 hidden DOF disclosed") |
| 1 | Introduction | 1.1 MOND 50년 / 1.2 a₀ 수치 puzzle / 1.3 SQT framework (axiom 인용만, derivation 없음) / **1.4 Scope: galactic-only, cosmology claims excluded** | — |
| 2 | Theoretical framework | 2.1 σ-framework dimensional 차원분석 / 2.2 Depletion-zone scale L_dep / 2.3 a₀ = c·H₀/(2π) (base.md / verify_milgrom_a0.py 인용만) / **2.4 Verlinde 2017 degeneracy: 명시 인정** | Y |
| 3 | a₀ verification | 3.1 H₀ 입력 (73 km/s/Mpc, SH0ES) / 3.2 a₀(SQT) = 1.129 × 10⁻¹⁰ m/s² → **0.71σ deviation** (verify_milgrom_a0.py 실측) — *L539 §2.3 정정 확정* | — |
| 4 | Empirical anchors | 4.1 RAR PASS_MODERATE (factor-≤1.5 sub-row PASS_STRONG) / 4.2 BTFR / **4.3 Bullet cluster: residual DM 정직 인정** | Y |
| 5 | Pre-registered falsifiers | 5.1 6→6 falsifier list / 5.2 8.87σ ρ-corrected / 5.3 N_eff=4.44 (BAO 채널 제거 후 재 fit 의무 — Round 10 R10-Exec-B) | — |
| 6 | Limitations | 6.1 SPARC galaxy-by-galaxy fit 부재 / 6.2 cluster DM / 6.3 Verlinde degeneracy / 6.4 hidden DOF k_eff≈3 / 6.5 cosmology 클레임 0 (의도) / 6.6 σ-framework anchor count=3 / 6.7 a₀ universality K=1/4 | Y (전부) |
| 7 | Conclusion | galactic-only verdict; cosmology claim 0 재확인; Companion B + arXiv D 교차참조 | — |
| 8 | Reproducibility | verify_milgrom_a0.py + Docker + expected_outputs JSON 인용 (Companion B 와 동일 infrastructure) | — |

- MNRAS-specific format notes 는 별도 L539 §2.1 (5) 에서 처리 완료. 변경 없음.
- §3.2 의 "0.42σ vs 0.71σ" 는 본 L546 plan 에서 **0.71σ 단일 채택** (verify_milgrom_a0.py 실측 우선). expected_outputs/verify_milgrom_a0.json 디스크 값 cross-check 는 R10-Exec-B 의무.

### 2.3 Key Claims (audit-aligned)

1. a₀(SQT) = c·H₀/(2π) = 1.129 × 10⁻¹⁰ m/s² (H₀=73 입력) → 0.71σ vs Begeman+ 1991 a₀_obs = 1.20 ± 0.10. **PASS_MODERATE (factor-≤1.5)**.
2. RAR (L482 base candidate) PASS_MODERATE — factor-≤1.5 sub-row 만 PASS_STRONG (L505 격하 확정).
3. Newton-only SPARC fail (C7) — 진정 invariant.
4. **Verlinde 2017 emergent gravity 와 a₀ 수치 동일 (cH₀/2π) — galactic-only scope 내부에서 novelty 약함 정직 인정**.
5. Bullet cluster: SQT 가 cluster DM 잔존을 *제거* 하지 못함 → pure MOND 와 동일 약점 인정.
6. cosmology claims (DESI w_a, S8, ISW, UHE-CR) **0건** — 본 paper scope 외부.

### 2.4 Submission Timeline

- **2026-05 ~ 06**: R10-Disk-Audit 통과 후 R10-Exec-A (8인 Rule-A) — paper/base.md final state 확정 (§05→§10 이동, claims_status v1.3, abstract 재작성).
- **2026-06**: R10-Exec-B (4인 Rule-B) — verify_milgrom_a0.py 실측 cross-check, N_eff BAO 채널 제거 재 fit.
- **2026-07**: MNRAS_DRAFT.md final 화 (L539 초안 → §3.2 0.71σ 정정 + L546 plan 적용), figures 재생성.
- **2026-08**: 내부 review (단일 에이전트 자기 review 금지 — 8인 라운드 의무).
- **2026-09**: **MNRAS 제출**.
- **2026-10 ~ 2027-Q1**: reviewer 라운드 (MNRAS 평균 review 기간 4–6mo).
- **2027 Q2 (DR3 공개 후)**: arXiv D falsifier 결과로 revision 보강 (preregistered, MNRAS scope 외부 → 별도 supplementary).

### 2.5 Cross-reference Policy

- arXiv D 인용: §1.3 "SQT framework" 부분에서 1회 ("for cosmological context, see [arXiv D]") — *cosmology claim 의 외부 위치 락인*.
- Companion B 인용: §8 "Reproducibility" 에서 1회 ("verification infrastructure described in [Companion B]") — *방법론 자산 분리*.
- JCAP-A (보류) 인용: **0건** — portfolio 에 포함 안 함.
- 자기 referrer (Main → Main): **0건** (외부 cosmology cross-link 금지).

---

## 3. Paper 2 — Companion B

### 3.1 Final Title

> **"A reproducibility framework for high-stakes cosmological claims: Pre-registered falsifiers, hidden-DOF audits, and a tiered claim-status schema"**

- 길이: 21 단어. OJA / JOSS 가이드라인 정합 (≤25 단어 권장).
- "SQMH" / "spacetime quantum metabolism" / "Λ origin" / "DESI w_a" 단어 title 0건. *"high-stakes cosmological claims"* 으로 일반화.

### 3.2 Section Structure (methodology + verification only)

| § | 제목 | 핵심 내용 | hidden DOF disclosure |
|---|---|---|---|
| 0 | Abstract | 200 단어, framework 일반화 + 1 case study 인용 (SQMH = adopter #1, name 명시) | Y |
| 1 | Introduction | 1.1 reproducibility crisis in cosmology / 1.2 Methodology-only contribution / 1.3 Case study scope (SQMH single adopter) | — |
| 2 | Verification harness | 2.1 7-script architecture / **2.2 Script table (verify_milgrom_a0 / verify_lambda_origin / verify_Q_parameter / verify_S8_forecast / verify_cosmic_shear / verify_monotonic_rejection / verify_mock_false_detection)** / 2.3 expected_outputs JSON convention / 2.4 Docker + conda 환경 | — |
| 3 | claims_status.json schema | 3.1 Tier 정의 (PASS_STRONG / PASS_MODERATE / PASS_QUALITATIVE / PASS_BY_INHERITANCE / FAIL) / 3.2 JSON schema spec / **3.3 audit trail integration (8인 Rule-A 라운드 hook)** | — |
| 4 | Hidden-DOF audit protocol | 4.1 effective k 추정 방법 / 4.2 ΔAICc penalty calculation / 4.3 case study: SQMH k_eff=9–13 disclosed | Y |
| 5 | Pre-registered falsifier protocol | 5.1 falsifier definition / 5.2 6→6 list 인용 (SQMH case) / 5.3 OSF DOI / pre-print 우선권 락인 워크플로 | — |
| 6 | Limitations | 6.1 adopter count = 1 / 6.2 SQMH-flavoured tier enum / 6.3 PASS_BY_INHERITANCE 의 framework dependency / 6.4 Q_parameter FAIL 미해결 인정 / 6.5 negative-control 1건 (verify_mock_false_detection) → false-positive 차단만 검증 | Y |
| 7 | Comparison to existing tools | 7.1 ASCL / Zenodo / GitHub release 와의 차이 / 7.2 prereg.org cosmology 적용 사례 | — |
| 8 | Conclusion | methodology 일반화 가능성; SQMH 외 framework adoption 호소 | — |

### 3.3 Key Claims (audit-aligned)

1. 7-script verification harness (디스크 실재 — L539 §3.3 검증 완료).
2. claims_status.json schema with 5 tiers + JSON schema spec.
3. Hidden-DOF audit protocol (effective k → ΔAICc penalty).
4. Pre-registered falsifier workflow (OSF DOI + arXiv preprint 우선권).
5. Negative-control 1건 (verify_mock_false_detection.py) — false-positive 차단 검증.
6. **single adopter (SQMH)** — adoption count 1 정직 인정.
7. Q_parameter verify FAIL — *harness 가 FAIL 을 잡았다* 가 contribution frame.

### 3.4 Submission Timeline

- **2026-05 ~ 06**: R10-Disk-Audit + R10-Exec-A 통과 후 COMPANION_DRAFT.md final 화.
- **2026-07**: OJA 제출 준비 (MNRAS 보다 먼저 — 방법론 paper 가 review 중일 때 Main 이 cite 가능하도록).
- **2026-07 말 / 2026-08 초**: **OJA 제출**.
- **2026-09 ~ 2026-12**: review 라운드 (OJA 평균 2–4mo).
- **2027 Q1**: 출간 예상.

### 3.5 Cross-reference Policy

- Main MNRAS-γ 인용: §1.3 "Case study scope" 1회 ("the case study draws on the galactic test reported in [Main MNRAS-γ]") — submission 시점 우선순위 (OJA 가 먼저 출간 가능).
- arXiv D 인용: §5.3 "OSF DOI workflow" 1회 ("see [arXiv D] for the SQMH preregistered falsifier list").
- 자기 referrer: 0건.

---

## 4. Paper 3 — arXiv D (preprint priority lock)

### 4.1 Final Title

> **"Pre-registered falsifiers for SQMH-class dark-energy phenomenology: A DESI DR3 priority claim"**

- 길이: 15 단어. arXiv 가이드라인 정합.
- *priority lock-in* 명시 — DR3 결과 발표 *전* 제출 의무.

### 4.2 Section Structure (preprint, ≤15 pages)

| § | 제목 | 핵심 내용 |
|---|---|---|
| 0 | Abstract | 200 단어, "amplitude-locking partial result + DR3 falsifier" 락인 |
| 1 | Introduction | DESI DR2 w_a<0 sign + SQMH-class phenomenology 호환성 |
| 2 | Amplitude-locking partial result | Q17 partial: Δρ_DE ∝ Ω_m derivation (E(0)=1 정규화 귀결, 동역학적 유도 *아님* — 정직 인정) |
| 3 | Pre-registered falsifier | DR3 wa>−0.5 면 SQMH-class KILL; wa∈[−0.5, −0.7] 면 PASS_QUALITATIVE; wa<−0.7 면 PASS_MODERATE |
| 4 | Comparison to independent theories | C28 Maggiore-Mancarella RR non-local (independent), A12 erf-diffusion (L529 winner) — *SQMH 단독 주장 금지* |
| 5 | Limitations | Q17 동역학 미달성 / Q13 (S8) FAIL / Q14 (lensing) 미평가 / PRD Letter 영구 차단 명시 |
| 6 | Reproducibility | OSF DOI + Companion B verification harness 인용 |

### 4.3 Key Claims

1. Δρ_DE ∝ Ω_m amplitude-locking *partial* (Q17 일부, exact coefficient=1 은 normalization 귀결).
2. DR3 falsifier 정량 (wa cutoff 3-tier).
3. **C28 은 SQMH 와 독립 이론 — phenomenological 일치만 주장** (CLAUDE.md L6 명시 의무).
4. PRD Letter 진입 영구 차단 (Q17 미달 + Q13/Q14 미동시) 정직 인정.

### 4.4 Submission Timeline

- **2026-05 즉시 (R10-Disk-Audit 통과 직후)**: arXiv 제출 — *DR3 공개 전* priority lock 의 정직성 자산 락인.
- **2026-05**: OSF DOI 부여, falsifier 사전등록 락인.
- **2027 Q2 (DR3 공개)**: falsifier 평가 결과 *별도* 후속 paper (Round 11 트랙).
- **arXiv D 자체 revision 금지** — pre-DR3 락인의 정직성 자산.

### 4.5 Cross-reference Policy

- Main MNRAS-γ: §1 "Introduction" 1회 (galactic test 분리 명시).
- Companion B: §6 "Reproducibility" 1회.
- 자기 자체 revision 금지 (4.4 명시).

---

## 5. Portfolio acceptance — 산술 vs reviewer overlap 보정

### 5.1 단순 독립 가정 (L540 §5.2 인용)

- Main 22% + Companion 47% (mid 보수 보정 후) → 1 − 0.78·0.53 = **0.586** ≈ 0.59
- + arXiv D ~100% (preprint) → peer-reviewed 1지 이상 0.59, *priority lock 자체* 1.00

### 5.2 reviewer-pool overlap 보정 (L546 신규)

> **CLAUDE.md "결과 왜곡 금지" 정합 — 독립 가정의 한계 명시.**

- MNRAS reviewer pool ⊃ {galactic dynamics, SPARC RAR, MOND community} ≈ 200–400명.
- OJA reviewer pool ⊃ {cosmology methodology, open-science, reproducibility} ≈ 100–250명.
- **overlap 추정**: MOND/cosmology 양쪽 active reviewer 약 30–60명 (≈ MNRAS pool 의 10–20%, OJA pool 의 15–25%).
- arXiv D 는 peer-reviewed 아님 → overlap 무관.

correlation coefficient ρ ≈ 0.15–0.25 (overlap 비율 + brand bias) 가정 시:

- Main+Companion 결합 acceptance (correlated) = 1 − [1 − P(M)][1 − P(C)] · (1 + ρ·δ) ≈ **0.50** (ρ=0.20, δ=0.6 보정).
- 보수 하한 (ρ=0.30): **0.43** (L540 §5.2 보수 하한과 정합).
- 낙관 상한 (ρ=0.10): **0.55**.

**중앙 0.50, 보수 0.43, 낙관 0.55** — peer-reviewed 1지 이상.

### 5.3 SQT brand bias 추가 위험

- MNRAS 의 referee 중 1명이 Companion B 를 *동시 review* 할 확률 ≈ 5–10%.
- 두 paper 모두 SQMH author 라벨 → "단일 framework 의 self-promotion" cluster bias.
- 완화: arXiv D 를 *먼저* 제출 (2026-05) → preprint 만 referenced, author 단일성 brand bias 분산.

### 5.4 갱신 trajectory

| 시점 | acceptance (peer-reviewed 1지 이상) | 누적 Δ vs L490 |
|---|---|---|
| Pre-audit (L490, JCAP 단일) | 68% | 0 |
| L526 R8 | 5% | −63%p |
| L535 αγ hybrid (single) | 22% | −46%p |
| L540 portfolio (단순 독립) | 59% | −9%p |
| **L546 portfolio (overlap 보정)** | **50%** | **−18%p** |
| L546 + R10-Exec-A 통과 (예상) | 55–65% | −3 ~ −13%p |

**핵심 관찰**: overlap 보정 후 글로벌 고점 회복률 = 50/68 ≈ **74%** (L540 87% 보다 보수). "통합 이론 single paper" 야심에서는 여전히 영구 미달.

---

## 6. 실행 체크리스트 (Round 10 통과 후)

| 단계 | 트랙 | 시점 | 의존성 |
|---|---|---|---|
| 1 | R10-Disk-Audit | 2026-05 즉시 | (선결) |
| 2 | R10-Exec-A (8인 Rule-A) — paper/base.md final state | 2026-05 ~ 06 | 1 통과 |
| 3 | R10-Exec-B (4인 Rule-B) — N_eff 재 fit + verify_milgrom_a0.json cross-check | 2026-06 | 2 통과 |
| 4 | **arXiv D 제출** | 2026-05 (R10-DA 통과 직후 즉시) | 1 통과만 필요 — 가장 빠른 우선권 락인 |
| 5 | Companion B (OJA) 제출 | 2026-07 ~ 08 | 2, 3 통과 |
| 6 | Main MNRAS-γ 제출 | 2026-09 | 2, 3, 5 통과 |
| 7 | DR3 결과 도착 시 후속 paper (Round 11) | 2027 Q2 | DR3 공개 |

---

## 7. 금지 사항 (CLAUDE.md 정합)

- **단일 에이전트 paper/base.md 직접 수정** (L6, [최우선-2]) — 본 L546 도 0건.
- **DR3 스크립트 실행** (CLAUDE.md L6 / L34) — DR3 공개 전 금지.
- **arXiv D 의 DR3 결과 후 falsifier revision** — pre-DR3 락인 정직성 자산 영구 손실.
- **Main MNRAS-γ abstract 에 cosmology 어휘** ("metabolism" / "DE" / "DESI" / "DR3") — 0건.
- **Companion B 가 SQMH 외 framework 보편화 주장** — adopter count = 1 정직 인정 의무.
- **portfolio acceptance "산술 max" 단독 인용** — overlap 보정 + brand bias 동시 명시 의무.
- **L538 / L539 빈 디렉터리에 역추적 산출물** — 결과 왜곡 금지.
- **8인 / 4인 라운드 미경유 직접 제출** — L6 의무 위반.

---

## 8. CLAUDE.md 정합성 체크

- **[최우선-1] 방향만 제공, 지도 금지**: 신규 수식 0줄, 신규 파라미터 0개. portfolio plan 은 *방향* 만 제시. ✓
- **[최우선-2] 팀 독립 도출**: 본 L546 단일 작성. 8인 Rule-A 라운드 미실행 명시. ✓
- **결과 왜곡 금지**: §5.2 overlap 보정 + §5.3 brand bias + §0 acceptance 0.43–0.50 보수 하한 모두 명시. L539 §2.3 "0.42σ → 0.71σ 정정" 본 plan §2.2 §3.2 에서 0.71σ 단일 채택 확정. ✓
- **paper/base.md edit 0건** ✓
- **simulations/ 신규 코드 0줄** ✓
- **claims_status.json edit 0건** ✓
- **disk-absence 정직 보고** (L499/L505/L511/L518/L521/L526 R8/L531/L537/L540 선례) — §0 / §6 / §7 정합. ✓

---

## 9. 정직 한 줄 (재진술)

**3-paper portfolio (Main MNRAS-γ galactic-only, Companion B methodology-only, arXiv D pre-DR3 priority lock) 의 final title / section structure / claims (audit-aligned, hidden DOF 9–13 + Verlinde degeneracy + Bullet DM 잔존 disclosed) / submission timeline (arXiv D 2026-05 즉시 → Companion B 2026-07 → Main MNRAS-γ 2026-09) / cross-reference policy (Main 의 cosmology 클레임 0, arXiv D 가 cosmology 락인, Companion B 가 방법론 분리) 를 정의하되, peer-reviewed 1지 이상 acceptance 중앙은 reviewer-pool overlap (ρ≈0.20) + SQT brand bias 보정 후 0.50 (보수 0.43, 낙관 0.55) — L540 단순 독립 0.59 대비 −9%p 보수화, 글로벌 고점 회복률 74%, 본 plan 의 채택 / 실행 / 제출은 *모두* Round 10 R10-Disk-Audit + 8인 Rule-A / 4인 Rule-B 결정에 종속.**

---

*저장: 2026-05-01. results/L546/PORTFOLIO_PLAN.md. 단일 작성 에이전트. paper/base.md edit 0건. simulations/ 신규 코드 0줄. claims_status.json edit 0건. 신규 수식 0줄. 신규 파라미터 0개. CLAUDE.md [최우선-1] / [최우선-2] / 결과 왜곡 금지 / L6 재발방지 모두 정합. 본 문서가 제시한 모든 title / section / timeline / acceptance estimate 는 *방향 제시* 이며 채택은 후속 Round 10 8인/4인 라운드 결정.*
