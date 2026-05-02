# Section 2: Axioms and derived relations

## 2.1 Field content and conventions

We work on a 4-dimensional pseudo-Riemannian manifold M with metric
g_μν of signature (-,+,+,+). The fundamental fields are: a scalar
quantum density field n: M → ℝ_≥0, the matter mass density ρ_m: M →
ℝ_≥0, and the spacetime metric g_μν. Greek indices μ, ν, ρ, σ run
over spacetime (0, 1, 2, 3); spatial indices i, j are restricted to
(1, 2, 3). The Einstein summation convention is in effect; covariant
derivative is denoted ;. We use SI units throughout with ℏ, c, G the
reduced Planck constant, speed of light, and Newton's constant.

## 2.2 Six axioms

**A1 (Absorption)**. The volumetric absorption rate of n by ρ_m is

   R_abs(x, t) = σ_0(env) · n(x, t) · ρ_m(x, t)

where σ_0 ≥ 0 is the regime-dependent quantum-matter coupling
(Section 3) and 'env' refers to local environmental properties.

**A2 (Energy conservation)**. Each absorption event transfers energy
ε from the n field to matter:

   ∂_t (ρ_m c²) + 3H ρ_m c² = +R_abs · ε
   ∂_t (n ε) + 3H n ε = -R_abs · ε + Γ_0 · ε

The second equation includes the cosmic creation source (A3).

**A3 (Cosmic creation)**. The n field has uniform isotropic creation
in cosmic frame:

   (∂_t n)_creation = +Γ_0   (constant Γ_0 ≥ 0)

The cosmic frame coincides with the CMB rest frame as an observational
convention; Γ_0 itself is a Lorentz scalar.

**A4 (Emergent metric)**. The spacetime metric g_μν is functionally
related to the n field configuration: g_μν = g_μν[n; ε, σ_0]. In the
limit σ_0 → 0, g_μν reduces to the standard Lorentzian metric of GR.

**A5 (Bound matter)**. Stable particles are localized bound
configurations of n satisfying ∫ ρ_m d³x = m_particle. The Standard
Model emerges from A5 in a manner detailed elsewhere.

**A6 (Linear maintenance)**. Particle absorption cross section is
proportional to particle mass:

   σ_quantum-particle ∝ m_particle

This recovers the equivalence principle automatically.

## 2.3 Background equations

In a flat FRW background, the axioms imply the following coupled
ODE system:

   dn/dt + 3H n = Γ_0 - σ_0 n ρ_m              (continuity for n)
   dρ_m/dt + 3H ρ_m = +σ_0 n ρ_m (ε/c²)        (matter density)
   H² = (8π G / 3)(ρ_m + n ε/c² + ρ_r) + Λ_eff/3  (Friedmann)

where ρ_r is radiation energy density and Λ_eff is the effective
cosmological constant computed below.

## 2.4 Derived relations

The axioms imply five derived relations governing observable quantities:

**D1 (Newton's constant)**. Self-consistent τ_q(env) = σ_0(env)/(4πG)
gives

   G = σ_0(env) / (4π · τ_q(env))                    (D1)

This holds independently in each Branch B regime (Section 3).

**D2 (Steady-state cosmic n)**. From dn/dt = 0 with negligible
matter coupling (cosmic regime):

   n_∞ = Γ_0 · τ_q                                   (D2)

**D3 (Quantum energy)**. Heisenberg uncertainty between energy and
quantum lifetime gives:

   ε = ℏ / τ_q                                       (D3, scenario Y)

In cosmic regime, τ_q ~ 1/H_0 implies ε ~ ℏH_0.

**D4 (Cosmological constant)**. The effective Λ comes from the
quantum sector:

   Λ_eff = (8π G / c²) · n_∞ · ε / c² = (8π G / c⁴) · n_∞ · ε  (D4)

**D5 (Milgrom's a_0)**. Combining D2-D4 with disc azimuthal
projection 1/(2π) (Section 4.3):

   a_0 = σ_0 · ρ_crit · c · (1/π) = c · H_0 / (2π)   (D5)

## 2.5 Consistency theorems

**Theorem 1 (Causality)**. In linearized perturbation theory around
n = n_∞, the dispersion relation ω² = c²k² + m²_eff + iγ_eff·ω yields
front (signal) velocity v_signal = c. Damped Klein-Gordon
analysis [Sommerfeld-Brillouin 1914] establishes causality.

**Theorem 2 (Lorentz invariance)**. Γ_0 is a Lorentz scalar by
construction. The cosmic frame is the CMB rest frame (observational
convention), not a fundamental Lorentz violation.

**Theorem 3 (Vacuum stability)**. ∂(dn/dt)/∂n |_{n=n_∞} = -3H -
σ_0 ρ_m < 0 in all regimes, establishing stability of the cosmic
vacuum.

**Theorem 4 (GR limit)**. In the limit σ_0 → 0, the matter and quantum
fields decouple. The Friedmann equation reduces to standard ΛCDM
with Λ obtained from D4 evaluated at the steady state.

**Theorem 5 (CPT)**. With C, P, T invariance properties verified
[Section 4.7], the Pauli-Lüders CPT theorem applies: SQT is CPT-
invariant at microscopic level, with macroscopic T-asymmetry
emerging from cosmic creation Γ_0.

## 2.6 Effective field theory cutoff

SQT is a non-renormalizable EFT with cutoff:

   Λ_UV = ℏc / d_inter-quantum ≈ 18 MeV

where d_inter-quantum = n_∞^(-1/3) ≈ 0.07 fm. Above this scale,
the fluid description breaks down and a UV completion (Loop Quantum
Gravity, asymptotic safety) is required.

---

대략 700 단어. Paper section 2 ready.
