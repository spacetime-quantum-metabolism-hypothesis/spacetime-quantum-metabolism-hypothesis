# 8. Discussion and Limitations

We honestly list the limitations of this work, following base.md §10.4
and §XVI-XVII.

## 8.1 Effective field theory status

SQMH, as stated in §2, is a classical hypothesis about a discrete
micro-structure of spacetime.  The candidate families in §3 are
**effective field realisations** of this hypothesis, not first-principles
derivations.  In particular:

- The **non-local gravity** candidates (C27, C28) have their auxiliary
  fields inspired by, but not uniquely dictated by, the SQMH continuity
  equation.
- The **RVM family** (C23, C5r, C6s) assumes a specific functional form
  Λ(H²) = Λ₀ + 3νH², which is a truncation of a presumed RG flow.
- The **unimodular diffusion** candidate (C26) is the most direct SQMH
  L0/L1 realisation, but it assumes a specific form for the diffusion
  current J⁰ ∝ H that is not uniquely fixed by the axioms.
- The **IDE candidates** (C41, C11D, C10k) are fluid-level rewrites that
  do not attempt to derive the coupling from a micro-Lagrangian.

A full UV completion of SQMH — in which σ = 4πG t_P and Γ₀ are derived
from a single quantum theory of discrete spacetime — is a Phase 6 goal.

## 8.2 Hubble tension residual

None of the candidates substantially resolves the H₀ tension.  All
best-fit values cluster around h ≈ 0.668–0.680, compared to the
distance-ladder measurement h ≈ 0.732.  The DESI-compatible w_a < 0
drift lowers the inferred CMB-anchored H₀ by only Δh ≈ +0.01, which is
insufficient to close the ~5% gap.  We report this honestly rather than
hide it.

## 8.3 σ_8 / S_8 tension

The C10k (dark-only coupled) candidate, if accepted via the growth
channel, produces a σ_8 *enhancement* of ~2.3% for β_d ~ 0.107, which
**worsens** the existing S_8 ~ 2σ tension between Planck and weak
lensing surveys (KiDS, DES).  This is a structural cost of the dark-only
coupling mechanism and the reason why C10k is flagged "KEEP-growth"
rather than unconditional KEEP.

Other candidates (C27, C28, C33, C41, C26, C23, C5r, C6s) do not
modify linear growth appreciably and so do not worsen S_8.

## 8.4 Free parameter count

The strict SQMH as stated in §2 has **zero** free background parameters
(σ, Γ₀ derived from G, t_P, H₀, Ω_m, Ω_Λ).  The effective field
realisations in §3 introduce 1-3 additional parameters per candidate
(e.g. f₁, n for C33; α_Q for C26; β for C41; ν for C5r).  These
parameters should be regarded as phenomenological couplings whose
ultimate UV origin is the SQMH micro-theory.

## 8.5 DESI dependence

The main data-driven signal (w_a < 0) comes from DESI DR2 BAO alone.
The DR1 → DR2 transition already changed the central w_a value
significantly.  A DR3 result could further shift the preferred range;
our analysis should be re-run against DR3 when available.  The code is
parameter-reproducible (seed 42, pinned data files) so the re-run is
mechanical.

## 8.6 No phantom crossing promise

Our kill criterion K3 hard-excludes any w(z) crossing −1.  This is
motivated by ghost avoidance and by the SQMH sign rule (matter → DE
metabolism).  Some dark-energy EFT literature treats phantom crossing as
acceptable; we do not.  Readers who accept phantom crossing should
re-evaluate the L2 candidates we discarded at the structural level.

## 8.7 4-reviewer self-critique log

Each candidate's `simulations/l4/<ID>/review.md` documents a 4-reviewer
pass (numerical correctness / physical consistency / reproducibility /
CLAUDE.md rule compliance).  No candidate was accepted without all four
reviewers passing.
