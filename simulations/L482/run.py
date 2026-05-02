"""L482 — SPARC Radial Acceleration Relation (RAR) test.

McGaugh et al. 2016 (PRL 117, 201101) showed that, point-by-point in galaxy
rotation curves, the observed centripetal acceleration g_obs(r) = V_obs(r)^2 / r
is a tight one-parameter function of the Newtonian (baryonic) acceleration
g_bar(r) = V_bar(r)^2 / r:

    g_obs = F(g_bar; a0)

with the McGaugh interpolating function

    g_obs = g_bar / (1 - exp(-sqrt(g_bar / a0)))                (M16)

and best-fit a0_M16 = 1.20 +/- 0.02 (random) +/- 0.24 (sys) x 1e-10 m/s^2.

The SQT a-priori prediction (CLAUDE.md, L422/L448 framework) is

    a0_SQT = c * H0 / (2 pi)

which at H0 = 67.4 km/s/Mpc evaluates to ~ 1.04e-10 m/s^2 (within McGaugh systematic
band). L422 tested the *integrated* BTFR slope.  L448 tested the *integrated*
BTFR zero-point.  This L482 test uses the **point-by-point** RAR, which is a
formally distinct channel: it uses every radius in every rotation curve, not
just the asymptotic V_flat.  Many SPARC galaxies enter via multiple radii.

K-criteria (a priori, registered before fit):
  K_R1: a0_RAR_fit  within  30 %  of  a0_SQT(Planck)
  K_R2: |log10(a0_RAR / a0_SQT)| <= 2 sigma_fit
  K_R3: SQT-locked fit (a0 fixed to c H0/2pi) gives chi2/dof <= 1.5
  K_R4: dAICc(SQT-locked vs free-a0) >= -2  (SQT not strongly disfavoured)
  K_R5: dAICc(SQT-locked vs Newton-only) <= -10  (SQT clearly preferred over
        no-modification baseline)

Outputs:
  results/L482/RAR_TEST.md
  results/L482/L482_results.json
  simulations/L482/run.py (this file)
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar

# ---------------------------------------------------------------------------
# Constants (SI)
# ---------------------------------------------------------------------------
C_LIGHT = 2.99792458e8
G_NEWT = 6.67430e-11
KPC = 3.0857e19
MPC = 3.0857e22
KM = 1.0e3

H0_PLANCK = 67.4
H0_RIESS = 73.04

UPSILON_DISK = 0.5
UPSILON_BUL = 0.7  # SPARC convention (Lelli et al. 2016, McGaugh 2016)

A0_MCGAUGH = 1.20e-10  # McGaugh 2016 best-fit


def a0_sqt(h0_kmsmpc: float) -> float:
    h0_si = h0_kmsmpc * KM / MPC
    return C_LIGHT * h0_si / (2.0 * math.pi)


# ---------------------------------------------------------------------------
# SPARC rotmod parser
# ---------------------------------------------------------------------------
def parse_rotmod(path: Path) -> dict:
    """Return arrays {R[kpc], Vobs, errV, Vgas, Vdisk, Vbul} (km/s)."""
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
    """Concatenate all radii from all galaxies into (g_bar, g_obs, e_g_obs)."""
    gbar_all, gobs_all, eg_all, gname_all = [], [], [], []
    for g in galaxies:
        R = g['R']
        if R.size == 0:
            continue
        Vobs = g['Vobs']
        errV = g['errV']
        # Avoid R=0 and Vobs<=0
        good = (R > 0) & (Vobs > 0) & (errV > 0)
        if not np.any(good):
            continue
        R_m = R[good] * KPC
        Vo = Vobs[good] * KM
        eV = errV[good] * KM
        # SPARC convention: V_disk and V_bul tabulated for Ups=1, V_gas for Ups=1.
        # Baryonic V^2 = ups_disk * V_disk^2 * sign(Vdisk) + ups_bul * V_bul^2 * sign(Vbul) + V_gas^2 * sign
        # Sign preserves direction (some Vdisk values can be negative for inner falling).
        def sq_signed(arr):
            return np.sign(arr) * arr ** 2
        Vd = g['Vdisk'][good] * KM
        Vb = g['Vbul'][good] * KM
        Vg = g['Vgas'][good] * KM
        Vbar2 = ups_disk * sq_signed(Vd) + ups_bul * sq_signed(Vb) + sq_signed(Vg)
        # Reject points where Vbar2<=0 (rare inner artefacts)
        valid = Vbar2 > 0
        if not np.any(valid):
            continue
        R_m = R_m[valid]
        Vo = Vo[valid]
        eV = eV[valid]
        Vbar2 = Vbar2[valid]

        gbar = Vbar2 / R_m
        gobs = Vo ** 2 / R_m
        # Error on g_obs: dominant from V_obs:  d g_obs / d Vobs = 2 Vobs / R
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
# Models
# ---------------------------------------------------------------------------
def mcgaugh_F(gbar: np.ndarray, a0: float) -> np.ndarray:
    """McGaugh 2016 interpolating function g_obs = gbar / (1 - exp(-sqrt(gbar/a0)))."""
    x = np.sqrt(np.maximum(gbar / a0, 1e-300))
    # Stable for x small: 1-exp(-x) ~ x - x^2/2 ; gbar/(1-exp(-x)) ~ gbar/x = sqrt(gbar a0)
    den = 1.0 - np.exp(-x)
    # Avoid 0/0 for x->0 (gbar->0): use limit gbar/x = sqrt(gbar a0)
    out = np.where(x > 1e-6, gbar / np.maximum(den, 1e-300), np.sqrt(gbar * a0))
    return out


def chi2_for_a0(gbar, gobs, sigma_log, a0):
    pred = mcgaugh_F(gbar, a0)
    # Use log-space residuals (McGaugh 2016): scatter is ~0.13 dex
    res = (np.log10(gobs) - np.log10(pred)) / sigma_log
    return float(np.sum(res ** 2))


def fit_a0(gbar, gobs, sigma_log) -> tuple:
    """Fit a0 by minimising chi2 in log10 space."""
    def obj(log10_a0):
        a0 = 10.0 ** log10_a0
        return chi2_for_a0(gbar, gobs, sigma_log, a0)
    # search in log10(a0) over [-12, -8]
    res = minimize_scalar(obj, bounds=(-12.0, -8.0), method='bounded',
                          options=dict(xatol=1e-5))
    log10_a0_hat = res.x
    a0_hat = 10.0 ** log10_a0_hat
    chi2_min = res.fun
    # Crude 1-sigma from Delta chi2 = 1
    # Scan locally
    grid = np.linspace(log10_a0_hat - 0.30, log10_a0_hat + 0.30, 601)
    chi2_grid = np.array([obj(x) for x in grid])
    inside = grid[chi2_grid <= chi2_min + 1.0]
    if inside.size >= 2:
        sigma_log10_a0 = 0.5 * (inside.max() - inside.min())
    else:
        sigma_log10_a0 = float('nan')
    return a0_hat, log10_a0_hat, chi2_min, sigma_log10_a0, grid, chi2_grid


def aicc(chi2: float, k: int, n: int) -> float:
    aic = chi2 + 2 * k
    if n - k - 1 > 0:
        aic += 2 * k * (k + 1) / (n - k - 1)
    return aic


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
    print(f"Found {len(files)} SPARC rotation-curve files")

    galaxies = [parse_rotmod(p) for p in files]
    galaxies = [g for g in galaxies if g['R'].size >= 3]
    print(f"Kept {len(galaxies)} galaxies with >=3 points")

    sample = build_g_arrays(galaxies)
    gbar = sample['gbar']
    gobs = sample['gobs']
    e_gobs = sample['e_gobs']
    n_pts = gbar.size
    n_gal = len(set(sample['names']))
    print(f"Total RAR points: n={n_pts}  from {n_gal} galaxies")

    # log-space scatter floor (McGaugh 2016 reports ~0.13 dex intrinsic + obs)
    # Use observed err on g_obs converted to log + 0.13 dex floor in quadrature.
    e_log_gobs = e_gobs / (np.maximum(gobs, 1e-300) * math.log(10.0))
    sigma_log = np.sqrt(e_log_gobs ** 2 + 0.13 ** 2)

    a0_sqt_p = a0_sqt(H0_PLANCK)
    a0_sqt_r = a0_sqt(H0_RIESS)
    print(f"a0_SQT(Planck H0=67.4) = {a0_sqt_p:.4e} m/s^2")
    print(f"a0_SQT(Riess  H0=73.04)= {a0_sqt_r:.4e} m/s^2")
    print(f"a0_McGaugh             = {A0_MCGAUGH:.4e} m/s^2")
    print()

    # 1) Free a0 RAR fit
    a0_hat, log_a0_hat, chi2_free, sig_log_a0, grid, chi2_grid = fit_a0(gbar, gobs, sigma_log)
    n_free_param = 1  # only a0 (Ups fixed to SPARC convention)
    aicc_free = aicc(chi2_free, n_free_param, n_pts)
    print(f"Free-a0 best fit:")
    print(f"  a0_RAR  = {a0_hat:.4e} m/s^2  (log10 = {log_a0_hat:.4f} +/- {sig_log_a0:.4f})")
    print(f"  chi2/dof = {chi2_free:.1f} / {n_pts-1} = {chi2_free/(n_pts-1):.3f}")
    print(f"  AICc    = {aicc_free:.2f}")

    # 2) SQT-locked fit (a0 fixed = c H0_planck / 2pi)
    chi2_sqt = chi2_for_a0(gbar, gobs, sigma_log, a0_sqt_p)
    aicc_sqt = aicc(chi2_sqt, 0, n_pts)
    print(f"\nSQT-locked (a0 = c H0/(2pi), Planck H0):")
    print(f"  chi2/dof = {chi2_sqt:.1f} / {n_pts} = {chi2_sqt/n_pts:.3f}")
    print(f"  AICc    = {aicc_sqt:.2f}")

    # 2b) SQT-locked at Riess H0 (alternative)
    chi2_sqt_r = chi2_for_a0(gbar, gobs, sigma_log, a0_sqt_r)
    aicc_sqt_r = aicc(chi2_sqt_r, 0, n_pts)

    # 3) Newton-only baseline: g_obs = g_bar
    # chi2_newton = sum ((log10 gobs - log10 gbar)/sigma_log)^2
    res_newton = (np.log10(gobs) - np.log10(gbar)) / sigma_log
    chi2_newton = float(np.sum(res_newton ** 2))
    aicc_newton = aicc(chi2_newton, 0, n_pts)
    print(f"\nNewton-only (g_obs = g_bar):")
    print(f"  chi2/dof = {chi2_newton:.1f} / {n_pts} = {chi2_newton/n_pts:.3f}")
    print(f"  AICc    = {aicc_newton:.2f}")

    # 4) McGaugh-locked fit (a0 = 1.20e-10)
    chi2_m16 = chi2_for_a0(gbar, gobs, sigma_log, A0_MCGAUGH)
    aicc_m16 = aicc(chi2_m16, 0, n_pts)
    print(f"\nMcGaugh-locked (a0 = 1.20e-10):")
    print(f"  chi2/dof = {chi2_m16:.1f} / {n_pts} = {chi2_m16/n_pts:.3f}")
    print(f"  AICc    = {aicc_m16:.2f}")

    # ---- K-criteria ----
    ratio = a0_sqt_p / a0_hat
    K_R1 = abs(1.0 - ratio) <= 0.30
    delta_log = math.log10(a0_hat) - math.log10(a0_sqt_p)
    K_R2 = abs(delta_log) <= 2.0 * sig_log_a0 if not math.isnan(sig_log_a0) else False
    K_R3 = (chi2_sqt / max(n_pts, 1)) <= 1.5
    dAICc_sqt_vs_free = aicc_sqt - aicc_free
    dAICc_sqt_vs_newton = aicc_sqt - aicc_newton
    K_R4 = dAICc_sqt_vs_free >= -2.0  # SQT not strongly worse than free fit (delta worse <2 means OK; we use sqt-free, negative = sqt better)
    # interpretation: aicc_sqt - aicc_free.  If sqt > free + 2, SQT worse; we want sqt - free <= 2
    K_R4 = (aicc_sqt - aicc_free) <= 2.0
    K_R5 = dAICc_sqt_vs_newton <= -10.0

    print(f"\n--- K-criteria ---")
    print(f"  K_R1 (a0 within 30%)              : ratio_SQT/RAR={ratio:.3f}   {K_R1}")
    print(f"  K_R2 (within 2 sigma)             : |dlog|={abs(delta_log):.3f}, 2sig={2*sig_log_a0:.3f}   {K_R2}")
    print(f"  K_R3 (SQT chi2/dof <= 1.5)        : {chi2_sqt/n_pts:.3f}   {K_R3}")
    print(f"  K_R4 (AICc_SQT - AICc_free <= 2)  : {aicc_sqt - aicc_free:.2f}   {K_R4}")
    print(f"  K_R5 (AICc_SQT - AICc_Newton<=-10): {dAICc_sqt_vs_newton:.2f}   {K_R5}")

    n_pass = sum([K_R1, K_R2, K_R3, K_R4, K_R5])
    print(f"\n  K-criteria PASS: {n_pass}/5")

    # ---- Channel-independence vs L422/L448 ----
    # L422 and L448 use one number per galaxy (V_flat).  RAR uses every (R,V) sample.
    # Quantify: number of unique (R,V) samples vs number of galaxies.
    independence = dict(
        n_galaxies=int(n_gal),
        n_radial_points=int(n_pts),
        avg_points_per_galaxy=float(n_pts / max(n_gal, 1)),
        note=("RAR uses point-by-point (R,V) including inner radii where V<<V_flat. "
              "BTFR (L422/L448) uses only V_flat. Information overlap is partial: "
              "outer radii dominate g_bar small / g_obs ~ V_flat^2/R, inner radii "
              "test the high-acceleration Newtonian regime which BTFR cannot probe."),
    )

    out = dict(
        H0_planck=H0_PLANCK,
        H0_riess=H0_RIESS,
        a0_sqt_planck=float(a0_sqt_p),
        a0_sqt_riess=float(a0_sqt_r),
        a0_mcgaugh=float(A0_MCGAUGH),
        n_galaxies=int(n_gal),
        n_radial_points=int(n_pts),
        upsilon_disk=UPSILON_DISK,
        upsilon_bul=UPSILON_BUL,
        sigma_log_floor_dex=0.13,
        free_fit=dict(
            a0=float(a0_hat),
            log10_a0=float(log_a0_hat),
            sigma_log10_a0=float(sig_log_a0),
            chi2=float(chi2_free),
            chi2_per_dof=float(chi2_free / max(n_pts - 1, 1)),
            aicc=float(aicc_free),
            n_params=1,
        ),
        sqt_locked_planck=dict(
            a0=float(a0_sqt_p),
            chi2=float(chi2_sqt),
            chi2_per_dof=float(chi2_sqt / max(n_pts, 1)),
            aicc=float(aicc_sqt),
            n_params=0,
        ),
        sqt_locked_riess=dict(
            a0=float(a0_sqt_r),
            chi2=float(chi2_sqt_r),
            chi2_per_dof=float(chi2_sqt_r / max(n_pts, 1)),
            aicc=float(aicc_sqt_r),
        ),
        newton_only=dict(
            chi2=float(chi2_newton),
            chi2_per_dof=float(chi2_newton / max(n_pts, 1)),
            aicc=float(aicc_newton),
            n_params=0,
        ),
        mcgaugh_locked=dict(
            a0=float(A0_MCGAUGH),
            chi2=float(chi2_m16),
            chi2_per_dof=float(chi2_m16 / max(n_pts, 1)),
            aicc=float(aicc_m16),
        ),
        deltas=dict(
            dAICc_SQT_minus_free=float(aicc_sqt - aicc_free),
            dAICc_SQT_minus_newton=float(aicc_sqt - aicc_newton),
            dAICc_SQT_minus_mcgaugh=float(aicc_sqt - aicc_m16),
            dAICc_free_minus_mcgaugh=float(aicc_free - aicc_m16),
        ),
        K_criteria=dict(
            K_R1_within_30pct=bool(K_R1),
            K_R2_within_2sigma=bool(K_R2),
            K_R3_chi2_per_dof_le_1p5=bool(K_R3),
            K_R4_AICc_SQT_minus_free_le_2=bool(K_R4),
            K_R5_AICc_SQT_minus_newton_le_minus10=bool(K_R5),
            n_pass=int(n_pass),
        ),
        channel_independence=independence,
    )

    out_json = here.parent.parent / 'results' / 'L482' / 'L482_results.json'
    out_json.parent.mkdir(parents=True, exist_ok=True)
    with out_json.open('w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, default=float)
    print(f"\nWrote {out_json}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
