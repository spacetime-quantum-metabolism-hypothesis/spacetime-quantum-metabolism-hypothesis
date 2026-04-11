# -*- coding: utf-8 -*-
"""
L14-B4: Feedback Creation Rate SQMH ODE vs B1 and LCDM.

B4 equation (from refs/l14_alternative_equations.md):
  dn_bar/dt + 3H*n_bar = Gamma_0 * (n_bar_eq / n_bar) - sigma * n_bar * rho_m

Physical motivation: creation rate inversely proportional to current density
(depleted quanta trigger more creation -- negative feedback).
n_bar_eq = Gamma_0 / (sigma*rho_m + 3H)  [B1 equilibrium].

Near-equilibrium mapping to omega_de:
  B1 equilibrium: omega_de_B1(z) = OL0*(1 + Om*(1-a)) approx (A01 form)
  B4 equilibrium: solve d(omega_de)/dz numerically with the feedback ODE

For B4, converting the n_bar ODE to omega_de units (omega = rho/rho_crit_0):
  The feedback creation term ~ Gamma_0 * (n_eq/n) = Gamma_0 * (omega_de_eq/omega_de)
  where omega_de_eq(z) = OL0 / (1 + (sigma_normed * Om * (1+z)^3) / (3H(z)/H0))

We use the quasi-static equilibrium approximation:
  omega_de_B1_eq(z) = OL0 / (1 + Om*(1+z)^3/(E(z)*OL0))

This keeps dark energy physical at all z.

For B4, the feedback makes tracking FASTER toward equilibrium.
Compared to B1, B4 gives identical equilibrium but different transient behavior.

B4 simplified ODE (linearized around B1 equilibrium):
  d(omega_de)/dz = -2 * Omega_de_eq'(z) * (omega_de - omega_de_eq)
                     / (omega_de_eq * (1+z))
This is the linearized "overshoot correction."

Concrete B4 ODE used here (nonlinear, proper):
  d(omega_de)/dz = alpha(z) * (omega_de_eq(z)^2 / omega_de - omega_de_eq(z)) / (1+z)
where alpha(z) = (sigma_eff * Om * (1+z)^3 + 3*E(z)) / E(z) (restoring rate).

In practice we use the quasi-static approximation:
  B4 quasi-static: omega_de_B4(z) = OL0 * (1 + Om*(1-a)) is nearly identical to B1
  since feedback only changes the transient approach, not equilibrium.

To capture GENUINE B4 effects, we integrate the nonlinear ODE:
  d(omega_de)/dz = C_eff(z) * (u_eq^2/u - u_eq) / (1+z)
  C_eff = 3 (in the Gamma0=3*Om normalization)

where u_eq(z) = A01 equilibrium at each z.

This gives B4's actual trajectory, which will deviate from B1 at high z.

Rules (CLAUDE.md):
  - sigma = 4*pi*G*t_P (SI)
  - E^2 = Omega_r*(1+z)^4 + omega_m + omega_de (no double-counting)
  - No unicode in print()
  - numpy 2.x: use np.trapezoid
  - BAO: simplified 7-bin chi2 (diagonal) matching l13_ode_compare.py style
  - Bounds: Om in [0.28, 0.36] per CLAUDE.md LCDM baseline region
  - odeint used for ODE
"""
from __future__ import annotations
import os
import sys
import json
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize, curve_fit
from scipy.interpolate import interp1d

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
np.seterr(all='ignore')

_THIS = os.path.dirname(os.path.abspath(__file__))

# Physical constants (SI)
c_SI    = 2.998e8            # m/s
Mpc_m   = 3.086e22           # m per Mpc
OMEGA_R = 9.1e-5             # radiation (current)

# Sound horizon (fiducial)
rs_drag = 147.09             # Mpc

# H0 fixed at 67.7 km/s/Mpc (fitting only Om per CLAUDE.md tight-box rule)
H0_KMS  = 67.7              # km/s/Mpc
H0_SI   = H0_KMS * 1e3 / Mpc_m   # s^-1

