"""
L66: Structural Scale-Separation Test for 4 Axiom Candidates
============================================================

Goal: For each axiom, test whether a SINGLE free parameter can produce
      f_X(cosmic) ~ 0  AND  f_X(galactic) ~ 1  simultaneously.

Axioms tested:
  A: Threshold (density)
  B: Gradient (|grad rho|/rho)
  D: Bound (virial parameter, T/|U|)
  H: Flow (peculiar velocity)

This is NOT a fit to H_0/sigma_8/a_0. This is a STRUCTURAL test:
  if no single parameter can separate scales, the axiom is dead.
  if separation works, axiom is qualified for L67 quantitative test.

The activation function is a smooth sigmoid (log-space for density/gradient
/virial, log-space for velocity with floor). Sigmoid is the minimal
monotonic transition; alternative forms (Heaviside, tanh, erf) yield
qualitatively identical separation if monotonic.

The 4 reviewer comments at the top represent the 4-person team review:
  P (theory) / N (numeric) / O (observation) / H (self-consistency hunter)
"""

# ============================================================
# 4-Team Review (recorded BEFORE running, applied to design)
# ============================================================
# P (theory):
#   - Sigmoid activation is phenomenological. Real derivation requires
#     microscopic Lagrangian. L66 tests structural viability only.
#   - 'Flow' axiom has covariance concern: rest frame = CMB? Local inertial?
#     Use CMB rest frame for L66; flag as L67 issue.
# N (numeric):
#   - Use log-spaced threshold scan (8+ decades). 200 points per axiom.
#   - Single sigmoid width = 0.3 dex (steep but smooth). Width sensitivity
#     test included.
# O (observation):
#   - Reference environments must include: cosmic_mean, void, cluster_outer,
#     cluster_core, galaxy_disk, solar_neighborhood, planet.
#   - Critical PASS requires: cosmic OFF, galaxy ON, solar ON
#     (else Newton broken locally), cluster intermediate (MOND fails here).
# H (self-consistency hunter):
#   - Hidden DOF check: only the threshold is varied. Width is fixed
#     and reported separately. No magic numbers in core test.
#   - PASS thresholds (0.05, 0.95) are reporting choices, NOT fit DOF.
# ============================================================

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

OUT = Path("/Users/blu/Desktop/spacetime-quantum-metabolism-hypothesis/results/L66")
OUT.mkdir(parents=True, exist_ok=True)

# ============================================================
# Reference Environments (SI, with citations to standard astro)
# ============================================================
# Densities: kg/m^3
# Cosmic critical: rho_c0 = 3 H0^2 / (8 pi G) ~ 8.5e-27
# Cosmic matter mean: Omega_m * rho_c0 ~ 2.7e-27
# Voids: ~0.1 of cosmic mean (Aragon-Calvo+ 2010)
# Cluster outer (200 x cosmic, virial radius)
# Cluster core (~1e3 x cosmic)
# Galaxy disk avg: ISM ~ 1 atom/cm^3 ~ 1.7e-21
# Solar neighborhood: ~ 1 H/cc avg
# Earth: 5500
ENV = {
    'cosmic_mean':       dict(rho=2.7e-27,  grad_rel=1.0/4.4e26, virial=1e6,  v_pec=1.0),
    'void_center':       dict(rho=2.7e-28,  grad_rel=1.0/3.0e23, virial=1e3,  v_pec=300.0),
    'filament':          dict(rho=1.4e-26,  grad_rel=1.0/3.0e22, virial=10.0, v_pec=3.0e5),
    'cluster_outer':     dict(rho=5.4e-25,  grad_rel=1.0/3.0e22, virial=0.8,  v_pec=5.0e5),
    'cluster_core':      dict(rho=2.7e-24,  grad_rel=1.0/3.0e21, virial=0.4,  v_pec=1.0e6),
    'galaxy_outskirt':   dict(rho=2.7e-22,  grad_rel=1.0/3.0e20, virial=0.5,  v_pec=1.5e5),
    'galaxy_disk':       dict(rho=1.7e-21,  grad_rel=1.0/1.0e20, virial=0.4,  v_pec=2.0e5),
    'solar_neighborhood':dict(rho=1.7e-21,  grad_rel=1.0/3.0e18, virial=0.35, v_pec=2.2e5),
    'planet':            dict(rho=5.5e3,    grad_rel=1.0/6.4e6,  virial=0.3,  v_pec=3.0e4),
}

