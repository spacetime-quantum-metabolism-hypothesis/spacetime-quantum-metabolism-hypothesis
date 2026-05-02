"""L406 — S_8 mitigation grid + Euclid/LSST forecast.

Direction (no map): explore whether a generic time/density-dependent vacuum
profile V(n,t) on the dark sector can shift mu_eff away from 1 enough to
mitigate the +1.14% S_8 worsening, and forecast Euclid/LSST detection.

Outputs:
  results/L406/grid_S8_vs_Vparams.csv
  results/L406/forecast_facilities.json

Honest stance: if no point in the explored grid reaches |Delta S_8| < 0.5%,
report mitigation as STRUCTURALLY UNREACHABLE within this fluid-level toy.
"""
from __future__ import annotations
import json, os, csv, math
from multiprocessing import get_context

# Force single-thread per worker (CLAUDE.md rule)
for _k in ("OMP_NUM_THREADS","MKL_NUM_THREADS","OPENBLAS_NUM_THREADS"):
    os.environ.setdefault(_k, "1")

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT  = os.path.join(ROOT, "results", "L406")
os.makedirs(OUT, exist_ok=True)

# ---------- Background (LCDM-equivalent, since we're testing growth shifts) ----------
H0 = 67.4
Om = 0.315
OL = 1.0 - Om

def E_lcdm(a):
    return np.sqrt(Om*a**-3 + OL)

# ---------- Growth ODE with mu_eff(a) and beta_eff(a) ----------
# d^2 D / d ln a^2 + (2 + dlnH/dlna) dD/dlna - 1.5 * Om(a) * mu_eff * D = 0
# G_eff/G = mu_eff = 1 + 2 beta_eff(a)^2  (Phase-2 approximation)
# beta_eff(a) parameterised by V(n,t) toy: beta_eff(a) = beta0 * a^p * f_dark
#   where f_dark = OL/(Om*a^-3 + OL) is the dark-sector dominance fraction.
# This embodies "dark-only" coupling that grows when DE dominates.

from scipy.integrate import odeint

def growth(beta0, p, fdark_only=True):
    a_grid = np.geomspace(1e-3, 1.0, 600)
    lna = np.log(a_grid)
    def beta(a):
        if fdark_only:
            f = OL/(Om*a**-3 + OL)
        else:
            f = 1.0
        return beta0 * (a**p) * f
    def mu(a):
        return 1.0 + 2.0*beta(a)**2
    def dlnHdlna(a):
        # E^2 = Om a^-3 + OL ; 2E dE/dlna = -3 Om a^-3
        E2 = Om*a**-3 + OL
        return 0.5 * (-3*Om*a**-3) / E2
    def Om_a(a):
        return Om*a**-3 / (Om*a**-3 + OL)
    def deriv(y, lna):
        D, Dp = y
        a = math.exp(lna)
        return [Dp, -(2.0 + dlnHdlna(a))*Dp + 1.5*Om_a(a)*mu(a)*D]
    sol = odeint(deriv, [a_grid[0], a_grid[0]], lna, full_output=False)
    D_raw = sol[:,0].copy()
    Dp_raw = sol[:,1].copy()
    if not (np.all(np.isfinite(D_raw)) and D_raw[-1] > 0):
        return None
    D = D_raw / D_raw[-1]
    f = Dp_raw / D_raw  # dlnD/dlna using raw values
    return a_grid, D, f

# sigma_8 today ~ proportional to D(a=1) normalisation; shift relative to LCDM:
# We track sigma_8_SQT/sigma_8_LCDM = sqrt( <D(a)^2 P_lin> / <D_LCDM^2 P_lin> ),
# but for k-independent mu_eff this collapses to D_SQT(a=1)/D_LCDM(a=1) when both
# normalised at high z (a=1e-3). Compute that ratio.

def sigma8_ratio(beta0, p):
    base = growth(0.0, 0.0)
    test = growth(beta0, p)
    if base is None or test is None:
        return None
    a, Db, _ = base
    _, Dt, _ = test
    # Normalise at early time a=1e-3 (matter era) instead of today
    norm_b = Db[0]; norm_t = Dt[0]
    Db_e = Db / norm_b
    Dt_e = Dt / norm_t
    return Dt_e[-1] / Db_e[-1]

