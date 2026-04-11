# L4 Kill / Keep Criteria — Frozen 2026-04-11

**Commit**: 이후 변경 금지. 실행 도중 임계값 조정 시 L4 테스트 무효.

## Inherited from L3 (K1-K8)

See `refs/l3_kill_criteria.md`.

| ID | Condition | Threshold |
|---|---|---|
| K1 | BAO+SN+CMB+RSD joint Δχ² vs LCDM best-fit | > +4.0 |
| K2 | \|w_a\| amplitude | < 0.125 |
| K3 | Phantom crossing | any |
| K4 | Cassini \|γ-1\| | > 2.3e-5 |
| K5 | Reproducibility drift | > 1e-3 |
| K6 | L0/L1 silent modification | auto-fail |
| K7 | c_s² < 0 or gradient | auto-fail |
| K8 | Boltzmann blow-up | auto-fail |

## L4 new KILL conditions

| ID | Condition | Threshold |
|---|---|---|
| K9  | MCMC non-convergence (R̂ on any param) | > 1.05 auto-fail |
| K10 | Full-Boltzmann w_a sign disagrees with L3 toy | auto-fail (toy misleading) |
| K11 | Perturbation c_s² < 0 or ghost dof | auto-fail |
| K12 | 2-D (w0, w_a) posterior contains LCDM within 2σ | marginal KILL |

## L4 KEEP conditions (Phase 5 entry = paper main candidate)

| ID | Condition |
|---|---|
| Q1 | K1-K12 all clear |
| Q2 | MCMC 2σ posterior excludes LCDM **or** Δχ² ≤ -6 |
| Q3 | Full-Boltzmann and toy w0, w_a sign + magnitude consistent |
| Q4 | Linear perturbation ODE explicit + c_s² > 0 proof |
| Q5 | Numerical Cassini \|γ-1\| < 2.3e-5 |
| Q6 | SQMH L0/L1 direct interpretation (theory score ≥ 6/10) |

**Phase 5 entry target: 2-3 main candidates**. Tie-break by theory score.

## LCDM baseline reference

χ²_total = 1676.89 at (Ω_m=0.3204, h=0.6691), rd=147.09, ω_b=0.02237.
From `simulations/l3/lcdm_baseline.json`. Reused for L4 without refit.
