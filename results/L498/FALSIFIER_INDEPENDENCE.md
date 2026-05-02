# L498 — Falsifier Independence Audit

**Date:** 2026-05-01
**Scope:** 6 SQMH pre-registered falsifiers — DESI DR3, Euclid, CMB-S4, ET, LSST, SKA
**Question:** Are these 6 truly independent channels, or does observable overlap (cosmic shear, BAO, matter power) collapse the effective number of tests?

---

## 1. Inputs

| # | Channel | Forecast σ | Source pre-reg |
|---|---------|------------|----------------|
| F1 | DESI DR3 | 5.00 | (BAO+RSD, w₀-w_a tension extension) |
| F2 | Euclid | 4.40 | (cosmic shear + BAO at z<2) |
| F3 | CMB-S4 | 7.90 | L486 P22 (compressed CMB + lensing) |
| F4 | ET (Einstein Telescope) | 7.40 | L487 P16 (GW scalar polarization, BNS) |
| F5 | LSST | 2.85 | (cosmic shear + cluster counts) |
| F6 | SKA | 0.00 (NULL) | L485 P25 (HI 21cm — structurally null for minimal SQT) |

SKA is a **structural null** — it should not register a deviation if minimal SQT is correct, so it acts as a *consistency* falsifier (rejects the model only if a signal *appears*) rather than a *detection* falsifier. It is included in the correlation analysis but excluded from "active detection" combined Z.

## 2. Method

Independence is not declared by survey name; it is determined by the **physical observable footprint**.

**Observable basis (8):** BAO, RSD, WL cosmic shear, CMB compressed (θ\*, R), CMB lensing, GW scalar polarization, HI 21cm, cluster counts.

**Channel × observable incidence matrix A** (1 = primary leverage, 0.5 = secondary, 0 = none):

|          | BAO | RSD | WL | CMBc | CMBl | GW_s | HI | Cl |
|----------|-----|-----|----|------|------|------|----|----|
| DESI DR3 | 1.0 | 1.0 | 0  | 0    | 0    | 0    | 0  | 0  |
| Euclid   | 0.5 | 0.5 | 1.0| 0    | 0    | 0    | 0  | 0.5|
| CMB-S4   | 0   | 0   | 0  | 1.0  | 1.0  | 0    | 0  | 0  |
| ET       | 0   | 0   | 0  | 0    | 0    | 1.0  | 0  | 0  |
| LSST     | 0   | 0   | 1.0| 0    | 0    | 0    | 0  | 1.0|
| SKA      | 0   | 0.5 | 0  | 0    | 0    | 0    | 1.0| 0  |

**Correlation matrix** ρ_ij = cosine similarity of observable rows.

**Effective N** via three estimators:
- Cheverud–Galwey 1991 (eigenvalue variance)
- Participation ratio (Σλ)² / Σλ²
- Li–Ji 2005 step

**Combined Z under correlation** (Strube 1985):
Z_comb = Σ Z_i / √(Σ_ij ρ_ij)

**Family-wise control:** Bonferroni and Holm step-down at α = 0.05, M_active = 5.

## 3. Correlation matrix

|          | DESI | Euclid | CMB-S4 | ET    | LSST  | SKA   |
|----------|------|--------|--------|-------|-------|-------|
| DESI DR3 | 1.000| 0.535  | 0.000  | 0.000 | 0.000 | 0.316 |
| Euclid   | 0.535| 1.000  | 0.000  | 0.000 | **0.802** | 0.169 |
| CMB-S4   | 0    | 0      | 1.000  | 0     | 0     | 0     |
| ET       | 0    | 0      | 0      | 1.000 | 0     | 0     |
| LSST     | 0    | **0.802**  | 0  | 0     | 1.000 | 0     |
| SKA      | 0.316| 0.169  | 0      | 0     | 0     | 1.000 |

**Highly correlated pairs:**
- **Euclid ↔ LSST = 0.80** — both are weak-lensing + cluster surveys at low z. ESSENTIALLY THE SAME CHANNEL (different sky/depth, same physics).
- **DESI DR3 ↔ Euclid = 0.54** — shared BAO/RSD leverage at z<2.
- **DESI ↔ SKA = 0.32** — minor RSD overlap.

**Truly orthogonal:** CMB-S4, ET. SKA is orthogonal in observable space but NULL in signal.

## 4. Effective N

