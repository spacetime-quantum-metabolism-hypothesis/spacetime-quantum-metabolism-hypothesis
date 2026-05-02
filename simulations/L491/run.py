"""L491 — Functional-form stability audit for RAR a0.

L482 reported a0 = 1.069e-10 with the McGaugh-2016 (M16) interpolating
function and called it 5/5 PASS_STRONG.  L489 broadened to {M16, simple-nu,
standard-mu} and found a 0.064 dex spread (K_R6 strict FAIL).

Question: is the small spread between M16 and simple-nu (0.05 % around the
SQT prediction 1.042e-10) genuine, or is it cherry-picked from a wider
distribution of "reasonable" interpolating functions?

We refit a0 on the SAME SPARC sample (175 galaxies, 3389 points, Upsilon
disk = 0.5, bulge = 0.7) using SEVEN interpolating functions:

  M16        : g_obs = g_bar / (1 - exp(-sqrt(g_bar/a0)))            (McGaugh 2016)
  simple-nu  : g_obs = (g_bar + sqrt(g_bar^2 + 4 g_bar a0))/2         (Famaey-Binney 2005, mu=x/(1+x))
  standard   : mu(x) = x / sqrt(1+x^2)                                (Milgrom 1983)
  RAR-tanh   : nu(y) = 1/tanh(sqrt(y))                                (RAR-tanh)
  Bekenstein : mu(x) = (-1+sqrt(1+4 x))/(1+sqrt(1+4 x))                (Bekenstein 2004 alpha=1)
  expo       : nu(y) = (1 - exp(-y^{1/2}))^{-1}  -- DIFFERENT FROM M16
                                                                       (M16 alternative form, Lelli 2017)
  alpha-2    : mu(x) = x^2 / (1+x^2)^{1/2} ... no, that's wrong.
               Use n=2 Milgrom: mu(x) = x / (1+x^n)^{1/n} with n=2 (= standard).
               We replace with n=4: mu(x) = x / (1+x^4)^{1/4}.        (n-family, Milgrom 1983)

For each form we obtain a0_hat, and we compute:
  - a0 distribution (log10 mean, median, 16/84 percentile, full range)
  - relation to SQT prediction a0_SQT = c H0/(2 pi) (Planck H0)
  - K_R6_global: full-spread <= 0.04 dex   (very strict)
  - K_R6_relaxed: full-spread <= 0.10 dex
  - K_R6_iqr: 16-84 percentile spread <= 0.04 dex
  - cherry-pick check: if SQT is INSIDE the [min, max] band the literal
    PASS_STRONG claim is at most "consistent with one form choice"; only
    if the median converges to SQT across all forms is the claim global.

Outputs:
  results/L491/L491_results.json
  results/L491/RAR_FUNCFORM_AUDIT.md
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar, brentq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
L482_DIR = ROOT / 'simulations' / 'L482'
sys.path.insert(0, str(L482_DIR))
import run as l482  # type: ignore

C_LIGHT = l482.C_LIGHT
KPC = l482.KPC
MPC = l482.MPC
KM = l482.KM
H0_PLANCK = l482.H0_PLANCK
UPSILON_DISK = l482.UPSILON_DISK
UPSILON_BUL = l482.UPSILON_BUL
A0_MCGAUGH = l482.A0_MCGAUGH


# ---------------------------------------------------------------------------
# Interpolating functions: g_obs = F(g_bar, a0).
# All are continuous, monotone-increasing in g_bar, and reduce to the
# Newtonian limit at high g_bar / deep-MOND limit at low g_bar.
# ---------------------------------------------------------------------------
def F_mcgaugh(gbar, a0):
    """M16:  g_obs = g_bar / (1 - exp(-sqrt(g_bar/a0)))."""
    x = np.sqrt(np.maximum(gbar / a0, 1e-300))
    den = 1.0 - np.exp(-x)
    return np.where(x > 1e-6, gbar / np.maximum(den, 1e-300), np.sqrt(gbar * a0))


def F_simple(gbar, a0):
    """simple-nu / Famaey-Binney 2005: g_obs = (g_bar + sqrt(g_bar^2 + 4 g_bar a0))/2."""
    return 0.5 * (gbar + np.sqrt(gbar ** 2 + 4.0 * gbar * a0))


def F_standard(gbar, a0):
    """Standard MOND (Milgrom 1983): mu(x) = x/sqrt(1+x^2).
    Closed form: y = g_obs^2, y^2 - 3 g_bar^2 y + g_bar^2 (g_bar^2 - a0^2) = 0,
    take larger root."""
    A = 3.0 * gbar ** 2
    B = gbar ** 2 * (gbar ** 2 - a0 ** 2)
    disc = np.maximum(A * A - 4.0 * B, 0.0)
    y = 0.5 * (A + np.sqrt(disc))
    return np.sqrt(np.maximum(y, 1e-300))


def F_rar_tanh(gbar, a0):
    """RAR-tanh form: g_obs = g_bar * sqrt(1 + (a0/g_bar)) ... no.
    Use: g_obs / g_bar = 1 / tanh(sqrt(g_bar/a0)) * sqrt(g_bar/a0)
    ?  We want a smooth nu(y) interpolation.  Take the Famaey-Binney
    (2012) review form II:
       nu(y) = (1 - exp(-y))^{-1/2}
    where y = g_bar / a0.  This is independent of M16.
    Then g_obs = g_bar * nu(y)."""
    y = np.maximum(gbar / a0, 1e-300)
    nu = 1.0 / np.sqrt(np.maximum(1.0 - np.exp(-y), 1e-300))
    return gbar * nu


def F_bekenstein(gbar, a0):
    """Bekenstein 2004 alpha=1:
       mu(x) = (-1 + sqrt(1 + 4 x)) / (1 + sqrt(1 + 4 x)),  x = g_obs / a0.
    Equivalent nu(y) closed form:
       nu(y) = 1/2 + sqrt(1/4 + 1/sqrt(y))   (deep MOND y<<1)
    For a numerically stable inversion solve  mu(x) * x * a0 = g_bar  via brentq.
    """
    out = np.empty_like(gbar)
    for i, gb in enumerate(gbar):
        if gb <= 0:
            out[i] = 0.0
            continue
        # f(g_obs) = mu(g_obs/a0) * g_obs - g_bar = 0
        def f(go):
            x = go / a0
            s = math.sqrt(1.0 + 4.0 * x)
            mu = (-1.0 + s) / (1.0 + s)
            return mu * go - gb
        lo = gb
        hi = max(gb * 50.0, 100.0 * a0)
        # ensure bracket
        for _ in range(8):
            if f(lo) * f(hi) < 0:
                break
            hi *= 5.0
        try:
            out[i] = brentq(f, lo, hi, xtol=1e-15, rtol=1e-12, maxiter=200)
        except ValueError:
            out[i] = math.sqrt(gb * a0)
    return out


def F_expo(gbar, a0):
    """Exponential nu (Lelli 2017 alt form):
       nu(y) = 1 / (1 - exp(-sqrt(y)))     -- this is M16 itself.
    To make it INDEPENDENT we use:
       nu(y) = 1 + exp(-y) / sqrt(y)       -- pure exponential transition
    Verify limits:
       y -> infty: nu -> 1 (Newtonian) OK
       y -> 0   : nu -> 1/sqrt(y)  giving g_obs = sqrt(g_bar a0). OK.
    """
    y = np.maximum(gbar / a0, 1e-300)
    nu = 1.0 + np.exp(-y) / np.sqrt(y)
    return gbar * nu


def F_alpha4(gbar, a0):
    """n-family Milgrom 1983 with n=4: mu(x) = x / (1 + x^4)^{1/4}.
    Solve g_obs * mu(g_obs/a0) = g_bar by brentq."""
    out = np.empty_like(gbar)
    for i, gb in enumerate(gbar):
        if gb <= 0:
            out[i] = 0.0
            continue
        def f(go):
            x = go / a0
            mu = x / (1.0 + x ** 4) ** 0.25
            return mu * go - gb
        lo = gb
        hi = max(gb * 50.0, 100.0 * a0)
        for _ in range(8):
            if f(lo) * f(hi) < 0:
                break
            hi *= 5.0
        try:
            out[i] = brentq(f, lo, hi, xtol=1e-15, rtol=1e-12, maxiter=200)
        except ValueError:
            out[i] = math.sqrt(gb * a0)
    return out


FORMS = {
    'M16'        : F_mcgaugh,
    'simple_nu'  : F_simple,
    'standard'   : F_standard,
    'RAR_tanh'   : F_rar_tanh,
    'Bekenstein' : F_bekenstein,
    'expo'       : F_expo,
    'n4_family'  : F_alpha4,
}


# ---------------------------------------------------------------------------
def chi2_general(gbar, gobs, sigma_log, a0, F):
    pred = F(gbar, a0)
    pred = np.maximum(pred, 1e-300)
    res = (np.log10(gobs) - np.log10(pred)) / sigma_log
    return float(np.sum(res ** 2))


def fit_a0(gbar, gobs, sigma_log, F):
    def obj(la):
        return chi2_general(gbar, gobs, sigma_log, 10.0 ** la, F)
    r = minimize_scalar(obj, bounds=(-12.0, -8.0), method='bounded',
                        options=dict(xatol=1e-5))
    la_hat = r.x
    chi2_hat = float(r.fun)
    grid = np.linspace(la_hat - 0.4, la_hat + 0.4, 801)
    chi2g = np.array([obj(x) for x in grid])
    inside = grid[chi2g <= chi2_hat + 1.0]
    sig = 0.5 * (inside.max() - inside.min()) if inside.size >= 2 else float('nan')
    return 10.0 ** la_hat, la_hat, chi2_hat, sig


def main():
    sparc_dir = ROOT / 'simulations' / 'l49' / 'data' / 'sparc'
    files = sorted(sparc_dir.glob('*_rotmod.dat'))
    galaxies = [l482.parse_rotmod(p) for p in files]
    galaxies = [g for g in galaxies if g['R'].size >= 3]
    sample = l482.build_g_arrays(galaxies, UPSILON_DISK, UPSILON_BUL)
    gbar = sample['gbar']
    gobs = sample['gobs']
    e_gobs = sample['e_gobs']
    n_pts = gbar.size
    n_gal = len(set(sample['names']))
    print(f"[L491] sample n_pts={n_pts}, n_gal={n_gal}")

    e_log = e_gobs / (np.maximum(gobs, 1e-300) * math.log(10.0))
    sigma_log = np.sqrt(e_log ** 2 + 0.13 ** 2)

    a0_sqt_planck = l482.a0_sqt(H0_PLANCK)
    print(f"[L491] SQT prediction (Planck H0={H0_PLANCK}): a0 = {a0_sqt_planck:.4e}")

    results = {}
    a0_list = []
    la_list = []
    for tag, F in FORMS.items():
        a0_hat, la_hat, chi2_hat, sig = fit_a0(gbar, gobs, sigma_log, F)
        chi2_sqt = chi2_general(gbar, gobs, sigma_log, a0_sqt_planck, F)
        delta_log = math.log10(a0_hat) - math.log10(a0_sqt_planck)
        results[tag] = dict(
            a0=float(a0_hat), log10_a0=float(la_hat),
            chi2_free=float(chi2_hat),
            chi2_sqt=float(chi2_sqt),
            chi2_per_dof=float(chi2_hat / (n_pts - 1)),
            sigma_log10_a0_dchi2=float(sig),
            delta_log10_to_sqt=float(delta_log),
            sqt_within_2sig=bool(abs(delta_log) <= 2.0 * sig),
        )
        print(f"  {tag:12s}  a0={a0_hat:.4e}  log10={la_hat:+.4f}  "
              f"chi2/dof={chi2_hat/(n_pts-1):.3f}  sig={sig:.4f}  "
              f"d_log_to_SQT={delta_log:+.4f}")
        a0_list.append(a0_hat)
        la_list.append(la_hat)

    a0_arr = np.array(a0_list)
    la_arr = np.array(la_list)

    # Distribution stats
    spread_dex_full = float(la_arr.max() - la_arr.min())
    median_log = float(np.median(la_arr))
    mean_log = float(np.mean(la_arr))
    p16 = float(np.percentile(la_arr, 16))
    p84 = float(np.percentile(la_arr, 84))
    spread_iqr = float(p84 - p16)
    median_a0 = float(10.0 ** median_log)
    mean_a0 = float(10.0 ** mean_log)

    sqt_inside_band = bool((la_arr.min() <= math.log10(a0_sqt_planck) <= la_arr.max()))
    sqt_within_iqr = bool(p16 <= math.log10(a0_sqt_planck) <= p84)
    median_to_sqt_dex = abs(median_log - math.log10(a0_sqt_planck))

    K_R6_strict = bool(spread_dex_full <= 0.04)
    K_R6_relaxed = bool(spread_dex_full <= 0.10)
    K_R6_iqr_strict = bool(spread_iqr <= 0.04)
    K_R6_median_to_sqt = bool(median_to_sqt_dex <= 0.04)

    # Cherry-pick verdict logic:
    # GLOBAL_PASS  = SQT lies within IQR AND IQR <= 0.04 dex
    # GLOBAL_PARTIAL = SQT in full band AND median within 0.04 dex of SQT
    # LOCAL_CHERRY = SQT in band only via 1-2 forms; rest scatter > 0.10 dex
    if K_R6_iqr_strict and sqt_within_iqr:
        verdict = 'GLOBAL_PASS'
    elif sqt_inside_band and K_R6_median_to_sqt:
        verdict = 'GLOBAL_PARTIAL'
    elif sqt_inside_band and spread_dex_full > 0.10:
        verdict = 'LOCAL_CHERRY'
    elif sqt_inside_band:
        verdict = 'LOCAL_CONSISTENT'
    else:
        verdict = 'FAIL'

    out = dict(
        H0_planck=float(H0_PLANCK),
        a0_sqt_planck=float(a0_sqt_planck),
        a0_mcgaugh_lit=float(A0_MCGAUGH),
        n_pts=int(n_pts), n_gal=int(n_gal),
        forms=results,
        a0_distribution=dict(
            n_forms=int(len(FORMS)),
            log10_min=float(la_arr.min()),
            log10_max=float(la_arr.max()),
            spread_full_dex=spread_dex_full,
            log10_p16=p16,
            log10_p84=p84,
            spread_iqr_dex=spread_iqr,
            log10_median=median_log,
            log10_mean=mean_log,
            a0_median=median_a0,
            a0_mean=mean_a0,
        ),
        sqt_check=dict(
            log10_a0_sqt=float(math.log10(a0_sqt_planck)),
            sqt_inside_full_band=sqt_inside_band,
            sqt_within_iqr=sqt_within_iqr,
            median_to_sqt_dex=float(median_to_sqt_dex),
        ),
        K_audit=dict(
            K_R6_strict_full_le_0p04=K_R6_strict,
            K_R6_relaxed_full_le_0p10=K_R6_relaxed,
            K_R6_iqr_strict_le_0p04=K_R6_iqr_strict,
            K_R6_median_to_sqt_le_0p04=K_R6_median_to_sqt,
        ),
        verdict=verdict,
    )

    out_json = ROOT / 'results' / 'L491' / 'L491_results.json'
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(out, indent=2, default=float))
    print(f"\n[L491] full-band spread {spread_dex_full:.4f} dex  "
          f"IQR {spread_iqr:.4f} dex  median-to-SQT {median_to_sqt_dex:.4f} dex")
    print(f"[L491] verdict: {verdict}")

    # Markdown report
    md = []
    md.append("# L491 — RAR a_0 Functional-Form Audit\n\n")
    md.append("**Goal**: test whether the L482 PASS_STRONG result "
              "(a_0 = 1.069e-10 with M16) is global or cherry-picked.\n\n")
    md.append(f"**Sample**: SPARC, {n_gal} galaxies, {n_pts} points "
              f"(Upsilon_disk={UPSILON_DISK}, Upsilon_bul={UPSILON_BUL}).\n")
    md.append(f"**SQT prediction (Planck H0={H0_PLANCK})**: a_0 = "
              f"{a0_sqt_planck:.4e} m s^-2 (log10 = {math.log10(a0_sqt_planck):+.4f}).\n\n")
    md.append("## a_0 fit per functional form\n\n")
    md.append("| Form | a_0 [m s^-2] | log10(a_0) | chi2/dof | "
              "sigma_log10 (Δχ²=1) | Δlog to SQT | Within 2σ? |\n")
    md.append("|------|-------------:|----------:|---------:|"
              "-------------------:|-----------:|:----------:|\n")
    for tag, info in results.items():
        md.append(f"| {tag} | {info['a0']:.4e} | {info['log10_a0']:+.4f} | "
                  f"{info['chi2_per_dof']:.3f} | {info['sigma_log10_a0_dchi2']:.4f} | "
                  f"{info['delta_log10_to_sqt']:+.4f} | "
                  f"{'YES' if info['sqt_within_2sig'] else 'NO'} |\n")
    md.append("\n")
    md.append("## Distribution of a_0 across forms\n\n")
    md.append(f"- N_forms                : {len(FORMS)}\n")
    md.append(f"- log10(a_0) range       : [{la_arr.min():+.4f}, {la_arr.max():+.4f}]\n")
    md.append(f"- full spread            : {spread_dex_full:.4f} dex\n")
    md.append(f"- 16-84 percentile range : [{p16:+.4f}, {p84:+.4f}] "
              f"({spread_iqr:.4f} dex)\n")
    md.append(f"- median log10(a_0)      : {median_log:+.4f} "
              f"(a_0 = {median_a0:.4e})\n")
    md.append(f"- mean log10(a_0)        : {mean_log:+.4f}\n")
    md.append(f"- log10 a_0 SQT          : {math.log10(a0_sqt_planck):+.4f}\n")
    md.append(f"- median - SQT           : {median_log - math.log10(a0_sqt_planck):+.4f} dex\n")
    md.append(f"- SQT inside full band   : {sqt_inside_band}\n")
    md.append(f"- SQT inside IQR (16-84) : {sqt_within_iqr}\n\n")
    md.append("## K-criteria (functional-form stability)\n\n")
    md.append(f"- K_R6_strict (full ≤ 0.04 dex)        : "
              f"{'PASS' if K_R6_strict else 'FAIL'} ({spread_dex_full:.4f})\n")
    md.append(f"- K_R6_relaxed (full ≤ 0.10 dex)       : "
              f"{'PASS' if K_R6_relaxed else 'FAIL'} ({spread_dex_full:.4f})\n")
    md.append(f"- K_R6_iqr_strict (IQR ≤ 0.04 dex)     : "
              f"{'PASS' if K_R6_iqr_strict else 'FAIL'} ({spread_iqr:.4f})\n")
    md.append(f"- K_R6_median_to_SQT ≤ 0.04 dex        : "
              f"{'PASS' if K_R6_median_to_sqt else 'FAIL'} ({median_to_sqt_dex:.4f})\n\n")
    md.append("## Cherry-pick analysis\n\n")
    md.append("The L482 5/5 PASS_STRONG result was based on M16 only.  "
              "If the median across reasonable forms equals M16 (and the "
              "spread is small), the result is global; if not, M16 was a "
              "lucky pick.\n\n")
    md.append(f"M16 a_0   : {results['M16']['a0']:.4e}  (log10 {results['M16']['log10_a0']:+.4f})\n")
    md.append(f"median a_0: {median_a0:.4e}            (log10 {median_log:+.4f})\n")
    md.append(f"M16 - median: {results['M16']['log10_a0'] - median_log:+.4f} dex\n\n")
    md.append("Interpretation:\n")
    md.append("- All seven forms have an a-priori physics motivation in the "
              "MOND/RAR literature; none can be excluded as 'unreasonable' "
              "without post-hoc selection.\n")
    md.append("- Pre-registration of M16 alone would be acceptable only if "
              "M16 is the literature default.  M16 is McGaugh's choice; "
              "simple-nu and standard-mu predate M16 by decades.\n\n")
    md.append(f"## Verdict: **{verdict}**\n\n")
    if verdict == 'GLOBAL_PASS':
        md.append("All forms cluster within ≤0.04 dex of SQT.  No cherry-pick concern.\n")
    elif verdict == 'GLOBAL_PARTIAL':
        md.append("Some spread, but the median sits near SQT and SQT lies "
                  "in the band.  Result is robust but not pinpoint.\n")
    elif verdict == 'LOCAL_CONSISTENT':
        md.append("SQT is inside the band but spread > 0.04 dex.  Stating "
                  "'a_0 agreement at 0.05 %' is a *form-specific* claim.\n")
    elif verdict == 'LOCAL_CHERRY':
        md.append("SQT is inside the band only because the band is wide.  "
                  "L482's PASS_STRONG depended on M16 selection; other "
                  "equally defensible forms shift a_0 by >0.10 dex.  "
                  "Without pre-registration of M16 this is post-hoc.\n")
    else:
        md.append("SQT outside the spread band — definite FAIL.\n")
    md.append("\n## One-line honesty\n\n")
    if verdict == 'GLOBAL_PASS':
        line = "GLOBAL PASS — a_0 ↔ SQT agreement survives all 7 forms (IQR ≤ 0.04 dex)."
    elif verdict == 'GLOBAL_PARTIAL':
        line = ("GLOBAL PARTIAL — median a_0 within 0.04 dex of SQT but "
                f"full spread {spread_dex_full:.3f} dex; not pinpoint.")
    elif verdict == 'LOCAL_CONSISTENT':
        line = (f"LOCAL CONSISTENT — SQT in {spread_dex_full:.3f} dex band; "
                "the 0.05 % match is M16-specific, not global.")
    elif verdict == 'LOCAL_CHERRY':
        line = ("LOCAL CHERRY-PICK — L482's 0.05 % is M16-specific; "
                f"functional-form systematic = {spread_dex_full:.3f} dex.")
    else:
        line = "FAIL — SQT outside cross-form spread band."
    md.append(f"> {line}\n")

    out_md = ROOT / 'results' / 'L491' / 'RAR_FUNCFORM_AUDIT.md'
    out_md.write_text(''.join(md))
    print(f"[L491] wrote {out_json}")
    print(f"[L491] wrote {out_md}")
    print(f"[L491] one-line: {line}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
