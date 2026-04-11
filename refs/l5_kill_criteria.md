# L5 Kill / Keep Criteria — frozen 2026-04-11

Inherits all L4 criteria (K1-K12) from `refs/l4_kill_criteria.md`.

## L5 NEW KILL criteria

| ID  | Condition | Threshold |
|-----|-----------|-----------|
| K13 | Production MCMC R̂ > 1.02 on any parameter (48 walkers × 2000 steps, burn 500, thin 10) | auto-fail |
| K14 | log Bayesian evidence Δ ln Z = ln Z − ln Z_LCDM < −1 (decisive against on Jeffreys' scale) | KILL |
| K15 | Cosmic shear S_8 posterior mean > 0.84 (exceeds DES-Y3 3σ upper bound) | KILL |
| K16 | Alt-20 SVD principal analysis: candidate is a linear combination of other alt candidates at the ≥ 99% variance level | cluster merge (not a KILL for survivors — only for selecting class representative) |

## L5 NEW KEEP criteria (submission-ready)

| ID  | Condition |
|-----|-----------|
| Q7  | K1-K16 all pass (or K16 merged via cluster representative selection) |
| Q8  | Δ ln Z ≥ +2.5 (substantial on Jeffreys' scale) |
| Q9  | DESI DR3 Fisher forecast: ≥ 2σ separation from LCDM on w_a axis |
| Q10 | Cosmic shear joint χ² ≤ (BAO+SN+CMB+RSD) χ² + 3 (no catastrophic growth-sector penalty) |
| Q11 | H₀ tension vs SH0ES (h=0.732) not worsened by more than 0.005 (|Δh_tension| ≤ +0.005) |
| Q12 | Theoretical interpretation document `paper/l5_<ID>_interpretation.md` completed |

## Jeffreys' scale (for K14 / Q8)

| Δ ln Z range | Verdict |
|--------------|---------|
| > +5         | strong support |
| +2.5 to +5   | substantial (Q8 threshold) |
| +1 to +2.5   | weak |
| −1 to +1     | inconclusive |
| < −1         | decisive against (K14 KILL) |

## L5 target candidate list

**Tier 1 Mainstream (2)**: C28 Maggiore RR, C33 f(Q).
**Tier 2 Alt-hard (4)**: A01, A05, A12, A17.
**Tier 3 Re-evaluation (2)**: C11D Disformal IDE, C26 Perez-Sudarsky.
**Tier 4 Alt-soft degenerate class (9)**: A03, A06, A08, A09, A11, A13, A15, A16, A19, A20 — class reduction via SVD (L5-F).
**Excluded**: A02, A07, A10, A14, A18 (L2/L3 killed); A04 (K2-OK w_a=-0.469 but Δχ²=-8.89 weak) kept as outlier in cluster analysis only.

Submission winner target: 1-3 candidates.
