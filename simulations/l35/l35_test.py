# -*- coding: utf-8 -*-
"""
l35_test.py -- L35: Multi-probe joint fit (BAO+CMB+SN+RSD)
==========================================================
Tests Models A (k=2), B (k=3), C (k=4) vs LCDM baseline.
Om~0.30 region (CMB-constrained).

L34 bug prevention applied:
- config.H_0_km = H0 before each CMB chi2 call
- ratio clipped [1,200]
- N_GRID=4000, cumulative_trapezoid
- Om range [0.15, 0.50]
- omega_b=0.02236 fixed (k unchanged)
"""

import os, sys, json, time, warnings
import numpy as np
from scipy.integrate import cumulative_trapezoid, solve_ivp, quad
from scipy.optimize import minimize, differential_evolution

warnings.filterwarnings('ignore')
np.seterr(all='ignore')
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SIM_DIR    = os.path.dirname(_SCRIPT_DIR)
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

import config as _cfg
from desi_data import DESI_DR2, DESI_DR2_COV_INV
from phase2.sn_likelihood import DESY5SN

C_KMS  = 299792.458
R_S    = 147.09
OR     = 5.38e-5
N_GRID = 4000
OMEGA_B_FIXED = 0.02236
SIGMA_8_0     = 0.8111

# ─── Planck 2018 compressed CMB prior (shift params) ────────────────────────
# R = 1.7502 ± 0.0046,  l_A = 301.471 ± 0.090,  Ob_h2 = 0.02236 ± 0.00015
CMB_OBS = np.array([1.7502,    301.471,   0.02236])
CMB_SIG = np.array([0.0046,    0.090,     0.00015])

def _z_star(omega_b, omega_m):
    g1 = 0.0783 * omega_b**(-0.238) / (1.0 + 39.5 * omega_b**0.763)
    g2 = 0.560 / (1.0 + 21.1 * omega_b**1.81)
    return 1048.0 * (1.0 + 0.00124 * omega_b**(-0.738)) * (1.0 + g1 * omega_m**g2)

def _r_s(omega_b, omega_c, h, z_star):
    omega_gamma = 2.4728e-5
    omega_nu    = 3.046 * (7./8.) * (4./11.)**(4./3.) * omega_gamma
    omega_r     = omega_gamma + omega_nu
    omega_m     = omega_b + omega_c
    omega_de    = h*h - omega_m - omega_r

    def integrand(a):
        R   = 3.0 * omega_b / (4.0 * omega_gamma) * a
        c_s = 1.0 / np.sqrt(3.0 * (1.0 + R))
        H2  = (omega_r/a**4 + omega_m/a**3 + omega_de) * 100.0**2
        # C_KMS [km/s] / sqrt(H2) [km/s/Mpc] = Mpc (no extra 1e-3)
        return C_KMS * c_s / (a*a * np.sqrt(max(H2, 1e-30)))

    a_star = 1.0 / (1.0 + z_star)
    val, _ = quad(integrand, 1e-8, a_star, limit=200, epsabs=1e-4)
    return val  # Mpc

def chi2_cmb(E_fn, Om, H0):
    h       = H0 / 100.0
    omega_b = OMEGA_B_FIXED
    omega_c = Om * h**2 - omega_b
    if omega_c <= 0:
        return 1e8
    _cfg.H_0_km = H0  # CRITICAL: fix H0 for D_M calculation

    omega_m = omega_b + omega_c
    z_star  = _z_star(omega_b, omega_m)

    # D_M(z*) = (c/H0) * integral 1/E dz  — use quad for accuracy (trapz with 2000pts
    # over [0,1100] has 0.38% error in D_M → chi2_lA≈269 artifact)
    def _inv_E(z_val):
        v = E_fn(np.array([float(z_val)]), Om)
        return 0.0 if (v is None or not np.isfinite(v[0]) or v[0] <= 0) else 1.0/float(v[0])
    DM_val, _ = quad(_inv_E, 0.0, z_star, limit=300, epsabs=1e-6)
    DM_star = (C_KMS / H0) * DM_val

    # R shift parameter
    R_th  = np.sqrt(Om) * DM_star * H0 / C_KMS

    # l_A acoustic parameter
    rs    = _r_s(omega_b, omega_c, h, z_star)
    if rs <= 0:
        return 1e8
    lA_th = np.pi * DM_star / rs

    # omega_b h^2
    Ob_h2 = omega_b  # OMEGA_B_FIXED is already Omega_b * h^2 (physical density)

    theory = np.array([R_th, lA_th, Ob_h2])
    delta  = theory - CMB_OBS
    return float(np.sum((delta / CMB_SIG)**2))


