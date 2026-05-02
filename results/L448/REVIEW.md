# L448 — REVIEW: BTFR Zero-Point (a_0) A Priori Test

## TL;DR

**FAIL on all four K-criteria.** SQT a priori prediction `a_0 = c·H_0/(2π) = 1.042e-10 m/s² (Planck H_0)` is **3.7–6.0σ low** vs SPARC empirical median across all quality cuts. Stellar M/L (Υ★) variation alone cannot rescue: requires Υ★ ≥ 0.60 (above McGaugh-Schombert 2014 baseline 0.50). H_0 required to bring SQT into agreement: **98.6–111.6 km/s/Mpc**, well above any extant H_0 measurement.

## 측정값 (median estimator, slope=4 fixed)

| Cut | n | a_0 median (m/s²) | log10 σ (boot) | ratio SQT/data | σ(Planck) | σ(McGaugh) |
|-----|---|-------------------|----------------|----------------|-----------|------------|
| Q1     | 87  | 1.726e-10 | 0.0383 | 0.604 | 5.73 | 4.13 |
| Q12    | 129 | 1.526e-10 | 0.0280 | 0.683 | 5.92 | 3.73 |
| Q123   | 135 | 1.524e-10 | 0.0273 | 0.684 | 6.05 | 3.81 |

68% bootstrap intervals do **not** include either SQT (1.04e-10) or McGaugh (1.20e-10).

## SQT 와 McGaugh 의 관계

McGaugh 의 관측값 1.20e-10 자체도 SPARC 미디언 1.52–1.73e-10 과 **3.7–4.1σ 떨어짐**. 즉 본 분석의 데이터 (Vflat, MHI, L36, He=1.33, Υ★=0.5) 처리 규약 하에서는 McGaugh 1.20 도 underpredict. McGaugh 1.20 은 보통 baryonic-mass 계열 별도 보정 + radial-acceleration relation 수렴값에서 유도. SQT 의 `c·H_0/(2π)` 는 **0.868× McGaugh** 로 13% 부족 — McGaugh 값 자체와 비교하면 SQT 는 1σ 안 (K_Z3b: SQT 가 McGaugh 와 sigma_distance ~ 2.7 — 여전히 FAIL, 하지만 관측 a_0 정의 모호성 안에 들 가능성).

## Υ★ sensitivity (Q12 기준)

| Υ★ | a_0 median | SQT/data ratio | within 30%? |
|------|------------|----------------|--------------|
| 0.30 | 2.083e-10  | 0.500 | NO |
| 0.40 | 1.773e-10  | 0.588 | NO |
| 0.50 | 1.526e-10  | 0.683 | NO (default) |
| 0.60 | 1.375e-10  | 0.758 | YES (boundary) |
| 0.70 | 1.263e-10  | 0.825 | YES |

→ Υ★ 을 0.5 → 0.7 로 올리면 30%-band 통과. 그러나 Υ★ = 0.7 은 3.6μm IRAC 의 IMF + age priors 로부터 도출되는 표준값 (Schombert et al. 2019 reports 0.5±0.1 with population synthesis, not 0.7).

## H_0 requirement

SQT a_0 가 데이터 median 을 (Q12) 30%-band 안으로 재현하려면 H_0 ∈ **[69.1, 128.3]** km/s/Mpc (lower bound 69.1 이 실제 의미). 즉 30% 관용 안에서는 SH0ES H_0=73.04 도 통과. **central match (no tolerance)**: H_0_required ≈ 98.7 km/s/Mpc — 어떤 H_0 측정과도 불일치.

## K-기준 PASS/FAIL

- K_Z1 (within 30% of SQT prediction): **FAIL** (Q1/Q12/Q123 all)
- K_Z2 (SQT within 2σ of data): **FAIL** (5.7–6.0σ off)
- K_Z3 (data ↔ McGaugh observed): **FAIL** (3.7–4.1σ off — 데이터 처리 규약 차이)
- K_Z4 (Υ★ ∈ [0.4, 0.6] 안정성): **FAIL** (Υ★ ≥ 0.6 만 통과)

## Honest interpretation

1. **Slope (L422 FAIL) + zero-point (L448 FAIL) → BTFR 채널은 SQT 형식의 deep-MOND 한계를 완전히 지지하지 않음.** 두 차원 모두 죽었다.
2. **단, "방향성"은 살아있다**: SQT 예측값 1.04e-10 은 관측 a_0 와 같은 자릿수, 같은 부호. ≈ 0.6–0.8× 의 비율은 우연으로 보기에는 좁다. SQT 가 이 비율을 더 큰 이론 (예: 환경의존 a_0(z), 은하 mass dependence) 의 leading term 으로 해석하는 것은 가능.
3. **rescue path 의 비용**: a_0_eff 와 SQT 일치를 위해서는 (a) Υ★ ≈ 0.6–0.7 (관측 priors 와 충돌), (b) H_0 ≈ 100 km/s/Mpc (어떤 측정도 없음), 또는 (c) `a_0 = ξ · c·H_0/(2π)` 의 dimensionless 결합상수 ξ ≈ 1.46 도입 (a priori 성격 상실). 모두 받아들이기 어렵다.
4. **L422 slope 와의 결합**: slope 3.58–3.70 < 4 이면 데이터의 V^4/M 이 큰 V (큰 M) 에서 점증함 — 즉 어떤 조건이든 a_per 가 mass 의존적. SQT 가 단일 universal a_0 를 가정하면 이 mass-dependent drift 를 흡수 못함.

## 정직 한 줄

BTFR zero-point a priori 는 5–6σ 로 KILL — slope 채널과 결합해 BTFR 전체 가 SQT-MOND 한계의 단순 형식을 지지하지 않는다.
