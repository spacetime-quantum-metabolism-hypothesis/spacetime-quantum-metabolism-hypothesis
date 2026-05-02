# L327 — ATTACK DESIGN: Systematic uncertainty inflation

## 공격 목표
L208 ΔAICc=99.49 의 BB 우위는 anchor χ² (=103.61) 가 100% 제공.
anchor σ 가 underestimated 되어 있다면 ΔAICc 는 spurious. 인플레이션
factor f ∈ {2, 5, 10} 에서 BB 우위가 살아남는지 정량 평가.

## 가설 (8인 자유도 분담)

### A1. Anchor σ inflation
σ_anchor → f·σ_anchor → χ²_anchor(LCDM) → 103.61/f². ΔAICc(f) = 103.61/f² − pen_diff.

### A2. SPARC log_a0 σ inflation
SPARC χ² 두 모델 동일 (universal a0). σ_intrinsic 인플레이션은 ΔAICc invariant
하지만 absolute χ²/dof 는 변함 — SPARC fit 자체 신뢰성 점검.

### A3. Combined inflation
anchor + SPARC 둘 다 inflation. 4×4 grid. ΔAICc 가 anchor factor 에만 의존
하면 SPARC 잡음은 무관함을 정량 확인.

### A4. Error model misspecification
anchor residual 분포가 가우시안이 아닐 가능성. cluster anchor (A1689) 가
χ² 의 ~98% 차지 (z_cluster ≈ 10σ). 이는 outlier 가능성 시사.

### A5. Robust statistics
Huber loss (k=1.345): outlier 영향 캡. 큰 residual 을 linear 로 truncate.
Tukey biweight: outlier 완전 제외. cluster anchor 단일 outlier 시 ΔAICc 붕괴 가능성.

## 임계값 분석
f_crit 는 다음을 만족하는 inflation factor:
- ΔAICc = 10 (학계 conventional cutoff)
- ΔAICc = 2 (marginal)
- ΔAICc = 0 (tie)

## 산출
- `simulations/L327/run.py` — 4-factor scan + 4×4 combined + robust stats
- `results/L327/report.json` — 모든 수치
- `REVIEW.md` — 4인 평가
- `NEXT_STEP.md` — 후속 액션
