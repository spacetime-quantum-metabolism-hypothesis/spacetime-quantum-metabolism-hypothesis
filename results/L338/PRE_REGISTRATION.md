# SQT Pre-Registration Document — DESI DR3 w_a Test (P17)

**Title:** Pre-registered SQT prediction for the dark-energy CPL parameters (w_0, w_a) prior to DESI DR3 release
**Author:** SQMH collaboration (8-person independent committee, L338)
**Date frozen:** 2026-05-01
**Cumulative loop count at freeze:** 245
**Intended timestamp channels:** OSF registration + arXiv preprint + signed Git tag (`v1.0-preDR3-prereg`)
**Target data release:** DESI DR3, expected mid-to-late 2026

---

## 1. Scope and intent

This document fixes the SQT-predicted values, theory uncertainties, and decision boundaries for the dark-energy equation-of-state parameters (w_0, w_a) measured by the DESI DR3 BAO release. It is intended to be timestamped publicly *before* DR3 unblinding so that the post-release verdict cannot be back-fitted.

This is a single-shot pre-registration: post-DR3 the SQMH collaboration commits to publishing the verdict using exactly the bands defined here, regardless of outcome.

---

## 2. Theory tiers being tested

### Tier A — Minimal SQT (Λ-static)

**Axiom commitment:** L0–L2 of SQT with constant V(n).
**Predicted central values:**
- w_0 = −1.000  (no theory uncertainty)
- w_a =  0.000  (no theory uncertainty)

Tier A is observationally indistinguishable from ΛCDM at the background w(z) level. It can only be falsified by a w_a or w_0 measurement that excludes (−1, 0) at high significance.

### Tier B — Extended SQT V(n,t) (independent derivation, L327)

**Axiom commitment:** L0–L2 plus a temporally running V(n,t) tracker (slow-roll regime, |λ| ≲ 0.4). The functional form is derived independently in L327 and is *not* fit to DR3 data.
**Predicted central values + 1σ theory band:**
- w_0 = −0.95 ± 0.03
- w_a = −0.30 ± 0.15

The 1σ theory bands are *prior* uncertainties from residual freedom in the slow-roll parameter space, not posterior fits. They are frozen here and cannot be widened post-DR3.

**Correlated predictions (all locked simultaneously):**
- CPL ellipse principal-axis slope dw_a/dw_0 ≈ +6 ± 2 along the SQT trajectory.
- Ω_m ∈ [0.27, 0.35] (preferred 0.31 ± 0.02 under Tier B).
- H_0 unresolved (Tier A ≈ 67.4 km/s/Mpc Planck; Tier B does not shift H_0 — μ_eff ≈ 1 structurally; SQT does NOT predict high H_0).

---

## 3. DR3 measurement assumed

We assume DR3 will publicly release a CPL fit with central w_a^DR3 and 1σ uncertainty σ_DR3 in the range 0.10 ≤ σ_DR3 ≤ 0.18 (likely) for the BAO+CMB primary combination. If σ_DR3 falls outside this range we will recompute boundaries using the DESI-released σ_DR3 *exactly as quoted*, with no further freedom.

**Primary statistic:** w_a^DR3 from the DESI primary combination (BAO + Planck CMB, no SN). Secondary statistics: BAO-only, BAO+SN+CMB joint. We pre-commit "primary" = BAO+CMB joint.

---

## 4. Decision rules (frozen)

### 4.1 Tier A bands

| Region | Condition on w_a^DR3 | Verdict |
|--------|----------------------|---------|
| PASS A | \|w_a^DR3\| ≤ 2 σ_DR3 | Tier A consistent |
| INCONCLUSIVE A | 2 σ_DR3 < \|w_a^DR3\| ≤ 3 σ_DR3 | Tension |
| FAIL A | \|w_a^DR3\| > 3 σ_DR3 | Tier A killed |

### 4.2 Tier B bands

Define σ_tot ≡ √(σ_DR3² + 0.15²).

| Region | Condition on w_a^DR3 | Verdict |
|--------|----------------------|---------|
| PASS B (strong) | \|w_a^DR3 + 0.30\| ≤ 1 σ_tot AND w_a^DR3 < 0 | Tier B confirmed |
| PASS B (weak) | \|w_a^DR3 + 0.30\| ≤ 2 σ_tot AND w_a^DR3 < 0 | Consistent |
| INCONCLUSIVE B | 2 σ_tot < \|w_a^DR3 + 0.30\| ≤ 3 σ_tot | Tension |
| FAIL B | w_a^DR3 > +0.10 OR w_a^DR3 < −1.50 OR \|w_a^DR3 + 0.30\| > 3 σ_tot | Tier B killed |

