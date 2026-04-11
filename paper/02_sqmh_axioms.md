# 2. SQMH Axioms

## 2.1 L0: discrete spacetime micro-structure

We posit that the gravitational field carries an additional discrete
degree of freedom described by a scalar number density n(x, t) of
"spacetime quanta" with individual rest mass μ.  The product nμ has
dimensions of an energy density and, at the present epoch, is fixed by
the Planck density:

```
n₀ μ = ρ_Planck / (4π) ≈ 4.1 × 10⁹⁵ kg m⁻³.
```

The individual values of n₀ and μ are not self-consistently determined
by the classical theory; only the product enters all observable
predictions.

## 2.2 L1: universal metabolism

Matter annihilates these quanta at a two-body mass-action rate σ n ρ_m,
with the cross-section fixed by matching the Newtonian gravitational
potential (§3.2):

```
σ = 4π G t_P   (SI units)
  ≈ 4.52 × 10⁻⁵³ m³ kg⁻¹ s⁻¹.
```

The vacuum generates quanta at a uniform rate Γ₀, fixed by the present
metabolism balance

```
Γ₀ = σ n₀ ρ_{m,0} + 3 H₀ n₀.
```

The continuity equation for n then reads

```
∂_t n + ∇·(n v) = Γ₀ − σ n ρ_m,    (2.1)
```

with v being the mean flow of spacetime quanta.  Gravity is identified
with the inflow v induced by local net annihilation near matter
(§3.1); cosmic expansion is identified with the net generation in
matter-empty regions.

## 2.3 Zero free parameters

Given (G, t_P, H₀, Ω_m, Ω_Λ), the SQMH has **no free background
parameters**.  This is the key feature distinguishing SQMH from generic
dynamical dark-energy (DDE) models, which typically carry (w₀, w_a) or
equivalent quintessence potential parameters.

## 2.4 FLRW continuity

In a homogeneous isotropic universe with ρ_m = ρ_m(t), Equation (2.1)
becomes

```
ṅ + 3 H n = Γ₀ − σ n ρ_m.    (2.2)
```

Solving this against the Einstein field equations with the identification
ρ_DE = (c² μ / 4π G) · (Γ₀ − σ n₀ ρ_{m,0}) (modulo bookkeeping) yields
the effective modified Friedmann equation

```
H²(a) = H₀² [Ω_r a⁻⁴ + Ω_m a⁻³ + Ω_Λ + ξ_q f(a)],    (2.3)
```

where f(a) encodes the metabolism drift.  The parameter ξ_q is itself
derivable from the SQMH invariants; in this paper we treat it as zero
for the strict zero-parameter SQMH and as a posterior-fit parameter
within the effective-field-theory realisations considered in §3.

## 2.5 Relation to existing frameworks

SQMH is structurally closest to:
- **Unimodular diffusion** (Perez-Sudarsky 2019): L1 is exactly a
  diffusion current J⁰ > 0 from matter to Λ.
- **Running Vacuum Models** (Solà, Gómez-Valent 2024): Λ(H²) = Λ₀ +
  3 ν H² maps to a particular closed form of Eq. (2.3).
- **Non-local gravity** (Deser-Woodard 2008, Maggiore-Mancarella 2014):
  localised auxiliary fields U, V, S obey equations structurally
  identical to Eq. (2.2) after gauge fixing.

These correspondences drive the candidate list in §3.
