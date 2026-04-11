# -*- coding: utf-8 -*-
"""
C6s: Stringy RVM cosmology with H^2 ln(H^2) running.

Gomez-Valent, Mavromatos, Sola Peracaula CQG 41 015026 (2024):
    rho_vac(H) = c0 + c1 H^2 + c2 H^2 ln(H^2/H0^2) + O(H^4)

Modified Friedmann:
    H^2 = H0^2 [ Om (1+z)^3 + OL_eff(H) ]

with OL_eff self-consistent in H. Solve numerically and extract
CPL-projected (w_0, w_a).
"""
import numpy as np
from scipy.optimize import brentq, curve_fit

Om = 0.315
OL0 = 1 - Om

def rho_vac(H2_ratio, c2):
    """rho_vac / rho_crit0  with ln running"""
    # OL0 absorbs c0+c1. c2 governs running.
    return OL0 + c2 * (H2_ratio * np.log(max(H2_ratio, 1e-12)))

def E2_implicit(z, c2):
    """Solve self-consistent E^2(z) from modified Friedmann."""
    def f(E2):
        return E2 - (Om * (1+z)**3 + rho_vac(E2, c2))
    try:
        return brentq(f, 1e-3, 1e6)
    except ValueError:
        return Om * (1+z)**3 + OL0  # fallback LCDM

def w_eff(z, c2, dz=1e-3):
    rho_de = lambda zp: E2_implicit(zp, c2) - Om*(1+zp)**3
    r1 = rho_de(z + dz)
    r0 = rho_de(z - dz) if z > dz else rho_de(0)
    drho = (r1 - r0)/(2*dz) if z > dz else (r1 - r0)/dz
    w = -1.0 + (1+z)/3.0 * drho/max(rho_de(z), 1e-12)
    return w

def cpl(a, w0, wa):
    return w0 + wa*(1 - a)

def main():
    print("=" * 60)
    print("C6s Stringy RVM H^2 ln(H^2) cosmology")
    print("=" * 60)
    a_grid = np.linspace(0.3, 1.0, 30)
    z_grid = 1.0/a_grid - 1
    print(f"{'c2':>10} {'w_0':>10} {'w_a':>10} {'wa<0?':>8}")
    results = []
    for c2 in [-0.05, -0.02, -0.01, 0.0, 0.01, 0.02, 0.05]:
        w_vals = np.array([w_eff(z, c2) for z in z_grid])
        try:
            (w0, wa), _ = curve_fit(cpl, a_grid, w_vals, p0=[-1.0, 0.0])
        except Exception:
            w0, wa = np.nan, np.nan
        flag = "YES" if wa < 0 else "NO"
        print(f"{c2:>10.3f} {w0:>10.4f} {wa:>10.4f} {flag:>8}")
        results.append((c2, w0, wa))

    desi_wa = -0.83
    desi_err = 0.22
    c2_pass = [r for r in results if np.isfinite(r[2]) and r[2] < 0]
    c2_best = None
    if c2_pass:
        c2_best = min(c2_pass, key=lambda r: abs(r[2] - desi_wa))

    print()
    print(f"DESI wa target: {desi_wa} +/- {desi_err}")
    if c2_best is not None:
        print(f"Best C6s c2 = {c2_best[0]:+.3f} -> wa={c2_best[2]:.4f}")
        dev = abs(c2_best[2] - desi_wa)/desi_err
        print(f"Deviation: {dev:.2f} sigma")
        print(f"Within 2 sigma of DESI: {dev < 2}")
    print()
    print("C4 structural wa<0: " + ("PASS (c2<0 branch)" if c2_pass else "FAIL"))

if __name__ == "__main__":
    main()
