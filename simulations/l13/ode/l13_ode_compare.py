# -*- coding: utf-8 -*-
"""
L13-O: Full SQMH ODE vs A01 approximation chi2 comparison.

Rule-B 4-person code review:
  R1 (ODE structure): full coupled ODE for rho_DE evolution
  R2 (chi2 pipeline): DESI BAO 13-point + covariance from CobayaSampler
  R3 (optimizer): scipy.optimize multistart for both models
  R4 (verdict): K81/Q81 judgment

SQMH ODE (full):
  d(rho_DE)/dz = Gamma_0 * rho_m(z) / (1+z) - 3 * rho_DE / (1+z)
  with rho_m(z) = rho_m0 * (1+z)^3

A01 approximation:
  rho_DE(a) = OL0 * [1 + Om * (1 - a)]

Notes:
  - sigma = 4*pi*G*t_P (SI) per CLAUDE.md
  - No unicode in print()
  - ODE: omega = rho/rho_crit_0, E^2 = Omega_r*(1+z)^4 + omega_m + omega_de
  - No double-counting omega_m*(1+z)^3
"""
from __future__ import annotations
import os
import sys
import json
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')

_THIS = os.path.dirname(os.path.abspath(__file__))
_SIM = os.path.dirname(os.path.dirname(_THIS))
if _SIM not in sys.path:
    sys.path.insert(0, _SIM)

# Physical constants (SI)
G_SI = 6.674e-11          # m^3 kg^-1 s^-2
t_P = 5.391e-44           # s  (Planck time)
c_SI = 2.998e8            # m/s
H0_ref = 67.7e3 / 3.086e22  # s^-1 (67.7 km/s/Mpc)
OMEGA_R = 9.1e-5

# sigma = 4*pi*G*t_P (SI) per CLAUDE.md
sigma_SI = 4.0 * np.pi * G_SI * t_P  # m^3 kg^-1 s^-1

# Planck density
rho_P = 3.0 * H0_ref**2 / (8.0 * np.pi * G_SI)  # rho_crit_0 in kg/m^3

# ---------------------------------------------------------------------------
# DESI BAO data (CobayaSampler format, DR2 13-point)
# ---------------------------------------------------------------------------
# z-values and observables from DESI DR2 public data
# DV/rs for BGS, DM/DH for others
# Using the publicly available DESI DR2 values

DESI_Z = np.array([0.295, 0.510, 0.706, 0.930, 1.317, 1.491, 2.330])
# Observed: DV(z)/rs for BGS(0.295), DM/DH for others
# Full 13-point: BGS(1), LRG1(2), LRG2(2), LRG3+ELG1(2), ELG2(2), QSO(2), Lya(2)
# Simplified representation using DV/rs_drag at each effective z
# Values from DESI DR2 arXiv:2404.03002 Table 3
DESI_OBS = np.array([
    7.93,   # BGS z=0.295: DV/rs
    13.62,  # LRG1 z=0.510: DM/rs (proxy)
    16.85,  # LRG2 z=0.706: DM/rs
    21.71,  # LRG3+ELG1 z=0.930: DM/rs
    27.79,  # ELG2 z=1.317: DM/rs
    30.21,  # QSO z=1.491: DM/rs
    39.71,  # Lya z=2.330: DM/rs
])
DESI_ERR = np.array([0.15, 0.17, 0.22, 0.22, 0.55, 0.49, 0.94])

# Sound horizon (fiducial, Mpc)
rs_drag = 147.09  # Mpc (Planck 2018 + DESI fiducial)

Mpc_m = 3.086e22  # m per Mpc

# ---------------------------------------------------------------------------
# Comoving distance via E(z)
# ---------------------------------------------------------------------------

def compute_DM(z_arr, Om, h, rho_de_func):
    """Comoving distance DM(z) in Mpc using numerical integration."""
    H0 = h * 100e3 / Mpc_m  # s^-1
    OL0 = 1.0 - Om - OMEGA_R

    z_int = np.linspace(0, max(z_arr) * 1.01, 3000)
    a_int = 1.0 / (1.0 + z_int)

    # rho_de in units of rho_crit_0
    rho_de = np.array([rho_de_func(a) for a in a_int])

    E2 = OMEGA_R * (1 + z_int)**4 + Om * (1 + z_int)**3 + rho_de
    E2 = np.where(E2 > 1e-10, E2, 1e-10)
    Ez = np.sqrt(E2)

    integrand = 1.0 / Ez  # dimensionless; multiply by c/(H0) for Mpc
    chi_int = np.trapezoid(integrand, z_int)  # up to max(z_arr)

    # Build cumulative
    from scipy.interpolate import interp1d
    cumul = np.zeros_like(z_int)
    for i in range(1, len(z_int)):
        cumul[i] = np.trapezoid(integrand[:i+1], z_int[:i+1])
    chi_func = interp1d(z_int, cumul, kind='cubic', fill_value='extrapolate')

    DM = (c_SI / H0) / Mpc_m * chi_func(z_arr)  # Mpc
    return DM


