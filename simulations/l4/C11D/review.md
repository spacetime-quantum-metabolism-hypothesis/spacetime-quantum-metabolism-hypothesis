# L4 C11D Disformal IDE — 4-Reviewer Panel

## Writer (R1) summary
- Background: thawing disformal CPL template
  w0_eff = -1 + gamma_D^2/3,  wa_eff = -(2/3) gamma_D^2.
- gamma_D in [0, 3.0].
- Best fit: Om=0.3102, h=0.6768, gamma_D=0.658.
- chi2=1653.974, dchi2=-22.92 vs LCDM.
- CPL: w0=-0.856, wa=-0.289 (|wa|=0.289, **K2 PASS**).
- MCMC: 16 walkers x 200 steps x burn 50, emcee.
- **K3 FAIL** (phantom crossing detected: w(z<<0)=-1.145 < -1).
- K9 FAIL (rhat max 1.17 > 1.05).
- Q1 FAIL (K3, K9).
- **Verdict: KILL** (K3 phantom crossing is a hard SQMH violation).

## Critic R2 (physics)
- K2 rejudge: at L3 the background toy (rho_DE proportional exp(gd(1-a))) gave
  |wa|=0.1149, just below 0.125. L4 replaced the toy with the leading-order
  thawing disformal expansion -> |wa| naturally scales as gd^2 and can reach
  >0.5 for gd~1. K2 is generously passable now.
- BUT: the same template produces w0=-1+gd^2/3 > -1 at a=1 and w(a<<1) =
  w0+wa = -1 - gd^2/3 < -1 -> phantom crossing at z>0. This is the well
  known artifact of the CPL leading-order expansion of a thawing field.
- Full hi_class disformal scalar does NOT phantom-cross (Z-K-B 2013 shows
  w >= -1 always for pure disformal A'=0). The L4 phantom is a **template
  artifact**, not a real physical prediction. K3 kill is therefore a kill of
  the template, not of the model.
- Static PPN gamma-1=0 exact (Z-K-B 2013 Sec IV, A'=0 pure disformal).
- **Flag**: K10 (sign consistency L3 vs L4) PASSES (both wa<0) but the
  phantom crossing in L4 is a new artifact. Must note the template limitation.

## Critic R3 (numerics)
- K2 rejudge scan: max |wa|=6.0 at gamma_D=3, but best_scan_chi2=1665.47 at
  large gamma_D that does not improve over LCDM; sweet spot gamma_D~0.6-0.8.
- tight_fit converged to interior point (all params away from bounds).
- MCMC rhat 1.10-1.17: under-burnt. Phase 5 48x2000 recommended.
- phantom_crossing() detector uses numerical d ln rho_de / d ln a and is
  robust for CPL template (no rho_de<0 artifact).

## Critic R4 (data / statistics)
- dchi2=-22.92 with 1 extra parameter: significant. Beats LCDM decisively on
  BAO (9.48 vs 23.57) and SN (1636.6 vs 1643.7), CMB unchanged.
- Q2 passes via dchi2<=-6.
- Posterior does not contain LCDM in 2-sigma (K12 pass).

## Panel decision
**KILL on template basis, RECOVERABLE in Phase 5 full disformal Boltzmann**.
- K3 phantom crossing is a CPL-expansion artifact; real disformal quintessence
  (A'=0) has w >= -1 everywhere.
- K9 is a compute-budget issue (fixable with longer MCMC).
- Recommendation: do NOT promote to Phase 5 KEEP list based on L4 alone.
  Instead, open a FOLLOW-UP Phase 5 run with hi_class disformal branch or
  Sakstein-Jain 2017 exact background to re-judge K3 without CPL artifact.
- Empirical performance (dchi2=-22.9) is the strongest of the three L4
  IDE candidates -> high priority for hi_class re-run.
