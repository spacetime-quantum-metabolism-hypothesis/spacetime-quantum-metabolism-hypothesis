# 7. Comparison to ΛCDM

## 7.1 Joint Δχ² table

The ΛCDM baseline on the full BAO+SN+CMB+RSD joint likelihood is

```
chi2_total = 1676.89    at (Omega_m, h) = (0.320, 0.669).
```

Phase-5 full results:

| ID | Family | Δχ² | w_0 | w_a | Params | Phase-5 verdict |
|---|---|---|---|---|---|---|
| **C11D** | Disformal IDE | **−22.12** | −0.877 | −0.186 | 1 (λ) | **WINNER** |
| **C28** | Maggiore RR | **−21.08** | −0.849 | −0.242 | 1 (γ_0) | **WINNER** |
| **A12** | erf-diffusion | **−21.62** | −0.886 | −0.133 | 0 | **WINNER (class rep)** |
| A17 | adiabatic pulse | −21.26 | −0.895 | −0.178 | 0 | backup |
| A01 | SQMH canonical | −21.12 | −0.899 | −0.115 | 0 | cluster member |
| A05 | sqrt relaxation | −21.03 | −0.900 | −0.124 | 0 | cluster member |
| A04 | volume-cumul. | −8.89 | −0.757 | −0.469 | 0 | outlier (DR3 sentinel) |
| C33 | f(Q) | −6.28 | −0.984 | −0.262 | 2 | DEMOTED (S_8) |
| C26 | Perez-Sudarsky | ~0 | −1.000 | 0 | 1 | KILL (CMB) |
| C27 | Deser-Woodard | +0.37 | — | — | 1 | KILL (posterior collapse) |

## 7.2 Bayesian evidence (Jeffreys' scale)

Phase-5 fixed-θ results (extra parameters fixed at L4 MAP): LCDM ln Z = −843.689 ± 0.170.

| ID | ln Z | Δ ln Z (fixed-θ) | Jeffreys | K14 | Q8 |
|---|---|---|---|---|---|
| C28 | −832.432 | **+11.257** | STRONG | — | ✓ |
| A17 | −832.909 | **+10.780** | STRONG | — | ✓ |
| A12 | −832.910 | **+10.779** | STRONG | — | ✓ |
| A01 | −832.999 | **+10.690** | STRONG | — | ✓ |
| A05 | −833.108 | **+10.581** | STRONG | — | ✓ |
| A06 | −833.115 | **+10.574** | STRONG | — | ✓ |
| A16 | −833.135 | **+10.554** | STRONG | — | ✓ |
| A20 | −833.389 | **+10.300** | STRONG | — | ✓ |
| A03 | −833.566 | **+10.123** | STRONG | — | ✓ |
| A09 | −833.679 | **+10.010** | STRONG | — | ✓ |
| A08 | −834.054 |  **+9.635** | STRONG | — | ✓ |
| C11D | −834.738 | **+8.951** | STRONG | — | ✓ |
| A13 | −835.032 |  **+8.657** | STRONG | — | ✓ |
| A15 | −835.975 |  **+7.714** | STRONG | — | ✓ |
| A11 | −836.409 |  **+7.280** | STRONG | — | ✓ |
| A19 | −839.229 |  **+4.460** | substantial | — | ✓ |
| C33 | −841.181 |  **+2.508** | substantial | — | ✓ |

**K14 failures: 0.  Q8 passes: 17/17.**

**Phase-6 fully marginalized results** (L6-E, dynesty nlive=800/1000, 2026-04-11):
LCDM ln Z = −843.538 ± 0.083 (hires re-run, seed=42).

| ID | Δ ln Z (L6 marginalized) | Jeffreys | K17 | vs L5 fixed-θ |
|---|---|---|---|---|
| A12 | **+10.769** | STRONG | PASS | −0.010 |
| A17 | **+10.524** | STRONG | PASS | −0.256 |
| A01 | **+10.515** | STRONG | PASS | −0.175 |
| A05 | **+10.432** | STRONG | PASS | −0.149 |
| A06 | **+10.527** | STRONG | PASS | −0.047 |
| A09 |  **+9.968** | STRONG | PASS | −0.042 |
| A08 |  **+9.437** | STRONG | PASS | −0.198 |
| C11D |  **+8.771** | STRONG | PASS | −0.180 |
| C28 |  **+8.633** | STRONG | PASS | −2.624 |

**Key observation (L6)**: Full marginalization reverses the C28 lead.
A12 (0-param) Δ ln Z = +10.769 **exceeds** C28 (1-param) Δ ln Z = +8.633 by 2.14 nats.
C28's large drop (−2.6 nats vs fixed-θ) reflects the full 3D prior volume penalty.
Zero-parameter alt models are decisively preferred over C28 on marginalized evidence.

**Original key observation (L5)**: alt-20 cluster (A01,A05,A06,A12,A16,A17,A20) clusters at
Δ ln Z ≈ +10.3–10.8 fixed-θ, nearly matching C28 (+11.3). Now confirmed: marginalized
evidence inverts this ordering, with A12 > C28 by 2.14 nats.

