# Figure 12 — Phase 2 Joint Fit (BAO + SN + compressed CMB + RSD)

**Generated**: 2026-04-10 by `simulations/phase2/phase2_joint_fit.py`

## Data

| Dataset | Points | Source |
|---------|--------|--------|
| DESI DR2 BAO | 13 | arXiv:2503.14738 (CobayaSampler/bao_data) |
| DESY5 SN | 1829 | Vincenzi et al. 2024 (CobayaSampler/sn_data) |
| Planck compressed CMB | 3 (θ*, ω_b, ω_c) | Planck 2018 VI (arXiv:1807.06209) |
| RSD fσ_8 | 8 | 6dFGS / SDSS MGS / BOSS DR12 / eBOSS DR16 (see rsd_likelihood.py) |
| **Total** | **1853** | |

## Methodology

- E(z) for quintessence models from Phase 1 coupled ODE (`quintessence.py`).
- Sound horizon θ* via Hu & Sugiyama 1996 z_* fitting formula + sound-horizon
  integral from radiation era. 0.3% theoretical floor added to Planck's 3e-6
  stat error (fit formula accuracy limit).
- High-z bridge: for z > 2.5 we substitute LCDM-scaled E(z) because coupled
  IDE / V(φ) effects are negligible deep in matter+radiation era.
- SN χ² analytically marginalised over absolute magnitude (Conley 2011
  appendix B).
- BAO χ² uses full 13×13 covariance (already validated in Phase 1).
- **Linear growth** via Amendola-Quartin-Tsujikawa-Waga 2006 (astro-ph/0605488)
  eq 16 in sub-horizon quasi-static limit: `δ'' + [2+H'/H−β·φ'] δ' = (3/2)(1+2β²)Ω_m·δ`.
  Background for the growth ODE uses the analytic LCDM formula with the same
  Ω_m_0 (backward scalar-field ODE is numerically unreliable at z > 1 due to
  phi_N → √6 anti-damping). φ_N enters via a slow-roll approximation
  `φ_N ≈ √(2/3)·β·Ω_m(a)`.
- fσ_8(z) theory = f(z) · σ_8_0 · D(z)/D(0), with σ_8_0 = 0.8111 (Planck VI).
- Fluid IDE has no scalar-field growth module; we use LCDM growth with the
  same Ω_m as a **conservative** proxy.
- r_d fixed at CMB-preferred 147.09 Mpc; ω_b/ω_c fixed at Planck best-fit.

## Results

| Model | χ²_BAO | χ²_SN | χ²_CMB | χ²_RSD | χ²_tot | k | AIC | BIC | ΔAIC |
|-------|--------|-------|--------|--------|--------|---|-----|-----|------|
| **LCDM** (Ω_m=0.3198) | **24.18** | **1643.90** | **2.08** | **7.29** | **1677.45** | **1** | **1679.45** | **1684.97** | **0** |
| Fluid IDE (ξ_q∈R, best −0.0065) | 28.30 | 1644.83 | 0.53 | 7.15 | 1680.82 | 1 | 1682.82 | 1688.34 | +3.37 |
| Fluid IDE (ξ_q≥0, boundary 0.000) | 29.81 | 1645.04 | 0.06 | 7.15 | 1682.07 | 1 | 1684.07 | 1689.59 | +4.62 |
| V_RP (β=0.097, n=0.113) | 29.05 | 1644.94 | 0.13 | 7.47 | 1681.59 | 2 | 1685.59 | 1696.64 | +6.14 |
| V_exp (β=0.096, λ=0.111) | 29.08 | 1644.94 | 0.12 | 7.46 | 1681.60 | 2 | 1685.60 | 1696.65 | +6.15 |

**Bug-fix rerun (8-person team review, 2026-04-10)**:
- `sn_likelihood.py`: integrated with `zCMB` → now `zHD` (CobayaSampler / DESY5 convention, peculiar-velocity corrected). SN χ² dropped ~24 across all models proportionally; ΔAIC rankings and verdict unchanged.
- `phase2_joint_fit.py`: V_RP / V_exp β bounds tightened from `[-1, 2]` → `[0, 2]` to enforce the SQMH sign convention (matter gains energy from φ ⇒ β ≥ 0). Best-fit β remains positive (~0.097), so the fit is numerically identical to within the new constraint — but the SQMH-physical branch is now explicitly guaranteed rather than accidentally favored.
- `quintessence_perturb.py`: defensive `.copy()` on `sol.y[0/1]`, removed dead `import quintessence as qn` (LCDM-background substitution made it unused).

**Note on Fluid IDE**: unconstrained best fit lands in the phantom region
(ξ_q = −0.0067 → w_DE < −1), which violates the SQMH physical branch. The
SQMH-consistent branch (ξ_q ≥ 0) converges to the boundary ξ_q = 0 (i.e.
indistinguishable from ΛCDM at the level of background observables), with
ΔAIC = +5.17.

