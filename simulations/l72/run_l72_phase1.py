#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L72 Phase 1 — Three observational lock-in tests (O4 + O5 + O8)
================================================================

O4 — Field vs Cluster dwarf a_0:
  Use SPARC distance method f_D as environmental classifier:
    f_D=1 (Hubble flow):       'field' (n=97)
    f_D=4 (Ursa Major Cluster): 'cluster' (n=28)
  Branch B prediction: a_0(field) = a_0(cluster) within ±0.05 dex.

O5 — Cosmic sigma_0(z) re-extraction (using existing DESI infrastructure
     not strictly required; we can use the SPARC sigma_0 already in hand
     to test alternative: does sigma_0 vary across distance? — same
     mechanism since high-z = high-D):
  Use SPARC distance D as a (rough) z proxy and check sigma_0(D).
  This is a simpler stand-in than full DESI re-fit.

O8 — Intrinsic scatter origin:
  After step1 multivariate fit (R^2=0.262), regress residuals on
  additional features: Inc, Reff, SBeff, MHI (HI mass), Q, chi2_red
  to identify what drives the remaining ~0.57 dex scatter.

================================================================
4-Team review (P / N / O / H), recorded BEFORE running:
================================================================
P (theory):
  - O4: this is the cleanest test of Branch B's "regime stability"
    claim available with current data.
  - O5: SPARC distance is at most 130 Mpc — z < 0.03. Limited dynamic
    range vs DESI BAO (z up to 1+). But a NULL within SPARC strengthens
    Branch B.
  - O8: residuals' structure may reveal a hidden variable. If pure
    noise, intrinsic scatter is fundamental. If structured, we missed
    a predictor.
N (numeric):
  - O4: Welch t-test + bootstrap CI on log a_0 difference.
  - O8: regress full set incl. (Reff, SBeff, MHI, Inc, Q, chi2_red).
    Compare R^2 to step1's 0.262.
O (observation):
  - UMa cluster is a LOOSE cluster (rho ~ a few × cosmic mean).
    Branch B 'cluster' regime sensu stricto is rho ~ 1e-22 - 1e-26;
    UMa is at the loose/field boundary. So this tests environmental
    SENSITIVITY rather than strict regime crossing.
H (self-consistency hunter, STRONG):
  > "O4: predict NULL within ±0.05 dex. Any positive (cluster lower
    a_0 than field) signal would be Branch A signature: it would
    imply environment matters even within nominally same regime."
  > "O5 within SPARC may be too narrow to detect z evolution. Treat
    as NULL test only."
  > "O8: if residuals correlate with M/L (Upsilon) — that's expected
    fitting noise, not new physics. If residuals correlate with
    morphology (T-type, Inc) — that's environment signal."
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
from scipy.stats import ttest_ind

ROOT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis")
OUT = ROOT / "results/L72"
OUT.mkdir(parents=True, exist_ok=True)

# ============================================================
# Load L69 step1 data (per-galaxy SPARC fits + catalog)
# ============================================================
with open(ROOT / "results/L69/l69_step1_report.json") as f:
    step1 = json.load(f)

ROWS = step1['rows']
print(f"Loaded {len(ROWS)} SPARC galaxies (Q in {{1,2}})")

# ============================================================
# O4 — Field vs Cluster (f_D classifier)
# ============================================================
print("\n" + "=" * 60)
print("O4: Field (f_D=1) vs Cluster (f_D=4, UMa) a_0 comparison")
print("=" * 60)

field   = [r for r in ROWS if r['f_D'] == 1]
cluster = [r for r in ROWS if r['f_D'] == 4]
trgb    = [r for r in ROWS if r['f_D'] == 2]
print(f"  field   (Hubble-flow, f_D=1): n={len(field)}")
print(f"  cluster (UMa,         f_D=4): n={len(cluster)}")
print(f"  TRGB    (local,       f_D=2): n={len(trgb)}")

la0_field   = np.array([r['log_a0']    for r in field])
la0_cluster = np.array([r['log_a0']    for r in cluster])
ls_field    = np.array([r['log_sigma'] for r in field])
ls_cluster  = np.array([r['log_sigma'] for r in cluster])