# ─── BAO chi2 ────────────────────────────────────────────────────────────────

def chi2_bao(E_fn, Om, H0):
    z_eff  = DESI_DR2['z_eff']
    z_grid = np.linspace(0.0, z_eff.max() + 0.01, N_GRID)
    Eg = E_fn(z_grid, Om)
    if Eg is None or not np.all(np.isfinite(Eg)):
        return 1e8
    Eg = np.maximum(Eg, 1e-15)
    DM = (C_KMS / H0) * np.concatenate([[0.], cumulative_trapezoid(1.0/Eg, z_grid)])
    tv = np.empty(13)
    for i, (z, qty) in enumerate(zip(z_eff, DESI_DR2['quantity'])):
        idx = min(np.searchsorted(z_grid, z), N_GRID-1)
        DH  = C_KMS / (H0 * Eg[idx])
        DV  = (z * DM[idx]**2 * DH)**(1./3.) if z > 0 else 0.
        if 'DV' in qty:   tv[i] = DV / R_S
        elif 'DM' in qty: tv[i] = DM[idx] / R_S
        elif 'DH' in qty: tv[i] = DH / R_S
        else:              tv[i] = np.nan
    d = DESI_DR2['value'] - tv
    if not np.all(np.isfinite(d)):
        return 1e8
    return float(d @ DESI_DR2_COV_INV @ d)


# ─── SN chi2 ─────────────────────────────────────────────────────────────────

_SN = None
def get_sn():
    global _SN
    if _SN is None:
        _SN = DESY5SN()
    return _SN

def chi2_sn(E_fn, Om, H0):
    def E_func(z):
        v = E_fn(np.array([float(z)]), Om)
        return 1e30 if (v is None or not np.isfinite(v[0])) else float(v[0])
    return get_sn().chi2(E_func, H0_km=H0)


# ─── RSD f*sigma8 chi2 ───────────────────────────────────────────────────────

Z_RSD  = np.array([0.067, 0.15, 0.38, 0.51, 0.61, 0.70, 0.85, 1.48])
FS8_OBS = np.array([0.423, 0.490, 0.497, 0.458, 0.436, 0.473, 0.315, 0.462])
FS8_SIG = np.array([0.055, 0.145, 0.045, 0.038, 0.034, 0.044, 0.095, 0.045])


def _growth_fs8(E_fn, Om, z_arr):
    """Solve linear growth ODE with modified E(z), G_eff=G."""
    z_max = max(z_arr) + 0.01
    N_g   = 800
    z_g   = np.linspace(0.0, z_max * 1.5 + 5.0, N_g)
    Eg    = E_fn(z_g, Om)
    if Eg is None or not np.all(np.isfinite(Eg)) or np.any(Eg <= 0):
        return None

    # Use N = ln(1+z) grid, forward integration from high z (z=50) to z=0
    N_ini  = np.log(51.0)   # z=50
    N_end  = np.log(1.0)    # z=0
    N_span = (N_ini, N_end)

    # E(N) interpolator where N = ln(1+z)
    N_g2   = np.log(1.0 + z_g)
    from scipy.interpolate import interp1d
    E_interp = interp1d(N_g2, Eg, fill_value='extrapolate')

    def growth_ode(N, y):
        z_loc = np.exp(N) - 1.0
        a_loc = np.exp(-N)  # a = 1/(1+z), N=ln(1+z) => a=e^{-N}
        E_val = float(E_interp(N))
        if E_val <= 0:
            return [0., 0.]
        # dE/dN numerically
        dN    = 1e-5
        dEdN  = (float(E_interp(N+dN)) - float(E_interp(N-dN))) / (2*dN)
        # Growth ODE in N=ln(1+z): D_NN = (2 - E_N/E)*D_N + (3/2)*Omega_m*D
        # Derivation: standard d²D/dt²+2H dD/dt=4piG rho_m D, convert via dN/dt=-H
        # Matter domination check: D=e^{-N}, E_N/E=3/2 → (2-3/2)(-1)+3/2=1=D_NN ✓
        Omz = 1.5 * Om * (1.0 + z_loc)**3 / E_val**2
        return [y[1],
                (2.0 - dEdN/E_val) * y[1] + Omz * y[0]]

    # Initial conditions: matter domination at high z → D ∝ a ∝ e^{-N} (decreasing with N)
    # At N_ini (z=50): D = 1/51, D' = d(1/(1+z))/dN = d(e^{-N})/dN = -e^{-N} = -1/51
    D0  = 1.0 / 51.0
    Dp0 = -D0  # dD/dN at matter domination

    sol = solve_ivp(growth_ode, N_span, [D0, Dp0],
                    method='RK45', dense_output=True,
                    rtol=1e-6, atol=1e-8, max_step=0.05)
    if not sol.success:
        return None

    # Evaluate at z_arr
    N_query = np.log(1.0 + np.asarray(z_arr))
    D_vals  = sol.sol(N_query)[0]
    Dp_vals = sol.sol(N_query)[1]  # dD/dN

    D_today = sol.sol(0.0)[0]  # at N=0 (z=0)
    if D_today <= 0 or not np.isfinite(D_today):
        return None

    D_norm  = D_vals / D_today  # D(z)/D(0)
    # f = dlnD/dlna = dlnD/d(-N) = -N' * dlnD/dN
    # N = ln(1+z), a = 1/(1+z), so ln a = -N → dlnD/dlna = -dlnD/dN = -Dp/D
    f_vals  = -Dp_vals / np.maximum(D_vals, 1e-30)

    fs8_th  = f_vals * SIGMA_8_0 * D_norm
    return fs8_th


