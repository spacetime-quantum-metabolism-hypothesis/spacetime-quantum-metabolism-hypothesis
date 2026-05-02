# L323 — Next step

## 핵심 finding (한 줄)

> BB 3-param 공간은 **effective dim ≈ 1 (σ_cluster stiff, 나머지 2개 sloppy)**.
> L281 Occam 12.2 와 L272 mock 100% false-rate 가 *같은* 기하로 설명된다.

## 즉시 (L324 후보)

1. **Multi-start global optimization (L272 보강)**
   - SPARC + cluster + cosmic anchor 위에 N=50 random restart minimizer.
   - chi² basin 갯수, 위치, 깊이 측정 → "global 최적합 single basin?" 검증.
   - 발견 multimodality 가 L272 false-rate 100% 의 직접 원인인지 확인.

2. **Profile likelihood along σ_cluster (stiff direction)**
   - σ_cluster fix → (σ_cosmic, σ_galactic) marginalize.
   - L323 가 예측하는 1D residual chi² curve 가 실제 surface 와 일치하는가.

3. **Sloppy reparameterization 제안 (Sec 3 신규)**
   - BB 를 (η_stiff, ξ₁, ξ₂) 직교 기저로 재표현.
   - η = σ_cluster (또는 dominant eigenvector projection),
     ξ_{1,2} = sloppy combinations.
   - 논문에서 "3 regime" 대신 "1 dominant scale + 2 nuisance combinations" 으로 정직 기술.

## 중기 (L325-L330)

- Topological data analysis on chi² landscape (persistence diagram of basins)
- Riemannian curvature scalar R(θ) along the manifold (Sloppy Sethna 후속)
- Fisher pencil eigenvector decomposition with anchor data swap
  (cosmic-only / cluster-only / galactic-only sub-Fisher → which anchors *make* stiff direction)

## 보류 / Drop

- 원래 8인 공격 vector A4 (geodesic 적분) 는 toy Hessian 에서 직선거리 = 충분.
  curved metric 은 실측 likelihood 위에서만 의미. L325+ 에서 부활.

## 등급 reflect

L323 처리 후 추정 등급 변화: ★★★★★ −0.05 → −0.048.
JCAP acceptance 변화 미미 (소수점 이하). 핵심은 *논문 narrative 정직 강화*.

## 산출물 요약

- ATTACK_DESIGN.md — 8인 공격 + 자율 분담 + protocol
- simulations/L323/run.py + report.json — 4 Hessian shape, MC cross-check
- REVIEW.md — 4인 합의, 논문 Sec 3/6 반영 의무
- NEXT_STEP.md — L324 multi-start global optimization 권고
