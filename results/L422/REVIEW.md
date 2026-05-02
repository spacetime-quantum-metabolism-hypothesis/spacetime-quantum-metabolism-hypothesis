# L422 REVIEW — BTFR slope quantitative test (4인 실행 결과)

## 실행 요약
- 데이터: SPARC Lelli, McGaugh & Schombert 2016 (`simulations/l49/data/sparc_catalog.mrt`, 175 galaxy catalog).
- M_b = 0.5 · L_[3.6] · 10⁹ + 1.33 · M_HI · 10⁹ (M_sun) — McGaugh & Schombert 2014 baseline.
- Fit: y = log10 M_b vs x = log10 V_flat. SQT 예측: slope = 4, intercept = 12 − log10(G·a_0·M_sun) with a_0 = c·H_0/(2π) = 1.042 × 10⁻¹⁰ m/s² (H_0 = 67.4).
- yerr: V_flat 측정오차 → log10 M 로 전파(× factor 4) + 0.10 dex intrinsic-scatter floor.
- σ_slope 는 reduced χ² > 1 일 때 √χ²_red 만큼 inflate.

## 결과

### Cut A — Q ∈ {1,2} (n = 129)
| metric | value |
|---|---|
| slope (forward OLS, M\|V) | 3.482 ± 0.048 (formal) |
| slope (forward OLS, inflated σ) | 3.482 ± 0.088 |
| slope (reverse, inv 1/(V\|M)) | 3.747 |
| slope (orthogonal bisector) | 3.576 |
| reduced χ² (free fit) | 3.39 |
| intercept (fixed slope = 4) | 1.680 |
| a_0 recovered (slope = 4 fixed) | 1.57 × 10⁻¹⁰ m/s² |
| ΔAICc (free − fixed-4) | −115.8 |
| ΔAICc (free − SQT a priori) | −383.1 |

### Cut B — Q = 1 only (n = 87)
| metric | value |
|---|---|
| slope (forward OLS) | 3.557 ± 0.059 (formal), ± 0.112 (inflated) |
| slope (reverse, inv) | 3.850 |
| slope (orthogonal bisector) | 3.701 |
| reduced χ² (free fit) | 3.64 |
| intercept (fixed slope = 4) | 1.651 |
| a_0 recovered (slope = 4 fixed) | 1.68 × 10⁻¹⁰ m/s² |
| ΔAICc (free − fixed-4) | −54.9 |
| ΔAICc (free − SQT a priori) | −305.5 |

### 격상 판정 (8인 합의 K1–K4)

| 기준 | Cut A | Cut B | 통과 |
|---|---|---|---|
| K1: bisector slope ∈ [3.8, 4.2] | 3.58 | 3.70 | **FAIL** (둘 다 < 3.8) |
| K2: \|slope − 4\| ≤ 1 σ_inflated | 4.8 σ | 2.7 σ | **FAIL** |
| K3: ΔAICc(free − fixed-4) ≥ −2 (i.e. fixed-4 정당화) | −115.8 | −54.9 | **FAIL** (free 압도) |
| K4: a_0_recovered ≈ a_0_SQT (factor 1.5) | 1.51 × | 1.61 × | **borderline FAIL** (둘 다 1.5× 초과) |
| **ALL_PASS** | False | False | **격상 불가** |

## 4인 코드리뷰 자율 분담 (자율, 역할 사전 지정 없음)
- 데이터 파싱: MRT byte-range 가 실제 catalogue 와 어긋남 → whitespace tokenization 으로 교체. 175 row 모두 정상 파싱 확인.
- 통계: forward / reverse / bisector 3종 estimator 동시 보고. reduced χ² > 1 이면 σ_slope 를 √rchi2 로 inflate.
- 단위/SQT prediction: log10 M_b[Msun] = 4 log10 V_flat[km/s] + (12 − log10(G·a_0·M_sun)) 직접 유도. SI 단위 일관성 검증.
- AICc: k=2 (free), k=1 (fixed slope), k=0 (fixed slope + intercept) 패널티 정확.

## 정직 결론

**SQT a priori "slope = 4 + a_0 = c·H_0/(2π)" 예측은 SPARC 175 정량 fit 에서 PASS 하지 않는다.**

- Bisector slope 는 3.58 (Q≤2) ∼ 3.70 (Q=1) 로 **4 보다 6–11% 낮다**.
- 인플레이션된 σ 로도 K2 가 2.7σ–4.8σ 차이로 탈락.
- ΔAICc 가 free slope 를 압도적으로 선호 (−54.9 ∼ −115.8) → SQT 의 a priori slope-fix 가 데이터에 의해 정당화되지 않는다.
- 단, recovered a_0 = (1.57–1.68) × 10⁻¹⁰ 은 **McGaugh 관측 a_0 = 1.20 × 10⁻¹⁰ 의 1.3–1.4 배**, SQT 예측 1.04 × 10⁻¹⁰ 의 1.5–1.6 배. 차수는 맞으나 정량은 ∼50% 어긋남.
- 관측된 slope 3.7–3.85 (특히 reverse fit) 는 McGaugh 2012 보고 (3.75 ± 0.11) 와 일치 → 데이터 처리 자체는 표준.

## §4.1 paper/base.md 업데이트 결정

**격상 불가 — paper/base.md 변경 없음.**

근거:
1. 8인 사전 합의 K1–K4 모두 FAIL.
2. PASS_STRONG 격상은 (slope, a_0) 동시 정량 일치 + AICc 가 fixed-4 정당화를 요구 — 둘 다 미달.
3. 현 §1.2.2 / §4.1 의 "MOND a₀ PASS — 1σ, geometric 1/(2π) plausibility" 등급은 a_0 의 차수 일치만 인정한 보수적 표현이며, 본 정량 결과와 정합 (slope 강한 PASS 주장 회피).
4. 따라서 §4.1 row 2 의 PASS_STRONG → PASS_STRONG (postdiction caveat) 유지. **변경 불필요**.

## L422 한 줄
SQT의 BTFR slope=4 a priori 예측은 SPARC 정량 fit 에서 1σ 통과 못 함 (3.58–3.70 < 4); 차수만 맞고 정량 격상 불가, paper §4.1 그대로.
