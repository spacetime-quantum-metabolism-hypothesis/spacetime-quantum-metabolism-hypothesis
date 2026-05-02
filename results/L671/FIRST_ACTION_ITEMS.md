# L671 — First Action Items (즉시 / 1주 / 1달 / 1분기 / 2027 Q2)

생성일: 2026-05-02
선행 컨텍스트: L572 ACTION_ITEMS (Phase 11–30, 23건) + Phase 50–55 18 산출물 통합
포지셔닝: 사용자가 01:00 이후 직접 결정/실행 가능한 *concrete actions* 만. abstract plan 제외.

---

## §1. 즉시 (~24시간, 2026-05-03 까지)

### 1.1 사용자 결정 (Paper C 진입 게이트)

- [ ] **D1.** Paper C Draft v3 (L667) 정독 — §1~§7 전 구간
- [ ] **D2.** §6 design objective (L666) 동의 여부 — "정직한 falsifiable phenomenology" 포지셔닝 확정
- [ ] **D3.** Acceptance 양면 인용 동의 — plan 시뮬 63–72% / 회의적 35–50% 양쪽 모두 본문 인용
- [ ] **D4.** Companion B 재포지셔닝 동의 — "case report + framework proposal" (claim 강도 down-tune)

게이트 통과 조건: D1–D4 모두 [x]. 1건이라도 미동의면 §2 차단.

### 1.2 즉시 실행 가능 (사용자 단독, 코드 없음)

- [ ] **A1.** OSF account 등록 — https://osf.io/ — 5 분
- [ ] **A2.** DR3 preregistration document 초안 (L660) → OSF 업로드 *plan* 메모
- [ ] **A3.** arXiv account 확인 — endorsement 상태, primary category (astro-ph.CO)

---

## §2. 1주 (~2026-05-10 까지)

### 2.1 8인 Rule-A 라운드 trigger (L620 Path 1/2)

Paper claim 강도가 [최우선-1] / [최우선-2] 와 충돌 위험 → 외부 cross-validation 필수.

- [ ] **R1.** L648 Template 1 (LLM cross-validation) — 다른 LLM 의뢰 (GPT-5 / Gemini 3 / Grok 4 中 2개 이상)
- [ ] **R2.** L648 Template 2 (third-party human) — NDA 조건 외부 연구자 1인 이상
- [ ] **R3.** L648 Template 3 (time-separated) — 1주 후 self-review (2026-05-09 trigger)

R1–R3 결과 합산 후 paper edit 진입 결정.

### 2.2 Paper plan v3 → 실제 paper edit (Rule-A 통과 후에만)

- [ ] **P1.** L661 v2 / L667 v3 → `paper/PAPER_C.md` (신규 파일)
- [ ] **P2.** L662 → `paper/COMPANION_B.md` (신규 파일)
- [ ] **P3.** L654 어휘 갱신 적용 (claim 강도 / hedging 표현 통일)

Rule-A 미통과 시 P1–P3 차단, 본 항목은 1주 → 2주로 슬라이드.

### 2.3 Schema sync (Rule-B 4인 자율 분담)

- [ ] **S1.** L638 claims_status v1.3 schema → 실제 JSON edit
- [ ] **S2.** L642 schema mismatch 정리 — M1 PASS_MODERATE 통일
- [ ] **S3.** L635 erratum 디렉터리 → CLAUDE.md 등재

---

## §3. 1달 (~2026-06-03 까지)

### 3.1 Submission 준비

- [ ] **M1.** Paper C v3 → JCAP submission template 변환
- [ ] **M2.** Companion B → OJA submission template 변환
- [ ] **M3.** Cover letter 작성 (L319 Phase 11 템플릿)
- [ ] **M4.** Referee response template 준비 (L320 Phase 11)

### 3.2 DR3 Preregistration lock-in

- [ ] **M5.** OSF DOI 등록
- [ ] **M6.** arXiv preprint §7 cross-ref 추가
- [ ] **M7.** Preprint 공개 *이전* lock-in (시점 동결)

### 3.3 README sync (L644)

- [ ] **M8.** README.md 전면 rewrite (L644 18 항목)
- [ ] **M9.** README.ko.md sync
- [ ] **M10.** GitHub 첫페이지 갱신

---

## §4. 1분기 (~2026-08-03 까지)

### 4.1 Submission 진행

- [ ] **Q1.** Paper C → JCAP 제출
- [ ] **Q2.** Companion B → OJA 제출

### 4.2 Review 라운드

- [ ] **Q3.** Reviewer response 작성 (L320 + L663 시뮬 템플릿)
- [ ] **Q4.** Revision round 1 — 시간 예산 ~3주
- [ ] **Q5.** Revision round 2 (필요 시)

---

## §5. 2027 Q2 — DR3 공개 후

- [ ] **Y1.** L657 3 시나리오 decision tree 적용
  - 시나리오 A: DR3 LCDM 회귀 → Paper C falsified, erratum
  - 시나리오 B: DR3 SQT 일치 → 후속 paper (Round 11) 진입
  - 시나리오 C: 모호 (~1.5σ) → re-analysis + DR4 대기
- [ ] **Y2.** Paper revision (시나리오별 분기)
- [ ] **Y3.** 후속 paper 기획 (Round 11)

---

## §6. 의존성 체인

```
D1–D4 (24h 결정)
  ↓
A1–A3 (24h 실행, D 와 병렬 가능)
  ↓
R1–R3 (1주 cross-validation)  ←—— 게이트
  ↓
P1–P3 (paper edit)        S1–S3 (schema, R 와 병렬)
  ↓                          ↓
M1–M4 (submission prep)   M8–M10 (README)
  ↓
M5–M7 (DR3 lock-in)
  ↓
Q1–Q2 (submit)
  ↓
Q3–Q5 (revisions)
  ↓
Y1–Y3 (DR3 공개, 2027 Q2)
```

핵심 차단: R1–R3 (Rule-A) 미통과 시 P/M 전 단계 정지.
독립 트랙: A1–A3, S1–S3, M8–M10 은 D/R 게이트 무관 진행 가능.

---

## §7. 정직 한 줄

본 문서는 *plan / decision support* 이며 Paper / claims_status / 디스크 edit 0건. 모든 실제 변경은 Rule-A (8인) / Rule-B (4인) 통과 후 별도 세션에서 수행.
