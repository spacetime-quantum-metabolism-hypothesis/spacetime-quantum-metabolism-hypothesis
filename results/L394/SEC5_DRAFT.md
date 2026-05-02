# Section 5. Cosmology

## 5.1 Background scale matching: rho_q vs the cosmological constant

The Spacetime-Quantum-Metabolism (SQM) hypothesis posits a metabolic n-field whose
present-day energy density follows from the Planck-scale density divided by a
geometric 4 pi factor (see Sec. 2 for the construction). Numerically,

  rho_q_0 = 6.8555 x 10^-27 kg / m^3,

which is to be compared with the cosmological constant inferred from Planck 2018
in the same units,

  rho_Lambda(Planck) = 6.8555 x 10^-27 kg / m^3,

yielding the ratio

  rho_q_0 / rho_Lambda(Planck) = 1.0000  (4 significant figures, L207).

This is, to our knowledge, the closest first-principles match of a candidate
dark-energy density to the observed Lambda density that does not invoke
anthropic selection or fine-tuning. We emphasize, however, that the present
calculation does *not* yet distinguish between two interpretations:

  (i)  a structural prediction in which the SQM construction unavoidably fixes
       rho_q_0 to within O(unity) of rho_Lambda; or
  (ii) a coincidence enforced by the chosen normalization (Planck mass density
       divided by 4 pi).

Disentangling (i) from (ii) requires an independent, top-down derivation of the
4 pi normalization from the SQM action; this is left to future work.


## 5.2 Stress-energy tensor of the n-field

The covariant stress-energy of the n-field admits a fluid form (signature
(-,+,+,+) throughout):

  T^{mu nu}_n = (rho_q + p_q) u^mu u^nu + p_q g^{mu nu},

with rho_q = n epsilon / c^2 and, in the Lambda-like limit, p_q = - rho_q.
This form is *not* an a priori assumption: it follows from the variational
analysis of the SQM Lagrangian under a cosmological-symmetry ansatz (L207),
which selects fluid kinematics with a single equation of state w_q = p_q / rho_q.

The reduction to a perfect fluid is a leading-order result valid for the
homogeneous-isotropic background. Anisotropic and viscous corrections, which
would contribute at the level of cosmological perturbations, are not yet
characterized; they enter Section 6 as an open systematic.


## 5.3 Bianchi identity and energy exchange

Covariant conservation of the *total* matter+n stress tensor, together with
Bianchi identities of the Einstein equations, yields

  nabla_mu T^{mu nu}_n = - nabla_mu T^{mu nu}_m == Q^nu,

i.e. the n-field exchanges energy with the matter sector through a covariant
source Q^nu. The numerical magnitude of this exchange, evaluated at the present
epoch from the SQM dynamical equations, is

  | drho_q/dt | / (3 H rho_q) = 0.1041   (10.4 percent per Hubble time, L207).

A non-negligible exchange rate of this size means that the n-field is *not* a
pure cosmological constant; instead it is dynamically active at a level that
mimics a phantom- or quintessence-like dark-energy component on cosmological
time scales.


## 5.4 Comparison with DESI DR2

The DESI DR2 joint analysis (DESI + Planck + DES-SN5YR) reports, for a CPL
parametrization w(z) = w_0 + w_a z/(1+z),

  w_0 = -0.757 +/- 0.058,
  w_a = -0.83  (+0.24 / -0.21).

Mapping the SQM absorption rate of Sec. 5.3 onto an effective CPL amplitude
(leading order, background-only) gives an effective |w_a| of order 0.3, i.e.
about a factor three below the DESI central value. We therefore record, with
deliberate caution:

  *Direction* of evolution: phantom/quintessence-like, consistent in sign with
  DESI DR2.

  *Magnitude*: roughly one third of the DESI w_a central value. SQM and DESI
  are *not* in quantitative agreement at the present level of the calculation.

We resist the temptation to declare a successful fit. A direct joint
BAO + SN + CMB + RSD pipeline analogous to L34 / L46-L56, in which the SQM
background is propagated through the full likelihood without CPL truncation,
is required before any quantitative claim can be made. The present numbers
are background-level proxies and should not be cited as posterior values.

## 5.5 Falsifiable predictions

Within the regime in which the leading-order treatment is reliable, SQM
predicts:

  (P1) A persistently negative w_a with |w_a| in the range ~ 0.2 - 0.4.
       DESI DR3 will tighten the central value; |w_a| < 0.1 at >3 sigma would
       falsify the leading-order SQM phenomenology.

  (P2) A nontrivial coupling Q^nu producing percent-level scale-dependent
       modifications of the matter growth rate f sigma_8(z) at z ~ 0.3 - 1.
       Detection at this level requires DESI-FS or Euclid spectroscopic
       galaxy clustering.

  (P3) No significant resolution of the S8 tension at the background-only
       level (consistent with L5/L6 findings that mu_eff ~ 1 cannot relax S8).

## 5.6 Caveats and cross-links

We list the principal limitations of the present cosmological treatment:

  (C1) The 4 pi normalization of rho_q_0 has not been derived from a deeper
       SQM principle (Sec. 5.1).

  (C2) The fluid reduction of T^{mu nu}_n is leading order; perturbative
       anisotropy / shear has not been computed.

  (C3) The "effective w_a ~ -0.3" estimate is an order-of-magnitude proxy.
       A full joint-likelihood fit is required (deferred).

  (C4) The galactic-rotation evidence (L208) is *not* an independent test of
       Sec. 5: the SPARC anchor matches are by construction, and the
       Delta AICc = 99.5 reported there should not be cited as cosmological
       support.

  (C5) The dark-matter-direct-detection bound (L209) currently *fails* if the
       n-field is identified with a sub-eV cold dark-matter species through a
       naive nucleon coupling; the n-nucleon coupling has not been derived
       from the SQM action and this tension is recorded explicitly.

## 5.7 Honest one-line summary

SQM gives rho_q_0 / rho_Lambda(Planck) = 1.0000 and a covariant Bianchi
exchange of 10.4 percent per Hubble time, correct in sign relative to DESI
DR2 but a factor of about three below the observed |w_a| - the mechanism
passes, the quantitative fit is pending.