def chi2_rsd(E_fn, Om, H0):
    fs8_th = _growth_fs8(E_fn, Om, Z_RSD)
    if fs8_th is None or not np.all(np.isfinite(fs8_th)):
        return 1e6
    return float(np.sum(((fs8_th - FS8_OBS) / FS8_SIG)**2))


# ─── Model E(z) functions ────────────────────────────────────────────────────

def _base(z_arr, Om):
    OL0   = 1.0 - Om - OR
    if OL0 <= 0 or Om <= 0:
        return None, None, None
    alpha = Om / OL0
    psi_z = 1.0 / (1.0 + alpha * (1.0 + z_arr)**3)
    psi0  = 1.0 / (1.0 + alpha)
    ratio = np.clip(psi0 / psi_z, 1.0, 200.0)
    return OL0, ratio, psi0

def E_lcdm(z_arr, Om):
    OL0 = 1.0 - Om - OR
    E2  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
    return np.sqrt(np.maximum(E2, 1e-30))

def E_model_A(z_arr, Om):
    OL0, ratio, _ = _base(z_arr, Om)
    if OL0 is None: return None
    rde = OL0 * ratio
    E2  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
    return None if np.any(E2 <= 0) else np.sqrt(E2)

def E_model_B(z_arr, Om, amp=2.5):
    OL0, ratio, _ = _base(z_arr, Om)
    if OL0 is None: return None
    g   = np.tanh(np.sqrt(np.pi/2) * np.clip(ratio - 1.0, -10, 10))
    rde = OL0 * (1.0 + amp * g)
    E2  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
    return None if np.any(E2 <= 0) else np.sqrt(E2)

def E_model_C(z_arr, Om, amp=2.5, c=1.47):
    OL0, ratio, _ = _base(z_arr, Om)
    if OL0 is None: return None
    rm1 = ratio - 1.0
    wt  = np.tanh(z_arr)
    g   = ((1.0 - wt) * np.tanh(np.sqrt(np.pi/2) * c * np.clip(rm1, -10, 10))
           + wt * rm1)
    rde = OL0 * (1.0 + amp * g)
    E2  = OR*(1+z_arr)**4 + Om*(1+z_arr)**3 + rde
    return None if np.any(E2 <= 0) else np.sqrt(E2)


# ─── Joint chi2 and AICc ─────────────────────────────────────────────────────

N_TOTAL = 13 + 3 + 1829 + 8  # 1853

def aicc(chi2, k):
    return chi2 + 2*k + 2*k*(k+1)/(N_TOTAL - k - 1)

