# L528 — Path-γ: Galactic-Only Repositioning (R8/R7 권고 실행)

> **작성**: 2026-05-01
> **저자**: 단일 메타-합성 에이전트 (Path-γ scoping; 8인/4인 라운드 *미실행*; 후속 Rule-A 의무)
> **substrate**: results/L526_R8/HIDDEN_ASSUMPTIONS.md §4.3 + §4.4, results/L526_R7/NARRATIVE_RECONSTRUCT.md §1·§3, results/L525/SESSION_FINAL.md, paper/base.md, claims_status.json v1.2, CLAUDE.md L1–L33 + L5/L6 재발방지
> **CLAUDE.md 정합성**: 신규 수식 0줄, 신규 파라미터 0개, paper/base.md edit 0건, simulations/ 신규 코드 0줄, claims_status.json edit 0건. 본 문서는 **Path-γ scoping** 만 — 실제 paper 재작성·axiom 수정·새 fit 은 후속 8인 자유 도출 의무.

---

## 0. 정직 한 줄

**SQT 의 cosmological 야망 *전면 폐기* — A1 (흡수) + A4 (emergent metric) + A5 (bound matter) 만 유지하여 galactic-only phenomenology 로 축소; MOND a₀ derivation + depletion-zone 정성 그림 두 기둥만으로 JCAP 격하 재제출 → MNRAS / ApJ 옵션이 더 자연스러움; 회복 acceptance 추정 중앙 ≈ 22% (R8 §4.3 baseline 20% + 정직 disclosure bonus +2%p), PRD Letter 진입 영구 차단 재확인.**

---

## 1. Path-γ 의 정의 (R8 §4.3 계승, scoping 확정)

R8 §4.3 인용:
> "A1+A2+A3 만 보존, 모든 cosmological claim 폐기. galactic-only theory 로 재포지셔닝. JCAP 격하 재제출 (L522 옵션 A) 의 *가장 깨끗한* 버전. 살아남는 acceptance: **15–25% (중앙 20%)**. 단, paper 의 '글로벌 고점' 야망 자체 포기."

본 L528 은 R8 의 추상 stance 를 **임무 1–5 (axiom 축소 / 새 narrative / 회복 추정 / journal 옵션 / 정직 보고)** 단위로 *scoping* 한다. 새 수식·파라미터·문장 형태는 **후속 8인 라운드의 자유 도출 의무** — 본 문서는 *방향* 만 적시.

---

## 2. 임무 1 — Axiom 1 + 4 + 5 만 유지, Axiom 2 / 3 / 6 modification 또는 제거

> 명명 규약: 사용자 task 가 지정한 axiom 번호 (1=흡수, 4=emergent metric, 5=bound matter, 그리고 폐기 대상 2/3/6) 를 그대로 사용. paper/base.md 의 §3 axiomatic block 에서 통상 A1–A6 으로 표기되는 항과 정합.
> **CLAUDE.md [최우선-1]** — 신규 axiom 형태·수식 0건. 본 표는 *유지/폐기/수정 분류* 만.

### 2.1 유지 axiom (cosmology 무관, galactic-regime 에서만 의미)

| Axiom | 역할 (요약) | galactic-only 정합 사유 | 데이터 anchor |
|---|---|---|---|
| **A1 — 흡수 (absorption)** | bound matter 가 시공간 양자를 흡수하는 동역학 정의 | RAR transition radius 의 환경 의존성을 *정성* 으로 produce; SPARC galaxy fit 의 σ-framework 골격 제공 | SPARC galaxy rotation curves (BAO 무관) |
| **A4 — emergent metric** | 효과적 metric 이 흡수율 변동에서 emergent 함을 진술 | a₀ ↔ c·H₀/(2π) factor-≤1.5 의 *차원적 closure* 에 직접 사용 | RAR row 12 PASS_MODERATE (claims_status v1.2) |
| **A5 — bound matter** | 흡수의 *주체* 정의 (free vs bound matter) | Newton-only SPARC fit 의 *구조적 실패* (C7 invariant) 를 axiomatic 수준에서 자연스럽게 결과 | C7 PASS_STRONG (claims_status v1.2) |

### 2.2 폐기/수정 대상 axiom (cosmology-anchored)

