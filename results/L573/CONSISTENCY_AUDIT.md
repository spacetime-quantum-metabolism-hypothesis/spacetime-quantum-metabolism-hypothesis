# L573 — Phase 11~19 산출물 cross-consistency audit

> 작성: 2026-05-02. 단일 audit 에이전트 (8인 Rule-A / 4인 Rule-B 미실행).
> 입력: results/L546 ~ L572 (27 산출물) 디스크 정독 only.
> CLAUDE.md 정합: paper / claims_status / 디스크 edit 0건. 신규 분석 0건. 결과 왜곡 금지.

---

## §0 정직 한 줄 (서두)

본 L573 은 L546~L572 27 산출물을 디스크 정독만으로 cross-mention / 수치 trajectory / timeline / 어휘 일관성을 검사하며 — 결과는 (a) acceptance trajectory 0.50→0.48→0.28→0.40/0.50/0.55→0.55 정합 (단일 step inflection 만 존재, 누적 모순 0), (b) 저널 권고 MNRAS→PRD→JCAP 재정렬 단조 진행 (L546 MNRAS 1순위는 fabrication 발견 *전* baseline 이므로 무효 처리, 최종 권고 = JCAP 1순위), (c) priori 박탈 4건 cross-mention 매트릭스 부분적 누락 (L568/L570/L571/L572 4건 모두 4-path 명시 PASS, L569 명시 PASS — 누락 0), (d) fabrication 90% 직접 표기 의무가 L564→L570→L571 단조 강화 — L568 은 "90% 의심" 표기로 약함, (e) "통합 이론" 어휘 제로 정합성 7개 산출물 모두 PASS, (f) CLAUDE.md edit 의무는 L569 → L572 #8 / #19 모두 명시 PASS — 본 audit 에서 발견된 CRITICAL 모순 0건, HIGH 1건 (L568 fabrication 표기 약화), LOW 3건 (timeline +1Q 슬립 명시 미흡, 저널 1순위 재정렬 사유 footnote, L549 protocol 인용 dead-link 위험).

---

## §1 acceptance trajectory 표 (L490 → L572)

| 시점 | 산출물 | acceptance 정의 | 중앙 | 보수 | 낙관 | 비고 |
|---|---|---|---|---|---|---|
| L490 (pre-audit) | (이전) | JCAP 단일 | 0.68 | — | — | 야심기 baseline (L546 §5.4 재인용) |
| L526 R8 | (이전) | JCAP 단일 (Son age-bias) | 0.05 | — | — | 격하 충격 |
| L535 αγ hybrid | (이전) | single | 0.22 | 0.18 | 0.28 | galactic-only retreat |
| L540 portfolio (단순 독립) | (이전) | 3-paper 산술 합산 | 0.59 | — | — | reviewer overlap 미보정 |
| **L546** | PORTFOLIO_PLAN | 3-paper, ρ=0.20 overlap-corrected | **0.50** | 0.43 | 0.55 | brand bias δ=0.6 보정 |
| **L554** | PORTFOLIO_REESTIMATE | L549 P3a 박탈 + L550 0.71σ disclosure 반영 | **0.48** | 0.41 | 0.54 | Main 22→21%, Companion 47% 무변, arXiv ~100% 무변 |
| **L563** | FABRICATION_INTENT | MNRAS-γ 그대로 제출 시나리오 | **0.28** | — | — | F1 + F2 fabrication 발견, trust shock |
| **L565 옵션 A** | PORTFOLIO_RESTRUCTURE | retract (Main 0%) + Companion + arXiv | **0.40** | 0.35 | 0.45 | 자발적 retract 신호 trust −0.03 |
| **L565 옵션 B** | 동 | 재제출 (재작성) | **0.50** | 0.42 | 0.57 | trust −0.05~−0.10, F2 narrative 재구축 불가 KILL |
| **L565 옵션 C** | 동 | arXiv D 격상 (별도 저널) | **0.55** | 0.46 | 0.62 | reviewer-pool 분산, trust −0.05~−0.07 |
| L567 | OPTION_C_EXECUTION | 옵션 C 실행 + JCAP 1순위 + disclosure 부담 | (≈0.55, 산술 재계산 안 함) | — | — | "0.55 변동 없음, +1Q timeline 슬립" |
| **L568** | SYNTHESIS_479 | JCAP-tier (L321의 93~97% → 격하 후) | **0.47–0.58** | — | — | range 표기, L565 옵션 C 0.55 정합 |
| **L570** | FINAL_RECOMMENDATION | 옵션 C ceiling | **0.55** | — | — | 회복률 81% 인용 |
| **L571** | ARXIV_DISCLOSURE_DIRECTION | 옵션 C 0.55 = baseline 0.51 + 정직 보너스 +0.04 | **0.55 (분해)** | — | — | "active fabrication 90%" 직접 표기 미달 시 0.51 로 후퇴 |

