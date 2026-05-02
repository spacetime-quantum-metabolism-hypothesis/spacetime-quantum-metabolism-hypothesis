# L656 — arXiv Preprint Draft §3 / §4 Sync Plan

**목적**: L646 에서 작성한 §3 4-pillar covariance (4 paragraph) + §4 layered axioms (3 paragraph) 본문 예시를 `paper/arXiv_PREPRINT_DRAFT.md` 에 어떻게 통합할지에 대한 *plan-only* 산출물. 본 문서는 plan 단계이며 arXiv draft / paper plan v3 / claims_status / 그 외 디스크 파일 어떤 것도 직접 edit 하지 않는다.

**원칙 (CLAUDE.md 최우선-1 준수)**: 수식 0줄, 파라미터 값 0개, 신규 prediction 0건, 신규 후보 0건. arXiv draft 본문 갱신 (실제 edit) 은 본 plan 통과 + 8인 Rule-A 리뷰 통과 이후 *submission 단계* 에서만 진행.

**금지 어휘** (L591/L596/L635/L640/L654 sync): "통합 이론", "0 free parameter", "priori 도출", L654 무효화 7건 어휘.
**권장 어휘**: "PASS_MODERATE", "covariance" (4-pillar cross-validation 의미; GR-style "general covariance" 와 혼동 금지를 §3 도입부에 한 번 명시).

---

## §1 arXiv draft 현재 §3 / §4 상태 (snapshot)

`paper/arXiv_PREPRINT_DRAFT.md` 의 현재 큰 섹션 구조:

- §1 Introduction (1.1 scope / 1.2 headline / 1.3 relation to MOND-MOG-TeVeS-Verlinde)
- §2 SQT framework — minimal axioms (A0~A6 중 a₀ 도출에 필요한 A1/A2/A4/A5 만 import)
- §3 Derivation of a₀ = c·H₀/(2π) (A4 + A5 sketch + verification script 포인터)
- §4 Evidence at PASS_MODERATE — four channels (4.1 RAR / 4.2 BBN ΔN_eff / 4.3 Cassini / 4.4 EP |η|)
- §5 Falsifiers (pre-registered)
- §6 Hidden DOF disclosure
- §7 Discussion / limitations / conclusions

**관찰**:
1. 현재 draft 의 §3 은 *a₀ derivation* 한 가지 만 다룸. paper plan v3 (L634) 의 "§3 4-pillar covariance" 와 의미가 완전히 다름.
2. 현재 draft 의 §4 는 *4-channel evidence* 표만 다룸. plan v3 의 "§4 layered axioms (core / derived / hidden)" 와 의미가 완전히 다름.
3. 현재 draft §6 (Hidden DOF disclosure) 가 plan v3 의 §4.3 에 해당. 즉 hidden DOF disclosure 자체는 draft 에 이미 있으며 *위치* 만 §6 → §4.3 으로 이동 필요.
4. 현재 draft §2 의 A1/A2/A4/A5 라벨은 plan v3 의 layered (core a1-a3 / derived B1, a4, a6) 라벨과 *충돌* 한다 (대문자 A vs 소문자 a, 번호 의미 다름).

---

## §2 L646 본문 예시 적용 위치 plan

### §2.1 §3 4-pillar covariance (L646 §3.1~§3.4 4 paragraph) 삽입 위치

권고: 현재 draft §3 (Derivation of a₀) 을 **§3 → §5** 로 재배치하고, 새로운 §3 자리에 L646 §3.1~§3.4 4 paragraph 을 통째로 배치. 새 §3 도입부 (§3.0 한 단락) 에서:

- "covariance" 가 본 논문에서 4-pillar cross-validation 의미로만 쓰임을 한 줄 명시 (GR-style general covariance 와 구분).
- 4 paragraph 가 모두 PASS_MODERATE 등급임을 도입부에서 한 번 묶어서 명시 (각 sub-section 끝에서도 반복).

세부 paragraph → sub-section 매핑:

| L646 paragraph | arXiv 새 sub-section | 비고 |
|---|---|---|
| §3.1 SK Schwinger-Keldysh | §3.1 (동일 라벨 유지) | "axiom independence" 표현 그대로 사용 |
| §3.2 Wetterich RG | §3.2 | three fixed points 언급 시 cosmic / cluster / galactic regime 라벨 sync (L654 어휘 갱신과 무충돌 확인 필요) |
| §3.3 Holographic σ₀ | §3.3 | "dimensional statement, not priori derivation" 강조 (L596 sync) |
| §3.4 Z₂ SSB | §3.4 | "discrete symmetry → no Goldstone" 표현 유지 |

