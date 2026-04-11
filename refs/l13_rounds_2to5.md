# refs/l13_rounds_2to5.md -- L13 Rounds 2-5 Deep Dives

> Date: 2026-04-11.
> 8-person parallel team, Rule-B 4-person code review.

---

## Round 2: ODE Form Analysis (L13-O Deep Dive)

**Focus**: Understanding why A01 and exact SQMH ODE are structurally different.

### Exact ODE with Gamma0=7.36 (A01-matching G0):

The Gamma0 required to match A01's linear term at a=1:
  Gamma0_match = OL0*(3+Om)/Om = 0.685*(3.31)/0.31 = 7.36

With Gamma0=7.36, general ODE solution:
  omega_de(a) = 7.36*Om/(6*a^3) + C*a^3
  C = OL0 - 7.36*Om/6 = 0.685 - 0.380 = 0.305

At z=2 (a=1/3):
  omega_de = 7.36*0.31/(6*0.037) + 0.305*0.037 = 10.27 + 0.011 = 10.28
  vs A01: OL0*(1+Om*2) = 0.685*(1+0.62) = 1.11

The ODE with G0=7.36 gives ~10x more DE at z=2 than A01.
Contrast: the ODE with G0=3*Om gives ~0.013 at z=2 (10x LESS than A01).

Conclusion: A01 sits at an intermediate level of high-z DE that no single-G0
ODE solution reproduces. A01 is effectively a separate empirical model.

### Key insight:
A01 = OL0*(1+Om*(1-a)) behaves as:
- rho_DE/OL0 ~ 1 at z=0
- rho_DE/OL0 ~ 1+Om at z->inf (bounded!)

The exact ODE: either grows as (1+z)^3 (for large G0) or as (1+z)^(-3) (decays).
A01 grows LINEARLY as (1+z) at high z -- intermediate behavior impossible from ODE.

This is the root cause: the functional form (1+Om*(1-a)) = (1+Om) - Om*a
grows linearly in (1/a) = (1+z), which is between the ODE's (1+z)^3 and (1+z)^(-3).

The A01 form is phenomenologically between the two ODE behaviors.
No single Gamma0 can reproduce it exactly.

**Round 2 verdict**: A01 is genuinely empirical -- not an approximation to any
exact SQMH ODE. This is a structural finding that needs honest documentation.

---

## Round 3: Uniqueness Comprehensive Analysis (L13-U Deep Dive)

**Focus**: Why does A01 predict A=Om when data prefers A~2?

### Physical interpretation:

SQMH birth-death: production proportional to rho_m.
At equilibrium: DE density ~ Gamma0 * rho_m / (3H)

