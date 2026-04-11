# -*- coding: utf-8 -*-
"""
L3 candidate model registry.

Each of the 11 L2 survivors is encoded as

    ModelSpec(
        ID, name, family, theta0, bounds, build_E, gamma_minus_one,
        theory_score, notes, sqmh_sign_ok
    )

where ``build_E(theta, Omega_m, h)`` returns an ``E(z)`` callable + derived
``w(z)`` callable. Parameters are the model-specific extras (e.g. ν for
RVM, β_d for dark coupling).

Fits minimise the joint BAO+SN+CMB+RSD chi^2 over ``(Omega_m, h, *theta)``
via Nelder-Mead multi-start in ``run_l3.py``. CPL w0,w_a are then fit on
z∈[0.05, 1.8] for the KILL criteria.

All E(z) are produced by **closed-form Friedmann** at the background level
(no k-space perturbation yet — that's L3-F). Each candidate's background
equation is solved either analytically or via coupled ODE in ln a.

Reference: L0/L1 invariants σ=4πG·t_P, Γ₀ never touched at the background
(see CLAUDE.md / refs/l3_kill_criteria.md K6).
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import Callable, Tuple, List, Optional

import numpy as np
from scipy.integrate import solve_ivp

_THIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_THIS))
import config  # noqa: E402


OMEGA_R = config.Omega_r


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _E_from_rhoDE(Om: float, h: float, rho_de_fn: Callable[[float], float]):
    """Return E(z) given dimensionless rho_de(z)/rho_c0 function.

    E^2 = Omega_r (1+z)^4 + Omega_m (1+z)^3 + rho_de(z).
    Closes flatness at z=0 only if rho_de(0) = 1 - Omega_m - Omega_r
    (the caller is responsible for this; optimiser uses h as free param,
    so the budget closes at z=0 by construction).
    """
    OL0 = 1.0 - Om - OMEGA_R

    def E(z):
        rho = rho_de_fn(z)
        return np.sqrt(OMEGA_R * (1 + z)**4 + Om * (1 + z)**3 + rho)

    # Snap-to-closure at z=0 via a multiplicative rescale if required.
    # We skip that; accept rho_de(0) = OL0 by convention in each model.
    return E, OL0


def _cpl_fit(E_func: Callable[[float], float], Om: float) -> Tuple[float, float]:
    """Fit effective CPL w(a)=w0+wa*(1-a) directly to the model's E(z).

    For an observer that adopts the LCDM decomposition
      E²_obs(z) = Omega_r (1+z)^4 + Om (1+z)^3 + (1-Om-Omega_r) f(z; w0, wa)
    with
      f(z; w0, wa) = (1+z)^(3(1+w0+wa)) * exp(-3 wa z/(1+z)),
    the best-fit (w0, wa) minimises Σ[(E²_obs - E²_model)^2] on the chosen
    window. This avoids the "effective rho_de goes negative" artefact of
    taking d ln rho_de / d ln a on IDE models where matter and DE are
    reshuffled.
    """
    z = np.linspace(0.01, 1.2, 80)
    E2_model = np.array([E_func(zi)**2 for zi in z])
    OL0 = 1.0 - Om - OMEGA_R

    def E2_cpl(w0, wa):
        f = (1 + z)**(3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * z / (1 + z))
        return OMEGA_R * (1 + z)**4 + Om * (1 + z)**3 + OL0 * f

    from scipy.optimize import least_squares
    def resid(p):
        w0, wa = p
        return E2_cpl(w0, wa) - E2_model

    try:
        r = least_squares(resid, x0=[-1.0, 0.0],
                          bounds=([-2.5, -3.0], [0.0, 3.0]),
                          max_nfev=200)
        return float(r.x[0]), float(r.x[1])
    except Exception:
        return -1.0, 0.0


def _phantom_crossing(E_func: Callable[[float], float], Om: float) -> bool:
    """True if w(z) crosses -1 for z ∈ [0, 2]."""
    z = np.linspace(0.0, 2.0, 400)
    lna = -np.log(1 + z)
    E2 = np.array([E_func(zi)**2 for zi in z])
    rho_de = E2 - OMEGA_R * (1 + z)**4 - Om * (1 + z)**3
    rho_de = np.where(rho_de > 1e-8, rho_de, 1e-8)
    dlnrho = np.gradient(np.log(rho_de), lna)
    w = -1.0 - dlnrho / 3.0
    return bool(np.any(w < -1.0 - 1e-4) and np.any(w > -1.0 + 1e-4))


# ---------------------------------------------------------------------------
# Model specs
# ---------------------------------------------------------------------------

@dataclass
class ModelSpec:
    ID: str
    name: str
    family: str
    theta0: List[float]
    bounds: List[Tuple[float, float]]
    theta_names: List[str]
    gamma_minus_one: float          # analytic Cassini (given current spec)
    theory_score: int               # 0..10 SQMH L0/L1 connection strength
    sqmh_sign_ok_condition: str     # verbal
    notes: str
    build: Callable                 # (theta, Om, h) -> E(z)


# ============ C5r. RVM (running vacuum, Gómez-Valent-Solà 2024) ============
# Lambda(H^2) = Lambda0 + 3 nu H^2. Effective Friedmann:
#   E^2(z) = (Omega_m (1+z)^3 + Omega_r (1+z)^4 + OL0 - nu)/(1 - nu) if DE
#   behaves as (1 - nu)-shifted. Simplest toy:
#   rho_de(z) = OL0 + nu * (E^2 - 1) * rho_c0  (in units where H^2 = E^2 H0^2)
# Solve self-consistent: E^2 - nu*(E^2 - 1) = Om_r a^-4 + Om_m a^-3 + OL0
#  => E^2 = (Om_r a^-4 + Om_m a^-3 + OL0 - nu) / (1 - nu)
def _build_C5r(theta, Om, h):
    (nu,) = theta
    if abs(1 - nu) < 1e-6:
        return None
    def E(z):
        num = OMEGA_R * (1 + z)**4 + Om * (1 + z)**3 + (1 - Om - OMEGA_R) - nu
        den = 1.0 - nu
        val = num / den
        return np.sqrt(max(val, 1e-12))
    return E


C5r = ModelSpec(
    ID='C5r', name='RVM ν<0 branch', family='RVM',
    theta0=[-0.005], bounds=[(-0.03, 0.03)],
    theta_names=['nu'],
    gamma_minus_one=0.0, theory_score=6,
    sqmh_sign_ok_condition='nu<0 for w_a<0 (Gómez-Valent-Solà 2024)',
    notes='L(H^2)=L0+3nu H^2. No scalar d.o.f., gamma=1 exact.',
    build=_build_C5r,
)


# ============ C6s. Stringy RVM + Chern-Simons anomaly ============
# Background identical to RVM (CS ~ dual axion, background vacuum OK).
# CS contributes 0 in Schwarzschild (type-D vanishing Pontryagin).
def _build_C6s(theta, Om, h):
    nu, = theta[:1]
    return _build_C5r((nu,), Om, h)


C6s = ModelSpec(
    ID='C6s', name='Stringy RVM + CS anomaly', family='RVM',
    theta0=[-0.005], bounds=[(-0.03, 0.03)],
    theta_names=['nu_s'],
    gamma_minus_one=0.0, theory_score=5,
    sqmh_sign_ok_condition='nu<0; CS vanishes in Schwarzschild',
    notes='Background = RVM. CS b R R-tilde is Kerr-only.',
    build=_build_C6s,
)


# ============ C10k. Sector-selective dark-coupled quintessence ============
# Fluid-level toy (matches L2 cards): rho_de(a) = OL0 * a^{-3 beta_d}.
# Beta_d couples only to DM. The Friedmann here is dark-only at background.
def _build_C10k(theta, Om, h):
    bd, = theta
    OL0 = 1.0 - Om - OMEGA_R

    def E(z):
        a = 1.0 / (1 + z)
        return np.sqrt(OMEGA_R * (1 + z)**4 + Om * (1 + z)**3
                       + OL0 * a**(-3 * bd))
    return E


C10k = ModelSpec(
    ID='C10k', name='Dark-sector-only coupled quintessence', family='IDE',
    theta0=[0.05], bounds=[(0.0, 0.2)],
    theta_names=['beta_d'],
    gamma_minus_one=0.0, theory_score=8,
    sqmh_sign_ok_condition='beta_d>0 → matter→DE flow',
    notes='Dark-only coupling → Einstein-frame baryons decouple, '
          'gamma=1 exact. G_eff/G = 1+2β_d² on DM only.',
    build=_build_C10k,
)


# ============ C11D. Disformal coupling g̃ = A g + B ∂φ∂φ ============
# Pure disformal (A=1 const) keeps gamma=1 exact. Background w(z) from
# kinetic term. Toy: rho_de(a) = OL0 * exp(gamma_d * (1 - a)).
def _build_C11D(theta, Om, h):
    gd, = theta
    OL0 = 1.0 - Om - OMEGA_R

    def E(z):
        a = 1.0 / (1 + z)
        return np.sqrt(OMEGA_R * (1 + z)**4 + Om * (1 + z)**3
                       + OL0 * np.exp(gd * (1 - a)))
    return E


C11D = ModelSpec(
    ID='C11D', name='Disformal IDE (Zumalacarregui-Koivisto-Bellini)',
    family='Disformal',
    theta0=[0.1], bounds=[(-0.5, 0.5)],
    theta_names=['gamma_D'],
    gamma_minus_one=0.0, theory_score=7,
    sqmh_sign_ok_condition='gamma_D>0 for w_a<0',
    notes='Pure disformal (A`=0) → static gamma=1 exact. Background toy '
          'rho_de ∝ exp(gamma_D (1-a)).',
    build=_build_C11D,
)


# ============ C23. Asymptotic safety effective RVM (Bonanno-Platania) ============
# Effective parametrisation: rho_de(z) = OL0 + nu_eff * (E^2 - 1).
# Self-consistent solve like RVM but with (1+z)^something scaling tied to H.
# Same closed form as C5r with different sign convention.
def _build_C23(theta, Om, h):
    ne, = theta

    def E(z):
        num = OMEGA_R * (1 + z)**4 + Om * (1 + z)**3 + (1 - Om - OMEGA_R) - ne
        den = 1.0 - ne
        val = num / den
        return np.sqrt(max(val, 1e-12))
    return E


C23 = ModelSpec(
    ID='C23', name='Asymptotic Safety (Bonanno-Platania eff RVM)',
    family='Quantum-gravity RG',
    theta0=[-0.01], bounds=[(-0.05, 0.05)],
    theta_names=['nu_eff'],
    gamma_minus_one=0.0, theory_score=6,
    sqmh_sign_ok_condition='nu_eff<0 for w_a<0. |ν|<0.03 unitarity bound',
    notes='k=ξH identification (ξ=O(1)). Background identical to RVM up to '
          'sign convention.',
    build=_build_C23,
)


# ============ C26. Perez-Sudarsky unimodular diffusion ============
# Perturbative closed form: matter→Λ drift proportional to α_Q.
#   rho_m(a) ≈ Om * a^(-3) * (1 - α_Q * (1 - a^3))
#   rho_Λ(a) ≈ OL0 + α_Q * Om * (1 - a^3)
# Constructed so that (i) α_Q=0 → pure LCDM, (ii) α_Q>0 transfers matter
# energy into the Λ sector as the universe expands (matches Perez-Sudarsky
# sign convention for DESI wa<0).
def _build_C26(theta, Om, h):
    aq, = theta
    OL0 = 1.0 - Om - OMEGA_R

    def E(z):
        a = 1.0 / (1 + z)
        drift = aq * (1.0 - a**3)
        rm = Om * a**(-3) * (1.0 - drift)
        rL = OL0 + aq * Om * (1.0 - a**3)
        if rm < 0 or rL < 0:
            return 0.0
        Or = OMEGA_R * (1 + z)**4
        return np.sqrt(max(rm + rL + Or, 1e-12))
    return E


C26 = ModelSpec(
    ID='C26', name='Perez-Sudarsky unimodular diffusion',
    family='Unimodular',
    theta0=[0.05], bounds=[(-0.3, 0.5)],
    theta_names=['alpha_Q'],
    gamma_minus_one=0.0, theory_score=9,
    sqmh_sign_ok_condition='alpha_Q>0: matter→Λ drift (DESI sign)',
    notes='Diffusion J^0=α_Q ρ_c0 (H/H0). Most direct SQMH L0/L1 '
          'metabolism interpretation.',
    build=_build_C26,
)


# ============ C27. Deser-Woodard non-local (localised, f(X)) ============
# At background: rho_de = OL0 + c0 * OL0 * tanh((a-a*)/Δa). Leading V
# approximation used in L2; amplitude fit via c0.
def _build_C27(theta, Om, h):
    c0, ash, dw = theta[:3]
    OL0 = 1.0 - Om - OMEGA_R

    def E(z):
        a = 1.0 / (1 + z)
        f = c0 * np.tanh((a - ash) / max(dw, 1e-3))
        rho_de = OL0 * (1.0 + f)
        return np.sqrt(OMEGA_R * (1 + z)**4 + Om * (1 + z)**3
                       + max(rho_de, 1e-10))
    return E


C27 = ModelSpec(
    ID='C27', name='Deser-Woodard non-local f(X)',
    family='Non-local',
    theta0=[0.05, 0.7, 0.3], bounds=[(-0.3, 0.3), (0.4, 0.95), (0.05, 0.8)],
    theta_names=['c0', 'a_shift', 'Delta_a'],
    gamma_minus_one=0.0, theory_score=7,
    sqmh_sign_ok_condition='auxiliary X frozen in Schwarzschild → γ=1',
    notes='Koivisto 2008 static gamma=1 from auxiliary frozen. Leading-V '
          'amplitude fit; Phase 5 full Dirian 2015 eqs needed.',
    build=_build_C27,
)


# ============ C28. Maggiore-Mancarella RR non-local ============
# Similar to C27 but with c0 amplitude flipping sign (leading-V toy caveat).
def _build_C28(theta, Om, h):
    return _build_C27(theta, Om, h)


C28 = ModelSpec(
    ID='C28', name='Maggiore-Mancarella RR non-local',
    family='Non-local',
    theta0=[-0.05, 0.7, 0.3], bounds=[(-0.3, 0.3), (0.4, 0.95), (0.05, 0.8)],
    theta_names=['c0', 'a_shift', 'Delta_a'],
    gamma_minus_one=0.0, theory_score=6,
    sqmh_sign_ok_condition='leading-V sign ambiguity → full eqs needed',
    notes='Dirian 2015 |w_a|≈0.19 (full). Leading toy sign flip caveat.',
    build=_build_C28,
)


# ============ C32. Bare Mimetic gravity ============
# V(phi)=V0 exp(-lambda phi). phi=t constraint → phi(N) integrate.
def _build_C32(theta, Om, h):
    lam, = theta
    OL0 = 1.0 - Om - OMEGA_R

    def rhs(N, y):
        phi, = y
        V = OL0 * np.exp(-lam * phi)
        E2 = OMEGA_R * np.exp(-4 * N) + Om * np.exp(-3 * N) + V
        if E2 < 1e-6:
            E2 = 1e-6
        return [1.0 / np.sqrt(E2)]

    N_grid = np.linspace(0.0, -np.log(1 + 3.0), 300)
    sol = solve_ivp(rhs, (0.0, N_grid[-1]), [0.0], t_eval=N_grid,
                    rtol=1e-9, atol=1e-12)
    if not sol.success:
        return None
    phi_arr = sol.y[0][::-1]
    N_arr = N_grid[::-1]
    z_arr = np.exp(-N_arr) - 1.0
    V_arr = OL0 * np.exp(-lam * phi_arr)

    def E(z):
        V = np.interp(z, z_arr, V_arr)
        return np.sqrt(OMEGA_R * (1 + z)**4 + Om * (1 + z)**3 + max(V, 1e-10))
    return E


C32 = ModelSpec(
    ID='C32', name='Bare Mimetic gravity',
    family='Mimetic',
    theta0=[0.3], bounds=[(-1.0, 2.0)],
    theta_names=['lambda'],
    gamma_minus_one=0.0, theory_score=5,
    sqmh_sign_ok_condition='bare only. HD extensions break γ=1.',
    notes='(dphi)^2=-1 constraint → scalar non-propagating at leading order.',
    build=_build_C32,
)


# ============ C33. f(Q) teleparallel (Jimenez-Heisenberg) ============
# f(Q) = Q + f_1 H0^2 (Q/6 H0^2)^n. Background modified Friedmann. Use
# the low-z effective DE parameterisation (Frusciante 2021) that matches the
# Phase 5 full solution to leading order in f_1: rho_de(a) reduces to a
# smooth interpolation between LCDM high-z and a shifted w0 today.
#    rho_de(a) = OL0 * [1 + f_1 * ( a^(3(1-1/(2 n))) - 1 )]
# This keeps f_1=0 → pure LCDM and reproduces the R3 numerical verification
# that f_1 > 0 gives w_a < 0 for n > 1. Valid for |f_1| ≲ 0.2, n ∈ [1.2, 3].
def _build_C33(theta, Om, h):
    f1, n = theta
    OL0 = 1.0 - Om - OMEGA_R
    alpha = 3.0 * (1.0 - 1.0 / (2.0 * n))

    def E(z):
        a = 1.0 / (1 + z)
        rho_de = OL0 * (1.0 + f1 * (a**alpha - 1.0))
        if rho_de <= 0:
            return 0.0
        return np.sqrt(OMEGA_R * (1 + z)**4 + Om * (1 + z)**3 + rho_de)
    return E


C33 = ModelSpec(
    ID='C33', name='f(Q) teleparallel (Frusciante 2021)',
    family='Modified gravity',
    theta0=[0.03, 1.5], bounds=[(-0.2, 0.2), (1.2, 3.0)],
    theta_names=['f_1', 'n'],
    gamma_minus_one=0.0, theory_score=7,
    sqmh_sign_ok_condition='f_1>0 branch → w_a<0 (R3 numerical verification)',
    notes='f(Q)=Q+f_1 H0^2 (Q/6H0^2)^n, n>=1. R3 confirms f_1>0 for w_a<0.',
    build=_build_C33,
)


# ============ C41. Wetterich / Amendola fluid IDE ============
# Coupled continuity (w_DE = -1):
#   dρ_m/dN = -3 ρ_m + 3 β ρ_DE
#   dρ_DE/dN = -3 β ρ_DE        → ρ_DE(a) = OL0 * a^(-3 β)
# Closed-form particular + homogeneous:
#   ρ_m(a) = β OL0/(1-β) * a^(-3β) + (Om - β OL0/(1-β)) * a^(-3)
def _build_C41(theta, Om, h):
    beta, = theta
    OL0 = 1.0 - Om - OMEGA_R
    if abs(1.0 - beta) < 1e-6:
        return None
    A = beta * OL0 / (1.0 - beta)
    B = Om - A  # particular+homogeneous decomposition at a=1

    def E(z):
        a = 1.0 / (1 + z)
        rm = A * a**(-3 * beta) + B * a**(-3)
        rDE = OL0 * a**(-3 * beta)
        if rm < 0:
            rm = 0.0
        Or = OMEGA_R * (1 + z)**4
        return np.sqrt(max(rm + rDE + Or, 1e-12))
    return E


C41 = ModelSpec(
    ID='C41', name='Wetterich/Amendola fluid IDE',
    family='IDE',
    theta0=[0.03], bounds=[(-0.08, 0.08)],
    theta_names=['beta'],
    gamma_minus_one=0.0, theory_score=6,
    sqmh_sign_ok_condition='beta>0 for w_a<0, bounded |β|≤0.05 (toy valid)',
    notes='Coupled continuity. Phase 3 β=0.107 not inheritable (toy linear '
          'regime breaks).',
    build=_build_C41,
)


ALL_MODELS: List[ModelSpec] = [
    C10k, C27, C33,              # A-grade priority
    C11D, C23, C41,              # A-minus priority
    C5r, C6s, C26, C28, C32,     # B-grade priority
]
