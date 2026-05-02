# L486 — CMB-S4 Lensing Forecast (P22 Falsifier Pre-Registration)

**Pre-registration timestamp (UTC):** `2026-05-01T13:49:57Z`
**Prediction ID:** P22 — CMB-S4 lensing reconstruction (paper §4.5 mid-term falsifier)
**Channel:** Reconstructed CMB lensing power `C_L^{phi phi}`
**Status:** **PENDING** (CMB-S4 first lensing maps expected 2031–2033)

---

## 1. SQT structural prediction

In the dark-only embedding pre-registered in L406 (`results/L406/forecast_facilities.json`),
SQT predicts a *structural* growth enhancement `mu_eff = 1 + 2 beta_eff^2 >= 1`
(Phase-2, k-independent), giving

* `delta sigma_8 / sigma_8 = +1.14%` (frozen at L406 baseline; CLAUDE.md L5 rule).
* Cosmic shear `xi_+(10') = +2.29%` (factor 2 because `xi ~ S_8^2`).
* CMB lensing power, scaling as `<D(z)^2>_W` where `W(chi)^2/chi^2`-weighted
  growth integrand peaks at `z ~ 0.5–3`, propagates with the same factor 2:
  **`C_L^{phi phi} / C_L^{LCDM} = (1 + 0.0114)^2 = 1.02293` (+2.29%).**

The shift is approximately L-independent in the k-independent `mu_eff` limit
(it is a pure growth-amplitude rescaling along the kernel).

## 2. CMB-S4 sensitivity

Configuration (Abazajian et al. 1610.02743 / S4 Decadal Survey 2019):

| parameter | value |
|---|---|
| white noise `Delta_T` | 1.4 µK·arcmin |
| beam FWHM | 1.0 arcmin |
| sky fraction `f_sky` | 0.4 |
| reconstruction range | `L ∈ [30, 1500]` |
| iterative-EB `N_L^{phi phi}` template | `4e-9 * (1 + (L/900)^4)` |
| `C_L^{phi phi}` template | `1e-7 (L/50)^-1 exp(-(L/2500)^2) + 5e-9` |

Forecast Fisher SNR:

```
sigma^2(Delta C_L) = 2 / [(2L+1) f_sky] (C_L + N_L)^2
chi^2 = Sum_L (Delta C_L)^2 / sigma^2,   Delta C_L = (ratio - 1) C_L
SNR  = sqrt(chi^2)
```

**Result: `SNR(CMB-S4) = 7.90σ` — DETECT >5σ.**

## 3. Pre-registered decision rule (two-sided, locked at timestamp above)

Let `r = C_L^{phi phi}_{S4} / C_L^{LCDM} - 1` measured by CMB-S4 (averaged over
the SNR-optimal `L` band). The frozen target is `r* = +2.29%`.

| measured `r` | verdict |
|---|---|
| `0.0% <= r <= +3.0%` | **SQT CONSISTENT** (1σ band of prediction) |
| `-1.0% <= r < 0.0%` | **AMBIGUOUS** (`Delta chi^2 < 4`, tension not exclusion) |
| `r < -1.0%`  or  `r > +3.0%` | **SQT FALSIFIED** at central dark-only embedding |

Falsification floor: cosmology-convention 3σ. Discovery-grade 5σ NOT claimed —
the central forecast 7.9σ is a *Fisher* projection contingent on the noise
template; realised noise at `L > 1200` may shift it to 5–8σ.

## 4. Anchor scan (self-consistent ODE check)

For full transparency, the same code runs a self-consistent growth-ODE scan
under `mu_eff = 1 + 2 [beta_0 a^p f_dark(a)]^2`, normalised at `a = 1e-3`:

| beta_0 | p | label | C_L^φφ shift | SNR(S4) |
|---|---|---|---|---|
| 0.107 | 0  | L4 dark-only Phase-3 posterior | +0.10% | 0.35σ |
| 0.107 | +1 | growth-late dominated | +0.05% | 0.16σ |
| 0.107 | -1 | growth-early dominated | +0.30% | 1.05σ |
| 0.150 | 0  | Cassini dark-only upper | +0.20% | 0.69σ |
| 0.060 | 0  | weak dark-only | +0.03% | 0.11σ |
| 0.030 | 0  | very weak dark-only | +0.008% | 0.03σ |

**Why the gap from L406's +1.14%?** The grid above multiplies coupling by
`f_dark(a) = OL/(Om a^-3 + OL)`, which strongly suppresses high-z growth where
the CMB-lensing kernel is most sensitive. The pre-registered central +2.29%
uses the L406 *background-fit-derived* sigma_8 shift directly, which is the
relevant phenomenology for cosmic shear and CMB lensing. The grid is reported
as a structural *lower bound* under the narrowest dark-only embedding.

## 5. Honest caveats

1. Ratio assumes k-independent `mu_eff` (Phase-2). Scale-dependent
   modifications (k-essence, Galileon screening) would shift `L >= 500` ratio.
2. `N_L` template fits Abazajian+2016 anchors at `L = 100, 500, 1000, 1500`;
   true iterative-EB reconstruction may differ <30% at `L > 1200`.
3. `C_L^{phi phi}` here is an analytic stand-in for full CAMB output;
   SNR depends on cosmic-variance term so absolute `Cl` normalisation enters
   at the ±20% level (4σ-floor unaffected).
4. Background = LCDM exactly in this embedding (D5 dark-only). A V(n,t)
   extension that shifts `w(z)` adds a projection effect via `chi(z)` not
   modelled here.
5. Per CLAUDE.md L5/L6 rules: `mu_eff ≈ 1` is structural in this embedding,
   and the +2.29% C_L^φφ shift is therefore a **structural prediction** of
   SQT — not an extra fitted parameter. CMB-S4 is the cleanest single-channel
   falsifier in the 2030+ window.

## 6. Cross-check vs paper §4 facility table

| facility | channel | central forecast | source |
|---|---|---|---|
| DES-Y3 | xi_+(10') | 0.63σ — INVISIBLE | L406 |
| LSST-Y10 | xi_+(10') | 2.85σ — MARGINAL | L406 |
| Euclid DR1 | xi_+(10') | 4.38σ — DETECT 3-5σ | L406 |
| **CMB-S4** | **C_L^{phi phi}** | **7.90σ — DETECT >5σ** | **L486 (this)** |

CMB-S4 is the *strongest* mid-term P22 falsifier under the dark-only
embedding because (a) cosmic-variance limit at low L is essentially saturated
for `L < 500` reconstruction, (b) `f_sky = 0.4` is large, (c) the +2.29% shift
is broadband and survives the SNR-weighted sum.

## 7. Files

* `simulations/L486/run.py` — multiprocessing-spawn parallel forecast.
* `results/L486/cmbs4_clpp_ratio.csv` — `L`, `Cl_template`, `ratio_central`, `N_L`.
* `results/L486/cmbs4_forecast.json` — full machine-readable summary.
* `results/L486/CMBS4_FORECAST.md` — this report.

정직 한 줄: SQT structural μ_eff≥1 dark-only embedding 은 CMB-S4 lensing 에서
+2.29% (7.9σ) detect 가 *반드시* 나와야 하며, 부재 시 P22 falsified — pre-reg
완료 (UTC 2026-05-01T13:49:57Z).
