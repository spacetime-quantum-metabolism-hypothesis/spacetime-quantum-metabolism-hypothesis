# Figure 13 — Phase 3 MCMC Posterior (V_RP corner plot)

**Generated**: 2026-04-10 by `simulations/phase3/mcmc_phase3.py`

## Scope

Phase 3 = **Python-only MCMC marginalisation** of the Phase 2 joint likelihood.
This is the realistic single-session Phase 3 — NOT the full CLASS/Cobaya programme
described in `base.fix.class.md §3.1`, which requires a CLASS C patch + Planck clik
likelihood (~12 months of work, deferred to Phase 4).

## What changed vs Phase 2

| Aspect | Phase 2 | Phase 3 |
|--------|---------|---------|
| Ω_m | optimised (scipy) | **MCMC marginalised** |
| h = H_0/100 | fixed 0.6736 | **MCMC marginalised** (flat [0.55, 0.80]) |
| ω_b | fixed 0.02237 | **BBN prior** 0.02237 ± 0.00015 |
| σ_8,0 | fixed 0.8111 | **Planck prior** 0.8111 ± 0.02 |
| r_d | fixed 147.09 Mpc | **derived** via EH98 z_drag + sound horizon integral |
| RSD cov | diagonal | **BOSS DR12 3×3 off-diagonal block** (Alam+ 2017: ρ_38,51=0.24, ρ_38,61=0.10, ρ_51,61=0.26) |
| V_RP (β, n) | point estimate | **MCMC marginalised** (flat priors: β∈[0,1], n∈[0.05,3.0]) |

## Sampler

- emcee `EnsembleSampler`, 20 walkers
- LCDM: 200 burn-in + 700 sampling = 14 000 total samples (4 params)
- V_RP: 200 burn-in + 600 sampling = 12 000 total samples (6 params)
- Start centred at Phase 2 best-fit with Gaussian scatter
- Pure LCDM high-z bridge (z > 2.5): SQMH coupling negligible deep in matter/radiation era;
  no rescaling at z_cut (avoids backward-ODE phi_N→√6 pathology tainting theta*)

## Marginalised posteriors

### LCDM (4 parameters, 14 000 samples, τ ≈ 21-34, acceptance 0.59)

| Parameter | Median | −1σ | +1σ | Notes |
|-----------|--------|-----|-----|-------|
| Ω_m | 0.3124 | 0.0025 | 0.0026 | BAO+SN pull |
| h | 0.6777 | 0.0022 | 0.0023 | BAO(via r_d) + CMB θ* |
| ω_b | 0.02242 | 0.00015 | 0.00015 | BBN prior dominated |
| σ_8,0 | 0.8101 | 0.0163 | 0.0164 | Planck prior dominated |

**Best fit**: χ²_min = **1683.10** at (0.3125, 0.6778, 0.02242, 0.8123)

### V_RP (6 parameters, 12 000 samples, τ ≈ 32-41, acceptance 0.49)

| Parameter | Median | −1σ | +1σ | Notes |
|-----------|--------|-----|-----|-------|
| Ω_m | 0.3228 | 0.0044 | 0.0039 | shifted +0.010 vs LCDM |
| h | 0.6712 | 0.0033 | 0.0036 | shifted −0.006 vs LCDM |
| ω_b | 0.02247 | 0.00015 | 0.00015 | BBN prior dominated |
| σ_8,0 | 0.8075 | 0.0169 | 0.0182 | Planck prior dominated |
| **β** | 0.098 | 0.038 | 0.051 | ~2σ from 0 |
| **n** | 0.087 | 0.025 | 0.042 | small-n limit |

**Best fit**: χ²_min = **1681.73** at (β=0.066, n=0.057), effectively near the
LCDM limit of the V_RP family.

## Model comparison

| Metric | LCDM | V_RP | Δ |
|--------|------|------|---|
| χ²_min | 1683.10 | 1681.73 | **−1.37** |
| k (free params) | 4 | 6 | +2 |
| AIC | 1691.10 | 1693.73 | **+2.63** |
| BIC | 1713.20 | 1726.88 | **+13.68** |

