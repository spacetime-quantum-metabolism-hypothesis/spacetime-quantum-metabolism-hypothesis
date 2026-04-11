# refs/l8_round5_verdict.md -- L8 Round 5: Dimensional Analysis / Buckingham Pi

> Date: 2026-04-11
> Round 5 of 5 additional rounds (Rounds 2-6).
> Method: 8-person parallel team, simultaneous independent attack angles,
>   immediate cross-sharing, deliberation, final consensus.
> Focus: Dimensional analysis / Buckingham pi -- what are the dimensionless
>   groups of each candidate? Can they be mapped to SQMH's Gamma_0/(sigma*rho_m)?
> Prior established: Q31/Q32/Q33 FAIL (Rounds 1-4).

---

## Attack Angle: Dimensional Analysis / Buckingham Pi Theorem

Question: What are the natural dimensionless numbers of each system?
Is there a dimensionless Pi-group common to SQMH and any candidate?

---

## SQMH Fundamental Parameters

Physical parameters of SQMH:
  sigma = 4pi*G*t_P = 4.52e-53 m^3/(kg*s)   [somatic coupling]
  Gamma_0 = [source rate]                     [s^-1, if n_bar ~ m^-3]
  n_bar ~ [m^-3]                              [number density]
  rho_m ~ [kg/m^3]                            [matter density]
  H ~ [s^-1]                                  [Hubble rate]

SQMH dimensionless groups (Buckingham Pi):

Pi_1 = sigma * rho_m / (3H) = 1.83e-62  [ratio: somatic loss / Hubble dilution]
Pi_2 = Gamma_0 / (3H * n_bar)           [ratio: production / Hubble dilution]
Pi_3 = Pi_1 / Pi_2 = sigma * rho_m * n_bar / Gamma_0  [loss/production]

Stationary solution (dn/dt=0): Gamma_0 = 3H*n_bar + sigma*n_bar*rho_m
  -> Pi_2 = 1 + Pi_1 ~ 1 (since Pi_1 ~ 10^-62)

Fundamental SQMH dimensionless ratio:
  Pi_SQMH = Gamma_0 / (sigma * rho_m * n_bar) ~ 1/Pi_1 ~ 10^62  [huge]

Interpretation: SQMH production dominates loss by 62 orders of magnitude.
The quasi-static n_bar ~ Gamma_0/(3H) (production-Hubble balance, not production-loss).

---

## 8-Person Parallel Discussion

### [Member 1 -- Buckingham Pi for A12]

A12 parameters: {Omega_m, H_0, z_transition} or just {Omega_m, H_0} for zero-param.

Dimensionless groups of A12:
  Pi_A12_1 = Omega_m  [density fraction]
  Pi_A12_2 = w0 = -0.886  [EOS today]
  Pi_A12_3 = wa = -0.133  [EOS evolution]

A12 has NO sigma-like parameter. The erf proxy is dimensionless by construction:
  E^2(z) / E^2(z=0) [ratio of Hubble rates -- dimensionless]

The SQMH dimensionless ratio Pi_SQMH = Gamma_0/(sigma*rho_m*n_bar) has no
analog in A12. A12 has no coupling between DE and matter fields.

Buckingham Pi verdict for A12: Incompatible dimensionless group structure.
No Pi-group mapping to SQMH Gamma_0/(sigma*rho_m) exists.

### [Member 2 -- Buckingham Pi for C11D]

C11D (CLW exponential quintessence) parameters:
  {lambda, M_P, H_0, Omega_m}

Dimensionless groups of CLW:
  Pi_CLW_1 = lambda = 0.8872  [slope of potential]
  Pi_CLW_2 = x = phi_dot/(sqrt(6)*H*M_P)  [kinetic fraction]
  Pi_CLW_3 = y = sqrt(V/(3H^2*M_P^2))  [potential fraction]
  Pi_CLW_4 = Omega_phi = x^2 + y^2  [DE fraction]
  Pi_CLW_5 = Omega_m = 1 - x^2 - y^2  [matter fraction]

The lambda parameter has dimension [M_P^-1] in the exponent:
  V = V_0 * exp(-lambda * phi / M_P)

So lambda is already dimensionless. Key CLW ratio:
  Pi_CLW_key = sqrt(6)*lambda*x / (3*(1-w_phi)*Omega_phi)
  [tracker condition ratio -- =1 at tracker]

