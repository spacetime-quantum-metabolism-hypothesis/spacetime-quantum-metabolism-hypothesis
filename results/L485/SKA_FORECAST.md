# L485 — SKA 21cm Cosmic Dawn Forecast (Pre-Registration)

**Pre-registration timestamp (UTC):** 2026-05-01T13:48:31Z
**Local date (KST):** 2026-05-01
**Paper hook:** §4.5 mid-term falsifier P25 ("21cm post-EDGES")
**Repository commit:** see `git log -1` at registration time
**Author email of record:** genesos@gmail.com

> Honest one-liner: **SQT minimal predicts a SKA1-Low δT_b shift of order ~10⁻⁵ relative to ΛCDM at z = 10–15 (background channel only); SKA1-Low cannot detect this; the 21cm cosmic-dawn channel is a NULL falsifier for minimal SQT.** A perturbation-channel (μ, Σ) detection would not falsify SQT either, because SQT is structurally μ_eff ≈ 1 (paper §4.6). The EDGES depth is **not** sourced by SQT; the background channel is structurally orthogonal to the anomaly.

---

## 1. SKA Phase 1 21cm sensitivity (50–200 MHz)

- SKA1-Low frequency band 50–200 MHz maps to redshift z ≈ 6.1–27 for the
  rest-frame 1420 MHz line.
- Cosmic-dawn target window (z = 10–15) corresponds to ν ≈ 89–129 MHz.
- Projected thermal noise after ~1000 hr integration on coarse Δz ≈ 0.5
  redshift slices (Koopmans+2015 SKA1-Low Sci Case; Mertens+2020 LOFAR
  cross-check):
  σ_T(z=10) ≈ 0.5 mK,  σ_T(z=12) ≈ 0.8 mK,  σ_T(z=15) ≈ 1.5 mK.
- Foreground residuals dominate the global-signal noise floor at z ≳ 15;
  the values above are conservative thermal-only references and the
  *minimum* σ achievable in practice is larger.

These σ_T values are recorded as `ska1_sigma_T_mK` in
`simulations/L485/forecast.json`.

## 2. SQT signal at z = 10–15 (background channel)

Standard differential brightness temperature (Furlanetto 2006 Eq. 1):

  δT_b ≈ 27 mK · x_HI · (1 − T_CMB/T_S) · √[(1+z)/10 · 0.15/(Ω_m h²)]
         · (Ω_b h² / 0.023) · (H_LCDM(z) / H(z))

The **only** SQT entry channel at the background level is the H(z) ratio.
SQT minimal (paper §5.1, w_q = −1 cosmic) yields **H_SQT(z) ≡ H_LCDM(z)** at
all z because the cosmological-constant-equivalent w_q = −1 is identical to
ΛCDM. We therefore evaluate two scenarios:

| Scenario       | (w₀, wₐ)   | Source                          |
|----------------|------------|---------------------------------|
| `LCDM`         | (−1, 0)    | Planck 2018 baseline            |
| `SQT_minimal`  | (−1, 0)    | Paper §5.1, identical to LCDM   |
| `SQT_DR3_edge` | (−1, −0.1) | Paper §4.4 inconclusive boundary |

`SQT_DR3_edge` is included **only** to bound the channel's discriminating
power assuming the V(n,t)-extension saturates the §4.4 boundary; it is
*not* a minimal-SQT prediction.

### Predicted δT_b (mK) — minimal model

| z   | E(z)_LCDM | δT_b_LCDM (mK) | δT_b_SQT_min (mK) | Δ(SQT − LCDM) |
|-----|-----------|----------------|-------------------|---------------|
| 10  | 20.493    | −28.20         | −28.20            | 0             |
| 12  | 26.320    | −30.66         | −30.66            | 0             |
| 15  | 35.929    | −34.01         | −34.01            | 0             |
| 17  | 42.869    | −36.07         | −36.07            | 0             |

### Predicted δT_b (mK) — DR3-edge bound

| z   | δT_b_LCDM | δT_b_DR3edge | ΔδT_b (mK) | rel.    | σ-detect (1000 hr) |
|-----|-----------|--------------|------------|---------|--------------------|
| 10  | −28.20    | −28.21       | −8.3 × 10⁻³ | 2.9 × 10⁻⁴ | 0.017 σ |
| 12  | −30.66    | −30.66       | −5.9 × 10⁻³ | 1.9 × 10⁻⁴ | 0.007 σ |
| 15  | −34.01    | −34.01       | −3.8 × 10⁻³ | 1.1 × 10⁻⁴ | 0.003 σ |

Even at the DR3 inconclusive-band edge, the cosmic-dawn 21cm channel
delivers <0.02 σ discrimination per redshift bin against ΛCDM. No plausible
SKA1-Low integration recovers a measurable signal.