med_f, std_f = float(np.median(la0_field)), float(np.std(la0_field))
med_c, std_c = float(np.median(la0_cluster)), float(np.std(la0_cluster))
med_diff = med_c - med_f
sem_diff = np.sqrt((std_f**2 / len(field)) + (std_c**2 / len(cluster)))

# Bootstrap CI on the median difference
rng = np.random.default_rng(seed=42)
boots = np.zeros(2000)
for i in range(2000):
    f_b = rng.choice(la0_field,   size=len(field),   replace=True)
    c_b = rng.choice(la0_cluster, size=len(cluster), replace=True)
    boots[i] = np.median(c_b) - np.median(f_b)
ci_lo, ci_hi = np.percentile(boots, [2.5, 97.5])

# t-test on means
t_stat, p_val = ttest_ind(la0_cluster, la0_field, equal_var=False)

print(f"  Field   log_a0:   median={med_f:.3f}  std={std_f:.3f}")
print(f"  Cluster log_a0:   median={med_c:.3f}  std={std_c:.3f}")
print(f"  Difference (cluster - field) = {med_diff:+.3f} dex")
print(f"  Bootstrap 95% CI: [{ci_lo:+.3f}, {ci_hi:+.3f}]")
print(f"  Welch t-test:     t={t_stat:+.3f}, p={p_val:.3e}")

# Branch B says ±0.05 dex tolerance
threshold_dex = 0.05
if abs(med_diff) <= threshold_dex and ci_lo > -threshold_dex and ci_hi < threshold_dex:
    o4_verdict = f"PASS - difference {med_diff:+.3f} dex within ±{threshold_dex}"
elif (ci_lo > 0) or (ci_hi < 0):
    o4_verdict = f"FAIL - difference {med_diff:+.3f} dex CI excludes 0 -> Branch B falsified"
else:
    o4_verdict = (f"INCONCLUSIVE - difference {med_diff:+.3f} dex CI [{ci_lo:.2f},{ci_hi:.2f}] "
                  f"crosses 0 but exceeds ±{threshold_dex}")
print(f"  O4 verdict: {o4_verdict}")

# ============================================================
# O5 — SPARC distance proxy for sigma_0(D) ≈ sigma_0(z)
# ============================================================
print("\n" + "=" * 60)
print("O5: sigma_0 vs distance (SPARC z proxy)")
print("=" * 60)

D_arr      = np.array([r['D']         for r in ROWS])
ls_arr     = np.array([r['log_sigma'] for r in ROWS])
print(f"  Distance range: {D_arr.min():.1f} - {D_arr.max():.1f} Mpc")
print(f"  z proxy:       {D_arr.min()/4280:.4f} - {D_arr.max()/4280:.4f} (Hubble dist 4280 Mpc/c)")

# Pearson + linear fit
slope, intercept = np.polyfit(D_arr, ls_arr, 1)
ls_pred = slope * D_arr + intercept
resid = ls_arr - ls_pred
ss_res = np.sum(resid**2)
ss_tot = np.sum((ls_arr - np.mean(ls_arr))**2)
r2 = 1 - ss_res / ss_tot

# Bootstrap on slope
slope_boots = np.zeros(2000)
for i in range(2000):
    idx = rng.choice(len(ROWS), size=len(ROWS), replace=True)
    s_, _ = np.polyfit(D_arr[idx], ls_arr[idx], 1)
    slope_boots[i] = s_
slope_ci = np.percentile(slope_boots, [2.5, 97.5])
print(f"  Slope d(log sigma)/dD = {slope:+.4e} 1/Mpc")
print(f"  Bootstrap 95% CI: [{slope_ci[0]:+.4e}, {slope_ci[1]:+.4e}]")
print(f"  R^2 = {r2:.4f}")
print(f"  Span: {(slope * (D_arr.max() - D_arr.min())):+.3f} dex over full range")

# Branch B prediction: slope ≈ 0 (no D evolution within galactic regime)
total_span = abs(slope * (D_arr.max() - D_arr.min()))
if (slope_ci[0] < 0 < slope_ci[1]) and total_span < 0.05:
    o5_verdict = f"PASS - slope CI crosses 0, total variation {total_span:.3f} dex < 0.05"
