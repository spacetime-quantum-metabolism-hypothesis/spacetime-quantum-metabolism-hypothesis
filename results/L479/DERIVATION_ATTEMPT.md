# L479 — Holographic energy-density crossing: priori derivation attempt

**Status**: free derivation attempt, single author. No team session.
**Date**: 2026-05-01
**Scope**: extend L463 free speculation by mapping the surviving sub-hypothesis
("energy-density crossing", not dof-count crossing) onto paper foundation 3
and derived 4, and check whether *cluster mass scale* is the unique
crossing scale.

## 1. The two paper anchors

### 1.1 Foundation 3 (UV holographic identity)

Paper §2 / paper/base.md table 2.4 row 3:
```
sigma_0 = 4 pi G t_P     (PASS_IDENTITY, axiom-level)
```
Equivalent UV-IR statement (Cohen-Kaplan-Nelson form):
```
rho_vac(L) * L^4  <=  M_P^2 * L^2     =>     rho_UV(L) ~ M_P^2 c^2 / L^2
                                                       = c^2 / (G L^2)
                                              (mass density, kg/m^3)
```
The second equality uses `M_P^2 = hbar c / G` so `M_P^2 / hbar` cancels
to `c/G`, and `hbar` drops out — the bound is **classical** in the
mass-density form.

### 1.2 Derived 4 (Lambda origin, ρ_q via n*epsilon/c^2)

Paper §5.2 / claims_status.json `Lambda_origin = CONSISTENCY_CHECK`:
```
rho_Lambda = n_inf * epsilon / c^2  =  rho_Planck / (4 pi)
                                    ~  4.10e95 kg/m^3
```
This sets the *system-mass* side ceiling: a self-gravitating system of
radius R, mass M has mean density
```
rho_sys(R, M) = M / (4/3 pi R^3).
```
The Bekenstein/black-hole limit (when M → c^2 R / 2G) saturates this
side at `rho_BH(R) = 3 c^2 / (8 pi G R^2)`.

## 2. The crossing condition

L463 surviving sub-hypothesis equates `rho_UV` and `rho_sys`:
```
c^2 / (G L^2)  =  M / (4/3 pi L^3)
=> M*(L) = (4 pi / 3) * c^2 L / G
```
Numerical:
- L = 1 kpc      → M* ≈ 1.3e18  M_sun
- L = 1 Mpc      → M* ≈ 8.8e19  M_sun
- L = 100 Mpc    → M* ≈ 8.8e21  M_sun

## 3. Priori check — does it pick out clusters?

| anchor              | R [Mpc] | M [M_sun] | M*(R) [M_sun] | log10 M/M* |
|---------------------|---------|-----------|---------------|------------|
| Globular cluster    |  3e-5   |  1e6      | 2.6e15        | -9.42      |
| Dwarf galaxy        |  1e-3   |  1e9      | 8.8e16        | -7.94      |
| Milky Way disk      |  0.015  |  1e12     | 1.3e18        | -6.12      |
| Galaxy halo         |  0.2    |  2e12     | 1.8e19        | -6.94      |
| Galaxy group        |  0.5    |  5e13     | 4.4e19        | -5.94      |
| **Virgo cluster**   |  2.0    |  1.2e15   | 1.8e20        | **-5.16**  |
| **Coma cluster**    |  3.0    |  1.5e15   | 2.6e20        | **-5.24**  |
| **Massive cluster** |  2.5    |  2.0e15   | 2.2e20        | **-5.04**  |
| Supercluster        |  50     |  1e17     | 4.4e21        | -4.64      |
| BAO scale           |  150    |  1e18     | 1.3e22        | -4.12      |
| Hubble volume       |  4400   |  1e23     | 3.9e23        | **-0.59**  |

Real cluster masses sit **~5 orders of magnitude below** the crossing
line. The Hubble volume is the only anchor within 1 dex of the crossing
(by construction — that *is* the cosmic horizon mass).

## 4. Why the crossing is not cluster-specific

Algebraic check:
```
M_BH(R) = R c^2 / (2 G)
M*(R)  = (4 pi/3) R c^2 / G
M*/M_BH = (4 pi/3) / (1/2) = 8 pi / 3 ~ 8.378   (scale-free constant)
```
The crossing line is **just the Schwarzschild line scaled by ~8.38**.
It is the universal "this object is a black hole" curve — not a feature
of cluster physics. No real bound astrophysical system except the cosmic
horizon itself sits near it.

## 5. Mapping back to paper foundation 3 / derived 4

The crossing equates two quantities that *both* live at the saturation
edge:
- `rho_UV(L) = c^2/(G L^2)` is the holographic *upper bound* on vacuum
  density at scale L (foundation 3 channel, UV).
- `rho_sys(L, M_BH)` is the upper bound on bound-state density at the
  Schwarzschild limit (derived 4 channel, IR).

Both are *ceilings*. Where they meet the system itself must be a black
hole of the relevant size. Real clusters live ~10^5 below this ceiling,
so the crossing is **structurally far** from any non-degenerate
astrophysical regime. The numerical coincidence noted in L463 §4
(M ~ 5e15–2e16 M_sun at L ~ 1–3 Mpc) used different prefactors
(`M ~ M_P^2 L`, missing the 4π/3 and a c^2/G consistency) — when the
correct prefactors are restored, the crossing rises by 5 dex and clusters
fall away.

## 6. Falsification of every other mass scale

The simulation tests 11 anchors from globular clusters (3e-5 Mpc) to
Hubble volume (4400 Mpc). Every astrophysical bound system sits at
log10(M/M*) ∈ [-9.4, -4.1]. Only the cosmic horizon (-0.59) approaches
the line. **Cluster scale is not singled out at all** — it sits in the
middle of a smooth excess curve.

## 7. Verdict (one line, honest)

**Priori 도출 불가능** — the holographic energy-density crossing reduces
to the Schwarzschild line × 8.38 and selects black-hole-density systems
only; cluster scale enjoys no special status.

## 8. What survives for future work

1. The L463 dof-crossing was already negative; this L479 attempt closes
   the energy-density variant as well. The "cluster-scale dip in
   effective sigma_0" claim cannot be derived from any naive holographic
   crossing of foundation 3 and derived 4.
2. If a cluster-scale signature does appear in data, it must come from
   a *different* mechanism (e.g. R5 quantum sector M_PBH window, axiom-4
   Z2 vacuum domain, or a dedicated 5th-pillar microscopic structure).
   It is **not** holographic in the CKN/Bekenstein sense.
3. Foundation 3 and derived 4 remain consistent with each other (both
   live at the Planck-density ceiling rho_P/(4π)) but their consistency
   does not generate a new mass-scale prediction. The Λ origin claim
   keeps its CONSISTENCY_CHECK status (paper §5.2, L412 down-grade).

## 9. Outputs

- `simulations/L479/run.py` — verifies the algebraic identity
  M*/M_BH = 8π/3 and prints the 11-anchor table.

## 10. Honest one-line summary

Holographic foundation 3 × derived 4 energy-density crossing ≡ Schwarzschild
line; not cluster-specific; **priori 도출 불가능**.