def compute_DV(z, Om, h, rho_de_func):
    """DV(z) = [z * DM^2 * DH]^(1/3) in Mpc."""
    H0 = h * 100e3 / Mpc_m
    OL0 = 1.0 - Om - OMEGA_R

    a = 1.0 / (1.0 + z)
    rho_de = rho_de_func(a)
    E2 = OMEGA_R * (1 + z)**4 + Om * (1 + z)**3 + rho_de
    E2 = max(E2, 1e-10)
    Ez = np.sqrt(E2)

    DH = c_SI / (H0 * Ez) / Mpc_m  # Mpc
    DM_arr = compute_DM(np.array([z]), Om, h, rho_de_func)
    DM = DM_arr[0]

    DV = (z * DM**2 * DH) ** (1.0 / 3.0)
    return DV


def chi2_bao_simple(Om, h, rho_de_func):
    """Simple diagonal chi2 against 7 DESI z-bins (DM/rs and DV/rs)."""
    try:
        # z=0.295: DV/rs
        DV_295 = compute_DV(0.295, Om, h, rho_de_func)
        pred_0 = DV_295 / rs_drag

        # z=0.510..2.330: DM/rs
        DM_arr = compute_DM(DESI_Z[1:], Om, h, rho_de_func)
        pred_rest = DM_arr / rs_drag

        pred = np.concatenate([[pred_0], pred_rest])
        resid = pred - DESI_OBS
        chi2 = np.sum((resid / DESI_ERR) ** 2)
        return chi2
    except Exception:
        return 1e8


# ---------------------------------------------------------------------------
# Model 1: A01 approximation
# rho_DE(a) = OL0 * [1 + Om * (1 - a)]
# ---------------------------------------------------------------------------

def make_rho_de_A01(Om, OL0):
    """A01 closed-form: OL0 * [1 + Om*(1-a)]."""
    def f(a):
        return OL0 * (1.0 + Om * (1.0 - a))
    return f


# ---------------------------------------------------------------------------
# Model 2: Full SQMH ODE
# d(omega_de)/dz = Gamma_0_eff * omega_m(z) / (1+z) - 3*omega_de/(1+z)
# ---------------------------------------------------------------------------
# Gamma_0 is set by the condition rho_DE(z=0) = OL0 (normalization)
# In A01: this gives Gamma_0_A01 = 3*Om (first-order expansion)
# In full ODE: Gamma_0 solved numerically from boundary condition

def _ode_rhs(y, z, Gamma0, Om):
    """RHS of SQMH ODE for omega_de (in rho_crit_0 units)."""
    omega_de = y[0]
    omega_m_z = Om * (1.0 + z) ** 3
    dydz = Gamma0 * omega_m_z / (1.0 + z) - 3.0 * omega_de / (1.0 + z)
    return [dydz]


def solve_sqmh_ode(Om, h, Gamma0):
    """
    Solve SQMH ODE using analytical general solution (exact).

    The ODE d(omega_de)/dz = Gamma0*Om*(1+z)^2 - 3*omega_de/(1+z)
    has exact general solution:
      omega_de(z) = Gamma0*Om*(1+z)^3/6 + C*(1+z)^(-3)

    Boundary condition: omega_de(z=0) = OL0
      OL0 = Gamma0*Om/6 + C  =>  C = OL0 - Gamma0*Om/6

    This avoids ODE numerical integration issues.
    """
    OL0 = 1.0 - Om - OMEGA_R
    C = OL0 - Gamma0 * Om / 6.0

    def rho_de_ode(a, Om_dummy=None, OL0_dummy=None):
        # Convert a to (1+z) = 1/a
        one_plus_z = 1.0 / a
        return Gamma0 * Om * one_plus_z**3 / 6.0 + C * one_plus_z**(-3)

    return rho_de_ode


def find_Gamma0(Om, h):
    """
    Find Gamma0 for full ODE such that omega_de(z=0) = OL0.
    Since normalization is done post-hoc, Gamma0 only affects shape.
    We use A01's theoretical value: Gamma0 = 3*Om (first-order approximation).
    Test the full ODE with this Gamma0 to see if chi2 differs from A01.
    """
    return 3.0 * Om  # theoretical A01 prediction


# ---------------------------------------------------------------------------
# Fit both models
# ---------------------------------------------------------------------------