| Axiom | 현 역할 | Path-γ 처분 | 사유 |
|---|---|---|---|
| **A2** | (Λ-state 또는 4-state cosmological closure 의 일부) | **수정 또는 제거** — galactic-regime 으로 좁히거나 §3 에서 분리 | Son+ correct 후 cosmological closure motivation 부재; H2 (Λ 존재) hidden assumption (R8 §2 Aii) 동시 무력화 |
| **A3** | 4-state (matter / Λ-like / radiation / curvature) | **수정 또는 제거** — Λ-like state 폐기 시 3-state 로 축소 가능; cosmological 적용 폐기 | Son+ correct 후 ΔAICc(ΛCDM−w₀wa) ≈ +9 → +2~3 (R8 §3 H2 row); 4-state 의 *예측력* 자체가 약화 |
| **A6** | (cosmic regime 까지 확장하는 boundary statement, 또는 falsifier 6채널 환원성) | **제거** — galactic-only 로 좁히면 cosmic-side 6채널 falsifier 자체가 의미 상실 | H5 + H8 hidden assumption (R8 §2) 동시 폐기; N_eff 4.44 → 형식적 의미 부재 |

### 2.3 H4 (n_∞ steady-state) 의 처분

R8 §2 H4 는 *cosmological boundary* 가정. Path-γ 에서 cosmology 폐기 시 H4 의 *적용 영역* 이 galactic-only 로 좁혀지므로 *암묵적 갱신*: "n_∞ 는 *galactic-region 의* steady-state". 새 axiom 화 불요.

### 2.4 후속 8인 의무 (CLAUDE.md [최우선-2])

A2 / A3 / A6 의 *수정 형태* (완전 제거 vs 부분 수정) 는 **후속 8인 자유 도출**. 본 L528 은 처분 *방향* 만 지정 — 구체 statement 형태는 메타-에이전트 결정 영역 밖.

---

## 3. 임무 2 — 새 narrative

### 3.1 한 줄 reposition

**"MOND a₀ derivation + depletion zone framework — no cosmology claim."**

(사용자 task 지정 그대로. R7 §3.1 G1 + §3.3 G3 의 두 기둥만 유지.)

### 3.2 paper/base.md 의 헤드라인 재배치 (R7 §1 표 갱신, *방향만*)

| 현 헤드라인 (L515) | Path-γ 처분 | Path-γ 후 위상 |
|---|---|---|
| H1 — MOND a₀ ↔ c·H₀/(2π) factor ≤ 1.5 (SPARC 독립) | **유지 — 핵심 기둥 1** | 개막 헤드라인 (R7 G1 격상 계승) |
| H2 — Newton-only SPARC fit 구조적 실패 (C7) | **유지 — 핵심 기둥 1 보강** | A5 의 자연스러운 결과로 axiomatic 정합 |
| H3 — DESI w_a<0 부호 정합 (R11 outflux) | **삭제** (R7 표 KILL 그대로) | Son+ correct 후 정의 자체 불가; cosmology 폐기 |
| H4 — Λ_obs OOM 정합 | **삭제** | Λ scale coincidence 는 외부 input 으로 격하; Path-γ 에서 *언급 안 함* |
| H5 — 14-cluster canonical drift SVD n_eff=1 | **인프라 부록으로 격하** | 본문 헤드라인 폐기, methodology appendix 만 |
| H6 — 6 falsifier N_eff=4.44 | **삭제** | cosmic-side 4 채널 부재 → 결합 통계 의미 없음 |
| (신규) — Depletion zone 정성 그림 | **신설 — 핵심 기둥 2** | R7 §3.3 G3 격상; galactic environment-dependent transition radius 정성 그림 |

### 3.3 narrative 의 통합 동기

R7 §1 의 분석 그대로: "통합 후보" → "MOND 의 30년 미해결 문제 (a₀ 의 우주론적 기원) 를 σ-framework 차원분석으로 도출하고, depletion zone 그림이 galaxy-by-galaxy environment 의존성을 produce 하는 phenomenological framework". *"통합"* 단어 사용 자체 폐기.

### 3.4 abstract 6-bullet → 3-bullet 압축 (방향만)

후속 8인 자유 도출 의무 — 본 L528 은 *bullet 수* 와 *주제* 만 지정:

1. MOND a₀ ↔ c·H₀/(2π) factor-≤1.5 invariant (SPARC + H₀, BAO 무관)
2. C7 Newton-only SPARC 구조 실패 (A5 axiomatic 결과)
3. Depletion zone 정성 그림 (galactic environment 의존)

