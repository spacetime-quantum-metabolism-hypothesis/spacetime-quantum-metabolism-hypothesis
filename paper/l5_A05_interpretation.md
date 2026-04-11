# L5 Alt-20 Interpretation: A05 — Sqrt Relaxation Drift

## Closed form

rho_DE(a) / Lambda_0 = sqrt(1 + 2 * Omega_m * (1 - a))

Zero free parameters: amplitude locked to Omega_m.  See
`refs/alt20_catalog.md` row A05.

## SQMH L0 / L1 derivation sketch

The sqrt form arises naturally when the metabolism equation is written in
terms of the square of the DE density rather than the density itself.
Starting from axiom L1 in the form

    d(rho_DE^2) / dN = 2 * Gamma_0 * rho_m * rho_DE / H

and using the SQMH saturation condition (Gamma_0 / H) -> 1 at the plateau,
plus rho_m / rho_DE ~ Omega_m / (1 - Omega_m) near the transition, the
leading solution is

    rho_DE(a)^2 = Lambda_0^2 * (1 + 2 * Omega_m * (1 - a) + O(x^2))

Taking the square root yields the A05 closed form.  The sqrt structure is
a direct consequence of SQMH's quadratic coupling of the metabolism source
term in the L1 continuity equation when expressed via rho_DE^2 — an
alternative bookkeeping that respects the same Planck-scale constant
sigma = 4 * pi * G * t_P and the same reservoir Omega_m.

Note that to first order in x = 1 - a, A05 reduces exactly to A01:
sqrt(1 + 2 * m * x) = 1 + m * x - (m^2 / 2) * x^2 + O(x^3).
Hence A05 is the "second-order resummation" of the same leading metabolism
drift.

## Why amplitude locking to Omega_m is consistent

Same derivation as A01, with the sole difference that the metabolism
equation is integrated in the rho_DE^2 representation.  The amplitude
factor 2 * Omega_m is not a free parameter — it is fixed by the
combinatorial count of ways a matter quantum can pair with two vacuum
degrees of freedom in the SQMH absorption channel (base.md §VI.2 Planck
pairing counting).  The overall normalisation sqrt(1 + ...) ensures that
rho_DE(a=1) = Lambda_0 exactly (today's DE density is the cosmological
constant), as required by the boundary condition at N = 0.

## Degeneracy with A01

In the L3-L4 scans A01 and A05 give Delta chi^2 differences of order 0.1,
both producing (w0, w_a) within (0.005, 0.01) of each other.  They cannot
be distinguished by current BAO+SN+CMB+RSD data; the SQMH interpretation
sees them as two representations of the same physical drift (linear vs
quadratic bookkeeping).  In Phase L5-F the canonical-drift-class SVD
analysis will formally merge them into a single effective degree of
freedom; A01 is the selected representative by convention.

## L4/L5 status

- L4 Delta chi^2 = -21.03, (w_0, w_a) = (-0.900, -0.124).
- L5 production MCMC (this directory): 16 walkers x 400 steps, 2-D
  posterior over (Omega_m, h).  budget_reduced=True.

## References

- base.md §VI (metabolism equation), §VI.2 (pairing counting)
- refs/alt20_catalog.md A05 row
- `simulations/l4_alt/runner.py` ALT['A05']
