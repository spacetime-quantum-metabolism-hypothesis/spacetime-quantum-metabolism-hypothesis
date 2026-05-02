# L413 — 8-Person Attack Design (Euclid 4.4σ pre-registered falsifier)

## Mandate (PR P0-2)

L406 produced the forecast `ΔS_8 = +0.0114` (SQT vs ΛCDM, structurally
unreachable mitigation, μ_eff≈1) and three facility n-σ values:

| Facility | σ(S_8) | n-σ |
|---|---|---|
| DES-Y3 (current) | 0.018 | **0.63σ** |
| LSST-Y10 (~2032) | 0.0040 | **2.85σ** |
| Euclid IST (~2027) | 0.0026 | **4.38σ** |

The 8-person team red-teams the question: **is "Euclid 4.4σ pre-registered
falsifier" a sufficient, defensible, falsifiable claim for a JCAP / PRD
referee, and is the threshold (4.4σ) physically and statistically
well-defined?** No role pre-assignment (CLAUDE.md L17 rule); team
self-distributed across attack vectors.

## Attack vectors enumerated (free discussion → 6 reviewer angles)

### V1 — "4.4σ is point-estimate, not posterior. Refuse."
> Reviewer challenge: the n-σ comes from a Gaussian likelihood
> `ΔS_8 / σ(S_8)` with σ(S_8) lifted from Euclid IST forecasts. It is
> NOT a marginalised posterior over (Ω_m, h, n_s, ω_b, A_s, ...).
> True forecast must run the full Euclid mock 3×2pt likelihood with
> nuisance parameters (IA, photo-z, baryonic feedback).

**Defence**: Concede that 4.4σ is a **toy linear-bias forecast** with
ξ_+ ∝ S_8². The ATTACK_DESIGN explicitly disclaims it as a Phase-7
upgrade. The pre-registered claim is *"a structural ξ_+ excess of
~+2.29% should be detectable by Euclid DR1 weak-lensing 2pt at the
3–5σ level under standard nuisance assumptions"* — the 4.4σ is the
central value, not a proper posterior bound. The CLAUDE.md L406
caveat is already in place.

**Residual risk**: Medium. A Boltzmann-purist reviewer may still demand
hi_class + Cobaya likelihood. We pre-empt with abstract footnote
*"central forecast; full nuisance-marginalised likelihood is Phase-7
work"*. Probability of forced revision: ~20%, not reject.

### V2 — "Why 4.4σ instead of 3σ or 5σ?"
> Reviewer challenge: discovery threshold convention is 5σ in particle
> physics, 3σ in cosmology. Why a non-standard 4.4σ?

