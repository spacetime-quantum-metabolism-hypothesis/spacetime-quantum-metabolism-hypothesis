"""
L380 — P17 Tier B  V(n,t) extension toy.

V(n,t) = V_0 + (1/2) m_n^2 n^2  (slow-roll-like mass term).

Background ODE in N=ln a, units M_Pl=1, H_0=1.
  Friedmann (closure):  E^2 = Om*a^-3 + Or*a^-4 + (1/2) E^2 nN^2 + v(n)/(3),
  where v(n) = V/H_0^2/M_Pl^2 = v0 + 0.5*mu^2 * n^2  (mu=m_n/H_0).
  So  E^2 (1 - 0.5 nN^2) = Om*a^-3 + Or*a^-4 + v(n)/3.
  KG:  n_NN + (3 + EN/E) n_N + (1/E^2) v_n /  ... carefull:
       n_dd + 3 H n_d + V_n = 0.
       d/dt = H d/dN.  n_d = H n_N. n_dd = H^2 (n_NN + (EN/E) n_N).
       =>  n_NN + (3 + EN/E) n_N + V_n/(H^2) = 0
       V_n / H^2 = mu^2 * n / E^2.

Initial (z=20-ish, N_ini=-3): thawing => n=n_i, n_N=0. v0 fixed by closure at N=0.

Procedure:
  - For trial v0, integrate forward; iterate v0 by bisection so that E(N=0)=1.
  - Compute D_M(z), D_H(z) integrals; chi^2 vs DESI DR2 with full cov.
  - Extract w(z) = p_de/rho_de from rho_de_eff = 3 E^2 - 3 Om a^-3 - 3 Or a^-4.
  - CPL fit (w0, wa) on z in [0.01, 1.2].
"""

from __future__ import annotations
import os, sys, json, time, math
os.environ['OMP_NUM_THREADS']='1'; os.environ['MKL_NUM_THREADS']='1'; os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np
from scipy.integrate import solve_ivp, cumulative_trapezoid
from scipy.optimize import least_squares, minimize, brentq
import multiprocessing as mp

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'simulations'))
from desi_data import DESI_DR2, DESI_DR2_COV_INV  # 13 pts, full cov

C_KMS = 299792.458  # km/s
RD_FID = 147.05     # Mpc, DESI fiducial r_d (we treat as fixed; alpha-marginalize variant possible)

# Radiation density (3 nu, omega_r0 ~ 4.18e-5 / h^2 -> small but kept)
def Omega_r0(h):
    return 4.183e-5 / (h*h)

