"""
L484 — Cluster scaling relations test.

Mandate:
- M-T_X, M-Y_X, M-sigma_v scaling relations.
- Compare SQT depletion-zone prediction vs LCDM (self-similar) prediction.
- Reference: Kravtsov & Borgani 2012 ARA&A; Kravtsov 2018 review.
- Data: SPT-SZ (Bocquet+ 2019), Planck PSZ2 (Planck 2016 XXIV) — published
  best-fit values used as "synthetic-from-published" inputs (no MCMC, no chi2
  fit per CLAUDE.md L33+ rules; just relation-level comparison).

Honest one-liner output:
- LCDM self-similar predicts slopes (3/2, 5/3, 1/3) for (T,Y,sigma_v).
- SQT depletion-zone effect: gravitational depletion at sigma_cluster scale
  introduces a mass-dependent correction f_dep(M) = 1 + delta(M) where
  delta(M) is the SQT prediction. We model this *qualitatively* — coefficients
  are placeholders. CLAUDE.md forbids prefactor specification.

This script writes:
  results/L484/scaling_table.tsv  — relation slopes and normalisations
  results/L484/scaling_relations.png — diagnostic plot (if matplotlib available)
"""

from __future__ import annotations

import os

import numpy as np


# -----------------------------------------------------------------------------
# Self-similar (LCDM) scaling — Kaiser 1986 / Kravtsov & Borgani 2012.
# Relations are written for E(z) M_500 vs observable.
# -----------------------------------------------------------------------------

def lcdm_M_TX(T_keV: np.ndarray) -> np.ndarray:
    """E(z) M_500c vs T_X [keV]. Self-similar slope = 3/2.
    Vikhlinin+ 2009 / Mantz+ 2016: M_500 ~ 3.0e14 Msun at T = 5 keV.
    Returns mass in 10^13 Msun units (so axis matches plot)."""
    A_e14 = 3.02  # 10^14 Msun at T=5 keV (Vikhlinin+ 2009)
    alpha = 3.0 / 2.0
    return A_e14 * (T_keV / 5.0) ** alpha * 10.0  # in 10^13 Msun


def lcdm_M_YX(YX: np.ndarray) -> np.ndarray:
    """E(z)^(2/5) M_500c vs Y_X = M_gas * T_X [10^13 Msun keV]. Slope = 3/5.
    Norm from Kravtsov+ 2006: A_YX ~ 5.77 (10^14 Msun)."""
    A = 5.77
    alpha = 3.0 / 5.0
    return A * (YX / 3.0) ** alpha


def lcdm_M_sigv(sigv_kms: np.ndarray) -> np.ndarray:
    """M_200c vs sigma_v. Self-similar slope = 3 (M ~ sigma^3).
    Evrard+ 2008: sigma_DM = 1082.9 (h(z) M_200/1e15)^0.3361 km/s
    -> inverted: M ~ sigma^(1/0.3361) ~ sigma^2.975."""
    A = 1.0  # 10^15 Msun at sigv = 1082.9
    alpha = 1.0 / 0.3361
    return A * (sigv_kms / 1082.9) ** alpha  # in 10^15 Msun


# -----------------------------------------------------------------------------
# SQT depletion-zone correction.
# CLAUDE.md compliance: NO numerical prefactor commitment. We expose a single
# "amplitude placeholder" `eps` to be derived independently by the team.
# Functional form: depletion fraction g(M) localised around M_dep.
# -----------------------------------------------------------------------------

def sqt_depletion_correction(M_e14: np.ndarray, eps: float, M_dep: float, w: float) -> np.ndarray:
    """Multiplicative depletion correction f(M) = 1 - eps * sech^2((lnM - lnM_dep)/w).

    eps : amplitude placeholder (sign convention: positive = depletion -> mass-deficit)
    M_dep : zone centre (10^14 Msun)
    w : log-width
    """
    x = (np.log(M_e14) - np.log(M_dep)) / w
    return 1.0 - eps * (1.0 / np.cosh(x)) ** 2


def sqt_M_TX(T_keV: np.ndarray, eps: float, M_dep: float, w: float) -> np.ndarray:
    M_lcdm = lcdm_M_TX(T_keV)  # 10^13 Msun
    f = sqt_depletion_correction(M_lcdm / 10.0, eps, M_dep, w)
    return M_lcdm * f


def sqt_M_YX(YX: np.ndarray, eps: float, M_dep: float, w: float) -> np.ndarray:
    M_lcdm = lcdm_M_YX(YX)  # 10^14 Msun
    f = sqt_depletion_correction(M_lcdm, eps, M_dep, w)
    return M_lcdm * f


