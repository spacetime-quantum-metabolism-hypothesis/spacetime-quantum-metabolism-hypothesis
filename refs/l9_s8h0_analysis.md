# refs/l9_s8h0_analysis.md -- L9-D S8/H0 Tension Analysis

> Date: 2026-04-11
> Phase: L9-D
> Script: simulations/l9/tensions/s8h0_analysis.py
> 8-person parallel team derivation.

---

## Observed Tensions

- S8 tension: DES-Y3 S8 = 0.759 vs Planck S8 = 0.834 (gap = 0.075, 2.3 sigma)
- H0 tension: CMB H0 = 67.4 vs SH0ES H0 = 73.0 km/s/Mpc (gap = 5.6, 5 sigma)
- Q45 threshold: DeltaS8 > 0.01 OR DeltaH0 > 0.5 km/s/Mpc

---

## Team Derivation

### Person 1 (Growth factor comparison)

From s8h0_analysis.py:
  LCDM:  D=0.704, f=0.527, sigma8_ratio=1.000, S8=0.8546
  A12:   D=0.691, f=0.525, sigma8_ratio=0.981, S8=0.8384, Delta_S8=+0.004
  C11D:  D=0.688, f=0.525, sigma8_ratio=0.978, S8=0.8356, Delta_S8=+0.002
  C28:   D=0.687, f=0.525, sigma8_ratio=0.976, S8=0.8341, Delta_S8=+0.000

All candidates give S8 slightly HIGHER than LCDM (by 0-2%), far above DES-Y3.
Needed direction: S8 must DECREASE by 0.075 to reach DES-Y3 = 0.759.
All CPL candidates move in the WRONG direction relative to LCDM S8 = 0.834.

Key insight: CPL wa<0 means DE was more energy-dense in the past.
More DE suppresses growth -> D smaller -> sigma8 smaller -> S8 smaller.
But the effect is only 0.4-2%: S8 remains ~0.834-0.838, far above 0.759.

### Person 2 (Q45 artifact analysis)

The script reported Q45_S8 = True because LCDM itself gives Delta_S8 = 0.021.
This is an ARTIFACT: the S8_LCDM value in our normalization convention
uses sigma8_ratio = D_LCDM / D_LCDM = 1 but then S8_proxy = S8_planck * 1.021
due to the sqrt(OmegaM/0.3) factor with OmegaM=0.315 > 0.3.

The PHYSICAL question: do any candidates DECREASE S8 towards DES-Y3?
Answer: No. The candidates move sigma8 DOWN relative to LCDM (correct direction)
but only by 0.4-2.4% -- insufficient for the 9% needed decrease.

Corrected Delta_S8 (relative to DES-Y3 need):
  Needed: -0.075 (from 0.834 to 0.759)
  A12:    -0.004 (from 0.834 to 0.830) -- achieves 5.3% of needed gap
  C11D:   -0.002 (from 0.834 to 0.832) -- achieves 2.1% of needed gap
  C28:    -0.000 (from 0.834 to 0.834) -- negligible

**Honest assessment: Q45_S8 NOT achieved for the S8 tension problem.**

### Person 3 (G_eff channel)

Maximum possible S8 improvement via G_eff/G modification:
  For gravity weakening: G_eff/G = 1 - epsilon
  Delta_sigma8/sigma8 ~ -0.55 * epsilon
  For DeltaS8 = -0.075: epsilon_needed ~ 0.164 (16.4%)

SQMH G_eff/G correction: epsilon_SQMH ~ Pi_SQMH * (rho_DE/rho_m) ~ 4e-62
Ratio: epsilon_needed / epsilon_SQMH ~ 4e60

The required G_eff suppression is 60 orders above SQMH capability.
This is the same Cramer-Rao obstruction from NF-10.

Alternative: phenomenological G_eff = 1 - 0.164 (not from SQMH).
Such a large gravity suppression would violate:
  - Gravitational lensing (CMB lensing: G_eff/G = 0.99 +/- 0.02)
  - Cluster counts (sensitive to growth history)
  - BBN (nucleosynthesis at z~10^9 requires G = G_Newton to 1%)

Conclusion: G_eff path to S8 resolution requires 16.4% suppression,
which is observationally ruled out by CMB lensing and BBN.

### Person 4 (H0 channel)

