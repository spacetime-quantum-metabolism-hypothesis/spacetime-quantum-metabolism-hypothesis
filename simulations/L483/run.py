"""L483 — BTFR FAIL re-framing.

L422/L448 BTFR slope=4 + a0=cH0/(2pi) test FAILed:
  bisector slope 3.58-3.70 (need 3.8-4.2),
  intercept 5.92 sigma off (a0_data ~ 1.53e-10 vs a0_SQT 1.04e-10),
  K-Z4 Upsilon* stability marginal (Q12 ups>=0.6 only).

This script tests four alternative framings to ask whether SQT survives
*outside* the V_flat^4 a priori channel:

  Channel A — RAR (radial acceleration relation) using resolved rotation
              curves. SQT predicts an interpolation function nu(y) with
              y = g_bar / a0; we fit g_obs = g_bar * nu(g_bar/a0) for SQT,
              MOND-simple, and McGaugh-2016 nu_e shapes, recovering a0.
              This is the *intermediate*-acceleration channel that the
              outer-only V_flat^4 BTFR collapses.

  Channel B — Outer-only RAR (deep-MOND, g_bar << a0). Restricts the RAR
              to points well below a0 to test the asymptotic relation
              g_obs = sqrt(g_bar * a0). Fits a0 directly.

  Channel C — Upsilon* re-fit. Re-derives BTFR slope and a0 with Upsilon*
              treated as a global free parameter (not McGaugh's 0.5 prior).
              Tests whether the K-Z4 marginal stability hides a Upsilon*
              degeneracy that, when broken by RAR, picks Upsilon* != 0.5.

  Channel D — Non-monotonic SQT deviation. SQT psi-conservation could
              imprint a *bend* in the RAR at a characteristic g_bar (e.g.
              g_bar ~ a0). We bin the residual log10(g_obs) - log10(g_MOND)
              vs log10(g_bar) and scan for a non-monotonic feature; if SQT
              predicts a bend the data does not show, that channel also
              fails.

A0 hypotheses tested:
  a0_SQT = c*H0/(2pi) = 1.042e-10 (Planck H0=67.4)
  a0_obs = 1.20e-10 (McGaugh 2016)

Output: simulations/L483/L483_results.json + console summary.
The MD report writes a "재현 path 있음 / 영구 실패" verdict on each channel.
"""

from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

# ---------- constants (SI) ----------
C_LIGHT = 2.99792458e8
G_NEWT  = 6.67430e-11
KPC     = 3.0857e19
MPC     = 3.0857e22
MSUN    = 1.98892e30
KM      = 1.0e3
H0_KMSMPC = 67.4
H0_SI = H0_KMSMPC * KM / MPC
A0_SQT = C_LIGHT * H0_SI / (2.0 * math.pi)   # ~1.042e-10
A0_OBS = 1.20e-10

UPSILON_STAR_DEFAULT = 0.5
HE_FACTOR = 1.33

HERE = Path(__file__).resolve().parent
SPARC_CAT = HERE.parent / 'l49' / 'data' / 'sparc_catalog.mrt'
SPARC_DIR = HERE.parent / 'l49' / 'data' / 'sparc'
RESULTS_DIR = HERE.parent.parent / 'results' / 'L483'


# ---------- catalog parsing (same as L422) ----------

def parse_sparc(path: Path) -> list[dict]:
    rows = []
    in_data = False
    dash = 0
    with path.open('r', encoding='ascii', errors='ignore') as fh:
        for line in fh:
            ln = line.rstrip('\n')
            if ln.startswith('---'):
                dash += 1
                if dash >= 4:
                    in_data = True
                continue
            if not in_data or not ln.strip():
                continue
            tok = ln.split()
            if len(tok) < 18:
                continue
            try:
                rows.append(dict(
                    name=tok[0], T=int(tok[1]), D=float(tok[2]), e_D=float(tok[3]),
                    Inc=float(tok[5]), e_Inc=float(tok[6]),
                    L36=float(tok[7]), e_L36=float(tok[8]),
                    MHI=float(tok[13]), Vflat=float(tok[15]), e_Vflat=float(tok[16]),
                    Q=int(tok[17]),
                ))
            except (ValueError, IndexError):
                continue
    return rows


# ---------- rotmod parsing ----------

