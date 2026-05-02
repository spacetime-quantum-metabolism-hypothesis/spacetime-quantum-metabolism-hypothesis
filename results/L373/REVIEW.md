# L373 REVIEW — SPARC monotonic vs V-shape (marginalized lnZ 실측)

## 실행 결과 (`results/L373/report.json`)

| 모델 | k | χ² | AIC | BIC | AICc | Laplace ln Z |
|---|---:|---:|---:|---:|---:|---:|
| M1 linear (monotonic)     | 2 | **209.776** | 213.78 | 219.96 | 213.85 | **−112.603** |
| M2 V-shape symmetric      | 3 | 206.817 | 212.82 | 222.10 | 213.07 | −112.798 |
| M2 V-shape asymmetric     | 4 | 202.818 | 210.84 | 223.19 | 211.10 | −114.444 |

**N = 163 galaxies** (L69 step1, log_a0+log_Vmax 둘 다 유한). σ_y = 0.567 dex (L69 residual_std).

**M1 best fit**: A=−11.243, B=+0.532. `log_a0 ≈ −11.24 + 0.53 · log_Vmax` — 정상-방향 monotonic.

**M2 sym best fit**: A=−10.43, B=+0.69, x0=1.30 (≈ 데이터 좌측 경계 근처) — V-shape 의 vertex 가
경계 근방에 박혀 사실상 단조 line 과 거의 동치 (Δχ² = 2.96).

**M2 asym best fit**: x0=1.78, B_L=−1.95, B_R=+0.22 — formal Δχ²=6.96 으로 chi² 만 보면 약한
개선이지만 lnZ 는 더 나빠짐 (Occam 패널티 +1.84).

## Δ 비교 정량

- **Δχ² (M1 − M2sym)** = +2.96 — **3-anchor L342 의 +288 대비 ≈ 1/97 수준** (즉 SPARC 데이터는
  비단조성을 거의 선호하지 않는다).
- **Δχ² (M1 − M2asym)** = +6.96.
- **Δ ln Z (M2sym − M1)** = **−0.20**. → "거의 무차별, 약하게 M1 (monotonic) 선호."
- **Δ ln Z (M2asym − M1)** = **−1.84**. → 약한 M1 선호 (Occam 패널티 가 χ² 개선을 상쇄).
- **ΔBIC (M1 − M2sym)** = −2.14, **ΔBIC (M1 − M2asym)** = −3.23. BIC 도 M1 을 선호.

## L342 vs L373 대조

| 항목 | L342 | L373 |
|---|---|---|
| 데이터 | 3 anchor (cosmic/cluster/galactic) | SPARC 163 galaxies |
| Regime span | 6 dex in log ρ_env | ~1.3 dex in log_Vmax (galactic only) |
| Δχ² (mono → V-shape) | **288.04** | **2.96** |
| 해석 | cluster outlier 가 단조성 17σ 기각 | galactic 내부엔 비단조 흔적 거의 없음 |
| caveat | single-source cluster 의존 | env-proxy 가 log_Vmax (intra-halo) |

## 정직 평가

1. **L342 의 17σ 는 galactic-내부 효과가 아니라 regime-간 갭**임을 본 loop 가 *데이터로*
   확인. L342 결과를 "SPARC 도 비단조" 로 확대해석하면 안 된다.
2. **galactic regime 내부**에선 단조 linear 가 marginalized lnZ 로도 BIC 로도 약하게 선호.
   비단조성 prior 강도는 본 채널에서 0 에 가깝다.
3. **L371 −0.12 등급 회복 효과**: 본 실측은 이론에 추가 힘을 주지 않으나, "비단조성이
   regime-간 효과임" 이라는 caveat 를 *수치로* 굳히므로 L342 해석의 reproducibility 가
   강해진다. 등급 영향 ≈ +0.000~+0.005 (caveat clarification).
4. **위험**: x = log_Vmax 가 env density 의 진짜 proxy 가 아닐 가능성. 더 좋은 proxy
   (local density Σ_5, group catalog environment) 로 재검증 필요.

## 한계

- σ_y 일정 가정 (per-galaxy chi2_red 무시). chi2_red weighting 으로 재실행 필요.
- Laplace 근사: posterior 가 unimodal/gaussian 가정 — V-shape 의 multimodality (x0 grid)
  엄밀히는 nested sampling 필요.
- prior box 는 generous 하지만 임의적. 폭 의존성 ΔlnZ 영향 ≈ ±0.5 추정.

## 정직 한 줄

> SPARC 163-galaxy 분포에서 monotonic linear 와 V-shape 의 marginalized Δ ln Z = −0.2 ~ −1.8 (M1 선호) — L342 의 Δχ²=288 은 SPARC 내부가 아니라 cluster-vs-galactic regime gap 에서 온 것이며, galactic regime 자체는 비단조성 흔적이 거의 없다.
