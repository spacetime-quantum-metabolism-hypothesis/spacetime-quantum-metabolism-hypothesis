# L400 — Final-Round Referee Response (Template)

**Loop**: L400 (independent)
**Target journal**: JCAP
**Submission**: SQMH/SQT, second revision
**Date**: 2026-05-01
**Predecessor**: L320 first-round response template
**정직 한 줄**: L320 first-round 응답을 모두 계승하며, L342~L391 의 신규 회복(L342/L350/L360/L370/L380/L385/L388/L389/L390)과 신규 한계를 reviewer 별 추가 응답 항목으로 모두 정직하게 반영한다. 결과 수치가 미확정인 항목은 placeholder 로 명시한다.

---

## Cover note to the editor

We are grateful for the opportunity to submit the second revision. Since the first round (responses recorded in L320), we have completed nine internal investigations (L342, L350, L360, L370, L380, L385, L388, L389, L390) that strengthen several defenses while honestly exposing additional limitations. Each new investigation is mapped one-to-one to a referee channel below. Where a quantitative result is still being finalized for the companion paper (L370), we have inserted an explicit placeholder rather than promotional language. We hope the editor finds the honesty-first treatment consistent with JCAP's standards.

---

## Referee 1 — Theorist (final round)

We thank Referee 1 again for the careful first-round critique. The first-round responses (R1.1–R1.4) are retained from L320 unchanged; we summarise them briefly below and add four new responses (R1.5–R1.8) addressing concerns that arose from internal investigations after first submission.

### Carry-over (L320 condensed)

- **R1.1 (D5 phenomenological status)**: Sec 4.2 rewritten — D5 explicitly labeled phenomenological; n is fixed by SPARC and not refit per analysis.
- **R1.2 (RG cubic coefficients)**: Sec 5.1 paragraph delimits tree-level domain, defers loop calculation, removes axiomatic-determination language.
- **R1.3 (frame ambiguity)**: Sec 3 clarification — Jordan-frame observables, Bekenstein/ZKB equivalence cited.
- **R1.4 (recommendation)**: pillars-vs-phenomenology separation completed.

### New (final round)

**R1.5 — Holographic CKN saturation as a consistency check, not a prediction (L385)**

We have added Sec 5.4 (and Appendix F) reporting the saturation ratio r(L) = n_∞ / n_max(L) at four scales (lab, AU, kpc, Hubble). The result we report is:

> "At L = R_H = c/H_0 the saturation ratio is of order unity. At sub-Hubble scales (lab, AU, kpc) the ratio is many orders of magnitude below unity. We therefore do *not* claim that SQT predicts the observed Λ from the CKN bound. We claim only that, given Λ_obs as input, the SQT asymptotic n_∞ is consistent with the CKN ceiling at the cosmological scale and severely under-saturates it at smaller scales. This is a post-dictive consistency check, not a derivation of Λ_obs."

This framing pre-empts the circularity concern and is recorded honestly in the limitations section.

**R1.6 — c-coefficient closure status at 2-loop (L388)**

Following the referee's loop-calculation request (L320 R1.2), we attempted a 2-loop n self-energy / setting-sun analysis (L388). [PLACEHOLDER: insert L388 conclusion when 8-person team consensus is finalized — current draft text:]

> "At 2-loop the c-coefficient remains a free EFT parameter; the setting-sun topology produces no symmetry-protected fixed value beyond the counterterms required at 1-loop. We therefore report c as a Wilsonian truncation parameter and do not claim first-principle closure. The number of free parameters is updated in Table 1 accordingly."

If the L388 final consensus differs (i.e. closure is achieved or partially achieved at 2-loop), the response above will be revised before resubmission; the current honest framing assumes the most adversarial outcome.

**R1.7 — BRST diffeomorphism gauge invariance, verified order (L389)**

We have added Appendix G reporting the BRST nilpotency check on the SQMH action up to graviton order [PLACEHOLDER: insert L389 verified order]. Unverified orders are flagged as future work. We do not claim full-order BRST consistency and explicitly delimit the verified order in the abstract.

**R1.8 — Conformal anomaly contribution to Λ_eff (L390)**

We have evaluated the n-field contribution to the conformal anomaly trace ⟨T^μ_μ⟩ via heat-kernel a_2 / Seeley-DeWitt expansion (L390). [PLACEHOLDER: insert L390 numerical conclusion]. If the contribution to Λ_eff is non-zero at the level relevant for D2 (FLRW background), we will revise the D2 pillar text to state explicitly that the FLRW background is anomaly-corrected; if the contribution is negligible at the relevant scale, we will state that explicitly. Either outcome is recorded honestly.

---

## Referee 2 — Observer (final round)