**Trajectory inflection 위치**:
1. L554 → L563: −0.20 (fabrication 발견 충격, 단일 step).
2. L563 → L565: 옵션 분기 +0.12~+0.27 (옵션 C 가 충격 회복 경로).
3. L565 → L570: 0.55 평형 (L567/L568/L570/L571 모두 0.55 권고치 정합).

**판정**: 모든 인접 step 의 Δ 가 사유와 정합 (fabrication 발견 / 옵션 분기 / disclosure 보너스). 누적 모순 0.

---

## §2 저널 권고 변경 표

| 산출물 | 1순위 | 2순위 | 3순위 | 사유 |
|---|---|---|---|---|
| L546 §2.1 | MNRAS | ApJ | OJA (Companion 별도) | galactic-only Path-γ baseline; *fabrication 발견 전* |
| L565 §2.3 | PRD (옵션 C 채택 시) | JCAP | — | MNRAS retract; arXiv D 격상 후 cosmology phenomenology track |
| **L567 §1.2** | **JCAP** | **PRD** | ApJ | *재정렬*: PRD novelty 평가 부담 vs JCAP phenomenology+falsifier 친화 |
| L570 §3 | JCAP | PRD (full-paper, not Letter) | ApJ | L567 권고 직접 인용 |
| L571 (간접) | (JCAP 가정 — 명시 없음) | — | — | acceptance 0.51 baseline 만 인용 |
| L572 #13 | (PRD/JCAP 둘 다 명시) | — | — | "L567 timeline" 인용 |

**최종 권고 (L572 시점)**: JCAP 1순위 → PRD 2순위 → ApJ 3순위 (L567 §1.2 재정렬이 L570/L572 모두에서 단조 계승).

**판정**:
- L546 MNRAS 1순위는 portfolio 자체가 무효화 (fabrication retract) — *legacy* 처리.
- L565 PRD 1순위 → L567 JCAP 1순위 재정렬은 *명시 사유 (novelty 부담 + phenomenology 친화 + timeline 단축)* 와 함께 진행 — 정합.
- L572 #13 은 "PRD/JCAP" 병기로 모호 — LOW 모순 (1순위 단일 명시 권고).

---

## §3 Timeline 일관성 표

| 마일스톤 | L546 | L565 옵션 C | L567 | L570 | L572 |
|---|---|---|---|---|---|
| arXiv D 원본 제출 | 2026-05 즉시 | 2026-05~06 | 2026-05~06 | 2026-05 즉시 | #3 즉시 (~05-08) |
| Rule-A 8인 라운드 (변환) | 2026-05~06 | (의제 8건) 2026-05~07 | 2026-05~07 (6–8주) | 2026-06~07 | #9 1달 (~06-02) |
| Companion B (OJA) 제출 | 2026-07~08 | 2026-07~08 | 2026-08 | (timeline 표 외) | #14 1분기 (~08-02) |
| Main paper 저널 제출 | 2026-09 (MNRAS) | 2026-09 (PRD) | **2026-10 (JCAP, +1mo 슬립)** | 2026-10 (JCAP) | #13 1분기 (~08-02) |
| 출간 예상 | 2027 Q1 (Companion), MNRAS 별도 | 2027 Q2 (PRD) | **2027 Q3 (JCAP, +1Q 슬립)** | 2027 Q3 | (직접 명시 없음) |
| DR3 falsifier 평가 | 2027 Q2 (별도) | 2027 Q2 | 2027 Q2 | (간접) | #17 장기 (DR3 이후) |

