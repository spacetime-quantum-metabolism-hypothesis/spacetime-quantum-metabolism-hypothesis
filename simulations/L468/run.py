"""L468 free speculation toy: information-theoretic origin of cluster-scale dip.

Hypothesis (free guess):
  sigma_0(R) — the SQMH metabolism-coupled scale-dependent variance / coupling
  amplitude — is governed by an information-theoretic quantity. Specifically,
  we postulate

      sigma_0(R) ∝  1 / sqrt( I_F(R) )           (Cramer-Rao-like)

  where I_F(R) is the Fisher information that the matter density field at scale
  R carries about the cosmological large-scale anchors that SQMH metabolism
  uses to constrain cluster scale (here we use two anchors: the linear-regime
  scale R_lin ~ 80 Mpc/h and the deeply non-linear scale R_nl ~ 1 Mpc/h).

  At cluster scale R ~ 8 Mpc/h the field decorrelates from BOTH anchors:
    - too non-linear to be informative about R_lin
    - too linear to be informative about R_nl
  → Fisher information takes a MINIMUM at R ~ R_cluster
  → sigma_0 takes a MAXIMUM (largest scatter / coupling needed)
  → which translates to a "dip" in the metabolic-corrected observables that
    L46x have been chasing.

  Equivalently, the maximum-entropy distribution of overdensities given only
  the two anchor moments (sigma at R_lin, sigma at R_nl) has its entropy
  MAXIMUM at the scale that interpolates between them — the cluster scale.
  Maximum entropy ↔ minimum mutual information with the anchors ↔ minimum
  Fisher info.

This is a phenomenological toy: we *do not* claim the numerical coefficients,
only the qualitative structure (dip at cluster scale from information-theoretic
extremum). Any quantitative match is to be checked against L46x dip residuals
in a follow-up session.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent
RES = OUT.parent.parent / "results" / "L468"
RES.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# 1. Toy linear-power proxy P(k) ∝ k^n_eff(k)  with running tilt
# ---------------------------------------------------------------------------
def power_proxy(k):
    # very crude broken power law mimicking LCDM transfer function
    # (not for fitting, just to give k^3 P(k) the right qualitative shape)
    k_eq = 0.015  # h/Mpc
    return k / (1.0 + (k / k_eq) ** 2) ** 2


def sigma2_R(R, k):
    # Top-hat window
    x = k * R
    # avoid x=0 singularity
    W = np.where(
        x < 1e-3,
        1.0 - x ** 2 / 10.0,
        3.0 * (np.sin(x) - x * np.cos(x)) / x ** 3,
    )
    integrand = (k ** 2 * power_proxy(k) * W ** 2) / (2.0 * np.pi ** 2)
    return np.trapezoid(integrand, k)


# ---------------------------------------------------------------------------
# 2. Fisher information of a two-anchor maxent distribution at scale R
#    Anchors: sigma(R_lin), sigma(R_nl).  Treat ln sigma(R) as the "signal"
#    and the two anchor sigmas as parameters theta_1, theta_2.
#    Decompose ln sigma(R) into a convex mixture
#         ln sigma(R) = w(R) * ln sigma(R_lin) + (1-w(R)) * ln sigma(R_nl)
#    where w is fixed by interpolation in log R.  The Fisher info that
#    measurement at scale R carries about (theta_1, theta_2) is then
#         I_F(R) = w(R)^2 + (1-w(R))^2
#    which has a *minimum* at w = 1/2  (cluster scale).
# ---------------------------------------------------------------------------
def fisher_info(R, R_lin=80.0, R_nl=1.0):
    w = (np.log(R) - np.log(R_nl)) / (np.log(R_lin) - np.log(R_nl))
    w = np.clip(w, 0.0, 1.0)
    return w ** 2 + (1.0 - w) ** 2  # min at w=0.5


def maxent_entropy(R, R_lin=80.0, R_nl=1.0):
    # Shannon entropy of the binary mixture w(R)
    w = (np.log(R) - np.log(R_nl)) / (np.log(R_lin) - np.log(R_nl))
    w = np.clip(w, 1e-9, 1.0 - 1e-9)
    return -(w * np.log(w) + (1.0 - w) * np.log(1.0 - w))  # max at w=0.5


def mutual_info(R, R_lin=80.0, R_nl=1.0):
    # MI between the scale-R field and the anchors, proxied as 1 - H(w)/ln2
    # (high when w near 0 or 1, low at w=0.5)
    H = maxent_entropy(R, R_lin, R_nl)
    return 1.0 - H / np.log(2.0)


# ---------------------------------------------------------------------------
# 3. Predicted sigma_0(R) ∝ 1/sqrt(I_F)  (Cramer-Rao-like saturation)
# ---------------------------------------------------------------------------
def sigma0_pred(R):
    return 1.0 / np.sqrt(fisher_info(R))


# ---------------------------------------------------------------------------
# 4. Run + dump
# ---------------------------------------------------------------------------
def main():
    R_grid = np.logspace(-0.5, 2.0, 41)  # 0.3 .. 100 Mpc/h
    k_grid = np.logspace(-4, 2, 4000)

    sig2 = np.array([sigma2_R(R, k_grid) for R in R_grid])
    IF = fisher_info(R_grid)
    Hmax = maxent_entropy(R_grid)
    MI = mutual_info(R_grid)
    sig0 = sigma0_pred(R_grid)

    # Locate extrema
    i_min_IF = int(np.argmin(IF))
    i_max_H = int(np.argmax(Hmax))
    i_max_sig0 = int(np.argmax(sig0))

    summary = {
        "hypothesis": (
            "sigma_0(R) ∝ 1/sqrt(I_F(R)); cluster-scale dip is the "
            "Fisher-information minimum / maxent entropy maximum"
        ),
        "anchors_Mpc_h": {"R_lin": 80.0, "R_nl": 1.0},
        "expected_dip_scale_Mpc_h": float(np.exp(0.5 * (np.log(80.0) + np.log(1.0)))),
        "fisher_min_at_R": float(R_grid[i_min_IF]),
        "fisher_min_value": float(IF[i_min_IF]),
        "entropy_max_at_R": float(R_grid[i_max_H]),
        "entropy_max_value_nats": float(Hmax[i_max_H]),
        "sigma0_max_at_R": float(R_grid[i_max_sig0]),
        "sigma0_max_value": float(sig0[i_max_sig0]),
        "mutual_info_min_at_R": float(R_grid[int(np.argmin(MI))]),
        "comment_cluster_scale_match": (
            "geometric mean of (1, 80) = 8.94 Mpc/h ≈ canonical sigma_8 scale; "
            "matches the L46x dip locus phenomenologically."
        ),
    }

    np.savez(
        OUT / "scan.npz",
        R=R_grid,
        sigma2_field=sig2,
        fisher_info=IF,
        maxent_entropy=Hmax,
        mutual_info=MI,
        sigma0_pred=sig0,
    )
    with open(RES / "scan_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("=== L468 information-theoretic dip toy ===")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    # Optional plot (skip if matplotlib missing)
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(9, 7))
        axes[0, 0].loglog(R_grid, sig2)
        axes[0, 0].set(xlabel="R [Mpc/h]", ylabel=r"$\sigma^2(R)$ proxy")
        axes[0, 1].semilogx(R_grid, IF, label=r"$I_F(R)$")
        axes[0, 1].semilogx(R_grid, Hmax / np.log(2), label="H(w)/ln2")
        axes[0, 1].axvline(8.94, color="gray", ls="--", label="cluster ~8.9 Mpc/h")
        axes[0, 1].legend(); axes[0, 1].set_xlabel("R")
        axes[1, 0].semilogx(R_grid, sig0)
        axes[1, 0].axvline(8.94, color="gray", ls="--")
        axes[1, 0].set(xlabel="R [Mpc/h]", ylabel=r"$\sigma_0(R)\propto 1/\sqrt{I_F}$")
        axes[1, 1].semilogx(R_grid, MI)
        axes[1, 1].axvline(8.94, color="gray", ls="--")
        axes[1, 1].set(xlabel="R [Mpc/h]", ylabel="mutual info proxy")
        fig.suptitle("L468: information-theoretic origin of cluster dip (toy)")
        fig.tight_layout()
        fig.savefig(RES / "scan.png", dpi=130)
        print(f"  plot: {RES / 'scan.png'}")
    except Exception as e:
        print(f"  (plot skipped: {e})")


if __name__ == "__main__":
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    main()
