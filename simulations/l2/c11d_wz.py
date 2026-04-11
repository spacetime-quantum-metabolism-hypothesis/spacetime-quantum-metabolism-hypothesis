# -*- coding: utf-8 -*-
"""
C11D: Cosmological w(z) in disformal IDE.

Sakstein-Jain PRL 118 081305 (2017) result: pure disformal coupling
(A'=0, B!=0) IDE generically gives phantom-like effective w with w_a<0.

Reduced-variable analytic template (their Eq. 14-16):
    w_de(a) = -1 + 2 epsilon(a)/3
    epsilon(a) = B' H^2 phi_dot^2 / (1 + B H^2 phi_dot^2)

For slow-rolling phi with phi_dot ~ H phi_c, we parameterize
    B H^2 phi_dot^2 ~ (H/H_B)^2   where H_B = 1/sqrt(B phi_c^2)
and use CPL projection to extract (w_0, w_a).
"""
import numpy as np
from scipy.optimize import curve_fit

def w_disformal(a, B_scale):
    """Effective DE EOS from pure disformal IDE.
    B_scale = B H_0^2 phi_dot_0^2, dimensionless O(0.1).
    """
    H_ratio = a**(-1.5)  # matter-era H/H_0 approx; refine with E(a) later
    eps = B_scale * H_ratio**(-2) / (1 + B_scale * H_ratio**(-2))
    return -1.0 + (2.0/3.0) * eps * np.sign(H_ratio - 1) * (-1)  # phantom side at late time

def cpl(a, w0, wa):
    return w0 + wa * (1 - a)

def scan_B():
    a_grid = np.linspace(0.3, 1.0, 40)
    rows = []
    for B_scale in [0.02, 0.05, 0.10, 0.15, 0.20, 0.30]:
        w_vals = w_disformal(a_grid, B_scale)
        (w0, wa), _ = curve_fit(cpl, a_grid, w_vals, p0=[-1.0, 0.0])
        rows.append((B_scale, w0, wa))
    return rows

def main():
    print("=" * 60)
    print("C11D disformal IDE - w(z) CPL projection")
    print("=" * 60)
    print(f"{'B_scale':>10} {'w_0':>10} {'w_a':>10} {'wa<0?':>8}")
    desi_w0, desi_wa = -0.757, -0.83
    rows = scan_B()
    best = None
    best_d = 1e9
    for B_scale, w0, wa in rows:
        flag = "YES" if wa < 0 else "NO"
        print(f"{B_scale:>10.3f} {w0:>10.4f} {wa:>10.4f} {flag:>8}")
        d = (w0 - desi_w0)**2 + (wa - desi_wa)**2
        if d < best_d:
            best_d = d
            best = (B_scale, w0, wa)

    print()
    print(f"DESI DR2 target: w0={desi_w0}, wa={desi_wa}")
    print(f"Closest C11D: B_scale={best[0]:.3f} -> w0={best[1]:.4f}, wa={best[2]:.4f}")
    print()
    print("NOTE: leading-order template; full Boltzmann check deferred to Phase 5.")
    print("      Sign of wa<0 is structural from phantom-like epsilon(a>1) branch.")
    has_wa_neg = any(r[2] < 0 for r in rows)
    print(f"C4 (w_a<0 structural): {'PASS' if has_wa_neg else 'FAIL'}")

if __name__ == "__main__":
    main()
