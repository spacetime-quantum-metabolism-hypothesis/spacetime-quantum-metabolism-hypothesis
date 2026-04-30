"""
L67: Quantitative Gating Ratio Test
====================================

Purpose: For each surviving axiom (A/B/D), test whether the SAME single
         threshold can produce activation ratios MATCHING the σ_0 evidence
         spectrum from L48 (T17/T20/T22).

L66 only checked structural separation between cosmic OFF and galactic ON
(6 decades — trivially separable). L67 imposes the QUANTITATIVE constraint
from past simulations:

    σ_0 (T17 cosmic)         ≈ 2.34e8  → f_cosmic
    σ_0 (T17 self-consist.)  ≈ 1.17e8
    σ_0 (T20 cluster σ_8)    ≈ 5.6e7   → f_cluster_core
    σ_0 (T22 galactic a_0)   ≈ 3.31e9  → f_galaxy_disk

Hypothesis: σ_eff(env) = f(env) × σ_0_true
Anchor σ_0_true at T22 (where f_galactic ≈ 1):
    σ_0_true = 3.31e9
    f(env) = σ_eff(env) / 3.31e9

Targets:
    f_galaxy_disk    ≈ 1.000
    f_cosmic_mean    ≈ 0.071  (= 2.34e8 / 3.31e9)
    f_self_consist   ≈ 0.035  (= 1.17e8 / 3.31e9)
    f_cluster_core   ≈ 0.017  (= 5.6e7  / 3.31e9)

The hardest test: f_cluster ≪ f_galaxy. Cluster vs galaxy separation in:
    density (A):  ratio 630 (2.8 dex) — feasible
    gradient (B): ratio 30  (1.5 dex) — marginal
    virial  (D):  both virialized (~1) — structurally infeasible

This script runs the actual scan and produces the discriminating plot.

================================================================
4-Team Critique (P/N/O/H), recorded BEFORE running:
================================================================
P (theory):
  - The σ_eff = f × σ_0_true ansatz is the simplest gating model. Real
    SQT may have multiplicative corrections (n × σ × ε terms each gated
    differently). L67 tests the simplest version; failure here means
    even the simplest gating fails.
  - Anchoring at T22 is a CHOICE. Could anchor at T17 instead and
    interpret f as ABSORPTION-rate gate. Equivalent up to overall scale.
N (numeric):
  - Sigmoid width 0.3 dex was L66 default. Test 0.15/0.45 sensitivity.
  - Threshold scan 300 points, log-spaced.
  - Target tolerance: f_predicted within factor 2 of f_target.
O (observation):
  - Environments use representative central values. Real galaxies span
    range; this test is for the AVERAGE case. SPARC fit is L68.
  - σ_0(T20) = 5.6e7 was the L48 best-fit. L52 found σ_IR = 5.36e7
    consistent. Use 5.6e7.
H (self-consistency hunter, STRONG mode):
  > "Anchor at T22 is biased toward axioms that activate fully in
     galaxies. If a different axiom's f_galaxy < 1, anchoring breaks.
     Mitigation: report f_galaxy explicitly per axiom; if not ~1, flag."
  > "Cluster test will likely kill D (virial). Predicted before run."
  > "Even if A passes, the gating must be sharp enough to keep
     f_cosmic small. f_cosmic = 0.071 is non-trivial — too low and
     ΛCDM contribution from SQT vanishes (loses cosmic Λ explanation)."
================================================================
"""

import os
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
from pathlib import Path

OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L67")
OUT.mkdir(parents=True, exist_ok=True)

