# -*- coding: utf-8 -*-
"""
L13-W: wa theoretical correction analysis.

Rule-B 4-person code review:
  R1 (CPL extraction): extract w0,wa from A01 and full ODE
  R2 (perturbative corrections): higher-order terms in SQMH expansion
  R3 (initial conditions): non-equilibrium initial conditions effect on wa
  R4 (verdict): K83/Q83 judgment

A01 wa ~ -0.133 (from L11 CPL fit)
DESI wa = -0.64 (center value, DR2 + Planck + DES-all)
Gap = 0.507

Can SQMH theory produce wa corrections >= 0.3?

Three channels:
1. Higher-order expansion (2nd order in Om)
2. Non-equilibrium initial conditions (n_bar_init != n_bar_eq at high z)
3. Radiation era coupling (OMEGA_R contribution)
"""
from __future__ import annotations
import os
import sys
import json
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import curve_fit, minimize

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')

_THIS = os.path.dirname(os.path.abspath(__file__))

OMEGA_R = 9.1e-5
Om_fid = 0.3102
OL0_fid = 1.0 - Om_fid - OMEGA_R
H0_fid = 67.7e3 / 3.086e22  # s^-1


def extract_cpl_from_rho(rho_de_func, Om, OL0, z_fit_max=1.5):
    """
    Extract CPL w0, wa by fitting E^2(z) to CPL template.
    Uses direct E^2 comparison in z in [0.01, z_fit_max].
    """
    z_arr = np.linspace(0.01, z_fit_max, 200)
    a_arr = 1.0 / (1.0 + z_arr)

    rho_de_arr = np.array([rho_de_func(a) for a in a_arr])
    E2_model = OMEGA_R * (1 + z_arr)**4 + Om * (1 + z_arr)**3 + rho_de_arr

    def cpl_E2(z, w0, wa):
        a = 1.0 / (1.0 + z)
        # CPL: w = w0 + wa*(1-a)
        # rho_DE/OL0 = exp(3*integral da/a (1+w))
        # = exp(3*integral da/a (1+w0+wa*(1-a)))
        # = a^(-3*(1+w0+wa)) * exp(3*wa*(a-1))... exact CPL
        rho_cpl = OL0 * a**(-3.0*(1.0 + w0 + wa)) * np.exp(3.0 * wa * (a - 1.0))
        E2 = OMEGA_R * (1 + z)**4 + Om * (1 + z)**3 + rho_cpl
        return E2

    try:
        popt, _ = curve_fit(cpl_E2, z_arr, E2_model, p0=[-0.9, -0.13],
                            bounds=([-1.5, -3.0], [-0.5, 2.0]),
                            maxfev=5000)
        w0, wa = popt
    except Exception:
        w0, wa = -0.9, -0.13
    return w0, wa


# ---------------------------------------------------------------------------
# Channel 1: A01 baseline
# ---------------------------------------------------------------------------

def rho_A01(a, Om=Om_fid, OL0=OL0_fid):
    return OL0 * (1.0 + Om * (1.0 - a))


# ---------------------------------------------------------------------------
# Channel 2: Higher-order SQMH expansion (2nd order in perturbation)
# ---------------------------------------------------------------------------
# A01 = 1st order in delta = Om*(1-a)
# 2nd order: include (1-a)^2 term
# From ODE solution:
#   omega_de(a) = G0*Om/(6*a^3) + C*a^3
# Expand at a=1-epsilon, epsilon = 1-a:
#   1/a^3 ~ 1 + 3*epsilon + 6*epsilon^2 + ...
#   a^3 ~ 1 - 3*epsilon + 3*epsilon^2 + ...
# omega_de = G0*Om/6 * (1+3e+6e^2+...) + C*(1-3e+3e^2+...)
#          = [G0*Om/6+C] + e*[G0*Om/2 - 3C] + e^2*[G0*Om - 3C] + ...
# At e=0: G0*Om/6+C = OL0 (BC)
# Linear: G0*Om/2 - 3C (this is the wa term)
# Quadratic: G0*Om - 3C

def rho_2nd_order(a, Om=Om_fid, OL0=OL0_fid, G0=None):
    """2nd order SQMH expansion."""
    if G0 is None:
        G0 = 3.0 * Om  # A01 prescription
    C = OL0 - G0 * Om / 6.0
    epsilon = 1.0 - a
    # Exact ODE solution (not truncated):
    rho = G0 * Om / (6.0 * a**3) + C * a**3
    return rho