def integrate_background(Om, h, mu, n_i, v0_trial,
                         N_min=-5.0, N_max=0.0, n_pts=2000):
    """Return (N, E, n, nN) over grid; or None if unphysical."""
    Or = Omega_r0(h)
    def rhs(N, y):
        n, nN = y
        try:
            a = math.exp(N)
        except OverflowError:
            return [0.0, 0.0]
        v = v0_trial + 0.5*mu*mu*n*n
        # E^2 = (Om*a^-3 + Or*a^-4 + v/3) / (1 - 0.5 nN^2)
        denom = 1.0 - 0.5*nN*nN
        if denom <= 1e-3 or not math.isfinite(denom):
            return [0.0, 0.0]
        if not (math.isfinite(n) and math.isfinite(nN)):
            return [0.0, 0.0]
        num = Om*a**-3 + Or*a**-4 + v/3.0
        E2 = num/denom
        if E2 <= 0:
            return [0.0, 0.0]
        E = math.sqrt(E2)
        # E_N: differentiate E^2; from KG we need EN/E.
        # d(E^2)/dN = -3 Om a^-3 - 4 Or a^-4 + (1/3) v_N / (1-0.5 nN^2) + (E^2)*(0.5 *2 nN nNN)/(1-0.5 nN^2)
        # Avoid implicit: use Friedmann derivative identity:
        #   2 E EN = -3 Om a^-3 - 4 Or a^-4 + (mu^2 n nN)/3 / denom + E^2 * (nN nNN)/denom + (num/denom^2)*(nN nNN)
        # Simpler: substitute KG and Raychaudhuri. Use:
        # 2 H Hd = -(rho+p)*1.  in N: 2 E EN = -3*(rho+p)/rho_crit0 in units; rho_crit0=3.
        # rho+p (in 3H0^2 units) = Om a^-3 + (4/3) Or a^-4 + E^2 nN^2
        rho_plus_p = Om*a**-3 + (4.0/3.0)*Or*a**-4 + E2*nN*nN
        EN = -1.5 * rho_plus_p / E
        # n_NN = -(3 + EN/E) nN - mu^2 n / E^2
        nNN = -(3.0 + EN/E)*nN - mu*mu*n/E2
        return [nN, nNN]

    y0 = [n_i, 0.0]
    try:
        sol = solve_ivp(rhs, (N_min, N_max), y0, method='RK45',
                        t_eval=np.linspace(N_min, N_max, n_pts),
                        rtol=1e-7, atol=1e-9, max_step=0.05)
    except Exception:
        return None
    if not sol.success or sol.t.size < n_pts:
        return None
    N = sol.t
    n_arr = sol.y[0]; nN_arr = sol.y[1]
    a = np.exp(N)
    v = v0_trial + 0.5*mu*mu*n_arr*n_arr
    denom = 1.0 - 0.5*nN_arr*nN_arr
    if np.any(denom <= 1e-6):
        return None
    num = Om*a**-3 + Or*a**-4 + v/3.0
    E2 = num/denom
    if np.any(E2 <= 0) or np.any(~np.isfinite(E2)):
        return None
    E = np.sqrt(E2)
    return N, E, n_arr, nN_arr

def closure_v0(Om, h, mu, n_i):
    """Find v0 so that E(N=0) = 1."""
    def f(v0):
        res = integrate_background(Om, h, mu, n_i, v0)
        if res is None:
            return 1e3
        _, E, _, _ = res
        return E[-1] - 1.0
    # bracket
    try:
        # increasing v0 increases E -> bracket
        a, b = 0.0, 3.0
        fa, fb = f(a), f(b)
        if fa*fb > 0:
            # widen
            for hi in [5.0, 10.0, 20.0]:
                fb = f(hi); b=hi
                if fa*fb<0: break
            else:
                return None
        v0 = brentq(f, a, b, xtol=1e-6)
        return v0
    except Exception:
        return None

def comoving_DM(z_target, N, E, h):
    """Return D_M(z)/r_d-like; full Mpc. We compute c/H0 * integral dz'/E(z') from 0 to z."""
    # Build z from N: z = e^-N - 1, increasing as N decreases.
    z_arr = np.exp(-N) - 1.0  # decreasing then 0 at N=0, increases as N decreases
    # We want ascending z. Reverse arrays.
    idx = np.argsort(z_arr)
    z_s = z_arr[idx]; E_s = E[idx]
    # cumulative integral of 1/E from z=0 upward
    integrand = 1.0/E_s
    DC = cumulative_trapezoid(integrand, z_s, initial=0.0)  # in units of c/H0
    # interpolate at z_target
    DM = np.interp(z_target, z_s, DC) * (C_KMS/(100.0*h))  # Mpc
    DH = (C_KMS/(100.0*h)) / np.interp(z_target, z_s, E_s)
    return DM, DH

