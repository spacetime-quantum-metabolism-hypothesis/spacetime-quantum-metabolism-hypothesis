# -*- coding: utf-8 -*-
"""
Phase 3.5 A2 -- r_d promoted to a free MCMC parameter.

Re-uses all Phase 3 likelihood machinery from mcmc_phase3.py but adds
`r_d` to the parameter vector with a flat prior [130, 165] Mpc (Planck +
DESI DR2 consensus window with safety margin).

Parameter vectors:
  LCDM   : (Om, h, omb, s8, r_d)                        k = 5
  V_RP   : (Om, h, omb, s8, r_d, beta, n)               k = 7
  V_exp  : (Om, h, omb, s8, r_d, beta, lam)             k = 7

Runs emcee with the same seed as mcmc_phase3.py for reproducibility.
Writes chains to `chains/lcdm_rdfree_*.npy`, etc., so A1 outputs survive.
"""
import os
import sys
import time
import matplotlib
matplotlib.use('Agg')
import numpy as np
import emcee

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'phase2'))

import config
import desi_fitting as df
import compressed_cmb as ccmb

import mcmc_phase3 as m3
from mcmc_phase3 import (SN, _fast_sn_chi2, _fast_E_quint, _EWrap,
                         _bridge_highz, E_lcdm_factory, rsd_chi2_lcdm,
                         rsd_chi2_quint, Z_RSD, N_RSD, _finite)


# --- Flat prior on r_d ---
RD_LO, RD_HI = 130.0, 165.0    # Mpc


def log_prior_lcdm5(theta):
    Om, h, omb, s8, rd = theta
    if not (0.20 < Om < 0.45): return -np.inf
    if not (0.55 < h < 0.80): return -np.inf
    if not (RD_LO < rd < RD_HI): return -np.inf
    lp = -0.5 * ((omb - 0.02237) / 0.00015)**2
    lp += -0.5 * ((s8 - 0.8111) / 0.02)**2
    omc = Om * h * h - omb
    if not (0.05 < omc < 0.20): return -np.inf
    return lp


def log_prior_rp7(theta):
    Om, h, omb, s8, rd, beta, n = theta
    base = log_prior_lcdm5((Om, h, omb, s8, rd))
    if not np.isfinite(base): return -np.inf
    if not (0.0 <= beta < 1.0): return -np.inf
    if not (0.05 < n < 3.0): return -np.inf
    return base


def log_prior_exp7(theta):
    Om, h, omb, s8, rd, beta, lam = theta
    base = log_prior_lcdm5((Om, h, omb, s8, rd))
    if not np.isfinite(base): return -np.inf
    if not (0.0 <= beta < 1.0): return -np.inf
    if not (0.05 < lam < 3.0): return -np.inf
    return base


def log_like_lcdm5(theta):
    Om, h, omb, s8, rd = theta
    omc = Om * h * h - omb
    E = E_lcdm_factory(Om)
    c_bao = df.chi2(_EWrap(E), rd)                          # r_d direct
    c_sn = _fast_sn_chi2(SN, E, H0_km=100.0 * h)
    c_cmb = ccmb.chi2_compressed_cmb(omb, omc, h, _bridge_highz(E, Om=Om))
    c_rsd = rsd_chi2_lcdm(Om, s8)
    if not _finite(c_bao, c_sn, c_cmb, c_rsd): return -np.inf
    return -0.5 * (c_bao + c_sn + c_cmb + c_rsd)


def log_like_rp7(theta):
    Om, h, omb, s8, rd, beta, n = theta
    omc = Om * h * h - omb
    itp = _fast_E_quint('RP', beta, (n,))
    if itp is None: return -np.inf
    E = lambda z: float(itp(z))
    c_bao = df.chi2(_EWrap(E), rd)
    c_sn = _fast_sn_chi2(SN, E, H0_km=100.0 * h)
    c_cmb = ccmb.chi2_compressed_cmb(omb, omc, h, _bridge_highz(E, Om=Om))
    c_rsd = rsd_chi2_quint('RP', beta, (n,), s8)
    if not _finite(c_bao, c_sn, c_cmb, c_rsd): return -np.inf
    return -0.5 * (c_bao + c_sn + c_cmb + c_rsd)


def log_like_exp7(theta):
    Om, h, omb, s8, rd, beta, lam = theta
    omc = Om * h * h - omb
    itp = _fast_E_quint('exp', beta, (lam,))
    if itp is None: return -np.inf
    E = lambda z: float(itp(z))
    c_bao = df.chi2(_EWrap(E), rd)
    c_sn = _fast_sn_chi2(SN, E, H0_km=100.0 * h)
    c_cmb = ccmb.chi2_compressed_cmb(omb, omc, h, _bridge_highz(E, Om=Om))
    c_rsd = rsd_chi2_quint('exp', beta, (lam,), s8)
    if not _finite(c_bao, c_sn, c_cmb, c_rsd): return -np.inf
    return -0.5 * (c_bao + c_sn + c_cmb + c_rsd)


def log_post_factory(prior_fn, like_fn):
    def f(theta):
        lp = prior_fn(theta)
        if not np.isfinite(lp): return -np.inf
        ll = like_fn(theta)
        if not np.isfinite(ll): return -np.inf
        return lp + ll
    return f