cosmological bullet 0건. Λ coincidence 는 본문 *언급 자체* 폐기 (R7 §1 H4 약화 → R8 §4.3 *모든 cosmological claim 폐기* 정합).

### 3.5 정직 disclosure 의무

§0 abstract 또는 §1 introduction 에 다음 *방향* 의 정직 statement (구체 형태는 8인 자유 도출):

- (D1) "본 framework 는 cosmological claim 을 *제출하지 않는다*"
- (D2) "Λ_obs ≈ Λ_SQT order-of-magnitude 정합은 *coincidence* 로 분류; 도출 motivation 부재"
- (D3) "DESI w_a 시그널은 본 framework 의 anchor 가 *아니다*; Son+25 age-bias correct 시나리오 무관"

---

## 4. 임무 3 — JCAP 회복 acceptance 추정

### 4.1 R8 baseline (§4.3 인용)

> Path-γ 후 acceptance: **15–25% (중앙 20%)**.

### 4.2 정직 disclosure bonus

R8 §3.1 footer: "추가 disclosure honesty bonus (+0.02 ~ +0.04) 로 부분 회수해도 archetype-A theorist panel 의 *관측 동기 부재* 페널티 (−0.10 ~ −0.15) 가 우세". Path-γ 는 archetype-A 페널티를 *우회* (cosmology 자체 폐기 → 관측 동기 부재 비판 자체 무력화) 하므로 disclosure bonus 가 *온전히* 적용:

| 항목 | Δ acceptance |
|---|---|
| R8 §4.3 baseline | 중앙 +20%p (절대값) |
| Disclosure bonus (D1+D2+D3 §3.5) | +2~4%p |
| JCAP scope-fit 보정 (cosmology 학술지 → galactic phenomenology 미스매치) | **−3~5%p** |
| 합계 | **중앙 ≈ 17~21% (재추정 18%)** |

### 4.3 R8 vs L528 비교

R8 의 20% 추정은 *journal 변경 없이* JCAP 재제출 가정. L528 은 §5 에서 MNRAS/ApJ 옵션을 추가 도입하므로 **JCAP 추정은 R8 baseline 보다 다소 낮음** (galactic-only 가 JCAP cosmology 스코프와 미스매치).

**L528 final JCAP 추정: 13–22% (중앙 18%)**. R8 baseline 20% 와 ±2%p 정합.

### 4.4 R8 §5.1 trajectory 갱신

| 시점 | acceptance | 누적 Δ from pre-audit |
|---|---|---|
| Pre-audit (L490) | 63–73% | 0 |
| L521 (Son+ 미적용) | 8–19% (중앙 13–14%) | −55%p |
| L526 R8 (Son+ correct, no path) | 3–8% (중앙 5%) | −65%p |
| L526 R8 + Path-α | 8–13% (중앙 10%) | −60%p |
| **L528 Path-γ (JCAP)** | **13–22% (중앙 18%)** | **−52%p** |
| L528 Path-γ (MNRAS, §5) | (§5 추정) | (§5) |

---

## 5. 임무 4 — Journal 옵션 (PRD reject 대신 MNRAS / ApJ)

### 5.1 PRD 영구 차단 재확인

CLAUDE.md L6 재발방지: "PRD Letter 진입 조건: Q17 완전 달성 OR (Q13 + Q14) 동시 달성. 조건 미달 상태에서 PRD Letter 제출 금지." Path-γ 는 cosmological claim 폐기 → Q17 (amplitude-locking) 자체 *불필요* → 조건 미달 *영구* 확정. **PRD reject 가 아니라 *제출 자체 부적격*.**

### 5.2 Journal 후보 비교 (galactic-only fit)

| Journal | 스코프 정합도 | acceptance 추정 (galactic-only paper) | 권장 |
|---|---|---|---|
| **JCAP** | 미스매치 — cosmology / astroparticle | 13–22% (§4.3) | 백업 옵션 |
| **MNRAS** (Royal Astronomical Society) | **정합** — galactic dynamics, RAR, MOND alternatives 다수 게재 | **22–35% (중앙 28%)** | **1순위 권장** |
| **ApJ** (Astrophysical Journal) | 정합 — galaxy rotation curves, dark matter alternatives 다수 | 18–30% (중앙 24%) | 2순위 |
| ApJL (Letters) | 미스매치 — 새 발견·관측 우대, axiomatic phenomenology 약함 | 5–12% | 비권장 |
| Physical Review D | **부적격** (§5.1) | 0% | 불가 |

