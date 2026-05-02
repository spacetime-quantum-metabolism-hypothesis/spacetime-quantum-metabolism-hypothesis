# L596 — L591 어휘 통일 vs L577~L583 retroactive sync *방향*

**전제**: 본 문서는 *방향* 산출물. L577~L583 본문 직접 edit 0건. 수식 0줄, 파라미터 값 0개. [최우선-1] 준수.

**근거**: L591 §8 어휘 통일 표 (영구 금지: "priori derivation", "PASS_STRONG", "PRD Letter target" / 사용자 제약: 출판 시도 영구 금지) ↔ L577~L583 산출물 어휘 drift 점검.

---

## §1. L577~L583 어휘 위반 위치 표 (grep 실측)

| 산출물 | 라인 | 등장 어구 | 위반 카테고리 |
|---|---|---|---|
| L577/Q17_DYNAMIC.md | 15 | "PRD Letter 진입 조건: Q17 완전 달성 OR (Q13 + Q14 동시)" | PRD Letter target |
| L577/Q17_DYNAMIC.md | 60 | "§3. Q17 완성 시 PRD Letter 진입 시나리오" | PRD Letter target (헤더) |
| L577/Q17_DYNAMIC.md | 62 | "PRD Letter 진입조건: Q17 완전 달성 OR (Q13 + Q14 동시 달성)" | PRD Letter target |
| L577/Q17_DYNAMIC.md | 64 | "Q17 완성 단독: PRD Letter 진입 조건의 절반 (OR 의 첫 항) 충족" | PRD Letter target |
| L578/Q17_PATH3_RULE_A.md | 49 | "PRD Letter OR-조건 첫 항 (Q17 완전 달성) 충족 주장…" | PRD Letter target |
| L578/Q17_PATH3_RULE_A.md | 52 | "PRD Letter 가 OR 조건 첫 항 단독으로 받아들여진다는…" | PRD Letter target |
| L578/Q17_PATH3_RULE_A.md | 87 | "Q17 단독 달성으로 PRD Letter 진입 *조건 충족*…" | PRD Letter target |
| L578/Q17_PATH3_RULE_A.md | 94 | "§3. PRD Letter 차단 해제 평가 (정직)" | PRD Letter target (헤더) |
| L578/Q17_PATH3_RULE_A.md | 96 | "L577 §3 주장: Q17 완전 달성 단독으로 PRD Letter OR-조건…" | PRD Letter target |
| L578/Q17_PATH3_RULE_A.md | 106 | "OR 첫 항 충족 = 차단 해제의 비약: PRD Letter 진입 조건…" | PRD Letter target |
| L578/Q17_PATH3_RULE_A.md | 123 | "PRD Letter 강진입은 Q17+Q13+Q14 동시 달성 시점까지 보류" | PRD Letter target |
| L580/CROSS_IMPACT_Q13.md | 15 | "PRD Letter 진입조건: Q17 완전 달성 OR (Q13 + Q14 동시)" | PRD Letter target |
| L580/CROSS_IMPACT_Q13.md | 62 | "§4. PRD Letter 진입조건 갱신" | PRD Letter target (헤더) |
| L581/COMBINED_REVISED.md | 16 | "PRD Letter 진입조건: Q17 완전 달성 OR (Q13 + Q14 동시 달성)" | PRD Letter target |
| L581/COMBINED_REVISED.md | 89 | "§4. PRD Letter 진입조건 OR 양쪽 활성화 등급" | PRD Letter target (헤더) |
| L581/COMBINED_REVISED.md | 100 | "PRD Letter 강진입 (조건 양쪽 동시 충족) 시나리오는…" | PRD Letter target |
| L581/COMBINED_REVISED.md | 127 | "PRD Letter OR 양쪽 활성화 강함, hidden DOF 하한 −1" | PRD Letter target |
| L581/COMBINED_REVISED.md | 133 | "PRD Letter 진입 path 자체는 …" | PRD Letter target |
| L583/Q17_R3R4_PROTOCOL.md | 33-34 | "PRD Letter 진입 조건 재고 / PRD Letter 진입 조건이 더 멀어졌음" | PRD Letter target |
| L583/Q17_R3R4_PROTOCOL.md | 49-50 | "PASS_STRONG enum 영구 0 명시화" / "PASS_STRONG 인스턴스 0…" | PASS_STRONG (열거형 잔존 OK, 헤드라인은 위반) |
| L583/Q17_R3R4_PROTOCOL.md | 77 | "priori 도출 / derived a priori" — mass redef 종결로 도출 주장 근거 소멸 | priori derivation (단, *폐기* 맥락) |
| L583/Q17_R3R4_PROTOCOL.md | 93 | "PASS_STRONG enum 항을 유지하되 current_count: 0…" | PASS_STRONG (schema 잔존 OK) |
| L585/Q17_PATH5_A7.md | 41/48/72/80 | "글로벌 고점 회복 가능성" | priori 회복 어휘 (출판 무관 명시 필요) |

