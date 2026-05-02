# Statistical Methods Appendix

This appendix consolidates the statistical machinery used throughout the SQMH
paper in response to Referee R3's request for a single, self-contained
methodological reference. It defines every information criterion, evidence
estimator, and model-averaging weight used in the main text, specifies the
mock injection protocol used to validate the pipeline, and documents the
R-grid sensitivity tests cited in §6 and §7.

Honest one-liner: this appendix records definitions, approximations, and
reproduction procedures only — it introduces no new data fits, no new
predictions, and no new posterior numbers beyond those already reported in
the main text.

---

## A.1 Information Criteria

Let `L_max` denote the maximum of the likelihood, `chi2_min = -2 ln L_max`
the corresponding chi-square at the best-fit point, `k` the number of free
parameters of the model, and `n` the number of independent data points
entering the joint likelihood (BAO+SN+CMB+RSD, optionally +WL when
explicitly noted).

### A.1.1 AIC and AICc

The Akaike Information Criterion is

    AIC = 2 k - 2 ln L_max = chi2_min + 2 k.

For the small-sample regime (`n / k < 40`, which is borderline for the
13-point DESI BAO subset and decisive for the compressed CMB triplet) we
use the Hurvich-Tsai (1989) corrected form throughout:

    AICc = AIC + 2 k (k + 1) / (n - k - 1).

We require `n - k - 1 > 0`; whenever this fails for a candidate model we
report `AICc = NaN` and exclude that candidate from criterion-based
ranking, falling back to BIC and marginalized evidence.

### A.1.2 BIC

The Schwarz / Bayesian Information Criterion is

    BIC = k ln n - 2 ln L_max = chi2_min + k ln n.

BIC is reported alongside AICc to expose the prior-volume sensitivity of
the chosen criterion: any conclusion that survives only under one
criterion but not the other is flagged in the main text as criterion-
dependent.

### A.1.3 DIC

For posterior samples `{theta_s}` from the MCMC chains we compute the
Deviance Information Criterion (Spiegelhalter et al. 2002) as

    D(theta) = -2 ln L(theta),
    D_bar    = <D(theta)>_posterior,
    p_D      = D_bar - D(theta_bar),
    DIC      = D_bar + p_D = D(theta_bar) + 2 p_D,

where `theta_bar` is the posterior mean. `p_D` measures the effective
number of parameters as resolved by the data; we report it to flag cases
where the nominal `k` overstates model flexibility (e.g. parameters that
are prior-dominated).

### A.1.4 WAIC

The Watanabe-Akaike (widely applicable) Information Criterion (Watanabe
2010; Gelman, Hwang & Vehtari 2014) uses pointwise log-likelihoods. For
data points `i = 1..n` and posterior samples `s = 1..S`:

    lppd     = sum_i ln ( (1/S) sum_s p(y_i | theta_s) ),
    p_WAIC   = sum_i Var_s [ ln p(y_i | theta_s) ],
    WAIC     = -2 ( lppd - p_WAIC ).

WAIC is preferred over DIC when posteriors are non-Gaussian, which is the
case for the C28 RR non-local candidate and several Alt-20 drift toys.
DIC and WAIC are reported in parallel; disagreements larger than `Delta = 2`
are noted explicitly.

---

## A.2 Marginalized Log-Evidence by Laplace Approximation

For models where full nested sampling is too expensive (Phase-3/Phase-4
joint chi2 ~ 100 ms/call, 5–6 h per candidate at the production setting),
we report a Laplace approximation to the marginalized log-evidence:

    ln Z = ln integral L(theta) pi(theta) d^d theta
         ≈ ln L(theta_MAP) + ln pi(theta_MAP)
           + (d/2) ln(2 pi) - (1/2) ln det H,

where `d` is the parameter-space dimension, `theta_MAP` is the maximum a
posteriori point, and `H = -d^2 ln[L pi]/dtheta dtheta'` evaluated at
`theta_MAP` is the negative Hessian of the log-posterior. We compute `H`
either (i) numerically from a finite-difference stencil at the MAP or
(ii) from the inverse covariance estimated from the converged MCMC chain
when `Rhat < 1.05`. Both estimates are reported when available; agreement
within 0.5 nats is required for the Laplace value to be quoted as a
final number.

The Laplace estimate is biased high in two regimes that occur in this
paper:
1. parameters railed to a prior boundary (e.g. `beta_d >= 0` in dark-only
   coupled quintessence), where the local Gaussian assumption fails;
2. multi-modal posteriors (C28 5D fits), where the local Hessian
   captures only one mode.

In both cases we substitute a thermodynamic-integration or nested-sampling
estimate from a single high-fidelity dynesty run and quote the difference.

### A.2.1 Fixed-θ vs marginalized evidence (L6 caveat)

L5 reported "fixed-θ evidence gaps" obtained by holding extra parameters
at their MAP values; these omit the Occam volume penalty. L6 quotes
fully marginalized `ln Z`, which is necessarily lower for any model with
parameters not strongly constrained by the data. The two numbers are not
interchangeable. Throughout this appendix and the main text, `ln Z` with
no qualifier always refers to the marginalized value defined in this
section. Fixed-θ values, when quoted at all, are explicitly labelled
`ln L_max` or `ln Z_fixed`.

---

## A.3 Bayesian Model Averaging (BMA)

Given a discrete set of candidate models `M_i` with prior probabilities
`pi_i` (we use uniform `pi_i = 1/N_models` unless stated otherwise) and
marginalized evidences `Z_i` from §A.2, the posterior model probability is

    P(M_i | D) = pi_i Z_i / sum_j pi_j Z_j,

