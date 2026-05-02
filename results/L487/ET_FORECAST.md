# L487 — Einstein Telescope GW Scalar Mode Falsifier (P16) Pre-Registration

**Pre-registration timestamp (UTC):** 2026-05-01T13:47:30Z
**Paper anchor:** `paper/04_perturbation_theory.md` row C11D + `paper/base.md` §4.1 / §4.5
**Facility:** Einstein Telescope, ET-D design (Hild+ 2011, Maggiore+ JCAP 2020)
**Expected operation:** ~2030+
**Falsifier ID in paper:** P16 — "ET GW scalar mode" (paper/base.md L907)

> Honest one-liner: SQT-minimal predicts a *null* scalar mode (h_S/h_T = 0,
> pure disformal C11D); the 3.4×10⁻³ ceiling is a Cassini-derived upper
> envelope, not a positive SQT amplitude. ET cannot distinguish minimal-SQT
> from GR by null detection alone — but a positive detection above the
> envelope falsifies the C11D sector outright.

---

## 1. SQT structural prediction

| Branch | Source | h_S/h_T |
|---|---|---|
| Minimal SQT (pure disformal C11D) | Zumalacárregui-Koivisto-Bellini 2013; paper §4.1 row C11D | **0** (decouples at static order) |
| Cassini-saturating conformal residual | Will 2014 LRR Eq 36, |γ−1| < 2.3×10⁻⁵ | **≤ 3.4×10⁻³** (ceiling) |

Derivation: the conformal Brans-Dicke-like sector contributes
|γ−1| ≃ 2β_eff² (Will 2014). Saturating Cassini gives
|β_eff| ≤ √(2.3×10⁻⁵ / 2) ≃ 3.4×10⁻³, and the breathing-mode amplitude
ratio inherits this scaling at leading order.

The minimal model is a **null prediction**. ET sensitivity is forecast
against the *ceiling* so we can pre-register a clean falsification
threshold for the C11D sector.

## 2. ET-D sensitivity & forecast

Reference waveform: 1.4–1.4 M☉ BNS at D_L = 470 Mpc (z ≃ 0.1).
Single-event tensor SNR with ET-D (Hild+ 2011 fit, restricted PN inspiral
5–2000 Hz): **SNR_T ≃ 68.7**.

Fisher 1σ on the dimensionless amplitude ratio σ(h_S/h_T) = 1/(SNR_T·√N).

| Catalog assumption | N events | σ(h_S/h_T) | n_σ at ceiling 3.4×10⁻³ |
|---|---|---|---|
| Single fiducial BNS (470 Mpc) | 1 | 1.5×10⁻² | 0.23σ |
| 1 yr ET, loud only (SNR > 30) | 10³ | 4.6×10⁻⁴ | **7.4σ** |
| 1 yr ET, full BNS catalog | 7×10⁴ | 5.5×10⁻⁵ | **61.8σ** |

The "1 yr loud" sample is the conservative pre-registered benchmark.

## 3. Pre-registered decision rule (locked before ET first-light)

Let m = measured |h_S/h_T| from the 1-yr loud BNS stack (N ≃ 10³,
σ ≃ 4.6×10⁻⁴):

| Measurement | Verdict |
|---|---|
| m < σ (≈4.6×10⁻⁴) | **CONSISTENT** with SQT-minimal & GR (null branch) — does not discriminate |
| σ ≤ m ≤ 3.4×10⁻³ | **AMBIGUOUS** — within Cassini envelope, residual conformal allowed |
| m > 3.4×10⁻³ at ≥ 3σ | **C11D SECTOR FALSIFIED** — pure-disformal structure incompatible |

Triple-timestamp lock (per paper §4.6 protocol): arXiv submission ID +
GitHub release tag `v-preET-2026.NN` + OSF DOI, all created *before* the
first ET science run public-release announcement.

## 4. Caveats / honesty disclaimer

1. SQT-minimal is structurally a *null* prediction. ET non-detection
   does **not** uniquely confirm SQT — it is degenerate with GR.
2. The 3.4×10⁻³ ceiling assumes Cassini saturates; the actual SQT
   amplitude could be anywhere in [0, 3.4×10⁻³] without further
   constraint from current data.
3. The Fisher estimator assumes the scalar polarization channel is
   independent of the tensor waveform (Chatziioannou+ 2012 Eq 22
   simplified). Detector-network angular response degeneracies with
   inclination and sky position will inflate σ by ~O(2) — not
   modelled here, deferred to ET MDC analysis.
4. n=70 000 BNS/yr quoted only as an upper-end illustration; the
   pre-registered decision uses N=10³ loud events only.
5. No ad-hoc parameter tuning. n_σ values are the direct ratio of
   the Cassini ceiling to the Fisher 1σ, no fudge factors.

## 5. Outputs

- `results/L487/forecast.json` — machine-readable numbers
- `results/L487/ET_FORECAST.md` — this document
- `simulations/L487/run.py` — reproducible script (deterministic,
  no MC, runs in <1 s)

---

*Honest one-liner* — ET is a falsifier of SQT's pure-disformal structure
*only* in the positive-detection direction; null is degenerate with GR.
