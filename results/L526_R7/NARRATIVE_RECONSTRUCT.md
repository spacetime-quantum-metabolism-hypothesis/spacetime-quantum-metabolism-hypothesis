# L526 R7 — SQMH paper narrative *fundamental reconstruction* under Son+ correct

> 작성: 2026-05-01. 단일 philosophy/writing 메타-에이전트.
> 모드: 8인/4인 라운드 *미실행*. Command [최우선-1] 준수 — 본 문서는 *방향만* 제시하며 새로운 수식·파라미터 값을 제안하지 않는다. 인용된 수식·값은 모두 기존 paper/base.md, claims_status.json v1.2, L477/L488/L515/L521/L525 에 *이미 존재*하는 것을 그대로 가져온 것. 새 fit 결과 0 건. paper/base.md edit 0 건.
> 정직 한 줄: **Son+ 가 옳다면 SQMH paper 의 "암흑에너지 기원" 헤드라인은 사망하고, 살아남는 것은 (a) MOND a₀ ↔ c·H₀/(2π), (b) σ-framework 의 비-fit 골격, (c) depletion zone 정성 그림 셋 뿐 — Λ_obs ≈ Λ_SQMH 는 *order-of-magnitude coincidence* 로 격하되며, paper 는 "통합 후보" 가 아니라 "MOND 와 Λ scale 의 우연일치를 한 평면에서 설명하는 phenomenological framework" 로 재포지셔닝된다.**

---

## 0. 기점 — "Son+ correct" 의 정의와 영향 범위

본 R7 task 가 가정하는 시나리오:

1. Son+25 (Ryu, Son et al. 2025, arXiv ref. paper/base.md 인용) 의 *BAO age-bias 정정* 이 **독립 분석에서 재현·통과**.
2. 정정 후 DESI DR2 의 `(w₀, wₐ) ≠ (-1, 0)` 신호가 **Δχ² ≲ 4** 수준으로 약화 (= LCDM 와 통계적 구분 불능).
3. 즉 *DR2 단계* 에서 "DESI dynamical dark energy" 모티브 **부재**.

이 가정 하에 SQMH paper 의 어느 클레임이 *생존* 하고 어느 클레임이 *사망* 하는지를 **paper/base.md 와 claims_status.json v1.2 의 14 개 활성 클레임 행 단위**로 재 mapping.

영향 범위는 *데이터-의존* 클레임에 한정. 데이터-비의존 (a priori 도출 / 차원분석 / 기하) 클레임은 영향 없음.

---

## 1. 현 paper narrative — 한 페이지 압축

`paper/base.md` 헤드라인 구조 (L515 §0 abstract 6-bullet 기준):

| # | 헤드라인 한 줄 | 데이터 의존성 | Son+ 영향 |
|---|---|---|---|
| H1 | MOND a₀ ↔ c·H₀/(2π) (factor ≤ 1.5) — RAR row 12 PASS_MODERATE | SPARC + H₀ | **무영향** (SPARC 은 BAO 와 독립) |
| H2 | Newton-only SPARC fit *구조적 실패* — C7 invariant | SPARC | **무영향** |
| H3 | DESI w_a<0 → ψ-flux outflux 부호 매칭 (R11 branch) | **DESI BAO** | **사망** (Son+ 정정 시 wₐ≈0) |
| H4 | Λ_obs ≈ ρ_Planck/(σ·t_macro²) order-of-magnitude 정합 | (σ 는 a priori, Λ_obs 는 CMB+BAO 결합) | **약화** — Λ_obs 추정에 BAO 가 들어감 |
| H5 | 14-cluster canonical drift = SVD n_eff=1 (검증 인프라) | 데이터 비의존 | **무영향** |
| H6 | 6 falsifier 결합 N_eff=4.44 / 8.87σ (ρ-corrected) | DESI BAO 채널 1 개 포함 | **약화** — N_eff=3.x 로 강등 추정 |

