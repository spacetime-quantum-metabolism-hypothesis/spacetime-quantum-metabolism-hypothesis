# -*- coding: utf-8 -*-
"""
Coupled Quintessence Module (Phase 1 of base.fix.class.md)

Solves scalar field phi with selectable V(phi) coupled to matter.
Formulation: Amendola 2000 coupled quintessence in reduced Planck units
(M_P = 1), e-folds N = ln(a) as time.

Key equations (M_P=1, H_0 as time unit):
  rho_DE = (1/2)*phi_dot^2 + V(phi)
  V_tilde = V / (3 H_0^2)                           # dimensionless
  Omega_DE = (1/6)*E^2*phi_N^2 + V_tilde            # phi_N = dphi/dN
  Friedmann: E^2*(1 - phi_N^2/6) = Omega_m + Omega_r + V_tilde
  KG:        phi_NN + (3 + E_N/E)*phi_N + 3*V'/E^2 = -sqrt(6)*beta*Omega_m/E^2
  Matter:    Omega_m_N = -3*Omega_m + sqrt(2/3)*beta*phi_N*Omega_m
  Raychaudhuri: E_N/E = -0.5*(3*Omega_m + 4*Omega_r)/E^2 - 0.5*phi_N^2

beta is dimensionless coupling. SIGN CONVENTION (important):
  In Amendola 2000 (astro-ph/9908023), the continuity equation is
    rho_m_dot + 3*H*rho_m = -sqrt(2/3)*Q_A*phi_dot*rho_m
  with + sign on KG source. Here we define beta = -Q_A so that positive
  beta corresponds to matter gaining energy from phi (phi_dot > 0), matching
  SQMH intuition (matter "annihilates" DE background).

  Hence our equations:
    dOmega_m/dN  = -3*Omega_m + sqrt(2/3)*beta*phi_N*Omega_m   (+sign)
    phi_NN + ... = -sqrt(6)*beta*Omega_m/E^2                   (-sign)

  (sqrt(6) = 3*sqrt(2/3) comes from rho_m/H^2 = 3*Omega_m/E^2
   when substituting rho_m in Amendola's eq.9 RHS.)

  Internal consistency verified against Friedmann constraint:
    E^2*(1 - phi_N^2/6) = Omega_m + Omega_r + V_tilde
  and Raychaudhuri:
    E_N/E = -0.5*(3*Omega_m + 4*Omega_r)/E^2 - 0.5*phi_N^2

For SQMH xi coupling (L_int = xi*phi*T^a_a): exact mapping to beta requires
GFT-level derivation (open problem, §15.1 #1). Here beta is fit parameter.

V(phi) families (all in reduced Planck units, phi dimensionless):
  mass:    V_tilde(phi) = (A/2) * phi^2                   (thawing)
  RP:      V_tilde(phi) = A * phi^(-n)                    (freezing, tracker)
  exp:     V_tilde(phi) = A * exp(-lam*phi)               (variable)

Integration: backward from N=0 (today) to N=-1.5 (z~3.5, covers DESI).
Today conditions:
  Omega_m(0) = config.Omega_m
  phi(0) = 1.0 (arbitrary, absorbed into A)
  phi_N(0) = 0 (slow-roll today)
  -> A determined from V_tilde(phi=1) = Omega_DE_0
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
from scipy.optimize import minimize
import config


# ============================================================
# V(phi) family definitions. Return (V_tilde, dV_tilde/dphi).
# ============================================================

def V_mass(phi, A):
    """Thawing mass term: V = (A/2) phi^2."""
    return 0.5 * A * phi**2, A * phi


def V_RP(phi, A, n):
    """Ratra-Peebles tracker: V = A phi^(-n). Requires phi > 0."""
    phi_safe = max(phi, 1e-8) if np.isscalar(phi) else np.maximum(phi, 1e-8)
    V = A * phi_safe**(-n)
    Vp = -n * A * phi_safe**(-n - 1)
    return V, Vp


def V_exp(phi, A, lam):
    """Exponential: V = A exp(-lam phi)."""
    V = A * np.exp(-lam * phi)
    return V, -lam * V


# Amplitude calibration so V_tilde(phi_0=1) = Omega_DE_0
def calibrate_amplitude(V_family, extra_params, Omega_DE_0):
    """Return A such that V_family(phi=1, A, *extra) = Omega_DE_0."""
    phi_0 = 1.0
    if V_family == "mass":
        # (A/2)*1^2 = Omega_DE_0
        return 2.0 * Omega_DE_0
    elif V_family == "RP":
        # A * 1^(-n) = A = Omega_DE_0
        return Omega_DE_0
    elif V_family == "exp":
        # A * exp(-lam) = Omega_DE_0
        lam = extra_params[0]
        return Omega_DE_0 * np.exp(lam)
    else:
        raise ValueError(f"Unknown V family: {V_family}")


def V_call(V_family, phi, A, extra_params):
    """Dispatch V(phi) evaluation."""
    if V_family == "mass":
        return V_mass(phi, A)
    elif V_family == "RP":
        return V_RP(phi, A, extra_params[0])
    elif V_family == "exp":
        return V_exp(phi, A, extra_params[0])
    raise ValueError(V_family)


# ============================================================
# Backward ODE integration
# ============================================================

def integrate_quintessence(V_family, beta, extra_params,
                           N_min=-1.5, n_steps=600,
                           phi_0=1.0, phi_N_0=0.0,
                           return_phi_N=False):
    """
    Backward integrate from today (N=0) to N=N_min.

    Returns:
      if return_phi_N is False: (z_arr, E_arr, Omega_m_arr) sorted ascending z
      if return_phi_N is True : (z_arr, E_arr, Omega_m_arr, phi_N_arr)
      or None if integration failed.
    """
    Omega_m_0 = config.Omega_m
    Omega_r_0 = config.Omega_r
    Omega_DE_0 = 1.0 - Omega_m_0 - Omega_r_0

    A = calibrate_amplitude(V_family, extra_params, Omega_DE_0)

    state0 = [Omega_m_0, phi_0, phi_N_0]

    # Track catastrophic failure (raised via NaN propagation so solve_ivp stops)
    def _fail():
        return [np.nan, np.nan, np.nan]

    def rhs(N, y):
        Om_m, phi, phi_N = y
        # phi<=0 is unphysical for V_RP (V = A*phi^-n diverges); for V_mass/V_exp
        # it is allowed but optimizer should not prefer these points.
        if not np.isfinite(phi):
            return _fail()
        if V_family == "RP" and phi <= 1e-8:
            return _fail()
        try:
            V, Vp = V_call(V_family, phi, A, extra_params)
        except (OverflowError, ValueError, ZeroDivisionError):
            return _fail()
        if not (np.isfinite(V) and np.isfinite(Vp)):
            return _fail()

        Om_r = Omega_r_0 * np.exp(-4 * N)

        denom = 1.0 - phi_N**2 / 6.0
        if denom <= 1e-4:
            # Ghost / phantom crossing region: kill trajectory.
            return _fail()
        E2 = (Om_m + Om_r + V) / denom
        if E2 <= 1e-10 or not np.isfinite(E2):
            return _fail()

        EN_over_E = -0.5 * (3.0 * Om_m + 4.0 * Om_r) / E2 - 0.5 * phi_N**2

        dOm_m = -3.0 * Om_m + np.sqrt(2.0 / 3.0) * beta * phi_N * Om_m
        dphi_N = (-(3.0 + EN_over_E) * phi_N
                  - 3.0 * Vp / E2
                  - np.sqrt(6.0) * beta * Om_m / E2)

        return [dOm_m, phi_N, dphi_N]

    try:
        N_eval = np.linspace(0.0, N_min, n_steps)
        sol = solve_ivp(rhs, [0.0, N_min], state0, t_eval=N_eval,
                        rtol=1e-8, atol=1e-10, method='DOP853',
                        max_step=0.01)
        if not sol.success:
            return None
    except Exception:
        return None

    Om_m_arr = sol.y[0].copy()
    phi_arr = sol.y[1].copy()
    phi_N_arr = sol.y[2].copy()

    # NaN guard: any NaN from _fail propagation marks the trajectory invalid.
    if (np.any(~np.isfinite(Om_m_arr)) or np.any(~np.isfinite(phi_arr))
            or np.any(~np.isfinite(phi_N_arr))):
        return None

    # Reconstruct E(z)
    V_arr = np.zeros_like(phi_arr)
    for i, p in enumerate(phi_arr):
        try:
            V_arr[i], _ = V_call(V_family, p, A, extra_params)
        except Exception:
            V_arr[i] = np.nan

    Om_r_arr = Omega_r_0 * np.exp(-4 * N_eval)
    denom_arr = np.maximum(1.0 - phi_N_arr**2 / 6.0, 1e-6)
    E2_arr = (Om_m_arr + Om_r_arr + V_arr) / denom_arr

    if np.any(~np.isfinite(E2_arr)) or np.any(E2_arr <= 0):
        return None

    E_arr = np.sqrt(E2_arr)
    z_arr = np.exp(-N_eval) - 1.0

    idx = np.argsort(z_arr)
    z_sorted = z_arr[idx]
    E_sorted = E_arr[idx]
    Om_m_sorted = Om_m_arr[idx]
    phi_N_sorted = phi_N_arr[idx]

    if return_phi_N:
        return z_sorted, E_sorted, Om_m_sorted, phi_N_sorted
    return z_sorted, E_sorted, Om_m_sorted


class E_quintessence:
    """Callable E(z) interpolator for given V family + parameters."""

    def __init__(self, V_family, beta, extra_params=()):
        self.V_family = V_family
        self.beta = beta
        self.extra_params = extra_params
        result = integrate_quintessence(V_family, beta, extra_params)
        if result is None:
            self._ok = False
            self._interp = None
        else:
            z_arr, E_arr, _ = result
            self._ok = True
            self._interp = interp1d(z_arr, E_arr, kind='cubic',
                                    bounds_error=False,
                                    fill_value=(E_arr[0], E_arr[-1]))

    def __call__(self, z, *args):
        if not self._ok:
            return 1e6
        return float(self._interp(z))

    @property
    def ok(self):
        return self._ok


# ============================================================
# Effective w(z) extraction for diagnostics
# ============================================================

def w_of_z(V_family, beta, extra_params=(), z_arr=None):
    """Compute effective w_DE(z) from numerical d ln(rho_DE)/d ln a."""
    if z_arr is None:
        z_arr = np.linspace(0, 2.5, 50)

    result = integrate_quintessence(V_family, beta, extra_params,
                                    N_min=-1.5, n_steps=2000)
    if result is None:
        return None, None

    z_num, E_num, Om_m_num = result
    N_num = -np.log(1 + z_num)

    Om_r_num = config.Omega_r * np.exp(-4 * N_num)
    Om_DE_num = E_num**2 - Om_m_num - Om_r_num

    rho_DE = Om_DE_num
    valid = rho_DE > 1e-6
    if np.sum(valid) < 10:
        return None, None

    ln_rho = np.log(np.abs(rho_DE[valid]))
    N_valid = N_num[valid]
    dln_rho_dN = np.gradient(ln_rho, N_valid)
    w_eff = -1.0 - dln_rho_dN / 3.0

    w_interp = interp1d(z_num[valid], w_eff, kind='linear',
                        bounds_error=False,
                        fill_value=(w_eff[0], w_eff[-1]))
    return z_arr, w_interp(z_arr)
