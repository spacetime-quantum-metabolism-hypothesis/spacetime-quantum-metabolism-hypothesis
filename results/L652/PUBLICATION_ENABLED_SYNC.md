# L652 — Publication-Enabled Retroactive Sync Plan

**작성일**: 2026-05-02
**Trigger**: 사용자 직접 정정 (2026-05-03 00:00+ KST)

> "이 논문은 출판가능함. '출판금지' 는 과거 내 지시의 오해이자 착각이었음.
>  출판가능하고 할꺼고 단지 논문의 가치가 높을수록 출판가능성이 점점 더 올라감."

본 정정은 Phase 22-49 의 **102 개 산출물** 의 *근본 가정* 을 갱신한다:
"submission 영구 금지" → "submission 가능, 가치 높을수록 acceptance 향상".

**[최우선-1] 준수**: 본 문서는 sync *plan* 만이며, 실제 산출물 본문 edit 0 건.
모든 수식 0 줄. 8인 Rule-A 의무.

---

## §1. 즉시 무효화 항목 (잘못된 가정에 의존)

| # | 산출물 | 무효화 사유 | 갱신 방향 |
|---|---|---|---|
| 1 | L569 PHENOMENOLOGY_PIVOT | "phenomenology framework 영구 전환" 어휘는 출판 환경에서 *가치 격하* 효과 — 부정확 | "phenomenology framing 은 정직 전략, submission 시 reviewer 친화 reframing 가능" |
| 2 | L591 PAPER_HONEST_REFRAMING | "출판 시도 영구 금지" 가정 위에 작성됨 | "honest reframing 유지하되 submission 경로 개방, 가치 향상에 따라 PRD/JCAP/MNRAS" |
| 3 | L597 FINAL_RECOMMENDATION_v2 | 옵션 C "plan-only" — submission 진행 부재 | 옵션 C *submission 진행* 으로 갱신 (plan + execution) |
| 4 | L600 GRAND_SUMMARY | "submission 영구 금지" 한계 5건 항목 | 한계 항목에서 "submission 금지" 제거, "가치 의존 acceptance" 로 |
| 5 | L617 PAPER_PLAN_PARADIGM | submission 영구 금지 frame | submission 가능 frame + 저널 선택 단계화 |
| 6 | L622 PARADIGM_GRAND_SUMMARY | frame D (보류) 권장 | submission 가능 환경에서 frame 재평가, frame B/C 부활 검토 |
| 7 | L624 FINAL_SUMMARY | "출판 영구 금지" 한계 항목 | 한계 → "현재 가치 수준에서의 acceptance 확률" 로 재기술 |
| 8 | L629 PROCESS_PAPER | "출판 금지 환경 전용 가치" 가정 | process paper 도 submission 가능 (MNRAS Methods, RNAAS 등) |
| 9 | L634 PAPER_PLAN_V3 §7/§8 | submission 영구 금지 어휘 | §7 outlook + §8 reproducibility 어휘 갱신 (§4 참조) |
| 10 | L644 README_SYNC_PLAN | "submission 영구 금지" 어휘 정정 항목 | 정정 항목 자체를 갱신 — README 에 submission 가능성 명시 |
| 11 | L647 POSITIVE_ASSET_QUANT | 학계 mainstream 가치 ★★ (낮음) | ★★★~★★★★ 부활 (output quality 의존) |
| 12 | L648 EXTERNAL_REVIEW_TEMPLATES | Path 5 boundary "출판 금지 vs preprint" 모호성 | Path 5 → "preprint + peer-review submission" 명시화 |

**총 12 산출물 즉시 어휘 갱신 대상**.

---

## §2. 부분 갱신 항목 (submission 환경 변화 영향 적음)

| # | 산출물 | 상태 | 비고 |
|---|---|---|---|
| 1 | L582 mass redef 영구 종결 | 그대로 유지 | submission 무관, 물리적 종결 사실 |
| 2 | L549 / L552 / L562 / L566 4 priori 박탈 | 그대로 유지 | submission 무관, 정직성 사실 |
| 3 | L564 fabrication 90% disclosure | **더 중요** | submission 환경에서 pre-submission 정정 의무 강화 |
| 4 | L573 / L594 cross-consistency audit | 그대로 유지 | 결과 자체는 출판 가능 자산 |

