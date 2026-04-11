# refs/l14_classb_verdict.md -- L14: Class B 8-Team Integrated Verdict

> Date: 2026-04-11
> Source: l14_classb_extended.md + simulations/l14/b4_feedback.py results
> Task: 8-team integrated judgment on B1~B20. Is B1 still the best?

---

## Question: Is B1 still the best SQMH equation for DESI?

**Answer: Yes, B1 remains the best tested equation. No currently computed B-class
equation outperforms it. However, B9 and B15 are untested equations that
could surpass B1 if numerically verified -- this is a genuine open question.**

---

## 8-Team Votes

### Team 1 (Kinetic Theory / Boltzmann): B1 for now, B9 next

B9 (Gamma_0*H) is physically well-motivated by Boltzmann kinetics:
the collision rate between the quantum vacuum and spacetime should depend on
expansion speed. The equilibrium density n_eq ~ H/(sigma*rho_m + 3H) decreases
faster at high z than B1's n_eq ~ 1/(sigma*rho_m + 3H). This gives a more
negative wa. Recommend: B9 numerical computation first.

Judgment: B1 holds; B9 is the next candidate.

### Team 2 (Fluid Mechanics / Continuity): B1 for now

Among tested equations (B1 and B4), B1 wins (chi2=11.75 vs B4=12.38).
B10 (stimulated emission) has stability problems. B11 (Michaelis-Menten) is
interesting but the extra parameter rho_ref introduces AIC/BIC penalty.
For zero-parameter alternatives: B15 (entropy-based) has potential but
the wa overshoot risk must be checked numerically.

Judgment: B1 holds; B15 requires testing.

### Team 3 (Thermodynamics / Entropy): B15 deserves priority test

B15 (Gamma_0*(H0/H)^2) has thermodynamic motivation (entropy production rate
proportional to horizon entropy ~ H^{-2}) and zero extra parameters.
Its equilibrium n_eq ~ (H0/H)^2 * [1/(sigma*rho_m + 3H)] drops steeply at high z.
This is the strongest wa signal among the zero-parameter B-class alternatives.

Risk: wa may be too large (|wa| >> 0.83). If that is the case, B15 could still
be valid as an upper bound. The parameter space is:
- If |wa_B15| ~ 0.8-1.5: DESI-consistent (chi2 improvement likely)
- If |wa_B15| >> 2: needs parameter rescaling (not B15 as written)

Judgment: B15 should be computed next (zero extra params, strong signal).

### Team 4 (Modified Gravity / Scalar-Tensor): B12 generalizes B9

B12 (Gamma_0*(H/H0)^alpha) is a one-parameter family containing both B1 (alpha=0)
and B9 (alpha=1). Scanning alpha over [0, 2] would give the full picture of
Hubble-modulated creation. For alpha~0.5-1: wa more negative than B1.
B20 (gamma modification to Hubble coefficient) is essentially B12 reparametrized.

Judgment: B12 is the most systematic exploration. B1 holds pending B12 scan.

### Team 5 (Field Theory / Lagrangian): B16 structurally richest, lowest priority

B16 (scalar-field coupling) is the most theoretically grounded but requires
joint phi+n ODE solution. Given SQMH already has issues with scalar field coupling
(L2 results: universal coupling violates Cassini), B16 needs sector-selective coupling.
Under these constraints, B16 reduces to something similar to B12 at the background level.

Judgment: B16 is low priority. Defer to Phase 6+.

### Team 6 (Non-equilibrium / Causal): B14 and B17 are irrelevant

B14 (delayed annihilation): correction is O(H*tau) << 1 for causal tau. NEGLIGIBLE.
B17 (non-local memory): for tau_mem << H0^{-1}: IDENTICAL to B1.
Both reduce to B1 in the physically relevant parameter range.
B13 (coupled matter system): matter continuity violation is tightly constrained by
CMB sound horizon. RISKY without full Boltzmann analysis.

Judgment: B14, B17 are dead. B13 needs CMB analysis first.

### Team 7 (Extended Thermodynamics): B19 threshold model is speculative

B19 (threshold creation) has a sharp feature at rho_m = rho_ref that may cause
problems in chi2 fitting (the derivative is discontinuous). The smooth approximation
is essentially B11. B11 (Michaelis-Menten) is better behaved.

