"""
L383 — Wetterich Gamma_k 1차 truncation (LPA) sigma_0 flow

Single real scalar field sigma in D-dimensional Euclidean space.
Z2-symmetric local potential approximation:

    Gamma_k[sigma] = int d^D x [ (1/2)(d sigma)^2 + U_k(sigma) ]

with Z_k = 1 (LPA, no anomalous dimension).

Flow equation (Wetterich 1993) reduced via Litim optimised cutoff
R_k(q) = (k^2 - q^2) theta(k^2 - q^2):

    dU_k/dt = (c_D / 2) k^{D+2} / (k^2 + U_k''(sigma))      [t = ln k]

with c_D = 2 / ((4 pi)^{D/2} Gamma(D/2+1)) the Litim flux constant.

Polynomial truncation U_k(sigma) = (1/2) m_k^2 sigma^2 + (1/24) lambda_k sigma^4
(symmetric phase reference; broken phase tracked via sigma_0^2 = -m^2/lambda
when m^2 < 0).

Dimensionless variables:
    rho     = (1/2) sigma^2
    rho~    = k^{2-D} Z_k rho        (Z_k=1 in LPA)
    u_k     = k^{-D} U_k
    m~^2    = k^{-2} m^2
    lam~    = k^{D-4} lambda

Outputs:
    - results/L383/lpa_flow.json        (flow trajectory + FP location)
    - results/L383/lpa_flow.png         (sigma_0(t), u(sigma_0,t))

Independence: numerical RG of dimensionless polynomial truncation; no external
SQT fits, no cosmological data, no hidden constants.

Honest one-liner: LPA is the coarsest SQT-σ flow approximation and in D=4 the
non-trivial FP collapses to Gaussian; this run sets the baseline for LPA' / DE2
extensions, nothing more.
"""

import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# -------------------------------------------------------------------- constants

def litim_constant(D: float) -> float:
    """c_D = 2 / ((4 pi)^{D/2} Gamma(D/2+1))."""
    return 2.0 / ((4.0 * math.pi) ** (D / 2.0) * math.gamma(D / 2.0 + 1.0))


# -------------------------------------------------------------------- LPA flow

def beta_polynomial(y, D: float):
    """
    Beta functions for dimensionless m~^2 and lam~ in symmetric-phase
    polynomial LPA (Z_k=1, Litim cutoff).

    Reference (textbook form, e.g. Delamotte 2007 hep-th/0702365 sec.4):
        partial_t m~^2 = -2 m~^2  - c_D * lam~ / (1 + m~^2)^2 / 2
        partial_t lam~ = (D-4) lam~ + 3 c_D * lam~^2 / (1 + m~^2)^3

    (Single-component scalar; symmetry factor for the 2-leg loop: 1/2 for m^2,
    3/2 for lambda from rho-derivative chain.)
    """
    mm, lam = y
    cD = litim_constant(D)
    denom = 1.0 + mm
    # numerical guard: regulator pole
    if denom <= 1e-6:
        denom = 1e-6
    dm = -2.0 * mm - 0.5 * cD * lam / denom**2
    dl = (D - 4.0) * lam + 3.0 * cD * lam**2 / denom**3
    return np.array([dm, dl])


def find_fixed_points(D: float):
    """Solve beta = 0 in (m~^2, lam~) plane via multi-start Newton."""
    fps = []
    starts = [
        (0.0, 0.0),
        (-0.1, 0.5),
        (-0.2, 1.0),
        (0.1, 0.1),
        (-0.5, 2.0),
        (0.5, 0.5),
    ]
    for s in starts:
        sol = root(lambda y: beta_polynomial(y, D), s, method="hybr",
                   tol=1e-12)
        if not sol.success:
            continue
        y = sol.x
        # de-duplicate
        is_new = True
        for f in fps:
            if np.linalg.norm(np.array(f) - y) < 1e-6:
                is_new = False
                break
        if is_new:
            fps.append(tuple(float(v) for v in y))
    return fps


