# Phase 11: Bose-Einstein Condensation of Spacetime Quanta

## Phenomenological Interpretation of A1 and A2

**A1**: Spacetime quanta are bosons that condense below a critical temperature T_c.
- Matter annihilates quanta = phonon excitation (heating the condensate, depleting it).
- Empty space creates quanta = the cooling bath that maintains/restores condensation.

**A2**: The quantum-classical boundary is derivable from A1.
- Derivation: The boundary is exactly the condensate threshold T = T_c.
- Above T_c (high matter density, high z): quanta are in excited states → classical geometry.
- Below T_c (low matter density, low z): quanta condense → coherent quantum vacuum = dark energy.

## Setup

Critical temperature scales as T_c ∝ n^{2/3} where n is the number density of quanta.
Effective temperature T_eff(z) ∝ rho_m(z)^{1/3} (matter heating scales with energy density).
Condensate fraction: f_c = 1 - (T_eff/T_c)^{3/2} for T_eff < T_c; else f_c = 0.

Define dimensionless matter density: x(z) = rho_m(z)/rho_m0 = (1+z)^3.

---

## Theory B1: Condensate Fraction (BEC threshold)

**Physical picture**: Dark energy density proportional to the condensate fraction.
At z=0, matter density is rho_m0 = Om*rho_crit0; condensate is partially formed.
At higher z, rho_m > rho_c_BEC → condensate destroyed → dark energy suppressed.

BEC condensate fraction:
  f_c(z) = max(1 - (rho_m(z)/rho_m0)^{1/2}, 0)
           = max(1 - (1+z)^{3/2}, 0)

Note: f_c(0) = 1 - 1 = 0 if we use rho_m0 as the critical density exactly.
To avoid degeneracy, define rho_c_BEC = A * rho_m0 with A > 1, so:
  f_c(z) = max(1 - (rho_m(z)/(A*rho_m0))^{1/2}, 0)
           = max(1 - (1+z)^{3/2}/A^{1/2}, 0)

Normalize: omega_de(0) = OL0 requires f_c(0)/f_c(0) = 1.

**Explicit formula B1**:
```
omega_de(z) = OL0 * max(1 - (1+z)^{3/2}/sqrt(A), 0) / max(1 - 1/sqrt(A), 0)
```

Parameters: A > 1 (ratio of critical to present matter density, A ~ 2-10).

Phenomenological range: for A=4, f_c(0) = 1 - 0.5 = 0.5; at z=1: f_c = max(1 - 2.83/2, 0) = 0 → omega_de drops to zero above z ~ (A^{1/3} - 1) ≈ 0.59 (for A=4).

**Effective equation of state**: w(z) approaches -1 at z=0, becomes less negative then truncates. Strong evolution → wa << -1 possible in effective CPL fit.

---

## Theory B2: BEC Order Parameter (Bogoliubov mean field)

**Physical picture**: The BEC order parameter |Psi|^2 grows as matter density drops below rho_m0. The order parameter scales as the condensate density excess, following Ginzburg-Landau theory where |Psi|^2 ∝ (rho_c - rho_m)^{beta_GL} with beta_GL = 2/3 in 3D BEC.

For rho_m(z) < rho_m0 (i.e., z=0 only for our convention, or interpret rho_m0 as the BEC threshold):
  |Psi(z)|^2 ∝ (rho_m_threshold - rho_m(z))^{2/3}
             ∝ (rho_m0 * (1 - (1+z)^3))^{2/3}   [only valid for z such that (1+z)^3 < 1, unphysical]

Reinterpret: order parameter enhancement above baseline:
  omega_de = OL0 * (1 + A * (rho_m0/rho_m(z) - 1)^{2/3})   for rho_m(z) < rho_m0 i.e. z=0
           = OL0 * (1 + A * ((1+z)^{-3} - 1)^{2/3})         for z < 0 (future only)

Physical reinterpretation for all z: order parameter = how far system is ABOVE the transition.
Replace (rho_m0/rho_m - 1) → (1/(1+z)^3 - 1) is negative for z > 0.
Use modulus with sign: omega_de = OL0 * (1 + A * |1 - (1+z)^3|^{2/3} * sign(1-(1+z)^3))

For a well-defined formula valid for all z with enhancement at z > 0:
Let the BEC threshold be at z_c such that matter was at BEC transition then.
Define: effective order parameter grows as matter density decreases toward present.

**Explicit formula B2** (recast as written in prompt):
```
omega_de(z) = OL0 * (1 + A * ((1+z)^{-3} - 1)^{2/3})
```
Valid for z small enough that (1+z)^{-3} - 1 > 0, i.e., only z < 0 (future).

For cosmologically useful form (z ≥ 0): the condensate fraction today is partial.
Use: p(z) = Om*(1+z)^3 / (Om*(1+z)^3 + OL0) as instantaneous matter fraction.
Order parameter enhancement: (p(0)/p(z))^{2/3} = (OL0_eff_fraction_ratio)^{2/3}.

