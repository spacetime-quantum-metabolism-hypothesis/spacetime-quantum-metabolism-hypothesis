# -*- coding: utf-8 -*-
"""
ee2_mcmc.py  --  EE2 Dark Energy MCMC (L23 Phase 2)
=====================================================
Three MCMC runs with emcee:
  Run 1-2 : A-free  (B fixed at B_EE2)   -- theta = [Omega_m, H0, A]
  Run 3-4 : B-free  (A fixed at A_EE2)   -- theta = [Omega_m, H0, B]
  Run 5-6 : A+B free                      -- theta = [Omega_m, H0, A, B]
  Run 7-8 : result analysis + corner plots + AICc table + cross-check

CLAUDE.md compliance:
- OMP/MKL/OPENBLAS_NUM_THREADS=1 enforced at import time
- matplotlib.use('Agg') before any matplotlib/corner import
- numpy 2.x: trapz -> trapezoid (via cumulative_trapezoid in ee2_fit)
- ASCII-only in print()
- emcee reproducibility: np.random.seed(42) inside run_mcmc call
- MCMC chi2 failure -> return -np.inf (no sentinel 1e6)
- emcee only (no dynesty)
- multiprocessing spawn pool for parallel walkers
"""

import os
import sys

# Thread safety for multiprocessing workers (must be first)
os.environ['OMP_NUM_THREADS']     = '1'
os.environ['MKL_NUM_THREADS']     = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import math
import warnings
import numpy as np

# matplotlib backend before ANY matplotlib/corner import
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')
np.seterr(all='ignore')

# ── Import paths ─────────────────────────────────────────────────────────────
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SIM_DIR    = os.path.dirname(_SCRIPT_DIR)

for _p in [_SCRIPT_DIR, _SIM_DIR]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

import emcee
import corner

from desi_data import DESI_DR2, DESI_DR2_COV_INV
from ee2_ode   import (solve_ee2, E_LCDM,
                        A_EE2, B_EE2, OL0_EE2,
                        OMEGA_M_FID, OMEGA_R_FID, H0_KMS)
from ee2_fit   import (compute_theory_vector, aicc,
                        C_KMS, R_S, OR, N_DATA, N_GRID)
from scipy.integrate import cumulative_trapezoid

# ── Constants ─────────────────────────────────────────────────────────────────
AICC_LCDM = 15.39   # Phase 1 reference (k=2, n=13)
N_WALKERS = 32
N_STEPS   = 3000
N_BURN    = 1000

# MCMC uses same N_GRID as ee2_fit (4000) to ensure chi2 cross-check passes
# ODE solver uses production solve_ee2 (max_step=5e-3, rtol=1e-9)
N_GRID_MCMC  = N_GRID   # 4000, same as ee2_fit production


# ═══════════════════════════════════════════════════════════════════════════════
# THEORY VECTOR WITH FREE A, B
# ═══════════════════════════════════════════════════════════════════════════════

def compute_theory_vector_ee2(Omega_m, H0, A=A_EE2, B=B_EE2):
    """
    BAO theory vector for EE2 with arbitrary A, B.
    Uses production solve_ee2 (DOP853 forward-shooting, max_step=5e-3).
    N_GRID_MCMC=1500 (reduced from 4000) for comoving integral grid.
    Returns ndarray shape (13,) or None on failure.
    """
    z_eff = DESI_DR2['z_eff']
    z_max = z_eff.max() + 0.01
    z_grid = np.linspace(0.0, z_max, N_GRID)

    _, E_grid, _ = solve_ee2(
        A=A, B=B, OL0=OL0_EE2,
        Omega_m=Omega_m, Omega_r=OR,
        z_arr=z_grid,
    )
    if E_grid is None:
        return None

    inv_E = 1.0 / np.maximum(E_grid, 1e-15)

    DM_cum = (C_KMS / H0) * np.concatenate(
        [[0.0], cumulative_trapezoid(inv_E, z_grid)]
    )

    theory_vec = np.empty(N_DATA)
    for i, (z, qty) in enumerate(zip(z_eff, DESI_DR2['quantity'])):
        idx = min(np.searchsorted(z_grid, z), N_GRID - 1)
        E_z = E_grid[idx]
        DH  = C_KMS / (H0 * E_z)
        DM  = DM_cum[idx]
        DV  = (z * DM**2 * DH)**(1.0/3.0) if z > 0 else 0.0

        if   'DV' in qty:
            theory_vec[i] = DV / R_S
        elif 'DM' in qty:
            theory_vec[i] = DM / R_S
        elif 'DH' in qty:
            theory_vec[i] = DH / R_S
        else:
            theory_vec[i] = np.nan

    return theory_vec


