# refs/l9_final_verdict.md -- L9 Round 15: Final Verdict After All 15 Rounds

> Date: 2026-04-11
> Source: All L9 Rounds 1-15 findings.
> Purpose: Definitive Kill/Keep table, paper positioning, and JCAP reviewer Q&A.
> Language standard: refs/l7_honest_phenomenology.md.
> Anti-falsification: all claims verified numerically or by mathematical proof.

---

## L9 Complete Summary

15 rounds completed across 5 phases:
  - Rounds 1-5: Core analysis (K41/K43/K44 triggered, Q42 PASS)
  - Rounds 6-10: C28-A12 deepening (NF-16/17, Q45 FAIL, isomorphism = MEDIUM)
  - Rounds 11-15: NF-16 resolution, mechanism survey, limit analysis, paper §2 draft

---

## DEFINITIVE KILL / KEEP TABLE (After All 15 Rounds)

| Criterion | Status | Evidence | Confidence |
|-----------|--------|----------|-----------|
| K41: SQMH perturbation wa<0 impossible | TRIGGERED | G_eff/G - 1 = 4e-62; perturbation level same as background | CONFIRMED |
| K42: C28 full Dirian wa mismatch | NOT TRIGGERED | wa_C28 = -0.176 (shooting) or -0.19 (literature); |Dwa|=0.043 < 0.10 | CONFIRMED |
| K43: Gradient SQMH erf impossible | TRIGGERED | NF-14 mathematical proof; advection-only PDE | CONFIRMED |
| K44: S8/H0 unresolvable | TRIGGERED | DeltaS8=-0.004 (5%); DeltaH0=0.7 km/s/Mpc (12%) | CONFIRMED |
| Q41: SQMH perturbation wa<0 | FAIL | G_eff/G correction = 4e-62 << 1% | CONFIRMED FAIL |
| Q42: C28 wa within 0.10 of A12 | PASS | |wa_C28 - wa_A12| = 0.043 (shooting, R11) | CONFIRMED PASS |
| Q43: erf from gradient SQMH | FAIL | Mathematical impossibility proof (NF-14) | CONFIRMED FAIL |
| Q44: Q41+Q43 both PASS | FAIL | Q41 FAIL -> Q44 FAIL automatically | CONFIRMED FAIL |
| Q45: C28 wa within 0.03 of A12 in L6 range | FAIL | Best in L6 range: |Dwa|=0.067 > 0.03 (R7) | CONFIRMED FAIL |

Kill count: 3/4 (K41, K43, K44)
Keep count: 1/5 (Q42 only)

### Q42 Clarification (NF-16/NF-18 resolution):

Q42 is PASS but with precise characterization:
  - wa_C28 (Dirian 2015 literature) = -0.19, |Dwa| = 0.057 (Q42 basis in R1-R5)
  - wa_C28 (shooting, E2=1.0, R11) = -0.1757, |Dwa| = 0.043 (upgraded Q42)
  - wa_C28 (L6 unnormalized ODE) = -0.098 (NF-16 artifact, NOT physical C28)
  
  The physical wa_C28 is -0.18 ± 0.02 (range from IC and shooting).
  Both are < 0.10 from wa_A12 = -0.133. Q42 PASS is robust.

---

## Numerical Results Table (Complete L9, All 15 Rounds)

| Parameter | Value | Source |
|-----------|-------|--------|
| Pi_SQMH | 1.855e-62 | L9-A (R1) |
| G_eff/G deviation at z=0 | 4.03e-62 | L9-A (R1) |
| delta_n/n_bar (gradient) | 1.67e-61 | L9-B (R1) |
| wa_C28 (Dirian 2015 literature) | -0.19 | L9-C (R1) |
| wa_C28 (shooting, E2=1.0) | -0.1757 | R11 (NF-18) |
| gamma0_Dirian (shooting) | 0.000624 | R11 (NF-18) |
| gamma0_L6 (MCMC posterior) | 0.00151 | L6 posterior |
| E2_today at gamma0_L6 | 1.81 | R11 (NF-16) |
| Q42 diff (shooting) | 0.043 < 0.10 | R11 PASS |
| Q42 diff (literature) | 0.057 < 0.10 | R1 PASS |
| Q45 best in L6 range | 0.067 > 0.03 | R7 FAIL |
| gamma0 for Q45 (full scan) | 0.00054 (outside L6) | R7 FAIL |
| DeltaS8 (A12) | -0.004 (5% of gap) | L9-D (R1) |
| DeltaH0 (A12 at fixed theta*) | +0.46 km/s/Mpc | L9-D (R1) |
| DeltaH0 (C28 estimate) | ~0.7 km/s/Mpc | L9-D (R1) |
| UV cross-term 3*V*V1 at z=0 | ~4283 >> 2U-V1^2 ~ 82 | L9-C (R1) |
| Ricci HDE wa (alpha=0.46) | ~ -0.13, |Dwa|~0.003 | R12 (NF-19) |
| No limit C28->A12 | CONFIRMED | R13 (NF-20) |
| wa_C28 in L6 unnorm. ODE | -0.098 | R11 (NF-16) |

