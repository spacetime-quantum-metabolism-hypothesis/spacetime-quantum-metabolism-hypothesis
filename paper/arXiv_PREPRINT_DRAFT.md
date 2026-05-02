# MOND acceleration scale a₀ = c·H₀/(2π) from a spacetime-quantum framework

**Draft target**: arXiv preprint (~20 pages, single-column manuscript style)
**Primary category**: astro-ph.CO  **Cross-list**: gr-qc
**Status**: L547 D-path draft (single-agent). Subject to 8-person Rule-A and 4-person Rule-B review before submission. Numbers in this draft are *transcribed* from `paper/base.md` (L515 sync) and `results/L482/`, `L491–L498`, `L502`, `L506`, `L513`, `L515`. No new fits or parameter values are introduced here.

---

## Abstract

(Approximately 250 words. Galactic-phenomenology only — cosmological-acceleration claims are deferred to a companion paper because of unresolved sensitivity to recent age-bias revisions of the SN sample.)

We report a single quantitative result of a 6-axiom spacetime-quantum (SQT) framework: the Milgrom acceleration scale a₀ that organises galactic rotation-curve phenomenology emerges from the framework as a₀ = c·H₀/(2π), with an azimuthal-projection geometric factor 1/(2π). With H₀ = 67.4 km s⁻¹ Mpc⁻¹ this evaluates to 1.042 × 10⁻¹⁰ m s⁻², 2.5% below the SPARC RAR fit of McGaugh et al. (2016) at 1.069 × 10⁻¹⁰ m s⁻², and within ~1σ of the published RAR uncertainty. We classify this prediction as PASS_MODERATE rather than PASS_STRONG, after an explicit hidden-degrees-of-freedom (hidden-DOF) AICc audit that identifies up to nine implicit choices (functional form of the M16 fit, anchor selection between cosmic / cluster / galactic regimes, mass-to-light convention Υ⋆, B1 bilinear ansatz, three-regime carrier+saddle structure, axiom-scale stipulation). Applying these as AICc capacity penalties moves a₀ from naive ΔAICc(SQT−free) ≈ +0.7 to +4.7 (applicable-only) or +18.8 (full count), demoting it from PASS_STRONG to PASS_MODERATE. We additionally report PASS_MODERATE for BBN ΔN_eff (≈10⁻⁴⁶ < 0.17), Cassini |γ−1| (~10⁻⁴⁰ < 2.3×10⁻⁵, channel-dependent), and EP |η| ≤ 10⁻¹⁵ (dark-only embedding); each is downgraded from PASS_STRONG by the same hidden-DOF AICc penalty (ΔAICc ≥ +18 at k_hidden=9). We pre-register five active falsifier channels (Euclid DR1 cosmic-shear S₈, DESI DR3 w_a, CMB-S4 N_eff, ET inspiral phase, SKA cosmic-string null) plus one null channel; their participation-ratio effective number is N_eff = 4.44, combined ρ-corrected significance 8.87σ. We do *not* claim PASS_STRONG anywhere in this preprint, and we do *not* claim a derivation of cosmic-acceleration amplitude.

---

## 1. Introduction

### 1.1 Scope and what this preprint is *not*

This preprint reports galactic-scale phenomenology only. Cosmic-acceleration claims (Λ origin, w(z), σ₈) are deferred. The motivation is twofold:

1. **Son+2025 age-bias contingency.** Recent re-analysis of the SN luminosity sample by Son et al. (2025) raises the possibility that the canonical late-time acceleration evidence is partially absorbed into a host-age systematic. The framework's cosmological narrative (Λ as an absorption/emission balance of spacetime quanta; SQT base.md §1.2.1) is *premised* on the canonical accelerating-Λ picture and would require revision under the Son+ correct branch (paper §1.2.1 caveat; results/L526 R8 §4.1; results/L538 sync). Until the SN community converges, a galactic-phenomenology-only preprint avoids cosmology-conditional claims.
2. **Hidden-DOF audit (L495 / L502 / L513).** The framework was previously advertised as "0 free parameters". A self-audit identified up to nine implicit choices that operate as hidden capacity. Applying them as AICc penalties moves *every* substantive PASS_STRONG candidate to PASS_MODERATE or below. This preprint front-loads that disclosure rather than burying it.

