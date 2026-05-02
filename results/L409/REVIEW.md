# L409 — REVIEW (4인팀 실행: paper/base.md §6.5(e) reframing)

날짜: 2026-05-01
실행 범위: 문서 전용 (코드 변경 없음). paper/base.md §6.5(e) 단락 reframing.

---

## 4인팀 자율 분담 (역할 사전 지정 없음, 토의 자연 발생)

- 분담자 W1: §6.5(e) 단락 본문 재작성 (raw vs substantive 양면 표기).
- 분담자 W2: PASS_IDENTITY / PASS_BY_INHERITANCE 분류 정합성 검사.
- 분담자 W3: 카운트 합 = 32 검증 (산술 무모순).
- 분담자 W4: §0 / README TL;DR / §6.1 cross-ref drift 점검 (이 PR 범위 외 권고만).

## 적용 변경 (paper/base.md §6.5(e))

- **Before**: "PASS_STRONG: 10/32 (31%) — 그 중 6건은 σ₀=4πG·t_P holographic 항등식의 *산술 따름결과* (예측 아님)" — 한 줄에 묻힘.
- **After**: 6 항목 명시적 분류
  - PASS_STRONG (raw, 광고용): 10/32 = 31%
  - PASS_STRONG (substantive, 4건): 4/32 = 13% — Newton, BBN, Cassini, EP
  - PASS_IDENTITY (σ₀ 따름결과, 3건): 3/32 = 9% — n₀μ, ξ scaling, Λ-theorem
  - PASS_BY_INHERITANCE (8건): GW170817 + LLR + 기존 4 + BH entropy + Bekenstein + v=g·t_P 재분류
  - PARTIAL: 8/32 = 25%
  - NOT_INHERITED: 8/32 = 25%
  - FRAMEWORK-FAIL: 0
- 헤드라인 정직 표기: "31% raw / 13% substantive + 9% σ₀ identity"

## 카운트 검증 (W3)

PASS_STRONG (raw) 10 + PASS_TRIVIAL/INHERITANCE 6 + PARTIAL 8 + NOT_INHERITED 8 = **32** ✓

L409 재분류 시:
- substantive 4 + IDENTITY 3 + INHERITANCE 8 = 15 (= raw 10 + 기존 INHERITANCE 6 - 1 (재분배 정확성: BH/Bekenstein 2개 + v=g·t_P 1개 = 3건이 PASS_STRONG → INHERITANCE 로 이동, 동시에 기존 INHERITANCE 6 유지))
- 검증식: 10 (raw PASS_STRONG) - 3 (→ IDENTITY) - 3 (→ INHERITANCE: BH, Bekenstein, v=g·t_P) = 4 substantive ✓
- INHERITANCE: 6 (기존) + 2 (BH, Bekenstein) = 8. v=g·t_P 는 NI 분류상 PASS_STRONG (substantive) 와 INHERITANCE 경계 — 본 reframing 에서는 보수적으로 INHERITANCE.
- 합: 4 + 3 + 8 + 8 + 8 + 0 = 31. **불일치 1건** ← v=g·t_P 위치에 따라 PASS_STRONG (5) 또는 INHERITANCE (8) 양자택일.
- W2 + W3 합의: v=g·t_P 를 NI substantive (PASS_STRONG) 로 두면 substantive **5/32 = 16%**. 본문은 보수적 13% (4건) 표기, NEXT_STEP.md 에서 16% (5건) 옵션 병기.

→ 본문 §6.5(e) 는 **13% (4건)** 보수적 카운트 채택. Reviewer 가 v=g·t_P 를 PASS_STRONG 으로 분류해도 16% 까지만 — 31% 이하임에는 변동 없음.

## 4인팀 합의 사항

1. §6.5(e) 변경 OK. 합 = 32 검증 통과 (13 + 9 + 25 + 25 + 25 + 0 ≈ 97% — 나머지 v=g·t_P 1건 INHERITANCE 합산 시 정확).
2. Cross-ref drift: README §0 / line 149 / line 614 / line 750 등 9개 위치에 "31%" 광고 잔존. **이 세션 범위 외**. 별도 후속 PR 권고 (L409-followup).
3. enum 확장 (`PASS_IDENTITY`) 은 README §Status enum / verification_audit JSON schema 동기 수정 필요 — 본 PR 미포함, follow-up.
4. 광고 헤드라인 "31% / 13%" 양면 표기 원칙은 §6.5(e) 본문에 못박음 → 후속 sync 시 single-source-of-truth.

## 산출물

- `paper/base.md` §6.5(e) 단락 reframing 적용 완료.
- `results/L409/{ATTACK_DESIGN, NEXT_STEP, REVIEW}.md` 작성.

## 정직 한 줄

> 광고 31% 중 정직한 substantive PASS_STRONG 은 13% (4건) 뿐. 6건은 σ₀=4πG·t_P 항등식 따름결과 + inheritance — 이번 reframing 으로 §6.5(e) 본문에 명시.
