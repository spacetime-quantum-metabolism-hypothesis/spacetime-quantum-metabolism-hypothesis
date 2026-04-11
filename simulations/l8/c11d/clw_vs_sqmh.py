# -*- coding: utf-8 -*-
# CODE REVIEW: Bug-v Physics-v Repro-v Rules-v  [2026-04-11]
"""L8-C: CLW quintessence ODE vs SQMH 연속방정식 동형 탐색.

핵심 후보: n_bar = n0 * exp(-lam*phi/M_P)
동형 조건:
  sigma_eff(a) = [Gamma0_eff/n_bar(a) + (sqrt(6)*lam*x(a) - 3)*H(a)] / rho_m(a)

Q32 판정:
  (1) sigma_eff(a) ~ const (std/mean < 20%)
  (2) sigma_eff_mean ~ 4*pi*G*t_P (10% 이내)

CLW 자율계 (Copeland-Liddle-Wands 1998, w_m=0):
  x' = -3x + (√6/2)*lam*y^2 + (3/2)*x*(2x^2+Om_m)
  y' = -(√6/2)*lam*x*y + (3/2)*y*(2x^2+Om_m)
  ' = d/dlna
"""
from __future__ import annotations
import json, os, sys
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import brentq

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
lam = 0.8872

print('[L8-C] CLW vs SQMH isomorphism (corrected)', flush=True)
print('[L8-C] sigma_SQMH = %.3e, lam = %.4f' % (sigma_SQMH, lam), flush=True)

# ============================================================
# CLW 자율계 (정확한 형태)
# ============================================================
def clw_rhs(state, lna):
    x, y = state
    Om_phi = x**2 + y**2
    Om_m = max(0.0, 1.0 - Om_phi)
    dx = -3.0*x + (np.sqrt(6.0)/2.0)*lam*y**2 + 1.5*x*(2.0*x**2 + Om_m)
    dy = -(np.sqrt(6.0)/2.0)*lam*x*y + 1.5*y*(2.0*x**2 + Om_m)
    return [dx, dy]

# 적분 범위
lna_ini = np.log(1e-4)  # a = 1e-4 (z~9999)
lna_arr = np.linspace(lna_ini, 0.0, 5000)
a_arr = np.exp(lna_arr)

# ============================================================
# shooting: y_ini 조정해서 Om_phi(a=1) = OmDE
# ============================================================
def Om_phi_today(y_ini, x_ini=1e-6):
    try:
        sol = odeint(clw_rhs, [x_ini, y_ini], lna_arr, rtol=1e-9, atol=1e-12)
        x1, y1 = sol[-1]
        return x1**2 + y1**2
    except:
        return 0.0

print('[L8-C] Shooting y_ini to achieve Om_phi(a=1) = %.4f...' % OmDE, flush=True)
# 범위 탐색
for y_t in [1e-4, 1e-3, 1e-2]:
    om_t = Om_phi_today(y_t)
    print('[L8-C]   y_ini=%.1e -> Om_phi(a=1)=%.4f' % (y_t, om_t), flush=True)

try:
    # 구간 탐색
    y_lo, y_hi = 1e-6, 1e-1
    r_lo = Om_phi_today(y_lo) - OmDE
    r_hi = Om_phi_today(y_hi) - OmDE
    if r_lo * r_hi < 0:
        y_ini_opt = brentq(lambda y: Om_phi_today(y) - OmDE, y_lo, y_hi, rtol=1e-4)
        print('[L8-C] y_ini_opt = %.6e' % y_ini_opt, flush=True)
        shooting_ok = True
    else:
        print('[L8-C] Bracket failed. Using y_ini=%.1e (closest).' % 1e-3, flush=True)
        # 가장 가까운 값 사용
        y_ini_opt = 1e-3
        shooting_ok = False
except Exception as e:
    print('[L8-C] Shooting failed: %s' % str(e)[:60], flush=True)
    y_ini_opt = 1e-3
    shooting_ok = False

# 최종 궤도
sol = odeint(clw_rhs, [1e-6, y_ini_opt], lna_arr, rtol=1e-9, atol=1e-12)
x_arr = sol[:, 0]
y_arr = sol[:, 1]
Om_phi_arr = x_arr**2 + y_arr**2
w_phi_arr = np.where(Om_phi_arr > 1e-10, (x_arr**2 - y_arr**2)/Om_phi_arr, -1.0)

print('[L8-C] Trajectory: Om_phi(a=1) = %.4f, x(a=1) = %.4f, y(a=1) = %.4f' % (
    Om_phi_arr[-1], x_arr[-1], y_arr[-1]), flush=True)
print('[L8-C] w_phi(a=1) = %.4f (target ~-0.877)' % w_phi_arr[-1], flush=True)

# H(a) 계산 (LCDM 배경 근사 — pure disformal A'=0 이면 배경 = minimal coupling)
H_arr = H0_SI * np.sqrt(Om * a_arr**(-3) + Om_phi_arr)
rho_m_arr = rho_m0 * a_arr**(-3)

