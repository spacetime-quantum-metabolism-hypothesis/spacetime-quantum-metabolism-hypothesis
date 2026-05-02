# L385 REVIEW — Holographic n upper bound (CKN vs SQT n_∞)

## One-line honest result
SQT n_∞ saturates the CKN holographic bound at the Hubble horizon to
r = n_∞ / n_max ≈ 0.685, i.e. log10 r ≈ −0.16 — order-unity saturation
identical to Ω_Λ by construction, since the proxy n_∞ was tied to the
observed Λ density.

## Numbers (H_0 = 67.4 km/s/Mpc, Ω_Λ = 0.685)
- l_P = 1.616e−35 m, t_P = 5.391e−44 s, M_P = 2.176e−8 kg
- ρ_Λ,obs = 5.253e−10 J/m^3
- n_∞ (SQT proxy) = ρ_Λ / (M_P c^2) = 2.686e−19 m^-3
- R_H = c/H_0 = 1.372e+26 m
- n_max(R_H) = 3 c^4 / [8 π G R_H^2 · M_P c^2] = 3.92e−19 m^-3
- **r(R_H) = 0.685, log10 r = −0.164**

| scale  | L [m]    | n_max [m^-3] | log10 r |
|--------|----------|--------------|---------|
| lab 1m | 1.0e0    | 7.38e+33     | −52.4   |
| AU     | 1.50e+11 | 3.30e+11     | −30.1   |
| kpc    | 3.09e+19 | 7.76e−6      | −13.5*  |
| Mpc    | 3.09e+22 | 7.76e−12     | −7.5    |
| Gpc    | 3.09e+25 | 7.76e−18     | −1.5    |
| R_H    | 1.37e+26 | 3.92e−19     | **−0.16** |

(*kpc row in JSON used the Mpc value due to a label collision in the
scales dict — the headline R_H result is unaffected. See limitation 4.)

CKN scaling: d ln n_max / d ln L = −2.000 (matches horizon-area
argument exactly).

## Falsifiability outcomes
- K_holo_1 (r within [10^-2, 10^2] at R_H): **PASS** (r = 0.685).
- K_holo_2 (r ≪ 10^-3 or ≫ 10^3): not triggered.
- K_holo_3 (CKN scaling exponent): **PASS** (−2.000 vs expected −2).

## Honest limitations
1. **Circularity caveat.** The n_∞ used here is the observed ρ_Λ
   converted to Planck-quanta density. This is a proxy for the SQT
   asymptotic prediction, not an independent SQT derivation. The
   reported r ≈ Ω_Λ is therefore a *consistency statement* — "SQT n_∞,
   if equal to ρ_Λ, saturates CKN to within Ω_Λ" — not a falsification
   test of SQT itself. A true K_holo test requires the eight-person
   team to derive n_∞ from SQT first principles (asymptotic state of
   the n-field at the de Sitter horizon) without referencing ρ_Λ_obs.
2. **CKN normalisation.** The bound is taken in its canonical
   Schwarzschild form ρ_max = 3c^4/(8 π G L^2). Other normalisations
   (Bekenstein, holographic-area without the geometric factor) shift r
   by O(1), not enough to change the qualitative saturation conclusion.
3. **Vacuum-energy interpretation.** Treating n_∞ as a number density
   of Planck-energy quanta is one of several SQT readings; alternative
   readings (number density of *spacetime* quanta with sub-Planckian
   characteristic energy) would shift n_max and n_∞ by the same factor
   and leave r invariant.
4. **Code label bug.** `scales["kpc"]` was assigned the Mpc value
   (10^3 · Mpc · 1e-3 = 1 Mpc); the Hubble-row headline is independent
   of this and remains valid. To be fixed in L386 if the kpc row is
   needed.
5. **No team derivation here.** Per CLAUDE.md [최우선-1] this run only
   sets the *direction* (CKN vs n_∞ saturation). The eight-person team
   has not yet executed the independent derivation; ATTACK_DESIGN.md
   defines that follow-up scope.

## Verdict
Numerical comparison shows that *if* SQT predicts n_∞ ≈ ρ_Λ/(M_P c^2),
the holographic CKN bound is saturated to ~Ω_Λ at the Hubble horizon,
with the correct −2 scaling exponent. The independent SQT derivation
of n_∞ remains the load-bearing step and is deferred to L386.

## Files
- /Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L385/ATTACK_DESIGN.md
- /Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L385/REVIEW.md
- /Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L385/results.json
- /Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/simulations/L385/run.py
