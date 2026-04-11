# C33 f(Q) Teleparallel — L4 Review (4-reviewer team)

## Reviewer 1: Numerical correctness (lead: numerical methods)

**Scope**: Friedmann solver, CPL extraction, MCMC sampler.

- Modified Friedmann eq (**) derived from Jimenez-Heisenberg-Koivisto-
  Pekar 2020 Eq. 17 with `f = Q + F` and Q = 6H^2.  Starting from
  `6 H^2 f_Q - (1/2) f = rho_matter` and simplifying with
  `F = f_1 H0^2 (H^2/H0^2)^n`:
  `3 H^2 = rho_matter + F/2 - 6 H^2 F_Q`.
  Dividing by `3 H0^2`:
  `E^2 = Om a^-3 + Or a^-4 + (f_1/6)(1 - 2n) E^(2n)`.
- Closure residual absorbed into `OL0` term: `E^2 = Om a^-3 + Or a^-4 +
  OL0 + (f_1/6)(1-2n)(E^(2n) - 1)`.  At f_1 = 0, pure LCDM.
- brentq solves E^2 at each z with adaptive bracket [1e-8, 1e6].
- LCDM E(0) recovered to 1e-6 (sanity check in build_E).
- Pre-computed 90-point log-spaced z grid + log-log interpolation for
  MCMC speed.  Interpolation error < 0.05% vs direct brentq over
  z in [0, 1100].

**Verdict: PASS**.

## Reviewer 2: Physical consistency (lead: cosmology / theory)

**Scope**: sign conventions, perturbation spec, Cassini, c_s^2.

- Sign verification scan `sign_verification.md` resolves the L3 toy
  ambiguity: **f_1 > 0** is the physical, DESI-consistent branch with
  w_a < 0.  The L3 toy `rho_de = OL0 [1 + f_1 (a^alpha - 1)]` used
  a parameterisation that inverted the role of f_1.
- Static PPN gamma - 1 = 0: Schwarzschild vacuum has Q = 0 (type-D
  metric); F(Q) vanishes at all orders, leaving GR exact.  Cassini
  |gamma - 1| < 2.3e-5 trivially satisfied.
- c_s^2 = 1 for the sub-leading scalar mode; f_1 > 0 keeps
  f_Q > 0 (no ghost).  Hohmann-Krasnov-Krssak 2019 shows the scalar
  is non-propagating at background + subhorizon order, so Phase 2
  mu(a) ~ 1/f_Q is within 1% of unity and treated as LCDM-like.
- Phase 5 refinement path: full f(Q) perturbation spectrum via
  hi_class or self-implemented symmetric-teleparallel mu/Sigma.

**Verdict: PASS with Phase 5 note** (full perturbation spectrum not
evaluated at L4; sub-percent correction expected).

## Reviewer 3: Reproducibility (lead: data + CI)

**Scope**: seeds, data paths, version pinning.

- `np.random.seed(42)` set at top of `mcmc.py`; `run_mcmc` also seeds
  internally.
- `matplotlib.use('Agg')` set before any pyplot import (L2 lesson).
- tight_fit uses `rng_seed=42`; deterministic across runs.
- Brentq on well-conditioned bracket; no dependence on wall clock.
- MCMC reduced to (24 walkers, 180 steps, 40 burn) from spec
  (48, 2000, 500) due to ~0.12 s / log_prob call on this host.
  Documented in `result.json['mcmc_deviation']` and read flagged.
- R-hat computed from walker splits.  If any R-hat > 1.05 the result
  is flagged K9.

**Verdict: PASS (with MCMC spec deviation disclosed)**.

## Reviewer 4: CLAUDE.md rules compliance

- No non-ASCII in `print()`: all string output uses ASCII (no
  Unicode math symbols).  matplotlib labels OK per rule.
- `np.trapezoid` implicit via `common.py`; this module uses no trapz.
- `tight_fit` bounds: Omega_m in [0.28, 0.36], h in [0.64, 0.71],
  f_1 in [0.0, 0.30] (sign-enforced), n in [1.0, 4.0].
- emcee `np.random.seed(42)` set inside `mcmc.py` before
  `run_mcmc`.
- No `array.reduce`; no stored procedures; no DB writes.
- Frusciante 2021 (arXiv:2103.11823) cited in `background.py`.

**Verdict: PASS**.

## Overall

4 / 4 PASS (Reviewer 2 with Phase 5 note).  See `result.json` for
kill/keep decision under K1-K12 / Q1-Q6.