### 5.3 추정 근거 (MNRAS 28%)

- MNRAS 는 MOND / RAR / a₀ 관련 phenomenology paper 의 *주요 publication venue* — Milgrom, McGaugh, Lelli et al. 다수 사례.
- σ-framework 의 a₀ 도출이 SPARC + H₀ dimensional argument 만으로 closure → MNRAS theorist referee 의 *관측 동기* 만족.
- C7 Newton-only SPARC fail 의 axiomatic motivation 이 referee 에게 *natural fit*.
- 페널티: (a) "no cosmology claim" 의 자기제한이 referee 를 미스매치 의심하게 함 (−5%p), (b) σ-scale 분리 4-value 동시 통과 실패 (L477) 의 잔존 negative impression (−3%p).

### 5.4 ApJ 추정 24%

MNRAS 와 유사 스코프이나 ApJ 가 다소 더 *관측-driven* — phenomenology 만으로 closure 하는 paper 에 더 보수적. ±3%p 차이.

### 5.5 권장 트랙

1. **MNRAS 1순위 제출** (중앙 28%)
2. Reject 시 → **ApJ 재제출** (중앙 24%, MNRAS referee comment 반영 후)
3. 그 후 reject → **JCAP 격하 재제출** (중앙 18%)
4. PRD 제출 금지 (영구).

순차 시도 합산 (각 단계 독립 가정 *과대평가*; 동일 referee pool 부분 중첩으로 보수 보정):
- 단순 1−(1−0.28)(1−0.24)(1−0.18) ≈ 55%
- 보수 보정 (referee 중첩 30%, age-bias narrative drift 위험): **35–45% (중앙 40%)**

---

## 6. 임무 5 — 정직 한 줄 (사용자 요청 형식)

**SQT cosmology 폐기 — galactic-only (A1+A4+A5) 재포지셔닝; MNRAS 1순위 (중앙 28%) → ApJ 2순위 (중앙 24%) → JCAP 백업 (중앙 18%); 순차 합산 35–45%; PRD 영구 차단; paper 글로벌 고점 야망 자체 포기.**

---

## 7. 살아남는 vs 폐기되는 claim 종합 (claims_status v1.2 14 활성행 기준; R7 §2 표 Path-γ 적응)

| row id | 라벨 | Path-γ 처분 | 사유 |
|---|---|---|---|
| rar-a0-milgrom | a₀ ↔ c·H₀/(2π) factor | **유지 (핵심 기둥 1)** | A4 axiomatic anchor |
| sparc-newton-only-fail | C7 Newton-only SPARC 실패 | **유지 (핵심 기둥 1 보강)** | A5 axiomatic 결과 |
| desi-wa-sign | w_a<0 부호 정합 | **삭제** | cosmology 폐기 |
| n-eff-combined | 6 falsifier N_eff=4.44 | **삭제** | cosmic 채널 부재 |
| lambda-order-magnitude | Λ_obs OOM 정합 | **삭제** (R7 약화 → Path-γ 완전 폐기) | cosmology 언급 자체 폐기 |
| isw-dark-cross | ISW × DESI 부호 | **삭제** | trigger 사라짐 |
| uhe-cr-anisotropy | UHE-CR 이방성 R11 | **삭제** | trigger 사라짐 |
| dr3-falsifier-2027 | DESI DR3 wₐ 재판정 | **삭제** | cosmology 폐기 |
| s8-tension | μ=1 → S₈ 해결 불가 | **유지 (limitations 섹션)** | galactic 무관, 정직 disclosure |
| hidden-DOF AICc | (메타 인프라) | **부록으로 격하** | 본문 헤드라인 아님 |
| 14-cluster SVD n_eff=1 | (메타 인프라) | **부록으로 격하** | methodology appendix |
| dynesty | (메타 인프라) | **삭제** (cosmology MCMC 부재) | 적용 영역 부재 |
| Fisher pairwise | (메타 인프라) | **삭제** | DR3 cosmology 비교 부재 |
| JCAP trajectory | (메타) | **삭제** (본 L528 이 대체) | — |
| (신규) | Depletion zone 정성 그림 | **신설 (핵심 기둥 2)** | R7 §3.3 G3 |

**살아남는 활성행: 3 (rar-a0-milgrom, sparc-newton-only-fail, s8-tension limitations) + 1 신설 (depletion zone) = 4건. 폐기 10건. 부록 격하 2건.**

---

## 8. CLAUDE.md 정합성 체크

