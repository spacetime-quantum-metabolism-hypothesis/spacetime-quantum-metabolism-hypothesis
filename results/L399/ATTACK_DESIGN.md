# L399 ATTACK DESIGN — Appendix A (mock injection + bootstrap + sensitivity)

Independent session. Honest one-liner: Appendix A is a *consolidation* of L272 / L275 /
L277 / L278 / L279 / L280 into one self-contained robustness appendix; no new numbers
are produced here, and L272's CRITICAL finding (Branch B 100% false detection on LCDM
mocks under data-driven tertile split) must remain visible — it is *not* re-spun.

## Goal
Draft the outline for paper Appendix A. The appendix collects every robustness
diagnostic already executed across L272–L280 and presents them in a single coherent
narrative around four claims:

1. **Mock injection-recovery (L272)** — measures false-positive rate of Branch B
   3-regime detection on simulated LCDM data.
2. **Prior sensitivity (L275)** — quantifies posterior MAP shift across 4 prior
   combinations.
3. **Posterior predictive checks (L277)** — KS / coverage / dispersion vs SPARC
   replicated data.
4. **Jackknife + bootstrap + SBC (L278 / L279 / L280)** — leave-one-out leverage,
   anchor-bootstrap CI, simulation-based calibration of posterior coverage.

## Attack lines

### A. Mock injection (Appendix A.1, source = L272)
- L272 finding: **N=200 LCDM mocks → 200/200 false BB preference, median ΔAICc = 132.95**.
- Attack 1: reviewer reads A.1 as "BB rejected by mock". Mitigation: A.1 must
  state up-front that the mocks use **data-driven tertile split** (worst-case
  overfitting probe), and that the L272 conclusion is *conditional* on whether
  σ_0 anchors are theory-prior vs data-fit.
- Attack 2: mock seed dependence. Mitigation: report seed range used, note that
  the false-rate result is seed-insensitive at this magnitude (132.95 ≫ AICc
  noise floor).
- Attack 3: anchor-fixed re-mock missing. Acknowledge as future work; the L272
  REVIEW already flags this as the resolution path.

### B. Prior sensitivity (Appendix A.2, source = L275)
- L275 finding: max MAP shift across 4 priors = **0.045 dex ≪ 0.3 dex threshold**.
  Cluster anchor is mildly prior-sensitive (single A1689).
- Attack 1: reviewer asks for log-uniform vs uniform comparison. Already covered
  by L275's 2×2 grid.
- Attack 2: anchor inflation x2 — covered.
- Honest framing: A.2 is the strongest robustness panel (prior-robust at the
  0.05-dex level).

### C. Posterior predictive checks (Appendix A.3, source = L277)
- L277 finding: KS p = 0.18 (PASS), 90% PI coverage 87% (marginal), std
  underdispersion ~8%.
- Attack 1: 87% < 90% nominal — must state "marginal overconfidence" honestly,
  not paper over.
- Attack 2: tail / outlier galaxies (L204 outlier list) — A.3 should cite L204
  outlier list and note the 8% underdispersion is consistent with that.

### D. Jackknife (Appendix A.4, source = L278)
- L278 finding: max per-galaxy leverage **< 5%**, top-5 removal ΔAICc shift = -7
  (still BB-preferred), Q=1 only subset ΔAICc(LCDM-BB) = 78 vs full 99.
- Attack 1: Q=1 subset weakening — disclose; do not bury.
- Attack 2: high-mass / late-type strata — A.4 lists these as *not yet executed*;
  flag as Appendix-A scope limitation.

### E. Bootstrap anchors (Appendix A.5, source = L279)
- L279 finding: 1000-bootstrap CIs match Hessian within 5%; cluster anchor
  remains the weakest (single A1689, ±0.15 in log).
- Attack: cluster anchor — already noted in L279 REVIEW. A.5 should explicitly
  request additional cluster anchors as the obvious follow-up.

### F. Simulation-based calibration (Appendix A.6, source = L280)
- L280 finding: rank-uniformity KS p ∈ {0.34, 0.21, 0.41} (all PASS); 68% coverage
  67–71%; 95% coverage 93–96%.
- Attack 1: only 100 SBC rounds (1000 recommended). A.6 must disclose this and
  flag it as a budget-limited result, *not* a posterior-quality conclusion.

## Integration narrative (Appendix A.0, intro paragraph)
The six diagnostics are *not* independent: L277 PPC + L280 SBC are linked
(coverage 87% → 93% as one moves from PPC to SBC-rank — anchor-vs-posterior
calibration consistent). L272 is the **single critical caveat** and is reported
as such; L275/L278/L279/L280 are PASSes that establish robustness *given* the
L272 anchor-prior caveat is honored in the main text.

## Anti-spin discipline (carry-over from CLAUDE.md L5/L6)
- Do **not** present L272 as resolved.
- Do **not** claim "mock validation passed" — the mocks **failed** under
  data-driven anchors; passes are conditional.
- Do **not** rephrase the 0.045 dex prior shift as "stable" without numerical
  context.
- Companion-paper hedge (Sec 7.3 / L396) applies: Appendix A is the falsifiable
  evidence layer; if PRD/JCAP referee challenges BB's ΔAICc, Appendix A is what
  they audit.

## Non-goals
- No new simulations. No re-runs. No re-fits.
- No revision of headline ΔAICc = 99 from L208.
- No claim that S_8 / K15 robustness is in scope (L6 rule: structurally
  unaddressable in background-only fits).

## Output structure
- ATTACK_DESIGN.md (this file) — plan only.
- REVIEW.md — adversarial review against CLAUDE.md rules and L5/L6 carry-overs.
- APPENDIX_OUTLINE.md — final Appendix A outline (A.0 intro through A.6 SBC,
  plus A.7 limitations & open robustness items).
