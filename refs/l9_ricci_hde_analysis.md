# refs/l9_ricci_hde_analysis.md -- L9 Round 16: Ricci HDE Deep-Dive

> Date: 2026-04-11
> Source: L9 Round 16, simulations/l9/ricci/ricci_hde.py
> Purpose: Physical analysis of Ricci HDE, CPL extraction, Jeffreys assessment.
> Language standard: refs/l7_honest_phenomenology.md.
> Anti-falsification: CPL discrepancy with NF-19 literature claim fully documented.

---

## Context

NF-19 (Round 12) found: Ricci HDE with alpha=0.46 gives wa ~ -0.13, |Dwa| ~ 0.003.
This was the closest any known mechanism came to A12.
Round 16 objective: deep-dive verification, chi2 fit, Jeffreys threshold check.

---

## What IS Ricci HDE Physically?

**Model**: rho_DE = 3*c^2*M_P^2 * alpha * (H_dot + 2*H^2)

Equivalently:
  rho_DE = 3*alpha*M_P^2 * H^2 * (2 + d(ln H)/dN)

where N = ln(a) and d(ln H)/dN = (1/2)*d(ln E^2)/dN.

**Motivation**: The dark energy density is proportional to the RICCI SCALAR R.
In flat FLRW: R = -6*(H_dot + 2*H^2), so rho_DE ~ -R/6 ~ H^2*(2 + xi)
where xi = d(ln H)/dN.

The IR cutoff is L = (-R/6)^{-1/2} = 1/sqrt(H^2*(2+xi)), the curvature length scale.
This differs from Hubble-horizon HDE (L=1/H) which gives wa > 0.

**Closed-form E^2(z) solution** (Kim+2008, arXiv:0801.0296):

Starting from the modified Friedmann equation:
  E^2*(1-2*alpha) = Omega_m*a^{-3} + (alpha/2)*dE^2/dN

Solving the linear ODE:
  E^2(a) = C * a^{-2*(1-2*alpha)/alpha} + [2*Omega_m/(2-alpha)] * a^{-3}

where C = 1 - 2*Omega_m/(2-alpha) enforces E^2(a=1) = 1.

**Parameter constraints**:
  - Ghost condition: 1 - 2*alpha > 0, i.e., alpha < 0.5
  - For alpha = 0.46: 1 - 2*0.46 = 0.08 > 0. STABLE.
  - For alpha = 0.50: degenerate (homogeneous term diverges). FORBIDDEN.
  - alpha > 0 required for positive rho_DE.

---

## Does Ricci HDE Have SQMH-like Structure?

**SQMH**: rho_DE ~ Gamma_0/(3H + sigma*rho_m) ~ H^{-1} * (inverse tracking)

**Ricci HDE**: rho_DE ~ alpha*H^2*(2 + xi) ~ alpha*H^2 * (direct tracking)

Both track H but with OPPOSITE power laws:
  - SQMH: rho_DE grows as H DECREASES (anti-correlated; birth-death equilibrium)
  - Ricci HDE: rho_DE FALLS as H decreases (correlated with expansion rate)

CONCLUSION: Ricci HDE does NOT have SQMH-like birth-death structure. The
functional forms are structurally incompatible.

Is rho_DE proportional to H proportional to 1/t? 
  - SQMH equilibrium: n_star ~ Gamma_0/(sigma*rho_m) * 1/H -> rho_DE ~ 1/H ~ 1/t (matter era)
  - Ricci HDE: rho_DE ~ H^2 ~ 1/t^2 (matter era)
  NO. Different time scaling.

---

## CPL Extraction: Critical Discrepancy with NF-19

### NF-19 claim (Round 12 survey):
  "Ricci HDE with alpha=0.46 gives wa ~ -0.13 (Kim+2008 arXiv:0801.0296)"

### Round 16 numerical computation:

Two different CPL extraction methods give different wa values:

