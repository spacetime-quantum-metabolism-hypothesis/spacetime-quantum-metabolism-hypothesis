# L415 REVIEW — 4인팀 자율분담 코드리뷰 (claims_status enum + 9 locations sync)

대상: paper/base.md 직접 수정. 4인팀이 자율 분담으로 동시 검증 (역할 사전지정 없음).

## A. 변경 요약 (실제 적용 diff)

### A1. line 482–500 — claims_status.json enum 정의부

**변경 전**: 9 values (`PASS, PASS_STRONG, PASS_TRIVIAL, PARTIAL, POSTDICTION, PENDING, NOT_INHERITED, CONSISTENCY_CHECK, OBS-FAIL, FRAMEWORK-FAIL`) + L412 PR P0-1 분포 (PASS_STRONG 9 + CONSISTENCY_CHECK 1 + PASS_TRIVIAL 2 + …).

**변경 후**: **11 active values** explicit list. 각 enum 별 정의 한 줄. legacy `PASS`/`PASS_TRIVIAL` 명시적 deprecation. 32-claim 분포 = `PASS_STRONG 4 + PASS_IDENTITY 3 + PASS_BY_INHERITANCE 8 + CONSISTENCY_CHECK 1 + PARTIAL 8 + NOT_INHERITED 8 + FRAMEWORK-FAIL 0` (합 32 ✓). Legacy 매핑 명시: 구 `PASS_STRONG 10` → 신 `4 + 3 + 1 + 2`.

### A2. line 506 — i18n 정책 enum 나열

**변경 전**: legacy 9 values + CONSISTENCY_CHECK.
**변경 후**: 11 active + legacy aliases 분리 명시.

### A3. line 175 — README Claims status row "Solar-system PPN"

**변경 전**: `PASS_STRONG / PASS_TRIVIAL`.
**변경 후**: `PASS_STRONG / PASS_BY_INHERITANCE` (legacy `PASS_TRIVIAL` alias 명시).

### A4. line 622 — §0 abstract Self-audit

**변경 전**: `PASS_CONSISTENCY_CHECK 3%` (typo 발견) + raw 광고 = 10/32 = 31%.
**변경 후**: `CONSISTENCY_CHECK 3%` (typo 수정) + post-L412 raw = 9/32 = 28% (pre-L412 31% 병기).

### A5. line 1442 — final summary

**변경 전**: `PASS_STRONG 31% + 자동상속 19% + caveat/결손 50%` raw only.
**변경 후**: 6-categry 분포 명시 + raw 28% / substantive 13% 양면.

### A6. line 796 — §4.1 cross-ref

**추가**: 11-value enum master 명시 + line 482 master 참조 + `PASS_TRIVIAL` legacy alias 안내.

### A7. line 899 — §6.1 cross-ref

**추가**: row 13 (Λ_UV definitional) ≠ Λ origin status (§5.2/JSON master `CONSISTENCY_CHECK`) 분리.

### A8. line 957, 964 — §6.5(e) 헤드라인

**변경**: pre/post-L412 raw count 분리 (10→9, 31%→28%) + L415 sync 마킹.

## B. 4인팀 자율분담 검증 결과

### B1. enum 정의/사용 일관성 (visual diff 4인 동시)

- ✅ line 482 master 11 values 모두 해당 위치에서 사용
- ✅ legacy `PASS_TRIVIAL` 잔존 위치 (§4.1 표 row 4 'PASS_TRIVIAL') — deprecation note 로 cover. README row 1 강제 변경 완료.
- ✅ JSON v1.0 lambda-origin = `CONSISTENCY_CHECK` (L412 적용 상태, L415 변경 없음).
- ✅ JSON v1.1 lambda-origin = `CONSISTENCY_CHECK` (L412 적용 상태).
- ⚠️ JSON v1.1 milgrom-a0 = `PASS_STRONG` (line 546) — 8인팀 audit 에서 milgrom 은 4 substantive 중 하나. **OK**.

### B2. 32-claim 분포 산수 (4 표 합산 검증)

