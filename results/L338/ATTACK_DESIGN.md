# L338 — Attack Design: P17 Pre-Registration for DESI DR3 w_a Unblinding

**Date:** 2026-05-01
**Loop:** 245 (cumulative)
**Frame:** Lock SQT prediction band on w_a (and supporting CPL geometry) *before* DESI DR3 unblinding so that the post-release verdict is genuinely pre-registered, not back-fitted.
**Method:** Two-tier prediction (minimal SQT vs V(n,t)-extended SQT), explicit PASS / FAIL / INCONCLUSIVE bands, frozen prior to DR3 release; arXiv preprint + OSF time-stamping protocol.
**8-person independent ideation; no equation-level guidance.**

---

## 1. Why this is the decisive falsifier

From L326 KL ranking (cumulative 244 loops):

- D_KL(P17) ≈ 5.6 – 14.2 nats (highest of 8 channels)
- Cost: $ (data already collected, awaiting public release)
- Timeline: 2025–2026 (imminent; DR3 expected mid-to-late 2026)
- Risky/safe split: predicts a *direction* (w_a < 0) that DR2 already mildly favors; DR3 σ shrinks → SQT either consolidates or is killed.

P17 is the only forward channel that can both confirm and falsify SQT inside the next 12–18 months at the σ level required for a PRD/JCAP-decisive claim. Pre-registration is therefore the pivotal scientific-integrity step: without a pre-DR3 timestamp the eventual claim is suspect of post-hoc fit, regardless of how well SQT ends up matching.

---

## 2. SQT prediction tiers — what gets locked

Two independent prediction tiers must be locked simultaneously, because each tier corresponds to a different theoretical commitment, and DR3 will discriminate between them.

### Tier A — Minimal SQT (Λ-static branch)

**Theoretical commitment:** SQT axiom set L0–L2 with V(n) ≡ const (no temporal tracker), matter-radiation-Λ standard background.

**Prediction:**
- w_0 = −1.000  (exact, no parameter freedom)
- w_a =  0.000  (exact)
- Equivalent to ΛCDM at the background w(z) level.

**Distinguishing observable:** SQT-minimal predicts that the DR3 CPL ellipse must contain (w_0, w_a) = (−1, 0) at ≤2σ. Any DR3 result that excludes the ΛCDM point at ≥3σ kills Tier A.

### Tier B — Extended SQT V(n,t) (running tracker branch)

**Theoretical commitment:** SQT with the V(n,t) extension (independently derived in L327; not imported here). Adds one effective parameter coupling psi-field running to background expansion.

**Prediction (central + 1σ theory band):**
- w_0 = −0.95 ± 0.03
- w_a = −0.30 ± 0.15

The 1σ theory band reflects genuine residual freedom in the V(n,t) shape (slow-roll regime, |λ| ≲ 0.4) — *not* a fitted posterior. Wider would be intellectually dishonest; narrower would pretend the extension is fully determined.

---

## 3. Pre-registered decision boundaries on w_a

DR3 forecast σ(w_a) is in the range 0.10 – 0.18 depending on which dataset combination the collaboration releases (BAO-only vs BAO+SN+CMB joint). We lock the verdict bands using DR3 central w_a and its quoted 1σ.

Let w_a^DR3 be the DR3-released central value, σ_DR3 its quoted 1σ.

### Tier A (Λ-static) verdict bands

| Region | Condition | Verdict |
|--------|-----------|---------|
| PASS A | \|w_a^DR3\| ≤ 2 σ_DR3 | Λ-static SQT consistent at <2σ |
| INCONCLUSIVE A | 2 σ_DR3 < \|w_a^DR3\| ≤ 3 σ_DR3 | Tension but not fatal |
| FAIL A | \|w_a^DR3\| > 3 σ_DR3 | Tier A killed; Tier B still alive |

### Tier B (V(n,t) extended) verdict bands

Tier B central w_a^pred = −0.30, theory 1σ = 0.15. Combined uncertainty σ_tot = √(σ_DR3² + 0.15²).

| Region | Condition | Verdict |
|--------|-----------|---------|
| PASS B (strong) | \|w_a^DR3 − (−0.30)\| ≤ 1 σ_tot AND w_a^DR3 < 0 | SQT-ext confirmed |
| PASS B (weak) | \|w_a^DR3 − (−0.30)\| ≤ 2 σ_tot AND w_a^DR3 < 0 | Consistent |
| INCONCLUSIVE B | 2 σ_tot < \|w_a^DR3 − (−0.30)\| ≤ 3 σ_tot | Tension |
| FAIL B | w_a^DR3 > +0.10 OR w_a^DR3 < −1.50 OR \|w_a^DR3 − (−0.30)\| > 3 σ_tot | Tier B killed |

### Joint (theory-level) outcome matrix

| DR3 result | Tier A | Tier B | Theory verdict |
|------------|--------|--------|----------------|
| \|w_a\| ≤ 0.1 (≈ ΛCDM) | PASS | FAIL B (w_a^pred too negative) | **SQT collapses to minimal Λ-static** — V(n,t) extension dies; paper Sec 4 promoted, Sec 5 retracted |
| −0.6 < w_a < −0.1 | weak FAIL or INCONCLUSIVE A | PASS B | **Strongest SQT outcome** — extension confirmed |
| w_a ≈ −0.7 to −1.0 | FAIL A | INCONCLUSIVE B → PASS B (weak) | Compatible with SQT-ext at 2σ; Λ-static dead |
| w_a > +0.1 or w_a < −1.5 | FAIL A | FAIL B | **Both branches falsified — SQT killed at the BAO-CPL level** |