### 1.2 Headline result

The MOND acceleration scale a₀ — the universal scale at which galactic rotation curves transition from Newtonian to flat — is read off the framework as

> a₀ = c · H₀ / (2π)

with the geometric factor 1/(2π) interpreted as a disc-azimuthal projection of the framework's emission rate Γ₀ (paper/base.md §1.2.2; verification/verify_milgrom_a0.py). Numerically, with H₀ = 67.4 km s⁻¹ Mpc⁻¹,

> a₀(SQT) = 1.042 × 10⁻¹⁰ m s⁻²,
> a₀(SPARC RAR; McGaugh et al. 2016) = 1.069 × 10⁻¹⁰ m s⁻²,
> fractional residual = 2.5%, within published RAR uncertainty.

We **do not** call this a falsification-grade prediction of MOND. We call it a PASS_MODERATE consistency check after hidden-DOF AICc penalty (§4.1).

### 1.3 Relation to MOND, MOG, TeVeS, Verlinde

MOND fits a₀ as a single free parameter; MOG, TeVeS, EMG, EG, Verlinde entropic gravity each provide a derivation route with different hidden inputs. Our claim is *not* that the SQT route is uniquely correct, but that under explicit hidden-DOF accounting it remains within ~1σ of SPARC at zero advertised free parameters and at most nine hidden DOFs, comparable to or fewer than the alternatives. Side-by-side comparison: paper/COMPARISON_TABLE.md.

---

## 2. SQT framework — minimal axioms used in this paper

We import only the axioms that feed the a₀ derivation; the full 6-axiom set is in paper/base.md §3 and paper/02_sqmh_axioms.md. The galactic-phenomenology subset is:

- **A1 (quantum substrate).** Spacetime is composed of discrete units carrying a baseline emission/absorption rate Γ₀.
- **A2 (mass-action absorption).** Local matter density acts as a sink for spacetime quanta; the mean-field absorption rate is Γ_abs ∝ ρ.
- **A4 (geometric projection).** For an azimuthally symmetric disc the framework's rate Γ₀ projects onto the radial acceleration with factor 1/(2π) (paper/base.md derived 5; verification/verify_milgrom_a0.py).
- **A5 (Hubble pacing).** Γ₀ is paced by the Hubble rate, Γ₀ ∝ H₀, in the present epoch.

The a₀ derivation uses only A4 + A5, plus dimensional consistency [c · H₀] = m s⁻². The other axioms (A0 metabolism, A3 emission balance, A6 dark-only embedding) are needed for cosmology and PPN, not for §1.2.

---

## 3. Derivation of a₀ = c·H₀/(2π)

**Sketch.** A4 fixes the geometric prefactor; A5 fixes the rate scale c·H₀ (the only Lorentz-invariant combination at order H₀¹). Putting them together,

> a₀ = (1/(2π)) · c · H₀ = c · H₀ / (2π).

**Quantitative check.** Verification script `paper/verification/verify_milgrom_a0.py` reproduces 1.042 × 10⁻¹⁰ m s⁻² at H₀ = 67.4 km s⁻¹ Mpc⁻¹ (expected output: `paper/verification/expected_outputs/verify_milgrom_a0.json`). Sensitivity to H₀ is linear: H₀ = 73.0 (SH0ES) gives a₀ = 1.13 × 10⁻¹⁰ m s⁻², still within RAR 1σ.

**What is *not* derived.** The numerical factor 1/(2π) is a geometric *plausibility argument* (disc azimuthal projection), not a first-principles CFT calculation. The framework supplies dimensional structure c·H₀ rigorously; the prefactor is one of the nine hidden DOFs (§4.2).

---

## 4. Evidence at PASS_MODERATE — four channels

Each of the four channels below is downgraded from PASS_STRONG to PASS_MODERATE by the L502 hidden-DOF AICc penalty (k_hidden = 9 conservative; ΔAICc ≥ +18). We report PASS_MODERATE as the honest grade.

