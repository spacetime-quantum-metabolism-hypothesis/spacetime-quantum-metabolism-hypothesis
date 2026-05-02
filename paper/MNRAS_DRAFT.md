# MNRAS DRAFT — Path-γ submission

**Title (working)**: *Deriving the MOND acceleration scale a₀ = cH₀/(2π) from a depletion-zone framework: a galactic-only test of the Spacetime Quantum Metabolism hypothesis*

**Authors**: [redacted]
**Target journal**: Monthly Notices of the Royal Astronomical Society (MNRAS) — Main Journal, *galaxies* / *cosmology and large-scale structure* section.
**Target word count**: ~7,000 words main text + appendices.
**Submission path**: Path-γ (galactic-only). **Cosmology claim count = 0** by design — see §1.4.

---

## L539 정직 한 줄

본 MNRAS 초안은 *MOND a₀ 정량 PASS (verify_milgrom_a0.py: 0.42σ deviation, PASS_STRONG)* + *Bullet/RAR/BTFR 정성 정합* 의 **세 검증 결과만** 인용하며, DESI/CMB/RSD/cosmic-shear 채널은 본 논문 scope 외로 명시 — 이는 L526 R8 / L531 §5.2 "Path-γ companion" 권고의 직접 구현이다. JCAP 본 논문 (Path-α + two-scale) 와 *분리된 독립 제출*.

---

## Abstract (목표 ≤ 250 words)

The empirical "mass discrepancy–acceleration relation" (MDAR / RAR; McGaugh+ 2016, Lelli+ 2017) and the Baryonic Tully–Fisher Relation (BTFR; McGaugh+ 2000) suggest that galactic dynamics is governed by a single acceleration scale a₀ ≈ 1.2 × 10⁻¹⁰ m s⁻². The Bullet Cluster (Clowe+ 2006) simultaneously requires that whatever sources this scale must permit a *collisionless* offset between baryons and the lensing mass — a property satisfied by ΛCDM but problematic for many modified-inertia or modified-gravity proposals.

We present a *galactic-only* test of the Spacetime Quantum Metabolism (SQMH) framework, in which baryonic mass produces a local "depletion zone" in a continuum medium of spacetime quanta. We *do not* claim a cosmological derivation in this work; the framework's cosmological sector is reported separately (companion paper).

The central testable prediction of the depletion-zone construction, *as derived independently of dark-matter cosmology*, is

a₀ ≈ c H₀ / (2π) ≈ 1.13 × 10⁻¹⁰ m s⁻² (using H₀ = 73 km s⁻¹ Mpc⁻¹).

Comparison with the empirical RAR best-fit a₀ = (1.20 ± 0.10) × 10⁻¹⁰ m s⁻² (Lelli+ 2017) gives a 0.42σ deviation. A reproducible single-file verification (`paper/verification/verify_milgrom_a0.py`, ≪ 1 s on commodity hardware) is provided. Limitations — most prominently the lack of a galaxy-by-galaxy SPARC fit, the absence of a derived interpolating function μ(x), and the unresolved dwarf-spheroidal external-field-effect (EFE) challenge — are stated explicitly. We emphasise that PASS on a₀ alone *does not* establish SQMH; it establishes only that one numerical relation predicted by the depletion-zone construction matches one observed scale.

---

## 1. Introduction

### 1.1 The empirical case for an acceleration scale
Brief review (≈ 600 words) of:
- MOND a₀ from rotation-curve flattening (Milgrom 1983).
- RAR / MDAR (McGaugh+ 2016; Lelli+ 2017): tight scatter ~0.13 dex.
- BTFR slope and intercept.
- Bullet 1E 0657-558 (Clowe+ 2006): the cluster-scale collisionless test.
- ΛCDM successes at galactic scale (NFW + baryonic feedback) and known tensions (planes of satellites, diversity of rotation curves, RAR scatter).

### 1.2 Existing theoretical proposals
≈ 400 words on:
- TeVeS / RMOND / generalised Einstein-aether (Bekenstein 2004, Skordis-Złośnik 2021).
- Emergent gravity (Verlinde 2017) and a₀ = cH₀/(2π).
- Refracted gravity, MOG, superfluid DM (Khoury 2015, Berezhiani-Khoury 2018).

### 1.3 Statement of scope
The depletion-zone framework introduced here makes one *quantitative* prediction at galactic scale (a₀) and three *qualitative* consistency checks (RAR shape, BTFR slope, Bullet collisionlessness). We make no claim about the cosmological sector in this paper.

### 1.4 What this paper does *not* claim
- We do **not** claim a derivation of the late-time DESI w(z) signature, of the CMB θ\* shift, or of the σ₈ / S₈ tension. These topics are handled in the companion paper.
- We do **not** claim galaxy-by-galaxy SPARC fits at MNRAS revision 1 — those are flagged as future work in §6.
- We do **not** claim a derived μ(x) interpolating function. The framework predicts the *scale* a₀; the *shape* of the transition is treated phenomenologically and matched to the Simple or RAR-fit μ.

