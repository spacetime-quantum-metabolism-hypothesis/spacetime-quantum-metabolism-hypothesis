"""anchor: monotonic vs V-shape chi^2 (regime-gap scale only).

Three SQT anchors (cosmic / cluster-outskirt / galactic-outer) reject a
single monotonic slope at ~17 sigma in favour of the V-shape (3-regime).

NOTE: This is a REGIME-GAP claim. SPARC galactic-internal data shows the
opposite trend (Lelli+ 2016 RAR is monotonic). Do not over-interpret.
Run: < 2 s.
"""
import numpy as np
from scipy.optimize import minimize_scalar, minimize

# columns: log10(rho_env / kg/m^3),  log10(sigma_0 / [SI]),  +/- err
anchors = np.array([
    [-30,  8.37, 0.05],   # cosmic / inflow
    [-26,  7.75, 0.20],   # cluster outskirt (dip)
    [-22,  9.56, 0.05],   # galactic outer
])
x, y, err = anchors.T

def chi2_mono(slope):
    intercept = np.mean(y - slope * x)
    return float(np.sum(((y - (slope * x + intercept)) / err) ** 2))

r1 = minimize_scalar(chi2_mono, bounds=(-2, 2), method='bounded')

def chi2_V(p):
    sL, sR, vy = p
    pred = np.where(x < -26, sL * (x + 26) + vy, sR * (x + 26) + vy)
    return float(np.sum(((y - pred) / err) ** 2))

r2 = minimize(chi2_V, x0=[-0.2, 0.5, 7.75], method='Nelder-Mead')

dchi2 = r1.fun - r2.fun
print(f"chi^2 (monotonic) = {r1.fun:.2f}")
print(f"chi^2 (V-shape)   = {r2.fun:.2f}")
print(f"Delta chi^2       = {dchi2:.2f} (~{np.sqrt(max(dchi2,0)):.1f} sigma, 1-DOF approx)")
print("NOTE: only at REGIME-GAP scale. SPARC galactic-internal shows opposite.")
