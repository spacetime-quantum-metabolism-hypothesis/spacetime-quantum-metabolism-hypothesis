"""L422 — BTFR slope a priori test against SPARC.

SQT a priori prediction: V_flat^4 = G * M_b * a_0  with  a_0 = c*H0/(2pi).
=> log10 V_flat = (1/4) log10(M_b) + (1/4) log10(G * a_0)
=> structural slope = 4.0 .

Compare to SPARC 175-galaxy catalogue (Lelli, McGaugh, Schombert 2016).
"""

from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Constants (SI)
# ---------------------------------------------------------------------------
C_LIGHT = 2.99792458e8           # m/s
G_NEWT  = 6.67430e-11            # m^3 kg^-1 s^-2
MPC     = 3.0857e22              # m
MSUN    = 1.98892e30             # kg
KM      = 1.0e3
H0_KMSMPC = 67.4                 # Planck 2018, km/s/Mpc
H0_SI = H0_KMSMPC * KM / MPC     # 1/s

A0_SQT  = C_LIGHT * H0_SI / (2.0 * math.pi)   # m/s^2 ~ 1.16e-10
A0_OBS  = 1.20e-10                            # McGaugh observed BTFR a0

UPSILON_STAR = 0.5  # M_sun / L_sun at 3.6 micron (McGaugh & Schombert 2014 baseline)
HE_FACTOR    = 1.33

# ---------------------------------------------------------------------------
# SPARC catalog parser (Table1.mrt fixed width)
# Bytes (1-indexed):
#  Galaxy 1-11, T 12-13, D 14-19, e_D 20-24, f_D 25-26, Inc 27-30, e_Inc 31-34,
#  L[3.6] 35-41 [1e9 Lsun], e_L 42-48, Reff 49-53, SBeff 54-61, Rdisk 62-66,
#  SBdisk 67-74, MHI 75-81 [1e9 Msun], RHI 82-86, Vflat 87-91 [km/s],
#  e_Vflat 92-96, Q 97-99, Ref 100-113.
# ---------------------------------------------------------------------------

def _f(line: str, lo: int, hi: int) -> float:
    s = line[lo - 1:hi].strip()
    if not s:
        return float('nan')
    try:
        return float(s)
    except ValueError:
        return float('nan')


def _i(line: str, lo: int, hi: int) -> int:
    s = line[lo - 1:hi].strip()
    if not s:
        return -1
    try:
        return int(s)
    except ValueError:
        return -1


def parse_sparc(path: Path) -> list[dict]:
    """Whitespace-tokenized parser for the SPARC Table1 catalogue.

    Field order (from MRT header):
        Galaxy T D e_D f_D Inc e_Inc L[3.6] e_L[3.6] Reff SBeff Rdisk SBdisk
        MHI RHI Vflat e_Vflat Q [Ref]
    """
    rows: list[dict] = []
    in_data = False
    dash_run = 0
    with path.open('r', encoding='ascii', errors='ignore') as fh:
        for line in fh:
            line_r = line.rstrip('\n')
            if line_r.startswith('---'):
                dash_run += 1
                if dash_run >= 4:
                    in_data = True
                continue
            if not in_data:
                continue
            if not line_r.strip():
                continue
            tok = line_r.split()
            # Need at least 18 numeric tokens after name; Ref optional.
            if len(tok) < 18:
                continue
            try:
                name   = tok[0]
                T_h    = int(tok[1])
                D      = float(tok[2])
                e_D    = float(tok[3])
                # tok[4] = f_D (int)
                Inc    = float(tok[5])
                e_Inc  = float(tok[6])
                L36    = float(tok[7])
                e_L36  = float(tok[8])
                # Reff(9), SBeff(10), Rdisk(11), SBdisk(12)
                MHI    = float(tok[13])
                # RHI(14)
                Vflat  = float(tok[15])
                e_Vf   = float(tok[16])
                Q      = int(tok[17])
            except (ValueError, IndexError):
                continue
            rows.append(dict(
                name=name, T=T_h, D=D, e_D=e_D, Inc=Inc, e_Inc=e_Inc,
                L36=L36, e_L36=e_L36, MHI=MHI, Vflat=Vflat, e_Vflat=e_Vf, Q=Q,
            ))
    return rows


