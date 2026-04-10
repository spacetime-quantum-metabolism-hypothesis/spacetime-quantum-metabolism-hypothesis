# -*- coding: utf-8 -*-
"""
Phase 2 compressed CMB likelihood (Python, background-only).

We use three geometric CMB parameters that are robust to early-time physics
changes much smaller than Phase 2's coupling effects:

  theta_star  : 100 * theta* = 1.04110 +/- 0.00031  (Planck 2018 VI, Table 2)
  omega_b h^2 : 0.02237 +/- 0.00015                  (Planck 2018 VI)
  omega_c h^2 : 0.12000 +/- 0.00120                  (Planck 2018 VI)

Source: Planck Collaboration VI (arXiv:1807.06209), Table 2 "TT,TE,EE+lowE".

Correlations between (theta*, omega_b, omega_c) are small in the Planck
2018 TT,TE,EE+lowE chain (|rho| < 0.5) but non-zero. For Phase 2 scaffolding
we use an uncorrelated Gaussian prior; this slightly over-penalises. A full
covariance can be plugged in later by replacing COV_PLANCK18 below with the
3x3 matrix from the Planck 2018 base_plikHM_TTTEEE_lowl_lowE chain
(getdist -> cov).

theta* is computed as

    theta* = r_s(z*) / D_A_comoving(z*)

with z* from Hu & Sugiyama (1996) fitting formula, r_s via integrating the
baryon-photon sound speed, and D_A from the cosmological E(z).

NOTE: The sound horizon depends on the *pre-recombination* expansion,
which is standard LCDM for our Phase 2 models (SQMH coupling turns on only
after matter-radiation equality; phi is frozen in the radiation era per
Amendola attractor conditions). This is why theta* is a clean consistency
check and not double-counted with DESI BAO.
"""
import numpy as np
from scipy.integrate import quad

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import config


# --- Planck 2018 TT,TE,EE+lowE central values (1807.06209 Table 2) ---
THETA_STAR_OBS = 1.04110e-2       # 100*theta* = 1.04110
THETA_STAR_SIG_PLANCK = 0.00031e-2

# Hu & Sugiyama (1996) z_* fitting formula has ~0.3% theoretical precision
# vs modern CAMB-level Boltzmann, which dominates over the Planck measurement
# precision (3e-6) here. Add this as a floor theory error, else Phase 2 scan
# chases numerical fit-formula artefacts instead of physics.
THETA_STAR_SIG_THEORY = 0.003 * THETA_STAR_OBS
THETA_STAR_SIG = np.sqrt(THETA_STAR_SIG_PLANCK**2 + THETA_STAR_SIG_THEORY**2)

OMEGA_B_OBS = 0.02237
OMEGA_B_SIG = 0.00015

OMEGA_C_OBS = 0.12000
OMEGA_C_SIG = 0.00120


def _z_star(omega_b, omega_m):
    """Hu & Sugiyama 1996 fitting formula for z_*, eq. E-1."""
    g1 = 0.0783 * omega_b**(-0.238) / (1.0 + 39.5 * omega_b**0.763)
    g2 = 0.560 / (1.0 + 21.1 * omega_b**1.81)
    return 1048.0 * (1.0 + 0.00124 * omega_b**(-0.738)) * \
        (1.0 + g1 * omega_m**g2)


def sound_horizon_comoving(omega_b, omega_c, h, z_star):
    """
    Comoving sound horizon at z_star in Mpc.
    r_s = integral_0^{1/(1+z_*)} da c_s / (a^2 H(a))
    with c_s = 1/sqrt(3*(1 + R)), R = 3*omega_b / (4*omega_gamma*(1+z)^-1)
    i.e. R(a) = (3 omega_b / 4 omega_gamma) * a.

    omega_gamma fixed by T_CMB = 2.7255 K:
      omega_gamma = 2.4728e-5
    Neutrinos: N_eff = 3.046, T_nu/T_gamma = (4/11)^(1/3).
    """
    omega_gamma = 2.4728e-5
    omega_nu = 3.046 * (7.0 / 8.0) * (4.0 / 11.0)**(4.0 / 3.0) * omega_gamma
    omega_r = omega_gamma + omega_nu
    omega_m = omega_b + omega_c

    # H(a) in km/s/Mpc during radiation+matter era (DE negligible at z~1100)
    # E^2(a) = (omega_r/a^4 + omega_m/a^3 + omega_de) / h^2
    omega_de = h*h - omega_m - omega_r  # flat universe

    def integrand(a):
        R = 3.0 * omega_b / (4.0 * omega_gamma) * a
        c_s = 1.0 / np.sqrt(3.0 * (1.0 + R))
        H2 = (omega_r / a**4 + omega_m / a**3 + omega_de) * (100.0)**2
        # c_s * c / (a^2 H), using c in km/s
        return config.c * 1e-3 * c_s / (a * a * np.sqrt(H2))

    a_star = 1.0 / (1.0 + z_star)
    r_s, _ = quad(integrand, 1e-8, a_star, limit=200, epsabs=1e-4)
    return r_s  # Mpc


def comoving_distance(z, E_func):
    """Comoving distance to z using arbitrary E(z) interpolator (dimensionless).
    Returns Mpc."""
    c_km = config.c * 1e-3
    H0 = getattr(config, 'H_0_km', 67.36)
    integrand = lambda zp: 1.0 / E_func(zp)
    val, _ = quad(integrand, 0.0, z, limit=200, epsabs=1e-4)
    return c_km / H0 * val


def theta_star(omega_b, omega_c, h, E_func):
    """Compute compressed CMB angular scale theta_star (dimensionless)."""
    omega_m = omega_b + omega_c
    zs = _z_star(omega_b, omega_m)
    r_s = sound_horizon_comoving(omega_b, omega_c, h, zs)
    # Comoving angular diameter distance at z_star uses E(z) at high-z.
    D_A_c = comoving_distance(zs, E_func)
    return r_s / D_A_c


def chi2_compressed_cmb(omega_b, omega_c, h, E_func):
    """
    Returns chi^2 against Planck 2018 TT,TE,EE+lowE compressed prior on
    (theta*, omega_b, omega_c). Diagonal approximation.
    """
    th = theta_star(omega_b, omega_c, h, E_func)
    chi2 = ((th - THETA_STAR_OBS) / THETA_STAR_SIG)**2
    chi2 += ((omega_b - OMEGA_B_OBS) / OMEGA_B_SIG)**2
    chi2 += ((omega_c - OMEGA_C_OBS) / OMEGA_C_SIG)**2
    return chi2


if __name__ == "__main__":
    # Quick LCDM sanity check — should give chi^2 ~ 0.
    h = 0.6736
    omega_b = 0.02237
    omega_c = 0.12000
    omega_m = omega_b + omega_c
    Om_m_frac = omega_m / h**2

    def E_lcdm(z):
        omega_r = 2.4728e-5 * (1.0 + 3.046 * (7/8) * (4/11)**(4/3)) / h**2
        return np.sqrt(omega_r * (1 + z)**4
                       + Om_m_frac * (1 + z)**3
                       + (1 - Om_m_frac - omega_r))

    th = theta_star(omega_b, omega_c, h, E_lcdm)
    print(f"LCDM theta* = {100*th:.5f} (target 1.04110)")
    chi2 = chi2_compressed_cmb(omega_b, omega_c, h, E_lcdm)
    print(f"LCDM chi2 compressed CMB = {chi2:.3f}")