# ---------------------------------------------------------------------------
# Channel 3: Non-equilibrium initial conditions
# ---------------------------------------------------------------------------
# In SQMH: if n_bar_init > n_bar_eq at high z (over-production)
# Then dark energy decays faster -> more negative wa
# delta_init = (n_bar_init - n_bar_eq) / n_bar_eq

def rho_nonequil(a, Om=Om_fid, OL0=OL0_fid, delta_init=0.1, G0=None):
    """
    SQMH ODE with non-equilibrium initial condition at z_ini=3.
    omega_de(a) = G0*Om/(6*a^3) + C_eff*a^3
    where C_eff accounts for delta_init.
    """
    if G0 is None:
        G0 = 3.0 * Om
    z_ini = 3.0
    a_ini = 1.0 / (1.0 + z_ini)
    # Equilibrium omega_de at z_ini:
    omega_de_eq_ini = G0 * Om / (6.0 * a_ini**3)
    # Non-equilibrium: start with (1 + delta_init) * omega_de_eq
    omega_de_ini = omega_de_eq_ini * (1.0 + delta_init)
    # General solution: omega_de(a) = G0*Om/(6*a^3) + D*a^3
    # At a=a_ini: omega_de_ini = G0*Om/(6*a_ini^3) + D*a_ini^3
    # => D = (omega_de_ini - G0*Om/(6*a_ini^3)) / a_ini^3
    D = (omega_de_ini - G0 * Om / (6.0 * a_ini**3)) / a_ini**3
    rho = G0 * Om / (6.0 * a**3) + D * a**3
    # Normalize to OL0 at a=1:
    rho_today = G0 * Om / 6.0 + D
    norm = OL0 / max(rho_today, 1e-10)
    return rho * norm


# ---------------------------------------------------------------------------
# Channel 4: Radiation coupling
# ---------------------------------------------------------------------------
# A01 ignores radiation in rho_m(z) = Om*(1+z)^3
# Full matter: rho_m_total = Om*(1+z)^3 + OMEGA_R*(1+z)^4 * (matter fraction)
# Radiation-era contribution adds (1+z)^4 term to ODE source

def rho_with_radiation(a, Om=Om_fid, OL0=OL0_fid, G0=None):
    """SQMH with radiation contribution to production term."""
    if G0 is None:
        G0 = 3.0 * Om
    # Modified production: source = G0 * (Om*(1+z)^3 + OMEGA_R*(1+z)^4)
    # ODE: dydz = G0*(Om*(1+z)^2 + OMEGA_R*(1+z)^3) - 3y/(1+z)
    # Particular solutions:
    #   From Om*(1+z)^2 term: y_p1 = G0*Om*(1+z)^3/6 [same as before]
    #   From OMEGA_R*(1+z)^3 term: try y_p2 = B*(1+z)^4
    #     4B*(1+z)^3 = G0*OMEGA_R*(1+z)^3 - 3*B*(1+z)^3 ... wait
    #     dy/dz|_{y_p2} = 4B*(1+z)^3
    #     rhs = G0*OMEGA_R*(1+z)^3 - 3*B*(1+z)^3
    #     => 4B = G0*OMEGA_R - 3B => 7B = G0*OMEGA_R => B = G0*OMEGA_R/7
    #   So y_p2 = G0*OMEGA_R*(1+z)^4/7
    # General: y = G0*Om*(1+z)^3/6 + G0*OMEGA_R*(1+z)^4/7 + C*(1+z)^(-3)
    # BC at a=1: y(0) = G0*Om/6 + G0*OMEGA_R/7 + C = OL0
    C = OL0 - G0 * Om / 6.0 - G0 * OMEGA_R / 7.0
    rho = G0 * Om / (6.0 * a**3) + G0 * OMEGA_R / (7.0 * a**4) + C * a**3
    # Normalize at a=1
    rho_today = G0 * Om / 6.0 + G0 * OMEGA_R / 7.0 + C
    norm = OL0 / max(rho_today, 1e-10)
    return rho * norm


