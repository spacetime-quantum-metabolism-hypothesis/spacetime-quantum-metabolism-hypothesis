# refs/l9_paper_section2_draft.md -- L9 Round 14: Draft Paper Section 2 (Theory and Motivation)

> Date: 2026-04-11
> Source: All L9 findings (Rounds 1-13), NF-3, NF-5, NF-14, Q42, NF-16 resolution.
> Purpose: Actual paper prose for Section 2 (~500 words, JCAP style).
> Language standard: refs/l7_honest_phenomenology.md (QG-motivated phenomenology).
> Anti-overclaiming: No claim that SQMH predicts wa exactly.
> Positioning: QG-motivated phenomenology for JCAP.

---

## Language Rules (from refs/l7_honest_phenomenology.md)

ALLOWED:
- "SQMH motivates a particular class of dark energy models"
- "The perturbation analysis shows G_eff/G - 1 = Pi_SQMH ~ 10^{-62}"
- "erf functional form is mathematically impossible in SQMH"
- "C28 shares CPL-level structural proximity with our best-fit template"

FORBIDDEN:
- "SQMH predicts wa = -0.133 exactly"
- "SQMH derives the erf proxy"
- "C28 is a parent theory of A12"
- "SQMH solves the S8 or H0 tension"

---

## Section 2: Theory and Motivation

### 2.1 The Spacetime Quantum Metabolism Hypothesis

We motivate our phenomenological dark energy templates from the Spacetime Quantum
Metabolism Hypothesis (SQMH), a QG-inspired framework in which spacetime degrees
of freedom undergo continuous birth-death kinetics. In the SQMH picture, a
spacetime "quantum" (an elementary unit of volume with energy scale mu ~ M_Planck)
is spontaneously created at rate Gamma_0 and annihilated upon collision with
ordinary matter at rate sigma*rho_m. The resulting number density n evolves as

  dn/dt + 3H*n = Gamma_0 - sigma*n*rho_m,        (2.1)

where H is the Hubble rate and rho_m is the matter energy density. This is a
linear birth-death process whose equilibrium density n_star = Gamma_0/(3H + sigma*rho_m)
acts as an effective dark energy sector. The SI value of sigma is sigma = 4*pi*G*t_P
[m^3 kg^{-1} s^{-1}] (not sigma = 4*pi*G in Planck units).

The key dimensionless combination governing SQMH dynamics is

  Pi_SQMH = Omega_m * H_0 * t_P ~ 1.85 x 10^{-62},        (2.2)

where t_P = sqrt(hbar*G/c^5) ~ 5.4 x 10^{-44} s is the Planck time. This quantity
represents the ratio of the current Hubble rate to the Planck rate, and is the
suppression factor for all SQMH modifications relative to LCDM.

### 2.2 Background and Perturbation-Level SQMH

At the level of the homogeneous background, the SQMH equilibrium density obeys

  rho_DE^{SQMH} = mu * n_star = Gamma_0/(3H + sigma*rho_m) = LCDM to O(Pi_SQMH).

Numerically, sigma*rho_m/(3H_0) = 1.83 x 10^{-62} (see Section 3),
making the SQMH background energy density indistinguishable from a cosmological
constant at any observable redshift. At the perturbation level, density
fluctuations delta generate a perturbation delta_n/n_star ~ Pi_SQMH * delta,
yielding an effective Newton constant

  G_eff/G = 1 - Pi_SQMH * (rho_DE/rho_m) = 1 - 4 x 10^{-62}        (2.3)

at z=0 -- again 62 orders below observational sensitivity (delta G_eff/G < 0.02
from CMB lensing). The SQMH framework therefore makes no testable prediction at
the background or linear perturbation level in its minimal form (NF-5, NF-3).

### 2.3 The erf Impossibility Theorem

Despite the 62-order suppression, the qualitative structure of the SQMH equation
motivates a class of dark energy models in which rho_DE tracks the matter density
through a smooth interpolation. We showed in preliminary analysis that the error
function (erf) provides an empirically well-motivated proxy for this interpolation
(A12 template, Section 4). However, a mathematical proof demonstrates that the
erf functional form cannot arise from the SQMH equation at any level:

  (i)   Background: rho_DE^{SQMH} is algebraic in H, rho_m -- no erf.
  (ii)  Perturbation: G_eff/G - 1 = Pi_SQMH -- no spatial erf.
  (iii) Gradient: The SQMH PDE contains only first-order spatial terms (advection);
        erf requires the second-order diffusion operator nabla^2 n, which is absent.
  (iv)  Stochastic: Fluctuations in n-space are diffusive, but this differs from
        a diffusion in position space; the latter would give erf(r), not erf(z).

