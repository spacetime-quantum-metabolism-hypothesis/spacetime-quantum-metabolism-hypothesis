# refs/l8_round9_verdict.md -- L8 Round 9: Action Principle Reconstruction

> Date: 2026-04-11
> Round 9 of second batch (Rounds 7-11).
> Method: 8-person parallel team, all 3 candidates + SQMH simultaneously.
> Focus: What Lagrangian gives the SQMH ODE as its Euler-Lagrange equation?
>   Compare to A12/C11D/C28 Lagrangians. Is there a unifying action?
> Prior established: Q31/Q32/Q33 FAIL (Rounds 1-8). NF-1 through NF-8 registered.

---

## Framework Overview

The SQMH equation is:
  dn_bar/dt + 3H*n_bar = Gamma_0 - sigma*n_bar*rho_m     [SQMH ODE]

This is a FIRST-ORDER ODE in n_bar. First-order ODEs can be derived from
action principles but require specific constructions (dissipative systems,
Rayleigh function, Caldirola-Kanai type, or doubled-variable Schwinger-Keldysh).

The challenge: SQMH is DISSIPATIVE (has damping 3H*n_bar and dissipation
sigma*n_bar*rho_m). Standard Lagrangian mechanics generates CONSERVATIVE
equations. Dissipation requires extensions.

---

## 8-Person Parallel Discussion

### [Member 1 -- Naive Euler-Lagrange attempt for SQMH]

For a scalar field n(x, t) in FRW spacetime, the Euler-Lagrange equation is:
  d/dt (dL/d(n_dot)) - dL/dn + (1/a^3) * d(a^3 * dL/d(n)) / dx = 0

For a homogeneous field n(t) (no spatial gradient):
  d/dt (dL/d(n_dot)) - dL/dn = 0

Standard kinetic term: L = (1/2)*n_dot^2 + V(n)
  EL: n_ddot - dV/dn = 0  [conservative, no damping].

To get the SQMH first-order equation, one approach: use L = n_dot * F(n) - V(n)
  This gives first-order EL: dF/dn * n_dot - F'(n)*n_dot - dV/dn = ?

Actually, for L = n_dot * F(n):
  dL/d(n_dot) = F(n)
  dL/dn = n_dot * F'(n)
  EL: d/dt [F(n)] - n_dot * F'(n) = 0
    F'(n) * n_dot - n_dot * F'(n) = 0
    0 = 0   (trivially satisfied, no dynamics!)

This is the DEGENERATE case. L linear in n_dot gives a CONSTRAINT, not an EL equation.

To get SQMH from EL, we need a DISSIPATIVE Lagrangian. Options:
  (a) Caldirola-Kanai (1941): L_CK = e^(gamma*t) * [(1/2)*n_dot^2 - V(n)]
  (b) Bateman doubled system: L_B = n_dot*psi_dot + ... (mirror system)
  (c) Schwinger-Keldysh (in-in formalism): L_SK for open quantum systems

### [Member 2 -- Caldirola-Kanai Lagrangian for SQMH]

Caldirola-Kanai Lagrangian for a damped oscillator:
  L_CK = e^(gamma*t) * [(1/2)*n_dot^2 - V(n)]

EL equation: e^(gamma*t) * [n_ddot + gamma*n_dot + dV/dn] = 0
  => n_ddot + gamma*n_dot + dV/dn = 0

This is second-order. SQMH is first-order. We need to take the overdamped limit.

Overdamped limit (remove n_ddot term):
  gamma*n_dot + dV/dn = 0
  n_dot = -(1/gamma) * dV/dn   [gradient flow]

Matching to SQMH:
  n_dot = -(3H + sigma*rho_m)*n + Gamma_0
  
For gradient flow: -(1/gamma)*dV/dn = -(3H + sigma*rho_m)*n + Gamma_0
  dV/dn = gamma * [(3H + sigma*rho_m)*n - Gamma_0]
  V(n) = gamma * [(3H + sigma*rho_m)*n^2/2 - Gamma_0*n]

This requires gamma to absorb the damping:
  For constant gamma: gamma = 3H + sigma*rho_m = kappa(t).

But kappa is TIME-DEPENDENT (H changes). The Caldirola-Kanai approach
with constant gamma does not directly apply.