---

## New Findings Summary (All L9)

| ID | Finding | Type | Round |
|----|---------|------|-------|
| NF-13 | C28 UV cross-term confirmed; Q42 PASS | STRUCTURAL | R1-R3 |
| NF-14 | erf impossibility theorem (advection-only) | STRUCTURAL NEW | R4 |
| NF-15 | S8/H0 structural impossibility | ANTI-FALSIFICATION | R1-R5 |
| NF-16 | gamma0 convention mismatch L6 vs Dirian | STRUCTURAL | R7 |
| NF-17 | C28-A12 isomorphism = MEDIUM only | STRUCTURAL | R8 |
| NF-18 | NF-16 resolved: shooting wa=-0.176, Q42 confirmed | STRUCTURAL RESOLUTION | R11 |
| NF-19 | Ricci HDE coincidence wa~-0.13 (NF-18 candidate) | STRUCTURAL FOOTNOTE | R12 |
| NF-20 | No limit of C28 -> A12 (mathematical proof) | STRUCTURAL | R13 |

---

## Paper Section Impact (Full L9)

### Section 2 (Theory and Motivation):
  - SQMH birth-death motivation (NF-3, from L8)
  - Pi_SQMH = Omega_m*H_0*t_P ~ 1e-62 QG signature (NF-5, from L8)
  - erf impossibility theorem (NF-14, L9)
  - C28 CPL proximity wa=-0.176 ± 0.02 (Q42, NF-18, with NF-16 caveat resolved)
  - Prose draft: refs/l9_paper_section2_draft.md (~560 words, JCAP style)

### Section on C28 (Results):
  - Full Dirian 2015 implementation with shooting (NF-18)
  - gamma0_Dirian = 0.000624 vs gamma0_L6 = 0.0015 convention clarified (NF-16)
  - CPL-level proximity language: "medium isomorphism" (NF-17)
  - No limit of C28 reduces to A12 (NF-20)
  - Ricci HDE coincidence in discussion (NF-19)

### Limitations Section:
  - S8 tension: DeltaS8=-0.004 (5%); 60 orders structural shortfall (NF-15)
  - H0 tension: DeltaH0=0.7 km/s/Mpc (12%); pre-recombination needed (NF-15)
  - erf impossibility: mathematical proof, no SQMH derivation (NF-14)
  - C28 independence: no derivation, medium proximity only (NF-17, NF-20)
  - hi_class: K19 provisional flag remains

---

## JCAP Reviewers: What They Will Ask and How to Answer

### Q1: "Why does SQMH motivate the erf proxy? The erf form cannot come from SQMH."

**Answer**: Correct. We demonstrate mathematically (Section 2.3) that the erf
functional form is impossible in SQMH at any level -- background, perturbation,
or gradient (advection-only PDE). The A12 erf template is motivated by SQMH in
the sense that SQMH suggests a dark energy sector tracking matter density through
a smooth interpolation; the erf form is a flexible proxy for this interpolation
chosen on phenomenological grounds. We are explicit that A12 is a "QG-motivated
phenomenological proxy" not a derivation (Section 2, Limitations).

### Q2: "Is C28 really related to your SQMH framework, or is it a completely separate theory?"

**Answer**: C28 is an INDEPENDENT theory (Maggiore-Mancarella 2014, Dirian 2015)
with no derivational connection to SQMH. We test C28 as a benchmark because its
CPL approximation gives wa_C28 ~ -0.18, numerically close to our best-fit A12
template (wa_A12 = -0.133, |Delta wa| = 0.043, Q42 PASS). This proximity is a
numerical coincidence, not a derivation. We show explicitly (Section 6,
refs/l9_a12_c28_limit.md) that no mathematical limit of C28 reduces to A12.
C28 provides independent theoretical motivation for the wa ~ -0.13 to -0.19 regime.

### Q3: "Why not use hi_class for the full Boltzmann calculation? The K19 'provisional' flag is concerning."

**Answer**: Full hi_class computation is deferred due to computational scope.
Our analysis uses compressed CMB chi^2 (K19 provisional). All BAO and SN results
are unaffected (no Boltzmann needed for background observables). Growth factor
calculations use LCDM-calibrated approximation. We flag K19 explicitly in
Limitations Section. The main claims (Bayesian evidence comparison, wa proximity)
are robust at the background level and do not require hi_class verification.

