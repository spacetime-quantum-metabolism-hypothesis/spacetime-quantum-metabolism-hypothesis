# L333 — 4인 review (sloppy reparameterization & MBAM-style reduction)

## 측정 결과 (simulations/L333/report.json)

| shape | Occam | v_max(cluster)² | v_max(cosmic)² | v_max(galactic)² | rot(rescale) | MBAM 첫 boundary | ΔAICc(1−3, n=30) |
|-------|------:|----------------:|----------------:|------------------:|-------------:|------------------|-----------------:|
| anisotropic 100:1:1 | 12.21 | **0.806** | 0.057 | 0.137 | 0° | cosmic / prior_upper @ 2.08 | **−4.78** |
| log-uniform 1e4:1e2:1 | 12.19 | **0.977** | 0.006 | 0.017 | 0° | cosmic / prior_upper @ 2.46 | **−4.78** |
| anisotropic 1e6:1:1 | 12.19 | **0.806** | 0.057 | 0.137 | 0° | cosmic / prior_upper @ 2.07 | **−4.78** |

세 case 모두 동일한 dAICc 인 이유: chi²_min=0 일 때 AICc 차이는 자유도와
data 수만의 함수 (Burnham-Anderson). 격하 결정은 *Occam-패널티 만으로*
판정되며 fit quality 와 무관 — 이는 의도된 보수적 기준.

마지널 일치 검사 (P4): `lnV_3d − (lnV_1d_stiff + sloppy_log_vol)` =
**−1.0397** (세 케이스 모두 동일). 이는 로그 기준의 좌표 회전 보정
(eigenbasis ↔ 원좌표) 에서 발생하는 일정 항 — toy Hessian 의 alignment
효과. 0 이 아니라 *상수* 라는 점이 핵심: marginalize 와 reduce 가 동등
*형태* 이지만 prior 정의가 induce vs uniform 두 방식 차이로 ≈1 nat 만큼
어긋남. 이는 P4 KILL 이 아니라 *prior 정의 의존성* disclosure 항목.

## 4인

- **P** (Pro-BB): cluster 성분 0.806~0.977 — stiff direction 이 *물리적*
  으로 cluster scale 와 동일하다고 명명할 만큼 dominant. "BB의 본질
  자유도는 σ_cluster" 라는 해석 정당. 다만 0.806 케이스에서 galactic
  성분 0.137 도 무시 못함 — "cluster 단독" 보다 "cluster-dominant mix"
  가 더 정직.

- **N** (Nay): ΔAICc = −4.78 (n=30), −6.30 (n=13), −4.21 (n=100) — 모든
  data scale 에서 1-param 격하가 결정적 (|Δ|>2). "3 free param" 보고는
  **공식적 over-claim**. 논문 본문 본문 self-격하 의무.

- **O** (Observational): MBAM 적분이 세 케이스 모두 **cosmic 좌표가
  prior_upper 에 먼저 도달** 로 일관. 즉 sloppy direction 따라가면
  σ_cosmic 이 가장 먼저 의미를 잃는다. evaporating dof 후보는 cosmic.
  galactic 은 stiff mix 에 일부 기여 (0.137) → reduction 시 보존가치
  중간. "1-param = cluster (+galactic 잔여)" 가 가장 정직한 framing.

- **H** (Honest): P5 rotation = 0° (정확) — 선형/로그 좌표 재선택 무관.
  P4 marginal_diff = −1.04 은 induced prior vs uniform prior 차이로
  설명 가능하며, *세 case 동일* 이라는 사실이 그 진단을 뒷받침.
  L323 의 PR=1.04 / κ=100 finding 과 정량 정합 (eigenvalue ratio
  100:1:1 그대로 재현).

## 합의

> L333 은 BB 가 통계적 의미에서 **1-parameter model (stiff =
> cluster-dominant combination)** 임을 정량 확인한다. AICc 기준 격하
> 권고 (ΔAICc ≤ −4.2 across n=13~100). MBAM boundary 가 cosmic 축
> evaporation 으로 일관 — 격하 시 사실상 사라지는 자유도는 σ_cosmic.
>
> 단, "1-param" 의 *물리적* 정체는 σ_cluster 단독이 아니라 cluster
> (≈0.81~0.98) + galactic (≈0.14) 의 mix combination. 논문에서는
> "BB effective dof = 1 with cluster-dominant stiff direction" 으로
> 정직 기술.

## 논문 반영 의무 (Sec 3 / Sec 6.2 / Sec 6.4)

1. **Sec 3.x model definition**: BB 를 nominal 3-param 으로 도입하되,
   바로 다음 문단에서 "Fisher analysis (App. X = L323/L333) yields
   effective dof ≈ 1 with stiff direction dominated by σ_cluster
   (component fraction 0.81~0.98)" 명시. AICc 격하 결과 표 포함.
2. **Sec 6.2 (mock disclosure)**: L272 false-detection 100% 의 직접
   원인이 sloppy direction 임을 L323 에서 추정, L333 에서 *reduction
   가능성* 까지 확장 입증. "anchors 가 1 stiff axis 만 제약 → 다른
   2 축은 mock 노이즈에 자기조정" 으로 false-detection 메커니즘 마무리.
3. **Sec 6.4 (limitations)**: "BB 의 3-regime phenomenological
   framing 은 통계 dof 1 + nuisance 2 로 reduce 가능하지만, 본 논문은
   model space transparency 를 위해 nominal 3-param 형태를 유지하고
   reduction 결과를 disclosure" 형태 정직 기술.

## 등급 영향

- (+) AICc 기반 정량 격하 권고 — L323 sloppy 진단의 *결론* 매듭: +0.005
- (+) MBAM boundary identification (cosmic evaporation) — falsifiable
      reduction path 제공: +0.003
- (−) 마지널 prior 정의 ambiguity (P4 fail, induced vs uniform 1 nat
      gap) — disclosure 항목 추가: −0.002
- (−) "1-param" framing 으로의 격하 자체가 model claim 약화: −0.003

순 변화: **+0.003** → 등급 ★★★★★ −0.067 (L332 −0.07 대비 미세 개선).

## 가드

- **Toy Hessian 의존**: L323 와 동일. 실측 likelihood 의 reduction 여부는
  L334+ 에서 multi-start optimum chi² + profile likelihood 위에서 직접
  검증 필요. 본 격하 권고는 "Hessian local geometry 한정" 명시 필수.
- **AICc 격하 결정의 chi²_min 가정**: 본 분석은 chi²_min(3) = chi²_min(1)
  가정. 실측에서 reduced 1-param 의 chi²_min 이 +2 이상 악화되면 격하
  취소. 즉 *통계 패널티 만으로* 격하한 것이며 적합도 보존 검증 필수.
- **"1-param 의 물리 정체" 단정 금지**: cluster 성분 0.806~0.977 은
  stiff direction 이 cluster-dominant 이라는 *통계적 사실*. "cluster
  scale 이 SQMH 의 본질 dof" 류 물리 해석은 별도 동역학적 근거 필요.
- **Boundary identification (cosmic evaporation)**: prior box 와 LCDM
  cutoff 위치에 의존. cutoff −3 → −5 sweep 시 boundary 좌표 보존되는지
  L334 에서 재확인 권고.
- **prior 정의 P4 gap 1 nat**: induced prior on η vs uniform prior on
  (cosmic, cluster, galactic) 의 표준 차이. 두 정의 모두 논문 부록 보고.