def sqt_M_sigv(sigv_kms: np.ndarray, eps: float, M_dep: float, w: float) -> np.ndarray:
    M_lcdm = lcdm_M_sigv(sigv_kms)  # 10^15 Msun
    f = sqt_depletion_correction(M_lcdm * 10.0, eps, M_dep, w)
    return M_lcdm * f


# -----------------------------------------------------------------------------
# Published data anchor points (synthetic-from-literature).
# - SPT-SZ Bocquet+ 2019 ApJ 878 55: ~377 clusters, M_500 ~ 4-12 x10^14 Msun
# - Planck PSZ2 (Planck 2016 XXIV): ~439 confirmed.
# - Vikhlinin+ 2009: M-T calibration sample.
# - Sifón+ 2016: M-sigma_v cluster sample.
# Single representative anchor per relation, used for sanity check only.
# -----------------------------------------------------------------------------

ANCHORS = {
    "M_TX": {
        "T_keV": 6.0,
        "M_500_e14_obs": 4.5,  # Vikhlinin+ 2009 fig 4 trend at T=6 keV
        "M_500_err": 0.5,
    },
    "M_YX": {
        "YX_e13_keV": 5.0,
        "M_500_e14_obs": 7.5,  # Kravtsov+ 2006 fit
        "M_500_err": 0.7,
    },
    "M_sigv": {
        "sigv_kms": 1000.0,
        "M_200_e15_obs": 0.78,  # Sifón+ 2016, Evrard+ 2008
        "M_200_err": 0.10,
    },
}


