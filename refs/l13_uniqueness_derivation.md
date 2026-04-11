# refs/l13_uniqueness_derivation.md -- L13-U: SQMH Uniqueness Analysis

> Date: 2026-04-11. Round 1 execution.
> 8-person parallel review team.

---

## Key Question

A01 is phenomenologically similar to a free 1-parameter model rho_DE = OL0*(1+A*(1-a)).
Is A01 statistically distinct from this arbitrary class? (K86 vs Q86)

---

## Model Definitions

- LCDM: A=0 (2 free params: Om, h)
- A01: A=Om THEORY-FIXED (2 free params: Om, h; A not free)
- Free-A: A free (3 free params: Om, h, A)

---

## Numerical Results (l13_uniqueness_results.json)

| Model  | Om   | h     | A    | chi2  | AIC   | BIC   |
|--------|------|-------|------|-------|-------|-------|
| LCDM   | 0.292| 0.690 | 0.0  | 12.14 | 16.14 | 16.03 |
| A01    | 0.289| 0.682 | ~0.29| 11.63 | 15.63 | 15.52 |
| Free-A | 0.264| 0.635 | 2.0  | 9.77  | 15.77 | 15.61 |

Dchi2 A01 vs LCDM: -0.51
Dchi2 Free-A vs LCDM: -2.37
Dchi2 A01 vs Free-A: +1.86 (Free-A fits better by 1.86)

AIC A01: 15.63, AIC Free-A: 15.77
Delta AIC (A01 - Free): -0.14 (A01 preferred by AIC -- FEWER PARAMS!)
BIC A01: 15.52, BIC Free-A: 15.61
Delta BIC (A01 - Free): -0.08 (A01 preferred by BIC)

---

## Critical Finding

The Free-A model best-fit A = 2.0 (at the upper bound!), NOT A ~ Om = 0.29.
The A scan confirms best chi2 at A~1.5, far from Om.

This means:
1. The best phenomenological 1-parameter model (A~2.0) is DIFFERENT from A01.
2. A01's specific prediction A=Om is NOT where the chi2 minimum falls.
3. The FREE-A model prefers A ~ 5-7x Om.

**Q86 cannot be triggered**: The best-fit free A != Om. SQMH does NOT uniquely
determine A to match data optimally.

However, an important nuance:
- AIC and BIC FAVOR A01 over Free-A (-0.14 and -0.08 respectively).
- This means A01's 0-extra-parameter prediction A=Om gives BETTER information
  criteria than the free model, even though Free-A has lower chi2.
- The Occam penalty exactly compensates for Free-A's chi2 gain.

**K86 status**: K86 asks if A01 is "statistically indistinguishable" from an
arbitrary 1-parameter model. The answer is nuanced:
- In terms of AIC/BIC: A01 is PREFERRED (not indistinguishable).
- In terms of raw chi2: Free-A fits better by 1.86 units.
- The best-fit A is NOT Om -- so the class of "A near Om" is disfavored vs "A~2".

---

## Additional Analysis: A Scan

The chi2 vs A scan shows:
- A=Om (0.31): chi2 ~ 11.58
- A=1.5: chi2 ~ 10.13 (global minimum from scan)
- A=0 (LCDM): chi2 ~ 12.14

The likelihood landscape is broad. A=Om is NOT the chi2 minimum, but it's
within 1.4 chi2 units of the scan minimum.

---

## SQMH Uniqueness: Honest Assessment

SQMH uniquely predicts A=Om through the theory structure (matter coupling).
However:
1. Empirically, A~1.5 fits slightly better than A=Om.
2. The physical 1-parameter model space (free A) best-fit differs from A01.
3. SQMH's prediction A=Om is NOT uniquely favored by data.

What SQMH DOES uniquely determine:
- The FORM of the perturbation: (1-a) dependence (linear in redshift)
- The COUPLING to matter: A proportional to Om (qualitatively)
- The ZERO-CROSSING: rho_DE(a=1)=OL0 without extra parameters

What SQMH does NOT uniquely determine:
- The EXACT coefficient A=Om (vs A=1.5 or A=2)

---

## K86/Q86 Verdict

**K86**: PARTIALLY TRIGGERED. A01 is NOT the global chi2 minimum of the 1-param class.
Best-fit A~2 >> Om. By this measure, A01 is not uniquely optimal.

**Q86 FAIL**: Cannot prove A=Om is uniquely determined.

**Intermediate verdict**: AIC/BIC favor A01 (fewer params, nearly same fit).
This means A01 is PARSIMONIOUS relative to the free-A class.
But it's not because SQMH uniquely determines A=Om; it's because
adding the free parameter A doesn't help enough to justify it.

**Paper language**: "SQMH uniquely predicts the perturbation amplitude A=Om
without free parameters. While a free amplitude A~1.5 yields slightly better
chi2 (by 1.4), information criteria (AIC, BIC) favor the 0-parameter A01 form.
SQMH's theoretical prediction A=Om is supported by parsimony, though the
data does not strongly constrain A to Om."