추가 권고: §3.5 "Cross-validation summary" 한 단락 신설 — 4 pillar 가 모두 PASS_MODERATE 등급이며 어떤 cross-validation test 가 통과되었는지 요약 (실제 wording 은 8인 Rule-A 리뷰에서 확정).

### §2.2 §4 layered axioms (L646 §4.1~§4.3 3 paragraph) 삽입 위치

권고: 현재 draft §2 (minimal axioms A1/A2/A4/A5) 와 §6 (Hidden DOF) 를 **하나의 새로운 §4 layered axioms** 으로 통합. 현재 draft §4 (PASS_MODERATE evidence) 는 §6 으로 이동.

세부 paragraph → sub-section 매핑:

| L646 paragraph | arXiv 새 sub-section | 비고 |
|---|---|---|
| §4.1 Core axioms (a1 substrate / a2 mass-action / a3 emission balance) | §4.1 | 현재 draft §2 의 A1/A2 와 라벨 collision (§3 참조) — 라벨 통합안 채택 |
| §4.2 Derived axioms (B1 bilinear / a4 geometric 1/(2π) / a6 dark-only) | §4.2 | 현재 draft §2 의 A4/A5 일부와 §3 의 1/(2π) 설명을 흡수 |
| §4.3 Hidden DOF disclosure (9-13 honest items) | §4.3 | 현재 draft §6 의 hidden DOF 항목을 옮겨 옴; 정확한 항목 수 (9 vs 13) 는 8인 Rule-A 에서 확정 |

### §2.3 기존 §3 / §4 재배치 plan

제안 새 목차 (실제 edit 은 submission 단계에서 8인 Rule-A 통과 후):

1. §1 Introduction (현행 유지)
2. §2 (삭제 또는 §4 로 흡수) — 현재 §2 의 minimal axiom import 는 §4 layered axioms 로 통합되므로 §2 는 비움 또는 §4 로 흡수 권고
3. §3 4-pillar covariance (신설; L646 §3.1~§3.4 + §3.0 도입부 + §3.5 summary)
4. §4 Layered axioms (신설; L646 §4.1~§4.3, hidden DOF list 흡수)
5. §5 Derivation of a₀ = c·H₀/(2π) (현행 §3 이동)
6. §6 Evidence at PASS_MODERATE — four channels (현행 §4 이동)
7. §7 Falsifiers (현행 §5 이동, 라벨만 갱신)
8. §8 Discussion / limitations / conclusions (현행 §7 이동)

대안 (재배치 부담 최소화): 현재 §2 / §3 / §4 / §6 라벨을 유지하되 본문만 위 매핑대로 교체. 이 경우 "§3 = a₀ derivation" 이라는 historical 참조가 유효하지 않게 됨 — 라벨 변경이 더 깔끔하나 8인 합의 필요.

---

## §3 Axiom-label collision 해소

현재 draft §2 는 **대문자 A1 / A2 / A4 / A5** 라벨을 사용. paper plan v3 (L634) + L646 §4 는 **소문자 a1 / a2 / a3** (core), **B1 / a4 / a6** (derived) 라벨을 사용. 이 collision 은 통합 시 독자 혼란 유발 위험 큼.

해소안 후보:

1. **소문자 통일안** (권고): plan v3 / L646 의 layered 어휘가 더 명시적이므로 draft 도 소문자 a1/a2/a3 + B1/a4/a6 으로 통일. 현재 draft §2 의 "A1 quantum substrate" → "a1 substrate", "A2 mass-action absorption" → "a2 mass-action", "A4 geometric projection" → "a4 (1/(2π) geometric, derived)", "A5 Hubble pacing" → core/derived 분류는 8인 합의에서 확정 (현재는 a3 emission balance 와 구별하기 위해 별도 라벨 필요).

2. **대문자 유지안**: draft 와의 backward-compatibility 목적. 단 plan v3 의 layered 분류 (core / derived) 가 라벨에서 시각적으로 안 드러나는 단점.

3. **이중 라벨 표기**: 본문 첫 등장 시 "a1 (= draft 이전 버전의 A1)" 형식 한 번 명시 후 이후로는 소문자 통일. backward-compatibility + plan v3 정합성 모두 확보. **plan 단계 권고안**.