### 4.3 Inconclusive (joint)

> **Inconclusive ≡** w_a^DR3 is consistent with both (w_a = 0) and (w_a = −0.30) at less than 2σ_tot, AND its 95% CI spans both predictions.
>
> Under inconclusive: neither tier may be reported as confirmed; result is "deferred to DR4 / Euclid-BAO joint".

### 4.4 Joint outcome matrix

| DR3 result region | Tier A | Tier B | Theory verdict |
|-------------------|--------|--------|----------------|
| \|w_a^DR3\| ≲ 0.1 | PASS | FAIL B | SQT collapses to Λ-static; V(n,t) extension dies |
| −0.6 ≲ w_a^DR3 ≲ −0.1 | INCONCLUSIVE/FAIL A | PASS B | Strongest SQT outcome — extension confirmed |
| −1.0 ≲ w_a^DR3 ≲ −0.6 | FAIL A | PASS B (weak) | Compatible with Tier B at 2σ |
| w_a^DR3 > +0.10 | FAIL A | FAIL B | **SQT falsified at the BAO-CPL level** |
| w_a^DR3 < −1.50 | FAIL A | FAIL B | **SQT falsified at the BAO-CPL level** |

### 4.5 Correlated-channel triggers (separate FAIL flags)

These trigger independent FAIL even if w_a alone passes:

- Ω_m^DR3 < 0.27 OR > 0.35 → Tier B Ω_m FAIL.
- CPL ellipse slope dw_a/dw_0 outside +4 to +8 → Tier B geometry FAIL.
- w_0^DR3 outside [−1.05, −0.85] AND Tier B otherwise active → Tier B w_0 FAIL.

---

## 5. What this document does NOT claim

To prevent overreach, the following are explicitly excluded from the pre-registered claims:

- SQT does not predict resolution of the H_0 tension. A high-H_0 DR3 outcome is neutral, not supportive.
- SQT does not predict resolution of the S_8 tension (μ_eff ≈ 1 structurally; ΔS_8 < 0.01%). Any S_8 movement in DR3-derived joint analyses is unrelated.
- Tier B 1σ band 0.15 is a theory prior, not a measurement uncertainty. We do not claim it shrinks with more data.
- "Pre-registration" applies only after public OSF + arXiv + signed-Git timestamps are achieved before DR3 unblinding. This document alone is internal.

---

## 6. Post-DR3 reporting commitment

On DR3 release day, the SQMH collaboration commits to:

1. Reading w_a^DR3, σ_DR3, w_0^DR3, Ω_m^DR3 from the DESI primary combination *first*.
2. Computing σ_tot using the locked Tier B 1σ = 0.15 (not refit).
3. Applying the §4 decision rules without modification.
4. Publishing the verdict (PASS / FAIL / INCONCLUSIVE under each tier) within 30 days of DR3 release.
5. If FAIL on both tiers: retract SQT BAO-CPL claims in the JCAP manuscript; preserve the rest of the framework only as exploratory.
6. If INCONCLUSIVE: defer to DR4 / Euclid-BAO joint and explicitly state "DR3 does not discriminate".

---

## 7. Hash and timestamp record (to be filled at registration)

```
SHA-256 of this file (PRE_REGISTRATION.md):    [TO BE COMPUTED AT FREEZE]
SHA-256 of ATTACK_DESIGN.md (companion):       [TO BE COMPUTED AT FREEZE]
OSF registration ID:                            [TO BE FILLED]
arXiv preprint number:                          [TO BE FILLED]
Git tag:                                        v1.0-preDR3-prereg
Git commit SHA (signed):                        [TO BE FILLED]
DESI DR3 expected release window:               2026 mid-to-late
Date this document frozen:                      2026-05-01
```

---

## 8. Honest caveats

- Tier B numerical bands depend on L327 V(n,t) derivation completing as an independent single-parameter family. If L327 fails to converge before timestamp deadline, only Tier A is pre-registered, and Tier B becomes a post-DR3 exploratory test (clearly marked, not a "prediction").
- The DR3 σ range 0.10 – 0.18 is forecast; actual may be 1.3–2× larger if DESI quotes more conservative systematics. We commit to using the DESI-quoted σ_DR3 verbatim.
- Pre-registration is a scientific-integrity claim, not a statistical guarantee. Even with timestamps, an unblinded look at preliminary DR3 data before freezing this document would invalidate the claim. We affirm no such look has occurred at freeze date.