**소계**: 위반/주의 라인 23건 (L577: 4, L578: 7, L580: 2, L581: 5, L583: 5, L585: 4 — L585 는 priori 회복 톤).

**주의**: "first-principles" / "0 free parameter" 어구는 L577~L583 어디에도 직접 등장하지 않음 (grep 결과 0).

---

## §2. retroactive 정정 권고 매트릭스

| 위치 | 현재 어휘 | 권고 정정 *방향* (L591 §8 가이드) | 비고 |
|---|---|---|---|
| L577 §1 / §3 | "PRD Letter 진입 조건 (충족)" | "내부 의사결정 OR-조건 첫 항 (Q17 완전 달성)" 또는 "L6 게이트 OR-조건" | 출판 어휘 → 내부 게이트 어휘 |
| L578 §1-§3 | "PRD Letter 차단 해제 / OR 첫 항" | "내부 게이트 OR 첫 항 / 출판 시도 무관 정합성 조건" | "차단 해제" 어구 자체는 출판 무관 시 의미 잔존 — 단, paper-bound 어휘로 재해석 금지 명시 |
| L580 §4 | "PRD Letter 진입조건 갱신" | "내부 OR-게이트 갱신" 또는 "L6 진입조건 갱신" | 헤더 어휘 교체 |
| L581 §4 | "PRD Letter 진입조건 OR 양쪽 활성화 등급" | "내부 OR-게이트 양쪽 활성화 강도 등급" | 헤더 어휘 교체 |
| L583 §6 (lines 33-34) | "PRD Letter 진입 조건이 더 멀어졌음" | "내부 게이트 OR-조건 양쪽 모두 추가 박탈 (출판 시도 영구 금지 sync)" | conclusion §6 톤 수정 |
| L583 §3 (lines 49-50, 93) | "PASS_STRONG enum 영구 0 명시화" | enum 키 자체는 schema 호환 위해 유지, 단 *헤드라인* 사용 영구 금지 명시 + `current_count: 0` 영구 불변 주석 — L591 §8 와 일치. **헤더 어휘 자체 변경 불요** | 사실상 L591 ↔ L583 정합 |
| L583 §6 (line 77) | "priori 도출 / derived a priori" — 폐기 맥락 | 그대로 *폐기 맥락* 유지 (인용 형태). 단, paper 본문 0회 등장 sync 명시 필요 | 위반 아님, sync 보강 |
| L585 §3 | "글로벌 고점 회복 가능성" | "priori 회복 가능성 (출판 시도 무관, 내부 정합성 한정)" | 출판 무관 명시 필요 |
| L583 §4 | "falsifier 등록" / "사전등록 falsifier" | "출판 무관 plan 단계 falsifier (사전등록 - 내부 락인)" | 사전등록 자체는 plan 단계로 유지 — 출판과 분리 |

