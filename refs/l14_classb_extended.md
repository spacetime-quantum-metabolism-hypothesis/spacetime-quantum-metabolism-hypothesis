# refs/l14_classb_extended.md -- L14: Class B Extended (B1-B20)

> Date: 2026-04-11
> Source: l14_alternative_equations.md (B1-B8) + 8-team extended exploration
> Task: Expand Class B to 20 equations; evaluate DESI improvement potential.

Premise: "Spacetime quanta are annihilated upon collision with matter."
All Class B equations include a creation term Gamma_0 > 0 (beyond premise).

---

## B1~B8 Summary (from l14_alternative_equations.md)

| Eq | Form | Status | DESI qualitative |
|----|------|--------|-----------------|
| B1 | dn/dt+3Hn = Gamma_0 - sigma*n*rho_m | Current standard | w0~-0.9, wa~-0.1. PARTIAL |
| B2 | dn/dt+3Hn = Gamma_0 - sigma*n*rho_m^2 | Untested (quadratic sink) | sigma2 is 39 orders below sigma1; indistinguishable |
| B3 | dn/dt+3Hn = Gamma_0 - sigma*n*rho_m^alpha (alpha<1) | Sub-linear | Flatter than B1; wa->0 as alpha->0. WORSE |
| B4 | dn/dt+3Hn = Gamma_0*(n_eq/n) - sigma*n*rho_m | Feedback creation | Numerically: wa~-0.004. WORSE than B1 |
| B5 | dn/dt+3Hn = Gamma_0 - sigma*n*(rho_m+eps*rho_r) | Radiation coupling | Negligible at low z. SIMILAR to B1 |
| B6 | tau*d^2n/dt^2+dn/dt+3Hn = Gamma_0 - sigma*n*rho_m | Telegrapher | Oscillatory for tau~H0^-1. WORSE |
| B7 | dn/dt+3Hn = Gamma_0 - sigma*n*rho_m + D*nabla^2n | Diffusion | Irrelevant at cosmological scales. IDENTICAL to B1 |
| B8 | Full quantum foam operator equation | Quantum | Planck-suppressed. IDENTICAL to B1 |

---

## B9~B20: New Equations (8-team independent search)

---

### B9. Hubble-Modulated Creation Rate

**Team:** Team 1 (Kinetic theory / Boltzmann)
**Strategy:** Vary Gamma_0 to depend on H

**Equation:**

    dn/dt + 3Hn = Gamma_0 * (H/H0) - sigma*n*rho_m

**Physical motivation:**
Creation rate of spacetime quanta is proportional to the expansion rate.
In de Sitter inflation, pair creation rates scale with H (Hawking-like).
If quantum foam "boils" faster at higher H, Gamma_0 should track H(z).
This gives Gamma_0_eff(z) = Gamma_0 * E(z), where E(z) = H(z)/H0.

**Equilibrium:**

    n_eq(z) = Gamma_0 * E(z) / (sigma*rho_m(z) + 3H(z))
            = Gamma_0 / (sigma*rho_m(z)/H(z) + 3H0)

At high z: E(z) grows as (1+z)^(3/2) (matter dominated), but rho_m also grows.
The ratio E(z)/rho_m(z) ~ (1+z)^(3/2)/(1+z)^3 = (1+z)^(-3/2) -> 0 at large z.
So n_eq -> 0 at high z: LESS dark energy in the past than B1.

**DESI prediction:**
- rho_DE decreases faster at high z than B1
- wa more negative than B1 (wa < -0.1)
- w0 similar to B1 (~-0.9)
- Potentially closer to DESI wa = -0.83 if the rate is right

**Additional parameters:** 0 (Gamma_0 redefined by normalization)
**DESI improvement:** Potentially YES -- wa more negative. Worth numerical test.
**Numerical value:** HIGH (wa direction correct for DESI)

---

### B10. Density-Squared Creation Rate

**Team:** Team 2 (Fluid mechanics / Continuity)
**Strategy:** Gamma_0 depends on n^2 (stimulated emission analogy)

