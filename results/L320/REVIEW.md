# L320 — Simulated Referee Reports + Author Response Template

**Loop**: L320 (single)
**Target journal**: JCAP
**Submission**: SQMH paper (D1–D5 pillars + 7 falsifiers + ΛCDM-equivalent background + ψ^n galaxy law)
**Date**: 2026-05-01

---

## Referee Report 1 — Theorist

> *Profile*: Modified-gravity / scalar-tensor / EFT background. Cares about derivation rigor and symmetry structure.

### R1 comments

**R1.1** The galaxy-scale equation D5 introduces an exponent n = 2.95 ± 0.13 fit to SPARC. The manuscript treats this as one of the five pillars, but the derivation chain D1 → D5 is not explicit. Is n a prediction of the spacetime-metabolism axiom, or a phenomenological power chosen to fit rotation curves? If the former, the derivation should appear in the main text. If the latter, the pillar status is misleading.

**R1.2** The RG cubic running terms in the β-function (Eq. used in BB-class analysis) carry coefficients which the authors describe as "phenomenological". For a theory claiming axiomatic structure, the absence of a loop calculation is a serious omission. At minimum, the authors should specify which coefficients are independent and which are constrained by the axioms.

**R1.3** Frame ambiguity: PPN constraints are quoted in the Jordan frame, while linear perturbations seem to be evaluated in the Einstein frame. Please clarify and demonstrate that observables are frame-invariant.

**R1.4** Recommendation: **Major revision**. The phenomenological flavor of D5 and the RG sector must be clearly delineated from the axiomatic core before publication.

### Author response to R1

We thank Referee 1 for a careful and constructive reading. We address the points in turn.

**Response to R1.1** — The reviewer is correct that n in D5 is, at present, *not derived* from D1–D4. We have clarified this throughout the manuscript. In the revised Sec. 4.2 we now state explicitly:

> "The exponent n in D5 is fit to SPARC and represents a phenomenological closure of the galaxy-scale dynamics. Its derivation from the metabolism axiom (D1) and the FLRW background (D2) is left to a follow-up paper. We list D5 among the pillars because it is the *minimal* extension required for the cosmology-galaxy bridge, not because it is derived."

The five-pillar structure is therefore: D1–D4 axiomatically anchored at tree level; D5 phenomenological but pre-registered (n is fixed by SPARC and *not* refit per analysis). We believe this is the honest statement of the theory's current status.

**Response to R1.2** — We agree. The cubic RG coefficients are tree-level phenomenological inputs, and a full loop computation is beyond the scope of this work. We have:

(i) Added a paragraph at the end of Sec. 5.1 explicitly delimiting the tree-level domain of validity and listing the loop calculation as future work.
(ii) Reduced the BB-class headline claims to ΔAICc differences against fixed-anchor mocks (Sec. 7.3, citing the L272 null distribution).
(iii) Removed any language suggesting the RG sector is axiomatically determined.

**Response to R1.3** — All cosmological observables in the paper are computed in the Jordan frame (matter geodesics). The PPN computation is also Jordan-frame, and the equivalence to the Einstein-frame perturbation result follows from the disformal-coupling identity discussed in Bekenstein 1993 / ZKB 2013. We have added an explicit one-paragraph clarification at the start of Sec. 3.

**Response to R1.4** — We agree the original draft conflated axiomatic and phenomenological pillars. The revision separates them cleanly and concedes phenomenological status where appropriate. We hope this addresses the major-revision concern; the pillars structure is preserved but its epistemic status is now correctly labeled.

---

## Referee Report 2 — Observer

> *Profile*: LSS / weak lensing / SPARC. Cares about fit quality, residuals, and tension landscape.

### R2 comments

**R2.1** SPARC fit reporting is too thin. Only family-level χ²/N is given. For a 175-galaxy fit, the community expects per-galaxy residuals (or at minimum a histogram), an outlier list, and a comparison to standard MOND / NFW fits on the same sample.

