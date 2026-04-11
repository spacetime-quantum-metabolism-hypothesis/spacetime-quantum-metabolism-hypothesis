# 9. Conclusion

We tested whether the Spacetime Quantum Metabolism Hypothesis — matter
annihilates discrete spacetime quanta while vacuum generates them at a
universal rate — admits effective field realisations that simultaneously
satisfy the DESI DR2 BAO + DESY5 SN + compressed Planck CMB + 8-point
RSD joint likelihood, Cassini |γ−1| < 2.3 × 10⁻⁵, no phantom crossing,
and direct SQMH L0/L1 interpretation.

Starting from ~40 candidate families at L2, five analysis levels
(L2 structural screen, L3 background toy, L4 full-Boltzmann MCMC,
L5 production MCMC + Bayesian evidence + cosmic shear + DR3 Fisher)
reduced the catalogue to **three Phase-5 winners**:

---

**Winner 1: C11D — Pure-disformal IDE quintessence (Tier-1, rank 1)**

- Δχ² = −22.12, Δ ln Z = +8.95 (STRONG), 1 parameter (λ)
- w_0 = −0.877, w_a = −0.186 (no phantom crossing, structural guarantee)
- L4 K3 kill cleared: CPL-template artefact, exact CLW ODE has w ≥ −1
- DESI DR3 Fisher: ~2.9σ LCDM separation
- SQMH interpretation: pure-disformal coupling (A' = 0) = minimal quintessence
  at background level; λ ~ 0.9 drives the metabolism-balanced dark energy drift.

**Winner 2: C28 — Maggiore-Mancarella RR non-local gravity (Tier-1, rank 2)**

- Δχ² = −21.08, Δ ln Z = +11.26 (STRONG, evidence-top-ranked), 1 parameter
- w_0 = −0.849, w_a = −0.242 (no phantom crossing, Cassini γ=1 exact)
- DESI DR3 Fisher: 3.91σ LCDM separation (strongest of all winners)
- SQMH interpretation: non-local auxiliary field (U, S) acts as a
  metabolic memory of matter-to-DE drift history.

**Winner 3: A12 — erf-diffusion, canonical alt-20 class representative (Tier-2)**

- Δχ² = −21.62, Δ ln Z = +10.78 (STRONG), 0 parameters
- w_0 = −0.886, w_a = −0.133
- Represents a single canonical drift class of 14 alt-20 candidates
  (SVD n_eff = 1, participation ratio = 1.017)
- DESI DR3 Fisher: 2.16σ (borderline Q9 pass)
- SQMH interpretation: erf-diffusion is the integrated profile of a
  matter-proportional metabolism rate locked to the SQMH Ω_m normalisation.

---

## 9.1 Demotions and kills

**C33 f(Q) teleparallel** — demoted by triple S_8 failure (K15+Q10+Q11):
S_8 = 0.891 exceeds DES-Y3 3σ upper bound.  Δ ln Z = +2.508 (borderline Q8).
Relegated to appendix as a negative result with DR3 prediction.

**C26 Perez-Sudarsky** — confirmed KILL.  J⁰ = α_Q H ρ_m ansatz is
CMB-dead at any α_Q ≥ 0.02 (sound-horizon explosion).  Negative result
consistent with base.md §XVI: SQMH unimodular diffusion requires a
perturbation-level mechanism beyond the background.

**All other L4 kills confirmed**: C27 (posterior collapse), C41 (Cassini),
C10k (w_a ≡ 0 + σ_8), C23/C5r/C6s (wrong-sign ν), C32 (w_a=0 structural).

## 9.2 Two critical negative results

1. **Zero-parameter alt candidates achieve the same Bayesian evidence as
   1-parameter C28.** The extra free parameter in C28 relative to A12 is not
   statistically justified (Δ ln Z gap = 0.48, vs Occam penalty ~0.5).
   The DESI DR2 signal is well-described by a single drift direction in
   E²(z) space.  This does not falsify C28 (it is still a STRONG winner),
   but it means the data cannot prefer it over A12 on model-selection grounds.

2. **S_8 tension is not resolved by any winner.**  All μ=1 background-only
   models cannot structurally address weak-lensing tension.  Phase 6 must
   introduce perturbation-level modifications (μ(a,k) ≠ 1) via SQMH
   axioms at the perturbation level.

## 9.3 DESI DR3 prediction

For all three winners we predict:
- w(z=0) ∈ [−0.877, −0.849] (less negative than −1)
- w(z) monotonically decreasing toward −1 at high z
- **No phantom crossing** — SQMH L0/L1 structural guarantee
- LCDM separation ≥ 2σ in DR3 Fisher forecast (Q9 pass for all three)

If DESI DR3 w_a < 0 tightens and h > 0.677 improves, C11D (rank 1) is the
primary testable prediction.  If DR3 observes A04-like |w_a| = 0.469 signal
at 7.98σ separation, the alt-20 class hypothesis would be strongly indicated.

The code is pinned (seed 42, data SHA-256 hashes) and DR3 re-runs are mechanical.

## 9.4 Outlook to Phase 6

1. Full 48×2000 production MCMC (K13 formal pass) on high-CPU hardware
2. Perturbation-level modifications (μ(a,k) ≠ 1) via SQMH axioms
3. hi_class full disformal (A' ≠ 0) — check if γ−1 ≠ 0 at any level
4. S_8 tension structural resolution — requires growth-sector coupling
5. DESI DR3 real data verification when available

**Final statement**: DESI DR2 w_a < 0 preference is reproduced with
Bayesian STRONG evidence by three SQMH-compatible effective field
realisations, none requiring phantom crossing, and all consistent with
Cassini PPN constraints.  If DR3 confirms w_a < 0 and tightens it beyond
2σ, at least one winner will remain viable.  If all three fail the DR3
test, SQMH in its present background-level form is falsified, and the
hypothesis requires either a perturbation-sector UV completion or outright
revision.
