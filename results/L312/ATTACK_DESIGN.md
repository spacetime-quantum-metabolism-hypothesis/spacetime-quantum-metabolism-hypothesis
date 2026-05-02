# L312 ATTACK_DESIGN — Paper Section 1-2 (Intro + Axioms) Finalization

**Loop**: L312 (단일 loop, post-L271 -0.05 progression)
**Target**: Section 1 (Introduction) + Section 2 (Axioms & Derived Quantities)
**Status before attack**: Outline-stable, but unaudited from a hostile-reviewer angle.
**Honesty constraint**: Mock injection 100% false-detection rate (L272) and σ_8/H_0 structural limitation (Sec 6.4) MUST be visible in narrative framing.

---

## 8 Attack Vectors (V1–V8)

### V1 — Hook strength (Sec 1, opening 2 paragraphs)
- Current outline opens with "6 cosmological problems" enumeration. Reviewer first-impression test (Cosmology referee, 90-second skim) likely flags this as generic.
- Attack: a referee who reads only the first paragraph must (a) know SQMH is **a metabolism axiom set**, not yet another w(z) parameterization, and (b) see one **falsifiable** claim in the first 200 words (e.g., P15–P22 falsifier list pointer).
- Failure mode if unattacked: paper read as "yet another dark-energy fluid" → desk-reject probability ↑.

### V2 — Motivation completeness vs honest scope (Sec 1.2)
- 6 problems listed (H_0, S_8, w(z) drift, EDE-like phenomenology, BAO low-z anomaly, isotropy). But Sec 6.4 admits σ_8 / H_0 are **structurally unresolved** by SQMH.
- Attack: motivating with problems the theory cannot solve is intellectually dishonest. Either drop H_0/S_8 from motivation or explicitly state "we address (3,4,5); (1,2) are constraints, not targets" up-front in Sec 1.
- This is a Rule-A 8-person-grade claim shift; must be flagged.

### V3 — Prior work coverage (Sec 1.3)
- Required minimum: ΛCDM + DESI DR2 (arXiv 2503.14738), CPL (Chevallier-Polarski-Linder), quintessence reviews (Tsujikawa), IDE (Wang-Meng), modified gravity (Clifton et al. 2012), holographic DE (Li 2004), unimodular/diffusion (Perez-Sudarsky), non-local (Maggiore-Mancarella, Deser-Woodard).
- Attack: any missing class invites "uninformed" reviewer. Specifically check (i) RVM (Solà 2024 ApJ 975 64), (ii) f(Q) (Frusciante 2021), (iii) Chaplygin family (note: family already KILLed in L2 R3 — cite as completed survey, not as live competitor).
- Also: mainstream phenomenology like CLASS-based hi_class must be cited because Sec 5 acknowledges hi_class would be required for full disformal/k-essence.

### V4 — Length & structural balance
- Sec 1 target ≈ 4–6 pages JCAP single-column. Sec 2 target ≈ 3–5 pages.
- Risk: axiom block (a1–a6) + derived (D1–D5) + Branch B 3-regime σ_0 + 4 microscopic pillars (SK + Wetterich RG + Holographic + Z_2) overflows Sec 2 into ≥ 8 pages.
- Attack: split — keep Sec 2 to axioms+derived only; **move 3-regime σ_0 detail to Sec 3 (Background dynamics)** and 4-pillar microscopics to **Sec 4 (Microscopic origin) or Appendix A**. Otherwise Sec 2 reads as a kitchen sink.

### V5 — Key claim clarity
- Required headline claims (status as of L311): (a) BAO-only ★★★★★ improvement = -0.065 (cumulative 211-loop best), (b) joint analysis Δ ln Z modest (Occam-corrected, L6 lesson), (c) 7 falsifiers P15–P22 pre-registered, (d) σ_8/H_0 structurally unresolved (Sec 6.4).
- Attack: Sec 1 must contain one sentence per claim, in order, with quantitative anchor. Currently outline mentions only (a) and (c). Add (b) and (d) explicitly to prevent reviewer "where is honest scope?" objection.

