# L5 Alt-20 Interpretation: A17 — Adiabatic Pulse Drift

## Closed form

rho_DE(a) / Lambda_0 = 1 + Omega_m * (1 - a) * exp(-(1 - a)^2)

Zero free parameters.  See `refs/alt20_catalog.md` row A17.

## SQMH L0 / L1 derivation sketch

The adiabatic pulse form is the SQMH metabolism drift modulated by a
Gaussian adiabaticity envelope.  Physically, the metabolism channel is
most active near the matter-DE transition and suppressed both at early
times (matter era, where the channel has not yet "opened") and at
asymptotic future (a -> infinity, where the matter reservoir is depleted).
The Gaussian envelope exp(-(1 - a)^2) is the leading adiabatic correction
from the WKB expansion of the metabolism propagator in the N = ln a
variable (base.md §XVI.3 adiabatic limit).

Derivation sketch: starting from the SQMH metabolism equation

    d rho_DE / dN = Gamma_0(N) * rho_m(N)

and taking the adiabatic (slow-roll) limit where Gamma_0(N) / H varies
slowly across an e-fold, the leading-order WKB correction adds a Gaussian
weight centred at the transition epoch:

    Gamma_0(N) -> Gamma_0^{(0)} * exp(-(N - N_*)^2 / 2)

with N_* = 0 the transition e-fold (today).  The cumulative integral in
the slow-roll limit yields, to leading order in Omega_m,

    Delta(rho_DE / Lambda_0) ~ Omega_m * (1 - a) * exp(-(1 - a)^2).

The (1 - a) prefactor is the same linear drift as A01, and the exp(-x^2)
factor is the adiabatic Gaussian envelope from the WKB correction.

## Why amplitude locking to Omega_m is consistent

The prefactor Omega_m in front of the (1 - a) * exp(-x^2) structure is the
same reservoir amplitude as in A01: the matter density available at the
transition epoch.  The Gaussian envelope is dimensionless and adds no
free parameter, since its width is fixed at unity in e-fold units by the
WKB expansion (the natural scale is one e-fold, the same scale that
appears in the metabolism equation).  Hence A17 is still zero-parameter,
with the same L0/L1 locking as A01-A12.

## Distinctive features

Among the Alt-20 hard-K2 survivors, A17 has the largest |w_a| (~ 0.178 at
L4), indicating that the Gaussian envelope amplifies the drift near the
transition epoch and produces the strongest late-time acceleration
signature.  This makes A17 the most observationally distinguishable of the
canonical drift class, and a candidate for a DESI DR3 discriminator
(Phase L5-G Fisher forecast).

At late times (a >> 1, which is not physically probed but relevant for
asymptotic stability), the exp(-x^2) suppression returns the DE density to
Lambda_0, so A17 is automatically thawing with a finite asymptotic state.
This is a desirable SQMH feature: no runaway phantom behaviour.

## L4/L5 status

- L4 Delta chi^2 = -21.26, (w_0, w_a) = (-0.895, -0.178).
- L5 production MCMC: 16 walkers x 400 steps, 2-D, budget reduced.
- Strongest |w_a| signature in the Alt-20 hard class — recommended as
  the Alt-20 class representative for the DESI DR3 Fisher forecast in
  Phase L5-G if the SVD reduction supports n_eff = 1.

## References

- base.md §VI (metabolism), §XVI.3 (adiabatic WKB limit)
- refs/alt20_catalog.md A17 row
- `simulations/l4_alt/runner.py` ALT['A17']
