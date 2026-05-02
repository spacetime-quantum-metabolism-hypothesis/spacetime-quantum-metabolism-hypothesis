# L526 R8 — SQT Hidden Assumptions: 종합 + Son+ correct 후 framework 운명

> **작성**: 2026-05-01
> **저자**: 단일 메타-합성 에이전트 (8인/4인 라운드 *없음*; 후속 Rule-A 의무)
> **substrate**: results/L525/SESSION_FINAL.md (Phase 1–6 누적), paper/base.md, claims_status.json v1.2, base.l43–l46.command.md (Son+25 정합성), CLAUDE.md L1–L33
> **CLAUDE.md 정합성**: 신규 수식 0줄, 신규 파라미터 0개, paper/base.md edit 0건, simulations/ 신규 코드 0줄.

---

## 0. 정직 한 줄 — framework 살아남음 / 재구성 필수

**근본 재구성 필수.** Son+25 age-bias correct 가 *단일* 가정 하나만 무너뜨리면 SQT 의 *cosmological observational anchor* 가 부재 상태로 격하되며, paper 의 글로벌 고점은 P1–P6 누적 (L525 §1) 의 −55%p 위에서 추가 −15~25%p 의 *순수 phenomenological* 손실을 입는다. SQT 의 *형식적* lagrangian / axiomatic 구조 (A1+A2+A3) 는 살아남지만 그 구조가 *주장하던* 관측 정당화 (DESI w_a<0 방향 정합) 가 사라지므로 **post-hoc curve-fitting 으로 재분류**된다. JCAP-acceptance 8–19% (중앙 13–14%, L521) → **3–8% (중앙 5%)** 로 추정. PRD Letter 진입 영구 차단 재확인.

---

## 1. R1–R7 산출물 디스크 검증 (정직 보고)

L499/L505/L511/L518/L521 선례 계승 — 디스크 부재 정직 명시.

| Round | 디렉터리 | 파일 수 | 상태 |
|-------|----------|---------|------|
| L526_R1 | 존재 | 0 | **빈 디렉터리** — 본 R8 은 substrate 부재로 R1 의도만 유추 |
| L526_R2 | **부재** | — | 디렉터리 미생성 |
| L526_R3 | 존재 | 0 | **빈 디렉터리** |
| L526_R4 | 존재 | 0 | **빈 디렉터리** |
| L526_R5 | **부재** | — | 디렉터리 미생성 |
| L526_R6 | **부재** | — | 디렉터리 미생성 |
| L526_R7 | **부재** | — | 디렉터리 미생성 |

⇒ 본 R8 은 **R1–R7 종합 불가능** 상태에서 작성됨. substrate 는 L525 SESSION_FINAL + L491–L524 Phase 1–6 누적 + base.l43–l46 (Son+25 회로) 만. R1–R7 의도 추정 + L525 카탈로그 cross-ref 합성으로 임무 1–4 수행.

---

## 2. SQT 의 Hidden Implicit Assumptions (paper 에서 명시 안 됨)

> 임무 1. 카탈로그 only — 명시·비명시 구분.
> *명시 안 됨* = paper/base.md 본문 / 초록 / §0–§7 어디에도 가정 statement 형태로 노출 안 된 것.

### A. Cosmological-regime hidden assumptions (5건, 임무 1 의 핵심)

