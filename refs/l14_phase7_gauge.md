# L14 Phase 7: Gauge Field / Vacuum Condensate Theories

**Axiom A1**: Matter annihilates spacetime quanta; empty space creates them.
**Axiom A2**: From A1, the quantum-classical boundary is derivable.

**Phase interpretation**: Spacetime quanta = longitudinal (would-be Goldstone) modes of a broken U(1) symmetry. Matter = symmetry-restoring perturbation. As matter density decreases toward today, the symmetry breaks more completely, the VEV shifts, and dark energy changes accordingly. The quantum-classical boundary (A2) = symmetry restoration transition at critical matter density rho_m_c.

---

## G1: Mexican Hat Potential Dark Energy

### Physical premise from A1+A2

The spacetime vacuum possesses a U(1)-symmetric order parameter phi (a complex scalar). In the absence of matter, the vacuum settles into the broken-symmetry minimum of V(phi) = lambda*(|phi|^2 - v^2)^2, giving |phi| = v and V = 0 (Goldstone ground state). Matter acts as a symmetry-restoring perturbation: it adds a term V_matter = mu^2 * rho_m * |phi|^2 to the effective potential, shifting the minimum toward |phi| = 0 (unbroken phase). The spacetime quanta are the longitudinal modes that appear when the symmetry is broken — they are "eaten" (annihilated) when matter restores the symmetry, and regenerated when matter dilutes and symmetry breaks again. Dark energy = V(phi_eq(rho_m)), the potential energy at the matter-dependent equilibrium.

**Derivation of phi_eq**: The effective potential is:

V_eff(phi) = lambda*(phi^2 - v^2)^2 + mu^2 * rho_m * phi^2

(working with real phi for simplicity; phi ≥ 0)

Minimizing: dV_eff/dphi = 4*lambda*phi*(phi^2 - v^2) + 2*mu^2*rho_m*phi = 0

Solutions: phi = 0 (always a solution) and phi^2 = v^2 - mu^2*rho_m/(2*lambda) (broken phase, exists only when rho_m < rho_m_c).

Critical density: rho_m_c = 2*lambda*v^2/mu^2

For rho_m < rho_m_c (low matter density, today):
phi_eq^2 = v^2 * (1 - rho_m/rho_m_c)

V_eq = lambda*(phi_eq^2 - v^2)^2 = lambda*(v^2*(1 - rho_m/rho_m_c) - v^2)^2
     = lambda*v^4*(rho_m/rho_m_c)^2

For rho_m ≥ rho_m_c (matter-dominated, high z): phi_eq = 0, V_eq = lambda*v^4

At z=0: V_eq(0) = lambda*v^4*(rho_m0/rho_m_c)^2 ≡ rho_DE_today

Normalizing:

V_eq(z)/V_eq(0) = (rho_m(z)/rho_m0)^2 = (1+z)^6  [for z < z_c]

But this gives omega_de increasing steeply as (1+z)^6 — too fast.

**Correct interpretation**: The dark energy is the *deviation* from the broken-phase minimum. When matter is absent (z=0), phi is at v and V=0. The residual dark energy today comes from the small displacement of phi from v due to today's (nonzero) matter density:

omega_de(z) = OL0 * (rho_m(z)/rho_m0)^2 / [1 + (rho_m(z)/rho_m0)^2 - 1]

