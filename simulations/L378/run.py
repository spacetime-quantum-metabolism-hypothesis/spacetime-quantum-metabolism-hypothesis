"""
L378 - single-anchor Leave-One-Out fragility on the 3-anchor sigma_0(rho_env)
       monotonic (M1) vs non-monotonic (M2) likelihood-ratio claim from L342.

See results/L378/ATTACK_DESIGN.md for the pre-registered design.

Tests:
  A: direct N=2 fits (saturated; recorded for transparency only).
  B: LOO predictive chi^2: fit on remaining 2 points, predict held-out.
     For M2 we fix x_min to the L342 full-data MAP so M2 has k=2 free
     parameters (C, D) and produces a unique 2-point fit.
  C: full-data Delta-chi^2 with sigma_i -> inf for the held-out anchor
     (likelihood-marginalisation form of leave-one-out).
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

# ---- data (identical to L342) ----------------------------------------------
DATA = np.array([
    ("cosmic",   -27.0, 8.37, 0.06),
    ("cluster",  -24.0, 7.75, 0.06),
    ("galactic", -21.0, 9.56, 0.05),
], dtype=[("name", "U16"), ("x", "f8"), ("y", "f8"), ("sy", "f8")])

NAMES = list(DATA["name"])
X = DATA["x"].astype(float)
Y = DATA["y"].astype(float)
SY = DATA["sy"].astype(float)
N = len(X)


# ---- helpers ---------------------------------------------------------------
def chi2(yhat, y, sy):
    return float(np.sum(((y - yhat) / sy) ** 2))


def fit_linear(x, y, sy):
    """WLS y = A + B x. Saturated for N=2."""
    w = 1.0 / sy ** 2
    Sw = w.sum()
    Swx = (w * x).sum()
    Swy = (w * y).sum()
    Swxx = (w * x * x).sum()
    Swxy = (w * x * y).sum()
    det = Sw * Swxx - Swx * Swx
    B = (Sw * Swxy - Swx * Swy) / det
    A = (Swy - B * Swx) / Sw
    return float(A), float(B)


def fit_parabola_xmin_fixed(x, y, sy, x_min):
    """y = C + D (x - x_min)^2.  Linear in (C, D) -> WLS closed form."""
    z = (x - x_min) ** 2
    w = 1.0 / sy ** 2
    Sw = w.sum()
    Swz = (w * z).sum()
    Swy = (w * y).sum()
    Swzz = (w * z * z).sum()
    Swzy = (w * z * y).sum()
    det = Sw * Swzz - Swz * Swz
    if abs(det) < 1e-15:
        return None
    D = (Sw * Swzy - Swz * Swy) / det
    C = (Swy - D * Swz) / Sw
    return float(C), float(D)


def fit_parabola_full(x, y, sy):
    """y = C + D(x - x_min)^2 with all 3 free; multistart Nelder-Mead."""
    def loss(p):
        C, D, xm = p
        return chi2(C + D * (x - xm) ** 2, y, sy)
    best = None
    for C0 in (7.5, 8.0, 8.5):
        for D0 in (0.05, 0.1, 0.5, 1.0):
            for xm0 in (-26, -25, -24, -23):
                res = minimize(loss, x0=[C0, D0, xm0], method="Nelder-Mead",
                               options={"xatol": 1e-9, "fatol": 1e-9,
                                        "maxiter": 5000})
                if best is None or res.fun < best.fun:
                    best = res
    C, D, xm = best.x
    return float(C), float(D), float(xm), float(best.fun)


# ---- baseline reproduction (L342) ------------------------------------------
def baseline():
    A, B = fit_linear(X, Y, SY)
    yhat_M1 = A + B * X
    chi2_M1 = chi2(yhat_M1, Y, SY)

    C, D, xm, chi2_M2 = fit_parabola_full(X, Y, SY)
    yhat_M2 = C + D * (X - xm) ** 2

    return {
        "M1": {"A": A, "B": B, "chi2": chi2_M1, "yhat": yhat_M1.tolist()},
        "M2": {"C": C, "D": D, "x_min": xm, "chi2": chi2_M2,
               "yhat": yhat_M2.tolist()},
        "delta_chi2_M1_minus_M2": chi2_M1 - chi2_M2,
    }


# ---- Test A: N=2 direct fits (saturation record) ---------------------------
def test_A(x_min_full):
    rows = []
    for i, name in enumerate(NAMES):
        keep = np.array([j for j in range(N) if j != i])
        x_k, y_k, sy_k = X[keep], Y[keep], SY[keep]

        A, B = fit_linear(x_k, y_k, sy_k)
        chi2_M1 = chi2(A + B * x_k, y_k, sy_k)

        # M2 with x_min FREE on N=2 -> infinitely many zero-chi2 solutions.
        # Record that with x_min fixed to full-data MAP it is also saturated:
        res = fit_parabola_xmin_fixed(x_k, y_k, sy_k, x_min_full)
        if res is None:
            C, D, chi2_M2 = float("nan"), float("nan"), float("nan")
        else:
            C, D = res
            chi2_M2 = chi2(C + D * (x_k - x_min_full) ** 2, y_k, sy_k)

        rows.append({
            "left_out": name,
            "M1_fit_chi2_on_kept": chi2_M1,        # ~0 (saturated)
            "M2_xmin_fixed_chi2_on_kept": chi2_M2, # ~0 (saturated)
            "M1_params": {"A": A, "B": B},
            "M2_params": {"C": C, "D": D, "x_min_fixed": x_min_full},
        })
    return rows


# ---- Test B: LOO predictive chi^2 ------------------------------------------
def test_B(x_min_full):
    rows = []
    for i, name in enumerate(NAMES):
        keep = np.array([j for j in range(N) if j != i])
        x_k, y_k, sy_k = X[keep], Y[keep], SY[keep]
        x_o, y_o, sy_o = X[i], Y[i], SY[i]

        # M1 saturated linear fit on 2 kept points -> unique extrapolation
        A, B = fit_linear(x_k, y_k, sy_k)
        y_pred_M1 = A + B * x_o
        r_M1 = (y_o - y_pred_M1) / sy_o
        chi2_pred_M1 = float(r_M1 ** 2)

        # M2 (x_min fixed to full-data MAP) saturated 2-param fit on 2 kept
        res = fit_parabola_xmin_fixed(x_k, y_k, sy_k, x_min_full)
        if res is None:
            chi2_pred_M2 = float("nan")
            y_pred_M2 = float("nan")
        else:
            C, D = res
            y_pred_M2 = C + D * (x_o - x_min_full) ** 2
            chi2_pred_M2 = float(((y_o - y_pred_M2) / sy_o) ** 2)

        delta = chi2_pred_M1 - chi2_pred_M2
        rows.append({
            "left_out": name,
            "y_obs": float(y_o),
            "y_pred_M1": float(y_pred_M1),
            "y_pred_M2_xmin_fixed": float(y_pred_M2),
            "chi2_pred_M1": chi2_pred_M1,
            "chi2_pred_M2_xmin_fixed": chi2_pred_M2,
            "delta_chi2_M1_minus_M2": float(delta),
        })
    return rows


# ---- Test C: full-data with sigma_i -> inf ---------------------------------
def test_C():
    rows = []
    INF = 1e6
    for i, name in enumerate(NAMES):
        sy_eff = SY.copy()
        sy_eff[i] *= INF

        A, B = fit_linear(X, Y, sy_eff)
        chi2_M1 = chi2(A + B * X, Y, sy_eff)

        # M2 free: refit fully
        C, D, xm, chi2_M2 = fit_parabola_full(X, Y, sy_eff)

        rows.append({
            "muted_anchor": name,
            "chi2_M1_inflated": float(chi2_M1),
            "chi2_M2_inflated": float(chi2_M2),
            "delta_chi2_M1_minus_M2": float(chi2_M1 - chi2_M2),
            "M1_params": {"A": A, "B": B},
            "M2_params": {"C": C, "D": D, "x_min": xm},
        })
    return rows


# ---- driver share ----------------------------------------------------------
def driver_share(test_B_rows):
    deltas = np.array([r["delta_chi2_M1_minus_M2"] for r in test_B_rows])
    pos = np.maximum(deltas, 0.0)
    total = pos.sum()
    if total <= 0:
        return {"shares": [0.0] * len(deltas),
                "max_share": 0.0, "max_anchor": None,
                "fragile": False, "total_positive_delta": 0.0}
    shares = (pos / total).tolist()
    imax = int(np.argmax(pos))
    return {
        "anchors": NAMES,
        "deltas": deltas.tolist(),
        "shares": shares,
        "max_share": float(shares[imax]),
        "max_anchor": NAMES[imax],
        "fragile": bool(shares[imax] > 0.85),
        "total_positive_delta": float(total),
    }


# ---- main ------------------------------------------------------------------
def main():
    out_dir = Path(__file__).resolve().parents[2] / "results" / "L378"
    out_dir.mkdir(parents=True, exist_ok=True)

    base = baseline()
    x_min_full = base["M2"]["x_min"]

    A = test_A(x_min_full)
    B = test_B(x_min_full)
    C = test_C()
    share = driver_share(B)

    report = {
        "anchors": NAMES,
        "data": [
            {"name": n, "x": float(x), "y": float(y), "sy": float(s)}
            for n, x, y, s in zip(NAMES, X, Y, SY)
        ],
        "baseline_L342_reproduction": base,
        "test_A_N2_fits": A,
        "test_B_LOO_predictive": B,
        "test_C_sigma_inflated": C,
        "driver_diagnostic": share,
        "decision": (
            "FRAGILE - single-anchor driver" if share["fragile"]
            else "ROBUST-IN-3 - distributed driver"
        ),
        "criterion": "max share of positive Delta-chi^2 > 0.85",
        "honest_notes": [
            "N=3 LOO is a single-point predictive test, not Bayesian CV.",
            "M2 with x_min fixed to full-data MAP introduces leakage: "
            "the held-out point informed x_min. This biases Test B toward "
            "M2. The diagnostic remains valid as a fragility floor: if "
            "even with this M2-friendly choice the share is still >0.85 "
            "for one anchor, the L342 LRT is single-point dominated.",
            "Test C is the cleanest leave-out (full chi^2 machinery).",
        ],
    }

    with open(out_dir / "report.json", "w") as f:
        json.dump(report, f, indent=2)

    # console summary
    print("=== L378 Leave-One-Out fragility on L342 3-anchor LRT ===")
    print(f"baseline Delta-chi^2(M1-M2)={base['delta_chi2_M1_minus_M2']:.3f}  "
          f"x_min*={x_min_full:.4f}")
    print()
    print("Test B - LOO predictive Delta-chi^2 per left-out anchor:")
    print(f"{'left_out':<10} {'chi2_M1_pred':>14} "
          f"{'chi2_M2_pred':>14} {'delta':>10}")
    for r in B:
        print(f"{r['left_out']:<10} {r['chi2_pred_M1']:>14.3f} "
              f"{r['chi2_pred_M2_xmin_fixed']:>14.3f} "
              f"{r['delta_chi2_M1_minus_M2']:>10.3f}")
    print()
    print("Test C - full data with sigma_i -> inf:")
    print(f"{'muted':<10} {'chi2_M1_inf':>14} {'chi2_M2_inf':>14} "
          f"{'delta':>10}")
    for r in C:
        print(f"{r['muted_anchor']:<10} {r['chi2_M1_inflated']:>14.3f} "
              f"{r['chi2_M2_inflated']:>14.3f} "
              f"{r['delta_chi2_M1_minus_M2']:>10.3f}")
    print()
    print(f"Driver shares: {share['shares']}")
    print(f"Max anchor: {share['max_anchor']}  share={share['max_share']:.3f}")
    print(f"DECISION: {report['decision']}")
    print(f"Output -> {out_dir/'report.json'}")


if __name__ == "__main__":
    main()
