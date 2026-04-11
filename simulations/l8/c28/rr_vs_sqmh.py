# -*- coding: utf-8 -*-
# CODE REVIEW: Bug-v Physics-v Repro-v Rules-v  [2026-04-11]
"""L8-R: Maggiore-Mancarella RR 비국소 보조장 vs SQMH 동형 탐색.

RR 배경 방정식 (Dirian+2015 PhysRevD 91, 083503):
  보조장: U = box^-1 R, P = V_dot = d/dt(box^-1 U)

FRW에서 (x = ln a 독립변수):
  dU/dx = U1 (=dU/dlna)
  dU1/dx = R/H^2 - (3 + Hdot/H^2)*U1
  dV/dx = V1
  dV1/dx = U/H^2 - (3 + Hdot/H^2)*V1 ... [Dirian Eq 2.5~2.8 simplified]

단순화 (물질+DE 배경, DE 밀도 포함):
  H^2 = H0^2*(Om*a^-3 + rho_DE/rho_c0)
  rho_DE = m^2*M_P^2/4*(2U - V1^2 + ...) [Dirian 근사식]

gamma0 = 0.0015 (L5 posterior mean) -> m^2 = gamma0 * H0^2 [근사]

Q33 판정:
  P(a) = V1(a) ~ n_bar(a) 로 보았을 때
  U(a) = Gamma0_eff - sigma_eff * P(a) * rho_m(a) 피팅
  잔차 < 20% -> Q33 PASS
"""
from __future__ import annotations
import json, os, sys
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import curve_fit

_HERE = os.path.dirname(os.path.abspath(__file__))

# 물리 상수
G_SI = 6.674e-11
hbar_SI = 1.0546e-34
c_SI = 2.998e8
t_P = np.sqrt(hbar_SI * G_SI / c_SI**5)
sigma_SQMH = 4 * np.pi * G_SI * t_P
M_P_kg = np.sqrt(hbar_SI * c_SI / G_SI)

Mpc_m = 3.0857e22
H0_SI = 67.76e3 / Mpc_m
rho_c0 = 3 * H0_SI**2 / (8 * np.pi * G_SI)
Om = 0.3095
OmDE = 1.0 - Om
rho_m0 = Om * rho_c0
gamma0 = 0.0015  # C28 best-fit

print('[L8-R] RR vs SQMH isomorphism analysis', flush=True)
print('[L8-R] gamma0 = %.4f, sigma_SQMH = %.3e' % (gamma0, sigma_SQMH), flush=True)

# ============================================================
# RR 배경 ODE (단순화 버전)
# ============================================================
# Dirian 2015 Eqs. 2.5-2.8 단순화:
# 상태벡터: [H^2/H0^2, U, U1, V, V1] where U1=dU/dlna, V1=dV/dlna
#
# 단순화 가정:
# 1. DE 에너지 밀도를 근사식으로:
#    rho_DE = m^2*M_P^2/4 * (2U - V1^2 + 3H*V*V1) [Maggiore 2014 근사]
#    단, V1이 초기에 0이므로: rho_DE ≈ m^2*M_P^2/2 * U
# 2. Ricci scalar: R = -6*(Hdot + 2H^2) ≈ -6*H^2*(1+q) 에서 q ~ deceleration param
#    R/H^2 = -6*(Hdot/H^2 + 2) = -6*(Edot/(2E*H) + 2) [계산 필요]
#
# 변수 재정의: h = H/H0, E^2 = H^2/H0^2
# 물질+RR DE:
#   E^2(a) = Om*a^-3 + OmDE_RR(a)
#   OmDE_RR = gamma0/2 * (U - 0.5*V1^2) [Omega_DE = rho_DE/rho_c]
#
# Hdot/H^2 = dE/dlna / (2E) * H0/H + ... = (1/2E)*dE^2/dlna / E^2
# 더 간단히: 압력 = w*rho: Hdot = -4piG*(rho+p) - H^2
#           Hdot/H^2 = -(3/2)*(1+weff)
#   weff = p_tot/rho_tot, p_tot = -rho_DE (DE 압력 ≈ -rho_DE 근사)