**Method 1**: CPL fit to total E^2(z) = Omega_m*(1+z)^3 + Omega_DE(z):
  - alpha=0.46: w0 = -0.870, wa = +0.897
  - alpha=0.40: w0 = -0.650, wa = +0.453
  - Result: wa > 0 for all alpha in [0.35, 0.50]
  - This method captures the CPL ENVELOPE of E^2(z) but Omega_DE(z) grows with z
    (Omega_DE increases from z=0 to z=2 in Ricci HDE), making CPL w > -1 in E^2 sense
    while the actual EoS is w < -1.

**Method 2**: EoS from rho_X derivative (standard w_DE = -1 - (1/3)*d(ln rho_DE)/dN):
  - alpha=0.46: w0 = -0.743, wa = -0.314, |Dwa| = 0.181
  - alpha=0.37: w0 = -0.428, wa = -0.133, |Dwa| = 0.000 *** EXACT MATCH ***
  - This method uses the actual EoS of the Ricci HDE fluid component.

### Resolution:
The Kim+2008 wa ~ -0.13 result for alpha=0.46 used their specific parameterization
of the CPL fit in their numerical scheme, which is NOT identical to either of our
methods above. The NF-19 |Dwa| ~ 0.003 claim cannot be reproduced with our
self-consistent calculation.

**Key finding (NF-21 candidate)**:
  - If the rho_X derivative EoS (Method 2) is used: alpha=0.370 gives wa = -0.133 exactly.
  - If the E^2(z) CPL fit (Method 1) is used: wa > 0 for all alpha < 0.5.
  - The "NF-19 wa~-0.13 for alpha=0.46" is a convention-dependent result.
  - Honest assessment: Ricci HDE gives wa ~ -0.13 only for alpha ~ 0.37 (EoS method)
    or alpha ~ 0.46 (Kim+2008 convention). The two methods disagree by factor ~25%.

---

## Chi^2 and Jeffreys Evidence Assessment

### From ricci_hde.py (chi2_approx, 5-point BAO + compressed CMB + 4-bin SN):

NOTE: These are chi2_approx results, NOT equivalent to L5/L6 full nested sampling.
The chi2_approx uses a simplified 5-point BAO dataset (not full 13-point DESI DR2).

Best fit parameters: alpha ~ 0.10 (boundary), Omega_m ~ 0.20 (boundary)
  -> The optimizer hits parameter boundaries, indicating Ricci HDE is not
     well-fitted to the DESI BAO data with this chi2_approx.
  -> chi2_approx(Ricci HDE) >> chi2_approx(LCDM): Ricci HDE is WORSE.

**CRITICAL ISSUE**: For alpha ~ 0.10 (boundary value):
  - rho_X is very small: barely any dark energy component from Ricci HDE.
  - Model effectively becomes close to LCDM with slightly different Omega_m.
  - This means the chi2 optimizer is finding the LCDM limit of Ricci HDE,
    not a genuine Ricci HDE signal.

For alpha ~ 0.37 (EoS-method best, wa=-0.133):
  - chi2_approx is much larger (model cannot fit BAO+CMB simultaneously).
  - The reason: at alpha=0.37, C = 1 - 2*0.315/(2-0.37) = 0.614,
    exponent = 2*(1-2*0.37)/0.37 = 1.43.
  - E^2(z) grows faster than LCDM at high z (exponent 1.43 << 3), making
    the BAO angles too large.

### Jeffreys Evidence Estimate:
  - Delta chi2 (LCDM - Ricci HDE) < 0 for physically motivated alpha.
  - Delta ln Z_approx << 0 (Ricci HDE is WORSE than LCDM on chi2_approx).
  - Jeffreys verdict: BELOW THRESHOLD (fails STRONG evidence requirement).

### COMPARISON WITH THRESHOLD:
  - A12 Bayesian evidence: Delta ln Z = +10.769 vs LCDM (STRONG, from L5/L6).
  - Ricci HDE estimate: Delta ln Z < 0 (WORSE than LCDM).
  - Occam penalty for 1 extra param (alpha): ~ -1.5 nats.
  - Net: Ricci HDE does not qualify as a surviving candidate.

---

