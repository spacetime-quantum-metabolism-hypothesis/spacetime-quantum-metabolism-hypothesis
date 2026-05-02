# L635 Erratum 디렉터리 — README

## 목적

본 디렉터리는 **L577~L585 산출물의 어휘 drift retroactive sync 자료**이다.
L596 (`results/L596/VOCABULARY_SYNC.md`) §3 옵션 A 권고 — "별도 erratum 디렉터리" — 의 직접 실행 결과.

## 원칙

- **원 산출물 본문은 무수정.** L577/L578/L580/L581/L583/L585 의 본문 라인 단 한 글자도 edit 하지 않는다.
- **본 erratum 만 추가.** 어휘 매핑 표 + 라인별 cross-ref 형태.
- **수식 0줄, 파라미터 값 0개.** [최우선-1] 준수. 어휘 정정 사실 그대로 기록.
- **단일 에이전트 결정 금지.** 본 erratum 은 *8인 Rule-A 합의 입력 자료*. 실제 본문 sync 또는 CLAUDE.md 등록은 8인 합의 후에만 진행.

## 파일 구성

- `erratum.md` — 메인 어휘 매핑 표 (L596 §1~§2 정정 권고 23건 정리)
- `L577_erratum.md` — L577/Q17_DYNAMIC.md 위반 4건 라인별 정정 매핑
- `L578_erratum.md` — L578/Q17_PATH3_RULE_A.md 위반 7건 라인별 정정 매핑
- `L580_erratum.md` — L580/CROSS_IMPACT_Q13.md 위반 2건 라인별 정정 매핑
- `L581_erratum.md` — L581/COMBINED_REVISED.md 위반 5건 라인별 정정 매핑
- `L583_erratum.md` — L583/Q17_R3R4_PROTOCOL.md 위반/주의 5건 라인별 정정 매핑
- `L585_erratum.md` — L585/Q17_PATH5_A7.md 주의 4건 라인별 정정 매핑

## Cross-reference

- **L591 §8 어휘 가이드**: `results/L591/PAPER_HONEST_REFRAMING.md` §8.
  영구 금지 어휘 4종 ("PRD Letter target" / "priori derivation" / "PASS_STRONG" 헤드라인 / "first-principles" / "0 free parameter").
- **L596 권고**: `results/L596/VOCABULARY_SYNC.md` §1 (위반 표) + §2 (정정 매트릭스) + §3 옵션 A.
- **L597 의사결정 항목 #6**: `results/L597/FINAL_RECOMMENDATION_v2.md` — 어휘 sync 항목 sync.

## 재독해 규칙 요약

| 원 어휘 (paper-bound) | 재독해 어휘 (내부 / phenomenological) |
|---|---|
| PRD Letter 진입 조건 | 내부 의사결정 OR-게이트 / L6 OR-조건 |
| PRD Letter 차단 해제 | 내부 게이트 OR 첫 항 충족 (출판 무관) |
| PASS_STRONG (헤드라인) | PASS_MODERATE 단일화 (enum 키는 schema 호환을 위해 유지, current_count=0 영구 고정) |
| priori derivation / a priori 도출 | phenomenological match (출판 시도 영구 금지 sync) |
| 글로벌 고점 회복 | priori 회복 가능성 (출판 시도 무관, 내부 정합성 한정) |
| first-principles / 0 free parameter | (L577~L585 본문 0회 등장 — 위반 없음, sync 불필요) |

## 다음 단계 (8인 Rule-A 합의 사항)

1. 본 erratum 디렉터리 8인 검토.
2. 합의 후 옵션 B (각 산출물 헤더에 L591 cross-ref 1줄 추가) 채택 여부 결정.
3. CLAUDE.md L569/L591 재발방지 섹션에 어휘 가이드 등록 여부 결정 (L596 §4).
4. claims_status.yaml PASS_STRONG enum 주석 보강 (L596 §3 옵션 C).

## 정직 한 줄

본 L635 erratum 은 L577~L585 의 PRD Letter 어휘 18건 + PASS_STRONG/priori 주의 5건 = 23건의 *재독해 방향* 만 명시한다. 원 산출물 본문은 무수정이며, 결과 자체의 물리적 결론은 영향받지 않는다 — 어휘 통일은 출판 시도 영구 금지 사용자 제약과의 정합성 확보 목적이다.
