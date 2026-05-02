# L316 ATTACK_DESIGN — Paper Section 6 (Limitations) Final + Honest Disclosure

**Loop**: L316 single
**Subject**: Paper Section 6 (Limitations & Caveats) — final draft, full honest disclosure
**Position thesis**: Sec 6 must be the *most honest* section of the paper. Pre-empt every reasonable reviewer attack by stating it ourselves first, with magnitude and direction.
**Length target**: 2–3 pages (≈ 1500–2200 words), 4 permanent limitation rows + open-issue subsection + L210 audit table reference.

---

## 1. Strategic frame (4-person team rationale)

| Vector | Position | Rationale |
|---|---|---|
| **P (positive)** | Full disclosure raises reviewer trust | Reviewers trained on cosmology overclaim culture (e.g. early-DESI w₀wₐ headlines) reward authors who self-flag tensions before they do |
| **N (negative)** | σ_8 worsening (+1.14%) and BB-mock 100% false-detect are *real* weaknesses; concealment guarantees rejection | These two findings are visible in any independent reanalysis. Failing to disclose ≡ giving reviewer ammunition |
| **O (opportunity)** | JCAP-style "honest phenomenology" positioning improves accept probability over "PRD Letter discovery" framing | L6-T3 8-person consensus: SQT does not meet PRD Letter bar (Q17 partial, Q13/Q14 not joint). Sec 6 anchors the JCAP framing |
| **H (consistency)** | Avoidance ≠ rigor. The paper's Sec 4 (Results) and Sec 5 (Robustness) already concede individual findings — Sec 6 must aggregate them, not re-spin |

**Decision**: Section 6 = aggregation + magnitude reporting + direction-of-bias disclosure. No spin, no hedging language designed to soften.

---

## 2. Section 6 architecture (final)

### 6.1  Permanent limitations (table, 4 rows)

| ID | Limitation | Magnitude | Direction | Mitigation status |
|---|---|---|---|---|
| **L1** | σ_8 / S_8 *worsening* relative to ΛCDM | structural +1.14% (L242); ΔS_8 ≈ +0.003 | SQT increases tension with DES-Y3 | NOT mitigable in background-only μ_eff=1 framework. Requires full perturbation extension (future work) |
| **L2** | H_0 only ~10% of needed shift | L243: relief is structurally bounded ≲ 10% of (73−67)=6 km/s/Mpc gap | SQT reduces but does not resolve H_0 tension | Honest concession; SQT is *not* an H_0-tension solution |
| **L3** | n_s out-of-sample drift | L210 audit OPEN row | direction model-dependent | Acknowledged as open; CMB Planck-only fit; full TT/TE/EE pending |
| **L4** | β-function (RG) treatment phenomenological | L210 audit OPEN row | unknown | Effective parametrisation; UV completion not claimed |

### 6.2  Mock-injection caveat (the BB false-detection finding)

**Core sentence (must appear verbatim in paper)**:
> *In a controlled mock-injection test (L272), the BB-channel pipeline returned a 100% false-detection rate against pure-noise inputs. We therefore treat the BB anchor as a **data-driven prior** rather than an independent detection, and our headline evidence (Sec 4) is reported with and without this anchor (Tab. X).*

**Required follow-up**:
- Cite L272 audit explicitly in supplementary.
- Provide both anchored and un-anchored Δ ln Z columns side-by-side.
- State which of the paper's claims survive the un-anchored variant (currently: structural prediction Q17-partial survives; amplitude-locking exact coefficient does not survive un-anchored — must be downgraded).

### 6.3  Marginalized evidence honesty

**Core sentence**:
> *Our headline marginalized log-evidence advantage over ΛCDM is Δ ln Z = 0.8 (L281), which by Jeffreys' scale is "barely worth mentioning". Earlier internal numbers as large as Δ ln Z ≈ 13 referred to fixed-θ (best-fit) evidence and are not the appropriate Bayesian comparison; we report only the fully marginalized value in the main text.*

This pre-empts the standard reviewer attack ("you're quoting fixed-θ evidence, the real number is much smaller") by stating it ourselves.

### 6.4  Open issues subsection (L210 audit summary)

Reference the L210 14-item self-audit (2 RESOLVED, 4 PARTIAL, 3 ACK, 5 OPEN). Provide the table in supplementary, summarise in main text:

> *Of fourteen reviewer concerns enumerated in our internal audit (L210), two are resolved, four are partially addressed, three are acknowledged, and five remain open. The five open items (n_s drift, β-function UV, full perturbation σ_8, joint MCMC convergence at 5D, and DR3 forecast validation) define our planned follow-up program.*

### 6.5  Scope statement (closing paragraph)

Position SQT explicitly as:
- **Not** a solution to S_8 tension (L1).
- **Not** a complete solution to H_0 tension (L2).
- **A** falsifiable structural prediction (sgn w_a < 0, amplitude-locking partial) testable against DESI DR3.
- Bayesian preference is *modest* (Δ ln Z ≈ 0.8, marginalized).

---

## 3. Reviewer pre-emption checklist

Each anticipated attack → counter-citation in Sec 6:

| Likely reviewer attack | Sec 6 location of pre-emption |
|---|---|
| "You haven't checked S_8" | 6.1 L1 row, magnitude stated |
| "H_0 claim is overstated" | 6.1 L2 row, "only ~10%" |
| "BB anchor looks fishy" | 6.2 verbatim disclosure |
| "Δ ln Z = 13 in your abstract is misleading" | 6.3 — paper never quotes 13 in main text; only marginalized 0.8 |
| "Fixed-θ vs marginalized confusion" | 6.3 |
| "Is this PRD Letter material?" | 6.5 — explicit JCAP-style framing |
| "n_s drift" | 6.1 L3 + 6.4 |
| "β UV-completion?" | 6.1 L4 + 6.4 |

---

## 4. Length budget

- 6.1 table + 1 paragraph: ~400 words
- 6.2 mock-injection: ~350 words
- 6.3 marginalized evidence: ~250 words
- 6.4 open issues: ~250 words
- 6.5 scope statement: ~200 words
- **Total**: ≈ 1450 words ≈ 2 pages two-column. Fits target.

---

## 5. Hard rules for the draft

1. **No softening adverbs** ("merely", "only slightly", "in some sense") in the magnitude statements.
2. **Numerical magnitudes always cited with L-loop ID** (L242, L243, L272, L281, L210) for traceability.
3. **No claim in Sec 6 may contradict Sec 4** — if Sec 4 spins, Sec 6 forces a Sec 4 rewrite.
4. **The word "robust" is banned in Sec 6**.
5. **L286 finding (SQT *worse* than ΛCDM on S_8)** must appear in 6.1 L1 row, not buried.
