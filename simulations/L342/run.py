"""
L342 — sigma_0(rho_env) monotonic vs non-monotonic likelihood ratio.

3 anchor measurements:
  cosmic   log10 sigma_0 = 8.37 +- 0.06   at log10 rho_env ~ -27 (voids/IGM)
  cluster  log10 sigma_0 = 7.75 +- 0.06   at log10 rho_env ~ -24 (cluster ICM)
  galactic log10 sigma_0 = 9.56 +- 0.05   at log10 rho_env ~ -21 (galactic disc/lab)

(Density anchors taken as representative log10 of the regime midpoint in
SI kg/m^3.  cosmic ~ rho_crit ~ 1e-27; cluster ICM ~ 1e-24; galactic mean
~ 1e-21.  Test is robust to +-1 dex shifts.)

Models:
  M1 (monotonic, k=2):   y = A + B*x         (linear in log rho)
  M1b (monotonic, k=2):  y = A + B*tanh((x-x0)/w)   [bounded sigmoid; we fix
                          x0=-24, w=2 to keep it 2-param so it competes with M1]
                          -> kept as supplementary check (still monotonic).
  M2 (non-monotonic, k=3): y = C + D*(x - x_min)^2   (parabola, V-shape)

For 3 data points:
  M1:  N - k = 1 dof
  M2:  N - k = 0 dof (saturated; chi^2 ~ 0 by construction)
We therefore use chi^2 + AICc as the scoring rule (AICc handles small N).

AICc = chi^2 + 2k + 2k(k+1)/(N-k-1).
For N=3, k=2: penalty = 4 + 12 = 16
For N=3, k=3: AICc undefined (N-k-1=-1). Convention: use AICc with
          N -> N+1 trick OR fall back to BIC with N=3 -> BIC=chi^2+k*ln3.
We report BOTH AIC and BIC for honesty (and a delta-chi2 ratio test).

Output: results/L342/run_output.json with chi2, AIC, BIC, delta values.
"""

from __future__ import annotations
import json
import math
import os
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

# ---- data --------------------------------------------------------------
# log10 rho_env (kg/m^3), log10 sigma_0, sigma uncertainty (dex)
DATA = np.array([
    # name        x = log10 rho_env   y = log10 sigma_0   sy
    ("cosmic",    -27.0,              8.37,               0.06),
    ("cluster",   -24.0,              7.75,               0.06),
    ("galactic",  -21.0,              9.56,               0.05),
], dtype=[("name", "U16"), ("x", "f8"), ("y", "f8"), ("sy", "f8")])

X = DATA["x"]
Y = DATA["y"]
SY = DATA["sy"]
N = len(X)


def chi2_of(yhat: np.ndarray) -> float:
    return float(np.sum(((Y - yhat) / SY) ** 2))


# ---- M1: monotonic linear (k=2) ----------------------------------------
def fit_M1():
    # y = A + B x
    # Closed-form WLS
    w = 1.0 / SY**2
    Sw = w.sum()
    Swx = (w * X).sum()
    Swy = (w * Y).sum()
    Swxx = (w * X * X).sum()
    Swxy = (w * X * Y).sum()
    det = Sw * Swxx - Swx * Swx
    B = (Sw * Swxy - Swx * Swy) / det
    A = (Swy - B * Swx) / Sw
    yhat = A + B * X
    return {"k": 2, "params": {"A": A, "B": B}, "chi2": chi2_of(yhat),
            "yhat": yhat.tolist()}


# ---- M1b: monotonic tanh (k=3 free, but fix x0,w -> k=2) ---------------
def fit_M1b():
    # y = A + B * tanh((x - x0)/w), x0=-24 fixed, w=2 fixed -> k=2
    x0, w = -24.0, 2.0

    def loss(p):
        A, B = p
        yhat = A + B * np.tanh((X - x0) / w)
        return chi2_of(yhat)

    res = minimize(loss, x0=[8.5, 1.0], method="Nelder-Mead",
                   options={"xatol": 1e-8, "fatol": 1e-8})
    A, B = res.x
    yhat = A + B * np.tanh((X - x0) / w)
    return {"k": 2, "params": {"A": float(A), "B": float(B),
                                "x0_fixed": x0, "w_fixed": w},
            "chi2": chi2_of(yhat), "yhat": yhat.tolist()}


