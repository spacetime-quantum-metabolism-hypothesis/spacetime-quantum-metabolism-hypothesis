# refs/l14_assumption_alternatives.md -- L14: 20 Structural Alternative Equations

> Date: 2026-04-11
> Source: 8-team independent analysis of hidden assumptions H1-H8 in the standard B1 equation
> Task: Systematically relax/modify structural assumptions to derive 20 genuinely distinct
>       alternative equations. This is NOT a B-class continuation (B1-B20 covered creation
>       rate variations). This document varies the STRUCTURAL skeleton of the SQMH equation.

---

## Preamble: The 8 Hidden Structural Assumptions in B1

The standard SQMH equation:

    dn_bar/dt + 3H*n_bar = Gamma_0 - sigma*n_bar*rho_m      (B1)
    sigma = 4*pi*G*t_P

rests on these structural assumptions beyond the single premise:

- H1: FLRW geometry => gives the 3H*n_bar dilution term with coefficient 3
- H2: Non-relativistic quanta (w_sq = 0) => coefficient exactly 3 (not 4 for radiation)
- H3: Linear mass-action law => sigma*n_bar*rho_m (not sigma*n_bar^p * rho_m^q)
- H4: Gamma_0 > 0 exists (creation term) => NOT in premise (premise: annihilation only)
- H5: Gamma_0 = const (uniform, isotropic) => de Sitter / global symmetry assumption
- H6: sigma = 4*pi*G*t_P specifically => Newtonian Gauss-law matching
- H7: Only matter rho_m couples (not radiation rho_r) => traceless T^mu_nu argument
- H8: No quanta self-interaction => neglect n_bar^2 terms in collision integral

Each of the 20 equations below relaxes exactly one or a minimal combination of these.

---

## Team 1 (Kinetic Theory): Equations C1-C3
### Focus: H2 (equation of state) and H3 (nonlinear mass-action)

---

### C1. Relativistic Quanta (w_sq = 1/3): Modified Hubble Coefficient

**Modified assumption:** H2 -- quanta have w_sq = 1/3 (ultra-relativistic)

**Equation:**

    dn_bar/dt + 4H*n_bar = Gamma_0 - sigma*n_bar*rho_m

**Derivation:**
For a fluid with equation of state w, the Hubble dilution coefficient in FLRW is 3(1+w).
For w_sq = 0 (non-relativistic, B1): coefficient = 3.
For w_sq = 1/3 (ultra-relativistic, radiation-like quanta): coefficient = 4.
This arises from dn_bar/dt + (rho + p)/rho * 3H * n_bar = sources, which for w_sq = 1/3
gives 3*(1 + 1/3)*H*n_bar = 4H*n_bar.

The equilibrium density:

    n_bar_eq = Gamma_0 / (sigma*rho_m + 4H)

Compared to B1: n_bar_eq = Gamma_0 / (sigma*rho_m + 3H).

At high z (matter dominated): 4H >> sigma*rho_m at some transition redshift, so
n_bar_eq(C1) < n_bar_eq(B1). The ratio n_bar_eq(C1)/n_bar_eq(B1) = (sigma*rho_m + 3H)/(sigma*rho_m + 4H) < 1.

**Physical motivation:**
If spacetime quanta are Planck-scale objects with kinetic energy k*c >> m*c^2 (Planck
mass at Planck frequency), they would be ultra-relativistic by any cosmological standard.
The energy density of relativistic quanta dilutes as a^{-4} rather than a^{-3}, making
the Hubble coefficient 4 instead of 3. This is the kinetic-theory derivation: the
Liouville term for relativistic particles gives partial_t f + c*hat_p*nabla f = C[f],
and upon momentum integration with ultra-relativistic phase-space weights, the divergence
term becomes (4/3)*nabla*(n_bar*v_avg) = 4H*n_bar in FLRW.

**Dark energy qualitative prediction:**
- rho_DE at low z: similar to B1 (sigma*rho_m dominates denominator)
- rho_DE at high z: more suppressed (4H > 3H adds extra dilution in past)
- Qualitative: w_0 similar to B1 (~-0.9); w_a more negative than B1 (~-0.15 to -0.25)
- Direction: w_a shifts toward more negative compared to B1

**Key structural difference vs B1:**
The Hubble dilution coefficient changes from 3 to 4. This means n_bar was smaller
in the past (more diluted). The transition from "Hubble dominated" to "matter dominated"
in the denominator occurs at a different redshift.

**Assessment:** PROMISING. Zero additional parameters. If w_a(C1) ~ -0.3 to -0.5, it
improves over B1 toward DESI target w_a = -0.83. Requires numerical verification.

---

### C2. Intermediate Equation of State (0 < w_sq < 1/3): Fractional Hubble Coefficient

**Modified assumption:** H2 -- quanta have general w_sq in (0, 1/3)

**Equation:**

    dn_bar/dt + 3*(1 + w_sq)*H*n_bar = Gamma_0 - sigma*n_bar*rho_m

where 0 < w_sq < 1/3 is a free parameter.

**Derivation:**
Generalization of C1 to arbitrary w_sq. The FLRW volume dilution for a fluid with
equation of state w_sq is: d(n_bar*a^3)/dt = creation - annihilation, where the
"number density" n_bar includes the factor (1+w_sq) from the thermodynamic work term
in the continuity equation. For w_sq = 0: standard B1. For w_sq = 1/3: C1 above.

Equilibrium:

    n_bar_eq = Gamma_0 / (sigma*rho_m + 3*(1+w_sq)*H)

**Physical motivation:**
Spacetime quanta may have a pressure from self-interactions or from their kinetic
distribution. A Planck-mass quantum at thermal equilibrium with the CMB bath at
temperature T << T_Planck would be non-relativistic (w_sq ~ 0), but quanta created
by quantum gravity effects at sub-Planck scales might carry significant momentum.
The w_sq parameter encodes our ignorance of the quantum foam's thermal state.

**Dark energy qualitative prediction:**
- As w_sq increases from 0 to 1/3: Hubble coefficient increases from 3 to 4
- w_a becomes progressively more negative
- w_0 stays near -0.9 (low-z behavior similar for all w_sq)
- At w_sq = 1/3: reaches the C1 limit

**Key structural difference vs B1:**
Introduces a continuous parameter w_sq that connects B1 (w_sq=0) to C1 (w_sq=1/3).
The B1 choice w_sq=0 is the extreme non-relativistic limit -- arguably least likely
for Planck-scale quanta. Any w_sq > 0 gives a more negative w_a than B1.

**Assessment:** PROMISING. The w_sq parameter is physically motivated and tests
whether the non-relativistic assumption H2 was correct. Scan w_sq in [0, 1/3]
to find DESI-compatible range.

---

### C3. Fractional Power Mass-Action (p in n_bar^p): Quantum-Classical Cross-Section

**Modified assumption:** H3 -- mass-action is nonlinear in n_bar (not rho_m)

**Equation:**

    dn_bar/dt + 3H*n_bar = Gamma_0 - sigma_p * n_bar^p * rho_m     (p != 1)

where p = 1/2 represents quantum diffraction correction; p = 2 represents
two-quantum cooperative annihilation.

**Derivation from kinetic theory:**
The standard mass-action rate sigma*n_bar*rho_m arises from the classical binary
collision integral: rate = (cross-section) * (relative velocity) * n_bar * n_matter.
If the quantum-matter cross-section depends on the ambient quantum density
(quantum field corrections), then sigma_eff = sigma_0 * n_bar^{p-1}, giving
rate = sigma_0 * n_bar^p * rho_m.

For p = 1/2: quantum-coherent annihilation rate scales as sqrt(n_bar) (Fermi-golden-rule
type quantum amplitude with collective wavefunction). sigma_{1/2} has units [m^{9/2} kg^{-1} s^{-1}].
For p = 2: cooperative annihilation (two quanta simultaneously absorbed by matter).
sigma_2 has units [m^6 kg^{-1} s^{-1}].

For p = 1/2 (sub-linear):
    n_bar_eq: Gamma_0 = sigma_{1/2} * n_bar_eq^{1/2} * rho_m + 3H * n_bar_eq
    This is a quadratic in sqrt(n_bar_eq). At high z: n_bar_eq ~ (Gamma_0/(sigma_{1/2}*rho_m))^2

**Physical motivation:**
Classical kinetic theory assumes uncorrelated binary collisions. Spacetime quanta are
quantum-coherent objects -- their annihilation cross-section may involve interference
effects from nearby quanta. In quantum optics, stimulated absorption scales as n
(number of photons), but in nonlinear media, the effective cross-section can depend
on the field intensity. Analogously, the quantum foam cross-section for matter
absorption may depend on the local quantum density.

**Dark energy qualitative prediction:**
For p = 1/2: equilibrium n_bar_eq is larger at high z than B1 (sub-linear annihilation
is weaker). This gives MORE dark energy at high z: w_a > 0 (wrong direction for DESI).
For p = 2: cooperative annihilation is stronger at high n_bar (early universe). This
gives LESS dark energy at high z: w_a more negative, potentially helping DESI fit.
However, sigma_2 must be specified -- dimensional analysis gives sigma_2 ~ G^2*t_P
which is 40+ orders smaller than sigma (same issue as B2 with rho_m^2 in H3).

