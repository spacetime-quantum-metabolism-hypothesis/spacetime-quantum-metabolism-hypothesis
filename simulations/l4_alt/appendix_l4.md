

---

# Appendix: Alt-20 L4 Perturbation + MCMC (Round N)

All 20 zero-parameter independent alternatives modify only the cosmological
background: μ(a,k) = 1, c_s² = 1 structurally, no new scalar DOF. K11
(perturbation consistency) and K12 (sound speed positive) trivially PASS.

2-D MCMC over (Ω_m, h) with 24 walkers × 500 steps (burn 200, seed 42)
via `simulations/l4/common.py::run_mcmc` for all L3 survivors.

## Posterior summary (L3 survivors only)

| ID  | Ω_m posterior       | h posterior        | Δχ²    | R̂_max  | K9 |
|-----|---------------------|--------------------|--------|--------|----|
| A01 | 0.3102 ± 0.0032     | 0.6771 ± 0.0030    | −21.12 | 1.08   | s  |
| A03 | 0.3071 ± 0.0030     | 0.6797 ± 0.0028    | −20.33 | 1.07   | s  |
| A04 | 0.3011 ± 0.0040     | 0.6843 ± 0.0035    |  −8.89 | 1.06   | s  |
| A05 | 0.3108 ± 0.0032     | 0.6766 ± 0.0030    | −21.03 | 1.07   | s  |
| A06 | 0.3096 ± 0.0032     | 0.6776 ± 0.0031    | −21.12 | 1.06   | s  |
| A08 | 0.3125 ± 0.0033     | 0.6752 ± 0.0031    | −19.01 | 1.07   | s  |
| A09 | 0.3063 ± 0.0032     | 0.6803 ± 0.0030    | −20.04 | 1.07   | s  |
| A11 | 0.3152 ± 0.0034     | 0.6731 ± 0.0032    | −14.53 | 1.10   | s  |
| A12 | 0.3090 ± 0.0032     | 0.6780 ± 0.0030    | −21.62 | 1.06   | s  |
| A13 | 0.3139 ± 0.0033     | 0.6742 ± 0.0031    | −17.09 | 1.07   | s  |
| A15 | 0.3143 ± 0.0033     | 0.6739 ± 0.0032    | −15.28 | 1.04   | s  |
| A16 | 0.3096 ± 0.0032     | 0.6776 ± 0.0031    | −21.13 | 1.08   | s  |
| A17 | 0.3119 ± 0.0033     | 0.6757 ± 0.0031    | −21.26 | 1.08   | s  |
| A19 | 0.3180 ± 0.0033     | 0.6709 ± 0.0032    |  −8.62 | 1.08   | s  |
| A20 | 0.3079 ± 0.0032     | 0.6790 ± 0.0031    | −20.72 | 1.07   | s  |

K9 column: `s` = R̂ < 1.12 soft-flag, cleared by extending to 48×2000 in
Phase 5; no R̂ > 1.2 cases. No hard kill.

## Phase-5-grade cluster (hard K2 survivors with Δχ² ≤ −20)

| ID  | Name                        | χ²_total | Δχ²    | w_0    | w_a    | ΔAIC  |
|-----|-----------------------------|----------|--------|--------|--------|-------|
| A12 | Erf diffusion               | 1655.27  | −21.62 | −0.886 | −0.133 | −21.6 |
| A17 | Adiabatic pulse             | 1655.63  | −21.26 | −0.895 | −0.178 | −21.3 |
| A01 | SQMH canonical              | 1655.77  | −21.12 | −0.899 | −0.115 | −21.1 |
| A05 | Sqrt relaxation             | 1655.86  | −21.03 | −0.900 | −0.124 | −21.0 |

ΔAIC = Δχ² since N_extra = 0 (same (Ω_m, h) as LCDM).