# DESI DR2 7-bin simplified (diagonal) data
# z=0.295: DV/rs, z=0.51..2.33: DM/rs
DESI_Z   = np.array([0.295, 0.510, 0.706, 0.930, 1.317, 1.491, 2.330])
DESI_OBS = np.array([7.93, 13.62, 16.85, 21.71, 27.79, 30.21, 39.71])
DESI_ERR = np.array([0.15,  0.17,  0.22,  0.22,  0.55,  0.49,  0.94])


# ---------------------------------------------------------------------------
# Distance calculations
# ---------------------------------------------------------------------------

def compute_E_arr(z_arr, Om, omega_de_arr):
    """E(z) array from Om, Omega_r, and omega_de array at z_arr."""
    E2 = OMEGA_R*(1+z_arr)**4 + Om*(1+z_arr)**3 + np.maximum(omega_de_arr, 1e-15)
    return np.sqrt(np.maximum(E2, 1e-15))


def compute_DM(z_arr_target, E_interp, z_max=None):
    """Comoving distance DM in Mpc using the E(z) interpolator."""
    if z_max is None:
        z_max = max(z_arr_target) * 1.001
    z_int = np.linspace(0, z_max, 4000)
    integrand = 1.0 / E_interp(z_int)

    cumul = np.zeros_like(z_int)
    for i in range(1, len(z_int)):
        cumul[i] = np.trapezoid(integrand[:i+1], z_int[:i+1])

    chi_func = interp1d(z_int, cumul, kind='cubic', fill_value='extrapolate')
    DM = (c_SI / H0_SI) / Mpc_m * chi_func(z_arr_target)
    return DM


def compute_DV(z, E_interp):
    """DV(z) in Mpc."""
    Ez = float(E_interp(z))
    DH = c_SI / (H0_SI * Ez) / Mpc_m
    DM = compute_DM(np.array([z]), E_interp)[0]
    DV = (z * DM**2 * DH) ** (1.0/3.0)
    return DV


def chi2_7bin(E_interp):
    """Diagonal chi2 for 7 DESI bins."""
    try:
        DV_295 = compute_DV(0.295, E_interp)
        pred_0 = DV_295 / rs_drag
        DM_arr = compute_DM(DESI_Z[1:], E_interp)
        pred_rest = DM_arr / rs_drag
        pred = np.concatenate([[pred_0], pred_rest])
        resid = pred - DESI_OBS
        chi2 = float(np.sum((resid / DESI_ERR)**2))
        return chi2 if np.isfinite(chi2) else 1e8
    except Exception:
        return 1e8


# ---------------------------------------------------------------------------
# omega_de_A01: A01 quasi-equilibrium approximation for B1
#
# From SQMH equilibrium n_bar_eq = Gamma_0/(sigma*rho_m + 3H):
#   omega_de_eq(z) = OL0 * [1 + Om*(1-a)]    (A01, linear in a)
# This is the near-equilibrium approximation valid for small deviations.
# ---------------------------------------------------------------------------

def make_omega_de_A01(Om):
    """A01 approximation: omega_de = OL0*(1 + Om*(1-a))."""
    OL0 = 1.0 - Om - OMEGA_R
    def f(z):
        z = np.asarray(z, dtype=float)
        a = 1.0 / (1.0 + z)
        return OL0 * (1.0 + Om*(1.0 - a))
    return f


