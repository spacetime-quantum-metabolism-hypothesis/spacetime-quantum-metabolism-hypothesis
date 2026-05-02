# L465 Free Speculation — Z_3 / 3-state Potts Internal Symmetry of n field

**Status**: free speculation. Not a derivation, not a fit. Recorded
under CLAUDE.md "최우선" rule as a *direction*, with a small toy MC for
internal consistency. No cosmological data is used.

**Date**: 2026-05-01
**Session**: L465

---

## 1. The cluster dip and the Z_2 default

The SQMH metabolism field `n(x, t)` has been treated throughout the
paper as a real scalar with at most a Z_2 reflection symmetry
(`n -> -n` or `phi -> -phi` for the dual scalar). All vacuum structure
and tunnelling arguments inherit that assumption: two phases (broken /
unbroken), one critical surface, one universality class (Ising-like in
3D continuum limit).

The cluster-scale dip in `Delta rho_DE / rho_DE` reported in L33–L46 is
*intermediate* — neither the cosmological-mean state nor the deeply
non-linear collapsed state, but a regime of partial saturation. Within
a Z_2 picture this can only be a *crossover*, not a true phase, because
Z_2 admits only two ordered vacua plus the symmetric one.

## 2. Speculation: n carries a Z_3 / 3-state Potts label

> Free guess: the metabolism field carries an *internal* Z_3 symmetry
> in addition to its real-valued amplitude. The order parameter is not
> a scalar `n in R` but a clock variable `s in {0, 1, 2}` (or a
> complex `psi = n e^{2 pi i s / 3}`), and the effective potential has
> three degenerate minima rather than two.

The proposal is purely structural: do not commit to a microscopic
origin in this note. Candidate frames (each is itself speculative):

- 3-state Potts ordering of vacuum metabolism direction (information
  triality: source / sink / null), in line with C28 / Maggiore-Mancarella
  non-local triplet structure noted in L6.
- Three sectors of dark matter / DE / baryon coupling, where the n
  field selects which sector currently dominates the local sink rate.
- Topological Z_3 from a discrete remnant of an SU(3)-style internal
  gauge of the dissipation current.

## 3. Phase diagram (Potts on a continuum lattice in 3D)

Standard results (Wu 1982 review):

- 3D q=3 Potts: **first-order** transition (latent heat, no scaling).
- 2D q=3 Potts: continuous, central charge c = 4/5 (tricritical
  Ising sister), order-parameter exponent beta = 1/9.
- A *generic* q=3 system therefore admits, near the transition, two
  metastable phases coexisting at T_c and a *finite jump* in the order
  parameter — this is the structural ingredient absent from Z_2.

In a coarse-grained cosmological setting where the n field has a
slowly varying effective temperature `T_eff(z, environment)`, three
operating regimes appear naturally:

1. Disordered (high T_eff): `<s>` averages out — homogeneous DE,
   cluster scales below threshold.
2. **Intermediate metastable** (T_eff ~ T_c, finite cluster size):
   patches of two of the three minima coexist; the macroscopic order
   parameter is suppressed but non-zero. **This is the proposed home
   of the cluster dip.**
3. Ordered (low T_eff, deep voids or deep collapsed halos): one of
   the three vacua dominates locally.

Because the q=3 transition in 3D is first-order, the intermediate
regime is not infinitesimally thin: a finite `Delta T_eff` window
exists where mixed-vacuum domains live with a characteristic
correlation length of order the cluster scale. This is the
*structural* reason the dip can be a real phase-like feature rather
than a tuned crossover.

## 4. Compatibility with the published Z_2 paper

- **Background cosmology**: the Z_3 picture reduces to the Z_2 / scalar
  picture after coarse-graining over the discrete label, because the
  three-vacuum free-energy density at large scales is symmetric under
  the residual Z_3 quotient and looks like a single effective
  `rho_DE(z)`. Background `w(z)` predictions are therefore unchanged at
  leading order. **No conflict with L33 BAO fit, L43 SN fit, L46
  joint.**