**현 narrative 의 *유일성 motivation* (= "왜 SQMH 인가") 는 H3 (DESI 부호 일치) 가 핵심 기둥**. H3 가 빠지면 다른 5 헤드라인은 살아남지만 *통합 동기* 가 약해진다 — H1+H2 는 MOND 재구성, H4 는 Λ coincidence, H5 는 인프라, H6 는 결합 통계인데, H3 없이는 "왜 dark sector 도 같이 봐야 하는가" 의 직접 증거가 사라진다.

---

## 2. 데이터-의존 클레임 영향 행렬 (claims_status.json v1.2 14 활성행 기준)

| row id | 라벨 (요약) | 현 등급 (v1.2) | Son+ correct 후 등급 | 사유 |
|---|---|---|---|---|
| rar-a0-milgrom | a₀ ↔ c·H₀/(2π) factor | PASS_MODERATE | **PASS_MODERATE 유지** | SPARC 독립 |
| sparc-newton-only-fail | C7 Newton-only SPARC 구조 실패 | PASS_STRONG | **PASS_STRONG 유지** | SPARC 독립 |
| desi-wa-sign | w_a<0 부호 정합 (R11 outflux) | PARTIAL | **KILL** | wₐ≈0 시 부호 자체 정의 불가 |
| n-eff-combined | 6 falsifier N_eff=4.44 (8.87σ) | PARTIAL | **PARTIAL → 강등 candidate** | 1/6 채널 사망, 재계산 필요 |
| lambda-order-magnitude | Λ_obs OOM 정합 | PARTIAL | **PARTIAL 유지 (격하 문구 추가)** | OOM 자체는 살아남음 |
| isw-dark-cross | ISW × DESI cross 부호 예측 | pre-reg | **dormant** (R11 사망 시 트리거 없음) | trigger 사라짐 |
| uhe-cr-anisotropy | UHE-CR 이방성 R11 채널 | pre-reg | **dormant** | trigger 사라짐 |
| dr3-falsifier-2027 | DESI DR3 (2027) wₐ 재판정 | pre-reg | **이미 정답: wₐ≈0 예측** | Son+ 가 옳다면 DR3 도 같은 방향 |
| s8-tension | μ=1 구조 → S₈ 해결 불가 | (limitations) | **무영향** | SQMH 자체 한계 |
| (외 5 행: hidden-DOF AICc, 14-cluster SVD, dynesty, Fisher pairwise, JCAP trajectory) | 인프라/메타 | 모두 **무영향** | 데이터 비의존 |

**사망 1 (desi-wa-sign), 강등 후보 2 (n-eff, lambda-OOM 문구), dormant 2 (ISW/UHE-CR), 무영향 9. 활성행 14 중 5 행 영향 (35.7%).**

---

## 3. *살아남는* SQT 의 이유 — 4 골격

Son+ correct 후에도 SQT 가 paper 로서 *논문화 가치를 유지하는 이유* 4 가지:

### 3.1 G1 — MOND a₀ derivation (생존, 핵심 기둥 으로 격상)

- claims_status row `rar-a0-milgrom`: a₀ ↔ c·H₀/(2π) factor ≤ 1.5.
- SPARC + H₀ 만 사용. BAO 무관.
- L477 / L515 / L521 모두 이 행을 "최후 invariant" 로 식별.
- Son+ correct 후 paper 의 *개막 헤드라인* 이 H3 → G1 로 교체된다.
- **이유**: MOND 의 30 년 미해결 문제 (a₀ 의 우주론적 기원) 를 SQMH 의 σ-framework 가 *차원분석 1 줄* 로 도출. 이것 자체로 phenomenological 가치 유지.

### 3.2 G2 — σ-framework 의 a priori 골격 (생존, 단 "fit-dependent" 응용은 사망)

- σ_macro / σ_micro ≈ 2.6×10⁶⁰ 의 두 스케일 분리는 차원분석에 의해 결정 (L48 ~ L56 골격).
- 단일 σ 로 4-value (H_0, σ_8, a_0, BAO wₐ) 동시 통과는 이미 *L477 에서 사망 선언* — 본 시나리오와 무관하게 끝난 문제.
- Son+ correct 후 σ-framework 는 "두 스케일 분리는 차원적 필연이며, 그 중 하나가 a₀ 와 일치한다" 는 *최소 골격* 으로 환원.
- 정직 표기 필요: 4-value 동시 통과가 framework 의 목적이 아님을 명시. paper §6.5(e) 의 PARTIAL 라벨 그대로 유지.

