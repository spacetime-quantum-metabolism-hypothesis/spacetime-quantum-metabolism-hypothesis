# refs/l8_round3_verdict.md -- L8 Round 3: Symmetry / Group Theory

> Date: 2026-04-11
> Round 3 of 5 additional rounds (Rounds 2-6).
> Method: 8-person parallel team, simultaneous independent attack angles,
>   immediate cross-sharing, deliberation, final consensus.
> Focus: Symmetry/group theory -- what symmetry group does each candidate's
>   ODE have? Is there a symmetry transformation mapping it to SQMH?
> Prior established: Q31/Q32/Q33 FAIL (Rounds 1-2). Scale gap = 61-62 orders.

---

## Attack Angle: Symmetry / Group Theory

Question: Does there exist a Lie symmetry transformation of coordinates
and fields that maps each candidate's governing ODE to the SQMH
continuity equation dn_bar/dt + 3H n_bar = Gamma_0 - sigma*n_bar*rho_m?

---

## 8-Person Parallel Discussion

### [Member 1 -- SQMH symmetry group]

SQMH homogeneous ODE in standard form:
  dn_bar/da = (1/(aH)) [Gamma_0 - sigma*n_bar*rho_m] - 3*n_bar/a

Rewrite as autonomous system with a as independent variable:
  dn_bar/da = F(a, n_bar)  where F = (Gamma_0 - sigma*n_bar*rho_m)/(aH) - 3n_bar/a

This is a LINEAR non-homogeneous ODE in n_bar (treating H(a), rho_m(a) as
given functions of a, NOT as dynamical variables in the symmetry analysis).

Symmetry analysis of: dn_bar/da + [3/a + sigma*rho_m/(aH)] n_bar = Gamma_0/(aH)

Lie symmetry generator: X = xi(a,n) d/da + eta(a,n) d/dn_bar

Determining equations:
  eta_a + (F_a) xi + eta F_n - xi_a F - xi F_a = 0

For linear ODEs dy/dx = A(x)y + B(x), the Lie symmetry group is:
  1. Scaling: (a, n_bar) -> (a, lambda*n_bar)  -- valid iff B=0 (homogeneous)
  2. Translation: n_bar -> n_bar + c*y_particular  -- always valid
  3. Scaling+shift: for B != 0, one-parameter group of translations in n_bar

SQMH ODE symmetry group: {n_bar -> n_bar + c*n_particular(a)}, i.e.,
the affine group in fiber direction. Order-1 Lie group.

### [Member 2 -- A12 symmetry structure]

A12 is NOT defined by a dynamical ODE for n_bar. It is a parametric
ansatz E^2(z) = Om*(1+z)^3 + (1-Om)*F_erf(z).

Symmetry relevant question: Does the Friedmann ODE for A12 background
share a symmetry group with SQMH continuity?

A12 effective Friedmann: 3H^2 = rho_c0 * E^2(z).
This is an algebraic relation, not a differential equation for any field.

Therefore, symmetry group analysis of A12 ODE is trivial: A12 has no
field-level ODE symmetry group to compare with SQMH. A12 is kinematic,
not dynamic.

Conclusion: No symmetry transformation exists because A12 has no
autonomous ODE. The "mapping" question is ill-posed for A12.

### [Member 3 -- CLW symmetry group (C11D)]

CLW autonomous system:
  dx' = -3x + (sqrt(6)/2)*lambda*y^2 + (3/2)*x*[2x^2 + (1-w_m)*(1-x^2-y^2)]
  dy' = -(sqrt(6)/2)*lambda*x*y + (3/2)*y*[2x^2 + (1-w_m)*(1-x^2-y^2)]

where ' = d/d(ln a). This is a 2D NONLINEAR autonomous system.

Lie symmetry of CLW system:
The standard CLW system (with constant lambda) admits:
  - Rescaling symmetry: (a, x, y) -> (c*a, x, y) when lambda=0.
  - Time translation: ln(a) -> ln(a) + c (autonomous ODE always has this).
  - For lambda != 0: no additional continuous Lie symmetry (generic nonlinear system).

