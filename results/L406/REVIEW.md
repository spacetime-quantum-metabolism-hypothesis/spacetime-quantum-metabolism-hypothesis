# L406 — 4-Person Code/Result Review

Team self-distributed across (a) ODE/growth correctness, (b) coupling-channel
enumeration, (c) facility-σ literature, (d) honest-framing wording. No
roles pre-assigned (CLAUDE.md L17 rule).

## (a) Growth ODE — CORRECT

`simulations/L406/run.py::growth()` implements
`d²D/dlna² + (2 + dlnH/dlna) dD/dlna − 1.5 Ω_m(a) μ_eff D = 0`
on a=[1e-3, 1] log-grid (600 points), with
- `dlnH/dlna = 0.5·(−3 Ω_m a^−3)/E²` ← matter-only term, OK for ΛCDM bg.
- `μ_eff = 1 + 2 β_eff²` with `β_eff = β0 a^p · f_dark`,
  `f_dark = OL/(Ω_m a^−3 + OL)` — dark-only embedding (Cassini-safe).
- Normalisation at high z (a=1e-3) per CLAUDE.md "raw values, copy
  before /= " rule. Verified `D_raw>0`, finite throughout.

## (b) Coupling-channel coverage — COMPLETE

Four enumerated channels (A1–A4 in NEXT_STEP §A). Confirmed against
CLAUDE.md L2/L4/L6 prior findings:
- A1 (dark-only) → μ ≥ 1 monotone, growth enhanced (CLAUDE.md L5 entry:
  *"C10k β_d~0.107 → σ_8 +2.3%, S_8 tension +6.6 χ² worse"*).
- A2 (pure disformal A'=0) → background ≡ minimal-coupled quintessence
  (CLAUDE.md ZKB 2013 entry).
- A3, A4 forbidden by Cassini / GW170817.

No fifth channel found within the SQT framework axioms.

## (c) Facility σ(S_8) values — VERIFIED literature

| Facility | σ(S_8) | Source |
|---|---|---|
| DES-Y3 | 0.018 | Amon et al. 2022; Secco et al. 2022 |
| Euclid IST | 0.0026 | Euclid Collab. 2020 (Blanchard+) |
| LSST DESC Y10 | 0.0040 | DESC SRD v1 (Mandelbaum+ 2018) |

Forecast n-σ (ΔS_8/σ) computed in `_worker`/main of run.py:
- DES-Y3: 0.63σ (consistent with current non-detection)
- LSST-Y10: 2.85σ
- Euclid: 4.38σ

## (d) Honest-framing wording — APPROVED with one caveat

NEXT_STEP §C wording is internally consistent with paper/base.md §4.6,
§6.1.1 row 1, and §6.1 row 14. Caveat: phrase
*"4.4σ Euclid DR1 falsification target"* should specify it is a *toy
linear-bias forecast assuming ξ_+ ∝ S_8²*. Recommend abstract footnote:
*"forecast assumes Gaussian likelihood with literature σ(S_8); full
hi_class + Euclid mock chain is Phase-7 work."*

## Verdict

Code: PASS. Physics: PASS (mitigation correctly proven structurally
unreachable within fluid level). Framing: PASS with caveat (d).

No bug found. No parameter overfit. AICc penalty N/A (no fit performed,
this is a forward grid + Fisher forecast).

**Recommendation**: integrate NEXT_STEP §C edits into paper sections;
do not attempt mitigation simulation beyond L406; keep §6.1 row 1 as
permanent OBS-FAIL with falsifier upgrade.
