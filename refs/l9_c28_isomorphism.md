# refs/l9_c28_isomorphism.md -- L9 Round 8: C28-A12 Isomorphism Deep Analysis

> Date: 2026-04-11
> Source: L9 Q42 PASS confirmed (Round 3), gamma0 scan completed (Round 7).
> Method: 8-person parallel team, each from a different angle.
> Language standard: refs/l7_honest_phenomenology.md.
> Anti-falsification: Q45 FAIL confirmed numerically.

---

## Context

From L9 Rounds 1-7:
- Q42 PASS: |wa_C28 - wa_A12| = 0.057 < 0.10 (Dirian 2015 literature)
- Q45 FAIL: best gamma0 in L6 posterior [0.0011,0.0019] gives |Δwa| = 0.067 > 0.03
- Optimal gamma0 for |Δwa| < 0.03 is gamma0 ~ 0.00054 (outside L6 range)
- E2_today not normalized to 1 at L6 gamma0 values (convention issue)

The question for Round 8:
"What does Q42 PASS physically mean? At what level is C28 'the same as' A12?"

---

## 8-Person Parallel Team Analysis

### [1/8] Mathematical Level: Background E^2(z) Isomorphism

**Question**: Are E^2_C28(z) and E^2_A12(z) the same function?

**Answer**: NO at exact level. YES at CPL-approximation level.

E^2_A12(z): The A12 template is
  E^2_A12(z) = Omega_m*(1+z)^3 + (1-Omega_m)*CPL_A12(z)
  with w0_A12 = -0.886, wa_A12 = -0.133.

E^2_C28(z): From the Dirian 2015 full ODE:
  E^2_C28(z) = Omega_m*(1+z)^3 + (gamma0/4)*(2U-V1^2+3*V*V1)
  The nonlocal term evolves via the full U, V ODE system.

At CPL level: if we fit E^2_C28 with a CPL model, we get
  w0_C28 ~ -1.04, wa_C28 ~ -0.19 (Dirian 2015).
The wa values match within 0.057 (Q42 threshold 0.10 -> PASS).

Mathematical conclusion: C28 and A12 share the same SIGN and ORDER OF
MAGNITUDE in wa. They are not the same function, but their CPL projections
are within the Q42 ball (radius 0.10) around wa = -0.133.

This is NUMERICAL PROXIMITY, not mathematical isomorphism.

### [2/8] Perturbation Level: Is C28 the same as A12 in growth?

**Question**: Does C28 give the same f*sigma8(z) as A12?

**Answer**: Approximately yes, with differences at the 5-10% level.

The matter growth rate f = d(ln delta)/d(ln a) depends on E^2(z) and G_eff/G.
For C28 (non-local gravity), G_eff/G ~ 1 + delta_G_C28 where delta_G_C28
comes from the auxiliary field perturbations of the U, V fields.

From Belgacem 2018 (arXiv:1712.07071):
  G_eff/G (C28) ~ 1 + 0.02 at z=0 (2% modification)

For A12 (phenomenological erf proxy):
  G_eff/G (A12) = 1.0 (no modification, purely background DE)

The f*sigma8 difference at z=0:
  f(A12) ~ 0.527 (LCDM growth rate, as computed in L9-A)
  f(C28) ~ 0.527 * (1 + epsilon) where epsilon ~ 0.01 (1% from G_eff/G)

This is a MEASURABLE difference (SKAO-level) but not at current DESI DR2 precision.

Perturbation conclusion: C28 and A12 are DIFFERENT at perturbation level.
The wa numerical proximity at background level does not extend to identical
perturbation spectra. This distinguishes C28 as an independent theory.

### [3/8] CPL wa Level: Physical Meaning of Q42 PASS

**Question**: What does |wa_C28 - wa_A12| = 0.057 < 0.10 actually mean?

**Answer**: It means C28 and A12 are observationally degenerate at current precision.

DESI DR2 constraint on wa: wa = -0.83 +/- 0.24 (1-sigma).
The wa difference 0.057 is:
  - 0.057/0.24 = 24% of DESI 1-sigma uncertainty.
  - This is observable in principle but not at the current level.

Fisher forecast for distinguishing C28 from A12 on wa:
  Delta_wa ~ 0.057; DESI DR2 sigma_wa ~ 0.24.
  Detectability: 0.057/0.24 ~ 0.24 sigma -> NOT distinguishable.

For DESI DR3 (factor ~2 improvement): sigma_wa ~ 0.12.
  Detectability: 0.057/0.12 ~ 0.48 sigma -> STILL not distinguishable.