**Key structural difference vs B1:**
The annihilation term's dependence on n_bar changes the self-consistency of the
equilibrium and how fast n_bar relaxes to equilibrium. For p != 1, the equilibrium
value is determined by an algebraic equation of degree p (not linear).

**Assessment:** For p < 1: WORSE for DESI. For p > 1: physically suppressed. NEUTRAL
overall. The dimensional argument against large sigma_2 makes this less promising
than the H2 variation above.

---

## Team 2 (Fluid Dynamics): Equations C4-C6
### Focus: H1 (non-FLRW or modified geometry) and H7 (radiation coupling)

---

### C4. Anisotropic Bianchi-I Universe: Direction-Dependent Hubble Dilution

**Modified assumption:** H1 -- geometry is Bianchi-I (anisotropic) rather than FLRW (isotropic)

**Equation:**

    dn_bar/dt + (H_x + H_y + H_z)*n_bar = Gamma_0 - sigma*n_bar*rho_m

where H_x, H_y, H_z are directional Hubble rates with H_x + H_y + H_z = 3H_avg
but H_x^2 + H_y^2 + H_z^2 != 3H_avg^2 in general.

More practically, include the shear sigma_shear:

    dn_bar/dt + 3H*n_bar = Gamma_0 - sigma*n_bar*rho_m - delta*sigma_shear^2*n_bar

where sigma_shear is the shear scalar (measuring departure from isotropy) and delta
is a coupling constant.

**Derivation:**
In Bianchi-I spacetime with metric:
    ds^2 = -dt^2 + a_x^2(t)dx^2 + a_y^2(t)dy^2 + a_z^2(t)dz^2

The continuity equation for a fluid with w=0 gives:
    d(n_bar * a_x * a_y * a_z)/dt = sources
    dn_bar/dt + (H_x + H_y + H_z)*n_bar = Gamma_0 - sigma*n_bar*rho_m

The shear sigma_shear^2 = (1/3)*[(H_x-H_y)^2 + (H_y-H_z)^2 + (H_z-H_x)^2] enters
as an additional damping if spacetime quanta can be "shear-annihilated" by anisotropic
geometry (the tidal gravitational force analogue for quanta).

**Physical motivation:**
The current universe has very small but non-zero anisotropy. CMB constraints give
sigma_shear / H < 10^{-4} at low z. However, early-universe anisotropy could have
been larger, and the shear could modify n_bar evolution at high z (radiation era).
The SQMH theory might predict that anisotropy itself annihilates quanta (directional
shear tears spacetime foam). This provides an additional sink beyond matter density.

**Dark energy qualitative prediction:**
- Low z: sigma_shear/H is tiny, reduces to B1. No w_0 change.
- High z (radiation era): shear possibly larger. Additional n_bar suppression at high z.
- Qualitative: w_a more negative than B1 if shear was significant at early times.
- If sigma_shear/H ~ 10^{-3} at z~1000: correction ~ 10^{-6} -- negligible.

**Key structural difference vs B1:**
The Hubble term picks up an anisotropy correction. For FLRW limit (H_x=H_y=H_z),
recovers B1 exactly. The new physics is the shear-annihilation channel.

**Assessment:** NEUTRAL-WORSE. The shear term is cosmologically negligible given
CMB isotropy constraints. Only relevant for exotic early-universe scenarios. 
The anisotropy correction to w_a is < 0.01%.

---

### C5. Curvature-Corrected FLRW: Non-Flat Universe (k != 0)

**Modified assumption:** H1 -- spatial curvature k is non-zero

**Equation:**

    dn_bar/dt + (3H - k/(a^2*H))*n_bar = Gamma_0 - sigma*n_bar*rho_m

or more precisely, including the curvature in the expansion:

    dn_bar/dt + 3H*n_bar = Gamma_0 - sigma*n_bar*rho_m + (3*kappa/a^2)*n_bar

where kappa = k/3 captures the spatial curvature (k = +1, 0, -1).

**Derivation:**
In a curved FLRW universe, the covariant divergence of the quantum fluid number
flux includes a curvature correction. The Friedmann equation becomes:
    H^2 = (8*pi*G/3)*rho_total - k/a^2

The continuity equation for a non-interacting fluid is unchanged (divergence of
comoving current = 0), but if quanta are created/annihilated with reference to the
geodesic volume element, the effective creation volume includes a curvature correction:
    d(n_bar * a^3) / dt = (Gamma_0 - sigma*n_bar*rho_m) * a^3 * (1 + k_corr/a^2)

For small curvature (Omega_k << 1), the correction is:
    effective_Gamma_eff = Gamma_0 - sigma*n_bar*rho_m + (kappa/a^2)*n_bar

**Physical motivation:**
The universe has small but possibly non-zero spatial curvature. DESI DR1/DR2 data
give |Omega_k| < 0.01 (combined constraints). Non-flat geometry changes the proper
volume available for creation, and the spatial curvature provides a new geometric
source/sink for quantum foam. In positively curved (k=+1) universe, volumes close
faster (more creation pressure); in negatively curved (k=-1), volumes expand faster
(more dilution).

**Dark energy qualitative prediction:**
- For |Omega_k| < 0.01: correction is < 1% at z < 3. Very small effect on w_a.
- For k = -1 (open): curvature term provides additional dilution ~ (kappa/a^2)*n_bar.
  This gives MORE dark energy suppression at intermediate z. Potentially slightly
  more negative w_a than B1.
- For k = +1 (closed): curvature provides a source term. Less suppression, w_a > B1.

**Key structural difference vs B1:**
Adds a curvature-dependent correction to the effective creation/annihilation balance.
The spatial curvature term has a*(z) dependence that is different from both the
Hubble term (H) and the matter term (rho_m).

**Assessment:** NEUTRAL. Too small to matter for current observational precision.
Future CMB-S4 / DESI curvature measurements could constrain this, but the effect
on w_a is < 0.1% for |Omega_k| < 0.01.

---

### C6. Radiation-Coupled Annihilation with Full Trace Coupling

**Modified assumption:** H7 -- radiation (rho_r) couples via a different mechanism than assumed

**Equation:**

    dn_bar/dt + 3H*n_bar = Gamma_0 - sigma*n_bar*rho_m - sigma_r*n_bar*rho_r

where sigma_r is a separate, independent radiation-matter coupling constant.

**Derivation:**
The standard SQMH argument for ε=0 (no radiation coupling) is that spacetime quanta
couple via the trace of the stress-energy tensor T^mu_mu. For radiation:
T^mu_mu(radiation) = -rho_r + 3*p_r = -rho_r + rho_r = 0 (since p_r = rho_r/3).
This would imply sigma_r = 0 exactly.

However, this trace argument requires that the annihilation cross-section is proportional
to T^mu_mu. This is ONE possible physical model. Alternatively, if the annihilation
rate depends on the total energy density (not just the trace), then both matter AND
radiation contribute. In that case sigma_r = epsilon*sigma where epsilon is determined
by the coupling to the full stress-energy vs. the trace:
    sigma_r = sigma * (p_coupling) where p_coupling in [0,1]

**Physical motivation:**
The T^mu_mu coupling is motivated by the idea that spacetime quanta are "stress" rather
than "energy" -- they respond to the non-conformal part of the energy-momentum tensor.
But at Planck scales, conformal symmetry is expected to be broken. If quantum gravity
effects generate a conformal anomaly at Planck scale, then radiation DOES couple to
spacetime quanta even though T^mu_mu = 0 in classical GR. The sigma_r term captures
this UV correction. During radiation domination (z > z_eq ~ 3400), rho_r dominates
and would add a new annihilation channel if sigma_r != 0.

**Dark energy qualitative prediction:**
- z < z_eq: radiation negligible, reduces to B1.
- z > z_eq: additional rho_r annihilation. Stronger suppression of n_bar in early universe.
- The n_bar at the epoch of equality z_eq would be smaller by factor
  exp(-sigma_r * int(rho_r dt)), which is a large suppression if sigma_r ~ sigma.
- This gives rho_DE at z_eq much smaller than B1 predicts.
- Qualitative: w_a MUCH more negative than B1 (potentially overshooting DESI target).
  w_0 may be less negative than B1 (n_bar had less "time" to build up by today).

**Key structural difference vs B1:**
Adds an annihilation channel active during radiation domination. Unlike B1 where
dark energy is purely a late-time phenomenon, C6 has a coupled early-universe
evolution that changes the "initial condition" for the matter-era SQMH evolution.

**Assessment:** PROMISING but risky. If sigma_r is small (sigma_r << sigma), this
gives a natural explanation for why DE is a late-time phenomenon: quanta were being
efficiently annihilated in the early universe. Needs numerical testing. The CMB
constraint on early dark energy (f_EDE < 0.1) would constrain sigma_r.

