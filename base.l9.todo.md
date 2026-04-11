# base.l9.todo.md -- L9 Work Breakdown Structure

> Date: 2026-04-11

---

## Phase L9-0: Setup (COMPLETE)

- [x] Read base.l9.command.md, base.l8.result.md, refs/l8_new_findings.md
- [x] Create refs/l9_kill_criteria.md (K41-K44, Q41-Q44 fixed)
- [x] Create base.l9.todo.md (this file)
- [x] Create simulations/l9/ directories (perturbation/, gradient/, c28full/, tensions/, integration/)

---

## Phase L9-A: Perturbation-level SQMH (Q41)

- [x] 8-person parallel team theory derivation
- [x] Write simulations/l9/perturbation/sqmh_growth.py
- [x] Run growth equation with SQMH G_eff/G correction
- [x] Compare f*sigma8 to LCDM
- [x] Q41 judgment: FAIL (G_eff/G - 1 = 4e-62 << 1%; K41 TRIGGERED)
- [x] Write refs/l9_perturbation_derivation.md

---

## Phase L9-B: Non-uniform SQMH gradient term (Q43)

- [x] 8-person parallel team theory derivation
- [x] Write simulations/l9/gradient/sqmh_gradient.py
- [x] Solve spherically symmetric SQMH PDE
- [x] Extract rho_DE(t), check erf-like integral structure
- [x] Q43 judgment: FAIL (erf mathematically impossible; K43 TRIGGERED; NF-14)
- [x] Write refs/l9_gradient_derivation.md

---

## Phase L9-C: C28 Full Dirian 2015 (Q42)

- [x] 8-person parallel team theory derivation
- [x] Write simulations/l9/c28full/rr_full_dirian.py
- [x] Implement Dirian 2015 Eq 2.5-2.8 with UV cross-term
- [x] Extract wa_C28 (literature: -0.19; IC sensitivity issue in numerical)
- [x] Q42 judgment: PASS (|wa_C28 - (-0.133)| = 0.057 < 0.1; NF-13)
- [x] Write refs/l9_c28full_derivation.md

---

## Phase L9-D: S8/H0 tension analysis (Q45)

- [x] 8-person parallel team theory derivation
- [x] Write simulations/l9/tensions/s8h0_analysis.py
- [x] Compute S8, H0 predictions for A12/C11D/C28
- [x] Quantify DeltaS8, DeltaH0
- [x] Q45 judgment: FAIL physical (Delta_S8<0.01; Delta_H0<0.7; K44 triggered; NF-15)
- [x] Write refs/l9_s8h0_analysis.md

---

## Phase L9-N: Numerical integration + erf analysis

- [x] Write simulations/l9/integration/l9_erf_analysis.py
- [x] Collect all channel results
- [x] K41-K44, Q41-Q44 numerical verdict (K41/K43/K44 triggered; Q42 pass)

---

## Phase L9-I: Integration verdict

- [x] 8-person team final consensus
- [x] Write refs/l9_integration_verdict.md
- [x] Append NF-13/14/15 to refs/l8_new_findings.md
- [x] Write base.l9.result.md

---

## Phase L9 Rounds 6-10 (C28-A12 Deepening + Q45)

### Round 6: Limitations Language + Analytic gamma0 Estimate

- [x] Write refs/l9_limitations_language.md (paper-ready limitations text)
- [x] S8 tension: exact language confirmed (CLOSED)
- [x] H0 tension: exact language confirmed (CLOSED)
- [x] erf impossibility: exact language confirmed (NF-14)
- [x] C28 independence: exact language confirmed
- [x] Analytic gamma0 estimate: tentative Q45 PASS at gamma0~0.0011 (flagged for Round 7)

### Round 7: gamma0 Numerical Scan

- [x] Write simulations/l9/c28full/rr_gamma_scan.py
- [x] Write simulations/l9/c28full/rr_gamma_scan_v2.py (corrected wa extraction)
- [x] Run forward ODE scan gamma0 in [0.0003, 0.005]
- [x] Q45 assessment: FAIL (best |Δwa| in L6 = 0.067 > 0.03)
- [x] Optimal gamma0 outside L6: gamma0~0.00054 gives |Δwa|=0.006 but not in L6
- [x] Convention issue documented (NF-16)
- [x] JSON results saved

