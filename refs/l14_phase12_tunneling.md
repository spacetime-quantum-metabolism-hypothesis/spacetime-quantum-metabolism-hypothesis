# Phase 12: Quantum Tunneling / WKB Interpretation

## Phenomenological Interpretation of A1 and A2

**A1**: Spacetime quanta exist in localized potential wells (quantum phase = confined).
- Matter creates barriers between wells → suppresses tunneling → quanta become trapped (classical).
- Empty space = region of low potential barrier → tunneling freely → quantum coherent vacuum = dark energy.
- Matter annihilates quanta: raising barriers destroys inter-well coherence.
- Empty space creates quanta: lowering barriers restores coherence and spawns new tunneling paths.

**A2**: The quantum-classical boundary is derivable from A1.
- Derivation: boundary = the locus where tunneling rate Gamma_t → 0.
- When matter density is high (high z), barriers are tall → Gamma_t ≈ 0 → classical spacetime.
- When matter density is low (low z), barriers are low → Gamma_t > 0 → quantum coherent vacuum.

## Setup

WKB tunneling amplitude through a barrier of height V ~ rho_m(z) and width d:
  Gamma_t = exp(-2 * S_WKB)
  S_WKB = integral sqrt(2m*(V(x) - E)) dx ~ sqrt(V) * d ~ sqrt(rho_m(z)) * d_0

Setting d_0 absorbed into coefficient A:
  S_WKB(z) = A * sqrt(rho_m(z)/rho_m0) = A * sqrt((1+z)^3) = A * (1+z)^{3/2}

Dark energy = vacuum coherence maintained by tunneling:
  omega_de(z) ∝ Gamma_t(z) = exp(-2*A*(1+z)^{3/2})

---

## Theory Q1: WKB Tunneling Rate

**Physical picture**: Each spacetime quantum tunnels between adjacent void regions.
The tunneling probability (WKB) is suppressed by the square root of the matter density barrier.
Dark energy = the coherent tunneling amplitude squared across all spacetime quanta.

Raw tunneling rate:
  Gamma_t(z) = exp(-2 * S_WKB) = exp(-A * (1+z)^{3/2})
  [absorbing factor 2 into A]

Normalize to omega_de(0) = OL0:
  omega_de(z) = OL0 * Gamma_t(z) / Gamma_t(0)
              = OL0 * exp(-A*(1+z)^{3/2}) / exp(-A)
              = OL0 * exp(-A*((1+z)^{3/2} - 1))

**Explicit formula Q1**:
```
omega_de(z) = OL0 * exp(-A * ((1+z)^{3/2} - 1))
```

Parameters: A > 0 (WKB suppression coefficient; A ~ 0.3-2).

At z=0: omega_de = OL0 (exact).
At z=1: omega_de = OL0 * exp(-A*(2^{3/2}-1)) = OL0 * exp(-A*1.828).
For A=0.5: omega_de(z=1)/OL0 = exp(-0.914) ≈ 0.401.
For A=1.0: omega_de(z=1)/OL0 = exp(-1.828) ≈ 0.161.

Dark energy was smaller in the past (tunneling suppressed by higher matter density).
Onset of dark energy dominance controlled by A: sharper for larger A.
CPL effective wa: negative (quintessence-like), strength increases with A.

**Note on (1+z)^{3/2} vs (1+z)^3**: Q1 uses the square root WKB form, which gives slower growth than (1+z)^3. This means dark energy at z=1 is still nonzero, matching DESI sensitivity window.

---

## Theory Q2: Gamow Factor (Coulomb-analog tunneling)

**Physical picture**: Gamow factor from nuclear tunneling: S_G = pi * alpha_eff / v_rel.
In cosmological context: alpha_eff = coupling constant for spacetime quanta scattering off matter.
Relative velocity v_rel ~ thermal velocity of quanta ~ sqrt(T) ~ sqrt(1+z) (T ∝ 1+z for radiation-like bath).

Gamow tunneling rate:
  P_tunnel(z) = exp(-S_G(z)) = exp(-C / sqrt(1+z))

Dark energy baseline = OL0 (tunneling at z=0).
Enhancement at higher z: as z increases, v_rel decreases → S_G increases → tunneling suppressed.
But wait: v_rel ~ sqrt(1+z) means at higher z, thermal velocity is higher → S_G decreases → MORE tunneling? This gives dark energy increasing with z, consistent with DESI target.

Recheck: Gamow factor S_G = pi*Z1*Z2*e^2/(hbar*v). Higher temperature (higher z) → higher v → smaller S_G → larger tunneling rate.
So P_tunnel increases with z! This gives omega_de > OL0 at z > 0.

Baseline today: P_tunnel(0) = exp(-C).
At redshift z: P_tunnel(z) = exp(-C/sqrt(1+z)).

Normalize: omega_de(0) = OL0.
  omega_de(z) = OL0 * [1 + A * (exp(-C/sqrt(1+z)) - exp(-C))]

where A controls the enhancement amplitude and C controls the thermal velocity scale.

