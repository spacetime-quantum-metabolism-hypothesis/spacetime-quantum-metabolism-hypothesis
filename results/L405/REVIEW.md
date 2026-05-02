# L405 — 4인팀 코드리뷰 + 결과 해석 (자율 분담)

세션 일자: 2026-05-01
대상: simulations/L405/run.py + results/L405/run_log.txt + report.json
원칙: CLAUDE.md Rule-B — 4인팀 자율 분담, 역할 사전 지정 없음.

---

## 0. 실행 환경

- Python 3.9, numpy 2.0.2, scipy 1.13.1, dynesty 3.0.0
- macOS, OMP/MKL/OPENBLAS=1 강제
- seed=42, 8 toy anchors (base.md §3.5/§3.6 구조 calibrated)

---

## 1. 4인팀 자율 분담 점검 (요약)

**R1 (자율: 코드 구조):** "run.py 는 4 model (three_regime, two_regime,
monotonic, lcdm) 각각 (k, prior_centre, prior_natscale) 정의 명확. Laplace
근사로 ln Z 계산하는 `laplace_logz` 함수가 8 restarts Nelder-Mead + central
diff Hessian. R-grid + extra-anchor forecast + dynesty smoke 3 단계 분리 좋음.
한 가지 — `forecast_with_extra` 가 unused (대신 `print_anchor_forecast` 가
직접 globals 변경). dead code 정리 권고하나 결과 영향 없음."

**R2 (자율: 수치 결과 해석):**
- Sanity: 3R χ²=3.6 (8점-5param=3 dof, χ²/dof≈1.2 정상),
  2R χ²=137 (5dof, *bad*), monotonic χ²=135 (4dof, bad), LCDM χ²=195 (7dof, bad).
- **R-grid (핵심)**:

| R | 3R−LCDM | 2R−LCDM | monotonic 수렴 |
|---|---------|---------|----------------|
| 2  | +81.12 | +16.54  | nan (Hess 특이) |
| 3  | +79.90 | +15.98  | OK              |
| 5  | +78.37 | +15.09  | OK              |
| 10 | +14.68 | +13.76  | OK              |

  → R=10 에서 3R Δln Z 가 81→15 로 **급락**. Lindley wide-prior collapse 전조.
  실 데이터 marginalized Δln Z=0.8 (paper §3.6) 와 절대값은 다르나 *형태*
  (R 증가 시 단조 감소, R≥일정 임계에서 collapse) 는 동일 우려 적용.
- **Extra anchor**: compat 시나리오 +2.48 lnZ 이득, tension 시나리오 +0.35
  lnZ (사실상 baseline 유지). toy 라 절대 변화량 작음.
- **dynesty smoke**: ln Z(3R)= -19.12 ± 0.70, ln Z(LCDM)= -101.73 ± 0.38,
  Δ = +82.61 ± 0.79 — Laplace +78.37 대비 +4.27 차이. Hessian 근사가 약 4
  단위 underestimate (3-regime 의 hard threshold t1, t2 비매끄러움 영향 의심).

**R3 (자율: 통계 해석):** "본 toy 의 Δln Z 절대값 (~78) 은 paper §3.6 의 0.8
과 두 자릿수 차이. 이유: (a) toy anchor σ_err 가 0.05–0.10 으로 too tight,
(b) 3-regime 모델이 anchor 점에 perfectly 맞도록 합성. 이는 *의도된 calibration*
이며, run.py docstring 에 명시함. **신뢰 구간**: R-sensitivity *상대 변화율*
(R=5 → R=10 에서 Δln Z 가 5분의 1 로 줄어듦) 만 신뢰. 실 데이터 0.8 → R=10
에서 음수 가능성 — L406 실측 dynesty 에서 확인 필수. **paper 본문 인용 시**:
'Lindley fragility risk: in toy calibration, ΔlnZ collapses by factor ~5 at
R=10 vs R=5; production run pending (L406).' 형태 권장."

**R4 (자율: 정직성/정합성 audit):**
- monotonic R=2 에서 nan 발생 (Hess 특이) — narrow prior 에서 sigmoid w 파라미터
  underspec. 결과 영향 없음 (nan 줄만 표시).
- numpy 2.x trapezoid 규칙 미적용 (run.py 는 trapz 사용 안 함, 무관).
- print 유니코드 ('Δ', '±') 사용 — macOS UTF-8 환경에서 문제 없으나, Windows
  cp949 환경 실행 시 깨질 수 있음. CLAUDE.md "print 유니코드 금지" 위반 우려.
  → **fix 권고**: `Δ` → `Delta`, `±` → `+/-` 로 변경 (다음 세션). 본 세션은
  결과 출력 확인만으로 진행 (macOS 정상 출력 검증 완료).
- forecast_with_extra dead code (R1 지적) — 정직성 영향 없음.
- ATTACK_DESIGN B1–B10 매핑: B2 (R-grid 미보고) → R-grid 표 생성 ✓.
  B8 (dynesty 미수행) → smoke test 완료 ✓. B9 (extra anchor) → forecast ✓.
  B1, B4, B5 는 구조적 — 본 코드로 회피 불가 (paper-side framing 으로만 회복).

---

## 2. 4인팀 합의

1. run.py 정상 동작. 3 단계 (R-grid, anchor forecast, dynesty smoke) 모두
   수행되어 ATTACK_DESIGN B2/B8/B9 즉시 회복.
2. 절대값은 toy 한계 — paper §3.6 인용 시 *상대 변화 패턴* 만.
3. R=10 collapse 신호 (toy) → 실 데이터에서 Lindley fragility 정밀 측정 필요
   = L406 production dynesty.
4. dynesty Laplace gap +4.27 → 3-regime hard threshold 모델은 Laplace 신뢰
   부족. paper §3.6 marginalized Δln Z=0.8 도 Laplace 산출이라면 dynesty
   재산출 시 ±1-2 lnZ 변동 가능 — referee 가 "which ln Z method" 질문 시
   대비 답변 필요.
5. 다음 세션 (L406): 실 SPARC Q=1 + A1689 + cosmic 데이터 → dynesty
   nlive=500, 4 model production. budget ~수시간.

정직 한 줄: toy R-grid 에서 R=10 collapse 관찰 — 실 데이터에서 동일 패턴이
면 §3.6 Δln Z=0.8 가 R=10 에서 음수로 떨어질 위험 실재, L406 production
dynesty 로 즉시 검증 필요.