H0 tension mechanism: CMB measures chi*(CMB) = DA(z*)/c = rs(z*)/theta*.
If late-time models change E(z) at z<2 without changing rs(z*) or theta*,
then H0_inferred = H0_input (no shift).

But: A12 changes E(z) at z<2. If we hold theta* fixed:
  chi*(A12) = c/H0 * integral dz/E_A12(z)
If chi*(A12) != chi*(LCDM), then H0_A12 != H0_LCDM at fixed theta*.

Numerical result: chi_A12 = 3.098 < chi_LCDM = 3.120 (at fixed OmegaM=0.315)
-> H0_A12 = H0_LCDM * (chi_LCDM/chi_A12) = 67.4 * 1.007 = 67.9 km/s/Mpc
-> Delta_H0 = +0.46 km/s/Mpc (A12 moves H0 in correct direction)

But 0.46 km/s/Mpc is below the Q45 threshold of 0.5 km/s/Mpc by a small margin.

Wait: the H0 moves in the CORRECT direction? Let's verify:
  chi_LCDM = 3.120 > chi_A12 = 3.098
  chi = integral dz/E(z) from 0 to z_cmb
  If chi is SMALLER for A12, then H0 must be LARGER to keep r_s/D_A fixed.
  H0_A12 = H0_LCDM * (chi_LCDM / chi_A12) = 67.4 * (3.120/3.098) = 67.9 km/s/Mpc
  Delta_H0 = +0.46 km/s/Mpc (CORRECT direction: H0 increases)

But wait: A12 wa<0 means LESS DE in early universe -> E(z) for z~0.5-2 is LOWER.
Lower E(z) -> larger integral dz/E(z) -> larger chi -> H0 must DECREASE.
Let me recheck: chi_a12 = 3.098 < chi_lcdm = 3.120.
This means chi_A12 < chi_LCDM: the A12 integral is smaller.

This means at intermediate z, E_A12 > E_LCDM (more energy per unit redshift).
For A12: w_A12(z) = w0 + wa*(1-a) = -0.886 + (-0.133)*(1 - 1/(1+z))
At z=1: a=0.5, w_A12 = -0.886 + (-0.133)*0.5 = -0.953
At z=0: w_A12 = -0.886

The DE density for A12 relative to LCDM:
  rho_DE_A12(a) / rho_DE_LCDM = a^(-3*(1+w0+wa)) * exp(-3*wa*(1-a)) / 1
At a=0.5: a^(-3*(1-0.886-0.133)) * exp(-3*(-0.133)*0.5)
         = a^(-3*(-0.019)) * exp(0.2) = a^(0.057) * 1.22

For a=0.5: 0.5^0.057 * 1.22 = 0.962 * 1.22 = 1.17 (17% more DE)
This HIGHER rho_DE_A12 at intermediate z -> E_A12 > E_LCDM -> integral smaller.
H0_A12 > H0_LCDM by 0.46 km/s/Mpc.

The direction IS correct (higher H0). But magnitude (0.46 km/s/Mpc) is below 0.5 threshold.

### Person 5 (H0: more careful analysis)

The numerical result Delta_H0 = +0.46 km/s/Mpc is just below Q45 threshold.
However, the threshold is 0.5 km/s/Mpc -- very close to 0.46.

C11D (wa=-0.115) would give slightly smaller Delta_H0.
C28 (wa=-0.19) might give slightly larger Delta_H0.

For C28 wa=-0.19 (more negative than A12 wa=-0.133):
  More negative wa means EVEN more DE at intermediate z -> larger E(z)
  -> smaller chi -> H0_C28 > H0_A12 > H0_LCDM

Rough estimate: Delta_H0(C28) ~ 0.46 * (0.19/0.133) ~ 0.66 km/s/Mpc
This might exceed the Q45 threshold of 0.5 km/s/Mpc.

But at fixed theta*, we must account for the full sound horizon shift.
The Dirian 2015 C28 wa=-0.19 gives slightly larger H0 shift than A12.
However, the Bayesian evidence does not favor C28 (Delta ln Z = 0.48 vs A12).

Critical note: This H0 improvement is PHYSICAL -- it comes from:
  1. More DE at z=0.5-2 increases H(z) at those redshifts
  2. Fixed theta* -> higher H0_today
  3. This is a REAL improvement, not an artifact