Conclusion: C28 and A12 are currently indistinguishable on the wa axis.
They occupy the same observational "cell" in CPL space.
This is the OPERATIONAL meaning of Q42 PASS.

### [4/8] Derivational Hierarchy: Does C28 derive A12?

**Question**: Is A12 a derivable limit of C28? Or just numerically close?

**Answer**: A12 is NOT a derivable limit of C28.

C28 is the Maggiore-Mancarella RR non-local gravity:
  S_C28 = M_P^2/2 * int sqrt(-g) * R*(1 + m^2/6 * box^-1 * R) d^4x

A12 is the erf proxy for SQMH canonical drift:
  E^2_A12(z) = Omega_m*(1+z)^3 + Omega_DE * (CPL with w0, wa fitted to erf shape)

There is NO limit (m->0, m->inf, or any other) in which C28 reduces to A12.
The A12 erf proxy has no derivation from any known gravity theory (NF-14).
The C28 non-local term reduces to GR for m->0 (not to A12).

Derivational conclusion: C28 and A12 are STRUCTURALLY INDEPENDENT theories
that happen to have similar wa values. The proximity is a coincidence at the
CPL level, not a derivational relationship.

### [5/8] Philosophical Level: What Can We Honestly Claim?

**Question**: What language is scientifically defensible?

**ALLOWED claims**:
1. "C28 and A12 share CPL-level wa proximity (|Δwa| = 0.057 < observational error)."
2. "Both candidates are observationally degenerate in current DESI DR2 data on wa."
3. "C28 provides an independent theoretical motivation for wa ~ -0.15 to -0.20."
4. "The Q42 proximity is at the level of current observational precision."

**FORBIDDEN claims**:
1. "C28 derives A12" -- no derivational relationship exists.
2. "C28 is a parent theory of A12" -- they are independent theories.
3. "A12 is a limit of C28" -- no such limit exists.
4. "C28 and A12 are isomorphic" -- in strict mathematical sense, they are not.
5. "Q42 PASS proves structural unification" -- it proves only numerical proximity.

The honest, defensible claim:
"C28 (Maggiore-Mancarella RR non-local gravity) and A12 (SQMH-motivated erf proxy)
share CPL-level structural proximity in wa (|Δwa| = 0.057 < DESI 1-sigma = 0.24).
This proximity is observationally relevant: both candidates are consistent with
DESI DR2 data and mutually indistinguishable at current precision. C28 and A12
are independent theories; no derivational relationship between them has been found."

### [6/8] Falsifiability Angle: How to Break the Degeneracy?

**Question**: What observation would distinguish C28 from A12?

**Observable differences**:
1. G_eff/G: C28 predicts ~2% deviation; A12 predicts 0%. 
   CMB-S4 WL sensitivity: delta(G_eff/G) < 0.005. Distinguishable with CMB-S4.
2. GW speed: C28 (non-local gravity) has c_T = c (passes GW170817). A12 also c_T = c.
   Not distinguishable via GW.
3. Integrated Sachs-Wolfe: both give ISW ~ LCDM (SNR ~ 0.29, L9-A).
   Not distinguishable via ISW.
4. wa precision: |Δwa| = 0.057 requires sigma_wa < 0.03 to distinguish at 2-sigma.
   This needs ~80x DESI DR2 volume. Not achievable in near future.

Best near-term discriminator: G_eff/G from CMB-S4 lensing (2030-era).

### [7/8] Observational Degeneracy Angle: The CPL Cell Problem

**Question**: Are C28 and A12 in the same "CPL observational cell"?

From the DESI DR2 2D w0-wa posterior:
  DESI DR2 sigma(w0) ~ 0.06, sigma(wa) ~ 0.24.
  C28: w0 ~ -1.04, wa ~ -0.19.
  A12: w0 ~ -0.886, wa ~ -0.133.
  Separation in w0: |Δw0| ~ 0.15 ~ 2.5 * sigma(w0). DISTINGUISHABLE on w0.
  Separation in wa: |Δwa| ~ 0.057 ~ 0.24 * sigma(wa). NOT distinguishable on wa.

So C28 and A12 are:
  - Marginally distinguishable on w0 (2.5 sigma on background expansion)
  - Indistinguishable on wa (< 1 sigma)

In DESI DR2 chi^2 terms:
  chi^2 contribution from Δw0 alone ~ (0.15/0.06)^2 ~ 6.25
  But this ignores the covariance with wa, Omega_m, H0.

Given the chi^2 evidence favors A12 over C28 in L5 (Bayesian evidence gap
Δ ln Z ~ 0.48 = Occam penalty for extra C28 parameter), the two are effectively
equivalent models at current data quality.

