# L406 — 8-Person Next-Step Design

## A. S_8 mitigation paths — assessment

The team enumerated four candidate channels through which V(n,t) extension
could conceivably move μ_eff away from 1:

| # | Channel | Mechanism | Verdict |
|---|---|---|---|
| A1 | Dark-only conformal coupling (β grows with f_dark) | μ = 1 + 2β² | **structurally ≥ 1** → cannot reduce S_8. L406 grid 117 points confirms ΔS_8 ∈ [0, +X], never negative. |
| A2 | Disformal pure (A'=0) | μ = 1 (background ≡ minimal-coupled quintessence, ZKB 2013) | **null effect** — cannot mitigate. |
| A3 | Disformal with A'≠0 | non-trivial μ(k,a) | reopens γ-1 ≠ 0 → Cassini violation (CLAUDE.md L4). Forbidden. |
| A4 | Anisotropic stress / non-zero η - 1 | requires propagating extra dof | resurrects GW170817 c_T = c constraint (CLAUDE.md L6). Forbidden. |

**Conclusion**: every accessible mitigation channel is either
(i) μ ≥ 1 monotone (A1, cannot help), (ii) μ ≡ 1 (A2, no effect), or
(iii) ruled out by Cassini/GW170817 (A3, A4). **S_8 mitigation is
unreachable inside the SQT-allowed sector.**

This is a *structural prediction*, not a tuning gap.

## B. Euclid / LSST forecast (L406 simulation)

Baseline shift: ΔS_8 = +0.0114 (SQT vs ΛCDM), ξ_+(10') = +2.29%.

| Facility | σ(S_8) (lit.) | n-σ detection | Verdict |
|---|---|---|---|
| DES-Y3 (current) | 0.018 | **0.63σ** | INVISIBLE today — consistent with no current detection |
| LSST Y10 (~2032) | 0.0040 | **2.85σ** | MARGINAL 3σ — falsifier-grade evidence |
| Euclid IST (~2027) | 0.0026 | **4.38σ** | DETECT 3-5σ — **strong falsifier** |

Source: simulations/L406/run.py → results/L406/forecast_facilities.json.
σ(S_8) values: Euclid Collab. 2020 IST forecast, LSST DESC SRD Y10,
DES-Y3 official.

**Falsification clock**: ~2027 (Euclid DR1 cosmic-shear). If Euclid
measures σ_8 *higher* than ΛCDM by ~1%, SQT is consistent (very weak
signal). If Euclid sees no excess or σ_8 *lower*, SQT is excluded at
~4σ. Either outcome is publishable.

## C. Honest-framing strengthening

Recommended paper edits (8-person consensus):

1. **Abstract** — add one sentence:
   > *"The model structurally worsens cosmic-shear S_8 by +1.14%
   > (ξ_+ +2.29%); this is pre-registered as a 4.4σ Euclid DR1
   > falsification target."*

2. **§4.6 closing line** — append:
   > *"Within the SQT-allowed sector (Cassini + GW170817), every
   > μ_eff channel is ≥ 1 (L406 §A). S_8 cannot be mitigated
   > theory-side; the worsening is a robust prediction."*

3. **§6.1 row 14** — change "OPEN, LSST/Euclid 대기" to:
   > *"PRE-REGISTERED FALSIFIER: Euclid 4.4σ, LSST-Y10 2.9σ
   > (L406 forecast)."*

4. **§9 conclusion** — add explicit clause: *"This paper makes a
   falsifiable prediction with timeline ~2027."*

## D. Decision

- **Do NOT** attempt parameter mitigation (would be artefact; A1-A4 forbidden).
- **DO** quantify facility forecast in paper (B above).
- **DO** strengthen honest framing (C above).
- **Action items for 4-person execution team**: §3 below.

> Net effect: convert a perceived weakness into a publishable
> falsification badge. P(reject by Archetype A) drops from ~25% to ~10%.
