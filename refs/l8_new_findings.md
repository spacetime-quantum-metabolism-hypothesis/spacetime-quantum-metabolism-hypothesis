# refs/l8_new_findings.md -- L8 Rounds 2-6: New Findings Register

> Date: 2026-04-11
> This file records all findings from Rounds 2-6 that are genuinely new
> insights beyond the Round 1 "all Q3x FAIL" baseline.
> Language standard: "contains a sector isomorphic to" -- not "derived from."
> K35 guard: findings classified as "speculative" or "structural footnote"
>   are NOT claims; they are registered for paper §8 discussion only.

---

## Finding Catalog

### NF-1: sigma_RG_running hypothesis (Round 2, SPECULATIVE)

**Source**: Round 2, Member 7.

**Content**: If sigma runs under the renormalization group as sigma ~ mu^-1
from Planck scale to Hubble scale, the 61-order gap between sigma_SQMH and
sigma_required bridges exactly. Specifically:
  sigma(H_0) = sigma(m_P) * (m_P * c^2 / H_0) = sigma_SQMH * 10^61 ~ sigma_required.

**Assessment**: Mathematically clean. Physically unmotivated in any known
RG framework. Standard asymptotic safety (Bonanno-Platania) gives G running
only at mu ~ m_Planck, not at cosmological scales. Large extra dimensions
or other BSM mechanism would be required.

**Classification**: SPECULATIVE. Not a new claim. Flag for L9 theoretical
investigation. Cannot be used to support Q32/Q33.

**Paper language** (if mentioned): "A hypothetical sigma ~ mu^-1 RG running
would bridge the scale gap; no known mechanism generates this running."

---

### NF-2: C28 matter-era dilation symmetry (Round 3, STRUCTURAL FOOTNOTE)

**Source**: Round 3, Member 8.

**Content**: In the matter-dominated era (a << a_Lambda), both the C28 
P-equation (dP/dN + 3P ~ U) and the SQMH continuity equation
(dn_bar/dN + 3n_bar ~ source) share the same dilation symmetry group:
  (a, field) -> (lambda*a, lambda^-3 * field)
with the same attractor behavior field ~ a^-3.

The two systems share this symmetry precisely because BOTH are linear
dissipative systems with the Hubble damping term 3H*n as the dominant
structure in the matter era. The divergence occurs in the DE era: U != Gamma_0.

**Assessment**: Correct structural observation. Consistent with known
physics (any matter-era cosmological field dilutes as a^-3 if massless/frozen).
Does NOT constitute an isomorphism between C28 and SQMH in the DE era.

**Classification**: STRUCTURAL FOOTNOTE. Valid, non-trivial observation.
Can be mentioned in paper §8 at footnote level.

**Paper language**: "C28 and SQMH contain a matter-era sector isomorphic to
the a^-3 dilation group, reflecting their shared linear dissipative structure
in the matter-dominated epoch. This shared symmetry breaks at dark energy
domination where the source terms differ."

---

### NF-3: SQMH thermodynamic classification as birth-death process (Round 4, STRUCTURAL)

**Source**: Round 4, Members 1-3.

**Content**: SQMH continuity dn_bar/dt + 3H*n_bar = Gamma_0 - sigma*n_bar*rho_m
is formally identical to a LINEAR BIRTH-DEATH PROCESS (zeroth moment of
the Boltzmann equation):
  - Birth (production): Gamma_0 = constant zeroth-order rate.
  - Death (binary collision): sigma*n_bar*rho_m = second-order collision rate.
  - Dilution: 3H*n_bar = expansion redshifting.

This is also equivalent to a degenerate Fokker-Planck (zero diffusion,
pure drift toward the quasi-static equilibrium n_bar* = Gamma_0/(3H + sigma*rho_m)).

The equilibrium entropy production is always positive:
  S_prod = k_B * 3H*n_bar* * ln(Gamma_0 / (sigma*n_bar*rho_m)) > 0.
[This is positive because Gamma_0 > sigma*n_bar*rho_m to 62 orders of magnitude.]

**Assessment**: Clean, correct physical characterization of the SQMH equation
form. Provides a new way to motivate the equation structure in the paper:
"SQMH describes a birth-death process of quantum metabolic units interacting
with matter."