We therefore position the A12 erf template as a QG-motivated phenomenological proxy,
not as a direct derivation from SQMH. Its empirical success (Bayesian evidence
Delta ln Z > 8.6, Section 5) is attributed to its flexibility in capturing a
wa < 0 dark energy structure rather than to any SQMH first-principles prediction.

### 2.4 Independent Theoretical Support: C28 RR Non-Local Gravity

An independent theoretical motivation for the wa < 0 regime comes from the RR
non-local gravity model of Maggiore and Mancarella (C28). In this framework, the
gravitational action is augmented by the non-local term

  S_NL = (m^2/6) * integral R * Box^{-1} R * sqrt{-g} d^4x,        (2.4)

where Box^{-1} is the retarded Green's function of the d'Alembertian operator.
The model introduces two auxiliary scalar fields U = -Box^{-1}R and V = -Box^{-1}U
whose late-time evolution (constrained by the modified Friedmann equation with
E^2(a=1) = 1 enforced by a self-consistency condition on the mass parameter m)
generates an effective dark energy with CPL approximation

  w0_C28 ~ -0.93,   wa_C28 ~ -0.18,        (2.5)

(Dirian et al. 2015, confirmed by our forward ODE shooting with gamma0 = m^2/H_0^2
= 0.000624). The proximity to our best-fit A12 template (wa_A12 = -0.133) at
the level |Delta wa| = 0.043 < 0.10 (Q42 PASS) is a numerical coincidence rather
than a derivational relationship: no mathematical limit of C28 reduces to A12
(Section 6 and refs/l9_a12_c28_limit.md). Nevertheless, the C28 prediction
provides independent physical motivation for the wa ~ -0.13 to -0.19 regime.
Both A12 and C28 occupy the same CPL cell at current DESI DR2 sensitivity
(sigma_wa = 0.24, Section 5.3).

---

## Section 2 Word Count and Status

Word count (above prose): approximately 560 words. Meets JCAP target (~500 words).

### Language check against refs/l7_honest_phenomenology.md:

- [PASS] "QG-motivated phenomenological proxy" positioning: YES
- [PASS] No claim "SQMH predicts wa=-0.133": correct, not stated
- [PASS] erf impossibility stated with proof structure: YES
- [PASS] C28 proximity stated as "numerical coincidence": YES
- [PASS] "No mathematical limit reduces A12 to C28": YES
- [PASS] Pi_SQMH = 10^{-62} quantitative bound: YES
- [PASS] S8/H0 tensions: NOT claimed resolved (moved to limitations)

### Open items for paper finalization:

1. Eq (2.3) G_eff/G: cite simulation ref simulations/l9/perturbation/sqmh_growth.py
2. Eq (2.5) C28 values: cite Dirian 2015 arXiv:1507.02141 + Round 11 shooting
3. Delta ln Z value in para 3: verify from base.l8.result.md (Delta ln Z = 10.77 for A12)
4. sigma_wa = 0.24: verify from base.l6.result.md DESI DR2 joint constraint
5. Section 6: reference to C28-A12 limit analysis (this round)

---

## Notes on JCAP Positioning

SQMH cannot be tested directly (62-order suppression). The paper's contribution is:
  1. The SQMH birth-death framework as motivation for a class of DE models (NF-3)
  2. The erf template as a flexible CPL-like parameterization (A12)
  3. The impossibility theorem as a clear theoretical bound (NF-14)
  4. The C28 connection as independent corroboration (Q42)

This positioning is consistent with "QG-motivated phenomenology" for JCAP and
avoids the overclaiming that would be needed for PRD Letters.

The phrase "QG-motivated phenomenological proxy" should appear in the abstract and
in the opening of Section 2, as agreed in the L6-L9 review team discussions.

---

*Round 14 completed: 2026-04-11*
*Team: theory (NF-3, NF-5 synthesis), impossibility (NF-14 formalization),
 C28 (Q42 NF-16 integration), language check (l7 rules)*
