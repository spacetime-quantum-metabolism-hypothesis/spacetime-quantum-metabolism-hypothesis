# C26 Perez-Sudarsky — L5 Phase E reformulation

**Verdict: KILL (CMB-dominated).  K10 self-consistent but the new ansatz
hits CMB too hard for any α_Q > 0 to survive the joint fit.**

## Background

L4 killed C26 on K10 because the full-ODE ansatz J⁰ = α_Q ρ_c0 (H/H₀)
exponentially depleted matter and disagreed with the L3 linearised drift
toy.  The Phase E task was to test an alternative ansatz
**J⁰ = α_Q H ρ_m** (matter-proportional drift, more natural for
unimodular diffusion since the source is intrinsic to the matter sector).

## Method

The new ansatz gives a **linear closed-form** solution in e-folds:

    dρ_m/dN = −3ρ_m − α_Q ρ_m  =>  ρ_m(N) = ρ_m,0 · exp(−(3+α_Q) N)
                                            = Ω_m · a^{−(3+α_Q)}

    dρ_L/dN = +α_Q ρ_m
    =>  ρ_L(a) = Ω_L,0 + (α_Q Ω_m / (3+α_Q)) · (1 − a^{−(3+α_Q)})

No ODE solver, no bisection, no stiffness — the failure mode that killed
the L4 full ODE is structurally impossible here.

## Result

| α_Q   | Ω_m  | h    | χ²_BAO | χ²_SN  | χ²_CMB | χ²_RSD | χ²_tot |
|-------|------|------|--------|--------|--------|--------|--------|
| 0.00  | 0.320| 0.669| 23.57  | 1643.73| **2.29** | 7.31   | 1676.90 |
| 0.02  | 0.320| 0.670| 24.67  | 1643.52| **38.34**| 7.29   | 1713.83 |
| 0.05  | 0.320| 0.670| 30.17  | 1643.13| **193.61**| 7.29  | 1874.21 |
| 0.10  | 0.320| 0.670| 50.62  | 1642.58| **727.40**| 7.29  | 2427.89 |

tight_fit best fit: α_Q = 0 exactly (indistinguishable from LCDM).
Δχ² vs LCDM = −1.2 × 10⁻⁶.

## Physical interpretation

The matter-proportional drift `J⁰ = α_Q H ρ_m` makes ρ_m grow as
`a^{−(3+α_Q)}` going backward, i.e. matter was *more* abundant in the
past than in standard ΛCDM.  This shifts the matter-radiation equality
redshift and the acoustic sound horizon by an amount that Planck
compressed CMB rejects immediately: χ²_CMB goes from 2.3 at α_Q=0 to
38 at α_Q=0.02 (already > 5σ).

The L3 drift toy `ρ_m ≈ Ω_m a⁻³ (1 − α_Q(1−a³))` is the a → 1 first
derivative of this exact form, and agrees with it in sign at *fixed*
(Om, h).  When joint (Om, h, α_Q) are fit against CMB, however, the
toy's incorrect high-z behaviour — it underestimates matter growth at
z ≫ 1 — masks the CMB penalty that the full form incurs.  The L3 toy
was effectively fitting a different model.

## K flags

- K1 (Δχ²): 0  — no improvement
- K2 (|w_a|): w_a ≈ 0 at the minimum, 0 < 0.125
- K10 (toy ↔ full sign): formally matches at the degenerate minimum
  (both → 0), but if we force α_Q = 0.05 both give w_a < 0 so the
  sign *direction* is consistent — K10 cleared in the sense originally
  meant in the Phase E task.  The **real issue is K1/K2**: the CMB
  simply rejects the diffusion source.
- K12: LCDM trivially within 1σ (model reduces to LCDM).

## Verdict

**KILL.**  The reformulation succeeds at fixing the L4 K10 failure
(closed-form, no ODE blow-up, consistent with the L3 toy in the
small-α_Q limit), but the joint likelihood now rejects every α_Q > 0
with overwhelming CMB penalty.  Perez-Sudarsky unimodular diffusion
at background level with a matter-proportional current is **CMB-dead**
under the compressed CMB likelihood.

A future attempt could move the diffusion source off-shell (e.g.
affect only dark sector through a sector-selective coupling, as in
C10k) but that is a different model.  For Phase L5 Tier 1,
C26 remains KILLed.
