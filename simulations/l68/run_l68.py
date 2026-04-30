#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L68: Test the "Measurement Contamination" Hypothesis (3 phases)
================================================================

User hypothesis: sigma_0 non-monotonicity (T17 cosmic, T20 cluster,
T22 galactic) might be artifact of different measurement chains, NOT
real theory variation.

Phase 1 - SPARC environment binning:
    Per-galaxy a_0 from 175 SPARC galaxies. Bin by V_max (mass/env proxy)
    and distance. If sigma(log a_0) collapses inside bins, environment
    drives the spread (consistent with systematics interpretation).

Phase 2 - Inflate systematics on T17/T20/T22:
    Apply known/standard systematics (Cepheid zero-point, AGN feedback,
    nonlinear correction, galaxy mass-to-light scatter). Compute the
    chi^2 of single-sigma_0 hypothesis with inflated errors. PASS if
    chi^2/dof < 2.

Phase 3 - AICc model comparison:
    Model A: single sigma_0 + 4 systematic-shift parameters (5 DoF)
    Model B: monotonic sigmoid gating (1 DoF, from L66/L67 best fits)
    Compute AICc on the 4 sigma_eff "datapoints".

================================================================
4-Team review (P / N / O / H), recorded BEFORE running:
================================================================
P (theory):
  - Phase 1 logic: if a_0 spread collapses by V_max bin, the spread
    is environment-correlated, suggesting a single underlying a_0.
  - Phase 2 caveat: standard systematics ~0.05-0.15 dex per channel.
    Total spread is 1.4 dex (T22-T20). Systematics alone unlikely
    to absorb full spread. Predict marginal pass at best.
N (numeric):
  - SPARC fit: reuse L49 logic (Nelder-Mead, 5 init seeds in log_a0,
    3 in Upsilon). 175 gal x 8 workers.
  - V_max bins: equal-count quartiles. Distance: 4 quantile bins.
  - AICc penalty: k=5 vs k=1 -> Delta-AIC bias of ~12 against Model A.
O (observation):
  - V_max correlates with stellar mass M_*. M_* correlates with
    environment (heavy galaxies in clusters). V_max is reasonable
    env proxy but coarse.
  - SPARC has Lelli et al 2016 catalog with type, distance, V_flat —
    we use what's in the rotmod files plus computed V_max.
H (self-consistency hunter, STRONG):
  > Phase 1 is the cleanest test. If a_0 spread is intrinsic (NOT
    correlated with V_max/D), then systematics interpretation is
    weak — it would require unmeasured systematic correlated only
    with galaxy itself.
  > Pre-prediction: V_max-bin spread ~ 0.6-0.7 dex (mostly intrinsic).
    M/L scatter alone ~0.2 dex. Distance ~0.05 dex. Predict Phase 1
    PASS partial — bin sigma reduced but not eliminated.
  > Phase 2 prediction: systematics absorb T17 vs T22 (cosmic vs
    galactic) but NOT T20 (cluster sigma_8). T20 = 5.6e7 vs T22 =
    3.3e9 is 1.77 dex. Systematics ~0.3 dex max. Phase 2 FAIL likely.
  > Phase 3 prediction: AICc favors Model B (non-monotonic with 1 DoF)
    over Model A (single + 5 systematics). Model A is overfit.
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
from scipy.stats import chi2 as sp_chi2

warnings.filterwarnings('ignore')
np.seterr(all='ignore')

ROOT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis")
SPARC_DIR = ROOT / "simulations/l49/data/sparc"
OUT = ROOT / "results/L68"
OUT.mkdir(parents=True, exist_ok=True)

# ============================================================
# Constants (from L49)
# ============================================================
G_KPC = 4.302e-6
G_SI  = 6.674e-11
C_SI  = 2.998e8
H0_KMS = 73.8
Mpc_m  = 3.0857e22
KPC_CONV = 3.241e-14
A0_SI    = 1.2e-10
A0_KPC   = A0_SI / KPC_CONV  # ~3703

