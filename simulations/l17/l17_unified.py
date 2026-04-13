# -*- coding: utf-8 -*-
"""
L17 Phase 1: 통합 수식 현상적 검증
omega_de = OL0*(1+A*(1-cos(B1*theta + B2*ln(E))))
theta = (Om*(1+z)^3 - Om) / OL0
Stage 0T -> Stage 1 (13pt AICc) -> Stage 2 (물리) -> Stage 3 (Joint)
병렬: multiprocessing.spawn 3 프로세스

코드리뷰 수정 (2026-04-12):
- chi2_13pt: L15 검증 패턴으로 교체 (trapezoid, 올바른 변수명)
- 변수명 오류 수정: DESI_DR2_COV_INV (DESI_COV_INV 아님)
- 거리 인자: c_SI / (H0_SI * Mpc_m) 단위 L15 동일
"""
import os, sys, json, time
import numpy as np
from scipy.optimize import minimize, curve_fit
from scipy.interpolate import interp1d
import multiprocessing as mp

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
np.seterr(all='ignore')

_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_THIS))
_SIMS = os.path.join(_ROOT, 'simulations')
_L3   = os.path.join(_SIMS, 'l3')
for _p in (_SIMS, _L3, os.path.join(_SIMS, 'phase2')):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# ── 상수 ────────────────────────────────────────────────────────────────────────
c_SI    = 2.998e8
Mpc_m   = 3.086e22
OMEGA_R = 9.1e-5
RS_DRAG = 147.09
H0_KMS  = 67.7
H0_SI   = H0_KMS * 1e3 / Mpc_m
H0_H    = H0_KMS / 100.0
OMEGA_B = 0.02237

N_Z   = 3000
Z_MAX = 6.0
Z_ARR = np.linspace(0.0, Z_MAX, N_Z)

# ── DESI DR2 데이터 로드 (L15 동일 패턴) ──────────────────────────────────────
from desi_data import DESI_DR2, DESI_DR2_COV, DESI_DR2_COV_INV
OBS_13   = DESI_DR2['value']
INV_COV  = DESI_DR2_COV_INV
Z_13     = DESI_DR2['z_eff']
QTYPES   = DESI_DR2['quantity']


# ── chi2_13pt: L15 검증 패턴 그대로 ───────────────────────────────────────────

def _E_LCDM(Om, z_arr):
    OL0 = 1.0 - Om - OMEGA_R
    return np.sqrt(OMEGA_R*(1+z_arr)**4 + Om*(1+z_arr)**3 + OL0)


def _build_E_interp(z_arr, ode_arr, Om):
    E2 = OMEGA_R*(1+z_arr)**4 + Om*(1+z_arr)**3 + np.maximum(ode_arr, 0)
    E_arr = np.sqrt(np.maximum(E2, 1e-15))
    return interp1d(z_arr, E_arr, kind='cubic',
                    fill_value='extrapolate', bounds_error=False)


def _chi_interp(E_interp):
    """공동 거리 적분: trapezoid."""
    z_int = np.linspace(0, Z_MAX*0.99, 6000)
    inv_E = 1.0 / np.maximum(E_interp(z_int), 1e-10)
    dz    = np.diff(z_int)
    cum   = np.zeros(len(z_int))
    for i in range(1, len(z_int)):
        cum[i] = cum[i-1] + 0.5*(inv_E[i-1]+inv_E[i])*dz[i-1]
    return interp1d(z_int, cum, kind='cubic',
                    fill_value='extrapolate', bounds_error=False)


