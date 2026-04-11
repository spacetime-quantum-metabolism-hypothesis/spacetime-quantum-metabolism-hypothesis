# L3 Kill / Keep Criteria — Frozen 2026-04-11

**Commit**: 이후 변경 금지. 사후 조정 시 L3 테스트 무효.

## KILL conditions (any one → immediate exclusion)

| ID | Condition | Threshold |
|---|---|---|
| K1 | BAO+SN+CMB+RSD joint Δχ² vs LCDM best-fit | > +4.0 (95% CL) |
| K2 | \|w_a\| amplitude vs DESI central 0.83 | < 15% i.e. \|w_a\| < 0.125 |
| K3 | Phantom crossing (w(z) crosses -1) | SQMH L0/L1 sign rule violation |
| K4 | Numerical recomputed Cassini \|γ-1\| | > 2.3e-5 |
| K5 | Reproducibility drift with fixed seed | > 1e-3 in χ² or w_a |
| K6 | SQMH L0/L1 invariants (σ=4πG·t_P, Γ₀) silent modification | auto-fail |
| K7 | Linear perturbation ghost / gradient (c_s² < 0) | auto-fail |
| K8 | CLASS/CAMB-level implementation numerical blow-up | auto-fail |

## KEEP conditions (all must hold → Phase 5 entry)

| ID | Condition |
|---|---|
| P1 | K1-K8 all clear |
| P2 | Δχ² ≤ 0 **or** theoretical consistency score ≥ 8/10 (direct SQMH L0/L1 link) |
| P3 | Python reproducibility complete (seed, data paths, pinned deps) |
| P4 | Explicit linear perturbation theory (linear + 1st order) written |
| P5 | CLASS/CAMB-level Boltzmann implementation (hi_class branch or custom Python) |

## LCDM baseline (reference point for Δχ²)

Phase L3-A, fixed once at the start of execution. Stored in
`simulations/l3/lcdm_baseline.json`.

## Phase 5 entry count

Not capped. All candidates satisfying P1-P5 are promoted. If no candidate
survives, `paper/negative_result.md` appendix is written.

## Notes on threshold rationale

- K1 = +4.0 (2-σ). Stricter would prematurely kill C26/C32 which have
  weak fit but high theoretical consistency.
- K2 = 15%. Keeps C28 (Dirian 2015 |w_a|≈0.19) in contention.
- K3 = phantom crossing. Matter→DE metabolism sign rule (L0/L1).
- K4 = numerical PPN recomputation, not analytic proof.