def load_rotmod(name: str) -> dict | None:
    """Return per-galaxy {R[kpc], Vobs, eV, Vgas, Vdisk, Vbul} arrays, or None."""
    p = SPARC_DIR / f'{name}_rotmod.dat'
    if not p.exists():
        return None
    R, Vobs, eV, Vg, Vd, Vb = [], [], [], [], [], []
    try:
        for line in p.open('r', encoding='ascii', errors='ignore'):
            s = line.strip()
            if not s or s.startswith('#'):
                continue
            tok = s.split()
            if len(tok) < 6:
                continue
            try:
                R.append(float(tok[0]))
                Vobs.append(float(tok[1]))
                eV.append(float(tok[2]))
                Vg.append(float(tok[3]))
                Vd.append(float(tok[4]))
                Vb.append(float(tok[5]))
            except ValueError:
                continue
    except OSError:
        return None
    if len(R) < 3:
        return None
    return dict(R=np.array(R), Vobs=np.array(Vobs), eV=np.array(eV),
                Vgas=np.array(Vg), Vdisk=np.array(Vd), Vbul=np.array(Vb))


# ---------- RAR construction ----------

def build_rar(rows: list[dict], q_max: int, ups: float = UPSILON_STAR_DEFAULT,
              vmin: float = 5.0) -> dict:
    """Build (g_bar, g_obs, weight) from resolved rotmod files.

    g_bar = V_bar^2 / R, V_bar^2 = Upsilon*Vdisk^2 + 1.4*Vbul^2*ups + Vgas^2
            (we use ups for both disk and bulge mass-to-light; Vgas already
             includes He.)
    g_obs = V_obs^2 / R.
    """
    gbar_all, gobs_all, w_all, gname = [], [], [], []
    used = 0
    for r in rows:
        if r['Q'] < 1 or r['Q'] > q_max:
            continue
        rm = load_rotmod(r['name'])
        if rm is None:
            continue
        R = rm['R']
        if R.size < 3:
            continue
        # Convert to SI accelerations
        R_si = R * KPC
        Vbar2 = (ups * rm['Vdisk'] ** 2
                 + 1.4 * ups * rm['Vbul'] ** 2
                 + rm['Vgas'] ** 2) * (KM ** 2)
        Vobs2 = rm['Vobs'] ** 2 * (KM ** 2)
        gb = Vbar2 / R_si
        go = Vobs2 / R_si
        # filter: positive, finite, V_obs reasonable
        mask = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (rm['Vobs'] > vmin)
        if mask.sum() < 3:
            continue
        gbar_all.append(gb[mask])
        gobs_all.append(go[mask])
        # error weight ~ relative error of g_obs from V_obs error
        eg = 2.0 * rm['eV'][mask] / np.maximum(rm['Vobs'][mask], 1e-3)  # frac err in g_obs
        eg = np.where((eg > 0) & np.isfinite(eg), eg, 0.1)
        w_all.append(1.0 / np.maximum(eg, 0.05) ** 2)
        gname.append(np.full(mask.sum(), r['name']))
        used += 1
    if used == 0:
        return dict(g_bar=np.array([]), g_obs=np.array([]), w=np.array([]),
                    n_galaxies=0, n_points=0, names=[])
    return dict(
        g_bar=np.concatenate(gbar_all),
        g_obs=np.concatenate(gobs_all),
        w=np.concatenate(w_all),
        n_galaxies=used,
        n_points=int(np.concatenate(gbar_all).size),
        names=np.concatenate(gname),
    )


# ---------- interpolation functions nu(y) ----------

def nu_simple(y: np.ndarray) -> np.ndarray:
    """MOND simple: g_obs = g_bar * nu, nu(y) = 0.5 + sqrt(0.25 + 1/y)."""
    return 0.5 + np.sqrt(0.25 + 1.0 / np.maximum(y, 1e-30))


def nu_mcgaugh(y: np.ndarray) -> np.ndarray:
    """McGaugh 2016: g_obs = g_bar / (1 - exp(-sqrt(y))).
    => nu(y) = 1/(1 - exp(-sqrt(y)))."""
    s = np.sqrt(np.maximum(y, 1e-30))
    return 1.0 / (1.0 - np.exp(-s))


def nu_sqt_powerlaw(y: np.ndarray, n: float = 1.0) -> np.ndarray:
    """SQT-style ad hoc: nu(y) = (1 + y^{-n/2})^{1/n}.
    n=1 -> simple-like, n=2 -> standard, larger n sharper transition."""
    yy = np.maximum(y, 1e-30)
    return (1.0 + yy ** (-n / 2.0)) ** (1.0 / n)


