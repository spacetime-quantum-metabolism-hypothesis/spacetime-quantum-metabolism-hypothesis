# refs/l9_a12_c28_limit.md -- L9 Round 13: Is A12 the IR Limit of C28?

> Date: 2026-04-11
> Source: L9 Q42 PASS, Round 11 NF-16 resolution, Round 12 mechanism survey.
> Purpose: Mathematically explore whether A12 is a limit of C28 (gamma0->0 or large-m limit).
> Language standard: refs/l7_honest_phenomenology.md.
> Anti-falsification: No limit found => state clearly.
> 8-person parallel team.

---

## Context

From L9 Rounds 1-11:
- Q42 PASS: |wa_C28 - wa_A12| = 0.043 (shooting) to 0.057 (Dirian literature)
- C28-A12 isomorphism depth: MEDIUM (CPL-level proximity only, Round 8)
- Both theories are INDEPENDENT (no derivational relationship established)
- A12 uses erf functional form; C28 uses non-local UV auxiliary field dynamics

Question for Round 13:
"Is A12 the gamma0->0 limit of C28? Or the large-m limit?
Mathematically, does ANY limit of C28 reduce to A12's specific erf form?"

---

## 8-Person Parallel Analysis

### [1/8] gamma0 -> 0 Limit of C28

**Setting**: C28 Friedmann equation:
  E2 = Omega_m*(1+z)^3 + Omega_r*(1+z)^4 + (gamma0/4)*(2U - V1^2 + 3*V*V1)

**As gamma0 -> 0**:
  The non-local contribution vanishes: (gamma0/4)*nonlocal_term -> 0.
  E2 -> Omega_m*(1+z)^3 + Omega_r*(1+z)^4.
  This is matter + radiation ONLY -- NOT LCDM (no Lambda), NOT A12.

**U, V ODE in gamma0->0 limit**:
  The U, V equations are driven by R (Ricci scalar), which itself depends on E2.
  In the limit gamma0->0, E2 = E2_matter, and R = -6*H^2*(xi+2).
  U, V grow as particular solutions in the matter era.
  But their BACK-REACTION on E2 is proportional to gamma0, which vanishes.
  So the dark energy contribution itself vanishes.

**Conclusion**: gamma0 -> 0 gives DARK ENERGY ABSENT. This is the opposite of A12.
  A12 has dark energy with w0 ~ -0.886, wa ~ -0.133.
  The gamma0->0 limit of C28 does NOT reduce to A12.
  It reduces to a matter+radiation universe with no dark energy.

---

### [2/8] Large-m Limit (gamma0 -> infinity)

**Setting**: m^2/H0^2 = gamma0 (large).

**As gamma0 -> infinity**:
  The non-local term (gamma0/4)*nonlocal dominates in E2.
  E2 ~ (gamma0/4)*nonlocal_term >> Omega_m*(1+z)^3.
  The expansion history is dominated by the non-local sector.

**Behavior**: From the ODE in the large-gamma0 limit:
  The xi = d(lnH)/dN feedback becomes self-referential and unstable.
  Physically: large m means the non-local field oscillates rapidly.
  In the limit m >> H, the Box^{-1} operator integrates out the fast modes.
  The result is NOT A12 -- it gives strong oscillations in E2(z).

**From numerical scan** (Round 7, rr_gamma_scan_v2_results.json):
  At gamma0 = 0.005: wa ~ +0.06 (positive, wrong sign)
  At gamma0 = 0.01: wa ~ +0.09 (positive)
  At large gamma0, wa > 0.

**Conclusion**: Large-m (gamma0->infinity) limit gives wa > 0. WRONG direction.
  A12 has wa < 0. The large-m limit is NOT A12.

---

### [3/8] Self-Consistent Limit: gamma0 = gamma0_Dirian (E2=1.0)

**From Round 11**: gamma0_Dirian = 0.000624 gives E2_today = 1.0 exactly.
  wa_C28 = -0.1757 at this value.

**Question**: Is there a limit where C28 exactly gives wa = -0.133?

**From gamma scan** (rr_gamma_scan_v2_results.json):
  At gamma0 = 0.00054: wa = -0.127, |Dwa| = 0.006. Very close to A12.
  At gamma0 = 0.00030: wa = -0.148, |Dwa| = 0.015.
  At gamma0 = 0.00042: wa = -0.139, |Dwa| = 0.006.
  At gamma0 = 0.00060: wa = -0.114, |Dwa| = 0.019.

**Linear interpolation**: wa = -0.133 at gamma0 ~ 0.000480 (between 0.00042 and 0.00054).
  But at gamma0=0.00048: E2_today ~ 0.90 (unnormalized scan, not E2=1.0).
  With shooting normalization: need separate calculation.

**Physical interpretation**: wa ~ -0.133 is achievable in C28 for some specific gamma0.
  But this is parameter tuning, not a limit in a mathematical sense.
  The function wa(gamma0) is smooth and passes through -0.133 at some gamma0*.

**Conclusion**: C28 contains A12's wa value as a parameter point but not as a
  distinguished limit. There is no physical reason to single out gamma0* as special.

---

### [4/8] Large-N Limit of C28 (Far Future)

**Setting**: N = ln(a) -> infinity (far future, de Sitter era).

**In de Sitter limit**:
  xi = d(lnH)/dN -> 0 (H = const for de Sitter).
  U equation: U'' + 3*U' = 6*(2+0) = 12.  Particular: U_p = 4, growing.
  V equation: V'' + 3*V' = U ~ 4.  Particular: V_p = 4/3.
  The non-local term: 2U - V1^2 + 3*V*V1 -> const (de Sitter attractor).
  rho_DE -> const -> w_eff -> -1 (de Sitter).

