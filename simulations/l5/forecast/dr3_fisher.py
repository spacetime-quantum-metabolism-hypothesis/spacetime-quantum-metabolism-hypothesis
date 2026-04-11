# -*- coding: utf-8 -*-
"""
L5-G. DESI DR3 Fisher forecast for all L5 survivors.

For each candidate, compute sigma(w_0), sigma(w_a), correlation, and
predicted LCDM separation on the w_a axis using the DR3 precision
projection (~2x improvement over DR2).

Also computes pairwise discrimination |w_a^A - w_a^B| / sqrt(2) / sigma(w_a)
between candidates — if < 2, DR3 cannot distinguish them.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

_THIS = os.path.dirname(os.path.abspath(__file__))
_L5 = os.path.dirname(_THIS)
_SIMS = os.path.dirname(_L5)
sys.path.insert(0, _SIMS)
sys.path.insert(0, _L5)
sys.path.insert(0, os.path.join(_SIMS, 'l4_alt'))

from l5.common import dr3_fisher_forecast, jsonify  # noqa: E402
from l4.common import E_lcdm, LCDM_OM, LCDM_H  # noqa: E402
import runner as alt_runner  # noqa: E402

# Load alt-20 best-fit results
with open(os.path.join(_SIMS, 'l4_alt', 'alt20_results.json'), 'r') as f:
    alt_data = json.load(f)


def get_alt_E(aid):
    rec = next(r for r in alt_data['results'] if r['id'] == aid)
    name, fr = alt_runner.ALT[aid]
    build = alt_runner._make_E(fr)
    return build([], rec['Om'], rec['h']), rec['Om'], rec['h']


# Mainstream best-fit (from paper/06_mcmc_results.md and base.l4.result.md)
MAINSTREAM = {
    'C28': {'Om': 0.310, 'h': 0.677, 'w0': -0.849, 'wa': -0.242,
            'note': 'Maggiore RR (CPL template)'},
    'C33': {'Om': 0.340, 'h': 0.647, 'w0': -0.984, 'wa': -0.262,
            'note': 'f(Q) teleparallel (CPL template)'},
}

L5_ALT_TIER1 = ['A01', 'A05', 'A12', 'A17']
L5_ALT_TIER4 = ['A03', 'A06', 'A08', 'A09', 'A11', 'A13', 'A15', 'A16',
                'A19', 'A20', 'A04']


def make_cpl_E(Om, h, w0, wa):
    """Build E(z) from CPL (Om, h, w0, wa) for mainstream candidates."""
    OL = 1.0 - Om - 9.2e-5
    Omega_r = 9.2e-5
    def E(z):
        z = np.asarray(z, dtype=float)
        f = (1.0 + z) ** (3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * z / (1.0 + z))
        return np.sqrt(Omega_r * (1 + z) ** 4 + Om * (1 + z) ** 3 + OL * f)
    return E


def main():
    results = []

    # LCDM baseline Fisher
    E_lc = E_lcdm(LCDM_OM, LCDM_H)
    f_lc = dr3_fisher_forecast(E_lc, LCDM_OM, LCDM_H)
    f_lc['id'] = 'LCDM'
    results.append(f_lc)

    # Mainstream
    for mid, cfg in MAINSTREAM.items():
        E = make_cpl_E(cfg['Om'], cfg['h'], cfg['w0'], cfg['wa'])
        f = dr3_fisher_forecast(E, cfg['Om'], cfg['h'])
        f['id'] = mid
        f['note'] = cfg['note']
        results.append(f)

    # Alt-20 Tier 1
    for aid in L5_ALT_TIER1 + L5_ALT_TIER4:
        E, Om, h = get_alt_E(aid)
        f = dr3_fisher_forecast(E, Om, h)
        f['id'] = aid
        results.append(f)

    # Print table
    print("=== DESI DR3 Fisher forecast ===")
    print(f"{'ID':<6}{'w0_fid':>10}{'wa_fid':>10}"
          f"{'σ(w0)':>10}{'σ(wa)':>10}{'ρ':>8}{'LCDM sep':>11}")
    for r in results:
        print(f"{r['id']:<6}{r['w0_fid']:>10.4f}{r['wa_fid']:>10.4f}"
              f"{r['sigma_w0']:>10.4f}{r['sigma_wa']:>10.4f}"
              f"{r['rho']:>8.3f}{r['lcdm_sep_sigma']:>10.2f}σ")

    # Pairwise discrimination matrix for candidates with |wa| > 0.05
    sharp = [r for r in results
             if r['id'] != 'LCDM' and abs(r['wa_fid']) > 0.05]
    print("\n=== Pairwise DR3 discrimination (|Δwa|/√2/σ(wa)) ===")
    print("  (DR3 can distinguish pairs with value > 2)")
    header = '      ' + ''.join(f"{r['id']:>7}" for r in sharp)
    print(header)
    pair_matrix = {}
    for i, a in enumerate(sharp):
        line = f"  {a['id']:<4}"
        pair_matrix[a['id']] = {}
        for j, b in enumerate(sharp):
            if i == j:
                line += '      -'
                pair_matrix[a['id']][b['id']] = 0.0
                continue
            sig = 0.5 * (a['sigma_wa'] + b['sigma_wa'])
            sep = abs(a['wa_fid'] - b['wa_fid']) / (sig * np.sqrt(2))
            line += f"{sep:>7.2f}"
            pair_matrix[a['id']][b['id']] = float(sep)
        print(line)

    out = {
        'lcdm_baseline': {
            'Om': LCDM_OM, 'h': LCDM_H,
            'sigma_wa': f_lc['sigma_wa'],
            'sigma_w0': f_lc['sigma_w0'],
        },
        'dr3_precision_assumed': {'sigma_DA': 0.008, 'sigma_H': 0.010},
        'candidates': results,
        'pairwise': pair_matrix,
    }
    out_path = os.path.join(_THIS, 'dr3_forecast.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(jsonify(out), f, indent=2)
    print(f"\nWrote {out_path}")

    # Plot
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.patches import Ellipse
        fig, ax = plt.subplots(figsize=(8, 6))
        colors = {'LCDM': 'k', 'C28': 'b', 'C33': 'g',
                  'A01': 'r', 'A05': 'orange', 'A12': 'purple', 'A17': 'brown'}
        for r in results:
            col = colors.get(r['id'], 'gray')
            ax.errorbar(r['w0_fid'], r['wa_fid'],
                        xerr=r['sigma_w0'], yerr=r['sigma_wa'],
                        fmt='o', color=col, label=r['id'],
                        capsize=3, markersize=6 if r['id'] in colors else 3)
        ax.axhline(0, color='k', lw=0.5, alpha=0.5)
        ax.axvline(-1, color='k', lw=0.5, alpha=0.5)
        ax.set_xlabel('w_0')
        ax.set_ylabel('w_a')
        ax.set_title('DESI DR3 Fisher forecast — L5 candidates')
        ax.legend(fontsize=8, loc='upper left', ncol=2)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        fig_path = os.path.join(
            _SIMS, '..', 'paper', 'figures', 'l5_dr3_forecast.png')
        plt.savefig(fig_path, dpi=150)
        plt.close(fig)
        print(f"Wrote {fig_path}")
    except Exception as e:
        print(f"(plot skipped: {e})")


if __name__ == '__main__':
    main()
