# L491 — RAR a_0 Functional-Form Audit

**Goal**: test whether the L482 PASS_STRONG result (a_0 = 1.069e-10 with M16) is global or cherry-picked.

**Sample**: SPARC, 175 galaxies, 3389 points (Upsilon_disk=0.5, Upsilon_bul=0.7).
**SQT prediction (Planck H0=67.4)**: a_0 = 1.0422e-10 m s^-2 (log10 = -9.9821).

## a_0 fit per functional form

| Form | a_0 [m s^-2] | log10(a_0) | chi2/dof | sigma_log10 (Δχ²=1) | Δlog to SQT | Within 2σ? |
|------|-------------:|----------:|---------:|-------------------:|-----------:|:----------:|
| M16 | 1.0687e-10 | -9.9712 | 1.294 | 0.0060 | +0.0109 | YES |
| simple_nu | 1.0427e-10 | -9.9818 | 1.293 | 0.0060 | +0.0002 | YES |
| standard | 1.2080e-10 | -9.9180 | 1.497 | 0.0060 | +0.0641 | NO |
| RAR_tanh | 1.5009e-10 | -9.8236 | 1.397 | 0.0050 | +0.1584 | NO |
| Bekenstein | 6.9617e-11 | -10.1573 | 1.354 | 0.0070 | -0.1752 | NO |
| expo | 1.0985e-10 | -9.9592 | 1.396 | 0.0060 | +0.0228 | NO |
| n4_family | 1.6261e-10 | -9.7888 | 1.489 | 0.0050 | +0.1932 | NO |

## Distribution of a_0 across forms

- N_forms                : 7
- log10(a_0) range       : [-10.1573, -9.7888]
- full spread            : 0.3684 dex
- 16-84 percentile range : [-9.9889, -9.8222] (0.1666 dex)
- median log10(a_0)      : -9.9592 (a_0 = 1.0985e-10)
- mean log10(a_0)        : -9.9428
- log10 a_0 SQT          : -9.9821
- median - SQT           : +0.0228 dex
- SQT inside full band   : True
- SQT inside IQR (16-84) : True

## K-criteria (functional-form stability)

- K_R6_strict (full ≤ 0.04 dex)        : FAIL (0.3684)
- K_R6_relaxed (full ≤ 0.10 dex)       : FAIL (0.3684)
- K_R6_iqr_strict (IQR ≤ 0.04 dex)     : FAIL (0.1666)
- K_R6_median_to_SQT ≤ 0.04 dex        : PASS (0.0228)

## Cherry-pick analysis

The L482 5/5 PASS_STRONG result was based on M16 only.  If the median across reasonable forms equals M16 (and the spread is small), the result is global; if not, M16 was a lucky pick.

M16 a_0   : 1.0687e-10  (log10 -9.9712)
median a_0: 1.0985e-10            (log10 -9.9592)
M16 - median: -0.0119 dex

Interpretation:
- All seven forms have an a-priori physics motivation in the MOND/RAR literature; none can be excluded as 'unreasonable' without post-hoc selection.
- Pre-registration of M16 alone would be acceptable only if M16 is the literature default.  M16 is McGaugh's choice; simple-nu and standard-mu predate M16 by decades.

## Verdict: **GLOBAL_PARTIAL**

Some spread, but the median sits near SQT and SQT lies in the band.  Result is robust but not pinpoint.

## One-line honesty

> GLOBAL PARTIAL — median a_0 within 0.04 dex of SQT but full spread 0.368 dex; not pinpoint.