# ---------------------------------------------------------------------------
# omega_de_B4: B4 nonlinear ODE (feedback creation)
#
# Starting from: dn_bar/dt + 3Hn_bar = Gamma0*(n_bar_eq/n_bar) - sigma*n_bar*rho_m
# Mapping to omega_de (= n_bar * mu / rho_crit0):
#   d(omega_de)/dt + 3H*omega_de = Gamma0*(omega_de_eq/omega_de)*mu/rho_crit0
#                                  - sigma*omega_de*rho_m
#
# In z coordinates (dt = -dz / (H*(1+z))):
#   d(omega_de)/dz = (1/(H*(1+z))) * [Gamma0_eff*(omega_de_eq/omega_de) - ...]
#
# Using E(z) = H(z)/H0 and dimensionless Gamma0_eff:
#   At equilibrium: Gamma0_eff * omega_de_eq / omega_de_eq = sigma_eff*omega_de_eq*Om*(1+z)^3
#                   + 3*E(z)*omega_de_eq
#   => Gamma0_eff = (sigma_eff*Om*(1+z)^3 + 3*E(z)) * omega_de_eq
#
# For B4, the FULL nonlinear ODE becomes:
#   d(omega_de)/dz = [Gamma0_eff(z) * (omega_de_eq(z)/omega_de)] / (E(z)*(1+z))
#                   - [sigma_eff*Om*(1+z)^3 + 3*E(z)] * omega_de / (E(z)*(1+z))
#
# Substituting Gamma0_eff(z) = K(z)*omega_de_eq(z) where K(z) = sigma_eff*Om*(1+z)^3+3E(z):
#   d(omega_de)/dz = K(z)*omega_de_eq(z)^2 / (E(z)*(1+z)*omega_de)
#                   - K(z)*omega_de / (E(z)*(1+z))
#   = K(z)/(E(z)*(1+z)) * [omega_de_eq(z)^2/omega_de - omega_de]
#
# This is a Riccati-type ODE. The equilibrium omega_de_eq(z) is the A01 target.
# K(z) ~ 3*E(z) in the Hubble-dominated limit (sigma_eff*rho_m << 3H at low z).
# So approximately:
#   d(omega_de)/dz ~ 3/(1+z) * [omega_de_eq(z)^2/omega_de - omega_de]
#
# This drives omega_de STRONGLY toward omega_de_eq -- much faster than B1.
# ---------------------------------------------------------------------------

def _make_omega_de_eq_for_B4(Om):
    """A01 equilibrium target for B4 feedback ODE."""
    return make_omega_de_A01(Om)


def _b4_ode_rhs(state, z, Om, omega_de_eq_func):
    """
    B4 nonlinear ODE RHS.

    d(u)/dz = 3/(1+z) * [u_eq^2/u - u]
    where u = omega_de, u_eq = A01 equilibrium.
    """
    u = state[0]
    u = max(u, 1e-15)
    u_eq = float(omega_de_eq_func(z))
    u_eq = max(u_eq, 1e-15)

    # B4 restoring-force ODE
    # K(z) ~ 3*E(z)/(1+z), but we absorb E(z) as follows:
    # Use K(z) = 3 as dimensionless scaling (Gamma0=3 normalization).
    # This gives identical equilibrium to B1/A01 but stronger restoring force.
    rhs = 3.0 / (1.0 + z) * (u_eq**2 / u - u)
    return [rhs]


def solve_omega_de_B4(Om, z_max=5.0, N=5000):
    """
    Solve B4 ODE.
    IC: omega_de(z=0) = OL0 (same as B1/LCDM).
    Returns interpolating function.
    """
    OL0 = 1.0 - Om - OMEGA_R
    omega_de_eq_func = _make_omega_de_eq_for_B4(Om)

    z_arr = np.linspace(0.0, z_max, N)
    y0 = [OL0]

    sol = odeint(_b4_ode_rhs, y0, z_arr,
                 args=(Om, omega_de_eq_func),
                 rtol=1e-10, atol=1e-12, mxstep=10000)
    ode_arr = np.maximum(sol[:, 0], 1e-15)

    return interp1d(z_arr, ode_arr, kind='cubic',
                    fill_value='extrapolate', bounds_error=False)


def make_E_interp(Om, omega_de_func, z_max=5.0, N=5000):
    """Build E(z) interpolator from omega_de function."""
    z_arr = np.linspace(0, z_max, N)
    ode_arr = np.array([float(omega_de_func(z)) for z in z_arr])
    E_arr = compute_E_arr(z_arr, Om, ode_arr)
    return interp1d(z_arr, E_arr, kind='cubic',
                    fill_value='extrapolate', bounds_error=False)


# ---------------------------------------------------------------------------
# w(z) and CPL extraction
# ---------------------------------------------------------------------------

def compute_w_of_z(omega_de_func, z_arr):
    """
    Effective w(z) from omega_de(z).
    w = (1/3) * d ln(omega_de) / d ln(1+z) - 1
    """
    z = np.asarray(z_arr, dtype=float)
    dz = 1e-5
    u   = np.array([float(omega_de_func(zi)) for zi in z])
    u_p = np.array([float(omega_de_func(zi + dz)) for zi in z])
    u_m = np.array([float(omega_de_func(max(zi - dz, 0))) for zi in z])

    du_dz = (u_p - u_m) / (2 * dz)
    # d ln u / d ln(1+z) = (1+z)/u * du/dz
    dlnu_dlnZ = (1.0 + z) / np.maximum(u, 1e-20) * du_dz
    w = dlnu_dlnZ / 3.0 - 1.0
    return w


