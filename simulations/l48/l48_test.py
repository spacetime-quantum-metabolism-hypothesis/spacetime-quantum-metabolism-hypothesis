#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L48: T17_full -- SQT 3-Variable ODE (n, rho_m, H) sigma0 x Gamma0 grid scan
     T20      -- sigma8 growth factor prediction
     Goal: find (sigma0, Gamma0) region satisfying H0_local=73.8 + H0_CMB=67.4 + G self-consistency

ODE system:
  dn/dt    = Gamma0 - 3H*n - sigma0*n*rho_m
  drho_m/dt = -3H*rho_m + sigma0*n*rho_m*eps/c^2
  H^2      = (8*pi*G/3)*(rho_m + n*eps/c^2)   [Friedmann, simplified]

Key relations:
  tau_q = sigma0 / (4*pi*G_N)      [from G = sigma0/(4*pi*tau_q)]
  n_inf = Gamma0 * tau_q            [equilibrium density]
  eps   = 3*H0^2*OmL*c^2 / (8*pi*G*n_inf)  [quantum energy, from Lambda_eff]
"""

import os, sys, time, json, warnings
import numpy as np
from scipy.integrate import solve_ivp, cumulative_trapezoid
import multiprocessing as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')
np.seterr(all='ignore')
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ──────────────────────────────────────────────────────────────────────────────
# Physical Constants (SI)
# ──────────────────────────────────────────────────────────────────────────────
G_N    = 6.674e-11        # m^3 kg^-1 s^-2
C_SI   = 2.998e8          # m/s
Mpc_m  = 3.0857e22        # m per Mpc
kmsM   = 1e3 / Mpc_m      # 1 km/s/Mpc in s^-1

# ── Cosmological Parameters ──
H0_LOCAL   = 73.80   # km/s/Mpc (local, SH0ES)
H0_CMB_PL  = 67.40   # km/s/Mpc (Planck CMB)
H0_TARGET  = 73.80   # input "true" H0 for ODE normalization
OM_FID     = 0.3150
OL_FID     = 0.6850   # flat: OM + OL = 1
OB_FID     = 0.0493
OR_FID     = 9.20e-5  # radiation (photons + nu, approx)
Z_STAR     = 1090.0
SIGMA8_PL  = 0.811    # Planck sigma8

# ── Grid ──
N_SIGMA  = 20
N_GAMMA  = 20
SIGMA_GRID = np.logspace(6, 9, N_SIGMA)   # sigma0 [m^3/(kg*s)]
GAMMA_GRID = np.logspace(0, 12, N_GAMMA)  # Gamma0 [m^-3 s^-1]
N_WORKERS  = 8

# ── ODE integration ──
A_INI  = 1.0 / 101.0   # z=100 start
A_FIN  = 1.0            # z=0
N_A    = 500            # evaluation points


def _jsonify(obj):
    if isinstance(obj, dict):       return {k: _jsonify(v) for k, v in obj.items()}
    if isinstance(obj, list):       return [_jsonify(v) for v in obj]
    if isinstance(obj, np.ndarray): return _jsonify(obj.tolist())
    if isinstance(obj, bool):       return bool(obj)
    if isinstance(obj, np.integer): return int(obj)
    if isinstance(obj, (np.floating, float)):
        f = float(obj)
        return None if not np.isfinite(f) else f
    return obj


# ──────────────────────────────────────────────────────────────────────────────
# Derived Parameters
# ──────────────────────────────────────────────────────────────────────────────

def _tau_q(sigma0):
    """tau_q = sigma0 / (4*pi*G_N) [s]"""
    return sigma0 / (4.0 * np.pi * G_N)


def _n_inf(sigma0, Gamma0):
    """n_inf = Gamma0 * tau_q [m^-3]"""
    return Gamma0 * _tau_q(sigma0)


def _rho_m0(H0_kmsMpc):
    """Present-day matter density [kg/m^3]"""
    H0_si = H0_kmsMpc * kmsM
    return 3.0 * H0_si**2 * OM_FID / (8.0 * np.pi * G_N)


def _eps(sigma0, Gamma0, H0_kmsMpc):
    """
    Quantum energy per quantum [J].
    Determined by matching Lambda_eff = 3*H0^2*OmL = 8*pi*G*n_inf*eps/c^2.
    eps = 3*H0^2*OmL*c^2 / (8*pi*G*n_inf)
    Returns None if n_inf <= 0.
    """
    H0_si = H0_kmsMpc * kmsM
    ni = _n_inf(sigma0, Gamma0)
    if ni <= 0.0:
        return None
    eps_val = 3.0 * H0_si**2 * OL_FID * C_SI**2 / (8.0 * np.pi * G_N * ni)
    return eps_val if np.isfinite(eps_val) and eps_val > 0 else None


def _rho_DE_density(n, eps):
    """rho_n = n * eps / c^2 [kg/m^3]"""
    return n * eps / C_SI**2


# ──────────────────────────────────────────────────────────────────────────────
# LCDM Background (used for high-z bridge and comparison)
# ──────────────────────────────────────────────────────────────────────────────

def _E_lcdm(z, Om=OM_FID, OL=OL_FID, Or=OR_FID):
    """E(z) = H(z)/H0 for flat LCDM."""
    return np.sqrt(np.maximum(Om*(1+z)**3 + Or*(1+z)**4 + OL, 1e-30))


def _H_lcdm_si(z, H0_kmsMpc):
    return H0_kmsMpc * kmsM * _E_lcdm(z)


# ──────────────────────────────────────────────────────────────────────────────
# SQT ODE System (scale factor a as independent variable)
# ──────────────────────────────────────────────────────────────────────────────

def _sqt_ode(a, y, sigma0, Gamma0, eps_val):
    """
    ODE in scale factor a = 1/(1+z), a in [a_ini, 1].
    y = [n, rho_m]
    dn/dt    = Gamma0 - 3H*n - sigma0*n*rho_m
    drho_m/dt = -3H*rho_m + sigma0*n*rho_m*eps/c^2
    H^2      = (8*pi*G/3)*(rho_m + n*eps/c^2)
    Transform: dy/da = (dy/dt) / (da/dt) = (dy/dt) / (a*H)
    """
    n, rho_m = float(y[0]), float(y[1])
    n     = max(n,     0.0)
    rho_m = max(rho_m, 0.0)

    rho_n   = n * eps_val / C_SI**2
    rho_tot = rho_m + rho_n
    if rho_tot <= 0.0:
        return [0.0, 0.0]

    H = np.sqrt(8.0 * np.pi * G_N * rho_tot / 3.0)
    if not np.isfinite(H) or H <= 0.0:
        return [0.0, 0.0]

    dadt = a * H
    if dadt <= 0.0:
        return [0.0, 0.0]

    dn_dt    = Gamma0 - 3.0*H*n - sigma0*n*rho_m
    drm_dt   = -3.0*H*rho_m + sigma0*n*rho_m*eps_val/C_SI**2

    return [dn_dt / dadt, drm_dt / dadt]


def _solve_sqt_ode(sigma0, Gamma0, H0_kmsMpc=H0_TARGET):
    """
    Solve SQT ODE from a=a_ini to a=1.
    Returns dict with a_arr, n_arr, rho_m_arr, H_arr, E_arr, or None on failure.
    """
    eps_val = _eps(sigma0, Gamma0, H0_kmsMpc)
    if eps_val is None:
        return None

    H0_si = H0_kmsMpc * kmsM
    rho_m0_val = _rho_m0(H0_kmsMpc)

    # Initial conditions at a = a_ini (z = 1/a_ini - 1 ~ 100)
    z_ini   = 1.0/A_INI - 1.0
    rm_ini  = rho_m0_val * (1.0 + z_ini)**3  # matter-dominated, a^-3 scaling
    H_ini   = _H_lcdm_si(z_ini, H0_kmsMpc)   # LCDM H at z_ini (SQT correction ~0 there)
    # Equilibrium n at high z: dn/dt~0 → n_eq ≈ Gamma0 / (3H + sigma0*rho_m)
    denom   = 3.0*H_ini + sigma0*rm_ini
    n_ini   = Gamma0 / max(denom, 1e-100)

    y0 = [n_ini, rm_ini]
    a_span = [A_INI, A_FIN]
    a_eval = np.linspace(A_INI, A_FIN, N_A)

    try:
        sol = solve_ivp(
            _sqt_ode, a_span, y0,
            args=(sigma0, Gamma0, eps_val),
            method='RK45',
            t_eval=a_eval,
            rtol=1e-6, atol=1e-10,
            max_step=0.01,
        )
    except Exception:
        return None

    if not sol.success or sol.y.shape[1] < 2:
        return None

    a_arr   = sol.t
    n_arr   = np.maximum(sol.y[0], 0.0)
    rm_arr  = np.maximum(sol.y[1], 0.0)
    rho_n_arr = n_arr * eps_val / C_SI**2
    rho_tot = rm_arr + rho_n_arr
    H2_arr  = 8.0*np.pi*G_N*rho_tot/3.0
    H2_arr  = np.maximum(H2_arr, 1e-80)
    H_arr   = np.sqrt(H2_arr)
    E_arr   = H_arr / H0_si

    # Verify E at a=1 (z=0) ~ 1
    E0 = float(E_arr[-1])
    if not np.isfinite(E0) or E0 <= 0.0:
        return None

    z_arr = 1.0/a_arr - 1.0

    return {
        'a': a_arr, 'z': z_arr,
        'n': n_arr, 'rho_m': rm_arr,
        'H': H_arr, 'E': E_arr,
        'E0': E0,   'H0_eff': float(H_arr[-1]) / kmsM,
        'eps': eps_val,
        'n_inf': _n_inf(sigma0, Gamma0),
        'tau_q': _tau_q(sigma0),
    }


# ──────────────────────────────────────────────────────────────────────────────
# H0 Tension Analysis
# ──────────────────────────────────────────────────────────────────────────────

def _sound_horizon_si(H0_kmsMpc, E_fn, Om=OM_FID, Ob=OB_FID, Or=OR_FID):
    """
    Comoving sound horizon at recombination [m]:
    r_s = integral_0^{z_*} c_s / H(z) dz
    c_s = c / sqrt(3*(1 + R_b)),  R_b = 3*rho_b/(4*rho_gamma) = 3Ob/(4Or)/(1+z)
    For z > z_ini (ODE range), use LCDM bridge (SQT correction ~0 there).
    """
    H0_si = H0_kmsMpc * kmsM
    Rb0   = 3.0*Ob/(4.0*Or)

    # Correct pre-recombination integral: from z_* to early universe (high z)
    # SQT correction negligible at z > z_ini (~100); LCDM bridge used by E_fn
    Z_HIGH = 10000.0
    n_pts = 800
    z_int = np.linspace(Z_STAR, Z_HIGH, n_pts)
    Rb_z  = Rb0 / (1.0 + z_int)
    cs_z  = C_SI / np.sqrt(3.0*(1.0 + Rb_z))
    H_z   = H0_si * np.array([float(E_fn(z)) for z in z_int])
    integrand = cs_z / np.maximum(H_z, 1e-50)
    return np.trapezoid(integrand, z_int)


def _comoving_dist_si(H0_kmsMpc, z_max, E_fn):
    """chi(z_max) = integral_0^{z_max} c/H dz [m]"""
    H0_si = H0_kmsMpc * kmsM
    n_pts = 800
    z_int = np.linspace(0.0, z_max, n_pts)
    H_z   = H0_si * np.array([float(E_fn(z)) for z in z_int])
    return np.trapezoid(C_SI / np.maximum(H_z, 1e-50), z_int)


def _E_fn_from_sol(sol, H0_kmsMpc):
    """Build E(z) interpolant from ODE solution, using LCDM for z > z_ini."""
    z_ode = sol['z'][::-1]   # increasing z
    E_ode = sol['E'][::-1]
    z_min_ode = float(z_ode[0])
    z_max_ode = float(z_ode[-1])

    def E_fn(z):
        z = float(z)
        if z <= z_max_ode:
            return float(np.interp(z, z_ode, E_ode))
        else:
            return float(_E_lcdm(z))
    return E_fn


def _h0_tension_metric(sigma0, Gamma0, H0_true=H0_TARGET):
    """
    Compute H0_local and H0_CMB_apparent for given (sigma0, Gamma0).

    H0_CMB_apparent: LCDM template fitted to the same theta_* = r_s/D_A.
    Mechanism: SQT modifies H(z), changing r_s and D_A relative to LCDM.
    Approximation: H0_CMB / H0_true ~ (r_s_SQT/r_s_LCDM) * (D_A_LCDM/D_A_SQT)
    """
    sol = _solve_sqt_ode(sigma0, Gamma0, H0_true)
    if sol is None:
        return None

    E_sqt  = _E_fn_from_sol(sol, H0_true)
    E_lcdm = lambda z: float(_E_lcdm(z))

    rs_sqt  = _sound_horizon_si(H0_true, E_sqt)
    rs_lcdm = _sound_horizon_si(H0_true, E_lcdm)
    chi_sqt  = _comoving_dist_si(H0_true, Z_STAR, E_sqt)
    chi_lcdm = _comoving_dist_si(H0_true, Z_STAR, E_lcdm)

    DA_sqt  = chi_sqt  / (1.0 + Z_STAR)
    DA_lcdm = chi_lcdm / (1.0 + Z_STAR)

    theta_sqt  = rs_sqt  / max(DA_sqt,  1e-10)
    theta_lcdm = rs_lcdm / max(DA_lcdm, 1e-10)

    # CMB-apparent H0: LCDM analyst scales H0 to match theta_*
    h0_ratio   = (rs_sqt / max(rs_lcdm, 1e-10)) * (DA_lcdm / max(DA_sqt, 1e-10))
    H0_CMB_app = H0_true * h0_ratio

    return {
        'H0_local':  H0_true,
        'H0_CMB':    float(H0_CMB_app),
        'h0_ratio':  float(h0_ratio),
        'tension_km': float(H0_true - H0_CMB_app),
        'rs_sqt_Mpc':  float(rs_sqt  / Mpc_m),
        'rs_lcdm_Mpc': float(rs_lcdm / Mpc_m),
        'DA_sqt_Mpc':  float(DA_sqt  / Mpc_m),
        'DA_lcdm_Mpc': float(DA_lcdm / Mpc_m),
        'theta_sqt':   float(theta_sqt),
        'theta_lcdm':  float(theta_lcdm),
        'sol_E0':      float(sol['E0']),
    }


# ──────────────────────────────────────────────────────────────────────────────
# Self-consistency Check
# ──────────────────────────────────────────────────────────────────────────────

def _self_consistency(sigma0, H0_kmsMpc=H0_TARGET):
    """
    tau_q = sigma0/(4*pi*G_N)
    G_derived = sigma0/(4*pi*tau_q) = G_N by construction (identity)
    Self-consistency: tau_q * 3*H0 should equal 1.
    """
    H0_si  = H0_kmsMpc * kmsM
    tau_q  = _tau_q(sigma0)
    ratio  = tau_q * 3.0 * H0_si   # should = 1 for perfect self-consistency
    sigma_sc = G_N * 4.0 * np.pi / (3.0 * H0_si)  # self-consistent sigma0
    return {
        'tau_q':    float(tau_q),
        'tau_ratio': float(ratio),
        'sigma_sc': float(sigma_sc),
        'G_derived': float(G_N),   # always = G_N by construction
    }


# ──────────────────────────────────────────────────────────────────────────────
# T20: sigma8 via growth factor
# ──────────────────────────────────────────────────────────────────────────────

def _growth_ode(a, y, E_fn, Om, H0_si):
    """
    Linear growth ODE in scale factor a:
    D'' + (3/a + H'/H) * D' - (3/2)*Om*H0^2/(a^5*H^2) * D = 0
    y = [D, D']
    """
    D, Dp = y[0], y[1]
    H  = H0_si * float(E_fn(1.0/a - 1.0))
    if H <= 0:
        return [Dp, 0.0]
    # dH/da numerically
    da = max(a * 1e-4, 1e-8)
    H_p = H0_si * float(E_fn(1.0/max(a+da, 1e-8) - 1.0))
    H_m = H0_si * float(E_fn(1.0/max(a-da, 1e-8) - 1.0))
    dHda = (H_p - H_m) / (2.0*da)

    coeff_friction = 3.0/a + dHda/H
    coeff_source   = 1.5 * Om * H0_si**2 / (a**5 * H**2)
    dDda  = Dp
    dDpda = -coeff_friction * Dp + coeff_source * D
    return [dDda, dDpda]


def _sigma8_ratio(sigma0, Gamma0, H0_kmsMpc=H0_TARGET):
    """
    sigma8_SQT / sigma8_LCDM via D+(z=0) ratio (unnormalized).
    Returns ratio or None.
    """
    H0_si  = H0_kmsMpc * kmsM

    def _grow(E_fn):
        a_ini_g = 1.0/31.0  # z=30
        y0 = [a_ini_g, 1.0]   # D~a, D'~1 in matter domination
        try:
            sol = solve_ivp(_growth_ode, [a_ini_g, 1.0], y0,
                             args=(E_fn, OM_FID, H0_si),
                             method='RK45', rtol=1e-5, atol=1e-8,
                             max_step=0.01)
            if sol.success and len(sol.t) > 1:
                return float(sol.y[0, -1])
        except Exception:
            pass
        return None

    sol_sqt = _solve_sqt_ode(sigma0, Gamma0, H0_kmsMpc)
    if sol_sqt is None:
        return None
    E_sqt  = _E_fn_from_sol(sol_sqt, H0_kmsMpc)
    E_lcdm = lambda z: float(_E_lcdm(z))

    D_sqt  = _grow(E_sqt)
    D_lcdm = _grow(E_lcdm)
    if D_sqt is None or D_lcdm is None or D_lcdm <= 0:
        return None

    return float(D_sqt / D_lcdm)


# ──────────────────────────────────────────────────────────────────────────────
# Worker (spawn-safe)
# ──────────────────────────────────────────────────────────────────────────────

def _worker(args):
    """Full analysis for one (sigma0, Gamma0) pair."""
    warnings.filterwarnings('ignore')
    np.seterr(all='ignore')
    sigma0, Gamma0 = args

    sc   = _self_consistency(sigma0)
    tens = _h0_tension_metric(sigma0, Gamma0)
    s8r  = _sigma8_ratio(sigma0, Gamma0)
    ni   = _n_inf(sigma0, Gamma0)
    tau  = _tau_q(sigma0)
    eps_v = _eps(sigma0, Gamma0, H0_TARGET)

    return {
        'sigma0':   float(sigma0),
        'Gamma0':   float(Gamma0),
        'n_inf':    float(ni) if np.isfinite(ni) else None,
        'tau_q':    float(tau),
        'eps':      float(eps_v) if eps_v is not None and np.isfinite(eps_v) else None,
        'sc':       sc,
        'tension':  tens,
        's8_ratio': float(s8r) if s8r is not None else None,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Pre-task: Validation
# ──────────────────────────────────────────────────────────────────────────────

def pretask(out_dir):
    print('\n' + '='*60)
    print('Pre-task: L48 SQT ODE Validation')
    print('='*60)
    all_ok = True

    # PT1: self-consistent sigma0
    H0_si = H0_TARGET * kmsM
    sigma_sc = G_N * 4.0*np.pi / (3.0*H0_si)
    tau_sc   = _tau_q(sigma_sc)
    ratio_sc = tau_sc * 3.0 * H0_si
    ok1 = abs(ratio_sc - 1.0) < 1e-8
    print(f'\n[PT1] Self-consistent sigma0:')
    print(f'  sigma_sc = {sigma_sc:.4e} m^3/(kg*s)')
    print(f'  tau_q    = {tau_sc:.4e} s  (should be 1/(3H0) = {1/(3*H0_si):.4e})')
    print(f'  ratio    = tau_q*3H0 = {ratio_sc:.8f}  [{"OK" if ok1 else "FAIL"}]')
    if not ok1: all_ok = False

    # PT2: ODE numerical stability at sigma_sc
    print(f'\n[PT2] ODE stability at sigma_sc, Gamma0=1e8:')
    Gamma0_test = 1e8
    sol_test = _solve_sqt_ode(sigma_sc, Gamma0_test)
    if sol_test is None:
        print('  ODE FAILED [FAIL]')
        all_ok = False
    else:
        print(f'  E(z=0)   = {sol_test["E0"]:.6f}  [{"OK" if abs(sol_test["E0"]-1)<0.05 else "WARN"}]')
        print(f'  n_inf    = {sol_test["n_inf"]:.4e} m^-3')
        print(f'  eps      = {sol_test["eps"]:.4e} J')
        print(f'  ODE [OK]')

    # PT3: eps dimension check
    print(f'\n[PT3] eps dimensional check:')
    eps_test = _eps(sigma_sc, Gamma0_test, H0_TARGET)
    if eps_test is not None:
        eps_eV = eps_test / 1.602e-19
        print(f'  eps = {eps_test:.4e} J = {eps_eV:.4e} eV')
        print(f'  n_inf * eps/c^2 / rho_crit,0 should ~ OmL = {OL_FID:.3f}')
        rho_crit0 = 3*(H0_TARGET*kmsM)**2/(8*np.pi*G_N)
        ni = _n_inf(sigma_sc, Gamma0_test)
        ratio_OL = ni * eps_test / C_SI**2 / rho_crit0
        print(f'  ratio = {ratio_OL:.4f}  [{"OK" if abs(ratio_OL-OL_FID)<0.01 else "WARN"}]')

    # PT4: r_s LCDM check (Planck: ~147 Mpc)
    print(f'\n[PT4] LCDM sound horizon:')
    rs_lcdm = _sound_horizon_si(H0_TARGET, lambda z: float(_E_lcdm(z)))
    rs_Mpc  = rs_lcdm / Mpc_m
    print(f'  r_s = {rs_Mpc:.2f} Mpc  (Planck: ~147 Mpc)  '
          f'[{"OK" if 130 < rs_Mpc < 165 else "WARN"}]')

    print(f'\n  Pre-task complete [{"OK" if all_ok else "WARN"}]')
    sys.stdout.flush()
    return all_ok


# ──────────────────────────────────────────────────────────────────────────────
# Task 0: LCDM Baseline
# ──────────────────────────────────────────────────────────────────────────────

def task0_baseline():
    print('\n' + '='*60)
    print('Task 0: LCDM Baseline')
    print('='*60)
    H0_si  = H0_TARGET * kmsM
    rho_m0 = _rho_m0(H0_TARGET)
    rho_c0 = 3.0*H0_si**2/(8.0*np.pi*G_N)
    Om_check = rho_m0/rho_c0
    rs_Mpc  = _sound_horizon_si(H0_TARGET, lambda z: float(_E_lcdm(z))) / Mpc_m
    chi_Mpc = _comoving_dist_si(H0_TARGET, Z_STAR, lambda z: float(_E_lcdm(z))) / Mpc_m
    theta   = (rs_Mpc / chi_Mpc) * (1+Z_STAR)
    print(f'  H0_true   = {H0_TARGET:.2f} km/s/Mpc')
    print(f'  H0_CMB_PL = {H0_CMB_PL:.2f} km/s/Mpc')
    print(f'  Tension   = {H0_TARGET - H0_CMB_PL:.2f} km/s/Mpc')
    print(f'  Om_check  = {Om_check:.4f} (target {OM_FID:.4f})')
    print(f'  r_s LCDM  = {rs_Mpc:.2f} Mpc')
    print(f'  theta*    = {theta:.5f} (Planck: 0.01041)')
    print(f'  sigma_sc  = {G_N*4*np.pi/(3*H0_si):.4e} m^3/(kg*s)')
    sys.stdout.flush()
    return {'rs_Mpc': rs_Mpc, 'theta': theta, 'H0': H0_TARGET}


# ──────────────────────────────────────────────────────────────────────────────
# Task 1: T17_full Grid Scan
# ──────────────────────────────────────────────────────────────────────────────

def task1_scan(pool):
    print('\n' + '='*60)
    print(f'Task 1: T17_full Grid Scan ({N_SIGMA}x{N_GAMMA}={N_SIGMA*N_GAMMA} pts)')
    print('='*60)
    t0 = time.time()

    param_list = [(s, g) for s in SIGMA_GRID for g in GAMMA_GRID]
    print(f'  Dispatching {len(param_list)} tasks to {N_WORKERS} workers...')
    sys.stdout.flush()

    results = pool.map(_worker, param_list)
    elapsed = time.time() - t0
    print(f'  Done in {elapsed:.1f}s')

    # Build result arrays
    n_pts = len(results)
    H0_local_arr  = np.full(n_pts, np.nan)
    H0_CMB_arr    = np.full(n_pts, np.nan)
    tension_arr   = np.full(n_pts, np.nan)
    tau_ratio_arr = np.full(n_pts, np.nan)
    s8_arr        = np.full(n_pts, np.nan)
    valid_mask    = np.zeros(n_pts, dtype=bool)

    for i, r in enumerate(results):
        sc_ratio = r['sc']['tau_ratio'] if r['sc'] else None
        if sc_ratio is not None:
            tau_ratio_arr[i] = sc_ratio
        if r['tension'] is not None:
            H0_local_arr[i] = r['tension']['H0_local']
            H0_CMB_arr[i]   = r['tension']['H0_CMB']
            tension_arr[i]  = r['tension']['tension_km']
            valid_mask[i]   = True
        if r['s8_ratio'] is not None:
            s8_arr[i] = r['s8_ratio']

    n_valid = int(valid_mask.sum())
    print(f'  Valid results: {n_valid}/{n_pts}')
    if n_valid > 0:
        H0_cmb_valid = H0_CMB_arr[valid_mask]
        print(f'  H0_CMB range: [{np.nanmin(H0_cmb_valid):.2f}, {np.nanmax(H0_cmb_valid):.2f}] km/s/Mpc')
        print(f'  Tension range: [{np.nanmin(tension_arr[valid_mask]):.2f}, '
              f'{np.nanmax(tension_arr[valid_mask]):.2f}] km/s/Mpc')

    sys.stdout.flush()
    return {
        'results':    results,
        'H0_local':   H0_local_arr,
        'H0_CMB':     H0_CMB_arr,
        'tension':    tension_arr,
        'tau_ratio':  tau_ratio_arr,
        's8_ratio':   s8_arr,
        'valid_mask': valid_mask,
        'sigma_grid': SIGMA_GRID,
        'gamma_grid': GAMMA_GRID,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Task 2: Self-consistency & Best-fit Analysis
# ──────────────────────────────────────────────────────────────────────────────

def task2_analyze(scan):
    print('\n' + '='*60)
    print('Task 2: Self-consistency & Best-fit Analysis')
    print('='*60)

    results   = scan['results']
    H0_CMB    = scan['H0_CMB']
    tension   = scan['tension']
    tau_ratio = scan['tau_ratio']
    s8_ratio  = scan['s8_ratio']
    valid     = scan['valid_mask']

    # Self-consistent sigma0: tau_ratio ~ 1
    H0_si = H0_TARGET * kmsM
    sigma_sc = G_N * 4.0*np.pi / (3.0*H0_si)
    print(f'\n  Self-consistent sigma0 = {sigma_sc:.4e} m^3/(kg*s)')
    print(f'  (tau_q*3H0 = 1 at this sigma0)')

    # Find pairs with H0_CMB ≈ 67.4 (+/- 2)
    target_CMB = H0_CMB_PL
    tol_CMB    = 2.0   # km/s/Mpc
    match_CMB  = valid & (np.abs(H0_CMB - target_CMB) < tol_CMB)
    n_match    = int(match_CMB.sum())
    print(f'\n  Pairs with H0_CMB in [{target_CMB-tol_CMB:.1f}, {target_CMB+tol_CMB:.1f}]: {n_match}')

    if n_match > 0:
        idx_best = np.where(match_CMB)[0]
        for ii in idx_best[:5]:
            r = results[ii]
            s8_str = f'{s8_ratio[ii]:.3f}' if np.isfinite(s8_ratio[ii]) else 'N/A'
            print(f'    sigma0={r["sigma0"]:.2e}  Gamma0={r["Gamma0"]:.2e}  '
                  f'H0_CMB={H0_CMB[ii]:.2f}  tau_ratio={tau_ratio[ii]:.3f}  '
                  f's8_ratio={s8_str}')

    # Best sigma8
    s8_valid = valid & np.isfinite(s8_ratio)
    if s8_valid.any():
        s8_vals = s8_ratio[s8_valid] * SIGMA8_PL
        print(f'\n  sigma8 range: [{np.nanmin(s8_vals):.3f}, {np.nanmax(s8_vals):.3f}]')
        print(f'  Planck sigma8 = {SIGMA8_PL:.3f}')

    sys.stdout.flush()
    return {'match_CMB': match_CMB, 'sigma_sc': sigma_sc, 'n_match': n_match}


# ──────────────────────────────────────────────────────────────────────────────
# Task 3: Visualization (4-panel)
# ──────────────────────────────────────────────────────────────────────────────

def task3_visualize(scan, analysis, lcdm_result, out_dir):
    print('\n' + '='*60)
    print('Task 3: 4-Panel Visualization')
    print('='*60)

    ns   = N_SIGMA
    ng   = N_GAMMA
    sG   = SIGMA_GRID
    gG   = GAMMA_GRID

    H0_CMB_2d = scan['H0_CMB'].reshape(ns, ng)
    tension_2d = scan['tension'].reshape(ns, ng)
    tau_r_2d   = scan['tau_ratio'].reshape(ns, ng)
    s8_2d      = scan['s8_ratio'].reshape(ns, ng) * SIGMA8_PL

    log_sigma = np.log10(sG)
    log_gamma = np.log10(gG)
    ls_mesh, lg_mesh = np.meshgrid(log_sigma, log_gamma, indexing='ij')

    fig, axes = plt.subplots(2, 2, figsize=(14, 11))
    fig.suptitle('L48: SQT T17_full sigma0 x Gamma0 Grid Scan\n'
                 f'H0_local={H0_TARGET:.1f} | H0_CMB_target={H0_CMB_PL:.1f} km/s/Mpc',
                 fontsize=13, fontweight='bold')

    BLUE = '#1f4e79'
    GRAY = '#7f7f7f'
    RED  = '#c00000'

    # ── Panel (a): H0_CMB contour ──
    ax = axes[0, 0]
    H_plot = np.where(np.isfinite(H0_CMB_2d), H0_CMB_2d, np.nan)
    levels_h = np.arange(55, 80, 2)
    cf = ax.contourf(ls_mesh, lg_mesh, H_plot, levels=50, cmap='coolwarm_r', vmin=60, vmax=78)
    plt.colorbar(cf, ax=ax, label='H0_CMB (km/s/Mpc)')
    cs = ax.contour(ls_mesh, lg_mesh, H_plot, levels=[H0_CMB_PL], colors=RED, linewidths=2)
    ax.clabel(cs, fmt=f'H0_CMB={H0_CMB_PL:.1f}', fontsize=9)
    # Self-consistent sigma0 line
    sigma_sc_log = np.log10(analysis['sigma_sc'])
    ax.axvline(sigma_sc_log, color=BLUE, ls='--', lw=1.5, label=f'sigma_sc')
    ax.set_xlabel('log10(sigma0)')
    ax.set_ylabel('log10(Gamma0)')
    ax.set_title('(a) H0_CMB apparent [km/s/Mpc]')
    ax.legend(fontsize=8)

    # ── Panel (b): H0 tension ──
    ax = axes[0, 1]
    t_plot = np.where(np.isfinite(tension_2d), tension_2d, np.nan)
    cf = ax.contourf(ls_mesh, lg_mesh, t_plot, levels=50, cmap='RdYlGn', vmin=-5, vmax=15)
    plt.colorbar(cf, ax=ax, label='H0_local - H0_CMB (km/s/Mpc)')
    target_t = H0_TARGET - H0_CMB_PL
    cs = ax.contour(ls_mesh, lg_mesh, t_plot, levels=[target_t], colors=RED, linewidths=2)
    ax.clabel(cs, fmt=f'tension={target_t:.1f}', fontsize=9)
    ax.axvline(sigma_sc_log, color=BLUE, ls='--', lw=1.5, label='sigma_sc')
    ax.set_xlabel('log10(sigma0)')
    ax.set_ylabel('log10(Gamma0)')
    ax.set_title(f'(b) H0 tension (target={target_t:.1f} km/s/Mpc)')
    ax.legend(fontsize=8)

    # ── Panel (c): tau_q self-consistency ──
    ax = axes[1, 0]
    tau_plot = np.where(np.isfinite(tau_r_2d), tau_r_2d, np.nan)
    cf = ax.contourf(ls_mesh, lg_mesh, np.log10(np.maximum(tau_plot, 1e-10)),
                     levels=50, cmap='PuOr')
    plt.colorbar(cf, ax=ax, label='log10(tau_q * 3H0)')
    cs = ax.contour(ls_mesh, lg_mesh, tau_plot, levels=[1.0], colors=BLUE, linewidths=2.5)
    ax.clabel(cs, fmt='tau_q*3H0=1', fontsize=9)
    ax.set_xlabel('log10(sigma0)')
    ax.set_ylabel('log10(Gamma0)')
    ax.set_title('(c) Self-consistency: tau_q * 3H0')
    # Highlight self-consistent sigma0
    ax.axvline(sigma_sc_log, color=RED, ls='--', lw=1.5, label='tau*3H0=1 exact')
    ax.legend(fontsize=8)

    # ── Panel (d): H(z) for best-fit + LCDM ──
    ax = axes[1, 1]
    z_plot = np.linspace(0.0, 3.0, 200)
    H_lcdm = H0_TARGET * _E_lcdm(z_plot)
    ax.plot(z_plot, H_lcdm, color=GRAY, lw=2, ls='--', label=f'LCDM (H0={H0_TARGET:.1f})')
    H_cmb_lcdm = H0_CMB_PL * _E_lcdm(z_plot, OL=1-OM_FID)
    ax.plot(z_plot, H_cmb_lcdm, color=GRAY, lw=1, ls=':', label=f'LCDM (H0={H0_CMB_PL:.1f})')

    # Plot best models (smallest |H0_CMB - H0_CMB_PL|)
    valid_idx = np.where(scan['valid_mask'])[0]
    if len(valid_idx) > 0:
        H0_cmb_v = scan['H0_CMB'][valid_idx]
        dist      = np.abs(H0_cmb_v - H0_CMB_PL)
        best_idx  = valid_idx[np.argsort(dist)[:3]]
        colors_b  = [BLUE, '#2471a3', '#5dade2']
        for bi, col in zip(best_idx, colors_b):
            r = scan['results'][bi]
            sol = _solve_sqt_ode(r['sigma0'], r['Gamma0'])
            if sol is not None:
                a_sol = sol['a']
                z_sol = 1.0/a_sol - 1.0
                H_sol = sol['H'] / kmsM
                sort_i = np.argsort(z_sol)
                ax.plot(z_sol[sort_i], H_sol[sort_i], color=col, lw=1.5,
                        label=f's={r["sigma0"]:.1e} g={r["Gamma0"]:.1e}\nH0_CMB={scan["H0_CMB"][bi]:.1f}')

    # Observational anchors
    z_obs = np.array([0.57])
    H_obs = np.array([96.8])
    H_err = np.array([3.4])
    ax.errorbar(z_obs, H_obs, yerr=H_err, fmt='ro', ms=6, label='BOSS z=0.57')

    ax.set_xlabel('z')
    ax.set_ylabel('H(z) [km/s/Mpc]')
    ax.set_title('(d) H(z): best-fit SQT vs LCDM')
    ax.legend(fontsize=7, loc='upper left')
    ax.set_xlim(0, 3); ax.set_ylim(50, 350)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    out = os.path.join(out_dir, 'l48_task3_main.png')
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Main plot: {out}')

    # ── sigma8 panel ──
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    s8_plot = np.where(np.isfinite(s8_2d), s8_2d, np.nan)
    cf = ax2.contourf(ls_mesh, lg_mesh, s8_plot, levels=50, cmap='viridis',
                      vmin=0.6, vmax=1.0)
    plt.colorbar(cf, ax=ax2, label='sigma8 (SQT)')
    cs1 = ax2.contour(ls_mesh, lg_mesh, s8_plot, levels=[0.811], colors=RED, lw=2)
    ax2.clabel(cs1, fmt='sigma8=0.811 (Planck)', fontsize=9)
    cs2 = ax2.contour(ls_mesh, lg_mesh, s8_plot, levels=[0.76], colors='orange', lw=2)
    ax2.clabel(cs2, fmt='sigma8=0.76 (KiDS)', fontsize=9)
    ax2.axvline(sigma_sc_log, color=BLUE, ls='--', lw=1.5)
    ax2.set_xlabel('log10(sigma0)')
    ax2.set_ylabel('log10(Gamma0)')
    ax2.set_title('T20: sigma8 prediction (SQT)\nBlue dashed = self-consistent sigma0')
    out2 = os.path.join(out_dir, 'l48_task3_sigma8.png')
    fig2.savefig(out2, dpi=150, bbox_inches='tight')
    plt.close(fig2)
    print(f'  sigma8 plot: {out2}')
    sys.stdout.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Task 4: Final Verdict
# ──────────────────────────────────────────────────────────────────────────────

def task4_verdict(scan, analysis):
    print('\n' + '='*60)
    print('L48 FINAL VERDICT')
    print('='*60)

    n_match = analysis['n_match']
    sigma_sc = analysis['sigma_sc']
    H0_si    = H0_TARGET * kmsM

    # Check if self-consistent sigma0 is in the scan range
    in_range = SIGMA_GRID.min() <= sigma_sc <= SIGMA_GRID.max()

    print(f'\n  sigma_sc = {sigma_sc:.4e} m^3/(kg*s)  '
          f'[{"IN RANGE" if in_range else "OUT OF RANGE"} of grid]')
    print(f'  tau_q_sc = {_tau_q(sigma_sc):.4e} s  = 1/(3H0)')
    print(f'\n  H0 tension resolution:')
    print(f'  H0_local  target = {H0_TARGET:.2f} km/s/Mpc')
    print(f'  H0_CMB_PL target = {H0_CMB_PL:.2f} km/s/Mpc')
    print(f'  Grid pairs matching H0_CMB: {n_match}/{N_SIGMA*N_GAMMA}')

    # Overall verdict
    if n_match > 0 and in_range:
        verdict = 'Q1 CANDIDATE -- tension region found AND sigma_sc in grid'
    elif n_match > 0:
        verdict = 'Q2 PARTIAL -- tension region found, sigma_sc out of grid range'
    elif in_range:
        verdict = 'Q3 SELF_CONSISTENT -- sigma_sc in range but no tension resolution'
    else:
        verdict = 'K0 FAIL -- no tension resolution, sigma_sc out of range'

    print(f'\n  [VERDICT] {verdict}')
    sys.stdout.flush()
    return {'verdict': verdict, 'n_match': n_match, 'sigma_sc': sigma_sc}


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    OUT_DIR  = _SCRIPT_DIR
    LOG_FILE = os.path.join(OUT_DIR, 'l48_run.log')

    print('='*60)
    print('L48: SQT 3-Variable ODE -- T17_full + T20')
    print(f'Grid: {N_SIGMA}x{N_GAMMA}={N_SIGMA*N_GAMMA} pts | {N_WORKERS} workers')
    print(f'H0_local={H0_TARGET:.1f}  H0_CMB_target={H0_CMB_PL:.1f} km/s/Mpc')
    print('='*60)
    sys.stdout.flush()

    pretask(OUT_DIR)

    ctx  = mp.get_context('spawn')
    pool = ctx.Pool(N_WORKERS)

    scan     = {}
    analysis = {}
    verdict  = {}
    lcdm_res = {}

    try:
        lcdm_res = task0_baseline()
        scan     = task1_scan(pool)
        analysis = task2_analyze(scan)
        task3_visualize(scan, analysis, lcdm_res, OUT_DIR)
        verdict  = task4_verdict(scan, analysis)

    finally:
        pool.close()
        pool.join()

    # ── Summary ──
    print('\n' + '='*60)
    print('L48 RESULTS SUMMARY')
    print('='*60)
    print(f"[Task 0] LCDM baseline: r_s={lcdm_res.get('rs_Mpc','?'):.2f} Mpc  "
          f"theta*={lcdm_res.get('theta','?'):.5f}")
    print(f"[Task 1] Grid {N_SIGMA}x{N_GAMMA} done. "
          f"Valid: {int(scan.get('valid_mask', np.array([])).sum())}/{N_SIGMA*N_GAMMA}")
    print(f"[Task 2] H0_CMB match pairs: {analysis.get('n_match', 0)}")
    print(f"[Verdict] {verdict.get('verdict', 'N/A')}")

    # Save JSON
    save = {
        'lcdm': _jsonify(lcdm_res),
        'verdict': _jsonify(verdict),
        'n_match': int(analysis.get('n_match', 0)),
        'sigma_sc': float(analysis.get('sigma_sc', 0)),
        'params': {
            'H0_local':  H0_TARGET,
            'H0_CMB_PL': H0_CMB_PL,
            'OM':        OM_FID,
            'OL':        OL_FID,
            'N_SIGMA':   N_SIGMA,
            'N_GAMMA':   N_GAMMA,
        },
    }
    out_json = os.path.join(OUT_DIR, 'l48_results.json')
    with open(out_json, 'w') as f:
        json.dump(save, f, indent=2)
    print(f'Saved: {out_json}')