A5 (Hubble pacing) 의 위치: 현재 draft §3 a₀ derivation 에서 핵심 인풋이지만 plan v3 layered 구조에서는 core a1-a3 에 들어 있지 않음. 8인 Rule-A 에서 "A5 → a3 (emission balance) 의 cosmological 응용" 인지 "별도 derived axiom" 인지 결정 필요. **본 plan 은 결정하지 않음** (수식/파라미터 없는 plan-only 산출물 원칙).

---

## §4 Submission 환경 적용 (출판 가능 → submission 단계 이동)

사용자 명시 정정: 본 sync 작업은 **plan 단계 산출물 (L656)** 이며, arXiv draft 본문 실제 갱신은 **submission 단계** 에서 8인 Rule-A 리뷰 통과 후 진행. 즉 본 문서가 "출판 가능" 상태를 의미하지 않는다.

submission 단계 진입 전 의무 항목:

- (Q1) 본 plan 의 §2.1 / §2.2 / §2.3 매핑 8인 Rule-A 합의
- (Q2) §3 axiom-label collision 해소안 (소문자 통일안 / 이중 라벨 표기 중 채택) 8인 Rule-A 합의
- (Q3) §3.5 cross-validation summary 단락의 정확한 wording 8인 Rule-A 합의
- (Q4) §4.3 hidden DOF 항목 수 (9 vs 13) 와 정확한 항목 list 8인 Rule-A 합의
- (Q5) **L654 어휘 갱신 sync 의무**: L654 에서 무효화된 B 카테고리 7건 어휘가 L646 §3 / §4 본문 예시 + 본 plan 어디에도 잔존하지 않는지 8인 Rule-A 검증. 잔존 발견 시 본 plan 을 차단하고 L646 본문 예시 부터 재작성 후 재제출.
- (Q6) 라벨 변경 (§2/§3/§4/§6 → 새 §3/§4/§5/§6) 시 cross-reference (figures, tables, references) 일괄 grep & 갱신 plan — 본 작업도 submission 단계에서 별도 4인 Rule-B 코드/문서 grep 리뷰 필요.

submission 단계에서의 실제 edit 대상 파일 (예상):

- `paper/arXiv_PREPRINT_DRAFT.md` (본문 갱신, 라벨 갱신)
- `paper/02_sqmh_axioms.md` (axiom-label collision 해소안 sync)
- `paper/base.md` 의 axiom 목록 라벨 (collision 해소안 sync, 단 base.md edit 은 별도 8인 검토 필요)
- `paper/arxiv_submission_checklist.md` (체크리스트 갱신)
- `paper/COVER_LETTER_v4.md` (4-pillar covariance / layered axioms 어휘 sync)

본 plan 단계 산출물은 위 파일 어느 것도 edit 하지 않는다 (L656 임무 문구 직접 인용).

---

## §5 8인 Rule-A 의무

본 sync plan 은 **이론 클레임** (4-pillar axiom independence, layered axiom 구조, hidden DOF 9-13 list, axiom-label 통일안) 을 직접 다루므로 CLAUDE.md L6 규칙에 따라 arXiv draft 통합 (submission 단계) 진입 전 **8인 순차 Rule-A 리뷰 필수**. 본 plan 자체도 §4 의 Q1~Q6 6 항목 합의가 끝나야 submission 단계로 넘어갈 수 있다.

코드 변경 (라벨 일괄 grep / cross-reference 갱신 등) 은 submission 단계에서 발생하며, 그 시점에 별도 **4인 Rule-B 코드/문서 리뷰** 필요. 본 plan 단계에서는 코드 변경 0건이므로 Rule-B 대상이 아니다.

---

## §6 정직 한 줄

본 L656 sync plan 은 L645 에서 발견된 paper plan v3 ↔ arXiv draft 의 §3 / §4 sync gap 을 닫기 위해 L646 본문 예시를 draft 에 어떻게 통합할지에 대한 *plan 단계* 산출물이며, arXiv draft / paper plan v3 / claims_status / 그 외 어떤 디스크 파일도 본 산출 과정에서 edit 되지 않았다. 4-pillar covariance 와 layered axiom 모두 현재 PASS_MODERATE 등급이며, 본 plan 은 출판 가능 상태가 아니라 submission 단계 진입 전 8인 Rule-A 리뷰를 통과해야 하는 *plan 단계* 임을 명시한다.
