# L380 — P17 Tier B  V(n,t) extension toy

## 목표
SQMH 흡수율 밀도장 n(t) 에 slow-roll-like 질량항을 더한 toy potential
을 사용해 background w(z) 형상을 도출하고, DESI DR2 BAO 13포인트와의
chi^2 (전체 공분산) 을 측정한다.  DESI 발표값 w0=-0.757, wa=-0.83 와의
일관성 여부를 정직하게 보고한다.

## 사용자 지시 ansatz (toy)
V(n,t) = V_0 + (1/2) m_n^2 n^2

해석 (독립 도출):
- SQMH 에서 n 은 흡수율 밀도장 (mass-dim 1, 여기서는 dimensionless 로 환원).
- KG 방정식 : n_dd + 3 H n_d + V_,n = 0,  V_,n = m_n^2 n.
- 에너지밀도 / 압력 :
    rho = (1/2) n_d^2 + V,   p = (1/2) n_d^2 - V.
- w(n,t) = (K - V) / (K + V), K=(1/2) n_d^2.
- 초기조건 : matter-dominated era 에서 n=n_i (frozen), n_d=0.
  m_n^2 << H_0^2 한도에서 thawing 거동 → w(z=0) > -1, w_a < 0 부호.

## 자유 파라미터
- Omega_m  ∈ [0.25, 0.40]
- h        ∈ [0.62, 0.74]
- mu = m_n/H_0  ∈ [0.0, 1.5]
- xi  = V_0 / (3 H_0^2 M_Pl^2)  : closure 로 묶임 → Omega_de = 1-Omega_m 강제, 따라서 V_0 는 도출치 (free 아님).
- n_i  : 단위계 dimensionless, [0.05, 1.0]  (M_Pl 단위)

총 4 free (Omega_m, h, mu, n_i).

## 수치 절차
1. 배경 ODE forward shooting.  변수 N=ln a, n(N), n_N(N).
2. Friedmann closure : H^2 = (rho_m + rho_r + rho_n)/(3 M_Pl^2),
   여기서 rho_n = (1/2) H^2 n_N^2 + V.  → 한 번 implicit 풀이 후 forward.
3. z_grid : N=-3..0, dense 800 pt; cumulative_trapezoid 적분으로 D_M.
4. r_d 는 nuisance 로 amplitude marginalize (DESI 표준 trick: alpha=r_d_fid/r_d 로 곱 marginalize). 여기서는 fixed r_d=147.05 Mpc 사용 + Omega_m·h^2 가까이서 부드럽게. (Tier-B toy 이므로 r_d 정밀계산 생략.)
5. chi^2 = (d-m)^T Cov^-1 (d-m), d, Cov 는 desi_data.py 의 13×13 official.
6. CPL 추출 : rho_de_eff(z) = 3H^2 - rho_m - rho_r 에서 직접 w(z) → least_squares 로 (w0,wa) fit (z∈[0.01,1.2]).

## 통과 기준
- chi^2(DESI DR2) ≤ 17.0  (LCDM 21.4 대비 Δ≤-4.4 가 의미있는 개선).
- (w0, wa) 가 DESI 박스 (w0∈[-0.85,-0.66], wa∈[-1.07,-0.59]) 안.
- xi_q 부호 SQMH 정합 (rho_n>0, w>-1 thawing 이면 자동 만족).

## 위험 / 가드
- m_n>>H_0 oscillation regime 진입 시 w 평균 0 → matter-like, 의미 없음.  mu<=1.5 cap.
- n_i 너무 작으면 closure 만족 위해 V_0 > 3H_0^2 M_Pl^2 → 비물리.  n_i lower 0.05 cap + V_0>=0 검사.
- chi^2 가 LCDM 보다 *나쁘면* 정직하게 negative 결과 보고.