def integrate_flow(D: float, y0, t_span=(0.0, -20.0), n_pts: int = 400):
    """Integrate from UV (t=0, k=Lambda) to IR (t<<0, k->0)."""
    sol = solve_ivp(
        lambda t, y: beta_polynomial(y, D),
        t_span,
        y0,
        method="LSODA",
        rtol=1e-9,
        atol=1e-12,
        dense_output=True,
        t_eval=np.linspace(t_span[0], t_span[1], n_pts),
    )
    if not sol.success:
        raise RuntimeError(f"flow integration failed: {sol.message}")
    return sol


def sigma0_from(mm, lam):
    """
    Dimensionless minimum position of U(sigma).
    For symmetric phase (m~^2 > 0) the minimum sits at sigma=0 -> sigma_0 = 0.
    For broken phase (m~^2 < 0): sigma_0^2 = -6 m~^2 / lam~.
    Returns sigma_0 (signed-positive convention).
    """
    out = np.zeros_like(mm)
    broken = (mm < 0.0) & (lam > 1e-12)
    out[broken] = np.sqrt(-6.0 * mm[broken] / lam[broken])
    return out


def u_at_sigma0(mm, lam):
    """Dimensionless potential value at the minimum."""
    s0 = sigma0_from(mm, lam)
    rho = 0.5 * s0 * s0
    return mm * rho + (lam / 6.0) * rho * rho


# -------------------------------------------------------------------- driver

def main():
    out_dir = Path(__file__).resolve().parent.parent.parent / "results" / "L383"
    out_dir.mkdir(parents=True, exist_ok=True)

    results = {"D_cases": {}}

    for D in (4.0, 3.0):
        c_D = litim_constant(D)
        fps = find_fixed_points(D)

        # canonical UV initial condition: small symmetric phase
        y0 = (0.05, 0.20)
        sol = integrate_flow(D, y0, t_span=(0.0, -15.0), n_pts=400)

        t = sol.t
        mm = sol.y[0]
        lam = sol.y[1]
        s0 = sigma0_from(mm, lam)
        u0 = u_at_sigma0(mm, lam)

        results["D_cases"][f"D={D}"] = {
            "litim_c_D": c_D,
            "fixed_points": fps,
            "ic_y0": list(y0),
            "t": t.tolist(),
            "m2_dimless": mm.tolist(),
            "lambda_dimless": lam.tolist(),
            "sigma0_dimless": s0.tolist(),
            "u_at_sigma0": u0.tolist(),
        }

        print(f"[D={D}] c_D = {c_D:.6e}")
        print(f"[D={D}] fixed points (m~^2, lam~):")
        for fp in fps:
            print(f"    {fp}")
        print(f"[D={D}] flow endpoints: m~^2 {mm[0]:+.4f} -> {mm[-1]:+.4f}, "
              f"lam~ {lam[0]:+.4f} -> {lam[-1]:+.4f}")

    # save JSON
    with open(out_dir / "lpa_flow.json", "w") as f:
        json.dump(results, f, indent=2)

    # plot
    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    for col, D in enumerate((4.0, 3.0)):
        rec = results["D_cases"][f"D={D}"]
        t = np.array(rec["t"])
        mm = np.array(rec["m2_dimless"])
        lam = np.array(rec["lambda_dimless"])
        s0 = np.array(rec["sigma0_dimless"])
        u0 = np.array(rec["u_at_sigma0"])

        ax = axes[0, col]
        ax.plot(t, mm, label=r"$\tilde m^2$")
        ax.plot(t, lam, label=r"$\tilde\lambda$")
        ax.set_xlabel(r"$t = \ln(k/\Lambda)$")
        ax.set_ylabel("dimensionless couplings")
        ax.set_title(f"D={D}: coupling flow")
        ax.legend()
        ax.grid(alpha=0.3)

        ax = axes[1, col]
        ax.plot(t, s0, label=r"$\tilde\sigma_0$", color="C2")
        ax.plot(t, u0, label=r"$u(\tilde\sigma_0)$", color="C3")
        ax.set_xlabel(r"$t = \ln(k/\Lambda)$")
        ax.set_title(f"D={D}: $\\sigma_0$ flow")
        ax.legend()
        ax.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(out_dir / "lpa_flow.png", dpi=130)
    plt.close(fig)

    print(f"\nwrote: {out_dir/'lpa_flow.json'}")
    print(f"wrote: {out_dir/'lpa_flow.png'}")


if __name__ == "__main__":
    main()
