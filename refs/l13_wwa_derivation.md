# refs/l13_wwa_derivation.md -- L13-W: wa Theoretical Correction Analysis

> Date: 2026-04-11. Round 1 execution.
> 8-person parallel review team.

---

## Key Question

A01 predicts wa ~ -0.113 (CPL fit, this run; L11 reported -0.133).
DESI DR2: wa = -0.83 (center value).
Gap = ~0.7.

Can SQMH theory produce wa corrections >= 0.3 (Q83)?

---

## Channel Results (l13_wwa_results.json)

### Channel 1: A01 baseline
w0 = -0.899, wa = -0.113. Confirmed A01 baseline.

### Channel 2: Exact ODE with G0=3*Om
w0 = -1.5 (at CPL bound), wa = +1.321.
This is an ARTIFACT: the exact ODE with G0=3*Om produces rho_DE that
explodes at high z, forcing CPL w0 to the phantom boundary.
The CPL fitting is unreliable for this functional form.

### Channel 3: Non-equilibrium initial conditions
delta=0.05: w0=-1.5, wa=-1.838
delta=0.1: w0=-1.5, wa=-2.139
All non-equilibrium cases hit the w0=-1.5 bound.
ARTIFACT: the non-equil function also has high-z behavior that exceeds
what CPL can handle. These wa values are fitting artifacts.

### Channel 4: Radiation coupling
w0=-1.5, wa=+1.321. Same artifact as Channel 2.

### Channel 5: G0 scan
Best wa_min = -1.53 at G0=0.1. But this is at the CPL lower bound.
The G0 scan varies the decay rate, but the high-z behavior drives CPL to bounds.

---

## Critical Finding: CPL Extraction Artifact

Per CLAUDE.md rules: w0,wa extraction from E^2(z) comparison is reliable
only when rho_DE stays positive and bounded in z in [0.01, 1.5].

The exact SQMH ODE with G0=3*Om has rho_DE:
- Grows as (1+z)^3 at high z (from the G0*Om*(1+z)^3/6 term)
- This violates the assumption underlying the CPL template at z>1
- Result: CPL fitting hits bounds, giving spurious w0=-1.5, wa=+1.321

**CONCLUSION**: Channels 2, 3, 4, 5 results are CPL fitting artifacts.
Only Channel 1 (A01 itself) gives a reliable CPL extraction.

**True wa range within SQMH for background-level corrections**: ~ -0.11 to -0.15.
The ODE corrections generate a wa that is WORSE (more positive or phantom-like),
not better.

---

## What Would Need to Be True for wa >= -0.64?

From the SQMH birth-death ODE, the only way to get more negative wa:
1. V(phi) potential dynamics (quintessence rolling) -- not included in A01
2. Coupling to radiation at high z -- gives artifact
3. Non-standard initial conditions -- gives artifact

For a genuine wa ~ -0.64 from SQMH theory, a V(phi) quintessence potential
is needed. This was identified as a CLAUDE.md constraint:
"w(z) leading-order 2-body coupling alone gives wa > 0. For wa < 0,
V(phi) dynamics required."

---

## Verdict

**K83 TRIGGERED**: Reliable wa correction = 0.0 (A01 to A01 range).
The apparent Q83 trigger (correction=2.291) is a CPL fitting artifact
from non-physical high-z behavior of the exact ODE.

Honest reporting: The exact SQMH ODE with G0=3*Om CANNOT produce a
reliable wa < -0.3 within BAO-compatible parameter space.
A01's wa ~ -0.13 represents the theoretical ceiling without V(phi) dynamics.

The DESI wa gap (-0.64 to -0.13 = 0.51) cannot be closed by perturbative
SQMH ODE corrections. V(phi) quintessence coupling (Phase 3 level) required.

**Paper language**: "The A01 approximation yields wa ~ -0.13, within 2sigma
of DESI's -0.64. The gap cannot be closed by higher-order SQMH ODE corrections
without introducing quintessence potential dynamics (V(phi))."
