#!/usr/bin/env python3
"""L487 — ET (Einstein Telescope) GW scalar mode forecast for SQT (P16).

Pre-registration: forecast detection significance of a scalar (breathing)
GW polarization predicted by SQT, using ET-D design sensitivity and a
Fisher-style amplitude estimator.

Honest framing
--------------
The SQT scalar-mode amplitude is *not* derived a priori from axioms 1-4.
We bracket the prediction by two paper-anchored structural arguments:

  (A) Pure disformal limit (paper §4.1 row C11D, Zumalacarregui 2013):
      scalar mode decouples at static order  ->  h_S/h_T ~ 0 (GR limit).
  (B) Cassini PPN bound on residual conformal coupling:
      |gamma - 1| < 2.3e-5  ->  beta_eff^2 ~< 1.15e-5
      h_S/h_T ~ |beta_eff|  ~< 3.4e-3  (ceiling).

We forecast ET-D sensitivity to (B) -- the *upper* SQT branch -- because
(A) is a null prediction (no scalar mode -> ET cannot distinguish from GR).
Detection of any h_S/h_T > sigma_ET would falsify the C11D/disformal
sector of SQT (paper §4.1).

Reference: Chatziioannou+ 2012 PRD 86 022004, Will 2014 LRR 17 4,
Maggiore+ 2020 JCAP 03 050 (ET design).
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent.parent.parent / "results" / "L487"
OUT.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# ET-D design sensitivity (Hild+ 2011, Maggiore+ 2020)
# ---------------------------------------------------------------------------
def Sn_ET_D(f):
    """ET-D one-sided strain noise PSD (1/Hz). Analytic fit from Hild+11.

    Valid 1 <= f <= 1e4 Hz; we evaluate over the scalar-mode-relevant band.
    """
    x = f / 200.0
    # Hild+11 Eq A2 fit coefficients (ET-D)
    a1, b1 = 2.39e-27, -15.64
    a2, b2 = 0.349, -2.145
    a3, b3 = 1.76, -0.12
    a4, b4 = 0.409, 1.10
    Sh = (
        a1 * x**b1
        + a2 * x**b2
        + a3 * x**b3
        + a4 * x**b4
    ) ** 2 * 1e-50
    return Sh


# ---------------------------------------------------------------------------
# Tensor-mode SNR for a fiducial BNS at z=0.1 (luminosity dist ~ 470 Mpc)
# ---------------------------------------------------------------------------
def tensor_snr_bns(D_L_Mpc=470.0, M_chirp_Msun=1.22):
    """Inspiral-only SNR for a 1.4-1.4 Msun BNS, ET-D, restricted PN."""
    # Restricted-PN h_T characteristic strain amplitude scaling
    # |h_T(f)| ~ A * f^{-7/6}, with A from Cutler-Flanagan 1994
    G = 6.674e-11
    c = 2.998e8
    Msun = 1.989e30
    Mpc = 3.086e22
    Mc = M_chirp_Msun * Msun
    DL = D_L_Mpc * Mpc
    A = (1.0 / np.pi ** (2.0 / 3.0)) * np.sqrt(5.0 / 24.0) * (
        (G * Mc) ** (5.0 / 6.0)
    ) / (c ** (3.0 / 2.0) * DL)
    f = np.geomspace(5.0, 2000.0, 4096)
    Sh = Sn_ET_D(f)
    integrand = (A * f ** (-7.0 / 6.0)) ** 2 / Sh
    snr2 = 4.0 * np.trapezoid(integrand, f)
    return float(np.sqrt(snr2))


# ---------------------------------------------------------------------------
# Scalar-mode Fisher uncertainty on h_S / h_T amplitude ratio
# ---------------------------------------------------------------------------
def sigma_hS_over_hT(snr_T, n_events=1):
    """Population-stacked Fisher 1-sigma on the scalar/tensor amplitude ratio.

    Single-event Fisher (Chatziioannou+12 Eq 22 simplified): for an
    independent breathing-mode channel that does not couple to the tensor
    waveform shape, sigma_{h_S/h_T} ~ 1/SNR_T per event.
    Stacked over n_events independent BNS: sigma -> sigma / sqrt(N).
    """
    return 1.0 / (snr_T * np.sqrt(n_events))


def main():
    snr_T = tensor_snr_bns()
    # ET BNS rate forecast: ~7e4 / yr detected with SNR>8 (Maggiore+ 2020).
    # Conservative pre-reg: 1 yr observation, only louds (SNR > 30): ~1e3.
    cases = {
        "single_BNS_at_470Mpc": 1,
        "1yr_loud_BNS_SNR30plus": 1000,
        "1yr_full_BNS_catalog": 70000,
    }

    # SQT prediction band (paper §4.1):
    #   minimal pure disformal (C11D):    h_S/h_T = 0 (null)
    #   Cassini-saturating conformal:     h_S/h_T <= 3.4e-3 (ceiling)
    sqt_null = 0.0
    sqt_ceiling = 3.4e-3  # 2 * |beta_eff|_max from Cassini |gamma-1|<2.3e-5

    forecasts = {}
    for label, N in cases.items():
        sig = sigma_hS_over_hT(snr_T, n_events=N)
        # detection significance of the *ceiling* prediction
        n_sigma_ceiling = sqt_ceiling / sig
        forecasts[label] = {
            "n_events": N,
            "sigma_hS_over_hT": sig,
            "n_sigma_at_ceiling_3p4e-3": n_sigma_ceiling,
            "decision": (
                "SQT pure-disformal SURVIVES if measured |h_S/h_T| < %.2g "
                "(1-sigma); FALSIFIED if > %.2g at >= 3 sigma."
            )
            % (sig, 3 * sig),
        }

    out = {
        "L_index": "L487",
        "preregistration_timestamp_UTC": "2026-05-01T13:47:30Z",
        "facility": "Einstein Telescope (ET-D, ~2030+)",
        "paper_anchor": "§4.1 row C11D + §4.5 ET GW scalar mode",
        "fiducial_BNS_SNR_tensor_at_470Mpc": snr_T,
        "SQT_prediction_band": {
            "minimal_disformal_C11D": sqt_null,
            "Cassini_ceiling_conformal": sqt_ceiling,
            "derivation": (
                "h_S/h_T ~ |beta_eff| with beta_eff^2 = (|gamma-1|)/2 from "
                "Will 2014 LRR Eq 36; |gamma-1| < 2.3e-5 (Cassini) -> "
                "|beta_eff| < 3.4e-3 (single-side amplitude)."
            ),
        },
        "forecasts": forecasts,
        "honesty_disclaimer": (
            "SQT minimal model predicts h_S/h_T = 0 exactly (pure disformal "
            "decouples scalar at static order). The 3.4e-3 ceiling is a "
            "Cassini-saturation upper envelope, NOT a positive SQT "
            "amplitude prediction. ET non-detection is consistent with "
            "BOTH SQT-minimal AND GR. ET POSITIVE detection of any "
            "|h_S/h_T| > 3.4e-3 falsifies the entire C11D sector."
        ),
        "decision_rule_preregistered": {
            "h_S_over_hT_measured__lt__sigma": "consistent with SQT-minimal & GR (null)",
            "sigma__le__h_S_over_hT__le__3p4e-3": "ambiguous - within Cassini envelope",
            "h_S_over_hT__gt__3p4e-3_at_3sigma": "C11D SECTOR FALSIFIED",
        },
    }

    with open(OUT / "forecast.json", "w") as f:
        json.dump(out, f, indent=2)
    print("[L487] forecast written to", OUT / "forecast.json")
    print("  tensor SNR (BNS @ 470 Mpc):", f"{snr_T:.1f}")
    for k, v in forecasts.items():
        print(
            "  ",
            k,
            ": sigma(h_S/h_T) =",
            f"{v['sigma_hS_over_hT']:.2e}",
            ", n_sigma at ceiling =",
            f"{v['n_sigma_at_ceiling_3p4e-3']:.2f}",
        )


if __name__ == "__main__":
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    main()