**Explicit formula Q2**:
```
omega_de(z) = OL0 * (1 + A * (exp(-C/sqrt(1+z)) - exp(-C)))
```

Parameters: A > 0 (amplitude of tunneling variation), C > 0 (Gamow coupling, C ~ 1-5).

At z=0: omega_de = OL0*(1 + A*(exp(-C) - exp(-C))) = OL0. (exact)
At z=1: omega_de = OL0*(1 + A*(exp(-C/sqrt(2)) - exp(-C))).
For C=2, A=1: enhancement = exp(-2/1.414) - exp(-2) = exp(-1.414) - exp(-2) = 0.2436 - 0.1353 = 0.108.
omega_de(z=1) = OL0 * 1.108. Modest enhancement (~11%).
For C=2, A=3: omega_de(z=1) = OL0 * 1.325.

This gives dark energy that was LARGER in the past, peaking at high z then saturating (Gamow factor saturates as v → infinity). Shape: rises from z=0 up, flattens at z >> (C^2) ~ 4 (for C=2).

This is the DESI-favored behavior: omega_de larger in the past, peaks around z~0.5-1.

**CPL estimate**: w0 ≈ -1, wa could be significantly negative (< -0.5) depending on A, C.

---

## Theory Q3: Resonant Tunneling (Lorentzian)

**Physical picture**: Spacetime quanta have a resonant tunneling condition: maximum transmission occurs when the matter density matches a resonant energy level rho_r. Off-resonance (either too high or too low matter density) → suppressed tunneling → less dark energy.

Resonant transmission probability (Breit-Wigner / Lorentzian):
  T_res(rho) = (Gamma_res^2) / ((rho_m - rho_r)^2 + Gamma_res^2)

where rho_r is the resonant density and Gamma_res is the resonance width.

In terms of z with rho_m(z) = Om*rho_crit0*(1+z)^3:
  Numerator: rho_r^2 (constant)
  Denominator: (rho_m(z) - rho_r)^2 + rho_r^2   [setting Gamma_res = rho_r for simplicity]

Or using the form from the prompt: Lorentzian in rho_m:
  T_res(z) = A * rho_m(z) / (rho_r^2 + rho_m(z)^2)

This peaks when rho_m = rho_r, i.e., (1+z_peak)^3 = rho_r / (Om*rho_crit0).

Normalize at z=0: T_res(0) can be nonzero.

**Explicit formula Q3** (as given in prompt, with normalization):
```
omega_de(z) = OL0 * (1 + A * rho_m(z) / (rho_r^2 + rho_m(z)^2))
```

Substituting rho_m(z) = Om*(1+z)^3 (in units of rho_crit0), and rho_r = B (resonant density parameter):
```
omega_de(z) = OL0 * (1 + A * Om*(1+z)^3 / (B^2 + (Om*(1+z)^3)^2))
```

Parameters: A > 0 (resonance strength), B > 0 (resonance scale density).

Normalize: divide by omega_de(0)/OL0 = 1 + A*Om/(B^2 + Om^2).

**Normalized Q3**:
```
f0 = 1 + A*Om / (B^2 + Om^2)
omega_de(z) = OL0 * (1 + A*Om*(1+z)^3 / (B^2 + (Om*(1+z)^3)^2)) / f0
```

Resonance peak at (1+z_peak) = (B/Om)^{1/3}.
For B=Om (peak at z=0): maximum today, decreasing into future and past.
For B=2*Om (peak at z ~ 0.26): dark energy peaked slightly in the past.
For B=8*Om (peak at z ~ 1): dark energy peaked around z=1, matching DESI preferred.

This form naturally produces a bump in omega_de at intermediate z, with suppression at both z=0 and z>>1.
Effective w(z) crosses -1 (phantom divide crossing): w > -1 before peak, w < -1 after peak.
Could give wa substantially negative.

---

## Summary Table

| Theory | Formula | Parameters | Shape |
|--------|---------|------------|-------|
| Q1 | `OL0 * exp(-A*((1+z)^{3/2} - 1))` | A>0 | Monotone decrease into past |
| Q2 | `OL0 * (1 + A*(exp(-C/sqrt(1+z)) - exp(-C)))` | A,C>0 | Monotone increase into past, saturates |
| Q3 | `OL0 * (1 + A*Om*(1+z)^3/(B^2+(Om*(1+z)^3)^2)) / (1 + A*Om/(B^2+Om^2))` | A,B>0 | Peaked at z_peak=(B/Om)^{1/3}-1 |

## CPL Forecasts (qualitative)

- **Q1**: wa ~ -0.2 to -0.6 (quintessence, smaller dark energy in past).
- **Q2**: wa ~ -0.3 to -0.8 (dark energy larger in past, Gamow saturation). Best DESI candidate.
- **Q3**: wa depends on resonance position. If z_peak ~ 0.5-1, could give wa ~ -0.5 to -1.5.

## Priority for Fitting

Q2 and Q3 give dark energy larger in the past → match DESI DR1 preference for wa < 0.
Q2 > Q3 > Q1 for expected chi² improvement over ΛCDM.
