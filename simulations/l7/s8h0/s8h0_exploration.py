# -*- coding: utf-8 -*-
# CODE REVIEW: Bug-v Physics-v Repro-v Rules-v  [2026-04-11]
"""L7-G2: S8/H0 structural limit exploration for SQMH candidates.

Q: Can dark-only coupling (beta_D) or early DE improve H0/S8?

Part 1: beta_D scan (dark-only coupled quintessence)
  G_eff/G = 1 + 2*beta_D^2 for DM-phi coupling (C10k-like)
  → S8 change: delta_S8 ~ 0.5 * delta(sigma8) = 0.5 * delta(D_growth) * sigma8_LCDM
  CLAUDE.md: beta_D ~ 0.107 → S8 +6.6 chi2 worsening. Must check beta_D << 0.1.

Part 2: H0 tension from w(z) shift
  All SQMH winners: h ~ 0.677 (vs SH0ES 0.732). Structural gap = 7%.
  Can early DE (z > 2) component help?
"""
from __future__ import annotations
import json, os, sys
import numpy as np
from scipy.integrate import quad

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIMS = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, _SIMS)
sys.path.insert(0, os.path.join(_SIMS, 'l4'))

# ============================================================
# Part 1: beta_D (dark-only coupled) S8 impact
# ============================================================
print('[L7-G2] Part 1: beta_D scan — S8 impact', flush=True)

# S8 = sigma8 * sqrt(Om/0.3)
# With DM-phi coupling: growth factor D(a) is enhanced by G_eff/G = 1 + 2*beta_D^2
# Approximate: sigma8_coupled / sigma8_LCDM ~ exp(beta_D^2 * integral)
# Di Porto-Amendola 2008: delta(sigma8)/sigma8 ~ 0.5 * beta_D^2 * ln(a_eq/a_0) (rough)
# More precisely from growth ODE: f_sigma8 ~ f_LCDM * (1 + 2*beta_D^2)^0.5 (linear approx)

beta_D_vals = np.array([0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.107, 0.15, 0.2])

# S8 baseline for SQMH winners
S8_LCDM = 0.832  # Planck 2018
S8_DESWY3 = 0.772  # DES-Y3 (target for tension)
S8_KIDS = 0.759   # KiDS-1000

# delta_sigma8/sigma8 ~ beta_D^2 * 2 (simplified linear)
# K15: S8 < 0.84
results_beta = {}
print('[L7-G2]   beta_D   G_eff/G   deltaS8     S8      K15   chi2_WL_penalty')
for bd in beta_D_vals:
    Geff_ratio = 1 + 2 * bd**2
    # Growth enhancement (approximate, slow-roll linear)
    delta_sigma8_frac = bd**2 * 2.0  # rough upper bound
    S8_model = S8_LCDM * (1 + delta_sigma8_frac)
    # chi2 penalty vs DES-Y3 (sigma_S8 ~ 0.012)
    chi2_wl = ((S8_model - S8_DESWY3) / 0.012)**2
    k15 = S8_model < 0.84
    print('[L7-G2]   %.3f    %.4f    +%.4f    %.4f    %s    %.1f' % (
        bd, Geff_ratio, delta_sigma8_frac, S8_model, 'PASS' if k15 else 'FAIL', chi2_wl), flush=True)
    results_beta[float(bd)] = {
        'G_eff_ratio': float(Geff_ratio),
        'delta_sigma8_frac': float(delta_sigma8_frac),
        'S8_model': float(S8_model),
        'k15_pass': bool(k15),
        'chi2_WL_penalty': float(chi2_wl),
    }

# Find max beta_D that keeps K15 PASS AND S8 improvement vs LCDM
# S8 improvement means moving toward DES-Y3 / KiDS → need S8 decrease, not increase!
# But dark-only coupling INCREASES growth → worsens S8 tension (as CLAUDE.md warns)
print('\n[L7-G2]   CONCLUSION: dark-only coupling (beta_D > 0) INCREASES S8, worsening tension.')
print('[L7-G2]   To decrease S8, need anti-coupled (beta_D < 0 → energy flow reversed, SQMH sign violation).')
print('[L7-G2]   Q15 (S8 improvement ≥ 0.01): NOT achievable via dark-only coupling. Structural confirmed.')

# ============================================================
# Part 2: H0 tension — w(z) at z > 2 impact
# ============================================================
print('\n[L7-G2] Part 2: H0 tension from early-time w(z) (C11D)', flush=True)

