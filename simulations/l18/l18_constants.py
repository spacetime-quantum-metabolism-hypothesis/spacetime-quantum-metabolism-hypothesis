# -*- coding: utf-8 -*-
"""
L18 Phase 2: EE2 상수 A, B 단위 분석
omega_de = OL0*(1+A*(1-cos(B*ln(H/H0))))

MCMC 결과를 읽어 A, B 값과 자연 스케일 비교.
"""
import os, sys, json
import numpy as np

_THIS = os.path.dirname(os.path.abspath(__file__))

# ── 기본 상수 ──────────────────────────────────────────────────────────────────
H0_KMS  = 67.7          # km/s/Mpc (Planck 2018)
H0_SI   = H0_KMS * 1e3 / 3.086e22  # s^-1
c_SI    = 2.998e8       # m/s
G_SI    = 6.674e-11     # m^3 kg^-1 s^-2
hbar_SI = 1.055e-34     # J*s
kB_SI   = 1.381e-23     # J/K
T_CMB   = 2.7255        # K

# 우주론 파라미터 (MCMC 또는 L17 best-fit)
Om   = 0.3055
OL0  = 1.0 - Om - 9.1e-5

# EE2 파라미터 (MCMC 읽기 시도, 없으면 L17 best-fit)
mcmc_path = os.path.join(_THIS, 'l18_mcmc_results.json')
if os.path.exists(mcmc_path):
    with open(mcmc_path) as f:
        mcmc = json.load(f)
    A_best = mcmc['A']['median']
    B_best = mcmc['B']['median']
    A_err  = (mcmc['A']['lo'] + mcmc['A']['hi']) / 2
    B_err  = (mcmc['B']['lo'] + mcmc['B']['hi']) / 2
    source = 'MCMC'
else:
    A_best = 0.088
    B_best = 8.76
    A_err  = 0.02   # 추정
    B_err  = 0.5    # 추정
    source = 'L17 best-fit (MCMC 없음)'

print(f"EE2 상수 분석 (source: {source})")
print(f"A = {A_best:.4f} +/- {A_err:.4f}")
print(f"B = {B_best:.3f} +/- {B_err:.3f}")
print(f"B/A = {B_best/A_best:.2f}")
print()


# ── B 분석 ────────────────────────────────────────────────────────────────────

print("="*60)
print("B 분석: 무차원수 자연 스케일 목록")
print("="*60)

# 우주론 스케일
z_eq   = 3402.0         # 물질-복사 동등점 (Planck 2018)
z_cmb  = 1089.8         # 재결합 (Planck 2018)
z_mde  = (OL0/Om)**(1/3) - 1  # 물질-DE 동등점
z_bbn  = 2e8            # BBN

candidates_B = [
    ("ln(1+z_eq) [물질-복사 동등점]",  np.log(1+z_eq)),
    ("ln(1+z_cmb) [재결합]",           np.log(1+z_cmb)),
    ("ln(1+z_mde) [물질-DE 동등점]",   np.log(1+z_mde)),
    ("pi^2",                            np.pi**2),
    ("3*pi",                            3*np.pi),
    ("e^2",                             np.e**2),
    ("2*pi*e",                          2*np.pi*np.e),
    ("1/Om",                            1/Om),
    ("OL0/Om^2",                        OL0/Om**2),
    ("sqrt(OL0/Om^3)",                  np.sqrt(OL0/Om**3)),
    ("ln(OL0/Om)^2",                    np.log(OL0/Om)**2),
    ("N_eq_matter [e-fold 물질우세]",   np.log(1+z_eq) - np.log(1+z_mde)),
    ("H0*t_univ [H0*13.8Gyr]",         H0_KMS/978.0),  # H0 in s^-1, t=13.8Gyr=4.35e17s
    ("ln(rho_Lambda/rho_m0)^(1/3)",     np.log((OL0/Om)**(1/3))),
    ("sqrt(Om/OL0)*ln(1+z_eq)",         np.sqrt(Om/OL0)*np.log(1+z_eq)),
    ("OL0*ln(1+z_eq)",                  OL0*np.log(1+z_eq)),
]

print(f"\n{'스케일':<40} {'값':>8}  {'|B-val|/B':>10}  {'sigma':>8}")
print("-"*75)
for name, val in candidates_B:
    diff = abs(B_best - val) / B_best
    sigma = abs(B_best - val) / B_err if B_err > 0 else float('inf')
    flag = " <-- ***" if sigma < 2 else (" <-- *" if sigma < 5 else "")
    print(f"{name:<40} {val:>8.3f}  {diff:>10.3f}  {sigma:>8.2f}{flag}")

print()
print(f"B_best = {B_best:.3f}")


# ── A 분석 ────────────────────────────────────────────────────────────────────

print()
print("="*60)
print("A 분석: 무차원 진폭 자연 스케일")
print("="*60)

omega_b  = 0.02237
omega_c  = 0.12000
omega_m  = omega_b + omega_c
h        = 0.677
Omega_b  = omega_b / h**2
Omega_nu = 3.046 * (7/8) * (4/11)**(4/3) * 2.4728e-5 / h**2  # radiation

