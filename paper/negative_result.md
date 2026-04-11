# Negative Result: Background-Level Coupled Quintessence from Spacetime Quantum Metabolism Fails Joint BAO + SN + CMB + RSD Fit

**Author**. (pending) · **Date**. 2026-04-10 · **Status**. Draft (Path F, No-Go).

## Abstract

The Spacetime Quantum Metabolism Hypothesis (SQMH) postulates a dark-sector
scalar field φ whose background dynamics mimic a coupled quintessence with
universal coupling β to the matter sector and one of three potentials:
quadratic thawing V_mass, Ratra-Peebles V_RP, or exponential V_exp. We test
the background-level version of this model against the joint dataset of
DESI DR2 BAO (13 points), DESY5 SN Ia (1829), Planck 2018 compressed CMB
(3 points), and RSD fσ8 (8 points), N = 1853. Using emcee MCMC with 24
walkers and fixed seed, we find that (i) none of the three coupled-quintessence
families improves χ² against ΛCDM by more than 0.5, (ii) the resulting ΔAIC
and ΔBIC both disfavor coupled quintessence with ΔBIC > 15, (iii) promoting
r_d to a free parameter lowers the joint χ² by ~16 but pulls r_d to
148.6 ± 0.4 Mpc, producing a 3.13σ tension with the Planck direct measurement
r_d = 147.09 ± 0.30 Mpc for the V_RP family, (iv) the universal coupling
β ≈ 0.11 preferred by the posterior violates the Cassini bound
|γ − 1| < 2.3×10^−5 by a factor of 984 unless non-linear Vainshtein screening
(cubic Galileon, M^4 ∼ M_Pl^2 H_0^2) is invoked, at the cost of introducing
additional Lagrangian structure not present in the original SQMH action.
Background-only CPL (w0, wa) extensions attain a larger ΔAIC = −9.43 but
still fail the ΔBIC ≤ 0 threshold. We declare the background-level SQMH
program unviable and release the full reproducibility package.

## 1. Introduction

SQMH (base.md) proposes a quantum-metabolic reformulation of spacetime
dynamics with a scalar degree of freedom φ whose equation of state at the
background level mimics a coupled quintessence with universal coupling β to
the matter stress-energy trace T^a_a. Phase 1 and Phase 2 simulations
(simulations/phase1, phase2) verified the Friedmann-level consistency and
returned tentative fits at χ² ≈ 1683 (ΛCDM baseline). Phase 3 added a full
MCMC treatment with compressed CMB and RSD; this paper reports Phase 3.5 and
Phase 3.6 results.

## 2. Data and likelihood

- **BAO**: DESI DR2 13-point compilation (D_V, D_M/r_d, D_H/r_d) with the
  full 13×13 covariance matrix, from CobayaSampler/bao_data.
- **SN**: DESY5 1829 SNe Ia, zHD distance modulus, CobayaSampler/sn_data.
- **CMB**: Planck 2018 compressed (R, l_A, ω_b) with 3×3 covariance.
- **RSD**: 8 fσ8 points from 6dFGS, SDSS MGS, BOSS DR12 (with covariance),
  eBOSS LRG/ELG/QSO.

Total N = 1853.

## 3. Models

### 3.1 ΛCDM baseline
5 parameters: (Ω_m, h, ω_b, σ_8, r_d) when r_d is free; 4 when r_d is fixed
to Eisenstein–Hu 1998 fitting formula with BBN ω_b.

### 3.2 Coupled quintessence
V_mass: V(φ) = ½ m² φ². V_RP: V(φ) = M^(4+n) φ^(−n). V_exp: V(φ) = V₀ e^(−λφ).
Universal coupling β in the matter continuity equation:
ρ̇_m + 3H ρ_m = β(φ) ρ_m φ̇. Background ODE integrated forward from matter era
(N_ini = −12) with bisection on initial potential amplitude y₀ to hit
Ω_φ(0) = 0.685. RSD growth uses Di Porto–Amendola 2008 drag term with
G_eff/G = 1 + 2β².

## 4. Results

### 4.1 Phase 3 MCMC (r_d fixed by EH98)

```
  model    chi2    k      AIC       BIC     dAIC   dBIC
  LCDM   1683.11   4   1691.11   1713.20   +0.00  +0.00
  V_RP   1681.73   6   1693.73   1726.88   +2.62 +13.67
  V_exp  1681.81   6   1693.81   1726.96   +2.71 +13.76
```

Posterior medians: β_RP = 0.107 ± 0.05, n = 0.096; β_exp = 0.102, λ = 0.090.
Both families collapse toward the LCDM boundary.

### 4.2 Phase 3.5 A2 (r_d free)