def chi2_13pt(z_arr, ode_arr, Om):
    """L15 검증 패턴 13pt chi2."""
    E_interp = _build_E_interp(z_arr, ode_arr, Om)
    chi_func = _chi_interp(E_interp)
    fac = c_SI / (H0_SI * Mpc_m)

    pred = np.zeros(13)
    for i, (z, qt) in enumerate(zip(Z_13, QTYPES)):
        DM = fac * chi_func(z)
        DH = fac / E_interp(z)
        if qt == 'DV_over_rs':
            DV = (z * DM**2 * DH)**(1.0/3.0)
            pred[i] = DV / RS_DRAG
        elif qt == 'DM_over_rs':
            pred[i] = DM / RS_DRAG
        elif qt == 'DH_over_rs':
            pred[i] = DH / RS_DRAG

    if not np.all(np.isfinite(pred)):
        return 1e8
    resid = pred - OBS_13
    c2 = float(resid @ INV_COV @ resid)
    return c2 if np.isfinite(c2) and c2 < 1e8 else 1e8


def aicc(chi2, k, n=13):
    pen = 2*k + 2*k*(k+1)/max(n-k-1, 1)
    return chi2 + pen


# ── 모델 함수 ──────────────────────────────────────────────────────────────────

def make_UNI(p):
    """통합: omega_de = OL0*(1+A*(1-cos(B1*theta + B2*lnE)))"""
    Om = p[0]; A = p[1]; B1 = max(p[2], 0.0); B2 = max(p[3], 0.0)
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01: return None
    E     = _E_LCDM(Om, Z_ARR)
    theta = B1 * (Om*(1+Z_ARR)**3 - Om) / max(OL0, 1e-10)
    lnE   = B2 * np.log(np.maximum(E, 1e-10))
    phase = np.minimum(theta + lnE, 20.0)
    return OL0 * (1.0 + A * (1.0 - np.cos(phase)))


def make_AX3(p):
    """B2=0 극한: AX3"""
    Om = p[0]; A = p[1]; B1 = max(p[2], 0.01)
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01: return None
    theta = B1 * (Om*(1+Z_ARR)**3 - Om) / max(OL0, 1e-10)
    return OL0 * (1.0 + A * (1.0 - np.cos(np.minimum(theta, 20))))


def make_EE2(p):
    """B1=0 극한: EE2"""
    Om = p[0]; A = p[1]; B2 = max(p[2], 0.01)
    OL0 = 1.0 - Om - OMEGA_R
    if OL0 < 0.01: return None
    E   = _E_LCDM(Om, Z_ARR)
    lnE = B2 * np.log(np.maximum(E, 1e-10))
    return OL0 * (1.0 + A * (1.0 - np.cos(np.minimum(lnE, 20))))


# ── Stage 0T ──────────────────────────────────────────────────────────────────

def stage0T(make_fn, p):
    """A1 이론 필터: omega_de 유한·양수 확인 + A >= 0 (A1 방향).
    고z에서 omega_de > OL0 는 A1 물리 (고z 물질 소멸 → DE 생성) 이므로 허용.
    이전 < OL0 기준은 오류 — AX3/EE2 모두 잘못 탈락시킴.
    """
    arr = make_fn(p)
    if arr is None: return False
    if not np.all(np.isfinite(arr)): return False
    if np.any(arr < 0): return False
    # A >= 0 : A1 방향 (물질 소멸 → DE 증가)
    A = float(p[1])
    if A < 0: return False
    return True


# ── Stage 1 최적화 ─────────────────────────────────────────────────────────────

def opt_stage1(make_fn, bounds_list, ndim, n_starts=60):
    """랜덤 다중 시작 Nelder-Mead. 4D에서 n_starts=60 사용."""
    best_chi2 = 1e9
    best_p    = None
    rng = np.random.RandomState(42)

    for _ in range(n_starts):
        p0 = np.array([rng.uniform(lo, hi) for lo, hi in bounds_list])

        def obj(p):
            arr = make_fn(p)
            if arr is None: return 1e8
            return chi2_13pt(Z_ARR, arr, p[0])

        try:
            res = minimize(obj, p0, method='Nelder-Mead',
                           options={'maxiter': 8000, 'xatol': 1e-5, 'fatol': 1e-5})
            if res.fun < best_chi2:
                best_chi2 = res.fun
                best_p    = res.x.copy()
        except Exception:
            pass

    return best_chi2, best_p