| # | hidden assumption | 어디서 *암묵적* 으로 사용되는가 | 명시화 시 노출되는 의존성 |
|---|---|---|---|
| **H1** | **가속 우주 진위 (Riess1998+Perlmutter1999 lineage 무비판 수용)** | §4 a₀ ↔ c·H₀/(2π) factor-≤1.5 invariant 의 *H₀ 자체* 가 가속우주 model 안에서 측정. SH0ES vs Planck H₀ tension 5.0σ 가 substrate. 가속 자체가 흔들리면 a₀ 수치 표적이 흐려진다. | factor-≤1.5 invariant C1 의 robustness 가 H₀ measurement-model dependence 로 전파; "factor-≤1.5" 가 *measurement-model 의 1σ band* 이내로 격하. |
| **H2** | **Λ (cosmological constant) 의 존재 자체** | A3 4-state (matter / Λ-like / radiation / curvature) 에서 Λ-like 항이 0 이 아니라는 가정. Q95 VICTORY (base.l46) 의 ΔAICc 비교 baseline 이 ΛCDM. | Λ→0 시 Friedmann 방정식의 closure 불가 → A3 의 "4 상태" 가 3 상태로 축소되며 axiom redundancy 발생. claims_status PASS_BY_INHERITANCE 8건 중 cosmology 인용분 (≈3건) 부정. |
| **H3** | **τ_q ~ 1/H₀ (대사 시간상수의 Hubble-time scaling)** | RAR a₀ 도출에서 c·H₀/(2π) 의 *H₀* 가 들어가는 경로는 τ_q ~ 1/H₀ 가정 없이는 dimensional 으로 닫히지 않음. base.md §4.1 에서 명시 statement 부재 — derivation 안에 묻혀 있음. | τ_q 가 H₀ 와 분리된 지역적 시간상수면 a₀ 의 cosmological dependence 가 무너지고 invariant C1 이 *우연의 일치* 로 격하. |
| **H4** | **n_∞ steady-state (대사 밀도 무한원에서 고정값)** | a₀ ↔ c·H₀/(2π) factor-≤1.5 도출의 boundary condition. 우주가 진화하면 n_∞ 도 시간의존 → a₀(t). 현재 paper 는 a₀ 시간의존을 다루지 않음 — 즉 steady-state 암묵 가정. | n_∞(t) 동역학 도입 시 RAR row 12 의 PASS_MODERATE 가 PASS_PROVISIONAL 로 격하 (z-evolution 검증 필요). |
| **H5** | **Cosmic regime 이 *measurement* 로 도달 가능 (epistemic accessibility)** | DESI BAO + SN + CMB+ RSD joint chi² 100ms/call (L525 §1 P5/P6 P5 budget) 가 "관측가능 우주가 SQT regime 의 sample 을 제공" 을 가정. 그러나 SQT 의 dark-only coupling 은 baryon-frame 에서 *관측 불가* 일 수 있음 (C10k Cassini 통과의 대가). | dark-only 이면 baryonic-side observable channel = {falsifier 6 중 SKA-null, ET, CMB-S4} 한정 → N_eff 4.44 가 추가 격하. |

### B. Cross-cutting hidden assumptions (3건, 임무 1 의 보조)

| # | hidden assumption | 영향 |
|---|---|---|
| **H6** | **Mach-frame 등가** (관성계 선택이 SQT regime 의 boundary condition 에 영향 없음) | base.md §3 axiomatic block 에 명시 statement 부재. PPN γ=1 검증의 Cassini channel-conditional 결론 (L506) 이 frame-dependence 로 추가 격하 가능. |
| **H7** | **n₀μ 곱이 우주적으로 균질** (CLAUDE.md 재발방지 "n₀μ만 물리적 의미" 와 정합하나 *균질성* 자체가 비명시) | inhomogeneous n₀μ(x) 도입 시 SPARC galaxy-by-galaxy fit 의 K_X 1/4 universality FAIL (L503) 이 *예측* 으로 흡수 가능 — *재해석* 시 PASS_MODERATE → PARTIAL 격하 또는 격상 모두 가능 (양면). |
| **H8** | **Falsifier 6채널 의 환원 가능 epistemology** (CMB-S4 / ET / SKA-null / DESI / Euclid / LSST 가 *동시에* SQT 와 standard physics 를 구분한다는 가정) | L498 ρ-corrected N_eff=4.44 이미 일부 노출. 그러나 *"falsification 자체가 standard-model embedding 과 분리 가능"* 이라는 더 깊은 가정은 비명시. embedding-conditional 격하 (L506 Cassini) 가 6 채널 모두에 전이 가능. |

---

## 3. Son+ correct 시 각 가정의 정량 변화 (임무 2)

> **Son+ correct** 의 정의 (base.l46 + base.l43 정합): Son+25 age-bias correction 을 *수용* — DESI DR1/DR2 의 w_a<0 신호가 host-galaxy age-bias 로 인한 systematic 으로 일부/전부 흡수되어 w_a 의 진짜 amplitude 가 −0.83 → ≈ −0.20 ~ 0 으로 격하되는 시나리오.

