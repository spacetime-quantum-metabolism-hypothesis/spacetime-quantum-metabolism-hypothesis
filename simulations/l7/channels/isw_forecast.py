# -*- coding: utf-8 -*-
# CODE REVIEW: Bug-v Physics-v Repro-v Rules-v  [2026-04-11]
"""L7-X2: ISW power spectrum forecast — C11D vs LCDM using classy.

Integrated Sachs-Wolfe (ISW) effect: late-time DE changes gravitational
potential → cross-correlation C_l^{Tg} between CMB temperature and galaxy counts.
CMB-S4 / Simons Observatory sensitivity can distinguish DE models.
"""
from __future__ import annotations
import json, os, sys, time
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))

try:
    import classy
except ImportError:
    print('[L7-X2] classy not installed', flush=True)
    sys.exit(1)

def run_isw(label, w0, wa, Om, h, lmax=200):
    """Compute ISW C_l^TT and C_l^Tg proxy for a CPL DE model."""
    omega_b = 0.02237
    omega_cdm = Om * h**2 - omega_b
    if omega_cdm <= 0:
        return None

    params = {
        'h': h,
        'omega_b': omega_b,
        'omega_cdm': omega_cdm,
        'n_s': 0.9649,
        'A_s': 2.1e-9,
        'tau_reio': 0.0544,
        'output': 'tCl,pCl,lCl',
        'lensing': 'no',
        'l_max_scalars': lmax,
    }
    if abs(w0 + 1.0) > 0.001 or abs(wa) > 0.001:
        OmDE = 1.0 - Om
        params['Omega_fld'] = OmDE
        params['w0_fld'] = w0
        params['wa_fld'] = wa
        params['cs2_fld'] = 1.0

    c = classy.Class()
    c.set(params)
    try:
        c.compute()
        cl = c.raw_cl(lmax)
        tt = cl['tt']  # TT power spectrum
        c.struct_cleanup()
        return tt
    except Exception as e:
        c.struct_cleanup()
        print('[L7-X2] %s error: %s' % (label, e), flush=True)
        return None

def main():
    t0 = time.time()
    print('[L7-X2] ISW forecast: C11D vs LCDM using classy', flush=True)
    lmax = 100  # ISW is relevant at low-l

    # CPL approximations
    candidates = [
        ('LCDM', -1.000,  0.000, 0.320, 0.669),
        ('C11D', -0.877, -0.186, 0.3095, 0.6776),
        ('A12',  -0.886, -0.133, 0.3095, 0.6770),
    ]

    cls = {}
    for label, w0, wa, Om, h in candidates:
        print('[L7-X2] Computing %s...' % label, flush=True)
        tt = run_isw(label, w0, wa, Om, h, lmax=lmax)
        if tt is not None:
            cls[label] = tt.tolist()
            print('[L7-X2] %s C_l[2]=%.4e C_l[10]=%.4e C_l[50]=%.4e' % (
                label, tt[2], tt[10], tt[50]), flush=True)

    # Compute fractional difference vs LCDM at low-l
    if 'LCDM' in cls and 'C11D' in cls:
        tt_lcdm = np.array(cls['LCDM'])
        tt_c11d = np.array(cls['C11D'])
        ls = np.arange(lmax + 1)
        # ISW is at l < 20
        isw_band = slice(2, 20)
        frac_diff = (tt_c11d[isw_band] - tt_lcdm[isw_band]) / tt_lcdm[isw_band]
        rms_diff = float(np.sqrt(np.mean(frac_diff**2)))
        print('\n[L7-X2] ISW band (l=2-19) RMS fractional diff C11D vs LCDM: %.4f%%' % (rms_diff * 100), flush=True)

        # CMB-S4 sensitivity at low-l (cosmic variance limited l<30 + noise)
        # Cosmic variance sigma_l ~ sqrt(2/(2l+1)) * C_l
        cv_sigma = np.sqrt(2.0 / (2 * ls[isw_band] + 1)) * tt_lcdm[isw_band]
        snr_per_l = np.abs(tt_c11d[isw_band] - tt_lcdm[isw_band]) / cv_sigma
        total_snr = float(np.sqrt(np.sum(snr_per_l**2)))
        print('[L7-X2] ISW CMB-S4 cosmic-variance SNR (C11D vs LCDM): %.4f' % total_snr, flush=True)
        print('[L7-X2] ISW distinguishable at CMB-S4? %s (need SNR > 1)' % (total_snr > 1), flush=True)
    else:
        rms_diff = None
        total_snr = None

    dt = time.time() - t0
    out = {
        'phase': 'L7-X2',
        'method': 'classy_CPL_ISW',
        'lmax': lmax,
        'cls': cls,
        'isw_analysis': {
            'band': 'l=2-19',
            'rms_frac_diff_C11D_LCDM': rms_diff,
            'cmbs4_cosmic_variance_snr': total_snr,
            'distinguishable': total_snr > 1.0 if total_snr is not None else None,
        },
        'wall_sec': float(dt),
    }
    out_path = os.path.join(_HERE, 'isw_forecast.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, default=lambda x: float(x) if isinstance(x, np.floating) else x)
    print('[L7-X2] Done in %.1fs. Saved to %s' % (dt, out_path), flush=True)

if __name__ == '__main__':
    main()
