# L415 NEXT_STEP — 11-value canonical enum + 9 locations sync

8인팀 자율 분담 결과 (NEXT_STEP). 코드리뷰 단계는 4인팀 (REVIEW.md).

## 1. Canonical 11-value enum (확정안)

기존 9 + 신설 2 = **11 values**. 모두 영문 고정, 한국어는 i18n object 만 별도.

| # | enum | 의미 | 32-claim count |
|---|------|------|----------------|
| 1 | `PASS_STRONG` | substantive falsifiable prediction (additional axiom 입력 필요) | 4 (13%) |
| 2 | `PASS_IDENTITY` | σ₀=4πG·t_P 산술 따름결과 (자유도 0, 차원 분석) | 3 (9%) |
| 3 | `PASS_BY_INHERITANCE` | 구 PASS_TRIVIAL + 외부 prior knowledge 상속 | 8 (25%) |
| 4 | `PASS_TRIVIAL` | (legacy alias of `PASS_BY_INHERITANCE`, v1.1 deprecate) | — |
| 5 | `PASS` | (generic, legacy — 신규 항목에서 사용 금지) | — |
| 6 | `CONSISTENCY_CHECK` | order-unity dimensional match, 동역학적 도출 아님 (Λ origin) | 1 (3%) |
| 7 | `PARTIAL` | caveat 명시 — 함수형/관측 채널 부분 검증 | 8 (25%) |
| 8 | `POSTDICTION` | 데이터 fit 후 명명, a priori 도출 아님 | (별도 §6.2) |
| 9 | `PENDING` | falsifier 미도래 (DESI DR3 등) | (별도 §4.3) |
| 10 | `NOT_INHERITED` | paper framework 외부 — 미상속 8건 | 8 (25%) |
| 11 | `OBS-FAIL` | observational tension (S_8 등), framework 내부 모순 아님 | (§6.1.1 #1 별도) |
| 12 | `FRAMEWORK-FAIL` | paper 내부 logical/mathematical 모순 (currently 0) | 0 |

**32-claim 분포 합산**: 4 + 3 + 8 + 1 + 8 + 8 = **32** ✓ (PASS_STRONG + PASS_IDENTITY + PASS_BY_INHERITANCE + CONSISTENCY_CHECK + PARTIAL + NOT_INHERITED).

**legacy 매핑**: 구 line 487 의 `PASS_STRONG 10` = 신 `PASS_STRONG 4 (substantive) + PASS_IDENTITY 3 + CONSISTENCY_CHECK 1 + PASS_BY_INHERITANCE 2 (구 PASS_TRIVIAL — GW170817 Lagrangian, LLR 동어반복)`. 합 4+3+1+2=10 ✓.

→ `PASS_BY_INHERITANCE` 8 = 구 (`PASS_TRIVIAL 2 + PASS_BY_INHERITANCE 4`) + L409 재분류 2 (BH entropy, Bekenstein bound) = 8 ✓.

총 12 entries (중 `PASS`, `PASS_TRIVIAL` 은 legacy alias, 신규 사용 금지). 활성 11 + legacy 1 (`PASS_TRIVIAL` deprecate-alias).

## 2. 9 locations cross-reference 동기화 절차

| # | location | line | 현 상태 | 갱신 |
|---|----------|------|---------|------|
| L1 | TL;DR self-audit bullet | 149 | OK (이미 11-value) | — |
| L2 | README Claims status legend (table) | 167–180 | Λ origin = PASS_STRONG (구) | row 1 강등 → CONSISTENCY_CHECK |
| L3 | §4.1 cross-ref + 11행 PASS 표 | 750–763 | enum 표기 OK 하나 row 1 (σ₀ regime) 미명시 | 메모만 추가 |
| L4 | §6.1 cross-ref + 22행 표 | 837–873 | row 13 (Λ_UV definitional) 와 Λ origin 별도 — OK | 별도 §5.2 stmt 동기화 필요 |
| L5 | §6.5(e) | 894–902 | OK (이미 11-value) | — |
| L6 | claims_status.json enum 정의 (v1.0+v1.1) | 482–506, 494, 519 | 9-value 만 정의 + JSON status="PASS" | 11-value 확장 + JSON status="CONSISTENCY_CHECK" |
| L7 | verification_audit/ link mention | 149, 614 | 외부 디렉토리 (script rerun 별도) | "L402/409/411 reframe pending" caveat 명시 |
| L8 | FAQ EN/KO | (faq_en.md, faq_ko.md) | grep 후 갱신 | 별도 — 본 base.md 범위 외 |
| L9 | §0 abstract Self-audit + final summary | 614, 1380 | "31% PASS_STRONG" 단독 (CLAUDE.md 위반) | 양면 표기 (raw 31% / substantive 13% + identity 9%) 강제 |

**드리프트 가드 룰**:
- (G1) 모든 enum 정의는 line 482 master 만 참조. 다른 곳에서 재정의 금지.
- (G2) "31%" 인용 시 "13% substantive + 9% identity" 양면 동시 표기 필수.
- (G3) Λ origin 등급은 master = §5.2 + claims_status.json. 다른 모든 표는 master 따른다.
- (G4) JSON 예시는 v1.0 (legacy) + v1.1 (신규) 동시 게시. v1.1 master, v1.0 deprecation 표시.

## 3. 4인팀 코드리뷰 분담 (자율, 사전지정 없음)

본 NEXT_STEP 의 9 location 갱신을 4인팀이 자율 분담으로 동시 검증:
- enum 정의부 (L1, L5, L6) — 4인 모두 visual diff
- 한국어 표기 일관성 — i18n 정책 위반 없는지 (status 영문 고정)
- 32-claim 분포 합산 산수 — 4 표 모두 합이 32 인지
- L402/L409/L411 결정 누락 여부 — Λ origin 강등이 모든 location 에 반영되었는지