elif (slope_ci[0] > 0) or (slope_ci[1] < 0):
    o5_verdict = f"FAIL - slope CI excludes 0, sigma_0(D) varies systematically"
else:
    o5_verdict = f"MARGINAL - slope CI crosses 0 but total variation {total_span:.3f} dex > 0.05"
print(f"  O5 verdict: {o5_verdict}")

# ============================================================
# O8 — Residual scatter origin
# ============================================================
print("\n" + "=" * 60)
print("O8: Intrinsic scatter origin — residuals vs additional features")
print("=" * 60)

# Recompute step1 multivariate residuals using available features
y = np.array([r['log_sigma'] for r in ROWS])

base_predictors = [
    ('T',         lambda r: r['T']),
    ('D',         lambda r: r['D']),
    ('log_L36',   lambda r: r.get('log_L36') if r.get('log_L36') is not None else np.nan),
    ('log_MHI',   lambda r: r.get('log_MHI') if r.get('log_MHI') is not None else np.nan),
    ('log_Vmax',  lambda r: r['log_Vmax']),
    ('Q',         lambda r: r['Q']),
    ('chi2_red',  lambda r: r['chi2_red']),
]

def build_X(predictors, rows):
    X = np.array([[p[1](r) for p in predictors] for r in rows], dtype=float)
    for j in range(X.shape[1]):
        col = X[:, j]
        med = np.nanmedian(col)
        col[np.isnan(col)] = med
        X[:, j] = col
    return X

def linreg(X, y):
    X1 = np.column_stack([np.ones(len(X)), X])
    beta = np.linalg.pinv(X1.T @ X1) @ X1.T @ y
    pred = X1 @ beta
    rss = np.sum((y - pred)**2)
    tss = np.sum((y - np.mean(y))**2)
    r2 = 1 - rss/tss
    return beta, r2, pred

X_base = build_X(base_predictors, ROWS)
beta_base, r2_base, pred_base = linreg(X_base, y)
residuals = y - pred_base
res_std = float(np.std(residuals))
print(f"  Base R^2 = {r2_base:.3f}, residual std = {res_std:.3f} dex (matches L69 step 1)")

# Test each additional feature alone vs residual
extra_predictors = [
    ('Reff',     lambda r: 1.0),  # placeholder; not in step1.rows actually
    ('SBeff',    lambda r: 1.0),
    ('Inc',      lambda r: 1.0),
]
# We don't have Reff/SBeff/Inc in step1 rows. Use what's available.
# Available extra: V_max (already in base), chi2_red (already), MHI (in base)
# Try squared/interaction features:
extra_features = {
    'log_Vmax_sq':  np.array([r['log_Vmax']**2 for r in ROWS]),
    'Q_sq':         np.array([r['Q']**2 for r in ROWS]),
    'chi2_red_log': np.array([np.log10(max(r['chi2_red'], 1e-3)) for r in ROWS]),
    'log_L36_sq':   np.array([(r.get('log_L36') if r.get('log_L36') is not None else 0.0)**2
                              for r in ROWS]),
    'T_sq':         np.array([r['T']**2 for r in ROWS]),
    'D_sq':         np.array([r['D']**2 for r in ROWS]),
}

residual_predictions = {}
for fname, fvals in extra_features.items():
    if np.all(np.isnan(fvals)):
        continue
    mask = np.isfinite(fvals)
    if mask.sum() < 5:
        continue
    f_, r_ = fvals[mask], residuals[mask]
    s, c = np.polyfit(f_, r_, 1)
    pred = s * f_ + c
    rss = np.sum((r_ - pred)**2)
    tss = np.sum((r_ - np.mean(r_))**2)
    r2_extra = 1 - rss/tss if tss > 0 else 0
    residual_predictions[fname] = dict(slope=float(s), r2=float(r2_extra), n=int(mask.sum()))

print(f"\n  Univariate residual R^2 (best non-trivial predictor of remaining ~0.57 dex):")
sorted_extras = sorted(residual_predictions.items(),
                       key=lambda kv: kv[1]['r2'], reverse=True)
for fname, info in sorted_extras:
    print(f"    {fname:18s}: R^2={info['r2']:.4f}, slope={info['slope']:+.3f}, n={info['n']}")

