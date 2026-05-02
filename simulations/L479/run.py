"""
L479 — Holographic energy-density crossing: priori derivation attempt.

Maps:
  - paper foundation 3 (UV holographic identity): sigma_0 = 4 pi G t_P
    => energy-density saturation rho_UV(L) ~ M_P^2 c^4 / L^2 (Cohen-Kaplan-Nelson IR cutoff form)
  - paper derived 4 (Lambda origin): rho_Lambda = n_inf * eps / c^2 ~ rho_Planck/(4 pi)
    => system-mass holographic ceiling rho_sys(R,M) = M c^2 / (4/3 pi R^3)

L463 free-speculation surviving sub-hypothesis (energy-density crossing):
   rho_UV(L) = rho_sys(L, M)   =>   M*(L) = (4/3) pi M_P^2 c^2 L / (G * ???)
We carry the dimensional pre-factors explicitly and check whether real
astrophysical scales (galaxy / cluster / supercluster / cosmic / Planck)
land on the crossing curve.

Prediction to test:
   The crossing M*(L) is a SINGLE monotone curve (one mass per radius).
   The interesting physics is whether OBSERVED bound systems hug it.
   Three regimes are tested:
     - sub-galactic scale (kpc, M ~ 1e10 Msun)
     - galaxy / group   (~100 kpc, ~1e12-1e13 Msun)
     - cluster          (1-3 Mpc, ~1e14-1e15 Msun)
     - supercluster     (50 Mpc, ~1e17 Msun)
     - cosmic / Hubble  (4400 Mpc, ~1e23 Msun)

Verdict logic:
   If only one regime sits within ~0.5 dex of the crossing curve, that
   regime is "uniquely picked out" by the holographic energy-density
   crossing; otherwise the crossing is a generic upper envelope and the
   coincidence with cluster scale is empirically suggestive but NOT
   priori-forced.
"""

from __future__ import annotations

import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import numpy as np

# ---------------- constants (SI) ----------------
c    = 2.99792458e8
G    = 6.67430e-11
hbar = 1.054571817e-34
Mpc  = 3.0856775814913673e22
Msun = 1.98847e30
kpc  = Mpc / 1000.0

M_P     = np.sqrt(hbar * c / G)            # ~2.176e-8 kg
l_P     = np.sqrt(hbar * G / c**3)         # ~1.616e-35 m
t_P     = l_P / c
rho_P   = c**5 / (hbar * G**2)             # Planck density ~5.16e96 kg/m^3
rho_Lam = rho_P / (4.0 * np.pi)            # paper derived-4 input scale (n_inf*eps/c^2)


# ---------------- holographic energy densities ----------------

def rho_UV_CKN(L_m):
    """Cohen-Kaplan-Nelson UV-IR saturation (foundation-3 channel).

    rho_UV * L^4 <= M_P^2 c^2 L^2  =>  rho_UV ~ M_P^2 c^2 / L^2 (mass-density)
    Equivalent energy density: rho_UV * c^2 = M_P^2 c^4 / L^2 (J/m^3).
    Here we keep MASS density (kg/m^3) for direct comparison with rho_sys.
    """
    L = np.asarray(L_m, dtype=float)
    return M_P**2 / (L**2 * (hbar / c))     # = M_P^2 c / (hbar L^2) [kg/m^3]
    # Note: M_P^2 c / hbar = c^3/G/c = c^3/G... let's verify by alternative path:


def rho_UV_alt(L_m):
    """Alternative form: rho_UV = c^2 / (G L^2). Equivalent to above modulo
    M_P^2 c / hbar = c^2 / G (since M_P^2 = hbar c / G)."""
    L = np.asarray(L_m, dtype=float)
    return c**2 / (G * L**2)                 # kg/m^3, exact


def rho_sys_BH(R_m, M_kg):
    """Mean mass density of a self-gravitating system (Bekenstein/BH limit
    when M -> M_BH(R) = R c^2 / 2G)."""
    R = np.asarray(R_m, dtype=float)
    M = np.asarray(M_kg, dtype=float)
    return M / (4.0 * np.pi / 3.0 * R**3)


def crossing_mass(L_m):
    """Solve rho_UV(L) = rho_sys(L, M*) for M*.

    rho_UV = c^2/(G L^2);  rho_sys = M / (4/3 pi L^3)
    =>  M*(L) = (4 pi / 3) * c^2 L / G  (independent of hbar — purely classical!)
    """
    L = np.asarray(L_m, dtype=float)
    return (4.0 * np.pi / 3.0) * c**2 * L / G


# ---------------- anchors ----------------

ANCHORS = [
    # name,                 R [m],          M [kg]
    ("Globular cluster",   30.0 * kpc * 1e-3, 1e6  * Msun),  # 30 pc, 1e6 Msun
    ("Dwarf galaxy",       1.0 * kpc,       1e9  * Msun),
    ("Milky Way disk",     15.0 * kpc,      1e12 * Msun),
    ("Galaxy halo",        200.0 * kpc,     2e12 * Msun),
    ("Galaxy group",       0.5 * Mpc,       5e13 * Msun),
    ("Virgo cluster",      2.0 * Mpc,       1.2e15 * Msun),
    ("Coma cluster",       3.0 * Mpc,       1.5e15 * Msun),
    ("Massive cluster",    2.5 * Mpc,       2.0e15 * Msun),
    ("Supercluster",       50.0 * Mpc,      1e17 * Msun),
    ("BAO scale",          150.0 * Mpc,     1e18 * Msun),
    ("Hubble volume",      4400.0 * Mpc,    1e23 * Msun),
]