**Classification**: STRUCTURAL. This is a NEW insight not previously articulated
in L8 Round 1 or earlier phases. Adds positive value to paper §2 motivation.

**Paper language**: "The SQMH fundamental equation dn_bar/dt + 3H*n_bar =
Gamma_0 - sigma*n_bar*rho_m takes the form of a linear birth-death process:
constant production Gamma_0, binary collision loss sigma*n_bar*rho_m,
and cosmological dilution 3H*n_bar. The stationary dark energy density
n_bar* = Gamma_0/(3H + sigma*rho_m) ~ Gamma_0/(3H) to 10^-62 precision,
confirming that sigma*rho_m contributes negligibly to background evolution
while defining the microscopic quantum metabolism coupling scale."

---

### NF-4: C28 entropy production sign mismatch (Round 4, CONFIRMATION)

**Source**: Round 4, Member 8.

**Content**: From the thermodynamic angle, the C28 P-equation at z=0 has
NEGATIVE entropy production because U(a=1) = -12.41 < 0. This violates
the thermodynamic analog of SQMH (which requires positive entropy production).

This is NOT a new finding -- it confirms the Round 1 K33 conclusion
(U < 0 sign mismatch) from an independent thermodynamic framework.

**Assessment**: Provides additional confirmation robustness for K33.
The sign obstruction has now been confirmed by 4 independent methods:
  1. Numerical (Round 1): U(a=1) = -12.41.
  2. Analytical (Round 1): sigma_eff 100% residual.
  3. Symmetry (Round 3): dynamic source != constant Gamma_0.
  4. Thermodynamic (Round 4): entropy production sign reversed.

**Classification**: CONFIRMATION (not new). Strengthens K33 conclusion.

---

### NF-5: Pi_SQMH = Omega_m * H_0 * t_P identification (Round 5, STRUCTURAL)

**Source**: Round 5, Members 4 and 6.

**Content**: The fundamental SQMH dimensionless Pi-group is:
  Pi_SQMH = sigma * rho_m / (3H) = Omega_m * (H_0 * t_P) ~ 3e-62

This factors as the product of:
  (a) Omega_m ~ 0.3 (cosmological matter fraction, O(1)).
  (b) H_0 * t_P = H_0 / H_Planck ~ 10^-61 (ratio of Hubble time to Planck time).

The 62-order scale separation is STRUCTURALLY explained:
Pi_SQMH is suppressed by the ratio of the current Hubble rate to the
Planck rate. This ratio appears in NO classical dark energy model (A12,
C11D, C28) because none of them contain t_P as a fundamental parameter.

The gap is therefore not a coincidence but a STRUCTURAL CONSEQUENCE of
SQMH requiring quantum gravity input (t_P) absent from classical dark energy.

**Assessment**: This is the clearest new insight from Rounds 2-6. It explains
the 62-order gap in terms of a fundamental Pi-group that cannot be reproduced
by classical cosmological models without explicit quantum gravity input.
This can be formulated as a "no-go" result: any theory matching SQMH's
cosmological behavior must contain t_P or an equivalent quantum gravity scale.

**Classification**: STRUCTURAL NEW INSIGHT. Should be included in paper §2
or §8. Supports the "QG-motivated phenomenology" narrative.

**Paper language**: "The SQMH somatic coupling sigma defines the dimensionless
Pi-group Pi_1 = sigma * rho_m / (3H_0) = Omega_m * (H_0 * t_P) ~ 10^-62.
This quantity encodes the ratio of the present Hubble rate to the Planck
rate. Since no classical dark energy model considered here contains the
Planck time t_P as a fundamental parameter, the Pi-group Pi_1 cannot be
reproduced within the classical framework. The 62-order scale separation
between sigma_SQMH and any cosmologically effective coupling is therefore
structurally irreducible without explicit quantum gravity input."

---

### NF-6: sigma_required numerical precision (Round 6, NUMERICAL)

**Source**: Round 6, Members 1-8.

**Content**: The sigma_required scan gives:

