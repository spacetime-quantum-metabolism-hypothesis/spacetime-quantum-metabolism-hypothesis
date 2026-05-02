# R3 Audit — Root /base.md §14.3 8 axioms (paper/base.md framework)

**Reviewer**: R3 (QFT theorist, cold)
**Scope**: Verify whether the *axiom-consistency 8/8 PASS* claim of root `/base.md §14.3` survives the *paper/base.md framework only* (4 micro foundations: Schwinger-Keldysh, Wetterich RG, Holographic σ₀=4πG·t_P, Z₂ SSB; dark-only embedding μ_eff≈1).
**Script**: `paper/verification_audit/R3_axioms.py` (executed 2026-05-01).

---

## 1. Honest classification rule

| Verdict | Meaning |
|---------|---------|
| **PASS (trivial inherit)** | Standard QFT theorem inherited the moment paper/base.md L⁰ is local + Lorentz scalar + Hermitian. *Not* a novel SQMH win. |
| **PASS (structural)** | Inherited via a *specific* paper/base.md foundation (SK, Z₂, holographic, dark-only). Genuinely SQMH-shaped. |
| **PASS (verified)** | Numerical residual computed; machine-zero in framework. |
| **PARTIAL** | Inherits with caveat (e.g. circularity at derived 4). |
| **NOT_INHERITED** | Framework cannot deliver the claim without external input. |

---

## 2. 8/8 verdict table (R3 cold)

| # | Axiom | Inherit type | Quantitative residual | Verdict |
|---|-------|--------------|----------------------|---------|
| 10 | **Lorentz invariance** (KMS) | trivial QFT + verified | `\|n/(1+n) - exp(−βω)\|` max = **1.39 × 10⁻¹⁷** | **PASS** |
| 11 | **Equivalence principle** | structural (dark-only) | η = 2β_b² = **0** (β_b≡0) vs MICROSCOPE 10⁻¹⁵ | **PASS** |
| 12 | **Uncertainty principle** | trivial QFT | Gaussian min-uncertainty Δx·Δp / (ℏ/2) = **1.000000** | **PASS** |
| 13 | **CPT theorem** | trivial Pauli-Lüders | no internal test (framework-level) | **PASS (trivial)** |
| 14 | **2nd law** | structural (SK) | min(ΔS) over relaxation = **+3.39 × 10⁻²⁹** ≥ 0 | **PASS** |
| 15 | **Holographic principle** | structural (foundation 3) | S_BH(k_B A c³/4Għ) / S_BH(k_B A/4 l_P²) = **1.000000** | **PASS** |
| 16 | **Bekenstein bound** | structural (foundation 3) | S_BH / S_Bek = **1.000000** (Schwarzschild saturation) | **PASS** |
| 17 | **Conservation laws** | Noether + circular d4 | ρ_q / ρ_Λ_obs = **1.0000000000** (5.2 circularity) | **PARTIAL→PASS\*** |

\*A17 PASSes the Friedmann continuity check by construction since paper/base.md derived 4 calibrates n_∞ to ρ_Λ_obs (paper/base.md §5.2 caveat). The conservation law itself is genuine Noether; only the *cosmological coincidence* number is circular.

**Total: 8/8 PASS** in the paper/base.md framework.

---

## 3. R3 cold breakdown — where SQMH actually does work vs. inherits for free

### 3.1 Trivial inheritance (3) — *not novel*

- **A10 Lorentz**, **A12 Uncertainty**, **A13 CPT**: any local Lorentz-scalar Hermitian Lagrangian inherits these. Paper/base.md L⁰ = (∂n)² − V(n) − g_c·n·T satisfies the antecedents. KMS PASS at 10⁻¹⁷ is a *consistency check*, not an SQMH-shaped result.

### 3.2 Structural inheritance (4) — *SQMH-shaped*

- **A11 Equivalence**: dark-only embedding kills baryon coupling β_b → 0 ⇒ η ≡ 0 *structurally*. This is genuinely SQMH (root universal-coupling failure was the whole reason for the dark-only retreat — see CLAUDE.md L2 lessons).
- **A14 2nd law**: SK doubled-contour with retarded G_R analyticity (paper/base.md §2.3 PASS) ⇒ Lindblad-form CPTP map ⇒ H-theorem. Toy 2-level relaxation gives min(ΔS) = +3.4 × 10⁻²⁹ J/K (machine-zero non-negative).
- **A15 Holographic**, **A16 Bekenstein**: the σ₀ = 4πG·t_P foundation 3 directly implies S_BH = k_B A c³/(4Għ), which equals k_B A/(4 l_P²) by definition of l_P, and saturates the Bekenstein bound 2π k_B E R/(ℏc) for Schwarzschild — all three identities collapse to **1.000000**.

### 3.3 Genuine SQMH content (1) — *with caveat*

- **A17 Conservation**: Noether is universal. The cosmic ρ_q = ρ_Λ_obs equality (paper/base.md derived 4) PASSes only because n_∞ is calibrated to ρ_Λ_obs (paper/base.md §5.2 circularity). This is **not** a prediction of energy-momentum conservation — it is the SK input being self-consistent with the cosmological output. Honest mark: **PASS as consistency, not as derivation**.

---

## 4. What this audit does *not* claim

- No claim that paper/base.md *predicts* any of the 8 (Lorentz, EP, uncertainty, CPT, 2nd law, holography, Bekenstein, conservation) — these are *consistency*, not *consequences*.
- No claim that 8/8 PASS distinguishes SQMH from ΛCDM + standard QFT — both pass identically.
- A17 ρ_q = ρ_Λ_obs identity has the *5.2 circularity caveat* and must not be advertised as a derivation in the paper.

---

## 5. Honesty one-liner

**8/8 PASS, but only A11 (dark-only EP), A14 (SK 2nd law), A15/A16 (σ₀=4πG·t_P holography) are SQMH-shaped — A10/A12/A13 are trivial QFT inheritance and A17 is consistency-not-derivation.**