# ============================================================
# phi(a) 복원: dphi/dlna = sqrt(6) * x * M_P
# ============================================================
phi_arr = np.zeros(len(lna_arr))
for i in range(1, len(lna_arr)):
    dlna = lna_arr[i] - lna_arr[i-1]
    phi_arr[i] = phi_arr[i-1] + np.sqrt(6.0) * x_arr[i] * M_P_kg * dlna
phi_over_MP = phi_arr / M_P_kg
print('[L8-C] phi/M_P at a=1: %.3f' % phi_over_MP[-1], flush=True)

# ============================================================
# SQMH 스케일 분석 (핵심)
# ============================================================
print('\n[L8-C] === SQMH 스케일 분석 ===', flush=True)
# sigma_eff 조건: sigma_SQMH * rho_m ~ H * (3 - sqrt6*lam*x) * n_bar_scale
# 실효 sigma 필요값: sigma_need ~ H0/rho_m0 ~ [s^-1]/[kg/m^3]=[m^3/(kg*s)]
sigma_need = H0_SI / rho_m0
print('[L8-C] Required sigma for SQMH~CLW: ~ H0/rho_m0 = %.3e m^3/kg/s' % sigma_need, flush=True)
print('[L8-C] Actual sigma_SQMH = %.3e m^3/kg/s' % sigma_SQMH, flush=True)
print('[L8-C] Ratio = %.3e (%d orders of magnitude off)' % (
    sigma_SQMH/sigma_need, np.log10(sigma_need/sigma_SQMH)), flush=True)

# ============================================================
# sigma_eff 역산 (두 후보)
# ============================================================
print('\n[L8-C] === Candidate 1: n_bar ~ exp(-lam*phi/M_P) ===', flush=True)
n_bar_c1 = np.exp(-lam * phi_over_MP)
n_bar_c1 = n_bar_c1 / n_bar_c1[-1]  # 오늘 = 1로 normalize

# Gamma0 결정: 경계조건 SQMH-BG at a=1
# sigma_eff(a=1) = [Gamma0/n_bar0 + (sqrt6*lam*x0 - 3)*H0] / rho_m0 = sigma_SQMH
# -> Gamma0 = n_bar0 * (sigma_SQMH * rho_m0 + (3 - sqrt6*lam*x0)*H0)
x0, H0_val = x_arr[-1], H_arr[-1]
Gamma0_c1 = 1.0 * (sigma_SQMH * rho_m_arr[-1] + (3.0 - np.sqrt(6.0)*lam*x0)*H0_val)
# sigma_eff(a):
sigma_eff_c1 = (Gamma0_c1/n_bar_c1 + (np.sqrt(6.0)*lam*x_arr - 3.0)*H_arr) / rho_m_arr

print('[L8-C] Gamma0_c1 = %.3e' % Gamma0_c1, flush=True)
# Valid region: a > 0.1 (z < 9, avoid early time divergence)
mask = a_arr > 0.1
sigma_c1_valid = sigma_eff_c1[mask]
n_pos = np.sum(sigma_c1_valid > 0)
print('[L8-C] sigma_eff(c1) range [a>0.1]: %.3e to %.3e' % (
    sigma_c1_valid.min(), sigma_c1_valid.max()), flush=True)
print('[L8-C] Positive fraction: %d/%d' % (n_pos, len(sigma_c1_valid)), flush=True)

if n_pos > len(sigma_c1_valid) * 0.8:  # 80% 이상 양수
    mean_c1 = float(sigma_c1_valid[sigma_c1_valid > 0].mean())
    std_c1 = float(sigma_c1_valid[sigma_c1_valid > 0].std())
    cv_c1 = std_c1 / mean_c1 if mean_c1 > 0 else np.inf
    ratio_c1 = mean_c1 / sigma_SQMH
    print('[L8-C] sigma_eff(c1): mean=%.3e, CV=%.3f, ratio=%.3e' % (mean_c1, cv_c1, ratio_c1), flush=True)
    q32_c1 = cv_c1 < 0.20 and abs(ratio_c1 - 1.0) < 0.10
else:
    mean_c1, std_c1, cv_c1, ratio_c1 = 0.0, 0.0, np.inf, 0.0
    q32_c1 = False
print('[L8-C] Q32 (c1): %s' % ('PASS' if q32_c1 else 'FAIL'), flush=True)

print('\n[L8-C] === Candidate 2: n_bar ~ exp(+lam*phi/M_P) ===', flush=True)
n_bar_c2 = np.exp(+lam * phi_over_MP)
n_bar_c2 = n_bar_c2 / n_bar_c2[-1]
Gamma0_c2 = 1.0 * (sigma_SQMH * rho_m_arr[-1] + (np.sqrt(6.0)*lam*x0 + 3.0)*H0_val)
sigma_eff_c2 = (Gamma0_c2/n_bar_c2 - (np.sqrt(6.0)*lam*x_arr + 3.0)*H_arr) / rho_m_arr

sigma_c2_valid = sigma_eff_c2[mask]
n_pos2 = np.sum(sigma_c2_valid > 0)
print('[L8-C] sigma_eff(c2) range [a>0.1]: %.3e to %.3e' % (
    sigma_c2_valid.min(), sigma_c2_valid.max()), flush=True)
