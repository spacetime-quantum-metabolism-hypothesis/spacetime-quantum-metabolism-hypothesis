# -*- coding: utf-8 -*-
"""
Phase 2 joint chi^2 fit: DESI DR2 BAO + DESY5 SN + compressed Planck CMB.

Models compared:
  LCDM          : 1 free param (Omega_m)
  Fluid IDE     : 1 free param (xi_q)          -- SQMH background toy
  V_RP          : 2 free params (beta, n)      -- Ratra-Peebles quintessence
  V_exp         : 2 free params (beta, lambda) -- exponential quintessence

Output: AIC / BIC table, figure 12_phase2_joint.png.

Notes:
  - r_d (sound horizon) fixed at CMB-preferred 147.09 Mpc as in Phase 1
    (BAO alone can't pin r_d). The compressed CMB term independently
    constrains theta* and thus r_d implicitly.
  - omega_b, omega_c carried as nuisance with Planck priors (not
    marginalised; fixed to best-fit Planck values for scaffolding speed).
"""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))  # simulations/
sys.path.insert(0, HERE)

import config
import desi_data
import desi_fitting as df   # reuse chi2 and E_sqmh_ode
import quintessence as qn
import compressed_cmb as ccmb
import sn_likelihood as snl
import rsd_likelihood as rsd


R_D = 147.09  # Mpc, CMB-preferred
N_BAO = 13    # DESI DR2 uses 13 data points

SN = snl.DESY5SN()
print(f"[Phase 2] Loaded {SN.N} DESY5 SNe")


class _CallableWrapper:
    """Wrap a bare E(z) function so it accepts *args (df.chi2 passes them)."""

    def __init__(self, f):
        self._f = f

    def __call__(self, z, *args):
        return float(self._f(z))


class _HighZBridge:
    """
    Combine a low-z E(z) (valid for z < Z_CUT) with a high-z LCDM-like
    extrapolation. Used for compressed-CMB integration that needs E(z) up
    to z_star ~ 1090, because Phase-1/desi_fitting solvers only run to
    z ~ 1.5-3.

    The bridge assumes that any SQMH / V(phi) coupling is negligible for
    z > Z_CUT (coupling Q ~ rho_DE * rho_m / H vanishes when Omega_DE/Omega_m
    << 1). In that regime the universe is matter+radiation, so LCDM with
    the same Omega_m matches to ~0.1%.
    """

    def __init__(self, low_z_E, Z_CUT=2.5):
        self._low = low_z_E
        self._zcut = Z_CUT
        # Pure LCDM tail at z > Z_CUT (no rescale). Rescaling with
        # e_low/e_high contaminates theta* for extreme V_RP params where
        # the coupled E(z=2.5) drifts from the LCDM value — the backward
        # ODE phi_N can approach the phantom edge and inject a spurious
        # multiplicative factor into the sound-horizon integrand out to
        # z_star ~ 1090. Phase 3 adopted the pure-LCDM tail and Phase 2
        # must match.
        Om = config.Omega_m
        Or = config.Omega_r
        OL = config.Omega_DE

        def E_lcdm(z):
            return np.sqrt(Or * (1 + z)**4 + Om * (1 + z)**3 + OL)

        self._Elcdm = E_lcdm

    def __call__(self, z, *args):
        if z <= self._zcut:
            return float(self._low(z))
        return self._Elcdm(z)


def _bao_chi2_E(E_func):
    """BAO chi^2 for arbitrary E(z). df.chi2 expects a callable E(z,*args)."""
    try:
        return df.chi2(_CallableWrapper(E_func), R_D)
    except Exception:
        return np.nan


def _cmb_chi2_E(E_func):
    """Compressed CMB chi^2. Bridges low-z coupled E(z) onto LCDM high-z
    for the sound-horizon / angular-scale integration."""
    h = config.H_0_km / 100.0
    bridged = _HighZBridge(E_func)
    return ccmb.chi2_compressed_cmb(ccmb.OMEGA_B_OBS, ccmb.OMEGA_C_OBS,
                                    h, bridged)


def _sn_chi2_E(E_func):
    return SN.chi2(E_func, H0_km=config.H_0_km)


def chi2_total(E_func, rsd_chi2=0.0):
    """Joint chi^2 = BAO + SN + CMB (+ RSD if provided).
    RSD is computed outside (needs growth info, not just E)."""
    c_bao = _bao_chi2_E(E_func)
    c_sn = _sn_chi2_E(E_func)
    c_cmb = _cmb_chi2_E(E_func)
    tot = c_bao + c_sn + c_cmb + rsd_chi2
    return c_bao, c_sn, c_cmb, rsd_chi2, tot


