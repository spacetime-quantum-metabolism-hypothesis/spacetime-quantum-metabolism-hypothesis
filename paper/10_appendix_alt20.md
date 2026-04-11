# Appendix A. Twenty Independent Zero-Parameter Candidates

## A.1 Motivation

All twenty mainstream families in §3–§4 (quintessence, f(R/Q/T),
Horndeski/DHOST/Galileon, non-local gravity, RVM, unimodular diffusion,
IDE, disformal coupling, k-essence, mimetic, Chaplygin, TeVeS, bimetric,
holographic, Cardassian, DGP, emergent/entropic, varying-constants,
early dark energy) introduce at least one extra parameter beyond ΛCDM.
A natural question is whether the DESI DR2 preference for (w_0 ≈ −0.85,
w_a < 0) can be reproduced **without any free parameter** — i.e.
whether the drift amplitude can be locked to a quantity already in ΛCDM
such as the matter fraction Ω_m itself.

We constructed twenty closed-form modifications to ρ_DE(a)/Ω_Λ in which
the amplitude is tied to Ω_m by construction. The complete definitions
are listed in `refs/alt20_catalog.md` and implemented as
one-line expressions in `simulations/l4_alt/runner.py`. We emphasise
that these are NOT twenty independent physical theories — §A.3 shows
that they form a single one-dimensional family once projected onto the
drift direction.

## A.2 Catalogue

Let x = 1 − a and m = Ω_m. The twenty candidates are (baseline OL):

| ID  | Name                                | ρ_DE(a) / OL                                    |
|-----|-------------------------------------|-------------------------------------------------|
| A01 | SQMH canonical (matter-drift)       | 1 + m·x                                         |
| A02 | Quadratic drift                     | 1 + m·x²                                        |
| A03 | Log horizon entropy                 | 1 − m·ln a                                      |
| A04 | Volume-cumulative                   | 1 + m·(1 − a³)                                  |
| A05 | Sqrt relaxation                     | √(1 + 2 m·x)                                    |
| A06 | Exponential                         | exp(m·x)                                        |
| A07 | Hyperbolic (cosh)                   | cosh(m·x)                                       |
| A08 | Tanh transition                     | 1 + tanh(m·x) / (1 + tanh m)                    |
| A09 | Causal-diamond 2D                   | 1 + m·x·(1 + x)                                 |
| A10 | Reciprocal drift                    | 1 / (1 − m·x·a)                                 |
| A11 | Sigmoid (logistic)                  | 2 / (1 + exp(−m·x))                             |
| A12 | Error-function diffusion            | 1 + erf(m·x)                                    |
| A13 | Arctan plateau                      | 1 + (2/π)·arctan(m·x)                           |
| A14 | Matter-ratio power                  | a^(−m·(1 − m)·x)                                |
| A15 | Stretched exponential               | exp(m·(1 − √a))                                 |
| A16 | Second-order Taylor                 | 1 + m·x + ½ m²·x²                               |
| A17 | Adiabatic pulse                     | 1 + m·x·exp(−x²)                                |
| A18 | Gaussian localised                  | 1 + m·(1 − exp(−x²/m))                          |
| A19 | Harmonic fraction                   | 1 / (1 − m²·x/(1 + x))                          |
| A20 | Two-term geometric                  | (1 + m·x) / (1 − m·x²/2)                        |

All twenty have exactly zero free parameters: only (Ω_m, h) are fit,
identical to ΛCDM.

## A.3 L2/L3/L4/L5 verdict summary

| ID  | L2 C4 | L3 K3 | L4 Δχ² | w_a     | L5 verdict       |
|-----|-------|-------|--------|---------|------------------|
| A01 | ✓     | ✓     | −21.12 | −0.115  | cluster member   |
| A02 | ✗     | —     | —      | +0.086  | KILL L2 C4       |
| A03 | ✓     | ✓     | −20.33 | −0.036  | K2-soft cluster  |
| A04 | ✓     | ✓     |  −8.89 | −0.469  | **outlier**      |
| A05 | ✓     | ✓     | −21.03 | −0.124  | cluster member   |
| A06 | ✓     | ✓     | −21.12 | −0.103  | cluster member   |
| A07 | ✗     | —     |  −1.45 | +0.015  | KILL L2 C4       |
| A08 | ✓     | ✓     | −19.01 | −0.089  | K2-soft cluster  |
| A09 | ✓     | ✓     | −20.04 | −0.051  | K2-soft cluster  |
| A10 | ✓     | ✗     | −20.04 | −0.203  | KILL L3 K3       |
| A11 | ✓     | ✓     | −14.53 | −0.056  | K2-soft cluster  |
| A12 | ✓     | ✓     | −21.62 | −0.133  | **cluster champion** |
| A13 | ✓     | ✓     | −17.09 | −0.073  | K2-soft cluster  |
| A14 | ✗     | —     |  −5.85 | +0.120  | KILL L2 C4       |
| A15 | ✓     | ✓     | −15.28 | −0.031  | K2-soft cluster  |
| A16 | ✓     | ✓     | −21.13 | −0.104  | cluster member   |
| A17 | ✓     | ✓     | −21.26 | −0.178  | cluster member   |
| A18 | ✗     | —     | −16.48 | +0.051  | KILL L2 C4       |
| A19 | ✓     | ✓     |  −8.62 | −0.047  | K2-soft cluster  |
| A20 | ✓     | ✓     | −20.72 | −0.066  | K2-soft cluster  |

