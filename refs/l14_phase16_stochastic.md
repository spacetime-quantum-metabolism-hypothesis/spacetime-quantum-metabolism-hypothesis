# Phase 16: Stochastic Gravity / Noise-Induced Transitions

**Axiom A1**: Matter annihilates spacetime quanta; empty space creates them.
**Axiom A2**: Quantum-classical boundary derivable from A1.

Interpretation: Spacetime quanta subject to vacuum noise. Matter = dissipation source. Empty space = fluctuation source. Quantum-classical boundary = stochastic resonance threshold.

---

## N1: Fokker-Planck Stationary Distribution

**Physical basis**: Spacetime quantum density n evolves via Fokker-Planck equation with drift (matter-induced dissipation) and diffusion (vacuum fluctuations). Stationary distribution P_st(n) ∝ exp(-V_eff(n)/D) where matter increases effective potential V_eff, suppressing quantum density.

**Derivation**: Effective potential V_eff(n) = (Omega_m(z) - Omega_m0) * n where Omega_m(z) = Om*(1+z)³/E_LCDM²(z). Dark energy density tracks exp(-V_eff/D), normalized to OL0 at z=0.

**omega_de(z)**:
```
omega_de(z) = OL0 * exp(-A * (Omega_m(z) - Om0))
```
where `Omega_m(z) = Om*(1+z)³ / E_LCDM²(z)`, `E_LCDM²(z) = Om*(1+z)³ + OL0`, and A > 0 is noise coupling.

At z=0: Omega_m(0) = Om0, so exp(0) = 1, giving omega_de(0) = OL0. Correct normalization.
At high z: Omega_m(z) → 1, potential deepens, omega_de suppressed — dark energy dilutes.

**Free parameters**: A (noise coupling strength), Om, OL0.

---

## N2: Noise-Induced Phase Transition

**Physical basis**: Order parameter phi ~ exp(-D/epsilon) where D = noise amplitude, epsilon = inverse matter density ~ 1/rho_m. Phase transition occurs when noise amplitude matches matter-set barrier height. Dark energy is the order parameter of the quantum spacetime phase.

**Derivation**: epsilon(z) ~ OL0 / (Om*(1+z)³ + OL0) = f_de(z), fraction of dark energy. As z increases, f_de decreases, epsilon decreases, order parameter phi → 0 (classical phase). omega_de tracks phi.

**omega_de(z)**:
```
omega_de(z) = OL0 * exp(-A * OL0 / (Om*(1+z)³ + OL0))
```
where A > 0. At z=0: argument = -A*OL0/(OL0+Om*(1+z=0)³) evaluated... note this does NOT give OL0 at z=0 unless normalized. Normalized form:

```
omega_de(z) = OL0 * exp(-A * OL0 / (Om*(1+z)³ + OL0)) / exp(-A * OL0 / (Om + OL0))
```

Simplified single-parameter form (absorbing normalization into A):
```
omega_de(z) = OL0 * exp(A * (OL0/(Om*(1+z)³ + OL0) - OL0/(Om + OL0)))
```

**Free parameters**: A (barrier height / noise ratio), Om, OL0.

---

## N3: Stochastic Resonance — Gaussian Peak in H

**Physical basis**: Stochastic resonance maximizes dark energy output when noise amplitude D matches signal frequency ~ H(z). Signal-to-noise ratio peaks at H(z)/H0 = 1 (today), falls off at higher and lower H. Gaussian peak in H-ratio.

**Derivation**: Resonance condition: maximum response when driving frequency = H0. Dark energy enhanced near resonance, suppressed away from it. At high z, H >> H0, far from resonance, omega_de suppressed.

**omega_de(z)**:
```
omega_de(z) = OL0 * (1 + A * (H(z)/H0) * exp(-B * (H(z)/H0 - 1)²))
```
where `H(z)/H0 = E(z) = sqrt(Om*(1+z)³ + OL0)` (LCDM background), A > 0 is resonance amplitude, B > 0 is resonance width.

At z=0: E(0) = 1, so `1 + A*1*exp(0) = 1 + A`. Not OL0 unless A=0. Normalized:
```
omega_de(z) = OL0 * (1 + A*(E(z)-1)*exp(-B*(E(z)-1)²))
```
This gives omega_de(0) = OL0*(1+0) = OL0. Correct.

**Free parameters**: A (resonance strength), B (resonance width), Om, OL0.

---

## Summary Table

| Theory | omega_de(z) | wa character |
|--------|------------|--------------|
| N1 | OL0*exp(-A*(Omega_m(z)-Om0)) | Decreasing with z, wa < 0 |
| N2 | OL0*exp(A*(f_de(z)-f_de(0))) | Mild evolution, wa ~ -0.1 to -0.5 |
| N3 | OL0*(1+A*(E(z)-1)*exp(-B*(E(z)-1)²)) | Non-monotone, resonance peak |
