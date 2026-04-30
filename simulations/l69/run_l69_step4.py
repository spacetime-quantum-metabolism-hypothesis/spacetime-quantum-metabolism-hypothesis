#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L69 Step 4 — Full-data AICc on 165 points (163 SPARC + cosmic + cluster)
=========================================================================
Step 2/3 fits on 3 anchor points were under-determined (chi^2=0 with k=3).
This step uses the full 163 SPARC galaxies as individual data points,
each with its own Vflat. Anchor points get appropriate down-weighting
(error = inverse-variance scale of SPARC sample).

Models (predict log_sigma_0 from environment):
  M1 single sigma_0  (k=1)               — null/baseline
  M2 monotonic in log Vflat   (k=2)      — linear
  M3 monotonic in log rho     (k=2)      — linear
  M4 Gaussian peak in log Vflat (k=3)    — A2 from step 2/3
  M5 Gaussian peak in log rho   (k=3)    — A1 from step 2/3
  M6 V-shape on log rho       (k=4)      — A3
  M7 3-regime independent    (k=3)       — B (cosmic, cluster, galactic
                                            galactic = SPARC median)

For SPARC galaxies, the env variable is taken from the catalog (Vflat or
inferred rho via M_HI/V_flat or simpler V_flat as proxy). For cosmic/
cluster anchors, env values are the standard regime values.

Important: each SPARC galaxy contributes one (sigma_0, Vflat, rho_proxy)
data point with measurement error = SPARC_LOG_SIGMA_STD / sqrt(2) per
galaxy (heuristic per-fit floor).

================================================================
4-Team review (P / N / O / H), recorded BEFORE running:
================================================================
P: Per-galaxy data forces axiom prediction to fit the SPARC scatter,
   not just the median. This is much more discriminating.
N: error per SPARC galaxy ~ 0.5 dex (heuristic). With n=163, the
   anchor points (cosmic, cluster) need explicit weights to not be
   washed out. We weight them by 1/err^2 from their literature systs.
O: This pre-supposes that SPARC galaxies are individual samples from
   the underlying sigma_0(env) function. Each Vflat value matters.
H (STRONG):
  > "Peak-in-Vflat (M4) prediction: ALL SPARC galaxies with Vflat~25
    km/s should have higher sigma_0 than galaxies with Vflat~250.
    Step 1 showed slope -0.7 (R^2=0.055). M4 prediction has nonlinear
    structure. Test: does M4 explain SPARC scatter WITH the cosmic and
    cluster anchors? Goodness of fit informative."
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
from scipy.optimize import differential_evolution

ROOT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis")
OUT = ROOT / "results/L69"
OUT.mkdir(parents=True, exist_ok=True)

# Load Step 1 SPARC data
with open(OUT / 'l69_step1_report.json') as f:
    step1 = json.load(f)
SPARC_ROWS = step1['rows']
SPARC_LOG_SIGMA_STD = step1['log_sigma_std']  # 0.66 dex

# Anchors (cosmic, cluster)
ANCHORS = [
    # name, log_sigma, err, log_rho, log_Vflat
    ('cosmic',  8.37, 0.06, np.log10(2.7e-27), np.log10(1.0)),
    ('cluster', 7.75, 0.06, np.log10(2.7e-24), np.log10(1000.0)),
]

# SPARC: filter Vflat present (n=129)
sparc = [r for r in SPARC_ROWS if r.get('Vflat') and r['Vflat'] > 0]
print(f"SPARC with Vflat: {len(sparc)}")

# Per-galaxy err: take the per-fit residual std as err = SPARC_LOG_SIGMA_STD
# (a generous per-galaxy intrinsic scatter)
SPARC_GAL_ERR = SPARC_LOG_SIGMA_STD     # ~0.66 dex per galaxy

# Build combined data arrays
log_sigma  = np.concatenate([
    np.array([a[1] for a in ANCHORS]),
    np.array([r['log_sigma'] for r in sparc])
])
err        = np.concatenate([
    np.array([a[2] for a in ANCHORS]),
    np.full(len(sparc), SPARC_GAL_ERR)
])
log_rho    = np.concatenate([
    np.array([a[3] for a in ANCHORS]),
    np.array([np.log10(1.7e-21)] * len(sparc))    # all SPARC at galactic regime rho
])
log_Vflat  = np.concatenate([
    np.array([a[4] for a in ANCHORS]),
    np.array([np.log10(r['Vflat']) for r in sparc])
])
N = len(log_sigma)
N_anchor = len(ANCHORS)
N_sparc = len(sparc)
print(f"Total data points: {N} ({N_anchor} anchors + {N_sparc} SPARC)")

