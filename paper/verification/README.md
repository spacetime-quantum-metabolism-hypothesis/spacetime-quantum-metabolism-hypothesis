# SQT / SQMH — `paper/verification/`

External Quickstart: 5 stand-alone Python scripts that reproduce the
key falsifiable / consistency claims of the SQMH paper in **< 5 seconds each**
(mock injection: < 1 minute), with **only `numpy` and `scipy`** as deps.

> Internal cold-blooded audit (R1–R8 reports + raw evidence JSON) lives
> in `paper/verification_audit/` — not here. See paper §9.7 for the role
> separation.

---

## Quickstart

```bash
pip install -r requirements.txt
python verify_lambda_origin.py        # CONSISTENCY_CHECK (Lambda origin)
python verify_milgrom_a0.py           # PASS_STRONG (MOND a_0)
python verify_monotonic_rejection.py  # regime-gap rejection
python verify_mock_false_detection.py # honest false-positive caveat
python verify_cosmic_shear.py         # Euclid / LSST structural falsifier
```

Reference outputs are in `expected_outputs/*.json`. Re-running on a
fresh box should reproduce them within the documented tolerance
(seed = 42 fixed where stochastic).

---

## Script catalogue

| # | Script | Verdict / role | Runtime |
|---|--------|----------------|---------|
| 1 | `verify_lambda_origin.py` | `rho_q / rho_Lambda = 1.000000` — **CONSISTENCY_CHECK** (down-graded from PASS_STRONG per L412 — circular w.r.t. `rho_Lambda_obs`, see §5.2) | < 1 s |
| 2 | `verify_milgrom_a0.py` | `a_0 = c * H_0 / (2 * pi)` — **PASS_STRONG**, ~0.7 sigma | < 1 s |
| 3 | `verify_monotonic_rejection.py` | 3-anchor V-shape vs monotonic — `Delta chi^2 ~ 148` (regime-gap only; **not** SPARC-internal) | < 2 s |
| 4 | `verify_mock_false_detection.py` | LCDM mock x 200 -> 3-regime false-detection rate = 100 % — **honest caveat** for the SPARC `Delta AICc` advantage | < 1 min |
| 5 | `verify_cosmic_shear.py` | `+1.14 %` S_8 -> `+2.29 %` `xi_+(10')` — Euclid / LSST **structural falsifier** | < 1 s |

---

## Honesty notes (one line each)

- **Script 1** is **not** an a-priori prediction. `n_inf` is derived
  *from* `rho_Lambda_obs`, so `ratio = 1` is tautological.
- **Script 3** sigma is `Delta chi^2`-derived 1-DOF approximation; the
  paper's headline `~17 sigma` reflects a different anchor / error
  budget. Both reject monotonic well above the 5-sigma threshold.
- **Script 4** is a **caveat reproduction**, not a victory: a 100 %
  false-positive rate on null data means the SPARC `Delta AICc`
  advantage of the 3-regime model needs to be benchmarked against this
  baseline.
- **Script 5** is the cleanest **falsifier**. If Euclid / LSST
  measure `xi_+(10')` consistent with LCDM at the < 2 % level, SQMH is
  falsified in its current parametric form.

---

## Reproducibility checklist

- [x] Python 3.10+ (tested 3.11 / 3.13), numpy >= 2 (`np.trapezoid`),
      scipy >= 1.10
- [x] No GPU / no MPI / no MCMC required
- [x] `rng = np.random.default_rng(42)` fixed in script 4
- [ ] CI: `.github/workflows/verify.yml` (TODO)

---

See `README.ko.md` for the Korean version.