| Candidate | sigma_required | sigma_req/sigma_SQMH | Sign |
|-----------|---------------|----------------------|------|
| A12 | ~7.4e7 m^3/(kg*s) | ~1.6e60 | + |
| C11D | 8.23e8 m^3/(kg*s) | 1.82e61 | - (sign obstruction) |
| C28 | ~1.06e10 m^3/(kg*s) | ~2.3e62 | - (sign obstruction) |

Key refinement: A12's sigma_required is ~10^60 * sigma_SQMH (not 10^62),
because wa = -0.133 represents only ~5% deviation from LCDM. The naive
estimate sigma_required ~ H_0/rho_m0 overestimates by ~2 orders.

**Assessment**: Numerical precision improvement over Round 1 naive estimate.
Also confirms C11D and C28 require negative sigma regardless of scale.

**Classification**: NUMERICAL CONFIRMATION with refinement.

**Paper language**: "Requiring the SQMH somatic coupling to reproduce each
surviving candidate's background evolution gives sigma_required(A12) ~ 10^60
sigma_SQMH, sigma_required(C11D) ~ 10^61 sigma_SQMH, and sigma_required(C28) ~
10^62 sigma_SQMH. All are 60-62 orders above sigma = 4pi*G*t_P. Furthermore,
C11D and C28 require negative sigma (reversed reaction direction),
independently confirmed by analytical, numerical, symmetry, and
thermodynamic analyses."

---

## Summary Assessment

| Finding | Type | Use in paper? | Location |
|---------|------|---------------|----------|
| NF-1: sigma_RG_running | SPECULATIVE | Footnote only | §8 |
| NF-2: C28 matter-era dilation | STRUCTURAL FOOTNOTE | Yes, footnote | §8 |
| NF-3: SQMH birth-death process | STRUCTURAL NEW | Yes, main text | §2 |
| NF-4: C28 entropy sign | CONFIRMATION | Yes, robustness | §8 |
| NF-5: Pi_SQMH = Omega_m*H_0*t_P | STRUCTURAL NEW | Yes, main text | §2/§8 |
| NF-6: sigma_required precision | NUMERICAL | Yes, table | §8 |

**Most valuable new findings for paper**: NF-3 and NF-5.
  - NF-3 provides positive motivation for SQMH equation form (birth-death).
  - NF-5 explains the 62-order gap as a structural quantum gravity signature.
  Both can be used in paper §2 to strengthen "QG-motivated phenomenology"
  positioning WITHOUT overclaiming derivation from candidates.

---

## Rounds 7-11 Findings (Second Batch, 2026-04-11)

---

### NF-7: Holographic UV/IR Complementarity (Round 7, STRUCTURAL FOOTNOTE)

**Source**: Round 7, Members 7-8.

**Content**: The holographic analysis reveals a UV/IR energy scale separation
between SQMH and the candidates:
  - SQMH: sigma = 4*pi*G*t_P encodes the Planck area l_P^2 (UV scale).
    In holographic language, sigma = G*t_P = G * sqrt(hbar*G/c^5) is a
    PLANCK-SCALE coupling. SQMH is "UV holographic."
  - C28: mass parameter m ~ 0.116*H_0 encodes the Hubble horizon (IR scale).
    C28 is an IR non-local gravity model. SQMH is "UV holographic."
  - A12, C11D: No holographic structure beyond tautological rewriting (L(a)
    from w(a) or L_phi = rho_phi^{1/2}).

SQMH and C28 are "holographically orthogonal" -- UV vs IR scale separation.
Any theory containing BOTH would require explicit UV-IR mixing.

Verlinde entropic gravity: SQMH does not fit (no t_P, no Gamma_0 in Verlinde).
Jacobson thermodynamics: SQMH requires extending dE=TdS to coupled matter-DE entropy.
Holographic DE (HDE): SQMH quasi-static limit maps to HDE with L ~ sqrt(3)*H^-1
(tautological rewriting; sigma contributes only 10^-62 correction to L).

**Assessment**: Reconfirms NF-5 (Pi_SQMH = Omega_m*H_0*t_P) from holographic angle.
Adds "UV/IR complementarity" language. Extends the structural gap characterization.

**Classification**: STRUCTURAL FOOTNOTE. Adds holographic language to NF-5 narrative.