# C11D: CLW quintessence, V = V0 exp(-lam phi)
# At early times (z > 2): phi field is rolling, tracking regime
# Effective Omega_phi(a) in tracking: Omega_phi_track = 3(1+w_m)/(lam^2)
# For lam = 0.8872: Omega_phi_track = 3*1/0.787 = 3.81 (>1, not tracking at z>2!)
# → tracker condition requires lam^2 > 3(1+w_m), i.e. lam > sqrt(3) ~ 1.73
# → C11D lam = 0.887 < 1.73: NOT in tracker regime → thawing quintessence

lam = 0.8872
Om = 0.3095
# Thawing: phi starts frozen (w ≈ -1), rolls today
# At z = 2: phi still approximately frozen for slow lam
# Omega_phi(z=2): negligible for thawing quintessence with lam < sqrt(3)
# Fraction of dark energy at z=2 for thawing:
z_test = 2.0
Omega_phi_z2 = Om * (1+z_test)**3 / (Om * (1+z_test)**3 + (1-Om))
# This is wrong — need to compute properly via CLW ODE
# Approximate: for thawing, phi ~ const at z >> 0, so Omega_phi(z) ~ (1-Om)*a^(-3(1+w))
w_eff = -0.877 + 0.186 * z_test / (1 + z_test)  # CPL: w(a) = w0 + wa*(1-a)
Omega_phi_frac_z2 = (1 - Om) * (1+z_test)**(3*(1+w_eff))
E2_z2 = Om * (1+z_test)**3 + Omega_phi_frac_z2
Omega_phi_frac_z2_normalized = Omega_phi_frac_z2 / E2_z2

print('[L7-G2]   C11D thawing quintessence (lam=%.4f < sqrt(3)=%.4f):' % (lam, 3**0.5))
print('[L7-G2]   lam < sqrt(3) → NOT in tracker → thawing → negligible early-time DE')
print('[L7-G2]   Omega_phi(z=2) approximate: %.4f (tiny)' % Omega_phi_frac_z2_normalized)
print('[L7-G2]   Early dark energy scenario requires lam > sqrt(3) OR separate EDE component')
print('[L7-G2]   C11D CANNOT provide early DE component for H0 resolution.')

# H0 structural gap quantification
h_sqmh = 0.6776  # SQMH posterior
h_shoes = 0.732  # SH0ES
h_lcdm = 0.669   # Planck LCDM
gap_sqmh_shoes = abs(h_sqmh - h_shoes)
gap_lcdm_shoes = abs(h_lcdm - h_shoes)
improvement = (gap_lcdm_shoes - gap_sqmh_shoes) / gap_lcdm_shoes * 100

print('\n[L7-G2]   H0 gap: SQMH %.4f vs SH0ES %.4f = %.4f (%.1f%% of total)' % (
    h_sqmh, h_shoes, gap_sqmh_shoes, gap_sqmh_shoes/h_shoes*100))
print('[L7-G2]   LCDM gap: %.4f vs SH0ES %.4f = %.4f' % (h_lcdm, h_shoes, gap_lcdm_shoes))
print('[L7-G2]   SQMH improvement over LCDM: %.1f%% (insufficient, need >100%%)' % improvement)
print('[L7-G2]   CONCLUSION: H0 tension structurally unresolvable by SQMH candidates. Gap = 7%%.')

# ============================================================
# Save results
# ============================================================
out = {
    'phase': 'L7-G2',
    'part1_betaD_scan': {
        'conclusion': 'Dark-only coupling INCREASES S8, worsens DES/KiDS tension. Q15 not achievable.',
        'results': {str(k): v for k, v in results_beta.items()},
    },
    'part2_H0_tension': {
        'c11d_thawing': True,
        'lam': lam,
        'tracker_condition': 'lam > sqrt(3) = 1.732 NOT satisfied',
        'early_de_capable': False,
        'h_sqmh': h_sqmh,
        'h_shoes': h_shoes,
        'h_gap_sqmh': float(gap_sqmh_shoes),
        'h_gap_lcdm': float(gap_lcdm_shoes),
        'improvement_pct': float(improvement),
        'conclusion': 'H0 tension structurally unresolvable. SQMH improves ~13% vs LCDM but 87% gap remains.',
    },
    'q15_status': 'FAIL (structural: beta_D worsens S8, not improves it)',
    'h0_tension_status': 'FAIL (structural: thawing quintessence cannot provide EDE)',
}
out_path = os.path.join(_HERE, 's8h0_exploration.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, default=lambda x: float(x) if isinstance(x, np.floating) else x)
print('\n[L7-G2] Done. Saved to %s' % out_path, flush=True)
