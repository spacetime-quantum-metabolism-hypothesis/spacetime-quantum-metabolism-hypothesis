#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L69 Step 2/3 — Spectrum integration + Branch A/B AICc comparison
=================================================================
Step 1 found: SPARC log10(sigma_0) median=9.56, std=0.66 dex (Q in {1,2}, n=163).
              Multivariate R^2 with catalog vars = 0.262 (74% intrinsic).
              => measurement contamination NOT dominant. The non-monotonic
                 spectrum across cosmic/cluster/galactic is robust.

Step 2: Combine SPARC distribution with T17/T20 evidence:
  - Cosmic    (T17)  : log sigma = 8.37 +- 0.06 (Cepheid/TRGB syst)
  - Cluster   (T20)  : log sigma = 7.75 +- 0.06 (HMcode/AGN syst)
  - Galactic  (SPARC): use median +- std/sqrt(n_eff) for the central
                       value, plus the per-galaxy distribution itself.

Step 3 (Branch A): Non-monotonic axiom function families
  A1 single Gaussian peak in log_rho (=resonance peak at galactic density)
  A2 single Gaussian peak in log_Vflat (=resonance in dynamical scale)
  A3 piecewise-linear breakpoint (bound vs unbound transition)
  A4 dim-power law: sigma_0 ~ rho^alpha (single param, allows non-monotonic
     ONLY if alpha is environment-dependent; included as monotonic baseline)

Step 3 (Branch B): Per-regime phenomenology (3 free sigma_0)
  B  three independent sigma_0 (cosmic / cluster / galactic) — k=3

AICc comparison on 3 anchor points + SPARC distribution:
  log L ~ -0.5 sum chi^2 over 3 anchors
  N_eff = 3 (we use the 3 anchor measurements, treating SPARC as one
  galactic point with std/sqrt(n) error bar)

================================================================
4-Team review (P / N / O / H), recorded BEFORE running:
================================================================
P (theory):
  - The non-monotonic spectrum (cosmic 8.37, cluster 7.75, galactic 9.56)
    has a CLUSTER MINIMUM. Any successful axiom must produce a dip at
    cluster density.
  - Resonance models (A1, A2) naturally produce dips. Compare locations.
N (numeric):
  - 3 anchor points + 3-5 free params: AICc penalty ~2k. Need careful
    interpretation when N - k - 1 small.
  - Use chi^2 with anchor errors; SPARC error = std/sqrt(n_q).
O (observation):
  - SPARC anchor = log(sigma_med)=9.56, error = 0.66/sqrt(163)=0.052 dex.
  - With 0.05 dex error, even small mismatches create big chi^2.
H (self-consistency hunter, STRONG):
  > Pre-prediction: Branch B (3 free) wins absolute fit (chi^2~0).
  > AICc penalty: 2*3=6 vs Branch A k=2: 4. Delta=2 favors B; but
    if B+penalty > A_chi^2 + 4, A wins.
  > A1 (Gaussian peak in rho) prediction: peak at log_rho ~= -22 (between
    cluster and galaxy), wide enough to fit cosmic on the tail.
