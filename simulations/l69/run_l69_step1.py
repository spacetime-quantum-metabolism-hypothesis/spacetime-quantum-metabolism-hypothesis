#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L69 Step 1 — SPARC Multivariate Regression (C-1 ~ C-4)
========================================================
Goal: Extract sigma_0(env) function form DIRECTLY from data, with NO
      pre-imposed gating model.

Data:
  - L68 per-galaxy a_0 (refit here for self-containment)
  - Lelli2016 SPARC catalog (175 rows, T type / D / L[3.6] / MHI / Vflat / Q / etc.)

Procedure:
  C-1: per-galaxy sigma_0 = 4*pi*G*c / a_0
  C-2: match catalog metadata
  C-3: multivariate regression sigma_0 ~ (T, D, L[3.6], MHI, Vflat, Q)
       - linear (interpretable)
       - random forest (variance partition)
  C-4: residual analysis — how much of sigma_0 spread is explained by env?

================================================================
4-Team review (P / N / O / H), recorded BEFORE running:
================================================================
P (theory):
  - We treat sigma_0 as if it were a measurement of some physical
    quantity per galaxy. Under SQT, sigma_0 = 4*pi*G*tau_q (constant).
    If we measure sigma_0 varying with V_flat, this is the gating signal.
  - DO NOT impose any axiom. Let regression discover it.
N (numeric):
  - 175 rows, 6+ predictors. n/p > 25, OK for linear regression.
  - Random forest: n_estimators=500, max_depth=8, oob_score=True.
  - Quality flag Q=3 (low) galaxies should be excluded or downweighted
    -- they have noisier rotation curves. Test sensitivity.
O (observation):
  - Vflat is the BEST predictor by physics (this is the regime where
    a_0 is "asymptotic"). Use Vflat preferentially over V_max.
  - Hubble type T encodes morphology. T=10/11 are dwarfs/BCDs.
  - Quality Q stratifies fit reliability.
H (self-consistency hunter, STRONG):
  > "Pre-prediction: Vflat will be the strongest predictor, capturing
     ~50-70% of sigma_0 variance. T type and Q will add ~10-20%.
     Distance D should NOT be a strong predictor under SQT (D is
     measurement, not physics). If D dominates, that's a systematic."
  > "If R^2 > 0.7 by env predictors, single underlying sigma_0 with
     env-dependent gating is supported. If R^2 < 0.3, sigma_0 is
     genuinely intrinsic per galaxy and gating fails."
  > "Test: regression on Vflat ALONE. The coefficient and R^2 there
     determines whether sigma_0(Vflat) is the SQT gating signature."
