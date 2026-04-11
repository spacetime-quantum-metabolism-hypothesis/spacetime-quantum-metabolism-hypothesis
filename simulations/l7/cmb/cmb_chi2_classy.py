# -*- coding: utf-8 -*-
# CODE REVIEW: Bug-v Physics-v Repro-v Rules-v  [2026-04-11]
"""L7-C: Formal CMB chi2 via classy (K23 verdict).

Method: compute TT power spectrum for each DE model (CPL approx),
compare to Planck-best-fit LCDM spectrum using cosmic-variance chi2.
chi2_cv = sum_l (2l+1)/2 * [(C_l^model/C_l^LCDM - 1)^2]  (l=2..l_max)

K23: if chi2_cv(model) - chi2_cv(LCDM) > 6 → FAIL (LCDM always wins over itself = 0).
So K23 = chi2_cv(model) <= 6.

Also compute theta_s comparison for sanity check.
"""
from __future__ import annotations
import json, os, sys, time
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))

try:
    import classy
except ImportError:
    print('[L7-C] classy not installed', flush=True)
    sys.exit(1)

LMAX = 500  # ISW + first few acoustic peaks; sufficient for K23

# Planck 2018 best-fit LCDM parameters (Aghanim+2020 Table 2, TT+TE+EE+lowl+lowE)
LCDM_PLANCK = {
    'h': 0.6736,
    'omega_b': 0.02237,
    'omega_cdm': 0.1200,
    'n_s': 0.9649,
    'A_s': 2.101e-9,
    'tau_reio': 0.0544,
}

def run_class_tt(label, h, omega_b, omega_cdm, n_s, A_s, tau_reio, w0=-1.0, wa=0.0, lmax=LMAX):
    """Compute C_l^TT for given params. Returns array indexed 0..lmax."""
    OmDE = 1.0 - (omega_b + omega_cdm) / h**2
    if OmDE <= 0.01 or OmDE >= 0.99:
        print('[L7-C] %s: OmDE=%.3f out of range' % (label, OmDE), flush=True)
        return None

    params = {
        'h': h, 'omega_b': omega_b, 'omega_cdm': omega_cdm,
        'n_s': n_s, 'A_s': A_s, 'tau_reio': tau_reio,
        'output': 'tCl', 'lensing': 'no', 'l_max_scalars': lmax,
    }
    if abs(w0 + 1.0) > 1e-4 or abs(wa) > 1e-4:
        params['Omega_fld'] = OmDE
        params['w0_fld'] = w0
        params['wa_fld'] = wa
        params['cs2_fld'] = 1.0

    c = classy.Class()
    c.set(params)
    try:
        c.compute()
        cl = c.raw_cl(lmax)
        th_100 = c.theta_s_100()
        c.struct_cleanup()
        return cl['tt'], th_100
    except Exception as e:
        c.struct_cleanup()
        print('[L7-C] %s classy error: %s' % (label, str(e)[:80]), flush=True)
        return None

def chi2_vs_lcdm(tt_model, tt_lcdm, lmin=2, lmax=LMAX):
    """Cosmic-variance chi2 of model vs LCDM reference spectrum."""
    ls = np.arange(lmax + 1, dtype=float)
    weight = (2 * ls + 1) / 2.0
    ratio = tt_model / (tt_lcdm + 1e-300)
    # chi2 = sum_l weight_l * (ratio - 1)^2
    chi2 = float(np.sum(weight[lmin:lmax+1] * (ratio[lmin:lmax+1] - 1)**2))
    return chi2

def main():
    t0 = time.time()
    print('[L7-C] classy CMB K23 verdict (TT cosmic-variance chi2)', flush=True)
    print('[L7-C] LCDM reference: Planck 2018 best-fit', flush=True)

    # Step 1: LCDM reference (Planck best-fit)
    print('\n[L7-C] Computing LCDM reference...', flush=True)
    lcdm_result = run_class_tt('LCDM', **LCDM_PLANCK, lmax=LMAX)
    if lcdm_result is None:
        print('[L7-C] LCDM FAILED', flush=True)
        sys.exit(1)
    tt_lcdm, th_lcdm = lcdm_result
    print('[L7-C] LCDM theta_s_100=%.5f' % th_lcdm, flush=True)

    # Step 2: DE models — use LCDM Planck params + CPL DE
    # (same omega_b, omega_cdm, n_s, A_s, tau; vary only w0, wa)
    # Note: for fair comparison, use same base params but allow h to shift slightly
    # via Omega_fld constraint (flat universe)
    candidates = [
        # label, w0, wa, h_init (adjusted for each model from L5 posterior)
        ('C11D', -0.877, -0.186, 0.6776),
        ('A12',  -0.886, -0.133, 0.6770),
        ('C28',  -0.849, -0.242, 0.6789),
    ]

    results = {}
    for label, w0, wa, h_model in candidates:
        print('\n[L7-C] --- %s (w0=%.3f wa=%.3f h=%.4f) ---' % (label, w0, wa, h_model), flush=True)
        model_result = run_class_tt(
            label, h=h_model,
            omega_b=LCDM_PLANCK['omega_b'],
            omega_cdm=LCDM_PLANCK['omega_cdm'],
            n_s=LCDM_PLANCK['n_s'],
            A_s=LCDM_PLANCK['A_s'],
            tau_reio=LCDM_PLANCK['tau_reio'],
            w0=w0, wa=wa, lmax=LMAX
        )
        if model_result is None:
            results[label] = {'error': 'class failed'}
            continue
        tt_model, th_model = model_result

        chi2 = chi2_vs_lcdm(tt_model, tt_lcdm)
        # K23: chi2 vs LCDM ≤ 6 → PASS
        k23 = chi2 <= 6.0
        print('[L7-C] %s: theta_s_100=%.5f  chi2_cv=%.4f  K23=%s' % (
            label, th_model, chi2, 'PASS' if k23 else 'FAIL'), flush=True)
        print('[L7-C] %s: Δtheta_s_100 = %.5f vs LCDM %.5f' % (
            label, th_model - th_lcdm, th_lcdm), flush=True)

        results[label] = {
            'h_model': float(h_model),
            'theta_s_100_model': float(th_model),
            'theta_s_100_lcdm': float(th_lcdm),
            'delta_theta_s_100': float(th_model - th_lcdm),
            'chi2_cv_vs_lcdm': float(chi2),
            'k23_threshold': 6.0,
            'k23_pass': bool(k23),
        }

    dt = time.time() - t0
    out = {
        'phase': 'L7-C',
        'method': 'classy_TT_cosmic_variance_chi2',
        'lmax': LMAX,
        'lcdm_reference': LCDM_PLANCK,
        'lcdm_theta_s_100': float(th_lcdm),
        'note': 'CPL approximation for C11D/A12/C28. chi2_cv = sum_l (2l+1)/2 (Cl^model/Cl^LCDM - 1)^2.',
        'results': results,
        'wall_sec': float(dt),
    }
    out_path = os.path.join(_HERE, 'cmb_chi2_L7.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)
    print('\n[L7-C] Done in %.1fs. Saved to %s' % (dt, out_path), flush=True)

if __name__ == '__main__':
    main()