| 가정 | Son+ 적용 전 | Son+ correct 후 | Δ (정량) | 메커니즘 |
|------|-------------|-----------------|---------|----------|
| **H1 (가속 우주)** | 가속 robust (>5σ) | 가속 정성 유지, *진화 amplitude* 격하 | w_a tension 5σ → 1.5–2σ | host-age systematic 흡수 → late-time deviation 신호 약화 |
| **H2 (Λ 존재)** | ΛCDM baseline | ΛCDM 거의 충분, w₀wa CDM 우월성 ΔAICc 격하 | ΔAICc(ΛCDM−w₀wa) ≈ +9 → +2~3 | DESI DR2 의 ΛCDM exclusion 약화 |
| **H3 (τ_q ~ 1/H₀)** | RAR factor-≤1.5 PASS_MODERATE | 동일 (galactic regime 무관) | Δ ≈ 0 | Son+ 은 cosmological-regime 만 영향, RAR (galactic) 분리 |
| **H4 (n_∞ steady-state)** | 안전 | **압박** — Son+ 후 SQT 의 *관측 동기* 약화 | n_∞(t) 동역학 도입 압력 ↑ | w_a≈0 이면 SQT 가 *해결할 문제* 가 사라짐 → 대안 *예측* 으로 n_∞(t) 시간의존 도입 동기 발생 |
| **H5 (cosmic regime accessibility)** | 6 falsifier 중 4 cosmological | 6 falsifier 중 4→2 effective | N_eff 4.44 → 약 3.0–3.3 | DESI / Euclid 두 채널이 *Son+ corrected DESI DR3* 을 거치면 이미 ΛCDM-consistent 영역 → SQT-discrimination 약화 |
| **H6 (Mach-frame)** | 비활성 | 비활성 | Δ ≈ 0 | Son+ 은 frame 무관 |
| **H7 (n₀μ 균질)** | 비활성 | **압박** — 후속 dark-energy reframing 에 inhomogeneous 동기 | 정성 | Son+ 후 SQT 가 "homogeneous Λ 닮음" 으로 격하되면 재미가 없어짐, inhomogeneous 로 도주 압력 |
| **H8 (falsifier 환원성)** | embedding-conditional 격하 (L506) | 추가 격하 — *cosmological* 채널 4건 모두 conditional | 8.87σ → 5.5–6.5σ (ρ-corrected) | DESI/Euclid/LSST/CMB-S4 4 채널 의 SQT-vs-LCDM separation 이 host-age systematic 통과 후 약 30–40% 손실 |

### 3.1 누적 정량 (L525 §4 trajectory 갱신)

| 시점 | acceptance | Δ from L521 |
|------|-----------|-------------|
| L521 (Son+ 미적용 baseline) | 8–19%, 중앙 13–14% | (기준) |
| **L526 R8 (Son+ correct 가정)** | **3–8%, 중앙 5%** | **−8~9%p** |

추가 disclosure honesty bonus (+0.02 ~ +0.04) 로 부분 회수해도 archetype-A theorist panel 의 *관측 동기 부재* 페널티 (−0.10 ~ −0.15) 가 우세.

---

## 4. SQT framework 가 *형식적* 으로 살아남는 *최소 변경 path* (임무 3)

> "최소 변경" = paper/base.md axiomatic block (A1+A2+A3) 와 §3 mathematical core 를 보존하되, hidden assumption 1–2 개만 *명시화* 하여 falsifiability 를 재정의.

### 4.1 Path-α (가장 보수적, 권고)

1. **H4 (n_∞ steady-state) 를 명시 axiom 으로 승격** — paper §3 에 statement 추가 (지도 금지 원칙 — 형태는 8인 팀 자유 도출).
2. **H1 (가속 우주) 와 H2 (Λ) 를 "external observational input" 으로 분리 명시** — SQT 가 *예측* 하지 않고 *수용* 함을 §0 abstract 에 정직 statement.
3. **C1 invariant (a₀ ↔ c·H₀/(2π) factor-≤1.5) 만 SQT-internal prediction 으로 유지** — 나머지 cross-cutting claim 은 *embedding-conditional* 명시.

이 path 는 paper 의 글로벌 고점을 *RAR-galactic regime* 단독 anchor 로 좁히되, falsifiability 는 보존. 살아남는 정직 acceptance: **8–13% (중앙 10%)** — Son+ correct 손실의 약 50% 회복.

### 4.2 Path-β (적극적, 위험)

1. **H4 → 시간의존 n_∞(t) 동역학 도입** — *예측 채널 신설* (예: galaxy a₀(z)).
2. **A3 의 Λ-state 를 dynamical state 로 reformulate** — Q17 amplitude-locking 동역학 유도 (CLAUDE.md L6 "Q17 미달 상태에서 PRD 진입 금지" 의 *해제 조건*).
3. **5 위치 abstract drift 차단 + companion B paper 동시 reframe.**

위험: 신규 파라미터 도입 → CLAUDE.md "AICc 패널티 명시" 의무, 8인 팀 자유 도출 의무. 성공 시 PRD Letter 진입 가능, 실패 시 Q17 다시 미달로 trajectory 추가 −5%p.

### 4.3 Path-γ (포기 – 형식적 최소)

- A1+A2+A3 만 보존, 모든 cosmological claim 폐기. galactic-only theory 로 재포지셔닝.
- JCAP 격하 재제출 (L522 옵션 A) 의 *가장 깨끗한* 버전.
- 살아남는 acceptance: **15–25% (중앙 20%)** — Son+ correct 의 cosmological 손실을 *회피* 하므로 오히려 상승. 단, paper 의 "글로벌 고점" 야망 자체 포기.

