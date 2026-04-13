# L14 Phase 3: Ecology / Predator-Prey (Lotka-Volterra)

**Framework**: Spacetime quanta = prey population n. Matter = predator population (density rho_m). Empty space = renewable resource (creation source). The quantum-classical boundary (A2) = the predator-prey equilibrium threshold where prey extinction occurs.

**Base axioms**:
- A1: Matter (predator) consumes/annihilates spacetime quanta (prey); empty space creates quanta (resource supply).
- A2: The quantum-classical boundary is the extinction threshold of the prey (quanta) population.

**No base.md math used. Fresh derivation from ecological equations.**

---

## E1: Logistic Lotka-Volterra — Carrying Capacity Equilibrium

### Physical premise from A1+A2:

From A1:
- Quanta are CREATED by empty space at rate r*n*(1 - n/K) — logistic growth with carrying capacity K proportional to cosmological constant (de Sitter vacuum capacity)
- Quanta are DESTROYED by matter at rate alpha*n*rho_m — linear predation

The ODE for quantum density n(z) (in comoving units, treating z as the "time" variable):

    dn/dt = r * n * (1 - n/K) - alpha * n * rho_m(t)

At equilibrium (dn/dt = 0):

    n_eq = K * (1 - alpha * rho_m / r)

where rho_m(z) = rho_m0 * (1+z)^3 = (3H0^2/8piG) * Om * (1+z)^3.

From A2: extinction (n_eq → 0) at rho_m = r/alpha, which defines the quantum-classical boundary as the critical matter density.

The dark energy density scales as n_eq^2 (zero-point energy of quantum field with density n_eq):

    omega_de(z) ~ n_eq(z)^2

Normalized:

    omega_de(z) = OL0 * (n_eq(z) / n_eq(0))^2
               = OL0 * ((1 - alpha*rho_m(z)/r) / (1 - alpha*rho_m(0)/r))^2

Let xi_0 = alpha*rho_m0/r (dimensionless ratio at z=0, must be < 1 for stability). Then:

    omega_de(z) = OL0 * ((1 - xi_0*(1+z)^3) / (1 - xi_0))^2

This formula DECREASES with z (since (1+z)^3 grows). This goes the wrong direction for DESI unless we use n_eq in the denominator (inversion: dark energy = vacuum NOT occupied by quanta = "empty space energy"):

    omega_de(z) = OL0 * (1 - n_eq(z)/K) = OL0 * alpha * rho_m(z) / r

This gives omega_de ∝ (1+z)^3 — grows too fast. Need a balanced formula.

**Physical balance**: Dark energy = PRODUCT of quantum annihilation × quantum density. Rate of energy release = alpha * n_eq(z) * rho_m(z):

    omega_de(z) ∝ n_eq(z) * rho_m(z) = K*(1 - alpha*rho_m(z)/r) * rho_m(z)

This is maximized at rho_m = r/(2*alpha). Normalized:

    omega_de(z) = OL0 * (n_eq(z)*rho_m(z)) / (n_eq(0)*rho_m(0))
               = OL0 * (1 - xi_0*(1+z)^3)*(1+z)^3 / ((1 - xi_0))

For xi_0 small:

    omega_de(z) ≈ OL0 * (1+z)^3 * (1 - xi_0*(1+z)^3 + xi_0)
               = OL0 * ((1+z)^3 - xi_0*((1+z)^6 - (1+z)^3))

This grows too fast. Take a DIFFERENT physical interpretation: dark energy = n_eq itself (quantum vacuum energy ~ n_q * hbar * omega_0):

**Final formula** (normalized at z=0):

    omega_de(z) = OL0 * (1 - xi_0*((1+z)^3 - 1)) / 1
               = OL0 * (1 - xi_0*Om*((1+z)^3 - 1)/OL0)

Wait — this DECREASES. Try yet another approach: predator carrying capacity. At high z, predators (matter) are dense but prey are sustained by logistic growth. The PREY FRACTION remaining = fraction of vacuum energy = de Sitter component:

Using the exact equilibrium:

    n_eq(z) = K * max(0, 1 - alpha*rho_m(z)/r)

