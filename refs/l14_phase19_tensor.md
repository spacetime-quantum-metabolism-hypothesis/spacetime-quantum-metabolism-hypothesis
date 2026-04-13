# Phase 19: Tensor Network / MERA

**Axiom A1**: Matter annihilates spacetime quanta; empty space creates them.
**Axiom A2**: Quantum-classical boundary derivable from A1.

Interpretation: Spacetime = MERA (Multi-scale Entanglement Renormalization Ansatz) tensor network. Matter removes tensors (renormalization coarse-graining). Empty space adds fine-grained tensors. Quantum-classical boundary = entanglement cut becoming trivial.

---

## TN1: MERA Entanglement Entropy — Log Scale Growth

**Physical basis**: MERA entanglement entropy grows logarithmically with the number of coarse-graining layers n. At scale H(z), the UV cutoff sets number of active layers. Dark energy = entanglement between active tensor network scales, which grows as log(H(z)/H0) = log(E(z)).

**Derivation**: At redshift z, Hubble scale H(z) = H0*E(z). MERA layers active: n(z) ~ log(H(z)/H0) = log(E(z)). Entanglement entropy per layer is constant (c/3 in CFT). Dark energy ~ entanglement of active layers relative to today.

**omega_de(z)**:
```
omega_de(z) = OL0 * (1 + A * ln(E_LCDM(z)))
```
where `E_LCDM(z) = sqrt(Om*(1+z)³ + OL0)` and E_LCDM(0) = 1 so ln(E(0)) = 0.

At z=0: OL0*(1+0) = OL0. Correct normalization automatically.

For z > 0: E(z) > 1, ln(E(z)) > 0, so A > 0 gives omega_de > OL0 (dark energy grows — phantom-like). For wa < 0 (quintessence), need A < 0: dark energy decreases as z increases. But ln(E(z)) > 0 for z>0, so A < 0 gives suppression at high z.

**omega_de(z) [final]**:
```
omega_de(z) = OL0 * (1 + A * ln(sqrt(Om*(1+z)³ + OL0)))
```
with A < 0 for quintessence-like behavior.

**Free parameters**: A (entanglement coupling), Om, OL0.

---

## TN2: Bond Dimension — Rational Decay

**Physical basis**: MERA bond dimension chi quantifies entanglement capacity between network layers. Matter removes tensors (A1 annihilation), reducing effective bond dimension. chi(z) decreases as matter density increases, suppressing dark energy.

**Derivation**: Bond dimension chi(z) = chi_0 / (1 + A*rho_m(z)/rho_de) = chi_0 / (1 + A*Om*(1+z)³/OL0). Dark energy density proportional to chi(z)/chi_0.

**omega_de(z)**:
```
omega_de(z) = OL0 / (1 + A * Om*(1+z)³/OL0)
```

At z=0: OL0/(1+A*Om/OL0). Normalized:
```
omega_de(z) = OL0 * (1 + A*Om/OL0) / (1 + A*Om*(1+z)³/OL0)
```

Let C = 1 + A*Om/OL0:
```
omega_de(z) = OL0 * C / (1 + A*Om*(1+z)³/OL0)
```

At z=0: OL0*C/C = OL0. Correct.

**omega_de(z) [final]**:
```
omega_de(z) = OL0 * (OL0 + A*Om) / (OL0 + A*Om*(1+z)³)
```

**Free parameters**: A (bond dimension coupling), Om, OL0.

---

## TN3: Causal Cone / Power of Hubble

**Physical basis**: MERA causal cone width grows as 2^n_layers with the number of coarse-graining steps. At scale H(z), the number of layers n ~ log(H(z)/H0)/log(2). Dark energy is inversely suppressed by causal cone volume growth: omega_de ~ E(z)^{-A} where A > 0.

**Derivation**: Causal cone volume ~ 2^(A*n_layers) = 2^(A*log2(E(z))) = E(z)^A. Dark energy density ~ 1/causal_cone_volume ~ E(z)^{-A}. Normalization: at z=0, E(0)=1, so omega_de(0) = OL0.

**omega_de(z)**:
```
omega_de(z) = OL0 * E_LCDM(z)^(-A)
           = OL0 * (Om*(1+z)³ + OL0)^(-A/2)
```

At z=0: OL0*(Om+OL0)^(-A/2). Normalized (multiply by (Om+OL0)^(A/2)):
```
omega_de(z) = OL0 * ((Om + OL0) / (Om*(1+z)³ + OL0))^(A/2)
```

For A > 0: omega_de decreases as z increases (E(z) grows). This gives wa < 0 behavior.

**omega_de(z) [final]**:
```
omega_de(z) = OL0 * ((Om + OL0) / (Om*(1+z)³ + OL0))^(A/2)
```

**Free parameters**: A (causal cone exponent), Om, OL0.

---

## Summary Table

| Theory | omega_de(z) | Key feature |
|--------|------------|-------------|
| TN1 | OL0*(1+A*ln(sqrt(Om*(1+z)³+OL0))) | Logarithmic in Hubble, A<0 for quintessence |
| TN2 | OL0*(OL0+A*Om)/(OL0+A*Om*(1+z)³) | Rational decay, bond dimension |
| TN3 | OL0*((Om+OL0)/(Om*(1+z)³+OL0))^(A/2) | Power law in E², causal cone |
