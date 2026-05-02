# Contributing to SQMH

Thank you for your interest in the Spacetime Quantum Metabolism Hypothesis (SQMH) project. This is an open scientific exploration, and contributions of many kinds are welcome.

## Project Stance

SQMH is a falsifiable phenomenology effort. We value honesty over advocacy: negative results, KILL flags, and corrections to past claims are first-class contributions. The repository's history includes both confirmed advances and recorded falsifications — please preserve that pattern.

Before contributing, please read:

- `CLAUDE.md` — project rules, regression-prevention notes, and methodology.
- `results/` — past session reports (LXX) for context on what has already been tried.
- `README.md` — overall project orientation.

## Welcome Contribution Categories

### 1. NOT_INHERITED Pull Requests

Independent reanalyses, alternative templates, or new candidate models that are *not* derived from any existing LXX result are especially welcome. Tag the PR title with `[NOT_INHERITED]` and include in the description:

- A statement that you did not inherit equations, parameter values, or derivation paths from prior LXX sessions.
- The directional / physical motivation for your candidate.
- Independent toy verification (Python script + numerical output).

This category exists to counteract overfit-by-inheritance and is treated with high priority.

### 2. Translations

Translations of the README, FAQ, and selected results documents into other languages are welcome. Please:

- Place translated files under `docs/<lang-code>/` (e.g. `docs/ko/`, `docs/ja/`, `docs/zh/`).
- Keep filenames parallel to the English originals.
- Note in the PR which commit hash of the source you translated from.

Partial translations are accepted; mark unfinished sections clearly.

### 3. Figures

Improvements to plots, schematic diagrams, and paper-quality figures are welcome:

- Vector formats (SVG, PDF) preferred for diagrams; PNG at >=300 dpi for raster.
- Source files (e.g. matplotlib script, Inkscape `.svg`) should be included alongside the rendered output.
- Reuse existing color palettes and font choices where possible for consistency.
- Caption text in English; translated captions may be added in `docs/<lang>/`.

### 4. Verification Extensions

Independent re-runs and extensions of existing simulations strengthen the project:

- Re-run prior LXX simulations with different RNG seeds, alternate optimisers, or stricter convergence criteria and report any deltas.
- Extend candidate scans to new parameter regions (document the range and reason).
- Port a simulation to a different language / library and confirm numerical agreement.
- Add new validation tests under `tests/` (e.g. assertions on covariance ordering, dimensional checks).

Please attach raw output (chi2, AICc, posterior summaries) and the exact command used to reproduce.

## What We Generally Decline

- Cherry-picked results without code or seeds.
- Claims that omit a SQMH-consistency check (e.g. xi_q sign, beta_d sign conventions).
- Equations or parameters silently inherited from prior LXX sessions, presented as new.
- Removal of recorded falsifications from `results/` history.

## Pull Request Checklist

- [ ] Branch is up to date with `main`.
- [ ] New scripts run cleanly with the threading guard (`OMP/MKL/OPENBLAS_NUM_THREADS=1`).
- [ ] No Unicode in `print()` statements (matplotlib labels are fine).
- [ ] If your change modifies a regression-prevention rule, `CLAUDE.md` is updated in the same PR.
- [ ] Honest one-line summary: what worked, what did not.

## Code of Conduct

All participation is governed by `.github/CODE_OF_CONDUCT.md` (Contributor Covenant 2.1).

## Contact

Open a GitHub issue for questions, or use the discussion tab for open-ended scientific exchange.