# ---- M2: non-monotonic parabola (k=3) ----------------------------------
def fit_M2():
    # y = C + D * (x - x_min)^2
    def loss(p):
        C, D, xm = p
        yhat = C + D * (X - xm) ** 2
        return chi2_of(yhat)

    best = None
    for C0 in (7.5, 8.0, 8.5):
        for D0 in (0.1, 0.5, 1.0):
            for xm0 in (-25, -24, -23):
                res = minimize(loss, x0=[C0, D0, xm0], method="Nelder-Mead",
                               options={"xatol": 1e-9, "fatol": 1e-9,
                                        "maxiter": 5000})
                if best is None or res.fun < best.fun:
                    best = res
    C, D, xm = best.x
    yhat = C + D * (X - xm) ** 2
    return {"k": 3, "params": {"C": float(C), "D": float(D), "x_min": float(xm)},
            "chi2": chi2_of(yhat), "yhat": yhat.tolist()}


# ---- scoring -----------------------------------------------------------
def aic(chi2: float, k: int) -> float:
    return chi2 + 2 * k


def aicc(chi2: float, k: int, n: int) -> float:
    denom = n - k - 1
    if denom <= 0:
        return float("nan")
    return aic(chi2, k) + 2 * k * (k + 1) / denom


def bic(chi2: float, k: int, n: int) -> float:
    return chi2 + k * math.log(n)


def main():
    M1 = fit_M1()
    M1b = fit_M1b()
    M2 = fit_M2()

    rows = []
    for name, m in [("M1_linear_monotonic", M1),
                    ("M1b_tanh_monotonic", M1b),
                    ("M2_parabola_nonmono", M2)]:
        m["AIC"] = aic(m["chi2"], m["k"])
        m["AICc"] = aicc(m["chi2"], m["k"], N)
        m["BIC"] = bic(m["chi2"], m["k"], N)
        m["name"] = name
        rows.append(m)

    chi2_min = min(r["chi2"] for r in rows)
    aic_min = min(r["AIC"] for r in rows)
    bic_min = min(r["BIC"] for r in rows)
    for r in rows:
        r["dchi2"] = r["chi2"] - chi2_min
        r["dAIC"] = r["AIC"] - aic_min
        r["dBIC"] = r["BIC"] - bic_min

    # likelihood ratio: -2 ln (L_M1/L_M2) ~ chi2(M1) - chi2(M2)
    lrt_M1_vs_M2 = M1["chi2"] - M2["chi2"]
    lrt_M1b_vs_M2 = M1b["chi2"] - M2["chi2"]

    out = {
        "data": [{"name": str(d["name"]), "x": float(d["x"]),
                   "y": float(d["y"]), "sy": float(d["sy"])} for d in DATA],
        "models": rows,
        "lrt_chi2_M1_minus_M2": float(lrt_M1_vs_M2),
        "lrt_chi2_M1b_minus_M2": float(lrt_M1b_vs_M2),
        "lrt_significance_M1_sigma_eq": float(math.sqrt(max(lrt_M1_vs_M2, 0.0))),
        "note": ("With N=3, k=3 saturates -> M2 chi2 ~ 0 by construction. "
                 "AICc(k=3,N=3) is undefined; AIC and BIC reported. "
                 "The honest discriminator is delta-chi^2 (LRT) and BIC."),
    }

    out_dir = Path(__file__).resolve().parents[2] / "results" / "L342"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "run_output.json", "w") as f:
        json.dump(out, f, indent=2)

    # human-readable echo
    print("=== L342 sigma_0(rho_env) monotonic vs non-monotonic ===")
    print(f"{'model':<28} {'k':>2} {'chi2':>8} {'AIC':>8} {'BIC':>8} "
          f"{'dchi2':>8} {'dBIC':>8}")
    for r in rows:
        print(f"{r['name']:<28} {r['k']:>2} {r['chi2']:>8.3f} "
              f"{r['AIC']:>8.3f} {r['BIC']:>8.3f} "
              f"{r['dchi2']:>8.3f} {r['dBIC']:>8.3f}")
    print(f"\nLRT chi^2 (M1 - M2) = {lrt_M1_vs_M2:.3f}  "
          f"(equiv {math.sqrt(max(lrt_M1_vs_M2,0)):.2f} sigma if 1 dof)")
    print(f"LRT chi^2 (M1b - M2) = {lrt_M1b_vs_M2:.3f}")
    print(f"Output: {out_dir/'run_output.json'}")


if __name__ == "__main__":
    main()