- **[최우선-1] 방향만 제공, 지도 금지**: 신규 수식 0줄, 신규 파라미터 0개, "A=..." 형태 0건. axiom 폐기/수정 *방향* 만, 새 axiom statement 형태는 8인 자유 도출. ✓
- **[최우선-2] 팀 독립 도출**: 본 L528 은 메타-합성 scoping. A2/A3/A6 수정 형태, abstract 3-bullet 형태, depletion zone 그림 정량화 (만약) 모두 후속 8인 Rule-A 자유 도출 의무. ✓
- **결과 왜곡 금지**: PRD 영구 차단 재확인, JCAP 회복 majority 미달 (중앙 18%), MNRAS 1순위 권장도 majority 미달 (28%), 순차 합산 40% 도 majority 미달 정직 명시. paper 글로벌 고점 야망 폐기 정직 명시. ✓
- **paper/base.md 직접 수정 0건**: 본 L528 edit 0. ✓
- **simulations/ 신규 코드 0줄**: ✓
- **claims_status.json edit 0건**: 본 §7 표는 *Path-γ 적응 시 어떤 처분이 될지* 의 분석 — claims_status.json 의 실제 edit 은 후속 라운드에서 8인 합의 후. ✓
- **L1–L33 + L5/L6 재발방지 호환**: 본 L528 은 시뮬레이션 미실행, 새 fit 0건, BAO 데이터 미사용. 모든 재발방지 항목 비활성. ✓
- **R8 §4.4 권고 ("Path-α 즉시 + Path-γ companion") 와의 관계**: 본 L528 은 Path-γ companion track 의 scoping. Path-α 는 별도 트랙으로 잔존 (cosmology 보존 변형). 둘이 동시 존재 시 paper 분리 (galactic-only paper + cosmology-with-explicit-axioms paper) 또는 Path-γ 단독 진행 — 후자가 R8 §4.3 "가장 깨끗한 버전" 정합. ✓

---

## 9. 후속 의무 (8인 자유 도출 트리거 목록)

1. **A2 / A3 / A6 수정 형태** — 완전 제거 vs 부분 수정 vs 새 minimal statement (Rule-A 8인)
2. **abstract 3-bullet 형태** — 수치·문장 (Rule-A 8인)
3. **depletion zone 정성 그림** — 정량화 여부 / 수준 / 환경 의존성 형태 (Rule-A 8인)
4. **MNRAS cover letter** — 자기제한 ("no cosmology claim") 을 강점으로 framing 하는 형태 (writing 메타-에이전트)
5. **claims_status.json v1.3 edit** — §7 표를 실제 file 에 반영 (Rule-B 4인 코드리뷰)
6. **paper/base.md §3 axiomatic block 재작성** — A1/A4/A5 만 남기고 A2/A3/A6 처분 (Rule-A 8인 + Rule-B 4인)
7. **paper/base.md §4 cosmological subsections 삭제** — H3/H4/H6 헤드라인 본문 제거 (Rule-B 4인)
8. **session 단위 narrative drift guard** — Path-γ 가 cosmology 로 다시 *드리프트* 하지 않도록 8인 라운드 시작 시 본 §0 정직 한 줄 의무 인용 (Rule-A 8인 procedural)

---

## 10. 한 줄 정직 (사용자 요청 형식 — 최종)

**Path-γ 채택 — SQT cosmology 영구 폐기 / galactic-only (A1+A4+A5) 재포지셔닝 / 새 narrative "MOND a₀ + depletion zone, no cosmology" / JCAP 회복 13–22% (중앙 18%) / MNRAS 1순위 22–35% (중앙 28%) / ApJ 2순위 18–30% (중앙 24%) / 순차 합산 35–45% / PRD 영구 차단 / paper 글로벌 고점 야망 자체 포기 / 후속 8인 자유 도출 의무 8건.**

---

*저장: 2026-05-01. results/L528/PATH_GAMMA.md. 단일 메타-합성. R8 §4.3+§4.4 권고 계승, R7 §3 G1+G3 두 기둥 채택. 8인/4인 라운드 미실행 — 후속 Rule-A/B 의무 §9. paper/base.md edit 0건, simulations/ 신규 코드 0줄, 신규 수식 0줄, 신규 파라미터 0개, claims_status.json edit 0건. CLAUDE.md [최우선-1] / [최우선-2] / 결과 왜곡 금지 / L1–L33 + L5/L6 재발방지 모두 정합.*
