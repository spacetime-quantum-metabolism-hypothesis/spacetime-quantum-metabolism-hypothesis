# L328 — 4인 review (Bayes factor subset stability, analytic)

## 분석 (선행 결과 기반 추론, simulations 미실행)
입력:
- L196 fixed-θ Akaike weight (BB) ≈ 100% — full joint, no Occam.
- L281 marginalized ΔlnZ (full joint) = +0.8 (Laplace, BB 3-param vs smooth 5-param).
- L276 LOO-CV ΔAICc:
  - full: ≫ 0 (BB 강우위)
  - leave-cluster-out: 56
  - leave-cosmic-out: 89
  - leave-galactic-out: 41
  - 2-out: 5–15 (임계)
  - 3-out (= SPARC only): 0

## ΔAICc → ΔlnZ heuristic
Laplace 에서 −2 lnZ ≈ χ²_min + k ln(2π σ_eff² /Δθ²) + const.
AICc 와 marginalized lnZ 차이는 prior-volume 의존 Occam term.
L281 에서 측정된 Occam penalty:
  fixed-θ (≈ AICc-식) ΔlnZ ≈ +13 → marginalized +0.8.
  ΔOccam ≈ −12.2 (BB 3-param + smooth 5-param 합산).
같은 penalty 를 subset 별로 적용 (likelihood 만 변함, prior 동일):

| Subset            | ΔAICc | ΔAICc/2 (≈fixed-θ ΔlnZ) | marginalized ΔlnZ ≈ ΔAICc/2 − 12.2 |
|-------------------|-------|---------------------------|-----|
| Full joint        | ~26   | +13                       | **+0.8** (L281 측정값)          |
| Leave-cluster-out | 56    | +28                       | **+15.8** (?? 모순)              |
| Leave-cosmic-out  | 89    | +44.5                     | +32.3                            |
| Leave-galactic-out| 41    | +20.5                     | +8.3                             |
| SPARC only (3-out)| 0     | 0                         | **−12.2**                        |

→ 위 표의 leave-X-out 행이 full 보다 *큰 ΔlnZ* 인 것은 L276 ΔAICc 정의가
"LCDM AICc − BB AICc" 로 anchor 의 χ² 잔차에 따라 달라지기 때문 (single anchor
제거 시 LCDM 부담 감소량 vs BB 부담 감소량). 즉 ΔAICc=56 은 anchor 1 개만 빠진
상태에서 *남은* 우주 데이터의 BB 우위. full joint 가 +13 (fixed-θ) 인데 1-out
이 +28 처럼 더 클 수는 없으므로 L276 표의 *정의가 다름* (LOO log-likelihood
sum 일 가능성). 이 모순은 L276 표 재정의 필요 — REVIEW 에 정직 기록.

## 안정한 두 끝점 (모순 없는 부분)
- **Full joint marginalized ΔlnZ = +0.8** (L281, 정량).
- **SPARC-only (3-out) ΔAICc = 0** → BB 와 LCDM 구분 불가.
  prior 부피 동일하면 marginalized ΔlnZ ≈ −Occam penalty (BB 가 *disfavored*).

이 두 끝점만으로 결론은 명확:
**ΔlnZ 가 subset 에 따라 크게 변한다.** SPARC-only 에서는 음수 영역.
Full joint 에서는 +0.8 (weak positive). 차이 |Δ(ΔlnZ)| ≳ 10.

## 4인
- P: 두 끝점 차이 ≳ 10 → 명백한 subset-specific. global 주장 불가.
- N: L276 1-out ΔAICc 표 정의 모호 — L328 본 시뮬에서 동일 likelihood pipeline 으로
  재계산 필요. heuristic 표 (위) 인용 시 caveat 명시.
- O: 논문 본문에 "BB 우위는 anchor 다중성에 의존, SPARC 단독으로는 LCDM 등가"
  명시. Akaike weight 100% / ΔlnZ=+0.8 둘 다 *full joint conditional* 표기.
- H: L208 anchor caveat + L276 결론 + L281 격하와 완전 일관. 새 정보가 아니라
  *재확인*. paper 에 재확인 한 줄 추가.

## 정직 한 줄
**ΔlnZ 는 subset-specific. SPARC only ≈ −Occam penalty (음수), full joint ≈ +0.8 — BB
우위는 3 anchor (cluster, galactic, cosmic) 의 leverage 에서만 발생.**
