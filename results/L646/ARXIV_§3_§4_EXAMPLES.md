# L646 — arXiv Draft §3 4-Pillar Covariance + §4 Layered Axioms 본문 예시

**목적**: paper plan v3 (L634) 와 arXiv draft (paper/arXiv_PREPRINT_DRAFT.md) 의 §3/§4 sync gap (L645 발견) 을 해소하기 위한 본문 예시 작성. 본 문서는 plan 한정이며 arXiv draft / paper / claims_status 어떤 디스크 파일도 직접 edit 하지 않음.

**원칙 (CLAUDE.md 최우선-1 준수)**: 수식 0줄, 파라미터 값 0개, 신규 prediction 0건, 신규 후보 0건. 어휘 가이드 L591/L596/L635/L640 sync.

**금지 어휘**: "통합 이론", "0 free parameter", "priori 도출". **권장 어휘**: "PASS_MODERATE", "covariance" (4-pillar cross-validation 의미로만 사용; GR-style "general covariance" 와 혼동 금지를 위해 본문 도입부에서 한 번 명시).

---

## §3 4-Pillar Covariance (4 paragraph, 250-300자/단락)

### §3.1 SK Schwinger-Keldysh Pillar (Closed-Time-Path)

The first pillar grounds the substrate dynamics in closed-time-path (Schwinger-Keldysh) field theory. Working on the doubled time contour allows the framework to track non-equilibrium expectation values of substrate density and current operators without committing to a particular vacuum, which is essential for a cosmological setting where the background itself evolves. The SK formulation independently fixes the operator structure entering the bilinear emission-absorption channel and the sign of the dissipative response, and it does so without any reference to the renormalisation-group, holographic, or symmetry-breaking pillars that follow. This *axiom independence* is what makes the SK pillar a genuine cross-check rather than a restatement: any inconsistency between SK-derived operator content and the structure required by the other three pillars would falsify the construction, and in §3.5 we summarise where this independence has already been tested at PASS_MODERATE level.

### §3.2 Wetterich RG Pillar (Three Fixed Points)

The second pillar is the Wetterich functional renormalisation-group flow, which the framework uses to organise scale dependence across cosmic, cluster, and galactic regimes. Three fixed points emerge from the flow — one associated with the cosmological IR, one with cluster-scale intermediate behaviour, and one with galactic-scale dynamics — and each fixed point is approached along an independent trajectory determined solely by the Wetterich equation, without input from SK operator content or holographic dimensional analysis. The RG pillar therefore supplies an *axiom-independent* skeleton of scale separations: where the three fixed points sit, and how trajectories interpolate between them, is fixed by RG flow alone. Cross-validation against the SK pillar (operator content) and the holographic pillar (dimensional saturation) is what we mean by 4-pillar covariance in this paper, and we document the consistency of the three-fixed-point pattern with the other pillars at PASS_MODERATE level.

### §3.3 Holographic Pillar (Dimensional σ₀)

The third pillar enforces a holographic dimensional relation that ties the substrate's emission coefficient σ₀ to Newton's constant and the Planck time. We emphasise that this pillar enters the framework as a *dimensional* statement — it fixes how σ₀ must scale with G and t_P on dimensional grounds — and it does *not* by itself fix any free numerical coefficient; we are explicit throughout the paper that this is a structural constraint, not a "priori derivation" of a parameter value. The holographic pillar is independent of SK (which fixes operator content) and of Wetterich RG (which fixes scale-flow structure): no SK or RG input is needed to write the dimensional relation. Cross-validation arises because the dimensionally allowed σ₀ must be compatible with the operator coefficients delivered by SK and with the fixed-point structure delivered by Wetterich, and that joint compatibility is the second leg of the 4-pillar covariance test, again currently rated PASS_MODERATE.

### §3.4 Z₂ SSB Pillar (Dark Mass Without Goldstone)

The fourth pillar is a Z₂ spontaneous-symmetry-breaking sector that gives the dark substrate a mass without producing a Goldstone mode. Because the broken symmetry is discrete, no continuous symmetry is lost and no massless scalar appears — this is the structural reason a dark mass scale can coexist with the absence of a fifth-force-like Goldstone signal in cluster and galactic data. The Z₂ SSB pillar is independent of the other three: SK supplies operator structure, Wetterich supplies scale flow, holography supplies dimensional saturation, and Z₂ SSB supplies the discrete-symmetry mass mechanism, each derivable without reference to the others. The 4-pillar covariance claim is then the statement that the four *independently axiomatised* pillars produce a *jointly consistent* picture — operator content (SK), scale skeleton (RG), dimensional balance (holography), and dark-mass mechanism (Z₂ SSB) all agree at PASS_MODERATE level under the cross-validation tests summarised in §3.5.

---

## §4 Layered Axioms (3 paragraph, 250-300자/단락)

### §4.1 Core Axioms (a1 substrate / a2 mass-action / a3 emission balance)