# ---------- fitting ----------

def fit_a0(g_bar: np.ndarray, g_obs: np.ndarray, w: np.ndarray,
           nu_fn, a0_init: float = A0_SQT, extra_args=()) -> dict:
    """Fit a0 (and optionally extra params) so g_obs = g_bar * nu(g_bar/a0).
    Operates in log10. Returns chi2, dof, a0, etc."""
    log_go = np.log10(np.maximum(g_obs, 1e-30))
    log_gb = np.log10(np.maximum(g_bar, 1e-30))
    err_log = 1.0 / np.sqrt(np.maximum(w, 1e-12)) / math.log(10.0)
    err_log = np.maximum(err_log, 0.04)  # floor 0.04 dex

    def resid(theta):
        a0 = 10.0 ** theta[0]
        if len(theta) > 1:
            extra = theta[1:]
            mu = nu_fn(g_bar / a0, *extra)
        else:
            mu = nu_fn(g_bar / a0)
        gpred = g_bar * mu
        return (np.log10(np.maximum(gpred, 1e-30)) - log_go) / err_log

    x0 = [math.log10(a0_init)] + list(extra_args)
    try:
        sol = least_squares(resid, x0=x0, method='lm', max_nfev=2000)
    except Exception as exc:
        return dict(error=str(exc))
    a0_fit = 10.0 ** sol.x[0]
    res = resid(sol.x)
    chi2 = float((res ** 2).sum())
    dof = max(len(res) - len(x0), 1)
    rchi2 = chi2 / dof
    return dict(a0=a0_fit, log10_a0=float(sol.x[0]), extra=list(sol.x[1:]),
                chi2=chi2, dof=dof, rchi2=rchi2, n=len(res))


# ---------- channel A: full RAR ----------

def channel_A(rar: dict) -> dict:
    out = dict(channel='A_full_RAR', n_pts=rar['n_points'], n_gal=rar['n_galaxies'])
    if rar['n_points'] < 50:
        out['error'] = 'too few points'
        return out
    gb, go, w = rar['g_bar'], rar['g_obs'], rar['w']
    # fit each interpolation function
    out['fit_simple']    = fit_a0(gb, go, w, nu_simple)
    out['fit_mcgaugh']   = fit_a0(gb, go, w, nu_mcgaugh)
    # power-law n free
    out['fit_powerlaw']  = fit_a0(gb, go, w, nu_sqt_powerlaw, extra_args=(1.0,))
    # consistency vs SQT prediction (factor 1.5)
    for k in ('fit_simple', 'fit_mcgaugh', 'fit_powerlaw'):
        f = out[k]
        if 'a0' in f:
            f['ratio_vs_sqt']     = f['a0'] / A0_SQT
            f['ratio_vs_mcgaugh'] = f['a0'] / A0_OBS
            f['within_factor_1p5_sqt'] = bool(0.667 * A0_SQT <= f['a0'] <= 1.5 * A0_SQT)
    return out


# ---------- channel B: outer-only deep-MOND ----------

def channel_B(rar: dict, a0_thresh: float = A0_SQT) -> dict:
    """Deep-MOND limit: g_bar << a0 => g_obs = sqrt(g_bar * a0).
    Fit a0 from the mean (log g_obs - 0.5 log g_bar)."""
    out = dict(channel='B_outer_only')
    if rar['n_points'] == 0:
        out['error'] = 'empty'
        return out
    gb = rar['g_bar']; go = rar['g_obs']; w = rar['w']
    # restrict to deep-MOND: g_bar < a0_thresh / 10
    mask = gb < a0_thresh / 10.0
    out['n_pts_after_cut'] = int(mask.sum())
    if mask.sum() < 30:
        out['error'] = 'insufficient deep-MOND points (<30)'
        return out
    log_a0_pts = 2.0 * np.log10(go[mask]) - np.log10(gb[mask])
    a0_pts = 10.0 ** log_a0_pts
    ww = w[mask]
    log_a0_w = float(np.average(log_a0_pts, weights=ww))
    a0_fit = 10.0 ** log_a0_w
    # bootstrap sigma
    rng = np.random.default_rng(42)
    boot = []
    for _ in range(2000):
        idx = rng.integers(0, mask.sum(), size=mask.sum())
        boot.append(np.average(log_a0_pts[idx], weights=ww[idx]))
    boot = np.array(boot)
    out['a0_deep_MOND'] = a0_fit
    out['log10_a0_mean'] = log_a0_w
    out['log10_a0_sigma_boot'] = float(boot.std())
    out['ratio_vs_sqt'] = a0_fit / A0_SQT
    out['ratio_vs_mcgaugh'] = a0_fit / A0_OBS
    out['sigma_distance_sqt'] = abs(log_a0_w - math.log10(A0_SQT)) / max(boot.std(), 1e-6)
    out['within_factor_1p5_sqt'] = bool(0.667 * A0_SQT <= a0_fit <= 1.5 * A0_SQT)
    return out


