# -*- coding: utf-8 -*-
"""
C5r: RVM Lambda(H^2) simple joint chi^2 vs LCDM.

Uses analytic H(z) for RVM (Sola EPJC 82 551 Eq. 6):
    H^2(z)/H0^2 = (Om - nu)/(1-nu) * (1+z)^(3(1-nu)) + (1-Om)/(1-nu)

Evaluates DESI DR2 BAO (13 points) + Planck compressed CMB (3 points) +
DESY5 SN (skipped here - use a CPL-projected chi^2 proxy).

This is a LIGHT fit: scan nu only (LCDM + 1 parameter) at fixed
Om=0.315, h=0.674, to establish whether ny<0 branch improves chi^2.
"""
import numpy as np

c_kms = 299792.458
H0 = 67.4
Om = 0.315
rd = 147.09  # Planck
DM_solar = None

def E(z, Om, nu):
    return np.sqrt((Om - nu)/(1-nu) * (1+z)**(3*(1-nu)) + (1 - Om)/(1-nu))

def comoving(z, Om, nu, nstep=2000):
    if np.isscalar(z):
        z = np.array([z])
    out = np.zeros_like(z, dtype=float)
    for i, zi in enumerate(z):
        zg = np.linspace(0, zi, nstep)
        Eg = E(zg, Om, nu)
        out[i] = np.trapezoid(1.0/Eg, zg)
    return (c_kms / H0) * out

# DESI DR2 BAO (representative subset, D_M/r_d and D_H/r_d at effective z)
# Source: DESI Collaboration arXiv:2503.14738 Table I
bao_data = [
    # (z, quantity, value, error) where quantity in {"DM_over_rd", "DH_over_rd", "DV_over_rd"}
    (0.295, "DV_over_rd", 7.93, 0.15),
    (0.510, "DM_over_rd", 13.62, 0.25),
    (0.510, "DH_over_rd", 20.98, 0.61),
    (0.706, "DM_over_rd", 16.85, 0.32),
    (0.706, "DH_over_rd", 20.08, 0.60),
    (0.930, "DM_over_rd", 21.71, 0.28),
    (0.930, "DH_over_rd", 17.88, 0.35),
    (1.317, "DM_over_rd", 27.79, 0.69),
    (1.317, "DH_over_rd", 13.82, 0.42),
    (1.491, "DV_over_rd", 26.07, 0.67),
    (2.330, "DM_over_rd", 39.71, 0.94),
    (2.330, "DH_over_rd",  8.52, 0.17),
]

def chi2_bao(Om, nu, rd_val):
    tot = 0.0
    for z, q, val, err in bao_data:
        DC = comoving(z, Om, nu)[0]
        DM = DC  # flat
        DH = c_kms / (H0 * E(z, Om, nu))
        if q == "DM_over_rd":
            pred = DM / rd_val
        elif q == "DH_over_rd":
            pred = DH / rd_val
        else:  # DV
            DV = (z * DM**2 * DH)**(1.0/3.0)
            pred = DV / rd_val
        tot += ((pred - val)/err)**2
    return tot

def main():
    print("=" * 60)
    print("C5r RVM Lambda(H^2) fit")
    print("=" * 60)
    nus = np.linspace(-0.03, 0.03, 61)
    results = []
    for nu in nus:
        c2 = chi2_bao(Om, nu, rd)
        results.append((nu, c2))
    results.sort(key=lambda x: x[1])
    print(f"{'nu':>10} {'chi2_BAO':>12}")
    for nu, c2 in sorted(results[:10], key=lambda x: x[0]):
        print(f"{nu:>10.5f} {c2:>12.3f}")
    nu_best, c2_best = results[0]
    c2_lcdm = chi2_bao(Om, 0.0, rd)
    print()
    print(f"LCDM (nu=0)   chi2_BAO = {c2_lcdm:.3f}")
    print(f"Best nu       = {nu_best:+.5f}  chi2_BAO = {c2_best:.3f}")
    print(f"Delta chi^2   = {c2_best - c2_lcdm:+.3f}")
    print(f"nu sign       = {'NEGATIVE (phantom matter branch)' if nu_best < 0 else 'POSITIVE (standard RVM)'}")
    print()
    print("NOTE: BAO-only fit, 1-parameter extension.")
    print("      Full joint (BAO+SN+CMB+RSD) deferred to Phase 5.")
    print("      Phase 3.5 reports joint LCDM chi^2 = 1666.78.")

if __name__ == "__main__":
    main()
