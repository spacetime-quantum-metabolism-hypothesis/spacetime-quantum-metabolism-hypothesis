# R5 Quantum verification audit (cold-blooded)

**Scope.** Verify root `/base.md` §14.5 *quantum interface 3 claims* (marked
"검증 ✅") under the **paper/base.md** framework only (4 foundations:
Schwinger–Keldysh, Wetterich RG, Holographic bound, Z₂ SSB; no GFT, no BEC).

Script: `paper/verification_audit/R5_quantum.py`
Result: `paper/verification_audit/R5_quantum_result.json`

---

## Claim Q1 — Q-parameter (quantum–classical transition, "0 extra parameters")

### What paper/base.md actually provides
paper/base.md does **not** state a closed-form definition of `Q`. It exposes
only the structural quantities

```
σ₀ = 4πG·t_P            (holographic foundation)
τ_q ≡ 1/(3H₀)           (cosmic Γ₀ timescale)
n_∞ = ρ_Λ c²/ε ,  ε = ℏ/τ_q
```

Any `Q(m, Δx, ρ_local, …)` is a **modeller's choice** of what
"Γ_dec / Γ_dyn" means — paper/base.md never fixes this ratio.

### Numerical scan over 5 dimensionally consistent definitions

| Def | Formula                                                 | Q_macro (1 kg, 1 mm) | Q_micro (e⁻, 1 Å) | macro≫1 & micro≪1 |
|-----|---------------------------------------------------------|----------------------|-------------------|--------------------|
| A   | `σ₀ n_∞ ρ Δx² / (m c²)`                                | 4.1e-31              | 4.5e-48           | **fail**           |
| B   | `(m Δx²/ℏ) · (σ₀ n_∞ ρ)`                               | 3.5e+20              | 3.2e-57           | **pass**           |
| C   | `(σ₀ n_∞) · (m Δx²/ℏ)`  (ambient only)                 | 3.5e+17              | 3.2e-27           | **pass**           |
| D   | `σ₀ n_∞ (m/m_P)² c²/ℏ  ÷  c/Δx`                        | 2.2e+44              | 1.9e-23           | **pass**           |
| E   | `τ_q · m c² / ℏ`  (cosmic vs Compton)                  | 1.2e+68              | 1.1e+38           | **fail (micro≫1)** |

### Cold-blooded verdict
Three distinct definitions reproduce the macro/micro split (B, C, D), and
they disagree by **38 orders of magnitude** in `Q_macro`. The "0 extra
parameter" claim only holds **after** a definition is chosen, but the
choice itself is a hidden theoretical degree of freedom. paper/base.md
never selects one.

**Status: PASS (any-of), but with caveat** — at least one definition
recovers the expected sign asymptotics structurally from the four
paper/base.md foundations. The transition mass scale and threshold are
**not predicted**; they slide with the definition. "Predicts the
quantum–classical transition with 0 free parameters" is **overclaim**;
"is consistent with a structural macro/micro split" is fair.

---

## Claim Q2 — Wavefunction "real + probability" duality

paper/base.md is built on standard Schwinger–Keldysh QFT for a real scalar
`n` with a Z₂ SSB vacuum. The ψ ↔ δn/n₀ identification is a **rephrasing**
of canonical quantization around the SSB vacuum:
- "real" piece = density fluctuation δn (operator-valued field)
- "probability" piece = standard Born rule on the SK contour

No new prediction, no quantitative deviation from textbook QFT.

**Status: PASS by inheritance** (standard QFT). Adds zero falsifiable
content beyond canonical QFT — should be presented as *interpretive*, not
*derivational*, in the paper.

---

## Claim Q3 — BEC coherence → nonlocality

paper/base.md foundations contain:
- SK open-system formulation
- Wetterich RG
- Holographic bound
- **Z₂ SSB** (discrete vacuum manifold {+v, −v}, no continuous U(1) phase)

Bose–Einstein condensation is **not** among them. The root `/base.md`
narrative ("BEC 위상 코히런스 → 벨 위반의 물리적 기반") relies explicitly
on **GFT BEC condensation** `⟨φ̂⟩ = σ₀ ≠ 0` from root §6.4–6.5, which is
**dropped** in paper/base.md. Z₂ has no global phase, hence no macroscopic
coherent phase that could underpin Bell correlations.

**Status: NOT_INHERITED.** The mechanism does not exist inside the
paper/base.md framework. Either:
(i) drop Q3 from paper/base.md §14.5 (honesty), or
(ii) re-promote the GFT/BEC layer to a 5th foundation and re-derive its
phenomenology — this is a non-trivial additional commitment.

---

## Summary table

| Claim | Verdict             | Notes                                                      |
|-------|---------------------|------------------------------------------------------------|
| Q1    | PASS (caveat)       | Definition is non-unique; "0 free params" overstated.       |
| Q2    | PASS_BY_INHERITANCE | Standard QFT rephrasing; no new content.                    |
| Q3    | NOT_INHERITED       | BEC absent in paper/base.md; Z₂ has no continuous phase.    |

## Honest one-line

> paper/base.md §14.5 의 *양자 접점 ✅ 3개* 중 Q1 은 정의 선택이 자유로워 "추가 매개변수 0" 주장이 과장이고, Q2 는 standard QFT 재서술이며, Q3 는 BEC 구조가 paper/base.md 에 부재하여 inherit 되지 않으므로 — 정직하게 "1.5/3" (Q1 caveat + Q2 inherit) 이며 Q3 는 paper/base.md 에서 삭제 또는 5번째 foundation 추가가 필요하다.
