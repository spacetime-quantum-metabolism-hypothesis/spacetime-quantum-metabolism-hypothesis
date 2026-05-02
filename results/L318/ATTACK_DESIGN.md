# L318 — Attack Design (Paper figures + tables plan)

## 목적
L274 outline 을 받아 JCAP 제출용 figures (9 essential) 과 tables (4) 의
**제작 명세** (caption / 축 / 단위 / 색맹 / 데이터 출처 / 재현 경로) 를 확정.
실제 TeX/PNG 생성은 별도 long-running session. 본 loop 는 spec 만.

## 방향 (지도 아님)
- 색맹 안전: matplotlib `viridis`/`cividis` 또는 Wong 8-color palette. 빨강/녹색 단독 대비 금지.
- 단위 명시: 모든 축에 SI + 천체물리 관용 단위 병기.
- 재현성: 각 figure 캡션 끝에 `[Source: results/Lxx/...]` 태그 강제.
- JCAP figure budget: 본문 ≤ 10 figures (9 essential 적합). 부록 무제한.
- 단일 컬럼폭 86 mm / 2-컬럼폭 178 mm 기준. dpi ≥ 300, vector 우선 (PDF/EPS).
- 모든 figure 는 grayscale print 에서도 판독 가능해야 함 (line-style + marker 차이).

---

## Figures (9 essential) — 제작 명세

### F1 — σ_0(env) 3-regime
- **내용**: 환경 (galactic / cluster / cosmic void) 별 σ_0 측정값 + 이론 prediction band.
- **축**: x = environment label (categorical, 3 bins) / y = σ_0 [SI 단위, m³ kg⁻¹ s⁻¹], log scale.
- **plot type**: errorbar + 이론 horizontal band.
- **색**: Wong palette idx 0/2/4 (blue/green/orange).
- **재현**: results/L1xx σ_0 fit 결과 → JSON aggregator 필요.
- **caption 핵심**: "환경 독립성 검정. 3 regime 모두 동일 σ_0 within 1σ → 보편 상수 가설 지지/기각 명시."

### F2 — SPARC fit examples (3 galaxies)
- **내용**: 대표 galaxy 3종 (low/mid/high surface brightness) 회전곡선 + SQMH fit + LCDM/MOND 비교.
- **subplot**: 1×3 panel.
- **축**: x = R [kpc] / y = V_circ [km/s].
- **선**: SQMH (solid), MOND (dashed), Newtonian baryon (dotted), 데이터 (errorbar).
- **재현**: SPARC 데이터 + results/L1xx SQMH fit pipeline.

### F3 — a_0 = c·H_0/(2π) derivation
- **내용**: predicted vs measured a_0 비교 (numerator). 또는 derivation pictograph + posterior.
- **축**: x = experiment / y = a_0 [m s⁻²].
- **horizontal line**: SQMH prediction c·H_0/(2π) ± H_0 uncertainty band.
- **재현**: results/L1xx a_0 derivation note.

### F4 — Cluster mass profile
- **내용**: 대표 cluster (e.g. Coma, A1689) 의 M(<r) profile, SQMH vs NFW vs lensing.
- **축**: x = r [Mpc], log / y = M(<r) [M_sun], log.
- **재현**: results/L1xx cluster fit.

### F5 — ρ_q evolution Bianchi (L207)
- **내용**: ρ_q(t) over redshift / cosmic time, Bianchi I anisotropic background.
- **축**: x = z (or a), log / y = ρ_q / ρ_q0, log.
- **선**: isotropic FLRW (reference) + Bianchi shear levels (3 curves).
- **재현**: results/L207/L207.png 재가공 + report.json.

### F6 — Hierarchical GMM (L273)
- **내용**: hierarchical Gaussian mixture model posterior on σ_0 분포.
- **축**: x = σ_0 / y = posterior density.
- **plot**: violin or KDE per cluster + global posterior overlay.
- **재현**: results/L273/report.json.

### F7 — Mock injection (L272)
- **내용**: injection-recovery test. true vs recovered parameter.
- **축**: x = injected / y = recovered, 1:1 line + scatter.
- **재현**: results/L272/report.json.

### F8 — IC 4종 비교 bar
- **내용**: 4 information criteria (AIC, AICc, BIC, DIC) Δ값 bar chart for SQMH vs LCDM/MOND/wCDM.
- **축**: x = model / y = ΔIC vs best, grouped bars (4 IC × N model).
- **참조선**: ΔIC = 2, 6, 10 thresholds.
- **재현**: results/L1xx IC summary aggregator.

### F9 — Facility forecast P15-P22
- **내용**: P15~P22 (8 falsifiable predictions) 의 향후 facility (DESI DR3, Euclid, LSST, SKA, CMB-S4) sensitivity forecast.
- **축**: x = prediction id (P15~P22) / y = SQMH 예측값 ± 미래 1σ error bar.
- **plot**: errorbar + facility legend (markers).
- **재현**: forecast script (sigma scaling from public ETC).

---

## Tables (4) — 제작 명세

### T1 — Axioms
- **column**: id (A1..) / 명제 / 형식 표현 / 정당성 출처.
- **포맷**: booktabs longtable, two-column 가능.
- **완전성 check**: L160 PAPER_DRAFT axioms 와 1:1 매핑.

### T2 — Derived quantities
- **column**: 기호 / 정의 / SI 값 ± 1σ / 출처 Lxx.
- **포함**: σ_0, n₀μ, a_0, ρ_q0, t_P 등.

### T3 — Predictions + Limitations
- **column**: P# / 진술 / 검정 가능 데이터셋 / 현 상태 (passed/pending/limitation).
- **14 predictions + 8 limitations** = 22 row, longtable.
- **색 강조 금지** (grayscale print).

### T4 — Evidence summary
- **column**: 데이터셋 / N / χ²/dof / Δχ² vs LCDM / 출처 Lxx.
- BAO / SN / CMB / RSD / SPARC / cluster / GW / lab.

---

## 재현성 규약 (모든 figure/table 공통)
1. 각 figure script 는 `paper/figures/fig{n}_*.py`.
2. 데이터 의존성은 `results/Lxx/report.json` 만 사용 (raw 재실행 금지).
3. caption 끝에 `[Source: results/Lxx, script: paper/figures/figN.py]`.
4. seed 고정 (np.random.seed=42), git hash 캡션 footnote 권고.
5. PDF 빌드는 `make figures && make paper`.

## 위험
- F1 σ_0 환경별 측정값 aggregation 미수행 → 별도 L319+ pipeline 필요.
- F9 facility forecast 의 1σ 추정은 ETC 단순화 — 캡션에 "approximate" 명시.
- T3 22-row longtable JCAP 본문 길이 압박 → 본문 6 row + 부록 잔여 분리 옵션.

## 정직
실제 figure rendering / TeX table 생성은 본 loop 미수행. spec 확정만.
