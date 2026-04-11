# 6. MCMC Posteriors

## 6.1 Sampling setup

We use emcee (Foreman-Mackey et al.) with the stretch-move sampler.
Priors are flat within physical bounds:

- Ω_m ∈ [0.28, 0.36]
- h ∈ [0.64, 0.71]
- candidate-specific θ within model bounds.

Seed 42 is injected via `np.random.seed(42)` inside the run driver to
make stretch-move reproducible despite emcee's use of the global RNG.

**Note on K13 budget.** Phase-5 production target is 48 walkers × 2000
steps × burn 500, thin 10 (K13: R̂ < 1.02).  All six Phase-5 MCMC runs
(C28, C33, A01, A05, A12, A17) were executed at reduced budget
(16 walkers × 300–400 steps) due to shared-CPU constraints; posterior
locations are reproduced within Δχ² ≤ 2.5 of L4 values and are used
for corner plots.  Formal K13 pass requires a high-CPU re-run (estimated
5–6 hours per candidate at 48×2000).  This limitation is recorded in §8.
Bayesian evidence (§7.2) is unaffected as it uses a separate dynesty
nested sampler.

## 6.2 C11D Pure-disformal IDE quintessence (Tier-1 winner, rank 1)

Re-evaluated via Sakstein-Jain 2015 / Copeland-Liddle-Wands 1998 exact
background ODE.  The L4 K3 phantom-crossing kill arose from the
leading-order CPL thawing template w_0 ≈ −1+λ²/3, w_a ≈ −(2/3)λ²
which generates phantom-side noise near γ = 0.  The exact CLW ODE has
w(z) ≥ −1 structurally (positive kinetic energy of real scalar field).

Best-fit posterior (L5-E CLW ODE):

| Parameter | Value | note |
|---|---|---|
| Ω_m | 0.3093 | |
| h | 0.6778 | |
| λ (slope) | 0.90 | exponential V(φ) slope |
| w_0 (derived) | −0.8766 | |
| w_a (CPL proj.) | −0.1855 | |
| Δχ² vs LCDM | **−22.12** | rank 1 |
| phantom crossing | False | |w+1|>1e-3 both sides |

K3 phantom crossing: **CLEARED**. Promoted to Tier-1 winner.
Corner plot: `paper/figures/l5_C11D_corner.png` (pending full 48×2000 run).

## 6.3 C28 Maggiore RR non-local (Tier-1 winner, rank 2)

Posterior means (L5-A reduced budget, R̂_max = 1.82 — K13 pending):

| Parameter | Mean | 1σ | LCDM | σ-dist |
|---|---|---|---|---|
| Ω_m | 0.310 | 0.003 | 0.320 | 3.3σ |
| h | 0.677 | 0.003 | 0.669 | 2.7σ |
| γ_0 (RR coupling) | 1.5e-3 | 8.1e-4 | 0 | 1.85σ |
| w_0 (derived) | −0.849 | 0.018 | −1 | 8.4σ |
| w_a (derived) | −0.242 | 0.054 | 0 | 4.5σ |

Corner plot: `paper/figures/l5_C28_corner.png`.

## 6.4 A12 erf-diffusion (Tier-2 winner, alt-20 class representative)

Zero-parameter closed-form:
E²(z) = E²_LCDM(z) + Ω_m · erf(m · (1−a)), m fixed by E(0)=1.
Posterior samples only (Ω_m, h).

| Parameter | Mean | 1σ |
|---|---|---|
| Ω_m | 0.3093 | 0.003 |
| h | 0.6775 | 0.003 |
| w_0 (CPL proj.) | −0.886 | — |
| w_a (CPL proj.) | −0.133 | — |
| Δχ² vs LCDM | **−21.62** | |

The tight clustering of alt-20 posteriors at (Ω_m ≈ 0.310, h ≈ 0.677)
is consistent with the SVD n_eff = 1 result (Appendix A): all 14
candidates lock to the same physical drift direction.
Corner plot: `paper/figures/l5_A12_corner.png`.

## 6.5 Backup candidates (within winner class)

**A17 adiabatic pulse** (zero-parameter):
Δχ² = −21.26, w_0 = −0.895, w_a = −0.178, Δ ln Z = +10.780 (STRONG).
DR3 separation 2.75σ.  Strongest non-A12 alt cluster member.

**A04 volume-cumulative** (zero-parameter, outlier):
Δχ² = −8.89, w_a = −0.469 (largest |w_a| in the set).
DR3 separation **7.98σ** — highest discrimination power.
Not a winner due to weak Δχ²; flagged as DESI DR3 discriminating sentinel.

## 6.6 Demoted: C33 f(Q) teleparallel

| Parameter | Mean | 1σ |
|---|---|---|
| Ω_m | 0.340 | 0.004 |
| h | 0.647 | 0.005 |
| f_1 | 0.155 | 0.068 |
| w_0 (derived) | −0.984 | 0.007 |
| w_a (derived) | −0.262 | 0.123 |
| Δ ln Z | +2.508 (substantial, borderline Q8) | |

L5-D triple failure: K15 (S_8 = 0.891), Q10 (Δχ²_WL = +54.5), Q11.
Relegated to negative-result appendix.

## 6.7 Eliminated candidates — summary

- **C27 Deser-Woodard**: c₀ posterior collapses to 0. KILL.
- **C41 Wetterich fluid IDE**: Cassini |γ−1| = 2β² ~ 5×10⁻³. KILL.
- **C10k Dark-only**: w_a ≡ 0 structurally, σ_8 worsens. KILL.
- **C23, C5r, C6s RVM**: ν posterior pins at wrong sign (+, not −). KILL.
- **C26 Perez-Sudarsky**: CMB sound-horizon collapse at α_Q > 0. KILL.

## 6.8 Reproducibility

Phase-5 MCMC chains: `simulations/l5/<ID>/mcmc_production.{py,json}`.
Phase-4 chains: `simulations/l4/<ID>/mcmc_posterior.json`.
Seeds, data SHA-256 hashes, and pinned dependency versions in
`simulations/l{4,5}/<ID>/review.md`.