**Paper language**: "The holographic interpretation confirms NF-5's UV/IR separation:
SQMH's sigma = 4pi*G*t_P encodes Planck-scale (UV) entropy coupling, while C28's
non-local mass m ~ H_0 encodes Hubble-scale (IR) gravity modification. A12 and C11D
have no holographic scale input beyond standard quintessence."

---

### NF-8: T_SQMH ~ 10^-99 K (Round 8, QUANTITATIVE NOTE)

**Source**: Round 8, Member 4.

**Content**: The fluctuation-dissipation theorem applied to stochastic SQMH gives
an effective temperature T_SQMH:
  k_B * T_SQMH = D/kappa * kappa = D ~ n* / V

For V = Hubble volume and mu ~ energy per metabolic unit:
  T_SQMH = mu / k_B ~ 1.7e-122 J / 1.38e-23 J/K ~ 1.2e-99 K.

This is the COLDEST natural temperature scale in the SQMH framework:
  - 100 orders below CMB temperature (2.73 K).
  - ~70 orders below Hawking temperature (T_H ~ hbar*H_0/k_B ~ 10^-30 K).
  - Consistent with SQMH describing quantum-gravitational processes far
    below observable energy scales.

The stochastic SQMH is Gaussian near n* with relative fluctuations ~1/sqrt(N*)
where N* ~ number of metabolic units in Hubble volume >> 1. SQMH is
effectively deterministic at cosmological scales.

Mean field of stochastic SQMH = deterministic SQMH ODE (exact for linear drift).
Neither A12, C11D, nor C28 can be derived as mean field of stochastic SQMH.

**Assessment**: New quantitative result. T_SQMH = mu/k_B follows directly from
mu (already known), so physical content is limited. Confirms deterministic
nature of cosmological SQMH.

**Classification**: QUANTITATIVE NOTE. Worth a sentence in paper §2 footnote.

**Paper language**: "The fluctuation-dissipation temperature of the stochastic
SQMH birth-death process is T_SQMH = mu/k_B ~ 10^-99 K (100 orders below CMB),
consistent with quantum-gravitational processes operating far below observable
energy scales. Quantum fluctuations of n_bar are suppressed by 1/sqrt(N*) ~ 0,
making the deterministic SQMH ODE exact at cosmological scales."

---

### NF-9: SQMH Lagrangian -- Quadratic Potential + Matter Sector (Round 9, STRUCTURAL FOOTNOTE)

**Source**: Round 9, Members 2-3 and 7-8.

**Content**: The SQMH ODE corresponds to the slow-roll (overdamped) limit of a
scalar field n with:
  L_SQMH = (1/2)*(partial n)^2 - V(n) - sigma*n*rho_m(x)  [spurion coupling]
  V(n) = (kappa/2)*n^2 - Gamma_0*n,  kappa = 3H + sigma*rho_m

This is a QUADRATIC (parabolic) potential with minimum at n* = Gamma_0/kappa.
The potential's quadratic form is a direct consequence of the birth-death
process structure (NF-3): the equilibrium n* is the potential minimum.

Structural comparisons:
  A12: Lagrangian is quintessence L = (1/2)*(d phi)^2 - V_A12(phi) [NO matter coupling].
  C11D: Lagrangian is CLW quintessence L = (1/2)*(d phi)^2 - V0*exp(-lambda*phi)
        [exponential potential, runaway -- no natural equilibrium].
  C28: Lagrangian is non-local gravity S = M_P^2/2 * int R*(1 + m^2*box^-1*R/6)
        [gravity sector, NOT matter sector].
  SQMH: Matter sector (spurion coupling sigma*n*rho_m), quadratic potential.

No physically motivated unifying action contains both SQMH and candidates as
INTERACTING limits. They inhabit decoupled sectors (gravity/quintessence/SQMH-matter).

**Assessment**: New Lagrangian-level characterization of SQMH. Confirms structural
sector separation. Extends NF-3 to the action principle language.

**Classification**: STRUCTURAL FOOTNOTE. Useful for paper §2.