# ── Stage 2 ───────────────────────────────────────────────────────────────────

def extract_cpl(make_fn, p):
    arr = make_fn(p)
    if arr is None: return float('nan'), float('nan')
    z_fit = np.linspace(0.01, 1.5, 300); dz = 1e-4
    oi  = interp1d(Z_ARR, arr, kind='cubic', fill_value='extrapolate', bounds_error=False)
    u   = np.array([float(oi(z))            for z in z_fit])
    u_p = np.array([float(oi(z+dz))         for z in z_fit])
    u_m = np.array([float(oi(max(z-dz,1e-5))) for z in z_fit])
    dlnu = (u_p - u_m) / (2*dz * np.maximum(u, 1e-20))
    w_z  = (1+z_fit)*dlnu/3.0 - 1.0
    try:
        popt, _ = curve_fit(lambda z, w0, wa: w0+wa*(1-1/(1+z)),
                            z_fit, w_z, p0=[-0.9,-0.3],
                            bounds=([-3.,-10.],[0.5,5.]), maxfev=5000)
        return float(popt[0]), float(popt[1])
    except Exception:
        return float('nan'), float('nan')


def stage2_check(p, w0, wa):
    Om = p[0]
    if not (0.28 < Om < 0.36):  return False, f"Om={Om:.3f}"
    if not (-1.5 < w0 < -0.3):  return False, f"w0={w0:.3f}"
    if not (-3.0 < wa < 1.5):   return False, f"wa={wa:.3f}"
    return True, "OK"


# ── Stage 3 ───────────────────────────────────────────────────────────────────

def stage3_joint(make_fn, p):
    from l3.data_loader import chi2_joint, get_data
    get_data()
    arr = make_fn(p)
    if arr is None: return None
    Om = float(np.clip(p[0], 0.28, 0.36))
    E2 = OMEGA_R*(1+Z_ARR)**4 + Om*(1+Z_ARR)**3 + np.maximum(arr, 0)
    Ea = np.sqrt(np.maximum(E2, 1e-15))
    ei = interp1d(Z_ARR, Ea, kind='cubic', bounds_error=False,
                  fill_value=(float(Ea[0]), float(Ea[-1])))

    # CLAUDE.md 규칙: 고z 구간은 LCDM bridge. cubic extrapolation 금지.
    # CMB 적분은 z~1100 까지 필요 — DE 기여 무시 가능 (z>>6에서 matter+radiation 지배)
    Z_CUT = Z_MAX * 0.95

    def E_func(z):
        z = float(z)
        if z <= Z_CUT:
            return float(ei(z))
        # 고z: DE 기여 negligible → LCDM (matter + radiation)
        return float(np.sqrt(OMEGA_R*(1+z)**4 + Om*(1+z)**3))

    omega_c = Om*H0_H**2 - OMEGA_B
    if omega_c <= 0.01: return None
    try:
        return chi2_joint(E_func, rd=RS_DRAG, Omega_m=Om,
                          omega_b=OMEGA_B, omega_c=omega_c,
                          h=H0_H, H0_km=H0_KMS)
    except Exception:
        return None


# ── 워커 ────────────────────────────────────────────────────────────────────────

