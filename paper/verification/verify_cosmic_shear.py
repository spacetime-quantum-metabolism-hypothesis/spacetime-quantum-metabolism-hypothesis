"""SQT +1.14% S_8 -> xi_+(10') +2.29% (toy, structural falsifier).

If Euclid / LSST detects xi_+(10') consistent with LCDM at <2% level,
SQT is FALSIFIED in its current form (S_8 prediction is structural,
not tunable). See paper §5 / §8.

Run: < 1 s.
"""
import numpy as np

S8_LCDM = 0.832
shift_S8 = 0.0114
S8_SQT = S8_LCDM * (1 + shift_S8)

xi_LCDM = S8_LCDM ** 2
xi_SQT = S8_SQT ** 2
shift_xi = (xi_SQT - xi_LCDM) / xi_LCDM

print(f"S_8 LCDM    = {S8_LCDM:.4f}")
print(f"S_8 SQT     = {S8_SQT:.4f} (+{shift_S8 * 100:.2f}%)")
print(f"xi_+ shift  = +{shift_xi * 100:.2f}%")
print("Detection by Euclid/LSST = SQT FALSIFIED (structural).")
_ = np  # silence unused-import linter