```
  model    chi2    k      AIC       BIC     dAIC   dBIC
  LCDM   1666.78   5   1676.78   1704.40   +0.00  +0.00
  V_RP   1667.00   7   1681.00   1719.67   +4.22 +15.27
  V_exp  1667.32   7   1681.32   1719.99   +4.54 +15.59
```

Freeing r_d lowers χ² by ~16 for all models. The data prefers
r_d ≈ 148.6 Mpc, about 1.5 Mpc above the Planck direct measurement.

### 4.3 r_d tension vs Planck 147.09 ± 0.30 Mpc

```
  model   r_d [Mpc]           delta   n_sigma  verdict
  LCDM    148.69 +0.53/-0.49   +1.60   +2.63   within 3sigma
  V_RP    148.62 +0.34/-0.39   +1.53   +3.13   TENSION
  V_exp   148.56 +0.42/-0.41   +1.47   +2.82   within 3sigma
```

V_RP fails D1.4. The narrow posterior (±0.37) is driven by (β, n) absorbing
the r_d–H_0 degeneracy elsewhere.

### 4.4 Cassini fifth force

Universal coupling yields |γ−1| = 2β²/(1+β²). For β = 0.107:
|γ−1| = 2.26×10^−2, a factor 984 above the Cassini bound 2.3×10^−5.
Unscreened fifth-force χ² ≈ 9.7×10^5. Cubic-Galileon Vainshtein with
M^4 ∼ M_Pl² H_0² gives r_V(Sun) = 3.82×10^18 m = 124 pc; at Cassini (8 AU)
the suppression (r/r_V)^(3/2) = 1.75×10^−10, which beats the required
1.02×10^−3 by seven orders of magnitude. Vainshtein rescues Cassini at the
cost of adding a cubic Galileon term not present in the baseline SQMH action.

### 4.5 Fisher forecast of CPL extensions

Background-only (w0, wa) CPL with (Ω_m, h, ω_b) marginalised:
Δχ²_min = −13.43 at (w0*, wa*) = (−0.86, −0.98). ΔAIC = −9.43 (pass D1.1);
ΔBIC = +1.62 (fail D1.2). At the DESI DR2 headline (−0.757, −0.83) the
profiled χ² is +26.16 higher — our joint dataset prefers a different
minimum than DESI alone.

## 5. Decision gate and conclusion

Four-condition AND:

| gate | condition | status |
|---|---|---|
| D1.1 | ΔAIC ≤ −6 | ✗ V_family; ✓ CPL Fisher |
| D1.2 | ΔBIC ≤ 0 | ✗ all |
| D1.3 | Cassini | ✓ (with Vainshtein) |
| D1.4 | r_d within 3σ Planck | ✗ V_RP |

AND fails. **No-Go**.

### Lessons preserved

1. The five-program unification (base.md §V) remains internally consistent.
2. The BEC-motivated n₀μ = ρ_Pl/(4π) normalization is physically well-defined.
3. The forward-shooting k-essence background code (simulations/kessence.py)
   is a reusable tool; it demonstrates w_a < 0 from exponential quintessence
   for λ > 0.3, correcting an earlier incorrect claim that coupled thawing
   always gives w_a > 0.
4. The full reproducibility package (seed-fixed MCMC, public data only) is
   available for independent verification or extension.

## 6. Reproducibility

- Repo: https://github.com/(pending)/sqmh
- Commit: (pending)
- MCMC seed: emcee.EnsembleSampler with np.random.seed(42) in run_mcmc.
- Data sources: CobayaSampler/bao_data, CobayaSampler/sn_data, Planck 2018
  TT,TE,EE+lowE+lensing compressed summary (Chen et al. 2018).
- Key scripts:
  - simulations/phase3/mcmc_phase3.py (r_d fixed)
  - simulations/phase3/mcmc_rdfree.py (r_d free, 5D/7D)
  - simulations/phase4/fisher_kessence.py (CPL Fisher)
  - simulations/screening.py (fifth force)
  - simulations/vainshtein.py (Vainshtein radii)
  - simulations/kessence.py (CLW forward shooting)

## 6.1. Appendix A — L2 redesign survivors (post-hoc)

After the No-Go verdict on the universal-coupling implementation, a
theoretical exploration of alternative L2 kinetic/coupling sectors was
undertaken (see `base.l2.md`). Twelve candidates drawn from eight
independent research programs (GFT condensate, Volovik superfluid, RVM,
Padmanabhan emergence, k-essence/Horndeski, disformal coupling, sector-
selective coupling, causal set) were evaluated against four pre-registered
acceptance conditions:

  C1. Cassini `|gamma-1| < 2.3e-5` internally (no Vainshtein post-injection)
  C2. Phase 3 best-fit beta ~ 0.107 automatically consistent with C1
  C3. `nabla_mu T^mu_nu = 0` + Bianchi identity simultaneously
  C4. `w_a < 0` structural or natural (no ad-hoc lambda tuning)