def run_model(args):
    label, make_fn, bounds_list, ndim = args
    import warnings; warnings.filterwarnings('ignore')

    chi2_s1, p_best = opt_stage1(make_fn, bounds_list, ndim)
    if p_best is None:
        return label, {'error': 'opt_failed'}

    aicc_val = aicc(chi2_s1, ndim)
    w0, wa   = extract_cpl(make_fn, p_best)
    s0t      = stage0T(make_fn, p_best)
    s2_ok, s2_msg = stage2_check(p_best, w0, wa)

    res3 = None
    if s0t and s2_ok:
        res3 = stage3_joint(make_fn, p_best)

    cj    = res3['total'] if res3 else None
    delta = (cj - 1687.763) if cj else None

    return label, {
        'stage0T':     'PASS' if s0t else 'FAIL',
        'stage2':      'PASS' if s2_ok else f'FAIL:{s2_msg}',
        'stage3':      'PASS' if cj else 'SKIP',
        'chi2_13pt':   round(chi2_s1, 4),
        'aicc':        round(aicc_val, 3),
        'daicc_lcdm':  round(aicc_val - 19.83, 3),
        'chi2_joint':  round(cj, 3) if cj else None,
        'delta_joint': round(delta, 3) if delta else None,
        'chi2_bao':    round(res3['bao'], 3) if res3 else None,
        'chi2_sn':     round(res3['sn'], 3)  if res3 else None,
        'chi2_cmb':    round(res3['cmb'], 3) if res3 else None,
        'chi2_rsd':    round(res3['rsd'], 3) if res3 else None,
        'w0': round(w0, 4), 'wa': round(wa, 4),
        'Om': round(float(p_best[0]), 5),
        'p':  [round(float(x), 6) for x in p_best],
        'ndim': ndim,
        'aicc_extra_vs_3param': round(aicc_val - 14.268, 3),  # vs EE2
    }


def main():
    tasks = [
        ('UNI-unified',  make_UNI,  [(0.28,0.36),(0.0,1.0),(0.0,30.0),(0.0,30.0)], 4),
        ('UNI-AX3',      make_AX3,  [(0.28,0.36),(0.0,1.0),(0.0,30.0)],            3),
        ('UNI-EE2',      make_EE2,  [(0.28,0.36),(0.0,1.0),(0.0,30.0)],            3),
    ]

    print("L17 Phase 1: 통합 수식 검증 (코드리뷰 후 재실행)")
    print(f"LCDM baseline: chi2_joint=1687.763, AICc=19.83")
    print(f"EE2 reference: chi2_joint=1657.04,  AICc=14.268")
    print(f"과적합 판정: UNI AICc 추가 패널티 +4.33 (4파라미터 vs 3파라미터)\n")

    t0 = time.time()
    ctx = mp.get_context('spawn')
    with ctx.Pool(processes=len(tasks)) as pool:
        results_list = pool.map(run_model, tasks)
    print(f"완료: {(time.time()-t0)/60:.1f}분\n")

    results = {}
    print(f"{'Model':<18} {'chi2_13':>8} {'AICc':>7} {'dAICc_LCDM':>11} "
          f"{'chi2_jt':>9} {'delta':>7} {'w0':>7} {'wa':>7}")
    print("-"*80)
    for label, r in results_list:
        results[label] = r
        print(f"{label:<18} "
              f"{str(r.get('chi2_13pt','-')):>8} "
              f"{str(r.get('aicc','-')):>7} "
              f"{str(r.get('daicc_lcdm','-')):>11} "
              f"{str(r.get('chi2_joint','-')):>9} "
              f"{str(r.get('delta_joint','-')):>7} "
              f"{str(r.get('w0','-')):>7} "
              f"{str(r.get('wa','-')):>7}")

    # 과적합 판정
    print("\n[과적합 판정]")
    uni = results.get('UNI-unified', {})
    ee2 = results.get('UNI-EE2', {})
    if uni.get('aicc') and ee2.get('aicc'):
        diff = uni['aicc'] - ee2['aicc']
        print(f"UNI AICc - EE2 AICc = {diff:+.3f}")
        if diff < 0:
            print("=> UNI가 AICc 기준 EE2보다 우수. 과적합 없음.")
        elif diff < 4.33:
            print("=> UNI가 AICc 기준 개선 없음. EE2 단독 선택 권장.")
        else:
            print("=> UNI AICc 악화. EE2 선택.")

    out = os.path.join(_THIS, 'l17_unified_results.json')
    with open(out, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n저장: {out}")


if __name__ == '__main__':
    mp.freeze_support()
    main()