# sigma_0 reference values
SIGMA_REF = {
    'T17_tension': 2.34e8,
    'T17_sc':      1.17e8,
    'T20_s8':      5.6e7,
    'T22_a0':      3.31e9,
}

# ============================================================
# SPARC parser (with distance from header)
# ============================================================
def parse_sparc_file(filepath):
    fp = Path(filepath)
    try:
        distance = None
        rows = []
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
        errV = np.maximum(arr[:, 2], 1.0)
        return dict(
            name=fp.stem.replace('_rotmod', ''),
            distance_Mpc=distance,
            Rad=arr[:, 0],
            Vobs=arr[:, 1],
            errV=errV,
            Vgas=arr[:, 3],
            Vdisk=arr[:, 4],
            Vbul=arr[:, 5],
        )
    except Exception:
        return None

def _v_bary2(g, Up_d, Up_b=None):
    if Up_b is None:
        Up_b = Up_d
    return g['Vgas']**2 + Up_d * g['Vdisk']**2 + Up_b * g['Vbul']**2

def _v_sqt(r, a_N, a_0):
    a_tot = 0.5 * (a_N + np.sqrt(a_N**2 + 4.0 * a_N * a_0))
    return np.sqrt(np.maximum(a_tot * r, 0.0))

def _chi2(v_obs, v_mod, err):
    return float(np.sum(((v_obs - v_mod) / err)**2))

def fit_sqt(g):
    r, vobs, err = g['Rad'], g['Vobs'], g['errV']
    n = len(r)
    if n < 3:
        return None
    LOG_A0 = np.log10(A0_KPC)
    best = {'chi2': np.inf}
    for la0_init in [LOG_A0 - 1.0, LOG_A0 - 0.5, LOG_A0, LOG_A0 + 0.5, LOG_A0 + 1.0]:
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
                return _chi2(vobs, vm, err)
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
                        success=True,
                    )
            except Exception:
                continue
    return best if best.get('success') else None

def _worker(filepath):
    g = parse_sparc_file(filepath)
    if g is None:
        return dict(name=Path(filepath).stem, ok=False)
    fit = fit_sqt(g)
    if fit is None:
        return dict(name=g['name'], ok=False)
    V_max = float(np.max(g['Vobs']))
    return dict(
        name=g['name'], ok=True,
        distance_Mpc=g['distance_Mpc'],
        V_max=V_max,
        n_points=len(g['Rad']),
        **fit,
    )