### 4.1 RAR a₀ — galactic rotation curves (SPARC; McGaugh et al. 2016)

- **Datum.** SPARC 175-galaxy RAR, M16 fit a₀ = 1.069 × 10⁻¹⁰ m s⁻².
- **SQT.** a₀ = c·H₀/(2π) = 1.042 × 10⁻¹⁰ m s⁻² → 2.5% offset, ~1σ.
- **Cross-form spread (L491).** Eight functional-form variants of the fit yield 0.37 dex spread; *median* form 0.023 dex consistent with SQT. PASS is form-dependent.
- **Dwarf cross-dataset (L492).** Dwarf-galaxy subsample yields a₀ = 0.46 × 10⁻¹⁰ m s⁻² with non-trivial cross-dataset disagreement; KS dwarf-vs-bright p = 0.005.
- **OOS / mock (L493 / L494).** 30% out-of-sample retention; 0/1000 mock false-positives → real signal confirmed at the SPARC anchor.
- **Hidden-DOF AICc (L502).** ΔAICc(SQT−free) = +0.70 (naive), +4.71 (applicable-only), +18.8 (full k_hidden=9). PASS_MODERATE under applicable-only, demoted further under full count.

**Grade:** PASS_MODERATE.

### 4.2 BBN ΔN_eff (Planck + light-element)

- **Datum.** ΔN_eff < 0.17 (95%).
- **SQT.** ΔN_eff ≈ 10⁻⁴⁶ (η_{Z₂} ≈ 10 MeV ≫ T_BBN; β_eff² double-suppression).
- **Caveat.** Consistency check, not a falsifiable prediction (the suppression is automatic given axiom inputs).
- **Hidden-DOF AICc.** ΔAICc ≥ +18 at k_h = 9 → PASS_MODERATE.

**Grade:** PASS_MODERATE (consistency).

### 4.3 Cassini |γ−1| (PPN)

- **Datum.** |γ−1| < 2.3 × 10⁻⁵ (Cassini 2003).
- **SQT.** |γ−1| ≈ 1.1 × 10⁻⁴⁰ via β_eff = Λ_UV/M_Pl ≈ 7.4 × 10⁻²¹ (small-coupling channel).
- **Channel dependence (L506).** Universal scalar coupling at Phase-3 β = 0.107 yields |γ−1| ≈ 2.3 × 10⁻², ~10³× hard-fail. K_C1–C4 4/4 FAIL universal; PASS depends on dark-only / screening channel selection.
- **Hidden-DOF AICc.** Channel selection itself is one of the nine hidden DOFs.

**Grade:** PASS_MODERATE (channel-dependent).

### 4.4 Equivalence-principle |η|

- **Datum.** |η| ≤ 10⁻¹⁵ (MICROSCOPE).
- **SQT.** |η| = 0 by construction (β_b = 0, dark-only embedding).
- **Caveat.** Structural — set by axiom A6 (baryons in Einstein frame). Not falsifiable within the present framework version.
- **Hidden-DOF AICc.** PASS_MODERATE after k_h = 9 penalty.

**Grade:** PASS_MODERATE (structural).

---

## 5. Falsifiers (pre-registered)

Six pre-registered falsifier channels (paper/base.md §4.9; results/L498/FALSIFIER_INDEPENDENCE.md) compress to N_eff = 4.44 (participation-ratio; *headline*). The naive count of 6 and the naive combined 11.25σ **must not** be cited standalone; the corrected ρ-aware combined is 8.87σ.

| # | Channel | Window | Status |
|---|---|---|---|
| F1 | Euclid DR1 cosmic-shear S₈ | 2026 | active; central 4.38σ falsification trigger if SQT predicted +1.14% σ₈ structural worsening confirmed |
| F2 | DESI DR3 w_a | 2027 | active; SQT requires w_a < 0 amplitude consistent with axiom-3 emission balance (cosmology-conditional, see §1.1) |
| F3 | CMB-S4 N_eff | 2030 | active; load-bearing orthogonal channel |
| F4 | Einstein Telescope inspiral phase | 2030s | active; load-bearing orthogonal channel |
| F5 | SKA cosmic-string null | 2030s | null; load-bearing orthogonal channel |
| F6 | LSST cluster-shear cross with Euclid | 2030s | active; passes Bonferroni only by ~2× margin if Euclid×LSST ρ < 0.80 |