- **Cluster-scale phenomenology**: the dip in `Delta rho_DE / rho_DE`
  *is* the residue of the discrete label that the Z_2 coarse-graining
  averages over. The Z_2 paper's inability to host an "intermediate
  phase" is exactly the structural weakness this guess targets.
- **Cassini / PPN**: γ−1 is governed by linearised perturbations of the
  amplitude `|n|`, not the discrete label. Z_3 leaves γ untouched.
- **GW170817 c_T = c**: the discrete sector contributes no kinetic
  cross-term to the metric perturbation at quadratic order, so c_T = c
  is preserved.

**Potential conflict**: a *first-order* transition in 3D Potts produces
domain walls with surface tension. If domain-wall energy density were
cosmologically relevant, the model would be killed by the Zel'dovich
bound. The escape clause is that the wall tension `sigma_w ~ T_c^3`
must be set by a *sub-cosmological* scale (e.g. cluster virial energy
density `~ rho_crit * 200`), so that walls are confined inside
clusters and never tile the Hubble volume. **This is a real
constraint on the speculation and would have to be checked before any
paper submission.**

## 5. Universality comparison (from textbook + toy)

| Symmetry        | Universality      | Order              | Matches dip? |
|-----------------|-------------------|--------------------|--------------|
| Z_2 (Ising)     | Ising             | continuous in 3D   | crossover only |
| Z_3 (Potts)     | 3-state Potts     | **first-order in 3D** | yes — intermediate phase |
| 3-state clock   | XY (gapless 2D)   | BKT-like in 2D, Ising in 3D | partial |
| O(2) (XY)       | XY                | continuous         | no — wrong topology |

Z_3 / 3-state Potts is the *only* low-symmetry option that gives a
genuine intermediate metastable regime as an equilibrium phenomenon
rather than a crossover.

## 6. Toy MC sanity check

`simulations/L465/run.py` runs a 2D 24×24 Potts MC for q=2 (Ising) and
q=3 (Potts) and writes `potts_scan.csv` + `potts_phase.png`. The toy
is 2D not 3D, so it sees the *continuous* q=3 transition rather than
the first-order one — but the order-parameter curve for q=3 already
shows a markedly steeper rise around β/β_c = 1 than q=2, with mixed
domains visible in the susceptibility profile across a wider β window.

This is consistent with the structural claim that Z_3 supports a finite
intermediate window. A 3D extension (planned for a future L) would be
needed to see the true first-order jump.

Numerical artefacts to be wary of (for any future extension):

- 24×24 is far too small to resolve a true phase transition; the
  apparent multi-peak structure in `<m>` near β/β_c ~ 0.9 is
  finite-size noise, not metastability evidence.
- Random-sweep Metropolis is autocorrelated near T_c. Wolff cluster
  updates would be required for any quantitative claim.

## 7. What would falsify this guess

1. A 3D q=3 Potts MC with realistic mapping of `T_eff(z)` should
   predict the cluster-dip amplitude *without re-fitting* the L33
   global `amp` parameter. If the predicted amplitude is wrong by >1
   order of magnitude, the guess is dead.
2. Cluster-scale weak-lensing maps should show `triple-vacuum domain
   walls` — measurable as anisotropic shear on a characteristic
   correlation length. Absence at the predicted scale falsifies it.
3. Domain-wall tension must satisfy `sigma_w * (cluster radius)^2 <
   cluster binding energy`. A back-of-envelope check (deferred) is
   the first quantitative gate.

## 8. Status

- **Direction**: Z_3 / 3-state Potts internal symmetry of n.
- **No equations were imported from L14, L22, L33, L46, L60s.**
- **No parameter values are quoted from prior L sessions.**
- This note is a free recording under the project's "방향만 제공" rule.
- Paper Z_2 framing is *not* invalidated; this guess is a
  **substructure** that becomes relevant only at cluster scales.

Artefacts:

- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L465/SPECULATION.md` (this file)
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/simulations/L465/run.py` (Potts toy MC)
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L465/potts_scan.csv` (toy output)
- `/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L465/potts_phase.png` (toy plot)
