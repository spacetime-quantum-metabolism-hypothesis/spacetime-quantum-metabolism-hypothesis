# L134 — Standardized notation & conventions for SQT paper

논문 제출용 표준 표기 정착. 학계 conventions 준수.

---

## Field content

| Symbol | Meaning | Units (SI) | Natural units (ℏ=c=1) |
|--------|---------|------------|---------------------|
| n(x,t) | Quantum number density | m⁻³ | E³ |
| ρ_m(x,t) | Matter mass density | kg·m⁻³ | E⁴ |
| ε | Per-quantum energy | J | E |
| τ_q | Quantum lifetime | s | E⁻¹ |
| σ_0 | Quantum-matter coupling | m³·kg⁻¹·s⁻¹ | E⁻³ (× E²) |
| Γ_0 | Cosmic creation rate | m⁻³·s⁻¹ | E⁴ |
| H | Hubble rate | s⁻¹ | E |
| Λ_eff | Effective cosmological constant | s⁻² | E² |

---

## Index conventions

- Greek indices μ, ν, ρ, σ run 0, 1, 2, 3 (spacetime)
- Latin indices i, j, k run 1, 2, 3 (spatial only)
- Metric signature: (-,+,+,+) (mostly-plus)
- Einstein summation convention
- ; for covariant derivative, , for partial

---

## Action principle (Schwinger-Keldysh)

```
S_SK[n_+, n_-] = ∫_C d⁴x √(-g) · L_SK
```

with closed time path C: -∞ → +∞ → -∞.

```
L_SK = (1/2)·g^μν·(∂_μ n_+·∂_ν n_+ - ∂_μ n_-·∂_ν n_-)
       - V(n_+) + V(n_-)
       + n_+·J_+ - n_-·J_-
       + (matter coupling)
```

where J_± are matter sources, V(n) is the n field potential.

---

## Equations of motion

**Quantum density continuity** (Branch B regime r):
```
∂_t n + 3H·n = Γ_0 - σ_0(r)·n·ρ_m
```

**Matter conservation** (with absorption):
```
∂_t ρ_m + 3H·ρ_m = +σ_0(r)·n·ρ_m·ε/c²
```

**Modified Friedmann**:
```
H² = (8π·G/3)·(ρ_m + n·ε/c²) + Λ_eff/3
```

---

## Branch B regime definitions

```
cosmic regime:    ρ_m < 1×10⁻²⁶ kg/m³,    σ_0 = 10^8.37 m³/(kg·s)
cluster regime:   1×10⁻²⁶ < ρ_m < 1×10⁻²² kg/m³,  σ_0 = 10^7.75
galactic regime:  ρ_m > 1×10⁻²² kg/m³,    σ_0 = 10^9.56
```

Smooth transition (Π width 0.3 dex):
```
σ_0_eff(ρ) = σ_cosmic·s₀(ρ) + σ_cluster·s₁(ρ)·(1-s₀(ρ)) + σ_galactic·s₂(ρ)
```
where s_i are tanh-based smooth step functions.

---

## Key derived relations

```
D1: G = σ_0(env)/(4π·τ_q(env))             [Newton constant]
D2: n_∞ = Γ_0·τ_q                          [steady-state density]
D3: ε = ℏ/τ_q   (scenario Y)               [Heisenberg]
D4: ρ_Λ = n_∞·ε/c²                         [DE from quanta]
D5: a_0 = c·H_0/(2π) [from D4 + 1/(2π) disc geometry]  [Milgrom]
```

---

## Self-consistency check

For consistent Branch B, must satisfy:
```
G = σ_galactic/(4π·τ_q_galactic)
G = σ_cosmic /(4π·τ_q_cosmic)
G = σ_cluster /(4π·τ_q_cluster)
```

This implies regime-local τ_q(env) = σ_0(env)/(4πG) (L92 derivation).

---

## Predictive notation

For new predictions:
```
P_i: SQT-unique prediction, indexed
G2: Geometric prediction (revised L115): a_0(disc)/a_0(spheroid) = 2
P7: a_0(z) = c·H(z)/(2π)
P13: a_0(void) = a_0_cosmic·(σ_cosmic/σ_galactic) ≈ 0.07·a_0_normal
```

---

## Falsifiers

```
F_DESI: w_a < -0.5 robustly → SQT requires τ_q(t) extension
F_MICROSCOPE: η_EP > 1e-17 → P3 depletion zone signature
F_SKA: a_0(z=2)/a_0(0) < 1.5 or > 5 → P7 violation
F_ATLAS: a_0(disc)/a_0(spheroid) within 1% of 1 → G2 violation
```

---

## References to existing literature

- Schwinger 1961 (closed-time-path)
- Keldysh 1965 (real-time formalism)
- Milgrom 1983 (MOND, a_0)
- Lelli+ 2016 (SPARC catalog)
- DESI 2024 (DR2 BAO)
- Sola+ 2024 (RVM precedent)
- Verlinde 2017 (entropic gravity)

---

이 표기를 paper 전체에 일관되게 사용. PRD/JCAP convention 준수.