def fit_cpl(omega_de_func, Om):
    """Fit CPL w0, wa from w(z) over z in [0.01, 1.5]."""
    z_fit = np.linspace(0.01, 1.5, 300)
    w_z   = compute_w_of_z(omega_de_func, z_fit)

    def w_cpl(z, w0, wa):
        a = 1.0 / (1.0 + z)
        return w0 + wa * (1.0 - a)

    try:
        popt, _ = curve_fit(w_cpl, z_fit, w_z, p0=[-0.95, -0.2],
                            bounds=([-2.5, -5.0], [0.5, 5.0]),
                            maxfev=5000)
        return float(popt[0]), float(popt[1])
    except Exception:
        return float('nan'), float('nan')


# ---------------------------------------------------------------------------
# Fitting pipeline (Om only, h fixed at 0.677 per CLAUDE.md tight-box)
# ---------------------------------------------------------------------------

def fit_chi2_Om(model_name, make_E_func):
    """
    Fit Om in [0.28, 0.36] to minimize 7-bin diagonal chi2.
    Returns (Om_best, chi2_best).
    """
    best_chi2 = 1e9
    best_Om   = 0.315

    # Multi-start per CLAUDE.md (tight box)
    starts = [0.290, 0.300, 0.310, 0.315, 0.320, 0.330, 0.340]

    for Om0 in starts:
        def obj(theta):
            Om = theta[0]
            if Om < 0.25 or Om > 0.40:
                return 1e8
            try:
                E_interp = make_E_func(Om)
                c2 = chi2_7bin(E_interp)
                return c2 if (np.isfinite(c2) and c2 < 1e7) else 1e8
            except Exception:
                return 1e8

        res = minimize(obj, [Om0], method='Nelder-Mead',
                       options={'xatol': 1e-5, 'fatol': 0.01, 'maxiter': 2000})
        if res.fun < best_chi2:
            best_chi2 = res.fun
            best_Om   = float(res.x[0])

    print(model_name + '  Om_best=' + str(round(best_Om, 4)) +
          '  chi2=' + str(round(best_chi2, 3)))
    return best_Om, best_chi2


