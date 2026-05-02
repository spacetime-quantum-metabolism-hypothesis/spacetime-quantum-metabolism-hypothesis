# L443 REVIEW

## Honest one-liner
F0/F5/F9 = real; F6/F7 = schematic with synthetic data (annotated as such); F1/F2/F3/F4/F8 = labelled placeholders — paper-figures slot is filled but four real-data figures still need their pipelines.

## What was done
- Created `paper/figures/` (already partially populated by L5 corner plots; left untouched).
- Wrote `results/L443/make_figures.py` — single script regenerating all 10 PNGs.
- Generated:
  - `F0_axiom_graph.png` — 6 axioms (L0–L5) → 5 derived predictions (D1–D5) DAG.
  - `F5_rho_q_evolution.png` — uses `results/L207/report.json` (`rho_q_0`, `absorption_per_hubble = 0.104`); two-panel ρ_q(z) and ratio plot.
  - `F6_gmm_sparc.png` — schematic 2-component GMM over synthetic log_σ₀ data; carries inline "replace with real SPARC GMM fit" warning.
  - `F7_mock_injection.png` — schematic null-vs-injection ΔAICc histograms; carries inline "replace with real mock pipeline" warning.
  - `F9_facility_gantt.png` — manually curated 2025–2034 Gantt: DESI DR3/DR4, Euclid DR1/DR3, Rubin LSST Y1/Y10, CMB-S4, LiteBIRD, SKA1.
  - F1/F2/F3/F4/F8: placeholder PNGs with spec text.
- Wrote `paper/figures/README.md` (status table + honesty notes + regen command).
- Wrote L443 ATTACK_DESIGN, NEXT_STEP, REVIEW.

## Compliance checks
- `matplotlib.use('Agg')` set before any pyplot import (CLAUDE.md rule).
- All plot text ASCII (cp949-safe). Greek letters appear only via raw strings in TeX-style labels which matplotlib renders, not via `print()`.
- No theory derivation / parameter fits done inside this task (CLAUDE.md 최우선-1 not engaged — pure plotting task).
- Schematic figures carry visible disclosure both on the PNG itself and in the README — no falsification.

## Risk
F6 and F7 are visually convincing 2-D plots backed by synthetic data. If the paper inadvertently cites them as final SPARC / mock results without regenerating, that would violate "결과 왜곡 금지". README explicitly flags this; NEXT_STEP queues regeneration work.