### Round 8: Deep Isomorphism Analysis

- [x] Write refs/l9_c28_isomorphism.md
- [x] 8-person parallel team (8 angles)
- [x] Mathematical level: DIFFERENT exact functions, CLOSE CPL wa
- [x] Perturbation level: DIFFERENT G_eff/G (~2% C28 vs 0% A12)
- [x] Derivational: INDEPENDENT theories, no limit connects them
- [x] Observational: wa-DEGENERATE at DESI DR2 precision
- [x] Falsifiability: CMB-S4 G_eff/G best discriminator (~2030)
- [x] Paper language confirmed: "CPL-level structural proximity"
- [x] Isomorphism depth: MEDIUM (Q42 only, Q45 FAIL)

### Round 9: Revised JCAP Narrative

- [x] Write refs/l9_paper_synthesis.md
- [x] C28 status upgraded: "CPL structural proximity to A12"
- [x] Proposed section ordering (8 sections) documented
- [x] All L9 additions to each paper section mapped
- [x] PRD Letter status: UNCHANGED (JCAP confirmed)
- [x] NF-17 documented

### Round 10: Final Wrap-up

- [x] Update base.l9.result.md (Rounds 6-10 added)
- [x] Update base.l9.todo.md (this file)
- [x] Append NF-16, NF-17 to refs/l8_new_findings.md
- [x] All K/Q verdicts finalized (K41/43/44 TRIGGERED; Q42 PASS only)
- [x] Q45: FAIL confirmed numerically

---

---

## Phase L9 Rounds 11-15 (NF-16 Resolution + Mechanism Survey + Paper Draft)

### Round 11: NF-16 Resolution (Dirian-Normalized Shooting)

- [x] Write simulations/l9/c28full/rr_dirian_normalized.py
- [x] Implement shooting method: brentq search for gamma0 that gives E2_today=1.0
- [x] Run forward ODE scan gamma0 in [0.0003, 0.30]
- [x] Bracket found: [0.00060, 0.00100]
- [x] gamma0_Dirian (E2=1.0) = 0.000624 (self-consistent)
- [x] wa_C28 (shooting) = -0.1757, |Dwa| = 0.043 -> Q42 PASS CONFIRMED
- [x] wa_L6 (unnormalized) = -0.098 -> NF-16 artifact identified
- [x] Convention mapping: gamma0_L6 = 0.0015 -> E2_today = 1.81 (not 1.0)
- [x] NF-18 established: NF-16 fully resolved
- [x] JSON results saved: rr_dirian_normalized_results.json
- [x] 8-person convention mapping analysis (7 angles)

### Round 12: Physical Mechanism Survey (erf/wa<0)

- [x] Write refs/l9_erf_mechanism_survey.md
- [x] 8-person parallel team survey
- [x] Thawing quintessence CLW: wa<0 qualitative; V~phi^{-0.618} for wa=-0.133; no erf
- [x] Holographic dark energy (Ricci): wa~-0.13 at alpha~0.46; |Dwa|~0.003 (closest!)
- [x] Perez-Sudarsky diffusion: wa<0 tunable; no erf; killed at background (L5)
- [x] C28 RR non-local: wa=-0.176 (shooting); closest physics-motivated; no erf
- [x] CSL/True diffusion: could produce erf; speculative; no cosmological implementation
- [x] NF-19: Ricci HDE as closest mechanism (|Dwa|~0.003); footnote candidate
- [x] Conclusion: no mechanism gives wa=-0.133 from first principles

### Round 13: A12 as IR Limit of C28

- [x] Write refs/l9_a12_c28_limit.md
- [x] 8-person parallel team (7 mathematical angles)
- [x] gamma0->0 limit: no dark energy (not A12)
- [x] gamma0->infinity limit: wa>0 oscillations (not A12)
- [x] E2=1.0 shooting: wa=-0.176 (close but not exact A12)
- [x] de Sitter future: w->-1 (not A12 trajectory)
- [x] Mathematical function: ODE system != CPL algebraic (different structures)
- [x] Perturbation limit: delta_G->0 kills DE (not A12)
- [x] Symmetry group: different symmetries (C28 nonlocal vs A12 pure CPL)
- [x] NF-20: No mathematical limit of C28 -> A12 (CONFIRMED)
- [x] wa=-0.133 appears at gamma0~0.00048 (parameter tuning, not limit)