# ---------------------------------------------------------------------------
# Estimators
# ---------------------------------------------------------------------------

def ols_forward(x: np.ndarray, y: np.ndarray, yerr: np.ndarray | None) -> tuple[float, float, float, float]:
    """Weighted OLS y = a*x + b. Returns (slope, intercept, sigma_slope, sigma_int)."""
    if yerr is None:
        w = np.ones_like(y)
    else:
        w = 1.0 / np.maximum(yerr, 1e-6) ** 2
    Sw = w.sum()
    Sx = (w * x).sum()
    Sy = (w * y).sum()
    Sxx = (w * x * x).sum()
    Sxy = (w * x * y).sum()
    D = Sw * Sxx - Sx * Sx
    a = (Sw * Sxy - Sx * Sy) / D
    b = (Sxx * Sy - Sx * Sxy) / D
    sa = math.sqrt(Sw / D)
    sb = math.sqrt(Sxx / D)
    return a, b, sa, sb


def ols_reverse_as_forward(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """Fit x = a' y + b' then invert: slope_inv = 1/a', intercept = -b'/a'."""
    a_p, b_p, _, _ = ols_forward(y, x, None)
    return 1.0 / a_p, -b_p / a_p


def orthogonal_bisector(x: np.ndarray, y: np.ndarray) -> float:
    """Geometric mean / bisector slope: sign(r) * sqrt(slope_fwd * slope_rev_inv)."""
    a_fwd, _, _, _ = ols_forward(x, y, None)
    a_rev_inv, _ = ols_reverse_as_forward(x, y)
    s = math.copysign(1.0, a_fwd)
    return s * math.sqrt(abs(a_fwd) * abs(a_rev_inv))


# ---------------------------------------------------------------------------
# Build sample
# ---------------------------------------------------------------------------

def build_sample(rows: list[dict], q_max: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str]]:
    """Returns (x, y, yerr) with x = log10 V_flat[km/s], y = log10 M_b[Msun].

    BTFR convention: M_b = A * V_flat^slope  =>  log M = slope * log V + const.
    SQT a priori slope = 4. We fit y(x).
    """
    xs: list[float] = []   # log10 V
    ys: list[float] = []   # log10 M
    ye: list[float] = []   # uncertainty in log10 M propagated from V error
    names: list[str] = []
    for r in rows:
        if not (r['Vflat'] > 0 and r['e_Vflat'] > 0):
            continue
        if not (r['Q'] >= 1 and r['Q'] <= q_max):
            continue
        if not (r['L36'] > 0 or r['MHI'] > 0):
            continue
        M_star = UPSILON_STAR * max(r['L36'], 0.0) * 1e9
        M_gas  = HE_FACTOR * max(r['MHI'], 0.0) * 1e9
        M_b    = M_star + M_gas
        if M_b <= 0:
            continue
        x = math.log10(r['Vflat'])
        y = math.log10(M_b)
        # If true slope ~ 4, then sigma(log M) ~ 4 * sigma(log V) = 4 * e_V/(V ln10)
        # but we use only V uncertainty here; intrinsic scatter dominates anyway.
        ye_logV = r['e_Vflat'] / (r['Vflat'] * math.log(10.0))
        ye_logM = 4.0 * ye_logV
        # add a floor for intrinsic scatter (~0.1 dex typical BTFR)
        ye_logM = math.sqrt(ye_logM ** 2 + 0.10 ** 2)
        xs.append(x); ys.append(y); ye.append(ye_logM); names.append(r['name'])
    return np.array(xs), np.array(ys), np.array(ye), names


# ---------------------------------------------------------------------------
# AICc
# ---------------------------------------------------------------------------

def aicc(chi2: float, k: int, n: int) -> float:
    aic = chi2 + 2.0 * k
    if n - k - 1 <= 0:
        return aic
    return aic + 2.0 * k * (k + 1) / (n - k - 1)


def chi2_of(x: np.ndarray, y: np.ndarray, ye: np.ndarray, slope: float, intercept: float) -> float:
    yhat = slope * x + intercept
    r = (y - yhat) / np.maximum(ye, 1e-6)
    return float((r * r).sum())


