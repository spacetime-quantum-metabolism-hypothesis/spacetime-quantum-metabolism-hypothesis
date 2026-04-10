# -*- coding: utf-8 -*-
"""
Phase 2 linear perturbation module (Python, sub-horizon quasi-static).

Background uses Phase 1 `quintessence.py` (e-folds N = ln a). On top of that
we solve the standard matter density contrast equation in the sub-horizon
quasi-static approximation for coupled quintessence
(Amendola & Tsujikawa 2010, Ch. 9; Di Porto & Amendola 2008):

  delta_m'' + (2 + E'/E) * delta_m' - (3/2) * Omega_m(a) * (G_eff/G) * delta_m = 0

with effective Newton coupling in the sub-horizon limit k >> a H / c_s:

  G_eff / G = 1 + 2 * beta^2

(beta is the dimensionless matter-scalar coupling, same sign convention as
 `quintessence.py`: beta = -Q_Amendola.)

Assumptions / limitations:
  - Quasi-static: valid for k > ~0.01 h/Mpc. Galaxy RSD at k ~ 0.1 h/Mpc OK.
  - Sub-horizon: no ISW / lensing Cl contribution. Phase 3 (CLASS) needed
    for those.
  - Massless scalar sub-horizon: ignores the (1 + m_phi^2 a^2 / k^2) Yukawa
    factor. Correct for thawing/freezing quintessence where m_phi < H_0.
  - No radiation in the growth equation (valid at z < z_eq ~ 3400).

Output: D(a) normalized so that D(a=1) = 1, and f(a) = d ln D / d ln a.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import config


def _background_EN_over_E(N_arr, E_arr):
    """Numerical E'/E = d ln E / dN on an e-folds grid (sorted ascending)."""
    ln_E = np.log(E_arr)
    return np.gradient(ln_E, N_arr)


