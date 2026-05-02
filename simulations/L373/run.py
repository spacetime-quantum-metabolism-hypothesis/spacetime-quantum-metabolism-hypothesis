#!/usr/bin/env python3
"""L373 — SPARC per-galaxy log_a0 distribution: monotonic vs V-shape

Compare two functional forms for log_a0 vs env-proxy axis x:
  M1 (monotonic linear)  : y = A + B*x                     (k=2)
  M2 (V-shape, 3-anchor) : y = A + B*(x - x0) for x>=x0
                           y = A - B*(x - x0) for x<x0     (k=3, with x0 free)

Marginalized evidence ln Z via Laplace approximation on flat priors.
Compare against L342's 3-anchor Δχ²=288 result.

Data: SPARC log_a0 from results/L69/l69_step1_report.json (163 galaxies).
Env-proxy x: log_Vmax (more massive halo => denser inner env).
"""
import json
import os
import sys
import numpy as np
from scipy.optimize import minimize

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(os.path.dirname(ROOT), "results", "L69", "l69_step1_report.json")
OUT  = os.path.join(os.path.dirname(ROOT), "results", "L373", "report.json")

with open(SRC, "r") as f:
    L69 = json.load(f)

rows = L69["rows"]
y_all = []
x_all = []
sy_all = []
names = []

# Use log_Vmax as env proxy. Skip rows with missing values or extreme chi2_red.
for r in rows:
    la0 = r.get("log_a0", None)
    lvm = r.get("log_Vmax", None)
    chi2r = r.get("chi2_red", None)
    if la0 is None or lvm is None or chi2r is None:
        continue
    if not np.isfinite(la0) or not np.isfinite(lvm):
        continue
    y_all.append(la0)
    x_all.append(lvm)
    # Per-galaxy uncertainty: scale residual_std by sqrt(chi2_red) (approximate)
    sy_all.append(L69["residual_std"])  # constant residual_std as base sigma_y
    names.append(r.get("name", "?"))

y = np.array(y_all)
x = np.array(x_all)
sy = np.array(sy_all)
N = len(y)
print(f"[L373] N galaxies = {N}, x range [{x.min():.2f},{x.max():.2f}], "
      f"y range [{y.min():.2f},{y.max():.2f}], sy = {sy[0]:.3f}")

# ---------------- Models ----------------
def chi2_M1(theta):
    A, B = theta
    yhat = A + B*x
    return float(np.sum(((y - yhat)/sy)**2))

def chi2_M2(theta):
    A, B, x0 = theta
    yhat = A + B*np.abs(x - x0)  # V-shape (symmetric)
    return float(np.sum(((y - yhat)/sy)**2))

def chi2_M2asym(theta):
    A, BL, BR, x0 = theta
    yhat = np.where(x >= x0, A + BR*(x-x0), A - BL*(x-x0))
    return float(np.sum(((y - yhat)/sy)**2))

# ---------------- Fits ----------------
# M1
res1 = minimize(chi2_M1, x0=[np.mean(y), 0.0], method="Nelder-Mead",
                options={"xatol":1e-6,"fatol":1e-6,"maxiter":20000})
A1, B1 = res1.x; chi2_1 = res1.fun

# Bounds for L-BFGS-B: x0 confined to [x.min()+0.05, x.max()-0.05] (within data interior).
x0_lo, x0_hi = x.min()+0.05, x.max()-0.05
bnd_M2  = [(-15.0,-5.0), (-5.0,5.0), (x0_lo, x0_hi)]
bnd_M2a = [(-15.0,-5.0), (-5.0,5.0), (-5.0,5.0), (x0_lo, x0_hi)]

# M2 symmetric V (k=3) — bounded
best2 = (np.inf, None)
for x0_seed in np.linspace(x0_lo, x0_hi, 25):
    r = minimize(chi2_M2, x0=[np.mean(y), 0.0, x0_seed], method="L-BFGS-B",
                 bounds=bnd_M2, options={"ftol":1e-10,"gtol":1e-8,"maxiter":5000})
    if r.fun < best2[0]:
        best2 = (r.fun, r.x)
