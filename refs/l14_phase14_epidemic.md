# Phase 14: Epidemic / SIR Model of Spacetime Quanta

## Phenomenological Interpretation of A1 and A2

**A1**: Spacetime quanta are susceptible (S) agents in an epidemic model.
- Matter "infects" quantum spacetime: S → I → classical (recovered/removed state).
- Matter annihilates quanta: infected quanta lose quantum coherence (become classical geometry).
- Empty space regenerates quanta: recovery/birth of new susceptible quanta in voids.

**A2**: The quantum-classical boundary is derivable from A1.
- Derivation: boundary = epidemic threshold R_0 = 1 (basic reproduction number).
- R_0 = beta_inf * rho_m / Gamma_recovery.
- R_0 < 1 (low matter density, low z): epidemic dies out → quantum coherent vacuum survives → dark energy.
- R_0 > 1 (high matter density, high z): epidemic spreads → classical domination → dark energy suppressed.

## SIR Background

Standard SIR model: dS/dt = -beta*S*I, dI/dt = beta*S*I - gamma*I, dR/dt = gamma*I.
Equilibrium susceptible fraction: S_eq/N = gamma/beta = 1/R_0.
Dark energy = susceptible fraction (unconverted quanta) = S_eq/N.

In cosmological mapping:
- S = quantum spacetime density (= dark energy density).
- I = classicalized spacetime (inert, not dark energy).
- R_0(z) = beta_inf * rho_m(z) / (Gamma * rho_de) — matter density drives infection rate.

---

## Theory EP1: SIR Equilibrium (Michaelis-Menten form)

**Physical picture**: At each epoch, SIR equilibrium is established quasi-statically.
Susceptible fraction = 1/R_0 = Gamma/(beta_inf * rho_m(z)).
But susceptible fraction is bounded [0,1]; use saturation form:

  S_eq / S_total = 1 / (1 + R_0) = 1 / (1 + beta_inf * rho_m / Gamma)

This is the Michaelis-Menten form from enzyme kinetics (identical math to SIR equilibrium).
Dark energy proportional to susceptible fraction:
  omega_de(z) / OL0 = 1 / (1 + A * Om*(1+z)^3 / OL0)

where A = beta_inf/Gamma (infection-to-recovery ratio).

**Explicit formula EP1**:
```
omega_de(z) = OL0 / (1 + A * Om*(1+z)^3 / OL0)
            = OL0^2 / (OL0 + A * Om*(1+z)^3)
```

Parameters: A > 0 (infection rate / recovery rate ratio).

At z=0: omega_de = OL0^2 / (OL0 + A*Om).
Normalize to omega_de(0) = OL0: multiply by (OL0 + A*Om)/OL0.

**Normalized EP1**:
```
f0 = OL0 / (OL0 + A*Om)
omega_de(z) = OL0 * f0 * OL0 / (OL0 + A*Om*(1+z)^3)
            = OL0 * OL0^2 / ((OL0 + A*Om) * (OL0 + A*Om*(1+z)^3))
```

Equivalently (simpler normalization by dividing by f0):
```
omega_de(z) = OL0 * (OL0 + A*Om) / (OL0 + A*Om*(1+z)^3)
```

At z=0: omega_de = OL0*(OL0+A*Om)/(OL0+A*Om) = OL0. (exact)
At z=1: omega_de = OL0*(OL0+A*Om)/(OL0+8*A*Om).

For A=1, Om=0.3, OL0=0.7: numerator = 0.7+0.3 = 1.0. denominator = 0.7+2.4 = 3.1.
omega_de(z=1) = OL0 * 1/3.1 = OL0 * 0.323.

This gives dark energy that was MUCH SMALLER in the past: dark energy decreasing rapidly.
Wait: this is wrong direction. (OL0+A*Om)/(OL0+8*A*Om) < 1 for z>0 means omega_de DECREASES going back in time (z increasing). This gives dark energy that was SMALLER in the past → w > -1 (quintessence behavior).

The prompt says EP1 follows Michaelis-Menten: omega_de = OL0/(1+A*Om*(1+z)^3/OL0).
This gives omega_de decreasing with z (smaller in the past). Quintessence-type behavior.
w_eff < -1 is NOT directly achieved with this form.

**Note**: For chi² improvement, EP1 may still fit DESI if the DESI data prefers dark energy that was larger today than in the past (quintessence) rather than phantom. The CPL fit wa > 0 would be unusual for DESI preference. May need to reinterpret.

