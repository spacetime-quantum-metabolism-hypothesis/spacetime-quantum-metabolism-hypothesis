# base.l4.todo — L4 execution WBS

## Phase L4-0. Setup
- [x] refs/l4_kill_criteria.md commit
- [x] simulations/l4/ tree
- [x] data_loader reuse from L3
- [x] base.l4.todo.md committed

## Phase L4-A. Full-Boltzmann backgrounds (10 candidates)
- [ ] C27 Deser-Woodard (Dirian 2015 Eq 2.5-2.8, U/V localisation)
- [ ] C28 Maggiore RR non-local (U/S localisation)
- [ ] C33 f(Q) teleparallel (Frusciante 2021 original Friedmann)
- [ ] C41 Wetterich fluid IDE (coupled continuity, β≤0.05 regime)
- [ ] C26 Perez-Sudarsky unimodular diffusion
- [ ] C23 Asymptotic Safety (Bonanno-Platania, ξH RG identification)
- [ ] C5r RVM ν<0 branch (Gomez-Valent-Sola 2024)
- [ ] C6s Stringy RVM + CS (background identical to C5r)
- [ ] C11D Disformal IDE hi_class-style full (pure disformal, γ_D∈[0,5])
- [ ] C10k Dark-only coupled (background + growth channel)

## Phase L4-B. Linear perturbations (10 candidates)
- [ ] Per-candidate δ_m, θ_m, (δφ or fluid DE) ODE
- [ ] μ, Σ, G_eff/G extraction
- [ ] c_s² positivity + ghost check
- [ ] fσ_8(z) prediction on 8 RSD redshifts

## Phase L4-C. MCMC posteriors (10 candidates)
- [ ] emcee 64×20000, burn 5000, seed 42
- [ ] log_prob -∞ on chi² failure (no sentinel)
- [ ] R̂ < 1.05
- [ ] corner plot saved

## Phase L4-D. Special handling
- [ ] C27 vs C28 full-eqs differentiation
- [ ] C33 sign re-confirmation (f_1 sign → w_a sign)
- [ ] C11D hi_class disformal full re-judgement (K2)
- [ ] C10k growth channel (G_eff/G, σ_8) evaluation

## Phase L4-E. Phase 5 candidate selection
- [ ] Q1-Q6 scoring all 10
- [ ] Ranking by Δχ² + theory score tie-break
- [ ] 2-3 main + 1-2 backup

## Phase L4-F. Paper draft (9 English sections)
- [ ] paper/00_abstract.md
- [ ] paper/01_introduction.md
- [ ] paper/02_sqmh_axioms.md
- [ ] paper/03_background_derivation.md
- [ ] paper/04_perturbation_theory.md
- [ ] paper/05_desi_prediction.md
- [ ] paper/06_mcmc_results.md
- [ ] paper/07_comparison_lcdm.md
- [ ] paper/08_discussion_limitations.md
- [ ] paper/09_conclusion.md
- [ ] paper/references.bib

## Phase L4-G. 4-reviewer loop
- [ ] Per candidate review.md (numerical / physical / reproducibility / rules)

## Phase L4-H. Ranking + final verdict
- [ ] simulations/l4/ranking.py
- [ ] base.l4.result.md integrated report

## Phase L4-I. Housekeeping
- [ ] CLAUDE.md L4 prevention rules
- [ ] base.l4.todo.result.md execution log