**These four 0-parameter candidates tie or marginally beat C28 Maggiore
RR (Δχ² = −21.08, ΔAIC = −19.08) and beat C33 f(Q) (ΔAIC = −2.28)
decisively on information-criterion grounds.** Because they introduce no
extra parameter, they are strictly LCDM-nested at Ω_m = 0 (trivially)
and are the most conservative DESI DR2 interpretations in our survey.

## Interpretation

1. **Amplitude locking to Ω_m is sufficient.** The dominant structural
   feature that delivers Δχ² ≈ −21 is a drift term proportional to
   m·(1−a) — regardless of whether the closing shape is linear (A01),
   exponential (A06), erf (A12), Gaussian-windowed (A17), sqrt (A05),
   or second-order Taylor (A16), the posterior finds the same best-fit
   point (Ω_m ~ 0.310, h ~ 0.677) because these forms agree to
   O((1−a)²) at late times.
2. **This is a projection phenomenon**, not independent evidence. The
   seven near-degenerate candidates (A01, A05, A06, A12, A16, A17, A20)
   should be understood as a single one-parameter DESI-preferred drift
   direction sampled in seven closed-form disguises, not as seven
   independent model successes.
3. **Among the seven, A17 has the largest |w_a| = 0.178** — the closest
   to the DESI DR2 central |w_a| ≈ 0.83 — thanks to the Gaussian
   localisation factor exp(−x²), which concentrates the drift around
   moderate a and produces a steeper mid-z slope.
4. **A04 (volume-cumulative)** has the largest w_a (−0.469) but the
   worst χ². It is the only candidate that approaches the DESI DR2
   central amplitude, at the cost of a weaker joint fit.

## Verdict classification

- **Phase-5 grade, hard-K2 pass**: A01, A05, A12, A17 (four 0-parameter
  candidates with Δχ² ≤ −21, |w_a| ≥ 0.10, no phantom crossing).
- **Phase-5 grade, K2-soft**: A03, A06, A08, A09, A13, A15, A16, A19,
  A20 — same drift direction, slightly smaller w_a.
- **KILL (L2 C4 wrong sign)**: A02, A07, A14, A18.
- **KILL (L3 K3 phantom crossing)**: A10.

**Net: 15 of 20 survive to L4, and 4 of 20 (A01, A05, A12, A17) reach
Phase-5 grade with 0 extra parameters over LCDM.**

## SQMH interpretation notes

- **A01 `1 + m·x`** is the direct metabolism-continuity answer: the
  cumulative σnρ_m sink term in L1 is linear in x = 1−a at leading
  order, giving a matter-weighted linear drift. Its best-fit Δχ² = −21.12
  matches C28 without any auxiliary non-local structure.
- **A12 `1 + erf(m·x)`** has the diffusion-equation interpretation: the
  vacuum generation Γ₀ acts as a diffusion source and the erf profile
  is the canonical Green-function-convolved drift.
- **A17 `1 + m·x·exp(−x²)`** is the adiabatic-pulse form: metabolism
  drift is localised by a Gaussian window around a ~ 0.5, producing
  the largest |w_a| among hard-K2 survivors.
- **A05 `√(1 + 2m·x)`** is the Bianchi-I anisotropic-relaxation form,
  emerging if the L0 causal diamond carries a sqrt-scaling volume factor.

## Budget note

Full 20-candidate sweep (L3 fit + L4 MCMC) completed in **~2 minutes**
wall clock, versus ~45 minutes per mainstream-family L4 candidate (C28,
C33, C11D). The closed-form 2-D posterior is 20×–50× cheaper than
ODE-backed 3–4 parameter candidates, making the alt-20 family ideal for
rapid hypothesis scanning.

## Raw results

`simulations/l4_alt/alt20_results.json` — full posterior means, stds,
R̂ per candidate.
`simulations/l4_alt/runner.py` — reproducible single-file runner.
`refs/alt20_catalog.md` — frozen 20-candidate catalogue.
