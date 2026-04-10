# Figure 12: DESI DR3 SQMH 사전예측

## 요약
DESI DR3 (2026-2027) 출시 전 기록하는 SQMH 사전예측. DESI DR2 BAO 피팅 결과 반영.

## 견고한 예측 (xi_q > 0, 모델 독립적)
1. **w >= -1 항상** -- phantom crossing 불가. sigma*n*rho_m >= 0 보장.
2. **이차 IDE**: Q proportional to rho_DE*rho_m -- 2체 질량작용법칙에서 유일하게 결정.
3. **w0 > -1** -- 비영 결합에서 필연.

## 선도차수 예측 (V(phi) 보정 가능)
4. **wa > 0** -- 선도차수 2체 모델. wa < 0은 V(phi) 감쇠 역학 필요 (미구현).

## DESI DR2 BAO 피팅 결과 반영
| 조건 | delta_chi2 vs LCDM | 비고 |
|------|-------------------|------|
| xi_q > 0 + Planck r_d (147.09) | **0** (개선 없음) | SQMH 물리적, 보수적 |
| xi_q > 0 + free r_d | **-4.83** | xi_q=0.04, r_d=149.8 Mpc |
| xi_q < 0 + Planck r_d | -2.85 | **SQMH 물리 위반 (phantom)** |

## 반증 기준
- **w < -1** 고신뢰도 확인 시 -> SQMH 반증
- **linear IDE** (Q proportional to rho_DE) 선호 시 -> 함수형 예측 실패
- **quadratic IDE 확인 + w >= -1** -> SQMH 강력 지지

## 데이터 출처
- DESI DR2: arXiv:2503.14738 (DESI Collaboration, 2025)
- BAO 데이터: github.com/CobayaSampler/bao_data/desi_bao_dr2/
- Planck 2018: arXiv:1807.06209

## 재생성
```
cd simulations && python desi_fitting.py
```
