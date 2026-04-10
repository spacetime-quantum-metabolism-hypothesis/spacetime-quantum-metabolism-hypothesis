# -*- coding: utf-8 -*-
"""
Phase 2 RSD (redshift-space distortion) f*sigma_8 likelihood.

Purpose
-------
Test whether SQMH coupled-quintessence growth enhancement (G_eff/G = 1+2beta^2)
is compatible with f*sigma_8(z) measurements from galaxy redshift surveys.

Data compilation (SCAFFOLDING — 8 well-established fs8 points)
-------------------------------------------------------------
Sources (all 1-sigma errors, diagonal covariance approximation):

  z      fsigma8   sigma    Survey                  Reference
  0.067  0.423     0.055    6dFGS                   Beutler+ 2012 (1204.4725)
  0.15   0.490     0.145    SDSS MGS                Howlett+ 2015 (1409.3238)
  0.38   0.497     0.045    BOSS DR12 LOWZ          Alam+   2017 (1607.03155)
  0.51   0.458     0.038    BOSS DR12 CMASS1        Alam+   2017 (1607.03155)
  0.61   0.436     0.034    BOSS DR12 CMASS2        Alam+   2017 (1607.03155)
  0.70   0.473     0.044    eBOSS DR16 LRG          Bautista+2021 (2007.08993)
  0.85   0.315     0.095    eBOSS DR16 ELG          de Mattia+2021 (2007.09008)
  1.48   0.462     0.045    eBOSS DR16 QSO          Hou+     2021 (2007.08998)

Notes
-----
1. BOSS DR12 three points (0.38/0.51/0.61) have off-diagonal correlations
   ~0.2-0.4 in the published consensus covariance. Ignoring them is a
   ~10% underestimate of the effective chi^2 penalty. Phase 2 scaffolding.
2. DESI DR1/DR2 full-shape RSD is preferred (consistent with our BAO data
   source) but the public likelihood is not plumbed here yet. Replace this
   module with the Cobaya `desi_2024_fs` block when Phase 3 materializes.
3. sigma_8(z=0) is taken from Planck 2018 TT,TE,EE+lowE+lensing
   central value: sigma_8_0 = 0.8111 (Planck VI Table 2).
   This is held fixed (not marginalized). A Gaussian shift prior could
   loosen the bound by ~10% but would not reverse the verdict.
4. Theory fs8(z) = f(z) * sigma_8(z) = f(z) * sigma_8_0 * D(z)/D(0)
   where D(z) is from coupled quintessence growth (quintessence_perturb).
   For LCDM and Fluid IDE (no scalar field): use standard LCDM growth.
"""
import numpy as np
from scipy.interpolate import interp1d

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import config
import quintessence_perturb as qp


SIGMA_8_0 = 0.8111  # Planck 2018 TT,TE,EE+lowE+lensing, arXiv:1807.06209 Table 2

# (z, fsigma8, sigma) -- see docstring for provenance
RSD_DATA = np.array([
    (0.067, 0.423, 0.055),   # Beutler+ 2012, 6dFGS
    (0.15,  0.490, 0.145),   # Howlett+ 2015, SDSS MGS
    (0.38,  0.497, 0.045),   # Alam+ 2017, BOSS LOWZ
    (0.51,  0.458, 0.038),   # Alam+ 2017, BOSS CMASS1
    (0.61,  0.436, 0.034),   # Alam+ 2017, BOSS CMASS2
    (0.70,  0.473, 0.044),   # Bautista+ 2021, eBOSS LRG
    (0.85,  0.315, 0.095),   # de Mattia+ 2021, eBOSS ELG
    (1.48,  0.462, 0.045),   # Hou+ 2021, eBOSS QSO
], dtype=float)

Z_RSD = RSD_DATA[:, 0]
FS8_OBS = RSD_DATA[:, 1]
FS8_SIG = RSD_DATA[:, 2]
N_RSD = len(Z_RSD)