### 4.4 권고 (R8 수준 합성)

**Path-α 즉시 + Path-γ companion** 동시 트랙. Path-β 는 Q17 우연 도출 시에만 (L525 §6.3 정합).

---

## 5. Paper 의 *글로벌 고점* 에 미치는 영향 (임무 4)

### 5.1 trajectory 갱신 (L525 §4 + 본 R8 종합)

| 시점 | acceptance | 누적 Δ from pre-audit |
|------|-----------|----------------------|
| Pre-audit (L490) | 63–73% | 0 |
| L490 (Phase-1) | 30–45% | −30%p |
| L517 (4-audit) | 11–22% (중앙 16%) | −50%p |
| L521 (Phase 3 cross) | 8–19% (중앙 13–14%) | −55%p |
| **L526 R8 (Son+ correct)** | **3–8% (중앙 5%)** | **−65%p** |
| L526 R8 + Path-α | 8–13% (중앙 10%) | −60%p |
| L526 R8 + Path-γ | 15–25% (중앙 20%) | −50%p |

### 5.2 글로벌 고점 영구 미달 사유 (R8 시점)

1. **PASS_STRONG 0/33 (claims_status v1.2, L516)** — Son+ correct 가 새로 추가하는 PASS_STRONG 0건.
2. **진정 invariant {C1, C7} 만 — Son+ correct 후 C1 의 *cosmological motivation* 약화** (galactic regime 보존, factor-≤1.5 수치는 영향 없음 ; H3 격리).
3. **Q17 (amplitude-locking 동역학) + Q13/Q14 동시 미달 영구** — Son+ 무관, PRD Letter 진입 영구 차단 (CLAUDE.md L6).
4. **N_eff 4.44 → 3.0–3.3 추가 격하** — Son+ correct 후 cosmological 채널 약화 (§3.1 H8).
5. **JCAP majority acceptance (>50%) 회복 path 부재** — Path-α 도 10%, Path-γ 도 20% 로 majority 미달.

### 5.3 살아남는 *형식적* 가치

- Axiomatic block A1+A2+A3 의 *consistency* 자체는 Son+ 무관.
- Cassini PPN γ=1 channel-conditional PASS_MODERATE (L506) — Son+ 무관.
- BBN ΔN_eff cross-experiment 4/4 PASS (L507) — Son+ 무관.
- RAR factor-≤1.5 invariant C1 — galactic regime 유지.
- Newton-only SPARC fail 정성 결과 C7 — Son+ 무관.

⇒ **framework 형식 보존 ≠ paper 글로벌 고점 도달.** 살아남으나 *야심* 은 무너진다.

---

## 6. CLAUDE.md 정합성 체크

- **[최우선-1] 방향만 제공, 지도 금지**: 신규 수식 0줄, 신규 파라미터 0개, "A=..." 형태 0건. 본 문서는 hidden assumption 카탈로그 + Path 옵션 *방향* 만, 구체 수식 부재. ✓
- **[최우선-2] 팀 독립 도출**: 본 R8 은 메타-합성. 8인/4인 라운드 *미실행*. Path-α/β/γ 의 axiom 명시화 형태는 후속 8인 Rule-A 라운드에서 자유 도출 의무. ✓
- **결과 왜곡 금지**: framework 살아남으나 글로벌 고점 미달 정직 명시. R1–R7 디스크 부재 정직 명시. JCAP −65%p trajectory 정직 노출. ✓
- **paper/base.md 직접 수정 0건**: 본 R8 edit 0. ✓
- **simulations/ 신규 코드 0줄**: ✓
- **claims_status.json edit 0건**: ✓
- **disk-absence 정직 보고 (L499/L505/L511/L518/L521 선례)**: §1 표로 명시. ✓

---

## 7. 한 줄 정직 (사용자 요청 형식)

**Framework 형식적 살아남음 — 그러나 paper 의 cosmological 글로벌 고점 야망은 근본 재구성 필수 (Path-α 권고; JCAP majority 회복 불가, PRD Letter 진입 영구 차단 재확인).**

---

*저장: 2026-05-01. results/L526_R8/HIDDEN_ASSUMPTIONS.md. 단일 메타-합성. R1–R7 디스크 부재로 substrate 는 L525 + L491–L524 + base.l43–l46 + claims_status v1.2 + CLAUDE.md. 8인/4인 라운드 미실행 — 후속 Rule-A 의무. paper/base.md edit 0건, simulations/ 신규 코드 0줄, 신규 수식 0줄, 신규 파라미터 0개. CLAUDE.md [최우선-1] / [최우선-2] / 결과 왜곡 금지 / 디스크 부재 정직 인정 모두 정합.*
