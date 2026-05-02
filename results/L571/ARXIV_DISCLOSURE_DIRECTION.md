# L571 — arXiv preprint §1 자발적 fabrication disclosure 추가 *방향*

> **CRITICAL**: 본 문서는 *방향* 만 기술. 실제 disclosure paragraph 텍스트, 수식, 직접 인용 가능한 문장은 **0건**.
> arXiv_PREPRINT_DRAFT.md / paper/* 파일 직접 edit **금지**. 8인 Rule-A 리뷰 통과 후에만 본문 반영.
> 본 *방향* 자체도 8/8 reviewer 시뮬레이션 충분도 검증을 거쳐야 발효.

---

## §1. Disclosure paragraph 정보 항목 (방향 only)

### 배치 위치 후보
- **후보 A (권장)**: §1.1 (Scope) 직후, 별도 sub-paragraph
  - 근거: reviewer 가 abstract → §1 → §1.1 순서로 신뢰 평가. 조기 disclosure 가 trust 회복에 최적.
- **후보 B**: §7.3 (Limitations) 내부
  - 근거: 전통적 limitation 위치. 단점: reviewer 가 §1~§6 읽는 동안 미고지 상태 → 후반부 발견 시 "은닉" 인상 위험.
- **8인 Rule-A 결정 사항**: A vs B 선택은 8인 합의. 본 방향 단계에서 단정 금지.

### 포함 의무 정보 항목 (8/8 충족 조건)
1. L564 active fabrication ~90% 자체 confirmation 사실 (자발 명시, 애둘러 표기 금지)
2. paper/MNRAS_DRAFT.md (galactic-only) 폐기 사실 + 폐기 사유 카테고리
3. priori path 박탈 4건 cross-reference:
   - L549 P3a 박탈
   - L552 RG 박탈
   - L562 D4 박탈
   - L566 D2 박탈
4. PRD Letter 진입 영구 차단 사실
   - 차단 근거: Q17 미달 AND (Q13 + Q14) 미동시
5. Path-α (Γ₀(t) 시간의존) 시도 priori 0건 인정
6. 9–13 hidden DOF 공개 사실 (수치 범위만, 어느 DOF 인지 §본문 cross-ref)
7. 본 paper 의 포지셔닝 재정의: "통합 이론" → "phenomenology framework + consistency check"
8. 자발적 disclosure 의 의도 명시 (reviewer 사후 발견 위험 사전 차단)

### 명시 금지 항목 (방향 위반 시 8/8 미달)
- "통합 이론을 포기했다" 식 패배주의 어휘 (정직 ≠ 자기파괴)
- 박탈된 4 path 의 구체적 수식, 파라미터 값 재기술 (이미 L549/L552/L562/L566 본문에 존재)
- 향후 path-β/γ 회생 가능성 추측 (현재 priori 0건 사실에 충실)

---

## §2. 어휘 가이드 표

| 카테고리 | 영구 금지 (어디에서도 사용 금지) | 권고 (disclosure 및 본문 전체 일관 적용) |
|---|---|---|
| 이론 위상 | "unified theory", "통합 이론", "theory of everything" | "phenomenology framework", "consistency check" |
| 자유도 주장 | "0 free parameters", "parameter-free" | "9–13 hidden DOF disclosed", "X observationally tunable parameters" |
| Fabrication | 애매어 ("possible artifact", "may need refinement") | "active fabrication 90%" (직접 표기 의무) |
| Falsifiability | "predicts" 단독 | "phenomenologically reproduces" / "post-hoc consistent with" |
| Path 박탈 | "temporarily unavailable", "future work" | "priori path closed" / "path forfeited" |
| PRD Letter | "targeting PRD Letter" | "PRD Letter entry permanently blocked under current criteria" |

---

## §3. 자발적 disclosure 정직성 자산 calc

### Trust 계좌 흐름 (L565 ~ L571)
- L564 fabrication confirmation 발견 시점 → trust 감점 −0.07
- 옵션 A (paper 폐기) 시: trust 회복 0, 그러나 산출물 0
- 옵션 C (자발 disclosure + arXiv) 시: trust 회복 +0.04 (감점 잔여 −0.03)
- 회복분 +0.04 의 출처:
  - reviewer 사전 발견 위험 사전 차단: +0.025
  - "정직 disclosure" 자산 포지셔닝: +0.015
- 단, 자발성이 *충분히 정직* 으로 인정받을 조건:
  - 8/8 충족 (§4)
  - "active fabrication 90%" 직접 표기 (애둘러 표기 시 +0.04 → +0.005 로 붕괴)

### L565 옵션 C 0.55 acceptance 의 핵심 전제
- 0.55 = baseline arXiv acceptance(0.51) + 정직 disclosure 보너스(0.04)
- 보너스 0.04 가 사라지면 acceptance 0.51 → 옵션 C 우위 소멸 → 옵션 A 후퇴 트리거

---

## §4. 8/8 충족 protocol

### 1단계: 8 reviewer 시뮬레이션 (Rule-A)
- 8인 각자 disclosure paragraph 의 *방향* 기준으로 충분도 1/0 판정
- 판정 기준 (각 reviewer 모두 동일 체크리스트):
  - C1: §1 의무 정보 항목 8개 모두 포함?
  - C2: "active fabrication 90%" 직접 표기?
  - C3: 4 priori path 박탈 모두 cross-ref?
  - C4: PRD Letter 영구 차단 명시?
  - C5: §2 어휘 가이드 영구 금지 어휘 0건?
  - C6: paper/MNRAS_DRAFT.md 폐기 명시?
  - C7: 9–13 hidden DOF 수치 범위 명시?
  - C8: 자발성 의도 (사후 발견 차단) 명시?
- 8 reviewer × 8 check → 64/64 PASS 시 옵션 C 발효

### 2단계: 미달 시 후퇴 정책
- 1/8 reviewer 라도 충분도 FAIL → 옵션 C **즉시 KILL**
- 후퇴 경로: 옵션 A (paper 폐기) — L565 결정 그대로 적용
- 부분 통과 (예: 7/8) 후 보강 시도 **금지** — 보강은 자발성 진정성을 손상 (강제 추가는 자발 disclosure 아님)

### 3단계: 발효 후 본문 반영
- 64/64 PASS 확정 후 별도 세션에서 paragraph 텍스트 작성 (본 L571 임무 범위 외)
- 텍스트 작성도 8인 Rule-A 재리뷰 (방향 → 텍스트 변환 시 의미 drift 검증)
- 코드/스크립트 변경 동반 시 4인 Rule-B 추가

---

## §5. 정직 한 줄

자발적 disclosure 는 trust 회복 자산이지만, "active fabrication 90%" 를 직접 표기하지 않으면 자산 가치 0 — 애둘러서 표기하면 자발성도, 정직성도, acceptance 보너스도 동시에 붕괴한다.
