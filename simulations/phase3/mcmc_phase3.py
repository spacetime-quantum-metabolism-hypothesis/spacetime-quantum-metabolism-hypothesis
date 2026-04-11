# -*- coding: utf-8 -*-
"""
Phase 3 — Python-only MCMC marginalisation of Phase 2 likelihood.

Scope (realistic single-session Phase 3):
  - emcee sampler over Phase 2 joint likelihood (BAO + SN + compressed CMB + RSD)
  - Marginalise nuisances that Phase 2 had fixed:
      Omega_m, h, omega_b (BBN prior), sigma_8_0 (Planck prior), r_d (EH98 derived)
  - Two models:
      LCDM    : theta = (Om, h, omega_b, sigma_8_0)          k=4
      V_RP    : theta = (Om, h, omega_b, sigma_8_0, beta, n) k=6
  - Output: chains, posterior summaries, corner plot.
  - BOSS DR12 3x3 consensus covariance added to RSD likelihood.

Scope EXCLUDED (Phase 4+):
  - Full CLASS Boltzmann code (TT/EE/lensing)
  - Planck full likelihood (clik)
  - Fluid perturbation module for Fluid IDE
  - Cobaya/MontePython wrappers
"""
import os
import sys
import time
# Lock matplotlib to Agg before any package (corner, emcee utilities) can
# import pyplot and pin a GUI backend — headless runs otherwise fail.
import matplotlib
matplotlib.use('Agg')
import numpy as np
import emcee

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))           # simulations/
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'phase2'))

import config
import desi_fitting as df
import compressed_cmb as ccmb
import sn_likelihood as snl
import quintessence_perturb as qp
import quintessence as qn


# Fast SN chi2: reduce integration grid from 3000 to 500 points.
# Accuracy loss at z<1.3 well below stat precision (1/N_grid^2 ~ 4e-6).
def _fast_sn_chi2(sn, E_func, H0_km=67.36):
    c_km = config.c * 1e-3
    zs = sn.z_hd
    z_grid = np.linspace(0.0, zs.max() * 1.01, 500)
    inv_E = np.array([1.0 / E_func(z) for z in z_grid])
    cum = np.concatenate(([0.0],
                          np.cumsum(0.5 * (inv_E[:-1] + inv_E[1:])
                                    * np.diff(z_grid))))
    D_C = np.interp(zs, z_grid, cum) * (c_km / H0_km)
    D_L = (1.0 + sn.z_hel) * D_C
    mu_th = 5.0 * np.log10(D_L) + 25.0
    delta = sn.mu_obs - mu_th
    Cinv_d = sn.cov_inv @ delta
    A = float(delta @ Cinv_d)
    B = float(np.ones(sn.N) @ Cinv_d)
    return A - (B * B) / sn._one_Cinv_1


# ---------------------------------------------------------------
# Cached Phase 2 data loaders
# ---------------------------------------------------------------
SN = snl.DESY5SN()
print(f"[Phase 3] Loaded {SN.N} DESY5 SNe")


# ---------------------------------------------------------------
# RSD: 8 points + BOSS DR12 off-diagonal block (Alam+ 2017 consensus)
# ---------------------------------------------------------------
# (z, fsigma8, sigma) — same 8 points as Phase 2
Z_RSD = np.array([0.067, 0.15, 0.38, 0.51, 0.61, 0.70, 0.85, 1.48])
FS8_OBS = np.array([0.423, 0.490, 0.497, 0.458, 0.436, 0.473, 0.315, 0.462])
FS8_ERR = np.array([0.055, 0.145, 0.045, 0.038, 0.034, 0.044, 0.095, 0.045])

# Build diagonal first, then overwrite BOSS DR12 block [idx 2,3,4]
RSD_COV = np.diag(FS8_ERR**2)

