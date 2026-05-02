# L516 — claims_status.json 13-value enum + L502/L495 격하 동기화

> **작성**: 2026-05-01
> **저자**: 단일 분석 에이전트 (bookkeeping sync — 이론 도출 / 새 수식 0).
> **대상**: `claims_status.json` (v1.1 → v1.2)
> **CLAUDE.md 정합성**: 신규 물리식 0줄, 신규 파라미터 0개. enum 확장 + 격하 사후동기화 한정.

---

## 0. 정직 한 줄

**L495 hidden DOF 감사 (k_h = 9 보수 ~ 13 확장) + L502 AICc 정직 검증 (k_h_applicable ∈ {1,2}) 결과: PASS_STRONG 4 (Newton/BBN/Cassini/EP) 가 모두 ΔAICc_honest ∈ [+2, +4] 로 강등 사유. L482 RAR 도 +4.707 로 PASS_STRONG 후보 자격 상실. Bullet 은 L509 cross-sample 4/4 (Abell 520 충돌) 로 PASS_QUALITATIVE 정착. 본 sync 후 PASS_STRONG = 0/33, PASS_MODERATE = 5, PASS_QUALITATIVE = 1, PASS_IDENTITY = 3, PASS_BY_INHERITANCE = 8, CONSISTENCY_CHECK = 1, PARTIAL = 7, NOT_INHERITED = 8 → 합 33 ✓.**

---

## 1. enum 확장 (11 → 13 active values)

기존 10 active + `OPEN_PROVISIONAL` (L516 신설) + `PASS_MODERATE` + `PASS_QUALITATIVE` = **13 active**.

| 신규 grade | 정의 | 부여 기준 |
|---|---|---|
| **PASS_MODERATE** | bare bound 통과 + ΔAICc_honest ∈ [+2, +6] (k_h_applicable 부과) | 5 행 (Newton, BBN, Cassini, EP, RAR-a₀) |
| **PASS_QUALITATIVE** | 정성 진술 PASS, magnitude 비도출 | 1 행 (Bullet cluster) |
| **OPEN_PROVISIONAL** | 채널 특이적 PASS 인데 cross-channel audit 한 곳 이상에서 FAIL — 현재 부여 없음 (예약) | 0 행 |

`status_enum_legacy_deprecated` 는 `PASS`, `PASS_TRIVIAL` 그대로 유지.

## 2. PASS_STRONG → PASS_MODERATE 강등 (4건 + RAR 신규)

L502 §2 표 직접 인용:

| Claim | k_h_applicable | ΔAICc_honest | hidden DOF |
|---|---|---|---|
| `newton-recovery` | 2 | +4.0 | B1 ansatz, σ₀ amplitude scale |
| `bbn-deltaNeff` | 1 | +2.0 | η_Z₂ ≈ 10 MeV stipulation |
| `cassini-ppn` | 1 | +2.0 | Λ_UV stipulation |
| `ep-eta` | 1 | +2.0 | dark-only embedding |
| `rar-a0-milgrom` (신규) | 2 | +4.707 | M16 functional + Υ⋆ convention |
| `bullet-cluster` | 2 | +4.0 | B1 ansatz + scale → **PASS_QUALITATIVE** (L509 4/4 cross-sample, Abell 520 직접 충돌) |

→ JSON 의 `L516_demotion_log` object 에 row 단위 명시. 각 claim 의 `caveat` 필드에 ΔAICc + hidden DOF + cross-channel audit (L506/L508/L509) 사유 직접 기록.

## 3. claims 행 추가: `rar-a0-milgrom` (신규)

기존 32 → 33. L482 RAR 결과는 그동안 paper 본문에 PASS_STRONG candidate 로 등장했지만 `claims_status.json` 에 *행이 없었음* — drift. 본 L516 에서 명시적으로 추가:

- status: `PASS_MODERATE`
- cross-channel: L491 (functional-form 0.37 dex), L492 (subset K_X1·K_X2·K_X3 FAIL), L493 (OOS chi²/dof = 1.283 PASS), L494 (false-positive 0/200 → real), L503 (per-galaxy universality FAIL).