**원칙**: 물리/수치 사실은 변경 없음. submission 어휘만 갱신.

---

## §3. 부활 항목 (submission 가능 환경에서 재활성화)

| # | 항목 | 이전 상태 | 부활 후 상태 |
|---|---|---|---|
| 1 | L565 옵션 C arXiv→JCAP 0.55 acceptance | 잠정 보류 | **부활**, JCAP 1차 타겟 |
| 2 | L567 OPTION_C_EXECUTION timeline | 비활성화 | **재활성화**, 단 가치 향상 우선 |
| 3 | 학계 mainstream 가치 평가 (L647) | ★★ (출판 금지 가정) | ★★★~★★★★ (output quality 의존) |
| 4 | PRD Letter 경로 | 영구 차단 | 조건부 부활 (Q17 완전 달성 OR Q13+Q14 동시 달성 — CLAUDE.md 기존 규칙) |
| 5 | MNRAS / Phys. Dark Univ. 보조 경로 | 미고려 | 후보 추가 |

---

## §4. paper plan v3 어휘 갱신 plan

**대상 파일**: `results/L634/PAPER_PLAN_V3.md` (가정)

### §0 Abstract
- **이전**: "출판 시도 영구 금지" / "preprint-only honest disclosure"
- **갱신**: "submission 가능, 가치 향상에 따라 acceptance 확률 상승. 1차 타겟 JCAP, 보조 PRD Letter (조건 충족 시) / MNRAS"

### §7 Outlook
- **이전**: "출판 영구 금지, 후속 연구만 진행"
- **갱신**: "submission 시기 = paper 가치 임계 도달 시점. 저널 선택 단계화: JCAP (현재 가치) → PRD Letter (Q17 OR Q13+Q14 시) → MNRAS (process paper 분리 시)"

### §8 Reproducibility
- **이전**: "preprint 단계만, submission 영구 금지"
- **갱신**: "preprint (arXiv) + peer-review submission. 재현성 자료 (data/code/seed) 모두 supplementary 로 동행"

**수식 0 줄 원칙 준수** — 어휘 변경만, 모델/수치 변경 없음.

---

## §5. 8인 Rule-A 의무

본 sync 자체가 8인 Rule-A 의무 — submission 환경 변화는 *모든* 산출물 의 근본 가정에 영향, 따라서 8인 (이론 클레임 레벨) 순차 리뷰 대상.

**리뷰 항목**:
1. submission 환경 변화가 정직성 어휘 (L591/L600/L624) 에 미치는 영향 — overclaiming 위험 평가
2. 옵션 C 부활 (L565/L567) 의 timeline 현실성
3. PRD Letter 조건 (Q17 OR Q13+Q14) 충족 가능성 재평가
4. paper plan v3 어휘 갱신안 (§4) 의 reviewer 친화도
5. mainstream 가치 ★ 등급 재평가 (L647) — 객관 근거
6. fabrication disclosure (L564) 의 pre-submission 정정 의무 강화 절차
7. process paper (L629) 분리 submission 전략
8. external review template (L648) Path 5 갱신안

**리뷰 완료 전 산출물 본문 edit 금지** (CLAUDE.md L6 8인/4인 규칙).

---

## §6. 정직 한 줄

> submission 가능 환경에서 paper 의 가치는 *부활* 했다.
> 단, 가치는 자동 부활하지 않는다 — output quality (현재 발견 + 정직한 한계 명시 + 재현성) 가
> 가치를 결정하며, submission 시점과 저널 선택은 그 가치에 의존한다.
> 본 sync 는 어휘만 갱신할 뿐, 물리적/수치적 사실은 변경하지 않는다.

---

## §7. 다음 단계

1. 8인 Rule-A 리뷰 세션 개시 (§5 8 항목)
2. 리뷰 합의 후 §1 의 12 산출물 어휘 패치 (별도 LXX session, 본 L652 에서 edit 금지)
3. paper plan v3 어휘 갱신 (§4) — Rule-A 합의 후 단일 commit
4. README (L644) 어휘 동기화
5. external review template (L648) Path 5 갱신
