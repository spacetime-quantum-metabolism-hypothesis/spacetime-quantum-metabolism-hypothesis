# -*- coding: utf-8 -*-
"""
L13-U Round 3: Comprehensive uniqueness analysis.

Tests:
1. Is rho_DE = OL0*(1 + A*(1-a)) the right functional form?
2. What about rho_DE = OL0*(1 + A*(1-a^n))?
3. What about rho_DE = OL0*exp(A*(1-a))?
4. AIC/BIC comparison of all functional forms.
"""
from __future__ import annotations
import os
import json
import numpy as np
from scipy.optimize import minimize
from scipy.interpolate import interp1d

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')

_THIS = os.path.dirname(os.path.abspath(__file__))

OMEGA_R = 9.1e-5
c_SI = 2.998e8
Mpc_m = 3.086e22
rs_drag = 147.09

DESI_Z = np.array([0.295, 0.510, 0.706, 0.930, 1.317, 1.491, 2.330])
DESI_OBS = np.array([7.93, 13.62, 16.85, 21.71, 27.79, 30.21, 39.71])
DESI_ERR = np.array([0.15, 0.17, 0.22, 0.22, 0.55, 0.49, 0.94])
N_DATA = 7


def compute_DM(z_arr, Om, h, rho_func):
    H0 = h * 100e3 / Mpc_m
    z_int = np.linspace(0, max(z_arr)*1.001, 2000)
    a_int = 1.0 / (1.0 + z_int)
    rho = np.array([rho_func(a) for a in a_int])
    E2 = OMEGA_R*(1+z_int)**4 + Om*(1+z_int)**3 + rho
    E2 = np.where(E2 > 1e-10, E2, 1e-10)
    integrand = 1.0 / np.sqrt(E2)
    cumul = np.zeros(len(z_int))
    for i in range(1, len(z_int)):
        cumul[i] = np.trapezoid(integrand[:i+1], z_int[:i+1])
    chi_func = interp1d(z_int, cumul, kind='cubic', fill_value='extrapolate')
    return (c_SI/H0)/Mpc_m * chi_func(z_arr)


def compute_DV(z, Om, h, rho_func):
    H0 = h * 100e3 / Mpc_m
    a = 1.0 / (1.0+z)
    rho = rho_func(a)
    E2 = OMEGA_R*(1+z)**4 + Om*(1+z)**3 + rho
    E2 = max(float(E2), 1e-10)
    DH = c_SI/(H0*np.sqrt(E2)) / Mpc_m
    DM = compute_DM(np.array([z]), Om, h, rho_func)[0]
    return (z*DM**2*DH)**(1.0/3.0)


def chi2_model(Om, h, rho_func):
    try:
        pred_0 = compute_DV(0.295, Om, h, rho_func) / rs_drag
        DM_arr = compute_DM(DESI_Z[1:], Om, h, rho_func)
        pred = np.concatenate([[pred_0], DM_arr/rs_drag])
        resid = pred - DESI_OBS
        c2 = float(np.sum((resid/DESI_ERR)**2))
        return c2 if np.isfinite(c2) else 1e8
    except Exception:
        return 1e8


def fit_fixed_form(rho_maker_fixed):
    """Fit Om, h with fixed functional form (0 extra params)."""
    best = (1e8, None)
    for Om0, h0 in [(0.310, 0.677), (0.305, 0.680), (0.315, 0.673)]:
        def neg_ll(theta):
            Om, h = theta
            if Om < 0.25 or Om > 0.40 or h < 0.60 or h > 0.75: return 1e8
            return chi2_model(Om, h, rho_maker_fixed(Om))
        res = minimize(neg_ll, [Om0, h0], method='Nelder-Mead',
                       options={'xatol':1e-5, 'fatol':0.01, 'maxiter':2000})
        if res.fun < best[0]:
            best = (res.fun, res.x)
    if best[1] is None: return 0.31, 0.677, 1e8
    return float(best[1][0]), float(best[1][1]), float(best[0])


def fit_free_param(rho_maker_free, p0_list, bounds_p=(-5, 5)):
    """Fit Om, h, p (1 extra param) with free functional form."""
    best = (1e8, None)
    for Om0, h0 in [(0.310, 0.677), (0.305, 0.680), (0.315, 0.673)]:
        for p0 in p0_list:
            def neg_ll(theta):
                Om, h, p = theta
                if Om<0.25 or Om>0.40 or h<0.60 or h>0.75: return 1e8
                if p < bounds_p[0] or p > bounds_p[1]: return 1e8
                return chi2_model(Om, h, rho_maker_free(Om, p))
            res = minimize(neg_ll, [Om0, h0, p0], method='Nelder-Mead',
                           options={'xatol':1e-5, 'fatol':0.01, 'maxiter':3000})
            if res.fun < best[0]:
                best = (res.fun, res.x)
    if best[1] is None: return 0.31, 0.677, 0.0, 1e8
    return float(best[1][0]), float(best[1][1]), float(best[1][2]), float(best[0])