The framework rests on three core axioms that are taken as primitive. Axiom **a1 (substrate)** posits an underlying substrate whose density and current are the fundamental dynamical variables, distinct from the metric and from any matter field; this is the object on which the SK pillar operates. Axiom **a2 (mass-action law)** specifies that the substrate's emission and absorption channels are governed by a mass-action-style balance between substrate occupation and emitted/absorbed quanta, which fixes the gross structure of the bilinear coupling channel without committing to a numerical coefficient. Axiom **a3 (emission balance)** asserts that the steady-state emission and absorption rates obey a detailed-balance condition on cosmological scales, which is what allows the cosmological background equations to close. These three axioms are *core* in the sense that nothing in the paper attempts to derive them from a deeper principle: they are stated, their consequences are computed, and the paper's predictions stand or fall with them.

### §4.2 Derived Axioms (B1 bilinear / a4 geometric 1/(2π) / a6 dark-only)

A second tier of axioms is *derived* in the sense that they follow from the core axioms together with one of the four pillars, and we are explicit in the text that they are derived rather than primitive. The bilinear-coupling axiom **B1** follows from a1+a2 once the SK operator structure of §3.1 is imposed: the lowest-dimension SK-consistent coupling channel is bilinear, and B1 simply names this consequence. The geometric **a4 (1/(2π))** axiom comes from the holographic pillar's dimensional accounting together with the standard 2π factor of phase-space integration; it is geometric and dimensional, not dynamical. The **a6 (dark-only)** axiom — that the substrate couples to the dark sector and not to baryons at the relevant scales — is derived from Z₂ SSB plus the absence of a Goldstone fifth-force channel discussed in §3.4. Labelling these as derived rather than core is the layered-axiom discipline that paper plan v3 (L634) requires.

### §4.3 Hidden DOF Disclosure (9-13 honest items)

The third tier is the explicit disclosure of hidden degrees of freedom — modelling choices that are *not* fixed by the four pillars and that the reader should be able to inspect and challenge. We list 9 to 13 such items, with the exact count and wording set in §4.3 of the draft once 8-person Rule-A review (mandatory before publication) signs off. The disclosed items include: the **anchor pick** for the cosmological-scale substrate density normalisation; the **Υ★** scaling choice in the cluster-scale fit; the **functional form** chosen for the emission-balance kernel where multiple SK-consistent forms remain admissible; the **mass redefinition closure** convention used to absorb counterterms; and several further items in the same category. We frame this section as honest disclosure rather than as a parameter count: the framework is not "0 free parameter", and we do not claim "priori derivation" of these choices. Calling them out at the axiom level — rather than burying them in fit tables — is the L640 honesty discipline that the rest of the paper inherits.

---

## 어휘 가이드 Cross-Reference

- **L591** — "통합 이론" 어휘 영구 금지. 본 §3/§4 본문에서 미사용 확인.
- **L596** — "0 free parameter" / "priori 도출" 영구 금지. §3.3 holographic pillar 와 §4.3 hidden DOF 단락에서 명시적으로 부정문으로 처리.
- **L634 (paper plan v3)** — §3 4-pillar 구조 + §4 layered (core/derived/hidden) 구조의 출처. 본 예시는 plan v3 의 본문 sync.
- **L635** — "PASS_MODERATE" 통일 어휘. §3.1/§3.2/§3.3/§3.4 단락 말미 모두 PASS_MODERATE 사용.
- **L640** — Hidden DOF 정직 disclosure 원칙. §4.3 가 직접 구현.
- **GR-covariance 혼동 방지** — §3 도입부 (별도 § 3.0 or §3 첫 단락) 에서 "covariance" 가 본 논문에서 4-pillar cross-validation 의미로만 사용됨을 한 줄 명시 권장 (본 예시 단락에는 미포함, draft 통합 시 추가).

---

## 8인 Rule-A 의무

본 §3/§4 본문은 **이론 클레임** (4-pillar axiom independence, layered axiom 구조, hidden DOF 9-13 list) 을 포함하므로 CLAUDE.md L6 규칙에 따라 arXiv draft 통합 전 **8인 순차 Rule-A 리뷰 필수**. 본 예시의 단어 선택, 단락 순서, hidden DOF 항목 9-13 의 정확한 wording 모두 8인 합의 후 확정.

코드 변경은 본 산출물에 없음 (Rule-B 4인 리뷰 대상 아님).

---

## 정직 한 줄

본 §3/§4 본문 예시는 paper plan v3 (L634) 의 sync gap (L645 발견) 을 닫기 위한 plan 단계 산출물이며, arXiv draft 자체에 통합되기 전 8인 Rule-A 리뷰를 통과해야 한다. 4-pillar covariance 와 layered axiom 모두 현재 PASS_MODERATE 등급이며, "통합 이론" / "0 free parameter" / "priori 도출" 주장은 본 예시 어디에도 포함되지 않는다.