### Round 14: Draft Paper Section 2

- [x] Write refs/l9_paper_section2_draft.md
- [x] ~560 words JCAP prose format
- [x] Sec 2.1: SQMH birth-death motivation (NF-3, sigma=4piG*t_P)
- [x] Sec 2.2: Background + perturbation level (G_eff/G-1=4e-62, Pi_SQMH)
- [x] Sec 2.3: erf impossibility theorem (4-point proof: background/perturbation/gradient/math)
- [x] Sec 2.4: C28 independent support (wa=-0.176, Q42 PASS, NF-20 no limit)
- [x] All language rules from refs/l7_honest_phenomenology.md checked: PASS
- [x] Open items listed for paper finalization

### Round 15: Final L9 Synthesis

- [x] Update base.l9.result.md with Rounds 11-15
- [x] Update base.l9.todo.md (this file, mark complete)
- [x] Append NF-18/19/20 to refs/l8_new_findings.md
- [x] Write refs/l9_final_verdict.md with Kill/Keep table + JCAP Q&A
- [x] K/Q final verdict confirmed: K41/K43/K44 TRIGGERED; Q42 PASS (CONFIRMED)
- [x] Paper status: JCAP ready; PRD Letter not triggered; outstanding items listed
- [x] JCAP reviewer Q&A: 7 questions with full answers prepared

---

*WBS created: 2026-04-11*
*Rounds 6-10 completed: 2026-04-11*
*Rounds 11-15 completed: 2026-04-11*

### Round 16: Ricci HDE Deep-Dive

- [x] Write simulations/l9/ricci/ricci_hde.py and run simulation
- [x] CPL extraction with correct Kim+2008 closed-form solution
- [x] Jeffreys evidence assessment: BELOW THRESHOLD (Delta ln Z << 0)
- [x] Fourth candidate verdict: REJECTED
- [x] NF-21 established: CPL convention dependence documented
- [x] Write refs/l9_ricci_hde_analysis.md
- [x] Physical structure: rho_DE ~ H^2 (vs SQMH ~ H^{-1}), no birth-death analog

### Round 17: C28 G_eff Profile

- [x] Write simulations/l9/c28full/c28_geff_profile.py
- [x] G_eff/G profile: +2% at z=0, monotone, from NF-13 / Belgacem+2018 calibration
- [x] Planck CMB lensing constraint: PASS (A_lens within 0.3 sigma)
- [x] CMB-S4 (2030+): projected detectable at ~2-4 sigma
- [x] SKAO RSD (2027+): marginal now, discriminating at SKAO precision
- [x] NF-22 established: monotone profile, positive sign, unique MG signature
- [x] Write refs/l9_c28_geff.md

### Round 18: Paper Outline + Abstract

- [x] Write refs/l9_paper_abstract_outline.md
- [x] 9-section outline with word counts (total ~5000 words body + 152 abstract)
- [x] Abstract: 152 words, l7 language check PASS
- [x] Key equations list (8 core equations)
- [x] Outstanding items for submission updated

### Round 19: Adversarial Review

- [x] Write refs/l9_adversarial_review.md
- [x] 6 harshest JCAP reviewer objections with full rebuttals
- [x] None are fatal; paper publishable in JCAP
- [x] Most dangerous: O2 (CPL comparison needed -- action item)

### Round 20: Final Commit Preparation

- [x] Write base_4.md (updated project status, L1-L9 all 20 rounds)
- [x] Update base.l9.result.md with Rounds 16-20 (this session)
- [x] Append NF-21/22 to refs/l8_new_findings.md
- [x] Git add candidates: 10 new/modified files listed in base.l9.result.md
- [x] Update base.l9.todo.md (this file)

*Rounds 16-20 completed: 2026-04-11*
