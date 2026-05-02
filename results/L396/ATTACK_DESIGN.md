# L396 ATTACK DESIGN — Sec 7 Outlook (Final)

Independent session. Honest one-liner: this is a forward-looking outlook for Sec 7,
not a new measurement; nothing here changes the headline numbers from L46–L99 / L300s.

## Goal
Draft the final form of paper Sec 7 ("Outlook"). Three subsections must close cleanly:
1. **DR3 timeline** — what discriminates SQT phenomenology from LCDM and from
   mainstream alternates (C28 Maggiore-Mancarella RR non-local, C33 f(Q),
   A12 erf-diffusion canonical drift class) once DESI DR3 BAO ships.
2. **Facility map** — which next-decade facilities probe which SQT-relevant
   channel (background w(z), growth f sigma_8, S_8/WL, GW standard sirens, CMB-S4
   compressed-CMB tightening, 21cm intensity mapping cross-check of low-z BAO).
3. **Companion paper** — scope, division, and timing of a phenomenology-only
   companion that reports the L33 / L46 / L48 / L80s grid champions without
   theoretical SQMH framing (defensive split if PRD asks for it).

## Attack lines

### A. DR3 timeline (Sec 7.1)
- Pull the Fisher pairwise discrimination numbers already produced for DR2 in L5
  (C28 vs C33 = 0.19 sigma) and project to DR3 using DESI Y3→Y5 effective volume
  scaling (~1.8x). Honest framing: even with that scaling the 1-parameter
  mainstream pair stays sub-1 sigma; SQT champion (Q93/Q95 family) breaks degeneracy
  primarily through the low-z transition shape of g(z), not through (w0, wa).
- Identify the **decision points** that DR3 will set: (i) BGS DV at z=0.295,
  (ii) LRG D_M/D_H at 0.51/0.706/0.93, (iii) ELG at 1.32, (iv) QSO 1.49, (v) Lyα 2.33.
  For each, list the predicted shift relative to LCDM-Planck for SQT champion vs
  C28 vs C33 (qualitative, sign + ~size, no fabricated numbers).
- Honest caveat: **CLAUDE.md L6 rule** — DR3 scripts at simulations/l6/dr3/
  must NOT be executed before public release. Sec 7.1 reports forecasts, not
  results.

### B. Facility map (Sec 7.2)
Map by SQT-distinctive channel:
| Channel | Facility (≤2030) | Why it matters for SQT |
|---|---|---|
| Background w(z), low-z transition | DESI DR3, Euclid Y1 spectro | Tests the L33 sigmoid weight z_t ≈ 0.4–0.6 directly |
| Growth f sigma_8 | DESI RSD DR2/DR3, Euclid 3x2pt, PFS | SQMH backgrounds with G_eff/G ≈ 1 predict LCDM-like f sigma_8 within 1% — null target |
| S_8 / weak lensing | LSST Y1, Euclid WL, Roman | K15 was structurally fail across L5/L6 winners — Sec 7.2 must state SQT does not predict S_8 relief |
| GW standard sirens | LIGO O5, ET/CE pathfinder | Independent H0 anchor; SQT agnostic but constrains disformal A'≠0 branches via c_T |
| CMB compressed | SPT-3G ongoing, CMB-S4 (~2030+) | Tightens theta_star floor below 0.3% Hu-Sugiyama; sharpens omega_m,h posterior |
| 21cm IM | CHIME ongoing, HIRAX/SKA-Mid | Cross-check of BAO at z ~ 1–3, orthogonal systematics to optical galaxy surveys |

Discipline: avoid claiming SQT *needs* any specific facility. Frame as
"falsifiable channel X tightens by factor Y; SQT champion predicts Z within that".

### C. Companion paper (Sec 7.3)
- Scope: pure phenomenology — L33 g(z) functional form scan, L46/L48 grid wins,
  AICc/BIC tables, no SQMH derivation, no plenum metabolism narrative.
- Authorship/positioning rationale: Q17 partial (amplitude-locking ∝ Ω_m
  partially derived), Q13/Q14 not jointly satisfied → main paper stays JCAP
  ("honest falsifiable phenomenology", per L6 8-person consensus). Companion
  paper is a fallback if a referee asks for theory–data separation.
- Timeline: companion draft frozen at +1 month from main submission;
  released only if requested or if DR3 confirms the L33 family Δχ² > 4 vs LCDM.
- Anti-overclaim guard: companion must NOT cite "extra parameter preferred by
  data" (L5/L6 rule — Δ ln Z gap < Occam penalty for current data).

## Non-goals
- No new MCMC. No DR3 mock chains. No revised numerical headline.
- No edit to Sec 1–6 numbers.

## Output structure
- ATTACK_DESIGN.md (this file) — plan only.
- REVIEW.md — adversarial review against project rules + L5/L6 carry-over guards.
- SEC7_DRAFT.md — final Sec 7 prose, three subsections, ~1.5–2 pages target.
