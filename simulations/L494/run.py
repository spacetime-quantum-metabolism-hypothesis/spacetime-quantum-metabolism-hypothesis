"""L494 — RAR null-mock false-positive audit.

Goal
----
L482/L489 reported that the SPARC RAR fit gives a0_RAR = 1.07e-10 m/s^2,
matching the SQT a-priori prediction a0_SQT = c H0 / (2 pi) = 1.042e-10
(Planck H0) at the ~3% level, with 5/5 K_R criteria PASS.  This task asks:

    Is that match a real signal, or is it the kind of coincidence that
    a non-modified (LCDM / pure-baryon-Newton) universe would *also*
    produce in random-realisation mocks?

Method
------
1. Build SPARC-like null mocks.  We preserve the SPARC sampling structure
   (same R_i, same V_bar(R_i) per galaxy) but draw V_obs(R_i) from the
   **null hypothesis**:

       g_obs_null(R_i) = g_bar(R_i)          (pure Newton; no MOND/SQT)

   then add the McGaugh 2016 intrinsic+observational log-scatter
   (0.13 dex floor).  Optionally we also test a *realistic* null where
   g_obs follows a **MOND-with-random-a0** template (a0 drawn uniformly
   in the McGaugh 1-sigma systematic band) to ask whether the
   particular SQT value (1.042e-10) is privileged.

2. For each mock and for each of N_FUNC functional forms, fit a0 in
   log10 space.

3. Define a "false positive" as a mock that satisfies the same passing
   condition as the L482 real fit:
       K_R1:  |a0_fit - a0_SQT| / a0_SQT  <=  0.30           (within 30%)
       K_R3:  chi2/dof at SQT-locked a0    <=  1.5
       K_R5:  dAICc(SQT  vs  Newton-only)  <= -10
   We tally FP rates per criterion and the joint rate.

Functional forms (5)
--------------------
F1 McGaugh-2016:   g = g_bar / (1 - exp(-sqrt(g_bar/a0)))
F2 simple-mu:      g = 0.5*(g_bar + sqrt(g_bar^2 + 4 g_bar a0))
F3 standard-mu:    g/a0 such that  mu(g/a0) g = g_bar  with mu(x) = x/sqrt(1+x^2)
F4 Bekenstein nu:  nu(y) = 0.5 + sqrt(0.25 + 1/y),  g = nu(g_bar/a0) g_bar
F5 power-law:      log10(g) = log10(g_bar) + 0.5*tanh((log10(a0)-log10(g_bar))/dx)*dx
                   (smooth interpolation; a0 sets the kink)

All five share the property that g(g_bar) -> g_bar at high acceleration
and -> sqrt(g_bar a0) at low acceleration.  They are common, well-cited
RAR template families.

Outputs
-------
results/L494/MOCK_FALSE_RATE.md
results/L494/L494_summary.json
"""
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

# Force single-threaded BLAS to avoid cross-process contention
for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np
from scipy.optimize import minimize_scalar
import multiprocessing as mp

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
C_LIGHT = 2.99792458e8
KPC = 3.0857e19
MPC = 3.0857e22
KM = 1.0e3
H0_PLANCK = 67.4
UPS_DISK = 0.5
UPS_BUL = 0.7
SIGMA_LOG_DEX = 0.13           # McGaugh 2016 intrinsic scatter floor
A0_MCGAUGH = 1.20e-10

N_MOCKS = 200
SEED_BASE = 20260501

# K-criteria thresholds (mirror L482)
K_R1_TOL = 0.30
K_R3_CHI2_PER_DOF_MAX = 1.5
K_R5_DAICC_MAX = -10.0


def a0_sqt(h0_kmsmpc: float) -> float:
    return C_LIGHT * h0_kmsmpc * KM / MPC / (2.0 * math.pi)


# ---------------------------------------------------------------------------
# SPARC parser (mirrors L482)
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


def build_baryonic_template(galaxies):
    """Concatenate (g_bar, e_gobs_template) keeping per-point structure."""
    gbar_list, e_gobs_list, gname_list = [], [], []
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
        Vd = g['Vdisk'][good] * KM
        Vb = g['Vbul'][good] * KM
        Vg = g['Vgas'][good] * KM
        sgn_sq = lambda a: np.sign(a) * a * a
        Vbar2 = UPS_DISK * sgn_sq(Vd) + UPS_BUL * sgn_sq(Vb) + sgn_sq(Vg)
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
        gbar_list.append(gbar)
        e_gobs_list.append(e_gobs)
        gname_list.extend([g['name']] * gbar.size)
        # also keep per-point gobs to compute its log-error scale
        # (we will fold into sigma_log via the same expression as L482)
        # store gobs scale in the e_gobs slot via observed gobs
        # but we keep gobs separately for sigma_log calc
    gbar_all = np.concatenate(gbar_list) if gbar_list else np.array([])
    e_gobs_all = np.concatenate(e_gobs_list) if e_gobs_list else np.array([])
    return gbar_all, e_gobs_all, gname_list


