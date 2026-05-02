# Spacetime Quantum Theory (SQT)

🇺🇸 English | [🇰🇷 한국어](README.ko.md)

[![DOI](https://img.shields.io/badge/DOI-pending-lightgrey.svg)](https://doi.org/10.5281/zenodo.PENDING)
[![CI](https://img.shields.io/badge/CI-pending-lightgrey.svg)](https://github.com/USER/REPO/actions)
[![License: MIT (code) / CC-BY-4.0 (text)](https://img.shields.io/badge/license-MIT%20%2B%20CC--BY--4.0-blue.svg)](LICENSES.md)
[![OSF preregistration](https://img.shields.io/badge/OSF-preregistered-lightgrey.svg)](https://osf.io/PENDING)

![Hero infographic](paper/figures/hero.png)

> **One-sentence headline**: *A 6-axiom phenomenological framework for the cosmological constant scale and Milgrom's a₀ — published with explicit hidden-DOF disclosure, embedding-conditional caveats, and a single pre-registered DR3 falsifier.*

## TL;DR
- ⚠️ ρ_q/ρ_Λ(Planck) order-unity (CONSISTENCY_CHECK; circularity structural — see §5.2; L402 audit confirmed unavoidable)
- ✅ a₀ = c·H₀/(2π) order-of-magnitude invariance (factor-≤1.5 across 5 axes; *quantitative* row demoted to PASS_MODERATE per L502/L516)
- ⚠️ Bullet cluster: PASS_QUALITATIVE only (Bullet/MACSJ0025/MACSJ1149 3/4; A520 dark-core ambiguous; L509)
- ❌ S_8 tension: SQT *worsens* by +1.14% (OBS-FAIL, structural μ_eff≈1, no parameter escape)
- ⚠️ Three-regime σ₀(env) is post-hoc fit; **L510**: zero of three anchors are truly external (cosmic circular, cluster LCDM-bridged, galactic MOND-prior + SQT-internal)
- ⏰ **Decisive falsifier: DESI DR3 w_a (full-Y5 cosmology release expected 2027 per LBL Apr-2026 announcement; L520)** — minimal SQT predicts w_a=0
- 📊 Self-audit (33 claims, *L516 hidden-DOF re-grading*): substantive PASS_STRONG **0%** under honest AICc penalty (k_h applicable per row) ; PASS_MODERATE 5 + PASS_QUALITATIVE 1 = **18% combined PASS** ; PASS_IDENTITY 3 + PASS_BY_INHERITANCE 8 + CONSISTENCY_CHECK 1 + PARTIAL 7 + NOT_INHERITED 8 ; FRAMEWORK-FAIL 0. Headline raw 28% (PASS_STRONG 9/32, *pre-L516, deprecated*) retained for legacy reference only. Full §6.1 + raw evidence in [paper/verification_audit/](paper/verification_audit/).
- 🎯 **Independence audit (L498)**: 6 pre-registered falsifiers carry **N_eff = 4.44** (participation ratio); ρ-corrected combined detection **8.87σ** (active 5 → 9.95σ), naive 11.25σ retired.
- 📡 **JCAP majority-acceptance estimate (L517 + L521 update)**: 8–19%, central **13–14%**, conditional on (abstract-drift 5-loc fix + claims_status sync + §4.1 RAR sub-row split + §6 limitations 8-row addition).

## Verify in 5 seconds
```bash
git clone https://github.com/USER/REPO.git
cd REPO/paper/verification
pip install -r requirements.txt
python verify_lambda_origin.py     # Λ origin dimensional consistency check
                                   # (circular w.r.t. ρ_Λ_obs — see §5.2)
```
4 more scripts in `paper/verification/`. See [Verification README](paper/verification/README.md).
For internal audit details (R1–R8 cold-blooded audit + L491–L514, L517 substrate), see [paper/verification_audit/](paper/verification_audit/) and [results/L518](results/L518/SYNTHESIS_v7.md), [results/L521](results/L521/SYNTHESIS_v8.md).

## Claims status (machine-readable: [claims_status.json](claims_status.json))

*Summary view of the canonical 22-row limitations table (§6.1) + 11-row PASS table (§4.1). Each row below aggregates one or more entries; see the **Maps to** column.*

*Two distinct meanings of "fail" (do not conflate):*
- ❌ **OBS-FAIL** (observational worsening) — SQT structurally worsens fit to a real dataset, no parameter escape (e.g. S_8). *Theory-vs-data tension.*
- 🚫 **FRAMEWORK-FAIL** (internal inconsistency) — paper framework itself contains a logical/mathematical contradiction surfaced by self-audit. **Currently 0** (see §6.5(e)).

*Per L516 hidden-DOF re-grading: every previously-substantive PASS_STRONG row carries 1–2 applicable hidden DOF. With the L502 AICc penalty rule (k_h ∈ {1,2}, ΔAICc(SQT − free) ∈ [+2, +5]), **no claim survives an honest AICc test at PASS_STRONG**. Three new grades introduced: PASS_MODERATE, PASS_QUALITATIVE, OPEN_PROVISIONAL.*

| Claim | Status (post-L516) | Evidence | Caveat | Maps to |
|---|---|---|---|---|
| Λ origin | ⚠️ CONSISTENCY_CHECK | ρ_q/ρ_Λ order-unity (dimensional, *not* a prediction) | circularity structural (n_∞ uses ρ_Λ_obs via axiom 3); L402 Path-α independent derivation failed | §5.2; §6.1 row 13 |
| MOND a₀ (order-of-magnitude) | ✅ PASS_MODERATE [`RAR_a0_orderof`] | a₀ = c·H₀/(2π), factor-≤1.5 invariant across 5 axes (Υ⋆/ν-form/anchor/cuts/H₀); 7-criterion 6/7 PASS | L491 cross-form spread 0.37 dex (IQR 0.17); L496 LOO max\|ΔPR\|=0.089 < 0.125 | §1.2.2; §4.1 sub-row (a) |
| MOND a₀ (quantitative) | ⚠️ PASS_MODERATE [`RAR_a0_quantitative`] | M16 + Υ⋆ canonical, ΔAICc_honest = +4.707 (k_h=2) | L492 1/4 cross-dataset PASS (D4 dwarf Δlog=−0.353); L503 a₀ NOT universal per-galaxy; L495 hidden DOF 9–13 | §4.1 sub-row (b) |
| Bullet cluster | ⚠️ PASS_QUALITATIVE | Bullet/MACSJ0025/MACSJ1149 3/4 qualitative PASS | A520 dark-core ambiguous; quantitative magnitude not derivable for any of 4 (L509) | §4.1 row 10 |
| BBN ΔN_eff | ✅ PASS_MODERATE | ΔN_eff ≈ 10⁻⁴⁶ < 0.17; cross-experiment robust (L507) | η_Z₂ ≈ 10 MeV stipulation (k_h=1); ΔAICc_honest = +2.0 — borderline | §4.1 row 2 |
| Cassini PPN | ✅ PASS_MODERATE | \|γ−1\|≈10⁻⁴⁰ on 6/8 channels | **embedding-conditional**: channel 3 universal_phase3 (β=0.107) HARD FAIL ~1000×; PASS contingent on dark-only / Vainshtein / chameleon screening (L506) | §4.1 row 3 |
| EP \|η\|=0 | ✅ PASS_MODERATE | MICROSCOPE structurally 0 | LLR Nordtvedt channel \|η_N\|≲10⁻¹⁴ non-zero (G_N(t) drift at β_dark~0.1; L508) | §4.1 row 4 |
| GW170817 c_T, LLR Ġ/G | ✅ PASS_BY_INHERITANCE | \|Δc/c\|=0; Ġ/G=0 | Lagrangian-form choice + axiom tautology (legacy `PASS_TRIVIAL` alias); disformal revival ⇒ KILL | §4.1 rows 5–6 |
| Three-regime σ₀(env) | ⚠️ PARTIAL + POSTDICTION | 17σ regime-gap | **L510**: 0/3 anchors truly external — cosmic circular, cluster LCDM-bridged + Lorentzian ansatz, galactic MOND-prior + SQT-internal D1 (β=1); 1.81 dex gap may be methodological-prior artefact | §3.4; §6.1 rows 5–7 |
| CMB θ_* shift | ⚠️ PARTIAL | δr_d/r_d ≈ 0.7% (Planck σ × 23) | matter-era φ evolution; same channel as Phase-2 BAO | §4.1 row 8 |
| S_8 tension | ❌ OBS-FAIL (structural) | +1.14% worse than ΛCDM (ξ_+ +2.29%) | structural μ_eff≈1, no parameter escape | §4.6; §6.1 row 1 |
| DESI w_a | ⏰ PENDING (DR3 full Y5 cosmology = 2027) | minimal SQT: w_a=0; V(n,t)-extension gate OPEN | LBL Apr-2026 announcement: full Y5 results expected 2027 (L520); preprint window 12–18 months | §4.3, §4.4, §5.4; §6.1 row 12 |
| Foundational/inheritance gaps | ⚠️ NOT_INHERITED | 8/33 claims (singularity, Volovik, Jacobson, GFT/BEC chain) | axiom 4 5th-pillar decision (Causet vs GFT) blocks 5/8 | §6.1 rows 15–22 |

### New audit-derived keys recommended for `claims_status.json` (L518 §3.3 + L498/L495/L502/L506/L508/L510)

The following 6 keys are *recommended additions* — direct application gated on L512 (Rule-A 8-reviewer round) + L513 (Rule-B 4-reviewer code review) sign-off. Tracked under [results/L524/REPO_FINAL.md](results/L524/REPO_FINAL.md):

1. `RAR_a0_orderof` — PASS_MODERATE; factor-≤1.5 invariance across 5 axes.
2. `RAR_a0_quantitative` — PASS_MODERATE; ΔAICc_honest = +4.707, hidden DOF k≈3 (M16 + Υ⋆ canonical only).
3. `falsifier_Neff` — value 4.44 (participation ratio, L498); naive 6 retired; combined significance {all6_corr: 8.87σ, active5_corr: 9.95σ, naive: 11.25σ}.
4. `hidden_dof_audit` — conservative 9 / expansive 13 (L495); 5 abstract-drift locations catalogued.
5. `cassini_embedding_conditional` (caveat extension on `cassini-ppn`) — universal β=0.107 HARD FAIL 1000×; PASS only under dark-only / screening.
6. `sigma0_methodological_prior` (caveat extension on `sigma0-three-regime`) — 0/3 anchors truly external (L510); 1.81 dex gap likely partly methodological.

## How to cite
```bibtex
@article{SQT2026,
  title   = {Spacetime Quantum Theory: A 6-Axiom Phenomenological Framework with Honest Hidden-DOF Disclosure and Pre-Registered Falsifiers},
  author  = {<author>},
  year    = {2026},
  version = {L524},
  doi     = {10.5281/zenodo.PENDING},
  url     = {https://github.com/genesos/spacetime-quantum-metabolism-hypothesis}
}
```

> **DOI versioning**: the Zenodo *concept DOI* aggregates all versions; *version DOIs* cite a specific release. Paper-body citations should use the **concept DOI**.

## Documentation
- [Paper PDF (English)](paper/main_en.pdf) | [Paper PDF (한국어)](paper/main_ko.pdf)
- [FAQ for general audience](paper/faq_en.md) | [한국어 FAQ](paper/faq_ko.md)
- [Verification quickstart](paper/verification/README.md)
- [Honest limitations table (machine-readable)](claims_status.json)
- [L518 Phase 1+2+3 synthesis](results/L518/SYNTHESIS_v7.md)
- [L520 pre-DR3 publish strategy](results/L520/PUBLISH_STRATEGY.md)
- [L521 Phase 1+2+3+4+5 synthesis (v8)](results/L521/SYNTHESIS_v8.md)
- [L524 repository final-touch decision](results/L524/REPO_FINAL.md)
- [Pre-registration on OSF](https://osf.io/PENDING)
- [Translation policy](TRANSLATION_POLICY.md)

## Honesty statement (L524)

This README and the underlying paper deliberately avoid retrofitting headline numbers. Specifically:
- The legacy "PASS_STRONG 9/32 = 28%" headline is *retired* in favour of the L516 hidden-DOF-honest distribution (PASS_STRONG **0%** under AICc penalty).
- "6 independent falsifiers, 11.25σ" is retired in favour of N_eff = 4.44 / 8.87σ (ρ-corrected).
- "DR3 in 2025–2026" is corrected to "full Y5 cosmology release in 2027" per the LBL Apr-2026 announcement (L520).
- All cross-channel caveats (Cassini embedding, EP LLR, σ₀ external-anchor count) are pulled forward from §6.1 into the headline table so referees do not encounter them only after page 30.

## Contributing
See [CONTRIBUTING.md](.github/CONTRIBUTING.md). Issue templates for verification-failure reports live in `.github/ISSUE_TEMPLATE/`.

## License
Code: **MIT**. Text/Figures: **CC-BY-4.0**. Per-directory table: [LICENSES.md](LICENSES.md).