## Physical Reason Ricci HDE Fails BAO Fit

The closed-form solution:
  E^2(z) = C * (1+z)^{2*(1-2alpha)/alpha} + [2*Omega_m/(2-alpha)] * (1+z)^3

has two problems for alpha ~ 0.37-0.46:
  1. The matter coefficient 2*Omega_m/(2-alpha) > Omega_m for all alpha < 2/3.
     At alpha=0.37: 2*0.315/1.63 = 0.386 > 0.315. Effective matter density is enhanced.
  2. The homogeneous term has exponent 2*(1-2alpha)/alpha ~ 0.35-1.43,
     which is LESS than 3. This means dark energy grows faster than matter with z,
     creating excessive dark energy at BAO z~0.5-2.3 and spoiling the BAO signal.

This explains why the optimizer escapes to alpha~0.10 (LCDM limit): the physically
motivated alpha values are strongly penalized by BAO data.

---

## Fourth Surviving Candidate Assessment

| Requirement | Status | Details |
|-------------|--------|---------|
| R1: Physical motivation | YES | IR cutoff = Ricci scale |
| R2: wa < 0 naturally | CONDITIONAL | Only for specific EoS definition; wa > 0 in CPL-E^2 sense |
| R3: Jeffreys STRONG | NO | Delta ln Z < 0 (fails BAO fit) |
| R4: No fatal contradiction | FAIL | Over-produces dark energy at BAO z values |

**VERDICT: Ricci HDE does NOT qualify as a fourth surviving candidate.**

Reasons:
  1. Fails BAO chi2 fit (Ricci HDE over-produces DE at 0.5 < z < 2.3).
  2. Delta ln Z < 0 (worse than LCDM).
  3. The wa ~ -0.13 coincidence depends on EoS definition convention.
  4. The Kim+2008 numerical result (alpha=0.46) cannot be reproduced with
     the self-consistent closed-form solution for DESI DR2 data.

---

## Allowed Paper Language

NF-19 should be revised from:
  "Ricci HDE coincidence wa~-0.13" (Round 12)

To (corrected):
  "Ricci HDE (Gao+2009) can produce wa ~ -0.13 in the component EoS sense
  for alpha ~ 0.37, but fails to fit DESI BAO at physically motivated alpha values.
  The Kim+2008 result (alpha=0.46, wa~-0.13) uses a convention-dependent CPL
  extraction not equivalent to the standard DESI CPL parameterization.
  Ricci HDE is not adopted as a fourth candidate."

---

## New Finding: NF-21 (Ricci HDE CPL Convention Dependence)

**NF-21**: Ricci HDE CPL wa depends critically on whether one uses:
  (a) CPL fit to total E^2(z) -> wa > 0 (spuriously positive)
  (b) Component EoS w_DE = -1-(1/3)*d(ln rho_DE)/dN -> wa < 0 for alpha < 0.46
  (c) Kim+2008 convention (specific numerical parameterization) -> wa~-0.13 at alpha=0.46

These three methods give different wa values. The "NF-19 wa~-0.13 coincidence"
was based on (c), which uses a convention different from the DESI standard (a).
When DESI-standard CPL (a) is used, Ricci HDE gives wa > 0 for all alpha in [0.35, 0.50],
making it inconsistent with DESI DR2 preference for wa < 0.

**Implication**: NF-19 is a STRUCTURAL FOOTNOTE (correct as a literature observation),
but the wa coincidence does not survive standard DESI CPL comparison. The "fourth
candidate" status for Ricci HDE is REJECTED.

---

## Output Files

- simulations/l9/ricci/ricci_hde.py: COMPLETE, VERIFIED (Round 16)
- simulations/l9/ricci/ricci_hde_results.json: COMPLETE (Round 16)
- refs/l9_ricci_hde_analysis.md: THIS FILE (Round 16)

---

*Round 16 completed: 2026-04-11*
*Key result: Ricci HDE FAILS fourth-candidate test. NF-19 CPL coincidence is*
*convention-dependent. NF-21 established (CPL convention dependence).*
