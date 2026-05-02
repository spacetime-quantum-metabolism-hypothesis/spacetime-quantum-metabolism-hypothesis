"""L503 — RAR a0 universality test (per-galaxy, dwarf, cluster).

L482 found the SPARC-175-pooled RAR fit gives a0 ~ c H0 / (2 pi).
L489 audited functional-form sensitivity.
L492 audited subset (Q-cut, dwarf, bright) cross-dataset stability.

L503 asks the *per-galaxy universality* question (McGaugh-Lelli-Schombert
universality): is the SQT prediction a0 = c H0 / (2 pi) consistent with a
*single, environment-independent* acceleration scale, when each galaxy
gets its own free a0 ?

Procedure:
  - Fit a0_i for each SPARC galaxy individually (M16 functional form, locked
    Upsilon_disk = 0.5, Upsilon_bul = 0.7).
  - Build the per-galaxy log10(a0_i) distribution.
  - Compare its scatter against:
      (a) SPARC intrinsic scatter floor (sigma_log_floor = 0.13 dex,
          McGaugh+16 reported intrinsic scatter ~ 0.11 dex).
      (b) The SQT predicted value (locked at H0_Planck).
  - Split the per-galaxy a0 distribution by environment proxies:
        * dwarf  (V_flat <= 60 km/s, T >= 8) — LITTLE THINGS scale.
        * normal (60 < V_flat < 150 km/s).
        * bright (V_flat >= 150 km/s).
    Test if the *median* a0 differs between bins (KS / median test).
  - Add cluster RAR (Tian-Ko 2016 / Eckert+22) as literature: a0_cluster ~
    (5-10) x a0_SPARC.  Re-analysed = no (no on-disk cluster rotation curves
    in this repo); the literature value is a hard structural challenge for
    universality regardless.

PASS criterion (a priori, single line):
   per_galaxy_scatter_dex <= SPARC intrinsic scatter (0.13 dex)  AND
   |median(log a0) - log a0_SQT| <= 0.05 dex                     AND
   no significant environment trend (KS p > 0.05 between dwarf and bright).

Outputs:
  results/L503/L503_results.json
  results/L503/UNIVERSALITY.md
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar
from scipy import stats

C_LIGHT = 2.99792458e8
KPC = 3.0857e19
MPC = 3.0857e22
KM = 1.0e3

H0_PLANCK = 67.4
UPSILON_DISK = 0.5
UPSILON_BUL = 0.7
SIGMA_LOG_FLOOR = 0.13   # SPARC intrinsic scatter floor (McGaugh+16: ~0.11-0.13 dex).
SPARC_INTRINSIC_DEX = 0.13


def a0_sqt(h0_kmsmpc: float) -> float:
    h0_si = h0_kmsmpc * KM / MPC
    return C_LIGHT * h0_si / (2.0 * math.pi)


def parse_rotmod(path: Path) -> dict:
    Rs, Vo, eV, Vg, Vd, Vb = [], [], [], [], [], []
    with path.open('r', encoding='ascii', errors='ignore') as fh:
        for line in fh:
            s = line.strip()
            if not s or s.startswith('#'):
                continue
            tok = s.split()
            if len(tok) < 6:
                continue
            try:
                Rs.append(float(tok[0])); Vo.append(float(tok[1])); eV.append(float(tok[2]))
                Vg.append(float(tok[3])); Vd.append(float(tok[4])); Vb.append(float(tok[5]))
            except ValueError:
                continue
    return dict(name=path.stem.replace('_rotmod', ''),
                R=np.asarray(Rs), Vobs=np.asarray(Vo), errV=np.asarray(eV),
                Vgas=np.asarray(Vg), Vdisk=np.asarray(Vd), Vbul=np.asarray(Vb))


def parse_catalog(path: Path) -> dict:
    out = {}
    sep_count = 0
    with path.open('r', encoding='ascii', errors='ignore') as fh:
        for line in fh:
            stripped = line.rstrip('\n')
            if stripped and set(stripped) == {'-'} and len(stripped) >= 20:
                sep_count += 1
                continue
            if sep_count < 4:
                continue
            if not line.strip():
                continue
            tok = line.split()
            if len(tok) < 18:
                continue
            try:
                name = tok[0]
                T = int(tok[1])
                Vflat = float(tok[15])
                Q = int(tok[17])
            except (ValueError, IndexError):
                continue
            out[name] = dict(T=T, Vflat=Vflat, Q=Q)
    return out


def galaxy_g_arrays(g: dict):
    """Return per-galaxy (gbar, gobs, e_gobs) arrays, or None if invalid."""
    R = g['R']
    if R.size == 0:
        return None
    Vobs = g['Vobs']; errV = g['errV']
    good = (R > 0) & (Vobs > 0) & (errV > 0)
    if not np.any(good):
        return None
    R_m = R[good] * KPC
    Vo = Vobs[good] * KM
    eV = errV[good] * KM
    Vd = g['Vdisk'][good] * KM
    Vb = g['Vbul'][good] * KM
    Vgs = g['Vgas'][good] * KM

    def sq_signed(arr):
        return np.sign(arr) * arr ** 2

    Vbar2 = UPSILON_DISK * sq_signed(Vd) + UPSILON_BUL * sq_signed(Vb) + sq_signed(Vgs)
    valid = Vbar2 > 0
    if not np.any(valid):
        return None
    R_m = R_m[valid]; Vo = Vo[valid]; eV = eV[valid]; Vbar2 = Vbar2[valid]
    gbar = Vbar2 / R_m
    gobs = Vo ** 2 / R_m
    e_gobs = 2.0 * Vo * eV / R_m
    return gbar, gobs, e_gobs


def mcgaugh_F(gbar: np.ndarray, a0: float) -> np.ndarray:
    x = np.sqrt(np.maximum(gbar / a0, 1e-300))
    den = 1.0 - np.exp(-x)
    return np.where(x > 1e-6, gbar / np.maximum(den, 1e-300), np.sqrt(gbar * a0))


def chi2_for_a0(gbar, gobs, sigma_log, a0):
    pred = mcgaugh_F(gbar, a0)
    res = (np.log10(gobs) - np.log10(pred)) / sigma_log
    return float(np.sum(res ** 2))


def fit_a0_galaxy(gbar, gobs, e_gobs):
    e_log = e_gobs / (np.maximum(gobs, 1e-300) * math.log(10.0))
    sigma_log = np.sqrt(e_log ** 2 + SIGMA_LOG_FLOOR ** 2)

    def obj(log10_a0):
        return chi2_for_a0(gbar, gobs, sigma_log, 10.0 ** log10_a0)

    res = minimize_scalar(obj, bounds=(-12.0, -8.0), method='bounded',
                          options=dict(xatol=1e-5))
    log10_a0_hat = res.x
    a0_hat = 10.0 ** log10_a0_hat
    chi2_min = res.fun
    n_pts = gbar.size
    chi2_per_dof = chi2_min / max(n_pts - 1, 1)
    # Δχ²=1 envelope for sigma(log a0)
    grid = np.linspace(log10_a0_hat - 0.40, log10_a0_hat + 0.40, 401)
    chi2_grid = np.array([obj(x) for x in grid])
    inside = grid[chi2_grid <= chi2_min + 1.0]
    sig = float(0.5 * (inside.max() - inside.min())) if inside.size >= 2 else float('nan')
    return dict(a0=float(a0_hat), log10_a0=float(log10_a0_hat),
                sigma_log10_a0=sig, chi2=float(chi2_min),
                chi2_per_dof=float(chi2_per_dof), n_pts=int(n_pts))


def main() -> int:
    here = Path(__file__).resolve().parent
    sparc_dir = here.parent / 'l49' / 'data' / 'sparc'
    cat_path = here.parent / 'l49' / 'data' / 'sparc_catalog.mrt'
    if not sparc_dir.exists() or not cat_path.exists():
        print('SPARC data missing', file=sys.stderr)
        return 1

    catalog = parse_catalog(cat_path)
    print(f'Catalog parsed: {len(catalog)} entries.')

    files = sorted(sparc_dir.glob('*_rotmod.dat'))
    galaxies_all = [parse_rotmod(p) for p in files]
    galaxies_all = [g for g in galaxies_all if g['R'].size >= 3]
    print(f'Loaded {len(galaxies_all)} rotmod galaxies (>=3 pts).')

    matched = 0
    for g in galaxies_all:
        meta = catalog.get(g['name'])
        g['Q'] = meta['Q'] if meta else -1
        g['Vflat'] = meta['Vflat'] if meta else -1.0
        g['T'] = meta['T'] if meta else -1
        if meta:
            matched += 1
    print(f'Matched catalogue metadata for {matched}/{len(galaxies_all)} galaxies.')

    a0_sqt_p = a0_sqt(H0_PLANCK)
    log10_a0_sqt = math.log10(a0_sqt_p)
    print(f'a0_SQT(Planck H0={H0_PLANCK}) = {a0_sqt_p:.4e} m/s^2')
    print(f'log10(a0_SQT) = {log10_a0_sqt:+.4f}')

    # Per-galaxy fit
    per_gal = []
    skipped = 0
    for g in galaxies_all:
        arr = galaxy_g_arrays(g)
        if arr is None:
            skipped += 1
            continue
        gbar, gobs, e_gobs = arr
        # Need enough points for a meaningful per-galaxy a0
        if gbar.size < 4:
            skipped += 1
            continue
        fit = fit_a0_galaxy(gbar, gobs, e_gobs)
        if not np.isfinite(fit['a0']) or fit['a0'] <= 0:
            skipped += 1
            continue
        # Drop pathological boundary fits
        if fit['log10_a0'] <= -11.9 or fit['log10_a0'] >= -8.1:
            skipped += 1
            continue
        fit.update(name=g['name'], Q=g['Q'], Vflat=g['Vflat'], T=g['T'])
        per_gal.append(fit)
    print(f'Per-galaxy fits: {len(per_gal)} (skipped {skipped}).')

    log_a0 = np.array([p['log10_a0'] for p in per_gal])
    weights = 1.0 / np.maximum(np.array([p['sigma_log10_a0'] for p in per_gal]), 0.02) ** 2

    median_log = float(np.median(log_a0))
    mean_log = float(np.average(log_a0, weights=weights))
    std_log = float(np.std(log_a0, ddof=1))
    mad = float(stats.median_abs_deviation(log_a0, scale='normal'))  # robust sigma
    p16, p84 = np.percentile(log_a0, [16, 84])
    iqr_sigma = float(0.5 * (p84 - p16))

    # Subtract typical per-galaxy fit uncertainty in quadrature -> intrinsic spread
    sig_fit = np.array([p['sigma_log10_a0'] for p in per_gal])
    sig_fit = sig_fit[np.isfinite(sig_fit)]
    median_sigfit = float(np.median(sig_fit))
    intrinsic_sq = std_log ** 2 - median_sigfit ** 2
    intrinsic_dex = float(math.sqrt(intrinsic_sq)) if intrinsic_sq > 0 else 0.0

    delta_median_vs_sqt = median_log - log10_a0_sqt
    delta_mean_vs_sqt = mean_log - log10_a0_sqt

    # Environment splits
    def split(condition):
        return [p for p in per_gal if condition(p)]

    g_dwarf  = split(lambda p: 0 < p['Vflat'] <= 60.0 and p['T'] >= 8)
    g_bright = split(lambda p: p['Vflat'] >= 150.0)
    g_normal = split(lambda p: 60.0 < p['Vflat'] < 150.0)

    def stat(gs, label):
        if not gs:
            return dict(label=label, n=0)
        x = np.array([p['log10_a0'] for p in gs])
        return dict(label=label, n=len(gs),
                    median_log10_a0=float(np.median(x)),
                    mean_log10_a0=float(np.mean(x)),
                    std_log10_a0=float(np.std(x, ddof=1) if x.size > 1 else 0.0),
                    delta_median_vs_SQT=float(np.median(x) - log10_a0_sqt))

    s_dwarf  = stat(g_dwarf,  'dwarf_LT_proxy')
    s_normal = stat(g_normal, 'normal_disk')
    s_bright = stat(g_bright, 'bright_disk')

    # KS / Mann-Whitney between dwarf and bright
    if g_dwarf and g_bright:
        x_d = np.array([p['log10_a0'] for p in g_dwarf])
        x_b = np.array([p['log10_a0'] for p in g_bright])
        ks_stat, ks_p = stats.ks_2samp(x_d, x_b)
        mw_stat, mw_p = stats.mannwhitneyu(x_d, x_b, alternative='two-sided')
    else:
        ks_stat = ks_p = mw_stat = mw_p = float('nan')

    # Cluster: literature only (no rotmod / lensing data here)
    cluster_lit = dict(
        reanalysed_here=False,
        references=[
            'Tian & Ko 2016 ApJ 818 32',
            'Pradel-Loubeyre style 2014',
            'Eckert et al. 2022 A&A 662 A123',
        ],
        a0_cluster_over_a0_SPARC_range=(5.0, 10.0),
        log10_a0_cluster_offset_dex=(math.log10(5.0), math.log10(10.0)),  # +0.70, +1.00 dex
        note=('Cluster RAR universally reports a0_cluster ~ (5-10) x a0_SPARC. '
              'A single SQT prediction a0 = cH0/(2 pi) cannot match both SPARC and '
              'cluster scales simultaneously. Universality fails on cluster scale '
              'regardless of SPARC-internal per-galaxy spread.'),
    )

    # PASS criteria
    K1_scatter_le_intrinsic = bool(intrinsic_dex <= SPARC_INTRINSIC_DEX)
    K2_median_close_to_SQT = bool(abs(delta_median_vs_sqt) <= 0.05)
    K3_no_env_trend = bool(np.isfinite(ks_p) and ks_p > 0.05)
    K4_cluster_consistent = False  # literature offset >= +0.70 dex >> any reasonable spread
    n_pass = sum([K1_scatter_le_intrinsic, K2_median_close_to_SQT,
                  K3_no_env_trend, K4_cluster_consistent])

    print('\n--- Per-galaxy a0 distribution (SPARC) ---')
    print(f'  N galaxies fitted     : {len(per_gal)}')
    print(f'  median log10(a0)      : {median_log:+.4f}  (a0 = {10**median_log:.3e})')
    print(f'  mean   log10(a0)      : {mean_log:+.4f}')
    print(f'  std    log10(a0)      : {std_log:.3f} dex')
    print(f'  MAD-sigma  log10(a0)  : {mad:.3f} dex')
    print(f'  IQR-sigma log10(a0)   : {iqr_sigma:.3f} dex')
    print(f'  median sigma_fit      : {median_sigfit:.3f} dex')
    print(f'  intrinsic spread      : {intrinsic_dex:.3f} dex')
    print(f'  log10(a0_SQT)         : {log10_a0_sqt:+.4f}')
    print(f'  Δ(median - SQT)       : {delta_median_vs_sqt:+.3f} dex')
    print(f'  Δ(mean   - SQT)       : {delta_mean_vs_sqt:+.3f} dex')

    print('\n--- Environment splits ---')
    for s in (s_dwarf, s_normal, s_bright):
        if s['n'] == 0:
            print(f'  {s["label"]:18s}: n=0 (no galaxies)')
        else:
            print(f'  {s["label"]:18s}: n={s["n"]:3d}  median={s["median_log10_a0"]:+.3f} '
                  f' Δ_SQT={s["delta_median_vs_SQT"]:+.3f}  std={s["std_log10_a0"]:.3f}')
    print(f'  KS dwarf-vs-bright   : stat={ks_stat:.3f}  p={ks_p:.3g}')
    print(f'  MW dwarf-vs-bright   : p={mw_p:.3g}')

    print('\n--- Universality K-criteria ---')
    print(f'  K1 intrinsic_dex <= 0.13   : {K1_scatter_le_intrinsic}  ({intrinsic_dex:.3f})')
    print(f'  K2 |median - SQT| <= 0.05  : {K2_median_close_to_SQT}  ({delta_median_vs_sqt:+.3f})')
    print(f'  K3 KS dwarf~bright p>0.05  : {K3_no_env_trend}  (p={ks_p:.3g})')
    print(f'  K4 cluster a0 ~ a0_SPARC   : {K4_cluster_consistent}  (literature: +0.70 to +1.00 dex)')
    print(f'  PASS: {n_pass}/4')

    if n_pass == 4:
        verdict = 'PASS — a0 universal across galaxies, environments, AND cluster scale.'
    elif n_pass == 3 and not K4_cluster_consistent:
        verdict = ('PARTIAL — universal within SPARC galaxies but FAILS at cluster scale '
                   '(structural single-a0 limit).')
    else:
        verdict = 'FAIL — a0 not universal; environment dependence and/or cluster mismatch.'

    out = dict(
        H0_planck=H0_PLANCK,
        a0_sqt_planck=float(a0_sqt_p),
        log10_a0_sqt=float(log10_a0_sqt),
        upsilon_disk=UPSILON_DISK, upsilon_bul=UPSILON_BUL,
        sigma_log_floor_dex=SIGMA_LOG_FLOOR,
        sparc_intrinsic_dex=SPARC_INTRINSIC_DEX,
        n_galaxies_fit=len(per_gal),
        per_galaxy=per_gal,
        per_galaxy_distribution=dict(
            median_log10_a0=median_log,
            mean_log10_a0=mean_log,
            std_log10_a0=std_log,
            mad_sigma_log10_a0=mad,
            iqr_sigma_log10_a0=iqr_sigma,
            median_sigma_fit_dex=median_sigfit,
            intrinsic_spread_dex=intrinsic_dex,
            delta_median_vs_SQT_dex=delta_median_vs_sqt,
            delta_mean_vs_SQT_dex=delta_mean_vs_sqt,
        ),
        environment_splits=dict(
            dwarf_LT_proxy=s_dwarf,
            normal_disk=s_normal,
            bright_disk=s_bright,
            ks_dwarf_vs_bright=dict(stat=float(ks_stat), p=float(ks_p)),
            mw_dwarf_vs_bright=dict(stat=float(mw_stat), p=float(mw_p)),
        ),
        clusters=cluster_lit,
        K_criteria=dict(
            K1_scatter_le_intrinsic=K1_scatter_le_intrinsic,
            K2_median_close_to_SQT=K2_median_close_to_SQT,
            K3_no_env_trend=K3_no_env_trend,
            K4_cluster_consistent=K4_cluster_consistent,
            n_pass=int(n_pass),
        ),
        verdict=verdict,
    )

    out_json = here.parent.parent / 'results' / 'L503' / 'L503_results.json'
    out_json.parent.mkdir(parents=True, exist_ok=True)
    with out_json.open('w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, default=float)
    print(f'\nWrote {out_json}')
    print(f'\nVERDICT: {verdict}')

    # ---- Markdown report ----
    md_path = here.parent.parent / 'results' / 'L503' / 'UNIVERSALITY.md'
    lines = []
    lines.append('# L503 — RAR a0 Universality Test (per-galaxy + environment + clusters)')
    lines.append('')
    lines.append(f'**Verdict (one line, honest):** {verdict}')
    lines.append('')
    lines.append('## 1. Setup')
    lines.append('- Data: SPARC 175 (Lelli et al. 2016 AJ 152 157); per-galaxy rotation curves.')
    lines.append(f'- Functional form: McGaugh 2016 (M16). Upsilon_disk={UPSILON_DISK}, Upsilon_bul={UPSILON_BUL}.')
    lines.append(f'- sigma_log floor = {SIGMA_LOG_FLOOR} dex (SPARC intrinsic scatter ~ 0.13 dex).')
    lines.append(f'- SQT prediction: a0 = c H0 / (2 pi). At H0 = {H0_PLANCK} km/s/Mpc -> a0 = {a0_sqt_p:.4e} m/s^2 '
                 f'(log10 = {log10_a0_sqt:+.4f}).')
    lines.append(f'- Clusters: literature only (Tian-Ko 2016, Eckert+22). a0_cluster ~ (5-10) x a0_SPARC.')
    lines.append('')
    lines.append('## 2. Per-galaxy a0 distribution')
    lines.append('')
    lines.append(f'- N galaxies (with valid 4+ point M16 fit, non-boundary): **{len(per_gal)}**')
    lines.append('')
    lines.append('| Statistic | Value (dex) |')
    lines.append('|---|---|')
    lines.append(f'| median log10(a0) | {median_log:+.4f} |')
    lines.append(f'| weighted mean log10(a0) | {mean_log:+.4f} |')
    lines.append(f'| std log10(a0) | {std_log:.3f} |')
    lines.append(f'| MAD-sigma | {mad:.3f} |')
    lines.append(f'| IQR-sigma | {iqr_sigma:.3f} |')
    lines.append(f'| median per-galaxy fit sigma | {median_sigfit:.3f} |')
    lines.append(f'| intrinsic spread (std^2 - sigma_fit^2)^{{1/2}} | **{intrinsic_dex:.3f}** |')
    lines.append(f'| Delta(median - SQT) | **{delta_median_vs_sqt:+.3f}** |')
    lines.append(f'| Delta(mean - SQT) | {delta_mean_vs_sqt:+.3f} |')
    lines.append('')
    lines.append('## 3. Environment splits (Vflat-based)')
    lines.append('')
    lines.append('| Bin | n | median log10 a0 | Delta vs SQT | std (dex) |')
    lines.append('|---|---|---|---|---|')
    for s in (s_dwarf, s_normal, s_bright):
        if s['n'] == 0:
            lines.append(f'| {s["label"]} | 0 | -- | -- | -- |')
        else:
            lines.append(f'| {s["label"]} | {s["n"]} | {s["median_log10_a0"]:+.3f} | '
                         f'{s["delta_median_vs_SQT"]:+.3f} | {s["std_log10_a0"]:.3f} |')
    lines.append('')
    lines.append(f'KS test (dwarf vs bright): stat={ks_stat:.3f}, p={ks_p:.3g}')
    lines.append(f'Mann-Whitney (dwarf vs bright): p={mw_p:.3g}')
    lines.append('')
    lines.append('## 4. Cluster scale (literature, not re-analysed)')
    lines.append('')
    lines.append('Tian & Ko 2016 ApJ 818 32; Eckert+22 A&A 662 A123; Pradel 2014.')
    lines.append('')
    lines.append('a0_cluster / a0_SPARC ~ 5 - 10 -> log10 offset = +0.70 to +1.00 dex.')
    lines.append('')
    lines.append('A single SQT prediction (a0 = c H0 / 2 pi) cannot reach cluster scale.')
    lines.append('This is the standard MOND "missing baryon" problem and applies identically to SQT.')
    lines.append('')
    lines.append('## 5. K-criteria')
    lines.append('')
    lines.append('| K | definition | result |')
    lines.append('|---|---|---|')
    lines.append(f'| K1 | intrinsic spread <= {SPARC_INTRINSIC_DEX} dex | '
                 f'{"PASS" if K1_scatter_le_intrinsic else "FAIL"} ({intrinsic_dex:.3f}) |')
    lines.append(f'| K2 | |median - SQT| <= 0.05 dex | '
                 f'{"PASS" if K2_median_close_to_SQT else "FAIL"} ({delta_median_vs_sqt:+.3f}) |')
    lines.append(f'| K3 | KS dwarf-vs-bright p > 0.05 | '
                 f'{"PASS" if K3_no_env_trend else "FAIL"} (p={ks_p:.3g}) |')
    lines.append(f'| K4 | cluster a0 within 0.10 dex of SPARC a0 | '
                 f'{"PASS" if K4_cluster_consistent else "FAIL"} (lit: +0.70 to +1.00 dex) |')
    lines.append('')
    lines.append(f'**PASS: {n_pass} / 4**')
    lines.append('')
    lines.append('## 6. One-line conclusion')
    lines.append('')
    lines.append(f'**{verdict}**')
    lines.append('')
    lines.append('## 7. Outputs')
    lines.append('- `simulations/L503/run.py`')
    lines.append('- `results/L503/L503_results.json`')
    lines.append('- `results/L503/UNIVERSALITY.md` (this file)')
    lines.append('')

    with md_path.open('w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))
    print(f'Wrote {md_path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