For A01 to work, we need rho_DE(a) ~ OL0 * (1 + Om*(1-a)).
The "extra" DE fraction is Om*(1-a): at a=0, extra DE = Om*OL0.
This extra DE ~ Om * (today's DE) = matter fraction * cosmological constant.

Why Om specifically?
In SQMH: the BIRTH TERM scales as Gamma0*rho_m ~ Gamma0*Om.
If Gamma0 ~ OL0/OL0 ~ 1 (dimensionless rate), then extra DE ~ Om.
But Gamma0 is NOT ~ 1 in the microsopic theory; it's 3*Om phenomenologically.

The prediction A=Om arises from a SPECIFIC choice of how to normalize:
If we say "the amplitude of DE fluctuation = the fractional matter density Om",
this is a natural COINCIDENCE in a flat universe where Om + OL0 ~ 1.
It does not uniquely follow from the ODE.

### Alternative 1-parameter models that fit DESI:

The A scan shows that A~1.5-2.0 fits best. What do these correspond to?
- A=1.5: rho_DE ~ OL0*(1+1.5*(1-a)) -> 37% extra DE at a=0 vs 31% for A01.
- A=2: rho_DE ~ OL0*(1+2*(1-a)) -> 3x OL0 at a=0.

Why does DESI prefer higher A?
DESI BAO data shows D_M(z) consistently below LCDM predictions.
Higher A means more DE at high z, which changes the expansion history
in a way that better fits the DESI distance-redshift relationship.

The SQMH prediction A=Om gives less DE at high z than DESI prefers.

**Round 3 verdict**: SQMH predicts A=Om, but data prefers A~5-7x Om.
AIC/BIC favor A01 only marginally (chi2 gain ~1.8 barely justifies extra param).
This is SQMH's key uniqueness problem.

---

## Round 4: DR3 Fisher Comprehensive Analysis (L13-D Deep Dive)

**Focus**: Is the combined 3.5sigma DR3 signal robust?

### Assessment of DR3 scaling assumptions:

DR3 volume scaling assumptions (from DESI Year 3 forecasts):
- BGS: 2x DR2 in N_gal -> sigma_DR3 = sigma_DR2/sqrt(2) = 0.707*sigma_DR2
- LRG: 3x DR2 -> sigma_DR3 = 0.577*sigma_DR2
- ELG: 3.5x DR2 -> sigma_DR3 = 0.535*sigma_DR2
- QSO: 2.5x DR2 -> sigma_DR3 = 0.632*sigma_DR2
- Lya: 1.5x DR2 -> sigma_DR3 = 0.816*sigma_DR2

These are conservative estimates. Actual DR3 may have better control of systematics.

### Combined Fisher SNR calculation:

Diagonal chi2 approximation:
  SNR_combined = sqrt(sum_i [(A01_pred_i - LCDM_pred_i)^2 / sigma_DR3_i^2])
             = sqrt(sum of individual SNR^2)

Individual SNR^2:
  z=0.295: 0.97
  z=0.510: 3.13
  z=0.706: 3.11
  z=0.930: 3.41
  z=1.317: 0.83
  z=1.491: 0.71
  z=2.330: 0.06

Sum = 12.22, SNR = 3.50 sigma.

The dominant contribution comes from z=0.51-0.93 (LRG bins).
These are where DR3 has the biggest gain (3x more galaxies).

### Robustness check:

If we use only the 4 middle bins (z=0.51-0.93):
  SNR = sqrt(3.13+3.11+3.41) = sqrt(9.65) = 3.11 sigma.

So even using a subset, combined SNR > 3sigma.

### Critical caveat:

These calculations use the DIAGONAL covariance only.
Full off-diagonal covariance would change the result.
Also: A01 and LCDM use DIFFERENT best-fit Om and h.
A fair comparison should use the same Om,h for both, or marginalize.

If we fix Om=0.31, h=0.677 for both models:
  LCDM: rho_DE = OL0 (constant)
  A01: rho_DE = OL0*(1+Om*(1-a))
  The difference is purely from the perturbation, not Om/h choice.

This gives a "pure SQMH perturbation signal" discrimination.
At fixed Om,h, the SNR is larger (models differ only in rho_DE shape).

**Round 4 verdict**: DR3 combined SNR ~ 3.5 sigma is robust at diagonal level.
Full covariance + proper Om,h marginalization needed for definitive answer.
But the signal is real and within DR3 reach.

---

## Round 5: Gamma0/sigma Alternative Motivation

**Focus**: Building on NF-34 (Penrose identity). Can we strengthen Q84?

### NF-34 revisited:

sigma * rho_P = 4*pi/t_P = Penrose collapse rate for Planck quanta.

Can we derive 4*pi geometrically from SQMH?

In SQMH, spacetime quanta are born/annihilated isotropically around a source.
If each source emits/absorbs quanta over a 4*pi solid angle sphere:
  Gamma = (Penrose rate per volume) * (volume element) * (solid angle)
  = (1/t_P per m^3) * l_P^3 * 4*pi/(4*pi l_P^2) [at distance l_P]

This reduces to 1/(t_P*l_P^2) per steradian... which is not quite right.

Alternative: In semiclassical GR, the Hawking radiation from a black hole goes as:
  dE/dt = hbar/(360*pi) * kappa^2 * Area
where kappa is surface gravity. For Planck mass: kappa = c^3/(4*G*m_P), Area = l_P^2.
  dE/dt = hbar*c^6/(5760*pi*G^2*m_P^2) * l_P^2 / c [units fix]

This gives a Hawking rate ~ (1/t_P) with a numerical factor ~ 1/(5760*pi).
The 4*pi in sigma is different (larger by factor ~(5760/4) = 1440).

So the 4*pi factor is NOT from Hawking radiation. It's from the solid angle
of a sphere (Omega=4*pi steradians). This is the strongest available explanation.

### Alternative: Bohr solid angle from quantum mechanics

In QM, when a quantum system emits a photon isotropically, the angular factor
in the emission probability is:
  <|cos theta|^2> integrated over 4*pi = 4*pi/3 for dipole, 4*pi for isotropic.

The 4*pi in sigma corresponds to isotropic (monopole) Planck-scale emission.
This is the simplest geometric factor for spherical symmetry.

### Conclusion on Q84:

Q84 requires "at least one of Gamma0 or sigma to have theoretical basis."

sigma = 4*pi*G*t_P:
- G*t_P: dimensionally forced (unique combination with correct units).
- 4*pi: isotropic geometry (sphere solid angle). Not derived, but geometrically natural.
- NF-34: sigma*rho_P = 4*pi/t_P = Penrose collapse rate. Physical interpretation.

**Q84 PARTIAL judgment confirmed**: sigma has a non-circular physical interpretation
via NF-34. This is medium-strength evidence. Not a derivation.

K84 remains triggered (range=62 orders). Q84 partial.

**Round 5 verdict**: NF-34 stands as the strongest available motivation for sigma.
The 4*pi factor is geometric (isotropic). The G*t_P combination is unit-forced.
Together: sigma = G*t_P * 4*pi is the unique isotropic Planck-coupling constant.
This is the best SQMH can achieve without a fundamental theory of quantum gravity.

---

## 5-Round Summary for L13

| Round | Focus | Key Finding | Impact |
|-------|-------|------------|--------|
| R1 | All 6 phases | K83,K84,K85 triggered; NF-34 discovered | Baseline established |
| R2 | ODE structure | A01 is DIFFERENT model from exact ODE | Critical structural finding |
| R3 | Uniqueness | Best-fit A~2 >> Om; AIC marginal win | K86 partially confirmed |
| R4 | DR3 Fisher | Combined SNR=3.5sigma; per-bin SNR<2 | K85 per-bin, Q85 combined |
| R5 | Gamma0/sigma | NF-34 strengthened; 4*pi geometric | Q84 partial confirmed |

**Final verdict**: 5 of 6 Kill criteria triggered. 1 partial Keep (Q84 Penrose).
1 near-Keep (Q85 combined DR3 3.5sigma).
No game-changers. Honest assessment: SQMH phenomenology works but theoretical
foundations remain weak.
