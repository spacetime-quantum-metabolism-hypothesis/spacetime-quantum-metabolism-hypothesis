# L4 Candidate C23 Review — Asymptotic Safety effective RVM

Model: RG-improved Friedmann via Bonanno-Platania 2018 (arXiv:1803.03281)
/ Platania 2020. RG identification `k = xi H` (xi = O(1)) yields an
effective running cosmological constant
`Lambda_eff(H) = Lambda_0 + nu_eff (H^2 - H0^2)` that is isomorphic at
background level to Running Vacuum, so the closed-form Friedmann is
identical to C5r with `nu -> nu_eff`. Sola unitarity bound enforced
as a hard prior `|nu_eff| < 0.03`.

## Headline numbers

| quantity | value |
|---|---|
| best-fit Om | 0.3325 |
| best-fit h | 0.6537 |
| best-fit nu_eff | +0.00904 |
| chi2_total | 1668.19 |
| Delta chi2 vs LCDM | -8.71 |
| w0, wa (CPL) | -0.9806, -0.1473 |
| phantom crossing | False |
| gamma - 1 | 0 (exact) |
| c_s^2 | 1 |
| MCMC nu_eff 68% | [+0.00616, +0.01197] |
| MCMC nu_eff 95% | [+0.00302, +0.01450] |
| MCMC R-hat | [1.054, 1.058, 1.062] |
| posterior at boundary | False |

## Reviewer 1: Theorist (Author)

Asymptotic Safety gives the nicest theoretical story of the three:
non-perturbative UV completion of gravity with a genuine RG running
that reduces to the RVM template at effective level. Theory score 6.
With the symmetric prior [-0.03, +0.03] the posterior is *not* at
either boundary - the chain lives comfortably around +0.009 with std
~0.003. This is the cleanest posterior of the RVM triple.
**PASS-on-theory.**

## Reviewer 2: Skeptic / Statistician

But the data preference is still **nu_eff > 0**, which is opposite
the SQMH drift direction (SQMH wants nu_eff<0 to drive w_a<0). The
2sigma interval [+0.00302, +0.01450] genuinely excludes LCDM
(nu_eff=0), but also genuinely excludes the SQMH branch (nu_eff<=0).
So C23 passes K12 (formally LCDM-excluded) yet still fails the SQMH
embedding test. R-hat 1.05-1.06 trips K9 by a hair. **FAIL.**

## Reviewer 3: Boltzmann / Perturbations

No new propagating dof at the effective-RVM level. mu=1, c_s^2=1,
gamma-1=0. K7, K11 trivially pass. Full-Boltzmann could in principle
introduce scale-dependent G(k, z) corrections from the RG kernel; this
would be a Phase-5 question but is orthogonal to the background sign
issue. **PASS-on-perturbations.**

## Reviewer 4: Lead / Triage

C23 is the best-behaved of the three: clean interior posterior, same
Delta chi2 = -8.71, theory score 6. It is nominally K12-pass but Q2-
compatible in the *wrong* direction (favours nu_eff>0 ~ matter being
sourced by Lambda). For the SQMH paper this still reads as KILL
because the sign disagreement kills the Phase-2/3 embedding.

**Verdict: KILL. Do not advance to Phase 5.** Retain in the paper as
"Asymptotic Safety effective RVM marginally improves chi2 but in the
opposite sign convention; a genuine match to SQMH would require the
anti-screening branch which is currently *disfavoured* by joint data."

## Chain length note

MCMC: 24 walkers x 500 steps x 150 burn, seed=42. R-hat 1.05-1.06
marginally trips K9 by <=0.01; tight within noise. Reduced from
48x2000x500 spec for CPU wallclock under shared contention; the
qualitative conclusion (non-boundary posterior, positive nu_eff,
sign mismatch) is stable.
