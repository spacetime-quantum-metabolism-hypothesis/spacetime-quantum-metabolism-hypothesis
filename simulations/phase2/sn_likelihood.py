# -*- coding: utf-8 -*-
"""
DESY5 supernova likelihood (distance modulus, no growth needed).

Data source: https://github.com/CobayaSampler/sn_data/tree/master/DESY5
  DES-SN5YR_HD.csv   : 1829 SNe (CID, IDSURVEY, zCMB, zHD, zHEL, MU, MUERR_FINAL)
  covsys_000.txt     : systematic covariance (flat list, first line N=1829)

Likelihood: marginalized over the absolute magnitude offset M (Conley et al.
2011, Appendix B) so H_0 decouples from the fit and only the shape of mu(z)
matters. This mirrors the DESY5 cosmomc module.
"""
import os
import numpy as np
from scipy.integrate import quad

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import config

_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def _load_hd():
    path = os.path.join(_DATA_DIR, 'DES-SN5YR_HD.csv')
    dat = np.genfromtxt(path, delimiter=',', names=True, skip_header=0)
    # DESY5 / CobayaSampler convention: integrate distance with zHD (CMB
    # frame, peculiar-velocity corrected), apply (1+zHEL) luminosity factor
    # with the heliocentric redshift. Using zCMB here introduces a ~0.001
    # low-z bias relative to the official likelihood.
    z_hd = dat['zHD']
    z_hel = dat['zHEL']
    mu_obs = dat['MU']
    mu_err = dat['MUERR_FINAL']
    return z_hd, z_hel, mu_obs, mu_err


def _load_covsys(N):
    path = os.path.join(_DATA_DIR, 'DESY5_covsys.txt')
    with open(path, 'r') as f:
        first = int(f.readline().strip())
        assert first == N, f"covsys header N={first} != data N={N}"
        vals = np.fromfile(f, sep='\n', count=N * N)
    if vals.size != N * N:
        raise ValueError(
            f"DESY5 covsys truncated: got {vals.size} values, expected "
            f"{N * N}. File {path} may be incomplete."
        )
    return vals.reshape(N, N)


class DESY5SN:
    """Holds the DESY5 SN data + cached covariance inverse."""

    def __init__(self):
        self.z_hd, self.z_hel, self.mu_obs, self.mu_err = _load_hd()
        self.N = len(self.z_hd)
        cov_sys = _load_covsys(self.N)
        self.cov = cov_sys + np.diag(self.mu_err**2)
        self.cov_inv = np.linalg.inv(self.cov)
        # Pre-compute sums for analytic marginalisation over absolute mag.
        ones = np.ones(self.N)
        self._C_inv_1 = self.cov_inv @ ones
        self._one_Cinv_1 = float(ones @ self._C_inv_1)

    def chi2(self, E_func, H0_km=67.36):
        """
        Distance-modulus chi^2, marginalized over absolute magnitude offset.

        mu_theory(z) = 5 log10(d_L / 10 pc)
                     = 5 log10( (1+z_hel) * D_M_Mpc ) + 25
          D_M = c/H0 * integral_0^z_hd dz' / E(z')
        """
        c_km = config.c * 1e-3
        # Comoving distance at each zHD (CMB + peculiar-velocity frame)
        zs = self.z_hd
        # Simple trapezoidal integration on a shared grid for efficiency.
        z_grid = np.linspace(0.0, zs.max() * 1.01, 3000)
        inv_E = np.array([1.0 / E_func(z) for z in z_grid])
        cum = np.concatenate(([0.0],
                              np.cumsum(0.5 * (inv_E[:-1] + inv_E[1:])
                                        * np.diff(z_grid))))
        D_C = np.interp(zs, z_grid, cum) * (c_km / H0_km)   # Mpc
        D_L = (1.0 + self.z_hel) * D_C                      # luminosity dist
        mu_th = 5.0 * np.log10(D_L) + 25.0

        delta = self.mu_obs - mu_th
        # Marginalised chi^2:
        #   chi^2 = d^T Cinv d - (1^T Cinv d)^2 / (1^T Cinv 1)
        # (Goliath et al. 2001; Conley+ 2011)
        Cinv_d = self.cov_inv @ delta
        A = float(delta @ Cinv_d)
        B = float(np.ones(self.N) @ Cinv_d)
        return A - (B * B) / self._one_Cinv_1


if __name__ == "__main__":
    print("DESY5 SN sanity check")
    sn = DESY5SN()
    print(f"  Loaded {sn.N} SNe, zHD range = [{sn.z_hd.min():.3f}, "
          f"{sn.z_hd.max():.3f}]")

    # LCDM check
    Om = 0.315

    def E_lcdm(z):
        return np.sqrt(Om * (1 + z)**3 + (1 - Om))

    chi2 = sn.chi2(E_lcdm)
    print(f"  LCDM (Om={Om}) chi2 = {chi2:.2f} "
          f"(dof ~ {sn.N - 1}; reduced ~ {chi2 / (sn.N - 1):.3f})")
