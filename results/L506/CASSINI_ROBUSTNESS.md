# L506 - Cassini PPN |gamma-1| Cross-Form Robustness Audit

**Goal**: test whether the paper's PASS_STRONG result
(|gamma-1| ~ 1.1e-40 << 2.3e-5) is a *global* SQMH prediction
or a derivation-channel-specific number.

Same logic as L491 (RAR a_0 cross-form), applied to PPN gamma.

**Cassini bound**: |gamma-1| < 2.30e-05 (Bertotti+ 2003)
**Paper headline**: |gamma-1| ~ 1.1e-40 via beta_eff = Lambda_UV/M_Pl ~ 7.4e-21

## Channels and predictions

| # | Channel | beta | |gamma-1| | log10 | Pass? | Margin |
|--:|---------|-----:|---------:|------:|:-----:|------:|
| 1 | beta_eff_paper | 1.47e-21 | 4.35e-42 | -41.4 | YES | 5.3e+36 |
| 2 | universal_at_beta_eff | 1.47e-21 | 4.35e-42 | -41.4 | YES | 5.3e+36 |
| 3 | universal_phase3 | 1.07e-01 | 2.26e-02 | -1.6 | NO | 1.0e-03 |
| 4 | dark_only_structural | 0.00e+00 | 0 (structural) | -inf | YES | inf |
| 5 | brans_dicke | 1.47e-21 | 4.35e-42 | -41.4 | YES | 5.3e+36 |
| 6 | pure_disformal | n/a | 0 (structural) | -inf | YES | inf |
| 7 | vainshtein_screened | 1.07e-01 | 5.20e-12 | -11.3 | YES | 4.4e+06 |
| 8 | chameleon_screened | n/a | 1.00e-07 | -7.0 | YES | 2.3e+02 |

## Channel notes

**(1) beta_eff_paper**  -- 2 beta^2/(1+beta^2), beta=Lambda_UV/M_Pl, Lambda_UV=18MeV

  - Paper headline. Lambda_UV stipulated, not derived from axioms.

**(2) universal_at_beta_eff**  -- Universal coupling (no dark-only) at the same beta_eff

  - Same arithmetic as (1). Channel name distinguishes the *embedding*: if baryons couple, beta=7.4e-21 still passes -- but only because Lambda_UV was tuned to MeV scale.

**(3) universal_phase3**  -- Universal coupling at Phase-3 cosmology posterior beta=0.107

  - HARD FAIL: |gamma-1|~2.3e-2 vs limit 2.3e-5 (1000x violation). Forces the dark-only embedding choice.

**(4) dark_only_structural**  -- Sector-selective coupling: matter sector decoupled, beta_b=0

  - STRUCTURAL gamma=1 exact. Identical to PASS_TRIVIAL: any theory with beta_b=0 trivially passes. Dark-only embedding is an axiom-level *choice* (Foundation 5), not a derivation.

**(5) brans_dicke**  -- |g-1| = 1/(1+omega_BD), omega_BD = 1/(2 beta^2)

  - Reduces to (1) algebraically -- not an independent prediction.

**(6) pure_disformal**  -- Pure disformal coupling: g~ = g + B d_phi d_phi, A'=0

  - STRUCTURAL gamma=1 exact (Zumalacarregui-Koivisto-Bellini 2013). Schwarzschild solves the modified equations with auxiliary field frozen. Independent of beta. PASS_TRIVIAL.

**(7) vainshtein_screened**  -- Cubic Galileon Vainshtein: |g-1| ~ 2 beta^2 (r/r_V)^{3/2}

  - Phase-3 posterior beta survives Cassini *if* Vainshtein screening active. Adds a screening axiom (cubic Galileon), not currently in SQMH foundations.

**(8) chameleon_screened**  -- Chameleon thin-shell screening, KW 2004 ceiling

  - Literature ceiling from thin-shell argument. Adds a chameleon potential axiom not in SQMH foundations.

## Cross-form distribution (finite, positive |g-1|)

- N channels (finite)         : 6 of 8
- N structural-zero           : 2
- log10|g-1| min              : -41.36
- log10|g-1| max              : -1.65
- spread                      : 39.72 dex
- median                      : -11.28
- log10|g-1| paper headline   : -41.36
- channels within 1 dex of paper: 3 / 6

## Hypothesis-sensitivity decomposition

| Channel | Depends on |
|---|---|
| (1)/(2)/(5) beta_eff family | Lambda_UV ~ 18 MeV stipulation |
| (3) universal at Phase-3 beta | beta=0.107 from BAO+SN+CMB+RSD posterior |
| (4) dark-only | sector-selective embedding axiom (Foundation 5) |
| (6) pure disformal | A'=0 disformal-only Lagrangian choice |
| (7) Vainshtein | cubic Galileon screening axiom (extra) |
| (8) chameleon | KW 2004 thin-shell potential axiom (extra) |

## K-criteria

- K_C1 all channels PASS Cassini   : FAIL (7/8)
- K_C2 every channel within 1 dex of 10^-40 : FAIL (3/6)
- K_C3 cross-form spread <= 5 dex  : FAIL (39.72 dex)
- K_C4 no hard fails (channel-indep): FAIL (1 hard fails)

## Verdict: **CHANNEL_DEPENDENT**

Some natural channels (e.g. universal coupling at Phase-3
posterior beta) HARD-FAIL Cassini.  PASS_STRONG is global
*only because SQMH selects* the dark-only / screened
channel.  This is the failure mode the dark-only
embedding axiom was introduced to repair (L4 universal
fluid-IDE Cassini violation).

## One-line honesty

> PASS_STRONG channel-dependent -- universal coupling at Phase-3 beta HARD FAILS; PASS rests on dark-only / screening axiom selection.
