# -*- coding: utf-8 -*-
# CODE REVIEW: Bug-v Physics-v Repro-v Rules-v  [2026-04-11]
"""L6: Collect all completed evidence JSON results and update occam_analysis.json."""
from __future__ import annotations
import json, os, sys, glob
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))

# L5 fixed-theta values (for comparison)
L5_FIXED = {
    'LCDM': -843.689,
    'C28':  11.257,
    'C11D':  8.951,
    'A12':  10.779,
    'A17':  10.780,
    'A01':  10.690,
    'A05':  10.581,
    'A06':  10.574,
    'A08':   9.635,
    'A09':  10.010,
}

def load_all():
    results = {}
    for jf in sorted(glob.glob(os.path.join(_HERE, 'evidence_*.json'))):
        if 'occam' in jf or 'summary' in jf:
            continue
        try:
            with open(jf, encoding='utf-8') as f:
                d = json.load(f)
            mid = d.get('ID', os.path.basename(jf).replace('evidence_','').replace('.json',''))
            results[mid] = d
            print('[collect] %s: delta_logz=%.4f K17=%s' % (mid, d.get('delta_logz', float('nan')), d.get('k17_pass','?')))
        except Exception as e:
            print('[collect] WARN: %s -> %s' % (jf, e))
    return results

def main():
    results = load_all()

    # Extract LCDM baseline (use hires if available)
    lcdm_logz = -843.689  # L5 default
    if 'LCDM' in results:
        lcdm_logz = results['LCDM']['logz']
        print('[collect] Using L6-hires LCDM logz=%.4f' % lcdm_logz)

    # Recalculate delta_logz relative to hires LCDM if needed
    summary = {}
    for mid, d in results.items():
        if mid == 'LCDM':
            continue
        dz = d.get('delta_logz', float('nan'))
        # If result used L5 LCDM baseline, recalculate
        if abs(d.get('lcdm_logz', -843.689) - (-843.689)) < 0.01 and abs(lcdm_logz - (-843.689)) > 0.01:
            dz = d['logz'] - lcdm_logz
            print('[collect] %s: recalculated delta_logz=%.4f (using hires LCDM)' % (mid, dz))
        summary[mid] = {
            'logz': d.get('logz'),
            'logz_err': d.get('logz_err'),
            'delta_logz': dz,
            'k17_pass': dz >= 2.5,
            'jeffreys': 'STRONG' if dz > 5 else 'substantial' if dz > 2.5 else 'weak' if dz > 1 else 'inconclusive',
            'nlive': d.get('nlive'),
            'l5_fixed_theta': L5_FIXED.get(mid, None),
            'occam_delta': (d.get('logz', float('nan')) - dz) if d.get('logz') is not None else None,  # not meaningful here
        }

    # Occam analysis: C28 vs A12 (if both available)
    print('\n--- Occam Summary ---')
    if 'C28' in summary and 'A12' in summary:
        gap_c28_a12 = summary['C28']['delta_logz'] - summary['A12']['delta_logz']
        # Gaussian Occam penalty: -0.5 * (ndim_extra * ln(2*pi*e))
        # C28 ndim=3 vs A12 ndim=2 → 1 extra dim, Occam_diff ≈ -1.38 nats (L5 estimate)
        occam_diff = -1.380  # conservative from L5
        net = gap_c28_a12 + occam_diff
        print('C28 - A12 gap = %.4f  occam_diff = %.4f  net = %.4f  justified=%s' % (
            gap_c28_a12, occam_diff, net, net > 0))
        summary['_occam_C28_vs_A12'] = {
            'delta_logz_gap': gap_c28_a12,
            'occam_diff': occam_diff,
            'net': net,
            'justified': net > 0,
        }

    if 'C11D' in summary and 'A12' in summary:
        gap_c11d_a12 = summary['C11D']['delta_logz'] - summary['A12']['delta_logz']
        occam_diff = -0.746  # conservative from L5
        net = gap_c11d_a12 + occam_diff
        print('C11D - A12 gap = %.4f  occam_diff = %.4f  net = %.4f  justified=%s' % (
            gap_c11d_a12, occam_diff, net, net > 0))
        summary['_occam_C11D_vs_A12'] = {
            'delta_logz_gap': gap_c11d_a12,
            'occam_diff': occam_diff,
            'net': net,
            'justified': net > 0,
        }

    # Save
    out = {'lcdm_logz_hires': lcdm_logz, 'results': summary}
    out_path = os.path.join(_HERE, 'evidence_summary_L6.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, default=lambda x: float(x) if isinstance(x, np.floating) else x)
    print('\n[collect] Saved to', out_path)

if __name__ == '__main__':
    main()
