# -*- coding: utf-8 -*-
"""
ee2_mcmc_analyze.py -- Run 7-8: Load saved chains and produce results + plots
Usage: python3 ee2_mcmc_analyze.py
"""
import os, sys
os.environ['OMP_NUM_THREADS']     = '1'
os.environ['MKL_NUM_THREADS']     = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import warnings
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')
np.seterr(all='ignore')

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SIM_DIR    = os.path.dirname(_SCRIPT_DIR)
for _p in [_SCRIPT_DIR, _SIM_DIR]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

import corner
from ee2_mcmc import (
    log_prob_A_free, log_prob_B_free, log_prob_AB_free,
    chain_stats,
    A_EE2, B_EE2, AICC_LCDM, N_DATA,
    cross_check,
)


def best_chi2_fast(flat_chain, log_prob_fn, n_sample=300, rng_seed=42):
    """
    Estimate best chi2 from chain by evaluating log_prob on a random subsample.
    n_sample=300 is sufficient for chains of ~9600 points.
    """
    rng = np.random.default_rng(rng_seed)
    idx = rng.choice(len(flat_chain), size=min(n_sample, len(flat_chain)), replace=False)
    sub = flat_chain[idx]
    log_probs = np.array([log_prob_fn(theta) for theta in sub])
    finite = log_probs[np.isfinite(log_probs)]
    if len(finite) == 0:
        return np.inf
    return -2.0 * np.max(finite)
from ee2_fit import aicc


# ── Cross-check ───────────────────────────────────────────────────────────────
print('=' * 60)
print('EE2 MCMC -- Run 7-8: Analysis')
print('=' * 60)
print(f'A_EE2 = {A_EE2:.6f}  (2*exp(-pi))')
print(f'B_EE2 = {B_EE2:.6f}  (2*pi/ln2)')
print()
print('--- Cross-check ---')
cross_check()

# ── Load chains ───────────────────────────────────────────────────────────────
chain_a  = os.path.join(_SCRIPT_DIR, 'ee2_mcmc_chain_a_free.npy')
chain_b  = os.path.join(_SCRIPT_DIR, 'ee2_mcmc_chain_b_free.npy')
chain_ab = os.path.join(_SCRIPT_DIR, 'ee2_mcmc_chain_ab_free.npy')

print('Loading chains...')
flat_A  = np.load(chain_a)
flat_B  = np.load(chain_b)
flat_AB = np.load(chain_ab)
print(f'  A-free  chain: {flat_A.shape}')
print(f'  B-free  chain: {flat_B.shape}')
print(f'  AB-free chain: {flat_AB.shape}')
print()

# ── A-free stats ──────────────────────────────────────────────────────────────
Om_med_A, Om_lo_A, Om_hi_A = chain_stats(flat_A, 0)
H0_med_A, H0_lo_A, H0_hi_A = chain_stats(flat_A, 1)
A_med, A_lo, A_hi = chain_stats(flat_A, 2)
A_sigma_half = (A_hi - A_lo) / 2.0
A_offset_sigma = (A_med - A_EE2) / A_sigma_half if A_sigma_half > 0 else float('nan')

print('Computing best chi2 from A-free chain (subsample 300/9600)...')
chi2_A_best = best_chi2_fast(flat_A, log_prob_A_free)
aicc_A = aicc(chi2_A_best, k=3, n=N_DATA)
d_aicc_A = aicc_A - AICC_LCDM

# ── B-free stats ──────────────────────────────────────────────────────────────
Om_med_B, Om_lo_B, Om_hi_B = chain_stats(flat_B, 0)
H0_med_B, H0_lo_B, H0_hi_B = chain_stats(flat_B, 1)
B_med, B_lo, B_hi = chain_stats(flat_B, 2)
B_sigma_half = (B_hi - B_lo) / 2.0
B_offset_sigma = (B_med - B_EE2) / B_sigma_half if B_sigma_half > 0 else float('nan')

print('Computing best chi2 from B-free chain (subsample 300/9600)...')
chi2_B_best = best_chi2_fast(flat_B, log_prob_B_free)
aicc_B = aicc(chi2_B_best, k=3, n=N_DATA)
d_aicc_B = aicc_B - AICC_LCDM

