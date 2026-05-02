# L406 — 8-Person Attack Design (S_8 Worsening Reviewer Risk)

## Threat model
A reviewer (PRD/JCAP) reads §6.1 row 1 + §4.6 and reacts in one of three ways.
We need to know which probability dominates and whether the existing
"honest disclosure" (paper/base.md §4.6, §6.1, README) defuses each.

## 8-person red-team scan (no role pre-assignment; team self-distributed)

The team converged on three reviewer archetypes through free discussion:

### Archetype A — "instant reject" (worst case)
> "The model worsens a tension it claims to address. Reject."

- **Trigger**: reading abstract or §1.2.3 in isolation.
- **Mitigation present?** Partially. §4.6 + §6.1.1 #1 explicitly admit
  `+1.14% structural worsening, no escape`. Abstract carries the disclosure.
- **Residual risk**: a hostile reviewer who skim-reads will still pull this
  trigger. Honest framing reduces probability but cannot eliminate it.
- **Estimated probability**: ~25% (down from ~70% if disclosure absent).

### Archetype B — "this is a falsifier, not a flaw" (best case)
> "Worsening is a real prediction; Euclid/LSST will adjudicate. Accept as
>  honest pre-registered falsification target."

- **Trigger**: reading §4.6 + §6.1 row 1 + §6.1 row 14 together.
- **Conditions**: requires (i) explicit "no parameter escape" wording,
  (ii) facility-specific n-sigma detection forecast, (iii) pre-registered
  falsification statement.
- **Currently present?** (i) yes, (ii) partial (only LSST mentioned in
  §4.6, no σ quantified), (iii) yes (table row 14 is OPEN, "LSST/Euclid
  대기").
- **Gap**: quantitative forecast missing. **L406 fills this gap**
  (forecast_facilities.json: DES-Y3 0.6σ, Euclid 4.4σ, LSST-Y10 2.9σ).

### Archetype C — "fix it or remove the claim" (middle case)
> "If the theory worsens S_8, either propose a mitigation channel or
>  retract the cosmological-fit claims."

- **Trigger**: structural-physicist reviewer with strong-Bayes priors.
- **Mitigation path required**: must show that *within the hypothesis
  space* there is no escape (so the worsening is a real prediction, not
  a fixable bug).
- **L406 §3 simulation result**: dark-only fluid-level coupling
  `G_eff/G = 1 + 2β_eff²` is **monotonically ≥ 1** for any β_eff(a)
  → growth always *enhanced* → ΔS_8 ≥ 0 *structurally*. No grid point
  produces negative ΔS_8. Mitigation **STRUCTURALLY UNREACHABLE** at
  fluid level.
- **Effect on archetype C**: converts complaint into evidence that the
  worsening is a *robust prediction*, not a tunable nuisance.

## Effect of existing honest disclosure (paper/base.md §6.1 #1)

| Reviewer archetype | P(reject) without §6.1 | P(reject) with §6.1 |
|---|---|---|
| A — instant reject | ~70% | ~25% |
| B — falsifier-friendly | ~10% | ~5% |
| C — structural-physicist | ~50% | ~20% (further → ~10% if L406 attached) |

The §6.1 row + §4.6 disclosure is **necessary but not sufficient**.
Sufficient framing requires:
1. Quantitative facility forecast (L406 produces).
2. Structural-impossibility proof of mitigation within fluid-level
   embedding (L406 produces).
3. Pre-registered Euclid/LSST falsification clause in abstract.

## Attack-design summary

The dominant residual risk is Archetype A skim-reject. To defuse it:
- Move `+1.14% S_8 worsening (Euclid 4.4σ falsifier)` into the **first
  paragraph of the abstract** alongside the DESI w_a claim.
- Phrase as: *"This work pre-registers a 4.4σ Euclid falsification
  target."* — converts a weakness into a falsifiability badge.

Verdict: continue with current honest-framing track. Add quantitative
forecast (NEXT_STEP §B). Do **not** attempt mitigation — L406 §3 shows
it cannot succeed at this theory level and any apparent fix would be
parameter-fitting artefact.
