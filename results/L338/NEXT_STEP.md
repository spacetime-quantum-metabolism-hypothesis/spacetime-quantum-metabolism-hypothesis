# L338 — Next Step

**From:** L338 P17 pre-registration design + 8-person review.
**Decision:** Adopt the two-tier (Λ-static + V(n,t)-extended) pre-registration with explicit PASS/FAIL/INCONCLUSIVE bands; apply the five mechanical review amendments; gate timestamp on L327.

---

## Immediate (next loop, L339)

1. **Apply 5 review amendments to PRE_REGISTRATION.md** (mechanical, no new physics):
   a. CPL reprojection footnote in §3 (Reviewer 2).
   b. Tighten verdict publication 30 → 14 days in §6 (Reviewer 4).
   c. Hard-block on L327 V(n,t) hash in §7 (Reviewer 6).
   d. No-pre-release-access affirmation in cover (Reviewer 7).
   e. §1 modal-expectation honesty clarification (Reviewer 8).
2. **L327 status check** — confirm V(n,t) derivation is complete and produces a single-parameter family. If incomplete, defer Tier B from pre-registration; freeze Tier A only and label Tier B as "post-DR3 exploratory test".
3. **Compute SHA-256 of frozen ATTACK_DESIGN.md and PRE_REGISTRATION.md** and record in §7 of PRE_REGISTRATION.

## Short-term (L339–L345)

4. **L339** — Bayes-factor side calculation B(Tier A vs Tier B | DR3 mock) as secondary statistic (not decision rule). Reviewer 3 request.
5. **L340** — σ_DR3 sensitivity sweep at σ ∈ {0.10, 0.13, 0.15, 0.18}: tabulate how PASS/FAIL boundaries shift; verify decision rules degrade gracefully.
6. **L341** — Pre-flight CPL reprojection script: given any DESI w(z) parametrisation, produce (w_0, w_a) under the locked CPL convention. Single-point validated against a known LCDM mock.
7. **L342** — DR3-readiness checklist: data ingestion paths, covariance matrix extraction, joint χ² recomputation script frozen.
8. **L343** — JCAP manuscript Sec 7 "Pre-DR3 falsifiable prediction" final draft incorporating these documents verbatim (with hashes).
9. **L344** — OSF registration submission (does not require external review).
10. **L345** — arXiv preprint submission + signed Git tag `v1.0-preDR3-prereg`.

## Mid-term (DR3 release window, late 2026)

11. **DR3 release day** — read primary BAO+CMB combination first; record w_a^DR3, σ_DR3, w_0^DR3, Ω_m^DR3.
12. **DR3 + 14 days** — publish verdict applying §4 of PRE_REGISTRATION verbatim. PASS, FAIL, or INCONCLUSIVE.
13. **DR3 + 30 days** — paper resubmission to JCAP with verdict; if FAIL on both tiers, retract Sec 4.1 + Sec 5 BAO-CPL claims and reorganise around remaining channels (P19, P21, P15).

## Avoid

- Do **not** look at any pre-release DR3 data, even informally, before timestamping is complete.
- Do **not** widen Tier B 1σ from 0.15 post-release to make a near-miss "pass".
- Do **not** drop the CPL slope or Ω_m correlated FAIL flags — they prevent selective w_a-only reporting.
- Do **not** treat Tier A PASS as SQT support; Tier A PASS is identical to ΛCDM and means V(n,t) extension is dead.
- Do **not** import V(n,t) form from this document into L327; L327 must derive independently per CLAUDE.md 최우선-2.

---

## Single-line directive

**Apply the 5 review amendments, gate on L327 V(n,t) completion, then timestamp ATTACK_DESIGN.md + PRE_REGISTRATION.md via OSF + arXiv + signed Git tag before any DESI DR3 unblinding.**
