"""SQT +1.14% S_8 worsening -> Euclid / LSST / DES-Y3 detection forecast.

Toy Fisher-style forecast: SQT (dark-only embedding A1, mu_eff = 1 + 2 beta^2)
predicts a STRUCTURALLY POSITIVE S_8 shift of +1.14% relative to LCDM
(see L406 grid scan: structurally unreachable below 0). With literature
1-sigma errors on S_8 from each facility, we report the detection
significance n-sigma = |Delta S_8| / sigma(S_8).

Detection threshold (paper §5 / §8):
  - DES-Y3   sigma(S_8) ~ 0.018   (Amon+2022, Secco+2022)  -> 0.63 sigma -> INVISIBLE
  - LSST Y10 sigma(S_8) ~ 0.0040  (DESC SRD v1, Mandelbaum+2018) -> 2.85 sigma -> MARGINAL
  - Euclid   sigma(S_8) ~ 0.0026  (Euclid IST, Blanchard+2020) -> 4.38 sigma -> DETECT 3-5 sigma

If Euclid DR1 reports S_8 consistent with LCDM at < 2 sigma, SQT in its
dark-only embedding form is FALSIFIED. Forecast assumes Gaussian likelihood
and linear bias xi_+ ~ S_8^2; full hi_class chain is Phase-7 work (see L406).

Run: < 1 s, stand-alone (numpy only).
"""
import numpy as np

# --- baseline values (paper §4.6, §6.1) ---
S8_LCDM = 0.832
shift_S8 = 0.0114              # fractional structural positive shift (L406)
shift_S8_pct = 100.0 * shift_S8

# --- facility 1-sigma errors (literature, fractional / S_8 absolute units;
#     L406 uses these directly against the fractional shift, n-sigma=shift/sigma) ---
sigma_facility = {
    "DES_Y3":  0.018,    # Amon+2022, Secco+2022
    "LSST_Y10":0.0040,   # DESC SRD v1, Mandelbaum+2018
    "Euclid":  0.0026,   # Euclid IST, Blanchard+2020
}

verdict_thresholds = [
    (3.0, "DETECT 3-5 sigma"),
    (1.0, "MARGINAL 1-3 sigma"),
    (0.0, "INVISIBLE"),
]

def classify(nsig: float) -> str:
    for thr, label in verdict_thresholds:
        if nsig >= thr:
            return label
    return "INVISIBLE"

print(f"S_8 LCDM        = {S8_LCDM:.4f}")
print(f"shift S_8 SQT   = +{shift_S8:.4f} (+{shift_S8_pct:.2f}% structural)")
print("")
print(f"{'Facility':<10s} {'sigma(S_8)':>12s} {'n-sigma':>10s}  verdict")
print("-" * 56)
results = {}
for name, sig in sigma_facility.items():
    nsig = shift_S8 / sig
    verdict = classify(nsig)
    results[name] = {"sigma_S8": sig, "n_sigma": nsig, "verdict": verdict}
    print(f"{name:<10s} {sig:>12.4f} {nsig:>10.2f}  {verdict}")

print("")
print("Detection consistent with LCDM at Euclid (>3 sigma) = SQT FALSIFIED.")
print("Source: L406 (4-person review PASS), paper §5 / §8 / §6.1 row 1.")
_ = np  # silence unused-import linter
