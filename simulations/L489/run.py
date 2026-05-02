"""L489 — Independent re-verification of L482 RAR PASS_STRONG candidate.

Strong-skeptic stance.  We do NOT trust L482's 5/5 PASS at face value.
Goals:
  (A) Reproduce L482 a0 fit with the same McGaugh interpolating function on
      the same SPARC sample, *independently* implemented.
  (B) Refit a0 with TWO alternative interpolating functions:
        - simple-mu  : g_obs = (g_bar + sqrt(g_bar^2 + 4 g_bar a0)) / 2
                       (== Famaey-Binney "simple" / nu(y) = 1/2 + sqrt(1/4 + 1/y))
        - standard-mu: mu(x)= x/sqrt(1+x^2)  =>  g_obs solved from
                       g_obs * x / sqrt(1+x^2) = g_bar with x = g_obs/a0.
      If a0_fit moves by >>2sigma between functions, the M16 value is shape-
      dependent and the "agreement with SQT" is only meaningful for the
      M16 functional form.
  (C) Compare against McGaugh 2016 a0 = 1.20e-10.  Two independent SPARC
      analyses since:
         - Li et al. 2018 (A&A 615, A3): a0 = 1.10e-10 +/- 0.02 (Bayes,
           per-galaxy Upsilon free).
         - Chae et al. 2020 (ApJ 904, 51): a0 ~ 1.1e-10 with Bayes Upsilon.
      These give a *spread* 1.1 - 1.2.  SQT 1.04 sits at the lower edge.
      Decide by reproducing the analysis at SPARC-canonical Ups vs at
      best-fit Ups.
  (D) Cherry-pick audit: re-check K_R2 with proper sigma definition.
      L482 used sigma_log10_a0 ~ 0.006 dex from Delta chi2 = 1, but the
      chi2/dof is 1.295, indicating residuals are non-Gaussian or the
      0.13 dex floor underestimates true scatter.  The standard fix is
      to *rescale* sigma_floor until chi2/dof = 1, then redo the
      Delta chi2 = 1 contour.  This typically inflates sigma_log10_a0 by
      sqrt(1.295) ~ 1.14, but we check.
  (E) Channel-independence check vs L422/L448: re-derive a0 from a
      *V_flat-only* summary on the SAME 175 galaxies, then refit RAR
      with only the outermost radius per galaxy.  If outermost-only RAR
      reproduces L448's median ~1.5e-10, BTFR/RAR overlap is large; if
      outermost-only RAR gives ~1.07e-10, RAR's information edge is
      coming from somewhere other than inner radii (suspicious).

Outputs: results/L489/REVERIFY_L482.md and results/L489/L489_results.json.

We obey CLAUDE.md L33/L48 rules: numpy 2.x trapezoid, no theory hints,
honest reporting.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar, brentq

# Reuse L482 parser/builders.
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
H0_RIESS = l482.H0_RIESS

UPSILON_DISK = l482.UPSILON_DISK
UPSILON_BUL = l482.UPSILON_BUL
A0_MCGAUGH = l482.A0_MCGAUGH


# ---------- Independent interpolating functions ----------
def F_mcgaugh(gbar, a0):
    x = np.sqrt(np.maximum(gbar / a0, 1e-300))
    den = 1.0 - np.exp(-x)
    return np.where(x > 1e-6, gbar / np.maximum(den, 1e-300), np.sqrt(gbar * a0))


def F_simple(gbar, a0):
    """Simple-nu (Famaey-Binney 2005): g_obs = (g_bar + sqrt(g_bar^2 + 4 g_bar a0))/2.
    Equivalent to mu(x)=x/(1+x) with x=g_obs/a0."""
    return 0.5 * (gbar + np.sqrt(gbar ** 2 + 4.0 * gbar * a0))


def F_standard(gbar, a0):
    """Standard MOND mu(x)=x/sqrt(1+x^2).  Solve g_obs from
    g_obs * x_norm / sqrt(1+x_norm^2) = g_bar where x_norm = g_obs/a0.
    => g_obs^2 - g_bar^2 - g_bar * sqrt(g_obs^2 + a0^2) = 0
    Closed form: let y = g_obs^2.  Then y - g_bar^2 = g_bar sqrt(y+a0^2)
       -> (y-g_bar^2)^2 = g_bar^2 (y + a0^2)
       -> y^2 - 2 g_bar^2 y + g_bar^4 = g_bar^2 y + g_bar^2 a0^2
       -> y^2 - (2 g_bar^2 + g_bar^2) y + (g_bar^4 - g_bar^2 a0^2) = 0
       -> y^2 - 3 g_bar^2 y + g_bar^2(g_bar^2 - a0^2) = 0
    Quadratic, take the larger root (since g_obs >= g_bar):
    """
    A = 3.0 * gbar ** 2
    B = gbar ** 2 * (gbar ** 2 - a0 ** 2)
    disc = np.maximum(A * A - 4.0 * B, 0.0)
    y = 0.5 * (A + np.sqrt(disc))
    return np.sqrt(np.maximum(y, 1e-300))


def chi2_general(gbar, gobs, sigma_log, a0, F):
    pred = F(gbar, a0)
    res = (np.log10(gobs) - np.log10(pred)) / sigma_log
    return float(np.sum(res ** 2))


def fit_a0_general(gbar, gobs, sigma_log, F):
    def obj(la):
        return chi2_general(gbar, gobs, sigma_log, 10.0 ** la, F)
    r = minimize_scalar(obj, bounds=(-12.0, -8.0), method='bounded',
                        options=dict(xatol=1e-5))
    la_hat = r.x
    chi2_hat = r.fun
    grid = np.linspace(la_hat - 0.4, la_hat + 0.4, 801)
    chi2g = np.array([obj(x) for x in grid])
    inside = grid[chi2g <= chi2_hat + 1.0]
    sig = 0.5 * (inside.max() - inside.min()) if inside.size >= 2 else float('nan')
    return 10.0 ** la_hat, la_hat, chi2_hat, sig


# ---------- Driver ----------
def main():
    sparc_dir = ROOT / 'simulations' / 'l49' / 'data' / 'sparc'
    files = sorted(sparc_dir.glob('*_rotmod.dat'))
    galaxies = [l482.parse_rotmod(p) for p in files]
    galaxies = [g for g in galaxies if g['R'].size >= 3]
    sample = l482.build_g_arrays(galaxies, UPSILON_DISK, UPSILON_BUL)
    gbar = sample['gbar']
    gobs = sample['gobs']
    e_gobs = sample['e_gobs']
    names = sample['names']
    n_pts = gbar.size
    n_gal = len(set(names))
    print(f"[L489] sample: n_pts={n_pts}  n_gal={n_gal}")

    e_log = e_gobs / (np.maximum(gobs, 1e-300) * math.log(10.0))
    sigma_log = np.sqrt(e_log ** 2 + 0.13 ** 2)

    a0_sqt_p = l482.a0_sqt(H0_PLANCK)

    # (A) L482 reproduction with M16
    a0_m16, la_m16, chi2_m16_free, sig_m16 = fit_a0_general(gbar, gobs, sigma_log, F_mcgaugh)
    chi2_m16_sqt = chi2_general(gbar, gobs, sigma_log, a0_sqt_p, F_mcgaugh)
    print(f"[A] M16 fit: a0={a0_m16:.4e}, chi2={chi2_m16_free:.1f}/{n_pts-1}, "
          f"sig_log={sig_m16:.4f}")
    print(f"    L482 reported a0=1.0687e-10 chi2=4384.5  -- diff "
          f"{abs(a0_m16-1.0687e-10)/1.0687e-10*100:.3f}%")

    # (B) Alternative interpolating functions
    a0_simple, la_s, chi2_s_free, sig_s = fit_a0_general(gbar, gobs, sigma_log, F_simple)
    chi2_s_sqt = chi2_general(gbar, gobs, sigma_log, a0_sqt_p, F_simple)
    a0_std, la_std, chi2_std_free, sig_std = fit_a0_general(gbar, gobs, sigma_log, F_standard)
    chi2_std_sqt = chi2_general(gbar, gobs, sigma_log, a0_sqt_p, F_standard)
    print(f"[B] simple-nu : a0={a0_simple:.4e}  chi2={chi2_s_free:.1f}  sig_log={sig_s:.4f}")
    print(f"    standard  : a0={a0_std:.4e}    chi2={chi2_std_free:.1f}  sig_log={sig_std:.4f}")

    # Cross-form spread: shape systematic on a0
    a0_array = np.array([a0_m16, a0_simple, a0_std])
    log_a0_spread_dex = np.log10(a0_array.max()) - np.log10(a0_array.min())
    print(f"    cross-form a0 range = [{a0_array.min():.3e}, {a0_array.max():.3e}]"
          f"  spread = {log_a0_spread_dex:.3f} dex")

    # (D) sigma rescaling: enforce chi2/dof=1
    chi2dof = chi2_m16_free / (n_pts - 1)
    rescale = math.sqrt(max(chi2dof, 1e-12))
    sigma_log_rescaled = sigma_log * rescale
    a0_resc, la_resc, chi2_resc_free, sig_resc = fit_a0_general(
        gbar, gobs, sigma_log_rescaled, F_mcgaugh)
    chi2_resc_sqt = chi2_general(gbar, gobs, sigma_log_rescaled, a0_sqt_p, F_mcgaugh)
    print(f"[D] sigma rescale by sqrt(chi2/dof)={rescale:.4f}: a0={a0_resc:.4e}, "
          f"sig_log={sig_resc:.4f} (vs {sig_m16:.4f}). new chi2/dof={chi2_resc_free/(n_pts-1):.3f}")

    # (E) channel-independence: outer-radius-only RAR
    outer_gbar, outer_gobs, outer_sigma = [], [], []
    by_name = {}
    for i, nm in enumerate(names):
        by_name.setdefault(nm, []).append(i)
    for nm, idxs in by_name.items():
        # take outermost radius (largest R proxy: smallest g_bar typically; but
        # we have only g.  Use original galaxy R via gbar=Vbar^2/R; outer radius
        # has *smallest* gbar generally for a flat-rotation system).
        # Safer: re-load from galaxy and pick max R
        pass
    # Rebuild outer per galaxy using stored R explicitly
    outer = []
    for g in galaxies:
        R = g['R']
        if R.size == 0:
            continue
        Vobs = g['Vobs']
        errV = g['errV']
        good = (R > 0) & (Vobs > 0) & (errV > 0)
        if not np.any(good):
            continue
        Vd = g['Vdisk'][good] * KM
        Vb = g['Vbul'][good] * KM
        Vg = g['Vgas'][good] * KM
        sq = lambda a: np.sign(a) * a ** 2
        Vbar2 = UPSILON_DISK * sq(Vd) + UPSILON_BUL * sq(Vb) + sq(Vg)
        valid = Vbar2 > 0
        if not np.any(valid):
            continue
        Rg = R[good][valid] * KPC
        Vo = Vobs[good][valid] * KM
        eV = errV[good][valid] * KM
        Vbar2 = Vbar2[valid]
        # outermost
        idx = int(np.argmax(Rg))
        gbar_o = Vbar2[idx] / Rg[idx]
        gobs_o = Vo[idx] ** 2 / Rg[idx]
        e_g = 2.0 * Vo[idx] * eV[idx] / Rg[idx]
        outer.append((gbar_o, gobs_o, e_g))
    o = np.array(outer)
    o_gbar, o_gobs, o_eg = o[:, 0], o[:, 1], o[:, 2]
    o_elog = o_eg / (np.maximum(o_gobs, 1e-300) * math.log(10.0))
    o_sigma_log = np.sqrt(o_elog ** 2 + 0.13 ** 2)
    a0_outer, la_outer, chi2_outer, sig_outer = fit_a0_general(
        o_gbar, o_gobs, o_sigma_log, F_mcgaugh)
    chi2_outer_sqt = chi2_general(o_gbar, o_gobs, o_sigma_log, a0_sqt_p, F_mcgaugh)
    print(f"[E] outer-only ({o.shape[0]} galaxies): a0={a0_outer:.4e}  "
          f"chi2={chi2_outer:.1f}  sig_log={sig_outer:.4f}")
    # Inner-only too
    inner = []
    for g in galaxies:
        R = g['R']
        if R.size == 0:
            continue
        Vobs = g['Vobs']
        errV = g['errV']
        good = (R > 0) & (Vobs > 0) & (errV > 0)
        if not np.any(good):
            continue
        Vd = g['Vdisk'][good] * KM
        Vb = g['Vbul'][good] * KM
        Vg = g['Vgas'][good] * KM
        sq = lambda a: np.sign(a) * a ** 2
        Vbar2 = UPSILON_DISK * sq(Vd) + UPSILON_BUL * sq(Vb) + sq(Vg)
        valid = Vbar2 > 0
        if not np.any(valid):
            continue
        Rg = R[good][valid] * KPC
        Vo = Vobs[good][valid] * KM
        eV = errV[good][valid] * KM
        Vbar2 = Vbar2[valid]
        idx = int(np.argmin(Rg))
        inner.append((Vbar2[idx] / Rg[idx], Vo[idx] ** 2 / Rg[idx],
                      2.0 * Vo[idx] * eV[idx] / Rg[idx]))
    inn = np.array(inner)
    i_gbar, i_gobs, i_eg = inn[:, 0], inn[:, 1], inn[:, 2]
    i_elog = i_eg / (np.maximum(i_gobs, 1e-300) * math.log(10.0))
    i_sigma_log = np.sqrt(i_elog ** 2 + 0.13 ** 2)
    a0_inner, la_inner, chi2_inner, sig_inner = fit_a0_general(
        i_gbar, i_gobs, i_sigma_log, F_mcgaugh)
    print(f"[E] inner-only ({inn.shape[0]} galaxies): a0={a0_inner:.4e}  "
          f"chi2={chi2_inner:.1f}  sig_log={sig_inner:.4f}")

    # K-criteria audit (M16, full sample, with rescaled sigma)
    K_R1 = abs(1.0 - a0_sqt_p / a0_m16) <= 0.30
    delta_log = math.log10(a0_m16) - math.log10(a0_sqt_p)
    K_R2_orig = abs(delta_log) <= 2.0 * sig_m16
    K_R2_resc = abs(delta_log) <= 2.0 * sig_resc
    K_R3 = (chi2_m16_sqt / n_pts) <= 1.5
    aicc_free = chi2_m16_free + 2 * 1 + 2 * 1 * 2 / max(n_pts - 1 - 1, 1)
    aicc_sqt = chi2_m16_sqt
    K_R4 = (aicc_sqt - aicc_free) <= 2.0
    # Newton chi2 (g_obs = g_bar)
    res_n = (np.log10(gobs) - np.log10(gbar)) / sigma_log
    chi2_n = float(np.sum(res_n ** 2))
    K_R5 = (aicc_sqt - chi2_n) <= -10.0

    # New audit checks:
    K_R6_shape_robust = log_a0_spread_dex <= 0.04   # 10 % across functional forms
    K_R7_outer_inner_consistent = abs(math.log10(a0_outer) - math.log10(a0_inner)) <= 0.10

    n_pass = sum([K_R1, K_R2_orig, K_R3, K_R4, K_R5])
    n_pass_strict = sum([K_R1, K_R2_resc, K_R3, K_R4, K_R5,
                         K_R6_shape_robust, K_R7_outer_inner_consistent])

    out = dict(
        H0_planck=H0_PLANCK,
        a0_sqt_planck=float(a0_sqt_p),
        a0_mcgaugh=float(A0_MCGAUGH),
        n_pts=int(n_pts),
        n_gal=int(n_gal),
        # (A) reproduction
        repro_M16=dict(a0=float(a0_m16), chi2=float(chi2_m16_free),
                       sigma_log=float(sig_m16),
                       chi2_sqt=float(chi2_m16_sqt),
                       chi2_per_dof=float(chi2_m16_free / (n_pts - 1))),
        L482_reported=dict(a0=1.0686771873602096e-10, chi2=4384.4642839662665,
                           sigma_log=0.006),
        repro_match=dict(
            d_a0_pct=float(abs(a0_m16 - 1.0686771873602096e-10) /
                           1.0686771873602096e-10 * 100),
            d_chi2=float(abs(chi2_m16_free - 4384.4642839662665))),
        # (B) alternative forms
        simple_nu=dict(a0=float(a0_simple), chi2=float(chi2_s_free),
                       chi2_sqt=float(chi2_s_sqt), sigma_log=float(sig_s)),
        standard=dict(a0=float(a0_std), chi2=float(chi2_std_free),
                      chi2_sqt=float(chi2_std_sqt), sigma_log=float(sig_std)),
        cross_form_spread_dex=float(log_a0_spread_dex),
        # (D) sigma rescaling
        rescaled=dict(rescale_factor=float(rescale),
                      a0=float(a0_resc), sigma_log=float(sig_resc),
                      chi2_per_dof=float(chi2_resc_free / (n_pts - 1))),
        # (E) channel independence
        outer_only=dict(n=int(o.shape[0]), a0=float(a0_outer),
                        chi2=float(chi2_outer), sigma_log=float(sig_outer)),
        inner_only=dict(n=int(inn.shape[0]), a0=float(a0_inner),
                        chi2=float(chi2_inner), sigma_log=float(sig_inner)),
        outer_inner_log10_diff=float(abs(math.log10(a0_outer) - math.log10(a0_inner))),
        # K
        K_audit=dict(
            K_R1=bool(K_R1), K_R2_orig=bool(K_R2_orig),
            K_R2_resc=bool(K_R2_resc), K_R3=bool(K_R3),
            K_R4=bool(K_R4), K_R5=bool(K_R5),
            K_R6_shape_robust=bool(K_R6_shape_robust),
            K_R7_outer_inner_consistent=bool(K_R7_outer_inner_consistent),
            n_pass_orig5=int(n_pass),
            n_pass_strict7=int(n_pass_strict),
        ),
    )
    out_json = ROOT / 'results' / 'L489' / 'L489_results.json'
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(out, indent=2, default=float))
    print(f"\nWrote {out_json}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