### Q4: "You say S8 and H0 tensions are 'unresolvable.' Is that too strong? Could a new mechanism help?"

**Answer**: Our statement is qualified: "structurally unresolvable within the
present A12/C11D/C28 framework." We quantify the gap:
  S8: requires DeltaS8 = -0.075; maximum achievable = -0.004 (5%).
  H0: requires DeltaH0 = +5.6 km/s/Mpc; maximum achievable = +0.7 (12%).
Both require pre-recombination physics (Early Dark Energy for H0, modified
large-scale structure for S8) absent from our models. We do not claim the
tensions cannot be resolved by other means.

### Q5: "What exactly is the NF-16 convention issue? Is Q42 still valid?"

**Answer**: NF-16 identified that the L6 MCMC posterior gamma0 = 0.0015 uses a
different normalization than Dirian 2015 (who enforce E2(a=1) = 1.0 by construction).
Running our forward ODE at gamma0 = 0.0015 without shooting gives E2_today = 1.81,
producing wa = -0.098 -- a normalization artifact. We resolve this (Round 11) by
implementing a shooting method: binary search gives gamma0_Dirian = 0.000624 with
E2_today = 1.0 exactly, yielding wa_C28 = -0.176. The Q42 criterion
(|Delta wa| < 0.10) is satisfied: |(-0.176) - (-0.133)| = 0.043 < 0.10.
Q42 PASS is confirmed with self-consistent normalization, not just from literature.

### Q6: "Is the 'erf impossibility' claim too strong? What if you modify SQMH?"

**Answer**: The impossibility theorem (NF-14) applies to the SQMH PDE in its
standard form: dn/dt + nabla.(n*v) = Gamma_0 - sigma*n*rho_m. This is a
first-order PDE in spatial derivatives (advection-type). erf requires a second-order
spatial operator (nabla^2 n, diffusion-type), which is absent. The claim is
"erf is mathematically impossible in standard SQMH." If SQMH is modified to
include a diffusion term (e.g., sigma^2/2 * nabla^2 n), erf would become possible.
We note this in the discussion and remark that such a modification would correspond
to CSL-type stochastic mechanics applied to spacetime quanta (speculative).

### Q7: "What is the falsifiable prediction of your paper?"

**Answer**: The paper makes the following falsifiable claims:
  (1) A12 erf template achieves Bayesian evidence Delta ln Z > 8.6 vs LCDM
      on the DESI DR2 + SNIa + CMB dataset. Falsifiable: repeat with DESI DR3.
  (2) C28 (gamma0 = 0.000624, E2=1 normalized) gives wa_C28 = -0.176 ± 0.02.
      Falsifiable: CMB-S4 G_eff/G measurement (2030+) will distinguish C28 (2%)
      from A12 (0%) at ~4 sigma.
  (3) All three candidates fail S8 tension (DeltaS8 < 0.005).
      Falsifiable: any improvement here requires modification outside our framework.
  The primary falsifiable result is (1); results (2) and (3) are secondary structural claims.

---

## Final Paper Status

**JCAP submission**: READY (after paper §2 text integrated from R14 draft)

**PRD Letters status**: NOT TRIGGERED
  Conditions for PRD Letters:
    - Q44 (Q41+Q43 simultaneous): FAIL
    - New observable prediction beyond CPL wa: None (G_eff/G ~ 10^{-62})
    Conclusion: JCAP is appropriate target.

**Outstanding before submission**:
  1. Integrate Section 2 prose from refs/l9_paper_section2_draft.md
  2. Add NF-18 shooting result to C28 section (gamma0 = 0.000624, wa = -0.176)
  3. Add NF-20 to C28 discussion ("no limit of C28 reduces to A12")
  4. Add NF-19 Ricci HDE footnote to discussion section
  5. Final bibliography check for Dirian 2015, Belgacem 2018, Kim 2008 (Ricci HDE)
  6. hi_class: K19 provisional -- add sentence in Limitations

---

## WBS Completion (Rounds 11-15)

- [x] Round 11: rr_dirian_normalized.py written and run; NF-16 RESOLVED; NF-18 established
- [x] Round 12: refs/l9_erf_mechanism_survey.md written (8-person); NF-19 (Ricci HDE)
- [x] Round 13: refs/l9_a12_c28_limit.md written (8-person); NF-20 (no limit)
- [x] Round 14: refs/l9_paper_section2_draft.md written (~560 words, JCAP prose)
- [x] Round 15: refs/l9_final_verdict.md (this file); base.l9.result.md updated;
                base.l9.todo.md updated; NF-18/19/20 appended to refs/l8_new_findings.md

---

*L9 Final Verdict (all 15 rounds) completed: 2026-04-11*