# ---------- channel C: Upsilon* re-fit on RAR ----------

def channel_C(rows: list[dict], q_max: int = 2) -> dict:
    """Refit a0 jointly with Upsilon* over a grid; for each ups, build RAR,
    fit a0 with simple-nu, record chi2. Min chi2 picks Upsilon*."""
    out = dict(channel='C_upsilon_refit', q_max=q_max)
    grid = np.linspace(0.30, 0.80, 11)
    rows_out = []
    best = None
    for ups in grid:
        rar = build_rar(rows, q_max=q_max, ups=ups)
        if rar['n_points'] < 50:
            continue
        f = fit_a0(rar['g_bar'], rar['g_obs'], rar['w'], nu_simple)
        if 'chi2' not in f:
            continue
        row = dict(ups=float(ups), n_pts=rar['n_points'], n_gal=rar['n_galaxies'],
                   a0=f['a0'], chi2=f['chi2'], rchi2=f['rchi2'])
        rows_out.append(row)
        if best is None or f['chi2'] < best['chi2']:
            best = row
    out['scan'] = rows_out
    out['best'] = best
    if best is not None:
        out['best_ups'] = best['ups']
        out['best_a0'] = best['a0']
        out['ratio_vs_sqt'] = best['a0'] / A0_SQT
        out['breaks_ups_05_degeneracy'] = bool(abs(best['ups'] - 0.5) > 0.1)
    return out


# ---------- channel D: non-monotonic deviation ----------

def channel_D(rar: dict, a0: float = A0_SQT, n_bins: int = 12) -> dict:
    """Bin residuals delta = log10(g_obs) - log10(g_MOND-simple) vs log10(g_bar).
    SQT-distinct prediction would be a non-monotonic feature near g_bar ~ a0.
    Test for monotonicity via Spearman-like rank correlation of |delta_bin|."""
    out = dict(channel='D_nonmonotonic_deviation', a0_used=a0, n_bins=n_bins)
    if rar['n_points'] < 100:
        out['error'] = 'too few points for binning'
        return out
    gb, go = rar['g_bar'], rar['g_obs']
    pred = gb * nu_simple(gb / a0)
    delta = np.log10(go) - np.log10(pred)
    log_gb = np.log10(gb)
    edges = np.linspace(log_gb.min(), log_gb.max(), n_bins + 1)
    bin_centers, bin_means, bin_stds, bin_n = [], [], [], []
    for i in range(n_bins):
        m = (log_gb >= edges[i]) & (log_gb < edges[i + 1])
        if m.sum() < 5:
            continue
        bin_centers.append(0.5 * (edges[i] + edges[i + 1]))
        bin_means.append(float(delta[m].mean()))
        bin_stds.append(float(delta[m].std() / max(math.sqrt(m.sum()), 1.0)))
        bin_n.append(int(m.sum()))
    bin_centers = np.array(bin_centers); bin_means = np.array(bin_means)
    bin_stds = np.array(bin_stds)
    out['bin_centers_log_gbar'] = bin_centers.tolist()
    out['bin_mean_residual_dex'] = bin_means.tolist()
    out['bin_sigma_dex'] = bin_stds.tolist()
    out['bin_n'] = bin_n
    # quantify: max |residual| and where; sign changes
    if bin_means.size >= 3:
        out['max_abs_residual_dex'] = float(np.max(np.abs(bin_means)))
        out['max_residual_at_log_gbar'] = float(bin_centers[np.argmax(np.abs(bin_means))])
        sign_changes = int(np.sum(np.diff(np.sign(bin_means)) != 0))
        out['sign_changes'] = sign_changes
        # significance of largest deviation
        i_max = int(np.argmax(np.abs(bin_means)))
        out['max_dev_sigma'] = float(abs(bin_means[i_max]) / max(bin_stds[i_max], 1e-3))
        # SQT structural prediction would imprint multiple sign changes (>=2)
        out['nonmonotonic_evidence'] = bool(sign_changes >= 2 and out['max_dev_sigma'] > 3.0)
    return out