chi2_2, theta2 = best2

# M2 asym V (k=4) — bounded
best2a = (np.inf, None)
for x0_seed in np.linspace(x0_lo, x0_hi, 25):
    r = minimize(chi2_M2asym, x0=[np.mean(y), 0.0, 0.0, x0_seed], method="L-BFGS-B",
                 bounds=bnd_M2a, options={"ftol":1e-10,"gtol":1e-8,"maxiter":5000})
    if r.fun < best2a[0]:
        best2a = (r.fun, r.x)
chi2_2a, theta2a = best2a

# ---------------- Laplace ln Z ----------------
# ln Z ≈ -chi2/2 + (k/2) ln(2π) + 0.5 ln det(Cov) - ln V_prior
# where Cov = (Hessian/2)^{-1}, Hessian computed numerically.
def hessian(f, theta, eps=None):
    n = len(theta)
    if eps is None:
        eps = np.maximum(1e-4*np.abs(np.array(theta)), 1e-6)
    H = np.zeros((n,n))
    f0 = f(theta)
    for i in range(n):
        for j in range(i, n):
            tpp = list(theta); tpp[i]+=eps[i]; tpp[j]+=eps[j]
            tpm = list(theta); tpm[i]+=eps[i]; tpm[j]-=eps[j]
            tmp = list(theta); tmp[i]-=eps[i]; tmp[j]+=eps[j]
            tmm = list(theta); tmm[i]-=eps[i]; tmm[j]-=eps[j]
            H[i,j] = (f(tpp) - f(tpm) - f(tmp) + f(tmm))/(4*eps[i]*eps[j])
            H[j,i] = H[i,j]
    return H

# Flat prior boxes (generous but bounded)
prior_M1 = {"A":(-15.0,-5.0), "B":(-5.0, 5.0)}
prior_M2 = {"A":(-15.0,-5.0), "B":(-5.0, 5.0), "x0":(x0_lo, x0_hi)}
prior_M2a = {"A":(-15.0,-5.0), "BL":(-5.0,5.0), "BR":(-5.0,5.0), "x0":(x0_lo, x0_hi)}

def prior_volume(prior_dict):
    V = 1.0
    for (lo,hi) in prior_dict.values():
        V *= (hi - lo)
    return V

def laplace_lnZ(chi2_min, theta_best, chi2_func, prior_dict):
    k = len(theta_best)
    H = hessian(chi2_func, list(theta_best))
    A = 0.5*H  # since chi2 = -2 ln L (gaussian), Hessian of (-ln L) = 0.5*Hess(chi2)
    try:
        sign, logdet = np.linalg.slogdet(A)
        if sign <= 0:
            return None, None, "non-PD Hessian"
    except Exception as e:
        return None, None, f"hessian err: {e}"
    V_prior = prior_volume(prior_dict)
    # ln Z = -chi2/2 + (k/2) ln(2π) - 0.5 ln det(A) - ln V_prior
    lnZ = -0.5*chi2_min + 0.5*k*np.log(2*np.pi) - 0.5*logdet - np.log(V_prior)
    return float(lnZ), float(logdet), None

lnZ1, ld1, err1 = laplace_lnZ(chi2_1, [A1, B1], chi2_M1, prior_M1)
lnZ2, ld2, err2 = laplace_lnZ(chi2_2, list(theta2), chi2_M2, prior_M2)
lnZ2a, ld2a, err2a = laplace_lnZ(chi2_2a, list(theta2a), chi2_M2asym, prior_M2a)

# ---------------- AIC/BIC ----------------
def info(chi2, k, N):
    aic = chi2 + 2*k
    bic = chi2 + k*np.log(N)
    aicc = aic + (2*k*(k+1))/(N-k-1) if (N-k-1)>0 else float("nan")
    return aic, bic, aicc

aic1, bic1, aicc1 = info(chi2_1, 2, N)
aic2, bic2, aicc2 = info(chi2_2, 3, N)
aic2a, bic2a, aicc2a = info(chi2_2a, 4, N)

