# L412 — NEXT_STEP (8인팀 reword path 3 후보 비교)

세션 일자: 2026-05-01
선행: L402 (회피 불가능 확정), L411 (REVIEW placeholder), L412
ATTACK_DESIGN (강등 미적용 시 8 attack 면).
원칙: CLAUDE.md [최우선-1, 2] — 수식 변경 없음. 광고 등급/명칭만 재작성.

---

## 0. 결정 변수 정의

- 변경 대상: paper/base.md §5.2 + abstract (§0) + 1.2.1 + derived 4 + 2.5
  table + §0 TL;DR (README block) + claims_status table + verifier 광고
  + Self-audit headline (32 claim 분포).
- 변경 *불가* 대상: §5.2 본문의 수식, n_∞ 정의식, axiom 3 균형식 — 8인
  팀이 자율 도출한 부분이라 수정 시 [최우선-2] 위반.

## 1. Path 3 후보

### Path (i) — 직접 강등 (PASS_STRONG → CONSISTENCY_CHECK)

- claims_status enum 한 줄 변경: `Λ origin ✅ PASS_STRONG` →
  `Λ origin ⚠️ CONSISTENCY_CHECK`.
- abstract 1번 bullet 동기화.
- TL;DR 첫 ✅ → ⚠️.
- Pro: 최소 침습. 8 attack 면 중 7개 (B1–B3, B5–B8) 동시 무력화.
- Con: 새 enum (`CONSISTENCY_CHECK`) 추가 — 기존 enum 표 (§4.1
  description, line 449/483/506) 6 곳 동시 sync 필요. 누락 시 silent
  drift.

### Path (ii) — "dimensional consistency check" 명칭만 사용

- enum 은 기존 PARTIAL 또는 PASS_TRIVIAL 에 흡수 (새 enum 불필요).
- 본문 명칭만 `dimensional consistency check (not a prediction)` 으로
  재서술.
- Pro: enum 표 변경 0. 자동화 안정.
- Con: PASS_TRIVIAL/PARTIAL 어느 쪽을 선택해도 의미 부정확. PASS_TRIVIAL
  은 "Lagrangian-form choice" 등 다른 사례와 혼동, PARTIAL 은 "부분
  통과" 함의로 circularity 본질을 가린다. 8 attack 면 중 B6 (enum)
  은 회피되나 B1·B2 (광고-본문 불일치) 는 의미가 약해 잔존.

### Path (iii) — 등급 분리 + 본문 circularity 강화 hybrid

- claims_status enum 새로 신설 (`CONSISTENCY_CHECK`) — Path (i) 와 동일.
- *추가로* §5.2 본문에 "L402 audit 결과 회피 불가능 확정 (Path-α
  10⁶⁰ 어긋남)" 한 문장 명시. abstract 도 "circularity is structural
  in the current axiom 3" 한 줄.
- Pro: B1–B8 모두 동시 무력화 + L402 audit 자체를 *공개 disclosure*
  로 전환 (B2 의 "self-aware circularity" 무기화 → 정직 disclosure 로
  반전).
- Con: 본문 길이 증가 (~3 lines). enum 표 변경 6 곳 + 본문 1 곳 +
  abstract 1 곳 동시 sync 필요.

## 2. 8인팀 합의 (요약)

- P1·P3·P7: Path (iii) 권고. "광고와 본문 일치 + L402 audit 정직
  disclosure" 가 referee 정직성 평가에서 net positive.
- P2·P5·P6: Path (i) 만으로도 attack 면 7/8 무력화 충족 — 침습 최소화
  관점에서 (i) 도 acceptable.
- P4·P8: (ii) 비추천 — enum 흡수가 의미 손실, "consistency check" 명칭
  은 (i)/(iii) 양쪽에 모두 포함되므로 단독 선택 의미 없음.

**합의**: Path (iii) 채택. (i) 의 enum 변경 + (ii) 의 명칭 재서술 +
L402 audit disclosure 한 문장 = hybrid.