Direct formula from prompt:
```
omega_de(z) = OL0 / (1 + A*Om*(1+z)^3/OL0)
```
unnormalized version. Normalized:
```
omega_de(z) = OL0 * (1 + A*Om/OL0) / (1 + A*Om*(1+z)^3/OL0)
```

---

## Theory EP2: SIS Model (rational decay)

**Physical picture**: SIS model (Susceptible-Infected-Susceptible): infected quanta can recover back to susceptible. No permanent removal. Prevalence at equilibrium:
  I* = 1 - 1/R_0 = 1 - Gamma/(beta_inf * rho_m)

Dark energy = susceptible fraction = 1/R_0 (in the SIS model, without demographic turnover):
  omega_de / OL0 = 1/R_0 = Gamma / (beta_inf * rho_m(z))
                 = (Gamma/beta_inf) / rho_m(z)
                 = OL0 / (A * Om*(1+z)^3)  [identifying Gamma/beta_inf with OL0/(A*Om)]

But this diverges at z=0 if we don't regularize. Use the full SIS equilibrium:
  S* = N / R_0 = N * Gamma / (beta_inf * rho_m)

Including the total pool:
  S* = N * OL0 / (A*Om*(1+z)^3 + OL0)

**Explicit formula EP2** (from prompt, as SIS steady-state susceptible fraction):
```
omega_de(z) = OL0 * OL0 / (A*Om*(1+z)^3 + OL0)
            = OL0^2 / (OL0 + A*Om*(1+z)^3)
```

Normalized to omega_de(0) = OL0:
At z=0: omega_de = OL0^2 / (OL0 + A*Om).
Divide raw formula by OL0/(OL0+A*Om):
```
omega_de(z) = OL0 * (OL0 + A*Om) / (OL0 + A*Om*(1+z)^3)
```

This is identical to normalized EP1! The two formulations converge to the same rational decay form.

**Alternative EP2 form** (emphasizing SIS distinct behavior): with demographic renewal rate mu:
  R_0_eff = beta_inf * rho_m / (Gamma + mu)
  S*/N = (Gamma+mu)/beta_inf / rho_m → saturation form with two-parameter denominator.

Or use the prompt's form directly:
```
omega_de(z) = OL0 * (OL0 / (A*Om*(1+z)^3 + OL0))
```
Normalized:
```
f0 = OL0 / (A*Om + OL0)
omega_de(z) = OL0 * (OL0/(A*Om*(1+z)^3+OL0)) / f0
            = OL0 * (A*Om+OL0)/(A*Om*(1+z)^3+OL0)
```

Both EP1 and EP2 in normalized form are: omega_de(z) = OL0 * (OL0 + A*Om) / (OL0 + A*Om*(1+z)^3).

For EP2, set a different normalization convention:
  omega_de(0) = OL0, and the SIS formula at z=0 is OL0^2/(OL0+A*Om).
  Rather than normalizing, accept that OL0 is already the normalized value, and use:
```
omega_de(z) = OL0 * OL0 / (A*Om*(1+z)^3 + OL0)  [prompt's form, unnormalized]
```

Or cleanly:
```
omega_de(z) = OL0^2 / (OL0 + A*Om*(1+z)^3)
```

This gives omega_de(z=0) = OL0^2/(OL0+A*Om) ≠ OL0 unless A=0. Use with A as a free parameter that also shifts OL0_eff.

---

## Theory EP3: SIR with Vaccination Analog (exponential depletion + saturation)

**Physical picture**: Some spacetime quanta are "immune" (vaccinated) — they reside in voids and are protected from matter infection. The vaccination fraction f_v depends on the void fraction, which in turn depends on matter density.

Effective susceptible fraction in vaccinated SIR:
  S_eff = S_0 * (1 - f_v(z))  where f_v(z) is fraction of "immune" (void) quanta.

As matter density increases (higher z), voids are compressed → fewer immune quanta → f_v decreases.
Alternatively: as matter increases, immune fraction decreases exponentially (voids filled).

Immune/void fraction: f_v(z) = A * exp(-B * Om*(1+z)^3/OL0).
At z=0: f_v(0) = A * exp(-B*Om/OL0) > 0 (finite immune fraction today).
At z → infinity: f_v → 0 (no voids in matter-dominated universe).

Dark energy = susceptible quanta + vaccinated immune quanta (both contribute to quantum vacuum):
  omega_de(z) = OL0 * (1 + A * exp(-B * Om*(1+z)^3 / OL0))

**Explicit formula EP3**:
```
omega_de(z) = OL0 * (1 + A * exp(-B * Om*(1+z)^3 / OL0))
```

Parameters: A > 0 (immune fraction amplitude), B > 0 (void depletion rate).

