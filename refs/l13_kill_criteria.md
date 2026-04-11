# refs/l13_kill_criteria.md -- L13 Kill/Keep Criteria (FROZEN before execution)

> Date: 2026-04-11. Fixed before any L13 computation.
> These criteria are immutable. Results must be reported honestly against them.

---

## L13 KILL Conditions

| ID  | Condition | Implication |
|-----|-----------|-------------|
| K81 | Full SQMH ODE numerical Δchi² = A01 Δchi² ± 0.5 | A01 approximation sufficient. First-order approximation justified. |
| K82 | Ωm amplitude comes only from normalization condition (not theory structure) | Amplitude derivation fails. Must note "amplitude locking = normalization artifact" in paper. |
| K83 | wa theoretical correction < 0.1 | Perturbation theory cannot close wa gap. |
| K84 | New angle also gives Γ₀ range > 20 orders, σ=4πGt_P also lacks basis | NF-27 fully confirmed. Both parameters lack theoretical basis. |
| K85 | DR3 Fisher: A01 vs ΛCDM discrimination SNR < 2σ | DR3 cannot arbitrate. Euclid/CMB-S4 required. |
| K86 | A01 is statistically indistinguishable from arbitrary 1-parameter model with wa<0 | No SQMH uniqueness. Piggyback model confirmed. Full repositioning needed. |

## L13 KEEP Conditions

| ID  | Condition | Implication |
|-----|-----------|-------------|
| Q81 | Full ODE Δchi² > A01 + 2 | Terms missing in first-order approximation. Full ODE as paper main result. |
| Q82 | Ωm amplitude theoretically derived from SQMH equation structure | "Ωm is theory prediction" can be added as paper core claim. |
| Q83 | wa theoretical correction ≥ 0.3 (DESI direction) | wa gap partially resolved theoretically. Paper §3 upgrade. |
| Q84 | Either Γ₀ or σ=4πGt_P has at least partial theoretical basis | Fundamental motivation partially resolved. Paper §2 strengthened. |
| Q85 | DR3 Fisher: specific z-bin SNR ≥ 3σ | Clear verification timeline. Paper §5 addition. |
| Q86 | SQMH uniquely determines Ωm amplitude without free parameters | "Not coincidence" established. SQMH uniqueness secured. Paper core strength. |

---

## Reference Values (from L5 MCMC production run)

- A01 best-fit: Om = 0.3102, h = 0.6771
- A01 chi2_at_mean = 1655.78
- LCDM chi2 = 1676.89
- A01 Δchi² vs LCDM = -21.12 (improvement)
- A01 wa (CPL fit from L11): approximately -0.133

## Thresholds for L13-O

- K81 triggers if: |chi2_full_ODE - chi2_A01| ≤ 0.5
- Q81 triggers if: chi2_full_ODE < chi2_A01 - 2.0 (full ODE better by 2+)