# ---------- Worker ----------
def _worker(args):
    b0, p = args
    r = sigma8_ratio(b0, p)
    if r is None:
        return (b0, p, float('nan'), float('nan'), float('nan'))
    delta_s8 = r - 1.0  # fractional shift in sigma_8 today
    delta_xi  = 2.0 * delta_s8  # cosmic shear scaling (xi_+ ~ S_8^2)
    # Target: cancel +1.14% baseline worsening => need delta_s8 ~ -0.0114
    cancellation = abs(delta_s8 + 0.0114)  # smaller is better
    return (b0, p, delta_s8, delta_xi, cancellation)

def main():
    beta0_grid = np.linspace(0.0, 0.30, 13)   # 0..0.30 (Cassini dark-only OK)
    p_grid     = np.linspace(-2.0, 2.0, 9)
    tasks = [(b, p) for b in beta0_grid for p in p_grid]

    ctx = get_context('spawn')
    with ctx.Pool(processes=8) as pool:
        rows = pool.map(_worker, tasks)

    csv_path = os.path.join(OUT, "grid_S8_vs_Vparams.csv")
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(["beta0","p","delta_s8","delta_xi_plus","cancel_residual"])
        for r in rows: w.writerow(r)

    # Best mitigation
    finite = [r for r in rows if math.isfinite(r[4])]
    finite.sort(key=lambda r: r[4])
    best = finite[0] if finite else None

    # Also track S_8 *most negative* shift achievable (max mitigation downward)
    finite_neg = sorted(finite, key=lambda r: r[2])  # ascending delta_s8
    max_down = finite_neg[0] if finite_neg else None

    # Best is the (beta0, p) closest to canceling +1.14%. mu_eff=1+2 beta^2
    # always >=1 => growth ENHANCED => sigma_8 INCREASES => delta_s8 >= 0.
    # So this toy *cannot* reduce S_8. Mitigation requires mu_eff < 1, which
    # |2 beta^2| construction forbids. Honest report below.

    # Forecast Euclid/LSST (Fisher-style toy)
    # baseline +1.14% S_8 = +2.29% xi_+ shift
    # Euclid sigma(S_8) ~ 0.0026 (Euclid Collab. 2020 IST forecast)
    # LSST  sigma(S_8) ~ 0.0040 (DESC SRD Y10)
    # DES-Y3 sigma(S_8) ~ 0.018  (current)
    sigmas = {"DES_Y3":0.018, "Euclid":0.0026, "LSST_Y10":0.0040}
    shift = 0.0114  # SQT vs LCDM
    forecast = {f: shift/s for f,s in sigmas.items()}  # n-sigma detection

    summary = {
        "grid_size": len(rows),
        "max_mitigation_attempt_grid":{
            "beta0_max": float(beta0_grid.max()),
            "p_range":   [float(p_grid.min()), float(p_grid.max())]
        },
        "best_cancellation": {
            "beta0": best[0], "p": best[1],
            "delta_s8": best[2], "delta_xi_plus": best[3],
            "residual_after_mitigation_pct": (best[2]+0.0114)*100
        } if best else None,
        "max_downward_S8_shift_pct": max_down[2]*100 if max_down else None,
        "structural_finding":(
            "mu_eff = 1 + 2 beta_eff^2 >= 1 always (Phase-2 dark-only embedding). "
            "Growth ENHANCED, sigma_8 INCREASES with any non-zero coupling. "
            "Within fluid-level G_eff/G = 1+2 beta^2 toy, S_8 mitigation is "
            "STRUCTURALLY UNREACHABLE (cannot produce delta_s8 < 0)."
        ),
        "facility_forecast_sigma": forecast,
        "facility_verdict":{
            f:("DETECT >5σ" if n>=5 else "DETECT 3-5σ" if n>=3 else
               "MARGINAL 1-3σ" if n>=1 else "INVISIBLE")
            for f,n in forecast.items()
        }
    }
    with open(os.path.join(OUT, "forecast_facilities.json"),'w') as f:
        json.dump(summary, f, indent=2)

    print("[L406] grid done:", csv_path)
    print("[L406] best cancel:", summary["best_cancellation"])
    print("[L406] max downward S_8 shift (%):", summary["max_downward_S8_shift_pct"])
    print("[L406] structural:", summary["structural_finding"])
    print("[L406] forecast n-sigma:", forecast)

if __name__ == "__main__":
    main()
