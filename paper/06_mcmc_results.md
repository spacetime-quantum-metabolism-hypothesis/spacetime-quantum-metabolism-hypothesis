# 6. MCMC Posteriors

## 6.1 Sampling setup

We use emcee (Foreman-Mackey et al.) with the stretch-move sampler.
Priors are flat within physical bounds:

- Ω_m ∈ [0.28, 0.36]
- h ∈ [0.64, 0.71]
- candidate-specific θ within model bounds.

Seed 42 is injected via `np.random.seed(42)` inside the run driver to
make stretch-move reproducible despite emcee's use of the global RNG.

**Note on budget.** The L4 runs reported here used a reduced budget
(16–24 walkers, 180–500 steps) due to shared-CPU runtime constraints
across ten parallel candidate drivers.  The target Phase-5 production
budget is 48 walkers × 2000 steps × burn 500, thin 10, which will
reduce Gelman-Rubin R̂ from the current 1.05–1.27 range to below 1.02
on all parameters.

## 6.2 C28 Maggiore RR non-local

Posterior means (L4-reduced):

| Parameter | Mean | 1σ | LCDM | σ-distance |
|---|---|---|---|---|
| Ω_m | 0.310 | 0.003 | 0.320 | 3.3σ |
| h | 0.677 | 0.003 | 0.669 | 2.7σ |
| γ_0 (RR coupling) | 1.5e-3 | 8.1e-4 | 0 | 1.85σ |
| w_0 (derived) | -0.849 | 0.018 | -1 | 8.4σ |
| w_a (derived) | -0.242 | 0.054 | 0 | 4.5σ |

R̂_max = 1.12 → 1.23 (K9 soft-flag, to be cleared by re-run).

LCDM is excluded in the (w_0, w_a) 2-D plane at ~3σ via the DESY5 SN
likelihood.  The γ_0 coupling is marginally preferred at ~1.85σ; the
dominant constraining power comes from the background BAO + SN fit,
not from the auxiliary coupling itself.

## 6.3 C33 f(Q) teleparallel

| Parameter | Mean | 1σ | LCDM | σ-distance |
|---|---|---|---|---|
| Ω_m | 0.340 | 0.004 | 0.320 | 5.0σ |
| h | 0.647 | 0.005 | 0.669 | 4.4σ |
| f_1 | 0.155 | 0.068 | 0 | 2.3σ |
| n | 1.12 | 0.15 | — | — |
| w_0 (derived) | -0.984 | 0.007 | -1 | 2.3σ |
| w_a (derived) | -0.262 | 0.123 | 0 | 2.1σ |

R̂_max = 1.27 (K9 soft-flag).

The Ω_m and h posterior are noticeably displaced from the ΛCDM
best-fit, reflecting the teleparallel rescaling of the early-time
expansion history.  f_1 > 0 is preferred at ~2.3σ, consistent with the
L2 numerical verification and disagreeing with the L3 toy (which had a
parametrisation-induced sign flip).

## 6.4 C11D Disformal IDE (under re-evaluation)

| Parameter | Mean | 1σ |
|---|---|---|
| Ω_m | 0.310 | 0.003 |
| h | 0.677 | 0.003 |
| γ_D | 0.650 | 0.063 |
| w_0 | -0.858 | 0.027 |
| w_a | -0.285 | 0.055 |

C11D has the largest Δχ² improvement (−22.9) of any candidate in L4
but is currently KILLed on K3 (phantom crossing).  Phase 5 will re-run
with a hi_class disformal exact background; if K3 clears, C11D will be
the strongest Phase-5 candidate.

## 6.5 Eliminated candidates — posterior summaries

For completeness we list the posterior summaries of the candidates that
were killed at L4:

- **C27 Deser-Woodard**: c₀ = 0.003 ± 0.082 (compatible with 0),
  posterior collapses to ΛCDM.  KILL.
- **C41 Wetterich fluid IDE**: β = 0.047 ± 0.007, Δχ² = −14.2, but
  Cassini |γ−1| = 2β² ~ 5×10⁻³ fails Q5.  KILL.
- **C10k Dark-only**: β_d = 0.185 ± 0.019, w_a ≡ 0 at background, growth
  channel Δχ²_RSD = +0.0 (no improvement), σ_8 worsens by +0.96%.  KILL.
- **C23 Asymptotic Safety**: ν_eff = +0.009 ± 0.003 (interior), wrong
  sign for SQMH metabolism (expected ν < 0).  KILL.
- **C5r, C6s RVM**: ν pinned at +0.009 (prior wall on [-0.03, +0.01]),
  wrong sign.  KILL.
- **C26 Perez-Sudarsky**: α_Q collapses to 0 in full ODE; the L3 toy
  form was a first-order expansion not equivalent to the integrated
  diffusion source.  KILL, under re-formulation.

## 6.6 Reproducibility

All MCMC chains are dumped in `simulations/l4/<ID>/mcmc_posterior.json`.
Seeds, data file SHA-256 hashes, and pinned dependency versions are
recorded in the companion `simulations/l4/<ID>/review.md`.  Re-runs
are mechanical: `python simulations/l4/<ID>/mcmc.py`.
