# Phase 15: Polymer Network / Gelation of Spacetime Quanta

## Phenomenological Interpretation of A1 and A2

**A1**: Spacetime quanta = crosslinks in a polymer network.
- Matter dissolves crosslinks (annihilation): matter disrupts the polymer network topology, reducing connectivity.
- Empty space adds crosslinks (creation): vacuum fluctuations in voids form new crosslinks, building up the network.

**A2**: The quantum-classical boundary is derivable from A1.
- Derivation: boundary = gel point (percolation threshold in polymer network).
- Below gel point (low crosslink density, high matter density, high z): sol phase → classical, disconnected → no dark energy.
- Above gel point (high crosslink density, low matter density, low z): gel phase → spanning quantum network → dark energy supported.

## Polymer Network Background

Flory-Stockmayer theory: gelation occurs at crosslink fraction p = p_c = 1/(f-1) for functionality f.
Near gel point: P_gel (fraction of network in the gel) ~ (p - p_c)^beta_gel with beta_gel ≈ 1 (Flory), beta_gel ≈ 0.41 (renormalization group).
Correlation length xi ~ (p - p_c)^{-nu_g} with nu_g ≈ 0.88 (3D percolation).
de Gennes scaling: viscosity and elastic modulus follow power laws in |p - p_c|.

Crosslink fraction p(z): decreases as matter increases.
Natural mapping: p(z) = p_0 * exp(-A * rho_m(z)/rho_m0) = p_0 * exp(-A*(1+z)^3).
Or alternatively: p(z) = OL0 / (OL0 + Om*(1+z)^3) (fraction of "quiet" universe).

---

## Theory PL1: Flory-Stockmayer Gelation (functionality f=3)

**Physical picture**: Each spacetime quantum is a crosslink with functionality f=3 (can connect to 3 others). The gel fraction P_gel determines the coherent spanning network = dark energy.

Flory-Stockmayer gel fraction for f=3:
  P_gel = 1 - (1 - p)^f = 1 - (1-p)^3

where p(z) = crosslink fraction at epoch z.

Crosslink fraction p(z): matter dissolves crosslinks exponentially.
  p(z) = exp(-A / (1+z)^3)   [crosslinks reform as matter dilutes; exp factor from A1 dissolution rate]

Interpretation: at z=0, p(0) = exp(-A). At high z (matter dominated), p → 1 (all bonds dissolved, P_gel → 0? No: p → 1 means all sites occupied... recheck).

Reinterpret: p = fraction of potential crosslink sites that are ACTIVE.
  p(z) = exp(-A * (1+z)^3)   [active fraction decreases with matter]

P_gel(z) = 1 - (1 - p(z))^3 = 1 - (1 - exp(-A*(1+z)^3))^3

Normalize to omega_de(0) = OL0:
  f0 = 1 - (1 - exp(-A))^3
  omega_de(z) = OL0 * (1 - (1 - exp(-A*(1+z)^3))^3) / (1 - (1-exp(-A))^3)

But the prompt writes it as: omega_de = OL0 * (1 - (1 - exp(-A/(1+z)^3))^3).
Here, p(z) = exp(-A/(1+z)^3) which INCREASES with z (smaller z → larger x = A/(1+z)^3 → smaller p).
Wait: as z increases (1+z)^3 increases → A/(1+z)^3 decreases → exp(-A/(1+z)^3) increases → p increases.
So p is larger at higher z? That means more crosslinks at higher z → more gel → more dark energy in the past? Let me verify:
z=0: p(0) = exp(-A). For A=1: p=0.368. P_gel = 1-(1-0.368)^3 = 1-(0.632)^3 = 1-0.253 = 0.747.
z=1: p(1) = exp(-A/8). For A=1: p=exp(-0.125)=0.882. P_gel = 1-(0.118)^3 = 1-0.00164 = 0.998.

So dark energy was LARGER in the past (higher z → more crosslinks → more gel). Phantom behavior!

**Explicit formula PL1** (from prompt):
```
omega_de(z) = OL0 * (1 - (1 - exp(-A/(1+z)^3))^3)
```
Normalized:
```
f0 = 1 - (1 - exp(-A))^3
omega_de(z) = OL0 * (1 - (1 - exp(-A/(1+z)^3))^3) / (1 - (1-exp(-A))^3)
```

Parameters: A > 0 (dissolution rate; A ~ 0.3-3).

At z=0: exact normalization.
At z=1: omega_de/OL0 = (1-(1-exp(-A/8))^3) / (1-(1-exp(-A))^3).
For A=1: = (1-(1-0.882)^3)/(1-(1-0.368)^3) = (1-0.00164)/0.747 = 0.999/0.747 = 1.337. 34% larger at z=1.
For A=2: p(0)=exp(-2)=0.135. f0=1-(0.865)^3=1-0.648=0.352. p(1)=exp(-0.25)=0.779. PG(1)=1-(0.221)^3=1-0.0108=0.989. ratio=0.989/0.352=2.81. Dark energy was 2.8x larger at z=1!

