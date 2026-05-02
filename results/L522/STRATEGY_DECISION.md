# L522 — Publish 전략 4 옵션 정량 비교 + 최종 권고

**Date**: 2026-05-01
**Status**: 단일 작성자 결정 메모 (8인 Rule-A 리뷰 전)
**상위 컨텍스트**: L520 PUBLISH_STRATEGY (DR3 윈도우 12–18개월), L521 SYNTHESIS_v8 (Q17 부분 / Q13·Q14 미달 / Q15 전원 FAIL), L6-T3 8인 합의 ("정직한 falsifiable phenomenology")

**한 줄 정직**: 현재 상태로는 PRD Letter 노릴 자격이 없고, JCAP 도 격하 framing 으로만 가능하며, *최적 가치는 B+D hybrid (companion methodology paper + arXiv preprint) 로 priority 와 credibility 를 동시에 락인하면서 main JCAP 트랙을 병렬 진행하는 것*이다.

---

## 1. 4 옵션 정량 비교표

수치는 L46–L56 audit, L520 timeline, L521 synthesis, JCAP/PRD 분야 평균 통계를 종합한 *내부 추정* 임을 명시. 8인 리뷰에서 재추정 필수.

| 축 | A: JCAP 격하 재제출 | B: Companion 분리 (methodology only) | C: 6–9개월 R&D 후 PRD Letter | D: arXiv-only (no journal) |
|---|---|---|---|---|
| **Acceptance prob (중앙)** | 13–14% | **55–65%** | 8–12% | N/A (자기수락 100%) |
| **Acceptance prob (lower / upper 90%)** | 6% / 22% | 40% / 75% | 3% / 25% | — |
| **Time-to-submission** | 3–5 개월 | 1.5–2.5 개월 | **6–9 개월 + 추가 R&D 위험** | **2–4 주** |
| **Time-to-published** | 9–14 개월 (peer review 4–6 + revisions) | 5–9 개월 | 12–18 개월 (R&D + review) | **즉시 (preprint)** |
| **Cost (인시 추정)** | 중 (audit 반영 + 8인/4인 리뷰) | 저 (verification infra 만 묶음, 이미 80% 작성됨) | 매우 높음 (Q17 동역학 유도 + Q13 saddle FP — 신규 이론) | 매우 낮음 |
| **DR3 priority 락인** | 강 (peer-reviewed timestamp) | 약–중 (이론 claim 부재) | 위험 (2027-Q1 DR3 와 충돌) | 강 (arXiv timestamp = 학계 1차 priority) |
| **Falsifiability claim 강도** | 중 (격하 framing 으로 약화) | 낮음 (이론 claim 없음) | 매우 높음 (성공 시) / 0 (실패 시) | 중–높음 (OSF 동반 시) |
| **거절 시 회복 비용** | 높음 (재시도 시 6–9개월 추가) | 낮음 (다른 저널 즉시 가능) | 매우 높음 (PRD Letter 거절 후 JCAP 재진입은 사실상 1년 손실) | 0 |
| **Scoop 위험** | 중 (DR3 직전 RVM/IDE 재해석 paper 폭증 예측) | 낮음 (이론 claim 부재) | **매우 높음** (DR3 가 먼저 나오면 사후 fitting 의심 영구 노출) | 낮음 |
| **Q15 (S8) 노출 처리** | limitations 정직 기재 | 해당사항 없음 | 해결 필수 (불가능에 가까움) | limitations 기재 |
| **Reputation downside (거절 시)** | 중 (격하 framing 자체가 자기경고) | 낮음 | **매우 높음** (PRD reject 는 분야 신호) | 매우 낮음 (preprint 는 거절 개념 없음) |
| **Reputation upside (수락 시)** | 중 (JCAP, falsifiable) | 중 (open science / verification infra 기여 인정) | **매우 높음** (PRD Letter = top-tier) | 낮음 (peer review 무) |
| **Citation 기대치 5y** | 15–40 | 20–50 (verification 인프라는 인용률 의외로 높음) | 80–250 (성공 시) / 0 (실패 시) | 5–25 |
| **Risk-adjusted EV (정성)** | **0.135 × 중간 가치 ≈ 낮음** | **0.60 × 중간 가치 ≈ 높음** | 0.10 × 매우 높은 가치 ≈ 중간 (high variance) | 1.0 × 낮은 가치 ≈ 낮음 |
| **8인 합의 (L6-T3) 정합성** | 부분 정합 (포지셔닝은 맞으나 acceptance 가 낮음) | **고정합** (verification infra 가 정직 라인의 핵심) | 비정합 (Q17·Q13 미달 상태에서 PRD 진입 금지 — CLAUDE.md 명시) | 부분 정합 (priority 락인은 맞으나 validation 부재) |

