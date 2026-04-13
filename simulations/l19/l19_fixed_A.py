# -*- coding: utf-8 -*-
"""
L19 Phase 3: A 고정 시뮬레이션
A = 0.0863 (2e^-pi) vs A = 0.0611 (sqrt(2)*e^-pi) vs A 자유
현재 13pt BAO 데이터로 두 이론값 판별 가능성 정량화
"""
import os, sys, json, time
import numpy as np
from scipy.optimize import minimize
from scipy.interpolate import interp1d

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
np.seterr(all='ignore')

_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_THIS))
_SIMS = os.path.join(_ROOT, 'simulations')
for _p in (_SIMS,):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# ── 상수 ──────────────────────────────────────────────────────────────────────
c_SI    = 2.998e8
Mpc_m   = 3.086e22
OMEGA_R = 9.1e-5
RS_DRAG = 147.09
H0_KMS  = 67.7
H0_SI   = H0_KMS * 1e3 / Mpc_m

N_Z   = 3000
Z_MAX = 6.0
Z_ARR = np.linspace(0.0, Z_MAX, N_Z)

from desi_data import DESI_DR2, DESI_DR2_COV_INV
OBS_13  = DESI_DR2['value']
INV_COV = DESI_DR2_COV_INV
Z_13    = DESI_DR2['z_eff']
QTYPES  = DESI_DR2['quantity']


def _E_LCDM(Om, z_arr):
    OL0 = 1.0 - Om - OMEGA_R
    return np.sqrt(OMEGA_R*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0)


def make_EE2(Om, A, B):
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01: return None
    E   = _E_LCDM(Om, Z_ARR)
    lnE = B * np.log(np.maximum(E, 1e-10))
    return OL0 * (1.0 + A * (1.0 - np.cos(np.minimum(lnE, 20))))


def chi2_13pt(Om, A, B):
    arr = make_EE2(Om, A, B)
    if arr is None: return 1e8
    E2  = OMEGA_R*(1+Z_ARR)**4 + Om*(1+Z_ARR)**3 + np.maximum(arr, 0)
    Ea  = np.sqrt(np.maximum(E2, 1e-15))
    ei  = interp1d(Z_ARR, Ea, kind='cubic', bounds_error=False,
                   fill_value=(float(Ea[0]), float(Ea[-1])))
    z_int = np.linspace(0, Z_MAX*0.99, 6000)
    inv_E = 1.0 / np.maximum(ei(z_int), 1e-10)
    dz    = np.diff(z_int)
    cum   = np.zeros(len(z_int))
    for i in range(1, len(z_int)):
        cum[i] = cum[i-1] + 0.5*(inv_E[i-1]+inv_E[i])*dz[i-1]
    chi_fn = interp1d(z_int, cum, kind='cubic', fill_value='extrapolate', bounds_error=False)
    fac    = c_SI / (H0_SI * Mpc_m)
    pred   = np.zeros(13)
    for i, (z, qt) in enumerate(zip(Z_13, QTYPES)):
        DM = fac * chi_fn(z)
        DH = fac / ei(z)
        if qt == 'DV_over_rs':
            DV = (z * DM**2 * DH)**(1.0/3.0)
            pred[i] = DV / RS_DRAG
        elif qt == 'DM_over_rs':
            pred[i] = DM / RS_DRAG
        elif qt == 'DH_over_rs':
            pred[i] = DH / RS_DRAG
    if not np.all(np.isfinite(pred)): return 1e8
    resid = pred - OBS_13
    c2    = float(resid @ INV_COV @ resid)
    return c2 if np.isfinite(c2) and c2 < 1e8 else 1e8


def fit_free(n_starts=60):
    """A 자유: 3파라미터 (Om, A, B) 최적화"""
    rng  = np.random.RandomState(42)
    best = (1e9, None)
    bounds = [(0.28,0.36),(0.0,0.5),(0.1,30.0)]
    for _ in range(n_starts):
        Om0 = rng.uniform(0.28, 0.36)
        A0  = rng.uniform(0.0,  0.3)
        B0  = rng.uniform(0.5,  20.0)
        def obj(p): return chi2_13pt(p[0], p[1], max(p[2],0.01))
        try:
            r = minimize(obj, [Om0, A0, B0], method='Nelder-Mead',
                         options={'maxiter':8000,'xatol':1e-6,'fatol':1e-6})
            if r.fun < best[0]:
                best = (r.fun, r.x.copy())
        except Exception:
            pass
    return best


def fit_fixed_A(A_fixed, n_starts=60):
    """A 고정: 2파라미터 (Om, B) 최적화"""
    rng  = np.random.RandomState(42)
    best = (1e9, None)
    for _ in range(n_starts):
        Om0 = rng.uniform(0.28, 0.36)
        B0  = rng.uniform(0.5,  20.0)
        def obj(p): return chi2_13pt(p[0], A_fixed, max(p[1],0.01))
        try:
            r = minimize(obj, [Om0, B0], method='Nelder-Mead',
                         options={'maxiter':8000,'xatol':1e-6,'fatol':1e-6})
            if r.fun < best[0]:
                best = (r.fun, r.x.copy())
        except Exception:
            pass
    return best


