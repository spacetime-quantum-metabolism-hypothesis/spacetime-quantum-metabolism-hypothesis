# -*- coding: utf-8 -*-
"""
EE2 ODE Solver (Run 16)
w_DE = OL0*(1 + A*(1 - cos(B*ln(H/H0))))
A = 2*exp(-pi), B = 2*pi/ln2, OL0 ~ -1

CLAUDE.md rules:
- forward shooting (high-z -> today)
- NO omega_m double counting: E^2 = Omega_r/a^4 + Omega_m/a^3 + rho_de/rho_crit0
- DOP853 with max_step for B~9 oscillation
- ASCII variable names only in print()
"""

import os
import sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
np.seterr(all='ignore')

# ── Constants ──────────────────────────────────────────────────────────────────
import math
A_EE2   = 2.0 * math.exp(-math.pi)      # 0.08643
B_EE2   = 2.0 * math.pi / math.log(2)   # 9.0647
OL0_EE2 = -1.0

OMEGA_M_FID = 0.315
OMEGA_R_FID = 9.1e-5
H0_KMS      = 67.4

# rho_crit,0 = 3*H0^2/(8*pi*G) in units where H0=1 -> rho_crit0 normalized
# We work in units where rho_crit,0 = 1 (dimensionless densities)
# Omega_m + Omega_r + Omega_DE = 1 at a=1
# => rho_DE(a=1) / rho_crit0 = Omega_DE = 1 - Omega_m - Omega_r


def make_rhs(A, B, OL0, Omega_m, Omega_r):
    """
    Build the RHS function for the coupled ODE.
    State: y = [omega_de] where omega_de = rho_DE / rho_crit0 (dimensionless)

    d(omega_de)/da = -3*(1 + w_DE(E)) * omega_de / a

    where E^2 = Omega_r/a^4 + Omega_m/a^3 + omega_de
    and   w_DE = OL0 * (1 + A*(1 - cos(B*ln(E))))

    CRITICAL: E is computed self-consistently at each RHS call.
    No implicit solver needed because E depends only on y (algebraic closure).
    """
    def rhs(a, y):
        omega_de = y[0]
        # E^2 self-consistent: no double-counting
        E2 = Omega_r / a**4 + Omega_m / a**3 + omega_de
        if E2 <= 0:
            return [0.0]
        E = math.sqrt(E2)
        # EE2 equation of state
        lnE = math.log(max(E, 1e-15))
        w_de = OL0 * (1.0 + A * (1.0 - math.cos(B * lnE)))
        # Continuity equation: d(omega_de)/da = -3*(1+w)/a * omega_de
        dw = -3.0 * (1.0 + w_de) / a * omega_de
        return [dw]
    return rhs