# PASS criteria (chosen by 4-team consensus, NOT fit DOF)
PASS_CRITERIA = {
    'cosmic_mean':       ('OFF', 0.05),  # < 0.05
    'void_center':       ('OFF', 0.30),  # < 0.30 (loose)
    'cluster_core':      ('ON',  0.30),  # > 0.30 (intermediate OK)
    'galaxy_disk':       ('ON',  0.95),  # > 0.95
    'solar_neighborhood':('ON',  0.95),  # > 0.95
    'planet':            ('ON',  0.95),  # > 0.95 (Newton must hold)
}

# ============================================================
# Activation function (single sigmoid in log-space)
# ============================================================
def sigmoid_log(x, x_thresh, width=0.3, ascending=True):
    """f -> 1 if x >> x_thresh (ascending=True), or x << x_thresh (False)."""
    x = np.maximum(x, 1e-300)
    z = (np.log10(x) - np.log10(x_thresh)) / width
    if not ascending:
        z = -z
    return 1.0 / (1.0 + np.exp(-z))

# ============================================================
# 4 Axiom Activations (each: single threshold parameter)
# ============================================================
# Axiom A (Threshold): SQT activates when local density > rho_thresh
def f_A(env, rho_thresh, width=0.3):
    return sigmoid_log(env['rho'], rho_thresh, width, ascending=True)

# Axiom B (Gradient): SQT activates when |grad rho|/rho > g_thresh (1/m)
def f_B(env, grad_thresh, width=0.3):
    return sigmoid_log(env['grad_rel'], grad_thresh, width, ascending=True)

# Axiom D (Bound): SQT activates when virial < virial_thresh (bound systems)
def f_D(env, virial_thresh, width=0.3):
    return sigmoid_log(env['virial'], virial_thresh, width, ascending=False)

# Axiom H (Flow): SQT activates when v_pec > v_thresh
def f_H(env, v_thresh, width=0.3):
    return sigmoid_log(env['v_pec'], v_thresh, width, ascending=True)

AXIOMS = [
    ('A_threshold',  f_A, 'rho_thresh',   np.logspace(-28, -20, 200), 'rho [kg/m^3]'),
    ('B_gradient',   f_B, 'grad_thresh',  np.logspace(-26, -16, 200), '|grad rho|/rho [1/m]'),
    ('D_bound',      f_D, 'virial_thresh',np.logspace(-2, 4, 200),    'virial parameter'),
    ('H_flow',       f_H, 'v_thresh',     np.logspace(0, 7, 200),     'v_pec [m/s]'),
]

# ============================================================
# Score: how many environments PASS at given threshold
# ============================================================
def score_threshold(activation_fn, threshold, width=0.3):
    results = {}
    pass_count = 0
    fail_envs = []
    margin_min = 1.0
    for env_name, criterion in PASS_CRITERIA.items():
        f = activation_fn(ENV[env_name], threshold, width)
        results[env_name] = float(f)
        target, level = criterion
        if target == 'OFF':
            ok = f < level
            margin = level - f
        else:
            ok = f > level
            margin = f - level
        if ok:
            pass_count += 1
        else:
            fail_envs.append(env_name)
        margin_min = min(margin_min, margin)
    return dict(
        pass_count=pass_count,
        fail_envs=fail_envs,
        margin_min=margin_min,
        env_activations=results,
    )

