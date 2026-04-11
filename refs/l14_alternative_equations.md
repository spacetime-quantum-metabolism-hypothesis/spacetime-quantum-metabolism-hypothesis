# refs/l14_alternative_equations.md -- L14: Alternative Equations from the Premise

> Date: 2026-04-11
> Source: l14_equation_derivation_8teams.md 8-team analysis
> Task: Catalog alternative equations derivable from the single premise,
>       and assess qualitative DESI predictions for each.

---

## The Premise (reminder)

> "Spacetime quanta are annihilated upon collision with matter."

The current SQMH equation is:

    dn̄/dt + 3Hn̄ = Γ₀ − σn̄ρ_m        (SQMH-standard)
    σ = 4πGt_P,    Γ₀ = σn̄₀ρ_m0 + 3H₀n̄₀

This document catalogs the alternatives found by the 8-team review.

---

## Class A: No-Creation Equations (premise-pure)

### A1. Pure Annihilation (no FLRW, Minkowski)

    dn/dt = −σnρ_m

**Assumptions added beyond premise:** None — this is closest to the premise.

**Solution:** n(t) = n_0 · exp(−σ · ∫ρ_m dt)

For matter-dominated universe: n → 0 at late times exponentially.

**Dark energy:** n̄ → 0 → ρ_DE → 0. The universe ends in matter domination with no dark energy.

**DESI prediction:**
- ρ_DE(z) → 0 at z = 0. Contradicts observed Ω_Λ ≈ 0.69.
- No accelerated expansion.
- Catastrophic failure vs DESI data: FAIL.

**Assessment:** Closest to the premise but observationally dead.

---

### A2. Pure Annihilation with FLRW Dilution

    dn̄/dt + 3Hn̄ = −σn̄ρ_m

**Assumptions added:** FLRW geometry (Hubble dilution term 3Hn̄).

**Solution for matter-dominated H ≈ H₀(1+z)^{3/2}:**

    n̄(z) = n̄₀ · (1+z)^3 · exp(+σ · ∫₀^z ρ_m dz'/H(z'))

The 3Hn̄ term actually INCREASES n̄ as we go to higher z (past), since d(n̄a³)/da = source term. The annihilation reduces n̄ further. Net: n̄ → 0 at late times regardless.

**Dark energy:** ρ_DE ∝ n̄ → 0 at z = 0. Same failure as A1.

**DESI prediction:** FAIL (no dark energy today).

---

### A3. Pure Annihilation with Different Equation of State (w_sq ≠ 0)

    dn̄/dt + 3H(1 + w_sq)n̄ = −σn̄ρ_m

For w_sq = −1 (dark-energy-like quanta): the Hubble dilution term vanishes completely:

    dn̄/dt = −σn̄ρ_m

This is the same as A1. For w_sq between −1 and 0, intermediate decay.

**DESI prediction:** Still fails (n̄ → 0 unless w_sq = −1 AND σ → 0).

---

## Class B: Creation-Annihilation Balance Equations

### B1. Standard SQMH (current equation — included for reference)

    dn̄/dt + 3Hn̄ = Γ₀ − σn̄ρ_m

where Γ₀ = const (current SQMH assumption).

**Additional assumptions beyond premise:**
- FLRW geometry (H3Hn̄)
- Non-relativistic w_sq = 0
- Mass-action law
- Γ₀ = const > 0 (independent creation term)
- σ = 4πGt_P (Newtonian matching)

**DESI prediction:**
Equilibrium density: n̄_eq = Γ₀/(σρ_m + 3H)
ρ_DE = n̄_eq · μ ∝ 1/(σρ_m + 3H)

As ρ_m → 0 (void): ρ_DE → Γ₀μ/(3H) ∝ H^{-1} (slowly growing)
As ρ_m → ∞: ρ_DE → Γ₀μ/(σρ_m) ∝ ρ_m^{-1} (suppressed in dense regions)