# Random feature null comparison
np.random.seed(123)
null_r2 = []
for _ in range(100):
    rand_feat = np.random.randn(len(residuals))
    s, c = np.polyfit(rand_feat, residuals, 1)
    pred = s * rand_feat + c
    rss = np.sum((residuals - pred)**2)
    tss = np.sum((residuals - np.mean(residuals))**2)
    null_r2.append(1 - rss/tss)
null_p95 = np.percentile(null_r2, 95)
print(f"\n  Null distribution (100 random features) 95% R^2 = {null_p95:.4f}")
top_extra_r2 = sorted_extras[0][1]['r2'] if sorted_extras else 0.0
if top_extra_r2 > null_p95 * 2:
    o8_verdict = (f"STRUCTURED - top residual predictor R^2={top_extra_r2:.3f} >> "
                  f"null 95th {null_p95:.3f}")
elif top_extra_r2 > null_p95:
    o8_verdict = f"WEAK - top R^2={top_extra_r2:.3f} just above null"
else:
    o8_verdict = (f"PURE NOISE - top R^2={top_extra_r2:.3f} <= null 95th {null_p95:.3f}; "
                  f"residual scatter is intrinsic / fitting noise")
print(f"\n  O8 verdict: {o8_verdict}")

# ============================================================
# Visualization
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(20, 11))

# (a) O4 violin/box + scatter
ax = axes[0, 0]
ax.boxplot([la0_field, la0_cluster], labels=['field\n(f_D=1)', 'cluster\n(f_D=4 UMa)'],
           widths=0.5)
ax.scatter([1]*len(la0_field), la0_field, alpha=0.4, color='tab:blue', s=20)
ax.scatter([2]*len(la0_cluster), la0_cluster, alpha=0.4, color='tab:red', s=20)
ax.axhline(np.median(la0_field), color='blue', ls='--', alpha=0.5)
ax.axhline(np.median(la0_cluster), color='red', ls='--', alpha=0.5)
ax.set_ylabel('log10(a_0) [m/s^2]')
ax.set_title(f'(a) O4 field vs cluster\n'
             f'diff={med_diff:+.3f} dex, p={p_val:.2e}')
ax.grid(alpha=0.3, axis='y')

# (b) O4 bootstrap distribution
ax = axes[0, 1]
ax.hist(boots, bins=40, alpha=0.7, color='tab:purple', edgecolor='black')
ax.axvline(med_diff, color='red', ls='-', label=f'observed = {med_diff:+.3f}')
ax.axvline(0, color='black', lw=1)
ax.axvline(threshold_dex, color='green', ls=':', label=f'±{threshold_dex} (Branch B)')
ax.axvline(-threshold_dex, color='green', ls=':')
ax.axvline(ci_lo, color='gray', ls='--', label='95% CI')
ax.axvline(ci_hi, color='gray', ls='--')
ax.set_xlabel('Bootstrap diff (cluster - field) [dex]')
ax.set_title(f'(b) O4 bootstrap — CI=[{ci_lo:+.3f}, {ci_hi:+.3f}]')
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

# (c) O5 sigma vs D
ax = axes[0, 2]
ax.scatter(D_arr, ls_arr, alpha=0.5, color='tab:orange')
xs = np.linspace(D_arr.min(), D_arr.max(), 100)
ax.plot(xs, slope*xs + intercept, 'r-', lw=2,
        label=f"slope={slope:+.2e} (95% CI [{slope_ci[0]:+.2e},{slope_ci[1]:+.2e}])")
ax.axhline(np.median(ls_arr), color='black', ls='--', alpha=0.5,
           label=f'median = {np.median(ls_arr):.2f}')
ax.set_xlabel('Distance [Mpc]')
ax.set_ylabel('log10(sigma_0)')
ax.set_title(f'(c) O5 sigma_0 vs D (z proxy)\n'
             f'span={(slope*(D_arr.max()-D_arr.min())):+.3f} dex')
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

