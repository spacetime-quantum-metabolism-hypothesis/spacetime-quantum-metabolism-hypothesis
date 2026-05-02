# L503 — RAR a0 Universality Test (per-galaxy + environment + clusters)

**Verdict (one line, honest):** FAIL — a0 not universal; environment dependence and/or cluster mismatch.

## 1. Setup
- Data: SPARC 175 (Lelli et al. 2016 AJ 152 157); per-galaxy rotation curves.
- Functional form: McGaugh 2016 (M16). Upsilon_disk=0.5, Upsilon_bul=0.7.
- sigma_log floor = 0.13 dex (SPARC intrinsic scatter ~ 0.13 dex).
- SQT prediction: a0 = c H0 / (2 pi). At H0 = 67.4 km/s/Mpc -> a0 = 1.0422e-10 m/s^2 (log10 = -9.9821).
- Clusters: literature only (Tian-Ko 2016, Eckert+22). a0_cluster ~ (5-10) x a0_SPARC.

## 2. Per-galaxy a0 distribution

- N galaxies (with valid 4+ point M16 fit, non-boundary): **171**

| Statistic | Value (dex) |
|---|---|
| median log10(a0) | -10.0196 |
| weighted mean log10(a0) | -9.9114 |
| std log10(a0) | 0.438 |
| MAD-sigma | 0.333 |
| IQR-sigma | 0.357 |
| median per-galaxy fit sigma | 0.096 |
| intrinsic spread (std^2 - sigma_fit^2)^{1/2} | **0.427** |
| Delta(median - SQT) | **-0.038** |
| Delta(mean - SQT) | +0.071 |

## 3. Environment splits (Vflat-based)

| Bin | n | median log10 a0 | Delta vs SQT | std (dex) |
|---|---|---|---|---|
| dwarf_LT_proxy | 17 | -10.286 | -0.304 | 0.575 |
| normal_disk | 63 | -9.912 | +0.070 | 0.330 |
| bright_disk | 54 | -9.957 | +0.025 | 0.284 |

KS test (dwarf vs bright): stat=0.460, p=0.00516
Mann-Whitney (dwarf vs bright): p=0.000175

## 4. Cluster scale (literature, not re-analysed)

Tian & Ko 2016 ApJ 818 32; Eckert+22 A&A 662 A123; Pradel 2014.

a0_cluster / a0_SPARC ~ 5 - 10 -> log10 offset = +0.70 to +1.00 dex.

A single SQT prediction (a0 = c H0 / 2 pi) cannot reach cluster scale.
This is the standard MOND "missing baryon" problem and applies identically to SQT.

## 5. K-criteria

| K | definition | result |
|---|---|---|
| K1 | intrinsic spread <= 0.13 dex | FAIL (0.427) |
| K2 | |median - SQT| <= 0.05 dex | PASS (-0.038) |
| K3 | KS dwarf-vs-bright p > 0.05 | FAIL (p=0.00516) |
| K4 | cluster a0 within 0.10 dex of SPARC a0 | FAIL (lit: +0.70 to +1.00 dex) |

**PASS: 1 / 4**

## 6. One-line conclusion

**FAIL — a0 not universal; environment dependence and/or cluster mismatch.**

## 7. Outputs
- `simulations/L503/run.py`
- `results/L503/L503_results.json`
- `results/L503/UNIVERSALITY.md` (this file)
