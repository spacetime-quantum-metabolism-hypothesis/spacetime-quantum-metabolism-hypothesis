# refs/l10_nonlinear_derivation.md -- L10-N: Nonlinear Halo Structure SQMH

> Date: 2026-04-11
> Phase: L10-N (Rounds 1-10)
> Kill: K52 (correction < 1e-60)
> Keep: Q52 (correction > 1e-50, structural departure)

---

## Background

L9-A: G_eff/G - 1 = 4e-62 at linear perturbation level.
L10-N: At nonlinear level (halo formation), does SQMH produce new structure?

---

## 8-Person Parallel Team Discussion

### [해석 접근] Member 1: Halo Overdensity Analysis

Inside a virialized halo: rho_m(halo) = delta_c * rho_m(background)
delta_c = 200 (standard virial overdensity).

SQMH equilibrium density: n_eq = Gamma_0 / (sigma * rho_m)
Inside halo: n_eq(halo) = Gamma_0 / (sigma * 200 * rho_m(bg)) = n_eq(bg) / 200.

Counterintuitively, n_eq is LOWER inside halos (more efficient annihilation).
The effective Pi_SQMH inside a halo:
Pi_SQMH(halo) = sigma * n_eq(halo) * rho_m(halo) = sigma * (n_eq/200) * (200*rho_m) = Pi_SQMH(bg)

Wait: Pi_SQMH = sigma*n*rho_m evaluated at equilibrium n = n_eq.
At equilibrium (quasi-static): sigma*n_eq*rho_m = Gamma_0 everywhere (same Gamma_0).
So the equilibrium product sigma*n_eq*rho_m = Gamma_0 = CONSTANT.

G_eff/G - 1 = 4 * Pi_SQMH_background (not halo-specific).

**Analytical conclusion**: At equilibrium, SQMH correction is background-level everywhere.

---

### [수치 접근] Member 2: Numerical Nonlinear Calculation

From sqmh_halo.py:
- G_eff/G - 1 (delta_c=200): 2.97e-59 (log10 = -58.5)
- Background G_eff/G - 1: 1.48e-61
- Ratio: 200 = delta_c

BUT: Member 1 shows equilibrium n_eq(halo) = n_eq(bg)/delta_c.
The product sigma*n*rho_m at equilibrium = sigma*(n_eq/delta_c)*(delta_c*rho_m) = sigma*n_eq*rho_m (unchanged).

The code computed Pi_SQMH(halo) = Om_m_eff(halo)*H0*t_P where Om_m_eff = delta_c*Om_m.
This overestimates the halo correction: it assumes n stays at background n_eq
while rho_m is enhanced. This is incorrect for equilibrium.

**Correction**: If n_eq self-adjusts to halo density, G_eff/G - 1 is SAME in halo and background.
If n does NOT equilibrate (dynamical case): the halo passes through with n = n_eq(bg),
while rho_m(halo) = 200*rho_m(bg).
Then: sigma*n*rho_m(halo) = 200 * sigma*n*rho_m(bg) = 200 * Pi_SQMH.
G_eff/G - 1 (dynamical, in-falling matter): 200 * 4e-62 = 8e-60.

**Numerical conclusion**: Dynamical correction: 8e-60 (NOT at equilibrium).
K52 threshold: 1e-60. At delta_c=200: 8e-60 > 1e-60 -> K52 NOT TRIGGERED.
But Q52: 8e-60 < 1e-50 -> Q52 FAIL.

---

### [대수 접근] Member 3: Press-Schechter Correction

P-S mass function correction from sigma_8:
Delta_sigma_8 = epsilon_SQMH * sigma_8 = 4e-62 * 0.811 = 3.2e-62

Relative correction in dn/dM: proportional to (delta_c/sigma_R)^2 * epsilon
For a cluster-mass halo (sigma_R ~ 0.3):
Relative correction ~ (1.686/0.3)^2 * 4e-62 = 31.6 * 4e-62 = 1.3e-60.

This is at the threshold of K52 (1e-60). Technically:
- For M < M_* (galaxy scales, sigma_R ~ 1): correction ~ 4e-62 << 1e-60
- For M >> M_* (cluster scales, sigma_R ~ 0.3): correction ~ 1.3e-60 ~ 1e-60

**Algebraic conclusion**: P-S correction is ~ 1e-60 at cluster mass scales.
K52 status: MARGINAL (at the threshold).

---

### [위상 접근] Member 4: Topological Structure of SQMH in Nonlinear Regime

In the nonlinear regime (delta >> 1), density field develops filaments and walls
(cosmic web). SQMH adds a velocity contribution v_r ~ sigma*n*r (from spherical infall).

This is a monopole vector field (radially inward). In topological language:
winding number of v_r around any point = 0 (no vortices).
SQMH generates ZERO winding number structures -- no topological defects from SQMH.