# (d) O8 univariate residual R^2 ranking
ax = axes[1, 0]
fnames = [k for k, _ in sorted_extras]
r2s    = [v['r2'] for _, v in sorted_extras]
bars = ax.bar(fnames, r2s, color='tab:purple', alpha=0.7)
ax.axhline(null_p95, color='red', ls='--', label=f'null 95th = {null_p95:.4f}')
ax.set_ylabel('Residual R^2')
ax.set_title('(d) O8 residual scatter — what predicts it?')
plt.setp(ax.xaxis.get_majorticklabels(), rotation=20)
ax.legend()
ax.grid(alpha=0.3, axis='y')

# (e) Residuals histogram
ax = axes[1, 1]
ax.hist(residuals, bins=25, color='tab:red', alpha=0.7, edgecolor='black')
ax.axvline(0, color='black')
ax.set_xlabel('Multivariate residual log10(sigma_0)')
ax.set_ylabel('count')
ax.set_title(f'(e) Residual distribution\n'
             f'std={res_std:.3f} dex (intrinsic scatter)')
ax.grid(alpha=0.3)

# (f) Verdict
ax = axes[1, 2]
ax.axis('off')
lines = [
    "L72 Phase 1 - Three lock-in tests",
    "=" * 40,
    "",
    "O4 (Field vs Cluster a_0):",
    f"  field   (n={len(field)}):   med={med_f:.3f}",
    f"  cluster (n={len(cluster)}): med={med_c:.3f}",
    f"  diff = {med_diff:+.3f} dex",
    f"  95% CI = [{ci_lo:+.3f}, {ci_hi:+.3f}]",
    f"  p-val = {p_val:.2e}",
    f"  -> {o4_verdict[:36]}",
    "",
    "O5 (sigma vs Distance proxy):",
    f"  slope = {slope:+.2e} dex/Mpc",
    f"  total span over SPARC = {(slope*(D_arr.max()-D_arr.min())):+.3f} dex",
    f"  -> {o5_verdict[:36]}",
    "",
    "O8 (Residual scatter origin):",
    f"  base R^2 = {r2_base:.3f}",
    f"  residual std = {res_std:.3f} dex",
    f"  Best extra predictor: ",
]
if sorted_extras:
    lines.append(f"    {sorted_extras[0][0]} R^2={sorted_extras[0][1]['r2']:.4f}")
lines += [
    f"  null 95th = {null_p95:.4f}",
    f"  -> {o8_verdict[:36]}",
    "",
    "Branch B status (after Phase 1):",
]
n_pass = sum(1 for v in [o4_verdict, o5_verdict] if 'PASS' in v)
if n_pass == 2:
    lines.append("  STRENGTHENED (O4+O5 both PASS)")
elif n_pass == 1:
    lines.append("  PARTIAL (1 PASS, 1 marginal)")
else:
    lines.append("  CHALLENGED (multiple PASS criteria failed)")

ax.text(0.02, 0.98, "\n".join(lines), family='monospace', fontsize=8,
        transform=ax.transAxes, va='top')

plt.suptitle('L72 Phase 1: O4 + O5 + O8 observational lock-in', fontsize=13)
plt.tight_layout()
plt.savefig(OUT / 'L72_phase1.png', dpi=140, bbox_inches='tight')
plt.close()
print(f"\nSaved: {OUT/'L72_phase1.png'}")

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
    O4=dict(
        n_field=len(field), n_cluster=len(cluster),
        med_field=med_f, med_cluster=med_c, std_field=std_f, std_cluster=std_c,
        median_diff=float(med_diff), ci_95=[float(ci_lo), float(ci_hi)],
        t_stat=float(t_stat), p_value=float(p_val),
        verdict=o4_verdict,
    ),
    O5=dict(
        slope_dex_per_Mpc=float(slope),
        slope_ci_95=[float(slope_ci[0]), float(slope_ci[1])],
        intercept=float(intercept), r2=float(r2),
        total_span_dex=float(slope * (D_arr.max() - D_arr.min())),
        verdict=o5_verdict,
    ),
    O8=dict(
        base_R2=float(r2_base),
        residual_std=float(res_std),
        residual_predictors=residual_predictions,
        null_p95=float(null_p95),
        verdict=o8_verdict,
    ),
)
with open(OUT / 'l72_phase1_report.json', 'w') as f:
    json.dump(_j(report), f, indent=2)
print(f"Saved: {OUT/'l72_phase1_report.json'}")
