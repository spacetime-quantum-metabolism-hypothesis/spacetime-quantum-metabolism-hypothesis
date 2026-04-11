# refs/l13_amplitude_derivation.md -- L13-A: Omega_m Amplitude Theoretical Origin

> Date: 2026-04-11. Round 1 execution.
> 8-person parallel review team.

---

## Key Question

In A01: rho_DE(a) = OL0 * [1 + Om * (1-a)]
The amplitude of perturbation is Om. Is this:
  (a) Derived from SQMH equation structure?
  (b) A normalization artifact?

---

## Analytical Derivation

From l13_amplitude_derivation.py:

SQMH ODE general solution:
  omega_de(z) = Gamma0*Om*(1+z)^3/6 + C*(1+z)^(-3)
  C = OL0 - Gamma0*Om/6

Linearized slope at a=1 (z=0):
  d(omega_de)/da|_{a=1} = 3*OL0 - Gamma0*Om

For A01 form rho_DE = OL0*(1 + A*(1-a)), the slope is:
  d(omega_de)/da|_{a=1} = -OL0*A

Matching: 3*OL0 - Gamma0*Om = -OL0*A
=> A = Gamma0*Om/OL0 - 3

For Gamma0 = 3*Om (A01 prescription):
  A = 3*Om^2/OL0 - 3 = 3*(Om^2 - OL0)/OL0 = -2.58 (NEGATIVE!)

This means the A01 amplitude (+Om) cannot be derived from Gamma0=3*Om in the ODE.

---

## Numerical Comparison

At z=0.1,0.3,0.5,1.0,1.5,2.0,3.0:
- A01 rho_DE: monotonically increases with z (physically reasonable)
- ODE rho_DE (G0=3*Om): drops at low z, then explodes at high z
- Difference grows to -2.24 at z=3

A01 and the ODE with G0=3*Om are ENTIRELY DIFFERENT functions.

---

## What Sets the Om Amplitude?

The Om amplitude in A01 comes from:
1. Empirical fitting: the form OL0*(1+A*(1-a)) with A=Om is the best-fitting
   functional form found in the Alt-20 scan.
2. SQMH structural motivation: the birth-death equation says DE production
   is proportional to rho_m. At high z, rho_m ~ Om*(1+z)^3.
   This suggests DE "excess" at high z should scale as Om.
3. But the EXACT coefficient A=Om (not Om/OL0, not Om^2) is NOT derived.

**Normalization check**: rho_DE(a=1)=OL0 is automatically satisfied for ANY A.
So A=Om is NOT a normalization artifact. But it IS empirically fitted.

---

## Gamma0 Required for Exact A01 Match

To exactly reproduce A01's linear term, need:
  Gamma0 = OL0*(3+Om)/Om = 0.685*(3.31)/0.31 = 7.36

Not 3*Om = 0.93. This Gamma0 has no SQMH theory motivation.

---

## Verdict

**K82 PARTIAL**: Amplitude Om is NOT a pure normalization artifact
(normalization alone doesn't force A=Om). But the exact coefficient A=Om
is phenomenologically fitted, not theoretically derived.

**Q82 FAIL**: Cannot prove A=Om is uniquely determined by SQMH structure.
The structural motivation (matter coupling -> Om scaling) is qualitative,
not quantitative.

**Honest assessment**: A01's Om amplitude is an empirical observation
consistent with SQMH physics (matter drives DE production, so amplitude
scales with Om), but the exact match A=Om is not derived.

Paper language: "The amplitude Om of the perturbation reflects the SQMH
birth-death coupling (DE production proportional to matter density),
but the exact coefficient requires further theoretical derivation."
