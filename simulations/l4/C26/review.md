# C26 Perez-Sudarsky Unimodular Diffusion — L4 Review

## Reviewer 1: Numerical correctness

- Backward ODE from N = 0 to N = ln(1e-4) for coupled (rho_m, rho_L)
  with source `J^0 = alpha_Q * rho_c0 * (H/H0)`.  `H/H0 = E(N)` is
  self-consistent inside the RHS: `E^2 = Or e^-4N + rho_m + rho_L`.
- RK45 with rtol = 1e-9, atol = 1e-12; dense_output enabled.
- 2000-point log-spaced grid -> cubic interp1d on (ln(1+z), ln E).
- E(0) = 1 enforced by boundary condition; sanity check |E(0) - 1| <
  1e-3 before returning.  Integration stable for alpha_Q in [0, 0.30].
- Positivity checks on rho_m and E^2 on the output grid; returns None
  on any negative or NaN entry.

**Verdict: PASS**.

## Reviewer 2: Physical consistency

- Perez-Sudarsky 2019 (arXiv:1711.05183) unimodular diffusion: source
  J^0 drives matter -> Lambda at rate alpha_Q * H, matching CSL-like
  "collapse" picture invoked as SQMH L0/L1 metabolism.
- Sign: alpha_Q > 0 enforced in tight_fit bounds and MCMC log_prob
  (matter -> Lambda = DESI w_a < 0 sign).  alpha_Q < 0 would reverse
  the flow and is rejected at prior level.
- Static PPN gamma - 1 = 0: no new propagating scalar mode (J^0 is a
  homogeneous source, not a field), so Einstein's equations are
  unmodified in the vacuum limit.  Cassini trivially passed.
- Perturbations reduce to LCDM at sub-horizon scales (Perez-Sudarsky
  Sec 4), mu(a) = 1, c_s^2 = 1.  No ghost, no gradient instability.

**Verdict: PASS**.

## Reviewer 3: Reproducibility

- `np.random.seed(42)` set.
- `matplotlib.use('Agg')` before any pyplot import.
- `solve_ivp` with fixed tolerances; no stochastic integration.
- MCMC reduced to (24, 180, 40) from spec (48, 2000, 500) due to
  ~0.18 s / log_prob call (ODE + chi^2 dominated).  Deviation logged
  in `result.json['mcmc_deviation']`.
- Seeds both at numpy top level and inside `run_mcmc`.

**Verdict: PASS (with MCMC spec deviation disclosed)**.

## Reviewer 4: CLAUDE.md rules compliance

- ASCII-only `print()`.
- `np.trapezoid` via common only.
- tight_fit bounds: Omega_m [0.28, 0.36], h [0.64, 0.71],
  alpha_Q [0.0, 0.30] (sign-enforced per redbook).
- `run_mcmc` seeded.
- Backward ODE with solve_ivp chosen over odeint (re-entrant,
  dense_output); positivity check prevents E^2 <= 0 silent pass.
- Perez-Sudarsky cited; SQMH sign convention documented.

**Verdict: PASS**.

## Overall

4 / 4 methodology PASS, but the **full-ODE background is physically
incompatible with the L3 closed-form toy**.  The L3 ansatz
`rho_m = Om a^-3 (1 - alpha_Q (1 - a^3))` corresponds to an implicit
source `J_N = -3 alpha_Q Om = const`, whereas the spec-mandated source
`J^0 = alpha_Q rho_c0 (H/H0)` integrates to a different rho_m(a)
history that drives chi^2 strictly worse than LCDM for any alpha_Q > 0
in the (Om, h) box [0.28, 0.38] x [0.64, 0.71].  Example: Om=0.35,
h=0.64, alpha_Q=0.094 yields chi^2 = 2643.8 (full ODE) vs 1667.1
(L3 toy) vs 1676.9 (LCDM).

**K10 fires**: the L3 toy was not a valid leading-order approximation
of the full unimodular-diffusion background for the relevant alpha_Q
range.  tight_fit correctly collapses to the LCDM limit alpha_Q = 0.
C26 is killed at L4.  Phase 5 revisit would require the alternative
source form `J^0 = alpha_Q H rho_m` (first-principles CSL coupling)
or a reformulation of the L3 ansatz.