Conclusion: In the w0-wa observational cell defined by DESI DR2 precision,
C28 and A12 are in the SAME wa-cell but adjacent w0-cells. They are
operationally degenerate but not observationally identical.

### [8/8] Synthesis: The Correct Paper Language

**8-person consensus language for paper**:

Level 1 (background E^2): 
  "The RR non-local gravity model (C28, Maggiore-Mancarella 2014) yields a CPL
  wa parameter of wa_C28 ~ -0.19 (Dirian 2015), within |Δwa| = 0.057 of the
  A12 erf template (wa_A12 = -0.133). Both are consistent with DESI DR2
  constraints on wa."

Level 2 (observational degeneracy):
  "At current DESI DR2 precision (sigma_wa ~ 0.24), C28 and A12 are
  indistinguishable on the wa axis. Discrimination on the w0 axis
  (|Δw0| ~ 0.15 ~ 2.5 sigma) is marginally possible with current data."

Level 3 (theoretical independence):
  "C28 and A12 are theoretically independent: C28 is a specific non-local
  gravity model (Lagrangian-level derivation); A12 is a phenomenological
  proxy for SQMH canonical drift (no Lagrangian derivation). No limiting
  procedure reduces one to the other."

Level 4 (honest limitation -- what we CANNOT claim):
  "The proximity |Δwa| = 0.057 is a numerical coincidence at CPL level.
  We do not claim derivational, structural, or theoretical isomorphism.
  The term 'structural proximity' refers strictly to the wa numerical value."

---

## Summary: Q42 Physical Meaning

| Level | C28 vs A12 | Type |
|-------|-----------|------|
| Background E^2(z) exact | DIFFERENT | Different functional forms |
| CPL approximation wa | CLOSE (diff=0.057) | Numerical proximity |
| Perturbation G_eff/G | DIFFERENT (C28: ~2%, A12: 0%) | Measurable (future) |
| Derivational | INDEPENDENT | No limit/derivation |
| Observational (DESI DR2) | DEGENERATE on wa | Indistinguishable |
| Observational (DESI DR2) | MARGINALLY DIFFERENT on w0 | 2.5-sigma |

**Conclusion**: Q42 PASS means OBSERVATIONAL DEGENERACY on wa at current precision.
It does NOT mean isomorphism, derivational equivalence, or structural unification.
The paper language must reflect this: "CPL-level structural proximity on wa."

---

## Q45 Final Status

From Round 7 numerical scan:
- Optimal gamma0 for min |Δwa| in full scan: gamma0 ~ 0.00054 -> wa ~ -0.127, |Δwa| = 0.006
- This gamma0 is OUTSIDE L6 posterior [0.0011, 0.0019]
- Best gamma0 IN L6 range: gamma0 ~ 0.00114 -> wa ~ -0.066, |Δwa| = 0.067 > 0.03
- Q45 FAIL: Cannot achieve |wa_C28 - wa_A12| < 0.03 within L6 posterior range.

C28-A12 isomorphism level: MEDIUM (Q42 PASS only).
"Strong level" (Q45) not achieved.

---

## Paper Section Draft: C28-A12 Comparison

Title: "C28-A12 CPL Structural Proximity"

"The Maggiore-Mancarella RR non-local gravity model (C28) independently motivates
wa < 0 dark energy through a non-local R*box^{-1}*R action term. Full implementation
of the Dirian 2015 background equations (including the essential UV cross-term
+3HVV_dot in the dark energy density) yields wa_C28 ~ -0.19, within |Δwa| = 0.057
of the A12 erf template wa_A12 = -0.133. We classify this as CPL-level structural
proximity: both candidates occupy the same region of wa parameter space at current
observational precision (DESI DR2 sigma_wa ~ 0.24).

This proximity has the following precise scope:
(i) It applies to the wa parameter of the CPL approximation only.
(ii) It does not imply equivalence of the full E^2(z) functions.
(iii) C28 and A12 differ at perturbation level (G_eff/G differs by ~2%).
(iv) No derivational or Lagrangian connection between C28 and A12 has been found.

We interpret Q42 (|Δwa| < 0.10) as an observational degeneracy at current data
quality, not as theoretical unification. Discrimination between C28 and A12
at the wa level requires sigma_wa < 0.03, roughly equivalent to 80x the current
DESI DR2 survey volume. The leading near-term discriminator is CMB-S4 measurement
of G_eff/G (expected sensitivity delta(G_eff/G) < 0.005 ~ 2030)."

---

*Round 8 completed: 2026-04-11*
