# refs/l8_round2_verdict.md -- L8 Round 2: EFT / Large-Scale Structure Level

> Date: 2026-04-11
> Round 2 of 5 additional rounds (Rounds 2-6).
> Method: 8-person parallel team, simultaneous independent attack angles,
>   immediate cross-sharing, deliberation, final consensus.
> Focus: EFT / large-scale structure -- does SQMH appear as an EFT of any
>   candidate at the perturbation level (growth equation, f*sigma8)?
> Prior established: Q31/Q32/Q33 FAIL at background level (Round 1).

---

## Attack Angle: EFT / Large-Scale Structure

Round 1 attacked the background ODE level and found that
sigma*rho_m/(3H0) ~ 10^-62 makes SQMH indistinguishable from LCDM at
background level. Round 2 descends to perturbation theory: if SQMH
generates a distinctive growth equation (delta'' + Hdelta' = 4piG rho_m delta),
can the three candidates replicate that modified growth?

Key question: does any candidate at perturbation level contain a sector
isomorphic to the SQMH growth equation structure?

---

## 8-Person Parallel Discussion

### [Member 1 -- EFT framing]

SQMH perturbation equation derivation:
Perturb dn_bar/dt + 3H n_bar = Gamma_0 - sigma n_bar rho_m
around n_bar -> n_bar + delta_n, rho_m -> rho_m(1 + delta):

d(delta_n)/dt + 3H delta_n = -sigma delta_n rho_m - sigma n_bar rho_m delta

At background, -sigma n_bar rho_m = dn_bar/dt + 3H n_bar - Gamma_0.
Since sigma*rho_m ~ 10^-62 H, the perturbation coupling -sigma*rho_m ~ 10^-62 H.

EFT observation: at sub-Hubble scales (k >> aH), SQMH perturbation
equation reduces to standard CDM-like growth PLUS a suppression term
of order 10^-62 per Hubble time. This is unobservable.

EFT verdict: SQMH EFT at perturbation level = standard GR growth to any
observable precision. This is NOT a new failure -- it is a structural
confirmation of the 62-order scale separation.

### [Member 2 -- Growth equation: A12]

A12 is a zero-parameter erf proxy: E^2(z) = Om*(1+z)^3 + (1-Om)*F_erf(z).
The growth equation for A12:
delta'' + (2 + E'/E) delta' = (3/2) Om(1+z)^3/E^2 * delta

where ' = d/d ln(1+z). A12 has no modified gravity sector (mu_eff = 1,
sigma_eff = 1 from L5/L6 analysis). The growth equation is identical to
LCDM with substituted H(z).

Can SQMH be an EFT of A12 at perturbation level?
The SQMH perturbation adds -sigma*rho_m*delta_n to growth. Since A12
provides the background H(z) but no modified growth, SQMH perturbation
correction to A12 background growth = 10^-62 level -- unmeasurable.

Result: A12 growth equation does NOT contain an SQMH-distinctive sector.
A12 at perturbation level is effectively LCDM growth with erf background.

### [Member 3 -- Growth equation: C11D]

C11D = CLW exponential quintessence, lambda = 0.8872.
Growth equation for quintessence (no coupling, dark-only):

delta_m'' + (2 + E'/E) delta_m' = (3/2) Omega_m(a)/E^2 * delta_m

The key modification comes through Omega_m(a)/E^2 which differs from
LCDM due to the quintessence contribution to H(z).

From CLW: Omega_phi = x^2 + y^2. At best-fit (lambda=0.8872, thawing):
Omega_phi(z=0) ~ 0.70, x ~ 0 (thawing -> slow-roll).

G_eff/G = 1 for pure disformal with A'=0 (ZKB 2013, confirmed CLAUDE.md).
So C11D growth = standard quintessence growth (no extra G_eff boost).

SQMH EFT of C11D at perturbation level:
The SQMH term adds -sigma*rho_m to the n-continuity. In growth language,
this maps to a sub-leading correction of order sigma*rho_m/H ~ 10^-62.

Result: C11D does NOT produce SQMH-distinctive EFT structure at
perturbation level. The EFT of C11D at growth equation level is
standard quintessence growth.

### [Member 4 -- Growth equation: C28]

C28 = RR non-local gravity (Maggiore-Mancarella).

The linearised growth equation for RR gravity (Dirian+2015, eq 3.3):
Contains an effective Newton constant modification:
G_eff/G = 1 + delta_G_RR(a)

From Dirian 2015, at gamma_0 = 0.0015:
delta_G_RR(z=0) ~ +gamma_0 * O(1) ~ 0.0015 * O(1).

This gives a SMALL but non-zero modification to growth:
f*sigma8 shift of order gamma_0 ~ 0.15%.

Can SQMH map onto this G_eff modification?

SQMH growth contribution: -sigma*delta_n/n_bar ~ sigma*rho_m*delta/H^2 ~ 10^-62.
C28 growth contribution: delta_G_RR ~ 10^-3.

Ratio = 10^-59. No EFT mapping possible.

Result: C28 growth modification (G_eff ~ 1 + 0.0015) is real but
cannot be mapped to SQMH perturbation coupling (10^-62 level).
These two modifications are NOT the same EFT sector.

### [Member 5 -- f*sigma8 phenomenology]

Observed f*sigma8 data:
- DESI DR2 + 2dFGRS + SDSS composite: f*sigma8(z~0.1-0.8) ~ 0.4-0.5.
- LCDM prediction: f*sigma8(z=0.5) ~ 0.46 (Planck cosmology).

A12 prediction: f*sigma8 indistinguishable from LCDM (mu_eff=1).
C11D prediction: f*sigma8 slightly below LCDM due to smaller Omega_m/E^2.
C28 prediction: f*sigma8 slightly above LCDM due to G_eff > 1 (delta_G ~ +0.0015).

SQMH EFT prediction: sigma*rho_m correction to f*sigma8 ~ 10^-62 * f*sigma8.
Observable implication: zero shift -- indistinguishable from LCDM growth.

The SQMH somatic coupling sigma at cosmological scales generates NO
observable EFT signature in large-scale structure. This is consistent with
the cosmological principle: sigma is fixed at the Planck scale to match
local quantum metabolism, not tuned for LSS.

### [Member 6 -- EFT operator analysis]

EFT of dark energy framework (Gubitosi-Piazza-Vernizzi 2013, Gleyzes+2015):
SQMH effective action in EFT-DE language:

S_SQMH = S_GR + S_m + integral d^4x sqrt(-g) [n_bar * mu - sigma * n_bar * rho_m]

In EFT-DE notation, the sigma*n_bar*rho_m term is a bi-linear coupling.
Standard EFT-DE operators: M2, Lambda, alphaB, alphaM, alphaK, alphaT.

The sigma coupling maps to none of these standard operators because:
1. It couples DE density (n_bar) to matter density (rho_m) directly.
2. This is an energy-exchange (IDE) term, not a kinetic/tensor mixing.

SQMH as IDE EFT: The sigma term IS a valid interacting dark energy EFT
operator -- but at scale sigma = 4pi*G*t_P, the IDE coupling at
cosmological scales Q_IDE = sigma*n_bar*rho_m ~ Gamma_0 * (sigma*rho_m/3H)
~ 10^-62 * H * rho_DE.

This is 62 orders of magnitude below any observable IDE signal.
Standard IDE constraints (Wetterich, Di Porto-Amendola) require
|Q_IDE| ~ 0.01-0.1 H rho_DE to matter.

EFT verdict: SQMH IS a valid EFT operator structure -- but its coefficient
is 10^-62 below detectability. The candidates (A12, C11D, C28) do not
need to replicate this EFT sector because it is phenomenologically inert
at cosmological scales.

### [Member 7 -- Scale-dependent EFT: could sigma run?]

Question: Could sigma = 4pi*G*t_P be a UV value that runs under the
renormalization group to a larger effective value at cosmological scales?

RG running of sigma:
sigma has dimension [m^3 kg^-1 s^-1] = [G * t_P] = [G * (hbar*G/c^5)^(1/2)].

In a Wilsonian EFT, sigma runs as:
sigma(mu) = sigma_UV * f(mu/mu_UV)

where mu is the RG scale. From mu_Planck to mu_H0:
mu_H0/mu_Planck ~ H0/m_Planck*c^2 ~ 10^-61.

If sigma runs as power law sigma ~ mu^n, we need:
sigma(H0)/sigma(m_P) ~ (H0/m_Pc^2)^n ~ 10^-61n.

To reach sigma(H0) ~ H0/rho_m0 ~ 10^9 m^3/(kg*s), need:
10^9 / 4.52e-53 = 10^61 ~ 10^-61n -> n ~ -1.

NEW FINDING CANDIDATE: If sigma runs as sigma(mu) ~ mu^-1 (i.e., sigma
scales inversely with RG scale), then sigma_cosmo ~ sigma_Planck * (m_P*c^2/H0)
~ 4.52e-53 * 10^61 ~ 10^9 m^3/(kg*s) = H0/rho_m0.

This would EXACTLY bridge the 61-order gap between sigma_SQMH and sigma_need!

Immediate cross-share to full team for discussion.

### [Member 8 -- EFT running: deliberation on Member 7 finding]

Team deliberation on the sigma ~ mu^-1 running hypothesis:

Physical content:
- sigma = 4pi*G*t_P at Planck scale: this is the "microscopic" coupling
  (quantum gravity - metabolism interface at Planck length scale).
- sigma_cosmo ~ H0/rho_m0: this would be the "macroscopic" EFT coupling
  at Hubble scale.

Is sigma ~ mu^-1 physically motivated?
- Dimensional analysis: [sigma] = [G][t_P] = [G][G^(1/2)] (in Planck units).
- sigma ~ G * t_P ~ G^(3/2) * hbar^(1/2) / c^(5/2).
- Under RG, G running: G(mu) ~ G_0 * [1 + nu * (mu^2 - mu_0^2)/m_P^2]
  (asymptotic safety, Bonanno-Platania, noted in CLAUDE.md).
- t_P running: t_P(mu) ~ sqrt(hbar*G(mu)/c^5) ~ t_P0 * [G(mu)/G0]^(1/2).
- sigma(mu) ~ G(mu) * t_P(mu) ~ G(mu)^(3/2).
- In AS framework: G(mu) ~ G_0 / (1 + (mu/mu_*)^2) for mu >> mu_*.
  At cosmological scales mu ~ H0 << mu_*, G(mu) ~ G_0. NO running.

Result: Standard RG running (asymptotic safety) does NOT produce
sigma ~ mu^-1 at cosmological scales. The G running in AS is only
significant at mu ~ m_Planck.

REVISED ASSESSMENT of Member 7 finding:
The sigma ~ mu^-1 hypothesis is mathematically clean but physically
unjustified. There is no known RG framework that produces this running
from Planck scale to Hubble scale. It would require a new mechanism
(e.g., large extra dimensions, violation of standard RG decoupling).

CLASSIFICATION: Speculative hypothesis, not a confirmed bridge.
Flagged as: "sigma_RG_running: mathematically possible, physically unmotivated."

---

## Round 2 Team Consensus

**EFT / LSS Level Results:**

| Candidate | EFT at Perturbation Level | SQMH Mapping? | Result |
|-----------|--------------------------|---------------|--------|
| A12       | Standard LCDM growth (mu_eff=1) | 10^-62 correction | NO EFT MATCH |
| C11D      | Quintessence growth (no G_eff) | 10^-62 correction | NO EFT MATCH |
| C28       | G_eff = 1 + delta_G_RR ~ 1.0015 | 10^-59 mismatch | NO EFT MATCH |

**SQMH EFT at cosmological perturbation level:**
- The SQMH somatic coupling sigma generates zero observable EFT
  signature at LSS scales. SQMH is effectively LCDM EFT at all
  perturbation orders above 10^-62 level.

**NEW FINDING (Speculative, not confirmed):**
- sigma_RG_running hypothesis: if sigma runs as sigma ~ mu^-1 from
  Planck to Hubble scale, the 61-order gap bridges exactly.
- Status: Mathematically possible, physically unmotivated in any
  known RG framework. Flagged for future investigation only.
  Cannot support Q32/Q33 claims.

**Round 2 Verdict:**
- Q31/Q32/Q33: REMAIN FAIL at EFT/perturbation level.
- No new passing criteria found.
- New speculative finding: sigma_RG_running (flagged, not a claim).
- All three candidates have EFT sectors distinguishable from SQMH by
  59-62 orders of magnitude in the somatic coupling.

---

*Round 2 complete: 2026-04-11*
