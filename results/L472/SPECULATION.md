# L472 — Tsallis Non-Extensive Entropy as Origin of the Cluster-Scale σ_0 Dip

**Status**: Free speculation. No theoretical map provided to derivation team — direction-only.
**Date**: 2026-05-01
**Tier**: SPECULATION (not theory; not yet falsifiable design).

---

## 0. Setup — observational anchor

Earlier SQMH cluster-scale analyses (L4xx series) reported a phenomenological dip in the
effective absorption / source amplitude σ_0 around cluster scales (R ~ 0.3–3 Mpc, equivalently
M ~ 10^13.5–10^15 M_sun). The dip is structural: it sits below the smooth interpolation
between galactic-halo (~kpc) and large-scale (>10 Mpc) regimes.

Working observational signature (schematic):
- σ_0(R) approximately constant on galactic scales,
- a localised suppression centred at R_dip ≈ 1 Mpc with depth Δσ/σ ≈ 10–20%,
- recovery to large-scale value beyond R ≈ 10 Mpc.

The conventional SQMH absorption picture assumes Boltzmann-Gibbs (BG) statistics of metabolic
microstates. The dip is **not** explained by any extensive-entropy mechanism we have identified
in L1–L471. This document records a free speculation that the dip is a thermodynamic — not
gravitational — signature.

---

## 1. Hypothesis

**Cluster-scale σ_0 dip = signature of Tsallis q-entropy reaching its minimum at cluster scales.**

In Tsallis non-extensive thermostatistics, the entropy of a long-range-correlated system is

  S_q[p] = k_B (1 − Σ p_i^q) / (q − 1),

with q = 1 recovering Boltzmann-Gibbs. The "non-extensivity index" q − 1 measures the
strength of long-range correlations / non-locality of the underlying microstate distribution.
Empirically, gravitating self-similar systems (galaxy clusters, dark-matter haloes, stellar
polytropes, peculiar-velocity distributions) are repeatedly fit by q ≠ 1 with q in the range
~1.1–1.5 (Tsallis-Plastino, Lima, Ourabah, etc.).

Conjecture: as the spatial scale R is varied, the effective q(R) of the SQMH metabolic field
is **not** monotonic. It has a minimum near cluster scale because:

- on galactic scales, virialised baryon+halo systems have q > 1 (mild long-range tail),
- on cluster scales, the dynamical-time-scale crossover (t_dyn ≈ Hubble) drives the
  correlation length to *saturate* relative to the system size, which in q-statistics
  corresponds to **q approaching 1 from above** — the BG limit,
- on supercluster / cosmic-web scales, the filamentary topology re-introduces strong
  long-range correlation and q rises again.

If σ_0 is monotonically increasing in (q − 1) — which it is, in any model where σ_0
counts the *available phase-space volume per metabolic absorption event*, since the
q-deformed density of states grows with non-extensivity — then σ_0(R) inherits the
non-monotonic q(R) profile. The dip is the Boltzmann-Gibbs window.

---

## 2. Mechanism sketch (direction-only, no formula imposed)

The derivation team should explore, independently:

1. **q-deformed metabolic partition**. Replace BG state-counting in the SQMH absorption
   functional with a Tsallis q-exponential ensemble. Identify how σ_0 depends on q.
2. **Scale-running of q**. The SQMH field has an intrinsic correlation length ξ_SQMH set by
   the dissipation/absorption rate. The effective q at observation scale R is a functional
   of R/ξ_SQMH. Investigate whether the natural map has a stationary point.
3. **Long-range correlation weakening at cluster scale**. The same mechanism that flattens
   cluster turn-around overdensity (~178 in BG, but observed scatter is q-distributed) may
   weaken the SQMH source coupling at cluster scale by reducing effective phase-space
   accessibility. This is the σ_0-suppression channel.
4. **Tsallis vs Boltzmann distinguishability**. BG predicts σ_0(R) smooth and monotone.
   Tsallis predicts a localised dip. Depth and width of the dip are diagnostic of q_min
   and the running scale.

Deliberately not provided: q(R) functional form, ξ_SQMH numerical value, σ_0(q)
relationship, fitting parameters. Team must derive.

---

## 3. Status & predictions to test

- **Q-test 1 (existence)**: Can the Tsallis-running ansatz reproduce the observed dip
  with a single non-extensivity parameter q_max (off-cluster) and a single scale ξ?
- **Q-test 2 (BG limit)**: Does the model collapse to standard SQMH on galactic scales
  (q → 1+ε with ε → 0) without ad-hoc switches?
- **Q-test 3 (Tsallis vs BG)**: AICc penalty for the +1 Tsallis parameter must be
  defeated by Δχ² ≥ 2 vs the BG baseline on cluster σ_0 data.
- **Q-test 4 (cosmological imprint)**: A non-trivial q(R) at cluster scale should
  leave a small but coherent imprint on the cluster mass function high-mass tail
  (Tsallis q > 1 enhances the tail). Independent check.

Failure modes acknowledged in advance:
- If q_min(cluster) ≈ q(galactic), the dip is not explained by q-running and the
  hypothesis is dead. This is the primary kill criterion.
- If the fit prefers q < 1 (sub-extensive), the SQMH long-range-correlation reading
  is reversed and the speculation must be rewritten.

---

## 4. Connection to SQMH core (loose)

The spacetime metabolism axiom L0 already gives the absorption rate as a *non-local*
sink. Non-locality + finite correlation length is exactly the regime where Tsallis
statistics is the natural generalisation of BG (Beck-Cohen superstatistics, Tsallis
2009). The cluster-scale dip would be the first observational handle on the
**thermostatistical** sector of SQMH, distinct from the geometric (BAO) and kinematic
(growth) sectors explored in L1–L471.

This is speculation. No commitment.

---

## 5. Numerical companion

`simulations/L472/run.py` fits a phenomenological Tsallis-running curve

  σ_0(R) = σ_∞ · [ 1 − A · exp( − ((log10(R/R_dip))/w)^2 ) ]

to a synthetic dip profile (placeholder until cluster σ_0 data are extracted in L473).
The fit returns (σ_∞, A, R_dip, w) and an effective q-amplitude estimate
q_eff − 1 ≈ A. BG-only baseline (A = 0) is fit alongside for AICc comparison.

The script is a curve-fit harness, not a physical derivation. Physical derivation
is reserved for the 8-person team in L473+.
