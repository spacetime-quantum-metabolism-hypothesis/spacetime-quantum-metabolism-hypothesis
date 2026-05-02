# L273 — Hierarchical Bayesian per-tracer (deferred from L254)

## 8인 공격
A1: "단일 σ_0 가 SPARC + cluster + cosmic anchor 동일하다는 가정 — hierarchical 검증 필요."
A2: "Per-galaxy σ_0 변동성 → hyper-prior 명시."
A3: "Population-level shrinkage 적용 시 Branch B 3-regime 유지?"
A4: "Hyper-parameter posterior — broad? localized?"
A5: "Stan/PyMC convergence Rhat<1.01."
A6: "Hierarchical 후 ΔAICc 어떻게 변하나."
A7: "Empirical Bayes vs full hierarchical."
A8: "DIC posterior averaging."

## Top 3
A3 (regime survival), A6 (ΔAICc revision), A2 (per-galaxy variance)

## 다음 권고
SPARC per-galaxy σ_0 fit + Gaussian hyper-prior μ, τ → posterior 로 3 mode 검출 시 BB confirm.
