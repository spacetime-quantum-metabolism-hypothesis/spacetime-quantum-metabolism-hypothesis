# 8. Discussion and Limitations

We honestly list the limitations of this work, following base.md §10.4
and §XVI–XVII.

## 8.1 Effective field theory status

SQMH, as stated in §2, is a classical hypothesis about a discrete
micro-structure of spacetime.  The candidate families in §3 are
**effective field realisations** of this hypothesis, not first-principles
derivations.  In particular:

- **C11D** (pure disformal) is the most principled: the background is
  exactly minimally coupled quintessence (ZKB 2013), with disformal
  coupling entering only at the perturbation level.  The V(φ) slope λ
  should ultimately be derived from the SQMH micro-theory.
- **C28** (RR non-local) has auxiliary fields (U, S) inspired by, but not
  uniquely dictated by, the SQMH continuity equation.
- **A12 / alt-20 class** is a phenomenological closed-form E²(z)
  parametrisation.  The SQMH L0/L1 interpretation is that the erf drift
  represents the integrated matter-to-DE metabolism flow over cosmic time.

A full UV completion — deriving σ = 4πG t_P and Γ₀ from a single quantum
theory of discrete spacetime — is a Phase-6 goal.

## 8.2 Hubble tension residual

None of the candidates resolves the H₀ tension.  All winners cluster at
h ≈ 0.677–0.678, vs. distance-ladder h ≈ 0.732 (SH0ES).  The DESI-compatible
w_a < 0 drift reduces the gap by only Δh ≈ +0.009, insufficient to close
the ~7% discrepancy.  C33 (demoted) worsens it.

## 8.3 S_8 / σ_8 tension — structural non-resolution

All Phase-5 winners have μ_eff = 1 (no modified gravity at sub-horizon
scales).  The cosmic-shear S_8 tension (Planck ~ 0.834 vs DES-Y3 ~ 0.772,
KiDS-1000 ~ 0.759, ~2.5σ gap) is therefore **not resolved** by any winner.

The apparent S_8 improvement for some candidates comes from Ω_m shifting;
this is a parametric artefact, not a structural resolution.

C33 f(Q) (demoted) is the cautionary example: its best-fit Ω_m = 0.340
raises S_8 = 0.891 via S_8 ∝ √(Ω_m/0.3), exceeding the DES-Y3 3σ upper
bound.  This is a structural cost of the teleparallel rescaling.

DES-Y3 and KiDS-1000 cosmic-shear data were applied as K15 / Q10 / Q11
criteria in L5-D:
- **K15**: S_8(winner) < 0.84 — passed by C11D, C28, A12; failed by C33.
- **Q10**: Δχ²_WL ≤ +3 vs LCDM — passed by all winners; C33 Δχ²_WL = +54.5.
- **Q11**: |Δh_tension| ≤ +0.005 — passed by all winners; C33 worsens.

## 8.4 Free parameter count and zero-parameter evidence

The strict SQMH has zero free background parameters (§2).  The effective
realisations introduce 0–2 extra parameters per candidate.

**Phase-5 observation (fixed-θ)**: the zero-parameter A12 (erf-diffusion)
achieves Δ ln Z = +10.779, nearly matching the 1-parameter C28
(Δ ln Z = +11.257). Raw gap = 0.48 nats, consistent with marginal benefit.

**Phase-6 confirmation (fully marginalized)**: L6-E dynesty runs
(nlive=800, seed=42, LCDM ln Z = −843.538) decisively confirm the result.
Full 3D marginalization of C28 yields Δ ln Z = +8.633 — **2.14 nats below**
A12's fully marginalized Δ ln Z = +10.769.  The ordering reverses: the
zero-parameter model A12 is preferred over C28 by more than 2 nats even
before any Occam correction.  With the Gaussian Occam penalty
(Δ = −1.38 nats for 1 extra dimension), the net difference is −3.52 nats
against C28.

This means **data decisively do not justify the extra parameter in C28
relative to A12**.  C28's fixed-θ lead (+0.48 nats) was an artefact of
fixing γ₀ at the L4 MAP, which concentrates the posterior artificially.
Full prior-volume integration erases this lead and reverses it.

Interpretation: the DESI DR2 preference is well-described by a single
drift direction in E²(z) space (confirmed by SVD n_eff = 1, §A).  Any
closed-form that captures this drift with sufficient curvature achieves
evidence indistinguishable from, or exceeding, LCDM+1-parameter models.
This is not evidence of richer physics; it is evidence of a 1-D data
preference that favours parsimony.

## 8.5 Production MCMC (K13) — Phase-5 final results

The K13 criterion (R̂ < 1.02, 48 walkers × 2000 steps, burn=500, thin=10)
was run to completion (2026-04-11). Results:

| ID | R̂_max | Δχ² | K13 | Time |
|---|---|---|---|---|
| C11D | **1.0114** | −22.063 | **PASS** | 194 min |
| A12  | 1.0095 | −21.617 | **PASS** | 26 min |
| A17  | 1.0085 | −21.257 | **PASS** | 34 min |
| A01  | 1.0078 | −21.117 | **PASS** | 22 min |
| A05  | 1.0105 | −21.030 | **PASS** | 32 min |
| C28  | 1.3653 | +5.272  | **FAIL** | 55 min |

**C11D, A12, A17, A01, A05: K13 formally passed.**
C28 fails K13 (R̂=1.37) due to 5D parameter space not mixing at 48×2000.
C28's MCMC Δχ² = +5.272 is unreliable (non-converged posterior);
Bayesian evidence (+11.26, fixed-θ) remains the relevant metric for C28.
C28 remains a Phase-5 winner on evidence grounds pending full 3D marginalization.

~100 ms/call × 48 × 2000 ≈ 5–6 hours per candidate (CLW ODE overhead for C11D).

## 8.6 Alt-20 canonical drift class degeneracy

The 14-candidate alt-20 cluster is confirmed as a single canonical drift
class (SVD n_eff = 1, participation ratio = 1.017, 99.15% variance in
mode 1).  The cluster spans erf, sqrt, exp, tanh, arctan, and other
functional forms — all are reparametrisations of the same m·(1−a) drift
direction in E²(z) space.

This has two implications:

1. **The 14 candidates do not represent 14 independent physics hypotheses.**
   They represent one physical effect captured by different basis functions.
   arXiv submission presents A12 as the single representative.

2. **The SQMH L0/L1 "canonical drift" prediction (matter-weighted Ω_m
   drift in E²) is confirmed as a viable 0-parameter description of the
   DESI DR2 signal.** Whether this is the correct UV physics or a numerical
   coincidence is a Phase-6 question.

## 8.7 DESI data dependence

The main signal (w_a < 0) is driven by DESI DR2 BAO.  The DR1 → DR2
transition already changed central w_a significantly.  A DR3 result could
further shift the preferred range.  All code is parameter-reproducible
(seed 42, pinned data files); re-runs against DR3 are mechanical.

## 8.8 C26 negative result — unimodular diffusion boundary

C26 Perez-Sudarsky diffusion was the most direct SQMH L0/L1 interpretation
candidate.  The reformulated ansatz J⁰ = α_Q H ρ_m eliminates the original
ODE blow-up but introduces CMB dead zone: any α_Q ≥ 0.02 drives χ²_CMB
above 38 (LCDM baseline 2.3), due to matter density decaying as a^(−(3+α_Q))
and shifting the sound horizon beyond Planck tolerance.

Conclusion: **Perez-Sudarsky unimodular diffusion + matter-proportional
current is CMB-dead at background level**.  A perturbation-level channel
(new physics beyond background) would be needed for revival.  This is
recorded as a Phase-5 negative result, consistent with §XVI of base.md.

## 8.9 Phase-6 Theory Positioning (8-person sequential review)

A Phase-6 eight-person sequential theory review (L6-T3, `refs/l6_theory_positioning.md`)
reached the following consensus on the theoretical status of SQMH:

**Claims supported by 8-person consensus**:
1. SQMH continuity equation motivates wₐ < 0 structure (not re-description).
2. C11D pure disformal BAO+SN+CMB+RSD+S₈ 5-channel fit: Δχ² = −22.063 (K13 pass R̂=1.011).
3. A'=0 → γ=1 PPN is structural (disformal geometry) and GW170817-enforced.
4. DR3 falsifiable prediction at 2.9–3.9σ (Fisher).

**Claims NOT supported** (8-person consensus prohibits):
1. "SQMH derives DESI acceleration" — re-description cannot be excluded.
2. "Amplitude-locking is first-principles" — theory-motivated normalization귀결, not full derivation.
3. "SQMH integrates 5 independent physics programs" — cosmology channel only verified.
4. "C28 is a SQMH model" — independent Maggiore-Mancarella theory.

**Phase-6 amplitude-locking result** (L6-T1): Δρ_DE ∝ Ω_m arises from
SQMH annihilation term σ·n̄·ρ̄_m ∝ ρ_m ∝ Ω_m (partial derivation).
Exact coefficient unity = E(0)=1 normalization귀결. K20 not triggered.
Journal target remains JCAP pending full marginalized evidence (L6-E).

## 8.10 No phantom crossing promise

K3 hard-excludes any w(z) crossing −1.  All winners satisfy this.
C11D's apparent L4 phantom crossing was a CPL-template artefact (CLAUDE.md
L5 rule added).  Readers who accept phantom crossing should re-evaluate
the L2 candidates discarded at the structural level.