SQMH ODE symmetry: linear, 1D, affine group in fiber.
CLW symmetry: nonlinear, 2D, only time-translation (for lambda != 0).

Symmetry group comparison:
- SQMH: {translation in n_bar fiber} (abelian, 1-dim).
- CLW: {translation in ln(a)} (abelian, 1-dim, trivial for autonomous ODE).

These are FORMALLY isomorphic as abstract groups (both = R^1) but with
completely different geometric content (fiber translation vs. base translation).
A symmetry transformation mapping CLW to SQMH would require reducing
the 2D nonlinear system to 1D linear system -- this requires:
  (a) Restricting to a 1D invariant submanifold of CLW phase space.
  (b) Linearizing the dynamics on that submanifold.

Check: Does CLW have a 1D invariant submanifold?
The tracker (x/y = const) and the kinetic-dominated (y=0) lines are
invariant, but x=0, y=x (tracker) are not of SQMH form.

Member 3 finds: No symmetry transformation maps CLW ODE to SQMH ODE.

### [Member 4 -- RR symmetry group (C28)]

C28 RR ODE system:
  U'' + 3H*U' = R = -6(H' + 2H^2)  [U eq]
  V'' + 3H*V' = U                   [V eq]

where ' = d/dt. This is a LINEAR, 2D, second-order system.

Rewrite as 4D first-order: (U, U', V, V') = (U, P_U, V, P_V).

System matrix (in conformal time or ln(a)):
  [dU/dN] = P_U
  [dP_U/dN] = R(N) - 3H*P_U
  [dV/dN] = P_V
  [dP_V/dN] = U - 3H*P_V

This is a LINEAR, non-autonomous, 4D system.

SQMH ODE:
  dn_bar/dN = (Gamma_0 - sigma*n_bar*rho_m)/H - 3*n_bar

This is LINEAR, non-autonomous, 1D system.

Symmetry group of a linear system:
A linear system dy/dx = A(x)*y + b(x) always has the FULL AFFINE GROUP
as its fiber symmetry: y -> y + y_homogeneous for any homogeneous solution.

The 4D RR system symmetry group: GL(4) extended by affine translations.
The 1D SQMH system symmetry group: GL(1) = R* extended by affine translations.

Group theory question: Is there a GL(4) -> GL(1) group homomorphism
that maps RR to SQMH?

Answer: YES, trivially -- project onto any 1D subspace. But the question
is whether there is a PHYSICALLY MEANINGFUL such map that preserves
the SQMH somatic structure sigma*n_bar*rho_m.

