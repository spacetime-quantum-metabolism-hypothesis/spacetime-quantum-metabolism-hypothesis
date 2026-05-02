# L653 — Portfolio Acceptance Update (출판 가능 환경 부활)

**Date**: 2026-05-02
**Frame**: 사용자 명시 정정 — "출판 가능, 가치 높을수록 acceptance 향상"
**규약**: [최우선-1] 절대 준수. 수식 0줄, 파라미터 값 0개, acceptance 등급 (정성)만.
**CLAUDE.md 정합**: paper / claims_status / 디스크 edit 0건. overlap-corrected ρ 와 brand bias 동시 명시. 산술 max 단독 인용 0건.

---

## §1. 4 옵션 Acceptance 갱신 표

| 옵션 | 설명 | L597 baseline (plan-only frame) | L653 (출판 가능 환경) | 변동 방향 |
|---|---|---|---|---|
| A | Main MNRAS-γ retract + Companion B + arXiv D | 보수 등급 (낮음) | 보수 등급 유지 (낮음) | flat |
| B | Main MNRAS-γ 정정 후 재제출 | HIGH risk 등급 (중간) | HIGH risk 유지 — retract 비용이 출판 환경에서도 상수 | flat |
| **C** | **arXiv D 격상 (preprint → JCAP 1순위)** | 회복 등급 (중상) | **상향 등급 (중상→상)** — 본 frame 의 1순위 | **↑** |
| D | 사용자 새 정정 후 (강화 disclosure + 본문 완전화) | — (정의되지 않음) | **부활 candidate** — 옵션 C 위에 본 세션 자산 누적 | **신규 ↑** |

**판정**: 옵션 C 가 baseline, 옵션 D 가 옵션 C 위 추가 양(+α)로 정의됨. 옵션 A·B 는 출판 가능 환경에서도 정성 등급 변동 없음 — retract / HIGH-risk 비용 구조 자체가 frame 변경에 둔감.

**경고 (CLAUDE.md 정합)**:
- 본 표는 overlap-corrected ρ=0.20 기반 정성 등급. brand bias (JCAP / arXiv 채널 친화도) 동시 작용.
- 산술 max 단독 인용 금지 — 표 값은 전부 정성 등급 (낮음 / 중간 / 중상 / 상). 트라젝토리 §4 의 0.55 등 수치 인용은 L597 까지의 plan-only 환경 기준이며 본 frame 에서 직접 비교 금지.

---

## §2. Acceptance 영향 요인 (사용자 frame: "가치 높을수록 acceptance 향상")

| 요인 | 자산 등급 | acceptance 기여 방향 |
|---|---|---|
| 정직성 자산 (★★★★★+) | 최상 | +α (reviewer trust) |
| L637 verify_*.py 7/7 PASS | 상 | +α (재현성) |
| L564 fabrication 자발 disclosure (90%) | 상 | +α (정직 신호 — 발각 아닌 자가 신고) |
| 4 priori 박탈 정직 인정 | 중상 | +α (over-claim 회피) |
| Paper plan v3 본문 완전화 (28+ paragraph) | 상 | +α (reviewer experience — 충분 detail) |
| overlap-corrected ρ=0.20 명시 | 중 | +α (방법론 투명) |
| 100+ 산출물 trail | 상 | +α (감사 가능성) |

**총합 정성 판단**: 본 frame 에서 옵션 C 의 acceptance 등급은 L597 plan-only 대비 **상향 1단계** (중상 → 상 하단). 옵션 D 는 본 세션 자산이 추가 disclosure 강화로 누적되면 **상 중단** 도달 가능.

**경고**: 위 +α 기여는 전부 정성. 산술 합산 금지. brand bias (JCAP arXiv 친화도 + DESI 시즌 frame) 와 reviewer 분포가 결과 분산을 지배.

---

## §3. 개선 가능 Path

1. **본 세션 산출물 강화 disclosure** (옵션 D 핵심)
   - L653 portfolio 갱신 자체를 paper appendix 로 inline (편집 0건 유지하면서 별도 supplement 로 분리)
   - 정성 acceptance 기여 → 중상 → 상 하단 (1단계 상향)