### V6 — Reference adequacy & data provenance
- DESI DR2 official = arXiv 2503.14738 (CobayaSampler/bao_data). DESY5 SN = 2401.02929. Planck 2018 compressed = 1807.06209.
- Attack: every dataset used must be cited with arXiv ID **and** access path (CobayaSampler/sn_data, etc.). Reviewer who knows DR1→DR2 wa shift (CLAUDE.md re-prevent rule) will check first.
- Also: cross-reference L34 joint pipeline (analytical M marginalization, Conley 2011) and Hu-Sugiyama theory floor 0.3% (CLAUDE.md).

### V7 — Abstract ↔ Intro consistency
- Abstract typically drafted last. Risk: claim drift between abstract and Sec 1 once L312–L320 inject new joint numbers.
- Attack: lock a **claim manifest** (5 bullets, numerical) that abstract, intro last paragraph, and conclusion all reference verbatim. Treat manifest as a regression test — any future loop changing a number must update all three.

### V8 — Sec 2 axiom rigor (a1–a6 motivation, D1–D5 derivation, notation)
- a1–a6: each axiom needs (i) physical statement, (ii) operational definition, (iii) where it enters which equation, (iv) which falsifier P15–P22 maps to its violation. Currently outline has (i,ii) only.
- D1–D5 derivation: must cite L296 independence proof (axioms not redundant) and reference T^μν_n tensor formalism from L207. Notation must comply with L134 CONVENTIONS. Microscopic origin pointers (SK, Wetterich RG, Holographic, Z_2) appear here as forward-references to Sec 4.
- Attack: a referee focusing on a single axiom (likely a3 or a4 — metabolism rate σ_0) will demand (a) microscopic motivation, (b) independence from a1/a2, (c) at least one experimental falsifier. If any axiom lacks all three, mark it weak.

---

## Top 3 Recommendations (priority order)

### R1 — Honesty-first restructuring of Sec 1.2 (covers V2, V5, V8)
Rewrite motivation paragraph to **separate targets from constraints**:
- Targets (SQMH addresses): w(z) drift, BAO low-z residual, ★★★★★ -0.065 family.
- Constraints (SQMH must respect): H_0 (CMB+SH0ES), σ_8 (DES-Y3 / KiDS), GW170817 c_T, Cassini γ.
- Explicit sentence: "SQMH does **not** claim to resolve H_0 or σ_8 tensions; Sec 6.4 documents these as structural limitations."
This is a Rule-A 8-person claim shift — must be 8-person reviewed before final LaTeX.

### R2 — Structural split of Sec 2 (covers V4, V8)
- Sec 2 = axioms a1–a6 + derived D1–D5 only (~3 pages).
- Branch B 3-regime σ_0 → Sec 3 (background dynamics).
- 4 microscopic pillars → Sec 4 (microscopic origin) with Appendix A holding SK contour + Wetterich RG flow equations.
- For each axiom add the 4-tuple (statement, operational def, equation entry, falsifier mapping).
- Independence proof: cite L296 in Sec 2 last paragraph; full proof in Appendix A.

### R3 — Lock claim manifest + reference audit (covers V1, V3, V6, V7)
- Draft a 5-bullet **numerical claim manifest** (BAO Δχ², joint Δ ln Z marginalized, falsifier count, σ_8/H_0 disclaimer, mock-injection FDR=100%) and embed verbatim in (abstract, Sec 1 last paragraph, Sec 7 conclusion).
- Reference audit: confirm DESI DR2 arXiv 2503.14738, DESY5 2401.02929, Planck 1807.06209, plus RVM Solà 2024 ApJ 975 64, f(Q) Frusciante 2021, hi_class Zumalacárregui 2017. Add "completed survey" citations for KILLed families (Chaplygin, Perez-Sudarsky, RVM ν<0 BAO-only artefact).
- First-impression hook: rewrite Sec 1 paragraph 1 so a 90-second skim reveals (axiom-based, falsifiable, honest-scope).

---

## Out-of-scope (deliberate)
- No LaTeX edits this loop.
- No new simulation runs.
- No claim that any of {H_0, σ_8} can be solved — V2/R1 enforces opposite.
- 8-person Rule-A review required before R1 lands; 4-person Rule-B review for R3 reference audit script.
