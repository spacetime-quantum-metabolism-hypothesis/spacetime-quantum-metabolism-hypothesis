# refs/l8_round7_verdict.md -- L8 Round 7: Holographic / Entropic Gravity

> Date: 2026-04-11
> Round 7 of second batch (Rounds 7-11).
> Method: 8-person parallel team, all 3 candidates + SQMH simultaneously.
> Focus: Holographic/entropic gravity framework -- Verlinde, holographic DE,
>   Jacobson thermodynamics. Does SQMH fit into any of these frameworks?
>   Do A12/C11D/C28 share holographic structure with SQMH?
> Prior established: Q31/Q32/Q33 FAIL (Rounds 1-6). NF-1 through NF-6 registered.

---

## Framework Overview

Three distinct holographic/entropic gravity approaches probed:

1. Verlinde entropic gravity: F = T * Delta_S / Delta_x.
   Gravity as emergent from entropy gradients on holographic screens.

2. Holographic dark energy: rho_DE = 3c^2 M_P^2 / L^2.
   L = IR cutoff (Hubble, future horizon, Ricci scale).

3. Jacobson thermodynamics: dE = TdS on local Rindler horizons.
   Einstein equations emerge; any modification of L must preserve dE=TdS.

---

## 8-Person Parallel Discussion

### [Member 1 -- Verlinde entropic gravity vs SQMH]

Verlinde (2011, arXiv:1001.0785): Gravity emerges from entropy changes
when matter moves in an information field. The entropic force is:
  F = T * Delta_S / Delta_x  [temperature * entropy gradient]

The entropy on the holographic screen of radius R:
  S = A / (4 * l_P^2) = 4*pi*R^2 / (4*l_P^2) = pi*R^2/l_P^2

The temperature on the screen:
  T = hbar*a / (2*pi*c*k_B)  [Unruh temperature for acceleration a]

For cosmological application (Verlinde 2011, Sec 6):
  The dark energy density arises from an "elastic" response of spacetime.
  rho_DE = 3*H^2*M_P^2 * (L/H^-1) correction terms.

Now consider SQMH. The "quantum metabolic units" n_bar with energy mu each
give a dark energy density rho_DE = n_bar * mu.

Does SQMH fit into Verlinde's entropic framework?

For Verlinde, the dark energy must come from a GRAVITATIONAL entropy change.
SQMH posits dark energy from MATTER + QUANTUM VACUUM interactions:
  - Production Gamma_0: vacuum -> metabolic units (constant).
  - Loss sigma*n_bar*rho_m: matter collision destroys metabolic units.

Verlinde's approach does NOT include a production term Gamma_0; his dark energy
is a BULK entropy effect with no kinetic source. The binary collision term
sigma*n_bar*rho_m has no analog in Verlinde's framework (his matter-energy
is on the holographic screen, not a collision partner).

SQMH also has a SPECIFIC value sigma = 4*pi*G*t_P. In Verlinde's framework,
the only dimensionful quantities are G, c, hbar -- NO t_P appears explicitly.

Verdict: SQMH does NOT naturally fit into Verlinde's entropic framework.
  - Verlinde requires no explicit t_P.
  - Verlinde has no production term analog for Gamma_0.
  - Verlinde's entropic gravity is a STATIC emergent gravity, not a kinetic
    matter-dark energy coupling.

Note (SPECULATIVE, not NF-grade): One could try to FORCE-FIT Verlinde by
interpreting n_bar as a surface entropy density on a holographic screen
and Gamma_0 as an entropy production rate. But this requires additional
assumptions not present in Verlinde's original formulation.

### [Member 2 -- Holographic dark energy (HDE) vs SQMH]

Standard holographic dark energy (Cohen-Kaplan-Nelson 1999, Li 2004):
  rho_DE = 3c^2 M_P^2 / L^2