**Equation:**

    dn/dt + 3Hn = Gamma_0 * (n/n_0)^2 - sigma*n*rho_m

**Physical motivation:**
Stimulated creation: existing quanta "catalyze" creation of new ones,
analogous to stimulated emission in lasers. Rate ~ n^2 (two-quantum process).
At n < n_0: creation suppressed. At n > n_0: creation enhanced (unstable).

**Equilibrium (linearizing around n_0):**
Let u = n/n_0. Then: du/dt = Gamma_0/n_0 * u^2 - sigma*n_0*u*rho_m - 3H*u
Equilibrium: u_eq^2 * Gamma_0/n_0 = u_eq*(sigma*n_0*rho_m + 3H)
=> u_eq = n_0 * (sigma*n_0*rho_m + 3H) / Gamma_0
For n < n_eq: creation term < loss term => n decreases. Unstable unless Gamma_0 large.

**Stability issue:** Runaway for n > n_0. Not naturally stable. Requires Gamma_0 >> sigma*n_0*rho_m.

**DESI prediction:**
For stable regime (near n_0): similar to B1 but with stronger dependence on current n.
The functional form is different -- the effective equation of state may oscillate.
Qualitatively: wa could be positive or negative depending on parameter regime.

**Additional parameters:** 1 (n_0 -- reference density)
**DESI improvement:** LOW (stability issues; oscillatory behavior likely)
**Numerical value:** LOW

---

### B11. Void-Enhancement Creation

**Team:** Team 3 (Thermodynamics / Entropy)
**Strategy:** Gamma_0 enhanced in low-density regions

**Equation:**

    dn/dt + 3Hn = Gamma_0 / (1 + rho_m/rho_ref) - sigma*n*rho_m

**Physical motivation:**
Spacetime quantum creation is suppressed in dense regions (matter "screens" the
quantum vacuum from which quanta are created) and enhanced in voids (free vacuum).
rho_ref is a reference density scale (e.g., rho_crit_0). This is the Michaelis-Menten
(saturation) functional form from enzyme kinetics.

**Equilibrium:**

    n_eq = Gamma_0 / [(sigma*rho_m + 3H) * (1 + rho_m/rho_ref)]

At high z (rho_m >> rho_ref): n_eq ~ Gamma_0 / (sigma*rho_m^2/rho_ref) ~ rho_m^(-2)
At low z (rho_m << rho_ref): n_eq ~ Gamma_0 / (sigma*rho_m + 3H) -> B1

**DESI prediction:**
More suppression at high z than B1: rho_DE ~ (1+z)^(-6) at high z.
At low z: identical to B1. Transition at z where rho_m ~ rho_ref.
This gives a strong rho_DE(z) drop at some z* -- larger |wa| than B1.
Could give wa closer to DESI -0.83 for appropriate rho_ref.

**Additional parameters:** 1 (rho_ref)
**DESI improvement:** POTENTIALLY YES (stronger z-evolution, tunable wa)
**Numerical value:** MODERATE-HIGH (1 extra free parameter)

---

### B12. Power-Law Hubble Creation

**Team:** Team 4 (Modified gravity / Scalar-tensor)
**Strategy:** Gamma_0 ~ H^alpha (power-law)

**Equation:**

    dn/dt + 3Hn = Gamma_0 * (H/H0)^alpha - sigma*n*rho_m

**Physical motivation:**
Generalizes B9 (alpha=1) to arbitrary power. Alpha=0 gives B1 (constant Gamma_0).
Alpha=2 gives Gamma_0 ~ H^2 ~ rho_crit (total energy density). For H-driven creation:
quantum foam is related to spacetime curvature R ~ H^2, and creation ~ R^(alpha/2).

**Equilibrium:**

    n_eq(z) = Gamma_0 * E(z)^alpha / (sigma*rho_m + 3H)

For alpha in (0,2]: interpolates between B1 and strong-H coupling.
For alpha=2: n_eq ~ E(z)^2 / (sigma*rho_m + 3H) ~ E(z)^2 / (Om*(1+z)^3 + 3E)
At high z (matter dominated): ~ (1+z)^3 / (1+z)^3 = const. Nearly constant n_eq at high z.
This would give MUCH less wa than B1 -- worse for DESI.