# ============================================================
# Run scan for each axiom
# ============================================================
def run_axiom(name, fn, param_name, grid, label, width=0.3):
    scan = []
    for thresh in grid:
        s = score_threshold(fn, thresh, width)
        scan.append(dict(threshold=float(thresh), **s))
    # Find best (max pass_count, then max margin_min)
    best = max(scan, key=lambda r: (r['pass_count'], r['margin_min']))
    full_pass = [r for r in scan if r['pass_count'] == len(PASS_CRITERIA)]
    return dict(
        name=name, param_name=param_name, label=label, width=width,
        scan=scan, best=best, n_full_pass=len(full_pass),
        full_pass_range=(
            (float(full_pass[0]['threshold']), float(full_pass[-1]['threshold']))
            if full_pass else None
        ),
    )

print("=" * 60)
print("L66: Structural Scale-Separation Test")
print("=" * 60)

results_all = {}
for name, fn, pname, grid, label in AXIOMS:
    print(f"\nRunning axiom {name} ...")
    res = run_axiom(name, fn, pname, grid, label, width=0.3)
    results_all[name] = res
    bp = res['best']
    print(f"  best threshold = {bp['threshold']:.3e}")
    print(f"  pass_count     = {bp['pass_count']} / {len(PASS_CRITERIA)}")
    print(f"  margin_min     = {bp['margin_min']:.3f}")
    print(f"  full-PASS range: {res['full_pass_range']}")
    if bp['fail_envs']:
        print(f"  failed envs    : {bp['fail_envs']}")

# Sensitivity: rerun with width = 0.15 (steeper) and 0.6 (looser)
print("\n--- Width sensitivity (0.15 / 0.6) ---")
sensitivity = {}
for name, fn, pname, grid, label in AXIOMS:
    s_steep = run_axiom(name, fn, pname, grid, label, width=0.15)
    s_loose = run_axiom(name, fn, pname, grid, label, width=0.6)
    sensitivity[name] = dict(
        steep_n_pass=s_steep['n_full_pass'],
        loose_n_pass=s_loose['n_full_pass'],
        steep_best_pc=s_steep['best']['pass_count'],
        loose_best_pc=s_loose['best']['pass_count'],
    )
    print(f"  {name}: steep n_full_pass={s_steep['n_full_pass']}, "
          f"loose n_full_pass={s_loose['n_full_pass']}")

# ============================================================
# Visualization (6 panels)
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(20, 11))

env_order = list(PASS_CRITERIA.keys())
env_short = [e.replace('_', '\n') for e in env_order]

# Panels (a-d): per-axiom activation across threshold scan
panel_pos = [(0, 0), (0, 1), (0, 2), (1, 0)]
for i, (name, fn, pname, grid, label) in enumerate(AXIOMS):
    ax = axes[panel_pos[i]]
    res = results_all[name]
    # plot pass_count vs threshold
    pc = [r['pass_count'] for r in res['scan']]
    mm = [r['margin_min'] for r in res['scan']]
    ax2 = ax.twinx()
    ln1 = ax.plot(grid, pc, 'b-', lw=2, label='pass_count')
    ln2 = ax2.plot(grid, mm, 'r--', lw=1.5, label='margin_min', alpha=0.7)
    ax.set_xscale('log')
    ax.set_xlabel(label)
    ax.set_ylabel('pass_count', color='b')
    ax2.set_ylabel('margin_min', color='r')
    ax.set_ylim(-0.5, len(PASS_CRITERIA) + 0.5)
    ax2.set_ylim(-1, 1)
    ax.axhline(len(PASS_CRITERIA), color='gray', ls=':', alpha=0.5)
    bp = res['best']
    ax.axvline(bp['threshold'], color='green', ls='-.', alpha=0.5,
               label=f"best={bp['threshold']:.2e}")
    ax.set_title(f"({chr(97+i)}) Axiom {name}\nbest pc={bp['pass_count']}/{len(PASS_CRITERIA)}, "
                 f"full-PASS={res['n_full_pass']}/200")
    ax.grid(alpha=0.3)
    ax.legend(loc='upper left', fontsize=8)

