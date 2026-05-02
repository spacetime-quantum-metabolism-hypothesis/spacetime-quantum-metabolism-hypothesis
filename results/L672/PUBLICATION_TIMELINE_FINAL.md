# L672 — Publication Final Timeline (2026-05-03 → 2027 Q3)

작성일: 2026-05-02
범위: Paper C (JCAP) + Companion B (OJA) + Paper A (retract/정정 결정) + DR3 contingency
근거: L597 (publication readiness), L661 v2 (status), L667 v3 (plan), L572/L592 (기존 timeline)

---

## §1 주별 / 월별 Timeline

### Phase 0 — Decision Week

| 기간 | Week | 주요 산출물 / 결정 |
|------|------|---------------------|
| 2026-05-03 ~ 05-10 | Week 1 | L597 / L661 v2 / L667 v3 정독 · frame 결정 (Paper C 1순위 vs portfolio C+B+A 동시) · Paper A retract or 정정 결정 (L564 fabrication 처리) · OSF account 등록 |

### Phase 1 — Rule-A/B Review Round

| 기간 | Week | 주요 산출물 |
|------|------|-------------|
| 2026-05-10 ~ 05-17 | Week 2 | 8인 Rule-A round 1 (L648 Template 1 — 이론 클레임) · paper plan v3 review |
| 2026-05-17 ~ 05-24 | Week 3 | 8인 Rule-A round 2 (L648 Template 2 — phenomenology / positioning) · 4인 Rule-B (verify scripts cross-check) |
| 2026-05-24 ~ 05-31 | Week 4 | Rule-A/B 통과 후 paper plan v3 → 실제 paper edit 착수 |

### Phase 2 — Submission 준비 (Month 2)

| 기간 | 주요 산출물 |
|------|-------------|
| 2026-06-01 ~ 06-15 | Paper C v3 → JCAP submission template 변환 · Companion B → OJA submission template 변환 |
| 2026-06-15 ~ 06-30 | cover letter 초안 · referee response template (L320 + L663 reviewer 시뮬 기반) · DR3 preregistration document → OSF DOI 등록 (DR3 공개 *이전* lock-in 필수) |

### Phase 3 — Submission 진행 (Month 3)

| 기간 | 주요 산출물 |
|------|-------------|
| 2026-07-01 ~ 07-15 | 최종 author check · arXiv preprint 동시 공개 준비 |
| 2026-07-15 ~ 07-31 | Paper C → JCAP 제출 · Companion B → OJA 제출 · arXiv preprint 공개 |

### Phase 4 — Review 라운드 (Month 4-6)

| 기간 | Month | 주요 활동 |
|------|-------|-----------|
| 2026-08 | Month 4 | referee 1차 응답 대기 / Companion B 빠른 review (OJA 평균 ~6주) |
| 2026-09 | Month 5 | referee response 작성 (L320 + L663 simulated reviewer 활용) · revision draft |
| 2026-10 | Month 6 | revision 제출 · 추가 referee round 대응 |

### Phase 5 — Final Acceptance (Month 7-9)

| 기간 | Month | 주요 활동 |
|------|-------|-----------|
| 2026-11 | Month 7 | OJA Companion B accept/reject 1차 결정 예상 |
| 2026-12 | Month 8 | JCAP Paper C accept/reject 1차 결정 예상 |
| 2027-01 | Month 9 | 최종 accept/reject 정리 · 후속 (Round 11) plan 초안 |

### Phase 6 — Buffer (Month 10-12)

| 기간 | Month | 주요 활동 |
|------|-------|-----------|
| 2027-02 | Month 10 | 추가 revision round 대응 (필요 시) |
| 2027-03 | Month 11 | preprint update · arXiv v2 |
| 2027-04 | Month 12 | DR3 직전 preregistration freeze 확인 |

### Phase 7 — DR3 분기점 (2027 Q2)

| 기간 | 주요 활동 |
|------|-----------|
| 2027-05 ~ 06 (DR3 공개 직후) | L657 3-시나리오 decision tree 가동 · 시나리오 A (PASS): paper revision + 후속 paper · 시나리오 B (Inconclusive): minimal update · 시나리오 C (KILL): paper retraction or framework 격하 |

