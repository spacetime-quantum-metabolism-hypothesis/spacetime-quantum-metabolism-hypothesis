# L338 — 8-Person Review of P17 Pre-Registration

**Date:** 2026-05-01
**Loop:** 245
**Documents reviewed:** ATTACK_DESIGN.md, PRE_REGISTRATION.md, NEXT_STEP.md (L338).
**Rule:** Independent 8-person review (Rule-A, theory-claim level). Self-assigned focus, no role pre-allocation.

---

## 1. Reviewer 1 — Information theorist (focus: D_KL accounting)

- §3 outcome matrix correctly separates PASS A (which is *also* a PASS for ΛCDM) from PASS B (genuine SQT-ext support). Good.
- σ_tot construction √(σ_DR3² + 0.15²) is the right combination only if the 0.15 is treated as a Gaussian theory prior. **Caveat needed:** the slow-roll bound is more box-like than Gaussian. Acceptable but should be stated. *(Now stated in PRE_REGISTRATION §5.)*
- Inconclusive band 2σ_tot < |·| ≤ 3σ_tot is generous to SQT. Suggest noting that under inconclusive we *cannot* take credit for "near miss". Document does so. PASS.

**Verdict:** Accept.

## 2. Reviewer 2 — Experimentalist (focus: DESI release format)

- DR3 will likely release at least three combinations. Document correctly pre-commits "primary = BAO+CMB joint". Good.
- Concern: DESI may quote w_a in a non-CPL parametrisation (e.g., w_φ(z) basis). If so, decision rules need an explicit translation rule. **Recommend adding** to §3 of PRE_REGISTRATION: "If DR3 does not quote CPL (w_0, w_a) directly, we will reproject onto CPL using the published w(z) at z=0 and z→∞ before applying §4". *(Adopted as §3 footnote — see NEXT_STEP item 2.)*
- σ_DR3 range 0.10 – 0.18 is reasonable; actual likely 0.12 – 0.15.

**Verdict:** Accept with §3 amendment.

## 3. Reviewer 3 — Bayesian (focus: prior vs posterior framing)

- Tier B 1σ = 0.15 is correctly framed as a theory prior, not a posterior. PRE_REGISTRATION §2 and §5 both state this explicitly. Good.
- Recommend a Bayes-factor side-calculation as a *secondary* statistic: B(Tier A vs Tier B | DR3) for completeness. Not a decision criterion. *(Add to NEXT_STEP as optional L339 item.)*
- The "5σ if |w_a| > 0.6" line from L326 is correctly *not* repeated in PRE_REGISTRATION (it would conflate prior and data σ). Good catch.

**Verdict:** Accept.

## 4. Reviewer 4 — Risk officer (focus: escape-hatch detection)

- Inconclusive band is the highest-risk feature. Document defines it tightly (must overlap *both* predictions at <2σ_tot AND 95% CI spans both). This blocks the standard escape pattern. Good.
- §4.5 correlated FAIL flags (Ω_m, slope, w_0) prevent selective w_a-only reporting. Good.
- **Strongest concern:** §6 commitment "publish verdict within 30 days of DR3 release" should be even stricter. 30 days lets us see the community reaction. Suggest 14 days. **Reject as written; tighten to 14 days.** *(Adopted in NEXT_STEP item 5.)*

**Verdict:** Accept with timing tightening.

## 5. Reviewer 5 — Phenomenologist (focus: correlated geometry)

- Joint w_0–w_a treatment is correct (§4.5 separate FAIL flags + recommended joint χ² in attack design §7). Good.
- Tier B slope prediction dw_a/dw_0 ≈ +6 ± 2 needs a derivation reference. Currently sourced in L327; if L327 doesn't pin it, this number becomes unjustified. **Hard dependency on L327.**
- Ω_m band 0.27–0.35 is wide; probably fine but should we tighten to 0.29–0.33? Decision: keep wide — Tier B has genuine slow-roll Ω_m freedom; tightening would over-claim.

**Verdict:** Accept conditional on L327.

## 6. Reviewer 6 — Theorist (focus: V(n,t) derivation status)

- **Critical issue:** PRE_REGISTRATION Tier B is conditional on L327 V(n,t) producing a single-parameter family. Currently L327 is teed up but not complete. Per CLAUDE.md 최우선-2 (team derives independently), we must not import the V(n,t) form here.
- §8 of PRE_REGISTRATION correctly states the conditional. Good.
- **Hard requirement:** L327 must produce derivation, hash it, link from PRE_REGISTRATION before timestamping. If L327 fails, freeze Tier A only.

**Verdict:** Accept with hard L327 dependency.

## 7. Reviewer 7 — Reviewer simulator (focus: how this looks to JCAP referees)

- "Pre-registration" claim will be checked. Three-channel timestamp (OSF + arXiv + signed Git) is the right level of seriousness. Good.
- Section 5 ("What this document does NOT claim") is unusual but exactly right — referees will appreciate the explicit honesty about H_0 and S_8 non-resolution.
- Suggest adding to PRE_REGISTRATION cover paragraph: "No author has accessed pre-release DR3 data; the bands are derived from L0–L2 axioms and L327 V(n,t) derivation only." *(Adopted in NEXT_STEP item 4.)*

**Verdict:** Accept with cover affirmation.

## 8. Reviewer 8 — Honest broker (focus: what we may have to retract)

- §6 item 5 ("If FAIL on both tiers: retract SQT BAO-CPL claims") is the hardest commitment in the document. It must stay. Confirmed.
- The "deferred to DR4" inconclusive outcome is the most likely actual result given DR3 σ ~ 0.15. Need to be honest that this is the modal expected outcome — not a victory.
- Suggest amending §1 to read "intent: lock predictions and accept any of {pass, fail, deferred} as legitimate outcomes". *(Adopted as a one-line clarification in §1 of PRE_REGISTRATION pre-timestamp edit.)*

**Verdict:** Accept with §1 honesty clarification.

---

## Consensus

8/8 accept the documents, with the following amendments to be applied **before** OSF/arXiv timestamping:

1. (Reviewer 2) Add CPL reprojection footnote to PRE_REGISTRATION §3.
2. (Reviewer 4) Tighten 30-day → 14-day verdict publication commitment in PRE_REGISTRATION §6.
3. (Reviewer 6) Hard-block timestamp until L327 V(n,t) derivation hash is available.
4. (Reviewer 7) Add no-pre-release-access affirmation to PRE_REGISTRATION cover.
5. (Reviewer 8) Add modal-expectation honesty clarification to PRE_REGISTRATION §1.

These five amendments are mechanical and do not require an additional 8-person review. After they land, the documents are ready for the three-channel timestamp protocol.

---

## Open issues for L339+

- L327 V(n,t) derivation (hard dependency).
- L339 optional Bayes factor secondary-statistic spec.
- L340 σ_DR3 sensitivity sweep: how the §4 boundaries shift across σ_DR3 ∈ {0.10, 0.13, 0.15, 0.18}.
- DESI DR3 release-date monitoring (no internal-data exposure).
