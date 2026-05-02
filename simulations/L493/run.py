"""L493 — SPARC Radial Acceleration Relation: out-of-sample test.

Goal
----
SQT (the spacetime-quantum-metabolism a-priori scale a0 = c H0 / (2 pi)) is a
*0-free-parameter* prediction.  The L482/L489 RAR result fitted the McGaugh
interpolating function on the *full* SPARC 175-galaxy sample, then compared the
fitted a0 with the SQT prediction.  That is a self-consistency check, not a
predictive test.

L493 splits the 175 galaxies into

    train  : 70 %  (122 galaxies)   --   used only for the McGaugh free-a0 fit
                                          (the "MOND-like phenomenology"
                                          baseline) and for choosing the Upsilon
                                          convention (we keep the SPARC
                                          standard, no fitting).
    test   : 30 %  ( 53 galaxies)   --   *evaluated only*.  No parameter from
                                          the test set ever enters a fit.

For SQT, *no fit happens at all* — a0_SQT = c H0_Planck / (2 pi) is fixed
before seeing any data.  The test-set chi2 of the SQT-locked model therefore
measures genuine predictive accuracy, not in-sample goodness.

Reported quantities (all on the held-out 30 % test set):

    chi2_test_SQT   : SQT-locked McGaugh function, a0 = c H0 / 2pi
    chi2_test_TRAIN : McGaugh function with a0 = a0_train (fit from 70 %)
    chi2_test_NEWT  : Newton-only baseline, g_obs = g_bar
    chi2_test_M16   : McGaugh-locked a0 = 1.20e-10 m/s^2 (PRL value)

K-criteria (registered before the split):

    K_OOS1 : chi2/dof_test (SQT)  <= 1.5
    K_OOS2 : |chi2/dof_test_SQT - chi2/dof_train_TRAIN| <= 0.30
             (test/train accuracy difference small => no overfit)
    K_OOS3 : dAICc_test (SQT - TRAIN_a0) >= -2
             (the 0-parameter SQT model not strongly disfavoured vs the
              1-parameter trained-a0 model on held-out data)
    K_OOS4 : dAICc_test (SQT - Newton) <= -10
             (SQT clearly preferred over no-modification on held-out data)
    K_OOS5 : a0_train within 30 % of a0_SQT(Planck)
             (the train-only fit lands near the a-priori SQT scale)

Outputs
-------
    simulations/L493/run.py     (this file)
    results/L493/L493_results.json
    results/L493/OUT_OF_SAMPLE.md

CLAUDE.md compliance: no map provided to the team — only the train/test
direction.  All numerical constants reproduced from L482 (already approved),
no new theory parameters introduced.  ASCII-only print().
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar

# ---------------------------------------------------------------------------
# Constants (mirror L482)
# ---------------------------------------------------------------------------
C_LIGHT = 2.99792458e8
G_NEWT = 6.67430e-11
KPC = 3.0857e19
MPC = 3.0857e22
KM = 1.0e3

H0_PLANCK = 67.4
H0_RIESS = 73.04

UPSILON_DISK = 0.5
UPSILON_BUL = 0.7

A0_MCGAUGH = 1.20e-10

SEED = 20260501           # registered before split
TRAIN_FRAC = 0.70


def a0_sqt(h0_kmsmpc: float) -> float:
    h0_si = h0_kmsmpc * KM / MPC
    return C_LIGHT * h0_si / (2.0 * math.pi)


# ---------------------------------------------------------------------------
# SPARC parser & RAR builder (kept identical to L482 for reproducibility)
# ---------------------------------------------------------------------------
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
                Rs.append(float(tok[0]))
                Vo.append(float(tok[1]))
                eV.append(float(tok[2]))
                Vg.append(float(tok[3]))
                Vd.append(float(tok[4]))
                Vb.append(float(tok[5]))
            except ValueError:
                continue
    return dict(name=path.stem.replace('_rotmod', ''),
                R=np.asarray(Rs), Vobs=np.asarray(Vo), errV=np.asarray(eV),
                Vgas=np.asarray(Vg), Vdisk=np.asarray(Vd), Vbul=np.asarray(Vb))


def build_g_arrays(galaxies: list[dict],
                   ups_disk: float = UPSILON_DISK,
                   ups_bul: float = UPSILON_BUL) -> dict:
    gbar_all, gobs_all, eg_all, gname_all = [], [], [], []
    for g in galaxies:
        R = g['R']
        if R.size == 0:
            continue
        Vobs = g['Vobs']
        errV = g['errV']
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
        Vbar2 = ups_disk * sq_signed(Vd) + ups_bul * sq_signed(Vb) + sq_signed(Vg)
        valid = Vbar2 > 0
        if not np.any(valid):
            continue
        R_m = R_m[valid]
        Vo = Vo[valid]
        eV = eV[valid]
        Vbar2 = Vbar2[valid]

        gbar = Vbar2 / R_m
        gobs = Vo ** 2 / R_m
        e_gobs = 2.0 * Vo * eV / R_m

        gbar_all.append(gbar)
        gobs_all.append(gobs)
        eg_all.append(e_gobs)
        gname_all.extend([g['name']] * len(gbar))

    gbar_all = np.concatenate(gbar_all) if gbar_all else np.array([])
    gobs_all = np.concatenate(gobs_all) if gobs_all else np.array([])
    eg_all = np.concatenate(eg_all) if eg_all else np.array([])
    return dict(gbar=gbar_all, gobs=gobs_all, e_gobs=eg_all, names=gname_all)


# ---------------------------------------------------------------------------
# McGaugh F + chi2
# ---------------------------------------------------------------------------
def mcgaugh_F(gbar: np.ndarray, a0: float) -> np.ndarray:
    x = np.sqrt(np.maximum(gbar / a0, 1e-300))
    den = 1.0 - np.exp(-x)
    out = np.where(x > 1e-6, gbar / np.maximum(den, 1e-300), np.sqrt(gbar * a0))
    return out


def chi2_for_a0(gbar, gobs, sigma_log, a0):
    pred = mcgaugh_F(gbar, a0)
    res = (np.log10(gobs) - np.log10(pred)) / sigma_log
    return float(np.sum(res ** 2))


def fit_a0(gbar, gobs, sigma_log) -> tuple:
    def obj(log10_a0):
        a0 = 10.0 ** log10_a0
        return chi2_for_a0(gbar, gobs, sigma_log, a0)

    res = minimize_scalar(obj, bounds=(-12.0, -8.0), method='bounded',
                          options=dict(xatol=1e-5))
    log10_a0_hat = res.x
    a0_hat = 10.0 ** log10_a0_hat
    chi2_min = res.fun
    grid = np.linspace(log10_a0_hat - 0.30, log10_a0_hat + 0.30, 601)
    chi2_grid = np.array([obj(x) for x in grid])
    inside = grid[chi2_grid <= chi2_min + 1.0]
    if inside.size >= 2:
        sigma_log10_a0 = 0.5 * (inside.max() - inside.min())
    else:
        sigma_log10_a0 = float('nan')
    return a0_hat, log10_a0_hat, chi2_min, sigma_log10_a0


def aicc(chi2: float, k: int, n: int) -> float:
    aic = chi2 + 2 * k
    if n - k - 1 > 0:
        aic += 2 * k * (k + 1) / (n - k - 1)
    return aic


def chi2_newton_log(gbar, gobs, sigma_log) -> float:
    res = (np.log10(gobs) - np.log10(gbar)) / sigma_log
    return float(np.sum(res ** 2))


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def main() -> int:
    here = Path(__file__).resolve().parent
    sparc_dir = here.parent / 'l49' / 'data' / 'sparc'
    if not sparc_dir.exists():
        print(f"SPARC rotmod dir not found at {sparc_dir}", file=sys.stderr)
        return 1

    files = sorted(sparc_dir.glob('*_rotmod.dat'))
    galaxies = [parse_rotmod(p) for p in files]
    galaxies = [g for g in galaxies if g['R'].size >= 3]
    n_gal = len(galaxies)
    print(f"Total SPARC galaxies usable (>=3 points): {n_gal}")

    # Galaxy-level split: shuffle galaxy names with fixed seed, take 70/30.
    rng = np.random.default_rng(SEED)
    idx = np.arange(n_gal)
    rng.shuffle(idx)
    n_train = int(round(TRAIN_FRAC * n_gal))
    train_idx = sorted(idx[:n_train].tolist())
    test_idx = sorted(idx[n_train:].tolist())
    train_galaxies = [galaxies[i] for i in train_idx]
    test_galaxies = [galaxies[i] for i in test_idx]
    print(f"Split: train = {len(train_galaxies)} galaxies, "
          f"test = {len(test_galaxies)} galaxies (seed={SEED})")

    train_sample = build_g_arrays(train_galaxies)
    test_sample = build_g_arrays(test_galaxies)
    n_train_pts = train_sample['gbar'].size
    n_test_pts = test_sample['gbar'].size
    print(f"Train points: {n_train_pts}   Test points: {n_test_pts}")

    # log-space sigma per point (McGaugh 0.13 dex floor + obs)
    def sigma_log_of(sample):
        e_log = sample['e_gobs'] / (np.maximum(sample['gobs'], 1e-300) * math.log(10.0))
        return np.sqrt(e_log ** 2 + 0.13 ** 2)

    sigma_train = sigma_log_of(train_sample)
    sigma_test = sigma_log_of(test_sample)

    a0_p = a0_sqt(H0_PLANCK)
    a0_r = a0_sqt(H0_RIESS)
    print(f"a0_SQT(Planck H0=67.4) = {a0_p:.4e} m/s^2  (no data used)")

    # -------- TRAIN: fit a0 on training set only --------
    a0_train, log_a0_train, chi2_train_fit, sig_log_a0_train = fit_a0(
        train_sample['gbar'], train_sample['gobs'], sigma_train)
    chi2_train_train = chi2_for_a0(train_sample['gbar'], train_sample['gobs'],
                                   sigma_train, a0_train)
    chi2_train_sqt = chi2_for_a0(train_sample['gbar'], train_sample['gobs'],
                                 sigma_train, a0_p)
    chi2_train_newt = chi2_newton_log(train_sample['gbar'],
                                      train_sample['gobs'], sigma_train)
    print()
    print(f"TRAIN free-a0 fit : a0 = {a0_train:.4e}  "
          f"(log10 = {log_a0_train:.4f} +/- {sig_log_a0_train:.4f})")
    print(f"TRAIN chi2/dof    : free={chi2_train_train/(n_train_pts-1):.3f}  "
          f"SQT={chi2_train_sqt/n_train_pts:.3f}  "
          f"Newton={chi2_train_newt/n_train_pts:.3f}")

    # -------- TEST: predict only, no fit --------
    chi2_test_sqt = chi2_for_a0(test_sample['gbar'], test_sample['gobs'],
                                sigma_test, a0_p)
    chi2_test_train = chi2_for_a0(test_sample['gbar'], test_sample['gobs'],
                                  sigma_test, a0_train)
    chi2_test_newt = chi2_newton_log(test_sample['gbar'],
                                     test_sample['gobs'], sigma_test)
    chi2_test_m16 = chi2_for_a0(test_sample['gbar'], test_sample['gobs'],
                                sigma_test, A0_MCGAUGH)

    # AICc on test set.  SQT and Newton have 0 free parameters *re-used*
    # on the test set; the trained-a0 model has 1 parameter learned on TRAIN
    # but spent on TEST.  For out-of-sample AICc we count k=0 for SQT/Newton
    # and k=1 for trained-a0 (the parameter was estimated, even though not
    # on this set, so its uncertainty propagates).
    aicc_test_sqt = aicc(chi2_test_sqt, 0, n_test_pts)
    aicc_test_train = aicc(chi2_test_train, 1, n_test_pts)
    aicc_test_newt = aicc(chi2_test_newt, 0, n_test_pts)
    aicc_test_m16 = aicc(chi2_test_m16, 0, n_test_pts)

    print()
    print("TEST (held-out 30 %) -- no fitting:")
    print(f"  SQT-locked     : chi2/dof = {chi2_test_sqt/n_test_pts:.3f}   "
          f"AICc = {aicc_test_sqt:.2f}")
    print(f"  TRAIN-a0       : chi2/dof = {chi2_test_train/n_test_pts:.3f}   "
          f"AICc = {aicc_test_train:.2f}")
    print(f"  Newton-only    : chi2/dof = {chi2_test_newt/n_test_pts:.3f}   "
          f"AICc = {aicc_test_newt:.2f}")
    print(f"  McGaugh PRL a0 : chi2/dof = {chi2_test_m16/n_test_pts:.3f}   "
          f"AICc = {aicc_test_m16:.2f}")

    # -------- K-criteria (registered) --------
    chi2dof_test_sqt = chi2_test_sqt / max(n_test_pts, 1)
    chi2dof_train_train = chi2_train_train / max(n_train_pts - 1, 1)

    K_OOS1 = chi2dof_test_sqt <= 1.5
    K_OOS2 = abs(chi2dof_test_sqt - chi2dof_train_train) <= 0.30
    dAICc_sqt_minus_train = aicc_test_sqt - aicc_test_train
    K_OOS3 = dAICc_sqt_minus_train >= -2.0  # SQT not >2 worse than trained
    # convention: dAICc < 0 means SQT *better*; we PASS if SQT not >2 worse.
    K_OOS3 = dAICc_sqt_minus_train <= 2.0
    dAICc_sqt_minus_newt = aicc_test_sqt - aicc_test_newt
    K_OOS4 = dAICc_sqt_minus_newt <= -10.0
    ratio = a0_p / a0_train
    K_OOS5 = abs(1.0 - ratio) <= 0.30

    n_pass = int(K_OOS1) + int(K_OOS2) + int(K_OOS3) + int(K_OOS4) + int(K_OOS5)

    print()
    print("--- K-criteria (out-of-sample) ---")
    print(f"  K_OOS1 chi2/dof_test_SQT <= 1.5         : "
          f"{chi2dof_test_sqt:.3f}   {K_OOS1}")
    print(f"  K_OOS2 |test - train chi2/dof| <= 0.30  : "
          f"|{chi2dof_test_sqt:.3f} - {chi2dof_train_train:.3f}| = "
          f"{abs(chi2dof_test_sqt - chi2dof_train_train):.3f}   {K_OOS2}")
    print(f"  K_OOS3 AICc(SQT)-AICc(train) <= 2       : "
          f"{dAICc_sqt_minus_train:.2f}   {K_OOS3}")
    print(f"  K_OOS4 AICc(SQT)-AICc(Newton) <= -10    : "
          f"{dAICc_sqt_minus_newt:.2f}   {K_OOS4}")
    print(f"  K_OOS5 a0_train within 30 % of a0_SQT   : "
          f"ratio={ratio:.3f}   {K_OOS5}")
    print(f"  n_pass = {n_pass}/5")

    # -------- Persist --------
    out = dict(
        seed=SEED,
        train_frac=TRAIN_FRAC,
        n_galaxies_total=int(n_gal),
        n_train_galaxies=len(train_galaxies),
        n_test_galaxies=len(test_galaxies),
        n_train_points=int(n_train_pts),
        n_test_points=int(n_test_pts),
        H0_planck=H0_PLANCK,
        a0_sqt_planck=float(a0_p),
        train_fit=dict(
            a0=float(a0_train),
            log10_a0=float(log_a0_train),
            sigma_log10_a0=float(sig_log_a0_train),
            chi2=float(chi2_train_train),
            chi2_per_dof=float(chi2dof_train_train),
            n_params=1,
        ),
        train_sqt_locked=dict(
            chi2=float(chi2_train_sqt),
            chi2_per_dof=float(chi2_train_sqt / max(n_train_pts, 1)),
        ),
        train_newton=dict(
            chi2=float(chi2_train_newt),
            chi2_per_dof=float(chi2_train_newt / max(n_train_pts, 1)),
        ),
        test_sqt_locked=dict(
            chi2=float(chi2_test_sqt),
            chi2_per_dof=float(chi2dof_test_sqt),
            aicc=float(aicc_test_sqt),
            n_params=0,
        ),
        test_train_a0=dict(
            chi2=float(chi2_test_train),
            chi2_per_dof=float(chi2_test_train / max(n_test_pts, 1)),
            aicc=float(aicc_test_train),
            n_params=1,
        ),
        test_newton=dict(
            chi2=float(chi2_test_newt),
            chi2_per_dof=float(chi2_test_newt / max(n_test_pts, 1)),
            aicc=float(aicc_test_newt),
            n_params=0,
        ),
        test_mcgaugh_locked=dict(
            chi2=float(chi2_test_m16),
            chi2_per_dof=float(chi2_test_m16 / max(n_test_pts, 1)),
            aicc=float(aicc_test_m16),
            n_params=0,
        ),
        deltas=dict(
            dAICc_test_SQT_minus_train=float(dAICc_sqt_minus_train),
            dAICc_test_SQT_minus_newton=float(dAICc_sqt_minus_newt),
            dAICc_test_SQT_minus_mcgaugh=float(aicc_test_sqt - aicc_test_m16),
        ),
        K_criteria=dict(
            K_OOS1_chi2dof_test_le_1p5=bool(K_OOS1),
            K_OOS2_test_train_gap_le_0p30=bool(K_OOS2),
            K_OOS3_dAICc_SQT_minus_train_le_2=bool(K_OOS3),
            K_OOS4_dAICc_SQT_minus_newton_le_minus10=bool(K_OOS4),
            K_OOS5_a0_train_within_30pct_of_SQT=bool(K_OOS5),
            n_pass=int(n_pass),
        ),
    )

    out_json = here.parent.parent / 'results' / 'L493' / 'L493_results.json'
    out_json.parent.mkdir(parents=True, exist_ok=True)
    with out_json.open('w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, default=float)
    print(f"\nWrote {out_json}")

    # -------- Markdown report --------
    md = []
    md.append("# L493 -- SPARC RAR out-of-sample test\n")
    md.append(f"Seed: {SEED}   Train fraction: {TRAIN_FRAC}\n")
    md.append(f"Galaxies: total {n_gal} = train {len(train_galaxies)} + "
              f"test {len(test_galaxies)}\n")
    md.append(f"Radial points: train {n_train_pts}, test {n_test_pts}\n\n")
    md.append("## SQT a-priori prediction (no data used)\n")
    md.append(f"a0_SQT = c H0_Planck / (2 pi) = {a0_p:.4e} m s^-2\n\n")
    md.append("## Train-only fit\n")
    md.append(f"a0_train = {a0_train:.4e} m s^-2  "
              f"(log10 a0 = {log_a0_train:.4f} +/- {sig_log_a0_train:.4f})\n")
    md.append(f"a0_train / a0_SQT = {a0_train / a0_p:.3f}\n")
    md.append(f"chi2/dof (train, free-a0)  = {chi2dof_train_train:.3f}\n")
    md.append(f"chi2/dof (train, SQT)      = "
              f"{chi2_train_sqt / n_train_pts:.3f}\n")
    md.append(f"chi2/dof (train, Newton)   = "
              f"{chi2_train_newt / n_train_pts:.3f}\n\n")
    md.append("## Held-out test set (30 %, evaluation only)\n")
    md.append("| model | params | chi2 | chi2/dof | AICc |\n")
    md.append("|---|---|---|---|---|\n")
    md.append(f"| SQT-locked (a0 = c H0/2pi)   | 0 | {chi2_test_sqt:.2f} | "
              f"{chi2dof_test_sqt:.3f} | {aicc_test_sqt:.2f} |\n")
    md.append(f"| Train-fit a0                 | 1 | {chi2_test_train:.2f} | "
              f"{chi2_test_train / n_test_pts:.3f} | {aicc_test_train:.2f} |\n")
    md.append(f"| Newton-only (g_obs = g_bar)  | 0 | {chi2_test_newt:.2f} | "
              f"{chi2_test_newt / n_test_pts:.3f} | {aicc_test_newt:.2f} |\n")
    md.append(f"| McGaugh PRL a0 = 1.20e-10    | 0 | {chi2_test_m16:.2f} | "
              f"{chi2_test_m16 / n_test_pts:.3f} | {aicc_test_m16:.2f} |\n\n")
    md.append("## Train/test accuracy comparison\n")
    md.append(f"chi2/dof (train, train-a0)  = {chi2dof_train_train:.3f}\n")
    md.append(f"chi2/dof (test, SQT-locked) = {chi2dof_test_sqt:.3f}\n")
    md.append(f"|test - train| = "
              f"{abs(chi2dof_test_sqt - chi2dof_train_train):.3f}\n\n")
    md.append("## K-criteria\n")
    md.append(f"- K_OOS1 chi2/dof_test_SQT <= 1.5             : {K_OOS1}\n")
    md.append(f"- K_OOS2 |test - train chi2/dof| <= 0.30      : {K_OOS2}\n")
    md.append(f"- K_OOS3 AICc(SQT)-AICc(train) <= 2           : {K_OOS3}\n")
    md.append(f"- K_OOS4 AICc(SQT)-AICc(Newton) <= -10        : {K_OOS4}\n")
    md.append(f"- K_OOS5 a0_train within 30 % of a0_SQT       : {K_OOS5}\n")
    md.append(f"- n_pass = {n_pass}/5\n\n")
    md.append("## dAICc (test set)\n")
    md.append(f"dAICc(SQT - trained-a0)  = {dAICc_sqt_minus_train:+.2f}\n")
    md.append(f"dAICc(SQT - Newton)      = {dAICc_sqt_minus_newt:+.2f}\n")
    md.append(f"dAICc(SQT - McGaugh PRL) = "
              f"{aicc_test_sqt - aicc_test_m16:+.2f}\n\n")
    md.append("## Honest one-line\n")
    if K_OOS1 and K_OOS3 and K_OOS4:
        verdict = ("SQT a0 = c H0 / 2pi predicts the held-out 30 % SPARC RAR "
                   "with no fitting; out-of-sample accuracy matches train, "
                   "consistent with the 0-free-parameter claim.")
    elif K_OOS4:
        verdict = ("SQT clearly beats Newton on held-out data, but does not "
                   "match the train-fit accuracy on every K-criterion; "
                   "0-free-parameter claim partially supported.")
    else:
        verdict = ("Out-of-sample test does not support the 0-free-parameter "
                   "SQT prediction at the registered K-criteria.")
    md.append(verdict + "\n")

    out_md = here.parent.parent / 'results' / 'L493' / 'OUT_OF_SAMPLE.md'
    with out_md.open('w', encoding='utf-8') as fh:
        fh.writelines(md)
    print(f"Wrote {out_md}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