**Explicit formula B2 (operational)**:
```
omega_de(z) = OL0 * (1 + A * (1/(1+z)^2 - 1))
            = OL0 * (1 + A * ((1+z)^{-2} - 1))
```
where the 2/3 power applied to (rho_m0/rho_m)^{1/3} difference gives effective (1+z)^{-2} envelope.

Exact derivation: |Psi|^2 ~ (rho_threshold - rho_m)^{2/3}.
Set rho_threshold = rho_m0 * A_thresh (BEC occurs at z=0 marginally if A_thresh=1).
omega_de(z) = OL0 * [1 + A * (1 - (1+z)^3/A_thresh)^{2/3}]  for (1+z)^3 < A_thresh

**Final B2 formula**:
```
omega_de(z) = OL0 * (1 + A * max(1 - (1+z)^3, 0)^{2/3})
```
where we set A_thresh = 1 (BEC transition at z=0 by definition), with enhancement for z < 0 and omega_de(0) = OL0*(1+0) = OL0 exactly.

This means dark energy is exactly OL0 today and increases into the future (z < 0), decreasing into the past. With A controlling the present-epoch slope.

Generalized form for nontrivial past behavior: use A_thresh > 1.
```
omega_de(z) = OL0 * (1 + A * max(1 - (1+z)^3/A_thresh, 0)^{2/3})
```
At z=0: omega_de = OL0*(1 + A*(1 - 1/A_thresh)^{2/3}).
Normalize to OL0: divide by (1 + A*(1-1/A_thresh)^{2/3}).

**Normalized B2**:
```
omega_de(z) = OL0 * max(1 - (1+z)^3/A_thresh, 0)^{2/3} / (1 - 1/A_thresh)^{2/3}
```

Parameters: A_thresh > 1 (e.g., A_thresh = 2 means BEC transition was at z ~ 0.26).

---

## Theory B3: Bogoliubov Excitation Spectrum (zero-momentum occupation)

**Physical picture**: In a BEC, the Bogoliubov spectrum gives quasi-particle excitations.
Dark energy = occupation of the zero-momentum (k=0) mode.
Matter creates phonon excitations, depleting the k=0 mode exponentially.

Zero-momentum occupation: N_0 / N_total = exp(-A * rho_m(z) / rho_m0) in mean-field approximation (Bogoliubov depletion factor).

At z=0: N_0/N ∝ exp(-A).
At high z: N_0/N → 0 (all quanta excited by matter).

Normalize so that omega_de(0) = OL0:
  omega_de(z) = OL0 * exp(-A * rho_m(z)/rho_m0) / exp(-A)
              = OL0 * exp(-A * ((1+z)^3 - 1))

**Explicit formula B3**:
```
omega_de(z) = OL0 * exp(-A * ((1+z)^3 - 1))
```

Equivalently: omega_de(z) = OL0 * exp(A) * exp(-A*(1+z)^3)

Parameters: A > 0 (Bogoliubov depletion strength; A ~ 0.3-2).

At z=0: omega_de = OL0 (exact normalization).
At z=1: omega_de = OL0 * exp(-A*(8-1)) = OL0 * exp(-7A).
For A=0.1: omega_de(z=1)/OL0 = exp(-0.7) ≈ 0.497. Strong evolution.
For A=0.3: omega_de(z=1)/OL0 = exp(-2.1) ≈ 0.122. Very strong evolution.

This naturally gives wa << -1 in CPL fit since dark energy was much larger in the past... wait, actually it's *smaller* in the past (higher z = less dark energy). This gives phantom-like behavior in reverse: dark energy DECREASES going back in time → w > -1 (quintessence-like). Effective w_eff depends on how Hubble equation is affected.

**Note**: B3 gives dark energy that was *less* in the past (condensate was depleted by more matter), consistent with accelerated expansion onset at z ~ 0.3-0.7.

---

## Summary Table

| Theory | Formula | Parameters | Physical mechanism |
|--------|---------|------------|-------------------|
| B1 | `OL0 * max(1-(1+z)^{3/2}/sqrt(A), 0) / max(1-1/sqrt(A), 0)` | A>1 | Hard condensate threshold |
| B2 | `OL0 * max(1-(1+z)^3/A_thresh, 0)^{2/3} / (1-1/A_thresh)^{2/3}` | A_thresh>1 | Mean-field order parameter |
| B3 | `OL0 * exp(-A*((1+z)^3 - 1))` | A>0 | Bogoliubov zero-mode depletion |

## CPL Forecasts (qualitative)

- **B1**: Hard cutoff creates very steep w(z); effective wa could be << -1 but truncated.
- **B2**: Power-law 2/3 softens the transition; wa ~ -0.4 to -0.8 range plausible.
- **B3**: Pure exponential; mimics quintessence; wa ~ -0.2 to -0.5 depending on A.

## Fit to DESI DR1 Target

Goal: chi² < 11, wa < -0.5.
- B3 with A ~ 0.2-0.5 gives smooth growth: omega_de larger at z~0.5-1 → natural fit shape.
- B2 with A_thresh ~ 1.5 gives peaked behavior around z_c ~ 0.14 → check against D1.
- B1 cutoff too sharp; may overfit at low z.

Priority fit order: B3 > B2 > B1.