and the BMA weight is

    w_i = P(M_i | D).

Predictions for any derived observable `X` are averaged as

    <X>_BMA   = sum_i w_i <X>_i,
    Var(X)_BMA = sum_i w_i [ Var(X)_i + (<X>_i - <X>_BMA)^2 ].

We deliberately use marginalized `Z_i`, not `L_max,i`, in the BMA weights:
using `L_max,i` would double-count parameter freedom and would falsely
elevate flexible toys (e.g. the 14-cluster Alt-20 SVD-degenerate set,
n_eff = 1) above their effective rank.

When two candidates have indistinguishable evidence
(`|Delta ln Z| < 0.5`) and a Fisher pairwise discrimination below
`0.5 sigma` even at DR3 forecast precision (e.g. C28 vs C33,
0.19 sigma), we flag the BMA result as data-undecided and refrain from
claiming a unique winner.

---

## A.4 Mock Injection Setup

The mock injection pipeline used in §6 and Appendix verification/ takes
the following form, identical for every candidate:

1. Choose a fiducial parameter vector `theta_true`. For SQMH-internal
   tests we use the joint-best A12 MAP; for null tests we use the
   Planck-2018 LCDM mean.
2. For each data block in the joint likelihood (DESI DR2 BAO 13 pt,
   DES-Y5 SN, compressed CMB triplet, RSD f sigma_8 9 pt, optionally
   DES-Y3 cosmic shear S_8) compute the model prediction
   `mu(theta_true)`.
3. Draw a Gaussian noise realisation `eta ~ N(0, C)` where `C` is the
   published covariance for that block. Cross-block covariances are
   set to zero (justified at the < 1% level for the analyses here).
4. The mock data vector is `d_mock = mu(theta_true) + eta`. We use the
   same covariance `C` for both injection and recovery.
5. Re-run the full MCMC with the same priors and proposal as the real
   analysis (chains: 48 walkers, 2000 steps after a 1000-step burn-in,
   `np.random.seed(42)` inside `run_mcmc`).
6. The recovery test passes if (a) the marginal posterior for every
   parameter contains `theta_true` at the 68% level for at least 64% of
   100 independent realisations, and (b) the joint chi2 distribution
   over realisations is statistically consistent with chi2_(n-k).

The seed schedule for the production mock suite is `seed = 100 + i`
for `i = 0..99`, fixed at code-freeze and recorded in
`simulations/l442/mock_seeds.txt` (provenance only; no new fits in this
appendix).

Failure modes guarded against by this protocol: (i) prior-railed
parameters that produce biased recovery (we monitor the fraction of
chains hitting the boundary); (ii) under-coverage from the Laplace
approximation, which is why §A.2 cross-checks against MCMC samples.

---

## A.5 R-grid Sensitivity

Several SQMH candidates depend on a discretised redshift grid `R = {z_i}`
used to integrate the modified expansion history. We document the grid
choices and the corresponding stability test cited in §7:

- Default grid: `N_R = 4000` linearly spaced points on
  `z in [0, max(z_eff) + 0.01]`, integrated with
  `scipy.integrate.cumulative_trapezoid` (L33 re-occurrence rule).
- Alternative grids tested: `N_R in {1000, 2000, 4000, 8000}` linear,
  and `N_R = 4000` log-spaced on `1 + z`.
- Stability criterion: the joint chi2 at the best-fit point must vary by
  less than `Delta chi2 = 0.05` across all grid choices; the AICc
  reported in the main text uses `N_R = 4000` linear.
- The previously documented 800-point + `np.cumsum` mid-point pattern is
  forbidden by project rule (L33 re-occurrence) because it under-estimates
  chi2 by ~ 0.75 and inflates `Delta AICc`.

The BAO comoving-distance integrand `1/E(z)` is also clipped at
`ratio = clip(psi_0/psi_z, 1.0, 200.0)` for SQT-family candidates to
prevent the high-z divergence noted in the L33 rule. Sensitivity to the
upper clip (testing `100, 200, 400, 800`) changes the joint chi2 by less
than `0.02` for every candidate reported.

---

## A.6 Mapping to R3 Reviewer Items

| R3 item                                             | Section                |
|-----------------------------------------------------|------------------------|
| "Define every IC used"                              | §A.1.1–A.1.4           |
| "Show how marginalized lnZ is computed"             | §A.2                   |
| "Distinguish fixed-θ from marginalized evidence"    | §A.2.1                 |
| "Provide proper BMA weights, not max-L weights"     | §A.3                   |
| "Document the mock injection / recovery test"       | §A.4                   |
| "R-grid sensitivity for SQT integrals"              | §A.5                   |
| "Show that BMA respects Occam volume"               | §A.2.1 + §A.3          |

---

## A.7 What this appendix does *not* claim

- No new posterior numbers are introduced here. All Δ AICc, Δ ln Z, BMA
  weights, and Fisher pairwise figures cited in this appendix are
  references to the corresponding tables in the main text.
- The Laplace approximation is acknowledged as an approximation; cases
  where it disagrees with full nested sampling by more than 0.5 nats
  are footnoted in the main text and the nested-sampling value is
  preferred.
- BMA does not, and cannot, repair an under-specified model space: if
  the true generating model is outside the candidate set, the weights
  are conditional on a wrong prior over models. The mock injection
  tests in §A.4 are explicitly designed to detect this failure mode
  on the candidates considered.