For alpha=1 (B9): as analyzed above, wa more negative.
For alpha<0: creation decreases with H -- n_eq drops at high z. Very large |wa|.

**Additional parameters:** 1 (alpha)
**DESI improvement:** For alpha~0.5-1: possibly YES. For alpha~2: NO.
**Numerical value:** MODERATE (scan over alpha to find DESI-compatible range)

---

### B13. Coupled System: n and rho_m Mutual Feedback

**Team:** Team 5 (Field theory / Lagrangian)
**Strategy:** n and rho_m coupled bidirectionally

**Equations (system):**

    dn/dt + 3Hn = Gamma_0 - sigma*n*rho_m + beta*rho_m*(n_0-n)/n_0
    d(rho_m)/dt + 3H*rho_m = -sigma*n*rho_m

**Physical motivation:**
Matter absorbing spacetime quanta should be modified: matter density decreases
as quanta are annihilated (matter is partially "converted"). The second equation
shows matter density decreasing at rate sigma*n*rho_m (each annihilation removes
one quantum and slightly modifies matter). This is the full IDE system.
beta is an additional coupling for direct n-rho_m feedback.

**Equilibrium:**
The system has a fixed point where dn/dt = drho_m/dt = 0.
In the simple (beta=0) case: matter continuity is violated (rho_m evolves differently from (1+z)^3).
This changes the sound horizon and is tightly constrained by CMB.

**DESI prediction:**
If beta=0: matter density depletion creates a DE-like component at late times.
rho_m drops faster than (1+z)^3, allowing n to grow beyond the B1 prediction.
Could give w0 < -1 (phantom) if matter depletion is large enough.
If SQMH requires sigma*n*rho_m << rho_m: the matter sector is nearly unaffected.

**Additional parameters:** 1 (beta), plus the coupled system changes rho_m(z)
**DESI improvement:** UNCERTAIN -- likely tightly constrained by CMB/BAO (r_d)
**Numerical value:** LOW-MODERATE (matter sector modification is dangerous)

---

### B14. Delayed Annihilation (Retarded ODE)

**Team:** Team 6 (Non-equilibrium / Causal)
**Strategy:** Annihilation uses delayed density

**Equation:**

    dn/dt + 3Hn = Gamma_0 - sigma*n(t)*rho_m(t - tau)

**Physical motivation:**
Annihilation is not instantaneous: a quantum traveling at c takes a light-crossing
time tau to "register" the local matter density before being absorbed.
tau ~ l_mfp / c where l_mfp is the mean free path. For cosmological n, tau << H^{-1}.

**Analysis:**
Expanding rho_m(t - tau) ~ rho_m(t) - tau * d(rho_m)/dt + ...
For matter domination: d(rho_m)/dt = -3H*rho_m, so:
  rho_m(t-tau) ~ rho_m(t) * (1 + 3H*tau)

This gives an effective sigma_eff = sigma * (1 + 3H*tau).
For tau << H^{-1}: tiny correction, indistinguishable from B1.
For tau ~ H^{-1}: large correction, but requires tau ~ Gyr -- unphysical.

**DESI prediction:**
Correction is O(H*tau) ~ O(sigma_correction). For cosmological tau: IDENTICAL to B1.
**Additional parameters:** 1 (tau -- but physically forced to be negligibly small)
**DESI improvement:** NO (correction negligible for causal tau)
**Numerical value:** LOW

---

### B15. Entropy-Based Creation Rate

**Team:** Team 7 (Extended thermodynamics / Clausius)
**Strategy:** Gamma_0 derived from entropy production rate

**Equation:**

    dn/dt + 3Hn = (T * dS/dt) / (mu * V) - sigma*n*rho_m

where dS/dt is the entropy production rate in the quantum foam.