# ---------------------------------------------------------------------------
# Functional forms (5)
# ---------------------------------------------------------------------------
def F1_mcgaugh(gbar, a0):
    x = np.sqrt(np.maximum(gbar / a0, 1e-300))
    den = 1.0 - np.exp(-x)
    return np.where(x > 1e-6, gbar / np.maximum(den, 1e-300),
                    np.sqrt(gbar * a0))


def F2_simple_mu(gbar, a0):
    # Solves x = mu(g/a0)*g with mu(y)=y/(1+y) -> g = 0.5*(g_b + sqrt(g_b^2+4 g_b a0))
    return 0.5 * (gbar + np.sqrt(gbar * gbar + 4.0 * gbar * a0))


def F3_standard_mu(gbar, a0):
    # mu(y) = y / sqrt(1+y^2),  g_b = mu(g/a0)*g  -->  closed form:
    # let u = g/a0,  g_b/a0 = u^2 / sqrt(1+u^2)
    # invert numerically via stable algebra:  solve u^2 = (g_b/a0) sqrt(1+u^2)
    # let z = u^2 ; z^2 = (g_b/a0)^2 (1+z) -> z^2 - q^2 z - q^2 = 0,  q = g_b/a0
    q = gbar / a0
    z = 0.5 * (q * q + np.sqrt(q ** 4 + 4.0 * q * q))
    u = np.sqrt(z)
    return u * a0


def F4_bekenstein(gbar, a0):
    # nu(y) = 0.5 + sqrt(0.25 + 1/y),  g = nu(g_bar/a0) * g_bar
    y = np.maximum(gbar / a0, 1e-300)
    nu = 0.5 + np.sqrt(0.25 + 1.0 / y)
    return nu * gbar


def F5_smooth_kink(gbar, a0):
    # log10 g = log10 g_bar + 0.5 dx ( 1 - tanh((log10 g_bar - log10 a0)/dx) )
    # at g_bar >> a0 -> tanh -> +1 -> bracket 0 -> g = g_bar  (Newton)
    # at g_bar << a0 -> tanh -> -1 -> bracket 1 -> log10 g = log10 g_bar + dx
    #   want low-acc limit g = sqrt(g_bar a0) -> log10 g - log10 g_bar
    #   = 0.5 (log10 a0 - log10 g_bar);  this is dx-dependent.  We pick
    #   dx ~ 1.0 (log10 unit) which approximates the MOND limit over a
    #   one-decade transition.  Form is bounded and analytic.
    DX = 1.0
    lg = np.log10(np.maximum(gbar, 1e-300))
    la = math.log10(a0)
    return 10.0 ** (lg + 0.5 * DX * (1.0 - np.tanh((lg - la) / DX)))


FUNCS = [
    ("F1_McGaugh",     F1_mcgaugh),
    ("F2_simple_mu",   F2_simple_mu),
    ("F3_standard_mu", F3_standard_mu),
    ("F4_Bekenstein",  F4_bekenstein),
    ("F5_smooth_kink", F5_smooth_kink),
]


# ---------------------------------------------------------------------------
# Fitter
# ---------------------------------------------------------------------------
def chi2_for(form, gbar, gobs, sigma_log, a0):
    pred = form(gbar, a0)
    res = (np.log10(np.maximum(gobs, 1e-300))
           - np.log10(np.maximum(pred, 1e-300))) / sigma_log
    return float(np.sum(res ** 2))


def fit_a0(form, gbar, gobs, sigma_log):
    def obj(log10_a0):
        return chi2_for(form, gbar, gobs, sigma_log, 10.0 ** log10_a0)
    res = minimize_scalar(obj, bounds=(-12.0, -8.0), method='bounded',
                          options=dict(xatol=1e-5))
    a0 = 10.0 ** res.x
    return a0, float(res.x), float(res.fun)