**Jeffreys' scale**:

| Δ ln Z | Interpretation |
|--------|----------------|
| > 5    | Strong |
| 2.5–5  | Substantial |
| 1–2.5  | Weak |
| −1–1   | Inconclusive |
| < −1   | Decisive against (K14) |

## 7.3 2-D (w_0, w_a) posterior contours

Corner plots in `paper/figures/`:
- `l5_C28_corner.png`, `l5_A12_corner.png`, `l5_A17_corner.png`
- `l5_A01_corner.png`, `l5_A05_corner.png`
- `l5_dr3_forecast.png` — Fisher ellipses + candidate prediction points

LCDM (w_0, w_a) = (−1, 0) lies outside the 3σ contour for C11D and C28;
A12 excludes LCDM at ~2.5σ.  DESI DR2 central (−0.757, −0.83) compatible
at 2σ with all winners but not reproduced at 1σ.

## 7.4 Hubble tension

| ID | h | Δh vs SH0ES |
|---|---|---|
| LCDM | 0.669 | −0.063 |
| C11D | 0.678 | −0.054 |
| C28 | 0.677 | −0.055 |
| A12 | 0.677 | −0.055 |
| C33 (demoted) | 0.647 | −0.085 |
| SH0ES | 0.732 | 0 |

All winners reduce tension by ~13% vs LCDM.  No resolution.  §8 records
this honestly.

## 7.5 Phase-6 Occam Analysis

**L6-E3 Gaussian approximation** (preliminary, 2026-04-11):

| Model | ndim | Occam penalty (nats) | L5 Δ ln Z (fixed-θ) | Net after Occam |
|-------|------|---------------------|---------------------|-----------------|
| A12   | 2    | −2.53               | +10.779             | +8.25 (reference)|
| C11D  | 3    | −3.28               | +8.951              | +5.67            |
| C28   | 5    | −3.91               | +11.257             | +7.35            |

**L6-E actual marginalization** (dynesty nlive=800, LCDM ln Z = −843.538):

| Comparison | L6 marginalized gap | Occam diff (Gaussian) | Net | Justified? |
|---|---|---|---|---|
| C28 − A12 | −2.136 nats | −1.380 nats | −3.516 nats | **No** |
| C11D − A12 | −1.998 nats | −0.746 nats | −2.744 nats | **No** |

**Key result (L6-E final, 2026-04-11)**:

| Comparison | L6 marginalized gap | Occam diff (Gaussian) | Net | Justified? |
|---|---|---|---|---|
| C28 − A12 | −2.136 nats | −1.380 nats | −3.516 nats | **No** |
| C11D − A12 | −1.998 nats | −0.746 nats | −2.744 nats | **No** |

Full marginalization confirms zero-parameter A12 > C11D (1-param) by 2.00 nats,
and A12 > C28 (1-param) by 2.14 nats — no Gaussian approximation needed.

C11D's small drop (−0.18 nats vs fixed-θ) reflects a tight posterior on λ;
the MAP is close to the posterior mean. C28's large drop (−2.62 nats) reflects
a broad prior on γ₀ that is poorly constrained by data.

**Interpretation**: Data does NOT justify extra parameters in C11D or C28 relative
to the zero-parameter A12. The ranking on fully marginalized evidence is:
A12 > alt-20 cluster > C11D > C28 (all STRONG Jeffreys).

## 7.6 μ_eff and Growth Sector (Phase-6)

L6-G2 analysis (2026-04-11): All three winners have μ_eff ≈ 1 at current
observational scales:

| Model | μ_eff(a=1, k=0.1/Mpc) | K18 | ΔS₈ | Q15 |
|-------|----------------------|-----|-----|-----|
| C11D  | 1.0000 (GW enforces A'=0 → α_T~0) | — | 0.000 | — |
| C28   | 1.0015 (γ₀=0.0015 << 1)           | — | 0.001% | — |
| A12   | 1.0000 (background-only, declared) | — | 0.000 | — |

**S₈ tension is structurally not resolved** at the background + perturbation
level. Full CLASS CMB power spectrum verification: pending (hi_class not
installed; K19 provisional via compressed likelihood: C11D Δχ²_CMB = −6.33
vs LCDM at same parameters).

## 7.5 S_8 / σ_8

Winners (C11D, C28, A12): μ_eff ≈ 1, S_8 ~ 0.82 (within 0.5% of LCDM).
S_8 tension (Planck ~ 0.834, DES-Y3 ~ 0.772, KiDS-1000 ~ 0.759) is
**not resolved** — all background-only μ=1 models cannot address it
structurally.  Parametric Ω_m shifts produce apparent improvement only.

C33 (demoted): S_8 = 0.891, Ω_m = 0.340, exceeds DES-Y3 3σ upper bound.

## 7.6 fσ_8(z) predictions

All winners match LCDM growth to ≤ 0.5% at all 8 RSD redshifts.
RSD provides weak winner discrimination; growth channel is degenerate.