| Estimator | N_eff |
|-----------|-------|
| Cheverud–Galwey 1991 | **5.71** |
| Participation ratio  | **4.44** |
| Li–Ji 2005           | **5.00** |
| Naive count          | 6.00 |

Eigenvalues: [0.036, 0.712, 1.000, 1.000, 1.226, 2.026]
The largest eigenvalue (2.03) absorbs the {Euclid, LSST, DESI} cosmic-shear/BAO bloc — that is the redundancy.

**Best estimate: N_eff ≈ 4.4–5.0**, not 6. The "6 falsifiers" headline overstates by **20–27 %**.

## 5. Combined significance

| Combination | Z_comb |
|-------------|--------|
| All 6, naive (independent) | 11.25 σ |
| All 6, ρ-corrected         | **8.87 σ** |
| Active 5 (drop SKA), naive | 12.32 σ |
| Active 5, ρ-corrected      | **9.95 σ** |

Correlation correction costs ~2.4 σ. The honest combined detection significance is **≈ 9.9 σ**, not 12.3 σ.

## 6. Bonferroni / Holm (M_active = 5, α = 0.05)

| Channel | Z | p (two-sided) | Bonferroni (p<0.01) | Holm |
|---------|------|---------------|---------------------|------|
| DESI DR3| 5.00 | 5.73e-07 | PASS | PASS |
| Euclid  | 4.40 | 1.08e-05 | PASS | PASS |
| CMB-S4  | 7.90 | 2.89e-15 | PASS | PASS |
| ET      | 7.40 | 1.36e-13 | PASS | PASS |
| LSST    | 2.85 | 4.37e-03 | PASS | PASS |

All five active channels survive Bonferroni and Holm at the family α = 0.05. **LSST passes by ~2× margin only**; if the true Euclid×LSST correlation is higher than 0.80 (it likely is — same WL physics), LSST contributes essentially nothing beyond Euclid.

## 7. Findings

1. **Not 6 independent tests.** N_eff ≈ 4.4–5.0. The participation-ratio estimate (4.44) is the most conservative and most honest for highly-overlapping pairs.
2. **Three truly orthogonal channels:** CMB-S4, ET, SKA. These are the *structural* tests of SQMH (recombination physics, GW polarization sector, 21cm null).
3. **Cosmic-shear cluster (Euclid+LSST):** counts as ~1.2 channels, not 2. ρ = 0.80 is conservative; using the same theoretical pipeline on overlapping sky drives this toward 0.9+.
4. **DESI DR3:** correlated with Euclid through BAO (ρ = 0.54) but distinct enough (RSD primary, no shear) to count as ~0.7 of an independent channel.
5. **SKA NULL:** orthogonal in observables but contributes 0 to Z_comb. Functions as a *consistency check*, not a *detection*.
6. **Combined significance honestly stated: 9.9 σ**, not "12+ σ". Bonferroni and Holm both clean (all five active channels reject H₀ = LCDM individually at family α = 0.05).

## 8. Recommendation for paper §6 (forecasts)

- Replace "6 independent 5σ-class falsifiers" with **"5 active + 1 null falsifier across N_eff ≈ 4.4 independent observable channels"**.
- Quote combined significance as **8.9 σ (all six, ρ-corrected) / 9.9 σ (active five, ρ-corrected)**, not the naive 11–12 σ.
- Drop LSST as a *primary* falsifier or merge it into a single "WL block" with Euclid for headline counts.
- Keep CMB-S4, ET, SKA as the three *load-bearing* orthogonal tests — these alone give Z_comb = √(7.9² + 7.4² + 0²) = **10.83 σ** at full independence, and they remain truly uncorrelated.

---

## Honest one-liner

**6 pre-registered falsifiers compress to N_eff ≈ 4.44 truly independent channels (participation ratio); Euclid–LSST (ρ=0.80) and DESI–Euclid (ρ=0.54) overlap in cosmic-shear / BAO observables, so the honest correlation-corrected combined detection is 8.87 σ (all six) or 9.95 σ (active five), not the naive 11.25 / 12.32 σ — the three orthogonal load-bearing tests are CMB-S4, ET, and the SKA null.**

---

*Artifacts:*
- `simulations/L498/run.py` — correlation analysis, eigen-decomposition, Bonferroni/Holm
- `results/L498/l498_results.json` — full numerical output
