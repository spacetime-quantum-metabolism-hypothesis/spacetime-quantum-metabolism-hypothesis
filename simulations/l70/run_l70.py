#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L70 — M4 Resonance Precision Test + Cross-Validation
=====================================================

L69 result: Branch A (M4 peak-Vflat) and Branch B (3-regime) tied (ΔAICc=0.33).
This step BREAKS the degeneracy via two tests:

OPTION (1): Dwarf precision test
  - Select SPARC galaxies with V_flat in [20, 40] km/s (where M4 peak lies).
  - M4 predicts: log sigma_0 ≈ peak amplitude in this range.
  - Test: do dwarfs in this band actually show higher sigma_0 than:
       galaxies far from peak (V_flat > 100)?
  - Compare median (sub-band) vs (out-of-band).

OPTION (4): Cross-validation
  - Random 50/50 split of SPARC sample (n=129 with Vflat).
  - Fit M4 (peak-Vflat) on TRAIN; predict TEST.
  - Compare to M7 3-regime (just constant) and M2 linear baseline.
  - 100 random splits, report distributions of test chi^2/dof.

If M4 wins on cross-validation AND dwarf precision, Branch A confirmed.
If M4 ties with M7, Branch B accepted as more conservative.
If M4 loses, axiom Mapping fails.

================================================================
4-Team review (P / N / O / H), recorded BEFORE running:
================================================================
P (theory):
  - Cross-validation is THE critical test. Overfitting on full data
    can hide a model that's not generalisable. Holding out half the
    data and predicting it is decisive.
  - Predict: M4 generalises if peak structure is real; M4 fails if
    L69 ΔAICc=0.33 advantage was overfitting noise.
N (numeric):
  - 100 random splits with seeded RNG. Bootstrap CI.
  - Use chi^2/dof on test set as performance metric.
  - Track best-fit V_peak STABILITY across splits — drift = bad.
O (observation):
  - Dwarf SPARC galaxies (V_flat 20-40) are typically Q=2 or Q=3
    (lower quality rotation curves due to short discs).
  - Watch for selection effects: dwarfs with measurable V_flat may be
    biased toward strong rotators.
H (self-consistency hunter, STRONG):
  > Pre-prediction:
    1. Cross-validation: M4 test chi^2/dof very close to M7's. The 0.33
       ΔAICc was on edge; CV likely shows tie.
    2. Dwarf precision: in-band median sigma might be 0.2-0.5 dex
       higher than out-of-band; if peak is real, this is the signature.
    3. Best outcome: clear in-band excess + stable V_peak across splits
       => Branch A confirmed. Otherwise Branch B.
  > "If V_peak drifts across splits by >0.3 dex or in-band excess <0.1
     dex => M4 is a coincidence on the 3 anchor scales, not a real
     resonance. ABANDON Branch A."
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
OUT = ROOT / "results/L70"
OUT.mkdir(parents=True, exist_ok=True)

# Load Step 1 data
with open(ROOT / "results/L69/l69_step1_report.json") as f:
    step1 = json.load(f)
SPARC_ROWS = [r for r in step1['rows'] if r.get('Vflat') and r['Vflat'] > 0]
print(f"SPARC galaxies with Vflat: {len(SPARC_ROWS)}")

log_sigma  = np.array([r['log_sigma'] for r in SPARC_ROWS])
log_Vflat  = np.array([np.log10(r['Vflat']) for r in SPARC_ROWS])
SPARC_GAL_ERR = step1['log_sigma_std']  # ~0.66 dex per-galaxy

# Cosmic and cluster anchors (treated as ALWAYS in fit)
ANCHOR_LOG_SIG = np.array([8.37, 7.75])
ANCHOR_ERR    = np.array([0.06, 0.06])
ANCHOR_LOG_V  = np.array([np.log10(1.0), np.log10(1000.0)])

# ============================================================
# Models (from L69 step 4)
# ============================================================
def m4_peak_V(p, x_V):
    s, V0, w = p
    if w < 0.05 or w > 5: return np.full_like(x_V, 1e10)
    return s - 0.5 * ((x_V - V0) / w)**2

def m2_lin_V(p, x_V):
    return p[0] + p[1] * x_V

def m1_const(p, x_V):
    return np.full_like(x_V, p[0])

