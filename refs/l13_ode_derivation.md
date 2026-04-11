# refs/l13_ode_derivation.md -- L13-O: Full SQMH ODE vs A01 Approximation

> Date: 2026-04-11. Round 1 execution.
> 8-person parallel review team.

---

## Key Question

A01 uses: rho_DE(a) = OL0 * [1 + Om * (1 - a)]
Is this a good approximation to the full SQMH ODE?
Does using the full ODE improve chi2 by > 2 (Q81) or is it within 0.5 (K81)?

---

## SQMH ODE (Full)

d(omega_de)/dz = Gamma0 * Om * (1+z)^2 - 3 * omega_de / (1+z)

General solution (exact):
  omega_de(z) = Gamma0*Om*(1+z)^3/6 + C*(1+z)^(-3)
  C = OL0 - Gamma0*Om/6  [from BC: omega_de(z=0)=OL0]

This is the exact analytical solution; ODE numerical integration is not required.

---

## A01 Approximation

rho_DE(a) = OL0 * [1 + Om * (1-a)]

This is NOT the exact ODE solution with any specific Gamma0.
From the ODE analysis (l13_amplitude_derivation.py):
  - The linear slope of the exact ODE at a=1 is: 3*OL0 - Gamma0*Om
  - For A01 slope: need -OL0*Om
  - => Gamma0 = OL0*(3+Om)/Om ~ 7.36 (NOT 3*Om = 0.93)

A01 uses Gamma0 = 3*Om = 0.93, giving A_amp = -2.58 (from linear ODE), not +Om.
A01 is a DIFFERENT functional form chosen empirically.

---

## Numerical Results (l13_ode_results.json)

| Model     | Om_best | h_best | chi2  | Dchi2 vs LCDM |
|-----------|---------|--------|-------|----------------|
| LCDM      | 0.2921  | 0.6904 | 12.14 | (baseline)     |
| A01       | 0.2885  | 0.6816 | 11.63 | -0.51          |
| Full ODE (G0=3*Om) | 0.302 | 0.75 | 21.74 | +9.60 |

ODE - A01 chi2 = +10.11 (ODE WORSE than A01 with G0=3*Om)

---

## Analysis

The full SQMH ODE with Gamma0=3*Om gives chi2=21.74, WORSE than both LCDM (12.14) 
and A01 (11.63). This is because:

1. Gamma0=3*Om is the A01 phenomenological prescription, not the true ODE Gamma0.
2. The exact ODE solution with G0=3*Om has a very different functional form from A01.
3. The exact ODE solution: omega_de(a) = 0.93*0.31/(6*a^3) + C*a^3
   This grows as a^(-3) at low a (high z), creating a fast-decaying function.
4. At z=2, the ODE solution is ~3x OL0, while A01 is only ~1.2x OL0.
   This over-production at high z hurts chi2 vs BAO data.

The correct Gamma0 to match A01 exactly is Gamma0 ~ 7.36, not 3*Om.
But there is no SQMH theory reason to prefer Gamma0=7.36.

---

## Conclusion

**K81 NOT strictly triggered** (|diff|=10.1 >> 0.5).
**Q81 NOT triggered** (ODE is WORSE, not better, than A01).

HONEST FINDING: The full SQMH ODE with A01's Gamma0 prescription performs
significantly WORSE than A01 against DESI data. This means:
- A01 is NOT an approximation to the full ODE -- it is a DIFFERENT model.
- The "correct" SQMH ODE (if G0 is set self-consistently) fits the data differently.
- To make full ODE fit well, G0 would need to be tuned to ~7.36, not 3*Om.
- This tuning is not theoretically motivated.

The ODE result is worse by ~10 chi2 units vs A01. This is a significant finding:
A01's phenomenological form is what fits the data, not the literal ODE with G0=3*Om.

**Verdict**: Neither K81 nor Q81. A01 approximation is not the ODE with G0=3*Om.
The full ODE requires a different Gamma0 to match DESI data comparably to A01.
This is an important structural finding about A01's relationship to SQMH theory.