**Physical motivation:**
The second law of thermodynamics: the total entropy of the universe increases.
Spacetime quanta are created at the rate needed to prevent entropy from decreasing.
If annihilation reduces entropy, creation must compensate.
From Clausius: dS/dt >= 0 everywhere. If each annihilation produces entropy delta_S,
then creation must produce negative entropy at rate Gamma_0 = sigma*n*rho_m (balance).
This recovers the equilibrium condition dS/dt = 0 exactly at late times.

For a non-equilibrium cosmology:
  dS/dt = (H * S_Hubble) - sigma*n*rho_m * delta_s
where S_Hubble is the entropy of the cosmological horizon ~ (H/H0)^{-2}.

Simplified:
  Gamma_eff = Gamma_0 * (H0/H)^2 = Gamma_0 * E(z)^{-2}

**Equation:**

    dn/dt + 3Hn = Gamma_0 * (H0/H)^2 - sigma*n*rho_m

**Equilibrium:**

    n_eq(z) = Gamma_0 / (E(z)^2 * (sigma*rho_m + 3H))
            = Gamma_0 / (E(z)^2 * sigma*rho_m + 3*H0*E(z))

At high z: E(z)^2 ~ (1+z)^3, sigma*rho_m ~ (1+z)^3, so n_eq ~ (1+z)^{-6}.
Faster decay than B1 (which gives ~ (1+z)^{-3}). Much larger |wa|.

**DESI prediction:**
- rho_DE drops as (1+z)^{-6} at high z (much steeper than B1)
- wa >> |0.83| -- possibly too large
- w0 similar to B1 or slightly more negative
- Could match DESI or overshoot wa

**Additional parameters:** 0 (Gamma_0 by normalization)
**DESI improvement:** POSSIBLY YES but may overshoot wa
**Numerical value:** MODERATE-HIGH (no extra params; strong DESI signal)

---

### B16. Scalar Field Coupled Creation

**Team:** Team 8 (Scalar-tensor / Quintessence coupling)
**Strategy:** Gamma_0 coupled to scalar field phi

**Equation:**

    dn/dt + 3Hn = Gamma_0 * exp(-lambda*phi/M_P) - sigma*n*rho_m
    phi'' + 3H*phi' + dV/dphi = beta*n*mu

**Physical motivation:**
The creation rate depends on a background scalar field phi (dark energy quintessence).
As phi evolves (slow-roll), Gamma_0_eff changes. The back-reaction of n on phi
adds a source term to the Klein-Gordon equation. This is the coupled dark energy framework.
lambda and beta are dimensionless coupling constants (beta related to SQMH coupling).

For slow-roll phi: Gamma_0_eff = Gamma_0 * exp(-lambda*phi/M_P) changes slowly.
At late times (phi -> phi_inf): Gamma_0_eff can increase or decrease depending on lambda.

**DESI prediction:**
Very model-dependent. For lambda > 0 and phi increasing:
- Gamma_0_eff decreases at late times
- n_eq decreases at late times
- rho_DE decreases: w0 becomes more negative; wa could be negative or positive
This class effectively merges SQMH with thawing quintessence.
Constraint: K12 from SQMH project -- w(z=0) coupling to scalar.

**Additional parameters:** 2 (lambda, beta)
**DESI improvement:** UNTESTED but structurally flexible
**Numerical value:** MODERATE (requires joint quintessence+SQMH ODE)

---

### B17. Non-Local Creation (Integral Creation Rate)

**Team:** Team 1 (Round 2)
**Strategy:** Creation rate as a time-integral (non-local in time)

**Equation:**

    dn/dt + 3Hn = Gamma_0 * integral_0^t [K(t,t')*n(t')*dt'] - sigma*n*rho_m

where K(t,t') = exp(-(t-t')/tau_mem) / tau_mem is a memory kernel.

**Physical motivation:**
Spacetime quantum creation depends on the history of the quantum density,
not just the instantaneous value. If quanta were more abundant in the past,
the "quantum vacuum tension" (driving creation) is reduced now.
This is a Volterra integral equation with exponential memory.

**Mathematical reduction:**
For exponential kernel, define auxiliary field psi:
  dpsi/dt + psi/tau_mem = n