def chi2_ee2_free(Omega_m, H0, A=A_EE2, B=B_EE2):
    """chi2 for EE2 with free A, B. Returns float or np.inf on failure."""
    th = compute_theory_vector_ee2(Omega_m, H0, A=A, B=B)
    if th is None or not np.all(np.isfinite(th)):
        return np.inf
    delta = DESI_DR2['value'] - th
    return float(delta @ DESI_DR2_COV_INV @ delta)


# ═══════════════════════════════════════════════════════════════════════════════
# LOG-PROBABILITY FUNCTIONS (for emcee)
# ═══════════════════════════════════════════════════════════════════════════════

def log_prob_A_free(theta):
    """
    Run 1-2: A-free, B fixed.
    theta = [Omega_m, H0, A]
    Prior: Omega_m U[0.20, 0.45], H0 U[60, 80], A U[0.0, 0.5]
    """
    Om, H0, A = theta
    if not (0.20 <= Om <= 0.45 and 60.0 <= H0 <= 80.0 and 0.0 <= A <= 0.5):
        return -np.inf
    c2 = chi2_ee2_free(Om, H0, A=A, B=B_EE2)
    if not np.isfinite(c2):
        return -np.inf
    return -0.5 * c2


def log_prob_B_free(theta):
    """
    Run 3-4: B-free, A fixed.
    theta = [Omega_m, H0, B]
    Prior: Omega_m U[0.20, 0.45], H0 U[60, 80], B U[1.0, 30.0]
    """
    Om, H0, B = theta
    if not (0.20 <= Om <= 0.45 and 60.0 <= H0 <= 80.0 and 1.0 <= B <= 30.0):
        return -np.inf
    c2 = chi2_ee2_free(Om, H0, A=A_EE2, B=B)
    if not np.isfinite(c2):
        return -np.inf
    return -0.5 * c2


def log_prob_AB_free(theta):
    """
    Run 5-6: A+B free.
    theta = [Omega_m, H0, A, B]
    Prior: Omega_m U[0.20, 0.45], H0 U[60, 80], A U[0.0, 0.5], B U[1.0, 30.0]
    """
    Om, H0, A, B = theta
    if not (0.20 <= Om <= 0.45 and 60.0 <= H0 <= 80.0
            and 0.0 <= A <= 0.5 and 1.0 <= B <= 30.0):
        return -np.inf
    c2 = chi2_ee2_free(Om, H0, A=A, B=B)
    if not np.isfinite(c2):
        return -np.inf
    return -0.5 * c2


# ═══════════════════════════════════════════════════════════════════════════════
# MCMC RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_mcmc(log_prob_fn, p0, label, n_walkers=N_WALKERS,
             n_steps=N_STEPS, n_burn=N_BURN, pool=None):
    """
    Run emcee EnsembleSampler.
    p0: initial positions (n_walkers, ndim)
    pool: multiprocessing Pool (optional, must be created externally)
    Returns flat_chain (post-burn) shape (n_walkers*(n_steps-n_burn), ndim)
    """
    ndim = p0.shape[1]
    print(f'  Starting {label}: {n_walkers} walkers x {n_steps} steps '
          f'({n_burn} burn), ndim={ndim}')

    sampler = emcee.EnsembleSampler(n_walkers, ndim, log_prob_fn, pool=pool)

    # emcee reproducibility: seed inside run_mcmc (CLAUDE.md rule)
    np.random.seed(42)
    sampler.run_mcmc(p0, n_steps, progress=False)

    flat = sampler.get_chain(discard=n_burn, flat=True)
    accept = np.mean(sampler.acceptance_fraction)
    print(f'    Acceptance fraction: {accept:.3f}')
    print(f'    Flat chain shape: {flat.shape}')
    return flat, sampler


# ═══════════════════════════════════════════════════════════════════════════════
# STATISTICS
# ═══════════════════════════════════════════════════════════════════════════════