### 3.3 G3 — Depletion zone 정성 그림 (생존, 정량 fit 분리 명시)

- Depletion zone (paper §IX 부근) 은 *정성 시공간 양자 그림*. RAR transition radius 의 환경 의존성을 자연스럽게 produce.
- BAO 와 무관. SPARC 의 *외부 영역* 데이터 (R > 3 r_d) 와 정합.
- Son+ correct 후 영향 0. 다만 paper narrative 에서 "depletion zone 이 dark sector 동역학을 함의" 라는 H3 연결 줄은 *제거*.

### 3.4 G4 — Λ_obs ≈ ρ_Planck/(σ·t_macro²) — *order-of-magnitude only* 로 명시 격하

- 현재 paper §IV/§VI 표현: "Λ scale 이 SQMH 자연 계산값과 정합" (정합 정도는 OOM 수준).
- Son+ correct 후 Λ_obs 추정 자체가 LCDM 으로 회귀 (BAO 정정으로 Ω_Λ 추정 정밀도 변화 없음 — Λ 값은 BAO 보다 CMB 가 dominant). 즉 Λ_obs 자체는 큰 변화 없음.
- 그러나 SQMH 가 *dark energy 동역학* 을 추가로 설명한다는 클레임이 사라지므로, Λ scale 정합은 "*동역학 없는* OOM coincidence" 로 *재 명시*.
- 살아남는 표현: "SQMH 의 σ 골격이 Λ 의 작음 (vacuum catastrophe 122 dex) 과 a₀ 의 작음을 *동일한 두 스케일 비* 로 부분 설명한다." — 이것은 OOM 일치 **2 채널**.
- 사망 표현: "SQMH 가 Λ 의 *시간 의존 구조* 를 예측" — Son+ correct 시 시간 의존 신호 부재.

---

## 4. *사망* 하는 클레임 — 정직 청산 목록

### 4.1 H3 = DESI w_a<0 부호 정합 (직접 사망)

- claims_status row `desi-wa-sign`: PARTIAL → **KILL**.
- paper §05 desi_prediction 섹션 *전면 재작성* 또는 *축약*.
- L488 §5 의 "Son+25 wₐ≈-1.9 와의 정량 비교" 트리거는 dormant.

### 4.2 R11 (Boundary A3 cosmological flux) 의 BAO 채널 (사망)

- L477 에서 R11 의 강점은 "*세 채널* (BAO + ISW + UHE-CR) 동시 부호 예측" 이었다.
- BAO 채널 사망 시 ISW / UHE-CR 채널은 *trigger amplitude* 가 사라져 사실상 자유 파라미터 1 개 추가 model 로 격하.
- R11 가 H1 (R3⊗R7) 과 같이 paper appendix §10 에 "탐색된 후보" 로 남되, 본문 헤드라인에서 *제거*.

### 4.3 6 falsifier 결합 N_eff=4.44 의 BAO 항 (재계산 필요)

- 6 falsifier (a_0, MOND, dwarf, BAO, RAR, σ_v) 중 BAO 항 1 개 사망.
- 결합 N_eff 단순 재계산 시 √(5/6)·4.44 ≈ 4.05 (ρ-corrected 가 아니라 naive 추정. 정밀 재계산은 4 인 코드리뷰 라운드 작업 — 본 R7 은 *방향만*).
- Σ 표기: paper §4.9 의 "8.87σ" 는 *재 fit 후 강등* — 추정 7-8σ 영역. 단 본 R7 은 새 fit 0 건이므로 정확값 미제시.

### 4.4 paper 헤드라인에서 *암흑에너지 기원* 표제어 *제거*

- 현 abstract 6-bullet 의 dark-energy 관련 줄 (≥1 줄, L515 §0) → *삭제 또는 격하 문구*.
- "암흑에너지 origin proposal" → "Λ scale OOM coincidence (no dynamical claim)".
- 이 변경은 8 인 라운드 *필수* — 단일 메타 에이전트 권한 밖.

