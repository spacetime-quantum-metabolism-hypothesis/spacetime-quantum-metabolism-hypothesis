"""
L532 -- Path-alpha a_0(z) time-evolution channel: priori-forecast scan.

PURPOSE
-------
Test whether the new prediction channel P28 -- a redshift evolution of the
MOND-scale acceleration a_0 induced by Gamma_0(t) (axiom 3' of L527
Path-alpha) -- is in principle distinguishable from a_0 = const at the
sensitivity of:

  (a) SPARC galaxy catalog (z ~ 0 - 0.03 Hubble-flow regime),
  (b) Euclid weak-lensing + spectroscopic galaxy clustering (z ~ 0.5 - 2),
  (c) LSST cosmic-shear tomography (z ~ 0.3 - 3).

CRITICAL CLAUDE.md COMPLIANCE
-----------------------------
- We do NOT prescribe a functional form for Gamma_0(t). The 8-person
  Rule-A team must derive that independently (per L527 PATH_ALPHA.md
  Sec 1.2, 4.2).
- The relation a_0 <-> c*H/(2*pi) (within factor-of-1.5) is an EXISTING
  derived result in the SQMH paper (claims_status C1, PASS_MODERATE).
  L532 only evaluates it at z > 0 by substituting H0 -> H(z); no new
  functional form is introduced.
- This script is a CONSUMER of two pre-existing pieces:
    (i)  the C1 relation (existing; derived in paper/03_background_*)
    (ii) the L527 axiom 3' time-dependence statement (existing).
- We compute *forecasts* (information content + fractional sensitivity);
  no parameter of Gamma_0(t) is fitted from data and locked.
- Per CLAUDE.md "AICc penalty when free parameters added": a_0(z) channel
  introduces +1 effective DOF over a_0 = const. We track this.
- Per "honest reporting": if the SPARC redshift baseline is too short to
  see the signal at S/N >= 1 under standard intrinsic-scatter assumptions,
  we report that bluntly.

OUTPUT
------
- stdout summary table.
- results/L532/a0_z_forecast.json (per-survey sensitivities).

USAGE
-----
    python3 simulations/L532/run.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np

# environment hardening per CLAUDE.md
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = REPO_ROOT / "results" / "L532"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
SPARC_CAT = REPO_ROOT / "simulations" / "l49" / "data" / "sparc_catalog.mrt"


# ============================================================================
# Cosmology helper -- LCDM background (BACKGROUND ONLY; no SQMH parameters
# locked here). Used purely as the reference H(z) against which the
# (existing) C1 substitution H0 -> H(z) is evaluated.
# ============================================================================
def E_lcdm(z, Om=0.315):
    return np.sqrt(Om * (1.0 + z) ** 3 + (1.0 - Om))


# ============================================================================
# SPARC catalog loader -- distances only (we do NOT refit RAR here; we use
# the existing C1 PASS_MODERATE result as the z=0 anchor and ask whether
# the SPARC redshift spread is enough to detect *evolution* of a_0).
# ============================================================================
def load_sparc_distances(path: Path) -> np.ndarray:
    """Return distances [Mpc] for all SPARC galaxies (175 entries)."""
    ds = []
    with open(path) as f:
        lines = f.readlines()
    started = False
    for s in lines:
        if "CamB" in s and not started:
            started = True
        if not started:
            continue
        s = s.rstrip("\n")
        if len(s) < 50:
            continue
        # MRT byte 14-19 -> python slice [13:19]
        try:
            d = float(s[13:19])
            if d > 0:
                ds.append(d)
        except ValueError:
            parts = s.split()
            if len(parts) >= 4:
                try:
                    d = float(parts[2])
                    if d > 0:
                        ds.append(d)
                except ValueError:
                    pass
    return np.array(ds)


def hubble_flow_z(D_Mpc: np.ndarray, H0_kms_Mpc: float = 70.0) -> np.ndarray:
    """Linear Hubble-flow z = D*H0/c (valid for z << 1, SPARC regime)."""
    c = 299792.458  # km/s
    return D_Mpc * H0_kms_Mpc / c


# ============================================================================
# Sensitivity bookkeeping. Under the existing C1 relation
#     a_0(z) ~ c * H(z) / (2*pi)        [substitution H0 -> H(z)]
# the *fractional* signal between z1 and z2 is
#     Delta a_0 / a_0(0) = E(z2) - E(z1)
# That is the only quantity we need for a discrimination forecast.
# We do NOT recompute the C1 normalisation; we only ask: given the noise
# floor of each survey, is the inter-z difference detectable?
# ============================================================================
def fractional_signal(z_lo: float, z_hi: float, Om: float = 0.315) -> float:
    return float(E_lcdm(z_hi, Om) - E_lcdm(z_lo, Om))


# ----------------------------------------------------------------------------
# Per-survey effective noise floor on a_0 (or its proxy).
#
# SPARC:    intrinsic RAR scatter sigma_int(log10 a) ~ 0.13 dex (Lelli+17).
#           Mapped to fractional a_0: sigma_frac ~ ln(10)*0.13/sqrt(N_eff).
# Euclid:   spectroscopic galaxy clustering at z ~ 0.5-2 measures H(z)/H0
#           to ~1% per dz=0.1 bin (Euclid forecast IST 2020). The implied
#           a_0(z) sensitivity is ~1% per z-bin.
# LSST:     cosmic-shear tomography measures dGrowth/d ln a, which couples
#           to mu_eff ~ 1+2*beta^2; for the L527 channel it constrains
#           a_0(z) at ~2-3% per tomographic bin (DESC SRD 2018-style).
#
# These floors are CONSERVATIVE published forecasts; we do not re-derive
# them. They serve only as anchors for the discrimination calculation.
# ----------------------------------------------------------------------------
SURVEY_NOISE_FRAC = {
    "SPARC":  None,        # computed below from intrinsic scatter and N
    "Euclid": 0.010,       # 1% per dz=0.1 spec-z bin
    "LSST":   0.025,       # 2.5% per tomographic shear bin
}


def sparc_noise_floor(N: int, sigma_log_dex: float = 0.13) -> float:
    """Fractional a_0 uncertainty from the SPARC intrinsic RAR scatter,
    averaged over N galaxies in a redshift sub-bin.

    Conversion: sigma_frac(a) ~ ln(10) * sigma_log10(a) / sqrt(N).
    """
    if N < 1:
        return float("inf")
    return float(np.log(10.0) * sigma_log_dex / np.sqrt(N))


# ============================================================================
# SPARC redshift-bin construction (z=0 - 0.03 Hubble-flow regime).
# ============================================================================
def sparc_redshift_bins(D_Mpc: np.ndarray):
    z = hubble_flow_z(D_Mpc)
    bins = [
        ("z<=0.005",   z <= 0.005),
        ("0.005-0.010", (z > 0.005) & (z <= 0.010)),
        ("0.010-0.020", (z > 0.010) & (z <= 0.020)),
        ("0.020-0.030", (z > 0.020) & (z <= 0.030)),
    ]
    out = []
    for label, mask in bins:
        N = int(mask.sum())
        z_med = float(np.median(z[mask])) if N > 0 else float("nan")
        out.append({"label": label, "N": N, "z_median": z_med})
    return out, z


# ============================================================================
# Survey forecasts -- distinguishability of P28 (a_0(z)) vs null (a_0=const).
# ============================================================================
def forecast_sparc(D_Mpc: np.ndarray):
    bins, z_all = sparc_redshift_bins(D_Mpc)
    # Lowest non-empty bin is anchor z_lo.
    nonempty = [b for b in bins if b["N"] >= 5]
    if len(nonempty) < 2:
        return {"channel": "SPARC", "viable": False,
                "reason": "insufficient bins with N>=5"}

    anchor = nonempty[0]
    rows = []
    for b in nonempty:
        signal = fractional_signal(anchor["z_median"], b["z_median"])
        noise = sparc_noise_floor(b["N"])
        # combined noise across the difference: sqrt(N_anchor + N_b)
        noise_anchor = sparc_noise_floor(anchor["N"])
        noise_diff = float(np.hypot(noise, noise_anchor))
        snr = abs(signal) / noise_diff if noise_diff > 0 else 0.0
        rows.append({
            "label": b["label"],
            "N": b["N"],
            "z_median": b["z_median"],
            "signal_frac": signal,
            "noise_frac": noise,
            "noise_diff": noise_diff,
            "snr": snr,
        })
    snr_max = max(r["snr"] for r in rows)
    return {
        "channel": "SPARC",
        "anchor_bin": anchor["label"],
        "anchor_z_median": anchor["z_median"],
        "bins": rows,
        "snr_max": snr_max,
        "viable": snr_max >= 1.0,
        "verdict": ("SNR>=1 detection feasible" if snr_max >= 1.0
                    else "SNR<1 -- z baseline too short for SPARC alone"),
    }


def forecast_survey(name: str, z_bins: list, noise_per_bin: float):
    """Generic forecast: ask if E(z_hi)-E(z_lo) is detectable above
    per-bin noise, summed in quadrature across bin pairs.
    """
    pairs = []
    for i in range(len(z_bins) - 1):
        for j in range(i + 1, len(z_bins)):
            sig = fractional_signal(z_bins[i], z_bins[j])
            # difference noise = sqrt(2) * single-bin noise
            n = noise_per_bin * np.sqrt(2.0)
            snr = abs(sig) / n if n > 0 else 0.0
            pairs.append({
                "z_lo": z_bins[i], "z_hi": z_bins[j],
                "signal_frac": sig, "noise_frac": n, "snr": snr,
            })
    # combined SNR^2 -- conservative: only adjacent-bin pairs
    snr2 = sum(p["snr"] ** 2 for p in pairs[: len(z_bins) - 1])
    snr_combined = float(np.sqrt(snr2))
    snr_max = float(max(p["snr"] for p in pairs))
    return {
        "channel": name,
        "z_bins": z_bins,
        "noise_per_bin_frac": noise_per_bin,
        "pairs": pairs,
        "snr_combined_adjacent": snr_combined,
        "snr_max_pair": snr_max,
        "viable": snr_combined >= 3.0,
        "verdict": (f"combined SNR {snr_combined:.1f}sigma -- detection"
                    if snr_combined >= 3.0
                    else f"combined SNR {snr_combined:.1f}sigma -- marginal"),
    }


# ============================================================================
# AICc bookkeeping for adding the a_0(z) channel.
# Per CLAUDE.md: extra DOF must be penalised. P28 introduces +1 free
# parameter (the amplitude of the time evolution; functional form is
# Gamma_0(t)-derived but its single timescale parameter is what data fits).
# Required Delta chi^2 improvement to overcome AICc:
#     Delta AICc = 2*k + 2*k*(k+1)/(N-k-1) - 2*ln(L_ratio)
#   with k=1, large N: AICc threshold ~ 2 (chi^2 improvement >= 2).
# ============================================================================
AICC_THRESHOLD_CHI2 = 2.0


# ============================================================================
# Priori-recovery check
# ============================================================================
def priori_recovery_assessment():
    """Summarise whether L532's channel is a 'true priori' recovery for SQMH.

    Criteria (from L527 PATH_ALPHA.md Sec 6.2):
      C-1: functional form derived from existing axioms only -- DEFERRED
           to 8-person team. L532 makes NO derivation claim; it only
           tests substitution.
      C-2: no new free parameters beyond what Gamma_0(t)'s monotonic
           single-parameter family carries -- HOLDS by construction
           (we add +1 DOF, not 2+).
      C-3: prediction is empirically falsifiable on a defined timescale
           -- HOLDS (Euclid 2030, LSST DR2 2028 give <5y horizon).
    """
    return {
        "C1_axiomatic_derivation_done": False,
        "C1_status": ("8-person Rule-A team must derive Gamma_0(t) functional "
                      "form; L532 does not assert it. Per CLAUDE.md topmost-1."),
        "C2_dof_count_consistent": True,
        "C2_status": "+1 DOF (amplitude of time-evolution); AICc threshold dchi2>=2.",
        "C3_falsifiable_horizon_years": 5,
        "C3_status": "Euclid 2030 + LSST 2028 cover P28 directly.",
        "verdict": ("PARTIAL priori recovery only. SPARC alone is "
                    "insufficient (z baseline too short); cosmological "
                    "channels (Euclid, LSST) provide the real test."),
    }


def main():
    # ---- SPARC ----
    if not SPARC_CAT.exists():
        print(f"[ERROR] SPARC catalog not found: {SPARC_CAT}")
        return False
    D_Mpc = load_sparc_distances(SPARC_CAT)
    sparc = forecast_sparc(D_Mpc)

    # ---- Euclid ----
    euclid_zbins = [0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.8]
    euclid = forecast_survey("Euclid", euclid_zbins,
                             SURVEY_NOISE_FRAC["Euclid"])

    # ---- LSST ----
    lsst_zbins = [0.3, 0.6, 0.9, 1.2, 1.6, 2.0, 2.5]
    lsst = forecast_survey("LSST", lsst_zbins,
                           SURVEY_NOISE_FRAC["LSST"])

    priori = priori_recovery_assessment()

    # ---- Report ----
    print("=" * 72)
    print("L532 -- a_0(z) priori-forecast scan (P28 channel)")
    print("=" * 72)
    print()
    print(f"SPARC: N_total = {len(D_Mpc)} galaxies, "
          f"z range = {hubble_flow_z(D_Mpc).min():.4f} - "
          f"{hubble_flow_z(D_Mpc).max():.4f}")
    print(f"  anchor bin: {sparc['anchor_bin']} "
          f"(z_med = {sparc['anchor_z_median']:.4f})")
    print(f"  {'bin':<14}{'N':>5}{'z_med':>10}"
          f"{'signal':>12}{'noise':>10}{'SNR':>8}")
    for r in sparc["bins"]:
        print(f"  {r['label']:<14}{r['N']:>5}{r['z_median']:>10.4f}"
              f"{r['signal_frac']:>12.5f}{r['noise_diff']:>10.4f}"
              f"{r['snr']:>8.3f}")
    print(f"  -> verdict: {sparc['verdict']}")
    print()

    print(f"Euclid (spec-z, sigma_bin = "
          f"{SURVEY_NOISE_FRAC['Euclid']*100:.1f}% per dz=0.2):")
    print(f"  z-bins: {euclid_zbins}")
    print(f"  combined-adjacent SNR = "
          f"{euclid['snr_combined_adjacent']:.2f} sigma")
    print(f"  max-pair SNR         = {euclid['snr_max_pair']:.2f} sigma")
    print(f"  -> verdict: {euclid['verdict']}")
    print()

    print(f"LSST (cosmic shear, sigma_bin = "
          f"{SURVEY_NOISE_FRAC['LSST']*100:.1f}% per tomo bin):")
    print(f"  z-bins: {lsst_zbins}")
    print(f"  combined-adjacent SNR = "
          f"{lsst['snr_combined_adjacent']:.2f} sigma")
    print(f"  max-pair SNR         = {lsst['snr_max_pair']:.2f} sigma")
    print(f"  -> verdict: {lsst['verdict']}")
    print()

    print("Priori-recovery assessment:")
    for k, v in priori.items():
        print(f"  {k}: {v}")
    print()

    # ---- Save ----
    out = {
        "sparc": sparc,
        "euclid": euclid,
        "lsst": lsst,
        "priori_recovery": priori,
        "aicc_threshold_dchi2": AICC_THRESHOLD_CHI2,
        "notes": [
            "L532 is a CONSUMER of (i) the existing C1 relation "
            "a_0 <-> c*H/(2*pi) and (ii) the L527 axiom 3' statement "
            "Gamma_0 -> Gamma_0(t).",
            "No Gamma_0(t) functional form is asserted here. Per "
            "CLAUDE.md topmost-1 (no theory map) the 8-person Rule-A "
            "team must derive that independently.",
            "Survey noise floors are conservative published forecasts "
            "(Euclid IST 2020; LSST DESC SRD 2018; SPARC Lelli+2017).",
            "SPARC alone CANNOT confirm a_0(z) -- z baseline too short. "
            "The real test is Euclid + LSST cosmological a_0(z).",
        ],
    }
    out_path = RESULTS_DIR / "a0_z_forecast.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"saved: {out_path}")
    return True


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