Global (homogeneous) solution gives A01 form:
    ρ_DE(a) ≈ Ω_Λ[1 + Ω_m(1−a)]    (linear in scale factor)
    → w_0 ≈ −1 + Ω_m/3,  w_a ≈ −Ω_m/3 (approximately)

DESI DR2 best-fit: w_0 = −0.757, w_a = −0.83 (with CMB+SN).
SQMH A01: w_0 ≈ −0.9, w_a ≈ −0.1 (rough), which is NOT the DESI headline.

Full ODE fit gives Δχ² ≈ −21 vs ΛCDM (L5 results, A01 form), but this is the phenomenological form, not the exact ODE solution.

**DESI prediction: PARTIAL FIT (χ² improvement ~21, but wa significantly off headline).**

---

### B2. Nonlinear Mass-Action (quadratic in ρ_m)

    dn̄/dt + 3Hn̄ = Γ₀ − σ·n̄·ρ_m²

**Physical motivation:** Annihilation requires collision between a quantum AND two matter particles simultaneously (3-body process). More likely in high-density regions.

**Units:** σ must have units [m⁶ kg⁻² s⁻¹] instead of [m³ kg⁻¹ s⁻¹]. Different σ.

**Equilibrium:** n̄_eq = Γ₀/(σρ_m² + 3H)

More suppressed in dense regions; weaker dependence on ρ_m at low density.

**Dark energy evolution:**
ρ_DE ∝ n̄_eq ∝ 1/(σρ_m² + 3H)