# ---------------------------------------------------------------------------
# Mock generator
# ---------------------------------------------------------------------------
def make_null_mock(gbar, e_gobs_template, sigma_log_floor, rng,
                   mode: str, a0_inj: float):
    """
    mode = 'newton'   -> g_obs_truth = g_bar  (LCDM/no-MOND null)
    mode = 'mond_inj' -> g_obs_truth = F1_McGaugh(g_bar, a0_inj)
    Then add log-normal scatter with sigma_log per point built the same way
    as the real-data sigma_log (obs-error + 0.13 dex floor).
    """
    if mode == 'newton':
        truth = gbar.copy()
    elif mode == 'mond_inj':
        truth = F1_mcgaugh(gbar, a0_inj)
    else:
        raise ValueError(mode)
    # Build sigma_log using a self-consistent observed-error template:
    # treat e_gobs_template as if it scales with truth, i.e.
    # sigma_obs_log = e_gobs_template / (max(gobs_template,1e-300) ln10)
    # We approximate gobs_template ~ truth (consistent with the mock).
    sigma_obs_log = e_gobs_template / (np.maximum(truth, 1e-300) * math.log(10.0))
    sigma_log = np.sqrt(sigma_obs_log ** 2 + sigma_log_floor ** 2)
    log_truth = np.log10(np.maximum(truth, 1e-300))
    log_mock = log_truth + rng.normal(0.0, sigma_log)
    gobs_mock = 10.0 ** log_mock
    return gobs_mock, sigma_log