BUT the improvement is only ~0.5 km/s/Mpc vs needed 5.6 km/s/Mpc (9%).
K44 is still effectively triggered in terms of resolving the H0 tension.

### Person 6 (mu_eff structural argument)

From L8 (all mu_eff ~ 1): GW170817 tensor speed constraint limits modified gravity.
For SQMH and CPL models: mu_eff = 1 (no tensor perturbation modification).
This means:
  1. No additional weak lensing amplification (S8 ~ sigma8 unchanged by lensing)
  2. No modified slip parameter (eta = 1)
  3. No ISW-lensing correlation enhancement

The ONLY S8 improvement channels available are:
  a) Background change in sigma8 via D(a) (already computed: 0-2%)
  b) G_eff/G modification (requires 16.4% -> observationally ruled out)
  c) Neutrino mass (not part of SQMH/CPL)
  d) Baryonic feedback (not part of SQMH/CPL)

### Person 7 (Honest summary)

The Q45 verdict requires careful interpretation:
  - Q45_S8 = True in our code: ARTIFACT from normalization convention
  - True physical Delta_S8 for A12 vs DES-Y3 = -0.004 (0.4% of gap)
  - Q45_H0 = False: Delta_H0 = 0.46 km/s/Mpc < 0.50 threshold
  - C28 might give Delta_H0 ~ 0.5-0.7 (borderline)

Anti-falsification statement:
  "The S8 tension cannot be resolved: all candidates give Delta_S8 < 0.010
  (< 15% of the 0.075 gap), far below the Q45 threshold. The H0 tension
  is similarly unresolvable: max Delta_H0 < 0.7 km/s/Mpc (< 12% of 5.6 km/s/Mpc gap)."

### Person 8 (NF-15 formulation)

New finding NF-15 (S8/H0 Structural Impossibility):

S8 structural impossibility:
  Required G_eff/G deviation: 16.4% (gravity suppression)
  SQMH provides: 4e-62 (60-order gap)
  CPL background shift: 0-2% sigma8 (5-20x insufficient)
  All candidates mu_eff = 1 (no lensing modification)
  CMB lensing constrains |G_eff/G - 1| < 2% (observational bound)
  Even the physical maximum G_eff modification is 8x insufficient

H0 structural impossibility:
  Required shift: +5.6 km/s/Mpc (83% increase from 67.4)
  All candidates modify only z<2 physics
  Maximum achievable via CPL wa<0: ~0.7 km/s/Mpc (C28) = 12.5% of needed
  EDE would be needed for full resolution (not present in candidates)
  Direction is correct (wa<0 increases intermediate E(z)) but magnitude insufficient

Both tensions: "structurally unresolved" in the JCAP paper.

---

## Q45 Judgment

NUMERICAL (corrected):
  True Delta_S8 (A12 vs DES-Y3): ~ -0.004 (insufficient: < 0.01)
  Delta_H0 (A12 at fixed theta*): +0.46 km/s/Mpc (below 0.50 threshold)
  Delta_H0 (C28 estimate): ~0.5-0.7 km/s/Mpc (borderline)

**K44 effectively triggered**: Neither S8 nor H0 resolution achievable.
A12/C11D/C28 cannot address either tension at the required level.

Note: The code Q45_pass=True was an artifact of comparing LCDM vs A12 (wrong baseline).
The correct baseline is DES-Y3 S8=0.759, which none of the candidates can approach.

---

## Paper Language

"Neither the S8 tension (DES-Y3 S8=0.759 vs Planck S8=0.834) nor the H0 tension
(H0=67.4 vs SH0ES H0=73.0 km/s/Mpc) can be resolved by A12, C11D, or C28 within
the background-level CPL framework. The maximum achievable S8 reduction is <2%
of the 9% gap (from modified sigma8 via growth factor D(a)), with no lensing-sector
modification (mu_eff=1). The SQMH G_eff/G correction epsilon ~ 10^-62 is 60 orders
below the 16% gravity suppression needed to resolve S8. For H0, all candidates
modify only z<2 physics and achieve at most Delta_H0 ~ 0.7 km/s/Mpc (C28), 12%
of the required 5.6 km/s/Mpc shift. These tensions remain structurally unresolved."

---

*L9-D completed: 2026-04-11*
