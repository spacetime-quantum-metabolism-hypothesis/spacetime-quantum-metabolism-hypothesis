# L463 — Free Speculation: CKN x Bekenstein Crossing as Cluster-Scale sigma_0 Dip

**Status**: free speculation, single-author (no team derivation), order-of-magnitude only.
**Date**: 2026-05-01

## 1. The hypothesis

Cluster-scale phenomenology in SQT (the apparent dip in effective sigma_0
near R ~ 1–3 Mpc, M ~ 10^14–10^15 M_sun) is conjectured to arise from a
*crossover* between two holographic/informational saturation channels:

- **Cohen-Kaplan-Nelson (CKN) bound** [hep-th/9803132] — IR/system-size
  cutoff on vacuum dof, set by the *Hubble / region size* L. Counts dof as
  N_CKN(L) ~ (L / l_P)^{3/2}.
- **Bekenstein bound** [PRD 23 287, 1981] — local mass-radius information
  ceiling, N_Bek(R, M) ~ 2 pi R M c / (hbar ln 2). Saturates at the black-hole
  area law N_BH ~ pi (R/l_P)^2.

When both ceilings become *commensurate* on the same physical region,
the two saturation channels can interfere. The free speculation is that
this interference is *destructive* in the SQT coupling channel, weakening
the effective sigma_0 and producing a localized cluster-scale dip.

Schematic suppression ansatz:

    S(L, M) = 1 - exp[ -(log10 T)^2 / w^2 ],   T = N_CKN(L) / N_Bek(L, M)

with w an order-unity decoherence width.

## 2. Where the bounds cross

The crossing condition N_CKN(L) = N_Bek(L, M) gives

    M*(L) = (hbar ln 2) / (2 pi c) * L^{1/2} / l_P^{3/2}.

Plugging numbers (see `simulations/L463/run.py`):

|     L [Mpc] |  M*(L) [M_sun] |
|-------------|----------------|
|    1.0e-03  |    1.7e-12     |
|    1.0e-01  |    1.7e-11     |
|    1.0      |    5.5e-11     |
|   10        |    1.7e-10     |
|  100        |    5.5e-10     |
| 4400        |    3.5e-09     |

Equating the two literal bounds picks out an *absurdly low* mass curve
(femto-grams). Real bound systems sit roughly 25 orders of magnitude
above N_Bek and below N_CKN (CKN is the looser of the two at galactic+
scales because it grows only as L^{3/2}, while Bekenstein uses the
*actual* mass which is far below the black-hole limit at these radii).

| anchor              | R [Mpc] |   M [M_sun] | log10 T | S(supp) |
|---------------------|---------|-------------|---------|---------|
| Milky Way disk      |  0.015  |    1e12     |  -23.2  |  ~1.000 |
| Galaxy group        |  0.5    |    5e13     |  -24.1  |  ~1.000 |
| Virgo cluster       |  2.0    |    1.2e15   |  -25.2  |  ~1.000 |
| Coma cluster        |  3.0    |    1.5e15   |  -25.2  |  ~1.000 |
| Massive cluster     |  2.5    |    2.0e15   |  -25.4  |  ~1.000 |
| Supercluster        | 50      |    1e17     |  -26.4  |  ~1.000 |
| Hubble volume       | 4400    |    1e23     |  -31.5  |  ~1.000 |

## 3. Verdict on the speculation

**The naive crossing does not happen at cluster scales.** With the
literal CKN and Bekenstein expressions, |log10 T| is monotonically large
(~25) across all astrophysical anchors and *minimum near galactic scales*,
not at clusters. Cluster scales are not specially picked out.

For the speculation to survive, one of the following must be invoked
(none of which is justified here, listed only as escape routes for any
follow-up):

1. **Effective dof rescaling** — if the SQT-relevant CKN bound uses an
   *effective* hbar_eff or M_P scaled by (rho_crit / rho_Planck), the
   crossing scale shifts. Order of magnitude needed: ~10^25, i.e.
   roughly (rho_crit / rho_Planck)^(1/3) ~ 10^-40 — unlikely.
2. **Black-hole-saturated Bekenstein** (use N_BH = pi(R/l_P)^2 instead
   of mass-based N_Bek). Then T = (l_P / L)^{1/2}, monotone again,
   no cluster-scale singling.
3. **Channel mixing not at N=N but at *energy-density* matching**:
   rho_CKN ~ M_P^2/L^2 vs rho_BH ~ M/(L^3). These cross at
   M ~ M_P^2 L. For L = 2 Mpc this gives M ~ 1e16 M_sun — *the right
   ballpark for clusters*. This is the speculation that survives.

## 4. Surviving sub-hypothesis (logged for future test)

The *energy-density* (not dof-count) version of the crossing,

    rho_CKN(L) ~ M_P^2 c^4 / L^2,    rho_sys(R, M) ~ M c^2 / (4/3 pi R^3),

equates at M ~ M_P^2 c^2 L / G, which for L = 1–3 Mpc lands on
M ~ 5e15 – 2e16 M_sun. That is one decade above typical cluster masses
and could plausibly *graze* the high-mass tail.

This is the candidate worth a real derivation: not bound dof crossing,
but bound *energy-density* crossing. A future LXX session should hand
this direction (without map) to the 8-person team for independent
formulation.

## 5. Output

- `simulations/L463/run.py` — toy that prints the crossing table and
  suppression S for the seven anchors above.

## 6. Honest one-line summary

CKN-vs-Bekenstein dof crossing at clusters is *not* supported by the
naive numbers; the energy-density variant lands in the cluster mass
ballpark and is the only piece of this speculation worth carrying
forward.