The P-variable (V' = P) from Round 1 already exploits this:
dP/dN + (3 + H'/H^2)P = U. This IS isomorphic to SQMH in form.

But the source U is NOT sigma*n_bar*rho_m -- it is a dynamic field
satisfying its own ODE (Box*U = R). In SQMH, the source Gamma_0 is
CONSTANT (not dynamic). This distinction breaks the exact symmetry map.

### [Member 5 -- Symmetry obstruction: source structure]

Key insight (immediately cross-shared):

The fundamental symmetry obstruction for C11D and C28 mapping to SQMH:

SQMH structure: dn_bar/dt + 3H*n_bar = Gamma_0 - sigma*n_bar*rho_m
  - Source: Gamma_0 = CONSTANT.
  - Dissipation: sigma*n_bar*rho_m (multiplicative, linear in n_bar).

CLW structure (C11D): 2D nonlinear in (x,y).
  - No constant source term.
  - Dissipation: nonlinear in x,y.

RR structure (C28): P-eq has U as source.
  - Source U = dynamic field (NOT constant).
  - Dissipation: 3H*P (linear, same as SQMH).

The SYMMETRY OBSTRUCTION is the constant source Gamma_0.

Any symmetry transformation mapping C11D or C28 to SQMH must:
  - Map the variable source in those models to a CONSTANT.
  - Require: d(source)/dt = 0 on the symmetry orbit.

For C28: d(U)/dt != 0 (U evolves via Box*U = R). The symmetry map
requires the RR "source freezing condition" dU/dt = 0, which is
ONLY satisfied if R = 0 (i.e., Minkowski spacetime). Not cosmological.

For C11D: The nonlinear CLW source (drift term ~lambda*y^2) is time-dependent
via the orbit. Source freezing requires phi = const (frozen field), i.e.,
lambda -> 0 limit. But lambda=0 gives LCDM, not SQMH.

Conclusion: The constant-Gamma_0 structure of SQMH is a symmetry invariant
that is NOT shared by either C11D (dynamic nonlinear source) or C28
(dynamic auxiliary field source). No symmetry map exists.

### [Member 6 -- Noether symmetry approach]

Noether symmetry method: Look for symmetry vector X = xi(t)*d/dt + eta(n)*d/dn
such that Noether's first integral I = eta - xi*dn/dt is conserved.

For SQMH: L = (1/2)*(dn/dt)^2 (formally -- SQMH is a first-order dissipative
system, not Lagrangian). The Noether approach requires Lagrangian structure.

Issue: SQMH continuity equation is DISSIPATIVE (sigma*n*rho_m dissipates n).
Dissipative systems in general do NOT have Noether symmetries from a
standard Lagrangian. They can have integrating factors.

Integrating factor for SQMH:
mu(a) * [dn/da + A(a)*n] = mu(a)*B(a)
where mu(a) = exp(integral A da).

Integrating factor symmetry: SQMH, CLW, and RR all possess integrating
factors (being linear or integrable). But integrating factors are NOT
symmetry transformations -- they are solution techniques.

Noether symmetry verdict: SQMH is not Lagrangian -> Noether analysis
does not directly apply. No new symmetry found via this route.

### [Member 7 -- Darboux / Prelle-Singer symmetry]

Prelle-Singer method for first integrals of ODEs:
For dn/dt = F(t,n), seek rational integrating factor R(t,n) such that
d/dt[R*(n-n_particular)] = 0.

For SQMH: dn_bar/dt + (3H + sigma*rho_m)*n_bar = Gamma_0.
This is LINEAR in n_bar. The general solution:

n_bar(a) = exp(-integral A da) [integral B*exp(integral A da) da + C]

where A = 3/a + sigma*rho_m/(aH), B = Gamma_0/(aH).

Since sigma*rho_m/(3H) ~ 10^-62, A ~ 3/a and:
n_bar(a) ~ a^-3 * [integral Gamma_0/(aH) * a^3 da + C]

For C11D (CLW): x-equation is nonlinear. No rational integrating factor
exists in general (Prelle-Singer theorem: nonlinear systems with
transcendental terms generically have no rational first integrals).

For C28 (RR): P-equation is linear. Prelle-Singer gives integrating factor.
But the P-equation source U(a) is NOT Gamma_0 = const.

Prelle-Singer verdict: The symmetry group structure (linear vs nonlinear,
constant vs dynamic source) is NOT compatible between SQMH and candidates.

### [Member 8 -- NEW FINDING: Scale-free limit and conformal symmetry]

NEW FINDING CANDIDATE (flagged for team review):

Consider the SQMH ODE in the sigma -> 0 limit:
  dn_bar/da + 3n_bar/a = Gamma_0/(aH)

This is a SCALE-FREE ODE if H ~ a^-n (power law). In matter era H ~ a^-3/2:
  dn_bar/da + 3n_bar/a = Gamma_0/(a * H_0 * a^(-3/2)) = (Gamma_0/H_0) * a^(1/2)

Solution: n_bar ~ a^-3 + (2*Gamma_0)/(7*H_0) * a^(1/2).

The ODE dn/da + 3n/a = f(a) has the dilation symmetry:
  (a, n) -> (lambda*a, lambda^-3 * n)  [provided f(a) transforms as f -> lambda^(-3-alpha) f]

For f ~ a^(1/2): scaling dimension alpha = -1/2. The dilation maps:
  a -> lambda*a, n -> lambda^-3 * n, f -> lambda^(-7/2) * f.

This is a BROKEN SCALE symmetry (not exact) -- only holds in matter era.

Now: Does CLW (C11D) or RR (C28) possess this SAME broken dilation symmetry
in the matter era?

CLW in matter era (Omega_m ~ 1, x ~ 0, y ~ 0 for thawing):
  dx'/dn ~ -3x + ...: decays. The dilation (a -> lambda*a, x -> lambda^0*x)
  is NOT the same as SQMH dilation (a -> lambda*a, n -> lambda^-3*n).

RR in matter era (U ~ 0, V ~ 0 for small gamma_0):
  P' + 3P ~ U: dilation (a -> lambda*a, P -> lambda^-3*P, U -> lambda^-3*U).
  This IS the SAME dilation as SQMH (with P <-> n_bar, U <-> source).

  Team deliberation: In matter era, the RR P-equation and SQMH both exhibit
  the SAME scale-free dilation symmetry (a,P) -> (lambda*a, lambda^-3*P).
  The difference appears only in the source: U(a) [dynamic] vs Gamma_0 [constant].

  In the matter era, U(a) ~ 0 (C28 field equations in deep matter era give U->0).
  In matter era: P' + 3P ~ 0 and dn/da + 3n ~ 0 BOTH reduce to n ~ a^-3.

  The matter-era attractor of BOTH C28 and SQMH is n_bar ~ a^-3.
  They share the same Lie symmetry in the matter-era limit.

ASSESSMENT: This is a structural observation -- in matter era, C28 and SQMH
share the same dilation symmetry and the same attractor behavior.
The difference (U != Gamma_0) only manifests in DE era. This is NOT a
new isomorphism claim -- it is consistent with both being well-behaved
at matter era and diverging in DE era.

Team verdict: "C28 and SQMH contain a matter-era sector isomorphic to
n ~ a^-3 dilation scaling." This is at the level of a structural footnote,
not a derivation link.

---

## Round 3 Team Consensus

**Symmetry / Group Theory Results:**

| Candidate | ODE Type | Symmetry Group | Maps to SQMH? |
|-----------|----------|----------------|---------------|
| A12       | Algebraic (no ODE) | Trivial | ILL-POSED |
| C11D      | 2D nonlinear (CLW) | Time-translation only | NO |
| C28       | 4D linear (U,V system) | Affine GL(4) | PARTIAL (P-eq structure only) |

**Fundamental Symmetry Obstruction:**
- SQMH has a CONSTANT source Gamma_0. Candidates have dynamic sources.
- No symmetry transformation maps a dynamic source to a constant while
  preserving the ODE structure.
- The only exception: matter-era limit where sources vanish (U->0, Gamma_0 neglected).

**NEW FINDING (Structure, not derivation claim):**
- In the matter-dominated era (a << a_eq), C28 P-equation and SQMH
  continuity equation share the SAME dilation symmetry group:
  (a, field) -> (lambda*a, lambda^-3*field).
- Both systems have attractor n ~ a^-3 in matter era.
- Divergence in DE era: U != constant.
- Language: "C28 and SQMH contain a matter-era sector isomorphic to
  the a^-3 dilation group. The shared symmetry breaks at DE domination."

**Round 3 Verdict:**
- Q31/Q32/Q33: REMAIN FAIL. No symmetry map sufficient for isomorphism claim.
- New structural footnote: C28 matter-era dilation symmetry matches SQMH.
- Flagged as: "C28_matter_era_symmetry" -- footnote level, not a new claim.

---

*Round 3 complete: 2026-04-11*