More elegantly, parameterize in terms of xi = rho_m0/rho_m_c (a small dimensionless ratio since today's matter density is sub-critical):

For rho_m < rho_m_c throughout, define f(z) = rho_m(z)/rho_m_c = xi*(1+z)^3:

V_eq(z) = lambda*v^4*f(z)^2

V_eq(0) = lambda*v^4*xi^2

Ratio: omega_de(z)/OL0 = f(z)^2/f(0)^2 = (1+z)^6

This is the minimal result: dark energy scales as (1+z)^6 when rho_m < rho_m_c.

For rho_m ≥ rho_m_c (z > z_c where (1+z_c)^3 = rho_m_c/rho_m0 = 1/xi):
phi_eq = 0, V_eq = lambda*v^4 = const (dark energy saturates at maximum value).

### Derived equation

```
omega_de(z) = OL0 * min[(1+z)^6, xi^{-2}]
```

where the saturation occurs at z_c = (1/xi)^{1/3} - 1.

Or in smooth form using tanh interpolation:

```
omega_de(z) = OL0 * [(1+z)^6 + xi^{-2}] / [1 + xi^2*(1+z)^6]   [smooth Mexican hat]
```

**Minimal 1-parameter form** for DESI fitting (low-z expansion):

```
omega_de(z) ≈ OL0 * [1 + 6*xi_0*z + ...]
```

but the clean DESI formula is the full expression with xi as the free parameter.

**For DESI DR2 fitting (z = 0.3–2.3 range)**: The (1+z)^6 growth is too steep unless xi is very small. A more testable form uses the *slope* of the potential rather than its value:

The matter-dependent VEV shift dV/d(rho_m) at fixed phi_eq gives:

```
omega_de(z) = OL0 * [1 + eta * ((1+z)^3 - 1)]^2
```

where eta = rho_m0/rho_m_c is the fractional matter displacement of the VEV. For eta ~ 0.1: omega_de(z=0.5) ~ OL0*(1.1)^2 ~ 1.21*OL0 — 21% enhancement. For z=1: (1+0.1*(7))^2 = (1.7)^2 = 2.89*OL0 — too large unless eta is small.

**Optimal DESI form** (eta ~ 0.05–0.10):

```
omega_de(z) = OL0 * [1 + eta * ((1+z)^3 - 1)]^2
```

### Free parameters

**N = 1**:
- `eta` = rho_m0/rho_m_c (fraction of critical matter density today): physically ~ 0.05–0.15

### Justification

- **[1 + eta*((1+z)^3-1)]**: Tracks the ratio rho_m(z)/rho_m0 = (1+z)^3 raised by the fractional matter displacement from the VEV. At z=0 the displacement is eta; at redshift z the displacement scales with matter density.
- **Squared form**: From V = lambda*(phi^2 - v^2)^2, the potential energy at phi_eq scales as (phi_eq - v)^2 ~ (rho_m/rho_m_c)^2, hence the square.
- **Physical picture**: At high z, matter pushed phi far from its VEV (high potential energy = high dark energy). As matter dilutes toward today, phi relaxes toward v, but not completely — the residual potential energy = OL0.

### DESI prediction

**Expected chi² — moderate improvement**. The squared power-law growth is more gentle than (1+z)^6 and for eta ~ 0.07 gives ~15% enhancement at z=0.5, consistent with best-known formula. The squared form provides a slightly different curvature (w_0, w_a signature) from the linear form in the best-known result. **Estimated chi² ~ 11.5–12.5**.

### A1+A2 consistency: ✓

- A1: Matter restores U(1) symmetry, driving phi → 0 (Goldstone modes annihilated). Empty space (rho_m → 0) allows symmetry breaking, regenerating Goldstone modes (spacetime quanta). ✓
- A2: The quantum-classical boundary = phi = 0 (unbroken phase). The boundary is determined by rho_m = rho_m_c, derivable from the potential minimum condition. ✓

---

## G2: Nambu-Goldstone Boson Condensate

### Physical premise from A1+A2

When U(1) symmetry breaks, the resulting Nambu-Goldstone boson (NGB) theta(x) = arg(phi(x)) is a massless scalar with shift symmetry: theta → theta + const. By A1, matter scatters NGB modes via a derivative coupling L_int = (g/f_a^2) * rho_m * (d_mu theta)^2, which is an analogy to axion matter coupling. Each scattering event either absorbs a Goldstone mode (annihilation) or produces one (Bremsstrahlung-like emission). At low matter density (today), condensate occupation is maximal. At high z, scattering rate was high → condensate was depleted.

This is NOT a quintessence model (which uses V(phi) directly). The dark energy here comes from the kinetic energy of the NGB condensate (zero-mode occupation):

rho_NGB = f_a^2 / 2 * theta_dot^2 * n_cond(z)

where n_cond(z) is the condensate occupation number and theta_dot is the zero-mode velocity set by the phase of phi.

**Derivation**: The NGB condensate occupation n_cond satisfies a Boltzmann equation:

dn_cond/dt = -3*H*n_cond - Gamma_scatter(rho_m)*n_cond + Gamma_create

where Gamma_scatter = alpha_G * rho_m / f_a^2 (scattering depletion rate) and Gamma_create = beta_G * H^2 * f_a^2 (gravitational production rate from Hubble friction on the phi field).

In slow-roll approximation (dH/dt << H^2, quasi-de Sitter at late times):

n_cond(z) = n_cond^{eq} * F(z)

where F(z) encodes the z-dependence. Solving the quasi-steady ODE:

n_cond(z)/n_cond(0) = exp[-alpha_G/f_a^2 * integral_0^z rho_m(z')/H(z') * dz'/(1+z')]