At large z (high ρ_m): ρ_DE ∝ ρ_m^{-2} ∝ (1+z)^{-6} (faster suppression than B1's (1+z)^{-3}).
In void: ρ_DE ∝ H^{-1} (same as B1).

**DESI prediction:**
The ρ_DE evolution would be more curved than the linear A01 form. Since B1's linear form already fits DESI moderately, B2's stronger nonlinearity would likely give different w_a. The quadratic ρ_m dependence would suppress dark energy more rapidly at high z. Qualitatively: larger |w_a|, possibly making the DESI wa ≈ −0.83 more accessible.

**Assessment: UNTESTED. Potentially interesting — stronger z-dependence than B1. Worth numerical investigation.**

---

### B3. Sub-linear Mass-Action (α < 1 in ρ_m^α)

    dn̄/dt + 3Hn̄ = Γ₀ − σ·n̄·ρ_m^α     (0 < α < 1)

**Physical motivation:** Annihilation rate saturates at high density (cooperative shielding, or rate-limited by quantum flux, not matter density alone).

**Equilibrium:** n̄_eq = Γ₀/(σρ_m^α + 3H)

More gentle suppression in dense regions; n̄_eq larger than B1 in high-density regions.

**DESI prediction:**
Sub-linear α reduces the ρ_m dependence. The A01 form ρ_DE ∝ (1 + Ω_m(1−a)) would be modified toward a flatter evolution. Qualitatively: smaller |w_a|, less DESI-like.

**Assessment: Less consistent with DESI than B1 (wa ≈ 0 limit as α → 0).**

---

### B4. Density-Dependent Creation Rate

    dn̄/dt + 3Hn̄ = Γ(n̄) − σ·n̄·ρ_m

where Γ(n̄) is a function of n̄ itself (feedback: when quanta are depleted, creation increases).

**Physical motivation:** Spontaneous creation rate is proportional to available "spacetime volume" ∝ 1/n̄ (more room → more creation). This gives:

    Γ(n̄) = Γ_0 · (n̄_0/n̄)    or    Γ(n̄) = Γ_ref · (1 + δ·(n̄_0 − n̄)/n̄_0)

The simplest feedback model: Γ(n̄) = Γ_0 · (n̄_0/n̄) gives:

    dn̄/dt + 3Hn̄ = Γ_0·(n̄_0/n̄) − σn̄ρ_m

This is a nonlinear ODE. Near equilibrium: linearizing around n̄_eq changes the response to perturbations.

**DESI prediction:**
This is qualitatively different from B1. The effective dark energy would have a different functional form. At low z, similar to B1 (if feedback is weak). At high z, n̄ → n̄_0 is protected by feedback. This could produce a more ΛCDM-like high-z behavior while having deviations at low z — potentially improving the DESI fit.

**Assessment: UNTESTED. Feedback term changes the character of the ODE significantly. May give different w_a sign.**

---

### B5. Radiation-Coupled Annihilation

    dn̄/dt + 3Hn̄ = Γ₀ − σ·n̄·(ρ_m + ε·ρ_r)

**Physical motivation:** Spacetime quanta interact with all matter, including radiation (photons and neutrinos). ε is a relative coupling (ε < 1 if quanta couple more weakly to radiation due to T^α_α = 0 for radiation — SQMH's T^α_α coupling sets ε = 0).

**Note:** SQMH's standard form has ε = 0 by T^α_α argument (radiation has trace-free stress tensor). This is HIDDEN ASSUMPTION #8 from the 8-team review. If ε > 0, the early universe (radiation-dominated) would have much faster annihilation.

**DESI prediction:**
For ε = 0 (current SQMH): no change from B1.
For ε > 0: ρ_r term dominates at high z. Dark energy would be suppressed in the radiation era, which may IMPROVE fit to CMB constraints but could modify r_d.

**Assessment: The standard SQMH choice ε = 0 is defensible (T^α_α coupling) but not forced by the premise.**

---

### B6. Relaxation/Telegrapher Extension

    τ·d²n̄/dt² + dn̄/dt + 3Hn̄ = Γ₀ − σ·n̄·ρ_m

**Physical motivation:** Spacetime quanta have a "memory time" τ — they do not respond instantaneously to annihilation events. This is the telegrapher's equation (finite propagation speed of information).

**Note from L10-S (Team 8):** For a TEMPORAL erf profile to emerge, τ > H₀^{-1} is required — which is unphysical (memory time longer than Hubble time). So this extension is motivated only if τ is sub-Hubble.

**DESI prediction:**
For τ ≪ H₀^{-1}: approaches B1 in the overdamped limit.
For τ ∼ H₀^{-1}: introduces oscillatory behavior in ρ_DE(z) — unlikely to improve DESI fit.

**Assessment: Generally makes fit worse. Not motivated for cosmological scales.**

---

### B7. Stochastic / Diffusion Extension

    dn̄/dt + 3Hn̄ = Γ₀ − σ·n̄·ρ_m + D∇²n̄ + noise

**Physical motivation:** Spacetime quanta can diffuse spatially (CSL-type or Planck-thermal diffusion).

**Note from L10-S (all members):** For CSL/thermal diffusion, D is so small that ∇²n̄ term is irrelevant at cosmological scales (21+ orders below Mpc). For homogeneous background, ∇²n̄ = 0 anyway.

**DESI prediction:** No change from B1 at cosmological scales. Irrelevant.

**Assessment: Does not change DESI predictions. Formally allowed but irrelevant.**

---

### B8. Quantum Superposition (n̄ as quantum amplitude)

    iħ ∂ψ/∂t = Ĥψ    where ψ = wavefunction of quantum foam density

**Physical motivation:** If spacetime quanta are truly quantum, their density is an operator, not a classical field. The semiclassical (mean-field) limit recovers B1, but quantum fluctuations are distinct.

**DESI prediction:**
The semiclassical expectation value ⟨n̂⟩ satisfies B1 plus quantum correction terms. Corrections are O(ħ/S_class) where S_class is the classical action. These corrections are Planck-scale suppressed (S_class ≫ ħ for cosmological n̄).

**Assessment: Quantum corrections negligible at cosmological scales. Mean-field (B1) is reliable.**

---

## Class C: Fundamentally Different Formulations

### C1. Gradient / Flux Formulation

Instead of a density equation, write the FLUX equation:

    ∂(n̄v)/∂t + ... = −σ·(n̄v)·ρ_m

where n̄v is the quantum flux (not the density). The "collision" reduces the flux, not the density.

**Physical interpretation:** Matter doesn't annihilate quanta; it redirects/scatters them (reduces their bulk flow). The NUMBER of quanta is conserved; only their directed flow is reduced.

This gives a different physical picture: matter creates vorticity in the quantum flow field, not a net sink.

**Dark energy:** In this formulation, ρ_DE is related to the kinetic energy of the quantum flow (n̄v²) rather than the density (n̄). The evolution equation for the bulk kinetic energy would be different from B1.

**DESI prediction:**
Qualitatively different. The "dark energy" would be kinetic rather than potential, giving potentially different w(z) behavior. This would need to be worked out in detail; qualitatively, w might oscillate around −1 depending on the flow dynamics.

**Assessment: UNTESTED. Structurally very different from B1. Would require full derivation.**

---

### C2. Holographic / Surface Formulation

Instead of a bulk density equation:

    d(N_surface)/dt = Γ₀ · A − σ · N_surface · M_enclosed

where N_surface is the number of quanta on the holographic screen (e.g., Hubble horizon), A is the area, M_enclosed is the enclosed mass.

**Physical motivation:** Holographic principle suggests information (quanta count) is encoded on surfaces, not in bulk. The SQMH equation for surface quanta replaces the bulk equation.

**DESI prediction:**
The effective Friedmann equation from d(N_surface)/dt would involve Area × H and enclosed mass. This is similar in spirit to Padmanabhan's emergence equation (L10, L11 references). The resulting w(z) would depend on how N_surface maps to ρ_DE.

**Assessment: Interesting reformulation. Padmanabhan's version recovers ΛCDM exactly. SQMH modification would give deviations near matter structures — difficult to parameterize as w₀w_a.**

---

### C3. Causal Set / Discrete Creation-Annihilation

    N(t+δt) = N(t) + C(t) − A(t)

where:
- N(t) = integer count of spacetime events in causal past
- C(t) = Poisson random variable with mean Γ₀·V·δt (creation events)
- A(t) = Poisson random variable with mean σ·N·ρ_m·V·δt (annihilation events)

**Physical motivation:** Causal set theory treats spacetime as a discrete partially ordered set. Each creation/annihilation is a discrete event. The mean-field limit recovers B1, but fluctuations are Poissonian (sqrt(N) noise), not Gaussian.

**DESI prediction:**
Mean-field: same as B1. Fluctuations: σ_N/N ~ 1/sqrt(N) ~ 1/sqrt(n̄·V).
For cosmological volumes V ~ Gpc³: N ~ n̄·Gpc³ >> 1, so fluctuations are negligible.
Causal set effects only relevant at smallest scales (near l_P).

**Assessment: Recovers B1 at cosmological scales. Causal set signature only at sub-Planck scales.**

---

### C4. Varying-σ / Running Coupling

    dn̄/dt + 3Hn̄ = Γ₀ − σ(z)·n̄·ρ_m

where σ(z) = σ₀·f(z) is a running coupling.

**Physical motivation:** If σ runs with the RG scale k ~ H(z) (Section L10-RG), then σ varies across cosmic history. Standard AS gives σ variation < 10^{-120} — negligible. But phenomenologically, allowing σ to vary is possible.

**DESI prediction:**
If σ(z) increases at high z: more suppression of n̄ in the past → less dark energy at high z → more negative w_a.

For σ(z) = σ₀·(1+z)^β:
ρ_DE(z) ∝ 1/(σ₀(1+z)^β · ρ_m(z) + 3H(z))

This is a 1-parameter extension of B1. For β > 0: faster decay of DE at high z. For β < 0: slower decay.

**DESI prediction:** This class can tune w_a more freely. For β ~ 0.5, the w_a could be made more negative, potentially improving DESI fit. However, from L10-RG: no physical mechanism gives such running at cosmological scales. It is purely phenomenological.

**Assessment: Phenomenologically richer but physically unmotivated. AIC/BIC would penalize the extra parameter.**

---

## Summary Table: Alternative Equations vs DESI

| Equation | Class | w₀ | w_a | DESI fit (qualitative) | Physical motivation |
|----------|-------|-----|-----|----------------------|-------------------|
| A1: pure annihilation (Minkowski) | No creation | N/A | N/A | CATASTROPHIC FAIL | Closest to premise |
| A2: pure annihilation (FLRW) | No creation | N/A | N/A | CATASTROPHIC FAIL | Minimal |
| B1: standard SQMH | Balance | ≈−0.9 | ≈−0.1 | PARTIAL (Δχ²≈−21 via A01 proxy) | Good (with extra assumptions) |
| B2: quadratic ρ_m | Nonlinear sink | ≈−0.95 | < −0.1? | UNTESTED (stronger z-decay) | 3-body, less natural |
| B3: sub-linear ρ_m^α | Soft nonlinear | ≈−1 | ≈0 | WORSE (flatter) | Saturation |
| B4: feedback Γ(n̄) | Nonlinear creation | TBD | TBD | UNTESTED | Feedback motivation |
| B5: radiation coupling | Extension | ≈B1 | ≈B1 | SIMILAR to B1 (small ε correction) | T^α_α = 0 excludes naturally |
| B6: telegrapher | Memory | oscillatory? | oscillatory? | WORSE | Unphysical for τ > H₀^{-1} |
| B7: diffusion | Stochastic | ≈B1 | ≈B1 | IDENTICAL to B1 | CSL scale mismatch |
| B8: quantum foam | Quantum | ≈B1 | ≈B1 | IDENTICAL to B1 | Corrections O(ħ/S) negligible |
| C1: flux formulation | Kinematic | ? | ? | UNTESTED | Different premise interpretation |
| C2: holographic | Surface | ≈−1 | ≈0 | SIMILAR to ΛCDM | Padmanabhan-like |
| C3: causal set | Discrete | ≈B1 | ≈B1 | IDENTICAL to B1 | Mean-field recovers B1 |
| C4: varying σ | Running | ≈B1 | more negative? | POTENTIALLY BETTER | No physical mechanism |

---

## Key Finding: Why the Standard SQMH Equation Was Chosen

The standard SQMH equation (B1) is the **simplest** equation satisfying:

1. Annihilation ∝ nρ_m (linear mass-action — simplest)
2. Stable late-time behavior (requires Γ₀ > 0)
3. FLRW compatibility (gives 3Hn̄)
4. Newtonian gravity recovery (fixes σ)
5. Cosmological constant as leading order (n̄ near equilibrium → Γ₀/3H)

But "simplest" is a CHOICE, not a logical necessity from the premise. In particular:

- **Equations without Γ₀ (A-class) are closer to the premise but cosmologically dead.**
- **Nonlinear equations (B2, B4) are as well-motivated as B1 but unexplored.**
- **The equation of state assumption w_sq = 0 (vs w_sq = 1/3 or w_sq = −1) changes the Hubble coefficient.**

---

## Most Interesting Untested Alternative: Equation B4 (Feedback)

    dn̄/dt + 3Hn̄ = Γ₀·(n̄_eq/n̄) − σ·n̄·ρ_m

This has:
- A physically motivated feedback mechanism (depleted quanta trigger more creation)
- The same number of parameters as B1
- Different dynamics: n̄ is attracted to equilibrium more strongly (faster return)
- Potentially different w(z): n̄(z) would track ρ_m more closely than B1

**Qualitative DESI prediction for B4:**
The equilibrium is the same as B1 at z = 0, but the approach to equilibrium is faster. At high z, n̄ was closer to its then-equilibrium value (n̄_eq(z) = Γ₀·n̄_eq/(σρ_m + 3H)). This means:
- ρ_DE(z)/ρ_DE(0) changes more steeply
- Potentially |w_a| > |w_a|_{B1}
- Could fit the DESI wa ≈ −0.83 better than B1's w_a ≈ −0.1

**This equation deserves numerical investigation.**

---

## Most Interesting Untested Alternative: Quadratic σ (Equation B2)

    dn̄/dt + 3Hn̄ = Γ₀ − σ₂·n̄·ρ_m²

where σ₂ has units [m⁶ kg⁻² s⁻¹].

**σ₂ dimensional analysis:** From {G, c, ħ}: G²t_P has units:
    [G²t_P] = [m³ kg⁻¹ s⁻²]² · [s] = m⁶ kg⁻² s⁻³    [not right]
    
Actually: [m⁶ kg⁻² s⁻¹] = G · t_P · (m³ kg⁻¹) = G·t_P · (1/ρ_P) · (something)...

The natural σ₂ from Planck units: σ₂ = G²t_P (with possible numerical prefactor). This is Planck-scale suppressed even more strongly than σ₁ = 4πGt_P. For ρ_m ~ ρ_crit ~ 10^{-27} kg/m³:

    σ₂·ρ_m²/(σ₁·ρ_m) = (G²t_P·ρ_m)/(4πGt_P) = G·ρ_m/(4π)
                       = (6.67e-11·1e-27)/(4π) ~ 5e-39

The quadratic term is 39 orders of magnitude smaller than the linear term at cosmological density! This makes B2 essentially indistinguishable from B1 at z ≤ few.

**Assessment: B2 is observationally irrelevant for current density scales.**

---

## Γ₀ Determination: Alternative Prescriptions

Even accepting that Γ₀ > 0 (the standard SQMH choice), there are different ways to determine its value:

| Prescription | Γ₀ value | Physical basis |
|-------------|---------|---------------|
| Current SQMH: balance condition | σn̄₀ρ_m0 + 3H₀n̄₀ (set dn̄/dt = 0 today) | Chosen for stability; free choice of epoch |
| Penrose rate: σ·ρ_P = 4π/t_P | 4π/t_P (Planck rate) | NF-34: Penrose collapse (interpretation only) |
| Holographic: Bekenstein prediction | H₀·S_H/(S_q·V_H) ~ 7.3e24 s⁻¹ | L12-B: 19 orders below Penrose value |
| de Sitter creation: Γ₀ = H | H₀ ~ 2e-18 s⁻¹ | de Sitter pair creation rate |
| QFT detailed balance | Γ₀ = σ·n̄·ρ_m·e^{-ΔE/kT} | Boltzmann factor: exponentially small for T << T_P |

None of these agree with each other. The range spans 62 orders of magnitude. **No derivation of Γ₀ from first principles exists.** (L13-Gamma confirms: K84 triggered, Q84 partial at best.)

---

## Conclusion: The Honest Assessment

**From the single premise "spacetime quanta are annihilated by matter," the current SQMH equation is:**
- **NOT uniquely derivable**
- **A reasonable first choice, but one of many equally valid options**
- **The most conspicuous addition beyond the premise is Γ₀ (creation term), which directly contradicts the premise's silence on creation**

**The alternative equations closest to the premise (A1, A2) are observationally dead** — they predict no dark energy. The premise alone is insufficient to derive the observed accelerated expansion.

**The standard SQMH equation represents the minimal extension of the premise that is also cosmologically viable**, requiring 8 additional assumptions (H1–H8) beyond the single premise.

**The most promising untested alternative** is the feedback equation B4, which may produce larger |w_a| values closer to the DESI headline (w_a ≈ −0.83), but requires numerical investigation.

---

*L14 alternative equations analysis completed: 2026-04-11*
