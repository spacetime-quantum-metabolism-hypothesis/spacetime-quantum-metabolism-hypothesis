# refs/l14_equation_derivation_8teams.md -- L14: 8-Team Independent Derivation Review

> Date: 2026-04-11
> Task: 8 independent teams, each starting only from the single premise:
>   "시공간 양자가 물질과 충돌하면 소멸한다."
>   ("Spacetime quanta are annihilated upon collision with matter.")
> No other shared assumptions. Each team may adopt any physical framework.

---

## The Premise

**Single shared premise (only):**
> "Spacetime quanta collide with matter and are annihilated."

Nothing else is shared. The following questions are investigated independently:
1. Does this premise uniquely force the form dn̄/dt + 3Hn̄ = Γ₀ − σn̄ρ_m?
2. What is added beyond the premise (hidden assumptions)?
3. Are alternative equations equally valid from this premise?
4. Where does σ = 4πGt_P come from?
5. Why is Γ₀ (creation term) present if the premise mentions only annihilation?

---

## Team 1: Kinetic Theory / Boltzmann Approach

**Framework:** Classical kinetic theory. Spacetime quanta treated as a dilute gas with a distribution function f(x, p, t). Matter particles are treated as a fixed background density field.

### Derivation

Starting from the Boltzmann equation for spacetime quanta:

    ∂f/∂t + v · ∇f = C[f]

where C[f] is the collision integral. The premise says: when a spacetime quantum hits matter, it is annihilated. This is a sink term. The collision integral for annihilation:

    C[f]_annihilation = -f · (cross-section) · (relative velocity) · ρ_m/m_matter

Integrating over momentum space to get the number density n = ∫f d³p:

    ∂n/∂t + ∇·(nv_avg) = -σ_eff · n · ρ_m

where σ_eff = σ has units [m³ kg⁻¹ s⁻¹] from integrating the cross-section × relative velocity / mass over momentum distribution.

In FLRW background, the ∇·(nv_avg) term for a homogeneous n becomes the Hubble dilution term +3Hn (with H > 0 for expansion). Wait — this sign: the volume element grows as a³, so ∂(na³)/∂t = source terms:

    dn/dt + 3Hn = C_source - σ · n · ρ_m

**The 3Hn term arises from FLRW volume expansion — this is NOT in the premise.** The premise is silent on whether we are in an expanding universe. Adopting FLRW is an additional assumption.

### What Team 1 finds about the creation term Γ₀

The Boltzmann equation must have: (rate of creation) - (rate of annihilation). The premise specifies annihilation only. A Boltzmann treatment with only sinks gives:

    dn/dt + 3Hn = -σnρ_m

This has no Γ₀. The system evolves to n = 0 at late times (all quanta annihilated). This contradicts a stable cosmology.

**Conclusion from Team 1:**

The premise alone, plus kinetic theory plus FLRW, gives:

    **dn/dt + 3Hn = -σnρ_m (no Γ₀)**

Γ₀ is NOT derivable from the premise. It requires an independent assumption: "there is also spontaneous creation of spacetime quanta." The premise says nothing about this.

