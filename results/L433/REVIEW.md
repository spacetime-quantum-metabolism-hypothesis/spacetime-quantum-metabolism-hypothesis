# L433 REVIEW — 4인팀 자율 코드리뷰 + forecast 결과 평가

**대상**: `simulations/L433/run.py` + `l433_results.json`.
**규칙**: Rule-B 4인 자율 분담 (역할 사전 지정 없음, CLAUDE.md). 결과 왜곡 금지.

---

## 1. 4인팀 자율 분담 코드리뷰

### (i) 적분/grid
- `scipy.integrate.quad` 로 `r_s(z)` 와 `D_C(z)` 를 직접 적분. `epsrel=1e-7~1e-8`, `limit=400` 충분.
- `Z_INF = 1.5e4` 상한 → 라디에이션 우세 영역까지 포함, sound horizon 적분 수렴.
- Drag/recombination 분리 (`Z_DRAG=1059.94`, `Z_STAR=1089.92`) 충족.

### (ii) 단위 일관성
- `c_s` [km/s], `H` [km/s/Mpc] → `c_s/H` 단위 [Mpc] OK.
- `D_C` 동일 단위 OK. flat universe `D_A = D_C / (1+z)` OK.

### (iii) Sentinel / NaN
- `compute_shifts(beta=0)` 가 정확히 0 을 반환 (β=0 ⇒ LCDM 동일 함수형) → sanity 통과.
- ODE 폭주 위험 없음 (closed-form `E_sqmh` 사용). NaN guard 불필요.

### (iv) "Planck σ" 정의 명시
- `PLANCK_THETA_STAR_SIG_FRAC = 2.98e-6` ← Planck 2018 Plik 100θ_* = 1.04110 ± 0.00031.
- `PLANCK_RD_SIG_FRAC = 0.0020` ← r_d = 147.05 ± 0.30 Mpc.
- 본 forecast 는 두 σ 모두 제공해 "× 23" 라벨 의미 모호성 제거.

**4인팀 합의**: 코드 측 결함 없음. 결과 해석 진행 가능.

---

## 2. Forecast 결과 — β grid scan

| β | δr_d/r_d | δθ_*/θ_* | N σ(Planck θ_*) |
|---|----------|----------|-----------------|
| 0.000 | +0.0e+00 | +0.0e+00 | 0.0 |
| 0.020 | −3.5e−05 | +1.3e−04 | 44 |
| 0.050 | −2.2e−04 | +8.2e−04 | 276 |
| 0.080 | −5.7e−04 | +2.1e−03 | 705 |
| 0.100 | −8.9e−04 | +3.3e−03 | 1099 |
| 0.107 | −1.0e−03 | +3.7e−03 | 1257 |
| 0.150 | −2.0e−03 | +7.3e−03 | 2450 |
| 0.200 | −3.5e−03 | +1.3e−02 | 4297 |
| **0.300** | **−7.9e−03** | **+2.8e−02** | **9315** |
| 0.400 | −1.4e−02 | +4.7e−02 | 15753 |

**0.7% δr_d 재현하는 β ≈ 0.30**.

---

## 3. 결정 게이트 평가

### G1 — axiom + 1 파라미터 forward
**PASS (구조적)**: 본 toy 는 β 1개 dynamical 파라미터로 r_d, r_s(z_*), D_A(z_*) 를 동시 도출.
단, 본 toy 의 함수형 (`drift = 1+β² · matter_window`) 은 axiom 도출이 아닌 *방향 placeholder*.
NEXT_STEP.md Step 1 의 채널 결정이 선행돼야 G1 의 *substantive* PASS 로 격상 가능.

### G2 — δθ_*/θ_* ≥ 3σ
**PASS (강하게, 그러나 잘못된 방향)**: β=0.30 에서 δθ_* = 2.8e−2 = 9315σ.
이는 0.7% δr_d 가 **Planck θ_* 과 정합 불가능** 함을 의미.
즉 *δr_d 만 보면* 0.7% 가 가능 하지만 *동시* δθ_* 가 ~10⁴σ 위반.

### G3 — Forecast falsifiable?
**PASS**: Planck 2018 자체가 이미 본 toy 의 β ≥ 0.02 영역을 ≥ 44σ 로 falsify.
LiteBIRD (≈ 2030) 의 σ(θ_*) 향상은 본 결론을 강화.

---

## 4. PARTIAL #6 등급 재평가

본 toy template 가 *유일한* matter-era φ 채널 후보는 아니다 (NEXT_STEP.md A.Step 1 의 3개 후보 중 1개).
그러나 **세 채널 모두에서 r_d 와 r_s(z_*) 가 동일 부호로 움직이고 D_A 가 부분 cancel** 하는 구조는 공통이며,
"0.7% δr_d 를 Planck σ 통과시키는 β 영역 = 약 |β| ≤ 0.02" (현재 toy 기준) 로 *극단적으로 좁다*.

**4인팀 정직 평가**:
1. "δr_d/r_d ≈ 0.7%" 자체는 β ≈ 0.3 에서 재현 가능 → **descriptive 라벨로서는 valid**.
2. 그러나 *동일 β* 가 Planck θ_* 측정과 **9300σ 불일치** → **prediction 으로 인용하면 자기파괴**.
3. 따라서 README L177 / §4.1 row 8 의 "δr_d/r_d ≈ 0.7%" 는 **r_d 만 따로 본 fit-residual descriptive number** 임이 forecast 로 확정.
4. `(Planck σ × 23)` 단위 표기는 **Planck r_d 정밀도 (≈ 0.20%)** 기준 (0.7%/0.20% ≈ 3.5σ × 6.5 ≈ 23 ≈ 합당) — θ_* 정밀도 (3×10⁻⁶) 기준이 아님. 본문 명시 필요.

---

## 5. 권고 (한 줄 정직)

> **PARTIAL #6 의 0.7% 는 "r_d only" descriptive label 이며, 동일 mechanism 의 *θ_*에 대한 forward 예측* 은 Planck θ_* 와 ~10³σ 충돌한다. 따라서 paper 본문에 (a) "(Planck σ × 23)" 의 σ 가 r_d 의 σ 임을 명시, (b) 동일 채널이 θ_*에는 강하게 reject 됨을 caveat 으로 부기, (c) PARTIAL 등급은 *descriptive* level 에 한정한다고 명시 — 이 3개 보강 없이는 POSTDICTION 으로 등급 격하가 정직하다.**