# ── AB-free stats ─────────────────────────────────────────────────────────────
Om_med_AB, Om_lo_AB, Om_hi_AB = chain_stats(flat_AB, 0)
H0_med_AB, H0_lo_AB, H0_hi_AB = chain_stats(flat_AB, 1)
A_med_AB, A_lo_AB, A_hi_AB = chain_stats(flat_AB, 2)
B_med_AB, B_lo_AB, B_hi_AB = chain_stats(flat_AB, 3)

print('Computing best chi2 from AB-free chain (subsample 300/9600)...')
chi2_AB_best = best_chi2_fast(flat_AB, log_prob_AB_free)
aicc_AB = aicc(chi2_AB_best, k=4, n=N_DATA)
d_aicc_AB = aicc_AB - AICC_LCDM

# ── Print full results ────────────────────────────────────────────────────────
print()
print('=' * 60)
print('=== MCMC Results ===')
print('=' * 60)

print()
print('--- A-free (B fixed at B_EE2 = {:.4f}) ---'.format(B_EE2))
print('A_median = {:.4f}  [{:.4f}, {:.4f}] (68% CI)'.format(A_med, A_lo, A_hi))
print('A_theory = {:.4f}  -> offset: {:.2f} sigma'.format(A_EE2, A_offset_sigma))
print('Omega_m  = {:.4f}  [{:.4f}, {:.4f}]'.format(Om_med_A, Om_lo_A, Om_hi_A))
print('H0       = {:.3f}  [{:.3f}, {:.3f}]'.format(H0_med_A, H0_lo_A, H0_hi_A))
print('best chi2(A-free)    = {:.3f}'.format(chi2_A_best))
print('AICc(A-free, k=3)   = {:.3f}'.format(aicc_A))
print('AICc(LCDM,   k=2)   = {:.3f}'.format(AICC_LCDM))
print('Delta_AICc(A-free vs LCDM) = {:.3f}'.format(d_aicc_A))

print()
print('--- B-free (A fixed at A_EE2 = {:.5f}) ---'.format(A_EE2))
print('B_median = {:.4f}  [{:.4f}, {:.4f}] (68% CI)'.format(B_med, B_lo, B_hi))
print('B_theory = {:.4f}  -> offset: {:.2f} sigma'.format(B_EE2, B_offset_sigma))
print('Omega_m  = {:.4f}  [{:.4f}, {:.4f}]'.format(Om_med_B, Om_lo_B, Om_hi_B))
print('H0       = {:.3f}  [{:.3f}, {:.3f}]'.format(H0_med_B, H0_lo_B, H0_hi_B))
print('best chi2(B-free)    = {:.3f}'.format(chi2_B_best))
print('AICc(B-free, k=3)   = {:.3f}'.format(aicc_B))
print('AICc(LCDM,   k=2)   = {:.3f}'.format(AICC_LCDM))
print('Delta_AICc(B-free vs LCDM) = {:.3f}'.format(d_aicc_B))

print()
print('--- A+B free ---')
print('A_median = {:.4f}  [{:.4f}, {:.4f}]'.format(A_med_AB, A_lo_AB, A_hi_AB))
print('B_median = {:.4f}  [{:.4f}, {:.4f}]'.format(B_med_AB, B_lo_AB, B_hi_AB))
print('Omega_m  = {:.4f}  [{:.4f}, {:.4f}]'.format(Om_med_AB, Om_lo_AB, Om_hi_AB))
print('H0       = {:.3f}  [{:.3f}, {:.3f}]'.format(H0_med_AB, H0_lo_AB, H0_hi_AB))
print('best chi2(A+B-free) = {:.3f}'.format(chi2_AB_best))
print('AICc(k=4)           = {:.3f}'.format(aicc_AB))
print('AICc(LCDM,  k=2)   = {:.3f}'.format(AICC_LCDM))
print('Delta_AICc(A+B-free vs LCDM) = {:.3f}'.format(d_aicc_AB))

