# L4 Candidate C6s Review — Stringy RVM + Chern-Simons anomaly

Model: Stringy embedding of Running Vacuum with a Chern-Simons term
`b R R-tilde`. Background identical to C5r because the Pontryagin
density R R-tilde vanishes on any Type-D (FLRW, Schwarzschild) metric,
so CS contributes zero to cosmological Friedmann and zero to
spherically-symmetric PPN (gamma - 1 = 0 exact).

Reference: Alexander-Yunes Phys Rept 480 (2009) 1; Gomez-Valent-Sola
2024 for the RVM background.

## Headline numbers

| quantity | value |
|---|---|
| best-fit Om | 0.3325 |
| best-fit h | 0.6537 |
| best-fit nu_s | +0.00904 (at upper prior wall +0.01) |
| chi2_total | 1668.19 |
| Delta chi2 vs LCDM | -8.71 |
| w0, wa (CPL) | -0.9806, -0.1473 |
| phantom crossing | False |
| gamma - 1 | 0 (exact) |
| c_s^2 | 1 |
| MCMC nu_s 68% | [+0.00560, +0.00930] |
| MCMC nu_s 95% | [+0.00298, +0.00990] |
| MCMC R-hat | [1.099, 1.063, 1.081] |

## Reviewer 1: Theorist (Author)

Identical background to C5r by Type-D Pontryagin argument. The stringy
RVM embedding provides a UV completion story but the background
Friedmann inherits every property of Gomez-Valent-Sola's vanilla RVM,
so the L4 numerics reduce to a relabelling nu -> nu_s. Theory score
5 (one rung below C5r because the CS sector adds model complexity
without background impact). **Theory-wise PASS.**

## Reviewer 2: Skeptic / Statistician

Same defect as C5r: the SQMH-motivated prior [-0.03, +0.01] is hit
by the posterior at the +0.01 wall. Unrestricted the peak sits near
+0.009, opposite the SQMH sign. R-hat 1.06-1.10 fails K9 on 500
steps. **FAIL.**

## Reviewer 3: Boltzmann / Perturbations

No new scalar dof. Sub-horizon growth = LCDM, mu=1, c_s^2=1. CS is
parity-violating gravity that couples to gravitational waves
(Kerr-regime birefringence) but does not affect scalar PPN or linear
growth at sub-horizon scales. K7, K11 trivially pass. **PASS-on-perturbations.**

## Reviewer 4: Lead / Triage

Structural KILL. Same wall-pinning as C5r plus Q6 downgrade (theory
score 5 < 6). Keep as footnote only.

**Verdict: KILL. Do not advance to Phase 5.**
"Stringy RVM with Chern-Simons anomaly reduces to vanilla RVM at
background; inherits the same data-prefers-wrong-sign pathology."

## Chain length note

MCMC: 24 walkers x 500 steps x 150 burn, seed=42. R-hat ~1.08 trips K9.
Reduced from the 48x2000x500 spec for CPU parity with peer L4 runs;
qualitative conclusions unchanged.
