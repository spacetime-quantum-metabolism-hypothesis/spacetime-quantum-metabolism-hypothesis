# L665 — Acceptance 정직 격하 sync (L663 회의적 발견 retroactive 적용)

**작성일**: 2026-05-02
**상위 컨텍스트**: L658 (Path 5+1, 63-72%) → L663 (회의적 evaluator, 35-50%)
**본 문서 목적**: Phase 50-53 산출물의 acceptance 추정을 *retroactive* 정직 격하 sync.
**원칙**: [최우선-1] 절대 준수 — 수식 0줄. plan only. paper / claims_status / 디스크 edit 0건.

---

## §1. Acceptance 추정 격하 trajectory (정직)

본 문서는 acceptance 추정의 시간 변천을 단일 표로 통합 — "산술 max 단독 인용" 금지 의무를 만족시키기 위함.

| 시점 | acceptance 추정 | 출판 환경 | 격하/부활 사유 |
|---|---|---|---|
| L490 | 63–73% | 가능 | Pre-audit 초기 추정 |
| L526 R8 | 5% | 가능 | Son+ contingency, audit trough |
| L546 portfolio | 0.50 | 가능 | overlap-corrected portfolio |
| L554 | 0.48 | 가능 | P3a 박탈 반영 |
| L563 | 0.28 | 가능 | fabrication 자발 disclosure |
| L565 / L567 | 0.55 | 가능 | 옵션 C 회복률 81% |
| L597 | 0.55 | 출판 금지 (오해) | plan-only 단계로 잘못 격하 |
| **L653 부활** | 상 하단 | 가능 (사용자 정정) | trajectory 부활 — "중상→상 하단" |
| **L658 plan** | **63–72%** | 가능 | Path 5+1 적용 optimistic |
| **L663 회의적** | **35–50%** | 가능 | hidden DOFs / channel-dep PPN / postdiction |

**해석**: L663 회의적 reality 적용 시 L658 의 "63–72%" 는 *upper-bound plan 시나리오* 로 격하. 실제 인용 시 양면 표기 의무.

---

## §2. 영향 요인 재평가 (positive vs negative)

### Positive (acceptance ↑) — L658 plan 의 자산
- ★★★★★+ 정직성 자산 (fabrication 자발 disclosure, 90%)
- verify 7/7 PASS (재현성 확보)
- paper 본문 28+ paragraph (충실한 limitation 서술)
- L546 portfolio 다중 진입로 (Main / Companion / arXiv)
- L655 Paper C JCAP 1순위 적합성

### Negative (acceptance ↓) — L663 회의적 발견
1. **§6 limitations *marketing tool design* risk**
   - reviewer trust ↓ 우려 — 정직성 자산이 marketing 으로 보일 위험
2. **"0 free parameter" 어휘 잔존**
   - L591 / L654 갱신 후에도 부분 잔존, hidden DOF 비판 직접 노출
3. **channel-dependent PPN ("4/4" 잘못 주장 가능성)**
   - 채널별 차등 효과를 단일 4/4 합격으로 표기한 잔존 risk
4. **3-regime postdiction**
   - 사후 fitting 구조 → reviewer "epicycle" 의심
5. **Verlinde 0.71σ 구분 불가**
   - 경쟁 이론과 데이터-수준 distinction 부재
6. **preregistration internal markdown only**
   - public OSF/Zenodo registration 부재 — 정직성 자산 외부 검증 불가

### 종합
positive 자산이 강하지만 negative 6항목 중 다수가 reviewer 직접 노출 → L663 회의적 35–50% 가 더 신뢰할 만한 mid-range.

---

## §3. 정직 격하 의무 (L658 / L655 / L653 retroactive sync)

### 3.1 L658 의 "63–72%" 어휘
- 변경 전: "Path 5+1 적용 시 acceptance 63–72%"
- 변경 후 (의무): "Path 5+1 plan optimistic 63–72% / L663 회의적 reality 35–50%"
- 단독 인용 금지: "63–72%" 만 인용 시 marketing tool 위반

### 3.2 L655 의 "55–65%" 어휘
- 변경 전: "Paper C JCAP 1순위 acceptance 55–65%"
- 변경 후 (의무): "L663 회의적 reality 35–50% (L655 plan 55–65% 는 plan-only)"

### 3.3 L653 의 "C 상향 (중상→상 하단)"
- 변경 전: "출판 가능 환경 상 하단"
- 변경 후 (의무): "L663 회의적 격하 (중상→중) 적용"

### 3.4 portfolio overlap-corrected 갱신 (질문 항목)
- L565 / L567 옵션 C: 0.55
- L663 회의적 reality 적용 시: **portfolio overlap-corrected ≈ 0.35–0.50 mid-band**
  - (L546 portfolio 의 Main 22% / Companion 47% 가지치기에 회의적 -10~-15pt 적용)
- 본 추정은 *plan-level* 이며 산술 max 단독 인용 금지

---

## §4. 8인 Rule-A 의무 (acceptance 추정 sync)

### 적용 대상
acceptance 추정은 *이론 클레임의 외부 평가* 에 해당 → CLAUDE.md L6 규칙 "이론 클레임 → Rule-A 8인 순차 리뷰" 적용.

### 8인 리뷰 항목 (sync)
1. L658 plan optimistic (63–72%) 의 *marketing tool design* 자기인식 문서화
2. L663 negative 6항목 (channel-dep PPN, 3-regime postdiction, Verlinde 구분 불가, "0 free param" 잔존, §6 marketing risk, prereg 부재) 각각에 대해 8인 합의 부호 (PASS / 부분개선 / OPEN)
3. portfolio overlap-corrected 0.35–0.50 mid-band 채택 합의
4. 양면 인용 의무 ("plan optimistic / 회의적 reality") 모든 후속 산출물 강제
5. paper / claims_status / 디스크 edit 은 8인 합의 *후* 별도 phase 에서만 수행

### 본 phase 금지
- L658 plan-only / L663 회의적 reality 어느 한쪽으로 *결정* 금지 — 양면 동시 보존 의무
- "최종 acceptance = X%" 단일 숫자 결론 금지

---

## §5. 정직 한 줄

> L658 의 63–72% 는 plan optimistic upper-bound, L663 의 35–50% 는 회의적 mid-band — 두 추정 모두 *plan 수준* 이며 단일 숫자 결론 보유 금지, 양면 동시 인용 의무, 그리고 §6 limitations 자체가 *marketing tool* 로 작동하지 않도록 외부 prereg 가 향후 phase 의 진짜 fix 다.

---

## 부록 A. 본 phase 산출 범위

- 변경된 파일: 본 문서 1개 (`results/L665/ACCEPTANCE_HONEST_DEMOTE.md`)
- 변경되지 않은 파일: paper / claims_status / 코드 / 시뮬레이션 0건 (의도적)
- 후속 phase 의무: 8인 Rule-A 리뷰 → 합의 후 L658 / L655 / L653 의 어휘 retroactive 갱신

## 부록 B. 금지 사항 재확인 (체크리스트)

- [x] 수식 0줄 ([최우선-1])
- [x] 산술 max 단독 인용 0건
- [x] paper / claims_status / 디스크 edit 0건
- [x] "최종 acceptance = X%" 단일 결론 0건
- [x] L658 / L663 양면 인용 의무 명시