print()
print('--- AICc Summary Table ---')
print('{:<25} {:>6}  {:>10}  {:>12}'.format('Model', 'k', 'AICc', 'Delta_AICc'))
print('-' * 58)
print('{:<25} {:>6}  {:>10.3f}  {:>12}'.format('LCDM (reference)', 2, AICC_LCDM, '0.000'))
print('{:<25} {:>6}  {:>10.3f}  {:>12.3f}'.format('EE2 A-free', 3, aicc_A, d_aicc_A))
print('{:<25} {:>6}  {:>10.3f}  {:>12.3f}'.format('EE2 B-free', 3, aicc_B, d_aicc_B))
print('{:<25} {:>6}  {:>10.3f}  {:>12.3f}'.format('EE2 A+B-free', 4, aicc_AB, d_aicc_AB))

print()
print('--- Verdict ---')
for name, d_aicc in [('A-free', d_aicc_A), ('B-free', d_aicc_B), ('A+B-free', d_aicc_AB)]:
    if d_aicc > 6:
        v = 'LCDM strongly preferred'
    elif d_aicc > 2:
        v = 'LCDM moderately preferred'
    elif d_aicc > 0:
        v = 'LCDM slightly preferred'
    else:
        v = 'EE2 variant preferred'
    print(f'  {name}: Delta_AICc={d_aicc:.3f} -> {v}')

# ── Corner plots ──────────────────────────────────────────────────────────────
print()
print('Generating corner plots...')

def save_corner(flat_chain, labels, title, outfile, truths=None):
    fig = corner.corner(
        flat_chain,
        labels=labels,
        truths=truths,
        quantiles=[0.16, 0.50, 0.84],
        show_titles=True,
        title_kwargs={'fontsize': 10},
        truth_color='red',
    )
    fig.suptitle(title, fontsize=12, y=1.01)
    fig.savefig(outfile, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved: {outfile}')

save_corner(
    flat_A,
    labels=['Omega_m', 'H0', 'A'],
    title='EE2 A-free MCMC (B fixed = {:.4f})'.format(B_EE2),
    outfile=os.path.join(_SCRIPT_DIR, 'ee2_mcmc_corner_A_free.png'),
    truths=[None, None, A_EE2],
)

save_corner(
    flat_B,
    labels=['Omega_m', 'H0', 'B'],
    title='EE2 B-free MCMC (A fixed = {:.5f})'.format(A_EE2),
    outfile=os.path.join(_SCRIPT_DIR, 'ee2_mcmc_corner_B_free.png'),
    truths=[None, None, B_EE2],
)

save_corner(
    flat_AB,
    labels=['Omega_m', 'H0', 'A', 'B'],
    title='EE2 A+B-free MCMC',
    outfile=os.path.join(_SCRIPT_DIR, 'ee2_mcmc_corner_AB_free.png'),
    truths=[None, None, A_EE2, B_EE2],
)

# ── Posterior histograms ──────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

ax = axes[0]
ax.hist(flat_A[:, 2], bins=50, color='steelblue', alpha=0.7,
        density=True, label='A posterior (B fixed)')
ax.axvline(A_EE2, color='red',   lw=2, ls='--', label=f'A theory={A_EE2:.4f}')
ax.axvline(A_med, color='black', lw=1.5, ls='-', label=f'A median={A_med:.4f}')
ax.set_xlabel('A')
ax.set_ylabel('Posterior density')
ax.set_title('A-free posterior')
ax.legend(fontsize=9)

ax = axes[1]
ax.hist(flat_B[:, 2], bins=50, color='darkorange', alpha=0.7,
        density=True, label='B posterior (A fixed)')
ax.axvline(B_EE2, color='red',   lw=2, ls='--', label=f'B theory={B_EE2:.4f}')
ax.axvline(B_med, color='black', lw=1.5, ls='-', label=f'B median={B_med:.4f}')
ax.set_xlabel('B')
ax.set_ylabel('Posterior density')
ax.set_title('B-free posterior')
ax.legend(fontsize=9)

plt.suptitle('EE2 MCMC Posterior: A and B marginals', fontsize=12)
plt.tight_layout()
hist_out = os.path.join(_SCRIPT_DIR, 'ee2_mcmc_AB_posteriors.png')
plt.savefig(hist_out, dpi=150, bbox_inches='tight')
plt.close()
print(f'  Saved: {hist_out}')

print()
print('=== ee2_mcmc_analyze.py complete ===')
