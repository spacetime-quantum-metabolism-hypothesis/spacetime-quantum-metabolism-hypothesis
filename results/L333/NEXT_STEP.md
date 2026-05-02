# L333 — Next step

## 핵심 finding (한 줄)

> BB 의 stiff direction 은 **cluster-dominant (0.81~0.98) + galactic (~0.14)
> mix combination**. ΔAICc(1−3) ≤ −4.2 (n=13~100) → 1-param 공식 격하 권고.
> MBAM 적분 시 첫 evaporating 좌표는 σ_cosmic — sloppy 채널의 물리적 출구.
> 격하 후 framing: "BB effective dof = 1 with cluster-dominant stiff axis".

## 즉시 (L334 후보)

1. **실측 likelihood 위 reduction 검증**
   - SPARC + cluster + cosmic anchor 실측 chi²(σ) 위에서 v_max 1D
     projection 적합도 측정.
   - chi²_min(reduced) − chi²_min(full) ≤ +2 이면 격하 확정.
   - +2 초과 시 "통계적 reduction 가능 but 적합도 손실" 로 disclosure 만.

2. **Profile likelihood along v_max** (L323 NEXT_STEP 잔여)
   - η = v_max·θ 고정 → (ξ₁, ξ₂) marginalize.
   - 1D residual chi² curve 가 toy 예측과 일치하는지 정량.
   - 두 sloppy 좌표가 진짜 *flat* 인지 (mock 100% false-rate 직접 원인)
     실측 confirmation.

3. **MBAM boundary cutoff sweep**
   - LCDM cutoff −3 → {−2, −4, −5} sweep 에서 첫 evaporation 좌표 보존?
   - prior box halfwidth 도 1.0 / 3.0 로 변형해 boundary 식별 robust.

4. **Reduced model 의 prior 정의 확정**
   - induced prior on η (3D uniform 의 marginal) vs uniform prior on η
     두 가지 모두 evidence 계산 → 1 nat gap 의 공식 보고.

## 중기 (L335-L340)

- **물리 해석 재검토**: "cluster-dominant stiff" 가 SQMH 동역학에서
  *왜* 그러한지 (= 어떤 anchor 가 그 방향을 stiff 하게 만드는가)
  Fisher pencil sub-Hessian decomposition (cosmic-only / cluster-only /
  SPARC-only) 으로 추적. L323 가드 항목.
- **Topological data analysis** (L323 NEXT_STEP 잔여): persistence diagram
  으로 1-stiff + 2-soft 구조가 chi² landscape 의 *전역* 위상에 반영되는지.
- **격하 결정 의무화**: L334 결과가 chi²_min 보존이면 Sec 3 BB 정의를
  공식적으로 1-param 으로 rewrite (paper revision Pass 2).

## 보류 / Drop

- "Riemannian curvature scalar" (L323 NEXT_STEP) 은 toy Hessian 위에서
  trivial (constant metric → R=0). 실측 likelihood 위에서만 의미.
- "Sloppy direction 의 microphysics 명명" (예: galactic 성분 0.14 의
  의미) — 본 loop 격하 결정에 불필요. 논문 본문 외 부록 정도로만.

## 등급 reflect

L333 처리 후 추정 등급: ★★★★★ −0.07 → −0.067 (Δ +0.003).
JCAP acceptance 91-95% 변화 미미. 핵심은 **"BB 가 본질적 1-param 모델"
이라는 정직한 model 격하 권고를 데이터 (L323 + L333) 로 정량 뒷받침**.

논문 narrative 변화: "3-regime BB" → "1-parameter cluster-dominant model
with phenomenological 3-regime decomposition for interpretability".
이것이 L333 의 진짜 산출물.

## 산출물 요약

- ATTACK_DESIGN.md — 8인 자율 분담 + protocol (수식·파라미터 미주입)
- simulations/L333/run.py + report.json — Fisher eigendecomp + MBAM +
  AICc(1) vs AICc(3)
- REVIEW.md — 4인 합의, 1-param 격하 권고 + cluster-dominant
  framing 재정의
- NEXT_STEP.md — L334 실측 likelihood reduction 검증 권고
