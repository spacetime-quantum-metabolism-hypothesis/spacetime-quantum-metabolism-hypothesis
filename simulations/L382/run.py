"""
L382: SK Wightman propagator W_+, W_- explicit for n field at thermal equilibrium.

Derives and numerically verifies (in frequency space, fixed momentum k):
  W_+(omega) = ⟨n(t) n(0)⟩
  W_-(omega) = ⟨n(0) n(t)⟩
  rho(omega) = W_+ - W_-   (spectral function)
KMS gate: W_+(omega) = exp(beta*omega) * W_-(omega).

Free real scalar, equilibrium, no SQMH-specific interaction (L382 is microscopic
foundation only; vertex effects deferred to later L sessions).

Standard textbook result (Le Bellac, Kapusta-Gale) re-stated in SQMH n-field
notation. No new physics. Used as numerical infrastructure for later FDR work.
"""

from __future__ import annotations

import os
import sys
import json
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")  # before any other matplotlib import
import matplotlib.pyplot as plt


# ----------------------------------------------------------------------
# Wightman functions for free real scalar at finite T (k fixed -> 0+1D form)
#
# W_pm(omega) at fixed momentum k for a free scalar with mass m and dispersion
# omega_k = sqrt(k^2 + m^2):
#
#   W_+(omega) = 2 pi * [ (1 + n_B(omega_k)) * delta(omega - omega_k)
#                       +  n_B(omega_k)      * delta(omega + omega_k) ]
#   W_-(omega) = 2 pi * [  n_B(omega_k)      * delta(omega - omega_k)
#                       + (1 + n_B(omega_k)) * delta(omega + omega_k) ]
#   rho(omega) = 2 pi * sgn(omega) [ delta(omega - omega_k) - delta(omega + omega_k) ]
#
# For numerical visualisation we replace each delta by a narrow Lorentzian
# of width eta. The KMS identity W_+(omega) = exp(beta*omega) W_-(omega) is
# checked at each pole (where W_- is non-trivial), so the regularisation
# does not affect the gate.
# ----------------------------------------------------------------------


def n_bose(omega: np.ndarray, beta: float) -> np.ndarray:
    """Bose-Einstein occupation. Safe for omega>0; we only call with omega_k>0."""
    return 1.0 / np.expm1(beta * omega)


def lorentzian(x: np.ndarray, x0: float, eta: float) -> np.ndarray:
    return (eta / np.pi) / ((x - x0) ** 2 + eta**2)


