# Figure 11: DESI DR2 BAO 피팅 -- LCDM vs SQMH Fluid IDE vs V(phi) Quintessence (Phase 1)

## 요약
DESI DR2 공식 BAO 데이터 피팅. 3가지 모델군 비교:
1. **LCDM** (베이스라인)
2. **SQMH Fluid IDE** — Q proportional to rho_DE*rho_m (기존 2체 결합)
3. **SQMH V(phi) Quintessence** — base.fix.class.md Phase 1 신규 (mass / Ratra-Peebles / exponential 3종)

## 결과

### Planck r_d 고정 (r_d = 147.09 Mpc)
| 모델 | chi2 (13점) | k | AIC | BIC | delta_chi2 vs LCDM |
|------|------------|---|-----|-----|-------------------|
| LCDM | 29.81 | 1 | 31.81 | 32.38 | -- |
| Fluid IDE (xi_q=-0.021, phantom) | 26.96 | 2 | 30.96 | 32.09 | -2.85 |
| **V_mass** (thawing) | **UNSTABLE** | 1 | -- | -- | backward anti-damping |
| **V_RP** (Ratra-Peebles: beta=+0.352, n=0.348) | **26.71** | 2 | **30.71** | 31.84 | **-3.10** |
| **V_exp** (exponential: beta=+0.355, lambda=0.345) | 26.77 | 2 | 30.77 | 31.90 | -3.04 |

### Delta_AIC vs LCDM (negative = better)
| 모델 | Delta_AIC |
|------|-----------|
| Fluid IDE | -0.85 |
| V_RP | **-1.10** (best among quintessence) |
| V_exp | -1.04 |

### Phase 1 판정
- **최우수 V(phi)**: Ratra-Peebles, Delta_AIC = -1.10
- **판정 기준** (base.fix.class.md §6.2):
  - Delta_AIC < -6: 강한 개선 (Path A 성공)
  - Delta_AIC < -2: 약한 개선
  - Delta_AIC > -2: **개선 없음**
- **결과**: Delta_AIC = -1.10 -> **NO improvement**

**Phase 1 결론**: background 수준 DESI DR2 BAO만으로는 V(phi) 형태 교체가 SQMH를 LCDM 대비 유의미하게 개선하지 못함. 경로 A(Ratra-Peebles tracker) 즉시 성공 실패. Phase 2 (CMB + 섭동) 및 Phase 3 (full joint likelihood) 필요.

### r_d 자유화 (Fluid IDE 전용 비교)
| 모델 | chi2 | best r_d (Mpc) | xi_q | 추가 param |
|------|------|----------------|------|-----------|
| LCDM | 14.44 | 148.69 | -- | 1 (r_d) |
| **Fluid IDE** | **9.61** | **149.79** | **+0.040** | 2 (r_d + xi_q) |

r_d 2.7 Mpc 이동 (Planck 대비 1.8%) 시 Delta_chi2 = -4.83. Hubble tension 맥락 독립 검증 필요.

### V_mass 불안정성 설명
Mass term V = (A/2)*phi^2는 thawing 형태. Klein-Gordon 방정식 phi_ddot + 3H*phi_dot + V' = 0은 정방향에선 감쇠(stable), 후방 적분(오늘 -> 과거)에선 **anti-damping** 이 돼 phi가 발산. 이는 수치적 문제가 아니라 thawing 동역학 자체의 특성. 정방향 shooting 구현은 Phase 2에서 CLASS 모듈을 통해 수행.

## 이론 배경 (thawing vs freezing)
- **Caldwell & Linder (2005)**: quintessence를 w(z) 궤적으로 분류
- **Thawing** (V_mass, V_exp 일부): w ~ -1에서 출발, 시간 진행에 따라 -1에서 이탈 -> **wa > 0**
- **Freezing** (V_RP = M^4/phi^n tracker): w > -1에서 출발, -1로 수렴 -> **wa < 0**
- SQMH 기본 라그랑지안 V = mass term은 thawing -> base.md §10.2 wa > 0 결과의 물리적 원인
- DESI DR2 관측 wa < 0 (4.2 sigma) -> freezing form 필요 -> Phase 1 Ratra-Peebles 시도 -> background 수준에선 미해결

## 방법
- **Fluid IDE**: coupled fluid ODE (odeint, rtol=1e-10), omega = rho/rho_crit_0
- **V(phi) quintessence**: `simulations/quintessence.py` 모듈. Amendola 2000 좌표계 (M_P=1, e-folds N=ln(a)). 후방 적분 (오늘 -> z~3.5), DOP853. V(phi) amplitude는 V_tilde(phi_0=1) = Omega_DE_0 으로 보정.
- **피팅**: scipy.optimize Nelder-Mead, 다중 시작점. 전체 13x13 공분산행렬 사용.
- **정보기준**: AIC = chi2 + 2k, BIC = chi2 + k*ln(13).

## 데이터 출처
- **DESI DR2 BAO**: arXiv:2503.14738 (DESI Collaboration, 2025)
- **데이터 파일**: github.com/CobayaSampler/bao_data/desi_bao_dr2/
- **Planck 2018**: arXiv:1807.06209 (H0=67.36, Omega_m=0.3153, r_d=147.09 Mpc)
- **DESI DR2 w0-wa**: w0=-0.757+/-0.058, wa=-0.83+0.24/-0.21 (DESI+Planck+DES-all, arXiv:2507.09981)
- **Quintessence 분류**: Caldwell & Linder, Phys. Rev. Lett. 95, 141301 (2005), astro-ph/0505494
- **Coupled quintessence**: Amendola, Phys. Rev. D 62, 043511 (2000), astro-ph/9908023
- **Ratra-Peebles tracker**: Ratra & Peebles, Phys. Rev. D 37, 3406 (1988)

## 재생성
```
cd simulations && python desi_fitting.py
```