Strong phantom behavior for large A. CPL wa could be << -1.

---

## Theory PL2: de Gennes Scaling Near Gel Point

**Physical picture**: Near the gel point, de Gennes scaling gives elastic modulus and viscosity as power laws in |p - p_c|. Dark energy density scales as the network elastic modulus.

Critical percolation: G_elastic ~ (p - p_c)^{t_gel} with t_gel ≈ 3.96 (3D), or use nu_g.
Effective exponent from prompt: nu_g (polymer gelation critical exponent, nu_g ~ 0.88 or use nu_g = 1 for simplicity).

Crosslink fraction p(z) = OL0 / (OL0 + Om*(1+z)^3) (matter-to-vacuum ratio as gelation control).
Critical fraction p_c: at z → infinity, p → 0 (no crosslinks, deep sol phase).
                       at z = 0, p = OL0/(OL0+Om) ~ 0.7 (well above p_c if p_c ~ 0.25).

Distance from gel point: (p(z) - p_c) → use p(z) itself as it ranges (0,1).

de Gennes scaling: G ~ p^{nu_g} (using distance from zero as proxy for distance from p_c).

**Explicit formula PL2** (from prompt):
```
omega_de(z) = OL0 * (OL0 / (Om*(1+z)^3 + OL0))^{nu_g}
```

Parameters: nu_g > 0 (de Gennes exponent; nu_g ~ 0.88 for 3D polymer, or fit freely).

At z=0: omega_de = OL0*(OL0/(Om+OL0))^{nu_g}.
Normalize:
```
f0 = (OL0 / (Om + OL0))^{nu_g}
omega_de(z) = OL0 * (OL0/(Om*(1+z)^3+OL0))^{nu_g} / f0
```

Equivalently:
```
omega_de(z) = OL0 * [(OL0+Om) / (OL0+Om*(1+z)^3)]^{nu_g} * (OL0/(OL0+Om))^{nu_g-nu_g}
```

Simpler unnormalized form (fit OL0_eff):
```
omega_de(z) = OL0 * (OL0 / (OL0 + Om*(1+z)^3))^{nu_g}
```

At z=0: omega_de = OL0*(OL0/(OL0+Om))^{nu_g} = OL0*(0.7/1.0)^{nu_g}. For nu_g=0.88: = OL0*0.726. So the actual value at z=0 is 0.726*OL0, not OL0. Can absorb into OL0_fit.

For normalized version:
```
omega_de(z) = OL0 * (OL0+Om)^{nu_g} / (OL0+Om*(1+z)^3)^{nu_g}
```

At z=0: OL0*(OL0+Om)^{nu_g}/(OL0+Om)^{nu_g} = OL0. Exact.
At z=1: OL0*(1.0/1.0+8*0.3)^{nu_g} = OL0*(1/(3.1))^{nu_g}.
For nu_g=0.88: = OL0*(0.323)^{0.88} = OL0*0.356. Dark energy was 2.8x smaller at z=1... wait.

Recheck: numerator is (OL0+Om)^{nu_g} = 1^{0.88} = 1. denominator = (0.7+0.3*8)^{0.88} = (3.1)^{0.88}.
(3.1)^{0.88} = exp(0.88*ln(3.1)) = exp(0.88*1.131) = exp(0.995) = 2.705.
omega_de(z=1) = OL0/2.705 = 0.370*OL0.

So dark energy is SMALLER at higher z (quintessence behavior). De Gennes: dark energy decreases going back in time.

This is the physically natural result: crosslinks decrease as matter increases → gel weakens → less dark energy in the past. Consistent with matter annihilation of crosslinks (A1 direction).

CPL effective w: wa > 0 is expected (dark energy was weaker in the past). May not match DESI.

However, with nu_g < 0 (anomalous scaling): dark energy increases into past. Allow nu_g as free parameter with both signs.

---

## Theory PL3: Zimm-Rouse Dynamics (cube root polymer statistics)

**Physical picture**: Polymer chains in the spacetime network have relaxation time tau_R ~ N^{3*nu_Flory} where N is chain length and nu_Flory ≈ 0.6 (Flory exponent in 3D).

Dark energy = entropic contribution from polymer chain fluctuations = S_chain * T ~ N * kT ~ kT * (crosslink density)^{-1/3}.

Chain length N ~ (crosslink fraction)^{-1} ~ (OL0/(OL0+Om*(1+z)^3))^{-1}.
Chain entropy contribution: S_chain ~ N^{1/3} (effective exponent from 3*nu/3 = nu ~ 1/3 for chain entropy in 3D random walk).