where L is an IR cutoff. Three choices:
  (a) L = H^-1 (Hubble horizon): gives rho_DE ~ rho_crit ~ E^2 [same as LCDM]
  (b) L = R_h (future horizon): gives accelerating expansion
  (c) L = R_Ricci = sqrt(6/(R)) (Ricci scale): gives Ricci HDE

Question: Is there a choice of L that gives rho_DE ~ n_bar(t) * mu ~ SQMH behavior?

From SQMH: n_bar ~ Gamma_0 / (3H) at late times (sigma*rho_m << 3H).
  rho_DE_SQMH ~ n_bar * mu ~ Gamma_0 * mu / (3H)

For HDE: rho_DE = 3c^2 M_P^2 / L^2
  If L = L_SQMH, then: L_SQMH^2 = 3c^2 M_P^2 / (n_bar * mu)
  = 3c^2 M_P^2 * 3H / (Gamma_0 * mu)

This defines a SQMH holographic length:
  L_SQMH = sqrt(9 c^2 M_P^2 H / (Gamma_0 * mu))

Substituting Gamma_0 = 3H * n_bar_eq and n_bar_eq * mu = rho_DE_eq:
  L_SQMH = sqrt(9 c^2 M_P^2 H / (3H * rho_DE_eq))
  = sqrt(3 c^2 M_P^2 / rho_DE_eq)
  = sqrt(3) * M_P / sqrt(rho_DE_eq)
  ~ sqrt(3) * H_0^-1 * c  [since rho_DE_eq ~ rho_crit ~ 3M_P^2 H_0^2/c^2]

This gives L_SQMH ~ sqrt(3) * c/H_0 ~ sqrt(3) * Hubble horizon!

STRUCTURAL FINDING: The SQMH quasi-static solution maps to a holographic
dark energy model with IR cutoff L ~ sqrt(3) * Hubble horizon.

However: This is the QUASI-STATIC limit (sigma << H). The full SQMH ODE
contains the sigma*n_bar*rho_m term which breaks simple HDE because L becomes
time-dependent in a specific way that depends on sigma (and hence t_P).

For the HDE to encode sigma = 4*pi*G*t_P, we would need:
  L^2 ~ L_Hubble^2 * (1 + correction proportional to sigma*rho_m/H)

The correction is of order Pi_SQMH ~ 10^-62, completely negligible.

CONCLUSION FOR HDE: SQMH in the quasi-static limit is trivially equivalent
to a Hubble-horizon HDE with c^2 = (1/3) * (rho_DE_eq / rho_crit).
The sigma coupling that distinguishes SQMH from LCDM contributes a 10^-62
correction to L. HDE with L ~ H^-1 does NOT capture the SQMH dynamics.

Is this an NF? No -- it confirms that SQMH is LCDM-like (known from Round 1).
The "HDE length scale" identification is a tautological rewriting, not new physics.

### [Member 3 -- Jacobson thermodynamics vs SQMH]

Jacobson (1995, PRL 75 1260): Einstein equations dG_mu_nu = 8*pi*G * T_mu_nu
emerge from dE = TdS applied to local Rindler horizons.

For SQMH to be "entropic dark energy" in Jacobson's sense, the dark energy
stress tensor T_DE (from n_bar) must be consistently derived from TdS on
some surface.

Jacobson's original derivation requires:
  1. Local Rindler horizon with Unruh temperature T = hbar*kappa/(2*pi*c)
  2. Entropy S = A/(4*l_P^2) (Bekenstein-Hawking)
  3. Heat flux delta_Q = T*dS through the horizon

For SQMH as dark energy:
  rho_DE = n_bar * mu
  p_DE = -rho_DE  [if w = -1, as in quasi-static limit]

The stress tensor T_mu_nu = diag(-rho_DE, p_DE, p_DE, p_DE) satisfies
the continuity equation dE = TdS only if:
  drho_DE/dt + 3H*(rho_DE + p_DE) = -Gamma (source term)
  => drho_DE/dt = -Gamma  [since p_DE = -rho_DE]