def m7_3regime_simple(p, x_V):
    # for SPARC (which is at galactic) it's just s_galactic
    s_cosm, s_clust, s_gal = p
    out = np.empty_like(x_V)
    out[:] = s_gal
    out[x_V <= 0.5] = s_cosm     # log V <= 0.5 => V <= ~3 (cosmic-like)
    out[x_V >= 2.7] = s_clust    # log V >= 2.7 => V >= 500 (cluster-like)
    return out

# ============================================================
# OPTION (1) Dwarf precision test
# ============================================================
print("\n" + "=" * 60)
print("OPTION (1): Dwarf precision test")
print("=" * 60)

# Define peak band from L69 best-fit M4: V_peak=24, width=5x in linear (0.77 dex)
# Take a band of +/- 0.3 dex around the peak
V_peak_logV = 1.38            # log10(24)
in_band_low = 10**(V_peak_logV - 0.3)   # ~12 km/s
in_band_high = 10**(V_peak_logV + 0.3)  # ~48 km/s
out_band_low = 10**(V_peak_logV + 0.7)  # > 120 km/s

vflat_arr = np.array([r['Vflat'] for r in SPARC_ROWS])
in_band  = (vflat_arr >= in_band_low) & (vflat_arr <= in_band_high)
out_band = (vflat_arr >= out_band_low)

n_in  = int(in_band.sum())
n_out = int(out_band.sum())
print(f"  Peak band  (V_flat in [{in_band_low:.1f}, {in_band_high:.1f}] km/s): n={n_in}")
print(f"  Out-of-peak (V_flat >= {out_band_low:.1f} km/s):                    n={n_out}")

if n_in < 5 or n_out < 5:
    print("  WARNING: insufficient sample in one band")

med_in  = float(np.median(log_sigma[in_band])) if n_in >= 5 else np.nan
med_out = float(np.median(log_sigma[out_band])) if n_out >= 5 else np.nan
std_in  = float(np.std(log_sigma[in_band])) if n_in >= 5 else np.nan
std_out = float(np.std(log_sigma[out_band])) if n_out >= 5 else np.nan
diff = med_in - med_out

# bootstrap on the difference (1000 reps)
rng = np.random.default_rng(seed=42)
n_boot = 1000
diffs_boot = np.zeros(n_boot)
for i in range(n_boot):
    idx_in  = rng.choice(np.where(in_band)[0],  size=n_in,  replace=True)
    idx_out = rng.choice(np.where(out_band)[0], size=n_out, replace=True)
    diffs_boot[i] = np.median(log_sigma[idx_in]) - np.median(log_sigma[idx_out])
ci_lo, ci_hi = np.percentile(diffs_boot, [2.5, 97.5])

print(f"  In-band  median log_sigma = {med_in:.3f} (std {std_in:.3f})")
print(f"  Out-band median log_sigma = {med_out:.3f} (std {std_out:.3f})")
print(f"  Difference (in - out) = {diff:.3f} dex, 95% CI: [{ci_lo:.3f}, {ci_hi:.3f}]")

# M4 prediction at the band centers
def m4_pred(p, V):
    return m4_peak_V(p, np.log10(np.atleast_1d(V)))

# Use L69 step 4 best-fit M4 params
m4_params_l69 = [9.995, 1.383, 0.767]
pred_in  = m4_pred(m4_params_l69, np.array([24.0]))[0]
pred_out_avg = float(np.median(m4_pred(m4_params_l69, vflat_arr[out_band])))
pred_diff = pred_in - pred_out_avg
print(f"\n  M4 (L69) prediction at V=24: log_sigma = {pred_in:.3f}")
print(f"  M4 (L69) prediction median in out-band: log_sigma = {pred_out_avg:.3f}")
print(f"  M4 predicted difference = {pred_diff:.3f} dex")

# Compare observed vs predicted
agreement_dex = abs(diff - pred_diff)
if agreement_dex < 0.15 and (ci_hi > 0):
    p1_verdict = "PASS — observed in-band excess matches M4 prediction"
elif (ci_lo > 0) and agreement_dex < 0.5:
    p1_verdict = "WEAK PASS — sign correct but magnitude off"
elif ci_hi < 0:
    p1_verdict = "FAIL — observed slope OPPOSITE to M4 (in-band lower!)"
else:
    p1_verdict = "AMBIGUOUS — CI crosses zero"