def main():
    print('=== L13-U Round 3: Uniqueness Comprehensive ===')
    print()

    models = {}

    # 0. LCDM
    Om_lc, h_lc, c2_lc = fit_fixed_form(
        lambda Om: (lambda a: 1.0-Om-OMEGA_R))
    models['LCDM'] = {'Om':Om_lc,'h':h_lc,'chi2':c2_lc,'k':2,'label':'LCDM (A=0)'}

    # 1. A01: rho_DE = OL0*(1+Om*(1-a)), A=Om theory-fixed
    Om_a1, h_a1, c2_a1 = fit_fixed_form(
        lambda Om: (lambda a: (1-Om-OMEGA_R)*(1+Om*(1-a))))
    models['A01'] = {'Om':Om_a1,'h':h_a1,'chi2':c2_a1,'k':2,'label':'A01 A=Om (SQMH)'}

    # 2. Free A: rho_DE = OL0*(1+A*(1-a)), A free
    Om_f2, h_f2, A_f2, c2_f2 = fit_free_param(
        lambda Om, A: (lambda a: (1-Om-OMEGA_R)*(1+A*(1-a))),
        p0_list=[0.3, 1.0, 2.0], bounds_p=(-1.0, 5.0))
    models['FreeA'] = {'Om':Om_f2,'h':h_f2,'A':A_f2,'chi2':c2_f2,'k':3,
                       'label':'Free-A (1+A*(1-a))'}

    # 3. Power-law: rho_DE = OL0*(1+Om*(1-a^n)), n free
    Om_f3, h_f3, n_f3, c2_f3 = fit_free_param(
        lambda Om, n: (lambda a: (1-Om-OMEGA_R)*(1+Om*(1-a**max(n,0.01)))),
        p0_list=[1.0, 0.5, 2.0], bounds_p=(0.01, 5.0))
    models['PowerN'] = {'Om':Om_f3,'h':h_f3,'n':n_f3,'chi2':c2_f3,'k':3,
                        'label':'Power-n (1+Om*(1-a^n))'}

    # 4. Exponential: rho_DE = OL0*exp(Om*(1-a)), amplitude=Om theory-fixed
    Om_f4, h_f4, c2_f4 = fit_fixed_form(
        lambda Om: (lambda a: (1-Om-OMEGA_R)*np.exp(Om*(1-a))))
    models['ExpOm'] = {'Om':Om_f4,'h':h_f4,'chi2':c2_f4,'k':2,
                       'label':'Exp-Om (OL0*exp(Om*(1-a)))'}

    # 5. Free exponential: rho_DE = OL0*exp(A*(1-a)), A free
    Om_f5, h_f5, A_f5, c2_f5 = fit_free_param(
        lambda Om, A: (lambda a: (1-Om-OMEGA_R)*np.exp(A*(1-a))),
        p0_list=[0.3, 1.0], bounds_p=(-1.0, 3.0))
    models['FreeExp'] = {'Om':Om_f5,'h':h_f5,'A':A_f5,'chi2':c2_f5,'k':3,
                         'label':'Free-Exp (OL0*exp(A*(1-a)))'}

    print('Model comparison:')
    print('%-25s  Om      h      chi2    AIC     BIC     Dchi2' % 'Model')
    print('-'*80)
    for name, m in models.items():
        k = m['k']
        aic = m['chi2'] + 2*k
        bic = m['chi2'] + k*np.log(N_DATA)
        dchi2 = m['chi2'] - c2_lc
        print('%-25s  %.4f  %.4f  %6.3f  %6.3f  %6.3f  %6.3f' % (
            m['label'][:25], m['Om'], m['h'], m['chi2'], aic, bic, dchi2))
        m['AIC'] = float(aic)
        m['BIC'] = float(bic)
        m['dchi2_vs_lcdm'] = float(dchi2)
        if 'A' in m: print('   A=' + str(round(m['A'], 3)))
        if 'n' in m: print('   n=' + str(round(m['n'], 3)))

    print()
    # Which model is AIC best?
    aic_best = min(m['AIC'] for m in models.values())
    bic_best = min(m['BIC'] for m in models.values())
    for name, m in models.items():
        if m['AIC'] == aic_best: print('AIC best: ' + m['label'])
        if m['BIC'] == bic_best: print('BIC best: ' + m['label'])

    # Does A01 uniquely predict A01?
    a01_aic_rank = sorted(models.values(), key=lambda x: x['AIC']).index(models['A01']) + 1
    print()
    print('A01 AIC rank: ' + str(a01_aic_rank) + ' out of ' + str(len(models)))

    results = {k: {kk: (float(vv) if isinstance(vv, (int, float, np.floating)) else vv)
                   for kk, vv in v.items()} for k, v in models.items()}
    results['a01_aic_rank'] = a01_aic_rank

    out_path = os.path.join(_THIS, 'l13_uniqueness_r3_results.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print('Results saved to: ' + out_path)
    return results


if __name__ == '__main__':
    main()
