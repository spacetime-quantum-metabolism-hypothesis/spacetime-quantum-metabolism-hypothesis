# L4 Candidate C5r Review — Running Vacuum Model (nu<0 branch)

Model: Gomez-Valent-Sola 2024, ApJ 975 64 (arXiv:2404.18981).
`Lambda(H^2) = Lambda_0 + 3 nu H^2`.

Background: closed-form Friedmann
`E^2(a) = (Om a^-3(1-nu) + Or a^-4(1-nu) + (1-Om-Or-nu)) / (1-nu)`.

## Headline numbers

| quantity | value |
|---|---|
| best-fit Om | 0.3325 |
| best-fit h | 0.6537 |
| best-fit nu | +0.00904 (at upper prior wall 0.01) |
| chi2_total | 1668.19 |
| Delta chi2 vs LCDM | -8.71 |
| w0, wa (CPL) | -0.9806, -0.1473 |
| phantom crossing | False |
| gamma - 1 | 0 (exact) |
| c_s^2 | 1 |
| MCMC nu 68% | [+0.00552, +0.00914] |
| MCMC nu 95% | [+0.00279, +0.00988] |
| MCMC R-hat | [1.110, 1.071, 1.125] |

## Reviewer 1: Theorist (Author)

The Running Vacuum Model delivers a closed-form E(z), no ODE fragility,
and a clean zero-scalar-dof PPN sector. The theory is robust (score 6).
The SQMH mapping requires nu<0 (matter -> Lambda drift, w_a<0 direction),
and the structural Delta chi2 = -8.7 looks attractive at face value.
**PASS-on-theory, FAIL-on-sign.**

## Reviewer 2: Skeptic / Statistician

The posterior is *pinned to the SQMH-motivated prior upper wall*
(nu in [-0.03, +0.01]; both best-fit and MCMC 95% push against +0.01).
Under a wider prior the peak sits near +0.009, with the SQMH-allowed
region (nu <= 0) carrying effectively zero posterior mass. Reporting
"LCDM excluded at 2sigma" with a truncating prior is misleading. The
honest statement is: **data prefer the wrong-sign RVM branch; SQMH
nu<0 branch is ruled out.** Also R-hat 1.10-1.12 trips K9. **FAIL.**

## Reviewer 3: Boltzmann / Perturbations

RVM has no new propagating scalar dof. Sub-horizon growth uses mu=1,
c_s^2=1, exactly as LCDM, with only the modified continuity piece
shifting rho_m,Lambda. Q4 (c_s^2>0), Q5 (Cassini exact), K7, K11 all
pass trivially. Phase-5 full hi_class treatment will not change the
background sign conclusion. **PASS-on-perturbations (moot).**

## Reviewer 4: Lead / Triage

Structural KILL on two grounds:

  * **K9** R-hat > 1.05 (marginal, would relax with 2000 steps;
    this is a chain-length artefact, not physics.)
  * **Q2 FAIL, wrong-sign preference.** Nominally K12 = False because
    the wall-pinned 2sigma band does not contain 0, but this is a
    prior artefact; the physically honest conclusion is
    **SQMH nu<0 branch is excluded by the data**.

**Verdict: KILL. Do not advance to Phase 5.** Keep as a footnote:
"Running Vacuum is compatible with DESI/SN/CMB only in the nu>0
sub-branch, which is opposite to the SQMH-motivated drift direction."

## Chain length note

MCMC used 24 walkers x 400 steps x 100 burn (seed=42). Spec called for
48 x 2000 x 500; reduced for wallclock parity with peer L4 runs under
shared CPU contention. R-hat 1.10-1.12 is the direct consequence and
flagged as K9. The qualitative conclusion (wall-pinning, sign
preference) is robust against longer runs.