print(f"\n  P1 VERDICT: {p1_verdict}")

# ============================================================
# OPTION (4) Cross-validation (50/50 splits)
# ============================================================
print("\n" + "=" * 60)
print("OPTION (4): 100-fold 50/50 cross-validation")
print("=" * 60)

def fit_model_global(model_fn, k, bounds, x_train, y_train, e_train):
    def obj(p):
        pred = model_fn(p, x_train)
        if not np.all(np.isfinite(pred)):
            return 1e10
        return float(np.sum(((y_train - pred) / e_train)**2))
    res = differential_evolution(obj, bounds, seed=42, tol=1e-7,
                                  maxiter=300, polish=True)
    return res.x

# Combined arrays (anchors always in TRAIN to anchor scale)
def cv_one(seed, model_fn, k, bounds):
    rng = np.random.default_rng(seed)
    n = len(SPARC_ROWS)
    perm = rng.permutation(n)
    half = n // 2
    train_idx = perm[:half]
    test_idx  = perm[half:]
    # Train: SPARC half + both anchors
    x_train = np.concatenate([log_Vflat[train_idx], ANCHOR_LOG_V])
    y_train = np.concatenate([log_sigma[train_idx], ANCHOR_LOG_SIG])
    e_train = np.concatenate([np.full(len(train_idx), SPARC_GAL_ERR), ANCHOR_ERR])
    # Test: SPARC other half (anchors not in test)
    x_test = log_Vflat[test_idx]
    y_test = log_sigma[test_idx]
    e_test = np.full(len(test_idx), SPARC_GAL_ERR)
    # Fit
    p_best = fit_model_global(model_fn, k, bounds, x_train, y_train, e_train)
    # Test chi^2
    pred = model_fn(p_best, x_test)
    chi2_test = float(np.sum(((y_test - pred) / e_test)**2))
    return p_best, chi2_test, len(test_idx)

n_splits = 100
m4_params_history = []
m4_chi2 = []
m1_chi2 = []
m2_chi2 = []
m7_chi2 = []

print(f"  Running {n_splits} 50/50 splits ...")
for seed in range(n_splits):
    p4, c4, n_test = cv_one(seed, m4_peak_V, 3,
                             [(7,12), (-1,5), (0.1,5)])
    m4_params_history.append(p4)
    m4_chi2.append(c4)
    p1, c1, _ = cv_one(seed, m1_const, 1, [(7,11)])
    m1_chi2.append(c1)
    p2, c2, _ = cv_one(seed, m2_lin_V, 2, [(0,20), (-3,3)])
    m2_chi2.append(c2)
    p7, c7, _ = cv_one(seed, m7_3regime_simple, 3, [(7,11), (6,10), (8,11)])
    m7_chi2.append(c7)

m4_chi2 = np.array(m4_chi2)
m1_chi2 = np.array(m1_chi2)
m2_chi2 = np.array(m2_chi2)
m7_chi2 = np.array(m7_chi2)
m4_params_history = np.array(m4_params_history)

# n_test = len(test) approx 64
nt = n_test
# Lower test chi^2 = better
def summary_cv(arr, name):
    return dict(
        name=name,
        median=float(np.median(arr)),
        mean=float(np.mean(arr)),
        p16=float(np.percentile(arr, 16)),
        p84=float(np.percentile(arr, 84)),
        median_per_dof=float(np.median(arr) / nt),
    )

cv_stats = dict(
    M1=summary_cv(m1_chi2, 'M1 const'),
    M2=summary_cv(m2_chi2, 'M2 linear-V'),
    M4=summary_cv(m4_chi2, 'M4 peak-V'),
    M7=summary_cv(m7_chi2, 'M7 3-regime'),
)

print(f"\n  Test chi^2 (median, on n_test={nt} galaxies):")
for k, s in cv_stats.items():
    print(f"    {s['name']:14s}  median={s['median']:7.2f}  "
          f"per-dof={s['median_per_dof']:.3f}  "
          f"16-84%=[{s['p16']:.1f}, {s['p84']:.1f}]")

# Param stability for M4
v_peak_history = m4_params_history[:, 1]
v_peak_med = float(np.median(v_peak_history))
v_peak_std = float(np.std(v_peak_history))
print(f"\n  M4 V_peak (log_Vflat) stability across splits:")
print(f"    median = {v_peak_med:.3f}, std = {v_peak_std:.3f}")
if v_peak_std < 0.20:
    p4_stab = "STABLE"