### Acceptance 13–14% 의 출처 분해 (옵션 A)
- JCAP 베이스라인 acceptance ~25–30% (분야 평균).
- Q15 전원 FAIL + Q17 부분 + K19 provisional 의 reviewer flag 누적: -10~12pp.
- Falsifiable prediction 명시 + reproducibility 패키지 + OSF pre-reg: +3~5pp.
- 격하 framing ("phenomenology, not first-principles") 자체의 reviewer 우호도: 중립 (-2 ~ +2pp).
- → 13–14% 중앙값 합리.

---

## 2. 각 옵션의 "globe optimum" 가치 — 최선 시나리오에서의 학문적/전략적 가치

옵션이 *완벽히 작동* 했을 때 SQMH 프로젝트에 가져다주는 가치 (8인 합의 정직 라인 기준).

### A globe optimum
- JCAP published, DR3 (2027) 가 w_a < -0.4 확인 → falsifier 통과 → "DR3 사전예측 적중" 으로 follow-up paper 가속.
- 한계: Q17 미달성은 영구 기록. PRD 트랙 진입은 별도 paper 필요.
- 가치: **중상**. SQMH 가 학계 visible 영역에 진입.

### B globe optimum
- Companion paper = "Cosmological model verification framework: 14-cluster canonical drift class, Fisher pairwise discrimination, dynesty-based evidence pipeline".
- non-controversial → JCAP/MNRAS/OJA 중 acceptance 60% +.
- *2차 효과*: 본 SQMH paper (옵션 A 트랙) 의 재현성 backbone 인용 가능. methodology paper 가 먼저 published 되면 SQMH paper reviewer 우호도 +5~10pp 상승.
- 가치: **중**. 학문적 임팩트는 작지만 *옵션 A 의 acceptance 를 끌어올리는 레버* 역할.

### C globe optimum
- Q17 동역학 유도 (Λ priori 완전) + Q13 saddle FP priori 동시 달성 → PRD Letter accept → SQMH 가 **first-principles** 이론으로 인정.
- citation 100~250 / 5y.
- 가치: **매우 높음**. 그러나 *조건부 확률이 8–12%* 이며, 실패 시 ~9개월 손실.

### D globe optimum
- arXiv preprint + OSF pre-reg → priority 락인. DR3 후 confirmation 시 follow-up paper 에서 인용.
- 한계: peer review 부재 → 학계 인용 약. *주류 cosmology* 에서는 preprint-only 는 보통 50–70% citation 손실.
- 가치: **하중**. priority 는 잡지만 학문적 입지는 약함.

---

## 3. 통합 (hybrid) 가능성

후보 조합과 각각의 정량 효과:

### H1 = B + D (companion methodology + arXiv preprint **본 SQMH paper**)
- **순서**: (1) D 즉시 (2–4주 내) — main SQMH paper arXiv preprint + OSF pre-reg. (2) B 1.5–2개월 — companion methodology paper JCAP 제출. (3) 옵션 A 는 별도 트랙으로 3–5개월 후 main SQMH paper JCAP 제출.
- **상호작용**:
  - D 의 priority 락인이 A 트랙의 *DR3 priority claim* 백업.
  - B 의 acceptance (55–65%) 가 A 의 reviewer 신뢰도 부스트.
  - B 가 먼저 published 되면 A 의 acceptance 13% → **추정 18–22%** 로 상승.
- **총 비용**: D 는 거의 zero. B 는 1.5–2.5개월. A 는 3–5개월 (병렬 일부 가능).
- **거절 회복**: A 가 거절되어도 B+D 는 이미 가치 회수.
- **위험**: D 의 arXiv preprint 가 *완성도 부족* 으로 학계 negative impression 유발 가능 — 따라서 D 는 *최소한 8인 리뷰 1차 통과* 후 제출 필수.
- **EV (정성)**: **최대**. 모든 다른 옵션 단독보다 위험조정 가치 우월.

### H2 = A + D (preprint + JCAP 동시 — L520 권고 라인)
- L520 § 4 시퀀스. priority 강력 락인 + JCAP 트랙.
- B 의 acceptance 부스트 효과 결여.
- **EV**: 중상. H1 보다 한 단계 아래.

### H3 = B + C (companion 먼저, 그 후 PRD Letter 진입)
- B 가 verification infra 로 신뢰 구축 → 9–12개월 후 Q17 달성 시 PRD 진입.
- B 통과해도 C 의 acceptance 8–12% 는 변하지 않음 (이론 자체 문제).
- C 실패 시 B 만 남음 — 하지만 B 단독 가치보다 9개월 늦은 실패.
- **EV**: 중. B+D 대비 시간 손실.

### H4 = A + B + D (전 트랙)
- 자원 분산 위험. SQMH 단일 작성자 환경에서 3 트랙 동시 진행은 각 trace 의 품질 저하.
- B+D 부터 시작하고 A 를 *조건부* (B 통과 후) 진행하는 H1 의 sequencing 이 우월.
- **EV**: H1 과 비슷하나 timing 제어 떨어짐.

---

## 4. 최종 권고