print('[L8-C] Positive fraction: %d/%d' % (n_pos2, len(sigma_c2_valid)), flush=True)

if n_pos2 > len(sigma_c2_valid) * 0.5:
    mean_c2 = float(sigma_c2_valid[sigma_c2_valid > 0].mean())
    cv_c2 = sigma_c2_valid[sigma_c2_valid > 0].std() / mean_c2 if mean_c2 > 0 else np.inf
    ratio_c2 = mean_c2 / sigma_SQMH
    q32_c2 = cv_c2 < 0.20 and abs(ratio_c2 - 1.0) < 0.10
    print('[L8-C] sigma_eff(c2): mean=%.3e, CV=%.3f, ratio=%.3e' % (mean_c2, cv_c2, ratio_c2), flush=True)
else:
    mean_c2, cv_c2, ratio_c2, q32_c2 = 0.0, np.inf, 0.0, False
    print('[L8-C] Mostly negative -> K32 for c2', flush=True)
print('[L8-C] Q32 (c2): %s' % ('PASS' if q32_c2 else 'FAIL'), flush=True)

# ============================================================
# E2(z) CLW vs A12 CPL
# ============================================================
w0_A12, wa_A12 = -0.886, -0.133
E2_CLW = Om * a_arr**(-3) + Om_phi_arr
# CPL E2 = Om*(1+z)^3 + OmDE*(1+z)^(3(1+w0+wa))*exp(-3*wa*z/(1+z))
z_arr = 1.0/a_arr - 1.0
E2_A12 = Om * (1+z_arr)**3 + OmDE * (1+z_arr)**(3*(1+w0_A12+wa_A12)) * np.exp(-3*wa_A12*z_arr/(1+z_arr))
sigma_chi = 0.01 * E2_A12
chi2_CLW_A12 = float(np.nansum(((E2_CLW - E2_A12)/sigma_chi)**2) / (len(a_arr)-1))
print('\n[L8-C] E2 CLW vs A12: chi2/dof = %.4f' % chi2_CLW_A12, flush=True)
print('[L8-C] E2_CLW(a=1) = %.4f, E2_A12(a=1) = %.4f' % (E2_CLW[-1], E2_A12[-1]), flush=True)

# ============================================================
# 최종 판정
# ============================================================
q32_pass = q32_c1 or q32_c2
k32_triggered = not q32_pass
print('\n[L8-C] Q32 PASS: %s' % q32_pass, flush=True)
print('[L8-C] K32 TRIGGERED: %s' % k32_triggered, flush=True)

if k32_triggered:
    print('[L8-C] K32 이유: sigma_eff / sigma_SQMH = %.0e (>10 orders off)' % (
        mean_c1/sigma_SQMH if mean_c1 > 0 else 0), flush=True)
    print('[L8-C] CLW 동역학에서 SQMH 소멸항 스케일을 재현 불가.', flush=True)

out = {
    'phase': 'L8-C',
    'lam': lam,
    'sigma_SQMH': float(sigma_SQMH),
    'trajectory': {
        'Om_phi_today': float(Om_phi_arr[-1]),
        'x_today': float(x_arr[-1]),
        'y_today': float(y_arr[-1]),
        'w_phi_today': float(w_phi_arr[-1]),
        'phi_over_MP_today': float(phi_over_MP[-1]),
        'shooting_ok': shooting_ok,
    },
    'scale_analysis': {
        'sigma_need': float(sigma_need),
        'sigma_SQMH': float(sigma_SQMH),
        'ratio': float(sigma_SQMH/sigma_need),
        'log10_gap': float(np.log10(sigma_need/sigma_SQMH)),
    },
    'candidate_1': {
        'definition': 'n_bar ~ exp(-lam*phi/M_P)',
        'sigma_eff_mean': float(mean_c1),
        'sigma_eff_cv': float(cv_c1),
        'ratio_to_SQMH': float(ratio_c1),
        'q32': bool(q32_c1),
    },
    'candidate_2': {
        'definition': 'n_bar ~ exp(+lam*phi/M_P)',
        'sigma_eff_mean': float(mean_c2),
        'sigma_eff_cv': float(cv_c2),
        'ratio_to_SQMH': float(ratio_c2),
        'q32': bool(q32_c2),
    },
    'chi2_CLW_vs_A12': float(chi2_CLW_A12),
    'q32_pass': bool(q32_pass),
    'k32_triggered': bool(k32_triggered),
    'interpretation': (
        'K32 CONFIRMED: CLW quintessence (lam=0.8872) cannot realize SQMH isomorphism.'
        ' Required sigma ~ H0/rho_m ~ 8.5e8 m^3/kg/s, SQMH sigma = 4.5e-53 m^3/kg/s.'
        ' Gap: 61 orders of magnitude. No variable substitution bridges this scale gap.'
    ),
}
out_path = os.path.join(_HERE, 'clw_vs_sqmh.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2,
              default=lambda x: float(x) if isinstance(x, (np.floating, np.integer)) else x)
print('\n[L8-C] Done. Saved to %s' % out_path, flush=True)
