# refs/l9_paper_synthesis.md -- L9 Round 9: Revised JCAP Paper Narrative

> Date: 2026-04-11
> Source: All L9 findings (Rounds 1-8) plus L8 results.
> Purpose: Full synthesis of what changes in the JCAP paper from L8 to L9.
> Language standard: refs/l7_honest_phenomenology.md.

---

## Context: What Changed from L8 to L9

L8 concluded:
- Reverse derivation: all Q3x FAIL (3/3 candidates cannot be derived from SQMH)
- A12: STRONG Bayesian evidence (Delta ln Z = +10.77)
- SQMH background ODE = ΛCDM (sigma suppressed 62 orders)
- 8-person critique: "nobody explains why erf proxy works"

L9 adds:
- NEW POSITIVE: Q42 PASS (C28-A12 wa proximity = 0.057 < 0.10)
- NEW NEGATIVE: NF-14 erf impossibility theorem (mathematical proof)
- NEW NEGATIVE: NF-15 S8/H0 structural impossibility (confirmed quantitative)
- NEW: Q45 FAIL (gamma0 scan -- cannot achieve |Δwa| < 0.03 in L6 range)
- NEW: C28-A12 isomorphism depth analysis (Round 8)

---

## Revised Paper Narrative (JCAP submission)

### Abstract Change

OLD (L8): "We test three SQMH-motivated dark energy candidates against DESI DR2.
All three achieve strong Bayesian evidence. Reverse derivation fails at 62-order
scale separation."

NEW (L9 addition): "The RR non-local gravity model (C28) independently yields
wa ~ -0.19, within CPL-level proximity of our best-performing A12 template
(wa = -0.133). We prove that the erf proxy functional form cannot emerge from
any SQMH mechanism (erf impossibility theorem). S8 and H0 tensions are
structurally unresolvable within the present framework (quantified)."

### Section 2 (Theory) -- Changes

ADDITION 1: erf impossibility theorem (NF-14)
  Location: After SQMH background ODE derivation.
  Text: see refs/l9_limitations_language.md (Subsection: erf Proxy Origin)

ADDITION 2: C28-A12 CPL proximity
  Location: After C28 introduction.
  Text: see refs/l9_c28_isomorphism.md (Paper Section Draft)

ADDITION 3: Pi_SQMH structural explanation (NF-5, from L8)
  "Pi_SQMH = Omega_m * H_0 * t_P ~ 10^{-62} explains the 62-order gap as
  the ratio of current Hubble rate to Planck rate."

ADDITION 4: SQMH birth-death process (NF-3, from L8)
  "The SQMH equation is a linear birth-death process with constant production
  rate Gamma_0 and binary collision loss rate sigma*rho_m."

### Section on Results -- Changes

UPGRADE C28 STATUS: From "independent theory" to "structural twin of A12 on wa"
  OLD: "C28 is an independent Maggiore-Mancarella theory."
  NEW: "C28 achieves CPL-level structural proximity to A12 (|Δwa| = 0.057 < DESI sigma_wa),
        while remaining a theoretically independent model. Both are observationally
        degenerate at current DESI DR2 wa precision."

NOTE: "Structural twin" is still too strong. Use "CPL-level structural proximity."
FORBIDDEN: "C28 derives from A12", "C28 = A12", "isomorphism" (without qualification).
ALLOWED: "CPL-level structural proximity", "wa-degenerate at current precision."

### New Section: Limitations (JCAP required)

Full text: see refs/l9_limitations_language.md.
Key subsections:
1. S8 tension: "DeltaS8 = -0.004 (5% of gap); structurally unresolvable"
2. H0 tension: "DeltaH0 = 0.7 km/s/Mpc (12% of gap); pre-recombination required"
3. erf proxy origin: "mathematical proof of impossibility in SQMH"
4. C28 independence: "no derivation between C28 and A12 found"
5. hi_class provisional: "K19 flag remains active"

### Section Ordering for JCAP

Proposed structure:
1. Introduction (SQMH motivation + DESI DR2 context)
2. Theory:
   2.1 SQMH equation (birth-death process, NF-3)
   2.2 Background ODE = ΛCDM (Pi_SQMH ~ 10^{-62}, NF-5)
   2.3 erf impossibility theorem (NF-14)
   2.4 C28 RR non-local gravity (full Dirian, NF-13, Q42)
