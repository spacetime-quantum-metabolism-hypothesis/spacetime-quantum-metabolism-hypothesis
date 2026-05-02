"""L423 — SPARC 175 outer Tully-Fisher comparison.

Stage 1 + Stage 2 of NEXT_STEP.md (4인 자율 분담 실행).

Tests whether the SPARC outer-region asymptote V_flat satisfies
the deep-MOND / SQT-limit form V^4 ~ G * M_bar * a0 vs a free
generalisation V^n ~ K * M_bar^m.

Inputs:
  - simulations/l49/data/sparc_catalog.mrt (catalog with Vflat, e_Vflat, Q)
  - simulations/l49/data/sparc/*_rotmod.dat (rotation curves)

Outputs:
  - results/L423/L423_results.json
  - figures/L423_tully_fisher.png

ASCII-only prints (cp949 safe).
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import least_squares

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
SPARC_CAT = ROOT / "simulations" / "l49" / "data" / "sparc_catalog.mrt"
SPARC_DIR = ROOT / "simulations" / "l49" / "data" / "sparc"
OUT_JSON = ROOT / "results" / "L423" / "L423_results.json"
OUT_FIG = ROOT / "figures" / "L423_tully_fisher.png"
OUT_FIG.parent.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# Constants (SI; we work in km/s, Msun, kpc and convert when needed)
# -----------------------------------------------------------------------------
G_KMS_KPC_MSUN = 4.30091e-6  # G in (km/s)^2 * kpc / Msun
A0_MOND_MS2 = 1.2e-10        # m/s^2  (Begeman et al 1991)
KPC_M = 3.0857e19
A0_KMS_KPC = A0_MOND_MS2 * KPC_M / 1.0e6  # to (km/s)^2 / kpc


# -----------------------------------------------------------------------------
# Catalog parser (fixed-width MRT, byte ranges per header)
# -----------------------------------------------------------------------------
def parse_catalog(path: Path) -> list[dict]:
    """Parse SPARC Table1 MRT by whitespace split.

    Data section starts after the LAST '----' separator. Each data line has
    19 fields:
      name T D eD fD Inc eInc L36 eL36 Reff SBeff Rdisk SBdisk MHI RHI
      Vflat eVflat Q Ref
    """
    rows: list[dict] = []
    with path.open() as fh:
        lines = fh.readlines()
    # locate last '------' separator
    last_sep = max(i for i, l in enumerate(lines) if l.startswith("------"))
    for line in lines[last_sep + 1:]:
        toks = line.split()
        if len(toks) < 18:
            continue
        try:
            name = toks[0]
            T = int(toks[1])
            D = float(toks[2])
            L36 = float(toks[7])
            MHI = float(toks[13])
            Vflat = float(toks[15])
            e_Vflat = float(toks[16])
            Q = int(toks[17])
        except (ValueError, IndexError):
            continue
        rows.append(
            dict(name=name, T=T, D=D, L36=L36, MHI=MHI,
                 Vflat=Vflat, e_Vflat=e_Vflat, Q=Q)
        )
    return rows


# -----------------------------------------------------------------------------
# Rotation curve loader -> outer baryonic mass M(<R_out)
# -----------------------------------------------------------------------------
def load_rotmod(path: Path) -> np.ndarray:
    arr = np.loadtxt(path, comments="#")
    # cols: Rad Vobs errV Vgas Vdisk Vbul SBdisk SBbul
    return arr


def outer_mass_from_rc(rc: np.ndarray, upsilon_disk: float = 0.5,
                      upsilon_bul: float = 0.7) -> tuple[float, float, float]:
    """Return (R_out [kpc], V_obs_out [km/s], M_bar(<R_out) [Msun]).

    M_bar(<R) is built from quadrature of component contributions:
       V_bar^2 = V_gas|V_gas| + Y_d * V_disk|V_disk| + Y_b * V_bul|V_bul|
    SPARC publishes V_disk, V_bul at Y=1; gas already physical. The bar
    around |.| handles negative V_disk (counter-rotating disk solutions).
    Then M_bar(<R) = V_bar^2 * R / G.
    """
    R = rc[:, 0]
    Vgas = rc[:, 3]
    Vdisk = rc[:, 4]
    Vbul = rc[:, 5]
    # Outer point = last radius
    i = -1
    R_out = float(R[i])
    Vbar2 = (Vgas[i] * abs(Vgas[i])
             + upsilon_disk * Vdisk[i] * abs(Vdisk[i])
             + upsilon_bul * Vbul[i] * abs(Vbul[i]))
    if Vbar2 <= 0:
        return R_out, float(rc[i, 1]), float("nan")
    Mbar = Vbar2 * R_out / G_KMS_KPC_MSUN
    return R_out, float(rc[i, 1]), Mbar


# -----------------------------------------------------------------------------
# Models
# -----------------------------------------------------------------------------
def fit_model_A(M: np.ndarray, V: np.ndarray, sigma_lnV: np.ndarray
                ) -> tuple[float, float]:
    """Fixed (n=4, m=1): V^4 = G * M * a0_eff. Solve for a0_eff via WLS in ln.

    ln V = 0.25 * ln(G M) + 0.25 * ln(a0_eff)
    -> intercept c = 0.25 ln(a0_eff)
    """
    y = np.log(V)
    x = 0.25 * np.log(G_KMS_KPC_MSUN * M)  # in (km/s)^2 / kpc units for a0
    w = 1.0 / sigma_lnV**2
    c = np.sum(w * (y - x)) / np.sum(w)
    a0_eff = np.exp(4.0 * c)  # in (km/s)^2 / kpc
    resid = y - x - c
    chi2 = float(np.sum(w * resid**2))
    return a0_eff, chi2


def fit_model_B(M: np.ndarray, V: np.ndarray, sigma_lnV: np.ndarray):
    """Free (n, m, K): ln V = (m/n) ln M + (1/n) ln K."""
    lnM = np.log(M)
    lnV = np.log(V)
    w = 1.0 / sigma_lnV

    # Reparameterise: a = m/n, b = (1/n) ln K  -> ln V = a ln M + b
    # then n free? In a single linear regression we cannot recover n alone;
    # n is degenerate with K. We therefore fit (a, b) and report only the
    # ratio m/n which is what the data constrains, plus Model A residual.
    A = np.vstack([lnM, np.ones_like(lnM)]).T
    Aw = A * w[:, None]
    yw = lnV * w
    coef, *_ = np.linalg.lstsq(Aw, yw, rcond=None)
    a_fit, b_fit = coef
    resid = lnV - A @ coef
    chi2 = float(np.sum((resid * w) ** 2))
    # Also fit MOND-prior (a = 0.25 fixed) to compare
    return a_fit, b_fit, chi2


def aicc(chi2: float, k: int, n: int) -> float:
    return chi2 + 2 * k + (2 * k * (k + 1)) / max(n - k - 1, 1)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main() -> dict:
    cat = parse_catalog(SPARC_CAT)
    print(f"[L423] catalog rows parsed: {len(cat)}")

    records = []
    for row in cat:
        rc_path = SPARC_DIR / f"{row['name']}_rotmod.dat"
        if not rc_path.exists():
            continue
        try:
            rc = load_rotmod(rc_path)
        except Exception:
            continue
        if rc.ndim != 2 or rc.shape[1] < 6 or rc.shape[0] < 3:
            continue
        R_out, V_out, Mbar = outer_mass_from_rc(rc)
        if not np.isfinite(Mbar) or Mbar <= 0:
            continue
        if row["Vflat"] <= 0 or row["e_Vflat"] <= 0:
            continue
        records.append(dict(name=row["name"], Q=row["Q"],
                            Vflat=row["Vflat"], e_Vflat=row["e_Vflat"],
                            R_out=R_out, V_out=V_out, Mbar=Mbar))

    print(f"[L423] usable galaxies (Vflat>0, Mbar>0): {len(records)}")

    M = np.array([r["Mbar"] for r in records])
    V = np.array([r["Vflat"] for r in records])
    eV = np.array([r["e_Vflat"] for r in records])
    Q = np.array([r["Q"] for r in records])
    sigma_lnV = eV / V
    # floor sigma for catalog rows with eVflat=0 noise
    sigma_lnV = np.clip(sigma_lnV, 0.02, None)

    # Model A: deep-MOND / SQT-limit form
    a0_eff, chi2_A = fit_model_A(M, V, sigma_lnV)
    # Convert a0_eff back to m/s^2 for reporting
    a0_eff_ms2 = a0_eff / KPC_M * 1.0e6  # inverse of A0_KMS_KPC scaling
    n = len(records)
    k_A = 1
    aicc_A = aicc(chi2_A, k_A, n)

    # Model B: free slope a = m/n  (intercept b)
    a_B, b_B, chi2_B = fit_model_B(M, V, sigma_lnV)
    k_B = 2
    aicc_B = aicc(chi2_B, k_B, n)

    # Slope uncertainty (jackknife)
    a_jk = []
    for i in range(n):
        idx = np.arange(n) != i
        a_i, _, _ = fit_model_B(M[idx], V[idx], sigma_lnV[idx])
        a_jk.append(a_i)
    a_jk = np.array(a_jk)
    a_B_std = float(np.sqrt((n - 1) / n * np.sum((a_jk - a_jk.mean()) ** 2)))

    # Q-quality split
    def fit_subset(mask):
        if mask.sum() < 10:
            return None
        a0_s, chi2_As = fit_model_A(M[mask], V[mask], sigma_lnV[mask])
        a_s, _, chi2_Bs = fit_model_B(M[mask], V[mask], sigma_lnV[mask])
        return dict(n=int(mask.sum()),
                    a0_eff_ms2=float(a0_s / KPC_M * 1.0e6),
                    chi2_A=float(chi2_As),
                    slope_a=float(a_s),
                    chi2_B=float(chi2_Bs))

    subsets = {
        "Q1": fit_subset(Q == 1),
        "Q2": fit_subset(Q == 2),
        "Q3": fit_subset(Q == 3),
        "all": dict(n=n,
                    a0_eff_ms2=float(a0_eff_ms2),
                    chi2_A=float(chi2_A),
                    slope_a=float(a_B),
                    slope_a_jk_std=a_B_std,
                    chi2_B=float(chi2_B),
                    aicc_A=float(aicc_A),
                    aicc_B=float(aicc_B),
                    delta_aicc_BminusA=float(aicc_B - aicc_A)),
    }

    result = dict(
        n_galaxies=n,
        model_A=dict(form="V^4 = G * Mbar * a0_eff",
                     a0_eff_ms2=float(a0_eff_ms2),
                     chi2=float(chi2_A),
                     k=k_A,
                     aicc=float(aicc_A)),
        model_B=dict(form="ln V = a * ln Mbar + b   (a = m/n)",
                     slope_a=float(a_B),
                     slope_a_std_jk=a_B_std,
                     intercept_b=float(b_B),
                     chi2=float(chi2_B),
                     k=k_B,
                     aicc=float(aicc_B)),
        delta_aicc_BminusA=float(aicc_B - aicc_A),
        mond_prior_slope_025=dict(
            distance_to_data_slope_in_sigma=float(
                (a_B - 0.25) / max(a_B_std, 1e-6))),
        Q_subsets=subsets,
        a0_mond_reference_ms2=A0_MOND_MS2,
        notes=(
            "Model A is the deep-MOND / SQT outer-asymptotic limit V^4 = G M a0. "
            "Model B is a free Tully-Fisher slope. "
            "Negative delta_AICc (B-A) means free slope justified; positive means "
            "data does NOT justify the extra parameter and the (n=4, m=1) form is "
            "statistically equivalent. "
            "Per CLAUDE.md: this single test cannot distinguish SQT from MOND "
            "without a sub-leading-correction signature (NEXT_STEP stages 3-4)."
        ),
    )

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSON.open("w") as fh:
        json.dump(result, fh, indent=2)
    print(f"[L423] wrote {OUT_JSON}")

    # Plot
    fig, ax = plt.subplots(figsize=(6.4, 5.0))
    ax.errorbar(np.log10(M), np.log10(V), yerr=eV / V / np.log(10),
                fmt="o", ms=3, alpha=0.5, label=f"SPARC ({n})")
    xx = np.linspace(np.log10(M.min()), np.log10(M.max()), 100)
    # Model A line
    yA = 0.25 * (np.log10(G_KMS_KPC_MSUN) + xx) + 0.25 * np.log10(a0_eff)
    ax.plot(xx, yA, "r-", lw=2,
            label=f"Model A: n=4, m=1 (a0={a0_eff_ms2:.2e} m/s^2)")
    # Model B line
    yB = a_B * xx * np.log(10) / np.log(10) + b_B / np.log(10)
    yB = (a_B * xx * np.log(10) + b_B) / np.log(10)
    ax.plot(xx, yB, "b--", lw=2,
            label=f"Model B free: slope m/n={a_B:.3f}+/-{a_B_std:.3f}")
    ax.set_xlabel(r"$\log_{10}\,M_{\rm bar}\;[M_\odot]$")
    ax.set_ylabel(r"$\log_{10}\,V_{\rm flat}\;[{\rm km/s}]$")
    ax.set_title("L423 SPARC outer Tully-Fisher: SQT/MOND limit vs free slope")
    ax.legend(loc="lower right", fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_FIG, dpi=130)
    print(f"[L423] wrote {OUT_FIG}")

    return result


if __name__ == "__main__":
    res = main()
    print(json.dumps(
        dict(n=res["n_galaxies"],
             a0_eff_ms2=res["model_A"]["a0_eff_ms2"],
             slope_a_modelB=res["model_B"]["slope_a"],
             slope_std_jk=res["model_B"]["slope_a_std_jk"],
             delta_aicc=res["delta_aicc_BminusA"]),
        indent=2))