We thank Referee 2 again. R2.1–R2.4 (L320) are retained; new responses R2.5–R2.8 address concerns that arose from investigations of cluster systematics and cross-dataset universality.

### Carry-over (L320 condensed)

- **R2.1 (SPARC residual detail)**: Appendix C added — per-galaxy χ² histogram, 11 outliers identified, MOND/NFW side-by-side.
- **R2.2 (S_8 1% worsening)**: Sec 6.4 honest concession — background-only μ_eff ≈ 1 cannot reduce S_8 tension; we do not claim solution.
- **R2.3 (DESI DR2 13-pt covariance)**: Sec 5.3 clarified.
- **R2.4 (μ_eff ≈ 1 / RSD)**: Sec 5.5 — RSD is a tie not a win.

### New (final round)

**R2.5 — PSZ2 cluster σ vs lensing-selected σ (L350)**

We have added Appendix C.2 reporting the consistency of the cluster σ_cluster anchor between Planck PSZ2 and a lensing-selected cluster sample, with hydrostatic mass bias (1−b) propagated. [PLACEHOLDER: insert L350 result — KS / Anderson-Darling / hierarchical posterior overlap, deconvolved selection function]. If the two samples are inconsistent at >2σ, the cluster anchor uncertainty is broadened in Sec 4.3 and the σ(ρ) non-monotonicity claim (R3.5) is correspondingly weakened. We have committed to reporting the outcome regardless of direction.

**R2.6 — Cross-dataset universality of σ_0 via Q_DMAP (L360)**

We have added Sec 7.4 reporting Q_DMAP (Raveri-Doux 2021) for the three pair-wise comparisons (SPARC vs DESI, SPARC vs Planck-compressed, DESI vs Planck-compressed). [PLACEHOLDER: insert L360 result]. We adopt the standard threshold: Q_DMAP > 5 → severe tension, > 3 → caution, < 2 → consistent. If any channel exceeds 3, we will explicitly concede that SQT σ_0 is *not* cross-scale universal at present and the SPARC-fit σ_0 vs cosmological-fit σ_0 will be reported as separate parameters. This outcome will be reported as a partial falsification, not hidden.

**R2.7 — V(n,t) thawing toy quantitative consistency with DESI (L380)**

We have added Sec 5.6 reporting the χ² of the V(n,t) thawing toy (V = V_0 + ½ m_n² n²) against the DESI DR2 13-point BAO with full covariance. [PLACEHOLDER: insert L380 χ² and best-fit (Ω_m, h, μ=m_n/H_0, n_i)]. The current statement is conservative:

> "The V(n,t) toy reproduces the *sign* of DESI's reported (w_0, w_a). The amplitude consistency is reported as a χ² with full covariance; we do not claim quantitative match where it is absent."

If the amplitude does not match within the joint covariance, we say so explicitly. The toy's role is structural plausibility, not amplitude prediction.

**R2.8 — S_8 worsening as systematic vs isolated regression (L342 + L360)**

The referee's first-round R2.2 concern is sharpened by the L342 σ(ρ) non-monotonicity result and the L360 Q_DMAP analysis. We address this as follows in Sec 6.4:

> "The 1% S_8 worsening is *structural*: it reflects the fact that SQMH is a background-modifying theory at the linear level (μ_eff ≈ 1, GW170817-anchored). It is not a tuning artifact, and it persists across the σ(ρ) anchor analysis. We do not claim S_8 resolution. The L360 Q_DMAP analysis tests whether σ_0 itself is cross-scale universal; the S_8 worsening is logically independent of that test."

This is the honest framing.

---

## Referee 3 — Statistician (final round)

We thank Referee 3 again. R3.1–R3.4 (L320) are retained; new responses R3.5–R3.8 address concerns about additional model-selection metrics, cross-dataset tension calibration, and reproducibility.

### Carry-over (L320 condensed)

- **R3.1 (anchor mock null distribution)**: Appendix D expanded — 2000 mocks, p < 5×10⁻⁴.
- **R3.2 (ΔAICc=99 vs ΔlnZ=0.8)**: Abstract + Sec 7.1 rewritten — fixed-θ vs marginalized clearly separated; headline reframed to falsifiability.
- **R3.3 (false-detection rate)**: Appendix E added — Monte Carlo over 5000 random 2-parameter DE phenomenologies; fraction with ΔAICc ≥ 99 is < 0.1%.
- **R3.4 (LOO-CV)**: Appendix D.3 — stable across BAO bins, SN compilations, RSD points.

### New (final round)

**R3.5 — σ_0(ρ_env) non-monotonicity model selection at N=3 (L342)**

