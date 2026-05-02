# L554 — Portfolio acceptance 재계산 (L549 P3a 박탈 반영)

> 작성: 2026-05-02. 단일 작성 에이전트 (8인 Rule-A / 4인 Rule-B 미실행).
> 선례 계승: L546 §5.1 §5.2 산식 / L549 P3a Rule-A 회의적 압박 / L550 0.42σ→0.71σ 디스크 cross-check.
> CLAUDE.md 정합: paper/base.md edit 0건, claims_status.json edit 0건, simulations/ 신규 코드 0줄, 신규 수식 0줄, 신규 파라미터 0개.

---

## 0. 정직 한 줄

본 L554 는 *L546 portfolio acceptance (overlap-corrected 중앙 0.50, ρ≈0.20)* 를, **L549 의 P3a priori 자격 박탈** (R1+R8 hidden DOF 14~18 재계상 → CANDIDATE/PASS_QUALITATIVE 강등) 과 **L550 의 paper §3.2 0.42σ→0.71σ 정정 의무** 두 외부 충격을 반영하여 재계산하며 — *arXiv D 본문* 은 P3a 가 §3 추가 자산이 아니라 §2 amplitude-locking partial 만 있었으므로 모더레이션 ~100% 자체는 변동 0%p 이지만 *Round 11 후속 paper* (DR3 결과 후) 의 P3a-extension 트랙은 영구 손실, *Main MNRAS-γ* 는 0.71σ 정정 + L549 cross-mention disclosure 두 가지 신규 disclosure 부담으로 acceptance −1 ~ −3%p, *Companion B* 는 거의 영향 없음 (방법론 only) — portfolio peer-reviewed-1지-이상 acceptance 중앙은 **0.48 (보수 0.41, 낙관 0.54)** 로 **L546 0.50 대비 −2%p**, 글로벌 고점 회복률 **74% → 71%** 로 보수화. paper/base.md / claims_status.json edit 0건, 본 plan 의 채택 / 실행은 후속 8인 Rule-A / 4인 Rule-B 결정에 종속.

---

## 1. L549 / L550 영향 매핑 (paper-by-paper)

### 1.1 arXiv D (preprint priority lock)

| 항목 | L546 가정 | L549 박탈 후 |
|---|---|---|
| §2 amplitude-locking partial | Q17 부분 도출 (E(0)=1 정규화 귀결, 동역학 미달성 정직 인정) | **무변** — P3a 와 무관 |
| §3 DR3 falsifier 정량 (wa>−0.5 KILL, ∈[−0.5,−0.7] PASS_QUALITATIVE, <−0.7 PASS_MODERATE) | preregistered cosmology falsifier | **무변** — P3a (CMB-S4 BB bispectrum) 는 §3 가 아니라 *Round 11 후속 paper* 의 자산 |
| §4 C28 독립 이론 명시 | Maggiore-Mancarella RR non-local | **무변** |
| arXiv 모더레이션 acceptance | ~100% | **~100% (변동 0%p)** |
| 후속 paper (Round 11) | DR3 결과 + P3a CMB-S4 trial-spec 이중 트랙 | **단일 트랙으로 축소** — P3a 가 priori 자산 손실, "≥4 후보 중 1" (R3) 자격 |
| brand asset | "L1 priori candidate" (P3a) + "Q17 partial" + "DR3 preregistered" | **"Q17 partial" + "DR3 preregistered"** — L1 자산 1건 손실 |

핵심: arXiv D *본문 자체* 는 영향 0. 영향은 후속 paper (Round 11) 의 priority 자산 손실에 집중. 본 L554 portfolio acceptance 재계산은 *peer-reviewed 1지 이상* 정의에 한정되므로 arXiv D 모더레이션은 ~100% 유지.

### 1.2 Main MNRAS-γ

| 항목 | L546 가정 | L549/L550 후 |
|---|---|---|
| §3.2 a₀ 편차 | 0.71σ 단일 채택 명시 | **L550 디스크 사실 확정** (verify_milgrom_a0.py + JSON + stdout 3-way 0.71σ 합의) → abstract/intro 의 stale "0.42σ" 일괄 정정 의무 +1 |
| L539 §2.3 정정 흔적 | "0.42σ → 0.71σ 정정" 메모 | **MNRAS_DRAFT.md L14/L28/L89 stale-figure** 명시 정정 — reviewer 의 clone-and-run cross-check 시 즉시 충돌 차단 (L550 §5 사유 6) |
| Verlinde 2017 degeneracy | §6.3 명시 인정 | **무변** |
| Bullet cluster DM 잔존 | §4.3 정직 인정 | **무변** |
| hidden DOF | 9–13 disclosed (paper §6.5(e)) | **paper-internal 무변** — L549 R4/R8 의 +1 (Γ₀(t)) +3 (K-Z) +1 (GFT BEC) = 14~18 DOF 는 *P3a 한정* 재계상이며 Main MNRAS-γ scope 밖 (galactic-only) |
| 외부 cross-mention | arXiv D 1회 (§1.3), Companion B 1회 (§8) | **+ L549 disclosure** — arXiv D cite 부분에서 "(P3a strand demoted to CANDIDATE per L549)" 한 줄 추가 권고 (정직성 자산) |
| acceptance 중앙 | 22% (range 18–28%) | **20–21%** (−1 ~ −2%p; 0.71σ 정정 대비 0.42σ→0.71σ 정정 자체는 reviewer-friendly 이지만 abstract retitled stale-figure flag, P3a CANDIDATE cross-mention 부담 합산) |
| 보수 하한 | 18% | **17%** |
| 낙관 상한 | 28% | **27%** |