3. Candidate templates:
   3.1 A12 (erf proxy)
   3.2 C11D (CLW quintessence)
   3.3 C28 (RR non-local)
4. Data and Methodology
5. Results:
   5.1 Bayesian evidence (A12 wins, Delta ln Z = +10.77)
   5.2 C28-A12 CPL proximity (Q42)
   5.3 DR3 falsifiability predictions
6. Discussion:
   6.1 Scale separation (Cramer-Rao obstruction, NF-10)
   6.2 Holographic interpretation (NF-7)
   6.3 Effective EOS (w0^eff ~ -0.83, NF-11)
7. Limitations:
   7.1 S8 tension (structural impossibility, NF-15)
   7.2 H0 tension (structural impossibility, NF-15)
   7.3 erf proxy origin (impossibility theorem, NF-14)
   7.4 hi_class verification (K19 provisional)
8. Conclusion

---

## Section-Level Change Summary

| Section | Change | Source |
|---------|--------|--------|
| Abstract | +erf impossibility, +C28 proximity | NF-14, Q42 |
| Sec 2.1 SQMH | +birth-death, +Pi_SQMH | NF-3, NF-5 |
| Sec 2.2 Background | +62-order structural explanation | NF-5, K41 |
| NEW Sec 2.3 erf impossibility | New | NF-14 |
| NEW Sec 2.4 C28 full Dirian | New | NF-13, Q42 |
| Results: C28 | Upgraded: "CPL structural proximity" | Q42 |
| NEW Limitations | S8, H0, erf, C28 independence | NF-14, NF-15 |
| Discussion | +Cramer-Rao obstruction | NF-10 |

---

## Key Narrative Upgrade: C28

OLD narrative (L8): "C28 is one of three candidates. It passes Bayesian evidence.
  It cannot be derived from SQMH. It is an independent theory."

NEW narrative (L9):
  "C28 (RR non-local gravity) independently generates wa < 0 via a non-local
  gravity action, without any SQMH input. Full Dirian 2015 implementation
  reveals that the UV cross-term +3HVV_dot (absent in L8's simplified treatment)
  is essential for positive dark energy density. The resulting wa_C28 ~ -0.19
  falls within |Δwa| = 0.057 of the A12 template wa_A12 = -0.133.

  At current DESI DR2 precision (sigma_wa ~ 0.24), C28 and A12 are indistinguishable
  on the wa axis. This CPL-level proximity -- while not a derivational relationship --
  suggests that independently motivated theories with wa < 0 occupy a preferred region
  of CPL parameter space that the data selects. C28 provides independent theoretical
  support for wa ~ -0.13 to -0.19 without requiring SQMH assumptions.

  The isomorphism depth is medium level:
  (i) wa numerical proximity: YES (|Δwa| = 0.057 < observational precision)
  (ii) Full E^2(z) identity: NO (different functional forms)
  (iii) Perturbation sector: NO (G_eff/G differs by ~2%)
  (iv) Derivational: NO (independent theories)"

---

## PRD Letter Status Assessment

Current status: JCAP target confirmed (as L8).

PRD Letter upgrade conditions (from L6 T3):
  - Q17 complete derivation: NOT met (NF-14 proves impossibility)
  - Q13+Q14 simultaneous: NOT met (Q41 FAIL, Q43 FAIL)
  - NEW potential: Q42 PASS + Q45 PASS would have enabled "strong isomorphism" claim
  - Q45 FAIL confirmed: PRD Letter upgrade NOT triggered

PRD Letter remains unavailable. JCAP submission is the correct target.

The C28-A12 Q42 result (medium-level isomorphism) is a positive contribution
that strengthens the JCAP paper's narrative without meeting PRD Letter threshold.

---

## What Sections of paper/ Need Updating

Based on the above, the following paper/ files need updating:
1. paper/ (any draft sections on C28) -- add Q42 result and CPL proximity language
2. paper/ (any draft limitations section) -- add NF-14, NF-15 exact language
3. paper/ (abstract if it exists) -- add erf impossibility and C28 proximity
4. paper/ (Section 2 theory) -- add birth-death, Pi_SQMH, erf impossibility

Note: The paper/ directory is not modified in this analysis phase.
These are PRESCRIPTIONS for the next writing phase.

---

*Round 9 completed: 2026-04-11*