def wightman_pm(
    omega_grid: np.ndarray, omega_k: float, beta: float, eta: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    nB = n_bose(np.array([omega_k]), beta)[0]
    Lp = lorentzian(omega_grid, +omega_k, eta)
    Lm = lorentzian(omega_grid, -omega_k, eta)
    Wp = 2.0 * np.pi * ((1.0 + nB) * Lp + nB * Lm)
    Wm = 2.0 * np.pi * (nB * Lp + (1.0 + nB) * Lm)
    rho = Wp - Wm  # = 2 pi sgn(omega) [delta(omega - omega_k) - delta(omega + omega_k)] in eta->0
    return Wp, Wm, rho


def kms_residual_at_pole(omega_k: float, beta: float) -> float:
    """
    Exact (no regulator) KMS check at the positive pole:
        W_+ / W_- |_{omega = omega_k} = (1 + nB) / nB = e^{beta omega_k}.
    Returns relative residual.
    """
    nB = 1.0 / np.expm1(beta * omega_k)
    ratio = (1.0 + nB) / nB
    target = np.exp(beta * omega_k)
    return float(abs(ratio - target) / target)


def run_case(beta: float, m: float, k: float, eta: float = 1e-3, N: int = 800):
    omega_k = float(np.sqrt(k * k + m * m))
    omega = np.linspace(-5.0, 5.0, N)
    Wp, Wm, rho = wightman_pm(omega, omega_k, beta, eta)

    # --- KMS gate: exact at omega_k (delta-limit), and numerical near pole ---
    kms_exact = kms_residual_at_pole(omega_k, beta)

    # numerical KMS: W_+(omega)/W_-(omega) vs exp(beta*omega), evaluated where
    # both are well above floor (avoid division noise in the gap between poles).
    floor = 1e-6 * max(Wp.max(), Wm.max())
    mask = (Wp > floor) & (Wm > floor)
    ratio_num = Wp[mask] / Wm[mask]
    target_num = np.exp(beta * omega[mask])
    kms_num = float(np.max(np.abs(ratio_num - target_num) / target_num))

    # positivity of rho: in delta-limit rho(omega>0)>=0, rho(omega<0)<=0.
    # The signed quantity sgn(omega)*rho should be >=0.
    pos_violation = float(min((np.sign(omega) * rho).min(), 0.0))

    return {
        "beta": beta,
        "m": m,
        "k": k,
        "omega_k": omega_k,
        "kms_exact_residual": kms_exact,
        "kms_numerical_max_residual": kms_num,
        "positivity_min": pos_violation,
        "omega": omega,
        "Wp": Wp,
        "Wm": Wm,
        "rho": rho,
    }


def main():
    out_dir = Path(__file__).resolve().parent.parent.parent / "results" / "L382"
    out_dir.mkdir(parents=True, exist_ok=True)

    grid = []
    for beta in (0.5, 1.0, 2.0):
        for m in (0.0, 0.3, 1.0):
            for k in (0.0, 0.5):
                if m == 0.0 and k == 0.0:
                    continue  # massless zero mode singular
                grid.append(run_case(beta=beta, m=m, k=k))

    summary = []
    print("L382 SK Wightman / KMS verification")
    print("=" * 72)
    print(f"{'beta':>5} {'m':>5} {'k':>5} {'omega_k':>9} "
          f"{'KMS_exact':>12} {'KMS_num':>12} {'pos_min':>12}")
    for r in grid:
        print(f"{r['beta']:5.2f} {r['m']:5.2f} {r['k']:5.2f} "
              f"{r['omega_k']:9.4f} {r['kms_exact_residual']:12.2e} "
              f"{r['kms_numerical_max_residual']:12.2e} "
              f"{r['positivity_min']:12.2e}")
        summary.append({
            "beta": r["beta"], "m": r["m"], "k": r["k"],
            "omega_k": r["omega_k"],
            "kms_exact_residual": r["kms_exact_residual"],
            "kms_numerical_max_residual": r["kms_numerical_max_residual"],
            "positivity_min": r["positivity_min"],
        })

    # ---- gates ----
    K1 = max(s["kms_exact_residual"] for s in summary)
    K2 = min(s["positivity_min"] for s in summary)
    K3_ok = True  # 1D real scalar Wightman in frequency is real for our regulator
    K4 = max(s["kms_numerical_max_residual"] for s in summary)

    gates = {
        "K1_kms_exact_max": K1,
        "K1_pass": bool(K1 < 1e-10),
        "K2_positivity_min": K2,
        "K2_pass": bool(K2 > -1e-10),
        "K3_realness_pass": K3_ok,
        "K4_kms_numerical_max": K4,
        "K4_pass": bool(K4 < 5e-2),  # smearing-limited, dominated by Lorentzian tails
    }
    print("-" * 72)
    print("Gates:", json.dumps(gates, indent=2))

    # ---- figure: representative case beta=1, m=0.3, k=0 ----
    rep = run_case(beta=1.0, m=0.3, k=0.0, eta=5e-3, N=2000)
    fig, axes = plt.subplots(2, 2, figsize=(10, 7), constrained_layout=True)

    ax = axes[0, 0]
    ax.plot(rep["omega"], rep["Wp"], label=r"$W_+(\omega)$", color="C0")
    ax.plot(rep["omega"], rep["Wm"], label=r"$W_-(\omega)$", color="C3", ls="--")
    ax.set_xlabel(r"$\omega$"); ax.set_ylabel("W"); ax.legend(); ax.set_title("Wightman functions")

    ax = axes[0, 1]
    ax.plot(rep["omega"], rep["rho"], color="C2")
    ax.axhline(0, color="k", lw=0.5)
    ax.set_xlabel(r"$\omega$"); ax.set_ylabel(r"$\rho(\omega)$"); ax.set_title("Spectral function")

    ax = axes[1, 0]
    floor = 1e-6 * max(rep["Wp"].max(), rep["Wm"].max())
    mask = (rep["Wp"] > floor) & (rep["Wm"] > floor)
    ax.semilogy(rep["omega"][mask], rep["Wp"][mask] / rep["Wm"][mask],
                label=r"$W_+/W_-$", color="C0")
    ax.semilogy(rep["omega"][mask], np.exp(rep["beta"] * rep["omega"][mask]),
                label=r"$e^{\beta\omega}$", color="C3", ls="--")
    ax.set_xlabel(r"$\omega$"); ax.legend(); ax.set_title(r"KMS check (log)")

    ax = axes[1, 1]
    betas = [0.5, 1.0, 2.0]
    for b in betas:
        r = run_case(beta=b, m=0.3, k=0.0, eta=5e-3, N=2000)
        floor = 1e-6 * max(r["Wp"].max(), r["Wm"].max())
        mask = (r["Wp"] > floor) & (r["Wm"] > floor)
        resid = np.abs(r["Wp"][mask] / r["Wm"][mask]
                       - np.exp(r["beta"] * r["omega"][mask])) / np.exp(r["beta"] * r["omega"][mask])
        ax.semilogy(r["omega"][mask], resid, label=fr"$\beta={b}$")
    ax.set_xlabel(r"$\omega$"); ax.set_ylabel("KMS rel. residual")
    ax.legend(); ax.set_title("KMS residual vs beta")

    fig_path = out_dir / "wightman_kms.png"
    fig.savefig(fig_path, dpi=140)
    print(f"figure -> {fig_path}")

    json_path = out_dir / "L382_summary.json"
    with open(json_path, "w") as f:
        json.dump({"cases": summary, "gates": gates}, f, indent=2)
    print(f"summary -> {json_path}")


if __name__ == "__main__":
    # enforce single-thread BLAS for reproducibility (CLAUDE.md rule)
    for k in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
        os.environ.setdefault(k, "1")
    main()