The Zeldovich pancake formation: in the linear regime, overdense regions collapse.
SQMH correction to collapse time t_coll:
t_coll(SQMH) = t_coll(LCDM) * (1 - epsilon_SQMH/2) ~ t_coll(LCDM) (identical to 62 orders).

**Topological conclusion**: No new topological structure from SQMH in nonlinear regime.
Cosmic web topology identical to LCDM to 62 orders.

---

### [열역학 접근] Member 5: Halo Virialization and SQMH Equilibrium

Virialization: kinetic energy = -1/2 * potential energy (virial theorem).
For SQMH: modified gravitational potential.

The SQMH correction to the halo potential energy:
U_SQMH = -(G_eff/G) * G * M^2 / R = -G*M^2/R * (1 + 4e-62)

Modified virial condition: K = -1/2 * U_SQMH
K_SQMH = K_LCDM * (1 + 4e-62)

Velocity dispersion: sigma_v^2 = K/M = sigma_v_LCDM^2 * (1 + 4e-62)
This is undetectable (current precision: 1-3%).

SQMH also adds a dissipative term: the interaction sigma*n*rho_m acts as friction.
This could modify the relaxation timescale:
tau_relax(SQMH) = tau_relax(LCDM) / (1 + sigma*n*rho_m/H) ~ tau_relax(LCDM)
(since sigma*n*rho_m/H = Pi_SQMH << 1)

**Thermodynamic conclusion**: SQMH halo virialization: identical to LCDM to 62 orders.

---

### [정보기하학 접근] Member 6: Halo Mass Function Information Content

Fisher information in the mass function dn/dM:
I(sigma_8) = integral [(d ln dn/dM / d sigma_8)^2 * dn/dM * V] dM dz

SQMH epsilon correction:
I(sigma_8)_SQMH = I(sigma_8)_LCDM * (1 + 2*epsilon_SQMH)

Detectability: Fisher SNR for sigma_8 change:
SNR_SQMH = sqrt(delta I) * Delta_sigma_8 / sigma(sigma_8)

Current sigma_8 constraint: sigma(sigma_8) ~ 0.015.
SQMH contribution: Delta_sigma_8 = 3.2e-62.

SNR_SQMH = sqrt(2*4e-62 * I_LCDM) * 3.2e-62 / 0.015
~ 0 (completely undetectable)

**Information-geometric conclusion**: SQMH carries zero detectable information
in the nonlinear mass function. K52 effectively triggered.

---

### [대칭군 접근] Member 7: Spherical Collapse Symmetry

Standard Press-Schechter: spherical symmetry (SO(3) invariant).
SQMH correction to spherical collapse:
delta_dot_dot + 2H*delta_dot = 4*pi*G_eff*rho_m*delta (growth equation)

With G_eff = G*(1 + 4e-62): delta_c_eff = delta_c_LCDM * (1 + epsilon)?

Exact: In spherical collapse, the collapse threshold:
delta_c(G_eff) = delta_c_LCDM * (G/G_eff)^0.3 ~ delta_c_LCDM * (1 - 0.3*4e-62)

Change in delta_c: Delta delta_c = -0.3 * 4e-62 * 1.686 = -2e-62.

This is undetectable. Halo number density:
dn/d ln M ~ exp(-delta_c^2/(2*sigma_R^2))
Relative change: d ln (dn/d ln M) / d epsilon = delta_c^2/sigma_R^2 * 0.3
~ (1.686/0.5)^2 * 0.3 ~ 3.4

=> Relative change in halo number: 3.4 * 4e-62 = 1.4e-61. Still < 1e-60.

**Symmetry conclusion**: SO(3)-invariant correction to halo number: 1.4e-61 ~ threshold.

---

### [현상론 접근] Member 8: 21cm Signal and SKAO

SQMH correction to 21cm brightness temperature:
T_21(SQMH)/T_21(LCDM) = (D(z)_SQMH/D(z)_LCDM)^2 ~ (1 + 2*4e-62/2)^2 ~ 1 + 4e-62

SKAO sensitivity: 1 mK per beam. Current T_21 ~ 10 mK.
Relative sensitivity: 1e-3/10 = 1e-4.
SQMH correction: 4e-62.
SNR: 4e-62 / 1e-4 = 4e-58.

After foreground cleaning (factor 10^4 improvement in some models):
SNR ~ 4e-54. Still 54 orders below unity.

**Phenomenological conclusion**: SQMH nonlinear signal in 21cm: undetectable.
K52 effectively triggered for all observational channels.

---

## Team Synthesis (Rounds 1-10)