# Alam+ 2017 BOSS DR12 fsigma8 consensus correlation matrix
# (rough consensus from eq 28 of 1607.03155, rounded):
#   rho(0.38, 0.51) = 0.24
#   rho(0.38, 0.61) = 0.10
#   rho(0.51, 0.61) = 0.26
_BOSS_IDX = (2, 3, 4)
_BOSS_RHO = np.array([
    [1.00, 0.24, 0.10],
    [0.24, 1.00, 0.26],
    [0.10, 0.26, 1.00],
])
# Sanity checks: Z_RSD must be ascending, and _BOSS_IDX must point at the
# three BOSS DR12 redshifts (z=0.38, 0.51, 0.61). Any reorder of Z_RSD would
# otherwise silently drop the consensus correlation onto the wrong bins.
assert np.all(np.diff(Z_RSD) > 0), "Z_RSD must be strictly ascending"
_BOSS_Z_EXPECTED = (0.38, 0.51, 0.61)
for _k, _idx in enumerate(_BOSS_IDX):
    assert abs(Z_RSD[_idx] - _BOSS_Z_EXPECTED[_k]) < 1e-6, (
        f"BOSS DR12 index {_idx} expected z={_BOSS_Z_EXPECTED[_k]}, "
        f"got z={Z_RSD[_idx]}")

# Drift guard: Phase 2 rsd_likelihood.py holds the authoritative table.
# If either side is edited without the other, raise here rather than
# letting the two chi2 definitions silently disagree.
import rsd_likelihood as _rsd_p2
assert np.allclose(Z_RSD, _rsd_p2.Z_RSD), "Phase2/3 Z_RSD drift"
assert np.allclose(FS8_OBS, _rsd_p2.FS8_OBS), "Phase2/3 FS8_OBS drift"
assert np.allclose(FS8_ERR, _rsd_p2.FS8_SIG), "Phase2/3 FS8_ERR drift"
del _rsd_p2

_sigs_boss = FS8_ERR[list(_BOSS_IDX)]
_cov_boss = _BOSS_RHO * np.outer(_sigs_boss, _sigs_boss)
for i_loc, i_glob in enumerate(_BOSS_IDX):
    for j_loc, j_glob in enumerate(_BOSS_IDX):
        RSD_COV[i_glob, j_glob] = _cov_boss[i_loc, j_loc]

RSD_COV_INV = np.linalg.inv(RSD_COV)
N_RSD = len(Z_RSD)


def rsd_chi2_lcdm(Om, sigma_8_0):
    """LCDM fs8(z) chi2 with BOSS DR12 full-cov block."""
    from scipy.integrate import solve_ivp
    from scipy.interpolate import interp1d
    Or = config.Omega_r
    OL = 1.0 - Om - Or

    def E2(N):
        a = np.exp(N)
        return Om * a**(-3) + Or * a**(-4) + OL

    def Om_frac(N):
        a = np.exp(N)
        return Om * a**(-3) / E2(N)

    def ENE(N):
        a = np.exp(N)
        e2 = E2(N)
        de2 = -3.0 * Om * a**(-3) - 4.0 * Or * a**(-4)
        return 0.5 * de2 / e2

    def rhs(N, y):
        d, dN = y
        return [dN, -(2.0 + ENE(N)) * dN + 1.5 * Om_frac(N) * d]

    N_grid = np.linspace(-3.0, 0.0, 200)
    sol = solve_ivp(rhs, [-3.0, 0.0], [np.exp(-3.0), np.exp(-3.0)],
                    t_eval=N_grid, rtol=1e-8, atol=1e-10, method='DOP853')
    if not sol.success:
        return np.nan
    D_raw = sol.y[0].copy()
    DN_raw = sol.y[1].copy()
    f = DN_raw / D_raw
    D = D_raw / D_raw[-1]
    z_arr = np.exp(-N_grid) - 1.0
    fs8 = f * sigma_8_0 * D
    idx = np.argsort(z_arr)
    itp = interp1d(z_arr[idx], fs8[idx], kind='cubic',
                   bounds_error=False,
                   fill_value=(fs8[idx][0], fs8[idx][-1]))
    fs8_th = np.array([float(itp(z)) for z in Z_RSD])
    delta = FS8_OBS - fs8_th
    return float(delta @ RSD_COV_INV @ delta)


def rsd_chi2_quint(V_family, beta, extra, sigma_8_0):
    """Coupled quintessence fs8 chi2 with BOSS full-cov."""
    res = qp.growth_factor(V_family, beta, extra,
                           N_ini=-3.0, N_end=0.0, n_pts=200)
    if res is None:
        return np.nan
    a_arr, D_arr, f_arr = res
    z_arr = 1.0 / a_arr - 1.0
    fs8 = f_arr * sigma_8_0 * D_arr
    from scipy.interpolate import interp1d
    idx = np.argsort(z_arr)
    itp = interp1d(z_arr[idx], fs8[idx], kind='cubic',
                   bounds_error=False,
                   fill_value=(fs8[idx][0], fs8[idx][-1]))
    fs8_th = np.array([float(itp(z)) for z in Z_RSD])
    delta = FS8_OBS - fs8_th
    return float(delta @ RSD_COV_INV @ delta)


