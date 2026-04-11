# L4 C10k Dark-only Coupled Quintessence — 4-Reviewer Panel

## Writer (R1) summary
- Background: w_eff = -1 + (2/3) beta_d^2 (constant), rho_DE(a) = OL0 a^(-2 beta_d^2).
- beta_d in [0, 0.2].
- Best fit: Om=0.3168, h=0.6719, beta_d=0.200 (at UPPER bound).
- chi2=1667.54, dchi2=-9.36 vs LCDM.
- CPL: w0=-0.9733, wa=0 (structural, **K2 FAIL**).
- Growth channel re-assessment: best beta_d=0 in the RSD-only fit, dchi2_rsd=0;
  sigma_8 proxy shift at beta_d=0.107 is +0.96% (S_8 worsens).
- **Verdict: CONFIRMED KILL**.

## Critic R2 (physics)
- Dark-only embedding: baryons Einstein-frame -> Cassini gamma-1=0 exact.
  Q5 PASS — one of the few L4 candidates that cleanly passes Cassini.
- BUT background is structurally wa=0 (leading order in beta_d^2). No wa
  content at any beta_d.
- Growth channel: G_eff/G = 1+2 beta_d^2 should *increase* sigma_8 -> S_8
  tension becomes WORSE, not better (CLAUDE.md rule: +6.6 chi2 at bd~0.107).
  Our shift estimate +0.96% at bd=0.107 is consistent.
- RSD chi2 does not improve: best fit at bd=0 means the data prefers no
  coupling in the growth channel.

## Critic R3 (numerics)
- Fit pushed beta_d to the upper bound (0.200). Background chi2 decreases
  because higher bd changes Om, h marginally, but it's NOT capturing real
  physics — it's data re-parameterising around LCDM. Evidence: wa=0
  structurally means the w(z) shape is flat; dchi2=-9.36 comes entirely from
  moving (Om, h) off LCDM best-fit.
- Growth ODE (common.growth_fs8) checked positive D(a) throughout.
- MCMC rhat 1.16-1.19 at 16x200. K9 fails but irrelevant given K2 fail.

## Critic R4 (data / statistics)
- Q1 fails via K2, Q2 formally passes via dchi2<=-6 branch but that is
  misleading because the improvement is not from the DE sector.
- LCDM RSD chi2 baseline = 7.304 (matches L3). beta_d sweep monotonically
  WORSENS RSD or keeps it flat. This is a HARD FALSIFICATION of the growth
  channel pathway advertised in L3 as the C10k rescue route.
- dchi2 decomposition at best fit: the -9.36 total is actually driven by the
  change in (Om, h) pair; at fixed LCDM (Om=0.3204, h=0.6691) the beta_d
  contribution is zero to 4th order.

## Panel decision
**CONFIRMED KILL**.
- Background K2 fail is structural (wa=0).
- Growth-channel rescue route falsified: RSD chi2 does not improve, sigma_8
  proxy shifts the wrong way.
- Cassini pass (Q5) is insufficient compensation for K2 + growth channel
  failures.
- C10k does NOT enter Phase 5 KEEP list.

Recommendation: record C10k as "cleanly killed" reference and use as a
control for the dark-only sector when benchmarking disformal / diffusion
candidates.