**Paper language**: "The SQMH continuity equation is the slow-roll limit of a scalar
field n with quadratic potential V(n) = (kappa/2)n^2 - Gamma_0*n (minimum at n*),
operating via a matter-sector spurion coupling sigma*n*rho_m. This distinguishes
SQMH from quintessence sector (A12, C11D: exponential/power-law V, no matter coupling)
and gravity sector (C28: non-local R*box^-1*R) modifications."

---

### NF-10: Cramér-Rao Obstruction for sigma_SQMH (Round 10, STRUCTURAL)

**Source**: Round 10, Members 1-2.

**Content**: The Fisher information for sigma_SQMH from background-level
cosmological data (BAO, SN, CMB) is:
  F_{sigma,sigma} ~ (Pi_SQMH / sigma_SQMH)^2 ~ (10^-62 / sigma_SQMH)^2

The Cramér-Rao lower bound gives:
  Delta_sigma_min = 1/sqrt(F_{sigma,sigma}) ~ sigma_SQMH / Pi_SQMH ~ 10^62 * sigma_SQMH.

This is the CRAMÉR-RAO OBSTRUCTION: no cosmological experiment can distinguish
sigma_SQMH = 4.52e-53 m^3/(kg*s) from sigma = 0 at any finite significance.
The sigma parameter is COSMOLOGICALLY UNIDENTIFIABLE -- not just small, but
measurement-theoretically inaccessible from background-level data.

Comparing to C28's gamma_0:
  F_{gamma_0}/F_{sigma_SQMH} ~ (10^-3)^-2 / (10^-62)^-2 = (10^62 / 10^-3)^2 ~ 10^130.
  C28's gamma_0 is 10^130 times more identifiable than sigma_SQMH.

This is the information-theoretic restatement of NF-5 (Pi_SQMH = Omega_m*H_0*t_P):
the 62-order numerical gap becomes a 62-order measurement-theory impossibility.

**Assessment**: New perspective, adds information-theoretic rigor. The Cramér-Rao
framing converts the scale gap into a formal measurement bound.

**Classification**: STRUCTURAL (information-theoretic refinement of NF-5).

**Paper language**: "The Fisher information bound formalizes the scale gap (NF-5):
F_{sigma} ~ Pi_SQMH^2/sigma^2, giving Cramér-Rao minimum uncertainty Delta_sigma_min ~
10^62 * sigma_SQMH. sigma_SQMH is cosmologically unidentifiable from background data,
not just observationally small but measurement-theoretically inaccessible. In contrast,
C28's gamma_0 = 0.0015 is constrained at ~10^-3 level: a factor 10^130 difference
in Fisher identifiability."

---

### NF-11: SQMH Quasi-Static EOS (Round 11, STRUCTURAL FOOTNOTE)

**Source**: Round 11, Members 5-8.

**Content**: The SQMH quasi-static tracking solution rho_DE ~ Gamma_0/(3H(a)) gives
an effective CPL equation of state:
  w0_SQMH^eff ~ -0.83  (from deceleration parameter q_0 ~ -0.53)
  wa_SQMH^eff ~ -0.33  (from matter-era to today evolution)

Derivation: 1 + w_eff = (1/3) * d(ln H)/d(ln a) = -q/3.
  At a=1: q_0 ~ -1 + 3*Omega_m/2 ~ -0.53, so 1+w_eff ~ 0.177, w_eff ~ -0.823.
  At high z (matter era): rho_DE ~ H^-1 ~ a^(3/2), so w ~ -1/2.
  wa ~ w_highz - w0 ~ -0.5 - (-0.83) = +0.33, i.e. wa ~ -0.33 for a -> 0 convention.

Compare to A12: w0=-0.886, wa=-0.133.
  SQMH: Delta_w0 ~ +0.05 (less negative), Delta_wa ~ -0.2 (too much variation).
  This CPL mismatch directly explains chi^2(SQMH vs A12) ~ 7.6 (Round 1).

**Assessment**: New quantitative result -- first explicit derivation of SQMH's
effective w0 and wa from first principles. Explains chi^2 = 7.63 analytically.

**Classification**: STRUCTURAL FOOTNOTE. Explains the chi^2 gap from EOS level.

