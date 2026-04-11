# 4. Linear Perturbation Theory

We now work out the linear scalar perturbations for each candidate
effective field realisation.  The purpose is (i) to compute fσ_8(z) for
the RSD likelihood, (ii) to verify positive sound speed and absence of
ghost degrees of freedom (K11), and (iii) to check that the effective
μ(a, k) and Σ(a, k) functions are consistent with Solar-System
constraints (K4).

## 4.1 Synchronous gauge ODEs

We follow the Ma-Bertschinger (1995) convention.  In synchronous gauge
the relevant scalar perturbation variables are (δ_m, θ_m, δ_DE, θ_DE)
for fluid dark energy and (δφ, δφ̇) for scalar dark energy.  At
sub-horizon scales (k ≫ a H) the matter density contrast obeys

```
δ″_m + (2 + H′/H) δ′_m − (3/2) Ω_m(a) μ(a, k) δ_m = 0,    (4.1)
```

where μ(a, k) = G_eff/G is the effective Newton constant felt by
matter.  The growth factor D(a, k) and growth rate
f(a, k) = d ln D / d ln a are obtained by integrating Eq. (4.1)
from a_ini = 10⁻³ with matter-dominated initial conditions
(D ∝ a, D′ ∝ 1).  fσ_8(z) is then constructed as

```
fσ_8(z) = f(z) · σ_8(z) = f(z) · σ_{8,0} · D(a) / D(1).
```

Full code in `simulations/l4/<ID>/perturbation.py` and
`simulations/l4/common.py::growth_fs8`.

## 4.2 Effective μ(a, k) per candidate

| ID | μ(a, k) | Comment |
|---|---|---|
| C27 | 1 | auxiliary U frozen in sub-horizon regime (Koivisto 2008) |
| C28 | 1 + small scale-dependent term from S auxiliary | Dirian 2015 Sec 4 |
| C33 | 1 + correction O(f₁ H²/k²) · (negligible at sub-horizon) | Hohmann-Krššák 2018 |
| C41 | 1 + drag term −β φ_N δ_m (continuity modification) | Di Porto-Amendola 2008 Eq 3 |
| C26 | 1 (diffusion is background effect only) | Perez-Sudarsky 2019 Sec 4 |
| C23 | 1 | no new scalar dof |
| C5r,C6s | 1 | Λ(H²) modifies only continuity |
| C11D | 1 (pure disformal, scalar mode decouples at static order) | Zumalacárregui 2013 |
| C10k | 1 + 2 β_d² (DM only, baryons untouched) | Amendola 2000 dark-only |

## 4.3 Sound speed positivity (K11)

For each candidate that carries an effective scalar degree of freedom
(C27, C28, C33, C41, C10k, C11D), we verify c_s² > 0 at all a ∈ (10⁻³, 1).
The non-local candidates (C27, C28) have auxiliary modes that are
non-propagating in the static limit and so c_s² is trivially positive.
C33 has c_s² = 1 for the teleparallel scalar.  C41 (fluid IDE) requires
c_s² = 1 by construction.  C10k and C11D inherit the quintessence sound
speed, set to c_s² = 1 throughout.

No candidate exhibits a negative sound speed or ghost degree of freedom,
so K11 is passed by all nine KEEP candidates.

## 4.4 Static post-Newtonian γ

The Cassini bound |γ − 1| < 2.3 × 10⁻⁵ (K4) is the strongest single
constraint that kills universal-coupling scalar-tensor theories.  All
candidates retained here satisfy γ − 1 = 0 **exactly** in the static
spherical limit:

- **C27, C28**: auxiliary fields U, V, S are frozen in Schwarzschild
  (R = 0 for Type D metrics), reducing the static limit to GR.
- **C33 f(Q)**: the symmetric teleparallel connection has no propagating
  extra scalar at this order (Hohmann-Krššák 2018).
- **C26**: diffusion modifies only background, not PPN.
- **C23, C5r, C6s**: RVM modifies only the Λ source; no new scalar dof.
- **C11D**: pure disformal in the A′ = 0 limit.
- **C10k**: dark-only coupling decouples baryons from the scalar; PPN
  reduces to GR on luminous matter.

## 4.5 fσ_8 predictions

Predicted fσ_8(z) at the 8 RSD redshifts is tabulated in §6, together
with posterior predictions from the MCMC runs.