Then: creation = Gamma_0 * psi
System:
  dn/dt + 3Hn = Gamma_0 * psi - sigma*n*rho_m
  dpsi/dt + psi/tau_mem = n

For tau_mem << H^{-1}: psi ~ tau_mem * n, and Gamma_0*psi ~ Gamma_0*tau_mem*n.
This gives a modified Gamma_0_eff ~ Gamma_0*tau_mem with a slightly modified equation.
For tau_mem >> H^{-1}: psi tracks a long-time average of n, introducing a lag.

**DESI prediction:**
For tau_mem << H0^{-1}: identical to B1 (tau_mem correction negligible).
For tau_mem ~ H0^{-1}: introduces non-trivial phase lag.
The dark energy density would respond to matter density changes with a delay,
potentially creating oscillatory or delayed transitions.

**Additional parameters:** 1 (tau_mem)
**DESI improvement:** UNTESTED (potentially interesting for tau_mem ~ H0^{-1})
**Numerical value:** MODERATE

---

### B18. Temperature-Dependent Creation Rate

**Team:** Team 2 (Round 2)
**Strategy:** Gamma_0 ~ T^n (photon temperature)

**Equation:**

    dn/dt + 3Hn = Gamma_0 * (T/T0)^2 - sigma*n*rho_m

where T = T0*(1+z) is the CMB photon temperature.

**Physical motivation:**
Quantum foam is in partial thermal contact with the photon bath.
Creation rate ~ Planck radiation density ~ T^4, but effective coupling may give T^2.
At high z: T >> T0, creation rate enhanced. At low z: creation reduced.
This is opposite to what is needed for DESI (we need LESS dark energy at high z).

**Equilibrium:**

    n_eq(z) = Gamma_0 * (1+z)^2 / (sigma*rho_m + 3H)
             ~ Gamma_0 * (1+z)^2 / (sigma*Om*(1+z)^3*rho_c0 + 3H0*E)

At high z (matter dominated):
  n_eq ~ Gamma_0 * (1+z)^2 / (sigma*Om*(1+z)^3*rho_c0) ~ (1+z)^{-1} -> MORE dark energy at high z.
This increases rho_DE at high z vs low z: wa > 0 (WRONG SIGN for DESI).

**DESI prediction:**
wa > 0. Wrong direction for DESI wa = -0.83. FAIL.
**Additional parameters:** 0 (Gamma_0 by normalization; exponent fixed at 2)
**DESI improvement:** NO (wrong wa sign)
**Numerical value:** LOW

---

### B19. Threshold Creation (Step-Function)

**Team:** Team 3 (Round 2)
**Strategy:** Creation only occurs below a critical density

**Equation:**

    dn/dt + 3Hn = Gamma_0 * Theta(rho_crit_local - rho_m) - sigma*n*rho_m

where Theta is the Heaviside step function (creation only in voids).

Smooth approximation:

    dn/dt + 3Hn = Gamma_0 / (1 + exp(alpha*(rho_m - rho_ref)/rho_ref)) - sigma*n*rho_m

**Physical motivation:**
In SQMH, dense matter environments suppress quantum creation.
Above a threshold density rho_ref, creation is completely suppressed (Pauli-exclusion-like
saturation of the quantum foam). In cosmic voids, creation proceeds normally.
This is the "cosmic void breathing" mechanism: dark energy is created only in voids.

**Homogeneous universe (smooth approx):**
At z=0: rho_m << rho_ref (typically), Gamma_eff ~ Gamma_0 (creation on).
At high z: rho_m >> rho_ref, Gamma_eff ~ 0 (creation off).
The transition at rho_m ~ rho_ref occurs at z* where Om*(1+z*)^3 = rho_ref/rho_c0.

**Equilibrium:**

For z < z*: n_eq ~ Gamma_0/(sigma*rho_m + 3H)  [like B1]
For z > z*: n_eq ~ 0/(sigma*rho_m + 3H) = 0   [dark energy vanishes]