elif v_peak_std < 0.50:
    p4_stab = "MARGINAL"
else:
    p4_stab = "UNSTABLE"
print(f"    Stability: {p4_stab}")

# Decisive comparison: does M4 beat M7 on test set?
m4_vs_m7 = m4_chi2 - m7_chi2
n_m4_wins = int((m4_vs_m7 < 0).sum())
print(f"\n  M4 wins over M7 in {n_m4_wins}/{n_splits} splits (paired)")
print(f"  Median (M4_chi2 - M7_chi2) = {float(np.median(m4_vs_m7)):+.3f}")

if v_peak_std < 0.20 and (med_in - med_out > 0.1) and ci_lo > 0:
    final_verdict = "BRANCH A CONFIRMED — M4 resonance survives precision tests"
elif v_peak_std > 0.5 or ci_hi < 0:
    final_verdict = "BRANCH A REJECTED — fall back to Branch B (3-regime phenomenology)"
else:
    final_verdict = "TIE — Branch A and B statistically indistinguishable; choose B for parsimony"

print(f"\n  FINAL VERDICT: {final_verdict}")

# ============================================================
# Visualization
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(20, 11))

# (a) Dwarf precision test scatter
ax = axes[0, 0]
ax.scatter(log_Vflat, log_sigma, alpha=0.4, color='tab:gray',
           label=f'all SPARC (n={len(SPARC_ROWS)})')
ax.scatter(log_Vflat[in_band],  log_sigma[in_band],  c='tab:red',  s=50, label=f'in-band (n={n_in})')
ax.scatter(log_Vflat[out_band], log_sigma[out_band], c='tab:blue', s=50, label=f'out-band (n={n_out})')
xs = np.linspace(log_Vflat.min(), log_Vflat.max(), 100)
ax.plot(xs, m4_peak_V(m4_params_l69, xs), 'r-', lw=2, label='L69 M4 fit')
ax.axvline(V_peak_logV, color='red', ls='--', alpha=0.5, label=f'peak at {10**V_peak_logV:.0f} km/s')
ax.set_xlabel('log10(V_flat) [km/s]')
ax.set_ylabel('log10(sigma_0)')
ax.set_title(f'(a) Dwarf precision: in-band vs out-band\n'
             f'diff = {diff:+.3f} dex (95% CI [{ci_lo:+.2f}, {ci_hi:+.2f}])')
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

# (b) Bootstrap distribution of in-out difference
ax = axes[0, 1]
ax.hist(diffs_boot, bins=40, alpha=0.7, color='tab:purple', edgecolor='black')
ax.axvline(0, color='black', lw=1)
ax.axvline(diff, color='red', ls='--', label=f'observed = {diff:+.3f}')
ax.axvline(pred_diff, color='blue', ls='-.', label=f'M4 predicted = {pred_diff:+.3f}')
ax.axvline(ci_lo, color='gray', ls=':', label='95% CI')
ax.axvline(ci_hi, color='gray', ls=':')
ax.set_xlabel('Difference in median log_sigma (in - out)')
ax.set_ylabel('Bootstrap count')
ax.set_title('(b) Bootstrap distribution of in-band excess')
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

# (c) CV test chi^2 distributions
ax = axes[0, 2]
data_to_plot = [m1_chi2, m2_chi2, m4_chi2, m7_chi2]
labels_cv = ['M1 const', 'M2 linear-V', 'M4 peak-V', 'M7 3-regime']
bp = ax.boxplot(data_to_plot, labels=labels_cv, showfliers=False, patch_artist=True)
for patch, color in zip(bp['boxes'], ['tab:gray', 'tab:orange', 'tab:red', 'tab:green']):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax.set_ylabel('test chi^2 (lower = better generalisation)')
ax.set_title(f'(c) Cross-validation test chi^2 (100 splits, n_test~{nt})')
plt.setp(ax.xaxis.get_majorticklabels(), rotation=20)
ax.grid(alpha=0.3, axis='y')

