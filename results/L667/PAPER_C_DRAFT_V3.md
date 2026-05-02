# Paper C — Draft v3 (Plan Document)

**Status**: paper *plan* document (no manuscript edit, no claims_status edit, no disk artefact edit)
**Lineage**: L661 v2 → L667 v3 retro-update
**Inputs absorbed**:
- L663 (skeptical findings — 10 deprivation triggers)
- L664 (5 mandatory items plan)
- L665 (acceptance downgrade — 35–50% skeptical band)
- L666 (§6 design objective refresh — *acceptance optimization removed*)
**Honesty one-liner**: *Paper C v3 is a falsifiable phenomenology submission with marketing intent zero; honesty assets are an incidental property of the framing, never the primary objective.*
**Constraint compliance**: zero formulas, zero parameter values, zero disk-file edits outside this plan document.

---

## 0. Abstract (revised)

Replace v2 abstract framing with the following plan-level requirements:

- Remove any standalone "63–72%" acceptance citation. L665 imposes **two-sided citation discipline**: any acceptance band must appear adjacent to its skeptical counter-band, and neither band may be quoted as a headline figure.
- Insert the explicit phrase **"marketing intent zero"** as a structural commitment of the abstract (per L666 §6 design objective refresh). The abstract states that the paper does *not* optimise for acceptance probability, reviewer persuasion, or community uptake.
- Reposition the **honesty assets** (retraction discipline, fabrication disclosure, deprivation log) as **incidental** properties of the falsifiability commitment — they are *not* the primary scientific objective and must not be foregrounded as a selling point.
- Primary objective restated as: *publish the falsifiable phenomenology of the SQMH dark sector at the level the data currently licenses, including the active limitations*.

## 5. Quantitative predictions (revised)

The v2 wording **"4/4 PPN PASS"** is retracted at the abstract, body, and table-of-claims level.

Replacement plan (per L664 mandatory item 4):

- State the channel result as **"1/4 dark-only PASS, 3/4 N/A under axiom 6"**.
- Cross-reference **L506 channel-dependence finding** as the originating retraction.
- Add a sentence noting that the previous "4/4" claim was a universality assertion that L506 invalidated; the dark-only PASS is a sectoral statement and cannot be advertised as universal PPN compliance.
- The §5 table of quantitative predictions must show, in a single column, the *current* channel status alongside the *retracted* v2 status, so readers see the change rather than the new wording alone.

## 6. Active limitations (restructured)

§6 is rebuilt around L666 design + L664 mandatory items 2, 4, 5. Acceptance-optimised softeners from v2 are removed.

### §6.1 — Quantitative hidden-DOF table (L664 item 2)

- Itemise the **9 baseline hidden DOF** identified in prior phases.
- Add the **4 extension DOF** surfaced by the current candidate set.
- Total **13 DOF**, presented as a table (DOF name, sector, status, citation).
- Pair the table with the **ΔAICc penalty** discussion from L502 so readers see the information-criterion cost of the hidden DOF, not just the count.

### §6.2 — Channel retraction (L664 item 4)

- Explicit "**4/4 → 1/4 dark-only**" statement, repeated from §5 in limitations form.
- Re-state **L506 cross-form universal FAIL** at 4/4 level.
- Remove any v2 phrasing that implied screening or Vainshtein universality.

### §6.3 — Postdiction admission

- Acknowledge the **3-regime σ₀(env)** structure as a *post-hoc* discovery, not a prediction.
- State plainly that an **out-of-sample test is currently absent**, and that L664 item 5 (held-out predictive test) is not yet satisfied.
- No language in §6.3 may frame the postdiction as prediction-equivalent.

### §6.4 — Fabrication disclosure (cross-mention only)

- Reference the L564 fabrication disclosure — cross-mention only, no re-litigation in §6.
- Pointer to the standalone disclosure document.

### §6.5 — Priori 4 deprivations

- Enumerate the four a-priori deprivations: L549, L552, L562, L566.
- One sentence per deprivation, no defence text.

### §6.6 — Mass redefinition closed permanently

- Cite L582 as the permanent closure of the mass-redefinition route.
- Do not leave the door open in §7 outlook.