def chi2_desi(Om, h, mu, n_i):
    v0 = closure_v0(Om, h, mu, n_i)
    if v0 is None:
        return None, None, None
    res = integrate_background(Om, h, mu, n_i, v0)
    if res is None:
        return None, None, None
    N, E, n_arr, nN_arr = res
    z_eff = DESI_DR2['z_eff']
    quants = DESI_DR2['quantity']
    obs = DESI_DR2['value']
    model = np.zeros_like(obs)
    DM_arr, DH_arr = comoving_DM(z_eff, N, E, h)
    for i, (z, q) in enumerate(zip(z_eff, quants)):
        DM, DH = DM_arr[i], DH_arr[i]
        DV = (z * DM*DM * DH)**(1.0/3.0)
        if q == 'DV_over_rs':
            model[i] = DV / RD_FID
        elif q == 'DM_over_rs':
            model[i] = DM / RD_FID
        elif q == 'DH_over_rs':
            model[i] = DH / RD_FID
    d = obs - model
    chi2 = float(d @ DESI_DR2_COV_INV @ d)
    # compute w(z) and CPL
    return chi2, (N, E, n_arr, nN_arr, v0), model

def w_and_cpl(N, E, n_arr, nN_arr, v0, Om, h, mu):
    a = np.exp(N)
    Or = Omega_r0(h)
    # rho_de in units of 3H0^2 = E^2 - Om a^-3 - Or a^-4
    rho_de = E*E - Om*a**-3 - Or*a**-4
    # K = 0.5 * (H/H0)^2 * nN^2 in units 3H0^2: K_norm = 0.5 E^2 nN^2 / 3
    # but rho_n in units 3H0^2: rho_n = (1/2) E^2 nN^2 + (v/3) actually our v is V/H0^2/MPl^2
    # rho_n_norm = (1/2 E^2 nN^2)/3 + v/9 ... let's just compute p/rho directly:
    # K = 0.5 (H n_N H)^2 ...units: rho_n in M_pl^2 H^2 units = ...
    # Use ratio K-V over K+V (units cancel): w_de = (K - V) / (K + V).
    K = 0.5 * (E*E) * nN_arr*nN_arr  # in units H_0^2 (×M_Pl^2 implied)
    V = (v0 + 0.5*mu*mu*n_arr*n_arr)  # same units
    w = (K - V) / (K + V + 1e-30)
    z_arr = 1.0/a - 1.0
    # CPL fit on 0.01 < z < 1.2
    mask = (z_arr > 0.01) & (z_arr < 1.2)
    zfit = z_arr[mask]; wfit = w[mask]
    def res_cpl(p):
        w0, wa = p
        return (w0 + wa*zfit/(1.0+zfit)) - wfit
    sol = least_squares(res_cpl, [-0.95, 0.0])
    w0, wa = float(sol.x[0]), float(sol.x[1])
    return w0, wa, float(w[-1])  # w_today

# === LCDM reference chi^2 for context ===
def chi2_lcdm(Om, h):
    Or = Omega_r0(h)
    z_eff = DESI_DR2['z_eff']
    quants = DESI_DR2['quantity']
    obs = DESI_DR2['value']
    z_dense = np.linspace(0.0, 3.0, 5000)
    E_dense = np.sqrt(Om*(1+z_dense)**3 + Or*(1+z_dense)**4 + (1.0-Om-Or))
    DC = cumulative_trapezoid(1.0/E_dense, z_dense, initial=0.0)
    DH0 = C_KMS/(100.0*h)
    DM_arr = np.interp(z_eff, z_dense, DC)*DH0
    DH_arr = DH0/np.interp(z_eff, z_dense, E_dense)
    model = np.zeros_like(obs)
    for i,(z,q) in enumerate(zip(z_eff, quants)):
        DV = (z*DM_arr[i]**2*DH_arr[i])**(1.0/3.0)
        if q=='DV_over_rs': model[i]=DV/RD_FID
        elif q=='DM_over_rs': model[i]=DM_arr[i]/RD_FID
        else: model[i]=DH_arr[i]/RD_FID
    d = obs - model
    return float(d @ DESI_DR2_COV_INV @ d)

# === Worker ===
def worker(args):
    Om, h, mu, n_i = args
    try:
        out = chi2_desi(Om, h, mu, n_i)
        if out[0] is None:
            return (Om, h, mu, n_i, None, None, None, None)
        chi2, sol_pack, model = out
        N, E, n_arr, nN_arr, v0 = sol_pack
        w0, wa, w_today = w_and_cpl(N, E, n_arr, nN_arr, v0, Om, h, mu)
        return (Om, h, mu, n_i, chi2, w0, wa, w_today)
    except Exception as e:
        return (Om, h, mu, n_i, None, None, None, str(e))

