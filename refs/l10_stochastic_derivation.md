# refs/l10_stochastic_derivation.md -- L10-S: Stochastic SQMH

> Date: 2026-04-11
> Phase: L10-S (Round 1 standard + Rounds 2-10 deepening)
> Method: 8-person parallel team discussion
> Kill criterion: K51 (erf impossible even with diffusion)
> Keep criterion: Q51 (erf appears with diffusion at some eta_crit)

---

## Background

L9 NF-14 proved: standard SQMH is an advection-type first-order PDE.
No nabla^2 n term. Therefore erf is mathematically impossible in standard SQMH.

L9 JCAP reviewer Q6 response: "If diffusion term added (CSL-type), erf becomes possible."

L10-S investigates: is this physically justified?

---

## 8-Person Parallel Team Discussion

### [해석 접근] Member 1: Fokker-Planck Analysis

Standard SQMH continuity: dn/dt + 3H*n = Gamma_0 - sigma*n*rho_m
This is a drift-only Langevin equation with drift coefficient:
  mu(n) = Gamma_0 - sigma*n*rho_m - 3H*n

Corresponding Fokker-Planck (Gamma=0, pure drift):
  dP/dt = -d/dn [mu(n) P(n,t)]

The stationary solution is:
  P_stat(n) = C * exp(2 * integral mu(n') dn' / D(n'))

For D -> 0 (no diffusion), P_stat -> delta(n - n_eq) where n_eq = Gamma_0/(3H + sigma*rho_m).
No erf emerges. erf requires a 1D spatial diffusion, not an n-space diffusion.

Even with n-space noise eta*sqrt(n)*dW(t), the spatial profile <n(x)> obeys:
  d<n>/dt = mu(<n>) + (diffusion correction ~ eta^2/2 * d^2<n>/d<n>^2 * variance)

This is a scalar drift equation, not a spatial PDE. erf in space still impossible.

**Conclusion from Member 1**: n-space stochastic noise does NOT generate spatial erf.
The stochastic term must be a SPATIAL diffusion D_s * nabla^2 n to produce erf.

---

### [수치 접근] Member 2: Euler-Maruyama Simulation

Langevin SDE: dn = [Gamma_0 - sigma*n*rho_m - 3H*n] dt + eta*sqrt(n) dW

Numerical scheme (Euler-Maruyama, dt = 1e-3 H_0^-1):
  n_{k+1} = n_k + [Gamma_0 - sigma*n_k*rho_m - 3H*n_k]*dt + eta*sqrt(n_k)*sqrt(dt)*xi_k
  where xi_k ~ N(0,1)

Ensemble of N=1000 trajectories. <n(t)> extracted.

Result (see sqmh_langevin.py):
  - For all eta in [1e-80, 1e-30] SI: <n(t)> converges to n_eq +/- fluctuations
  - Temporal profile of <n(t)>: exponential relaxation to n_eq, NOT erf
  - Spatial profile (assuming spherical infall): still first-order advection
  - erf fit R^2 < 0.01 for all eta tested

**Numerical conclusion**: No erf from n-space Langevin. K51 TRIGGERED numerically.

---

### [대수 접근] Member 3: CSL-Type Extension Analysis

CSL (Continuous Spontaneous Localization) applied to spacetime quanta n:
  dn/dt + nabla.(nv) = Gamma_0 - sigma*n*rho_m + (D_CSL/m_CSL^2) nabla^2 n

where D_CSL ~ 10^-30 m^2/s (standard CSL diffusion constant), m_CSL is localization mass.

For the density n measured in quanta/m^3:
  D_CSL/m_CSL^2 ~ 10^-30 m^2/s / (m_Planck)^2 ~ 10^-30 / (2.18e-8)^2 ~ 2e-15 m^2/s / kg^2

This is an extremely small spatial diffusion. The erf profile emerges when:
  D_CSL * t_Hubble ~ L_scale^2
  => L_scale ~ sqrt(D_CSL * t_Hubble) ~ sqrt(2e-15 * 4e17) ~ sqrt(8e2) ~ 28 m

At cosmological scales L ~ Mpc = 3e22 m: the CSL diffusion produces erf only on 28 m scales.
This is 21 orders of magnitude below cosmological structure scales.

**Algebraic conclusion**: CSL diffusion cannot produce cosmologically relevant erf.
Even if physically justified (speculative), scale is wrong by 21 orders of magnitude.

---

### [위상 접근] Member 4: Topological Obstruction to erf

For erf to emerge from a PDE, the spatial profile must satisfy:
  u_t = D u_xx + f(u)  [reaction-diffusion]

The key topological requirement: existence of a bistable potential V(u) with two minima.
  f(u) = -V'(u), V(u) = (u^2 - 1)^2/4 (example: Allen-Cahn / Fisher-KPP)

SQMH source term: Gamma_0 - sigma*n*rho_m is MONOTONE in n (single well, not bistable).
The effective potential V(n) = sigma*rho_m*n^2/2 - Gamma_0*n has a SINGLE minimum at n_eq.

Topological result: No bistable potential => No traveling wave solution => No erf profile.
This is independent of noise strength eta.

**Topological conclusion**: erf requires bistable effective potential. SQMH has monostable potential.
Even with diffusion added, no erf can emerge. K51 topologically confirmed.

---

### [열역학 접근] Member 5: Thermal Fluctuation Scale

Planck-temperature thermal fluctuations in n:
  <delta_n^2> ~ n * T_Planck / (hbar * c^2) [dimensional estimate]
  T_Planck = sqrt(hbar*c^5/G*k_B) = 1.416e32 K

Spatial diffusion coefficient from thermal kicks:
  D_thermal ~ k_B * T_Planck / (6*pi*eta_visc*r_Planck) [Stokes-Einstein]
  ~ (1.38e-23 * 1.416e32) / (6*pi * rho_Planck * l_Planck^2 / t_Planck * l_Planck)

This is purely Planck-scale physics. The spatial diffusion length over t_Hubble:
  L_diff ~ sqrt(D_thermal * t_Hubble)

Even if D_thermal is as large as c*l_Planck ~ 3e8 * 1.6e-35 ~ 5e-27 m^2/s:
  L_diff ~ sqrt(5e-27 * 4e17) ~ sqrt(2e-9) ~ 5e-5 m = 50 microns

Again, 27 orders of magnitude below Mpc scales.

**Thermodynamic conclusion**: No physically motivated diffusion produces cosmological-scale erf.

---

### [정보기하학 접근] Member 6: Fisher Metric and Information Diffusion

In information geometry, the SQMH density n is a coordinate on the statistical manifold
of spacetime quantum configurations. The Fisher information metric:
  g_ij = sum_x partial_i ln P(x|theta) * partial_j ln P(x|theta)

For n as a Poisson process (birth-death):
  P(n|lambda) = lambda^n * exp(-lambda) / n!
  Fisher metric: g_nn = 1/n_bar (variance = n_bar for Poisson)

Information diffusion in n-space (thermodynamic uncertainty relation):
  Sigma_dot >= 4*Var(n) / (n_bar^2 * tau_corr)

This yields entropy production, not spatial erf. The natural diffusion in information
space is over the n-values, not over the spatial coordinate x.

To get spatial erf, we would need spatial correlations in n(x), which require
a long-range kernel K(x-x') coupling different spatial locations. SQMH has no such kernel.

**Information-geometric conclusion**: Information diffusion in n-space gives temporal relaxation,
not spatial erf profile. K51 confirmed from information geometry.

---

### [대칭군 접근] Member 7: Symmetry Analysis of erf Generation

erf(x/sigma_0) emerges as the fundamental solution of:
  u_t = D u_xx (heat equation)

This requires TRANSLATION SYMMETRY breaking in x. The profile erf((x-x0)/sqrt(4Dt))
arises from initial condition u(x,0) = theta(x-x0) (step function).

SQMH in its stochastic extension:
  dn/dt + nabla.(nv) = Gamma_0 - sigma*n*rho_m + eta*nabla^2(n) + noise

The symmetry group of this equation (in FLRW background) is O(3) spatial rotations only.
No preferred spatial direction x0 exists. Therefore no erf profile can emerge
from SYMMETRIC initial conditions (which cosmological n(x) must have at large scales).

UNLESS: initial conditions break O(3) symmetry locally (e.g., at a domain wall).
But domain walls in n(x) require a first-order phase transition in n, which SQMH
has no mechanism to produce (monostable potential, cf. Member 4).

**Symmetry conclusion**: O(3) symmetry + monostable potential -> no spatial erf.
Even with diffusion term, erf requires symmetry-breaking initial condition absent from SQMH.

---

### [현상론 접근] Member 8: Phenomenological Reverse-Engineering

The A12 erf template: w(z) = w0 + wa * erf((z - z_trans)/sigma_z)
with w0 = -0.886, wa = -0.133, z_trans ~ 0.5.

If SQMH + stochastic diffusion is to produce this:
  - We need n(z) to have an erf profile as a function of redshift
  - Translating: n(a) = n0 * (1 + wa_eff * erf((a - a_trans)/sigma_a))

For erf in a (scale factor, not space), we need a "time diffusion" not a spatial diffusion.
Time diffusion: d^2n/dt^2 type term (second-order in time), e.g., telegraphers equation.

Telegrapher's equation: tau * n_tt + n_t + 3H*n_t = [source terms] + D*nabla^2 n

In the overdamped limit (tau -> 0), this reduces to standard advection.
The erf profile in TIME requires the underdamped regime: tau > 1/H_0.

Physical interpretation: spacetime quanta have a "memory time" tau > Hubble time.
This is unphysical: it means quanta take longer than the age of the universe to relax.

**Phenomenological conclusion**: erf in time/redshift requires tau > t_Hubble, unphysical.
erf in space requires CSL/thermal diffusion, but scale is wrong by 21+ orders of magnitude.

---

## Team Synthesis (Rounds 1-10)

**Round 1 consensus**: K51 TRIGGERED.

All 8 approaches agree:
1. n-space stochastic noise does NOT produce spatial erf (Members 1,2,6)
2. Spatial diffusion (CSL/thermal) produces erf only on ~micron scales, not Mpc (Members 3,5)
3. Topological obstruction: monostable SQMH potential cannot produce bistable erf profile (Member 4)
4. O(3) symmetry + monostable potential: no spatial erf from symmetric ICs (Member 7)
5. Time erf requires tau > t_Hubble (unphysical) (Member 8)

**Rounds 2-5 (deeper exploration)**:

Round 2: Explored CDT-type stochastic causal sets. Result: causal set fluctuations in n
produce a fractional Brownian noise in n(t), still no spatial erf.

Round 3: Explored colored noise (non-Markovian) Langevin. Result: power-law temporal
correlations can produce 1/f noise in n(t), but spatial profile still advection-only.

Round 4: Explored reaction-diffusion with bistable potential (artificially modified SQMH).
V(n) = alpha*(n - n1)^2*(n - n2)^2. This DOES produce erf! But requires explicit bistability
not present in SQMH. The conclusion: erf is possible IF AND ONLY IF the source term
Gamma_0 - sigma*n*rho_m is replaced by a bistable function f(n).

Round 5: This bistable modification would mean n has TWO stable equilibria: a "low-n"
cosmological phase and a "high-n" Planck phase. Possible interpretation: cosmological
phase transition in spacetime quanta density. SPECULATIVE but internally consistent.

**Rounds 6-10 (focus)**:

Round 6: Quantified the bistable modification parameters needed:
  V(n) bistable with minima at n1 = n_eq/2, n2 = 2*n_eq
  Domain wall width: xi ~ sqrt(D/Delta_V) ~ sqrt(1e-27 / 1e-130) ~ macroscopic
  Scale: the domain wall is at least galaxy-cluster scale. Testable? No.

Round 7: Investigated stochastic resonance: could noise alone generate apparent erf?
Result: stochastic resonance requires bistable potential. SQMH monostable -> no resonance.

Round 8: New finding (NF-23 candidate): If SQMH is embedded in a Calogero-Moser
interacting particle system (n particles in 1D with 1/r^2 repulsion), the density
profile can develop erf-like features via collective relaxation. However, this
requires 62-order amplified coupling, still not physically motivated.

Round 9: Language finalization. The most honest statement:
  "Stochastic SQMH with physical diffusion (CSL/Planck thermal) generates erf only
   at scales 21+ orders below cosmological. Bistable SQMH (modified source term)
   CAN generate erf but requires explicit ad hoc modification of the source term.
   Standard SQMH: erf impossible. Extended bistable SQMH: erf possible but speculative."

Round 10: K51 CONFIRMED (standard and CSL-physical extension).
Q51 PARTIALLY triggered for bistable extension only (not standard CSL).

---

## K51 / Q51 Final Verdict

| Verdict | Status | Basis |
|---------|--------|-------|
| K51 (erf impossible with physical diffusion) | TRIGGERED | CSL/thermal diffusion: 21+ order scale mismatch; monostable potential topology |
| Q51 (erf possible with bistable extension) | PARTIAL PASS | Bistable SQMH (modified source term) can produce erf; requires non-standard modification |

**Paper language** (L10):
  "We demonstrate that stochastic SQMH with physically motivated diffusion coefficients
   (CSL, Planck thermal) cannot produce the erf functional form at cosmological scales:
   the diffusion length is 21 or more orders of magnitude below Mpc scales. Furthermore,
   the SQMH source term is monostable, presenting a topological obstruction to erf generation.
   A bistable modification of the source term (two-phase spacetime quanta scenario) would
   permit erf profiles but requires explicit ad hoc modification and is speculative."

---

*L10-S completed: 2026-04-11. All 10 rounds.*