# ---------------------------------------------------------------
# r_d from Eisenstein-Hu 1998 z_drag + sound horizon integral
# ---------------------------------------------------------------
def r_d_EH98(omega_b, omega_c, h):
    """Comoving sound horizon at drag epoch (Mpc).

    Uses EH98 (astro-ph/9709112) fitting formula for z_drag, then the
    existing Phase 2 sound horizon integral from ccmb.sound_horizon_comoving.
    """
    omega_m = omega_b + omega_c
    b1 = 0.313 * omega_m**(-0.419) * (1.0 + 0.607 * omega_m**0.674)
    b2 = 0.238 * omega_m**0.223
    z_d = (1291.0 * omega_m**0.251 / (1.0 + 0.659 * omega_m**0.828)
           * (1.0 + b1 * omega_b**b2))
    return ccmb.sound_horizon_comoving(omega_b, omega_c, h, z_d)


# ---------------------------------------------------------------
# E(z) helpers
# ---------------------------------------------------------------
def E_lcdm_factory(Om):
    Or = config.Omega_r
    OL = 1.0 - Om - Or

    def E(z):
        a = 1.0 / (1.0 + z)
        return float(np.sqrt(Om * (1.0 + z)**3 + Or * (1.0 + z)**4 + OL))
    return E


def _bridge_highz(E_low, zcut=2.5, Om=None, Or=None):
    """Wrap low-z coupled E(z) with PURE LCDM high-z tail for CMB integral.

    SQMH coupling Q ~ rho_DE*rho_m/H vanishes when Omega_DE/Omega_m << 1
    (z > 2.5), so the high-z tail is guaranteed to be LCDM with the same
    Om_m at ~0.1% precision. We do NOT rescale by e_low/e_hi at the junction
    because the Phase 1 backward scalar-field ODE drifts to phi_N -> sqrt(6)
    (phantom boundary) for large n/beta and returns unreliable E(z) near
    z_cut. Using the pure analytic LCDM tail disconnects the CMB integral
    from that unstable region; any small discontinuity at z_cut is quadrature
    -integrated harmlessly by scipy.quad.
    """
    if Om is None:
        Om = config.Omega_m
    if Or is None:
        Or = config.Omega_r
    OL = 1.0 - Om - Or

    def E_hi(z):
        return float(np.sqrt(Or * (1 + z)**4 + Om * (1 + z)**3 + OL))

    def wrapped(z, *args):
        if z <= zcut:
            return float(E_low(z))
        return E_hi(z)
    return wrapped


class _EWrap:
    """Bare E(z) → E(z, *args) for df.chi2 callers."""
    def __init__(self, f):
        self._f = f

    def __call__(self, z, *args):
        return float(self._f(z))


# ---------------------------------------------------------------
# Priors
# ---------------------------------------------------------------
PRIORS_LCDM = {
    'Om': (0.20, 0.45),          # flat
    'h':  (0.55, 0.80),          # flat
    'omega_b': (0.02237, 0.00015),   # Gaussian (BBN-like)
    'sigma_8_0': (0.8111, 0.02),     # Gaussian (Planck prior)
}
PRIORS_RP = {
    **PRIORS_LCDM,
    'beta': (0.0, 1.0),          # flat, SQMH positive
    'n':    (0.05, 3.0),         # flat
}
PRIORS_EXP = {
    **PRIORS_LCDM,
    'beta':  (0.0, 1.0),         # flat, SQMH positive
    'lam':   (0.05, 3.0),        # flat (Ferreira-Joyce tracker range)
}


def log_prior_lcdm(theta):
    Om, h, omb, s8 = theta
    if not (0.20 < Om < 0.45):
        return -np.inf
    if not (0.55 < h < 0.80):
        return -np.inf
    lp = -0.5 * ((omb - 0.02237) / 0.00015)**2
    lp += -0.5 * ((s8 - 0.8111) / 0.02)**2
    # derived omega_c must be positive and within plausible band
    omc = Om * h * h - omb
    if not (0.05 < omc < 0.20):
        return -np.inf
    return lp