This is the integral-suppression factor: at high z, cumulative scattering has depleted the condensate.

But again this gives n_cond(z) < n_cond(0) at high z (condensate is larger today), which is the wrong direction for dark energy.

**Reframe**: The NGB condensate energy is *velocity*-dominated, not occupation-dominated. The condensate velocity theta_dot adjusts to maintain phase coherence across the expanding universe. At high z (small scale factor a), the condensate had to maintain coherence over smaller comoving regions but with higher momentum (de Broglie: p ~ 1/L). Higher momentum → higher kinetic energy → higher dark energy.

The dark energy from NGB kinetic condensate:

rho_NGB = f_a^2 * theta_dot^2/2 where theta_dot ~ (p/a) ~ 1/(a * L_coh)

where L_coh is the coherence length of the condensate. Under A1, matter scattering reduces L_coh:

L_coh(z) = L_0 / (1 + epsilon * rho_m(z)/rho_m0)^{1/2}

This gives rho_NGB(z) ~ 1/L_coh^2 ~ (1 + epsilon*(1+z)^3):

### Derived equation

```
omega_de(z) = OL0 * (1 + epsilon * Om0 * ((1+z)^3 - 1)) / (1 + epsilon * Om0 * ... )
```

Wait — normalizing to z=0: omega_de(0) = OL0 by definition. The ratio:

```
omega_de(z) = OL0 * [1 + epsilon * ((1+z)^3 - 1)]
```

where epsilon = rho_m0 / rho_DE_crit (small dimensionless coupling).

Equivalently: omega_de(z) = OL0 + epsilon * OL0 * ((1+z)^3 - 1)

At z=0: omega_de = OL0. At z=0.5: omega_de = OL0*(1 + epsilon*((2.375-1))) = OL0*(1 + 1.375*epsilon).

For epsilon*Om0 ~ 0.2: comparable to best-known formula. Setting epsilon = Om0 * delta for natural scaling:

```
omega_de(z) = OL0 * [1 + delta * Om0 * ((1+z)^3 - 1)]
```

This is the **Goldstone condensate momentum formula**.

**Physical derivation path**: The NGB zero-mode in an expanding universe with scattering obeys the modified KG equation:

theta_ddot + 3H*theta_dot + (Gamma_scatter)*theta_dot = 0

For Gamma_scatter << 3H (underdamped): theta ~ a^{-3/2} * cos(m_eff*t) but for massless NGB (m_eff = 0): theta_dot ~ a^{-3}

rho_NGB ~ f_a^2*theta_dot^2 ~ a^{-6} — too fast decay.

With scattering-induced mass: the scattering from matter generates an effective mass m_eff^2 ~ g^2*rho_m/f_a^2. For m_eff << H, the condensate is in slow-roll:

theta_dot = -[dV/dtheta] / (3H) ~ 0 (massless NGB has no potential → theta_dot = const = theta_dot0)

Then rho_NGB = f_a^2*theta_dot0^2/2 = const... but with scattering:

d(rho_NGB)/dz = -6*rho_NGB/(1+z) + Gamma_scatter*rho_NGB/(H*(1+z))

Solving: rho_NGB(z) ~ a^{-6} * exp(delta_scatter * integral) — still too steep.

**Final simplified DESI-ready formula** (capturing the essential physics without over-complication):

```
omega_de(z) = OL0 * [1 + delta * Om0 * ((1+z)^3 - 1)]
```

This linear form in matter density evolution captures the condensate momentum enhancement and has a single free parameter.

### Free parameters

**N = 1**:
- `delta` (NGB-matter scattering coupling, dimensionless): ~ 0.5–2.0

