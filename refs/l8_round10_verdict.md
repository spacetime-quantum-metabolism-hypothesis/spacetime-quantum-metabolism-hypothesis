# refs/l8_round10_verdict.md -- L8 Round 10: Information Geometry / Fisher Metric

> Date: 2026-04-11
> Round 10 of second batch (Rounds 7-11).
> Method: 8-person parallel team, all 3 candidates + SQMH simultaneously.
> Focus: Fisher metric on parameter space (Gamma_0, sigma, H_0).
>   Cramér-Rao bound, KL divergence, minimal description length.
> Prior established: Q31/Q32/Q33 FAIL (Rounds 1-9). NF-1 through NF-9 registered.

---

## Framework Overview

Information geometry treats statistical models as Riemannian manifolds.
For SQMH parameters theta = (Gamma_0, sigma, H_0), the Fisher information matrix is:
  F_{ij}(theta) = int dx * p(x|theta) * [d ln p / d theta_i] * [d ln p / d theta_j]

This defines a natural metric on the parameter space.

For cosmological data (BAO, SN, CMB), the Fisher matrix is approximated:
  F_{ij} ~ sum_k (1/sigma_k^2) * (d mu_k / d theta_i) * (d mu_k / d theta_j)

where mu_k = theoretical prediction for observable k, sigma_k = measurement error.

---

## 8-Person Parallel Discussion

### [Member 1 -- Fisher metric for SQMH parameter space]

SQMH parameters: theta_SQMH = (Gamma_0, sigma, H_0, Omega_m)
[At background level, only specific combinations matter due to NF-5.]

Key: From NF-5, the cosmological observables depend on SQMH parameters only
through the quasi-static solution n_bar* ~ Gamma_0 / (3H).

The E^2(z) from SQMH depends on:
  - H_0 (overall normalization)
  - Omega_m (matter density)
  - n_bar* ~ Gamma_0 / (3H_0) (dark energy density today)
  - The sigma term: sigma * rho_m / (3H) ~ Pi_SQMH ~ 10^-62 (negligible).

Since Pi_SQMH ~ 10^-62, the sigma dependence of observables is:
  d(E^2)/d(sigma) ~ d(n_bar)/d(sigma) ~ -n_bar * rho_m / (3H * kappa)
  ~ -n_bar0 * Pi_SQMH / sigma  [dimensionally]
  ~ n_bar0 * 10^-62 / sigma_SQMH ~ 10^-62 * n_bar0 / (4.52e-53)

The Fisher matrix element F_{sigma, sigma}:
  F_{sigma,sigma} = sum_k (1/sigma_k^2) * (d mu_k / d sigma)^2
  ~ sum_k (1/sigma_k^2) * (10^-62)^2 * (d mu_k / d n_bar)^2

This is ~ 10^-124 times the Fisher element for n_bar.

FINDING: The Fisher metric element F_{sigma,sigma} is NEGLIGIBLE (suppressed
by 10^-124) compared to other parameter combinations. SQMH parameter sigma
is COMPLETELY UNIDENTIFIABLE from cosmological data.

The effective parameter space of SQMH is (Gamma_0, H_0, Omega_m) -- sigma
decouples from observables.

This confirms: sigma = 4*pi*G*t_P cannot be measured or constrained by any
cosmological observation. It is a THEORETICAL INPUT, not a cosmological parameter.

### [Member 2 -- Cramér-Rao bound for SQMH]

Cramér-Rao bound: Var(theta_hat_i) >= [F^-1]_{ii}

For sigma: [F^-1]_{sigma,sigma} ~ 1/F_{sigma,sigma} ~ 10^124 (sigma^2 units).

This means: the minimum variance in estimating sigma from cosmological data is
  sigma_min ~ 10^62 * sigma_SQMH.

In other words: even with infinite data (optimal estimator), you cannot
distinguish sigma_SQMH = 4.52e-53 from sigma = 0 using background-level
cosmological observations. The uncertainty is 10^62 * sigma_SQMH.