def log_prior_rp(theta):
    Om, h, omb, s8, beta, n = theta
    base = log_prior_lcdm((Om, h, omb, s8))
    if not np.isfinite(base):
        return -np.inf
    if not (0.0 <= beta < 1.0):
        return -np.inf
    if not (0.05 < n < 3.0):
        return -np.inf
    return base


def log_prior_exp(theta):
    Om, h, omb, s8, beta, lam = theta
    base = log_prior_lcdm((Om, h, omb, s8))
    if not np.isfinite(base):
        return -np.inf
    if not (0.0 <= beta < 1.0):
        return -np.inf
    if not (0.05 < lam < 3.0):
        return -np.inf
    return base


# ---------------------------------------------------------------
# Likelihood
# ---------------------------------------------------------------
def _finite(*vals):
    """Return True iff every chi2 component is a finite real number.

    NOTE: prefer this over replacing None/nan with a large sentinel (e.g. 1e6).
    Summing a sentinel into tot gives log-post ~ -5e5 rather than -inf, and
    emcee walkers can get stuck in that deep-but-finite basin instead of
    cleanly rejecting the proposal.
    """
    for v in vals:
        if v is None:
            return False
        if not np.isfinite(v):
            return False
    return True


def log_like_lcdm(theta):
    Om, h, omb, s8 = theta
    omc = Om * h * h - omb
    E = E_lcdm_factory(Om)

    c_bao = df.chi2(_EWrap(E), r_d_EH98(omb, omc, h))
    c_sn = _fast_sn_chi2(SN, E, H0_km=100.0 * h)
    c_cmb = ccmb.chi2_compressed_cmb(omb, omc, h, _bridge_highz(E, Om=Om))
    c_rsd = rsd_chi2_lcdm(Om, s8)
    if not _finite(c_bao, c_sn, c_cmb, c_rsd):
        return -np.inf
    return -0.5 * (c_bao + c_sn + c_cmb + c_rsd)


def _fast_E_quint(family, beta, extra):
    """Thin wrapper: integrate with n_steps=250 (MCMC accuracy)."""
    res = qn.integrate_quintessence(family, beta, extra, n_steps=250)
    if res is None:
        return None
    z_arr, E_arr, _ = res
    from scipy.interpolate import interp1d
    return interp1d(z_arr, E_arr, kind='cubic',
                    bounds_error=False,
                    fill_value=(E_arr[0], E_arr[-1]))


def log_like_rp(theta):
    Om, h, omb, s8, beta, n = theta
    omc = Om * h * h - omb
    itp = _fast_E_quint('RP', beta, (n,))
    if itp is None:
        return -np.inf
    E = lambda z: float(itp(z))
    c_bao = df.chi2(_EWrap(E), r_d_EH98(omb, omc, h))
    c_sn = _fast_sn_chi2(SN, E, H0_km=100.0 * h)
    c_cmb = ccmb.chi2_compressed_cmb(omb, omc, h, _bridge_highz(E, Om=Om))
    c_rsd = rsd_chi2_quint('RP', beta, (n,), s8)
    if not _finite(c_bao, c_sn, c_cmb, c_rsd):
        return -np.inf
    return -0.5 * (c_bao + c_sn + c_cmb + c_rsd)


def log_like_exp(theta):
    Om, h, omb, s8, beta, lam = theta
    omc = Om * h * h - omb
    itp = _fast_E_quint('exp', beta, (lam,))
    if itp is None:
        return -np.inf
    E = lambda z: float(itp(z))
    c_bao = df.chi2(_EWrap(E), r_d_EH98(omb, omc, h))
    c_sn = _fast_sn_chi2(SN, E, H0_km=100.0 * h)
    c_cmb = ccmb.chi2_compressed_cmb(omb, omc, h, _bridge_highz(E, Om=Om))
    c_rsd = rsd_chi2_quint('exp', beta, (lam,), s8)
    if not _finite(c_bao, c_sn, c_cmb, c_rsd):
        return -np.inf
    return -0.5 * (c_bao + c_sn + c_cmb + c_rsd)


def log_post_lcdm(theta):
    lp = log_prior_lcdm(theta)
    if not np.isfinite(lp):
        return -np.inf
    ll = log_like_lcdm(theta)
    if not np.isfinite(ll):
        return -np.inf
    return lp + ll


