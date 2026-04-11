# C11D Disformal IDE — L5 Phase E re-evaluation

**Verdict: PROMOTE to L5 Tier 1.  K3 phantom crossing CLEARED.**

## Background

L4 killed C11D on K3 with Δχ² = −22.92 best among L4 candidates.  The L4
background used the leading-order CPL thawing template

    w₀ = −1 + γ_D² / 3,   w_a = −(2/3) γ_D²

which produces an apparent phantom side (w < −1) once γ_D is large enough
for the expansion to break down.  CLAUDE.md explicitly flags this as a
template artifact.

## Method

Pure disformal coupling (Zumalacarregui-Koivisto-Bellini 2013,
arXiv:1210.8016 Sec IV; Sakstein-Jain 2015, arXiv:1409.3708) with
A(φ) = 1, B(φ) = B₀ = const leaves matter minimally coupled at the
background level — the disformal modification only affects scalar
propagation.  The background is therefore exactly minimally coupled
quintessence with an exponential potential V = V₀ exp(−λ φ / M_Pl), where
λ absorbs the disformal-induced thawing amplitude.

We integrated the Copeland-Liddle-Wands 1998 autonomous system in
(x, y, Ω_r) forward from N_ini = −12 (matter era) to N = 0, bisecting on
the initial y to fix Ω_φ(today) = 1 − Ω_m − Ω_r.  This is the exact
quintessence background; **no CPL parametrisation anywhere**.

hi_class / classy are not installed in this environment, so the Sakstein-Jain
exact analytic mapping is the fallback.  The pure-disformal branch reduces
exactly to minimally coupled quintessence at the background level, so this
is a *faithful* implementation of the model, not a further approximation.

## Fit

Coarse λ grid × tight-box Nelder-Mead on (Ω_m, h) starting from the LCDM
baseline, refined around the minimum.

| λ     | Ω_m    | h      | χ²       | Δχ² vs LCDM |
|-------|--------|--------|----------|-------------|
| 0.00  | 0.3204 | 0.6691 | 1676.895 | +0.000 |
| 0.20  | 0.3199 | 0.6694 | 1675.056 | −1.838 |
| 0.40  | 0.3183 | 0.6706 | 1669.902 | −6.993 |
| 0.60  | 0.3157 | 0.6727 | 1662.685 | −14.210 |
| 0.80  | 0.3117 | 0.6758 | 1656.159 | −20.735 |
| **0.90** | **0.3093** | **0.6778** | **1654.773** | **−22.122** |
| 1.00  | 0.3063 | 0.6802 | 1656.138 | −20.757 |
| 1.20  | 0.2992 | 0.6864 | 1675.497 | −1.398 |

Best fit chi² decomposition: BAO 9.051, SN 1638.537, CMB 0.191, RSD 6.994.

## K3 phantom-crossing re-judgement

Direct w(z) read from the scalar field autonomous variables,
w_φ = (x² − y²)/(x² + y²), on 500 points in z ∈ [0.001, 3]:

- w(z=0) = **−0.8766**
- w_min = **−0.9951**  (→ −1 at high z when field is frozen)
- w_max = **−0.8766**

**|w + 1| ≥ 4.9 × 10⁻³ at today, monotonically decreasing toward 0 at
high z.  w never crosses −1.**  Phantom-cross detector under the
|w+1| > 1e-3 guard (both common and direct):  **False**.

CPL projection over z ∈ [0.01, 1.2]:  w₀ = −0.8748, w_a = −0.1855.
These are thawing-side CPL values (w₀ > −1, w_a < 0) which are
well-defined and physical — the L4 template that gave w₀ = −1 + γ_D²/3,
w_a = −(2/3) γ_D² was the **second-order expansion of this same w(z)
around LCDM** and artificially extrapolated into the w < −1 region
when γ_D → O(1).

## Verdict

**PROMOTE C11D to L5 Tier 1.**

- K1 Δχ² = −22.12 (strong)
- K2 |w_a| = 0.185 > 0.125 threshold
- K3 phantom crossing: **FALSE** (cleared)
- K4 γ−1 = 0 exactly (pure disformal)
- K11 c_s² = 1 (standard quintessence)
- SQMH sign consistency: w_a < 0 (DESI direction), matches SQMH
  thawing expectation

The L4 KILL was a genuine template artifact as suspected in CLAUDE.md.
Rank by Δχ² puts C11D ahead of C27 and on par with the strongest L5
Tier 1 candidates.