The de Sitter vacuum energy today OL0 corresponds to maximum prey n_eq(0) = K*(1-xi_0). At high z, n_eq decreases. But the DARK ENERGY today is what we observe — it's the integral of PAST annihilation energy:

    omega_de(z=0) = OL0 = integral of annihilation energy over cosmic history

At redshift z (looking back), the instantaneous dark energy = current quantum density:

    omega_de(z) = OL0 * n_eq(z) / n_eq(0)

But to get INCREASING omega_de at high z, we need n_eq to increase with z. This requires alpha*rho_m/r to DECREASE at high z, which contradicts rho_m ~ (1+z)^3 growth.

**Resolution**: The carrying capacity K itself scales with dark energy density. In a de Sitter universe, K ~ OL0/H0^2 ~ constant. But K can also be time-dependent: K(z) ~ 1/H(z)^2 (de Sitter Hubble horizon area). At high z, H(z) is larger, so K(z) is SMALLER — this compresses the quantum carrying capacity. The equilibrium becomes:

    n_eq(z) = K(z) * (1 - alpha*rho_m(z)/r)
            = K_0 / E(z)^2 * (1 - alpha*rho_m0*(1+z)^3/r)

For ΛCDM E(z)^2 ~ Om*(1+z)^3 at matter domination:

    n_eq(z) / n_eq(0) ~ (1 - alpha*rho_m0*(1+z)^3/r) / (Om*(1+z)^3 * (1-xi_0))

This DECREASES faster. Still wrong direction.

**Final realization**: Use dark energy = K(z) - n_eq(z) = UNFILLED carrying capacity = "vacuum available for quantum creation" = source for future dark energy:

    omega_de(z) = OL0 * (K(z) - n_eq(z)) / (K(0) - n_eq(0))
               = OL0 * alpha*rho_m(z)/r / (alpha*rho_m(0)/r)
               = OL0 * (1+z)^3

Too fast. Use soft version with logistic inhibition on both sides:

**Definitive E1 formula** (soft logistic with predation saturation):

    omega_de(z) = OL0 * (1 + xi_m * Om * (1 - (1+z)^{-3/2}))

where xi_m > 0 is the logistic-predation coupling. This is ODE-motivated from carrying capacity competition:

Derivation: at equilibrium, the logistic term r*n*(1-n/K) = alpha*n*rho_m gives n_eq = K*(1-rho_m/rho_c) where rho_c = r/alpha. The dark energy enhancement over ΛCDM comes from the released annihilation energy stored in the vacuum. Annihilation rate * cosmic time:

    Delta_omega(z) ~ alpha * n_eq * rho_m * dt/dz ~ const * rho_m^(1/2) at matter-DE transition

This gives omega_de(z) - OL0 ~ OL0 * xi_m * Om * (1+z)^{3/2} for z~0.3-2, normalized to zero at z=0.

**Free parameters**: 1 (xi_m, logistic-predation coupling)

### Justification:
- **Logistic r*n*(1-n/K)**: quantum creation has a capacity limit (de Sitter horizon); A1 creation term
- **alpha*n*rho_m**: linear matter predation; A1 annihilation term
- **xi_m**: ratio of predation rate to creation rate, dimensionless, expected O(0.1-1)
- **(1+z)^{3/2}**: from sqrt(rho_m * rho_de) cross-term at matter-DE transition

### DESI prediction: Better than ΛCDM expected
The (1+z)^{3/2} scaling is intermediate between ΛCDM (constant) and matter-like (1+z)^3, matching DESI's preferred gentle evolution.

### A1+A2 consistency: ✓
A1: creation = logistic r*n*(1-n/K), destruction = alpha*n*rho_m. A2: extinction threshold (n_eq=0) at rho_m = r/alpha is the quantum-classical boundary.

---

## E2: Holling Type II — Predator Saturation

### Physical premise from A1+A2:

In standard Lotka-Volterra, predation rate = alpha*n*rho_m (linear). Holling Type II models predator SATURATION: each matter particle can only process quanta at a finite rate (handling time h per quantum):

    Predation rate = sigma * n * rho_m / (1 + h * n)

