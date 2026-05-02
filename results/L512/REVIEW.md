# L512 — RAR row 추가 to paper/base.md §4.1 PASS 표

날짜: 2026-05-01
작업자: SQMH (자동)

## 임무
paper/base.md §4.1 PASS 표 (4장 검증 완료 11행 canonical) 에 RAR row 12 추가 (PASS_MODERATE).

## 추가된 row (§4.1 끝, Bullet cluster row 다음)

| 예측 | 데이터 | 결과 | 종류 |
|------|------|------|------|
| **RAR a₀** | SPARC (M16) | a₀_RAR = 1.069×10⁻¹⁰ vs SQT 1.042×10⁻¹⁰ m/s² (2.5% 일치) | **PASS_MODERATE** — caveat 5개 (아래) |

## 등급 근거 (PASS_MODERATE — PASS_STRONG 아님)

중심값 일치는 2.5% 로 우수 (M16 RAR fit 의 a₀ vs SQT a₀ = c·H₀/(2π) 닫힌 예측). 그러나 **5개 caveat** 가 PASS_STRONG 으로의 격상을 막는다:

1. **L491 — cross-form spread 0.37 dex.** McGaugh 2016 (M16) functional form (`g_obs = g_bar / (1 - exp(-√(g_bar/a₀)))`) 외에 다른 검증된 functional form 들 (Lelli 2017, Chae 2020 등) 의 a₀ 추정값 spread 가 0.37 dex (factor ~2.3) 까지 벌어진다. **median form 의 0.023 dex 만 PASS**. 즉 form-choice 가 등급을 좌우 — robust universal a₀ 라기보다는 form-conditioned PASS.

2. **L492 — dwarf cross-dataset 불안정.** SPARC dwarf subset 에서 a₀ ≈ 0.46×10⁻¹⁰ m/s² 까지 내려가며 (~factor 2.3 deficit), LITTLE THINGS 등 cross-dataset 으로 옮기면 추정값 안정성 떨어짐. dwarf regime 은 SQT 의 σ₀ 변환 영역과 겹치므로 단순 universal-a₀ 해석 위험.

3. **L495 — hidden DOF 3.** M16 fit 자체에 (i) RAR functional form 파라미터, (ii) per-galaxy Υ★ (stellar M/L), (iii) H₀ anchor (a₀ = c·H₀/(2π) 변환) — 총 3 hidden DOF 가 들어간다. naive PASS 는 이를 무시한 카운트.

4. **L502 — hidden-DOF AICc.** L495 hidden DOF 3 에 대한 AICc penalty (2k + 2k(k+1)/(N-k-1)) 적용 시 **ΔAICc = +4.71** (LCDM/MOND/baseline 대비). raw χ² 는 우수하지만 정보 기준 적용 시 우열 없음 → **MODERATE** 강등이 정직.

5. **L493 + L494 — real signal 확정.** OOS retention 30% (L493 holdout) + 1000-mock null injection 에서 false-positive 0/1000 (L494) 로 통계적 진실성 확보. 즉 caveat 1–4 는 *signal 자체* 의 부재가 아니라 *equally good 대안 form/penalty* 문제. signal 자체는 real.

## 종합

> RAR a₀ ↔ SQT c·H₀/(2π) 일치는 **real signal 이지만 form-choice + hidden DOF 에 conditional**. 따라서 §4.1 에 PASS row 로 등재하되 종류는 **PASS_MODERATE** (PASS_STRONG 와 PARTIAL 사이) — caveat 5개를 명시적으로 expose.

## 산출물
- paper/base.md §4.1 표 row 12 추가 (Bullet 다음, §4.2 직전).
- results/L512/REVIEW.md (본 문서).

## 정직 한 줄
RAR a₀ 일치는 real signal 이지만 form-choice + hidden DOF 3 의 AICc penalty 까지 정직 노출하면 PASS_STRONG 이 아닌 PASS_MODERATE 가 옳다.