def main():
    t0 = time.time()
    print('[L380] V(n,t) toy DESI DR2 chi^2 scan')
    # LCDM baseline
    from scipy.optimize import minimize_scalar
    def lcdm_chi2_h(Om):
        r = minimize(lambda h: chi2_lcdm(Om, h[0]), x0=[0.68], bounds=[(0.60,0.78)])
        return r.fun, r.x[0]
    r = minimize(lambda Om: lcdm_chi2_h(Om[0])[0], x0=[0.32], bounds=[(0.25,0.40)])
    Om_lcdm = float(r.x[0])
    chi2_l, h_lcdm = lcdm_chi2_h(Om_lcdm)
    print(f'  LCDM best: Om={Om_lcdm:.4f} h={h_lcdm:.4f}  chi^2={chi2_l:.3f}')

    # Coarse grid scan
    Om_grid = np.linspace(0.27, 0.36, 10)
    h_grid  = np.linspace(0.64, 0.72, 9)
    mu_grid = np.linspace(0.0, 3.0, 13)
    ni_grid = np.array([0.10, 0.30, 0.60, 1.00, 1.50, 2.00])
    args_list = [(Om, h, mu, ni) for Om in Om_grid for h in h_grid
                                  for mu in mu_grid for ni in ni_grid]
    print(f'  scanning {len(args_list)} points across 9 workers...')
    ctx = mp.get_context('spawn')
    with ctx.Pool(9) as pool:
        results = pool.map(worker, args_list)

    # collect best
    valid = [r for r in results if r[4] is not None and isinstance(r[4],(int,float))]
    valid.sort(key=lambda r: r[4])
    best = valid[0] if valid else None
    print(f'  valid={len(valid)} / {len(results)}')

    out = {
        'lcdm': {'Om': Om_lcdm, 'h': h_lcdm, 'chi2': chi2_l},
        'desi_box': {'w0': [-0.815, -0.699], 'wa': [-1.07, -0.59]},
        'top10': [
            dict(Om=r[0], h=r[1], mu=r[2], n_i=r[3], chi2=r[4],
                 w0=r[5], wa=r[6], w_today=r[7])
            for r in valid[:10]
        ],
        'best': None,
        'summary': {},
        'runtime_s': None,
    }
    if best:
        Om,h,mu,ni,chi2,w0,wa,w_today = best
        out['best'] = dict(Om=Om, h=h, mu=mu, n_i=ni,
                           chi2=chi2, w0=w0, wa=wa, w_today=w_today)
        # consistency vs DESI box
        in_w0 = (-0.815 <= w0 <= -0.699)
        in_wa = (-1.07 <= wa <= -0.59)
        out['summary'] = {
            'delta_chi2_vs_lcdm': chi2 - chi2_l,
            'in_w0_box': bool(in_w0),
            'in_wa_box': bool(in_wa),
            'box_consistent': bool(in_w0 and in_wa),
            'pass_chi2_threshold_17': bool(chi2 <= 17.0),
        }
        print(f'  BEST: Om={Om:.3f} h={h:.3f} mu={mu:.3f} n_i={ni:.2f}')
        print(f'        chi^2={chi2:.3f}  w0={w0:.3f} wa={wa:.3f} w_today={w_today:.3f}')
        print(f'        DELTA vs LCDM = {chi2-chi2_l:+.3f}')
        print(f'        DESI box (w0,wa) consistent: {in_w0 and in_wa}')
    out['runtime_s'] = time.time()-t0
    out_path = os.path.join(ROOT, 'results', 'L380', 'report.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'  wrote {out_path}  (t={out["runtime_s"]:.1f}s)')

if __name__ == '__main__':
    mp.set_start_method('spawn', force=True)
    main()