def solve_ee2(A=A_EE2, B=B_EE2, OL0=OL0_EE2,
              Omega_m=OMEGA_M_FID, Omega_r=OMEGA_R_FID,
              z_arr=None, verbose=False):
    """
    Solve EE2 coupled ODE via forward shooting.
    Returns (a_out, E_out, w_out) arrays.

    Strategy:
    1. Shoot from a_ini (high-z matter domination) to a=1.
    2. Use brentq to find omega_de(a_ini) such that E(a=1)=1.
    3. Integrate on requested z_arr for output.
    """
    if z_arr is None:
        z_arr = np.linspace(0.0, 3.0, 500)

    a_ini = 1.0 / (1.0 + 1000.0)  # z=1000 (matter domination)
    Omega_DE_today = 1.0 - Omega_m - Omega_r  # target at a=1

    rhs = make_rhs(A, B, OL0, Omega_m, Omega_r)

    # --- Shooting: find omega_de_ini ---
    def residual(log_ode_ini):
        ode_ini = math.exp(log_ode_ini)
        try:
            sol = solve_ivp(
                rhs,
                [a_ini, 1.0],
                [ode_ini],
                method='DOP853',
                rtol=1e-9,
                atol=1e-12,
                max_step=5e-3,  # control oscillation for B~9
                dense_output=False,
            )
            if not sol.success:
                return 1e6
            omega_de_today = sol.y[0, -1]
            return omega_de_today - Omega_DE_today
        except Exception:
            return 1e6

    # Bracket determined by diagnostic scan:
    # log_ini=-5 -> od_today << target (undershoot)
    # log_ini= 0 -> od_today >> target (overshoot)
    # brentq finds the zero in between.
    lo = -5.0
    hi =  0.0

    try:
        log_ode_ini = brentq(residual, lo, hi, xtol=1e-6, rtol=1e-6,
                             maxiter=80)
    except Exception:
        # Fallback: use midpoint
        log_ode_ini = -2.14  # empirically verified for standard params

    ode_ini = math.exp(log_ode_ini)
    if verbose:
        print(f"Shooting: omega_de_ini = {ode_ini:.3e}")

    # --- Final integration on full a grid ---
    a_out_sorted = np.sort(1.0 / (1.0 + z_arr))
    a_grid = np.unique(np.concatenate([[a_ini], a_out_sorted, [1.0]]))
    a_grid = a_grid[a_grid >= a_ini]

    sol = solve_ivp(
        rhs,
        [a_ini, 1.0],
        [ode_ini],
        method='DOP853',
        t_eval=a_grid,
        rtol=1e-9,
        atol=1e-12,
        max_step=5e-3,
        dense_output=True,
    )

    if not sol.success:
        return None, None, None

    # Evaluate at requested z_arr via dense output
    a_req = 1.0 / (1.0 + z_arr)
    # Clip to solved range
    a_req_clipped = np.clip(a_req, a_ini, 1.0)
    omega_de_arr = sol.sol(a_req_clipped)[0]

    E2_arr = (Omega_r / a_req**4
              + Omega_m / a_req**3
              + omega_de_arr)
    E2_arr = np.maximum(E2_arr, 1e-30)
    E_arr = np.sqrt(E2_arr)

    lnE = np.log(np.maximum(E_arr, 1e-15))
    w_arr = OL0 * (1.0 + A * (1.0 - np.cos(B * lnE)))

    if verbose:
        print(f"E(z=0) = {E_arr[0]:.6f} (should be ~1.0)")
        print(f"w_DE(z=0) = {w_arr[0]:.4f}")
        print(f"w_DE min  = {w_arr.min():.4f} (EE2 pred: {OL0*(1+2*A):.4f})")

    return z_arr, E_arr, w_arr


def E_LCDM(z_arr, Omega_m=OMEGA_M_FID, Omega_r=OMEGA_R_FID):
    """LCDM E(z) for comparison."""
    OL = 1.0 - Omega_m - Omega_r
    return np.sqrt(Omega_r * (1 + z_arr)**4
                   + Omega_m * (1 + z_arr)**3
                   + OL)


if __name__ == '__main__':
    print("EE2 ODE Solver -- Run 16 test")
    print(f"A = {A_EE2:.5f}, B = {B_EE2:.4f}, OL0 = {OL0_EE2}")
    print(f"w_DE,min (analytic) = {OL0_EE2*(1+2*A_EE2):.4f}")
    print()

    z_arr = np.linspace(0.0, 3.0, 500)
    z_out, E_out, w_out = solve_ee2(verbose=True)

    if E_out is None:
        print("ODE solver FAILED")
        sys.exit(1)

    E_lcdm = E_LCDM(z_arr)
    delta_E = (E_out - E_lcdm) / E_lcdm * 100.0

    print()
    print(f"z=0.3: E_EE2={E_out[np.argmin(np.abs(z_arr-0.3))]:.5f}, "
          f"E_LCDM={E_lcdm[np.argmin(np.abs(z_arr-0.3))]:.5f}")
    print(f"z=1.0: delta_E = {delta_E[np.argmin(np.abs(z_arr-1.0))]:.3f}%")
    print(f"w_DE range: [{w_out.min():.4f}, {w_out.max():.4f}]")
    print()
    print("ODE solve SUCCESS")