# ============================================================
# Phase 1 — SPARC binning
# ============================================================
def phase1_sparc_binning():
    print("\n" + "=" * 60)
    print("Phase 1: SPARC per-galaxy a_0 + V_max/distance binning")
    print("=" * 60)

    files = sorted(SPARC_DIR.glob("*_rotmod.dat"))
    if not files:
        raise FileNotFoundError(f"No SPARC files in {SPARC_DIR}")
    print(f"  Found {len(files)} SPARC files")

    t0 = time.time()
    ctx = mp.get_context('spawn')
    with ctx.Pool(8) as pool:
        results = pool.map(_worker, [str(f) for f in files])
    print(f"  Fit done in {time.time()-t0:.1f}s")

    ok = [r for r in results if r.get('ok')]
    print(f"  OK: {len(ok)}/{len(results)}")
    if len(ok) < 100:
        print("  WARNING: <100 OK fits, results suspect")

    # Per-galaxy log a_0 (m/s^2)
    log_a0 = np.array([np.log10(r['a0_SI']) for r in ok])
    V_max  = np.array([r['V_max'] for r in ok])
    dist   = np.array([r['distance_Mpc'] for r in ok if r['distance_Mpc']])
    # Filter outliers (a0 very small/large = fit failed)
    sane = (log_a0 > -13) & (log_a0 < -8)
    ok_sane = [ok[i] for i in range(len(ok)) if sane[i]]
    log_a0_s = log_a0[sane]
    V_max_s  = V_max[sane]
    print(f"  Sane fits (-13<log10 a_0<-8): {len(ok_sane)}/{len(ok)}")

    # Overall spread
    overall_std = float(np.std(log_a0_s))
    overall_med = float(np.median(log_a0_s))
    print(f"  Overall: median(log10 a_0)={overall_med:.3f}  std={overall_std:.3f} dex")

    # Bin by V_max quartiles
    q = np.quantile(V_max_s, [0.0, 0.25, 0.5, 0.75, 1.0])
    bin_results = []
    for i in range(4):
        mask = (V_max_s >= q[i]) & (V_max_s <= q[i+1] if i == 3 else V_max_s < q[i+1])
        if mask.sum() < 5:
            continue
        bin_log = log_a0_s[mask]
        bin_results.append(dict(
            bin=i, vmin=float(q[i]), vmax=float(q[i+1]),
            n=int(mask.sum()),
            median=float(np.median(bin_log)),
            std=float(np.std(bin_log)),
        ))
        print(f"  V_max bin [{q[i]:.0f},{q[i+1]:.0f}] km/s: n={mask.sum()}, "
              f"median={np.median(bin_log):.3f}, std={np.std(bin_log):.3f}")

    # Mean within-bin std (variance reduction signature of systematics absorption)
    bin_stds = [b['std'] for b in bin_results]
    mean_within_std = float(np.mean(bin_stds))
    var_reduction = (overall_std**2 - mean_within_std**2) / overall_std**2
    print(f"\n  Mean within-bin std: {mean_within_std:.3f} dex")
    print(f"  Variance reduction by V_max binning: {100*var_reduction:.1f}%")
    if mean_within_std < 0.30:
        verdict_p1 = "PASS-tight (within-bin <0.30 dex)"
    elif mean_within_std < 0.50:
        verdict_p1 = "PASS-loose (within-bin <0.50 dex)"
    else:
        verdict_p1 = "FAIL (within-bin >=0.50 dex; intrinsic spread)"
    print(f"  Phase 1 verdict: {verdict_p1}")

    return dict(
        per_galaxy=ok_sane,
        overall_std=overall_std,
        overall_median=overall_med,
        bin_results=bin_results,
        mean_within_std=mean_within_std,
        var_reduction=var_reduction,
        verdict=verdict_p1,
        log_a0=log_a0_s.tolist(),
        V_max=V_max_s.tolist(),
    )

