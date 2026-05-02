# L395 — Sec 6 DRAFT (14-row limitations table + 비단조 postdiction caveat)

논문 Section 6 "Limitations and Honest Disclosure" 본문 초안.
- 14행 표는 L368 §3 채택 (변경 없음).
- L346 J1 비단조 fit 판정은 별도 단락 + 행 4 / 행 7 footnote 로 통합 (옵션 C).
- L368 R2 conditional 의 hedging 차단 표현 적용.

---

## 6. Limitations and Honest Disclosure

We document **fourteen acknowledged limitations** of the present formulation. We adopt a strict no-hedging policy: limitations marked *structural* are recognized as permanent within the background-only formulation, and we make no promises of resolution by unspecified future work.

### 6.1 Fourteen-row limitations table

**Table 6.1 — Fourteen acknowledged limitations of the SQT formulation.**

| # | Limitation | Status | Note |
|---|-----------|--------|------|
| 1 | σ_8 +1.14% structural offset | structural | Background-only μ_eff ≈ 1; permanent within current formulation. |
| 2 | H_0 tension only ~10% relieved | partial | Full Boltzmann channel deferred. |
| 3 | n_s out-of-sample (no direct CMB primary prediction) | structural | CMB primary channel not accessible at present. |
| 4 | β-function full first-principle derivation incomplete | partial | Post-hoc anchored; see footnote¹. |
| 5 | Three-regime structure not strictly required | downgraded | Two-regime baseline adopted (cf. L332). |
| 6 | Sloppy effective dimension ≈ 1 | acknowledged | Cluster-dominant reparametrization (L333). |
| 7 | Theory-prior partial only (pillar 4 ★★) | downgraded | See footnote². |
| 8 | Cluster constraint single-source (A1689 only) | plan | Thirteen-cluster archive analysis planned (L335). |
| 9 | Subset Bayes factor only (full 5-dataset joint not run) | plan | 24–30 hr MCMC scheduled (L336). |
| 10 | Microphysical justification 70–80% upper bound | acknowledged | Fifth pillar OPEN (L337). |
| 11 | a4 emergent metric microscopic origin | OPEN | Not derived. |
| 12 | P17 Tier B V(n,t) derivation gate | OPEN | Pre-registration plan; gate not yet passed (L338). |
| 13 | Cosmic-shear / S_8 external channel not fitted | structural | Background-only formulation; consistent with, but not predicted by, current theory. |
| 14 | DR3-class blinded validation not yet performed | plan | OSF + arXiv timestamped pre-registration in preparation. |

Counts: 4 permanent + 6 (L322–L330) + 2 (L332–L340) + 2 (L368) = **14**.

**Footnote 1 (row 4).** The incompleteness of the β-function derivation shares its underlying cause with the postdiction caveat in §6.2: the four pillars permit but do not enforce the observed σ_0(z) shape.

**Footnote 2 (row 7).** The ★★ rating reflects the qualitative pillar-by-pillar assessment of L346 (axis A1): no individual pillar enforces the non-monotonic σ_0(z) shape, and the combined pillars do not fix the location of the extremum.

### 6.2 Non-monotonic σ_0(z) is a postdiction, not a prediction

We state explicitly that the non-monotonic shape of σ_0(z) reported in earlier sections is a **postdiction** — a feature observed in the data and found to be *consistent with* the four-pillar structure of SQT — and **not** an a priori prediction derived from those pillars before exposure to the data. The historical record (results/L67, L68) shows non-monotonicity was first identified as a data-fit pattern, with mechanism searches following afterwards. The pillar-by-pillar analysis of L346 finds:

- The RG-saddle pillar *permits* sign change but does not enforce it.
- The holographic pillar assigns no sign to the monotonicity of σ_0.
- The Z_2 pillar requires evenness about its symmetry point, which is consistent with — but does not require — sign change.
- The fourth (a4 / scaling) pillar remains OPEN at the microscopic level (row 11).

Consequently the four pillars **do not assign a strong a priori probability** to the non-monotonic shape, and they **do not predict** the location z_* ≈ O(0.5) of the observed extremum. We therefore use the language *postdiction* throughout this paper. To convert the non-monotonic shape into a falsifiable prediction would require completion of the P17 Tier B V(n,t) derivation gate (row 12), which remains OPEN.

This caveat is stated once here; we have removed corresponding "predicts non-monotonic" language elsewhere in the manuscript.

### 6.3 Scope of disclosure

Items marked *structural* (rows 1, 3, 13) are acknowledged permanent within the background-only formulation and are **not** offered for resolution by unspecified future work. Items marked *plan* (rows 8, 9, 14) refer to analyses with concrete scope and budget but no completed result at submission. Items marked *OPEN* (rows 11, 12) are theoretical gates that remain unsatisfied; we make no claim of imminent closure. Items marked *partial* / *downgraded* / *acknowledged* are quantitatively bounded in the corresponding loop reports cited in the rightmost column.

Cross-references: BMA evidence accounting in §5 is conditional on the limitations of rows 9 and 12; future-work language in §7 is restricted to plan-status items only and contains no promises about structural items.

---

## 정직 한 줄

> 14행 한계 표 + 비단조 σ_0(z) 는 prediction 아닌 postdiction 임을 본문 한 단락 + 두 footnote 로 명시, hedging 표현 0개.