**This is NOT A12**: A12 approaches de Sitter through CPL with specific wa.
  C28 reaches de Sitter from a different trajectory.

---

### [5/8] Mathematical Structure Comparison

**C28 E2(z)** (exact):
  E2_C28(z) = Omega_m*(1+z)^3 + (gamma0/4)*F_UV(z)
  where F_UV(z) = 2U(z) - V1(z)^2 + 3*V(z)*V1(z) from ODE.

**A12 E2(z)** (exact):
  E2_A12(z) = Omega_m*(1+z)^3 + Omega_DE * CPL(z, w0, wa)
  where CPL(z) = (1+z)^{3(1+w0+wa)} * exp(3*wa*z/(1+z)).

**Are these the same function?**
  C28: F_UV(z) is determined by a system of ODEs (4th-order equivalent).
  A12: CPL(z) is an algebraic function of z.
  They are DIFFERENT mathematical structures.

**Can F_UV(z) be approximated as CPL?**
  Yes: any smooth monotonic function over z in [0, 3] can be approximated by CPL.
  But the CPL fit parameters (w0, wa) are then just fitting parameters, not a limit.
  Q42 PASS (|Dwa|=0.043) is a statement about the QUALITY of the CPL approximation
  to both C28 and A12, not about mathematical equivalence.

**Conclusion**: There is no mathematical limit where C28 reduces to A12.
  They are different functional forms that happen to have similar CPL projections.

---

### [6/8] Perturbation-Level Limit Analysis

**C28 perturbations** (Belgacem 2018, arXiv:1712.07071):
  G_eff/G = 1 + delta_G_C28(k, z) where delta_G_C28 ~ 2% at z=0 (k-independent at large scales).
  This is a GENUINE modification not present in A12 (which has delta_G_A12 = 0 by construction).

**A12 perturbations**: Pure CPL background, no G_eff modification.
  A12 is a phenomenological background template without perturbation modification.

**Question**: Is A12 the "zero perturbation modification" limit of C28?
  In C28, if gamma0 -> 0: delta_G -> 0 (no modification). But this also kills dark energy.
  There is no limit where C28 has dark energy but delta_G = 0.

**Conclusion**: A12 cannot be obtained from C28 by any limit that preserves dark energy.
  The perturbation structures are fundamentally different (delta_G ~ 0 vs 2%).

---

### [7/8] Group-Theoretic / Symmetry Limit

**Does A12 have a symmetry that C28 lacks?**

A12 is a pure CPL parameterization:
  - Background only (no field dynamics)
  - Two free parameters (w0, wa)
  - No perturbation modification
  - No theoretical derivation

C28 has:
  - Non-local scalar sector (two auxiliary fields U, V)
  - One physical parameter (gamma0 = m^2/H0^2)
  - Perturbation modification (delta_G ~ 2%)
  - Theoretical derivation from non-local quantum gravity

**A12 has MORE symmetry** than C28: it is the "no-modification" effective theory.
C28 in the "no-perturbation" limit still modifies the background non-locally.
A12 in the "no-theory" limit is just CPL.

**Conclusion**: A12 is not a symmetry limit of C28. They have different symmetry
  structures. A12 is a phenomenological template; C28 is a dynamical theory.

---

### [8/8] Synthesis: Is A12 = limit of C28?

**Summary of all 7 analyses:**

| Limit | C28 -> ? | Is it A12? |
|-------|---------|-----------|
| gamma0 -> 0 | No dark energy | NO |
| gamma0 -> infinity | wa > 0, oscillations | NO |
| gamma0 = gamma0_Dirian | wa = -0.176 | CLOSE but not exact |
| Far future (de Sitter) | w -> -1 | NO |
| Mathematical function | ODE solution, not CPL | NO |
| Perturbation limit | delta_G -> 0 kills dark energy | NO |
| Symmetry limit | Different symmetry structures | NO |

**Definitive answer**: NO. A12 is NOT the gamma0->0 limit, the large-m limit,
  or any other limit of C28 in a mathematical sense.

**What is their relationship?**
  A12 and C28 are INDEPENDENT theories that happen to have SIMILAR CPL projections
  (wa_C28 ~ -0.176, wa_A12 = -0.133, |Dwa| = 0.043 < 0.10).
  This numerical proximity (Q42 PASS) is a coincidence or a symptom of a deeper
  shared structure (possibly the curvature-sensitive dark energy sector).

**Allowed paper language:**
  "C28 and A12 share CPL-level structural proximity (|Dwa| = 0.043 < 0.10)
   without any derivational relationship. No limit of C28 reduces to A12."

**Forbidden paper language:**
  "A12 is the IR limit of C28" (false)
  "C28 parent theory of A12" (false)
  "A12 derives from C28 via limit X" (not established)

---

## Round 13 Verdict

**Main finding**: A12 is NOT any limit of C28. Mathematical analysis (7 independent
  perspectives) confirms no limit connects them. Their CPL proximity (Q42 PASS)
  reflects a coincidental numerical agreement at the level of 0.043 in wa.

**Alternative interpretation**: Both C28 and A12 may be independently reflecting
  a deeper physical principle -- possibly the Ricci curvature scale (NF-18a from
  Round 12) -- that naturally gives wa ~ -0.13 to -0.18. This would explain why
  multiple independent theories converge on this wa range without being related.

**Paper impact**:
  - Section on C28 should maintain "CPL structural proximity, not derivation"
  - Round 13 finding reinforces Round 8 isomorphism depth: MEDIUM only
  - New addition: "No mathematical limit of C28 reduces to A12"

---

*Round 13 completed: 2026-04-11*
*8-person parallel team: gamma0-limit, large-m, self-consistent, future, math-structure,
 perturbation, symmetry, synthesis*
