# -*- coding: utf-8 -*-
"""
patch_template.py
V(phi) reference implementation for porting to CLASS C code.

CANONICAL V_family REPRESENTATION (all Phase 1/2/3 code must use this):
  Python side  : strings "mass", "RP", "exp"   (used by quintessence.py,
                 desi_fitting.py, yaml configs, verify_background.py)
  CLASS C side : integer enum below — mapped at the Python/C boundary only.

Signature convention for C port:
  double V_sqmh(double phi, int V_family_code, double * V_params);
  double dVdphi_sqmh(double phi, int V_family_code, double * V_params);

Python here serves as verification oracle for verify_background.py.
"""
import numpy as np

# C-side integer codes (parity with include/background.h enum).
# Python callers pass the string name; _TO_CODE maps at the boundary.
V_MASS = 0
V_RP = 1
V_EXP = 2

_TO_CODE = {"mass": V_MASS, "RP": V_RP, "exp": V_EXP}


def _resolve(V_family):
    """Accept either string name or integer code. Returns int code."""
    if isinstance(V_family, str):
        if V_family not in _TO_CODE:
            raise ValueError(f"Unknown V_family string: {V_family!r}")
        return _TO_CODE[V_family]
    return int(V_family)


def V_sqmh(phi, V_family, V_params):
    """V(phi) in reduced-Planck units. Returns V_tilde = V/(3*H0^2).

    V_family: "mass"|"RP"|"exp" (canonical) or V_MASS/V_RP/V_EXP int code.
    """
    code = _resolve(V_family)
    if code == V_MASS:
        A = V_params[0]
        return 0.5 * A * phi**2
    elif code == V_RP:
        A, n = V_params[0], V_params[1]
        if phi <= 0:
            phi = 1e-8
        return A * phi**(-n)
    elif code == V_EXP:
        A, lam = V_params[0], V_params[1]
        return A * np.exp(-lam * phi)
    raise ValueError(V_family)


def dVdphi_sqmh(phi, V_family, V_params):
    """dV/dphi in same units."""
    code = _resolve(V_family)
    if code == V_MASS:
        A = V_params[0]
        return A * phi
    elif code == V_RP:
        A, n = V_params[0], V_params[1]
        if phi <= 0:
            phi = 1e-8
        return -n * A * phi**(-n - 1)
    elif code == V_EXP:
        A, lam = V_params[0], V_params[1]
        return -lam * A * np.exp(-lam * phi)
    raise ValueError(V_family)


# CLASS struct field layout reference (to be added to include/background.h):
#
# struct background {
#     ...existing...
#
#     /* SQMH extension */
#     int SQMH_enabled;           /* 0=off, 1=on */
#     int SQMH_V_family;          /* V_MASS=0, V_RP=1, V_EXP=2 */
#     double SQMH_V_params[4];    /* amplitude, shape params */
#     double SQMH_xi;             /* matter-scalar coupling (beta) */
#
#     /* storage for background evolution */
#     int index_bg_phi_sqmh;
#     int index_bg_phi_prime_sqmh;
#     int index_bg_rho_sqmh;
#     int index_bg_p_sqmh;
#     int index_bg_w_sqmh;
# };


# Reference Klein-Gordon in CLASS tau (conformal time) variable:
# Note: CLASS uses conformal time tau, dtau = dt/a, H_conf = a'/a = a*H
#
#   phi'' + 2*H_conf*phi' + a^2 * dV/dphi = -a^2 * sqrt(2/3)*xi*rho_m
#   rho_m' + 3*H_conf*rho_m = +sqrt(2/3)*xi*phi'*rho_m  (conformal time)
#
# Conversion Phase 1 (e-folds N) <-> CLASS (conformal tau):
#   dN = H*dt = H*a*dtau = H_conf*dtau
#   phi_N = phi_prime / H_conf  (where prime is d/dtau)
#   phi_NN = phi''/H_conf^2 - (H_conf'/H_conf^3)*phi_prime

if __name__ == "__main__":
    # Quick sanity: V_sqmh(phi=1) with amplitude 0.685 should give 0.685 for RP
    Omega_DE_0 = 0.685

    # V_mass: A = 2*Omega_DE_0 so V(1) = 0.685
    print("V_mass(phi=1, A=1.37):", V_sqmh(1.0, "mass", [1.37]))
    print("  dV/dphi:", dVdphi_sqmh(1.0, "mass", [1.37]))

    # V_RP: A = Omega_DE_0
    print("V_RP(phi=1, A=0.685, n=1):", V_sqmh(1.0, "RP", [0.685, 1.0]))
    print("  dV/dphi:", dVdphi_sqmh(1.0, "RP", [0.685, 1.0]))

    # V_exp: A = Omega_DE_0 * exp(lam=1)
    print("V_exp(phi=1, A=0.685*e, lam=1):",
          V_sqmh(1.0, "exp", [0.685 * np.e, 1.0]))
    print("  dV/dphi:",
          dVdphi_sqmh(1.0, "exp", [0.685 * np.e, 1.0]))

    # String/int equivalence check
    assert V_sqmh(1.0, "RP", [0.685, 1.0]) == V_sqmh(1.0, V_RP, [0.685, 1.0])
    print("[OK] string/int V_family equivalence")