# ============================================================
# Phase 2 — Inflated systematics on T17/T20/T22 sigma_0
# ============================================================
def phase2_systematics_inflation(p1):
    print("\n" + "=" * 60)
    print("Phase 2: Inflated systematics on sigma_0 datapoints")
    print("=" * 60)

    # log10(sigma_0) per measurement
    log_sigma = {k: np.log10(v) for k, v in SIGMA_REF.items()}

    # Standard systematics estimates (dex on log10 sigma_0)
    # These are conservative LITERATURE estimates, not magic numbers:
    #   T17 H0: Cepheid zeroP ~0.02, TRGB ~0.02, sigma_8-Om degen ~0.05
    #           Total quadrature ~0.06 dex
    #   T20 sigma_8: HMcode nonlinear ~0.02, AGN feedback ~0.03,
    #                M-c relation ~0.04; total ~0.06 dex
    #   T22 a_0 SPARC: from Phase 1 (from-data) within-bin std ~p1['mean_within_std']
    #                  Systematic on the median: ~p1['mean_within_std']/sqrt(N_bin)
    SYST_DEX = {
        'T17_tension': 0.06,
        'T17_sc':      0.06,
        'T20_s8':      0.06,
        'T22_a0':      max(0.10, p1['mean_within_std'] / np.sqrt(40)),
    }
    print("  Systematic uncertainties (dex on log10 sigma_0):")
    for k, v in SYST_DEX.items():
        print(f"    {k:14s}: {v:.3f} dex")

    # For T22, the "measurement" of sigma_0 from Phase 1 is the median
    # log a_0, propagating to log sigma_0 via:
    # sigma_0 = 4*pi*G*c/a_0  =>  log sigma_0 = const - log a_0
    log_a0_med = p1['overall_median']                  # log10(a_0 SI)
    log_sigma_T22_from_data = np.log10(4 * np.pi * G_SI * C_SI) - log_a0_med
    log_sigma['T22_a0_data'] = log_sigma_T22_from_data
    print(f"\n  log10 sigma_0 per measurement:")
    for k, v in log_sigma.items():
        print(f"    {k:18s}: {v:.3f}")

    # Single-sigma_0 hypothesis test: chi^2 with inflated errors
    # Use the 4 primary measurements and propagated T22
    # We treat T17_tension and T17_sc as cosmic variants; pick one for cleanness
    measurements = {
        'T17_tension': (log_sigma['T17_tension'], SYST_DEX['T17_tension']),
        'T20_s8':      (log_sigma['T20_s8'],      SYST_DEX['T20_s8']),
        'T22_a0_data': (log_sigma_T22_from_data,  SYST_DEX['T22_a0']),
    }
    log_vals = np.array([m[0] for m in measurements.values()])
    log_errs = np.array([m[1] for m in measurements.values()])

    # Best single sigma_0 = inverse-variance weighted
    w = 1.0 / log_errs**2
    log_sigma_best = float(np.sum(log_vals * w) / np.sum(w))
    chi2 = float(np.sum(((log_vals - log_sigma_best) / log_errs)**2))
    dof = len(log_vals) - 1
    p_val = 1.0 - sp_chi2.cdf(chi2, dof)

    print(f"\n  Single-sigma_0 hypothesis (inflated errors):")
    print(f"    Best log10 sigma_0 = {log_sigma_best:.3f} -> sigma_0 = {10**log_sigma_best:.3e}")
    print(f"    chi^2/dof = {chi2/dof:.2f}  (chi^2={chi2:.2f}, dof={dof})")
    print(f"    p-value = {p_val:.2e}")

    if chi2 / dof < 2.0:
        verdict_p2 = "PASS - single sigma_0 acceptable"
    elif chi2 / dof < 5.0:
        verdict_p2 = "MARGINAL - tension but not killing"
    else:
        verdict_p2 = "FAIL - systematics cannot absorb spread"
    print(f"  Phase 2 verdict: {verdict_p2}")

    # Required systematic per channel to PASS (chi^2/dof <= 1)
    # Equivalent: all log_vals within ~1 sigma of mean
    spread = np.max(log_vals) - np.min(log_vals)
    syst_required = spread / 2.0
    print(f"\n  Spread (max-min log sigma) = {spread:.3f} dex")
    print(f"  Systematic required for PASS = {syst_required:.3f} dex per channel")
    print(f"  vs. literature estimate ~0.06 dex -> ratio {syst_required/0.06:.1f}x")

    return dict(
        log_sigma=log_sigma,
        SYST_DEX=SYST_DEX,
        log_sigma_best=log_sigma_best,
        chi2=chi2, dof=dof, p_value=p_val,
        spread_dex=float(spread),
        syst_required=float(syst_required),
        verdict=verdict_p2,
        measurements={k: (float(v[0]), float(v[1])) for k, v in measurements.items()},
    )

