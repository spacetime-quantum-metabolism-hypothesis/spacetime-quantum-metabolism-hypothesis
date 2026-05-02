# L507 — BBN Cross-Experiment Robustness for SQT ΔN_eff

**Date**: 2026-05-01
**Predecessor**: L83 (constant Γ_0, ΔN_eff ≤ 6e-32) and L149 (V(n,t) extension, ΔN_eff ≤ 1.1e-47)
**SQT characteristic prediction (this audit)**: ΔN_eff ≈ 10⁻⁴⁶

---

## 1. Standard channels — does SQT pass *each* independent measurement?

| Channel                       | 95% CL bound on \|ΔN_eff\| | SQT margin       | Verdict |
|-------------------------------|---------------------------|------------------|---------|
| Planck 2018 CMB (TT,TE,EE+lowE+lensing) | ≤ 0.17           | 1.7 × 10⁴⁵       | PASS    |
| Primordial He-4 (Aver+2021)   | ≤ 0.20                    | 2.0 × 10⁴⁵       | PASS    |
| Primordial D/H (Cooke+2018)   | ≤ 0.15 (tightest)         | 1.5 × 10⁴⁵       | PASS    |
| BBN combined (Pitrou+2018)    | ≤ 0.16                    | 1.6 × 10⁴⁵       | PASS    |

All four independent channels: **PASS_STRONG (≥ 45 orders of magnitude headroom)**.

Robustness conclusion: **cross-experiment robust, not a single-measurement artefact.**
The smallness of SQT's predicted ΔN_eff is structural (set by cosmological-constant–scale
ρ_DE at the BBN epoch z ≈ 10⁹), not tuned to any one experimental window.

## 2. Anomaly channels — can SQT *explain* the tensions?

| Anomaly                       | Preferred ΔN_eff       | SQT can explain? | Distance from SQT |
|-------------------------------|------------------------|------------------|-------------------|
| EMPRESS 2022 low He-4 (Y_p ≈ 0.237) | ≈ −0.5 (±0.5)    | NO               | 1.0 σ             |
| Li-7 problem (factor 3–5 high) | ≈ −0.4 (effective ±0.5) | NO              | 0.8 σ             |

SQT predicts ΔN_eff ≈ 0 to 46-decimal precision, so it **cannot generate** an anomalous
−0.5 shift. Important caveats:

- **EMPRESS** is in tension with Aver+2021 / Hsyu+2020 at ~2σ. Yeh+2023 reanalysis
  finds the EMPRESS preference for ΔN_eff < 0 weakens substantially. SQT's null
  prediction sits at ≈1σ from the EMPRESS central value — *consistent within errors*,
  not in conflict.
- **Li-7** is widely attributed to stellar atmospheric depletion (Korn+2006), not to
  primordial physics. SQT being unable to shift Li-7 is *not* a failure mode for any
  serious BBN theory.

## 3. Why this matters

The L83/L149 PASS_STRONG result is **not** an artefact of choosing the most permissive
single channel:

1. The tightest bound (D/H, 0.15) and the loosest bound (He-4 Aver, 0.20) differ by
   only ~30 %. SQT's prediction is 45 orders of magnitude below either.
2. EMPRESS — the only measurement that *prefers* a non-zero shift — cannot be
   "rescued" by SQT, but is also not the consensus value.
3. Li-7 is a stellar-physics problem; SQT's silence here is appropriate, not a
   weakness.

## 4. Honest one-line verdict

> **Cross-experiment robust** — SQT's ΔN_eff ≈ 10⁻⁴⁶ passes *all four* independent
> standard BBN/CMB channels (Planck, He-4 Aver, D/H Cooke, Pitrou-combined) with
> ≥45 orders of magnitude headroom; it cannot explain the EMPRESS-He4 or Li-7
> anomalies, but neither is required of any standard-physics extension.

## 5. Files

- `simulations/L507/run.py` — evaluator
- `results/L507/cross_exp_report.json` — machine-readable margins per channel
- Predecessor data: `results/L83/report.json`, `results/L149/report.json`

## 6. References

- Planck Collaboration 2018, A&A 641, A6 (Planck 2018 VI)
- Aver, Berg, Hirschauer, Olive, Pogge 2021, JCAP 03 027
- Cooke, Pettini, Steidel 2018, ApJ 855, 102
- Pitrou, Coc, Uzan, Vangioni 2018, Phys. Rep. 754, 1
- Matsumoto et al. (EMPRESS) 2022, ApJ 941, 167
- Yeh, Olive, Fields 2023 (EMPRESS reanalysis)
- Fields 2011, Annu. Rev. Nucl. Part. Sci. 61, 47 (Li-7 review)
