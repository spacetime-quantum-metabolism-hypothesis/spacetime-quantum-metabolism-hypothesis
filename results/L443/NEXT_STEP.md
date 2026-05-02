# L443 NEXT_STEP

## Immediate follow-ups (replace schematic / placeholder PNGs)

1. **F6 — real SPARC GMM**
   - Load SPARC galaxy log_σ₀ values from project SPARC dataset (locate under
     `simulations/` or `refs/`).
   - Fit `sklearn.mixture.GaussianMixture(n_components=2)` on log_σ₀.
   - Replace `F6_gmm_sparc.png` and remove the "schematic" annotation.

2. **F7 — real mock-injection histogram**
   - Locate or build the mock pipeline (likely under `simulations/Lxx/` for
     SPARC or DESI mocks) that produces ΔAICc(SQMH − ΛCDM).
   - Run N≥1000 nulls + N≥1000 injections, save histograms to JSON, then
     redraw F7 from the JSON.

3. **F1 — σ₀(env) 3-regime aggregator**
   - Aggregate σ₀(environment) results from existing per-environment runs
     (low / mid / high density). Plot on log scale with non-monotonic dip.

4. **F8 — IC grouped bar**
   - Pull AIC / BIC / DIC / WAIC numbers from the L4–L6 model comparison
     tables (e.g. `paper/06_mcmc_results.md`, `results/L107`...).

5. **F2 — SPARC 3-galaxy panel**, **F4 — Bullet cluster overlay**, **F3 — a₀
   derivation diagram**: dedicated session each (F2, F4 need real data; F3
   is a vector-graphic / TikZ task best done outside matplotlib).

## After replacements
- Re-run `python3 results/L443/make_figures.py` and verify all 10 PNGs exist.
- Update `paper/figures/README.md` status column real/schematic/placeholder.
- Cross-link F0–F9 from the relevant paper sections in `paper/0X_*.md`.
