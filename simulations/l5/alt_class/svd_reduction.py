# -*- coding: utf-8 -*-
"""
L5-F. Alt-20 SVD class reduction.

Take the 14 L5-target alt candidates (A01, A03-A06, A08, A09, A11-A13,
A15-A17, A19, A20), compute their best-fit E^2(z)/E^2_LCDM(z) - 1 across
z in [0, 2], stack into a matrix, run SVD, and extract:
  * singular values (explained variance per mode)
  * n_eff = number of independent drift directions at 99% variance
  * principal drift modes (shape of V1, V2, ...)

This quantifies whether the "alt-20 cluster" is really one physics or
several. Expected result: n_eff = 1 (Taylor-equivalent degeneracy).
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')

_THIS = os.path.dirname(os.path.abspath(__file__))
_L5 = os.path.dirname(_THIS)
_SIMS = os.path.dirname(_L5)
for _p in (_SIMS, _L5):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# We need the build_E closures from runner.ALT
sys.path.insert(0, os.path.join(_SIMS, 'l4_alt'))
import runner as alt_runner  # noqa: E402
from l4.common import E_lcdm, OMEGA_R, LCDM_CHI2  # noqa: E402

# Load L4 alt-20 fit results for best-fit (Om, h) per candidate
_ALT_RESULTS = os.path.join(_SIMS, 'l4_alt', 'alt20_results.json')
with open(_ALT_RESULTS, 'r', encoding='utf-8') as f:
    alt_data = json.load(f)

# The L5 target class: L2/L3 survivors (15) minus A10 killed (= 14 + A04 outlier)
L5_TARGETS = ['A01', 'A03', 'A04', 'A05', 'A06', 'A08', 'A09', 'A11',
              'A12', 'A13', 'A15', 'A16', 'A17', 'A19', 'A20']


def build_E_best(aid):
    """Rebuild best-fit E(z) from stored Om, h and runner.ALT closed form."""
    rec = next(r for r in alt_data['results'] if r['id'] == aid)
    Om = rec['Om']
    h = rec['h']
    name, f_ratio = alt_runner.ALT[aid]
    build = alt_runner._make_E(f_ratio)
    return build([], Om, h), Om, h, rec['delta_chi2']


def main():
    # Redshift grid
    z = np.linspace(0.0, 2.0, 201)
    # LCDM reference at the same Om as each candidate (so we isolate shape,
    # not Om shift)
    rows = []
    meta = []
    for aid in L5_TARGETS:
        E_model, Om, h, dchi2 = build_E_best(aid)
        E_ref = E_lcdm(Om, h)
        E2_model = np.array([float(E_model(zi)) ** 2 for zi in z])
        E2_ref = np.array([float(E_ref(zi)) ** 2 for zi in z])
        delta = (E2_model - E2_ref) / E2_ref  # relative deviation
        rows.append(delta)
        meta.append({'id': aid, 'Om': Om, 'h': h, 'dchi2': dchi2})

    M = np.array(rows)  # shape (14, 201)

    # SVD: M = U * S * V^T  where rows of V^T are principal modes
    U, S, Vt = np.linalg.svd(M, full_matrices=False)
    variance = S ** 2
    frac = variance / variance.sum()
    cum = np.cumsum(frac)

    # n_eff definitions
    n_eff_99 = int(np.searchsorted(cum, 0.99) + 1)
    n_eff_999 = int(np.searchsorted(cum, 0.999) + 1)
    # Effective number of modes (participation ratio)
    n_eff_pr = float(1.0 / np.sum(frac ** 2))

    # Project each candidate onto the principal mode
    proj_mode1 = U[:, 0] * S[0]
    proj_mode2 = U[:, 1] * S[1] if len(S) >= 2 else np.zeros_like(proj_mode1)

    result = {
        'n_candidates': int(M.shape[0]),
        'n_z_points': int(M.shape[1]),
        'singular_values': S.tolist(),
        'variance_fractions': frac.tolist(),
        'cumulative_variance': cum.tolist(),
        'n_eff_99': n_eff_99,
        'n_eff_999': n_eff_999,
        'n_eff_participation_ratio': n_eff_pr,
        'principal_mode1_shape': (Vt[0]).tolist(),
        'principal_mode2_shape': (Vt[1]).tolist() if len(S) >= 2 else None,
        'z_grid': z.tolist(),
        'candidates': [
            {
                **meta[i],
                'proj_mode1': float(proj_mode1[i]),
                'proj_mode2': float(proj_mode2[i]),
            }
            for i in range(M.shape[0])
        ],
    }

    # Print summary
    print("=== Alt-20 SVD Class Reduction ===")
    print(f"  Matrix shape: {M.shape}")
    print(f"  Singular values: {np.array2string(S[:5], precision=4)}")
    print(f"  Variance fractions (top 5): "
          f"{np.array2string(frac[:5], precision=4)}")
    print(f"  Cumulative variance: "
          f"{np.array2string(cum[:5], precision=5)}")
    print(f"  n_eff @ 99% variance:  {n_eff_99}")
    print(f"  n_eff @ 99.9% variance: {n_eff_999}")
    print(f"  n_eff (participation ratio): {n_eff_pr:.3f}")

    print("\n  Mode 1 projection (candidates sorted by |proj|):")
    ordered = sorted(result['candidates'],
                     key=lambda r: -abs(r['proj_mode1']))
    for r in ordered:
        print(f"    {r['id']}: proj1={r['proj_mode1']:+.4f}  "
              f"proj2={r['proj_mode2']:+.4f}  Δχ²={r['dchi2']:+.2f}")

    # Cluster representative: the candidate with max |proj_mode1| AND
    # the best (most negative) Δχ² is the single best drift-class champion.
    scored = [(-r['dchi2'] + 0.5 * abs(r['proj_mode1']), r['id'])
              for r in ordered]
    scored.sort(reverse=True)
    champion = scored[0][1]
    result['cluster_representative'] = champion
    print(f"\n  Cluster champion (-Δχ² + 0.5|proj1|): {champion}")

    out_path = os.path.join(_THIS, 'class_reduction.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    print(f"\nWrote {out_path}")

    # Plot
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
        # Left: singular values (log scale)
        axes[0].semilogy(np.arange(1, len(S) + 1), S, 'o-', lw=1.5)
        axes[0].set_xlabel('Mode index')
        axes[0].set_ylabel('Singular value')
        axes[0].set_title('Alt-20 drift-shape SVD spectrum')
        axes[0].grid(True, alpha=0.3)
        # Annotate cumulative variance
        for i in range(min(5, len(cum))):
            axes[0].annotate(f'{cum[i] * 100:.2f}%',
                             (i + 1, S[i]), fontsize=8,
                             textcoords='offset points', xytext=(5, 5))
        # Right: principal mode shapes
        axes[1].plot(z, Vt[0], 'b-', label='Mode 1')
        if len(S) >= 2:
            axes[1].plot(z, Vt[1], 'r--', label='Mode 2')
        if len(S) >= 3:
            axes[1].plot(z, Vt[2], 'g:', label='Mode 3')
        axes[1].set_xlabel('z')
        axes[1].set_ylabel('Principal component of ΔE²/E²_LCDM')
        axes[1].set_title('Principal drift modes')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        plt.tight_layout()
        fig_path = os.path.join(
            _SIMS, '..', 'paper', 'figures', 'l5_alt_class_svd.png')
        os.makedirs(os.path.dirname(fig_path), exist_ok=True)
        plt.savefig(fig_path, dpi=150)
        plt.close(fig)
        print(f"Wrote {fig_path}")
    except Exception as e:
        print(f"(plot skipped: {e})")


if __name__ == '__main__':
    main()