def chain_stats(flat_chain, param_idx):
    """Median and 68% CI for parameter at param_idx."""
    samples = flat_chain[:, param_idx]
    lo, med, hi = np.percentile(samples, [16, 50, 84])
    return med, lo, hi


def best_chi2_from_chain(flat_chain, log_prob_fn):
    """Find minimum chi2 in flat chain via log_prob evaluation."""
    log_probs = np.array([log_prob_fn(theta) for theta in flat_chain])
    best_lp = np.max(log_probs[np.isfinite(log_probs)])
    return -2.0 * best_lp


# ═══════════════════════════════════════════════════════════════════════════════
# PLOTS
# ═══════════════════════════════════════════════════════════════════════════════

def save_corner(flat_chain, labels, title, outfile, truths=None):
    """Save corner plot to file."""
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
    print(f'  Saved corner plot: {outfile}')


# ═══════════════════════════════════════════════════════════════════════════════
# CROSS-CHECK (Round 7-8)
# ═══════════════════════════════════════════════════════════════════════════════

def cross_check():
    """
    Verify that chi2_ee2_free matches ee2_fit.chi2() for the EE2 fixed case.
    Also verify LCDM chi2 via compute_theory_vector.
    """
    from ee2_fit import chi2 as chi2_fit

    # EE2 fixed parameters
    Om_test = OMEGA_M_FID  # 0.315
    H0_test = H0_KMS       # 67.4

    c2_fit  = chi2_fit(Om_test, H0_test, 'ee2')
    c2_new  = chi2_ee2_free(Om_test, H0_test, A=A_EE2, B=B_EE2)
    c2_diff = abs(c2_fit - c2_new)

    print('Cross-check: chi2_ee2_free vs ee2_fit.chi2 (EE2 fixed params):')
    print(f'  ee2_fit.chi2    = {c2_fit:.6f}')
    print(f'  chi2_ee2_free   = {c2_new:.6f}')
    print(f'  |diff|          = {c2_diff:.2e}')
    if c2_diff < 1e-3:
        print('  PASS: chi2 functions agree to < 1e-3')
    else:
        print('  WARN: chi2 functions disagree -- investigate')

    # LCDM cross-check
    c2_lcdm_fit = chi2_fit(Om_test, H0_test, 'lcdm')
    th_lcdm = compute_theory_vector(Om_test, H0_test, 'lcdm')
    delta_lcdm = DESI_DR2['value'] - th_lcdm
    c2_lcdm_new = float(delta_lcdm @ DESI_DR2_COV_INV @ delta_lcdm)
    print('Cross-check: LCDM chi2:')
    print(f'  ee2_fit.chi2    = {c2_lcdm_fit:.6f}')
    print(f'  recomputed      = {c2_lcdm_new:.6f}')
    print(f'  |diff|          = {abs(c2_lcdm_fit - c2_lcdm_new):.2e}')
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    OUT_DIR = _SCRIPT_DIR

    print('=' * 60)
    print('EE2 MCMC Phase 2 -- L23')
    print('=' * 60)
    print(f'A_EE2 = {A_EE2:.6f}  (2*exp(-pi))')
    print(f'B_EE2 = {B_EE2:.6f}  (2*pi/ln2)')
    print(f'N_WALKERS={N_WALKERS}, N_STEPS={N_STEPS}, N_BURN={N_BURN}')
    print(f'N_DATA={N_DATA}, AICc(LCDM,k=2) reference = {AICC_LCDM}')
    print()

    # ── Round 7-8 pre-run cross-check ────────────────────────────────────────
    print('--- Cross-check (Round 7-8) ---')
    cross_check()

    # ── Initial positions (ball around LCDM best-fit region) ─────────────────
    rng = np.random.default_rng(42)

    # A-free: [Omega_m, H0, A]
    p0_A = np.column_stack([
        rng.uniform(0.29, 0.34, N_WALKERS),   # Omega_m
        rng.uniform(65.0, 70.0, N_WALKERS),   # H0
        rng.uniform(0.04, 0.14, N_WALKERS),   # A (around theory val 0.0864)
    ])

    # B-free: [Omega_m, H0, B]
    p0_B = np.column_stack([
        rng.uniform(0.29, 0.34, N_WALKERS),   # Omega_m
        rng.uniform(65.0, 70.0, N_WALKERS),   # H0
        rng.uniform(6.0,  12.0, N_WALKERS),   # B (around theory val 9.065)
    ])

    # AB-free: [Omega_m, H0, A, B]
    p0_AB = np.column_stack([
        rng.uniform(0.29, 0.34, N_WALKERS),   # Omega_m
        rng.uniform(65.0, 70.0, N_WALKERS),   # H0
        rng.uniform(0.04, 0.14, N_WALKERS),   # A
        rng.uniform(6.0,  12.0, N_WALKERS),   # B
    ])

    # ── Multiprocessing Pool (spawn, 8 workers for 32 walkers) ───────────────
    import multiprocessing
    ctx = multiprocessing.get_context('spawn')
    N_WORKERS = min(8, multiprocessing.cpu_count() - 1)
    N_WORKERS = max(1, N_WORKERS)
    print(f'Using {N_WORKERS} parallel workers for emcee (spawn pool)')

    # ── Run 1-2: A-free MCMC ─────────────────────────────────────────────────
    print('--- Run 1-2: A-free MCMC (B = B_EE2 fixed) ---')
    with ctx.Pool(N_WORKERS) as pool_A:
        flat_A, sampler_A = run_mcmc(
            log_prob_A_free, p0_A,
            label='A-free', pool=pool_A,
        )

    # Stats for A-free
    Om_med_A, Om_lo_A, Om_hi_A = chain_stats(flat_A, 0)
    H0_med_A, H0_lo_A, H0_hi_A = chain_stats(flat_A, 1)
    A_med,    A_lo,    A_hi    = chain_stats(flat_A, 2)
    A_sigma_half = (A_hi - A_lo) / 2.0
    A_offset_sigma = (A_med - A_EE2) / A_sigma_half if A_sigma_half > 0 else np.nan

    # Best chi2 from chain for AICc
    print('  Computing best chi2 from A-free chain...')
    chi2_A_best = best_chi2_from_chain(flat_A, log_prob_A_free)
    aicc_A = aicc(chi2_A_best, k=3, n=N_DATA)
    d_aicc_A = aicc_A - AICC_LCDM

    # ── Run 3-4: B-free MCMC ─────────────────────────────────────────────────
    print('--- Run 3-4: B-free MCMC (A = A_EE2 fixed) ---')
    with ctx.Pool(N_WORKERS) as pool_B:
        flat_B, sampler_B = run_mcmc(
            log_prob_B_free, p0_B,
            label='B-free', pool=pool_B,
        )

    Om_med_B, Om_lo_B, Om_hi_B = chain_stats(flat_B, 0)
    H0_med_B, H0_lo_B, H0_hi_B = chain_stats(flat_B, 1)
    B_med,    B_lo,    B_hi    = chain_stats(flat_B, 2)
    B_sigma_half = (B_hi - B_lo) / 2.0
    B_offset_sigma = (B_med - B_EE2) / B_sigma_half if B_sigma_half > 0 else np.nan

    print('  Computing best chi2 from B-free chain...')
    chi2_B_best = best_chi2_from_chain(flat_B, log_prob_B_free)
    aicc_B = aicc(chi2_B_best, k=3, n=N_DATA)
    d_aicc_B = aicc_B - AICC_LCDM

    # ── Run 5-6: A+B free MCMC ───────────────────────────────────────────────
    print('--- Run 5-6: A+B free MCMC ---')
    with ctx.Pool(N_WORKERS) as pool_AB:
        flat_AB, sampler_AB = run_mcmc(
            log_prob_AB_free, p0_AB,
            label='A+B-free', pool=pool_AB,
        )

    Om_med_AB, Om_lo_AB, Om_hi_AB = chain_stats(flat_AB, 0)
    H0_med_AB, H0_lo_AB, H0_hi_AB = chain_stats(flat_AB, 1)
    A_med_AB, A_lo_AB, A_hi_AB    = chain_stats(flat_AB, 2)
    B_med_AB, B_lo_AB, B_hi_AB    = chain_stats(flat_AB, 3)

    print('  Computing best chi2 from A+B-free chain...')
    chi2_AB_best = best_chi2_from_chain(flat_AB, log_prob_AB_free)
    aicc_AB = aicc(chi2_AB_best, k=4, n=N_DATA)
    d_aicc_AB = aicc_AB - AICC_LCDM

    # ── Run 7-8: Print results ────────────────────────────────────────────────
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
    print('{:<25} {:>6}  {:>10}  {:>12}'.format(
        'Model', 'k', 'AICc', 'Delta_AICc'))
    print('-' * 58)
    print('{:<25} {:>6}  {:>10.3f}  {:>12}'.format(
        'LCDM (reference)', 2, AICC_LCDM, '0.000'))
    print('{:<25} {:>6}  {:>10.3f}  {:>12.3f}'.format(
        'EE2 A-free', 3, aicc_A, d_aicc_A))
    print('{:<25} {:>6}  {:>10.3f}  {:>12.3f}'.format(
        'EE2 B-free', 3, aicc_B, d_aicc_B))
    print('{:<25} {:>6}  {:>10.3f}  {:>12.3f}'.format(
        'EE2 A+B-free', 4, aicc_AB, d_aicc_AB))

    # Verdict
    print()
    print('--- Verdict ---')
    for name, d_aicc in [('A-free', d_aicc_A), ('B-free', d_aicc_B),
                          ('A+B-free', d_aicc_AB)]:
        if d_aicc > 6:
            v = 'LCDM strongly preferred'
        elif d_aicc > 2:
            v = 'LCDM moderately preferred'
        elif d_aicc > 0:
            v = 'LCDM slightly preferred'
        else:
            v = 'EE2 variant preferred'
        print(f'  {name}: Delta_AICc={d_aicc:.3f} -> {v}')

    # ── Corner plots ──────────────────────────────────────────────────────────
    print()
    print('Generating corner plots...')

    save_corner(
        flat_A,
        labels=['Omega_m', 'H0', 'A'],
        title='EE2 A-free MCMC (B fixed = {:.4f})'.format(B_EE2),
        outfile=os.path.join(OUT_DIR, 'ee2_mcmc_corner_A_free.png'),
        truths=[None, None, A_EE2],
    )

    save_corner(
        flat_B,
        labels=['Omega_m', 'H0', 'B'],
        title='EE2 B-free MCMC (A fixed = {:.5f})'.format(A_EE2),
        outfile=os.path.join(OUT_DIR, 'ee2_mcmc_corner_B_free.png'),
        truths=[None, None, B_EE2],
    )

    save_corner(
        flat_AB,
        labels=['Omega_m', 'H0', 'A', 'B'],
        title='EE2 A+B-free MCMC',
        outfile=os.path.join(OUT_DIR, 'ee2_mcmc_corner_AB_free.png'),
        truths=[None, None, A_EE2, B_EE2],
    )

    # ── Posterior histogram: A and B ──────────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    ax = axes[0]
    ax.hist(flat_A[:, 2], bins=50, color='steelblue', alpha=0.7,
            density=True, label='A posterior (B fixed)')
    ax.axvline(A_EE2,  color='red',   lw=2, ls='--', label=f'A theory={A_EE2:.4f}')
    ax.axvline(A_med,  color='black', lw=1.5, ls='-', label=f'A median={A_med:.4f}')
    ax.set_xlabel('A')
    ax.set_ylabel('Posterior density')
    ax.set_title('A-free posterior')
    ax.legend(fontsize=9)

    ax = axes[1]
    ax.hist(flat_B[:, 2], bins=50, color='darkorange', alpha=0.7,
            density=True, label='B posterior (A fixed)')
    ax.axvline(B_EE2,  color='red',   lw=2, ls='--', label=f'B theory={B_EE2:.4f}')
    ax.axvline(B_med,  color='black', lw=1.5, ls='-', label=f'B median={B_med:.4f}')
    ax.set_xlabel('B')
    ax.set_ylabel('Posterior density')
    ax.set_title('B-free posterior')
    ax.legend(fontsize=9)

    plt.suptitle('EE2 MCMC Posterior: A and B marginals', fontsize=12)
    plt.tight_layout()
    hist_out = os.path.join(OUT_DIR, 'ee2_mcmc_AB_posteriors.png')
    plt.savefig(hist_out, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'  Saved: {hist_out}')

    print()
    print('=== ee2_mcmc.py complete ===')


if __name__ == '__main__':
    main()