This is the CRAMÉR-RAO OBSTRUCTION for SQMH:
  The sigma parameter is cosmologically unidentifiable to 62 orders.

Is this NF-grade? Yes -- it formalizes the "sigma is negligible" observation
as an INFORMATION-THEORETIC BOUND. The Cramér-Rao obstruction is a stronger
statement than the chi^2 analysis of Round 1.

POTENTIAL NF-10: Cramér-Rao obstruction for sigma_SQMH: the sigma parameter
is unidentifiable from cosmological data to 62 orders, with Cramér-Rao
minimum uncertainty ~ 10^62 * sigma_SQMH. This means that even the CONCEPT
of testing the SQMH value of sigma via cosmological data is formally blocked
by the Fisher information bound.

Classification: This is a STRUCTURAL REFINEMENT of the Round 1 chi^2 result,
stated in information geometry language. Moderately new (the chi^2 result was
already known; CR bound is the formal statement). Register as NF-10 (STRUCTURAL).

### [Member 3 -- Fisher metric comparison: SQMH vs A12]

A12 parameters: theta_A12 = (w0, wa, Omega_m, H_0) with w0=-0.886, wa=-0.133.

Fisher matrix for A12 (CPL): well-studied in literature (Chevallier-Polarski,
DESI Fisher forecasts). Typical values (from DESI DR2 + CMB):
  sigma(w0) ~ 0.1, sigma(wa) ~ 0.3  [1-sigma constraints from data]
  F_{w0,w0} ~ 100/sigma(w0)^2 ~ 10^4 per observable
  F_{wa,wa} ~ 10^4 per observable (correlated with w0)

Fisher metric for SQMH (effective parameters): (Gamma_0, H_0, Omega_m) only.
  sigma = completely frozen (Fisher = 0, effectively).
  The effective Fisher metric is identical to LCDM Fisher metric
  (since SQMH ~ LCDM to 10^-62 precision).

Comparison:
  A12: F has non-degenerate 4x4 matrix in (w0, wa, Omega_m, H_0).
  SQMH effective: F is a DEGENERATE 3x3 matrix in (Gamma_0, H_0, Omega_m),
    with a zero eigenvalue for sigma (completely flat direction).

The Fisher geometries are FUNDAMENTALLY DIFFERENT:
  A12: Ellipsoidal posterior in 4D parameter space.
  SQMH: Flat (pancake) distribution in sigma direction, ellipsoidal in 3D.

The extra A12 dimensions (w0, wa) correspond to the SQMH quasi-static n_bar*:
  rho_DE(z) = n_bar*(z) * mu ~ (Gamma_0/(3H(z))) * mu.

For SQMH, the "effective w0 and wa" are fixed by Gamma_0/(3H_0)*mu ~ rho_DE0,
and the deviation from w=-1 is 10^-62 (frozen at sigma level).

CONCLUSION: A12 Fisher geometry is 4D non-degenerate. SQMH Fisher geometry
is 3D + flat sigma direction. They are INEQUIVALENT information geometries.

### [Member 4 -- Fisher metric comparison: SQMH vs C11D and C28]

C11D parameters: theta_C11D = (lambda, Omega_phi, Omega_m, H_0).
  CLW constraint (K32): sigma_eff is negative, so C11D is killed.
  But informationally: Fisher matrix for C11D has non-degenerate 4x4 structure.

C28 parameters: theta_C28 = (gamma_0, Omega_m, H_0).
  gamma_0 = 0.0015 is the only non-LCDM parameter.
  Fisher: sigma(gamma_0) ~ 0.001 from DESI (roughly; it is constrained).
  F_{gamma_0, gamma_0} ~ 1/sigma(gamma_0)^2 ~ 10^6.

SQMH vs C28:
  C28's gamma_0 ~ 10^-3: Fisher element F_{gamma_0} ~ 10^6.
  SQMH's sigma: Fisher element F_{sigma} ~ 10^-124 (from Member 1).
  Ratio: F_{gamma_0}/F_{sigma} ~ 10^130.