**Round 1 consensus**:
- Equilibrium case: K52 TRIGGERED (n_eq adjusts, G_eff/G-1 same as background).
- Dynamical case: K52 NOT TRIGGERED for delta_c=200 (8e-60 > 1e-60).
- But Q52 FAIL (8e-60 < 1e-50).

**Rounds 2-5 (deepening)**:

Round 2: Explored extreme halos (galaxy cores): rho_m ~ 10^-20 kg/m^3 at galactic center.
rho_m(center)/rho_m(bg) ~ 10^7. Pi_SQMH(center) ~ 10^7 * 4e-62 = 4e-55.
Still < 1e-50.

Round 3: Black hole core: rho ~ 10^30 kg/m^3.
Pi_SQMH(BH) ~ 10^57 * 4e-62 = 4e-5 ~ 0.004%. Finally non-negligible!
But black hole interiors are not cosmological structure. K52 triggered for cosmology.

Round 4: The halo result (delta_c=200): 8e-60 is technically > 1e-60.
K52 criterion: "SQMH correction < 1e-60". 
Actual: 8e-60 (if dynamical, n not equilibrated). K52 NOT technically triggered.
But this is a cosmetically unhelpful result: 8e-60 is still 59 orders below unity.

Round 5: Honest verdict: K52 is at the borderline for delta_c=200.
The correction at delta_c=200 is 8e-60 (slightly above K52 threshold of 1e-60).
But remains 50 orders below Q52 threshold of 1e-50.
NF structure: no genuinely new physical result.

**Rounds 6-10 (focus)**:

Round 6: Explored non-equilibrium SQMH in halos.
During halo collapse, the SQMH density n "lags" behind equilibrium.
Relaxation time: tau_SQMH = 1/(sigma*rho_m + 3H) ~ H^{-1}/Pi_SQMH ~ 10^62 Hubble times.
=> n NEVER reaches halo equilibrium. Always at background n_eq.
=> Dynamical correction IS the correct one: 200 * Pi_SQMH ~ 8e-60.

Round 7: Compared to bullet cluster constraints.
Bullet cluster: G_eff/G within ~10% (gravitational lensing vs X-ray mass).
SQMH: G_eff/G - 1 = 8e-60 << 10%. No constraint possible.

Round 8: Found that K52 is "NOT TRIGGERED" technically (8e-60 > 1e-60) but useless.
New finding candidate: in halos with delta_c >> 1, G_eff/G correction is ENHANCED by delta_c.
This is a new structure even if not observable. Register as NF-23 candidate (STRUCTURAL).

Round 9: NF-23 verdict: The enhancement G_eff/G-1 ~ delta_c * Pi_SQMH is a genuine structural
result but:
1. Still < 1 for any realistic delta_c (delta_c < 10^62 required for O(1) correction).
2. Not observable.
3. For BH cores: non-negligible (delta_c ~ 10^57, G_eff/G-1 ~ 0.4%), but inside BH.
NF-23 flagged as STRUCTURAL with very low observability.

Round 10: K52/Q52 final verdict confirmed.

---

## K52 / Q52 Final Verdict

| Verdict | Status | Value | Basis |
|---------|--------|-------|-------|
| K52 (correction < 1e-60) | NOT TRIGGERED | 8e-60 (delta_c=200, dynamical) | Dynamical case: n at background level, rho_m enhanced |
| K52 (equilibrium case) | TRIGGERED | = background (4e-62) | Equilibrium n_eq adjusts, product unchanged |
| Q52 (correction > 1e-50) | FAIL | 8e-60 < 1e-50 | |

**Nuance**: K52 is technically NOT TRIGGERED (8e-60 > 1e-60) in the dynamical case.
But this is cosmetically meaningless: 8e-60 is still 59 orders below observable levels.
The "improvement" from linear to nonlinear is a factor of 200 (delta_c), not a qualitative change.

**NF-23 (new finding, STRUCTURAL, Round 9)**:
"SQMH G_eff/G correction is enhanced inside virialized halos by the overdensity factor delta_c.
At delta_c = 200 (cluster virial): correction = 8e-60 (59 orders below unity).
At extreme overdensities delta_c ~ 10^50, correction would be O(0.01%) -- marginally non-negligible.
For black hole cores (delta_c ~ 10^57): G_eff/G - 1 ~ 0.004%. Not cosmological structure."

**Paper language** (L10):
  "In virialized halos (delta_c = 200), the SQMH G_eff correction is enhanced by delta_c:
   G_eff/G - 1 ~ 8e-60 (dynamical case), compared to the linear 4e-62.
   This enhancement requires delta_c > 10^50 to produce observationally significant effects,
   exceeding any realistic astrophysical overdensity by many orders of magnitude.
   The nonlinear channel does not rescue SQMH observability."

---

*L10-N completed: 2026-04-11. All 10 rounds.*