where Gamma is an entropy production rate.

For SQMH: drho_DE/dt = (dn_bar/dt)*mu
  From ODE: dn_bar/dt = Gamma_0 - sigma*n_bar*rho_m - 3H*n_bar
  drho_DE/dt = mu * [Gamma_0 - sigma*n_bar*rho_m - 3H*n_bar]

At quasi-static: drho_DE/dt ~ -3H*n_bar*mu ~ -3H*rho_DE [dilution only]

For Jacobson: the "entropy production rate" Gamma_SQMH corresponds to:
  Gamma_SQMH = -mu * (Gamma_0 - sigma*n_bar*rho_m - 3H*n_bar)

This is NOT a simple horizon entropy production rate.
The sigma*n_bar*rho_m term introduces a MATTER-DARK ENERGY coupling not
present in Jacobson's vacuum Rindler derivation.

CONCLUSION: SQMH cannot be cleanly derived from Jacobson's TdS formalism
without extending it to include coupled matter-dark energy entropy exchanges.
This is a known open problem in entropic gravity (beyond Jacobson 1995).

### [Member 4 -- A12 in holographic framework]

A12: erf-type CPL parameterization with w0=-0.886, wa=-0.133.

CPL w(a) = w0 + wa*(1-a) is phenomenological. It has no holographic motivation.

For A12 to be a holographic DE model, we would need:
  rho_DE = 3*c^2*M_P^2 / L(a)^2
  where L(a) gives w(a) = w0 + wa*(1-a).

From: 1 + w = -(1/3) * d(ln rho_DE) / d(ln a)
  d(ln rho_DE)/d(ln a) = -3*(1 + w0 + wa*(1-a))
  
Integrating: rho_DE(a) = rho_DE0 * exp(-3*[(1+w0+wa)*ln(a) + wa*(a-1)])
  = rho_DE0 * a^(-3*(1+w0+wa)) * exp(3*wa*(1-a))

For this to equal 3*c^2*M_P^2/L^2:
  L(a) = sqrt(3*c^2*M_P^2 / rho_DE0) * a^(3*(1+w0+wa)/2) * exp(-3*wa*(1-a)/2)

This gives a valid L(a) for any CPL, but L(a) is just derived from w(a) -- no
physical IR cutoff meaning. It's a mathematical rewriting, not a holographic derivation.

A12 is NOT a holographic dark energy model in any standard sense.

Compare to SQMH: SQMH L ~ H^-1 (Hubble horizon, as shown by Member 2).
A12 L(a) deviates from H^-1 by an amount proportional to wa = -0.133.

Gap: A12's L(a) and SQMH's L ~ H^-1 differ by a factor (1 + O(wa)).
This is the SAME 5% difference identified in Round 1. No new insight.

### [Member 5 -- C11D (CLW disformal) in holographic framework]

C11D: Coupled quintessence/disformal with CLW potential V ~ exp(-lambda*phi).

Holographic DE for scalar field theories (Nojiri-Odintsov 2006):
  For a scalar field phi with V(phi), the effective IR cutoff is:
    L_eff = sqrt(M_P^2 * V / rho_phi)

For C11D with V = V0*exp(-lambda*phi) and E(a), L_eff(a) is calculable.
At the CLW attractor (lambda > sqrt(6)): rho_phi ∝ rho_m, V/rho_phi = const.
  L_eff ~ sqrt(M_P^2 * V0 * exp(-lambda*phi)) / rho_phi^(1/2)

This is time-varying. There is no fixed holographic length for C11D.

More importantly: C11D is a SCALAR FIELD theory with kinetic and potential
terms. The holographic DE framework parametrizes DE as rho_DE = 3*M_P^2/L^2.
C11D DE density is given by rho_phi = (phi_dot^2)/2 + V(phi).
These are equivalent only if L(a) = sqrt(3*M_P^2/rho_phi(a)).