**DESI prediction:**
Sharp decrease in rho_DE at z > z*. For rho_ref ~ rho_crit_0: z* ~ few.
This could give very large |wa|. The step-function form gives a sharp transition
that may not fit BAO smoothly -- but could approximate the DESI signal.

**Additional parameters:** 1 (rho_ref)
**DESI improvement:** POTENTIALLY large improvement in wa, but sharp transition may fail chi2
**Numerical value:** MODERATE-HIGH (interesting shape, but parameter tuning needed)

---

### B20. Quadratic Hubble Damping

**Team:** Team 4 (Round 2)
**Strategy:** Modify the dilution term (Hubble coefficient)

**Equation:**

    dn/dt + 3H(1 + gamma*H/H0)*n = Gamma_0 - sigma*n*rho_m

**Physical motivation:**
The FLRW dilution term 3Hn assumes w_sq = 0 (non-relativistic quanta).
If quanta have a small pressure p_sq = gamma*H/H0 * (rho_sq/3) (H-dependent EoS),
the effective Hubble coefficient becomes 3H*(1 + gamma*E(z)/1).
At late times (low H): standard dilution. At early times (high H): enhanced dilution.

**Equilibrium:**

    n_eq(z) = Gamma_0 / (sigma*rho_m + 3H*(1 + gamma*E(z)))
             = Gamma_0 / (sigma*rho_m + 3H0*E(z)*(1+gamma*E(z)))

At high z: E(z)^2 >> 1, denominator ~ 3*gamma*H0*E(z)^2 ~ (1+z)^3.
n_eq ~ Gamma_0/((1+z)^3): same as matter dilution. rho_DE more suppressed at high z.
For gamma < 0: denominator smaller at high z -> LESS suppression -> wa > 0 (WORSE for DESI).
For gamma > 0: enhanced dilution -> MORE suppression -> larger |wa|, could match DESI.

**DESI prediction:**
For gamma ~ 0.1-0.5: wa more negative than B1. Direction correct for DESI.
The gamma parameter effectively increases the speed of rho_DE decrease at high z.
This is equivalent to B12 with alpha=1 (Hubble-modulated creation) up to reparametrization.
Not independent -- essentially the same physical content as B9/B12.

**Additional parameters:** 1 (gamma)
**DESI improvement:** YES for gamma > 0, but not independent of B9/B12
**Numerical value:** MODERATE (conceptually redundant with B9)

---

## Summary Table: B1-B20

| Eq | Creation form | Annihilation form | Extra params | wa direction vs B1 | DESI value |
|----|--------------|-------------------|-------------|-------------------|-----------|
| B1 | Gamma_0=const | sigma*n*rho_m | 0 | reference (wa~-0.1) | BASELINE |
| B2 | Gamma_0=const | sigma*n*rho_m^2 | 0 (sigma2) | More negative? | NEGLIGIBLE (39 OOM) |
| B3 | Gamma_0=const | sigma*n*rho_m^alpha <1 | 1 | Less negative | WORSE |
| B4 | Gamma_0*(n_eq/n) | sigma*n*rho_m | 0 | wa~0 | WORSE (B4 chi2=12.38 vs B1=11.75) |
| B5 | Gamma_0=const | sigma*n*(rho_m+eps*rho_r) | 1 | ~B1 | SIMILAR |
| B6 | Gamma_0=const | sigma*n*rho_m | 1 (tau) | Oscillatory | WORSE |
| B7 | Gamma_0=const+diffusion | sigma*n*rho_m | 1 (D) | ~B1 | IDENTICAL |
| B8 | QFT Hamiltonian | QFT | -- | ~B1 | IDENTICAL |
| B9 | Gamma_0*H/H0 | sigma*n*rho_m | 0 | More negative | HIGH |
| B10 | Gamma_0*(n/n0)^2 | sigma*n*rho_m | 1 | Mixed | LOW (unstable) |
| B11 | Gamma_0/(1+rho_m/rho_ref) | sigma*n*rho_m | 1 | More negative | MODERATE-HIGH |
| B12 | Gamma_0*(H/H0)^alpha | sigma*n*rho_m | 1 | Tunable | MODERATE |
| B13 | Gamma_0=const (coupled) | sigma*n*rho_m (depletes rho_m) | 1 (beta) | Uncertain | LOW-MOD |
| B14 | Gamma_0=const | sigma*n*rho_m(t-tau) | 1 (tau) | ~B1 | NEGLIGIBLE |
| B15 | Gamma_0*(H0/H)^2 | sigma*n*rho_m | 0 | Much more negative | HIGH (may overshoot) |
| B16 | Gamma_0*exp(-lambda*phi) | sigma*n*rho_m | 2 | Model-dependent | MODERATE |
| B17 | Gamma_0*psi (memory) | sigma*n*rho_m | 1 (tau_mem) | Delayed | MODERATE |
| B18 | Gamma_0*(T/T0)^2 | sigma*n*rho_m | 0 | wa > 0 (WRONG) | FAIL |
| B19 | Gamma_0*Theta(rho_ref-rho_m) | sigma*n*rho_m | 1 (rho_ref) | Very negative | MOD-HIGH |
| B20 | Gamma_0=const | sigma*n*rho_m+gamma*H term | 1 (gamma) | More negative | MODERATE |