def log_post_rp(theta):
    lp = log_prior_rp(theta)
    if not np.isfinite(lp):
        return -np.inf
    ll = log_like_rp(theta)
    if not np.isfinite(ll):
        return -np.inf
    return lp + ll


def log_post_exp(theta):
    lp = log_prior_exp(theta)
    if not np.isfinite(lp):
        return -np.inf
    ll = log_like_exp(theta)
    if not np.isfinite(ll):
        return -np.inf
    return lp + ll


# ---------------------------------------------------------------
# MCMC drivers
# ---------------------------------------------------------------
def run_mcmc(log_post, p0_center, p0_scale, labels,
             n_walkers=24, n_burn=200, n_sample=800):
    ndim = len(p0_center)
    # Seed both the local generator (walker init) AND numpy's global RNG —
    # emcee's stretch move samples through np.random.*, so without the
    # global seed the chain is not reproducible across runs.
    rng = np.random.default_rng(42)
    np.random.seed(42)
    p0 = p0_center + p0_scale * rng.standard_normal((n_walkers, ndim))
    sampler = emcee.EnsembleSampler(n_walkers, ndim, log_post)
    t0 = time.time()
    print(f"  [MCMC] burn-in {n_burn} steps x {n_walkers} walkers...")
    state = sampler.run_mcmc(p0, n_burn, progress=False)
    sampler.reset()
    print(f"  [MCMC] sampling {n_sample} steps...")
    sampler.run_mcmc(state, n_sample, progress=False)
    dt = time.time() - t0
    chain = sampler.get_chain(flat=True)
    logp = sampler.get_log_prob(flat=True)
    tau = None
    try:
        tau = sampler.get_autocorr_time(tol=0)
    except Exception:
        pass
    print(f"  [MCMC] done in {dt:.1f}s, "
          f"acceptance={np.mean(sampler.acceptance_fraction):.2f}, "
          f"tau={tau}")
    return chain, logp, labels


def summarize(chain, logp, labels):
    med = np.median(chain, axis=0)
    lo = np.percentile(chain, 16, axis=0)
    hi = np.percentile(chain, 84, axis=0)
    print(f"  {'param':<12}{'median':>10}{'-1sig':>10}{'+1sig':>10}")
    for lab, m, l, h in zip(labels, med, lo, hi):
        print(f"  {lab:<12}{m:>10.4f}{(m-l):>10.4f}{(h-m):>10.4f}")
    # Best fit (max log-post)
    imax = int(np.argmax(logp))
    chi2_min = -2.0 * logp[imax]
    print(f"  best chi2 = {chi2_min:.2f} at theta = {chain[imax]}")
    return {'median': med, 'low': lo, 'high': hi,
            'best': chain[imax], 'chi2_min': chi2_min}