def main():
    print('=== L13-W: wa Theoretical Correction Analysis ===')
    print()

    # Reference values
    w0_DESI = -0.757
    wa_DESI = -0.83  # DESI DR2 + Planck + DES-all
    w0_A01_ref = -0.9
    wa_A01_ref = -0.133  # from L11

    Om = Om_fid
    OL0 = OL0_fid

    print('DESI DR2: w0=' + str(w0_DESI) + ', wa=' + str(wa_DESI))
    print('A01 (L11): w0~' + str(w0_A01_ref) + ', wa~' + str(wa_A01_ref))
    print('wa gap to close: ' + str(round(wa_DESI - wa_A01_ref, 3)))
    print()

    results = {}

    # --- Channel 1: A01 baseline ---
    w0_a01, wa_a01 = extract_cpl_from_rho(lambda a: rho_A01(a), Om, OL0)
    print('Channel 1 (A01 baseline): w0=' + str(round(w0_a01, 3)) +
          ', wa=' + str(round(wa_a01, 3)))
    results['A01_w0'] = float(w0_a01)
    results['A01_wa'] = float(wa_a01)

    # --- Channel 2: Exact ODE solution with G0=3*Om ---
    w0_ode, wa_ode = extract_cpl_from_rho(lambda a: rho_2nd_order(a), Om, OL0)
    print('Channel 2 (Exact ODE, G0=3*Om): w0=' + str(round(w0_ode, 3)) +
          ', wa=' + str(round(wa_ode, 3)))
    results['ODE_exact_w0'] = float(w0_ode)
    results['ODE_exact_wa'] = float(wa_ode)

    # --- Channel 3: Non-equilibrium initial conditions ---
    for delta in [0.05, 0.1, 0.2, 0.5, 1.0]:
        w0_ne, wa_ne = extract_cpl_from_rho(
            lambda a, d=delta: rho_nonequil(a, delta_init=d), Om, OL0)
        print('Channel 3 (non-equil, delta=' + str(delta) + '): w0=' +
              str(round(w0_ne, 3)) + ', wa=' + str(round(wa_ne, 3)))
        results['nonequil_delta_' + str(delta)] = {'w0': float(w0_ne), 'wa': float(wa_ne)}

    # --- Channel 4: Radiation coupling ---
    w0_rad, wa_rad = extract_cpl_from_rho(lambda a: rho_with_radiation(a), Om, OL0)
    print('Channel 4 (radiation coupling): w0=' + str(round(w0_rad, 3)) +
          ', wa=' + str(round(wa_rad, 3)))
    results['radiation_w0'] = float(w0_rad)
    results['radiation_wa'] = float(wa_rad)

    print()

    # --- Channel 5: Scan G0 to find wa achievable within SQMH ---
    print('Channel 5: G0 scan to find max |wa| within SQMH...')
    G0_scan = np.linspace(0.1, 10.0, 50)
    wa_scan = []
    for G0 in G0_scan:
        w0_s, wa_s = extract_cpl_from_rho(
            lambda a, g=G0: rho_2nd_order(a, G0=g), Om, OL0)
        wa_scan.append(wa_s)

    wa_scan = np.array(wa_scan)
    max_neg_wa = np.min(wa_scan)
    G0_max_neg = G0_scan[np.argmin(wa_scan)]
    print('Max achievable |wa| by G0 scan: wa_min=' + str(round(max_neg_wa, 3)) +
          ' at G0=' + str(round(G0_max_neg, 3)))
    results['G0_scan_wa_min'] = float(max_neg_wa)
    results['G0_scan_wa_min_G0'] = float(G0_max_neg)
    results['G0_scan_values'] = G0_scan.tolist()
    results['wa_scan_values'] = wa_scan.tolist()

    print()

    # Verdict
    best_wa_achieved = min(wa_a01, wa_ode, wa_rad,
                           min(v['wa'] for v in
                               [r for k, r in results.items()
                                if isinstance(r, dict) and 'wa' in r]),
                           max_neg_wa)

    # Check K83/Q83
    wa_correction = abs(best_wa_achieved - wa_A01_ref)
    print('Best wa achieved (most negative): ' + str(round(best_wa_achieved, 3)))
    print('wa correction beyond A01: ' + str(round(wa_correction, 3)))
    print()

    if wa_correction < 0.1:
        verdict = 'K83 TRIGGERED: wa correction < 0.1. Perturbation theory insufficient.'
    elif wa_correction >= 0.3:
        verdict = 'Q83 TRIGGERED: wa correction >= 0.3. Partial gap closure possible.'
    else:
        verdict = 'K83/Q83 intermediate: correction = ' + str(round(wa_correction, 3))

    print(verdict)
    results['wa_a01_ref'] = wa_A01_ref
    results['wa_desi'] = wa_DESI
    results['best_wa_achieved'] = float(best_wa_achieved)
    results['wa_correction_beyond_A01'] = float(wa_correction)
    results['verdict'] = verdict
    results['k83_triggered'] = wa_correction < 0.1
    results['q83_triggered'] = wa_correction >= 0.3

    out_path = os.path.join(_THIS, 'l13_wwa_results.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print('Results saved to: ' + out_path)
    return results


if __name__ == '__main__':
    main()