---

## Top 3 Most Promising (DESI Improvement Potential)

### 1st: B9 -- Hubble-Modulated Creation Rate (RECOMMENDED for numerical test)

    dn/dt + 3Hn = Gamma_0*(H/H0) - sigma*n*rho_m

**Rationale:**
- Zero extra parameters (Gamma_0 absorbed into normalization)
- Physical motivation: de Sitter-like creation proportional to H
- At high z: E(z) grows but rho_m grows faster -> n_eq decreases faster than B1
- Predicted: wa more negative (direction correct for DESI wa=-0.83)
- Simple, analytically tractable, same parameter count as B1
- Equilibrium: n_eq = Gamma_0*E(z) / (sigma*rho_m + 3H0*E(z))

### 2nd: B15 -- Entropy-Based Creation (Strong DESI signal, zero extra params)

    dn/dt + 3Hn = Gamma_0*(H0/H)^2 - sigma*n*rho_m

**Rationale:**
- Zero extra parameters
- Strong wa signal: rho_DE ~ (1+z)^{-6} at high z -> large negative wa
- Thermodynamic motivation (Clausius entropy production)
- Risk: wa may overshoot DESI -0.83 (could be too large)
- If |wa| ~ 0.5-2.0 range accessible, useful for DESI

### 3rd: B11 -- Void-Enhancement Creation (Tunable with 1 param)

    dn/dt + 3Hn = Gamma_0/(1 + rho_m/rho_ref) - sigma*n*rho_m

**Rationale:**
- 1 extra parameter (rho_ref) allows tuning wa to match DESI
- Physical motivation: creation suppressed in dense regions (Michaelis-Menten)
- At z < z*: identical to B1. At z > z*: rho_DE drops as (1+z)^{-6}
- rho_ref can be chosen to set the transition at the right epoch
- Most flexible among the zero-or-one-parameter extensions

---

## B4 Numerical Result (computed)

B4 equation:
  d(omega_de)/dz = (3/(1+z)) * (u_eq^2/u - u)
  where u_eq = A01 equilibrium, IC: omega_de(z=0) = OL0

Results (7-bin diagonal chi2, DESI DR2):
  LCDM  chi2=13.198  Om=0.3266
  B1    chi2=11.752  Dchi2 vs LCDM=-1.446  w0=-0.903  wa=-0.107
  B4    chi2=12.378  Dchi2 vs LCDM=-0.820  w0=-0.943  wa=-0.004

B4 verdict: WORSE than B1 by Dchi2=0.627.
The feedback mechanism drives omega_de very quickly to equilibrium, suppressing
all z-dependence beyond the equilibrium curve. This effectively kills wa.
B4 is NOT a promising DESI alternative.

---

*L14 ClassB Extended completed: 2026-04-11*
*8-team exploration: B9~B20 identified, B4 numerically computed.*