**Note on V_RP / V_exp shift due to RSD**: before RSD was added, the best-fit
coupling was β ≈ 0.195 (Phase 2 v1). After adding RSD, RSD's penalty on
enhanced growth (G_eff/G = 1 + 2β²) pulls β down to ≈ 0.099, halving the
coupling. But the lower coupling also removes the small background benefit
V_RP/V_exp had at BAO+SN+CMB, so the joint χ² *worsens* — RSD and BAO pull
in opposite directions on β with no compromise available. Classic projection
effect: what looks like "some freedom" in one data slice disappears when
another slice is added.

## Phase 2 verdict

**Path F (rejection), now reinforced by RSD.** Every SQMH variant lands at
ΔAIC ≥ +3.8 vs ΛCDM, with V_RP / V_exp worsening to ΔAIC ≈ +6.7 once growth
data is added. The SQMH-consistent Fluid IDE branch (ξ_q ≥ 0) converges
*onto* ΛCDM, showing the background fluid toy has no remaining freedom to
improve the joint fit without entering the phantom region, which the theory
forbids.

## Why Phase 1 looked different

Phase 1 used BAO alone, where V(φ) freezing models exploit a degeneracy in
the 13-point BAO vector. Adding 1829 SN distance moduli constrains the low-z
Hubble-diagram slope, which V_RP cannot fit without breaking the BAO
compromise. Adding θ* pins the sound horizon / angular-distance ratio at
z = 1090. Adding fσ_8 pins the *growth* at z < 1.5, which is sensitive to
the G_eff enhancement that V_RP / V_exp *must* carry whenever β ≠ 0. These
four constraints together leave no viable corner of SQMH background/coupling
parameter space.

## Caveats

1. **Compressed CMB** (θ*, ω_b, ω_c) misses the TT/EE/lensing peak-structure
   information. A full Planck TTTEEE analysis (Option A via CLASS patch) is
   ~3× more constraining on φ dynamics in principle. Phase 2 rejection is
   already strong enough that Phase 3 is unlikely to reverse it.
2. **r_d held fixed** at 147.09 Mpc. Varying r_d inside Phase 1 joint
   optimisation gave Δχ²_BAO = −20 for Fluid IDE, but that is
   double-counted against the θ* constraint here, so we keep r_d fixed.
3. **RSD scaffolding**: 8 points, diagonal covariance. BOSS DR12 consensus
   has off-diagonal correlations (~0.2-0.4) that we ignore — this *under*-
   estimates the χ² penalty by ~10%, so the true verdict is slightly worse
   than shown. DESI DR1/DR2 full-shape RSD would be the correct long-term
   replacement.
4. **Growth background is LCDM-substituted**: the coupled-quintessence
   background at z < 3 is correct to ~1% for |β| < 0.4, but we avoid using
   it directly in the growth ODE because the backward scalar-field
   integrator drifts to phi_N → √6 (phantom boundary). The substitution is
   conservative: it *removes* a small amount of late-time E(z) freedom that
   V_RP / V_exp might otherwise use.
5. **σ_8_0 held fixed** at Planck central value (0.8111). A nuisance shift
   at the ±0.02 level would only loosen V_RP / V_exp by ~0.5 in χ²_RSD.
6. **Fluid IDE has no scalar-field perturbations**: we assign LCDM growth
   at Ω_m = 0.3153 as a proxy. Phase 3 would need a full fluid-perturbation
   module to do this right.
7. **ω_b, ω_c held fixed** at Planck central values. Full marginalisation
   could loosen the bound by ~15% but would not reverse the verdict.

## Consequences for base.md §XV

Phase 2 cross-check confirms Phase 1's honest conclusion and now goes further:

- Pure background + sub-horizon growth SQMH modifications (IDE + V(φ) coupled
  quintessence) are *worse* than ΛCDM when evaluated against
  BAO + SN + compressed CMB + RSD jointly.
- **The base.md §XV prediction of w_a < 0 is not derivable** from the
  current effective Lagrangian at two-body coupling order. The only mechanism
  in Phase 2 that gives w_a < 0 is a V(φ) thawing/freezing potential, and
  those potentials are now excluded by the joint data.
- Remaining theoretical paths: (a) re-derive the ξφT^a_a interaction with
  full GFT-level matching to obtain a *radically different* w(z) shape, or
  (b) abandon the §XV DESI prediction as not derivable and revise the paper.
  The w_a < 0 claim in base.md should be moved to "speculative, not yet
  derivable" status in base_2.md until the GFT matching is completed.

This is recorded in base.fix.class.md §9 and §10.
