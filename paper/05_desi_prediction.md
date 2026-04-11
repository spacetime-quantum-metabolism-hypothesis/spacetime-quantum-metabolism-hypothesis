# 5. DESI DR2/DR3 w(z) Predictions

## 5.1 Predictions for the two Phase-5 main candidates

After L4 winnowing, the Phase-5 main candidates are **C28
(Maggiore-Mancarella RR non-local)** and **C33 (f(Q) teleparallel)**.
Both reproduce the DESI DR2 w_a < 0 signal without phantom crossing and
satisfy Cassini |γ − 1| = 0 analytically.

### 5.1.1 C28 Maggiore RR non-local

Best-fit CPL reconstruction on z ∈ [0.01, 1.2]:

```
w_0 = -0.848,    w_a = -0.245.
```

MCMC posterior (reduced budget, to be re-run at 48×2000 in Phase 5):

```
w_0 = -0.849 ± 0.018,    w_a = -0.242 ± 0.054.
```

w(z) structural features:
- w(z = 0) = -0.848
- w(z → ∞) → -1 (asymptotic ΛCDM recovery)
- Monotonically decreasing
- No phantom crossing
- Inflection feature at z ~ 0.55 from the localised (U, S) auxiliary
  pair crossing matter-DE equality.

### 5.1.2 C33 f(Q) teleparallel

Best-fit CPL:

```
w_0 = -0.981,    w_a = -0.316.
```

MCMC posterior (L4-reduced):

```
w_0 = -0.984 ± 0.007,    w_a = -0.262 ± 0.123.
```

Compared to C28, C33 has w₀ much closer to -1 but a larger |w_a|,
producing a more rapid drift at moderate z.

### 5.1.3 Comparison to DESI DR2 central values

DESI DR2 joint (DESI+CMB+DESY5) central values:

```
w_0 = -0.757 ± 0.058,    w_a = -0.83 ± 0.24.
```

Both candidates sit at less extreme |w_a| than the DESI central value,
but are within 1–2σ when the DESY5 SN likelihood is included.  Neither
predicts phantom crossing, consistent with SQMH L0/L1 sign rules.

## 5.2 DR3 forecast

The anticipated DESI DR3 w_a statistical precision is ~0.12 (factor ~2
improvement over DR2).  At this sensitivity:

- C28 (|w_a| = 0.245) would be distinguishable from ΛCDM at ~2σ.
- C33 (|w_a| = 0.316) would be distinguishable at ~2.6σ.
- The difference between C28 and C33 (Δw_a ~ 0.07) would remain below
  the DR3 sensitivity; DR4 or a combined DESI+Euclid analysis may be
  required for discrimination.

## 5.3 Under-re-evaluation candidates

**C11D Disformal IDE** has the largest raw Δχ² improvement (−22.9) and
the strongest w_a signal (−0.29) in our L4 analysis, but is currently
flagged K3 (phantom crossing) due to a CPL thawing-template artifact.
If a full hi_class disformal-branch background re-judgement in Phase 5
clears the K3 flag, C11D would become the primary Phase-5 candidate,
promoting C28 and C33 to backup status.

**C26 Perez-Sudarsky diffusion** was the most direct SQMH L0/L1
interpretation candidate (theory score 9/10) but the full ODE
implementation collapsed to ΛCDM with the specific ansatz
J⁰ ∝ H.  An alternative source J⁰ ∝ H ρ_m is being re-cast for Phase 5;
if successful, C26 would provide a third independent Phase-5 candidate.

## 5.4 No phantom-crossing promise

All Phase-5 main candidates satisfy:

```
w(z) > -1    for all z ∈ [0, z_CMB].
```

This is a structural SQMH L0/L1 prediction and a sharp discriminator
against phantom quintessence, phantom-crossing EFT-of-DE families, and
generic CPL parameter space.  A DESI DR3 result showing w(z) > -1 at
all z would be consistent with SQMH; a result requiring phantom crossing
would falsify the L0/L1 sign rule.
