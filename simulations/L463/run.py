"""
L463 free speculation — CKN x Bekenstein crossing at cluster scales.

Hypothesis (speculation, not derivation):
    Cluster-scale dip in SQT effective sigma_0 may originate from a
    crossover regime where the cosmic Cohen-Kaplan-Nelson (CKN) holographic
    dof bound (set by the Hubble / system IR scale) and the local Bekenstein
    information bound (set by the bound state mass-radius) become
    *commensurate*, leading to destructive interference between the two
    saturation channels.

Toy quantities (order-of-magnitude only — explicitly speculative):

    1. CKN dof for a region of size L:
           N_CKN(L) ~ (L * M_P / hbar_eff)^{3/2}
       where M_P = sqrt(hbar c / G) (Planck mass) and we use the
       UV-IR relation rho_vac * L^4 <= M_P^2 * L^2.

    2. Bekenstein bound for a self-gravitating system of mass M and radius R:
           N_Bek(R, M) ~ 2 pi R M c / (hbar * ln 2)
       For a system at the gravitational radius the black-hole limit gives
           N_BH(R) = A / (4 * l_P^2) = pi R^2 / l_P^2.

    3. Define a "tension ratio"
           T(L, M) = N_CKN(L) / N_Bek(L, M)
       The crossing T = 1 picks out a *scale-mass* curve. If real clusters
       (M ~ 1e14--1e15 M_sun, R ~ 1--3 Mpc) sit close to that curve, the
       hypothesis predicts an effective dof saturation overlap, which we
       *speculate* could weaken the SQT coupling sigma_0 by an interference
       suppression S(T) = 1 - exp(-(log10 T)^2 / w^2).

This script computes the crossing curve and prints how close real
cluster, galaxy, and Hubble-volume scales sit to it. It is purely
illustrative, no fitting to data.
"""

from __future__ import annotations

import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import numpy as np

# ---------- constants (SI) ----------
c    = 2.99792458e8       # m/s
G    = 6.67430e-11        # m^3 / (kg s^2)
hbar = 1.054571817e-34    # J s
kB   = 1.380649e-23       # J/K
ln2  = np.log(2.0)

M_P  = np.sqrt(hbar * c / G)          # ~2.176e-8 kg
l_P  = np.sqrt(hbar * G / c**3)        # ~1.616e-35 m

Mpc  = 3.0856775814913673e22           # m
Msun = 1.98847e30                      # kg


def N_CKN(L_m: np.ndarray | float) -> np.ndarray | float:
    """Cohen-Kaplan-Nelson holographic dof for region of size L (in meters).

    Saturation form: N ~ (L / l_P)^{3/2}, derived from
    rho_vac * L^4 <= M_P^2 * L^2 with one quantum per Compton cell.
    """
    return (np.asarray(L_m) / l_P) ** 1.5


def N_Bek(R_m: np.ndarray | float, M_kg: np.ndarray | float) -> np.ndarray | float:
    """Bekenstein bound N ~ 2 pi R M c / (hbar ln 2)."""
    R = np.asarray(R_m)
    M = np.asarray(M_kg)
    return 2.0 * np.pi * R * M * c / (hbar * ln2)


def N_BH(R_m: np.ndarray | float) -> np.ndarray | float:
    """Black-hole holographic ceiling on the Bekenstein side: N ~ pi (R/l_P)^2."""
    R = np.asarray(R_m)
    return np.pi * (R / l_P) ** 2


def crossing_mass(L_m: np.ndarray) -> np.ndarray:
    """Mass M*(L) at which N_CKN(L) = N_Bek(L, M)."""
    # (L/l_P)^{3/2} = 2 pi L M c / (hbar ln 2)
    # M = (hbar ln2) / (2 pi L c) * (L/l_P)^{3/2}
    return (hbar * ln2) / (2.0 * np.pi * L_m * c) * (L_m / l_P) ** 1.5


def interference_suppression(L_m: float, M_kg: float, w: float = 0.5) -> float:
    """Speculative destructive-interference factor on sigma_0.

    S = 1 - exp(-(log10 T)^2 / w^2),
    so S -> 0 (full suppression) when T = N_CKN/N_Bek = 1, and
    S -> 1 (no suppression) far from crossing.
    """
    T = N_CKN(L_m) / N_Bek(L_m, M_kg)
    return 1.0 - np.exp(-(np.log10(T)) ** 2 / w ** 2)


def report():
    print("=" * 72)
    print("L463  CKN x Bekenstein crossing speculation")
    print("=" * 72)
    print(f"M_P = {M_P:.3e} kg     l_P = {l_P:.3e} m")

    # crossing curve over scales spanning galaxy -> Hubble
    L_grid = np.logspace(np.log10(1e-3 * Mpc), np.log10(4.4e3 * Mpc), 9)
    print()
    print(f"{'L [Mpc]':>12}  {'M*(L) [Msun]':>16}  {'log10 T(L,M*)':>15}")
    for L in L_grid:
        M_star = crossing_mass(L)
        T = N_CKN(L) / N_Bek(L, M_star)
        print(f"{L/Mpc:12.3e}  {M_star/Msun:16.3e}  {np.log10(T):15.3e}")

    print()
    print("Astrophysical anchors (R, M) and how close they sit to the crossing")
    anchors = [
        ("Milky Way disk",      15.0e-3 * Mpc, 1.0e12 * Msun),
        ("Galaxy group",        0.5 * Mpc,     5.0e13 * Msun),
        ("Cluster (Virgo)",     2.0 * Mpc,     1.2e15 * Msun),
        ("Cluster (Coma)",      3.0 * Mpc,     1.5e15 * Msun),
        ("Massive cluster",     2.5 * Mpc,     2.0e15 * Msun),
        ("Supercluster",       50.0 * Mpc,     1.0e17 * Msun),
        ("Hubble volume",     4400.0 * Mpc,    1.0e23 * Msun),
    ]
    print(f"{'name':>22}  {'R [Mpc]':>10}  {'M [Msun]':>12}  "
          f"{'log10 T':>10}  {'S(supp)':>10}")
    for name, R, M in anchors:
        T = N_CKN(R) / N_Bek(R, M)
        S = interference_suppression(R, M, w=0.5)
        print(f"{name:>22}  {R/Mpc:10.2f}  {M/Msun:12.2e}  "
              f"{np.log10(T):10.3f}  {S:10.4f}")

    print()
    print("Reading: |log10 T| close to 0 => crossing => S small => sigma_0 dip.")
    print("Speculation only. Coefficients order-unity, not fit to anything.")


if __name__ == "__main__":
    report()
