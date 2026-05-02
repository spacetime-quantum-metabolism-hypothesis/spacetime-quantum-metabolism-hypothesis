# L637 — paper/verification/ 7 스크립트 실제 실행 + claim 검증

- 실행 일시: 2026-05-02
- 실행 환경: macOS, python3 (project default)
- 대상: paper/verification/verify_*.py × 7
- raw stdout: `results/L637/raw_stdout.txt`
- 비교 기준 1: `paper/verification/expected_outputs/*.json`
- 비교 기준 2: `results/L634/PAPER_PLAN_V3.md` §5 (vocabulary-only, 수치 비포함이 의도)

---

## §1 7 스크립트 별 실행 결과 (stdout 핵심줄)

| # | 스크립트 | exit | 핵심 출력 |
|---|----------|------|-----------|
| 1 | verify_milgrom_a0.py | 0 | `a_0(SQT)=1.129e-10 m/s^2`, `a_0(obs)=1.200e-10±1e-11`, `dev=0.71σ`, `PASS` |
| 2 | verify_lambda_origin.py | 0 | `rho_q=6.855508e-27`, `rho_Lambda=6.855508e-27`, `ratio=1.000000`, `STATUS: CONSISTENCY_CHECK` |
| 3 | verify_Q_parameter.py | 0 | `accuracy=100.0% (15/15)`, `log10(tau*)=16.974`, `tau*=9.422e+16`, `span=191.8 dec`, `STATUS: PARTIAL` |
| 4 | verify_S8_forecast.py | 0 | `S8 LCDM=0.8320`, `shift=+0.0114(+1.14%)`, DES_Y3 0.63σ INVISIBLE / LSST 2.85σ MARGINAL / Euclid 4.38σ DETECT |
| 5 | verify_cosmic_shear.py | 0 | `S8 LCDM=0.8320`, `S8 SQT=0.8415(+1.14%)`, `xi+ shift=+2.29%` |
| 6 | verify_monotonic_rejection.py | 0 | `chi2_mono=147.62`, `chi2_V=0.00`, `Δchi2=147.62 (~12.1σ)` |
| 7 | verify_mock_false_detection.py | 0 | `false-detection rate=100.0%` (CAVEAT 표시) |

전 7건 exit 0. 실행 실패 없음.

---

## §2 expected_outputs JSON cross-check

| 스크립트 | 기대값 키 | 기대값 | 실측값 | 일치? |
|----------|-----------|--------|--------|-------|
| milgrom_a0 | a0_SQT | 1.129e-10 | 1.129e-10 | OK |
| milgrom_a0 | deviation_sigma | 0.71 | 0.71 | OK |
| milgrom_a0 | verdict | PASS | PASS | OK (단, JSON `classification`은 `PASS_STRONG` — §4 mismatch 항 참조) |
| lambda_origin | rho_q | 6.855508e-27 | 6.855508e-27 | OK |
| lambda_origin | ratio | 1.000000 | 1.000000 | OK |
| Q_parameter | accuracy | 1.0 | 1.0 (15/15) | OK |
| Q_parameter | log10_tau_star | 16.974 | 16.974 | OK |
| Q_parameter | tau_star_linear | 9.422e16 | 9.422e+16 | OK |
| Q_parameter | span_decades | 191.842 | 191.8 (출력 반올림) | OK |
| S8_forecast | S8_LCDM | 0.832 | 0.8320 | OK |
| S8_forecast | shift_S8_pct | 1.14 | 1.14 | OK |
| S8_forecast | n_sigma DES/LSST/Euclid | 0.63/2.85/4.38 | 0.63/2.85/4.38 | OK |
| cosmic_shear | S8_SQT | 0.8415 | 0.8415 | OK |
| cosmic_shear | shift_xi_plus_pct | 2.29 | 2.29 | OK |
| monotonic_rejection | chi2_monotonic | 147.62 | 147.62 | OK |
| monotonic_rejection | sigma_1dof_approx | 12.1 | 12.1 | OK |
| mock_false_detection | false_detection_rate | 1.000 | 1.000 (100.0%) | OK |

**결론**: 7/7 expected_outputs JSON 과 stdout 핵심값 완전 일치 (반올림 차이 외 부정합 0건).

---