def best_intercept_fixed_slope(x: np.ndarray, y: np.ndarray, ye: np.ndarray, slope: float) -> float:
    w = 1.0 / np.maximum(ye, 1e-6) ** 2
    return float(((y - slope * x) * w).sum() / w.sum())


# ---------------------------------------------------------------------------
# SQT a priori intercept
# ---------------------------------------------------------------------------

def sqt_intercept(a0: float) -> float:
    """log10 M_b[Msun] = 4 * log10(V_flat[km/s]) + intercept.

    V^4 [m^4/s^4] = G * M_b[kg] * a0
    => M_b[kg] = V[m/s]^4 / (G a0)
    => log10 M_b[Msun] = 4 log10(V[m/s]) - log10(G a0 Msun)
                      = 4 (log10(V[km/s]) + 3) - log10(G a0 Msun)
                      = 4 log10(V[km/s]) + 12 - log10(G a0 Msun)
    """
    return 12.0 - math.log10(G_NEWT * a0 * MSUN)


def a0_from_intercept(intercept: float) -> float:
    """Inverse: intercept = 12 - log10(G*a0*Msun) -> a0 = 10^(12-intercept)/(G*Msun)."""
    return 10.0 ** (12.0 - intercept) / (G_NEWT * MSUN)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_one(rows: list[dict], q_max: int, label: str) -> dict:
    x, y, ye, names = build_sample(rows, q_max=q_max)
    n = len(x)
    print(f"[{label}] sample n = {n}")
    if n < 10:
        return dict(label=label, n=n, error='insufficient sample')

    a_fwd, b_fwd, sa_fwd, sb_fwd = ols_forward(x, y, ye)
    a_rev_inv, b_rev_inv = ols_reverse_as_forward(x, y)
    a_bi = orthogonal_bisector(x, y)

    # Inflate uncertainty if reduced chi2 > 1 (intrinsic scatter beyond stated errors).
    # Standard practice: scale sigma_slope by sqrt(chi2/dof).
    chi2_test = chi2_of(x, y, ye, a_fwd, b_fwd)
    dof = max(n - 2, 1)
    rchi2 = chi2_test / dof
    scale = math.sqrt(max(rchi2, 1.0))
    sa_fwd_inflated = sa_fwd * scale
    sb_fwd_inflated = sb_fwd * scale

    chi2_free = chi2_of(x, y, ye, a_fwd, b_fwd)
    aicc_free = aicc(chi2_free, k=2, n=n)

    b_fixed4 = best_intercept_fixed_slope(x, y, ye, 4.0)
    chi2_fix4 = chi2_of(x, y, ye, 4.0, b_fixed4)
    aicc_fix4 = aicc(chi2_fix4, k=1, n=n)

    int_sqt = sqt_intercept(A0_SQT)
    chi2_sqt = chi2_of(x, y, ye, 4.0, int_sqt)
    aicc_sqt = aicc(chi2_sqt, k=0, n=n)

    a0_recovered = a0_from_intercept(b_fixed4)

    res = dict(
        label=label,
        n=n,
        slope_free=a_fwd, intercept_free=b_fwd,
        sigma_slope_free=sa_fwd, sigma_intercept_free=sb_fwd,
        sigma_slope_free_inflated=sa_fwd_inflated,
        sigma_intercept_free_inflated=sb_fwd_inflated,
        rchi2_free=rchi2,
        slope_reverse_inv=a_rev_inv,
        slope_bisector=a_bi,
        chi2_free=chi2_free, aicc_free=aicc_free,
        intercept_fixed4=b_fixed4,
        chi2_fixed4=chi2_fix4, aicc_fixed4=aicc_fix4,
        intercept_sqt_apriori=int_sqt,
        chi2_sqt_apriori=chi2_sqt, aicc_sqt_apriori=aicc_sqt,
        a0_recovered_from_fixed4=a0_recovered,
        a0_sqt_prediction=A0_SQT,
        a0_mcgaugh=A0_OBS,
        delta_aicc_free_minus_fixed4=aicc_free - aicc_fix4,
        delta_aicc_free_minus_sqt=aicc_free - aicc_sqt,
    )

    # Pretty print
    print(f"  slope (forward OLS) = {a_fwd:.3f} +/- {sa_fwd:.3f}")
    print(f"  slope (reverse inv) = {a_rev_inv:.3f}")
    print(f"  slope (bisector)    = {a_bi:.3f}")
    print(f"  intercept_free      = {b_fwd:.3f}")
    print(f"  intercept_fixed4    = {b_fixed4:.3f}")
    print(f"  intercept_SQT_apriori = {int_sqt:.3f}")
    print(f"  chi2: free={chi2_free:.2f}  fixed4={chi2_fix4:.2f}  sqt_apriori={chi2_sqt:.2f}")
    print(f"  AICc: free={aicc_free:.2f}  fixed4={aicc_fix4:.2f}  sqt_apriori={aicc_sqt:.2f}")
    print(f"  Delta AICc (free - fixed4) = {res['delta_aicc_free_minus_fixed4']:.2f}")
    print(f"  Delta AICc (free - sqt   ) = {res['delta_aicc_free_minus_sqt']:.2f}")
    print(f"  a0 from fixed-4 fit = {a0_recovered:.3e}  (SQT a0 = {A0_SQT:.3e}, McGaugh = {A0_OBS:.3e})")

    # Pass criteria K1..K4
    # Use bisector slope for K1/K2 (less attenuation) and inflated sigma for K2.
    slope_report = a_bi
    sigma_report = sa_fwd_inflated  # conservative inflated sigma
    k1 = 3.8 <= slope_report <= 4.2
    k2 = abs(slope_report - 4.0) <= sigma_report
    res['slope_report_bisector'] = slope_report
    res['sigma_slope_used_for_K2'] = sigma_report
    k3 = res['delta_aicc_free_minus_fixed4'] >= -2.0  # i.e. fixed-4 is not strictly worse by >2
    # K4: a0_recovered within factor 1.5 of SQT prediction
    k4 = 0.667 * A0_SQT <= a0_recovered <= 1.5 * A0_SQT
    res['K1_slope_in_band'] = bool(k1)
    res['K2_within_1sigma_of_4'] = bool(k2)
    res['K3_aicc_supports_fixed4'] = bool(k3)
    res['K4_a0_recovered_matches_sqt'] = bool(k4)
    res['ALL_PASS'] = bool(k1 and k2 and k3 and k4)
    print(f"  K1 slope in [3.8,4.2]            : {k1}")
    print(f"  K2 |slope-4| <= 1*sigma          : {k2}")
    print(f"  K3 free vs fixed4 AICc           : {k3}")
    print(f"  K4 a0 recovered ~ SQT a0 (x1.5)  : {k4}")
    print(f"  ALL_PASS                          : {res['ALL_PASS']}")
    return res