**N_eff estimators.** Participation-ratio 4.44 (headline, conservative); Li–Ji 5.00; Cheverud–Galwey 5.71; naive 6.00. The "6 independent 5σ-class falsifiers" wording is replaced by **"5 active + 1 null falsifier across N_eff ≈ 4.44 independent observable channels, 8.87σ ρ-corrected combined."** Three load-bearing orthogonal channels (CMB-S4, ET, SKA-null) carry Z_comb ≈ 10.83σ alone. Correlated pairs: Euclid×LSST = 0.80, DESI×Euclid = 0.54, DESI×SKA = 0.32. All Holm/Bonferroni tests at family α = 0.05 still pass.

---

## 6. Hidden degrees of freedom — explicit disclosure

Following the L495 audit and L502 AICc analysis (`results/L495/HIDDEN_DOF_AUDIT.md`, `results/L502/HIDDEN_DOF_AICC.md`, `results/L513/REVIEW.md`), we enumerate the implicit choices that contribute capacity to the framework. This section is the §6.5(e) disclosure of paper/base.md transcribed in compressed form.

**Conservative count: k_hidden = 9.**

1. M16 functional form for RAR fit (one DOF).
2. Anchor selection between cosmic, cluster, and galactic regimes (three DOFs).
3. Mass-to-light Υ⋆ convention (one DOF).
4. B1 bilinear ansatz (one DOF).
5. Three-regime carrier + saddle structure (two DOFs).
6. Axiom-scale stipulation (one DOF; e.g., η_{Z₂} ≈ 10 MeV).

**Extended count: ~13** (adds functional-form variants of the geometric prefactor 1/(2π), disformal/conformal frame ambiguity).

**Consequence (L502 AICc, k_h = 9 conservative).** The four substantive PASS_STRONG candidates (a₀, BBN ΔN_eff, Cassini |γ−1|, EP |η|) all incur ΔAICc ≥ +18 → PASS_MODERATE or below.

**Headline.** Under the hidden-DOF AICc penalty, **PASS_STRONG count is 0 / 32** in the full self-audit. Citing the unpenalised raw counts (pre-L412 31%, post-L412 28%, substantive 13%) standalone is prohibited (L513 / L515 sync); they must be accompanied by the 0% honest headline.

**This is the §6.5(e) hidden-DOF disclosure transcribed into a public preprint.** It is intended to render the framework falsifiable on capacity-corrected grounds rather than on advertised-DOF grounds.

---

## 7. Discussion, limitations, conclusions

### 7.1 What this preprint claims

- a₀ = c·H₀/(2π) reproduces the SPARC RAR M16 fit at 2.5% (within 1σ).
- Three additional channels (BBN ΔN_eff, Cassini |γ−1| dark-only, EP |η|) pass at PASS_MODERATE under hidden-DOF AICc.
- Six pre-registered falsifiers compress to N_eff = 4.44, ρ-corrected 8.87σ; three load-bearing orthogonal (CMB-S4, ET, SKA-null).

### 7.2 What this preprint does *not* claim

- No PASS_STRONG anywhere (hidden-DOF AICc 0% headline).
- No first-principles derivation of the geometric prefactor 1/(2π); plausibility only.
- No cosmic-acceleration amplitude derivation (Q17 amplitude-locking is *not* dynamically derived; E(0)=1 normalisation only).
- No claim that S₈ tension is resolved (μ_eff ≈ 1 structurally; ΔS₈ < 0.01%).
- No claim of Cassini PASS in the universal-coupling channel.

### 7.3 Limitations

