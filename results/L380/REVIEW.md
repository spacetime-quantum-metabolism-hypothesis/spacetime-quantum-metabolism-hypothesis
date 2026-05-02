# L380 — V(n,t) extension toy : 결과 정리 (정직)

## 한 줄
**부분 일관 — wa 부호와 magnitude 는 재현하지만, (w0, wa) 가 DESI DR2 박스 안에 동시에 들어가는 점은 없음. chi^2(DR2) 는 LCDM 대비 -1.34 개선.**

## 데이터
DESI DR2 BAO 13포인트 + 13×13 공분산
(simulations/desi_data.py, arXiv:2503.14738)

## ansatz
V(n,t) = V_0 + (1/2) m_n^2 n^2 (slow-roll-like).
무차원화 mu = m_n/H_0, n_i = 초기 (z~150) 필드값 (M_Pl 단위).
배경 ODE forward shooting + V_0 closure (E(z=0)=1) bisection.

## free parameter (4)
Omega_m, h, mu, n_i.  (V_0 는 closure 에서 도출되어 free 아님.)

## 스캔 결과
- LCDM best (free Omega_m, h):  Omega_m=0.2972, h=0.6906, chi^2 = **10.302**
- V(n,t) best:  Omega_m=0.300, h=0.680, mu=3.000, n_i=0.30
  - chi^2 = **8.958**, **Δchi^2 = -1.344**
  - (w0, wa) = (-0.940, -0.023),  w_today = -0.959
  - DESI 박스 통과 : NO  (wa 가 너무 작음)
- 톱-10 중 wa 매그니튜드 가장 큰 점 :
  Omega_m=0.310, h=0.670, mu=2.000, n_i=1.00
  - chi^2 = 9.450,  (w0, wa) = (-0.486, -0.828)
  - wa magnitude DESI -0.83 와 일치, **그러나 w0 = -0.486 이 박스 [-0.815,-0.699] 밖.**

## 통과 / 실패 판정
| 기준                         | 결과 |
|------------------------------|------|
| chi^2(DR2) ≤ 17.0           | PASS (8.96) |
| Δchi^2 vs LCDM 의미있음 (≤-4.4) | FAIL (-1.34) |
| (w0, wa) DESI 박스 동시 통과  | FAIL |
| wa<0 부호                    | PASS (전 톱-10) |

## 해석 (정직)
1. V(n,t) = V_0 + (1/2)m_n^2 n^2 toy 는 wa<0 의 *부호* 와
   |wa| 까지 -0.83 근처 magnitude 모두 재현 가능 (mu~2, n_i~1).
2. 그러나 동일 점에서 w_0 = -0.49 로 phantom 쪽이 아닌 quintessence
   심층, DESI 박스 (w0~-0.76) 와 분리.  모델이 박스 내부에 동시에
   들어가지는 못함.
3. chi^2 개선 -1.34 는 AICc 패널티 (4 → 2 추가 파라미터, ΔAICc≈+4)
   를 *못 넘김*. **데이터가 V(n,t) 확장을 정당화하지 않음.**
4. Tier B 결과 : *wa 형상 일관성 부분 PASS, 정량 일관성 FAIL.*
   Phase 5 hi_class full 에서 r_d 자기무모순 계산 + 성장 채널 추가
   하면 결론 갱신 필요.

## 재발방지
- Tier B 토이의 chi^2 개선이 AICc 패널티 못 넘으면 LCDM 채택.
- (w0,wa) 박스는 *동시 통과* 가 기준. 매그니튜드 단독 일치만으로
  "DESI 일관" 주장 금지.
- V_0 closure 는 brentq bracket [0, 20] 충분히 넓혀야 mu>=2 영역
  포착 (좁으면 valid 비율 폭락).