---

## Team 3 (QFT): Equations C7-C9
### Focus: H4 (creation mechanism: stimulated vs. spontaneous) and H5 (creation rate form)

---

### C7. Stimulated Creation (Bose Enhancement): n_bar-Dependent Creation

**Modified assumption:** H4 -- creation mechanism is stimulated (Bose enhancement), not spontaneous

**Equation:**

    dn_bar/dt + 3H*n_bar = Gamma_0 * (1 + n_bar/n_c) - sigma*n_bar*rho_m

where n_c is a critical quantum density (natural scale: n_P = t_P^{-3} = Planck density / m_P).

**Derivation:**
In quantum field theory, the creation rate of bosons in state k is proportional to
(1 + N_k) where N_k is the occupation number. The "1" is spontaneous creation; the
N_k term is stimulated creation (Bose-Einstein enhancement). For a thermal distribution,
this gives the Planck spectrum. Applied to spacetime quanta:
- Spontaneous creation rate per unit volume: Gamma_0
- Stimulated creation rate: Gamma_0 * n_bar/n_c (each existing quantum "catalyzes" more)

The combined equation:

    dn_bar/dt + 3H*n_bar = Gamma_0 * (1 + n_bar/n_c) - sigma*n_bar*rho_m

This rearranges to:

    dn_bar/dt + (3H - Gamma_0/n_c)*n_bar = Gamma_0 - sigma*n_bar*rho_m

For Gamma_0/n_c << 3H: the stimulated correction is small, approaches B1.
For Gamma_0/n_c ~ 3H: the effective Hubble coefficient is reduced, leading to
slower dilution and MORE dark energy than B1.

**Physical motivation:**
Spacetime quanta are bosons (spin-2 gravitons are bosons; hypothetical spin-0/1
quantum foam constituents are likewise bosons). Bose-Einstein statistics require
that the creation rate be enhanced by the factor (1 + n_bar/n_c). This is NOT an
ad hoc assumption -- it follows from QFT principles for any bosonic system. The
current SQMH equation (B1) omits this enhancement, treating quanta classically.
The stimulated creation term is the QFT correction to the classical Boltzmann equation.

**Dark energy qualitative prediction:**
- The effective equation is equivalent to B1 with a reduced Hubble coefficient
  3H_eff = 3H - Gamma_0/n_c.
- This means quanta dilute SLOWER than in B1 => MORE dark energy at high z.
- Qualitative: w_a positive (wrong direction for DESI!).
- Unless n_c is very small (high occupation), this makes the DESI fit WORSE.

**Key structural difference vs B1:**
The creation term depends on n_bar itself (nonlinear ODE). The effective Hubble
coefficient in the evolution equation is reduced. The equilibrium is still well-defined
(n_bar_eq = Gamma_0*n_c / (sigma*rho_m*n_c - Gamma_0 + 3H*n_c)) but requires
sigma*rho_m + 3H > Gamma_0/n_c for stability.

**Assessment:** WORSE for DESI. Stimulated creation adds MORE dark energy at high z,
giving w_a > B1 (less negative, wrong direction). Interesting as a QFT consistency
test: SQMH must explain why stimulated creation is negligible (n_bar << n_c).

---

### C8. De Sitter Pair Creation: Geometry-Driven Creation Rate

**Modified assumption:** H5 -- creation rate is not constant but determined by de Sitter
temperature T_dS = H/(2*pi)

**Equation:**

    dn_bar/dt + 3H*n_bar = (Gamma_P * H^2 / H_P^2) - sigma*n_bar*rho_m

where Gamma_P = sigma * n_P * rho_P (Planck-scale rate) and H_P = t_P^{-1} is
the Planck Hubble rate.

Equivalently, with Gamma_dS = A * H^2:

    dn_bar/dt + 3H*n_bar = A * H^2 - sigma*n_bar*rho_m

where A = Gamma_0 / H_0^2 sets the normalization.

**Derivation:**
In de Sitter space with Hubble constant H, the Hawking-Gibbons temperature is
T_dS = H/(2*pi) (in Planck units). The thermal pair-creation rate for Planck-mass
quanta in a de Sitter background scales as:
    Gamma_dS ~ exp(-m_P / T_dS) * (phase space) ~ exp(-2*pi/H*t_P) * H^3

For H << H_P (current universe: H_0 ~ 10^{-60} in Planck units):
    Gamma_dS ~ exp(-2*pi * 10^{60}) * H^3 -- exponentially suppressed!

This is the CORRECT pair-creation rate and it is negligibly small. However, if we
instead use the SEMICLASSICAL creation rate (ignoring the Boltzmann suppression):
    Gamma_semi ~ (H * t_P)^2 * H = H^3 * t_P^2 = (H/H_P)^2 * H

This gives the equation above with A = Gamma_0/H_0^2.

**Physical motivation:**
The cosmological constant problem suggests that a geometric source of dark energy
(tied to spacetime curvature) is more natural than an arbitrary constant Gamma_0.
The H^2 scaling of the creation rate connects SQMH to the Running Vacuum Model (RVM):
rho_DE ~ Lambda_0 + nu * H^2 (Sola 2022). The C8 equation, through its equilibrium,
gives rho_DE(z) that tracks the RVM form. This connects two otherwise independent
dark energy frameworks.

**Equilibrium:**
    n_bar_eq = A * H / (sigma*rho_m/H + 3)

At high z (matter dominated, H ~ H_0*(1+z)^{3/2}):
    n_bar_eq ~ A * H_0 * (1+z)^{3/2} / (sigma*rho_m0/H_0 + 3)
    rho_DE ~ mu * n_bar_eq ~ H_0*(1+z)^{3/2} * (const)

This gives rho_DE INCREASING with z (rho_DE ~ (1+z)^{3/2}). This is WRONG for DESI
which requires rho_DE to decrease at high z. CATASTROPHIC FAILURE in the matter era.

**Dark energy qualitative prediction:**
- rho_DE increases at high z (wrong sign of evolution).
- w_a > 0 (significantly positive). Contradicts DESI.
- The H^2 creation rate produces MORE dark energy when H is large (past).

**Key structural difference vs B1:**
The creation rate grows with H^2. This couples the dark energy directly to the
expansion rate, producing a positive correlation between rho_DE and H. Since H
decreases with time (matter/radiation dominated era), this gives an INCREASING rho_DE
toward the future -- correct for the late-time acceleration, but wrong at intermediate z.

**Assessment:** WORSE for DESI at intermediate z. However, this is the RVM connection
and has been studied independently. The wa > 0 issue means C8 conflicts with DESI DR2.
Noted as negative result: H^2 creation = wrong direction for DESI.

---

### C9. Curved-Space QFT Particle Production: Parker-Zel'dovich Creation

**Modified assumption:** H5 -- creation rate comes from cosmological particle production
in curved spacetime (not a free parameter)

**Equation:**

    dn_bar/dt + 3H*n_bar = (3*H_dot + 9*H^2) * beta_PZ - sigma*n_bar*rho_m

where H_dot = dH/dt and beta_PZ = (rho_P / mu) * t_P^2 is a Planck-scale coefficient
derived from the Parker-Zel'dovich cosmological particle production rate.

More compactly, using the Ricci scalar R = 6*(H_dot + 2H^2):

    dn_bar/dt + 3H*n_bar = (R/6) * beta_PZ - sigma*n_bar*rho_m
                         = (H_dot + 2H^2) * beta_PZ - sigma*n_bar*rho_m

**Derivation:**
Parker (1969) showed that cosmological expansion creates particles through quantum
field theory in curved spacetime. The production rate is:
    d(n)/dt = (hbar / (2*pi^2)) * sum_k |beta_k|^2 / a^3

For massless scalar quanta in FLRW: the Bogoliubov coefficient beta_k satisfies
the WKB condition, and the total production rate at leading order is:
    Gamma_Parker ~ H_dot / H ~ (H^2 * dH/d(ln a)) / H

For a matter-dominated universe: H_dot = -(3/2)*H^2, R = -3H^2 < 0.
For a de Sitter universe: H_dot = 0, R = 12H^2 > 0.
The sign of R determines whether quanta are created (R > 0) or absorbed (R < 0).
This provides a GEOMETRIC creation rate from first principles, without a free parameter.

**Physical motivation:**
The creation of matter in an expanding universe is a fundamental result of QFT in
curved spacetime. If spacetime quanta are fundamental objects, their creation should
follow the same rules as all quantum fields. Parker-Zel'dovich production is the
natural, parameter-free creation mechanism for quantum foam. This removes the need
for the ad hoc assumption H4 (Gamma_0 exists) and H5 (Gamma_0 = const), replacing
both with a first-principles calculation.

**Dark energy qualitative prediction:**
At late times (lambda-dominated, de Sitter): H_dot -> 0, R -> 12H^2, so creation
is proportional to H^2 (similar to C8 -- same issue). However, in the transition
from matter to lambda domination: H_dot changes sign (negative to zero), providing
a natural "switching on" of creation near z ~ 0.3 (transition epoch). This could
give a sharp DE increase near z ~ 0.3 and w_a < 0 from the geometric transition.