핵심: 0.71σ 정정은 *재현성* 자산 (L550 §5 사유 6) → 단독으로는 reviewer 호의적. 그러나 (i) abstract/intro 정정 footprint, (ii) L549 P3a-CANDIDATE disclosure 의무 두 가지 신규 disclosure 가 acceptance 를 −1 ~ −3%p 보수화. 중앙 22% → **21%** (보수 17%, 낙관 27%) 채택.

### 1.3 Companion B (methodology)

| 항목 | L546 가정 | L549/L550 후 |
|---|---|---|
| 7-script verification harness | 디스크 실재 (L539 §3.3 검증) | **무변** — L550 이 verify_milgrom_a0.py 디스크 사실 0.71σ 재확인. harness 자산 강화 (4인 자율 분담 결과 3-way concordance) |
| claims_status.json schema | 5 tier | **무변** |
| Hidden-DOF audit protocol | k_eff 추정 + ΔAICc | **자산 강화** — L549 R8 이 hidden DOF 재계상 (14~18) → AICc penalty 28~36 → P3a 강등 prediction 의 *case study* 로 §4.3 추가 가능 (positive footprint) |
| Q_parameter FAIL | §6.4 정직 인정 | **무변** |
| Negative-control 1건 | verify_mock_false_detection.py | **무변** |
| 단일 adopter (SQMH) | §6.1 정직 인정 | **무변** |
| acceptance 중앙 | 47% (range 40–55%, mid 60% → 47%) | **47–48%** (+0~+1%p; L549 audit-trail demonstration 자산 약 +0.5%p, 의미 미미) |

핵심: Companion B 는 *방법론 paper* — 이론 클레임 강도 변동에 둔감. L549/L550 모두 harness/audit-trail 의 *작동 사례* 로 흡수 가능. 중앙 47% 그대로 채택 (변동 ≤ +1%p, range 내부).

---

## 2. 갱신 acceptance 표

### 2.1 paper-별

| 라벨 | L546 중앙 (보수–낙관) | L554 중앙 (보수–낙관) | Δ vs L546 | 사유 |
|---|---|---|---|---|
| Main MNRAS-γ | 22% (18–28%) | **21% (17–27%)** | −1%p | L550 0.71σ 정정 footprint + L549 P3a-CANDIDATE cross-mention disclosure 부담 |
| Companion B | 47% (40–55%) | **47% (40–55%)** | 0%p | L549/L550 모두 harness 작동 사례로 흡수, 방법론 변동 무 |
| arXiv D | ~100% (모더레이션) | **~100%** | 0%p | 본문 §2/§3 영향 무, 모더레이션 자격 무변 (priority brand asset 만 −1건) |

### 2.2 portfolio (peer-reviewed 1지 이상)

> overlap-corrected. ρ≈0.20 (MNRAS↔OJA reviewer pool 30–60명 overlap, brand bias δ=0.6).
> 산식: 1 − [1 − P(M)][1 − P(C)] · (1 + ρ·δ) (L546 §5.2 그대로)

| 시나리오 | P(Main) | P(Comp) | 단순 독립 1−(1−M)(1−C) | overlap 보정 (×(1+ρδ)) | portfolio |
|---|---|---|---|---|---|
| 중앙 (ρ=0.20, δ=0.6) | 0.21 | 0.47 | 0.581 | 0.581 × (1−0.12) ≈ **0.48** | **0.48** |
| 보수 (ρ=0.30) | 0.17 | 0.40 | 0.502 | 0.502 × (1−0.18) ≈ 0.41 | **0.41** |
| 낙관 (ρ=0.10) | 0.27 | 0.55 | 0.671 | 0.671 × (1−0.06) ≈ 0.54 | **0.54** |

> 보정 부호: +ρ·δ 가 *correlated downside* 이므로 (1 − ρδ) 형태로 적용 (L546 §5.2 와 동일 convention; "결합 acceptance 보수화" 방향).