For time-dependent damping gamma(t) = kappa(t):
  The Caldirola-Kanai Lagrangian becomes:
  L_CK = e^(int_0^t kappa(t') dt') * [(1/2)*n_dot^2 - V(n)]
  = a(t)^3 * exp(sigma * int_0^t rho_m dt') * [(1/2)*n_dot^2 - V(n)]

This is because int_0^t 3H dt' = ln(a^3) and int_0^t sigma*rho_m dt' separates.

STRUCTURAL FINDING: The Caldirola-Kanai Lagrangian for SQMH (in the overdamped
limit) is:
  L_CK_SQMH = a^3 * M(t) * [(1/2)*n_dot^2 - Gamma_0*n]

where M(t) = exp(sigma * int_0^t rho_m(t') dt') is a "matter interaction" factor.

In the sigma -> 0 limit: M -> 1, and L_CK_SQMH reduces to the standard
scalar field Lagrangian for a tachyon/quintom with potential Gamma_0*n.

The sigma coupling introduces the MATTER INTERACTION FACTOR M(t) which
is NOT present in any standard dark energy Lagrangian.

M(t) is approximately 1 + sigma * int_0^t rho_m dt' + ...
  ~ 1 + sigma * rho_m0 / H_0 * [some integral over a(t)]
  ~ 1 + Pi_SQMH * [O(1) factor]
  ~ 1 + 10^-62

The sigma correction to the Lagrangian is 10^-62 -- unobservably small.

### [Member 3 -- Scalar field action for SQMH in curved spacetime]

Attempt to embed SQMH in a covariant scalar field action:
  S = int d^4x sqrt(-g) * [R/(16*pi*G) + L_n]

where L_n is the Lagrangian density for n_bar.

From Member 2: the overdamped Lagrangian in the sigma->0 limit is:
  L_n ~ -V(n) = -Gamma_0 * n  [potential only, no kinetic term in overdamped limit]

But a covariant scalar field action requires kinetic term:
  L_n = -(1/2)*g^{mu nu}*partial_mu n * partial_nu n - V(n)
  = (1/2)*n_dot^2 - V(n)  [in FRW homogeneous case]

This gives second-order EL: n_ddot + 3H*n_dot + V'(n) = 0.

To get the SQMH FIRST-ORDER ODE, we need V'(n) >> n_ddot, n_dot*3H.
This is the SLOW-ROLL approximation!

SQMH corresponds to a scalar field n in the SLOW-ROLL (overdamped) limit:
  3H*n_dot = -V'(n) + Source
  where Source includes the matter coupling sigma*n*rho_m.

The effective scalar field Lagrangian that gives SQMH in slow-roll:
  L_n = (1/2)*n_dot^2 - V(n) - (sigma/2)*n^2*rho_m  [interaction term]

Wait -- the interaction term sigma*n*rho_m in SQMH is a LINEAR dissipation.
In Lagrangian terms, this would come from a COUPLING:
  L_int = -sigma * n * rho_m  [not a potential term, since rho_m is external]

This is a SPURION coupling (rho_m as external field). In the full theory,
rho_m would be dynamical and L_int would couple n to matter fields.

SQMH action (heuristic):
  S_SQMH = int d^4x sqrt(-g) * [R/(16*pi*G) + (1/2)*(partial n)^2
           - Gamma_0*n + sigma*n*rho_m(x)]

where the last term is the spurion matter coupling. In slow-roll:
  3H*n_dot = Gamma_0 - sigma*n*rho_m - 0   [V'(n) = Gamma_0 for V = Gamma_0*n]

Wait: if V = Gamma_0*n, then V'(n) = Gamma_0 (constant).
Slow-roll: 3H*n_dot + V'(n) - (sigma*rho_m)*n = 0 is missing the sign.

Let me redo. SQMH ODE: n_dot + 3H*n = Gamma_0 - sigma*n*rho_m
  n_dot + (3H + sigma*rho_m)*n = Gamma_0

For a scalar field in slow-roll: 3H*phi_dot = -V'(phi).
If phi = n and V(n) = [(3H_0 + sigma*rho_m0)/2]*n^2 - Gamma_0*n:
  V'(n) = (3H_0 + sigma*rho_m0)*n - Gamma_0
  Slow-roll: 3H*n_dot = -V'(n) = -(3H_0 + sigma*rho_m0)*n + Gamma_0

For H ~ H_0 (matter era to present): this gives EXACTLY the SQMH ODE.
But this requires H*n_dot ~ H_0*n_dot (valid when H ~ H_0, i.e., z ~ 0).

STRUCTURAL FINDING: SQMH is the slow-roll limit of a scalar field n with
potential V(n) = kappa*n^2/2 - Gamma_0*n (harmonic potential centered at n*).

This is a PARABOLIC potential, not an exponential or power-law.
The standard quintessence potentials for C11D (exponential) and A12 (no V) are
DIFFERENT in character from this parabolic V.

### [Member 4 -- A12 action vs SQMH action]

A12 is a CPL parameterization with w0=-0.886, wa=-0.133.

CPL does not correspond to a specific fundamental Lagrangian -- it is
phenomenological. However, any w(a) can be mapped to a quintessence V(phi):
  From w = (phi_dot^2/2 - V) / (phi_dot^2/2 + V):
  V(phi) = (1-w)/(1+w) * phi_dot^2/2  [relates V and phi_dot]

For CPL: one can numerically reconstruct V(phi). The result for w0=-0.886,
wa=-0.133 is approximately a THAWING quintessence with V ~ exp(-lambda*phi)
or V ~ phi^n.

The A12 Lagrangian:
  S_A12 = int d^4x sqrt(-g) * [R/(16*pi*G) + (1/2)*(partial phi)^2 - V_A12(phi)]

The SQMH action (from Member 3):
  S_SQMH ~ int d^4x sqrt(-g) * [R/(16*pi*G) + (1/2)*(partial n)^2
           - kappa*n^2/2 + Gamma_0*n + sigma*n*rho_m(x)]

Comparison:
  A12: L = (1/2)*(partial phi)^2 - V_A12(phi)  [free quintessence]
  SQMH: L = (1/2)*(partial n)^2 - kappa*n^2/2 + Gamma_0*n + sigma*n*rho_m

Key differences:
  1. SQMH has a MATTER COUPLING sigma*n*rho_m; A12 does not.
  2. SQMH has a CONSTANT PRODUCTION Gamma_0*n (linear in n); A12's potential
     is nonlinear (exponential or power-law in phi).
  3. SQMH potential is QUADRATIC (parabola); A12's is NOT quadratic.

The only overlap is the kinetic term (1/2)*(partial field)^2, which is
universal for all scalar fields. There is NO overlap in the potential sectors.

A12's Lagrangian sector is DISJOINT from SQMH's.
No unifying action contains both A12 and SQMH as limits.

### [Member 5 -- C11D action vs SQMH action]

C11D: CLW potential V = V0 * exp(-lambda*phi) with disformal coupling.

Pure quintessence sector (ignoring disformal for Lagrangian comparison):
  S_C11D = int d^4x sqrt(-g) * [R/(16*pi*G) + (1/2)*(partial phi)^2 - V0*exp(-lambda*phi)]

The C11D potential V_C11D(phi) = V0*exp(-lambda*phi) is EXPONENTIAL.
The SQMH potential V_SQMH(n) = kappa*n^2/2 - Gamma_0*n is QUADRATIC.

Comparison:
  C11D: V = V0 * exp(-lambda*phi)  [exponential -- typical runaway quintessence]
  SQMH: V = kappa*n^2/2 - Gamma_0*n  [quadratic -- harmonic-like]

An exponential and a quadratic are DIFFERENT analytic structures:
  - Exponential has no stationary point for lambda != 0 (runaway potential).
  - Quadratic has a minimum at n* = Gamma_0/kappa (natural equilibrium).

This difference reflects the PHYSICAL CHARACTER:
  - C11D is a RUNAWAY scalar field (tracks matter or dominates at late time).
  - SQMH is a BIRTH-DEATH process with natural equilibrium n* (recall NF-3).

For C11D to reduce to SQMH, we would need exp(-lambda*phi) ~ phi^2
over the relevant field range. This requires:
  - lambda*phi ~ -2*ln(phi) + const.
  - lambda ~ -2/phi * d(ln phi)/d(phi) = -2/phi^2, valid only locally.
  - Global approximation fails; the analogy breaks down for any finite lambda.

CONCLUSION: C11D Lagrangian is NOT isomorphic to SQMH Lagrangian.
The exponential vs quadratic potential difference represents a fundamental
structural incompatibility. No unifying action contains both as limits.

### [Member 6 -- C28 action vs SQMH action]

C28: Non-local Maggiore-Mancarella action:
  S_C28 = M_P^2/2 * int d^4x sqrt(-g) * [R - (m^2/6)*R*(box^-1*R)]

This is a TENSOR (non-local gravitational) action, not a scalar field action.
The localized form introduces auxiliary scalar fields U = -box^-1*R and V = -box^-1*U:
  S_C28_local = int d^4x sqrt(-g) * [M_P^2/2*R*(1 + m^2*V/6) + sigma_U*(U + box^-1*R) + ...]

The C28 Lagrangian operates in the GRAVITY SECTOR (modifying the Einstein-Hilbert action).
The SQMH Lagrangian (from Member 3) operates in the MATTER SECTOR (coupling n to rho_m).

This is a fundamental difference in which sector of the action they modify:
  C28: gravity sector (R, box^-1*R).
  SQMH: matter sector (n, coupling to rho_m via sigma).

For a unifying action containing both:
  S_unify = int d^4x sqrt(-g) * [M_P^2/2*R*(1 + m^2*V/6) + (1/2)*(partial n)^2
            - kappa*n^2/2 + Gamma_0*n + sigma*n*rho_m]

This action would contain both C28 (gravity sector) and SQMH (matter sector) as
INDEPENDENT SECTORS (not as limits of each other). The two sectors decouple unless
there is a MIXED COUPLING between V (the non-local auxiliary) and n (the SQMH field).

For a mixed coupling: L_mix = xi * V * n (some cross term).
There is NO physical motivation for this cross term in either C28 or SQMH.

CONCLUSION: C28 and SQMH are in DIFFERENT sectors (gravity vs matter).
A formal unifying action exists but requires an UNMOTIVATED cross coupling.
Without cross coupling, C28 and SQMH are DECOUPLED sectors in the full action.

The C28 system is NOT a limit of the SQMH scalar field action and vice versa.

### [Member 7 -- Is there ANY unifying action for all three candidates + SQMH?]

Testing a hypothetical unifying action:
  S_unify = int d^4x sqrt(-g) * [M_P^2/2*R*(1 + m^2*V/6)   [C28 sector]
            + (1/2)*(partial phi)^2 - V(phi)                [A12/C11D sector]
            + (1/2)*(partial n)^2 - kappa*n^2/2 + Gamma_0*n + sigma*n*T [SQMH sector]
            + L_matter]

Here T = rho_m is the trace of matter stress tensor (spurion coupling for SQMH).

For this to have each candidate as a limit:
  - A12 limit: set m=0, n=0 -> pure quintessence with V -> V_A12.
    WORKS: A12 is a limit (m=0, n=0 sector).
  - C11D limit: set m=0, n=0 and V = V0*exp(-lambda*phi) -> CLW.
    WORKS: C11D is a limit (m=0, n=0 sector, specific V).
  - C28 limit: set phi=0, n=0 -> pure non-local gravity.
    WORKS: C28 is a limit (phi=0, n=0 sector, m != 0).
  - SQMH limit: set m=0, phi=0 -> pure SQMH scalar field.
    WORKS: SQMH is a limit (m=0, phi=0 sector, sigma != 0).

So formally, ALL FOUR (A12, C11D, C28, SQMH) are limits of a single
"kitchen sink" action with multiple decoupled sectors.

However: This unification is TRIVIAL. Any theory can be embedded in a
larger action with multiple decoupled sectors. The question is whether
there is a NECESSARY coupling that connects them.

ANSWER: There is NO necessary coupling. Each sector operates independently.
The unifying action is a SUM of independent Lagrangians with no cross terms.
This is physically uninteresting (it's just writing all theories together).

KEY INSIGHT: A unifying action containing both SQMH and candidates as
INTERACTING LIMITS (not just decoupled sectors) would require:
  - Coupling phi to n: some L_phi_n = xi(phi) * n.
  - Coupling V (C28 auxiliary) to n: L_V_n = xi' * V * n.
  Neither coupling has physical motivation in the respective theories.

FINDING (STRUCTURAL): There is no physically motivated unifying action
that contains all candidates + SQMH as INTERACTING limits. The trivial
decoupled "kitchen sink" action is vacuous. This is a STRUCTURAL SEPARATION
confirmation -- the Lagrangians are in different sectors with no forced mixing.

### [Member 8 -- Round 9 consensus and NF assessment]

Summary of Round 9 findings:

1. SQMH as slow-roll scalar field: SQMH corresponds to a scalar field n with
   quadratic potential V(n) = kappa*n^2/2 - Gamma_0*n (minimum at n* = Gamma_0/kappa).
   This is the overdamped/slow-roll limit of a standard second-order scalar field ODE.

2. A12 Lagrangian: standard quintessence with reconstructed V_A12(phi). DIFFERENT
   sector from SQMH (no matter coupling, no constant production).

3. C11D Lagrangian: exponential potential V_C11D = V0*exp(-lambda*phi). Structurally
   incompatible with SQMH's quadratic potential (different analytic form, different physics).

4. C28 Lagrangian: non-local gravity in GRAVITY SECTOR vs SQMH in MATTER SECTOR.
   Formally decoupled in any unifying action.

5. Unifying action: exists trivially (sum of independent sectors) but has no
   physically motivated cross couplings. Trivial unification is vacuous.

NEW FINDING ASSESSMENT:

NF-9 CANDIDATE: SQMH corresponds to a slow-roll scalar field with QUADRATIC potential
V(n) = kappa*n^2/2 - Gamma_0*n (harmonic-like, with minimum at n* = Gamma_0/kappa).
This distinguishes SQMH from ALL standard dark energy models, which have either
exponential, power-law, or cosmological constant potentials.

The quadratic potential is directly tied to the birth-death process structure
(NF-3): the birth-death process has a natural equilibrium n* -- the scalar field
potential minimum is AT n*.

Is this NF-grade? Yes -- the identification of SQMH's effective Lagrangian as a
quadratic potential is new. It extends NF-3 (birth-death) to a Lagrangian language.

DECISION: Register NF-9 (SQMH slow-roll quadratic potential) as STRUCTURAL FOOTNOTE.
It extends NF-3 to the Lagrangian level and confirms the structural separation.

Also note: the MATTER COUPLING SECTOR SEPARATION (SQMH in matter sector, C28 in
gravity sector) is a NF-grade structural observation.

DECISION: Include matter/gravity sector separation as part of NF-9.

---

## Round 9 Team Consensus

### New Finding: NF-9 (SQMH Lagrangian: Quadratic Potential + Matter Sector)

**Classification**: STRUCTURAL FOOTNOTE (extends NF-3 to Lagrangian language)

**Content**: The SQMH ODE corresponds to the slow-roll (overdamped) limit of a
scalar field n with:
  L_SQMH = (1/2)*(partial n)^2 - V(n) - sigma*n*rho_m(x)
  V(n) = (kappa/2)*n^2 - Gamma_0*n,  kappa = 3H + sigma*rho_m

This gives a QUADRATIC potential with minimum at n* = Gamma_0/kappa ~ Gamma_0/(3H).

Key structural properties:
  (a) Potential is QUADRATIC -- distinct from all standard dark energy (exponential,
      power-law, or Lambda). The quadratic form is a direct consequence of
      the linear birth-death process (NF-3).
  (b) Matter coupling sigma*n*rho_m is in the MATTER SECTOR, not the gravity sector.
      This contrasts with C28 (gravity sector) and A12/C11D (quintessence sector).
  (c) No unifying action connects SQMH and candidates via motivated cross couplings.
      The four theories inhabit decoupled sectors (gravity, quintessence, SQMH-matter).

**Assessment**: New insight -- the Lagrangian sector analysis is not present
in Rounds 1-8. Adds precision to the structural separation argument.

**Paper language**: "The SQMH continuity equation is the slow-roll limit of a
scalar field n with quadratic potential V(n) = (kappa/2)n^2 - Gamma_0*n,
minimum at n* = Gamma_0/kappa (the quasi-static equilibrium). The matter
coupling sigma*n*rho_m places SQMH in the matter sector, distinct from the
gravity-sector modification of C28 (non-local R*box^-1*R) and the quintessence
sector of A12/C11D (free scalar fields). No physically motivated cross-coupling
connects these sectors."

### Q3x Status After Round 9

- Q31 (A12 chi^2/dof < 1.0): FAIL. A12 is quintessence sector, SQMH is matter sector.
  Different Lagrangian structure. No unifying action with motivated coupling.
- Q32 (C11D sigma_eff match): FAIL. C11D exponential potential ≠ SQMH quadratic.
  Different analytic form, no mapping even within quintessence sector.
- Q33 (C28 residual < 20%): FAIL. C28 gravity sector ≠ SQMH matter sector.
  No overlap in Lagrangian structure.

**Round 9 Verdict: Q31/Q32/Q33 REMAIN FAIL.**
NF-9 (SQMH Lagrangian: quadratic potential + matter sector) registered as STRUCTURAL FOOTNOTE.

---

*Round 9 complete: 2026-04-11*
