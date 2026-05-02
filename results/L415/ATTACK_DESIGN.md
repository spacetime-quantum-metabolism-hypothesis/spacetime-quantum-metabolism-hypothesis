# L415 ATTACK_DESIGN — claims_status enum drift 공격 시나리오

세션: L415 (독립). 8인팀 cold-blooded attack design.
대상: paper/base.md 의 enum 정의 (line 478-506) + 9 cross-reference locations.
선행: L402 (Λ origin → CONSISTENCY_CHECK), L409 (PASS_IDENTITY 분리), L411 (재프레이밍).

## 8인팀 공격 (역할 사전지정 없음, 자율 분담)

### A1 — enum 정의/사용 불일치 (가장 치명)

**공격**: line 482 의 canonical enum 은 9 values (`PASS / PASS_STRONG / PASS_TRIVIAL / PARTIAL / POSTDICTION / PENDING / NOT_INHERITED / OBS-FAIL / FRAMEWORK-FAIL`) 인데, line 149 (TL;DR) 와 line 894 (§6.5e) 는 `PASS_IDENTITY` + `CONSISTENCY_CHECK` 를 *이미 사용*. enum 정의부 미갱신 → reviewer 가 "정의되지 않은 enum 사용" 으로 즉시 reject.

**증거 grep**:
- line 482: 9 values 명시
- line 149: `σ₀-identity 9% (3) + ... + CONSISTENCY_CHECK 3% (1)` 사용
- line 506: 다시 9 values 만 나열 (i18n 정책)
- line 897: `PASS_IDENTITY` 정의 사용

**심각도**: CRITICAL. JCAP/PRD reviewer 가 첫 5초에 잡는다.

### A2 — 헤드라인 산수 합 분포 불일치

**공격**: 32 claim 분포 합산이 위치마다 다름.
- line 149 (TL;DR): 13% + 9% + 25% + 3% + 25% + 25% = **100%** (4+3+8+1+8+8 = 32, OK)
- line 487 (legacy): PASS_STRONG 10 + PASS_TRIVIAL 2 + PASS_BY_INHERITANCE 4 + PARTIAL 8 + NOT_INHERITED 8 + FAIL 0 = **32 (OK)**, 그러나 PASS_IDENTITY/CONSISTENCY_CHECK 미반영
- line 614 (abstract): 31% PASS_STRONG (10) + 19% inherited (6) + 50% caveat/gap (16) + FAIL 0 = **32 (OK)**, 그러나 raw 카운팅
- line 1380 (final): "PASS_STRONG 31% + 자동상속 19% + caveat/결손 50%" — raw only, reframed 11-value 미반영

→ 4 표 모두 합은 32, 그러나 *카테고리 정의가 다름*. Reviewer "어느 표가 master 인가?" 질문에 답 없음.

**심각도**: HIGH.

### A3 — Headline 31% vs substantive 13% 양면 표기 불일치

**공격**: line 149 는 양면 명시. line 614 (abstract) 와 line 1380 (final summary) 는 "31%" 단독. CLAUDE.md 자체에 "31% 단독 인용 금지" 등재되어 있음 (L409 ATTACK_DESIGN A1·A4·A7 회피 룰). **자기-위반**.

**심각도**: CRITICAL — reviewer 가 §0 abstract 부터 보면 "31% PASS_STRONG" 만 보임 → over-claim.

### A4 — Λ origin 강등 미반영 (§4.1 표 + Claims status)

**공격**: line 171 README Claims status 첫 줄: `Λ origin | ✅ PASS_STRONG | ρ_q/ρ_Λ = 1.0000 ...`. L402 결정 (PASS_STRONG → CONSISTENCY_CHECK) 미반영. line 837 의 row 13 cross-ref 도 "Λ origin caveat" 만 적고 enum 변경 없음. line 857 §6.1.1 row 13 은 "Λ_UV definitional, RG-유도 아님" 으로 row 정의 자체가 다름 (L402 강등 대상은 line 171 의 Λ origin 자체, row 13 Λ_UV 와 다름).

**심각도**: HIGH — L402 결정이 9 location 중 §4.1+README+abstract 3곳에서 누락.

### A5 — claims_status.json 예시의 status 갱신 누락

**공격**: line 494: `{"id": "lambda-origin", "status": "PASS"}` — L402 후 `CONSISTENCY_CHECK` 이어야 함. line 519: v1.1 예시도 `"status": "PASS_STRONG"` 그대로.

**심각도**: HIGH — JSON 이 바로 machine-readable 진위. reviewer 자동 검증 즉시 fail.

### A6 — verification_audit/ 디렉토리 미동기

**공격**: paper/verification_audit/audit_result.json 이 9-value enum 시대 산물. L402/L409/L411 reframe 미반영. README 에서 "raw evidence in paper/verification_audit/" 링크 → reviewer 클릭 시 outdated.

**심각도**: MEDIUM — 본 L415 범위 외 (별도 audit script rerun 필요), 그러나 *링크 깨짐 caveat* 본문 명시 필수.

### A7 — FAQ 동기화 미확인

**공격**: paper/faq_en.md / faq_ko.md 가 32-claim 분포 인용한다면 enum 갱신 필요. 본 세션 grep 으로 확인.

**심각도**: MEDIUM — 일반인 대상 문서이므로 raw 31% 만 적혀 있을 가능성.

### A8 — 헤드라인 percent 의 분모 합계 검증

**공격**: 13% + 9% + 25% + 3% + 25% + 25% = **100%** (정확). 그러나 underlying 카운트 (4+3+8+1+8+8=32) 가 line 487 (10+2+4+8+8 = 32) 와 *다른 cell partition*. line 487 의 PASS_STRONG 10 = 4 (substantive) + 3 (PASS_IDENTITY) + 2 (PASS_TRIVIAL — Lagrangian-form/LLR) + 1 (Λ origin → CONSISTENCY_CHECK) ?? 합이 4+3+2+1 = 10 (OK). 즉 *재분류* 결과는 일관되나 line 487 표기가 legacy.

**심각도**: HIGH — 분포가 두 카운팅 시스템 사이에서 일관되지만 본문에 *명시 적분* 없음. Reviewer 가 "어떻게 10 → 4+3+2+1" 인지 못 따라옴.

## 종합 KILL 시나리오

reviewer 가 다음 순서로 공격하면 paper 즉사:

1. **§0 abstract 읽기 → "31% strong-pass"** (line 614) 발견 → over-claim 의심.
2. **claims_status.json 정의부 (line 482) 읽기 → 9 values 만 정의됨**.
3. **§6.5(e) 읽기 → PASS_IDENTITY/CONSISTENCY_CHECK 사용** → 정의되지 않은 enum.
4. **README Claims status (line 171) 첫 줄 Λ origin = PASS_STRONG** → L402 reframe 미반영.
5. **JSON 예시 line 494 status="PASS" → 자동 검증 fail**.
6. **결론**: "이 paper 는 자기 enum 도 일관되지 않음. 산술/논리 점검 부실." → desk reject.

→ 본 L415 임무: 위 6단계 KILL 모두 무력화. 11-value canonical enum + 9 location sync.
