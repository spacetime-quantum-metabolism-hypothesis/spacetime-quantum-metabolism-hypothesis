# L468 — Free Speculation: Information-Theoretic Origin of the Cluster-Scale Dip

**Status:** speculation only. No data fit, no claim. Toy code in
`simulations/L468/run.py`, numerical scan in `results/L468/scan_summary.json`
and `results/L468/scan.png`.

## 0. The puzzle being chased

Across L34 → L46x the recurring residual is a **scale-dependent dip** that
appears at cluster scales (R ~ 5–10 Mpc/h, equivalently σ_8-scale, k ~ 0.1–0.2
h/Mpc). Background-only and ψⁿ-style metabolisms can move amplitudes
globally but cannot localize a dip *at one scale*. So the question is not
"what is the right potential" but **"why does this scale know it is special?"**

## 1. The free guess

> The cluster scale is the scale at which the matter density field is
> **maximally uninformative** about the two cosmological anchors that bracket
> it (the linear regime ~80 Mpc/h, the deeply non-linear regime ~1 Mpc/h).
> SQMH metabolism's σ_0(R) coupling saturates a Cramer–Rao-like floor:
>
> 𝛔_0(R) ∝ 1 / √I_F(R) ,
>
> so where Fisher information is **minimum**, σ_0 is **maximum**, producing
> the observed dip residual at the cluster scale.

This is an information-theoretic re-statement: the dip is not a feature of
the *potential* but a feature of *what the field can encode about the
anchors*.

## 2. Why this is plausible

1. **Maximum-entropy distribution from given anchors.** If the only inputs
   to the metabolism are σ(R_lin) and σ(R_nl), then the maxent overdensity
   distribution at intermediate R has Shannon entropy

       H(R) = − w(R) ln w(R) − (1−w(R)) ln (1−w(R)),
       w(R) = (ln R − ln R_nl) / (ln R_lin − ln R_nl).

   H(R) is maximized at w = 1/2, i.e. at the **geometric mean** of the
   anchors:

       R★ = √(R_lin · R_nl) ≈ √80 ≈ 8.94 Mpc/h.

   That is exactly the canonical σ_8 scale.

2. **Fisher information is minimum at the same scale.** Treating
   ln σ(R) as a linear interpolant of the two anchors with weight w,

       I_F(R) ∝ w² + (1−w)² ,

   minimum at w = 1/2 (= 1/2). The toy run confirms numerically:
   `fisher_min_at_R = 8.66 Mpc/h`, `entropy_max_at_R = 8.66 Mpc/h`,
   `mutual_info_min_at_R = 8.66 Mpc/h`. All three info-theoretic
   diagnostics put their extremum at the cluster scale.

3. **σ_0(R) ∝ 1/√I_F(R)** is the Cramér–Rao saturation: a coupling that is
   forced to "absorb" what the field cannot constrain. So σ_0 peaks where
   the field carries least information — the cluster scale dip emerges
   automatically.

## 3. Mapping σ_0 to information theory (sketch)

The conjectured mapping is

      σ_0(R)  ↔  (Cramér–Rao bound on metabolism rate at scale R)
              ↔  1 / √I_F(R; θ_anchors)

with θ_anchors = (σ(R_lin), σ(R_nl)) — the two cosmological "knowns" that
SQMH metabolism takes as boundary conditions. Equivalently, in the
maximum-entropy framing, σ_0(R) is dual to the Lagrange-multiplier ratio
that enforces the anchor constraints, and is largest where the constraints
have least leverage.

## 4. Falsifiable handles (for follow-up sessions)

H1. **Locus stability.** If R_lin or R_nl shifts (e.g. via DR3 BAO scale
    or improved small-scale data), the predicted dip locus shifts as
    R★ = √(R_lin R_nl). L46x dip locus should track that geometric mean.

H2. **Width of the dip.** The width in ln R of the H(R) maximum is set by
    the second derivative of H at w = 1/2, giving FWHM_lnR ≈ 1.76 in log-R.
    L46x residual should not be sharper than this.

H3. **Anchor degeneration.** Inflating uncertainty on σ(R_lin) should
    deepen the dip (less Fisher info → larger σ_0); a tighter linear-regime
    prior should shallow it. Direct test: BAO-only vs BAO+CMB σ_0(R)
    fit residuals at R★.

H4. **No tilt prediction.** Pure background-only modifications cannot
    reproduce a localized dip; this hypothesis predicts that any model that
    fits L46x at R★ must, internally, contain a 2-anchor maxent / Fisher
    structure (or be observationally indistinguishable from one).

## 5. What this hypothesis is NOT

- Not a derivation of σ_0's absolute amplitude. Only the **shape** σ_0(R)
  ∝ 1/√I_F(R) is conjectured.
- Not a replacement for SQMH dynamical equations — it is an emergent
  re-reading of why the metabolism must have a scale-dependent coupling.
- Not yet calibrated to any L46x residual. The next session should compare
  H(R) and 1/√I_F(R) shapes against the actual dip residual.

## 6. Numerical artefacts

```
fisher_min_at_R       = 8.66 Mpc/h
entropy_max_at_R      = 8.66 Mpc/h
sigma0_max_at_R       = 8.66 Mpc/h
mutual_info_min_at_R  = 8.66 Mpc/h
expected_dip_scale    = √(1 · 80) = 8.94 Mpc/h
```

All four extrema collapse onto the cluster scale; this collapse is the
content of the hypothesis.

## 7. One-line summary (한국어)

클러스터 스케일은 두 우주론적 앵커(선형 ~80 Mpc/h, 비선형 ~1 Mpc/h) 사이에서
**Fisher 정보가 극소 / 최대엔트로피**가 발생하는 스케일이며, σ_0(R) ∝ 1/√I_F(R)
의 Cramér–Rao 포화로 dip 가 자동 생성된다는 자유 추측.