def report():
    print("=" * 78)
    print("L479  Holographic energy-density crossing (foundation 3 x derived 4)")
    print("=" * 78)
    print(f"M_P       = {M_P:.3e} kg")
    print(f"l_P       = {l_P:.3e} m")
    print(f"t_P       = {t_P:.3e} s")
    print(f"rho_P     = {rho_P:.3e} kg/m^3 (Planck density)")
    print(f"rho_Lam   = rho_P/(4 pi) = {rho_Lam:.3e} kg/m^3  (paper derived-4)")
    print()

    # consistency check: two rho_UV forms agree
    Ltest = 1.0 * Mpc
    print(f"sanity: rho_UV via M_P^2 c/(hbar L^2) at L=1 Mpc = {rho_UV_CKN(Ltest):.3e}")
    print(f"sanity: rho_UV via c^2/(G L^2)         at L=1 Mpc = {rho_UV_alt(Ltest):.3e}")
    print()

    # crossing curve
    print("Crossing M*(L) = (4 pi / 3) c^2 L / G  (purely classical, hbar drops out)")
    print()
    L_grid = np.logspace(np.log10(0.1*kpc), np.log10(5e3*Mpc), 11)
    print(f"{'L [Mpc]':>14}  {'M*(L) [Msun]':>16}")
    for L in L_grid:
        Ms = crossing_mass(L)
        if L >= Mpc:
            print(f"{L/Mpc:14.3e}  {Ms/Msun:16.3e}")
        else:
            print(f"{L/Mpc:14.3e}  {Ms/Msun:16.3e}")
    print()

    # anchors: how close are real systems to the crossing line?
    print("Astrophysical anchors  vs  crossing line  (excess = log10 M / M*(R))")
    print(f"{'name':>22}  {'R [Mpc]':>10}  {'M [Msun]':>12}  "
          f"{'M*(R) [Msun]':>14}  {'log10 M/M*':>11}  {'verdict':>10}")
    flagged = []
    for name, R, M in ANCHORS:
        Mstar = crossing_mass(R)
        excess = np.log10(M / Mstar)
        if abs(excess) < 0.5:
            verdict = "ON LINE"
            flagged.append((name, excess))
        elif abs(excess) < 1.0:
            verdict = "near"
        else:
            verdict = "off"
        print(f"{name:>22}  {R/Mpc:10.3f}  {M/Msun:12.2e}  "
              f"{Mstar/Msun:14.2e}  {excess:11.3f}  {verdict:>10}")
    print()

    # verdict
    print("-" * 78)
    if not flagged:
        print("VERDICT: NO anchor sits within 0.5 dex of crossing line.")
        print("         Cluster scale is NOT singled out by holographic crossing.")
        print("         Priori derivation:  IMPOSSIBLE  (claim falsified).")
    else:
        names = [n for n, _ in flagged]
        if len(flagged) == 1:
            print(f"VERDICT: ONLY {names[0]} sits within 0.5 dex of crossing line.")
            print("         Cluster scale uniquely picked out (if name=cluster).")
        else:
            print(f"VERDICT: MULTIPLE anchors near crossing: {names}")
            print("         Crossing line not unique to clusters — generic envelope.")
    print("-" * 78)

    # falsification-grid check across mass scales
    print()
    print("Falsification grid (does the crossing coincide with M_BH limit M = R c^2/2G?)")
    print("If M*(L) = (4 pi/3) c^2 L/G  and  M_BH(R) = c^2 R/(2G),")
    print("ratio M*/M_BH = (4 pi/3) / (1/2) = 8 pi / 3 ~ 8.38  (constant, scale-free)")
    ratio = (4.0 * np.pi / 3.0) / 0.5
    print(f"  computed:  M*/M_BH = {ratio:.4f}  (expected 8.378)")
    print()
    print("=> M*(L) is just the SCHWARZSCHILD-RADIUS line shifted by 8.38x.")
    print("   It is NOT a feature of cluster physics — it is a UNIVERSAL")
    print("   black-hole-density curve. Any system on it is a black hole.")
    print()
    print("Real clusters have M ~ 1e15 Msun at R ~ 2 Mpc.")
    print(f"  M_BH(2 Mpc)    = {0.5*c**2*(2*Mpc)/G/Msun:.3e} Msun")
    print(f"  M*(2 Mpc)      = {crossing_mass(2*Mpc)/Msun:.3e} Msun")
    print(f"  M_obs(cluster) ~ 1.5e15 Msun")
    print(f"  log10 M_obs/M_BH = {np.log10(1.5e15*Msun / (0.5*c**2*2*Mpc/G)):.3f}")


if __name__ == "__main__":
    report()
