# Phase 20: Discrete Quantum Walk

**Axiom A1**: Matter annihilates spacetime quanta; empty space creates them.
**Axiom A2**: Quantum-classical boundary derivable from A1.

Interpretation: Spacetime quanta undergo discrete quantum walk on a graph. Matter = absorbing nodes. Empty space = walk source. Quantum-classical boundary = Anderson localization transition.

---

## W1: Grover Search Analog — Sqrt-Linear from Quantum Speedup

**Physical basis**: Grover's algorithm finds one marked (matter-absorbed) node among N nodes with probability ~ 1/sqrt(N) per step. N_matter ~ rho_m. Quantum walk survival probability ~ 1/sqrt(N_matter). Dark energy = density of non-absorbed (quantum) spacetime nodes.

**Derivation**: Fraction of quantum sites ~ 1/sqrt(N_matter). In redshift: N_matter(z) ~ Om*(1+z)³/OL0 (dimensionless matter density in dark energy units). Quantum walk speedup gives sqrt enhancement over classical diffusion. Dark energy tracks quantum site density with sqrt(1-matter_fraction) correction.

**omega_de(z)**:
```
omega_de(z) = OL0 * (1 + A * Om * (1 - (1+z)^(-1/2)))
```

Note: at z=0, (1-(1+0)^{-1/2}) = 0, so omega_de(0) = OL0. Correct.
At high z: (1-(1+z)^{-1/2}) → 1, so omega_de → OL0*(1+A*Om).

For A < 0 (absorbing nodes reduce dark energy):
```
omega_de(z) = OL0 * (1 - A * Om * (1 - (1+z)^(-1/2)))
```

More natural form using sqrt(1+z) - 1:
**omega_de(z) [final]**:
```
omega_de(z) = OL0 * (1 + A * Om * (1 - 1/sqrt(1+z)))
```
with A < 0 for dark energy suppression at high z (wa < 0).

**Free parameters**: A (Grover coupling), Om, OL0.

---

## W2: Anderson Localization — Exponential Suppression at High z Lifts

**Physical basis**: Anderson localization: quantum walk localizes when disorder (matter density) exceeds threshold. Localization length xi_loc ~ exp(1/rho_m). At high z (large rho_m), xi_loc → 0 — completely localized (classical). At low z, xi_loc → ∞ — extended quantum spacetime. Dark energy ~ delocalized walk probability.

**Derivation**: Delocalized probability ~ exp(-1/xi_loc) ~ exp(-exp(-1/rho_m)). Simplified: localization factor = 1 - exp(-xi_loc(z)) = 1 - exp(-exp(1/(Om*(1+z)³))). More tractable form: use xi_loc ~ exp(-B*(1+z)³), so delocalization probability ~ 1 - exp(-exp(-B*(1+z)³)).

Dark energy enhanced when delocalized. Difference from z=0 value:
```
omega_de(z) = OL0 * (1 + A * (exp(-B*(1+z)³) - exp(-B)))
```

At z=0: OL0*(1 + A*(exp(-B) - exp(-B))) = OL0. Correct.
At large z: exp(-B*(1+z)³) → 0, so omega_de → OL0*(1 - A*exp(-B)).

For A > 0: dark energy decreases at high z (B sets the localization scale today).

**omega_de(z) [final]**:
```
omega_de(z) = OL0 * (1 + A * (exp(-B*(1+z)³) - exp(-B)))
```

**Free parameters**: A (localization amplitude), B (disorder scale), Om, OL0.

---

## W3: Quantum Walk Spread — Linear Variance (Not Diffusive)

**Physical basis**: Classical random walk: position variance ~ t². Quantum walk: variance ~ t (linear, ballistic). Survival probability at origin S(t) ~ 1/t for quantum walk vs 1/sqrt(t) classical. In cosmological time: t ~ 1/H(z). Dark energy ~ S(H(z)) ~ H(z) ~ (1+z)^{3/2} suppression at high z via quantum walk return probability.

**Derivation**: Quantum walk survival probability at origin: S(z) ~ H(z)/H0 = E(z) (return to origin harder when Hubble rate faster). But dark energy should decrease at high z, so omega_de ~ 1/E(z) ~ 1/(1+z)^{3/2} (matter-dominated). Rational form with matter density:

**omega_de(z)**:
```
omega_de(z) = OL0 / (1 + A * Om*(1+z)^(3/2)/OL0)
```

At z=0: OL0/(1+A*Om/OL0). Normalized:
```
omega_de(z) = OL0 * (OL0 + A*Om) / (OL0 + A*Om*(1+z)^(3/2))
```

At z=0: OL0*(OL0+A*Om)/(OL0+A*Om) = OL0. Correct.

Note: Uses (1+z)^{3/2} (quantum walk linear spread ~ sqrt(matter) growth) instead of (1+z)^3 (classical matter). Slower growth → stronger dark energy at high z → more negative wa.

**omega_de(z) [final]**:
```
omega_de(z) = OL0 * (OL0 + A*Om) / (OL0 + A*Om*(1+z)^(3/2))
```

**Free parameters**: A (quantum walk coupling), Om, OL0.

---

## Summary Table

| Theory | omega_de(z) | Key feature |
|--------|------------|-------------|
| W1 | OL0*(1+A*Om*(1-1/sqrt(1+z))) | Grover sqrt speedup, A<0 for quintessence |
| W2 | OL0*(1+A*(exp(-B*(1+z)³)-exp(-B))) | Anderson localization, exponential |
| W3 | OL0*(OL0+A*Om)/(OL0+A*Om*(1+z)^(3/2)) | Quantum walk 3/2 power, slower dilution |
