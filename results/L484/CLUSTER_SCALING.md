# L484 — Cluster Scaling Relations: SQT Depletion-Zone vs LCDM Self-Similar

**Date**: 2026-05-01
**Mandate**: Test SQT prediction at σ_cluster scale against M-T_X, M-Y_X, M-σ_v
relations. Compare with Kravtsov 2018 / Kravtsov & Borgani 2012 self-similar
baseline and SPT-SZ + Planck cluster sample anchors.
**Mode**: Relation-level comparison (no chi2 fit, no MCMC — CLAUDE.md L33+
재발방지 규칙 준수).

> **정직 한 줄**: SQT 의 cluster-scale depletion 보정은 *placeholder amplitude
> ε=0.05 에서 LCDM self-similar 와 5% 이내로 구분 불능*. 현재 cluster mass
> 측정 오차 (~10%) 와 hydrostatic bias (~15%) 보다 작아, **이 채널만으로는
> SQT 와 LCDM 을 분리할 수 없다**. PASS 가 아니다.

---

## 1. 표준 (LCDM self-similar)

Kaiser 1986 / Kravtsov & Borgani 2012 ARA&A 50 353:

| 관계 | 자기-유사 slope | 정규화 reference |
|---|---|---|
| M_500c – T_X | 3/2 (M ∝ T^1.5) | Vikhlinin+ 2009: 3.02×10¹⁴ M⊙ at T=5 keV |
| M_500c – Y_X | 3/5 (M ∝ Y_X^0.6) | Kravtsov+ 2006: A=5.77×10¹⁴ M⊙ |
| M_200c – σ_v | ≈ 1/0.336 ≈ 2.975 | Evrard+ 2008: σ_DM = 1082.9 (h(z)M_200/10¹⁵)^0.3361 km/s |

L484 sim 검증: 세 slope 모두 baseline 값 (1.500 / 0.600 / 2.975) 정확 재현.

## 2. SQT depletion-zone 예측 (질적)

CLAUDE.md 최우선-1 (방향만 제공) 준수:
- 함수 형태: `f(M) = 1 − ε · sech²((ln M − ln M_dep)/w)`
- ε, M_dep, w 는 **placeholder**. 8인 팀이 σ_0(M, z) 트래커에서 독립 도출.
- 부호 규약: ε > 0 = mass-deficit (SQT 가 cluster mass 를 *낮추는* 방향).

L484 본 스크립트는 ε=0.05, M_dep=3×10¹⁴ M⊙, w=0.6 (log) 임의 placeholder 로
*형태만* 시각화. 수치 prefactor 의 고정 시도가 아님.

## 3. anchor-level 결과

`simulations/L484/run.py` 출력 (synthetic-from-published anchors):

| 관계 | obs anchor | LCDM | SQT (ε=0.05) | LCDM 편차 | SQT 편차 |
|---|---:|---:|---:|---:|---:|
| M-T_X (T=6 keV) | 4.50 ± 0.5 ×10¹⁴ M⊙ | 3.97 | 3.81 | −1.06σ | −1.38σ |
| M-Y_X (Y=5×10¹³) | 7.50 ± 0.7 ×10¹⁴ M⊙ | 7.84 | 7.78 | +0.48σ | +0.40σ |
| M-σ_v (1000 km/s) | 0.78 ± 0.10 ×10¹⁵ M⊙ | 0.79 | 0.78 | +0.09σ | +0.03σ |

slope diagnostics (log-log fit, 2-15 keV / 0.5-30 Y_X / 500-1500 km/s):

| 관계 | self-sim. | LCDM toy | SQT toy |
|---|---:|---:|---:|
| M-T_X | 1.500 | 1.500 | 1.505 |
| M-Y_X | 0.600 | 0.600 | 0.614 |
| M-σ_v | 2.975 | 2.975 | 3.005 |

## 4. 비교: SPT-SZ / Planck cluster sample

- **SPT-SZ (Bocquet+ 2019, ApJ 878 55)**: 377개 cluster, M_500 ~ 4-12×10¹⁴
  M⊙. tSZ-mass scaling normalisation 정확도 ~10%. self-similar 와 통계적
  일치, σ_8 ≈ 0.766±0.025.
- **Planck PSZ2 (Planck 2016 XXIV)**: ~439 cluster. Y_SZ-M relation 의
  hydrostatic bias (1−b) ≈ 0.62-0.80 (calibration-dependent, σ~10-20%).
- **Vikhlinin+ 2009**: M-T calibration sample, scatter ~15% intrinsic.
- **Sifón+ 2016**: M-σ_v sample for SPT cluster, slope 0.32±0.04 in σ-M log
  (-> M ∝ σ^3.13±0.4), self-similar 와 일치.

**핵심 관찰**: 세 관계 모두 self-similar slope 와 통계적으로 일치하며
intrinsic scatter (15-30%) 가 ε ≲ 0.10 의 SQT 보정을 *흡수*해 버린다.

## 5. PASS / FAIL 판정

| 기준 | 결과 |
|---|---|
| K1: SQT 가 LCDM 보다 명확히 다른 slope 예측? | **FAIL** (slope 차이 ≲ 1%) |
| K2: anchor 편차에서 SQT 가 LCDM 보다 우수? | **FAIL** (세 관계 모두 LCDM 이 같거나 더 나음) |
| K3: ε 의 독립 도출 (CLAUDE.md 최우선-2) | **MISSING** (placeholder 만 사용) |
| K4: SPT/Planck 데이터 직접 비교 | **PARTIAL** (anchor-level only, no full sample) |

**총평: 신규 PASS 없음**. cluster scaling 채널은 SQT depletion-zone 신호가
*있다고 가정해도* 현재 데이터 정밀도로는 LCDM 과 분리 불능. 진짜 PASS 를
얻으려면:

1. ε, M_dep, w 의 SQT 첫원리 도출 (현 placeholder 단계 탈출).
2. Sunyaev-Zel'dovich Y_500 vs weak-lensing M_500 의 *redshift 의존성*
   (f_dep(z)) 채널로 이동 — z-dependence 가 self-similar 와 다를 수 있음.
3. cluster 외곽 (r > r_500) 의 mass profile 에서 depletion-zone 이
   독특한 break 를 만든다면 그것이 차별 채널.

## 6. CLAUDE.md 정합성 점검

- L33+ 적분/chi2 규칙: chi2 fit 미사용. 단지 anchor 편차 σ 표기. ✓
- 최우선-1 (수식/파라미터 사전 지정 금지): ε=0.05 등은 **placeholder** 로
  명시, "SQT 가 이 값" 주장 아님. ✓
- L5 "background-only fix 가 S8 등을 자동 해결" 금지: 본 결과는 *못 한다*
  쪽 보고, 정직 기록. ✓

---

## 7. 산출물

- `results/L484/CLUSTER_SCALING.md` (이 파일)
- `results/L484/scaling_table.tsv` (anchor 비교 + slope)
- `results/L484/scaling_relations.png` (M-T, M-Y, M-σ 3 panel)
- `simulations/L484/run.py`

## 8. 한 줄 결론

> SQT cluster depletion-zone 효과는 *현재 SPT/Planck 데이터 정밀도 안에 숨을
> 만큼* 작거나, *self-similar 와 동일한 형태로* 위장한다. PASS 못 함.
> 다음 시도는 z-진화 (M-T 의 redshift dependence) 또는 외곽 profile break
> 채널.