## §3 paper plan v3 (L634) §5 와 일치 매트릭스

PAPER_PLAN_V3 §5 는 의도적으로 **qualitative-only** (수식·수치 비포함, L631 A4 / 최우선-1 준수). 따라서 일치 여부는 *수치 일치*가 아니라 *티어/스코프/falsifier-tag* 정합으로 평가.

| 스크립트 | plan §5 매핑 | plan tier 표현 | 스크립트 STATUS / classification | 정합? |
|----------|--------------|----------------|----------------------------------|-------|
| verify_milgrom_a0 | §5.1 acceleration-scale | "moderate-pass tier; 1 auxiliary axiom" | stdout `PASS` / JSON `PASS_STRONG` | 부분 정합 (§4 mismatch 1) |
| verify_lambda_origin | §5.2 coupling-scale dimensional uniqueness | "dimensional uniqueness, not dynamical derivation; O(1) hidden DOF" | `CONSISTENCY_CHECK` (L412 down-grade) | OK (둘 다 a-priori 도출 부정) |
| verify_Q_parameter | §5.3 falsifier (lab decoherence) | "pre-registered falsifier" | `PARTIAL` (5 후보 중 C; K3 8-team 미해결) | OK |
| verify_S8_forecast | §5.3 falsifier (Euclid/LSST/DES) | "tied to specific data release" | structural falsifier, Euclid 4.38σ | OK |
| verify_cosmic_shear | §5.3 falsifier (xi+ Euclid/LSST) | 동일 | structural falsifier | OK |
| verify_monotonic_rejection | §5.3 regime-gap channel | "regime-gap only, NOT SPARC-internal" | NOTE 명시 일치 | OK |
| verify_mock_false_detection | §6 limitations / §6.4 hidden DOF | "anchor-driven advantage on null data" CAVEAT | CAVEAT 명시 일치 | OK |

**결론**: 7/7 plan v3 §5/§6 의 honesty-tier 와 정합. plan 이 수치를 안 적기에 "값 일치"는 N/A.

---

## §4 발견된 mismatch

### M1. verify_milgrom_a0: PASS vs PASS_STRONG schema 차이
- stdout 마지막 라인: `PASS`
- expected_outputs JSON `classification`: `"PASS_STRONG (substantive prediction, MOND a_0)"`
- expected_outputs JSON `verdict`: `"PASS"`
- 해석: JSON 은 두 키(`classification` strong / `verdict` PASS)를 분리. 스크립트 stdout 은 `verdict` 만 출력. 데이터 부정합 아님 — schema 표기 분기.
- 영향: 해석상 혼동 가능 (PASS vs PASS_STRONG 혼용). 논문 §5.1 인용 시 어느 키 쓰는지 명시 필요. plan v3 은 "moderate-pass" 라는 *제3* 표현 — 세 표기(`PASS`/`PASS_STRONG`/`moderate-pass`) 가 동일 결과를 가리키나 강도 어휘 상이.

### M2. verify_Q_parameter: classification vs verdict 키 부재
- expected JSON 은 `classification: "PARTIAL"` 만 있고 verdict 키 없음 — milgrom 과 schema 비대칭. 7 JSON 간 schema 일관성 부재 (일부는 `verdict`, 일부는 `classification`만, 일부는 둘 다).
- 영향: compare_outputs.py 자동 비교가 키별로 None 조건 분기 필요할 수 있음. 본 L637 임무 범위 외 (수정 금지).

### M3. monotonic_rejection 시그마 표기
- expected JSON note: 본문은 ~17σ 라고 인용하나 toy 는 ~12.1σ. JSON 자체에 "Both reject monotonic at >> 5 sigma" 로 정직 기재됨. mismatch 라기보다 *내장된 disclosure*.

그 외 mismatch 없음.

---

## §5 정직 한 줄

7 verify 스크립트 전건 exit 0 + expected_outputs JSON 수치 100% 일치 + plan v3 §5 honesty-tier 정합. 단 PASS vs PASS_STRONG vs moderate-pass 세 어휘가 동일 결과(milgrom a₀ 0.71σ)를 가리켜 schema 일관화가 필요하며, 이는 L637 범위 밖 (스크립트/JSON/논문 수정 금지) — 향후 별도 LXX 에서 통일.