# ============================================================
# Models
# ============================================================
def m1_const(p, x_rho, x_V):
    return np.full_like(x_rho, p[0])

def m2_lin_V(p, x_rho, x_V):
    return p[0] + p[1] * x_V

def m3_lin_rho(p, x_rho, x_V):
    return p[0] + p[1] * x_rho

def m4_peak_V(p, x_rho, x_V):
    s, V0, w = p
    if w < 0.05 or w > 5: return np.full_like(x_V, 1e10)
    return s - 0.5 * ((x_V - V0) / w)**2

def m5_peak_rho(p, x_rho, x_V):
    s, r0, w = p
    if w < 0.05 or w > 10: return np.full_like(x_rho, 1e10)
    return s - 0.5 * ((x_rho - r0) / w)**2

def m6_Vshape_rho(p, x_rho, x_V):
    s_min, x0, m_l, m_r = p
    return np.where(x_rho < x0,
                    s_min + m_l * (x_rho - x0),
                    s_min + m_r * (x_rho - x0))

def m7_3regime(p, x_rho, x_V):
    s_cosm, s_clust, s_gal = p
    out = np.empty_like(x_rho)
    # cosmic if log_rho < -25
    # cluster if -25 <= log_rho < -22
    # galactic else
    out[:] = s_gal
    out[x_rho < -25] = s_cosm
    out[(x_rho >= -25) & (x_rho < -22)] = s_clust
    return out

MODELS = [
    ('M1 const',         m1_const,      1, [(7, 11)]),
    ('M2 linear-Vflat',  m2_lin_V,      2, [(0, 20), (-3, 3)]),
    ('M3 linear-rho',    m3_lin_rho,    2, [(-50, 50), (-3, 3)]),
    ('M4 peak-Vflat',    m4_peak_V,     3, [(7, 12), (-1, 5), (0.1, 5.0)]),
    ('M5 peak-rho',      m5_peak_rho,   3, [(7, 12), (-28, -19), (0.5, 8.0)]),
    ('M6 Vshape-rho',    m6_Vshape_rho, 4, [(6, 11), (-26, -20), (-3, 3), (-3, 3)]),
    ('M7 3-regime',      m7_3regime,    3, [(7, 11), (6, 10), (8, 11)]),
]

# ============================================================
# Fit and AICc (proper)
# ============================================================
def chi2(model_fn, p, x_rho, x_V, y, e):
    pred = model_fn(p, x_rho, x_V)
    if not np.all(np.isfinite(pred)):
        return 1e10
    return float(np.sum(((y - pred) / e)**2))

def aicc(c2, k, n):
    """Standard AICc (Hurvich-Tsai 1989). n - k - 1 must be > 0."""
    if n - k - 1 <= 0:
        # fallback to AIC
        return c2 + 2 * k
    return c2 + 2 * k + (2 * k * (k + 1)) / (n - k - 1)

def fit(label, model_fn, k, bounds):
    def obj(p):
        return chi2(model_fn, p, log_rho, log_Vflat, log_sigma, err)
    res = differential_evolution(obj, bounds, seed=42, tol=1e-9,
                                  maxiter=600, polish=True)
    c2 = float(res.fun)
    a = aicc(c2, k, N)
    bic = c2 + k * np.log(N)
    return dict(label=label, params=res.x.tolist(), chi2=c2,
                k=k, AICc=float(a), BIC=float(bic),
                chi2_per_dof=c2 / max(N - k, 1))

print("\n" + "=" * 60)
print(f"Fitting on {N} total points (n_dof = N - k)")
print("=" * 60)
results = []
for label, mf, k, b in MODELS:
    r = fit(label, mf, k, b)
    print(f"  {label:22s}: chi2={r['chi2']:8.2f}  k={k}  "
          f"chi2/dof={r['chi2_per_dof']:6.3f}  AICc={r['AICc']:8.2f}  BIC={r['BIC']:8.2f}")
    results.append(r)

results_sorted = sorted(results, key=lambda r: r['AICc'])
ai_min = results_sorted[0]['AICc']
print(f"\nAICc Ranking (delta = AICc - best):")
for r in results_sorted:
    delta = r['AICc'] - ai_min
    print(f"  {r['label']:22s}  dAICc={delta:+8.2f}  chi2={r['chi2']:7.2f}  k={r['k']}")