## 3. 실행 sync 대상 (4인팀 실행 단계 입력)

paper/base.md 내 변경 위치 (행 번호 L402 시점 기준):

| 위치 | 현재 표기 | 변경 후 |
|------|----------|---------|
| L143 (TL;DR) | `✅ ρ_q/ρ_Λ(Planck) = 1.0000 (dimensional consistency, with circularity caveat)` | `⚠️ ρ_q/ρ_Λ(Planck) = order-unity (CONSISTENCY_CHECK; circularity structural — see §5.2)` |
| L149 (Self-audit headline) | `PASS_STRONG 10` 카운트 | `PASS_STRONG 9 + CONSISTENCY_CHECK 1` (이미 part 적용된 line 149 의 분포 표기 정확화) |
| L156 (Quickstart) | `verify_lambda_origin.py # Λ origin (1.0000 match)` | `verify_lambda_origin.py # Λ origin dimensional consistency check (circular w.r.t. ρ_Λ_obs)` |
| L171 (claims_status) | `Λ origin ✅ PASS_STRONG ρ_q/ρ_Λ = 1.0000 match` | `Λ origin ⚠️ CONSISTENCY_CHECK ρ_q/ρ_Λ order-unity match` |
| L494 (claims_status.json sample) | `"status": "PASS"` | `"status": "CONSISTENCY_CHECK"` |
| L519 (R-block sample) | `"status": "PASS_STRONG"` | `"status": "CONSISTENCY_CHECK"` |
| L607 (§0 abstract bullet 1) | `ρ_q/ρ_Λ(Planck) = 1.0000 (단, 5.2 절 circularity caveat 참조)` | `ρ_q/ρ_Λ(Planck) order-unity 일치 — *consistency check* (circularity 구조적, L402 audit 확정)` |
| L614 (Self-audit 분포) | `31% strong-pass (10/32, PASS_STRONG)` | `28% strong-pass (9/32, PASS_STRONG) + 3% CONSISTENCY_CHECK (1/32, Λ origin)` |
| L627 (1.2.1) | `SQT: 도출 (output) — 단, 5.2 circularity caveat 적용` | `SQT: order-unity dimensional consistency (circularity 구조적; 진정 a priori 도출 미달)` |
| L676 (derived 4) | `Λ = nε/c² → ρ_Λ ★ 5.2 circularity caveat 필수` | `Λ = nε/c² → ρ_Λ ★ CONSISTENCY_CHECK only (5.2 circularity 구조적)` |
| L808–810 (§5.2 본문) | `★★ Λ 기원 — circularity 정직 disclosure (★ 가장 중요)` | 명칭 변경 + L402 audit 결과 한 문장 추가 |
| L483, L506 (enum 표) | `PASS_STRONG, PASS_TRIVIAL, ...` 목록 | `CONSISTENCY_CHECK` 추가 |
| L449 (emoji↔enum) | mapping 표 | `⚠️ ↔ ... CONSISTENCY_CHECK` 추가 |

추가 sync (paper 외부):
- README.md (project root): §5.2 광고 미포함 — *변경 없음* 확인됨 (L412 검토).
- README.ko.md: 존재 시 L143/L149 mirror sync 필요 — 없으면 skip.

## 4. 위험 / mitigation

- 새 enum `CONSISTENCY_CHECK` 추가 → claims_status.json schema 변경.
  schema validator 실행 필수. (4인팀 실행 단계에서 grep 으로 enum 표
  6 곳 동시 update 확인.)
- "31% raw" 광고 표기 변화 → L411 의 "양면 표기 의무" 와 충돌 안 함
  (raw 31% 자체는 PASS_STRONG 10 + 강등 후 9 + CONSISTENCY_CHECK 1 =
  여전히 10 명목, 그러나 substantive 13% 는 unchanged). 분포 식만 수정.

## 5. 결정

**Path (iii) 채택, 4인팀 실행 단계 진입.**
