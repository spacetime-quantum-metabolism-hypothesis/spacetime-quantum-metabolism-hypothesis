# L4 C27 Review — Deser-Woodard non-local gravity

Four-reviewer checklist (writer: A; critics: B/C/D).

## Reviewer A (writer) — numerical

- Background integrates (U, U', V, V') in e-folds over N in [-7, 0] on 401 points; RK45 rtol 1e-8.
- Self-consistent iteration (up to 6 passes) couples auxiliary fields to the modified Friedmann via f(U) = c0 tanh((U-X_shift)/dX).
- tight_fit uses the common fitter with tight box Om in [0.28,0.36], h in [0.64,0.71]; theta bounds documented in mcmc.py.
- Smoke test: build_E returns monotone finite E(z) at z = 0, 0.1, 0.5, 1, 2, 10.

**Verdict: PASS**

## Reviewer B — physical

- Localization scheme follows Nojiri-Odintsov 2008 / Koivisto 2008; auxiliary U = box^-1 R with box in e-folds written as -H^2 (U'' + (3+h1) U').
- Matter-era initial conditions U = U' = 0 match Deser-Woodard's requirement that nonlocal sector is dormant at high z.
- Cassini gamma-1 = 0 justified by auxiliary freezing in Ricci-flat Schwarzschild (Koivisto 2008 Sec IV.B).
- Caveat: the modified Friedmann uses a leading 1 + f(U)/2 denominator (not the full Dirian 2015 non-linear form). Flagged in result.json.notes.

**Verdict: PASS (with Phase 5 caveat)**

## Reviewer C — reproducibility

- Uses common.run_mcmc which seeds numpy.random.seed inside the call.
- Script entry also calls np.random.seed(42) before tight_fit.
- All outputs (result.json, mcmc_posterior.json) UTF-8 with ensure_ascii = False but free of non-ASCII.
- Prints contain no unicode (cp949-safe).

**Verdict: PASS**

## Reviewer D — CLAUDE.md rules

- np.trapezoid not used; uses CubicSpline and np.gradient only.
- emcee seed is set inside run_mcmc (common.py line 213).
- No reduce / lodash issue (Python).
- Matplotlib not imported (no figure emission here).
- DB reads: none touched.

**Verdict: PASS**