# ============================================================
# Visualization
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(20, 11))

# (a) sigma vs Vflat with data + best models
ax = axes[0, 0]
ax.scatter(log_Vflat[N_anchor:], log_sigma[N_anchor:], alpha=0.3,
           color='tab:blue', s=20, label=f'SPARC (n={N_sparc})')
ax.errorbar(log_Vflat[:N_anchor], log_sigma[:N_anchor], yerr=err[:N_anchor],
            fmt='ks', markersize=14, capsize=8, label='cosmic/cluster anchors',
            zorder=10)
xs = np.linspace(-1, 4, 200)
xrho_dummy = np.full_like(xs, -22.0)
for r in results:
    if 'M4' in r['label']:
        ax.plot(xs, m4_peak_V(r['params'], xrho_dummy, xs), 'r-', lw=2,
                label=f"M4 peak-Vflat (chi^2={r['chi2']:.0f})")
    if 'M2' in r['label']:
        ax.plot(xs, m2_lin_V(r['params'], xrho_dummy, xs), 'g--', lw=2,
                label=f"M2 linear (chi^2={r['chi2']:.0f})")
ax.set_xlabel('log10(V_flat) [km/s]')
ax.set_ylabel('log10(sigma_0)')
ax.set_title(f'(a) sigma_0 vs Vflat (n={N})')
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

# (b) sigma vs rho with anchors
ax = axes[0, 1]
ax.scatter(log_rho[N_anchor:], log_sigma[N_anchor:], alpha=0.3,
           color='tab:blue', s=20, label=f'SPARC at log_rho=-20.77')
ax.errorbar(log_rho[:N_anchor], log_sigma[:N_anchor], yerr=err[:N_anchor],
            fmt='ks', markersize=14, capsize=8, label='cosmic/cluster anchors',
            zorder=10)
xs = np.linspace(-28, -19, 200)
xV_dummy = np.full_like(xs, 2.0)
for r in results:
    if 'M5' in r['label']:
        ax.plot(xs, m5_peak_rho(r['params'], xs, xV_dummy), 'r-', lw=2,
                label=f"M5 peak-rho (chi^2={r['chi2']:.0f})")
    if 'M6' in r['label']:
        ax.plot(xs, m6_Vshape_rho(r['params'], xs, xV_dummy), 'm:', lw=2,
                label=f"M6 V-shape (chi^2={r['chi2']:.0f})")
    if 'M7' in r['label']:
        ax.plot(xs, m7_3regime(r['params'], xs, xV_dummy), 'g-.', lw=2,
                label=f"M7 3-regime (chi^2={r['chi2']:.0f})")
ax.set_xlabel('log10(rho) [kg/m^3]')
ax.set_ylabel('log10(sigma_0)')
ax.set_title('(b) sigma_0 vs density')
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

# (c) AICc ranking
ax = axes[0, 2]
labels = [r['label'].split()[0] for r in results_sorted]
deltas = [r['AICc'] - ai_min for r in results_sorted]
chi2s  = [r['chi2'] for r in results_sorted]
ks     = [r['k'] for r in results_sorted]
colors = ['green' if d == 0 else ('orange' if d < 4 else 'red') for d in deltas]
bars = ax.bar(labels, deltas, color=colors, alpha=0.7)
for bar, c2, k in zip(bars, chi2s, ks):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(deltas)*0.02,
            f"chi2={c2:.0f}\nk={k}", ha='center', fontsize=8)
ax.axhline(2, color='orange', ls='--', label='Delta=2')
ax.axhline(10, color='red', ls='--', label='Delta=10')
ax.set_ylabel('Delta AICc from best')
ax.set_title('(c) AICc model ranking')
plt.setp(ax.xaxis.get_majorticklabels(), rotation=20)
ax.legend(fontsize=8)
ax.grid(alpha=0.3, axis='y')

# (d) chi2 per dof (should be ~1 for good model)
ax = axes[1, 0]
labels2 = [r['label'].split()[0] for r in results_sorted]
chi2_dof = [r['chi2_per_dof'] for r in results_sorted]
bars = ax.bar(labels2, chi2_dof, color='tab:purple', alpha=0.7)
for bar, v in zip(bars, chi2_dof):
    ax.text(bar.get_x() + bar.get_width()/2, v + max(chi2_dof)*0.02,
            f'{v:.2f}', ha='center', fontsize=8)