def main():
    out_dir = os.path.join(HERE, 'chains')
    os.makedirs(out_dir, exist_ok=True)

    labels_lcdm = ['Om', 'h', 'omega_b', 'sigma_8_0']
    lcdm_c = os.path.join(out_dir, 'lcdm_chain.npy')
    lcdm_p = os.path.join(out_dir, 'lcdm_logp.npy')
    if os.path.exists(lcdm_c) and os.path.exists(lcdm_p):
        print("\n[Phase 3] Loading cached LCDM chain ...")
        chain_l = np.load(lcdm_c); logp_l = np.load(lcdm_p)
    else:
        print("\n[Phase 3] Running LCDM MCMC ...")
        p0 = np.array([0.320, 0.673, 0.02237, 0.8111])
        scale = np.array([0.005, 0.005, 0.00005, 0.005])
        chain_l, logp_l, _ = run_mcmc(log_post_lcdm, p0, scale, labels_lcdm,
                                       n_walkers=20, n_burn=200, n_sample=700)
        np.save(lcdm_c, chain_l); np.save(lcdm_p, logp_l)
    summary_l = summarize(chain_l, logp_l, labels_lcdm)

    labels_rp = ['Om', 'h', 'omega_b', 'sigma_8_0', 'beta', 'n']
    vrp_c = os.path.join(out_dir, 'vrp_chain.npy')
    vrp_p = os.path.join(out_dir, 'vrp_logp.npy')
    if os.path.exists(vrp_c) and os.path.exists(vrp_p):
        print("\n[Phase 3] Loading cached V_RP chain ...")
        chain_r = np.load(vrp_c); logp_r = np.load(vrp_p)
    else:
        print("\n[Phase 3] Running V_RP MCMC ...")
        p0 = np.array([0.320, 0.673, 0.02237, 0.8111, 0.097, 0.113])
        scale = np.array([0.005, 0.005, 0.00005, 0.005, 0.01, 0.02])
        chain_r, logp_r, _ = run_mcmc(log_post_rp, p0, scale, labels_rp,
                                       n_walkers=20, n_burn=200, n_sample=600)
        np.save(vrp_c, chain_r); np.save(vrp_p, logp_r)
    summary_r = summarize(chain_r, logp_r, labels_rp)

    print("\n[Phase 3] Running V_exp MCMC ...")
    labels_exp = ['Om', 'h', 'omega_b', 'sigma_8_0', 'beta', 'lam']
    p0 = np.array([0.320, 0.673, 0.02237, 0.8111, 0.100, 0.150])
    scale = np.array([0.005, 0.005, 0.00005, 0.005, 0.01, 0.02])
    chain_e, logp_e, _ = run_mcmc(log_post_exp, p0, scale, labels_exp,
                                   n_walkers=20, n_burn=200, n_sample=600)
    summary_e = summarize(chain_e, logp_e, labels_exp)
    np.save(os.path.join(out_dir, 'vexp_chain.npy'), chain_e)
    np.save(os.path.join(out_dir, 'vexp_logp.npy'), logp_e)

    # Delta chi2 / AIC / BIC
    N_tot = 13 + SN.N + 3 + N_RSD
    ln_N = float(np.log(N_tot))
    chi2_L = summary_l['chi2_min']; k_L = 4
    chi2_R = summary_r['chi2_min']; k_R = 6
    chi2_E = summary_e['chi2_min']; k_E = 6
    def _aic(c, k): return c + 2 * k
    def _bic(c, k): return c + k * ln_N
    print(f"\n[Phase 3] N = {N_tot}  (ln N = {ln_N:.3f})")
    print(f"  {'model':<8}{'chi2_min':>12}{'k':>4}"
          f"{'AIC':>12}{'BIC':>12}{'dAIC':>10}{'dBIC':>10}")
    for name, c, k in (('LCDM', chi2_L, k_L),
                       ('V_RP', chi2_R, k_R),
                       ('V_exp', chi2_E, k_E)):
        print(f"  {name:<8}{c:>12.2f}{k:>4}"
              f"{_aic(c,k):>12.2f}{_bic(c,k):>12.2f}"
              f"{_aic(c,k)-_aic(chi2_L,k_L):>+10.2f}"
              f"{_bic(c,k)-_bic(chi2_L,k_L):>+10.2f}")

    # Corner plots
    try:
        import corner
        import matplotlib.pyplot as plt
        fig_dir = os.path.abspath(os.path.join(HERE, '..', '..', 'figures'))
        os.makedirs(fig_dir, exist_ok=True)

        fig = corner.corner(chain_r, labels=labels_rp,
                            show_titles=True, title_fmt='.3f',
                            quantiles=[0.16, 0.5, 0.84])
        fig.suptitle('Phase 3 MCMC — V_RP posterior\n'
                     'BAO+SN+compressed CMB+RSD(BOSS DR12 cov)',
                     fontsize=12, y=1.02)
        out_fig = os.path.join(fig_dir, '13_phase3_mcmc.png')
        fig.savefig(out_fig, dpi=150, bbox_inches='tight')
        plt.close(fig)
        print(f"[Phase 3] Figure saved: {out_fig}")

        fig = corner.corner(chain_e, labels=labels_exp,
                            show_titles=True, title_fmt='.3f',
                            quantiles=[0.16, 0.5, 0.84])
        fig.suptitle('Phase 3 MCMC — V_exp posterior\n'
                     'BAO+SN+compressed CMB+RSD(BOSS DR12 cov)',
                     fontsize=12, y=1.02)
        out_fig = os.path.join(fig_dir, '14_phase3_vexp.png')
        fig.savefig(out_fig, dpi=150, bbox_inches='tight')
        plt.close(fig)
        print(f"[Phase 3] Figure saved: {out_fig}")
    except Exception as e:
        print(f"[Phase 3] Corner plot failed: {e}")

    return summary_l, summary_r, summary_e


if __name__ == "__main__":
    main()