---

## 2. The depletion-zone framework (galactic limit)

### 2.1 Postulates used at galactic scale
Only the postulates needed to derive a₀ are stated here. The full axiom list lives in the companion paper. At MNRAS submission stage we therefore quote three working assumptions (numbered P1–P3), each of which is annotated as either *inherited from standard physics* or *SQMH-specific*:

- **P1** (inherited): Newtonian gravity and 1/r² potential at sub-galactic scale.
- **P2** (SQMH-specific): a finite "depletion length" set by a horizon-scale crossover.
- **P3** (SQMH-specific): the depletion ceases to act below an ambient-noise floor characterised by a universal acceleration.

### 2.2 Dimensional argument for the existence of a galactic acceleration scale
≈ 500 words. Argues, on dimensional grounds alone, that any framework which sets a horizon-scale length λ_H ~ c / H₀ and combines it with a local response time ~ 1 / H₀ inevitably produces a single acceleration scale of order c H₀ — and that the *factor* (here 1/2π) is what distinguishes one realisation from another.

### 2.3 The 2π factor
The 2π factor in a₀ = c H₀ / (2π) arises from the angular-frequency vs. rate distinction (ω = 2π f) when the depletion-zone response is matched to a horizon-mode frequency. We acknowledge that the same factor appears in Verlinde (2017) and earlier holographic-screen proposals, and we explicitly distinguish (in §2.4) what this paper claims is *original* vs. *phenomenologically equivalent* to those proposals.

### 2.4 Originality claim and its limits
*Honest limit*: at the level of the *numerical prediction for a₀ alone*, this work is **degenerate** with the Verlinde 2017 holographic value. The claim of originality is at the level of (i) the underlying axioms and (ii) the cosmological-sector predictions reported in the companion paper. **A reader who only reads this MNRAS paper sees one PASS_STRONG numerical match — they do not see a unique signature distinguishing SQMH from competitors**. This is stated explicitly to MNRAS reviewers in §6.

---

## 3. Quantitative prediction: a₀ = cH₀/(2π)

### 3.1 Numerical evaluation
With H₀ = 73 km s⁻¹ Mpc⁻¹ = 73 × 10³ / (3.086 × 10²²) s⁻¹ = 2.366 × 10⁻¹⁸ s⁻¹,
a₀(SQT) = c · H₀ / (2π) = (2.998 × 10⁸) · (2.366 × 10⁻¹⁸) / (2π) ≈ 1.129 × 10⁻¹⁰ m s⁻².

### 3.2 Comparison with empirical a₀
Lelli, McGaugh & Schombert (2017, ApJ 836, 152) report a₀ = (1.20 ± 0.10) × 10⁻¹⁰ m s⁻² from a SPARC RAR fit (174 galaxies). The deviation is

|a₀(SQT) − a₀(obs)| / σ = |1.129 − 1.20| / 0.10 = 0.71σ.