- **L2 C4 killed (4)**: A02, A07, A14, A18 — w_a > 0, wrong drift direction.
- **L3 K3 killed (1)**: A10 — phantom crossing in the reciprocal form.
- **L4/L5 survivors (15)**: A01, A03–A06, A08, A09, A11–A13, A15–A17, A19, A20.

## A.4 Principal component analysis (L5-F SVD)

**The central result of this appendix.** We constructed a 15 × 201
matrix whose rows are the relative deviation
ΔE²(z)/E²_ΛCDM(z) for each surviving candidate at its best-fit
(Ω_m, h), evaluated on a uniform grid z ∈ [0, 2]. SVD gave:

| Mode | Singular value | Variance fraction | Cumulative |
|------|----------------|-------------------|------------|
| 1    | 1.748          | 99.147 %          | 99.147 %   |
| 2    | 0.162          |  0.848 %          | 99.995 %   |
| 3    | 0.0126         |  0.0051 %         | ≈100.000 % |
| 4    | 0.0017         |  9.4 × 10⁻⁵ %     | ≈100.000 % |
| 5    | 5.6 × 10⁻⁵     | 10⁻⁹              | ≈100.000 % |

**Effective dimensionality** (participation ratio
n_eff = 1 / Σ f_i²): **1.017**.

**Interpretation.** The fifteen closed-form candidates collapse onto a
single one-dimensional drift direction at better than 99 % of total
variance. The "alt-20 cluster" is not fifteen independent theories;
it is **one drift family, sampled in fifteen mutually equivalent
closed-form disguises**. All Taylor expansions to O(x²) share
1 + m·x + O(x²) as their leading term, which explains the observed
degeneracy.

Only A04 (volume-cumulative `1 + m·(1 − a³)`) sits noticeably off the
principal mode because its a³ weighting concentrates the drift at late
times rather than at leading order in x.

### Cluster representative selection

We select the cluster champion by the composite score
S = −Δχ² + 0.5 · |proj₁|. Full ordering:

| Rank | ID  | Δχ²    | |proj₁|  | Score S |
|------|-----|--------|---------|---------|
| 1    | A12 | −21.62 | 0.478   | 21.86   |
| 2    | A17 | −21.26 | 0.353   | 21.44   |
| 3    | A16 | −21.13 | 0.454   | 21.36   |
| 4    | A01 | −21.12 | 0.427   | 21.33   |
| 5    | A06 | −21.12 | 0.456   | 21.35   |
| 6    | A05 | −21.03 | 0.402   | 21.23   |
| 7    | A20 | −20.72 | 0.534   | 20.99   |

**Champion: A12 (erf diffusion)** `ρ_DE/Ω_Λ = 1 + erf(m·x)`. This
single closed form is our L5 representative of the entire alt-20
drift class.

The SVD spectrum and principal mode shapes are plotted in
`paper/figures/l5_alt_class_svd.png`.

## A.5 DESI DR3 Fisher forecast (L5-G)

Using the projected DR3 precision σ(D_A)/D_A ≈ 0.008,
σ(H)/H ≈ 0.010 (DESI 2024 forecast), we compute the Fisher
matrix on (w_0, w_a) at each candidate's best-fit:

| ID  | w_0     | w_a     | σ(w_0) | σ(w_a) | LCDM separation |
|-----|---------|---------|--------|--------|-----------------|
| LCDM| −1.000  |  0.000  | 0.016  | 0.071  |     0.00 σ      |
| C28 | −0.849  | −0.242  | 0.014  | 0.062  |     3.91 σ      |
| C33 | −0.984  | −0.262  | 0.018  | 0.084  |     3.12 σ      |
| A04 | −0.757  | −0.469  | 0.014  | 0.059  |   **7.98 σ**    |
| A17 | −0.895  | −0.178  | 0.015  | 0.065  |     2.75 σ      |
| A12 | −0.886  | −0.133  | 0.014  | 0.062  |     2.16 σ      |
| A05 | −0.900  | −0.124  | 0.015  | 0.063  |     1.96 σ      |
| A01 | −0.899  | −0.115  | 0.015  | 0.063  |     1.84 σ      |

**Q9 (≥ 2 σ LCDM separation) pass-list**: C28, C33, A04, A17, A12.
**Q9 borderline**: A05 (1.96 σ).
**Q9 fail**: A01, A03, A06, A08, A09, A11, A13, A15, A16, A19, A20 —
the rest of the cluster.

