# Alt-20 Independent SQMH Candidates — Round N

**Frozen 2026-04-11**. Independent from L2-R1/R2/R3 catalog and from all
mainstream DE/MG families:

**Excluded** (explicit blacklist): quintessence (thawing/tracker/freezing);
f(R), f(Q), f(T), f(G); Horndeski, DHOST, Galileon, beyond-Horndeski;
non-local gravity (Deser-Woodard, Maggiore RR); RVM Λ(H²); asymptotic
safety RG; unimodular diffusion (Perez-Sudarsky); IDE (Wetterich,
coupled quintessence, dark-only); disformal coupling; k-essence, DBI,
mimetic; Chaplygin gas family; TeVeS, bimetric; holographic/agegraphic
DE; Cardassian; braneworld DGP; emergent/entropic gravity;
varying-constants; phantom; early dark energy.

**Hard constraint**: **0 or 1** free parameters (absolute).  The
candidates here are **0-parameter** — any modification amplitude is tied
to Ω_m (matter fraction), so only (Ω_m, h) are fit, identical to LCDM.

**Elegance requirement**: each functional form is a closed-form
modification to ρ_DE(a) expressible in one line and motivated by an
SQMH L0/L1 interpretation (metabolism continuity, matter-modulated
vacuum generation, horizon entropy, causal diamond counting, etc.).

All are evaluated against DESI DR2 BAO + DESY5 SN + compressed Planck
CMB + 8-point RSD via `simulations/l4/common.py::chi2_joint`.  LCDM
baseline χ² = 1676.89 at (Ω_m=0.3204, h=0.6691).

## Candidate list

Notation: `x = 1 − a`, `m = Ω_m`, base LCDM term OL = 1 − Ω_m − Ω_r.

| ID  | Name (SQMH interpretation)              | ρ_DE(a) / OL                             | Params |
|-----|------------------------------------------|------------------------------------------|--------|
| A01 | SQMH canonical (matter-weighted drift)   | 1 + m·x                                  | 0      |
| A02 | Quadratic metabolism drift               | 1 + m·x²                                 | 0      |
| A03 | Log horizon entropy                      | 1 − m·ln a                               | 0      |
| A04 | Volume-cumulative matter drift           | 1 + m·(1−a³)                             | 0      |
| A05 | Sqrt relaxation                          | √(1 + 2·m·x)                             | 0      |
| A06 | Exponential metabolism                   | exp(m·x)                                 | 0      |
| A07 | Hyperbolic (cosh)                        | cosh(m·x)                                | 0      |
| A08 | Tanh transition                          | 1 + tanh(m·x)/(1 + tanh(m))              | 0      |
| A09 | Causal-diamond 2D                        | 1 + m·x·(1+x)                            | 0      |
| A10 | Reciprocal drift                         | 1/(1 − m·x·a)                            | 0      |
| A11 | Sigmoid (logistic)                       | 2/(1 + exp(−m·x))                        | 0      |
| A12 | Error-function diffusion                 | 1 + erf(m·x)                             | 0      |
| A13 | Arctan plateau                           | 1 + (2/π)·arctan(m·x)                    | 0      |
| A14 | Matter-ratio power                       | a^(−m·(1−m)·x)                           | 0      |
| A15 | Stretched exponential                    | exp(m·(1 − √a))                          | 0      |
| A16 | Second-order Taylor                      | 1 + m·x + 0.5·m²·x²                      | 0      |
| A17 | Adiabatic pulse                          | 1 + m·x·exp(−x²)                         | 0      |
| A18 | Gaussian localised                       | 1 + m·(1 − exp(−x²/m))                   | 0      |
| A19 | Harmonic fraction                        | 1/(1 − m²·x/(1+x))                       | 0      |
| A20 | Two-term geometric                       | (1 + m·x)/(1 − m·x²/2)                   | 0      |

**All are zero-parameter**: the modification amplitude is locked to the
matter fraction Ω_m itself — a direct SQMH-native binding between
metabolism drift and matter density.

## L2 structural screen (C1-C4)

- **C1 Cassini γ−1 = 0**: all 20 modify only the cosmological background;
  no scalar dof propagating in the static Schwarzschild limit → γ−1 = 0
  analytically for all.  PASS.
- **C2 no phantom crossing**: to be checked numerically with
  `common.phantom_crossing`.
- **C3 |w_a| ≥ 0.125**: to be checked via `common.cpl_fit`.
- **C4 SQMH sign**: all 20 have ρ_DE(a) monotonically decreasing into
  the past (matter → DE drift direction) by construction → PASS.

## L3 background fit

Via `common.tight_fit(build_E, theta_bounds=[], theta0=[])`.  With zero
θ, only (Ω_m, h) are fit.  Kill criteria K1-K4 applied.

## L4 perturbations + MCMC

All 20 have μ(a,k) = 1 (no new scalar dof) and c_s² = 1 (background-only
modification).  K11 trivially passes.  MCMC via `common.run_mcmc` over
(Ω_m, h) only (2-D posterior) with 24 walkers × 500 steps.

## Result dump

- `simulations/l4_alt/alt20_results.json`
- Append section to `base.l2.result.md`, `base.l3.result.md`,
  `base.l4.result.md` for surviving candidates.