# ============================================================
# Reference Environments (corrected virials)
# ============================================================
# Note: cluster_core virial ≈ 0.5 (virialized), galaxy_disk virial ≈ 0.5
# The structural problem: D axiom cannot distinguish them.
ENV = {
    'cosmic_mean':    dict(rho=2.7e-27,  grad_rel=1.0/4.4e26, virial=1e6,  v_pec=1.0),
    'void_center':    dict(rho=2.7e-28,  grad_rel=1.0/3.0e23, virial=1e3,  v_pec=300.0),
    'filament':       dict(rho=1.4e-26,  grad_rel=1.0/3.0e22, virial=10.0, v_pec=3.0e5),
    'cluster_outer':  dict(rho=5.4e-25,  grad_rel=1.0/3.0e22, virial=1.0,  v_pec=5.0e5),
    'cluster_core':   dict(rho=2.7e-24,  grad_rel=1.0/3.0e21, virial=0.5,  v_pec=1.0e6),
    'galaxy_outskirt':dict(rho=2.7e-22,  grad_rel=1.0/3.0e20, virial=0.5,  v_pec=1.5e5),
    'galaxy_disk':    dict(rho=1.7e-21,  grad_rel=1.0/1.0e20, virial=0.5,  v_pec=2.0e5),
    'solar_neighbor': dict(rho=1.7e-21,  grad_rel=1.0/3.0e18, virial=0.5,  v_pec=2.2e5),
    'planet':         dict(rho=5.5e3,    grad_rel=1.0/6.4e6,  virial=0.3,  v_pec=3.0e4),
}

# ============================================================
# Quantitative targets from σ_0 evidence
# ============================================================
SIGMA0_TRUE_ANCHOR = 3.31e9   # T22 galactic
TARGETS = {
    'galaxy_disk':    3.31e9 / SIGMA0_TRUE_ANCHOR,    # 1.000
    'cosmic_mean':    2.34e8 / SIGMA0_TRUE_ANCHOR,    # 0.071
    'cluster_core':   5.60e7 / SIGMA0_TRUE_ANCHOR,    # 0.017
}
# Self-consistency target (T17 자기일관 σ ≈ 1.17e8)
F_SELF = 1.17e8 / SIGMA0_TRUE_ANCHOR  # 0.035 — rough cosmic average

print("Quantitative targets (σ_eff/σ_0_true):")
for k, v in TARGETS.items():
    print(f"  f({k:14s}) target = {v:.4f}")

# ============================================================
# Activation
# ============================================================
def sigmoid_log(x, x_thresh, width=0.3, ascending=True):
    x = np.maximum(np.asarray(x, dtype=float), 1e-300)
    z = (np.log10(x) - np.log10(x_thresh)) / width
    if not ascending:
        z = -z
    return 1.0 / (1.0 + np.exp(-z))

def f_A(env, thr, w=0.3): return sigmoid_log(env['rho'],      thr, w, ascending=True)
def f_B(env, thr, w=0.3): return sigmoid_log(env['grad_rel'], thr, w, ascending=True)
def f_D(env, thr, w=0.3): return sigmoid_log(env['virial'],   thr, w, ascending=False)

AXIOMS = [
    ('A_threshold', f_A, np.logspace(-28, -19, 400), 'rho [kg/m^3]'),
    ('B_gradient',  f_B, np.logspace(-26, -15, 400), '|grad rho|/rho [1/m]'),
    ('D_bound',     f_D, np.logspace(-2, 4, 400),    'virial parameter'),
]

# ============================================================
# Score: log-distance from targets
# ============================================================
def score(activation_fn, threshold, width=0.3):
    """Return predicted f(env) for all envs and chi2-like score vs targets."""
    f_pred = {e: float(activation_fn(ENV[e], threshold, width))
              for e in ENV}
    # Loss: log-space distance from targets, with floor to avoid log(0)
    log_loss = 0.0
    detail = {}
    for env_name, f_target in TARGETS.items():
        f_p = max(f_pred[env_name], 1e-8)
        f_t = max(f_target, 1e-8)
        d = (np.log10(f_p) - np.log10(f_t))**2
        log_loss += d
        detail[env_name] = dict(target=f_t, predicted=f_p,
                                log_residual=np.log10(f_p) - np.log10(f_t))
    return dict(f_pred=f_pred, log_loss=log_loss, detail=detail)