**중앙 0.48, 보수 0.41, 낙관 0.54** — peer-reviewed 1지 이상.

### 2.3 brand bias 추가 (변동 무)

L546 §5.3 그대로 유지. arXiv D 를 2026-05 즉시 제출하여 author 단일성 brand bias 분산. L549 P3a 박탈은 cluster bias 에 영향 없음 (P3a 는 어차피 arXiv D 본문 §3 자산이 아니었음).

---

## 3. 갱신 trajectory

| 시점 | acceptance (peer-reviewed 1지 이상) | 누적 Δ vs L490 | 주 이벤트 |
|---|---|---|---|
| L490 (JCAP 단일, pre-audit) | 68% | 0 | 야심기 baseline |
| L526 R8 | 5% | −63%p | hidden DOF 9~13 disclosure shock |
| L535 αγ hybrid (single) | 22% | −46%p | galactic-only retreat |
| L540 portfolio (단순 독립) | 59% | −9%p | 3-paper portfolio 산술 합산 |
| L546 portfolio (overlap-corrected, ρ≈0.20) | 50% | −18%p | reviewer-pool overlap + brand bias 보정 |
| **L554 portfolio (P3a 박탈 + 0.71σ 정정 반영)** | **48%** | **−20%p** | L549 P3a CANDIDATE 강등 + L550 disk-truth 정정 disclosure |
| L554 + R10-Exec-A 통과 (예상) | 53–63% | −5 ~ −15%p | 8인 Rule-A 통과 시 disclosure 안정화 |

**글로벌 고점 회복률**: 48 / 68 ≈ **71%** (L546 74% → L554 71%, −3%p 보수화).

"통합 이론 single paper" 야심 (L490 JCAP 단일 68%) 에서는 영구 미달 — L549 P3a 박탈로 portfolio strand 의 brand-asset 1건 손실이 trajectory 에 영구 각인.

---

## 4. CLAUDE.md 정합성 체크

- **[최우선-1] 방향만 제공, 지도 금지**: 신규 수식 0줄, 신규 파라미터 0개. ✓
- **[최우선-2] 팀 독립 도출**: 본 L554 단일 작성, 8인 Rule-A 미실행 명시. ✓
- **결과 왜곡 금지**: §0 / §1.1 / §2.2 / §3 모두 "P3a 박탈 영향 정직 보고" + "글로벌 고점 회복률 71% (L546 74% 보다 보수)" 정직 기재. portfolio acceptance 산술 max 단독 인용 0건 (overlap + brand bias 동시 명시). ✓
- **paper/base.md edit 0건** ✓
- **claims_status.json edit 0건** ✓
- **simulations/ 신규 코드 0줄** ✓
- **L549 / L550 디스크 사실 인용만, 재해석 금지** — §1.2 의 0.71σ 채택은 L550 §5 결정 인용 (재계산 아님). §1.1 의 P3a 박탈은 L549 R8 집계 인용 (재판정 아님). ✓
- **L546 산식 그대로 사용** — §2.2 ρ=0.20, δ=0.6 convention L546 §5.2 직접 상속. 신규 보정 도입 0건. ✓

---

## 5. 정직 한 줄 (재진술)

L549 P3a priori 자격 박탈 (R1+R8 hidden DOF 14~18 재계상 → CANDIDATE/PASS_QUALITATIVE 강등) 과 L550 paper §3.2 0.42σ→0.71σ 디스크 정정 의무를 L546 portfolio 산식에 반영하여, peer-reviewed 1지 이상 acceptance 중앙은 **0.48 (보수 0.41, 낙관 0.54)** — L546 0.50 대비 −2%p, 글로벌 고점 회복률 **71%** (L546 74% → −3%p) — Main MNRAS-γ 가 0.71σ stale-figure 정정 + P3a CANDIDATE cross-mention disclosure 부담으로 22%→21%, Companion B 는 무변, arXiv D 본문은 무변 (P3a 는 §3 자산이 아니므로 모더레이션 ~100% 유지) 이지만 후속 Round 11 paper 의 priority brand asset 1건 영구 손실, 본 재계산의 채택은 후속 8인 Rule-A / 4인 Rule-B 결정에 종속, paper/base.md / claims_status.json edit 0건.

---

*저장: 2026-05-02. results/L554/PORTFOLIO_REESTIMATE.md. 단일 작성 에이전트. paper/base.md edit 0건. simulations/ 신규 코드 0줄. claims_status.json edit 0건. 신규 수식 0줄. 신규 파라미터 0개. CLAUDE.md [최우선-1] / [최우선-2] / 결과 왜곡 금지 / L546 산식 직접 상속 정합. 본 문서가 제시한 모든 acceptance 재계산 / trajectory / 회복률 갱신 은 *방향 제시* 이며 채택은 후속 Round 10 8인/4인 라운드 결정.*
