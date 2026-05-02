# L326 — Next Step

**From:** L326 falsifier KL ranking (ATTACK_DESIGN.md)
**Decision:** ratify P17 → P21 → P19 → P15 priority and execute pre-registration sequence.

---

## Immediate (next loop, L327)

1. **Draft P17 pre-registration block** for arXiv preprint Sec 4 / 7:
   - Explicit w_a band: PASS −1.0 < w_a < −0.4; FAIL outside.
   - Lock SQT extension assumption (V(n,t)) and required parameter values *before* DR3 unblinding.
   - Insert "submitted YYYY-MM-DD, prior to DESI DR3 release" timestamp claim into Sec 7.
2. **Insert P19 + P21 structural prediction** (+1.14% S_8) into Sec 4.4 as a *risky* prediction, with explicit FAIL band: |S_8,obs − S_8,Planck − 0.011| > 0.005 falsifies SQT at >3σ.
3. **Drop P18 and downgrade P16** in Sec 7 outlook table — be honest that 5 of 8 forward channels are decisive, 3 are not.

## Short-term (L327–L335)

4. **L327** — write the SQT V(n,t) extension explicitly so P17 prediction is reproducible. Independent derivation (no equation imports from L284).
5. **L328** — Fisher matrix recompute D_KL with realistic DR3 covariance (ask DESI white paper σ values, not forecast guesses).
6. **L329** — Euclid DR1 (2026 Q3?) data drop preparation: SQT vs LCDM χ² pipeline frozen now.
7. **L330** — LSST DC2 sim S_8 mock pipeline: verify SQT really predicts +1.14% under realistic survey selection.

## Mid-term (DR3 window, late 2026)

8. **DR3 unblinding** → P17 verdict. If PASS: paper Sec 4.1 promoted to "confirmed prediction"; if FAIL outside band: theory section 6 reorganised, retract w_a claim, retain Branch B core.
9. **L335+** — paper resubmission after DR3 outcome.

## Avoid

- New BAO standalone scans without single-point validation (CLAUDE.md L33 rule).
- Adding parameters to chase σ_8 — it is structurally unfixable at μ_eff ≈ 1.
- Calling P17 a "prediction" if extension V(n,t) is fitted post-DR3.

---

## Single-line directive

**Lock pre-registration of P17/P19/P21 in the JCAP preprint before DESI DR3 release; treat P15 as the only remaining mid-term mission-grade test; drop P18 and demote P16.**