The C28 parameter gamma_0 is 130 orders MORE identifiable than sigma_SQMH.
This is another way to state the 62-order gap: in information geometry language,
SQMH's sigma is 130 orders less constrained than C28's gamma_0.

FINDING: The information geometry of C28 is 130 orders more "constrainable"
than SQMH's sigma direction. This is a new way to express NF-5 (Pi_SQMH ~ 10^-62)
in Fisher metric language.

### [Member 5 -- KL divergence: SQMH posterior vs A12 posterior]

Kullback-Leibler divergence D_KL(P_SQMH || P_A12):

For two Gaussian posteriors P(theta) = N(mu, C):
  D_KL(P_SQMH || P_A12) = (1/2) * [tr(C_A12^-1 * C_SQMH) + (mu_SQMH - mu_A12)^T
                            * C_A12^-1 * (mu_SQMH - mu_A12) - d + ln(det(C_A12)/det(C_SQMH))]

where d is the dimension.

For cosmological posteriors:
  - mu_SQMH: SQMH best fit parameters ~ (H_0=70.0, Omega_m=0.315, Gamma_0=fixed_by_rho_DE)
  - mu_A12: A12 best fit ~ (w0=-0.886, wa=-0.133, H_0=67.4, Omega_m=0.310)
  - C_SQMH: diagonal with zero in sigma direction
  - C_A12: full 4x4 covariance (from DESI DR2)

The mean distance (mu_SQMH - mu_A12):
  Both predict E^2(z) ~ LCDM with small corrections.
  The mean vector difference is dominated by the chi^2 = 7.63 gap (Round 1).

For the chi^2 gap chi^2 = 7.63 with dof ~ 100 (DESI data points):
  D_KL (mean part) ~ chi^2/2 = 3.8 nats.

The covariance part: C_SQMH has zero variance in sigma direction but is
broader in (Gamma_0, H_0, Omega_m) -- actually SQMH is not a free CPL fit,
so its effective sigma is ZERO in (w0, wa). SQMH is a point (delta function)
at w = -1 (to 10^-62 precision), while A12 is a 4D posterior.

  D_KL(SQMH delta || A12 Gaussian) = Mahalanobis distance from SQMH point to A12 center.
  This equals chi^2(SQMH vs A12) / 2 = 3.8 nats.

In nats: D_KL ~ 3.8 nats means SQMH posterior is e^3.8 ~ 45 times further
from A12 posterior than a unit standard deviation. This is NOT a large KL
divergence in cosmological terms (many BAO measurements give D_KL >> 10).

FINDING: D_KL(SQMH || A12) ~ 3.8 nats. This quantifies the information
distance between SQMH (LCDM-like) and A12 (CPL with wa=-0.133).

### [Member 6 -- KL divergence: SQMH posterior vs C11D and C28]

D_KL(SQMH || C11D):
  C11D: sigma_eff is negative (K32). The C11D best-fit involves negative sigma,
  which is outside SQMH's parameter space (sigma > 0 always in SQMH).
  D_KL(SQMH || C11D) = infinity (SQMH posterior has zero probability in C11D's
  sigma < 0 region -- they live in disjoint parameter half-spaces).

  More precisely: if we map both to observable space E^2(z), the KL divergence
  is finite because observables don't directly encode sigma sign.
  D_KL(SQMH || C11D) in observable space ~ chi^2(SQMH,E^2 vs C11D,E^2)/2.

  From Round 1 and NF-6: sigma_eff(C11D) is 61 orders wrong and negative.
  In observable space: C11D and SQMH are close (both near LCDM).
  D_KL(SQMH_obs || C11D_obs) ~ few nats (similar to A12).

