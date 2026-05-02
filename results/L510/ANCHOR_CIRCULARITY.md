# L510 — σ₀ Anchor Anti-Circularity Audit

**Date**: 2026-05-01
**Scope**: Three σ₀ Branch B anchors — cosmic 8.37, cluster 7.75, galactic 9.56 (dex, in m³/(kg·s)).
**Goal**: Determine whether the *measurement procedure* for each anchor is genuinely external to SQT, or whether it embeds a hidden SQT (or SQT-equivalent MOND-prior) assumption.

---

## TL;DR (one-line per anchor)

| Anchor | Value (log σ₀) | Procedure | Verdict |
|--------|---------------|-----------|---------|
| Cosmic | 8.37 ± 0.06 | Solve T17 self-consistency with ρ_Λ_obs(Planck) as input | **CIRCULAR (admitted §5.2)** — n_∞ derivation uses ρ_Λ_obs ⇒ σ₀ inversion is not an independent measurement |
| Cluster | 7.75 ± 0.06 | T20 σ₈(k) Lorentzian fit to LCDM linear-theory P(k) baseline | **PARTIALLY CIRCULAR** — assumes LCDM background + σ₀(k) parametric form; not an A1689-only lensing inversion despite paper attribution |
| Galactic | 9.56 ± 0.05 | SPARC fit of MOND-form a_tot = ½(a_N + √(a_N² + 4 a_N a₀)), then σ₀ = 4πG·c/a₀·β⁻¹ with β=1 | **HIDDEN MOND-PRIOR + SQT-internal D1 conversion** — the fit functional is MOND; σ₀ extraction uses SQT D1 (G = σ₀/4πτ_q) |

**Honest one-liner (요청)**: 세 anchor 중 *완전 외부 측정* 은 0개. cosmic 은 명시적 circular(§5.2 인정), cluster 는 LCDM-bridged + σ₀(k) parametric, galactic 은 MOND functional fit + SQT-internal D1 conversion (β=1 assumption).

---

## 1. Cosmic anchor (log σ₀ = 8.37)

### 1.1 Procedure (T17 cosmic-mean fit, L48)

1. Adopt Planck 2018 ρ_Λ_obs ≈ 6.0 × 10⁻²⁷ kg/m³ as **input**.
2. Solve coupled SQT background ODE
   - dn/dt + 3H·n = Γ₀ − σ₀·n·ρ_m
   - dρ_m/dt + 3H·ρ_m = +σ₀·n·ρ_m·ε/c²
   - H² = (8πG/3)(ρ_m + n·ε/c² + ρ_r) + Λ_eff/3
   under steady state n_∞ = Γ₀·τ_q.
3. Identification ρ_Λ ≡ n_∞·ε/c² (axiom D4) inverted for σ₀ given Γ₀ and τ_q via D1 (G = σ₀/4π·τ_q) closure.

### 1.2 Circularity diagnosis

The output σ₀ is the value that **forces** ρ_q,model = ρ_Λ_obs. In the paper this is logged as a *CONSISTENCY_CHECK* (paper §5.2 / L412 PR P0-1):

> "n_∞ derivation uses ρ_Λ_obs as input via axiom 3 → identification ρ_q/ρ_Λ ≡ 1.0000 by construction." (paper/base.md, claims_status row "Λ origin")

L402 attempted Path-α (independent UV cutoff derivation): **failed by 10⁶⁰** (vacuum catastrophe).
L412 down-graded the Λ origin claim from PASS_STRONG to CONSISTENCY_CHECK.

### 1.3 External verification possibility

- *In principle*: an independent measurement of (Γ₀, τ_q) from a non-cosmological channel (e.g. lab-scale quantum vacuum nucleation, or a clean BBN ΔN_eff bound that does not rely on Λ closure) would break circularity.
- *Available channels*: BBN Γ₀·τ_q bound (paper §4.1 row 2) — provides only an *upper limit* (ΔN_eff ≈ 10⁻⁴⁶), not a value. Insufficient to fix σ_cosmic independently.

**Verdict: TRUE CIRCULAR. No external measurement available. (Paper concedes.)**

---

## 2. Cluster anchor (log σ₀ = 7.75)

### 2.1 Paper-stated procedure (D-3)

paper/base.md D-3 maps Cluster → "A1689 (Limousin 2007) — strong + weak lensing".

### 2.2 Actual procedure (T20, L48)

The L48/L67/L68 source records show T20 is **not** an A1689 lensing inversion but a **σ_8(k) Lorentzian fit**:

> "T20 (cluster σ_8): σ_0(k) Lorentzian fit, 모델 의존" — L67/REVIEW.md line 53

> "L48 누적 σ_0 값 비교: T20 (cluster σ_8) = 5.6e7 ← 최소" — L67/REVIEW.md lines 17–22

The number 5.6×10⁷ ⇒ log = 7.748 ≈ 7.75 confirms identity with the "cluster" anchor.

### 2.3 Hidden inputs

a. **LCDM background**: σ_8(k) inference uses LCDM linear-theory P(k) as the comparison baseline. Any modification of growth or background by SQT enters as a residual that the fit then attributes to σ₀(k). The σ₀ value is therefore an LCDM-residual, not a model-independent observable.

b. **Parametric form**: Lorentzian σ₀(k) profile is an *ansatz*. L67 notes "모델 의존" (model-dependent).

c. **Single-source dominance**: paper §3.7 acknowledges "single-source dominance 59.7%" requiring multi-cluster joint (A1689+Coma+Perseus or 13-cluster pool) for recovery. **The current 7.75 anchor inherits this fragility.**

d. **Paper↔code attribution mismatch**: D-3 table claims A1689 strong+weak lensing; T20 actual procedure is σ_8 fit. This is a documentation drift, not an independent A1689 lensing inversion in the canonical SQT pipeline.

### 2.4 SQT-prior contamination check

The σ_8 fit does not import an SQT mass profile. However, the σ₀ → cluster value mapping presupposes that *whatever* σ_8 residual exists is due to an absorption-type coupling (axiom A1) rather than to nuisance astrophysics, baryonic feedback, or a different DM model. The Lorentzian width parameter is unconstrained by SQT axioms.

**Verdict: PARTIALLY CIRCULAR.**
- No SQT mass profile is forward-modeled into A1689 (so the *strict* A1689 inversion charge does not apply; rather the issue is that the canonical anchor is *not* an A1689 inversion).
- The actual σ_8(k) fit is LCDM-bridged + ansatz-dependent.
- An independent A1689-only strong+weak lensing σ₀ extraction *has not been performed* in the L48–L505 trail (no L*/A1689*.py found).

**External verification possibility: YES, in principle** — perform a forward A1689 SQT lensing fit (free σ₀, free cluster mass profile) and compare. Not yet done. **Recommended before publication if cluster anchor is cited as A1689.**

---

## 3. Galactic anchor (log σ₀ = 9.56)

### 3.1 Procedure (T22 / L49, fit_sqt + extraction)

`simulations/l49/l49_test.py`:

1. **Fit functional**: `_v_sqt(r, a_N, a_0) = ½ (a_N + √(a_N² + 4 a_N a_0))` (lines 145–157). This is the **standard simple-MOND interpolation function**. The code itself comments "SQT rotation velocity: simple MOND interpolation" (line 147) and `_v_mond_std` returns the same expression (line 165). **The functional form is identical to MOND; no SQT-axiom-derived modification of the rotation curve is used at the fitting stage.**
2. Per-galaxy free parameters: log a₀, Υ_disk. χ² fit over 175 SPARC galaxies (Q=1,2).
3. **σ₀ extraction** (line 491–492):
   ```
   sigma_0 assuming beta=1: a_0 = 1*c/tau_q → tau_q = c/a_0 → sigma_0 = 4piG*c/a_0
   ```
   This uses SQT D1 (G = σ₀/4π·τ_q) plus the SQT prediction (D5 partial) `a₀ = β·c/τ_q` with β fixed to 1.

### 3.2 Hidden assumptions

