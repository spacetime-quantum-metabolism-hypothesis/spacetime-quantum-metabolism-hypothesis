# L392 ATTACK DESIGN — Sec 3 (Branch B) Final Draft

## Mission
Produce a LaTeX-ready outline for **Section 3 (Branch B: Cosmological Phenomenology)** of the SQMH paper, integrating:

1. The **3-regime baseline narrative** (user insight, L390/L391):
   - Regime I (z ≲ 0.5): late-time DE-dominated phenomenology
   - Regime II (0.5 ≲ z ≲ 2): transition / matter-DE crossover
   - Regime III (z ≳ 2): high-z BAO + sound-horizon anchor
2. **L342 result**: 17σ rejection of the strict ψ-monotone (a priori) family
3. **L346 caveat**: amplitude-locking is *fit*, not prediction (Q17 partial; Δρ_DE ∝ Ω_m structurally derived; coefficient = 1 from E(0)=1 normalisation, not dynamics)
4. One **honest line** stating the epistemic posture

## Honesty Posture (one-line, mandatory)
> "SQMH passes a falsifiable phenomenological test (3-regime monotone family rejected at 17σ) but does not yet predict the amplitude of the dark-sector anomaly from first principles."

This sentence appears verbatim in:
- Sec 3 abstract paragraph
- Sec 3 conclusion
- Discussion (Sec 5) via cross-reference

## Section 3 Skeleton

### 3.1 Setup and notation
- Recap of SQMH dark-sector kernel (ref. Sec 2)
- Definition of ψ(z) "vacancy density" proxy and the **monotone class** M = {ψ : dψ/dz ≤ 0}
- 3-regime decomposition rationale (data-driven, not theory-driven; cite L390 user insight)

### 3.2 The 3-regime baseline (B0)
- Regime I — DESI BAO low-z (BGS, LRG1)
- Regime II — DESI BAO mid-z (LRG2/3, ELG1/2, QSO)
- Regime III — Lyα BAO (z_eff ≈ 2.33) + compressed CMB θ*
- Statistical setup: 13-pt DESI DR2 + full covariance, Hu-Sugiyama θ* with 0.3% theory floor
- Free parameters: Ω_m, h, plus regime-specific shape (3 dof per regime, AICc-penalised)

### 3.3 A priori monotone test (L342)
- Strict ψ-monotone family with **no free shape**, only Ω_m, h
- Result: Δχ² = +N (vs LCDM), **17σ rejection** of the parameter-free monotone class
- Interpretation: ψ-monotonicity alone is insufficient; the data demand structure beyond simple monotone decay
- This is the **falsifiable kill** — reported as the principal Branch-B result

### 3.4 Amplitude-locking fit (L346 caveat — explicit)
- 3-regime fit recovers Δρ_DE ∝ Ω_m with coefficient ≈ 1
- **Caveat box (LaTeX `\fbox{}` or `tcolorbox`):**
  - The proportionality Δρ_DE ∝ Ω_m is **structurally derived** from the SQMH continuity ansatz (Q17 partial)
  - The coefficient = 1 is **fixed by E(0)=1 normalisation**, not by dynamics
  - Therefore: amplitude-locking is a **post-hoc fit consistent with SQMH**, not an a priori prediction
  - Q17 status: **partial** (structural form yes, amplitude no)

### 3.5 Statistical caveats and robustness
- L33 integration audit (N_GRID=4000, cumulative_trapezoid, ratio clipping)
- BAO-only low-Ω_m artefact (Ω_m≈0.07 best-fit; **not** the joint Ω_m)
- Joint BAO+SN+CMB pulls Ω_m ≈ 0.30, k=2 free parameters
- Bayesian evidence: A12 (0-param drift) vs C28 (1-param) → Δ ln Z ≈ 0.48, below Occam threshold
- DR3 Fisher: pairwise discrimination ≈ 0.19σ — **DR3 will not resolve** between SQMH-class fits and mainstream alts

### 3.6 Honest summary
- Branch B status: **falsifiable test passed (monotone rejection robust); predictive amplitude not yet derived**
- Position relative to literature: phenomenological alternative to CPL, comparable evidence to RVM/non-local-gravity at current data quality
- Roadmap: full hi_class implementation (Phase 7) for K20 (true a priori amplitude) attempt

## Review gates (Rule-A 8-person)
- T1: 3-regime decomposition justified (not over-fit)?
- T2: 17σ number traceable to L342 covariance + dof accounting?
- T3: L346 caveat phrased without overclaim?
- T4: Honesty line consistent across abstract/body/conclusion?
- T5: AICc/BIC/Occam consistent with L5 lessons?
- T6: No PRD-Letter language; JCAP-target tone preserved (L6 rule)?
- T7: Cassini/PPN compliance not over-claimed (μ_eff≈1, S_8 not solved)?
- T8: Sign conventions (ν, β, ξ_q) and SQMH-consistent branch flags present?

## Deliverable cadence
1. ATTACK_DESIGN.md (this file) — done
2. SEC3_DRAFT.md — LaTeX-ready outline with paragraph stubs + figure/table placeholders
3. REVIEW.md — 8-gate review record + final verdict