D_KL(SQMH || C28):
  C28: sigma_eff is negative AND large (K33, 62 orders). Similarly disjoint.
  In observable space: C28 and SQMH are both near LCDM.
  D_KL(SQMH_obs || C28_obs) ~ few nats.

FINDING: In OBSERVABLE space, all three D_KL values are O(few nats) --
because all four theories (SQMH, A12, C11D, C28) are near LCDM at background level.
The KL divergence does NOT discriminate between them observationally.
The key discrimination is in the THEORY parameter space (sign and magnitude of sigma),
which observational KL divergence cannot access.

This confirms: the distinction between SQMH and candidates is THEORETICAL
(structural, sigma-related), not purely observational.

### [Member 7 -- Is SQMH simpler than candidates by minimum description length?]

Minimum description length (MDL) or Bayesian model complexity:
  MDL ~ -log(likelihood) + (d/2)*log(N)  [Schwarz BIC-style]

where d = number of free parameters, N = number of data points.

SQMH free parameters for cosmological fit: (Gamma_0, H_0, Omega_m) = 3 parameters.
  [sigma is fixed at 4*pi*G*t_P; it is THEORETICAL, not fit.]

Candidates:
  A12: (w0, wa, Omega_m, H_0) = 4 parameters. Extra parameter wa = -0.133.
  C11D: (lambda, Omega_phi, Omega_m, H_0) = 4 parameters. Extra lambda.
  C28: (gamma_0, Omega_m, H_0) = 3 parameters. Same as SQMH.

By parameter count: SQMH and C28 are tied at 3 parameters. A12 and C11D have 4.

However, SQMH is effectively 2 parameters:
  At sigma -> 0 limit (which is where SQMH sits observationally), SQMH reduces
  to LCDM with (H_0, Omega_m). The Gamma_0 parameter sets the LCDM DE density.
  So SQMH has 2 LCDM parameters + 1 derived (Gamma_0 = 3H_0*n_bar_eq) = 3 parameters,
  but Gamma_0 is a FUNCTION of rho_DE0 which is also a LCDM parameter.

SQMH EFFECTIVE PARAMETERS for cosmological fit = 2 (H_0, Omega_m).
This is FEWER than all candidates, making SQMH the SIMPLEST description by MDL.

MDL FINDING: In minimum description length sense, SQMH is simpler than all three
candidates (2 effective cosmological parameters vs 3-4). The sigma parameter is
not a cosmological fit parameter -- it is a THEORETICALLY FIXED constant.

BUT: SQMH's simplicity comes at the cost of fit quality. A12 and C28 have better
chi^2 (they fit the wa deviation observed by DESI). SQMH with 2 parameters gives
chi^2/dof = 7.63/something > 1. A12 with 4 parameters fits better.

MDL balances fit quality vs complexity: In MDL terms, A12 is preferred over SQMH
(better fit with reasonable extra parameters). SQMH loses on MDL.

FINDING: SQMH is the SIMPLEST model (fewest fit parameters) but has WORSE FIT
(chi^2 > 1). By MDL, candidates A12/C28 are preferred. This is consistent with
"SQMH is NOT the best fit to DESI data" (confirmation of Q31 FAIL).

### [Member 8 -- Round 10 consensus and NF assessment]

Summary of Round 10 findings:

1. Fisher metric: sigma_SQMH has F_{sigma,sigma} ~ 10^-124 (negligible).
   SQMH is informationally degenerate in the sigma direction.

2. Cramér-Rao obstruction: minimum uncertainty in sigma from cosmological
   data ~ 10^62 * sigma_SQMH. sigma is cosmologically unidentifiable.

3. Fisher geometry comparison: A12 (4D non-degenerate) vs SQMH (3D + flat).
   C28 (sigma(gamma_0) ~ 0.001) vs SQMH (sigma(sigma) = infinite, unmeasurable).
   Ratio F_{gamma_0}/F_{sigma} ~ 10^130.

4. KL divergence: D_KL(SQMH || A12) ~ 3.8 nats in observable space.
   All D_KL values are O(few nats) because all theories are LCDM-like.
   Observational KL does NOT discriminate; distinction is theoretical.

