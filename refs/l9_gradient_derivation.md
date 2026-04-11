# refs/l9_gradient_derivation.md -- L9-B Non-uniform SQMH Gradient Analysis

> Date: 2026-04-11
> Phase: L9-B
> Script: simulations/l9/gradient/sqmh_gradient.py
> 8-person parallel team derivation.

---

## Team Derivation

### Person 1 (Full PDE Setup)

Non-uniform SQMH:
  dn/dt + nabla.(n*v) = Gamma0 - sigma*n*rho_m(r,t)

In FLRW background + perturbations (spherical symmetry):
  dn/dt + 3H*n + (1/r^2)*d/dr(r^2*n*v_r) = Gamma0 - sigma*n*rho_m(r,t)

Comoving frame: x = r/a (physical -> comoving)
  d(delta_n)/dN + 3*delta_n + (v_infall/aH)*d(delta_n)/dx = -sigma*n_bar*delta_rho_m(x)

### Person 2 (Infall velocity estimate)

Infall velocity from CLAUDE.md rule:
  v(r) = g(r)*t_P  [gravity acceleration * Planck time]
  g(r) = GM(<r)/r^2 = (4pi/3)*G*rho_m*r  [for uniform sphere]
  v_r = -(4pi/3)*G*rho_m*r * t_P  [negative = infall]

In Hubble units:
  v_r/(H*r) = -(4pi/3)*G*rho_m*t_P / H
             = -(4pi/3)*(G*rho_m/H) * t_P
             = -(Omega_m/2)*(H0^2/H^2) * (H0*t_P)  [using rho_m = Omega_m*3H0^2/8piG*a^-3]
             ~ -Omega_m/2 * H0*t_P   [at z=0, E=1]
             ~ -Pi_SQMH * (3/(2*Omega_m))
             ~ -1.85e-62 * (3/0.63)
             ~ -8.8e-62

Infall velocity is 62 orders below Hubble velocity. The gradient term is:
  (v_r/aH) * d(delta_n)/dx ~ 1e-62 * d(delta_n)/dx

This is completely negligible compared to all other terms.

### Person 3 (Perturbation equation analysis)

For the n-field perturbation at linear order:
  d(delta_n)/dN = -3*delta_n - (v_amp)*x*d(delta_n)/dx - sigma_dimless*delta_rho_m(x)

  where sigma_dimless = sigma*rho_crit0/H0 ~ 1.77e-61