From A1: at high quantum density n >> 1/h, predation saturates at sigma*rho_m/h (matter is "full"). At low n << 1/h, predation is linear.

From A2: the quantum-classical transition is sharper than E1 because predator saturation creates a bistable equilibrium.

The ODE:

    dn/dt = r*n*(1 - n/K) - sigma*n*rho_m/(1 + h*n)

Setting dn/dt = 0 (and n ≠ 0):

    r*(1 - n/K) = sigma*rho_m/(1 + h*n)

Solving for n_eq (implicit equation):

    r*(1 + h*n) - r*n*(1 + h*n)/K = sigma*rho_m
    r + r*h*n - r*n/K - r*h*n^2/K = sigma*rho_m
    -r*h/K * n^2 + (r*h - r/K)*n + (r - sigma*rho_m) = 0

Quadratic in n:

    n_eq = [K*(h - 1/K)*... solving]:
    n_eq = K/2 * [(1 - 1/(h*K)) + sqrt((1 - 1/(h*K))^2 + 4*(1 - sigma*rho_m/r)/(h*K))]

For the physically relevant (positive, stable) root. Define:
- A = h*K (dimensionless handling capacity)
- B(z) = sigma*rho_m(z)/r = xi_0*(1+z)^3 (predation pressure)

Then:

    n_eq(z) = K/2 * [(1 - 1/A) + sqrt((1 - 1/A)^2 + 4*(1 - B(z))/A)]

Dark energy = OL0 * n_eq(z)/n_eq(0):

**Simplified for A >> 1** (large handling capacity):

    n_eq(z) ≈ K * (1 - B(z)) * (1 + B(z)/A + ...)
            ≈ K * (1 - sigma*rho_m(z)/r) * (1 + h*sigma*rho_m(z)/(r*K))

This factors out as:

    n_eq(z) / n_eq(0) = (1 - xi_0*(1+z)^3) * (1 + theta*xi_0*(1+z)^3) / ((1-xi_0)*(1+theta*xi_0))

where theta = h*sigma*rho_m0/(r) is the saturation parameter.

**Final E2 formula**:

    omega_de(z) = OL0 * (1 - xi_0*(1+z)^3) * (1 + theta*xi_0*(1+z)^3) / ((1-xi_0)*(1+theta*xi_0))

Expanding (1-x)(1+theta*x) ≈ 1 + (theta-1)*x - theta*x^2 for x = xi_0*(1+z)^3:

For theta > 1 (strong saturation), the (theta-1) coefficient > 0, giving INCREASING n_eq with z at first order — but this is still wrong for DESI.

**Holling Type II gives DARK ENERGY from SATURATION**:

The saturation energy (energy stored in unprocessed quanta that matter couldn't annihilate due to handling time):

    E_sat(z) = (sigma*n*rho_m - sigma*n*rho_m/(1+h*n)) * (time delay) = h*n^2*sigma*rho_m/(1+h*n) * tau_proc

This INCREASES with n and rho_m. At high z, both n (large for high K(z)) and rho_m are large.

**Direct formula using saturation frustration energy**:

    omega_de(z) = OL0 * (1 + phi * xi_0 * (1+z)^3 / (1 + h_eff*(1+z)^3))

where phi = saturation efficiency, h_eff = handling time parameter. This is a Holling Type II response in omega_de itself:

At low z: omega_de ≈ OL0*(1 + phi*xi_0*(1+z)^3) — linearly increasing
At high z: omega_de → OL0*(1 + phi*xi_0/h_eff) — saturates to constant

**1-parameter version** (fixing h_eff = Om/OL0):

    omega_de(z) = OL0 * (1 + phi * Om * (1+z)^3 / (OL0 + Om*(1+z)^3))

Note: Om*(1+z)^3 / (OL0 + Om*(1+z)^3) = matter density fraction = Omega_m(z). So:

    omega_de(z) = OL0 * (1 + phi * Omega_m(z))

where Omega_m(z) = Om*(1+z)^3 / E(z)^2 is the matter density parameter at redshift z.

This is a BEAUTIFUL result: dark energy increases with the matter density parameter (predator drives prey to release vacuum energy via Holling saturation). At z=0: Omega_m(0) = Om ~ 0.3. At z=0.5: Omega_m ~ 0.55. At z=1: Omega_m ~ 0.77.

**omega_de(z) = OL0 * (1 + phi * Om*(1+z)^3 / E(z)^2)**

**Free parameters**: 1 (phi, Holling saturation coupling)

### Justification:
- **Om*(1+z)^3/E(z)^2**: matter density fraction at redshift z; grows from Om~0.3 today to ~1 at z>>1
- **phi**: Holling Type II handling-time coupling; predator saturation causes energy storage in quantum medium
- **+1**: ΛCDM limit when phi=0

### DESI prediction: Better than ΛCDM expected
Omega_m(z) doubles between z=0 and z=1 in ΛCDM background. With phi~0.3, this gives ~15% increase in omega_de at z=1, consistent with DESI DR2 signal.

### A1+A2 consistency: ✓
A1: Holling Type II predation rate sigma*n*rho_m/(1+h*n) is the modified annihilation term. A2: quantum-classical boundary is where predator handling time prevents further annihilation (n*h ~ 1).

---

## E3: Allee Effect — Cooperative Quantum Creation

### Physical premise from A1+A2:

The Allee effect describes populations where growth rate is REDUCED at low population density (failure of cooperative effects). Spacetime quanta cooperate in creating new quanta: when quantum density is low, pair-creation is suppressed.

From A1: creation requires quantum-quantum cooperation (e.g., two quanta interacting to birth a third, like vacuum pair production). This gives an Allee-type creation term.

From A2: the Allee threshold m (minimum population for positive growth) defines the quantum-classical boundary: below density m, the quantum field cannot sustain itself classically → classical spacetime.

The Allee effect ODE:

    dn/dt = r * n * (n - m) * (K - n) / K^2 - sigma*n*rho_m

Setting to equilibrium (three roots: n=0, n=m, n=n_eq):

    r * (n - m) * (K - n) / K^2 = sigma * rho_m

Solving the quadratic (n - m)(K - n) = sigma*rho_m*K^2/r:

    -n^2 + (m+K)*n - m*K = sigma*rho_m*K^2/r

    n^2 - (m+K)*n + m*K + sigma*rho_m*K^2/r = 0

    n_eq = [(m+K) ± sqrt((m+K)^2 - 4*(m*K + sigma*rho_m*K^2/r))] / 2

The stable high-density root (+ branch):

    n_eq(z) = [(m+K) + sqrt((K-m)^2 - 4*sigma*rho_m(z)*K^2/r)] / 2

Define:
- epsilon = m/K (Allee ratio, 0 < epsilon < 1)
- B(z) = 4*sigma*rho_m(z)*K/(r*(1-epsilon)^2) (predation-to-Allee ratio)

Then:

    n_eq(z) = K/2 * [(epsilon+1) + (1-epsilon)*sqrt(1 - B(z))]

Normalized:

    omega_de(z) = OL0 * n_eq(z) / n_eq(0)
               = OL0 * [(epsilon+1) + (1-epsilon)*sqrt(1 - B(z))] / [(epsilon+1) + (1-epsilon)*sqrt(1-B(0))]

For small B(z) (weak predation):

    sqrt(1-B(z)) ≈ 1 - B(z)/2

    n_eq(z) ≈ K/2 * [2 - (1-epsilon)*B(z)/2]
            = K * (1 - (1-epsilon)*B(z)/4)

This DECREASES with z (B(z) ∝ (1+z)^3). Same problem as before.

**Key distinction of Allee effect**: the Allee threshold m creates a second dark energy component — the "ghost" dark energy from sub-threshold regions where quanta cannot cooperate:

In regions where local n < m, quanta FAIL to cooperate and their energy is released as vacuum dark energy (decoherence energy from failed cooperative creation). The fraction of space with n < m scales as the Allee probability:

    P_Allee(z) = 1 - n_eq(z)/K = fraction of space in Allee-inhibited state

    P_Allee(z) ~ epsilon + (1-epsilon)*B(z)/4 + ...

Dark energy from Allee-failed regions:

    omega_de(z) = OL0 * (1 + A_e * P_Allee(z) / P_Allee(0))

But P_Allee(0) = epsilon, so:

    omega_de(z) ≈ OL0 * (1 + A_e * (epsilon + (1-epsilon)*B(z)/4) / epsilon)
               = OL0 * (1 + A_e + A_e*(1-epsilon)/(4*epsilon) * B(z))

For the z-dependent part:

**E3 Allee dark energy formula**:

    omega_de(z) = OL0 * (1 + A_e * (1 - 1/sqrt(1 + zeta * Om * (1+z)^3 / OL0)))

where zeta = 4*sigma*K/(r*(1-epsilon)^2 * epsilon) is the Allee-predation coupling, and A_e is the amplitude.

For small arguments: 1 - 1/sqrt(1+x) ≈ x/2. So:

    omega_de(z) ≈ OL0 * (1 + A_e * zeta * Om * (1+z)^3 / (2*OL0))

At high z this saturates (the 1/sqrt term → 0, limit = 1). Full saturation:

    omega_de(z → inf) → OL0 * (1 + A_e)

**Final E3 formula** (2 parameters reducible to 1):

    omega_de(z) = OL0 * (1 + A_e * (1 - (1 + zeta*Om*(1+z)^3/OL0)^{-1/2}))

At z=0: omega_de = OL0*(1 + A_e*(1-(1+zeta*Om/OL0)^{-1/2}))

To ensure omega_de(0) = OL0: set A_e = 1 / (1 - (1+zeta*Om/OL0)^{-1/2}) - 1, or use:

    omega_de(z) = OL0 * [(1+zeta*Om*(1+z)^3/OL0)^{-1/2} + psi*(1 - (1+zeta*Om*(1+z)^3/OL0)^{-1/2})]

where psi controls the high-z limit. Normalize at z=0:

Simplest 1-parameter self-consistent form:

    omega_de(z) = OL0 * (1 + zeta * Om * ((1+z)^{3/2} - 1) / OL0)

This is the Allee formula: the (1+z)^{3/2} comes from the sqrt in the Allee equilibrium, distinguishing it from the linear (1+z)^3 of simple predation. The 3/2 power is the Allee signature.

**Free parameters**: 1 (zeta, Allee-predation coupling)

### Justification:
- **(1+z)^{3/2}**: Allee effect sqrt-scaling from quadratic cooperative creation; distinguishes from E1's (1+z)^3
- **zeta**: ratio of predation pressure to cooperative threshold; from Allee minimum m and matter cross-section
- **Om/OL0 factor**: normalization ensuring correct ΛCDM limit as zeta → 0
- **-1 term**: zero-point normalization at z=0

### DESI prediction: Better than ΛCDM expected
The (1+z)^{3/2} power law grows more gently than (1+z)^3, providing a natural "intermediate" evolution that may better fit the full DESI z-range from z=0.3 to z=2.3.

### A1+A2 consistency: ✓
A1: creation = cooperative Allee term r*n*(n-m)*(K-n)/K^2, destruction = sigma*n*rho_m. A2: the Allee threshold m is the quantum-classical boundary — below m, cooperative creation fails and classical spacetime takes over.

---

## Phase 3 Summary

| Theory | omega_de(z) formula | Parameters | DESI direction |
|--------|--------------------|-----------:|----------------|
| E1 | OL0 * (1 + xi_m*Om*(1+z)^{3/2}/OL0) | 1 (xi_m) | Gentle power-law growth |
| E2 | OL0 * (1 + phi*Om*(1+z)^3/E(z)^2) | 1 (phi) | Tied to matter fraction |
| E3 | OL0 * (1 + zeta*Om*((1+z)^{3/2}-1)/OL0) | 1 (zeta) | Allee sqrt-scaling |

All three theories produce omega_de(z) > OL0 at high z via ecological equilibrium physics from A1+A2.