def aicc(chi2, k, n=13):
    return chi2 + 2*k + 2*k*(k+1)/max(n-k-1,1)


def main():
    import math
    A_theory_2   = 2.0 * math.exp(-math.pi)      # = 0.08627
    A_theory_rt2 = math.sqrt(2) * math.exp(-math.pi)  # = 0.06104

    print("L19 Phase 3: A 고정 시뮬레이션")
    print(f"A_theory [2*e^-pi]    = {A_theory_2:.5f}")
    print(f"A_theory [sqrt2*e^-pi]= {A_theory_rt2:.5f}")
    print()

    t0 = time.time()

    # 케이스 0: A 자유
    print("케이스 0: A 자유 (3파라미터)...")
    c2_free, p_free = fit_free()
    aicc_free = aicc(c2_free, 3)
    print(f"  chi2={c2_free:.4f}, Om={p_free[0]:.4f}, A={p_free[1]:.4f}, B={p_free[2]:.4f}, AICc={aicc_free:.3f}")

    # 케이스 1: A = 2e^(-pi)
    print(f"\n케이스 1: A = 2*e^-pi = {A_theory_2:.5f} 고정 (2파라미터)...")
    c2_case1, p1 = fit_fixed_A(A_theory_2)
    aicc_case1 = aicc(c2_case1, 2)
    print(f"  chi2={c2_case1:.4f}, Om={p1[0]:.4f}, B={p1[1]:.4f}, AICc={aicc_case1:.3f}")
    dchi2_1 = c2_case1 - c2_free
    print(f"  delta_chi2 vs free = {dchi2_1:+.4f}")

    # 케이스 2: A = sqrt(2)*e^(-pi)
    print(f"\n케이스 2: A = sqrt(2)*e^-pi = {A_theory_rt2:.5f} 고정 (2파라미터)...")
    c2_case2, p2 = fit_fixed_A(A_theory_rt2)
    aicc_case2 = aicc(c2_case2, 2)
    print(f"  chi2={c2_case2:.4f}, Om={p2[0]:.4f}, B={p2[1]:.4f}, AICc={aicc_case2:.3f}")
    dchi2_2 = c2_case2 - c2_free
    print(f"  delta_chi2 vs free = {dchi2_2:+.4f}")

    print(f"\n완료: {(time.time()-t0)/60:.1f}분")

    print("\n" + "="*60)
    print("[판별 결과]")
    print("="*60)
    print(f"chi2(A자유)   = {c2_free:.4f}  (기준)")
    print(f"chi2(A=0.086) = {c2_case1:.4f}  (delta={dchi2_1:+.4f})")
    print(f"chi2(A=0.061) = {c2_case2:.4f}  (delta={dchi2_2:+.4f})")
    print()

    if abs(dchi2_1) < 1.0 and abs(dchi2_2) < 1.0:
        print("판정: 현재 13pt 데이터로 두 값 구별 불가 (delta_chi2 < 1.0)")
        print("      DESI full / Euclid 데이터 필요")
    elif dchi2_1 < dchi2_2 and dchi2_2 - dchi2_1 > 1.0:
        print(f"판정: A = 0.086 (2e^-pi) 선호 (우위: delta_chi2 = {dchi2_2-dchi2_1:.3f})")
    elif dchi2_2 < dchi2_1 and dchi2_1 - dchi2_2 > 1.0:
        print(f"판정: A = 0.061 (sqrt2*e^-pi) 선호 (우위: delta_chi2 = {dchi2_1-dchi2_2:.3f})")
    else:
        print(f"판정: 경계 — 미세한 선호 있으나 유의하지 않음")

    # AICc 비교 (파라미터 수가 다르므로 AICc가 적절)
    print()
    print(f"AICc(A자유, k=3)   = {aicc_free:.3f}")
    print(f"AICc(A=0.086, k=2) = {aicc_case1:.3f}  (delta={aicc_case1-aicc_free:+.3f})")
    print(f"AICc(A=0.061, k=2) = {aicc_case2:.3f}  (delta={aicc_case2-aicc_free:+.3f})")
    print("(AICc가 작을수록 좋음. delta < 0이면 고정이 오히려 더 경제적)")

    result = {
        'A_theory_2epim': round(A_theory_2, 6),
        'A_theory_rt2epim': round(A_theory_rt2, 6),
        'free': {'chi2': round(c2_free,4), 'AICc': round(aicc_free,3),
                 'Om': round(float(p_free[0]),5), 'A': round(float(p_free[1]),5),
                 'B': round(float(p_free[2]),4)},
        'fixed_2epim': {'chi2': round(c2_case1,4), 'AICc': round(aicc_case1,3),
                        'dchi2': round(dchi2_1,4),
                        'Om': round(float(p1[0]),5), 'B': round(float(p1[1]),4)},
        'fixed_rt2epim': {'chi2': round(c2_case2,4), 'AICc': round(aicc_case2,3),
                          'dchi2': round(dchi2_2,4),
                          'Om': round(float(p2[0]),5), 'B': round(float(p2[1]),4)},
    }
    out = os.path.join(_THIS, 'l19_fixed_A_results.json')
    with open(out, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\n저장: {out}")


if __name__ == '__main__':
    main()