================================================================
"""

import os
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import sys, json, warnings, time
import numpy as np
from pathlib import Path
import multiprocessing as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import minimize

warnings.filterwarnings('ignore')
np.seterr(all='ignore')

ROOT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis")
SPARC_DIR = ROOT / "simulations/l49/data/sparc"
CATALOG = ROOT / "simulations/l49/data/sparc_catalog.mrt"
OUT = ROOT / "results/L69"
OUT.mkdir(parents=True, exist_ok=True)

# Constants
G_SI = 6.674e-11
C_SI = 2.998e8
KPC_CONV = 3.241e-14
A0_SI    = 1.2e-10
A0_KPC   = A0_SI / KPC_CONV

# ============================================================
# SPARC catalog parser (Lelli 2016, fixed-width)
# ============================================================
def parse_catalog(path):
    """Parse the SPARC master catalog by whitespace splitting.
    Token mapping:
      0 name, 1 T, 2 D, 3 e_D, 4 f_D, 5 Inc, 6 e_Inc, 7 L36, 8 e_L36,
      9 Reff, 10 SBeff, 11 Rdisk, 12 SBdisk, 13 MHI, 14 RHI, 15 Vflat,
      16 e_Vflat, 17 Q, 18 Ref
    """
    catalog = {}
    in_data = False
    dash_count = 0
    with open(path, 'r') as f:
        for line in f:
            ls = line.rstrip()
            if ls.startswith('---'):
                dash_count += 1
                if dash_count >= 4:
                    in_data = True
                continue
            if not in_data or not ls.strip():
                continue
            toks = ls.split()
            if len(toks) < 18:
                continue
            try:
                name = toks[0]
                T = int(toks[1])
                D = float(toks[2])
                f_D = int(toks[4])
                Inc = float(toks[5])
                L36 = float(toks[7])
                Reff = float(toks[9])
                SBeff = float(toks[10])
                MHI = float(toks[13])
                Vflat = float(toks[15])
                Q = int(toks[17])
                catalog[name] = dict(
                    T=T, D=D, f_D=f_D, Inc=Inc,
                    L36=L36, Reff=Reff, SBeff=SBeff, MHI=MHI,
                    Vflat=Vflat, Q=Q,
                )
            except Exception:
                continue
    return catalog

# ============================================================
# SPARC rotmod parser + SQT fit (from L68)
# ============================================================
def parse_rotmod(filepath):
    fp = Path(filepath)
    try:
        rows = []
        distance = None
        with open(fp, 'r') as f:
            for line in f:
                ls = line.strip()
                if ls.startswith('# Distance'):
                    try:
                        distance = float(ls.split('=')[1].split()[0])
                    except Exception:
                        pass
                if not ls or ls.startswith('#'):
                    continue
                parts = ls.split()
                if len(parts) >= 6:
                    row = [float(x) for x in parts[:8]]
                    while len(row) < 8:
                        row.append(0.0)
                    rows.append(row)
        if len(rows) < 3:
            return None
        arr = np.array(rows, dtype=float)
        return dict(
            name=fp.stem.replace('_rotmod', ''),
            distance_Mpc=distance,
            Rad=arr[:, 0], Vobs=arr[:, 1],
            errV=np.maximum(arr[:, 2], 1.0),
            Vgas=arr[:, 3], Vdisk=arr[:, 4], Vbul=arr[:, 5],
        )
    except Exception:
        return None

def _v_bary2(g, Up):
    return g['Vgas']**2 + Up * g['Vdisk']**2 + Up * g['Vbul']**2

def _v_sqt(r, a_N, a_0):
    a_tot = 0.5 * (a_N + np.sqrt(a_N**2 + 4.0 * a_N * a_0))
    return np.sqrt(np.maximum(a_tot * r, 0.0))

def fit_sqt_one(filepath):
    g = parse_rotmod(filepath)
    if g is None:
        return None
    r, vobs, err = g['Rad'], g['Vobs'], g['errV']
    n = len(r)
    if n < 3:
        return None
    LOG_A0 = np.log10(A0_KPC)
    best = {'chi2': np.inf}
    for la0_init in np.linspace(LOG_A0 - 1.5, LOG_A0 + 1.5, 5):
        for Up_init in [0.3, 0.7, 1.2]:
            def obj(p):
                la0, Up = p
                if la0 < LOG_A0 - 3 or la0 > LOG_A0 + 3:
                    return 1e10
                a0 = 10**la0
                aN = _v_bary2(g, max(Up, 0.05)) / r
                vm = _v_sqt(r, aN, a0)
                if not np.all(np.isfinite(vm)):
                    return 1e10
                return float(np.sum(((vobs - vm) / err)**2))
            try:
                res = minimize(obj, [la0_init, Up_init], method='Nelder-Mead',
                               options={'xatol': 1e-4, 'fatol': 1e-4, 'maxiter': 2000})
                if res.fun < best['chi2']:
                    la0, Up = res.x
                    best = dict(
                        chi2=float(res.fun), dof=max(n - 2, 1),
                        log_a0_kpc=float(la0),
                        a0_SI=float(10**la0 * KPC_CONV),
                        Upsilon=float(max(Up, 0.05)),
                        V_max=float(np.max(vobs)),
                        n_pts=int(n),
                        success=True,
                    )
            except Exception:
                continue
    if not best.get('success'):
        return None
    best['name'] = g['name']
    best['distance_Mpc'] = g['distance_Mpc']
    return best

# ============================================================
# Linear regression with statistics
# ============================================================
def linear_regression(X, y, names):
    """Multivariate OLS. Returns dict with coeffs, R^2, p-values."""
    X1 = np.column_stack([np.ones(len(X)), X])
    # Coefficients
    XtX = X1.T @ X1
    XtX_inv = np.linalg.pinv(XtX)
    beta = XtX_inv @ X1.T @ y
    y_pred = X1 @ beta
    residuals = y - y_pred
    n, p = X1.shape
    dof = n - p
    rss = np.sum(residuals**2)
    tss = np.sum((y - np.mean(y))**2)
    r2 = 1 - rss / tss
    sigma2 = rss / dof
    var_beta = sigma2 * np.diag(XtX_inv)
    se_beta = np.sqrt(np.maximum(var_beta, 0))
    t_stat = beta / np.where(se_beta > 0, se_beta, 1)
    return dict(
        intercept=float(beta[0]), coeffs=beta[1:].tolist(),
        se=se_beta[1:].tolist(), t_stat=t_stat[1:].tolist(),
        r2=float(r2), n=int(n), p=int(p), dof=int(dof),
        rss=float(rss), tss=float(tss),
        residuals=residuals.tolist(),
        names=names,
    )

# ============================================================
# Variance partition by single-predictor R^2
# ============================================================
def single_predictor_r2(X, y, names):
    """Univariate R^2 for each predictor. Provides 'standalone' importance."""
    out = []
    for j, name in enumerate(names):
        xj = X[:, j]
        if np.all(np.isnan(xj)):
            out.append(dict(name=name, r2=np.nan))
            continue
        mask = ~np.isnan(xj)
        if mask.sum() < 5:
            out.append(dict(name=name, r2=np.nan))
            continue
        x_, y_ = xj[mask], y[mask]
        try:
            slope, intercept = np.polyfit(x_, y_, 1)
            y_pred = slope * x_ + intercept
            rss = np.sum((y_ - y_pred)**2)
            tss = np.sum((y_ - np.mean(y_))**2)
            r2 = 1 - rss / tss if tss > 0 else 0
            out.append(dict(name=name, r2=float(r2),
                            slope=float(slope), intercept=float(intercept),
                            n=int(mask.sum())))
        except Exception:
            out.append(dict(name=name, r2=np.nan))
    return out

# ============================================================
# Main
# ============================================================
def main():
    print("=" * 60)
    print("L69 Step 1 — SPARC Multivariate Regression")
    print("=" * 60)

    # --- C-1: per-galaxy a_0 (parallel re-fit) ---
    print("\n[C-1] Re-fitting 175 SPARC galaxies for a_0 / sigma_0 ...")
    files = sorted(SPARC_DIR.glob("*_rotmod.dat"))
    print(f"  Files: {len(files)}")
    t0 = time.time()
    ctx = mp.get_context('spawn')
    with ctx.Pool(8) as pool:
        results = pool.map(fit_sqt_one, [str(f) for f in files])
    fits = [r for r in results if r is not None]
    print(f"  OK: {len(fits)}/{len(results)} in {time.time()-t0:.1f}s")

    # sigma_0 per galaxy
    fits_dict = {f['name']: f for f in fits}
    sigma_per_gal = {n: 4 * np.pi * G_SI * C_SI / max(f['a0_SI'], 1e-15)
                     for n, f in fits_dict.items()}

    # --- C-2: catalog match ---
    print("\n[C-2] Matching SPARC Lelli 2016 catalog ...")
    catalog = parse_catalog(CATALOG)
    print(f"  Catalog rows: {len(catalog)}")
    matched = 0
    rows = []
    for name, fit in fits_dict.items():
        c = catalog.get(name)
        if c is None:
            # Try name variants
            for alt in [name.replace('UGC0', 'UGC'), 'UGC0' + name[3:],
                        name.replace('NGC0', 'NGC'), 'NGC0' + name[3:]]:
                if alt in catalog:
                    c = catalog[alt]
                    break
        if c is None:
            continue
        log_a0 = np.log10(fit['a0_SI'])
        log_sigma = np.log10(sigma_per_gal[name])
        rows.append(dict(
            name=name,
            log_a0=log_a0,
            log_sigma=log_sigma,
            T=c['T'],
            D=c['D'],
            f_D=c['f_D'],
            L36=c['L36'],
            log_L36=np.log10(c['L36']) if c['L36'] > 0 else np.nan,
            MHI=c['MHI'],
            log_MHI=np.log10(c['MHI']) if c['MHI'] > 0 else np.nan,
            Vflat=c['Vflat'],
            log_Vflat=np.log10(c['Vflat']) if c['Vflat'] > 0 else np.nan,
            Q=c['Q'],
            V_max=fit['V_max'],
            log_Vmax=np.log10(fit['V_max']),
            chi2=fit['chi2'], dof=fit['dof'],
            chi2_red=fit['chi2'] / max(fit['dof'], 1),
        ))
        matched += 1
    print(f"  Matched: {matched}/{len(fits_dict)}")

    # Filter sane fits and good quality
    rows_all = rows
    rows_q = [r for r in rows_all if r['Q'] in (1, 2)]   # exclude Q=3 (low quality)
    rows_qv = [r for r in rows_q if not np.isnan(r['log_Vflat'])]
    print(f"  After Q in {{1,2}}: {len(rows_q)}")
    print(f"  With Vflat present:  {len(rows_qv)}")

    # --- C-3: multivariate regression on Q in {1,2} sample ---
    print("\n[C-3] Multivariate regression on log10(sigma_0) ...")
    y = np.array([r['log_sigma'] for r in rows_q])
    print(f"  Sample n={len(y)}")
    print(f"  log10(sigma_0): mean={np.mean(y):.3f}, std={np.std(y):.3f} dex")

    # Feature set 1: full predictors (log scale where natural)
    pred_names = ['T', 'D', 'log_L36', 'log_MHI', 'log_Vmax', 'Q', 'chi2_red']
    X = np.array([[r['T'], r['D'], r['log_L36'], r['log_MHI'],
                   r['log_Vmax'], r['Q'], r['chi2_red']]
                  for r in rows_q], dtype=float)
    # Replace NaN with column median (light imputation)
    for j in range(X.shape[1]):
        col = X[:, j]
        med = np.nanmedian(col)
        col[np.isnan(col)] = med
        X[:, j] = col

    reg_full = linear_regression(X, y, pred_names)
    print(f"  Full multivariate R^2 = {reg_full['r2']:.3f}")
    for nm, c, se, t in zip(pred_names, reg_full['coeffs'], reg_full['se'], reg_full['t_stat']):
        print(f"    {nm:12s}: beta={c:+.3f}  se={se:.3f}  t={t:+.2f}")

    # Univariate R^2 (importance)
    uni = single_predictor_r2(X, y, pred_names)
    print("\n  Univariate R^2 (standalone):")
    uni_sorted = sorted(uni, key=lambda d: d.get('r2', 0) or 0, reverse=True)
    for u in uni_sorted:
        if not np.isnan(u.get('r2', np.nan)):
            print(f"    {u['name']:12s}: R^2={u['r2']:.3f}, slope={u['slope']:+.3f}, n={u['n']}")

    # Vflat-only fit (the SQT critical predictor)
    rows_qv_arr = np.array([[r['log_Vflat']] for r in rows_qv], dtype=float)
    y_qv = np.array([r['log_sigma'] for r in rows_qv])
    reg_vflat = linear_regression(rows_qv_arr, y_qv, ['log_Vflat'])
    print(f"\n  Vflat-only on Q in {{1,2}} & Vflat present (n={len(y_qv)}):")
    print(f"    log10(sigma_0) = {reg_vflat['intercept']:.3f} + "
          f"{reg_vflat['coeffs'][0]:+.3f} * log10(Vflat)")
    print(f"    R^2 = {reg_vflat['r2']:.3f}")

    # --- C-4: residual analysis ---
    print("\n[C-4] Residual analysis ...")
    residuals = np.array(reg_full['residuals'])
    res_std = float(np.std(residuals))
    print(f"  Residual std after multivariate fit: {res_std:.3f} dex")
    print(f"  Original spread:                     {np.std(y):.3f} dex")
    print(f"  Fraction explained by predictors:    {1 - (res_std/np.std(y))**2:.3f}")
    # Expected fit-noise floor: dwarfs have V_max-driven scatter in the rotation
    # curves themselves. Estimate from chi2_red distribution.
    chi2_reds = np.array([r['chi2_red'] for r in rows_q])
    print(f"  Median chi^2/dof of fits: {np.median(chi2_reds):.2f}")
    print(f"  This indicates the per-galaxy a_0 measurement noise floor.")

    # --- Summary verdict ---
    if reg_vflat['r2'] > 0.5:
        verdict = ("Vflat strongly predicts sigma_0 ({:.1%}). "
                   "Single underlying sigma_0 with Vflat gating is supported.").format(reg_vflat['r2'])
    elif reg_vflat['r2'] > 0.3:
        verdict = ("Vflat moderately predicts sigma_0 ({:.1%}). "
                   "Gating signal present but with residual intrinsic spread.").format(reg_vflat['r2'])
    else:
        verdict = ("Vflat weakly predicts sigma_0 ({:.1%}). "
                   "sigma_0 spread is largely intrinsic.").format(reg_vflat['r2'])

    print(f"\nVERDICT: {verdict}")

    # ===========================================================
    # Visualization
    # ===========================================================
    fig, axes = plt.subplots(2, 3, figsize=(20, 11))

    # (a) sigma_0 vs Vflat
    ax = axes[0, 0]
    log_vflat = np.array([r['log_Vflat'] for r in rows_qv])
    log_sig_qv = np.array([r['log_sigma'] for r in rows_qv])
    ax.scatter(log_vflat, log_sig_qv, alpha=0.6, c='tab:blue', s=50)
    xs = np.linspace(log_vflat.min(), log_vflat.max(), 100)
    ax.plot(xs, reg_vflat['intercept'] + reg_vflat['coeffs'][0] * xs,
            'r-', lw=2, label=f"slope={reg_vflat['coeffs'][0]:+.2f}, R^2={reg_vflat['r2']:.2f}")
    # SQT predicts sigma_0 = const, so slope should be 0 if SQT is right with single sigma
    ax.axhline(np.log10(SIGMA_T17 := 2.34e8), color='gray', ls=':',
               label=f"T17 (cosmic) = {np.log10(SIGMA_T17):.2f}")
    ax.axhline(np.log10(5.6e7), color='gray', ls='--', label="T20 (cluster) = 7.75")
    ax.set_xlabel('log10(Vflat) [km/s]')
    ax.set_ylabel('log10(sigma_0)')
    ax.set_title(f"(a) sigma_0 vs Vflat (n={len(rows_qv)}, Q in {{1,2}})")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (b) sigma_0 vs Hubble type
    ax = axes[0, 1]
    Ts = np.array([r['T'] for r in rows_q])
    log_sig = np.array([r['log_sigma'] for r in rows_q])
    # Box plot per T
    T_uniq = sorted(set(Ts))
    box_data = [log_sig[Ts == t] for t in T_uniq]
    ax.boxplot(box_data, positions=T_uniq, widths=0.6)
    ax.scatter(Ts + np.random.uniform(-0.15, 0.15, len(Ts)), log_sig,
               alpha=0.4, c='tab:orange', s=20)
    ax.set_xlabel('Hubble type T (0=S0, 11=BCD)')
    ax.set_ylabel('log10(sigma_0)')
    ax.set_title('(b) sigma_0 vs Hubble type')
    ax.grid(alpha=0.3)

    # (c) sigma_0 vs L[3.6] (luminosity / mass proxy)
    ax = axes[0, 2]
    log_L = np.array([r['log_L36'] for r in rows_q])
    valid_L = ~np.isnan(log_L)
    ax.scatter(log_L[valid_L], log_sig[valid_L], alpha=0.6, c='tab:green', s=40)
    # Fit
    p = np.polyfit(log_L[valid_L], log_sig[valid_L], 1)
    xs = np.linspace(log_L[valid_L].min(), log_L[valid_L].max(), 100)
    ax.plot(xs, np.polyval(p, xs), 'r-', lw=2,
            label=f"slope={p[0]:+.2f}")
    ax.set_xlabel('log10(L[3.6])  [10^9 Lsun]')
    ax.set_ylabel('log10(sigma_0)')
    ax.set_title(f"(c) sigma_0 vs Luminosity (n={valid_L.sum()})")
    ax.legend()
    ax.grid(alpha=0.3)

    # (d) Univariate R^2 bars
    ax = axes[1, 0]
    valid_uni = [u for u in uni_sorted if not np.isnan(u.get('r2', np.nan))]
    names_u = [u['name'] for u in valid_uni]
    r2s = [u['r2'] for u in valid_uni]
    bars = ax.bar(names_u, r2s, color='tab:purple', alpha=0.7)
    for bar, v in zip(bars, r2s):
        ax.text(bar.get_x() + bar.get_width()/2, v + 0.01,
                f'{v:.2f}', ha='center', fontsize=9)
    ax.set_ylabel('Univariate R^2')
    ax.set_title('(d) Standalone predictor importance (R^2 single)')
    ax.set_ylim(0, max(r2s + [0.05]) * 1.2)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=20)
    ax.grid(alpha=0.3, axis='y')

    # (e) residuals histogram
    ax = axes[1, 1]
    ax.hist(residuals, bins=25, color='tab:red', alpha=0.6, edgecolor='black')
    ax.axvline(0, color='black', ls='-')
    ax.set_xlabel('Residual log10(sigma_0)')
    ax.set_ylabel('N')
    ax.set_title(f"(e) Residuals after multivariate fit\n"
                 f"std={res_std:.3f} dex (orig {np.std(y):.3f})")
    ax.grid(alpha=0.3)

    # (f) verdict / summary
    ax = axes[1, 2]
    ax.axis('off')

    txt = [
        "L69 Step 1: SPARC sigma_0(env) regression",
        "=" * 42,
        f"Sample: n={len(rows_q)} (Q in {{1,2}})",
        f"Original sigma(log sigma_0) = {np.std(y):.3f} dex",
        "",
        "Multivariate OLS:",
        f"  R^2 = {reg_full['r2']:.3f}",
        f"  Residual std = {res_std:.3f} dex",
        f"  Fraction var explained = {1-(res_std/np.std(y))**2:.3f}",
        "",
        "Univariate R^2 ranking:",
    ]
    for u in uni_sorted[:5]:
        if not np.isnan(u.get('r2', np.nan)):
            txt.append(f"  {u['name']:12s} R^2={u['r2']:.3f}")

    txt += [
        "",
        f"Vflat-only (n={len(rows_qv)}):",
        f"  log sigma_0 = {reg_vflat['intercept']:.2f} + "
        f"{reg_vflat['coeffs'][0]:+.2f} * log Vflat",
        f"  R^2 = {reg_vflat['r2']:.3f}",
        "",
        f"sigma_0 ref values (log):",
        f"  T17 cosmic   = 8.37",
        f"  T17 sc       = 8.07",
        f"  T20 cluster  = 7.75",
        f"  median(SPARC)= {np.median(y):.3f}",
        "",
        "Verdict:",
    ]
    # word wrap
    line = ""
    for w in verdict.split():
        if len(line) + len(w) + 1 > 36:
            txt.append(line)
            line = w
        else:
            line = line + " " + w if line else w
    if line:
        txt.append(line)

    ax.text(0.02, 0.98, "\n".join(txt), family='monospace', fontsize=9,
            transform=ax.transAxes, va='top')

    plt.suptitle('L69 Step 1: SPARC sigma_0 regression on environment', fontsize=13)
    plt.tight_layout()
    plt.savefig(OUT / 'L69_step1.png', dpi=140, bbox_inches='tight')
    plt.close()
    print(f"\nSaved: {OUT/'L69_step1.png'}")

    # Save report
    def _j(o):
        if isinstance(o, (np.bool_, bool)): return bool(o)
        if isinstance(o, (np.integer, int)): return int(o)
        if isinstance(o, (np.floating, float)):
            return float(o) if np.isfinite(o) else None
        if isinstance(o, np.ndarray): return o.tolist()
        if isinstance(o, dict): return {k: _j(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)): return [_j(x) for x in o]
        return o
    report = dict(
        n_galaxies=len(rows_q),
        log_sigma_mean=float(np.mean(y)),
        log_sigma_std=float(np.std(y)),
        regression_full=reg_full,
        regression_vflat=reg_vflat,
        univariate_r2=uni_sorted,
        verdict=verdict,
        residual_std=res_std,
        rows=rows_q,
    )
    # Trim heavy fields
    report['regression_full'].pop('residuals', None)
    with open(OUT / 'l69_step1_report.json', 'w') as f:
        json.dump(_j(report), f, indent=2)
    print(f"Saved: {OUT/'l69_step1_report.json'}")

    return report

if __name__ == "__main__":
    main()