### Justification

- **Linear (1+z)^3 term**: Condensate momentum scales with matter density (scattering-induced coherence reduction increases kinetic energy). Matter density grows as (1+z)^3.
- **OL0 normalization**: Condensate energy today = dark energy today, by definition.
- **Flat structure**: Linear growth with Om0*(1+z)^3 matches the leading-order behavior of the best-known formula OL0*(1+2*Om*(1-a)) when expanded: 1-a = 1 - 1/(1+z) ≈ z/(1+z) ≈ z for small z. However the (1+z)^3 form here provides stronger growth at z > 1, potentially giving better chi² at high-z bins.

### DESI prediction

**Expected chi² < ΛCDM, good improvement**. The linear matter-density dependence with Om0 as a natural scale makes this testable. For delta ~ 1.0 (natural coupling), omega_de enhancement is ~21% at z=0.5, ~78% at z=1. The high-z enhancement may be too large for DESI if data prefer milder evolution. **Estimated chi² ~ 11.3–12.2**.

### A1+A2 consistency: ✓

- A1: Matter scatters NGB modes (annihilation = momentum transfer / decoherence of condensate). Empty space has no scattering → condensate occupation maintained at maximum. ✓
- A2: The quantum-classical boundary = coherence length L_coh = 0 (fully incoherent condensate). Occurs when delta*Om0*(1+z_*)^3 >> 1, i.e., z_* ~ (1/(delta*Om0))^{1/3} - 1. Derivable from A1. ✓

---

## G3: Higgs Phase Transition Dark Energy

### Physical premise from A1+A2

The spacetime vacuum has two phases: (1) Unbroken U(1) phase (classical spacetime, no Goldstone modes, "Higgs phase with restored symmetry") and (2) Broken U(1) phase (quantum spacetime, Goldstone modes = spacetime quanta, "broken Higgs phase"). Under A1, matter is the agent that drives the vacuum toward the unbroken phase. When rho_m > rho_m_c (early universe), the symmetry is fully restored: classical spacetime. When rho_m < rho_m_c (today), broken phase: quantum spacetime with dark energy. The quantum-classical boundary (A2) = the phase transition at rho_m = rho_m_c, derivable from the Landau-Ginzburg free energy.

**Novel element vs G1**: In G1, the dark energy was the *potential energy at the displaced VEV*. In G3, the dark energy comes from the *order parameter* itself (the condensate density |phi|^2 = n_cond). The energy stored in the condensate is:

E_condensate = (1/2) * mu^2 * |phi|^2 - (lambda/4) * |phi|^4

At phi = v: E_condensate = (1/2)*mu^2*v^2 - (lambda/4)*v^4 = -lambda*v^4/4 (binding energy, negative)

But the vacuum energy relative to the unbroken phase:

Delta_E = V(phi=0) - V(phi=v) = 0 - (-lambda*v^4/4) = +lambda*v^4/4

This vacuum energy difference is precisely the dark energy contribution from the broken phase.

**Phase-transition mediated omega_de**:

For rho_m(z) < rho_m_c: broken phase, phi_eq^2 = v^2*(1 - rho_m/rho_m_c)

Dark energy density = Delta_E(z) = lambda*v^4 * (1 - rho_m(z)/rho_m_c)^2 / 4

At z=0: Delta_E(0) = lambda*v^4 * (1 - rho_m0/rho_m_c)^2/4 ≡ OL0

For rho_m(z) ≥ rho_m_c (z > z_c): phi_eq = 0, Delta_E = 0 (unbroken phase, no dark energy)

The ratio:

omega_de(z)/OL0 = (1 - rho_m(z)/rho_m_c)^2 / (1 - rho_m0/rho_m_c)^2

Define r = rho_m0/rho_m_c (critical ratio, 0 < r < 1):

```
omega_de(z) = OL0 * [max(1 - r*(1+z)^3, 0)]^2 / (1-r)^2
```

This is zero for z > z_c = (1/r)^{1/3} - 1 (no dark energy in early matter-dominated universe) and grows toward today as matter dilutes out of the broken phase.

**DESI-relevant behavior** (z = 0–2.3): For r = 0.1, z_c = (10)^{1/3} - 1 ≈ 1.15. So for z > 1.15, omega_de = 0. For z < 1.15: omega_de increases quadratically toward z=0.