# ---- Model evaluation ----
def E_lcdm_factory(Om):
    def E(z):
        return np.sqrt(Om * (1 + z)**3 + (1 - Om))
    return E


def fit_lcdm():
    def cost(p):
        Om = float(p[0])
        if not 0.1 < Om < 0.6:
            return 1e6
        c_rsd = rsd.chi2_lcdm(Om)
        _, _, _, _, tot = chi2_total(E_lcdm_factory(Om), rsd_chi2=c_rsd)
        return tot
    res = minimize(cost, [0.315], method='Nelder-Mead',
                   options={'xatol': 1e-5, 'fatol': 1e-3})
    Om = float(res.x[0])
    c_rsd = rsd.chi2_lcdm(Om)
    parts = chi2_total(E_lcdm_factory(Om), rsd_chi2=c_rsd)
    return {'model': 'LCDM', 'k': 1, 'params': {'Om': Om},
            'chi2_bao': parts[0], 'chi2_sn': parts[1],
            'chi2_cmb': parts[2], 'chi2_rsd': parts[3], 'chi2': parts[4]}


def E_quintessence_factory(family, beta, extra):
    E = qn.E_quintessence(family, beta, extra)
    if not E.ok:
        return None
    return E


def fit_quintessence(family, p0_list, bounds):
    best = (1e8, None, None)
    for p0 in p0_list:
        def cost(p):
            for (lo, hi), v in zip(bounds, p):
                if not (lo <= v <= hi):
                    return 1e6
            beta = float(p[0])
            extra = tuple(float(x) for x in p[1:])
            E = E_quintessence_factory(family, beta, extra)
            if E is None:
                return 1e6
            c_rsd = rsd.chi2_quintessence(family, beta, extra)
            if not np.isfinite(c_rsd):
                c_rsd = 1e3  # penalize growth failure
            _, _, _, _, tot = chi2_total(E, rsd_chi2=c_rsd)
            if not np.isfinite(tot):
                return 1e6
            return tot
        try:
            res = minimize(cost, p0, method='Nelder-Mead',
                           options={'xatol': 1e-4, 'fatol': 1e-2,
                                    'maxiter': 400})
            if res.fun < best[0]:
                best = (res.fun, res.x, None)
        except Exception:
            continue
    if best[1] is None:
        return None
    beta = float(best[1][0])
    extra = tuple(float(x) for x in best[1][1:])
    E = E_quintessence_factory(family, beta, extra)
    c_rsd = rsd.chi2_quintessence(family, beta, extra)
    parts = chi2_total(E, rsd_chi2=c_rsd)
    return {'model': f'V_{family}', 'k': len(best[1]),
            'params': {'beta': beta, **({'n': extra[0]} if family == 'RP'
                                        else {'lambda': extra[0]} if family == 'exp'
                                        else {})},
            'chi2_bao': parts[0], 'chi2_sn': parts[1],
            'chi2_cmb': parts[2], 'chi2_rsd': parts[3], 'chi2': parts[4]}


