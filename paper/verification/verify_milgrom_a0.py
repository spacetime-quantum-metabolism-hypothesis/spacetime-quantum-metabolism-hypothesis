"""SQT derived 5: a_0 = c * H_0 / (2 * pi).

PASS_STRONG (substantive prediction): MOND acceleration scale.
Run: < 1 s, stand-alone (numpy only).
"""
import numpy as np

c = 2.998e8                       # m/s
H0 = 73e3 / 3.086e22              # s^-1

a0_SQT = c * H0 / (2.0 * np.pi)
a0_obs = 1.2e-10                  # m/s^2 (Begeman+ 1991, Famaey-McGaugh 2012)
a0_err = 0.1e-10

dev = abs(a0_SQT - a0_obs) / a0_err
print(f"a_0 (SQT)   = {a0_SQT:.3e} m/s^2")
print(f"a_0 (obs)   = {a0_obs:.3e} +/- {a0_err:.0e}")
print(f"deviation   = {dev:.2f} sigma")
print("PASS" if dev < 2 else "FAIL")