**Pairwise discrimination**. The (w_0, w_a) separation between C28
and C33 is only 0.19 σ at DR3 precision, meaning **DR3 cannot
distinguish C28 Maggiore RR from C33 f(Q)** on the background level
alone. The alt-hard cluster (A01, A05, A06, A12, A16, A20) is
mutually indistinguishable at < 0.5 σ. A04 stands apart from all
others at ≥ 3 σ.

The Fisher ellipses in the (w_0, w_a) plane are plotted in
`paper/figures/l5_dr3_forecast.png`.

## A.6 Cosmic shear S₈ channel (L5-D)

All alt-20 candidates have μ(a,k) = 1 structurally; the only effect
on S₈ comes through the modified background changing Ω_m and the
growth normalisation D(a=1). The S₈ values are:

| ID  | Ω_m    | S₈     | Δχ²_WL vs LCDM  |
|-----|--------|--------|-----------------|
| LCDM| 0.3204 | 0.8381 |      0.00       |
| A04 | 0.3011 | 0.7719 |    −27.38       |
| A12 | 0.3090 | 0.7977 |    −22.18       |
| A01 | 0.3102 | 0.8018 |    −20.69       |
| A17 | 0.3119 | 0.8086 |    −17.88       |
| A05 | 0.3108 | 0.8039 |    −19.88       |

Every cluster member **numerically** improves the S₈ tension
(LCDM χ²_WL = 27.58 vs WL mean 0.766 ± 0.014), because the lower
best-fit Ω_m pulls S₈ ∝ √(Ω_m/0.3) downward. However this is a
**parametric artefact**, not a structural growth-sector fix: μ(a,k)=1
means the candidates inherit the same S₈ physics as ΛCDM. A genuine
resolution of the S₈ tension requires a non-trivial μ(a,k) ≠ 1
modification, which none of the alt-20 candidates provide.

**Notable exception**: C33 f(Q) teleparallel has best-fit Ω_m = 0.340,
giving S₈ = 0.891 — this **exceeds** the DES-Y3 3σ upper bound and
**fails K15** in addition to **failing Q10** (Δχ²_WL = +54.5) and
**Q11** (H₀ tension worsened to 0.085). C33 is demoted from Phase-5
main to borderline on the cosmic-shear front alone.

## A.7 Canonical drift class interpretation

The SVD result (n_eff = 1) and the Fisher discrimination result
(intra-cluster ≤ 0.5 σ on w_a at DR3 precision) together establish
that the alt-20 survivors form a **single canonical drift class**.
A single member suffices as the class representative, and we choose
A12 (`1 + erf(m·x)`) on the basis of (a) maximum |Δχ²|, and (b)
the error-function form has a clean diffusion interpretation
consistent with the SQMH vacuum-generation axiom L1 acting as a
stochastic source (see §2 and §A.8).

Interpreted within the SQMH framework:

- The **amplitude-locking** to Ω_m arises because the L1 metabolism
  continuity equation ṅ + 3Hn = Γ₀ − σ n ρ_m has its sink term
  proportional to ρ_m. The accumulated sink over cosmic history is
  ∫₀^a σ n ρ_m dt' ∝ Ω_m at leading order in (1 − a).
- The **closed-form shape** (linear, exponential, erf, sqrt, …) is
  a higher-order refinement of the L0 causal-diamond volume element;
  the data currently cannot distinguish these refinements, and DR3
  will still be unable to.
- The alt-20 family therefore represents the **SQMH-native minimal
  phenomenology**: zero new parameters, amplitude tied to Ω_m by the
  axioms themselves, single drift direction, Δχ² ≈ −21 improvement
  over ΛCDM — **indistinguishable from C28 Maggiore RR at the DR3
  level** despite having one fewer parameter.

## A.8 SQMH interpretation of the class champion A12

The error-function form `1 + erf(m·x)` arises naturally if the
metabolism source Γ₀ acts as a diffusion source on the vacuum density,
and one treats the cumulative drift from matter era to today as the
integral of a Gaussian kernel. The leading-order Taylor expansion,
erf(u) = (2/√π) (u − u³/3 + ...), gives
1 + erf(m·x) ≈ 1 + (2/√π) m·x at small x, which is a renormalised
version of the linear canonical form A01 with amplitude 2/√π ≈ 1.128.
The higher-order saturation at large x (erf → 1) prevents the drift
from growing unboundedly at a → 0, a structural advantage over the
bare linear form A01.

## A.9 Code availability

- `refs/alt20_catalog.md` — frozen 20-candidate catalogue
- `simulations/l4_alt/runner.py` — single-file L3+L4 runner
- `simulations/l4_alt/alt20_results.json` — L4 outputs
- `simulations/l5/alt_class/svd_reduction.py` — L5-F SVD driver
- `simulations/l5/alt_class/class_reduction.json` — SVD results
- `simulations/l5/forecast/dr3_fisher.py` — L5-G DR3 Fisher
- `simulations/l5/forecast/dr3_forecast.json` — DR3 numbers
- `paper/figures/l5_alt_class_svd.png`
- `paper/figures/l5_dr3_forecast.png`