**AIC verdict**: LCDM weakly preferred by ΔAIC ≈ 2.6 (not a strong rejection;
Jeffreys' scale = "positive but not strong"). **BIC verdict**: LCDM strongly
preferred by ΔBIC ≈ 13.7 (Jeffreys' = "very strong").

## What changed vs Phase 2 — the projection-effect reversal

Phase 2 (all nuisances **fixed**) reported V_RP **worse** by Δχ² ≈ +4.14
(ΔAIC = +6.66). Phase 3 (nuisances **marginalised**) reports V_RP **better**
by Δχ² = −1.37 (ΔAIC = +2.63). The sign of Δχ² flipped.

Mechanism: V_RP exploits the joint (h, r_d) correlation that Phase 2 had
frozen at Planck fiducial. V_RP shifts h down by ~1% and lets r_d (EH98-derived)
rise ~1%, partially absorbing the BAO distance scale. β ≈ 0.098 then adds a
tiny growth/background modulation that recovers an extra Δχ² ≈ 1.4. The net
best-fit V_RP point is effectively "LCDM + 2 free knobs of wiggle room", not
a distinct SQMH signal.

The AIC penalty (+4 for the 2 extra parameters) still beats that Δχ², so LCDM
is preferred. But the preference is much weaker than Phase 2 claimed. The
**honest Phase 2 verdict would have been** "LCDM preferred at the marginal
level once joint nuisances are accounted for", not the stronger "ΔAIC ≈ +6.7"
rejection we previously reported.

## Verdict

**Path F (rejection) holds, but downgraded from "strong" to "weak" preference.**

- BIC decisively rejects V_RP (ΔBIC = +13.7) — a full-Bayesian penalty on model
  complexity at N = 1853.
- AIC only weakly prefers LCDM (ΔAIC = +2.63) — frequentist complexity penalty.
- V_RP posterior is consistent with the LCDM limit (β, n both ~2σ from zero),
  so the "improvement" comes from being *allowed* to wiggle, not from a
  coherent SQMH signal.
- The V_RP best fit **lowers** H_0 to 0.6712, moving further from the SH0ES
  distance-ladder value (~0.73). SQMH does **not** help the H_0 tension under
  this coupled-quintessence parametrisation.

**Action items for base_2.md**:
1. The headline "Phase 2 ΔAIC = +6.7" should be replaced with the
   marginalised Phase 3 number: **ΔAIC = +2.6 (weak), ΔBIC = +13.7 (strong)**.
2. The §XV w_a < 0 retraction (`base.fix.class.md §10.6`) stands — V_RP best
   fit is "near-LCDM", not a distinct w_a-producing signal.
3. The H_0 tension discussion must note that coupled V(φ) SQMH variants *worsen*
   the tension rather than relieving it.

## Artifacts

- `simulations/phase3/mcmc_phase3.py` — MCMC driver
- `simulations/phase3/chains/lcdm_chain.npy`, `lcdm_logp.npy` (14 000 samples)
- `simulations/phase3/chains/vrp_chain.npy`, `vrp_logp.npy` (12 000 samples)
- `figures/13_phase3_mcmc.png` — V_RP 6D corner plot
- `simulations/phase3/phase3_run.log` — run log

## Caveats

1. **Compressed CMB only** — no TT/EE/lensing. Phase 4 needs CLASS patch.
2. **ω_c is derived** (= Ω_m·h² − ω_b), not independently sampled. Joint (ω_b, ω_c) Planck
   covariance ignored; treated as diagonal.
3. **r_d via EH98** fitting formula; ~1% bias vs Boltzmann codes. Dominant consequence:
   BAO χ² minimum shifts by ~few vs Phase 2 fixed r_d=147.09.
4. **Growth background still LCDM-substituted** (quintessence_perturb.py uses analytic LCDM
   E(N) for the growth ODE; slow-roll φ_N approximation). Proper tracker φ_N needs Phase 4.
5. **Fluid IDE skipped** in Phase 3 MCMC — Phase 2 showed it converges onto the LCDM boundary
   (ξ_q = 0) with no posterior freedom to sample.
6. **20 walkers × 800 steps** is modest; autocorrelation τ and R-hat tracked. Posteriors
   should be visually smooth but 1-σ tails may be under-sampled. Adequate for headline
   parameter constraints, not for tail-probability claims.

## Verdict

<!-- filled in after run -->