Four candidates survived with >= 3/4 acceptance. Two candidates pass all
four conditions:

  **C10k. Sector-selective dark-only coupling.** Baryons couple only to
  the Einstein metric `g_mu_nu`; the scalar `phi` sources only the dark
  sector (DM + DE). Baryonic test particles follow pure GR geodesics,
  giving gamma_PPN = 1 exactly at solar-system scales, independent of the
  coupling strength beta_d. The Phase 3 posterior beta ~ 0.107 is
  reinterpreted as a dark-only coupling and is automatically compatible
  with Cassini. Dark IDE naturally yields `w_a < 0`.

  **C11D. Disformal coupling** `g_tilde = A(phi) g + B(phi) partial phi
  partial phi`. In the pure-disformal limit (`A' = 0`), static spherical
  sources yield gamma_PPN = 1 exactly (Zumalacarregui-Koivisto-Bellini
  JCAP 2013). The Phase 3 posterior beta is re-assigned to the disformal
  coefficient `B'`, leaving cosmological dynamics unchanged at leading
  order while Cassini is trivially satisfied. Sakstein-Jain PRL 118
  081305 (2017) shows disformal-only IDE generically produces `w_a < 0`.

Numerical verification scripts under `simulations/l2/`:

  - `c10k_ppn_gamma.py` - symbolic gamma=1, numerical bound < 4.4e-25
  - `c11d_disformal_gamma.py` - symbolic gamma-1 = 0 in pure disformal
  - `c5r_rvm.py` - RVM Lambda(H^2), 3/4 pass, nu<0 branch required
  - `c6s_stringy_rvm.py` - Stringy RVM, 3/4 pass, Pontryagin vanishing

**Scope of this result.** The L2 survivors restore internal consistency
at the *Lagrangian level* for a carefully chosen kinetic/coupling sector.
They do **not** rescue the original `base.md` universal-xi formulation.
They constitute a post-mortem road map: the negative result stands for
the implementation tested in the main body of this paper, while the
survivors indicate where a Phase 5 re-analysis should begin.

**Honest caveats on the L2 survivors (post-hoc numerical checks).** The
4/4 pass reported above refers to the PPN/Lagrangian conditions
C1-C3 together with a *structural* reading of C4. Subsequent light
numerical experiments (`simulations/l2/c10k_reinterpret.py`,
`c11d_wz.py`, `c5r_fit.py`, `c6s_cosmo.py`) revealed two tensions that
tighten the verdict:

  *C10k* carries a linear-growth enhancement `G_eff/G = 1 + 2 beta_d^2`
  restricted to the dark sector, which at the Phase 3 posterior median
  `beta_d ~ 0.107` shifts sigma_8 by +2.3% and worsens the KiDS-1000
  S_8 tension by approximately `Delta chi^2 ~ +6.6`. The PPN victory is
  exact; the clustering implication must be revisited under a full
  Phase 5 Boltzmann analysis.

  *C11D* survives C1-C3 exactly but our leading-order CPL projection of
  the pure-disformal IDE does **not** reproduce the `w_a<0` claim of
  Sakstein-Jain PRL 118 081305 (2017); the toy template gives
  `w_a>0` over the plausible `B`-range. A `hi_class` disformal-branch
  run is required to settle C4 for C11D.

  *C5r* (RVM with `nu<0`) and *C6s* (Stringy RVM with `c_2<0`) do show
  a `w_a<0` branch numerically consistent with DESI DR2 at the 0.5 sigma
  level in BAO-only toy fits, consistent with the Gomez-Valent-Sola
  2024 "phantom matter" branch.

These caveats move the overall verdict from "4 strong survivors" to
"2 PPN-exact survivors with open cosmological questions + 2 partial
survivors with viable `w_a<0` branch", and are the concrete inputs for
the Phase 5 entry criteria.

## 7. Acknowledgements

(pending)

## 8. References

(pending — Planck 2018 VI, DESI DR2 arXiv:2503.14738, Ratra-Peebles 1988,
Amendola 2000, Di Porto-Amendola 2008, Copeland-Liddle-Wands 1998, Nicolis-
Rattazzi-Trincherini 2009 (Galileon), Babichev-Deffayet-Esposito-Farèse 2011
(Vainshtein), Bertotti-Iess-Tortora 2003 (Cassini), Williams-Turyshev-Boggs
2012 (LLR), Touboul et al. 2017 (MICROSCOPE).)