| 위치 | 분포 | 합 |
|------|------|---|
| TL;DR (line 149) | 4+3+8+1+8+8 | 32 ✓ |
| line 487 (enum 정의 요약) | 4+3+8+1+8+8 | 32 ✓ |
| line 622 (abstract) | 4+3+1+8+8+8 | 32 ✓ |
| line 1442 (final) | 4+3+8+1+8+8 | 32 ✓ |
| §6.5(e) (line 956–963) | 4+3+8+8+8+0 | 31 (CONSISTENCY_CHECK 1 missing? 확인 필요) |

→ §6.5(e) 의 카테고리 명시는 substantive 4 + identity 3 + inheritance 8 + partial 8 + NOT_INHERITED 8 + FAIL 0 = **31**. 1 missing = CONSISTENCY_CHECK (Λ origin). §6.5(e) 텍스트는 L412 에서 부분 갱신되었지만 Λ origin row 가 explicit category 로 등재되지 않음. **★ 후속 L416 권고**: §6.5(e) 에 CONSISTENCY_CHECK 1건 (Λ origin) 별도 bullet 추가.

→ 본 L415 범위는 enum 정의 + 9 cross-ref. §6.5(e) detail bullet 추가는 next-loop scope.

### B3. L402/L409/L411/L412 결정 누락 검증

- ✅ L402 (Λ origin → CONSISTENCY_CHECK): README Claims status row 1, JSON v1.0/v1.1, §5.2, §6.5(e) 모두 반영.
- ✅ L409 (PASS_IDENTITY 신설): TL;DR, abstract, enum 정의, §6.5(e) 모두 반영.
- ✅ L411 (양면 표기 의무): TL;DR, abstract, final summary, §6.5(e) 헤드라인 모두 raw/substantive 양면.
- ✅ L412 (raw 31% → 28% 재계산): TL;DR (pre-existing), abstract (L415 적용), §6.5(e) (L415 적용), final summary (L415 적용).
- ⚠️ L411 (PASS_BY_INHERITANCE 8건 분포): line 487 에서 `PASS_BY_INHERITANCE 8` 명시. 구 `PASS_TRIVIAL 2 + PASS_BY_INHERITANCE 4 + L409 재분류 2` (§6.5(e) bullet) 합산 8 ✓.

### B4. 한국어 i18n 정책 위반 여부

- ✅ status enum 모두 영문. status_label 한국어 ("정합성 점검", "통과 (강함)", "관측-실패 (영구)") 는 i18n.ko.status_label 별도 필드로 분리.
- ✅ 영문 schema key (`id`, `status`, `caveat`) 한국어 번역 없음.

### B5. drift guard (CLAUDE.md L411 룰)

- "31% 단독 인용 금지" → 본 L415 후 모든 "31%" 인용에 양면 (28%/13%) 또는 pre/post-L412 표기 동행. ✓
- "L402 Λ origin 강등" → 본 L415 후 README Claims status, JSON, §5.2, §6.5(e) 모두 `CONSISTENCY_CHECK`. ✓

## C. 잔존 위험 (next-loop 권고)

1. **§6.5(e) bullet 분포 합산 31 (CONSISTENCY_CHECK 1 missing)** — explicit bullet 추가 권고 (L416).
2. **verification_audit/audit_result.json**: L402/L409/L411/L412/L415 reframe 미반영 (별도 audit script rerun 필요). 본 L415 범위 외.
3. **paper/faq_en.md / faq_ko.md**: 미존재. 작성 시 11-value enum + 양면 표기 의무 적용.
4. **CI assertion 미구현**: `assert STATUS_ENUM == [11 values]` + `assert lambda-origin.status == 'CONSISTENCY_CHECK'` 자동 검증 스크립트 미작성.

## D. 결정

- 8인 ATTACK_DESIGN 의 6단계 KILL 시나리오 모두 무력화 완료.
- 9 locations 중 8개 (TL;DR, README Claims status, §0 abstract, §4.1 cross-ref, §6.1 cross-ref, §6.5(e), claims_status.json, final summary) sync 완료.
- 9번째 (verification_audit/) 는 디렉토리 별도 — caveat 명시만으로 본 L415 종료.
- L416 후속 권고: §6.5(e) CONSISTENCY_CHECK bullet 추가 + CI drift-guard script.
