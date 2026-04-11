# L4 C41 Wetterich/Amendola Fluid IDE — 4-Reviewer Panel

## Writer (R1) summary
- Background: analytic closed form rho_m(a) = A a^-3beta + B a^-3,
  rho_DE(a) = OL0 * a^-3beta. beta in [0, 0.1].
- Best fit: Om=0.3488, h=0.64 (lower bound), beta=0.0522.
- chi2=1662.656, dchi2=-14.24 vs LCDM.
- CPL: w0=-0.896, wa=-0.907 (|wa| far above K2 threshold).
- MCMC: 16 walkers x 200 steps x burn 50, emcee backend.
- K1 PASS, K2 PASS, K3 PASS, K9 FAIL (rhat max 1.13 > 1.05).
- Q1 FAIL (K9), Q5 FAIL (universal fluid coupling -> |gamma-1|=2 beta^2 > 2.3e-5).
- **Verdict: KILL** (Q1+Q5 both fail).

## Critic R2 (physics)
- SQMH sign beta>=0: OK (DESI matter->DE direction).
- Toy validity: best fit beta=0.052 stays in the linear regime (<=0.1), consistent
  with CLAUDE.md rule "Phase 3 beta=0.107 not directly inheritable".
- Universal coupling (baryons + CDM) is the physical problem. Without a
  dark-only embedding (a la C10k), Cassini |gamma-1|<2.3e-5 cannot be satisfied.
- wa=-0.907 is a structural prediction of the coupled-fluid continuity toy,
  not an ad hoc flip.
- **Flag**: Q5 fails under universal coupling. C41 becomes viable only if
  re-embedded as dark-only (which is effectively C10k with scalar background).

## Critic R3 (numerics)
- tight_fit pushed h to 0.64 (hard lower bound). Worth widening h bounds in
  Phase 5, but regression check against LCDM baseline still meaningful.
- Background is exact analytic, no ODE stability concerns.
- MCMC rhat 1.08-1.13 on all three parameters -> under-burnt; want >=2000 effective
  samples per walker. K9 flagged. Phase 5 should use 48x2000.
- Reproducibility: np.random.seed(42) set in run_mcmc; rerun produces same
  means within <1e-3. Satisfies K5.
- numpy 2.x trapz, thread settings, warning suppression all in place.

## Critic R4 (data / statistics)
- LCDM reference chi2=1676.895 matches l3/lcdm_baseline.json. No drift.
- dchi2=-14.24 with 1 extra parameter (beta) -> naive Delta-AIC = -12.24 vs LCDM.
  Significant background improvement, but misleading because walkers cluster
  near (Om=0.35, h=0.64) boundary.
- Q2 passes via dchi2<=-6 branch.
- K12: posterior does not include LCDM in 2-sigma (wa_mean far from 0), but
  rhat>1.05 makes the posterior width unreliable.

## Panel decision
**KILL** (Q1 fails via K9, Q5 fails via universal coupling). Even with a longer
MCMC that cures K9, the model still fails Q5 unless re-cast as dark-only.
C41's empirical power is subsumed by C10k + scalar background work.

Tie-break recommendation: do NOT promote to Phase 5. Consider a separate
"dark-only C41" candidate in a follow-up round if a Phase 5 slot opens.
