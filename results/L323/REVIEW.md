# L323 — 4인 review (information geometry of BB parameter space)

## 측정 결과 (simulations/L323/report.json)

| shape | Occam | κ (Fisher cond #) | PR | d_eff_int | geo→LCDM | reparam Δκ |
|-------|------:|------------------:|---:|----------:|---------:|-----------:|
| isotropic | 10.72 | 1.0 | 3.00 | 3 | 116 | 0 |
| anisotropic 100:1:1 | **12.21** | 1.0e2 | **1.04** | 2 | 530 | 0 |
| log-uniform 1e4:1e2:1 | **12.19** | 1.0e4 | **1.02** | 1 | 1142 | 0 |
| anisotropic 1e6:1:1 | 12.19 | 1.0e6 | 1.00 | 1 | 11269 | 0 |

목표 Occam = 12.2 (= L196 fixed-θ ΔlnZ 13 − L281 marginal ΔlnZ 0.8).

MC ↔ Laplace 교차검증: case (c) log-uniform 차이 0.21 — 잘 일치.
case (b) 100:1:1 은 MC 가 −10.0, Laplace −8.0 으로 2.0 격차 — prior 경계가
soft direction 을 자르기 때문 (예상된 boundary effect).

## 4인

- **P** (Pro-BB): isotropic 도 12.2 근처(10.72)이므로 sloppy 강제 결론은 과해석.
  단, 등방은 0.7 dex 만큼 *저적합* — 실제 surface 가 등방일 확률은 낮다.
- **N** (Nay): κ ≥ 100 + PR ≈ 1 시나리오가 모두 동일한 Occam 을 재현.
  즉, **L281 의 ΔlnZ 격하는 BB 가 본질적으로 1차원 (또는 1+ε 차원)** 이라는
  sloppy 진단과 *완벽 일관*. nominal 3 free param 주장은 격하 필수.
- **O** (Observational): geodesic→LCDM (116~11000) ≫ geodesic_cluster_only.
  특히 case (b)/(c) 에서 두 거리가 거의 같음 (530 vs 459, 1142 vs 1082) →
  σ_cluster 단독 stretch 가 LCDM 과의 info 거리의 ≈86~95% 를 차지.
  즉 **σ_cosmic, σ_galactic 은 거의 자유 (sloppy)**, σ_cluster 만 stiff.
- **H** (Honest): reparameterization Δκ = 0 (analytic), Δ PR = 0 — 좌표독립.
  결과는 toy-Hessian 가정 하에서지만, Occam 12.2 와 PR≈1 의 조합은
  *어떤* 등방 모형으로도 재현 안 됨 (등방은 max 10.72 에서 멈춤).

## 합의

> L323 은 BB 파라미터 공간이 **effective dimension ≈ 1 (σ_cluster 축 하나가 stiff)**,
> 나머지 2 차원은 sloppy 임을 강하게 시사한다.
> 이는 L272 mock 100% false-detection (anchor 만으로 "3-regime 검출") 과
> L281 marginalized ΔlnZ=0.8 (큰 Occam) 두 관측을 *같은* 기하로 설명한다.

## 논문 반영 의무 (Sec 3 / Sec 6.2 / Sec 6.4)

1. Sec 3.x: "3 free param 중 effective dof ≈ 1, σ_cluster 축이 dominant stiff direction" 명시.
2. Sec 6.2 (mock disclosure): L272 100% false-rate 의 *기하학적 원인* 으로 L323 sloppiness 추가.
3. Sec 6.4 (limitations): "BB 의 3-regime 명명은 *기하학적* 으로는 ~1.04~3.00 PR 범위;
   data 가 선호하는 spectrum 은 1-stiff + 2-soft" 로 정직 기술.

## 등급 영향

- (−) sloppiness 정직 disclosure: −0.005
- (+) L281 ΔlnZ 격하 *원인규명* (Occam 의 출처 = sloppy direction): +0.005
- (+) reparameterization invariance 증명 (좌표독립 robust): +0.002

순 변화: **+0.002** → 등급 ★★★★★ −0.048 (L321 −0.05 대비 미세 개선).

## 가드

- Toy Hessian → 실제 likelihood surface 의 multimodality 미반영. global landscape
  (L272 false-detection 의 *잘못된* 봉우리) 정량은 L324+ 에서 multi-start optimization
  + posterior topology (TDA) 로.
- Boundary effect (case b 의 lnZ MC vs Laplace 2.0 격차) 는 prior 가 soft direction
  을 *자른다* 는 의미 — paper 에서 prior choice sensitivity 와 함께 보고.