def fit_fluid_ide(xi_min=-1.0, xi_max=1.0):
    """SQMH background fluid toy: coupled ODE via df.E_sqmh_ode(xi_q).
    xi_min=0 restricts to SQMH-consistent (non-phantom) branch."""
    def make_E(xi_q):
        return df.E_sqmh_ode(xi_q)

    # Fluid IDE has no scalar-field growth module; use LCDM growth with
    # config.Omega_m as a proxy. Conservative: fluid picture cannot exploit
    # extra growth freedom it does not possess.
    c_rsd_fluid = rsd.chi2_lcdm(config.Omega_m)

    def cost(p):
        xi_q = float(p[0])
        if not (xi_min <= xi_q <= xi_max):
            return 1e6
        try:
            E = make_E(xi_q)
        except Exception:
            return 1e6
        _, _, _, _, tot = chi2_total(E, rsd_chi2=c_rsd_fluid)
        return tot

    best = (1e8, None)
    starts = [x for x in [-0.3, -0.05, 0.0, 0.05, 0.3]
              if xi_min <= x <= xi_max]
    if not starts:
        starts = [0.5 * (xi_min + xi_max)]
    for x0 in starts:
        try:
            res = minimize(cost, [x0], method='Nelder-Mead',
                           options={'xatol': 1e-5, 'fatol': 1e-3})
            if res.fun < best[0]:
                best = (res.fun, res.x)
        except Exception:
            continue
    if best[1] is None:
        return {'model': 'Fluid IDE', 'k': 1, 'params': {},
                'chi2_bao': np.nan, 'chi2_sn': np.nan,
                'chi2_cmb': np.nan, 'chi2_rsd': np.nan, 'chi2': np.nan}
    xi_q = float(best[1][0])
    try:
        E = make_E(xi_q)
        parts = chi2_total(E, rsd_chi2=c_rsd_fluid)
    except Exception:
        return {'model': 'Fluid IDE', 'k': 1, 'params': {'xi_q': xi_q},
                'chi2_bao': np.nan, 'chi2_sn': np.nan,
                'chi2_cmb': np.nan, 'chi2_rsd': np.nan, 'chi2': np.nan}
    return {'model': 'Fluid IDE', 'k': 1, 'params': {'xi_q': xi_q},
            'chi2_bao': parts[0], 'chi2_sn': parts[1],
            'chi2_cmb': parts[2], 'chi2_rsd': parts[3], 'chi2': parts[4]}


def _info_criteria(chi2, k, N_total):
    aic = chi2 + 2 * k
    bic = chi2 + k * np.log(N_total)
    return aic, bic


def _regression_sanity():
    """LCDM BAO-only best fit must match Phase 1 / df.chi2 directly.
    Expected BAO-only min ~ 21-22 at Om ~ 0.32-0.33 (DESI DR2 13-pt + cov)."""
    from scipy.optimize import minimize_scalar
    def c(Om):
        return _bao_chi2_E(E_lcdm_factory(Om))
    res = minimize_scalar(c, bounds=(0.2, 0.5), method='bounded',
                          options={'xatol': 1e-4})
    ok = 20.0 < res.fun < 23.0 and 0.30 < res.x < 0.35
    tag = "OK" if ok else "MISMATCH"
    print(f"[Phase 2] Regression: LCDM BAO-only min chi2={res.fun:.2f} "
          f"at Om={res.x:.4f} (expect ~21.4 at Om~0.326) [{tag}]")
    return ok


