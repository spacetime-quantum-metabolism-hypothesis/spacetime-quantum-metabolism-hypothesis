# -*- coding: utf-8 -*-
# CODE REVIEW: Bug-v Physics-v Repro-v Rules-v  [2026-04-11]
"""L8-N: 세 후보 (A12, C11D, C28) SQMH 동형 비교 통합.

각 서브파트 JSON 로드 -> 비교 테이블 출력 -> 통합 판정.
"""
from __future__ import annotations
import json, os
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))

def load(rel):
    path = os.path.join(_ROOT, rel)
    with open(path) as f:
        return json.load(f)

print('[L8-N] Loading L8 sub-results...', flush=True)
r_a12 = load('simulations/l8/a12/sqmh_ode_vs_erf.json')
r_c11d = load('simulations/l8/c11d/clw_vs_sqmh.json')
r_c28 = load('simulations/l8/c28/rr_vs_sqmh.json')

print('\n[L8-N] ===== L8 SQMH 역유도 통합 비교 =====', flush=True)
print('[L8-N] 대상: A12 (erf proxy) | C11D (CLW quintessence) | C28 (RR non-local)', flush=True)

# ============================================================
# 스케일 분석 요약
# ============================================================
print('\n[L8-N] --- 스케일 분석 ---', flush=True)
ratio_a12 = r_a12['scale_analysis']['ratio_SQMH_sink_to_Hubble']
ratio_c11d = r_c11d['scale_analysis']['ratio']
print('[L8-N] A12: sigma*rho_m/(3H0) = %.2e  (62 orders small)' % ratio_a12, flush=True)
print('[L8-N] C11D: sigma_SQMH/sigma_need = %.2e  (61 orders small)' % ratio_c11d, flush=True)
print('[L8-N] C28: RR auxiliary P ~ n_bar structurally (but E2_RR(a=1)=%.4f, not 1)' %
      r_c28['e2_comparison'].get('chi2_dof_RR_vs_A12', -1), flush=True)

# ============================================================
# 판정 요약
# ============================================================
print('\n[L8-N] --- 판정 ---', flush=True)
results = [
    ('A12', 'Q31', r_a12['q31_pass'], r_a12['chi2_dof']['SQMH_vs_A12'],
     'chi2/dof=%.2f (LCDM~SQMH bg). wa<0 not from bg ODE.' % r_a12['chi2_dof']['SQMH_vs_A12']),
    ('C11D', 'Q32', r_c11d['q32_pass'], 0.0,
     'sigma_eff < 0 everywhere. Scale gap 61 orders.'),
    ('C28', 'Q33', r_c28['q33_pass'], r_c28['isomorphism_fit']['mean_residual'],
     'Residual=100%%. E2_RR(a=1) wrong (simplified ODE limitation).'),
]

print('[L8-N] %-6s %-4s %-6s %-10s %s' % ('Cand', 'Q', 'PASS?', 'Metric', 'Remark'), flush=True)
print('[L8-N] ' + '-'*70, flush=True)
for cand, q, qpass, metric, remark in results:
    print('[L8-N] %-6s %-4s %-6s %-10s %s' % (
        cand, q, 'PASS' if qpass else 'FAIL', '%.3f' % metric, remark), flush=True)

# Kill summary
k31 = r_a12['k31_triggered']
k32 = r_c11d['k32_triggered']
k33 = r_c28['k33_triggered']
print('\n[L8-N] Kill 판정:', flush=True)
print('[L8-N] K31 (A12 bg ODE -> wa<0): %s' % ('TRIGGERED' if k31 else 'Not triggered'), flush=True)
print('[L8-N] K32 (C11D CLW -> SQMH sigma): %s' % ('TRIGGERED' if k32 else 'Not triggered'), flush=True)
print('[L8-N] K33 (C28 RR -> SQMH P<->n_bar): %s' % ('TRIGGERED' if k33 else 'Not triggered'), flush=True)

# ============================================================
# 핵심 물리 결론
# ============================================================
print('\n[L8-N] === 핵심 결론 ===', flush=True)
print('[L8-N] 1. SQMH sigma = 4pi*G*t_P 는 배경 우주론에 62자리 무시가능.', flush=True)
print('[L8-N] 2. SQMH 배경 ODE ~ LCDM (sigma->0 극한).', flush=True)
print('[L8-N] 3. A12 erf proxy / C11D CLW 에서 SQMH 역유도 불가.', flush=True)
print('[L8-N] 4. C28 RR: 연속방정식 구조 동형 (dP/dt+3HP=U <-> dn/dt+3Hn=Gamma0-sigma*n*rho_m)', flush=True)
print('[L8-N]    그러나 소스항 U ~ 상수 아님 (gamma0 스케일 내 변동). K33 판정.', flush=True)
print('[L8-N] 5. PRD Letter 진입 조건 (Q32 PASS) 미충족.', flush=True)
print('[L8-N] 6. JCAP 타깃 유지: 8인 합의 phenomenological proxy 포지셔닝.', flush=True)

# ============================================================
# 저장
# ============================================================
out = {
    'phase': 'L8-N',
    'method': 'L8_integration_comparison',
    'candidates': {
        'A12': {
            'Q31_pass': r_a12['q31_pass'],
            'K31_triggered': r_a12['k31_triggered'],
            'chi2_SQMH_vs_A12': r_a12['chi2_dof']['SQMH_vs_A12'],
            'scale_ratio': r_a12['scale_analysis']['ratio_SQMH_sink_to_Hubble'],
        },
        'C11D': {
            'Q32_pass': r_c11d['q32_pass'],
            'K32_triggered': r_c11d['k32_triggered'],
            'sigma_gap_orders': r_c11d['scale_analysis']['log10_gap'],
        },
        'C28': {
            'Q33_pass': r_c28['q33_pass'],
            'K33_triggered': r_c28['k33_triggered'],
            'isomorphism_residual': r_c28['isomorphism_fit']['mean_residual'],
        },
    },
    'overall': {
        'any_Q_pass': False,
        'PRD_Letter_condition': False,
        'JCAP_target': True,
        'key_conclusion': (
            'No surviving candidate can be analytically derived from SQMH fundamental equation.'
            ' sigma=4*pi*G*t_P is 62 orders too small for background cosmology.'
            ' All three candidates (A12, C11D, C28) confirmed as phenomenological proxies.'
        ),
    },
}
out_path = os.path.join(_HERE, 'l8_comparison.json')
with open(out_path, 'w') as f:
    json.dump(out, f, indent=2)
print('\n[L8-N] Done. Saved to %s' % out_path, flush=True)
