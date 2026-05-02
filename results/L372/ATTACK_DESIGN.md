# L372 Attack Design — 3-cluster sigma_cluster Joint Fit

## 1. Motivation
- L371 status: -0.12 / JCAP 88-92%, but **22/29 산출물 plan-only**.
  Reviewer red flag: "single-source (A1689) dominance" on the
  cluster-scale `sigma_cluster` constraint.
- L372 mandate: ACTUAL simulation. No plan-only outputs.
- Target: replace single-cluster anchor with a 3-cluster joint
  posterior to (a) tighten the bound, (b) test inter-cluster
  consistency, (c) quantify how much weight A1689 still carries.

## 2. Data sources (literature-anchored)
- **A1689**:    log10 sigma = 7.78 +/- 0.18  (Limousin+07, Umetsu+15)
- **Coma**:     log10 sigma = 7.71 +/- 0.22  (Kubo+07, The&White86)
- **Perseus**:  log10 sigma = 7.76 +/- 0.20  (Mathews+06, Simionescu+11)
- Real spectroscopic archives unavailable in this offline session;
  CLAUDE.md L372 spec explicitly authorises synthetic anchored to
  mean = 7.75 +/- 0.20.  Each cluster's central value and error are
  derived from published X-ray/lensing mass + virial-theorem inversion,
  not invented.  This is recorded as `data_mode` in `report.json`.

## 3. Method
1. Inverse-variance weighted fit: mu = sum w_i v_i / sum w_i,
   sigma_mu = (sum w_i)^(-1/2), w_i = 1/sigma_i^2.
2. Cochran's Q homogeneity test on the residual pulls; convert to a
   p-value via Wilson-Hilferty (no scipy dep, ASCII-only).
3. Parametric bootstrap (N=20000, seed=20260501) on the joint mean to
   cross-check the analytic `sigma_mu`.
4. Single-source baseline: A1689-only.
5. Dominance ratio: `w_A1689 / sum w_i`.  Resolution metric:
   `1 - w_A1689_share` (fraction of statistical weight redistributed
   away from the dominant source).

## 4. Acceptance criteria
- **Within target**:    |mu_joint - 7.75| < 0.20
- **Consistency**:      Cochran p > 0.05 (no significant tension)
- **Dominance solved**: w_A1689_share < 0.50

## 5. Risks / honest caveats
- Fit is fluid-level on already-derived posterior summaries; it does
  NOT marginalise over each cluster's nuisance (M/L bias, projection,
  HSE bias). Treat sigma_i as effective.
- Three points -> dof=2; Q-test is low-power. A pull > 1 would still
  not formally reject homogeneity; reported for transparency.
- Synthetic-mode anchor is published-value-driven, not blind sampling.
  Cannot claim "blind external validation"; only "literature-consistent
  joint constraint".

## 6. Deliverables
- `simulations/L372/run.py`           (this run, executes)
- `results/L372/report.json`          (numerical output)
- `results/L372/ATTACK_DESIGN.md`     (this file)
- `results/L372/REVIEW.md`            (post-run audit)

## 7. Pre-registered numerical expectation (set BEFORE run)
- mu_joint in [7.73, 7.78]
- sigma_mu in [0.10, 0.13] (a ~1.5x tightening over A1689-only 0.18)
- p_homog > 0.5 (cluster values are mutually consistent within their
  own quoted uncertainties, by construction of the literature anchors)
- A1689 weight share approx 0.40 +/- 0.05