# Panel (e): activation across environments at best threshold
ax = axes[1, 1]
ax.clear()
x = np.arange(len(env_order))
width_bar = 0.2
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']
for j, (name, fn, pname, grid, label) in enumerate(AXIOMS):
    bp = results_all[name]['best']
    activations = [bp['env_activations'][e] for e in env_order]
    ax.bar(x + (j - 1.5) * width_bar, activations, width_bar,
           label=name, color=colors[j], alpha=0.8)
ax.set_xticks(x)
ax.set_xticklabels(env_short, rotation=45, ha='right', fontsize=8)
ax.set_ylabel('activation f')
ax.set_ylim(0, 1.1)
# Mark PASS targets
for i, e in enumerate(env_order):
    target, level = PASS_CRITERIA[e]
    if target == 'OFF':
        ax.plot([i - 0.4, i + 0.4], [level, level], 'k-', lw=2)
        ax.fill_between([i - 0.4, i + 0.4], 0, level, alpha=0.1, color='green')
    else:
        ax.plot([i - 0.4, i + 0.4], [level, level], 'k-', lw=2)
        ax.fill_between([i - 0.4, i + 0.4], level, 1, alpha=0.1, color='green')
ax.legend(loc='upper left', fontsize=8)
ax.set_title('(e) Activation by environment (best threshold)\nGreen = PASS region')
ax.grid(alpha=0.3)

# Panel (f): summary text
ax = axes[1, 2]
ax.axis('off')

n_envs = len(PASS_CRITERIA)
summary_lines = [
    "L66: Structural Scale-Separation Test",
    "=" * 40,
    f"Environments tested: {n_envs}",
    f"PASS = single threshold satisfies all envs",
    "",
    "Results:",
]
for name, res in results_all.items():
    bp = res['best']
    star = "PASS" if bp['pass_count'] == n_envs else f"FAIL({bp['pass_count']}/{n_envs})"
    summary_lines.append(
        f"  {name:14s} {star:10s} "
        f"thresh={bp['threshold']:.2e}"
    )
    if bp['fail_envs']:
        summary_lines.append(f"      failed: {','.join(bp['fail_envs'])}")
    if res['full_pass_range']:
        lo, hi = res['full_pass_range']
        summary_lines.append(f"      PASS range: [{lo:.2e}, {hi:.2e}]")

summary_lines += [
    "",
    "Width sensitivity (n_full_pass):",
]
for name, s in sensitivity.items():
    summary_lines.append(
        f"  {name:14s} steep={s['steep_n_pass']:3d}  "
        f"loose={s['loose_n_pass']:3d}"
    )

summary_lines += [
    "",
    "Verdict (PASS = qualifies for L67):",
]
n_pass = sum(1 for r in results_all.values()
             if r['best']['pass_count'] == n_envs)
summary_lines.append(f"  Surviving axioms: {n_pass} / 4")

ax.text(0.02, 0.98, "\n".join(summary_lines),
        family='monospace', fontsize=9,
        transform=ax.transAxes, va='top')

plt.suptitle('L66: 4-Axiom Structural Scale-Separation Test', fontsize=14)
plt.tight_layout()
plt.savefig(OUT / 'L66_main.png', dpi=140, bbox_inches='tight')
plt.close()
print(f"\nSaved: {OUT / 'L66_main.png'}")

# ============================================================
# Save report (JSON, jsonifiable)
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
    environments=ENV,
    pass_criteria={k: list(v) for k, v in PASS_CRITERIA.items()},
    results={name: dict(
        param_name=r['param_name'],
        best=r['best'],
        n_full_pass=r['n_full_pass'],
        full_pass_range=r['full_pass_range'],
    ) for name, r in results_all.items()},
    sensitivity=sensitivity,
)
with open(OUT / 'report.json', 'w') as f:
    json.dump(_json(report), f, indent=2)

print(f"Saved: {OUT / 'report.json'}")
print("\n" + "=" * 60)
print("DONE")
print("=" * 60)