ax.axhline(1.0, color='green', ls='--', label='chi^2/dof=1')
ax.axhline(2.0, color='orange', ls='--', label='chi^2/dof=2')
ax.set_ylabel('chi^2 / dof')
ax.set_title('(d) Goodness of fit')
plt.setp(ax.xaxis.get_majorticklabels(), rotation=20)
ax.legend(fontsize=8)
ax.grid(alpha=0.3, axis='y')

# (e) residuals from best model
ax = axes[1, 1]
best = results_sorted[0]
# recompute predictions
for label, mf, k, _ in MODELS:
    if label == best['label']:
        pred = mf(best['params'], log_rho, log_Vflat)
        break
residuals = log_sigma - pred
ax.scatter(log_Vflat, residuals, alpha=0.4, color='tab:red', s=25,
           label=f"residuals from {best['label']}")
ax.errorbar(log_Vflat[:N_anchor], residuals[:N_anchor], yerr=err[:N_anchor],
            fmt='ks', markersize=10, capsize=6, label='anchor residuals')
ax.axhline(0, color='black')
ax.set_xlabel('log10(V_flat)')
ax.set_ylabel('residual log10(sigma_0)')
ax.set_title(f'(e) Residuals from best model: {best["label"]}\n'
             f'std={np.std(residuals):.3f} dex')
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

# (f) verdict
ax = axes[1, 2]
ax.axis('off')
lines = [
    f"L69 Step 4: AICc on {N} data points",
    "=" * 42,
    "",
    f"Data: {N_anchor} anchors + {N_sparc} SPARC galaxies",
    f"Galactic anchor err = SPARC_std/sqrt(n)",
    f"SPARC galaxy err     = {SPARC_GAL_ERR:.2f} dex (intrinsic+fit)",
    "",
    "AICc Ranking:",
]
for r in results_sorted:
    delta = r['AICc'] - ai_min
    lines.append(f"  {r['label']:22s} dAICc={delta:+7.1f} k={r['k']}")

lines += [
    "",
    "Goodness chi^2/dof:",
]
for r in results_sorted:
    lines.append(f"  {r['label']:22s} {r['chi2_per_dof']:.3f}")

best_short = results_sorted[0]['label']
chi2_dof_best = results_sorted[0]['chi2_per_dof']
lines += [
    "",
    f"BEST: {best_short}",
    f"chi^2/dof = {chi2_dof_best:.3f}",
]

if 'M4' in best_short or 'M5' in best_short:
    lines.append("=> Branch A (resonance) WINS")
    lines.append("=> Non-monotonic axiom validated")
elif 'M7' in best_short:
    lines.append("=> Branch B (3-regime) WINS")
    lines.append("=> Per-regime phenomenology")
elif 'M6' in best_short:
    lines.append("=> A V-shape WINS (4 params)")
elif 'M2' in best_short or 'M3' in best_short:
    lines.append("=> Linear monotonic survives")
    lines.append("(SPARC pulls toward linear trend)")
else:
    lines.append("=> Constant null wins")
    lines.append("(no env dependence detected)")

if chi2_dof_best > 2:
    lines.append(f"WARNING: chi^2/dof = {chi2_dof_best:.2f} > 2,")
    lines.append("absolute fit poor; conclusions tentative.")

ax.text(0.02, 0.98, "\n".join(lines), family='monospace', fontsize=9,
        transform=ax.transAxes, va='top')

plt.suptitle(f'L69 Step 4: Full-data AICc — best={best["label"]}', fontsize=13)
plt.tight_layout()
plt.savefig(OUT / 'L69_step4.png', dpi=140, bbox_inches='tight')
plt.close()
print(f"\nSaved: {OUT/'L69_step4.png'}")

# Save report
def _j(o):
    if isinstance(o, (np.bool_, bool)): return bool(o)
    if isinstance(o, (np.integer, int)): return int(o)
    if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else None
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, dict): return {k: _j(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_j(x) for x in o]
    return o

report = dict(
    n_total=N, n_anchors=N_anchor, n_sparc=N_sparc,
    sparc_gal_err=SPARC_GAL_ERR,
    models=results_sorted,
    best=results_sorted[0]['label'],
    delta_aicc_to_2nd=results_sorted[1]['AICc'] - results_sorted[0]['AICc'],
    chi2_per_dof_best=results_sorted[0]['chi2_per_dof'],
)
with open(OUT / 'l69_step4_report.json', 'w') as f:
    json.dump(_j(report), f, indent=2)
print(f"Saved: {OUT/'l69_step4_report.json'}")
print("\nDONE")