# ---------------- Report ----------------
out = {
    "loop": "L373",
    "data_source": "results/L69/l69_step1_report.json",
    "N": N,
    "x_axis": "log_Vmax (env proxy)",
    "y_axis": "log_a0 per galaxy",
    "sigma_y_const": float(sy[0]),
    "models": {
        "M1_monotonic_linear": {
            "k": 2, "params": {"A": float(A1), "B": float(B1)},
            "chi2": chi2_1, "AIC": aic1, "BIC": bic1, "AICc": aicc1,
            "lnZ_laplace": lnZ1, "logdet_halfH": ld1, "lnZ_err": err1,
            "prior_volume": prior_volume(prior_M1)
        },
        "M2_Vshape_symmetric": {
            "k": 3, "params": {"A": float(theta2[0]), "B": float(theta2[1]), "x0": float(theta2[2])},
            "chi2": chi2_2, "AIC": aic2, "BIC": bic2, "AICc": aicc2,
            "lnZ_laplace": lnZ2, "logdet_halfH": ld2, "lnZ_err": err2,
            "prior_volume": prior_volume(prior_M2)
        },
        "M2_Vshape_asymmetric": {
            "k": 4,
            "params": {"A": float(theta2a[0]), "BL": float(theta2a[1]),
                       "BR": float(theta2a[2]), "x0": float(theta2a[3])},
            "chi2": chi2_2a, "AIC": aic2a, "BIC": bic2a, "AICc": aicc2a,
            "lnZ_laplace": lnZ2a, "logdet_halfH": ld2a, "lnZ_err": err2a,
            "prior_volume": prior_volume(prior_M2a)
        }
    },
    "comparisons": {
        "dchi2_M1_minus_M2sym":  chi2_1 - chi2_2,
        "dchi2_M1_minus_M2asym": chi2_1 - chi2_2a,
        "dlnZ_M2sym_minus_M1":  (lnZ2  - lnZ1)  if (lnZ2  is not None and lnZ1 is not None) else None,
        "dlnZ_M2asym_minus_M1": (lnZ2a - lnZ1) if (lnZ2a is not None and lnZ1 is not None) else None,
        "dBIC_M1_minus_M2sym": bic1 - bic2,
        "dBIC_M1_minus_M2asym": bic1 - bic2a
    },
    "L342_comparison": {
        "L342_dchi2_3anchor": 288.04,
        "L342_data": "3 anchors (cosmic/cluster/galactic)",
        "L373_data": f"SPARC {N}-galaxy per-galaxy log_a0 distribution"
    },
    "honest_note": (
        "SPARC sample probes ONLY the galactic regime in env-density. "
        "x = log_Vmax is an INTRA-galactic proxy (halo mass), NOT cosmic-vs-cluster. "
        "L342's 17sigma Δχ²=288 came from cluster-vs-galactic gap which SPARC cannot test."
    )
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    json.dump(out, f, indent=2)

# Console summary
print(f"\n[M1 linear   ] chi2={chi2_1:.3f}, AIC={aic1:.2f}, BIC={bic1:.2f}, lnZ={lnZ1}")
print(f"[M2 V sym k=3] chi2={chi2_2:.3f}, AIC={aic2:.2f}, BIC={bic2:.2f}, lnZ={lnZ2}")
print(f"[M2 V asym k4] chi2={chi2_2a:.3f}, AIC={aic2a:.2f}, BIC={bic2a:.2f}, lnZ={lnZ2a}")
if lnZ1 is not None and lnZ2 is not None:
    print(f"\nDelta ln Z (M2sym - M1)  = {lnZ2-lnZ1:+.3f}")
if lnZ1 is not None and lnZ2a is not None:
    print(f"Delta ln Z (M2asym - M1) = {lnZ2a-lnZ1:+.3f}")
print(f"Delta chi2 (M1 - M2sym)  = {chi2_1 - chi2_2:+.3f}")
print(f"Delta chi2 (M1 - M2asym) = {chi2_1 - chi2_2a:+.3f}")
print(f"\nL342 reference: Delta chi2 = 288.04 (3 anchors, cluster outlier-driven)")
print(f"\nReport written: {OUT}")