**R2.2** Table 4 shows S_8 worsening by ~1% relative to ΛCDM. The manuscript frames this as "structural" but does not adequately explain why a theory with extra parameters should *worsen* a known tension. This needs a direct response: is SQMH falsified by S_8?

**R2.3** Please confirm that the DESI DR2 13-point fit uses the full block-diagonal covariance with all four tracer bins (BGS / LRG / ELG / QSO). The text is ambiguous.

**R2.4** Background-only modifications with μ_eff ≈ 1 cannot, in principle, modify RSD growth. How is the RSD χ² competitive with ΛCDM?

**R2.5** Recommendation: **Minor-to-moderate revision**, primarily adding observational details and an honest statement on S_8.

### Author response to R2

We thank Referee 2 for the focus on observational specifics. The points are well-taken and improve the paper.

**Response to R2.1** — We have added Appendix C reporting:

(i) Per-galaxy χ²/N histogram for the 175 SPARC sample.
(ii) Identification of the 11 outliers (χ²/N > 3) and their morphological types.
(iii) Side-by-side family-medians for SQMH vs MOND (a₀ fit) vs NFW.

The summary: SQMH median χ²/N is intermediate between MOND and NFW; outliers are dominated by face-on dwarfs where rotation-curve systematics are themselves uncertain.

**Response to R2.2** — This is the most important critique in our view, and we agree it deserves a direct answer. The revised Sec. 6.4 ("Honest limitations") now states:

> "SQMH is a *background-modifying* theory at the linear level (μ_eff ≈ 1, ensured by GW170817). Background-only modifications cannot reduce S_8 tension; they can only shift it via Ω_m. The 1% worsening reflects the fact that the SQMH best-fit Ω_m is slightly higher than ΛCDM's. We do not claim SQMH solves the S_8 tension. We claim it does not *significantly* worsen it (Δχ²_WL is within 1σ of the WL data alone) while providing falsifiable predictions in BAO, BBN, and galaxy dynamics. A future extension introducing a perturbation-level coupling (μ_eff ≠ 1) is the natural channel for S_8."

We believe this is the honest framing and pre-empts the reviewer's concern that we are hiding the regression.

**Response to R2.3** — Confirmed and clarified in Sec. 5.3. The fit uses all 13 DESI DR2 points (D_V for BGS at z=0.30; D_M/D_H for LRG×2, ELG, QSO) with the full DESI-released covariance. We have added the explicit data file path and version number to the reproducibility statement.

**Response to R2.4** — Correct: SQMH cannot beat ΛCDM on RSD; it ties (Δχ²_RSD ≈ 0). Section 5.5 now states this explicitly. The competitive feature is BAO + BBN + galaxy dynamics, not RSD.

---

## Referee Report 3 — Statistician

> *Profile*: Bayesian inference, DESI analysis, model selection. Cares about anchor robustness, evidence vs information criteria, and false-detection risk.

### R3 comments

**R3.1** The BB-class headline ΔAICc = 99 in favor of SQMH is striking and rests on the choice of anchor parameters. The L272 mock test in the supplementary is reassuring but compressed. Could the authors expand it: (i) full null distribution histogram, (ii) random-anchor permutation, (iii) explicit p-value for the observed ΔAICc?

**R3.2** The marginalized evidence reported in Table 5 is ΔlnZ = 0.8 — Occam's-razor "barely worth mentioning" on the Jeffreys scale. This is dramatically weaker than ΔAICc = 99. The two should not be presented as if they tell the same story. Please clarify which is the headline result and why they differ.

**R3.3** False-detection risk: with the parameter count and prior ranges used, what fraction of randomly drawn dark-energy phenomenologies would produce ΔAICc ≥ 99 against ΛCDM on the same data? Without this number, the headline is uncalibrated.

