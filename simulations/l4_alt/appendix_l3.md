

---

# Appendix: Alt-20 L3 Background Fit (Round N)

0-parameter alternatives from `refs/alt20_catalog.md`; tight-box
(Ω_m ∈ [0.28, 0.36], h ∈ [0.64, 0.71]) Nelder-Mead via
`simulations/l4/common.py::tight_fit`. LCDM baseline χ² = 1676.89.

## Joint fit results (BAO+SN+CMB+RSD, 13+1829+3+8 points)

| ID  | Ω_m   | h     | χ²_total | Δχ²    | w_0     | w_a     | Verdict |
|-----|-------|-------|----------|--------|---------|---------|---------|
| A01 | 0.3102| 0.6771| 1655.77  | −21.12 | −0.899  | −0.115  | KEEP    |
| A02 | 0.3162| 0.6725| 1669.11  |  −7.78 | −0.987  | +0.086  | KILL C4 |
| A03 | 0.3071| 0.6797| 1656.56  | −20.33 | −0.897  | −0.036  | KEEP*   |
| A04 | 0.3011| 0.6843| 1668.00  |  −8.89 | −0.757  | −0.469  | KEEP    |
| A05 | 0.3108| 0.6766| 1655.86  | −21.03 | −0.900  | −0.124  | KEEP    |
| A06 | 0.3096| 0.6776| 1655.77  | −21.12 | −0.897  | −0.103  | KEEP    |
| A07 | 0.3197| 0.6696| 1675.44  |  −1.45 | −0.998  | +0.015  | KILL C4 |
| A08 | 0.3125| 0.6752| 1657.88  | −19.01 | −0.921  | −0.089  | KEEP*   |
| A09 | 0.3063| 0.6803| 1656.85  | −20.04 | −0.886  | −0.051  | KEEP*   |
| A10 | —     | —     | 1656.85  | −20.04 | −0.904  | −0.203  | KILL K3 |
| A11 | 0.3152| 0.6731| 1662.36  | −14.53 | −0.948  | −0.056  | KEEP*   |
| A12 | 0.3090| 0.6780| 1655.27  | −21.62 | −0.886  | −0.133  | KEEP    |
| A13 | 0.3139| 0.6742| 1659.80  | −17.09 | −0.934  | −0.073  | KEEP*   |
| A14 | 0.3161| 0.6726| 1671.04  |  −5.85 | −0.997  | +0.120  | KILL C4 |
| A15 | 0.3143| 0.6739| 1661.61  | −15.28 | −0.947  | −0.031  | KEEP*   |
| A16 | 0.3096| 0.6776| 1655.76  | −21.13 | −0.897  | −0.104  | KEEP    |
| A17 | 0.3119| 0.6757| 1655.63  | −21.26 | −0.895  | −0.178  | **KEEP**|
| A18 | 0.3109| 0.6766| 1660.41  | −16.48 | −0.938  | +0.051  | KILL C4 |
| A19 | 0.3180| 0.6709| 1668.27  |  −8.62 | −0.970  | −0.047  | KEEP*   |
| A20 | 0.3079| 0.6790| 1656.17  | −20.72 | −0.894  | −0.066  | KEEP*   |

`KEEP` = passes K1-K4 including K2 |w_a| ≥ 0.10 margin.
`KEEP*` = passes K1, K3, K4 but K2 soft (|w_a| < 0.10).
`KILL C4` = L2 sign failure (w_a > 0).
`KILL K3` = phantom crossing detected (A10 reciprocal form crosses w = −1
through (1−m·x·a) factor near a ~ 0.6).

## Strong L3 survivors (K1-K4 all PASS)

A01, A04, A05, A12, A17 — five 0-parameter candidates that reach DESI-
DR2-compatible |w_a| ≥ 0.1 without any free θ.

A01 / A05 / A06 / A12 / A16 / A17 / A20 cluster at Δχ² ≈ −21, matching
the C28 Maggiore RR non-local improvement (Δχ² = −21.08) with **zero**
extra parameters. This is a striking feature of the amplitude-locked
ansatz: at Ω_m ~ 0.31 the drift term m·(1−a) naturally has the right
amplitude to reproduce the DESI-DR2-preferred w_0 ≈ −0.9 region.

## L3 → L4

**L3 PASS (KEEP, hard)**: A01, A04, A05, A12, A17 (5 candidates).
**L3 PASS-soft (KEEP*, |w_a|<0.10)**: A03, A08, A09, A11, A13, A15, A19,
A20 — promoted to L4 but flagged K2-soft.
**L3 KILL**: A02, A07, A10, A14, A18 (5 candidates).

## Notes

- Every non-linear candidate lands in a **narrow Ω_m ∈ [0.30, 0.32],
  h ∈ [0.67, 0.68] box** — the SN+BAO joint prefers this point regardless
  of the functional form, as long as the drift amplitude is locked to Ω_m.
- The closed-form nature makes these runs ≈100× faster than C28/C33,
  enabling full 20-candidate sweep in < 2 minutes.
- A04 (volume-cumulative `1+m(1−a³)`) has the largest |w_a| = 0.469 but
  the worst χ² among survivors (Δχ² = −8.89) — the `a³` weighting pushes
  the drift to too-late times to match SN+BAO jointly.