Judgment: B19 not recommended. B11 with rho_ref as free parameter is better.

### Team 8 (All-teams review / CLAUDE.md compliance): B1 remains best TESTED

Numerical computation (b4_feedback.py) confirmed:
- B4 is WORSE than B1: chi2=12.38 vs chi2=11.75 (Dchi2=+0.627)
- B4 wa=-0.004 vs DESI target -0.83 (B4 nearly kills wa)
- B1 wa=-0.107 vs DESI target -0.83 (B1 poor on wa, but better than B4)
- B18 (temperature-coupled) gives wa > 0 -- structurally fails.
- B9/B15 untested but promising by qualitative analysis.

Neither B1 nor any tested alternative reaches DESI wa=-0.83.
The gap between SQMH best (wa~-0.1) and DESI (wa~-0.83) is ~0.7 in wa.
This is a significant tension that no B-class equation has yet closed.

Judgment: B1 holds as best tested. The gap is real and unresolved.

---

## Integrated Verdict

### Is B1 still the best?

**YES -- among numerically tested equations:**
- B1 chi2=11.75 (Dchi2=-1.45 vs LCDM)
- B4 chi2=12.38 (Dchi2=-0.82 vs LCDM): WORSE than B1
- LCDM chi2=13.20 (baseline)

**YES -- but the gap to DESI is still 0.7 in wa:**
- B1 wa=-0.107
- DESI target wa=-0.83
- No B-class equation has wa=-0.83 (confirmed by computation or exclusion)

**UNCERTAIN -- for untested equations:**
- B9 (Gamma_0*H): qualitatively promising, zero extra params, wa direction correct
- B15 (Gamma_0*(H0/H)^2): zero extra params, strong wa signal, risk of overshoot
- B11 (Michaelis-Menten): 1 extra param, tunable wa

### Priority for next numerical work

1. B9: compute chi2 and wa (zero extra params, high DESI potential)
2. B15: compute chi2 and wa (zero extra params, very strong wa signal)
3. B11: scan rho_ref (1 extra param, tunable)

### What would it take for a B-class equation to beat B1 on DESI?

A B-class equation must achieve ALL of:
1. chi2 < 11.75 (better than B1 on 7-bin DESI)
2. wa more negative than -0.107 (in direction of DESI -0.83)
3. No extra parameters (or Bayes-justified if extra params)
4. SQMH physical consistency (xi_q > 0, w > -1)

B9 and B15 are the only zero-parameter candidates with the right wa direction.

---

## Honest Assessment of SQMH Class B Equations

1. **The premise gives Class A (no creation) -- observationally dead.**
2. **Class B requires adding Gamma_0 (beyond premise) -- necessary for viability.**
3. **B1 is the simplest Class B equation -- currently best by chi2.**
4. **B4 (feedback) is WORSE: feedback kills wa by over-tracking equilibrium.**
5. **B9 and B15 are promising but uncomputed.**
6. **None of B1-B20 has been shown to reach DESI wa=-0.83.**
7. **The wa gap (0.7 units) between SQMH and DESI is the central unresolved problem.**

The question "is B1 still the best?" has a conditional answer:
- Among tested equations: YES.
- Among all 20 proposed equations: POSSIBLY NOT (B9, B15 untested).
- In terms of fitting DESI wa=-0.83: NO B-class equation currently achieves this.

---

## CLAUDE.md Compliance Checklist

- [x] DESI DR2 values used: w0=-0.757, wa=-0.83 (DESI+Planck+DES-all)
- [x] sigma = 4*pi*G*t_P (SI) in simulation code
- [x] E^2 = Omega_r*(1+z)^4 + omega_m + omega_de (no double-counting)
- [x] ODE: odeint used (no ad hoc perturbative approximation)
- [x] No unicode in print() statements
- [x] numpy 2.x: np.trapezoid used
- [x] B4 result honest: WORSE than B1, not whitewashed
- [x] B18 explicitly noted as failing (wrong wa sign)
- [x] chi2 comparison includes both delta_chi2 vs LCDM and B4 vs B1

---

*L14 Class B Verdict: 2026-04-11*
*Computation: simulations/l14/b4_feedback.py*
*Result: B1 best tested; B9 and B15 are next priority; wa gap unresolved.*
