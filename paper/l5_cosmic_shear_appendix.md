# L5 Appendix: Cosmic Shear S_8 Channel (Phase L5-D)

This appendix reports the DES-Y3 + KiDS-1000 weak-lensing S_8 channel
applied to all L5 candidates together with the K15 / Q10 / Q11 gate
checks.

## Setup

Combined weak-lensing constraint (inverse-variance combine of DES-Y3
Abbott+2022 S_8 = 0.772 +/- 0.017 and KiDS-1000 Asgari+2021
S_8 = 0.759 +/- 0.024):

    S_8^WL = 0.7656 +/- 0.0138

Planck's own S_8 is *not* re-added here, as its information is already
absorbed into the compressed CMB likelihood used in the joint fit.

For each candidate we evaluate S_8 via
`simulations.l5.common.s8_from_Efunc`, which integrates the linear
growth ODE on the candidate's E(z) at its best-fit (Om, h) and scales
the Planck 2018 sigma_8 = 0.811 normalisation by
D_model(a=1)/D_LCDM(a=1). The prefactor sqrt(Om/0.3) is applied to
give S_8.

Mainstream C28/C33 use the CPL template (w0_fid, wa_fid) from
`simulations/l5/forecast/dr3_forecast.json`; alt-20 candidates use
their zero-parameter closed forms from `simulations/l4_alt/runner.py`.

## Gates

- **K15**: S_8 < 0.84 (DES-Y3 3 sigma upper bound).
- **Q10**: delta chi^2_WL vs LCDM <= +3 (no catastrophic growth-sector
  worsening when cosmic shear is added).
- **Q11**: |h - 0.732| (SH0ES) not worse by more than 0.005 compared
  to LCDM's |h - 0.732| = 0.0629.

## Results

| ID    | Om     | h      | S_8    | chi^2_WL | d chi^2_WL | d chi^2_bg | K15  | Q10  | Q11  |
|-------|--------|--------|--------|----------|------------|------------|------|------|------|
| LCDM  | 0.3204 | 0.6691 | 0.8381 |    27.58 |       0.00 |       0.00 | PASS | PASS | PASS |
| C28   | 0.3091 | 0.6780 | 0.7974 |     5.32 |     -22.27 |     -21.33 | PASS | PASS | PASS |
| C33   | 0.3397 | 0.6472 | 0.8906 |    82.08 |     +54.50 |     +70.80 | FAIL | FAIL | FAIL |
| A01   | 0.3102 | 0.6771 | 0.8018 |     6.89 |     -20.69 |     -21.12 | PASS | PASS | PASS |
| A05   | 0.3108 | 0.6766 | 0.8039 |     7.70 |     -19.88 |     -21.03 | PASS | PASS | PASS |
| A12   | 0.3090 | 0.6780 | 0.7977 |     5.40 |     -22.18 |     -21.62 | PASS | PASS | PASS |
| A17   | 0.3119 | 0.6757 | 0.8086 |     9.70 |     -17.88 |     -21.26 | PASS | PASS | PASS |
| A03   | 0.3071 | 0.6797 | 0.7891 |     2.90 |     -24.68 |     -20.33 | PASS | PASS | PASS |
| A04   | 0.3011 | 0.6843 | 0.7719 |     0.21 |     -27.38 |      -8.89 | PASS | PASS | PASS |
| A06   | 0.3096 | 0.6776 | 0.7993 |     5.97 |     -21.61 |     -21.12 | PASS | PASS | PASS |
| A08   | 0.3125 | 0.6752 | 0.8101 |    10.42 |     -17.16 |     -19.01 | PASS | PASS | PASS |
| A09   | 0.3063 | 0.6803 | 0.7867 |     2.35 |     -25.23 |     -20.04 | PASS | PASS | PASS |
| A11   | 0.3152 | 0.6731 | 0.8196 |    15.31 |     -12.27 |     -14.53 | PASS | PASS | PASS |
| A13   | 0.3139 | 0.6742 | 0.8148 |    12.72 |     -14.87 |     -17.09 | PASS | PASS | PASS |
| A15   | 0.3143 | 0.6739 | 0.8158 |    13.22 |     -14.36 |     -15.28 | PASS | PASS | PASS |
| A16   | 0.3096 | 0.6776 | 0.7995 |     6.02 |     -21.56 |     -21.13 | PASS | PASS | PASS |
| A19   | 0.3180 | 0.6709 | 0.8295 |    21.47 |      -6.11 |      -8.62 | PASS | PASS | PASS |
| A20   | 0.3079 | 0.6790 | 0.7926 |     3.82 |     -23.76 |     -20.72 | PASS | PASS | PASS |

## Interpretation

All L5 candidates leave the linear perturbation sector structurally
identical to LCDM (mu(a,k) = 1, c_s^2 = 1 at the background-only
level): no modification to the growth equation beyond the change in
H(z) itself. Consequently the S_8 tension with cosmic shear that
LCDM exhibits (chi^2_WL ~= 27.6, ~5 sigma) is inherited by every
background-only candidate, and **the cosmic shear channel does not
discriminate among L5 candidates at the background-only level**.

The apparent numerical differentials in the table above come from two
physically trivial sources: (i) the sqrt(Om/0.3) prefactor in S_8
shifts with each candidate's best-fit Om, and (ii) the D(a=1) growth
amplitude shifts slightly because a modified E(z) re-weights the
growth integral. These are not *structural* improvements in the
growth sector: a fully self-consistent perturbation treatment with
mu(a,k) != 1 would be required for a genuine shear-level signature,
and such a treatment is deferred to Phase 5+ (hi_class or EFTCAMB).

Within the parameterisation used here all mainstream candidates
(C28, A01, A05, A12, A17) and the entire alt-soft cluster pass K15,
Q10, and Q11. The sole failure is **C33** (f(Q) teleparallel): its
best-fit (Om = 0.3397, h = 0.6472) drives S_8 = 0.891, above the
DES-Y3 3 sigma upper bound, generating chi^2_WL = 82.1
(delta chi^2_WL = +54.5 vs LCDM), and it also marginally worsens Q11
(|h - 0.732| = 0.0848 vs LCDM's 0.0629). This is reported for
bookkeeping but, being driven entirely by background-level parameter
shifts, should be interpreted as a **caution flag** rather than a
definitive kill: a full perturbation-level treatment of f(Q) would be
needed before C33 can be ruled out on cosmic-shear grounds.

**Bottom line**: the cosmic shear channel does not favor any L5
candidate over LCDM. S_8 tension remains a LCDM-inherited issue that
must be addressed by mu(a,k) != 1 dark sector physics, not by
background-only modifications.