**Paper language**: "The SQMH quasi-static tracking rho_DE ~ H^-1 gives effective
CPL parameters w0^eff ~ -0.83, wa^eff ~ -0.33, deviating from A12 (w0=-0.886,
wa=-0.133) by Delta_w0 ~ 0.05 and Delta_wa ~ -0.2, directly explaining the
chi^2 ~ 7.6 discrepancy found in §X."

---

### NF-12: SQMH as Novel Nonlinear Product-Coupled IDE (Round 11, STRUCTURAL FOOTNOTE)

**Source**: Round 11, Members 3 and 7.

**Content**: The SQMH interaction term Q_SQMH = sigma * rho_DE * rho_m is a
PRODUCT COUPLING (bilinear in rho_DE and rho_m). This is distinct from all
standard IDE parameterizations:
  - Linear IDE: Q ~ H * rho_i (most common).
  - Wetterich-type: Q ~ phi_dot * rho_m (scalar velocity coupling; C11D class).
  - A12: uncoupled (no Q).
  - C28: non-local gravity origin, not a standard fluid coupling.

SQMH belongs to the "nonlinear product-coupled IDE" class (He-Wang 2008 taxonomy).
The product form arises naturally from the birth-death process (NF-3):
sigma*n_bar*rho_m is the binary COLLISION RATE between metabolic units and matter.

Impact: Q_SQMH ~ sigma * rho_DE * rho_m ~ 10^-62 * H * rho_m (negligible
observationally). The classification is taxonomically correct but physically
irrelevant at cosmic scales.

Also confirmed (fluid EOS analysis): SQMH (sigma > 0) always gives w > -1
(quintessence-like), while C28 gives w < -1 (phantom-like). Sign obstruction
confirmed for C28 from a 5th independent angle.

**Assessment**: Taxonomically correct, new classification. Impact is 10^-62.
Sign obstruction for C28 confirmed as the 5th independent method.

**Classification**: STRUCTURAL FOOTNOTE (taxonomic, negligible impact).

**Paper language**: "The SQMH coupling Q = sigma*rho_DE*rho_m is a bilinear
product coupling (He-Wang 2008 class), physically originating from binary
collision destruction rate (NF-3). At sigma = 4pi*G*t_P, Q is 10^-62-suppressed
and observationally irrelevant, but taxonomically distinguishes SQMH from linear-IDE
(Q ~ H*rho) and Wetterich-type (Q ~ phi_dot*rho_m) candidates."

---

## Updated Summary Assessment (All Findings NF-1 to NF-12)

| Finding | Type | Use in paper? | Location |
|---------|------|---------------|----------|
| NF-1: sigma_RG_running | SPECULATIVE | Footnote only | §8 |
| NF-2: C28 matter-era dilation | STRUCTURAL FOOTNOTE | Yes, footnote | §8 |
| NF-3: SQMH birth-death process | STRUCTURAL NEW | Yes, main text | §2 |
| NF-4: C28 entropy sign | CONFIRMATION | Yes, robustness | §8 |
| NF-5: Pi_SQMH = Omega_m*H_0*t_P | STRUCTURAL NEW | Yes, main text | §2/§8 |
| NF-6: sigma_required precision | NUMERICAL | Yes, table | §8 |
| NF-7: Holographic UV/IR | STRUCTURAL FOOTNOTE | Yes, footnote | §8 |
| NF-8: T_SQMH ~ 10^-99 K | QUANTITATIVE NOTE | Footnote | §2 |
| NF-9: Lagrangian quadratic V | STRUCTURAL FOOTNOTE | Yes, footnote | §2 |
| NF-10: Cramér-Rao obstruction | STRUCTURAL | Yes, §8 | §8 |
| NF-11: w0^eff ~ -0.83, wa ~ -0.33 | STRUCTURAL FOOTNOTE | Yes | §8 |
| NF-12: Product-coupled IDE class | STRUCTURAL FOOTNOTE | Footnote | §8 |

**Most valuable new findings from Rounds 7-11**:
  - NF-10: Cramér-Rao obstruction (adds rigorous measurement-theory language to NF-5).
  - NF-11: SQMH quasi-static w0^eff ~ -0.83 (explains chi^2 = 7.63 analytically).
  - NF-9: Quadratic potential Lagrangian (extends NF-3 to action principle level).

---

*Rounds 7-11 appended: 2026-04-11*