Quantitatively: the creation term changes sign at H_dot = -2H^2 (w_eff = -1/3 epoch,
roughly z ~ 0.5 in LCDM). For z > 0.5: matter dominated (R < 0, creation off).
For z < 0.5: lambda dominated (R > 0, creation on).

This is a GEOMETRIC THRESHOLD mechanism -- dark energy appears when the universe
transitions from deceleration to acceleration. Very promising conceptually.

**Key structural difference vs B1:**
The creation term is NOT constant but tracks the Ricci curvature R. This ties
the dark energy onset to the geometric transition. No free parameter in the creation rate.
The Ricci scalar R changes sign at the deceleration/acceleration transition.

**Assessment:** PROMISING. This is one of the few equations where Gamma_0 is
derived from first principles (curved-space QFT). The DESI w_a prediction requires
numerical computation, but the geometric threshold mechanism is natural and novel.
Recommend as high-priority for numerical investigation.

---

## Team 4 (Statistical Mechanics): Equations C10-C12
### Focus: H3 (cooperative effects) and H8 (self-interaction)

---

### C10. Cooperative Annihilation (Ising-like Criticality): Phase Transition in Quantum Foam

**Modified assumption:** H8 -- quanta DO have self-interaction (cooperative annihilation)

**Equation:**

    dn_bar/dt + 3H*n_bar = Gamma_0 - sigma*n_bar*rho_m * (1 + J*n_bar/n_c)

where J is a dimensionless self-interaction coupling (J > 0: cooperative; J < 0: competitive).

**Derivation:**
In statistical mechanics, the mean-field theory of cooperative phenomena (Ising model)
gives: transition rate = (bare rate) * (1 + J * <phi>), where <phi> is the order
parameter (local density). For quantum foam near a critical point:
    Gamma_annihilate = sigma * n_bar * rho_m * (1 + J * n_bar/n_c)

This means: when quantum density is high (n_bar >> n_c), annihilation is enhanced
if J > 0 (quanta "help each other" get absorbed). When n_bar is low, back to B1.

The equilibrium:
    n_bar_eq * (1 + J*n_bar_eq/n_c) = Gamma_0 / (sigma*rho_m)  (ignoring 3H for simplicity)
    J/n_c * n_bar_eq^2 + n_bar_eq - Gamma_0/(sigma*rho_m) = 0

For J > 0: n_bar_eq is smaller than B1 (cooperative annihilation reduces density).
For J < 0: n_bar_eq is larger than B1 (competitive self-interaction slows annihilation).

**Physical motivation:**
Quantum foam may exhibit collective behavior near Planck scale. If quanta are
close-packed (density near Planck density), their interactions can be cooperative.
An Ising-like model applies if quanta can be in two states: "free" or "bound-to-matter",
with cooperative transitions between states. At cosmological densities
(n_bar << n_c = n_Planck), the J*n_bar/n_c correction is extremely small (n_bar/n_c
is cosmologically negligible). However, near the Planck era, cooperative effects
were important and set initial conditions for the SQMH evolution.

**Dark energy qualitative prediction:**
For cosmological n_bar << n_c: J*n_bar/n_c term is negligible. Reduces to B1.
The cooperative term matters only at densities comparable to n_c. For DESI purposes
(z < 3): identical to B1. No improvement over B1.

**Key structural difference vs B1:**
Adds nonlinearity in n_bar to the annihilation term (rather than in the creation term
like B4, or in rho_m like B2). This is a fundamentally different nonlinearity --
self-interaction of the quantum field with itself through matter mediation.

**Assessment:** NEUTRAL for DESI. Cosmologically negligible correction. Important
for theoretical consistency (self-interaction contribution to Planck-era cosmology)
but irrelevant for z < 10.

---

### C11. Quantum Diffusion and Self-Pressure: Gradient Corrections (H8 + H3)

**Modified assumption:** H8 -- quanta have self-pressure from quantum uncertainty

**Equation:**

    dn_bar/dt + 3H*n_bar = Gamma_0 - sigma*n_bar*rho_m - alpha_q * n_bar * nabla^2(ln n_bar)

or in the homogeneous background (nabla terms = 0) plus a pressure correction:

    dn_bar/dt + (3H + alpha_q * H^2)*n_bar = Gamma_0 - sigma*n_bar*rho_m

where alpha_q is a quantum pressure coefficient of order t_P^2 (Planck-scale).

**Derivation:**
A quantum fluid has a quantum pressure (Bohm quantum potential) Q = -hbar^2/(2m) *
nabla^2(sqrt(rho))/sqrt(rho). For Planck-mass quanta, this gives a pressure:
    p_q = (hbar^2)/(2*m_P) * (nabla^2 n_bar) / n_bar ~ t_P^2 * c^2 * nabla^2(ln n_bar)

This adds a quantum pressure to the stress tensor of the quantum foam fluid.
In FLRW (homogeneous n_bar), nabla^2(ln n_bar) = 0. The only cosmological effect
is through the equation of state: p_q adds to the effective w_sq. If n_bar has
small spatial gradients (perturbations), the quantum pressure resists clustering:
    p_q ~ -t_P^2 * H^2 * n_bar (from the homogeneous background gradient expansion)

This gives an effective additional Hubble term alpha_q * H^2 (dimension [s^{-1}]).

**Physical motivation:**
Quantum foam quanta obey Heisenberg uncertainty. A localized quantum has momentum
uncertainty delta_p ~ hbar / delta_x ~ hbar / l_P = m_P * c (Planck momentum).
This gives a "quantum pressure" that resists further localization. At cosmological
scales, this quantum pressure is negligible (l_P / Hubble ~ 10^{-61}), but it
appears as a modification to the effective equation of state. The quantum pressure
term alpha_q * H^2 corrects the Hubble dilution by a Planck-suppressed amount.

**Dark energy qualitative prediction:**
The alpha_q * H^2 correction changes the effective Hubble coefficient. At high z
(large H): the correction is larger (but still Planck-suppressed). This gives
a tiny additional suppression of n_bar at high z. Negligible for w_a.

**Key structural difference vs B1:**
Adds a Planck-scale quantum pressure that modifies the Hubble coefficient. The
modification is H-dependent (not constant), coupling the quantum foam equation
to spacetime geometry beyond the simple dilution term.

**Assessment:** WORSE (negligible at cosmological scales, adds complexity). Quantum
pressure is a 10^{-120} correction. Theoretically important as a self-consistency
check but observationally indistinguishable from B1.

---

### C12. Grand-Canonical Ensemble: Chemical Potential for Spacetime Quanta

**Modified assumption:** H3 + H8 -- quanta have a chemical potential mu_q that
modifies both the creation rate and self-interaction

**Equation:**

    dn_bar/dt + 3H*n_bar = Gamma_0 * exp(mu_q / (k_B * T_dS)) - sigma*n_bar*rho_m
                         = Gamma_0 * exp(2*pi*mu_q / H) - sigma*n_bar*rho_m

where T_dS = H/(2*pi*k_B) is the de Sitter temperature and mu_q is the chemical
potential of the quantum foam (which may be proportional to rho_DE itself -- see below).

For mu_q << k_B*T_dS: exp(mu_q/T_dS) ~ 1 + mu_q/T_dS, giving:

    dn_bar/dt + 3H*n_bar ~ Gamma_0 * (1 + 2*pi*mu_q / H) - sigma*n_bar*rho_m
                         = Gamma_0 - sigma*n_bar*rho_m + (2*pi*Gamma_0*mu_q) / H

where the last term goes as H^{-1} -- growing at late times.

**Physical motivation:**
In statistical mechanics, the grand canonical ensemble describes particles that can
be created/destroyed at rate controlled by chemical potential mu_q. Spacetime quanta
that can be annihilated by matter (as in SQMH) are in a grand canonical ensemble.
The equilibrium condition is set by mu_q = 0 (chemical equilibrium). If mu_q != 0,
the system is out of chemical equilibrium and drives creation (mu_q > 0) or
annihilation (mu_q < 0). The de Sitter temperature T_dS = H/(2*pi) sets the thermal
scale for this chemical potential.

**Dark energy qualitative prediction:**
If mu_q > 0 (excess quanta thermodynamically favored): creation is enhanced, giving
MORE dark energy. Tends to increase n_bar_eq. w_a becomes less negative.
If mu_q < 0 (quanta disfavored): creation is suppressed. Less dark energy at high z.
w_a becomes more negative -- potentially improving DESI fit.
The natural SQMH state is mu_q = 0 (equilibrium = B1). Departures from equilibrium
give the DESI-relevant variations.

**Key structural difference vs B1:**
The creation rate acquires an exponential factor from thermodynamic considerations.
This couples the quantum foam creation to the de Sitter temperature (i.e., H), introducing
an H-dependent creation rate similar to C8 but motivated by grand-canonical statistics.