# ---------- main ----------

def main() -> int:
    if not SPARC_CAT.exists():
        print(f"missing catalog: {SPARC_CAT}")
        return 1
    rows = parse_sparc(SPARC_CAT)
    print(f"parsed {len(rows)} catalog rows")
    print(f"H0 = {H0_KMSMPC} km/s/Mpc  a0_SQT = {A0_SQT:.4e}  a0_McGaugh = {A0_OBS:.4e}")

    rar = build_rar(rows, q_max=2, ups=UPSILON_STAR_DEFAULT)
    print(f"RAR Q<=2 ups=0.5: n_gal={rar['n_galaxies']} n_pts={rar['n_points']}")

    out = dict(
        H0_kmsmpc=H0_KMSMPC,
        a0_sqt=A0_SQT, a0_mcgaugh=A0_OBS,
        upsilon_default=UPSILON_STAR_DEFAULT,
        n_catalog=len(rows),
        rar_n_galaxies=rar['n_galaxies'],
        rar_n_points=rar['n_points'],
    )

    print("\n--- Channel A: full RAR fits ---")
    A = channel_A(rar)
    out['channel_A'] = A
    for k in ('fit_simple', 'fit_mcgaugh', 'fit_powerlaw'):
        if k in A and 'a0' in A[k]:
            f = A[k]
            print(f"  {k}: a0={f['a0']:.3e}  ratio_SQT={f['ratio_vs_sqt']:.3f}  "
                  f"rchi2={f['rchi2']:.3f}  pass1p5={f['within_factor_1p5_sqt']}")

    print("\n--- Channel B: outer-only deep-MOND ---")
    B = channel_B(rar, a0_thresh=A0_SQT)
    out['channel_B'] = B
    if 'a0_deep_MOND' in B:
        print(f"  a0_deep={B['a0_deep_MOND']:.3e}  ratio_SQT={B['ratio_vs_sqt']:.3f}  "
              f"sigma_dist_SQT={B['sigma_distance_sqt']:.2f}  pass1p5={B['within_factor_1p5_sqt']}")
    else:
        print(f"  {B}")

    print("\n--- Channel C: Upsilon* refit ---")
    C = channel_C(rows, q_max=2)
    out['channel_C'] = C
    if C.get('best') is not None:
        b = C['best']
        print(f"  best ups={b['ups']:.2f}  a0={b['a0']:.3e}  rchi2={b['rchi2']:.3f}  "
              f"breaks_05={C['breaks_ups_05_degeneracy']}")

    print("\n--- Channel D: non-monotonic deviation ---")
    D = channel_D(rar, a0=A0_SQT, n_bins=12)
    out['channel_D'] = D
    if 'max_abs_residual_dex' in D:
        print(f"  max |res|={D['max_abs_residual_dex']:.3f} dex at log_gbar="
              f"{D['max_residual_at_log_gbar']:.2f}  sign_changes={D['sign_changes']}  "
              f"max_dev_sigma={D['max_dev_sigma']:.2f}  evidence={D['nonmonotonic_evidence']}")

    # ---------- verdict ----------
    verdict = dict()
    a0_simple = A['fit_simple'].get('a0', float('nan'))
    a0_mcg    = A['fit_mcgaugh'].get('a0', float('nan'))
    verdict['A_full_RAR_pass'] = bool(A['fit_simple'].get('within_factor_1p5_sqt', False)
                                      or A['fit_mcgaugh'].get('within_factor_1p5_sqt', False))
    verdict['B_deepMOND_pass']  = bool(B.get('within_factor_1p5_sqt', False))
    verdict['C_ups_refit_breaks_degeneracy'] = bool(C.get('breaks_ups_05_degeneracy', False))
    verdict['D_sqt_nonmonotonic_signal']    = bool(D.get('nonmonotonic_evidence', False))
    any_pass = any(verdict.values())
    verdict['ANY_REVIVAL_CHANNEL_PASS'] = any_pass
    out['verdict'] = verdict

    print("\n--- L483 verdict ---")
    for k, v in verdict.items():
        print(f"  {k}: {v}")

    out_path = HERE / 'L483_results.json'
    with out_path.open('w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, default=float)
    print(f"\nwrote {out_path}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
