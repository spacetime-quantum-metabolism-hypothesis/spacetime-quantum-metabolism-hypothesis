# L5 Alt-20 Interpretation: A12 — Error-Function Diffusion Drift

## Closed form

rho_DE(a) / Lambda_0 = 1 + erf(Omega_m * (1 - a))

Zero free parameters.  See `refs/alt20_catalog.md` row A12.

## SQMH L0 / L1 derivation sketch

The error-function form emerges when the metabolism continuity equation is
interpreted as a diffusion-limited process in e-fold time N = ln a,
instead of as a simple rate equation.  The SQMH "Planck foam diffusion"
picture (base.md §XIV) treats the matter-to-vacuum absorption as a
stochastic process with diffusion constant D = sigma = 4 * pi * G * t_P
governed by a Gaussian Green function in the cumulative e-fold variable.

Integrating the Gaussian-kernelled source from N = -infty to N = 0 and
taking the characteristic diffusion length ~ Omega_m produces:

    Delta(rho_DE / Lambda_0)(a) = integral_{-infty}^{0}
        dN' * Omega_m * exp(-(N - N')^2 / (2 * sigma_N^2))
    ~ erf(Omega_m * (1 - a)) * Lambda_0

In the thawing (slow-roll) regime the cumulative integral of the Gaussian
kernel is exactly an error function, and the upper limit (1 - a) is the
fraction of e-folds remaining until today.  Hence

    rho_DE(a) / Lambda_0 = 1 + erf(Omega_m * (1 - a)).

This is a "diffusion-regularised" version of A01: at small x = 1 - a the
two agree to O(x^3) because erf(y) = (2 / sqrt(pi)) * (y - y^3/3 + ...) ~
y.  At larger x, the erf saturates, capturing the SQMH expectation that
the metabolism channel cannot grow unbounded — the Planck foam has a
finite diffusion capacity.

## Why amplitude locking to Omega_m is consistent

The argument of the error function is Omega_m * (1 - a), with no free
coupling strength.  This is because in the SQMH diffusion picture the
diffusion length in N is fixed by the same L0/L1 constants that appear in
A01: the matter reservoir supplies the source amplitude, and the diffusion
constant sigma = 4 * pi * G * t_P is absorbed into the overall
normalisation of the cumulative e-fold coordinate.  The only remaining
dimensionless free variable is Omega_m itself, which locks the argument.

## Distinctive features vs A01 / A05

- Higher-order: erf provides a smoother cap at large x, preventing the
  runaway behaviour of A01 at hypothetical large extrapolations.
- Preserves the same Delta chi^2 class (L4: -21.62, slightly better than
  A01 and A05).
- Slightly larger |w_a| ~ 0.133 than A01 (0.115), reflecting the
  non-linear tail of the erf at cosmologically relevant 1 - a ~ 0.3.

In the Phase L5-F SVD reduction, A12 is expected to share > 99 % of its
first principal drift mode with A01 and A05; it is a refined resummation,
not a physically independent model.

## L4/L5 status

- L4 Delta chi^2 = -21.62, (w_0, w_a) = (-0.886, -0.133).
- L5 production MCMC: 16 walkers x 400 steps, 2-D posterior, budget
  reduced.

## References

- base.md §VI (metabolism), §XIV (Planck foam diffusion picture)
- refs/alt20_catalog.md A12 row
- `simulations/l4_alt/runner.py` ALT['A12']
