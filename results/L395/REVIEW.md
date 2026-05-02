# L395 — REVIEW (8인 자율 분담)

CLAUDE.md Rule-A: 이론 클레임 (정직 disclosure 적정성 + hedging 차단) → 8인 순차 리뷰. 역할 사전 지정 없음, 자율 분담.

대상: ATTACK_DESIGN.md (옵션 C 통합) + SEC6_DRAFT.md (14-row 표 + 비단조 fit caveat 단락 + hedging-free 표현).

---

## R1 (이론 일관성)
14-row 카운트는 L368 과 일치 (4+6+2+2). 옵션 C 의 footnote 통합은 L346 J1 (비단조 fit) 을 행 4 / 행 7 의 *원인 근거* 로 연결하므로 의미상 정합. **PASS**.

## R2 (정직성 — hedging 차단)
SEC6_DRAFT 가 "future Phase 7 will solve" 류 표현 사용 안 함. 대신 "remains structural", "deferred", "consistent with, but not predicted by" 사용. L368 R2 conditional 의 잔존 우려 해소. **PASS**.

## R3 (저널 적합성)
JCAP/MNRAS/PRD 모두 14-row 표 + 별도 caveat 단락 분량 (~1.5 페이지) 허용. PRL Letter 진입은 L6 의 Q17/(Q13+Q14) 조건 미달이라 비대상 — Sec 6 형식은 JCAP 중심. **PASS**.

## R4 (재발방지 부합)
- "Limitations table 카운트 변경 시 abstract / sec 6 첫 단락 / 표 캡션 / cross-reference 4곳 동기화 필수" — 옵션 C 가 카운트 14 유지하므로 트리거 없음. **PASS**.
- "Background-only μ_eff≈1 모델은 cosmic-shear / S_8 영구 미해결, 'future Phase X resolves' 약속 표현 금지" — 행 13 Mitigation 컬럼이 "permanent limitation" 표현 사용. **PASS**.
- L346 J3 권고 ("'4 pillar 가 비단조성을 예측한다' 류 표현 약화 또는 삭제") — caveat 단락에서 명시적으로 "postdiction, not prediction" 표기. **PASS**.

## R5 (수치 카운트 동기화 점검)
- abstract: 본 loop 산출물 SEC6_DRAFT 는 Sec 6 단독. abstract 갱신은 후속 LaTeX 통합 loop 책임. 본 review 는 카운트 14 일관성만 확인. **PASS** (조건부, 통합 시 재확인).
- Sec 6 첫 단락 "fourteen acknowledged limitations" 표기 확인. **PASS**.
- 표 캡션 "Fourteen acknowledged limitations" 확인. **PASS**.
- 본문 cross-reference (Sec 5 BMA, Sec 7 future) — SEC6_DRAFT 에 reference 자리 마커 명시. **PASS**.

## R6 (옵션 C 정당성 — 옵션 A/B 와 비교)
- A (15-row 추가): 4곳 동기화 트리거, 리스크 큼. 기각 합리.
- B (행 4/7 텍스트만 강화): caveat 의 *논리적 위치* (4-pillar 강도 평가) 가 표 한 행 안에 들어가지 않음. 별도 단락이 필요. 기각 합리.
- C (footnote + 별도 단락): 카운트 유지 + L346 J1 표현 직접 인용 + Sec 3 prediction 류 표현과의 cross-link 가능. 채택 정당. **PASS**.

## R7 (격하 vs positive 균형)
- Negative: 비단조 fit caveat 명시 → reviewer "왜 prediction 으로 표기하지 않는가" 의문 차단 (-0%). 단 외부 독자에게 "이 이론은 비단조를 예측하지 않는다" 인상 부담 (-0.5~-1%).
- Positive: hedging 차단 + L346 정직 통합 → reviewer trust +1~+2%, 특히 JCAP referee culture 에 정합 (+1%).
- 순 영향: 약 +0~+1% (대체로 중립~약 positive). **PASS**.

## R8 (재발방지 후보 신규)
권고 신규 항목:
- "비단조 / 단조 형상 prediction vs fit 구분은 4-pillar a priori 강제력 분석 (L346 axis A1) 후에만 'prediction' 표현 허용. 구분 없이 'predicts non-monotonic' 표현 영구 금지."
- "Sec 6 limitations 표는 *외부 한계*, 4-pillar 내부 강도 caveat 는 *별도 단락* 으로 분리 통합. 한 행에 섞으면 의미 충돌."
**ACCEPT**.

---

## 종합 판정
- 8/8 PASS. R5 만 후속 LaTeX 통합 loop 에서 abstract 카운트 재확인 조건부.
- ATTACK_DESIGN (옵션 C) + SEC6_DRAFT 채택 권고.
- L396+ 에서 LaTeX 본문 직접 반영.

## 한 줄

> 14행 limitations 표 + 비단조 postdiction caveat 분리 통합, hedging 차단 8/8 통과 — JCAP 정직 disclosure 완성.
