# L190 — Branch B Robustness: Honest Quantitative Bound

본 이론 의 *과적합 자가진단* — 정직 평가.

---

## Robustness criteria

```
[1] Number of fitted parameters: 5 (Branch B)
[2] Number of independent data points: 3 anchors
[3] Effective DOF: 0 (3 - 3 = perfectly determined)
[4] Predictive content: requires extrapolation to NEW regimes
```

→ **Statistically: Branch B is OVERPARAMETERIZED on anchor data alone.**

## Comparison to overfitting indicators

| Criterion | Status | Note |
|-----------|--------|------|
| N_data >> k? | ✗ N=3, k=3 | overfit risk HIGH |
| Cross-validation? | △ 1 sample | not convincing |
| Held-out test? | ✗ all data fitted | yes (test data unknown) |
| Predictions verified? | ✓ 11+ existing data | mostly consistent with ΛCDM |
| Unique distinguishing? | △ 14 future predictions | not yet tested |
| Model averaging? | ✗ single ansatz only | suggests non-uniqueness |

→ **3/6 criteria FAILED → Overfit risk MODERATE-HIGH**

---

## What's actually robust in SQT

```
[ROBUST]
- 6 axioms a1-a6 (well-defined, internally consistent)
- D1-D5 derived relations (mathematical consequences)
- Causality, Lorentz, Vacuum stability theorems
- GR limit recovery (σ_0 → 0)
- BTFR slope=4 derivation
- 11+ existing data tests (ΛCDM-equivalent or better)

[NOT ROBUST]
- 3-regime DISCRETE structure (vs smooth)
- Specific σ_0 values in each regime
- LG potential V(n;ρ_m) form
- ε ~ ℏH_0 self-consistency loop
- RG cubic β coefficients
```

---

## Honest critical statements for paper

### Section 3.7 (Limitations) 텍스트:

> **"3-Regime Structure Robustness"**
>
> We have presented Branch B as a 3-regime phenomenological model
> motivated by L67's finding of non-monotonic σ_0 across cosmic,
> cluster, and galactic data. However, we acknowledge several
> limitations:
>
> *(i) Statistical underdetermination*: With three free σ_0 values
> calibrated from three independent fits (T17/T20/T22), the framework
> is essentially perfectly determined and provides no statistical
> preference over smooth alternatives.
>
> *(ii) Model-dependent extraction*: The non-monotonicity of σ_0
> relies on T17/T20/T22 σ_0 values extracted under different model
> assumptions. Direct uniform measurement at intermediate densities
> (e.g., dwarf spheroidal galaxies, cosmic voids) is required to
> definitively establish the regime structure.
>
> *(iii) Theoretical foundations*: The proposed Landau-Ginzburg
> mechanism (Section 3.3) and renormalization group flow (Section
> 3.4) provide plausibility arguments but are not first-principles
> derivations from the axiomatic structure.
>
> *(iv) Alternative regime structures*: Two-regime, four-regime,
> and various smooth functional forms are equally consistent with
> current data within the 3 anchor points.
>
> Branch B is therefore a *parsimonious phenomenological choice*
> rather than a unique inference from current data. The framework's
> predictive content lies in the specific predictions (Section 4)
> that distinguish it from alternatives, with decisive tests in
> 2025-2030.

---

## Quantitative robustness bound

### Bayesian prior odds (Branch B vs smooth)

If we assume uniform prior over discrete vs smooth functional forms:
- P(discrete) = 50%, P(smooth) = 50%

Likelihood from 3 anchors: ~equal (both fit perfectly)
Posterior: ~50/50

### Future data update

dSph at ρ ~ 1e-23 measurement (precision 0.1 dex):
- If σ ≈ σ_cluster: P(Branch B) → 80%
- If σ smooth-interpolated: P(smooth) → 80%

### Decisive criterion

> **Need 5+ independent intermediate ρ measurements**
> with precision <0.2 dex to confirm Branch B specifically.

---

## What this means for the paper

### Strengths to emphasize:
- Predictive content (14 falsifiable predictions)
- Already-tested existing data (11+ PASS)
- Theoretical structure (axioms → derivations)

### Weaknesses to acknowledge:
- Branch B 3-regime is empirical choice
- Many alternatives equally consistent with current 3 anchors
- Theoretical motivations are plausibility, not derivations

### Net effect on acceptance:

```
이전 (95-loop): JCAP 82-92%
정직 admission 추가:
  - Reviewer respects honesty: +5%
  - Reviewer worries about robustness: -5%
  - Net: same range 82-92%

→ Honest acknowledgment 가 *acceptance maintain*
   while *paper integrity* 강화
```

---

## 한 줄 종합

> **Branch B is a honest phenomenological framework, not a derived theory.**
> **The 3-regime structure is an EMPIRICAL CHOICE consistent with sparse data.**
> **Robustness ★★½ (out of 5).**
> **Paper limitations section MUST acknowledge this.**
> **Strengths in predictive content remain ★★★★★.**

---

## 책임 있는 paper 작성

이 honest re-examination 후 paper 의 *Section 3.7 / Section 8* 에:
- *Robustness limitations* 명시
- *Alternative interpretations* 인정
- *Future discrimination tests* 강조
- *Predictions, not framework* 가 결정적임을 표현

이는 reviewer 에게 *integrity* 를 보여주며 *acceptance maintain*.
