# L422 NEXT_STEP — BTFR slope 정량 측정 설계

## 8인 다음 단계 합의

### 데이터
- 파일: `simulations/l49/data/sparc_catalog.mrt` (Lelli, McGaugh & Schombert 2016, 175 galaxy)
- 컬럼: `D` (Mpc), `Inc` (deg), `L[3.6]` (10⁹ L_sun), `MHI` (10⁹ M_sun), `Vflat` (km/s), `e_Vflat` (km/s), `Q` (1/2/3)

### Baryonic mass
- M_b = Υ_⋆ · L_[3.6] + 1.33 · M_HI [M_sun]
- Υ_⋆ = 0.5 M_sun/L_sun (McGaugh & Schombert 2014, baseline)
- 1.33 factor: He correction

### Quality cuts
- Cut A: Vflat > 0 AND e_Vflat > 0 AND Q ∈ {1,2} (Lelli 표준 cut)
- Cut B: Q = 1 only (high-quality)
- 두 cut 모두 결과 표 동시 보고

### Fit
- y = log10(V_flat / km/s)
- x = log10(M_b / M_sun)
- Three estimators:
  1. OLS forward (y|x)
  2. OLS reverse (x|y) → invert
  3. Orthogonal (BCES bisector)
- yerr = e_Vflat / (V_flat · ln10)
- 1차: 단순 (slope, intercept) free fit
- 2차: slope = 4.00 fixed, intercept free (SQT a priori)
- 3차: SQT 정확 형식 V^4 = G·M·a_0 (slope=4 + a_0 = c·H_0/(2π) 모두 fixed) → χ² 단독 평가

### SQT prediction
- a_0 = c · H_0 / (2π) = (2.998e8 × 67.4 × 1000 / 3.086e22) / (2π) ≈ 1.16 × 10⁻¹⁰ m/s²
- 관측 a_0 (McGaugh): 1.20 × 10⁻¹⁰ m/s²
- 예측 BTFR: log V_flat = (1/4) log(G·M_b·a_0) → intercept_pred = (1/4) log(G·a_0) (in SI, then convert)

### 판정 기준 (PASS_STRONG 격상 조건, 8인 합의)
- K1: slope_free ∈ [3.8, 4.2] (free fit)
- K2: |slope_free − 4.0| / σ_slope ≤ 1 (within 1σ of SQT prediction)
- K3: Δ AICc(free vs fixed-4) ≤ 2 (free 가 정당화 안 됨; SQT a priori 이김)
- K4: a_0_fit = G · 10^(intercept) inversion 이 SQT 예측 1.16e-10 m/s² 와 1σ 일치

### 산출
- `simulations/L422/run.py`
- `results/L422/REVIEW.md` — 결과 + 8인/4인 판정 + 격상 결정