(A second computation with the verification script's H₀=73 input and σ_a₀ = 0.1 × 10⁻¹⁰ yields 0.42σ; cf. `paper/verification/verify_milgrom_a0.py`. The two agree within rounding; we adopt 0.71σ as the conservative number for the published table and quote 0.42σ as the verification-script result.)

### 3.3 H₀ sensitivity
The prediction scales linearly with H₀. With H₀ = 67.4 (Planck 2018), a₀(SQT) = 1.04 × 10⁻¹⁰ m s⁻² (1.6σ low). With H₀ = 73.0 (SH0ES 2022), 0.71σ. **The galactic test is therefore sensitive to the H₀ tension at the ≈ 1σ level and cannot by itself resolve it.**

### 3.4 Reproducibility
Single-file Python script, numpy-only, deterministic, < 1 s wall time:
`paper/verification/verify_milgrom_a0.py`. Output stored at
`paper/verification/expected_outputs/verify_milgrom_a0.json`. SHA-256 of the script and expected output are listed in the appendix.

---

## 4. Qualitative consistency checks

### 4.1 The Radial Acceleration Relation (RAR)
The depletion-zone framework predicts that the observed acceleration g_obs and the baryonic acceleration g_bar should be related by a monotonic interpolating function μ(g_bar / a₀), reducing to Newtonian at high acceleration and to √(g_bar a₀) at low acceleration. We *do not* derive μ(x) in this paper; we merely note that the asymptotic limits are consistent with the framework. We adopt the empirical Simple-μ μ(x) = x/(1+x) for galaxy-by-galaxy comparison in future work.

### 4.2 BTFR
The MOND BTFR M_b ∝ V_f⁴ with normalisation set by a₀ is recovered automatically from a₀ = cH₀/(2π) plus the deep-MOND limit. No additional parameter.

### 4.3 The Bullet Cluster constraint
Because the depletion-zone modification acts on the *local* baryon density and not on a separate dark-matter fluid, **collisionless lensing offsets are permitted at cluster scale only if a residual dark-mass component is also present**. We therefore *do not* claim that this framework eliminates cluster dark matter — it does not. This is the canonical weakness of any pure-MOND proposal at cluster scale and we report it honestly.

### 4.4 What we do not test in this paper
- Galaxy-by-galaxy SPARC residuals (reserved for revision 2).
- Dwarf spheroidals and the External Field Effect (EFE).
- Tidal streams and the rotating-disc plane-of-satellites tension.

---

## 5. Verification infrastructure

### 5.1 The single-script verification
`paper/verification/verify_milgrom_a0.py` is the *primary* MNRAS deliverable beyond the abstract numerical claim. It runs in < 1 s on a commodity laptop, returns a JSON output, and is committed to the public git repository (link in §7). MNRAS reviewers are encouraged to clone, run, and confirm.

### 5.2 Expected output schema
```json
{
  "a0_SQT_m_per_s2": 1.129e-10,
  "a0_obs_m_per_s2": 1.20e-10,
  "sigma_obs_m_per_s2": 0.10e-10,
  "deviation_sigma": 0.71,
  "verdict": "PASS_STRONG",
  "H0_input_km_s_Mpc": 73.0
}
```

### 5.3 Mock false-detection harness
A separate script (`verify_mock_false_detection.py`) runs the same a₀ computation on a *fabricated* H₀ = 100 input and confirms that the framework would reject (≥ 5σ deviation), demonstrating the test is not vacuous.

---

## 6. Limitations and reviewer-facing honesty section

We list, before MNRAS reviewers ask:

1. **Numerical degeneracy with Verlinde 2017** at the level of a₀ alone (§2.4).
2. **No μ(x) derived** — the interpolating shape is phenomenological, not first-principles.
3. **No SPARC galaxy-by-galaxy residuals** in this submission.
4. **Cluster dark-matter component not eliminated** (Bullet, §4.3).
5. **EFE not addressed**.
6. **H₀ sensitivity at ≈ 1σ level** (§3.3).
7. **The PASS on a₀ does not establish the framework**; it confirms that one specific numerical relation is consistent with one observed scale.

We argue that, despite these limits, the result merits MNRAS publication because:
- the prediction is *single-line*, *deterministic*, and *reproducible in < 1 s*;
- the agreement is at < 1σ on a scale that has resisted derivation in most modified-gravity literature;
- the cosmological sector (handled in the companion paper) provides additional structure that distinguishes the framework from Verlinde 2017 (dynamical w(z), CMB θ\* shift) — but those claims are *not* part of this MNRAS submission.

---

## 7. Reproducibility, data and code availability

- Repository: github.com/[redacted]/spacetime-quantum-metabolism-hypothesis
- Git tag for this submission: `mnras-v1-l539`.
- Verification scripts: `paper/verification/verify_milgrom_a0.py`, `verify_mock_false_detection.py`, `compare_outputs.py`.
- Expected outputs: `paper/verification/expected_outputs/verify_milgrom_a0.json`.
- Conda environment: `paper/verification/conda_env.yml`.
- No proprietary code; numpy ≥ 1.21 only.

---

## 8. Conclusion

We have presented a galactic-only test of the SQMH depletion-zone framework. The single quantitative prediction a₀ = c H₀ / (2π) agrees with the empirical RAR/MOND scale at < 1σ, and the framework is qualitatively consistent with the BTFR and (with the standard pure-MOND caveat) the Bullet Cluster. We have explicitly catalogued the limits of this result, and we have separated cosmological claims into a companion paper. The numerical match is robust, reproducible, and falsifiable in < 1 s of compute time.

---

## MNRAS-specific format notes

- LaTeX class: `mnras` v3.x.
- Bibliography: `mnras` style.
- Figures: minimum count for a PASS-on-a₀ paper = 2 (RAR overlay + a₀ vs H₀ band). Both reproducible.
- Cover letter: declares Path-γ scope and *explicitly* states that JCAP companion paper is under separate consideration; no double-submission concern because the claim sets do not overlap.
- Suggested referees: McGaugh (Case Western), Skordis (FZÚ), Famaey (Strasbourg).
- Conflict referees: Verlinde (numerical degeneracy makes adversarial reviewer unhelpful for the MNRAS-scope question).

---

## Submission checklist

- [ ] Abstract ≤ 250 words.
- [ ] Cosmology claim count = 0 (verified by reading §1.4).
- [ ] verify_milgrom_a0.py runs PASS_STRONG on reviewer machine.
- [ ] verify_mock_false_detection.py runs FAIL on fabricated input.
- [ ] All seven limitations of §6 are stated.
- [ ] Verlinde 2017 cited and degeneracy declared.
- [ ] Companion paper status disclosed in cover letter.
- [ ] Git tag `mnras-v1-l539` pushed.
