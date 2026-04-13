# Phase 18: Quantum Error Correction (QEC)

**Axiom A1**: Matter annihilates spacetime quanta; empty space creates them.
**Axiom A2**: Quantum-classical boundary derivable from A1.

Interpretation: Spacetime quanta = logical qubits in a QEC code. Matter = errors decohering qubits. Empty space = syndrome measurement + correction. Quantum-classical boundary = error threshold p_th.

---

## QE1: Below/Above Error Threshold

**Physical basis**: QEC codes have threshold p_th: below threshold, errors correctable and quantum spacetime survives; above threshold, errors cascade and spacetime becomes classical. Error probability p_error(z) = 1 - exp(-A*Omega_m(z)*(1+z)³) grows with matter density. Dark energy = logical qubit survival fraction, proportional to max(1 - p_error/p_th, 0)^nu.

**Derivation**: Error rate from matter density: p_error(z) = 1 - exp(-A*Om*(1+z)³). Quantum spacetime dark energy density ~ fraction of correctable code space. With nu=1 (linear falloff) and p_th ~ 0.1 (standard surface code threshold):

**omega_de(z)**:
```
omega_de(z) = OL0 * max(1 - (1 - exp(-A*Om*(1+z)³))/p_th, 0)
```

At z=0: 1 - (1-exp(-A*Om))/p_th. Normalized (define A such that at z=0, expression=1):
```
omega_de(z) = OL0 * (exp(-A*Om*(1+z)³) - exp(-A*Om*(1+z)³_max)) / (exp(-A*Om) - ...)
```

Practical form (set p_th to enforce omega_de(0) = OL0):
```
omega_de(z) = OL0 * exp(-A*Om*(1+z)³) / exp(-A*Om)
           = OL0 * exp(-A*Om*((1+z)³ - 1))
```
This is the correctable code fraction normalized to today.

**omega_de(z) [final]**:
```
omega_de(z) = OL0 * exp(-A * Om * ((1+z)³ - 1))
```

**Free parameters**: A (error rate coupling ~ 1/p_th), Om, OL0.

---

## QE2: Toric Code Threshold — Tanh Transition

**Physical basis**: Toric code has sharp threshold at p_c. Near threshold, logical error rate transitions sharply: below → 0, above → 1. This maps to tanh(B*(p - p_c)). Matter density drives p(z). Dark energy is suppressed above threshold via tanh transition.

**Derivation**: p(z) ~ Om*(1+z)³/OL0 (ratio of matter to dark energy). When matter dominates, p large, tanh → -1, dark energy suppressed. When dark energy dominates (z~0), p small, tanh → +A, dark energy enhanced.

**omega_de(z)**:
```
omega_de(z) = OL0 * (1 + A * tanh(-B * Om*(1+z)³/OL0))
```

At z=0: OL0*(1 + A*tanh(-B*Om/OL0)). Normalized:
```
omega_de(z) = OL0 * (1 + A*tanh(-B*Om*(1+z)³/OL0)) / (1 + A*tanh(-B*Om/OL0))
```

The tanh is negative for all z>0 (matter density positive), so this gives monotonically decreasing omega_de with z. A > 0 for enhancement today (wa < 0 behavior).

**Free parameters**: A (transition amplitude), B (threshold sharpness), Om, OL0.

---

## QE3: Surface Code Distance — Double Exponential Suppression

**Physical basis**: Surface code distance d scales as d ~ 1/sqrt(p_error). Logical error rate ~ exp(-alpha*d) ~ exp(-alpha/sqrt(p_error)). Dark energy = logical qubit survival = exp(-logical error rate). Double exponential: outer exp from logical error rate, inner exp from physical error rate vs matter density.

**Derivation**: Physical error probability p_error(z) = 1 - exp(-B*Om*(1+z)³). Code distance d ~ 1/sqrt(p_error). Logical error rate ~ exp(-A/sqrt(p_error)) ~ exp(-A/sqrt(1-exp(-B*Om*(1+z)³))). Dark energy ~ exp(-logical error rate).

**omega_de(z)**:
```
omega_de(z) = OL0 * exp(-A * (1 - exp(-B * Om*(1+z)³)))
```

At z=0: OL0*exp(-A*(1-exp(-B*Om))). Normalized:
```
omega_de(z) = OL0 * exp(-A*(1-exp(-B*Om*(1+z)³))) / exp(-A*(1-exp(-B*Om)))
           = OL0 * exp(A*(exp(-B*Om*(1+z)³) - exp(-B*Om)))
```

At z=0: exp(A*(1-1)) = 1. Correct normalization.

**omega_de(z) [final]**:
```
omega_de(z) = OL0 * exp(A * (exp(-B*Om*(1+z)³) - exp(-B*Om)))
```

**Free parameters**: A (logical error suppression), B (physical error rate), Om, OL0.

---

## Summary Table

| Theory | omega_de(z) | Key feature |
|--------|------------|-------------|
| QE1 | OL0*exp(-A*Om*((1+z)³-1)) | Simple exponential in matter growth |
| QE2 | OL0*(1+A*tanh(-B*Om*(1+z)³/OL0))/(1+A*tanh(-B*Om/OL0)) | Sharp threshold transition |
| QE3 | OL0*exp(A*(exp(-B*Om*(1+z)³)-exp(-B*Om))) | Double exponential, rapid early suppression |