# (d) M4 V_peak stability across splits
ax = axes[1, 0]
ax.hist(v_peak_history, bins=30, alpha=0.7, color='tab:red', edgecolor='black')
ax.axvline(v_peak_med, color='black', ls='-', label=f'median = {v_peak_med:.3f}')
ax.axvline(1.383, color='blue', ls='--', label='L69 full-fit V_peak = 1.383')
ax.set_xlabel('Best-fit log_Vpeak (per CV split)')
ax.set_ylabel('count')
ax.set_title(f'(d) M4 V_peak stability across 100 splits\n'
             f'std = {v_peak_std:.3f} ({p4_stab})')
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

# (e) Pairwise M4 vs M7
ax = axes[1, 1]
ax.scatter(m7_chi2, m4_chi2, alpha=0.6, color='tab:purple')
mn = min(m7_chi2.min(), m4_chi2.min())
mx = max(m7_chi2.max(), m4_chi2.max())
ax.plot([mn, mx], [mn, mx], 'k--', label='M4 = M7')
ax.set_xlabel('M7 test chi^2')
ax.set_ylabel('M4 test chi^2')
ax.set_title(f'(e) Pairwise: M4 wins {n_m4_wins}/{n_splits}\n'
             f'median(M4-M7) = {float(np.median(m4_vs_m7)):+.2f}')
ax.legend()
ax.grid(alpha=0.3)

# (f) Verdict
ax = axes[1, 2]
ax.axis('off')
lines = [
    "L70 — M4 precision test + CV",
    "=" * 38,
    "",
    "OPTION (1) DWARF BAND TEST:",
    f"  in-band  V_flat [{in_band_low:.1f},{in_band_high:.1f}]: n={n_in}",
    f"  out-band V_flat >= {out_band_low:.0f}:                  n={n_out}",
    f"  observed diff = {diff:+.3f} dex",
    f"  M4 predicted  = {pred_diff:+.3f} dex",
    f"  95% CI = [{ci_lo:+.3f}, {ci_hi:+.3f}]",
    f"  P1 verdict: {p1_verdict}",
    "",
    "OPTION (4) 100-FOLD CROSS-VALIDATION:",
    f"  M4 V_peak stability: std={v_peak_std:.3f} ({p4_stab})",
    f"  Test chi^2 medians (per dof):",
]
for k, s in cv_stats.items():
    lines.append(f"    {s['name']:14s} {s['median_per_dof']:.3f}")

lines += [
    f"  M4 beats M7 in {n_m4_wins}/{n_splits} splits",
    f"  median(M4-M7) chi^2 = {float(np.median(m4_vs_m7)):+.2f}",
    "",
    "FINAL VERDICT:",
]
for word_chunk in final_verdict.split('. '):
    line = ""
    for w in word_chunk.split():
        if len(line) + len(w) + 1 > 38:
            lines.append(line)
            line = w
        else:
            line = line + " " + w if line else w
    if line:
        lines.append(line)

ax.text(0.02, 0.98, "\n".join(lines), family='monospace', fontsize=8,
        transform=ax.transAxes, va='top')

plt.suptitle('L70: M4 resonance precision + cross-validation', fontsize=13)
plt.tight_layout()
plt.savefig(OUT / 'L70_main.png', dpi=140, bbox_inches='tight')
plt.close()
print(f"\nSaved: {OUT/'L70_main.png'}")

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
    n_sparc=len(SPARC_ROWS),
    in_band=dict(low=in_band_low, high=in_band_high, n=n_in,
                 median=med_in, std=std_in),
    out_band=dict(low=out_band_low, n=n_out, median=med_out, std=std_out),
    diff=diff, ci_95=[ci_lo, ci_hi],
    m4_predicted_diff=pred_diff,
    p1_verdict=p1_verdict,
    cv_n_splits=n_splits,
    cv_stats=cv_stats,
    cv_n_test_per_split=int(nt),
    m4_vpeak_median=v_peak_med,
    m4_vpeak_std=v_peak_std,
    m4_stability=p4_stab,
    m4_wins_over_m7=n_m4_wins,
    median_chi2_M4_minus_M7=float(np.median(m4_vs_m7)),
    final_verdict=final_verdict,
)
with open(OUT / 'l70_report.json', 'w') as f:
    json.dump(_j(report), f, indent=2)
print(f"Saved: {OUT/'l70_report.json'}")

print("\n" + "=" * 60)
print(f"L70 DONE — {final_verdict}")
print("=" * 60)