**Defence**: 4.4σ is **not a chosen threshold**; it is the *central
forecast value* derived from `+0.0114 / 0.0026 = 4.38σ`. The threshold
for falsification is operationally 3σ (cosmology convention). The 4.4σ
is the central detection-σ; the 3σ-falsification claim follows
*a fortiori* (4.4σ central → P(>3σ) ≈ 92% under Gaussian forecast).
The paper should phrase as:
> *"central forecast 4.4σ; structurally falsified at >3σ if Euclid DR1
> measures ξ_+(10') excess consistent with ΛCDM (not SQT +2.29%)."*

### V3 — "Pre-registration without timestamp is meaningless."
> Reviewer challenge: claiming "pre-registered" requires verifiable
> timestamp before Euclid DR1 release. GitHub commit hash + OSF DOI
> required, otherwise hindsight bias.

**Defence**: This is **valid and not yet executed**. NEXT_STEP §B
specifies the OSF + GitHub-tag procedure (Phase-7 pre-DR1 lock).
For the present submission, the claim is:
> *"pre-registered in this preprint version arXiv:YYMM.NNNNN at
> commit-hash <H>; cross-deposited on OSF DOI <D>."*
The commit hash is automatically generated at arXiv submission;
the OSF deposit is a Phase-7 administrative step (NEXT_STEP §B).

**Residual risk**: Medium-low. Verifiable on submission day.

### V4 — "Euclid DR1 timing — 2027 or later?"
> Reviewer challenge: Euclid Q1 release is 2025-03 (already public,
> partial sky). DR1 cosmic-shear 2pt is 2026–2027 (Euclid Collab. 2024
> roadmap). The paper must specify *which* Euclid release.

**Defence**: Lock to **Euclid DR1 cosmic-shear 2pt analysis**
(Euclid Collaboration roadmap, 2026–2027 expected). Q1 (2025-03)
is photometric only, not 3×2pt; Q1 cannot falsify the S_8 prediction.
DR1 σ(S_8) ≈ 0.0026 is the IST forecast number. Pre-registration
clock = "before Euclid DR1 cosmic-shear 2pt official ξ_± paper".

### V5 — "ΔS_8 = +0.0114 itself depends on Ω_m. Float it."
> Reviewer challenge: SQT μ_eff≈1 prediction shifts S_8 only after
> fixing Ω_m, h. If joint posterior Ω_m drifts, ΔS_8 changes.

**Defence**: L406 grid (`grid_S8_vs_Vparams.csv`, 117 points) sweeps
the V(n,t) parameter box and finds ΔS_8 ∈ [+0.0098, +0.0131] across
the entire physically allowed sector. The 4.4σ central value uses
mid-grid ΔS_8 = +0.0114; the 1σ band on the *prediction itself* is
±0.0008, which subtracts in quadrature: σ_total = √(0.0026² + 0.0008²)
≈ 0.00272 → 4.19σ (still > 4σ). Robust.

### V6 — "What if Euclid measures ΔS_8 = +0.005? Half the SQT prediction."
> Reviewer challenge: partial detection is the most likely outcome.
> What does SQT predict in that case?

**Defence**: This is the most physically interesting attack and
highlights the falsifier's two-sided nature.
- ξ_+(10') excess **+2.29% ± 0.5%** (1σ): SQT consistent.
- excess **0% (LCDM-like)**: SQT excluded at 4.4σ.
- excess **negative** (anti-SQT): SQT excluded at >5σ.
- excess **+1% (half)**: ambiguous, Δχ² ≈ 4 → tension but not exclusion.
The paper should embed the **two-sided decision rule** explicitly in
§4.6 and §6.1 row 14 (NEXT_STEP §C).

## Net assessment of "4.4σ Euclid pre-registered falsifier" claim

| Criterion | Status |
|---|---|
| Quantitatively defined? | Yes — central forecast 4.4σ, 3σ falsification floor. |
| Pre-registration verifiable? | Pending — OSF DOI + GitHub-tag procedure (NEXT_STEP §B). |
| Two-sided (consistency / exclusion)? | Yes — V6 decision rule. |
| Robust to nuisance / Ω_m drift? | Yes within grid (±0.0008 on ΔS_8); full hi_class is Phase-7. |
| Timing locked? | Yes — Euclid DR1 cosmic-shear 2pt (2026–2027). |

**Verdict**: **CLAIM IS DEFENSIBLE** with three caveats explicitly in
the paper:
1. "central forecast, full nuisance-marginalised likelihood is Phase-7"
2. "OSF DOI + GitHub-tag at submission t₀"
3. Two-sided decision rule (V6 above)

The 4.4σ is sufficient quantitatively (>3σ cosmology threshold). It is
NOT 5σ-discovery-grade, and the paper must not advertise it as such.

## Probability of reviewer reject (8-person consensus estimate)

| Reviewer archetype | P(reject) without §4.6 + row 14 update | P(reject) with L413 update |
|---|---|---|
| A — instant reject | ~25% | ~10% |
| B — falsifier-friendly | ~5% | ~3% |
| C — structural-physicist | ~20% | ~10% |
| D — Boltzmann-purist (V1) | ~30% | ~15% revise (not reject) |

Net P(reject) drops from ~20% (mean) to ~10% (mean). Net P(major-revise)
holds at ~15% (V1 likely demands hi_class). Acceptable for JCAP target.