### §6.7 — Paradigm-shift deprivation risk

- State the residual risk that further deprivation events could remove the remaining structural claims.
- Explicit non-defence: do not list mitigations that read as acceptance-optimising.

## 7. Outlook (revised)

- **L664 item 1 — OSF preregistration timestamp**: outlook commits to depositing the predictive test specification on OSF *before* DESI DR3 is released, with the timestamp publicly verifiable. The DR3 prohibition from CLAUDE.md (no DR3 script execution prior to public release) is honoured; OSF preregistration is the timestamp vehicle, not DR3 access.
- **L660 BCNF protocol**: cross-reference for the predictive workflow.
- **L664 item 5 — held-out predictive test definition**: §7 must define the held-out test in operational terms (data product, channel, falsification threshold, decision rule) without committing to specific parameter values in this plan document.

## 8. Reproducibility (revised)

- **verify_*.py 7/7 PASS** to be reported as a status line, not as a quality argument.
- **claims_status v1.3 + erratum** explicitly cited; the erratum is not hidden in supplementary material.
- **OSF DOI workflow** (per L664 item 1) described as the canonical reproducibility anchor for the held-out test, with the GitHub mirror as secondary.

---

## v2 → v3 change matrix

| Section | v2 statement (summary) | v3 plan statement (summary) | Driver |
|---|---|---|---|
| §0 Abstract | acceptance band cited; honesty as headline | two-sided citation; marketing intent zero; honesty incidental | L665, L666 |
| §5 Predictions | "4/4 PPN PASS" | "1/4 dark-only PASS, 3/4 N/A under axiom 6" | L664-4, L506 |
| §6 Limitations | acceptance-softened narrative | restructured §6.1–§6.7, no softeners | L666, L664-2/4/5 |
| §6.1 | hidden-DOF qualitative mention | quantitative 13-DOF table + ΔAICc | L664-2, L502 |
| §6.2 | channel universality preserved | explicit channel retraction | L664-4, L506 |
| §6.3 | postdiction equated to prediction | postdiction admission, OOS gap acknowledged | L664-5 |
| §6.4 | fabrication minimised | cross-mention only, no minimisation | L564 |
| §6.5 | priori deprivations dispersed | enumerated four-line block | L549/L552/L562/L566 |
| §6.6 | mass-redef left ambiguous | permanent closure cite | L582 |
| §6.7 | paradigm risk absent | explicit risk paragraph | L666 |
| §7 Outlook | DR3 forward-reference | OSF preregistration before DR3; BCNF cross-ref; held-out test defined operationally | L664-1/5, L660 |
| §8 Reproducibility | github-only | verify 7/7 + claims v1.3 + erratum + OSF DOI | L664-1 |

## Lexicon harmonisation

- L654 + L666 vocabulary synchronisation enforced across §0–§8.
- The phrase **"marketing intent zero"** is a body-text commitment, not only an abstract slogan — it must be reused verbatim in §6 and §7.
- Acceptance-band language ("likely accepted", "well received", "favourable") is removed throughout. Where acceptance is mentioned at all, it appears only as a two-sided band per L665.

## Mandatory 8-person Rule-A review

This plan document triggers Rule-A (theoretical-claim review) before any text from it is migrated into the manuscript draft. Items requiring 8-person review:

- abstract repositioning (marketing intent zero, honesty incidental)
- §5 channel retraction wording
- §6.1 hidden-DOF total (9 + 4 = 13) and the framing of ΔAICc penalty
- §6.3 postdiction-vs-prediction language
- §6.7 paradigm-shift deprivation risk paragraph
- §7 OSF preregistration commitment and held-out test operational definition

Code-level items (verify_*.py status reporting, OSF DOI workflow scripting) follow Rule-B (4-person) review when they reach implementation; this plan document does not author code.

## Constraints honoured

- No formulas.
- No parameter values.
- No edit to the manuscript, claims_status, verify scripts, or any other on-disk artefact.
- Single output file: this plan document.

## Honesty one-liner (closing)

*Paper C v3 publishes what the data licenses, retracts what L506 invalidated, admits what is postdiction, and pre-commits the held-out test on OSF before DR3 — with marketing intent zero.*