================================================================
"""

import os
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import json
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import minimize, differential_evolution

ROOT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis")
OUT = ROOT / "results/L69"
OUT.mkdir(parents=True, exist_ok=True)

# ============================================================
# Step 2: anchor data (cosmic, cluster, galactic)
# ============================================================
# log10(sigma_0) anchors with conservative literature systematics
# galactic: take median from L69 step1 sample (read from json)
import sys

step1_path = OUT / 'l69_step1_report.json'
if step1_path.exists():
    with open(step1_path) as f:
        step1 = json.load(f)
    SPARC_LOG_SIGMA_MED = step1['log_sigma_mean']  # mean of distribution
    SPARC_LOG_SIGMA_STD = step1['log_sigma_std']
    SPARC_N             = step1['n_galaxies']
else:
    SPARC_LOG_SIGMA_MED = 9.557
    SPARC_LOG_SIGMA_STD = 0.660
    SPARC_N             = 163

ANCHORS = {
    # name: (log_sigma, sys_dex, log_rho, log_Vflat)
    'cosmic'  : (8.37,  0.06, np.log10(2.7e-27), np.log10(1.0)),
    'cluster' : (7.75,  0.06, np.log10(2.7e-24), np.log10(1000.0)),
    'galactic': (SPARC_LOG_SIGMA_MED,
                 SPARC_LOG_SIGMA_STD / np.sqrt(SPARC_N),
                 np.log10(1.7e-21), np.log10(150.0)),
}
print("Anchors (log_sigma_0, error_dex, log_rho, log_Vflat):")
for k, v in ANCHORS.items():
    print(f"  {k:9s}: log_sig={v[0]:.3f} +- {v[1]:.4f}, "
          f"log_rho={v[2]:.2f}, log_Vflat={v[3]:.2f}")

log_sig = np.array([ANCHORS[k][0] for k in ['cosmic','cluster','galactic']])
err_sig = np.array([ANCHORS[k][1] for k in ['cosmic','cluster','galactic']])
log_rho = np.array([ANCHORS[k][2] for k in ['cosmic','cluster','galactic']])
log_Vfl = np.array([ANCHORS[k][3] for k in ['cosmic','cluster','galactic']])

N_DATA = len(log_sig)

# ============================================================
# Step 3 — Models
# ============================================================
def model_A1(params, x):
    """Gaussian peak in log_rho. params=(log_sigma_peak, log_rho_peak, width)"""
    s_peak, r_peak, w = params
    if w < 0.05 or w > 10: return np.full_like(x, 1e10)
    return s_peak - 0.5 * ((x - r_peak) / w)**2

def model_A2(params, x):
    """Gaussian peak in log_Vflat."""
    s_peak, V_peak, w = params
    if w < 0.05 or w > 5: return np.full_like(x, 1e10)
    return s_peak - 0.5 * ((x - V_peak) / w)**2

def model_A3(params, x):
    """V-shape (piecewise-linear with breakpoint)."""
    s_min, x_min, m_left, m_right = params
    out = np.where(x < x_min,
                   s_min + m_left  * (x - x_min),
                   s_min + m_right * (x - x_min))
    return out

def model_A4(params, x):
    """Single power law (monotonic baseline)."""
    a, b = params
    return a + b * x

def model_B(params, x):
    """Three independent values, x ignored. params: (s_cosmic, s_cluster, s_galactic)"""
    return np.array(params)

# ============================================================
# Fit each model
# ============================================================
def chi2_of(model_fn, params, x, y, err):
    pred = model_fn(params, x)
    if not np.all(np.isfinite(pred)):
        return 1e10
    return float(np.sum(((y - pred) / err)**2))

def aicc(chi2_val, k, n):
    if n - k - 1 <= 0:
        return chi2_val + 2 * k + 1e6  # heavy penalty if undefined
    return chi2_val + 2 * k + (2 * k * (k + 1)) / (n - k - 1)

# Use differential evolution for robust global fits
def fit_model(model_fn, k, x, y, err, bounds, label):
    def obj(p):
        return chi2_of(model_fn, p, x, y, err)
    # Global search
    res = differential_evolution(obj, bounds, seed=42, tol=1e-9,
                                  maxiter=400, polish=True)
    chi2_best = float(res.fun)
    a = aicc(chi2_best, k, N_DATA)
    print(f"  {label:30s}: chi2={chi2_best:8.3f}, k={k}, AICc={a:8.3f}, "
          f"params={[round(p,3) for p in res.x]}")
    return dict(label=label, params=res.x.tolist(), chi2=chi2_best,
                k=k, AICc=float(a))

print("\n" + "=" * 60)
print("Step 3: Fit models on 3 anchor points (cosmic/cluster/galactic)")
print("=" * 60)

results = []

# A1 Gaussian on rho
results.append(fit_model(
    lambda p, x: model_A1(p, x), 3, log_rho, log_sig, err_sig,
    bounds=[(7, 11), (-28, -19), (0.5, 8.0)],
    label='A1 Gaussian-peak in log_rho'))

# A2 Gaussian on Vflat
results.append(fit_model(
    lambda p, x: model_A2(p, x), 3, log_Vfl, log_sig, err_sig,
    bounds=[(7, 11), (-1, 5), (0.2, 5.0)],
    label='A2 Gaussian-peak in log_Vflat'))

# A3 V-shape on rho
results.append(fit_model(
    lambda p, x: model_A3(p, x), 4, log_rho, log_sig, err_sig,
    bounds=[(6, 10), (-26, -20), (-3, 3), (-3, 3)],
    label='A3 V-shape on log_rho'))

# A4 monotonic power law
results.append(fit_model(
    lambda p, x: model_A4(p, x), 2, log_rho, log_sig, err_sig,
    bounds=[(-50, 50), (-3, 3)],
    label='A4 monotonic linear (rho)'))

# B 3-regime independent
results.append(dict(
    label='B 3-regime independent', params=log_sig.tolist(),
    chi2=0.0, k=3, AICc=float(aicc(0.0, 3, N_DATA))))
print(f"  {'B 3-regime independent':30s}: chi2=   0.000, k=3, AICc={results[-1]['AICc']:8.3f}")

# Sort by AICc
results.sort(key=lambda r: r['AICc'])
print("\nRanking (lowest AICc = best):")
ai_min = results[0]['AICc']
for r in results:
    delta = r['AICc'] - ai_min
    print(f"  {r['label']:30s}  AICc={r['AICc']:8.3f}  Delta={delta:+8.3f}")

# ============================================================
# Visualization
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(20, 11))

# (a) Anchors with error bars + best A1 fit
ax = axes[0, 0]
ax.errorbar(log_rho, log_sig, yerr=err_sig, fmt='ks', markersize=12,
            capsize=8, label='anchors', zorder=5)
labels_x = ['cosmic', 'cluster', 'galactic']
for x, y, lbl in zip(log_rho, log_sig, labels_x):
    ax.annotate(lbl, (x, y), textcoords='offset points', xytext=(8, 8))
xs = np.linspace(-28, -19, 200)
for r in results:
    if 'A1' in r['label']:
        ax.plot(xs, model_A1(r['params'], xs), 'b-', lw=2,
                label=f"A1 (chi^2={r['chi2']:.1f})")
    elif 'A3' in r['label']:
        ax.plot(xs, model_A3(r['params'], xs), 'g--', lw=2,
                label=f"A3 V-shape (chi^2={r['chi2']:.1f})")
    elif 'A4' in r['label']:
        ax.plot(xs, model_A4(r['params'], xs), 'r:', lw=2,
                label=f"A4 monotonic (chi^2={r['chi2']:.1f})")
ax.set_xlabel('log10(rho) [kg/m^3]')
ax.set_ylabel('log10(sigma_0)')
ax.set_title('(a) sigma_0 vs density: density-based models')
ax.legend(fontsize=9)
ax.grid(alpha=0.3)

# (b) A2 fit (Vflat axis)
ax = axes[0, 1]
ax.errorbar(log_Vfl, log_sig, yerr=err_sig, fmt='ks', markersize=12,
            capsize=8, label='anchors')
for x, y, lbl in zip(log_Vfl, log_sig, labels_x):
    ax.annotate(lbl, (x, y), textcoords='offset points', xytext=(8, 8))
xs = np.linspace(-1, 4, 200)
for r in results:
    if 'A2' in r['label']:
        ax.plot(xs, model_A2(r['params'], xs), 'b-', lw=2,
                label=f"A2 Gaussian-Vflat (chi^2={r['chi2']:.1f})")
ax.set_xlabel('log10(V_flat) [km/s]')
ax.set_ylabel('log10(sigma_0)')
ax.set_title('(b) sigma_0 vs Vflat: Gaussian peak')
ax.legend(fontsize=9)
ax.grid(alpha=0.3)

# (c) AICc bar
ax = axes[0, 2]
labels = [r['label'].split()[0] for r in results]
aiccs = [r['AICc'] for r in results]
chi2s = [r['chi2'] for r in results]
ks = [r['k'] for r in results]
deltas = [a - aiccs[0] for a in aiccs]
colors = ['green' if d == 0 else ('orange' if d < 4 else 'red') for d in deltas]
bars = ax.bar(labels, deltas, color=colors, alpha=0.7)
for bar, c2, k in zip(bars, chi2s, ks):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f"chi2={c2:.1f}\nk={k}", ha='center', fontsize=8)
ax.axhline(2, color='orange', ls='--', label='Delta=2')
ax.axhline(10, color='red', ls='--', label='Delta=10')
ax.set_ylabel('Delta AICc from best')
ax.set_title('(c) AICc model comparison')
plt.setp(ax.xaxis.get_majorticklabels(), rotation=20)
ax.legend(fontsize=8)
ax.grid(alpha=0.3, axis='y')

# (d) SPARC distribution + anchors
ax = axes[1, 0]
if step1_path.exists():
    sparc_logs = np.array([row['log_sigma'] for row in step1['rows']])
    ax.hist(sparc_logs, bins=30, alpha=0.6, color='tab:blue',
            edgecolor='black', label=f'SPARC (n={len(sparc_logs)})')
ax.axvline(8.37, color='gray', ls=':', lw=2,
           label='T17 cosmic = 8.37')
ax.axvline(7.75, color='red', ls=':', lw=2,
           label='T20 cluster = 7.75')
ax.axvline(SPARC_LOG_SIGMA_MED, color='blue', ls='--', lw=2,
           label=f'SPARC median = {SPARC_LOG_SIGMA_MED:.2f}')
ax.set_xlabel('log10(sigma_0)')
ax.set_ylabel('N galaxies')
ax.set_title('(d) sigma_0 spectrum: SPARC + anchors')
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

# (e) Best vs worst model fit comparison
ax = axes[1, 1]
xs = np.linspace(-28, -19, 200)
ax.errorbar(log_rho, log_sig, yerr=err_sig, fmt='ks', markersize=14,
            capsize=8, label='data', zorder=10)
# Best (lowest AICc)
best = results[0]
ax.axhline(0, alpha=0)  # placeholder
if 'A1' in best['label']:
    ax.plot(xs, model_A1(best['params'], xs), 'g-', lw=2.5,
            label=f"BEST: {best['label'].split()[0]}")
elif 'A3' in best['label']:
    ax.plot(xs, model_A3(best['params'], xs), 'g-', lw=2.5,
            label=f"BEST: {best['label'].split()[0]}")
elif 'A4' in best['label']:
    ax.plot(xs, model_A4(best['params'], xs), 'g-', lw=2.5,
            label=f"BEST: {best['label'].split()[0]}")
elif 'B' in best['label']:
    for x, s in zip(log_rho, best['params']):
        ax.plot([x-0.5, x+0.5], [s, s], 'g-', lw=3, label='BEST: B regime')
# Worst
worst = results[-1]
if 'A4' in worst['label']:
    ax.plot(xs, model_A4(worst['params'], xs), 'r:', lw=2,
            label=f"WORST: {worst['label'].split()[0]}")
ax.set_xlabel('log10(rho) [kg/m^3]')
ax.set_ylabel('log10(sigma_0)')
ax.set_title('(e) Best vs worst model on rho axis')
ax.legend(fontsize=9)
ax.grid(alpha=0.3)

# (f) Verdict
ax = axes[1, 2]
ax.axis('off')
lines = [
    "L69 Step 2/3 - Non-monotonic spectrum analysis",
    "=" * 44,
    "",
    "Anchor points:",
]
for k, v in ANCHORS.items():
    lines.append(f"  {k:9s}: log sig = {v[0]:.2f} +- {v[1]:.3f}")
lines += [
    "",
    "Model AICc ranking:",
]
for r in results:
    delta = r['AICc'] - results[0]['AICc']
    lines.append(f"  {r['label']:30s}")
    lines.append(f"      chi2={r['chi2']:.2f} k={r['k']} dAICc={delta:+.2f}")

lines += [
    "",
    "Branch interpretation:",
]
best = results[0]
if 'B' in best['label']:
    lines.append("  Branch B (3-regime phenomenology) wins.")
    lines.append("  3 independent sigma_0 values per regime.")
    lines.append("  No single-axiom theory simpler than 3-regime.")
elif 'A' in best['label']:
    lines.append(f"  Branch A wins via {best['label'].split()[0]}.")
    if 'A1' in best['label']:
        s_pk, r_pk, w = best['params']
        lines.append(f"  log_sig peaks at log_rho={r_pk:.2f}")
        lines.append(f"  peak height = {s_pk:.2f}, width = {w:.2f} dex")
    elif 'A2' in best['label']:
        s_pk, V_pk, w = best['params']
        lines.append(f"  log_sig peaks at log_Vflat={V_pk:.2f}")
        lines.append(f"  (Vflat~{10**V_pk:.0f} km/s)")
    elif 'A3' in best['label']:
        s_min, x_min, m_l, m_r = best['params']
        lines.append(f"  V-shape with minimum at log_rho={x_min:.2f}")
    elif 'A4' in best['label']:
        lines.append("  Monotonic linear is best (surprise!)")

ax.text(0.02, 0.98, "\n".join(lines), family='monospace', fontsize=9,
        transform=ax.transAxes, va='top')

plt.suptitle('L69 Step 2/3: spectrum integration + AICc model comparison',
             fontsize=13)
plt.tight_layout()
plt.savefig(OUT / 'L69_step23.png', dpi=140, bbox_inches='tight')
plt.close()
print(f"\nSaved: {OUT/'L69_step23.png'}")

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
    anchors={k: dict(log_sigma=v[0], err=v[1], log_rho=v[2], log_Vflat=v[3])
             for k, v in ANCHORS.items()},
    sparc_log_sigma_mean=SPARC_LOG_SIGMA_MED,
    sparc_log_sigma_std=SPARC_LOG_SIGMA_STD,
    sparc_n=SPARC_N,
    models=results,
    best=results[0]['label'],
    delta_aicc_to_2nd=results[1]['AICc'] - results[0]['AICc'],
)
with open(OUT / 'l69_step23_report.json', 'w') as f:
    json.dump(_j(report), f, indent=2)
print(f"Saved: {OUT/'l69_step23_report.json'}")

print("\n" + "=" * 60)
print("L69 Step 2/3 DONE")
print(f"BEST MODEL: {results[0]['label']}")
print("=" * 60)
