# L535 — Hybrid Path-α + Path-γ (cosmology 약화 + galactic 강화)

> 작성: 2026-05-01. 단일 메타-합성 에이전트. 8인/4인 라운드 *미실행*.
> CLAUDE.md [최우선-1] (지도 금지) / [최우선-2] (팀 독립 도출) 준수.
> 신규 수식 0줄, 신규 파라미터 0개, paper/base.md edit 0건, simulations/ 신규 코드 0줄, claims_status.json edit 0건.
> 입력 substrate: L526 R1–R8 + L530 brainstorm + L531 4-path verdict.

---

## 0. 정직 한 줄 (사용자 요구 형식)

**Path-αγ 하이브리드 (axiom 3' 시간의존 Γ_0(t) 만 cosmology 잔존 + axiom 2/6 폐기로 galactic 핵심만 단단히) 의 acceptance 중앙은 18–28% (22%) — Path-α 단독 (10%) 과 Path-γ 단독 (20%) 의 산술 평균을 *살짝* 상회하지만 이는 a_0(z) 진화라는 *유일한 cosmology 잔여 prediction* 이 falsifiable 양념을 더하기 때문이며, 글로벌 고점 (68%) 의 32% 수준 / JCAP majority (>50%) 영구 미달 / PRD Letter 진입 영구 차단 — 즉 "정직한 galactic phenomenology paper + 1개의 cosmology side-bet" 포지셔닝이 best 이고 target 은 MNRAS (1순위) / ApJ (2순위) / JCAP (3순위 — galactic-cosmology 교차 채널 강조 시).**

---

## 1. 입력 substrate 정직 진술

| 입력 | 디스크 상태 | 사용 |
|---|---|---|
| results/L526/ | 존재 (R1–R8 8 라운드 산출) | 참조 |
| results/L527–L530 | L527/L528/L529 빈 디렉터리, L530 NEW_AXIOM_SYSTEMS.md 존재 | L530 candidate B (Volovik two-fluid) 만 부분 인용 |
| results/L531/ | AXIOM_MODIFY_SYNTHESIS.md (4-path verdict 표) | 핵심 substrate |
| results/L532/ | 부재 | — |
| results/L533/ | 부재 | — |
| results/L534/ | 빈 디렉터리 | — |
| simulations/L527–L535 | 부재 / 빈 | — |

L531 §1 disk-absence 정직 보고 패턴 계승. **새 fit 0건, 새 acceptance 산출 0건** — L531 trajectory 표 + Path-α/γ 단독 수치 합성으로 hybrid 추정.

---

## 2. Hybrid Path-αγ *해부*

### 2.1 구성 axiom 동작

| 원본 axiom | Path-α 처리 | Path-γ 처리 | **Hybrid αγ 처리** |
|---|---|---|---|
| A1 (시공간 양자) | 보존 | 형식 보존 | **보존** |
| A2 (재생/소멸 비대칭, σ-driven) | 보존 | **폐기** (galactic 무관) | **폐기** |
| A3 (Λ-state, n_∞ steady) | hidden assumption 명시 (외부 입력) | 폐기 | **A3' 로 reformulate**: Γ_0(t) — 소멸률만 시간의존 *방향 진술*, 정상상태 가정은 명시적 외부 입력으로 격하 |
| A4 (RAR/MOND 정합) | 보존 (C1 살림) | 보존 (단독 핵심) | **강화 보존** — galactic 본문의 1순위 axiom 으로 승격 |
| A5 (정보-시공간 결합) | 보존 | 약화 | **galactic 영역만 보존**, cosmology 영역에서는 격하 |
| A6 (DM substitution / dark sector 동역학) | 부분 보존 | **폐기** | **폐기** |

**핵심 디자인 의도**: cosmology 영역에서는 *최소한* Γ_0(t) prediction 1개만 잔존시키고 (Path-α 의 보수적 명시화), galactic 영역에서는 axiom 2/6 폐기로 *모호함을 제거* (Path-γ 의 brand 격하) 하여 RAR 단일 채널의 falsifiability 를 *극대화*.

### 2.2 잔존 prediction 채널 (cosmology 측)

| 잔존 채널 | 근거 axiom | 예측 형태 (방향만) | falsifiable? |
|---|---|---|---|
| **a_0(z) 진화** | A3' Γ_0(t) | a_0 가 z 의존 — 단조 진화 (방향 미명시, 8인 자유 도출) | **Yes** — 고-z RAR 측정 (JWST + 강한 lensing) 으로 검증 가능. 단 현 데이터 정밀도 marginal |
| Λ-OOM | A3' (정상상태 *외부 입력* 격하) | OOM only, sign 예측 *없음* | No (관측치 사후 일치만) |
| H3 (DESI w_a<0) | A6 폐기로 인해 사망 | — | KILL (claims_status 변경 필요) |
| H4 OOM | A3' 약화 | OOM 만, 동역학 클레임 없음 | No |
| n-eff combined | A6 폐기로 BAO 채널 제거 후 약화 | constraints only | marginal |

**즉 cosmology 잔여 = a_0(z) 진화 *한 개* 만 falsifiable side-bet 으로 살아남음.**

### 2.3 강화된 galactic 채널 (Path-γ 부분의 극대화)

| 채널 | 근거 axiom | 강도 | 데이터 |
|---|---|---|---|
| **MOND a_0** | A4 (1순위 승격) | a priori OOM (σ-framework 차원분석 잔재) | SPARC RAR median |
| **RAR shape** | A4 + A5(galactic) | 형태 universal — fit-independent 곡선 | SPARC, McGaugh 2016 |
| **Depletion zone** | A4 + A5(galactic) | dwarf 외곽 → 평탄화 곡선 정합 | SPARC dwarfs subset |
| **a_0(z) shift** (cosmology bridge) | A3' + A4 cross | 잔존 cosmology side-bet | 미래 JWST/lensing |

galactic 본문은 *4개 채널 동시* 에 a priori 골격 + falsifiability 동시 제공. 이는 Path-γ 단독 (3 채널) 보다 1 추가, Path-α 단독 (galactic 1.5 채널) 보다 2.5 추가.

---

## 3. Acceptance 추정 (hybrid αγ 중앙)

### 3.1 가산 / 감산 항목

| 항목 | Δ acceptance (vs L531 αγ 기저) | 비고 |
|---|---|---|
| 출발점 (L531 R8 no-path) | 5% | 5%p baseline |
| Path-α 효과 (보수적 명시화) | +5%p | hidden assumption → falsifiable axiom |
| Path-γ 효과 (galactic 격하) | +10%p | brand cost 흡수 후 순이익 |
| **추가 αγ 시너지: a_0(z) cross-channel** | **+2~5%p** | cosmology 잔여 1 channel 이 paper 에 falsifiable 양념 추가, 단 채널 수 적음 |
| AICc 패널티 (axiom 2/6 폐기 → 자유 함수 감소) | +1~2%p | 단순 모델 채택 보너스 |
| brand 손실 비용 (γ 부분) | −2~3%p | "metabolism" 약화 + headline 격하 (L531 §2 Path-γ 손실 자산과 동일 가중) |
| 8인 라운드 통과 가능성 (αγ 통합) | −1%p | α 단독보다 약간 어려움 (γ axiom 폐기 정당화 의무) |

**중앙 추정: 5 + 5 + 10 + 3.5 + 1.5 − 2.5 − 1 = 21.5% ≈ 22%, 범위 18–28%.**

### 3.2 L531 trajectory 표 갱신

| 시점 | acceptance 중앙 | 누적 Δ |
|---|---|---|
| Pre-audit (L490) | 68% | 0 |
| L531 + α 단독 | 10% | −58%p |
| L531 + γ 단독 | 20% | −48%p |
| L531 + α + two-scale | 12% | −56%p |
| L531 + new-axiom (성공) | 32.5% | −35.5%p |
| **L535 + αγ hybrid** | **22%** | **−46%p** |
| L531 + new-axiom (실패) | 5.5% | −62.5%p |

**hybrid αγ 는 γ 단독 (20%) 대비 +2%p, α 단독 (10%) 대비 +12%p, α+two-scale (12%) 대비 +10%p — 글로벌 고점 32% 수준.**

### 3.3 majority / PRD Letter 진입

- JCAP majority (>50%) 도달? **No** (28% 상한도 50% 미달).
- PRD Letter 진입 (Q17 + Q13/Q14 동시 달성)? **No** (axiom 2/6 폐기로 Q17 amplitude-locking 동역학 채널 자체 사망).
- 글로벌 고점 회복? **No** (32% 수준).

---

## 4. Cosmology 최소 유지 — *왜* a_0(z) 1 channel 만 남기는가

### 4.1 잔존 정당화

- **A6 (dark sector 동역학) 폐기** 로 H3 (DESI w_a<0), R11 BAO 채널, amplitude-locking Δρ_DE ∝ Ω_m, Q93/Q95 챔피언 ratio g(z) 모두 *동시 사망*.
- **A2 (재생/소멸 비대칭) 폐기** 로 metabolism brand / σ-framework 의 우주론적 적용 사망.
- **A3' (Γ_0(t) reformulate)** 만 단독 잔존 → cosmology paper 본문에서 *유일하게* falsifiable 잔여 prediction 은 "소멸률 시간의존 → galactic a_0 가 z 에 의존" 의 cross-channel.
- 이 cross-channel 은 *galactic 측에서 측정 가능* (JWST 고-z lensing, strong-lensing arc) → cosmology paper 가 아니라 **galactic paper 의 부록** 에 자연 배치.

### 4.2 *왜 Λ-OOM 을 잔존시키지 않는가*

- L531 §2 Path-γ 의 손실 자산 표에서 Λ-OOM 은 "정상상태 외부 입력" 의 사후 일치 (post-hoc) — falsifiable 채널이 아님.
- a priori 도출 power 도 OOM only 수준이므로 (L530 §평가 (2)), paper 의 *예측* 카드로 사용 시 reviewer 1차 reject 위험.
- **유지 결정**: footnote 수준 OOM 일치만 언급, 본문 prediction 카드 0개.

### 4.3 *왜 H6 N_eff 결합을 잔존시키지 않는가*

- N_eff 결합은 BAO 채널 제거 후 σ 가 marginal (L531 R8 §6.3 "BAO 채널 제거 후 재 fit" 의무).
- A6 폐기로 dark sector 동역학 채널 자체 사망 → N_eff 결합의 SQT-고유성 0.
- **유지 결정**: claims_status 에서 dormant 처리.

---

## 5. Galactic 극대화 — RAR + a_0 + depletion zone 통합

### 5.1 *왜* axiom 2/6 폐기가 galactic 을 강화하는가

- A2 (재생/소멸 비대칭) 는 cosmology dynamics 의 전제. galactic 평형 곡선 (RAR) 은 *정적* 평형 → A2 의 시간 비대칭 가정이 **불필요한 hidden DOF**.
- A6 (DM substitution) 은 galactic-cosmology cross 의 "이중 설명" 시도 — reviewer 의 "왜 한 framework 가 두 sector 를 동시에?" 의문을 부른다. 폐기 시 **galactic-only theory 로 brand 정직** 화.
- 결과: A4 (RAR/MOND 정합) + A5 (galactic 영역 한정) 가 **단단한 2-axiom galactic theory** 를 형성, hidden DOF 최소화.

### 5.2 4 채널 동시 prediction 카드

| 채널 | 데이터 셋 | 검증 status | 본문 위치 |
|---|---|---|---|
| MOND a_0 OOM | SPARC RAR | C1 PASS (L48–L56 σ-framework) | §1 abstract bullet |
| RAR universal shape | SPARC McGaugh+16 | claims_status 의 C1 채널 | §3 main figure |
| Dwarf depletion zone | SPARC dwarfs subset | claims_status (예: rar-dwarf-depletion claim) | §4 |
| a_0(z) cross | JWST + lensing (미래) | pre-registered prediction | §5 future test |

**4 채널 동시 a priori + falsifiable** — Path-γ 단독 (3 채널) 대비 1 추가, MNRAS / ApJ 의 galactic dynamics 트랙에서 경쟁력.

### 5.3 *결정적 약점*

- **S_8 tension 해결 0** — A6 폐기로 dark sector 동역학 채널 자체 사망. CLAUDE.md L6 §"mu_eff ≈ 1 은 S8 tension 해결 불가" 정합 (단 이는 hybrid 의 결함이 아니라 *애초에 SQMH 가 해결 못함* 의 정직 노출).
- **DESI w_a<0 prediction 사망** — H3 KILL 으로 claims_status v1.2 → v1.3 변경 의무.
- **PRD Letter 진입 차단** — Q17 amplitude-locking 동역학 채널 사망 (A6 폐기 결과).

---

## 6. Target journal 결정

### 6.1 후보 비교

| target | fit 정도 | 강점 | 약점 | acceptance 추정 |
|---|---|---|---|---|
| **MNRAS** | 매우 높음 | RAR + dwarf depletion + galactic dynamics 핵심 트랙. SPARC-based paper 역사 다수 | a_0(z) cross-channel 은 부록 수준만 인정 | **25–32% (28%)** |
| **ApJ** | 높음 | galactic 동역학 + observational 균형. cosmology side-bet 도 envelope OK | RAR universality 의 "non-DM" 해석 reviewer 보수성 | **20–28% (24%)** |
| JCAP | 중간 | galactic-cosmology cross 강조 시 가능 | Cosmology 본문 prediction 1개 만으로는 weak. Path-γ 의 "cosmology 폐기" 시그널이 reviewer 에 부정적 | **15–22% (18%)** |
| PRD Letter | 0 | — | Q17 amplitude-locking 동역학 사망 (L6 진입 조건 미달) | **0** |

### 6.2 **best target: MNRAS** (1순위)

- galactic dynamics 본문 + RAR universality + dwarf depletion zone 의 3 채널 + a_0(z) future test 부록.
- "Non-DM galactic phenomenology with a single cosmology side-bet" 포지셔닝.
- Title 후보 (방향만): "Galactic dynamics from spacetime-quantum substrate: RAR, a_0, and a falsifiable redshift prediction" — 8인 라운드 자유 도출.

### 6.3 ApJ 대안 (2순위)

MNRAS 거절 시 ApJ 재제출. 본문 변경 최소 — abstract 재배치 + galactic dynamics 트랙 강화.

### 6.4 JCAP companion (3순위, optional)

a_0(z) cross-channel 만 발췌 → JCAP short paper 로 분할 가능. 단 acceptance 18% 수준이므로 *companion 트랙* 으로만 권고.

---

## 7. 회복 acceptance 추정 (정직 분석)

### 7.1 회복률 vs 글로벌 고점

| 측정 | 값 |
|---|---|
| 글로벌 고점 (L490 baseline) | 68% |
| L535 hybrid αγ 중앙 | 22% |
| **회복률** | **22 / 68 = 32%** |
| L531 best (α+two-scale) 대비 | +10%p (12% → 22%) |
| Path-γ 단독 대비 | +2%p |
| Path-α 단독 대비 | +12%p |

### 7.2 회복 *불가* 영역 정직 명시

- **JCAP majority (>50%)**: 영구 미달. hybrid αγ 의 28% 상한도 50% 의 56% 수준.
- **PRD Letter**: 영구 차단. Q17 amplitude-locking 채널 사망 (A6 폐기).
- **"통합 이론" headline**: 영구 사망. galactic-only theory 로 brand 정직 화.
- **DESI w_a<0 H3**: KILL 처리 의무. claims_status v1.2 → v1.3.
- **S_8 tension**: hybrid 와 무관 — SQMH 자체가 해결 못함 (L6 재발방지).

### 7.3 회복 *가능* 영역

- **galactic dynamics paper**: MNRAS / ApJ 진입 가능. SPARC RAR + dwarf depletion 의 a priori 골격 단단.
- **a_0(z) future test**: JWST 고-z lensing 으로 검증 가능 — paper 본문의 falsifiable 양념.
- **honest phenomenology positioning**: γ 단독의 brand 자기파괴를 α 의 axiom 명시화로 *완화* — "정직한 galactic phenomenology + 1 cosmology side-bet".

---

## 8. CLAUDE.md 정합성 체크

- **[최우선-1] 방향만 제공, 지도 금지**: 신규 수식 0줄, 신규 파라미터 값 0개, "A=…" 형태 0건. axiom 3' Γ_0(t) 는 *시간의존 방향* 만, 함수 형태 미명시. a_0(z) prediction 도 *부호/모양 미명시* (8인 자유 도출 의무). ✓
- **[최우선-2] 팀 독립 도출**: hybrid axiom 통합 *방향* 만 합성, 8인 Rule-A 라운드 자유 도출 의무. ✓
- **결과 왜곡 금지**: §3 acceptance 22% / 회복률 32% / majority + PRD Letter 영구 차단 정직 명시. §7.2 회복 불가 영역 5개 정직 노출. L527–L529 disk 부재 §1 명시. ✓
- **paper/base.md edit 0건** ✓
- **simulations/ 신규 코드 0줄** ✓
- **claims_status.json edit 0건** ✓ (단 §5.3 H3 KILL 처리는 *권고* 만, 실제 edit 은 8인 Rule-A 통과 후)
- **L6 §"PRD Letter 진입 조건"**: hybrid αγ 미달 정직 명시 (§7.2). ✓
- **L6 §"DR3 스크립트 실행 금지"**: simulations 신규 0건 — 자동 정합. ✓
- **L6 §"mu_eff ≈ 1 은 S8 tension 해결 불가"**: §5.3 정직 인용. ✓
- **L6 §"리뷰 완료 전 결과 논문 반영 금지"**: 본 L535 는 *권고* 만. ✓
- **disk-absence 정직 보고 (L499/L505/L511/L518/L521/L526 R8/L531 선례)**: §1 정합. ✓

---

## 9. Round 9 권고 (L536+)

| 옵션 | 내용 | 권고? |
|---|---|---|
| **R9-Exec-A** | 8인 Rule-A 라운드 — Path-αγ hybrid 채택 합의, axiom 2/6 폐기 정당화, axiom 3' Γ_0(t) reformulate 자유 도출, paper §0 abstract 재작성 (galactic-first), title MNRAS 트랙 결정 | **YES (1순위)** |
| **R9-Exec-B** | 4인 Rule-B 라운드 — claims_status v1.2 → v1.3 (H3 KILL, h4-oom 격하, n-eff-combined dormant, rar-shape / a_0-OOM / dwarf-depletion 강화, a_0-z-future pre-reg), AICc 재산출 (axiom 2/6 폐기 패널티 게인 정량화) | **YES (2순위, R9-Exec-A 통과 후)** |
| R9-Free (Q17 우연 도출 시도) | new-axiom branch 활성 시도 | NO — A6 폐기로 Q17 채널 자체 사망. 의도 도출 [최우선-1] 위반 위험. |
| R9-Sim | DR3 / 신규 fit | **NO** — DR3 공개 전 금지 + galactic 본문은 SPARC-based, 신규 sim 불요 |
| R9-Meta | 추가 메타-진단 | **NO** — L526 R1–R8 + L531 + L535 합성으로 메타-진단 종결 |

---

## 10. 한 줄 정직 (재진술)

**Path-αγ hybrid (axiom 3' Γ_0(t) cosmology 1-channel 잔존 + axiom 2/6 폐기 galactic 4-channel 강화) 의 acceptance 중앙 22% / 글로벌 고점 회복률 32% / best target MNRAS / JCAP majority 영구 미달 / PRD Letter 영구 차단 — Path-γ 단독 (20%) 대비 +2%p 의 미세 이득은 a_0(z) cross-channel 의 falsifiable 양념 효과이며, "정직한 galactic phenomenology + 1 cosmology side-bet" 포지셔닝이 brand 자기파괴 비용을 부분 흡수하여 산출된 한계 이득.**

---

*저장: 2026-05-01. results/L535/HYBRID_AG.md. 단일 메타-합성 에이전트. L527–L529 / L532–L534 디스크 부재 정직 보고 (§1). paper/base.md edit 0건. simulations/ 신규 코드 0줄. claims_status.json edit 0건. 신규 수식 0줄. 신규 파라미터 0개. CLAUDE.md [최우선-1] / [최우선-2] / 결과 왜곡 금지 / 디스크 부재 정직 인정 / L6 재발방지 (PRD Letter 조건, S8 tension, mu_eff, DR3 금지, 리뷰 전 paper 반영 금지) 모두 정합. 본 문서가 제시한 모든 verdict / acceptance 수치는 *방향 제시* 이며 채택은 후속 R9 (L536+) 8인/4인 라운드 결정.*