### 권고: **H1 (B + D 즉시 병행 → A 후속 트랙)**

#### 실행 순서

| 단계 | 시점 | 산출 | 게이트 |
|---|---|---|---|
| S0 | 2026-05 (지금) | 8인 Rule-A 리뷰 (이 STRATEGY_DECISION 메모 + L520/L521 통합) | 합의 도달 시 진행 |
| S1 | 2026-05 ~ 2026-06 (4–6주) | B paper draft (companion methodology): 14-cluster canonical drift class, Fisher pairwise, dynesty pipeline, reproducibility infra. 4인 Rule-B 코드 리뷰. | B draft 완성 |
| S2 | 2026-06 말 | OSF pre-registration 등록 (L520 § 5 항목 1–4) | OSF DOI 확보 |
| S3 | 2026-07 초 | **D 실행**: main SQMH paper arXiv preprint 제출 (현 audit 반영본, 격하 framing). Companion B 도 같은 주에 arXiv + JCAP 제출. | arXiv ID 2건 확보 |
| S4 | 2026-07 ~ 2026-09 | A 트랙: main SQMH paper 를 JCAP submission 형태로 다듬기. B 의 reviewer feedback 받으면서 A 보강. | A draft submission-ready |
| S5 | 2026-09 ~ 2026-10 | A 실행: main SQMH paper JCAP 제출 (OSF pre-reg + companion B 인용). | A under review |
| S6 | 2026-12 마지노선 | 전 트랙 preprint 락인 완료 상태. | 미완 시 재계획 |
| S7 | 2027-Q1 ~ Q2 | DR3 발표 후 falsifier 적중/탈락 판정 → letter form companion 별도 (L520 § 4-5). | — |

#### 명시적 KILL 조건
- **B 가 거절될 경우**: A 의 acceptance boost 효과 상실. A 트랙 재평가 — 가능하면 OJA / MNRAS 로 변경.
- **D arXiv preprint 가 8인 리뷰에서 통과 못함**: D 보류, B 만 진행. priority 락인 약화 수용.
- **2026-12 까지 D 미실행**: priority claim 포기, post-DR3 정직 라인으로 전환.

#### 옵션 C (PRD Letter) 처리
- **공식 포기** (CLAUDE.md L6 규칙: "조건 미달 상태에서 PRD Letter 제출 금지").
- *하지만* B+D+A 진행 중 Q17 동역학 유도가 우연히 도출되면, 그 시점에 별도 PRD Letter 트랙을 *추가* (현재 paper 의 결과를 변경하지 않음 — 새로운 letter 로).
- 즉 C 는 "포기" 이지 "차단" 은 아님.

#### 옵션 A 단독 (현 framing) 비권고 이유
- 13–14% acceptance 는 *3–5개월 작업 + 8인/4인 리뷰 + reproducibility 패키지* 의 노력 대비 비효율.
- B 의 acceptance boost 없이 진행하면 거절 후 회복 비용 6–9개월.
- 거절 시 SQMH 의 전체 publish 트랙이 1년 지연 → DR3 priority 상실.

#### 최종 한 줄 정직
**옵션 A 단독 13% 는 B+D 백업 없이 도박이고, 옵션 C 는 자격 없는 PRD 시도이고, 옵션 D 단독은 학계 입장권 못 얻는다 — H1 (B+D 즉시 + A 후속) 만이 위험조정 EV 최대이며 8인 합의 정직 라인과 정합한다.**

---

## 5. 의존성 / 리스크 / 미정 항목

- **8인 Rule-A 리뷰 미실시**: 이 메모는 단일 작성자 추정. acceptance 수치, time cost, EV 모두 8인 검토에서 ±30% 변동 가능.
- **B paper scope 미정**: "verification infrastructure only" 의 정확한 범위 (RSD growth pipeline 포함 여부, Fisher pairwise framework, dynesty wrapper) 는 S1 단계에서 4인 Rule-B 가 정함.
- **JCAP vs OJA vs MNRAS for B**: methodology paper 에는 OJA (Open Journal of Astrophysics) 가 acceptance 70%+ 이며 DOI 학계 수용 양호. 별도 검토 필요.
- **arXiv 카테고리**: astro-ph.CO primary, gr-qc cross-list. 정직 라인 유지를 위해 hep-th 는 제외.
- **DR3 timeline 변동**: LBL 4월 2026 발표 ("2027 expected") 가 늦어지면 A 트랙 여유 증가. 빨라지면 D 의 2026-07 락인이 더 중요.

## Sources
- L520 PUBLISH_STRATEGY.md (DR3 timeline + OSF/arXiv priority 분석)
- L521 SYNTHESIS_v8.md (Q17/Q13/Q14/Q15 상태)
- CLAUDE.md L5–L6 재발방지 (PRD Letter 진입 조건, 8인/4인 리뷰 규칙)
- L6-T3 8인 합의 (정직한 falsifiable phenomenology 포지셔닝)