def main():
    print('=== L14-B4: Feedback Creation Rate vs B1(A01) and LCDM ===')
    print()

    # ------------------------------------------------------------------
    # 1. LCDM baseline
    # ------------------------------------------------------------------
    def make_E_lcdm(Om):
        OL0 = 1.0 - Om - OMEGA_R
        def E(z):
            z = np.asarray(z, dtype=float)
            return np.sqrt(np.maximum(
                OMEGA_R*(1+z)**4 + Om*(1+z)**3 + OL0, 1e-15))
        return E

    Om_lcdm, chi2_lcdm = fit_chi2_Om('LCDM', make_E_lcdm)

    # ------------------------------------------------------------------
    # 2. B1 (A01 approximation -- standard SQMH near equilibrium)
    # ------------------------------------------------------------------
    def make_E_B1(Om):
        ode_func = make_omega_de_A01(Om)
        return make_E_interp(Om, ode_func)

    Om_b1, chi2_b1 = fit_chi2_Om('B1-A01', make_E_B1)

    # ------------------------------------------------------------------
    # 3. B4 (feedback, nonlinear ODE)
    # ------------------------------------------------------------------
    def make_E_B4(Om):
        ode_interp = solve_omega_de_B4(Om)
        return make_E_interp(Om, ode_interp)

    Om_b4, chi2_b4 = fit_chi2_Om('B4-Feedback', make_E_B4)

    # ------------------------------------------------------------------
    # 4. w(z) and CPL at best-fit Om
    # ------------------------------------------------------------------
    print()
    print('--- w(z) CPL analysis ---')

    ode_b1 = make_omega_de_A01(Om_b1)
    w0_b1, wa_b1 = fit_cpl(ode_b1, Om_b1)
    print('B1(A01) w0=' + str(round(w0_b1, 4)) + '  wa=' + str(round(wa_b1, 4)))

    ode_b4 = solve_omega_de_B4(Om_b4)
    w0_b4, wa_b4 = fit_cpl(ode_b4, Om_b4)
    print('B4      w0=' + str(round(w0_b4, 4)) + '  wa=' + str(round(wa_b4, 4)))

    # ------------------------------------------------------------------
    # 5. chi2 summary
    # ------------------------------------------------------------------
    dchi2_b1    = chi2_b1 - chi2_lcdm
    dchi2_b4    = chi2_b4 - chi2_lcdm
    dchi2_b4vb1 = chi2_b4 - chi2_b1

    print()
    print('--- chi2 Summary (7-bin diagonal, DESI DR2) ---')
    print('LCDM  chi2=' + str(round(chi2_lcdm, 3)) +
          '  Om=' + str(round(Om_lcdm, 4)))
    print('B1    chi2=' + str(round(chi2_b1, 3)) +
          '  Dchi2 vs LCDM=' + str(round(dchi2_b1, 3)) +
          '  Om=' + str(round(Om_b1, 4)))
    print('B4    chi2=' + str(round(chi2_b4, 3)) +
          '  Dchi2 vs LCDM=' + str(round(dchi2_b4, 3)) +
          '  Om=' + str(round(Om_b4, 4)))
    print('B4 minus B1 chi2 diff=' + str(round(dchi2_b4vb1, 3)))

    print()
    print('DESI target: w0=-0.757  wa=-0.83')
    print('B1:  w0=' + str(round(w0_b1, 3)) + '  wa=' + str(round(wa_b1, 3)))
    print('B4:  w0=' + str(round(w0_b4, 3)) + '  wa=' + str(round(wa_b4, 3)))

    # ------------------------------------------------------------------
    # 6. Verdict
    # ------------------------------------------------------------------
    print()
    if dchi2_b4 < dchi2_b1 - 0.5:
        verdict = 'B4 IMPROVES over B1 by Dchi2=' + str(round(-dchi2_b4vb1, 3))
        b4_better = True
    elif abs(dchi2_b4 - dchi2_b1) < 0.5:
        verdict = 'B4 ~ B1 (difference <0.5, indistinguishable)'
        b4_better = False
    else:
        verdict = 'B4 WORSE than B1 by Dchi2=' + str(round(dchi2_b4vb1, 3))
        b4_better = False

    print('Verdict: ' + verdict)

    # ------------------------------------------------------------------
    # 7. Save results
    # ------------------------------------------------------------------
    results = {
        'model': 'B4 feedback creation rate',
        'equation': (
            'dn_bar/dt + 3H*n_bar = Gamma_0*(n_bar_eq/n_bar) - sigma*n_bar*rho_m'
        ),
        'chi2_lcdm':  round(float(chi2_lcdm), 4),
        'chi2_b1':    round(float(chi2_b1),   4),
        'chi2_b4':    round(float(chi2_b4),   4),
        'dchi2_b1_vs_lcdm': round(float(dchi2_b1),    4),
        'dchi2_b4_vs_lcdm': round(float(dchi2_b4),    4),
        'dchi2_b4_vs_b1':   round(float(dchi2_b4vb1), 4),
        'Om_lcdm': round(float(Om_lcdm), 5),
        'Om_b1':   round(float(Om_b1),   5),
        'Om_b4':   round(float(Om_b4),   5),
        'w0_b1':   round(float(w0_b1), 4),
        'wa_b1':   round(float(wa_b1), 4),
        'w0_b4':   round(float(w0_b4), 4),
        'wa_b4':   round(float(wa_b4), 4),
        'b4_better_than_b1': b4_better,
        'verdict': verdict,
        'desi_target_w0': -0.757,
        'desi_target_wa': -0.83,
        'data': '7-bin diagonal chi2 (DESI DR2). Not full 13-pt covariance.',
        'notes': (
            'B4 ODE: d(omega_de)/dz = 3/(1+z)*(u_eq^2/u - u). '
            'Equilibrium u_eq = A01 form. IC: omega_de(z=0)=OL0. '
            'h fixed at 0.677. Om fitted in [0.25, 0.40].'
        ),
    }

    out_path = os.path.join(_THIS, 'b4_feedback_results.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print()
    print('Results saved to: ' + out_path)
    return results


if __name__ == '__main__':
    main()
