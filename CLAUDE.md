# SQMH Project Rules

## 재발방지

- DESI BAO 데이터: 반드시 github.com/CobayaSampler/bao_data 공식 파일 사용. 임의 추정값 절대 금지.
- BAO 거리 D_H = c/(H0*E(z)) 계산 시 단위: c[m/s] / (H0[s^-1] * E * Mpc[m]) = Mpc. 중간 km/s/Mpc 변환 하지 말 것.
- BAO 피팅은 D_V(BGS) + D_M/D_H(나머지) 13포인트 + 전체 공분산행렬 사용. D_V만으로 피팅 금지.
- print()에 유니코드(✓₀μ³⁻ 등) 사용 금지 → cp949 에러. matplotlib 라벨은 OK.
- n₀, μ 개별값은 SI에서 자기무모순 안됨. 곱 n₀μ만 물리적 의미 있음.
- w(z) 선도차수 2체결합만으로는 wₐ>0. wₐ<0 주장하려면 V(phi) 역학 필수.
- numpy 2.x: trapz → trapezoid.
- 시뮬레이션 결과가 base.md 주장과 다르면 정직하게 base.fix.md에 기록. 결과 왜곡 금지.
- IDE ODE convention: 변수는 omega=rho/rho_crit_0 (물리적 밀도). E^2=Omega_r(1+z)^4+omega_m+omega_de. **절대 omega_m*(1+z)^3 이중카운팅 금지.**
- E(z) 계산은 반드시 coupled ODE solver (odeint) 사용. ad hoc perturbative 근사 금지.
- IDE 피팅 시 xi_q 양수/음수 모두 탐색 + scipy.optimize 사용. 수동 grid scan만으로 결론 금지.
- xi_q<0은 w<-1 (phantom) → SQMH 물리 위반. 피팅 결과 보고 시 반드시 SQMH 정합성 (xi_q>0) 분리 표기.
- DESI w0-wa 타원은 DESI+CMB+SN 결합 결과. BAO-only 비교 시 반드시 "결합 분석" 명시.
- DESI DR2 공식값: w0=-0.757+/-0.058, wa=-0.83+0.24/-0.21 (DESI+Planck+DES-all). wa=-1.27은 DR1 혼동 오류.
- DESI DR1→DR2 값 변경 주의: DR2에서 wa가 크게 변동. 항상 arXiv 번호로 출처 명시.
- **sigma = 4*pi*G*t_P (SI)**. sigma = 4*pi*G 는 플랑크 단위 전용. SI에서 sigma[m³kg⁻¹s⁻¹] ≠ 4piG[m³kg⁻¹s⁻²].
- n₀μ = rho_Planck/(4pi) ≈ 4.1e95 kg/m³. 이전값 6.6e-44는 sigma=4piG 오류에서 파생, 사용 금지.
- v(r) = g(r)*t_P (유입속도 = 중력가속도 x 플랑크시간). v(r) = GM/r² 표기는 속도/가속도 혼동.
- 문서 작성 시 유니코드 깨짐 주의: 파일 저장 후 반드시 인코딩 확인.