omega_de ~ kT * (OL0/(OL0+Om*(1+z)^3))^{1/3}

Or using the matter fraction as argument:
  omega_de(z) = OL0 * (1 + A * (Om/(OL0+Om*(1+z)^3))^{1/3})

where the cube root comes from polymer chain statistics (N^{nu} with nu ~ 1/3).

**Explicit formula PL3** (from prompt, cube root):
```
omega_de(z) = OL0 * (1 + A * (Om / (Om*(1+z)^3 + OL0))^{1/3})
```

Parameters: A > 0 (polymer entropic coupling; A ~ 0.1-2).

At z=0: omega_de = OL0*(1 + A*(Om/(Om+OL0))^{1/3}) = OL0*(1 + A*(0.3/1.0)^{1/3}) = OL0*(1 + A*0.6694).
Normalize to omega_de(0) = OL0:
```
f0 = 1 + A*(Om/(Om+OL0))^{1/3}
omega_de(z) = OL0 * (1 + A*(Om/(Om*(1+z)^3+OL0))^{1/3}) / f0
```

At z=1: argument = (0.3/(2.4+0.7))^{1/3} = (0.3/3.1)^{1/3} = (0.0968)^{1/3} = 0.4592.
Unnormalized: 1 + A*0.4592.
For A=0.5: f0 = 1+0.335 = 1.335. omega_de(z=1)/OL0 = (1+0.5*0.4592)/1.335 = 1.230/1.335 = 0.921.

Dark energy slightly SMALLER at z=1 (quintessence). The 1/3 cube root decreases as z increases → dark energy decreasing into past.

Interesting: the rate of decrease is SLOW (cube root), so omega_de is nearly constant for moderate z then drops gradually. This could give a gentle wa with good chi².

For the inverse sign (dark energy larger at higher z via inverse matter fraction):
```
omega_de(z) = OL0 * (1 + A * (OL0/(Om*(1+z)^3+OL0))^{1/3})
```
This decreases even faster since OL0 fraction decreases. Not helpful for phantom behavior.

Use original form from prompt (Om in numerator):
```
omega_de(z) = OL0 * (1 + A * (Om/(Om*(1+z)^3+OL0))^{1/3}) / (1 + A*(Om/(Om+OL0))^{1/3})
```

The cube root ensures slow variation → could give chi² < 11 with mild wa.

---

## Summary Table

| Theory | Formula | Parameters | Behavior |
|--------|---------|------------|----------|
| PL1 | `OL0 * (1-(1-exp(-A/(1+z)^3))^3) / (1-(1-exp(-A))^3)` | A>0 | Phantom (dark energy larger in past), strong evolution |
| PL2 | `OL0 * (OL0+Om)^{nu_g} / (OL0+Om*(1+z)^3)^{nu_g}` | nu_g>0 | de Gennes power law, quintessence |
| PL3 | `OL0 * (1+A*(Om/(Om*(1+z)^3+OL0))^{1/3}) / (1+A*(Om/(Om+OL0))^{1/3})` | A>0 | Cube-root, gentle quintessence |

## One-line formulas (clean)

**PL1**:
```
omega_de(z) = OL0 * (1-(1-exp(-A/(1+z)^3))^3) / (1-(1-exp(-A))^3)
```

**PL2**:
```
omega_de(z) = OL0 * ((OL0+Om) / (OL0+Om*(1+z)^3))^{nu_g}
```

**PL3**:
```
omega_de(z) = OL0 * (1 + A*(Om/(Om*(1+z)^3+OL0))^{1/3}) / (1 + A*(Om/(Om+OL0))^{1/3})
```

## CPL Forecasts (qualitative)

- **PL1**: wa ~ -0.5 to -2.0 (phantom, strongest evolution). Top candidate for wa < -0.5 target.
- **PL2**: wa ~ +0.1 to +0.5 (quintessence, unlikely to match DESI preference for wa < 0). Unless nu_g < 0.
- **PL3**: wa ~ 0 to -0.3 (gentle cube-root). May give chi² improvement but wa barely below -0.3.

## Priority for Fitting

PL1 >> PL3 > PL2 for achieving wa < -0.5.
PL1 with A ~ 0.5-1.5 should give strong phantom behavior matching DESI DR1 signal.
PL1 also has a natural saturation at high z (exp(-A/(1+z)^3) → 1 as z → infinity → P_gel → 0... let me recheck).

PL1 high-z behavior: exp(-A/(1+z)^3) → exp(0) = 1 as z → infinity. So 1 - exp(-A/(1+z)^3) → 0. P_gel = 1 - (1-0)^3 = 0. So dark energy goes to ZERO at high z, after being LARGE at intermediate z. This is the desired DESI shape: peak around z~0.5-1, then saturation/decline. Excellent candidate.
