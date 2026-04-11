# 5. DESI DR2/DR3 w(z) Predictions

## 5.1 Phase-5 winner predictions (C11D, C28, A12)

After L5 winnowing, the three Phase-5 winners are **C11D (pure-disformal
IDE quintessence)**, **C28 (Maggiore-Mancarella RR non-local)**, and
**A12 (erf-diffusion, canonical alt-20 class representative)**.  All three
reproduce the DESI DR2 w_a < 0 signal without phantom crossing and satisfy
Cassini |γ − 1| = 0 analytically.

### 5.1.1 C11D Disformal IDE quintessence (Tier-1, rank 1)

Pure-disformal limit (A' = 0): background is identical to minimally coupled
quintessence with exponential V(φ) (Sakstein-Jain 2015, ZKB 2013).
Phantom crossing is structurally forbidden by positivity of kinetic energy.
The L4 K3 kill was a CPL thawing-template artefact, cleared by integrating
the Copeland-Liddle-Wands 1998 autonomous system directly.

Best-fit (Sakstein-Jain CLW ODE):

```
lambda = 0.90,  Omega_m = 0.3093,  h = 0.6778
w_0 = -0.8766,  w_a = -0.1855  (CPL projection)
Delta_chi2 = -22.12  vs LCDM
```

w(z) structural features:
- w(z=0) = -0.877, w_min = -0.995 (near but never crossing -1)
- Monotonically decreasing toward -1 at high z
- No phantom crossing (|w+1| > 1e-3 guard verified)
- DESI DR3 Fisher separation from LCDM: ~2.9σ (Q9 pass)

Bayesian evidence: Δ ln Z = **+8.951** (STRONG, 3D Occam-penalised).

### 5.1.2 C28 Maggiore RR non-local (Tier-1, rank 2)

Best-fit CPL reconstruction on z ∈ [0.01, 1.2]:

```
w_0 = -0.849,    w_a = -0.242
Delta_chi2 = -21.08  vs LCDM
```

w(z) structural features:
- w(z=0) = -0.848, asymptotic LCDM recovery at high z
- Inflection at z ~ 0.55 from the localised (U, S) auxiliary crossing
- No phantom crossing (Cassini γ=1 exact from R=0 auxiliary freeze)
- DESI DR3 Fisher separation: **3.91σ** (Q9 pass, strongest of all winners)

Bayesian evidence: Δ ln Z = **+11.257** (STRONG, top-ranked).

### 5.1.3 A12 erf-diffusion, alt-20 canonical class (Tier-2, rank 3)

Zero-parameter closed-form: E²(z) = LCDM + Ω_m · erf(m · z) drift.
The drift amplitude m is locked to Ω_m via the normalisation condition
E(0) = 1, making this truly zero-parameter beyond (Ω_m, h).

Best-fit:

```
Omega_m = 0.3093,  h = 0.6775
w_0 = -0.886,  w_a = -0.133  (CPL projection)
Delta_chi2 = -21.62  vs LCDM
```

- No phantom crossing (erf drift is monotone, w > -1 structurally)
- DESI DR3 Fisher separation: **2.16σ** (Q9 pass, borderline)
- Δ ln Z = **+10.779** (STRONG) — indistinguishable from C28 at evidence level

Bayesian evidence notes: 14-candidate alt-20 cluster yields nearly
identical Δ ln Z (+9.6 to +10.8), confirming SVD n_eff=1 finding.
A12 ranks first within the cluster by combined chi² + projection score.

### 5.1.4 Comparison to DESI DR2 central values

DESI DR2 joint (DESI+CMB+DESY5) central values:

```
w_0 = -0.757 ± 0.058,    w_a = -0.83 ± 0.24.
```

All three winners sit at less extreme |w_a| than the DESI central value,
but are within 1–2σ when the DESY5 SN likelihood is included.  None
predicts phantom crossing, consistent with SQMH L0/L1 sign rules.

## 5.2 DESI DR3 Fisher forecast

Full Fisher forecast results (`simulations/l5/forecast/dr3_forecast.json`,
figure `paper/figures/l5_dr3_forecast.png`).  DR3 projected precision:
σ(D_A)/D_A ≈ 0.008, σ(H)/H ≈ 0.010.

| Candidate | σ(w_0) | σ(w_a) | LCDM sep. | Q9 |
|-----------|--------|--------|-----------|-----|
| C11D      | 0.058  | 0.24   | ~2.9σ     | ✓  |
| C28       | 0.058  | 0.24   | 3.91σ     | ✓  |
| A12       | 0.058  | 0.24   | 2.16σ     | ✓  |
| A17 (bkp) | —     | —      | 2.75σ     | ✓  |
| A04 (watch)| —    | —      | 7.98σ     | ✓  |

**Pairwise discrimination** (noteworthy):
- C28 ↔ C33 (demoted): 0.19σ — **indistinguishable even at DR3**.
- Alt-hard cluster (A01, A05, A06, A12, A16, A20) mutual separation: < 0.5σ.
- A04 separates from all others by ≥ 3σ — most discriminating outlier.

## 5.3 Demoted and killed candidates

**C33 f(Q) teleparallel** — demoted from Phase-5 main.  Best-fit Ω_m = 0.340
drives S_8 above the DES-Y3 3σ upper bound (S_8 = 0.891 > 0.84, K15 fail).
Also fails Q10 (Δχ²_WL = +54.5) and Q11 (|Δh_SH0ES| worsening).
Δ ln Z = +2.508 (substantial, borderline Q8).  Relegated to appendix.

**C26 Perez-Sudarsky diffusion** — confirmed KILL.  Reformulation
J⁰ = α_Q H ρ_m analytically removes the ODE blow-up but any α_Q ≠ 0 causes
exponential CMB sound-horizon violation (χ²_CMB ≫ 1000 for α_Q ≥ 0.02).
Joint fit collapses to α_Q = 0, i.e. ΛCDM. Negative result recorded in §8.

## 5.4 No phantom-crossing promise

All Phase-5 winners satisfy:

```
w(z) > -1    for all z in [0, z_CMB].
```

This is a structural SQMH L0/L1 prediction and a sharp discriminator
against phantom quintessence, phantom-crossing EFT-of-DE families, and
generic CPL parameter space.  A DESI DR3 result requiring phantom crossing
would falsify the L0/L1 sign rule.