def main() -> int:
    here = Path(__file__).resolve().parent
    sparc_path = here.parent / 'l49' / 'data' / 'sparc_catalog.mrt'
    if not sparc_path.exists():
        print(f"SPARC catalog not found at {sparc_path}", file=sys.stderr)
        return 1

    rows = parse_sparc(sparc_path)
    print(f"Parsed {len(rows)} catalog rows from {sparc_path}")
    print(f"H0 = {H0_KMSMPC} km/s/Mpc -> a0_SQT = c*H0/(2pi) = {A0_SQT:.4e} m/s^2")
    print(f"McGaugh observed a0 = {A0_OBS:.4e} m/s^2  (ratio SQT/obs = {A0_SQT/A0_OBS:.3f})")

    out: dict = dict(
        H0_kms_Mpc=H0_KMSMPC,
        a0_SQT=A0_SQT,
        a0_McGaugh=A0_OBS,
        Upsilon_star=UPSILON_STAR,
        He_factor=HE_FACTOR,
        n_catalog=len(rows),
    )

    out['cut_A_Q12'] = run_one(rows, q_max=2, label='Cut A (Q<=2)')
    print()
    out['cut_B_Q1'] = run_one(rows, q_max=1, label='Cut B (Q=1 only)')

    out_path = here / 'L422_btfr_results.json'
    with out_path.open('w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, default=float)
    print(f"\nWrote {out_path}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
