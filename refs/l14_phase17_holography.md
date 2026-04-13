# Phase 17: Holography + Ryu-Takayanagi (RT) Formula

**Axiom A1**: Matter annihilates spacetime quanta; empty space creates them.
**Axiom A2**: Quantum-classical boundary derivable from A1.

Interpretation: Spacetime quanta = RT surface area elements. Matter = bulk excitation reducing minimal surface area (annihilation = area loss). Empty space creates minimal surfaces. Quantum-classical boundary = RT area → 0.

---

## H1: RT Area Scaling — AdS Radius Suppressed by Matter

**Physical basis**: In AdS/CFT, RT minimal surface area S_RT ~ L^(d-2) where L is AdS radius. Matter (bulk excitations) reduce L via back-reaction: L ~ 1/rho_m^(1/3). Dark energy density tracks RT surface quantum density ~ S_RT/V ~ L^(d-2)/L^d = 1/L².

**Derivation**: L ~ 1/rho_m^(1/3) ~ 1/(Om*(1+z)³)^(1/3). Quantum density ~ L^(d-2) for d=3 bulk (2+1 RT surface): quantum density ~ L^1 ~ 1/(Om*(1+z)³)^(1/3). But dark energy is fraction of total: normalize by dark energy fraction. Area scaling gives 2/3 power of dark energy fraction.

**omega_de(z)**:
```
omega_de(z) = OL0 * (OL0 / (Om*(1+z)³ + OL0))^(2/3)
```

At z=0: (OL0/(Om+OL0))^(2/3) * OL0. Normalized form:
```
omega_de(z) = OL0 * (f_de(z)/f_de(0))^(2/3)
```
where `f_de(z) = OL0/(Om*(1+z)³ + OL0)`.

At z=0: f_de(z)/f_de(0) = 1, so omega_de = OL0. Correct.

**Free parameters**: Om, OL0 (no extra — pure RT prediction).

---

## H2: Page Curve Analog — Entanglement Entropy Growth Then Decrease

**Physical basis**: Page curve describes entanglement entropy S(t) first growing (before Page time) then decreasing. In cosmological context, dark energy entanglement entropy follows Page curve in redshift. Early universe (high z): small regions, suppressed entanglement. Middle z: peak entanglement. Late times (z→0): saturation or decrease as classical geometry dominates.

**Derivation**: Two factors — (1) growth of entanglement with matter fraction: ~ (rho_m/rho_total) = Omega_m(z); (2) early-time suppression factor: (1 - exp(-B/(1+z)³)) suppresses at very high z when (1+z)³ >> 1/B.

**omega_de(z)**:
```
omega_de(z) = OL0 * (1 + A * Om*(1+z)³/(OL0 + Om*(1+z)³)) * (1 - exp(-B/(1+z)³))
```

At z=0: (1 + A*Om/(OL0+Om)) * (1 - exp(-B)) — not exactly OL0 unless normalized. Normalized:
```
omega_de(z) = OL0 * [(1 + A*f_m(z)) * (1 - exp(-B/(1+z)³))] / [(1 + A*f_m(0)) * (1 - exp(-B))]
```
where `f_m(z) = Om*(1+z)³/(OL0 + Om*(1+z)³)`.

**Free parameters**: A (Page curve amplitude), B (early-time suppression scale), Om, OL0.

---

## H3: Holographic Screen Area — RT Area-to-Volume Ratio

**Physical basis**: Holographic screen at Hubble radius: A_H = 4π(c/H)². Screen quantum density ~ A_H * H = 4π c²/H (area × local quantum creation rate). As H(z) grows, screen shrinks but quantum creation rate falls faster. Dark energy tracks sqrt of quantum density ratio.

**Derivation**: Quantum density at z: n_q(z) ~ 1/H(z) (holographic screen quanta per unit area times area, net). Dark energy density ~ n_q relative to today, with RT correction for matter-occupied bulk: divide by (1 + A*rho_m/rho_de).

**omega_de(z)**:
```
omega_de(z) = OL0 * sqrt(E_LCDM(z) / (1 + A * Om*(1+z)³/OL0))
```
where `E_LCDM(z) = sqrt(Om*(1+z)³ + OL0)`.

At z=0: sqrt(1 / (1 + A*Om/OL0)). Normalized:
```
omega_de(z) = OL0 * sqrt((Om*(1+z)³ + OL0) / (OL0*(1 + A*Om*(1+z)³/OL0))) * sqrt(1 + A*Om/OL0)
```

Simplified form (absorbing normalization constant C):
```
omega_de(z) = C * sqrt(1 / (1 + A * Om*(1+z)³/OL0))
```
where C = OL0 * sqrt(1 + A*Om/OL0).

**Free parameters**: A (RT area-to-volume coupling), Om, OL0.

---

## Summary Table

| Theory | omega_de(z) | Key feature |
|--------|------------|-------------|
| H1 | OL0*(f_de(z)/f_de(0))^(2/3) | Pure power law in dark energy fraction |
| H2 | OL0*(1+A*f_m(z))*(1-exp(-B/(1+z)³)) / norm | Page curve: rise then saturation |
| H3 | C/sqrt(1+A*Om*(1+z)³/OL0) | Holographic suppression, monotone |