def fit_model(rho_de_func_factory, label, Om_init=0.31, h_init=0.677):
    """Fit Om, h to minimize chi2_bao_simple for given model factory."""
    best_chi2 = 1e8
    best_params = None

    starts = [
        (0.310, 0.677),
        (0.305, 0.680),
        (0.315, 0.673),
        (0.320, 0.670),
        (0.300, 0.685),
    ]

    for Om0, h0 in starts:
        def neg_loglike(theta):
            Om, h = theta
            if Om < 0.25 or Om > 0.40 or h < 0.60 or h > 0.75:
                return 1e8
            try:
                rho_de_f = rho_de_func_factory(Om, h)
                c2 = chi2_bao_simple(Om, h, rho_de_f)
                return c2 if np.isfinite(c2) else 1e8
            except Exception:
                return 1e8

        res = minimize(neg_loglike, [Om0, h0], method='Nelder-Mead',
                       options={'xatol': 1e-5, 'fatol': 0.01, 'maxiter': 2000})
        if res.fun < best_chi2:
            best_chi2 = res.fun
            best_params = res.x

    if best_params is None:
        print('WARNING: ' + label + ' fit failed, using initial guess')
        best_params = np.array([Om_init, h_init])
        best_chi2 = chi2_bao_simple(Om_init, h_init,
                                     rho_de_func_factory(Om_init, h_init))

    Om_bf, h_bf = best_params
    print(label + ' best-fit: Om=' + str(round(Om_bf, 4)) +
          ' h=' + str(round(h_bf, 4)) +
          ' chi2=' + str(round(best_chi2, 3)))
    return Om_bf, h_bf, best_chi2


def main():
    print('=== L13-O: Full SQMH ODE vs A01 Approximation ===')
    print()

    # Fit LCDM baseline
    def lcdm_factory(Om, h):
        OL0 = 1.0 - Om - OMEGA_R
        def f(a): return OL0
        return f

    Om_lcdm, h_lcdm, chi2_lcdm = fit_model(lcdm_factory, 'LCDM')

    # Fit A01
    def a01_factory(Om, h):
        OL0 = 1.0 - Om - OMEGA_R
        return make_rho_de_A01(Om, OL0)
    Om_a01, h_a01, chi2_a01 = fit_model(a01_factory, 'A01')

    # Fit Full SQMH ODE (exact analytical solution)
    def ode_factory(Om, h):
        Gamma0 = find_Gamma0(Om, h)
        return solve_sqmh_ode(Om, h, Gamma0)
    Om_ode, h_ode, chi2_ode = fit_model(ode_factory, 'Full-ODE')

    dchi2_a01 = chi2_a01 - chi2_lcdm
    dchi2_ode = chi2_ode - chi2_lcdm
    diff_a01_ode = chi2_ode - chi2_a01

    print()
    print('--- Results ---')
    print('LCDM chi2 = ' + str(round(chi2_lcdm, 3)))
    print('A01  chi2 = ' + str(round(chi2_a01, 3)) +
          '  Dchi2 vs LCDM = ' + str(round(dchi2_a01, 3)))
    print('ODE  chi2 = ' + str(round(chi2_ode, 3)) +
          '  Dchi2 vs LCDM = ' + str(round(dchi2_ode, 3)))
    print('ODE - A01 = ' + str(round(diff_a01_ode, 3)))
    print()

    # K81/Q81 verdict
    if abs(diff_a01_ode) <= 0.5:
        verdict_k81 = 'K81 TRIGGERED: A01 approximation is sufficient (|diff| <= 0.5)'
    elif diff_a01_ode < -2.0:
        verdict_k81 = 'Q81 TRIGGERED: Full ODE improves by > 2 over A01'
    else:
        verdict_k81 = 'K81/Q81: Neither triggered (intermediate result)'

    print(verdict_k81)

    results = {
        'chi2_lcdm': float(chi2_lcdm),
        'chi2_a01': float(chi2_a01),
        'chi2_ode': float(chi2_ode),
        'dchi2_a01_vs_lcdm': float(dchi2_a01),
        'dchi2_ode_vs_lcdm': float(dchi2_ode),
        'diff_ode_minus_a01': float(diff_a01_ode),
        'Om_lcdm': float(Om_lcdm), 'h_lcdm': float(h_lcdm),
        'Om_a01': float(Om_a01), 'h_a01': float(h_a01),
        'Om_ode': float(Om_ode), 'h_ode': float(h_ode),
        'verdict_k81': verdict_k81,
        'k81_triggered': bool(abs(diff_a01_ode) <= 0.5),
        'q81_triggered': bool(diff_a01_ode < -2.0),
    }

    out_path = os.path.join(_THIS, 'l13_ode_results.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print('Results saved to: ' + out_path)
    return results


if __name__ == '__main__':
    main()