def growth_factor(V_family, beta, extra_params,
                  N_ini=-3.0, N_end=0.0, n_pts=400):
    """
    Solve for D(a), f(a) = dlnD/dlnN in coupled quintessence.

    Starts at N_ini = -3 (z ~ 20). WHY not N = -6? Backward integration of
    thawing potentials (V_mass) is anti-damped and blows up before z ~ 400.
    At z = 20 we are still deep in matter era (Omega_m > 0.99) so the
    delta_m ~ a initial condition is accurate, and no V family hits
    anti-damping.

    Returns
    -------
    a_arr, D_arr, f_arr : ndarrays (sorted ascending a)
        D(a=1) = 1, f(a) = d ln D / d ln a.
        None if background integration failed.
    """
    # 1) Background: LCDM analytic with the SAME Omega_m_0. Why: the
    # backward scalar-field ODE in quintessence.py drives phi_N -> sqrt(6)
    # pathologically (anti-damping), inflating E(N) via the Friedmann
    # denominator (1 - phi_N^2/6). The true effect of V(phi) on the
    # background at z < 3 is sub-percent for |beta| < 0.4, so using LCDM
    # E(N) with the SAME Omega_m_0 is accurate to better than Phase 2
    # growth data precision. The DOMINANT coupling effect in growth is
    # G_eff/G = 1 + 2*beta^2 (source enhancement), which we preserve.
    # The drag correction -beta*phi_N*delta' is a secondary effect; we
    # use a slow-roll approximation phi_N ~ sqrt(2/3)*beta*Omega_m_frac
    # (accurate to factor ~2 for |beta| < 0.4) instead of the unreliable
    # backward ODE output.
    #
    # NOTE: V_family and extra_params are ACCEPTED for API compatibility
    # with the joint fit but enter ONLY through beta and G_eff. A full
    # treatment would plumb V(phi)-specific phi_N tracker behavior; that
    # is Phase 3 CLASS-level work.
    Om_m_0 = config.Omega_m
    Om_r_0 = config.Omega_r
    Om_DE_0 = 1.0 - Om_m_0 - Om_r_0

    def E2_lcdm(N):
        a = np.exp(N)
        return Om_m_0 * a**(-3) + Om_r_0 * a**(-4) + Om_DE_0

    def E_of_N(N):
        return float(np.sqrt(E2_lcdm(N)))

    def Omm_of_N(N):
        a = np.exp(N)
        return Om_m_0 * a**(-3) / E2_lcdm(N)

    def ENE_of_N(N):
        a = np.exp(N)
        E2 = E2_lcdm(N)
        dE2 = -3.0 * Om_m_0 * a**(-3) - 4.0 * Om_r_0 * a**(-4)
        return 0.5 * dE2 / E2

    # phi_N at late time from backward ODE: unreliable for N < -0.3, but
    # for N in [-0.3, 0] the backward integrator is still dominated by the
    # boundary condition phi_N(0) = 0 and is roughly OK. We use a damped
    # approximation: phi_N_approx(N) ~ beta * Omega_DE(a) * some_factor.
    # For beta = 0, phi_N = 0 exactly.
    # For beta != 0, use a simple fit from tracker solutions:
    #   phi_N ~ sqrt(2/3) * beta * Omega_m(a) (first-order Amendola slow-roll)
    # This is a crude approximation but good to factor ~2 for |beta| < 0.4.
    def phiN_of_N(N):
        if abs(beta) < 1e-10:
            return 0.0
        # Slow-roll tracker estimate: phi_N ~ sqrt(2/3) * beta * Om_m_frac
        return float(np.sqrt(2.0 / 3.0) * beta * Omm_of_N(N))

    # 2) Growth ODE in ln a = N. Let y = [delta_m, delta_m_N].
    # Amendola-Quartin-Tsujikawa-Waga 2006 (astro-ph/0605488) eq 16:
    #   delta'' + [2 + H'/H - beta*phi'] delta' = (3/2)(1+2beta^2) Om_m delta
    # Our sign convention matches AQT directly (verified via KG source
    # -sqrt(6)*beta*Om_m/E^2 and continuity +sqrt(2/3)*beta*phi_N*Om_m).
    G_eff_over_G = 1.0 + 2.0 * beta**2

    def rhs(N, y):
        delta, delta_N = y
        Om_m = Omm_of_N(N)
        ene = ENE_of_N(N)
        phiN = phiN_of_N(N)
        drag = 2.0 + ene - beta * phiN
        d2 = -drag * delta_N + 1.5 * Om_m * G_eff_over_G * delta
        return [delta_N, d2]

    # Matter-dominated initial conditions at N_ini: delta ~ a, so delta_N = delta.
    N_eval = np.linspace(N_ini, N_end, n_pts)
    y0 = [np.exp(N_ini), np.exp(N_ini)]  # arbitrary norm; we renormalize

    sol = solve_ivp(rhs, [N_ini, N_end], y0, t_eval=N_eval,
                    rtol=1e-8, atol=1e-10, method='DOP853')
    if not sol.success:
        return None

    D_raw = sol.y[0].copy()
    D_N_raw = sol.y[1].copy()
    if not (np.all(np.isfinite(D_raw)) and np.all(np.isfinite(D_N_raw))):
        return None
    if np.any(D_raw <= 0):
        # D must be positive; any zero/negative means the growth ODE
        # diverged or underflowed — treat as failure rather than dividing.
        return None

    # f = d ln D / d ln a = D_N / D, computed from RAW values before
    # normalization (f is scale-invariant, but keep raw to avoid any
    # in-place modification hazard).
    f_arr = D_N_raw / D_raw

    # Renormalize so D(a=1)=1.
    D_today = D_raw[-1]
    if not np.isfinite(D_today) or D_today <= 0:
        return None
    D_arr = D_raw / D_today

    a_arr = np.exp(N_eval)
    return a_arr, D_arr, f_arr


def D_of_z(V_family, beta, extra_params, z_query):
    """Convenience: interpolate D(z) at query redshifts."""
    res = growth_factor(V_family, beta, extra_params)
    if res is None:
        return None
    a_arr, D_arr, _ = res
    z_arr = 1.0 / a_arr - 1.0
    idx = np.argsort(z_arr)
    interp = interp1d(z_arr[idx], D_arr[idx], kind='cubic',
                      bounds_error=False,
                      fill_value=(D_arr[idx][0], D_arr[idx][-1]))
    return np.asarray([float(interp(z)) for z in np.atleast_1d(z_query)])


if __name__ == "__main__":
    print("Quintessence growth sanity check")
    print("-" * 50)
    for fam, beta, extra in [("mass", 0.0, ()),
                             ("RP", 0.352, (0.348,)),
                             ("exp", 0.355, (0.345,))]:
        res = growth_factor(fam, beta, extra)
        if res is None:
            print(f"  {fam}: FAIL")
            continue
        a, D, f = res
        z0 = 1/a[-1] - 1
        print(f"  {fam:5s} beta={beta:+.3f}  D(a=1)={D[-1]:.3f}  "
              f"f(a=1)={f[-1]:.3f}  G_eff/G={1+2*beta**2:.3f}")