We have added Sec 4.3 / Appendix D.4 reporting model selection between H0 = monotonic σ(ρ) and H1 = non-monotonic σ(ρ) using the three anchors (cosmic, cluster, galactic). At N=3, AICc is undefined for k=3. We therefore report BIC + Bayes factor + Δχ² simultaneously, following the referee's own statistical-rigor standard. [PLACEHOLDER: insert L342 BIC / Bayes factor / Δχ²]. The 3-regime extension is held in reserve until additional anchors (e.g. P11 NS forecast) are available, as recommended by the L332 internal review. We explicitly do not claim "decisive" non-monotonicity at present.

**R3.6 — Q_DMAP sensitivity to posterior non-Gaussianity (L360)**

Q_DMAP (Raveri-Doux 2021) is robust to non-Gaussian posteriors but not insensitive. In Appendix D.5 we report a sensitivity analysis: re-evaluating Q_DMAP under (i) marginal-Gaussian approximation, (ii) full non-Gaussian posterior (nested sampling). [PLACEHOLDER: insert L360 sensitivity result]. If the two estimators disagree by more than the threshold gap (e.g. crossing 3 vs 2), we report both numbers and adopt the more conservative.

**R3.7 — Effect of additional free parameters on marginalized evidence (L385 + L388)**

The first-round R3.2 distinction between fixed-θ ΔAICc and marginalized ΔlnZ is preserved. The L385 holographic-bound check does *not* add free parameters (it is a consistency check with Λ_obs as input). The L388 2-loop analysis [PLACEHOLDER: confirm L388 conclusion] indicates that c remains a free Wilsonian parameter, which we already counted in the marginalized evidence. We have re-run the marginalized-evidence calculation with the updated parameter count and report:

> "[PLACEHOLDER: updated ΔlnZ value]. The qualitative conclusion of R3.2 — that the Bayesian evidence does not yet justify the additional parameters in a strong sense — is unchanged. The headline remains falsifiability rather than Bayesian preference."

**R3.8 — Reproducibility channel and the companion paper (L370)**

To address the volume of methodological detail that would otherwise burden the main text (numerical integration conventions, 5-dataset χ² combination, cluster-pool SVD/participation-ratio analyses), we have prepared a companion paper outline (L370) covering Sec 1–5 of the methods. The companion paper will be posted to arXiv simultaneously with the main submission and explicitly cross-referenced in the reproducibility statement. Method-level referee questions are routed to the companion; the main paper retains theory + falsifiable results.

---

## Summary of revisions (final round)

| Reviewer | New concern (origin) | Resolution |
|----------|----------------------|------------|
| R1 | A1.5 CKN saturation circularity (L385) | Sec 5.4 + App F: consistency check, not prediction |
| R1 | A1.6 2-loop c closure (L388) | [PLACEHOLDER]: Wilsonian framing |
| R1 | A1.7 BRST verified order (L389) | App G: explicit order, future work flagged |
| R1 | A1.8 Conformal anomaly contribution (L390) | [PLACEHOLDER]: D2 text update if non-zero |
| R2 | A2.5 PSZ2 vs lensing-selected (L350) | App C.2: [PLACEHOLDER] result, anchor uncertainty |
| R2 | A2.6 Q_DMAP cross-dataset (L360) | Sec 7.4: [PLACEHOLDER], partial falsification reported if found |
| R2 | A2.7 V(n,t) DESI quantitative (L380) | Sec 5.6: [PLACEHOLDER] χ², sign-vs-amplitude split |
| R2 | A2.8 S_8 systematic vs isolated (L342+L360) | Sec 6.4: structural framing |
| R3 | A3.5 σ(ρ) non-monotonicity at N=3 (L342) | Sec 4.3 + App D.4: BIC + BF + Δχ² |
| R3 | A3.6 Q_DMAP sensitivity (L360) | App D.5: [PLACEHOLDER] sensitivity |
| R3 | A3.7 Marginalized evidence with new free params (L385+L388) | Updated ΔlnZ [PLACEHOLDER] |
| R3 | A3.8 Companion-paper reproducibility (L370) | Cross-reference + simultaneous arXiv |

**Headline (unchanged from L320 + reinforced)**: SQMH/SQT is a falsifiable phenomenology with pre-registered kill conditions. We do not claim Bayesian preference, S_8 resolution, or first-principle closure of the c-coefficient. The case for the theory rests on the seven (now expanded with K_holo / K_brst / K_anomaly) falsifiers and the post-dictive cross-scale consistency checks, openly conceding limitations where they exist.

**Honest disclosure of placeholders**: This response template is structurally complete but several quantitative results from L350, L360, L380, L388, L389, L390 are still being finalized by the internal 8-person review (Rule-A) at the time of writing. Numerical placeholders will be replaced before resubmission; qualitative framing of each placeholder is conservative, so any final result either confirms or weakens (never strengthens beyond) the stated claim.
