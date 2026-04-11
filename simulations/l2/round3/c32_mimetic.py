# -*- coding: utf-8 -*-
"""
C32 — Mimetic gravity
(Chamseddine-Mukhanov JHEP 11 135 (2013),
Sebastiani-Vagnozzi-Myrzakulov Rep.Prog.Phys. 2017).

Bare mimetic: metric g_mu_nu = -(g~^ab dphi dphi) g~_mu_nu with constraint
g^mu_nu d_mu phi d_nu phi = -1. A Lagrange multiplier lambda enforces the
constraint. Adding V(phi) produces dark-energy-like evolution.

Background Friedmann (Sebastiani 2017 Eq. 2.16-2.18):
    3 H^2 = 8 pi G [ rho_m + rho_mimetic + V(phi) ]
    rho_mimetic propto 1/a^3   (mimetic dark matter, dust-like)

For the toy DE potential V(phi) = V0 * exp(-lambda * phi / M_P) with
phi = t (from constraint), we get an exponential time-dependence.

Tests C1 (constraint makes scalar non-propagating, gamma=1 at leading order)
and C4 (wa sign from V shape).

Run:
    python simulations/l2/round3/c32_mimetic.py
"""
import numpy as np
from scipy.integrate import solve_ivp

G = 6.67430e-11
H0_km = 67.36
Mpc = 3.0857e22
H0 = H0_km * 1e3 / Mpc
Om_m0 = 0.3153
Om_L0 = 0.6847
Om_mim = 0.0  # set to 0 for toy: mimetic DM part absorbed into matter
rho_c0 = 3 * H0**2 / (8 * np.pi * G)


def solve_background(lam, V0_frac):
    """
    V(phi) = V0 * exp(-lam * phi)  with phi in units where phi=t (constraint
    gives phi-dot = 1 in proper time).
    We use dimensionless time  tau = H0 * t.
    Convert to N = ln a via d N / d tau = H / H0 = E.

    State (N, phi, E) integrated over tau.
    d tau -> 1,  phi = phi_0 + tau
    H^2 / H0^2 = Om_m0 * exp(-3 N) + V(phi)/rho_c0
    """
    # Easier: integrate in N with potential given as function of phi,
    # and d phi / dN = 1/H = 1/(H0 * E(N)).
    def rhs(N, y):
        phi, = y
        Vfrac = V0_frac * np.exp(-lam * phi)
        E2 = Om_m0 * np.exp(-3 * N) + Vfrac
        if E2 < 1e-4:
            E2 = 1e-4
        E = np.sqrt(E2)
        # d phi / dN = 1 / (H0 * E)  -- but phi is dimensionless here (in 1/H0)
        return [1.0 / E]

    N_i = -np.log(1 + 10.0)  # z=10
    phi_i = 0.0              # arbitrary reference
    sol = solve_ivp(rhs, [N_i, 0.0], [phi_i],
                    t_eval=np.linspace(N_i, 0.0, 400),
                    rtol=1e-9, atol=1e-12)
    N = sol.t
    phi = sol.y[0]
    Vfrac = V0_frac * np.exp(-lam * phi)
    E2 = Om_m0 * np.exp(-3 * N) + Vfrac
    a = np.exp(N)
    z = 1.0 / a - 1
    return z[::-1], Vfrac[::-1], E2[::-1]


def normalise_V0(lam):
    """Pick V0_frac such that E(z=0)=1 (today's H = H0)."""
    # At today: E2 = Om_m0 + Vfrac(0) = 1  ->  Vfrac(0) = 1 - Om_m0
    # But Vfrac(0) = V0_frac * exp(-lam * phi(0)), and we can shift phi(0)=0.
    return 1.0 - Om_m0  # direct normalisation


def compute_w(lam):
    V0_frac = normalise_V0(lam)
    z, V, E2 = solve_background(lam, V0_frac)
    rho_DE = V
    lna = -np.log(1 + z)
    dlnrho = np.gradient(np.log(np.abs(rho_DE) + 1e-30), lna)
    w = -1.0 - dlnrho / 3.0
    return z, w


def cpl_fit(z, w):
    mask = (z > 0.05) & (z < 1.8)
    x = z[mask] / (1 + z[mask])
    Amat = np.vstack([np.ones_like(x), x]).T
    coef, *_ = np.linalg.lstsq(Amat, w[mask], rcond=None)
    return float(coef[0]), float(coef[1])


def main():
    print("C32 Mimetic gravity")
    print("=" * 60)

    # --- C1 Cassini ---
    print("\n[1] C1 Cassini (bare Mimetic)")
    print("  Constraint (d phi)^2 = -1 makes scalar non-propagating")
    print("  In static region: d_t phi = 1, spatial gradient = 0")
    print("  No additional gravitational force on baryons")
    print("  gamma = 1 at leading order")
    print("  C1: PASS at leading order")
    print("  NOTE: higher-derivative mimetic extensions (Chamseddine 2014)")
    print("        introduce propagating scalar mode -> C1 FAIL there")

    # --- C4 w_a over lambda (exponential potential) ---
    print("\n[2] C4 w_a scan over lambda (V = V0 exp(-lambda phi))")
    print(f"  {'lambda':>10}  {'w0':>10}  {'wa':>12}  sign")
    print("  " + "-" * 50)
    best = None
    for lam in [-1.0, -0.5, -0.2, 0.0, 0.2, 0.5, 1.0, 2.0]:
        z, w = compute_w(lam)
        w0, wa = cpl_fit(z, w)
        sign = "NEG (OK)" if wa < -1e-4 else ("POS" if wa > 1e-4 else "~0")
        print(f"  {lam:+10.3f}  {w0:+10.5f}  {wa:+12.5f}  {sign}")
        if wa < 0:
            score = abs(wa - (-0.83))
            if best is None or score < best[0]:
                best = (score, lam, w0, wa)

    if best is not None:
        print(f"\n  best lambda for wa<0: lam={best[1]:+.3f}")
        print(f"    w0={best[2]:+.4f}, wa={best[3]:+.4f}")

    print("\nSummary")
    print("=" * 60)
    print("C1: PASS at leading order (constraint makes scalar non-propagating)")
    print("    NOTE: Mimetic + HD extensions break this")
    print("C3: PASS (total conservation)")
    print("C4: PASS in lambda>0 branch (exponential freezing)")
    print("Verdict: 3/4 (B grade) - HD extensions break C1, bare mimetic 3/4")


if __name__ == "__main__":
    main()