def main() -> None:
    out_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "results",
        "L484",
    )
    os.makedirs(out_dir, exist_ok=True)

    # Placeholder SQT parameters — NOT a fit, NOT a prediction.
    # Team must derive eps, M_dep, w independently.
    eps = 0.05  # placeholder amplitude — CLAUDE.md: prefactor unspecified.
    M_dep = 3.0  # 10^14 Msun — depletion zone centre placeholder
    w = 0.6  # log-width placeholder

    # Range scans
    T = np.logspace(np.log10(2.0), np.log10(15.0), 50)
    YX = np.logspace(np.log10(0.5), np.log10(30.0), 50)
    sigv = np.logspace(np.log10(500.0), np.log10(1500.0), 50)

    M_T_lcdm = lcdm_M_TX(T)
    M_T_sqt = sqt_M_TX(T, eps, M_dep, w)
    M_Y_lcdm = lcdm_M_YX(YX)
    M_Y_sqt = sqt_M_YX(YX, eps, M_dep, w)
    M_s_lcdm = lcdm_M_sigv(sigv)
    M_s_sqt = sqt_M_sigv(sigv, eps, M_dep, w)

    # Anchor-level deviation report (not chi2 — relation-level only)
    rows = ["# relation\tobs_value\tLCDM_pred\tSQT_pred\tdev_LCDM_sigma\tdev_SQT_sigma"]

    a = ANCHORS["M_TX"]
    M_lcdm = lcdm_M_TX(np.array([a["T_keV"]]))[0] / 10.0  # -> 10^14
    M_sqt = sqt_M_TX(np.array([a["T_keV"]]), eps, M_dep, w)[0] / 10.0
    rows.append(
        f"M-T_X\t{a['M_500_e14_obs']:.3f}\t{M_lcdm:.3f}\t{M_sqt:.3f}\t"
        f"{(M_lcdm - a['M_500_e14_obs']) / a['M_500_err']:.2f}\t"
        f"{(M_sqt - a['M_500_e14_obs']) / a['M_500_err']:.2f}"
    )

    a = ANCHORS["M_YX"]
    M_lcdm = lcdm_M_YX(np.array([a["YX_e13_keV"]]))[0]
    M_sqt = sqt_M_YX(np.array([a["YX_e13_keV"]]), eps, M_dep, w)[0]
    rows.append(
        f"M-Y_X\t{a['M_500_e14_obs']:.3f}\t{M_lcdm:.3f}\t{M_sqt:.3f}\t"
        f"{(M_lcdm - a['M_500_e14_obs']) / a['M_500_err']:.2f}\t"
        f"{(M_sqt - a['M_500_e14_obs']) / a['M_500_err']:.2f}"
    )

    a = ANCHORS["M_sigv"]
    M_lcdm = lcdm_M_sigv(np.array([a["sigv_kms"]]))[0]
    M_sqt = sqt_M_sigv(np.array([a["sigv_kms"]]), eps, M_dep, w)[0]
    rows.append(
        f"M-sigma_v\t{a['M_200_e15_obs']:.3f}\t{M_lcdm:.3f}\t{M_sqt:.3f}\t"
        f"{(M_lcdm - a['M_200_e15_obs']) / a['M_200_err']:.2f}\t"
        f"{(M_sqt - a['M_200_e15_obs']) / a['M_200_err']:.2f}"
    )

    # Slope diagnostics
    def slope(x, y):
        return np.polyfit(np.log(x), np.log(y), 1)[0]

    rows.append("")
    rows.append("# log-log slope diagnostics")
    rows.append(f"# M-T_X    slope LCDM = {slope(T, M_T_lcdm):.4f}  (self-similar 1.50)")
    rows.append(f"# M-T_X    slope SQT  = {slope(T, M_T_sqt):.4f}")
    rows.append(f"# M-Y_X    slope LCDM = {slope(YX, M_Y_lcdm):.4f}  (self-similar 0.60)")
    rows.append(f"# M-Y_X    slope SQT  = {slope(YX, M_Y_sqt):.4f}")
    rows.append(f"# M-sigv   slope LCDM = {slope(sigv, M_s_lcdm):.4f}  (Evrard+ 2.975)")
    rows.append(f"# M-sigv   slope SQT  = {slope(sigv, M_s_sqt):.4f}")

    table_path = os.path.join(out_dir, "scaling_table.tsv")
    with open(table_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rows))
    print("L484 scaling table:", table_path)
    for r in rows:
        print(r)

    # Plot
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

        axes[0].loglog(T, M_T_lcdm, "k-", label="LCDM self-similar")
        axes[0].loglog(T, M_T_sqt, "r--", label=f"SQT depl. (eps={eps} placeholder)")
        a = ANCHORS["M_TX"]
        axes[0].errorbar([a["T_keV"]], [a["M_500_e14_obs"] * 10.0],
                         yerr=[a["M_500_err"] * 10.0], fmt="bo", label="Vikhlinin+09 anchor")
        axes[0].set_xlabel("T_X [keV]")
        axes[0].set_ylabel("E(z) M_500c [10^13 Msun]")
        axes[0].set_title("M - T_X")
        axes[0].legend(fontsize=8)

        axes[1].loglog(YX, M_Y_lcdm, "k-", label="LCDM self-similar")
        axes[1].loglog(YX, M_Y_sqt, "r--", label="SQT depletion")
        a = ANCHORS["M_YX"]
        axes[1].errorbar([a["YX_e13_keV"]], [a["M_500_e14_obs"]],
                         yerr=[a["M_500_err"]], fmt="bo", label="Kravtsov+06 anchor")
        axes[1].set_xlabel("Y_X [10^13 Msun keV]")
        axes[1].set_ylabel("E(z)^(2/5) M_500c [10^14 Msun]")
        axes[1].set_title("M - Y_X")
        axes[1].legend(fontsize=8)

        axes[2].loglog(sigv, M_s_lcdm, "k-", label="LCDM self-similar")
        axes[2].loglog(sigv, M_s_sqt, "r--", label="SQT depletion")
        a = ANCHORS["M_sigv"]
        axes[2].errorbar([a["sigv_kms"]], [a["M_200_e15_obs"]],
                         yerr=[a["M_200_err"]], fmt="bo", label="Evrard+08/Sifon+16")
        axes[2].set_xlabel("sigma_v [km/s]")
        axes[2].set_ylabel("h(z) M_200c [10^15 Msun]")
        axes[2].set_title("M - sigma_v")
        axes[2].legend(fontsize=8)

        fig.suptitle(
            "L484 - cluster scaling relations: SQT depletion vs LCDM self-similar"
            "  (placeholder amplitudes; team derives independently)"
        )
        fig.tight_layout()
        fig_path = os.path.join(out_dir, "scaling_relations.png")
        fig.savefig(fig_path, dpi=120)
        plt.close(fig)
        print("L484 plot:", fig_path)
    except Exception as exc:  # noqa: BLE001
        print("matplotlib unavailable, skipping plot:", exc)

    print(
        "L484 done. Honest line: SQT placeholder eps={:.3f} produces "
        "<{:.1f}% deviation from LCDM in 2-15 keV cluster range; "
        "current data error bars (~10%) cannot distinguish.".format(eps, eps * 100)
    )


if __name__ == "__main__":
    main()