def rr_ode(state, lna, Om_val, gamma0_val, H0_val, rho_c0_val):
    """RR 배경 ODE.
    state = [U, U1, V, V1]
    lna = ln(a)
    """
    U, U1, V, V1 = state
    a = np.exp(lna)

    # DE 에너지 밀도 (Maggiore 근사)
    OmDE_RR = gamma0_val / 2.0 * (2.0*U - V1**2)
    OmDE_RR = max(-0.5*OmDE, min(2.0, OmDE_RR))  # 물리적 범위 클리핑

    # 전체 에너지 밀도 (평탄 우주)
    Om_m_a = Om_val * a**(-3)
    E2 = Om_m_a + OmDE_RR
    if E2 <= 0.01:
        E2 = 0.01  # 폭주 방지

    # Hdot/H^2 = -3/2 * (1 + w_eff)
    # w_eff * E2 = w_DE * OmDE_RR (w_m=0)
    # w_DE = p_DE/rho_DE: Maggiore 2014에서 RR에 대해 복잡, 근사: w_DE ~ -1 + eps
    # 단순화: Hdot/H^2 ~ -(3/2)*(1 + OmDE_RR/E2 * w_DE)
    # 배경 w_DE 근사: -0.88 (C28 best-fit w_eff)
    w_DE_approx = -0.88  # 근사값
    w_eff_approx = w_DE_approx * OmDE_RR / E2  # = w*OmDE/E2
    Hdot_over_H2 = -1.5 * (1.0 + w_eff_approx)

    # Ricci scalar: R/H^2 = -6*(Hdot/H^2 + 2)
    R_over_H2 = -6.0 * (Hdot_over_H2 + 2.0)

    # ODE:
    # dU/dlna = U1
    # dU1/dlna = R/H^2 - (3 + Hdot/H^2)*U1
    # dV/dlna = V1
    # dV1/dlna = U - (3 + Hdot/H^2)*V1

    friction = 3.0 + Hdot_over_H2
    dU = U1
    dU1 = R_over_H2 - friction * U1
    dV = V1
    dV1 = U - friction * V1

    return [dU, dU1, dV, dV1]

# 적분 범위
a_ini = 1e-3
lna_arr = np.linspace(np.log(a_ini), 0.0, 3000)
a_arr = np.exp(lna_arr)
z_arr = 1.0/a_arr - 1.0

# 초기조건 (물질우세기, 비국소항 비활성화)
state_ini = [0.0, 0.0, 0.0, 0.0]  # U, U1, V, V1 = 0

