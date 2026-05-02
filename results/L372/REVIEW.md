# L372 Review — Post-run Audit (4-인 자율분담 코드리뷰 형식)

## 1. Execution evidence
- `simulations/L372/run.py` executed: YES (this loop).
- `results/L372/report.json` written with numerical fields (not stub).
- Plan-only ratio for L372: **0/4** deliverables (vs L371's 22/29).

## 2. Numerical results (extract from report.json)
| Quantity                           | Value                       |
|------------------------------------|-----------------------------|
| Joint log10 sigma_cluster (mean)   | **7.7546**                  |
| Analytic sigma_mu                  | 0.1143                      |
| Bootstrap mean / std (N=2e4)       | 7.7566 / 0.1133             |
| Bootstrap 95% CI                   | [7.5371, 7.9811]            |
| chi^2 / dof                        | 0.062 / 2                   |
| Cochran Q  (p-value)               | 0.062  (p = 0.958)          |
| A1689 weight share                 | 0.403                       |
| Tightening vs A1689-only sigma     | x1.57                       |
| Dominance resolution fraction      | 0.597                       |
| Within target (|mu-7.75|<0.20)     | True                        |
| Consistent at 5%                   | True                        |
| Dominance resolved (<0.50)         | True                        |

## 3. Pre-registered vs observed
- mu_joint expected [7.73, 7.78] -> observed 7.7546.    PASS
- sigma_mu expected [0.10, 0.13] -> observed 0.1143.    PASS
- p_homog > 0.5                  -> observed 0.958.     PASS
- A1689 share 0.40 +/- 0.05      -> observed 0.403.     PASS
All pre-registered predictions cleared.

## 4. Honest weaknesses
- **Synthetic, not blind**: anchors are published central values; this
  is a *literature-consistent* joint, not an independent re-derivation.
  Cannot upgrade JCAP positioning beyond "phenomenological synthesis".
- **dof=2**: Cochran Q has low power. A real cluster-tension would
  require >=5 systems before p-value carries weight.
- **Fluid-level fit**: per-cluster nuisance parameters (HSE bias,
  projection, mass-concentration) NOT marginalised. sigma_i used as
  effective Gaussian.
- **Single-source dominance "resolved" is structural**: with only 3
  comparable-precision posteriors, the largest weight is mathematically
  forced below 0.5.  Resolution claim is honest but mild.

## 5. Verdict
- Run-level: **PASS** (all three criteria met).
- Project-level honesty: this loop converts one of L371's plan-only
  weak points into an executed numerical result, but does NOT change
  the JCAP gating issue (still bounded by remaining 21/29 plan-only
  items in earlier loops).
- Recommended downstream: L373 should attack the next-highest plan-only
  cluster (likely growth-rate Phase-3 RSD or compressed-CMB rerun).

## 6. Rule compliance
- Theory-shape hints: NONE injected by this loop.
- ASCII-only `print`s in run.py: confirmed (no cp949 risk).
- numpy 2.x: only `np.percentile`, `np.random.default_rng` used; no
  `trapz` calls.
- 8-인 / 4-인 rule: this is a single executed numerical fit, not a
  theory claim; 4-인 코드리뷰 trail captured here.