---

## 5. 새 paper title / abstract 제안 (3 안)

> **주의**: 본 절은 *제안* 이며 채택은 8 인 합의 (Rule-A) 필요. 본 R7 단독 권한으로 paper/base.md 에 반영 *금지*.

### 안 A — 보수적 재포지셔닝 (가장 정직, JCAP 친화)

**Title**: *"A two-scale spacetime-quantum framework: deriving the MOND acceleration scale from the Hubble rate"*

**Abstract** (5 줄 골격):

1. We propose a phenomenological framework (SQMH) in which spacetime quanta carry two characteristic scales, τ_micro (Planck-related) and τ_macro (Hubble-related).
2. Dimensional analysis fixes their ratio at ≈ 2.6×10⁶⁰, which we identify with two known coincidences: the MOND acceleration scale a₀ ↔ c·H₀/(2π) (factor ≤ 1.5; SPARC) and the smallness of Λ.
3. The framework reproduces the observed RAR for SPARC galaxies without dark matter halo profile freedom (row rar-a0-milgrom: PASS_MODERATE; Newton-only fits structurally fail).
4. We do *not* claim a dynamical dark-energy mechanism; the Λ-scale match is reported as an order-of-magnitude coincidence pending full Boltzmann-level analysis.
5. We register pre-falsifiers for SPARC outliers (DR3 SKA), MOND-cluster regime (Bullet), and a₀-shift cosmologies; no BAO-based dynamical claim is asserted.

**평가**: Son+ correct 시나리오와 100% 정합. headline 위험 0. 단 "통합 이론" 야망 포기. JCAP 채택 확률 추정 30–45% (L521 ~ L525 trajectory 의 중앙값).

### 안 B — 절충 재포지셔닝 (R11 outflux 를 *조건부* 부록으로)

**Title**: *"Two-scale spacetime quanta: MOND acceleration from the Hubble rate, with a conditional dark-sector flux extension"*

**Abstract**: 안 A 의 1–4 + 5 줄째 변형 — "We further outline a boundary-flux extension (R11) that becomes empirically relevant only if BAO age-bias corrections (Son+25) are *not* confirmed by DR3; the present paper takes no position on this branch."

**평가**: paper/base.md 의 dark-sector 관련 자산을 부록으로 보존. 단 "조건부 부록" 은 referee 입장에서 hedge 로 읽힐 위험 — 도리어 야망 줄이는 안 A 가 더 정직.

### 안 C — 최소 변경 (현 paper 골격 유지, §0 abstract 만 patch)

**Title**: 기존 유지 — *"Spacetime Quantum Metabolism Hypothesis ..."* (paper/base.md 현재 제목).

**Abstract**: 현 6-bullet 중 dark-energy 관련 1–2 줄을 *조건부 격하* 표현으로 교체 ("if Son+25 confirmed, the Λ-scale match reduces to an order-of-magnitude coincidence"). H1 (a₀), H2 (SPARC fail), H4 (OOM), H5 (인프라), H6 (강등된 N_eff) 는 유지.

**평가**: 변경 최소 — 단일 메타 에이전트 권한 *경계* 에 가장 가까운 안. 단 paper title 자체가 "metabolism" 을 강조하는데 dark-sector dynamics 부재 시 brand 와 내용 mismatch. 장기적으로 안 A 권장.

### 추천 — 안 A

근거 3:

1. **정직성** — Son+ correct 시나리오에서 paper 의 야망 축소를 사용자에게 *과대 광고 없이* 전달.
2. **JCAP fit** — L521 8 인 합의 "정직한 falsifiable phenomenology" 포지셔닝과 정확히 일치 (L6 재발방지 §"JCAP 타깃 조건").
3. **재발방지 정합** — L6 §"S₈ tension 해결 불가" / "mu_eff ≈ 1" 함정과 같은 부류의 *honest downgrade*. 8 인 라운드에서 통과 가능성 가장 높음.

---

## 6. paper/base.md 에 들어갈 *대기* 변경 (지금은 0 건, 8 인 라운드 후 발효)

