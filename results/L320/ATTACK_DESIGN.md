# L320 — Simulated Reviewer Attack Design

**Loop**: L320 (single)
**Target**: JCAP submission. Pre-empt referee report by simulating 3 typical reviewer profiles.
**Date**: 2026-05-01

## 1. Reviewer profile mapping

JCAP cosmology submissions are typically routed to three referees with overlapping but distinct lenses. We assume the editor selects:

| Slot | Profile | Likely background | Primary lens |
|------|---------|--------------------|--------------|
| R1 | Theorist | Modified gravity / scalar-tensor / EFT | Derivation rigor, symmetries, naturalness |
| R2 | Observer | LSS / galaxy rotation curves / weak lensing | Data fit quality, systematics, S_8 / H_0 tensions |
| R3 | Statistician | Bayesian inference / model comparison / DESI | Evidence calculation, anchor sensitivity, false-detection risk |

## 2. Attack vectors per reviewer

### R1 (Theorist) — expected attacks

- **A1.1**: D5 (galaxy-scale ψ^n equation) derivation — "where does the n=2.95±0.13 exponent originate? Is it postulated or derived from D1–D4?"
- **A1.2**: RG cubic running coefficient — "the β-function cubic term coefficients are stated as phenomenological. Where is the loop calculation?"
- **A1.3**: Tree-level vs loop consistency — "are pillars D1–D4 only valid at tree level? What about UV completion?"
- **A1.4**: Disformal / conformal frame ambiguity — "which frame are observables computed in?"

### R2 (Observer) — expected attacks

- **A2.1**: SPARC fit details — "175 galaxies but only χ²/N reported per family; show per-galaxy residuals and outlier handling"
- **A2.2**: S_8 worsens by ~1% vs ΛCDM — "this is a regression, not progress"
- **A2.3**: BAO sample selection — "DESI DR2 13-point full covariance — are BGS / LRG / ELG / QSO bins all included?"
- **A2.4**: μ_eff ≈ 1 means no growth signal — "how does the model explain RSD without G_eff modification?"

### R3 (Statistician) — expected attacks

- **A3.1**: BB ΔAICc = 99 anchor dependence — "L272 mock test claims robustness; show null distribution explicitly"
- **A3.2**: Marginalized evidence ΔlnZ = 0.8 vs fixed-θ ΔAICc = 99 — "these are inconsistent. Which is the headline?"
- **A3.3**: False-detection rate — "what is the probability that a random non-SQMH model with the same parameter count produces ΔAICc ≥ 99?"
- **A3.4**: LOO cross-validation — "leave-one-out across BAO bins / SN compilations / RSD points?"

## 3. Pillars vs attacks

| Pillar | R1 covers? | R2 covers? | R3 covers? |
|--------|------------|------------|------------|
| D1 (ψ axiom) | A1.3 | – | – |
| D2 (FLRW) | – | A2.3 | A3.1 |
| D3 (perturbation) | A1.4 | A2.4 | – |
| D4 (PPN) | A1.4 | – | – |
| D5 (galaxy ψ^n) | A1.1 | A2.1 | – |
| RG cubic | A1.2 | – | A3.2 |
| 7 falsifiers | – | A2.2 | A3.3, A3.4 |

## 4. Defense strategy

- **Honesty-first**: limitations table (paper Sec 6.4) is the primary shield. Concede S_8 worsening, μ_eff ≈ 1 background-only structure, RG coefficients phenomenological.
- **7 falsifiers as offensive weapon**: every concern about overfitting is parried by the explicit pre-registered kill conditions (K-list).
- **L272 / L276 / L281 stack**: anchor-mock + LOO-CV + marginalized evidence form a 3-layer statistical defense for R3.
- **Future-work scoping**: A1.1 (D5 derivation), A1.2 (loop RG), A2.4 (μ_eff modification) explicitly deferred to follow-up papers — prevents reviewers demanding scope creep.

## 5. Severity triage

| Attack | Severity | Resolution |
|--------|----------|------------|
| A1.1 | High | Future work + tree-level adequacy argument |
| A1.2 | Med | Future work, current pillars do not require it |
| A2.1 | Med | Add Appendix table on request |
| A2.2 | High | Honest concession, structural explanation, Sec 6.4 |
| A3.1 | High | Cite L272 mock; offer additional anchor-permutation test |
| A3.2 | Med | Clarify: ΔAICc = pointwise fit, ΔlnZ = Occam-corrected; both reported |
| A3.3 | Med | Cite L272 null mock false-positive rate |
| A3.4 | Low | L276 LOO-CV already in supplementary |

## 6. Response template structure

For each reviewer:
1. Thank the referee for the careful reading.
2. Quote the concern verbatim.
3. State whether: (a) addressed in revision, (b) clarified, (c) future work.
4. Point to specific section / equation / figure.
5. If textual change: paste the new paragraph in the response letter.

No combative language. No dismissals. Concede limitations openly — falsifiability is the headline, not perfection.