def main():
    out_dir = os.path.join(HERE, 'chains')
    os.makedirs(out_dir, exist_ok=True)

    N_data = 13 + SN.N + 3 + N_RSD
    ln_N = float(np.log(N_data))

    print(f"\n[A2] N={N_data}  ln N={ln_N:.3f}")
    print(f"[A2] r_d prior flat [{RD_LO}, {RD_HI}] Mpc")

    # --- LCDM 5D ---
    print("\n[A2] Running LCDM (5D, r_d free) ...")
    labels = ['Om', 'h', 'omega_b', 'sigma_8_0', 'r_d']
    p0 = np.array([0.3129, 0.6781, 0.02237, 0.8095, 147.5])
    scale = np.array([0.003, 0.003, 0.00005, 0.005, 1.0])
    chain_l, logp_l, _ = m3.run_mcmc(
        log_post_factory(log_prior_lcdm5, log_like_lcdm5),
        p0, scale, labels, n_walkers=24, n_burn=300, n_sample=800)
    sum_l = m3.summarize(chain_l, logp_l, labels)
    np.save(os.path.join(out_dir, 'lcdm_rdfree_chain.npy'), chain_l)
    np.save(os.path.join(out_dir, 'lcdm_rdfree_logp.npy'), logp_l)

    # --- V_RP 7D ---
    print("\n[A2] Running V_RP (7D, r_d free) ...")
    labels_r = ['Om', 'h', 'omega_b', 'sigma_8_0', 'r_d', 'beta', 'n']
    p0 = np.array([0.322, 0.672, 0.02237, 0.8052, 147.5, 0.10, 0.10])
    scale = np.array([0.003, 0.003, 0.00005, 0.005, 1.0, 0.01, 0.02])
    chain_r, logp_r, _ = m3.run_mcmc(
        log_post_factory(log_prior_rp7, log_like_rp7),
        p0, scale, labels_r, n_walkers=24, n_burn=300, n_sample=700)
    sum_r = m3.summarize(chain_r, logp_r, labels_r)
    np.save(os.path.join(out_dir, 'vrp_rdfree_chain.npy'), chain_r)
    np.save(os.path.join(out_dir, 'vrp_rdfree_logp.npy'), logp_r)

    # --- V_exp 7D ---
    print("\n[A2] Running V_exp (7D, r_d free) ...")
    labels_e = ['Om', 'h', 'omega_b', 'sigma_8_0', 'r_d', 'beta', 'lam']
    p0 = np.array([0.322, 0.672, 0.02237, 0.8052, 147.5, 0.10, 0.15])
    scale = np.array([0.003, 0.003, 0.00005, 0.005, 1.0, 0.01, 0.02])
    chain_e, logp_e, _ = m3.run_mcmc(
        log_post_factory(log_prior_exp7, log_like_exp7),
        p0, scale, labels_e, n_walkers=24, n_burn=300, n_sample=700)
    sum_e = m3.summarize(chain_e, logp_e, labels_e)
    np.save(os.path.join(out_dir, 'vexp_rdfree_chain.npy'), chain_e)
    np.save(os.path.join(out_dir, 'vexp_rdfree_logp.npy'), logp_e)

    # --- AIC / BIC table ---
    def _aic(c, k): return c + 2 * k
    def _bic(c, k): return c + k * ln_N
    print(f"\n[A2] Model comparison (r_d free)")
    print(f"  {'model':<10}{'chi2_min':>12}{'k':>4}"
          f"{'AIC':>12}{'BIC':>12}{'dAIC':>10}{'dBIC':>10}")
    cL = sum_l['chi2_min']; kL = 5
    for name, c, k, s in (('LCDM', cL, kL, sum_l),
                          ('V_RP', sum_r['chi2_min'], 7, sum_r),
                          ('V_exp', sum_e['chi2_min'], 7, sum_e)):
        print(f"  {name:<10}{c:>12.2f}{k:>4}"
              f"{_aic(c,k):>12.2f}{_bic(c,k):>12.2f}"
              f"{_aic(c,k)-_aic(cL,kL):>+10.2f}"
              f"{_bic(c,k)-_bic(cL,kL):>+10.2f}")

    # --- r_d tension vs Planck (A3.1/A3.2) ---
    print("\n[A3] r_d tension vs Planck (147.09 +/- 0.30 Mpc)")
    PLANCK_RD = 147.09
    PLANCK_RD_SIG = 0.30
    for name, s, idx_rd in (('LCDM', sum_l, 4),
                            ('V_RP', sum_r, 4),
                            ('V_exp', sum_e, 4)):
        med = s['median'][idx_rd]
        lo = s['median'][idx_rd] - s['low'][idx_rd]
        hi = s['high'][idx_rd] - s['median'][idx_rd]
        sig_side = max(hi, lo)
        diff = med - PLANCK_RD
        sig_total = np.sqrt(sig_side**2 + PLANCK_RD_SIG**2)
        n_sig = diff / sig_total
        verdict = "within 3sigma" if abs(n_sig) < 3 else "TENSION > 3sigma"
        print(f"  {name:<8} r_d = {med:.2f} +{hi:.2f}/-{lo:.2f}  "
              f"delta = {diff:+.2f}  n_sigma = {n_sig:+.2f}  [{verdict}]")

    return sum_l, sum_r, sum_e


if __name__ == "__main__":
    main()
