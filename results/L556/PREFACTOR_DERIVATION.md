# L556 — Geometric Prefactor Derivation: Direction-Only Exploration

**Status**: Direction scouting only. No derivation performed.
**Constraint**: CLAUDE.md [최우선-1] strictly observed — zero formulas, zero parameter values, zero derivation hints.
**Purpose**: Identify the two most promising *directions* among six candidates for a future Round 10 8-인 Rule-A 독립 도출 attempt.

---

## §1. Six Candidate Directions (direction names only)

| # | Direction (name only) | Physics pillar association | Conceptual handle (no math) |
|---|---|---|---|
| D1 | Disc azimuthal projection sharpened beyond simple angular averaging | (none — geometric) | Whether the paper's azimuthal averaging is actually a deeper quantization-measure constraint rather than a kinematic projection |
| D2 | Holographic boundary integration on a 2-sphere | Pillar — Holography | Whether boundary-area normalization on a closed 2-surface in an AdS-style setup carries an intrinsic angular-measure factor |
| D3 | Loop-quantum-gravity minimum-area discreteness | (extra-pillar — LQG) | Whether the discrete area spectrum of LQG admits a mapping onto SQT's quantum unit of dissipation/absorption |
| D4 | Closed-time-path / Schwinger-Keldysh path-integral measure | Pillar — SK propagator | Whether the CTP contour's functional measure carries a Jacobian normalization tied to angular phase-space |
| D5 | Z₂ domain-wall topological-charge integration | Pillar — Z₂ SSB | Whether the topological-charge counting of Z₂ wall configurations supplies an angular-measure factor |
| D6 | SO(2) character-integral / Haar-measure normalization | (group-theoretic) | Whether the compact-group invariant measure on the rotation group naturally supplies the prefactor |

(Strictly direction names. No formulas, coefficients, or derivation paths are written here, in conformance with [최우선-1].)

---

## §2. Top-2 Selection and Tentative Priori Grade

Selection rule applied: *(a)* explicit overlap with one of the four declared SQT pillars (so the derivation, if successful, is *not* an external import); *(b)* historical track record of producing closed-form angular-measure factors in independent physics literature; *(c)* compatibility with SQT's existing Axiom-4 statement so that a successful derivation reduces — rather than expands — the hidden-DOF count.

**Top-1 — D4 (Schwinger-Keldysh path-integral measure)**
- Pillar coverage: direct (SK is one of the four SQT pillars).
- Why promising as a *direction*: CTP measures are a standard locus where angular Jacobian factors appear in independent QFT literature. A derivation channel here would be *internal* to SQT (no new pillar imported).
- Tentative priori grade (direction only, before any derivation attempt): **L1 candidate — plausible**.
- Risk: the actual factor produced by a CTP measure is not guaranteed to coincide with the paper's stated geometric prefactor. Coincidence-vs-derivation must be adjudicated in Round 10.

**Top-2 — D2 (Holographic boundary integration)**
- Pillar coverage: direct (holography is one of the four SQT pillars).
- Why promising as a *direction*: closed 2-surface integrations in holographic setups have produced angular-area normalizations in independent literature. Possible compatibility with the σ₀ = 4πG·t_P factor structure already accepted in SQT (paper §1.2.2).
- Tentative priori grade (direction only): **L1–L2 candidate — plausible-but-fragile**. The fragility is that holographic angular factors more commonly appear as 4π or related, and the *specific* factor in question would need a non-trivial second projection step to emerge. That second step is precisely the unknown.
- Risk: outcome may be a *family* of related factors rather than the unique target factor; uniqueness must be demonstrated, not assumed.

**Demoted directions (and why, in one line each)**
- D1 — Direction is shallow as stated (re-statement of paper's existing language); unlikely to add information.
- D3 — Imports an extra pillar (LQG) not currently part of SQT's four-pillar scaffold; success would *raise* hidden-DOF count, not lower it.
- D5 — Topological-charge integration produces *integers*, not angular-measure factors; structural mismatch.
- D6 — Pure group-theoretic normalization is ungrounded in any SQT pillar; would be flagged as an external assumption rather than a derivation.

---

## §3. Round 10 Rule-A Trigger Recommendation (8-인)

**Recommendation**: Trigger Round 10 with the 8-인 panel given **D4 as primary direction, D2 as secondary**. The panel is to derive the prefactor *independently* — only the two direction names are provided, no formula and no expected outcome.

**Success criterion (binary, reported by panel)**
- A first-principles derivation channel is produced that yields the paper's stated prefactor as a *unique* and *parameter-free* consequence of either the SK measure (D4) or the holographic boundary integration (D2). Coefficient must emerge without tuning.

**Outcome accounting (if and only if success criterion met)**
- Hidden DOF count: −1 (Axiom-4's geometric plausibility caveat retired).
- a₀ channel: eligible to revisit and potentially restore PASS_STRONG, contingent on independent re-audit.
- Paper §1.2.2 / preprint §3 language: replace "geometric plausibility, not first-principles" with the derived statement, with full audit trail.

**Outcome accounting if Round 10 fails**
- Hidden DOF count: unchanged at the L552 baseline.
- D4 / D2 status: marked KILLED at the priori level (no further attempts on these directions without new physics input).
- 5th-path #1 retired from the active candidate list; the falsifiable-phenomenology positioning of L6 stands.

**Procedural guardrails for Round 10**
- Rule-A 8-인 sequential review (per L6 procedural rule for theoretical claims).
- Panel must not be shown this document's §2 grading or any pillar-association table — only the two direction names.
- Independent derivation requirement: each of the 8 reviewers attempts the channel without seeing the others' attempts until step 6 of the sequence.
- Honest-failure clause: a "no derivation found" outcome is a valid and reportable result; falsified or partial derivations must be logged in `base.fix.md` per project rules.

---

## §4. Honesty Statement (one line)

**This L556 document performed zero priori derivations; it provides direction names only, with the actual derivation deferred to a future Round 10 8-인 Rule-A panel.**

---

*End of L556 PREFACTOR_DERIVATION.md.*
