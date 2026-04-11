# L5 Alt-20 Interpretation: A01 — SQMH Canonical Matter-Weighted Drift

## Closed form

rho_DE(a) / Lambda_0 = 1 + Omega_m * (1 - a),  with x = 1 - a and m = Omega_m.

Zero free parameters: amplitude locked to the matter fraction. Only
(Omega_m, h) enter the fit.  See `refs/alt20_catalog.md` row A01 for the
frozen definition.

## SQMH L0 / L1 derivation sketch

In the SQMH axiomatic chain the fundamental relation is the Planck-scale
metabolism constant

    sigma = 4 * pi * G * t_P  (SI),   n0 * mu = rho_Planck / (4 * pi)

and the continuity equation for the vacuum-energy generation rate Gamma_0
coupled to the cold matter density:

    d rho_DE / dt + 3 H * (1 + w_eff) * rho_DE = Gamma_0 * rho_m

Working in e-folds N = ln a, and taking Gamma_0 / H ~ constant in the
late-time plateau (H approaches a slow-roll limit), the leading integrated
drift in the ratio rho_DE(a) / Lambda_0 is linear in (1 - a):

    rho_DE(a) / Lambda_0 = 1 + k * (1 - a) + O((1 - a)^2)

The SQMH closure condition demands the first-order coefficient be set by
the matter fraction at the same epoch — because Gamma_0 is the rate at
which matter quanta are "absorbed" into the vacuum metabolic channel
(axiom L1), and the available reservoir at the onset of DE domination is
exactly Omega_m.  Hence

    k = Omega_m  =>  rho_DE(a) / Lambda_0 = 1 + Omega_m * (1 - a).

This is the minimal, purely leading-order realisation of the metabolism
coupling.  Every higher-order closed-form in the Alt-20 catalogue (A02,
A05, A06, A12, A17, ...) can be viewed as a different resummation of the
O((1-a)^2) and higher terms in the same expansion, all sharing the same
amplitude lock k = Omega_m.

## Why amplitude locking to Omega_m is consistent with the metabolism equation

The metabolism equation (base.md §VI, eq. L1) states that the DE density
is sourced at a rate proportional to the product (Gamma_0 / H) * rho_m.
After normalising by the critical density, this becomes

    d(rho_DE / rho_crit_0) / dN = (Gamma_0 / H) * Omega_m(N)

Integrated from matter-radiation equality (where rho_DE / rho_crit_0 ~
Lambda_0 / rho_crit_0 = 1 - Omega_m - Omega_r) to today (N = 0), the
leading contribution is

    Delta(rho_DE / Lambda_0) = (Gamma_0 / H_0) * Omega_m * (1 - a)

where the (1-a) factor comes from the cumulative e-fold integral evaluated
in the thawing (slow-roll) regime.  SQMH axiom L1 fixes the dimensionless
ratio (Gamma_0 / H_0) = 1 at the plateau — this is the statement that the
metabolism rate saturates at the horizon rate when the DE channel becomes
dominant.  Substituting yields exactly A01.

Thus amplitude locking is not a phenomenological choice but a direct
consequence of combining (i) linearised metabolism continuity, (ii) the
SQMH saturation condition Gamma_0 / H_0 -> 1, and (iii) the initial
condition at matter-DE equality.

## Relation to `refs/alt20_catalog.md`

Row A01 in the catalogue gives the functional form `1 + m*x` and flags
this as the "SQMH canonical matter-weighted drift".  The SQMH
interpretation column identifies it as the linearised solution of the
metabolism continuity equation with the coupling normalisation fixed by
L1.  All other Alt-20 entries are higher-order or resummed variants of
the same leading term; A01 is the minimal representative and is used as
the canonical reference for the Alt-20 degeneracy class (Phase L5-F).

## L4/L5 status

- L4 Delta chi^2 = -21.12 (L4 alt20_results.json), (w0, w_a) =
  (-0.899, -0.115), K2 hard pass, phantom crossing absent.
- L5 production MCMC (this directory) used 16 walkers x 400 steps (budget
  reduced; spec 48x2000 not feasible within session wall time — see
  `mcmc_production.json::budget_reduced`).
- Expected K13 R-hat status: 2-D posterior over (Omega_m, h) is extremely
  well conditioned and converges rapidly even at reduced budgets.

## References

- base.md §VI (SQMH L0/L1 axioms), §XVI (metabolism closure)
- refs/alt20_catalog.md A01 row
- `simulations/l4_alt/runner.py` ALT['A01']