def _lcdm_growth_on_grid(N_grid, Om_0):
    """Standard LCDM growth D(N), f(N)=dlnD/dlnN (delta_m ~ a at matter era).
    Returns D_arr normalized so D(N=0)=1, and f_arr."""
    from scipy.integrate import solve_ivp
    Or = config.Omega_r
    OL = 1.0 - Om_0 - Or

    def E2(N):
        a = np.exp(N)
        return Om_0 * a**(-3) + Or * a**(-4) + OL

    def Om_frac(N):
        a = np.exp(N)
        return Om_0 * a**(-3) / E2(N)

    def ENE(N):
        a = np.exp(N)
        e2 = E2(N)
        de2 = -3.0 * Om_0 * a**(-3) - 4.0 * Or * a**(-4)
        return 0.5 * de2 / e2

    def rhs(N, y):
        d, dN = y
        return [dN, -(2.0 + ENE(N)) * dN + 1.5 * Om_frac(N) * d]

    N_ini = N_grid[0]
    y0 = [np.exp(N_ini), np.exp(N_ini)]
    sol = solve_ivp(rhs, [N_ini, N_grid[-1]], y0, t_eval=N_grid,
                    rtol=1e-9, atol=1e-11, method='DOP853')
    if not sol.success:
        return None, None
    D_raw = sol.y[0].copy()
    DN_raw = sol.y[1].copy()
    # Compute f = dlnD/dlnN from raw values BEFORE normalization.
    f = DN_raw / D_raw
    # Then renormalize D so D(N=0) = 1.
    D = D_raw / D_raw[-1]
    return D, f


def _interp_fs8_lcdm(Om_0):
    """Return fs8(z) interpolator for LCDM with given Omega_m."""
    N_grid = np.linspace(-3.0, 0.0, 400)
    D, f = _lcdm_growth_on_grid(N_grid, Om_0)
    if D is None:
        return None
    a_grid = np.exp(N_grid)
    z_grid = 1.0 / a_grid - 1.0
    # f*sigma_8(z) = f(z) * sigma_8_0 * D(z)/D(0)
    fs8 = f * SIGMA_8_0 * D
    # sort ascending z
    idx = np.argsort(z_grid)
    return interp1d(z_grid[idx], fs8[idx], kind='cubic',
                    bounds_error=False,
                    fill_value=(fs8[idx][0], fs8[idx][-1]))


def _interp_fs8_quint(V_family, beta, extra_params):
    """fs8(z) interpolator for coupled quintessence via quintessence_perturb."""
    res = qp.growth_factor(V_family, beta, extra_params,
                           N_ini=-3.0, N_end=0.0, n_pts=400)
    if res is None:
        return None
    a_arr, D_arr, f_arr = res
    z_arr = 1.0 / a_arr - 1.0
    fs8 = f_arr * SIGMA_8_0 * D_arr
    idx = np.argsort(z_arr)
    return interp1d(z_arr[idx], fs8[idx], kind='cubic',
                    bounds_error=False,
                    fill_value=(fs8[idx][0], fs8[idx][-1]))


def chi2_lcdm(Om_0):
    """RSD chi^2 for LCDM with given Omega_m."""
    interp = _interp_fs8_lcdm(Om_0)
    if interp is None:
        return np.nan
    fs8_th = np.array([float(interp(z)) for z in Z_RSD])
    delta = FS8_OBS - fs8_th
    return float(np.sum((delta / FS8_SIG)**2))


def chi2_quintessence(V_family, beta, extra_params):
    """RSD chi^2 for coupled quintessence V_family with given parameters."""
    interp = _interp_fs8_quint(V_family, beta, extra_params)
    if interp is None:
        return np.nan
    fs8_th = np.array([float(interp(z)) for z in Z_RSD])
    delta = FS8_OBS - fs8_th
    return float(np.sum((delta / FS8_SIG)**2))


def chi2_fluid_ide(xi_q):
    """RSD chi^2 for Fluid IDE toy. No separate growth equation in the
    fluid picture -- coupling affects background only -- so we use LCDM
    growth with the SAME Omega_m_0. This is a conservative approximation:
    the verdict can only get WORSE if the fluid picture has extra growth
    degrees of freedom it fails to exploit."""
    return chi2_lcdm(config.Omega_m)


if __name__ == "__main__":
    print("RSD likelihood sanity check")
    print(f"  N_RSD points: {N_RSD}")
    print(f"  sigma_8_0    : {SIGMA_8_0}")
    print()
    for Om in [0.28, 0.30, 0.315, 0.33]:
        c = chi2_lcdm(Om)
        print(f"  LCDM(Om={Om}): chi2 = {c:.2f} (dof {N_RSD-1})")
    print()
    print("  Per-point theory vs obs for LCDM(Om=0.315):")
    interp = _interp_fs8_lcdm(0.315)
    for z, obs, sig in RSD_DATA:
        th = float(interp(z))
        dev = (obs - th) / sig
        print(f"    z={z:.3f}  obs={obs:.3f}+/-{sig:.3f}  "
              f"th={th:.3f}  dev={dev:+.2f} sigma")
    print()
    print("  V_RP (beta=0.20, n=0.20):")
    print(f"    chi2 = {chi2_quintessence('RP', 0.20, (0.20,)):.2f}")
    print("  V_RP (beta=0.35, n=0.35):")
    print(f"    chi2 = {chi2_quintessence('RP', 0.35, (0.35,)):.2f}")