def chi2_all(E_fn, Om, H0):
    c_bao = chi2_bao(E_fn, Om, H0)
    c_cmb = chi2_cmb(E_fn, Om, H0)
    c_sn  = chi2_sn(E_fn, Om, H0)
    c_rsd = chi2_rsd(E_fn, Om, H0)
    return c_bao, c_cmb, c_sn, c_rsd, c_bao+c_cmb+c_sn+c_rsd


def cpl_wa(E_fn, Om):
    z_arr = np.linspace(0.01, 2.0, 40)
    Ev  = E_fn(z_arr, Om)
    if Ev is None or not np.all(np.isfinite(Ev)): return None, None
    E0v = E_fn(np.array([0.0]), Om)
    if E0v is None: return None, None
    rde  = Ev**2 - OR*(1+z_arr)**4 - Om*(1+z_arr)**3
    rde0 = float(E0v[0]**2 - OR - Om)
    if rde0 <= 0 or np.any(rde <= 0): return None, None
    lnrde = np.log(rde / rde0)
    ln1z  = np.log(1 + z_arr)
    A     = np.column_stack([-3.*ln1z, -3.*(ln1z - z_arr/(1+z_arr))])
    try:
        coef, *_ = np.linalg.lstsq(A, lnrde, rcond=None)
        return float(coef[0])-1., float(coef[1])
    except Exception:
        return None, None


# ─── Optimizer ───────────────────────────────────────────────────────────────