### Phase 8 — Post-DR3 (2027 Q3)

| 기간 | 주요 활동 |
|------|-----------|
| 2027-07 ~ 09 | 시나리오 A: 후속 Round 11 paper 본격 시작 · 시나리오 C: framework 격하 / retraction protocol 수행 · 시나리오 B: hold pattern + DR4 대기 |

---

## §2 가정 / 전제

1. 출판 가능 환경 (사용자 정정 — Phase 50).
2. acceptance 회의적 추정: Paper C 35-50%, Companion B 25%.
3. DR3 (2027 Q2) 가 primary trigger — 운명 분기점.
4. 8인 Rule-A 통과 의무 (이론 클레임 / positioning 양 라운드).
5. 4인 Rule-B 통과 의무 (verify scripts / 코드 cross-check).
6. Paper A 처리 결정 미완 (L564 fabrication) — Week 1 결정 필수.
7. 모든 schedule 은 referee response 평균 6-8주 가정. JCAP 평균 3-4 month 1차 결정.
8. DR3 공개 일정은 DESI 발표에 의존 (2027 Q2 추정, 변동 가능).

---

## §3 의존성 체인

```
[Week 1 Decision]
   ├─ frame (single vs portfolio)
   ├─ Paper A 처리
   └─ OSF account
        │
        ▼
[Rule-A/B Round (Week 2-4)]
   ├─ 8인 Rule-A (Template 1 → Template 2)
   └─ 4인 Rule-B (scripts cross-check)
        │ (통과 의무)
        ▼
[Paper edit (Week 4 → Month 2)]
        │
        ▼
[OSF preregistration DOI]  ← DR3 lock-in 필수
        │
        ▼
[Submission (Month 3)]
   ├─ JCAP (Paper C)
   ├─ OJA (Companion B)
   └─ arXiv preprint
        │
        ▼
[Review (Month 4-6)] ─ L320 + L663 simulated reviewer
        │
        ▼
[Acceptance (Month 7-9)]
        │
        ▼
[Buffer (Month 10-12)] ─ revision / preprint v2
        │
        ▼
[DR3 trigger (2027 Q2)] ─ L657 3-시나리오 decision tree
        │
        ├─ A (PASS) → 후속 Round 11
        ├─ B (Inconclusive) → minimal update
        └─ C (KILL) → retraction / framework 격하
```

핵심 의존성:
- Rule-A/B 미통과 시 Paper edit 진입 금지 → submission 전체 지연.
- OSF DOI 등록은 DR3 공개 *이전* 이어야 preregistration 효력 유지.
- DR3 시나리오 C 시 retraction protocol 이 후속 paper 모든 plan 우선.

---

## §4 기존 Timeline (L572 / L592) 와 Sync

| 항목 | L572 / L592 | L672 (본 문서) | 차이 / 갱신 |
|------|-------------|-----------------|-------------|
| Submission window | 2026 Q3 (estimate) | 2026-07 (Month 3) | 구체화 — Rule-A/B 통과 후 |
| DR3 분기점 | 2027 Q2 | 2027 Q2 (유지) | 동일 |
| Companion B 포함 | optional | 의무 (portfolio 옵션 시) | 강화 |
| Paper A 처리 | 미결 | Week 1 결정 강제 | 신규 |
| OSF preregistration | 언급만 | Month 2 DOI 등록 의무 | 신규 |
| Rule-A/B round | 1회 | 2회 (Template 1 + 2) | 강화 |
| Buffer | 없음 | Month 10-12 | 신규 |

기존 timeline 의 일정 가정은 유지하되, Rule-A/B 의무화 + OSF preregistration + Paper A 결정 강제로 현실화.

---

## §5 정직 한 줄

본 timeline 은 8인 Rule-A 통과 + DR3 미공개 가정 위에 구축된 추정 schedule 이며, 실제 submission / acceptance 일정은 referee 응답 속도와 DR3 공개 시기에 따라 ±2-3 month 변동 가능, 시나리오 C (DR3 KILL) 시 전체 retraction 으로 reset 될 수 있다.