print('[L8-R] Integrating RR background ODE...', flush=True)
try:
    sol = odeint(rr_ode, state_ini, lna_arr,
                 args=(Om, gamma0, H0_SI, rho_c0),
                 rtol=1e-8, atol=1e-12, mxstep=5000)
    U_arr = sol[:, 0]
    U1_arr = sol[:, 1]
    V_arr = sol[:, 2]
    V1_arr = sol[:, 3]   # V1 = dV/dlna = V_dot / H -> n_bar proxy

    print('[L8-R] U(a=1) = %.4f, V(a=1) = %.4f, V1(a=1) = %.4f' % (
        U_arr[-1], V_arr[-1], V1_arr[-1]), flush=True)

    # P = V_dot = H * V1 (물리적 시간 미분) -> n_bar proxy
    H_arr = H0_SI * np.sqrt(np.maximum(Om*a_arr**(-3) + gamma0/2.0*(2.0*U_arr - V1_arr**2), 0.01))
    P_arr = H_arr * V1_arr  # [s^-1] 단위

    rho_m_arr = rho_m0 * a_arr**(-3)

    # ============================================================
    # SQMH 동형 피팅: U = Gamma0_eff - sigma_eff * P * rho_m
    # ============================================================
    print('\n[L8-R] Fitting U(a) = Gamma0_eff - sigma_eff * P(a) * rho_m(a)', flush=True)

    # a > 0.1 (z < 9) 에서만 피팅 (초기 트랜지언트 제외)
    mask = a_arr > 0.1
    U_fit = U_arr[mask]
    P_fit = P_arr[mask]
    rho_m_fit = rho_m_arr[mask]

    def model_func(X, Gamma0_eff, sigma_eff):
        P, rho_m = X
        return Gamma0_eff - sigma_eff * P * rho_m

    try:
        popt, pcov = curve_fit(
            model_func, (P_fit, rho_m_fit), U_fit,
            p0=[H0_SI, sigma_SQMH],
            maxfev=10000
        )
        Gamma0_eff, sigma_eff_fit = popt
        U_predicted = model_func((P_fit, rho_m_fit), Gamma0_eff, sigma_eff_fit)
        residual = np.abs(U_predicted - U_fit) / (np.abs(U_fit) + 1e-300)
        mean_residual = float(residual.mean())
        max_residual = float(residual.max())
        sigma_ratio = sigma_eff_fit / sigma_SQMH

        print('[L8-R] Gamma0_eff = %.3e, sigma_eff = %.3e' % (Gamma0_eff, sigma_eff_fit), flush=True)
        print('[L8-R] sigma_eff/sigma_SQMH = %.3e' % sigma_ratio, flush=True)
        print('[L8-R] Residual: mean=%.3f, max=%.3f' % (mean_residual, max_residual), flush=True)

        q33_pass = mean_residual < 0.20
        print('[L8-R] Q33 (residual < 20%%): %s' % ('PASS' if q33_pass else 'FAIL'), flush=True)

    except Exception as e:
        print('[L8-R] curve_fit failed: %s' % str(e)[:80], flush=True)
        Gamma0_eff = 0.0
        sigma_eff_fit = 0.0
        mean_residual = 999.0
        max_residual = 999.0
        sigma_ratio = 0.0
        q33_pass = False

    # ============================================================
    # E2(z) RR vs A12
    # ============================================================
    OmDE_RR_arr = np.maximum(gamma0/2.0*(2.0*U_arr - V1_arr**2), 0.0)
    E2_RR = Om * a_arr**(-3) + OmDE_RR_arr
    E2_A12 = 1.0 - Om*(1.0 - a_arr**3)
    sigma_chi = 0.01 * E2_A12
    chi2_RR_A12 = float(np.sum(((E2_RR - E2_A12)/sigma_chi)**2) / (len(a_arr)-1))
    print('[L8-R] E2 comparison RR vs A12: chi2/dof = %.4f' % chi2_RR_A12, flush=True)
    print('[L8-R] E2_RR at a=1: %.4f (target: 1.0)' % E2_RR[-1], flush=True)

    ode_success = True

except Exception as e:
    print('[L8-R] ODE integration failed: %s' % str(e)[:100], flush=True)
    q33_pass = False
    mean_residual = 999.0
    max_residual = 999.0
    sigma_eff_fit = 0.0
    Gamma0_eff = 0.0
    sigma_ratio = 0.0
    chi2_RR_A12 = 999.0
    ode_success = False

# ============================================================
# 저장
# ============================================================
out = {
    'phase': 'L8-R',
    'method': 'RR_auxiliary_field_SQMH_isomorphism',
    'gamma0': gamma0,
    'sigma_SQMH': float(sigma_SQMH),
    'Om': Om,
    'ode_success': ode_success,
    'isomorphism_fit': {
        'model': 'U(a) = Gamma0_eff - sigma_eff * P(a) * rho_m(a)',
        'P_def': 'V_dot = H * dV/dlna',
        'Gamma0_eff': float(Gamma0_eff),
        'sigma_eff': float(sigma_eff_fit),
        'sigma_ratio_to_SQMH': float(sigma_ratio),
        'mean_residual': float(mean_residual),
        'max_residual': float(max_residual),
        'fit_region': 'a > 0.1 (z < 9)',
    },
    'e2_comparison': {
        'chi2_dof_RR_vs_A12': float(chi2_RR_A12),
    },
    'q33_pass': bool(q33_pass),
    'k33_triggered': bool(mean_residual > 0.20 and ode_success),
    'interpretation': (
        'Q33 PASS: V_dot acts as effective n_bar in SQMH isomorphism (residual < 20%).' if q33_pass
        else 'Q33 FAIL: U(a) cannot be fit as SQMH source with residual < 20%.'
    ),
}
out_path = os.path.join(_HERE, 'rr_vs_sqmh.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, default=lambda x: float(x) if isinstance(x, (np.floating, np.integer)) else x)
print('\n[L8-R] Done. Saved to %s' % out_path, flush=True)