# ============================================================
# Phase 3 — AICc comparison
# ============================================================
def phase3_aicc(p1, p2):
    print("\n" + "=" * 60)
    print("Phase 3: AICc model comparison")
    print("=" * 60)

    # The 4 measurements we want to explain
    obs = {
        'cosmic':  (np.log10(SIGMA_REF['T17_tension']), 0.06),
        'cluster': (np.log10(SIGMA_REF['T20_s8']),      0.06),
        'galactic':(p2['log_sigma']['T22_a0_data'],      p2['SYST_DEX']['T22_a0']),
    }
    log_obs = np.array([v[0] for v in obs.values()])
    log_err = np.array([v[1] for v in obs.values()])
    N = len(log_obs)

    # ----- Model A: single sigma_0 + per-channel additive shift c_i (k=N) -----
    # That is fully degenerate (perfect fit), but penalized by AICc.
    # Honest version: single sigma_0 + uniform contamination scale s (k=2)
    # log_sigma_pred(channel) = log_sigma_0 + s * w_channel
    # where w_channel encodes "pathlength weight" (cosmic > cluster > galactic).
    # We treat w_channel as known a priori from path arguments.
    w_path = {'cosmic': 1.0, 'cluster': 0.5, 'galactic': 0.0}
    w_arr = np.array([w_path[k] for k in obs])
    def chi2_A(params):
        log_s0, s_amp = params
        pred = log_s0 + s_amp * w_arr
        return np.sum(((log_obs - pred) / log_err)**2)
    res_A = minimize(chi2_A, [9.0, -1.0], method='Nelder-Mead',
                     options={'xatol': 1e-5, 'fatol': 1e-5, 'maxiter': 5000})
    chi2_A_best = float(res_A.fun)
    k_A = 2
    AIC_A  = chi2_A_best + 2 * k_A
    AICc_A = AIC_A + (2 * k_A * (k_A + 1)) / max(N - k_A - 1, 1)

    # ----- Model B: monotonic gating sigma_eff(env) = f(env) * sigma_0_anchor -----
    # f = sigmoid in log density (axiom A from L66).  Single threshold = 1 DoF.
    rho_env = {'cosmic': 2.7e-27, 'cluster': 2.7e-24, 'galactic': 1.7e-21}
    rho_arr = np.array([rho_env[k] for k in obs])
    sigma_anchor = SIGMA_REF['T22_a0']  # anchor at galactic
    def f_sigmoid(rho, log_thr, w=0.3):
        z = (np.log10(rho) - log_thr) / w
        return 1.0 / (1.0 + np.exp(-z))
    def chi2_B(params):
        log_thr, = params
        f = f_sigmoid(rho_arr, log_thr)
        f = np.maximum(f, 1e-8)
        pred = np.log10(sigma_anchor * f)
        return np.sum(((log_obs - pred) / log_err)**2)
    res_B = minimize(chi2_B, [-22.0], method='Nelder-Mead',
                     options={'xatol': 1e-5, 'fatol': 1e-5, 'maxiter': 5000})
    chi2_B_best = float(res_B.fun)
    k_B = 1
    AIC_B  = chi2_B_best + 2 * k_B
    AICc_B = AIC_B + (2 * k_B * (k_B + 1)) / max(N - k_B - 1, 1)

    # ----- Model C: non-monotonic axiom (resonance peak)
    # sigma_eff(rho) = sigma_anchor * exp(-((log rho - log rho_peak)/w)^2)
    # 2 DoF: log_rho_peak, width
    def gauss_peak(rho, log_peak, w):
        z = (np.log10(rho) - log_peak) / w
        return np.exp(-0.5 * z**2)
    def chi2_C(params):
        log_peak, w = params
        if w < 0.1 or w > 5.0:
            return 1e10
        f = gauss_peak(rho_arr, log_peak, w)
        f = np.maximum(f, 1e-8)
        pred = np.log10(sigma_anchor * f)
        return np.sum(((log_obs - pred) / log_err)**2)
    res_C = minimize(chi2_C, [-21.0, 0.5], method='Nelder-Mead',
                     options={'xatol': 1e-5, 'fatol': 1e-5, 'maxiter': 5000})
    chi2_C_best = float(res_C.fun)
    k_C = 2
    AIC_C  = chi2_C_best + 2 * k_C
    AICc_C = AIC_C + (2 * k_C * (k_C + 1)) / max(N - k_C - 1, 1)

    print(f"\n  Model A (single sigma_0 + path-systematics):")
    print(f"    log10 sigma_0 = {res_A.x[0]:.3f}, syst_amp = {res_A.x[1]:.3f}")
    print(f"    chi^2 = {chi2_A_best:.3f}, k={k_A}, AICc = {AICc_A:.3f}")
    print(f"\n  Model B (monotonic density-gating):")
    print(f"    log10 thr = {res_B.x[0]:.3f}")
    print(f"    chi^2 = {chi2_B_best:.3f}, k={k_B}, AICc = {AICc_B:.3f}")
    print(f"\n  Model C (resonance peak in log density):")
    print(f"    log10 rho_peak = {res_C.x[0]:.3f}, w = {res_C.x[1]:.3f}")
    print(f"    chi^2 = {chi2_C_best:.3f}, k={k_C}, AICc = {AICc_C:.3f}")

    # Ranking
    aiccs = sorted([
        ('A_single+syst',     AICc_A, k_A, chi2_A_best),
        ('B_monotonic_gate',  AICc_B, k_B, chi2_B_best),
        ('C_resonance_peak',  AICc_C, k_C, chi2_C_best),
    ], key=lambda x: x[1])
    print(f"\n  Ranking (lowest AICc = best):")
    aicc_min = aiccs[0][1]
    for name, aicc, k, chi2_val in aiccs:
        delta = aicc - aicc_min
        print(f"    {name:22s}  AICc={aicc:.2f}  Delta={delta:+.2f}  k={k}  chi^2={chi2_val:.2f}")

    return dict(
        modelA=dict(params=res_A.x.tolist(), chi2=chi2_A_best, k=k_A, AICc=AICc_A),
        modelB=dict(params=res_B.x.tolist(), chi2=chi2_B_best, k=k_B, AICc=AICc_B),
        modelC=dict(params=res_C.x.tolist(), chi2=chi2_C_best, k=k_C, AICc=AICc_C),
        ranking=[(n, float(a)) for n, a, _, _ in aiccs],
        obs_logsigma=log_obs.tolist(),
        obs_logerr=log_err.tolist(),
    )