def main():
    _regression_sanity()
    N_total = N_BAO + SN.N + 3 + rsd.N_RSD  # BAO + SN + 3 CMB + RSD
    print(f"[Phase 2] Total data points ~ {N_total} "
          f"(BAO {N_BAO} + SN {SN.N} + CMB 3 + RSD {rsd.N_RSD})")
    print("[Phase 2] Fitting models...")

    results = []
    results.append(fit_lcdm())
    print(f"  LCDM done: chi2={results[-1]['chi2']:.2f} "
          f"params={results[-1]['params']}")

    results.append(fit_fluid_ide())
    fi = results[-1]
    print(f"  Fluid IDE (unconstrained) done: chi2={fi['chi2']} "
          f"params={fi['params']}")
    xi = fi.get('params', {}).get('xi_q', 0.0)
    if xi < 0:
        print(f"  [WARN] xi_q={xi:+.4f} < 0 -> phantom, SQMH-inconsistent. "
              f"Also fitting SQMH-positive branch (xi_q in [0, 1]).")
        fi_pos = fit_fluid_ide(xi_min=0.0, xi_max=1.0)
        fi_pos['model'] = 'Fluid IDE (xi>=0)'
        results.append(fi_pos)
        print(f"  Fluid IDE (xi>=0) done: chi2={fi_pos['chi2']} "
              f"params={fi_pos['params']}")

    # SQMH physical constraint: beta >= 0 (matter gains energy from phi).
    # beta < 0 would flip the coupling direction, violating the SQMH sign
    # convention (CLAUDE.md reproof rule).
    r = fit_quintessence('RP',
                         p0_list=[(0.35, 0.35), (0.1, 0.5), (0.5, 0.2)],
                         bounds=[(0.0, 2.0), (0.05, 5.0)])
    results.append(r if r else {'model': 'V_RP', 'k': 2, 'chi2': np.nan,
                                'chi2_bao': np.nan, 'chi2_sn': np.nan,
                                'chi2_cmb': np.nan, 'params': {}})
    print(f"  V_RP done: chi2={results[-1]['chi2']} "
          f"params={results[-1].get('params', {})}")

    r = fit_quintessence('exp',
                         p0_list=[(0.35, 0.35), (0.1, 0.5), (0.5, 0.2)],
                         bounds=[(0.0, 2.0), (0.05, 3.0)])
    results.append(r if r else {'model': 'V_exp', 'k': 2, 'chi2': np.nan,
                                'chi2_bao': np.nan, 'chi2_sn': np.nan,
                                'chi2_cmb': np.nan, 'params': {}})
    print(f"  V_exp done: chi2={results[-1]['chi2']} "
          f"params={results[-1].get('params', {})}")

    # Report
    print("\n" + "=" * 92)
    print(f"{'Model':<20}{'BAO':>9}{'SN':>10}{'CMB':>8}{'RSD':>8}"
          f"{'tot':>11}{'k':>3}{'AIC':>10}{'BIC':>10}")
    print("-" * 92)
    chi2_lcdm = None
    for r in results:
        c = r['chi2']
        if not np.isfinite(c):
            print(f"{r['model']:<20}{'UNSTABLE':>10}")
            continue
        aic, bic = _info_criteria(c, r['k'], N_total)
        if r['model'] == 'LCDM':
            chi2_lcdm = c
            aic_lcdm = aic
            bic_lcdm = bic
        print(f"{r['model']:<20}{r['chi2_bao']:>9.2f}{r['chi2_sn']:>10.2f}"
              f"{r['chi2_cmb']:>8.2f}{r.get('chi2_rsd', np.nan):>8.2f}"
              f"{c:>11.2f}{r['k']:>3}"
              f"{aic:>10.2f}{bic:>10.2f}")

    print("-" * 92)
    print("Delta vs LCDM (negative = better):")
    for r in results:
        c = r['chi2']
        if not np.isfinite(c) or chi2_lcdm is None:
            continue
        if r['model'] == 'LCDM':
            continue
        aic, bic = _info_criteria(c, r['k'], N_total)
        print(f"  {r['model']:<20} Delta_chi2={c - chi2_lcdm:+.2f}  "
              f"Delta_AIC={aic - aic_lcdm:+.2f}  "
              f"Delta_BIC={bic - bic_lcdm:+.2f}")

    _plot(results, chi2_lcdm, N_total)
    return results


def _plot(results, chi2_lcdm, N_total):
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.axis('off')
    lines = ["Phase 2 Joint Fit -- DESI DR2 BAO + DESY5 SN + Planck compressed CMB",
             "Solver: coupled ODE (Phase 1), Hu-Sugiyama z*, 0.3% theory floor",
             f"Data points: BAO {N_BAO} + SN {SN.N} + CMB 3 = {N_total}",
             "",
             f"{'Model':<12}{'chi2_tot':>10}{'k':>4}{'AIC':>10}{'BIC':>10}{'Delta_AIC':>14}",
             "-" * 60]
    if chi2_lcdm is not None:
        aic_lcdm = chi2_lcdm + 2
    else:
        aic_lcdm = 0.0
    for r in results:
        c = r['chi2']
        if not np.isfinite(c):
            lines.append(f"{r['model']:<12}{'UNSTABLE':>10}")
            continue
        aic, bic = _info_criteria(c, r['k'], N_total)
        d_aic = aic - aic_lcdm
        lines.append(f"{r['model']:<12}{c:>10.2f}{r['k']:>4}{aic:>10.2f}"
                     f"{bic:>10.2f}{d_aic:>+14.2f}")
    lines.append("")
    lines.append("Interpretation:")
    lines.append("  Delta_AIC < -6  : strong improvement (Path A)")
    lines.append("  Delta_AIC -6..-2: weak hint, needs Phase 3 full Cl")
    lines.append("  Delta_AIC > -2  : no improvement (Path F if cumulative)")

    for i, ln in enumerate(lines):
        weight = 'bold' if i < 3 else 'normal'
        size = 10 if i < 3 else 9
        ax.text(0.02, 0.97 - i * 0.055, ln, transform=ax.transAxes,
                fontsize=size, fontweight=weight, fontfamily='monospace',
                verticalalignment='top')

    plt.tight_layout()
    out = os.path.join(os.path.dirname(HERE), '..', 'figures',
                       '12_phase2_joint.png')
    out = os.path.abspath(out)
    plt.savefig(out, dpi=200)
    print(f"[Phase 2] Figure saved: {out}")


if __name__ == "__main__":
    main()
