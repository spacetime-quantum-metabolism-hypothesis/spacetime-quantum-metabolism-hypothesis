# L413 — 8-Person Next-Step Design (Euclid pre-registration procedure)

## A. What "pre-registration" must concretely mean

A pre-registered falsifier requires three independently verifiable
artefacts, all timestamped *before* Euclid DR1 cosmic-shear 2pt
official release:

1. **arXiv preprint commit hash** — the SQT paper version that contains
   the §4.6 + §6.1 row 14 + abstract Euclid-4.4σ claim. arXiv assigns
   a date-stamped submission ID; this is the primary timestamp.
2. **GitHub release tag** — a tag on the SQMH repository
   (e.g. `v-preDR1-2026.NN`) pointing to the commit that contains
   `simulations/L406/run.py`, `forecast_facilities.json`,
   `paper/base.md` §4.6 + §6.1 row 14. GitHub guarantees immutable
   tag-→ commit association.
3. **OSF (Open Science Framework) deposit** — the same forecast
   artefacts (`forecast_facilities.json`, `grid_S8_vs_Vparams.csv`,
   §4.6 + row 14 text excerpt) deposited as a single OSF project
   with DOI. OSF timestamps are independently notarised.

The three together provide a **3-source timestamp** that makes
hindsight-bias rejection structurally impossible.

## B. Concrete OSF / GitHub procedure (Phase-7 admin task)

Step 1 — GitHub release tag (executable now):
```
git tag -a v-preDR1-2026.NN -m "SQT pre-DR1 falsifier lock; Euclid 4.4σ"
git push origin v-preDR1-2026.NN
```
Tag points to commit containing L406 + L413 artefacts and the §4.6 +
row 14 update.

Step 2 — OSF deposit (manual, ~30 min):
- Create OSF project "SQT-2026-Euclid-falsifier".
- Upload: `forecast_facilities.json`, `grid_S8_vs_Vparams.csv`,
  `results/L406/`, `results/L413/`, paper §4.6 + row 14 excerpt.
- Mark project public, register (locks edits + assigns DOI).
- DOI cited in paper §4.6 footnote and abstract footnote.

Step 3 — arXiv submission:
- Submit `paper/` build with §4.6 + row 14 + abstract pre-registration
  clauses (4-person execution, §C below).
- arXiv submission timestamp = primary clock.

## C. Threshold confirmation: 4.4σ vs other choices

The team confirms (8-person consensus) the following decision rule for
the paper:

| Quantity | Value | Source |
|---|---|---|
| Central forecast n-σ (Euclid DR1) | **4.38σ** (round to 4.4σ in prose) | L406 forecast_facilities.json |
| Cosmology falsification floor | **3σ** | community convention |
| Detection-σ for SQT consistency window | ξ_+(10') = +2.29% ± 0.5% | L406 + V5 quadrature |
| Two-sided decision boundary (V6) | excess < +1% → exclude | NEXT_STEP §D |
| Discovery-grade (5σ) | NO | not claimed |

The threshold 4.4σ is the **central forecast value**, NOT a chosen
decision boundary. The decision boundary is 3σ (cosmology convention).
Paper prose must distinguish these.

## D. Two-sided pre-registered decision rule (for §4.6 + row 14)

For Euclid DR1 cosmic-shear ξ_+(10') measurement m relative to ΛCDM
prediction:

| m / ξ_+(LCDM) − 1 | Outcome | SQT verdict |
|---|---|---|
| +1.5% to +3.0% | within 1σ of SQT prediction | **CONSISTENT** |
| +0.5% to +1.5% | ambiguous, Δχ² ~ 4 | tension, not exclusion |
| −0.5% to +0.5% | LCDM-like | **SQT excluded ~4σ** |
| < −0.5% | anti-SQT | **SQT excluded > 5σ** |

This is a *pre-registered binary outcome rule*; no parameter tuning
post-hoc allowed. (CLAUDE.md L17 rule extends here: no role
pre-assignment in interpreting outcome either; if Euclid result lands
in the ambiguous band, full hi_class re-analysis is required, not a
re-fit of toy parameters.)

## E. Paper edits required (4-person execution remit)

1. **Abstract (paper/base.md §0 line ~612)** — add one sentence to
   "정직 disclosure" line:
   > *"σ_8 +1.14% structural worsening is **pre-registered as a 4.4σ
   > Euclid DR1 cosmic-shear falsifier** (L406 forecast; central
   > value 4.38σ, cosmology 3σ floor)."*

2. **§4.6 (paper/base.md ~line 791)** — replace the two-line stub with
   structured falsifier block including (a) 4.4σ central forecast,
   (b) Euclid DR1 timing 2026–2027, (c) two-sided decision rule (D
   above), (d) pre-registration triple-timestamp (GitHub + OSF +
   arXiv).

3. **§6.1.1 row 14 (paper/base.md ~line 858)** — replace
   `"OPEN, LSST/Euclid 대기"` with:
   > *"PRE-REGISTERED FALSIFIER: Euclid DR1 4.4σ central, 3σ floor,
   > LSST-Y10 2.85σ; two-sided decision rule §4.6; commit-tag
   > v-preDR1-2026.NN + OSF DOI (Phase-7 admin)."*

4. **(optional) §4.5 line "Euclid f·σ_8"** — clarify that this is a
   *separate* growth-rate channel from cosmic shear; cosmic shear is
   §4.6 + §6.1 row 14.

## F. Decision summary (8-person consensus)

- DO update §4.6, §6.1 row 14, abstract per §E above (4-person team
  executes).
- DO record OSF + GitHub-tag procedure as Phase-7 admin task
  (do NOT execute now; arXiv submission is the trigger).
- DO NOT advertise 4.4σ as "discovery-grade"; it is a 3σ-floor
  falsifier with 4.4σ central forecast.
- DO NOT re-attempt mitigation (L406 §A enumeration is closed).

> Net effect of L413 update: converts the row 14 "OPEN" into a
> quantitative **falsifiability badge** with dated decision rule.
> P(reviewer reject) drops from ~20% to ~10% (cf. L413 ATTACK_DESIGN
> archetype-summary table).