There is no holographic structure unique to C11D (beyond tautological rewriting).

C11D shares NO special holographic structure with SQMH.

### [Member 6 -- C28 (non-local gravity) in holographic framework]

C28: Non-local gravity, R(box^-1 R)^2 (Maggiore-Mancarella).

Non-local gravity has a DEEP connection to holography (Arkani-Hamed et al 2002,
Porrati 2002): The Dvali-Gabadadze-Porrati (DGP) brane model, which produces
a specific non-local gravity term, emerges from holographic considerations.
C28's non-local operator box^-1*R can be related to graviton bulk propagation
in AdS/CFT holography.

However, the SPECIFIC connection between C28 and holographic DE is:

Maggiore-Mancarella model:
  S = M_P^2/2 * int d^4x sqrt(-g) * [R - m^2/6 * R * (box^-1 R)]

where m is the non-local mass. This has been shown (Maggiore 2015) to be
equivalent to a two-scalar-field system. The effective DE equation of state
is w_DE ~ -1 at z=0.

For holographic interpretation: The operator m^2 * R * box^-1*R can be
related to an ENTROPY DEFICIT of a black hole in a thermal bath
(Maggiore 2015, arXiv:1506.06217, footnote). But this connection is
speculative and not a formal derivation.

C28 mass parameter m: C28 uses gamma_0 = 0.0015 (= m^2/(9H_0^2)).
  m = H_0 * sqrt(9*gamma_0) = H_0 * sqrt(0.0135) ~ 0.116 * H_0.
  m ~ 10^-33 eV (in natural units).

Is there a holographic origin for m? If the graviton had a small mass m ~ H_0
from holographic considerations, this would give C28 a holographic motivation.
Some models (Gabadadze-Shifman 2004, "soft graviton mass") do produce m ~ H_0.

STRUCTURAL FINDING (SPECULATIVE): C28's non-local operator may have a weak
holographic motivation via graviton soft mass (m ~ H_0). This is different
from SQMH which requires t_P explicitly. 

If C28's m ~ H_0 and SQMH's sigma ~ G*t_P, then:
  C28 is infrared (m ~ H_0, no QG input)
  SQMH is ultraviolet (sigma ~ G*t_P, QG input required)
These are COMPLEMENTARY, not isomorphic.

### [Member 7 -- Does any candidate share SQMH holographic structure?]

Summary of holographic analysis for all three candidates:

A12: CPL parameterization. No holographic structure. L(a) is just a
mathematical rewriting of w(a). No connection to SQMH's L ~ H^-1.

C11D: Scalar field. L(a) = sqrt(3*M_P^2/rho_phi(a)) is a standard
tautological HDE equivalent. No special holographic structure. No t_P.

C28: Non-local gravity. Weakest holographic connection via graviton
soft mass (m ~ H_0). No QG input. No t_P. The non-local operator is
related to infrared gravity, not ultraviolet (Planck-scale) physics.

SQMH: sigma = G*t_P embeds t_P explicitly. If SQMH has a holographic
interpretation, it must come from PLANCK-SCALE holography (Bekenstein-Hawking
entropy at the Planck area, not the Hubble area).

Key comparison:
  SQMH L ~ Hubble horizon (quasi-static limit) but sigma encodes t_P (UV scale).
  No candidate encodes t_P.
  => SQMH's holographic length scale is degenerate with LCDM at z~0,
     but its sigma coupling has NO holographic parallel in any candidate.

POSSIBLE NF: The holographic approach CONFIRMS NF-5 from a different angle:
SQMH has a UV holographic coupling (sigma ~ G*t_P = Planck-area gravity coupling)
while all candidates are PURE IR theories. This makes SQMH holographically
unique but also holographically disconnected from all three candidates.

This is a RECONFIRMATION of NF-5, not a new independent finding.

### [Member 8 -- Round 7 consensus and new finding assessment]

Summary of Round 7 analysis:

Verlinde entropic gravity: SQMH does NOT fit. Verlinde has no t_P, no Gamma_0
  production term, no matter-dark energy coupling.

Holographic dark energy: SQMH quasi-static limit ~ Hubble-horizon HDE
  (c^2 = 1/3 convention). This is a tautological rewriting. The sigma term
  contributes only 10^-62 correction to L. Not new.

Jacobson thermodynamics: SQMH cannot be derived from dE=TdS without extending
  Jacobson to include coupled matter-dark energy entropy exchanges.

Candidates A12/C11D: No special holographic structure. No t_P.

Candidate C28: Weak holographic motivation via graviton soft mass (m ~ H_0).
  This is DISTINCT from SQMH's UV holographic coupling.

NEW FINDING ASSESSMENT:
The holographic analysis reveals a clear separation:
  SQMH: UV holographic coupling (sigma = G*t_P, Planck area = l_P^2).
  A12, C11D: No holographic structure beyond tautological rewriting.
  C28: IR holographic structure (m ~ H_0, Hubble horizon).

This is a STRUCTURAL FINDING worth noting: the holographic energy scales
are opposite for SQMH vs C28. SQMH: UV-motivated (t_P). C28: IR-motivated (H_0^-1).

CLASSIFICATION: This is a RECONFIRMATION + EXTENSION of NF-5 (the Pi_SQMH
= Omega_m * H_0 * t_P argument). The holographic angle adds the language
"UV vs IR holographic coupling" but does not constitute an independent new finding.

DECISION: Register as NF-7 (holographic UV/IR complementarity) with
STRUCTURAL FOOTNOTE classification -- not main text quality, but
adds holographic language to the Pi_SQMH narrative.

---

## Round 7 Team Consensus

### New Finding: NF-7 (Holographic UV/IR Complementarity)

**Classification**: STRUCTURAL FOOTNOTE

**Content**: The holographic analysis reveals a UV/IR energy scale separation:
  - SQMH: sigma = 4*pi*G*t_P embeds the Planck area l_P^2 = G*hbar/c^3.
    In holographic language, sigma encodes the PLANCK-SCALE (UV) entropy per
    unit area (1/l_P^2 = 1/(G*hbar/c^3)) times a Planck-time coupling.
  - C28: mass parameter m ~ 0.116*H_0 encodes the HUBBLE-SCALE (IR) cutoff.
    C28 is an IR non-local gravity model.
  - A12, C11D: No holographic structure beyond tautological rewriting.

The UV/IR complementarity means:
  SQMH and C28 are "holographically orthogonal" -- they encode opposite
  energy scales. Any theory containing BOTH would require explicit UV-IR
  mixing (e.g., string theory's UV/IR mixing, holographic swampland criteria).

This RECONFIRMS NF-5 (Pi_SQMH = Omega_m * H_0 * t_P) from a holographic angle.
The gap is not just dimensional but holographic: SQMH lives in UV, C28 in IR.

**Paper language**: "The holographic interpretation of SQMH reveals a UV/IR
complementarity: sigma = 4pi*G*t_P encodes Planck-scale (UV) entropy coupling,
while the surviving dark energy candidates A12, C11D operate without holographic
scale input and C28 encodes Hubble-scale (IR) non-local gravity. This holographic
UV/IR separation provides an independent perspective on the structural gap
identified in NF-5."

### Q3x Status After Round 7

- Q31 (A12 chi^2/dof < 1.0): FAIL. Holographic analysis adds no new path.
- Q32 (C11D sigma_eff match): FAIL. No holographic structure in C11D.
- Q33 (C28 residual < 20%): FAIL. C28 IR holographic ≠ SQMH UV holographic.

**Round 7 Verdict: Q31/Q32/Q33 REMAIN FAIL.**
NF-7 (holographic UV/IR complementarity) registered as STRUCTURAL FOOTNOTE.

---

*Round 7 complete: 2026-04-11*
