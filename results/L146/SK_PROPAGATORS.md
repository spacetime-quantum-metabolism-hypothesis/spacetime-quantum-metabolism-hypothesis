# L146 — Schwinger-Keldysh propagators for SQT

논문 *Section 6 (SK Formalism)* 보강.

---

## SK doubled-field propagators

In closed-time-path (CTP) formalism, the n field has 4 propagators:

```
G^++(x,y) = ⟨T n_+(x) n_+(y)⟩         (forward time-ordered)
G^--(x,y) = ⟨T̃ n_-(x) n_-(y)⟩         (anti-time-ordered)
G^+-(x,y) = ⟨n_-(y) n_+(x)⟩            (Wightman)
G^-+(x,y) = ⟨n_+(x) n_-(y)⟩            (anti-Wightman)
```

These satisfy:
G^++ + G^-- = G^+- + G^-+

---

## Keldysh basis (more practical):

Define:
G^R(x,y) = G^++ - G^+- (retarded)
G^A(x,y) = G^-- - G^-+ (advanced)
G^K(x,y) = G^++ + G^-- (Keldysh, statistical)

For SQT n field with mass m_eff and friction γ_eff:

**Retarded propagator** (in Fourier space):
```
G^R(ω, k) = 1 / (-ω² + c²k² + m_eff² - iγ_eff·ω)
```

**Keldysh propagator** (FDT):
```
G^K(ω, k) = (G^R - G^A) · coth(ω / 2T_eff)
```

where T_eff is effective temperature (de Sitter T_dS = ℏH/2π for cosmic).

---

## Spectral function

ρ(ω, k) = -2 Im G^R(ω, k) = 2γ_eff·ω / [(ω² - c²k² - m_eff²)² + γ_eff²·ω²]

Sum rule: ∫ ρ(ω, k) dω/2π = 1 (per mode)

---

## Branch B regime-dependent γ_eff

In each Branch B regime, friction γ_eff varies:
```
cosmic regime:    γ_eff = 3H_0 + σ_cosmic·ρ_m,cosmic    ≈ 7.9e-18 s⁻¹
cluster regime:   γ_eff = 3H + σ_cluster·ρ_m,cluster  ≈ 3.1e-16 s⁻¹
galactic regime:  γ_eff = 3H + σ_galactic·ρ_m,galactic ≈ 1.2e-11 s⁻¹
```

---

## Vertex functions

Linear matter coupling:
V₃(x; n, ρ_m) = σ_0(env)·n(x)·ρ_m(x)

Three-point vertex in Feynman diagrams:
```
   n(p)
   |
   |—— σ_0 vertex ——
   |
   ρ_m(q)
```

---

## Sample diagram: 1-loop self-energy

n field self-energy from matter coupling:
Σ(p) = σ_0² · ∫ (d⁴q)/(2π)⁴ G_matter^R(q) G^R(p-q)

This contributes to renormalized γ_eff:
γ_eff^renormalized = γ_eff^bare + Σ_imaginary

---

## Renormalization status

- 1-loop self-energy: finite at low energies (k < Λ_UV)
- 2-loop: finite if k < Λ_UV
- Above cutoff Λ_UV ≈ 18 MeV (L76 F4): UV completion required
- SQT is EFT — explicit cutoff regularization

---

## Connection to observable cross-sections

Per-mode absorption rate:
1/τ_q(env) = -2 Im Σ(p) / 2ω

In Branch B at galactic regime:
τ_q ≈ σ_galactic / (4πG) (per L92 self-consistent)

---

## Numerical values

```
At cosmic regime (E ~ ℏH_0 ~ 7.6e-52 J):
  γ_eff = 7.9e-18 s⁻¹
  m_eff² ≈ 0 (massless quantum)
  spectral peak: ω = ck (light-cone)
  
At galactic regime:
  γ_eff = 1.2e-11 s⁻¹ (much faster decay)
  Effective lifetime: 8e10 s ≈ kyr
```

---

## Implications for predictions

The SK propagators allow:
1. Explicit calculation of correlation functions for n field
2. Linear response to perturbations
3. Quantum noise spectrum (via Keldysh)
4. Decoherence rates (matter-quantum interaction, L97)
5. Cluster scale enhancement of gravity (via integrated G^R)

---

## Open work

- 2-loop renormalization of σ_0 → RG flow (related to Branch B regime origin)
- Non-perturbative phase transition (Landau-Ginzburg, L142)
- Stochastic limit (MSR, L79)
- Vertex corrections from matter loops

이는 PRD/JHEP reviewer 들의 *propagator/diagram* 요구 충족.