a. **MOND-prior in fit functional**: The χ² minimisation is on the MOND simple-interpolation curve. Any rotation-curve dataset that prefers a₀ ≈ 1.2×10⁻¹⁰ m/s² will return a tight log a₀ posterior whether or not SQT axioms are correct — the fit cannot discriminate SQT from vanilla MOND at the rotation-curve level (the code's `fit_mond_fixed` uses the *same* interpolation, line 270: `_v_mond_std(...)` returns `_v_sqt(...)`).

b. **β=1 conversion**: σ₀ ∝ 1/a₀ via D1 + (D5, β=1). β is a free coefficient in D5 (paper-stated as "1/π geometric, partial"). Fixing β=1 (rather than 1/(2π) per D5) is a **methodological choice** that propagates linearly into the σ₀ value.

c. **Comment in code**: line 492 claims "(not circular) — the T22 independent measurement". This claim is **misleading**: it is non-circular w.r.t. ρ_Λ_obs (the cosmic anchor's input), but it *is* internally dependent on (i) the MOND functional form and (ii) the SQT internal relation σ₀ = 4πG·c/a₀.

### 3.3 SQT-prior contamination check

- **MOND functional**: imported as fit shape ⇒ not derived from SQT in the fit pipeline. The paper §1.2.2 derives a₀ = c·H₀/(2π) post-hoc; the rotation-curve fit does not enforce this.
- **D1 closure**: σ₀ = 4πG·c/a₀ (β=1) is a pure-SQT internal identity. If D1 is wrong, σ_galactic is wrong.

**Verdict: HIDDEN MOND-PRIOR + SQT-INTERNAL CONVERSION.**
- The 175-galaxy a₀ posterior IS an external (observation-driven) quantity (a₀ ≈ 1.2×10⁻¹⁰ m/s² to ~5%, independent of SQT).
- The σ₀ value is **not** an independent measurement; it is a₀_obs reinterpreted through SQT D1 (β=1).
- *log σ_galactic = log(4πG·c) − log a₀ + log(1/β)*. The 9.56 ± 0.05 dispersion reflects a₀ posterior + Σ M/L systematics, not an independent σ₀ probe.

**External verification possibility: PARTIAL** — a₀ itself is externally measured. The SQT-specific σ₀ value is only verifiable by an independent τ_q measurement (e.g. ε = ℏ/τ_q ⇒ characteristic photon-graviton-SQT energy line; not currently observable).

---

## 4. Pairwise consistency

The three anchors are *not* three independent measurements of one σ₀; they are:
- Cosmic = ρ_Λ_obs ÷ (Γ₀·ε/c²) inverted via D1+D4 (circular)
- Cluster = LCDM σ_8 residual fit with Lorentzian σ₀(k) ansatz
- Galactic = MOND a₀_obs ÷ (1/4πG·c) via D1 + β=1

**No two anchors share the same measurement methodology.** The 1.81 dex spread (cosmic 8.37 / cluster 7.75 / galactic 9.56) — interpreted as Branch B "regime structure" — could equally reflect *three different methodological priors* applied to three different LCDM-residual datasets. L67 conclusion (non-monotonic pattern → single σ₀ DEAD) holds **only if the three anchors are accepted as equivalent measurements**, which this audit shows they are not.

---

## 5. Summary table — independence from SQT

| Anchor | LCDM background assumed? | SQT-internal closure used? | Functional ansatz imported? | Genuinely external? |
|--------|--------------------------|----------------------------|----------------------------|---------------------|
| Cosmic 8.37 | implicit (Planck ρ_Λ) | **YES** (D1 + D4 inversion uses ρ_Λ_obs) | — | **NO** (admitted §5.2) |
| Cluster 7.75 | **YES** (LCDM linear P(k)) | partial (axiom A1 implicit) | YES (Lorentzian σ₀(k)) | **NO (LCDM-bridged + ansatz)** |
| Galactic 9.56 | NO (rotation curves only) | **YES** (D1 + β=1) | YES (MOND simple interpolation) | **PARTIAL** (a₀ external; σ₀ via SQT D1) |

---

## 6. Recommendations

1. **Cosmic**: keep §5.2 circularity admission; do *not* re-promote Λ origin to a prediction. (Already done in L412.)
2. **Cluster**: either (i) actually run an A1689-only forward SQT lensing fit and report it as the canonical cluster anchor, or (ii) update paper D-3 table to honestly list "T20 σ_8 fit (LCDM-bridged, Lorentzian σ₀(k) ansatz)" instead of "A1689 strong+weak lensing". Current paper text and code procedure are inconsistent.
3. **Galactic**: clarify in §3 that σ_galactic is a₀_obs (genuinely external) re-expressed through SQT D1 with β=1; remove the "(not circular) — the T22 independent measurement" comment in `l49_test.py:492`, which overclaims independence.
4. **Branch B 17σ regime gap**: re-examine in light of methodological non-equivalence. The "POSTDICTION" tag in §6.1 row "Three-regime σ₀(env)" understates the issue — the gap may be a *methodological artifact* rather than a physical regime structure.

---

## 7. Final honest line

**진정 외부 측정: 0/3. cosmic 은 admitted-circular, cluster 는 LCDM-bridge + ansatz-dependent (paper 의 A1689 출처 표기는 실제 코드와 불일치), galactic 의 a₀ 는 external 이지만 σ_0 자체는 SQT-internal D1 (β=1) 환산값 — 세 anchor 의 1.81 dex 격차는 부분적으로 methodological prior 차이에서 올 수 있다.**
