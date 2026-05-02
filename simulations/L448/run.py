"""L448 — BTFR zero-point (a_0 intercept) a priori test against SPARC.

L422 slope (bisector ~3.58-3.70) failed K1/K2 vs predicted 4.0.
This script tests the *intercept* channel independently:
fix slope = 4 exactly, recover a_0_eff, and compare to SQT a_0 = c*H0/(2pi).

Outputs:
  - results/L448/L448_results.json
  - prints PASS/FAIL for K_Z1..K_Z4
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Constants (SI)
# ---------------------------------------------------------------------------
C_LIGHT = 2.99792458e8
G_NEWT = 6.67430e-11
MPC = 3.0857e22
MSUN = 1.98892e30
KM = 1.0e3

H0_PLANCK = 67.4    # km/s/Mpc (Planck 2018)
H0_RIESS = 73.04    # km/s/Mpc (SH0ES 2022)

UPSILON_STAR_DEFAULT = 0.5
HE_FACTOR = 1.33

A0_MCGAUGH = 1.20e-10  # observed BTFR a0 (McGaugh 2012)


def a0_sqt(h0_kmsmpc: float) -> float:
    h0_si = h0_kmsmpc * KM / MPC
    return C_LIGHT * h0_si / (2.0 * math.pi)


# ---------------------------------------------------------------------------
# SPARC parser (whitespace-tokenized; identical convention to L422)
# ---------------------------------------------------------------------------
def parse_sparc(path: Path) -> list[dict]:
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
            if len(tok) < 18:
                continue
            try:
                name = tok[0]
                D = float(tok[2])
                Inc = float(tok[5])
                L36 = float(tok[7])
                MHI = float(tok[13])
                Vflat = float(tok[15])
                e_Vf = float(tok[16])
                Q = int(tok[17])
            except (ValueError, IndexError):
                continue
            rows.append(dict(
                name=name, D=D, Inc=Inc, L36=L36, MHI=MHI,
                Vflat=Vflat, e_Vflat=e_Vf, Q=Q,
            ))
    return rows


# ---------------------------------------------------------------------------
# Sample build
# ---------------------------------------------------------------------------
def build_sample(rows: list[dict], q_max: int, ups_star: float) -> dict:
    V = []          # m/s
    e_V = []        # m/s
    Mb = []         # kg
    names = []
    for r in rows:
        if not (r['Vflat'] > 0 and r['e_Vflat'] > 0):
            continue
        if not (r['Q'] >= 1 and r['Q'] <= q_max):
            continue
        if not (r['L36'] > 0 or r['MHI'] > 0):
            continue
        M_star = ups_star * max(r['L36'], 0.0) * 1e9 * MSUN
        M_gas = HE_FACTOR * max(r['MHI'], 0.0) * 1e9 * MSUN
        Mb_si = M_star + M_gas
        if Mb_si <= 0:
            continue
        V.append(r['Vflat'] * KM)
        e_V.append(r['e_Vflat'] * KM)
        Mb.append(Mb_si)
        names.append(r['name'])
    return dict(V=np.array(V), e_V=np.array(e_V), Mb=np.array(Mb), names=names)


# ---------------------------------------------------------------------------
# a_0_eff estimators with slope = 4 fixed.
#
# Per-galaxy: a_per = V^4 / (G * Mb).  In deep-MOND limit a_per = a_0.
# Three estimators:
#   (1) median of log10(a_per)       -> robust
#   (2) chi2 fit in log10 space (slope=4 fixed): minimise sum w_i (y_i - 4 x_i - b)^2
#       where y_i = log10 V_i (m/s), x_i ... wait we want intercept = -log10(G*a0)+stuff.
#       Easier: fit log10(a_per) = const, weighted.
#   (3) least-squares on V^4 = G*M*a0
# We use (1) (median) and (2) (weighted log-mean).
# Bootstrap + jackknife uncertainties for both.
# ---------------------------------------------------------------------------

def a_per(V: np.ndarray, Mb: np.ndarray) -> np.ndarray:
    return V ** 4 / (G_NEWT * Mb)


def weighted_log_mean(a: np.ndarray, e_log: np.ndarray) -> float:
    w = 1.0 / np.maximum(e_log, 1e-6) ** 2
    return float((np.log10(a) * w).sum() / w.sum())


def jackknife_sigma(values: np.ndarray, statistic) -> float:
    n = len(values)
    if n < 2:
        return float('nan')
    s_full = statistic(values)
    s_loo = np.array([statistic(np.delete(values, i)) for i in range(n)])
    s_mean = s_loo.mean()
    var = (n - 1) / n * np.sum((s_loo - s_mean) ** 2)
    return float(math.sqrt(var))


def bootstrap_sigma(values: np.ndarray, statistic, n_boot: int = 2000, seed: int = 1234) -> tuple:
    rng = np.random.default_rng(seed)
    n = len(values)
    boots = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n, size=n)
        boots[i] = statistic(values[idx])
    return float(boots.mean()), float(boots.std(ddof=1)), float(np.percentile(boots, 16)), float(np.percentile(boots, 84))


# ---------------------------------------------------------------------------
# Main per-cut analysis
# ---------------------------------------------------------------------------
def analyse_cut(sample: dict, label: str, h0_kmsmpc: float = H0_PLANCK) -> dict:
    V = sample['V']
    e_V = sample['e_V']
    Mb = sample['Mb']
    n = len(V)
    if n < 10:
        return dict(label=label, n=n, error='insufficient sample')

    ap = a_per(V, Mb)
    log_ap = np.log10(ap)

    # Fractional V error -> log error: d log V = e_V/(V ln 10)
    e_logV = e_V / (V * math.log(10.0))
    e_log_ap = 4.0 * e_logV
    e_log_ap = np.sqrt(e_log_ap ** 2 + 0.10 ** 2)  # 0.1 dex intrinsic scatter floor

    # Estimators
    median_log = float(np.median(log_ap))
    a0_median = 10.0 ** median_log

    wlm = weighted_log_mean(ap, e_log_ap)
    a0_wlm = 10.0 ** wlm

    # Uncertainties on a0_median via bootstrap of log_ap median
    def med_stat(arr):
        return float(np.median(arr))

    boot_mean, boot_sd, boot_p16, boot_p84 = bootstrap_sigma(log_ap, med_stat, n_boot=4000, seed=42)
    jk_sd_median = jackknife_sigma(log_ap, med_stat)
    a0_p16 = 10.0 ** boot_p16
    a0_p84 = 10.0 ** boot_p84

    # SQT prediction at Planck H0
    a0_sqt_planck = a0_sqt(h0_kmsmpc)
    a0_sqt_riess = a0_sqt(H0_RIESS)

    # sigma distance (median estimator, bootstrap sigma in log space)
    delta_log = math.log10(a0_median) - math.log10(a0_sqt_planck)
    sigma_log = boot_sd
    sigma_distance_planck = abs(delta_log) / max(sigma_log, 1e-6)

    delta_log_riess = math.log10(a0_median) - math.log10(a0_sqt_riess)
    sigma_distance_riess = abs(delta_log_riess) / max(sigma_log, 1e-6)

    delta_log_mcg = math.log10(a0_median) - math.log10(A0_MCGAUGH)
    sigma_distance_mcgaugh = abs(delta_log_mcg) / max(sigma_log, 1e-6)

    # Inverse: H0_required to make SQT a0 match recovered a0
    # a0_SQT = c*H0/(2pi*Mpc/km), so H0_req = a0 * 2pi * Mpc/(c*km)
    H0_req = a0_median * 2.0 * math.pi * MPC / (C_LIGHT * KM)

    # K-criteria (zero-point only)
    ratio = a0_sqt_planck / a0_median
    K_Z1 = abs(1.0 - ratio) <= 0.30
    K_Z2 = (a0_sqt_planck >= a0_p16 / (10 ** (boot_sd))) and (a0_sqt_planck <= a0_p84 * (10 ** (boot_sd)))
    # Simpler K_Z2: SQT within 2*boot_sd in log10 space
    K_Z2 = abs(delta_log) <= 2.0 * boot_sd
    K_Z3 = sigma_distance_mcgaugh <= 1.0  # data agrees with McGaugh
    K_Z3b = abs(math.log10(A0_MCGAUGH) - math.log10(a0_sqt_planck)) / max(sigma_log, 1e-6) <= 1.0
    # K_Z4 left for ups scan summary (set later)

    res = dict(
        label=label,
        n=n,
        h0_kmsmpc_used=h0_kmsmpc,
        a0_median=float(a0_median),
        a0_weighted_log_mean=float(a0_wlm),
        log10_a0_median=median_log,
        log10_a0_bootstrap_mean=float(boot_mean),
        log10_a0_bootstrap_sigma=float(boot_sd),
        log10_a0_p16=float(boot_p16),
        log10_a0_p84=float(boot_p84),
        a0_p16=float(a0_p16),
        a0_p84=float(a0_p84),
        log10_a0_jackknife_sigma=float(jk_sd_median),
        a0_sqt_planck=float(a0_sqt_planck),
        a0_sqt_riess=float(a0_sqt_riess),
        a0_mcgaugh=float(A0_MCGAUGH),
        ratio_sqt_over_data=float(ratio),
        delta_log_data_minus_sqt=float(delta_log),
        sigma_distance_planck=float(sigma_distance_planck),
        sigma_distance_riess=float(sigma_distance_riess),
        sigma_distance_mcgaugh=float(sigma_distance_mcgaugh),
        H0_required_kmsmpc=float(H0_req),
        H0_required_over_planck=float(H0_req / H0_PLANCK),
        K_Z1_within_30pct=bool(K_Z1),
        K_Z2_within_2sigma=bool(K_Z2),
        K_Z3_data_consistent_mcgaugh=bool(K_Z3),
        K_Z3b_sqt_consistent_mcgaugh=bool(K_Z3b),
    )
    return res


def upsilon_scan(rows: list[dict], q_max: int, ups_grid: list[float], h0_kmsmpc: float = H0_PLANCK) -> dict:
    out = {}
    a0_sqt_p = a0_sqt(h0_kmsmpc)
    for u in ups_grid:
        s = build_sample(rows, q_max=q_max, ups_star=u)
        ap = a_per(s['V'], s['Mb'])
        a0_med = float(np.median(ap))
        out[f"ups_{u:.2f}"] = dict(
            ups=u,
            n=int(len(ap)),
            a0_median=a0_med,
            ratio_sqt_over_data=float(a0_sqt_p / a0_med),
            delta_log_data_minus_sqt=float(math.log10(a0_med) - math.log10(a0_sqt_p)),
            within_30pct=bool(abs(1 - a0_sqt_p / a0_med) <= 0.30),
        )
    return out


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def main() -> int:
    here = Path(__file__).resolve().parent
    sparc_path = here.parent / 'l49' / 'data' / 'sparc_catalog.mrt'
    if not sparc_path.exists():
        print(f"SPARC catalog not found at {sparc_path}", file=sys.stderr)
        return 1

    rows = parse_sparc(sparc_path)
    print(f"Parsed {len(rows)} catalog rows")
    print(f"a0_SQT(Planck H0=67.4) = {a0_sqt(H0_PLANCK):.4e} m/s^2")
    print(f"a0_SQT(SH0ES H0=73.04) = {a0_sqt(H0_RIESS):.4e} m/s^2")
    print(f"a0_McGaugh             = {A0_MCGAUGH:.4e} m/s^2")
    print()

    out: dict = dict(
        H0_planck=H0_PLANCK,
        H0_riess=H0_RIESS,
        a0_sqt_planck=a0_sqt(H0_PLANCK),
        a0_sqt_riess=a0_sqt(H0_RIESS),
        a0_mcgaugh=A0_MCGAUGH,
        ups_star_default=UPSILON_STAR_DEFAULT,
        He_factor=HE_FACTOR,
        n_catalog=len(rows),
        cuts={},
    )

    for q_max, label in [(1, 'Q1'), (2, 'Q12'), (3, 'Q123')]:
        s = build_sample(rows, q_max=q_max, ups_star=UPSILON_STAR_DEFAULT)
        if len(s['V']) < 10:
            continue
        res = analyse_cut(s, label=f"cut_{label}")
        out['cuts'][label] = res
        print(f"--- cut {label}  n={res['n']} ---")
        print(f"  a0_median           = {res['a0_median']:.3e}  (log10 = {res['log10_a0_median']:.4f})")
        print(f"  a0_weighted_logmean = {res['a0_weighted_log_mean']:.3e}")
        print(f"  bootstrap sigma(log10) = {res['log10_a0_bootstrap_sigma']:.4f}")
        print(f"  68% interval [{res['a0_p16']:.3e}, {res['a0_p84']:.3e}]")
        print(f"  ratio  SQT/data     = {res['ratio_sqt_over_data']:.3f}")
        print(f"  sigma distance (Planck SQT)   = {res['sigma_distance_planck']:.2f}")
        print(f"  sigma distance (Riess  SQT)   = {res['sigma_distance_riess']:.2f}")
        print(f"  sigma distance (McGaugh obs)  = {res['sigma_distance_mcgaugh']:.2f}")
        print(f"  H0 required to match data     = {res['H0_required_kmsmpc']:.2f} km/s/Mpc"
              f"  ({res['H0_required_over_planck']*100:.1f}% of Planck)")
        print(f"  K_Z1 (within 30%)             = {res['K_Z1_within_30pct']}")
        print(f"  K_Z2 (within 2 sigma)         = {res['K_Z2_within_2sigma']}")
        print(f"  K_Z3 (data ~ McGaugh)         = {res['K_Z3_data_consistent_mcgaugh']}")
        print(f"  K_Z3b (SQT ~ McGaugh)         = {res['K_Z3b_sqt_consistent_mcgaugh']}")
        print()

    # Upsilon scan on Q12
    print("--- Upsilon* sensitivity scan (cut Q12) ---")
    scan = upsilon_scan(rows, q_max=2, ups_grid=[0.30, 0.40, 0.50, 0.60, 0.70])
    for key, v in scan.items():
        print(f"  Ups={v['ups']:.2f}  n={v['n']}  a0_med={v['a0_median']:.3e}  ratio_SQT/data={v['ratio_sqt_over_data']:.3f}  within_30pct={v['within_30pct']}")
    out['upsilon_scan_Q12'] = scan

    # K_Z4: stability under Ups in [0.4, 0.6]
    K_Z4 = all(scan[f"ups_{u:.2f}"]['within_30pct'] for u in [0.40, 0.50, 0.60])
    out['K_Z4_ups_stability'] = bool(K_Z4)
    print(f"\n  K_Z4 (Ups in [0.4,0.6] all within 30%) = {K_Z4}")

    # H0 scan: range of H0 producing consistent a0
    a0_target = out['cuts'].get('Q12', {}).get('a0_median')
    if a0_target:
        h0_lo = (a0_target * 0.7) * 2 * math.pi * MPC / (C_LIGHT * KM)
        h0_hi = (a0_target * 1.3) * 2 * math.pi * MPC / (C_LIGHT * KM)
        print(f"\n  H0 needed for SQT a0 within 30% of data Q12: [{h0_lo:.1f}, {h0_hi:.1f}] km/s/Mpc")
        out['H0_band_Q12_30pct'] = [float(h0_lo), float(h0_hi)]

    out_path = here.parent.parent / 'results' / 'L448' / 'L448_results.json'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open('w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, default=float)
    print(f"\nWrote {out_path}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