Does C11D have a Pi-group analogous to SQMH's Gamma_0/(sigma*rho_m)?

SQMH Pi ~ Gamma_0 / (sigma * rho_m): ratio of source to collision rate.
CLW equivalent: There is no "collision rate" in CLW. The scalar field
loses energy via phi'' + 3H*phi' = -V'(phi), but this is conservative
(energy goes to dark energy, not removed by collision with matter).

For pure disformal (A'=0) CLW with no direct coupling: matter is NOT coupled
to phi in the equations of motion. There is no sigma_CLW * rho_m term.

Pi-group verdict: C11D has no Buckingham Pi group analogous to sigma*rho_m.
Incompatible dimensionless group structure.

### [Member 3 -- Buckingham Pi for C28]

C28 (RR non-local gravity) parameters:
  {gamma_0, H_0, Omega_m, m^2 = gamma_0 * H_0^2}

Dimensionless groups of C28:
  Pi_RR_1 = gamma_0 = 0.0015  [non-local coupling]
  Pi_RR_2 = m^2/H^2 = gamma_0 * H_0^2/H^2  [mass ratio]
  Pi_RR_3 = U(a)  [auxiliary field, dimensionless by convention]
  Pi_RR_4 = V(a)  [second auxiliary field]

The key RR dimensionless group is Pi_RR_1 = gamma_0 = m^2/H_0^2.

SQMH key dimensionless group: Pi_1 = sigma * rho_m / (3H) ~ 10^-62.

RR to SQMH Pi-group mapping attempt:
  sigma * rho_m / H  <-->  gamma_0 * H  ?

[sigma * rho_m / H] = [4pi*G*t_P * rho_m / H]
                    = [(G*rho_m/H) * (t_P)]
                    = [(rho_m/rho_crit) * (H^-1) / H * (t_P) * H^2 / G]

This mapping does not simplify. Dimensions:
  sigma * rho_m / H ~ [4pi*G*t_P*rho_m/H] ~ [G*t_P*rho_m/H]
    = [m^3/(kg*s) * kg/m^3 / (s^-1)] = dimensionless.  CHECK.

  gamma_0 * (H/H_0)^2: dimensionless.  CHECK.

Setting them equal:
  sigma * rho_m / H = gamma_0 * (H/H_0)^2
  => 1.83e-62 * (H_0/H) = gamma_0 * (H/H_0)^2
  [at z=0, H=H_0]: 1.83e-62 = gamma_0 = 0.0015.  
  RATIO = 1.83e-62 / 0.0015 = 1.2e-59.

  These are 59 orders apart. Not a valid Pi-group mapping.

### [Member 4 -- Natural scales and Pi-group table]

Summary table of natural Pi-groups for each system:

System | Key dimensionless groups | SQMH Pi analog?
-------|-------------------------|----------------
SQMH  | Pi_1 = sigma*rho_m/(3H) = 1.83e-62 | self
       | Pi_2 = Gamma_0/(3H*n_bar) ~ 1 |
       | Pi_SQMH = Gamma_0/(sigma*rho_m*n_bar) ~ 10^62 |
A12   | w0 = -0.886, wa = -0.133 | NO analog for sigma
C11D  | lambda = 0.8872, Omega_phi(z=0) ~ 0.7 | NO collision Pi
C28   | gamma_0 = 0.0015, m^2/H_0^2 = gamma_0 | Pi_RR_1/Pi_SQMH_1 = 10^59

Key observation: SQMH Pi_1 = 10^-62 is UNIQUELY small.
No candidate has a natural Pi-group at this scale.

The "scale separation" that emerged in Round 1 (background ODE) is
confirmed by dimensional analysis: 10^-62 is not a coincidence number
appearing in any cosmological theory. It is the ratio:
  G * t_P * rho_m / H = G^(3/2) * hbar^(1/2) * rho_m / (c^(5/2) * H)

This contains t_P = sqrt(hbar*G/c^5) -- a purely quantum gravity quantity.
No classical cosmological model has this Planck-scale coupling.

### [Member 5 -- Inverse Pi-group: could sigma be emergent?]

Question: Could sigma be constructed from C11D or C28 parameters via
a combination of Pi-groups?

From C11D:
  sigma_CLW = [H_0 / rho_m0] * f(lambda)
  Dimensionless ratio: sigma_CLW / sigma_SQMH = (H_0/rho_m0) / (4pi*G*t_P)
  = (H_0 * M_P) / (4pi * G * rho_m0 * t_P)
  = (H_0 / H_Planck) * (rho_Planck / (4pi * rho_m0))

  H_Planck = 1/t_P ~ 10^43 s^-1, H_0 ~ 2e-18 s^-1
  -> H_0/H_Planck ~ 2e-61.

  rho_Planck = m_P*c^2/l_P^3 ~ 5e96 kg/m^3, rho_m0 ~ 2.6e-27 kg/m^3
  -> rho_Planck/(4pi*rho_m0) ~ 1.6e122.

  sigma_CLW/sigma_SQMH ~ (2e-61) * (1.6e122) ~ 3e61.

So sigma_CLW ~ 3e61 * sigma_SQMH. Ratio off by 61 orders (as found in Round 1).

No combination of CLW Pi-groups can be made equal to SQMH Pi_1 without
introducing t_P explicitly. The Planck time is not a parameter of CLW.

From C28:
  sigma_RR = gamma_0 * H_0 / rho_m0
  sigma_RR / sigma_SQMH = gamma_0 * H_0 / (rho_m0 * 4pi*G*t_P)
  = gamma_0 * (H_0/H_Planck) * (rho_Planck/(4pi*rho_m0))
  ~ 0.0015 * (2e-61) * (1.6e122) ~ 4.8e58.

  sigma_RR ~ 4.8e58 * sigma_SQMH. Ratio off by 59 orders.

Member 5 finding: In all cases, bridging to sigma_SQMH requires explicitly
introducing t_P. No Pi-group in C11D or C28 contains t_P.

### [Member 6 -- NEW FINDING: The Planck-time Pi-group uniqueness]

NEW FINDING (flagged):

From the analysis so far, a pattern emerges:

The Pi-group Pi_SQMH = sigma*rho_m/(3H) = G*t_P*rho_m/H can be written as:

  Pi_SQMH = (G*rho_m/H^2) * (H*t_P)
           = Omega_m * (H*t_P)

where Omega_m = G*rho_m/H^2 (order 0.3) and (H*t_P) = H/H_Planck ~ 10^-61.

This factorizes as:
  Pi_SQMH = Omega_m * (H_0/H_Planck) = 0.3 * 2e-18 / (1/t_P)
           ~ 0.3 * 2e-18 * 5.4e-44 = 3.2e-62 ~ 10^-62.  CONSISTENT.

Key insight: Pi_SQMH = Omega_m * (H_0 * t_P) is the product of:
  (a) Omega_m ~ 0.3 [dimensionless cosmological parameter]
  (b) H_0 * t_P ~ 10^-61 [ratio of Hubble time to Planck time]

The ratio of Hubble time to Planck time:
  t_Hubble / t_Planck = (1/H_0) / t_P = 1/(H_0 * t_P) ~ 10^61.

This is the "hierarchy problem" of cosmology (horizon problem / age problem).
Pi_SQMH^-1 ~ 10^62 IS the ratio of cosmic time to Planck time.

NEW FINDING: "The SQMH somatic coupling sigma is uniquely characterized by
the Pi-group Pi_SQMH = Omega_m * (H_0 * t_P) ~ 10^-62, which equals the
inverse of the Hubble-to-Planck time ratio. This Pi-group appears in NO
classical cosmological candidate theory (A12, C11D, C28) because none of
them contain t_P as a parameter. The 62-order scale separation between
SQMH and the cosmological candidates is therefore not a numerical accident
but a STRUCTURAL consequence of the absence of Planck-time in standard
dark energy theory."

This finding does NOT help bridge the gap but EXPLAINS WHY the gap is
irreducible: it would require introducing quantum gravity (t_P) into
the classical cosmological models.

### [Member 7 -- Pi-group: could any combination work?]

Exhaustive search: Can any combination of C11D parameters equal Pi_SQMH?

C11D parameters: {lambda=0.8872, Omega_phi~0.7, Omega_m~0.3, w0~-0.9, wa~-0.1}
All are dimensionless and of order unity. No Planck-scale parameter.

Any product of these would be of order 10^0 - 10^-2 at most.
To reach Pi_SQMH ~ 10^-62: impossible from O(1) dimensionless parameters.

Can any ratio of C28 parameters equal Pi_SQMH?

C28: {gamma_0=0.0015, Omega_m=0.3, w0~-1.0, wa~-0.19}
Smallest parameter: gamma_0 = 1.5e-3.
Gamma_0^n for the ratio: (1.5e-3)^n = 10^-62 -> n = 62/3 ~ 21.

Pi_C28_candidate = gamma_0^21 ~ (1.5e-3)^21 = 10^-62.5. MATCHES!

Team immediate discussion: Is Pi_C28 = gamma_0^21 a meaningful Pi-group?

Assessment: gamma_0^21 is dimensionless but it has NO physical interpretation
as a first-principles Pi-group (Buckingham theorem requires constructing
Pi from the natural scales of the problem, not arbitrary powers).
gamma_0^21 would require a 21-body interaction, which has no motivation.

Verdict: Pi_C28 = gamma_0^21 is a mathematical coincidence, not a physical
Pi-group mapping. DISMISSED.

### [Member 8 -- Pi-group: can Planck units bridge?]

Final question: If we work in Planck units where t_P = 1, does SQMH
become compatible with the cosmological candidates?

In Planck units:
  sigma_Planck = 4pi*G_Planck * 1 = 4pi (since G=1, t_P=1 in Planck units)
  rho_m_Planck = rho_m / rho_Planck ~ 2.6e-27 / 5e96 = 5.2e-124
  H_Planck = H_0 * t_P = 2e-18 * 5.4e-44 = 1.1e-61

  Pi_SQMH_Planck = sigma_Planck * rho_m_Planck / (3 * H_Planck)
                 = 4pi * 5.2e-124 / (3 * 1.1e-61)
                 = 4pi * 5.2e-124 / 3.3e-61
                 = 2e-63 ~ 10^-62.  SAME RESULT.

Working in Planck units does NOT change the dimensionless ratio. The scale
separation is physical, not a unit artifact.

In Planck units, for C11D:
  sigma_need_Planck = H_Planck / rho_m_Planck = 1.1e-61 / 5.2e-124 = 2.1e62.
  sigma_need / sigma_SQMH = 2.1e62 / 4pi = 1.7e61.

The 61-order gap persists in ALL unit systems. This confirms the gap is
fundamental and not a units issue.

---

## Round 5 Team Consensus

**Dimensional Analysis / Buckingham Pi Results:**

SQMH key Pi-groups:
  Pi_1 = sigma * rho_m / (3H) = Omega_m * (H_0 * t_P) ~ 10^-62
  Pi_2 = Gamma_0 / (3H * n_bar) ~ 1

| Candidate | Key Pi-groups | Pi analog to Pi_1? | Gap |
|-----------|---------------|--------------------|-----|
| A12 | w0, wa, Omega_m [O(1)] | NONE | N/A |
| C11D | lambda, Omega_phi [O(1)] | NONE | >61 orders |
| C28 | gamma_0=1.5e-3, Omega_RR | NONE (gamma_0^21 coincidence) | >59 orders |

**NEW FINDING (structural insight):**
Pi_SQMH = Omega_m * (H_0 * t_P) = product of cosmological parameter
and Planck-time ratio. This Pi-group REQUIRES t_P (quantum gravity input).
No classical dark energy model (A12, C11D, C28) contains t_P.
The 62-order scale separation is STRUCTURALLY irreducible without
introducing quantum gravity parameters into the classical candidates.

Language for paper: "The SQMH somatic coupling sigma defines the
Pi-group Pi_1 = Omega_m * H_0 * t_P ~ 10^-62, which embeds the
Planck time into cosmological dynamics. No dark energy candidate
considered here contains a corresponding quantum gravity parameter,
rendering the scale separation structurally irreducible at the
classical cosmological level."

**Round 5 Verdict:**
- Q31/Q32/Q33: REMAIN FAIL.
- Dimensional analysis confirms: the 62-order gap is not a numerical
  accident but a structural consequence of SQMH requiring quantum
  gravity input (t_P) absent from all candidates.
- NEW FINDING: Pi_SQMH = Omega_m * H_0 * t_P identified as the
  fundamental dimensionless characterization of SQMH cosmological limit.

---

*Round 5 complete: 2026-04-11*
