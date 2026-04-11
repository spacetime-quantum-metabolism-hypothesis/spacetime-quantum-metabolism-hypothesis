

---

# Appendix: Independent Alt-20 Candidates (Round N, frozen 2026-04-11)

0-parameter SQMH-native closed-form ρ_DE(a)/OL modifications, amplitude
locked to Ω_m itself, independent of all mainstream DE/MG families
(see `refs/alt20_catalog.md` for the blacklist).

## L2 structural screen (C1-C4)

All 20 candidates modify only the cosmological background: no new scalar
DOF in the static Schwarzschild limit → **C1 Cassini γ−1 = 0 analytically,
PASS for all 20**. Linear perturbation μ(a,k) = 1, c_s² = 1 structurally
→ K11 trivially PASS.

**C4 SQMH sign (ρ_DE monotonically drifting as matter → DE)**: checked
via numerical w(z) from the L3 fit. 15/20 have w_a < 0 (DESI DR2 aligned,
SQMH-consistent). The remaining 5 (A02, A07, A14, A18, plus A04 edge)
have |w_a| ≤ 0.09 or w_a > 0, demoted to **C4-FAIL**.

| ID  | Name                               | C1 | C4 |
|-----|------------------------------------|----|----|
| A01 | SQMH canonical (matter-drift)      | ✓  | ✓  |
| A02 | Quadratic drift                    | ✓  | ✗ w_a=+0.086 |
| A03 | Log horizon entropy                | ✓  | ✓  |
| A04 | Volume-cumulative                  | ✓  | ✓ w_a=−0.469 |
| A05 | Sqrt relaxation                    | ✓  | ✓  |
| A06 | Exponential                        | ✓  | ✓  |
| A07 | cosh                               | ✓  | ✗ w_a=+0.015 |
| A08 | Tanh                               | ✓  | ✓  |
| A09 | Causal-diamond 2D                  | ✓  | ✓  |
| A10 | Reciprocal drift                   | ✓  | ✓  |
| A11 | Sigmoid                            | ✓  | ✓  |
| A12 | Erf diffusion                      | ✓  | ✓  |
| A13 | Arctan plateau                     | ✓  | ✓  |
| A14 | Matter-ratio power                 | ✓  | ✗ w_a=+0.120 |
| A15 | Stretched exp                      | ✓  | ✓  |
| A16 | Second-order Taylor                | ✓  | ✓  |
| A17 | Adiabatic pulse                    | ✓  | ✓  |
| A18 | Gaussian localised                 | ✓  | ✗ w_a=+0.051 |
| A19 | Harmonic fraction                  | ✓  | ✓  |
| A20 | Two-term geometric                 | ✓  | ✓  |

**L2 PASS → L3**: 16 candidates (A01, A03-A06, A08-A13, A15-A17, A19, A20).
**L2 FAIL (C4)**: A02, A07, A14, A18.