## 3. EDGES anomaly (Bowman+2018, −500 mK at z ≈ 17)

| Quantity                                    | Value                       |
|---------------------------------------------|-----------------------------|
| Observed centroid depth                     | −500 ± 200 mK               |
| Standard astrophysical ceiling (Furlanetto) | ≈ −200 mK                   |
| H_SQT_minimal(z=17) / H_LCDM(z=17)          | 1.0000 (identical at w_q=−1)|
| H_SQT_DR3edge(z=17) / H_LCDM(z=17)          | 1 + 8.2 × 10⁻⁵              |

**Verdict:** SQT minimal cannot source the EDGES depth via the background
H(z) channel. The required δT_b factor of ~2.5 over standard astrophysics
demands either (i) a non-cosmological systematic (Hills+2018, Singh+2022
SARAS-3 non-confirmation) or (ii) excess radio background / DM-baryon
cooling — neither is part of SQT's predictive content. Channel is
structurally orthogonal.

This means EDGES is **neither evidence for nor against** SQT. We pre-register
this orthogonality so future referees cannot retroactively claim SQT
"explains" or "is killed by" EDGES.

## 4. σ-detection forecast summary

| Channel                                  | Forecast σ           | Verdict          |
|------------------------------------------|----------------------|------------------|
| SKA1-Low z=10 cosmic-dawn dT_b (minimal) | 0.000 σ              | NULL             |
| SKA1-Low z=12 cosmic-dawn dT_b (minimal) | 0.000 σ              | NULL             |
| SKA1-Low z=15 cosmic-dawn dT_b (minimal) | 0.000 σ              | NULL             |
| SKA1-Low z=10–15 (DR3-edge bound)        | < 0.02 σ per bin     | NULL (extension) |
| EDGES centroid (z≈17)                    | structurally orthogonal | n/a            |

**Conclusion:** P25 (post-EDGES 21cm) is recorded as a **NULL falsifier** for
the minimal SQT model. The channel cannot exclude or confirm SQT at the
background level in the SKA1-Low era. P25 should remain in §4.5 as a *channel
inventory* item, with an explicit note that the *minimal-model* sensitivity
is null. Any future positive 21cm detection must be evaluated against
perturbation-level (μ_eff, Σ_eff) modifications, which SQT structurally pins
to ≈ 1 (paper §4.6) — therefore a 21cm anomaly would *also* not vindicate
SQT through that route.

## 5. Pre-registration and triple-timestamp

Per paper §4.6 / §4.7 convention:

- arXiv submission ID: **TBD** (to be appended at next arXiv push).
- GitHub release tag: **TBD** — propose `v-L485-SKA21cm-2026.05`.
- OSF DOI: **TBD** — Phase-7 admin task, *before* SKA1 cosmic-dawn first
  light. Current SKA1-Low first-light schedule: ~2029.

UTC timestamp of *this* registration: **2026-05-01T13:48:31Z**.
This file is committed to the public repository as the on-chain anchor.

## 6. Honesty disclosures

- The σ_T figures (0.5–1.5 mK at z = 10–15) are *literature projections*,
  not L485-derived noise simulations. They are bracketing values; real
  SKA1-Low foreground residuals will worsen them.
- The H(z) ratio is computed analytically (CPL form for the DR3-edge case),
  not from a coupled scalar-field solver. For w_a = −0.1 at z = 10–15 the
  CPL form is sub-percent accurate, well within the channel's null-falsifier
  margin.
- No prior L-result coefficient has been imported. The only knobs touched
  are (Ω_m, h, Ω_b h², w_a) at standard / paper-§4.4 values.
- The verdict "NULL falsifier" is a *structural* statement about minimal
  SQT, not a claim about the SKA1-Low instrument.

## 7. Files

- `simulations/L485/run.py` — forecast computation.
- `simulations/L485/forecast.json` — full numeric output.
- `results/L485/SKA_FORECAST.md` — this document.

## 8. Paper §4 P25 update (proposed)

Replace §4.5 line "Euclid f·σ_8, CMB-S4 lensing, ET GW scalar mode, 21cm
post-EDGES." with the same line plus a footnote / parenthetical:

> 21cm post-EDGES (P25) — pre-registered as **NULL falsifier** for the
> minimal model: SKA1-Low (z = 10–15, 1000 hr) sensitivity to the
> background channel is < 0.02 σ even at the DESI DR3 inconclusive-band
> edge (`results/L485/SKA_FORECAST.md`, 2026-05-01).

The paper edit itself is left for the next §4 audit pass; this file is the
source of truth for the verdict.