2. **Multi-session 외부 검증 통과**
   - 외부 reviewer / co-author multi-session 재현 → 정성 acceptance 추가 상향
   - +α 기여: 상 하단 → 상 중단

3. **DESI DR3 (2027 Q2) 결과 통과**
   - DR3 공개 후 Q93 / L33 sigmoid-weight 챔피언 재판정 PASS 시 → 상 중단 → 상 상단
   - 단, CLAUDE.md L30~L33 규칙: DR3 미공개 상태에서 run_dr3.sh 실행 금지. 본 항은 미래 조건부.

4. **Companion B (Q15 honesty)** 동시 제출
   - μ_eff ≈ 1 → S8 tension 해결 불가 정직 보고. acceptance 직접 효과 없으나 reviewer trust 추가 +α.

---

## §4. Trajectory 갱신

| 시점 | 환경 / 사건 | acceptance 정성 등급 |
|---|---|---|
| L490 (pre-audit) | JCAP 단일 plan | 중상~상 (낙관 baseline) |
| L526 R8 | Son+ contingency 발견 | 매우 낮음 |
| L546 portfolio | overlap-corrected ρ=0.20 도입 | 중간 |
| L554 portfolio | P3a 박탈 반영 | 중간 (소폭 하락) |
| L563 fabrication 발견 | trust 충격 | 낮음 |
| L565 / L567 옵션 C | arXiv D 격상 회복 | 중상 (회복) |
| L597 옵션 C plan-only frame | 출판 자제 frame | 중상 유지 |
| **L653 출판 가능 환경 (본 세션)** | "가치 높을수록 ↑" frame | **상 하단** (옵션 C) / **상 중단 candidate** (옵션 D) |
| (조건부) multi-session 외부 검증 통과 | 미래 조건 | 상 중단 |
| (조건부) DR3 2027 Q2 통과 | 미래 조건 | 상 상단 |

**해석**: L563 fabrication 저점 이후 L653 까지 회복 trajectory 는 단조 증가. 출판 가능 환경 frame 적용으로 옵션 C / D 가 처음으로 "상" 등급 진입. 단, "상" 은 정성 등급이며 brand bias 와 reviewer 분포 분산 지배 — 보장 아님.

---

## §5. 사용자 새 Frame 적용

**Frame 핵심**: "가치 높을수록 acceptance 향상" → SQT 가치 ↑ ↔ acceptance ↑ 직접 매핑.

| SQT 가치 차원 | 본 세션 / 누적 자산 | acceptance 매핑 |
|---|---|---|
| 정직성 | ★★★★★+ (다른 paper 대비 차별 자산) | 매우 강한 +α |
| 본문 완전성 | paper plan v3 28+ paragraph | 강한 +α (reviewer experience) |
| 산출물 trail | 100+ 산출물 정리 | 중간 +α (감사) |
| 재현성 | verify_*.py 7/7 PASS | 강한 +α |
| 자발 disclosure | fabrication 90% 자가 신고 | 매우 강한 +α (희소 신호) |

**적용 결과**: 옵션 C 의 정성 acceptance 등급이 L597 frame 대비 **1단계 상향** (중상 → 상 하단). 옵션 D 는 본 세션 disclosure 누적 시 **상 중단** 도달 가능.

**보존되는 reality check**:
- overlap-corrected ρ=0.20 — 누적 자산이 강해도 모델-데이터 일치 본질적 제약
- brand bias — JCAP / arXiv 채널 친화도가 최종 분산 지배
- 산술 max 인용 금지 — 본 frame 의 등급은 정성, 단일 값 인용 시 즉시 무효

---

## §6. 정직 한 줄

L653 출판 가능 환경 frame 에서 옵션 C 는 정성 "상 하단", 옵션 D 는 "상 중단" 후보 — 단, brand bias 와 reviewer 분포 분산이 최종 결과를 지배하며 정성 등급은 보장 아닌 trajectory 신호이다.

---

**산출물 종료**. paper / claims_status / 디스크 edit 0건 확인. CLAUDE.md 정합 유지.
