# L443 ATTACK_DESIGN — paper/figures F0–F9 PNG generation

## Goal
Materialise the 10 figure slots specified in `paper/base.md` (lines 1336–1345)
as actual PNG files under `paper/figures/`, using real data where available
and clearly-labelled placeholders elsewhere.

## Strategy
1. Build a single matplotlib script (`make_figures.py`) so regeneration is
   reproducible and side-effect-free (uses `Agg` backend before any pyplot
   calls — CLAUDE.md L4 reminder).
2. Categorise each figure:
   - **Real** (F0, F5, F9): can be drawn from existing artefacts /
     hand-curated content.
   - **Schematic** (F6, F7): the underlying real data isn't routed through
     a current artefact, but the layout/spec is concrete enough to draw with
     synthetic data and an explicit "schematic" overlay.
   - **Placeholder** (F1, F2, F3, F4, F8): no aggregator yet — emit a
     labelled placeholder PNG so the paper build doesn't break and the spec
     stays visible.
3. Inputs:
   - F5 → `results/L207/report.json` (`rho_q_0 = 6.86e-27`, `absorption_per_hubble = 0.104`).
   - F0 → manual axiom/derivation list curated from `paper/02_sqmh_axioms.md` style.
   - F9 → manual 2025–2034 facility timeline.

## Risks / honesty
- F6 and F7 use synthetic data; mis-citing them as real fits would be a
  CLAUDE.md "결과 왜곡 금지" violation. Mitigation: explicit "schematic"
  text annotation drawn into each PNG plus README disclosure.
- ASCII-only text in plot strings to avoid cp949 / unicode issues.

## Out of scope
- Building real F1/F8 IC aggregators or F2/F4 SPARC/Bullet fitters
  (requires multi-day data plumbing — flagged in NEXT_STEP).