> Command [최우선-1] 및 L6 재발방지 "리뷰 완료 전 결과 논문 반영 금지" 적용. 본 R7 작성 시점 paper/base.md edit *0 건*.

8 인 라운드 (Rule-A) 통과 시 시행할 *대기 변경* 목록:

| paper 섹션 | 대기 변경 | 종속성 |
|---|---|---|
| §0 abstract (L515) | 6-bullet 중 dark-energy 줄 → "OOM coincidence (no dynamical claim)" 격하 | 안 A 채택 |
| §1 introduction | "통합" 표현 → "MOND a₀ + Λ-scale 두 OOM coincidence 의 공통 골격" 으로 교체 | 안 A 채택 |
| §05 desi_prediction | 본문 → §10 appendix 로 이동, 헤더에 "DR2 + Son+25 정정 후 conditional" 명시 | desi-wa-sign KILL 확정 |
| §4.9 (line 618 N_eff) | 8.87σ → 7-8σ 범위 (재 fit 필요) | 4 인 코드리뷰 (Rule-B) 라운드 |
| §6.5(e) AICc-honest 0% | *유지* (Son+ correct 와 무관) | — |
| §10 appendix_alt20 | R11 (BAO + ISW + UHE-CR) → "dormant unless Son+25 reverted" 라벨 | desi-wa-sign KILL |
| arxiv_submission_checklist | "DESI BAO falsifier" 항목 → "Son+25 cross-check" 로 표제 변경 | 안 A 채택 |
| claims_status.json | desi-wa-sign: PARTIAL → KILL ; isw-dark-cross / uhe-cr-anisotropy : pre-reg → dormant ; n-eff-combined: 재 fit 결과 반영 ; lambda-order-magnitude: PARTIAL 유지 + 문구 격하 | 4 인 라운드 결과 |

**총 7 섹션 + claims_status.json 5 행 — 8 인 / 4 인 분담 분명. 단일 메타 에이전트 시행 *불가*.**

---

## 7. 8 인 라운드 권고 (Rule-A) — 본 R7 의 *전달 책임*

본 R7 은 narrative 재구성 *지도* 만 제공. 실제 변경은 다음 라운드에서:

- **Rule-A 8 인 (이론·해석)**: 안 A vs B vs C 선택; G1–G4 생존 골격 4 개 합의; Λ OOM 격하 문구 합의; H3 사망 선언; abstract 재작성.
- **Rule-B 4 인 (코드·통계)**: N_eff 재 fit (BAO 채널 제거); claims_status.json v1.2 → v1.3 sync; 6 falsifier 그래프 재생성; ρ-corrected 결합 σ 재산출.

**라운드 순서**: A → B (이론 합의 후 코드 반영). 동시 진행 금지 — L6 §"코드 리뷰 완료 전 결과 논문 반영 금지" 정합.

---

## 8. *정직 한 줄* — Command 산출 요구

> **Son+ correct 시 SQMH paper 는 "암흑에너지 통합 이론" 의 야망을 포기하고 "MOND a₀ + Λ scale 의 두 order-of-magnitude coincidence 를 두-스케일 σ 골격으로 동시에 phenomenological 하게 설명하는 framework" 로 축소된다 — 살아남는 골격 4 개 (G1 a₀, G2 σ-framework 골조, G3 depletion zone 정성, G4 Λ OOM), 사망 클레임 1 개 (H3 BAO wₐ<0), 영향 활성행 5/14 (35.7%); 권장 재포지셔닝은 안 A (보수적, JCAP 친화); 본 R7 단독 paper 변경 0 건, 8 인 + 4 인 라운드 *후* 발효.**

---

*저장: 2026-05-01. results/L526_R7/NARRATIVE_RECONSTRUCT.md. 단일 philosophy/writing 메타-에이전트. paper/base.md edit 0 건. claims_status.json edit 0 건. simulations/ 신규 코드 0 줄. CLAUDE.md [최우선-1]/[최우선-2]/L6 §"리뷰 완료 전 결과 논문 반영 금지" 모두 정합. 본 문서가 제시한 모든 클레임은 *방향 제시* 이며 채택은 후속 8 인/4 인 라운드 결정.*