**규칙**: 어휘 영구 금지 4종 ("PRD Letter target", "priori derivation", "PASS_STRONG" 헤드라인, "first-principles") 중 L577~L583 에서 실제 발생은 **PRD Letter target** (18건) 이 압도적. 나머지 3종은 L583 의 schema/폐기 맥락 인용에 한정 — 본문 주장 어휘 아님.

---

## §3. sync protocol *방향*

**원칙**: 본 L596 산출물은 L577~L583 본문을 *직접 edit 하지 않는다*. (8인 Rule-A 의무 — 본 task 는 산출 *방향* 단일.)

### 옵션 A — 별도 erratum 디렉터리 권고 (선호)
- 경로: `results/L596_erratum/` (본 산출물과 분리)
- 내용: 위 §1 표를 그대로 옮기고, 각 라인별 "이 어구는 L591 §8 어휘 통일 가이드에 의해 *내부 게이트 / 출판 무관 plan / phenomenological match* 어휘로 재독해되어야 함" 1줄 cross-ref.
- 장점: 원본 무결성 유지, 인용 추적 가능, 8인 Rule-A 합의 후 단일 erratum 으로 일괄 처리.

### 옵션 B — L591 §8 cross-ref 만 추가
- 각 산출물 (L577~L583) 헤더에 L591 cross-ref 1줄 추가:
  - 예: `[L591 §8 어휘 가이드 적용: "PRD Letter target" 등 어휘는 출판 무관 *내부 게이트* 로 재독해]`
- 단점: 본문 직접 edit 1줄 발생 — 본 L596 task 범위 위반 (산출물 본문 edit 0건 약속).
- → **본 L596 산출 시점에서는 옵션 B 비채택**, 차기 8인 Rule-A 합의 후 별도 task 로 이관.

### 옵션 C — 어휘 매핑 표 + claims_status YAML 주석 (보강)
- `claims_status.yaml` 의 PASS_STRONG enum 에 `# L591 §8: 헤드라인 어휘 영구 금지, current_count=0 영구 고정` 주석.
- L583 §3 권고와 정합. enum 구조 무변경.

**권고**: 옵션 A 채택 + 옵션 C 보강. 옵션 B 는 8인 Rule-A 합의 후 별도 L597+ task.

---

## §4. CLAUDE.md 등록 권고 (8인 Rule-A 합의 사항)

L591 §8 어휘 가이드를 CLAUDE.md L569/L591 재발방지 섹션에 1줄 등록 *권고*:

> **L591 어휘 통일 (영구)**: 산출물 본문에서 "PRD Letter target" / "priori derivation" / "PASS_STRONG" 헤드라인 / "first-principles" / "0 free parameter" 어휘 사용 금지. PRD Letter 어구는 *내부 게이트* 또는 *L6 OR-조건* 으로, priori derivation 은 *phenomenological match* 로, PASS_STRONG 은 *PASS_MODERATE* 단일화로 대체. 출판 시도 영구 금지 sync. (L596 retroactive 점검: L577~L583 23건 위반/주의 위치 식별됨, erratum 별도 처리.)

**8인 Rule-A 의무**: 본 등록은 8인 검토 합의 후에만 CLAUDE.md 반영. 본 L596 산출물 단독으로 CLAUDE.md edit 금지.

---

## §5. 정직 한 줄

L577~L583 의 PRD Letter 어휘 18건은 L591 §8 어휘 통일 가이드가 등장하기 *전에* 작성된 산출물의 자연스러운 drift 이며 결과 자체를 무효화하지 않으나, "PRD Letter 진입조건" 어구를 *내부 OR-게이트* 로 일관 재독해해야 출판 시도 영구 금지 사용자 제약과 정합한다 — 본 L596 은 이 재독해 *방향* 만 제시하며 산출물 본문은 단 한 글자도 수정하지 않는다.
