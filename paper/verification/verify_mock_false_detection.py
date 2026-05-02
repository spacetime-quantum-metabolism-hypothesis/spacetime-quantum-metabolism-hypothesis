"""LCDM mock 200 -> three-regime false-detection rate.

CAVEAT: high false-positive rate => anchor-driven advantage on null data.
This is the *honest reproduction* of paper §6.1 internal-audit caveat:
the anchor-fit advantage of the 3-regime model survives even on data with
no true regime structure, so the SPARC ΔAICc must be interpreted with
this baseline in mind.

Run: < 60 s.
"""
import numpy as np

rng = np.random.default_rng(42)
N_MOCK, N_GAL, ERR, sigma_truth = 200, 175, 0.10, 9.0

false = 0
for _ in range(N_MOCK):
    obs = rng.normal(sigma_truth, ERR, N_GAL)
    chi2_uni = float(np.sum(((obs - obs.mean()) / ERR) ** 2))
    s = np.sort(obs)
    t = N_GAL // 3
    g1, g2, g3 = s[:t], s[t:2 * t], s[2 * t:]
    chi2_3R = float(sum(np.sum(((g - g.mean()) / ERR) ** 2) for g in (g1, g2, g3)))
    aicc_uni = chi2_uni + 2 * 1 + 4 / (N_GAL - 2)
    aicc_3R = chi2_3R + 2 * 3 + 24 / (N_GAL - 4)
    if (aicc_uni - aicc_3R) > 10:
        false += 1

rate = false / N_MOCK
print(f"three-regime false-detection rate on LCDM mock: {rate:.1%}")
print("CAVEAT: high rate => anchor-driven advantage on null data.")