candidates_A = [
    ("Om^2",                             Om**2),
    ("Omega_b/Om [바리온 분율]",         Omega_b/Om),
    ("omega_b [바리온 물리밀도]",        omega_b),
    ("1/(2*pi^2)",                       1/(2*np.pi**2)),
    ("sqrt(Om*OL0)-OL0",                 abs(np.sqrt(Om*OL0)-OL0)),
    ("(Om/OL0)^3",                       (Om/OL0)**3),
    ("Om*(Om/OL0)^2",                    Om*(Om/OL0)**2),
    ("1/B_best",                         1/B_best),
    ("Om/B_best",                        Om/B_best),
    ("OL0/(4*pi*B_best)",                OL0/(4*np.pi*B_best)),
    ("exp(-B_best/pi)",                  np.exp(-B_best/np.pi)),
    ("exp(-sqrt(OL0/Om)*pi)",            np.exp(-np.sqrt(OL0/Om)*np.pi)),
    ("Om^(3/2)*OL0^(1/2)",              Om**1.5 * OL0**0.5),
    ("(Om*OL0)^(1/2)/B_best",           np.sqrt(Om*OL0)/B_best),
    ("Omega_b*B_best/OL0",              Omega_b*B_best/OL0),
]

print(f"\n{'스케일':<45} {'값':>8}  {'|A-val|/A':>10}  {'sigma':>8}")
print("-"*78)
for name, val in candidates_A:
    diff = abs(A_best - val) / A_best
    sigma = abs(A_best - val) / A_err if A_err > 0 else float('inf')
    flag = " <-- ***" if sigma < 2 else (" <-- *" if sigma < 5 else "")
    print(f"{name:<45} {val:>8.4f}  {diff:>10.3f}  {sigma:>8.2f}{flag}")

print()
print(f"A_best = {A_best:.4f}")


# ── B/A 비율 분석 ─────────────────────────────────────────────────────────────

print()
print("="*60)
print("B/A 비율 분석")
print("="*60)
BA = B_best / A_best
print(f"B/A = {BA:.2f}")

candidates_BA = [
    ("100",                  100.0),
    ("1/Om",                 1/Om),
    ("ln(1+z_eq)/Om",        np.log(1+z_eq)/Om),
    ("B/A = B/(Om^2*ln...)", np.log(1+z_eq)**2 / Om),
    ("pi^2/Om^2",            np.pi**2/Om**2),
    ("1/(Om*Omega_b)",       1/(Om*Omega_b)),
    ("OL0/omega_b",          OL0/omega_b),
    ("ln(1+z_eq)^2/(Om*OL0)", np.log(1+z_eq)**2/(Om*OL0)),
]

print(f"\n{'스케일':<45} {'값':>8}  {'|BA-val|/BA':>12}")
print("-"*70)
for name, val in candidates_BA:
    diff = abs(BA - val) / BA
    print(f"{name:<45} {val:>8.2f}  {diff:>12.3f}")


# ── EE2 물리적 해석 ────────────────────────────────────────────────────────────

print()
print("="*60)
print("EE2 물리적 해석 (피팅 파라미터 기반)")
print("="*60)

# 첫 번째 peak z: B*ln(E)=pi → E=exp(pi/B)
import sys
sys.path.insert(0, os.path.join(_THIS, '..'))
from desi_data import DESI_DR2
OMEGA_R_val = 9.1e-5

E_peak = np.exp(np.pi / B_best)
# LCDM 에서 E_peak 해당 z
# E^2 = OMEGA_R*(1+z)^4 + Om*(1+z)^3 + OL0
# 수치 풀기
z_arr = np.linspace(0, 3, 10000)
E2_arr = OMEGA_R_val*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0
E_arr  = np.sqrt(E2_arr)
from scipy.interpolate import interp1d
E_of_z = interp1d(z_arr, E_arr, kind='cubic')
z_of_E = interp1d(E_arr, z_arr, kind='cubic', fill_value='extrapolate', bounds_error=False)
z_peak = float(z_of_E(E_peak)) if E_peak < E_arr.max() else float('nan')

print(f"\nEE2 첫 번째 peak:")
print(f"  B*ln(E) = pi 조건: E = exp(pi/B) = exp(pi/{B_best:.2f}) = {E_peak:.4f}")
print(f"  해당 z_peak = {z_peak:.3f}")
print(f"  DESI 관측 범위 (0.1~2.3): {'포함' if 0 < z_peak < 2.3 else '범위 밖'}")

# DE peak 값
print(f"\nomega_de at z_peak: OL0*(1+2A) = {OL0*(1+2*A_best):.4f}")
print(f"omega_de at z=0:    OL0        = {OL0:.4f}")
print(f"peak 대비 증폭:     1+2A       = {1+2*A_best:.4f} (=+{2*A_best*100:.1f}%)")

# w(z) 해석
print(f"\nw0 ≈ -1 + A*B*pi/(3*OL0) (선도차수 근사)")
w0_approx = -1.0 + A_best * np.pi / (3.0)
print(f"  = -1 + {A_best:.4f}*pi/3 = {w0_approx:.3f}")
print(f"  (L17 수치: w0=-0.874)")


# ── 저장 ───────────────────────────────────────────────────────────────────────

results = {
    'source': source,
    'A': A_best, 'A_err': A_err,
    'B': B_best, 'B_err': B_err,
    'B_over_A': BA,
    'z_peak_first': z_peak,
    'Om': Om, 'OL0': OL0,
    'candidates_B_best': [],
    'candidates_A_best': [],
}

# 가장 유력한 후보 (sigma < 3)
for name, val in candidates_B:
    sigma = abs(B_best - val) / B_err
    if sigma < 3:
        results['candidates_B_best'].append({'name': name, 'val': float(val), 'sigma': float(sigma)})

for name, val in candidates_A:
    sigma = abs(A_best - val) / A_err
    if sigma < 3:
        results['candidates_A_best'].append({'name': name, 'val': float(val), 'sigma': float(sigma)})

out = os.path.join(_THIS, 'l18_constants_results.json')
with open(out, 'w') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f"\n분석 결과 저장: {out}")