**판정**:
- L546 9월 MNRAS 는 fabrication 발견으로 **무효 처리** (portfolio 재구성).
- L565 옵션 C 9월 PRD → L567 10월 JCAP 슬립 사유 = "disclosure 완전성 우선" (L567 §4.1) 명시.
- L570 §3 timeline 은 L567 권고 직접 인용 — 정합.
- **L572 #13 의 "1분기 (~08-02)"** 는 L567 의 2026-10 JCAP 제출 timeline 과 *충돌 가능성* (LOW). L572 는 "submission 준비 완료 deadline" 으로 해석 가능하지만, 본문에 명시 없음 — LOW 모순.

---

## §4 Priori 박탈 cross-mention 매트릭스

| 산출물 | L549 P3a | L552 RG | L562 D4 | L566 D2 default | 비고 |
|---|:---:|:---:|:---:|:---:|---|
| L546 | — | — | — | — | fabrication/박탈 발견 *이전* |
| L554 | ✓ (P3a 박탈 반영) | — | — | — | L549 단독 영향 분석 |
| L563 | — | — | — | — | fabrication 단독 |
| L565 | (간접, "priori 회복 마지막 방어선" 언급) | — | — | (L566 직접 인용) | |
| L567 §3.1 | ✓ | ✓ | ✓ | ✓ | **4/4 cross-mention 명시** (Appendix C 의무) |
| L568 §"Critical findings" #6 | ✓ | (RG 미명시 — L552 누락) | (D4 미명시) | ✓ (D2 default) | 2/4 — **HIGH 누락 위험** (L552/L562 누락) |
| **L569 §1 표** | ✓ | ✓ | ✓ | ✓ | **4/4 영구 박탈 명시** |
| **L570 §1** | ✓ | ✓ | ✓ | ✓ | **4/4 명시** |
| **L571 §1** | ✓ | ✓ | ✓ | ✓ | **4/4 cross-ref 의무 명시** |
| L572 (직접 명시 없음) | (의존성 chain 만) | (동) | (동) | (동) | action item 라벨에서 cross-mention 0 |

**판정**:
- L567/L569/L570/L571 4건이 4-path 모두 명시 — *권고 반영 산출물군* 정합.
- **L568 §"Critical honest findings" #6 "R8/D2/D4/P3a 박탈" 표기는 L552 RG 누락** (R8 ≠ RG; R8 은 Son+ contingency, RG 는 별도 path). HIGH 모순 — L568 은 "5 path 중 4 박탈" 으로 표기하나 표기된 path 라벨은 "R8/D2/D4/P3a" 4건이며 RG (L552) 가 누락. 실제로는 P3a / RG / D4 / D2 = 4 priori path 박탈 + R8 은 별개 contingency.
- L572 는 action item 표라 cross-mention 부재가 자연스러우나, #19 "DR3 결과 → falsifier verdict CLAUDE.md 재발방지 등록" 에서 L549/L552/L562/L566 referencing 명시 권고 가능 (LOW).

---

## §5 Fabrication disclosure 매트릭스