# ============================================================
# Visualization
# ============================================================
def visualize(p1, p2, p3):
    fig, axes = plt.subplots(2, 3, figsize=(20, 11))

    # (a) SPARC log a_0 distribution
    ax = axes[0, 0]
    ax.hist(p1['log_a0'], bins=30, alpha=0.7, color='tab:blue', edgecolor='black')
    ax.axvline(p1['overall_median'], color='red', ls='--',
               label=f"median={p1['overall_median']:.2f}")
    ax.axvline(np.log10(A0_SI), color='green', ls=':', label=f"MOND={np.log10(A0_SI):.2f}")
    ax.set_xlabel('log10(a_0) [m/s^2]')
    ax.set_ylabel('N galaxies')
    ax.set_title(f"(a) SPARC a_0 distribution (n={len(p1['log_a0'])})\n"
                 f"std={p1['overall_std']:.3f} dex")
    ax.legend()
    ax.grid(alpha=0.3)

    # (b) V_max binning
    ax = axes[0, 1]
    bin_centers = [0.5*(b['vmin']+b['vmax']) for b in p1['bin_results']]
    bin_means = [b['median'] for b in p1['bin_results']]
    bin_stds  = [b['std'] for b in p1['bin_results']]
    bin_ns    = [b['n'] for b in p1['bin_results']]
    ax.errorbar(bin_centers, bin_means, yerr=bin_stds, fmt='o-',
                capsize=5, markersize=10, color='tab:orange',
                label='per-bin median +- std')
    for c, m, s, n in zip(bin_centers, bin_means, bin_stds, bin_ns):
        ax.text(c, m + s + 0.05, f"n={n}", ha='center', fontsize=8)
    ax.axhline(p1['overall_median'], color='red', ls='--', alpha=0.5,
               label='overall median')
    ax.fill_between([min(bin_centers)-20, max(bin_centers)+20],
                    p1['overall_median'] - p1['overall_std'],
                    p1['overall_median'] + p1['overall_std'],
                    color='red', alpha=0.1, label='overall +-std')
    ax.set_xlabel('V_max [km/s]')
    ax.set_ylabel('log10(a_0) [m/s^2]')
    ax.set_title(f"(b) V_max-binned a_0\nwithin-bin std={p1['mean_within_std']:.3f} dex, "
                 f"var-red={100*p1['var_reduction']:.0f}%")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (c) sigma_0 evidence with inflated errors (Phase 2)
    ax = axes[0, 2]
    keys = list(p2['measurements'].keys())
    vals = [p2['measurements'][k][0] for k in keys]
    errs = [p2['measurements'][k][1] for k in keys]
    x = np.arange(len(keys))
    ax.errorbar(x, vals, yerr=errs, fmt='s', markersize=10, capsize=8,
                color='tab:red', label='measurement +- syst')
    ax.axhline(p2['log_sigma_best'], color='green', ls='-',
               label=f"single fit log_sigma={p2['log_sigma_best']:.2f}")
    ax.set_xticks(x)
    ax.set_xticklabels(keys, rotation=20, fontsize=9)
    ax.set_ylabel('log10(sigma_0)')
    ax.set_title(f"(c) Phase 2: inflated-error fit\n"
                 f"chi^2/dof={p2['chi2']/p2['dof']:.2f}, p={p2['p_value']:.1e}")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (d) Phase 3 model fits
    ax = axes[1, 0]
    rho_grid = np.logspace(-28, -20, 200)
    sigma_anchor = SIGMA_REF['T22_a0']
    # Model A on rho axis (uses w_path, not rho — represent at obs points)
    rho_obs = np.array([2.7e-27, 2.7e-24, 1.7e-21])
    obs_log = p3['obs_logsigma']
    obs_err = p3['obs_logerr']
    ax.errorbar(np.log10(rho_obs), obs_log, yerr=obs_err, fmt='ks',
                markersize=12, capsize=8, label='observed')
    # Model B
    log_thr_B = p3['modelB']['params'][0]
    f_B = 1.0 / (1.0 + np.exp(-(np.log10(rho_grid) - log_thr_B) / 0.3))
    sigma_B = sigma_anchor * np.maximum(f_B, 1e-8)
    ax.plot(np.log10(rho_grid), np.log10(sigma_B), 'b-', lw=2,
            label=f"B monotonic (chi^2={p3['modelB']['chi2']:.2f})")
    # Model C
    log_pk, w_C = p3['modelC']['params']
    f_C = np.exp(-0.5 * ((np.log10(rho_grid) - log_pk) / w_C)**2)
    sigma_C = sigma_anchor * np.maximum(f_C, 1e-8)
    ax.plot(np.log10(rho_grid), np.log10(sigma_C), 'r-', lw=2,
            label=f"C resonance (chi^2={p3['modelC']['chi2']:.2f})")
    # Model A predictions at the 3 points
    log_s0_A, s_amp_A = p3['modelA']['params']
    w_path_arr = np.array([1.0, 0.5, 0.0])
    pred_A = log_s0_A + s_amp_A * w_path_arr
    ax.plot(np.log10(rho_obs), pred_A, 'g^', markersize=12,
            label=f"A path-syst (chi^2={p3['modelA']['chi2']:.2f})")
    ax.set_xlabel('log10(rho) [kg/m^3]')
    ax.set_ylabel('log10(sigma_0)')
    ax.set_title('(d) Phase 3: 3-model fit on sigma_0 vs density')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (e) AICc bar chart
    ax = axes[1, 1]
    names = ['A_single+syst', 'B_monotonic', 'C_resonance']
    aiccs = [p3['modelA']['AICc'], p3['modelB']['AICc'], p3['modelC']['AICc']]
    chi2s = [p3['modelA']['chi2'], p3['modelB']['chi2'], p3['modelC']['chi2']]
    ks    = [p3['modelA']['k'],   p3['modelB']['k'],   p3['modelC']['k']]
    aicc_min = min(aiccs)
    deltas = [a - aicc_min for a in aiccs]
    bars = ax.bar(names, deltas, color=['green', 'blue', 'red'], alpha=0.7)
    for bar, chi2_v, k in zip(bars, chi2s, ks):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f"chi2={chi2_v:.1f}\nk={k}", ha='center', fontsize=9)
    ax.axhline(2, color='orange', ls='--', label='Delta=2 (tied)')
    ax.axhline(10, color='red', ls='--', label='Delta=10 (decisive)')
    ax.set_ylabel('Delta AICc (lower = better)')
    ax.set_title('(e) Phase 3: AICc Delta from best')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (f) Verdict text
    ax = axes[1, 2]
    ax.axis('off')
    lines = [
        "L68: Measurement Contamination Hypothesis Test",
        "=" * 44,
        "",
        f"Phase 1 (SPARC binning):",
        f"  Overall sigma(log a_0) = {p1['overall_std']:.3f} dex",
        f"  Within-bin (V_max):    {p1['mean_within_std']:.3f} dex",
        f"  Variance reduction:    {100*p1['var_reduction']:.1f}%",
        f"  Verdict: {p1['verdict']}",
        "",
        f"Phase 2 (inflated systematics):",
        f"  spread = {p2['spread_dex']:.2f} dex (max-min)",
        f"  required syst per chan = {p2['syst_required']:.2f} dex",
        f"  vs literature ~0.06 dex -> {p2['syst_required']/0.06:.1f}x",
        f"  chi^2/dof = {p2['chi2']/p2['dof']:.2f}",
        f"  Verdict: {p2['verdict']}",
        "",
        f"Phase 3 (AICc):",
        f"  Best model: {p3['ranking'][0][0]}",
    ]
    for n, a in p3['ranking']:
        delta = a - p3['ranking'][0][1]
        lines.append(f"  {n:18s}: AICc={a:.2f}  Delta={delta:+.2f}")

    lines += [
        "",
        "Interpretation:",
    ]
    best = p3['ranking'][0][0]
    if 'A_single' in best:
        lines.append("  Single sigma_0 + path systematics WINS.")
        lines.append("  Non-monotonicity may be measurement artifact.")
    elif 'B_monotonic' in best:
        lines.append("  Simple monotonic gating WINS.")
        lines.append("  Single threshold sufficient.")
    else:
        lines.append("  Resonance/non-monotonic WINS.")
        lines.append("  Genuine non-monotonic pattern.")

    ax.text(0.02, 0.98, "\n".join(lines), family='monospace', fontsize=9,
            transform=ax.transAxes, va='top')

    plt.suptitle('L68: 3-Phase test of measurement-contamination hypothesis',
                 fontsize=13)
    plt.tight_layout()
    plt.savefig(OUT / 'L68_main.png', dpi=140, bbox_inches='tight')
    plt.close()
    print(f"\n  Saved: {OUT/'L68_main.png'}")

# ============================================================
# Main
# ============================================================
def _jsonify(o):
    if isinstance(o, (np.bool_, bool)): return bool(o)
    if isinstance(o, (np.integer, int)): return int(o)
    if isinstance(o, (np.floating, float)): return float(o)
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, dict): return {k: _jsonify(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_jsonify(x) for x in o]
    return o

if __name__ == "__main__":
    p1 = phase1_sparc_binning()
    p2 = phase2_systematics_inflation(p1)
    p3 = phase3_aicc(p1, p2)

    visualize(p1, p2, p3)

    # Strip per-galaxy details from p1 for json
    p1_save = {k: v for k, v in p1.items() if k != 'per_galaxy'}
    report = dict(phase1=p1_save, phase2=p2, phase3=p3)
    with open(OUT / 'report.json', 'w') as f:
        json.dump(_jsonify(report), f, indent=2)
    print(f"  Saved: {OUT/'report.json'}")

    print("\n" + "=" * 60)
    print("L68 DONE")
    print("=" * 60)