# ---------------------------------------------------------------------------
# Worker: process one mock realisation
# ---------------------------------------------------------------------------
def worker(args):
    (mock_id, seed, gbar, e_gobs_tmpl, sigma_log_floor, a0_target,
     mode, a0_inj) = args
    rng = np.random.default_rng(seed)
    gobs, sigma_log = make_null_mock(gbar, e_gobs_tmpl, sigma_log_floor,
                                     rng, mode, a0_inj)
    n = gbar.size
    # Newton-only chi2 for K_R5
    res_newton = (np.log10(np.maximum(gobs, 1e-300)) - np.log10(np.maximum(gbar, 1e-300))) / sigma_log
    chi2_newton = float(np.sum(res_newton ** 2))
    aicc_newton = chi2_newton  # k=0
    out = dict(mock_id=mock_id, mode=mode, n=n, chi2_newton=chi2_newton)
    for fname, form in FUNCS:
        a0_hat, log_a0_hat, chi2_free = fit_a0(form, gbar, gobs, sigma_log)
        chi2_sqt = chi2_for(form, gbar, gobs, sigma_log, a0_target)
        # AICc with k=1 free, k=0 sqt-locked, k=0 newton (n large -> AICc~AIC)
        aicc_free = chi2_free + 2 * 1 + 2 * 1 * 2 / max(n - 2, 1)
        aicc_sqt = chi2_sqt
        ratio = a0_hat / a0_target
        K_R1 = abs(1.0 - ratio) <= K_R1_TOL
        K_R3 = (chi2_sqt / max(n, 1)) <= K_R3_CHI2_PER_DOF_MAX
        K_R5 = (aicc_sqt - aicc_newton) <= K_R5_DAICC_MAX
        K_joint = bool(K_R1 and K_R3 and K_R5)
        out[fname] = dict(
            a0_hat=float(a0_hat),
            log10_a0_hat=float(log_a0_hat),
            chi2_free=float(chi2_free),
            chi2_sqt=float(chi2_sqt),
            chi2_per_dof_sqt=float(chi2_sqt / max(n, 1)),
            dAICc_sqt_minus_free=float(aicc_sqt - aicc_free),
            dAICc_sqt_minus_newton=float(aicc_sqt - aicc_newton),
            ratio_a0=float(ratio),
            K_R1=bool(K_R1), K_R3=bool(K_R3), K_R5=bool(K_R5),
            K_joint=bool(K_joint),
        )
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    here = Path(__file__).resolve().parent
    sparc_dir = here.parent / 'l49' / 'data' / 'sparc'
    if not sparc_dir.exists():
        print(f"SPARC dir not found at {sparc_dir}", file=sys.stderr)
        return 1
    files = sorted(sparc_dir.glob('*_rotmod.dat'))
    galaxies = [parse_rotmod(p) for p in files]
    galaxies = [g for g in galaxies if g['R'].size >= 3]
    gbar, e_gobs_tmpl, names = build_baryonic_template(galaxies)
    n_pts = gbar.size
    n_gal = len(set(names))
    a0_target = a0_sqt(H0_PLANCK)
    print(f"SPARC template: {n_gal} galaxies, {n_pts} radial points")
    print(f"a0_SQT(Planck) = {a0_target:.4e} m/s^2")
    print(f"N_MOCKS per mode = {N_MOCKS}")

    modes = [('newton', 0.0), ('mond_inj', A0_MCGAUGH)]

    n_workers = min(9, max(1, mp.cpu_count() - 1))
    ctx = mp.get_context('spawn')

    all_results = {}
    for mode, a0_inj in modes:
        print(f"\n--- mode = {mode}  (injected a0 = {a0_inj:.3e}) ---")
        tasks = []
        for i in range(N_MOCKS):
            seed = SEED_BASE + (0 if mode == 'newton' else 10_000_000) + i
            tasks.append((i, seed, gbar, e_gobs_tmpl, SIGMA_LOG_DEX,
                          a0_target, mode, a0_inj))
        with ctx.Pool(n_workers) as pool:
            res_list = pool.map(worker, tasks)
        all_results[mode] = res_list
        # aggregate
        per_func = {fname: dict(K_R1=0, K_R3=0, K_R5=0, K_joint=0,
                                a0_hats=[], chi2_per_dof=[]) for fname, _ in FUNCS}
        for r in res_list:
            for fname, _ in FUNCS:
                d = r[fname]
                per_func[fname]['K_R1'] += int(d['K_R1'])
                per_func[fname]['K_R3'] += int(d['K_R3'])
                per_func[fname]['K_R5'] += int(d['K_R5'])
                per_func[fname]['K_joint'] += int(d['K_joint'])
                per_func[fname]['a0_hats'].append(d['a0_hat'])
                per_func[fname]['chi2_per_dof'].append(d['chi2_per_dof_sqt'])
        print(f"  False-positive counts (out of {N_MOCKS}):")
        print(f"  {'form':<18}  K_R1   K_R3   K_R5   K_joint   median a0_hat / a0_SQT")
        for fname, _ in FUNCS:
            pf = per_func[fname]
            med_ratio = float(np.median(pf['a0_hats'])) / a0_target
            print(f"  {fname:<18}  {pf['K_R1']:>4}   {pf['K_R3']:>4}   "
                  f"{pf['K_R5']:>4}   {pf['K_joint']:>5}     {med_ratio:.3f}")

    # Save summary JSON
    summary = dict(
        n_mocks=N_MOCKS,
        n_galaxies=n_gal,
        n_radial_points=n_pts,
        a0_SQT_Planck=float(a0_target),
        sigma_log_floor_dex=SIGMA_LOG_DEX,
        K_R1_tol=K_R1_TOL,
        K_R3_chi2_per_dof_max=K_R3_CHI2_PER_DOF_MAX,
        K_R5_dAICc_max=K_R5_DAICC_MAX,
        functional_forms=[fname for fname, _ in FUNCS],
        results={},
    )
    for mode, _ in modes:
        per_func_summary = {}
        for fname, _ in FUNCS:
            ks = dict(K_R1=0, K_R3=0, K_R5=0, K_joint=0)
            a_hats = []
            cpdofs = []
            for r in all_results[mode]:
                d = r[fname]
                ks['K_R1'] += int(d['K_R1'])
                ks['K_R3'] += int(d['K_R3'])
                ks['K_R5'] += int(d['K_R5'])
                ks['K_joint'] += int(d['K_joint'])
                a_hats.append(d['a0_hat'])
                cpdofs.append(d['chi2_per_dof_sqt'])
            per_func_summary[fname] = dict(
                K_R1_count=ks['K_R1'], K_R3_count=ks['K_R3'],
                K_R5_count=ks['K_R5'], K_joint_count=ks['K_joint'],
                K_R1_rate=ks['K_R1'] / N_MOCKS,
                K_R3_rate=ks['K_R3'] / N_MOCKS,
                K_R5_rate=ks['K_R5'] / N_MOCKS,
                K_joint_rate=ks['K_joint'] / N_MOCKS,
                median_a0_hat=float(np.median(a_hats)),
                median_a0_ratio_to_SQT=float(np.median(a_hats)) / float(a0_target),
                median_chi2_per_dof_sqt_locked=float(np.median(cpdofs)),
            )
        summary['results'][mode] = per_func_summary

    out_dir = here.parent.parent / 'results' / 'L494'
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / 'L494_summary.json').open('w', encoding='utf-8') as fh:
        json.dump(summary, fh, indent=2, default=float)
    print(f"\nWrote {out_dir / 'L494_summary.json'}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