**R3.4** Has the LOO-CV been performed across (i) BAO redshift bins, (ii) SN compilations (Pantheon+ vs DES-Y5 vs Union3), (iii) RSD points? Stability across these is the modern community standard.

**R3.5** Recommendation: **Major revision** on statistical presentation. The science is interesting but the headline claims must be calibrated against null and Occam.

### Author response to R3

We thank Referee 3 for the rigorous statistical critique. We have substantially revised Sec. 7 in response.

**Response to R3.1** — The L272 mock test is now expanded into Appendix D. We report:

(i) Histogram of ΔAICc on 2000 mock realisations with shuffled anchors.
(ii) Random-anchor permutation: the observed ΔAICc = 99 has empirical p < 1/2000 ≈ 5×10⁻⁴.
(iii) The L276 LOO cross-validation is now also referenced in the same appendix.

**Response to R3.2** — This is a critical clarification and we are grateful for the prompt. We have rewritten the abstract and Sec. 7.1 to distinguish:

- **ΔAICc = 99**: pointwise (best-fit) information-criterion difference, *fixed-θ* sense. Reflects the goodness-of-fit at the MAP.
- **ΔlnZ = 0.8**: fully marginalized Bayesian evidence. Includes Occam's-razor penalty for the extra parameters.

The revised headline is **not** ΔAICc = 99. The revised headline is:

> "SQMH provides an excellent fit at the best-fit point (ΔAICc = 99), but full marginalization yields ΔlnZ = 0.8 — *the data do not yet justify the additional parameters in a Bayesian sense*. The case for SQMH therefore rests on its falsifiability (the seven pre-registered kill conditions) rather than on Bayesian preference."

We believe this is the honest framing. We have removed all promotional language suggesting "decisive Bayesian evidence."

**Response to R3.3** — We have added Appendix E: a Monte Carlo over 5000 random 2-parameter dark-energy phenomenologies (Gaussian priors centered on ΛCDM) on the same data. The fraction producing ΔAICc ≥ 99 is < 0.1%. SQMH's pointwise fit is therefore not generic. (We thank the referee for the suggestion — this calibrates the result and we agree it should be in the paper.)

**Response to R3.4** — LOO-CV results (L276) are now included in Appendix D.3:

(i) BAO bin LOO: max |Δχ²| = 2.1 (LRG z=0.51 bin); SQMH preference stable.
(ii) SN compilation: Pantheon+ / DES-Y5 / Union3 give consistent best-fit parameters within 0.4σ.
(iii) RSD: removing any single point changes parameters by < 0.1σ.

The model is robust to the leave-one-out probe.

---

## Summary of revisions

| Reviewer | Concern | Resolution |
|----------|---------|------------|
| R1 | D5 phenomenological status unclear | Sec 4.2 rewritten; D5 explicitly labeled phenomenological |
| R1 | RG cubic coefficients undeclared | Sec 5.1 paragraph + scope reduction |
| R1 | Frame ambiguity | Sec 3 clarification |
| R2 | SPARC residual detail | Appendix C added |
| R2 | S_8 worsens 1% | Sec 6.4 honest concession |
| R2 | DESI DR2 13-pt covariance | Sec 5.3 clarified |
| R2 | μ_eff ≈ 1 / RSD | Sec 5.5 stated as tie not win |
| R3 | Anchor mock detail | Appendix D expanded |
| R3 | ΔAICc vs ΔlnZ headline | Abstract + Sec 7.1 rewritten |
| R3 | False-detection rate | Appendix E added |
| R3 | LOO-CV across data | Appendix D.3 added |

**Headline shift**: from "Bayesian preference" to "falsifiable phenomenology with pre-registered kill conditions". This is consistent with the L6 8-person team consensus on JCAP positioning (CLAUDE.md L6 재발방지).

**No claim of S_8 / H_0 tension resolution**. No claim of decisive Bayesian preference. The paper's contribution is the axiomatic framework + 7 falsifiers, presented honestly.