Pre-committing to this matrix is the entire point of the document. None of the bands can be moved post-release.

---

## 4. Inconclusive band — explicit definition

DR3 may release with σ(w_a) at the upper end of the 0.10 – 0.18 range, in which case both PASS B (weak) and INCONCLUSIVE A windows may overlap. We define "inconclusive" precisely so that we cannot retroactively claim a pass:

> **Inconclusive ≡** the DR3 central w_a is consistent with both (w_a = 0) and (w_a = −0.3) at less than 2σ_tot, AND its 95% CI spans both predictions.
>
> Under inconclusive, neither tier may be reported as confirmed; the paper must explicitly state "DR3 does not discriminate" and defer to DR4 / Euclid-BAO joint.

---

## 5. Supporting locked predictions (must travel with w_a in the same preprint)

For pre-registration to be meaningful, the *full set* of correlated SQT geometry predictions must be timestamped together. Otherwise a selective post-hoc claim on w_a alone would still be possible.

1. **w_0 prediction:** w_0^Tier-A = −1.000, w_0^Tier-B = −0.95 ± 0.03. Same PASS/FAIL grammar as w_a.
2. **H_0 expectation under each tier:** Tier A reproduces Planck H_0 ≈ 67.4 km/s/Mpc (no resolution); Tier B does not resolve H_0 tension either (μ_eff ≈ 1, structural). This is the honest negative — ruling out the post-hoc claim "SQT predicted high H_0".
3. **CPL ellipse orientation:** SQT-ext predicts w_0–w_a ellipse principal axis in the (−1, 0) → (−0.95, −0.30) direction. Pre-register the predicted slope dw_a/dw_0 ≈ +6 ± 2 along the SQT trajectory.
4. **Ω_m anti-correlation:** Tier B prefers Ω_m ≈ 0.31 ± 0.02. Anything outside 0.27–0.35 from DR3 is a separate FAIL flag.

---

## 6. Pre-registration mechanism (operational)

Three independent timestamps to make pre-registration unimpeachable:

1. **OSF (Open Science Framework) registration** — text of Sec 3 + Sec 4 of this doc, frozen, with SHA-256 hash of the file contents. OSF auto-timestamps and prevents post-hoc modification.
2. **arXiv preprint** — JCAP-target manuscript with Sec 7 explicitly titled "Pre-DR3 falsifiable prediction"; submission date ≥ 2 weeks before DR3 expected release window.
3. **Public Git tag** — `v1.0-preDR3-prereg` on the SQMH repo, signed commit, pushed to GitHub (third-party timestamp).

All three must occur before any DR3 internal-collaboration leak window. Internal SQMH documents (this folder included) **do not** count as pre-registration on their own — only the external timestamps do.

---

## 7. Risk register (8-person independent vote)

| Persona | Primary concern | Suggested mitigation |
|---------|-----------------|----------------------|
| Information-theorist | DR3 σ underestimated → false PASS | Use σ_DR3 *as released*, not forecast; recompute boundaries on release day before reading w_a |
| Experimentalist | DESI may release multiple combinations (BAO-only, +SN, +CMB) | Lock prediction against all three combinations separately; pre-register which is "primary" (BAO+CMB joint) |
| Bayesian | Tier B 1σ band 0.15 is theory-prior, not posterior | State explicitly in Sec 3 that 0.15 is a slow-roll bound, not a measurement uncertainty |
| Risk officer | Inconclusive band lets us escape falsification | Inconclusive must trigger "deferred verdict", not "consistent" — wording matters |
| Phenomenologist | w_0 and w_a correlated; treating independently double-counts | Use joint χ² in CPL plane, not 1D w_a alone, as primary statistic |
| Theorist | V(n,t) extension not yet independently derived | L327 must complete derivation before this preprint; otherwise Tier B is fitted not predicted |
| Reviewer simulator | "Pre-registration" claim will be scrutinized; arXiv timestamp + OSF both needed | Comply with both, mention in cover letter |
| Honest broker | If DR3 is inconclusive, paper has no result — accept this | Sec 8 of paper must state "deferred to DR4" gracefully |

**Consensus:** Pre-register Tier A and Tier B simultaneously with the joint outcome matrix; require σ_tot recomputation on DR3 release using DR3-quoted σ; do not claim "prediction" for Tier B unless L327 V(n,t) derivation completes first.

---

## 8. Stop conditions

Halt the pre-registration push if any of the following:

- L327 V(n,t) derivation does not converge to a single-parameter family (Tier B becomes unconstrained → not pre-registerable).
- DESI announces DR3 release date < 2 weeks out (insufficient time to OSF + arXiv + Git timestamp cleanly; pre-register Tier A only).
- Internal SQMH ξ_q sign or μ_eff structure shifts during L328–L337 (would invalidate the locked bands).

---

## 9. Single-paragraph directive

Lock Tier A (w_0=−1, w_a=0, exact) and Tier B (w_0=−0.95±0.03, w_a=−0.30±0.15) with the joint outcome matrix in §3, supported by §5 correlated predictions, via the three-channel timestamp mechanism in §6, before DESI DR3 unblinding. Do not move any band post-release. If DR3 falls in the explicit inconclusive band, report "deferred", not "consistent".
