# -*- coding: utf-8 -*-
"""
Phase 3.6 -- B2. Vainshtein screening radius.

For a cubic-Galileon-like non-linear kinetic term the fifth force is
suppressed inside the Vainshtein radius

    r_V = [ r_S * M_Pl^2 / M^4 ]^{1/3}                                  [Vai72]

where r_S = 2 G M_body / c^2 is the Schwarzschild radius of the source and M
is the strong-coupling mass of the Galileon / k-essence non-linear term.

For SQMH / k-essence with L_2 = X + gamma X^2 / M^4, the natural cosmological
scale is

    M^4 ~ M_Pl^2 H_0^2                                                  [SP06]

(Nicolis, Rattazzi, Trincherini 2009; cubic Galileon conformal coupling).
With this choice

    r_V ~ [ r_S * M_Pl^2 / (M_Pl^2 H_0^2) ]^{1/3}
        = [ r_S / H_0^2 ]^{1/3}
        = [ (2 G M / c^2) * (c / H_0)^2 ]^{1/3}
        = [ 2 G M / H_0^2 / c^2 * c^2 ]^{1/3}
        = [ 2 G M (c / H_0)^2 / c^2 ]^{1/3}

Numerically the Vainshtein radius for the Sun is of order

    r_V,Sun ~ 100 pc

so every solar-system test is DEEP inside r_V. The fifth-force suppression
factor in cubic Galileon is (r / r_V)^{3/2} for r << r_V.

Combined with B1: the unscreened |gamma-1| = 2.3e-2 (from beta ~ 0.1) must be
suppressed by at least 1e3 to satisfy Cassini. Required suppression factor at
Cassini distance r_Cas ~ 8 AU:

    (r_Cas / r_V)^{3/2} < 1e-3

    -> r_Cas / r_V < 1e-2
    -> r_V > 100 * r_Cas ~ 1.2e16 m ~ 4e-10 Gpc ~ 4 pc

Sun's r_V ~ 100 pc already exceeds this by factor 25 -> PASS for Sun.
"""
import numpy as np


# --- Physical constants (SI) ---
G = 6.67430e-11              # m^3 kg^-1 s^-2
c = 2.99792458e8             # m/s
H0_SI = 67.36e3 / 3.0857e22  # s^-1, h=0.6736
AU = 1.495978707e11          # m
PARSEC = 3.0857e16           # m
M_SUN = 1.98847e30           # kg
M_EARTH = 5.9722e24          # kg
M_WD = 0.6 * M_SUN           # typical white dwarf
R_CASSINI = 8.0 * AU         # Cassini grazing distance ~ 8 AU


def schwarzschild_radius(M):
    return 2.0 * G * M / c**2


def r_vainshtein(M_body, M4_over_MP2H02=1.0):
    """
    Vainshtein radius for a point source of mass M_body.

    Assumes cubic Galileon / k-essence with M^4 = M4_over_MP2H02 * M_Pl^2 * H_0^2.
    The natural value is M4_over_MP2H02 = O(1).

        r_V^3 = r_S * M_Pl^2 / M^4 = r_S / (M4_over_MP2H02 * H_0^2 / c^2 * c^2)

    We use the dimensional shortcut:

        r_V = [ r_S (c/H_0)^2 / M4_over_MP2H02 ]^{1/3}
    """
    rS = schwarzschild_radius(M_body)
    rH = c / H0_SI                              # Hubble radius (m)
    r_V3 = rS * rH**2 / M4_over_MP2H02
    return r_V3**(1.0/3.0)


def suppression_factor(r, r_V):
    """Cubic-Galileon fifth-force suppression (r << r_V limit)."""
    if r >= r_V:
        return 1.0
    return (r / r_V)**1.5


def _fmt_length(x_m):
    if x_m >= PARSEC:
        return f"{x_m/PARSEC:.3e} pc"
    if x_m >= AU:
        return f"{x_m/AU:.3e} AU"
    if x_m >= 1e3:
        return f"{x_m/1e3:.3e} km"
    return f"{x_m:.3e} m"


def report():
    print("=" * 72)
    print("Phase 3.6 B2 -- Vainshtein radius scan (cubic Galileon, M^4 ~ M_P^2 H_0^2)")
    print("=" * 72)
    print(f"Hubble radius c/H_0 = {_fmt_length(c/H0_SI)}")
    print()
    print(f"{'body':<12}{'M[kg]':<14}{'r_S':<18}{'r_V':<18}{'r_V [AU or pc]':<20}")
    for name, M in [("Sun", M_SUN), ("Earth", M_EARTH),
                    ("white dwarf", M_WD), ("Jupiter", 1.898e27),
                    ("Milky Way", 1.5e12 * M_SUN)]:
        rS = schwarzschild_radius(M)
        rV = r_vainshtein(M)
        print(f"{name:<12}{M:<14.3e}{_fmt_length(rS):<18}{rV:<18.3e}{_fmt_length(rV):<20}")

    print()
    print("--- Fifth-force suppression at Cassini distance (r ~ 8 AU from Sun) ---")
    rV_sun = r_vainshtein(M_SUN)
    ratio = R_CASSINI / rV_sun
    S = suppression_factor(R_CASSINI, rV_sun)
    print(f"  r_V,Sun       = {_fmt_length(rV_sun)}")
    print(f"  r_Cas / r_V   = {ratio:.3e}")
    print(f"  (r/r_V)^1.5   = {S:.3e}   (fifth-force suppression factor)")
    print()

    # B1 said unscreened |gamma-1| at beta=0.107 is 2.26e-2, limit 2.3e-5.
    # Required suppression = 2.3e-5 / 2.26e-2 = 1.02e-3.
    gamma_unscr = 2.26e-2
    gamma_limit = 2.3e-5
    required = gamma_limit / gamma_unscr
    print(f"  Required suppression (to satisfy Cassini with beta=0.107):")
    print(f"    {gamma_limit:.2e} / {gamma_unscr:.2e} = {required:.2e}")
    print(f"  Provided by cubic Galileon:  {S:.2e}")
    if S < required:
        print(f"  --> PASS: suppression {S:.2e} < required {required:.2e}")
    else:
        print(f"  --> FAIL: suppression {S:.2e} > required {required:.2e}")

    # Earth
    print()
    print("--- Earth fifth-force (r ~ R_Earth) ---")
    R_EARTH = 6.371e6
    rV_e = r_vainshtein(M_EARTH)
    Se = suppression_factor(R_EARTH, rV_e)
    print(f"  r_V,Earth     = {_fmt_length(rV_e)}")
    print(f"  R_E / r_V     = {R_EARTH/rV_e:.3e}")
    print(f"  suppression   = {Se:.3e}")


if __name__ == "__main__":
    report()