## 4. limitations 22 → 27 (5행 신규)

| 신규 # | id | 출처 | 핵심 |
|---|---|---|---|
| L23 | `L23-hidden-DOF-zero-param-overclaim` | L495 | "0 free parameter" 광고가 abstract / intro / appendix / discussion 에 drift; 보수 9, 확장 13 hidden DOF |
| L24 | `L24-AICc-honest-no-PASS_STRONG-survives` | L502 | k_h_applicable ∈ {1,2} 부과 시 PASS_STRONG 0/33 |
| L25 | `L25-N_eff-falsifier-channel-correlation` | L498 | 6 사전등록 falsifier 가 N_eff ≈ 4 (Euclid×LSST WL ρ=0.80, DESI×Euclid BAO ρ=0.54). Bonferroni α=0.01 |
| L26 | `L26-RAR-a0-NOT-universal` | L491/L492/L503 | per-galaxy intrinsic spread 0.427 dex; K_X 1/4 PASS; environment FAIL — aggregate 한정 일치 |
| L27 | `L27-Cassini-channel-conditional` | L506 | 8 channel 중 7 PASS, channel 3 (universal_phase3 β=0.107) FAIL — channel-conditional |

## 5. self_audit_distribution 갱신

```
이전 (v1.1, L411 reframed):  PASS_STRONG 4 + PASS_IDENTITY 3 + PASS_BY_INHERITANCE 8
                              + CONSISTENCY_CHECK 1 + PARTIAL 8 + NOT_INHERITED 8 = 32
이후 (v1.2, L516 sync):      PASS_STRONG 0 + PASS_MODERATE 5 + PASS_QUALITATIVE 1
                              + PASS_IDENTITY 3 + PASS_BY_INHERITANCE 8
                              + CONSISTENCY_CHECK 1 + PARTIAL 7 + NOT_INHERITED 8 = 33
```

증가 +1 = `rar-a0-milgrom` 신규 행. PARTIAL 8→7 = `bullet-cluster` 가 PARTIAL → PASS_QUALITATIVE 로 이동 (이전 v1.1 에서 PARTIAL 카테고리에 있었음).

substantive PASS_STRONG = 0/33 = **0%** (이전 13%). PASS_combined (MODERATE + QUALITATIVE) = 6/33 = **18%**.

## 6. CLAUDE.md 최우선-1 / 최우선-2 정합성

본 L516 작업은:
- 신규 물리 수식 0 줄 (enum extension + bookkeeping 한정)
- 신규 파라미터 0 개 (모든 ΔAICc 값은 L502 결과 직접 인용)
- 이론 도출 0 (L495 / L502 / L491–L494 / L498 / L503 / L506–L509 의 *기존* 결과 sync 만)

→ 최우선-1, 최우선-2 위반 없음.

## 7. 후속 의무 (별도 loop)

- abstract / 01_introduction / 10_appendix_alt20 / 08_discussion §8.4 / l5_A12_interpretation 의 "zero free parameter" 광고를 L495 정직 카운트 (9~13) 또는 paper/TABLES.md row 1 (5 free params Branch B) 와 일치시키도록 sweep — limitation L23 의 `future_plan`.
- README.md / README.ko.md "Claims status" summary 의 PASS_STRONG 카운트 표시 업데이트 — `last_synced_loop = "L516"` 문자열로 신호.
- paper/base.md §6.5(e) 32-claim 표 자체 텍스트는 본 sync 가 *건드리지 않음* (별도 loop). v1.2 enum 13-value 도입 사실은 §claims_status.json 에 L516 라인 추가 필요.

---

## 정직 한 줄 (재서)

**PASS_STRONG 4건 (Newton/BBN/Cassini/EP) 은 hidden-DOF 정직 카운트 + AICc 페널티 부과 후 *모두* PASS_MODERATE 로 강등; Bullet 은 PASS_QUALITATIVE; L482 RAR 신규 PASS_MODERATE 추가; PASS_STRONG = 0/33.**