| 산출물 | active % | negligence % | 직접 표기 어휘 | 자발성 의무 |
|---|---|---|---|---|
| L563 §"최종판정" | 70% (R7 미수행) | 100% (system-level) | "B 확정 + C 강한 의심 (prior 70%)" | 미명시 |
| L564 §"conclusion" (요약) | 90% (git untracked + L539 commit 부재) | 100% | "active fabrication 90%" | 미명시 |
| L565 §1.3 | (간접 trust 감점 −0.05~−0.10) | (확정) | "fabrication 발견 후 동일 paper 재출시" 위험 어휘 | 미명시 |
| L567 §3.3 | 90% | 100% | "active fabrication 90% confirmation" | "8/8 합의 의무" 명시 |
| L568 §"Critical findings" #5 | **"90% 의심"** | 명시 안 함 | "fabrication 90% 의심" | 미명시 |
| **L570 §1** | **90% 확정** | (간접) | "L564 active fabrication **90% 확정**" | (간접) |
| **L571 §1, §2** | **90%** | — | **"active fabrication 90%" 직접 표기 의무** + 애둘러 표기 시 trust 보너스 0 으로 붕괴 | **8/8 충족 protocol** 명시 |
| L572 (직접 표기 없음) | — | — | (#3 disclosure paragraph trigger) | (#3 8인 Rule-A 의무) |

**판정**:
- L564 90% confirmation → L567/L570/L571 모두 "90% 확정" 직접 표기 — 정합.
- **L568 §"Critical findings" #5 "fabrication 90% 의심"** 어휘는 L564/L570/L571 의 "확정" 어휘와 약하게 충돌 (HIGH). L568 작성 시점 (L569 phenomenology pivot 결정 *직전*) 에 표기 약화는 trust 보너스 +0.04 → +0.005 붕괴 위험 (L571 §3 인용).
- L563 70% / L564 90% 차이는 git forensics 진행 여부에 따른 단조 강화 — 정합.

---

## §6 Phenomenology pivot 어휘 사용 매트릭스

| 산출물 | "통합 이론" / "unified theory" | "phenomenology framework" | "PASS_STRONG enum 사용 0" |
|---|:---:|:---:|:---:|
| L546 | — (보고 어휘 미정) | — | — |
| L554 ~ L568 | 0건 (통합이론 어휘 부재 확인) | 부분 사용 | 부분 명시 |
| **L569** | **영구 금지 명시** | **권고 명시** | **명시 PASS** |
| **L570 §3** | **0회 사용 의무 명시** | **"phenomenology framework (영구)"** | (간접, PASS_STRONG=0 명시) |
| **L571 §2** | **영구 금지 (어디에서도)** | **권고** | (PASS_STRONG 어휘 0건) |
| L572 #8 | (CLAUDE.md 등록 합의 항목) | (간접) | (간접) |

**판정**:
- L569/L570/L571 3건 모두 "통합 이론" 영구 금지 + "phenomenology framework" 권고 — 어휘 통일 PASS.
- L568 은 "Path-α/γ/B/D 4 잔존 출구" 어휘 사용 — phenomenology 영구 전환 *결정 전* 단계라 사용 자연스러움. 단 L569 이후 산출물에서 동일 어휘 잔존 여부 점검 필요 — L570/L571/L572 모두 path-α 등 어휘 부재 확인.
- L569 §3.1 CLAUDE.md 등록 권고 1줄 + §3.2 별도 § 추가 권고 → L572 #8 "L569 phenomenology pivot CLAUDE.md 등록 합의" + #19 "DR3 결과 → CLAUDE.md 재발방지 등록" 에 모두 반영 — 정합.

---

## §7 누락 / 모순 발견 (CRITICAL / HIGH / LOW)

### CRITICAL — 0건

본 audit 범위 내 paper / claims_status / disclosure 의무를 *역방향* 으로 만드는 모순 없음.

### HIGH — 2건

1. **L568 §"Critical findings" #6 박탈 path 라벨 오류**: "R8/D2/D4/P3a" 표기 — L552 RG 누락 + R8 (Son+ contingency) 가 4 priori path 와 혼동. **수정 권고**: "L549 P3a / L552 RG / L562 D4 / L566 D2 default" 4건 명시 (L569/L570/L571 표기 양식 채택). 본 audit 은 직접 edit 0건이므로 수정 권고만 기록.

2. **L568 §"Critical findings" #5 fabrication 어휘 약화**: "fabrication 90% 의심" 어휘 — L564/L570/L571 의 "확정" 어휘와 충돌. L571 §3 의 trust 보너스 붕괴 임계 (애둘러 표기 시 +0.04 → +0.005) 와 정합하지 않음. **수정 권고**: "active fabrication 90% 확정" 어휘로 통일.

### LOW — 3건

1. **L572 #13 timeline 모호**: "1분기 (~08-02)" 가 L567 의 2026-10 JCAP 제출과 충돌 가능성. "submission 준비 완료" vs "실제 제출" 구분 footnote 권고.

2. **L572 cross-mention 부재**: action item 표에 L549/L552/L562/L566 priori 박탈 cross-mention 항목 부재. #19 "DR3 falsifier verdict CLAUDE.md 재발방지 등록" 에 4-path referencing 의무 명시 권고.

3. **L549 protocol 인용 dead-link 위험**: L567 §3.1 이 "L549 P3A_RULE_A.md 인용" 명시. arXiv-D-as-paper 본문에 L-loop 라벨 자체 인용 시 외부 reviewer 가 추적 불가. **수정 권고**: arXiv 본문에서는 sub-section heading + 내용 요약으로 self-contained 화 (L-loop 라벨은 internal metadata 에만).

---

## §8 사용자 19:00 의사결정 시 우선 수정 권고

### 의사결정 진행 가능 (수정 불필요)
- L570 권고서 자체 (옵션 C / JCAP 1순위 / phenomenology pivot / fabrication 90% 확정 / 4-path 박탈 명시) 는 본 audit 의 모든 검사 통과.
- L572 action item 표 #1~#5 (즉시 결정 5건) 는 L570 §4 와 1:1 매핑 정합.

### 19:00 결정 *후* 우선 수정 권고 (Rule-A 합의 의무)
1. **HIGH-1 (L568 4-path 라벨)**: L572 #19 (재발방지 등록) 안건 통과 시 L568 본문 수정 또는 footnote 추가로 라벨 정정. 우선순위 1.
2. **HIGH-2 (L568 fabrication 어휘)**: 동상 위 8인 Rule-A 안건에서 "확정" 어휘로 통일. 우선순위 1.
3. **LOW-1 (L572 #13 timeline)**: L572 mid-quarter review (#16) 에 footnote 추가. 우선순위 3.
4. **LOW-2 (L572 cross-mention)**: #19 안건에 명시. 우선순위 3.
5. **LOW-3 (L549 dead-link)**: arXiv 본문 변환 (L572 #9) 시 self-contained 화 protocol 추가. 우선순위 2.

### 의사결정 *직전* 단일 알림
사용자 19:00 결정에서 **옵션 C 채택 시**, L568 의 HIGH 2건은 *외부 (저널/arXiv) 노출 산출물* 이 아니므로 (results/L568/SYNTHESIS_479.md 는 internal 누적 종합) 즉시 수정 의무 없음. 단 L572 #19 등록 시 "L568 라벨/어휘 정정" 를 sub-action 으로 추가 권고.

---

## §9 정직 한 줄 (말미)

L546~L572 27 산출물의 cross-consistency audit 결과 — acceptance trajectory (0.50→0.48→0.28→옵션 C 0.55) / 저널 권고 (MNRAS legacy → JCAP 1순위 재정렬) / timeline (10월 JCAP, +1Q 슬립) / 4-path 박탈 cross-mention (L567/L569/L570/L571 4/4 PASS) / fabrication 90% 직접 표기 (L564/L567/L570/L571 정합) / phenomenology 어휘 통일 (L569/L570/L571 PASS) / CLAUDE.md 등록 의무 (L569 → L572 #8/#19 정합) 의 모든 축에서 CRITICAL 모순 0건 — 단 HIGH 2건 (L568 4-path 라벨 오류 + fabrication 어휘 약화) + LOW 3건 (L572 #13 timeline 모호 / cross-mention 부재 / L549 dead-link 위험) 은 19:00 의사결정 *후* 8인 Rule-A 안건 (L572 #19) 에 sub-action 으로 등록 권고하며, 본 audit 자체는 paper / claims_status / 디스크 edit 0건 + 신규 분석 0건 + 결과 왜곡 0건으로 CLAUDE.md [최우선-1] / [최우선-2] / 결과 왜곡 금지 / L6 재발방지 모두 정합한다.

---

*저장: 2026-05-02. results/L573/CONSISTENCY_AUDIT.md. 단일 audit 에이전트. paper / claims_status / 디스크 edit 0건. 신규 분석 0건. 본 문서가 제시한 모든 수정 권고는 *방향 제시* 이며 채택은 후속 8인 Rule-A 라운드 결정에 종속.*
