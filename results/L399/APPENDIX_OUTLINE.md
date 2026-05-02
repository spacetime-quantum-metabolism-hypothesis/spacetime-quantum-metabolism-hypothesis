# Appendix A — Robustness diagnostics (outline)

정직 한 줄: Appendix A is the consolidated robustness audit of the Branch-B fit;
the L272 mock-injection result (100% false BB preference under data-driven
tertile anchors) is the load-bearing caveat and is reported up front, not
softened.

Sources: L272 (mock injection), L275 (prior sensitivity), L277 (PPC),
L278 (jackknife), L279 (bootstrap), L280 (SBC). No new computation in this
appendix; all numbers are imported from those sessions.

---

## A.0 Scope and reading guide

- What this appendix is: a robustness audit of the BB 3-regime fit reported
  in Sec 4 (headline ΔAICc = 99 from L208).
- What this appendix is **not**: a Bayesian-evidence comparison (CLAUDE.md L5/L6
  rule — Δ ln Z gap < Occam penalty for current data); a S_8 / weak-lensing
  diagnostic (CLAUDE.md L6 rule — μ_eff ≈ 1 cannot relieve S_8 in
  background-only fits); a re-derivation of the headline number.
- Reading guide: A.1 is the **single critical caveat**. A.2–A.6 are PASS
  diagnostics that establish *robustness of the fit* under the assumption
  that A.1's anchor-prior caveat is honored in the main text. They are *not*
  independent evidence that BB beats LCDM.
- Calibration triangle: L275 (prior shift) ↔ L279 (bootstrap CI) ↔ L280 (SBC
  rank uniformity) form a self-consistent posterior-quality triangle. L277
  (PPC) and L278 (jackknife) provide data-replication and leverage checks
  on top.

---

## A.1 Mock injection-recovery (source: L272) — CRITICAL

Opening claim, verbatim from L272: **N = 200 LCDM-mock realisations → 200/200
false Branch-B preference; median ΔAICc = 132.95 under data-driven tertile
σ_0 anchors.**

Side-by-side with the headline:

| Quantity | Value |
|---|---|
| Real-data ΔAICc(LCDM − BB), L208 | 99 |
| Mock LCDM median ΔAICc(LCDM − BB), L272 | 132.95 |
| Mock false-positive rate (ΔAICc > 10) | 200/200 |

Interpretation: the real-data preference (99) is *smaller* than the
worst-case false-positive expectation (132.95) when σ_0 anchors are
data-driven. The headline ΔAICc therefore cannot be claimed as "evidence
for BB" without the explicit anchor-prior protocol stated in Sec 4
("anchors predetermined, not fitted").

Caveats and resolution path:
- The L272 mock uses **data-driven tertile split** — worst-case overfitting
  probe; not the analysis the main text uses.
- The required follow-up is a theory-prior anchor mock (anchors fixed
  before seeing data). This is named in L272 REVIEW and is explicitly
  open in A.7.
- Until that follow-up exists, BB's ΔAICc advantage is *consistent with*
  flexibility-driven overfitting and *consistent with* a real signal; the
  data alone cannot distinguish.

---

## A.2 Prior sensitivity (source: L275) — PASS

4-prior grid (uniform / log-uniform × narrow / wide). Reported MAP shifts:

| Anchor | MAP | Max prior-driven shift |
|---|---|---|
| log σ_galactic | 9.561 ± 0.014 | (prior-independent) |
| log σ_cluster | 7.748 ± 0.045 | mild — single A1689 anchor |
| log σ_cosmic | 8.371 ± 0.008 | (anchor strong) |

Maximum shift across all priors and all regimes: **0.045 dex**, well below
the 0.3-dex pre-registered threshold for "prior-driven".

Honest framing: A.2 is the strongest robustness panel. The cluster anchor
remains the single residual fragility (see A.5).

---

## A.3 Posterior predictive checks (source: L277)