def fit_model(name, E_fn_maker, param_names, bounds, starts_extra=None):
    """Fit model with free params. E_fn_maker(params) -> E_fn(z_arr, Om)."""
    print(f"\n[{name}] Fitting joint (BAO+CMB+SN+RSD)...")

    k = len(param_names)

    def obj(params):
        if any(p < b[0] or p > b[1] for p, b in zip(params, bounds)):
            return 1e9
        E_fn = E_fn_maker(params)
        Om, H0 = params[0], params[1]
        c_bao, c_cmb, c_sn, c_rsd, tot = chi2_all(E_fn, Om, H0)
        return tot

    # Build starts — dense around Om~0.28-0.33, H0~66-72
    starts = []
    for Om0 in [0.28, 0.295, 0.305, 0.315, 0.325]:
        for H0_0 in [66., 68., 70., 72.]:
            row = [Om0, H0_0] + [(b[0]+b[1])/2 for b in bounds[2:]]
            starts.append(row)

    best_val, best_par = 1e9, None
    for s in starts:
        try:
            r = minimize(obj, s, method='Nelder-Mead',
                         options={'xatol':1e-4, 'fatol':1e-4, 'maxiter':500})
            if r.fun < best_val:
                best_val, best_par = r.fun, r.x
        except Exception:
            pass

    # Refine best with tighter tolerance
    if best_par is not None:
        try:
            r = minimize(obj, best_par, method='Nelder-Mead',
                         options={'xatol':1e-6, 'fatol':1e-6, 'maxiter':2000})
            if r.fun < best_val:
                best_val, best_par = r.fun, r.x
        except Exception:
            pass

    try:
        r = differential_evolution(obj, bounds, seed=42, maxiter=100,
                                   tol=1e-5, popsize=6, workers=1)
        if r.fun < best_val:
            best_val, best_par = r.fun, r.x
    except Exception:
        pass

    if best_par is None:
        print(f"  FAILED")
        return None

    E_fn    = E_fn_maker(best_par)
    Om, H0  = best_par[0], best_par[1]
    c_bao, c_cmb, c_sn, c_rsd, c_tot = chi2_all(E_fn, Om, H0)
    ac      = aicc(c_tot, k)
    w0, wa  = cpl_wa(E_fn, Om)
    h0_tension = (73.04 - H0) / np.sqrt(1.04**2 + 0.5**2)  # vs SH0ES

    param_str = ', '.join(f'{pn}={v:.4f}' for pn, v in zip(param_names, best_par))
    print(f"  {param_str}")
    print(f"  chi2_BAO={c_bao:.4f}  chi2_CMB={c_cmb:.4f}  chi2_SN={c_sn:.4f}  chi2_RSD={c_rsd:.4f}")
    print(f"  chi2_joint={c_tot:.4f}  AICc={ac:.4f}")
    print(f"  w0={w0}  wa={wa}  H0_tension={h0_tension:.2f}sigma")

    return {
        'name': name, 'k': k,
        'params': {n: float(v) for n, v in zip(param_names, best_par)},
        'chi2_bao': c_bao, 'chi2_cmb': c_cmb, 'chi2_sn': c_sn, 'chi2_rsd': c_rsd,
        'chi2_joint': c_tot, 'aicc': ac,
        'w0': w0, 'wa': wa,
        'H0_tension_vs_shoes': h0_tension,
    }


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    t0 = time.time()
    print("="*60)
    print("L35: Multi-probe joint fit (BAO+CMB+SN+RSD)")
    print(f"n_total={N_TOTAL} (BAO:13 + CMB:3 + SN:1829 + RSD:8)")
    print("="*60)

    print("\nLoading DESY5 SN data...")
    sn = get_sn()
    print(f"  Loaded {sn.N} SNe")

    # Verify BAO chi2 at LCDM Planck values
    c_bao_check = chi2_bao(E_lcdm, 0.315, 67.36)
    c_cmb_check = chi2_cmb(E_lcdm, 0.315, 67.36)
    print(f"\n[VERIFY LCDM Planck] chi2_BAO={c_bao_check:.4f} (ref~10.8)  chi2_CMB={c_cmb_check:.4f} (ref~0-3)")

    # LCDM baseline
    res_lcdm = fit_model(
        'LCDM', lambda p: (lambda z, Om: E_lcdm(z, p[0])),
        ['Om', 'H0'], [(0.15, 0.50), (55., 82.)]
    )

    # Model A (k=2)
    res_A = fit_model(
        'Model_A', lambda p: (lambda z, Om: E_model_A(z, p[0])),
        ['Om', 'H0'], [(0.15, 0.50), (55., 82.)]
    )

    # Model B (k=3)
    res_B = fit_model(
        'Model_B', lambda p: (lambda z, Om: E_model_B(z, p[0], amp=p[2])),
        ['Om', 'H0', 'amp'], [(0.15, 0.50), (55., 82.), (0.1, 5.0)]
    )

    # Model C (k=4)
    res_C = fit_model(
        'Model_C', lambda p: (lambda z, Om: E_model_C(z, p[0], amp=p[2], c=p[3])),
        ['Om', 'H0', 'amp', 'c'], [(0.15, 0.50), (55., 82.), (0.1, 5.0), (0.5, 3.0)]
    )

    # ─── Summary ─────────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    lcdm_aicc = res_lcdm['aicc'] if res_lcdm else None
    for res, label in [(res_lcdm, 'LCDM'), (res_A, 'A'), (res_B, 'B'), (res_C, 'C')]:
        if res is None:
            print(f"\n{label}: FAILED")
            continue
        d_aicc = (res['aicc'] - lcdm_aicc) if (lcdm_aicc and label != 'LCDM') else 0.
        verdict = ''
        if label == 'LCDM':
            verdict = 'baseline'
        elif d_aicc < -4:
            verdict = 'Q92 GAME'
        elif d_aicc < -2:
            verdict = 'Q91 STRONG'
        elif d_aicc < 0:
            verdict = 'Q90 PASS'
        else:
            verdict = 'K90 KILL'
        wa_ok = res['wa'] is not None and res['wa'] < 0

        print(f"\n{label} ({res['name']}) k={res['k']}:")
        print(f"  chi2: BAO={res['chi2_bao']:.2f}  CMB={res['chi2_cmb']:.2f}  "
              f"SN={res['chi2_sn']:.2f}  RSD={res['chi2_rsd']:.2f}  total={res['chi2_joint']:.2f}")
        print(f"  AICc={res['aicc']:.2f}  ΔAICc={d_aicc:+.2f}")
        print(f"  {res['params']}")
        print(f"  w0={res['w0']}  wa={res['wa']}  wa<0: {wa_ok}")
        print(f"  H0 tension vs SH0ES: {res['H0_tension_vs_shoes']:.2f}σ")
        print(f"  VERDICT: {verdict}")

    # Save
    out = {'LCDM': res_lcdm, 'A': res_A, 'B': res_B, 'C': res_C,
           'n_total': N_TOTAL, 'elapsed_s': time.time()-t0}
    out_path = os.path.join(_SCRIPT_DIR, 'l35_results.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2, default=lambda x: None)
    print(f"\nSaved to {out_path}")
    print(f"Total elapsed: {time.time()-t0:.1f}s")


if __name__ == '__main__':
    main()
