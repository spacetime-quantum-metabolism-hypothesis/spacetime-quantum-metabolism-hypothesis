"""
Simulation 6: DESI DR2 BAO Fitting — LCDM vs SQMH Quadratic IDE

Uses OFFICIAL DESI DR2 data from:
  arXiv:2503.14738 (DESI DR2 Results II)
  github.com/CobayaSampler/bao_data/desi_bao_dr2/

13 data points: BGS(D_V) + 6 bins x (D_M, D_H)
Full covariance matrix with D_M-D_H correlations.

FIX (2026-04-10):
  1. Replaced ad hoc perturbative E_sqmh with coupled ODE solver
  2. Fixed ODE convention: track omega = rho/rho_crit_0 (physical density)
     E^2(z) = Omega_r(1+z)^4 + omega_m(z) + omega_de(z)
     NOT omega_m*(1+z)^3 (that double-counts dilution)
  3. scipy.optimize for xi_q (both signs) + optional r_d joint fit
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad, odeint
from scipy.interpolate import interp1d
from scipy.optimize import minimize_scalar, minimize
import config
import desi_data
import quintessence


# ============================================================
# Coupled ODE solver for SQMH E(z)
# ============================================================

def solve_sqmh_Ez(xi_q, z_max=3.0, N=2000):
    """
    Solve coupled DE-matter ODE and return E(z) interpolator.

    Variables: omega_m(z), omega_de(z) = rho/rho_crit_0 (physical density)
    E^2(z) = Omega_r*(1+z)^4 + omega_m(z) + omega_de(z)

    Conservation with quadratic IDE coupling Q = 3*H0*xi_q*omega_de*omega_m:
      d(omega_m)/dt  = -3H*omega_m + Q
      d(omega_de)/dt = -Q

    In redshift (dt = -dz/(H(1+z))):
      d(omega_m)/dz  = 3*omega_m/(1+z) - 3*xi_q*omega_de*omega_m/(E*(1+z))
      d(omega_de)/dz = 3*xi_q*omega_de*omega_m/(E*(1+z))

    xi_q > 0: DE -> matter (SQMH canonical: matter annihilates SQ)
    xi_q < 0: matter -> DE (reversed coupling direction)
    """
    def rhs(y, z):
        omega_m, omega_de = y
        omega_de_safe = max(omega_de, 1e-15)
        E2 = config.Omega_r * (1+z)**4 + omega_m + omega_de_safe
        if E2 <= 1e-30:
            return [0.0, 0.0]
        E = np.sqrt(E2)

        Q_term = 3.0 * xi_q * omega_de_safe * omega_m / (E * (1+z))

        d_omega_m = 3.0 * omega_m / (1+z) - Q_term
        d_omega_de = Q_term

        return [d_omega_m, d_omega_de]

    z_arr = np.linspace(0, z_max, N)
    y0 = [config.Omega_m, config.Omega_DE]
    sol = odeint(rhs, y0, z_arr, rtol=1e-10, atol=1e-12)

    omega_m_arr = sol[:, 0]
    omega_de_arr = sol[:, 1]

    E_arr = np.sqrt(config.Omega_r * (1+z_arr)**4
                    + omega_m_arr
                    + np.maximum(omega_de_arr, 1e-15))

    return interp1d(z_arr, E_arr, kind='cubic', fill_value='extrapolate')


# ============================================================
# E(z) functions
# ============================================================

def E_lcdm(z):
    """LCDM: E(z) = H(z)/H0"""
    return np.sqrt(config.Omega_r * (1+z)**4 +
                   config.Omega_m * (1+z)**3 +
                   config.Omega_DE)


class E_sqmh_ode:
    """Callable E(z) from coupled ODE solution. Caches interpolator."""

    def __init__(self, xi_q):
        self.xi_q = xi_q
        self._interp = solve_sqmh_Ez(xi_q)

    def __call__(self, z, *args):
        return float(self._interp(z))


# ============================================================
# Cosmological distance calculations
# ============================================================

def comoving_distance(z, E_func, *args):
    """d_C(z) = c/H0 * integral_0^z dz'/E(z') [in Mpc]"""
    result, _ = quad(lambda zp: 1.0 / E_func(zp, *args), 0, z,
                     limit=100, epsrel=1e-9)
    return (config.c / (config.H_0 * config.Mpc)) * result


def DM_over_rd(z, E_func, rd, *args):
    """D_M/r_d = d_C(z)/r_d (flat universe: D_M = d_C)"""
    dc = comoving_distance(z, E_func, *args)
    return dc / rd


def DH_over_rd(z, E_func, rd, *args):
    """D_H/r_d = c/(H(z)*r_d), where D_H in Mpc"""
    DH_mpc = config.c / (config.H_0 * E_func(z, *args) * config.Mpc)
    return DH_mpc / rd


def DV_over_rd(z, E_func, rd, *args):
    """D_V/r_d = [z * D_M^2 * D_H]^(1/3) / r_d"""
    dm = DM_over_rd(z, E_func, rd, *args) * rd
    dh = DH_over_rd(z, E_func, rd, *args) * rd
    dv = (z * dm**2 * dh)**(1.0/3.0)
    return dv / rd


# ============================================================
# Chi-squared calculation using full covariance
# ============================================================

def model_vector(E_func, rd, *args):
    """Compute model predictions matching DESI_DR2 data ordering."""
    pred = np.zeros(13)
    for i in range(13):
        z = desi_data.DESI_DR2['z_eff'][i]
        q = desi_data.DESI_DR2['quantity'][i]
        if 'DV' in q:
            pred[i] = DV_over_rd(z, E_func, rd, *args)
        elif 'DM' in q:
            pred[i] = DM_over_rd(z, E_func, rd, *args)
        elif 'DH' in q:
            pred[i] = DH_over_rd(z, E_func, rd, *args)
    return pred


def chi2(E_func, rd, *args):
    """Full chi2 with covariance matrix."""
    pred = model_vector(E_func, rd, *args)
    delta = desi_data.DESI_DR2['value'] - pred
    return float(delta @ desi_data.DESI_DR2_COV_INV @ delta)


def chi2_for_xi(xi_q, rd=147.09):
    """Chi2 as function of xi_q only (for optimizer)."""
    try:
        E_func = E_sqmh_ode(xi_q)
        return chi2(E_func, rd)
    except Exception:
        return 1e6


def chi2_for_xi_rd(params):
    """Chi2 as function of (xi_q, r_d) for joint optimization."""
    xi_q, rd = params
    if rd < 130 or rd > 165:
        return 1e6
    return chi2_for_xi(xi_q, rd)


# ============================================================
# Optimization
# ============================================================

def find_best_xi(rd=147.09):
    """Find xi_q that minimizes chi2 (both signs)."""
    # Coarse grid scan
    xi_grid = np.linspace(-1.0, 1.0, 101)
    chi2_grid = np.array([chi2_for_xi(xi, rd) for xi in xi_grid])

    best_idx = np.argmin(chi2_grid)
    xi_start = xi_grid[best_idx]

    # Refine
    lo = max(xi_start - 0.05, -2.0)
    hi = min(xi_start + 0.05, 2.0)
    result = minimize_scalar(lambda x: chi2_for_xi(x, rd),
                             bounds=(lo, hi), method='bounded')
    return result.x, result.fun


def find_best_xi_rd():
    """Joint optimization of xi_q and r_d."""
    xi0, _ = find_best_xi(147.09)
    result = minimize(chi2_for_xi_rd, [xi0, 147.09],
                      method='Nelder-Mead',
                      options={'xatol': 1e-4, 'fatol': 1e-3, 'maxiter': 500})
    return result.x[0], result.x[1], result.fun


# ============================================================
# Phase 1 (base.fix.class.md): V(phi) quintessence fitting
# Families: mass (thawing), RP (freezing tracker), exp (variable)
# ============================================================

def chi2_quintessence(V_family, beta, extra_params, rd=147.09):
    """Chi2 for a given V(phi) family + coupling."""
    E_func = quintessence.E_quintessence(V_family, beta, extra_params)
    if not E_func.ok:
        return 1e6
    try:
        return chi2(E_func, rd)
    except Exception:
        return 1e6


def fit_quintessence(V_family, rd=147.09):
    """
    Fit a V(phi) family to DESI DR2.

    Free parameters:
      mass: beta            (k=1)
      RP:   beta, n         (k=2)
      exp:  beta, lambda    (k=2)

    Returns: dict with best params, chi2, k (n_params), AIC, BIC.
    """
    N_data = 13  # DESI DR2 points

    # SQMH sign convention (CLAUDE.md rule): matter gains energy from phi
    # => beta >= 0. Negative beta is unphysical for all V(phi) families.
    if V_family == "mass":
        def cost(p):
            (beta,) = p
            if beta < 0.0 or beta > 2.0:
                return 1e6
            return chi2_quintessence("mass", beta, (), rd)

        # Multi-start over positive beta (mass has no shape param)
        best = (1e6, None)
        for b0 in [0.01, 0.1, 0.2, 0.3, 0.4]:
            res = minimize(cost, [b0], method='Nelder-Mead',
                           options={'xatol': 1e-4, 'fatol': 1e-3,
                                    'maxiter': 200})
            if res.fun < best[0]:
                best = (res.fun, res.x)
        if best[1] is None:
            return {'family': V_family, 'params': {}, 'chi2': np.nan,
                    'k': 1, 'AIC': np.nan, 'BIC': np.nan,
                    'error': 'all_starts_failed'}
        res_fun, res_x = best
        k = 1
        params = {'beta': float(res_x[0])}
        res = type('R', (), {'fun': res_fun, 'x': res_x})()

    elif V_family == "RP":
        def cost(p):
            beta, n = p
            if beta < 0.0 or beta > 2.0 or n < 0.01 or n > 5.0:
                return 1e6
            return chi2_quintessence("RP", beta, (n,), rd)

        best = (1e6, None)
        for n0 in [0.1, 0.5, 1.0, 2.0]:
            for b0 in [0.01, 0.1, 0.2]:
                res = minimize(cost, [b0, n0], method='Nelder-Mead',
                               options={'xatol': 1e-4, 'fatol': 1e-3,
                                        'maxiter': 300})
                if res.fun < best[0]:
                    best = (res.fun, res.x)
        if best[1] is None:
            return {'family': V_family, 'params': {}, 'chi2': np.nan,
                    'k': 2, 'AIC': np.nan, 'BIC': np.nan,
                    'error': 'all_starts_failed'}
        res_fun, res_x = best
        k = 2
        params = {'beta': float(res_x[0]), 'n': float(res_x[1])}
        res = type('R', (), {'fun': res_fun, 'x': res_x})()

    elif V_family == "exp":
        def cost(p):
            beta, lam = p
            if beta < 0.0 or beta > 2.0 or lam < -3.0 or lam > 3.0:
                return 1e6
            return chi2_quintessence("exp", beta, (lam,), rd)

        best = (1e6, None)
        for lam0 in [-0.5, 0.0, 0.5, 1.0]:
            for b0 in [0.01, 0.1, 0.2]:
                res = minimize(cost, [b0, lam0], method='Nelder-Mead',
                               options={'xatol': 1e-4, 'fatol': 1e-3,
                                        'maxiter': 300})
                if res.fun < best[0]:
                    best = (res.fun, res.x)
        if best[1] is None:
            return {'family': V_family, 'params': {}, 'chi2': np.nan,
                    'k': 2, 'AIC': np.nan, 'BIC': np.nan,
                    'error': 'all_starts_failed'}
        res_fun, res_x = best
        k = 2
        params = {'beta': float(res_x[0]), 'lambda': float(res_x[1])}
        res = type('R', (), {'fun': res_fun, 'x': res_x})()

    else:
        raise ValueError(V_family)

    chi2_val = float(res.fun)
    AIC = chi2_val + 2.0 * k
    BIC = chi2_val + k * np.log(N_data)

    return {
        'family': V_family,
        'params': params,
        'chi2': chi2_val,
        'k': k,
        'AIC': AIC,
        'BIC': BIC,
    }


def fit_all_quintessence(rd=147.09):
    """Fit all three V(phi) families. Returns list of result dicts."""
    results = []
    for family in ["mass", "RP", "exp"]:
        print(f"  Fitting V_{family}...")
        try:
            r = fit_quintessence(family, rd)
            results.append(r)
            print(f"    -> chi2={r['chi2']:.2f}, k={r['k']}, "
                  f"AIC={r['AIC']:.2f}, BIC={r['BIC']:.2f}, "
                  f"params={r['params']}")
        except Exception as e:
            print(f"    -> FAILED: {e}")
            results.append({'family': family, 'chi2': np.nan, 'k': 0,
                            'AIC': np.nan, 'BIC': np.nan, 'params': {},
                            'error': str(e)})
    return results


# ============================================================
# Plotting
# ============================================================

def plot_desi_fit():
    rd_planck = 147.09  # Mpc (Planck 2018 best-fit)

    # Verify: SQMH at xi_q=0 should match LCDM
    E_lcdm_wrap = lambda z, *a: E_lcdm(z)
    chi2_lcdm = chi2(E_lcdm_wrap, rd_planck)
    E_zero = E_sqmh_ode(0.0)
    chi2_zero = chi2(E_zero, rd_planck)
    print(f"Sanity: LCDM chi2={chi2_lcdm:.4f}, SQMH(xi=0) chi2={chi2_zero:.4f}")

    # Optimize xi_q (fixed r_d)
    print("Optimizing xi_q (fixed r_d=147.09)...")
    xi_best, chi2_best = find_best_xi(rd_planck)
    print(f"  Best xi_q = {xi_best:.4f}, chi2 = {chi2_best:.2f}, "
          f"Delta = {chi2_best - chi2_lcdm:+.2f}")

    # Joint optimization
    print("Joint optimization (xi_q, r_d)...")
    xi_joint, rd_joint, chi2_joint = find_best_xi_rd()
    print(f"  Best xi_q={xi_joint:.4f}, r_d={rd_joint:.2f}, "
          f"chi2={chi2_joint:.2f}, Delta={chi2_joint - chi2_lcdm:+.2f}")

    # Phase 1: quintessence V(phi) fits
    print("\n[Phase 1] Quintessence V(phi) fits (fixed r_d=147.09)...")
    q_results = fit_all_quintessence(rd_planck)
    # Store LCDM info as pseudo-entry
    lcdm_entry = {
        'family': 'LCDM', 'chi2': chi2_lcdm, 'k': 1,
        'AIC': chi2_lcdm + 2.0 * 1,
        'BIC': chi2_lcdm + 1 * np.log(13),
        'params': {}
    }

    # Display curves: LCDM + best-fit SQMH + a couple reference points
    xi_display_extra = []
    for candidate in [0.05, -0.05, 0.1, -0.1]:
        if abs(candidate - xi_best) > 0.02:
            xi_display_extra.append(candidate)
            if len(xi_display_extra) >= 2:
                break

    xi_display = sorted(set(xi_display_extra + [xi_best]))
    E_objs = {xi: E_sqmh_ode(xi) for xi in xi_display}

    z_plot = np.linspace(0.05, 2.8, 300)
    DM_lcdm = np.array([DM_over_rd(z, E_lcdm_wrap, rd_planck) for z in z_plot])
    DH_lcdm = np.array([DH_over_rd(z, E_lcdm_wrap, rd_planck) for z in z_plot])

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    cmap = plt.cm.coolwarm
    norm_xi = plt.Normalize(vmin=min(xi_display) - 0.01, vmax=max(xi_display) + 0.01)

    # --- Panel 1: D_M/r_d ---
    ax = axes[0, 0]
    ax.plot(z_plot, DM_lcdm, 'k-', lw=2, label='LCDM')
    for xi_q in xi_display:
        col = 'red' if xi_q == xi_best else cmap(norm_xi(xi_q))
        lw = 2.5 if xi_q == xi_best else 1.5
        ls = '-' if xi_q == xi_best else '--'
        lbl = f'SQMH best xi={xi_q:.3f}' if xi_q == xi_best else f'SQMH xi={xi_q:.2f}'
        DM_sq = np.array([DM_over_rd(z, E_objs[xi_q], rd_planck) for z in z_plot])
        ax.plot(z_plot, DM_sq, ls, color=col, lw=lw, label=lbl)

    for b in desi_data.DESI_BINS:
        if b['type'] == 'DM_DH':
            ax.errorbar(b['z'], b['DM'], b['DM_err'], fmt='o', color='#333',
                        ms=6, capsize=3, zorder=5)
            ax.annotate(b['tracer'], (b['z'], b['DM']), fontsize=7,
                        textcoords="offset points", xytext=(3, 5))

    ax.set_xlabel('Redshift z')
    ax.set_ylabel('$D_M / r_d$')
    ax.set_title('Transverse Distance')
    ax.legend(fontsize=7)

    # --- Panel 2: D_H/r_d ---
    ax = axes[0, 1]
    ax.plot(z_plot, DH_lcdm, 'k-', lw=2, label='LCDM')
    for xi_q in xi_display:
        col = 'red' if xi_q == xi_best else cmap(norm_xi(xi_q))
        lw = 2.5 if xi_q == xi_best else 1.5
        ls = '-' if xi_q == xi_best else '--'
        lbl = f'SQMH best xi={xi_q:.3f}' if xi_q == xi_best else f'SQMH xi={xi_q:.2f}'
        DH_sq = np.array([DH_over_rd(z, E_objs[xi_q], rd_planck) for z in z_plot])
        ax.plot(z_plot, DH_sq, ls, color=col, lw=lw, label=lbl)

    for b in desi_data.DESI_BINS:
        if b['type'] == 'DM_DH':
            ax.errorbar(b['z'], b['DH'], b['DH_err'], fmt='o', color='#333',
                        ms=6, capsize=3, zorder=5)
            ax.annotate(b['tracer'], (b['z'], b['DH']), fontsize=7,
                        textcoords="offset points", xytext=(3, 5))

    ax.set_xlabel('Redshift z')
    ax.set_ylabel('$D_H / r_d$')
    ax.set_title('Radial (Hubble) Distance')
    ax.legend(fontsize=7)

    # --- Panel 3: Residuals ---
    ax = axes[1, 0]
    pred_lcdm = model_vector(E_lcdm_wrap, rd_planck)
    E_best = E_sqmh_ode(xi_best)
    pred_sqmh = model_vector(E_best, rd_planck)
    residuals_lcdm = desi_data.DESI_DR2['value'] - pred_lcdm
    residuals_sqmh = desi_data.DESI_DR2['value'] - pred_sqmh
    sigma = desi_data.DESI_DR2['sigma']

    colors_by_type = {'DV_over_rs': 'green', 'DM_over_rs': 'blue', 'DH_over_rs': 'red'}
    for i in range(13):
        q = desi_data.DESI_DR2['quantity'][i]
        col = colors_by_type[q]
        z = desi_data.DESI_DR2['z_eff'][i]
        ax.errorbar(z - 0.015, residuals_lcdm[i] / sigma[i], 1.0,
                    fmt='o', color=col, ms=6, capsize=3, alpha=0.4)
        ax.errorbar(z + 0.015, residuals_sqmh[i] / sigma[i], 1.0,
                    fmt='s', color=col, ms=5, capsize=3, alpha=0.9)

    ax.axhline(0, color='k', ls='-', lw=1)
    ax.axhline(-2, color='gray', ls=':', alpha=0.5)
    ax.axhline(2, color='gray', ls=':', alpha=0.5)
    ax.set_xlabel('Redshift z')
    ax.set_ylabel('(data - model) / sigma')
    ax.set_title(f'Residuals: circles=LCDM, squares=SQMH(xi={xi_best:.3f})')

    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='green', label='D_V'),
                       Patch(facecolor='blue', label='D_M'),
                       Patch(facecolor='red', label='D_H')]
    ax.legend(handles=legend_elements, fontsize=8)

    # --- Panel 4: Chi-squared + AIC/BIC summary (Phase 1) ---
    ax = axes[1, 1]
    ax.axis('off')

    def _fmt_params(p):
        if not p:
            return ""
        return ", ".join(f"{k}={v:+.3f}" for k, v in p.items())

    lcdm_AIC = chi2_lcdm + 2.0
    lcdm_BIC = chi2_lcdm + np.log(13)

    lines = [
        "DESI DR2 BAO Fit -- Phase 1",
        "=" * 46,
        "Data: 13 pts (arXiv:2503.14738)",
        "Solver: coupled ODE, rtol=1e-8",
        "",
        "Model          chi2   k   AIC    BIC",
        "-" * 46,
        f"LCDM          {chi2_lcdm:6.2f}  1  {lcdm_AIC:6.2f} {lcdm_BIC:6.2f}",
        f"Fluid IDE     {chi2_best:6.2f}  1  "
        f"{chi2_best+2:6.2f} {chi2_best+np.log(13):6.2f}",
    ]
    for r in q_results:
        chi2_bad = (np.isnan(r['chi2']) or not np.isfinite(r['chi2'])
                    or r['chi2'] > 1000)
        if chi2_bad:
            # Unstable: could be backward anti-damping (V_mass) or NaN
            # propagation (e.g., phi<=0 for V_RP). Reason left generic.
            if r['family'] == 'mass':
                reason = "backward anti-damping"
            else:
                reason = "ODE invalid"
            lines.append(f"V_{r['family']:<10s}UNSTABLE ({reason})")
            r['_unstable'] = True
        else:
            lines.append(
                f"V_{r['family']:<10s}{r['chi2']:6.2f}  {r['k']}  "
                f"{r['AIC']:6.2f} {r['BIC']:6.2f}"
            )
    lines.append("-" * 46)
    lines.append("Delta_AIC vs LCDM (neg=better):")
    lines.append(f"  Fluid IDE : {chi2_best+2 - lcdm_AIC:+.2f}")
    for r in q_results:
        if not r.get('_unstable', False) and not np.isnan(r['chi2']):
            lines.append(f"  V_{r['family']:<8s}: {r['AIC'] - lcdm_AIC:+.2f}")
    lines.append("")
    lines.append("Phase 1 verdict:")
    best_q = min([r for r in q_results
                  if not r.get('_unstable', False) and not np.isnan(r['chi2'])],
                 key=lambda x: x['AIC'], default=None)
    if best_q is None:
        lines.append("  All V(phi) fits FAILED")
    else:
        d_aic = best_q['AIC'] - lcdm_AIC
        if d_aic < -6:
            verdict = "STRONG improvement"
        elif d_aic < -2:
            verdict = "WEAK improvement"
        else:
            verdict = "NO improvement"
        lines.append(f"  Best: V_{best_q['family']} ({_fmt_params(best_q['params'])})")
        lines.append(f"  Delta_AIC={d_aic:+.2f} -> {verdict}")

    for i, line in enumerate(lines):
        weight = 'bold' if i < 2 else 'normal'
        size = 9.5 if i < 2 else 7.5
        ax.text(0.02, 0.97 - i * 0.035, line, transform=ax.transAxes,
                fontsize=size, fontweight=weight, fontfamily='monospace',
                verticalalignment='top')

    plt.suptitle('DESI DR2 BAO: LCDM vs SQMH Fluid IDE vs V(phi) Quintessence '
                 '(Phase 1)', fontsize=12)
    plt.tight_layout()
    plt.savefig('../figures/11_desi_dr2_fit.png', dpi=300)
    plt.show()

    print(f"\nLCDM chi2 = {chi2_lcdm:.2f}")
    print(f"SQMH best (fixed r_d): xi_q={xi_best:+.4f}, chi2={chi2_best:.2f}, "
          f"Delta={chi2_best - chi2_lcdm:+.2f}")
    print(f"SQMH best (joint):     xi_q={xi_joint:+.4f}, r_d={rd_joint:.2f}, "
          f"chi2={chi2_joint:.2f}, Delta={chi2_joint - chi2_lcdm:+.2f}")

    return {
        'chi2_lcdm': chi2_lcdm,
        'xi_best': xi_best, 'chi2_best': chi2_best,
        'xi_joint': xi_joint, 'rd_joint': rd_joint, 'chi2_joint': chi2_joint,
        'quintessence': q_results,
    }


if __name__ == "__main__":
    print("=" * 60)
    print("SQMH DESI DR2 Fitting (Coupled ODE -- Fixed Convention)")
    print("=" * 60)
    plot_desi_fit()