BB MAP simulation reproduces SPARC log σ_0 distribution:

| Statistic | Mock | SPARC | Verdict |
|---|---|---|---|
| Mean (dex) | 0.52 | 0.53 | PASS |
| Std (dex) | 0.95 | 1.03 | mildly underdispersed (~8%) |
| KS p-value | 0.18 | — | PASS (not rejected) |
| 90% PI coverage | 87% | nominal 90% | marginal — slight overconfidence |

Honest disclosure: 87% < 90% nominal is reported as marginal, not as PASS.
The 8% std underdispersion is consistent with the L204 outlier-galaxy list
(true noise is mildly larger than the BB model accounts for).

---

## A.4 Jackknife on SPARC (source: L278) — PASS with disclosure

- Per-galaxy leave-one-out shift: median 0.001 dex, max 0.018 dex.
- Maximum single-galaxy influence on the fit: **< 5%**.
- Top-5 most-influential galaxies removed: ΔAICc shift = −7
  (BB still preferred).
- **Q = 1 only subset (90 galaxies): ΔAICc(LCDM − BB) = 78** vs full 99.

Disclosure: the Q = 1 subset reduces BB's preference by ~21 ΔAICc
units. Not catastrophic, but non-trivial; reported numerically rather
than qualitatively. High-mass / late-type / distance-bias strata are
**not** jackknifed in this appendix (see A.7).

---

## A.5 Bootstrap σ_0 anchors (source: L279) — PASS

1000-bootstrap confidence intervals vs Hessian-based CIs:

| Anchor | Bootstrap CI | Hessian-vs-bootstrap agreement |
|---|---|---|
| σ_galactic | 9.55–9.57 (±0.01) | within 5% |
| σ_cluster | 7.6–7.9 (±0.15) | within 5% |
| σ_cosmic | 8.36–8.38 (±0.01) | within 5% |

Anchor uncertainties are not underestimated. The single residual weakness
is the cluster anchor (single A1689, ±0.15 dex log). Named follow-up:
**additional cluster anchors** — the obvious tightening path.

---

## A.6 Simulation-based calibration (source: L280)

100 prior samples → 100 mock datasets → 100 BB fits → posterior rank
uniformity test:

| Anchor | Rank-uniformity KS p | Verdict |
|---|---|---|
| σ_galactic | 0.34 | PASS |
| σ_cluster | 0.21 | PASS |
| σ_cosmic | 0.41 | PASS |

Coverage:
- 68% nominal → 67–71% empirical (well-calibrated).
- 95% nominal → 93–96% empirical (PASS).

Caveat (verbatim from L280): **100 rounds; budget-limited; 1000 rounds
recommended.** Reported here as a posterior-implementation calibration,
not as a posterior-quality conclusion.

---

## A.7 Limitations and open robustness items

Open follow-ups, named in plain text so a referee can find them in one
read:

1. **Theory-prior anchor mock** — L272 used data-driven tertile anchors
   (worst-case probe). The matching diagnostic with anchors fixed before
   seeing data has not yet been executed. This is the single most
   important open robustness item; the BB ΔAICc claim is conditional on
   it until run.
2. **Stratified jackknife** — high-mass / low-mass, late-type / early-type,
   distance-bias, M/L-ratio strata listed in L278 attack lines are not
   yet jackknifed.
3. **SBC under-sampling** — 100 rounds vs 1000 recommended; rerun in a
   higher-budget environment will strengthen A.6.
4. **Cluster anchor** — single A1689 dominates A.5; additional cluster
   anchors are the obvious extension.
5. **Out of scope by rule** — S_8 / weak-lensing relief (CLAUDE.md L6),
   Bayesian evidence vs Occam penalty (CLAUDE.md L5/L6), DR3 forecasts
   (CLAUDE.md L6 — no DR3 execution before public release; that
   discussion lives in Sec 7.1, not here).
