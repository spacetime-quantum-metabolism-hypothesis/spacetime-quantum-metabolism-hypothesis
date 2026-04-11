# refs/l10_kill_criteria.md -- L10 Kill / Keep Criteria (Fixed Before Execution)

> Date: 2026-04-11
> Status: FIXED before any L10 execution. Do not modify after execution begins.
> Source: base.l10.command.md

---

## L10 KILL Conditions (K51-K58)

| ID | Condition | Trigger Value | Result if Triggered |
|----|-----------|--------------|---------------------|
| **K51** | Stochastic SQMH: CSL/Langevin with diffusion term nabla^2 n does NOT produce erf at any noise level eta | All eta in [0, 1e-30] SI: erf fit R^2 < 0.90 | Extended SQMH also erf-impossible. Paper: "erf impossible in all SQMH variants." |
| **K52** | Nonlinear halo SQMH correction < 1e-60 | SQMH correction to halo mass function < 1e-60 (62-order suppression persists even in dense halos) | Nonlinear channel eliminated. Paper limitations updated. |
| **K53** | C28 CMB-S4 detectability SNR < 1 | Expected SNR for G_eff/G = +2% signal < 1-sigma in CMB-S4 Fisher | NF-22 downgraded. C28 future verification channel closed. |
| **K54** | DESI DR3 mock: A12 Delta ln Z < 5.0 | 90% CI lower bound of predicted Delta ln Z(A12, DR3) < 5.0 | A12 data support weakening. Paper caveat added. |
| **K56** | UV completion: no QG framework (LQC/GFT/CDT) derives sigma = 4*pi*G*t_P | 8-person team consensus: no structural derivation found | sigma confirmed as phenomenological parameter. UV channel closed. |
| **K57** | Gamma_0 origin: dS temperature, Hawking, holography all fail to constrain | No scale matching within 2 orders of magnitude | Gamma_0 is a free parameter. Paper limitations updated. |
| **K58** | sigma RG running: all QG corrections give Delta_sigma/sigma < 1e-60 | AS G(k) and LQC holonomy corrections give sigma running < 62-order gap | sigma running cosmologically irrelevant. NF-1 hypothesis retired. |

---

## L10 KEEP Conditions (Q51-Q58)

| ID | Condition | Trigger Value | Result if Confirmed |
|----|-----------|--------------|---------------------|
| **Q51** | Stochastic SQMH with diffusion term produces erf-like profile | erf fit R^2 > 0.90 at some eta_crit | Paper Section 2 updated: "Extended SQMH -> erf possible." New research direction. |
| **Q52** | Nonlinear halo SQMH correction > 1e-50 | Halo correction > 1e-50 (structural departure from linear) | Nonlinear channel new result. Paper discussion added. |
| **Q53** | C28 CMB-S4: G_eff/G = +2% detectable SNR > 2 | Expected SNR > 2-sigma in CMB-S4 Fisher forecast | C28 "uniquely verifiable by CMB-S4" claim established. |
| **Q54** | DESI DR3 mock: A12 Delta ln Z > 8.0 | Predicted Delta ln Z(A12, DR3) > 8.0 at median | DR3 verification preparation complete. "Testable prediction" claim added. |
| **Q56** | UV partial success: any QG framework gives structural derivation of sigma value | At least one approach (LQC/GFT/CDT) gives sigma within factor 10 of 4*pi*G*t_P | Paper Section 2 UV motivation strengthened. "Structural similarity -> derivability." |
| **Q57** | Gamma_0 scale confirmed: dS temperature or holography matches Gamma_0/sigma ~ Planck density | Scale match within 2 orders of magnitude | Paper: "Gamma_0 has natural scale from Planck thermodynamics." |
| **Q58** | sigma RG running cosmologically relevant: Delta_sigma/sigma > 1e-50 in some energy regime | Running exceeds 50-order gap in nonlinear/early universe regime | sigma running new channel. NF-1 upgraded from SPECULATIVE. |

---

## Notes

- K55 is omitted per L9 verdict (absorbed into K54 scope).
- All criteria are fixed at 2026-04-11 before execution. Anti-cherry-picking: criteria cannot be weakened post-hoc.
- Language standard: refs/l7_honest_phenomenology.md applies to all L10 results.

---

*Fixed: 2026-04-11. L10 execution begins after this file is saved.*