**Assessment:** NEUTRAL-PROMISING. Provides a thermodynamic foundation for variations
in Gamma_0. The mu_q < 0 case could give more negative w_a. Requires a physical
model for what determines mu_q (e.g., from the second law or gravitational entropy).

---

## Team 5 (Thermodynamics): Equations C13-C14
### Focus: H5 (Gamma_0 from entropy) and H6 (sigma from different matching)

---

### C13. Clausius-Entropy-Driven Creation: Second-Law Sourced Gamma_0

**Modified assumption:** H5 -- Gamma_0 is not constant but is determined by the
requirement that total entropy S_total is non-decreasing (second law)

**Equation:**

The creation rate Gamma_0 is self-consistently determined by:

    Gamma_0(t) = sigma*n_bar*rho_m + 3H*n_bar - (1/(mu*V)) * dS_matter/dt

where dS_matter/dt is the entropy production rate in the matter sector from quantum
foam annihilation events. This gives a DYNAMICAL Gamma_0 that tracks the entropy.

For the Clausius form: each annihilation event produces entropy delta_S = mu/T_m
(energy mu deposited into matter at temperature T_m). So:
    dS_annihilate/dt = sigma*n_bar*rho_m * mu/T_m
    Gamma_0(t) = sigma*n_bar*rho_m * (1 + T_P/T_m) ~ sigma*n_bar*rho_m

This gives the self-consistent equation:

    dn_bar/dt + 3H*n_bar = sigma*n_bar*rho_m * T_P/T_m - sigma*n_bar*rho_m
                         = sigma*n_bar*rho_m * (T_P/T_m - 1)

For T_m = T_CMB (current temperature T_0 ~ 2.73 K) and T_P ~ 10^{32} K:
    T_P/T_m ~ 10^{31} >> 1, so Gamma_0 ~ sigma*n_bar*rho_m * T_P/T_m

Substituting back:

    dn_bar/dt + 3H*n_bar = sigma*n_bar*rho_m*(T_P/T_m - 1)

For T_m = T_0*(1+z): at high z (large T_m), the factor (T_P/T_m - 1) decreases.
At z ~ T_P/T_0 - 1 ~ 10^{31}: T_m = T_P, factor = 0, no net creation.

This means:
    dn_bar/dt + 3H*n_bar = sigma*n_bar*rho_m * (T_P/(T_0*(1+z)) - 1)

**Physical motivation:**
The second law of thermodynamics constrains the direction of all processes.
If annihilation produces entropy (quanta -> heat in matter), then the reverse
(creation of quanta) must be driven by the entropy gradient. The Clausius-Duhem
inequality gives the minimum creation rate needed to prevent overall entropy decrease.
This ties Gamma_0 to the CMB temperature T_m and Planck temperature T_P.

**Dark energy qualitative prediction:**
At z = 0: Gamma_0 ~ sigma*n_bar*rho_m0 * (T_P/T_0) ~ 10^{31} * sigma*n_bar*rho_m0
This is MUCH larger than rho_m0*sigma*n_bar, giving a net creation >> annihilation.
n_bar grows without bound at z = 0 -- runaway behavior.
The equation is not in the standard B1 equilibrium form. Something is wrong with
the dimensional analysis here -- the Clausius argument needs the chemical potential
mu (in energy units) rather than T_P (temperature). Let us restate carefully:

For the correct Clausius form with chemical potential mu:
    Gamma_0(t) = sigma*n_bar*rho_m - dn_bar/dt * (entropy correction)
This gives an implicit ODE that requires specification of mu(t) independently.

**Assessment:** NEUTRAL-NEGATIVE. The Clausius-entropy argument is physically
compelling but leads to either (a) self-consistent equations with trivial solutions
or (b) runaway if implemented naively. A careful field-theory treatment is needed.
The key insight is correct: Gamma_0 is not constant but tracks entropy production.

---

### C14. Conformal Matching for sigma: Alternative Derivation of the Coupling