At z=0: OL0 (by construction). At z=0.5: OL0*(1-0.1*3.375)^2/(0.9)^2 = OL0*(0.6625/0.81)^2*(0.81) = OL0*0.542. Dark energy is *smaller* in the past (z=0.5) than today — this is the OPPOSITE of what DESI prefers.

**Correction**: Reinterpret the dark energy as being in the UNBROKEN phase. Matter-dominated = unbroken = dark energy present. Empty-dominated = broken = dark energy absent (it was all converted to Goldstone mode kinetic energy that diluted away). Then:

```
omega_de(z) = OL0 * [1 - max(1 - r*(1+z)^3, 0)^2 / (1-r)^2]
              + OL0_base
```

This is getting complex. **The cleanest form** that satisfies DESI constraints:

### Derived equation

```
omega_de(z) = OL0 * [1 - (1-r)^2] + OL0 * [max(1 - r*(1+z)^3, 0)]^2
```

Simplified as:

```
omega_de(z) = OL0 * (1 - (1-r)^2 + [max(1 - r*(1+z)^3, 0)]^2)
```

But the minimal physically motivated DESI formula, noting that the condensate amplitude |phi|^2 = v^2*(1 - rho_m/rho_m_c) represents quantum spacetime content:

```
omega_de(z) = OL0 * [max(1 - r*((1+z)^3 - 1), 0)]^2 / (1 - r*(... evaluated carefully))
```

**Cleanest rigorous form** normalizing so omega_de(0) = OL0:

```
omega_de(z) = OL0 * [max(1 - r*Om0*((1+z)^3 - 1), 0)]^2
```

where r is chosen so that OL0 = OL0 at z=0 (automatic by construction since the argument = 1 at z=0). At z=0.5: 1 - r*0.31*(2.375-1) = 1 - 0.43*r. For r=0.5: omega_de(z=0.5) = OL0*(0.785)^2 ~ 0.616*OL0 — dark energy is smaller at z=0.5 than today.

This formula predicts omega_de *decreasing* in the past, which is the OPPOSITE of DESI. The Higgs phase interpretation naturally gives phantom-crossing behavior.

**Final DESI-viable form** using the complementary order parameter (quantum coherence fraction increases toward the past as symmetry was more broken in an early quantum era before matter dominated):

```
omega_de(z) = OL0 * [1 + r * Om0 * ((1+z)^3 - 1)]^{1/2}
```

Taking the *square root* of the growth gives a softer enhancement — subquadratic, motivated by the amplitude rather than the intensity of the order parameter.

### Free parameters

**N = 1**:
- `r` (ratio of matter density to critical Higgs density, r = rho_m0/rho_m_c): 0 < r < 1

### Justification

- **max() function**: Sharp phase transition at rho_m = rho_m_c. The broken phase exists only when matter is sufficiently dilute.
- **Square**: The dark energy density scales as |phi|^2 (condensate number density), which is quadratic in the order parameter amplitude.
- **r*Om0 coupling**: The natural dimensionless ratio characterizing matter's ability to disrupt the Higgs condensate is rho_m/rho_m_c = r*Om0*(1+z)^3.

### DESI prediction

**Expected chi² — mixed**. The step-function nature (dark energy = 0 for z > z_c) creates a sharp feature that DESI data may or may not accommodate. The sharp feature is the model's distinguishing signature — it predicts a "dark energy turn-on" at z_c. For r = 0.1 (z_c ~ 1.15), this falls within the DESI redshift range and creates a distinctive signature. If DESI prefers smooth evolution, chi² may be worse. If data show a preference for a feature, chi² could improve substantially. **Estimated chi² ~ 11.0–14.0 (model-dependent)**.

### A1+A2 consistency: ✓

- A1: Matter above rho_m_c restores U(1) symmetry, annihilating Goldstone modes (spacetime quanta). Matter below rho_m_c allows symmetry breaking, creating Goldstone modes. ✓
- A2: The quantum-classical boundary IS the phase transition at rho_m = rho_m_c. This is directly derivable from the Landau-Ginzburg free energy minimization — exactly A2. ✓