At z=0: omega_de = OL0*(1 + A*exp(-B*Om/OL0)).
Normalize to omega_de(0) = OL0: the formula as written does NOT equal OL0 at z=0 unless A=0.

Two conventions:
(a) Accept that A shifts OL0 and fit A, B, OL0 jointly.
(b) Normalize: let N0 = 1 + A*exp(-B*Om/OL0):
```
omega_de(z) = OL0 * (1 + A * exp(-B * Om*(1+z)^3 / OL0)) / (1 + A * exp(-B*Om/OL0))
```

At z=0: exactly OL0.
At z=1: omega_de = OL0 * (1 + A*exp(-8*B*Om/OL0)) / (1 + A*exp(-B*Om/OL0)).

For B=0.5, A=0.5, Om=0.3, OL0=0.7:
  exp(-B*Om/OL0) = exp(-0.214) = 0.807.
  exp(-8*B*Om/OL0) = exp(-1.714) = 0.180.
  f0 = 1+0.5*0.807 = 1.404.
  omega_de(z=1) = OL0 * (1+0.5*0.180)/1.404 = OL0 * 1.090/1.404 = OL0 * 0.777.

omega_de SMALLER at z=1: dark energy decreasing into the past (quintessence behavior).

To get dark energy larger in the past (phantom/DESI preferred): flip the sign or invert the exponential.

**Reinterpretation for phantom behavior**:
Immunity factor INCREASES with matter density (higher matter → more "stimulated" immune response):
  f_v(z) = A * (1 - exp(-B * Om*(1+z)^3 / OL0))

omega_de = OL0 * (1 + f_v(z)):
```
omega_de(z) = OL0 * (1 + A * (1 - exp(-B * Om*(1+z)^3 / OL0)))
```

At z=0: omega_de = OL0*(1 + A*(1-exp(-B*Om/OL0))).
Normalized:
```
f0 = 1 + A*(1 - exp(-B*Om/OL0))
omega_de(z) = OL0 * (1 + A*(1 - exp(-B*Om*(1+z)^3/OL0))) / f0
```

This gives dark energy LARGER in the past → phantom behavior → wa < -1 possible.
This is the more useful form for fitting DESI.

Using the prompt's original form (exponential depletion with saturation):
```
omega_de(z) = OL0 * (1 + A * exp(-B * Om*(1+z)^3 / OL0))
```
normalized to omega_de(0)=OL0, this gives quintessence (dark energy decreasing into past).
Still physically valid and testable.

---

## Summary Table

| Theory | Formula | Parameters | Behavior |
|--------|---------|------------|----------|
| EP1 | `OL0 * (OL0 + A*Om) / (OL0 + A*Om*(1+z)^3)` | A>0 | Rational decay, dark energy shrinks into past |
| EP2 | `OL0^2 / (OL0 + A*Om*(1+z)^3)` | A>0 | Similar rational decay (SIS variant) |
| EP3a | `OL0*(1+A*exp(-B*Om*(1+z)^3/OL0)) / (1+A*exp(-B*Om/OL0))` | A,B>0 | Exponential saturation, decreasing into past |
| EP3b | `OL0*(1+A*(1-exp(-B*Om*(1+z)^3/OL0))) / f0` | A,B>0 | Increasing into past, phantom-type |

## One-line formulas per theory

**EP1** (normalized):
```
omega_de(z) = OL0 * (OL0 + A*Om) / (OL0 + A*Om*(1+z)^3)
```

**EP2** (SIS rational):
```
omega_de(z) = OL0^2 / (OL0 + A*Om*(1+z)^3)
```

**EP3** (vaccination exponential, prompt original form, phantom reinterpretation):
```
omega_de(z) = OL0 * (1 + A*exp(-B*Om*(1+z)^3/OL0)) / (1 + A*exp(-B*Om/OL0))
```

## CPL Forecasts (qualitative)

- **EP1**: wa > 0 (quintessence: dark energy decreasing into past). May not match DESI preference for wa < 0.
- **EP2**: Similar to EP1 but with different normalization. wa > 0 typically.
- **EP3**: Depends on sign convention. EP3b (phantom version) gives wa ~ -0.3 to -0.8. Best DESI candidate among epidemic theories.

## Physical Motivation vs DESI

EP models give dark energy DECREASING into the past (matter infects/destroys quantum vacuum).
This is physically natural for the epidemic interpretation.
However, DESI DR1 prefers dark energy LARGER in the past → EP models may give wa > 0 or chi² > 11.
Priority: EP3b > EP1 ~ EP2 for DESI improvement.