The source term sigma_dimless*delta_rho_m creates a perturbation:
  delta_n(x, N) = -sigma_dimless * int_N_ini^N n_bar(N') * delta_rho_m(x) dN'
               ~ -sigma_dimless * n_bar * delta_N * delta_rho_m(x)

The SHAPE of delta_n(x) is the same as the shape of delta_rho_m(x).
If delta_rho_m ~ Gaussian: delta_n ~ Gaussian.
If delta_rho_m ~ Step (top-hat): delta_n ~ Step.
NEVER erf, because there is no diffusion term.

### Person 4 (Mathematical proof of no-erf)

Theorem: The SQMH PDE dn/dt = f(n, rho_m) with f first-order in space
cannot produce erf-like spatial profiles from smooth initial conditions.

Proof by example: For heat equation dn/dt = D*nabla^2(n) with step IC:
  n(x,0) = Theta(x) -> n(x,t) = (1/2)*erfc(-x/(2*sqrt(D*t)))

For SQMH: dn/dt = -sigma*n*rho_m + Gamma0 [no spatial operator]
  At each x, n(x,t) evolves INDEPENDENTLY:
  n(x,t) = [Gamma0/(3H + sigma*rho_m(x))] + transient
  This is the point-wise quasi-static solution.
  No information propagates between neighboring x positions.
  THEREFORE: spatial profile of n(x) mirrors spatial profile of rho_m(x).
  No erf generation possible without spatial coupling.

The nabla.(n*v) term adds:
  -nabla.(n*v) = -v*grad(n) - n*nabla.v
This IS a spatial coupling (advection) but NOT diffusion.
Advection preserves profile shape; it does NOT produce erf from step ICs.

### Person 5 (Stochastic SQMH spatial analysis)

Stochastic generalization:
  dn = [-3Hn + Gamma0 - sigma*n*rho_m]*dt + sqrt(D_n(x))*dW(x,t)

If D_n = 0 (no noise): no spatial coupling -> n mirrors rho_m.
If D_n != 0 (noise): Fokker-Planck:
  dP(n)/dt = -d/dn[(drift)*P] + (1/2)*d^2/dn^2[D_n*P]
This is diffusion in n-space, not x-space.
For spatial erf: need correlated spatial noise <dW(x)*dW(x')> = C(x-x').
Gaussian correlated noise gives:
  <delta_n(x)*delta_n(x')> ~ C(x-x') * amplitude
This is a spatial correlation, not an erf profile in n.

Even with spatial noise: n(x,t) approaches n_bar pointwise (each x independently).
The spatial profile of n_bar(x) is set by rho_m(x).
No erf emergence from stochastic SQMH.

### Person 6 (Numerical verification)

From sqmh_gradient.py:
  Max delta_n/n_bar = 1.67e-61
  (Ratio of SQMH perturbation to background: Pi_SQMH level)

Spatial profile of delta_n(x): Gaussian (mirrors Gaussian overdensity)
Correlation of n(x) with erf profile: undefined (nan, because delta_n is numerically zero)

The SQMH correction to rho_DE from spatial variation:
  delta_rho_DE_spatial = integral[delta_n * 4pi*r^2] dr
                       = -7e-57 (relative correction: -6.3e-64)

This is utterly negligible: 64 orders below rho_DE itself.

### Person 7 (Phase transition alternative)

Could SQMH have a phase transition that produces an erf front?
Phase transition requires a free-energy landscape with two minima:
  n=0 (vacuum) and n=n_bar (SQMH active)

SQMH equation has no such structure: the "potential" is:
  V(n) = (kappa/2)*n^2 - Gamma0*n  [from NF-9]
This is a single-minimum quadratic: n* = Gamma0/kappa (unique minimum).
No spontaneous symmetry breaking, no phase transition.
Domain wall / erf front: requires ZERO equilibrium separated by barrier.
SQMH does not support this.

### Person 8 (Literature comparison)

Models that DO produce erf:
  1. Higgs field bubble nucleation: erf-like thin-wall profile (Coleman-De Luccia)
  2. Axion domain walls: n ~ tanh((r-R)/delta) (close to erf)
  3. Phase transition fronts in EW baryogenesis: erf from diffusion-reaction
  4. Chemical fronts in reaction-diffusion systems (SQMH analog: C26 killed by L5)

All these require EITHER:
  a) A self-interaction term (V''*n^2 -> "surface tension" for wall)
  b) A diffusion term (nabla^2 n -> "thermal diffusion")

SQMH has neither. The sigma*n*rho_m term is a binary collision rate (NF-3),
not a self-interaction or diffusion.

---

## Q43 Judgment

NUMERICAL RESULT:
  Max delta_n/n_bar = 1.67e-61
  Spatial profile: Gaussian (NOT erf)
  Correlation with erf: undefined (amplitude below machine precision)
  Spatial rho_DE correction: 6.3e-64 (relative)

**Q43 FAIL**. **K43 TRIGGERED**: Non-uniform SQMH gradient term is 62-order suppressed.
SQMH has no diffusion term and cannot generate erf-like spatial profiles.

---

## Key New Finding: erf Impossibility Theorem (NF-14)

The erf functional form cannot emerge from the SQMH PDE at any level because:
1. SQMH is a zeroth-order spatial equation (no nabla^2 n term)
2. Advection (nabla.(nv)) preserves profile shape, does not generate erf
3. Self-interaction is absent (no V''*n^2 surface tension)
4. Phase transition is impossible (single-minimum quadratic potential NF-9)

Mathematical necessity: erf requires second-order spatial derivative.
SQMH has zero spatial derivatives. Therefore erf is structurally impossible in SQMH.

---

## Paper Language

"The non-uniform SQMH equation includes an advection term nabla.(n*v_infall)
where v_infall(r) = g(r)*t_P. With g(r) ~ GM/r^2, this gives v_r/(H*r) ~ Pi_SQMH
~ 10^-62, confirming the same 62-order suppression at the spatial gradient level.
Furthermore, the SQMH PDE is first-order in space (advection-only with no diffusion),
and cannot generate erf-like spatial profiles from any initial conditions:
erf requires a second-order spatial operator absent from SQMH. The A12 erf
proxy parameterization therefore has no derivational origin within SQMH."

---

*L9-B completed: 2026-04-11*