The CURRENT SQMH equation adds Γ₀ as an ad hoc balance condition. This is a HIDDEN ASSUMPTION (#1).

---

## Team 2: Fluid Mechanics / Continuity Equation Approach

**Framework:** Treat spacetime quanta as a compressible fluid with number density n(x,t) and velocity field v(x,t). Matter is a sink.

### Derivation

The continuity equation for any conserved fluid is:

    ∂n/∂t + ∇·(nv) = 0

But quanta are NOT conserved — they are annihilated by matter. So:

    ∂n/∂t + ∇·(nv) = R_source - R_sink

From the premise: R_sink = rate of annihilation per unit volume. If each quantum has rate proportional to local matter density:

    R_sink = α · n · ρ_m

where α is a coupling coefficient with units [m³ kg⁻¹ s⁻¹] — this is the σ in SQMH.

The premise gives: R_source = 0 (nothing mentioned about creation).

So the fluid equation from the premise alone:

    **∂n/∂t + ∇·(nv) = -σ · n · ρ_m**

In FLRW for homogeneous n̄:

    **dn̄/dt + 3Hn̄ = -σ · n̄ · ρ_m**

### What is the velocity field v?

The premise says quanta are annihilated near matter. This implies a net flow toward matter (like a fluid being absorbed by a sponge). In the absence of other forces, the flow field is determined by:

    ∇·v = -σ · ρ_m / n · (something) — not uniquely determined by the premise.

Team 2 notes: **the velocity field v is completely undetermined by the premise.** The Newtonian gravity derivation requires v(r) = σM/(4πr²), which requires specific boundary conditions and a mass action law — not just the premise.

### Additional assumption found

If we write v(r) for a point mass M at origin:

    4πr²·n·v(r) = σ·n·M (continuity for steady state)
    → v(r) = σM/(4πr²)

The match v(r) = g(r)·t_P = (GM/r²)·t_P requires:

    σM/(4πr²) = (GM/r²)·t_P
    → σ = 4πG·t_P

**But this matching is circular**: σ is defined by matching to Newtonian gravity, and then Newtonian gravity is "derived" from σ. The system is self-consistent but not independently predicted. **This is HIDDEN ASSUMPTION #2**: σ = 4πGt_P comes from matching to empirically known G, not from the premise.

**Conclusion from Team 2:**

The premise gives dn̄/dt + 3Hn̄ = -σn̄ρ_m (with FLRW as additional assumption). No Γ₀. σ is undetermined — it requires a separate matching condition.

---

## Team 3: Quantum Field Theory / Decay Rate Approach

**Framework:** Model spacetime quanta as a bosonic quantum field φ_sq, and matter as a fermionic field ψ. The premise is: φ_sq ψ → ψ (spacetime quantum absorbed by matter). This is an annihilation vertex.

### Lagrangian

The simplest Lagrangian for this process:

    L = (∂_μφ_sq)² - m²φ_sq² + ψ̄(i∂̸ - M)ψ + g · φ_sq · ψ̄ψ

The interaction term g·φ_sq·ψ̄ψ gives a 3-point vertex where one φ_sq is absorbed.

### Decay rate

The spontaneous decay rate of φ_sq into standard model particles via this vertex:

    Γ_decay ~ g² · m²_sq / (16π · m_matter)   [tree level]

The number density equation:

    dn_sq/dt = -Γ_decay · n_sq - (stimulated annihilation)

Wait — this gives exponential decay of n_sq without any density-of-matter dependence unless the interaction is stimulated (proportional to n_matter):

    dn_sq/dt = -Γ_stimulated · n_sq · n_matter

where n_matter ~ ρ_m/m_matter. So:

    dn_sq/dt = -(Γ_stimulated · m_matter⁻¹) · n_sq · ρ_m = -σ · n_sq · ρ_m

This IS the SQMH form! σ = Γ_stimulated/m_matter has the right units.

### What about Γ₀ (spontaneous creation)?

In QFT, if we have an annihilation vertex, we ALSO must have (by crossing symmetry and unitarity): a CREATION vertex where φ_sq is emitted. The reverse process: ψ → ψ + φ_sq.

This spontaneous emission rate:

    Γ_emission ~ g² · m_sq / (8π)    [by detailed balance with decay]

If m_sq is the spacetime quantum mass (interpreted as Planck mass), this gives:

    Γ_emission = n_0 · Γ_0    [some spontaneous creation per unit time per volume]

**Conclusion from Team 3:**

QFT crossing symmetry DOES suggest that if there is annihilation, there is also spontaneous creation. So Γ₀ is NOT entirely ad hoc if we take the QFT framework seriously. However:

1. Crossing symmetry requires the same interaction vertex for creation and destruction — the creation rate depends on the same coupling g, not independently set.
2. The specific value of Γ₀ is not determined by the premise; it depends on g and m_sq.
3. **HIDDEN ASSUMPTION #3**: The creation rate Γ₀ is set equal to the equilibrium value (Γ₀ = σn̄₀ρ_m0 + 3H₀n̄₀) to ensure a stable cosmology. This is an additional condition beyond the premise AND beyond QFT crossing symmetry.

σ = 4πGt_P is not derivable from QFT alone. It requires matching to known G — an empirical input, not a derivation.

---

## Team 4: Thermodynamic / Statistical Mechanics Approach

**Framework:** Treat the population of spacetime quanta as a grand canonical ensemble. Matter provides chemical potential sinks.

### Master equation

For the probability P(n,t) of having n spacetime quanta in volume V:

    dP(n)/dt = λ(n-1)P(n-1) + μ_eff(n+1)P(n+1) - [λ(n) + μ_eff(n)]P(n)

where:
- λ = creation rate per quantum (if any)  
- μ_eff(n) = n · (annihilation rate per quantum)

The premise gives: annihilation rate per quantum = σ · ρ_m (proportional to matter density). So:

    μ_eff(n) = n · σ · ρ_m

If λ = 0 (NO creation, as premise suggests), the birth-death process is a PURE DEATH process. The mean n̄ satisfies:

    dn̄/dt = λ·n̄ - μ_eff = -σ · ρ_m · n̄ (no creation)

Adding FLRW dilution: dn̄/dt + 3Hn̄ = -σn̄ρ_m.

### What if we want a stationary state?

For n̄_eq > 0, we NEED λ > 0 (creation term). The premise does not provide this. For a stationary cosmology:

    dn̄/dt = 0 → λ = σ · ρ_m + 3H

This is precisely Γ₀ = n̄_eq · (σρ_m + 3H) — but this is a CHOICE of Γ₀ to ensure stability, not a derivation from the premise.

### Thermodynamic uniqueness question

Is the 2-body interaction form σ·n·ρ_m the only possible annihilation rate?

NOT necessarily. In statistical mechanics, the annihilation rate could be:
- 1-body: α·n (if quantum spontaneously decays regardless of matter)
- 2-body: σ·n·ρ_m (as in SQMH — requires encounter with matter)
- 2-body nonlinear: σ·n²·ρ_m (if two quanta are needed)
- 3-body: σ₃·n·ρ_m² (if two matter particles cooperate)

The premise "collides with matter" favors 2-body (one quantum + one matter particle). But the mass-action law σ·n·ρ_m specifically assumes:
(a) Reactions scale linearly in n (rare quantum, dilute gas limit)
(b) Reactions scale linearly in ρ_m (dilute matter, or many independent targets)
(c) The rate is proportional to encounters (well-mixed system)

**HIDDEN ASSUMPTION #4**: The mass-action law for annihilation rate. The premise does not specify whether it should be σnρ_m, σn²ρ_m, σnρ_m^(1/2), etc.

**Conclusion from Team 4:**

Thermodynamic analysis: premise → dn̄/dt + 3Hn̄ = -σn̄ρ_m. Γ₀ is forced only by choosing to have a stationary solution. σ value is not determined. Mass-action law is an additional assumption.

---

## Team 5: Information Theory / Entropy Production Approach

**Framework:** Treat spacetime quanta as information carriers (bits). Annihilation = information destruction. Apply the second law of thermodynamics and entropy constraints.

### Premise reframing

"Spacetime quanta are annihilated by matter" = matter processes (erases) information in spacetime.

By Landauer's principle: erasing one bit of information costs at least k_B·T·ln(2) of energy. This implies:

    Energy extracted from spacetime per unit time = σ · n · ρ_m · E_per_quantum

This energy must go somewhere. If it goes into matter thermal energy: no net cosmological effect. But if it goes into gravitational potential energy (the SQMH gravity mechanism), then we need to track the energy-momentum tensor.

### Does information theory constrain σ?

From Bekenstein bound on information content of spacetime quanta:

    S_max = 2πk_B · R · E / (ħc)    per quantum

The information destruction rate must not exceed:

    Γ_max = c / (4G · m_P)    [Planck rate for BH formation]

Numerically: Γ_max = c³/(4Gm_P·m_P) ... dimensional analysis gives σ ~ G·t_P.

This gives a MOTIVATION for the form σ = 4πGt_P but not the precise numerical prefactor.

**HIDDEN ASSUMPTION #5**: The 4π prefactor in σ = 4πGt_P is geometric (solid angle of sphere). This is assumed, not derived from information theory.

### Landauer and Γ₀

By Landauer's principle applied in reverse: if information is being erased (annihilation), a complementary process of "information writing" (creation) must occur somewhere to maintain total information budget in a reversible universe. This is a thermodynamic motivation for Γ₀ > 0.

However, this requires: (i) time-reversal symmetry of the underlying process, (ii) the universe conserves total information. Neither is guaranteed by the premise.

**Conclusion from Team 5:**

Information theory provides motivation for σ ~ G·t_P (order of magnitude) and motivation for Γ₀ > 0 (Landauer-type argument), but:
- The exact σ = 4πGt_P requires empirical matching
- The specific value of Γ₀ is not constrained by information theory
- The equation form dn̄/dt + 3Hn̄ = Γ₀ - σn̄ρ_m is reasonable but not unique

Alternative: dn̄/dt + 3Hn̄ = Γ(n̄) - σn̄ρ_m where Γ depends on the current quantum density (feedback mechanism). SQMH's constant Γ₀ is a special case.

---

## Team 6: General Relativity / Energy-Momentum Conservation Approach

**Framework:** Work from the Bianchi identity ∇_μT^{μν} = 0. If spacetime quanta carry energy-momentum, their annihilation must be compensated.

### Setting up the problem

Let T^{μν}_sq be the energy-momentum tensor of spacetime quanta, T^{μν}_m the matter tensor. The total system:

    T^{μν}_total = T^{μν}_sq + T^{μν}_m + T^{μν}_interaction

Bianchi identity: ∇_μT^{μν}_total = 0.

If quanta are annihilated by matter, there is an energy-momentum exchange:

    ∇_μT^{μν}_sq = -Q^ν (quanta lose energy-momentum)
    ∇_μT^{μν}_m = +Q^ν (matter gains energy-momentum)

where Q^ν is the interaction current.

### What is Q^ν?

The premise says: quanta + matter → matter (absorption). The energy-momentum of the quantum is transferred to matter. So:

    Q^0 = n · (energy per quantum) · (annihilation rate per quantum)
         = n · μ_sq · σ · ρ_m    [where μ_sq is the mass-energy per quantum]

In the homogeneous FLRW case, Q^i = 0. Then the continuity equation for n̄ becomes (from the 0th component):

    ∂(n̄μ_sq)/∂t + 3H(n̄μ_sq)(1+w_sq) = -n̄·μ_sq·σ·ρ_m    [for constant μ_sq]

Dividing by μ_sq (if it's constant):

    ∂n̄/∂t + 3H·n̄·(1+w_sq) = -σ·n̄·ρ_m

For w_sq = 0 (non-relativistic quanta): the 3H term has coefficient (1+w_sq) = 1 → +3Hn̄. ✓
For w_sq = 1/3 (relativistic quanta): coefficient = 4/3 → +4Hn̄. Different!
For w_sq = -1 (dark-energy-like quanta): coefficient = 0 → no dilution term!

**HIDDEN ASSUMPTION #6**: The equation of state of spacetime quanta. SQMH assumes 3Hn̄ (implying w_sq = 0, non-relativistic). But the equation of state is NOT specified by the premise. Different w_sq values give different equations.

### The creation term from GR

GR requires ∇_μT^{μν}_total = 0. If quanta are only annihilated, then n̄ → 0 and eventually T^{μν}_sq → 0. This is consistent — the total T^{μν} is conserved because the energy goes into matter. No Γ₀ is required by GR.

Γ₀ requires an independent source term (like a cosmological creation mechanism — e.g., de Sitter creation, Hawking radiation, or GFT emergence). None of these are implied by the premise.

**Conclusion from Team 6:**

GR / energy-momentum conservation gives:

    **dn̄/dt + 3H·n̄·(1+w_sq) = -σ·n̄·ρ_m**

The 3H coefficient depends on the equation of state (HIDDEN ASSUMPTION #6). SQMH implicitly assumes w_sq = 0 without justification.

Γ₀ has no GR basis from the premise. σ is undetermined from GR alone.

---

## Team 7: Cosmological Perturbation Theory Approach

**Framework:** Start from a background (homogeneous) universe and check whether the SQMH equation is consistent with perturbation theory.

### Background equation

In FLRW, the background equation for n̄(t) from the premise (annihilation only):

    dn̄/dt + 3Hn̄ = -σn̄ρ̄_m

This is acceptable if n̄ decreases monotonically. But then n̄ → 0 and dark energy → 0, which contradicts observed accelerated expansion. So either:
(a) Γ₀ is added (the standard SQMH), or
(b) The premise must be supplemented with a de Sitter / void creation mechanism.

SQMH chooses (a).

### Alternative: Perturbation sourcing

What if the background is flat (n̄ = n̄_0 = const) and it's only PERTURBATIONS δn that obey the sink equation? Then:

    δn̄/dt + 3Hδn + σρ̄_m·δn + σn̄·δρ_m = 0

For linear perturbations around a fixed background n̄ = n̄_0, δn ≪ n̄_0. The background n̄_0 is a free parameter — not forced to satisfy dn̄/dt = 0.

This allows a DIFFERENT formulation: n̄_0 is set by initial conditions (or quantum gravity), and only perturbations evolve. The macroscopic dark energy is then encoded in n̄_0, not in Γ₀.

**Alternative equation from Team 7:**

If n̄ = n̄_0 is frozen (fixed background quantum density), then the relevant equation for dark energy perturbations is:

    δn/dt + 3Hδn + (3H + σρ̄_m)δn = -σn̄_0·δρ_m

The "dark energy" is n̄_0·μ = const, giving w_DE = -1 (cosmological constant behavior). The DESI wa ≠ 0 signal would then require a TIME-VARYING n̄_0, which brings back the Γ₀ question.

**Conclusion from Team 7:**

If the background is allowed to be static (n̄_0 = const), Γ₀ is not needed but the equation gives w_DE = -1 (pure cosmological constant) — no dynamics. To get w_DE ≠ -1 (dynamical DE), n̄ must evolve, which requires either Γ₀ or a different source. The dynamical premise forces the inclusion of Γ₀ as an additional assumption.

---

## Team 8: Dimensional Analysis / Effective Field Theory Approach

**Framework:** What is the most general equation consistent with the premise's symmetry requirements?

### Premise symmetries

The premise "spacetime quanta are annihilated by matter" implies:
- There is a quantum number N_sq that decreases in collisions with matter
- The rate must be Lorentz scalar (for covariance)
- The rate must be positive definite
- The rate must vanish when either n or ρ_m vanishes

The most general sink term consistent with these: f(n, ρ_m) where f(0, ρ_m) = f(n, 0) = 0, f > 0.

The simplest forms (expanding in n and ρ_m):

    (a) f = σ · n · ρ_m                              (mass action, linear)
    (b) f = σ · n^α · ρ_m^β for α, β ≠ 1           (nonlinear)
    (c) f = σ · n · ρ_m · (1 + δ·n)                (self-interaction correction)
    (d) f = σ · n · (ρ_m + ρ_r)                    (quanta also absorbed by radiation?)
    (e) f = σ · n · ρ_m · F(n/n_Planck)            (saturation near Planck density)

SQMH uses form (a). This is the simplest but NOT the only choice.

### What constrains σ?

Dimensional analysis: [σ] = [f] / [n] / [ρ_m] = (m⁻³ s⁻¹) / (m⁻³) / (kg m⁻³) = m³ kg⁻¹ s⁻¹.

From fundamental constants: {G, c, ħ, k_B}. The unique combination with units [m³ kg⁻¹ s⁻¹]:

    G · t_P = G · (ħG/c⁵)^{1/2} has units [m³ kg⁻¹ s⁻²] · [s] = [m³ kg⁻¹ s⁻¹] ✓

So σ ~ G · t_P is dimensionally unique (no other combination of {G, c, ħ} gives these units without introducing additional dimensionless factors). The 4π prefactor is NOT determined by dimensional analysis — it requires a physical argument (solid angle, Gauss's law, etc.).

**HIDDEN ASSUMPTION #7**: σ = 4πGt_P rather than σ = G·t_P or σ = 2πGt_P, etc. The 4π arises from matching to Gauss's law in Newtonian gravity, which is an additional assumption.

### What constrains the Hubble term?

The 3Hn̄ dilution term arises from FLRW geometry. In a static Minkowski universe, there would be no such term. More generally, in a universe with different spatial topology or dimensionality, the factor would differ:
- 4D FLRW: 3H
- 3D FLRW: 2H
- With spatial curvature k: modifications to H(t)

**HIDDEN ASSUMPTION #8**: FLRW geometry (homogeneous, isotropic, 3+1 dimensional expanding universe). The premise says nothing about cosmology.

**Conclusion from Team 8:**

EFT analysis: the premise is consistent with a large family of equations. The specific form dn̄/dt + 3Hn̄ = Γ₀ - σn̄ρ_m requires:
- Mass-action law (linear in both n and ρ_m)
- FLRW geometry (gives 3H)
- Non-relativistic quanta (gives coefficient 1, not 4/3)
- Σ = 4πGt_P (matching to Newtonian G)
- Γ₀ > 0 (separate creation mechanism)

None of these are in the premise. The SQMH equation is ONE CHOICE from a large family.

---

## Summary: Hidden Assumptions in Current SQMH Equation

The current SQMH equation is:

    dn̄/dt + 3Hn̄ = Γ₀ − σn̄ρ_m        with σ = 4πGt_P

**From the single premise, the following are NOT derived — they are hidden assumptions:**

| # | Hidden Assumption | Justified? | Teams detecting |
|---|------------------|-----------|----------------|
| H1 | FLRW expanding universe (gives 3Hn̄ term) | Yes — but must be stated | All teams |
| H2 | Non-relativistic equation of state for quanta (w_sq = 0, coefficient 1 not 4/3) | Not justified by premise | Team 6 |
| H3 | Mass-action law (σnρ_m, linear in both n and ρ_m, not σn²ρ_m etc.) | Assumed, not derived | Teams 4, 8 |
| H4 | Γ₀ > 0 (creation of spacetime quanta) | NOT in premise (premise says only annihilation) | Teams 1,2,3,4,5,6,7,8 |
| H5 | Γ₀ = const (uniform, isotropic creation) | Assumed for de Sitter symmetry | Base.md §2 |
| H6 | σ = 4πGt_P specifically (not 2πGt_P or σ = G·t_P) | Matching to Newtonian G; 4π is geometric assumption | Teams 2,5,8 |
| H7 | Annihilation rate ∝ ρ_m (not ρ_m^(1/2), ρ_m², etc.) | Mass-action law assumed | Teams 3,4,8 |
| H8 | Quanta do NOT interact with radiation (only matter ρ_m) | Chosen, not forced | Team 8 |

---

## σ = 4πGt_P: Origin and Assessment

**What all 8 teams agree on:**

1. The dimensional form σ ~ G·t_P is unique: no other combination of {G, c, ħ} gives units [m³ kg⁻¹ s⁻¹]. This is genuine.

2. The 4π prefactor is NOT forced by the premise. It comes from matching to Gauss's law / spherical geometry:
   - Team 2: arises from matching v(r) to Newton gravity → σ = 4πGt_P circular
   - Team 5: geometric motivation (solid angle) — assumed not derived
   - Team 8: purely empirical — 4π makes the math work for Newtonian gravity

3. The t_P factor is the unique Planck time from {G, ħ, c}. Its appearance is dimensional necessity, not prediction.

4. **The Penrose connection (NF-34, L13-Gamma)**: σ·ρ_P = 4π/t_P = Penrose collapse rate. This is a physically interesting interpretation but not a derivation. (All 8 teams: PARTIAL motivation only.)

**Team verdicts on σ = 4πGt_P:**

| Team | Verdict |
|------|---------|
| T1 (Kinetic) | Undetermined by premise; requires matching |
| T2 (Fluid) | Circular definition via Newtonian gravity matching |
| T3 (QFT) | g²/16π type expression; 4πGt_P not predicted |
| T4 (Stat. Mech.) | Undetermined; free parameter |
| T5 (Info Theory) | G·t_P dimensionally forced; 4π geometric assumption |
| T6 (GR) | Not derivable from GR / Bianchi alone |
| T7 (Perturbation) | Set by matching to observed G |
| T8 (EFT) | Dimensionally unique form; 4π not forced |

**Consensus**: σ = G·t_P is dimensionally unique. σ = 4πGt_P requires the 4π factor which is geometric/matching, not fundamental. The equation **σ = 4πGt_P is not derivable from the premise** — it is fixed by requiring the theory to reproduce Newtonian gravity.

---

## Γ₀ (Creation Term): Assessment

**The premise mentions ONLY annihilation. Γ₀ is entirely absent from the premise.**

| Team | Finding about Γ₀ |
|------|-----------------|
| T1 (Kinetic) | Premise gives Γ₀ = 0; equation unstable (n→0) |
| T2 (Fluid) | Premise gives Γ₀ = 0; must be added separately |
| T3 (QFT) | Crossing symmetry suggests creation exists; but value not fixed |
| T4 (Stat. Mech.) | Γ₀ > 0 required for stationary state; chosen to ensure stability |
| T5 (Info Theory) | Landauer motivates creation; value undetermined |
| T6 (GR) | Not required by Bianchi identity; cosmological constant can replace |
| T7 (Perturbation) | Required for dynamical DE (wa ≠ 0); w=-1 works without it |
| T8 (EFT) | General possible source term; specific Γ₀ = const is special |

**Consensus on Γ₀:**
- The premise does NOT imply Γ₀
- Γ₀ > 0 is added to ensure the universe is not empty at late times
- The specific value Γ₀ = σn̄₀ρ_m0 + 3H₀n̄₀ (balance condition) is a CHOICE of initial conditions, not a derivation
- Justifications available (QFT crossing symmetry, thermodynamic Landauer argument, de Sitter symmetry) are motivations, not derivations from the premise

**The creation term Γ₀ represents the single biggest departure from the premise.**

---

## Alternative Equations Reached by Each Team

| Team | Alternative Equation |
|------|---------------------|
| T1 (Kinetic) | dn̄/dt + 3Hn̄ = −σn̄ρ_m (no creation) |
| T2 (Fluid) | dn̄/dt + 3Hn̄ = −σn̄ρ_m (no creation) |
| T3 (QFT) | dn̄/dt + 3Hn̄ = Γ_sp − σn̄ρ_m (spontaneous emission from crossing symmetry, value unfixed) |
| T4 (Stat. Mech.) | dn̄/dt + 3Hn̄ = λ(n̄) − σn̄ρ_m (general creation function) |
| T5 (Info Theory) | dn̄/dt + 3Hn̄ = Γ(n̄) − σn̄ρ_m (Landauer feedback) |
| T6 (GR) | dn̄/dt + 3H(1+w_sq)n̄ = −σn̄ρ_m (w_sq undetermined) |
| T7 (Perturbation) | n̄ = n̄_0 = const (static background); only δn evolves |
| T8 (EFT) | dn̄/dt + 3Hn̄ = Γ₀ − σ·n̄^α·ρ_m^β (general nonlinear form) |

---

## Integrated Conclusion: Is the Current SQMH Equation Unique?

**NO. The current SQMH equation is NOT uniquely derivable from the premise.**

The 8 independent teams, each working from the same single premise, reached significantly different equations. The current SQMH equation:

    dn̄/dt + 3Hn̄ = Γ₀ − σn̄ρ_m    with σ = 4πGt_P

requires at minimum the following additional assumptions beyond the premise:

1. **FLRW geometry** (Hubble dilution term 3Hn̄)
2. **Non-relativistic quanta** (coefficient 1 vs 4/3)
3. **Linear mass-action law** (σnρ_m vs σn²ρ_m or σnρ_m^{1/2})
4. **Γ₀ > 0 (creation term)** — the single biggest departure from premise
5. **Γ₀ = const (uniform creation)** — de Sitter symmetry assumption
6. **σ = 4πGt_P specifically** — matching to Newtonian gravity; 4π is geometric assumption
7. **Quanta couple only to non-relativistic matter** (not radiation)

**The equation is a REASONABLE CHOICE given these additional assumptions, but it is not the ONLY or FORCED choice from the premise. It is a self-consistent but arbitrary selection from a family of possible equations.**

The most honest description: the SQMH equation is the simplest linear equation consistent with:
- The annihilation premise
- FLRW cosmology
- Newtonian gravity (for σ determination)
- A stable (non-empty) late-time universe (for Γ₀ ≠ 0)

**Each of these additional inputs is physically reasonable but is NOT contained in the original premise.**

---

*L14 8-team derivation review completed: 2026-04-11*