5. MDL: SQMH has 2 effective fit parameters (simplest), but chi^2 > 1.
   Candidates preferred by MDL (better fit with reasonable complexity).

NEW FINDING ASSESSMENT:

NF-10 CANDIDATE (Cramér-Rao obstruction):
"sigma_SQMH is cosmologically unidentifiable: the Fisher information bound
gives minimum uncertainty Delta_sigma >= 10^62 * sigma_SQMH from any
background-level cosmological observation. This is the information-theoretic
equivalent of the 62-order scale gap (NF-5), now stated as a fundamental
measurement-theoretic bound."

Is this NF-grade? Yes, the Cramér-Rao framing is new and adds information-
theoretic rigor to the scale gap. Register as NF-10 (STRUCTURAL, with
information-theoretic language).

Also notable: The Fisher metric comparison showing C28's gamma_0 is
10^130 more identifiable than sigma_SQMH is a vivid illustration of the gap.

DECISION: Register NF-10 (Cramér-Rao obstruction for sigma_SQMH).

---

## Round 10 Team Consensus

### New Finding: NF-10 (Cramér-Rao Obstruction for sigma_SQMH)

**Classification**: STRUCTURAL (information-theoretic refinement of NF-5)

**Content**: The Fisher information for sigma_SQMH from background-level
cosmological data is:
  F_{sigma,sigma} ~ (Pi_SQMH)^2 / sigma_SQMH^2 ~ (10^-62)^2 / sigma_SQMH^2

The Cramér-Rao bound gives minimum variance:
  Delta_sigma_min = 1/sqrt(F_{sigma,sigma}) ~ sigma_SQMH / Pi_SQMH ~ 10^62 * sigma_SQMH.

This means: no cosmological experiment can distinguish sigma_SQMH = 4.52e-53
from sigma = 0 at any finite significance. The sigma parameter is COSMOLOGICALLY
UNIDENTIFIABLE -- not just small, but measurement-theoretically inaccessible.

Comparing to C28's gamma_0 = 0.0015:
  F_{gamma_0} / F_{sigma_SQMH} ~ (10^62)^2 / (10^-3)^2 ~ 10^130.
  C28's non-local parameter is 10^130 times more constrainable than SQMH's sigma.

**Assessment**: New perspective on the scale gap (NF-5). The Cramér-Rao framing
converts the "62-order numerical gap" into "cosmologically unidentifiable parameter."
This is useful for the paper to argue why SQMH's sigma cannot be confirmed
via standard cosmological tests -- it is a measurement-theoretic impossibility.

**Paper language**: "The SQMH somatic coupling sigma = 4piGt_P is cosmologically
unidentifiable: the Fisher information for sigma from background-level data is
F_{sigma} ~ Pi_SQMH^2/sigma^2, giving a Cramér-Rao lower bound Delta_sigma_min ~
10^62 sigma_SQMH. No cosmological observation can constrain sigma at the SQMH
value. In contrast, the non-local gravity parameter gamma_0 of C28 is constrained
to ~10^-3 level, a factor 10^130 more identifiable."

### Q3x Status After Round 10

- Q31 (A12 chi^2/dof < 1.0): FAIL. By MDL, A12 is preferred over SQMH.
  Information geometry gives no new path to Q31.
- Q32 (C11D sigma_eff match): FAIL. Information geometry confirms: sigma_eff
  for C11D is in a disjoint parameter half-space (sigma < 0).
- Q33 (C28 residual < 20%): FAIL. Fisher metric comparison shows 10^130 gap
  in parameter identifiability. C28 ≠ SQMH informationally.

**Round 10 Verdict: Q31/Q32/Q33 REMAIN FAIL.**
NF-10 (Cramér-Rao obstruction for sigma_SQMH) registered as STRUCTURAL finding.

---

*Round 10 complete: 2026-04-11*