- **Cosmology-conditional.** Son+2025 age-bias correction, if confirmed, demotes much of the framework's cosmological narrative (paper §1.2.1 caveat).
- **Channel-dependent PPN.** Cassini PASS_MODERATE depends on dark-only embedding; universal coupling fails.
- **Postdiction risk.** Three-regime structure (galaxy / cluster / cosmic) was identified through data-fitting, not pre-registered.
- **Hidden DOFs.** The 9 hidden DOFs identified here are likely a *lower bound*; extended count ~13.

### 7.4 Path forward

- DESI DR3 (F2) is the most decisive near-term test once the Son+ branch settles.
- Euclid DR1 cosmic-shear (F1) provides a 4.38σ-class falsification trigger on σ₈ structural worsening.
- A first-principles derivation of the 1/(2π) geometric prefactor (e.g., disc-azimuthal CFT projection from a more fundamental SQT Lagrangian) is the most natural way to remove one hidden DOF.

---

## arXiv submission metadata

- **Primary**: astro-ph.CO  (cosmology and large-scale structure — galactic phenomenology of MOND scale).
- **Cross-list**: gr-qc  (alternative gravity framework, PPN constraints).
- **MSC**: 83F05 (cosmology), 83D05 (relativistic gravitational theories other than Einstein's).
- **Comment field**: "20 pages, 0 figures (verification scripts in ancillary). Hidden-degrees-of-freedom AICc audit applied throughout; no PASS_STRONG claimed."
- **Ancillary files**: `paper/verification/verify_milgrom_a0.py`, `paper/verification/expected_outputs/verify_milgrom_a0.json`, `paper/verification_audit/R3_axioms.json`, `paper/verification_audit/R5_quantum_result.json`, `results/L491/`, `results/L495/`, `results/L498/`, `results/L502/`, `results/L506/`, `results/L513/`.

---

## Reference pointers (to project documents — replace with bibliographic citations on arXiv submission)

- McGaugh, Lelli, Schombert (2016) — SPARC RAR fit (a₀ = 1.069 × 10⁻¹⁰ m s⁻²).
- Cassini PPN constraint — Bertotti, Iess, Tortora (2003).
- BBN ΔN_eff bound — Planck 2018 + Particle Data Group light-element review.
- MICROSCOPE EP — Touboul et al. (2017).
- DESI DR2 w_a — DESI Collaboration arXiv:2404.03002.
- Son et al. (2025) — SN host-age systematic (cited as cosmology-conditional caveat only).
- Internal audit chain: paper/base.md (L515 sync); results/L482 (RAR), L491 (cross-form spread), L492 (dwarf), L493–L494 (OOS/mock), L495 (hidden-DOF), L498 (falsifier independence), L502 (hidden-DOF AICc), L506 (Cassini robustness), L513 (headline integration), L515 (sync), L526 R8 (Son+ contingency), L537 (Phase 8 synthesis), L545 (Phase 10 synthesis).

---

## Honest one-liner (per CLAUDE.md)

This preprint claims four PASS_MODERATE galactic/local channels (RAR a₀ at 2.5%, BBN ΔN_eff, Cassini |γ−1| dark-only, EP |η|) and six pre-registered falsifiers compressing to N_eff = 4.44 / 8.87σ ρ-corrected; it claims **no** PASS_STRONG (hidden-DOF AICc 0% headline), **no** cosmic-acceleration derivation, and **no** S₈-tension resolution; the geometric prefactor 1/(2π) is plausibility, not first-principles; cosmology is deferred pending the Son+2025 SN age-bias branch resolution.

---

*Draft saved 2026-05-01. paper/arXiv_PREPRINT_DRAFT.md. Single-agent L547 D-path. CLAUDE.md [최우선-1] (no new equations, parameter values or derivation hints introduced — every numerical value is transcribed verbatim from existing audited results), [최우선-2] (8-person Rule-A and 4-person Rule-B independent review required prior to actual arXiv submission), 결과 왜곡 금지 (hidden-DOF 0% PASS_STRONG headline front-loaded; cosmology caveat front-loaded; channel-dependence of Cassini front-loaded), L6 §"PRD Letter 진입 조건" (Q17/Q13/Q14 미달 → arXiv preprint only, no PRD Letter submission).*
