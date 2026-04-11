# 7. Comparison to ΛCDM

## 7.1 Joint Δχ² table

The ΛCDM baseline on the full BAO+SN+CMB+RSD joint likelihood is

```
χ²_total = 1676.89    at (Ω_m, h) = (0.320, 0.669).
```

L4 full-Boltzmann fits:

| ID | Family | χ² | Δχ² | Verdict |
|---|---|---|---|---|
| C11D | Disformal IDE | 1653.97 | **−22.92** | Under re-eval (K3 artifact) |
| **C28** | **Maggiore RR** | **1655.81** | **−21.08** | **Phase-5 MAIN** |
| C41 | Wetterich fluid IDE | 1662.66 | −14.24 | KILL (Cassini) |
| C10k | Dark-only coupled | 1667.54 | −9.36 | KILL (K2 + growth) |
| C23 | Asymptotic Safety RVM | 1668.19 | −8.71 | KILL (wrong ν sign) |
| C5r | RVM ν<0 | 1668.19 | −8.71 | KILL (wrong ν sign) |
| C6s | Stringy RVM+CS | 1668.19 | −8.71 | KILL (wrong ν sign) |
| **C33** | **f(Q) teleparallel** | **1670.61** | **−6.28** | **Phase-5 MAIN** |
| C26 | Perez-Sudarsky | 1676.89 | ~0 | KILL (full-ODE ↔ toy mismatch) |
| C27 | Deser-Woodard | 1677.26 | +0.37 | KILL (posterior collapse) |

Δχ² = −6 corresponds to ~2.5σ preference over ΛCDM.  C28 and C33 cross
this threshold and enter Phase 5.  C11D would also cross comfortably
if K3 is cleared in the disformal re-judgement.

## 7.2 2-D (w_0, w_a) posterior contours

Corner plots are available in `paper/figures/l4_C28_corner.png` and
`paper/figures/l4_C33_corner.png`.  The LCDM point (w_0, w_a) = (−1, 0)
lies:
- **C28**: outside the 3σ contour, dominated by the w_0 direction.
- **C33**: at ~2σ from the posterior mean, dominated by the w_a
  direction.

The DESI DR2 central (w_0, w_a) = (−0.757, −0.83) lies at ~2σ from
both C28 and C33 posterior means; neither candidate reproduces the
DESI central w_a amplitude at 1σ, but both are compatible at 2σ.

## 7.3 Bayesian evidence sketch

A full Bayesian evidence calculation (thermodynamic integration or
nested sampling) is deferred to Phase 5.  As a rough Akaike criterion,
ΔAIC = Δχ² + 2 × (N_extra) where N_extra is the number of extra
parameters over ΛCDM:

| ID | Δχ² | N_extra | ΔAIC |
|---|---|---|---|
| C28 | −21.08 | 3 (Ω_m, h, γ_0) – 2 = 1 | **−19.08** |
| C33 | −6.28 | 4 – 2 = 2 | **−2.28** |
| C11D | −22.92 | 3 – 2 = 1 | **−20.92** |

Both C28 and C11D are preferred over ΛCDM by ΔAIC ≳ 19; C33 is
preferred by ~2.3.  Full model comparison at the Bayesian-evidence
level will be Phase 5.

## 7.4 Hubble tension

None of the candidates resolves the H₀ tension:

| ID | h | Distance-ladder Δh |
|---|---|---|
| LCDM | 0.669 | −0.063 |
| C28 | 0.677 | −0.055 |
| C33 | 0.647 | −0.085 |
| C11D | 0.677 | −0.055 |
| SH0ES | 0.732 | 0 |

C28 and C11D give a small reduction of the tension (~13% of the gap),
C33 makes it worse.  This is a structural limitation of all DESI
compatible w_a < 0 models and is discussed honestly in §8.

## 7.5 S_8 / σ_8

C28, C33 do not significantly modify linear growth (μ_eff = 1 at
sub-horizon scales within the L4 approximation).  Their predicted
σ_8(z = 0) is within 0.5% of ΛCDM.

C10k, had it survived, would have worsened σ_8 by +0.96%.  This is one
reason C10k is a confirmed KILL beyond just the background K2 failure.

## 7.6 fσ_8(z) prediction

Predicted fσ_8(z) at the 8 RSD redshifts (C28 and C33 both match ΛCDM
growth to within 0.5% at all z; C41 would have given a ~1% enhancement
from the coupling drag term but is eliminated):

```
z = 0.02, 0.15, 0.38, 0.51, 0.70, 0.85, 1.48, 1.52
LCDM: 0.447, 0.462, 0.478, 0.476, 0.470, 0.463, 0.448, 0.376
C28 : same to 0.5%
C33 : same to 0.5%
```

RSD data provides weak discrimination among the surviving candidates;
Phase 5 should consider including KiDS-1000 / DES-Y3 cosmic-shear to
tighten the growth constraint.