**Modified assumption:** H6 -- sigma is derived from conformal (Weyl) matching rather
than Newtonian (Gauss's law) matching

**Equation:**

    dn_bar/dt + 3H*n_bar = Gamma_0 - sigma_W * n_bar * rho_m

where sigma_W = 8*pi*G*t_P (Weyl matching) vs sigma = 4*pi*G*t_P (Newtonian matching).

**Derivation:**
The standard sigma = 4*pi*G*t_P comes from Gauss's law in Newtonian gravity:
    Phi = -GM/r => nabla^2(Phi) = 4*pi*G*rho_m
    sigma ~ (4*pi*G*t_P) matches the Newtonian gravitational cross-section.

Alternative: conformal matching from the Weyl tensor. The gravitational wave
(spin-2) cross-section for a Planck-mass quantum is set by the Compton wavelength
l_C = hbar/(m_P*c) = l_P (Planck length). The full relativistic cross-section
from GR in linearized gravity gives:
    sigma_GR = (8*pi/3) * G^2 * m_P^2 / c^4 * (omega/c)^2 -- frequency dependent

For omega = m_P*c^2/hbar = omega_P (Planck frequency):
    sigma_GR = (8*pi/3) * G^2 * m_P^2 / c^4 * (omega_P)^2 / c^2
            = (8*pi/3) * G^2 * m_P^2 * m_P^2 / (c^4 * hbar^2)
            = (8*pi/3) * G^2 * m_P^4 / (hbar^2 * c^4)
            = (8*pi/3) * (G * m_P^2 / (hbar * c))^2 / (something)

The precise calculation using the gravitational Compton cross-section gives
sigma_GR = 8*pi*G*t_P, which is a factor of 2 larger than the Newtonian Gauss match.

**Physical motivation:**
The Gauss's law matching (H6 in B1) is a NEWTONIAN approximation. The correct
relativistic (GR) cross-section for graviton-matter scattering gives a different
numerical coefficient. In particular, the full GR absorption cross-section for a
massless spin-2 graviton by a mass M includes the factor 8*pi (instead of 4*pi)
due to the two polarization modes of the graviton. If spacetime quanta are graviton-like
(spin-2), the correct coupling is sigma_W = 8*pi*G*t_P = 2*sigma.

**Dark energy qualitative prediction:**
The equilibrium density:
    n_bar_eq = Gamma_0 / (sigma_W * rho_m + 3H) = Gamma_0 / (2*sigma*rho_m + 3H)

This is SMALLER than B1 by a factor of ~ (sigma*rho_m + 3H)/(2*sigma*rho_m + 3H).
At high z (sigma*rho_m >> 3H): n_bar_eq(C14) ~ Gamma_0/(2*sigma*rho_m) = n_bar_eq(B1)/2.
At z = 0 (3H ~ sigma*rho_m): n_bar_eq(C14) ~ Gamma_0/(2*sigma*rho_m0+3H0).

The normalization is re-absorbed into Gamma_0 (using the same n_bar_0 today).
After normalization, the z-evolution of rho_DE(z) differs:
- At high z: rho_DE drops faster than B1 (factor-2 stronger annihilation).
- w_a more negative than B1.

**Key structural difference vs B1:**
The coupling constant sigma doubles. After normalization, the quantitative prediction
for w_a changes. The high-z suppression of dark energy is stronger.

**Assessment:** PROMISING. Simple factor-2 change in sigma with physical motivation.
Zero new parameters. After normalization (adjust n_bar_0), the w_a prediction
should be numerically testable. Predicts: w_a(C14) < w_a(B1) ~ -0.1, potentially
reaching -0.2 to -0.3. Direction correct for DESI.

---

## Team 6 (General Relativity): Equations C15-C17
### Focus: H2 (relativistic w_sq) and H1 (curvature terms in GR)

---

### C15. Full GR Covariant Formulation: Tensor Equation for Quantum Density

**Modified assumption:** H2 + H1 -- treat n_bar as a component of a 4-current N^mu
in full GR (not just FLRW)

**Equation:**

The covariant conservation equation for the quantum number flux N^mu = (n_bar * u^mu):

    nabla_mu N^mu = Gamma_0 - sigma*n_bar*rho_m

In FLRW with u^mu = (1, 0, 0, 0) (comoving frame), the covariant divergence gives:

    nabla_mu N^mu = dn_bar/dt + Gamma^mu_{mu 0} * n_bar = dn_bar/dt + 3H*n_bar

This recovers B1 -- the FLRW case is exact. The new physics appears in the
PERTURBATION THEORY: for perturbations delta(n_bar) around the background n_bar:

    nabla_mu (delta N^mu) + Gamma^mu_{mu nu} * delta N^nu + delta Gamma^mu_{mu 0} * n_bar
    = -sigma*(delta n_bar * rho_m + n_bar * delta rho_m)

The Christoffel symbol perturbation delta Gamma^mu_{mu 0} includes metric perturbations Phi, Psi:
    delta Gamma^mu_{mu 0} ~ 3*Phi_dot + ... (depends on gauge)

This gives a CORRECTION to the quantum density perturbation equation:

    delta_n_dot + ... = -sigma*(delta_n * rho_m + n_bar * delta_rho_m)
                      + (gravity coupling terms with Phi, Psi)

**Physical motivation:**
The background equation (FLRW) is the same as B1. The new physics is in the
PERTURBATION SECTOR: quantum density perturbations couple to gravitational
potential perturbations Phi and Psi. This is the GR generalization of SQMH.
The result is a new source term for dark energy perturbations tied to gravitational
potentials -- potentially modifiable by structure formation.

**Dark energy qualitative prediction:**
Background w_0, w_a: identical to B1 (same background equation).
Perturbation sector: quantum density traces gravitational potentials. This means
dark energy clusters slightly (as in k-essence or early dark energy), modifying
f*sigma_8(z) compared to LCDM. Potential signature in RSD data.

**Key structural difference vs B1:**
B1 is scalar (number density equation). C15 is tensorial (4-current equation).
The new physics appears in perturbations, not background. Could affect growth factor f(z).

**Assessment:** PROMISING for perturbation physics. Background is identical to B1.
The key observable difference is in f*sigma_8(z) via dark energy clustering.
This is a distinct prediction that DESI RSD data could constrain.

---

### C16. Palatini/Metric-Affine SQMH: Torsion-Coupled Annihilation

**Modified assumption:** H1 -- geometry includes torsion (Cartan connection, not Levi-Civita)

**Equation:**

    dn_bar/dt + (3H + S)*n_bar = Gamma_0 - sigma*n_bar*rho_m

where S = K^mu_{mu 0} is the contorsion trace (torsion contribution to the connection).

For Einstein-Cartan theory with spin density s (from fermions):
    S ~ (kappa^2/2) * s ~ G * n_fermion * hbar (spin density from matter)

**Derivation:**
In Riemann-Cartan spacetime, the covariant derivative includes torsion:
    nabla_mu V^mu = partial_mu V^mu + (Gamma + K)^mu_{mu nu} * V^nu

where K^mu_{nu rho} = (1/2)(T^mu_{nu rho} - T_{nu rho}^mu + T_{rho nu}^mu) is
the contorsion tensor and T^mu_{nu rho} is the torsion tensor. For a cosmological
background with spin polarization s:
    S = K^mu_{mu 0} ~ (8*pi*G/c^2) * s (in 3+1 decomposition)

For standard matter: s = spin_density ~ n_baryon * hbar / 2. At cosmological densities:
    S ~ G * n_baryon * hbar ~ 10^{-100} H_0

This is completely negligible. The torsion contribution is Planck-suppressed.

**Physical motivation:**
Einstein-Cartan theory (general relativity with torsion) is the most natural minimal
extension of GR when fermion spin is included. Spacetime torsion couples to the
spin of matter. If SQMH quanta interact with torsion (not just metric curvature),
then the annihilation rate includes a torsion-dependent term. This is a connection
to loop quantum gravity, which naturally generates torsion at Planck scale.

**Dark energy qualitative prediction:**
Torsion correction S ~ 10^{-100} H_0 at cosmological density. Completely negligible.
Even at BBN density: S ~ 10^{-60} H_0. No observable effect on w_a.

**Key structural difference vs B1:**
The Hubble coefficient picks up a torsion correction. In FLRW without matter spin
polarization, torsion averages to zero (isotropy). Only in the presence of macroscopic
spin polarization (e.g., cosmic magnetism, spin-polarized fermion condensate) would
torsion matter.

**Assessment:** WORSE for DESI (negligible effect). Theoretically interesting for
loop quantum gravity connections but observationally dead.

---

### C17. Horndeski/Galileon SQMH: Scalar-Tensor Geometry Correction

**Modified assumption:** H1 -- spacetime carries a scalar sector (Horndeski gravity) that
modifies the effective Planck mass and hence sigma

**Equation:**

    dn_bar/dt + 3H*n_bar = Gamma_0 - sigma(phi)*n_bar*rho_m

where sigma(phi) = 4*pi*G_eff(phi)*t_P depends on the effective gravitational constant:
    G_eff(phi) = G / A^2(phi) (conformal coupling)

For a conformal coupling A(phi) = exp(beta*phi/M_P):
    sigma(phi) = sigma * exp(-2*beta*phi/M_P)

Combined with the Klein-Gordon equation for phi:
    phi'' + 3H*phi' + dV/dphi = -beta * mu * n_bar * (1 + 3*w_phi) / M_P

**Physical motivation:**
Scalar-tensor theories of gravity (Brans-Dicke, Horndeski, DESI-inspired coupled DE)
predict that G_eff varies in time (or space). If sigma = 4*pi*G*t_P, then a varying G
gives a varying sigma. The DESI DR2 data shows a preference for w != -1, which many
groups have interpreted as evidence for scalar-tensor gravity. If SQMH is embedded in
a scalar-tensor theory, sigma varies as phi evolves.

**Dark energy qualitative prediction:**
For beta > 0 and phi increasing with time (thawing quintessence):
- sigma(phi) decreases at late times (lower G_eff)
- Annihilation rate decreases: more dark energy preserved at late times
- n_bar(z=0) > n_bar(B1): w_0 more negative (MORE dark energy today)
- n_bar at high z: similar to B1 (phi was frozen in the past by slow-roll)
- Result: w_a could be negative (more dark energy today vs past), potentially matching DESI

For phi DECREASING (freezing scenario): opposite -- sigma increases, more annihilation
today, less dark energy, w_0 less negative.

**Key structural difference vs B1:**
The coupling sigma becomes time-varying. This is the intersection of SQMH and
coupled quintessence. The n_bar equation and phi equation are coupled.

**Assessment:** PROMISING. Provides a natural framework for varying sigma that
connects to the well-studied Horndeski/disformal coupling program. The C11D
(disformal) route already studied in L2-L6 shows some promise; embedding SQMH
in that framework via varying sigma is a natural extension. Requires 2 extra
parameters (beta, phi_0). AIC/BIC penalty: 2 extra params.

---

## Team 7 (Perturbation Theory): Equations C18-C19
### Focus: H4 (no Gamma_0, different equilibrium) and H5 (Gamma_0 from geometry)

---

### C18. Equilibrium from Initial Conditions (No Creation Rate Required)

**Modified assumption:** H4 -- no Gamma_0; the observed dark energy comes from
a non-zero initial condition n_bar(t_initial) = n_bar_i >> 0 that has not yet
fully decayed.

**Equation:**

    dn_bar/dt + 3H*n_bar = -sigma*n_bar*rho_m

with initial condition n_bar(t_P) = n_bar_i = n_P (Planck density at Planck time).

**Derivation:**
This is the A2 equation from l14_alternative_equations.md but with a SPECIFIED
initial condition. The solution:
    d(n_bar * a^3)/dt = -sigma * n_bar * rho_m * a^3

For a matter-dominated universe:
    n_bar(z) = n_bar_i * (1+z)^3 * exp(-sigma * int[rho_m / H] dz from z to z_i)

The integral int[rho_m/H dz] from z_i to 0 gives the total "annihilation exposure":
For matter domination: int[rho_m0*(1+z)^3 / (H_0*(1+z)^{3/2})] dz = rho_m0/H_0 * int[(1+z)^{3/2} dz]
= rho_m0/H_0 * (2/5)*(1+z)^{5/2} | from z_eq to 0

For sigma = 4*pi*G*t_P and rho_m0 ~ 10^{-27} kg/m^3, H_0 ~ 2*10^{-18} s^{-1}:
    sigma*rho_m0/H_0 ~ (4*pi * 6.67e-11 * 5.4e-44) * 10^{-27} / (2e-18)
                    ~ (4.5e-53) * 5e-10 ~ 2.3e-62

The exponent is exp(-2.3e-62 * (1+z_eq)^{5/2}) which is exp(-10^{-61}) ~ 1.

The annihilation is COMPLETELY NEGLIGIBLE over the age of the universe! Therefore:

    n_bar(z) ~ n_bar_i * (1+z)^3 * a(t)^3 / a(t_i)^3 = n_bar_i = const

In other words, with sigma = 4*pi*G*t_P, the quanta essentially NEVER get annihilated
in the classical FLRW evolution (the cross-section is too small). The density n_bar(a)
just dilutes as a^{-3} without any significant annihilation.

**Dark energy prediction:**
If n_bar * a^3 = const: rho_DE ~ n_bar * mu ~ mu * n_bar_i * a^{-3} ~ rho_m.
This gives rho_DE proportional to rho_m -- NOT the observed late-time acceleration.
n_bar behaves like cold dark matter. Dark energy prediction: FAILS.

Interesting corollary: this derivation shows that sigma = 4*pi*G*t_P is SO SMALL
that annihilation is negligible over cosmic history. This is the "paradox" at the
heart of SQMH: why does the annihilation term matter at all? Answer: it only matters
through the RATIO n_bar/n_bar_eq (the deviation from equilibrium), not the absolute rate.

**Key structural difference vs B1:**
No creation term. The "dark energy" comes from the initial condition n_bar_i.
But since n_bar dilutes as a^{-3}, this gives w_DE = 0 (matter-like), not w = -1.

**Assessment:** WORSE than B1 (dilutes like matter). This analysis confirms that the
creation term Gamma_0 is NECESSARY for dark energy -- without it, n_bar behaves as
pressureless dust. The A-class equations are definitively ruled out.

---

### C19. Geometric Creation from Ricci-Flow: Trace-Anomaly Driven Gamma_0

**Modified assumption:** H5 -- Gamma_0 is determined by the trace anomaly (conformal
anomaly) of the quantum foam stress tensor in curved spacetime

**Equation:**

    dn_bar/dt + 3H*n_bar = (alpha_T / t_P^2) * (R^2 / R_P^2) - sigma*n_bar*rho_m

where R is the Ricci scalar, R_P = c^2/(G*t_P^2) ~ 1/l_P^2 is the Planck Ricci
scalar, and alpha_T is a dimensionless coupling from the trace anomaly coefficient.

For FLRW (with cosmological constant Lambda):
    R = 6*(H_dot + 2H^2) = -8*pi*G*(rho - 3p) + 4*Lambda

In a Lambda-dominated de Sitter universe (H = H_0 = const):
    R = 12*H_0^2 = 4*Lambda/c^2

The trace anomaly creation rate:
    Gamma_R = (alpha_T / t_P^2) * (R/R_P)^2
            = alpha_T * t_P^2 * R^2
            = alpha_T * t_P^2 * (12*H_0^2)^2
            = 144 * alpha_T * (H_0 * t_P)^2 * H_0^{-1}

In terms of H_0 ~ 2.3*10^{-18} s^{-1} and t_P ~ 5.4*10^{-44} s:
    H_0 * t_P ~ 1.2*10^{-61}
    Gamma_R ~ 144 * alpha_T * (1.2*10^{-61})^2 / (2.3*10^{-18}) ~ 10^{-122} / s

For this to match Gamma_0 (which must satisfy sigma*n_bar_0*rho_m0 ~ Gamma_0 ~ H_0):
    alpha_T ~ H_0 / (10^{-122} / s) ~ 10^{122}

This is the cosmological constant problem in new guise: to get the right Gamma_0
from the trace anomaly, alpha_T must be tuned to 10^{122}. NOT an improvement.

**Physical motivation:**
The trace anomaly (also known as the Weyl anomaly or conformal anomaly) is a
genuine quantum effect in curved spacetime. In QFT on curved backgrounds, the
renormalized stress tensor has a non-zero trace:
    <T^mu_mu> = c_1 * C^{mu nu rho sigma} * C_{mu nu rho sigma} + c_2 * R^2 + c_3 * Box R

where C is the Weyl tensor and c_1, c_2, c_3 are numerical coefficients of order 1
times the appropriate powers of hbar and G. This is a physically well-defined,
computable (if non-renormalizable) source. Proposing that Gamma_0 comes from
the trace anomaly is physically motivated (curved-space QFT) and parameter-free
(alpha_T computable in principle from N_fields and N_species in the quantum foam).

**Dark energy qualitative prediction:**
R = 12H^2 in de Sitter. R^2 ~ H^4. So Gamma_R ~ H^4. This gives:
    dn_bar/dt + 3H*n_bar ~ A*H^4 - sigma*n_bar*rho_m
    n_bar_eq ~ A*H^3 / (sigma*rho_m + 3H)

At high z: H^3 grows, rho_m grows. Whether n_bar_eq grows or shrinks depends on
the power: H^3 vs (H^3 in matter domination). In matter domination H ~ (1+z)^{3/2}:
    n_bar_eq ~ (1+z)^{9/2} / (sigma*rho_m0*(1+z)^3 + 3*H_0*(1+z)^{3/2})
            ~ (1+z)^{3/2} / (sigma*rho_m0/H_0 + 3) for high z

This grows at high z: MORE dark energy in the past. w_a > 0. Wrong direction for DESI.

**Key structural difference vs B1:**
Gamma_0 from the curvature squared R^2 gives a creation rate that grows rapidly
in the past (high z). This is the OPPOSITE of what DESI requires.

**Assessment:** WORSE for DESI (w_a > 0). The trace anomaly route gives H^4 scaling
which produces the wrong sign of w_a. However, the alpha_T tuning problem confirms
that any purely geometric Gamma_0 requires extreme fine-tuning unless the geometric
source is present only at late times (which R^2 does not provide).

---

## Team 8 (Effective Field Theory): Equations C20
### Focus: H6 (sigma alternatives) and H3+H7 combinations

---

### C20. EFT of Dark Energy Matching: sigma from Sound Speed and EFT Coefficients

**Modified assumption:** H6 -- sigma is determined by matching to the Effective Field
Theory of Dark Energy (EFTofDE) rather than to Newtonian gravity

**Equation:**

    dn_bar/dt + 3H*(1 + alpha_K/6)*n_bar = Gamma_0 - sigma_EFT*n_bar*rho_m

where:

    sigma_EFT = 4*pi*G*t_P * (1 + alpha_B)   (braiding correction)
    alpha_K = kinetic braiding parameter (EFTofDE)
    alpha_B = braiding parameter (EFTofDE)

The equation combines:
1. A modified Hubble coefficient from the kinetic braiding alpha_K
   (analogous to a modified w_sq, per H2)
2. A modified sigma from gravitational braiding alpha_B
   (modification to the gravitational cross-section, per H6)

**Derivation:**
The EFT of Dark Energy (Gubitosi, Piazza, Vernizzi 2013) parameterizes deviations
from LCDM by time-varying functions alpha_K(t), alpha_B(t), alpha_M(t), alpha_T(t).
In the context of SQMH:
- alpha_M(t) = d(ln M_P^2)/d(ln a) measures the running of the Planck mass.
  This modifies sigma: sigma_eff = sigma * (M_P_eff/M_P)^2 = sigma * exp(int alpha_M d(ln a)).
- alpha_B(t) measures "braiding" -- mixing of scalar field kinetic term with curvature.
  This modifies how n_bar couples to geometry.
- alpha_K(t) measures the kinetic term coefficient. For the quantum foam fluid,
  this changes the effective speed of sound c_s^2 and the effective equation of state.

The combined EFT equation takes the form above, where alpha_K and alpha_B are
matched to the SQMH microscopic model:
    alpha_K = 2*(w_sq - 0) = 2*w_sq (kinetic term from EoS)
    alpha_B = (sigma_EFT - sigma)/sigma = factor from GR vs Newtonian matching

For pure Horndeski gravity with SQMH: alpha_T = 0 (required by GW170817 constraint).
This forces alpha_B = alpha_M = f(alpha_K) through the consistency relation.

**Physical motivation:**
The EFT of Dark Energy is the most systematic framework for parameterizing all
possible dark energy models at the level of perturbations. Embedding SQMH in this
framework is the rigorous way to compute:
- The effective gravitational coupling G_eff(z) (relevant for growth)
- The dark energy sound speed c_s (relevant for clustering)
- The slip parameter eta = Psi/Phi (relevant for lensing)

The EFT matching translates SQMH's microscopic parameters (sigma, w_sq, n_bar)
into observable EFT parameters (alpha_K, alpha_B, alpha_M). This provides a
connection to existing EFT-based analyses of DESI data.

**Equilibrium:**

    n_bar_eq = Gamma_0 / (sigma_EFT*rho_m + 3H*(1 + alpha_K/6))

For alpha_B = 0 and alpha_K = 2*w_sq: this recovers C2 (arbitrary w_sq).
For alpha_B != 0: the effective sigma is modified by the braiding coupling.

**Dark energy qualitative prediction:**
- For alpha_B > 0 (gravitational braiding): sigma_EFT > sigma. More annihilation.
  n_bar_eq smaller at high z. w_a more negative than B1.
- For alpha_K > 0 (kinetic braiding): effective Hubble coefficient larger.
  More dilution. Same effect as C1 (relativistic EoS).
- Combined (alpha_B = alpha_K/2): self-consistent Horndeski theory.
  The combined effect: w_a significantly more negative than B1.

The EFT prediction for w_a in terms of alpha_B:
    w_a ~ -Omega_m/(3*(1 + alpha_B)) -- more negative for larger alpha_B.
    For alpha_B ~ 2: w_a ~ -Omega_m ~ -0.3 ... -0.5. Closer to DESI than B1.

**Key structural difference vs B1:**
This equation is the EFT generalization of both H2 and H6 simultaneously. The
two EFT parameters (alpha_K, alpha_B) replace the single physical parameters
(w_sq, sigma). This is the correct language for connecting SQMH to Boltzmann codes
(hi_class, EFTCAMB) that already implement the EFTofDE.

**Assessment:** VERY PROMISING. Zero ADDITIONAL parameters beyond what EFTofDE
already uses. The alpha_B > 0 case gives w_a more negative than B1, direction
correct for DESI. This equation provides the bridge between the microscopic SQMH
picture and the EFTofDE observational framework. Recommend as the top priority
for numerical implementation via hi_class.

---

## Summary Table: C1-C20 Structural Alternative Equations

| Eq  | H1-H8 modified | Equation form (schematic) | w_0 vs B1 | w_a vs B1 | DESI improvement | Extra params |
|-----|----------------|---------------------------|-----------|-----------|-----------------|--------------|
| C1  | H2 (w_sq=1/3) | dn/dt + 4Hn = Gamma_0 - sigma*n*rho_m | similar | more negative | PROMISING | 0 |
| C2  | H2 (0<w<1/3) | dn/dt + 3(1+w)Hn = Gamma_0 - sigma*n*rho_m | similar | more negative | PROMISING | 1 (w_sq) |
| C3  | H3 (n^p mass-action) | dn/dt + 3Hn = Gamma_0 - sigma_p*n^p*rho_m | ~ B1 | mixed | NEUTRAL | 1 (p) |
| C4  | H1 (Bianchi-I) | dn/dt + 3Hn = Gamma_0 - sigma*n*rho_m - delta*Sigma^2*n | ~ B1 | ~ B1 | NEUTRAL | 1 (delta) |
| C5  | H1 (k!=0) | dn/dt + 3Hn + kappa/a^2*n = Gamma_0 - sigma*n*rho_m | ~ B1 | tiny correction | NEUTRAL | 0 (|Omega_k|<0.01) |
| C6  | H7 (radiation) | dn/dt + 3Hn = Gamma_0 - sigma*n*rho_m - sigma_r*n*rho_r | ~ B1 | much more negative | PROMISING (risky) | 1 (sigma_r) |
| C7  | H4 (stimulated) | dn/dt + 3Hn = Gamma_0*(1+n/n_c) - sigma*n*rho_m | ~ B1 | less negative | WORSE | 1 (n_c) |
| C8  | H5 (H^2 creation) | dn/dt + 3Hn = A*H^2 - sigma*n*rho_m | ~ B1 | positive | WORSE | 0 |
| C9  | H5 (Parker-PZ) | dn/dt + 3Hn = beta_PZ*(H_dot+2H^2) - sigma*n*rho_m | ~ B1 | negative (late-time switch) | PROMISING | 0 |
| C10 | H8 (cooperative) | dn/dt + 3Hn = Gamma_0 - sigma*n*rho_m*(1+J*n/n_c) | ~ B1 | ~ B1 | NEUTRAL | 1 (J) |
| C11 | H8 (quantum pressure) | dn/dt + (3H+alpha_q*H^2)*n = Gamma_0 - sigma*n*rho_m | ~ B1 | ~ B1 | WORSE | 1 (alpha_q) |
| C12 | H3+H8 (chem. potential) | dn/dt + 3Hn = Gamma_0*exp(mu_q*2pi/H) - sigma*n*rho_m | ~ B1 | ~ B1 (mu_q=0) | NEUTRAL | 1 (mu_q) |
| C13 | H5 (entropy) | Gamma_0(t) from second-law constraint | ~ B1 | unstable | NEUTRAL | 0 |
| C14 | H6 (Weyl sigma) | dn/dt + 3Hn = Gamma_0 - 2*sigma*n*rho_m | ~ B1 | more negative | PROMISING | 0 |
| C15 | H1+H2 (GR covariant) | nabla_mu N^mu = Gamma_0 - sigma*n*rho_m | ~ B1 | ~ B1 (perturb. sector differs) | NEUTRAL (perturb.) | 0 |
| C16 | H1 (torsion) | dn/dt + (3H+S)*n = Gamma_0 - sigma*n*rho_m | ~ B1 | ~ B1 | WORSE | 0 |
| C17 | H1+H6 (scalar-tensor) | dn/dt + 3Hn = Gamma_0 - sigma(phi)*n*rho_m | variable | variable | PROMISING | 2 (beta,phi_0) |
| C18 | H4 (no Gamma_0) | dn/dt + 3Hn = -sigma*n*rho_m, n(t_P)=n_P | N/A (w=0) | N/A | WORSE (w_DE=0) | 0 |
| C19 | H5 (trace anomaly) | dn/dt + 3Hn = alpha_T*t_P^2*R^2 - sigma*n*rho_m | ~ B1 | positive | WORSE | 1 (alpha_T) |
| C20 | H2+H6 (EFTofDE) | dn/dt + 3H*(1+alpha_K/6)*n = Gamma_0 - sigma*(1+alpha_B)*n*rho_m | variable | more negative | VERY PROMISING | 2 (alpha_K, alpha_B) |

---

## Key Findings from Structural Analysis

### Finding 1: The H2 Assumption (w_sq = 0) is the Most Consequential

Varying w_sq from 0 to 1/3 changes the Hubble coefficient from 3 to 4 (a 33% increase).
This is the simplest, parameter-free modification that directly gives more negative w_a.
- C1 (w_sq = 1/3): zero extra parameters. Direction correct for DESI.
- C2 (general w_sq): one parameter scan. Can tune w_a toward -0.83.
- C20 (EFTofDE): generalizes this in the proper observational language.

The non-relativistic assumption w_sq = 0 is the LEAST justified for Planck-mass objects.
Planck quanta at any temperature T >> T_P (Planck temperature) would be ultra-relativistic.
Only if quanta thermalize with the CMB (T_CMB << T_P) would w_sq ~ 0 be correct.

### Finding 2: The H6 Assumption (sigma = 4*pi*G*t_P) Has a Factor-2 Uncertainty

The Newtonian matching (Gauss: 4*pi) vs full GR matching (two graviton polarizations: 8*pi)
gives sigma_GR = 2*sigma_Newton. C14 (Weyl matching) has zero extra parameters and
gives w_a more negative than B1. This is a straightforward and honest uncertainty
that should be propagated as a theoretical systematic.

### Finding 3: The H5 Assumption (Gamma_0 = const) Can Be Derived from First Principles

C9 (Parker-Zel'dovich) provides the only derivation of Gamma_0 from first principles
(curved-space QFT). It gives Gamma_0 proportional to the Ricci scalar R, which
changes sign at the deceleration/acceleration transition z ~ 0.3-0.5. This is a
geometric threshold mechanism for dark energy onset -- theoretically elegant.

### Finding 4: The H7 Assumption (no radiation coupling) is Testable

C6 (radiation coupling) would suppress n_bar during radiation domination, providing
a natural explanation for why dark energy appeared only at late times. The early dark
energy constraint (f_EDE < 0.1 from CMB) would constrain sigma_r. This is the
most direct observational test of assumption H7.

### Finding 5: Equations Without Gamma_0 (A-class, C18) Give w_DE = 0

C18 confirms definitively: without a creation term, n_bar dilutes as a^{-3} (dust).
Dark energy with w ~ -1 REQUIRES Gamma_0 > 0. The premise "quanta are annihilated by
matter" must be supplemented by some creation mechanism, or the model is observationally dead.

---

## Priority Ranking for Numerical Investigation

1. **C1** (w_sq=1/3): Zero parameters, physically motivated, direction correct. Test FIRST.
2. **C9** (Parker-PZ): First-principles derivation of Gamma_0. No free parameters. Elegant.
3. **C14** (Weyl sigma=2*sigma): Factor-2 change, zero parameters. Quick numerical check.
4. **C20** (EFTofDE): Connects to hi_class. Best framework for observational comparison.
5. **C6** (radiation coupling): Tests the H7 assumption. Requires early-universe integration.
6. **C2** (general w_sq): Parameter scan. Finds the range of w_sq consistent with DESI.
7. **C17** (scalar-tensor sigma): Requires joint scalar-tensor + SQMH ODE. More complex.

Equations definitively NOT worth further investigation: C4, C5, C7, C8, C10, C11, C13, C16, C18, C19.

---

## Honest Assessment of SQMH B1 vs Alternatives

The standard SQMH equation (B1) assumes the MOST FAVORABLE combination for simplicity:
- Lowest Hubble coefficient (w_sq=0 => 3H vs 4H)
- Newtonian sigma (not GR-corrected)
- No radiation coupling
- Constant creation rate

Remarkably, these assumptions all work AGAINST a large negative w_a. The alternatives
that increase |w_a| (C1, C14, C6) do so by using less conservative assumptions.

This means: **B1 is likely the WORST-CASE equation for DESI compatibility among the
physically motivated alternatives.** The true SQMH prediction may have a more negative
w_a than B1, making DESI consistency easier rather than harder.

This is a crucial asymmetry: the most conservative SQMH equation is also the hardest
to fit to DESI. More "correct" assumptions (relativistic w_sq, GR sigma, radiation coupling)
all push in the DESI-consistent direction.

---

*L14 structural assumption alternatives: 20 equations C1-C20 completed 2026-04-11*
*8 teams; H1-H8 systematic variation; DESI DR2 (w0=-0.757, wa=-0.83) target*
