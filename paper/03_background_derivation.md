# 3. Background Derivation and Candidate Effective Field Realisations

We construct the Friedmann background for each candidate effective field
realisation of SQMH.  The goal of this section is to trade the abstract
continuity equation (2.2) for concrete ODE systems that can be integrated
and confronted with BAO+SN+CMB+RSD.

## 3.1 Newtonian matching

See base.md §3.2.  Expanding Eq. (2.1) around a point mass M in the
static limit with ρ_m(x) = M δ³(x), the induced inflow velocity field
satisfies ∇·v = −σ n₀ ρ_m on matter and ∇·v = σ n₀ ρ_{m,0} + 3 H₀ in
vacuum (after removing the cosmological mean).  The resulting
gravitational potential is

```
Φ(r) = −G M / r,    G = σ² n₀ μ / (4 π),
```

which pins σ = 4πG t_P.

## 3.2 FLRW ansatz

Working in e-folds N = ln a, Eq. (2.2) becomes

```
n′ + 3 n = Γ₀ / H − (σ ρ_m / H) n,    (3.1)
```

where prime denotes d/dN.  Coupling to the Einstein equations via the
trace of Eq. (2.1) and the identification of ρ_DE with the net generation
produces an effective continuity equation for ρ_DE(a).  The specific
form of this equation depends on the chosen effective field realisation.

## 3.3 Candidate families

### 3.3.1 C27 Deser-Woodard non-local

S ⊃ (1/2) R f(□⁻¹ R) with f(X) = c₀ tanh((X − X_s)/ΔX).  Localisation
(Koivisto PRD 77 123513 2008) introduces auxiliary pair (U, V):

```
□U = R,    □V = R f′(U),
```

so the Friedmann equation becomes

```
6 H² = 8πG ρ + 6 H² (f(U) + f′(U) V) − 3 U̇ V̇ − ...    (3.2)
```

Explicit form is in Dirian-Foffa-Kehagias-Rio-Maggiore 2015 Eqs
(2.5–2.8).  We integrate (U, U̇, V, V̇) from a_ini = 10⁻⁴ to a = 1.
Free parameters (c₀, X_shift, ΔX).

### 3.3.2 C28 Maggiore-Mancarella RR non-local

S ⊃ (m²/6) R □⁻² R.  Localisation pair (U, S) with □U = R, □S = −U.
Friedmann equation: Dirian 2015 full RR branch.  The RR mass m is the
free parameter.  Structurally distinct from C27 (different auxiliary
pair) and so produces a distinct posterior.

### 3.3.3 C33 f(Q) teleparallel

Symmetric teleparallel gravity with f(Q) = Q + f₁ H₀² (Q/(6H₀²))ⁿ,
n ≥ 1 (Frusciante 2021, arXiv:2103.11823).  In FLRW Q = 6H², so the
Friedmann equation is

```
6 H² f_Q + f(Q) − 2 Q f_QQ H² = 8πG (ρ_m + ρ_r),   (3.3)
```

which we solve self-consistently at each a for H(a).  Free parameters
(f₁, n).  L2 numerical verification established f₁ > 0 ⇒ w_a < 0.

### 3.3.4 C41 Wetterich fluid IDE

Coupled continuity with energy flow Q = H β ρ_DE from DE to matter:

```
ρ_m′ = −3 ρ_m + 3 β ρ_DE,    ρ_DE′ = −3 β ρ_DE.
```

Analytic background: ρ_DE(a) = ρ_{DE,0} a⁻³ᵝ,  ρ_m(a) = A a⁻³ +
B a⁻³ᵝ with A = ρ_{m,0} − β/(1−β) ρ_{DE,0},  B = β/(1−β) ρ_{DE,0}
(valid for β < 1).  Free parameter β ∈ [0, 0.1] (linear regime).

### 3.3.5 C26 Perez-Sudarsky unimodular diffusion

J⁰ = α_Q ρ_c0 (H/H₀).  Continuity equations in e-folds:

```
ρ_m′ = −3 ρ_m + J⁰,    ρ_Λ′ = −J⁰.
```

Most direct SQMH L0/L1 realisation: J⁰ > 0 is literally the metabolism
drift.  Free parameter α_Q > 0.

### 3.3.6 C23 Asymptotic Safety effective RVM

RG identification k = ξH (ξ = O(1)) gives effective Λ(H²) = Λ₀ +
ν_eff (H² − H₀²).  Closed form Friedmann identical to RVM (below).
Unitarity bound |ν_eff| < 0.03.

### 3.3.7 C5r, C6s Running Vacuum Model

Λ(H²) = Λ₀ + 3ν H².  Closed form (Gómez-Valent-Solà 2024):

```
E²(a) = [Ω_m a⁻³⁽¹⁻ⁿ⁾ + Ω_r a⁻⁴⁽¹⁻ⁿ⁾ + (1 − Ω_m − Ω_r − ν)] / (1 − ν).
```

ν < 0 branch reproduces w_a < 0.  C6s (stringy RVM + Chern-Simons) has
identical background to C5r (Pontryagin vanishes for FLRW = Type D
metric).

### 3.3.8 C11D Disformal IDE

Pure disformal coupling g̃_μν = g_μν + B(φ) ∂_μφ ∂_νφ
(Zumalacárregui-Koivisto-Bellini 2013).  For A′ = 0 (pure disformal),
static γ = 1 exact.  Free parameter γ_D.

### 3.3.9 C10k Dark-only coupled quintessence

Amendola 2000 dark-only: Q = β_d ρ_c φ̇.  Background gives effective
w_eff = −1 + (2/3) β_d² — constant, so w_a = 0 at the background level.
L4 re-assessment is on the **growth channel**: the effective Newton
constant on DM is G_eff / G = 1 + 2 β_d².  Free parameter β_d.

## 3.4 Initial conditions

All backgrounds are matched to the ΛCDM matter-dominated era at
a_ini = 10⁻⁴ with initial auxiliary fields set to zero (for non-local)
or (A, B) chosen to satisfy the present-day Ω_m constraint (for IDE
analytic forms).

## 3.5 Numerical integration

Backgrounds are integrated with scipy.integrate.solve_ivp (RK45, rtol
10⁻⁷) in e-folds.  Closed-form cases (RVM family) are evaluated
directly.  Self-consistent solves (f(Q)) use scipy.optimize.brentq at
each requested redshift.

Full code is in `simulations/l4/<ID>/background.py` for each candidate.
