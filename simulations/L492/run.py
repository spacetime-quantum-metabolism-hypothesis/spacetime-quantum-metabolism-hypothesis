"""L492 — RAR cross-dataset stability audit.

L482 found a single-dataset (SPARC 175) RAR fit with a0 ~ c H0/(2 pi) (SQT prediction).
L489 audited functional-form sensitivity within SPARC.

L492 asks the *complementary* question: is the a0 estimate stable when we change the
*galaxy sample*?  We re-run the same M16-functional RAR fit on:

  D1: SPARC 175 (full)         — L482 baseline.
  D2: SPARC Q=1 (high quality) — Lelli+16 quality flag 1.
  D3: SPARC Q in {1,2}         — drop the lowest-quality (Q=3) galaxies.
  D4: SPARC dwarf-disc proxy   — V_flat <= 60 km/s; LITTLE THINGS scale.
  D5: SPARC bright-disc        — V_flat >= 150 km/s.

For each subset we report:
  - n_galaxies, n_radial_points
  - a0_RAR (free-fit)        +/- sigma_log10
  - chi2 / dof (M16-locked at a0_RAR)
  - delta_log = log10(a0_RAR / a0_SQT(Planck))
  - SQT-locked chi2 / dof   (a0 fixed = c H0_Planck / 2pi)

Cross-spread metric:
  spread_dex = std( log10(a0_RAR_per_dataset) )
  max_dev_from_SQT = max | log10(a0_RAR / a0_SQT) |

Audit verdict logic (a priori):
  K_X1 spread_dex <= 0.05    (within McGaugh systematic ~0.09 dex)
  K_X2 max_dev_from_SQT <= 0.10  (1 sigma McGaugh systematic)
  K_X3 every subset has chi2/dof <= 1.6 with SQT-locked a0
  K_X4 sign of (a0_RAR - a0_SQT) is not consistently positive across subsets
       (i.e., subsets do not all systematically drift away from SQT)

Galaxy clusters (D6) are NOT re-analysed here: the SPARC rotmod files do not include
clusters; the Pradel et al. 2014 / Tian-Ko 2016 / Eckert+22 cluster RAR analyses
report a0_cluster ~ (5-10) x a0_SPARC (the well-known "MOND cluster missing-baryon
problem").  We record this as a literature reference and a known structural failure
of background-only RAR universality.

Outputs:
  results/L492/RAR_DATASET_AUDIT.md
  results/L492/L492_results.json
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar

C_LIGHT = 2.99792458e8
G_NEWT = 6.67430e-11
KPC = 3.0857e19
MPC = 3.0857e22
KM = 1.0e3

H0_PLANCK = 67.4
UPSILON_DISK = 0.5
UPSILON_BUL = 0.7
SIGMA_LOG_FLOOR = 0.13


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
    """Return {galaxy_name : {Q, Vflat, T}} from SPARC MRT table."""
    out = {}
    in_data = False
    sep_count = 0
    with path.open('r', encoding='ascii', errors='ignore') as fh:
        for line in fh:
            stripped = line.rstrip('\n')
            # A separator is a line consisting entirely of '-' characters (>=20).
            if stripped and set(stripped) == {'-'} and len(stripped) >= 20:
                sep_count += 1
                # MRT layout: separators at #1 (after header), #2 (after byte spec),
                # #3 (after refs/notes). Data block starts after the 4th separator.
                continue
            if sep_count < 4:
                continue
            in_data = True
            if not line.strip():
                continue
            tok = line.split()
            # Expected layout: name T D e_D f_D Inc e_Inc L eL Reff SBeff Rdisk SBdisk MHI RHI Vflat e_Vflat Q Ref
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


def build_g_arrays(galaxies: list[dict]) -> dict:
    gbar_all, gobs_all, eg_all, gname_all = [], [], [], []
    for g in galaxies:
        R = g['R']
        if R.size == 0:
            continue
        Vobs = g['Vobs']; errV = g['errV']
        good = (R > 0) & (Vobs > 0) & (errV > 0)
        if not np.any(good):
            continue
        R_m = R[good] * KPC
        Vo = Vobs[good] * KM
        eV = errV[good] * KM
        def sq_signed(arr):
            return np.sign(arr) * arr ** 2
        Vd = g['Vdisk'][good] * KM
        Vb = g['Vbul'][good] * KM
        Vg = g['Vgas'][good] * KM
        Vbar2 = UPSILON_DISK * sq_signed(Vd) + UPSILON_BUL * sq_signed(Vb) + sq_signed(Vg)
        valid = Vbar2 > 0
        if not np.any(valid):
            continue
        R_m = R_m[valid]; Vo = Vo[valid]; eV = eV[valid]; Vbar2 = Vbar2[valid]
        gbar = Vbar2 / R_m
        gobs = Vo ** 2 / R_m
        e_gobs = 2.0 * Vo * eV / R_m
        gbar_all.append(gbar); gobs_all.append(gobs); eg_all.append(e_gobs)
        gname_all.extend([g['name']] * len(gbar))
    if not gbar_all:
        return dict(gbar=np.array([]), gobs=np.array([]), e_gobs=np.array([]), names=[])
    return dict(gbar=np.concatenate(gbar_all),
                gobs=np.concatenate(gobs_all),
                e_gobs=np.concatenate(eg_all),
                names=gname_all)


def mcgaugh_F(gbar: np.ndarray, a0: float) -> np.ndarray:
    x = np.sqrt(np.maximum(gbar / a0, 1e-300))
    den = 1.0 - np.exp(-x)
    return np.where(x > 1e-6, gbar / np.maximum(den, 1e-300), np.sqrt(gbar * a0))


def chi2_for_a0(gbar, gobs, sigma_log, a0):
    pred = mcgaugh_F(gbar, a0)
    res = (np.log10(gobs) - np.log10(pred)) / sigma_log
    return float(np.sum(res ** 2))


def fit_a0(gbar, gobs, sigma_log) -> tuple:
    def obj(log10_a0):
        return chi2_for_a0(gbar, gobs, sigma_log, 10.0 ** log10_a0)
    res = minimize_scalar(obj, bounds=(-12.0, -8.0), method='bounded',
                          options=dict(xatol=1e-5))
    log10_a0_hat = res.x
    a0_hat = 10.0 ** log10_a0_hat
    chi2_min = res.fun
    grid = np.linspace(log10_a0_hat - 0.30, log10_a0_hat + 0.30, 601)
    chi2_grid = np.array([obj(x) for x in grid])
    inside = grid[chi2_grid <= chi2_min + 1.0]
    sig = float(0.5 * (inside.max() - inside.min())) if inside.size >= 2 else float('nan')
    return a0_hat, log10_a0_hat, chi2_min, sig


def analyse_subset(name: str, galaxies: list[dict], a0_sqt_p: float) -> dict:
    sample = build_g_arrays(galaxies)
    gbar = sample['gbar']; gobs = sample['gobs']; e_gobs = sample['e_gobs']
    n_pts = gbar.size
    n_gal = len(set(sample['names']))
    if n_pts < 30:
        return dict(name=name, n_galaxies=n_gal, n_points=n_pts, valid=False)
    e_log = e_gobs / (np.maximum(gobs, 1e-300) * math.log(10.0))
    sigma_log = np.sqrt(e_log ** 2 + SIGMA_LOG_FLOOR ** 2)
    a0_hat, log_a0_hat, chi2_free, sig_log = fit_a0(gbar, gobs, sigma_log)
    chi2_sqt = chi2_for_a0(gbar, gobs, sigma_log, a0_sqt_p)
    delta_log = log_a0_hat - math.log10(a0_sqt_p)
    return dict(
        name=name, valid=True,
        n_galaxies=int(n_gal), n_points=int(n_pts),
        a0_RAR=float(a0_hat), log10_a0_RAR=float(log_a0_hat),
        sigma_log10_a0=float(sig_log),
        chi2_free=float(chi2_free),
        chi2_per_dof_free=float(chi2_free / max(n_pts - 1, 1)),
        chi2_sqt_locked=float(chi2_sqt),
        chi2_per_dof_sqt=float(chi2_sqt / max(n_pts, 1)),
        delta_log_vs_SQT=float(delta_log),
        ratio_SQT_over_RAR=float(a0_sqt_p / a0_hat),
    )


def main() -> int:
    here = Path(__file__).resolve().parent
    sparc_dir = here.parent / 'l49' / 'data' / 'sparc'
    cat_path = here.parent / 'l49' / 'data' / 'sparc_catalog.mrt'
    if not sparc_dir.exists() or not cat_path.exists():
        print('SPARC data missing', file=sys.stderr)
        return 1

    catalog = parse_catalog(cat_path)
    print(f'Catalog parsed: {len(catalog)} entries (Q-flag, Vflat).')

    files = sorted(sparc_dir.glob('*_rotmod.dat'))
    galaxies_all = [parse_rotmod(p) for p in files]
    galaxies_all = [g for g in galaxies_all if g['R'].size >= 3]
    print(f'Loaded {len(galaxies_all)} rotmod galaxies (>=3 points).')

    # Match catalogue
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
    print(f'a0_SQT(Planck) = {a0_sqt_p:.4e} m/s^2')

    # Define subsets
    subsets = {}
    subsets['D1_full']       = list(galaxies_all)
    subsets['D2_Q1']         = [g for g in galaxies_all if g['Q'] == 1]
    subsets['D3_Q12']        = [g for g in galaxies_all if g['Q'] in (1, 2)]
    # LITTLE THINGS proxy: SPARC subsample with V_flat <= 60 km/s and T>=8 (Sdm/Im/BCD).
    # Iorio+17 LITTLE THINGS scale ~ V_max < 70 km/s.
    subsets['D4_dwarf_LT_proxy'] = [g for g in galaxies_all
                                    if 0 < g['Vflat'] <= 60.0 and g['T'] >= 8]
    subsets['D5_bright']     = [g for g in galaxies_all if g['Vflat'] >= 150.0]

    # Run per subset
    results = {}
    print('\n--- Per-subset RAR fits ---')
    print(f'{"name":24s} {"Ngal":>5s} {"Npts":>6s} {"a0[1e-10]":>10s} {"sig":>6s} {"chi2/dof":>9s} {"dlog":>7s}')
    for key, gal_list in subsets.items():
        r = analyse_subset(key, gal_list, a0_sqt_p)
        results[key] = r
        if r.get('valid'):
            print(f'{key:24s} {r["n_galaxies"]:5d} {r["n_points"]:6d} '
                  f'{r["a0_RAR"]*1e10:10.4f} {r["sigma_log10_a0"]:6.3f} '
                  f'{r["chi2_per_dof_sqt"]:9.3f} {r["delta_log_vs_SQT"]:+7.3f}')
        else:
            print(f'{key:24s} {r["n_galaxies"]:5d} {r["n_points"]:6d}  -- INVALID --')

    # Cross-spread metrics
    log_a0s = np.array([r['log10_a0_RAR'] for r in results.values() if r.get('valid')])
    spread_dex = float(np.std(log_a0s, ddof=0)) if log_a0s.size > 1 else float('nan')
    max_dev = float(np.max(np.abs(log_a0s - math.log10(a0_sqt_p)))) if log_a0s.size else float('nan')
    drifts = [r['delta_log_vs_SQT'] for r in results.values() if r.get('valid')]
    same_sign = bool(all(d > 0 for d in drifts) or all(d < 0 for d in drifts))

    K_X1 = spread_dex <= 0.05
    K_X2 = max_dev <= 0.10
    K_X3 = all((r['chi2_per_dof_sqt'] <= 1.6) for r in results.values() if r.get('valid'))
    K_X4 = not same_sign  # PASS if drifts not all same direction

    n_pass = sum([K_X1, K_X2, K_X3, K_X4])
    print('\n--- Cross-dataset audit ---')
    print(f'  spread_dex (std log10 a0)       = {spread_dex:.3f}')
    print(f'  max |log10(a0_sub/a0_SQT)|      = {max_dev:.3f}')
    print(f'  K_X1 spread <= 0.05             : {K_X1}')
    print(f'  K_X2 max_dev <= 0.10            : {K_X2}')
    print(f'  K_X3 all chi2/dof_SQT <= 1.6    : {K_X3}')
    print(f'  K_X4 drifts not all same sign   : {K_X4}  (drifts={drifts})')
    print(f'  PASS: {n_pass}/4')

    # Cluster literature reference (NOT re-analysed)
    cluster_lit = dict(
        reanalysed_here=False,
        note=('Cluster RAR (Tian & Ko 2016 ApJ 818 32; Pradel-Loubeyre style; '
              'Eckert+22 A&A 662 A123) reports a0_cluster ~ (5-10) x a0_SPARC. '
              'Background-only RAR universality fails on cluster scales — known '
              '"MOND missing-baryon" problem. Not a SPARC-internal cross-dataset '
              'inconsistency, but a structural cross-system inconsistency for '
              'any single-a0 model including SQT.'),
        literature_a0_cluster_over_a0_SPARC=(5.0, 10.0),
    )

    # Verdict line
    if n_pass == 4:
        verdict = 'cross-dataset stable (within SPARC galaxy subsamples; clusters excluded)'
    elif n_pass >= 2:
        verdict = 'partially stable across SPARC subsets; significant subset drift'
    else:
        verdict = 'unstable — a0 RAR differs substantially across SPARC subsets'

    out = dict(
        H0_planck=H0_PLANCK,
        a0_sqt_planck=float(a0_sqt_p),
        functional_form='M16',
        upsilon_disk=UPSILON_DISK, upsilon_bul=UPSILON_BUL,
        sigma_log_floor_dex=SIGMA_LOG_FLOOR,
        subsets=results,
        cross_metrics=dict(
            spread_dex=spread_dex,
            max_dev_log10_vs_SQT=max_dev,
            drifts_log10=drifts,
            drifts_all_same_sign=same_sign,
        ),
        K_criteria=dict(
            K_X1_spread_le_0p05=bool(K_X1),
            K_X2_maxdev_le_0p10=bool(K_X2),
            K_X3_all_chi2dof_sqt_le_1p6=bool(K_X3),
            K_X4_drifts_not_all_same_sign=bool(K_X4),
            n_pass=int(n_pass),
        ),
        clusters=cluster_lit,
        verdict=verdict,
    )

    out_json = here.parent.parent / 'results' / 'L492' / 'L492_results.json'
    out_json.parent.mkdir(parents=True, exist_ok=True)
    with out_json.open('w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, default=float)
    print(f'\nWrote {out_json}')
    print(f'\nVERDICT: {verdict}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