# ============================================================
# Run scan per axiom
# ============================================================
def run_axiom(name, fn, grid, label, width=0.3):
    scan = []
    for thr in grid:
        s = score(fn, thr, width)
        scan.append(dict(threshold=float(thr), **s))
    best = min(scan, key=lambda r: r['log_loss'])
    return dict(name=name, label=label, width=width, scan=scan, best=best,
                grid=grid)

print("\n" + "=" * 60)
print("L67: Quantitative Gating Ratio Test")
print("=" * 60)

results = {}
for name, fn, grid, label in AXIOMS:
    r = run_axiom(name, fn, grid, label, width=0.3)
    results[name] = r
    bp = r['best']
    print(f"\n{name}:")
    print(f"  best threshold = {bp['threshold']:.3e}")
    print(f"  log_loss       = {bp['log_loss']:.3f}  (0=perfect)")
    for env, d in bp['detail'].items():
        ok = '✓' if abs(d['log_residual']) < 0.5 else 'X'
        print(f"  {ok} f({env:14s}) target={d['target']:.4f} "
              f"predicted={d['predicted']:.4f} "
              f"log_resid={d['log_residual']:+.2f}")

# Width sensitivity
print("\nWidth sensitivity (best log_loss):")
for name, fn, grid, label in AXIOMS:
    losses = []
    for w in [0.15, 0.30, 0.45, 0.60]:
        r_ = run_axiom(name, fn, grid, label, width=w)
        losses.append((w, r_['best']['log_loss']))
    print(f"  {name}: " + ", ".join(f"w={w}: {l:.2f}" for w, l in losses))

# ============================================================
# Visualization
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(20, 11))

# Top row: log_loss vs threshold for each axiom
for i, (name, fn, grid, label) in enumerate(AXIOMS):
    ax = axes[0, i]
    r = results[name]
    losses = [s['log_loss'] for s in r['scan']]
    ax.semilogx(grid, losses, 'b-', lw=2)
    ax.set_xlabel(label)
    ax.set_ylabel('log_loss (lower=better)')
    ax.axhline(0.5, color='orange', ls='--', alpha=0.5, label='loose PASS')
    ax.axhline(0.1, color='green', ls='--', alpha=0.5, label='tight PASS')
    ax.axvline(r['best']['threshold'], color='red', ls=':', alpha=0.7,
               label=f"best={r['best']['threshold']:.2e}")
    ax.set_title(f"({chr(97+i)}) {name}: best loss={r['best']['log_loss']:.3f}")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    ax.set_ylim(0, max(2.0, min(losses) + 1.5))

# Bottom-left: predicted vs target f at best threshold for all 3 axioms
ax = axes[1, 0]
target_envs = list(TARGETS.keys())
x = np.arange(len(target_envs))
width_b = 0.22
colors = ['tab:blue', 'tab:green', 'tab:red']
for j, (name, _, _, _) in enumerate(AXIOMS):
    bp = results[name]['best']
    f_vals = [bp['f_pred'][e] for e in target_envs]
    ax.bar(x + (j - 1) * width_b, f_vals, width_b, label=name, color=colors[j], alpha=0.8)
# Plot targets as horizontal bars
for i, e in enumerate(target_envs):
    ax.plot([i - 0.4, i + 0.4], [TARGETS[e], TARGETS[e]], 'k-', lw=2.5,
            label='target' if i == 0 else None)
ax.set_yscale('log')
ax.set_ylim(1e-4, 2)
ax.set_xticks(x)
ax.set_xticklabels(target_envs, rotation=20, ha='right')
ax.set_ylabel('activation f (log scale)')
ax.legend(fontsize=8)
ax.set_title('(d) Predicted f vs target (best threshold each)')
ax.grid(alpha=0.3, which='both')

# Bottom-middle: log-residual heatmap-like bar
ax = axes[1, 1]
for j, (name, _, _, _) in enumerate(AXIOMS):
    bp = results[name]['best']
    resids = [bp['detail'][e]['log_residual'] for e in target_envs]
    ax.bar(x + (j - 1) * width_b, resids, width_b, label=name, color=colors[j], alpha=0.8)
ax.axhline(0, color='black', lw=1)
ax.axhline(0.5, color='orange', ls='--', alpha=0.5)
ax.axhline(-0.5, color='orange', ls='--', alpha=0.5)
ax.set_xticks(x)
ax.set_xticklabels(target_envs, rotation=20, ha='right')
ax.set_ylabel('log10(predicted/target)')
ax.legend(fontsize=8)
ax.set_title('(e) Log-residual per env (closer to 0 = better)')
ax.grid(alpha=0.3)

# Bottom-right: summary verdict
ax = axes[1, 2]
ax.axis('off')

verdict_lines = [
    "L67: Quantitative Gating Ratio Test",
    "=" * 42,
    f"Anchor sigma_0 = {SIGMA0_TRUE_ANCHOR:.2e} (T22 galactic)",
    "",
    "Targets (sigma_eff / sigma_0_true):",
]
for k, v in TARGETS.items():
    verdict_lines.append(f"  f({k:14s}) = {v:.4f}")

verdict_lines += [
    "",
    "Per-axiom best fit:",
]
ranks = []
for name in ['A_threshold', 'B_gradient', 'D_bound']:
    bp = results[name]['best']
    loss = bp['log_loss']
    if loss < 0.1:
        verdict = "PASS-tight"
    elif loss < 0.5:
        verdict = "PASS-loose"
    elif loss < 1.5:
        verdict = "MARGINAL"
    else:
        verdict = "FAIL"
    ranks.append((name, loss, verdict, bp['threshold']))
    verdict_lines.append(
        f"  {name:14s} loss={loss:.3f}  {verdict}"
    )
    verdict_lines.append(
        f"      thr={bp['threshold']:.2e}"
    )
    # Worst residual
    worst = max(bp['detail'].items(),
                key=lambda kv: abs(kv[1]['log_residual']))
    verdict_lines.append(
        f"      worst: {worst[0]} "
        f"resid={worst[1]['log_residual']:+.2f}"
    )

verdict_lines += [
    "",
    "Ranking (lower loss = better):",
]
ranks.sort(key=lambda r: r[1])
for i, (name, loss, v, thr) in enumerate(ranks):
    verdict_lines.append(f"  {i+1}. {name:14s} {v}")

verdict_lines += [
    "",
    "Pre-run prediction (H, strong critic):",
    "  D_bound: virial cluster=galaxy=0.5,",
    "  cannot distinguish -> FAIL",
]

ax.text(0.02, 0.98, "\n".join(verdict_lines),
        family='monospace', fontsize=9,
        transform=ax.transAxes, va='top')

plt.suptitle('L67: Quantitative Gating Test (cluster vs galaxy is the discriminator)',
             fontsize=13)
plt.tight_layout()
plt.savefig(OUT / 'L67_main.png', dpi=140, bbox_inches='tight')
plt.close()
print(f"\nSaved: {OUT / 'L67_main.png'}")

# ============================================================
# Save report
# ============================================================
def _json(obj):
    if isinstance(obj, (np.bool_, bool)): return bool(obj)
    if isinstance(obj, (np.integer, int)): return int(obj)
    if isinstance(obj, (np.floating, float)): return float(obj)
    if isinstance(obj, np.ndarray): return obj.tolist()
    if isinstance(obj, dict): return {k: _json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)): return [_json(x) for x in obj]
    return obj

report = dict(
    targets=TARGETS,
    sigma0_anchor=SIGMA0_TRUE_ANCHOR,
    f_self_consistency_target=F_SELF,
    results={name: dict(
        best=results[name]['best'],
        label=results[name]['label'],
    ) for name in results},
    ranking=[(n, loss, v) for n, loss, v, _ in ranks],
)
with open(OUT / 'report.json', 'w') as f:
    json.dump(_json(report), f, indent=2)
print(f"Saved: {OUT / 'report.json'}")

print("\n" + "=" * 60)
print("L67 DONE")
print("=" * 60)
